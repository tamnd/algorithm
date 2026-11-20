---
tag: 5PQ8PD
kind: technique
slug: direct-sequence-spread-spectrum
name: Direct-sequence spread spectrum
aliases:
- DSSS
- direct-sequence spreading
area: communications/multiple-access-and-spread-spectrum
level: intro
summary: "Multiply each data symbol by a fast pseudorandom chip code, so that the signal fills a wide band. Correlating with the same code restores the symbol and spreads out interference."
prereqs: [processing-gain, maximal-length-sequence, matched-filter, additive-white-gaussian-noise-channel]
see_also: [frequency-hopping-spread-spectrum, code-division-multiple-access, rake-receiver, gold-sequences, ovsf-codes, serial-search-code-acquisition, delay-locked-loop, near-far-problem]
sources:
  - paper: doi:10.1109/TCOM.1982.1095533
    title: Raymond L. Pickholtz, Donald L. Schilling and Laurence B. Milstein, Theory of spread-spectrum communications, a tutorial, IEEE Transactions on Communications 30(5), 1982
    locator: pp. 855 to 884 (direct-sequence spreading, processing gain, jamming margin, code acquisition and tracking)
  - book: isbn:9780201633740
    title: Andrew J. Viterbi, CDMA, Principles of Spread Spectrum Communication, Addison-Wesley, 1995
    locator: The opening chapters on direct-sequence spreading and its use for multiple access
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, 5th edition, McGraw-Hill, 2008
    locator: The chapter on spread spectrum signals for digital communications
---

Direct-sequence spread spectrum (DSSS) sends each data symbol as a block of $N$ short pulses, the **chips**, whose signs follow a pseudorandom code known to the receiver. The chip rate is $N$ times the symbol rate, so the signal takes about $N$ times the bandwidth that the data needs. The receiver multiplies the received chips by the same code and adds them up over each symbol. This **despreading** collapses the wanted signal back into one strong value, while noise, narrowband interference and the signals of other codes stay spread out and add up only weakly. The factor by which the wanted signal gains over the interference is the [processing gain](/processing-gain/), about $N$. DSSS is the basis of [CDMA](/code-division-multiple-access/), of GPS and of the first Wi-Fi rates.

## In plain words

Each data bit is sent as a long, fast pattern of plus and minus pulses, chosen to look random. The receiver knows the pattern. It multiplies what it hears by the pattern, pulse by pulse, and adds up the results.

For the wanted signal every product has the same sign, so the sum grows large. For noise, for a steady tone, or for a user with another pattern, the products have mixed signs and mostly cancel. So the wanted bit stands out even when each single pulse is buried under the interference.

The cost is bandwidth: the fast pattern takes up a much wider band than the data alone. The receiver must also line up its copy of the pattern with the received one to within a fraction of a pulse, before it can decode anything.

## When it applies

- There is spare bandwidth, and a strong narrowband interferer, a jammer, or many other users must share the band.
- The receiver can find and follow the code timing: an acquisition step finds it to within about one chip, and a tracking loop keeps it there.
- Multipath delays are longer than one chip, so a [rake receiver](/rake-receiver/) can separate the paths and add them.
- Several users share the band at the same time, each with its own code, and their powers can be controlled. Without power control, a near user can swamp a far one; see [near-far problem](/near-far-problem/).
- The signal must be hard to detect or to read without the code: its power density can be below the noise floor.

## The template

Let $c = (c_0, \ldots, c_{N-1})$ be a code of $\pm 1$ chips, for example one period of an [m-sequence](/maximal-length-sequence/), and let $d_i \in \{+1, -1\}$ be the data symbols. The transmitter sends the chips $x[iN + n] = d_i c_n$. The receiver gets $r = x + $ interference and computes, for each symbol, the correlation with the code, which is a [matched filter](/matched-filter/) for one symbol:

$$z_i = \sum_{n=0}^{N-1} r[iN + n] \, c_n = N d_i + \sum_{n=0}^{N-1} e[iN + n] \, c_n,$$

where $e$ is the interference. With white noise of variance $\sigma^2$ per chip, the signal-to-noise ratio is $1/\sigma^2$ per chip and $N^2 / (N \sigma^2) = N/\sigma^2$ after despreading, a gain of $N$.

```pseudo id=main
SPREAD(d, c)                ▷ d data symbols ±1, c code of N chips ±1
L1  for each symbol d_i do
L2      send d_i c_0, d_i c_1, …, d_i c_{N-1}

DESPREAD(r, c)
L3  for each block i do z_i ← Σ_{n=0}^{N-1} r[iN + n] c_n
L4  return d̂_i ← sign(z_i) for each i
```

