---
title: Khachiyan's algorithm returns an enclosing ellipsoid within a volume factor (1 + ε(d + 1)/d)^(d/2) of the minimum, after at most 2(1 + ε)^2 (d + 1) ln n / ε^2 steps
proves: [correctness]
status: full
---

**Setting.** $P = \{a_1, \dots, a_n\} \subset \mathbb{R}^d$ spans $\mathbb{R}^d$ affinely, and $D = d + 1$. Put $q_i = (a_i, 1) \in \mathbb{R}^D$. For $p$ in the simplex $\Delta = \{p \in \mathbb{R}^n : p \ge 0, \sum_i p_i = 1\}$ put $\Lambda(p) = \sum_i p_i q_i q_i^\top$, $c_p = \sum_i p_i a_i$, $S_p = \sum_i p_i a_i a_i^\top - c_p c_p^\top = \sum_i p_i (a_i - c_p)(a_i - c_p)^\top$, and, when $\Lambda(p)$ is invertible, $w_i(p) = q_i^\top \Lambda(p)^{-1} q_i$ and $\kappa(p) = \max_i w_i(p)$. An ellipsoid is $E(z, M) = \{x : (x - z)^\top M (x - z) \le 1\}$ with $M$ symmetric positive definite; its volume is $\omega_d \det(M)^{-1/2}$. Exact arithmetic is assumed.

**Lemma 1 (block form).** Let $L = \begin{pmatrix} I & c_p \\ 0 & 1 \end{pmatrix}$. Then $\Lambda(p) = L \begin{pmatrix} S_p & 0 \\ 0 & 1 \end{pmatrix} L^\top$. Hence $\det \Lambda(p) = \det S_p$; $\Lambda(p)$ is positive definite if and only if $S_p$ is; and then $w_i(p) = (a_i - c_p)^\top S_p^{-1} (a_i - c_p) + 1$.

*Proof.* $\Lambda(p) = \begin{pmatrix} \sum_i p_i a_i a_i^\top & c_p \\ c_p^\top & 1 \end{pmatrix}$. Multiplying out, $L \,\mathrm{diag}(S_p, 1)\, L^\top = \begin{pmatrix} S_p + c_p c_p^\top & c_p \\ c_p^\top & 1 \end{pmatrix}$, which is the same matrix. $\det L = 1$ gives the determinant, and congruence by the invertible $L$ keeps definiteness. Since $L^{-1} = \begin{pmatrix} I & -c_p \\ 0 & 1 \end{pmatrix}$, $L^{-1} q_i = (a_i - c_p, 1)$, and $w_i = (L^{-1} q_i)^\top \mathrm{diag}(S_p^{-1}, 1) (L^{-1} q_i)$ is the stated sum. $\square$

**Lemma 2 (the weighted mean of $w$).** If $\Lambda(p)$ is invertible, $\sum_i p_i w_i(p) = D$. In particular $\kappa(p) \ge D$.

*Proof.* $\sum_i p_i q_i^\top \Lambda^{-1} q_i = \mathrm{tr}\bigl(\Lambda^{-1} \sum_i p_i q_i q_i^\top\bigr) = \mathrm{tr}(I_D) = D$. A weighted mean with weights summing to 1 is at most the maximum. $\square$

**Lemma 3 (all iterates are positive definite).** At the uniform start, $\Lambda$ is positive definite and $\kappa \le n$. Every step keeps $\Lambda$ positive definite.

*Proof.* $S_p$ for uniform $p$ is $\frac{1}{n}\sum_i (a_i - c_p)(a_i - c_p)^\top$; if $u^\top S_p u = 0$ for some $u \ne 0$, then all $a_i$ lie in the hyperplane $\{x : u^\top (x - c_p) = 0\}$, which contradicts the spanning hypothesis. By Lemma 1, $\Lambda$ is positive definite. Also $\Lambda \succeq \frac{1}{n} q_i q_i^\top$, so for every $i$, $1 \ge \frac{1}{n} q_i^\top \Lambda^{-1} q_i$ (for $\Lambda \succ 0$ and a vector $v$, $\Lambda \succeq v v^\top$ is equivalent to $v^\top \Lambda^{-1} v \le 1$). So $w_i \le n$. A step with $\kappa > D$ uses $\beta = (\kappa - D)/(D(\kappa - 1))$, and $0 < \beta < 1$ because $0 < \kappa - D < D(\kappa - 1)$. Then $(1 - \beta)\Lambda + \beta q_j q_j^\top \succeq (1 - \beta)\Lambda \succ 0$. $\square$

