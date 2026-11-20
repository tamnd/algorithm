---
tag: 0V0C3M
kind: theorem
slug: dirty-paper-coding
name: Dirty paper coding
aliases:
- Costa writing on dirty paper
area: communications/mimo-communications
level: advanced
summary: "Costa (1983): Gaussian interference known in advance to the transmitter costs no capacity. Weingarten, Steinberg and Shamai (2006) used it to get the MIMO broadcast capacity region."
prereqs: [additive-white-gaussian-noise-channel, channel-capacity, channel-coding-theorem]
see_also: [tomlinson-harashima-precoding, vector-perturbation-precoding, zero-forcing-precoding, mimo-capacity, mac-capacity-region, superposition-coding, lattice, weighted-sum-rate-maximization]
sources:
  - paper: doi:10.1109/TIT.1983.1056659
    title: "Max H. M. Costa, Writing on dirty paper, IEEE Transactions on Information Theory 29(3), 439-441, 1983"
    locator: "the channel Y = X + S + Z with Gaussian S known to the encoder, the capacity (1/2) log(1 + P/N) independent of the power of S, and the auxiliary variable U = X + alpha S with alpha = P/(P + N)"
  - paper: "S. I. Gelfand and M. S. Pinsker, Coding for channel with random parameters, Problems of Control and Information Theory 9(1), 19-31, 1980"
    locator: "the capacity max [I(U; Y) - I(U; S)] of a discrete memoryless channel whose state is known noncausally at the encoder"
  - book: isbn:9781107008731
    title: "Abbas El Gamal and Young-Han Kim, Network Information Theory, Cambridge University Press, 2011"
    locator: "Chapter 7 (channels with state), Section 7.5 (causal state information), Section 7.6 (noncausal state information, the Gelfand-Pinsker theorem and its proof by multicoding) and Section 7.7 (writing on dirty paper)"
  - paper: "Hanan Weingarten, Yossef Steinberg and Shlomo Shamai, The capacity region of the Gaussian multiple-input multiple-output broadcast channel, IEEE Transactions on Information Theory 52(9), 3936-3964, 2006"
    locator: "the proof that the dirty paper coding region is the capacity region of the Gaussian MIMO broadcast channel, by channel enhancement"
  - paper: doi:10.1109/TIT.2003.813523
    title: "Giuseppe Caire and Shlomo Shamai, On the achievable throughput of a multiantenna Gaussian broadcast channel, IEEE Transactions on Information Theory 49(7), 1691-1706, 2003"
    locator: "dirty paper coding for the multiantenna broadcast channel, the zero-forcing dirty paper scheme with a QR decomposition, and its comparison with linear precoding"
  - paper: "Uri Erez, Shlomo Shamai and Ram Zamir, Capacity and lattice strategies for canceling known interference, IEEE Transactions on Information Theory 51(11), 3820-3833, 2005"
    locator: "lattice strategies with dither and MMSE scaling that reach the dirty paper capacity for arbitrary interference, and the scalar and causal cases"
---

Dirty paper coding is the result of Costa (1983) that interference known in advance to the transmitter, but not to the receiver, does not lower the capacity of a Gaussian channel. If the channel is $y = x + s + w$ with Gaussian noise $w$ of power $N_0$ and Gaussian interference $s$ of any power, and the transmitter knows the whole sequence $s$ before it sends, the capacity is $\log_2(1 + P/N_0)$, the same as the [AWGN channel](/additive-white-gaussian-noise-channel/) with no interference. The kind of the page is theorem, but its name is that of a technique: the coding schemes that reach the bound (binning, lattice strategies and, as a scalar version, [Tomlinson-Harashima precoding](/tomlinson-harashima-precoding/)) are under Consequences. In a multiuser downlink, the transmitter knows the signals it sends to the other users, so it can treat them as known interference. With this idea, Weingarten, Steinberg and Shamai (2006) proved that dirty paper coding reaches the whole capacity region of the Gaussian MIMO broadcast channel; that consequence is their result, not Costa's. The linear precoders, such as [zero-forcing precoding](/zero-forcing-precoding/), are simpler schemes that approach this region.

## Statement

**Model.** The channel is complex and memoryless:

$$y_i = x_i + s_i + w_i, \qquad i = 1, \ldots, n,$$

with noise $w_i \sim \mathcal{CN}(0, N_0)$ i.i.d., interference $s_i \sim \mathcal{CN}(0, Q)$ i.i.d. for some $Q \ge 0$, and $w$, $s$ and the message independent. The encoder sees the message and the whole interference sequence $s^n = (s_1, \ldots, s_n)$ before the first channel use (noncausal knowledge). The decoder sees only $y^n$. Each codeword meets the power constraint $\frac{1}{n} \sum_{i=1}^n |x_i|^2 \le P$. Rates are in bits per complex channel use, and the error probability is averaged over the message, $s^n$ and $w^n$.

