---
tag: DH4WPC
kind: technique
slug: sparse-channel-estimation
name: Sparse channel estimation
aliases:
- compressed channel sensing
area: communications/channel-estimation-and-equalization
level: advanced
summary: "Estimate a channel with L taps of which only S are nonzero by sparse recovery, such as OMP or basis pursuit, from fewer than L pilot samples, with an error that scales with S and not L."
prereqs: [least-squares-channel-estimation, compressed-sensing, orthogonal-matching-pursuit]
see_also: [channel-estimation, sparse-signal-recovery, basis-pursuit, lasso-regression, iterative-hard-thresholding, mutual-coherence, restricted-isometry-property, delay-spread]
sources:
  - paper: doi:10.1109/JPROC.2010.2042415
    title: "Waheed U. Bajwa, Jarvis Haupt, Akbar M. Sayeed and Robert Nowak, Compressed channel sensing: a new approach to estimating sparse multipath channels, Proceedings of the IEEE 98(6), 2010, pages 1058 to 1076"
    locator: "sparse multipath channel models and compressed sensing estimators from training signals"
  - paper: "Shane F. Cotter and Bhaskar D. Rao, Sparse channel estimation via matching pursuit with application to equalization, IEEE Transactions on Communications 50(3), 2002, pages 374 to 377"
    locator: "the matching pursuit channel estimate, compared with thresholded least squares, and its use in an equalizer"
  - paper: doi:10.1109/TIT.2004.834793
    title: "Joel A. Tropp, Greed is good: algorithmic results for sparse approximation, IEEE Transactions on Information Theory 50(10), 2004, pages 2231 to 2242"
    locator: "the exact recovery condition for orthogonal matching pursuit and the bound in terms of the coherence"
---

Sparse channel estimation is [channel estimation](/channel-estimation/) for a channel whose impulse response has only a few large taps. Many wideband channels look like this: the delay spread covers $L$ taps, but the energy arrives along a small number $S$ of paths, so most taps are zero or close to zero. The pilot model is the usual $y = X h + w$, with $m$ pilot samples, but the unknown $h \in \mathbb{C}^L$ has at most $S$ nonzero entries. [Least squares](/least-squares-channel-estimation/) ignores this. It needs $m \ge L$ samples, and its error grows with $L$. Sparse recovery uses it. Methods of [compressed sensing](/compressed-sensing/), such as [orthogonal matching pursuit](/orthogonal-matching-pursuit/) (OMP) and [basis pursuit](/basis-pursuit/), find the few active taps and their gains from fewer samples, and they put the noise only on the taps they keep. Bajwa, Haupt, Sayeed and Nowak (2010) called this compressed channel sensing and studied it for multipath models in delay, Doppler and angle.

## In plain words

Suppose a channel can have echoes at any of 16 delays, but in fact only 2 echoes arrive. A plain estimator measures all 16 delays, and each measurement picks up some noise, so the result has noise at 16 places. A sparse estimator first asks which delays hold the real echoes. It picks the delay that best explains the received pilots, removes its effect, and repeats. Then it measures only the delays it picked. This needs fewer pilots, and it gets less noise, because it estimates 2 numbers instead of 16. The risk is to pick a wrong delay, which can happen if the pilots are too few or badly chosen.

## When it applies

- The channel has few significant paths compared with its length in taps: $S \ll L$. This is common in wideband systems with a long delay spread, in underwater acoustic links, and in millimeter wave links, where a few paths dominate in delay and in angle.
- The pilot matrix $X$ is incoherent enough: different taps must give pilot responses that do not look alike. Random or pseudo-random training sequences, and pilots on random OFDM subcarriers, are good choices; a constant sequence is the worst.
- The sparsity is in the right basis. Paths at delays between the sampling instants spread over several taps. If this leakage is large, the channel is only approximately sparse, and the gain falls.

## The template

**Model.** $y = X h + w$, $X \in \mathbb{C}^{m \times L}$ from the pilots, $w \sim \mathcal{CN}(0, N_0 I)$, and $\|h\|_0 \le S$. The pilot rows are formed as for any FIR channel estimate; $m$ may be smaller than $L$.

**Greedy recovery (OMP).** Let $x_j$ be column $j$ of $X$.

1. Set the residual $r = y$ and the support $T = \emptyset$.
2. Find the tap $j \notin T$ that maximizes $|x_j^H r| / \|x_j\|$, and add it to $T$.
3. Solve least squares on the support: $\hat h_T = (X_T^H X_T)^{-1} X_T^H y$, and set $r = y - X_T \hat h_T$.
4. Stop after $S$ steps, or when $\|r\|^2$ falls to about $m N_0$, the expected noise energy. Otherwise go to step 2.
5. Output $\hat h$ with the entries $\hat h_T$ on $T$ and zeros elsewhere.

Each step costs $O(m L)$ for the correlations and $O(m |T|^2)$ for the update, so $S$ steps cost $O(S m L + S^3)$ at most. For a Toeplitz $X$, the correlations are one convolution of the residual with the pilots.

**Convex recovery.** Basis pursuit denoising, or the [lasso](/lasso-regression/), solves $\min_h \tfrac{1}{2}\|y - X h\|^2 + \lambda \|h\|_1$, with $\lambda$ of the order of $\sqrt{N_0 \log L}$ times the column norm. It is slower than OMP but does not need $S$.

**Why it works.** Let $\mu$ be the largest normalized correlation $|x_i^H x_j| / (\|x_i\| \|x_j\|)$ between two different columns, the [mutual coherence](/mutual-coherence/). Tropp (2004) showed that, with no noise, OMP finds the exact support of every $S$-sparse $h$ in $S$ steps if $\mu < 1/(2S - 1)$; the same condition holds for basis pursuit. Conditions of the [restricted isometry](/restricted-isometry-property/) kind allow larger $S$ for random pilots, with $m$ of the order of $S$ times a logarithm of $L$.

