---
title: Polyphase merge sort sorts in l phases
proves: [correctness]
status: full
---

We use the line numbers of the pseudocode. Let $P = T - 1 \ge 2$. A *distribution* is a vector of run counts for the $P$ input tapes. Define the perfect distributions by $a^{(0)} = (1, 0, \ldots, 0)$ and

$$a^{(\ell+1)} = \big(a_1 + a_2,\ a_1 + a_3,\ \ldots,\ a_1 + a_P,\ a_1\big) \quad\text{for } a^{(\ell)} = (a_1, \ldots, a_P).$$

Write $t_\ell$ for the sum of the entries of $a^{(\ell)}$.

**Lemma 1 (shape).** For each $\ell \ge 0$, $a^{(\ell)}$ is non-increasing, and for $\ell \ge 1$ all its entries are at least 1. The totals grow strictly: $t_{\ell+1} > t_\ell$.

*Proof.* $a^{(0)}$ is non-increasing. If $a_1 \ge \cdots \ge a_P \ge 0$, then $a_1 + a_2 \ge \cdots \ge a_1 + a_P \ge a_1$, so $a^{(\ell+1)}$ is non-increasing, and each entry is at least $a_1 \ge 1$. Also $t_{\ell+1} = t_\ell + (P - 1)a_1 > t_\ell$, because $P \ge 2$ and $a_1 \ge 1$. $\blacksquare$

So line L2 finds a level $\ell$, and $t_\ell \ge S$. Line L4 gives each tape at most $a_d$ real runs, because it picks the tape with the largest deficit, and the total deficit $t_\ell - S$ before the last real run is at least 1. Line L5 fills each tape to exactly $a_d$ runs. A dummy run is an empty run.

**Lemma 2 (one phase).** Suppose that before line L8 the output tape is empty and the $P$ input tapes hold the counts of $a^{(j)}$, $j \ge 1$, in some order. Then after line L11 the new output tape is empty and the $P$ input tapes hold the counts of $a^{(j-1)}$, in some order.

*Proof.* Let $a^{(j-1)} = (b_1, \ldots, b_P)$, so the input tapes hold $b_1 + b_2, \ldots, b_1 + b_P, b_1$. The smallest of these is $k = b_1$, by Lemma 1. Lines L9 and L10 take $b_1$ runs from each input tape and write $b_1$ runs to the output tape. The input tapes now hold $b_2, \ldots, b_P, 0$, and the old output tape holds $b_1$. The tape that held $b_1$ runs is empty. If $j - 1 \ge 1$, all $b_i \ge 1$, so it is the only empty tape, and line L11 picks it. If $j - 1 = 0$, then $b = (1, 0, \ldots, 0)$, all input tapes are empty, line L11 picks one of them, and the counts are $b_1 = 1$ on the old output tape and 0 elsewhere. In both cases the counts are those of $a^{(j-1)}$. $\blacksquare$

**Lemma 3 (contents).** At each test of line L7, each run on a tape is sorted, and the multiset union of all runs on the tapes is the multiset of the items of $F$.

*Proof.* Line L1 makes sorted runs whose union is $F$, and dummy runs are empty. Line L10 removes one run from each input tape and appends their merge. The merge of sorted runs is sorted, and it holds exactly the items of the runs it merged. $\blacksquare$

**Theorem.** If $S \ge 2$, the loop of line L7 runs exactly $\ell$ times, and line L12 returns the items of $F$ in non-decreasing order.

*Proof.* Before the first phase, the input tapes hold $a^{(\ell)}$ and the output tape is empty. By Lemma 2 and induction, after $q$ phases the tapes hold the counts of $a^{(\ell - q)}$, with total $t_{\ell - q}$. By Lemma 1, $t_{\ell-q} > 1$ for $q < \ell$, and $t_0 = 1$. So the test of line L7 fails for the first time after $\ell$ phases, when exactly one run is left. By Lemma 3, this run is sorted and holds all items of $F$. $\blacksquare$

The sort is not stable. Take $F = (5_a, 5_b, 5_c)$, three equal keys, with $M = 1$ and $T = 3$. The distribution is $(2, 1)$: tape 1 holds $5_a, 5_b$ and tape 2 holds $5_c$. Phase 1 merges $5_a$ and $5_c$ onto tape 3. Phase 2 merges $5_b$ from tape 1 with $5_a 5_c$ from tape 3, and the merge takes tape 1 first on equal keys, so the output is $5_b, 5_a, 5_c$.