Spreading and despreading cost $O(N)$ operations per symbol. On a real link the chips are shaped pulses on a carrier, and the receiver must also find the code phase and the carrier before L3; see [serial-search code acquisition](/serial-search-code-acquisition/), [parallel code phase search](/parallel-code-phase-search/) and the [delay-locked loop](/delay-locked-loop/).

## Classic examples

- **Length 7.** With the m-sequence $1001011$ of $x^3 + x + 1$ and the mapping $0 \to +1$, $1 \to -1$, the code is $(-1, 1, 1, -1, 1, -1, -1)$. The symbols $(+1, -1)$ become $14$ chips, and despreading gives exactly $7$ and $-7$.
- **A constant jammer.** The chips of an m-sequence of length $N$ add up to $-1$, since the sequence has one more 1 than 0. A constant interferer of amplitude $A$ therefore adds exactly $-A$ to each correlator output, against $\pm N$ for the symbol. With $N = 127$ and $A = 40$, the jammer is $32.04$ dB stronger than the signal on each chip, but the outputs are $87$ and $-167$, and every decision is right.
- **White noise.** With $N = 31$ and noise variance $4$ per chip, the signal-to-noise ratio per chip is $-6.02$ dB. After despreading it is $31/4$, or $8.89$ dB.
- **Two users.** User 1 uses an m-sequence of length $31$, and user 2 uses a cyclic shift of it. Two different shifts of an m-sequence have periodic cross-correlation $-1$, so user 1 sees exactly $31 d_1 - d_2$. With [Gold sequences](/gold-sequences/) the cross-talk is larger but bounded, and there are many more codes.
- **GPS C/A code.** Each satellite spreads $50$ bit/s of navigation data with its own Gold code of $1023$ chips at $1.023$ Mchip/s, so one bit spans $20$ code periods and $20460$ chips.
- **IS-95 and WCDMA.** IS-95 spreads at $1.2288$ Mchip/s and separates the downlink users with Walsh codes of length $64$. WCDMA spreads at $3.84$ Mchip/s with [OVSF codes](/ovsf-codes/) and a long scrambling code.

## Variations

- **Short and long codes.** A short code repeats every symbol, which makes acquisition fast and allows [multiuser detection](/multiuser-detection/). A long code spans many symbols and makes the interference look more like noise.
- **Spreading with complex codes.** Two independent codes on the in-phase and quadrature branches (QPSK spreading) make the interference less dependent on carrier phase.
- **Code-shift keying.** Each group of $k$ bits selects one of $2^k$ codes; the receiver correlates with all of them and picks the largest. IEEE 802.11b at 5.5 and 11 Mbit/s uses a related scheme, complementary code keying.
- **Orthogonal codes in a synchronous downlink.** When all signals leave one transmitter at the same time, orthogonal codes such as [OVSF codes](/ovsf-codes/) remove the cross-talk on a single path.
- **Frequency hopping.** The other main way to spread is to hop the carrier; see [frequency-hopping spread spectrum](/frequency-hopping-spread-spectrum/).

## Pitfalls

- **The gain is not free against white noise.** Spreading does not change the energy per bit to noise density ratio, so the bit error rate on an [AWGN channel](/additive-white-gaussian-noise-channel/) is the same as without spreading. The gain is against interference whose power is fixed and does not grow with the bandwidth.
- **The code timing must be known.** An error of one chip or more makes the correlation fall to the off-peak level. Despreading only works after acquisition and with tracking.
- **Near-far.** The cross-talk from another user scales with its amplitude. A user near the base station can swamp a far user, unless the transmit powers are controlled.
- **Partial correlations.** In an asynchronous system, one symbol of the other user may change sign in the middle of the correlation window. The cross-talk is then an odd or partial correlation, not the periodic correlation, and it can be larger.
- **Bandwidth.** The signal needs $N$ times the bandwidth of the data. If the band is the limit and there is no interference to fight, DSSS lowers the [spectral efficiency](/spectral-efficiency/) of a single link.

## Exercises

1. Show that for an m-sequence of length $N$ and a constant interferer $A$, the correlator output is $N d_i - A$ exactly. How large can $A$ be before a symbol of $-1$ is decided wrongly?
2. Two users share the band with codes $c$ and $c'$ and periodic cross-correlation $\theta$. Write the output of the correlator for user 1 as a function of the two symbols, and find the largest $|\theta|$ that still allows error-free decisions without noise.
3. With white noise of variance $\sigma^2$ per chip, show that the variance of $z_i - N d_i$ is $N \sigma^2$, for any $\pm 1$ code.

## References
