---
tag: 6GEXZF
kind: definition
slug: continuous-phase-modulation
name: Continuous phase modulation
aliases:
- continuous-phase FSK
- CPFSK
area: communications/modulation-and-detection
level: core
summary: A constant-envelope modulation whose phase is a continuous function of the data, so it has memory and a trellis description.
prereqs: [frequency-shift-keying, digital-modulation]
see_also: [minimum-shift-keying, gaussian-minimum-shift-keying, laurent-decomposition, maximum-likelihood-sequence-estimation, viterbi-algorithm, trellis, power-spectral-density, frequency-shift-keying]
sources:
  - book: isbn:9780306421952
    title: John B. Anderson, Tor Aulin and Carl-Erik Sundberg, Digital Phase Modulation, Plenum Press, 1986
    locator: the CPM signal model, the minimum Euclidean distance and its upper bound, the power spectrum, and the maximum likelihood receivers
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008
    locator: Chapter 3 (continuous-phase FSK, CPM and its phase trellis, and the spectra of these signals) and Chapter 4 (the optimum receiver for CPM signals)
---

Continuous phase modulation (CPM) sends a signal of constant amplitude whose phase is a continuous function of time. The data changes the instantaneous frequency through a smooth frequency pulse, and the phase is the running integral of the frequency. Because the phase depends on all past symbols, the signal has memory, and a [trellis](/trellis/) with a finite number of states describes it when the modulation index is rational. The constant envelope lets the transmitter use a power amplifier in saturation, and the smooth phase gives a narrow spectrum. [Frequency-shift keying](/frequency-shift-keying/) with continuous phase is the simplest CPM. [Minimum-shift keying](/minimum-shift-keying/) and [Gaussian minimum-shift keying](/gaussian-minimum-shift-keying/) are the two most used members, and the [Laurent decomposition](/laurent-decomposition/) is the theorem that writes a CPM signal as a sum of linearly modulated pulses.

## Definition

Let $T$ be the symbol period, $E_s$ the energy per symbol, and $a_i \in \{\pm 1, \pm 3, \ldots, \pm(M - 1)\}$ the data symbols, with $M$ even. A **frequency pulse** $g(t)$ is zero outside $[0, LT]$ and has area $1/2$; the integer $L \ge 1$ is the **pulse length**. The **phase pulse** is

$$q(t) = \int_{-\infty}^{t} g(\tau)\, d\tau, \qquad q(t) = 0 \text{ for } t \le 0, \qquad q(t) = \tfrac12 \text{ for } t \ge LT.$$

The **CPM signal** in complex baseband is

$$s(t) = \sqrt{E_s/T}\; e^{j\phi(t)}, \qquad \phi(t) = 2\pi h \sum_{i} a_i\, q(t - iT),$$

where $j$ is the imaginary unit and $h > 0$ is the **modulation index**. The instantaneous frequency is $\phi'(t)/(2\pi) = h\sum_i a_i\, g(t - iT)$. Each symbol $a_i$ moves the phase by $\pi h a_i$ in total, spread over $L$ symbol periods. The signal is *full response* if $L = 1$ and *partial response* if $L > 1$.

Three pulses are common:
- **LREC**: $g(t) = 1/(2LT)$ on $[0, LT]$. With $L = 1$ this is continuous-phase FSK (CPFSK), the CPM subclass with rectangular frequency pulses: the frequency is constant in each symbol and the phase is linear.
- **LRC** (raised cosine): $g(t) = \frac{1}{2LT}\big(1 - \cos\frac{2\pi t}{LT}\big)$ on $[0, LT]$. The frequency is smooth too.
- **Gaussian**: a rectangular pulse of length $T$ filtered by a Gaussian filter of bandwidth $B$ and cut to a length $LT$; this gives GMSK.

**The phase trellis.** On the interval $nT \le t < (n+1)T$, the symbols with $i \le n - L$ have finished their phase pulses, so

$$\phi(t) = \theta_n + 2\pi h \sum_{i = n - L + 1}^{n} a_i\, q(t - iT), \qquad \theta_n = \pi h \sum_{i \le n - L} a_i \pmod{2\pi}.$$

The signal on this interval depends on $a_n$ and on the **state** $(\theta_n, a_{n-1}, \ldots, a_{n-L+1})$. Let $h = k/p$ with $k$ and $p$ coprime positive integers. Then $\theta_n$ is a multiple of $\pi k/p$ modulo $2\pi$, and it takes $p$ values if $k$ is even and $2p$ values if $k$ is odd. So the trellis has $pM^{L-1}$ or $2pM^{L-1}$ states and $M$ branches out of each state. With $k$ odd, only $p$ of the $2p$ phase values occur at each time, alternately. If $h$ is irrational, the number of phase states is infinite.

