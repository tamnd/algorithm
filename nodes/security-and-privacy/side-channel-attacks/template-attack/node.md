---
tag: 9Z5T63
kind: algorithm
slug: template-attack
name: Template attack
aliases:
- profiled side-channel attack
area: security-and-privacy/side-channel-attacks
level: advanced
summary: "Builds multivariate Gaussian templates of the leakage of each intermediate value on a copy of the device, then ranks the key guesses of the target by maximum likelihood."
model: real-ram
complexity:
  vars: {n: the number of profiling traces, m: the number of attack traces, T: the number of samples in each trace, g: the number of key guesses, V: the number of template classes}
  time: {worst: Θ(n T² + V T³ + g m T²), average: Θ(n T² + V T³ + g m T²), best: Θ(n T² + V T³ + g m T²)}
  space: {extra: Θ(V T² + g)}
history:
  year: 2002
  people: [Suresh Chari, Josyula R. Rao, Pankaj Rohatgi]
  note: "Chari, Rao and Rohatgi introduced template attacks at CHES 2002, with a multivariate Gaussian model of the noise learned on a device that the attacker controls."
prereqs: [correlation-power-analysis, maximum-likelihood-estimation, covariance-matrix]
see_also: [side-channel-key-rank-estimation, mutual-information-analysis, quadratic-discriminant-analysis, linear-discriminant-analysis, principal-component-analysis, cholesky-decomposition, bayes-theorem, naive-bayes-classifier]
sources:
  - paper: "Suresh Chari, Josyula R. Rao and Pankaj Rohatgi, Template attacks, CHES 2002, LNCS 2523, pages 13 to 28"
    locator: "the profiling step (a mean and a noise covariance for each value), the choice of points of interest, and the maximum likelihood classification"
  - paper: "Stefan Mangard, Elisabeth Oswald and Thomas Popp, Power Analysis Attacks, Springer, 2007, ISBN 978-0-387-30857-9"
    locator: "Chapter 4 (the multivariate Gaussian model of power traces) and Chapter 5, pages 101 to 118 (template attacks on a single trace)"
  - paper: doi:10.1007/978-3-642-01001-9_26
    title: "François-Xavier Standaert, Tal G. Malkin and Moti Yung, A unified framework for the analysis of side-channel key recovery attacks, EUROCRYPT 2009, LNCS 5479, pages 443 to 461"
    locator: the definitions of the success rate and the guessing entropy, and the profiled adversary
  - paper: doi:10.1007/978-3-540-74735-2_31
    title: "Andrey Bogdanov and others, PRESENT, an ultra-lightweight block cipher, CHES 2007, LNCS 4727"
    locator: the description of the substitution layer (the table of the 4-bit S-box used in the examples of this page)
---

A template attack is a side-channel attack in two phases. In the profiling phase the attacker uses a copy of the device with a known key and learns, for each value of a key-dependent intermediate, the mean trace and the [covariance matrix](/covariance-matrix/) of the noise: a multivariate Gaussian "template". In the attack phase it scores each key guess by the likelihood of the target's traces under the templates that the guess selects, and keeps the guess with the largest likelihood. With exact templates this maximum likelihood rule has the highest success probability of all rules on the same traces, which makes the template attack the reference for the strongest attacker in a stated model. Chari, Rao and Rohatgi (2002) introduced it.

## In plain words

First, the attacker gets a copy of the chip and sets the key itself. It records the power many times and sorts the recordings by the value the chip was handling, which it knows. For each value it writes down what a typical recording looks like and how the noise usually moves, for example that two moments in a recording tend to go up together. That is the template. Then it records the real chip a few times. For each key guess, it asks how well the new recordings fit the templates that this guess says should apply. A right guess explains the recordings well, and a wrong guess explains them badly. The guess with the best fit wins, often after very few recordings.

## The problem

The attacker is a profiling adversary. It has a copy of the device on which it can choose the key and the inputs, and it sees the target device on $m$ known inputs. In the model of this page, for the value $v = S(p \oplus k)$, where $S$ is the 4-bit S-box of PRESENT, a trace has $T = 2$ samples:

$$\ell = \mu_v + N, \qquad \mu_v = \Big(\mathrm{HW}(v),\ \sum_{b=0}^{3} w_b v_b\Big), \qquad N \sim \mathcal{N}(0, \Sigma), \quad \Sigma = \sigma^2 \begin{pmatrix} 1 & \rho \\ \rho & 1 \end{pmatrix},$$

where $v_b$ is bit $b$ of $v$, the weights are $w = (1, 0.5, 0.25, 2)$, and the noise of the two samples has correlation $\rho$. The 16 values give 16 different means. The profiling phase sees $n$ pairs $(v_i, \ell_i)$ with known $v_i$. The attack phase sees $m$ pairs $(p_i, \ell_i)$ from the target, with the key $k$ unknown. The goal is to output $k$. The cost model is the [real RAM](/real-ram/).

