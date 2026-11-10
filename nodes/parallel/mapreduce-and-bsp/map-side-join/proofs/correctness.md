---
title: The broadcast join and the merge join output exactly the join, with multiplicities
proves: [correctness]
status: full
---

The relations are bags: $R$ holds tuples $(a, b)$ and $S$ holds tuples $(b, c)$. The join $R \bowtie S$ is the bag in which $(a, b, c)$ has multiplicity $m_R(a, b) \cdot m_S(b, c)$. Equivalently, the join is the bag of all *matching pairs* $(r, s)$ with $r \in R$, $s \in S$ and the same join value, where copies count as different elements. The line numbers refer to the `pseudo id=main` block of the page.

## The broadcast join

**Theorem 1.** BROADCAST-JOIN outputs each matching pair exactly once.

*Proof.* The splits $R_1, \ldots, R_M$ cut $R$, so each tuple $r \in R$ is in exactly one split. Every map task gets a full copy of $S$ (line L1) and builds the table $T$ of line L3, in which $T[b]$ is the list of the $c$ values of the tuples of $S$ with join value $b$, one entry for each tuple. The task that holds $r = (a, b)$ outputs $(a, b, c)$ once for each entry of $T[b]$ (lines L4 and L5), so it outputs the pair $(r, s)$ exactly once for each $s \in S$ with join value $b$, and nothing else for $r$. No other task reads $r$. So each matching pair is output exactly once, and no other tuple is output. $\blacksquare$

## The merge join of one part

Fix a part $i$. The lists $R_i$ and $S_i$ are sorted by the join value. Call a matching pair $(R_i[x], S_i[y])$ *done* if $x < p$ and $y < q$, *open* if $x \ge p$ and $y \ge q$, and *split* otherwise.

**Lemma 2.** Each time line L7 tests its condition, no matching pair is split, and the output so far holds each done pair exactly once and no other tuple.

*Proof.* At the start, $p = q = 0$, every pair is open and the output is empty. Assume the claim holds before an iteration, and let $u$ be the join value of $R_i[p]$ and $v$ that of $S_i[q]$.

*Case $u < v$ (line L8).* A partner of $R_i[p]$ in $S_i$ has join value $u$. It is not at a position $y \ge q$, because those values are at least $v > u$ by the sort. It is not at a position $y < q$, because then the pair would be split. So $R_i[p]$ has no partner, and moving $p$ by one makes no pair split and no pair done.

*Case $u > v$ (line L9).* The same argument with the roles of $R_i$ and $S_i$ swapped.

*Case $u = v$ (lines L10 to L13).* Line L11 finds the runs $R_i[p \ldots p'-1]$ and $S_i[q \ldots q'-1]$ of the value $u$. Since the lists are sorted, the tuples with value $u$ at positions at least $p$ and $q$ are exactly these runs. So the open pairs with value $u$ are exactly the pairs of the product of the runs, and line L12 outputs each of them once. Line L13 makes them done. An open pair with another value has both tuples after the runs, because the sort puts values above $u$ after them and values below $u$ do not occur at or after positions $p$ and $q$. So it stays open. A pair made of a tuple of a run and a tuple after the other run would have two different values, so it is not a matching pair. No pair becomes split. $\square$

**Lemma 3.** MERGE-JOIN$(R_i, S_i)$ stops and outputs each matching pair of $R_i$ and $S_i$ exactly once.

*Proof.* Each iteration makes $p + q$ larger, and $p + q \le |R_i| + |S_i|$, so the loop stops. Then $p = |R_i|$ or $q = |S_i|$, so no pair is open. By Lemma 2, no pair is split. So every matching pair is done and is output exactly once, and nothing else is output. $\square$

## The merge join over all parts

**Theorem 4.** If $R$ and $S$ are co-partitioned, that is, they have the same number of parts, each part is sorted by the join value and each join value occurs in at most one part index, then the union of MERGE-JOIN$(R_i, S_i)$ over all $i$ is $R \bowtie S$.

*Proof.* Each tuple is in exactly one part. Take a matching pair $(r, s)$ with join value $b$. If $r \in R_i$ and $s \in S_j$, then $b$ occurs in part $i$ and in part $j$, so $i = j$ by the condition. So every matching pair lies inside one pair of parts $(R_i, S_i)$, and by Lemma 3 the task for part $i$ outputs it exactly once. A task for another part never sees $r$. So each matching pair is output exactly once over all tasks. $\blacksquare$

The condition holds for the outputs of two earlier MapReduce jobs that use the same number of reducers and the same partitioner on the join value, because reducer $j$ of each job gets exactly the keys with $h(b) \bmod k = j$ and writes them in sorted order. If the condition fails, a matching pair can lie in two different part indices and is lost, which is why the program checks the condition before it joins.
