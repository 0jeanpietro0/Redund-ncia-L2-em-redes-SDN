#!/usr/bin/env python3

from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.link import TCLink
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel


class TopologiaConvencional(Topo):

    def build(self):

        # Switch convencional em modo standalone.
        # Sem controlador SDN.
        s1 = self.addSwitch(
            's1',
            cls=OVSSwitch,
            failMode='standalone'
        )

        # Mesmos 4 hosts e mesmos enderecos da topologia SDN
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')
        h3 = self.addHost('h3', ip='10.0.0.3/24')
        h4 = self.addHost('h4', ip='10.0.0.4/24')

        # Mesmas conexoes do cenario SDN
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)
        self.addLink(h4, s1)


def run():

    topo = TopologiaConvencional()

    net = Mininet(
        topo=topo,
        controller=None,
        switch=OVSSwitch,
        link=TCLink,
        autoSetMacs=True
    )

    net.start()

    print("\n=== Topologia Convencional ===")
    print("Sem controlador SDN")
    print("Switch OVS em modo standalone")
    print("h1: 10.0.0.1")
    print("h2: 10.0.0.2")
    print("h3: 10.0.0.3")
    print("h4: 10.0.0.4")
    print("==============================\n")

    CLI(net)

    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