**Theorem (Costa 1983).** For every $Q \ge 0$, the capacity of this channel is

$$C = \log_2\!\left(1 + \frac{P}{N_0}\right).$$

Costa states the real form: for $Y = X + S + Z$ with $S \sim \mathcal{N}(0, Q I)$, $Z \sim \mathcal{N}(0, N I)$ and power $P$ per real symbol, $C = \frac{1}{2} \log_2(1 + P/N)$ per real channel use. The complex form follows from the same proof with circularly symmetric variables, or from the real form on the in-phase and quadrature parts with $N = N_0/2$ and power $P/2$ on each.

## In plain words

Think of a page that already has dirt on it, and a writer who knows where every spot of dirt is. The reader does not know where the dirt is. The obvious plan is to erase the dirt first, but that uses up all the ink when the dirt is heavy. Costa showed a better plan: the writer chooses, from many versions of each message, the version that fits best with the dirt that is already there, and writes only the difference. The reader then reads the message as if the page were clean.

For radio, the dirt is interference that the transmitter knows in advance, for example the signals that the same base station sends to other users at the same time. The result says that such interference costs no rate at all, no matter how strong it is. The receiver does not need to know the interference.

## Proof

The proof has an upper bound (the converse) and a matching scheme (achievability). Write $\mathrm{SNR} = P/N_0$.

**Converse.** Give the decoder $s^n$ as well. This can only help, so any rate that is achievable without it is achievable with it. Let $M$ be the message, uniform on $2^{nR}$ values and independent of $s^n$. By Fano's inequality, for a code with error probability $\epsilon_n \to 0$,

$$nR \le I(M; y^n, s^n) + n \delta_n = I(M; y^n \mid s^n) + n \delta_n,$$

with $\delta_n \to 0$, where the equality uses $I(M; s^n) = 0$. Since $x^n$ is a function of $(M, s^n)$ and $w^n$ is independent of $(M, s^n)$,

$$I(M; y^n \mid s^n) \le h(y^n \mid s^n) - h(y^n \mid M, s^n) = h(x^n + w^n \mid s^n) - h(w^n).$$

Conditioning does not increase differential entropy, and the entropy of a complex vector is at most the sum of the entropies of its entries, so $h(x^n + w^n \mid s^n) \le \sum_i h(x_i + w_i)$. A complex random variable with second moment $P_i + N_0$, where $P_i = \mathbb{E}|x_i|^2$, has differential entropy at most $\log_2(\pi e (P_i + N_0))$, the value of the circularly symmetric Gaussian law. With $h(w^n) = n \log_2(\pi e N_0)$,

$$nR \le \sum_{i=1}^n \log_2\!\left(1 + \frac{P_i}{N_0}\right) + n\delta_n \le n \log_2\!\left(1 + \frac{P}{N_0}\right) + n\delta_n,$$

by Jensen's inequality for the concave function $\log_2(1 + t/N_0)$ and $\frac{1}{n}\sum_i P_i \le P$. Let $n \to \infty$. This is also the capacity of the AWGN channel, since a decoder that knows $s^n$ can subtract it.

**The Gelfand-Pinsker theorem.** For a discrete memoryless channel $p(y \mid x, s)$ with i.i.d. state $s$ known noncausally at the encoder, Gelfand and Pinsker (1980) proved that the capacity is

$$C_{GP} = \max_{p(u \mid s),\ x = f(u, s)} \big[ I(U; Y) - I(U; S) \big],$$

with an auxiliary random variable $U$. The scheme behind the achievable part is random binning. Draw about $2^{n I(U; Y)}$ sequences $u^n$ i.i.d. from $p(u)$ and split them at random into $2^{nR}$ bins of about $2^{n I(U; S)}$ sequences each. To send message $m$, the encoder finds a $u^n$ in bin $m$ that is jointly typical with $s^n$; one exists with high probability because the bin holds more than $2^{n I(U;S)}$ sequences (the covering lemma). It sends $x_i = f(u_i, s_i)$. The decoder finds the unique $u^n$ that is jointly typical with $y^n$; it is unique with high probability because there are fewer than $2^{n I(U;Y)}$ sequences in total (the packing lemma). The rate is $R = I(U; Y) - I(U; S)$ minus an arbitrarily small margin. The full proof, and the standard extension to continuous alphabets with an average power constraint, are in El Gamal and Kim, Sections 7.6 and 7.7. We use the theorem without repeating that proof.

