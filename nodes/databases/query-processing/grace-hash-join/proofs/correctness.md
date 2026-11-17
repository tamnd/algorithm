---
title: Grace hash join returns the join as a multiset, stops, and costs 3(M + N) without recursion
proves: [correctness, termination, io.best]
status: full
---

We use the line numbers of the pseudocode. We treat each stored tuple as a distinct occurrence. For multisets $X \subseteq R$ and $Y \subseteq S$, write $X \bowtie Y$ for the multiset with one copy of $r \cdot s$ for each pair $(r, s) \in X \times Y$ with $r.a = s.b$. We assume that the in-memory hash join of line L5 and the block nested-loop join of line L10 are correct; this is proved on the pages [hash join](/hash-join/) and [block nested-loop join](/block-nested-loop-join/).

**Lemma 1 (partitioning).** Let lines L6 and L7 split $R'$ and $S'$ with the function $g(x) = h_1(x, \ell) \bmod (B - 1)$. Then $R' \bowtie S' = \biguplus_{i=0}^{B-2} R_i \bowtie S_i$, the multiset sum.

*Proof.* Each occurrence of $R'$ is written to exactly one partition, $R_{g(r.a)}$, and each occurrence of $S'$ to exactly one, $S_{g(s.b)}$. So the sets $R_i \times S_i$ are disjoint. Take a matching pair $(r, s)$ of $R' \times S'$. Since $r.a = s.b$, $g(r.a) = g(s.b)$, so the pair lies in $R_i \times S_i$ for $i = g(r.a)$, and in no other $R_j \times S_j$. Conversely each matching pair of some $R_i \times S_i$ is a matching pair of $R' \times S'$. So each matching pair of $R' \times S'$ is counted exactly once on the right side. $\square$

**Invariant.** At each test of line L2, let $\mathcal{P}$ be the multiset of pairs on the stack. Then

$$out \uplus \biguplus_{(X, Y, \ell) \in \mathcal{P}} X \bowtie Y = R \bowtie S.$$

*Initialization.* After line L1, $out$ is empty and the stack holds $(R, S, 0)$.

*Maintenance.* Line L3 removes one pair $(R', S', \ell)$. If line L5 runs, it appends $R' \bowtie S'$ to $out$ by the correctness of the hash join, and the sum is unchanged. Otherwise lines L6 and L7 split the pair, and by Lemma 1 the term $R' \bowtie S'$ equals the sum of the terms $R_i \bowtie S_i$. For each $i$, line L9 drops a pair with an empty side, whose term is empty. Line L10 appends $R_i \bowtie S_i$ to $out$, by the correctness of block nested loops. Line L11 pushes the pair, so its term moves back into the sum. In every case the equation holds again.

**Termination.** Line L11 pushes a pair only when its level $\ell + 1$ is below the depth limit $D$. So every pair on the stack has a level less than $D$. A pair at level $\ell$ pushes at most $B - 1$ pairs at level $\ell + 1$, so the total number of pairs ever pushed is at most $\sum_{\ell=0}^{D-1} (B - 1)^\ell$, which is finite. Each iteration pops one pair, so the loop stops.

**Theorem 1 (correctness).** GRACE-HASH-JOIN returns a list whose multiset of elements is $R \bowtie S$.

*Proof.* When the loop stops, the stack is empty, and the invariant gives $out = R \bowtie S$. $\blacksquare$

**Theorem 2 (I/O count without recursion).** Assume that, after the first partitioning, every pair with two nonempty sides has $f \cdot |R_i| \le B - 2$, that every partition page written is full, and that every partition is nonempty. Then the algorithm does exactly $3(M + N)$ page I/Os, without the writes of the output.

*Proof.* Lines L6 and L7 read $M + N$ pages. Each tuple is written once, and since every page written is full, the partitions take $M + N$ pages, so there are $M + N$ writes. Every pair has two nonempty sides and fits, so line L11 pushes each of them, and line L5 later reads each of them once without partitioning it again: $M + N$ reads. Line L10 does not run. The total is $3(M + N)$. $\blacksquare$

**The memory condition.** If $h_1$ spreads the tuples of $R$ evenly, each $R_i$ has at most $\lceil M/(B - 1) \rceil$ pages. The test of line L4 then passes when $f \lceil M/(B - 1) \rceil \le B - 2$. For example $f M \le (B - 1)(B - 2)$ is enough when $B - 1$ divides $M$, which is the precise form of the rule $B > \sqrt{f M}$ of Ramakrishnan and Gehrke, up to a small additive constant. $\blacksquare$
