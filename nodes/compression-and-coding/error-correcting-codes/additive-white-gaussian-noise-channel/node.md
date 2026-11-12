---
tag: QYZ6QZ
kind: model
slug: additive-white-gaussian-noise-channel
name: Additive white Gaussian noise channel
aliases:
- AWGN channel
area: compression-and-coding/error-correcting-codes
level: core
summary: A channel that adds independent Gaussian noise to each real symbol under a power limit. Its capacity is (1/2) log2(1 + SNR) bits per use, so Eb/N0 must exceed ln 2, or -1.59 dB.
prereqs: [binary-symmetric-channel]
see_also: [channel-capacity, channel-coding-theorem, forward-error-correction, binary-erasure-channel, maximum-likelihood-decoding, belief-propagation-decoding, turbo-code, ldpc-code]
sources:
  - paper: doi:10.1002/j.1538-7305.1948.tb00917.x
    title: C. E. Shannon, A mathematical theory of communication (continued), Bell System Technical Journal 27(4), 1948
    locator: Part IV (the continuous channel), the capacity W log2(1 + P/N) of a channel of band W with white thermal noise of power N and average signal power P
  - paper: doi:10.1109/JRPROC.1949.232969
    title: C. E. Shannon, Communication in the presence of noise, Proceedings of the IRE 37(1), 1949
    locator: The geometric argument with signals as points in a space of 2TW dimensions, and the capacity formula for white Gaussian noise
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Chapter 9 (Gaussian channel), Section 9.1 (definitions, p. 263) and Section 9.3 (band-limited channels, p. 270)
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 1 (BPSK on the AWGN channel, hard and soft decisions, the Shannon limit and coding gain)
---

The additive white Gaussian noise (AWGN) channel is the standard model of a radio, cable or optical link in which the main problem is thermal noise. The receiver sees the sent real number plus a sample of Gaussian noise, new and independent for each symbol, and the sender has a limit on the average power. Shannon showed that its capacity is $\tfrac12 \log_2(1 + \mathrm{SNR})$ bits per real symbol, and the distance in decibels between that limit and a real system is how coding schemes are compared.

## The machine

One use of the discrete-time channel takes a real input $x$ and returns

$$y = x + z, \qquad z \sim \mathcal{N}(0, \sigma^2),$$

with a fresh noise sample $z$ for each use, independent of the input and of the other samples. A codeword $x = (x_1, \ldots, x_n)$ must satisfy the **power constraint** $\frac1n \sum_i x_i^2 \le P$. The **signal-to-noise ratio** is $\mathrm{SNR} = P/\sigma^2$.

*White* means that the noise has the same power at all frequencies, which in discrete time means independent samples. A channel of bandwidth $W$ hertz with white noise of one-sided power spectral density $N_0$ is the same model with $2W$ real uses per second and $\sigma^2 = N_0/2$ per use.

**Binary inputs.** Most codes are binary, and the simplest modulation, BPSK, sends bit $b$ as $(1 - 2b)\sqrt{E_s}$, where $E_s$ is the energy per channel symbol. For a code of rate $R$, each information bit gets energy $E_b = E_s/R$. The figure of merit is $E_b/N_0$, usually in decibels, and

$$\mathrm{SNR} = \frac{E_s}{\sigma^2} = \frac{2 E_s}{N_0} = 2R \, \frac{E_b}{N_0}.$$

The receiver can keep each $y_i$ as a real number (*soft decisions*) or keep only its sign (*hard decisions*). The output of a hard decision is a bit, and the channel from $b$ to that bit is a [binary symmetric channel](/binary-symmetric-channel/) with crossover probability $p = Q\bigl(\sqrt{2E_s/N_0}\bigr)$, where $Q(x) = \Pr[\mathcal{N}(0, 1) > x]$.

## What it counts

- **Bit error rate** (BER) and **block error rate** after decoding, as functions of $E_b/N_0$. A code is described by its curve of BER against $E_b/N_0$ in dB.
- **Required $E_b/N_0$.** The least $E_b/N_0$ at which a scheme reaches a target BER, such as $10^{-5}$. The difference between two schemes at the same target, in dB, is the **coding gain** (see [forward error correction](/forward-error-correction/)).
- **Gap to capacity.** The difference between the required $E_b/N_0$ and the least value that capacity allows at the same rate.
- **Spectral efficiency.** Bits per real use (or per second per hertz), which trades against power.

## Relation to other models

