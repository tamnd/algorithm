---
title: Stepwise regression by sweeps scores every single move exactly and stops at a local minimum of the criterion
proves: [correctness, termination]
status: full
---

The arithmetic is exact. Let $\tilde x_1, \dots, \tilde x_m$ and $\tilde y$ be the columns of $X$ and $y$ minus their means, and let $a = A^{(0)}$ be the $(m + 1) \times (m + 1)$ matrix of their inner products, with $y$ as the last index. For $S \subseteq \{1, \dots, m\}$ write $\tilde X_S$ for the centered columns in $S$, $G_S = \tilde X_S^\top\tilde X_S$, and $T = \{1, \dots, m, y\} \setminus S$. Centering removes the intercept: for any $S$, the least squares fit of $y$ on $\mathbf 1$ and $X_S$ has the same slopes and residuals as the fit of $\tilde y$ on $\tilde X_S$ without intercept, because the residual of a fit with an intercept is orthogonal to $\mathbf 1$.

**Lemma 1 (block form of a swept matrix).** If $G_S$ is nonsingular, sweeping $A^{(0)}$ on the indices of $S$, one after the other in any order, meets only nonzero pivots and gives

$$A^{(S)} = \begin{pmatrix} -G_S^{-1} & G_S^{-1}a_{ST} \\ a_{TS}G_S^{-1} & a_{TT} - a_{TS}G_S^{-1}a_{ST} \end{pmatrix}.$$

*Proof.* By induction on $|S|$. For $S = \emptyset$ the formula is $A^{(0)}$. Suppose it holds for $S$, and sweep on $k \in T$, $k \ne y$, with $G_{S \cup \{k\}}$ nonsingular. The pivot is $d = A^{(S)}_{kk} = a_{kk} - a_{kS}G_S^{-1}a_{Sk}$, the Schur complement of $G_S$ in $G_{S \cup \{k\}}$, and $\det G_{S \cup \{k\}} = d\det G_S$, so $d \ne 0$. Write $g = G_S^{-1}a_{Sk}$. The block inverse formula (see [Schur complement](/schur-complement/)) gives

$$G_{S\cup\{k\}}^{-1} = \begin{pmatrix} G_S^{-1} + gg^\top/d & -g/d \\ -g^\top/d & 1/d \end{pmatrix}.$$

Compare the sweep of $A^{(S)}$ on $k$ with the formula for $S \cup \{k\}$, entry by entry, with $i, j \in S$ and $t, u \in T \setminus \{k\}$.

- Pivot: $-1/d$, which is minus the corner $1/d$.
- $(i, k)$: $A^{(S)}_{ik}/d = g_i/d$, which is minus the entry $-g_i/d$ of the inverse.
- $(i, j)$: $-(G_S^{-1})_{ij} - g_ig_j/d$, minus the top left block.
- $(k, t)$: $A^{(S)}_{kt}/d = (a_{kt} - g^\top a_{St})/d$. The target is row $k$ of $G_{S\cup k}^{-1}a_{S\cup k, t}$, which is $-g^\top a_{St}/d + a_{kt}/d$. They agree.
- $(i, t)$: $A^{(S)}_{it} - A^{(S)}_{ik}A^{(S)}_{kt}/d = (G_S^{-1}a_{St})_i - g_i(a_{kt} - g^\top a_{St})/d$. The target is $(G_S^{-1}a_{St})_i + g_ig^\top a_{St}/d - g_ia_{kt}/d$. They agree.
- $(t, u)$: $A^{(S)}_{tu} - A^{(S)}_{tk}A^{(S)}_{ku}/d$ with $A^{(S)}_{tk} = a_{tk} - a_{tS}g$. Expanding the target $a_{tu} - a_{t,S\cup k}G_{S\cup k}^{-1}a_{S\cup k,u}$ with the block inverse gives $a_{tu} - a_{tS}G_S^{-1}a_{Su} - (a_{tk} - a_{tS}g)(a_{ku} - g^\top a_{Su})/d$, the same.

The entries in row $k$ and columns $i$ or $t$ follow by symmetry. So the result is the formula for $S \cup \{k\}$. The formula depends only on the set, so the order of the sweeps does not matter. $\square$

**Lemma 2 (reading the swept matrix).** In $A^{(S)}$: $A^{(S)}_{Sy} = \hat b_S$, the least squares slopes of $y$ on $X_S$ with intercept; $A^{(S)}_{yy} = \mathrm{RSS}(S)$; for $j \notin S$, $A^{(S)}_{jj} = \|e_j\|^2$ and $A^{(S)}_{jy} = e_j^\top e_y$, where $e_j$ and $e_y$ are the residuals of $\tilde x_j$ and $\tilde y$ after projection on the span of $\tilde X_S$.

*Proof.* By Lemma 1, $A^{(S)}_{Sy} = G_S^{-1}\tilde X_S^\top\tilde y$, the solution of the normal equations. With $H = \tilde X_SG_S^{-1}\tilde X_S^\top$, the orthogonal projection on the span of $\tilde X_S$, the lower right block is $\tilde u^\top(I - H)\tilde v$ for $u, v \in T$, and $I - H$ is symmetric and idempotent, so this is $e_u^\top e_v$. For $u = v = y$ it is $\mathrm{RSS}(S)$. $\square$

