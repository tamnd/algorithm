---
title: The pass computes the Breslow sums, which reduce to Nelson-Aalen at beta = 0, maximize the full likelihood over the baseline jumps, and make the Cox-Snell residuals sum to the number of events
proves: [correctness]
status: full
---

Let the data be $(y_i, \delta_i, x_i)$, $i = 1, \ldots, n$, with risk scores $w_i = \exp(\beta^{\mathsf T}x_i) > 0$ for a fixed $\beta$. Let $t_1 < \cdots < t_k$ be the distinct event times, $R_j = \{i : y_i \ge t_j\}$ the risk set, $n_j = |R_j|$, $d_j$ the number of events at $t_j$, $S_j = \sum_{i \in R_j} w_i$ and $D_j$ the sum of $w_i$ over the $d_j$ subjects that have the event at $t_j$. The Breslow estimate is

$$\hat H_0(t) = \sum_{t_j \le t} \frac{d_j}{S_j}.$$

**Claim 1 (the pass computes the sums).** Every row that line L5 keeps is $(t_j, S_j, d_j, D_j)$, one row for each $j$, and after line L9 the variable $H$ holds $\hat H_0(t_j)$.

*Proof.* Line L1 sorts the subjects by decreasing time. The inner loop of line L4 reads exactly the subjects at the current distinct time $u$. Invariant: at the start of the group at $u$, the variable $S$ is the sum of $w_i$ over $\{i : y_i > u\}$. It holds at the first group with the empty sum. The group adds the $w_i$ of all subjects with $y_i = u$, so after the group $S = \sum_{y_i \ge u} w_i$, which is $S_j$ when $u = t_j$. In the same loop $d$ and $D$ count the events at $u$ and add their scores. Line L5 keeps the row only if $d > 0$, that is, if $u$ is an event time. Line L6 puts the rows in increasing order of time, and lines L7 to L9 add $d_j/S_j$ in that order. $\square$

The sum $S_j$ is built from the largest time down, so each $S_j$ is a sum of positive terms. A forward pass that subtracts the scores that leave the risk set would give the same value in exact arithmetic, but in floating point it can cancel when the late scores are small compared with the early ones.

**Claim 2 (Nelson-Aalen at $\beta = 0$).** If $\beta = 0$, then $\hat H_0(t) = \sum_{t_j \le t} d_j/n_j$, the [Nelson-Aalen estimator](/nelson-aalen-estimator/). With the Efron rule the increment at $t_j$ is at least $d_j/n_j$, with equality exactly when $d_j = 1$.

*Proof.* At $\beta = 0$ every $w_i = 1$, so $S_j = n_j$ and $D_j = d_j$. The Breslow increment is $d_j/n_j$. The Efron increment is $\sum_{r=0}^{d_j - 1} 1/(n_j - r)$. Each term is at least $1/n_j$, and the term with $r = 1$ is strictly larger when $d_j \ge 2$. $\square$

**Claim 3 (profile maximum likelihood).** Fix $\beta$. Over all cumulative baseline hazards $\Lambda_0$ that are nondecreasing step functions, the full likelihood

$$L(\beta, \Lambda_0) = \prod_{i=1}^n \bigl(w_i\,\Delta\Lambda_0(y_i)\bigr)^{\delta_i} \exp\bigl(-w_i \Lambda_0(y_i)\bigr)$$

is maximized uniquely by $\Lambda_0 = \hat H_0$. The maximum value is $e^{-d} \prod_j d_j^{d_j}$ times the Cox partial likelihood with the Breslow tie rule, where $d = \sum_j d_j$.

*Proof.* If $\Lambda_0$ has no jump at some $t_j$, then $L = 0$, so a maximizer has a jump $\lambda_j > 0$ at each $t_j$. A jump at a time that is not an event time does not change any factor $\Delta\Lambda_0(y_i)$ with $\delta_i = 1$, and it increases $\Lambda_0(y_i)$ for every $y_i$ at or after it, so removing it does not decrease $L$, and strictly increases $L$ if some $y_i$ is at or after it. So it is sufficient to take $\Lambda_0(t) = \sum_{t_j \le t} \lambda_j$. Then

$$\log L = \sum_{i} \delta_i \beta^{\mathsf T}x_i + \sum_{j} d_j \log\lambda_j - \sum_i w_i \sum_{t_j \le y_i} \lambda_j = \sum_i \delta_i \beta^{\mathsf T}x_i + \sum_j \bigl(d_j \log\lambda_j - \lambda_j S_j\bigr),$$

because $t_j \le y_i$ is the same as $i \in R_j$. Each term $d_j \log\lambda_j - \lambda_j S_j$ is strictly concave in $\lambda_j > 0$, and its derivative $d_j/\lambda_j - S_j$ is $0$ only at $\lambda_j = d_j/S_j$. Put this value back:

$$\log L = \sum_i \delta_i \beta^{\mathsf T}x_i - \sum_j d_j \log S_j + \sum_j d_j \log d_j - d.$$

The first two sums are the log partial likelihood with the Breslow tie rule (see [partial likelihood](/cox-partial-likelihood/)). $\square$

So the joint maximizer of $L$ over $(\beta, \Lambda_0)$ is the Breslow-ties Cox estimate together with the Breslow estimator at that estimate.

**Claim 4 (residuals).** For every $\beta$, the Cox-Snell residuals $r_i = w_i \hat H_0(y_i)$ sum to $d$, so the martingale residuals $\delta_i - r_i$ sum to $0$.

*Proof.* Change the order of summation:

$$\sum_i w_i \hat H_0(y_i) = \sum_i w_i \sum_{t_j \le y_i} \frac{d_j}{S_j} = \sum_j \frac{d_j}{S_j} \sum_{i \in R_j} w_i = \sum_j d_j = d. \qquad \square$$

The identity does not need $\beta$ to be the Cox estimate, and it fails for the Efron rule, whose increment times $S_j$ is larger than $d_j$ when $d_j \ge 2$.

**Claim 5 (variance with $\beta$ fixed).** Under the counting process model with intensity $Y_i(t) w_i h_0(t)$ and $\beta$ known, $\hat H_0(t) - \int_0^t 1\{S(u) > 0\}\,dH_0(u)$ is a martingale, and $\sum_{t_j \le t} d_j/S_j^2$ estimates its variance. This is the argument of the Nelson-Aalen proof with $n_j$ replaced by $S_j$, and we do not repeat it. When $\beta$ is replaced by $\hat\beta$, the variance gets an extra term $q(t)^{\mathsf T} \mathcal I(\hat\beta)^{-1} q(t)$ with $q(t) = \sum_{t_j \le t} d_j \bar x_j / S_j$ and $\bar x_j$ the weighted mean of $x$ over $R_j$ (Tsiatis 1981; Andersen and Gill 1982). We cite this result and do not prove it here.

**Cost.** One sort, $\Theta(n \log n)$, one pass over the subjects, $\Theta(n)$, and one pass over the event times. The Efron rule adds $d_j$ terms at $t_j$, $O(n)$ in total. The risk scores cost $O(np)$ for $p$ covariates.