## The algorithm

The algorithm estimates one mean for each of the $V = 16$ classes and one pooled covariance for all of them, factors the covariance once by [Cholesky decomposition](/cholesky-decomposition/), and sums log densities.

```pseudo id=main
TEMPLATE-ATTACK(profiling pairs (v_i, l_i), attack pairs (p_i, l_i), S-box S)
L1  for each class v do μ_v ← mean of the profiling traces l_i with v_i = v
L2  Σ ← pooled covariance of the residuals l_i - μ_{v_i}       ▷ divide by n - V
L3  C ← the Cholesky factor of Σ, so that C Cᵀ = Σ
L4  best ← none, top ← -∞
L5  for each key guess g = 0 .. |S| - 1 do
L6      score(g) ← 0
L7      for each attack pair (p, l) do
L8          score(g) ← score(g) - ½ ((l - μ_{S(p ⊕ g)})ᵀ Σ⁻¹ (l - μ_{S(p ⊕ g)}) + ln det Σ)
L9      if score(g) > top then
L10         best ← g, top ← score(g)
L11 return best and the list of scores
```

Line L8 is the log of the Gaussian density without the constant $-\tfrac{T}{2}\ln 2\pi$, which is the same for every guess. The quadratic form is computed as $\lVert C^{-1} d \rVert^2$ by one forward substitution with the triangular factor, never by an explicit inverse. With a pooled covariance the term $\ln\det\Sigma$ is also the same for every guess; it matters only for the variant with one covariance for each class. The sum of logs in line L8 is the log of the product of the densities of independent traces.

## Example

Take $\sigma = 0.5$, $\rho = 0.8$, the exact templates, and the key $k = \texttt{B}$. Three attack traces arrive:

| input p | trace l | value S(p ⊕ B) | template mean μ |
|---|---|---|---|
| 0 | (1.47, 1.96) | 8 | (1, 2) |
| 5 | (0.66, 0.84) | 1 | (1, 1) |
| 9 | (1.49, 0.32) | 6 | (2, 0.75) |

The scores below omit the term $\ln\det\Sigma$, which is the same for every guess.

| traces used | best guess and score | next guesses | rank of B |
|---|---|---|---|
| 1 | 6: -0.64 | 0: -0.66, B: -1.40 | 3 |
| 2 | B: -1.70 | 0: -2.07, E: -6.95 | 1 |
| 3 | B: -2.23 | 5: -13.02, 4: -13.53 | 1 |

After one trace the guesses 6 and 0 fit a little better than B, because their classes $\texttt{A}$ and $\texttt{C}$ have means $(2, 2.5)$ and $(2, 2.25)$, and the noise correlation of 0.8 makes a move along the diagonal cheap. After three traces the right key leads by $10.8$ in log likelihood, a likelihood ratio of about $5 \times 10^4$.

## Correctness

