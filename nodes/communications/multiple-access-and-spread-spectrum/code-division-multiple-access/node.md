---
tag: 7RH0C4
kind: technique
slug: code-division-multiple-access
name: Code-division multiple access
aliases:
- CDMA
area: communications/multiple-access-and-spread-spectrum
level: intro
summary: "Lets all users share the same time and band by giving each a spreading code with low crosscorrelation to the others; the receiver picks out a user by correlating with its code."
prereqs: [direct-sequence-spread-spectrum, cross-correlation]
see_also: [direct-sequence-spread-spectrum, multiuser-detection, near-far-problem, gold-sequences, ovsf-codes, rake-receiver, frequency-division-multiple-access, time-division-multiple-access]
sources:
  - paper: doi:10.1109/25.289411
    title: "Klein S. Gilhousen, Irwin M. Jacobs, Roberto Padovani, Andrew J. Viterbi, Lindsay A. Weaver and Charles E. Wheatley, On the capacity of a cellular CDMA system, IEEE Transactions on Vehicular Technology 40(2), 1991"
    locator: "the capacity of a CDMA cell in users, from the processing gain and the required Eb/I0, with power control, voice activity and sectorization"
  - book: isbn:9780521845274
    title: "David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005"
    locator: "Section 4.3, CDMA"
  - book: isbn:9780072957167
    title: "John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008"
    locator: "Chapter 12, Spread spectrum signals for digital communications, and Chapter 16, Multiuser communications"
  - book: isbn:9780521593731
    title: "Sergio Verdú, Multiuser Detection, Cambridge University Press, 1998"
    locator: "Chapters 4 to 7 (receivers for the CDMA channel)"
---

Code-division multiple access, or CDMA, lets many users send at the same time in the same frequency band. Each user multiplies its data by its own fast sequence of chips, its code or signature, which spreads the signal over a band much wider than the data needs, as in [direct-sequence spread spectrum](/direct-sequence-spread-spectrum/). The receiver correlates the sum of all signals with the code of one user. That user's signal adds up coherently over the $N$ chips of a symbol, while each other user contributes only its [crosscorrelation](/cross-correlation/) with that code. If the codes are nearly orthogonal, every user hears the others as a small noise. Unlike [FDMA](/frequency-division-multiple-access/) and [TDMA](/time-division-multiple-access/), CDMA has no hard limit on the number of users: each new user adds a little interference for everyone. It was the air interface of IS-95, of the third generation systems UMTS and cdma2000, and of GPS. Its main weakness is the [near-far problem](/near-far-problem/), which is solved by power control or by [multiuser detection](/multiuser-detection/).

## In plain words

Imagine a room where many pairs of people talk at the same time, each pair in a different language. You can follow your own partner because you understand only that language, and the other talk sounds like a murmur. CDMA gives each user a code instead of a language. The receiver for one user knows that code and listens for it. The other users' signals do not match the code, so they sound like weak noise. The more people talk, the louder the murmur gets, so there is a soft limit on how many users can share the room. If one person shouts, the others can no longer be heard, which is why CDMA systems control how loud each user is.

## When it applies

- Many users share one band and want to send at the same time without a central schedule of time slots or frequencies.
- The available bandwidth is much larger than the data rate of one user, so each symbol can be spread over many chips.
- The traffic is bursty or the users are often silent, as in voice, so the interference averages over many users.
- The system needs resistance to narrowband interference, multipath or interception, which spreading gives as a side effect.
- The receiver can control the users' powers, or can afford a multiuser detector.

## The template

```pseudo id=main
CDMA(users 1..K, data b_k[m], N chips per symbol)
L1  for each user k, choose a code c_k ∈ {±1}^N        ▷ hole: CODE-FAMILY
L2  transmitter k sends  x_k(t) = A_k b_k[m] c_k[i] for chip i of symbol m
L3  the channel adds all users:  y = Σ_k A_k b_k c_k / √N + noise
L4  set the powers A_k so the receiver can separate the users   ▷ hole: POWER-CONTROL
L5  receiver: z_k = c_kᵀ y / √N for every k               ▷ the matched filters
L6  decide all b_k from z_1..z_K                         ▷ hole: DETECTOR
```

The three holes are where designs differ. **CODE-FAMILY** chooses the codes: orthogonal codes such as Walsh or [OVSF codes](/ovsf-codes/) when the users are synchronous, and codes with low crosscorrelation at all shifts, such as [Gold sequences](/gold-sequences/), [Kasami sequences](/kasami-sequences/) or [m-sequences](/maximal-length-sequence/), when they are not. The [Welch bound](/welch-bound/) limits how small the crosscorrelations of many codes can be. **POWER-CONTROL** sets the received powers, usually equal for all users. **DETECTOR** is the single-user matched filter in the simplest systems, a [rake receiver](/rake-receiver/) on multipath channels, or a multiuser detector.

