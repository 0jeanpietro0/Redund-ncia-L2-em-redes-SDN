from collections import deque

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import (
    CONFIG_DISPATCHER,
    MAIN_DISPATCHER,
    DEAD_DISPATCHER
)
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3

from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import arp

from ryu.topology import event


class ARPProxy(app_manager.RyuApp):

    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(ARPProxy, self).__init__(*args, **kwargs)

        # IP -> {"mac": ..., "dpid": ..., "port": ...}
        self.arp_table = {}

        # DPID -> datapath (somente switches atualmente ativos)
        self.datapaths = {}

        # DPID -> [portas]
        self.switch_ports = {}

        # Portas usadas em enlaces switch-switch
        self.switch_links = set()

        # adjacency[s1][s2] = porta de s1 que leva até s2
        self.adjacency = {}

        # ARP Requests que chegaram antes de PortDesc estar pronto
        self.pending_discoveries = []

    # ---------------------------------------------------------
    # API PARA OUTROS SCRIPTS
    # ---------------------------------------------------------

    def get_hosts(self):
        return self.arp_table

    def get_host(self, ip):
        return self.arp_table.get(ip)

    def get_switch_ports(self):
        return self.switch_ports

    def get_links(self):
        return self.switch_links

    def get_adjacency(self):
        return self.adjacency

    # ---------------------------------------------------------
    # SWITCH FEATURES
    # ---------------------------------------------------------

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        """Instala somente a regra que envia ARP ao controlador."""

        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch(eth_type=0x0806)
        actions = [
            parser.OFPActionOutput(
                ofproto.OFPP_CONTROLLER,
                ofproto.OFPCML_NO_BUFFER
            )
        ]

        self.add_flow(datapath, 100, match, actions)

    # ---------------------------------------------------------
    # REGISTRO DINÂMICO DE SWITCHES
    # ---------------------------------------------------------

    @set_ev_cls(
        ofp_event.EventOFPStateChange,
        [MAIN_DISPATCHER, DEAD_DISPATCHER]
    )
    def state_change_handler(self, ev):
        datapath = ev.datapath
        dpid = datapath.id

        if ev.state == MAIN_DISPATCHER:
            if dpid not in self.datapaths:
                self.datapaths[dpid] = datapath
                self.switch_ports.setdefault(dpid, [])
                self.adjacency.setdefault(dpid, {})

                self.logger.info(
                    "Switch %s conectado | total ativos: %s | switches: %s",
                    dpid,
                    len(self.datapaths),
                    sorted(self.datapaths.keys())
                )

            self.request_ports(datapath)

        elif ev.state == DEAD_DISPATCHER:
            if dpid in self.datapaths:
                self.datapaths.pop(dpid, None)
                self.switch_ports.pop(dpid, None)
                self.adjacency.pop(dpid, None)

                self.switch_links = {
                    (sw, port)
                    for sw, port in self.switch_links
                    if sw != dpid
                }

                for neighbors in self.adjacency.values():
                    neighbors.pop(dpid, None)

                hosts_to_remove = [
                    ip
                    for ip, host in self.arp_table.items()
                    if host["dpid"] == dpid
                ]

                for ip in hosts_to_remove:
                    self.arp_table.pop(ip, None)

                self.pending_discoveries = [
                    item
                    for item in self.pending_discoveries
                    if item["src_dpid"] != dpid
                ]

                self.logger.info(
                    "Switch %s desconectado | total ativos: %s | switches: %s",
                    dpid,
                    len(self.datapaths),
                    sorted(self.datapaths.keys())
                )

    # ---------------------------------------------------------
    # PORT DESC
    # ---------------------------------------------------------

    def request_ports(self, datapath):
        parser = datapath.ofproto_parser
        req = parser.OFPPortDescStatsRequest(datapath)
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPPortDescStatsReply, MAIN_DISPATCHER)
    def port_desc_stats_reply_handler(self, ev):
        datapath = ev.msg.datapath
        dpid = datapath.id

        ports = []

        for p in ev.msg.body:
            # Ignora portas especiais do OpenFlow.
            if p.port_no < 4294967294:
                ports.append(p.port_no)

        ports.sort()
        self.switch_ports[dpid] = ports

        self.logger.info(
            "Switch %s portas atualizadas: %s",
            dpid,
            ports
        )

        self.process_pending_discoveries()

    # ---------------------------------------------------------
    # PRONTIDÃO DOS SWITCHES
    # ---------------------------------------------------------

    def switches_ready(self):
        if not self.datapaths:
            return False

        for dpid in self.datapaths:
            if not self.switch_ports.get(dpid, []):
                return False

        return True

    # ---------------------------------------------------------
    # ARP DISCOVERY PENDENTE
    # ---------------------------------------------------------

    def queue_pending_discovery(
        self,
        packet_data,
        src_dpid,
        in_port,
        src_ip,
        dst_ip
    ):
        # Evita duplicar a mesma descoberta por retransmissões ARP.
        for item in self.pending_discoveries:
            if (
                item["src_dpid"] == src_dpid
                and item["in_port"] == in_port
                and item["src_ip"] == src_ip
                and item["dst_ip"] == dst_ip
            ):
                return

        self.pending_discoveries.append(
            {
                "data": packet_data,
                "src_dpid": src_dpid,
                "in_port": in_port,
                "src_ip": src_ip,
                "dst_ip": dst_ip
            }
        )

        self.logger.info(
            "ARP %s -> %s aguardando PortDesc | pendentes: %s",
            src_ip,
            dst_ip,
            len(self.pending_discoveries)
        )

    def process_pending_discoveries(self):
        if not self.switches_ready():
            return

        if not self.pending_discoveries:
            return

        pending = self.pending_discoveries[:]
        self.pending_discoveries.clear()

        self.logger.info(
            "Topologia pronta | processando %s descoberta(s) ARP pendente(s)",
            len(pending)
        )

        for discovery in pending:
            if discovery["src_dpid"] not in self.datapaths:
                continue

            self.edge_discovery(
                packet_data=discovery["data"],
                src_dpid=discovery["src_dpid"],
                in_port=discovery["in_port"],
                dst_ip=discovery["dst_ip"]
            )

    # ---------------------------------------------------------
    # LINKS ENTRE SWITCHES
    # ---------------------------------------------------------

    @set_ev_cls(event.EventLinkAdd)
    def link_add_handler(self, ev):
        link = ev.link

        src_dpid = link.src.dpid
        src_port = link.src.port_no
        dst_dpid = link.dst.dpid
        dst_port = link.dst.port_no

        self.switch_links.add((src_dpid, src_port))
        self.switch_links.add((dst_dpid, dst_port))

        self.adjacency.setdefault(src_dpid, {})
        self.adjacency.setdefault(dst_dpid, {})

        self.adjacency[src_dpid][dst_dpid] = src_port
        self.adjacency[dst_dpid][src_dpid] = dst_port

        self.logger.info(
            "Link detectado: s%s:%s <-> s%s:%s",
            src_dpid,
            src_port,
            dst_dpid,
            dst_port
        )

    @set_ev_cls(event.EventLinkDelete)
    def link_delete_handler(self, ev):
        link = ev.link

        src_dpid = link.src.dpid
        src_port = link.src.port_no
        dst_dpid = link.dst.dpid
        dst_port = link.dst.port_no

        self.switch_links.discard((src_dpid, src_port))
        self.switch_links.discard((dst_dpid, dst_port))

        if src_dpid in self.adjacency:
            self.adjacency[src_dpid].pop(dst_dpid, None)

        if dst_dpid in self.adjacency:
            self.adjacency[dst_dpid].pop(src_dpid, None)

        self.logger.info(
            "Link removido: s%s:%s <-> s%s:%s",
            src_dpid,
            src_port,
            dst_dpid,
            dst_port
        )

    # ---------------------------------------------------------
    # ADD FLOW
    # ---------------------------------------------------------

    def add_flow(
        self,
        datapath,
        priority,
        match,
        actions,
        idle_timeout=0,
        hard_timeout=0
    ):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [
            parser.OFPInstructionActions(
                ofproto.OFPIT_APPLY_ACTIONS,
                actions
            )
        ]

        mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=priority,
            match=match,
            instructions=inst,
            idle_timeout=idle_timeout,
            hard_timeout=hard_timeout
        )

        datapath.send_msg(mod)

    # ---------------------------------------------------------
    # CÁLCULO DE CAMINHO
    # ---------------------------------------------------------

    def get_path(self, src_dpid, dst_dpid):
        """Menor caminho em número de saltos usando BFS."""

        if src_dpid == dst_dpid:
            return [src_dpid]

        visited = {src_dpid}
        queue = deque([(src_dpid, [src_dpid])])

        while queue:
            current, path = queue.popleft()

            for neighbor in self.adjacency.get(current, {}):
                if neighbor in visited:
                    continue

                new_path = path + [neighbor]

                if neighbor == dst_dpid:
                    return new_path

                visited.add(neighbor)
                queue.append((neighbor, new_path))

        return None

    # ---------------------------------------------------------
    # ENCAMINHAMENTO IPv4
    # ---------------------------------------------------------

    def install_ipv4_path(self, src_ip, dst_ip):
        if src_ip not in self.arp_table:
            return False

        if dst_ip not in self.arp_table:
            return False

        src = self.arp_table[src_ip]
        dst = self.arp_table[dst_ip]

        src_dpid = src["dpid"]
        dst_dpid = dst["dpid"]

        path = self.get_path(src_dpid, dst_dpid)

        if not path:
            self.logger.warning(
                "Nenhum caminho encontrado entre switch %s e switch %s",
                src_dpid,
                dst_dpid
            )
            return False

        for index, sw_dpid in enumerate(path):
            datapath = self.datapaths.get(sw_dpid)

            if not datapath:
                self.logger.warning(
                    "Datapath do switch %s não encontrado",
                    sw_dpid
                )
                return False

            parser = datapath.ofproto_parser

            if index == len(path) - 1:
                out_port = dst["port"]
            else:
                next_dpid = path[index + 1]
                out_port = self.adjacency[sw_dpid][next_dpid]

            match = parser.OFPMatch(
                eth_type=0x0800,
                eth_src=src["mac"],
                eth_dst=dst["mac"],
                ipv4_src=src_ip,
                ipv4_dst=dst_ip
            )

            actions = [parser.OFPActionOutput(out_port)]

            self.add_flow(
                datapath,
                priority=50,
                match=match,
                actions=actions,
                idle_timeout=60
            )

            self.logger.info(
                "Flow instalado: s%s | %s -> %s | saída %s",
                sw_dpid,
                src_ip,
                dst_ip,
                out_port
            )

        self.logger.info(
            "Caminho IPv4 instalado: %s -> %s | switches %s",
            src_ip,
            dst_ip,
            path
        )

        return True

    def install_bidirectional_ipv4_path(self, ip_a, ip_b):
        forward = self.install_ipv4_path(ip_a, ip_b)
        reverse = self.install_ipv4_path(ip_b, ip_a)
        return forward and reverse

    # ---------------------------------------------------------
    # ENVIO DIRETO PARA HOST
    # ---------------------------------------------------------

    def send_packet_to_host(self, msg_data, host):
        datapath = self.datapaths.get(host["dpid"])

        if not datapath:
            return

        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto

        actions = [parser.OFPActionOutput(host["port"])]

        out = parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=ofproto.OFP_NO_BUFFER,
            in_port=ofproto.OFPP_CONTROLLER,
            actions=actions,
            data=msg_data
        )

        datapath.send_msg(out)

    # ---------------------------------------------------------
    # EDGE DISCOVERY
    # ---------------------------------------------------------

    def edge_discovery(self, packet_data, src_dpid, in_port, dst_ip=None):
        """
        Envia o ARP Request somente às portas edge.

        Não envia:
        - à porta de origem;
        - às portas que pertencem a links switch-switch.
        """

        self.logger.info(
            "Executando Edge Discovery | destino: %s | switches ativos: %s",
            dst_ip,
            sorted(self.datapaths.keys())
        )

        for sw_dpid, ports in self.switch_ports.items():
            dp = self.datapaths.get(sw_dpid)

            if not dp:
                continue

            parser = dp.ofproto_parser
            ofproto = dp.ofproto

            for port in ports:
                if sw_dpid == src_dpid and port == in_port:
                    continue

                if (sw_dpid, port) in self.switch_links:
                    continue

                actions = [parser.OFPActionOutput(port)]

                out = parser.OFPPacketOut(
                    datapath=dp,
                    buffer_id=ofproto.OFP_NO_BUFFER,
                    in_port=ofproto.OFPP_CONTROLLER,
                    actions=actions,
                    data=packet_data
                )

                dp.send_msg(out)

    # ---------------------------------------------------------
    # PACKET IN
    # ---------------------------------------------------------

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath

        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto

        dpid = datapath.id
        in_port = msg.match["in_port"]

        pkt = packet.Packet(msg.data)
        arp_pkt = pkt.get_protocol(arp.arp)

        # Este aplicativo trata somente ARP via Packet-In.
        if not arp_pkt:
            return

        src_ip = arp_pkt.src_ip
        src_mac = arp_pkt.src_mac

        # -----------------------------------------------------
        # APRENDER HOST
        # -----------------------------------------------------

        self.arp_table[src_ip] = {
            "mac": src_mac,
            "dpid": dpid,
            "port": in_port
        }

        self.logger.info(
            "Aprendido %s -> %s no switch %s porta %s",
            src_ip,
            src_mac,
            dpid,
            in_port
        )

        # -----------------------------------------------------
        # ARP REQUEST
        # -----------------------------------------------------

        if arp_pkt.opcode == arp.ARP_REQUEST:
            dst_ip = arp_pkt.dst_ip

            # Destino conhecido: responde como ARP Proxy.
            if dst_ip in self.arp_table:
                dst = self.arp_table[dst_ip]

                self.install_bidirectional_ipv4_path(src_ip, dst_ip)

                self.logger.info(
                    "Respondendo ARP Proxy: %s pergunta por %s",
                    src_ip,
                    dst_ip
                )

                arp_reply = arp.arp(
                    opcode=arp.ARP_REPLY,
                    src_mac=dst["mac"],
                    src_ip=dst_ip,
                    dst_mac=src_mac,
                    dst_ip=src_ip
                )

                eth_reply = ethernet.ethernet(
                    ethertype=0x0806,
                    dst=src_mac,
                    src=dst["mac"]
                )

                p = packet.Packet()
                p.add_protocol(eth_reply)
                p.add_protocol(arp_reply)
                p.serialize()

                actions = [parser.OFPActionOutput(in_port)]

                out = parser.OFPPacketOut(
                    datapath=datapath,
                    buffer_id=ofproto.OFP_NO_BUFFER,
                    in_port=ofproto.OFPP_CONTROLLER,
                    actions=actions,
                    data=p.data
                )

                datapath.send_msg(out)

            # Destino desconhecido: edge discovery.
            else:
                self.logger.info(
                    "Destino %s desconhecido: preparando Edge Discovery",
                    dst_ip
                )

                if not self.switches_ready():
                    self.queue_pending_discovery(
                        packet_data=msg.data,
                        src_dpid=dpid,
                        in_port=in_port,
                        src_ip=src_ip,
                        dst_ip=dst_ip
                    )

                    for dp in self.datapaths.values():
                        self.request_ports(dp)

                    return

                self.edge_discovery(
                    packet_data=msg.data,
                    src_dpid=dpid,
                    in_port=in_port,
                    dst_ip=dst_ip
                )

        # -----------------------------------------------------
        # ARP REPLY
        # -----------------------------------------------------

        elif arp_pkt.opcode == arp.ARP_REPLY:
            dst_ip = arp_pkt.dst_ip

            self.logger.info(
                "ARP Reply recebido: %s respondeu para %s",
                src_ip,
                dst_ip
            )

            if dst_ip in self.arp_table:
                requester = self.arp_table[dst_ip]

                self.install_bidirectional_ipv4_path(dst_ip, src_ip)

                self.send_packet_to_host(msg.data, requester)

                self.logger.info(
                    "ARP Reply entregue diretamente a %s",
                    dst_ip
                )