The loop of line L5 keeps the [loop invariant](/loop-invariant/) that top is the largest score so far and best is the first guess with it. With exact templates, the score of $g$ is the log likelihood of the attack traces under $g$, up to a constant. The central fact is a theorem: if the key is uniform and the traces are independent given the key, the rule that returns the guess of largest likelihood has the largest success probability of all decision rules on the same traces. It is the maximum a posteriori rule, by [Bayes' theorem](/bayes-theorem/), and the maximum of the posterior is the best possible guess at each point. With estimated templates the estimates converge to the exact ones as $n$ grows, and so do the scores. The [proof](proofs/correctness.md) gives the computation of line L8, the optimality theorem and the convergence.

## Complexity

Line L1 costs $\Theta(nT)$, and line L2 costs $\Theta(nT^2)$ for the outer products of the residuals. Line L3 costs $\Theta(T^3)$ once; the variant with one covariance for each class costs $\Theta(V T^3)$. In the attack phase, each of the $g$ guesses and $m$ traces needs one forward substitution in $\Theta(T^2)$. So the time is $\Theta(nT^2 + VT^3 + gmT^2)$ in every case. The extra space is $\Theta(VT)$ for the means, $\Theta(VT^2)$ for the factors in the per-class variant, and $\Theta(g)$ for the scores.

A measurement in the model, with $\sigma = 1$, $\rho = 0.8$ and a random key in each run: the success rate for $m$ attack traces with the exact templates (300 runs), with pooled templates estimated from $n = 1600$ profiling traces (100 runs), and with the rule that ignores the noise correlation (300 runs):

| attack traces m | 1 | 2 | 3 | 5 | 8 | 12 |
|---|---|---|---|---|---|---|
| exact templates | 0.31 | 0.44 | 0.59 | 0.85 | 0.96 | 1.00 |
| estimated, pooled | 0.26 | 0.40 | 0.55 | 0.78 | 0.93 | 0.99 |
| covariance ignored | 0.30 | 0.32 | 0.54 | 0.69 | 0.87 | 0.94 |

## Properties

- **Optimal with exact templates.** No attack on the same traces has a higher success probability (a theorem, under a uniform key and independent traces). This is why evaluation labs use template attacks to bound what any attacker can do in a given leakage model.
- **Profiled.** It needs a device with a known or chosen key, and the profiling and the target device must leak in the same way. The theorem says nothing about the mismatch between two real devices.
- **Uses the noise structure.** The covariance lets the attack cancel noise that two samples share. In the measurement, the rule that ignores it needs about 50 percent more traces for a success rate of 0.9.
- **Few attack traces.** Because it uses the full distribution, it often needs far fewer attack traces than [CPA](/correlation-power-analysis/), down to one trace when the noise is small.
- **Full ranking.** The scores are log likelihoods, so they can be turned into probabilities for each key part and combined by [key rank estimation](/side-channel-key-rank-estimation/).

## Variants and improvements

- **Pooled or per-class covariance.** The original form estimates one covariance for each class, which makes the classifier a [quadratic discriminant analysis](/quadratic-discriminant-analysis/). Pooling one covariance for all classes, as above, makes it a [linear discriminant analysis](/linear-discriminant-analysis/) and needs far fewer profiling traces.
- **Points of interest.** Real traces have thousands of samples, and the covariance of all of them cannot be estimated. Chari, Rao and Rohatgi keep the few samples where the class means differ most; [principal component analysis](/principal-component-analysis/) and linear discriminant analysis are later ways to reduce the dimension.
- **Templates on the Hamming weight.** Building 5 classes for the weights instead of 16 for the values needs fewer profiling traces, at the cost of losing what the weight does not show.
- **Linear regression on the bits.** Fit the mean of each sample as a linear function of the bits of the value. For a 4-bit value this needs 5 parameters per sample (one for each bit and a constant) rather than 16 class means.
- **Machine learning.** A [naive Bayes classifier](/naive-bayes-classifier/), a [support vector machine](/support-vector-machine/) or a neural network can replace the Gaussian model. They need no Gaussian assumption, but they lose the optimality theorem.

## When to use it

Use a template attack in an evaluation that must bound the strongest attacker, or when the attacker in the threat model can buy or build a copy of the device. Use [CPA](/correlation-power-analysis/) or [MIA](/mutual-information-analysis/) when there is no profiling device. To show only that a device leaks, without a key, a [leakage test](/test-vector-leakage-assessment/) is cheaper.

## Pitfalls

- **Ignoring the covariance.** If line L2 sets $\Sigma$ to $\sigma^2 I$, line L8 measures a Euclidean distance and cannot cancel the noise that the samples share. In the measurement, the success rate at $m = 5$ falls from 0.85 to 0.69. Estimate the full covariance in line L2.
- **One covariance for each class with few traces.** With $T$ samples a class needs at least $T + 1$ traces for its covariance to be invertible, and many more for it to be accurate; with too few, the Cholesky step of line L3 fails or gives a factor with tiny diagonal entries, and line L8 then trusts noise. Pool the covariance, as line L2 does, unless the profiling set is large.
- **Multiplying densities.** If line L8 multiplies the densities of the traces instead of adding their logs, the product becomes smaller than the smallest floating point number once there are enough traces or samples, and all guesses tie at 0. Add logs.
- **An explicit inverse.** Computing $\Sigma^{-1}$ and then the quadratic form loses accuracy when $\Sigma$ is close to singular, which happens with strongly correlated samples. Use the Cholesky factor and a triangular solve, as in line L8.

## Implementations

The code of this page is an abstract model on synthetic data. Its profiling and attack traces come from the two-sample model of "The problem", drawn with a seeded `random.Random` by the functions `profiling_set` and `attack_set`; the code never reads a device, a file or a clock. The tests check the Cholesky factor and the quadratic form against a cofactor inverse, the scores against a direct formula on 500 random inputs, the pooled covariance against a direct computation, the example above, the loss from ignoring the covariance, and the success rate with estimated templates.

## History

Chari, Rao and Rohatgi introduced template attacks at CHES 2002, and showed that a well profiled device can leak a key from very few traces. Their model of the noise as a multivariate Gaussian, with a mean for each value and a covariance learned on a copy of the device, is the model of this page. Standaert, Malkin and Yung (2009) gave the framework of success rate and guessing entropy in which profiled and non-profiled attacks are compared. Later work replaced the Gaussian classifier by general machine learning, with the template attack as the baseline.

## References
