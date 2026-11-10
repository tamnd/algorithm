---
title: Mencius learns one value per instance and runs the same sequence everywhere
proves: [correctness]
status: full
---

The model is asynchronous, with $n = 2F + 1$ servers, crash failures, and messages that can be delayed, reordered and duplicated but not changed. Every server is an acceptor in every instance. Ballots are pairs $(k, p)$ ordered as tuples. In instance $i$, ballot $(0, i \bmod n)$ belongs to the coordinator $c(i) = i \bmod n$, and a ballot $(k, p)$ with $k \ge 1$ belongs to server $p$. Each server uses each ballot at most once per instance.

A value $v$ is *chosen* in instance $i$ at ballot $b$ when a majority has accepted $(b, v)$ in $i$. A server *learns* $v$ in $i$ at line L4 (its own suggestion), L5 (a skip), or L10 (a revocation), or from a LEARN message sent at L4 or L10.

**Lemma 1 (the coordinator proposes once).** In each instance $i$, the coordinator does exactly one of these, at most once: it suggests one command at line L1, or it skips $i$ at line L3. It never does both.

*Proof.* Line L1 uses $I_p$ and then raises $I_p$ by $n$. Line L3 skips only instances $j \ge I_p$ and then sets $I_p$ above all of them. $I_p$ never decreases, and both lines use an instance only when it equals or exceeds the current $I_p$, after which $I_p$ is larger. So each own instance is used by at most one of the two lines, once. $\square$

**Lemma 2 (possible values).** Every value accepted in instance $i$, at any ballot, is no-op or the command $v_i$ that $c(i)$ suggested in $i$.

*Proof.* At ballot 0 only the SUGGEST of $c(i)$ is accepted (line L2), and by Lemma 1 it carries $v_i$. At ballot $b > 0$ the value is chosen at line L8: either no-op, or a value reported in phase 1, which was accepted at a lower ballot. By induction on the ballot, it is no-op or $v_i$. $\square$

**Lemma 3 (Paxos safety per instance).** If $v$ is chosen in $i$ at ballot $b$, then every value accepted in $i$ at a ballot $b' > b$ is $v$.

*Proof.* This is the safety argument of [Paxos](/paxos/), since lines L2, L7, L8 and L9 are its phases with ballot 0 as a ballot whose phase 1 is empty (no acceptor can have accepted anything below ballot 0). By induction on $b'$: the revoker of $b'$ got promises from a majority $P$, and a majority $A$ accepted $(b, v)$. Some $a \in A \cap P$ accepted $(b, v)$ before promising $b'$, because after the promise it would refuse $b < b'$ (lines L2 and L9). So $a$ reported a ballot $\ge b$, and the highest reported ballot $b''$ satisfies $b \le b'' < b'$, with value $v$ by the induction hypothesis (or by uniqueness at ballot $b$, since one ballot carries one value). Line L8 picks it. $\square$

**Lemma 4 (what is learned is chosen).** If a server learns $v$ in $i$, then $v$ is chosen in $i$, or $v$ = no-op and the coordinator skipped $i$; in the second case, no-op is the only value that can ever be chosen in $i$.

*Proof.* Lines L4 and L10 learn after a majority accepted at one ballot, so the value is chosen. A LEARN message carries such a value. A skip (line L5) comes from line L3 at $c(i)$; by Lemma 1, $c(i)$ suggested nothing in $i$, so by Lemma 2 every accepted value in $i$ is no-op, and only no-op can be chosen. $\square$

**Theorem 1 (agreement per instance).** No two servers learn different values in the same instance.

*Proof.* By Lemma 3, two values chosen in $i$ at ballots $b \le b'$ are equal (the votes at $b'$ are for the value chosen at $b$; at $b = b'$ one ballot carries one value). By Lemma 4 every learned value is chosen, or is no-op in an instance where only no-op can be chosen. So all learned values in $i$ are the same. $\square$

**Theorem 2 (same sequence).** At any time, the sequence of commands that one server has run is a prefix of the sequence of another, or the other way round.

*Proof.* Line L12 runs instances in index order and runs instance $i$ only after all smaller instances are learned. By Theorem 1 each instance has one learned value at every server that learned it. So each server's sequence is the list of non-no-op values of the instances $0, 1, \ldots, m - 1$ for some $m$, and two such lists are prefixes of one another. $\square$

**Theorem 3 (no duplicates).** A command appears at most once in the sequence.

*Proof.* A client command is given to one server, which suggests it at line L1. It suggests it again (line L11) only after it learns no-op in the instance of its last suggestion, which by Theorem 1 means that the command is not chosen there. So at any time, at most one instance can still choose the command. $\square$

**Theorem 4 (liveness).** Assume at most $F$ crashes, reliable delivery between live servers, and a failure detector that eventually suspects every crashed server and eventually lets one live server run a revocation without competition. Then every command given to a server that never crashes is eventually run by every live server.

*Proof.* Let $p$ be live and suggest $v$ in $i$. If no server revokes $i$, a live majority accepts at ballot 0 and $p$ learns $v$ (line L4). If $i$ is revoked and no-op is chosen, $p$ suggests $v$ again (line L11), and this repeats only while revocations of $p$'s instances happen, which eventually stop. Now take any $j < i$. If $c(j)$ is live, it got the SUGGEST for $i$ and, by line L3, it skipped $j$ or used it at line L1. If $c(j)$ crashed, it is eventually suspected and $j$ is revoked (lines L6 to L10), and a revocation without competition ends since a majority is live. The LEARN and SKIP messages reach every live server, so every instance up to $i$ is learned everywhere, and line L12 runs $v$. $\blacksquare$

The rule that a skip is learned with one message (Lemma 4) is what makes an idle server cheap, and Lemma 1 is what makes it safe. Rule 4 (Theorem 4) is needed only because the failure detector can suspect a live server.
