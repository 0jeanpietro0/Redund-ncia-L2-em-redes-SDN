#!/usr/bin/python3

from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel


def run():

    net = Mininet(
        controller=None,
        switch=OVSSwitch,
        build=False,
        autoSetMacs=False
    )

    print("*** Criando hosts")

    h1 = net.addHost(
        'h1',
        ip='10.0.0.1/24',
        mac='00:00:00:00:00:01'
    )

    h2 = net.addHost(
        'h2',
        ip='10.0.0.2/24',
        mac='00:00:00:00:00:02'
    )

    h3 = net.addHost(
        'h3',
        ip='10.0.0.3/24',
        mac='00:00:00:00:00:03'
    )

    h4 = net.addHost(
        'h4',
        ip='10.0.0.4/24',
        mac='00:00:00:00:00:04'
    )

    print("*** Criando switches")

    s1 = net.addSwitch(
        's1',
        failMode='standalone'
    )

    s2 = net.addSwitch(
        's2',
        failMode='standalone'
    )

    print("*** Criando links")

    net.addLink(h1, s1)
    net.addLink(h2, s1)

    net.addLink(s1, s2)

    net.addLink(h3, s2)
    net.addLink(h4, s2)

    print("*** Iniciando rede")

    net.build()

    s1.start([])
    s2.start([])

    print("\n=== Topologia Convencional - 2 Switches ===")
    print("Sem controlador SDN")
    print("OVS standalone")
    print("")
    print("h1: 10.0.0.1 -> s1")
    print("h2: 10.0.0.2 -> s1")
    print("h3: 10.0.0.3 -> s2")
    print("h4: 10.0.0.4 -> s2")
    print("s1 <-> s2")
    print("============================================\n")

    CLI(net)

    print("*** Encerrando rede")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()