---
tag: 6F9FVQ
kind: definition
slug: frequency-shift-keying
name: Frequency-shift keying
aliases:
- FSK
- M-FSK
- orthogonal FSK
area: communications/modulation-and-detection
level: intro
summary: A modulation that sends one of M tones in each symbol period. A spacing of 1/(2T) makes the tones orthogonal for a coherent receiver, and 1/T for a noncoherent one.
prereqs: [digital-modulation, signal-space-representation]
see_also: [continuous-phase-modulation, minimum-shift-keying, gaussian-minimum-shift-keying, noncoherent-detection, phase-shift-keying, bit-error-rate, frequency-hopping-spread-spectrum, power-spectral-density]
sources:
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008
    locator: Chapter 3 (orthogonal signaling and frequency-shift keying) and Section 4.5 (noncoherent detection, with the optimal noncoherent detector for FSK and the error probability of orthogonal signals)
  - book: isbn:9780306421952
    title: John B. Anderson, Tor Aulin and Carl-Erik Sundberg, Digital Phase Modulation, Plenum Press, 1986
    locator: the introduction and the treatment of the CPM signal model (continuous-phase FSK as the simplest member of the family)
---

Frequency-shift keying (FSK) sends one of $M$ tones in each symbol period, and the data selects the tone. The tones have the same amplitude, so the signal has a constant envelope. If the tones are far enough apart, they are orthogonal, and a receiver can find the sent tone by comparing $M$ correlations. The smallest spacing for orthogonal tones is $1/(2T)$ for a coherent receiver and $1/T$ for a [noncoherent](/noncoherent-detection/) one, where $T$ is the symbol period. FSK whose phase is continuous from one symbol to the next is a [continuous phase modulation](/continuous-phase-modulation/); [minimum-shift keying](/minimum-shift-keying/) is its binary case with the spacing $1/(2T)$, and [Gaussian minimum-shift keying](/gaussian-minimum-shift-keying/) smooths the frequency changes of MSK.

## Definition

Let $M \ge 2$ be the number of tones, $T$ the symbol period, $\Delta f > 0$ the tone spacing and $E_s$ the energy per symbol. The **M-ary FSK** waveforms in complex baseband are

$$s_m(t) = \sqrt{E_s/T}\; e^{j 2\pi f_m t}, \qquad 0 \le t < T, \qquad f_m = \Big(m - \frac{M - 1}{2}\Big)\Delta f, \qquad m = 0, \ldots, M - 1,$$

where $j$ is the imaginary unit. Each symbol carries $\log_2 M$ bits, so $E_b = E_s/\log_2 M$ for uncoded FSK. The passband signal is $\mathrm{Re}\{s_m(t)\sqrt{2}\,e^{j 2\pi f_c t}\}$, a tone at $f_c + f_m$. The **modulation index** is $h = \Delta f\, T$.

**The inner product of two tones.** With $u = (m - n)\Delta f\,T$ and $\mathrm{sinc}(u) = \sin(\pi u)/(\pi u)$,

$$\langle s_m, s_n \rangle = \frac{E_s}{T}\int_0^T e^{j 2\pi (m - n)\Delta f\, t}\, dt = E_s\, e^{j\pi u}\, \mathrm{sinc}(u).$$

**Orthogonality.** A coherent receiver knows the carrier phase. It compares real passband signals, and their correlation is the real part of the baseband one: $\mathrm{Re}\langle s_m, s_n\rangle = E_s \cos(\pi u)\,\mathrm{sinc}(u) = E_s \sin(2\pi u)/(2\pi u)$. This is zero when $u$ is a nonzero multiple of $1/2$. A noncoherent receiver does not know the phase, so the tones must stay orthogonal for every phase offset between them. That needs $|\langle s_m, s_n\rangle| = E_s|\mathrm{sinc}(u)| = 0$, which holds when $u$ is a nonzero integer. So the smallest spacings are

$$\Delta f_{\text{coherent}} = \frac{1}{2T}, \qquad \Delta f_{\text{noncoherent}} = \frac{1}{T}.$$

These are exact in complex baseband. In passband the correlation has an extra term of order $1/(f_c T)$, which is negligible when the carrier frequency is much larger than the symbol rate.

**Phase at the symbol boundaries.** In *discontinuous-phase* FSK, each tone comes from its own oscillator, and the phase jumps at each symbol boundary. In *continuous-phase* FSK, one oscillator changes its frequency, so the phase is continuous. The jumps spread the spectrum: the power spectral density falls as $1/f^2$ far from the carrier for discontinuous phase, against $1/f^4$ for continuous phase with rectangular frequency pulses. Continuous-phase FSK has memory and is the CPM with a rectangular pulse of one symbol.

