---
tag: VPF3QG
kind: algorithm
slug: comb-pilot-channel-estimation
name: Comb-type pilot channel estimation
aliases:
- comb pilot interpolation
area: communications/ofdm-and-multicarrier
level: core
summary: "Estimates the OFDM channel by least squares on pilot subcarriers spaced evenly across the band in every symbol, and interpolates it to the data subcarriers along frequency."
solves: [channel-estimation]
model: real-ram
complexity:
  vars: {N: the number of subcarriers}
  time: {worst: O(N)}
  space: {extra: O(N)}
properties: {deterministic: true, keeps_pilots: true, needs_channel_statistics: false, tracks_every_symbol: true}
history:
  year: 2002
  people: [Sinem Coleri, Mustafa Ergen, Anuj Puri, Ahmad Bahai]
  note: "Coleri, Ergen, Puri and Bahai compared block-type and comb-type pilot arrangements for OFDM and the interpolation methods for comb pilots: linear, second order, low-pass, spline and time domain."
prereqs: [orthogonal-frequency-division-multiplexing, least-squares-channel-estimation, pilot-symbol-assisted-modulation, lagrange-interpolation]
see_also: [dft-based-channel-estimation, two-dimensional-wiener-pilot-interpolation, lmmse-channel-estimation, coherence-bandwidth, delay-spread, cubic-spline-interpolation, frequency-domain-equalization, orthogonal-frequency-division-multiple-access]
sources:
  - paper: doi:10.1109/TBC.2002.804034
    title: "S. Coleri, M. Ergen, A. Puri and A. Bahai, Channel estimation techniques based on pilot arrangement in OFDM systems, IEEE Transactions on Broadcasting 48(3), 2002"
    locator: "pages 223 to 229 (block-type and comb-type pilot arrangements, least squares at the pilots, and the comparison of interpolation methods)"
  - paper: doi:10.1109/VETEC.1995.504981
    title: "J.-J. van de Beek, O. Edfors, M. Sandell, S. K. Wilson and P. O. Börjesson, On channel estimation in OFDM systems, IEEE 45th Vehicular Technology Conference, 1995"
    locator: "pages 815 to 819 (least squares and linear minimum mean squared error estimates, and the estimate through the DFT)"
  - paper: doi:10.1109/ICASSP.1997.598897
    title: "P. Hoeher, S. Kaiser and P. Robertson, Two-dimensional pilot-symbol-aided channel estimation by Wiener filtering, IEEE ICASSP, 1997"
    locator: "volume 3, pages 1845 to 1848 (pilots spread in time and frequency, and their interpolation by two-dimensional Wiener filters)"
---

Comb-type pilot channel estimation is the simplest way for an [OFDM](/orthogonal-frequency-division-multiplexing/) receiver to learn the channel gain $H[k]$ of every subcarrier in every symbol. The transmitter puts known pilot values on the subcarriers $k_0, k_0 + D, k_0 + 2D, \ldots$, a comb with spacing $D$, and data on the others. After the DFT, the receiver has $Y[k] = H[k] X[k] + W[k]$. At each pilot it takes the [least squares](/least-squares-channel-estimation/) estimate $Y[p] / X[p]$, and between pilots it interpolates along frequency, here linearly or with a quadratic through three pilots. The channel response $H[k]$ is the DFT of the taps, so it has period $N$ in $k$ and the interpolation wraps around from the last pilot to the first. The estimate is good when the channel changes slowly across the band, that is, when its delay spread is short compared with the symbol: for a channel of $L$ taps, the comb needs $D \le N / L$. Because every symbol carries pilots, the estimate follows a channel that changes from symbol to symbol. The page uses $j$ for the imaginary unit and $H[k] = \sum_l h_l e^{-j 2\pi l k / N}$.

## In plain words

The receiver needs to know how much the channel boosts and turns each subcarrier, so that it can undo it. The sender reserves every fourth subcarrier, say, for a value the receiver already knows. On those, the receiver divides what it got by what was sent, which gives the channel there. For the subcarriers in between, it guesses by drawing a straight line between the two nearest known points. This works well when the channel changes smoothly from one subcarrier to the next, which is the case when the echoes in the channel are short. Long echoes make the channel change quickly across the band, and then the pilots must be closer together.

## The problem

The input is one OFDM symbol after the DFT, $Y[0], \ldots, Y[N-1]$, the known pilot values $X[p]$ on the comb $p = k_0 + iD$, $i = 0, \ldots, N/D - 1$, with $D$ dividing $N$, and the order of interpolation. The model is $Y[k] = H[k] X[k] + W[k]$ with an unknown channel of $L$ taps and white noise $W[k] \sim \mathcal{CN}(0, N_0)$. Output an estimate $\hat H[k]$ for all $N$ subcarriers.

