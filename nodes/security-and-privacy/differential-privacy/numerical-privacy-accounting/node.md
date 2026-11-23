---
tag: XTW2ZE
kind: algorithm
slug: numerical-privacy-accounting
name: Numerical privacy loss distribution accounting
aliases:
- PRV accountant
- privacy loss distribution accountant
- PLD accountant
- FFT accountant
area: security-and-privacy/differential-privacy
level: research
summary: "Composes mechanisms by convolving discretized privacy loss distributions with the FFT, which gives near-exact epsilon for given delta."
model: real-ram
complexity:
  vars: {n: the number of grid points of one privacy loss distribution, k: the number of composed steps}
  time: {worst: O(k n log(k n))}
  space: {extra: O(k n)}
properties: {deterministic: true, randomized: false}
history:
  year: 2018
  people: [Sebastian Meiser, Esfandiar Mohammadi, Antti Koskela, Joonas Jalko, Antti Honkela, Sivakanth Gopi, Yin Tat Lee, Lukas Wutschitz]
  note: "Meiser and Mohammadi computed upper and lower bounds on r-fold composition with privacy buckets (CCS 2018). Koskela, Jalko and Honkela used the FFT for the convolutions (AISTATS 2020). Gopi, Lee and Wutschitz gave the PRV accountant (NeurIPS 2021)."
prereqs: [privacy-loss-random-variable, convolution-via-fft]
see_also: [moments-accountant, optimal-composition-theorem, gaussian-differential-privacy, privacy-amplification-by-subsampling, dp-sgd, randomized-response, iterative-fft, bisection-method]
sources:
  - url: "https://eprint.iacr.org/2017/1034"
    title: "Sebastian Meiser and Esfandiar Mohammadi, Tight on budget? Tight bounds for r-fold approximate differential privacy, ACM CCS 2018, doi 10.1145/3243734.3243765"
    locator: "privacy buckets: provable upper and lower bounds on the delta of r-fold composition"
  - url: "https://arxiv.org/abs/1906.03049"
    title: "Antti Koskela, Joonas Jalko and Antti Honkela, Computing tight differential privacy guarantees using FFT, AISTATS 2020"
    locator: "the integral formula for exact (epsilon, delta), its discretization, the FFT evaluation of the convolutions, and the error bounds"
  - url: "https://arxiv.org/abs/2106.02848"
    title: "Sivakanth Gopi, Yin Tat Lee and Lukas Wutschitz, Numerical composition of differential privacy, NeurIPS 2021"
    locator: "privacy loss random variables, the PRV accountant and its error bounds, and the running time for k-fold composition"
---

Numerical privacy accounting computes the privacy guarantee of many composed mechanisms almost exactly. The tight $\delta$ of a mechanism at a given $\varepsilon$ is a function of the distribution of its [privacy loss random variable](/privacy-loss-random-variable/), the PLD. When mechanisms with independent noise are composed, their privacy losses add, so the PLD of the composition is the convolution of their PLDs. The accountant rounds each PLD to a grid of step $h$, convolves the grids with the [FFT](/convolution-via-fft/), and reads off $\delta(\varepsilon)$. If every loss is rounded up, the result is an upper bound on the true $\delta$; if every loss is rounded down, it is a lower bound. A finer grid closes the gap. For ten Gaussian steps that together are $1$-GDP, a grid of step $h = 0.002$ puts the true $\delta(1) = 0.126937$ between $0.125129$ and $0.128761$. The method is due to Meiser and Mohammadi (2018), Koskela, Jalko and Honkela (2020), and Gopi, Lee and Wutschitz (2021), who call their version the PRV accountant.

## In plain words

Each private step leaks a random amount about a person. Some outcomes leak a lot and most leak little. The full pattern of the leak is a list: how likely each size of leak is. When we run many steps, the leaks add up, and the list for the total can be computed from the lists of the steps.

The accountant writes each list on a fine ruler, and moves each entry to the next mark up, so that it never claims less leak than there is. It then combines the lists with a fast method for adding up all the ways the steps can combine. From the final list it reads the usual privacy numbers. A second run that moves each entry down gives a number that is too small. The true answer is between the two.

