---
title: Parallel radix sort is correct and stable
proves: [correctness]
status: full
---

Fix a pass $t$ and write $d(x) = \operatorname{digit}_t(x)$. Give the items of $A$ their input positions $0, \ldots, n-1$. Block $j$ holds the positions $\lfloor jn/p \rfloor$ to $\lfloor (j+1)n/p \rfloor - 1$, so the blocks cut the positions into consecutive ranges in increasing order of $j$.

## Lemma 1. One pass is a stable counting sort on digit t

Define the order by digit $t$: item $u$ comes before item $v$ if $d(u) < d(v)$, or $d(u) = d(v)$ and $u$ has the smaller position. After the pass, the item with $q$ items before it in this order is at position $q$ of $B$.

*Proof.* Let $x$ be an item in block $j$ with digit $d$. The items before $x$ in the order by digit $t$ are of three kinds:

1. the items with a digit less than $d$, in any block; there are $\sum_{d' < d} \sum_{j'} C[d'][j']$ of them;
2. the items with digit $d$ in a block $j' < j$, since these have smaller positions; there are $\sum_{j' < j} C[d][j']$ of them;
3. the items with digit $d$ in block $j$ that are to the left of $x$.

By the order of the prefix sum on line L4, the starting value of $O[d][j]$ is the sum of the counts of the first two kinds. Processor $j$ visits the keys of its block from left to right, and adds 1 to $O[d][j]$ after each key with digit $d$, so when it reaches $x$ the counter has grown by the number of items of the third kind. So $x$ is written at position $q$, where $q$ is the number of items before $x$.

The map from items to $q$ is a bijection onto $0, \ldots, n-1$, because the order by digit $t$ is a strict total order on the $n$ items. So every cell of $B$ is written exactly once. $\square$

## Lemma 2. Exclusive access

*Proof.* On line L3, processor $j$ reads only its own block and writes only the counts $C[\cdot][j]$. The prefix sum on line L4 can be done with exclusive reads and writes, as shown for the EREW PRAM on the page on [prefix sums](/all-prefix-sums/). On lines L5 to L7, processor $j$ reads its block and its own counters $O[\cdot][j]$, and by Lemma 1 the cells of $B$ it writes are distinct from each other and from those of every other processor. So no cell is read or written by two processors in the same step. $\square$

## Theorem. PAR-RADIX-SORT sorts stably

After the passes $0, \ldots, t$, the items are in the order of their low $t + 1$ digits, read as a number, with ties in input order. So after all $\lceil w/b \rceil$ passes they are sorted, stably.

*Proof.* By induction on $t$. For $t = 0$ this is Lemma 1 with the input order. Assume it after pass $t - 1$, and take two items $u$ and $v$ with $u$ before $v$ after pass $t$. By Lemma 1, either $d_t(u) < d_t(v)$, and then the low $t + 1$ digits of $u$ form a smaller number, or $d_t(u) = d_t(v)$ and $u$ was before $v$ after pass $t - 1$. In the second case, by induction, the low $t$ digits of $u$ form a number at most that of $v$, with $u$ earlier in the input if they are equal. In both cases $u$ comes before $v$ in the order of the claim. A key of $w$ bits has all its bits in the low $\lceil w/b \rceil$ digits, so the last pass leaves the keys sorted, with equal keys in input order. $\square$
