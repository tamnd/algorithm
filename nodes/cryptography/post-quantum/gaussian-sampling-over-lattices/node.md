---
tag: MWVGYZ
kind: algorithm
slug: gaussian-sampling-over-lattices
name: Gaussian sampling over lattices
aliases:
- discrete Gaussian sampler
- GPV sampler
- Klein sampler
- randomized nearest plane
area: cryptography/post-quantum
level: advanced
summary: "Sampling a lattice point with probability proportional to exp(-pi |v - c|^2 / s^2), from a basis: Klein's randomized nearest plane, Peikert's convolution sampler, and samplers over the integers."
model: word-ram
complexity:
  vars: {n: the lattice dimension}
  time: {worst: ∞, average: Θ(n^2), best: Θ(n^2)}
  space: {extra: Θ(n^2)}
properties: {deterministic: false, randomized: true}
history:
  year: 2008
  people: [Philip Klein, Craig Gentry, Chris Peikert, Vinod Vaikuntanathan]
  note: Klein gave the randomized nearest plane algorithm in 2000 for decoding. Gentry, Peikert and Vaikuntanathan proved in 2008 that it samples the discrete Gaussian. Peikert gave a parallel sampler in 2010.
prereqs: [lattice-basis, gram-schmidt-orthogonalization, babai-nearest-plane, rejection-sampling]
see_also: [gpv-signature, falcon, trapdoor-sampling-lattices, inverse-transform-sampling, timing-attack, closest-vector-problem, alias-method, fiat-shamir-with-aborts]
sources:
  - paper: doi:10.1145/1374376.1374407
    title: Craig Gentry, Chris Peikert and Vinod Vaikuntanathan, Trapdoors for hard lattices and new cryptographic constructions, STOC 2008
    locator: "Section 4 (SampleZ by rejection, SampleD as a randomized nearest plane, and the theorem that SampleD is close to D_{L,s,c} when s >= |B~| omega(sqrt(log n)))"
  - paper: "Philip Klein, Finding the closest lattice vector when it's unusually close, SODA 2000, pages 937 to 941"
    title: Philip Klein, Finding the closest lattice vector when it's unusually close, SODA 2000
    locator: the randomized rounding of each nearest plane step
  - paper: doi:10.1137/S0097539705447360
    title: Daniele Micciancio and Oded Regev, Worst-case to average-case reductions based on Gaussian measures, SIAM Journal on Computing 37(1), 2007
    locator: "the definition of the smoothing parameter, Lemma 3.3 (the bound with lambda_n and sqrt(ln(2n(1+1/eps))/pi)), Lemma 4.4 (the tail bound)"
  - paper: doi:10.1007/978-3-642-14623-7_5
    title: Chris Peikert, An efficient and parallel Gaussian sampler for lattices, CRYPTO 2010
    locator: "the convolution theorem, the offline perturbation and the online randomized rounding"
---

A discrete Gaussian over a lattice $\Lambda$ gives each lattice point $v$ a probability proportional to $\exp(-\pi \|v - c\|^2 / s^2)$, where $c$ is a center and $s$ a width. Sampling it is the core step of [GPV signatures](/gpv-signature/), [Falcon](/falcon/), lattice trapdoors, identity-based encryption and many security proofs. Given a basis $B$ of $\Lambda$, Klein's randomized nearest plane algorithm does it in $n$ steps: like [Babai's nearest plane](/babai-nearest-plane/), it walks the [Gram-Schmidt](/gram-schmidt-orthogonalization/) vectors from last to first, but instead of rounding each coefficient to the nearest integer it samples the coefficient from a one-dimensional discrete Gaussian. Gentry, Peikert and Vaikuntanathan (2008) proved that the output is close to the true distribution when $s$ is a little larger than the longest Gram-Schmidt vector, so the output does not reveal the basis. This page covers the lattice sampler and the integer samplers it uses; the trapdoors that supply the short basis are on the [trapdoor sampling](/trapdoor-sampling-lattices/) page.

