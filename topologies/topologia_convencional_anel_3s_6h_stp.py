#!/usr/bin/env python3
from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from time import sleep

def run():
    net = Mininet(
        controller=None,
        switch=OVSSwitch,
        build=False,
        autoSetMacs=False
    )

    # Hosts
    h1 = net.addHost('h1', ip='10.0.0.1/24', mac='00:00:00:00:00:01')
    h2 = net.addHost('h2', ip='10.0.0.2/24', mac='00:00:00:00:00:02')
    h3 = net.addHost('h3', ip='10.0.0.3/24', mac='00:00:00:00:00:03')
    h4 = net.addHost('h4', ip='10.0.0.4/24', mac='00:00:00:00:00:04')
    h5 = net.addHost('h5', ip='10.0.0.5/24', mac='00:00:00:00:00:05')
    h6 = net.addHost('h6', ip='10.0.0.6/24', mac='00:00:00:00:00:06')

    # Switches convencionais com STP
    s1 = net.addSwitch('s1', failMode='standalone', stp=True)
    s2 = net.addSwitch('s2', failMode='standalone', stp=True)
    s3 = net.addSwitch('s3', failMode='standalone', stp=True)

    # Hosts -> switches
    net.addLink(h1, s1)
    net.addLink(h2, s1)

    net.addLink(h3, s2)
    net.addLink(h4, s2)

    net.addLink(h5, s3)
    net.addLink(h6, s3)

    # Anel
    net.addLink(s1, s2)
    net.addLink(s2, s3)
    net.addLink(s3, s1)

    net.build()

    s1.start([])
    s2.start([])
    s3.start([])

    print("\n=== Convencional - 3 switches em anel / STP ATIVO ===")
    print("s1: h1 h2")
    print("s2: h3 h4")
    print("s3: h5 h6")
    print("Anel: s1 <-> s2 <-> s3 <-> s1")
    print("")
    print("ATENCAO: aguarde a convergencia do STP antes dos testes.")
    print("Use: sh ovs-appctl stp/show s1")
    print("     sh ovs-appctl stp/show s2")
    print("     sh ovs-appctl stp/show s3")
    print("=========================================================\n")

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
