---
title: Zab keeps total order and primary order under any crashes, recoveries and message losses
proves: [correctness]
status: full
---

We use lines L1 to L12 of the page. The model is asynchronous with crash and recovery: a process keeps $f.p$, $f.a$, its history $h_f$ and its delivered sequence on stable storage, and loses everything else in a crash. Channels are FIFO while a connection lasts. A lost message ends the connection for the follower, which then ignores every later message on it. Each run of leader election makes a new connection, and a process follows one connection at a time and never returns to an old one. We prove the safety properties only; liveness needs a leader that a quorum follows long enough, which the model gives as an oracle.

An epoch $e$ is *established* when its prospective leader receives ACK-E from all of its quorum $Q_e$ and fixes the initial history $I_e$ (line L4). The epoch is *synchronized* when its leader sends COMMIT-LD (line L7). A proposal of epoch $e$ is *committed* when the leader of $e$ sends COMMIT for it (line L11). Let $S_e$ be $I_e$ followed by the committed proposals of $e$, for a synchronized epoch $e$; it grows over time.

**Lemma 1 (one leader per epoch).** At most one leader establishes each epoch. So each zxid names one transaction.

*Proof.* A leader that establishes $e$ received ACK-E for $e$ from a quorum. A follower sends ACK-E for $e$ only if $e > f.p$, and then sets $f.p \leftarrow e$ on stable storage (line L3); $f.p$ never decreases. Two quorums share a follower, which would have acknowledged $e$ twice, the second time with $f.p \ge e$. Proposals of epoch $e$ come only from its leader, which numbers them $1, 2, \ldots$ (line L9). $\square$

**Lemma 2 (shape of histories).** At all times, each process $f$ with $f.a = e > 0$ has $h_f = I_e$ followed by the proposals of $e$ with counters $1, \ldots, m$ for some $m \ge 0$; a process with $f.a = 0$ has an empty history. Each $I_e$ is the history of some process with $f.a < e$. So every history is sorted by zxid, and for each epoch it holds the proposals with counters $1$ to some $m$.

*Proof.* $f.a$ changes only at line L6, where $h_f$ becomes the history in NEWLEADER, which the leader of $e$ (unique by Lemma 1) sends only after it is established. That history is $I_e$, or for a follower that joins late, $I_e$ followed by all proposals of $e$ so far. After that, $h_f$ changes only by PROPOSE on the same connection (line L10). The leader sends proposals in counter order, sends none to a follower before its NEWLEADER, and the channel is FIFO, so $f$ appends counters $m+1, m+2, \ldots$ in order. If one is lost, $f$ leaves the connection and appends nothing more until a new NEWLEADER. $I_e$ is the history of the chosen follower, whose current epoch is at most $f.p < e$ when it sends ACK-E. The last claim follows by induction on the epoch. $\square$

**Lemma 3 (committed history survives).** Let $e$ be synchronized and $e^* > e$ be established. Then (a) $S_e$, at any time, is a prefix of $I_{e^*}$, and (b) every transaction of $I_{e^*}$ whose epoch is less than $e$ is in $I_e$.

*Proof.* By induction on $e^*$. Fix a time and let $t$ be the last element of $S_e$ that is a proposal of $e$, if there is one. Let $C$ be a quorum that shows the commit: the followers that acknowledged $t$ (line L11), or, if no proposal of $e$ is committed, those that sent ACK-LD (line L7). Each member of $C$ had $f.a = e$ and held $I_e$, and $t$ if it exists. $C$ and $Q_{e^*}$ share a follower $f$.

First, $f$ did this before it sent ACK-E for $e^*$: after that ACK-E, $f.p \ge e^* > e$, so $f$ cannot accept NEWLEADER($e$); and it acted for $e$ on an old connection, to which it never returns. At its ACK-E for $e^*$, $f.a \ge e$ because $f.a$ never decreases. If $f.a = e$, then by Lemma 2, $h_f$ is $I_e$ followed by proposals of $e$, and it still holds $t$, since a history with the same current epoch only grows. If $f.a = e_1 > e$, then $e_1 < e^*$, because $f$ accepted NEWLEADER($e_1$) with $f.p = e_1$ before it acknowledged $e^* > f.p$. So by induction $S_e$ is a prefix of $I_{e_1}$, which is a prefix of $h_f$.