**Distance.** For two symbol sequences that differ from time $0$, the squared Euclidean distance between the signals, normalized by $2E_b$ with $E_b = E_s/\log_2 M$, is

$$d^2 = \frac{\log_2 M}{T}\int_0^{NT}\big(1 - \cos(\phi(t; \mathbf{a}) - \phi(t; \mathbf{b}))\big)\, dt$$

over an observation of $N$ symbols. In this normalization, BPSK and QPSK have $d^2 = 2$. For binary full response, the two sequences whose difference is $(2, -2, 0, 0, \ldots)$ merge after two symbols. For 1REC this pair gives

$$d_B^2(h) = 2\big(1 - \mathrm{sinc}(2h)\big), \qquad \mathrm{sinc}(x) = \frac{\sin \pi x}{\pi x},$$

an upper bound on the minimum distance of binary 1REC CPM. It is $2$ at $h = 1/2$, the value of BPSK, and it is largest, $2.43$, at $h = 0.715$, which is $0.85$ dB more than $2$.

**Receivers.** The maximum likelihood sequence detector runs the [Viterbi algorithm](/viterbi-algorithm/) on the phase trellis, with $M^L$ matched filters, one for each pattern of the $L$ active symbols, and the phase state added. This is [maximum likelihood sequence estimation](/maximum-likelihood-sequence-estimation/) on a trellis with $pM^{L-1}$ or $2pM^{L-1}$ states. Simpler receivers keep only the main pulses of the Laurent decomposition, or use a frequency discriminator.

## Examples and non-examples

**MSK.** Binary 1REC with $h = 1/2$. Here $k = 1$ is odd and $p = 2$, so the phase state takes $2p = 4$ values, $\{0, \pi/2, \pi, 3\pi/2\}$, and the trellis has $4$ states with $L = 1$. Each symbol turns the phase by $\pm\pi/2$ along a straight line.

**GMSK in GSM.** Binary, $h = 1/2$, Gaussian pulse with $BT = 0.3$, cut to $L = 3$ or $L = 4$ in practice. With $L = 3$ the trellis has $4 \cdot 2^2 = 16$ states.

**A weak index.** Binary 1REC with $h = 1$. The bound gives $d_B^2(1) = 2$, but the pair with difference $(2, 0, 0, \ldots)$ merges after one symbol, because the phase difference after one symbol is $2\pi h = 2\pi$. That pair has $d^2 = \int_0^1 (1 - \cos 2\pi x)\, dx = 1$. Integer $h$ also makes the spectrum contain discrete lines, so $h = 1$ is a poor choice.

**Partial response.** Binary 3RC with $h = 1/2$ has a much narrower spectrum than MSK. Its trellis has $4 \cdot 2^2 = 16$ states. Partial response trades distance for bandwidth at a given $h$; a larger $h$ can win the distance back.

**Multi-h CPM.** The index changes from symbol to symbol in a fixed cycle. Two paths then merge later, which raises the minimum distance. The aeronautical telemetry waveform ARTM CPM is quaternary 3RC with $h$ alternating between $4/16$ and $5/16$.

**Non-example: FSK with switched oscillators.** If each tone comes from a separate free-running oscillator, the phase jumps at every symbol boundary. The signal has a constant envelope between the jumps but is not CPM, and its spectrum falls only as $1/f^2$.

**Non-example: OQPSK with rectangular pulses.** The phase jumps by $\pm\pi/2$ at the half-symbol instants. With half-sine pulses instead, [offset QPSK](/offset-qpsk/) becomes MSK, which is CPM.

## Related definitions

- [Frequency-shift keying](/frequency-shift-keying/): the memoryless version; with continuous phase it is 1REC CPM.
- [Minimum-shift keying](/minimum-shift-keying/): 1REC with $h = 1/2$, the CPM that is also a linear modulation.
- [Gaussian minimum-shift keying](/gaussian-minimum-shift-keying/): $h = 1/2$ with a Gaussian frequency pulse.
- [Laurent decomposition](/laurent-decomposition/): binary CPM as an exact sum of $2^{L-1}$ PAM signals.
- [Maximum likelihood sequence estimation](/maximum-likelihood-sequence-estimation/): the optimum receiver on the phase trellis.
- [Power spectral density](/power-spectral-density/): smoother frequency pulses and longer $L$ make it fall faster.

## References
