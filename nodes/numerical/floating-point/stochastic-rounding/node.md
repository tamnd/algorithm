---
tag: WXNW47
kind: technique
slug: stochastic-rounding
name: Stochastic rounding
aliases:
- randomized rounding
- SR
- probabilistic rounding
area: numerical/floating-point
level: research
summary: Rounds up or down at random with probability proportional to distance, removing systematic bias.
prereqs: [rounding-modes, floating-point-model, rounding-error-analysis]
see_also: [bfloat16, round-to-nearest-even, floating-point-summation, kahan-summation, martingale, azuma-inequality, randomized-rounding, numerical-stability]
sources:
  - paper: doi:10.1098/rsos.211631
    title: Matteo Croci, Massimiliano Fasi, Nicholas J. Higham, Theo Mary and Mantas Mikaitis, Stochastic rounding, implementation, error analysis and applications, Royal Society Open Science 9(3) (2022), 211631
    locator: the definition of mode 1 and mode 2 stochastic rounding, unbiasedness and mean independence, stagnation, the hardware implementations, and the survey of applications
  - paper: doi:10.1137/20M1334796
    title: Michael P. Connolly, Nicholas J. Higham and Theo Mary, Stochastic rounding and its probabilistic backward error analysis, SIAM Journal on Scientific Computing 43(1) (2021), A566-A585
    locator: mean independence of the rounding errors, the martingale argument with the Azuma-Hoeffding inequality, and the probabilistic bounds of order √n u for inner products and related computations
  - paper: doi:10.1137/1001011
    title: George E. Forsythe, Reprint of a note on rounding-off errors, SIAM Review 1(1) (1959), 66-67
    locator: the proposal (first made in 1950) to round randomly so that rounding errors behave like independent random variables
  - url: https://arxiv.org/abs/1502.02551
    title: Suyog Gupta, Ankur Agrawal, Kailash Gopalakrishnan and Pritish Narayanan, Deep learning with limited numerical precision, ICML 2015
    locator: training networks in 16-bit fixed point, which fails with round to nearest and succeeds with stochastic rounding
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 2.8, Statistical Distribution of Rounding Errors (the rule of thumb √n u and its assumptions); Section 4.2 on the error of recursive summation
  - paper: doi:10.1137/18M1226312
    title: Nicholas J. Higham and Theo Mary, A new approach to probabilistic rounding error analysis, SIAM Journal on Scientific Computing 41(5) (2019), A2815-A2835
    locator: probabilistic bounds of order √n u under the assumption that the rounding errors are independent random variables of mean zero
---

Stochastic rounding replaces the deterministic choice of round to nearest by a random choice between the two floats that bracket the exact result. It rounds up with probability equal to the fraction of the gap that the exact value has covered, so the expected rounded value is exactly the true value. The errors then have mean zero and are mean independent, whatever the data. That turns the heuristic that rounding errors grow like $\sqrt{n}\,u$ into a provable statement with high probability. It also removes stagnation, where long sums of small terms stop growing in low precision. Stochastic rounding is used mainly for training neural networks in 8- and 16-bit formats, and it is studied for climate and ODE codes in low precision.

## In plain words

Usually a computer rounds each result to the nearest number it can store. If the same kind of small amount is added again and again, it can be rounded away every time, and the total never moves. Stochastic rounding flips a biased coin instead. A value 30% of the way from one stored number to the next is rounded up 30% of the time and down 70% of the time. Any single result is a little less accurate, but on average the results are exactly right. Over many operations the errors cancel instead of piling up in one direction.

## When it applies

Use stochastic rounding when the following conditions hold:

- **Many small updates.** The computation adds a large number of small contributions to an accumulator, as in gradient descent, ODE time stepping and long sums. Round to nearest can lose such updates entirely.
- **Low precision.** The format is short, such as [bfloat16](/bfloat16/), binary16 or 8-bit floats, so the bias of round to nearest is large compared with the quantity of interest.
- **Statistical accuracy is enough.** Correct results on average or with high probability are acceptable, and bit-for-bit reproducibility is not required, or the random stream can be fixed.

It does not help when one operation must be as accurate as possible. In a single operation, round to nearest has error at most $u|x|$, while stochastic rounding can err by almost $2u|x|$.

## The template

