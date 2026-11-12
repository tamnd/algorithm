# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/direct-server-return/. The authors are listed in prov/DKHAZZ.jsonl.

"""Direct server return (DSR) on a small packet model.

A client sends packets to the virtual IP (VIP) of a service. The balancer
picks a backend once per flow (round robin on the first packet, then a
connection table keyed by the 5-tuple) and forwards the packet without
changing its IP addresses: in "mac" mode it only sets the destination MAC
address, in "ipip" and "gre" mode it wraps the packet in an outer IP header
addressed to the backend. The backend has the VIP on a device that does not
answer ARP, accepts the packet, and replies from the VIP straight to the
client, so the reply never passes the balancer.

NatBalancer is the reference: it rewrites the destination to the backend, and
the reply comes back through it to be rewritten to the VIP.
"""

from dataclasses import dataclass, replace
from typing import Dict, List, Optional, Sequence, Tuple

IP_HEADER = 20
TCP_HEADER = 20
OVERHEAD = {"mac": 0, "ipip": IP_HEADER, "gre": IP_HEADER + 4}


@dataclass(frozen=True)
class Packet:
    src: str
    sport: int
    dst: str
    dport: int
    size: int  # bytes of the IP packet, headers included
    dst_mac: str = ""
    outer_src: Optional[str] = None  # set when the packet is in a tunnel
    outer_dst: Optional[str] = None
    encap: str = "mac"  # "mac" (no outer header), "ipip" or "gre"

    def key(self) -> Tuple[str, int, str, int, str]:
        return (self.src, self.sport, self.dst, self.dport, "tcp")

    def wire_size(self) -> int:
        return self.size + OVERHEAD[self.encap]


@dataclass
class Backend:
    ip: str
    mac: str
    vip: str
    vip_on_loopback: bool = True  # the VIP is a local address of the backend
    arp_ignore: bool = True  # arp_ignore=1: do not answer ARP for the VIP on the LAN

    def receive(self, pkt: Packet, reply_size: int) -> Optional[Packet]:
        """Accept a request packet and return the reply, or None if it is dropped."""
        if pkt.outer_dst is not None:  # @line L8
            if pkt.outer_dst != self.ip:
                return None
            pkt = replace(pkt, outer_src=None, outer_dst=None, encap="mac")  # unwrap
        elif pkt.dst_mac != self.mac:
            return None
        if pkt.dst != self.vip or not self.vip_on_loopback:  # @line L9
            return None  # not a local address: the kernel drops it
        return Packet(self.vip, pkt.dport, pkt.src, pkt.sport, reply_size)  # @line L10

    def answers_arp(self, ip: str) -> bool:
        return ip == self.ip or (ip == self.vip and self.vip_on_loopback and not self.arp_ignore)


class DsrBalancer:
    def __init__(self, ip: str, mac: str, vip: str, backends: Sequence[Backend], mode: str = "mac") -> None:
        if mode not in OVERHEAD:
            raise ValueError("mode must be mac, ipip or gre")
        self.ip, self.mac, self.vip, self.mode = ip, mac, vip, mode
        self.backends = list(backends)
        self.table: Dict[Tuple[str, int, str, int, str], int] = {}
        self.next = 0
        self.bytes = 0  # bytes that pass the balancer, both directions

    def forward(self, pkt: Packet) -> Tuple[int, Packet]:
        if pkt.dst != self.vip:
            raise ValueError("not a packet for the VIP")
        self.bytes += pkt.wire_size()
        key = pkt.key()  # @line L1
        if key not in self.table:  # @line L2
            self.table[key] = self.next  # @line L3
            self.next = (self.next + 1) % len(self.backends)
        j = self.table[key]
        b = self.backends[j]
        if self.mode == "mac":  # @line L4
            out = replace(pkt, dst_mac=b.mac)  # @line L5
        else:
            out = replace(pkt, outer_src=self.ip, outer_dst=b.ip, encap=self.mode)  # @line L6
        self.bytes += out.wire_size()  # the balancer sends it out again
        return j, out  # @line L7

    def close(self, pkt: Packet) -> None:
        self.table.pop(pkt.key(), None)


class NatBalancer:
    """Reference: destination NAT, replies go back through the balancer."""

    def __init__(self, vip: str, backends: Sequence[Backend]) -> None:
        self.vip = vip
        self.backends = list(backends)
        self.table: Dict[Tuple[str, int, str, int, str], int] = {}
        self.next = 0
        self.bytes = 0

    def forward(self, pkt: Packet) -> Tuple[int, Packet]:
        self.bytes += 2 * pkt.size
        key = pkt.key()
        if key not in self.table:
            self.table[key] = self.next
            self.next = (self.next + 1) % len(self.backends)
        j = self.table[key]
        return j, replace(pkt, dst=self.backends[j].ip)

    def backend_reply(self, j: int, pkt: Packet, reply_size: int) -> Packet:
        b = self.backends[j]
        assert pkt.dst == b.ip
        reply = Packet(b.ip, pkt.dport, pkt.src, pkt.sport, reply_size)
        self.bytes += 2 * reply.size
        return replace(reply, src=self.vip)  # rewrite the source back to the VIP


def max_mss(mtu: int, mode: str) -> int:
    """Largest TCP MSS so that a full segment, after encapsulation, fits the MTU."""
    return mtu - OVERHEAD[mode] - IP_HEADER - TCP_HEADER


def arp_answers(ip: str, balancer: DsrBalancer, backends: Sequence[Backend]) -> List[str]:
    """MAC addresses that answer an ARP request for ip on the shared LAN."""
    out = [balancer.mac] if ip in (balancer.ip, balancer.vip) else []
    return out + [b.mac for b in backends if b.answers_arp(ip)]


def run(flows: Sequence[Tuple[str, int, int]], balancer, reply_size: int, request_size: int = 100):
    """Send each (client, port, packets) flow through the balancer.

    Returns, for each flow, the list of backends that its packets reached and
    the list of replies the client got.
    """
    reached, replies = [], []
    for client, port, count in flows:
        r, got = [], []
        for _ in range(count):
            pkt = Packet(client, port, balancer.vip, 80, request_size)
            j, out = balancer.forward(pkt)
            r.append(j)
            if isinstance(balancer, NatBalancer):
                got.append(balancer.backend_reply(j, out, reply_size))
            else:
                rep = balancer.backends[j].receive(out, reply_size)
                if rep is not None:
                    got.append(rep)
        reached.append(r)
        replies.append(got)
    return reached, replies
