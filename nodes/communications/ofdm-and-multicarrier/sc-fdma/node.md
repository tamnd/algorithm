---
tag: 1A5ZQW
kind: technique
slug: sc-fdma
name: SC-FDMA
aliases:
- DFT-spread OFDM
- single-carrier FDMA
area: communications/ofdm-and-multicarrier
level: core
summary: "Spread each user's M symbols with an M-point DFT before the OFDM transform. The signal keeps a single-carrier envelope with a lower PAPR, and the receiver still equalizes per subcarrier."
prereqs: [orthogonal-frequency-division-multiple-access, frequency-domain-equalization, peak-to-average-power-ratio, discrete-fourier-transform]
see_also: [zadoff-chu-sequence, cyclic-prefix, zero-forcing-equalizer, mmse-linear-equalizer, raised-cosine-filter, frequency-division-multiple-access, active-constellation-extension, filter-bank-multicarrier]
sources:
  - paper: doi:10.1109/MVT.2006.307304
    title: "Hyung G. Myung, Junsung Lim and David J. Goodman, Single carrier FDMA for uplink wireless transmission, IEEE Vehicular Technology Magazine 1(3), 2006, pages 30 to 38"
    locator: "the transmitter and receiver structure, the localized and interleaved subcarrier mappings and the comparison of PAPR with OFDMA"
  - paper: doi:10.1109/35.995852
    title: "David Falconer, Sirikiat Lek Ariyavisitakul, Anader Benyamin-Seeyar and Brian Eidson, Frequency domain equalization for single-carrier broadband wireless systems, IEEE Communications Magazine 40(4), 2002, pages 58 to 66"
    locator: "single-carrier transmission with a cyclic prefix and frequency-domain equalization, compared with OFDM"
---

SC-FDMA (single-carrier frequency-division multiple access), also called DFT-spread OFDM, is a multiple-access scheme that gives each user a set of subcarriers, like [OFDMA](/orthogonal-frequency-division-multiple-access/), but first spreads the user's data over them with a DFT. A user with $M$ data symbols takes their $M$-point DFT, places the $M$ outputs on $M$ of the $N$ subcarriers, takes the $N$-point inverse DFT and adds a [cyclic prefix](/cyclic-prefix/). The inverse DFT partly undoes the first DFT, so the time signal is close to the original data, upsampled and interpolated: a single-carrier signal. Its [peak-to-average power ratio](/peak-to-average-power-ratio/) is therefore much lower than that of OFDMA, which matters for the battery-powered amplifier of a mobile terminal. The receiver keeps the simple one-tap [frequency-domain equalization](/frequency-domain-equalization/) of OFDM, followed by an $M$-point inverse DFT. The LTE uplink uses SC-FDMA. The page uses the unitary DFT $F_N[k, n] = e^{-j 2\pi k n / N}/\sqrt N$, and $j$ is the imaginary unit.

## In plain words

In OFDM each data symbol rides on its own tone, and many tones add up to a signal with tall, random peaks. In SC-FDMA the sender first mixes its symbols together with a Fourier transform and puts the mixture on its tones. The second transform, the one that makes the time signal, then unmixes them again. What goes on the air looks like the original symbols sent one after another, smoothed between them. Such a signal has no tall random peaks, so the amplifier can run closer to its limit. The receiver fixes the channel tone by tone, as in OFDM, and then unmixes the symbols. A user still gets its own tones, so many users can share the band.

## When it applies

- Several users share a band in the uplink, and each user's power amplifier is the limit, so a low PAPR saves power or extends coverage.
- The channel is frequency selective, with a delay spread shorter than a cyclic prefix that the system can afford, so each subcarrier sees one complex gain.
- Each user can be given a contiguous block of subcarriers (localized) or an evenly spaced comb (interleaved), with $Q = N/M$ an integer for the comb.
- The receiver can run a linear equalizer. SC-FDMA spreads each symbol over all its subcarriers, so a deep fade on one subcarrier affects every symbol a little rather than one symbol a lot.

## The template

```pseudo id=main
SC-FDMA(d[0..M-1], N, map, cp)               ▷ transmitter, then receiver
L1  D ← F_M d                                   ▷ M-point DFT spreading
L2  X ← 0 (N values);  X[map(m)] ← D[m] for m = 0..M-1
L3  x ← F_Nᴴ X                                   ▷ N-point inverse DFT
L4  send (x[N-cp..N-1], x)                       ▷ cyclic prefix
L5  Y ← F_N (received samples cp..cp+N-1)
L6  Z[m] ← conj(H[k]) Y[k] / (|H[k]|² + σ²) with k = map(m), for m = 0..M-1
L7  return F_Mᴴ Z                                ▷ M-point inverse DFT
```

**Mappings.** Localized: $\mathrm{map}(m) = (r + m) \bmod N$, a block of adjacent subcarriers starting at $r$. Interleaved: $\mathrm{map}(m) = r + Qm$, every $Q$-th subcarrier.

**The channel.** With a channel $h[0..\ell]$, $\ell \le cp$, the prefix makes the convolution circular, so $Y[k] = H[k] X[k]$ plus noise, with $H[k] = \sum_l h[l] e^{-j 2\pi k l/N}$. Line L6 is one-tap MMSE equalization with the noise variance $\sigma^2$ per subcarrier; $\sigma^2 = 0$ gives [zero forcing](/zero-forcing-equalizer/), and then the round trip is exact without noise.

**The interleaved signal.** With $X[r + Qm] = D[m]$,

$$x[n] = \frac{1}{\sqrt N}\sum_{m} D[m]\, e^{j 2\pi (r + Qm) n / N} = \frac{e^{j 2\pi r n/N}}{\sqrt Q}\; d[n \bmod M],$$

