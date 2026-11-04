---
title: The k-way merge outputs the stable sort of its runs
proves: [correctness]
status: full
---

We use the line numbers of the pseudocode. Let $S_1, \ldots, S_k$ be the runs at the start, each sorted in non-decreasing order, and let $n$ be the total number of items. Label each item with its run number $i$ and its position $j$ in the run. The *stable order* of the items is the order by key, then by $i$, then by $j$. The stable sort of the items is the list of all items in the stable order. During the merge, write $S_i$ for the part of run $i$ that is not yet removed. Each $S_i$ is a suffix of the original run, so it is sorted.

**Invariant.** At each test of line L5:

1. $O$ lists the removed items in the stable order.
2. $H$ holds exactly one pair for each $i$ with $S_i$ not empty, and this pair is $(h_i, i)$, where $h_i$ is the head of $S_i$.
3. Each item of $O$ comes before each item that is still in some $S_i$, in the stable order.

*Initialization.* Lines L2 and L3 add $(h_i, i)$ for each run that is not empty, and no other pair. Line L4 makes $O$ empty. So parts 1 and 3 are true with no removed items, and part 2 is true.

*Maintenance.* Assume the invariant and that $H$ is not empty. Let $(x, i)$ be the minimum of $H$ at line L6, in the order by key, then by run number. We show that $x$, which is $h_i$, is the first remaining item in the stable order. Take any remaining item $y$ in some $S_a$. Because $S_a$ is sorted, its head $h_a$ satisfies $h_a \le y$, and $(h_a, a)$ is in $H$ by part 2. If $y$ has a smaller key than $x$, then $h_a < x$, and $(h_a, a)$ is smaller than $(x, i)$, which is false. So the key of $y$ is at least the key of $x$. If the keys are equal and $a \ne i$, then $h_a \le y = x$, so $h_a = x$, and the minimum rule gives $i < a$. If $a = i$ and $y \ne x$, then $y$ comes after the head $x$ in run $i$, so it has a larger position. In each case $x$ comes before $y$ in the stable order.

Line L7 appends $x$ to $O$ and removes it from $S_i$. By part 3 and the result above, $O$ is still in the stable order, and $x$ comes before each remaining item, so parts 1 and 3 stay true. Only $S_i$ changed. If $S_i$ is not empty, line L8 puts the pair of its new head in the place of $(x, i)$. If $S_i$ is empty, line L9 removes $(x, i)$. In both cases part 2 stays true.

*Termination.* Each iteration removes exactly one item from the runs, and the runs hold $n$ items at the start. By part 2, $H$ is empty exactly when all runs are empty. So the loop runs exactly $n$ times.

**Theorem.** K-WAY-MERGE returns the stable sort of the items of $S_1, \ldots, S_k$.

*Proof.* When the loop stops, all $n$ items are removed, and by part 1, $O$ lists them in the stable order. Line L10 returns $O$. A list in the stable order is non-decreasing by key, and equal keys come in the order of their runs and of their positions. $\blacksquare$
