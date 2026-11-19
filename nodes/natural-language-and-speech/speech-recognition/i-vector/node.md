---
tag: Y9F5Q0
kind: model
slug: i-vector
name: i-vector
aliases:
- identity vector
- total variability model
area: natural-language-and-speech/speech-recognition
level: advanced
summary: A low-dimension vector for an utterance, the posterior mean of a latent factor in a factor analysis model of GMM supervectors.
history:
  year: 2011
  people: [Najim Dehak, Patrick J. Kenny, Réda Dehak, Pierre Dumouchel, Pierre Ouellet]
  note: Dehak et al. replaced the separate speaker and channel subspaces of joint factor analysis with one total variability subspace, and scored the resulting vectors with the cosine after LDA and WCCN. The i-vector with PLDA was the standard speaker recognition system until x-vectors.
prereqs: [factor-analysis, expectation-maximization, gmm-ubm-speaker-verification]
see_also: [plda-scoring, x-vector, map-speaker-adaptation, linear-discriminant-analysis, speaker-verification, speaker-diarization, principal-component-analysis, cosine-similarity]
sources:
  - paper: doi:10.1109/TASL.2010.2064307
    title: Najim Dehak, Patrick J. Kenny, Réda Dehak, Pierre Dumouchel and Pierre Ouellet, Front-end factor analysis for speaker verification, IEEE Transactions on Audio, Speech, and Language Processing 19(4), 2011, pages 788 to 798
    locator: the total variability model, the extraction of the i-vector from the Baum-Welch statistics, and the cosine scoring with LDA and WCCN
  - url: https://cs.joensuu.fi/sipu/pub/SRE-review-Kinnunen-and-Li.pdf
    title: Tomi Kinnunen and Haizhou Li, An overview of text-independent speaker recognition, from features to supervectors, Speech Communication 52(1), 2010, pages 12 to 40
    locator: the sections on GMM supervectors and on factor analysis
  - paper: doi:10.21437/Interspeech.2011-53
    title: Daniel Garcia-Romero and Carol Y. Espy-Wilson, Analysis of i-vector length normalization in speaker recognition systems, Interspeech 2011
    locator: the length normalization of i-vectors before Gaussian PLDA
---

An i-vector is a fixed-length vector, typically of 400 to 600 numbers, that summarizes one utterance of any length. A universal background model (a Gaussian mixture) turns the frames into statistics, and a factor analysis model says that the stacked means of the utterance's mixture lie near a low-dimension subspace of the background means. The i-vector is the posterior mean of the coordinates in that subspace. It carries the speaker and also the channel, so a back end such as [PLDA](/plda-scoring/) separates the two.

## The machine

Let the universal background model (UBM) have $C$ Gaussians with weights, means $m_c \in \mathbb{R}^F$ and diagonal covariances $\Sigma_c$. Stack the $C$ means into a supervector $m \in \mathbb{R}^{CF}$. The total variability model says that the supervector of the mixture that generated an utterance is

$$M = m + T w, \qquad w \sim \mathcal{N}(0, I_R),$$

where $T$ is a $CF \times R$ matrix with $R \ll CF$, and $T_c$ is its block of $F$ rows for component $c$. The frames of the utterance are then drawn from the mixture with means $m_c + T_c w$ and the UBM weights and covariances.

Given the frames $x_1, \ldots, x_n$, compute the occupation $\gamma_c(t)$ of each component under the UBM and the Baum-Welch statistics

$$N_c = \sum_t \gamma_c(t), \qquad \tilde F_c = \sum_t \gamma_c(t) (x_t - m_c).$$

With the occupations held fixed, the posterior of $w$ is Gaussian, with precision and mean

$$L = I + \sum_c N_c T_c^\top \Sigma_c^{-1} T_c, \qquad \hat w = L^{-1} \sum_c T_c^\top \Sigma_c^{-1} \tilde F_c.$$

The i-vector is $\hat w$. The matrix $T$ is trained by EM on many utterances, with every utterance treated as its own source, so no speaker labels are needed. EM is often started from a random $T$.

