---
tag: BBS4G5
kind: algorithm
slug: moments-accountant
name: Moments accountant
aliases:
- privacy accountant for DP-SGD
- RDP accountant
area: security-and-privacy/differential-privacy
level: advanced
summary: "Tracks the log moments of the privacy loss of each subsampled Gaussian step, adds them over the steps, and turns the sum into an (epsilon, delta) bound by a tail bound."
model: real-ram
complexity:
  vars: {m: the largest moment order that is tried}
  time: {worst: O(m^2)}
  space: {extra: O(m)}
properties: {deterministic: true, randomized: false}
history:
  year: 2016
  people: [Martin Abadi, Andy Chu, Ian Goodfellow, H. Brendan McMahan, Ilya Mironov, Kunal Talwar, Li Zhang]
  note: "Abadi et al. introduced the moments accountant in the paper on deep learning with differential privacy (CCS 2016). Mironov, Talwar and Zhang gave the exact finite sum for integer orders in 2019."
prereqs: [renyi-differential-privacy, privacy-amplification-by-subsampling, log-sum-exp-trick]
see_also: [dp-sgd, numerical-privacy-accounting, gaussian-mechanism, privacy-loss-random-variable, zero-concentrated-differential-privacy, advanced-composition-theorem, binomial-distribution, gaussian-differential-privacy]
sources:
  - paper: doi:10.1145/2976749.2978318
    title: "Martin Abadi, Andy Chu, Ian Goodfellow, H. Brendan McMahan, Ilya Mironov, Kunal Talwar and Li Zhang, Deep learning with differential privacy, ACM CCS 2016, pages 308 to 318"
    locator: "Section 3.1 (the differentially private SGD algorithm and its privacy example), Section 3.2 (the moments accountant, Theorem 1, the log moment alpha(lambda) and Theorem 2 on composability and the tail bound)"
  - url: "https://arxiv.org/abs/1908.10530"
    title: "Ilya Mironov, Kunal Talwar and Li Zhang, Renyi differential privacy of the sampled Gaussian mechanism, arXiv 1908.10530, 2019"
    locator: "Definition 3 (sampled Gaussian mechanism with add/remove neighbors), Section 3.1 (the expression A_alpha for integer alpha and the proof that it dominates B_alpha), Theorem 4 (reduction to one dimension) and Section 3.3 (numerically stable computation)"
  - paper: doi:10.1109/CSF.2017.11
    title: "Ilya Mironov, Renyi differential privacy, IEEE 30th Computer Security Foundations Symposium (CSF 2017), pages 263 to 275"
    locator: "Proposition 1 (composition) and Proposition 3 (conversion to (epsilon, delta)-DP)"
---

The moments accountant computes the privacy cost of training with [DP-SGD](/dp-sgd/), where each step picks a random batch of records, clips their gradients, adds them, and adds Gaussian noise. Abadi and coauthors introduced it in 2016. Instead of a pair $(\varepsilon, \delta)$ per step, it tracks the log of the moment generating function of the [privacy loss random variable](/privacy-loss-random-variable/) at a few orders $\lambda$. These log moments add up exactly under composition, and a tail bound at the end turns the sum into one $(\varepsilon, \delta)$ guarantee. For a step with sampling rate $q = 0.01$ and noise multiplier $\sigma = 4$, ten thousand steps cost about $\varepsilon = 1.26$ at $\delta = 10^{-5}$, while the [advanced composition theorem](/advanced-composition-theorem/) on the same steps gives about $9.34$. The log moment of order $\lambda$ is $\lambda$ times the Renyi divergence of order $\lambda + 1$, so the accountant is [Renyi DP](/renyi-differential-privacy/) accounting at integer orders. This page gives the version with the exact finite sum of Mironov, Talwar and Zhang.

## In plain words

Training a private model takes thousands of small noisy steps, and each step leaks a little about each person. Adding the worst-case leak of each step gives a total that is far too large to be useful.

The accountant keeps a better record. For each step it notes a few summary numbers that describe how the leak is spread out, not only its worst case. These numbers just add from step to step. At the end, one short calculation turns the totals into the usual privacy guarantee. Because the step uses a random batch, most people are not in it, and the numbers for one step are very small.

## The problem

One step of the subsampled Gaussian mechanism, under add/remove neighbors:

- keep each record independently with probability $q$ (Poisson sampling);
- for each kept record, compute a vector and clip it to $\ell_2$ norm at most 1;
- release the sum of the clipped vectors plus $N(0, \sigma^2 I)$.

The vectors of a step may depend on the outputs of earlier steps. Input: the rate $q \in [0, 1]$, the noise multiplier $\sigma > 0$, the number of steps $T$, a target $\delta \in (0, 1)$, and the largest order $m$ to try. Output: an $\varepsilon$ such that the $T$ steps together are $(\varepsilon, \delta)$-DP, as small as the method allows, and the order $\lambda$ that gives it.

For one step, let $\mu_0 = N(0, \sigma^2)$ and $\mu = (1 - q)\mu_0 + q N(1, \sigma^2)$. The log moment of order $\lambda$ that the accountant uses is

