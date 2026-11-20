---
tag: SAT4ZW
kind: algorithm
slug: multilevel-monte-carlo
name: Multilevel Monte Carlo
aliases:
- MLMC
area: scientific-computing/uncertainty-quantification
level: core
summary: Writes a fine-level expectation as a coarse one plus telescoping corrections, each estimated with fewer samples as the level grows.
solves: [forward-uncertainty-propagation]
model: real-ram
complexity:
  vars: {e: "the target root mean square error, in the case beta = gamma of the Euler example", L: the finest level, N: the total number of samples over all levels}
  time: {expected: "O(e^-2 (log e)^2)"}
  space: {extra: O(L)}
properties: {deterministic: false, randomized: true, exact: false, iterative: true}
history:
  year: 2008
  people: [Michael B. Giles, Stefan Heinrich]
  note: Heinrich used a multilevel splitting for parametric integration in 1998 and 2001. Kebaier used two levels for SDE simulation in 2005. Giles gave the general multilevel method for SDEs with its complexity theorem in 2008.
prereqs: [monte-carlo-integration, forward-uncertainty-propagation, variance]
see_also: [mlmc-complexity-theorem, monte-carlo-integration, multifidelity-monte-carlo, euler-maruyama-method, stochastic-differential-equation, multigrid-method, richardson-extrapolation, quasi-monte-carlo-integration]
sources:
  - paper: doi:10.1287/opre.1070.0496
    title: Michael B. Giles, Multilevel Monte Carlo path simulation, Operations Research 56(3), 2008, 607-617
    locator: Theorem 3.1 (the complexity theorem) and the numerical algorithm with its bias test, for Euler paths with step sizes in ratio 4
  - paper: doi:10.1017/S096249291500001X
    title: Michael B. Giles, Multilevel Monte Carlo methods, Acta Numerica 24, 2015, 259-328
    locator: Section 1.3 (the optimal number of samples on each level), Section 2.1, Theorem 1 (the complexity theorem), Section 5.1 (Euler-Maruyama paths and their coupling)
  - paper: doi:10.1007/3-540-45346-6_5
    title: Stefan Heinrich, Multilevel Monte Carlo methods, in Large-Scale Scientific Computing (LSSC 2001), Lecture Notes in Computer Science 2179, Springer, 2001, 58-67
    locator: the multilevel splitting for parametric integration
  - paper: doi:10.1007/s00791-011-0160-x
    title: K. Andrew Cliffe, Michael B. Giles, Robert Scheichl and Aretha L. Teckentrup, Multilevel Monte Carlo methods and applications to elliptic PDEs with random coefficients, Computing and Visualization in Science 14, 2011, 3-15
    locator: the complexity theorem in the form with alpha, beta and gamma, and the application to elliptic PDEs with random fields
---

Multilevel Monte Carlo (MLMC) estimates an expected value, such as the mean output of a simulation or an integral that a renderer computes by random sampling, when each sample comes from an approximation that gets more accurate and more expensive on finer levels. Plain [Monte Carlo integration](/monte-carlo-integration/) takes all samples on the finest level. MLMC writes the fine-level mean as the mean on a coarse level plus a sum of corrections between neighbor levels, and estimates each term with its own samples. A correction is the difference of two close approximations that use the same random input, so it has a small variance and needs few samples, and the many samples go to the cheap coarse level. For an output of a [stochastic differential equation](/stochastic-differential-equation/) solved by the [Euler-Maruyama method](/euler-maruyama-method/), this reduces the cost for a root mean square error $\varepsilon$ from $O(\varepsilon^{-3})$ to $O(\varepsilon^{-2} (\log \varepsilon)^2)$.

## In plain words

Say you want the average result of a simulation with random inputs. A fine simulation is accurate but slow, and a coarse one is fast but a little wrong. Plain Monte Carlo runs the fine simulation many times.

The multilevel idea is to ask the cheap question many times and the expensive question only a few times. First, average many coarse runs. Then fix the error of the coarse runs: run a fine and a coarse simulation on the same random input, and average the difference. The two runs see the same random input, so their difference is small and changes little from one input to the next. A small number of such pairs gives a good average of the difference. Do this again for each finer level. The sum of all the averages is as accurate as the finest level, at a fraction of the cost.

## The problem

