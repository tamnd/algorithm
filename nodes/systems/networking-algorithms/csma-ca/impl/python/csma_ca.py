# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/csma-ca/. The authors are listed in prov/HMFCEA.jsonl.
"""CSMA/CA as in the IEEE 802.11 distributed coordination function (DCF).

Three parts:
- bianchi_fixed_point and bianchi_throughput: the saturation model of Bianchi (2000);
- saturated_dcf: a seeded slot-level simulation of the binary exponential backoff
  of n saturated stations that all hear each other, the setting of that model;
- dcf_network: a seeded slot-by-slot simulation of DCF on a graph of who hears whom,
  with or without RTS/CTS and the NAV, for the hidden and exposed terminal cases.
"""

# Bianchi's basic access example (1 Mb/s): slot 50 us, payload 8184 bits, and
# Ts = H + P + SIFS + d + ACK + DIFS + d, Tc = H + P + DIFS + d, in microseconds.
BIANCHI_SLOT = 50
BIANCHI_PAYLOAD = 8184
BIANCHI_TS = 400 + 8184 + 28 + 1 + 240 + 128 + 1
BIANCHI_TC = 400 + 8184 + 128 + 1


def bianchi_tau(p, w, m):
    """Send probability per slot of one station given the collision probability p.

    w is the smallest window CWmin + 1 and m the number of doublings, so the
    window of stage i is 2^i w for i <= m. The form avoids 0/0 at p = 1/2.
    """
    geometric = sum((2 * p) ** k for k in range(m))
    return 2 / (1 + w + p * w * geometric)


def bianchi_fixed_point(n, w=32, m=5, iterations=200):
    """Solve tau = bianchi_tau(p), p = 1 - (1 - tau)^(n - 1) by bisection on p."""
    if n == 1:
        return bianchi_tau(0, w, m), 0.0
    lo, hi = 0.0, 1.0
    for _ in range(iterations):
        mid = (lo + hi) / 2
        tau = bianchi_tau(mid, w, m)
        if 1 - (1 - tau) ** (n - 1) > mid:
            lo = mid
        else:
            hi = mid
    p = (lo + hi) / 2
    return bianchi_tau(p, w, m), p


def bianchi_throughput(n, w=32, m=5, slot=BIANCHI_SLOT, ts=BIANCHI_TS, tc=BIANCHI_TC, payload=BIANCHI_PAYLOAD):
    """Saturation throughput S, the fraction of time spent on payload bits."""
    tau, _ = bianchi_fixed_point(n, w, m)
    p_tr = 1 - (1 - tau) ** n
    p_s = n * tau * (1 - tau) ** (n - 1) / p_tr
    busy = (1 - p_tr) * slot + p_tr * p_s * ts + p_tr * (1 - p_s) * tc
    return p_s * p_tr * payload / busy


def saturated_dcf(n, slots, rng, w=32, m=5):
    """Slot-level DCF of n saturated stations that all hear each other.

    One step is one backoff slot: an idle slot, a success or a collision. A station
    whose counter is 0 sends; the others count down by one (their counters are frozen
    during the busy period itself, which counts as one step, as in Bianchi's model).
    Returns (idle, successes, collisions, sends, collided_sends, per-station successes).
    """
    stage = [0] * n
    counter = [rng.randrange(w) for _ in range(n)]
    idle = succ = coll = sends = collided = 0
    wins = [0] * n
    for _ in range(slots):
        senders = [i for i in range(n) if counter[i] == 0]
        for i in range(n):
            if counter[i] > 0:
                counter[i] -= 1
        sends += len(senders)
        if not senders:
            idle += 1
            continue
        if len(senders) == 1:
            succ += 1
            i = senders[0]
            wins[i] += 1
            stage[i] = 0
            counter[i] = rng.randrange(w)
            continue
        coll += 1
        collided += len(senders)
        for i in senders:
            stage[i] = min(stage[i] + 1, m)
            counter[i] = rng.randrange(w << stage[i])
    return idle, succ, coll, sends, collided, wins


def sim_throughput(idle, succ, coll, slot=BIANCHI_SLOT, ts=BIANCHI_TS, tc=BIANCHI_TC, payload=BIANCHI_PAYLOAD):
    return succ * payload / (idle * slot + succ * ts + coll * tc)


# Durations for dcf_network, in slots.
DATA, RTS, CTS, ACK = 20, 2, 2, 2
SIFS, DIFS = 1, 3


class Tx:
    def __init__(self, kind, src, dst, start, dur, nav_end):
        self.kind, self.src, self.dst = kind, src, dst
        self.start, self.end, self.nav_end = start, start + dur, nav_end


