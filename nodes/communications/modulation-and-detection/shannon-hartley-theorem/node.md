---
tag: JFJ3K2
kind: theorem
slug: shannon-hartley-theorem
name: Shannon-Hartley theorem
aliases:
- Shannon-Hartley law
- Shannon limit
area: communications/modulation-and-detection
level: intro
summary: "A band of width B with white Gaussian noise of power N = N0 B and received signal power at most S has capacity B log2(1 + S/N) bits/s, reached by a Gaussian input."
prereqs: [additive-white-gaussian-noise-channel, channel-capacity, sampling-theorem]
see_also: [channel-coding-theorem, spectral-efficiency, energy-per-bit-to-noise-density-ratio, additive-white-gaussian-noise-channel, water-filling-power-allocation, nyquist-isi-criterion, power-spectral-density, mimo-capacity]
sources:
  - paper: doi:10.1002/j.1538-7305.1948.tb00917.x
    title: C. E. Shannon, A mathematical theory of communication (continued), Bell System Technical Journal 27(4), 1948
    locator: Part IV, the continuous channel (the capacity of a band W with white thermal noise of power N under an average power limit P is W log((P + N)/N))
  - paper: doi:10.1109/JRPROC.1949.232969
    title: C. E. Shannon, Communication in the presence of noise, Proceedings of the IRE 37(1), 1949
    locator: pp. 10 to 21 (signals of band W and duration T as points in 2TW dimensions, and the capacity W log2(1 + P/N) by a sphere-packing argument)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Chapter 9, Theorem 9.1.1 (the capacity of the discrete-time Gaussian channel with a power constraint, with the proof of achievability and the converse) and Section 9.3 (band-limited channels)
  - paper: doi:10.1109/T-AIEE.1928.5055024
    title: H. Nyquist, Certain topics in telegraph transmission theory, Transactions of the AIEE 47, 1928
    locator: pp. 617 to 644 (a band W carries at most 2W independent pulses per second)
  - paper: doi:10.1002/j.1538-7305.1928.tb01236.x
    title: R. V. L. Hartley, Transmission of information, Bell System Technical Journal 7(3), 1928
    locator: pp. 535 to 563 (information as the logarithm of the number of distinguishable sequences, proportional to the band and the time)
---

The Shannon-Hartley theorem gives the capacity of the band-limited channel with additive white Gaussian noise, in bits per second. It turns the capacity of the discrete-time [Gaussian channel](/additive-white-gaussian-noise-channel/), $\tfrac12 \log_2(1 + \mathrm{SNR})$ bits per use, into a rate for a continuous-time channel of bandwidth $B$, which offers $2B$ real uses per second. The result, $C = B \log_2(1 + S/N)$, is the upper limit that every modulation and code for this channel is measured against.

## Statement

Let a channel carry a real signal $x(t)$ whose spectrum lies in a band of width $B$ hertz (at baseband, $|f| \le B$). The receiver sees $y(t) = x(t) + z(t)$, where $z$ is white Gaussian noise with one-sided power spectral density $N_0$ (two-sided $N_0/2$), independent of $x$. The average power of $x$ at the receiver is at most $S$. Let $N = N_0 B$ be the noise power in the band. Then the capacity of the channel is

$$C = B \log_2\!\left(1 + \frac{S}{N}\right) = B \log_2\!\left(1 + \frac{S}{N_0 B}\right) \quad \text{bits per second}.$$

That is: for every rate $R < C$ there are codes whose error probability goes to $0$ as the block length grows, and for every $R > C$ the error probability of every code stays bounded away from $0$. The rate $C$ is reached with a Gaussian input: a stationary Gaussian process with a flat spectrum over the band and power $S$.

**How it relates to the nearby pages.** [Channel capacity](/channel-capacity/) defines the capacity of a channel as the largest mutual information per use, for any channel. The [channel coding theorem](/channel-coding-theorem/) says that this number is the limit of reliable rates. The Shannon-Hartley theorem is the evaluation of both for one channel: continuous time, band $B$, white Gaussian noise, power limit $S$. It is the only one of the three that gives bits per second.

**The bridge to the discrete AWGN channel.** Sampled at the rate $2B$, the channel becomes $2B$ uses per second of $Y = X + Z$ with noise variance $\sigma^2 = N_0/2$ per real sample and signal power $P = S/(2B)$ per real sample. The SNR per real use is $P/\sigma^2 = 2E_s/N_0$, where $E_s = P$ is the energy per real symbol, and here it equals $S/(N_0 B) = S/N$. For a complex baseband signal on a carrier with passband width $B$ there are $B$ complex uses per second, each with $\mathrm{SNR} = E_s/N_0$ per complex symbol, and the same formula $C = B\log_2(1 + E_s/N_0)$ holds with $E_s = S/B$.

