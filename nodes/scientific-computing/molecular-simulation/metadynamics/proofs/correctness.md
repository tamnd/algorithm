---
title: The growth of the standard bias, the fixed shape of the well-tempered bias, and the grid
proves: [correctness]
status: full
---

Let $s$ be one collective variable, $F(s) = -\beta^{-1} \ln p(s)$ its free energy at inverse temperature $\beta = 1/(k_B T)$, and $V_n(s)$ the bias after $n$ hills. Hill $j$ is centred at $s_j$, the value of $s$ at the time of deposit, and has height $w_j$ and width $\sigma$:
$$V_n(s) = \sum_{j=1}^{n} w_j\, e^{-(s - s_j)^2 / (2\sigma^2)}, \qquad w_j = w \text{ (standard)}, \quad w_j = w\, e^{-V_{j-1}(s_j) / (k_B \Delta T)} \text{ (well-tempered)}.$$

**Claim 1 (the standard bias grows without bound).** With $w_j = w$, $\int_{-\infty}^{\infty} V_n(s)\,ds = n\, w \sigma \sqrt{2\pi}$ for every trajectory. If all centres lie in an interval $[a, b]$, then $\max_s V_n(s) \ge n\, w \sigma \sqrt{2\pi}\,(1 - \epsilon) / (b - a + 2 L \sigma)$, where $\epsilon = \mathrm{erfc}(L / \sqrt 2)$ for any $L > 0$. So $\max V_n$ grows at least linearly in $n$. Since $V_n$ is nondecreasing in $n$ at every $s$, it does not converge to a bounded function, and it does not converge in $L^1$.

*Proof.* Each Gaussian has integral $w \sigma \sqrt{2\pi}$; sum over $j$. For a centre in $[a, b]$, the mass of its Gaussian outside $[a - L\sigma, b + L\sigma]$ is at most the mass outside $[s_j - L\sigma, s_j + L\sigma]$, which is the fraction $\mathrm{erfc}(L / \sqrt 2) = \epsilon$. So the integral of $V_n$ over the interval $[a - L\sigma, b + L\sigma]$, of length $b - a + 2L\sigma$, is at least $(1 - \epsilon) n w \sigma \sqrt{2\pi}$, and the maximum is at least this integral divided by the length. $\square$

Thus in standard metadynamics $-V_n$ can follow $F$ only up to a constant that grows with $n$, and the shape keeps fluctuating at the scale of the hills; Claim 2 describes the shape, not convergence.

For Claims 2 and 3 use the quasi-static model. The bias changes so slowly that at each time the walker has the equilibrium density of $s$ under $U + V$,
$$p_V(s) = \frac{e^{-\beta (F(s) + V(s))}}{Z_V}, \qquad Z_V = \int e^{-\beta (F + V)}\,ds,$$
and the hills are narrow, so each hill adds mass $w_j \sigma \sqrt{2\pi}$ at $s_j$. Then the expected change of $V$ per hill is
$$\frac{\partial V}{\partial n}(s) = \sigma \sqrt{2\pi}\, w\, g(V(s))\, p_V(s), \qquad g(V) = 1 \text{ (standard)}, \quad g(V) = e^{-V / (k_B \Delta T)} \text{ (well-tempered)}.$$

**Claim 2 (the fixed shape).** In the quasi-static model, the rate $\partial V / \partial n$ is the same at every $s$ if and only if
$$V(s) = -\frac{\Delta T}{T + \Delta T} F(s) + c \text{ (well-tempered)}, \qquad V(s) = -F(s) + c \text{ (standard)},$$
for a constant $c$. For the well-tempered shape, $p_V(s) \propto e^{-F(s) / (k_B (T + \Delta T))}$: $s$ is sampled as if at temperature $T + \Delta T$. For the standard shape, $p_V$ is uniform.

*Proof.* The rate is uniform if and only if $\ln g(V(s)) - \beta (F(s) + V(s))$ does not depend on $s$. For the standard form this reads $F + V = \text{const}$. For the well-tempered form it reads $V / (k_B \Delta T) + \beta (F + V) = \text{const}$; multiply by $k_B T \Delta T / (T + \Delta T)$ to get $V = -\frac{\Delta T}{T + \Delta T} F + c$. Then $F + V = \frac{T}{T + \Delta T} F + c$, so $\beta (F + V) = F / (k_B (T + \Delta T)) + \beta c$, which gives the density. $\square$

As $\Delta T \to \infty$ the well-tempered shape tends to the standard one and $g \to 1$; as $\Delta T \to 0$ the factor $\Delta T / (T + \Delta T)$ tends to 0, which is no bias. Line L7 of the algorithm inverts the well-tempered shape: $F = -\frac{T + \Delta T}{\Delta T} V + \text{const}$, and $(T + \Delta T)/\Delta T = (k_B T + k_B \Delta T)/(k_B \Delta T)$, the factor of the code.

