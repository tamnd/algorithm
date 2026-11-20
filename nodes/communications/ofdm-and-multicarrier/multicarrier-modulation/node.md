---
tag: YP1Q82
kind: concept
slug: multicarrier-modulation
name: Multicarrier modulation
aliases:
- MCM
area: communications/ofdm-and-multicarrier
level: intro
summary: "Splits a wideband stream into many narrowband subcarriers, each so narrow that the channel looks flat on it."
prereqs: [intersymbol-interference, multipath-fading]
see_also: [orthogonal-frequency-division-multiplexing, discrete-multitone, filter-bank-multicarrier, coherence-bandwidth, delay-spread, water-filling-power-allocation, bit-loading, channel-capacity]
sources:
  - book: isbn:9780521837163
    title: "Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005"
    locator: "Chapter 12, Sections 12.1 (data transmission using multiple carriers), 12.2 (multicarrier modulation with overlapping subchannels) and 12.3 (mitigation of subcarrier fading, with adaptive loading in 12.3.4)"
  - paper: doi:10.1002/j.1538-7305.1966.tb02435.x
    title: "R. W. Chang, Synthesis of band-limited orthogonal signals for multichannel data transmission, Bell System Technical Journal 45(10), 1966"
    locator: "pages 1775 to 1796 (band-limited subchannels whose spectra overlap and that stay orthogonal)"
  - paper: doi:10.1109/35.54342
    title: "J. A. C. Bingham, Multicarrier modulation for data transmission: an idea whose time has come, IEEE Communications Magazine 28(5), 1990"
    locator: "pages 5 to 14 (a survey of multicarrier modulation, its DFT implementation and the loading of bits on the subchannels)"
  - paper: doi:10.1109/TCOM.1971.1090705
    title: "S. B. Weinstein and P. M. Ebert, Data transmission by frequency-division multiplexing using the discrete Fourier transform, IEEE Transactions on Communication Technology 19(5), 1971"
    locator: "pages 628 to 634 (the DFT as the modulator and the demodulator of all subchannels)"
---

Multicarrier modulation (MCM) divides one data stream of rate $R$ symbols per second into $N$ substreams of rate $R/N$ and sends each substream on its own carrier frequency, a subcarrier. Each subcarrier then uses a bandwidth of about $B/N$ out of the total bandwidth $B$, and its symbols last $N$ times longer than the symbols of a single carrier. If $B/N$ is small compared with the [coherence bandwidth](/coherence-bandwidth/) of the channel, the channel gain is almost constant across each subcarrier, so a [multipath](/multipath-fading/) channel that would cause [intersymbol interference](/intersymbol-interference/) on one fast carrier becomes $N$ slow, flat channels. The receiver then needs only one gain per subcarrier instead of a long equalizer. [OFDM](/orthogonal-frequency-division-multiplexing/) is the form of MCM in which the subcarriers overlap in frequency, stay orthogonal, and are generated with one FFT; [discrete multitone](/discrete-multitone/) is its real-valued form for wires. The page uses $j$ for the imaginary unit.

## In plain words

A road with potholes is easy to drive slowly and hard to drive fast. A radio channel with echoes is like that: if symbols are short, the echo of one symbol lands on the next ones. Multicarrier modulation sends many slow streams side by side instead of one fast stream. Each stream gets a thin slice of the band, and its symbols are so long that an echo only blurs a small part of each one. In a thin slice the channel also has almost the same strength everywhere, so the receiver fixes each stream with one simple correction. Some slices may be weak, but the sender can put less data on them or protect them with a code that spreads the data across many slices.

## The idea

**Flat subchannels.** Let the channel have the delay spread $\sigma_\tau$ and the coherence bandwidth $B_c$. The rule $B_c \approx 1/(5 \sigma_\tau)$ is a rule of thumb, not a theorem. A single carrier with bandwidth $B \gg B_c$ sees a gain that changes strongly across its band, and its intersymbol interference spans about $\sigma_\tau B$ symbols or more. MCM chooses $N$ so that $B/N < B_c$. Then each subcarrier sees a nearly flat channel $Y_k = H_k X_k + W_k$, and its symbol time $N/B$ is long compared with the delay spread.

