---
tag: AXV6G0
kind: algorithm
slug: gmm-ubm-speaker-verification
name: GMM-UBM speaker verification
aliases:
- universal background model
- GMM-UBM
- adapted GMM speaker verification
area: natural-language-and-speech/speech-recognition
level: core
summary: Verify a claimed speaker by the average log likelihood ratio per frame between a speaker GMM, MAP-adapted from a universal background model, and that background model.
solves: [speaker-verification]
model: real-ram
complexity:
  vars: {T: the number of frames of the test utterance, M: the number of Gaussians in the UBM, d: the feature dimension, C: the number of components kept per frame in fast scoring}
  time: {worst: "O(T M d)"}
  space: {extra: "O(M d)"}
properties: {deterministic: true, exact: true, online: true, recursive: false}
history:
  year: 2000
  people: [Douglas A. Reynolds, Thomas F. Quatieri, Robert B. Dunn]
  note: Reynolds, Quatieri and Dunn described the system that MAP-adapts the speaker model from a universal background model and scores the log likelihood ratio, with fast top-C scoring and score normalization. It was the standard text-independent approach until factor analysis and i-vectors.
prereqs: [gaussian-mixture-model, likelihood-ratio-test, speaker-verification]
see_also: [map-speaker-adaptation, equal-error-rate, i-vector, plda-scoring, neyman-pearson-lemma, mel-frequency-cepstral-coefficients, voice-activity-detection, log-sum-exp-trick]
sources:
  - paper: doi:10.1006/dspr.1999.0361
    title: Douglas A. Reynolds, Thomas F. Quatieri and Robert B. Dunn, Speaker verification using adapted Gaussian mixture models, Digital Signal Processing 10(1-3), 2000, pages 19 to 41
    locator: the sections on the likelihood ratio detector, the universal background model, the adapted speaker models and fast scoring
  - paper: doi:10.1109/89.279278
    title: Jean-Luc Gauvain and Chin-Hui Lee, Maximum a posteriori estimation for multivariate Gaussian mixture observations of Markov chains, IEEE Transactions on Speech and Audio Processing 2(2), 1994, pages 291 to 298
    locator: the EM re-estimation formula for the means under a conjugate prior
  - url: https://cs.joensuu.fi/sipu/pub/SRE-review-Kinnunen-and-Li.pdf
    title: Tomi Kinnunen and Haizhou Li, An overview of text-independent speaker recognition, from features to supervectors, Speech Communication 52(1), 2010, pages 12 to 40
    locator: the section on Gaussian mixture models and the universal background model
---

GMM-UBM speaker verification decides whether a test utterance comes from a claimed speaker. A large Gaussian mixture, the universal background model (UBM), describes the speech of people in general. Enrollment turns it into a speaker model by moving its means toward the speaker's frames with [MAP adaptation](/map-speaker-adaptation/). A test utterance gets the score $\Lambda = \frac{1}{T} \sum_t [\log p(y_t \mid \text{speaker}) - \log p(y_t \mid \text{UBM})]$, and the claim is accepted when $\Lambda$ reaches a threshold.

## In plain words

First, build one general model of how people sound, from many hours of many speakers. When a new person enrolls, change this general model a little toward the person's own speech, so that you get a personal model. Parts of the general model that the person's speech does not touch stay as they are.

When someone claims to be that person, ask two questions about each short slice of the test speech. How well does the personal model explain it? How well does the general model explain it? If the personal model wins clearly on average, accept the claim. If not, reject it.

Comparing with the general model is the key step. A slice that every voice produces scores high in both models, so it gives no evidence either way.

## The problem

This is the [speaker verification](/speaker-verification/) problem. The input is a test utterance, given as feature frames $Y = y_1, \ldots, y_T$ (for example [MFCCs](/mel-frequency-cepstral-coefficients/) with deltas, after [voice activity detection](/voice-activity-detection/)), and an identity claim $s$. Two hypotheses compete: $H_0$, the utterance comes from $s$, and $H_1$, it comes from someone else. The system must output a score, and a decision at a threshold $\theta$.

