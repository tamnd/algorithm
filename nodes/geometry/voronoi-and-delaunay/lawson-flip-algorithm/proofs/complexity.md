---
title: Lawson's flip algorithm runs in O(n^2) worst-case time and O(n) space
proves: [complexity]
status: full
---

**Claim.** In the real RAM model, with the triangulation kept in a pointer structure where each edge knows its two triangles, LAWSON on $n$ distinct points, not all on one line, takes $O(n \log n + F)$ time, where $F \le n(n - 1)/2$ is the number of flips, so $O(n^2)$ time in the worst case, and $O(n)$ space. No general position is assumed.

**Proof.**

- *Line L1.* The sweep sorts the points in $O(n \log n)$ time. When it adds the point $p_i$, it visits the $k_i$ hull edges that $p_i$ sees, in $O(k_i + 1)$ time, adds $k_i$ triangles and removes those $k_i$ edges from the hull, while adding $2$ new hull edges. The hull starts with fewer than $n$ edges and gains $2$ per point, and every visit removes an edge from it, so $\sum_i k_i \le 3n$. So line L1 takes $O(n \log n)$ time, and its triangulation has fewer than $2n$ triangles and $3n$ edges by Euler's formula.
- *Line L2* puts fewer than $3n$ edges on the stack, in $O(n)$ time.
- *Lines L4 to L7.* One pass pops one edge, finds its two triangles and their third vertices in $O(1)$ time, makes one in-circle test, which is a $3 \times 3$ determinant of integers, and, if it flips, replaces two triangles and updates the six edge records in $O(1)$ time, and pushes at most $4$ edges.
- *Passes.* Every pass pops an edge that was pushed, and there are fewer than $3n + 4F$ pushes, so there are fewer than $3n + 4F$ passes.
- *Flips.* $F \le n(n - 1)/2$ by Lemma 5 of [the correctness proof](/lawson-flip-algorithm/).

So the time is $O(n \log n + n + F) = O(n^2)$. Each edge is on the stack at most once at a time, because line L7 pushes only edges that are not on it, so the stack holds at most $3n$ edges, and the triangulation has $O(n)$ size. So the space is $O(n)$. $\blacksquare$

*Remark.* The code keeps the edges in a Python dictionary, whose operations take $O(1)$ expected time, so for the code the bound on the time is an expected bound over the hashing; a pointer structure such as the [quad-edge structure](/quad-edge-data-structure/) gives the worst-case bound. The bound $F = O(n^2)$ is reached by the code on some inputs: for $m$ points on $y = x^2$ and $m$ points on $y = 10^7 - x^2$, with $x = 0, \ldots, m - 1$, the sweep start leads to $m(m - 2)$ flips for $m = 50, 100, 200, 400$. This count is observed, not proved.