- **Binary symmetric channel.** Hard decisions turn the AWGN channel with BPSK into a BSC. This is simple but costs signal energy: at rate $1/2$, reliable hard decision decoding needs about 1.77 dB, against 0.19 dB with soft decisions, and as the rate tends to 0 the loss tends to $10 \log_{10}(\pi/2) \approx 1.96$ dB.
- **Errors and erasures.** A receiver that marks outputs close to $0$ as erasures gets a channel between the BSC and the [binary erasure channel](/binary-erasure-channel/), and recovers part of the loss of hard decisions.
- **Binary-input AWGN channel.** Restrict the input to $\pm 1$: the result is a binary-input, symmetric, memoryless channel with real outputs. Its capacity is below the Gaussian capacity, by little at low SNR and by much at high SNR, where it cannot exceed 1 bit per use.
- **Other channels.** Fading channels multiply $x$ by a random gain; channels with intersymbol interference add past inputs; complex baseband channels are two real AWGN channels side by side.

## Known results in the model

1. **Capacity.** With the power limit $P$, the [channel capacity](/channel-capacity/) is
   $$C = \tfrac12 \log_2\bigl(1 + P/\sigma^2\bigr) \ \text{bits per real use}, \qquad C = W \log_2\Bigl(1 + \frac{P}{N_0 W}\Bigr) \ \text{bits per second}$$
   for the band-limited form (Shannon 1948). The best input is Gaussian with variance $P$. The [coding theorem](/channel-coding-theorem/) holds: every rate below $C$ is achievable with error probability tending to 0, and no rate above it is.
2. **The Shannon limit in $E_b/N_0$.** Reliable rate $R$ needs $R \le \frac12 \log_2(1 + 2R E_b/N_0)$, that is,
   $$\frac{E_b}{N_0} \ge \frac{2^{2R} - 1}{2R}.$$
   The right side increases with $R$. It is 0 dB at $R = 1/2$ and 1.76 dB at $R = 1$, and it decreases to $\ln 2 \approx 0.693$, or $-1.59$ dB, as $R \to 0$. No code at any rate works below $-1.59$ dB.
3. **Binary-input capacity.** With inputs $\pm 1$, noise variance $\sigma^2$ and the uniform input, which is best by symmetry,
   $$C_{\mathrm{BI}} = 1 - \mathbb{E}\bigl[\log_2\bigl(1 + e^{-2Y/\sigma^2}\bigr)\bigr], \qquad Y \sim \mathcal{N}(1, \sigma^2).$$
   It has no closed form; numerical integration (for example the [Simpson rule](/simpsons-rule/) or [Gaussian quadrature](/gaussian-quadrature/)) gives it. At $\sigma^2 = 1$ (SNR 0 dB) it is about 0.486 bits, against 0.5 for Gaussian inputs. The least $E_b/N_0$ for binary inputs at $R = 1/2$ is about 0.19 dB, and at $R \to 0$ it is again $-1.59$ dB.
4. **Uncoded BPSK.** The sign detector errs with probability $Q\bigl(\sqrt{2E_b/N_0}\bigr)$. A BER of $10^{-5}$ needs about 9.6 dB. At rate $1/2$ capacity allows reliable transmission at 0.19 dB, so codes can in principle save more than 9 dB at that target. [Turbo codes](/turbo-code/) and [LDPC codes](/ldpc-code/) with iterative decoding come within a fraction of a dB of the limit.
5. **Maximum likelihood is minimum Euclidean distance.** Given $y$, the likelihood of $x$ is proportional to $\exp\bigl(-\lVert y - x \rVert^2/(2\sigma^2)\bigr)$, so the [maximum likelihood decoder](/maximum-likelihood-decoding/) picks the codeword nearest to $y$ in Euclidean distance. For BPSK, $\lVert y - x \rVert^2$ is a constant minus $2\sum_i x_i y_i$, so it maximizes the correlation $\sum_i x_i y_i$.
6. **Asymptotic coding gain.** For a binary code of rate $R$ and [minimum distance](/minimum-distance/) $d$ with soft decision maximum likelihood decoding, the error probability at high $E_b/N_0$ behaves like $Q\bigl(\sqrt{2Rd\,E_b/N_0}\bigr)$ up to a constant factor, so the gain over uncoded BPSK tends to $10 \log_{10}(Rd)$ dB. With hard decisions and $t = \lfloor (d - 1)/2 \rfloor$ it tends to $10 \log_{10}(R(t + 1))$ dB. For the Hamming code $[7, 4, 3]$ these are about 2.34 dB and 0.58 dB.

## References
