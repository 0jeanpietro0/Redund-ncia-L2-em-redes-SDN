#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Topologia manual - Malha completa K4 com SDN + ARP Proxy v3.7.

4 switches em malha completa, 8 hosts:
    s1: h1, h2
    s2: h3, h4
    s3: h5, h6
    s4: h7, h8

Enlaces host-switch:
    100 Mbit/s, 0.2 ms

Enlaces inter-switch:
    10 Mbit/s, 1 ms

Enlaces entre switches:
    s1-s2, s1-s3, s1-s4,
    s2-s3, s2-s4, s3-s4

O script apenas cria a topologia e abre o CLI.
Nenhum teste é executado automaticamente.

Antes de executar esta topologia, iniciar o controlador:
    ryu-manager arp_proxy_v3_7.py --observe-links
"""

from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel


HOST_BW = 100
INTER_BW = 10
HOST_DELAY = '0.2ms'
INTER_DELAY = '1ms'


def run():

    net = Mininet(
        controller=None,
        switch=OVSSwitch,
        link=TCLink,
        build=False,
        autoSetMacs=False
    )

    # ---------------------------------------------------------
    # CONTROLADOR RYU
    # ---------------------------------------------------------

    c0 = net.addController(
        'c0',
        controller=RemoteController,
        ip='127.0.0.1',
        port=6653
    )

    # ---------------------------------------------------------
    # HOSTS
    # ---------------------------------------------------------

    hosts = {}

    for i in range(1, 9):
        hosts[f'h{i}'] = net.addHost(
            f'h{i}',
            ip=f'10.0.0.{i}/24',
            mac=f'00:00:00:00:00:{i:02x}'
        )

    # ---------------------------------------------------------
    # SWITCHES OPENFLOW
    # ---------------------------------------------------------

    switches = {}

    for i in range(1, 5):
        switches[f's{i}'] = net.addSwitch(
            f's{i}',
            protocols='OpenFlow13',
            failMode='secure'
        )

    s1 = switches['s1']
    s2 = switches['s2']
    s3 = switches['s3']
    s4 = switches['s4']

    # ---------------------------------------------------------
    # HOSTS -> SWITCHES
    # Portas 1 e 2 de cada switch
    # ---------------------------------------------------------

    net.addLink(hosts['h1'], s1, port2=1,
                bw=HOST_BW, delay=HOST_DELAY, max_queue_size=1000)
    net.addLink(hosts['h2'], s1, port2=2,
                bw=HOST_BW, delay=HOST_DELAY, max_queue_size=1000)

    net.addLink(hosts['h3'], s2, port2=1,
                bw=HOST_BW, delay=HOST_DELAY, max_queue_size=1000)
    net.addLink(hosts['h4'], s2, port2=2,
                bw=HOST_BW, delay=HOST_DELAY, max_queue_size=1000)

    net.addLink(hosts['h5'], s3, port2=1,
                bw=HOST_BW, delay=HOST_DELAY, max_queue_size=1000)
    net.addLink(hosts['h6'], s3, port2=2,
                bw=HOST_BW, delay=HOST_DELAY, max_queue_size=1000)

    net.addLink(hosts['h7'], s4, port2=1,
                bw=HOST_BW, delay=HOST_DELAY, max_queue_size=1000)
    net.addLink(hosts['h8'], s4, port2=2,
                bw=HOST_BW, delay=HOST_DELAY, max_queue_size=1000)

    # ---------------------------------------------------------
    # MALHA COMPLETA K4
    # Portas 3, 4 e 5 de cada switch
    # ---------------------------------------------------------

    net.addLink(s1, s2, port1=3, port2=3,
                bw=INTER_BW, delay=INTER_DELAY, max_queue_size=1000)

    net.addLink(s1, s3, port1=4, port2=3,
                bw=INTER_BW, delay=INTER_DELAY, max_queue_size=1000)

    net.addLink(s1, s4, port1=5, port2=3,
                bw=INTER_BW, delay=INTER_DELAY, max_queue_size=1000)

    net.addLink(s2, s3, port1=4, port2=4,
                bw=INTER_BW, delay=INTER_DELAY, max_queue_size=1000)

    net.addLink(s2, s4, port1=5, port2=4,
                bw=INTER_BW, delay=INTER_DELAY, max_queue_size=1000)

    net.addLink(s3, s4, port1=5, port2=5,
                bw=INTER_BW, delay=INTER_DELAY, max_queue_size=1000)

    # ---------------------------------------------------------
    # INICIALIZAÇÃO
    # ---------------------------------------------------------

    net.build()

    c0.start()

    for name, sw in switches.items():

        sw.start([c0])

        # O cenário SDN não utiliza STP/RSTP.
        sw.cmd(f'ovs-vsctl set Bridge {name} stp_enable=false')
        sw.cmd(f'ovs-vsctl set Bridge {name} rstp_enable=false')

    # ---------------------------------------------------------
    # INFORMAÇÕES PARA TESTES MANUAIS
    # ---------------------------------------------------------

    print('\n===========================================================')
    print(' TOPOLOGIA MANUAL - MALHA K4 / SDN + ARP PROXY v3.7')
    print('===========================================================')
    print('s1: h1 h2')
    print('s2: h3 h4')
    print('s3: h5 h6')
    print('s4: h7 h8')
    print('')
    print('Malha completa:')
    print('s1-s2  s1-s3  s1-s4')
    print('s2-s3  s2-s4')
    print('s3-s4')
    print('')
    print('Hosts -> switches: 100 Mbit/s | 0.2 ms')
    print('Switch -> switch:  10 Mbit/s | 1 ms')
    print('')
    print('Controlador esperado:')
    print('  ryu-manager arp_proxy_v3_7.py --observe-links')
    print('')
    print('Verificar flows:')
    print('  sh ovs-ofctl -O OpenFlow13 dump-flows s1')
    print('  sh ovs-ofctl -O OpenFlow13 dump-flows s2')
    print('  sh ovs-ofctl -O OpenFlow13 dump-flows s3')
    print('  sh ovs-ofctl -O OpenFlow13 dump-flows s4')
    print('')
    print('Exemplo de ping:')
    print('  h3 ping -c 20 10.0.0.5')
    print('')
    print('Exemplo de falha:')
    print('  link s1 s2 down')
    print('  link s1 s2 up')
    print('===========================================================\n')

    CLI(net)

    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
