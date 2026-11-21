---
title: Incognito returns all k-anonymous full-domain generalizations and the minimal ones
proves: [correctness]
status: full
---

The table $T$ has $n$ rows and $d$ quasi-identifier attributes. Attribute $a$ has a hierarchy with levels $0, \ldots, h_a$, and each level coarsens the level below it. A *node* is a pair $(A, l)$: a set $A$ of attributes, written in increasing order, and a level $l_a$ for each $a \in A$. The node is *anonymous* when the projection of $T$ on $A$, with each attribute $a$ generalized to level $l_a$, has no combination of values that occurs fewer than $k$ times. A direct generalization of $(A, l)$ raises one level by one, and a direct specialization lowers one level by one. Line L8 computes the frequency set of a node, and line L9 tests that each count is at least $k$, so a check of a node is correct when its frequency set is correct.

**Lemma 1 (generalization).** If $(A, l)$ is anonymous and $l \le l'$ for each attribute, then $(A, l')$ is anonymous.

*Proof.* The value at a higher level is a function of the value at a lower level, so each group of equal rows at $l'$ is a union of groups at $l$. A union of groups of at least $k$ rows has at least $k$ rows. $\square$

**Lemma 2 (subset).** If $(A, l)$ is anonymous and $B \subseteq A$, then $(B, l|_B)$ is anonymous.

*Proof.* Rows that are equal on $A$ are equal on $B$, so each group on $B$ is a union of groups on $A$. $\square$

**Lemma 3 (roll-up).** The roll-up of line L8 is the frequency set of the node.

*Proof.* A node $c$ gets a parent link at line L12 only from a direct specialization $b$ that was checked, with the frequency set of $b$, at a position $p$ with $c_p = b_p + 1$. Because the hierarchy of the attribute at position $p$ is a tree, each value at level $b_p$ has one parent value at level $b_p + 1$. So the rows of a combination of $b$ all go to one combination of $c$, and summing the counts of $b$ by the new combination gives the counts of $c$. By induction on the order of the checks, the frequency set of $b$ is correct, so the frequency set of $c$ is correct. $\square$

**Lemma 4 (one round).** Let $C$ be the set of candidate nodes of size $i$ at line L3. After the loop of line L5, $S = \{c \in C : c \text{ is anonymous}\}$.

*Proof.* A node leaves $S$ only at line L11, after a check that fails, so no anonymous node leaves $S$. We show by strong induction on the height $\sum_a l_a$ that each node $c \in C$ that is not anonymous is checked, so that line L11 removes it. Two facts help. First, a node is marked at line L10 only when a direct specialization of it is checked and is anonymous, and only nodes of $C$ are checked. Second, by Lemma 1 a direct generalization of an anonymous node is anonymous.

Let $c \in C$ not be anonymous. Then no direct specialization of $c$ is anonymous, by Lemma 1, so $c$ is never marked, and line L7 does not skip it if it is ever in the queue. If $c$ has no direct specialization in $C$, line L4 puts it in the queue. Otherwise each direct specialization $b \in C$ of $c$ has a lower height and is not anonymous, so by the induction hypothesis $b$ is checked and fails. Then line L12 puts $c$ in the queue, unless it is already there. In both cases $c$ is popped at line L6 and checked, and by Lemma 3 the check is correct. So $c$ fails the test of line L9 and leaves $S$ at line L11. $\square$

**Lemma 5 (candidates).** For each $i$, the candidate set $C_i$ of size $i$ holds every anonymous node of size $i$.

*Proof.* Line L1 puts every node of size 1 in $C_1$. Assume the claim for $i$, and let $N = (A, l)$ be an anonymous node of size $i + 1$, with attributes $a_1 < \cdots < a_{i+1}$. By Lemma 2, each node that $N$ gives on $i$ of its attributes is anonymous. By the hypothesis and Lemma 4, all of them are in $S$ after round $i$. Let $x$ be $N$ without $a_{i+1}$ and $y$ be $N$ without $a_i$. They agree on $a_1, \ldots, a_{i-1}$ and their levels, and the last attribute of $x$ is less than the last attribute of $y$. So line L13 joins them into $N$, and the test that each $i$-subset of $N$ is in $S$ holds. So $N \in C_{i+1}$. $\square$

**Theorem.** INCOGNITO returns the list of all vectors $v$ over the $d$ attributes such that $T$ generalized by $v$ is k-anonymous, and the list of the vectors of it that have no k-anonymous vector strictly below them.

*Proof.* A node of size $d$ is a vector over all attributes. By Lemma 5, $C_d$ holds every anonymous vector, and by Lemma 4 the set $S$ after round $d$ is exactly the set of anonymous vectors. Line L14 returns it. Line L15 keeps the vectors $v$ of $S$ with no direct specialization in $S$. If an anonymous $u$ is strictly below $v$, then raise the levels of $u$ one at a time toward $v$. The last vector before $v$ on this chain is a direct specialization of $v$, it is at least $u$, and it is anonymous by Lemma 1. So $v$ has no anonymous vector strictly below it if and only if it has no anonymous direct specialization. $\blacksquare$

**Remark.** The order of the priority queue is not used in the proof. Processing by height is what makes the marks useful. Line L12 pushes only nodes one level above the popped node, so the heights of the popped nodes never go down. So a node is popped after each of its direct specializations that is ever popped, and a mark set by any of them is seen before the check.
