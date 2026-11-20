---
tag: HMP9ST
kind: technique
slug: pulse-compression
name: Pulse compression
aliases:
- radar pulse compression
area: communications/radar-waveforms
level: core
summary: "Sends a long coded pulse and compresses its echo with a matched filter, which gives the energy of a long pulse and the resolution of a short one."
prereqs: [autocorrelation, matched-filter, discrete-convolution]
see_also: [ambiguity-function, linear-frequency-modulation-pulse, phase-coded-waveform, barker-code, mismatched-filter-design, window-functions, radar-range-equation, overlap-save-method]
sources:
  - paper: doi:10.1002/j.1538-7305.1960.tb03942.x
    title: "J. R. Klauder, A. C. Price, S. Darlington and W. J. Albersheim, The theory and design of chirp radars, Bell System Technical Journal 39(4), 1960"
    locator: "pp. 745 to 808 (the chirp pulse, its compression by the matched filter, the compression ratio, weighting for low sidelobes and the coupling of range and Doppler)"
  - book: isbn:9780471473787
    title: "Nadav Levanon and Eli Mozeson, Radar Signals, Wiley, 2004"
    locator: "Chapter 5, Frequency-Modulated Pulse, and Chapter 6, Phase-Coded Pulse"
  - book: isbn:9780071798327
    title: "Mark A. Richards, Fundamentals of Radar Signal Processing, second edition, McGraw-Hill, 2014"
    locator: "Chapter 4, Radar Waveforms (the matched filter, range resolution, the time bandwidth product, the chirp and phase codes)"
---

Pulse compression transmits a long pulse with a frequency or phase modulation inside it and passes the echo through a [matched filter](/matched-filter/), which compresses it into a peak about $1/B$ wide, where $B$ is the bandwidth. The detection depends on the energy of the long pulse, and the range resolution depends on the bandwidth, so a radar with a limited peak power can have both. The matched filter is the receiver, pulse compression is its use on a modulated pulse, and the [ambiguity function](/ambiguity-function/) describes the result for every delay and Doppler shift. The width of the pulse divided by the width of the compressed peak is the compression ratio, close to the time bandwidth product $TB$.

## In plain words

A radar must send much energy to see far, and short pulses to tell close targets apart. A short pulse with much energy needs a very high power, which the transmitter cannot give. So the radar sends a long pulse with a pattern inside it, for example a tone that rises in pitch, or a sequence of phase flips. The receiver knows the pattern. It slides a copy of the pattern along the echo and adds up the products. Where the echo and the copy line up, all the parts add in step and give a tall, narrow spike. Two targets close together give two separate spikes. The price is small bumps on each side of each spike, which special filters or weights can lower.

## When it applies

- The transmitter is limited in peak power, not in average power, as with solid state amplifiers and most tube transmitters at long range.
- The range resolution required, $\Delta R = c/(2B)$, needs more bandwidth than a plain pulse of the required energy can have, since a plain pulse of length $T$ has $B \approx 1/T$.
- The echo is close to a delayed copy of the transmitted pulse: the Doppler shift is small against the Doppler tolerance of the waveform, and the target is a point or a set of points.
- A blind zone of length $cT/2$ near the radar is acceptable, because the receiver is off while the long pulse is sent.
- Range sidelobes, at the level of the code or after weighting, are acceptable for the ratio of strong and weak echoes expected.

## The template

1. **Choose the bandwidth from the resolution.** $B = c/(2\Delta R)$. For $\Delta R = 149.9$ m this is 1 MHz, and for $\Delta R = 29.98$ m it is 5 MHz.
2. **Choose the length from the energy.** The output signal to noise ratio of the matched filter depends only on the energy $E = P T$, through the [radar range equation](/radar-range-equation/), not on the modulation. Choose $T$ to reach the energy at the peak power $P$, and check the blind zone $cT/2$.
3. **Choose a modulation with $TB \gg 1$.** A [linear frequency modulation pulse](/linear-frequency-modulation-pulse/) is Doppler tolerant and easy to make. A [phase-coded waveform](/phase-coded-waveform/) has low sidelobes without weighting for good codes and is easy to generate digitally. [Nonlinear frequency modulation](/nonlinear-frequency-modulation/) gives low sidelobes without a weighting loss.
4. **Compress.** Correlate the sampled echo with the conjugated pulse, by direct [convolution](/discrete-convolution/) for short pulses or with the FFT and the [overlap-save method](/overlap-save-method/) for long ones. Sample at a complex rate of at least $B$.
5. **Lower the sidelobes if needed.** Apply a [window](/window-functions/) in time or frequency to the reference, or replace it with a [mismatched filter](/mismatched-filter-design/). Both trade a loss in signal to noise ratio and a wider peak for lower sidelobes.
6. **Detect.** Threshold the magnitude of the output, for example with [CFAR detection](/cfar-detection/), and keep local peaks.

