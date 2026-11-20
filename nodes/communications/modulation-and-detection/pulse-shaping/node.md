---
tag: 3AE22G
kind: technique
slug: pulse-shaping
name: Pulse shaping
aliases:
- transmit pulse shaping
area: communications/modulation-and-detection
level: intro
summary: "Send each symbol as a smooth pulse instead of a rectangle. The pulse sets the spectrum of the signal, and with a matched receive filter it can also remove intersymbol interference."
prereqs: [digital-modulation, intersymbol-interference]
see_also: [raised-cosine-filter, root-raised-cosine-filter, nyquist-isi-criterion, matched-filter, eye-diagram, spectral-efficiency, polyphase-decomposition, peak-to-average-power-ratio]
sources:
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008
    locator: Chapter 3 (the power spectrum of linearly modulated signals) and Section 9.2-1 (the design of band-limited signals for no intersymbol interference, with the transmit and the receive filter)
  - book: isbn:9780521879071
    title: Robert G. Gallager, Principles of Digital Communication, Cambridge University Press, 2008
    locator: Chapter 6 (pulse amplitude modulation, the Nyquist criterion and orthonormal pulse shifts) and Chapter 7 (modulation onto a carrier)
---

Pulse shaping is the choice of the waveform that carries each symbol of a linear modulation. The transmitter sends $s(t) = \sum_k a_k\, g(t - kT)$, so the pulse $g$ alone sets the shape of the spectrum, and $g$ together with the receive filter sets the [intersymbol interference](/intersymbol-interference/) at the sampling instants. The usual choice is a [root-raised-cosine filter](/root-raised-cosine-filter/) at both ends, which keeps the signal inside a band of $(1 + \beta)/T$ and gives samples without ISI.

## In plain words

A transmitter has a list of numbers to send, one every symbol period. The simplest way is to hold each number for one period, which gives a signal with sharp steps. Sharp steps spread the signal over a very wide band, and that disturbs the users in the next channels. Pulse shaping replaces each step with a smooth bump. A smooth bump has a narrow spectrum, but it is longer than one period, so the bumps overlap in time. The trick is to choose the bump so that, after the filter at the receiver, the overlapping tails all pass through zero at the moments when the receiver reads the signal. Then each reading holds only its own number, while the signal still fits in a narrow band.

## When it applies

- Linear modulations: [PAM](/pulse-amplitude-modulation/), [PSK](/phase-shift-keying/), [QAM](/quadrature-amplitude-modulation/) and [APSK](/amplitude-and-phase-shift-keying/), where the signal is a sum of shifted copies of one pulse, scaled by the symbols.
- A channel with a fixed band, or a spectral mask that limits the power outside the assigned channel.
- A receiver that can apply its own filter and sample once per symbol at a known time, which needs [symbol timing recovery](/symbol-timing-recovery/).
- It does not apply in the same form to constant-envelope schemes such as [continuous-phase modulation](/continuous-phase-modulation/), where a pulse shapes the frequency, not the amplitude.

## The template

The holes are the transmit pulse PULSE (its taps $g[n] = g(nT/L_s)$), the number $L_s$ of samples per symbol, and the receive filter RECEIVE. The usual fill is an RRC pulse for both. The symbols $a_0, \ldots, a_{N-1}$ are complex numbers from the constellation.

```pseudo id=main
PULSE-SHAPED-LINK(a_0, ..., a_{N-1})        ▷ holes: PULSE g, L_s, RECEIVE q
L1  x ← N · L_s zeros
L2  for k = 0 to N - 1 do
L3      x[k · L_s] ← a_k                    ▷ upsample: a symbol, then L_s - 1 zeros
L4  s ← x convolved with g                  ▷ the transmit signal at L_s samples per symbol
L5  r ← CHANNEL(s)
L6  z ← r convolved with q                  ▷ q is usually g matched: q[n] = g[-n]*
L7  D ← the delay of g plus the delay of q   ▷ S · L_s each for filters of 2 S L_s + 1 taps
L8  for k = 0 to N - 1 do
L9      y_k ← z[D + k · L_s]                ▷ one sample per symbol, at the peak of the pair
L10 return y_0, ..., y_{N-1}
```

**The spectrum.** If the symbols are independent, with mean zero and variance $\sigma_a^2$, the power spectral density of $s(t) = \sum_k a_k g(t - kT)$ is

$$S_s(f) = \frac{\sigma_a^2}{T}\, |G(f)|^2.$$

The cross terms average to zero because the symbols are uncorrelated, so each pulse adds its own energy spectrum $|G(f)|^2$, and there is one pulse every $T$ seconds. So the [power spectral density](/power-spectral-density/) has the shape of $|G|^2$, whatever the constellation. On a carrier, the spectrum moves to $\pm f_c$ and the band doubles.

**No ISI.** The sample $y_k$ in line L9 is $\sum_i a_i\, p((k - i)T) + w_k$ with $p = g * c * q$ the overall response. It has no ISI when $p$ meets the [Nyquist ISI criterion](/nyquist-isi-criterion/). With an ideal channel and $q$ the [matched filter](/matched-filter/) of $g$, $p$ has the spectrum $|G(f)|^2$, and the condition is $\sum_m |G(f - m/T)|^2 = T$. The RRC pulse meets it, since $|G|^2$ is a [raised cosine](/raised-cosine-filter/). The matched filter also gives the largest SNR at the sampling instant, and the noise samples stay white.

**The sample rate.** The sampled signal in line L4 must hold the whole band, so $L_s/T > (1 + \beta)/T$, and $L_s \ge 2$ for any $\beta \le 1$. Values of $4$ to $8$ leave room for the analog filter after the digital-to-analog converter.

