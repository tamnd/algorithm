---
title: Linear worst-case bounds for walking in a triangulation
proves: [time.build, time.query, space.extra]
status: full
---

**Setting.** A triangulation of a convex polygon $K$ with $n$ vertices and $T$ triangles, edge to edge, as in [the correctness proof](../correctness/). Costs are on the real RAM. The walks are the straight walk and, in a triangulation whose interior edges are all locally Delaunay, the visibility walk.

**Claim.** (a) $T \le 2n - 5$, and the triangulation has at most $3n - 6$ edges. (b) The neighbor table is built in $O(n)$ time and takes $O(n)$ space. (c) A query takes $O(n)$ time in the worst case, and this is tight. (d) Apart from the table, a walk uses $O(1)$ space, or $O(n)$ if it records its path as the code does.

**Step 1 (counting, a).** The vertices and edges form a connected plane graph. Let $h \ge 3$ be the number of edges on the boundary of $K$. Every bounded face is a triangle and the outer face has $h$ edges, so $2E = 3T + h$. By Euler's formula, $n - E + (T + 1) = 2$. Eliminating $E$ gives $T = 2n - 2 - h \le 2n - 5$ and $E = 3n - 3 - h \le 3n - 6$.

**Step 2 (the table, b).** The table has one entry per directed edge of a triangle, so $3T$ entries, each built in $O(1)$ time with an array indexed by triangle and edge, or with a hash table keyed by the pair of end points in $O(1)$ expected time, as in the code. By Step 1 this is $O(n)$ time and space. The neighbor across a directed edge $u \to w$ is the triangle that owns $w \to u$.

**Step 3 (query time, c).** Each step of a walk does $O(1)$ work: at most three orientation tests for line L5 or L8, one more for line L6, and one table lookup. By Step 3 of the correctness proof, the straight walk visits each triangle at most once, so it takes at most $T$ steps. By Step 5 of the correctness proof, the visibility walk in a locally Delaunay triangulation never visits a triangle twice, so it also takes at most $T$ steps. Line L1 or the final classification costs $O(1)$. By Step 1, a query takes $O(n)$ time in the worst case. For tightness, take the vertices $(i, 0)$ and $(i, 1)$ for $0 \le i \le m$, and the triangles $(i, 0)(i + 1, 0)(i, 1)$ and $(i + 1, 0)(i + 1, 1)(i, 1)$. The four corners of each unit square lie on one circle, so all edges are locally Delaunay. The straight walk from the triangle $(0,0)(1,0)(0,1)$, with centroid $(1/3, 1/3)$, to $q = (m, 1)$ follows a segment that crosses each vertical edge $(i, 0)(i, 1)$, for $1 \le i \le m - 1$, at a height strictly between $1/3$ and $1$, so in its relative interior. Each crossing is one step, so the walk takes at least $m - 1 = \Theta(n)$ steps, with $n = 2m + 2$.

**Step 4 (space, d).** A walk keeps the current triangle, the current edge and, for the straight walk, the scaled points $3s$ and $3q$, so it uses $O(1)$ space beyond the table. The code also stores the visited triangles for testing, at most $T + 1$ of them by Step 3, so $O(n)$.
