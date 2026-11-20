---
tag: 1EJYTM
kind: definition
slug: gaussian-minimum-shift-keying
name: Gaussian minimum-shift keying
aliases:
- GMSK
area: communications/modulation-and-detection
level: core
summary: MSK whose frequency pulse is first passed through a Gaussian filter, which narrows the spectrum at the cost of controlled intersymbol interference.
prereqs: [minimum-shift-keying, continuous-phase-modulation]
see_also: [minimum-shift-keying, continuous-phase-modulation, laurent-decomposition, gaussian-filter, intersymbol-interference, maximum-likelihood-sequence-estimation, power-spectral-density, frequency-shift-keying]
sources:
  - paper: doi:10.1109/TCOM.1981.1095089
    title: Kazuaki Murota and Kenkichi Hirade, GMSK modulation for digital mobile radio telephony, IEEE Transactions on Communications 29(7), 1044-1050, 1981
    locator: the Gaussian premodulation filter, the spectra for several values of BT and the bit error rate of coherent detection
  - paper: doi:10.1109/TCOM.1986.1096504
    title: Pierre A. Laurent, Exact and approximate construction of digital phase modulations by superposition of amplitude modulated pulses (AMP), IEEE Transactions on Communications 34(2), 150-160, 1986
    locator: the decomposition of binary CPM into PAM pulses and the approximation by the main pulse
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008
    locator: Chapter 3 (CPM with Gaussian frequency pulses, GMSK)
---

Gaussian minimum-shift keying (GMSK) is binary [continuous phase modulation](/continuous-phase-modulation/) with modulation index $h = 1/2$, like [MSK](/minimum-shift-keying/), but its frequency pulse is the rectangular MSK pulse passed through a Gaussian lowpass filter. The smooth pulse makes the spectrum much narrower than that of MSK, and the signal keeps a constant envelope. The price is intersymbol interference on purpose: each bit changes the frequency over about three bit periods. GSM uses GMSK with $BT = 0.3$. By the [Laurent decomposition](/laurent-decomposition/), almost all the energy of GMSK is in one linear pulse, so a receiver can treat it as a linear modulation with a short channel.

## Definition

Let $T$ be the bit period, $B$ the 3 dB bandwidth of the Gaussian filter and $a_n \in \{+1, -1\}$ the data. The Gaussian filter has the transfer function $H(f) = \exp\big(-\frac{\ln 2}{2}\frac{f^2}{B^2}\big)$, so $|H(B)|^2 = 1/2$. Its impulse response is a Gaussian with standard deviation

$$\sigma = \frac{\sqrt{\ln 2}}{2\pi B}.$$

The filter acts on the MSK frequency pulse, the rectangle of height $1/(2T)$ on $[-T/2, T/2]$. The result is the **GMSK frequency pulse**

$$g(t) = \frac{1}{2T}\Big[Q\Big(\frac{t - T/2}{\sigma}\Big) - Q\Big(\frac{t + T/2}{\sigma}\Big)\Big],$$

where $Q$ is the [Gaussian Q function](/gaussian-q-function/). Its area is $1/2$, as CPM needs. The pulse has no end, so a transmitter cuts it to a length $LT$ around its center and shifts it by $LT/2$ to start at $0$. The **GMSK signal** is the CPM signal $e^{j\phi(t)}$ with this pulse and $h = 1/2$:

$$\phi(t) = \pi\sum_i a_i\, q(t - iT), \qquad q(t) = \int_{-\infty}^{t} g(\tau)\, d\tau.$$

The product $BT$ sets the shape. As $BT \to \infty$, $g$ becomes the rectangle and GMSK becomes MSK. A small $BT$ gives a wide, low pulse: a narrow spectrum but more interference between bits.

**The phase trellis.** With $h = 1/2$ and a pulse of $L$ bits, the trellis has $4 \cdot 2^{L-1}$ states: four phase states and the last $L - 1$ bits. A [maximum likelihood sequence](/maximum-likelihood-sequence-estimation/) receiver runs the Viterbi algorithm on it.

**The linear approximation.** The Laurent decomposition writes binary CPM as a sum of $2^{L-1}$ PAM signals. For GMSK the first pulse $c_0$ carries almost all the energy, and its symbols are $j^{A_n}$ with $A_n = \sum_{i \le n} a_i$, as for MSK. So GMSK is close to offset QPSK with the pulse $c_0$ and differentially encoded data. A receiver can use a linear equalizer or a small Viterbi equalizer on this model.

## Examples and non-examples

**The pulse at $BT = 0.3$.** Here $\sigma = 0.442\,T$. The peak of $g$ is $0.371/T$, against $0.5/T$ for the MSK rectangle. Cut to $L = 3$ bits, the pulse keeps an area of $0.49820$, that is $99.64\%$ of $1/2$; cut to $L = 4$ bits, $0.499961$, that is $99.992\%$. The transmitter scales the cut pulse back to the area $1/2$.

**Energy in the main Laurent pulse.** For $BT = 0.3$, the pulse $c_0$ holds $99.63\%$ of the total energy of the eight pulses with $L = 4$ and $c_1$ holds $0.37\%$; the other six pulses hold less than $10^{-5}$ together. For $BT = 0.25$ the share of $c_0$ is $99.20\%$, and for $BT = 0.5$ with $L = 3$ it is $99.97\%$. These values come from a numerical integration of the pulses of the Laurent decomposition with the cut and rescaled pulse.

**GSM.** GSM sends $270.833$ kbit/s in channels $200$ kHz apart with GMSK at $BT = 0.3$. The EDGE extension of GSM keeps the main Laurent pulse of this GMSK as the transmit pulse of its 8-PSK mode, so both modes have about the same spectrum.

**Non-example: Bluetooth Basic Rate.** It uses a Gaussian frequency pulse with $BT = 0.5$, but its modulation index is between $0.28$ and $0.35$, not $1/2$. It is Gaussian FSK, a CPM, but not GMSK.

**Non-example: Gaussian-filtered BPSK.** If the Gaussian filter acts on the amplitude of a BPSK signal, the envelope is no longer constant. GMSK filters the frequency, not the amplitude.

## Related definitions

- [Minimum-shift keying](/minimum-shift-keying/): the limit $BT \to \infty$.
- [Continuous phase modulation](/continuous-phase-modulation/): the family; GMSK is binary, $h = 1/2$, with a Gaussian pulse of $L$ bits.
- [Laurent decomposition](/laurent-decomposition/): the theorem behind the linear approximation by the pulse $c_0$.
- [Gaussian filter](/gaussian-filter/): the same Gaussian kernel, used here on the frequency pulse.
- [Intersymbol interference](/intersymbol-interference/): GMSK has it by design, over about $L = 3$ bits at $BT = 0.3$.
- [Power spectral density](/power-spectral-density/): it narrows as $BT$ decreases.

## References