**Error rates.** These are closed forms for equal-energy orthogonal tones in additive white Gaussian noise with perfect timing and equal priors; $Q$ is the [Gaussian Q function](/gaussian-q-function/).
- Coherent binary FSK: $P_b = Q(\sqrt{E_b/N_0})$. This is $3$ dB worse than BPSK, because the two signals are orthogonal and not antipodal.
- Noncoherent binary FSK: $P_b = \tfrac12 e^{-E_b/(2N_0)}$.
- Noncoherent $M$-ary FSK: the symbol error rate is
$$P_s = \sum_{n=1}^{M-1} (-1)^{n+1}\binom{M-1}{n}\frac{1}{n+1}\exp\Big(-\frac{n}{n+1}\frac{E_s}{N_0}\Big),$$
and every wrong tone is equally likely, so $P_b = \frac{M/2}{M-1}P_s$.

**Bandwidth and energy.** With the noncoherent spacing $1/T$, $M$ tones fill about $M/T$ hertz and carry $\log_2 M$ bits per $T$. So the [spectral efficiency](/spectral-efficiency/) falls as $M$ grows, while the $E_b/N_0$ needed for a given error rate also falls. With coherent detection, the error probability of $M$ orthogonal signals goes to zero as $M$ grows whenever $E_b/N_0 > \ln 2$, that is $-1.59$ dB. This is the opposite trade to [QAM](/quadrature-amplitude-modulation/) and [PSK](/phase-shift-keying/), which save bandwidth and spend energy.

## Examples and non-examples

**Binary FSK at 1000 symbols per second.** With $T = 1$ ms, a coherent receiver needs a spacing of at least $500$ Hz and a noncoherent receiver $1000$ Hz. At a spacing of $750$ Hz, $u = 0.75$: the coherent correlation is $E_s \sin(1.5\pi)/(1.5\pi) = -0.212\,E_s$, and the noncoherent one is $E_s\,|\mathrm{sinc}(0.75)| = 0.300\,E_s$. Neither receiver sees orthogonal tones.

**Error rates at $E_b/N_0 = 10$ dB.** Coherent BFSK has $P_b = Q(\sqrt{10}) = 7.83 \times 10^{-4}$. Noncoherent BFSK has $P_b = \tfrac12 e^{-5} = 3.369 \times 10^{-3}$. Noncoherent 4-FSK has $E_s/N_0 = 20$, $P_s = 6.66 \times 10^{-5}$ and $P_b = 4.44 \times 10^{-5}$: more tones give a lower error rate at the same $E_b/N_0$.

**Bell 103 modem.** The originating modem of this 300 bit/s telephone line modem sends $1070$ Hz for a space and $1270$ Hz for a mark. The spacing is $200$ Hz at $300$ symbols per second, so $h = 2/3$.

**Bluetooth Basic Rate.** It uses binary FSK with a Gaussian filter on the frequency pulse, $BT = 0.5$, and a modulation index between $0.28$ and $0.35$. The index is below $1/2$, so the tones are not orthogonal over one symbol, and a simple receiver uses a frequency discriminator instead of correlations.

**Non-example: MSK spacing with a noncoherent receiver.** At $\Delta f = 1/(2T)$ the tones are orthogonal for a coherent receiver, but $|\mathrm{sinc}(1/2)| = 2/\pi = 0.637$. A receiver that does not know the phase cannot separate them with one-symbol correlations.

**Non-example: chirps.** A chirp sweeps its frequency inside each symbol. Chirp spread spectrum signals select a starting frequency or a sweep, not one constant tone, so they are not FSK in the sense above.

## Related definitions

- [Continuous phase modulation](/continuous-phase-modulation/): the family that contains continuous-phase FSK, with smooth frequency pulses and pulses longer than one symbol.
- [Minimum-shift keying](/minimum-shift-keying/): binary continuous-phase FSK with $h = 1/2$, the smallest coherent spacing.
- [Gaussian minimum-shift keying](/gaussian-minimum-shift-keying/): MSK with a Gaussian-filtered frequency pulse.
- [Noncoherent detection](/noncoherent-detection/): the square-law and envelope receivers for FSK without a phase reference.
- [Frequency-hopping spread spectrum](/frequency-hopping-spread-spectrum/): it often uses $M$-FSK with noncoherent detection inside each hop.
- [Bit error rate](/bit-error-rate/): the error rates above next to those of PSK and QAM.

## References