## In plain words

A channel of a given width can carry only a certain number of separate values each second, twice its width. Noise blurs each value, so the receiver can tell apart only so many levels for each one. More signal power means more levels can be told apart, but the number grows slowly, as a logarithm. The theorem puts the two facts together: the best rate is the number of values per second times the number of bits each value can carry when the noise is random and Gaussian. No code can beat this rate, and good long codes can come as close to it as wanted. To come close, the transmitted values should look like random Gaussian noise themselves.

## Proof

The proof has three steps: reduce the band-limited channel to a discrete-time channel, find the capacity of that channel per use, and multiply by the number of uses per second.

**Step 1: dimensions.** By the [sampling theorem](/sampling-theorem/), a signal in the band $|f| \le B$ is determined by its samples at the spacing $1/(2B)$, and the functions $\phi_n(t) = \sqrt{2B}\, \mathrm{sinc}(2Bt - n)$, with $\mathrm{sinc}(u) = \sin(\pi u)/(\pi u)$, are an orthonormal basis of such signals. So $x(t) = \sum_n x_n \phi_n(t)$ with $x_n = \langle x, \phi_n \rangle$. Project the received signal on the same basis: $y_n = \langle y, \phi_n \rangle = x_n + z_n$. The noise outside the band is independent of the in-band part and carries no information about $x$, so nothing is lost. For white noise of two-sided density $N_0/2$ and an orthonormal basis, the $z_n$ are independent $\mathcal{N}(0, N_0/2)$. The power limit becomes $\frac{1}{n}\sum_{i \le n} x_i^2 \le S/(2B)$ for blocks of $n$ samples, since a stretch of time $T_0$ holds $n = 2BT_0$ samples and energy $\sum x_i^2 \le S T_0$.

So the channel is the discrete Gaussian channel $Y_i = X_i + Z_i$ with $Z_i \sim \mathcal{N}(0, \sigma^2)$, $\sigma^2 = N_0/2$, and average power at most $P = S/(2B)$, used $2B$ times per second.

