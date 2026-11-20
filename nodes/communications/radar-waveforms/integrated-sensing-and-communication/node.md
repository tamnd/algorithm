---
tag: CWR0G3
kind: concept
slug: integrated-sensing-and-communication
name: Integrated sensing and communication
aliases:
- ISAC
- joint radar and communication
area: communications/radar-waveforms
level: research
summary: "One waveform, one transmitter and one band serve both radar sensing and data transmission. The design trades sensing accuracy against data rate."
prereqs: [orthogonal-frequency-division-multiplexing, range-doppler-processing]
see_also: [ambiguity-function, fmcw-radar, cramer-rao-bound, beamforming, massive-mimo, orthogonal-time-frequency-space-modulation, channel-estimation, reconfigurable-intelligent-surface]
sources:
  - paper: doi:10.1109/JSAC.2022.3156632
    title: "Integrated sensing and communications: toward dual-functional wireless networks for 6G and beyond"
    locator: "F. Liu, Y. Cui, C. Masouros, J. Xu, T. X. Han, Y. C. Eldar and S. Buzzi, IEEE Journal on Selected Areas in Communications 40(6), 2022, pp. 1728 to 1767 (a survey of the waveforms, the tradeoffs, the performance limits and the applications)"
  - paper: doi:10.1109/JPROC.2011.2131110
    title: "Waveform design and signal processing aspects for fusion of wireless communications and radar sensing"
    locator: "C. Sturm and W. Wiesbeck, Proceedings of the IEEE 99(7), 2011, pp. 1236 to 1259 (OFDM radar processing by division of the received symbols by the sent symbols)"
---

Integrated sensing and communication (ISAC) is the idea that one transmitter, one band and, in the strongest form, one waveform serve both radar sensing and data transmission. A base station that sends data to users also receives the echoes of that signal from cars, people and buildings, and estimates their range, speed and angle. A car radar can in the same way carry data to other cars. ISAC saves spectrum and hardware, and the two tasks can help each other: the position of a user from sensing helps to point the beam, and the communication link can share what each node senses. The cost is a tradeoff. A good radar waveform has a sharp [ambiguity function](/ambiguity-function/) and a constant envelope, and a good communication waveform carries as many random bits as possible. One waveform cannot be the best at both.

## In plain words

A radio that sends data already lights up everything around it. If it also listens for the echoes, it is a radar for free. The data symbols are random, but the receiver of the echoes knows them, because it sent them. So it can remove them and keep only what the targets did to the signal: a delay for the range and a phase change over time for the speed. The question is how much sensing is lost because the signal carries data, and how much data is lost because the signal must also sense.

## The idea

**Three levels of integration.**

- **Coexistence.** Radar and communication use separate waveforms in the same band, and each treats the other as interference to avoid or cancel.
- **Cooperation.** The two systems share information, such as the position of the radar beam or the schedule of the users, to reduce the interference.
- **Co-design.** One waveform and one transmitter do both tasks. This is ISAC in the strict sense.

**Sensing-centric, communication-centric and joint designs.** A sensing-centric design starts from a radar waveform and puts data in it, for example in the phase or the start frequency of the chirps of an [FMCW radar](/fmcw-radar/), at a low data rate. A communication-centric design starts from a communication waveform, usually [OFDM](/orthogonal-frequency-division-multiplexing/), and uses its echoes for sensing. A joint design chooses the waveform or the beamformer by optimizing a weighted cost of the two tasks.

**OFDM radar.** Sturm and Wiesbeck (2011) gave the processing that most communication-centric work uses. The transmitter sends the data symbols $d[m][k]$ on $N$ subcarriers spaced $\Delta f$ apart, over $M$ OFDM symbols of length $T_{\text{sym}}$ each. A target at range $R$ and speed $v$ multiplies the received symbol on subcarrier $k$ and OFDM symbol $m$ by

$$e^{-j 2\pi k \Delta f \cdot 2R/c}\; e^{j 2\pi m T_{\text{sym}} \cdot 2v/\lambda}.$$

The sensing receiver divides each received symbol by the symbol it sent, which removes the data. What remains is a two dimensional array of complex exponentials. An inverse FFT over $k$ gives the range, and an FFT over $m$ gives the speed, as in [range-Doppler processing](/range-doppler-processing/). The range resolution is $c/(2N\Delta f)$, the unambiguous range is $c/(2\Delta f)$, the speed resolution is $\lambda/(2 M T_{\text{sym}})$ and the unambiguous speed is $\pm\lambda/(4 T_{\text{sym}})$.

**Check values.** With $N = 1024$ subcarriers at $\Delta f = 120$ kHz, the bandwidth is $122.88$ MHz, the range resolution is $1.22$ m and the unambiguous range is $1249$ m. The useful symbol lasts $1/\Delta f = 8.33$ μs; with the normal cyclic prefix of the 5G numerology for 120 kHz, 14 symbols fill $0.125$ ms, so $T_{\text{sym}} = 8.93$ μs on average. That cyclic prefix is $0.586$ μs, and an echo with a longer delay than that, a target beyond $87.8$ m, spreads into the next symbol and adds interference unless the receiver handles it. At 28 GHz ($\lambda = 10.71$ mm), $M = 112$ symbols last $1.0$ ms and give a speed resolution of $5.35$ m/s, with an unambiguous speed of $\pm 299.8$ m/s.

**The tradeoff.** The tradeoff is often drawn as a region of pairs (sensing accuracy, data rate) that a design can reach. Some causes:

- **Random data.** Symbols of a QAM constellation have different powers. After the division, the noise is larger on the subcarriers with small symbols, so the range and speed estimates are worse than with a constant envelope signal. Constant modulus symbols, such as PSK, avoid that but carry fewer bits per symbol.
- **Power and time.** Pilots, beams toward targets and symbols reserved for sensing take power, time or frequency from the data.
- **Beams.** A beam that points at a user is not, in general, a beam that scans the scene. Joint [beamforming](/beamforming/) shares the power of the array between the two, and [massive MIMO](/massive-mimo/) arrays have the degrees of freedom to do both.
- **Bounds.** The sensing side is measured by the mean squared error of the estimates or by the [Cramér-Rao bound](/cramer-rao-bound/), and the communication side by the rate. The exact boundary of the region is still a research question for most models.

**Monostatic and bistatic sensing.** In monostatic sensing, the transmitter also receives the echoes, and it knows the data, but it must transmit and receive at the same time, so it needs isolation between the two (full duplex). In bistatic sensing, another node receives, so there is no self-interference, but that node must know or decode the data and must share the timing and the frequency of the transmitter.

## Examples

- **A 5G or 6G base station.** It senses the cars and the people in its cell with the OFDM signals it already sends, as in the check values above.
- **A car radar that talks.** An FMCW radar puts a few bits in each chirp to send warnings to other cars, a sensing-centric design.
- **Wi-Fi sensing.** A Wi-Fi access point uses the changes of the channel estimates, from [channel estimation](/channel-estimation/), to detect motion and gestures in a room. This uses the channel, not a radar echo in the strict sense.
- **Delay-Doppler waveforms.** [OTFS](/orthogonal-time-frequency-space-modulation/) puts the data on a delay-Doppler grid, the same grid on which a radar sees targets, which is why it is studied for ISAC.

## Where it is used

- 6G research and standardization treat sensing as a service of the network, for traffic, drones and smart factories.
- Vehicle networks combine radar and the exchange of data between cars.
- Indoor sensing with Wi-Fi detects the presence of people and their motion.
- Work on [reconfigurable intelligent surfaces](/reconfigurable-intelligent-surface/) studies surfaces that shape the channel for both sensing and data.

## References
