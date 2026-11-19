---
tag: MHT9KM
kind: algorithm
slug: plda-scoring
name: PLDA scoring
aliases:
- probabilistic linear discriminant analysis
- PLDA
- two-covariance PLDA scoring
area: natural-language-and-speech/speech-recognition
level: advanced
summary: Score two speaker embeddings by the closed form log likelihood ratio that they share one latent speaker variable in a Gaussian PLDA model.
solves: [speaker-verification]
model: real-ram
complexity:
  vars: {d: the embedding dimension, N: the number of trials, n: the number of enrollment embeddings of a speaker}
  time: {worst: "O(d^3 + N d^2)"}
  space: {extra: "O(d^2)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2007
  people: [Sergey Ioffe, Simon J. D. Prince, James H. Elder]
  note: Ioffe in 2006 and Prince and Elder in 2007 proposed probabilistic LDA for face recognition. Speaker recognition took it up for i-vectors around 2010, and it stayed the usual back end for x-vectors.
prereqs: [factor-analysis, likelihood-ratio-test, speaker-verification]
see_also: [linear-discriminant-analysis, i-vector, x-vector, equal-error-rate, gmm-ubm-speaker-verification, schur-complement, cholesky-decomposition, conjugate-prior]
sources:
  - paper: doi:10.1109/ICCV.2007.4409052
    title: Simon J. D. Prince and James H. Elder, Probabilistic linear discriminant analysis for inferences about identity, IEEE 11th International Conference on Computer Vision (ICCV), 2007
    locator: the model with a signal subspace and a noise subspace, and the likelihood of a match
  - paper: doi:10.1007/11744085_41
    title: Sergey Ioffe, Probabilistic linear discriminant analysis, European Conference on Computer Vision (ECCV), Lecture Notes in Computer Science 3954, 2006
    locator: the generative model with a Gaussian prior on the class centers
  - paper: doi:10.21437/Interspeech.2011-53
    title: Daniel Garcia-Romero and Carol Y. Espy-Wilson, Analysis of i-vector length normalization in speaker recognition systems, Interspeech 2011
    locator: the Gaussian PLDA model for i-vectors and the length normalization before it
---

PLDA scoring compares two speaker embeddings, such as [i-vectors](/i-vector/) or [x-vectors](/x-vector/), and returns the log likelihood ratio that they come from the same speaker. It uses a Gaussian model in which every embedding is the sum of a speaker part, shared by all embeddings of that speaker, and a session part, new for each recording. Under this model the ratio has a closed form: a quadratic function of the two embeddings.

## In plain words

Recordings of one person do not give identical embeddings. The microphone, the room and the words change them. PLDA learns two kinds of spread: how much embeddings of different people differ, and how much embeddings of one person differ from recording to recording.

To compare two recordings, ask two questions. How likely are these two embeddings if one person made both? How likely are they if two different people made them? The score is the log of the ratio of the two answers. Two embeddings that are close count as strong evidence when people differ a lot and one person's recordings differ little. They count as weak evidence when the reverse is true.

## The problem

This is the scoring step of [speaker verification](/speaker-verification/). The input is two embeddings $x_1, x_2 \in \mathbb{R}^d$ and the model parameters. The two-covariance model says that an embedding of speaker $s$ is

$$x = m + y_s + e, \qquad y_s \sim \mathcal{N}(0, B), \qquad e \sim \mathcal{N}(0, W),$$

where $m$ is the mean, $B$ is the between-speaker covariance and $W$ is the within-speaker covariance. All embeddings of one speaker share $y_s$, and each embedding has its own $e$. The output is the log likelihood ratio of $H_s$ (same speaker) against $H_d$ (different speakers),

$$\text{LLR}(x_1, x_2) = \log \frac{p(x_1, x_2 \mid H_s)}{p(x_1, x_2 \mid H_d)}.$$

The parameters are trained on embeddings of many speakers with labels, by EM; this page takes them as given.

## The algorithm

Write $A = B + W$ for the total covariance. Under $H_d$ the pair $(x_1 - m, x_2 - m)$ is Gaussian with independent blocks of covariance $A$. Under $H_s$ the blocks have covariance $A$ and cross covariance $B$. The ratio of these two densities in $2d$ dimensions reduces to a form in $d$ dimensions:

```pseudo id=main
PREPARE(B, W)
L1  A ← B + W,  Λ ← A⁻¹
L2  S ← A - B Λ B,  Γ ← S⁻¹               ▷ S is a Schur complement
L3  Q ← Λ - Γ,  P ← Λ B Γ
L4  c ← ½ (log|A| - log|S|)
SCORE(x₁, x₂, m)
L5  u ← x₁ - m,  v ← x₂ - m
L6  return ½ uᵀQu + ½ vᵀQv + uᵀPv + c
SCORE-MULTI(x₁..xₙ, x_t, m, B, W)          ▷ several enrollment embeddings
L7  Cₙ ← (B⁻¹ + n W⁻¹)⁻¹
L8  μₙ ← Cₙ W⁻¹ Σᵢ (xᵢ - m)
L9  return log N(x_t; m + μₙ, W + Cₙ) - log N(x_t; m, A)
```

L1 to L4 depend only on the model, so they run once. Each trial then costs two quadratic forms. With several enrollment embeddings of one speaker, L7 and L8 compute the posterior of the speaker variable $y$, and L9 compares the predictive density of the test embedding with the density for an unknown speaker. With one enrollment embedding, L9 gives the same value as L6. The code computes the inverses and log determinants with the [Cholesky decomposition](/cholesky-decomposition/).

## Example

Take $d = 1$, $m = 0$, $B = 3$ and $W = 1$. Then $A = 4$, $\Lambda = 1/4$, $S = 4 - 9/4 = 7/4$ and $\Gamma = 4/7$. So $Q = 1/4 - 4/7 = -9/28$, $P = (1/4) \cdot 3 \cdot (4/7) = 3/7$ and $c = \frac12 \log(16/7) = 0.413339$.

| $x_1$ | $x_2$ | LLR |
|---|---|---|
| 1 | 1 | 0.520482 |
| 2 | 2 | 0.841911 |
| 0 | 0 | 0.413339 |
| 1 | -1 | -0.336661 |
| 3 | 0 | -1.033089 |

Equal embeddings far from the mean give more evidence than equal embeddings near it: $(2, 2)$ scores more than $(1, 1)$, and $(0, 0)$ scores least of the three. Two embeddings at the mean also fit the different-speaker hypothesis well, because most speakers are near the mean. Embeddings on opposite sides of the mean give a negative score.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Both hypotheses give Gaussian densities for the pair. The inverse of the joint covariance under $H_s$ has the blocks $\Gamma$ on the diagonal and $-\Lambda B \Gamma$ off it, and its determinant is $|A| |S|$. Subtracting the two log densities gives L6 exactly. The same proof shows that $P$ is symmetric, so the score is symmetric in $x_1$ and $x_2$, and that $Q$ is negative semidefinite and $c \ge 0$. The multi-enrollment score follows from the conjugate Gaussian posterior of $y$. The closed form needs $W$ positive definite but allows a singular $B$, for example $B = F F^\top$ of low rank.

## Complexity

In the real RAM, PREPARE inverts two $d \times d$ matrices and computes two log determinants, in $O(d^3)$ time and $O(d^2)$ memory. Each trial costs $O(d^2)$ for the quadratic forms, so $N$ trials cost $O(d^3 + N d^2)$. For a speaker with $n$ enrollment embeddings, L7 and L8 cost $O(d^3 + n d)$ once, and each test embedding then costs $O(d^2)$ if the inverse and log determinant of $W + C_n$ are kept. With $d$ often 150 to 400 after LDA, scoring is cheap next to computing the embeddings.

## Properties

- **Exact for the model.** The score is the exact log likelihood ratio of the two-covariance model (a theorem). How well it fits real embeddings is a question of measurement.
- **Symmetric.** $\text{LLR}(x_1, x_2) = \text{LLR}(x_2, x_1)$.
- **No speaker model.** Enrollment stores an embedding, or the sufficient statistics $n$ and $\sum_i (x_i - m)$. No per-speaker training is needed.
- **Uses the mean.** The score depends on where the pair lies, not only on the distance between the two embeddings, unlike [cosine similarity](/cosine-similarity/).
- **Not a calibrated ratio in practice.** Real embeddings are not Gaussian, so the scores are often calibrated with an affine map before a Bayes threshold is applied.

## Variants and improvements

- **The Prince-Elder form.** $x = m + F h + G w + \varepsilon$, with a speaker factor $h$, a session factor $w$ and diagonal noise. With $\varepsilon \sim \mathcal{N}(0, \Sigma)$, it is the two-covariance model with $B = F F^\top$ and $W = G G^\top + \Sigma$. Low rank $F$ and $G$ reduce the number of parameters.
- **Simplified PLDA.** Drop $G$ and let the noise covariance be full.
- **Heavy-tailed PLDA.** Student's t priors in place of Gaussians, which fit raw i-vectors better.
- **Length normalization.** Center, whiten and scale each embedding to unit length before Gaussian PLDA. In the experiments of Garcia-Romero and Espy-Wilson 2011, Gaussian PLDA after length normalization did about as well as heavy-tailed PLDA, at a lower cost (a measurement).
- **LDA first.** Reduce the dimension with [linear discriminant analysis](/linear-discriminant-analysis/) (for example to 150) before PLDA.
- **Discriminative training.** Train the parameters $Q$, $P$ and $c$ of the quadratic form directly, for example with [logistic regression](/logistic-regression/) on trial pairs.

## When to use it

Use PLDA when speakers are represented by fixed-length embeddings and the training set has many speakers with several recordings each. It is the usual back end for i-vectors and x-vectors. When the embeddings come from a network trained with an angular margin loss, plain cosine scoring is a common choice. It needs no trained back end, and whether it matches PLDA depends on the system and the data.

## Pitfalls

- **Wrong data for the parameters.** $B$ and $W$ trained on one language or channel do not fit another. Adapt them, or at least recompute the mean on data from the new domain.
- **Skipping length normalization.** Gaussian PLDA on raw embeddings fits poorly, because their norms vary a lot.
- **Singular matrices.** $W$ must be positive definite. With low-rank $G$ and no noise term, $W$ is singular and the inverse fails. Add a diagonal term.
- **Joint densities in $2d$ dimensions.** Computing the two joint densities directly costs $O(d^3)$ per trial and loses precision. Use the closed form.
- **Averaging enrollment scores.** Averaging the LLRs of $n$ enrollment embeddings is not the LLR of the enrollment set. Use SCORE-MULTI, or average the embeddings and accept an approximation.

## Implementations

## History

Ioffe 2006 and Prince and Elder 2007 proposed probabilistic LDA for face recognition. Both write the observation as a class-dependent part plus a within-class part and score identity by comparing hypotheses, with a closed form likelihood. Speaker recognition took PLDA up for i-vectors around 2010, first with heavy-tailed priors and then, after length normalization (Garcia-Romero and Espy-Wilson 2011), with Gaussian priors. When x-vectors replaced i-vectors in 2018, the back end of LDA, length normalization and PLDA stayed the same.

## References