## Classic examples

**Linear FM.** $T = 10\ \mu$s and $B = 5$ MHz give $TB = 50$. A plain pulse of 10 µs resolves $cT/2 = 1499$ m, and the compressed pulse resolves $c/(2B) = 29.98$ m, 50 times better at the same energy. The sidelobes of the unweighted chirp follow a sinc, with the first at $-13.26$ dB. With a Hamming weight, the large $TB$ approximation gives a first sidelobe at $-42.7$ dB, a 3 dB peak width 1.47 times larger and a loss of 1.34 dB in signal to noise ratio (closed forms from the transform of the window).

**Barker code of length 13.** Thirteen chips of 1 µs, each with phase 0 or π, make a pulse of 13 µs with a bandwidth of about 1 MHz. The compressed peak is one chip wide, 149.9 m, against 1949 m for the plain pulse, a ratio of 13. The [Barker code](/barker-code/) has the autocorrelation $13, 0, 1, 0, 1, \dots$, so all range sidelobes are at $20 \log_{10}(1/13) = -22.28$ dB with no weighting and no loss.

**Polyphase codes.** A [Frank code](/frank-code/) of $N = M^2$ chips has a peak sidelobe level that falls as $M$ grows: $-21.07$ dB for 16 chips and $-29.80$ dB for 100 chips (measured from the code). It has a better Doppler tolerance than a binary code of the same length, because it is a step approximation of a chirp.

**Mismatched filter.** For the Barker code of length 13, a least squares filter of 39 taps gives a peak sidelobe of $-38.47$ dB at a loss of 0.204 dB, against $-22.28$ dB for the matched filter.

## Variations

- **Stretch processing.** For a very wide chirp over a short range window, mix the echo with a delayed copy of the chirp. Each range becomes a tone, and an FFT replaces the matched filter. This is the receiver of [FMCW radar](/fmcw-radar/).
- **Synthetic bandwidth.** A [stepped frequency waveform](/stepped-frequency-waveform/) sends narrow pulses at stepped carriers and builds the wide bandwidth over many pulses.
- **Doppler filter bank.** For fast targets with a code that is not Doppler tolerant, run one matched filter per Doppler shift, which samples the cross-ambiguity function of the echo.
- **Frequency hopping.** A pulse that hops through frequencies in the order of a [Costas array](/costas-array/) has an ambiguity function close to a thumbtack.
- **Analog compression.** Before digital processors, dispersive delay lines and surface acoustic wave devices made the matched filter of a chirp.

## Pitfalls

- **Doppler mismatch.** A Doppler shift $\nu$ rotates the phase by $2\pi\nu T$ across the pulse. Binary phase codes lose their peak and their low sidelobes when $\nu T$ is not small. A chirp keeps its peak but moves it in range, which is [range-Doppler coupling](/range-doppler-coupling/).
- **The blind zone.** The receiver cannot listen while it transmits, so targets closer than $cT/2$ are not seen: 1.5 km for a 10 µs pulse. Radars often add a short pulse for near ranges.
- **Sidelobes that mask small targets.** A target 20 dB weaker than its neighbor falls below the $-13.26$ dB sidelobes of an unweighted chirp. Weight the filter, use a better code, or use a mismatched filter.
- **Sampling too sparsely.** The compressed peak is about $1/B$ wide. With samples spaced $1/B$ apart, a target halfway between two samples loses $20\log_{10}(2/\pi) = -3.92$ dB on the sinc main lobe. Sample faster or interpolate.
- **Distortion in the hardware.** Amplitude and phase ripple in the transmitter and receiver add paired echoes and raise the sidelobes above the ones the waveform predicts.
- **Counting the weighting twice.** If the window is in both the transmitter and the receiver, or in the reference and again in the FFT, the loss and the widening are larger than planned.

## Exercises

1. A radar needs a range resolution of 15 m and an energy of 1 mJ from a transmitter of 200 W. Find $B$, $T$, $TB$ and the blind zone.
2. Show from the matched filter that the output signal to noise ratio of a pulse of energy $E$ does not depend on its modulation, so that compression changes the resolution but not the detection range.
3. Compute the autocorrelation of the Barker code of length 7, $(1, 1, 1, -1, -1, 1, -1)$, and its peak sidelobe level in dB.
4. For a chirp with $T = 10\ \mu$s and $B = 5$ MHz at a carrier of 10 GHz, find the range error for a target that approaches at 300 m/s.
5. Show that a window $w$ on the reference lowers the signal to noise ratio by the factor $(\sum w)^2 / (N \sum w^2)$ for a pulse of constant amplitude, and compute it in dB for a Hamming window of many samples.

## References
