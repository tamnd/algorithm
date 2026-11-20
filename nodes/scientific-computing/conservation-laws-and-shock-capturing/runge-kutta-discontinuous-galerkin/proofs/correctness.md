---
title: RKDG with the minmod limiter is conservative, and its cell means are TVD and bounded under a CFL condition
proves: [correctness, termination]
status: full
---

**Setting.** The grid is periodic with $M$ cells of width $\Delta x$, $\lambda = \Delta t/\Delta x$, and $u_h = \sum_{l=0}^k U_{j,l}P_l(\xi)$ on cell $j$ with mean $\bar u_j = U_{j,0}$. The flux $\hat F(a, b)$ is consistent, nondecreasing in $a$ with Lipschitz constant $L_1$, and nonincreasing in $b$ with Lipschitz constant $L_2$. Write $\Delta_{j+1/2} = \bar u_{j+1} - \bar u_j$, $u^-_{j+1/2} = \bar u_j + \tilde u_j$ and $u^+_{j-1/2} = \bar u_j - \tilde{\tilde u}_j$, with the deviations of the main page. LIMIT is lines L5 to L8 with the TVB constant $M_{\text{TVB}} = 0$, so $\tilde m = m$.

**Lemma 1 (the limiter keeps the means).** LIMIT does not change any $U_{j,0}$.

*Proof.* L7 keeps the cell, and L8 changes only $U_{j,l}$ with $l \ge 1$. $\square$

**Lemma 2 (conservation).** With or without the limiter, $\sum_j \bar u_j$ is the same after every stage and every step.

*Proof.* The $l = 0$ row of the DG operator is $-(\hat F_{j+1/2} - \hat F_{j-1/2})/\Delta x$, which sums to zero over a periodic grid. Each stage in L2 to L4 is a linear combination of $U$ and of operator values with coefficients that do not depend on $j$, so it keeps $\sum_j \bar u_j$. By Lemma 1, so does LIMIT. $\square$

**Lemma 3 (limited deviations).** After LIMIT, for every cell $j$ there are numbers $\alpha_j, \beta_j, \gamma_j, \delta_j \in [0, 1]$ with

$$\tilde u_j = \alpha_j\Delta_{j+1/2} = \beta_j\Delta_{j-1/2}, \qquad \tilde{\tilde u}_j = \gamma_j\Delta_{j+1/2} = \delta_j\Delta_{j-1/2},$$

where a coefficient may be taken as $0$ when the difference it multiplies is $0$.

*Proof.* Say $d$ is admissible for cell $j$ if $d = m(d, \Delta_{j+1/2}, \Delta_{j-1/2})$. Then either $d = 0$, or $d$ has the sign of both differences and $|d| \le \min(|\Delta_{j+1/2}|, |\Delta_{j-1/2}|)$. In both cases $d$ is a multiple in $[0, 1]$ of each difference (if a difference is $0$, then $m$ returns $0$ and $d = 0$). If the cell passes L7, both deviations are admissible by the test. If not, L8 makes the cell linear with slope $s = m(U_{j,1}, \Delta_{j+1/2}, \Delta_{j-1/2})$. Then $\tilde u_j = \tilde{\tilde u}_j = s$, and $s$ is admissible because $m(s, \Delta_{j+1/2}, \Delta_{j-1/2}) = s$ when $s$ already has the sign and the bound. The means do not change (Lemma 1), so the differences used are those of the limited data. $\square$

