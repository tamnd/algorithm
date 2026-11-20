---
tag: 9JKSFD
kind: theorem
slug: mlmc-complexity-theorem
name: Multilevel Monte Carlo complexity theorem
aliases:
- Giles complexity theorem
area: scientific-computing/uncertainty-quantification
level: advanced
summary: Gives the cost of MLMC for root mean square error eps as eps^-2, eps^-2 (log eps)^2 or more, from the rates of variance decay and cost growth.
prereqs: [multilevel-monte-carlo]
see_also: [multilevel-monte-carlo, monte-carlo-integration, mean-squared-error, euler-maruyama-method, milstein-method, multifidelity-monte-carlo, central-limit-theorem, lagrange-multiplier]
sources:
  - paper: doi:10.1017/S096249291500001X
    title: Michael B. Giles, Multilevel Monte Carlo methods, Acta Numerica 24, 2015, 259-328
    locator: Section 2.1, Theorem 1 and its proof, and the discussion of the three cases; Section 5.1 for Euler-Maruyama paths
  - paper: doi:10.1287/opre.1070.0496
    title: Michael B. Giles, Multilevel Monte Carlo path simulation, Operations Research 56(3), 2008, 607-617
    locator: Theorem 3.1, the first form of the theorem
  - paper: doi:10.1007/s00791-011-0160-x
    title: K. Andrew Cliffe, Michael B. Giles, Robert Scheichl and Aretha L. Teckentrup, Multilevel Monte Carlo methods and applications to elliptic PDEs with random coefficients, Computing and Visualization in Science 14, 2011, 3-15
    locator: the theorem with general rates alpha, beta and gamma
  - paper: "Jakob Creutzig, Steffen Dereich, Thomas Müller-Gronbach and Klaus Ritter, Infinite-dimensional quadrature and approximation of distributions, Foundations of Computational Mathematics 9(4), 2009, 391-429"
    locator: the lower bound of order eps^-2 for SDE quadrature and the near optimality of the multilevel method for Lipschitz path functionals
---

## Statement

Let $P$ be a random variable and $P_0, P_1, \ldots$ approximations of it on levels $l = 0, 1, \ldots$. Let $Y_l = P_l - P_{l-1}$ with $P_{-1} = 0$, let $\widehat{Y}_l$ be the mean of $N_l$ independent samples of $Y_l$, with the samples of different levels independent, and let $\widehat{Y} = \sum_{l=0}^{L} \widehat{Y}_l$. Let $C_l$ be the expected cost of one sample of $Y_l$ and $V_l = \mathrm{Var}(Y_l)$.

**Theorem (Giles).** Suppose there are positive constants $\alpha, \beta, \gamma, c_1, c_2, c_3$ with $\alpha \ge \frac{1}{2}\min(\beta, \gamma)$ such that for all $l \ge 0$

1. $|\mathbb{E}[P_l - P]| \le c_1 2^{-\alpha l}$,
2. $V_l \le c_2 2^{-\beta l}$,
3. $C_l \le c_3 2^{\gamma l}$.

Then there is a constant $c_4$ such that for every $\varepsilon < e^{-1}$ there are a level $L$ and counts $N_0, \ldots, N_L$ for which the mean squared error $\mathbb{E}[(\widehat{Y} - \mathbb{E}[P])^2]$ is at most $\varepsilon^2$ and the expected cost $C = \sum_{l=0}^{L} N_l C_l$ satisfies

$$C \le \begin{cases} c_4\, \varepsilon^{-2}, & \beta > \gamma, \\ c_4\, \varepsilon^{-2} (\log \varepsilon)^2, & \beta = \gamma, \\ c_4\, \varepsilon^{-2 - (\gamma - \beta)/\alpha}, & \beta < \gamma. \end{cases}$$

The rate $\alpha$ is the weak rate of the bias, $\beta$ the rate of the variance of the corrections and $\gamma$ the rate of the cost growth. The theorem says that good choices exist; the [multilevel Monte Carlo](/multilevel-monte-carlo/) algorithm makes the choices of the proof from estimated $V_l$ and $C_l$.

## In plain words

The multilevel method mixes many cheap coarse samples with few expensive fine ones. This theorem says how much the whole mix costs for a given accuracy. Three numbers decide it: how fast the error of the levels falls, how fast the spread of the corrections falls, and how fast the cost of one sample grows from level to level.

If the spread falls faster than the cost grows, almost all the work is on the coarse levels, and the total is the same as if every sample were cheap and exact. If the two match, every level costs about the same, and there is a small extra factor for the number of levels. If the cost grows faster, the finest level dominates, but the total is still much less than with the finest level alone.

## Proof

We follow Giles 2015. All logarithms are natural logarithms, and $\varepsilon < e^{-1}$ gives $\log(\varepsilon^{-1}) > 1$. The mean squared error splits into a variance and a squared bias,

$$\mathbb{E}[(\widehat{Y} - \mathbb{E}[P])^2] = \sum_{l=0}^{L} \frac{V_l}{N_l} + \big(\mathbb{E}[P_L] - \mathbb{E}[P]\big)^2,$$