With unit-norm codes $s_k = c_k / \sqrt N$, the outputs of line L5 are $z = R A b + n$ with $R_{kj} = s_k^\top s_j$. The interference on user $k$ is $\sum_{j \ne k} R_{kj} A_j b_j$. For random $\pm 1$ codes, $E[R_{kj}^2] = 1/N$, so with equal powers the interference power on each user is about $(K - 1)/N$ times the user's own power. This is the sense in which the [processing gain](/processing-gain/) $N$ divides the interference.

**Capacity rule.** If all users arrive with equal power, the bandwidth is $W$, the data rate is $R_b$, and each user needs $E_b/I_0 = \gamma$, where $I_0$ is the interference density, then, ignoring thermal noise and other cells, the number of users is about

$$K \approx 1 + \frac{W / R_b}{\gamma}.$$

This is a rule of thumb from the analysis of Gilhousen and others. Voice activity, sectors and the interference from other cells change it by large factors.

## Classic examples

- **IS-95.** The second generation cellular standard used a chip rate of 1.2288 Mchip/s for 9.6 kbit/s of voice, a processing gain of 128, or 21.1 dB. On the downlink the users were separated by 64 Walsh codes; on the uplink, by long pseudonoise codes, with fast closed loop power control against the [near-far problem](/near-far-problem/). A [rake receiver](/rake-receiver/) combined the multipath components.
- **UMTS and cdma2000.** The third generation systems used wideband CDMA with [OVSF codes](/ovsf-codes/) to give users different spreading factors and data rates, and scrambling codes from [Gold sequences](/gold-sequences/) to separate cells and phones.
- **GPS.** Each satellite sends on the same carrier with its own C/A code, a Gold code of length 1023. The receiver finds each satellite by correlating with its code.
- **Multiuser receivers.** The [decorrelating detector](/decorrelating-detector/), the [MMSE detector](/mmse-multiuser-detector/) and [successive interference cancellation](/successive-interference-cancellation/) fill the DETECTOR hole with receivers that use all users' codes.

## Variations

- **Synchronous and asynchronous.** Synchronous users, as on a downlink, can use exactly orthogonal codes. Asynchronous users, as on an uplink, see the crosscorrelations at all relative shifts.
- **Short and long codes.** A short code repeats every symbol, so $R$ is constant and multiuser detection is easier. A long code changes from symbol to symbol, which makes the interference look random.
- **Frequency hopping CDMA.** Each user hops among frequencies by its own pattern, and users collide only when they hop to the same frequency at the same time.
- **Multicarrier CDMA.** The chips are sent on different subcarriers of an OFDM system instead of in time.
- **Random spreading.** Analyses with random codes give the large system limits of the detectors.
- **Overloaded and sparse CDMA.** More users than chips, with sparse codes and iterative detection, as in some designs for non-orthogonal multiple access.

## Pitfalls

- **Near-far.** With matched filter receivers, a strong user drowns a weak one through a small crosscorrelation. Use power control or a multiuser detector.
- **Orthogonality lost on the channel.** Orthogonal codes stay orthogonal only for aligned chips. Multipath delay and timing offsets bring back crosscorrelation. Walsh codes have poor correlation at shifts and need a scrambling code on top.
- **Interference limited.** Each extra user raises the interference of all others. The capacity is soft, and an overloaded cell degrades every user.
- **Counting users with the rule of thumb.** The capacity rule ignores other cells, fading and imperfect power control, and each of them can cost several dB.
- **Code shortage.** There are only $N$ orthogonal codes of length $N$, so orthogonal channelization needs a code tree such as OVSF and careful assignment.

## Exercises

1. Map the bits $0 \mapsto +1$ and $1 \mapsto -1$. Compute the normalized periodic crosscorrelation of the m-sequence $1001011$ with its cyclic shift $0010111$.
   *Answer.* The signs are $(-1, +1, +1, -1, +1, -1, -1)$ and $(+1, +1, -1, +1, -1, -1, -1)$. The products sum to $-1$, so the correlation is $-1/7$, as for every nonzero shift of an m-sequence of length 7.
2. Two codes have independent, equally likely $\pm 1$ chips. Show that the normalized crosscorrelation $\rho = \frac{1}{N} \sum_i c_i d_i$ has mean 0 and $E[\rho^2] = 1/N$.
   *Answer.* The products $c_i d_i$ are independent and equally likely $\pm 1$, with mean 0 and variance 1. So $\rho$ has mean 0 and variance $N / N^2 = 1/N$.
3. Use the capacity rule with $W / R_b = 128$ and $E_b/I_0 = 7$ dB. How many equal-power users fit in one isolated cell?
   *Answer.* $7$ dB is a ratio of about $5.01$, so $K \approx 1 + 128 / 5.01 \approx 26.5$, about 26 users before voice activity and sectors.
4. Two users have crosscorrelation $\rho$ and no noise. For which amplitude ratio does the matched filter of user 1 fail for some bits?
   *Answer.* $z_1 = A_1 b_1 + \rho A_2 b_2$ has the wrong sign for some $b_2$ when $|\rho| A_2 > A_1$, that is, when $A_2 / A_1 > 1/|\rho|$. At equality, $z_1 = 0$ for some bits, a tie.

## References
