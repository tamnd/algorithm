---
title: The multi-writer quorum register with write back is linearizable and wait-free
proves: [correctness]
status: full
---

**Statement.** Consider the algorithm of lines L1 to L9 in the asynchronous model with reliable links between correct processes. Let $\mathcal{R}$ and $\mathcal{W}$ be the sets of read and write quorums, with $Q_r \cap Q_w \ne \emptyset$ for all $Q_r \in \mathcal{R}$ and $Q_w \in \mathcal{W}$. Assume that some read quorum and some write quorum contain no crashed server. Then (a) every operation of a correct client completes, and (b) every history is linearizable.

**Notation.** Tags are pairs (ts, id), ordered lexicographically; the initial tag is $t_0 = (0, \bot)$ with $\bot$ below every id. For an operation $o$ that reaches line L3 or line L6, let $\tau(o)$ be the tag it sends there: for a write, the tag of line L2; for a read, the tag of line L5. Write $o_1 \to o_2$ if $o_1$ returns before $o_2$ is called.

**Lemma 1 (server tags grow).** The tag at a server never decreases.

*Proof.* Only line L8 changes it, and only to a larger tag. $\square$

**Lemma 2 (each phase ends).** A phase of a correct client ends.

*Proof.* The client sends to all servers. Every server that does not crash answers (QUERY and STORE are answered at once), and links are reliable. Some quorum of the needed kind has no crashed server, so the client gets enough replies. $\square$

Part (a) follows, since an operation has at most two phases.

**Lemma 3 (what a completed operation leaves).** When an operation $o$ returns, every server in some write quorum has a tag at least $\tau(o)$, and this stays true forever.

*Proof.* Before it returns, $o$ waits at line L3 or line L6 for acks from a write quorum $Q_w$ to STORE$(\tau(o), \cdot)$. A server acks only after line L8, so it then holds a tag at least $\tau(o)$. By Lemma 1 this stays true. $\square$

**Lemma 4 (real-time order).** If $o_1 \to o_2$ and $o_1$ completes, then $\tau(o_2) \ge \tau(o_1)$, with strict inequality if $o_2$ is a write.

*Proof.* The query of $o_2$ (line L1 or L4) starts after $o_1$ returned. It collects replies from a read quorum $Q_r$. By Lemma 3, a write quorum $Q_w$ holds tags at least $\tau(o_1)$ at that time, and $Q_r$ meets $Q_w$ in some server $s$. The reply of $s$ is sent after the query arrives, so its tag is at least $\tau(o_1)$. If $o_2$ is a read, line L5 takes the largest tag, so $\tau(o_2) \ge \tau(o_1)$. If $o_2$ is a write, line L2 sets the timestamp of $\tau(o_2)$ to at least $\mathrm{ts}(\tau(o_1)) + 1$, so $\tau(o_2) > \tau(o_1)$. $\square$

**Lemma 5 (unique write tags).** Two different writes $w_1 \ne w_2$ that reach line L3 have $\tau(w_1) \ne \tau(w_2)$.

*Proof.* If they come from different clients, the ids differ. If they come from the same client, that client runs them one after the other, so $w_1 \to w_2$ or $w_2 \to w_1$, and Lemma 4 gives a strict inequality. $\square$

**Lemma 6 (reads return the value of their tag).** If a read $r$ has $\tau(r) = t \ne t_0$, then some write $w$ with $\tau(w) = t$ reached line L3, and $r$ returns the value of $w$. If $t = t_0$, $r$ returns the initial value.

*Proof.* A pair (t, v) with $t \ne t_0$ exists at a server only because some STORE$(t, v)$ was sent, either by a write at line L3 or by a read at line L6. A read sends at L6 a pair it received, so by induction on the time at which pairs are first sent, every pair (t, v) in the system was first sent by a write with tag $t$ and value $v$. By Lemma 5 that write is unique, so the pair with tag $t$ always carries its value. $\square$

**Proof of (b).** Let $H$ be a history. Let $C$ be the set of completed operations, together with the pending writes $w$ for which some read in $C$ has $\tau(r) = \tau(w)$; the other pending operations are dropped, which linearizability allows. By Lemma 6 every pending write in $C$ reached line L3, so all operations in $C$ have tags.

Define a total order $<$ on $C$:

1. sort by tag;
2. among operations with the same tag, put the write first (there is at most one, by Lemma 5);
3. among reads with the same tag, sort by the time they were called.

*$<$ extends $\to$.* Let $o_1 \to o_2$. Then $o_1$ is complete, and by Lemma 4 $\tau(o_1) \le \tau(o_2)$. If the tags differ, $o_1 < o_2$ by rule 1. If they are equal, $o_2$ is not a write (Lemma 4 would give a strict inequality), so $o_2$ is a read. If $o_1$ is the write, rule 2 puts it first. If $o_1$ is a read, it was called before $o_2$ was called, so rule 3 puts it first.

*Every read returns the right value.* Let $r$ be a read with tag $t$. If $t = t_0$, no write precedes $r$ in $<$ (every write has a tag larger than $t_0$), and by Lemma 6 $r$ returns the initial value. Otherwise, by Lemma 6 a write $w$ with tag $t$ exists and $r$ returns its value. If $w$ is pending, it is in $C$ by the choice of $C$. In $<$, $w$ comes before $r$ (rule 2). Every other write in $C$ has a tag different from $t$ (Lemma 5): if it is smaller, the write comes before $w$, and if it is larger, the write comes after $r$ (rule 1). So $w$ is the last write before $r$ in $<$.

So the sequence of $C$ in the order $<$ is a legal run of a sequential register that respects $\to$, and $H$ is linearizable. $\square$

**Remark (why line L6 is needed).** Lemma 4 for a read $o_1$ uses Lemma 3, which needs the write back. Without it, a read can return a tag $t$ that only a few servers hold. A later read whose quorum misses those servers returns an older tag, and Lemma 4 fails. The new-old inversion on the page is such a run.

**Remark (Gifford's version numbers).** If the tag is only a timestamp, Lemma 5 fails: two concurrent writes can pick the same timestamp. Gifford's scheme prevents this with locks on a write quorum and the condition $2w > V$, so that two write quorums meet and two writers cannot hold their locks at the same time.
