---
tag: X1B51D
kind: definition
slug: processing-gain
name: Processing gain
aliases:
- spreading factor
area: communications/multiple-access-and-spread-spectrum
level: intro
summary: "The ratio of the spread bandwidth to the data rate. It is the factor by which despreading raises the signal over interference of fixed power that is spread across the band."
model: real-ram
prereqs: [energy-per-bit-to-noise-density-ratio, power-spectral-density]
see_also: [direct-sequence-spread-spectrum, frequency-hopping-spread-spectrum, code-division-multiple-access, ovsf-codes, spectral-efficiency, shannon-hartley-theorem]
sources:
  - paper: doi:10.1109/TCOM.1982.1095533
    title: Raymond L. Pickholtz, Donald L. Schilling and Laurence B. Milstein, Theory of spread-spectrum communications, a tutorial, IEEE Transactions on Communications 30(5), 1982
    locator: pp. 855 to 884 (the definitions of processing gain and jamming margin)
  - book: isbn:9780201633740
    title: Andrew J. Viterbi, CDMA, Principles of Spread Spectrum Communication, Addison-Wesley, 1995
    locator: The opening chapters (the ratio of spread bandwidth to data rate and its role in CDMA capacity)
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, 5th edition, McGraw-Hill, 2008
    locator: The chapter on spread spectrum signals for digital communications
---

The processing gain of a spread-spectrum system is the ratio $G_p = W / R$ of the bandwidth $W$ that the transmitted signal occupies to the information bit rate $R$. It measures how much the receiver gains over an interferer of fixed power when it despreads: an interferer that is spread over the band $W$ keeps only about a fraction $1/G_p$ of its power in the band of the data. In [direct-sequence spread spectrum](/direct-sequence-spread-spectrum/) with one code symbol per bit, $G_p$ is the number of chips per bit; in [frequency-hopping spread spectrum](/frequency-hopping-spread-spectrum/) it is about the number of hop channels. Processing gain does not help against white noise, whose power grows with the band.

## Definition

Let a system send $R$ information bits per second in a signal of bandwidth $W$ hertz. Its **processing gain** is

$$G_p = \frac{W}{R}, \qquad \text{often given in decibels as } 10 \log_{10} G_p.$$

For DSSS with chip duration $T_c$ and bit duration $T_b$, $W \approx 1/T_c$ and $R = 1/T_b$, so $G_p = T_b / T_c$, the number of chips per bit.

**Why it is a gain.** Let the received signal have power $S$, so the energy per bit is $E_b = S / R$. Let an interferer of power $J$ be spread evenly over the band $W$, by the jammer itself or by the despreader, so that its one-sided [power spectral density](/power-spectral-density/) is $J_0 = J / W$. Then

$$\frac{E_b}{J_0} = \frac{S / R}{J / W} = G_p \cdot \frac{S}{J}.$$

The detector sees $E_b / J_0$, which is $G_p$ times larger than the ratio $S/J$ of the powers at its input. If the link needs $E_b / J_0 \ge \gamma$ to meet its error rate, it can tolerate an interferer up to $J/S = G_p / \gamma$.

**Jamming margin.** In decibels, the largest tolerable $J/S$ is the **jamming margin**

$$M_J = G_p - \left(\frac{E_b}{J_0}\right)_{\text{req}} - L_{\text{sys}} \quad \text{(dB)},$$

where $L_{\text{sys}}$ collects implementation losses (Pickholtz, Schilling and Milstein 1982). It is a rule of thumb for a link budget, not an exact limit; the result depends on the type of jammer.

**Processing gain and chips per symbol.** $G_p$ counts chips per information bit. With a code of rate $r$ and one code bit per symbol, each code symbol gets $r \, G_p$ chips. So the number of chips per symbol equals $G_p$ only for DSSS without coding and with one bit per symbol.

## Examples and non-examples

**IS-95 forward link.** The chip rate is $1.2288$ Mchip/s and the full voice rate is $9.6$ kbit/s, so $G_p = 128$, or $21.07$ dB. A rate-1/2 convolutional code gives $19.2$ ksymbol/s, so each code symbol is spread by a Walsh code of $64$ chips. The processing gain is $128$, although each symbol has $64$ chips.

**GPS C/A code.** The code has $1023$ chips at $1.023$ Mchip/s, and the navigation data rate is $50$ bit/s. So $G_p = 20460$, or $43.11$ dB: $30.10$ dB from one code period of $1$ ms and $13.01$ dB from adding the $20$ code periods of each bit.

**Jamming margin.** A link with $G_p = 30$ dB that needs $E_b/J_0 = 10$ dB and has $2$ dB of losses has a jamming margin of $18$ dB: it works with an interferer up to $18$ dB stronger than the signal. With $G_p = 128$ and a required $E_b / J_0$ of $7$ dB, the margin before losses is $14.07$ dB.

**Frequency hopping.** Bluetooth Basic Rate hops over $79$ channels of $1$ MHz. Against a jammer that covers one channel, the hopping gives a factor of about $79$, or $18.98$ dB, in the sense that the jammer hits only one hop in $79$.

**Non-example: white noise.** For thermal noise of density $N_0$, the noise power in the band is $N_0 W$, which grows with $W$. The ratio $E_b / N_0$ does not change with spreading, so the bit error rate on an AWGN channel is the same with or without spreading. Processing gain is a gain only against interference of fixed total power.

**Non-example: bandwidth expansion by coding.** A rate-1/2 code without spreading doubles the bandwidth, but it is not counted as processing gain in the sense above. Its benefit is the coding gain, which also works against white noise. The two gains are separate entries in a link budget.

## Related definitions

- [Direct-sequence spread spectrum](/direct-sequence-spread-spectrum/) reaches the gain by multiplying each bit by $G_p$ chips and correlating at the receiver.
- [Frequency-hopping spread spectrum](/frequency-hopping-spread-spectrum/) reaches it by moving a narrowband signal over many channels.
- In [CDMA](/code-division-multiple-access/), the other users act as interference of roughly fixed power each, so the number of users that a cell can carry grows about in proportion to $G_p$.
- The [energy per bit to noise density ratio](/energy-per-bit-to-noise-density-ratio/) is the quantity that the gain raises when the noise is interference of fixed power.
- The [Shannon-Hartley theorem](/shannon-hartley-theorem/) gives the capacity $W \log_2(1 + S/(N_0 W))$, which grows with $W$. A wide band with a signal below the noise can still carry a low data rate, so spreading a low-rate signal costs little capacity.

## References
