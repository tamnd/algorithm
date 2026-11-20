---
tag: GSXKAS
kind: algorithm
slug: iq-imbalance-compensation
name: IQ imbalance compensation
aliases:
- IQ mismatch compensation
area: communications/ofdm-and-multicarrier
level: advanced
summary: "Estimates from two training symbols how IQ imbalance couples each OFDM subcarrier with its mirror, and removes the mirror image by a 2x2 solve per pair of subcarriers."
solves: [channel-equalization]
model: real-ram
complexity:
  vars: {N: the number of subcarriers}
  time: {worst: O(N)}
  space: {extra: O(N)}
properties: {deterministic: true, data_aided: true, exact_without_noise: true, joint_with_channel: true}
history:
  year: 2005
  people: [Alireza Tarighat, Rahim Bagheri, Ali H. Sayed]
  note: "Tarighat, Bagheri and Sayed modeled receiver IQ imbalance in OFDM as interference between mirror subcarriers and gave compensation schemes before and after the DFT, with an analysis of their performance."
prereqs: [orthogonal-frequency-division-multiplexing, quadrature-amplitude-modulation, least-squares-channel-estimation]
see_also: [common-phase-error-correction, inter-carrier-interference, channel-estimation, signal-constellation, frequency-offset-estimation, discrete-multitone, gaussian-elimination, orthogonal-frequency-division-multiple-access]
sources:
  - paper: doi:10.1109/TSP.2005.851156
    title: "A. Tarighat, R. Bagheri and A. H. Sayed, Compensation schemes and performance analysis of IQ imbalances in OFDM receivers, IEEE Transactions on Signal Processing 53(8), 2005"
    locator: "pages 3257 to 3268 (the model in which each subcarrier interferes with its mirror, and compensation schemes in the time and the frequency domain)"
---

IQ imbalance compensation removes a distortion of the analog receiver that an [OFDM](/orthogonal-frequency-division-multiplexing/) system feels strongly. A direct-conversion receiver mixes the signal down on two branches, in phase and in quadrature, and their gains and phases never match exactly. With a gain $g$ and a phase error $\phi$ on the quadrature branch, the complex baseband signal $y$ becomes $r = \mu y + \nu y^*$, with $\mu = (1 + g e^{-j\phi})/2$ and $\nu = (1 - g e^{j\phi})/2$. Conjugation in time mirrors the spectrum, so after the DFT, subcarrier $k$ receives an image of its mirror subcarrier $-k$: $R[k] = A[k] X[k] + B[k] X[-k]^*$, with $A[k] = \mu H[k]$ and $B[k] = \nu H[-k]^*$. The receiver estimates $A$ and $B$ from two training symbols by a 2x2 solve per subcarrier, and then recovers the data of each mirror pair by another 2x2 solve. This handles the channel and the imbalance together and is exact without noise. The page uses $j$ for the imaginary unit and the unitary DFT pair of the OFDM page, with indices modulo $N$, so $-k$ is $N - k$.

## In plain words

A radio receiver splits the signal into two parts, which should be exactly equal in strength and exactly a quarter turn apart. Cheap hardware gets this slightly wrong. The result is a faint mirror image: every subcarrier gets a little copy of the subcarrier on the opposite side of the center. If the opposite subcarrier is strong and this one is weak, the copy can spoil it. The receiver learns how strong the copy is from two known symbols, designed so that the true signal and the copy can be told apart. Then, for each pair of mirror subcarriers, it solves two equations in two unknowns to get both data values back without the copy.

## The problem

The input is the received OFDM symbols after the DFT: two training symbols $R_1$, $R_2$ with the known values $T_1$, $T_2$, and a data symbol $R$. The model is $R[k] = A[k] X[k] + B[k] X[-k]^* + V[k]$ with unknown $A[k]$ and $B[k]$ that stay the same during the burst, and noise $V$. Subcarriers $0$ and $N/2$ are their own mirrors and carry no data. Output estimates of $X[k]$ for every other subcarrier.

## The algorithm

```pseudo id=main
IQ-COMPENSATE(R1, R2, T1, T2, R)
L1  for k ≠ 0, N/2: M ← [[T1[k], conj(T1[-k])], [T2[k], conj(T2[-k])]]
L2      (A[k], B[k]) ← the solution of M (A, B) = (R1[k], R2[k])
L3  for k ≠ 0, N/2: Q ← [[A[k], B[k]], [conj(B[-k]), conj(A[-k])]]
L4      (X̂[k], ·) ← the solution of Q (u, v) = (R[k], conj(R[-k]))
L5  return X̂
```