The likelihood ratio $p(Y \mid H_0) / p(Y \mid H_1)$ is the best statistic if both densities are known ([likelihood ratio test](/likelihood-ratio-test/)). GMM-UBM models $H_0$ with the speaker model and $H_1$ with the UBM, a [Gaussian mixture](/gaussian-mixture-model/) with $M$ components (often 512 to 2048) and diagonal covariances, trained by EM on many speakers. The enrollment data of $s$ are frames $x_1, \ldots, x_N$.

## The algorithm

```pseudo id=main
ENROLL(X, UBM = (c, μ, Σ), r)                ▷ r: relevance factor
L1  γ_m(t) ← c_m N(x_t; μ_m, Σ_m) / p(x_t | UBM)   for every t, m   ▷ in log space
L2  n_m ← Σ_t γ_m(t),  E_m ← (1/n_m) Σ_t γ_m(t) x_t
L3  α_m ← n_m / (n_m + r)
L4  μ̂_m ← α_m E_m + (1 - α_m) μ_m
L5  return the speaker model (c, μ̂, Σ)

SCORE(Y, speaker, UBM, θ)
L6  Λ ← (1/T) Σ_t [log p(y_t | speaker) - log p(y_t | UBM)]
L7  accept if Λ ≥ θ, else reject
```

Only the means are adapted. The speaker model keeps the weights and the covariances of the UBM, and component $m$ of the speaker model describes the same part of the feature space as component $m$ of the UBM. A component with $n_m = 0$ keeps its UBM mean. Each mixture density is a sum of $M$ terms; the code computes its log with the [log-sum-exp trick](/log-sum-exp-trick/).

**Fast scoring.** For each test frame, find the $C$ components with the largest weighted UBM density, for a small $C$ such as 5. Sum both mixtures over these $C$ components only. Because the speaker components are adapted from the UBM components, the components that matter for the UBM are usually the ones that matter for the speaker model.

## Example

Take a one-dimensional UBM with two components: $c = (0.5, 0.5)$, $\mu = (-1, 1)$, $\sigma^2 = 1$. The speaker enrolls with four frames, $1.5, 2.0, 2.5, 0.5$, and $r = 4$. The usual value is $r = 16$; a smaller value is used here so that four frames move the means visibly.

| frame $x_t$ | 1.5 | 2.0 | 2.5 | 0.5 |
|---|---|---|---|---|
| $\gamma_1(t)$ | 0.047426 | 0.017986 | 0.006693 | 0.268941 |
| $\gamma_2(t)$ | 0.952574 | 0.982014 | 0.993307 | 0.731059 |

| component | $n_m$ | $E_m$ | $\alpha_m$ | $\hat\mu_m$ |
|---|---|---|---|---|
| 1 | 0.341046 | 0.757416 | 0.078563 | -0.861932 |
| 2 | 3.658954 | 1.705866 | 0.477735 | 1.337217 |

Component 2 has most of the data and moves from 1 to 1.337217. Component 1 moves only a little.

Now score two test utterances of two frames each.

| test utterance | per-frame log likelihood ratios | $\Lambda$ |
|---|---|---|
| $1.8, 2.2$ (the speaker) | 0.217649, 0.348872 | 0.283261 |
| $-1.2, 0.8$ (an impostor) | -0.082495, -0.053297 | -0.067896 |

With $\theta = 0$, the first claim is accepted and the second is rejected. The frame $0.8$ is close to the UBM mean $1$, where the speaker model has less density than the UBM, so its ratio is negative.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Enrollment is one step of MAP-EM, started at the UBM, with the prior $\mathcal{N}(\mu_m, \Sigma_m / r)$ on each mean; the MAP page proves that this step maximizes the penalized auxiliary function. With frames that are independent given the model, $\Lambda$ is the log likelihood ratio of the whole utterance divided by $T$, and the log-sum-exp form computes each mixture density exactly in real arithmetic. If the two models were the true densities, thresholding $\Lambda$ would be the most powerful test at its false alarm rate, by the [Neyman-Pearson lemma](/neyman-pearson-lemma/). Top-$C$ scoring equals the exact score when $C = M$, and its UBM term is within $\log(M/C)$ of the exact term for any $C$; the speaker term has no such bound.

