#!/usr/bin/env python3

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

    # ---------------------------------------------------------
    # HOSTS
    # ---------------------------------------------------------

    h1 = net.addHost('h1', ip='10.0.0.1/24', mac='00:00:00:00:00:01')
    h2 = net.addHost('h2', ip='10.0.0.2/24', mac='00:00:00:00:00:02')

    h3 = net.addHost('h3', ip='10.0.0.3/24', mac='00:00:00:00:00:03')
    h4 = net.addHost('h4', ip='10.0.0.4/24', mac='00:00:00:00:00:04')

    h5 = net.addHost('h5', ip='10.0.0.5/24', mac='00:00:00:00:00:05')
    h6 = net.addHost('h6', ip='10.0.0.6/24', mac='00:00:00:00:00:06')

    # ---------------------------------------------------------
    # SWITCHES CONVENCIONAIS
    # ---------------------------------------------------------

    s1 = net.addSwitch('s1', failMode='standalone')
    s2 = net.addSwitch('s2', failMode='standalone')
    s3 = net.addSwitch('s3', failMode='standalone')

    # ---------------------------------------------------------
    # HOSTS -> SWITCHES
    # ---------------------------------------------------------

    net.addLink(h1, s1)
    net.addLink(h2, s1)

    net.addLink(h3, s2)
    net.addLink(h4, s2)

    net.addLink(h5, s3)
    net.addLink(h6, s3)

    # ---------------------------------------------------------
    # ANEL ENTRE SWITCHES
    # ---------------------------------------------------------

    net.addLink(s1, s2)
    net.addLink(s2, s3)
    net.addLink(s3, s1)

    # ---------------------------------------------------------
    # INICIALIZAÇÃO
    # ---------------------------------------------------------

    net.build()

    s1.start([])
    s2.start([])
    s3.start([])

    # ---------------------------------------------------------
    # RSTP
    # ---------------------------------------------------------
    # Garante STP clássico desativado e habilita RSTP no OVS.
    #
    # Fazemos isso diretamente via ovs-vsctl para deixar claro
    # qual protocolo está sendo usado em cada bridge.

    for sw in (s1, s2, s3):
        sw.cmd(
            'ovs-vsctl set Bridge {} stp_enable=false'.format(sw.name)
        )
        sw.cmd(
            'ovs-vsctl set Bridge {} rstp_enable=true'.format(sw.name)
        )

    print("\n=== Convencional - 3 switches em anel / RSTP ATIVO ===")
    print("s1: h1 h2")
    print("s2: h3 h4")
    print("s3: h5 h6")
    print("Anel: s1 <-> s2 <-> s3 <-> s1")
    print("")
    print("RSTP habilitado nos tres switches.")
    print("Aguarde alguns segundos para convergencia antes dos testes.")
    print("")
    print("Verificar RSTP:")
    print("  sh ovs-appctl rstp/show s1")
    print("  sh ovs-appctl rstp/show s2")
    print("  sh ovs-appctl rstp/show s3")
    print("")
    print("Confirmar configuracao:")
    print("  sh ovs-vsctl get Bridge s1 rstp_enable")
    print("  sh ovs-vsctl get Bridge s2 rstp_enable")
    print("  sh ovs-vsctl get Bridge s3 rstp_enable")
    print("===========================================================\n")

    CLI(net)

    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
