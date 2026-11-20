---
tag: EG0TE4
kind: concept
slug: intersymbol-interference
name: Intersymbol interference
aliases:
- ISI
area: communications/modulation-and-detection
level: intro
summary: "The part of each received sample that comes from other symbols than the one being read. Band limits, multipath echoes, filters and timing errors cause it."
prereqs: [pulse-amplitude-modulation, discrete-convolution]
see_also: [nyquist-isi-criterion, eye-diagram, channel-equalization, pulse-shaping, partial-response-signaling, faster-than-nyquist-signaling, tapped-delay-line-channel-model, maximum-likelihood-sequence-estimation]
sources:
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008
    locator: Chapter 9 (digital communication through band-limited channels), Section 9.1 (characterization of band-limited channels) and Section 9.2 (signal design for no intersymbol interference and for controlled intersymbol interference)
  - paper: "R. W. Lucky, Automatic equalization for digital communication, Bell System Technical Journal 44(4), 1965"
    locator: pp. 547 to 588 (the peak distortion of a sampled response and the zero-forcing adjustment of a tapped delay line that minimizes it)
  - paper: "G. David Forney, Jr., Maximum-likelihood sequence estimation of digital sequences in the presence of intersymbol interference, IEEE Transactions on Information Theory 18(3), 1972"
    locator: pp. 363 to 378 (the discrete model of a channel with intersymbol interference, the whitened matched filter and the Viterbi search over the state of the channel)
  - book: isbn:9780521845274
    title: David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005
    locator: Chapter 2 (the discrete-time baseband model of a multipath channel, with one tap for each resolvable delay)
---

Intersymbol interference (ISI) is the part of a received sample that comes from symbols other than the one the receiver is reading. In a link that sends one pulse every $T$ seconds, it appears when the overall response from the symbols to the sampler is not zero at the other sampling instants. Its causes are a channel band that is too narrow for the symbol rate, multipath echoes that last longer than a fraction of a symbol, filters, and errors in the sampling time. The [Nyquist ISI criterion](/nyquist-isi-criterion/) says which pulses avoid it, and [channel equalization](/channel-equalization/) removes it after the channel.

## In plain words

Each symbol goes out as a short pulse. A real channel smears every pulse in time: a narrow band rounds it off, and echoes add late copies. So the tail of one pulse is still there when the receiver reads the next one, and the next after that. Each reading then holds its own symbol plus a mix of the neighbors. The mix depends on the data, so it acts like extra noise that does not go away when the real noise goes down. A receiver can live with it in three ways. It can choose pulses whose tails pass through zero at each reading time. It can undo the smear with a filter. Or it can take the smear into account and guess the whole sequence of symbols at once.

## The idea

**The discrete model.** Let the symbols be $a_k$, sent with the transmit pulse $g_T(t)$ through a channel with impulse response $c(t)$ and a receive filter $g_R(t)$. The overall response is the [convolution](/discrete-convolution/) $p = g_T * c * g_R$. Sampling at $t = kT$ (after a fixed delay) gives

$$y_k = \sum_i a_i\, p((k - i)T) + w_k = h_0 a_k + \underbrace{\sum_{i \ne 0} h_i a_{k - i}}_{\text{ISI}} + w_k, \qquad h_i = p(iT).$$

The numbers $h_i$ are the taps of the discrete channel at one sample per symbol. If $g_R$ is the [matched filter](/matched-filter/) of $g_T * c$ followed by a whitening filter, the noise $w_k$ is white; the [tapped delay line model](/tapped-delay-line-channel-model/) gives the same form for a multipath channel. The taps with $i > 0$ are *postcursors* (the tail of earlier symbols) and the taps with $i < 0$ are *precursors*.

**No ISI.** The ISI term is zero for every data sequence exactly when $h_i = 0$ for all $i \ne 0$. By the [Nyquist ISI criterion](/nyquist-isi-criterion/) this holds exactly when the spectrum of $p$, folded at multiples of $1/T$, is flat.

**Peak distortion.** For data with $|a_k| \le A_{\max}$, the ISI term is at most $A_{\max} \sum_{i \ne 0} |h_i|$ in absolute value, and some data sequence reaches this bound. Lucky called the ratio

$$D = \frac{1}{|h_0|} \sum_{i \ne 0} |h_i|$$

the peak distortion. For 2-PAM with $a_k = \pm 1$, the noiseless samples stay on the correct side of the threshold $0$ for every data sequence exactly when $D < 1$; then the [eye diagram](/eye-diagram/) is open at the sampling instant, with a vertical opening of $|h_0|(1 - D)$ on each side.

**ISI is not noise.** The ISI term depends on the data, so it does not shrink when the noise power falls. A symbol-by-symbol detector that treats it as noise has an error floor when $D \ge 1$. An optimal sequence detector can do better: [maximum-likelihood sequence estimation](/maximum-likelihood-sequence-estimation/) treats the channel memory as a state and searches with the [Viterbi algorithm](/viterbi-algorithm/), as on the [Viterbi equalizer](/viterbi-equalizer/) page. No detector does better at high SNR than the *matched filter bound*, the error rate of a single symbol sent alone with the full energy $\sum_i |h_i|^2$ of the response.

