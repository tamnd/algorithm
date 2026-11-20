---
tag: 96KC9Q
kind: technique
slug: orthogonal-frequency-division-multiple-access
name: Orthogonal frequency-division multiple access
aliases:
- OFDMA
area: communications/multiple-access-and-spread-spectrum
level: core
summary: Shares the subcarriers of OFDM among users and gives them out again in small time-frequency blocks, so each user gets the subcarriers where its channel is strong.
prereqs: [orthogonal-frequency-division-multiplexing, frequency-division-multiple-access, time-division-multiple-access]
see_also: [ofdma-resource-allocation, sc-fdma, cyclic-prefix, inter-carrier-interference, multiuser-diversity, proportional-fair-scheduling, non-orthogonal-multiple-access, multicarrier-modulation]
sources:
  - paper: doi:10.1109/49.793310
    title: Cheong Yui Wong, Roger S. Cheng, Khaled Ben Letaief and Ross D. Murch, Multiuser OFDM with adaptive subcarrier, bit, and power allocation, IEEE Journal on Selected Areas in Communications 17(10), 1999
    locator: pp. 1747 to 1758 (subcarriers shared among users and assigned from the channel of each user)
  - book: isbn:9780521845274
    title: David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005
    locator: Chapter 4, the section on wideband systems with OFDM (the OFDM-based cellular system, hopping of subcarriers and the uplink timing); Chapter 6 (multiuser diversity)
  - book: isbn:9780521837163
    title: Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005
    locator: Section 12.4 (OFDM and the cyclic prefix) and Section 14.2 (multiple access, with multicarrier and hybrid schemes)
  - url: https://www.3gpp.org/DynaReport/36211.htm
    title: 3GPP TS 36.211, Evolved Universal Terrestrial Radio Access (E-UTRA), physical channels and modulation
    locator: The frame structure, the resource grid, the resource block of 12 subcarriers and the cyclic prefix lengths
---

Orthogonal frequency-division multiple access (OFDMA) is the multiple access form of [OFDM](/orthogonal-frequency-division-multiplexing/). One OFDM symbol carries $N$ orthogonal subcarriers, and OFDMA gives different subcarriers to different users. The grid of subcarriers and OFDM symbols is cut into small blocks, and a scheduler hands the blocks out again in every short interval, often every millisecond. Compared with [FDMA](/frequency-division-multiple-access/), the bands of different users overlap in frequency but stay orthogonal, so no guard band is needed between them, and the assignment follows the channel. Compared with [TDMA](/time-division-multiple-access/), many users send at once, each on a part of the band. OFDMA is the downlink of LTE and 5G NR and both links of Wi-Fi 6. The question of who gets which block and how much power is [OFDMA resource allocation](/ofdma-resource-allocation/), a separate page.

## In plain words

OFDM splits a wide band into many narrow, closely packed tones. Their spacing is chosen so that they do not disturb each other. OFDMA lets many users share these tones. Each user gets a group of tones for a short time, and the base station decides again a moment later.

Each user sees a different channel. Some tones are strong for one user and weak for another. The base station can give each tone to a user for whom it is strong, so the band carries more data in total.

Users must stay lined up in time and in frequency. If a user's clock or carrier is off, its tones leak onto the tones of other users.

## When it applies

- The band is wide compared with the [coherence bandwidth](/coherence-bandwidth/), so the channel is frequency-selective. OFDM turns it into flat subchannels, and OFDMA can use the differences between users on each subchannel.
- The traffic is bursty and mixed. Small blocks let the scheduler give a voice user a few subcarriers and a download a large part of the band.
- The base station knows the channels, from pilots in the downlink and from channel reports or sounding in the uplink. Without channel knowledge, OFDMA still works, but with a fixed or hopping assignment.
- In the uplink, all terminals can keep their timing within the cyclic prefix and their carrier offset within a small part of the subcarrier spacing. Then the signals of different users stay orthogonal at the base station.
- The peak-to-average power ratio of OFDM is acceptable. LTE uses OFDMA only in the downlink and uses [SC-FDMA](/sc-fdma/), a DFT-spread form with a lower peak power, in the uplink.

