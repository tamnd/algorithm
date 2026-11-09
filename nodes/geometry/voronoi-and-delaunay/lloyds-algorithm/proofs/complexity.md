---
title: Cost of one step of Lloyd's algorithm
proves: [complexity]
status: full
---

**Claim.** In the real RAM model, for $n$ distinct sites in a box, one step of LLOYD takes $O(n \log n)$ time and $O(n)$ space when the Voronoi diagram is built by an $O(n \log n)$ algorithm and then clipped to the box. The code on this page builds each cell by clipping the box with $n - 1$ half-planes and takes $O(n^3)$ time per step in the worst case and $O(n)$ space. So $k$ steps take $O(k n \log n)$ time, and $O(k n^3)$ with the code.

**Proof.** *With a Voronoi algorithm.* [Fortune's algorithm](/fortunes-algorithm/) builds the diagram in $O(n \log n)$ time; it has $O(n)$ vertices and edges by the [Voronoi complexity theorem](/voronoi-complexity-theorem/). Clipping a convex cell with $s_i$ edges to the box takes $O(s_i)$ time, because the box has $4$ sides, and the clipped cell has at most $s_i + 4$ edges. Every Voronoi edge is a side of two cells, so $\sum_i s_i = O(n)$. Lines L3 and L4 compute each centroid from the vertices of its cell in $O(s_i + 4)$ time. So one step takes $O(n \log n) + O(n) = O(n \log n)$ time and $O(n)$ space.

*With the code.* Each cell starts as the box, with $4$ vertices, and is clipped by $n - 1$ half-planes. Each clip adds at most one vertex, so the polygon has at most $n + 3$ vertices, and each clip takes time linear in its size, so a cell takes $O(n^2)$ time and the $n$ cells take $O(n^3)$ time. Only one cell is being clipped at a time and the finished cells have $O(n)$ vertices in total, as above, so the space is $O(n)$. $\blacksquare$

*Remark.* The number of steps needed for a given accuracy is not bounded here; it depends on the input and on the density, and the convergence can be slow. In exact rational arithmetic the size of the numbers grows from step to step; the real RAM model does not count this, but a program that runs many steps uses floating point.