(Signals of finite duration are not exactly band-limited. The count of $2BT_0$ dimensions for a time $T_0$ and a band $B$ is exact only in the limit of large $T_0$; Cover and Thomas, Section 9.3, and Shannon's 1949 paper treat this step. It does not change the rate per second.)

**Step 2: the converse per use.** Let a code of $2^{nR}$ codewords of length $n$ meet the power limit, with error probability $P_e$. Fano's inequality gives $nR \le I(X^n; Y^n) + 1 + P_e\, nR$. The noise is independent from use to use, so $I(X^n; Y^n) \le \sum_i I(X_i; Y_i)$. For one use with input power $P_i = \mathbb{E} X_i^2$,

$$I(X_i; Y_i) = h(Y_i) - h(Z_i) \le \tfrac12 \log_2\!\big(2\pi e (P_i + \sigma^2)\big) - \tfrac12 \log_2(2\pi e \sigma^2) = \tfrac12 \log_2\!\left(1 + \frac{P_i}{\sigma^2}\right),$$

because $Y_i$ has variance $P_i + \sigma^2$ and the Gaussian has the largest differential entropy for a given variance. The function $\tfrac12\log_2(1 + p/\sigma^2)$ is concave in $p$ and $\frac1n \sum P_i \le P$, so by Jensen's inequality $\sum_i I(X_i; Y_i) \le \frac{n}{2}\log_2(1 + P/\sigma^2)$. Dividing by $n$ and letting $n \to \infty$: if $P_e \to 0$, then $R \le \tfrac12 \log_2(1 + P/\sigma^2)$.

**Step 3: achievability per use.** A random codebook with independent $\mathcal{N}(0, P - \epsilon)$ entries and a decoder that looks for the unique codeword jointly typical with the output reaches every rate below $\tfrac12\log_2(1 + P/\sigma^2)$ with error probability going to $0$; this is Theorem 9.1.1 of Cover and Thomas and an instance of the [channel coding theorem](/channel-coding-theorem/). The equality case in step 2 shows why the input must be Gaussian: $h(Y_i)$ is largest only when $Y_i$, and so $X_i$, is Gaussian.

**Step 4: per second.** The capacity per use is $\tfrac12\log_2(1 + P/\sigma^2)$ with

$$\frac{P}{\sigma^2} = \frac{S/(2B)}{N_0/2} = \frac{S}{N_0 B} = \frac{S}{N}.$$

There are $2B$ uses per second, so $C = 2B \cdot \tfrac12 \log_2(1 + S/N) = B\log_2(1 + S/N)$. $\blacksquare$

## Consequences

**Two numbers to check by hand.** A telephone-like band of $B = 3$ kHz at $S/N = 30$ dB ($1000$) gives $C = 3000 \log_2 1001 = 29.90$ kbit/s. A band of $1$ MHz at $30$ dB gives $9.967$ Mbit/s.

**Power-limited and band-limited regimes.** At high SNR, $C \approx B\log_2(S/N)$: doubling the power (3 dB) adds about $B$ bits per second, while doubling the band nearly doubles $C$. At low SNR, $\log_2(1 + u) \approx u\log_2 e$, so $C \approx (S/N_0)\log_2 e$ and the band hardly matters.

**The wideband limit.** For a fixed $S/N_0$, $C$ grows with $B$ but stays below $(S/N_0)\log_2 e$. With $S/N_0 = 10^6$ Hz:

| $B$ | $C$ |
|---|---|
| 100 kHz | 345.9 kbit/s |
| 1 MHz | 1.000 Mbit/s |
| 10 MHz | 1.375 Mbit/s |
| 100 MHz | 1.436 Mbit/s |
| $\to \infty$ | 1.443 Mbit/s |

**The bound on $E_b/N_0$.** Send $R$ bits per second, so $S = E_b R$, and let $\eta = R/B$ be the [spectral efficiency](/spectral-efficiency/). Reliable transmission needs $R \le C$, that is $\eta \le \log_2(1 + \eta E_b/N_0)$, or

$$\frac{E_b}{N_0} \ge \frac{2^\eta - 1}{\eta}.$$

The right side decreases to $\ln 2 = 0.693$, or $-1.59$ dB, as $\eta \to 0$. No scheme of any bandwidth works below this [energy per bit](/energy-per-bit-to-noise-density-ratio/). At $\eta = 2$ bits/s/Hz the bound is $1.5$, or $1.76$ dB.

**Uncoded modulation is far from the limit.** BPSK needs $E_b/N_0 = 9.59$ dB for a bit error rate of $10^{-5}$ at $\eta = 1$ (counting $B$ as the passband width of a Nyquist pulse), where the theorem allows $0$ dB. The gap of more than 9 dB is what channel codes recover; modern LDPC and turbo codes work within a fraction of a decibel of the bound.

## Tightness

- **The Gaussian input is needed.** Step 2 is an equality only for a Gaussian $Y$. A finite constellation of $M$ points carries at most $\log_2 M$ bits per use, so at high SNR its rate stays flat while $C$ keeps growing. At low SNR the loss is small, which is why binary signaling is close to optimal when the band is wide.
- **The rate is a sharp limit.** Below $C$ the error probability can be made as small as wanted; above $C$ it cannot go to $0$ (step 2). The theorem says nothing about the block length or the complexity needed.
- **The assumptions matter.** With a channel whose gain varies across the band, or with colored noise, the flat Gaussian input is no longer best: the capacity is $\int_0^B \log_2\big(1 + p(f)|H(f)|^2/N(f)\big)\, df$, where $H$ is the gain of the channel, $N(f)$ the one-sided noise density and $p(f)$ the input power per hertz, spread over the band by [water-filling](/water-filling-power-allocation/). With $H = 1$, $N(f) = N_0$ and $p(f) = S/B$ this is the formula of the theorem. With fading, several antennas or interference, other formulas apply, such as [MIMO capacity](/mimo-capacity/).
- **S is the received power.** The theorem knows nothing about path loss; $S$ is measured at the receiver, in the band, under an average (not peak) limit.

## History

Nyquist in 1928 showed that a band of $W$ hertz carries at most $2W$ independent pulses per second, the same count as in step 1. Hartley, in the same year, measured information as the logarithm of the number of messages that can be told apart, which grows with the band and the time; a rate of the form $2W\log_2 M$ for $M$ distinguishable levels is often called Hartley's law. Neither paper had noise as a random process or a probability of error. Shannon gave the capacity formula in Part IV of *A Mathematical Theory of Communication* (1948), and in *Communication in the Presence of Noise* (1949) he gave the geometric proof: signals of band $W$ and duration $T$ are points in a space of $2TW$ dimensions, the noise turns each point into a small sphere, and the number of spheres that fit gives the rate. The name Shannon-Hartley joins the formula to Hartley's earlier count of levels.

## References
