---
tag: 4S5G9S
kind: concept
slug: cyclic-prefix
name: Cyclic prefix
aliases:
- guard interval
area: communications/ofdm-and-multicarrier
level: intro
summary: "A copy of the end of each block placed in front of it, which turns linear convolution with the channel into circular convolution."
prereqs: [circular-convolution, intersymbol-interference]
see_also: [orthogonal-frequency-division-multiplexing, discrete-multitone, frequency-domain-equalization, sc-fdma, van-de-beek-estimator, delay-spread, overlap-add-method, convolution-theorem]
sources:
  - paper: doi:10.1109/ICASSP.1980.1171076
    title: "A. Peled and A. Ruiz, Frequency domain data transmission using reduced computational complexity algorithms, IEEE International Conference on Acoustics, Speech, and Signal Processing (ICASSP), 1980"
    locator: "pages 964 to 967 (the cyclic extension of each block)"
  - book: isbn:9780521845274
    title: "David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005"
    locator: "Section 3.4.4 (the cyclic prefix converts the linear convolution into a circular one, and the DFT diagonalizes it)"
  - book: isbn:9780521837163
    title: "Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005"
    locator: "Chapter 12, Section 12.4.2 (the cyclic prefix)"
  - paper: doi:10.1109/TCOM.1971.1090705
    title: "S. B. Weinstein and P. M. Ebert, Data transmission by frequency-division multiplexing using the discrete Fourier transform, IEEE Transactions on Communication Technology 19(5), 1971"
    locator: "pages 628 to 634 (the DFT system that the cyclic prefix later completed)"
---

A cyclic prefix is a copy of the last $N_{cp}$ samples of a block of $N$ samples, sent just before the block. A channel with $L$ taps convolves the sent samples with its impulse response, a linear convolution that mixes each block with the end of the previous one. If $N_{cp} \ge L - 1$ and the receiver drops the first $N_{cp}$ samples of each received block, the $N$ samples that remain are the [circular convolution](/circular-convolution/) of the block with the taps. A DFT turns a circular convolution into a product, so each frequency bin sees one complex gain. This is what makes [OFDM](/orthogonal-frequency-division-multiplexing/), [discrete multitone](/discrete-multitone/), single-carrier [frequency-domain equalization](/frequency-domain-equalization/) and [SC-FDMA](/sc-fdma/) work. The price is $N_{cp}$ extra samples per block, which carry energy but no new data. The page uses $j$ for the imaginary unit and the unnormalized DFT $H[k] = \sum_l h[l] e^{-j 2\pi k l / N}$ for the channel gains.

## In plain words

A channel with echoes makes each sample spill into the next few samples. When you send data in blocks, the end of one block spills into the start of the next one, and the start of each block lacks the echoes of its own end. The cyclic prefix fixes both problems. Before each block the sender repeats the last few samples of that block. The spill from the previous block lands on this copy, and the receiver throws the copy away. The echoes that the copy causes inside the block are exactly the echoes that the end of the block would cause if the block wrapped around. So the receiver sees the block as one turn of a loop, and the Fourier transform of a loop has no mixing between frequencies.

## The idea

Let the block be $x[0], \ldots, x[N-1]$ and the channel taps $h[0], \ldots, h[L-1]$. The sender transmits $s = (x[N - N_{cp}], \ldots, x[N-1], x[0], \ldots, x[N-1])$. The receiver gets $r[i] = \sum_l h[l]\, s[i - l]$ plus noise and keeps $y[n] = r[N_{cp} + n]$ for $n = 0, \ldots, N - 1$.

**Theorem (circular convolution).** If $N_{cp} \ge L - 1$, then $y[n] = \sum_{l=0}^{L-1} h[l]\, x[(n - l) \bmod N]$ plus noise, and the DFT gives $Y[k] = H[k] X[k] + W[k]$ on every bin $k$.

The reason is short. The sample $y[n]$ uses $s[N_{cp} + n - l]$ for $l = 0, \ldots, L - 1$. Its index is at least $N_{cp} - (L - 1) \ge 0$, so it is inside the current block, and the prefix holds $s[N_{cp} + m] = x[m \bmod N]$ for $m \ge -N_{cp}$. The DFT step is the [convolution theorem](/convolution-theorem/) for circular convolution. The full proof is on the [OFDM](/orthogonal-frequency-division-multiplexing/) page.

