---
tag: B8R7HN
kind: algorithm
slug: channel-shortening-equalizer
name: Channel shortening equalizer
aliases:
- time-domain equalizer for DMT
- TEQ
area: communications/channel-estimation-and-equalization
level: advanced
summary: A filter that compresses the channel impulse response to fit within the cyclic prefix of a multicarrier system.
solves: [channel-equalization]
model: real-ram
complexity:
  vars: {L: the number of channel taps, m: the number of filter taps (L_w on the page), K: the number of iterations}
  time: {worst: O(L m^2 + K m^3)}
  space: {extra: O(m^2)}
properties: {deterministic: true, linear: true, needs_channel: true, optimal: "for the shortening SNR at a fixed delay"}
history:
  year: 1973
  people: [David D. Falconer, F. R. Magee]
  note: "Falconer and Magee put a prefilter in front of a Viterbi detector to cut the channel memory. Melsa, Younce and Rohrs gave the MSSNR design for DMT in 1996."
prereqs: [discrete-multitone, cyclic-prefix, generalized-eigenvalue-problem]
see_also: [inverse-iteration, rayleigh-quotient, power-iteration, cholesky-decomposition, frequency-domain-equalization, orthogonal-frequency-division-multiplexing, reduced-state-sequence-estimation, viterbi-equalizer]
sources:
  - paper: "D. D. Falconer and F. R. Magee, Adaptive channel memory truncation for maximum likelihood sequence estimation, Bell System Technical Journal 52(9), 1973, pages 1541 to 1562"
    locator: "a prefilter and a short desired impulse response chosen for the minimum mean squared error, in front of a Viterbi detector"
  - paper: "Peter J. W. Melsa, Richard C. Younce and Charles E. Rohrs, Impulse response shortening for discrete multitone transceivers, IEEE Transactions on Communications 44(12), 1996, pages 1662 to 1672"
    locator: "the maximum shortening SNR design as a generalized eigenvalue problem"
  - paper: "Naofal Al-Dhahir and John M. Cioffi, Optimum finite-length equalization for multicarrier transceivers, IEEE Transactions on Communications 44(1), 1996, pages 56 to 64"
    locator: "finite-length TEQ designs for multicarrier receivers, including the design that maximizes the geometric SNR"
---

A channel shortening equalizer, or time-domain equalizer (TEQ), is a short FIR filter $w$ that the receiver of a multicarrier system puts in front of the DFT. The [cyclic prefix](/cyclic-prefix/) of $\nu$ samples makes the channel act per subcarrier only when the channel has at most $\nu + 1$ taps. Telephone lines in [DMT](/discrete-multitone/) are much longer than any prefix the system can pay for. The TEQ makes the effective channel $c = h * w$ put almost all of its energy into a window of $\nu + 1$ consecutive taps. The maximum shortening SNR (MSSNR) design maximizes the energy inside the window over the energy outside it, the wall. This ratio is a generalized Rayleigh quotient, so the best filter is a generalized eigenvector, which inverse iteration finds.

## In plain words

A long echo makes each received block leak into the next. The prefix absorbs only a short echo. The TEQ is a filter that cancels most of the echo tail, so that what is left fits in the prefix. It does not try to make the channel flat, as a usual equalizer does. It only makes the channel short, and the per-bin equalizer after the DFT handles the rest. Because only the shape of the channel matters, the design is the filter that puts the largest share of the channel energy inside the window.

## The problem

The input is a real channel $h_0, \ldots, h_{L-1}$, the filter length $L_w$, the prefix length $\nu$ and a delay $d$. With the convolution matrix $\mathbf{H}$ of $L + L_w - 1$ rows, $\mathbf{H}_{kj} = h_{k-j}$, the effective channel is $c = \mathbf{H} w$. The window is the set of indices $d, \ldots, d + \nu$. Let $\mathbf{B}$ be the sum of $\mathbf{h}_k \mathbf{h}_k^T$ over the rows $\mathbf{h}_k$ of $\mathbf{H}$ inside the window, and $\mathbf{A}$ the same sum over the rows outside it. The output is the filter that maximizes the shortening SNR
$$S(w) = \frac{\sum_{k=d}^{d+\nu} c_k^2}{\sum_{k \text{ outside}} c_k^2} = \frac{w^T \mathbf{B} w}{w^T \mathbf{A} w},$$
and the value of that maximum. The delay is a design parameter. The usual practice is to try every delay.

