---
title: Radial return solves the backward Euler equations of J2 plasticity uniquely, and line L8 is its derivative
proves: [correctness]
status: full
---

**Setting.** The data are $\kappa > 0$, $\mu > 0$, $\sigma_y > 0$, $K \ge 0$, $H \ge 0$, the state $(\varepsilon^p_n, \alpha_n, \beta_n)$ with $\varepsilon^p_n$ and $\beta_n$ symmetric and deviatoric, and the strain $\varepsilon = \varepsilon_{n+1}$. Write $r = \sqrt{2/3}$, $e = \mathrm{dev}\,\varepsilon$, $s_{\rm tr} = 2\mu(e - \varepsilon^p_n)$, $\xi_{\rm tr} = s_{\rm tr} - \beta_n$, $f_{\rm tr} = |\xi_{\rm tr}| - r(\sigma_y + K\alpha_n)$ and $c = 2\mu + \tfrac23(K + H) > 0$. The backward Euler equations are those of the section "The problem". A solution is a scalar $\Delta\gamma$ and a deviatoric unit tensor $\hat n$ that satisfy them; when $\Delta\gamma = 0$ the tensor $\hat n$ plays no role.

**Lemma 1 (reduction to one scalar).** For any $\Delta\gamma \ge 0$ and unit deviatoric $\hat n$, the equations for $\varepsilon^p_{n+1}$, $\alpha_{n+1}$, $\beta_{n+1}$ and $\sigma_{n+1}$ give

$$\xi_{n+1} = \xi_{\rm tr} - (2\mu + \tfrac23 H)\,\Delta\gamma\,\hat n, \qquad f_{n+1} = |\xi_{n+1}| - r(\sigma_y + K\alpha_n) - \tfrac23 K\,\Delta\gamma.$$

*Proof.* The deviator of $\sigma_{n+1}$ is $2\mu(e - \varepsilon^p_n - \Delta\gamma\,\hat n) = s_{\rm tr} - 2\mu\,\Delta\gamma\,\hat n$, because $\hat n$ is deviatoric. Subtract $\beta_{n+1} = \beta_n + \tfrac23 H\,\Delta\gamma\,\hat n$. For $f_{n+1}$ use $K\alpha_{n+1} = K\alpha_n + rK\,\Delta\gamma$ and $r \cdot r = \tfrac23$. $\square$

**Theorem 1 (existence and uniqueness).** The backward Euler equations with the loading conditions have exactly one solution for $(\sigma_{n+1}, \varepsilon^p_{n+1}, \alpha_{n+1}, \beta_{n+1})$. It is the output of lines L1 to L7: $\Delta\gamma = 0$ if $f_{\rm tr} \le 0$, and $\Delta\gamma = f_{\rm tr}/c$ with $\hat n = \xi_{\rm tr}/|\xi_{\rm tr}|$ if $f_{\rm tr} > 0$.

*Proof.* Case $\Delta\gamma = 0$. Then every quantity at $n + 1$ equals its trial value and $f_{n+1} = f_{\rm tr}$, so the conditions hold if and only if $f_{\rm tr} \le 0$.

Case $\Delta\gamma > 0$. The loading conditions force $f_{n+1} = 0$, so $|\xi_{n+1}| = r(\sigma_y + K\alpha_{n+1}) > 0$ and $\hat n = \xi_{n+1}/|\xi_{n+1}|$ is defined. Lemma 1 gives

$$\xi_{\rm tr} = \xi_{n+1} + (2\mu + \tfrac23 H)\,\Delta\gamma\,\frac{\xi_{n+1}}{|\xi_{n+1}|} = \Big(1 + \frac{(2\mu + \tfrac23 H)\Delta\gamma}{|\xi_{n+1}|}\Big)\,\xi_{n+1}.$$

The factor is larger than 1, so $\xi_{n+1}$ is a positive multiple of $\xi_{\rm tr}$. Hence $\xi_{\rm tr} \ne 0$, $\hat n = \xi_{\rm tr}/|\xi_{\rm tr}|$ and $|\xi_{n+1}| = |\xi_{\rm tr}| - (2\mu + \tfrac23 H)\Delta\gamma$. With Lemma 1, $f_{n+1} = f_{\rm tr} - c\,\Delta\gamma$, and $f_{n+1} = 0$ gives $\Delta\gamma = f_{\rm tr}/c$. This is positive if and only if $f_{\rm tr} > 0$.

The two cases exclude each other: if $f_{\rm tr} \le 0$ the second case has no solution, and if $f_{\rm tr} > 0$ the first case has none. In each case the solution is unique, and lines L5 to L7 compute it. Line L4 returns the first case. $\square$

**Corollary 1.** After a plastic step $f_{n+1} = 0$, the plastic strain increment is deviatoric and parallel to $\xi_{n+1}$ (normality), and the pressure is $\kappa\,\mathrm{tr}\,\varepsilon$. After an elastic step the state does not change. The reference tests check these facts on random strains.

**Theorem 2 (closest point, perfect plasticity).** Let $K = H = 0$, $R = r\sigma_y$ and $B = \{s : |s - \beta_n| \le R\}$. The deviatoric stress $s_{n+1}$ of lines L1 to L6 is the point of $B$ closest to $s_{\rm tr}$ in the Frobenius norm.

