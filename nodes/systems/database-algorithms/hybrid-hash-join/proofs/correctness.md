---
title: Hybrid hash join returns the join as a multiset, stops, and costs M + N + 2W with one level
proves: [correctness, termination, io.average, io.best]
status: full
---

We use the line numbers of the pseudocode. We treat each stored tuple as a distinct occurrence. For multisets $X \subseteq R$ and $Y \subseteq S$, write $X \bowtie Y$ for the multiset with one copy of $r \cdot s$ for each pair $(r, s) \in X \times Y$ with $r.a = s.b$. We assume that the in-memory hash join of line L4 and the block nested-loop join of line L15 are correct; this is proved on the pages [hash join](/hash-join/) and [block nested-loop join](/block-nested-loop-join/). We also assume that the lookup of line L13 returns exactly the tuples of $H_0$ with key $s.b$, which is the correctness of a [hash table](/hash-table/) with chaining.

**Lemma 1 (one level).** Let one pass of lines L5 to L13 handle the pair $(R', S')$ with $k \ge 1$. Let $H_0$ be the multiset of tuples inserted by line L8, let $R_1, \dots, R_{k+1}$ and $S_1, \dots, S_{k+1}$ be the partitions written, and let $O$ be the multiset that line L13 appends to $out$. Then
$$R' \bowtie S' = O \uplus \biguplus_{i=1}^{k+1} R_i \bowtie S_i.$$

*Proof.* Write $g(x) = h_1(x, \ell) \bmod (c + k d)$ and $\pi(j) = 1 + \lfloor (j - c)/d \rfloor$ for $j \ge c$. By lines L6 to L9, each occurrence $r$ of $R'$ is in exactly one place: in $R_{\pi(g(r.a))}$ if $g(r.a) \ge c$, and otherwise in $H_0$ or in $R_{k+1}$. Let $S_0$ be the tuples $s$ of $S'$ with $g(s.b) < c$. By lines L11 to L13, a tuple $s$ with $g(s.b) \ge c$ is in $S_{\pi(g(s.b))}$ only, and $S_{k+1} = S_0$ if $R_{k+1}$ is not empty, while $S_{k+1}$ is empty otherwise.

Take a matching pair $(r, s)$ of $R' \times S'$. Since $r.a = s.b$, the slots are equal: $g(r.a) = g(s.b) = j$.

- If $j \ge c$, then $r \in R_i$ and $s \in S_i$ for $i = \pi(j) \le k$. The pair is counted in $R_i \bowtie S_i$. It is not in $O$, because $s \notin S_0$, and not in any other term, because $r$ is in no other partition.
- If $j < c$ and $r \in H_0$, then $s \in S_0$, and line L13 appends $r \cdot s$ once to $O$ by the assumption on the lookup. The pair is in no term $R_i \bowtie S_i$, because $r$ is in no $R_i$.
- If $j < c$ and $r \in R_{k+1}$, then $R_{k+1}$ is not empty, so $s \in S_{k+1}$, and the pair is counted in $R_{k+1} \bowtie S_{k+1}$. It is not in $O$, because line L13 finds only tuples of $H_0$, and it is in no other term.

Conversely, every element of $O$ and of each $R_i \bowtie S_i$ comes from a matching pair of $R' \times S'$, because $H_0$ and the $R_i$ hold tuples of $R'$ and the $S_i$ hold tuples of $S'$. So each matching pair is counted exactly once on the right side, and nothing else is. $\square$

**Invariant.** At each test of line L2, let $\mathcal{P}$ be the multiset of pairs on the stack. Then
$$out \uplus \biguplus_{(X, Y, \ell) \in \mathcal{P}} X \bowtie Y = R \bowtie S.$$

*Initialization.* After line L1, $out$ is empty and the stack holds $(R, S, 0)$.

*Maintenance.* Line L3 removes one pair $(R', S', \ell)$. If line L4 runs, it appends $R' \bowtie S'$ to $out$ by the correctness of the hash join, and the sum is unchanged. Otherwise line L13 appends $O$ to $out$, and by Lemma 1 the removed term $R' \bowtie S'$ equals $O$ plus the terms $R_i \bowtie S_i$. Line L14 skips a pair with an empty side, whose term is empty. For each other pair, line L15 either appends $R_i \bowtie S_i$ to $out$, by the correctness of block nested loops, or pushes the pair, so its term returns to the sum. In every case the equation holds again.

**Termination.** Let $D$ be the depth limit. Line L15 pushes a pair at level $\ell + 1$ only if the pair fits, or if $\ell + 1 < D$. A pair that fits has $f \cdot |R_i| \le B - 2$, so PLAN returns $k = 0$ for it and line L4 handles it without pushing anything. So every pair that pushes has a level below $D$, and every pair on the stack has a level at most $D$. A pair pushes at most $k + 1 \le B$ pairs, so the number of pairs ever pushed is at most $\sum_{\ell=0}^{D} B^\ell$, which is finite. Each iteration pops one pair, so the loop stops.

**Theorem 1 (correctness).** HYBRID-HASH-JOIN returns a list whose multiset of elements is $R \bowtie S$.

*Proof.* When the loop stops, the stack is empty, and the invariant gives $out = R \bowtie S$. $\blacksquare$

**Theorem 2 (I/O count).** If $f M \le B - 2$, the algorithm does exactly $M + N$ page I/Os. Otherwise, assume that after the first level every disk pair has two nonempty sides and fits, $f \cdot |R_i| \le B - 2$. Let $W$ be the number of pages written by lines L7, L9, L12 and L13. Then the algorithm does exactly $M + N + 2W$ page I/Os, without the writes of the output.

*Proof.* If $f M \le B - 2$, PLAN returns $k = 0$, and line L4 reads each page of $R$ and of $S$ once and writes nothing: $M + N$. Otherwise lines L5 and L10 read $M + N$ pages, and the partitions are written with $W$ page writes. The tuples of $H_0$ and the probes of line L13 cost no I/O, because $H_0$ stays in memory. By the assumption, line L15 pushes every pair, and line L4 later reads each of them once without partitioning again. These pairs are all the pages written, so they cost $W$ reads. Line L15 never runs block nested loops. The total is $M + N + 2W$. $\blacksquare$

**The share kept in memory.** Suppose there is no overflow, every page written is full, and a share $\rho$ of the tuples of each relation falls in the slots below $c$. Then $W = (1 - \rho)(M + N)$, and Theorem 2 gives $(3 - 2\rho)(M + N)$. For $\rho = 0$ this is the cost $3(M + N)$ of the Grace hash join. $\blacksquare$
