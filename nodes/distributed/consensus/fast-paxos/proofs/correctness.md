---
title: Fast Paxos chooses at most one value under the Quorum Requirement
proves: [correctness]
status: full
---

The model is asynchronous, with crash failures and messages that can be lost, duplicated and reordered. Rounds are totally ordered. A value $v$ is *chosen in round* $j$ when every acceptor of some $j$-quorum votes for $v$ in round $j$ (line L12). We assume the Quorum Requirement: (a) any $i$-quorum and any $j$-quorum meet, and (b) if $j$ is fast, any $i$-quorum and any two $j$-quorums have a common acceptor. A value $w$ is *safe at round* $i$ if no value other than $w$ is chosen in any round $j < i$, at any time of the run.

**Lemma 0 (counting form).** Let quorums be the sets of at least $q_c$ acceptors (classic) and at least $q_f \ge q_c$ acceptors (fast), out of $n$. Then the Quorum Requirement holds if and only if $2q_c > n$ and $q_c + 2q_f > 2n$.

*Proof.* Sets $S_1, S_2, S_3$ of sizes $s_1, s_2, s_3$ have a common element if and only if their complements do not cover all $n$ acceptors. If $s_1 + s_2 + s_3 > 2n$, the complements have total size below $n$, so they cannot cover. If $s_1 + s_2 + s_3 \le 2n$, the complements have sizes $n - s_t$ with total at least $n$, so we can choose them to cover all acceptors, and then the three sets have no common element. The same argument with two sets gives: they always meet if and only if $s_1 + s_2 > n$. Condition (a) for the smallest sets is $2q_c > n$; the other pairs are larger. Condition (b) with the smallest sets is $q_c + 2q_f > 2n$. Larger quorums only make intersections larger. $\square$

**Lemma 1 (votes).** An acceptor votes at most once in each round, and the rounds of its votes never decrease. After it sends 1b($i$, vrnd, vval), it never votes in a round below $i$, and (vrnd, vval) is its vote with the largest round below $i$, or $\bot$.

*Proof.* Line L12 sets rnd to the round $i$ of the vote. Line L10 votes in round $i$ only if $i \ge$ rnd and there is no vote in round $i$ yet. Line L11 votes only in round rnd and only if there is no vote in that round. So votes come in nondecreasing rounds, and at most one per round. Line L9 sends 1b($i$, ...) after it sets rnd $\leftarrow i$, and rnd never decreases, so no later vote is in a round below $i$. vrnd and vval are written only by line L12, so they hold the last vote, which by monotonicity is the one with the largest round, and that round is at most the old rnd, which is below $i$. $\square$

In coordinated recovery, the 2b($i$, $v$) message of an acceptor stands for 1b($i+1$, $i$, $v$). Lemma 1 also holds for it: after the vote in round $i$ the acceptor has rnd at least $i$, it never votes in a round below $i$ again, and it never votes a second time in round $i$. So its vote in round $i$ is its vote with the largest round below $i + 1$.

**Lemma 2 (one value in a classic round).** In a classic round, all votes are for the same value.

*Proof.* The coordinator of round $i$ sends 2a($i$, ...) at most once, and in a classic round its value is not Any (line L4 gives Any only in a fast round). Line L11 votes only in a round with Any. So each vote in a classic round $i$ comes from line L10 with the single value of the 2a message. $\square$

**Lemma 3 (the rule is safe).** Let the coordinator of round $i$ run lines L3 to L7 on the reports of a classic quorum $Q$. Assume that each vote in each round $j < i$ is for a value safe at $j$. Then the value $v$ it returns is safe at $i$, and if $v$ = Any, every value is safe at $i$.

*Proof.* By Lemma 1, the votes of the acceptors of $Q$ in rounds below $i$ are exactly the reported ones, and no acceptor of $Q$ votes again in a round below $i$.

*Rounds $j$ with $k < j < i$.* No acceptor of $Q$ ever votes in round $j$. Each $j$-quorum meets $Q$ by (a), so no $j$-quorum votes in full, and no value is chosen in round $j$. If no acceptor of $Q$ has voted (line L4), this holds for all $j < i$, so every value is safe at $i$, and both Any and a proposed value are allowed.

From now on $k$ is defined. Let $V$ be the set of values that acceptors of $Q$ voted for in round $k$.

*Rounds below $k$.* Each $w \in V$ is safe at $k$ by the assumption. So no value other than $w$ is chosen below $k$. If $|V| \ge 2$, two different values are both safe at $k$, so no value at all is chosen below $k$.

*Round $k$.* Let $u$ be chosen in round $k$ with a $k$-quorum $R$. Each acceptor of $R \cap Q$ voted $u$ in round $k$, and by Lemma 1 it votes only once in round $k$, so its reported vote is $u$. So O4($u$) holds, and $R \cap Q$ is not empty by (a), so $u \in V$.

*Case $V = \{w\}$ (line L5).* Any value chosen in round $k$ is in $V$, so it is $w$. No value other than $w$ is chosen below $k$, nor strictly between $k$ and $i$. So $w$ is safe at $i$.

*Case $|V| \ge 2$.* By Lemma 2, round $k$ is fast. At most one value satisfies O4: if O4($u$) holds with the fast quorum $R$ and O4($u'$) with the fast quorum $R'$, condition (b) gives an acceptor in $Q \cap R \cap R'$, and it voted both $u$ and $u'$ in round $k$, so $u = u'$. If O4($w$) holds (line L6), the only value that can be chosen in round $k$ is $w$. If O4 holds for no value (line L7), no value is chosen in round $k$. In both cases nothing is chosen below $k$ or between $k$ and $i$, so the returned value is safe at $i$. $\square$

**Lemma 4 (every vote is safe).** Each vote in each round $i$ is for a value that is safe at $i$.

*Proof.* By strong induction on $i$. A vote in round $i$ comes from line L10 with the value of 2a($i$, $v$), or from line L10 or L11 with a client value after 2a($i$, Any). The coordinator chose $v$ by lines L3 to L7, either from 1b reports or, in coordinated recovery, from the 2b messages of round $i - 1$, which are valid reports by the remark after Lemma 1. All votes in rounds below $i$ are safe by the induction hypothesis, so Lemma 3 applies: $v$ is safe at $i$, and if $v$ = Any then every value is safe at $i$. $\square$

**Theorem (agreement).** If $v$ is chosen in round $j$ and $w$ is chosen in round $i$, then $v = w$.

*Proof.* Assume $j \le i$. If $j = i$ and the round is classic, Lemma 2 gives $v = w$. If $j = i$ and the round is fast, the two $i$-quorums meet by (a), and by Lemma 1 the common acceptor voted only once in round $i$, so $v = w$. If $j < i$, the acceptors of the quorum that chose $w$ voted $w$ in round $i$, so by Lemma 4, $w$ is safe at $i$. Since $v$ is chosen in round $j < i$, the definition of safe gives $v = w$. $\square$

**Theorem (validity).** Each chosen value was proposed by a client.

*Proof.* A vote is for a client proposal (line L11, or line L10 after Any), or for the value of a 2a message. Lines L4 and L7 send a proposed value or Any, and lines L5 and L6 send a value that an acceptor voted for earlier. Induction on the round gives the claim. $\square$

**Theorem (learners).** A learner learns only a chosen value, so all learners learn the same value.

*Proof.* Line L13 needs 2b($i$, $v$) from each acceptor of an $i$-quorum, and an acceptor sends 2b($i$, $v$) only when it votes $v$ in round $i$. So $v$ is chosen in round $i$, and agreement gives the rest. $\blacksquare$