**Lemma 3 (the RSS after one move).** Let $A = A^{(S)}$. For $j \notin S$ with $A_{jj} \ne 0$, $\mathrm{RSS}(S \cup \{j\}) = A_{yy} - A_{jy}^2/A_{jj}$. For $j \in S$, $\mathrm{RSS}(S \setminus \{j\}) = A_{yy} - A_{jy}^2/A_{jj}$ as well.

*Proof.* Adding: the span of $\tilde X_{S \cup \{j\}}$ is the span of $\tilde X_S$ plus the orthogonal direction $e_j$, so the new residual is $e_y - (e_j^\top e_y/\|e_j\|^2)e_j$, whose squared norm is $\|e_y\|^2 - (e_j^\top e_y)^2/\|e_j\|^2$. Lemma 2 turns this into the formula. Dropping: let $S' = S \setminus \{j\}$, and write $e'_j$ and $e'_y$ for the residuals on $S'$. The adding case gives $\mathrm{RSS}(S) = \mathrm{RSS}(S') - (e_j'^\top e'_y)^2/\|e'_j\|^2$. By Lemma 1, $A^{(S)}$ is $A^{(S')}$ swept on $j$, with pivot $\|e'_j\|^2$ by Lemma 2, so $A_{jj} = -1/\|e'_j\|^2$ and $A_{jy} = e_j'^\top e'_y/\|e'_j\|^2$. Then $-A_{jy}^2/A_{jj} = (e_j'^\top e'_y)^2/\|e'_j\|^2$, and $A_{yy} - A_{jy}^2/A_{jj} = \mathrm{RSS}(S')$. $\square$

**Lemma 4 (reverse sweep).** The reverse sweep on $k \in S$ applied to $A^{(S)}$ gives $A^{(S \setminus \{k\})}$.

*Proof.* Let $B$ be the sweep of a matrix $C$ on $k$, with pivot $d = c_{kk} \ne 0$. The reverse sweep of $B$ on $k$ has pivot $e = b_{kk} = -1/d$. It sets the pivot to $-1/e = d = c_{kk}$; it sets $b_{ik}$ to $-b_{ik}/e = -(c_{ik}/d)/(-1/d) = c_{ik}$, and the same for $b_{kj}$; and for $i, j \ne k$ it sets $b_{ij}$ to $b_{ij} - b_{ik}b_{kj}/e = (c_{ij} - c_{ik}c_{kj}/d) + c_{ik}c_{kj}/d = c_{ij}$. So the reverse sweep inverts the sweep. By Lemma 1 the order of sweeps is free, so $A^{(S)}$ is $A^{(S \setminus \{k\})}$ swept on $k$, and the reverse sweep on $k$ returns $A^{(S \setminus \{k\})}$. $\square$

**Lemma 5 (the F statistics).** The F-to-enter of $j \notin S$ and the F-to-remove of $j \in S$, computed from line L7, are the squared t statistics of $\hat b_j$ in the models $S \cup \{j\}$ and $S$, with $n - |S| - 2$ and $n - |S| - 1$ residual degrees of freedom.

*Proof.* For a model $M$ with $p$ columns including the intercept and a column $j \in M$, the extra sum of squares $\mathrm{RSS}(M \setminus \{j\}) - \mathrm{RSS}(M)$ divided by $\mathrm{RSS}(M)/(n - p)$ equals $t_j^2$ (the one-column case of the [regression F-test](/regression-f-test/)). For entering, $M = S \cup \{j\}$ has $p = |S| + 2$ columns; for removing, $M = S$ has $p = |S| + 1$. Lemma 3 gives both residual sums of squares. $\square$

**Theorem.** With a criterion $c$, the algorithm stops after at most $2^m$ moves and returns a subset $S$ with $c(\mathrm{RSS}(S), |S|) \le c(\mathrm{RSS}(S'), |S'|)$ for every allowed neighbor $S'$ whose design is nonsingular. With partial F-tests, it stops after visiting at most $2^m$ subsets.

*Proof.* By Lemmas 1 to 4, after each move the matrix equals $A^{(S)}$ for the current $S$, and line L7 gives $\mathrm{RSS}(S')$ for each neighbor $S'$ exactly. A neighbor with a singular design is skipped by line L6, since then $A_{jj} = \|e_j\|^2 = 0$. Line L8 chooses a move only if it strictly lowers $c$, so the values of $c$ along the path strictly decrease. Each subset has one value of $c$, so no subset appears twice, and there are $2^m$ subsets. When line L9 returns, no allowed neighbor has a smaller value, which is the claim. With F-tests the implementation records each subset it reaches and stops at the first repeat, so the loop runs at most $2^m$ times. $\square$

The theorem does not say that $S$ minimizes $c$ over all subsets, and that is false in general: on the example of the page, forward selection with AIC stops at $\{3\}$ while $\{1, 2, 3\}$ has a smaller AIC.
