---
tag: HY1FY8
kind: algorithm
slug: abc-sequential-monte-carlo
name: ABC sequential Monte Carlo
aliases:
- ABC-SMC
- ABC population Monte Carlo
area: statistics-and-inference/bayesian-statistics
level: research
summary: Runs ABC over a falling sequence of tolerances, moving and reweighting a population of particles, so far fewer simulations are wasted than in rejection ABC.
model: real-ram
complexity:
  vars: {T: the number of generations, N: the number of particles, C: the cost of one simulation, A: the smallest acceptance rate over the generations}
  time: {expected: Θ(T (N^2 + N C / A))}
  space: {extra: Θ(N)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2009
  people: [Mark A. Beaumont, Jean-Marie Cornuet, Jean-Michel Marin, Christian P. Robert, Scott A. Sisson, Tina Toni]
  note: Sisson, Fan and Tanaka (2007) proposed the first sequential ABC sampler; its weights gave a biased answer and were corrected in 2009. Beaumont, Cornuet, Marin and Robert (2009) gave the population Monte Carlo weights used here, and Toni and coauthors (2009) the same scheme for dynamical systems and model choice.
prereqs: [abc-rejection-sampling, importance-sampling, sequential-monte-carlo, effective-sample-size]
see_also: [approximate-bayesian-computation, particle-filter, kernel-density-estimation, annealed-importance-sampling, metropolis-hastings, simulation-based-calibration, nested-sampling, rejection-sampling]
sources:
  - paper: doi:10.1093/biomet/asp052
    title: "Mark A. Beaumont, Jean-Marie Cornuet, Jean-Michel Marin and Christian P. Robert, Adaptive approximate Bayesian computation, Biometrika 96(4), 2009"
    locator: "pages 983 to 990: the ABC population Monte Carlo algorithm, its importance weights, the kernel variance equal to twice the weighted variance of the previous population, and the bias of the earlier partial rejection control weights (general locator)"
  - paper: doi:10.1073/pnas.0607208104
    title: "Scott A. Sisson, Yanan Fan and Mark M. Tanaka, Sequential Monte Carlo without likelihoods, Proceedings of the National Academy of Sciences 104(6), 2007"
    locator: "pages 1760 to 1765: the first sequential ABC sampler (ABC partial rejection control); see the correction, doi:10.1073/pnas.0908847106, 2009 (general locator)"
  - paper: doi:10.1098/rsif.2008.0172
    title: "Tina Toni, David Welch, Natalja Strelkowa, Andreas Ipsen and Michael P. H. Stumpf, Approximate Bayesian computation scheme for parameter inference and model selection in dynamical systems, Journal of the Royal Society Interface 6(31), 2009"
    locator: "pages 187 to 202: ABC-SMC with importance weights, and its use for model selection (general locator)"
  - paper: doi:10.1007/s11222-011-9271-y
    title: "Pierre Del Moral, Arnaud Doucet and Ajay Jasra, An adaptive sequential Monte Carlo method for approximate Bayesian computation, Statistics and Computing 22(5), 2012"
    locator: "pages 1009 to 1020: tolerances chosen adaptively from the effective sample size, with MCMC moves (general locator)"
---

ABC sequential Monte Carlo runs [approximate Bayesian computation](/approximate-bayesian-computation/) on a population of $N$ particles through a falling sequence of tolerances $\varepsilon_1 > \varepsilon_2 > \cdots > \varepsilon_T$. The first generation is the [ABC rejection algorithm](/abc-rejection-sampling/) at a loose tolerance. Each later generation draws a particle from the previous one, moves it by a random kernel, simulates data, and keeps the moved particle when the summaries are within the new tolerance. Proposals then come from near the current approximate posterior instead of from the prior, so far fewer simulations are wasted. The moved particles do not follow the prior any more, so each gets the importance weight $\pi(\theta)/\sum_j W_j K(\theta \mid \theta_j)$ of Beaumont, Cornuet, Marin and Robert (2009). With these weights, the population of generation $t$ targets the $\varepsilon_t$-posterior for any previous population.

## In plain words

Searching for the settings of a simulator that reproduce the real data, ABC rejection guesses blindly from the prior every time, so a strict match is rare. This method starts with a loose match, which is easy, and keeps a crowd of settings that pass it. Then it tightens the match step by step. At each step it picks a setting from the crowd, nudges it a little, and tests the nudged setting against the stricter match. Most guesses now land in a good region, so fewer simulations are wasted. The crowd was built by nudging, not by guessing from the prior, so some regions are now visited too often. Each setting therefore gets a weight that undoes this. Without the weights, the answer is too narrow.

## The problem

**Input.** A proper prior density $\pi$ that can be sampled and evaluated; a simulator for $Y \sim f(\cdot \mid \theta)$; the observed summaries $s_{\mathrm{obs}} = S(x)$, a distance $\rho$, and tolerances $\varepsilon_1 \ge \cdots \ge \varepsilon_T$; the number $N$ of particles.

**Output.** Particles $\theta_1, \ldots, \theta_N$ with weights $W_1, \ldots, W_N$ whose weighted mean of any function $h$ estimates the mean of $h$ under the $\varepsilon_T$-posterior $\pi_{\varepsilon_T}(\theta) \propto \pi(\theta)\,P_\theta(\rho(S(Y), s_{\mathrm{obs}}) \le \varepsilon_T)$.

## The algorithm

```pseudo id=main
ABC-SMC(π, simulator, S, s_obs, ρ, ε₁ ≥ … ≥ ε_T, N)
L1  run ABC rejection at ε₁ to get θ₁..θ_N;  Wⱼ ← 1/N
L2  s² ← 2 · (weighted variance of θ₁..θ_N under W)          ▷ the kernel K(·|θ') = N(θ', s²)
L3  for t ← 2 to T
L4      for i ← 1 to N
L5          repeat
L6              pick j with probability Wⱼ;  θ* ← θⱼ + N(0, s²)
L7              if π(θ*) > 0 then Y ← a data set simulated from f(· | θ*)
L8          until π(θ*) > 0 and ρ(S(Y), s_obs) ≤ ε_t
L9          θᵢ' ← θ*;  wᵢ ← π(θ*) / Σⱼ Wⱼ K(θ* | θⱼ)
L10     θ ← θ';  W ← w / Σᵢ wᵢ;  recompute s² as in L2
L11 return θ₁..θ_N and W₁..W_N
```

L1 is [ABC rejection](/abc-rejection-sampling/) with a loose tolerance, which accepts often. L2 sets the kernel variance to twice the weighted variance of the population, the choice of Beaumont et al. (2009): wide enough to explore, narrow enough to accept often. L6 draws from the mixture $g_t(\theta) = \sum_j W_j K(\theta \mid \theta_j)$ of kernels centred at the particles. L7 skips the simulation when the prior is zero, for example outside $[0, 1]$ for a probability. L8 is the ABC test at the new tolerance. L9 is the [importance sampling](/importance-sampling/) weight: target $\pi\,a_{\varepsilon_t}$, proposal $g_t\,a_{\varepsilon_t}$, and the unknown acceptance probability $a_{\varepsilon_t}$ cancels. L9 costs $N$ kernel evaluations per particle. L10 normalizes the weights and updates the kernel. The [effective sample size](/effective-sample-size/) of the weights, $1/\sum_i W_i^2$, measures how much the weights vary.

## Example

**Trace with four particles.** $6$ successes in $20$ Bernoulli trials, uniform prior on $p$, $S$ = the number of successes, $\rho(u, v) = |u - v|$, tolerances $(3, 1)$, `random.Random(8)`. Generation 1 (L1) needs $6$ simulations and keeps $0.2267, 0.2439, 0.2317, 0.3514$ with equal weights. L2 gives $s = 0.0724$. Generation 2 needs $9$ simulations:

| new particle $\theta_i'$ | 0.2985 | 0.3659 | 0.3708 | 0.1851 |
|---|---|---|---|---|
| normalized weight $W_i$ | 0.1722 | 0.3075 | 0.3247 | 0.1956 |

The three old particles near $0.23$ make the kernel mixture $g_2$ large there. New particles far from that cluster, at $0.37$ and $0.19$, have small $g_2$ and get large weights; $0.2985$, close to the cluster, gets the smallest weight.

**A full run.** Same model, $N = 500$, tolerances $(6, 3, 1, 0)$, `random.Random(2)`. The last tolerance is $0$ and the summary is sufficient, so the target is the exact posterior Beta(7, 15), with mean $0.3182$ and variance $0.009432$.

| generation | $\varepsilon_t$ | kernel $s$ | simulations | acceptance | ESS | weighted mean | weighted variance |
|---|---|---|---|---|---|---|---|
| 1 | 6 | | 820 | 0.610 | 500 | 0.3171 | 0.038169 |
| 2 | 3 | 0.276 | 1161 | 0.431 | 495 | 0.3209 | 0.018306 |
| 3 | 1 | 0.191 | 2186 | 0.229 | 493 | 0.3168 | 0.009867 |
| 4 | 0 | 0.140 | 5071 | 0.099 | 476 | 0.3196 | 0.009897 |

The run uses $9238$ simulations in total. ABC rejection at $\varepsilon = 0$ keeps one proposal in $21$ here, so $500$ draws cost about $10500$ simulations. The gain is small in this problem because the uniform prior is not much wider than the posterior. With $30$ successes in $100$ trials and tolerances $(30, 15, 8, 4, 2, 1, 0)$, ten runs with $N = 500$ use $23434$ simulations on average, against $50500$ for rejection.

**Dropping the weights.** Replace $w_i$ in L9 by $1$. Over ten runs each, the mean of the final weighted variance is $0.009004$ with the weights and $0.007025$ without them, against the exact $0.009432$: without the weights the answer is $25$ percent too narrow. With $100$ trials it is $0.002042$ with the weights, $0.001347$ without, and $0.002054$ exact.

## Correctness

The full proof is in proofs/correctness.md. It proves:

1. **Generation 1** follows the $\varepsilon_1$-posterior, by the proof for [ABC rejection](/abc-rejection-sampling/).
2. **The proposal law.** Given the previous population, the kept particles of generation $t$ are independent with density proportional to $g_t(\theta)\mathbf{1}\{\pi(\theta) > 0\}a_{\varepsilon_t}(\theta)$.
3. **The weight identity.** With $w = \pi/g_t$, $\mathbb{E}_{q_t}[wh]/\mathbb{E}_{q_t}[w] = \mathbb{E}_{\pi_{\varepsilon_t}}[h]$ for every integrable $h$, whatever the previous population is. The key invariant: at every generation, the weighted population is an importance sample for $\pi_{\varepsilon_t}$.
4. **Consistency** of the weighted mean for a fixed previous population as the number of new particles grows, by the law of large numbers.
5. **Equal weights are wrong.** Without L9 the population targets $q_t$, whose ratio to $\pi_{\varepsilon_t}$ is proportional to $g_t/\pi$.

What is proved and what is measured: items 1 to 5 are exact. The behaviour of all generations together as $N$ grows, and the error at a fixed $N$, are not proved on this page; the tables measure them against the exact posterior. The tests check item 3 in rational arithmetic on $500$ random finite models, and the weighted distribution of the final population against Beta(7, 15) with a Kolmogorov-Smirnov bound of $2.5/\sqrt{\mathrm{ESS}}$. That bound is a working tolerance, since weighted samples do not follow the usual Kolmogorov-Smirnov law.

## Complexity

Generation $t$ needs about $N/A_t$ simulations of cost $C$, where $A_t$ is its acceptance rate, and $N^2$ kernel evaluations for the weights on L9. Over $T$ generations the expected time is $\Theta(T(N^2 + NC/A))$ with $A$ the smallest rate. When simulations are expensive, the simulations dominate; for cheap simulators and large $N$, the $N^2$ term does, and a kernel density approximation of $g_t$ removes it. The population takes $\Theta(N)$ space.

## Properties

- **Not exact.** It targets the $\varepsilon_T$-posterior, and the weighted estimates have a bias of order $1/N$, like every self-normalized importance sampling estimate.
- **Valid for any kernel.** The weight identity holds for every kernel with $g_t > 0$ on the support of the target. The kernel affects only efficiency.
- **Parallel within a generation.** The $N$ particles of one generation are independent given the previous population.
- **Weight degeneracy.** If the kernel is too wide or too narrow, a few weights dominate, which the effective sample size shows.
- **Gives the intermediate posteriors.** Each generation is an estimate of $\pi_{\varepsilon_t}$, so one run shows how the answer changes as the tolerance falls.

## Variants and improvements

- **Adaptive tolerances.** Choose $\varepsilon_t$ as a quantile of the distances of the previous generation, or, as in Del Moral, Doucet and Jasra (2012), so that the effective sample size falls by a fixed fraction. Stop when the acceptance rate becomes too small.
- **MCMC moves.** Del Moral, Doucet and Jasra (2012) resample the population and move each particle by an ABC [Metropolis-Hastings](/metropolis-hastings/) step, which needs no $O(N^2)$ weight and keeps the population at the target.
- **Local kernels.** Use a covariance estimated from the nearest particles, or an optimal local covariance, in place of the single $s^2$ of L2.
- **Model choice.** Toni and coauthors (2009) add a model index to the particle and run the same scheme to estimate posterior model probabilities, which are valid only with summaries sufficient for the model index.
- **Regression adjustment** of the final population, as for ABC rejection.

## When to use it

Use ABC-SMC when the likelihood is intractable, simulations are costly, and the prior is much wider than the posterior, so that ABC rejection would waste most simulations. It is the standard ABC sampler in systems biology and epidemiology. For cheap simulators and a narrow prior, plain [ABC rejection](/abc-rejection-sampling/) is simpler and gives independent draws. When the likelihood can be evaluated, use [sequential Monte Carlo](/sequential-monte-carlo/) or MCMC on the true posterior. Check the calibration with [simulation-based calibration](/simulation-based-calibration/).

## Pitfalls

- **Missing or wrong weights.** Setting $w_i = 1$ on L9 because "the ABC test already selects the right particles" gives a population that is too narrow, by $25$ percent in variance in the example. Keep $w_i = \pi(\theta^*)/\sum_j W_j K(\theta^* \mid \theta_j)$, and recompute the mixture with the previous weights, not the new ones.
- **A kernel that is too small.** A tiny $s$ on L6 gives high acceptance but leaves the population stuck where it started, and the weights then degenerate. Use the rule of L2 or an adaptive kernel, and watch the effective sample size.
- **Falling too fast.** Jumping from a loose to a strict tolerance in L3 makes the acceptance rate on L8 tiny, like plain rejection. Lower $\varepsilon_t$ gradually, for example by a quantile rule.
- **Forgetting the prior support.** If L7 simulates at $\theta^*$ outside the support, the simulator may fail or return nonsense. Test $\pi(\theta^*) > 0$ first, as L7 does.
- **Treating the result as the posterior.** With $\varepsilon_T > 0$ or an insufficient summary, the population targets $\pi_{\varepsilon_T}$ given $S(x)$, not $\pi(\theta \mid x)$. Report $\varepsilon_T$ and the summaries.

## Implementations

## History

Sisson, Fan and Tanaka (2007) proposed the first sequential ABC sampler, based on partial rejection control. Beaumont, Cornuet, Marin and Robert (2009) showed that its weights give a biased answer, and gave the population Monte Carlo version with the weights of L9 and a kernel variance of twice the previous variance. Sisson and coauthors published a correction in 2009. Toni and coauthors (2009) proposed the same weighted scheme for parameter inference and model selection in dynamical systems, which made it popular in systems biology. Del Moral, Doucet and Jasra (2012) placed ABC in the framework of [sequential Monte Carlo](/sequential-monte-carlo/) samplers, with adaptive tolerances and MCMC moves.

## References
