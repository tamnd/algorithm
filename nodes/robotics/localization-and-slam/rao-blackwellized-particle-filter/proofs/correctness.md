---
title: The RBPF is importance sampling on the sampled variables with exact conditionals
proves: [correctness]
status: full
---

**Setting.** The state splits into $r_t$, the part the filter samples, and $x_t$, the part it computes in closed form. In the code, $r_t = s_t$ is a mode of a Markov chain with $p(s_t \mid s_{t-1})$, and given the modes the model is linear and Gaussian: $x_t = a_{s_t} x_{t-1} + b_{s_t} + w_t$ and $z_t = c x_t + v_t$ with Gaussian noise. Particle $i$ holds a history $s^i_{1:t}$ (the code keeps only $s^i_t$, which is all that the next step needs), the mean and the variance of $x_t$ given that history and $z_{1:t}$, and a weight $w^i$.

**Claim.** (1) For each particle, lines L3 and L5 give the exact conditional $p(x_t \mid s^i_{1:t}, z_{1:t})$. (2) Lines L2, L4 and L6 are sequential importance sampling for the target $p(s_{1:t} \mid z_{1:t})$, with either proposal. (3) So the estimate of line L8 is a self-normalized importance sampling estimate of $E[f(x_t) \mid z_{1:t}]$ with the integrand $E[f(x_t) \mid s_{1:t}, z_{1:t}]$. (4) For a perfect sampler, this integrand has a variance no larger than that of $f(x_t)$, which is the Rao-Blackwell argument.

## The factorization

By the chain rule,

$$p(s_{1:t}, x_t \mid z_{1:t}) = p(x_t \mid s_{1:t}, z_{1:t}) \, p(s_{1:t} \mid z_{1:t}).$$

So it is enough to sample histories from the second factor and to compute the first one for each history.

## (1) The conditional of $x_t$ is a Kalman filter

Fix a history $s_{1:t}$. Then $x_t = a_{s_t} x_{t-1} + b_{s_t} + w_t$ and $z_t = c x_t + v_t$ form a linear Gaussian state space model with known, time varying coefficients. For such a model, the Kalman filter gives $p(x_t \mid s_{1:t}, z_{1:t})$ exactly, by induction over $t$: if $p(x_{t-1} \mid s_{1:t-1}, z_{1:t-1}) = N(m, P)$, the prediction is $N(a m + b, a^2 P + q)$, and Bayes' rule with the Gaussian reading gives the update of line L5. The mode $s_t$ enters only through $a$, $b$ and $q$, and $x_{t-1}$ does not depend on $s_t$ given $s_{1:t-1}$, so line L3 uses the right prior. The same recursion gives the predictive density of the reading,

$$p(z_t \mid s_{1:t}, z_{1:t-1}) = N\big(z_t; \; c \bar m, \; c^2 \bar P + r\big),$$

with the predicted moments $\bar m$ and $\bar P$ of line L3.

## (2) The weights

By Bayes' rule and the Markov property of the modes,

$$p(s_{1:t} \mid z_{1:t}) \propto p(s_{1:t-1} \mid z_{1:t-1}) \; p(s_t \mid s_{t-1}) \; p(z_t \mid s_{1:t}, z_{1:t-1}).$$

Suppose that the weighted particles at time $t-1$ represent $p(s_{1:t-1} \mid z_{1:t-1})$: for each $i$, $w^i_{t-1}$ is proportional to the target over the proposal density of $s^i_{1:t-1}$. Line L2 extends each history with $s_t \sim \pi(s_t \mid s^i_{1:t-1}, z_t)$. The importance weight of the extended history is then

$$w^i_t \propto w^i_{t-1} \, \frac{p(s^i_t \mid s^i_{t-1}) \, p(z_t \mid s^i_{1:t}, z_{1:t-1})}{\pi(s^i_t \mid s^i_{1:t-1}, z_t)}.$$

- **Prior proposal.** $\pi = p(s_t \mid s_{t-1})$, so the factor is the predictive density $p(z_t \mid s^i_{1:t}, z_{1:t-1})$. The code computes it as `probs[s] / trans[s_prev][s]`.
- **Optimal proposal.** $\pi(s_t) = p(s_t \mid s^i_{t-1}) \, p(z_t \mid s^i_{1:t-1}, s_t, z_{1:t-1}) / Z^i$ with $Z^i = \sum_{s} p(s \mid s^i_{t-1}) \, p(z_t \mid s^i_{1:t-1}, s, z_{1:t-1})$. Then the factor is $Z^i$, which does not depend on the drawn $s^i_t$. Because the factor is fixed once the past is fixed, the draw of $s^i_t$ adds no variance to the weight; this is why the proposal is called optimal. It needs the predictive density of every mode, which the code computes anyway.

Line L6 normalizes, which does not change the ratios. Line L7 resamples with the low variance sampler when the effective sample size $(\sum w)^2 / \sum w^2$ falls below $N/2$. Resampling draws $N$ histories with probabilities proportional to the weights and gives each the weight $1/N$, so the expected number of copies of each history is proportional to its weight, and the resampled set represents the same distribution.

## (3) The estimate

Line L8 returns $\sum_i \tilde w^i \, E[x_t \mid s^i_{1:t}, z_{1:t}]$ with the normalized weights $\tilde w^i$, and $\sum_i \tilde w^i [s^i_t = k]$ for the mode probabilities. By the factorization,

$$E[f(x_t) \mid z_{1:t}] = \sum_{s_{1:t}} p(s_{1:t} \mid z_{1:t}) \, E[f(x_t) \mid s_{1:t}, z_{1:t}],$$

so line L8 is the self-normalized importance sampling estimate of this sum. For a fixed $t$ and $N \to \infty$, such estimates converge to the sum; with resampling, this is the standard convergence of sequential Monte Carlo, which we use and do not prove here. The exact sum has $K^t$ terms, each a Kalman filter; `exact_posterior` in the code computes it, and the tests compare the filter with it.

## (4) Why it needs fewer particles

Let $g(s_{1:t}) = E[f(x_t) \mid s_{1:t}, z_{1:t}]$. By the law of total variance under the posterior,

$$\mathrm{Var}[f(x_t)] = \mathrm{Var}[g(s_{1:t})] + E\big[\mathrm{Var}[f(x_t) \mid s_{1:t}]\big] \ge \mathrm{Var}[g(s_{1:t})].$$

So with $N$ independent draws from the posterior, the average of $g$ has a variance no larger than the average of $f$ over draws of $(s_{1:t}, x_t)$. This is the [Rao-Blackwell theorem](/rao-blackwell-theorem/) applied to the estimator. For the full filter with resampling, the gain is not covered by these statements, so the code measures it: on the example of the page, with 100 particles over 20 seeds, the mean squared error of the RBPF is below that of a [particle filter](/particle-filter/) that samples $x_t$ too.