*Proof.* If $f_{\rm tr} \le 0$ then $s_{\rm tr} \in B$ and $s_{n+1} = s_{\rm tr}$. If not, $|\xi_{\rm tr}| > R$ and $s_{n+1} = \beta_n + R\,\xi_{\rm tr}/|\xi_{\rm tr}|$, since $2\mu\,\Delta\gamma = |\xi_{\rm tr}| - R$. For any $s \in B$, the triangle inequality gives $|s_{\rm tr} - s| \ge |s_{\rm tr} - \beta_n| - |s - \beta_n| \ge |\xi_{\rm tr}| - R = |s_{\rm tr} - s_{n+1}|$. Equality in the first step needs $s - \beta_n$ to be a nonnegative multiple of $\xi_{\rm tr}$, and in the second $|s - \beta_n| = R$, so the closest point is unique. $\square$

**Theorem 3 (consistent tangent).** At a strain with $f_{\rm tr} > 0$, the map $\varepsilon \mapsto \sigma_{n+1}$ is differentiable, and for symmetric increments $d\varepsilon$,

$$d\sigma_{n+1} = \big(\kappa\,I \otimes I + 2\mu\,\theta\,I_{\rm dev} - 2\mu\,\bar\theta\,\hat n \otimes \hat n\big)\,d\varepsilon, \qquad \theta = 1 - \frac{2\mu\,\Delta\gamma}{|\xi_{\rm tr}|}, \quad \bar\theta = \frac{1}{1 + (K + H)/(3\mu)} - (1 - \theta).$$

*Proof.* The set $f_{\rm tr} > 0$ is open, and there $\xi_{\rm tr} \ne 0$, so all maps below are smooth. The state at $n$ is fixed. Then $d s_{\rm tr} = 2\mu\,I_{\rm dev}\,d\varepsilon$, so $d\xi_{\rm tr} = 2\mu\,I_{\rm dev}\,d\varepsilon$. The derivative of the norm is $d|\xi_{\rm tr}| = \hat n : d\xi_{\rm tr} = 2\mu\,\hat n : d\varepsilon$, because $\hat n$ is deviatoric. So

$$d(\Delta\gamma) = \frac{2\mu}{c}\,\hat n : d\varepsilon = \frac{1}{1 + (K + H)/(3\mu)}\,\hat n : d\varepsilon.$$

The derivative of the unit tensor is $d\hat n = |\xi_{\rm tr}|^{-1}(I_{\rm dev} - \hat n \otimes \hat n)\,d\xi_{\rm tr}$ on deviatoric increments, which gives $d\hat n = \frac{2\mu}{|\xi_{\rm tr}|}(I_{\rm dev} - \hat n \otimes \hat n)\,d\varepsilon$. Line L6 is $\sigma_{n+1} = s_{\rm tr} - 2\mu\,\Delta\gamma\,\hat n + \kappa(\mathrm{tr}\,\varepsilon) I$, so

$$d\sigma_{n+1} = 2\mu\,I_{\rm dev}\,d\varepsilon - 2\mu\,\hat n\,d(\Delta\gamma) - 2\mu\,\Delta\gamma\,d\hat n + \kappa\,I\,(I : d\varepsilon).$$

Collect the terms. The coefficient of $I_{\rm dev}$ is $2\mu(1 - 2\mu\Delta\gamma/|\xi_{\rm tr}|) = 2\mu\theta$. The coefficient of $\hat n \otimes \hat n$ is $-2\mu\big(1/(1 + (K + H)/(3\mu)) - 2\mu\Delta\gamma/|\xi_{\rm tr}|\big) = -2\mu\bar\theta$. $\square$

**Remark 1 (one dimension).** The same steps with $E$ in place of $2\mu$ and without the factors $r$ and $\tfrac23$ give Theorem 1 for `return_map_1d`: $\Delta\gamma = f_{\rm tr}/(E + K + H)$ if $f_{\rm tr} > 0$. Then $d\sigma = E\,d\varepsilon - E\,\mathrm{sign}(\xi_{\rm tr})\,d(\Delta\gamma)$ with $d(\Delta\gamma) = E\,\mathrm{sign}(\xi_{\rm tr})\,d\varepsilon/(E + K + H)$, so $d\sigma/d\varepsilon = E(K + H)/(E + K + H)$, which is line L8 of the one-dimensional code.

**Remark 2 (exactness for the continuum law).** Let the continuum strain path be $\varepsilon(t)$ with $\mathrm{dev}\,\varepsilon(t) - \varepsilon^p(t) - \beta(t)/(2\mu)$ along a fixed unit tensor $\hat n$ for all $t$ in the step, and let the point stay plastic. Then the continuum flow rule $\dot\varepsilon^p = \dot\gamma\,\hat n$ integrates to $\varepsilon^p_{n+1} = \varepsilon^p_n + \Delta\gamma\,\hat n$ with $\Delta\gamma = \int\dot\gamma\,dt$, and the consistency condition at $t_{n+1}$ is the scalar equation of Theorem 1. So the backward Euler solution is the continuum solution. This covers monotone loading in one dimension and proportional loading in three. When $\hat n$ turns, the integral of $\dot\gamma\,\hat n$ is not $\Delta\gamma\,\hat n_{n+1}$, and the map has a first order error, which the reference tests measure.