$$\alpha(\lambda) = \ln E_{z \sim \mu}\left[\left(\frac{\mu(z)}{\mu_0(z)}\right)^{\lambda}\right] = \ln A_{\lambda + 1}, \qquad A_a = \sum_{k=0}^{a}\binom{a}{k}(1-q)^{a-k}q^k e^{(k^2 - k)/(2\sigma^2)}.$$

## The algorithm

```pseudo id=main
MOMENTS-ACCOUNTANT(q, sigma, T, delta, m)
L1  for lambda <- 1 to m do
L2      a <- lambda + 1
L3      t_k <- ln C(a, k) + (a - k) ln(1 - q) + k ln q + (k^2 - k)/(2 sigma^2)  for k = 0..a
L4      alpha <- LOG-SUM-EXP(t_0, ..., t_a)          ▷ alpha = ln A_a
L5      eps_lambda <- (T alpha + ln(1/delta)) / lambda
L6      keep the smallest eps_lambda and its lambda
L7  return the smallest eps_lambda and its lambda
```

Line L1 tries each integer order. Lines L2 and L3 write the $a + 1$ terms of the binomial sum $A_a$ as logs; a term with $q = 0$ or $q = 1$ that is 0 is left out. Line L4 adds the terms with the [log-sum-exp trick](/log-sum-exp-trick/): subtract the largest $t_k$, add the exponentials, take the log, and add the largest back. This is needed, because for small $\sigma$ and large $k$ the term $e^{(k^2 - k)/(2\sigma^2)}$ overflows a float. Line L5 applies the tail bound to the sum $T\alpha$ of the log moments of $T$ steps. Lines L6 and L7 return the best order.

The same sum gives $\delta$ for a fixed $\varepsilon$: $\delta = \min_\lambda e^{T\alpha(\lambda) - \lambda\varepsilon}$. The code has both directions.

The accountant does only arithmetic on public parameters; it does not touch data or draw noise. The training that it accounts for must draw its noise from a cryptographic source of randomness with an exact sampler, because float noise from a seeded generator leaks through its low-order bits (Mironov 2012; Canonne, Kamath and Steinke 2020). The [discrete Gaussian mechanism](/discrete-gaussian-mechanism/) page shows an exact sampler.

## Example

Take $q = 0.1$, $\sigma = 1$, $T = 10$, $\delta = 10^{-5}$ and $m = 8$, so $\ln(1/\delta) = 11.5129$. For $\lambda = 1$, the order is $a = 2$ and $A_2 = 1 + q^2(e^{1/\sigma^2} - 1) = 1.017183$, so $\alpha(1) = 0.017037$.

| $\lambda$ | $a$ (L2) | $\alpha(\lambda)$ (L4) | $T\alpha(\lambda)$ | $\varepsilon_\lambda$ (L5) | best so far (L6) |
|---|---|---|---|---|---|
| 1 | 2 | 0.017037 | 0.170369 | 11.6833 | 11.6833 at 1 |
| 2 | 3 | 0.063425 | 0.634246 | 6.0736 | 6.0736 at 2 |
| 3 | 4 | 0.176018 | 1.760178 | 4.4244 | 4.4244 at 3 |
| 4 | 5 | 0.519510 | 5.195097 | 4.1770 | 4.1770 at 4 |
| 5 | 6 | 1.855472 | 18.554718 | 6.0135 | 4.1770 at 4 |
| 6 | 7 | 5.068282 | 50.682817 | 10.3660 | 4.1770 at 4 |
| 7 | 8 | 9.648530 | 96.485299 | 15.4283 | 4.1770 at 4 |
| 8 | 9 | 15.304462 | 153.044625 | 20.5697 | 4.1770 at 4 |

Line L7 returns $\varepsilon = 4.177$ at $\lambda = 4$. Small orders pay too much for $\ln(1/\delta)/\lambda$; large orders pay too much for $T\alpha(\lambda)/\lambda$, which grows fast once the top terms of the sum, with their factor $e^{(k^2 - k)/(2\sigma^2)}$, beat the small factor $q^k$.

A second check, the setting of Abadi et al.: $q = 0.01$, $\sigma = 4$, $T = 10000$, $\delta = 10^{-5}$ and $m = 32$ give $\varepsilon = 1.2586$ at $\lambda = 19$. The paper reports about $1.26$.

## Correctness

**Theorem.** Let $\varepsilon^*$ be the output of MOMENTS-ACCOUNTANT$(q, \sigma, T, \delta, m)$. Then $T$ adaptively composed steps of the subsampled Gaussian mechanism, with Poisson rate $q$, clipping norm 1 and noise $N(0, \sigma^2 I)$, are $(\varepsilon^*, \delta)$-DP under add/remove neighbors.

