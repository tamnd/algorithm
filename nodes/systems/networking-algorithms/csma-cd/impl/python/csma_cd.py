# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/csma-cd/. The authors are listed in prov/296FV6.jsonl.
"""1-persistent CSMA/CD on a bus, as a discrete-event model in integer bit times.

A station at position x (in bit times of propagation from one end of the bus) that
sends during [a, b) puts its signal at position y during [a + |x - y|, b + |x - y|).
A station senses the channel busy when the signal of another station is present at
its own position. The constants are the 10 Mb/s Ethernet values of IEEE 802.3.
"""

SLOT_TIME = 512  # bit times; also the minimum frame length in bits (64 bytes)
JAM_SIZE = 32  # bit times
INTERFRAME_GAP = 96  # bit times
ATTEMPT_LIMIT = 16
BACKOFF_LIMIT = 10


class Signal:
    """One burst on the bus: a frame (perhaps cut short) or a jam."""

    def __init__(self, src, pos, start, end, frame):
        self.src, self.pos, self.start, self.end, self.frame = src, pos, start, end, frame

    def present(self, y, t):
        d = abs(self.pos - y)
        return self.start + d <= t < self.end + d


def overlap_at(a, b, y):
    """True when signals a and b are both present at position y at some time."""
    da, db = abs(a.pos - y), abs(b.pos - y)
    return max(a.start + da, b.start + db) < min(a.end + da, b.end + db)


def backoff_slots(collisions, rng):
    """Truncated binary exponential backoff: a uniform integer in [0, 2^min(c, 10) - 1]."""
    return rng.randrange(1 << min(collisions, BACKOFF_LIMIT))


def csma_cd(positions, frames, rng, horizon=10 ** 6, ifg=INTERFRAME_GAP, jam=JAM_SIZE, slot=SLOT_TIME):
    """Run CSMA/CD.

    positions[i] is the position of station i. frames is a list of
    (station, ready time, length in bits, destination station); each station sends
    its frames in the order given. Returns (outcome, signals): outcome[f] is
    (end time, attempts) for frame f when its sender finished it with no collision
    seen, or (time, 'dropped'); signals is every burst that was put on the bus.
    """
    n = len(positions)
    queue = [[f for f, fr in enumerate(frames) if fr[0] == i] for i in range(n)]
    state = ["idle"] * n  # idle, wait, tx, jam
    wake = [0] * n  # earliest time to sense again (ready time or end of backoff)
    idle_since = [0] * n  # the channel at the station has been idle since this time
    attempts = [0] * n
    current = [None] * n  # the Signal being sent
    outcome = {}
    signals = []
    live = []
    span = max(positions) - min(positions) + 1
    t = 0
    while t < horizon and (any(queue) or any(s in ("tx", "jam") for s in state)):
        live = [s for s in live if s.end + span > t]
        busy = [any(s.src != i and s.present(positions[i], t) for s in live) for i in range(n)]
        for i in range(n):
            if busy[i]:
                idle_since[i] = t + 1
        for i in range(n):
            sig = current[i]
            if state[i] == "tx":
                if busy[i]:  # @line L6 a collision is detected while sending
                    sig.end = t
                    current[i] = Signal(i, positions[i], t, t + jam, None)  # @line L7 jam
                    signals.append(current[i])
                    live.append(current[i])
                    state[i] = "jam"
                    attempts[i] += 1
                elif t == sig.end:  # @line L8 the whole frame went out with no collision
                    f = queue[i].pop(0)
                    outcome[f] = (t, attempts[i] + 1)
                    attempts[i] = 0
                    state[i] = "idle"
                    current[i] = None
                    idle_since[i] = max(idle_since[i], t)  # the gap counts from the end of the own frame
            elif state[i] == "jam" and t == sig.end:
                current[i] = None
                idle_since[i] = max(idle_since[i], t)
                if attempts[i] >= ATTEMPT_LIMIT:  # @line L9 give up after 16 attempts
                    outcome[queue[i].pop(0)] = (t, "dropped")
                    attempts[i] = 0
                    state[i] = "idle"
                else:
                    wake[i] = t + slot * backoff_slots(attempts[i], rng)  # @line L10 back off
                    state[i] = "wait"
            if state[i] == "idle" and queue[i]:  # @line L1 a frame is ready
                state[i] = "wait"
                wake[i] = max(t, frames[queue[i][0]][1])
            if state[i] == "wait" and t >= wake[i]:
                # @line L2 L3 sense: wait until the channel has been idle for the gap
                if not busy[i] and t - idle_since[i] >= ifg:
                    length = frames[queue[i][0]][2]
                    current[i] = Signal(i, positions[i], t, t + length, queue[i][0])  # @line L4 L5 send and listen
                    signals.append(current[i])
                    live.append(current[i])
                    state[i] = "tx"
        t += 1
    return outcome, signals


def intact_at(signal, signals, y):
    """True when no other burst overlaps this frame at position y."""
    return not any(o is not signal and overlap_at(signal, o, y) for o in signals)


def delivered_frames(frames, positions, outcome, signals):
    """For each frame its sender reports as sent, whether the last burst of it is intact at its destination."""
    last = {}
    for s in signals:
        if s.frame is not None:
            last[s.frame] = s
    res = {}
    for f, (_, att) in outcome.items():
        if att != "dropped":
            res[f] = intact_at(last[f], signals, positions[frames[f][3]])
    return res


def efficiency_approx(t_prop, t_trans):
    """The approximation 1 / (1 + 5a), a = t_prop / t_trans, of Kurose and Ross."""
    return 1 / (1 + 5 * t_prop / t_trans)
