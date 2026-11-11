---
tag: VX919M
kind: theorem
slug: slepian-wolf-theorem
name: Slepian-Wolf theorem
aliases:
- distributed source coding theorem
- Slepian-Wolf coding
area: compression-and-coding/entropy-coding
level: research
summary: Two correlated sources coded by separate encoders and one joint decoder need only R_X >= H(X|Y), R_Y >= H(Y|X) and R_X + R_Y >= H(X,Y), as if the encoders could talk.
prereqs: [conditional-entropy, source-coding-theorem]
see_also: [asymptotic-equipartition-property, hamming-code, syndrome, syndrome-decoding, linear-code, binary-symmetric-channel, channel-coding-theorem, lossy-compression]
sources:
  - paper: doi:10.1109/TIT.1973.1055037
    title: David Slepian and Jack K. Wolf, Noiseless coding of correlated information sources, IEEE Transactions on Information Theory 19(4), 1973
    locator: The main theorem (the admissible rate region for two correlated memoryless sources)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Section 15.4 (Encoding of correlated sources, Theorem 15.4.1, the proof by random binning, and the converse)
  - paper: doi:10.1109/TIT.2002.808103
    title: S. Sandeep Pradhan and Kannan Ramchandran, Distributed source coding using syndromes (DISCUS), design and construction, IEEE Transactions on Information Theory 49(3), 2003
    locator: The syndrome construction (cosets of a linear code as bins) and its example with a Hamming code
---

The Slepian-Wolf theorem is about two sources that are correlated, such as two sensors that watch the same scene. Each one is compressed by its own encoder, which does not see the other source, and one decoder gets both outputs and must recover both sources. The theorem says that the encoders lose nothing in total by working apart: the sum of the rates can be as small as the joint [entropy](/shannon-entropy/) $H(X, Y)$, the same as for one encoder that sees both. The proof assigns sequences to random bins. In practice the bins are the cosets of a linear error-correcting code, and the encoder sends a syndrome.

## Statement

Notation. $X$ takes values in a finite alphabet $\Sigma_X$ and $Y$ in $\Sigma_Y$. The model is a pair of memoryless sources: the pairs $(X_i, Y_i)$, $i = 1, 2, \ldots$, are independent, each with the joint law $p(x, y)$. $X^n = (X_1, \ldots, X_n)$ and $Y^n$ in the same way. Logarithms are base 2, and $H(X \mid Y)$ is the [conditional entropy](/conditional-entropy/).

A *distributed code* of rates $(R_X, R_Y)$ for blocks of length $n$ is an encoder $f_n : \Sigma_X^n \to \{1, \ldots, 2^{n R_X}\}$, an encoder $g_n : \Sigma_Y^n \to \{1, \ldots, 2^{n R_Y}\}$, and a decoder $\phi_n$ that maps the pair of indices $(f_n(X^n), g_n(Y^n))$ to an estimate of $(X^n, Y^n)$. Its error probability is $P_e^{(n)} = \Pr[\phi_n(f_n(X^n), g_n(Y^n)) \ne (X^n, Y^n)]$. A rate pair is *achievable* if there are codes with $P_e^{(n)} \to 0$.

**Theorem (Slepian and Wolf 1973).** A rate pair $(R_X, R_Y)$ is achievable if

$$R_X > H(X \mid Y), \qquad R_Y > H(Y \mid X), \qquad R_X + R_Y > H(X, Y),$$

and it is not achievable if $R_X < H(X \mid Y)$, or $R_Y < H(Y \mid X)$, or $R_X + R_Y < H(X, Y)$.

The region is a quadrant with one corner cut off. Its two corner points are $(H(X), H(Y \mid X))$ and $(H(X \mid Y), H(Y))$. At the second corner, $Y$ is compressed alone at rate $H(Y)$ by the [source coding theorem](/source-coding-theorem/), and $X$ is sent at rate $H(X \mid Y)$ with $Y^n$ as side information at the decoder only.

## In plain words

Two people each hold a long record, and the records are similar. Each must send a short summary to a third person, who must rebuild both records. They cannot talk to each other. It seems that each must send the full content of its own record. The theorem says that this is not so. The second sender can send much less, only the amount that the receiver still lacks after it has the first record, even though the second sender never sees the first record. The trick is to sort all possible records into many groups, called bins, and to send only the name of the group. The receiver then picks the one record in that group that fits the other record. Good groups come from codes that correct errors.