The input is a random output $P$ of a model, for example $P = q(u(\xi))$ for a random input $\xi$ on a probability space $(\Omega, \mathcal{F}, \mathbb{P})$, and approximations $P_0, P_1, P_2, \ldots$ on levels $l = 0, 1, 2, \ldots$, which get more accurate and more expensive as $l$ grows. The output is an estimate $\widehat{Y}$ of $\mathbb{E}[P]$ with mean squared error $\mathbb{E}[(\widehat{Y} - \mathbb{E}[P])^2] \le \varepsilon^2$. This is the moment form of [forward uncertainty propagation](/forward-uncertainty-propagation/).

With $Y_l = P_l - P_{l-1}$ and $P_{-1} = 0$, the means telescope:

$$\mathbb{E}[P_L] = \sum_{l=0}^{L} \mathbb{E}[Y_l] = \mathbb{E}[P_0] + \sum_{l=1}^{L} \mathbb{E}[P_l - P_{l-1}].$$

The estimator takes $N_l$ independent samples of $Y_l$ on each level: $\widehat{Y} = \sum_{l=0}^{L} N_l^{-1} \sum_{n=1}^{N_l} Y_l^{(n, l)}$. In one sample of $Y_l$, the fine value $P_l$ and the coarse value $P_{l-1}$ use the same random input $\omega$; samples on different levels are independent. With $V_l = \mathrm{Var}(Y_l)$ and $C_l$ the cost of one sample of $Y_l$, the mean squared error is

$$\mathrm{MSE} = \sum_{l=0}^{L} \frac{V_l}{N_l} + \big(\mathbb{E}[P_L] - \mathbb{E}[P]\big)^2,$$

a variance plus a squared bias. The method keeps each part below $\varepsilon^2/2$. The rates $\alpha$, $\beta$, $\gamma$ of the area notation describe the levels: $|\mathbb{E}[P_l - P]| \le c\, 2^{-\alpha l}$, $V_l \le c\, 2^{-\beta l}$ and $C_l \le c\, 2^{\gamma l}$.

## The algorithm

```pseudo id=main
MLMC(SAMPLE, ε, α, β, γ, L_0, N_0)
L1  L ← L_0;  N_l ← 0 and dN_l ← N_0 for l = 0..L
L2  while dN_l > 0 for some l do
L3      for each l with dN_l > 0: draw dN_l coupled samples of Y_l = P_l - P_(l-1) by SAMPLE,
            add their sum, sum of squares and cost, and set N_l ← N_l + dN_l
L4      V_l ← sample variance of Y_l, C_l ← mean cost of one sample of Y_l, for l = 0..L
L5      dN_l ← max(0, ⌈2 ε^(-2) sqrt(V_l / C_l) Σ_k sqrt(V_k C_k)⌉ - N_l) for l = 0..L
L6      if dN_l = 0 for all l then
L7          bias ← max(|Ŷ_L|, |Ŷ_(L-1)| / 2^α) / (2^α - 1)        ▷ Ŷ_l is the sample mean of Y_l
L8          if bias > ε / sqrt(2) then L ← L + 1, set V_L ← V_(L-1) / 2^β and C_L ← C_(L-1) 2^γ, redo L5
L9  return Ŷ = Ŷ_0 + Ŷ_1 + ... + Ŷ_L
```

Line L3 is the only place where the model runs. SAMPLE must return, for one random input, both $P_l$ and $P_{l-1}$; for Euler paths the coarse path adds pairs of the fine Brownian increments. Line L5 is the optimal sample count of Giles: it minimizes the cost $\sum_l N_l C_l$ under the variance target $\sum_l V_l / N_l \le \varepsilon^2/2$, and it is derived in the proof. Line L7 estimates the bias $\mathbb{E}[P] - \mathbb{E}[P_L]$ as the tail of a geometric series with ratio $2^{-\alpha}$, from the last correction and, as a guard, from the one before it. Line L8 adds a level when the bias is too large; the new level has no samples yet, so its $V_L$ and $C_L$ come from the rates $\beta$ and $\gamma$ until line L3 samples it.

## Example

The output is $P = S_T$ for the geometric Brownian motion $dS = r S\, dt + \sigma S\, dW$ with $S_0 = 1$, $r = 0.05$, $\sigma = 0.2$ and $T = 1$. The exact mean is $\mathbb{E}[S_T] = e^{rT} = 1.0512711$. Level $l$ is the Euler-Maruyama value with $2^l$ steps; its mean is exactly $\mathbb{E}[P_l] = (1 + r T/2^l)^{2^l}$, so the bias on level $l$ is known. The cost of a sample is its number of time steps, fine plus coarse. The run uses $\varepsilon = 0.0005$, $\alpha = \beta = \gamma = 1$, $L_0 = 2$, $N_0 = 200$ and `random.Random(2024)` (a measurement):

