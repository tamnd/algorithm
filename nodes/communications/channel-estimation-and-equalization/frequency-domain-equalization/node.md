---
tag: 8TF7E6
kind: algorithm
slug: frequency-domain-equalization
name: Single-carrier frequency-domain equalization
aliases:
- SC-FDE
- frequency-domain equalizer
area: communications/channel-estimation-and-equalization
level: core
summary: Equalizes a block of single-carrier symbols with a cyclic prefix by one complex tap per FFT bin.
solves: [channel-equalization]
model: real-ram
complexity:
  vars: {N: the block length, L: the number of channel taps, P: the prefix length}
  time: {worst: O(N log N)}
  space: {extra: O(N)}
properties: {deterministic: true, linear: true, needs_channel: true, needs_cyclic_prefix: true, biased: "the MMSE form, by the factor 1 - J/Es"}
history:
  year: 1995
  people: [Hikmet Sari, Georges Karam, Isabelle Jeanclaude]
  note: "Sari, Karam and Jeanclaude compared OFDM with single-carrier transmission equalized in the frequency domain and showed that the two receivers have about the same complexity. Falconer and coauthors made SC-FDE a standard option for broadband wireless in 2002."
prereqs: [cyclic-prefix, mmse-linear-equalizer, fast-fourier-transform]
see_also: [sc-fdma, orthogonal-frequency-division-multiplexing, zero-forcing-equalizer, decision-feedback-equalizer, channel-shortening-equalizer, circular-convolution, discrete-fourier-transform, turbo-equalization]
sources:
  - paper: "David Falconer, Sirikiat Lek Ariyavisitakul, Anader Benyamin-Seeyar and Brian Eidson, Frequency domain equalization for single-carrier broadband wireless systems, IEEE Communications Magazine 40(4), 2002, pages 58 to 66"
    locator: "the block structure with the cyclic prefix, the ZF and MMSE taps per bin, and the comparison with OFDM"
  - paper: "Hikmet Sari, Georges Karam and Isabelle Jeanclaude, Transmission techniques for digital terrestrial TV broadcasting, IEEE Communications Magazine 33(2), 1995, pages 100 to 109"
    locator: "single-carrier transmission with frequency-domain equalization against OFDM"
---

Single-carrier frequency-domain equalization (SC-FDE) equalizes a long channel with one complex multiplication per frequency bin. The transmitter sends the symbols in blocks of $N$ and puts a [cyclic prefix](/cyclic-prefix/) of $P \ge L - 1$ samples in front of each block. After the receiver removes the prefix, the channel acts on the block as a [circular convolution](/circular-convolution/), so the [DFT](/discrete-fourier-transform/) of the block is the DFT of the symbols times the channel frequency response, bin by bin. The receiver divides by the response (zero forcing) or applies the MMSE weight in each bin and returns to the time domain with an inverse DFT. The decisions are made in the time domain, on the symbols themselves. This is the same block structure as [OFDM](/orthogonal-frequency-division-multiplexing/), with the inverse DFT moved from the transmitter to the receiver. [SC-FDMA](/sc-fdma/) uses the same receiver for multiple users.

## In plain words

A time-domain equalizer for a long channel needs a long filter, and every output costs one multiplication per filter tap. In the frequency domain, a channel is only a gain and a phase per frequency, so undoing it is one division per frequency. The catch is that this is exact only for circular convolution, where the block wraps around. The cyclic prefix makes the channel wrap around: it repeats the end of the block at the front, so the echo of the previous block falls only on the prefix, and the receiver throws the prefix away. The fast Fourier transform makes the change of domain cheap.

## The problem

The input is a received block of $N + P$ samples $r_i = \sum_{l=0}^{L-1} h_l s_{i-l} + w_i$, where $s$ is the prefix followed by the block $x = (x_0, \ldots, x_{N-1})$, the channel $h$ is known, $P \ge L - 1$, and $w$ is white $\mathcal{CN}(0, N_0)$. The symbols are independent with energy $E_s$. The output is an estimate $\hat x$ of the block: the zero-forcing estimate, which removes all ISI, or the linear MMSE estimate, which minimizes $E|\hat x_n - x_n|^2$ among all linear functions of the received block.

## The algorithm

The DFT is unnormalized, $X_k = \sum_n x_n e^{-j2\pi kn/N}$, and the inverse DFT has the factor $1/N$.

```pseudo id=main
SC-FDE(r, h, N, P, N0, Es)
L1  y ← r[P .. P+N-1]                          ▷ remove the cyclic prefix
L2  Y ← FFT(y)
L3  H ← FFT(h padded with zeros to N)           ▷ once per channel
L4  W[k] ← 1 / H[k]                             ▷ zero forcing
L5  or W[k] ← conj(H[k]) / (|H[k]|² + N0/Es)     ▷ MMSE
L6  return IFFT(W[k] Y[k])
```

