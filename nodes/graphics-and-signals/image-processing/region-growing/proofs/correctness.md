---
title: The frontier lists make each step of SRG add the border pixel with the least difference from a current region mean
proves: [correctness]
status: full
---

Fix a gray image $g$ on a pixel grid with a neighborhood relation (4 or 8 neighbors), and disjoint nonempty seed sets $A_1, \ldots, A_R$. Write $A_i$ also for the current region $i$, $\mu_i = s_i / c_i$ for its current mean, and $T$ for the set of unlabeled pixels with a neighbor in some region. The step of the definition picks, among all pairs $(x, i)$ with $x \in T$ and $x$ adjacent to $A_i$, the pair with the least $\delta(x, i) = |g(x) - \mu_i|$, with ties broken by the key $(\delta, \text{row}, \text{column}, i)$, and adds $x$ to $A_i$.

**Invariant.** At the test of line L3, for every $i$: $s_i = \sum_{y \in A_i} g(y)$, $c_i = |A_i|$, and $F_i$ is exactly the set of unlabeled pixels with a neighbor in $A_i$.

*Proof.* After lines L1 and L2, the sums and counts are those of the seeds, and $F_i$ is the set of unlabeled neighbors of $A_i$. Suppose the invariant holds before a pass that adds $x$ to $A_i$. Line L6 labels $x$ and updates $s_i$ and $c_i$, so the first two parts still hold. For the lists, a pixel $z$ is unlabeled with a neighbor in the new $A_j$ in one of two ways. If $j \ne i$, region $j$ did not change, so $z$ was in $F_j$ before, unless $z = x$, which line L7 removes from every list. If $j = i$, either $z$ had a neighbor in the old $A_i$ and was in $F_i$, or its new neighbor is $x$, and line L8 adds it. Conversely, every pixel still in a list is unlabeled (only $x$ was labeled, and it was removed) and has a neighbor in the region of its list. $\square$

**Lemma (closest value in a sorted list).** Let $F$ be sorted by gray value and $\mu$ a number. Let $j$ be the first position with value at least $\mu$. The values closest to $\mu$ are at position $j - 1$ (the largest value below $\mu$) or at position $j$ (the smallest value at least $\mu$).

*Proof.* Every value at a position before $j - 1$ is at most the value at $j - 1$, which is below $\mu$, so it is at least as far from $\mu$. Every value after $j$ is at least the value at $j$, which is at least $\mu$, so it is at least as far. $\square$

Among the pixels of one gray value, the implementation takes the first in (row, column) order, which is the first of that value in a list sorted by (value, row, column). So line L4 returns, for each $i$, the least key $(\delta, \text{row}, \text{column})$ among the pairs $(x, i)$ with $x \in F_i$.

**Theorem.** Each pass of lines L4 to L8 performs the step of the definition, and the loop ends after $N - \sum_i |A_i|$ passes on a connected grid, with every pixel labeled. Every connected piece of the final region $i$ (under the same neighborhood) contains a pixel of $A_i$.

*Proof.* By the invariant, the pairs $(x, i)$ with $x \in F_i$ are exactly the pairs of the definition, with $\mu_i = s_i / c_i$ the current mean. By the lemma, line L4 finds the least key within each $F_i$, and line L5 takes the least over $i$, so the pair chosen has the least key overall, which is the pair of the definition. The loop continues while some $F_i$ is not empty, that is while $T \ne \emptyset$. Each pass labels one new pixel, so there are at most $N - \sum_i |A_i|$ passes. When $T = \emptyset$, no unlabeled pixel has a labeled neighbor. If some pixel were unlabeled, a path in the grid from it to a seed would contain an unlabeled pixel next to a labeled one, which would be in $T$. So on a connected grid all pixels are labeled, and the number of passes is exactly $N - \sum_i |A_i|$.

For the last claim, each pixel added to $A_i$ has a neighbor already in $A_i$ (it was in $F_i$). By induction on the order of addition, every pixel of the final $A_i$ is joined by a path inside $A_i$ to a pixel of the seed set $A_i$: a seed pixel trivially, and a later pixel through its earlier neighbor. A connected piece of the final region contains such a path, and so a seed pixel. $\square$

**Remark (the sorted-list version).** In the paper's implementation, the key of a pixel is computed against the mean at the moment it enters the list and is not changed later. The invariant then holds for the set of pixels in the list, but the key of a pixel can differ from its current $\delta$, so the step need not be the step of the definition. The second example on the page shows a case where the final result differs. The property that every connected piece of region $i$ contains a seed pixel of $A_i$ still holds, by the same induction, because a pixel joins a region only when it has a labeled neighbor in that region.
