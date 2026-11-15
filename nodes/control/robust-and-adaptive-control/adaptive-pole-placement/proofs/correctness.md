---
title: The pole placement design step has a unique solution for coprime estimates and places the closed loop poles
proves: [correctness]
status: full
---

Notation is that of the page. $A$ is monic of degree $n$, $B$ has degree at most $n - 1$, $A_c$ is monic of degree $n$ and $A_o$ is monic of degree $n - 1$. The unknowns are $R = q^{n-1} + r_1 q^{n-2} + \dots + r_{n-1}$ and $S = s_0 q^{n-1} + \dots + s_{n-1}$.

**Claim 1 (the linear system).** $A R + B S = A_c A_o$ holds if and only if $M x = c$, where $x = (r_1, \dots, r_{n-1}, s_0, \dots, s_{n-1})$, the column of $M$ for $r_i$ holds the coefficients of $q^{n-1-i}A$, the column for $s_j$ holds those of $q^{n-1-j}B$, and $c$ holds the coefficients of $A_c A_o - q^{n-1}A$, all for the powers $q^{2n-2}, \dots, q^0$.

*Proof.* $A R = q^{n-1}A + \sum_{i=1}^{n-1} r_i q^{n-1-i}A$ and $B S = \sum_{j=0}^{n-1} s_j q^{n-1-j}B$. Both $A_c A_o$ and $q^{n-1}A$ are monic of degree $2n - 1$, so their difference has degree at most $2n - 2$, and every term of the sums has degree at most $2n - 2$. Two polynomials of degree at most $2n - 2$ are equal if and only if their $2n - 1$ coefficients are equal, which is $M x = c$. $\square$

**Claim 2 (unique solution for coprime polynomials).** $M$ is invertible if and only if $A$ and $B$ have no common zero.

*Proof.* $M$ is square of size $2n - 1$. Suppose $M x = 0$ with $x \ne 0$. Then $A R' + B S = 0$ with $R' = \sum r_i q^{n-1-i}$ of degree at most $n - 2$ and $S$ of degree at most $n - 1$, not both zero. If $S = 0$ then $A R' = 0$ forces $R' = 0$, so $S \ne 0$. From $A R' = -B S$, every zero of $A$ (with multiplicity) is a zero of $B S$. If $A$ and $B$ are coprime, all $n$ zeros of $A$ are zeros of $S$, but $S \ne 0$ has degree at most $n - 1$, a contradiction. So coprime $A$, $B$ give an invertible $M$. Conversely, if $A = G A_1$ and $B = G B_1$ with $\deg G \ge 1$, then $R' = B_1$ (degree at most $n - 2$) and $S = -A_1$ (degree at most $n - 1$) give $A R' + B S = G A_1 B_1 - G B_1 A_1 = 0$ with $S \ne 0$, so $M$ is singular. $\square$

The determinant of $M$ equals, up to sign, the resultant of $A$ and $B$, which for monic $A$ with zeros $\alpha_1, \dots, \alpha_n$ is $\prod_i B(\alpha_i)$. The tests check this identity on random polynomials, and line L7 uses $|\det M|$ as the test of coprimeness.

**Claim 3 (the closed loop).** Let $A$, $B$ be the true plant, coprime, and let $R$, $S$ solve the equation with $T = t_0 A_o$, $t_0 = A_c(1)/B(1)$, $B(1) \ne 0$. Then the closed loop from $u_c$ to $y$ is $y = t_0 \frac{B}{A_c} u_c$, its characteristic polynomial is $A_c A_o$, and the static gain is 1.

*Proof.* From $A y = B u$ and $R u = T u_c - S y$, eliminate $u$: $A R y = B R u = B T u_c - B S y$, so $(A R + B S) y = B T u_c$ and $y = \frac{B T}{A_c A_o} u_c = \frac{t_0 B A_o}{A_c A_o} u_c$. The closed loop poles are the zeros of $A_c A_o$; the factor $A_o$ cancels in the transfer function from $u_c$ but not in the response to disturbances and initial states. At $q = 1$ the gain is $t_0 B(1)/A_c(1) = 1$. $\square$

**Claim 4 (the projection keeps the design defined).** Line L5 makes $\hat b_0 \ge b_{\min} > 0$, so $\hat B$ never vanishes identically and $\deg \hat B = n - 1$ exactly. Line L7 changes the controller only when $|\det M| > \mathrm{tol}$ and $|\hat B(1)| > \mathrm{tol}$, so by Claim 2 the solve is well defined whenever it runs; otherwise the last controller is kept. These two lines make every step of the algorithm defined; they do not prove that the adaptive closed loop is bounded, which needs the stronger projection described on the page.

**Example check.** For $A = q^2 - 1.5q + 0.7$, $B = q + 0.5$, $A_c A_o = q^3 - q^2 + 0.25q$, the solution in rational arithmetic is $r_1 = 7/34$, $s_0 = 5/17$, $s_1 = -49/170$, and $\det M = 17/10$. The resultant is $B(\alpha_1)B(\alpha_2) = \alpha_1\alpha_2 + 0.5(\alpha_1 + \alpha_2) + 0.25 = 0.7 + 0.75 + 0.25 = 1.7$, which agrees.
