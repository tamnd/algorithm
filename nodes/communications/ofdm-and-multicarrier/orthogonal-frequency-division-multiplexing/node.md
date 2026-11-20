---
tag: 2QCF2N
kind: algorithm
slug: orthogonal-frequency-division-multiplexing
name: Orthogonal frequency-division multiplexing
aliases:
- OFDM
area: communications/ofdm-and-multicarrier
level: intro
summary: "Builds a multicarrier symbol with an inverse FFT and a cyclic prefix, and demodulates it with an FFT and one tap per subcarrier. A prefix of at least L - 1 samples makes each subcarrier flat."
solves: [channel-equalization]
model: real-ram
complexity:
  vars: {N: the number of subcarriers, L: the number of channel taps}
  time: {worst: O(N log N)}
  space: {extra: O(N)}
properties: {deterministic: true, exact_without_noise: true, one_tap_per_subcarrier: true}
history:
  year: 1971
  people: [Stephen B. Weinstein, Paul M. Ebert]
  note: "Chang described orthogonal overlapping subchannels in 1966. Weinstein and Ebert built the modulator and demodulator from the DFT in 1971, and Peled and Ruiz added the cyclic prefix in 1980."
prereqs: [multicarrier-modulation, cyclic-prefix, fast-fourier-transform]
see_also: [inter-carrier-interference, discrete-multitone, orthogonal-frequency-division-multiple-access, peak-to-average-power-ratio, sc-fdma, frequency-domain-equalization, schmidl-cox-synchronization, comb-pilot-channel-estimation]
sources:
  - paper: doi:10.1002/j.1538-7305.1966.tb02435.x
    title: "R. W. Chang, Synthesis of band-limited orthogonal signals for multichannel data transmission, Bell System Technical Journal 45(10), 1966"
    locator: "pages 1775 to 1796 (band-limited subchannels whose spectra overlap and that stay orthogonal)"
  - paper: doi:10.1109/TCOM.1971.1090705
    title: "S. B. Weinstein and P. M. Ebert, Data transmission by frequency-division multiplexing using the discrete Fourier transform, IEEE Transactions on Communication Technology 19(5), 1971"
    locator: "pages 628 to 634 (the DFT as the modulator and the demodulator of a frequency-division multiplexed system)"
  - paper: doi:10.1109/ICASSP.1980.1171076
    title: "A. Peled and A. Ruiz, Frequency domain data transmission using reduced computational complexity algorithms, IEEE International Conference on Acoustics, Speech, and Signal Processing (ICASSP), 1980"
    locator: "pages 964 to 967 (the cyclic extension of each block)"
  - paper: doi:10.1109/TCOM.1985.1096357
    title: "L. J. Cimini, Analysis and simulation of a digital mobile channel using orthogonal frequency division multiplexing, IEEE Transactions on Communications 33(7), 1985"
    locator: "pages 665 to 675 (OFDM on the mobile radio channel)"
  - book: isbn:9780521837163
    title: "Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005"
    locator: "Chapter 12, Section 12.4.1 (the DFT implementation) and Section 12.4.2 (the cyclic prefix)"
  - book: isbn:9780521845274
    title: "David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005"
    locator: "Section 3.4.4 (OFDM: the cyclic prefix makes the channel a circular convolution, which the DFT diagonalizes)"
---

Orthogonal frequency-division multiplexing (OFDM) sends $N$ data symbols $X[0], \ldots, X[N-1]$ at the same time on $N$ subcarriers, one symbol per subcarrier. The transmitter computes the samples with an inverse [FFT](/fast-fourier-transform/) and puts a copy of the last $N_{cp}$ samples in front of them, the [cyclic prefix](/cyclic-prefix/). The receiver drops the prefix, takes an FFT and divides each output by one complex number, the channel gain $H[k]$ of that subcarrier. If the channel has $L$ taps and $N_{cp} \ge L - 1$, this one-tap division is exact apart from the noise: the frequency-selective channel, which causes [intersymbol interference](/intersymbol-interference/) for a single carrier, becomes $N$ flat channels $Y[k] = H[k] X[k] + W[k]$. OFDM is the discrete form of [multicarrier modulation](/multicarrier-modulation/). It differs from [frequency-domain equalization](/frequency-domain-equalization/) of a single carrier, which uses the same prefix and FFT but puts the data symbols in time, not on the subcarriers. This page uses the unitary DFT pair $x = F^H X$, $Y = F y$ with $F[k, n] = e^{-j 2\pi k n / N} / \sqrt N$, and $j$ is the imaginary unit. The algebra pages on the [discrete Fourier transform](/discrete-fourier-transform/) write $i$ and use the unnormalized pair.

