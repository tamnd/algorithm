---
title: External merge sort sorts the file stably and does at most the stated number of I/Os
proves: [correctness]
status: full
---

We use the line numbers of the pseudocode. A *stable sort* of a sequence $S$ is the sequence of its items in non-decreasing order, where equal items keep their order in $S$. We write $\operatorname{st}(S)$ for it. We assume $M \ge 3B$, so $k = M/B - 1 \ge 2$.

**Lemma 1 (merge).** Let $S_1, \ldots, S_g$ be sequences, and let $S = S_1 S_2 \cdots S_g$ be their concatenation. A merge of the runs $\operatorname{st}(S_1), \ldots, \operatorname{st}(S_g)$ that outputs the smallest head, and on equal heads the head of the run with the smallest index, outputs $\operatorname{st}(S)$.

*Proof.* Each run is sorted, so the head of run $j$ is its smallest item that is not yet output. So each output item is a minimum of the items that are not yet output, and the output is non-decreasing. Each item is output one time, so the output is a permutation of $S$ in non-decreasing order. Take two equal items $x$ and $y$, where $x$ comes before $y$ in $S$. If both are in the same part $S_j$, then $x$ comes before $y$ in $\operatorname{st}(S_j)$, and the merge outputs the items of one run in their order. If $x$ is in $S_i$ and $y$ is in $S_j$ with $i < j$, consider the step that outputs $y$. At this step $y$ is the head of run $j$. If $x$ were not yet output, the head $h$ of run $i$ would satisfy $h \le x = y$. If $h < y$, the merge would not output $y$. If $h = y$, the tie rule would output $h$ first. So $x$ is output before $y$. Both cases give the order of $S$. $\square$

**Invariant.** At each test of line L6, there are consecutive parts $F_1, \ldots, F_r$ of $F$, with $F = F_1 \cdots F_r$, such that $R = [\operatorname{st}(F_1), \ldots, \operatorname{st}(F_r)]$. If $N \ge 1$, each part is not empty.

*Initialization.* Lines L3 to L5 cut $F$ into pieces of $M$ consecutive items from left to right, the last piece possibly shorter, and append the stable sort of each piece to $R$ in this order. So the invariant is true with the pieces as the parts.

*Maintenance.* Line L8 cuts $R$ into groups of $k$ consecutive runs, from left to right. A group of runs $\operatorname{st}(F_a), \ldots, \operatorname{st}(F_b)$ becomes one run. If $a = b$, line L9 keeps it, and it is $\operatorname{st}(F_a)$. If $a < b$, Lemma 1 shows that line L10 makes $\operatorname{st}(F_a \cdots F_b)$. The new parts $F_a \cdots F_b$ are consecutive, in order, and their concatenation is $F$. So after line L11 the invariant is true again.

**Termination.** If $|R| = r \ge 2$ at line L6, the pass makes $\lceil r/k \rceil$ runs. Because $k \ge 2$, $\lceil r/k \rceil \le \lceil r/2 \rceil \le r - 1$. So $|R|$ drops by at least 1 in each pass, and the loop stops after at most $r - 1$ passes.

**Theorem.** EXTERNAL-MERGE-SORT returns $\operatorname{st}(F)$.

*Proof.* If $N = 0$, line L3 does nothing, $R$ is empty, and line L12 returns an empty file. If $N \ge 1$, the loop stops with $|R| = 1$, and by the invariant the one run is $\operatorname{st}(F_1)$ with $F_1 = F$. $\blacksquare$

**The I/O count.** Let $n = \lceil N/B \rceil$ and $r_0 = \lceil N/M \rceil$, and assume that $B$ divides $M$ and $N \ge 1$. Run formation reads and writes each piece. All pieces except the last have $M$ items, a multiple of $B$, so the pieces use $n$ blocks in total, and run formation costs $2n$ I/Os. By the invariant, in each pass all runs except the last hold a union of full pieces, so their lengths are multiples of $B$, and the runs use $n$ blocks in total. A pass reads and writes each run of a group with two or more runs, and does no I/O for a group of one run, so a pass costs at most $2n$ I/Os. For integers $x \ge 1$ and $k \ge 1$, $\lceil \lceil x/k \rceil / k \rceil = \lceil x/k^2 \rceil$. By induction, after pass $i$ there are $\lceil r_0/k^i \rceil$ runs. This is 1 exactly when $k^i \ge r_0$, so the number of passes is $\lceil \log_k r_0 \rceil$. The total is at most $2n(1 + \lceil \log_k r_0 \rceil)$. $\blacksquare$