## Proof

**Achievability by random binning.** Fix $\varepsilon > 0$ and rates with $R_X > H(X \mid Y) + 2\varepsilon$, $R_Y > H(Y \mid X) + 2\varepsilon$ and $R_X + R_Y > H(X, Y) + 2\varepsilon$. Choose $f_n$ by giving each $x^n$ an index drawn uniformly from $\{1, \ldots, 2^{n R_X}\}$, independently, and choose $g_n$ in the same way; the sets of strings with the same index are the *bins*. The decoder gets the indices $(i, j)$ and outputs the unique pair $(x^n, y^n)$ with $f_n(x^n) = i$, $g_n(y^n) = j$ that is *jointly typical*, that is, whose empirical $-\frac{1}{n} \log_2$ of $p(x^n)$, $p(y^n)$ and $p(x^n, y^n)$ are within $\varepsilon$ of $H(X)$, $H(Y)$ and $H(X, Y)$. If there is no such pair or more than one, it declares an error.

The decoder fails only if one of these events happens:

- $E_0$: the true pair $(X^n, Y^n)$ is not jointly typical. By the [AEP](/asymptotic-equipartition-property/) applied to $X$, to $Y$ and to the pairs, $\Pr[E_0] \to 0$.
- $E_1$: some $x'^n \ne X^n$ in the bin of $X^n$ is jointly typical with $Y^n$. For a fixed $y^n$, at most $2^{n(H(X \mid Y) + 2\varepsilon)}$ strings $x'^n$ are jointly typical with it (each such pair has probability at least $2^{-n(H(X, Y) + \varepsilon)}$, while $p(y^n) \le 2^{-n(H(Y) - \varepsilon)}$). Each falls in the bin of $X^n$ with probability $2^{-n R_X}$, so the expected number is at most $2^{-n(R_X - H(X \mid Y) - 2\varepsilon)} \to 0$.
- $E_2$: the same with the roles of $X$ and $Y$ exchanged; it needs $R_Y > H(Y \mid X) + 2\varepsilon$.
- $E_{12}$: some pair $(x'^n, y'^n)$ with $x'^n \ne X^n$ and $y'^n \ne Y^n$ in both bins is jointly typical. There are at most $2^{n(H(X, Y) + \varepsilon)}$ jointly typical pairs, each in both bins with probability $2^{-n(R_X + R_Y)}$, so this needs $R_X + R_Y > H(X, Y) + \varepsilon$.

By the union bound and Markov's inequality, the error probability averaged over the random choice of bins goes to 0. So for each $n$ some fixed choice of bins does at least as well as the average, and those codes have $P_e^{(n)} \to 0$.

**Converse.** Let $I = f_n(X^n)$ and $J = g_n(Y^n)$, and let $P_e^{(n)} \to 0$. By Fano's inequality, $H(X^n, Y^n \mid I, J) \le n \varepsilon_n$ with $\varepsilon_n \to 0$. Then

$$n(R_X + R_Y) \ge H(I, J) \ge H(I, J) - H(I, J \mid X^n, Y^n) = H(X^n, Y^n) - H(X^n, Y^n \mid I, J) \ge n H(X, Y) - n \varepsilon_n,$$

because $(I, J)$ is a function of $(X^n, Y^n)$ and the source is memoryless. For one rate, $J$ is a function of $Y^n$, so

$$n R_X \ge H(I) \ge H(I \mid Y^n) = H(X^n \mid Y^n) - H(X^n \mid I, Y^n) \ge n H(X \mid Y) - n \varepsilon_n,$$

where $H(I \mid Y^n) = H(X^n \mid Y^n) - H(X^n \mid I, Y^n)$ because $I$ is a function of $X^n$, and $H(X^n \mid I, Y^n) \le H(X^n \mid I, J) \le n \varepsilon_n$. The bound on $R_Y$ is the same. Let $n \to \infty$. $\square$

## Consequences