The proof in [proofs/correctness.md](proofs/correctness.md) has four steps. First, lines L2 to L4 compute $\ln A_{\lambda + 1}$ exactly in the real RAM, by the binomial theorem and the identity $E_{\mu_0}[(\mu_1/\mu_0)^k] = e^{(k^2 - k)/(2\sigma^2)}$ for $\mu_1 = N(1, \sigma^2)$. Second, for one step and each pair of neighbors, the log moment of order $\lambda$ of the privacy loss is at most $\ln A_{\lambda + 1}$: for the neighbor with the extra record this follows by joint convexity and a reduction to one dimension, and for the other order it is a result of Mironov, Talwar and Zhang that we cite. Third, log moments add over adaptive steps, by conditioning on the earlier outputs. Fourth, Markov's inequality on $e^{\lambda Z}$ gives $\Pr[Z > \varepsilon_\lambda] \le \delta$, and a tail bound of this form implies $(\varepsilon_\lambda, \delta)$-DP. Each $\varepsilon_\lambda$ is valid, so their minimum is valid.

## Complexity

In the real RAM, order $\lambda$ costs $O(\lambda)$ operations at lines L3 and L4, so the whole run costs $\sum_{\lambda \le m} O(\lambda) = O(m^2)$ time and $O(m)$ extra space for the terms of one order. The cost does not depend on $T$, because composition is one multiplication by $T$. Abadi et al. used $\lambda \le 32$, so $m$ is small in practice. A float version needs the log-sum-exp form of line L4, or the terms overflow.

## Properties

- **Exact for its pair.** For integer orders, $\alpha(\lambda)$ is the exact log moment of the one-dimensional pair, not an approximation. The asymptotic form in the paper of Abadi et al., $q^2\lambda(\lambda + 1)/((1 - q)\sigma^2) + O(q^3\lambda^3/\sigma^3)$, holds only under conditions on $q$, $\sigma$ and $\lambda$, and has a hidden term; the finite sum has neither problem.
- **Additive.** The state of the accountant during training is one vector of $m$ numbers, $\sum_{\text{steps}}\alpha_{\text{step}}(\lambda)$. Steps with different $q$ or $\sigma$ simply add their own vectors.
- **Pure arithmetic.** It reads no data and has no randomness.
- **Monotone.** $\varepsilon^*$ grows with $T$ and $q$, and shrinks as $\sigma$ or $\delta$ grows.

## Variants and improvements

- **Fractional orders.** Mironov, Talwar and Zhang give a series for real orders $\alpha > 1$. A finer grid of orders gives a slightly smaller $\varepsilon$.
- **Better conversions.** The step from Renyi divergence to $(\varepsilon, \delta)$ in line L5 loses a little. Later conversions shave this loss.
- **Numerical accounting.** [Numerical privacy accounting](/numerical-privacy-accounting/) composes the full privacy loss distribution with the FFT, and gives an $\varepsilon$ within a stated error of the exact value, which is smaller than the moments bound.
- **GDP accounting.** The central limit theorem of [Gaussian differential privacy](/gaussian-differential-privacy/) gives a simple approximation for many steps, but it is not an upper bound in general.
- **Other sampling schemes.** Sampling a fixed batch size without replacement under replace neighbors has its own bound, which is not $A_a$.

## When to use it

Use the moments accountant, or an RDP accountant built the same way, for long runs of subsampled Gaussian steps, as in DP-SGD and federated learning with Gaussian noise. It is simple, fast, and always an upper bound. Use [numerical accounting](/numerical-privacy-accounting/) when the last few percent of $\varepsilon$ matter, and the [advanced composition theorem](/advanced-composition-theorem/) only for steps that have nothing but an $(\varepsilon, \delta)$ guarantee.

## Pitfalls

- **Wrong sampling scheme at line L3.** The sum $A_a$ is for Poisson sampling with add/remove neighbors. Many training loops shuffle the data and take fixed-size batches; the bound for that scheme is different, and reporting the Poisson number for it is an error.
- **Overflow at line L4.** Adding $e^{t_k}$ directly overflows for small $\sigma$ and large $\lambda$. Use log-sum-exp, as in the pseudocode.
- **Too few orders at line L1.** If the best order is $m$ itself, the minimum may lie beyond $m$; raise $m$ and run again.
- **Clipping not enforced.** The bound assumes that each record changes the sum by at most 1 in $\ell_2$ norm. If the clip norm is $C$, the noise must be $N(0, \sigma^2C^2 I)$, and $\sigma$ in the accountant is the ratio.
- **Only one order of the pair.** Abadi et al. take the maximum of the two orders of the privacy loss. The formula here uses only the order with the extra record, which is correct because Mironov, Talwar and Zhang proved that it dominates. A homemade variant for another mechanism must check both orders.

## Implementations

## History

Abadi, Chu, Goodfellow, McMahan, Mironov, Talwar and Zhang introduced the moments accountant in 2016 to train neural networks with differential privacy. They bounded the log moments for small $q$ and computed them by numerical integration, and their example of $\varepsilon \approx 1.26$ against $9.34$ for strong composition showed how much the method saves. Mironov's Renyi differential privacy (2017) gave the general framework, in which the log moment of order $\lambda$ is $\lambda D_{\lambda + 1}$. Mironov, Talwar and Zhang (2019) derived the exact binomial sum for integer orders, a series for fractional orders, and the proof that one order dominates the other. RDP accountants of this form are in the main open source DP-SGD libraries.

## References