Line L1 is where the prefix matters: when $P \ge L - 1$, the samples that line L1 keeps contain no sample of the previous block, and $y$ is the circular convolution of $h$ and $x$. Line L2 turns it into $Y_k = H_k X_k + W_k$. Lines L4 and L5 are the one-tap equalizers. The MMSE taps are the [Wiener filter](/wiener-filter/) of each bin, and together they give exactly the block MMSE estimate. Line L6 returns to the symbols. The [fast Fourier transform](/fast-fourier-transform/) does lines L2, L3 and L6.

## Example

Take $N = 4$, $h = (1, 0.5)$, $P = 1$ and the BPSK block $x = (+1, -1, -1, +1)$. The transmitted samples are $(+1 \mid +1, -1, -1, +1)$, with the last symbol copied in front. After the prefix is removed and without noise, $y = (x_0 + 0.5x_3, x_1 + 0.5x_0, x_2 + 0.5x_1, x_3 + 0.5x_2) = (1.5, -0.5, -1.5, 0.5)$, a circular convolution. In the frequency domain:

| $k$ | $X_k$ | $H_k$ | $Y_k$ | $Y_k/H_k$ | $\lvert H_k\rvert^2$ | MMSE tap, $N_0 = 0.1$ |
|---|---|---|---|---|---|---|
| 0 | 0 | 1.5 | 0 | 0 | 2.25 | 0.6383 |
| 1 | $2 + 2j$ | $1 - 0.5j$ | $3 + j$ | $2 + 2j$ | 1.25 | $(1 + 0.5j)/1.35$ |
| 2 | 0 | 0.5 | 0 | 0 | 0.25 | 1.4286 |
| 3 | $2 - 2j$ | $1 + 0.5j$ | $3 - j$ | $2 - 2j$ | 1.25 | $(1 - 0.5j)/1.35$ |

The ZF output is the inverse DFT of $Y_k/H_k$, which is $x$ exactly. With $N_0 = 0.1$ and $E_s = 1$, the noise after ZF has the variance $\frac{N_0}{N}\sum_k |H_k|^{-2} = 0.1511$ per symbol, most of it from bin 2, where ZF multiplies by 2. The MMSE taps hold back in that bin, and the MSE is $J = \frac1N \sum_k N_0 E_s/(E_s|H_k|^2 + N_0) = 0.1191$. The MMSE output is biased: without noise it is $0.926\, x$ for this block, because both used bins have $|H_k|^2/(|H_k|^2 + 0.1) = 1.25/1.35$.

On the channel B of Proakis, $h = (0.407, 0.815, 0.407)$, with $N = 64$, $E_s/N_0 = 10$ dB and QPSK, the bin $k = 32$ has $H_{32} = 0.407 - 0.815 + 0.407 = -0.001$. ZF multiplies the noise in that bin by $10^6$, and the noise variance per symbol is 1707. The MMSE formula gives $J = 0.3364$, and 200 blocks with seed 7805 measured 0.3329. The unbiased SINR is $E_s/J - 1$, which is 2.95 dB.

## Correctness

**Claim.** With $P \ge L - 1$, the ZF output is $x$ plus noise of the variance $\frac{N_0}{N}\sum_k |H_k|^{-2}$ per symbol, and the MMSE output equals the block linear MMSE estimate $(\mathbf{C}^H\mathbf{C} + \frac{N_0}{E_s}\mathbf{I})^{-1}\mathbf{C}^H y$ for the circulant channel matrix $\mathbf{C}$. Its MSE is $J = \frac1N \sum_k N_0 E_s/(E_s|H_k|^2 + N_0)$ for every symbol, and its unbiased SINR is $E_s/J - 1$.

**Key step.** The prefix makes the channel matrix circulant, and the DFT diagonalizes every circulant matrix, with the eigenvalues $H_k$. So the matrix inverse in the MMSE formula becomes $N$ scalar divisions. The error covariance is circulant too, so all symbols have the same MSE, the average of the per-bin errors. The proofs folder has the details.

## Complexity

The FFT and the inverse FFT cost $O(N \log N)$ each for $N$ a power of 2, and the taps cost $O(N)$, so a block costs $O(N \log N)$ in the [real RAM](/real-ram/), or $O(\log N)$ per symbol, with $O(N)$ extra space. The channel FFT is computed once per channel estimate. A time-domain equalizer with $L_f$ taps costs $O(N L_f)$ per block, and $L_f$ must grow with the channel length $L$, so SC-FDE wins for long channels. The prefix costs a fraction $P/(N+P)$ of the throughput, which is why $N$ is chosen much larger than $L$.