| level $l$ | $N_l$ | $V_l$ | $\widehat{Y}_l$ | exact $\mathbb{E}[Y_l]$ | $N_l C_l$ |
|---|---|---|---|---|---|
| 0 | 495412 | $4.002 \times 10^{-2}$ | 1.050 | 1.05 | 495412 |
| 1 | 29469 | $4.247 \times 10^{-4}$ | $5.54 \times 10^{-4}$ | $6.25 \times 10^{-4}$ | 88407 |
| 2 | 15186 | $2.236 \times 10^{-4}$ | $4.23 \times 10^{-4}$ | $3.20 \times 10^{-4}$ | 91116 |
| 3 | 7672 | $1.152 \times 10^{-4}$ | $1.10 \times 10^{-4}$ | $1.62 \times 10^{-4}$ | 92064 |

The variance drops by a factor of about 100 from level 0 to level 1, because a correction is the difference of two close paths, and then halves with each level, as $\beta = 1$ says. The counts follow line L5: $N_l$ is proportional to $\sqrt{V_l / C_l}$. The loop stopped at $L = 3$, where line L7 gave $\max(1.10 \times 10^{-4}, 4.23 \times 10^{-4}/2) / 1 = 2.11 \times 10^{-4}$, below $\varepsilon/\sqrt{2} = 3.54 \times 10^{-4}$. The true bias at $L = 3$ is $1.0512711 - 1.0511075 = 1.64 \times 10^{-4}$.

The estimate is $1.0512784$, with error $7.3 \times 10^{-6}$, at a total cost of 766999 time steps. Plain Monte Carlo on level 3 needs $2 \varepsilon^{-2} V(P_3) = 320173$ samples of 8 steps each for the same variance, that is 2561384 steps, 3.3 times as many. The gap grows as $\varepsilon$ falls, as the complexity section shows. Over 30 seeds at $\varepsilon = 0.002$, the root mean square error was 0.00119, below the target.

## Correctness

The claim is that the estimate of line L9 has mean $\mathbb{E}[P_L]$, and that its mean squared error is at most $\varepsilon^2$ when the estimated variances and the bias test are right. The mean follows from the telescoping sum and [linearity of expectation](/linearity-of-expectation/). The variance is $\sum_l V_l / N_l$ because the samples are independent, and the counts of line L5 make it at most $\varepsilon^2/2$; by the Cauchy-Schwarz inequality no other counts reach this target at a lower cost. If $\mathbb{E}[Y_l]$ follows the rate $2^{-\alpha l}$ beyond level $L - 1$, the remaining bias is the geometric tail of line L7, which line L8 keeps at most $\varepsilon/\sqrt{2}$. The full proof, with termination, is in the proof file. It does not cover the error of the estimated $V_l$ and $\mathbb{E}[Y_l]$: with too few samples, or a correction that does not yet follow its rate, the bias test can pass too early.

## Complexity

The cost is $\sum_l N_l C_l$ model work, plus $O(1)$ arithmetic per sample and $O(L)$ per pass of the loop in the [real RAM](/real-ram/) model. With the counts of line L5,

$$\sum_l N_l C_l \approx 2 \varepsilon^{-2} \Big(\sum_{l=0}^{L} \sqrt{V_l C_l}\Big)^2, \qquad \sqrt{V_l C_l} \le c\, 2^{(\gamma - \beta) l / 2}.$$

The bias test stops at $L \approx \log_2(\varepsilon^{-1}) / \alpha$. If $\beta > \gamma$, the sum is a convergent geometric series and the cost is $O(\varepsilon^{-2})$, the cost of plain Monte Carlo with exact samples of unit cost. If $\beta = \gamma$, every term is $O(1)$, the sum is $O(L)$ and the cost is $O(\varepsilon^{-2} L^2) = O(\varepsilon^{-2} (\log \varepsilon)^2)$. If $\beta < \gamma$, the last term dominates and the cost is $O(\varepsilon^{-2 - (\gamma - \beta)/\alpha})$. These three cases are the [MLMC complexity theorem](/mlmc-complexity-theorem/); its proof needs $\alpha \ge \min(\beta, \gamma)/2$ and adds the rounding cost.

For the Euler example, $\alpha = \beta = \gamma = 1$, so MLMC costs $O(\varepsilon^{-2} (\log \varepsilon)^2)$. Plain Monte Carlo needs $O(\varepsilon^{-2})$ samples on a level with $O(\varepsilon^{-1})$ steps, which is $O(\varepsilon^{-3})$. The extra space is $O(L)$ for the sums of each level; the samples themselves are not stored.

