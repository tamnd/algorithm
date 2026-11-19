---
title: The lazy grid search of cube pruning is exact for monotone scores and a heuristic with a language model
proves: [correctness]
status: full
---

A chart cell gets hyperedges $e = 1, \ldots, E$. Hyperedge $e$ has $r_e$ child lists $L_{e,1}, \ldots, L_{e,r_e}$, each sorted best first. A *grid point* of $e$ is a vector $j = (j_1, \ldots, j_{r_e})$ with $0 \le j_x < |L_{e,x}|$, and it has a score $\mathrm{sc}_e(j)$. Write $j + 1_x$ for $j$ with coordinate $x$ raised by one. CUBE-PRUNE pushes the corner $(0, \ldots, 0)$ of each hyperedge (line L2), then pops at most $k$ grid points from a max-heap (lines L3 to L5), and after each pop pushes the neighbours $j + 1_x$ that exist and were never pushed (lines L6 to L8). A grid point is pushed at most once, because of the set of pushed points.

The score is *monotone* if $\mathrm{sc}_e(j) \ge \mathrm{sc}_e(j + 1_x)$ for every $e$, $j$ and $x$ with $j + 1_x$ in the grid. Without a language model, $\mathrm{sc}_e(j)$ is the rule score plus the sum of the child scores, and each child list is sorted, so the score is monotone.

**Lemma 1 (every grid point has a pushed ancestor).** At the start of each pass of line L3, every grid point $j$ of every hyperedge that was not popped yet has a point $j' \le j$ (coordinate by coordinate) that is in the heap.

*Proof.* Take the path from the corner to $j$ that raises the coordinates one at a time. The corner was pushed at line L2. Walk along the path to the first point that was not popped. If it is the corner, it is in the heap. Otherwise its predecessor on the path was popped, and when it was popped, line L8 pushed all its neighbours $+1_x$ that were not pushed before. So the point was pushed at some time, and it was not popped, so it is still in the heap. $\square$

**Theorem 1 (exact for monotone scores).** If the score is monotone, the points popped by CUBE-PRUNE are, in order, a list of the $\min(k, N)$ highest grid points of all hyperedges, with $N$ the total number of grid points. Line L9 does not change their order.

*Proof.* Consider a pop at line L4, and let $j$ be any grid point that was not popped before it. By Lemma 1 the heap holds some $j' \le j$, and by monotonicity along the path from $j'$ to $j$, $\mathrm{sc}(j') \ge \mathrm{sc}(j)$. The popped point has the largest score in the heap, so its score is at least $\mathrm{sc}(j)$. So each pop takes a highest point among those not popped yet. By induction, the first $q$ pops are $q$ highest points in decreasing order of score. The loop runs until $k$ pops or until the heap is empty, and by Lemma 1 the heap is empty only when every point was popped. $\square$

This is the lazy enumeration of Huang and Chiang (2005) for one hyperedge, and its merge over the hyperedges of one cell.

**Theorem 2 (always true).** For any scores, (a) each popped item is a real grid point with its true score; (b) line L9 returns the popped items in decreasing order of score; (c) if $k \ge N$, every grid point is popped, so the result is the full sorted list; (d) the $q$-th best returned score is at most the $q$-th best grid score.

*Proof.* (a) Line L8 pushes the point with the score that COMBINE computes for it. (b) Line L9 sorts. (c) By Lemma 1, while a point is not popped the heap is not empty, so with $k \ge N$ the loop stops only when all points are popped. (d) The returned items are $\min(k, N)$ distinct grid points, and the $q$-th best of any set of distinct grid points is at most the $q$-th best of all of them. $\square$

**With a language model the score is not monotone.** COMBINE adds the bigram scores at the junctions between the target words of a rule and of its children. A child item that is worse on its own can make a much better junction, so $\mathrm{sc}(j + 1_x) > \mathrm{sc}(j)$ can happen. Then the proof of Theorem 1 breaks, because the ancestor in the heap can score lower than a point behind it. In the example of the page, the corner "he go" scores $-4.8$, and its neighbours score $-2.3$ and $-2.4$. With $k = 3$, the point "she goes" ($-2.9$) is never pushed, because it lies behind "they goes" ($-5.2$) and "she go" ($-5.3$), and the result holds "he go" at $-4.8$ in its place. So cube pruning with a language model is a heuristic. Theorem 2 still holds.

**Cost.** Each pop pushes at most $r$ points, with $r = \max_e r_e$. So the heap holds at most $E + k r$ items, and the $E$ first pushes, the $k$ pops and the other pushes cost $O((E + k r) \log(E + k r))$ heap work, plus $E + k r$ calls of COMBINE. Without the lazy search, all $N = \sum_e \prod_x |L_{e,x}|$ points would be scored; with child lists of size $k$, that is up to $E k^r$.