Lines L1 and L2 write the training symbols in the model, two equations per subcarrier with the unknowns $A[k]$ and $B[k]$, and solve them. The training must make the matrix nonsingular: here $T_2$ equals $T_1$ on the lower half of the band and $-T_1$ on the upper half, so exactly one of $k$ and $-k$ changes sign. Line L3 forms the equations of the data symbol at $k$ and at its mirror, conjugated, which have the two unknowns $X[k]$ and $X[-k]^*$. Line L4 solves them and keeps $X[k]$; the mirror value is found again when the loop reaches $-k$. The estimates of line L2 contain the channel, so no separate channel estimate is needed.

## Example

Take $N = 8$, the channel taps $(0.9, 0.3j, -0.2)$, $g = 1.1$, $\phi = 5$ degrees, random 4-QAM training and data (seed 2), zero on subcarriers 0 and 4, and no noise. Then $\mu = 1.048 - 0.048j$ and $\nu = -0.048 - 0.048j$, and the image rejection ratio $|\mu|^2 / |\nu|^2$ is $23.79$ dB.

| $k$ | $H[k]$ | $A[k]$ (line L2) | $B[k]$ (line L2) | sent $X[k]$ | $R[k] / A[k]$ (one tap) | error | $\hat X[k]$ (line L4) |
|---|---|---|---|---|---|---|---|
| 1 | $1.112 + 0.412j$ | $1.185 + 0.379j$ | $-0.034 - 0.032j$ | $-0.707 - 0.707j$ | $-0.719 - 0.743j$ | 0.038 | $-0.707 - 0.707j$ |
| 2 | $1.400$ | $1.467 - 0.067j$ | $-0.038 - 0.038j$ | $-0.707 - 0.707j$ | $-0.709 - 0.670j$ | 0.037 | $-0.707 - 0.707j$ |
| 3 | $1.112 - 0.412j$ | $1.146 - 0.485j$ | $-0.032 - 0.034j$ | $0.707 + 0.707j$ | $0.673 + 0.692j$ | 0.038 | $0.707 + 0.707j$ |
| 5 | $0.688 - 0.012j$ | $0.720 - 0.046j$ | $-0.034 - 0.073j$ | $0.707 + 0.707j$ | $0.605 + 0.662j$ | 0.111 | $0.707 + 0.707j$ |
| 6 | $0.800$ | $0.838 - 0.038j$ | $-0.067 - 0.067j$ | $-0.707 + 0.707j$ | $-0.594 + 0.712j$ | 0.113 | $-0.707 + 0.707j$ |
| 7 | $0.688 + 0.012j$ | $0.721 - 0.020j$ | $-0.073 - 0.034j$ | $0.707 - 0.707j$ | $0.813 - 0.743j$ | 0.111 | $0.707 - 0.707j$ |

The plain one-tap equalizer leaves the image: an error of about $0.04$ on the strong subcarriers 1 to 3 and about $0.11$ on the weak subcarriers 5 to 7, whose mirrors are stronger. Lines L3 and L4 return the sent values exactly. The ratios $B[k] / A[-k]^*$ all equal $\nu / \mu^* = -0.0477 - 0.0436j$, the coefficient of the time-domain fix below.

With 64 subcarriers, the same channel and imbalance, and $N_0 = 0.001$ (30 dB), the tests measure over 25 symbols a mean squared error per subcarrier of $8.5 \times 10^{-3}$ for the one-tap equalizer and $2.8 \times 10^{-3}$ with compensation; the rest is noise, including the noise of the estimates from line L2.

## Correctness

**Claim.** (a) The receiver output is $\mu y + \nu y^*$, so after the DFT, $R[k] = A[k] X[k] + B[k] X[-k]^*$ with $A[k] = \mu H[k]$ and $B[k] = \nu H[-k]^*$. (b) With the training of lines L1 and L2, the 2x2 systems are nonsingular and return $A$ and $B$ exactly without noise. (c) The pair system of lines L3 and L4 has the determinant $g \cos\phi\, H[k] H[-k]^*$, so it returns $X[k]$ exactly without noise when $|\phi| < \pi/2$ and both subcarriers of the pair have a nonzero channel. All are theorems in the model above.

**Key invariant.** Conjugation in time is conjugation and mirroring in frequency: the DFT of $y^*$ at $k$ is $Y[-k]^*$. So the imbalance couples only the pairs $(k, -k)$, and each pair is a separate system of two equations.

