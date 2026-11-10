---
title: The vector-timestamp algorithm implements causal broadcast
proves: [correctness]
status: full
---

**Model.** There are $n$ processes $p_1, \ldots, p_n$ in the asynchronous model, and processes may crash. A process is *correct* if it never crashes. The algorithm runs on a reliable broadcast layer with these properties: a message broadcast by a correct process is eventually delivered by every correct process (validity); if a correct process delivers a message, every correct process eventually delivers it (agreement); each message is delivered at most once, and only if it was broadcast (integrity). Eager reliable broadcast, where each process relays a message to all others when it first receives it, has these properties over reliable channels.

**Causal precedence.** For messages $m$ and $m'$, write $m \to m'$ if the broadcast of $m$ happened before the broadcast of $m'$: the same process broadcast $m$ first, or the sender of $m'$ delivered $m$ before it broadcast $m'$, or a chain of such steps links them.

**Notation.** The $s$-th message broadcast by $p_j$ has *sequence number* $s$. For a message $m$ from $p_j$, $VT(m)$ is its timestamp.

**Lemma 1 (what the vectors count).** At every moment, at every process $p$, and for every $k$:

1. $VC_p[k]$ is the number of messages of $p_k$ that $p$ has delivered, and these are exactly the messages of $p_k$ with sequence numbers $1, \ldots, VC_p[k]$.
2. For a message $m$ from $p_j$, $VT(m)[j]$ is the sequence number of $m$, and for $k \ne j$, $VT(m)[k]$ is the number of messages of $p_k$ that $p_j$ had delivered when it broadcast $m$.

*Proof.* By induction over the run. Part 2 follows from part 1 at the sender: line L2 copies $VC_{p_j}$, which counts the deliveries at $p_j$, and raises entry $j$ by $1$. Since $p_j$ delivers each of its own messages at once (line L4), $VC_{p_j}[j]$ is the number of its earlier broadcasts, so $VT(m)[j]$ is the sequence number. For part 1, each delivery raises exactly one entry by $1$. A sender delivers its own messages in order. A receiver delivers a message $m$ of $p_j$ only when $VT(m)[j] = VC_p[j] + 1$, so the new message is the next one in the sequence of $p_j$. $\square$

**Lemma 2 (safety).** If $m \to m'$ and a process $p$ delivers $m'$, then $p$ delivered $m$ before $m'$.

*Proof.* Since the relation is transitive, it is enough to prove the claim for one step; a chain then follows by induction on its length. If $p$ is the sender of $m'$, then $p$ broadcast or delivered $m$ before it broadcast $m'$ by the definition of $\to$. Otherwise $p$ delivered $m'$ at line L7, when the condition of line L6 held with the vector $VC_p$ from before this delivery. Let $p_j$ be the sender of $m'$.

- If $p_j$ also sent $m$, with sequence number $s < VT(m')[j]$, then $VC_p[j] = VT(m')[j] - 1 \ge s$. By Lemma 1, $p$ has delivered the first $VC_p[j]$ messages of $p_j$, which include $m$.
- If $m$ came from $p_k \ne p_j$ with sequence number $s$, and $p_j$ delivered $m$ before broadcasting $m'$, then by Lemma 1 $p_j$ had delivered the first $s$ or more messages of $p_k$, so $VT(m')[k] \ge s$. The condition gives $VC_p[k] \ge VT(m')[k] \ge s$, so $p$ has delivered $m$.

In both cases $m$ was delivered before $m'$. $\square$

**Lemma 3 (progress).** Let $p$ be a correct process, and let $m$ be a message that $p$ has received from the reliable broadcast layer. If every message $m''$ with $m'' \to m$ is eventually delivered by $p$, then $p$ eventually delivers $m$.

*Proof.* Let $p_j$ send $m$ with sequence number $s$. The messages of $p_j$ with sequence numbers below $s$ precede $m$, and so do the first $VT(m)[k]$ messages of each $p_k$, by Lemma 1. Consider the moment when $p$ has delivered all of them and has received $m$. If $p$ has not yet delivered $m$, then by Lemma 1 $VC_p[j] = s - 1 = VT(m)[j] - 1$, and $VC_p[k] \ge VT(m)[k]$ for $k \ne j$. So $m$ meets the condition of line L6. The loop of lines L6 and L7 runs until no buffered message meets the condition, and the condition of $m$ stays true until $m$ is delivered. So $p$ delivers $m$ in that loop. $\square$

**Theorem.** The algorithm satisfies the properties of causal broadcast:

1. (Validity) If a correct process broadcasts $m$, every correct process eventually delivers $m$.
2. (Agreement) If a correct process delivers $m$, every correct process eventually delivers $m$.
3. (Integrity) Each process delivers each message at most once, and only if it was broadcast.
4. (Causal order) If $m \to m'$, no process delivers $m'$ unless it has already delivered $m$.

*Proof.* Causal order is Lemma 2. For integrity, the layer below delivers each message at most once and creates no message, and the sender delivers its own message once at line L4.

For agreement, let a correct process $p$ deliver $m$. By Lemma 2, $p$ delivered every $m''$ with $m'' \to m$ before. Each of these, and $m$ itself, was either broadcast by $p$, or received by $p$ from the reliable broadcast layer. In the first case, the reliable validity property applies because $p$ is correct. In the second case, the reliable agreement property applies. So every correct process $q$ eventually receives $m$ and all its predecessors. Now order the predecessors of $m$ by the time of their broadcast; each one's own predecessors come earlier. By induction along this order and Lemma 3, $q$ delivers each predecessor and then $m$. A message that $q$ broadcast itself is delivered at line L4.

Validity follows from agreement, because a correct sender delivers its own message at once at line L4. $\blacksquare$
