---
title: Vertical Paxos I and II choose at most one value
proves: [correctness]
status: full
---

The model is asynchronous, with crash failures, stable storage at acceptors, and a reliable master. For each ballot $b$ the master fixes config($b$) once, with read and write b-quorums such that every write b-quorum meets every read b-quorum and every write b-quorum. We follow Section 4 of Lamport, Malkhi and Zhou.

**Ballots.** In VP I the ballots are all numbers that the master has started. In VP II the ballots are $0$ and the numbers that the master has activated (line L3), and we write $Prev(b)$ for the next lower ballot. Votes in a number that is not a ballot have no effect: they never make a value chosen (line L13).

**Definitions.** A value $v$ is *chosen in* ballot $b$ when every acceptor of a write b-quorum has voted $v$ in $b$. It is *choosable in* $b$ when it is chosen in $b$ or can still become chosen in $b$, by votes of acceptors with $maxBallot \le b$. A value is *safe at* $b$ when no other value is choosable in a ballot below $b$. All values are safe at $0$. A ballot $d$ is *complete* when a value is chosen in $d$ or all values are safe at $d$. Ballot $0$ is complete in VP II, since nothing votes in it, and in VP I its leader finds AllSafe at once.

**Lemma 1 (one value per ballot).** All votes in a ballot $b$ are for the same value.

*Proof.* Only the leader of $b$ sends 2a($b$, ·) (lines L8 and L10), and it runs at most one of the two lines, once. Line L12 votes only for the value of a 2a message. $\square$

**Lemma 2 (an empty read quorum).** Suppose a read c-quorum $Q$ has sent 1b($b$, $c$, None) with $b > c$. Then no value is choosable in $c$.

*Proof.* Each $a \in Q$ set $maxBallot \ge b > c$ before it replied (line L11), and $maxBallot$ never decreases, so by line L12 it never votes in $c$ afterwards. It had no vote in $c$ when it replied. So no acceptor of $Q$ ever votes in $c$. Every write c-quorum contains an acceptor of $Q$, so none can ever be all voting in $c$. $\square$

**Lemma 3 (complete ballots).** Let $d < b$ be ballots. If $d$ is complete and no value is choosable in any ballot $c$ with $d \le c < b$, then all values are safe at $b$.

*Proof.* No value is chosen in $d$, so by completeness all values are safe at $d$: nothing is choosable below $d$. By the assumption nothing is choosable from $d$ up to $b$. So nothing is choosable below $b$. $\square$

**Invariant (safe votes).** In both variants, every vote in a ballot $b$ is for a value safe at $b$.

*Proof for VP I.* Consider the leader of $b$ and the ballots $c$ it reads, from $b - 1$ down. Each ballot it passes (line L7) has an empty read c-quorum, so by Lemma 2 nothing is choosable in it.

- If it stops at line L6 with a vote $v$ in ballot $c$, then $v$ was safe at $c$ by induction on the ballot (votes in $c$ precede, in time, the 1b that reports them, and $c < b$). By Lemma 1, $v$ is the only value that can be choosable in $c$. Nothing is choosable between $c$ and $b$. So no value other than $v$ is choosable below $b$: $v$ is safe at $b$.
- If it passes every ballot down to $completeBal = d$, then nothing is choosable in $d$ or above it below $b$, and $d$ is complete because its leader sent complete($d$) only after a write quorum voted (a chosen value) or after AllSafe (line L9). By Lemma 3, all values are safe at $b$, and line L10 may send a client value.

*Proof for VP II.* Let $b$ be activated, and let $p$ be the prevBal of its newBallot message. The master activated $b$ only when $curBal = p$ (line L3). Activations happen in increasing order, because $p = curBal$ at the start of $b$ and the master sets $curBal \leftarrow b > p$. So no ballot is activated between $p$ and $b$, and $p = Prev(b)$. Also $p$ is complete: $p = 0$, or its leader sent complete($p$, ·) after a chosen value or after AllSafe.

- If the leader finds a vote $v$ in $p$ (line L6), $v$ is safe at $p$ by induction, it is the only value that can be choosable in $p$ by Lemma 1, and no ballot lies between $p$ and $b$. So $v$ is safe at $b$.
- If it finds an empty read p-quorum (line L7), nothing is choosable in $p$ by Lemma 2, and by Lemma 3 all values are safe at $b$. The leader sends a client value only after activated($b$) (lines L9 and L10).

Votes of the leader of $b$ sent before activation are for the value found in $p$, which is safe at $b$ once $b$ is activated. Votes in a number that is never activated do not matter. $\square$

**Theorem (agreement).** At most one value is chosen.

*Proof.* Let $v$ be chosen in ballot $b_0$ and $w$ in $b_1$, with $b_0 \le b_1$. If $b_0 = b_1$, Lemma 1 gives $v = w$. If $b_0 < b_1$, the votes for $w$ in $b_1$ are for a value safe at $b_1$ by the invariant, so no value other than $w$ is choosable in $b_0 < b_1$. But $v$ is chosen, so choosable, in $b_0$. So $v = w$. $\square$

**Theorem (validity).** A chosen value was proposed by a client.

*Proof.* Line L10 sends a client value, and line L8 sends a value found in an earlier vote. By induction on the ballot, every vote is for a client value. $\blacksquare$

The rule that read and write quorums of one ballot meet is used only in Lemma 2. Configurations of different ballots are never compared, which is why the master may pick a completely new set of acceptors for each ballot.