## What it counts

- **One vector per utterance.** $\hat w$ has the same dimension $R$ for an utterance of 2 seconds and one of 2 minutes.
- **Shrinkage with little data.** The posterior covariance is $L^{-1}$. It depends only on the counts $N_c$, not on the values of the frames, and it shrinks as the counts grow. With little data the i-vector is pulled toward 0, the prior mean.
- **An example.** Take $C = 2$, $F = 1$, $R = 1$, $\Sigma_c = 1$ and $T = (1, 2)^\top$. An utterance with $N = (3, 1)$ and $\tilde F = (1.5, 2)$ gives $L = 1 + 3 \cdot 1 + 1 \cdot 4 = 8$, so $\hat w = (1 \cdot 1.5 + 2 \cdot 2)/8 = 0.6875$ with posterior variance $0.125$. Ten times as much data of the same kind gives $L = 71$, $\hat w = 55/71 = 0.774648$ and variance $0.014085$. As the data grow, $\hat w$ goes to $5.5/7 = 0.785714$, the maximum likelihood value.
- **Cost.** The statistics cost $O(n C F)$ for $n$ frames. With the matrices $T_c^\top \Sigma_c^{-1} T_c$ stored ($O(C R^2)$ memory), $L$ costs $O(C R^2)$ and solving for $\hat w$ costs $O(R^3)$. For large $C$ and $R$ this is more than the cost of the statistics, and fast approximations exist.

## Relation to other models

- **[Factor analysis](/factor-analysis/).** The total variability model is factor analysis of the supervector, with a hidden assignment of frames to components. Its posterior has the same form as in factor analysis, weighted by the counts.
- **[MAP adaptation](/map-speaker-adaptation/).** Relevance MAP of the means is the model $M = m + D z$ with $z \sim \mathcal{N}(0, I)$ and a diagonal $D$ with $D_c^2 = \Sigma_c / r$. It is full rank and has no shared subspace; the i-vector model is low rank.
- **Joint factor analysis.** JFA writes $M = m + V y + U x + D z$, with a speaker subspace $V$ and a channel subspace $U$. The i-vector model uses one subspace $T$ for both, because the channel subspace of JFA also carried speaker information.
- **The back end.** The i-vector carries channel effects. LDA, within-class covariance normalization (WCCN), length normalization and [PLDA](/plda-scoring/) or the [cosine](/cosine-similarity/) score handle them. Dehak et al. 2011 used LDA, WCCN and the cosine.
- **[x-vectors](/x-vector/).** x-vectors replace the UBM statistics and the subspace with a network trained to classify speakers, and keep the same back end.
- **[GMM-UBM](/gmm-ubm-speaker-verification/).** Both start from the same UBM. GMM-UBM keeps a whole adapted mixture per speaker; the i-vector keeps $R$ numbers per utterance.

## Known results in the model

- **Exact posterior (a theorem).** With the occupations fixed, the prior of $w$ is conjugate to the Gaussian likelihood of the frames, so the posterior is exactly $\mathcal{N}(\hat w, L^{-1})$. Writing the log posterior as a quadratic in $w$ gives $L$ and $\hat w$ above.
- **EM for $T$.** Each EM iteration does not decrease the likelihood of the training statistics, by the usual argument for [EM](/expectation-maximization/). The E-step needs the posterior mean and the posterior covariance of $w$ for every utterance.
- **Length normalization (a measurement).** Garcia-Romero and Espy-Wilson 2011 found that i-vectors are far from Gaussian, and that scaling them to unit length after centering and whitening lets Gaussian PLDA reach the accuracy of heavy-tailed PLDA.
- **Accuracy (a measurement).** Dehak et al. 2011 compare the system with JFA on NIST SRE 2008 data and report better results for the i-vector system. Error rates depend on the data set and the conditions. Snyder et al. 2018 found x-vectors more accurate than i-vectors on their test sets, especially when the training data were augmented.
- **Other uses.** The same vector is used for language identification, for [diarization](/speaker-diarization/) and as an input that adapts neural acoustic models to the speaker.

## References
