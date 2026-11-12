# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/direct-server-return/. The authors are listed in prov/DKHAZZ.jsonl.

import random

import pytest

from direct_server_return import (
    Backend,
    DsrBalancer,
    NatBalancer,
    Packet,
    arp_answers,
    max_mss,
    run,
)

VIP = "203.0.113.10"


def pool(k: int = 3, **kw) -> list:
    return [Backend(f"10.0.0.{11 + i}", f"02:00:00:00:00:{11 + i:02x}", VIP, **kw) for i in range(k)]


def random_flows(rng: random.Random, m: int) -> list:
    return [(f"198.51.100.{rng.randrange(1, 255)}", rng.randrange(1024, 65536), rng.randrange(1, 6)) for _ in range(m)]


@pytest.mark.parametrize("mode", ["mac", "ipip", "gre"])
def test_same_backends_and_replies_as_nat(mode: str) -> None:
    rng = random.Random(5)
    for _ in range(50):
        flows = random_flows(rng, rng.randrange(1, 30))
        flows = list({(c, p): (c, p, k) for c, p, k in flows}.values())  # one entry per 5-tuple
        dsr = DsrBalancer("10.0.0.2", "02:00:00:00:00:02", VIP, pool(), mode)
        nat = NatBalancer(VIP, pool())
        r1, rep1 = run(flows, dsr, 1000)
        r2, rep2 = run(flows, nat, 1000)
        assert r1 == r2  # the same backend for every packet
        assert rep1 == rep2  # the client sees the same replies, all from the VIP
        for (client, port, count), reached, got in zip(flows, r1, rep1):
            assert len(set(reached)) == 1  # flow affinity
            assert len(got) == count
            assert all(p.src == VIP and p.sport == 80 and p.dst == client and p.dport == port for p in got)


def test_bytes_of_the_page() -> None:
    flows = [("198.51.100.7", 40000 + i, 1) for i in range(10)]
    nat = NatBalancer(VIP, pool())
    run(flows, nat, 30000, request_size=300)
    assert nat.bytes == 10 * 60600
    for mode, per_request in (("mac", 600), ("ipip", 620), ("gre", 624)):
        dsr = DsrBalancer("10.0.0.2", "02:00:00:00:00:02", VIP, pool(), mode)
        run(flows, dsr, 30000, request_size=300)
        assert dsr.bytes == 10 * per_request
    assert round(600 / 60600 * 100, 2) == 0.99


def test_mss_of_the_page() -> None:
    assert max_mss(1500, "mac") == 1460
    assert max_mss(1500, "ipip") == 1440
    assert max_mss(1500, "gre") == 1436
    # a full segment of the plain MSS does not fit after encapsulation
    assert 1460 + 40 + 20 > 1500


def test_vip_must_be_local_on_backend() -> None:
    b = pool(1, vip_on_loopback=False)
    dsr = DsrBalancer("10.0.0.2", "02:00:00:00:00:02", VIP, b, "mac")
    _, replies = run([("198.51.100.7", 40000, 3)], dsr, 1000)
    assert replies == [[]]  # every packet is dropped


def test_tunnel_to_wrong_backend_is_dropped() -> None:
    b = pool(2)
    pkt = Packet("198.51.100.7", 40000, VIP, 80, 100, outer_src="10.0.0.2", outer_dst=b[0].ip, encap="ipip")
    assert b[1].receive(pkt, 10) is None
    assert b[0].receive(pkt, 10) == Packet(VIP, 80, "198.51.100.7", 40000, 10)


def test_arp_for_the_vip() -> None:
    lb = DsrBalancer("10.0.0.2", "02:00:00:00:00:02", VIP, pool(), "mac")
    assert arp_answers(VIP, lb, pool()) == ["02:00:00:00:00:02"]
    bad = pool(arp_ignore=False)
    answers = arp_answers(VIP, lb, bad)
    assert len(answers) == 4  # the balancer and all three backends claim the VIP
    assert arp_answers("10.0.0.12", lb, bad) == ["02:00:00:00:00:0c"]


def test_table_entry_removed_on_close() -> None:
    dsr = DsrBalancer("10.0.0.2", "02:00:00:00:00:02", VIP, pool(), "mac")
    p = Packet("198.51.100.7", 40000, VIP, 80, 100)
    j1, _ = dsr.forward(p)
    dsr.forward(Packet("198.51.100.8", 40000, VIP, 80, 100))
    dsr.close(p)
    j2, _ = dsr.forward(p)
    assert (j1, j2) == (0, 2)  # a new flow with the same 5-tuple gets a new pick
    with pytest.raises(ValueError):
        dsr.forward(Packet("198.51.100.7", 40000, "10.0.0.11", 80, 100))
    with pytest.raises(ValueError):
        DsrBalancer("10.0.0.2", "m", VIP, pool(), "nat")
