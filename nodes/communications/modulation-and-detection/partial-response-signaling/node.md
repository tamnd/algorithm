---
tag: HBVC3V
kind: technique
slug: partial-response-signaling
name: Partial-response signaling
aliases:
- duobinary signaling
- correlative coding
area: communications/modulation-and-detection
level: core
summary: "Add known intersymbol interference on purpose, such as a_k + a_(k-1), so the pulse fits the minimum band 1/(2T) with a smooth spectrum. A precoder lets the receiver decide each symbol alone."
prereqs: [nyquist-isi-criterion, intersymbol-interference]
see_also: [nyquist-isi-criterion, intersymbol-interference, pulse-shaping, eye-diagram, maximum-likelihood-sequence-estimation, viterbi-equalizer, tomlinson-harashima-precoding, faster-than-nyquist-signaling]
sources:
  - paper: doi:10.1109/TCE.1963.6373379
    title: Adam Lender, The duobinary technique for high-speed data transmission, IEEE Transactions on Communication and Electronics 82(2), 1963
    locator: pp. 214 to 218 (three-level duobinary transmission at twice the rate of a binary signal in the same band, with a precoder)
  - paper: "E. R. Kretzmer, Generalization of a technique for binary data communication, IEEE Transactions on Communication Technology COM-14(1), 1966"
    locator: pp. 67 to 68 (the classes of partial-response systems)
  - paper: doi:10.1109/TCOM.1975.1092918
    title: Peter Kabal and Subbarayan Pasupathy, Partial-response signaling, IEEE Transactions on Communications COM-23(9), 1975
    locator: pp. 921 to 934 (the general system with an integer polynomial in the delay operator, the precoder, the spectra of the classes, and modified duobinary 1 - D^2 as Class IV)
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008
    locator: Section 9.2-2 (design of band-limited signals with controlled ISI, duobinary and modified duobinary) and Section 9.2-3 (data detection for controlled ISI, the precoder, and the performance of symbol-by-symbol detection)
---

Partial-response signaling sends symbols through a pulse whose samples at the symbol instants are a few known nonzero numbers, for example $x(0) = x(T) = 1$. The [intersymbol interference](/intersymbol-interference/) is then not removed but controlled: each sample is a fixed integer combination such as $c_k = a_k + a_{k-1}$. In exchange, the pulse can use exactly the minimum bandwidth $1/(2T)$ of the [Nyquist ISI criterion](/nyquist-isi-criterion/) with a spectrum that goes smoothly to zero at the band edge, which the sinc pulse cannot. A precoder at the transmitter makes the bit decisions independent of each other, and a sequence detector recovers almost all of the SNR that the simple detector loses.

## In plain words

A pulse that fits in the narrowest possible band and has no interference between symbols must stop sharply at the edge of the band, and such a sharp filter cannot be built. Partial response gives up on zero interference. It lets each symbol leak into the next one in a fixed, known way, for example by adding each symbol to the one before it. Then the pulse can fade out gently at the band edge, and filters for it are easy to make. The receiver knows the rule, so it can undo it. A small trick at the transmitter, called a precoder, makes the receiver able to read each bit from one sample alone, so that one wrong reading does not spoil the bits after it.

## When it applies

- The band is fixed at $1/(2T)$ for the symbol rate $1/T$, and the filters must be realizable, with no sharp edge.
- The channel already has a response close to a partial-response polynomial, as in magnetic recording, where the read head blocks DC and the pulse is smooth, and $1 - D^2$ or $(1 - D)(1 + D)^2$ fit the channel well.
- The signal must have no power at DC (a channel with transformers or a magnetic head): the classes with a factor $1 - D$ have a spectral null at $f = 0$.
- The levels of the symbols are integers, so that the sum $c_k$ takes a few known values. For a channel with non-integer taps, the generalization is [Tomlinson-Harashima precoding](/tomlinson-harashima-precoding/).

## The template

