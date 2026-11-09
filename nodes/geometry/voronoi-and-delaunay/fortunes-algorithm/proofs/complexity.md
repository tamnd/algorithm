---
title: Fortune's sweep runs in O(n log n) worst-case time and O(n) space
proves: [complexity]
status: full
---

**Claim.** In the real RAM model, for $n$ sites in general position (G1) to (G3) of the correctness proof, Fortune's sweep with a binary heap as the event queue and a balanced binary search tree over the arcs takes $O(n \log n)$ time in the worst case and $O(n)$ space. The code on this page replaces the tree by a linked list and takes $O(n^2)$ time in the worst case.

**Notation.** $A$ is the largest number of arcs at one time, and $E$ is the number of events pushed into the queue.

**Lemma 1.** $A \le 2n - 1$, at most $2n - 5$ circle events are processed for $n \ge 3$, and $E \le 7n$.

*Proof.* The first site makes one arc. Each site event adds two arcs and each processed circle event removes one, so there are at most $1 + 2(n - 1) = 2n - 1$ arcs. By Lemma 9 of the correctness proof each processed circle event records a different Voronoi vertex, and there are at most $2n - 5$ of them by the [Voronoi complexity theorem](/voronoi-complexity-theorem/). The queue starts with $n - 1$ site events; each site event pushes at most two circle events, and each processed circle event pushes at most two; so $E \le (n - 1) + 2(n - 1) + 2(2n - 5) < 7n$. $\square$

**Proof of the claim.** Each arc is a node of the search tree, in left-to-right order. To find the arc above a new site $s$ (line L5), the search compares $s_x$ with the breakpoint stored between two neighbouring arcs; the breakpoint at the current height is a root of a quadratic, and the comparison is the exact sign test of the code, in $O(1)$ time. The tree order of the breakpoints is the left-to-right order at every height between events, by Lemma 7 of the correctness proof, so the search takes $O(\log A) = O(\log n)$ time. Insertions and deletions of arcs (lines L7 and L12) take $O(\log n)$ time, and the neighbours of an arc are kept as links, in $O(1)$ time. Each push and pop of the heap takes $O(\log E) = O(\log n)$ time, and an invalid event is marked in $O(1)$ time and skipped when popped. Line L14 visits each trace once, and there are at most $2n + 2(2n - 5)$ traces. So the time is $O(n \log n)$, and the space is $O(A + E + n) = O(n)$.

In the code, line L5 walks the list from the left end, which takes $O(A) = O(n)$ time per site, so $O(n^2)$ time in all; all other steps have the bounds above. $\blacksquare$

*Remark.* The $O(n \log n)$ bound is optimal: sorting reduces to the construction of the Voronoi diagram, so the [lower bound](/voronoi-construction-lower-bound/) of $\Omega(n \log n)$ holds in the algebraic decision tree model.
