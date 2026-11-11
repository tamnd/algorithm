# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zyzzyva/. The authors are listed in prov/8FSV21.jsonl.

"""Zyzzyva (Kotla, Alvisi, Dahlin, Clement and Wong, SOSP 2007 and TOCS 2009)
and the safety violation of its view change found by Abraham, Gueta, Malkhi,
Alvisi, Kotla and Martin (arXiv 1712.01367).

Replicas execute requests speculatively in the order of the primary and reply
to the client with their whole history. The client completes a request with
3f + 1 matching replies (fast path), or with 2f + 1 matching replies, a commit
certificate and 2f + 1 LOCAL-COMMIT messages (two-phase path).

The adversary is the scheduler: the functions below take explicit lists of
receivers, so a test can replay any asynchronous schedule step by step.
Signatures are unforgeable tokens: a spec response is valid only if the
replica made it, and a commit certificate only if it holds 2f + 1 valid
spec responses for the same view and history.
"""


class System:
    def __init__(self, n, f, faulty=()):
        self.n, self.f, self.faulty = n, f, set(faulty)
        self.view = {i: 1 for i in range(n)}
        self.history = {i: [] for i in range(n)}
        self.cc = {i: None for i in range(n)}  # the longest commit certificate seen
        self.tokens = set()
        self.completed = []  # (view, position, request, path)
        self.messages = 0

    def primary(self, v):
        return (v - 1) % self.n

    # ---- normal case ---------------------------------------------------------
    def order(self, v, req, to, prefix=None):
        """The primary of view v orders req after its history and sends
        ORDER-REQ to the replicas in `to`, which execute it speculatively.
        A faulty primary may give another prefix to some replicas."""
        p = self.primary(v)
        hist = (tuple(self.history[p]) if prefix is None else tuple(prefix)) + (req,)
        self.messages += len([i for i in to if i != p])  # @line L1
        replies = []
        for i in to:
            if self.view[i] == v and tuple(self.history[i]) == hist[:-1]:
                self.history[i].append(req)  # @line L2
                replies.append(self.spec_response(i))
        return replies

    def spec_response(self, i, hist=None):
        tok = ("spec", i, self.view[i], tuple(self.history[i]) if hist is None else hist)
        self.tokens.add(tok)
        self.messages += 1
        return tok

    def client(self, replies, req):
        """The client groups the valid replies by (view, history). It returns
        ("fast", ...) with 3f + 1 matching, ("cert", cc) with 2f + 1, or None."""
        groups = {}
        for tok in replies:
            if tok in self.tokens:
                groups.setdefault((tok[2], tok[3]), set()).add(tok[1])
        for (v, hist), who in groups.items():
            if len(who) >= 3 * self.f + 1:
                self.completed.append((v, hist, req, "fast"))  # @line L3
                return ("fast", v, hist)
        for (v, hist), who in groups.items():
            if len(who) >= 2 * self.f + 1:
                cc = ("cc", v, hist, frozenset(sorted(who)[: 2 * self.f + 1]))  # @line L4
                self.tokens.add(cc)
                return ("cert", cc)
        return None

    def valid_cc(self, cc):
        if cc is None:
            return True
        _, v, hist, who = cc
        return len(who) >= 2 * self.f + 1 and all(("spec", i, v, hist) in self.tokens for i in who)

    def commit(self, cc, to, req):
        """The client sends COMMIT with cc to `to`; it completes the request
        if 2f + 1 replicas answer LOCAL-COMMIT."""
        acks = 0
        self.messages += len(to)
        for i in to:
            hist = cc[2]
            if self.valid_cc(cc) and tuple(self.history[i][: len(hist)]) == hist:
                if self.cc[i] is None or len(self.cc[i][2]) < len(hist):
                    self.cc[i] = cc  # @line L5
                acks += 1
                self.messages += 1
        if acks >= 2 * self.f + 1:
            self.completed.append((cc[1], cc[2], req, "two-phase"))  # @line L6
            return True
        return False

    # ---- view change ---------------------------------------------------------
    def view_change_msg(self, i, cc="own", hist=None):
        """The VIEW-CHANGE of replica i: its commit certificate and its history.
        A faulty replica may hide its certificate or claim another history."""
        if i not in self.faulty:
            cc, hist = self.cc[i], tuple(self.history[i])
        elif cc == "own":
            cc = self.cc[i]
        self.messages += self.n - 1
        return (i, cc, tuple(self.history[i]) if hist is None else tuple(hist))  # @line L7

    def new_view(self, v, vcs, to):
        """The primary of view v builds the new history from 2f + 1 VIEW-CHANGE
        messages with the rule of the paper: start from the longest commit
        certificate, then add each request that f + 1 histories hold at its
        position. The replicas in `to` adopt it and enter view v."""
        assert len({i for i, _, _ in vcs}) >= 2 * self.f + 1
        assert all(self.valid_cc(cc) for _, cc, _ in vcs)
        certs = [cc for _, cc, _ in vcs if cc is not None]
        base = list(max(certs, key=lambda c: len(c[2]))[2]) if certs else []  # @line L8
        k = len(base)
        while True:
            votes = {}
            for _, _, hist in vcs:
                if len(hist) > k:
                    votes[hist[k]] = votes.get(hist[k], 0) + 1
            best = [m for m, c in votes.items() if c >= self.f + 1]
            if not best:
                break
            base.append(best[0])
            k += 1
        self.messages += self.n - 1
        for i in to:
            self.view[i] = v
            self.history[i] = list(base)  # @line L9
            if self.cc[i] is not None and tuple(base[: len(self.cc[i][2])]) != self.cc[i][2]:
                self.cc[i] = None
        return base