Write the controlled ISI as a polynomial $F(D) = \sum_{i=0}^{\nu} f_i D^i$ in the delay operator $D$, with integer taps and $f_0 = 1$. The overall pulse is $x(t) = \sum_i f_i\, \mathrm{sinc}(t/T - i)$, with $\mathrm{sinc}(u) = \sin(\pi u)/(\pi u)$, so its samples are $x(iT) = f_i$. The holes are $F$, the number $M$ of levels, and the detector DETECT. The data are digits $b_k \in \{0, \ldots, M - 1\}$.

```pseudo id=main
PARTIAL-RESPONSE-LINK(b_1, ..., b_N)           ▷ holes: F(D) = Σ f_i D^i, M, DETECT
L1  p_k ← 0 for k ≤ 0                           ▷ the precoder starts from a known state
L2  for k = 1 to N do
L3      p_k ← (b_k - Σ_{i=1..ν} f_i p_{k-i}) mod M ▷ the precoder
L4      a_k ← 2 p_k - (M - 1)                    ▷ an M-PAM level
L5      c_k ← Σ_{i=0..ν} f_i a_{k-i}             ▷ the controlled ISI, made by the pulse x(t)
L6      y_k ← c_k + w_k                          ▷ the receive sample, with noise
L7      ĉ_k ← DETECT(y_k)                        ▷ the nearest allowed value of c_k
L8      b̂_k ← ((ĉ_k + (M - 1) Σ_i f_i) / 2) mod M
L9  return b̂_1, ..., b̂_N
```

**Why line L8 works.** From line L4, $c_k = 2\sum_i f_i p_{k-i} - (M - 1)\sum_i f_i$. So $(c_k + (M - 1)\sum_i f_i)/2 = \sum_i f_i p_{k-i}$, and by line L3 this is $b_k$ modulo $M$. The decision on $b_k$ uses only $y_k$: one wrong $\hat c_k$ gives one wrong digit. Without the precoder ($p_k = b_k$) the receiver must compute $\hat b_k$ from $\hat c_k$ and its own earlier decisions, $\hat a_k = \hat c_k - \sum_{i \ge 1} f_i \hat a_{k-i}$, and one error then spreads to the following symbols.

**Duobinary.** $F(D) = 1 + D$ and $M = 2$. Line L3 is $p_k = b_k \oplus p_{k-1}$ (minus and plus are the same modulo $2$), $a_k = \pm 1$, and $c_k = a_k + a_{k-1} \in \{-2, 0, 2\}$. Line L8 gives $\hat b_k = 1$ if $\hat c_k = 0$ and $\hat b_k = 0$ if $\hat c_k = \pm 2$. The pulse is $x(t) = \mathrm{sinc}(t/T) + \mathrm{sinc}(t/T - 1)$, with spectrum

$$X(f) = 2T \cos(\pi f T)\, e^{-j\pi f T} \quad \text{for } |f| \le \frac{1}{2T}, \qquad 0 \text{ outside}.$$

It uses exactly the minimum band, and $|X(f)|$ falls to zero at the edge like a cosine instead of jumping. In time, $x(t)$ decays like $1/t^2$, not $1/|t|$ as the sinc does.

**A worked example.** Bits $1, 0, 1, 1, 0, 0, 1, 0$ with $p_0 = 0$ give the precoded bits $p = 1, 1, 0, 1, 1, 1, 0, 0$, the levels $a = 1, 1, -1, 1, 1, 1, -1, -1$ (with $a_0 = -1$), and the samples $c = 0, 2, 0, 0, 2, 2, 0, -2$. Reading $c = 0$ as $1$ and $c = \pm 2$ as $0$ gives back $1, 0, 1, 1, 0, 0, 1, 0$. If noise turns the fifth sample into $0$, only the fifth bit is wrong.

