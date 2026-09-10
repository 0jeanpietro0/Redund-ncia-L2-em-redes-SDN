#!/usr/bin/env python3

from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.link import TCLink
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel


class TopologiaARPProxy(Topo):

    def build(self):

        # Switch Open vSwitch usando OpenFlow 1.3
        s1 = self.addSwitch(
            's1',
            cls=OVSSwitch,
            protocols='OpenFlow13'
        )

        # Quatro hosts na mesma rede IPv4
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')
        h3 = self.addHost('h3', ip='10.0.0.3/24')
        h4 = self.addHost('h4', ip='10.0.0.4/24')

        # Todos os hosts conectados ao mesmo switch
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)
        self.addLink(h4, s1)


def run():

    topo = TopologiaARPProxy()

    net = Mininet(
        topo=topo,
        controller=None,
        switch=OVSSwitch,
        link=TCLink,
        autoSetMacs=True
    )

    # Controlador Ryu executado externamente
    c0 = net.addController(
        name='c0',
        controller=RemoteController,
        ip='127.0.0.1',
        port=6633
    )

    net.start()

    # Garante OpenFlow 1.3 no OVS
    for sw in net.switches:
        sw.cmd(
            'ovs-vsctl set bridge',
            sw.name,
            'protocols=OpenFlow13'
        )

    print("\n=== Topologia ARP Proxy ===")
    print("h1: 10.0.0.1")
    print("h2: 10.0.0.2")
    print("h3: 10.0.0.3")
    print("h4: 10.0.0.4")
    print("===========================\n")

    CLI(net)

    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
