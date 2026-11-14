---
title: Quadratic placement has a unique minimum when every group of cells reaches a pad, conjugate gradients find it, and it lies in the hull of the pads
proves: [correctness, termination, running time]
status: full
---

Write $V$ for the cells, $F$ for the pads, and $w_{ij} > 0$ for the weight of a pair after the clique model (pairs with weight 0 are not edges). The $x$ part of the objective is

$$ \Phi_x(x) = \sum_{\{i, j\} \subseteq V} w_{ij} (x_i - x_j)^2 + \sum_{i \in V, \, q \in F} w_{iq} (x_i - x_q)^2 . $$

The $y$ part has the same form, and $\Phi = \Phi_x + \Phi_y$ with no term that joins $x$ and $y$, so it is enough to treat $\Phi_x$. Pairs of two pads add a constant and are left out.

**Lemma 1 (the system).** With $A$ and $b$ as on the page, $\Phi_x(x) = x^{\mathsf T} A x - 2 b^{\mathsf T} x + c$ with $c = \sum w_{iq} x_q^2$, and $\nabla \Phi_x = 2 (A x - b)$.

*Proof.* Expand each square. A cell pair gives $w_{ij} x_i^2 + w_{ij} x_j^2 - 2 w_{ij} x_i x_j$. In $x^{\mathsf T} A x$ the term $x_i^2$ has the coefficient $A_{ii} = \sum_{j \in V} w_{ij} + \sum_{q \in F} w_{iq}$, and the term $x_i x_j$ appears twice with $A_{ij} = -w_{ij}$, which gives $-2 w_{ij} x_i x_j$. A cell to pad pair gives $w_{iq} x_i^2 - 2 w_{iq} x_q x_i + w_{iq} x_q^2$: the first part is in $A_{ii}$, the second is $-2 b_i x_i$ summed over $q$, and the third is in $c$. The gradient of $x^{\mathsf T} A x$ is $2 A x$ because $A$ is symmetric. $\square$

**Lemma 2 (positive definite).** Call a connected component of the graph on $V$ with the cell to cell edges a *group*. If every group has a cell with an edge to a pad, $A$ is positive definite. If some group has none, $A$ is singular.

*Proof.* By the same expansion as in Lemma 1 with $x_q = 0$,

$$ x^{\mathsf T} A x = \sum_{\{i, j\} \subseteq V} w_{ij} (x_i - x_j)^2 + \sum_{i, q} w_{iq} x_i^2 \ge 0 . $$

If this is 0, every term is 0. The first sum makes $x$ constant on each group, and the second makes $x_i = 0$ for every cell with a pad edge. If every group has such a cell, $x = 0$. So $x^{\mathsf T} A x > 0$ for $x \ne 0$. If a group $G$ has no pad edge, let $x$ be 1 on $G$ and 0 elsewhere. Every edge inside $G$ has equal ends, no edge leaves $G$ to another cell (since $G$ is a component), and no cell of $G$ has a pad edge, so $x^{\mathsf T} A x = 0$ for this $x \ne 0$, and $A x = 0$ because $A$ is positive semidefinite. $\square$

**Theorem 1 (unique minimum).** If every group reaches a pad, $\Phi$ has exactly one minimizer, the solutions of $A x = b_x$ and $A y = b_y$.

*Proof.* For a positive definite $A$, $\Phi_x$ is strictly convex, because $\Phi_x(x + t u) = \Phi_x(x) + 2 t u^{\mathsf T}(A x - b) + t^2 u^{\mathsf T} A u$ with $u^{\mathsf T} A u > 0$ for $u \ne 0$. Let $x^\ast = A^{-1} b$. Then for every $u \ne 0$, $\Phi_x(x^\ast + u) = \Phi_x(x^\ast) + u^{\mathsf T} A u > \Phi_x(x^\ast)$. So $x^\ast$ is the only minimizer. The same holds for $y$. $\blacksquare$

**Theorem 2 (termination of conjugate gradients).** For a positive definite $A$ of order $n$, lines L5 to L9 in exact arithmetic with $tol = 0$ stop after at most $n$ steps with $r = 0$, and then $z = A^{-1} b$.

*Proof.* The loop keeps $r = b - A z$: line L8 adds $\alpha d$ to $z$ and subtracts $\alpha A d$ from $r$. The conjugate gradient method has the property that, as long as no residual is zero, the residuals $r_0, r_1, \ldots$ are pairwise orthogonal and $\alpha$ is defined because $d^{\mathsf T} A d > 0$ for $d \ne 0$ (Hestenes and Stiefel 1952; the induction is on the [conjugate gradient method](/conjugate-gradient-method/) page). Pairwise orthogonal nonzero vectors in $\mathbb{R}^n$ are linearly independent, so there are at most $n$ of them, and $r_k = 0$ for some $k \le n$. Then $A z = b$. $\square$

**Lemma 3 (weighted mean).** At the minimum, $x_i = \left( \sum_{j \in V} w_{ij} x_j + \sum_{q \in F} w_{iq} x_q \right) / A_{ii}$ for every cell $i$, and the same for $y$.

*Proof.* Row $i$ of $A x = b$ reads $A_{ii} x_i - \sum_{j \in V} w_{ij} x_j = \sum_q w_{iq} x_q$. Divide by $A_{ii} > 0$; it is positive because every cell has an edge (a cell with no edge forms a group with no pad and was excluded). $\square$

**Theorem 3 (convex hull).** Let $G$ be a group and $F_G$ the set of pads with an edge to a cell of $G$. At the minimum, every cell of $G$ lies in the convex hull of the positions of $F_G$.

*Proof.* Take any vector $u \in \mathbb{R}^2$, and let $f(v) = u \cdot (x_v, y_v)$ for cells and pads. By Lemma 3, $f(i)$ is the weighted mean of $f$ over the neighbors of $i$, with positive weights, because $f$ is linear. Let $M = \max_{i \in G} f(i)$ and suppose that $M > \max_{q \in F_G} f(q)$. Let $S$ be the cells of $G$ with $f = M$. For $i \in S$, every neighbor has $f \le M$: a cell neighbor is in $G$, and a pad neighbor is in $F_G$ with $f < M$. A weighted mean with positive weights of values at most $M$ equals $M$ only if all values equal $M$. So every neighbor of $i$ is a cell of $S$, and $i$ has no pad neighbor. Then $S$ is closed under neighbors inside the connected group $G$, so $S = G$, and no cell of $G$ has a pad edge, which contradicts $F_G \ne \emptyset$ (Lemma 2 needs a pad edge in $G$). So for every $u$, $\max_{i \in G} f(i) \le \max_{q \in F_G} f(q)$. A point that satisfies this for every $u$ lies in the convex hull of $F_G$: otherwise a line strictly separates it from the hull, and the normal $u$ of that line breaks the inequality. $\square$

**Running time.** Line L1 visits the $p_e (p_e - 1)/2$ pairs of each net, $O(P + E)$ with a hash map for the weights. Line L2 makes the sparse rows in $O(n + E)$, and line L3 is a graph search in $O(n + E)$. Each step of the loop does one product $A d$ in $O(n + E)$ operations and a constant number of vector operations in $O(n)$. By Theorem 2 there are at most $n$ steps per coordinate in exact arithmetic, so the total is $O(P + E + n (n + E))$ arithmetic operations, and the space is $O(n + E)$ for $A$ and five vectors. With $k$ steps in floating point the loop costs $O(k (n + E))$.
