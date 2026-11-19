---
tag: TAZK46
kind: algorithm
slug: map-speaker-adaptation
name: MAP speaker adaptation
aliases:
- maximum a posteriori adaptation
- Gauvain-Lee adaptation
area: natural-language-and-speech/speech-recognition
level: advanced
summary: Adapt acoustic model parameters by MAP estimation with the speaker-independent model as prior, so well-observed Gaussians move most.
solves: [automatic-speech-recognition, speaker-verification]
model: real-ram
complexity:
  vars: {T: the number of adaptation frames, M: the number of Gaussians, n: the feature dimension, k: the number of EM iterations}
  time: {worst: "O(k T M n)"}
  space: {extra: "O(M n)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1994
  people: [Jean-Luc Gauvain, Chin-Hui Lee]
  note: Gauvain and Lee derived EM updates for the MAP estimate of the weights, means and covariances of Gaussian mixture HMMs under Dirichlet and normal-Wishart priors. Reynolds, Quatieri and Dunn 2000 used the mean update with a relevance factor to build speaker models from a universal background model.
prereqs: [gaussian-mixture-model, maximum-a-posteriori-estimation, conjugate-prior, expectation-maximization]
see_also: [maximum-likelihood-linear-regression, gmm-ubm-speaker-verification, gmm-hmm-acoustic-model, bayesian-inference, vocal-tract-length-normalization, i-vector, forward-backward-algorithm]
sources:
  - paper: doi:10.1109/89.279278
    title: Jean-Luc Gauvain and Chin-Hui Lee, Maximum a posteriori estimation for multivariate Gaussian mixture observations of Markov chains, IEEE Transactions on Speech and Audio Processing 2(2), 1994, pages 291 to 298
    locator: the choice of the Dirichlet and normal-Wishart priors and the EM re-estimation formulas for the weights, means and covariances
  - paper: doi:10.1006/dspr.1999.0361
    title: Douglas A. Reynolds, Thomas F. Quatieri and Robert B. Dunn, Speaker verification using adapted Gaussian mixture models, Digital Signal Processing 10(1-3), 2000, pages 19 to 41
    locator: the section on the adapted speaker model (the data-dependent adaptation coefficients and the relevance factor)
  - paper: doi:10.1561/2000000004
    title: Mark Gales and Steve Young, The application of hidden Markov models in speech recognition, Foundations and Trends in Signal Processing 1(3), 2008, pages 195 to 304
    locator: the chapter on adaptation and normalization
---

MAP speaker adaptation moves the Gaussians of a speaker independent model toward the data of one speaker, and it uses the old model as a prior. Each new mean is a weighted average of the old mean and the mean of the data assigned to that Gaussian, $\hat\mu_m = (\tau \mu^0_m + \sum_t \gamma_m(t) o_t) / (\tau + \sum_t \gamma_m(t))$. A Gaussian that saw much data moves almost to the data mean, and a Gaussian that saw none stays where it was. With more and more data, the result tends to the speaker dependent maximum likelihood model.

## In plain words

A speech model stores many small averages, each one describing a sound piece. You get some speech from a new speaker, and you want to move each average toward how this speaker sounds.

For each average, look at the speech that matches it, and count how much there is. If there is a lot, trust the new speech and move the average almost all the way to it. If there is a little, move it only a little. If there is none, leave it. A single number controls how much speech counts as "a lot".

This is a cautious kind of learning: the old model is the starting belief, and the new speech changes it in proportion to the evidence.

## The problem

The prior model is a mixture of $M$ Gaussians, or the Gaussians of the states of a [GMM-HMM acoustic model](/gmm-hmm-acoustic-model/). Gaussian $m$ has the weight $c_m$, the mean $\mu^0_m \in \mathbb{R}^n$ and the diagonal covariance $\Sigma_m$. The input is $T$ frames $o_1, \ldots, o_T$ of the target speaker, with a transcript in the HMM case. The prior on the means is

$$\mu_m \sim \mathcal{N}(\mu^0_m, \Sigma_m / \tau), \quad \text{independent over } m,$$

with one constant $\tau > 0$. A large $\tau$ means a tight prior. The task is to find the means that maximize the posterior $p(\mu \mid O) \propto p(O \mid \mu)\, p(\mu)$ with the weights and covariances fixed. Gauvain and Lee 1994 solve the more general problem in which the weights and the covariances have priors too.

## The algorithm

MAP-EM is EM with a penalty from the prior. The E-step is the same as in [maximum likelihood EM](/expectation-maximization/). The M-step mixes the prior mean with the statistics.

```pseudo id=main
MAP-ADAPT(O, c, μ⁰, Σ, τ, iters)
L1  μ_m ← μ⁰_m for every m
L2  repeat iters times
L3      γ_m(t) ← c_m N(o_t; μ_m, Σ_m) / Σ_j c_j N(o_t; μ_j, Σ_j) for every t, m   ▷ in log space
L4      n_m ← Σ_t γ_m(t),  s_m ← Σ_t γ_m(t) o_t
L5      μ_m ← (τ μ⁰_m + s_m) / (τ + n_m)
L6  return μ
```

Line L5 always shrinks toward the prior mean $\mu^0_m$, not toward the mean of the last iteration. Write $\alpha_m = n_m / (n_m + \tau)$ and $E_m = s_m / n_m$. Then line L5 is

$$\hat\mu_m = \alpha_m E_m + (1 - \alpha_m)\, \mu^0_m,$$

the form of Reynolds, Quatieri and Dunn 2000, who call $\tau$ the relevance factor $r$. In practice one iteration is common, mainly in speaker verification. In an HMM system the posteriors of line L3 come from the [forward-backward algorithm](/forward-backward-algorithm/) over the transcript.

## Example

**One Gaussian.** Take $n = 1$, $\mu^0 = 0$, $\tau = 16$, and data whose mean is $E = 2$. Every frame belongs to the one Gaussian, so $n_1 = T$:

| frames $T$ | $\alpha = T/(T + 16)$ | $\hat\mu = 2\alpha$ |
|---|---|---|
| 4 | 0.2 | 0.4 |
| 16 | 0.5 | 1.0 |
| 64 | 0.8 | 1.6 |

At $T = \tau$ the new mean is halfway between the prior and the data. So $\tau$ acts as a number of "virtual frames" of prior data.

**Two Gaussians.** Take $c = (0.5, 0.5)$, $\mu^0 = (-1, 1)$, $\sigma^2 = 1$, and the four frames $0.5, 1.5, 2.5, 3.0$. The posterior of Gaussian 2 at frame $x$ is $1/(1 + e^{-2x})$:

| frame | 0.5 | 1.5 | 2.5 | 3.0 |
|---|---|---|---|---|
| $\gamma_2$ | 0.731059 | 0.952574 | 0.993307 | 0.997527 |

So $n = (0.325533, 3.674467)$ and $E = (0.705795, 1.978584)$. The new means are:

| $\tau$ | $\alpha_1$ | $\hat\mu_1$ | $\alpha_2$ | $\hat\mu_2$ |
|---|---|---|---|---|
| 16 | 0.019940 | -0.965986 | 0.186763 | 1.182763 |
| 2 | 0.139982 | -0.761219 | 0.647544 | 1.633676 |

Gaussian 2 has most of the data and moves much more than Gaussian 1. With $\tau = 0$, the means would be the data means $E$, which is one step of maximum likelihood EM.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). For fixed posteriors, the expected complete-data log likelihood plus the log prior separates over the Gaussians and the coordinates. Each part is a strictly concave quadratic in one coordinate of one mean, and its maximizer is line L5. The Jensen argument of EM then shows that each iteration does not decrease the log posterior $\log p(O \mid \mu) + \log p(\mu)$. For one Gaussian the result is the exact posterior mean of a Gaussian mean with a Gaussian [conjugate prior](/conjugate-prior/). For a mixture, MAP-EM finds a stationary point, which can be a local maximum.

