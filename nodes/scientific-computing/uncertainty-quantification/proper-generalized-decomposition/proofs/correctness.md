---
title: Each PGD step is a one-factor energy minimizer, so the energy error does not grow, and the method stops
proves: [correctness, termination]
status: full
---

We assume exact arithmetic. $K_x$ and $K_y$ are symmetric positive definite, $\mathcal{A}(V) = K_x V + V K_y$, $\langle V, W \rangle = \sum_{ij} V_{ij} W_{ij}$, $U$ is the solution of $\mathcal{A}(U) = F$, and $J(V) = \frac12 \langle V, \mathcal{A} V \rangle - \langle F, V \rangle$.

**Lemma 1 (the energy identity).** $\mathcal{A}$ is symmetric positive definite for $\langle \cdot, \cdot \rangle$, and $\|U - V\|_{\mathcal{A}}^2 = \langle U - V, \mathcal{A}(U - V) \rangle = 2 (J(V) - J(U))$ for every $V$.

*Proof.* $\langle W, \mathcal{A} V \rangle = \operatorname{tr}(W^T K_x V) + \operatorname{tr}(W^T V K_y)$, which is symmetric in $V$ and $W$ because $K_x$ and $K_y$ are symmetric. With the eigendecompositions $K_x = Q \Lambda Q^T$ and $K_y = P M P^T$ and $\tilde{V} = Q^T V P$, $\langle V, \mathcal{A} V \rangle = \sum_{kl} (\lambda_k + \mu_l) \tilde{V}_{kl}^2 > 0$ for $V \ne 0$. Expand $J(V) - J(U)$ with $F = \mathcal{A} U$: it is $\frac12 \langle V, \mathcal{A} V \rangle - \langle U, \mathcal{A} V \rangle + \frac12 \langle U, \mathcal{A} U \rangle = \frac12 \|U - V\|_{\mathcal{A}}^2$. $\square$

Fix the current sum $U_{m-1}$ and its residual $R = F - \mathcal{A}(U_{m-1})$. For a product $X Y^T$,

$$\phi(X, Y) = J(U_{m-1} + X Y^T) - J(U_{m-1}) = \tfrac12 \langle X Y^T, \mathcal{A}(X Y^T) \rangle - \langle R, X Y^T \rangle .$$

**Lemma 2 (the half steps).** For a fixed $Y \ne 0$, $\phi(\cdot, Y)$ is a strictly convex quadratic with the unique minimizer $X^*$ given by line L7, and $\phi(X^*, Y) = -\frac12 (R Y)^T G^{-1} (R Y)$ with $G = \|Y\|^2 K_x + (Y^T K_y Y) I$. The same holds for line L8 with the roles of $X$ and $Y$ exchanged.

*Proof.* $\langle X Y^T, K_x X Y^T \rangle = \|Y\|^2 X^T K_x X$ and $\langle X Y^T, X Y^T K_y \rangle = (Y^T K_y Y) \|X\|^2$, so $\phi(X, Y) = \frac12 X^T G X - X^T (R Y)$. $G$ is positive definite, since $\|Y\|^2 > 0$, $K_x$ is positive definite and $Y^T K_y Y > 0$. So the unique minimizer solves $G X = R Y$, which is line L7, and the minimum value is $-\frac12 (RY)^T G^{-1} (RY)$. The proof for $Y$ uses $\langle X Y^T, \mathcal{A}(X Y^T) \rangle = (X^T K_x X) \|Y\|^2 + \|X\|^2 Y^T K_y Y$ in the same way. $\square$

**Lemma 3 (the start vector).** If $R \ne 0$, line L5 returns $Y$ with $R Y \ne 0$.

*Proof.* Some row $i$ of $R$ is not 0, so $R^T e_i \ne 0$, and the loop over $w = (1, \ldots, 1), e_1, e_2, \ldots$ finds a $w$ with $Y = R^T w \ne 0$. Then $w^T R Y = \|R^T w\|^2 > 0$, so $R Y \ne 0$. $\square$

**Theorem 1 (the energy error does not grow).** Let $R \ne 0$ at line L4. Then the new sum $U_m = U_{m-1} + X Y^T$ of line L9 satisfies $\|U - U_m\|_{\mathcal{A}} < \|U - U_{m-1}\|_{\mathcal{A}}$.

*Proof.* Let $Y_0$ be the vector of line L5 and $X_1, Y_1, X_2, \ldots$ the iterates of lines L7 and L8. By Lemma 2, each half step does not increase $\phi$: $\phi(X_1, Y_0) \ge \phi(X_1, Y_1) \ge \phi(X_2, Y_1) \ge \ldots$. By Lemmas 2 and 3, $\phi(X_1, Y_0) = -\frac12 (R Y_0)^T G^{-1} (R Y_0) < 0$, since $G^{-1}$ is positive definite and $R Y_0 \ne 0$. So the final product has $\phi(X, Y) < 0$, that is, $J(U_m) < J(U_{m-1})$, and Lemma 1 turns this into the claim. $\blacksquare$

**Theorem 2 (one mode for a product of eigenvectors).** If $F = s_k s_l^T$ with $K_x s_k = \lambda_k s_k$ and $K_y s_l = \mu_l s_l$, then the first mode is $X Y^T = U = s_k s_l^T / (\lambda_k + \mu_l)$, and the method stops at the next line L4.

*Proof.* With $U_0 = 0$, $R = F$, and line L5 gives $Y_0 = c\, s_l$ with $c = s_k^T w \ne 0$ by Lemma 3. Line L7 gives $c^2 \|s_l\|^2 (K_x + \mu_l I) X = c \|s_l\|^2 s_k$, so $X = s_k / (c(\lambda_k + \mu_l))$. Line L8 then has $X^T K_x X = \lambda_k \|X\|^2$ and $R^T X = (s_k^T X) s_l$, so $\|X\|^2 (\lambda_k I + K_y) Y = (s_k^T X) s_l$ and $Y = c\, s_l$ again. The product does not change, so the loop stops, and $X Y^T = s_k s_l^T / (\lambda_k + \mu_l)$. It solves the equation, since $\mathcal{A}(s_k s_l^T) = (\lambda_k + \mu_l) s_k s_l^T$. Then the next residual is 0. $\blacksquare$

**Termination.** Line L2 runs at most $M$ times and line L6 at most $I$ times, and each of lines L3, L5, L7 and L8 does a finite amount of work. No division by 0 occurs: the tridiagonal matrices of lines L7 and L8 are positive definite by Lemma 2, so all pivots of the Thomas algorithm are positive. Line L5 only runs when $R \ne 0$, and then Lemma 3 gives a nonzero $Y$, so $G$ is positive definite at the first step; every later $X$ and $Y$ is nonzero because it solves $G X = R Y$ with $R Y \ne 0$, which follows by induction from $\phi < 0$ (a zero factor gives $\phi = 0$, and $\phi$ does not increase).

**What is not proved here.** The energy error goes to 0 as $M \to \infty$ when each mode is the best rank-one product; this is the result of Le Bris, Lelièvre and Maday, and it is cited, not proved. The alternating loop of lines L6 to L8 gives a product with $\phi < 0$ but not always the best one, so for this implementation only the monotone decrease is proved.
