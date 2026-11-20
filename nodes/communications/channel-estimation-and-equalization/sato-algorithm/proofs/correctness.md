---
title: The Sato error is a stochastic gradient of a fixed cost, the perfect equalizer is a stationary point of the mean update, and the update is equivariant under a sign flip and under rotations by 90 degrees
proves: [correctness]
status: full
---

The symbols $a[n]$ are independent and identically distributed. For PAM they are real with a symmetric distribution, $E a = 0$, and $P(a = 0) = 0$. There is no noise. The combined response is $g = c * h$, so the equalizer output is $z[n] = \sum_k g_k\, a[n-k]$. The constant is $\gamma = E a^2 / E|a|$. The regressor of line L3 is $u = (y[k], \ldots, y[k-N+1])$, and line L6 adds $-\mu e\, \bar u_i$ to $c_i$, with $e = z - \gamma\, \mathrm{csgn}(z)$ from line L5.

**Lemma 1 (the error is a gradient).** Let $\phi(z) = |z|^2 / 2 - \gamma (|\mathrm{Re}\, z| + |\mathrm{Im}\, z|)$. At every $z$ with $\mathrm{Re}\, z \ne 0$ and $\mathrm{Im}\, z \ne 0$, the Wirtinger derivative is $\partial \phi / \partial \bar z = e / 2$. For a fixed $u$ and $z = \sum_i c_i u_i$, the derivative of $\phi(z)$ with respect to $\bar c_i$ is $(e/2)\, \bar u_i$.

*Proof.* Write $z = x + j y$. Then $\partial \phi / \partial x = x - \gamma\, \mathrm{sgn}(x)$ and $\partial \phi / \partial y = y - \gamma\, \mathrm{sgn}(y)$. The Wirtinger derivative is $\frac12 (\partial_x + j \partial_y)\phi = \frac12 (z - \gamma\, \mathrm{csgn}(z)) = e/2$. Since $\partial z / \partial \bar c_i = 0$ and $\partial \bar z / \partial \bar c_i = \bar u_i$, the chain rule gives $(\partial \phi / \partial \bar z)\, \bar u_i = (e/2)\, \bar u_i$. $\square$

So line L6 moves $c$ by $-2\mu$ times the derivative of $\phi(z)$ with respect to $\bar c$. For real PAM, $\phi(z) = z^2/2 - \gamma |z|$, and the expected direction of the update is the negative gradient of $J(c) = E[z^2/2 - \gamma |z|]$. The set where $z$ lies on an axis has probability zero when the input has a continuous part, for example noise, and for discrete inputs line L5 uses $\mathrm{sgn}(0) = 0$ there.

**Theorem 1 (the perfect equalizer is stationary).** Let $a$ be real PAM, as above, and let $g = \beta e_d$ with $\beta \ne 0$. Then $E[e\, a[n-j]] = 0$ for all $j \ne d$, and $E[e\, a[n-d]] = (|\beta| - 1)\, \mathrm{sgn}(\beta)\, E a^2$. So the mean update $-\mu E[e\, \bar u]$ is zero if and only if $\beta = \pm 1$.

*Proof.* With $g = \beta e_d$, $z = \beta a[n-d]$, so $\mathrm{sgn}(z) = \mathrm{sgn}(\beta)\, \mathrm{sgn}(a[n-d])$ and
$$e = \beta a[n-d] - \gamma\, \mathrm{sgn}(\beta)\, \mathrm{sgn}(a[n-d]).$$
This is a function of $a[n-d]$ only. For $j \ne d$, $a[n-j]$ is independent of it and has mean zero, so $E[e\, a[n-j]] = 0$. For $j = d$, write $a = a[n-d]$:
$$E[e\, a] = \beta E a^2 - \gamma\, \mathrm{sgn}(\beta)\, E|a| = \beta E a^2 - \mathrm{sgn}(\beta)\, E a^2 = \mathrm{sgn}(\beta)(|\beta| - 1) E a^2,$$
using $\gamma E|a| = E a^2$. Now $u_i = y[k-i] = \sum_l h_l\, a[k-i-l]$, so $E[e\, \bar u_i] = \sum_l \bar h_l\, E[e\, a[k-i-l]]$. If $\beta = \pm 1$, every term is zero. If $|\beta| \ne 1$, only the term with $k - i - l = n - d$ survives, and the vector $E[e\, \bar u]$ is a nonzero multiple of the column of the channel convolution matrix that maps $c$ to $g_d$. That column is not zero, because $g_d = \beta \ne 0$ is reachable. $\square$

For raw 4-PAM, $E a^2 = 5$ and $E|a| = 2$, so $\gamma = 5/2$. With $\beta = 9/10$, Theorem 1 gives $E[e\, a] = -\frac{1}{10} \cdot 5 = -\frac12$. The test `test_the_perfect_equalizer_is_a_stationary_point` checks this with exact fractions, and checks that a residual tap of $1/5$ is not stationary.

If line L5 uses a value $\gamma'$ in place of $\gamma$, the same computation gives the stationary gain $|\beta| = \gamma' E|a| / E a^2 = \gamma' / \gamma$. This is the scale error of the first pitfall on the page.

**What is not proved.** Theorem 1 says that the perfect equalizers are stationary. It does not say that they are the only stationary points, or that the iteration reaches one. Benveniste, Goursat and Ruget (1980) proved convergence for an equalizer of unbounded length under conditions on the input distribution. For a finite equalizer this page makes no convergence claim. The example on the page is a measurement.

**Theorem 2 (sign flip).** Run lines L1 to L7 on $y$ and on $-y$ with the same $N$, $\mu$, $\gamma$ and spike. Then the taps are equal at every step and the outputs are negated.

*Proof.* By induction on $k$. Both runs start from the same spike. If $c' = c$, then $u' = -u$, $z' = -z$, $\mathrm{csgn}(z') = -\mathrm{csgn}(z)$ and $e' = -e$. The update adds $-\mu e' \bar u'_i = -\mu e \bar u_i$, the same as in the first run. $\square$

**Theorem 3 (rotation by 90 degrees).** Run lines L1 to L7 on $y$ and on $j y$. Then the taps are equal at every step, and $z' = j z$.

*Proof.* Multiplying by $j$ maps $x + jy$ to $-y + jx$, so $\mathrm{csgn}(j z) = -\mathrm{sgn}(y) + j\, \mathrm{sgn}(x) = j\, \mathrm{csgn}(z)$. With $c' = c$, $u' = j u$, $z' = j z$ and $e' = j e$. The update adds $-\mu e' \bar u'_i = -\mu (j e)(-j \bar u_i) = -\mu e \bar u_i$. $\square$

For a rotation $e^{j\varphi}$ that is not a multiple of 90 degrees, $\mathrm{csgn}(e^{j\varphi} z) \ne e^{j\varphi}\, \mathrm{csgn}(z)$ in general, so the runs differ. This is why the QAM form, unlike CMA, can remove a carrier phase, but only up to a multiple of 90 degrees, which is the symmetry of square QAM. The test `test_qam_form_removes_a_carrier_phase_up_to_90_degrees` measures this for rotations of 25 and 70 degrees.