## Complexity

In the real RAM, line L3 evaluates $M$ Gaussians of dimension $n$ at each of $T$ frames, $O(T M n)$, and line L4 costs the same. Line L5 costs $O(M n)$. With $k$ iterations the time is $O(k T M n)$. The extra memory is $O(M n)$ for the statistics; the posteriors are added frame by frame and need not be stored. In a large system, most of the time goes into the E-step, as in ML training.

## Properties

- **Asymptotic behavior.** As $n_m \to \infty$ with $\tau$ fixed, $\alpha_m \to 1$ and the MAP mean tends to the ML mean. For an infinite amount of data, MAP adaptation and ML training agree.
- **Local update.** Only Gaussians with data move. This is the main difference from [MLLR](/maximum-likelihood-linear-regression/), where a shared transform moves every Gaussian of a class. With little data MLLR is better, and with much data MAP is better; Gales and Young 2008 describe this trade-off.
- **A heuristic constant.** The relevance factor $r = 16$ of Reynolds et al. 2000 was chosen by experiment, and other systems tune the value on development data. It is a heuristic, not a result of the theory.
- **Monotone MAP-EM.** Each iteration does not decrease the log posterior (Theorem 2 of the proof).
- **Aligned components.** The adapted model keeps the order and the meaning of the components of the prior model. This makes MAP-adapted models easy to compare: the stacked adapted means form a fixed-length "GMM supervector" for each speaker. The [i-vector](/i-vector/) extractor uses the same statistics $n_m$ and $s_m$.