**Lemma 4 (Harten's form).** Let $u_h$ be limited and let $\bar u^{\text{new}}_j = \bar u_j - \lambda(\hat F_{j+1/2} - \hat F_{j-1/2})$ be one forward Euler step of the means. Then

$$\bar u^{\text{new}}_j = \bar u_j + C_j\Delta_{j+1/2} - D_j\Delta_{j-1/2}, \qquad 0 \le C_j \le 2\lambda L_2, \quad 0 \le D_j \le 2\lambda L_1.$$

*Proof.* Add and subtract $\hat F(u^-_{j+1/2}, u^+_{j-1/2})$:

$$\bar u^{\text{new}}_j - \bar u_j = -\lambda\big[\hat F(u^-_{j+1/2}, u^+_{j+1/2}) - \hat F(u^-_{j+1/2}, u^+_{j-1/2})\big] - \lambda\big[\hat F(u^-_{j+1/2}, u^+_{j-1/2}) - \hat F(u^-_{j-1/2}, u^+_{j-1/2})\big].$$

In the first bracket only the second argument changes, by $u^+_{j+1/2} - u^+_{j-1/2} = \Delta_{j+1/2} - \tilde{\tilde u}_{j+1} + \tilde{\tilde u}_j = (1 - \delta_{j+1} + \gamma_j)\Delta_{j+1/2}$, using Lemma 3 and $\Delta_{(j+1)-1/2} = \Delta_{j+1/2}$. The factor $1 - \delta_{j+1} + \gamma_j$ lies in $[0, 2]$. Because $\hat F$ is nonincreasing in $b$ with constant $L_2$, the first term is $C_j\Delta_{j+1/2}$ with $C_j = \lambda\theta(1 - \delta_{j+1} + \gamma_j)$ for some $\theta \in [0, L_2]$ (take $C_j = 0$ when the change is $0$). So $0 \le C_j \le 2\lambda L_2$. In the second bracket only the first argument changes, by $u^-_{j+1/2} - u^-_{j-1/2} = \Delta_{j-1/2} + \tilde u_j - \tilde u_{j-1} = (1 + \beta_j - \alpha_{j-1})\Delta_{j-1/2}$, with a factor in $[0, 2]$. Because $\hat F$ is nondecreasing in $a$ with constant $L_1$, the second term is $-D_j\Delta_{j-1/2}$ with $0 \le D_j \le 2\lambda L_1$. $\square$

**Theorem (TVDM and maximum principle).** If $\lambda(L_1 + L_2) \le \tfrac12$, then one step of RKDG with $M_{\text{TVB}} = 0$ gives $\sum_j|\Delta^{\text{new}}_{j+1/2}| \le \sum_j|\Delta_{j+1/2}|$ and $\min_i \bar u_i \le \bar u^{\text{new}}_j \le \max_i \bar u_i$.

*Proof.* First one forward Euler step of limited data. By Lemma 4, $C_j + D_{j+1} \le 2\lambda(L_1 + L_2) \le 1$ and $C_j + D_j \le 1$. For the maximum principle, $\bar u^{\text{new}}_j = (1 - C_j - D_j)\bar u_j + C_j\bar u_{j+1} + D_j\bar u_{j-1}$ is a convex combination. For the total variation,

$$\Delta^{\text{new}}_{j+1/2} = (1 - C_j - D_{j+1})\Delta_{j+1/2} + C_{j+1}\Delta_{j+3/2} + D_j\Delta_{j-1/2}.$$

All three coefficients are nonnegative. Take absolute values, sum over $j$ and shift the indices of the last two sums on the periodic grid: the coefficients of each $|\Delta_{j+1/2}|$ add to $(1 - C_j - D_{j+1}) + C_j + D_{j+1} = 1$. So the total variation of the means does not grow.

Now the Runge-Kutta step. Stage L2 is a forward Euler step of limited data followed by LIMIT, which keeps the means, so its means satisfy both properties relative to $U$. Stage L3 gives means $\tfrac34\bar u + \tfrac14\bar w$, where $\bar w$ are the means of a forward Euler step from the limited $U^1$. The total variation is a seminorm, so it is convex: $TV(\tfrac34\bar u + \tfrac14\bar w) \le \tfrac34 TV(\bar u) + \tfrac14 TV(\bar w) \le TV(\bar u)$. A convex combination of values in $[\min\bar u, \max\bar u]$ also stays in it. Stage L4 is the same with weights $\tfrac13$ and $\tfrac23$. The limiter after each stage keeps the means, so the bounds pass to the next stage. $\square$

For Godunov's flux on data in $[a, b]$, $L_1, L_2 \le \max_{[a,b]}|f'|$, so the condition holds when $\lambda\max|f'| \le \tfrac14$. The tests use $\lambda\max|f'| = 0.15$ and check both properties at every step of a shock and rarefaction problem.

**What is cited.** With $M_{\text{TVB}} > 0$ the limiter can leave a cell with a deviation of size up to $M_{\text{TVB}}\Delta x^2$, which adds at most $O(M_{\text{TVB}}\Delta x)$ to the total variation per unit time; this gives the TVBM bound, compactness and convergence of a subsequence to a weak solution (Cockburn and Shu 1989). The order $k + 1$ for smooth solutions with a large enough $M_{\text{TVB}}$ is measured on the main page, not proved.

**Termination.** The loop L1 runs $\lceil T/\Delta t\rceil$ steps with the last one shortened. Each step makes three operator evaluations and three passes of LIMIT, each a fixed number of operations per cell. $\blacksquare$
