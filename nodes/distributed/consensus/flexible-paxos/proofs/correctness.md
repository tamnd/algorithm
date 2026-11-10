---
title: Flexible Paxos is safe when phase 1 and phase 2 quorums intersect
proves: [correctness]
status: full
---

The model is asynchronous, with crash failures, stable storage at acceptors, and messages that can be lost, duplicated and reordered. We assume that each phase 1 quorum meets each phase 2 quorum. A value $v$ is *chosen in ballot* $b$ when every acceptor of some phase 2 quorum has run line L7 with ballot $b$ and value $v$.

**Lemma 0 (counting quorums).** Let phase 1 quorums be the sets of at least $q_1$ of $n$ acceptors and phase 2 quorums the sets of at least $q_2$. Every phase 1 quorum meets every phase 2 quorum if and only if $q_1 + q_2 > n$.

*Proof.* If $q_1 + q_2 > n$, two sets of these sizes cannot be disjoint, because their union would have more than $n$ elements. If $q_1 + q_2 \le n$, the first $q_1$ acceptors and the last $q_2$ acceptors are disjoint quorums. $\square$

**Lemma 1 (one value per ballot).** For each ballot $b$, at most one value appears in a message ACCEPT($b$, $v$).

*Proof.* Only the proposer named in $b$ uses $b$, line L1 gives it a fresh round each time, and line L5 runs once per attempt because the proposer leaves phase 1. $\square$

**Lemma 2 (promises).** After acceptor $a$ sends PROMISE($b$, $vb$, $vv$), it never accepts a ballot below $b$, and $(vb, vv)$ is its accepted pair with the largest ballot so far, with $vb < b$.

*Proof.* promised never decreases (lines L6 and L7 only raise it) and is on stable storage. Line L7 accepts only $b' \ge$ promised. The ballots of the accepted pairs never decrease for the same reason, so the last pair is the largest, and line L6 sends a promise only when $b >$ promised $\ge vb$. $\square$

**Invariant P2c.** If ACCEPT($b$, $v$) is sent, there is a phase 1 quorum $S$ such that either (a) no acceptor of $S$ ever accepts a ballot below $b$, or (b) $v$ is the value of the largest ballot below $b$ that any acceptor of $S$ ever accepts.

*Proof.* Let $S$ be the phase 1 quorum of line L3. By Lemma 2, the acceptances of each $a \in S$ in ballots below $b$ all happen before its promise, and the promise reports the largest one. Line L4 takes the value with the largest reported ballot, which by Lemma 1 is the value of every acceptance in that ballot (case (b)), or any value if none is reported (case (a)). $\square$

**Theorem (agreement).** If $v$ is chosen in ballot $b_0$, every ACCEPT($b$, $w$) with $b > b_0$ has $w = v$. So at most one value is chosen.

*Proof.* Strong induction on $b$ over the finitely many ballots between $b_0$ and $b$. Let $C$ be the phase 2 quorum that chose $v$ in $b_0$, and let $S$ be the phase 1 quorum of P2c for ACCEPT($b$, $w$). By the assumption on quorums, some acceptor $a$ is in $S \cap C$. It accepts $b_0 < b$, so case (a) fails and case (b) holds: $w$ is the value of the largest ballot $c < b$ accepted in $S$, and $c \ge b_0$. If $c = b_0$, Lemma 1 gives $w = v$. If $b_0 < c < b$, the acceptance in $c$ follows an ACCEPT($c$, $w$), and the induction hypothesis gives $w = v$.

If $v$ is chosen in $b_0$ and $w$ in $b_1 \ge b_0$, then either $b_1 = b_0$ and Lemma 1 gives $v = w$, or the acceptances in $b_1$ follow ACCEPT($b_1$, $w$) and the first part gives $w = v$. $\square$

**Theorem (validity and learners).** Each chosen value is an input, and a learner learns only a chosen value.

*Proof.* Line L4 sends an input or a reported value, which by Lemma 2 was accepted in an earlier ballot, and induction on the ballot gives the first claim. Line L8 learns $v$ only when a phase 2 quorum has sent ACCEPTED($b$, $v$), which each acceptor sends only when it accepts $(b, v)$, so $v$ is chosen in $b$. $\blacksquare$

The assumption is used once, to find $a \in S \cap C$. Two phase 1 quorums, or two phase 2 quorums, are never compared, which is why they need not meet.