## The algorithm

```pseudo id=main
COMB-PILOT(Y, X_p, D, k0)
L1  Ĥ_p[i] ← Y[k0 + iD] / X_p[i]  for i = 0, .., P-1, with P = N / D
L2  for k ← 0, .., N-1: (i, rem) ← divmod((k - k0) mod N, D)
L3      t ← rem / D
L4      a ← Ĥ_p[i];  b ← Ĥ_p[(i + 1) mod P]
L5      Ĥ[k] ← (1 - t) a + t b
L6  return Ĥ
```

Line L1 is the least squares estimate at each pilot. Line L2 finds the last pilot at or before $k$ on the circle of subcarriers and the distance to it; line L3 turns the distance into a fraction. Line L4 takes that pilot and the next one, wrapping from the last pilot to the first. Line L5 interpolates linearly. The quadratic option of the implementation replaces line L5 by the Lagrange polynomial through the pilots at $t = -1, 0, 1$, with weights $t(t-1)/2$, $(1-t)(1+t)$ and $t(t+1)/2$.

## Example

Take $N = 16$, $D = 4$, $k_0 = 0$, the channel $h = (1, 0.5)$, all pilot values 1 and no noise, so the pilots on $k = 0, 4, 8, 12$ see $H[k] = 1 + 0.5 e^{-j 2\pi k / 16}$ exactly.

| $k$ | $H[k]$ | linear $\hat H[k]$ | linear error | quadratic $\hat H[k]$ | quadratic error |
|---|---|---|---|---|---|
| 0 | $1.500$ | $1.500$ | 0 | $1.500$ | 0 |
| 1 | $1.462 - 0.191j$ | $1.375 - 0.125j$ | 0.109 | $1.469 - 0.125j$ | 0.067 |
| 2 | $1.354 - 0.354j$ | $1.250 - 0.250j$ | 0.146 | $1.375 - 0.250j$ | 0.106 |
| 3 | $1.191 - 0.462j$ | $1.125 - 0.375j$ | 0.109 | $1.219 - 0.375j$ | 0.091 |
| 4 | $1.000 - 0.500j$ | $1.000 - 0.500j$ | 0 | $1.000 - 0.500j$ | 0 |
| 5 | $0.809 - 0.462j$ | $0.875 - 0.375j$ | 0.109 | $0.875 - 0.469j$ | 0.067 |
| 6 | $0.646 - 0.354j$ | $0.750 - 0.250j$ | 0.146 | $0.750 - 0.375j$ | 0.106 |
| 7 | $0.538 - 0.191j$ | $0.625 - 0.125j$ | 0.109 | $0.625 - 0.219j$ | 0.091 |
| 8 | $0.500$ | $0.500$ | 0 | $0.500$ | 0 |

The pilots are kept exactly. The largest linear error is $0.146$, in the middle between pilots, and the bound of the claim below is $\frac{\pi^2 \cdot 16}{2 \cdot 256} \cdot 0.5 = 0.154$. The quadratic estimate is closer on this smooth channel. With $D = 4$ and $N = 16$, there are 4 pilots for a channel of 2 taps, so the comb is dense enough, but only just for a linear interpolator.

Measured on $N = 64$ with three random taps of powers $0.5$, $0.3$, $0.2$ and no noise, the mean squared error of the interpolation is about $3.2 \times 10^{-5}$ (linear) and $1.1 \times 10^{-6}$ (quadratic) for $D = 2$, $6.5 \times 10^{-4}$ and $9.2 \times 10^{-5}$ for $D = 4$, and $1.08 \times 10^{-2}$ and $5.3 \times 10^{-3}$ for $D = 8$.

## Correctness

**Claim.** (a) The estimate equals the least squares estimate on every pilot. (b) Without noise, $|\hat H[k] - H[k]| \le \frac{D^2}{8} \max_f |H''(f)| \le \frac{\pi^2 D^2}{2 N^2} \sum_l l^2 |h_l|$ for every $k$, where $H(f)$ is the channel response at a real frequency index $f$. (c) On a flat channel with unit-modulus pilots, the noise in the linear estimate has the mean variance $0.6875\, N_0$ over the band for $D = 4$. All three are theorems in the model above.

**Key invariant.** $H(f) = \sum_l h_l e^{-j 2\pi l f / N}$ is smooth and has period $N$, so the pilot after the last one is the first pilot moved by $N$, with the same value. Lines L2 to L5 therefore interpolate one smooth periodic function at equally spaced points, with no edge at the ends of the band.