**Binning with a linear code: the syndrome method.** Random bins have no structure, so they cannot be decoded fast. Take instead a linear code $\mathcal{C} \subseteq \{0, 1\}^n$ with parity-check matrix $H_{\mathcal{C}}$ of size $(n - k) \times n$. Its cosets $\{x : H_{\mathcal{C}} x = s\}$ are $2^{n-k}$ bins of $2^k$ strings each. The encoder of $X$ sends the [syndrome](/syndrome/) $s = H_{\mathcal{C}} X^n$, which is $n - k$ bits. If $Y^n = X^n \oplus e$ for a likely error pattern $e$, the decoder computes $H_{\mathcal{C}} Y^n \oplus s = H_{\mathcal{C}} e$, finds $e$ by [syndrome decoding](/syndrome-decoding/), and outputs $Y^n \oplus e$. So distributed compression of $X$ is the same problem as channel decoding over the channel from $X$ to $Y$. This is the idea of DISCUS (Pradhan and Ramchandran 2003). For $Y$ the output of a [binary symmetric channel](/binary-symmetric-channel/) with crossover $p$ from a uniform $X$, a good code of rate $k/n$ near $1 - h(p)$ gives the corner rate $H(X \mid Y) = h(p)$.

**A 7-bit example with the Hamming code.** Let $X$ be uniform on $\{0, 1\}^7$ and let $Y$ differ from $X$ in at most one of the 7 positions, each of the 8 cases with probability $1/8$. Then $H(X) = H(Y) = 7$, $H(X \mid Y) = H(Y \mid X) = 3$ and $H(X, Y) = 10$ bits. Use the [Hamming code](/hamming-code/) of length 7: the syndrome of a string is the XOR of the positions (1 to 7, written in 3 bits) of its 1 bits. The 8 syndromes cut the 128 strings into 8 bins of 16, and two strings in one bin differ in at least 3 positions. $Y$ is sent in full (7 bits), and $X$ is sent as its syndrome (3 bits), so the total is $10 = H(X, Y)$, with no error at all.

For example, let $X = 1001101$ (1 bits at positions 1, 4, 5 and 7). Its syndrome is $1 \oplus 4 \oplus 5 \oplus 7 = 7$. Let $Y = 1001001$, which differs from $X$ in position 5. The decoder computes the syndrome of $Y$, $1 \oplus 4 \oplus 7 = 2$, and $2 \oplus 7 = 5$ gives the position where $X$ and $Y$ differ. Flipping bit 5 of $Y$ gives $X$. The code on this page checks this for all $128 \times 8$ pairs, and checks that every pair at distance 2 is decoded wrongly: the scheme relies on the model.

**Other consequences.** Sensor networks, distributed video coding (where the decoder, not the encoder, uses the correlation between frames) and compression of a file when the receiver has an old version all fit this setting. With a fidelity criterion instead of lossless recovery, the Wyner-Ziv theorem is the analogue for [lossy compression](/lossy-compression/); there, unlike here, side information at the decoder only is in general worse than at both ends.

## Tightness

The converse shows that the region is exact: no point outside it is achievable. Each of the three bounds matters. Without the encoders' cooperation one might expect the rate $H(X) + H(Y)$; the saving is $H(X) + H(Y) - H(X, Y) = I(X; Y)$, the mutual information. If $X$ and $Y$ are independent, the region is $R_X \ge H(X)$, $R_Y \ge H(Y)$ and there is no saving. If $X = Y$, $H(X \mid Y) = 0$ and the region is $R_X + R_Y \ge H(X)$: either encoder may send almost everything.

The theorem is asymptotic, with vanishing error for long blocks. For a finite block and zero error, the region can be much smaller. The Hamming example reaches a corner point exactly only because the model allows at most one difference in 7 bits; under a binary symmetric channel model, two or more differences in a block happen with positive probability, and then the syndrome decoder fails.

## History

Slepian and Wolf proved the theorem in 1973 for two memoryless sources. Wyner (1974) observed that the cosets of a linear code can serve as the bins, which is the syndrome method. Cover (1975) gave the proof by random binning and extended the theorem to stationary ergodic sources and to any number of sources. Practical codes came much later: DISCUS (Pradhan and Ramchandran, 2003) built distributed codes from syndromes of trellis and block codes, and later work used turbo and LDPC codes to come close to the Slepian-Wolf bound.

## References