So the loop is well defined, and $p$ stays in $\Delta$.

**Lemma 4 (containment).** At exit, with $c = c_p$, $S = S_p$ and $\kappa = \kappa(p)$, the ellipsoid $E = E(c, S^{-1}/(\kappa - 1))$ contains $P$.

*Proof.* $\kappa \ge D \ge 2$ by Lemma 2, so $\kappa - 1 > 0$. By Lemma 1, $(a_i - c)^\top S^{-1} (a_i - c) = w_i - 1 \le \kappa - 1$ for every $i$. Divide by $\kappa - 1$. (The implementation scales by $\max_i (a_i - c)^\top S^{-1} (a_i - c)$, which is $\kappa - 1$ by the same identity.) $\square$

**Lemma 5 (the lower bound).** For every $p \in \Delta$ and every ellipsoid $E(z, M) \supseteq P$, $\mathrm{vol}\, E(z, M) \ge \omega_d \det(d\, S_p)^{1/2}$.

*Proof.* For every $i$, $(a_i - z)^\top M (a_i - z) \le 1$. Multiply by $p_i$ and add:

$$1 \ge \mathrm{tr}\Bigl(M \sum_i p_i (a_i - z)(a_i - z)^\top\Bigr) = \mathrm{tr}\bigl(M (S_p + (c_p - z)(c_p - z)^\top)\bigr) \ge \mathrm{tr}(M S_p),$$

where the middle equality expands $a_i - z = (a_i - c_p) + (c_p - z)$ and uses $\sum_i p_i (a_i - c_p) = 0$, and the last step uses $(c_p - z)^\top M (c_p - z) \ge 0$. Let $\lambda_1, \dots, \lambda_d \ge 0$ be the eigenvalues of $M^{1/2} S_p M^{1/2}$. Their sum is $\mathrm{tr}(M S_p) \le 1$, so by the inequality of arithmetic and geometric means their product is at most $d^{-d}$. That product is $\det M \det S_p$. Hence $\det(M)^{-1} \ge d^d \det S_p = \det(d S_p)$, and $\mathrm{vol}\, E(z, M) = \omega_d \det(M)^{-1/2} \ge \omega_d \det(d S_p)^{1/2}$. $\square$

**Theorem 1 (the volume guarantee).** If the loop exits by the test on L5, the returned $E$ contains $P$ and

$$\frac{\mathrm{vol}(E)}{\mathrm{vol}(E^*)} \le \Bigl(\frac{\kappa - 1}{d}\Bigr)^{d/2} \le \Bigl(1 + \frac{\varepsilon (d + 1)}{d}\Bigr)^{d/2} \le (1 + \varepsilon)^{(d+1)/2},$$

where $E^*$ is the minimum volume enclosing ellipsoid.

*Proof.* Containment is Lemma 4. $\mathrm{vol}(E) = \omega_d \det(S^{-1}/(\kappa - 1))^{-1/2} = \omega_d \bigl((\kappa - 1)^d \det S\bigr)^{1/2}$. By Lemma 5 with the final $p$ and $E(z, M) = E^*$, $\mathrm{vol}(E^*) \ge \omega_d (d^d \det S)^{1/2}$. Dividing gives the first inequality. The exit test is $\kappa \le (1 + \varepsilon) D$, so $(\kappa - 1)/d \le (d + \varepsilon(d + 1))/d$, the second inequality. For the third, Bernoulli's inequality with the exponent $(d + 1)/d \ge 1$ gives $(1 + \varepsilon)^{(d+1)/d} \ge 1 + \varepsilon(d + 1)/d$; raise both sides to the power $d/2$. $\square$

**Lemma 6 (the gain of one step).** Let $\Lambda \succ 0$, $q = q_j$ with $\kappa = q^\top \Lambda^{-1} q > D$, and $g(\beta) = \log\det\bigl((1 - \beta)\Lambda + \beta q q^\top\bigr) - \log\det \Lambda$ for $0 \le \beta < 1$. Then $g$ is maximized at $\beta^\circ = (\kappa - D)/(D(\kappa - 1))$, and

