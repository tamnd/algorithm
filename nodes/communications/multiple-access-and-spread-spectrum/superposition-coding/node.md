---
tag: Y3706V
kind: technique
slug: superposition-coding
name: Superposition coding
aliases:
- layered broadcast coding
area: communications/multiple-access-and-spread-spectrum
level: advanced
summary: Adds the codewords of several users at different powers, which reaches the capacity region of the degraded broadcast channel.
prereqs: [channel-capacity, additive-white-gaussian-noise-channel, mac-capacity-region]
see_also: [non-orthogonal-multiple-access, successive-interference-cancellation, dirty-paper-coding, time-division-multiple-access, frequency-division-multiple-access, pulse-amplitude-modulation, multilevel-coding, sparse-code-multiple-access]
sources:
  - paper: doi:10.1109/TIT.1972.1054727
    title: Thomas M. Cover, Broadcast channels, IEEE Transactions on Information Theory 18(1), 1972
    locator: pp. 2 to 14 (superposition of a cloud code for the weak receiver and a satellite code for the strong receiver; the Gaussian and binary symmetric examples)
  - paper: doi:10.1109/TIT.1974.1055184
    title: Patrick P. Bergmans, A simple converse for broadcast channels with additive white Gaussian noise, IEEE Transactions on Information Theory 20(2), 1974
    locator: pp. 279 to 280 (superposition coding is optimal for the Gaussian broadcast channel)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Chapter 15, Section 15.6 (the broadcast channel, the degraded broadcast channel and its capacity region by superposition coding, and the Gaussian broadcast channel)
  - book: isbn:9780521845274
    title: David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005
    locator: Chapter 6, Section 6.2 (downlink AWGN channel, superposition coding with successive cancellation, and the comparison with orthogonal schemes)
---

Superposition coding sends messages to several receivers at once by adding their codewords, each at its own power, into one transmitted signal. The receiver with the weakest channel decodes only its own message and treats the rest as noise. A receiver with a stronger channel first decodes the messages meant for the weaker receivers, subtracts them, and then decodes its own. Cover introduced it in 1972 for the broadcast channel (one sender, many receivers), and on the scalar Gaussian broadcast channel it reaches the whole capacity region. It is a transmitter technique, the dual of the [MAC capacity region](/mac-capacity-region/): in the uplink the channel adds the users' signals, while here the sender adds them on purpose. [Non-orthogonal multiple access](/non-orthogonal-multiple-access/) is the system that uses superposition coding with [successive interference cancellation](/successive-interference-cancellation/) in a cellular downlink. For a broadcast channel with several transmit antennas, superposition is no longer enough, and [dirty paper coding](/dirty-paper-coding/) takes its place.

## In plain words

A base station talks to a near user and a far user at the same time, in the same band. It sends a loud message for the far user and a quiet message for the near user, added together.

The far user hears the loud message clearly, and the quiet one sounds like a little extra noise. So the far user just decodes the loud message.

The near user hears both messages well. It decodes the loud message first, even though it is not for this user. Then it takes it away and decodes the quiet message, which is now clean.

Both users get a better deal than if they took turns. The near user needs only a little power for a high rate, because its channel is good.

## When it applies

- One sender serves two or more receivers whose channel qualities differ, and the sender knows the order of the qualities.
- The channel is degraded: each weaker receiver gets a noisier version of what a stronger receiver gets. The scalar Gaussian broadcast channel, $y_k = h_k x + w_k$, is always degraded after scaling, with the order given by $|h_k|^2 / N_k$.
- The strong receivers can afford to decode the messages of the weak ones. This costs decoder work and needs the codebooks of the weak users.
- The channel gains are far apart. Then the gain over time sharing is large. For equal gains, superposition and time sharing give the same region.
- For broadcast with several transmit antennas the channel is not degraded in general; use precoding and [dirty paper coding](/dirty-paper-coding/) there.

## The template

Take two receivers on a complex Gaussian broadcast channel, $y_k = x + w_k$ with $w_k \sim \mathcal{CN}(0, N_k)$ and $N_1 < N_2$, so receiver 1 is strong and receiver 2 is weak. (A channel gain $h_k$ folds into $N_k$ as $N_k / |h_k|^2$.) The power constraint is $E|x|^2 \le P$. Define $\mathrm{SNR}_k = P / N_k$, which is $E_s/N_0$ per complex symbol at receiver $k$. Choose a power split $\alpha \in [0, 1]$.

```pseudo id=main
SUPERPOSE(m_1, m_2, alpha)
L1  c_2 ← codeword of m_2 from a Gaussian code of power (1 - alpha) P     ▷ cloud center
L2  c_1 ← codeword of m_1 from a Gaussian code of power alpha P           ▷ satellite
L3  send x ← c_1 + c_2
DECODE-WEAK(y_2)
L4  decode m_2 from y_2, with c_1 + w_2 as noise
DECODE-STRONG(y_1)
L5  decode m_2 from y_1, with c_1 + w_1 as noise
L6  subtract c_2(m_2) from y_1
L7  decode m_1 from y_1 - c_2
```

The rates are (a closed form for Gaussian codes on this channel, Cover and Thomas, Section 15.6)

$$R_2 = \log_2\!\left(1 + \frac{(1 - \alpha) P}{\alpha P + N_2}\right), \qquad R_1 = \log_2\!\left(1 + \frac{\alpha P}{N_1}\right).$$