## In plain words

A channel with echoes smears each sent sample into the next ones. If you send fast, the smear spreads over many symbols and they mix. OFDM avoids this. It splits the data into many slow streams, each on its own tone, and sends all the tones together as one long block. Each tone is so narrow that the echoes only change its strength and its phase. Before each block the sender repeats the end of the block. The receiver throws this copy away, so the echoes of the previous block fall into the part that is removed. What is left looks to the receiver as if the block were repeated forever. Then a Fourier transform separates the tones exactly, and the receiver corrects each tone with one division.

## The problem

The input is a block of $N$ complex data symbols $X[0], \ldots, X[N-1]$, for example points of [QPSK](/quadrature-amplitude-modulation/) with energy $E_s = E|X[k]|^2 = 1$. The channel is a linear time-invariant filter with taps $h[0], \ldots, h[L-1]$ (the [tapped delay line model](/tapped-delay-line-channel-model/) at one tap per sample) followed by white noise $w[i] \sim \mathcal{CN}(0, N_0)$. The SNR is $E_s / N_0$. The receiver knows $h$. The task is to send the block and recover it so that each symbol sees a scalar channel, without an equalizer whose cost grows with $L$ for each symbol. The frequency response of the channel is $H[k] = \sum_{l=0}^{L-1} h[l]\, e^{-j 2\pi k l / N}$, the unnormalized DFT of the taps padded to length $N$.

## The algorithm

```pseudo id=main
OFDM(X, h, N_cp)
L1  x ← Fᴴ X                                        ▷ transmitter: unitary inverse FFT of the N symbols
L2  s ← (x[N-N_cp], .., x[N-1], x[0], .., x[N-1])   ▷ put the cyclic prefix in front, send s
L3  y ← (r[N_cp], .., r[N_cp+N-1])                  ▷ receiver: r is s through the channel; drop the prefix
L4  Y ← F y                                         ▷ unitary FFT
L5  H[k] ← Σ_l h[l] e^(-j2πkl/N) for k = 0, .., N-1 ▷ channel gains, unnormalized DFT of the taps
L6  return X̂ with X̂[k] = Y[k] / H[k]                ▷ one tap per subcarrier
```

Line L1 builds the time samples. Sample $n$ is a sum of $N$ complex exponentials, one per subcarrier, with frequency $k f_s / N$ for the sample rate $f_s$; index $k \ge N/2$ stands for the negative frequency $k - N$. Line L2 copies the last $N_{cp}$ samples to the front, so the symbol on the air has $N + N_{cp}$ samples. Line L3 waits until the echoes of the previous symbol have died out and keeps the last $N$ samples. Inside this window, every sample of the current symbol that the channel mixes in is either a sample of $x$ or a copy of one from the prefix, so the window is the circular convolution of $h$ and $x$. Line L4 turns the circular convolution into a product on each subcarrier, line L5 computes the gains, and line L6 undoes them. In practice $H[k]$ comes from pilots, for example by [comb pilot estimation](/comb-pilot-channel-estimation/), and the receiver first finds the start of the symbol and the frequency offset with [Schmidl-Cox synchronization](/schmidl-cox-synchronization/) or the [van de Beek estimator](/van-de-beek-estimator/).

## Example

Take $N = 4$, $N_{cp} = 1$, the channel $h = (1, 0.5)$ with $L = 2$, so $N_{cp} = L - 1$, no noise, and the BPSK block $X = (1, -1, 1, 1)$.

| Step | Line | Values |
|---|---|---|
| inverse FFT | L1 | $x = (1, -j, 1, j)$ |
| add the prefix | L2 | $s = (j, 1, -j, 1, j)$ |
| channel output | | $r = (j,\ 1 + 0.5j,\ 0.5 - j,\ 1 - 0.5j,\ 0.5 + j,\ 0.5j)$ |
| drop the prefix | L3 | $y = (1 + 0.5j,\ 0.5 - j,\ 1 - 0.5j,\ 0.5 + j)$ |
| FFT | L4 | $Y = (1.5,\ -1 + 0.5j,\ 0.5,\ 1 + 0.5j)$ |
| gains | L5 | $H = (1.5,\ 1 - 0.5j,\ 0.5,\ 1 + 0.5j)$ |
| one tap | L6 | $\hat X = (1, -1, 1, 1)$ |