## The algorithm

```pseudo id=main
MSSNR-TEQ(h, Lw, ν, d)
L1  A, B ← wall and window matrices of h for the delay d
L2  w ← (1, 1, ..., 1)
L3  repeat until μ stops changing
L4      solve A v = B w
L5      w ← v / sqrt(vᵀ B v)                    ▷ now wᵀ B w = 1
L6      μ ← wᵀ A w                              ▷ the wall energy
L7  return w, 1/μ                               ▷ the filter and its SNR
```

Line L1 builds the two $L_w \times L_w$ matrices from the rows of the convolution matrix. Lines L4 and L5 are [inverse iteration](/inverse-iteration/) for the pencil $\mathbf{A} - \mu \mathbf{B}$ with the shift 0, which is the [power iteration](/power-iteration/) on $\mathbf{A}^{-1}\mathbf{B}$. It converges to the [generalized eigenvector](/generalized-eigenvalue-problem/) with the smallest $\mu$ in $\mathbf{A} w = \mu \mathbf{B} w$. Line L5 keeps the window energy at 1, so the wall energy in line L6 is $1/S(w)$. The code then takes up to 3 [Rayleigh quotient](/rayleigh-quotient/) steps, with the shift $\mu$, and keeps a step only if it does not increase $\mu$.

## Example

Take $h = (1, 0.5)$, $L_w = 2$, $\nu = 0$ and $d = 0$, so the window is the single tap $c_0$. The rows of $\mathbf{H}$ are $(1, 0)$, $(0.5, 1)$ and $(0, 0.5)$, so
$$\mathbf{B} = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}, \qquad \mathbf{A} = \begin{pmatrix} 0.25 & 0.5 \\ 0.5 & 1.25 \end{pmatrix}.$$
With $w_0 = 1$ the wall energy is $0.25 + w_1 + 1.25 w_1^2$, which is smallest at $w_1 = -0.4$, with the value $0.05$. So $w = (1, -0.4)$, $c = (1, 0.1, -0.2)$, and $S = 1/0.05 = 20$, or 13.01 dB. Without the TEQ, the window holds $c_0 = 1$ and the wall holds $0.5^2$, so $S = 4$, or 6.02 dB. The delays $d = 1$ and $d = 2$ give only 4.25 and 0.3125, so $d = 0$ is the best delay.

A longer case: $h_k = 0.8^k$ for $k = 0, \ldots, 7$, with $\nu = 2$ and $L_w = 4$. The best window of 3 taps of $h$ holds 4.99 dB more energy than the wall. The MSSNR filter at the best delay $d = 0$ is $w \approx (0.6985, 0, 0, -0.3285)$, and it gives 15.87 dB. The filter is close to $1 - 0.8^3 z^{-3}$ times a constant, which cancels the geometric tail of $h$ after 3 taps: the effective channel is $(0.6985, 0.5588, 0.4470)$ in the window and at most 0.108 in magnitude outside it.

## Correctness

**Claim.** If $\mathbf{A}$ is positive definite and the largest generalized eigenvalue $\lambda_1$ of $\mathbf{B} w = \lambda \mathbf{A} w$ is simple, the iteration converges to the filter $w$ that maximizes $S(w)$ for the delay $d$, and $1/\mu = S(w) = \lambda_1$.

**Key step.** With the [Cholesky factorization](/cholesky-decomposition/) $\mathbf{A} = \mathbf{R}\mathbf{R}^T$ and $u = \mathbf{R}^T w$, the ratio $S(w)$ is the ordinary Rayleigh quotient of the symmetric matrix $\mathbf{R}^{-1} \mathbf{B} \mathbf{R}^{-T}$, whose maximum is its largest eigenvalue. The matrix $\mathbf{A}^{-1}\mathbf{B}$ is similar to it, so the power method on $\mathbf{A}^{-1}\mathbf{B}$ converges to the right vector, with the error ratio $\lambda_2/\lambda_1$ per step. The proofs folder has the details.

## Complexity