because $\frac{1}{\sqrt M}\sum_m D[m] e^{j 2\pi m n/M} = d[n \bmod M]$. The $N$ samples are the data repeated $Q$ times, scaled by $1/\sqrt Q$ and rotated by a phase ramp. At these samples the PAPR is that of the data alone: exactly 0 dB for QPSK. The localized signal with $r = 0$ passes through $d[i]/\sqrt Q$ at the samples $n = Qi$ and interpolates between them with a periodic sinc.

**Cost.** The transmitter adds an $M$-point DFT to the $N$-point inverse DFT of OFDMA, and the receiver adds an $M$-point inverse DFT, so one symbol costs $O(N \log N + M \log M)$ operations.

## Classic examples

**PAPR against OFDMA.** Take $N = 64$, $M = 16$, oversampling by 4 for the measurement, and 1000 random blocks (Python `random.Random(3)`). OFDMA here means the same 16 subcarriers without the DFT spreading.

| constellation | signal | mean PAPR | 99 percent below | $\Pr(> 6\ \mathrm{dB})$ |
|---|---|---|---|---|
| QPSK | OFDMA | 6.29 dB | 8.77 dB | 0.519 |
| QPSK | SC-FDMA, localized | 4.49 dB | 6.50 dB | 0.048 |
| QPSK | SC-FDMA, interleaved | 4.46 dB | 6.42 dB | 0.035 |
| 16-QAM | OFDMA | 6.23 dB | 8.83 dB | 0.503 |
| 16-QAM | SC-FDMA, localized | 4.97 dB | 7.00 dB | 0.103 |
| 16-QAM | SC-FDMA, interleaved | 4.88 dB | 7.00 dB | 0.099 |

For QPSK, SC-FDMA saves 1.8 dB in the mean and 2.3 dB at the 99 percent point. For 16-QAM it saves 1.3 dB and 1.8 dB, because the 16-QAM points themselves have a PAPR of up to 2.55 dB. The interleaved signal is 0 dB for QPSK at its $N$ samples, but its peaks between the samples bring it to the same level as the localized signal. Without a pulse-shaping filter the two mappings differ little. A spectral shaping filter, such as a [raised-cosine](/raised-cosine-filter/) taper on the subcarriers, lowers both further at the cost of bandwidth.

**Full band.** If one user takes all $N$ subcarriers with the localized mapping and $r = 0$, then lines L1 to L3 give $F_N^H F_N d = d$: plain single-carrier transmission with a cyclic prefix and [frequency-domain equalization](/frequency-domain-equalization/), as described by Falconer and his coauthors.

**Through a channel.** With $N = 64$, $M = 16$, a prefix of 4 and a random 5-tap channel, lines L5 to L7 with $\sigma^2 = 0$ return the data to within rounding error for both mappings and any start $r$.

## Variations

- **Localized or interleaved.** Localized blocks allow scheduling on the best part of the band for each user; interleaved combs give frequency diversity and the exact repetition structure above. LTE uses localized blocks.
- **Pulse shaping.** Multiply the $M$ DFT outputs by a spectral window, using some extra subcarriers, to lower the PAPR further.
- **Pilots.** The reference signals of an SC-FDMA uplink are usually constant-amplitude sequences, such as [Zadoff-Chu sequences](/zadoff-chu-sequence/), placed in their own SC-FDMA symbols so that their PAPR is also low.
- **Clustered DFT-spread OFDM.** The $M$ outputs go to several separated blocks. This gives more scheduling freedom and a somewhat higher PAPR.
- **Nonlinear receivers.** Decision feedback or turbo equalization in the frequency domain recovers part of the loss of linear equalization on channels with deep fades.

## Pitfalls

- **Measuring at the sample rate.** At the $N$ samples an interleaved QPSK signal has a PAPR of exactly 0 dB, but the analog signal has peaks between them. Measure with oversampling by 4.
- **Forgetting the scale.** With an unscaled $M$-point DFT in line L1 and an inverse DFT scaled by $1/N$ in line L3, the interleaved samples are $d[n \bmod M]/Q$ instead of $d[n \bmod M]/\sqrt Q$, and the power is off by the factor $Q$. Use unitary DFTs in lines L1 and L3.
- **Equalizing in time.** The data are not on the subcarriers, so a decision per subcarrier is wrong. Equalize per subcarrier in line L6, then take the inverse DFT in line L7, then decide.
- **Zero forcing on deep fades.** With $\sigma^2 = 0$ in line L6, one weak subcarrier enhances the noise, and the inverse DFT spreads that noise over all $M$ symbols. Use the MMSE weights.
- **A prefix shorter than the channel.** The convolution is no longer circular and line L6 leaves interference between subcarriers and between symbols. The prefix must cover the delay spread.

## Exercises

1. Show that with the interleaved mapping and $Q = N/M$, the transmitted samples are $x[n] = e^{j 2\pi r n/N}\, d[n \bmod M]/\sqrt Q$.
2. Show that with $M = N$ and the localized mapping at $r = 0$, SC-FDMA is single-carrier transmission with a cyclic prefix.
3. With zero forcing and white noise of variance $\sigma^2$ per subcarrier, show that each recovered symbol has the noise variance $\frac{1}{M}\sum_m \sigma^2/|H[\mathrm{map}(m)]|^2$, the same for every symbol, while in OFDMA symbol $m$ has $\sigma^2/|H[\mathrm{map}(m)]|^2$.
4. Two users share $N = 64$ subcarriers with $M = 32$ each, one on the even and one on the odd subcarriers. Show that their signals are orthogonal over one symbol.
5. Explain why the localized SC-FDMA signal at oversampling 1 has almost the same PAPR as at oversampling 4 when $M = N/4$, using the fact that the $N$ samples already oversample the $M$ data symbols by 4.

## References
