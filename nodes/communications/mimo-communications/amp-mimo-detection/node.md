---
tag: V4YK5H
kind: algorithm
slug: amp-mimo-detection
name: Approximate message passing MIMO detection
aliases:
- AMP detector
- LAMA
area: communications/mimo-communications
level: research
summary: Detects a large MIMO system by approximate message passing with a symbol denoiser. For large i.i.d. channels its error rate is predicted by a scalar recursion, and it can reach the optimal error rate.
solves: [mimo-detection]
model: real-ram
complexity:
  vars: {n: the number of transmitted streams, m: the number of receive antennas, M: the constellation size, T: the number of iterations}
  time: {worst: O(T (n m + n M))}
  space: {extra: O(n m)}
properties: {deterministic: true, exact_ml: false, needs_noise_level: true, needs_matrix_inverse: false, channel_assumption: "large, with i.i.d. zero-mean entries", fixed_point_with_gaussian_prior: "the linear MMSE estimate"}
history:
  year: 2015
  people: [Charles Jeon, Ramina Ghods, Arian Maleki, Christoph Studer]
  note: "Donoho, Maleki and Montanari introduced AMP for compressed sensing in 2009, and Bayati and Montanari proved its state evolution in 2011. Jeon, Ghods, Maleki and Studer gave the complex Bayesian form for MIMO detection, LAMA, at ISIT 2015."
prereqs: [mimo-detection, mmse-mimo-detector, belief-propagation]
see_also: [approximate-message-passing, expectation-propagation-detection, mmse-mimo-detector, massive-mimo, iterative-shrinkage-thresholding, compressed-sensing, soft-demapping, message-passing]
sources:
  - paper: doi:10.1109/ISIT.2015.7282651
    title: Charles Jeon, Ramina Ghods, Arian Maleki and Christoph Studer, Optimality of large MIMO detection via approximate message passing, Proc. IEEE International Symposium on Information Theory (ISIT), Hong Kong, 2015, pages 1227-1231
    locator: the LAMA iteration for complex constellations, its state evolution and the conditions under which it reaches the individually optimal detector
  - paper: "Charles Jeon, Ramina Ghods, Arian Maleki and Christoph Studer, Optimal data detection in large MIMO, arXiv:1811.01917, 2018"
    locator: "Section II-A (the model, assumptions A1 and A2, beta = MT / MR), Section III-B (Algorithm 2, LAMA, and the denoisers F and G), Theorem 1 and Corollary 2 (state evolution), and Section IV (optimality, which uses the replica method for the optimal detector)"
  - paper: doi:10.1073/pnas.0909892106
    title: David L. Donoho, Arian Maleki and Andrea Montanari, Message-passing algorithms for compressed sensing, Proceedings of the National Academy of Sciences 106(45), 18914-18919, 2009
    locator: the AMP iteration with the Onsager term and its state evolution
  - paper: doi:10.1109/TIT.2010.2094817
    title: Mohsen Bayati and Andrea Montanari, The dynamics of message passing on dense graphs, with applications to compressed sensing, IEEE Transactions on Information Theory 57(2), 764-785, 2011
    locator: the proof of state evolution for i.i.d. Gaussian matrices and Lipschitz denoisers in the large system limit
---

Approximate message passing (AMP) MIMO detection solves the [MIMO detection](/mimo-detection/) problem for large systems by an iteration that costs two matrix-vector products per step and needs no matrix inverse. Each step forms one noisy copy $z_k$ of every transmitted symbol, removes the noise from it with the exact posterior mean for the constellation, and corrects the residual with an extra term, the Onsager term. For a channel with many antennas and i.i.d. zero-mean entries, the copies $z_k$ behave like $x_k$ plus Gaussian noise of a variance $s^2$ that a scalar recursion, the state evolution, predicts. So the large MIMO channel splits into $n$ scalar AWGN channels. The detector of this page is LAMA (large MIMO AMP) of Jeon, Ghods, Maleki and Studer (2015). The general AMP method for linear inverse problems, with sparse priors and soft thresholding, is on the [approximate message passing](/approximate-message-passing/) page. This page uses a discrete constellation prior and adds the MIMO results. [Expectation propagation detection](/expectation-propagation-detection/) has a similar goal, but it works for small and correlated channels and inverts an $n \times n$ matrix at each step.

## In plain words

