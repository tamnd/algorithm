---
title: Nested-loop join returns the join as a multiset and does the stated number of reads
proves: [correctness, termination, io.worst]
status: full
---

We use the line numbers of the pseudocode. Let $R$ be stored as pages $P_1, \ldots, P_M$ and $S$ as pages $Q_1, \ldots, Q_N$. A relation is a multiset, so we treat each stored tuple as a distinct occurrence: $R$ is the list of occurrences $r_1, \ldots, r_m$ in page order, and $S$ is $s_1, \ldots, s_n$. The join $R \bowtie_\theta S$ is the multiset that holds one copy of $r_i \cdot s_j$ for each pair of indices $(i, j)$ with $\theta(r_i, s_j)$ true.

**Lemma 1 (enumeration).** Lines L2 to L8 execute the test of line L8 exactly once for each pair of indices $(i, j)$ with $1 \le i \le m$ and $1 \le j \le n$, and for no other pair.

*Proof.* The loop of line L2 visits the pages $P_1, \ldots, P_M$ once each, and the loop of line L4 visits the tuples of the current page once each. The pages partition the occurrences of $R$, so each $r_i$ is the value of $r$ in exactly one iteration of line L4. Inside that iteration, lines L5 and L7 visit each occurrence $s_j$ exactly once in the same way. So the body of line L7 runs exactly once for each pair $(i, j)$. $\square$

**Theorem 1 (correctness).** NESTED-LOOP-JOIN returns a list whose multiset of elements is $R \bowtie_\theta S$.

*Proof.* By Lemma 1, line L8 considers each pair $(i, j)$ exactly once. It appends $r_i \cdot s_j$ exactly when $\theta(r_i, s_j)$ is true. No other line changes $out$ after line L1. So for each tuple $t$, the number of copies of $t$ in $out$ equals the number of pairs $(i, j)$ with $r_i \cdot s_j = t$ and $\theta(r_i, s_j)$ true, which is the multiplicity of $t$ in $R \bowtie_\theta S$. All loops are over finite lists, so the algorithm stops. $\blacksquare$

**Theorem 2 (page version).** PAGE-NESTED-LOOP-JOIN returns the same multiset.

*Proof.* Lines P2 and P4 visit each pair of pages $(P_a, Q_b)$ exactly once, and line P6 visits each pair of a tuple of $P_a$ and a tuple of $Q_b$ exactly once. Each pair $(i, j)$ of occurrences lies in exactly one pair of pages, so line P7 considers each pair $(i, j)$ exactly once, and the argument of Theorem 1 applies. $\blacksquare$

**Theorem 3 (I/O count).** The tuple version does exactly $M + mN$ page reads, which is $M + p_R M N$ when every page of $R$ holds $p_R$ tuples. The page version does exactly $M + MN$ page reads. Neither writes a page other than the output.

*Proof.* Reads happen only at lines L3 and L6. Line L3 runs once for each of the $M$ pages of $R$. Line L6 runs once for each page of $S$ in each iteration of line L4, and line L4 runs $m$ times in total, so line L6 runs $mN$ times. If each page holds $p_R$ tuples, $m = p_R M$. In the page version, line P3 runs $M$ times and line P5 runs $N$ times for each of the $M$ iterations of line P2, so the total is $M + MN$. Memory holds the current page of $R$, the current page of $S$ and one output page, so no intermediate page is written. $\blacksquare$
