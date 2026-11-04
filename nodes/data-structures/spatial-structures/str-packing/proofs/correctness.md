---
title: STR packing builds an R-tree of minimal height, and its search reports exactly the rectangles that meet the query
proves: [correctness, termination]
status: full
---

Let the input be $n \ge 1$ entries $(r, x)$ and $M \ge 2$. Write $E_j$ for the list of entries at the start of pass $j$, with $E_0$ the input and $k_j = |E_j|$.

**One pass.** Lines L3 to L5 sort $E_j$ and cut it into consecutive pieces: first slices, then runs of at most $M$ inside each slice. So the new nodes partition $E_j$: each entry is in exactly one node, and each node has between 1 and $M$ entries. Each slice except the last has exactly $S M$ entries, a multiple of $M$, so all its runs have $M$ entries. So all nodes of the pass are full except perhaps the last one of the last slice, and the number of nodes is $\lceil k_j / M \rceil$. Line L6 makes, for each new node $u$, the entry $(\operatorname{MBR}(u), u)$, so the rectangle of each internal entry is the MBR of its child.

**Termination.** If $k_j \ge 2$, then $k_{j+1} = \lceil k_j / M \rceil \le \lceil k_j / 2 \rceil < k_j$. If $k_j = 1$, the pass makes one node. So the sizes drop until a pass makes one node, and the loop stops; this node is the root.

**The tree is an R-tree.** The nodes of pass 0 are leaves; their entries are the input. The nodes of pass $j \ge 1$ have as children exactly the nodes of pass $j - 1$, each once, by the partition property. So by induction, every node of pass $j$ has all its leaves at depth $j$ below it, and all leaves are at the same depth from the root, the number of passes minus one. Every node has between 1 and $M$ entries, and each internal rectangle is the MBR of its child. Every input entry is in exactly one leaf, so the tree stores the input once.

**Height.** The number of passes $h + 1$ is the least $t$ with $\lceil \cdots \lceil n/M \rceil \cdots / M \rceil = 1$ after $t$ divisions, and since $\lceil \lceil a/M \rceil / M \rceil = \lceil a / M^2 \rceil$ for integers, this is the least $t \ge 1$ with $n \le M^t$. So the height $h$ is the least $h \ge 0$ with $n \le M^{h+1}$. No tree of nodes with at most $M$ entries and height $h'$ holds more than $M^{h'+1}$ entries, so no R-tree for the input has a smaller height.

**Search.** By induction on the height, each input rectangle in the subtree of an internal entry $(r, u)$ lies inside $r$, since $r = \operatorname{MBR}(u)$ contains the rectangle of each entry of $u$. Let $(s, x)$ be an input entry with $s \cap q \ne \emptyset$. Every rectangle on the path from the root to its leaf contains $s$, so it meets $q$, and lines L7 and L9 follow the path; line L8 reports $x$. Conversely, line L8 reports only leaf entries whose rectangle meets $q$, and each node is reached by its one path, so each entry is reported once. The tree is finite, so the search stops. $\blacksquare$