The receiver wants to know every symbol, and each antenna hears a mix of all of them. AMP guesses all symbols at once, computes what the antennas would hear for that guess, and looks at the difference. It uses the difference to make a new noisy copy of each symbol. Then it cleans each copy on its own: it knows that a symbol must be one of a few points, so it replaces the copy by the average of those points, weighted by how likely each one is. The clever part is a small correction term in the difference. Without it, the errors of one step feed back into the next one and pile up. With it, the error in each copy looks like fresh Gaussian noise of a known size. This is only true when the channel is large and random enough.

## The problem

The model is $y = H x + w$ with $H \in \mathbb{C}^{m \times n}$ known, $x \in \mathcal{S}^n$ for a constellation $\mathcal{S}$ of $M$ equally likely points with mean 0 and energy $E_s = 1$, and $w \sim \mathcal{CN}(0, N_0 I)$. The SNR is $E_s / N_0$ per complex symbol. The system ratio is $\beta = n / m$. The theory of AMP assumes that the entries of $H$ are i.i.d. $\mathcal{CN}(0, 1/m)$, so every column has a squared norm close to 1, and that $m$ and $n$ are large with $\beta$ fixed. The detector returns decisions $\hat x \in \mathcal{S}^n$ and, for soft output, the copies $z_k$ with their noise variance $s^2$.

## The algorithm

For a point $z \in \mathbb{C}$ and a variance $s^2$, let the weights be $w_a \propto \exp(-|z - a|^2 / s^2)$ for $a \in \mathcal{S}$, normalized to sum 1. These are the posterior probabilities of $X = a$ given $z = X + \mathcal{CN}(0, s^2)$. The denoiser is the posterior mean $F(z, s^2) = \sum_a w_a a$, and $G(z, s^2) = \sum_a w_a |a - F|^2$ is the posterior variance.

```pseudo id=main
AMP-DETECT(y, H, S, N0, T)
L1  x̂ ← (E[X], ..., E[X])                        ▷ the prior mean, 0 here
L2  r ← y - H x̂;  s² ← N0 + β Var[X]
L3  for t ← 1 to T
L4      z ← x̂ + Hᴴ r                             ▷ z_k ≈ x_k + CN(0, s²)
L5      for each k: x̂'_k ← F(z_k, s²),  g_k ← G(z_k, s²)
L6      r ← y - H x̂' + (β ḡ / s²) r               ▷ ḡ = the mean of g_k; Onsager term
L7      s² ← N0 + β ḡ;  x̂ ← x̂'
L8  for each k: x̂_k ← the point of S nearest to z_k
L9  return x̂
```

Line L4 adds the matched filter output of the residual to the current estimate. Line L5 is $n$ independent scalar posterior computations of $O(M)$ each. The term $(\beta \bar g / s^2) r$ of line L6 is the Onsager term: $\bar g / s^2$ is the mean derivative of $F$ with respect to $z$, so the term subtracts the part of the residual that comes from the estimate's own dependence on the earlier residual. Line L7 updates the noise variance. In LAMA this variance is written $N_0 (1 + \tau)$, with $\tau = \beta \bar g / N_0$; it is the same quantity. Line L8 is the ML decision for the scalar channel $z_k = x_k + \mathcal{CN}(0, s^2)$ with equal priors. A soft-output receiver instead computes bit LLRs from $z_k$ and $s^2$ as in [soft demapping](/soft-demapping/).

## Example

**A small channel, where AMP fails.** Take BPSK, $m = n = 2$, the channel of the [ZF page](/zero-forcing-mimo-detector/) with unit-norm columns,

$$H = \begin{pmatrix} 2/\sqrt 5 & 1/\sqrt 2 \\ 1/\sqrt 5 & 1/\sqrt 2 \end{pmatrix},$$

$y = (0.5, 0.6)$ and $N_0 = 0.25$. Then $\beta = 1$, and line L2 sets $r = y$ and $s^2 = 0.25 + 1 = 1.25$. For BPSK, $F(z, s^2) = \tanh(2 \,\mathrm{Re}\, z / s^2)$ and $G = 1 - F^2$. The first step gives

$$z = H^T y = (1.6/\sqrt 5,\; 1.1/\sqrt 2) = (0.7155,\; 0.7778),$$

