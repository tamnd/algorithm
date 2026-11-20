---
tag: T2M34N
kind: technique
slug: time-division-multiple-access
name: Time-division multiple access
aliases:
- TDMA
area: communications/multiple-access-and-spread-spectrum
level: intro
summary: Users take turns on the whole band, each sending only in its own time slot of a repeating frame. Guard times and timing advance keep the slots from overlapping.
prereqs: [additive-white-gaussian-noise-channel, channel-capacity]
see_also: [frequency-division-multiple-access, orthogonal-frequency-division-multiple-access, ofdma-resource-allocation, mac-capacity-region, slotted-aloha, medium-access-control, wireless-link-scheduling, code-division-multiple-access]
sources:
  - book: isbn:9780521837163
    title: Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005
    locator: Section 14.2 (multiple access) and Section 14.2.2 (time-division multiple access); Section 14.6.1 (capacity of the AWGN uplink, with the TDMA rates)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Chapter 15, Section 15.3 (the Gaussian multiple access channel, with time-division multiplexing compared with the capacity region)
  - book: isbn:9780130422323
    title: Theodore S. Rappaport, Wireless Communications, Principles and Practice, second edition, Prentice Hall, 2002
    locator: Chapter 9 (multiple access techniques), the TDMA section with the frame structure and the frame efficiency; the chapter on wireless systems and standards for the GSM frame
  - url: https://www.3gpp.org/DynaReport/45002.htm
    title: 3GPP TS 45.002, GSM/EDGE multiplexing and multiple access on the radio path
    locator: The TDMA frame, the time slots, the burst types and the timing advance
---

Time-division multiple access (TDMA) lets $K$ users share one carrier by taking turns. Time is cut into **frames**, each frame into **slots**, and each user sends a short burst in its own slot of every frame, using the whole band of the carrier. Between bursts there is a short empty **guard time**, so that a burst that arrives a little late does not run into the next one. [Frequency-division multiple access](/frequency-division-multiple-access/) cuts the same resource the other way: each user keeps a narrow band all the time, so FDMA needs no timing between users, while TDMA needs every terminal to follow a common clock. In GSM, a TDMA frame of 8 slots runs on each 200 kHz FDMA carrier. [OFDMA](/orthogonal-frequency-division-multiple-access/) cuts both time and frequency into small blocks, and the choice of which user gets which block is the problem of [OFDMA resource allocation](/ofdma-resource-allocation/).

## In plain words

Users take turns. The time on the channel is a repeating cycle, and each cycle has a fixed number of turns. Each user gets one turn per cycle and sends a short burst of data in it, at the full speed of the channel. Then it stays silent until its next turn.

Between turns there is a short pause. Users sit at different distances, so their bursts take different times to arrive. The pause keeps a late burst from hitting the next one. The base station also tells far users to send a bit early, so that all bursts arrive on time.

Each user sends in bursts, so its radio can be off most of the time, and it can listen to other channels in the gaps.

## When it applies

- All terminals can lock to a common clock sent by a base station, a satellite or a master node.
- The traffic is digital and can be buffered, so each user can send a frame's worth of data in one burst.
- The round-trip delays are known, or a timing advance can make up for them. Without it, the guard time must cover the full spread of delays in the cell.
- The amplifiers are nonlinear: with one burst at a time on the carrier, the amplifier can run near saturation, which FDMA with many carriers cannot do.
- The terminal has one radio and must also measure other channels: it can do so in the slots that are not its own. GSM uses these gaps for handover measurements.

## The template

A frame has length $T_f$ and $K$ slots of length $T_s = T_f / K$. Each slot holds a burst: a few tail symbols, the data, a training sequence for the channel estimate, and the guard time $T_g$ at the end, during which nobody sends. User $k$ sends in slot $k$ of every frame.

```pseudo id=main
TDMA-FRAME(frame index i)
L1  for k ← 0 to K - 1 do                     ▷ slot k of frame i
L2      t_k ← i T_f + k T_s - a_k              ▷ a_k is the timing advance of user k
L3      user k sends one burst from t_k for T_s - T_g
L4      the receiver estimates the channel from the training part and decodes the burst
L5      the receiver measures the arrival time and updates a_k
```

**Guard time and timing advance.** A user at distance $d$ sees the downlink $d/c$ late and its uplink burst comes back another $d/c$ late, so the round trip is $2d/c$. Without a timing advance, the guard time must cover the largest round trip in the cell: $T_g \ge 2 d_{\max} / c$ plus the ramp time of the amplifier. With a timing advance $a_k \approx 2 d_k / c$ (line L2), the guard only needs to cover the error of the advance and the ramp.

**Frame efficiency.** If each burst has $b_d$ data symbols out of $b_s$ symbol periods per slot, the frame efficiency is $\eta_f = b_d / b_s$. The rest goes to the guard, the training sequence and the tail.