## The template

Fix a DFT size $N$, a subcarrier spacing $\Delta f$, a cyclic prefix of $N_{cp}$ samples and $K$ users. The sample rate is $f_s = N \Delta f$. The time-frequency grid is cut into **resource blocks** of $Q$ adjacent subcarriers and $S$ OFDM symbols. In each scheduling interval, the scheduler gives each block to at most one user. User $k$ maps its data symbols to the subcarriers of its blocks. The base station transmits the sum, and each receiver keeps only its own subcarriers.

```pseudo id=main
OFDMA-DOWNLINK(data of K users, channel reports)
L1  for each scheduling interval do
L2      assign each resource block to one user        ▷ see ofdma-resource-allocation
L3      for each OFDM symbol in the interval do
L4          X[n] ← symbol of the user that owns subcarrier n, or 0 if none
L5          x ← IDFT_N(X); prepend the last N_cp samples of x
L6          send x
OFDMA-RECEIVE(user k)
L7  remove the cyclic prefix and take Y ← DFT_N(y)
L8  for each subcarrier n of user k do
L9      estimate H_k[n] from pilots and decide on Y[n] / H_k[n]
```

The DFT is the unnormalized pair of [discrete Fourier transform](/discrete-fourier-transform/): $X[n] = \sum_{t} x[t] e^{-j 2 \pi n t / N}$ and the inverse with the factor $1/N$; the imaginary unit is $j$. With $N_{cp} \ge L - 1$ for a channel of $L$ taps $h_k[0], \ldots, h_k[L-1]$, user $k$ sees on subcarrier $n$ the flat channel

$$Y_k[n] = H_k[n] X[n] + W_k[n],$$

where $H_k[n]$ is the DFT of the taps of user $k$, and $W_k[n]$ is complex Gaussian noise (see [cyclic prefix](/cyclic-prefix/)). Each user's subcarriers are disjoint, so the users do not interfere. Define the SNR of user $k$ on subcarrier $n$ as $\mathrm{SNR}_k[n] = |H_k[n]|^2 E_s / N_0$, where $E_s$ is the energy per complex symbol on the subcarrier and $N_0$ the noise power spectral density, so that the noise $W_k[n]$ has variance $N_0$ per subcarrier in the matching normalization. The rate on that subcarrier is at most $\log_2(1 + \mathrm{SNR}_k[n])$ bits per channel use.

**Guards.** OFDMA needs no guard between users in frequency, only a few unused subcarriers at the band edges and the unused DC subcarrier. In time, the cyclic prefix is the guard: it absorbs the delay spread and, in the uplink, the residual timing error of each user.

**Cost.** The transmitter and each receiver do one FFT of size $N$ per OFDM symbol, $O(N \log N)$ complex operations (link [fast Fourier transform](/fast-fourier-transform/)), plus one division per subcarrier. A user that owns $N_k$ subcarriers still needs the full FFT, or a partial transform for its $N_k$ outputs.

## Classic examples

**LTE downlink, 20 MHz.** The subcarrier spacing is 15 kHz. A resource block is 12 subcarriers (180 kHz) for one slot of 0.5 ms, which holds 7 OFDM symbols with the normal cyclic prefix. A subframe of 1 ms has two slots, and a radio frame of 10 ms has 10 subframes. The scheduler assigns pairs of resource blocks once per subframe. A 20 MHz carrier has 100 resource blocks, so 1200 subcarriers fill 18 MHz, and 1 MHz at each edge is the guard band. The FFT size is 2048 at 30.72 MHz. The cyclic prefix is 160 samples (5.21 microseconds) on the first symbol of a slot and 144 samples (4.69 microseconds) on the other six, so a slot holds $160 + 2048 + 6 \times (144 + 2048) = 15360$ samples, which is 0.5 ms. These numbers are from 3GPP TS 36.211. The time overhead of the prefix is $1 - 7 \times 2048 / 15360 = 6.7$ percent, and the band overhead is 10 percent. A prefix of 4.69 microseconds covers a path length difference of 1.4 km.

