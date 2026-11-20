---
tag: E8S9AK
kind: technique
slug: filter-bank-multicarrier
name: Filter bank multicarrier
aliases:
- FBMC
- "OFDM/OQAM"
area: communications/ofdm-and-multicarrier
level: advanced
summary: "Multicarrier transmission with a well-localized prototype filter on each subcarrier in place of a rectangular pulse. Offset QAM keeps the full rate with no cyclic prefix and very low sidelobes."
prereqs: [multicarrier-modulation, orthogonal-frequency-division-multiplexing, pulse-shaping, quadrature-amplitude-modulation]
see_also: [generalized-frequency-division-multiplexing, universal-filtered-multicarrier, sc-fdma, cyclic-prefix, polyphase-decomposition, nyquist-isi-criterion, root-raised-cosine-filter, short-time-fourier-transform]
sources:
  - paper: doi:10.1109/TCOM.1967.1089674
    title: "Burton R. Saltzberg, Performance of an efficient parallel data transmission system, IEEE Transactions on Communication Technology 15(6), 1967, pages 805 to 811"
    locator: "parallel transmission on overlapping subchannels with the quadrature components staggered by half a symbol period"
  - paper: doi:10.1109/MSP.2011.940267
    title: "Behrouz Farhang-Boroujeny, OFDM versus filter bank multicarrier, IEEE Signal Processing Magazine 28(3), 2011, pages 92 to 112"
    locator: "the OQAM synthesis and analysis filter banks, the real orthogonality, the polyphase implementation and the comparison with OFDM"
---

Filter bank multicarrier (FBMC) is a family of multicarrier schemes in which every subcarrier carries a pulse shaped by a prototype filter $g$ that is well localized in both time and frequency, instead of the rectangular pulse of [OFDM](/orthogonal-frequency-division-multiplexing/). The rectangular pulse gives each OFDM subcarrier a sinc spectrum with sidelobes that fall slowly, so OFDM needs guard bands and tight synchronization between users. A good prototype gives sidelobes that are orders of magnitude lower. The common form is OFDM/OQAM (offset QAM): each complex QAM symbol is split into its real and imaginary parts, which are sent half a symbol period apart, and the pulses carry the phases $j^{k+m}$. The pulses are then orthogonal in the real sense, which is enough for real symbols, and the scheme reaches the full symbol rate without a [cyclic prefix](/cyclic-prefix/). Saltzberg (1967) introduced the staggered form for parallel data transmission. The page uses $j$ for the imaginary unit, $M$ subcarriers and a real prototype of unit energy.

## In plain words

OFDM cuts every tone off sharply at the end of each symbol, and these sharp edges spread the energy of each tone far into its neighbors' frequencies. FBMC shapes each tone with a smooth window that starts and ends gently, so its energy stays close to its own frequency. The smooth windows are longer and overlap in time, and with ordinary complex symbols they would disturb each other. The trick is to send the real half and the imaginary half of each symbol at different times, half a symbol apart. The disturbance from the neighbors then always lands on the half the receiver does not read at that time. The receiver keeps only the half it wants and recovers every symbol.

## When it applies

- The spectrum must be well contained: narrow guard bands, coexistence with other systems, or uplink users that are not perfectly synchronized in time and frequency.
- The channel is nearly flat over one subcarrier and nearly constant over one prototype length, so a one-tap equalizer per subcarrier still works without a cyclic prefix.
- Transmission is in long bursts or continuous, so that the filter tails of $KM - 1$ samples at the start and end of a burst cost little.
- The system does not use schemes that need complex orthogonality between the pulses, such as Alamouti space-time coding applied directly on each subcarrier.

## The template

```pseudo id=main
FBMC-OQAM(c[0..S-1][0..M-1], g[0..D], M)
L1  for each i, k:  a[2i][k] ← Re c[i][k];  a[2i+1][k] ← Im c[i][k]      ▷ OQAM staggering
L2  s[n] ← Σ_m Σ_k a[m][k] · g[n - mM/2] · e^{j2πk(n - D/2)/M} · j^(k+m)
L3  â[m][k] ← Re Σ_n s[n] · conj( g[n - mM/2] · e^{j2πk(n - D/2)/M} · j^(k+m) )
L4  ĉ[i][k] ← â[2i][k] + j · â[2i+1][k]
```

**Real orthogonality.** Write $g_{k,m}[n] = g[n - mM/2]\, e^{j 2\pi k (n - D/2)/M}\, j^{k+m}$. The prototype is chosen so that

$$\mathrm{Re}\,\langle g_{k,m}, g_{k',m'} \rangle = \delta_{kk'}\, \delta_{mm'}.$$

Then line L3 returns $\hat a[m][k] = \sum_{m', k'} a[m'][k']\, \mathrm{Re}\langle g_{k',m'}, g_{k,m}\rangle = a[m][k]$ on a noiseless channel. The imaginary parts $\langle g_{k',m'}, g_{k,m} \rangle$ are not zero. They form the intrinsic interference, which line L3 discards by taking the real part.

**Density.** There are $M$ real symbols every $M/2$ samples, so $2M$ real values, or $M$ complex values, per $M$ samples: the rate of OFDM without the prefix. A complex-orthogonal system at this density with a pulse well localized in time and frequency is impossible, by the Balian-Low theorem of time-frequency analysis, and the offset structure is the way around it.