**Notation.** $\rho_{s,c}(x) = \exp(-\pi \|x - c\|^2 / s^2)$, and $D_{\Lambda, s, c}(v) = \rho_{s,c}(v) / \rho_{s,c}(\Lambda)$ for $v \in \Lambda$. The width $s$ relates to the standard deviation by $\sigma = s / \sqrt{2\pi}$. $B = (b_1, \dots, b_n)$ is a basis, $\tilde b_i$ its Gram-Schmidt vectors and $\|\tilde B\| = \max_i \|\tilde b_i\|$. The smoothing parameter $\eta_\varepsilon(\Lambda)$ is the smallest $s$ with $\rho_{1/s}(\Lambda^* \setminus \{0\}) \le \varepsilon$, where $\Lambda^*$ is the [dual lattice](/dual-lattice/). $\tau$ is a tail cut, a number of standard deviations.

## In plain words

We want a random lattice point near a target, where closer points are more likely, following a bell curve. We also want the result to say nothing about which basis we used.

The method works one direction at a time. It looks at the last basis direction, finds how far along it the target lies, and picks a whole number near that, at random, with a bell curve whose width fits the length of that direction. It subtracts that many copies of the basis vector from the target and goes to the next direction.

Each one-dimensional pick can be made with a lookup table, or by trying random numbers and keeping each with the right probability.

## The problem

Input: a basis $B$ of a lattice $\Lambda \subset \mathbb{R}^n$, a center $c \in \mathbb{R}^n$ and a width $s$. Output: a lattice point $v$ distributed as $D_{\Lambda, s, c}$, or within a small statistical distance of it. The output must not depend on which basis of $\Lambda$ was used, as long as the basis is short enough for $s$. For a signature this is what makes signatures safe to publish; compare the [closest vector problem](/closest-vector-problem/), where one wants a single nearest point and the answer may leak the basis.

## The algorithm

```pseudo id=main
CDT SETUP(s)                                    ▷ D_{Z,s} with center 0, support [−τσ, τσ]
L1  T[i] ← Σ_{x ≤ x_i} ρ_s(x) / Σ_x ρ_s(x)  for the support points x_1 < … < x_N
CDT SAMPLE()
L2  u ← uniform in [0, 1);  return the first x_i with T[i] ≥ u   ▷ binary search

SAMPLEZ(s, c)                                   ▷ D_{Z,s,c} by rejection
L3  x ← uniform integer in [c − τσ, c + τσ]
L4  with probability ρ_{s,c}(x) return x;  else go to L3

KLEIN(B, s, c)                                  ▷ randomized nearest plane
L5  b̃_1, …, b̃_n ← Gram-Schmidt(B)               ▷ once per basis
L6  v ← 0;  c' ← c
L7  for i ← n down to 1
L8      c_i ← ⟨c', b̃_i⟩ / ‖b̃_i‖²;  s_i ← s / ‖b̃_i‖
L9      z_i ← SAMPLEZ(s_i, c_i)
L10     c' ← c' − z_i b_i;  v ← v + z_i b_i
L11 return v
```

**The integer samplers.** CDT (lines L1 and L2) is [inverse transform sampling](/inverse-transform-sampling/) with a table; it works for a fixed $s$ and center, and other centers need a table per center or a combination with rejection. Rejection (lines L3 and L4) works for any $s$ and $c$, with about $2\tau\sigma / \rho_s(\mathbb{Z}) \approx 2\tau/\sqrt{2\pi}$ trials on average, about 10 for $\tau = 12$. The Knuth-Yao sampler walks a discrete distribution generating tree over the binary expansions of the probabilities and uses close to the minimum number of random bits. The Bernoulli sampler of BLISS and the sampler of Falcon combine a small base table with a rejection step $\exp(-x)$ computed in constant time. All of them must cut the tail at some $\tau$ and compute probabilities with finite precision; both errors must be below the security target, which can be measured with statistical distance or, more tightly, with the Rényi divergence.

**Klein's algorithm.** Lines L7 to L10 are Babai's nearest plane with line L9 in place of rounding $c_i$. The width $s_i = s / \|\tilde b_i\|$ makes the step in the direction of $\tilde b_i$ have width $s$ in space.

