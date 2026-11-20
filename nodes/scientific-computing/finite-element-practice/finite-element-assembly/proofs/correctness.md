---
title: Assembly computes the Galerkin matrix and the Dirichlet step keeps it symmetric
proves: [correctness]
status: full
---

**Setting.** The mesh has cells $K_1, \ldots, K_E$ and the global space $V_h$ has the basis $\phi_1, \ldots, \phi_N$. Each cell $K$ has local basis functions $\phi^K_1, \ldots, \phi^K_n$ and a local-to-global map $g = g_K$ from $\{1, \ldots, n\}$ to $\{1, \ldots, N\}$. We assume:

1. *(Map.)* $g_K$ is one to one, and for every $i$ the restriction $\phi_i|_K$ is $\phi^K_r$ if $g_K(r) = i$ and is $0$ if $i$ is not in the image of $g_K$.
2. *(Forms.)* $a(u, v) = \sum_K a_K(u|_K, v|_K)$ and $l(v) = \sum_K l_K(v|_K)$, as for forms that are integrals over $\Omega$ split into cells.
3. *(Element.)* For the cell data of $K$, ELEMENT returns $A_K[r, s] = a_K(\phi^K_s, \phi^K_r)$ and $b_K[r] = l_K(\phi^K_r)$.

A missing entry of the sparse matrix stands for $0$.

**Lemma 1 (assembly).** After line L9, $A[i, j] = a(\phi_j, \phi_i)$ and $b[i] = l(\phi_i)$ for all $i, j$.

*Proof.* We show the invariant: after the loop of line L2 has processed the cells $K_1, \ldots, K_m$,

$$A[i, j] = \sum_{t=1}^m \sum_{\substack{r, s:\ g_{K_t}(r) = i,\\ g_{K_t}(s) = j}} A_{K_t}[r, s], \qquad b[i] = \sum_{t=1}^m \sum_{r:\ g_{K_t}(r) = i} b_{K_t}[r].$$

For $m = 0$ both sides are $0$ by line L1. Assume it for $m - 1$ and process $K = K_m$. Line L3 takes its map $g$ and line L4 computes $A_K$ and $b_K$. For each pair $(r, s)$ the loops of lines L5 and L7 visit it exactly once, and line L8 adds $A_K[r, s]$ to $A[g(r), g(s)]$. No other entry of $A$ changes. In the same way line L6 adds $b_K[r]$ to $b[g(r)]$ once for each $r$. So the invariant holds for $m$.

At the end $m = E$. Fix $i$ and $j$ and a cell $K$. Because $g_K$ is one to one, the inner sum for $K$ has at most one term. If both $i$ and $j$ are in the image of $g_K$, with $g_K(r) = i$ and $g_K(s) = j$, the term is $A_K[r, s] = a_K(\phi^K_s, \phi^K_r) = a_K(\phi_j|_K, \phi_i|_K)$ by assumptions 3 and 1. If one of them is not in the image, the sum is empty, and by assumption 1 one of the restrictions is $0$, so again the sum equals $a_K(\phi_j|_K, \phi_i|_K) = 0$. By assumption 2 the sum over all cells is $a(\phi_j, \phi_i)$. The argument for $b$ is the same. $\square$

**Lemma 2 (Dirichlet step).** Let $D$ be the set of Dirichlet indices with prescribed values $g_j$, $j \in D$, and let $F$ be the other indices. Let $A'$ and $b'$ be the result of lines L10 to L13 applied to $A$ and $b$. Then:

1. $A'U = b'$ holds if and only if $U_j = g_j$ for all $j \in D$ and $\sum_k A[i, k]U_k = b[i]$ for all $i \in F$;
2. if $A$ is symmetric, so is $A'$;
3. if $A_{FF}$, the submatrix on the free indices, is positive definite, so is $A'$.

*Proof.* Lines L10 and L11 finish before line L12 starts, so they read the original $A$. For $i \in F$ they give $b'[i] = b[i] - \sum_{j \in D}A[i, j]g_j$, and they do not change $b[i]$ for $i \in D$ or any entry of $A$. Line L12 then makes row $i$ of $A$ the unit row $e_i^\top$ for every $i \in D$, sets $b'[i] = g_i$, and removes column $i$ from every other row. (The code reaches those rows through the pattern of row $i$. The pattern of $A$ is symmetric, because line L8 visits $(g(r), g(s))$ and $(g(s), g(r))$ for the same cell, so this removes every nonzero of the column.) In block form, with the free indices first,

$$A' = \begin{pmatrix} A_{FF} & 0 \\ 0 & I\end{pmatrix}, \qquad b' = \begin{pmatrix} b_F - A_{FD}\,g \\ g\end{pmatrix}.$$

So $A'U = b'$ means $U_D = g$ and $A_{FF}U_F = b_F - A_{FD}g$, that is, $A_{FF}U_F + A_{FD}U_D = b_F$, which is part 1. Part 2 holds because $A_{FF}$ is a principal submatrix of a symmetric matrix and the off-diagonal blocks are zero. For part 3, $x^\top A'x = x_F^\top A_{FF}x_F + |x_D|^2 > 0$ for $x \ne 0$. $\square$

**Theorem.** Under the assumptions above, ASSEMBLE followed by APPLY-DIRICHLET returns a system whose solution $U$ gives $u_h = \sum_k U_k\phi_k$ with $u_h(x_j) = g_j$ at the Dirichlet nodes and $a(u_h, \phi_i) = l(\phi_i)$ for every free basis function $\phi_i$. This is the Galerkin method on $V_h$ with the Dirichlet values imposed by nodal interpolation. If $a$ is symmetric and coercive on the functions of $V_h$ that vanish at the Dirichlet nodes, the system matrix is symmetric positive definite.

*Proof.* By Lemma 1, $\sum_k A[i, k]U_k = \sum_k a(\phi_k, \phi_i)U_k = a(u_h, \phi_i)$ and $b[i] = l(\phi_i)$. Lemma 2, part 1, gives the two conditions. For part 3 of Lemma 2, let $x_F \ne 0$ and $v = \sum_{k \in F}x_k\phi_k$. Then $v$ vanishes at the Dirichlet nodes and $x_F^\top A_{FF}x_F = a(v, v) > 0$. $\square$

**Remark (quadrature).** Assumption 3 holds exactly when the quadrature rule in ELEMENT integrates the element integrands exactly. The reference code uses Boole's rule on each 1D cell, which is exact for polynomials of degree 5, so the P1 and P2 stiffness and mass matrices for a constant $\kappa$ are exact. With a weaker rule, Lemma 1 still holds with $a_K$ replaced by its quadrature approximation, and the method is a Galerkin method for a perturbed form.