## The problem

A PLD on a grid of step $h > 0$ is a list of masses $\omega_0, \ldots, \omega_{n-1} \ge 0$ at the losses $\ell_j = (l + j)h$ for an integer offset $l$, and a mass $\omega_\infty \ge 0$ at $+\infty$. For a pair of output distributions $(P, Q)$ of a mechanism on two neighbors, the exact PLD is the law of $L = \ln(P(o)/Q(o))$ for $o \sim P$, and

$$\delta(\varepsilon) = \sup_S\left(P(S) - e^{\varepsilon}Q(S)\right) = E\left[\left(1 - e^{\varepsilon - L}\right)_+\right],$$

where the term is 1 when $L = +\infty$. Input: a grid PLD $\omega$, a number of steps $k \ge 1$, and $\varepsilon \ge 0$. Output: $\delta_k(\varepsilon)$ for the sum of $k$ independent copies of the loss. For the inverse problem, a target $\delta$ is given and the output is the least $\varepsilon$ with $\delta_k(\varepsilon) \le \delta$, which bisection finds because $\delta_k$ does not increase with $\varepsilon$.

Two discretizations of a continuous PLD with distribution function $F$:

- **pessimistic:** the mass of each cell $((i-1)h, ih]$ goes to $ih$; the mass below the grid goes to its lowest point, and the mass above it goes to $+\infty$;
- **optimistic:** the mass of each cell $((i-1)h, ih]$ goes to $(i-1)h$, and the mass outside the grid is dropped.

## The algorithm

```pseudo id=main
NUMERICAL-ACCOUNTANT(omega, k, epsilon)
L1  N <- the least power of 2 with N >= k(n - 1) + 1
L2  W <- FFT(omega_0, ..., omega_{n-1}, 0, ..., 0)     ▷ zero padded to length N
L3  W_s <- (W_s)^k  for s = 0..N-1
L4  omega' <- the first k(n - 1) + 1 entries of INVERSE-FFT(W)
L5  omega'_inf <- 1 - (1 - omega_inf)^k
L6  delta <- omega'_inf + sum over j with loss (kl + j)h > epsilon of omega'_j (1 - e^(epsilon - (kl + j)h))
L7  return delta
```

Line L1 picks a transform length that holds the whole $k$-fold convolution, which has $k(n-1)+1$ entries, so that the cyclic convolution of the FFT does not wrap around. Line L2 takes the discrete Fourier transform of the zero-padded masses. By the convolution theorem, the transform of a $k$-fold convolution is the $k$-th power of the transform, so line L3 raises each entry to the power $k$ and line L4 transforms back. The offset of the result is $kl$, because the losses add. Line L5 gives the mass at $+\infty$: the sum is infinite when at least one step is infinite. Line L6 evaluates the formula for $\delta$ on the composed grid, and line L7 returns it.

To compose different mechanisms on the same grid, multiply their transforms at line L3 instead of taking a power. To find $\varepsilon$ for a target $\delta$, compose once and run bisection on $\varepsilon$ with line L6 alone.

The accountant does only arithmetic on public parameters; it reads no data and draws no noise. The mechanisms that it accounts for must draw their noise from a cryptographic source of randomness with an exact sampler, because float noise from a seeded generator leaks through its low-order bits (Mironov 2012; Canonne, Kamath and Steinke 2020). The [discrete Gaussian mechanism](/discrete-gaussian-mechanism/) page shows an exact sampler.

## Example

Take [randomized response](/randomized-response/) with $\varepsilon_0 = 1$ on the grid $h = 1$: the loss is $+1$ with probability $p = e/(1+e) = 0.731059$ and $-1$ otherwise, so $l = -1$, $n = 3$ and $\omega = (0.268941, 0, 0.731059)$. Compose $k = 3$ steps.

