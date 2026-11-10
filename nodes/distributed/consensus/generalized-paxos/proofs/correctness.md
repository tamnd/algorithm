---
title: Generalized Paxos learns only compatible command histories
proves: [correctness]
status: full
---

The model is asynchronous, with crash failures, stable storage at acceptors, and messages that can be lost, duplicated and reordered. C-structs are command histories. Quorums satisfy: (Q1) any two quorums meet, and (Q2) for a fast ballot $k$, any two k-quorums and any quorum have a common acceptor. Ballots are totally ordered, and only the leader named in a ballot sends 2a messages for it.

A c-struct $v$ is *chosen in ballot* $j$ when there is a j-quorum $R$ such that each $a \in R$ has, at some time, a vote in $j$ that extends $v$.

**Lemma 1 (pairwise compatible histories have a lub).** If the histories in a finite set $T$ are pairwise compatible, $T$ has a least upper bound.

*Proof.* Let $U$ be the union of the command sets. Take two interfering commands $x, y \in U$. If $x$ is only in $t$ and $y$ is only in $t' \ne t$, then $t$ and $t'$ have no common upper bound, since an upper bound of $t$ must put $y$ after $x$ and an upper bound of $t'$ must put $x$ after $y$. So some $t$ holds both, and all members that hold both order them in the same way, by compatibility. This defines an order on each interfering pair of $U$. Each $t \in T$ is downward closed in it: if $x \in t$ and $y$ comes before $x$ in some $t'$, then $y \in t$, or else $t$ and $t'$ have no common upper bound. If these orders formed a cycle, take a member $t$ that holds one command of the cycle. By downward closure $t$ holds the command before it, and so on around the cycle, so $t$ holds the whole cycle, but the order inside $t$ has no cycle. So $U$ with these orders is a history, each $t$ is a prefix of it, and it is the least such history because it has no other commands or orders. $\square$

**Lemma 2 (votes in one ballot grow).** For each acceptor $a$ and ballot $m$, the votes of $a$ in $m$ form a chain in the prefix order. After $a$ sends 1b($m'$) with $m' > m$, it never votes in $m$ again.

*Proof.* Line L8 replaces a vote in the same ballot only by an extension $v \sqsupseteq vval$. Line L9 appends a command. Line L8 needs $m \ge bal$ and line L9 needs $bal = vrnd = m$. Line L7 sets $bal \leftarrow m' > m$, and $bal$ never decreases, so neither line can vote in $m$ after that. Each 1b reports $vrnd < m'$, since $vrnd \le bal < m'$. $\square$

**Lemma 3 (votes of a classic ballot are compatible).** In a classic ballot $k$, all votes are prefixes of the last c-struct that the leader of $k$ sends.

*Proof.* In a classic ballot line L9 does nothing, so each vote is a value of a 2a message. The leader sends a chain of values: line L2 sends $w$, and line L5 sends only extensions of it. $\square$

**Lemma 4 (ProvedSafe is defined).** In line L4 the values $\gamma(R) = \sqcap\{vval_a : a \in Q \cap R\}$ for $R \in RS$ have a lub.

*Proof.* Each $Q \cap R$ is not empty by (Q1). If $k$ is classic, each $vval_a$ with $vrnd_a = k$ is a vote in $k$, so by Lemma 3 all of them, and so all the $\gamma(R)$, are prefixes of one c-struct, and the lub exists. If $k$ is fast, for $R_1, R_2 \in RS$ there is $a \in Q \cap R_1 \cap R_2$ by (Q2), and both $\gamma(R_1)$ and $\gamma(R_2)$ are prefixes of $vval_a$. So the $\gamma$ values are pairwise compatible, and Lemma 1 gives the lub. $\square$

**Lemma 5 (ProvedSafe extends chosen values).** Let $Q$ be an m-quorum whose 1b messages for $m$ the leader uses in line L2. Let $j < m$ and let $v$ be chosen in $j$. If every vote in each ballot $c$ with $j < c < m$ extends $v$, then ProvedSafe($Q$) extends $v$.

*Proof.* Let $R$ be the j-quorum that chose $v$. By (Q1) some $a_0 \in Q \cap R$. By Lemma 2, $a_0$ voted in $j$ before its 1b, so its report has $vrnd \ge j$, and $k \ge j$.

If $k > j$, each reported $vval_a$ with $vrnd_a = k$ is a vote in ballot $k$ with $j < k < m$, so it extends $v$. ProvedSafe returns either one of these votes, or a lub of common prefixes of these votes. A common prefix of c-structs that all extend $v$ extends $v$, and so does a lub of them.

If $k = j$, each $a \in Q \cap R$ voted in $j$ and reports $vrnd_a \le k = j$, so $vrnd_a = j$, and $R \in RS$. By Lemma 2 the report of $a$ is its last vote in $j$, which extends the vote that helped choose $v$, so it extends $v$. Then $\gamma(R) \sqsupseteq v$, and the lub of line L4 extends $\gamma(R)$. $\square$

**Lemma 6 (later votes extend chosen values).** If $v$ is chosen in ballot $j$, every vote in every ballot $m > j$ extends $v$.

*Proof.* Strong induction on $m$. Every vote in $m$ starts from the value $w$ of a 2a($m$, $w$) message (line L8), and is $w$ or an extension of it by appends (lines L5 and L9). The first such $w$ is ProvedSafe($Q$) followed by appends (line L2). The induction hypothesis gives the condition of Lemma 5 for all ballots $c$ with $j < c < m$, so $w \sqsupseteq v$, and each vote in $m$ extends $v$. $\square$

**Theorem (consistency).** Any two chosen c-structs are compatible. So the values of all learners, at all times, are compatible.

*Proof.* Let $v$ be chosen in $j$ by $R$ and $v'$ in $j' \ge j$ by $R'$. If $j' > j$, each vote of $R'$ in $j'$ extends $v$ by Lemma 6, and $v'$ is a prefix of a vote of $R'$, so $v'$ and $v$ are both prefixes of that vote. If $j' = j$ is classic, both are prefixes of the leader's last c-struct by Lemma 3. If $j' = j$ is fast, (Q2) applied to $R$, $R'$ and any quorum gives a common acceptor $a$, and by Lemma 2 its last vote in $j$ extends both $v$ and $v'$. In all cases $v$ and $v'$ have a common upper bound.

Line L11 adds to a learner's value only common prefixes of votes of a whole quorum in one ballot, which are chosen c-structs (lines L10 and L11 use only 2b messages, and each one reports a real vote). So each learned value is the lub of a finite set of chosen c-structs. The union of these sets for all learners and times is pairwise compatible, so by Lemma 1 it has an upper bound, and every learned value is a prefix of it. $\square$

**Theorem (nontriviality and stability).** Each learned value holds only proposed commands, and each learner's value only grows.

*Proof.* Every c-struct in a message is built from $\bot$ by appends of commands from proposals (lines L2, L5 and L9), and common prefixes and lubs add no command. Line L11 replaces the learned value by a lub that contains it. $\blacksquare$
