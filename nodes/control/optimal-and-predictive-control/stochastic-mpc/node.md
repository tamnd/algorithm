---
tag: YWC263
kind: technique
slug: stochastic-mpc
name: Stochastic MPC
aliases:
- chance-constrained MPC
area: control/optimal-and-predictive-control
level: research
summary: MPC with random disturbances that minimizes an expected cost and asks that each constraint hold with a given probability.
prereqs: [linear-mpc, tube-mpc, chebyshev-inequality]
see_also: [min-max-mpc, economic-mpc, kalman-filter, lyapunov-equation, binomial-distribution, hoeffding-inequality, markov-inequality, input-to-state-stability]
sources:
  - paper: doi:10.1109/MCS.2016.2602087
    title: Ali Mesbah, Stochastic model predictive control, an overview and perspectives for future research, IEEE Control Systems Magazine 36(6), 30-44, 2016
    locator: the overview of expected costs, chance constraints, analytic tightening, scenario methods and the open questions
  - book: isbn:9780975937730
    title: James B. Rawlings, David Q. Mayne and Moritz M. Diehl, Model Predictive Control, Theory, Computation, and Design, 2nd edition, Nob Hill Publishing, 2017
    locator: the chapter on robust and stochastic MPC
---

Stochastic MPC is [model predictive control](/model-predictive-control/) for a plant with random disturbances whose distribution is known, at least in part. It minimizes the expected cost, and it replaces each hard constraint by a chance constraint: the constraint must hold with a probability of at least $1 - \varepsilon$. Robust MPC, such as [tube MPC](/tube-mpc/) or [min-max MPC](/min-max-mpc/), protects against the worst disturbance, which is rare and often far from typical. Stochastic MPC accepts a small, chosen rate of violations and in return uses the constraint range much better. For a linear plant with Gaussian noise and a fixed feedback, the expected cost is the nominal cost plus a constant, and each chance constraint becomes a deterministic constraint on the nominal state, tightened by a multiple of the standard deviation of the error. For other distributions, the tightening comes from a distribution-free inequality or from sampled scenarios.

## In plain words

When the disturbance is random, the worst case can be very unlikely but very large. Planning for it wastes most of the room you have. Stochastic predictive control plans for the usual case and allows a limit to be crossed only rarely, for example in one case out of twenty. It works out how far the real state can drift from the plan, as a spread of possible values, and keeps the plan away from each limit by a few times that spread. The spread is smaller than the worst case, so the plan can come closer to the limits. When little is known about the disturbance, a cruder rule or a set of sampled disturbances replaces the exact spread. The cost is an average over the random disturbances, not the cost of one bad case.

## When it applies

- A plant $x_{k+1} = A x_k + B u_k + w_k$ with independent disturbances $w_k$ of zero mean and covariance $W$, with a known distribution or at least a known covariance.
- Constraints whose rare violation is acceptable, such as a quality limit, a comfort band or an energy limit. Safety limits that must never be crossed need robust methods.
- A cost on the average behavior, $\mathbb{E} \sum_k (x_k^T Q x_k + u_k^T R u_k)$.
- For the analytic tightening below, a feedback $K$ with $A_K = A + B K$ Schur, and either Gaussian noise or a distribution-free bound.

## The template

1. **Split the state.** Write $u_k = K x_k + v_k$ for planned inputs $v_k$ and split $x_k = z_k + e_k$ into a nominal part $z_{k+1} = A_K z_k + B v_k$ with $z_0 = x$ and an error $e_{k+1} = A_K e_k + w_k$ with $e_0 = 0$.
2. **Propagate the covariance.** $\Sigma_0 = 0$ and $\Sigma_{k+1} = A_K \Sigma_k A_K^T + W$. This is computed once, offline. As $k$ grows, $\Sigma_k$ increases to the solution $\Sigma_\infty$ of the [Lyapunov equation](/lyapunov-equation/) $\Sigma = A_K \Sigma A_K^T + W$.
3. **Tighten the constraints.** Replace the chance constraint $\Pr(a^T x_k \le b) \ge 1 - \varepsilon$ by
$$a^T z_k \le b - \gamma \sqrt{a^T \Sigma_k a},$$
with $\gamma = \Phi^{-1}(1 - \varepsilon)$ for Gaussian noise, where $\Phi$ is the standard normal distribution function, or $\gamma = \sqrt{(1 - \varepsilon)/\varepsilon}$ for any distribution with the given covariance.
4. **Write the expected cost.** It equals the nominal cost of $(z, K z + v)$ plus terms $\mathrm{tr}(Q \Sigma_k) + \mathrm{tr}(K^T R K \Sigma_k)$ that do not depend on $v$.
5. **Solve and apply.** Solve the resulting QP for $v$, apply $u = K x + v_0$, and repeat at the next sample.