For example $x[1] = \frac12 (1 - j - 1 - j) = -j$, and $H[1] = 1 + 0.5\, e^{-j\pi/2} = 1 - 0.5j$, so $Y[1] = H[1] X[1] = -1 + 0.5j$. The last output sample $0.5j$ is the echo of this symbol into the next one; line L3 of the next symbol drops it with that symbol's prefix. Without the prefix ($N_{cp} = 0$), the window $y$ misses the echo $0.5\, x[3]$ in $y[0]$, and line L6 returns $(1 - 0.167j,\ -0.9 - 0.2j,\ 1 - 0.5j,\ 0.9 - 0.2j)$: every subcarrier is disturbed, not only one.

A larger case, as a measurement: $N = 64$, $N_{cp} = 8$, $h = (1, 0.5)$, QPSK, $E_s / N_0 = 10$ dB. Subcarrier $k$ sees the SNR $|H[k]|^2 E_s / N_0$, which goes from $2.5$ at $H = 0.5$ to $22.5$ at $H = 1.5$. The QPSK symbol error rate $2Q(\sqrt\gamma) - Q(\sqrt\gamma)^2$, averaged over the 64 values of $\gamma$, is $0.018549$, and 200 simulated symbols (12800 decisions) agree with it inside a Wilson interval. A flat channel at the same SNR gives $1.5648 \times 10^{-3}$; the weak subcarriers dominate the average, which is why OFDM needs coding or [bit loading](/bit-loading/) across subcarriers.

## Correctness

**Claim.** If $N_{cp} \ge L - 1$, lines L1 to L4 give $Y[k] = H[k] X[k] + W[k]$ for every $k$, where $W[0], \ldots, W[N-1]$ are independent $\mathcal{CN}(0, N_0)$. So line L6 returns $X[k] + W[k] / H[k]$, which is $X[k]$ exactly without noise when $H[k] \ne 0$. This is a theorem in the model of the page (linear time-invariant channel over the symbol, perfect timing, no frequency offset).

**Key invariant.** After line L3, $y[n] = \sum_l h[l]\, x[(n - l) \bmod N]$ plus noise, a [circular convolution](/circular-convolution/): every input sample that reaches the window is a sample of $x$ or its copy in the prefix, never a sample of the previous symbol.

The DFT of a circular convolution is the product of the DFTs, with the unnormalized DFT on the taps, and a unitary $F$ maps white noise to white noise of the same variance. The full proof is below.

## Complexity

Lines L1 and L4 are FFTs of size $N$, $O(N \log N)$ time each in the [real RAM](/real-ram/). Lines L2 and L3 copy $N_{cp} \le N$ samples, line L6 is $N$ divisions, and line L5 is one more FFT, done once for as long as the channel stays fixed. So a symbol costs $O(N \log N)$ time, or $O(\log N)$ per data symbol, whatever the length $L$ of the channel, against $O(N L)$ per block for a time-domain equalizer with $L$ taps. The extra space is $O(N)$. The implementation has its own radix-2 FFT for a power of two $N$ and checks it against the direct DFT of the shared helper.

## Properties

