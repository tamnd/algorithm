---
title: The A* embedding is optimal, and the heat weights exist, are nonnegative and sum to 1
proves: [correctness]
status: full
---

We use the notation of the page.
The arithmetic is exact.

## The embedding

The joints are numbered so that $\text{parent}(j) < j$, with the root $1$.
A node of the search is a partial assignment $(a(1), \ldots, a(k))$, and its cost is $g = \sum_{j = 2}^{k} \pi_j(a(\text{parent}(j)), a(j))$.
Every bone of $g$ has both ends placed, because the parent of a placed joint is placed.
Let $\text{low}_j = \min_{u, v} \pi_j(u, v) \ge 0$ and $h_k = \sum_{j > k} \text{low}_j$.

**Lemma 1.** $h$ is admissible and consistent: for every completion of a node, $g + h_k \le$ the cost of the completion, and if a child places joint $k + 1$, then $g' + h_{k+1} \ge g + h_k$.

*Proof.*
A completion adds $\pi_j(\cdot, \cdot) \ge \text{low}_j$ for every $j > k$, which gives the first claim.
For the child, $g' = g + \pi_{k+1}(\cdot, \cdot) \ge g + \text{low}_{k+1}$ and $h_{k+1} = h_k - \text{low}_{k+1}$. $\square$

**Theorem 1.** The first complete assignment that line L4 pops has the smallest cost.

*Proof.*
Let $a^*$ be an optimal assignment with the cost $g^*$, and suppose that line L4 pops a complete assignment $b$ with the cost $g_b > g^*$.
At that time, some prefix of $a^*$ is in the heap: the empty prefix was pushed, and when a prefix is popped, its child on the way to $a^*$ is pushed.
By Lemma 1, the priority of that prefix is at most $g^*$, which is smaller than the priority $g_b$ of $b$ (for a complete node $h = 0$).
The heap pops the smallest priority first, so it cannot pop $b$ before that prefix, and the same holds for every later prefix of $a^*$ down to $a^*$ itself.
So $a^*$, or another complete node with the priority at most $g^*$, is popped before $b$, which contradicts the choice of $b$. $\square$

The search tree has no repeated states, because a state is a sequence of choices for the joints in a fixed order, so no closed set is needed.
Every node popped has priority at most $g^*$, so the search expands at most the nodes with $g + h \le g^*$, and at most $\sum_{k < J} C^k$ nodes.

## The heat system

Let $K$ be the stiffness matrix of the closed polyline (or of the mesh), $M$ the diagonal of positive masses, and $H \ge 0$ diagonal.
For the polyline, $x^\top K x = \sum_{e = (u, v)} (x_u - x_v)^2 / \ell_e \ge 0$, with equality exactly for constant $x$ on a connected surface; the cotangent Laplacian of a Delaunay mesh has the same two properties.

**Lemma 2.** If $H_{jj} > 0$ for some $j$, then $A = K + M H$ is symmetric positive definite.

*Proof.*
$A$ is symmetric because $K$ is and $M H$ is diagonal.
$x^\top A x = x^\top K x + \sum_j m_j H_{jj} x_j^2 \ge 0$.
If it is zero, $x^\top K x = 0$, so $x$ is constant, $x = t \mathbf{1}$, and the second term is $t^2 m_j H_{jj}$ for the $j$ with $H_{jj} > 0$, so $t = 0$. $\square$

So the Cholesky factorization of line L9 exists, and each line L10 has exactly one solution.

**Theorem 2.** $\sum_i w^i = \mathbf{1}$.

*Proof.*
$\sum_i p^i_j = k \cdot (1 / k) = 1$ if vertex $j$ sees a bone, and the sum is 0 if it sees none, in which case $H_{jj} = 0$.
So $\sum_i M H p^i = M H \mathbf{1}$.
The system is linear, so $s = \sum_i w^i$ solves $A s = M H \mathbf{1}$.
$A \mathbf{1} = K \mathbf{1} + M H \mathbf{1} = M H \mathbf{1}$, because the rows of $K$ sum to 0.
By Lemma 2 the solution is unique, so $s = \mathbf{1}$. $\square$

**Theorem 3.** $w^i \ge 0$ for every bone, when the off-diagonal entries of $K$ are not positive (always on the polyline, and on a mesh with nonnegative cotangent weights).

*Proof.*
$A$ is symmetric positive definite with nonpositive entries off the diagonal, so $A$ is a nonsingular M-matrix, and $A^{-1}$ has no negative entries.
A direct argument: let $j$ be the index of the smallest entry of $w = w^i$, and suppose $w_j < 0$.
With $K_{jj} = -\sum_{u \ne j} K_{ju} = \sum_{u \ne j} |K_{ju}|$, row $j$ reads $\sum_{u \ne j} |K_{ju}| (w_j - w_u) + m_j H_{jj} w_j = m_j H_{jj} p^i_j$.
Each term of the sum is at most 0 because $w_j$ is the smallest entry, and the last term is at most 0 because $w_j < 0$.
The right side is at least 0.
So both sides are 0, $H_{jj} w_j = 0$ gives $H_{jj} = 0$, and $w_u = w_j$ for every neighbor $u$ with $K_{ju} \ne 0$.
The neighbors are also minima, and the same argument spreads over the connected surface, so $w$ is the constant $w_j$ and $H = 0$ everywhere, which contradicts the assumption of Lemma 2. $\square$

With Theorem 2, also $w^i \le 1$.

## The check value

On the square with side 2, every edge has $\ell_e = 2$, so $K_{jj} = 1$, $K_{ju} = -1/2$ for the two neighbors, and $m_j = 2$.
Every vertex has its nearest visible bone at the distance $\sqrt{0.5}$, so $H_{jj} = 1 / 0.5 = 2$ and $m_j H_{jj} = 4$.
The system for bone A is invariant under the reflection $x \mapsto -x$, which swaps vertices 1 and 2 and vertices 3 and 4, so by uniqueness $w^A = (a, a, b, b)$, and $b = 1 - a$ by Theorem 2.
Row 1: $a - \frac12 a - \frac12 b + 4 a = 4$, so $\frac92 a - \frac12 (1 - a) = 4$, $5 a = 4.5$ and $a = 0.9$.
Row 3: $b - \frac12 b - \frac12 a + 4 b = 0$ gives $4.5 \cdot 0.1 - 0.45 = 0$, which holds.