**Non-overlapping and overlapping subchannels.** The oldest form puts each subcarrier in its own band, with filters and guard bands between them, as in frequency-division multiplexing. This wastes bandwidth and needs $N$ sharp filters. Chang showed in 1966 that subchannels can overlap in frequency and still not interfere, if their signals are orthogonal over a symbol. With rectangular pulses of length $T$ and subcarrier spacing $1/T$, each subcarrier has a spectrum $\operatorname{sinc}((f - f_k) T)$ that is zero at the centers of all the others. Counting null to null, $N$ separate subcarriers with these pulses need about $2N/T$ of bandwidth, and $N$ overlapping ones need $(N + 1)/T$, close to half.

**A transform as the modulator.** For $N$ subcarriers at spacing $1/T$, the $N$ samples of one symbol are the inverse DFT of the $N$ data symbols. Weinstein and Ebert used this in 1971, so one FFT replaces $N$ oscillators. A [cyclic prefix](/cyclic-prefix/) then makes the subchannels exactly flat and exactly orthogonal over a channel with a finite impulse response, which is the OFDM algorithm.

**Weak subcarriers.** A frequency-selective channel gives different SNRs on different subcarriers. Goldsmith lists the ways to handle this: code across subcarriers, so that a few weak ones do not lose data; precode or equalize per subcarrier; or adapt the power and the number of bits per subcarrier, which is [bit loading](/bit-loading/). With known gains and a total power limit, the power allocation that maximizes the total rate is [water-filling](/water-filling-power-allocation/). The same parallel-channel view, with water-filling over frequency, is the standard way to compute the [channel capacity](/channel-capacity/) of a Gaussian channel with intersymbol interference.

**Costs.** Long symbols make MCM sensitive to anything that changes during a symbol: a carrier frequency offset or Doppler breaks the orthogonality and causes [inter-carrier interference](/inter-carrier-interference/). The sum of many subcarriers has a high [peak-to-average power ratio](/peak-to-average-power-ratio/). [Filter bank multicarrier](/filter-bank-multicarrier/) uses better pulses than the rectangle to make each subcarrier spectrum compact.

## Examples

**Echoes measured in symbols.** Take a band of 20 MHz and echoes that last $0.8\ \mu$s. A single carrier at 20 million symbols per second has symbols of 50 ns, so an echo reaches 16 symbols ahead, and an equalizer must handle 16 interfering symbols. With $N = 64$ subcarriers, each subcarrier carries 312.5 thousand symbols per second, its symbol lasts $3.2\ \mu$s, and the echo covers a quarter of one symbol. A cyclic prefix of $0.8\ \mu$s removes even that part, at a rate cost of $64/80 = 0.8$. These are the numbers of IEEE 802.11a.

**One gain per subcarrier.** The two-tap channel $h = (1, 0.5)$ at one tap per sample has the gains $H_k = 1 + 0.5\, e^{-j 2\pi k / N}$, whose size goes from $0.5$ to $1.5$ across the band. With $N = 64$ subcarriers and QPSK at $E_s / N_0 = 10$ dB, subcarrier $k$ has the SNR $|H_k|^2 E_s / N_0$, from $2.5$ to $22.5$. The average QPSK symbol error rate over the 64 subcarriers is $0.018549$, a closed form for this channel and a measured value of the OFDM code. A flat channel with the same mean gain has $1.5648 \times 10^{-3}$. So without coding or loading, the weak subcarriers set the error rate.

**Bandwidth of overlapping subchannels.** For $N = 16$ subcarriers with rectangular pulses of length $T$, separate subchannels need about $32/T$ of bandwidth null to null, and orthogonal overlapping ones need $17/T$.

## Where it is used

Multicarrier modulation in its OFDM form is the physical layer of IEEE 802.11 wireless LANs from 802.11a on, of LTE and 5G NR, and of digital audio and television broadcasting (DAB, DVB-T). Discrete multitone, the baseband form with bit loading, runs on telephone lines in ADSL and VDSL. Power line modems use it too. Filter bank forms are used in some cable and research systems. Bingham's 1990 survey gives the reasons it spread once the FFT became cheap.

## References