Part (b) is the error of linear interpolation in the Peano kernel form, which holds for complex functions, together with $|H''(f)| \le (2\pi/N)^2 \sum_l l^2 |h_l|$. Part (c) is the variance of $(1 - t) W_a + t W_b$. The full proof is below.

## Complexity

Line L1 is $P = N / D$ divisions and lines L2 to L5 cost $O(1)$ per subcarrier, so the time is $O(N)$ and the extra space is $O(N)$ for the output in the [real RAM](/real-ram/). The receiver needs no channel statistics and no matrix.

## Properties

- **Pilot overhead.** One subcarrier in $D$ carries no data, a rate loss of $1/D$ in every symbol.
- **Spacing rule.** $H[k]$ is a sum of $L$ complex exponentials in $k$, so $P \ge L$ equally spaced samples determine it, which is the condition $D \le N / L$. Interpolation by low-degree polynomials needs a denser comb than this limit to keep the bias small.
- **Bias and noise.** The bias grows as $D^2$ for linear interpolation (Claim (b)). The noise is never amplified above $N_0$: linear weights are in $[0, 1]$ and sum to 1, so the noise factor is between $1/2$ and $1$, and $0.6875$ on average for $D = 4$. The quadratic option has less bias and a larger noise factor, $0.81543$ for $D = 4$.
- **Tracking.** Each symbol is estimated on its own, so the estimate follows fast fading in time, unlike block-type pilots, which send a full pilot symbol now and then.
- **Model-free.** It needs no knowledge of the delay profile or the SNR, unlike [LMMSE estimation](/lmmse-channel-estimation/).

## Variants and improvements

- **Higher-order interpolation.** Coleri and coauthors compared linear, second order, low-pass and spline interpolation for comb pilots; smoother interpolators have less bias on channels with longer delays.
- **Through the DFT.** Taking the inverse DFT of the pilot estimates, keeping the first $L$ taps and transforming back is exact for $P \ge L$ without noise and removes most of the noise; see [DFT-based channel estimation](/dft-based-channel-estimation/).
- **LMMSE across frequency.** A Wiener filter with the frequency correlation of the channel gives the smallest mean squared error when the statistics are known.
- **Scattered pilots in two dimensions.** Pilots spread over both time and frequency, as in DVB-T and LTE, need fewer pilots per symbol; [two-dimensional Wiener interpolation](/two-dimensional-wiener-pilot-interpolation/) is the optimal filter for that layout.
- **Block-type pilots.** All subcarriers carry pilots in some symbols, which suits slow channels with long delays.

## When to use it

Use comb pilots with linear interpolation when the receiver must be simple, the channel changes from symbol to symbol, and the delay spread is short compared with $N / D$ samples. Use a smoother interpolator or the DFT-based estimate for longer delays, and the Wiener or LMMSE estimates when the delay profile and the SNR are known and the cost of a matrix is acceptable.

## Pitfalls

- **No wrap at the band edge.** Line L4 must take the next pilot as index $(i + 1) \bmod P$. Without the wrap, the subcarriers after the last pilot have no right neighbor, and holding the last value gives a large error there.
- **Spacing too large.** Line L1 samples $H$ every $D$ subcarriers. If $D > N / L$, the comb aliases the channel, and no interpolation in line L5 can recover it.
- **The wrong offset.** Line L2 must subtract the comb offset $k_0$ before the division. Without it, $t$ is wrong for every subcarrier when $k_0 \ne 0$.
- **Dividing by the wrong pilot.** Line L1 must divide by the known value on the same subcarrier, $X_p[i]$ for $p = k_0 + iD$, not by the first pilot value or by the received pilot.
- **Null subcarriers.** Real systems leave the DC and edge subcarriers empty, so the comb is not periodic over $N$. Line L4 then wraps across a gap, and the estimate near the edges needs extrapolation instead.

## Implementations

## History

Pilot-symbol-assisted modulation for fading channels was analyzed for single-carrier systems before OFDM receivers used it. For OFDM, van de Beek, Edfors, Sandell, Wilson and Börjesson studied least squares and LMMSE estimates in 1995, Hoeher, Kaiser and Robertson in 1997 treated pilots spread in time and frequency with two-dimensional Wiener filters, and Coleri, Ergen, Puri and Bahai in 2002 gave a widely cited comparison of block-type and comb-type arrangements and of the interpolators for comb pilots. Comb and scattered pilots with simple interpolation are the usual design in DVB-T, LTE and 5G NR receivers.

## References