## Variants and improvements

- **Weights and variances.** Reynolds et al. 2000 also adapt the weights, $\hat c_m = \beta\,[\alpha_m n_m / T + (1 - \alpha_m) c_m]$ with $\beta$ chosen so that the weights sum to 1, and the variances, $\hat\sigma^2_m = \alpha_m E_m[x^2] + (1 - \alpha_m)(\sigma^2_m + (\mu^0_m)^2) - \hat\mu_m^2$ per dimension. In their speaker verification experiments, adapting only the means gave the best results; this is a measurement on their data. The code implements both forms.
- **Separate factors.** Use a separate $\tau$ for the weights, the means and the variances, as in the general Gauvain and Lee formulas.
- **MAP on top of MLLR.** Use the MLLR-adapted model as the prior mean, so that unseen Gaussians also move, and refine the Gaussians with much data by MAP.
- **Joint factor analysis and eigenvoices.** Constrain the supervector of adapted means to a low-dimensional subspace. With little data, this moves all Gaussians in a coordinated way. The [i-vector](/i-vector/) model is the later form of this idea.

## When to use it

Use MAP adaptation when the target speaker or condition has enough data to see most Gaussians several times, for example minutes of speech for a GMM-HMM recognizer, or when the model must keep the components of the prior model aligned, as in [GMM-UBM speaker verification](/gmm-ubm-speaker-verification/). With only a few seconds of data, use MLLR or another transform with few parameters, or combine the two.

## Pitfalls

- **Shrinking toward the wrong mean.** Line L5 shrinks toward the prior mean $\mu^0_m$ at every iteration. Shrinking toward the last iterate makes the prior weaker at each step.
- **Too small a relevance factor.** With $\tau$ near 0, a Gaussian that saw one or two frames jumps to them. The model then fits noise, and its variance is no longer correct for the new mean.
- **Posteriors from the wrong model.** In speaker verification, the posteriors come from the universal background model. In iterative MAP-EM, they come from the current adapted model. Mixing the two changes the result.
- **Variance adaptation without a floor.** The adapted variance formula subtracts $\hat\mu_m^2$ and can give values near 0 with very little data. Floor the variances.
- **Products of densities.** Compute the posteriors of line L3 in log space with the log-sum-exp trick; densities of frames far from every mean are 0 in double precision.

## Implementations

## History

Gauvain and Lee 1994 gave the MAP estimate of the parameters of Gaussian mixture HMMs, with Dirichlet priors on the weights and normal-Wishart priors on the means and precisions, and EM updates for all of them. They used it for speaker adaptation and for training with little data. Reynolds, Quatieri and Dunn 2000 made the one-step mean update with a relevance factor the standard way to build speaker models from a universal background model. Joint factor analysis and the i-vector model later replaced the free per-Gaussian update with a low-dimensional one for speaker recognition.

## References