## Properties

- **Unbiased for the finest level.** The estimate has mean $\mathbb{E}[P_L]$ for any counts. All the bias is the bias of level $L$.
- **Randomized.** The estimate is random and its error is statistical. The error bound holds in mean square, not for every run.
- **Non-intrusive.** The model is a black box that returns a fine and a coarse value for one random input. The only demand on it is the coupling.
- **Adaptive.** The number of levels and the counts come from the run, with three rate parameters from the user.
- **Parallel.** The samples of a level are independent and can run in parallel; only the sums are shared.

## Variants and improvements

- **Coarsening factor 4.** Giles 2008 uses step sizes $h_l = 4^{-l} h_0$. Then the rates are $\alpha = \beta = \gamma = 2$ in powers of 2, with the same order of cost.
- **Antithetic and Milstein corrections.** A better coupling raises $\beta$. With the [Milstein method](/milstein-method/) in one dimension, $\beta = 2 > \gamma = 1$, and the cost is $O(\varepsilon^{-2})$.
- **Multilevel quasi-Monte Carlo.** Each level uses randomized [quasi-Monte Carlo integration](/quasi-monte-carlo-integration/) instead of independent samples, which can lower the cost further when the corrections are smooth in the random input.
- **Multi-index Monte Carlo.** The levels have several indices, for example the time step and the space mesh, and the corrections are mixed differences.
- **Randomized unbiased estimators.** A random level with known probabilities gives an estimator that is unbiased for $\mathbb{E}[P]$ itself, if $\beta > \gamma$.
- **Elliptic PDEs with random coefficients.** The levels are meshes of a [finite element method](/finite-element-method/), and the input is a [random field](/random-field/). Cliffe, Giles, Scheichl and Teckentrup showed the method for this case in 2011.

## When to use it

Use MLMC when the output is a mean, the model has a hierarchy of discretizations, and you can couple two neighbor levels so that $V_l$ decays: SDE paths in finance, PDEs with random fields, particle systems. Use plain [Monte Carlo integration](/monte-carlo-integration/) when there is no useful hierarchy, or when the finest level is cheap. Use [multifidelity Monte Carlo](/multifidelity-monte-carlo/) when the cheap models are not levels of one discretization, for example a reduced model and a data fit, and their correlation with the fine model is known. Use [polynomial chaos expansion](/polynomial-chaos-expansion/) or [stochastic collocation](/stochastic-collocation-method/) when the input has few dimensions and the output is smooth in it. MLMC is unlike [Richardson extrapolation](/richardson-extrapolation/): it does not cancel the bias by a known error expansion, it estimates each correction by sampling.

## Pitfalls

- **Independent coarse samples.** If line L3 draws the coarse value $P_{l-1}$ with its own random input, $V_l = \mathrm{Var}(P_l) + \mathrm{Var}(P_{l-1})$ and does not decay; the method is then slower than plain Monte Carlo. The fine and the coarse value of one sample must use the same input.
- **Level 0 as a difference.** $Y_0$ is $P_0$ itself ($P_{-1} = 0$). Starting the sum at a correction drops the main term.
- **Too few initial samples.** Line L4 estimates $V_l$ from $N_0$ samples. With heavy-tailed corrections, a small $N_0$ underestimates $V_l$, and line L5 then takes too few samples. Use $N_0$ of a few hundred, and check the rates against the level variances.
- **A bias test on one noisy mean.** If line L7 used only $|\widehat{Y}_L|$, a correction that is small by chance stops the loop early. The maximum with $|\widehat{Y}_{L-1}|/2^\alpha$ guards against this, but cannot help if the true corrections have not reached their asymptotic rate.
- **A wrong rate.** A non-smooth output, such as an indicator of an event, has $\beta = 1/2$ with Euler paths, not 1. With $\beta = 1$ in line L8, the new levels get too few samples until they are sampled.

## Implementations

## History

Heinrich used a multilevel splitting of the expectation for parametric integration in 1998, and published it as multilevel Monte Carlo in 2001. Kebaier used two levels of time steps, a statistical form of Romberg extrapolation, for SDE simulation in 2005. Giles gave the general method with any number of levels, the optimal sample counts and the complexity theorem for SDE paths in 2008. The idea is close to the [multigrid method](/multigrid-method/), which also does most of its work on coarse grids and only a little on the fine one. Cliffe, Giles, Scheichl and Teckentrup extended it to elliptic PDEs with random coefficients in 2011, and Giles wrote a review of the field in Acta Numerica in 2015.

## References
