---
title: Correctness of the exact Levinson-Durbin algorithm
proves: [correctness, termination]
status: full
---

We prove that LEVINSON returns the solution of $T x = c$ when every leading principal minor $\Delta_1, \ldots, \Delta_n$ of $T$ is nonzero, and that it fails exactly when one of them is zero. Notation is as on the main page: $K$ is a field, indices start at $0$, $T = (t_{i - j})$ is $n \times n$, $T_k$ is its leading $k \times k$ submatrix, $\Delta_k = \det T_k$ with $\Delta_0 = 1$, and $e_1, \ldots, e_k$ are the unit vectors of $K^k$.

**Termination.** The loop on line L4 runs $n - 1$ times, and each pass does a fixed number of inner products of length at most $n$. So the algorithm stops after finitely many steps, either at line L9 or at one of the failures on lines L2 and L6.

**Lemma 1 (shift structure).** Rows $0, \ldots, k - 1$ and columns $0, \ldots, k - 1$ of $T_{k+1}$ form $T_k$, and so do rows $1, \ldots, k$ and columns $1, \ldots, k$, because the entry in row $i$ and column $j$ depends only on $i - j$. Likewise, deleting row $0$ and column $0$ of $T_k$ leaves $T_{k-1}$, and so does deleting row $k - 1$ and column $k - 1$.

**Lemma 2 (padded vectors).** Let $u \in K^k$ and let $T_k u = y$. Then

$$T_{k+1} (u, 0) = \Big(y, \sum_{j<k} t_{k-j} u_j\Big), \qquad T_{k+1} (0, u) = \Big(\sum_{j<k} t_{-1-j} u_j, y\Big).$$

*Proof.* In $(u, 0)$ only columns $0, \ldots, k - 1$ of $T_{k+1}$ are used. By Lemma 1 rows $0, \ldots, k - 1$ give $T_k u = y$, and row $k$ has entries $t_{k - j}$ in column $j$. In $(0, u)$, $u_j$ sits in column $j + 1$. Rows $1, \ldots, k$ restricted to columns $1, \ldots, k$ form $T_k$ by Lemma 1 and give $y$, and row $0$ has entry $t_{0 - (j + 1)} = t_{-1-j}$ in column $j + 1$. $\square$

**Invariant.** At the test of line L4 with loop value $k$ ($1 \le k \le n$, with $k = n$ meaning the loop exits), $\Delta_1, \ldots, \Delta_k$ are nonzero and

$$T_k f = e_1, \qquad T_k g = e_k, \qquad T_k x = (c_0, \ldots, c_{k-1}).$$

*Initialization.* Line L2 passes only if $\Delta_1 = t_0 \ne 0$, and line L3 sets $f = g = (1/t_0)$ and $x = (c_0 / t_0)$, which satisfy the three equations for $T_1 = (t_0)$.

*Maintenance.* Assume the invariant for some $k < n$. With $\varepsilon_f$, $\varepsilon_g$, $\varepsilon_x$ from line L5, Lemma 2 gives

$$T_{k+1} (f, 0) = e_1 + \varepsilon_f e_{k+1}, \qquad T_{k+1} (0, g) = \varepsilon_g e_1 + e_{k+1}, \qquad T_{k+1} (x, 0) = (c_0, \ldots, c_{k-1}, \varepsilon_x),$$

where now $e_1$ and $e_{k+1}$ are unit vectors of $K^{k+1}$.

**Lemma 3.** $d = 1 - \varepsilon_f \varepsilon_g = \Delta_{k-1} \Delta_{k+1} / \Delta_k^2$.

*Proof.* By Cramer's rule, the first entry of $f = T_k^{-1} e_1$ is $f_0 = \det(T_k \text{ without row } 0 \text{ and column } 0) / \Delta_k$, and the last entry of $g = T_k^{-1} e_k$ is $g_{k-1} = \det(T_k \text{ without row } k-1 \text{ and column } k-1) / \Delta_k$. By Lemma 1 both deleted matrices are $T_{k-1}$, so $f_0 = g_{k-1} = \Delta_{k-1} / \Delta_k$; for $k = 1$ this reads $1 / t_0$, as it should.