Let $\mathbb{F}$ be the floating-point system with unit roundoff $u$. For a real $x$ in range, let $a = \mathrm{RD}(x)$ and $b = \mathrm{RU}(x)$ be the largest float at most $x$ and the smallest float at least $x$.

```pseudo id=main
SR(x, U)                          ▷ U uniform on [0, 1), independent of everything before
L1  a ← RD(x);  b ← RU(x)
L2  if a = b then return a        ▷ x is a float
L3  P ← (x − a) / (b − a)         ▷ the fraction of the gap covered
L4  if U < P then return b else return a
```

Every operation $x \mathbin{op} y$ is rounded as $\mathrm{SR}(x \mathbin{op} y, U_k)$ with a fresh $U_k$. In hardware the exact result is not available as a real number. The usual implementation adds $r$ random bits just below the last kept bit of the significand and then truncates. That realizes $P$ only to $r$ bits, and it is called few-bit stochastic rounding.

**What is proved.** The following hold under the assumptions of the [standard model](/floating-point-model/) (no overflow and no underflow), with the $U_k$ independent and uniform.

1. **Unbiased.** $\mathbb{E}[\mathrm{SR}(x)] = a(1 - P) + bP = a + (x - a) = x$.
2. **Bounded error.** $|\mathrm{SR}(x) - x| < b - a \le 2u|x|$, so $\mathrm{SR}(x) = x(1 + \delta)$ with $|\delta| < 2u$. Round to nearest has $|\delta| \le u$.
3. **Variance.** $\operatorname{Var}[\mathrm{SR}(x)] = (b - x)(x - a) \le (b - a)^2/4 \le u^2 x^2$.
4. **Mean independence.** For a computation $\hat t_k = \mathrm{SR}(\text{exact result of step } k)$, write $\hat t_k = t_k(1 + \delta_k)$. Then $\mathbb{E}[\delta_k \mid \delta_1, \ldots, \delta_{k-1}] = 0$, because, given the past, the exact result $t_k$ is fixed and item 1 applies. So the partial sums of $t_k\delta_k$ form a [martingale](/martingale/).
5. **Sums are unbiased.** For recursive summation $\hat s_k = \mathrm{SR}(\hat s_{k-1} + x_k)$ with $\hat s_0 = 0$, item 4 gives $\mathbb{E}[\hat s_k \mid \text{past}] = \hat s_{k-1} + x_k$. By induction $\mathbb{E}[\hat s_n] = \sum x_k$ exactly. By item 3, the increments of the martingale $\hat s_k - \sum_{i \le k} x_i$ have conditional variance at most $u^2(\hat s_{k-1} + x_k)^2$. So the error has standard deviation at most $u\bigl(\sum_k \mathbb{E}[(\hat s_{k-1} + x_k)^2]\bigr)^{1/2}$, which is of order $\sqrt{n}\,u\max_k |s_k|$.
6. **High-probability bounds.** Applying the [Azuma-Hoeffding inequality](/azuma-inequality/) to this martingale, Connolly, Higham and Mary (2021) prove backward error bounds for inner products, matrix products and related kernels. The bounds are of the form $\lambda\sqrt{n}\,u + O(u^2)$, and they hold with probability at least $1 - c_n\exp(-\lambda^2/2)$, where $c_n$ grows at most linearly in $n$. With round to nearest the corresponding $\sqrt{n}$ bounds of Higham and Mary (2019) need the assumption that the errors are independent. Under stochastic rounding they are theorems.

## Classic examples

**Stagnation in bfloat16.** Start from $s = 1$ and add $2^{-9}$ to it 4096 times in bfloat16 ($p = 8$, so the spacing at 1 is $2^{-7}$). The exact result is $9$. With round to nearest, $1 + 2^{-9}$ is below the midpoint $1 + 2^{-8}$, so it rounds back to $1$ at every step, and the final value is $1$. With stochastic rounding each step rounds up with probability $1/4$ while $s < 2$, and with smaller probabilities later, as the spacing grows. One run with seed 1 ended at $9.4375$. Twenty runs with other seeds had mean $9.008$, standard deviation $0.53$, and range $[7.91, 10.06]$. These are simulation results, not bounds.

**The harmonic series in binary16.** Summing $1/k$ in binary16 with round to nearest stops at $7.0859375$ when $k = 513$. From then on, every term is below half the spacing of the sum. With stochastic rounding, three runs of 2000 terms ended at $8.039$, $8.164$ and $8.188$. The true partial sum is $8.178$. This is a standard example in the literature on stochastic rounding (Croci et al. 2022), reproduced here with our own emulation.