## Properties

- **Exact block equalizers.** The ZF and MMSE outputs are the exact block ZF and block MMSE estimates for the circular channel, not approximations of a finite filter.
- **Same MSE for every symbol.** The error covariance is circulant, so no symbol of the block is worse off. A time-domain block equalizer without a prefix has worse errors at the block edges.
- **Averaging over frequency.** The MSE is an average over the bins of $N_0 E_s/(E_s|H_k|^2 + N_0)$. A deep fade in one bin raises the MSE of all symbols a little, instead of destroying the subcarriers in that bin, as in uncoded OFDM.
- **Biased MMSE.** The MMSE output is $g x + v$ with $g = 1 - J/E_s$. Scale by $1/g$ before a slicer for QAM.
- **Single-carrier envelope.** The transmitter sends the symbols directly, so the peak-to-average power ratio is that of the constellation and the pulse, lower than for OFDM.
- **Linear.** It is a linear equalizer and inherits the loss of linear equalizers on channels with deep nulls.

## Variants and improvements

- **Frequency-domain DFE.** A frequency-domain feedforward filter followed by a short time-domain feedback filter, which recovers much of the loss on channels with deep nulls. See the [decision feedback equalizer](/decision-feedback-equalizer/).
- **Iterative block DFE and turbo FDE.** Repeat the FDE with soft decisions from a decoder to cancel the residual ISI, as in [turbo equalization](/turbo-equalization/) and the [soft interference cancellation equalizer](/soft-interference-cancellation-equalizer/).
- **SC-FDMA.** Each user spreads its block with a DFT and maps it to some of the subcarriers of a larger IFFT. The receiver equalizes per bin and despreads with an inverse DFT. See [SC-FDMA](/sc-fdma/).
- **Unique word.** A known sequence in place of the cyclic prefix, at the end of every block, also makes the convolution circular and can serve as a pilot.
- **Overlap methods without a prefix.** The overlap-save method equalizes a continuous stream in the frequency domain with no prefix, at the cost of discarded overlap samples at the receiver.
- **Channel estimation.** With a known block or pilot bins, $H_k$ is estimated per bin by least squares, then smoothed by limiting the impulse response to $P + 1$ taps. See [least-squares channel estimation](/least-squares-channel-estimation/).

## When to use it

Use SC-FDE for long channels and high symbol rates, when the transmitter must keep a low peak-to-average power ratio: broadband wireless uplinks, satellite links and mobile terminals. Use [OFDM](/orthogonal-frequency-division-multiplexing/) when the transmitter can adapt the rate per subcarrier, and a [Viterbi equalizer](/viterbi-equalizer/) or a time-domain [DFE](/decision-feedback-equalizer/) when the channel is short and no prefix is in the frame format.

## Pitfalls

- **A prefix shorter than the channel.** If $P < L - 1$, the previous block leaks into the kept samples and the convolution is not circular. The error does not go away at high SNR. A [channel shortening equalizer](/channel-shortening-equalizer/) can shorten the channel first.
- **ZF near a null.** Dividing by a small $H_k$ blows up the noise in that bin and spreads it over every symbol. On the channel B of Proakis with $N = 64$, ZF gives a noise variance of 1707 per symbol. Use the MMSE taps.
- **Forgetting the bias.** The MMSE output is scaled by $g < 1$. For QAM with several amplitude levels, scale by $1/g$ before deciding.
- **The DFT scaling.** With the unnormalized DFT, the noise per bin has variance $N N_0$, and the inverse DFT carries the factor $1/N$. Mixing conventions gives the wrong $N_0$ in the MMSE taps.
- **Timing.** The kept window must start at the first sample of the block. A window that starts $d$ samples early still sees a circular convolution if $P \ge L - 1 + d$, but with the channel shifted circularly by $d$ samples, so the channel estimate must come from the same window. A window that starts late takes in the next block.

## Implementations

## History

In 1995, Sari, Karam and Jeanclaude compared OFDM with single-carrier transmission equalized in the frequency domain for digital terrestrial television, and showed that the two receivers have about the same complexity when both use the FFT. In 2002, Falconer, Ariyavisitakul, Benyamin-Seeyar and Eidson described SC-FDE for broadband wireless, with the cyclic prefix, the ZF and MMSE taps, the decision feedback variants and the comparison with OFDM. SC-FDMA, the uplink of LTE, uses the same receiver.

## References