Let $P$ be the $(k + 1) \times (k + 1)$ matrix whose column $0$ is $(f, 0)$, whose column $k$ is $(0, g)$, and whose other columns are the unit vectors $e_2, \ldots, e_k$ in their own places. $P$ differs from the identity only in columns $0$ and $k$, so expanding along the identity columns, $\det P$ equals the $2 \times 2$ determinant of rows $0$ and $k$ of these two columns:

$$\det P = \det \begin{pmatrix} f_0 & 0 \\ 0 & g_{k-1} \end{pmatrix} = f_0 g_{k-1}.$$

Now compute $\det (T_{k+1} P)$. Its column $0$ is $e_1 + \varepsilon_f e_{k+1}$, its column $k$ is $\varepsilon_g e_1 + e_{k+1}$, and its columns $1, \ldots, k - 1$ are the columns $a_1, \ldots, a_{k-1}$ of $T_{k+1}$. Subtracting $\varepsilon_f$ times column $k$ from column $0$ does not change the determinant and makes column $0$ equal to $(1 - \varepsilon_f \varepsilon_g) e_1 = d e_1$. By linearity in column $0$ and then in column $k$,

$$\det (T_{k+1} P) = d \det (e_1, a_1, \ldots, a_{k-1}, \varepsilon_g e_1 + e_{k+1}) = d \det (e_1, a_1, \ldots, a_{k-1}, e_{k+1}),$$

because the term with $\varepsilon_g e_1$ has two equal columns. Expanding along the unit columns $e_1$ and $e_{k+1}$ leaves the submatrix of $T_{k+1}$ in rows $1, \ldots, k - 1$ and columns $1, \ldots, k - 1$, which is $T_{k-1}$ by Lemma 1. Hence $\det (T_{k+1} P) = d \Delta_{k-1}$, and $\det (T_{k+1} P) = \Delta_{k+1} \det P$ gives

$$\Delta_{k+1} \frac{\Delta_{k-1}^2}{\Delta_k^2} = d \Delta_{k-1}.$$

Since $\Delta_{k-1} \ne 0$ (it is $\Delta_0 = 1$ or one of the minors in the invariant), dividing by $\Delta_{k-1}$ gives the claim. $\square$

So, since $\Delta_{k-1}$ and $\Delta_k$ are nonzero, line L6 fails exactly when $\Delta_{k+1} = 0$, and that is a correct report. Otherwise $d \ne 0$ and $\Delta_{k+1} \ne 0$. Line L7 computes both new vectors from the old $f$ and $g$:

$$T_{k+1} f' = \frac{(e_1 + \varepsilon_f e_{k+1}) - \varepsilon_f (\varepsilon_g e_1 + e_{k+1})}{d} = \frac{(1 - \varepsilon_f \varepsilon_g) e_1}{d} = e_1,$$

$$T_{k+1} g' = \frac{(\varepsilon_g e_1 + e_{k+1}) - \varepsilon_g (e_1 + \varepsilon_f e_{k+1})}{d} = \frac{(1 - \varepsilon_f \varepsilon_g) e_{k+1}}{d} = e_{k+1}.$$

Line L8 sets $x' = (x, 0) + (c_k - \varepsilon_x) g'$, so

$$T_{k+1} x' = (c_0, \ldots, c_{k-1}, \varepsilon_x) + (c_k - \varepsilon_x) e_{k+1} = (c_0, \ldots, c_{k-1}, c_k).$$

So the invariant holds for $k + 1$.

**Conclusion.** If $\Delta_1, \ldots, \Delta_n$ are all nonzero, line L2 passes and, by Lemma 3, line L6 never fails. The loop ends with the invariant for $k = n$, so $T x = T_n x = c$, and since $T$ is nonsingular this $x$ is the unique solution. If some leading minor is zero, let $\Delta_m$ be the first one. If $m = 1$, line L2 fails. If $m \ge 2$, the invariant holds up to $k = m - 1$, and at that pass Lemma 3 gives $d = \Delta_{m-2} \Delta_m / \Delta_{m-1}^2 = 0$, so line L6 fails. In both cases the report "some leading principal minor is zero" is correct, and the algorithm never fails when all of them are nonzero. For $n = 0$, line L1 returns the empty vector, which is the solution of the empty system. $\blacksquare$