In the [real RAM](/real-ram/), line L1 costs $O((L + L_w) L_w^2)$, and each step of the loop solves an $L_w \times L_w$ system in $O(L_w^3)$. With $K$ steps, one delay costs $O(L L_w^2 + K L_w^3)$, with $O(L_w^2)$ extra space. If $\mathbf{A}$ is factored once, each step costs only $O(L_w^2)$. The number of steps depends on the gap $\lambda_2/\lambda_1$. The search over all delays repeats this $L + L_w - 1 - \nu$ times. This is design work, done once per channel estimate. In operation, the TEQ costs $L_w$ multiplications per sample.

## Properties

- **Optimal for its criterion.** For a fixed delay, no filter of $L_w$ taps has a larger shortening SNR. In the tests, 2000 random filters for each of 5 random channels (seed 7903) never beat it.
- **Scale free.** $S(w)$ does not change when $w$ is scaled, so the gain of the filter is free. The per-bin equalizer after the DFT absorbs it.
- **Shape, not flatness.** The TEQ does not equalize the window taps. The effective channel inside the window can have any shape, and the frequency-domain equalizer inverts it.
- **Noise is ignored.** MSSNR looks only at the channel. It can put deep nulls in the frequency response of $w$ and so lower the SNR in some bins.
- **Linear and real.** The filter is real for a real baseband channel, as in DMT.

## Variants and improvements

- **MMSE target impulse response.** Choose $w$ and a target $b$ of $\nu + 1$ taps to minimize $E(w * r - b * x)^2$ with a norm constraint on $b$. Falconer and Magee used this form in 1973 to cut the channel memory in front of a Viterbi detector, and it is the MMSE TEQ of DMT.
- **Bit rate designs.** Al-Dhahir and Cioffi gave finite-length designs for multicarrier receivers, including one that maximizes the geometric mean of the bin SNRs, a proxy for the bit rate. Later designs maximize the bit rate directly.
- **Shortening for MLSE.** The same filter can shorten a channel for a [Viterbi equalizer](/viterbi-equalizer/), so that the trellis has $M^{\nu}$ states instead of $M^{L-1}$. [Reduced-state sequence estimation](/reduced-state-sequence-estimation/) is the alternative that keeps the full channel and cuts the trellis.
- **Blind and adaptive TEQs.** The filter can be adapted from the received data without a training sequence, by using the redundancy of the prefix.
- **Per-tone equalization.** Move the TEQ into the frequency domain, with a few taps per subcarrier, so that each bin gets its own optimal filter.

## When to use it

Use a TEQ in a DMT or [OFDM](/orthogonal-frequency-division-multiplexing/) receiver when the channel is longer than the prefix and a longer prefix would cost too much throughput, as on ADSL lines. If the prefix already covers the channel, the TEQ is not needed. For single-carrier blocks with a prefix, use [frequency-domain equalization](/frequency-domain-equalization/), which needs the same condition $L - 1 \le \nu$.

## Pitfalls

- **The delay matters.** The best delay can change the shortening SNR by many dB. In the first example, the three delays give 13.01 dB, 6.28 dB and below 0 dB. Search over all delays.
- **A singular wall matrix.** If $L_w$ is large enough to zero the wall exactly, $\mathbf{A}$ is singular and the shortening SNR is infinite. The solve in line L4 fails. Use a shorter filter, or solve for the null space of $\mathbf{A}$.
- **A singular window matrix.** $\mathbf{B}$ has rank at most $\nu + 1$, so it is singular when $L_w > \nu + 1$. Methods that factor $\mathbf{B}$ fail then. The iteration here factors only $\mathbf{A}$.
- **Shortening SNR is not bit rate.** A filter with a high shortening SNR can still have deep spectral nulls that ruin some bins. Check the bin SNRs after the design.
- **A bad start vector.** The power method needs a start with a component along the best eigenvector. The all-ones start can fail for special channels. Restart with another vector if $\mathbf{B} w = 0$.

## Implementations

## History

In 1973, Falconer and Magee proposed a prefilter in front of a Viterbi detector, adapted so that the channel seen by the detector has a short desired impulse response, to make maximum likelihood sequence estimation practical on long channels. When DMT was developed for digital subscriber lines, the same idea was used to fit the channel into the cyclic prefix. In 1996, Melsa, Younce and Rohrs gave the maximum shortening SNR design as a generalized eigenvalue problem, and Al-Dhahir and Cioffi gave optimum finite-length designs for multicarrier transceivers.

## References