**Why it works.** The error $e_k$ does not depend on the planned inputs, it has zero mean, and its covariance is $\Sigma_k$ by induction: $\mathrm{Cov}(A_K e_k + w_k) = A_K \Sigma_k A_K^T + W$, since $w_k$ is independent of $e_k$.

*Cost.* $\mathbb{E}[(z + e)^T Q (z + e)] = z^T Q z + 2 z^T Q\, \mathbb{E}[e] + \mathbb{E}[e^T Q e] = z^T Q z + \mathrm{tr}(Q \Sigma)$. The input $u = K (z + e) + v$ gives in the same way $\mathbb{E}[u^T R u] = (K z + v)^T R (K z + v) + \mathrm{tr}(K^T R K \Sigma)$.

*Gaussian constraints.* If the $w_k$ are Gaussian, so is $a^T e_k$, with mean 0 and variance $s^2 = a^T \Sigma_k a$. Then $\Pr(a^T x_k \le b) = \Phi((b - a^T z_k)/s)$, which is at least $1 - \varepsilon$ exactly when $a^T z_k \le b - \Phi^{-1}(1 - \varepsilon)\, s$.

*Any distribution.* The one-sided Chebyshev inequality, also called Cantelli's inequality, gives $\Pr(a^T e_k \ge t) \le s^2/(s^2 + t^2)$ for every $t > 0$. With $t = s \sqrt{(1 - \varepsilon)/\varepsilon}$ the bound is $\varepsilon$, so the tightened constraint again implies the chance constraint.

**What is not proved here.** The chance constraints hold for the prediction made at each sample, given the state measured then. The fraction of violations along the closed loop is a different quantity and needs a separate argument. With noise of unbounded support, such as Gaussian noise, no plan can stay feasible for every disturbance, so recursive feasibility does not follow from the shifted plan. Common remedies are to choose $z_0$ between the measured state and the last predicted nominal state, to impose the first step robustly for a bounded noise, or to soften the constraints. Stability holds in a mean-square or average sense, not for every path. Joint chance constraints over several rows or steps need either a split of $\varepsilon$ by Boole's inequality or a harder, nonconvex formulation.

## Classic examples

**Scalar tightening.** Take $x^+ = x + u + w$ with $w$ Gaussian of standard deviation $0.1$, the feedback $K = -0.5$ so that $A_K = 0.5$, and the chance constraint $\Pr(x_k \le 1) \ge 0.95$. Then $\Sigma_{k+1} = 0.25\, \Sigma_k + 0.01$, $\Phi^{-1}(0.95) = 1.6449$ and $\sqrt{19} = 4.3589$:

| step $k$ | $\Sigma_k$ | Gaussian tightening | Cantelli tightening |
|---|---|---|---|
| 1 | 0.01 | 0.1645 | 0.4359 |
| 2 | 0.0125 | 0.1839 | 0.4873 |
| 3 | 0.013125 | 0.1884 | 0.4994 |
| $\infty$ | 0.013333 | 0.1899 | 0.5033 |

So in steady state the planned state may go up to $0.810$ with Gaussian noise, and up to $0.497$ when only the variance is known. For comparison, if the noise were bounded by $|w| \le 0.3$, three standard deviations, the robust tube of [tube MPC](/tube-mpc/) would need a margin of $0.3/(1 - 0.5) = 0.6$.