$\hat x' = (\tanh 1.1448, \tanh 1.2445) = (0.8160, 0.8467)$, $\bar g = (0.3341 + 0.2831)/2 = 0.3086$, and the new $s^2 = 0.25 + 0.3086 = 0.5586$. The next steps give these values of $z$ (real parts, from the implementation):

| step | $z_1$ | $z_2$ | $s^2$ after the step |
|---|---|---|---|
| 1 | 0.7155 | 0.7778 | 0.5586 |
| 2 | 0.0889 | 0.1956 | 1.0197 |
| 3 | -0.8603 | -0.4116 | 0.5909 |
| 4 | 0.9588 | 1.3240 | 0.2533 |
| 5 | -0.2224 | -0.1569 | 0.4491 |

The signs flip from step to step, and the iteration does not settle. The ML vector is $(-1, +1)$, with metric 0.588 against 0.837 for $(+1, -1)$. Here the two columns have the correlation $3/\sqrt{10} = 0.949$, and $\beta = 1$ with $n = 2$ is far from the large i.i.d. setting that AMP needs.

**A large random channel, where AMP works.** Take 4-QAM, $n = 32$, $m = 64$ ($\beta = 0.5$), i.i.d. $\mathcal{CN}(0, 1/m)$ entries and $N_0 = 0.25$ ($E_s/N_0 = 6.02$ dB). The state evolution (Monte Carlo with 4000 samples, seed 2105) and the mean of $|z_k - x_k|^2$ measured over 20 channels (seed 7) are:

| step | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| state evolution $s^2$ | 0.750 | 0.429 | 0.344 | 0.316 | 0.307 | 0.304 | 0.303 |
| measured $\overline{\lvert z_k - x_k \rvert^2}$ | 0.796 | 0.413 | 0.328 | 0.303 | 0.297 | 0.289 | 0.290 |
| measured symbol error rate | 0.219 | 0.127 | 0.088 | 0.084 | 0.069 | 0.063 | 0.066 |

The fixed point $s^2 = 0.303$ predicts the symbol error rate $2Q(\sqrt{1/s^2}) - Q(\sqrt{1/s^2})^2 = 0.068$ of 4-QAM on the scalar channel, and the measurement is 0.066 (measurement, 640 symbols). For comparison, the linear MMSE detector in the same large system has the decoupled variance 0.390, the root of $s^2 = N_0 + \beta s^2 / (1 + s^2)$, and the error rate 0.106. The prior of the constellation gains 1.1 dB over the linear filter here.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows four things. First, $F$ and $G$ are the exact posterior mean and variance of a symbol seen through the scalar channel $z = x + \mathcal{CN}(0, s^2)$, and line L8 is the exact ML decision for that channel (a theorem). Second, with the Gaussian prior $\mathcal{CN}(0, E_s)$ in place of the constellation, every fixed point of the iteration is the linear MMSE estimate $(H^H H + (N_0/E_s) I)^{-1} H^H y$, for every $H$ (a theorem; the test checks it within $10^{-8}$). Third, for i.i.d. Gaussian $H$ in the large system limit, the state evolution $s^2_{t+1} = N_0 + \beta\, E|F(X + s_t Z, s_t^2) - X|^2$ gives the variance of $z_k - x_k$ at each step (a theorem of Bayati and Montanari for the real case with Lipschitz denoisers, stated for the complex case by Jeon et al.; this page does not prove it). Fourth, if the state evolution has a unique fixed point, the LAMA error rate equals that of the individually optimal detector. That statement rests on the replica method of statistical physics for the optimal detector, so it is a theorem only where the replica prediction has been proved; Jeon et al. give the conditions on $\beta$, the SNR and the constellation.

## Complexity

Each iteration costs two matrix-vector products, $H^H r$ and $H \hat x'$, of $n m$ complex multiplications each, and $n$ denoiser calls of $O(M)$ each. So $T$ iterations cost $O(T (n m + n M))$ in the [real RAM](/real-ram/), with $O(n m)$ space for $H$. There is no matrix inverse and no factorization, which is the main gain over the [MMSE detector](/mmse-mimo-detector/) at $O(n^2 m + n^3)$ per channel when $n$ is in the hundreds. The number of iterations does not grow with $n$ in the large system limit, because the state evolution does not depend on $n$; 10 to 20 steps are typical.

## Properties