| step | state |
|---|---|
| L1 | $k(n-1)+1 = 7$, so $N = 8$ |
| L2 to L4 | $\omega' = (0.019452, 0, 0.158631, 0, 0.431205, 0, 0.390712)$ at losses $-3, \ldots, 3$; offset $kl = -3$ |
| L5 | $\omega'_\infty = 0$ |
| L6, $\varepsilon = 0$ | $0.431205(1 - e^{-1}) + 0.390712(1 - e^{-3}) = 0.643833$ |
| L6, $\varepsilon = 1$ | $0.390712(1 - e^{-2}) = 0.337835$ |
| L6, $\varepsilon = 2$ | $0.390712(1 - e^{-1}) = 0.246977$ |
| L6, $\varepsilon = 3$ | $0$ |

The composed masses are the binomial law of the number of $+1$ losses, as they must be. Randomized response is the worst case among $\varepsilon_0$-DP mechanisms, so these numbers are also the tight values of the [optimal composition theorem](/optimal-composition-theorem/) for three $1$-DP steps.

A second example uses a continuous PLD. Ten Gaussian steps, each with $\mu_i = 1/\sqrt{10}$, compose to $1$-GDP, whose exact $\delta(1)$ is $\Phi(-1/2) - e\,\Phi(-3/2) = 0.126937$. The pessimistic and optimistic grids give:

| grid step $h$ | grid points $n$ | optimistic $\delta(1)$ | pessimistic $\delta(1)$ |
|---|---|---|---|
| 0.01 | 635 | 0.118074 | 0.136234 |
| 0.005 | 1267 | 0.122451 | 0.131531 |
| 0.002 | 3165 | 0.125129 | 0.128761 |

The gap shrinks in proportion to $h$. On the 4-fold composition of $\mu = 0.5$ with $h = 0.01$, bisection gives $\varepsilon = 4.397$ at $\delta = 10^{-5}$ from the pessimistic grid and $4.357$ from the optimistic grid; the exact value is $4.377$.

## Correctness

**Theorem.** Let $(P, Q)$ be a pair of distributions with PLD $L$, and let $\delta_k$ be the $\delta$ curve of $(P^{\otimes k}, Q^{\otimes k})$. In the real RAM, NUMERICAL-ACCOUNTANT on a grid PLD $\omega$ returns $E[(1 - e^{\varepsilon - S})_+]$ for $S$ the sum of $k$ independent draws from $\omega$. If $\omega$ is the pessimistic discretization of $L$, the result is at least $\delta_k(\varepsilon)$; if $\omega$ is the optimistic one, it is at most $\delta_k(\varepsilon)$.

The proof in [proofs/correctness.md](proofs/correctness.md) has four steps. First, $\delta(\varepsilon) = E[(1 - e^{\varepsilon - L})_+]$, the hockey-stick divergence written as an expectation under $P$. Second, the PLD of a product pair is the law of the sum of independent PLDs, so $\delta_k$ comes from the $k$-fold convolution. Third, lines L1 to L5 compute that convolution exactly, by the convolution theorem and because $N$ is large enough that the cyclic convolution equals the linear one. Fourth, the function $s \mapsto (1 - e^{\varepsilon - s})_+$ does not decrease, so rounding every loss up, or moving mass to $+\infty$, can only increase the result, and rounding down, or dropping mass, can only decrease it. When $(P, Q)$ is a dominating pair for each step of an adaptive composition, as for the Gaussian mechanism, the same bounds hold for the adaptive composition.

## Complexity

The composed grid has $k(n-1)+1$ points, so $N < 2kn$. In the real RAM, each FFT costs $O(N \log N)$, the powers at line L3 cost $O(N \log k)$, and line L6 costs $O(N)$. The total is $O(kn\log(kn))$ time and $O(kn)$ extra space. Each bisection step for $\varepsilon$ costs $O(kn)$.

The grid step sets the accuracy. Rounding moves each loss by less than $h$, so the sum of $k$ losses moves by less than $kh$, and the two bounds bracket $\delta$ in an $\varepsilon$ window of width $kh$. Gopi, Lee and Wutschitz show that a much coarser grid suffices, because the rounding errors of independent steps partly cancel when the rounding is done in expectation, and they give a running time of $\tilde O(\sqrt k)$ for a fixed target accuracy.

## Properties