The fixed shape attracts in this model. Write $V = V^* + u$ with $V^*$ the shape of Claim 2. Then $\partial u / \partial n (s) = K\, e^{-\alpha u(s)}$ with $\alpha = \beta + 1/(k_B \Delta T) > 0$ (or $\alpha = \beta$ for the standard form) and $K > 0$ independent of $s$. So where $u$ is larger it grows more slowly, and the difference $u(s_1) - u(s_2)$ moves towards 0.

**Claim 3 (the constant grows like a logarithm).** In the quasi-static model with the well-tempered shape $V_n = V^* + c_n$, there is $B > 0$ with $dc / dn = B\, e^{-c / (k_B \Delta T)}$, so
$$c_n = k_B \Delta T \ln\bigl(e^{c_0 / (k_B \Delta T)} + B n / (k_B \Delta T)\bigr),$$
which grows like $k_B \Delta T \ln n$, and the hill heights $w\,e^{-V_n(s)/(k_B \Delta T)}$ decay like $1/n$. For the standard form $dc / dn$ is a positive constant, so $c_n$ grows linearly, as in Claim 1.

*Proof.* $Z_{V^* + c} = e^{-\beta c} Z_{V^*}$, so $p_{V^* + c} = p_{V^*}$ does not depend on $c$. Then $\partial V / \partial n = \sigma \sqrt{2\pi}\, w\, e^{-c / (k_B \Delta T)} \cdot e^{-V^*(s) / (k_B \Delta T)} p_{V^*}(s)$, and by Claim 2 the last product is a positive constant; call $B$ its product with $\sigma \sqrt{2\pi}\, w$. Solve the separable equation: $d(e^{c / (k_B \Delta T)}) / dn = B / (k_B \Delta T)$. The heights are $w\,e^{-V^*(s)/(k_B \Delta T)} e^{-c_n / (k_B \Delta T)}$, and $e^{-c_n / (k_B \Delta T)} = 1 / (e^{c_0 / (k_B \Delta T)} + B n / (k_B \Delta T))$. For the standard form, $\partial V / \partial n = \sigma \sqrt{2\pi}\, w\, p_{V^*}$ with $p_{V^*}$ uniform. $\square$

Claims 2 and 3 hold in the quasi-static model only. They explain the scale factor and the decay of the hills, but they are not a proof that the stochastic algorithm converges. Dama, Parrinello and Voth (2014) proved the convergence of the well-tempered bias; this note does not repeat that proof.

**Claim 4 (the grid).** Let the grid have nodes $s_i = lo + i\,\Delta s$, and let the code store at each node the exact value $V(s_i)$ and slope $V'(s_i)$ of the sum of hills. On each cell the code returns the cubic Hermite interpolant $H$ of these values and slopes, and its derivative $H'$ as the force. Then $H$ is continuously differentiable on $[lo, hi]$, $H'$ is exactly its derivative, and
$$|V(s) - H(s)| \le \frac{\Delta s^4}{384} \max_{\text{cell}} |V^{(4)}|.$$

*Proof.* Each deposit adds the exact value and derivative of the new Gaussian at every node, so the stored data are exact. On a cell with $t = (s - s_i)/\Delta s$, $H = h_{00}(t) V_i + h_{10}(t) \Delta s V'_i + h_{01}(t) V_{i+1} + h_{11}(t) \Delta s V'_{i+1}$ with the Hermite basis $h_{00} = (1 + 2t)(1 - t)^2$, $h_{10} = t(1 - t)^2$, $h_{01} = t^2 (3 - 2t)$, $h_{11} = t^2 (t - 1)$. Their $t$-derivatives are $6t(t - 1)$, $(1 - t)(1 - 3t)$, $-6t(t - 1)$ and $t(3t - 2)$, and the chain rule divides by $\Delta s$; these are the expressions of the code. At $t = 0$ and $t = 1$, $H$ and $H'$ equal the stored values and slopes, so neighbouring cells join with matching value and slope. The error bound is the standard remainder of cubic Hermite interpolation, $V(s) - H(s) = V^{(4)}(\xi)\, t^2 (1 - t)^2 \Delta s^4 / 24$ for some $\xi$ in the cell, with $t^2 (1 - t)^2 \le 1/16$. $\square$

For a Gaussian of width $\sigma$, $|V^{(4)}| \le 3 w / \sigma^4$ per hill, so with $\Delta s = 0.01$ and $\sigma = 0.2$ the relative error is below $10^{-7}$ per hill, which agrees with the measured $4.8 \times 10^{-8}$ on the page. Outside $[lo, hi]$ the code returns 0, so the bias is not continuous at the edge of the grid; the runs on the page stay inside it.