**Matrix view.** Write the kept window as $y = C x + v$. With the prefix, $C$ is the $N \times N$ circulant matrix whose first column is $(h[0], \ldots, h[L-1], 0, \ldots, 0)$. Every circulant matrix is diagonalized by the DFT: $C = F^H \operatorname{diag}(H[0], \ldots, H[N-1])\, F$ with the unitary $F$. Without the prefix, $C$ is a lower triangular Toeplitz matrix plus a term from the previous block, and the DFT does not diagonalize it.

**What the prefix costs.** A block of $N$ data samples takes $N + N_{cp}$ sample times, so the rate drops by the factor $N / (N + N_{cp})$. The prefix also takes the fraction $N_{cp} / (N + N_{cp})$ of the transmit energy, a loss of $10 \log_{10}((N + N_{cp}) / N)$ dB in SNR per data symbol. To keep the loss small, $N$ must be large compared with the delay spread in samples; but a large $N$ makes the symbol long, and the channel must stay constant over it.

**Timing slack.** If the prefix is longer than the channel, the receiver may start its window up to $\delta = N_{cp} - (L - 1)$ samples early. The window is then still a circular convolution, shifted by $\delta$, and bin $k$ gets the extra phase $e^{-j 2\pi k \delta / N}$, which a channel estimate absorbs. So the excess prefix gives slack in the symbol timing. The redundancy of the prefix also lets the receiver find the timing and the frequency offset without pilots, as in the [van de Beek estimator](/van-de-beek-estimator/).

**Other ways to separate the blocks.** The sender can send $N_{cp}$ zeros after each block instead of a copy (zero padding). The receiver then adds the last $N_{cp}$ received samples to the first ones, the step of the [overlap-add method](/overlap-add-method/), and gets the same circular convolution. Zero padding sends no energy in the gap, but it adds the noise of the gap to the head of the block. Weinstein and Ebert in 1971 used an empty gap between blocks, which removes the interference between blocks but not the interference between subcarriers; the cyclic extension of Peled and Ruiz in 1980 removes both.

## Examples

**A four-sample block.** Take $N = 4$, $N_{cp} = 1$ and $h = (1, 0.5)$. The kept window is $y = C x$ with

$$C = \begin{bmatrix} 1 & 0 & 0 & 0.5 \\ 0.5 & 1 & 0 & 0 \\ 0 & 0.5 & 1 & 0 \\ 0 & 0 & 0.5 & 1 \end{bmatrix}.$$

The entry $0.5$ in the top right corner comes from the prefix: $y[0] = x[0] + 0.5\, x[-1]$, and the prefix sample $x[-1]$ is a copy of $x[3]$. The eigenvalues of $C$ are $H[k] = 1 + 0.5\, e^{-j\pi k/2}$, that is $1.5$, $1 - 0.5j$, $0.5$ and $1 + 0.5j$, and the eigenvectors are the columns of $F^H$. Without the prefix the corner entry is the sample $0.5$ times the last sample of the previous block, and for $X = (1, -1, 1, 1)$ after a silent block the one-tap receiver returns $(1 - 0.167j,\ -0.9 - 0.2j,\ 1 - 0.5j,\ 0.9 - 0.2j)$ instead of $X$.

**IEEE 802.11a.** $N = 64$ and $N_{cp} = 16$ at $f_s = 20$ MHz, so the prefix lasts $0.8\ \mu$s, the rate factor is $0.8$, and the energy loss is $10 \log_{10}(80/64) = 0.97$ dB. Echoes up to $0.8\ \mu$s, about 240 m of extra path, cause no interference between blocks.

**LTE with the normal prefix.** $N = 2048$ at $f_s = 30.72$ MHz (15 kHz spacing), with $N_{cp} = 144$ on most symbols, so the prefix lasts $4.69\ \mu$s and the energy loss is $10 \log_{10}(2192/2048) = 0.30$ dB. The longer symbol makes the relative cost smaller than in 802.11a.

## Where it is used

The cyclic prefix is part of almost every block transmission over a dispersive channel: OFDM in wireless LAN, LTE, 5G NR and digital broadcasting, [discrete multitone](/discrete-multitone/) on telephone lines, and single-carrier blocks with [frequency-domain equalization](/frequency-domain-equalization/) or [SC-FDMA](/sc-fdma/). The length is chosen from the [delay spread](/delay-spread/) of the channel. In OFDM receivers, the prefix is also the basis of blind timing and frequency estimation, and of the timing slack that lets the window start early.

## References