- **Two-sided.** The pessimistic and optimistic grids give a certified bracket on $\delta$, so the user can see how far the reported value is from the exact one.
- **Tight in the limit.** As $h \to 0$ and the grid range grows, both bounds tend to the exact $\delta_k(\varepsilon)$, unlike the bounds of the [moments accountant](/moments-accountant/) or the [advanced composition theorem](/advanced-composition-theorem/), which stay above it.
- **Any mechanism with a known PLD.** The method needs only the PLD of each step, which is known for the Laplace, Gaussian and randomized response mechanisms and can be computed numerically for the [subsampled](/privacy-amplification-by-subsampling/) Gaussian.
- **Pure arithmetic.** It reads no data and has no randomness.

## Variants and improvements

- **Privacy buckets.** Meiser and Mohammadi put the loss into buckets with geometric boundaries and convolve the buckets directly, with upper and lower bounds.
- **FFT accountant.** Koskela, Jalko and Honkela truncate the losses to an interval $[-L, L]$, let the FFT wrap around, and bound the error of the truncation and of the wrap. Their version handles the subsampled Gaussian of [DP-SGD](/dp-sgd/).
- **PRV accountant.** Gopi, Lee and Wutschitz round each loss so that its mean is kept, and truncate the domain using a tail bound on the composed loss. This gives a grid that grows like $\sqrt k$ rather than $k$, with explicit error bounds on $\varepsilon$.
- **Characteristic functions.** Later work composes the Fourier transforms of the continuous PLDs directly and inverts only once at the end.
- **Heterogeneous steps.** Steps with different noise multiply their own transforms at line L3; the grid step must be the same for all.

## When to use it

Use numerical accounting when the exact $\varepsilon$ matters, as in a public release or a long training run where the last ten or twenty percent of the budget decides the noise level. It applies whenever the PLD of each step is known. Use the [moments accountant](/moments-accountant/) for a fast bound during development, and the closed form of [Gaussian differential privacy](/gaussian-differential-privacy/) when every step is a Gaussian mechanism without subsampling.

## Pitfalls

- **Wrap-around at line L1.** If $N$ is smaller than the length of the composed grid, the cyclic convolution of the FFT adds the top of the distribution to the bottom, and $\delta$ comes out too small. Choose $N$ as in line L1, or bound the wrapped mass.
- **Wrong rounding direction.** The upper bound needs every loss rounded up and the top tail moved to $+\infty$, not dropped. Rounding to the nearest grid point at line L2 gives neither bound.
- **Float error at lines L2 to L4.** The FFT in floats has an absolute error near the machine precision times the total mass, and some masses come out slightly negative. A $\delta$ of $10^{-10}$ is then below the noise floor; the bracket from the two grids does not account for this error.
- **Forgetting the mass at infinity at line L5.** A mechanism with $\omega_\infty > 0$, such as one with a nonzero $\delta$ of its own, adds at least $1 - (1-\omega_\infty)^k$ to the final $\delta$.
- **A pair that does not dominate.** The result is a guarantee only if the PLD comes from a pair that is the worst case over all neighbors, in both orders. For subsampled mechanisms the two orders give different PLDs, and both must be checked.
- **Floating-point noise in the mechanism.** The accounting assumes exact noise. Noise from a float sampler or a non-cryptographic generator is not covered by the bound.

## Implementations

## History

Before 2018, composition was done with closed-form bounds such as the [advanced composition theorem](/advanced-composition-theorem/), with Renyi accounting, or, for pure DP steps, with the exact but costly formula of the [optimal composition theorem](/optimal-composition-theorem/). Meiser and Mohammadi (CCS 2018) showed that the loss distribution itself can be composed numerically, with provable upper and lower bounds, and found that the bounds of the moments accountant were loose. Koskela, Jalko and Honkela (AISTATS 2020) wrote the exact $\delta$ as an integral, evaluated the convolutions with the FFT, and gave error bounds; they applied it to DP-SGD. Gopi, Lee and Wutschitz (NeurIPS 2021) introduced privacy random variables, the PRV accountant, and error bounds that need far fewer grid points, which made the method much faster for long compositions. PLD and PRV accountants are now in the main open source differential privacy libraries.

## References