Line L5 succeeds whenever L4 does, because receiver 1 has less noise: $(1 - \alpha) P / (\alpha P + N_1) \ge (1 - \alpha) P / (\alpha P + N_2)$. As $\alpha$ runs from 0 to 1, these pairs trace the boundary of the capacity region of the Gaussian broadcast channel; Bergmans 1974 proved that no scheme does better (a theorem). For $K$ users ordered from strong to weak, user $k$ decodes and removes the messages of all weaker users and treats the stronger users' layers as noise.

**Cost.** Each strong receiver runs one decoder per weaker layer plus its own, so the decoder work grows with the number of layers below it. The encoder only adds the layers.

## Classic examples

**Two users far apart.** Let $P/N_1 = 100$ (20 dB) and $P/N_2 = 10$ (10 dB), and give the strong user $\alpha = 0.2$ of the power. Then the weak user gets $R_2 = \log_2(1 + 8/3) = 1.8745$ bits per channel use, and the strong user gets $R_1 = \log_2(1 + 20) = 4.3923$, a sum of 6.2668. With time sharing, half the time each, the rates are $0.5 \log_2 101 = 3.3291$ and $0.5 \log_2 11 = 1.7297$. To give the weak user the same 1.8745 by time sharing, it needs a fraction $1.8745 / \log_2 11 = 0.5418$ of the time, and the strong user is left with $0.4582 \log_2 101 = 3.0505$. Superposition gives the strong user 44 percent more at the same rate for the weak user. All values were computed with the formulas above.

**4-PAM as two layers.** Superpose two real BPSK layers $b_2, b_1 \in \{+1, -1\}$ with powers 0.8 and 0.2: $x = \sqrt{0.8}\, b_2 + \sqrt{0.2}\, b_1$. The four points are $\pm 1.3416$ and $\pm 0.4472$, which is unit-energy [4-PAM](/pulse-amplitude-modulation/) ($\pm 3/\sqrt{5}$, $\pm 1/\sqrt{5}$). The weak receiver reads $b_2$ from the sign of $y$. The strong receiver reads $b_2$, subtracts $\sqrt{0.8}\, b_2$, and reads $b_1$ from the sign of the rest. With $x = \sqrt{0.8}\, b_2 + \sqrt{0.2}\, b_2 b_1$, the bit labels from the top point down are 00, 01, 11, 10, which is a Gray labeling. Digital broadcast systems use this idea as hierarchical modulation.

**Broadcast of a common message.** In Cover's view the weak user's codewords are cloud centers and the strong user's codewords are satellites around each center. The weak receiver sees only which cloud was sent; the strong receiver resolves the satellite inside the cloud.

## Variations

- **Hierarchical modulation.** A fixed constellation with layers of different protection, as in the 4-PAM example. DVB-T has a hierarchical mode of this kind.
- **NOMA.** Power-domain [non-orthogonal multiple access](/non-orthogonal-multiple-access/) is superposition coding in the downlink with practical codes, plus user pairing and power allocation.
- **Rate splitting.** A message is split into a common part, decoded by all receivers, and a private part. Superposition of the common and private parts gives schemes for the interference channel (Han and Kobayashi 1981) and for downlinks with imperfect channel knowledge.
- **Broadcast with degraded message sets.** One message for all receivers and one only for the strong receiver; superposition coding is again optimal.
- **Layered coding for fading.** A sender that does not know the fade sends layers so that a receiver decodes as many layers as its fade allows. This is the broadcast approach to slow fading.
- **Multiple antennas.** The MIMO broadcast channel is not degraded. [Dirty paper coding](/dirty-paper-coding/) reaches its capacity region; superposition with SIC reaches only part of it.

## Pitfalls

- **Wrong decoding order.** The weak receiver must never try to decode the strong user's layer. The order of decoding follows the order of channel quality, not of power.
- **Error propagation.** If the strong receiver decodes the weak user's layer wrongly, it subtracts the wrong signal and its own decoding fails. With practical codes this pushes the power split away from the ideal value.
- **Equal channels give no gain.** If $N_1 = N_2$, superposition gives the same region as time sharing. The gain comes from the gap between the channels.
- **Rate of the weak layer limits the strong user.** The strong receiver must decode the weak layer, so the weak layer's rate must be below what the strong receiver supports too. This holds automatically in a degraded channel, but not if the order is misjudged because of stale channel knowledge.
- **Codebooks.** The strong receiver needs the weak user's codebook and modulation. In a real system this is extra signaling, and it means the weak user's data is not private from the strong receiver.

## Exercises

1. Show that, for $N_1 < N_2$, the pair $(R_1, R_2)$ of the template satisfies $R_1 + R_2 \le \log_2(1 + P/N_1)$, with equality only at $\alpha = 1$.
2. For $P/N_1 = 100$ and $P/N_2 = 10$, find $\alpha$ such that $R_1 = R_2$. Compare the common rate with that of time sharing with equal rates.
3. Show that with $N_1 = N_2$ the superposition region equals the time-sharing region $R_1 + R_2 \le \log_2(1 + P/N_1)$.
4. In the 4-PAM example, compute the minimum distance seen by the weak receiver for $b_2$ and by the strong receiver for $b_1$, before noise. (Answer: $2(\sqrt{0.8} - \sqrt{0.2}) = 0.8944$ between the inner points for $b_2$, and $2 \sqrt{0.2} = 0.8944$ for $b_1$ after cancellation.)
5. Extend the template to three users and write the rate of the middle user.

## References