**Rate on an AWGN channel.** Let user $k$ send in a fraction $\tau_k$ of the time, with $\sum_k \tau_k = 1$. The noise is white with the one-sided power spectral density $N_0$. Define $\mathrm{SNR}_k = P_k / (N_0 B)$ for the average power $P_k$ and the band $B$; in channel uses at the Nyquist rate it is $E_s/N_0$ per complex symbol. Two power models give two rates (both closed forms for the AWGN channel with Gaussian codes):
- Average power constraint: the user saves its energy for its own slot and sends at power $P_k / \tau_k$ during it. Then $R_k = \tau_k \log_2(1 + \mathrm{SNR}_k / \tau_k)$, the same as FDMA with band fractions $\tau_k$. With $\tau_k$ in proportion to $\mathrm{SNR}_k$, the sum rate is $\log_2(1 + \sum_k \mathrm{SNR}_k)$, the sum capacity of the [MAC capacity region](/mac-capacity-region/).
- Peak power constraint: the user cannot send more than $P_k$ at any time. Then $R_k = \tau_k \log_2(1 + \mathrm{SNR}_k)$, and TDMA falls well short of the sum capacity.

## Classic examples

**GSM.** Each 200 kHz carrier has 8 slots. The bit period is $48/13 = 3.6923$ microseconds, so the gross rate is 270.833 kbit/s. A slot lasts 156.25 bit periods, which is 576.92 microseconds, and a frame lasts 8 slots, which is 4.615 ms. A normal burst has 3 tail bits, 57 data bits, 1 flag bit, a training sequence of 26 bits, 1 flag bit, 57 data bits and 3 tail bits, and then a guard of 8.25 bit periods, which is 30.46 microseconds. The frame efficiency for the data bits is $114 / 156.25 = 0.7296$. The timing advance runs from 0 to 63 bit periods. A round trip of 63 bit periods is 232.6 microseconds, which fixes the largest cell radius at about 35 km. All numbers are from the frame of 3GPP TS 45.002.

**Two users, two power models.** Let $\mathrm{SNR}_1 = 10$ and $\mathrm{SNR}_2 = 5$, and let each user have half of the time. Under a peak power constraint, $R_1 = 0.5 \log_2 11 = 1.7297$ and $R_2 = 0.5 \log_2 6 = 1.2925$, a sum of 3.0222 bits per channel use. Under an average power constraint with $\tau_1 = 2/3$, the rates are $2.6667$ and $1.3333$, and the sum is 4.0000, the sum capacity $\log_2 16$. The gap of almost 1 bit is what the burst power gains.

**Guard time without timing advance.** For a cell of radius 35 km, the round trip is $2 \times 35000 / (3 \times 10^8) = 233$ microseconds. At the GSM bit period this is 63 bits, which would be 40 percent of the slot. The timing advance cuts this to 8.25 bits.

## Variations

- **Hybrid FDMA/TDMA.** GSM and the North American IS-136 system run TDMA frames on FDMA carriers.
- **Dynamic TDMA.** A scheduler gives slots to users each frame, according to their queues or their channels. Many satellite return links work this way. See [wireless link scheduling](/wireless-link-scheduling/).
- **Time-division duplex (TDD).** The uplink and the downlink share one carrier in separate slots, as in DECT.
- **Random access in slots.** Users with rare packets send in a random slot instead of a fixed one; see [slotted ALOHA](/slotted-aloha/) and [coded slotted ALOHA](/coded-slotted-aloha/). TDMA frames often keep a few slots for this kind of access.
- **OFDMA.** The frame is cut in frequency too, into blocks of subcarriers and symbols; see [OFDMA](/orthogonal-frequency-division-multiple-access/) and [OFDMA resource allocation](/ofdma-resource-allocation/).

## Pitfalls

- **Intersymbol interference.** Each user sends at the full rate of the carrier, so the symbols are short. If the delay spread is a large part of the symbol period, the receiver needs an equalizer. GSM uses its 26-bit training sequence for this. See [delay spread](/delay-spread/).
- **Guard time too short.** A guard sized for a small cell fails in a large one. Size it for the largest residual timing error after the timing advance, plus the ramp time.
- **Peak power.** A user that sends one slot in eight needs eight times its average power during the slot. If the amplifier cannot give it, the rate is the peak-power rate, which is lower.
- **Synchronization overhead.** Every burst repeats the training and tail bits. Short slots make this overhead large.
- **Idle slots.** Like FDMA, a fixed slot for a silent user is lost. Dynamic assignment fixes this at the cost of signaling.
- **Bursty interference.** A switched burst has a spectrum wider than the carrier during the ramp, and the 217 Hz burst rate of GSM is audible in nearby audio circuits.

## Exercises

1. A frame has 8 slots of 156.25 bit periods each and each burst carries 114 data bits. What is the data rate per user if the bit period is $48/13$ microseconds? (Answer: $114 / 4.615$ ms, which is 24.7 kbit/s before coding.)
2. Derive the largest cell radius for a guard of 8.25 bit periods with no timing advance. (Answer: $8.25 \times 3.6923$ microseconds $\times c / 2$, about 4.6 km.)
3. Show that the TDMA rate under an average power constraint, $\tau \log_2(1 + s/\tau)$, is at least the rate under a peak constraint, $\tau \log_2(1 + s)$, for $0 < \tau \le 1$.
4. Two users have $\mathrm{SNR}_1 = 10$ and $\mathrm{SNR}_2 = 5$ under a peak constraint. Which split of time gives the largest sum rate? (Answer: all the time to user 1, a sum of $\log_2 11 = 3.4594$, but then user 2 gets nothing.)

## References
