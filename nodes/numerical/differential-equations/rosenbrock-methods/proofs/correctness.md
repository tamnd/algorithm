---
title: Order conditions up to order 3, the stability function and the W-property of Rosenbrock methods
proves: [correctness, termination, convergence]
status: full
---

**Setting.** $f : [t_0, T] \times \mathbb{R}^d \to \mathbb{R}^d$ is $C^{p+1}$ near the solution with bounded derivatives, and Lipschitz in $y$ with constant $L$. A Rosenbrock method with $s$ stages has strictly lower triangular $(\alpha_{ij})$ and $(\gamma_{ij})$, weights $b_i$ and a diagonal value $\gamma$. Write $\alpha_i = \sum_{j<i}\alpha_{ij}$, $\gamma_i = \gamma + \sum_{j<i}\gamma_{ij}$, $\beta_{ij} = \alpha_{ij} + \gamma_{ij}$ and $\beta_i' = \sum_{j<i}\beta_{ij}$. One step of size $h$ from $(t, y)$ with $J = f_y(t, y)$ and $f_t = f_t(t, y)$ is

$$(I - h\gamma J) k_i = h f\Big(t + \alpha_i h,\ y + \sum_{j<i}\alpha_{ij}k_j\Big) + hJ\sum_{j<i}\gamma_{ij}k_j + \gamma_i h^2 f_t, \qquad y_{\text{new}} = y + \sum_i b_i k_i.$$

**Termination.** Line L1 gives a finite $N$. Each step does one LU factorization and exactly $s$ triangular solves; there is no iteration. If $I - h\gamma J$ is singular the factorization reports it. Otherwise each step finishes, so the method stops after $N$ steps.

**Lemma 1 (well defined for small h).** If $h\gamma\|J\| < 1$ then $I - h\gamma J$ is invertible, and the $k_i$ are computed one after the other from already known quantities. For a dissipative $J$ (logarithmic norm $\mu(J) \le 0$) and $\gamma > 0$ the matrix is invertible for every $h > 0$, which is the stiff case.

**Lemma 2 (autonomization).** Apply the method to the autonomous system $(t, y)' = (1, f(t, y))$. Its Jacobian has a zero first row, so the $t$-component of every stage is $k_i^t = h$. Substituting this into the $y$-component turns the term $h(f_t \sum_{j<i}\gamma_{ij}k_j^t) + h\gamma f_t k_i^t$ into $\gamma_i h^2 f_t$ and the time argument into $t + \alpha_i h$. So the method above is exactly the method for the autonomized system, and it suffices to treat $y' = f(y)$ with $f_t = 0$.

**Lemma 3 (Taylor expansion of the stages).** For $y' = f(y)$, with $f$, $f'$, $f''$ evaluated at $y$, the stages satisfy