**Achievability.** Take $x \sim \mathcal{CN}(0, P)$ independent of $s$, and $u = x + \alpha s$ for a constant $\alpha$. Then $x = u - \alpha s$ is a function of $(u, s)$, and $u$, $s$ and $y = x + s + w$ are jointly circularly symmetric Gaussian. For two such scalars $a$ and $b$,

$$I(a; b) = \log_2 \frac{\mathrm{Var}(a)\, \mathrm{Var}(b)}{\mathrm{Var}(a)\, \mathrm{Var}(b) - |\mathrm{Cov}(a, b)|^2}.$$

Here $\mathrm{Var}(u) = P + \alpha^2 Q$, $\mathrm{Var}(y) = P + Q + N_0$, $\mathrm{Cov}(u, y) = P + \alpha Q$ and $I(u; s) = \log_2((P + \alpha^2 Q)/P)$. So

$$I(u; y) - I(u; s) = \log_2 \frac{P (P + Q + N_0)}{(P + \alpha^2 Q)(P + Q + N_0) - (P + \alpha Q)^2} = \log_2 \frac{P (P + Q + N_0)}{P Q (1 - \alpha)^2 + N_0 (P + \alpha^2 Q)}.$$

Take $\alpha = P/(P + N_0)$. Then $1 - \alpha = N_0/(P + N_0)$ and the denominator is

$$\frac{P Q N_0^2}{(P + N_0)^2} + N_0 P + \frac{N_0 Q P^2}{(P + N_0)^2} = N_0 P + \frac{N_0 P Q}{P + N_0} = \frac{N_0 P (P + N_0 + Q)}{P + N_0}.$$

The ratio is $(P + N_0)/N_0$, so the rate is $\log_2(1 + P/N_0)$. A Gaussian input of power $P - \delta$ meets the per-codeword constraint with probability tending to 1, and $\delta \to 0$ closes the gap. Together with the converse, $C = \log_2(1 + P/N_0)$. $\blacksquare$

## Consequences

**A worked example.** Take $P/N_0 = 10$ (10 dB) and an interference power $Q = 100$, which is 10 dB stronger than the signal. The table gives the rate $I(u; y) - I(u; s)$ of the proof for several values of $\alpha$, in bits per complex channel use.

| scheme | $\alpha$ | rate |
|---|---|---|
| treat $s$ as noise, $\log_2(1 + P/(N_0 + Q))$ | 0 | 0.1362 |
| half the interference in $u$ | 0.5 | 1.9615 |
| near the optimum | 0.9 | 3.4581 |
| all the interference in $u$ | 1 | 3.3350 |
| Costa's choice | $10/11$ | 3.4594 |

Costa's value equals $\log_2 11$, the capacity of the AWGN channel at 10 dB. The choice $\alpha = 1$ is right when there is no noise, and it loses 0.124 bits here. The choice $\alpha = 0$ ignores the interference at the encoder, and the receiver then treats it as noise.

**Coding schemes (techniques, not part of the theorem).**
- *Random binning.* The scheme of the proof. It shows existence only and has no efficient encoder.
- *Lattice strategies.* Erez, Shamai and Zamir (2005) replace the bins by the cosets of a fine [lattice](/lattice/) inside a coarse lattice. The encoder sends $x = [v - \alpha s - d] \bmod \Lambda$ with a dither $d$, and the receiver scales by $\alpha$ and reduces modulo the coarse lattice. With good lattices in high dimension and $\alpha = P/(P + N_0)$, this reaches $\log_2(1 + P/N_0)$, and they show that it does so for arbitrary interference, so the Gaussian law of $s$ is not needed for the scheme. The search for the nearest coarse lattice point is a [closest vector problem](/closest-vector-problem/).
- *Scalar version.* [Tomlinson-Harashima precoding](/tomlinson-harashima-precoding/) is the one-dimensional lattice strategy with $\alpha = 1$: it subtracts the interference and folds the result into an interval with a modulo operation. It needs only causal knowledge of $s$. It loses the shaping gain of a high-dimensional lattice, at most $10 \log_{10}(\pi e / 6) = 1.53$ dB at high SNR, and its uniform output costs the power factor $M^2/(M^2 - 1)$ for $M$-PAM, which is $10 \log_{10}(16/15) = 0.280$ dB for 4-PAM.
- *Vector perturbation.* [Vector perturbation precoding](/vector-perturbation-precoding/) uses a multidimensional modulo lattice at the transmitter of a multiuser downlink; it is related to lattice dirty paper coding but is not a capacity-achieving scheme.

