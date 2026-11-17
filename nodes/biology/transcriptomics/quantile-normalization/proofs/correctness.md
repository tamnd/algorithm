---
title: Quantile normalization gives every sample the target distribution and keeps the order within each sample
proves: [correctness]
status: full
---

We prove that quantile normalization does what its name says. Without ties, every column of the output has exactly the target values (Theorem 2). With or without ties, it keeps the order of the values inside each column (Lemma 3) and gives every column the same sum (Lemma 4). Without ties, it is idempotent in exact arithmetic (Lemma 5). That the samples should have the same distribution is a modelling assumption. It is not proved here, and the page states when it fails.

**Setting.** A matrix $x$ with $n$ rows (genes) and $m$ columns (samples). For each column $j$, let $x_{(1)j} \le \dots \le x_{(n)j}$ be its sorted values. The target is $t_i = \frac1m\sum_{j=1}^m x_{(i)j}$ for $i = 1, \dots, n$. In column $j$, the entries split into tie blocks: maximal sets of equal values. A block that holds the sorted positions $a, \dots, b$ gets the value $\bar t_{[a,b]} = \frac{1}{b-a+1}\sum_{i=a}^b t_i$ in every entry. A block of one entry at position $a$ gets $t_a$.

**Lemma 1 (the target is sorted).** $t_1 \le t_2 \le \dots \le t_n$.

*Proof.* For each $j$, $x_{(i)j} \le x_{(i+1)j}$. Summing over $j$ and dividing by $m$ gives $t_i \le t_{i+1}$. $\square$

**Theorem 2 (the same distribution).** If column $j$ has no ties, the multiset of its output values is $\{t_1, \dots, t_n\}$, and the entry at sorted position $i$ gets $t_i$. So every column without ties has the same sorted values $t_1 \le \dots \le t_n$, and the same empirical distribution.

*Proof.* Without ties every block has one entry, so the entry at position $i$ gets $t_i$, and the positions $1, \dots, n$ each occur once. $\square$

Lines L1 and L2 compute $t$, and lines L3 to L5 give each block its value. The code sorts each column with a stable sort and then finds the blocks as runs of equal values, so the result does not depend on the input order of tied entries.

**Lemma 3 (order within a column).** In each column $j$, if $x_{gj} < x_{hj}$ then $y_{gj} \le y_{hj}$, and if $x_{gj} = x_{hj}$ then $y_{gj} = y_{hj}$.

*Proof.* Equal values are in the same block and get the same value. If $x_{gj} < x_{hj}$, the block of $g$ holds positions $[a, b]$ and the block of $h$ holds $[c, d]$ with $b < c$. A mean of a sorted sequence over a range is at most its last term, and at least its first term. So, by Lemma 1, $\bar t_{[a,b]} \le t_b \le t_c \le \bar t_{[c,d]}$. $\square$

Strict order can become equality, when the target has two equal neighbours $t_b = t_c$. Order is never reversed.

**Lemma 4 (equal sums).** Every output column has the sum $\sum_{i=1}^n t_i = \frac1m\sum_{g,j} x_{gj}$, with or without ties.

*Proof.* A block over positions $[a, b]$ has $b - a + 1$ entries, each equal to $\bar t_{[a,b]}$, so it contributes $\sum_{i=a}^b t_i$. The blocks of a column cover the positions $1, \dots, n$ once, so the column sum is $\sum_i t_i$. Then $\sum_i t_i = \frac1m\sum_j\sum_i x_{(i)j} = \frac1m\sum_{g,j}x_{gj}$, since sorting a column does not change its sum. $\square$

So all columns get the mean of the original column sums, and so the same mean value.

**Lemma 5 (idempotence).** Suppose no column of $x$ has ties and the target has no ties, $t_1 < \dots < t_n$. Then normalizing the output $y$ again gives $y$.

*Proof.* By Theorem 2, every column of $y$ has the sorted values $t_1 < \dots < t_n$, so the new target is $t'_i = \frac1m\sum_j t_i = t_i$. The columns of $y$ have no ties, so each entry at sorted position $i$ gets $t'_i = t_i$, which is its present value. $\square$

In floating point, $\frac1m\sum_j t_i$ can differ from $t_i$ in the last bits, so the tests check idempotence with a relative tolerance.

**Equivariance.** Permuting the rows of $x$ permutes the rows of the output in the same way, and permuting the columns permutes the output columns. Both follow because $t$ depends only on the multisets of the columns and on the set of columns, and each entry depends only on its rank in its column.

**Complexity.** Sorting the $m$ columns takes $\Theta(mn\log n)$ time. Computing $t$ and the prefix sums of $t$ takes $\Theta(mn)$, and with the prefix sums each block mean costs $O(1)$, so the assignment takes $\Theta(mn)$ after the sorts. The extra space is $\Theta(mn)$ for the output and $\Theta(n)$ for the sorted order of one column.

**What the tests check.** The test file checks Theorem 2 by exact equality of the sorted columns with $t$, Lemma 3 on every pair of entries, Lemma 4, Lemma 5 with a tolerance, the equivariance, and the tie rule against a brute force that averages $t$ over the positions of each value.