$$g(\beta^\circ) = h(\kappa) = (D - 1) \log \frac{(D - 1)\kappa}{D(\kappa - 1)} + \log \frac{\kappa}{D} \ge \frac{(\kappa - D)^2}{2\kappa^2}.$$

*Proof.* By the matrix determinant lemma, $\det\bigl((1 - \beta)\Lambda + \beta q q^\top\bigr) = (1 - \beta)^D \det \Lambda \,\bigl(1 + \frac{\beta}{1 - \beta}\kappa\bigr)$, so $g(\beta) = (D - 1)\log(1 - \beta) + \log(1 + \beta(\kappa - 1))$. This is a sum of concave functions, and

$$g'(\beta) = -\frac{D - 1}{1 - \beta} + \frac{\kappa - 1}{1 + \beta(\kappa - 1)},$$

which is 0 exactly when $(\kappa - 1)(1 - \beta) = (D - 1)(1 + \beta(\kappa - 1))$, that is $\kappa - D = \beta D (\kappa - 1)$. So $\beta^\circ$ is the maximizer. At $\beta^\circ$, $1 - \beta^\circ = \frac{(D - 1)\kappa}{D(\kappa - 1)}$ and $1 + \beta^\circ(\kappa - 1) = \kappa/D$, which gives $h(\kappa)$. Now $h(D) = 0$, and differentiating,

$$h'(s) = \frac{D - 1}{s} - \frac{D - 1}{s - 1} + \frac{1}{s} = \frac{D}{s} - \frac{D - 1}{s - 1} = \frac{s - D}{s(s - 1)}.$$

For $D \le s \le \kappa$, $s(s - 1) \le s^2 \le \kappa^2$, so $h(\kappa) = \int_D^\kappa \frac{s - D}{s(s - 1)}\, ds \ge \int_D^\kappa \frac{s - D}{\kappa^2}\, ds = \frac{(\kappa - D)^2}{2\kappa^2}$. $\square$

**Lemma 7 (the duality gap).** For all $p, p' \in \Delta$ with $\Lambda(p) \succ 0$, $\log\det \Lambda(p') \le \log\det \Lambda(p) + D \log(\kappa(p)/D)$.

*Proof.* If $\Lambda(p')$ is singular the left side is $-\infty$. Otherwise, $\log\det$ is concave on positive definite matrices, with gradient $X^{-1}$ at $X$, so for every $Y \succ 0$, $\log\det Y \le \log\det X + \mathrm{tr}(X^{-1}(Y - X))$. Take $X = \Lambda(p)$ and $Y = t \Lambda(p')$ with $t > 0$:

$$D \log t + \log\det \Lambda(p') \le \log\det \Lambda(p) + t \sum_i p'_i w_i(p) - D \le \log\det\Lambda(p) + t\,\kappa(p) - D.$$

Take $t = D/\kappa(p)$: $\log\det\Lambda(p') \le \log\det\Lambda(p) + D\log(\kappa(p)/D)$. $\square$

**Theorem 2 (termination).** The loop exits after at most $\dfrac{2(1 + \varepsilon)^2 D \ln n}{\varepsilon^2}$ steps.

*Proof.* Let $p_0$ be the uniform start and $p_k$ the weights after $k$ steps. Each step runs only if $\kappa > (1 + \varepsilon) D$. Write $\kappa = D(1 + t)$ with $t > \varepsilon$. By Lemma 6 the step raises $\log\det\Lambda$ by at least $\frac{t^2}{2(1 + t)^2} > \frac{\varepsilon^2}{2(1 + \varepsilon)^2}$, because $t/(1 + t)$ increases in $t$. So after $k$ steps, $\log\det\Lambda(p_k) - \log\det\Lambda(p_0) > k \varepsilon^2/(2(1 + \varepsilon)^2)$. By Lemma 7 with $p = p_0$ and $p' = p_k$, and by Lemma 3, this difference is at most $D \log(n/D) \le D \ln n$. So $k < 2(1 + \varepsilon)^2 D \ln n/\varepsilon^2$. $\blacksquare$