The determinant follows from $|\mu|^2 - |\nu|^2 = g \cos\phi$. The full proof is below.

## Complexity

Each used subcarrier needs one 2x2 solve in line L2 and one in line L4, $O(1)$ each, so the time is $O(N)$ per symbol after the DFT, and the extra space is $O(N)$ for $A$, $B$ and the output in the [real RAM](/real-ram/).

## Properties

- **Joint with the channel.** $A[k]$ already contains $H[k]$, so the method replaces the channel estimate; it needs two training symbols where an ideal receiver needs one.
- **Image rejection.** Without compensation, the image on a flat channel is $|\nu|^2 / |\mu|^2$ of the signal power, $23.79$ dB below it for $g = 1.1$ and 5 degrees. This limits the SNR of dense constellations such as 64-QAM and 256-QAM.
- **Worse on weak subcarriers.** The image on $k$ scales with $|H[-k]|^2 / |H[k]|^2$, so a subcarrier in a fade whose mirror is strong is hurt most, as in the example.
- **Frequency-flat imbalance.** The model assumes that $g$ and $\phi$ do not depend on frequency. Mismatched filters in the two branches make them frequency dependent; the pair solve still works, because $A[k]$ and $B[k]$ are estimated per subcarrier.
- **DC and the middle.** Subcarriers 0 and $N/2$ are their own mirrors, so their equations cannot separate $X$ from $X^*$; OFDM systems usually leave the DC subcarrier empty anyway.

## Variants and improvements

- **Time-domain fix.** With $c = \nu / \mu^*$, the correction $z = r - c\, r^*$ before the DFT gives $(\mu - |\nu|^2 / \mu^*)\, y$, with no image. The coefficient is the mean of $B[k] / A[-k]^*$, and the ordinary channel estimate then absorbs the scale. This is cheaper per symbol than the pair solve.
- **Blind estimation.** For a proper complex signal, $E[y^2] = 0$, while the imbalance makes $E[r^2] = 2\mu\nu E|y|^2 \ne 0$. Statistics of $r^2$ over many samples give $\nu / \mu^*$ without training, at the cost of a long average.
- **Transmitter imbalance.** A transmitter with IQ imbalance sends $\mu_t x + \nu_t x^*$, which gives the same mirror model; the pair solve handles both together if both are present.
- **With a frequency offset.** A carrier offset makes the image of $k$ fall at $-k$ shifted by twice the offset, so the pair model breaks; joint estimators of the offset and the imbalance exist for this case.
- **Adaptive.** Least mean squares updates of $c$ track slow drift of the analog branches.

## When to use it

Use IQ imbalance compensation in OFDM receivers with direct-conversion front ends, which is most low-cost Wi-Fi and cellular hardware, especially for dense constellations where an image $24$ dB down already costs throughput. Use the pair solve when training for both $A$ and $B$ is available and the imbalance may depend on frequency, and the time-domain fix when the imbalance is flat and the per-symbol cost must be minimal.

## Pitfalls

- **Training that cannot separate the image.** Line L1 needs two training symbols that are not proportional on every pair. If $T_2 = T_1$ everywhere, the matrix of line L1 is singular for every $k$. Changing the sign on half the band, as here, fixes it.
- **The wrong mirror.** Lines L1 and L3 must use $-k$, that is $N - k$ modulo $N$, not $N - 1 - k$. With the off-by-one mirror, the equations pair the wrong subcarriers and the image stays.
- **Forgetting the conjugates.** The second row in line L3 is the equation at $-k$ conjugated, $[B[-k]^*, A[-k]^*]$ against $R[-k]^*$. Without the conjugates, the unknowns do not match the first row.
- **Using the DC or middle subcarrier.** Lines L1 and L3 must skip $k = 0$ and $k = N/2$; there the mirror is the subcarrier itself, and the 2x2 system is singular in general.
- **Estimating the channel separately first.** Dividing by a channel estimate before line L2 mixes the image into the channel estimate; estimate $A$ and $B$ together from the raw values.

## Implementations

## History

IQ imbalance is a classic problem of direct-conversion receivers, which became common in the 1990s because they need no intermediate frequency stage. OFDM made it more visible, because the image falls on another data subcarrier instead of outside the band. Alireza Tarighat, Rahim Bagheri and Ali H. Sayed published compensation schemes for OFDM receivers in 2005, with the model of mirror subcarriers, methods before and after the DFT, and an analysis of their performance. Many later papers treat joint estimation with a frequency offset and frequency-dependent imbalance.

## References
