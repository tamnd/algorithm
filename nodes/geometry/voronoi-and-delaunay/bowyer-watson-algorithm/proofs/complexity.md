---
title: Structural change of the Bowyer-Watson algorithm in random order
proves: [complexity]
status: full
---

**Claim.** Let $S$ be a set of $n \ge 3$ points with no three on a line and no four on a circle, inserted by BOWYER-WATSON in a uniformly random order. Then the expected number of triangles (real and ghost) created by line L9 over the whole run is less than $6n$, and the expected total size of the cavities of line L6 is less than $6n$. In the worst case over all orders both totals are $O(n^2)$.

**Notation.** Let $\pi = (p_1, \ldots, p_n)$ be the insertion order and $S_i = \{p_1, \ldots, p_i\}$. With no three points on a line, the first three points form the triangle of line L3. With no four points on a circle, $S_i$ has exactly one Delaunay triangulation $D(S_i)$ (see [uniqueness](/delaunay-triangulation-uniqueness/)). By the correctness proof, after step $i$ the real triangles of $T$ are $D(S_i)$, and the ghosts are those of its hull edges.

**Lemma 1.** For $i \ge 4$, the triangles created at step $i$ are exactly the triangles of $D(S_i)$ incident to $p_i$, together with the two ghosts incident to $p_i$ when $p_i$ is a hull vertex of $S_i$.

*Proof.* Every triangle created by line L9 has $p_i$ as a vertex. Conversely, every triangle of $T$ at $p_i$ after step $i$ was created in step $i$, since $p_i$ was not present before. $\square$

**Lemma 2.** In a triangulation of $i$ points in general position with $h$ hull vertices, the number of real and ghost triangles at a vertex $v$ is $\deg v + [v \text{ on the hull}]$, and the sum of this over all vertices is $6i - 6 - h$.

*Proof.* An interior vertex of degree $\deg v$ has $\deg v$ triangles around it. A hull vertex has $\deg v - 1$ real triangles and $2$ ghosts. By [Euler's formula](/euler-formula/), a triangulation of $i$ points with $h$ hull vertices has $3i - 3 - h$ edges, so $\sum_v \deg v = 6i - 6 - 2h$, and adding $1$ for each of the $h$ hull vertices gives $6i - 6 - h$. $\square$

**Backwards analysis.** Fix $i \ge 4$ and condition on the set $S_i$. Under a uniformly random permutation, $p_i$ is then a uniformly random element of $S_i$, and $D(S_i)$ depends only on the set $S_i$. By Lemmas 1 and 2, the expected number of triangles created at step $i$ is

$$\frac{1}{i} \sum_{v \in S_i} \left(\deg v + [v \text{ on the hull}]\right) = \frac{6i - 6 - h}{i} < 6.$$

The bound does not depend on $S_i$, so it holds without the condition too. Step 3 creates $4$ triangles. By [linearity of expectation](/linearity-of-expectation/), the expected total number of created triangles is less than $4 + 6(n - 3) < 6n$.

**Cavities.** Every triangle in a cavity is removed by line L8, and each triangle is removed at most once after it is created. So the total cavity size is at most the number of created triangles, and its expectation is less than $6n$. This argument is [backwards analysis](/backwards-analysis/): it looks at the last insertion from the final set $S_i$ instead of at the next insertion from the current one.

**Worst case.** At step $i$ the structure has at most $2i$ triangles and ghosts ($2i - 2 - h$ real ones and $h$ ghosts), so a cavity has at most $2i$ triangles and a step creates at most $2i + 2$ triangles. Summing over $i \le n$ gives $O(n^2)$. The scan of line L5 takes $O(i)$ per step, which also sums to $O(n^2)$.

**What is not proved here.** The bound above counts structural changes only. The expected time of this implementation is not $O(n)$, because line L5 scans the triangles. With the history DAG or with conflict lists the location cost is $O(n \log n)$ expected; that proof is on the [Delaunay triangulation](/delaunay-triangulation/) page. The quadratic lower example (points $(k, k^2)$ in decreasing order of $k$) is observed in tests, not proved here. With cocircular points, $D(S_i)$ is not unique and the backwards analysis above does not apply as stated. $\blacksquare$
