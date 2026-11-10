---
title: Paxos chooses at most one value, and only a proposed value
proves: [correctness]
status: full
---

The model is the one of the page: asynchronous messages that can be lost, duplicated and reordered, and processes that crash. Acceptors keep promised, vb and vv on stable storage. We prove safety. No step uses time, so the proof holds in every run. A *majority* is a set of at least $\lfloor n/2 \rfloor + 1$ acceptors. A value $v$ is *chosen in ballot* $b$ when a majority of acceptors have each run line L14 with ballot $b$ and value $v$.

**Lemma 1 (one value per ballot).** For each ballot $b$, at most one value $v$ appears in a message ACCEPT($b$, $v$).

*Proof.* The ballot $b = (r, p)$ names its proposer $p$, so only $p$ sends ACCEPT messages with ballot $b$. Line L2 makes a new ballot at each start, and the round only grows, so $p$ uses $b$ in one attempt only. In that attempt, line L9 runs at most once, because it sets the phase to 2 and line L4 then ignores all later promises. A duplicate of the message carries the same value. $\square$

**Lemma 2 (promises are kept).** If acceptor $a$ sends PROMISE($b$, ...) at time $t$, then after $t$ the acceptor never runs line L14 with a ballot smaller than $b$.

*Proof.* At time $t$ line L11 sets promised to $b$. Lines L11 and L14 only change promised to a ballot that is at least the old value, so promised stays at least $b$, also across a restart, because it is on stable storage. Line L13 runs line L14 only for a ballot at least promised, so never for a ballot smaller than $b$. $\square$

**Lemma 3 (the report is the last vote).** When acceptor $a$ sends PROMISE($b$, $vb$, $vv$), the pair $(vb, vv)$ is the vote with the largest ballot that $a$ has cast so far, or $\bot$ if it has cast none. Also $vb < b$.

*Proof.* Line L14 is the only line that changes vb and vv, and it sets them to the ballot and value of the vote it casts. A vote with ballot $c$ needs $c \ge$ promised at that time, and then sets promised to $c$, so the ballots of the votes of $a$ never decrease. So $(vb, vv)$ is the last vote and also the vote with the largest ballot. Line L10 sends the promise only when $b >$ promised, and promised $\ge vb$, so $vb < b$. $\square$

**Invariant P2c.** If a message ACCEPT($b$, $v$) is sent, then there is a majority $S$ such that either (a) no acceptor in $S$ ever votes in a ballot smaller than $b$, or (b) $v$ is the value of the vote with the largest ballot smaller than $b$ cast by any acceptor in $S$, and no acceptor in $S$ votes in a ballot $c$ with that largest ballot $< c < b$.

*Proof.* Line L9 runs when the set $P$ holds promises for $b$ from a majority $S$ (line L6). For each $a \in S$, let $t_a$ be the time when $a$ sent its promise. By Lemma 3 the promise reports the vote of $a$ with the largest ballot before $t_a$, and that ballot is below $b$. By Lemma 2, after $t_a$ the acceptor $a$ never votes in a ballot below $b$. So the votes of $a$ in ballots below $b$ are exactly its votes before $t_a$, and the report of $a$ is the largest of them.

If no promise in $P$ reports a vote, no acceptor in $S$ ever votes below $b$, which is case (a). Line L8 may then take any value. Else let $c^*$ be the largest reported ballot. Then $c^*$ is the largest ballot below $b$ in which an acceptor of $S$ ever votes. Line L7 takes the value $v^*$ reported with $c^*$, and by Lemma 1 all votes in ballot $c^*$ have the same value. So $v = v^*$, which is case (b). $\square$

**Theorem (agreement).** If $v$ is chosen in ballot $b_0$, then each message ACCEPT($b$, $w$) with $b > b_0$ has $w = v$. So if $v$ is chosen in $b_0$ and $w$ is chosen in $b_1$, then $v = w$.

*Proof.* By strong induction on $b$ over the ballots larger than $b_0$. The ballots are totally ordered and there are finitely many ballots between $b_0$ and $b$ (rounds are natural numbers and ids are from a finite set), so the induction is well founded.

Let ACCEPT($b$, $w$) be sent with $b > b_0$, and assume the claim for all ballots $c$ with $b_0 < c < b$. Take the majority $S$ of P2c. Let $C$ be the majority that voted for $v$ in $b_0$. Two majorities of $n$ acceptors share at least one acceptor, because $|S| + |C| \ge 2(\lfloor n/2 \rfloor + 1) > n$. Let $a \in S \cap C$.

Acceptor $a$ votes in $b_0 < b$, so case (a) of P2c is false. So case (b) holds: $w$ is the value of the vote with the largest ballot $c$ below $b$ cast by the acceptors of $S$. Because $a$ votes in $b_0$, we have $c \ge b_0$. If $c = b_0$, then by Lemma 1 the value of that vote is $v$, so $w = v$. If $b_0 < c < b$, then the vote in $c$ was cast after a message ACCEPT($c$, $w$), and the induction hypothesis gives $w = v$.

For the second part, let $v$ be chosen in $b_0$ and $w$ in $b_1$. If $b_0 = b_1$, Lemma 1 gives $v = w$. If $b_0 < b_1$, a vote in $b_1$ needs a message ACCEPT($b_1$, $w$), and the first part gives $w = v$. The case $b_1 < b_0$ is the same with the roles swapped. $\square$

**Theorem (validity).** Each value in an ACCEPT message is the input of some proposer. So each chosen value and each learned value is an input.

*Proof.* By strong induction on the ballot. Line L8 sends an input. Line L7 sends a value $vv$ reported by an acceptor, and by Lemma 3 it is the value of a vote in a smaller ballot, so it came from an earlier ACCEPT message, whose value is an input by the induction hypothesis. Votes copy the value of an ACCEPT message (line L14). $\square$

**Theorem (learners).** If a learner learns $v$, then $v$ is chosen. So all learners learn the same value.

*Proof.* Line L17 runs when the set $S[b]$ holds a majority of distinct acceptors that sent ACCEPTED($b$, ...). Line L14 sends ACCEPTED($b$, $v$) only when the acceptor votes for $v$ in $b$, and by Lemma 1 all these votes have the same value $v$. So $v$ is chosen in $b$. By the agreement theorem, all learned values are equal. $\blacksquare$