because $\mathbb{E}[\widehat{Y}] = \mathbb{E}[P_L]$ by the telescoping sum and the samples are independent (see the proof page of [multilevel Monte Carlo](/multilevel-monte-carlo/)). We make each part at most $\varepsilon^2/2$.

**Step 1 (the level).** Let $L = \big\lceil \alpha^{-1} \log_2(\sqrt{2}\, c_1 \varepsilon^{-1}) \big\rceil$. Then $c_1 2^{-\alpha L} \le \varepsilon/\sqrt{2}$, so the squared bias is at most $\varepsilon^2/2$ by hypothesis 1. Also $L < \alpha^{-1}\log_2(\sqrt{2}\, c_1 \varepsilon^{-1}) + 1$, which gives

$$2^{\alpha L} < 2^{\alpha} \sqrt{2}\, c_1 \varepsilon^{-1} \qquad \text{and} \qquad L + 1 \le c_5 \log(\varepsilon^{-1}) \tag{1}$$

for a constant $c_5$; the second bound uses $\log(\varepsilon^{-1}) > 1$ to absorb the constant terms. From the first bound, $2^{\theta L} < (2^\alpha \sqrt{2}\, c_1)^{\theta/\alpha} \varepsilon^{-\theta/\alpha}$ for every $\theta > 0$.

**Step 2 (the counts).** Let $S = \sum_{l=0}^{L} \sqrt{V_l C_l}$ and $N_l = \big\lceil 2 \varepsilon^{-2} \sqrt{V_l / C_l}\, S \big\rceil$. Then

$$\sum_{l=0}^{L} \frac{V_l}{N_l} \le \sum_{l=0}^{L} \frac{\varepsilon^2 V_l}{2 S \sqrt{V_l / C_l}} = \frac{\varepsilon^2}{2S} \sum_{l=0}^{L} \sqrt{V_l C_l} = \frac{\varepsilon^2}{2},$$

so the mean squared error is at most $\varepsilon^2$. These counts are the minimizers of the cost under the variance constraint, found by a [Lagrange multiplier](/lagrange-multiplier/), rounded up. Since $N_l < 2 \varepsilon^{-2} \sqrt{V_l / C_l}\, S + 1$,

$$C = \sum_{l=0}^{L} N_l C_l < 2 \varepsilon^{-2} S^2 + \sum_{l=0}^{L} C_l. \tag{2}$$

**Step 3 (the rounding term).** By hypothesis 3, $\sum_{l=0}^{L} C_l \le c_3 \sum_{l=0}^{L} 2^{\gamma l} < c_3\, 2^{\gamma L} / (1 - 2^{-\gamma})$, and by (1) this is at most a constant times $\varepsilon^{-\gamma/\alpha}$. The condition $\alpha \ge \frac{1}{2}\min(\beta, \gamma)$ bounds this term in each case. If $\beta \ge \gamma$, it gives $\gamma/\alpha \le 2$, so the term is $O(\varepsilon^{-2})$. If $\beta < \gamma$, it gives $\beta/\alpha \le 2$, so $\gamma/\alpha = \beta/\alpha + (\gamma - \beta)/\alpha \le 2 + (\gamma - \beta)/\alpha$, and the term is $O(\varepsilon^{-2 - (\gamma - \beta)/\alpha})$. In both cases it is within the claimed bound (for $\beta = \gamma$ because $\varepsilon^{-2} \le \varepsilon^{-2} (\log \varepsilon)^2$).

**Step 4 (the main term).** By hypotheses 2 and 3, $\sqrt{V_l C_l} \le \sqrt{c_2 c_3}\, 2^{(\gamma - \beta) l / 2}$.

- If $\beta > \gamma$, the sum is bounded by a geometric series: $S \le \sqrt{c_2 c_3} / (1 - 2^{-(\beta - \gamma)/2})$, a constant. So $2 \varepsilon^{-2} S^2 = O(\varepsilon^{-2})$.
- If $\beta = \gamma$, each term is at most $\sqrt{c_2 c_3}$, so $S \le \sqrt{c_2 c_3}\,(L + 1) \le \sqrt{c_2 c_3}\, c_5 \log(\varepsilon^{-1})$ by (1). So $2 \varepsilon^{-2} S^2 \le 2 c_2 c_3 c_5^2\, \varepsilon^{-2} (\log \varepsilon)^2$.
- If $\beta < \gamma$, the sum is dominated by its last term: $S \le \sqrt{c_2 c_3}\, 2^{(\gamma - \beta) L / 2} / (1 - 2^{-(\gamma - \beta)/2})$. So $S^2$ is at most a constant times $2^{(\gamma - \beta) L}$, which by (1) is at most a constant times $\varepsilon^{-(\gamma - \beta)/\alpha}$, and $2 \varepsilon^{-2} S^2 = O(\varepsilon^{-2 - (\gamma - \beta)/\alpha})$.

Adding Step 3 and Step 4 in (2) and taking $c_4$ as the largest of the constants gives the three bounds. $\blacksquare$