- **Decoupling.** In the large i.i.d. setting each stream sees a scalar AWGN channel of variance $s^2$ (theorem, in the limit). The test checks the tracked $s^2$ against the measured noise within 25 percent for $n = 32$, $m = 64$.
- **Linear MMSE as a special case.** With a Gaussian prior, the fixed point is the linear MMSE estimate (theorem).
- **Possible optimality.** For some $\beta$, SNR and constellations, the error rate reaches that of the individually optimal detector in the limit (see Correctness for the status of this claim).
- **Measured agreement with ML.** For 4-QAM, $n = 4$, $m = 8$, i.i.d. $\mathcal{CN}(0, 1/m)$ entries and $E_s/N_0 = 15$ dB, the test with seed 2103 runs 100 vectors, and AMP with 15 steps agrees with brute-force ML on 98 (measurement).
- **Noiseless recovery.** With $N_0 = 0$, $n = 8$, $m = 32$ and 4-QAM, AMP recovered all 30 test vectors (seed 2102, measurement).
- **No guarantee for small or correlated channels.** The iteration can oscillate or diverge, as the first example shows.

## Variants and improvements

- **Damping.** Replace $\hat x'$ by a convex combination of the new and the old estimate. This helps on mildly correlated channels but removes the exact state evolution.
- **Orthogonal and vector AMP.** OAMP and VAMP replace the matched filter step by a linear MMSE step and keep a state evolution for right-rotationally invariant matrices, a much larger class than i.i.d. They need a matrix inverse or an SVD per channel.
- **Mismatched noise.** LAMA allows a postulated noise $N_0^{\text{post}} \ne N_0$; Jeon et al. give the state evolution for this case.
- **Soft output for coding.** The pairs $(z_k, s^2)$ feed a [soft demapper](/soft-demapping/) and then an LDPC or turbo decoder, as in [turbo equalization](/turbo-equalization/).
- **Real-valued form.** Writing the complex model as a real model of size $2m \times 2n$ gives the AMP of compressed sensing with a PAM prior.

## When to use it

Use AMP in large MIMO uplinks with $n$ and $m$ in the tens to hundreds and channels close to i.i.d., where the inverse of the [MMSE detector](/mmse-mimo-detector/) is too costly and a gain over linear detection is wanted. For small systems use a sphere search such as [Schnorr-Euchner enumeration](/schnorr-euchner-enumeration/) or the [K-best detector](/k-best-detector/). For correlated channels use [expectation propagation detection](/expectation-propagation-detection/) or a damped or vector form of AMP. In [massive MIMO](/massive-mimo/) with $m \gg n$, the linear detectors are already close to optimal, and AMP gains little.

## Pitfalls

- **Small or correlated channels.** The state evolution is a large-system result for i.i.d. entries. On a small or correlated channel AMP can oscillate, as in the example.
- **Wrong normalization.** The iteration assumes columns of squared norm about 1 (entries of variance $1/m$). Scale $H$ and $y$ before the iteration, and keep $N_0$ consistent with the scaling.
- **Dropping the Onsager term.** Without it, the iteration is iterative soft thresholding with a constellation denoiser. The noise in $z$ is then not Gaussian, and the tracked $s^2$ is wrong.
- **Overflow in the denoiser.** At small $s^2$ the weights $\exp(-|z - a|^2 / s^2)$ underflow. Subtract the largest exponent first, as the implementation does.
- **Reading the limit theorems as finite results.** The decoupling and the optimality are statements in the limit $n, m \to \infty$. For finite sizes they are good approximations, and the agreement must be measured.
- **Nonzero mean constellations.** Line L1 starts at the prior mean. With a constellation of nonzero mean, $\mathrm{Var}[X]$ in line L2 is not $E_s$.

## Implementations

## History

Message passing on dense graphs was used in CDMA multiuser detection from statistical physics in the early 2000s. Donoho, Maleki and Montanari (2009) wrote the AMP iteration for compressed sensing, with the Onsager term and the state evolution, and Bayati and Montanari (2011) proved the state evolution for i.i.d. Gaussian matrices. Jeon, Ghods, Maleki and Studer (2015) adapted the complex Bayesian form to MIMO detection with discrete constellations, named it LAMA, and gave conditions under which it reaches the individually optimal detector in the large system limit. Later work on orthogonal and vector AMP extended the method to a much larger class of channel matrices.

## References