**Prototypes.** With overlap factor $K$ the prototype has about $KM$ taps. The half-sine $g[n] = \sqrt{2/M}\,\sin(\pi(n + 1/2)/M)$, $n = 0, \ldots, M - 1$, has $K = 1$ and is exactly real-orthogonal. The PHYDYAS prototype has $K = 4$ and is defined by its frequency samples $H_0 = 1$, $H_1 = 0.97195983$, $H_2 = \sqrt 2/2$, $H_3 = 0.23514695$, with $H_1^2 + H_3^2 = 1$:

$$g[n] \propto H_0 + 2 \sum_{i=1}^{3} (-1)^i H_i \cos\Big(\frac{2\pi i (n + 1)}{4M}\Big), \qquad n = 0, \ldots, 4M - 2.$$

It is nearly real-orthogonal.

**Cost.** Lines L2 and L3 are written directly above. A real modem computes them with one $M$-point FFT and a [polyphase](/polyphase-decomposition/) network of $K$ taps per branch every $M/2$ samples, $O(M \log M + KM)$ per half period. The FFT runs twice per symbol period, so the work is at least twice that of OFDM.

## Classic examples

**Exact reconstruction with the half-sine.** With $M = 8$ and 6 real symbol slots, the real parts of all pulse inner products match the identity to within $6 \cdot 10^{-15}$, while the largest imaginary part is 0.5. Five blocks of random 16-QAM symbols pass through lines L1 to L4 and come back to within rounding error.

**PHYDYAS.** With $M = 8$ and 10 slots, the real parts of the inner products differ from the identity by at most $2.0 \cdot 10^{-4}$, and the largest intrinsic interference term is 0.564. Random 16-QAM symbols come back with a mean squared error 70 dB below the symbol energy, which is far below the noise in practice.

**Spectral containment.** For $M = 16$, the fraction of the energy of one subcarrier pulse that lies more than $e$ subcarrier spacings from its center:

| pulse | $e = 1$ | $e = 2$ | $e = 4$ |
|---|---|---|---|
| rectangular (OFDM) | $9.6 \cdot 10^{-2}$ | $4.7 \cdot 10^{-2}$ | $2.0 \cdot 10^{-2}$ |
| half-sine, $K = 1$ | $2.9 \cdot 10^{-2}$ | $2.1 \cdot 10^{-3}$ | $1.4 \cdot 10^{-4}$ |
| PHYDYAS, $K = 4$ | $2.7 \cdot 10^{-5}$ | $8.6 \cdot 10^{-8}$ | $1.3 \cdot 10^{-9}$ |

The PHYDYAS pulse keeps all but $3 \cdot 10^{-5}$ of its energy within one spacing of its center, while the OFDM pulse still has 2 percent beyond four spacings.

## Variations

- **Filtered multitone.** Use subcarriers that do not overlap in frequency, with complex QAM and no offset. It needs no real-orthogonality but loses rate to the gaps between subcarriers.
- **Cosine-modulated multitone.** A real-valued baseband version with PAM, proposed for wired systems.
- **FBMC-QAM.** Send complex QAM directly, for example with different prototypes on even and odd subcarriers, and accept a small loss of orthogonality in return for simpler MIMO schemes.
- **Frequency-spreading receiver.** Replace the polyphase network by a $KM$-point FFT followed by a short filter across adjacent bins.
- **Other prototypes.** Prototypes designed by optimization, or derived from the isotropic orthogonal transform algorithm or from a [root-raised-cosine](/root-raised-cosine-filter/) response, trade time and frequency localization.

## Pitfalls

- **Expecting complex orthogonality.** Taking the full complex inner product in line L3 instead of its real part adds the intrinsic interference, about 0.5 of a neighbor's amplitude. Keep the real part in line L3.
- **Pilots without care.** A pilot alone sees the intrinsic interference from its data neighbors as an imaginary term, so a plain channel estimate is wrong. Surround pilots with guard symbols, or choose a neighbor so that the interference at the pilot cancels.
- **Wrong phase pattern.** The phases $j^{k+m}$ in lines L2 and L3 must match; other valid patterns exist, but the transmitter and receiver must use the same one.
- **Short bursts.** Each burst has filter tails of about $KM$ samples. For short packets this overhead is larger than the cyclic prefix it replaces.
- **Long delay spread.** Without a prefix, a channel whose delay spread is a large fraction of $M$ breaks the one-tap model. Use a multi-tap equalizer per subcarrier or a larger $M$.

## Exercises

1. Show that the half-sine prototype of length $M$ has unit energy and is symmetric.
2. Show that if $\mathrm{Re}\langle g_{k,m}, g_{k',m'}\rangle = \delta_{kk'}\delta_{mm'}$, then line L3 recovers every real symbol exactly on a noiseless channel.
3. Count the real symbols per sample in OFDM/OQAM and in OFDM with a prefix of length $M/8$, and compare.
4. For the PHYDYAS coefficients, check that $H_1^2 + H_3^2 = 1$ and $H_0^2 + H_2^2 \cdot 2 = 2$, and explain the role of these conditions in the Nyquist property of $|G(f)|^2$.
5. Explain why a pilot with value $p$ and data neighbors receives $H(p + j u)$ for some real $u$, and why $u$ depends on the data.

## References