**Noise gain.** Once the support $T$ is right, the error is the least squares error on $T$ alone, $N_0\, \mathrm{tr}((X_T^H X_T)^{-1})$. With pilots of unit energy and nearly orthogonal columns, $X^H X \approx m I$, so this is about $S N_0 / m$, against $L N_0 / m$ for full least squares. The gain is the factor $L / S$.

## Classic examples

**Two paths among 16 taps, from 8 samples.** Let $L = 16$, $m = 8$, and the 23 training symbols be $x = (-, -, +, -, +, +, +, +, -, -, +, -, +, +, -, +, +, -, -, +, -, -, -)$, with $\pm$ for $\pm 1$ and row $i$ of $X$ equal to $(x[i + 15], \ldots, x[i])$. The channel has $h_3 = 1$ and $h_{11} = -0.6$, all other taps zero. Least squares cannot work, since $m < L$. With no noise, $y = (0.4, 0.4, -1.6, 0.4, 1.6, -0.4, -1.6, 1.6)$. The correlations $X^T y$ are largest at tap 3, with 8.0, and the next largest is 6.4 at tap 5, not at tap 11, which has $-4.8$. After step 3 removes tap 3, the largest correlation is at tap 11, and OMP returns $h$ exactly. For this sequence and the gains $(1, -0.6)$, OMP finds the correct pair for all $\binom{16}{2} = 120$ positions of the two paths. The coherence of $X$ is 0.75, so the guarantee $\mu < 1/(2S - 1)$ covers only $S = 1$. The guarantee is a worst case and is often pessimistic.

**The noise gain at $L = 16$, $S = 2$.** With $m = 32$ pilot samples and orthogonal columns, $X^H X = 32 I$. Full least squares has the error $16 N_0 / 32 = 0.5\, N_0$. Least squares on the two true taps has the error $2 N_0 / 32 = 0.0625\, N_0$, a gain of $16/2 = 8$, or 9.0 dB. OMP reaches this error when it finds the right support, which is likely at a high pilot SNR.

**Thresholded least squares.** A simple alternative computes the full least squares estimate and sets to zero every tap with $|\hat h_j|^2$ below a threshold, a few times $N_0 / m$. It needs $m \ge L$, but it removes most of the noise on the empty taps. Cotter and Rao (2002) compared matching pursuit estimates with thresholded least squares and used them in an equalizer.

## Variations

- **Algorithms.** OMP, [CoSaMP](/cosamp/), [iterative hard thresholding](/iterative-hard-thresholding/) and basis pursuit or the lasso, all from [sparse signal recovery](/sparse-signal-recovery/).
- **OFDM pilots.** The pilot subcarriers give rows of a DFT matrix. Pilots at random subcarriers make $X$ incoherent, while a regular comb, the usual choice of [comb pilot estimation](/comb-pilot-channel-estimation/), gives equal columns for taps whose delays differ by a multiple of the number of pilots.
- **Delay and Doppler.** A doubly selective channel with few paths is sparse in a delay and Doppler grid, as in [OTFS](/orthogonal-time-frequency-space-modulation/) systems.
- **Angle.** Massive MIMO and millimeter wave channels with few paths are sparse in the angle domain, which [hybrid beamforming](/hybrid-beamforming/) receivers use to estimate many antennas from few RF chains.
- **Structure.** Taps that come in clusters, or several channels with the same support, as on several antennas, lead to block and joint sparse recovery.
- **Tracking.** A support that changes slowly can be kept from frame to frame and updated, with fewer pilots per frame.

## Pitfalls

- **Off-grid paths.** A path delay between two taps, after the transmit and receive filters, spreads over many taps with slowly decaying sidelobes. The channel is then compressible, not sparse, and an estimate with $S$ taps has a bias floor. Finer grids raise the coherence of $X$.
- **Unknown sparsity.** Running OMP for too many steps adds noise taps, and too few steps miss weak paths. A residual threshold near $m N_0$ needs a good noise estimate.
- **Pilots with high coherence.** A periodic or constant training sequence makes some columns of $X$ equal, and no algorithm can separate those taps. Check the coherence or test the recovery on random supports before using a sequence.
- **Weak paths below the noise.** Sparse recovery finds strong paths reliably. A path whose gain is below the noise level per tap may be missed, and that error is not averaged away.
- **Comparing at equal pilots.** The gain over least squares comes from both fewer unknowns and fewer pilots. When pilots are cheap and $m \gg L$, the gain is only the noise factor $L / S$, and thresholded least squares gets most of it.

## Exercises

1. Show that if $h$ is $S$-sparse and every set of $2S$ columns of $X$ is linearly independent, then $h$ is the only $S$-sparse vector with $X h = y$ when there is no noise.
2. For $S = 1$ and no noise, show that the first step of OMP finds the right tap if $\mu < 1$, and that this matches $\mu < 1/(2S - 1)$.
3. Give a training sequence of length 10 for $L = 4$ such that two columns of $X$ are equal, and explain which channels it cannot tell apart.
4. With $X^H X = m I$ and the support known, derive the error $S N_0 / m$ of least squares on the support and compare it with the [Cramer-Rao bound](/cramer-rao-bound/) for the $S$ gains.
5. Explain why a regular comb of $P$ pilots, one every $N/P$ of the $N$ OFDM subcarriers, cannot separate taps $j$ and $j + P$, and why random pilot positions avoid this.

## References