**MIMO broadcast channel.** A base station with $M$ antennas serves $K$ single-antenna users, $y_k = h_k^H x + w_k$. Encode the users in order. The signal of user 1 is a Gaussian codeword. When the base station encodes user 2, it already knows the signal that user 1's beam puts at user 2, so it treats that signal as known interference and uses dirty paper coding against it. User $k$ then sees no interference from users $1, \ldots, k - 1$, and the beams handle the interference from later users. Caire and Shamai (2003) gave the zero-forcing version: with the LQ factorization $H = L Q$ (lower triangular $L$ and orthonormal rows of $Q$), the precoder $Q^H$ makes user $k$ see $l_{kk}$ times its own symbol plus known interference from earlier users. Take $M = K = 2$, $N_0 = 1$, $P = 10$ and the real channel $H = \begin{pmatrix} 2 & 1 \\ 1 & 1 \end{pmatrix}$ of the [zero-forcing precoding](/zero-forcing-precoding/) page. Then $|l_{11}|^2 = \|h_1\|^2 = 5$ and $|l_{22}|^2 = |\det H|^2 / \|h_1\|^2 = 0.2$.

| scheme | sum rate (bits per channel use) |
|---|---|
| zero-forcing precoding, water-filling | 2.853 |
| zero-forcing dirty paper coding, equal power | 5.700 |
| zero-forcing dirty paper coding, water-filling, powers (7.4, 2.6) | 5.852 |
| dirty paper coding sum capacity | 5.983 |
| both users at one receiver (cooperative bound) | 6.175 |

The sum capacity comes from the duality between the broadcast channel and the multiple access channel with the same total power (Vishwanath, Jindal and Goldsmith 2003; Viswanath and Tse 2003): it is $\max \log_2 \det(I + p_1 h_1 h_1^H + p_2 h_2 h_2^H)$ over $p_1 + p_2 = 10$. Here the determinant is $1 + 5 p_1 + 2 p_2 + p_1 p_2$, with the maximum $63.25$ at $p_1 = 6.5$, so the sum capacity is $\log_2 63.25 = 5.983$. The cooperative bound is the [MIMO capacity](/mimo-capacity/) with water-filling, which no broadcast scheme can beat because the users cannot share their outputs. See the [MAC capacity region](/mac-capacity-region/) page for the dual channel.

**Capacity region (theorem, Weingarten, Steinberg and Shamai 2006).** For the Gaussian MIMO broadcast channel with a fixed channel known to the transmitter and to every receiver, private messages and a power constraint, the capacity region equals the dirty paper coding region: the convex hull of the rate tuples that dirty paper coding reaches with Gaussian inputs, over all encoding orders and covariance matrices. The proof is not a direct corollary of Costa's theorem. Costa gives the inner bound, and the converse uses an enhanced channel that is degraded. Earlier work had proved the sum capacity (Caire and Shamai for two antennas; Vishwanath, Jindal and Goldsmith, Viswanath and Tse, and Yu and Cioffi in general).

## Tightness

- **Noncausal knowledge.** The theorem needs the whole sequence $s^n$ at the start. With only causal knowledge ($s_1, \ldots, s_i$ known when $x_i$ is sent), the capacity is given by Shannon strategies (El Gamal and Kim, Section 7.5), and the scalar schemes such as Tomlinson-Harashima precoding lose shaping gain at high SNR.
- **Exact knowledge.** The encoder must know $s$ exactly. If it knows only an estimate, the error acts as extra noise, and the rate falls below $\log_2(1 + P/N_0)$. In a broadcast channel this happens when the channel estimate at the base station is not exact.
- **Additive interference.** The interference must add to the signal. If it passes through a random gain that the encoder does not know, the rate is lower in general.
- **The receiver needs nothing.** The decoder does not need $s$, $Q$ or the coding order of the other users, only its own codebook.
- **Gaussian noise.** The proof uses Gaussian noise: in the converse through $h(w^n)$, and in the achievability through the Gaussian $u$. The Gaussian law of $s$ is not needed for the lattice scheme, as noted above.

## History

Gelfand and Pinsker (1980) found the capacity of a discrete memoryless channel with a state known noncausally at the encoder. Costa presented the Gaussian case at the 1981 International Symposium on Information Theory and published it in 1983 under the title "Writing on dirty paper", with the auxiliary $u = x + \alpha s$. The result stayed a curiosity until about 2000, when it was applied to information embedding and to the multiantenna broadcast channel. Caire and Shamai (2003) used dirty paper coding for the two-antenna broadcast channel. The sum capacity of the general case followed in 2003 and 2004 by duality with the multiple access channel, and Weingarten, Steinberg and Shamai (2006) proved that the dirty paper coding region is the whole capacity region. Erez, Shamai and Zamir (2005) gave lattice strategies that reach the capacity with structured codes.

## References
