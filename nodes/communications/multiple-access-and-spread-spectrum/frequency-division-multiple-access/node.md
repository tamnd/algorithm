---
tag: KDFRH5
kind: technique
slug: frequency-division-multiple-access
name: Frequency-division multiple access
aliases:
- FDMA
area: communications/multiple-access-and-spread-spectrum
level: intro
summary: Gives each user its own frequency band, separated by guard bands, for the whole time.
prereqs: [additive-white-gaussian-noise-channel, channel-capacity]
see_also: [time-division-multiple-access, orthogonal-frequency-division-multiple-access, ofdma-resource-allocation, code-division-multiple-access, mac-capacity-region, medium-access-control, multicarrier-modulation, frequency-hopping-spread-spectrum]
sources:
  - book: isbn:9780521837163
    title: Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005
    locator: Section 14.2 (multiple access) and Section 14.2.1 (frequency-division multiple access); Section 14.6.1 (capacity of the AWGN uplink, with the FDMA rates)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Chapter 15, Section 15.3 (the Gaussian multiple access channel, with the comparison of FDMA and TDMA against the capacity region)
  - book: isbn:9780521845274
    title: David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005
    locator: Chapter 4 (cellular systems, narrowband systems with orthogonal channels) and Chapter 6, Section 6.1 (uplink AWGN channel, orthogonal multiple access against the sum capacity)
  - book: isbn:9780130422323
    title: Theodore S. Rappaport, Wireless Communications, Principles and Practice, second edition, Prentice Hall, 2002
    locator: Chapter 9 (multiple access techniques for wireless communications), the FDMA section with the channel count of an AMPS operator
---

Frequency-division multiple access (FDMA) splits a band of width $B$ into $K$ narrower channels and gives each user one channel for as long as the user holds the connection. Users never share a channel, so the receiver separates them with a band-pass filter and nothing more. Neighboring channels sit apart by a small unused **guard band**, so that the filter skirts, the oscillator drift and the Doppler shift of one user do not spill into the next. [Time-division multiple access](/time-division-multiple-access/) cuts the same resource the other way: every user gets the whole band, but only for a short slot in each frame. [OFDMA](/orthogonal-frequency-division-multiple-access/) is FDMA with overlapping orthogonal subcarriers and no guard bands between them, and it hands the subcarriers out again every millisecond or so. How to choose the bands and powers of the users is the problem of [OFDMA resource allocation](/ofdma-resource-allocation/). FDMA is the scheme of the first analog cellular systems (AMPS), of satellite links with one carrier per channel, and of FM radio.

## In plain words

Think of a radio dial. Each station owns one spot on the dial and keeps it all the time. Between two stations there is a little gap, so that a strong station does not leak into its neighbor.

FDMA does the same for the users of a cell. Each user gets a narrow band of frequencies for the whole call. The receiver tunes to that band and filters out the rest. No timing is needed between users, because no two of them ever use the same band.

The price is waste. The gaps between bands carry nothing. A user who is silent still holds the band. And a narrow band can fall into a deep fade that lasts as long as the fade lasts, because the user has no other frequencies to fall back on.

## When it applies

- The traffic is steady, such as a voice call or a continuous telemetry stream, so a fixed channel does not sit idle much.
- The terminals are simple: a fixed carrier, a fixed filter, and no need to agree on time with other users. FDMA needs no frame timing between users, unlike TDMA.
- Each channel is narrow compared with the [coherence bandwidth](/coherence-bandwidth/), so the channel is flat inside it and the receiver needs no equalizer. This is the usual case for channels of 10 to 200 kHz.
- A transmitter amplifies one carrier only. A shared amplifier that carries many FDMA carriers, as in a satellite transponder, must back off from saturation because of intermodulation (see Pitfalls).
- The number of users is about fixed and known. With bursty data, a scheme that reassigns the band quickly ([OFDMA](/orthogonal-frequency-division-multiple-access/) with a scheduler, or random access by [medium access control](/medium-access-control/)) uses the band better.

## The template

The plan of an FDMA system is a frequency raster. It has no time frame: the "frame" is the list of channel centers. Let the total band be $B_t$, the channel width $B_c$ and the guard band at each edge of the allocation $B_g$. Then the number of channels is

$$K = \left\lfloor \frac{B_t - 2 B_g}{B_c} \right\rfloor,$$

and channel $k$ is centered at $f_k = f_0 + B_g + (k + \tfrac{1}{2}) B_c$ for $k = 0, \ldots, K - 1$. Inside each $B_c$, the useful signal takes a smaller width $B_s$; the difference $B_c - B_s$ is the guard between two neighboring channels. The spectral efficiency of the plan is $K B_s / B_t$ times the efficiency of the modulation inside one channel.

```pseudo id=main
FDMA-ASSIGN(K channels, request of user u)
L1  if a channel k is free then
L2      give channel k to user u and mark it busy
L3  else block the request              ▷ no channel left
FDMA-RECEIVE(r, k)
L4  shift r down by f_k                 ▷ channel k to baseband
L5  low-pass filter to width B_s / 2, then demodulate
FDMA-RELEASE(k)
L6  mark channel k free
```

With frequency-division duplex (FDD), each channel is a pair: one band for the uplink and one for the downlink, at a fixed duplex distance (45 MHz in AMPS).

**Rate on an AWGN channel.** Let user $k$ have power $P_k$ and a fraction $\alpha_k$ of a band of width $B$, with $\sum_k \alpha_k = 1$ and no guard bands. The noise has the one-sided power spectral density $N_0$, so the noise power in the user's band is $N_0 \alpha_k B$. Define the SNR of user $k$ over the whole band as $\mathrm{SNR}_k = P_k / (N_0 B)$; in channel uses at the Nyquist rate it is $E_s/N_0$ per complex symbol. Then user $k$ can send at (a closed form for the AWGN channel with Gaussian codes, by the [channel capacity](/channel-capacity/) formula of the [AWGN channel](/additive-white-gaussian-noise-channel/))

