---
tag: HVTX47
kind: algorithm
slug: randomized-smoothing
name: Randomized smoothing
aliases:
- Gaussian smoothing certificate
area: security-and-privacy/adversarial-machine-learning
level: advanced
summary: Classifies by the majority label under Gaussian noise and certifies an l2 radius from the gap between the top two class probabilities.
model: real-ram
complexity:
  vars: {n: the number of noise samples of both stages, c: the cost of one call of the base classifier, d: the input dimension, k: the number of labels}
  time: {worst: O(n (c + d))}
  space: {extra: O(d + k)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2019
  people: [Jeremy Cohen, Elan Rosenfeld, J. Zico Kolter, Mathias Lecuyer, Suman Jana]
  note: Lecuyer et al. certified noisy classifiers through differential privacy (IEEE S&P 2019), and Cohen, Rosenfeld and Kolter (ICML 2019) proved the tight l2 radius for Gaussian noise and gave the PREDICT and CERTIFY procedures.
prereqs: [adversarial-example, clopper-pearson-interval, neyman-pearson-lemma]
see_also: [neural-network-verification-problem, interval-bound-propagation, linear-bound-propagation, clopper-pearson-interval, neyman-pearson-lemma, binomial-test, gaussian-mechanism, adversarial-training]
sources:
  - url: https://proceedings.mlr.press/v97/cohen19c.html
    title: Jeremy Cohen, Elan Rosenfeld and J. Zico Kolter, Certified adversarial robustness via randomized smoothing, ICML 2019, PMLR 97, pages 1310 to 1320
    locator: Theorem 1 (the robustness radius), Theorem 2 (its tightness), the PREDICT and CERTIFY procedures with their guarantees, and the experiments on ImageNet
  - url: https://arxiv.org/abs/1802.03471
    title: Mathias Lecuyer, Vaggelis Atlidakis, Roxana Geambasu, Daniel Hsu and Suman Jana, Certified robustness to adversarial examples with differential privacy, IEEE S&P 2019
    locator: PixelDP, the first certificate for a classifier with a noise layer, from the stability guarantee of differential privacy
  - url: https://arxiv.org/abs/1902.06705
    title: Nicholas Carlini, Anish Athalye, Nicolas Papernot, Wieland Brendel, Jonas Rauber, Dimitris Tsipras, Ian Goodfellow, Aleksander Madry and Alexey Kurakin, On evaluating adversarial robustness, arXiv 2019
    locator: certified robust accuracy as a lower bound and attacks as an upper bound
  - paper: "Battista Biggio and Fabio Roli, Wild patterns: Ten years after the rise of adversarial machine learning, Pattern Recognition 84, pages 317 to 331, 2018"
    locator: the threat model in three parts used on this page
---

Randomized smoothing turns any base classifier $f$ into a smoothed classifier $g$ that returns the label that $f$ gives most often when Gaussian noise is added to the input: $g(x) = \arg\max_c P(f(x + \eta) = c)$ with $\eta \sim N(0, \sigma^2 I)$. Cohen, Rosenfeld and Kolter (2019) proved that if the top label $c_A$ has probability at least $p_A$ and every other label at most $p_B$, then $g$ is constant on the $\ell_2$ ball of radius $R = \frac{\sigma}{2}(\Phi^{-1}(p_A) - \Phi^{-1}(p_B))$ around $x$, where $\Phi^{-1}$ is the quantile function of the standard normal distribution. The probabilities are not known, so the CERTIFY procedure estimates a lower bound of $p_A$ from samples, and the certificate holds with probability at least $1 - \alpha$ over the samples. The certificate is for $g$, not for $f$, and it works for any $f$, of any size, because it needs only calls of $f$.

**Threat model.** Randomized smoothing is a defense with a certificate. The goal can be untargeted or targeted, since the certificate rules out every other label. The knowledge is unlimited: the attacker may know $f$, $\sigma$ and the procedure, but not the noise draws of the defender. The capability is a change at test time with $\lVert \delta \rVert_2 < R$, where $R$ is the certified radius of the point.

## In plain words

Take any classifier and do not trust its answer on one input. Instead, add random noise to the input many times, ask the classifier each time, and report the answer that comes back most often.

Noise blurs the inputs, so moving the input a little changes the vote only a little. If one answer wins the vote by a clear margin, a small move of the input cannot make another answer win. The bigger the margin and the noise, the bigger the safe distance.

The vote is counted from a finite number of samples, so the method uses a careful lower estimate of the share of the winner. The guarantee is about the voting classifier, not about the original one, and it can fail with a small, known probability, such as one in a thousand.

## The problem

Given a base classifier $f : \mathbb{R}^d \to \{1, \dots, k\}$, a noise level $\sigma > 0$ and an input $x$, define $g(x) = \arg\max_c P(f(x + \eta) = c)$ for $\eta \sim N(0, \sigma^2 I)$. Return a label $c_A$ and a radius $R > 0$ such that $g(x + \delta) = c_A$ for every $\lVert \delta \rVert_2 < R$, or abstain. Only calls of $f$ are allowed, so the answer must hold with probability at least $1 - \alpha$ over the noise draws. The perturbation set is the $\ell_2$ ball $B_2(x, R)$.

## The algorithm

```pseudo id=main
CERTIFY(f, sigma, x, n_0, n, alpha)
L1  counts_0 ← SAMPLE-UNDER-NOISE(f, x, n_0, sigma)
L2  c_A ← the label with the most counts in counts_0      ▷ only a guess of the top label
L3  counts ← SAMPLE-UNDER-NOISE(f, x, n, sigma)            ▷ fresh, independent samples
L4  p_A ← LOWER-CONF-BOUND(counts[c_A], n, 1 - alpha)      ▷ one-sided Clopper-Pearson bound
L5  if p_A > 1/2 then
L6      return (c_A, sigma · Φ^-1(p_A))
L7  return ABSTAIN
SAMPLE-UNDER-NOISE(f, x, n, sigma)
L8  for i ← 1 to n do
L9      eta ← a draw from N(0, sigma^2 I)
L10     counts[f(x + eta)] ← counts[f(x + eta)] + 1
L11 return counts
PREDICT(f, sigma, x, n, alpha)
L12 counts ← SAMPLE-UNDER-NOISE(f, x, n, sigma)
L13 c_A, c_B ← the two labels with the most counts
L14 if BINOMIAL-P-VALUE(counts[c_A], counts[c_A] + counts[c_B], 1/2) <= alpha then return c_A
L15 return ABSTAIN
```

Lines L1 and L2 pick the label to certify from a small sample. Line L3 draws a new sample, so the count of $c_A$ in it is a binomial variable whose success probability is the true $p_A = P(f(x + \eta) = c_A)$. Line L4 takes the one-sided [Clopper-Pearson](/clopper-pearson-interval/) lower bound: the number $\underline p_A$ with $P(\mathrm{Bin}(n, \underline p_A) \ge n_A) = \alpha$. Line L6 uses the bound $p_B \le 1 - \underline p_A$, which turns the radius of the theorem into $\sigma \Phi^{-1}(\underline p_A)$. If $\underline p_A \le 1/2$, no radius is certified.

PREDICT only returns the label. Line L14 is a two-sided [binomial test](/binomial-test/) of whether $c_A$ beats $c_B$; if the test is not significant, the procedure abstains, and a returned label differs from $g(x)$ with probability at most $\alpha$.

## Example

The check value: with $\sigma = 0.5$, $p_A = 0.9$ and $p_B = 0.1$, the radius is $R = \frac{0.5}{2}(\Phi^{-1}(0.9) - \Phi^{-1}(0.1)) = 0.25 \cdot 2 \cdot 1.28155 = 0.64078$.

The table shows line L4 and line L6 for $\sigma = 0.5$ and $\alpha = 0.001$, for several counts $n_A$ of the top label among $n$ samples.

| $n_A$ | $n$ | $n_A / n$ | $\underline p_A$ (line L4) | radius (line L6) |
|---|---|---|---|---|
| 550 | 1000 | 0.55 | 0.50068 | 0.00085 |
| 600 | 1000 | 0.60 | 0.55108 | 0.06419 |
| 900 | 1000 | 0.90 | 0.86746 | 0.55724 |
| 9000 | 10000 | 0.90 | 0.89041 | 0.61436 |
| 1000 | 1000 | 1.00 | 0.99312 | 1.23163 |
| 100000 | 100000 | 1.00 | 0.99993 | 1.90573 |

With the same share $0.9$ of votes, more samples move $\underline p_A$ closer to $0.9$ and the radius closer to the check value $0.64078$. Even with every vote for $c_A$, the radius is bounded: $\underline p_A = \alpha^{1/n}$, so for large $n$ the radius grows only like $\sigma \sqrt{2 \ln n}$, very slowly.

For a linear base classifier $f(x) = [w^\top x + b > 0]$ the smoothed classifier is the same as $f$, and the exact $p_A$ is $\Phi(|w^\top x + b| / (\sigma \lVert w \rVert_2))$, so $\sigma \Phi^{-1}(p_A)$ is exactly the distance from $x$ to the hyperplane. For $w = (3, 4)$, $b = -1$, $x = (0.6, 0.2)$ and $\sigma = 0.5$, $p_A = \Phi(0.64) = 0.73891$ and the radius is $0.32$, the distance to the boundary. So the theorem is tight.

## Correctness

**Theorem (Cohen, Rosenfeld and Kolter 2019).** Let $p_A \le P(f(x + \eta) = c_A)$ and $\max_{c \ne c_A} P(f(x + \eta) = c) \le p_B$ with $p_A > p_B$. Then $g(x + \delta) = c_A$ for every $\lVert \delta \rVert_2 < \frac{\sigma}{2}(\Phi^{-1}(p_A) - \Phi^{-1}(p_B))$.

**Corollary (CERTIFY).** With probability at least $1 - \alpha$ over the samples of lines L1 to L3, if CERTIFY returns $(c_A, R)$, then $g(x + \delta) = c_A$ for every $\lVert \delta \rVert_2 < R$.

The theorem follows from the [Neyman-Pearson lemma](/neyman-pearson-lemma/) for the two Gaussians $N(x, \sigma^2 I)$ and $N(x + \delta, \sigma^2 I)$: among all sets with probability $p_A$ under the first, a half-space orthogonal to $\delta$ has the least probability under the second, and that probability is $\Phi(\Phi^{-1}(p_A) - \lVert \delta \rVert_2 / \sigma)$. The top label keeps more than half of the mass, which is more than any other label can have, as long as $\lVert \delta \rVert_2 < \sigma \Phi^{-1}(p_A)$. For the corollary, the label of line L2 is fixed before line L3 draws its samples, and the Clopper-Pearson bound is below the true probability with probability at least $1 - \alpha$; a smaller $p_A$ gives a smaller radius. The full proof is in `proofs/correctness.md`.

## Complexity

- **Time.** $n_0 + n$ calls of $f$, plus $O(d)$ per noise draw, so $O(n(c + d))$ for $n$ samples in total. Line L4 costs $O(n)$ per step of a bisection. For an ImageNet model, Cohen et al. used $n = 100000$, so one certificate costs as much as 100000 forward passes.
- **Space.** $O(d + k)$ for one noisy input and the counts.
- **Samples against radius.** The largest radius that $n$ samples can certify grows like $\sigma\sqrt{2 \ln n}$, so a larger radius needs a larger $\sigma$ more than more samples.

## Properties

- **Probabilistic.** The certificate holds with probability at least $1 - \alpha$ over the defender's noise (a theorem about the procedure). Over $N$ test points, the expected number of wrong certificates is at most $\alpha N$.
- **Model-agnostic.** Only calls of $f$ are needed, so it scales to networks that no exact or bound-based verifier can handle.
- **Tight in $\ell_2$.** For a linear base classifier the radius equals the true distance to the boundary (Theorem 2 of Cohen et al.), so the bound cannot be improved using $p_A$ and $p_B$ alone.
- **A lower bound on robust accuracy of $g$.** The fraction of test points with a correct label and a radius above $r$ is a lower bound (with high probability) on the robust accuracy of $g$ at $\ell_2$ radius $r$, the certified accuracy. It says nothing about $f$.
- **Weak in $\ell_\infty$.** An $\ell_2$ radius $R$ gives an $\ell_\infty$ radius of only $R/\sqrt d$, which is small for images.
- **Accuracy costs.** The noise lowers the clean accuracy of $g$, more for a larger $\sigma$, so $\sigma$ trades accuracy for radius.

## Variants and improvements

- **Training with noise.** The base classifier should be trained on noisy inputs with the same $\sigma$; otherwise $f$ is near random under noise and $g$ abstains. Salman et al. (2019) train it with adversarial examples of the smoothed classifier and get larger certified radii.
- **PixelDP.** Lecuyer et al. (2019) add a noise layer and use the stability bound of [differential privacy](/differential-privacy-definition/), in the spirit of the [Gaussian mechanism](/gaussian-mechanism/), to certify; the radius is looser than the one of Cohen et al.
- **Other noise and other norms.** Uniform or Laplace noise gives certificates in $\ell_1$, and other distributions give other norms; the tight radius for each comes from a Neyman-Pearson argument for that noise.
- **Better confidence bounds.** Any valid one-sided lower confidence bound works at line L4; Clopper-Pearson is exact for the binomial and is the usual choice.
- **Abstain or answer.** PREDICT can abstain when the vote is close; it never needs a radius. In use, PREDICT runs at test time and CERTIFY is used to report certified accuracy.

## When to use it

Use randomized smoothing when the model is too large for [interval bound propagation](/interval-bound-propagation/) or [linear bound propagation](/linear-bound-propagation/), when a probabilistic guarantee is acceptable, and when the threat is an $\ell_2$ change. Do not use it when every prediction must be cheap, since each one costs many forward passes, or when the threat is an $\ell_\infty$ change of fixed size in high dimension. For small networks and an exact answer, use [Reluplex](/reluplex/).

## Pitfalls

- **The same samples for the guess and the bound.** If line L3 reuses the samples of line L1, the label is chosen to look good on the same data, and the bound of line L4 is no longer valid. Keep the two samples independent.
- **The point estimate in place of the bound.** Using $n_A / n$ at line L4 gives a radius that is too large about half the time. Line L4 must use a lower confidence bound.
- **A certificate for the base classifier.** The radius is for $g$. The base classifier $f$ can have adversarial examples very close to $x$, and an attack on $f$ is no counterexample to the certificate.
- **Clipped noise.** Clipping $x + \eta$ to $[0,1]^d$ at line L9 changes the noise distribution, and the theorem, which needs Gaussian noise, no longer applies as stated. Clipping inside $f$ is fine, because it is then part of the base classifier.
- **Too few samples.** With small $n$, line L4 gives a bound well below $n_A / n$, and many points abstain at line L7. Cohen et al. use $n_0 = 100$ and $n = 100000$ for this reason.
- **Reading $1 - \alpha$ for the whole test set.** The level holds for each point on its own. Over many points some certificates are wrong, about $\alpha N$ in expectation.

## Implementations

The code of this page is an abstract model on synthetic data. The base classifiers are linear models with given weights and two-layer ReLU networks from `mlkit.tiny_relu_net`, and the inputs are seeded random points. It never reads real data or touches a real system. The tests check the value $0.64078$, the binomial tail against a direct sum, that the Clopper-Pearson bound meets $\alpha$ and covers the true probability with level $1 - \alpha$ exactly over all outcomes, that the exact radius of a linear model is the distance to its boundary, that the certified radius of CERTIFY is at most that distance on all but a few of 60 points, that the exact smoothed label is constant inside each certified ball, and that points on the boundary abstain.

## History

Adding noise to inputs at test time was proposed as a heuristic defense several times, and some such defenses were later broken. Lecuyer et al. posted PixelDP in February 2018 (IEEE S&P 2019): a noise layer with a guarantee from differential privacy, the first certificate of this kind that scaled to ImageNet. Li et al. (2019) gave a tighter bound with Rényi divergence. Cohen, Rosenfeld and Kolter (ICML 2019) proved the tight $\ell_2$ radius for Gaussian noise with the Neyman-Pearson lemma, separated the smoothed classifier from the base classifier, and gave the sampling procedures with their statistical guarantees. They reported certified accuracy on ImageNet at $\ell_2$ radii where no other certificate worked (a measurement on their models). Later work trained better base classifiers and extended the method to other norms and to other kinds of data.

## References
