---
title: BST search returns the node with the key, or NIL when there is none
proves: [correctness, termination]
status: full
---

Let $T$ be a binary search tree with root $r$, with the strict [binary search tree property](/binary-search-tree-property/), and let $k$ be a key. For a node $x$ (or NIL) write $\mathrm{sub}(x)$ for the set of nodes of the subtree rooted at $x$, with $\mathrm{sub}(\mathrm{NIL}) = \emptyset$. The keys of $T$ are distinct, so at most one node $t$ has $t.key = k$.

**Claim.** TREE-SEARCH$(r, k)$ stops after at most $h + 1$ runs of the loop, where $h$ is the height of $T$. It returns $t$ if $t$ exists, and NIL else. It does not change $T$.

**Invariant (I).** At the test of line L1: if $t$ exists, then $t \in \mathrm{sub}(x)$. Also, $x$ is NIL or a node of depth $j$, where $j$ is the number of runs of the loop done so far.

**Initialization.** Before the first test, $x = r$, $j = 0$, and $\mathrm{sub}(r)$ is the whole tree, so (I) holds.

**Maintenance.** Suppose (I) holds and $x \ne$ NIL. If $k = x.key$, line L2 returns and the loop ends. Else assume $k < x.key$, so line L3 sets $x$ to $x' = x.left$. Each node $y$ in the right subtree of $x$ has $y.key > x.key > k$ by the BST property, and $x.key \ne k$. So $t$, if it exists, is in $\mathrm{sub}(x)$ but is not $x$ and not in the right subtree; hence $t \in \mathrm{sub}(x')$. The depth of $x'$ is $j + 1$. The case $k > x.key$ (line L4) is the same with left and right swapped, using $y.key < x.key < k$ for each $y$ in the left subtree. So (I) holds after the step.

**Termination.** By (I), after $j$ runs $x$ is NIL or has depth $j \le h$. So after at most $h + 1$ runs, $x$ is NIL, or the loop has returned. The quantity $h + 1 - j$ is a non-negative integer that drops by exactly 1 in each run.

**The answer.** If line L2 returns $x$, then $x.key = k$, so $x = t$. If the loop ends with $x = $ NIL, line L5 returns NIL; by (I) $t \in \mathrm{sub}(\mathrm{NIL}) = \emptyset$ if $t$ exists, so $t$ does not exist and NIL is right. The algorithm writes only the local variable $x$, so $T$ does not change. $\blacksquare$

**The cost.** The proof also shows that the number of runs is $d + 1$, where $d$ is the depth of the last node visited, because each run visits one node at depth $j$ and the depths are $0, 1, \ldots, d$.