**The scenario approach.** Instead of an analytic tightening, draw $S$ disturbance sequences and require the constraints for all of them. For a convex problem with $d$ decision variables, Campi and Garatti (2008) showed that the probability, over the draw of the samples, that the solution violates the constraint with a probability above $\varepsilon$ is at most $\beta$ when
$$\sum_{i=0}^{d-1} \binom{S}{i} \varepsilon^i (1 - \varepsilon)^{S - i} \le \beta.$$
For $\varepsilon = 0.05$ and $\beta = 10^{-6}$, the smallest numbers of scenarios are:

| $d$ | 1 | 2 | 5 | 10 | 20 |
|---|---|---|---|---|---|
| $S$ | 270 | 326 | 459 | 643 | 962 |

For $d = 1$ the condition is $0.95^S \le 10^{-6}$. The count grows roughly linearly in $d$ and in $1/\varepsilon$, and only with the logarithm of $1/\beta$. The method needs no knowledge of the distribution beyond the ability to sample it, but the online problem grows with $S$.

## Variations

- **Affine disturbance feedback.** Optimize $u_k = v_k + \sum_{j<k} M_{kj} w_j$ instead of fixing $K$. The problem stays convex and is less conservative.
- **Joint chance constraints.** Ask that all constraints hold together with probability $1 - \varepsilon$. Split $\varepsilon$ among the rows by Boole's inequality, or use scenarios.
- **Bounded noise.** With bounded support, combine robust constraints for the first step with chance constraints later, which gives recursive feasibility.
- **Nonlinear plants.** Propagate means and covariances by linearization or by the unscented transform, or use polynomial chaos expansions.
- **Expected value of other costs.** Use [economic](/economic-mpc/) costs, or risk measures such as the conditional value at risk instead of the mean.
- **Output feedback.** Use a [Kalman filter](/kalman-filter/) estimate, and add the estimation error covariance to $\Sigma_k$.

## Pitfalls

- **Wrong distribution.** The Gaussian tightening is exact only for Gaussian noise. With heavier tails, the violation rate is higher than $\varepsilon$. Use the Cantelli factor when unsure.
- **Unbounded noise and hard constraints.** With Gaussian noise, any hard state constraint will be violated eventually, and a hard constraint in the QP can make it infeasible. Use soft constraints or a feasible fallback.
- **Confusing the two probabilities.** The chance constraint is about the next prediction, not about the closed loop over time.
- **Many joint constraints.** Splitting $\varepsilon$ over many rows and steps makes each tightening large. Check how conservative the split is.
- **Too few scenarios.** The scenario bound depends on the number of decision variables. For long horizons with many inputs, the number of samples and the online cost grow fast.

## Exercises

1. For $e^+ = 0.5 e + w$ with $\mathrm{Var}(w) = 0.01$, find the stationary variance. (Answer: $\Sigma = 0.25\, \Sigma + 0.01$ gives $\Sigma = 0.01/0.75 = 0.01\overline{3}$, with standard deviation $0.1155$.)
2. Find the Gaussian tightening at step 1 in the scalar example. (Answer: $\Sigma_1 = 0.01$, so $1.6449 \times 0.1 = 0.1645$.)
3. Show that the expected cost of $x = z + e$ with $\mathbb{E}[e] = 0$ is $z^T Q z + \mathrm{tr}(Q \Sigma)$. (Answer: the cross term has expectation $2 z^T Q\, \mathbb{E}[e] = 0$, and $\mathbb{E}[e^T Q e] = \mathrm{tr}(Q\, \mathbb{E}[e e^T])$.)
4. Find the number of scenarios for $d = 1$, $\varepsilon = 0.05$ and $\beta = 10^{-6}$. (Answer: $0.95^S \le 10^{-6}$ gives $S \ge \ln(10^{-6})/\ln(0.95) = 269.3$, so $S = 270$.)
5. Two rows must hold jointly with probability $0.95$. Give a tightening factor for Gaussian noise. (Answer: by Boole's inequality, give each row $\varepsilon = 0.025$, so $\gamma = \Phi^{-1}(0.975) = 1.96$ for each row.)

## References