**Cost.** A filter with $2 S L_s + 1$ taps costs that many multiplications per output sample if it is applied as written. Most inputs in line L4 are zeros; a [polyphase](/polyphase-decomposition/) filter skips them and needs about $2S + 1$ multiplications per output sample, or $(2S + 1)L_s$ per symbol.

**Worked example.** QPSK at $1$ million symbols per second, $\beta = 0.25$, $L_s = 8$, span $S = 8$. Each RRC filter has $129$ taps and a delay of $64$ samples; line L7 gives $D = 128$. The signal occupies $1.25$ MHz around the carrier. With an ideal channel and no noise, the samples $y_k$ equal the symbols up to a residual ISI of $5.43 \times 10^{-4}$ times the symbol amplitude, which comes from truncating the filters to $8$ symbols on each side.

## Classic examples

- **Root raised cosine in satellite and cellular links.** DVB-S uses the [root-raised-cosine filter](/root-raised-cosine-filter/) with $\beta = 0.35$, DVB-S2 adds $0.25$ and $0.20$, and UMTS uses $0.22$.
- **The rectangular pulse.** Holding each symbol for $T$ gives $|G(f)|^2 \propto \mathrm{sinc}^2(fT)$, with $\mathrm{sinc}(x) = \sin(\pi x)/(\pi x)$. Only $90.3\%$ of the power is within $|f| < 1/T$, the first sidelobe is $13.3$ dB below the peak, and the sidelobes fall only as $1/f^2$. [OFDM](/orthogonal-frequency-division-multiplexing/) uses a rectangular pulse on each subcarrier and fixes the spectrum in other ways.
- **The half-sine pulse.** [Minimum-shift keying](/minimum-shift-keying/) is [offset QPSK](/offset-qpsk/) with a half-sine pulse of length $2T$ on each branch, which gives a constant envelope.
- **The Gaussian filter.** [GMSK](/gaussian-minimum-shift-keying/), used in GSM, shapes the frequency pulse with a Gaussian filter and accepts some ISI for a compact spectrum.
- **Controlled ISI.** [Partial-response signaling](/partial-response-signaling/) uses a pulse such as $\mathrm{sinc}(t/T) + \mathrm{sinc}(t/T - 1)$, which reaches the minimum bandwidth $1/(2T)$ with a smooth spectrum and a known ISI.

## Variations

- **Roll-off.** A smaller $\beta$ narrows the band; a larger one shortens the pulse, widens the eye in time and lowers the peaks of the signal.
- **Windowed or optimized pulses.** Truncating the RRC with a window from the [window functions](/window-functions/) lowers the far sidelobes. A filter design such as the [Parks-McClellan algorithm](/parks-mcclellan-algorithm/) can trade a small ISI for a tighter spectrum.
- **Split between the ends.** The RRC split is optimal for white noise. With a fixed receive filter, or with colored noise, the split moves; in the extreme, a raised cosine at the transmitter and a wide filter at the receiver also give no ISI, but lose SNR.
- **Faster than Nyquist.** [Faster-than-Nyquist signaling](/faster-than-nyquist-signaling/) keeps the pulse and sends the symbols more often than $1/T$, with ISI by design.
- **Rate change in the same filter.** In receivers the matched filter is often part of a [polyphase resampler](/polyphase-resampling/) that also changes the sample rate.

## Pitfalls

- **One RRC filter without its match.** The RRC alone is not a Nyquist pulse: for $\beta = 0.5$ its sample at $t = T$ is $-9.3\%$ of the peak. The ISI only goes away after the receive filter.
- **Wrong delay.** Sampling at a delay other than $D$ in line L9 reads the pulse away from its zeros and adds ISI. With an even number of taps, the delay is not a whole number of samples.
- **Too short a filter.** A span of $2$ or $3$ symbols on each side raises the sidelobes and the residual ISI. Check both against the spectral mask and the error rate.
- **Energy.** The taps set the energy per symbol. Scale them to unit energy so that $E_s$ is the constellation energy, or the measured $E_s/N_0$ will be wrong.
- **Peaks and the amplifier.** A smaller $\beta$ raises the [peak-to-average power ratio](/peak-to-average-power-ratio/) of the signal: for QPSK with RRC pulses the peak is about $1.46$ times the rms value at $\beta = 0.5$ and $1.56$ times at $\beta = 0.35$. A nonlinear amplifier clips the peaks and spreads the spectrum again.
- **A mismatched roll-off.** The two ends must use the same $\beta$; otherwise $|G|^2$ is not a raised cosine and the samples have ISI.

## Exercises

1. Show that $s(t) = \sum_k a_k\, g(t - kT)$ with independent symbols of mean zero and variance $\sigma_a^2$ has the power spectral density $(\sigma_a^2/T)|G(f)|^2$. (Average over a random time shift uniform on $[0, T)$ to make the process stationary.)
2. For the rectangular pulse of length $T$, compute the fraction of the power in $|f| < 1/T$. (About $0.903$.)
3. A link sends $2$ Mbit/s with QPSK in a channel $1.2$ MHz wide. What is the largest roll-off of an RRC pulse that fits? (The symbol rate is $1$ million per second and the band is $(1 + \beta)$ MHz, so $\beta \le 0.2$.)
4. With $L_s = 4$ and a span of $6$ symbols on each side, how many taps does the filter have, and how many multiplications per symbol does it cost in direct form and in polyphase form? ($49$ taps; $196$ and about $49$.)
5. Show that if $g$ is a Nyquist pulse and the receiver uses the matched filter $g(-t)$, the overall pulse $g * g(-\cdot)$ is in general not a Nyquist pulse. What property must $|G|^2$ have instead?

## References
