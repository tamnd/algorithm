---
title: CMA is a stochastic gradient method on the Godard cost, whose global minima for a sub-Gaussian circular alphabet are the perfect equalizers up to delay and phase
proves: [correctness]
status: full
---

The symbols $a[n]$ are independent and identically distributed, with $E a = 0$, $E a^2 = 0$ (circular), $E|a|^2 = 1$ and $\kappa = E|a|^4$. There is no noise. The channel $h$ and the taps $c$ have finite length, and the combined response is $g = c * h$, so the output is $z[n] = \sum_i c_i\, y[n-i] = \sum_k g_k\, a[n-k]$. The dispersion constant is $R_2 = E|a|^4 / E|a|^2 = \kappa$. The cost is $J = E(|z|^2 - R_2)^2$, and $J(g)$ means the cost as a function of the combined response.

**Lemma 1 (fourth moment).** $E|z|^2 = s$ and $E|z|^4 = 2 s^2 + (\kappa - 2) \sum_k |g_k|^4$, where $s = \sum_k |g_k|^2$.

*Proof.* $E|z|^2 = \sum_{k, l} g_k \bar g_l\, E[a_k \bar a_l] = \sum_k |g_k|^2$, with $a_k = a[n-k]$. For the fourth moment,
$$E|z|^4 = \sum_{i, j, k, l} g_i g_j \bar g_k \bar g_l\, E[a_i a_j \bar a_k \bar a_l].$$
If one index value appears exactly once among $i, j, k, l$, the expectation is a product with a factor $E a = 0$ or $E \bar a = 0$, by independence. So each index value appears at least twice. Either all four are equal, which gives $\kappa |g_i|^4$, or there are two distinct values, each twice. The pairing $i = j \ne k = l$ gives $E a_i^2\, E \bar a_k^2 = 0$, because the alphabet is circular. The pairings $i = k \ne j = l$ and $i = l \ne j = k$ each give $|g_i|^2 |g_j|^2$. So
$$E|z|^4 = \kappa \sum_i |g_i|^4 + 2 \sum_{i \ne j} |g_i|^2 |g_j|^2 = \kappa \sum_i |g_i|^4 + 2\left(s^2 - \sum_i |g_i|^4\right). \qquad \square$$

**Theorem 1 (the cost).** $J(g) = 2 s^2 + (\kappa - 2) \sum_k |g_k|^4 - 2\kappa s + \kappa^2$.

*Proof.* $J = E|z|^4 - 2 R_2 E|z|^2 + R_2^2$ with $R_2 = \kappa$, and Lemma 1. $\square$

For unit-energy 16-QAM, the raw points have $E|a|^2 = 10$ and $E|a|^4 = 132$, so $\kappa = 132/100 = 1.32$. For every PSK alphabet, $|a| = 1$ and $\kappa = 1$.

**Theorem 2 (global minima).** If $0 < \kappa < 2$, then $J(g) \ge \kappa(\kappa - 1)$ for every $g$, with equality if and only if $g = e^{j\theta} e_d$ for some delay $d$ and phase $\theta$.

*Proof.* $\sum_k |g_k|^4 \le (\sum_k |g_k|^2)^2 = s^2$, because the cross terms $|g_i|^2 |g_j|^2$ are not negative. Equality holds if and only if at most one $g_k$ is nonzero. Since $\kappa - 2 < 0$,
$$J(g) \ge 2 s^2 + (\kappa - 2) s^2 - 2\kappa s + \kappa^2 = \kappa (s - 1)^2 + \kappa(\kappa - 1) \ge \kappa(\kappa - 1).$$
Equality in the first step needs at most one nonzero tap, and in the second step $s = 1$. So equality holds exactly when $g$ has one tap of modulus 1. Conversely, $g = e^{j\theta} e_d$ has $s = 1$ and $\sum |g_k|^4 = 1$, so $J = 2 + \kappa - 2 - 2\kappa + \kappa^2 = \kappa(\kappa - 1)$. $\square$

If $\kappa > 2$ (a super-Gaussian alphabet), the inequality goes the other way, and spreading $g$ over many taps lowers $J$, so CMA does not equalize. If $\kappa = 2$, which is the value for a circular Gaussian, $J$ depends only on $s$, and no blind method based on this cost can find the channel.

**Lemma 2 (the update is a stochastic gradient).** For a fixed regressor $u$ and $z = \sum_i c_i u_i$, the Wirtinger derivative of $(|z|^2 - R_2)^2$ with respect to $\bar c_i$ is $2 (|z|^2 - R_2)\, z\, \bar u_i$. So line L6 moves $c$ by $-(\mu/2)$ times this derivative, and its expected direction, over the symbols and the noise, is $-(\mu/2)$ times the gradient of $J$ with respect to $\bar c$.

*Proof.* $|z|^2 = z \bar z$, with $\partial z / \partial \bar c_i = 0$ and $\partial \bar z / \partial \bar c_i = \bar u_i$. So $\partial |z|^2 / \partial \bar c_i = z \bar u_i$ and the chain rule gives the result. The expectation and the derivative commute because the cost is a polynomial in $c$ with finite moments. $\square$

For a small $\mu$, stochastic approximation theory says that the taps follow the gradient flow of $J$ near a stable stationary point. This page does not prove that step. It also does not claim that the flow reaches the global minimum. For a finite equalizer, the set of reachable combined responses $\{c * h\}$ is a subspace that need not contain any $e_d$, and $J$ restricted to it can have local minima with a large residual ISI. The test `test_a_finite_equalizer_has_a_worse_local_minimum` finds one for $h = (1, 0.5)$ and two taps.

**Theorem 3 (rotation).** Run lines L1 to L7 on $y$ and on $y' = e^{j\varphi} y$ with the same $N$, $\mu$ and $R_2$. Then the taps are equal at every step, and $z'[k] = e^{j\varphi} z[k]$.

*Proof.* By induction on $k$. Both runs start from the same spike (line L1). If $c' = c$ before step $k$, then $u' = e^{j\varphi} u$, so $z' = e^{j\varphi} z$ (line L4), $|z'| = |z|$, and $e' = e^{j\varphi} e$ (line L5). The update of line L6 adds $-\mu e' \bar u'_i = -\mu e^{j\varphi} e\, e^{-j\varphi} \bar u_i = -\mu e \bar u_i$, the same as in the first run. $\square$

So CMA cannot remove a carrier phase rotation, and by Theorem 2 it does not need to: every phase gives the same minimum cost.

**Remark on noise.** With noise $w \sim \mathcal{CN}(0, N_0)$, the output has an extra Gaussian term, and the minimizers of $J$ move away from $e^{j\theta} e_d$. They no longer give zero ISI, as the MMSE equalizer does not. Theorem 2 is a statement about the noiseless cost.