**Peikert's sampler.** Klein's algorithm is sequential and needs the Gram-Schmidt vectors. Peikert (2010) instead adds a continuous Gaussian perturbation $p$ with covariance $s^2 I - s_1^2 B B^\mathsf{T}$, prepared offline, and then rounds $B^{-1}(c - p)$ coordinate by coordinate with independent integer samples, which can run in parallel. The convolution of the two Gaussians is the spherical $D_{\Lambda, s, c}$. The price is a larger width: $s$ must exceed the largest singular value of $B$ times the smoothing parameter of $\mathbb{Z}$, not only $\|\tilde B\|$ times it.

## Example

**An integer CDT.** For $s = 2$ (so $\sigma \approx 0.80$), the weights $\rho_2(x) = e^{-\pi x^2 / 4}$ sum to about $2.00001$ over $\mathbb{Z}$, and the probabilities are $0.5$ at $0$, $0.228$ at $\pm 1$, $0.0216$ at $\pm 2$ and $0.0004$ at $\pm 3$. The cumulative table starts $0.0004, 0.0220, 0.2500, 0.7500, 0.9780, 0.9996$. A uniform $u = 0.6$ falls in the cell of $0$, and $u = 0.9$ in the cell of $1$.

**Klein in dimension 2.** Take $b_1 = (2, 1)$ and $b_2 = (1, 3)$, a lattice of determinant 5. Gram-Schmidt gives $\tilde b_1 = (2, 1)$ and $\tilde b_2 = (1, 3) - 1 \cdot (2, 1) = (-1, 2)$, both of squared length 5. With $s = 9$ and $c = (0.5, 0.25)$, every $s_i = 9 / \sqrt 5 \approx 4.02$. For $i = 2$, $c_2 = \langle c, (-1, 2) \rangle / 5 = 0$. Say line L9 returns $z_2 = 1$; then $c' = (-0.5, -2.75)$. For $i = 1$, $c_1 = \langle c', (2, 1) \rangle / 5 = -0.75$. Say $z_1 = -1$; the output is $v = b_2 - b_1 = (-1, 2)$. The tests draw 12000 samples this way and compare their counts with $D_{\Lambda, 9, c}$ by a chi-square test.

**The smoothing parameter of $\mathbb{Z}$.** For $\varepsilon = 2^{-64}$, $\eta_\varepsilon(\mathbb{Z}) \le \sqrt{\ln(2(1 + 2^{64})) / \pi} \approx 3.79$. So a width $s \ge 3.79 \cdot \|\tilde B\|$ is enough for each step of Klein's algorithm.

## Correctness

Each step adds an integer multiple of a basis vector, so the output is in $\Lambda$. Let $v = \sum_i z_i b_i$. Since $\tilde b_i$ is orthogonal to $b_1, \dots, b_{i-1}$ and $\langle b_i, \tilde b_i \rangle = \|\tilde b_i\|^2$, the probability of the path is a product of one-dimensional Gaussian weights, and their exponents add up to $-\pi \|v - c\|^2 / s^2$. The normalizing factor of step $i$ is $\rho_{s_i}(\mathbb{Z} - c_i)$, which depends on $c_i$; when $s_i \ge \eta_\varepsilon(\mathbb{Z})$ it lies within a factor $(1 \pm \varepsilon)$ of $s_i$, whatever the center. So the output distribution is within a factor $((1 + \varepsilon)/(1 - \varepsilon))^n$ of $D_{\Lambda, s, c}$ at every point. The full proof is in the proof file.

## Complexity

Gram-Schmidt costs $\Theta(n^3)$ once per basis and the table $\Theta(n^2)$ of storage. Each sample does $n$ steps with an inner product and a vector update of length $n$, so $\Theta(n^2)$ arithmetic operations, plus $n$ integer samples. The rejection sampler has a constant expected number of trials but no worst case bound, so the worst case is unbounded; a CDT sample costs $O(\log(\tau \sigma))$ comparisons. Peikert's sampler needs $\Theta(n^2)$ online work with $n$ independent integer samples that can run in parallel. With ring structure, Falcon's fast Fourier sampler does the same work as Klein in $O(n \log n)$.