The proof shows where the work is. If $\beta > \gamma$, the terms $\sqrt{V_l C_l}$ fall geometrically, and most of the cost is on the coarsest levels. If $\beta < \gamma$, they grow geometrically, and most of the cost is on the finest levels, where one sample costs $C_L = O(\varepsilon^{-\gamma/\alpha})$. If $\beta = \gamma$, the cost is spread evenly over the $L + 1 = O(\log \varepsilon^{-1})$ levels, and the factor $(\log \varepsilon)^2$ is $(L + 1)^2$.

## Consequences

- **Euler-Maruyama paths.** For an SDE with smooth coefficients and a Lipschitz output of the final value, the [Euler-Maruyama method](/euler-maruyama-method/) with $h_l = 2^{-l} h_0$ has weak order 1 and strong order 1/2, so $\alpha = 1$ and $V_l = O(h_l)$, $\beta = 1$; the cost per sample is $\gamma = 1$. The theorem gives $O(\varepsilon^{-2} (\log \varepsilon)^2)$. Plain [Monte Carlo integration](/monte-carlo-integration/) on one level needs $O(\varepsilon^{-2})$ samples with $O(\varepsilon^{-1})$ steps, which is $O(\varepsilon^{-3})$. With $h_l = 4^{-l} h_0$, as in Giles 2008, all three rates are 2 and the order is the same.
- **Milstein paths.** With the [Milstein method](/milstein-method/) in one dimension, the strong order is 1, so $\beta = 2 > \gamma = 1$ and the cost is $O(\varepsilon^{-2})$, the order of Monte Carlo with exact samples of unit cost.
- **Plain Monte Carlo as one level.** Plain Monte Carlo on level $L$ costs $O(\varepsilon^{-2} C_L) = O(\varepsilon^{-2 - \gamma/\alpha})$. In the case $\beta < \gamma$, MLMC saves the factor $\varepsilon^{-\beta/\alpha}$.
- **The condition on alpha.** Giles notes that if hypothesis 2 is tightened to a bound on $\mathbb{E}[Y_l^2]$, which is the quantity that numerical analysis usually bounds, then $\alpha \ge \beta/2$ follows, because $|\mathbb{E}[Y_l]| \le \sqrt{\mathbb{E}[Y_l^2]}$ and the bias is a sum of the $\mathbb{E}[Y_l]$.
- **Rule of thumb (heuristic, not part of the theorem).** In a run, plot $\log_2 V_l$, $\log_2 |\widehat{Y}_l|$ and $\log_2 C_l$ against $l$ to read the rates. If the plotted $V_l C_l$ grows, the finest levels dominate, and it pays to improve the coupling before anything else.

## Tightness

- **The rounding condition is needed.** Without $\alpha \ge \frac{1}{2}\min(\beta, \gamma)$, one sample on each level already costs about $C_L \approx 2^{\gamma L}$, which is of order $\varepsilon^{-\gamma/\alpha}$. For example, with $\beta > \gamma$ and $\alpha < \gamma/2$, this exceeds $\varepsilon^{-2}$, so the first bound fails.
- **The bounds are attained by the method.** If $V_l = c_2 2^{-\beta l}$ and $C_l = c_3 2^{\gamma l}$ hold with equality and the bias is exactly $c_1 2^{-\alpha L}$, then $L$ must be at least $\alpha^{-1}\log_2(\sqrt{2}\, c_1 \varepsilon^{-1})$, and by the Cauchy-Schwarz bound every choice of counts with variance at most $\varepsilon^2/2$ costs at least $2 \varepsilon^{-2} S^2$. For $\beta = \gamma$ this is of order $\varepsilon^{-2} L^2$, so the factor $(\log \varepsilon)^2$ cannot be removed for the multilevel estimator with these levels.
- **Near the lower bound for SDEs.** Creutzig, Dereich, Müller-Gronbach and Ritter proved in 2009 a lower bound of order $\varepsilon^{-2}$ for the quadrature of path functionals, and showed that the multilevel method reaches the worst case optimal order $\varepsilon^{-2} (\log \varepsilon)^2$ for a class of Lipschitz path-dependent functionals. So the Euler case is optimal up to the logarithm.
- **The factor $\varepsilon^{-2}$ is the floor.** Every bound has the factor $\varepsilon^{-2}$ of the [central limit theorem](/central-limit-theorem/): an estimator that averages independent samples of a variable with positive variance needs of order $\varepsilon^{-2}$ samples for root mean square error $\varepsilon$.

## History

Giles proved the theorem for SDE paths in 2008 (Theorem 3.1 of the Operations Research paper), with step sizes in the ratio 4 between levels. Cliffe, Giles, Scheichl and Teckentrup gave it in 2011 with general rates $\alpha$, $\beta$, $\gamma$, for elliptic PDEs with random coefficients. The form above, with expected costs, is Theorem 1 of the 2015 Acta Numerica review of Giles, who calls it a slight generalization of the 2008 theorem. Earlier, Heinrich had proved complexity bounds for multilevel methods in parametric integration and integral equations from 1998 on.

## References
