---
title: The symmetric hash join emits the join of the prefixes, each pair once
proves: [correctness, termination, space.extra]
status: full
---

We use the line numbers of the pseudocode. The inputs are relations $R$ and $S$ with the set $J$ of common attributes. We use bag semantics: every arriving tuple is a separate occurrence, and the join $X \bowtie Y$ of two bags holds one copy of the combined tuple $r \cdot s$ for each pair of occurrences $r \in X$, $s \in Y$ with $r[J] = s[J]$ and no NULL in $r[J]$ or $s[J]$. This is the SQL rule: NULL never matches.

The arrivals are $a_1, a_2, \dots$. Let $R_j$ and $S_j$ be the bags of occurrences of $R$ and $S$ among $a_1, \dots, a_j$, and let $O_j$ be the bag of tuples emitted by the first $j$ iterations of line L2. A tuple is *storable* if its key has no NULL.

**Lemma 1 (tables).** After iteration $j$, $H_R$ holds exactly the storable occurrences of $R_j$, each once, under their keys, and $H_S$ holds exactly the storable occurrences of $S_j$.

*Proof.* By induction on $j$. Before the first iteration both tables are empty (line L1). Iteration $j$ changes only the table of the side of $a_j$, and only at line L6, which runs if and only if $a_j$ is storable (line L5). It appends $a_j$ to the bucket of its key and never removes an entry. $\square$

**Lemma 2 (one step).** If $a_j = t$ is an occurrence of $R$, iteration $j$ emits exactly the bag $\{t\} \bowtie S_{j-1}$. If $a_j$ is an occurrence of $S$, it emits $R_{j-1} \bowtie \{t\}$.

*Proof.* Take $a_j = t$ in $R$; the other case is symmetric. If $t$ is not storable, line L5 skips it and nothing is emitted; also $\{t\} \bowtie S_{j-1}$ is empty, because a NULL in $t[J]$ matches nothing. Otherwise line L6 inserts $t$ into $H_R$, which does not change $H_S$. By Lemma 1 for $j - 1$, the bucket of $k = t[J]$ in $H_S$ holds exactly the storable occurrences $u$ of $S_{j-1}$ with $u[J] = k$, each once. These are exactly the occurrences of $S_{j-1}$ that join with $t$, because an occurrence that is not storable joins with nothing. Lines L7 and L8 emit $t \cdot u$ once for each of them. $\square$

**Theorem 1 (correctness).** For every $j \ge 0$, $O_j = R_j \bowtie S_j$ as bags.

*Proof.* By induction on $j$. For $j = 0$ both sides are empty. Suppose $O_{j-1} = R_{j-1} \bowtie S_{j-1}$ and $a_j = t$ is in $R$. Then $R_j = R_{j-1} + \{t\}$ and $S_j = S_{j-1}$. The bag join distributes over the sum of bags:
$$R_j \bowtie S_j = (R_{j-1} \bowtie S_{j-1}) + (\{t\} \bowtie S_{j-1}).$$
By the induction hypothesis and Lemma 2, the right side is $O_{j-1}$ plus the tuples of iteration $j$, which is $O_j$. The case $a_j \in S$ is the same with the roles exchanged. $\blacksquare$

**Corollary 1 (each pair once, at the earliest time).** Let $r$ be the $i$-th arrival and $s$ the $j$-th arrival, with $r \in R$, $s \in S$ and $r[J] = s[J]$ free of NULL. Then $r \cdot s$ is emitted for this pair exactly once, in iteration $\max(i, j)$.

*Proof.* If $i < j$, the pair is in $R_{j-1} \bowtie \{s\}$, which iteration $j$ emits by Lemma 2, and in no earlier iteration, because $s$ has not arrived. Later iterations emit only pairs that contain their own arriving tuple. The case $j < i$ is symmetric. No algorithm that reads the inputs in this order can emit the pair before iteration $\max(i, j)$, since one of the two tuples is not yet known. $\square$

**Termination.** Each iteration does a finite amount of work, because a bucket holds at most the number of earlier arrivals. So the join stops after a finite input, and for an infinite input each iteration ends.

**Theorem 2 (memory).** After iteration $j$, the tables hold exactly the storable occurrences among $a_1, \dots, a_j$, at most $j$ tuples. With no NULL keys, this is exactly $j$.

*Proof.* This is Lemma 1. $\blacksquare$

The memory bound is tight for an unbounded join: if every later tuple can match any stored tuple, no stored tuple can be dropped without losing output. A window or a punctuation that says that a key will not occur again is the only way to drop tuples, and then the join computes a different result, the window join.