**Where the ISI comes from.**
- A channel band narrower than $1/(2T)$: by the corollary of the Nyquist criterion, every pulse in that band has ISI.
- Multipath: an echo with a delay $\tau$ adds a tap about $\tau/T$ symbols later. A channel whose [delay spread](/delay-spread/) is a sizable fraction of $T$ or more has several taps. In frequency, the channel response then varies across the band, which is the frequency-selective fading of [multipath fading](/multipath-fading/).
- Filters: a transmit and a receive filter that do not form a Nyquist pair, a truncated pulse, or a single [root-raised-cosine filter](/root-raised-cosine-filter/) used alone.
- Timing: sampling at $kT + \delta$ instead of $kT$ reads the pulse off its zeros. The taps become $p(iT + \delta)$, which are not zero for $i \ne 0$ even for a Nyquist pulse. [Symbol timing recovery](/symbol-timing-recovery/) keeps $\delta$ small.

## Examples

**Two taps, 2-PAM.** Let $h_0 = 1$, $h_1 = 0.5$ and $a_k = \pm 1$, with real noise of variance $\sigma^2 = N_0/2$. The noiseless sample $a_k + 0.5\, a_{k-1}$ takes the values $\pm 1.5$ (when the two symbols agree) and $\pm 0.5$ (when they differ). The peak distortion is $D = 0.5$, so the eye is open with half its height. With a threshold at $0$ and equally likely data, the bit error rate is

$$P_b = \tfrac{1}{2}\, Q\!\left(\frac{1.5}{\sigma}\right) + \tfrac{1}{2}\, Q\!\left(\frac{0.5}{\sigma}\right),$$

where $Q$ is the [Gaussian Q function](/gaussian-q-function/). Take $E_b/N_0 = 8$ dB with $E_b = h_0^2 = 1$, so $\sigma^2 = 1/(2 \cdot 10^{0.8})$. Without the second tap, $P_b = Q(\sqrt{2 E_b/N_0}) = 1.9091 \times 10^{-4}$. With it, the formula gives $P_b = 0.018926$, about 100 times worse, almost all of it from the term with $0.5/\sigma$. The matched filter bound uses the energy $1 + 0.25 = 1.25$ and gives $Q(\sqrt{2 \cdot 1.25\, E_b/N_0}) = 3.569 \times 10^{-5}$. A sequence detector comes close to this bound at high SNR; the simple slicer is far from it.

**A channel that closes the eye.** With $h_0 = 1$, $h_1 = 0.6$ and $h_2 = 0.5$, the peak distortion is $D = 1.1 > 1$. The data $a_k = +1$, $a_{k-1} = a_{k-2} = -1$ give the noiseless sample $1 - 0.6 - 0.5 = -0.1$, on the wrong side of $0$. A slicer makes this error even without noise, so its error rate has a floor; a [zero-forcing equalizer](/zero-forcing-equalizer/) or a sequence detector is needed.

**Multipath at a given rate.** A two-ray channel with an echo $2\ \mu\mathrm{s}$ after the direct path, at $1$ million symbols per second ($T = 1\ \mu\mathrm{s}$), has taps at $0$ and $2$ symbols: three taps in the discrete model. The same echo at $10\,000$ symbols per second ($T = 100\ \mu\mathrm{s}$) is a fiftieth of a symbol and causes almost no ISI, but the two paths still add with a phase that depends on the carrier, which is flat fading. The rate decides whether multipath appears as ISI.

**A timing error.** The sinc pulse $p(t) = \mathrm{sinc}(t/T)$ has no ISI at $t = kT$. At $t = kT + 0.1T$ the taps are $\mathrm{sinc}(i + 0.1)$, and $\sum_{i \ne 0} |\mathrm{sinc}(i + 0.1)| = (\sin(0.1\pi)/\pi) \sum_{i \ne 0} 1/|i + 0.1|$ diverges like the harmonic series. So for long data the peak distortion of the sinc pulse is unbounded at any timing error. Pulses with excess bandwidth, such as the [raised-cosine filter](/raised-cosine-filter/), decay faster and keep $D$ small.

## Where it is used

- Pulse design: [pulse shaping](/pulse-shaping/), the [Nyquist ISI criterion](/nyquist-isi-criterion/), the [raised-cosine filter](/raised-cosine-filter/) and the [root-raised-cosine filter](/root-raised-cosine-filter/) avoid ISI at the sampling instants.
- Measurement: the [eye diagram](/eye-diagram/) shows the ISI of a link and its timing margin.
- Removal: the [channel equalization](/channel-equalization/) problem, with the [zero-forcing equalizer](/zero-forcing-equalizer/), the [decision-feedback equalizer](/decision-feedback-equalizer/) and the [Viterbi equalizer](/viterbi-equalizer/). [OFDM](/orthogonal-frequency-division-multiplexing/) avoids it with a [cyclic prefix](/cyclic-prefix/) longer than the channel.
- Deliberate ISI: [partial-response signaling](/partial-response-signaling/) adds a known amount to reach the minimum bandwidth with practical filters, and [faster-than-Nyquist signaling](/faster-than-nyquist-signaling/) sends pulses closer than the Nyquist spacing.
- Precoding: [Tomlinson-Harashima precoding](/tomlinson-harashima-precoding/) cancels postcursor ISI at the transmitter.

## References