**The cost of symbol-by-symbol detection.** The three levels of duobinary are closer together for the same energy. Split $|X(f)|$ equally between a transmit filter and a matched receive filter, each with magnitude $\sqrt{|X(f)|}$. Then the energy per symbol and the noise variance at the sampler are both scaled by $\int |X(f)|\, df = 4/\pi$, while the distance from each level to a threshold stays $1$. For the same $E_b/N_0$ as binary PAM without ISI, the ratio of distance to noise is smaller by the factor $\pi/4$, a loss of $20 \log_{10}(4/\pi) = 2.1$ dB. With equally likely bits the middle level $0$ has two neighbors and occurs half of the time, so $P_b = \tfrac{3}{2} Q(\cdot)$ of that argument, with $Q$ the [Gaussian Q function](/gaussian-q-function/). A [maximum-likelihood sequence](/maximum-likelihood-sequence-estimation/) detector on the trellis of $F(D)$ recovers the loss at high SNR: no error event of $1 + D$ has a smaller distance than a single wrong symbol, whose distance uses the full energy of the pulse.

## Classic examples

- **Duobinary**, $1 + D$ (Class I), from Lender (1963): three levels and a spectral null at $f = 1/(2T)$; optical links use it to narrow the spectrum of the light. See also the [eye diagram](/eye-diagram/), which shows two eyes stacked on top of each other.
- **Dicode**, $1 - D$: a null at $f = 0$ and none at the band edge, a simple model of a magnetic recording channel.
- **Modified duobinary**, $1 - D^2$ (Class IV): nulls at $f = 0$ and at $f = 1/(2T)$. Its precoder is $p_k = b_k \oplus p_{k-2}$, and $\hat b_k = 1$ exactly when $\hat c_k = \pm 2$. With a [Viterbi](/viterbi-equalizer/) detector it is the PRML read channel of hard disk drives.
- **Extended classes**, such as $(1 - D)(1 + D)^2$, fit the smoother channels of denser recording.
- **Multilevel duobinary**: $1 + D$ with $M = 4$ gives $7$ levels of $c_k$ and $2$ bits per symbol at the minimum bandwidth.

## Variations

- **Sequence detection** instead of line L7 and L8: the [Viterbi algorithm](/viterbi-algorithm/) over the $M^\nu$ states of the polynomial recovers the 2.1 dB of duobinary.
- **Tomlinson-Harashima precoding**: a modulo precoder for any channel with known taps, not only integer ones.
- **Faster than Nyquist**: [faster-than-Nyquist signaling](/faster-than-nyquist-signaling/) also accepts ISI on purpose, but by sending symbols faster through an ordinary pulse.
- **Different split of the filters**: the overall $X(f)$ can be split between transmitter and receiver in any way; the equal split of the magnitude is best in white noise.

## Pitfalls

- **No precoder.** Decoding by subtracting the earlier decisions spreads one error over many bits.
- **Wrong start of the precoder.** The receiver of line L8 needs no state, but the first $\nu$ samples depend on the initial $p_k$ and $a_k$; the transmitter must send them as agreed.
- **Threshold placement.** Duobinary has three levels, so the thresholds are at $\pm 1$, not at $0$.
- **Non-integer channels.** If the real channel is only close to $F(D)$, the residual ISI moves the levels; an equalizer must shape the channel to the target first.
- **Counting the loss twice.** The 2.1 dB loss applies to symbol-by-symbol detection; with sequence detection there is almost none.

## Exercises

1. Show that for any integer polynomial $F(D)$ with $f_0 = 1$, line L8 returns $b_k$ when $\hat c_k = c_k$.
2. For modified duobinary $1 - D^2$ and $M = 2$, find the spectrum $X(f)$ and the values of $c_k$, and write the decision rule of line L8.
3. Encode the bits $0, 1, 1, 0, 1$ with the duobinary precoder from $p_0 = 0$, $a_0 = -1$, and list $c_k$. (The samples are $-2, 0, 0, -2, 0$.)
4. Without a precoder, $\hat a_k = \hat c_k - \hat a_{k-1}$. Show that one wrong $\hat c_k$ can make every later decision wrong when the true $c$ samples that follow are all $0$.
5. Show that the duobinary pulse $x(t) = \mathrm{sinc}(t/T) + \mathrm{sinc}(t/T - 1)$ has $x(T/2) = 4/\pi$.

## References