$$R_k = \alpha_k \log_2\!\left(1 + \frac{\mathrm{SNR}_k}{\alpha_k}\right) \text{ bits per channel use of the full band.}$$

The user's power is packed into a narrower band, so the SNR inside the band is $\mathrm{SNR}_k / \alpha_k$. If $\alpha_k = \mathrm{SNR}_k / \sum_i \mathrm{SNR}_i$, every user sees the same in-band SNR $\sum_i \mathrm{SNR}_i$, and the sum of the rates is $\log_2(1 + \sum_k \mathrm{SNR}_k)$. This is the sum capacity of the Gaussian uplink (a theorem, Cover and Thomas, Section 15.3). So FDMA with bands in proportion to the powers reaches one point on the sum-rate face of the [MAC capacity region](/mac-capacity-region/). Any other split falls short of the sum capacity.

## Classic examples

**AMPS channel count.** A US AMPS operator has $B_t = 12.5$ MHz in each direction, channels of $B_c = 30$ kHz, and a guard of $B_g = 10$ kHz at each edge. Then $K = (12.5 \times 10^6 - 2 \times 10^4) / (3 \times 10^4) = 416$ channels. This is the textbook count (Rappaport, Chapter 9). Some of these channels carry control data, not calls.

**Two users on one band.** Let $\mathrm{SNR}_1 = 10$ and $\mathrm{SNR}_2 = 5$ over the whole band. The sum capacity is $\log_2 16 = 4$ bits per channel use.

| split $\alpha_1$ | $R_1$ | $R_2$ | $R_1 + R_2$ |
|---|---|---|---|
| 2/3 (in proportion to power) | 2.6667 | 1.3333 | 4.0000 |
| 1/2 | 2.1962 | 1.7297 | 3.9259 |
| 0.8 | 3.0039 | 0.9401 | 3.9440 |

The first row reaches the sum capacity. The equal split loses only 0.074 bits per channel use, because the rate curve is flat near its peak. All rates were computed with the formula above.

**Guard band overhead.** If a system leaves a guard of 10 percent of each channel, it loses 10 percent of the band before any coding. This is one reason OFDMA, which needs no guard between subcarriers of the same transmitter, replaced FDMA in broadband systems.

## Variations

- **Single channel per carrier (SCPC).** One FDMA carrier per voice or data channel on a satellite transponder. Demand-assigned SCPC gives out the carriers on request, as FDMA-ASSIGN above does.
- **Hybrid FDMA/TDMA.** GSM divides the band into 200 kHz carriers (FDMA) and each carrier into 8 time slots (TDMA). See [time-division multiple access](/time-division-multiple-access/) for the frame.
- **OFDMA and SC-FDMA.** The channels are subcarriers spaced at exactly the inverse of the symbol length, so they overlap but stay orthogonal; see [OFDMA](/orthogonal-frequency-division-multiple-access/) and [SC-FDMA](/sc-fdma/). The choice of who gets which subcarrier is [OFDMA resource allocation](/ofdma-resource-allocation/).
- **Frequency hopping.** Each user changes its channel in a pseudorandom pattern, which spreads the fades and the interference over many channels; see [frequency-hopping spread spectrum](/frequency-hopping-spread-spectrum/).
- **Wavelength-division multiplexing.** The optical form: each light wavelength is a channel on one fiber.

## Pitfalls

- **Intermodulation.** A nonlinear amplifier that carries several carriers makes products at frequencies such as $2 f_1 - f_2$, which can land in a third user's channel. The amplifier must back off from saturation, which costs power.
- **Adjacent channel interference with a near-far gap.** A filter with 60 dB of rejection is not enough if the neighbor channel is 70 dB stronger at the receiver. Power control and wider guards are the fixes; see [near-far problem](/near-far-problem/).
- **Frequency drift and Doppler.** A carrier offset larger than the guard moves energy into the next channel. Size the guard for the worst oscillator error plus the largest Doppler shift.
- **Idle channels.** A fixed channel stays assigned in the silent parts of a call. For bursty data the band is mostly idle.
- **No frequency diversity.** A narrow channel is flat and can sit in a deep fade for a long time. Coding over time does not help a static user in a static fade.
- **Equal split is not the capacity split.** Equal bands for users of unequal power miss the sum capacity, as the table shows. Matching the bands to the powers fixes it.

## Exercises

1. A band of 5 MHz is split into channels of 200 kHz with a guard of 100 kHz at each edge. How many channels fit? (Answer: $\lfloor 4.8 / 0.2 \rfloor = 24$.)
2. Show that $\alpha \log_2(1 + s/\alpha)$ grows with $\alpha$ for every $s > 0$. What does this say about a user who gets more band at the same power?
3. Show that, for two users, the sum $\alpha \log_2(1 + s_1/\alpha) + (1 - \alpha) \log_2(1 + s_2/(1 - \alpha))$ is largest at $\alpha = s_1 / (s_1 + s_2)$, and that the largest value is $\log_2(1 + s_1 + s_2)$.
4. A satellite amplifier carries 20 FDMA carriers. Why does it run 3 to 6 dB below its saturation power, while a single-carrier amplifier can run close to it?
5. A channel is 25 kHz wide and the carrier is 900 MHz. The oscillator error is 2 parts per million and the speed is 120 km/h. Find the worst carrier offset and compare it with the channel width. (Answer: 1.8 kHz plus 100 Hz, about 1.9 kHz, which is 7.6 percent of the channel.)

## References