$$k_i = h f + h^2 (\beta_i' + \gamma) f'f + h^3\Big(\tfrac{\alpha_i^2}{2} f''(f, f) + \Big(\sum_{j<i}\beta_{ij}(\beta_j' + \gamma) + \gamma(\beta_i' + \gamma)\Big) f'f'f\Big) + O(h^4).$$

*Proof.* By Lemma 1 the $k_i$ are smooth functions of $h$ with $k_i = O(h)$. Rewrite the stage equation as $k_i = h f(y + \sum_{j<i}\alpha_{ij}k_j) + hJ\big(\sum_{j<i}\gamma_{ij}k_j + \gamma k_i\big)$ and insert the expansions of the earlier stages. The $h$ term is $hf$. The $h^2$ terms come from $h f'\sum_j \alpha_{ij}k_j$ and $hJ(\sum_j\gamma_{ij}k_j + \gamma k_i)$ with $k_j \approx hf$ and $J = f'$, giving $(\alpha_i + \sum_{j<i}\gamma_{ij} + \gamma)f'f = (\beta_i' + \gamma)f'f$. The $h^3$ terms come from $\frac{h}{2}f''(\sum\alpha_{ij}k_j, \sum\alpha_{ij}k_j)$, which gives $\frac{\alpha_i^2}{2}f''(f, f)$, and from the $h^2$ parts of $k_j$ and $k_i$ in the linear terms, which give $\sum_{j<i}(\alpha_{ij} + \gamma_{ij})(\beta_j' + \gamma) f'f'f + \gamma(\beta_i' + \gamma)f'f'f$. $\square$

**Theorem 1 (order conditions up to 3, proved).** The local error $y(t + h) - y_{\text{new}}$ is $O(h^{p+1})$ for $p = 1, 2, 3$ if and only if the following hold up to the respective order:

- order 1: $\sum_i b_i = 1$;
- order 2: $\sum_i b_i\beta_i' = \frac12 - \gamma$;
- order 3: $\sum_i b_i\alpha_i^2 = \frac13$ and $\sum_i b_i\sum_{k<i}\beta_{ik}\beta_k' = \frac16 - \gamma + \gamma^2$.

*Proof.* The exact solution is $y + hf + \frac{h^2}{2}f'f + \frac{h^3}{6}(f''(f, f) + f'f'f) + O(h^4)$. Summing Lemma 3 with weights $b_i$ and comparing the coefficients of the independent elementary differentials $f$, $f'f$, $f''(f, f)$, $f'f'f$ gives $\sum b_i = 1$, $\sum b_i(\beta_i' + \gamma) = \frac12$, $\frac12\sum b_i\alpha_i^2 = \frac16$, and $\sum b_i\sum_{j<i}\beta_{ij}\beta_j' + \gamma\sum b_i\beta_i' + \gamma\sum b_i\beta_i' + \gamma^2 = \frac16$. Using the order 2 condition in the last one gives $\sum bββ' = \frac16 - 2\gamma(\frac12 - \gamma) - \gamma^2 = \frac16 - \gamma + \gamma^2$. The elementary differentials are independent (each is nonzero alone for a suitable polynomial $f$), so the conditions are also necessary. $\square$

The tests check these four residuals exactly in Fractions: all vanish for ROW3 with $\gamma = \frac12$, the first two vanish for ROS2 with $\gamma = \frac12$, and for ROS2 with $\gamma = 1 + 1/\sqrt2$ they vanish to rounding.

**Theorem 2 (convergence, proved).** If a method satisfies the conditions of order $p \le 3$ and $f$ is $C^{p+1}$, the global error on $[t_0, T]$ is $O(h^p)$. *Proof.* By Lemma 1 the increment $\sum_i b_i k_i / h$ is a smooth function of $(t, y, h)$ for $h \le h_0$, hence Lipschitz in $y$ on a neighbourhood of the solution. The local error is $O(h^{p+1})$ by Theorem 1, and the standard one-step argument gives $\|e_n\| \le C h^p$. $\square$

**Theorem 3 (W-methods, proved for order 2).** Replace $J$ by an arbitrary bounded matrix $W$. In Lemma 3 the $h^2$ term becomes $\alpha_i f'f + (\gamma_i)\,W f$ with $\gamma_i = \gamma + \sum_{j<i}\gamma_{ij} = \beta_i' + \gamma - \alpha_i$. Order 2 then needs $\sum b_i\alpha_i = \frac12$ and $\sum b_i\gamma_i = 0$; the latter equals $\sum b_i(\beta_i' + \gamma) - \sum b_i\alpha_i = \frac12 - \frac12$. So a method of order 2 with $\sum b_i\alpha_i = \frac12$ keeps order 2 for any $W$. This holds for both ROS2 variants ($\alpha_2 = 1$, $b_2 = \frac12$), and the tests observe order 2 with $W = 0$. It fails for the linearly implicit Euler method ($\sum b_i\alpha_i = 0$), which then is still order 1 only if $W = J + O(h)$.

**Theorem 4 (stability function, proved).** For $y' = \lambda y$, $z = h\lambda$, the stage equations become $k_i = zy + z\sum_{j<i}\beta_{ij}k_j + z\gamma k_i$, so $k = z(I - zB)^{-1}\mathbb{1}\,y$ with $B = (\beta_{ij})$ lower triangular with diagonal $\gamma$, and $y_{\text{new}} = R(z)y$ with $R(z) = 1 + zb^T(I - zB)^{-1}\mathbb{1} = P(z)/(1 - \gamma z)^s$, $\deg P \le s$. Order $p$ gives $R(z) = e^z + O(z^{p+1})$. For $s = 2$, $p = 2$ the numerator is $1 + (1 - 2\gamma)z + (\gamma^2 - 2\gamma + \frac12)z^2$, so $R(\infty) = 0$ exactly when $\gamma = 1 \pm 1/\sqrt2$. The stability function depends only on $\gamma$ and the order when $p = s$; for $s = 3$, $p = 3$, $\gamma = \frac12$, it is $(1 - \frac z2 - \frac{z^2}{4} + \frac{z^3}{24})/(1 - \frac z2)^3$, with $R(\infty) = -\frac13$.

**Linear invariants.** If $w^T f(t, y) = 0$ for all $(t, y)$ then $w^T J = 0$ and $w^T f_t = 0$, so multiplying the stage equation by $w^T$ gives $w^T k_i = 0$ and $w^T y_{\text{new}} = w^T y$. The Robertson test checks that $y_1 + y_2 + y_3$ stays 1 to rounding.