Now let $g$ be the follower chosen at line L4, with the largest $(g.a, \text{last zxid})$. Then $g.a \ge f.a \ge e$.

- If $g.a = e$, then $f.a = e$ too, and $h_g$ is $I_e$ followed by proposals of $e$ with counters $1$ to some $m$. The last zxid of $h_g$ is at least that of $h_f$, which is at least the zxid of $t$. So $h_g$ contains $t$ and all proposals of $e$ before it, and $S_e$ is a prefix of $I_{e^*} = h_g$. Every element of $h_g$ with epoch less than $e$ is in $I_e$.
- If $g.a = e_1 > e$, then $e_1 < e^*$ and $e_1$ is established, and $h_g$ is $I_{e_1}$ followed by proposals of $e_1$. By induction, $S_e$ is a prefix of $I_{e_1}$, so of $I_{e^*}$, and every element of $I_{e_1}$ with epoch less than $e$ is in $I_e$. The proposals of $e_1$ have epoch $e_1 > e$. $\square$

**Lemma 4 (what a process delivers).** At all times, the delivered sequence of a process is a prefix of $S_e$ for some synchronized epoch $e$.

*Proof.* A process delivers only at line L8 and line L12, for the leader of its current epoch $e$, which is synchronized because it has sent COMMIT-LD. At line L8 it delivers a prefix of $h_f$ of the length that NEWLEADER gave: all of $I_e$, or for a late follower, $I_e$ and the proposals committed so far. At line L12 it delivers $h_f$ up to a committed zxid $z$; by Lemma 2 and the commit order of line L11, that is $I_e$ followed by committed proposals. In both cases the new sequence is a prefix of $S_e$, provided that what was delivered before is a prefix of $h_f$. That holds: what was delivered before is a prefix of $S_{e'}$ for some synchronized $e' \le e$, and if $e' < e$, Lemma 3 (a) makes it a prefix of $I_e$, the start of $h_f$. $\square$

**Theorem.** Zab gives integrity, total order, agreement, local primary order, global primary order and primary integrity.

*Proof.* By Lemma 3 (a), $S_e$ is a prefix of $I_{e'}$, so of $S_{e'}$, for synchronized epochs $e < e'$. So the sequences $S_e$ form one chain, ordered by prefix, and by Lemma 4 every delivered sequence is a prefix of one sequence $S$. This gives total order and agreement in the form of [total-order broadcast](/total-order-broadcast/): two processes deliver the same transactions in the same order, up to the shorter of the two. By Lemma 2, $S$ is sorted by zxid with no repeats, and only broadcast transactions enter histories, which gives integrity. Sorted by zxid means sorted by epoch, which is global primary order. Within each epoch, a prefix of $S$ holds the proposals with counters $1$ to some $m$, so a process that delivers a proposal has delivered every earlier proposal of the same primary before it, which is local primary order.

For primary integrity, let the primary of $e$ broadcast $b$, so $e$ is synchronized, and let some process deliver $a$ of epoch $e' < e$. By Lemma 4, $a$ is in some $S_{e''}$. If $e'' < e$, Lemma 3 (a) puts $S_{e''}$ inside $I_e$. If $e'' = e$, then $a \in I_e$, since the proposals of $e$ have epoch $e$. If $e'' > e$, then $a \in I_{e''}$ and Lemma 3 (b) gives $a \in I_e$. So $a$ is in the initial history that the primary of $e$ installed on a quorum and committed before its first proposal. In the protocol of Junqueira, Reed and Serafini the leader is in its own quorum, so it delivers $I_e$ at COMMIT-LD, before it broadcasts $b$. $\square$

**What the tests check.** The simulator records $I_e$, the established leaders and the proposals of every epoch, and checks the theorem's properties after each seeded run with crashes, recoveries, lost messages and competing leaders. A broken version that picks a random history at line L4 instead of the largest $(f.a, \text{zxid})$ fails the checks in most runs; it breaks the case analysis on $g$ in Lemma 3.
