---
title: Sequence numbers over reliable broadcast implement FIFO broadcast
proves: [correctness]
status: full
---

**Model.** There are $n$ processes in the asynchronous model, and processes may crash. A process is *correct* if it never crashes. The algorithm runs on a reliable broadcast layer with validity (a message broadcast by a correct process is eventually delivered by every correct process), agreement (if a correct process delivers a message, every correct process eventually delivers it) and integrity (each message is delivered at most once, and only if it was broadcast).

The $s$-th message broadcast by $p_j$ carries the number $s$ (lines L2 and L3).

**Lemma 1.** At every moment, at every process $p$ and for every sender $p_k$, $p$ has delivered exactly the messages of $p_k$ with numbers $1, \ldots, next_p[k] - 1$, in this order.

*Proof.* By induction over the run. At the start $next_p[k] = 1$ and nothing is delivered. A sender delivers its own messages at line L4 in the order of their numbers and raises $next$ each time. A receiver delivers a message of $p_k$ only at line L7, only if its number equals $next_p[k]$, and then raises $next_p[k]$ by $1$. $\square$

**Lemma 2 (progress).** Let $p$ be correct and let $p$ receive from the reliable broadcast layer the messages of $p_k$ with numbers $1, \ldots, s$. Then $p$ eventually delivers all of them.

*Proof.* Suppose not, and let $t \le s$ be the smallest number that $p$ never delivers. After $p$ has delivered message $t - 1$ of $p_k$ and has received message $t$, Lemma 1 gives $next_p[k] = t$, and message $t$ is in the buffer under the key $(k, t)$. Whichever of these two events came last ran the loop of lines L6 and L7 on sender $k$: either the arrival of message $t$ (line L5 adds it, and the loop then sees it), or the delivery of message $t - 1$ inside the loop, which raises $next_p[k]$ to $t$ and tests again. So message $t$ is delivered, a contradiction. $\square$

**Theorem.** The algorithm satisfies the properties of FIFO broadcast:

1. (Validity) If a correct process broadcasts $m$, every correct process eventually delivers $m$.
2. (Agreement) If a correct process delivers $m$, every correct process eventually delivers $m$.
3. (Integrity) Each process delivers each message at most once, and only if it was broadcast.
4. (FIFO order) If a process broadcasts $m$ before $m'$, no process delivers $m'$ unless it has already delivered $m$.

*Proof.* FIFO order and integrity follow from Lemma 1: the delivered messages of each sender are exactly a prefix of its numbered sequence, delivered in order, and so each one appears once.

For agreement, let a correct process $p$ deliver $m$, the $s$-th message of $p_k$. By Lemma 1, $p$ has delivered messages $1, \ldots, s$ of $p_k$. If $p = p_k$, these messages were broadcast by a correct process. Otherwise $p$ received each of them from the reliable broadcast layer. By reliable validity or agreement, every correct process $q$ eventually receives all of them, or broadcast them itself if $q = p_k$. By Lemma 2, $q$ delivers all of them, including $m$.

Validity follows from agreement, because a correct sender delivers its own message at once at line L4. $\blacksquare$

**Remark (FIFO order is not causal order).** Let $p_1$ broadcast $m_1$, and let $p_2$ deliver $m_1$ and then broadcast $m_2$. Then $m_1 \to m_2$. If $m_2$ reaches $p_3$ first, it is the first message of $p_2$, so line L6 lets $p_3$ deliver it at once, before $m_1$. All four properties hold, but causal order does not.