- **Orthogonality.** The subcarriers $e^{j 2\pi k n / N}$, $n = 0, \ldots, N - 1$, are orthogonal over one symbol. Their spectra overlap, but each one is zero at the centers of all the others, so OFDM needs no guard band between subcarriers. Their spacing is $f_s / N$.
- **Cost of the prefix.** The data rate drops by the factor $N / (N + N_{cp})$, and the energy in the prefix is lost too. With IEEE 802.11a numbers, $N = 64$, $N_{cp} = 16$ and $f_s = 20$ MHz, the spacing is $312.5$ kHz, the symbol lasts $4\ \mu$s and the factor is $0.8$.
- **Energy.** With the unitary pair, $\sum_n |x[n]|^2 = \sum_k |X[k]|^2$ ([Parseval's theorem](/parsevals-theorem/)), so the energy per subcarrier equals the energy per time sample and $W[k]$ has the same variance $N_0$ as $w[n]$.
- **Diversity.** A coded OFDM link gets frequency diversity because a deep fade hits only a few subcarriers; an uncoded one does not, and its error rate is set by the weakest subcarriers.
- **Peaks.** The time samples are sums of $N$ independent terms and are close to Gaussian for large $N$, so the [peak-to-average power ratio](/peak-to-average-power-ratio/) is high. This is the main drawback for the power amplifier.

## Variants and improvements

- **Guard bands and a DC null.** Real systems leave the subcarriers near $\pm f_s/2$ and often $k = 0$ empty, to ease the filters and avoid the DC offset of the receiver.
- **Discrete multitone.** On a wire the signal must be real. [Discrete multitone](/discrete-multitone/) puts $X[N-k] = X[k]^*$ on the input of line L1 and loads a different number of bits on each subcarrier.
- **Multiple access.** [OFDMA](/orthogonal-frequency-division-multiple-access/) gives different subcarriers to different users. [SC-FDMA](/sc-fdma/) spreads each user's symbols with a DFT first, to lower the peaks.
- **Other pulses.** OFDM uses a rectangular pulse per subcarrier, so its spectrum falls slowly. [Filter bank multicarrier](/filter-bank-multicarrier/), [GFDM](/generalized-frequency-division-multiplexing/) and [UFMC](/universal-filtered-multicarrier/) shape the subcarriers or groups of them.
- **Doubly dispersive channels.** When the channel changes inside a symbol, the subcarriers leak into each other ([inter-carrier interference](/inter-carrier-interference/)). [OTFS](/orthogonal-time-frequency-space-modulation/) and [AFDM](/affine-frequency-division-multiplexing/) place the data in other domains for this case.

## When to use it

Use OFDM when the channel delay spread is long compared with the sample period, so that a single carrier would need a long equalizer: wireless LAN, LTE and 5G NR, digital broadcasting, and wired lines in the form of discrete multitone. It also suits links where the transmitter can adapt the power and the bits per subcarrier. Prefer a single carrier with [frequency-domain equalization](/frequency-domain-equalization/) or SC-FDMA when the power amplifier must run near saturation, and a plain single carrier when the channel is flat. OFDM is sensitive to frequency offsets, Doppler and phase noise, so it needs careful synchronization.

## Pitfalls

- **A prefix shorter than the channel.** With $N_{cp} < L - 1$ in line L2, the window of line L3 picks up samples of the previous symbol and $y$ is no longer a circular convolution; every subcarrier gets interference, not only the edge ones. Line L2 must use $N_{cp} \ge L - 1$, where $L - 1$ is the delay of the last significant tap in samples.
- **The wrong window.** Line L3 must start at sample $N_{cp}$ of the symbol. A window that starts inside the prefix but late enough still works, with a phase ramp $e^{-j 2\pi k \delta / N}$ that the channel estimate absorbs. A window that starts after the prefix takes samples of the next symbol.
- **Mixed DFT scales.** If line L1 uses the unnormalized inverse with $1/N$ and line L4 the unitary $F$, the result is $H[k] X[k] / \sqrt N$. Use one pair, and use the unnormalized DFT for $H[k]$ in line L5 with either pair.
- **Division by a deep fade.** Line L6 divides by $H[k]$, so a subcarrier with $|H[k]|$ near zero has a huge noise $W[k] / H[k]$. A decoder should weight each subcarrier by $|H[k]|^2$, or the transmitter should not use that subcarrier.
- **The prefix in the SNR.** The prefix carries energy but no new data. Count $E_s$ per data symbol as $(N + N_{cp}) / N$ times the energy per sample when you compare OFDM with a single carrier at the same $E_b / N_0$.

## Implementations

## History

Chang published the conditions for band-limited orthogonal subchannels with overlapping spectra in 1966 at Bell Labs. Weinstein and Ebert showed in 1971 that the DFT performs the modulation and the demodulation of all subcarriers at once, which removed the bank of oscillators and filters. They used a guard time of silence between symbols. Peled and Ruiz replaced the silence with a cyclic extension of each block in 1980, so that the channel acts as a circular convolution. Cimini studied OFDM for the mobile radio channel in 1985. With fast FFT hardware, OFDM became the modulation of digital audio and television broadcasting, of IEEE 802.11a and its successors, and of LTE and 5G NR.

## References