def violations(completed):
    """Positions (from 1) at which two completed histories differ. A client
    that completes a request learns the whole history before it, so two
    completed histories must be prefixes of each other."""
    bad = set()
    for _, h1, _, _ in completed:
        for _, h2, _, _ in completed:
            for k in range(min(len(h1), len(h2))):
                if h1[k] != h2[k]:
                    bad.add(k + 1)
    return sorted(bad)


def random_view(seed, steps=8):
    """One view with a faulty primary (replica 0) that gives each request a
    random prefix and a random set of receivers, and that signs spec
    responses for any history. Clients complete what they can."""
    import random

    rng = random.Random(seed)
    s = System(4, 1, faulty={0})
    for k in range(steps):
        req = "r%d" % k
        prefix = list(s.history[rng.choice((1, 2, 3))])
        to = [i for i in (1, 2, 3) if rng.random() < 0.7]
        replies = s.order(1, req, to, prefix=prefix)
        if rng.random() < 0.8:
            replies.append(s.spec_response(0, hist=tuple(prefix) + (req,)))
        out = s.client(replies, req)
        if out is not None and out[0] == "cert":
            s.commit(out[1], [i for i in range(4) if rng.random() < 0.8], req)
    return s


def normal_case(n, f, silent=()):
    """One request with the replicas in `silent` not answering. Returns the
    path, the message count and the message delays from the client."""
    s = System(n, f, faulty=silent)
    to = [i for i in range(n) if i not in silent]
    s.messages = 1  # the request to the primary
    replies = s.order(1, "m", to)
    out = s.client(replies, "m")
    if out is not None and out[0] == "fast":
        return "fast", s.messages, 3
    if out is not None and s.commit(out[1], to, "m"):
        return "two-phase", s.messages, 5
    return None, s.messages, None


def scenario_1():
    """Section 2.3 of arXiv 1712.01367: n = 4, f = 1, replica 0 (i1) Byzantine."""
    s = System(4, 1, faulty={0})
    # View 1: the faulty primary i1 orders a at i1, i2, i3, and b at i4.
    r = s.order(1, "a", [0, 1, 2])
    s.history[3] = ["b"]
    r4 = s.spec_response(3)
    out = s.client(r, "a")  # c1 gets 3 = 2f + 1 matching replies: a commit certificate
    assert out[0] == "cert" and r4 not in r
    cert_a = out[1]
    s.commit(cert_a, [0], "a")  # its COMMIT reaches only i1, which keeps it
    # View 2: leader i2 hears from i2 (a), i4 (b) and the faulty i1, which hides
    # its certificate and claims b. The f + 1 rule picks b.
    vcs = [s.view_change_msg(1), s.view_change_msg(3), s.view_change_msg(0, cc=None, hist=["b"])]
    base = s.new_view(2, vcs, [0, 1, 2, 3])
    assert base == ["b"]
    replies = [s.spec_response(i) for i in range(4)]
    s.client(replies, "b")  # c2 gets 4 matching replies: b completes on the fast path
    # View 3: leader i3 hears from i1 (cert for a), i3 (b), i4 (b) and prefers the certificate.
    vcs = [s.view_change_msg(0, cc=cert_a, hist=["a"]), s.view_change_msg(2), s.view_change_msg(3)]
    base = s.new_view(3, vcs, [0, 1, 2, 3])
    replies = [s.spec_response(i) for i in range(4)]
    s.client(replies, base[0])
    return s


def scenario_2():
    """Section 2.4 of arXiv 1712.01367: the longest certificate is stale."""
    s = System(4, 1, faulty={0})
    # View 1: the faulty primary orders a1, a2 at i1, i2, i3; i4 gets nothing.
    s.order(1, "a1", [0, 1, 2])
    r = s.order(1, "a2", [0, 1, 2])
    out = s.client(r, "a2")
    cert1 = out[1]  # (a1, a2), kept by the faulty i1 only
    s.commit(cert1, [0], "a2")
    # View 2: leader i2 hears from i1 (claims nothing), i2 (a1, a2), i4 (empty).
    vcs = [s.view_change_msg(0, cc=None, hist=[]), s.view_change_msg(1), s.view_change_msg(3)]
    s.new_view(2, vcs, [0, 1, 3])  # i3 is slow and stays in view 1
    r = s.order(2, "b1", [0, 1, 3])
    out = s.client(r, "b1")  # 3 replies: certificate cert2 for (b1)
    cert2 = out[1]
    s.commit(cert2, [0, 1, 3], "b1")  # LOCAL-COMMIT from i1, i2, i4: b1 completes
    # View 3: leader i3 hears from i1 (cert1), i3 (a1, a2) and i4 (cert2).
    vcs = [s.view_change_msg(0, cc=cert1, hist=["a1", "a2"]), s.view_change_msg(2), s.view_change_msg(3)]
    base = s.new_view(3, vcs, [0, 1, 2, 3])
    replies = [s.spec_response(i) for i in range(4)]
    s.client(replies, base[-1])
    return s


if __name__ == "__main__":
    print(normal_case(4, 1), normal_case(4, 1, silent=(3,)))
    for sc in (scenario_1, scenario_2):
        s = sc()
        print(sc.__name__, s.completed, violations(s.completed))