## Complexity

In the real RAM, enrollment evaluates $M$ Gaussians of dimension $d$ at each of $N$ frames: $O(N M d)$ time and $O(M d)$ extra memory. Scoring evaluates both mixtures at each of $T$ frames, $O(T M d)$. Fast scoring still evaluates the whole UBM, but only $C$ speaker components per frame, so it costs $O(T (M + C) d)$ plus the selection of the top $C$ in $O(T M)$. When one test utterance is scored against many speaker models, the UBM part and the top-$C$ lists are computed once, and each extra model costs only $O(T C d)$. The scores are sums over frames, so the scoring is online: each frame can be added as it arrives.

## Properties

- **Exact for the model.** The score is the exact average log likelihood ratio of the two mixtures, under independent frames.
- **Aligned models.** Every speaker model has the same components as the UBM, so fast scoring works, and the stacked adapted means form a fixed-length vector per speaker.
- **Robust with little data.** A component that saw no enrollment data keeps the UBM mean, so its ratio is near 0 for frames that it explains. Unseen sounds therefore give little evidence either way, which is what one wants.
- **Heuristics.** The relevance factor 16, mean-only adaptation and a small $C$ are choices found by experiment in Reynolds et al. 2000.
- **Not calibrated.** The average per frame is not the log likelihood ratio of the utterance, and the frames are not independent. Scores need normalization or calibration before a Bayes threshold can be applied.

## Variants and improvements

- **Score normalization.** Z-norm shifts and scales a speaker's scores by the mean and standard deviation of the scores of impostor utterances against this speaker model. T-norm uses the scores of the test utterance against a set of impostor models. Both make one threshold work for all speakers.
- **GMM supervectors with an SVM.** Stack the adapted means, scaled by the weights and covariances, into one long vector, and train a support vector machine per speaker.
- **Factor analysis and i-vectors.** Joint factor analysis splits the supervector into a speaker part and a channel part. The [i-vector](/i-vector/) model maps each utterance to a short vector, which is scored with [PLDA](/plda-scoring/).
- **Channel compensation.** Feature warping, [cepstral mean normalization](/cepstral-mean-normalization/) and nuisance attribute projection reduce the effect of the microphone and the channel.
- **Neural embeddings.** [x-vectors](/x-vector/) replaced the GMM with a network trained to classify speakers; the PLDA back end stayed.

## When to use it

Use GMM-UBM when the training data are small, when a simple and well understood system is needed, or as a baseline. It needs no labels of speakers to train the UBM, and it enrolls a speaker with seconds of speech. With large labeled corpora, i-vector and x-vector systems with PLDA are more accurate.

## Pitfalls

- **A UBM from the wrong data.** The UBM must match the test conditions: language, channel, gender balance. A UBM from clean read speech gives poor ratios on telephone speech.
- **Silence in the score.** Silence frames give ratios near 0 and dilute $\Lambda$. Remove them with a voice activity detector.
- **Products of densities.** A test utterance has hundreds of frames, and the product of the densities underflows. Add logs, and compute each mixture with the log-sum-exp trick.
- **Threshold by speaker.** Raw scores of different speakers lie on different scales. Normalize the scores, or the error rate at a single threshold goes up.
- **Adapting variances with little data.** The variance update can shrink a variance near 0 and give a few frames huge ratios. Adapt only the means, or floor the variances.

## Implementations

## History

Reynolds and Rose used Gaussian mixtures for text-independent speaker identification in 1995. The likelihood ratio against a background model replaced cohort models of selected impostors. Reynolds, Quatieri and Dunn 2000 described the complete system of the MIT Lincoln Laboratory: a single UBM trained on many speakers, mean-only MAP adaptation with a relevance factor, top-C fast scoring and score normalization. It was the reference approach of the NIST speaker recognition evaluations for the next decade, until joint factor analysis and then the i-vector of Dehak et al. 2011 took its place. Kinnunen and Li 2010 survey this period.

## References