**One rounding.** In a format with $p = 4$, $1/3$ lies between $5/16$ and $11/32$, at $2/3$ of the gap. Stochastic rounding returns $11/32$ with probability $2/3$ and $5/16$ with probability $1/3$. The expected value is $\tfrac23 \cdot \tfrac{11}{32} + \tfrac13 \cdot \tfrac{5}{16} = \tfrac13$.

**Low-precision training.** Gupta et al. (2015) trained neural networks with 16-bit fixed-point weights. With round to nearest, small gradient updates were lost and training failed. With stochastic rounding, training matched 32-bit floating point. Later work on 8-bit floating-point formats and on hardware with built-in stochastic rounding, for example Graphcore's IPU, builds on the same effect.

**ODE and climate models.** In explicit time stepping with a small step $h$, the update $y + hf(y)$ is small compared with $y$. Round to nearest in half precision can freeze the solution. Stochastic rounding keeps the expected trajectory on course, and it has been tested for weather and climate models in low precision.

## Variations

- **Mode 2, the definition above.** The probability is proportional to the distance. This is the variant meant by "stochastic rounding" in recent work.
- **Mode 1.** Round up or down with probability $1/2$ each, wherever $x$ lies in the gap. The expected value is the midpoint $(a + b)/2$, not $x$, so this mode is biased. It is mainly of historical interest, as the random rounding of the CESTAC method.
- **Few-bit stochastic rounding.** Use only $r$ random bits. The bias is then at most about $2^{-r}$ of an ulp, and $r$ around 8 to 16 is common in hardware.
- **Stochastic rounding for conversions only.** Compute in higher precision and stochastically round only when storing into a low-precision array, such as the weights or the state. This is the cheapest way to get most of the benefit.
- **Random rounding for error estimation.** The CESTAC method and CADNA run a program several times with random rounding and estimate the number of correct digits from the spread of the results. The goal there is diagnosis, not unbiasedness.
- **Not to be confused with** [randomized rounding](/randomized-rounding/) of linear programs, which rounds fractional solutions of LP relaxations to integers. The idea is similar, an unbiased random choice, but the setting is different.

## Pitfalls

- **Worse worst case.** A single stochastically rounded operation can have error close to $2u|x|$, twice the round-to-nearest bound. Deterministic bounds with $\gamma_n$ get worse by a factor of 2.
- **Correlated randomness.** The guarantees need fresh, independent random numbers for every rounding. A low-quality generator, or bits reused across lanes, brings back bias.
- **No reproducibility.** Results change from run to run unless the random stream is fixed. Debugging and regression testing need a seeded generator.
- **Exact results stay exact.** If $x$ is a float, $\mathrm{SR}(x) = x$. Stochastic rounding does not smooth out quantization of values that are already representable.
- **Not a cure for cancellation.** It removes bias, but it does not reduce the error caused by [catastrophic cancellation](/catastrophic-cancellation/) or ill conditioning.
- **Few-bit implementations are biased.** With $r$ random bits, values whose fraction of the gap is below $2^{-r}$ always round down. So very small updates can still stagnate.

## Exercises

1. Show that $\mathbb{E}[\mathrm{SR}(x)] = x$ and $\operatorname{Var}[\mathrm{SR}(x)] = (b - x)(x - a)$, and find the $x$ in $[a, b]$ that maximizes the variance.
2. Prove $|\mathrm{SR}(x) - x| < 2u|x|$ for $x$ not a float, and give a family of $x$ for which the ratio $|\mathrm{SR}(x) - x| / (u|x|)$ approaches 2.
3. For recursive summation of $n$ equal terms $x_k = c$ starting from 0, compute $\mathbb{E}[\hat s_n]$ under stochastic rounding. Then find the first $n$ at which round to nearest stagnates, in terms of $c$ and $u$.
4. Implement few-bit stochastic rounding with $r$ random bits, and compute its bias exactly for $x = a + \theta(b - a)$ as a function of $\theta$ and $r$.
5. Use the Azuma-Hoeffding inequality to show that the stochastic-rounding error of a sum of $n$ nonnegative terms is at most $\lambda\sqrt{n}\,u\sum_k x_k$, to first order in $u$, with probability at least $1 - 2\exp(-\lambda^2/2)$.

## References