## Properties

- **The basis does not leak.** Above the threshold, the output distribution depends only on $\Lambda$, $s$ and $c$, not on $B$.
- **Quality.** Klein's sampler needs $s \ge \|\tilde B\| \cdot \eta_\varepsilon(\mathbb{Z})$, which is the best known for a general basis; better bases give narrower samples and shorter signatures.
- **Short outputs.** For $s \ge \eta_\varepsilon(\Lambda)$, $\|v - c\| \le s \sqrt n$ except with probability about $2^{-n}$.
- **Not exact.** Klein's output is within a small factor of the target; the tail cut and floating point add further small errors.

## Variants and improvements

- **Peikert's convolution sampler (2010)** for parallel and offline/online sampling.
- **Fast Fourier sampling** (Ducas and Prest, 2016) for NTRU lattices, used by Falcon.
- **Sampling for q-ary lattices with a gadget** (Micciancio and Peikert, 2012), where the sampler for $G$ is simple and a perturbation handles the trapdoor; see [trapdoor sampling](/trapdoor-sampling-lattices/).
- **Integer samplers:** CDT, Knuth-Yao, Bernoulli and rejection, and constant-time versions; the [alias method](/alias-method/) also works for a fixed table.
- **Continuous to discrete:** the rounded Gaussian, a continuous sample rounded to an integer, is simpler but is not a discrete Gaussian and needs its own analysis.

## When to use it

Use a lattice Gaussian sampler wherever a secret short basis is used to produce public outputs: hash-and-sign signatures, identity-based and attribute-based encryption, and trapdoor delegation. Use an integer sampler for the noise of LWE-style schemes when a Gaussian is required, though most standards now use the centered binomial or uniform noise, which are easier to make constant time. For a single nearest point with no privacy need, use Babai's algorithm.

## Pitfalls

- **Timing and cache leaks.** Table lookups, rejection loops and branches depend on secret values. The cache attack of Groot Bruinderink, Hülsing, Lange and Yarom (2016) recovered BLISS keys from its Gaussian sampler. See [timing attack](/timing-attack/).
- **Width too small.** If $s$ is below $\|\tilde B\| \cdot \eta$, the output depends on $B$ and leaks it.
- **Tail cut and precision.** Too small a $\tau$ or too few bits of precision change the distribution in a way an attacker can measure over many signatures.
- **Wrong parameter convention.** Papers use $s$, $\sigma = s / \sqrt{2\pi}$, or $\sigma$ as the parameter in $\exp(-x^2 / (2\sigma^2))$; mixing them changes the width by a factor $\sqrt{2\pi}$.

## Implementations

The Python code on this page has a CDT sampler for $D_{\mathbb{Z}, s}$, a rejection sampler for $D_{\mathbb{Z}, s, c}$ with any center, exact Gram-Schmidt with fractions, Klein's sampler, and the bound on $\eta_\varepsilon(\mathbb{Z})$. Peikert's sampler and Knuth-Yao are not implemented. **There is no official vector:** a sampler is random, so the tests are statistical with fixed seeds. They compare counts with the exact probabilities by a chi-square test with a loose limit, check the variance $s^2 / (2\pi)$ and the mean of a shifted sampler, check that every Klein output is a lattice point, and compare Klein's output in dimension 2 with $D_{\Lambda, s, c}$. The code is for study only: it uses floating point, branches on secret values, and is not constant time.

## History

Klein (SODA 2000) gave the randomized version of nearest plane to find a closest vector when the target is unusually close, by repeating random runs. Micciancio and Regev (2004, published 2007) defined the smoothing parameter for their worst-case to average-case reductions. Gentry, Peikert and Vaikuntanathan (STOC 2008) showed that Klein's algorithm samples the discrete Gaussian and used it for signatures and identity-based encryption; they also gave the rejection sampler over $\mathbb{Z}$. Peikert (CRYPTO 2010) gave the convolution sampler. Later work made the integer samplers fast and constant time, and Ducas and Prest (2016) gave the fast Fourier sampler used in Falcon.

## References
