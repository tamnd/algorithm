---
tag: TR4HQ1
kind: algorithm
slug: maximum-likelihood-linear-regression
name: Maximum likelihood linear regression
aliases:
- MLLR
- MLLR mean adaptation
area: natural-language-and-speech/speech-recognition
level: advanced
summary: Adapt Gaussian means of an acoustic model to a speaker by affine maps shared over classes of Gaussians, fit by EM on little data.
solves: [automatic-speech-recognition]
model: real-ram
complexity:
  vars: {T: the number of adaptation frames, M: the number of Gaussians, n: the feature dimension, R: the number of regression classes, k: the number of EM iterations}
  time: {worst: "O(k (T M n + M n^3 + R n^4))"}
  space: {extra: "O(M n + R n^2)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1995
  people: [Christopher J. Leggetter, Philip C. Woodland]
  note: Leggetter and Woodland adapted the Gaussian means of a continuous density HMM recognizer with affine transforms that are shared by classes of Gaussians and estimated by EM. Gales 1998 added the constrained form that also transforms the covariances.
prereqs: [gaussian-mixture-model, expectation-maximization, gmm-hmm-acoustic-model]
see_also: [map-speaker-adaptation, vocal-tract-length-normalization, cepstral-mean-normalization, forward-backward-algorithm, ordinary-least-squares, gaussian-elimination, i-vector, phonetic-decision-tree-state-tying]
sources:
  - paper: doi:10.1006/csla.1995.0010
    title: C. J. Leggetter and P. C. Woodland, Maximum likelihood linear regression for speaker adaptation of continuous density hidden Markov models, Computer Speech and Language 9(2), 1995, pages 171 to 185
    locator: the derivation of the mean transform, its row by row solution for diagonal covariances, and the regression classes
  - paper: doi:10.1006/csla.1998.0043
    title: M. J. F. Gales, Maximum likelihood linear transformations for HMM-based speech recognition, Computer Speech and Language 12, 1998, pages 75 to 98
    locator: the unconstrained and constrained transforms and the iterative row by row estimate of the constrained transform
  - paper: doi:10.1561/2000000004
    title: Mark Gales and Steve Young, The application of hidden Markov models in speech recognition, Foundations and Trends in Signal Processing 1(3), 2008, pages 195 to 304
    locator: the chapter on adaptation and normalization
---

Maximum likelihood linear regression (MLLR) adapts a speaker independent acoustic model to a new speaker with a small amount of speech. It replaces each Gaussian mean $\mu_m$ by $A \mu_m + b$, where one affine map is shared by a whole class of Gaussians, and it fits the map by maximum likelihood with the [EM algorithm](/expectation-maximization/). Because the map is shared, Gaussians that saw no adaptation data also move. With diagonal covariances, each row of the map is the solution of a small weighted least squares problem, so the M-step is closed form.

## In plain words

A speech recognizer stores, for each small piece of each sound, an average of what that piece looks like. These averages come from many speakers. A new speaker sounds a bit different, and the error rate goes up. You have a few sentences from the new speaker, much too little to learn every average again.

The idea is to assume that the new speaker shifts and stretches all the averages in the same way. Learn one such shift and stretch from the few sentences, and apply it to every average, even to the sounds that the speaker did not say. With more data, use a few separate shifts, one for each group of similar sounds, for example one for the vowels and one for the consonants.

## The problem

The model has $M$ Gaussians, for example the Gaussians of all HMM states of a [GMM-HMM acoustic model](/gmm-hmm-acoustic-model/). Gaussian $m$ has the mean $\mu_m \in \mathbb{R}^n$ and the diagonal covariance $\Sigma_m = \mathrm{diag}(\sigma^2_{m,1}, \ldots, \sigma^2_{m,n})$. Each Gaussian belongs to one of $R$ regression classes, $r(m)$. The input is a sequence of $T$ adaptation frames $o_1, \ldots, o_T$ of the new speaker, usually with a transcript (supervised adaptation) or with the output of a first recognition pass (unsupervised adaptation).

Write the extended mean $\xi_m = (1, \mu_{m,1}, \ldots, \mu_{m,n})^\top$. For each class $r$, the unknown is an $n \times (n+1)$ matrix $W_r = [\,b_r \mid A_r\,]$, and the adapted mean is

$$\hat\mu_m = W_{r(m)}\, \xi_m = A_{r(m)} \mu_m + b_{r(m)}.$$

The task is to find the transforms that maximize the likelihood $p(o_1, \ldots, o_T \mid W_1, \ldots, W_R)$ of the adaptation data under the model with the adapted means. The weights, the transitions and the covariances stay as they are.

## The algorithm

EM alternates between the posteriors $\gamma_m(t)$ of each Gaussian at each frame (the E-step) and a new set of transforms (the M-step). The M-step needs only two statistics per Gaussian, the occupancy $\mathrm{occ}_m = \sum_t \gamma_m(t)$ and the first-order sum $s_m = \sum_t \gamma_m(t)\, o_t$. With diagonal covariances, row $i$ of $W_r$, written $w_{r,i}$, maximizes a separate quadratic function, and its maximizer solves the $(n+1) \times (n+1)$ system $G_{r,i} w_{r,i} = k_{r,i}$ with

$$G_{r,i} = \sum_{m: r(m) = r} \frac{\mathrm{occ}_m}{\sigma^2_{m,i}}\, \xi_m \xi_m^\top, \qquad k_{r,i} = \sum_{m: r(m) = r} \frac{s_{m,i}}{\sigma^2_{m,i}}\, \xi_m.$$

```pseudo id=main
MLLR(O, μ, σ², class, iters)            ▷ μ: speaker independent means, ξ_m = (1, μ_m)
L1  W_r ← [0 | I] for r = 1 .. R        ▷ start from the unchanged model
L2  repeat iters times
L3      μ̂_m ← W_{r(m)} ξ_m for every m
L4      γ_m(t) ← posterior of Gaussian m at frame t under the means μ̂   ▷ E-step, in log space
L5      occ_m ← Σ_t γ_m(t),  s_m ← Σ_t γ_m(t) o_t
L6      for each class r and each row i = 1 .. n do                     ▷ M-step
L7          G ← Σ_{m in r} (occ_m / σ²_{m,i}) ξ_m ξ_mᵀ,  k ← Σ_{m in r} (s_{m,i} / σ²_{m,i}) ξ_m
L8          w_{r,i} ← the solution of G w = k
L9  return W_1 .. W_R
```

Line L3 always starts from the speaker independent means $\xi_m$, not from the means of the last iteration. The posteriors of line L4 come from the current adapted model: in a Gaussian mixture they are the component posteriors, and in an HMM system they come from the [forward-backward algorithm](/forward-backward-algorithm/) over the transcript. Many systems run only one or two iterations.

## Example

Take $n = 1$ and one class with four Gaussians, all with $\sigma^2 = 1$. The speaker independent means are $\mu = 0, 1, 3, 2$. The E-step gave these statistics:

| Gaussian $m$ | $\mu_m$ | $\mathrm{occ}_m$ | $s_m$ | data mean $s_m / \mathrm{occ}_m$ |
|---|---|---|---|---|
| 1 | 0 | 4 | 4 | 1 |
| 2 | 1 | 2 | 4 | 2 |
| 3 | 3 | 2 | 16 | 8 |
| 4 | 2 | 0 | 0 | none |

With $\xi_m = (1, \mu_m)$, the system of line L7 is

$$G = \begin{pmatrix} \sum \mathrm{occ}_m & \sum \mathrm{occ}_m \mu_m \\ \sum \mathrm{occ}_m \mu_m & \sum \mathrm{occ}_m \mu_m^2 \end{pmatrix} = \begin{pmatrix} 8 & 8 \\ 8 & 20 \end{pmatrix}, \qquad k = \begin{pmatrix} \sum s_m \\ \sum s_m \mu_m \end{pmatrix} = \begin{pmatrix} 24 \\ 52 \end{pmatrix}.$$

The determinant is $8 \cdot 20 - 8 \cdot 8 = 96$, so $b = (20 \cdot 24 - 8 \cdot 52)/96 = 2/3$ and $a = (8 \cdot 52 - 8 \cdot 24)/96 = 7/3$. The adapted means are $\hat\mu = 7/3 \cdot \mu + 2/3$:

| Gaussian $m$ | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| $\hat\mu_m$ | 0.6667 | 3 | 7.6667 | 5.3333 |

This is a weighted least squares line through the points $(\mu_m, s_m / \mathrm{occ}_m)$ with the weights $\mathrm{occ}_m / \sigma^2_m$. The weighted squared error $\sum_m \mathrm{occ}_m (s_m/\mathrm{occ}_m - \hat\mu_m)^2$ falls from 56 for the unchanged means to $8/3$. A shift alone, $\hat\mu = \mu + b$, gives $b = 2$ and an error of 24. Gaussian 4 saw no data, but it moves from 2 to 5.3333, because it shares the transform. [MAP adaptation](/map-speaker-adaptation/) would leave it at 2.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). With diagonal covariances, the EM auxiliary function is a constant minus one half of a sum of quadratic forms $w^\top G_{r,i} w - 2 w^\top k_{r,i}$, one for each class and row, in disjoint variables. Each $G_{r,i}$ is positive semidefinite, and it is positive definite exactly when the class has $n+1$ affinely independent means with nonzero occupancy. Then line L8 gives the unique maximizer of the auxiliary function, and the usual EM argument (Jensen's inequality) shows that the likelihood of the adaptation data does not decrease from one iteration to the next. EM reaches a stationary point, not always the global maximum.

## Complexity

In the real RAM, one E-step evaluates $M$ diagonal Gaussians at each of $T$ frames, $O(T M n)$, and the statistics cost the same. For each Gaussian, the outer product $\xi_m \xi_m^\top$ is added into $n$ matrices $G_{r,i}$ with different scales, $O(n \cdot n^2)$, so the matrices cost $O(M n^3)$. The $R n$ systems of size $n+1$ cost $O(n^3)$ each by [Gaussian elimination](/gaussian-elimination/), so $O(R n^4)$. With $k$ iterations the total is $O(k (T M n + M n^3 + R n^4))$. In a real system $T M n$ dominates: for $n = 39$ the solves are about $40^3 \cdot 39 \approx 2.5 \cdot 10^6$ operations per class, which is small next to the E-step over thousands of Gaussians.

The extra memory is $O(M n)$ for the statistics and the adapted means and $O(R n^2)$ for the transforms. The statistics are added frame by frame, so the posteriors need not be stored.

## Properties

- **Shared parameters.** A global transform has $n(n+1)$ parameters, 1560 for $n = 39$, against $M n$ means. This is why MLLR works with a few sentences.
- **Unseen Gaussians move.** Every Gaussian of a class moves with the class, as Gaussian 4 of the example shows.
- **Closed form M-step.** For diagonal covariances each row is one linear solve. For full covariances the rows are coupled, and the M-step is one larger system.
- **Monotone EM.** The likelihood of the adaptation data never goes down (Theorem 2 of the proof).
- **No limit at large data.** With a fixed number of classes, more data does not make MLLR as good as a speaker dependent model, because the transform has a fixed number of parameters. More classes help, up to the data that each class can support.
- **Measured gain.** Leggetter and Woodland 1995 report, in the abstract, a 37% reduction in word error rate with supervised adaptation and 32% with unsupervised adaptation, on the ARPA Resource Management (RM1) data with 40 adaptation sentences, relative to the speaker independent model. This is a measurement on that task.

## Variants and improvements

- **Regression class trees.** Cluster the Gaussians into a binary tree by the closeness of their means. Walk the tree, and give a node its own transform only if its occupancy is above a threshold; otherwise use the transform of the parent. The number of transforms then grows with the amount of data.
- **Block diagonal and diagonal transforms.** For features with static, delta and delta-delta parts, a block diagonal $A$ with three blocks has fewer parameters. A diagonal $A$ is a per-dimension scale and shift.
- **Bias only.** $A = I$ gives a shift of all means, the model-space counterpart of [cepstral mean normalization](/cepstral-mean-normalization/).
- **Variance MLLR.** A second transform $\hat\Sigma_m = H \Sigma_m H^\top$ adapts the covariances, estimated after the means.
- **Constrained MLLR (CMLLR).** Gales 1998 uses the same matrix for the mean and the covariance: $\hat\mu = A' \mu - b'$ and $\hat\Sigma = A' \Sigma A'^\top$. This is the same as a transform of the features, $\hat o = A o + b$ with $A = A'^{-1}$, plus the Jacobian term $\log |\det A|$ in the likelihood. There is no closed form; each row is updated in turn by solving a quadratic equation, and the process is iterated. Because it acts on features, it is also called feature-space MLLR (fMLLR), and it is used to normalize the input of neural network acoustic models.
- **Speaker adaptive training.** Estimate a transform for each training speaker, and train the canonical model on the transformed data. The model then holds less speaker variation, and adaptation at test time works better.
- **Other uses of the statistics.** The same occupancies and first-order sums are the input of [MAP adaptation](/map-speaker-adaptation/) and of the [i-vector](/i-vector/) extractor. MAP and MLLR are often combined: MLLR moves all Gaussians first, and MAP then refines the ones with much data.

## When to use it

Use MLLR when a GMM-HMM recognizer must adapt to a speaker or a channel with a few seconds to a few minutes of speech, and when a transcript or a first-pass recognition is available. With a large amount of speaker data, MAP adaptation or full retraining gives a better model. For neural network acoustic models, the feature-space form (fMLLR) is the usual choice, because the network has no Gaussians to transform.

## Pitfalls

- **Too few Gaussians with data in a class.** If fewer than $n + 1$ affinely independent means have data, $G$ is singular. Use a regression class tree with an occupancy threshold, or fall back to a global or a bias-only transform.
- **Updating from the adapted means.** Each iteration must estimate the transform from the speaker independent means, with the posteriors of the current adapted model. Composing a new transform on top of the last adapted means also works, but then the transforms must be multiplied, and the code must not mix the two.
- **Errors in unsupervised adaptation.** A first-pass transcript with many errors gives posteriors for the wrong states, and adaptation can make the model worse. Use confidence scores to drop unreliable frames.
- **Silence.** Silence frames are many and carry little speaker information. Give silence its own class, or leave it out.
- **Full covariances.** The row by row formula holds only for diagonal covariances. With full covariances, the rows are coupled.
- **Products of densities.** The posteriors need the sum of $M$ weighted densities. Compute them in log space with the log-sum-exp trick; a frame far from all means gives densities that are 0 in double precision.

## Implementations

## History

Leggetter and Woodland published MLLR in 1995 for continuous density HMMs, after earlier work on speaker adaptation by MAP estimation (Gauvain and Lee 1994) and by spectral mapping. They introduced the regression classes that share one transform among many Gaussians. Gales and Woodland then adapted the variances with a second transform, and Gales 1998 described the constrained form, the basis of fMLLR and of speaker adaptive training with feature transforms. Gales and Young 2008 survey these methods.

## References
