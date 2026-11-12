---
title: RIDGE returns the unique minimizer of the ridge objective with an unpenalized intercept
proves: [correctness, termination]
status: full
---

Let $X \in \mathbb{R}^{n \times d}$, $y \in \mathbb{R}^n$ and $\lambda \ge 0$. Let $J(w, b) = \|y - Xw - b\mathbf{1}\|^2 + \lambda\|w\|^2$. Let $\bar x$, $\bar y$, $X_c$ and $y_c$ be as in lines L1 and L2, so $X_c^\top\mathbf{1} = 0$ and $y_c^\top\mathbf{1} = 0$. Assume $\lambda > 0$, or $\lambda = 0$ and $X_c$ has rank $d$. Arithmetic is exact in this proof.

**Lemma 1 (the intercept).** For each $w$, $J(w, b) = J_c(w) + n(b - \bar y + \bar x^\top w)^2$, where $J_c(w) = \|y_c - X_c w\|^2 + \lambda\|w\|^2$.

*Proof.* Write $y - Xw - b\mathbf{1} = (y_c - X_c w) + (\bar y - \bar x^\top w - b)\mathbf{1}$, because $y = y_c + \bar y\mathbf{1}$ and $Xw = X_c w + (\bar x^\top w)\mathbf{1}$. The first part is orthogonal to $\mathbf{1}$, since $\mathbf{1}^\top y_c = 0$ and $\mathbf{1}^\top X_c = 0$. By Pythagoras, the squared norm is $\|y_c - X_c w\|^2 + n(\bar y - \bar x^\top w - b)^2$. Add $\lambda\|w\|^2$. $\square$

So $(w, b)$ minimizes $J$ exactly when $w$ minimizes $J_c$ and $b = \bar y - \bar x^\top w$.

**Lemma 2 (the system).** $G = X_c^\top X_c + \lambda I$ is positive definite, and $J_c$ has exactly one minimizer, the solution of $Gw = h$ with $h = X_c^\top y_c$.

*Proof.* For $u \ne 0$, $u^\top G u = \|X_c u\|^2 + \lambda\|u\|^2$. If $\lambda > 0$ the second term is positive. If $\lambda = 0$, the first term is positive because $X_c$ has rank $d$. Next, $J_c(w) = w^\top G w - 2h^\top w + y_c^\top y_c$. For each $w$ and $u$, $J_c(w + u) - J_c(w) = 2u^\top(Gw - h) + u^\top G u$. If $Gw = h$, this is $u^\top Gu > 0$ for all $u \ne 0$, so $w$ is the unique minimizer. Such a $w$ exists because $G$ is nonsingular. $\square$

**Lemma 3 (Cholesky and the solves).** Line L5 computes a lower triangular $L$ with positive diagonal and $LL^\top = G$, and lines L6 and L7 give $w = G^{-1}h$.

*Proof.* The column loop of line L5 sets, for each $j$, $L_{jj}^2 = G_{jj} - \sum_{k<j}L_{jk}^2$ and $L_{ij} = (G_{ij} - \sum_{k<j}L_{ik}L_{jk})/L_{jj}$ for $i > j$. These are the entries $(j, j)$ and $(i, j)$ of $LL^\top = G$, solved for the new unknowns, so they hold whenever each $L_{jj}^2 > 0$. Let $G_j$ be the leading $j \times j$ block of $G$. If the first $j - 1$ columns are computed, then $L_{j-1}L_{j-1}^\top = G_{j-1}$, and the value $s$ at column $j$ is the Schur complement $G_{jj} - g^\top G_{j-1}^{-1} g$ of $G_{j-1}$ in $G_j$, where $g$ is the part of row $j$ to the left of the diagonal. So $s = \det G_j / \det G_{j-1}$. Each leading block of a positive definite matrix is positive definite, so its determinant is positive and $s > 0$. By induction all $d$ columns are computed. Then $Lz = h$ and $L^\top w = z$ have one solution each, found by the substitutions of lines L6 and L7, and $Gw = LL^\top w = Lz = h$. $\square$

**Termination.** Every line runs a fixed number of loops over $n$ and $d$, and by Lemma 3 line L5 does not stop with a non-positive pivot.

**Theorem.** RIDGE returns the unique minimizer $(\hat w, \hat b)$ of $J$.

*Proof.* By Lemmas 2 and 3, line L7 gives the unique minimizer $\hat w$ of $J_c$. By Lemma 1, $J(w, b) \ge J_c(w) \ge J_c(\hat w)$, with equality in the first step exactly when $b = \bar y - \bar x^\top w$ and in the second exactly when $w = \hat w$. Line L8 sets $\hat b = \bar y - \bar x^\top\hat w$. So $(\hat w, \hat b)$ is the only pair that reaches the minimum. $\blacksquare$