def dcf_network(neighbors, flows, slots, rng, rts=False, cw_min=15, cw_max=1023, retry_limit=7):
    """Slot-by-slot DCF on a graph.

    neighbors[i] is the set of nodes that hear node i (symmetric). flows maps a
    saturated sender to its receiver. A frame is received by r when r is a neighbor
    of the sender, r does not send meanwhile, and no other neighbor of r sends
    during the frame. Returns a dict of counters per sender: delivered (data received),
    lost (data sent but garbled at the receiver), acked, dropped, data_slots.
    """
    n = len(neighbors)
    nav = [0] * n
    mode = ["idle"] * n
    for s in flows:
        mode[s] = "contend"
    stage = [0] * n
    counter = [rng.randrange(cw_min + 1) for _ in range(n)]
    idle_run = [0] * n
    deadline = [0] * n
    scheduled = {}  # time -> list of Tx to start without carrier sense (SIFS responses)
    txs = []
    stats = {s: {"delivered": 0, "lost": 0, "acked": 0, "dropped": 0, "data_slots": 0} for s in flows}

    def cw(i):
        return min((cw_min + 1) << stage[i], cw_max + 1) - 1

    def heard(tx, r):
        if tx.src not in neighbors[r]:
            return False
        for o in txs:
            if o is tx or o.start >= tx.end or o.end <= tx.start:
                continue
            if o.src == r or o.src in neighbors[r]:
                return False
        return True

    def fail(i, t):
        stage[i] += 1
        if stage[i] > retry_limit:  # @line L9 give up after the retry limit
            stats[i]["dropped"] += 1
            stage[i] = 0
        counter[i] = rng.randrange(cw(i) + 1)  # @line L3 a new backoff over the doubled window
        idle_run[i] = 0
        mode[i] = "contend"

    for t in range(slots):
        txs = [o for o in txs if o.end + DATA + RTS + CTS > t]
        for tx in [o for o in txs if o.end == t]:
            if tx.kind == "DATA" and tx.src in stats:
                stats[tx.src]["data_slots"] += DATA
                if not heard(tx, tx.dst):
                    stats[tx.src]["lost"] += 1
            for r in neighbors[tx.src]:
                if not heard(tx, r):
                    continue
                if tx.dst != r:
                    nav[r] = max(nav[r], tx.nav_end)  # virtual carrier sense
                    continue
                if tx.kind == "RTS" and nav[r] <= t and mode[r] in ("idle", "contend"):
                    scheduled.setdefault(t + SIFS, []).append(Tx("CTS", r, tx.src, t + SIFS, CTS, tx.nav_end))
                elif tx.kind == "CTS" and mode[r] == "wait_cts" and t <= deadline[r]:
                    end = t + SIFS + DATA
                    scheduled.setdefault(t + SIFS, []).append(Tx("DATA", r, tx.src, t + SIFS, DATA, end + SIFS + ACK))
                    mode[r] = "wait_data_end"
                elif tx.kind == "DATA":
                    stats[tx.src]["delivered"] += 1
                    scheduled.setdefault(t + SIFS, []).append(Tx("ACK", r, tx.src, t + SIFS, ACK, t + SIFS + ACK))
                elif tx.kind == "ACK" and mode[r] == "wait_ack" and t <= deadline[r]:
                    stats[r]["acked"] += 1  # @line L7 the ACK came: the frame is sent
                    stage[r] = 0
                    counter[r] = rng.randrange(cw(r) + 1)  # @line L1 next frame, stage 0
                    idle_run[r] = 0
                    mode[r] = "contend"
            if tx.kind == "DATA" and mode[tx.src] == "wait_data_end":
                mode[tx.src] = "wait_ack"  # @line L6 wait SIFS + ACK for the ACK
                deadline[tx.src] = t + SIFS + ACK
        for i in flows:
            if mode[i] in ("wait_cts", "wait_ack") and t > deadline[i]:
                fail(i, t)  # @line L8 no CTS or no ACK: count a failure
        for tx in scheduled.pop(t, []):
            txs.append(tx)
            if tx.kind == "DATA":
                mode[tx.src] = "wait_data_end"
        busy = [any(o.start <= t < o.end and (o.src == i or o.src in neighbors[i]) for o in txs) for i in range(n)]
        for i in flows:
            if mode[i] != "contend":
                continue
            if busy[i] or nav[i] > t:  # @line L4 freeze while the medium is busy
                idle_run[i] = 0
                continue
            idle_run[i] += 1
            if idle_run[i] <= DIFS:  # @line L2 wait for DIFS of idle medium
                continue
            if counter[i] > 0:
                counter[i] -= 1  # @line L4 count down one idle slot
                continue
            dst = flows[i]
            if rts:
                exchange = t + RTS + SIFS + CTS + SIFS + DATA + SIFS + ACK
                txs.append(Tx("RTS", i, dst, t, RTS, exchange))  # @line L5 send (RTS first)
                mode[i] = "wait_cts"
                deadline[i] = t + RTS + SIFS + CTS
            else:
                txs.append(Tx("DATA", i, dst, t, DATA, t + DATA + SIFS + ACK))  # @line L5 send the frame
                mode[i] = "wait_data_end"
    return stats