**Choosing subcarriers by channel.** Two users share 4 subcarriers with equal power. Their SNRs on the subcarriers are $(10, 1, 4, 0.5)$ for user 1 and $(2, 8, 3, 6)$ for user 2. If each user takes a fixed block of two adjacent subcarriers (user 1 gets subcarriers 0 and 1), the total rate is $\log_2 11 + \log_2 2 + \log_2 4 + \log_2 7 = 9.2668$ bits per OFDM symbol. If each subcarrier goes to the user with the larger SNR (subcarriers 0 and 2 to user 1, 1 and 3 to user 2), the total is $\log_2 11 + \log_2 9 + \log_2 5 + \log_2 7 = 11.7586$ bits, 27 percent more. Here the best choice also splits the subcarriers evenly; in general it does not, and a fair scheduler trades some rate for fairness. This gain is [multiuser diversity](/multiuser-diversity/) in frequency.

## Variations

- **Localized and distributed blocks.** A localized block is a set of adjacent subcarriers, chosen where the user's channel is strong. A distributed block spreads its subcarriers over the band, for frequency diversity when the channel is not known.
- **Subcarrier hopping.** Each user follows a hopping pattern over the subcarriers, so that interference from other cells averages out. Flash-OFDM worked this way (Tse and Viswanath, Chapter 4).
- **SC-FDMA.** Each user spreads its symbols with a DFT before the subcarrier map, which lowers the peak-to-average power ratio; see [SC-FDMA](/sc-fdma/).
- **Numerologies.** 5G NR uses subcarrier spacings of $15 \times 2^\mu$ kHz, with shorter symbols and slots for larger spacings.
- **OFDMA with NOMA.** Two users can share one subcarrier with superposed powers; see [non-orthogonal multiple access](/non-orthogonal-multiple-access/).
- **Scheduling rules.** Max rate, [proportional fair](/proportional-fair-scheduling/) and round robin decide line L2. The optimization view is [OFDMA resource allocation](/ofdma-resource-allocation/).

## Pitfalls

- **Uplink timing.** In the uplink, users at different distances arrive at different times. If a user arrives later than the cyclic prefix allows, its subcarriers leak onto those of every other user. A timing advance, as in TDMA, keeps the arrivals inside the prefix.
- **Carrier frequency offset between users.** One user's offset breaks the orthogonality for all users, not only for itself, because its subcarriers shift onto the neighbors. The base station cannot correct the offsets of all users with one rotation. See [inter-carrier interference](/inter-carrier-interference/).
- **Stale channel reports.** The scheduler picks subcarriers from reports that are a few milliseconds old. At high speed the channel changes in that time, and the chosen subcarriers may be in a fade. Then distributed blocks are the safer choice.
- **Edge guard bands are still needed.** No guard is needed between users, but the spectrum mask still needs empty subcarriers at the band edges, because the sidelobes of the OFDM spectrum decay slowly.
- **Signaling overhead.** Telling each user which blocks it owns costs control data in every interval. Very small blocks give a better fit to the channel but more signaling.
- **Peak power.** The OFDMA downlink sum has a high peak-to-average power ratio, so the amplifier must back off.

## Exercises

1. A 10 MHz LTE carrier has 50 resource blocks. How many subcarriers are in use, and how wide is the occupied band? (Answer: 600 subcarriers, 9 MHz.)
2. With 15 kHz spacing and an FFT size of 2048, what is the sample rate? With a prefix of 144 samples, what is the longest delay spread that keeps the subcarriers orthogonal? (Answer: 30.72 MHz; 144 samples is 4.69 microseconds.)
3. In the 4-subcarrier example, find the assignment that maximizes the smaller of the two user rates. Compare its total rate with 11.7586.
4. Explain why a carrier offset at one uplink user harms the other users, while in the downlink each user's offset harms only itself.
5. Show that a user that owns all subcarriers in every interval turns OFDMA into plain OFDM, and that a fixed set of subcarriers per user turns it into a form of FDMA without guard bands.

## References
