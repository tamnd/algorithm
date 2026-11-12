---
tag: Q74BAQ
kind: theorem
slug: channel-polarization-theorem
name: Channel polarization theorem
aliases:
- Arikan polarization
- Arikan channel polarization theorem
area: compression-and-coding/error-correcting-codes
level: research
summary: "After n levels of the 2 by 2 polar transform, almost all N = 2^n synthetic channels are nearly perfect or nearly useless, and the fraction of good ones tends to the capacity."
history:
  year: 2009
  people: [Erdal Arıkan, Emre Telatar]
  note: Arıkan proved polarization and built polar codes on it in 2009. Arıkan and Telatar found the rate 2^(-N^β), β < 1/2, the same year.
prereqs: [binary-erasure-channel, channel-capacity]
see_also: [polar-code, successive-cancellation-decoding, binary-symmetric-channel, channel-coding-theorem, martingale, kronecker-product, bit-reversal-permutation, reed-muller-code]
sources:
  - paper: doi:10.1109/TIT.2009.2021379
    title: Erdal Arıkan, Channel polarization, a method for constructing capacity-achieving codes for symmetric binary-input memoryless channels, IEEE Transactions on Information Theory 55(7), 2009, pages 3051 to 3073
    locator: Section I (the kernel F, G_N = B_N F^(kron n) and the synthetic channels), the recursive channel transformation and its single-step properties, Theorem 1 (polarization), and the BEC recursion for the Bhattacharyya parameters
  - paper: doi:10.1109/ISIT.2009.5205856
    title: Erdal Arıkan and Emre Telatar, On the rate of channel polarization, Proceedings of the IEEE International Symposium on Information Theory (ISIT), 2009
    locator: The main theorem, the limits of P(Z_n <= 2^(-2^(n β))) for β < 1/2 and for β > 1/2
  - paper: doi:10.1561/0100000041
    title: Eren Şaşoğlu, Polarization and polar codes, Foundations and Trends in Communications and Information Theory 8(4), 2012
    locator: Chapter 2 (channel polarization, the martingale proof and the rate of polarization)
---

The channel polarization theorem says that a simple 2 by 2 transform, applied recursively to $N = 2^n$ copies of a [binary-input memoryless channel](/binary-symmetric-channel/) $W$, gives $N$ *synthetic channels* that are almost all either nearly noiseless or nearly pure noise. The fraction of nearly noiseless ones tends to the symmetric [capacity](/channel-capacity/) $I(W)$. Erdal Arıkan proved it in 2009 and built [polar codes](/polar-code/) on it: send data on the good channels, fix the bad ones to zero, and decode with [successive cancellation](/successive-cancellation-decoding/). On the [binary erasure channel](/binary-erasure-channel/) the synthetic channels are again erasure channels, and the whole theorem has a short exact proof, given below.

## Statement

**Notation.** Vectors are rows over $\mathrm{GF}(2)$. $N = 2^n$ is the block length. $W$ is a binary-input discrete memoryless channel with transition probabilities $W(y \mid x)$, $x \in \{0, 1\}$. $I(W)$ is its mutual information with a uniform input (the capacity $C$ when $W$ is symmetric, for example BSC($p$) or BEC($\varepsilon$)), and

$$Z(W) = \sum_y \sqrt{W(y \mid 0)\, W(y \mid 1)}$$

is its *Bhattacharyya parameter*, an upper bound on the error probability of a single bit under maximum likelihood decisions. On BEC($\varepsilon$), $Z = \varepsilon$ and $I = 1 - \varepsilon$.

**The transform.** Let $F = \begin{pmatrix} 1 & 0 \\ 1 & 1 \end{pmatrix}$ and $x = u F^{\otimes n}$, where $F^{\otimes n}$ is the $n$-th [Kronecker power](/kronecker-product/). Arıkan uses $G_N = B_N F^{\otimes n}$ with the [bit-reversal permutation](/bit-reversal-permutation/) $B_N$. Since $B_N F^{\otimes n} = F^{\otimes n} B_N$, the matrix $B_N$ only permutes the code bits, and the receiver sees all of them. So $B_N$ does not change any synthetic channel. This page uses $x = u F^{\otimes n}$, the order of 3GPP TS 38.212, and indices $0$ to $N - 1$.

**Synthetic channels.** Send $x = u F^{\otimes n}$ over $N$ independent uses of $W$, with $u$ uniform on $\mathrm{GF}(2)^N$. The $i$-th synthetic channel $W_N^{(i)}$ has input $u_i$ and output $(y_0^{N-1}, u_0^{i-1})$:

$$W_N^{(i)}\bigl(y_0^{N-1}, u_0^{i-1} \bigm| u_i\bigr) = \sum_{u_{i+1}^{N-1}} \frac{1}{2^{N-1}}\, \prod_{j=0}^{N-1} W\bigl(y_j \bigm| (u F^{\otimes n})_j\bigr).$$

It is the channel that bit $u_i$ sees when the decoder knows all earlier bits and not the later ones.

**One step.** For $N = 2$ the two synthetic channels are

$$W^-(y_1, y_2 \mid u_1) = \tfrac{1}{2} \sum_{u_2} W(y_1 \mid u_1 \oplus u_2)\, W(y_2 \mid u_2), \qquad W^+(y_1, y_2, u_1 \mid u_2) = \tfrac{1}{2}\, W(y_1 \mid u_1 \oplus u_2)\, W(y_2 \mid u_2).$$

They keep the total capacity, $I(W^-) + I(W^+) = 2 I(W)$, and $Z(W^+) = Z(W)^2$, $Z(W) \le Z(W^-) \le 2Z(W) - Z(W)^2$ (Arıkan 2009, single-step properties of the transform).

**Theorem (polarization, Arıkan 2009, Theorem 1).** For each binary-input discrete memoryless channel $W$ and each fixed $\delta \in (0, 1)$,

$$\lim_{n \to \infty} \frac{\bigl|\{ i : I(W_N^{(i)}) > 1 - \delta \}\bigr|}{N} = I(W), \qquad \lim_{n \to \infty} \frac{\bigl|\{ i : I(W_N^{(i)}) < \delta \}\bigr|}{N} = 1 - I(W).$$

**Theorem (the BEC case, exact).** Let $W = $ BEC($\varepsilon$) with $0 \le \varepsilon \le 1$. Then:

1. Each $W_N^{(i)}$ is a BEC with erasure probability $z_N^{(i)} = Z(W_N^{(i)})$. Write $i$ in binary with $n$ digits, $i = (b_1 b_2 \ldots b_n)_2$, $b_1$ the most significant. Start from $z = \varepsilon$ and for $t = 1, \ldots, n$ replace $z$ by $2z - z^2$ if $b_t = 0$ and by $z^2$ if $b_t = 1$. The result is $z_N^{(i)}$.
2. For each $\delta \in (0, 1/2]$, the fraction of indices with $\delta \le z_N^{(i)} \le 1 - \delta$ is at most $1 / (\delta (1 - \delta)(n + 4))$.
3. For each $\delta \in (0, 1/2]$, the fraction of indices with $z_N^{(i)} < \delta$ tends to $1 - \varepsilon = C$, and the fraction with $z_N^{(i)} > 1 - \delta$ tends to $\varepsilon$.

**Theorem (rate of polarization, Arıkan and Telatar 2009).** Let $Z_n = Z(W_N^{(i)})$ for an index $i$ chosen uniformly at random. For each $\beta < 1/2$,

$$\lim_{n \to \infty} \Pr\bigl[ Z_n \le 2^{-N^{\beta}} \bigr] = I(W),$$

and for each $\beta > 1/2$ the same probability tends to $0$ when $I(W) < 1$. So the good channels are not only good: their Bhattacharyya parameters are about $2^{-\sqrt{N}}$.

## In plain words

Take two copies of a noisy channel. Send the sum of two bits through the first copy and the second bit through the second copy. Now decode the first bit with no help: it is harder than before, because the second bit is unknown and hides it. Then decode the second bit with the first one known: it is easier, because the receiver now sees it twice. One channel got worse and one got better, and the total amount of information did not change.

Do the same thing again on the two new channels, and again, many times. The good channels get better and the bad channels get worse at each level. In the end almost every channel is either almost perfect or almost useless. The share of almost perfect channels equals the capacity of the first channel. A code sends data only on those.

## Proof

The general theorem needs a martingale argument (sketched at the end). The BEC case has a complete elementary proof.

**Lemma 1 (one step on the BEC).** Let $u_1, u_2$ be bits, send $u_1 \oplus u_2$ over BEC($a$) and $u_2$ over an independent BEC($b$), with $u_2$ uniform. Then the channel from $u_1$ to $(y_1, y_2)$ is BEC($1 - (1 - a)(1 - b)$), and the channel from $u_2$ to $(y_1, y_2, u_1)$ is BEC($ab$).

*Proof.* If neither output is erased, $u_1 = y_1 \oplus y_2$. If $y_2$ is erased, the output $(y_1, ?)$ has the same probability for $u_1 = 0$ and $u_1 = 1$, because $u_2$ is uniform and unseen, so $y_1$ is a uniform bit or $?$ for each $u_1$. If $y_1$ is erased, $y_2$ is independent of $u_1$. So $u_1$ is known exactly when both outputs arrive, with probability $(1 - a)(1 - b)$, and otherwise the output says nothing about it: this is a BEC with erasure probability $1 - (1 - a)(1 - b)$. For $u_2$: it is known if $y_2$ arrives ($u_2 = y_2$) or if $y_1$ arrives ($u_2 = y_1 \oplus u_1$, with $u_1$ given). If both are erased, the output $(?, ?, u_1)$ has the same probability for both values of $u_2$. So the erasure probability is $ab$. $\square$

With $a = b = z$ this gives $1 - (1 - z)^2 = 2z - z^2$ and $z^2$.

**Lemma 2 (recursion).** Let $n \ge 1$, $N = 2^n$ and $M = N/2$. For $0 \le i < M$, the channel $W_N^{(i)}$ is the $i$-th synthetic channel of the length-$M$ transform over $M$ independent copies of $W^-$, and $W_N^{(M + i)}$ is the $i$-th synthetic channel of the length-$M$ transform over $M$ independent copies of $W^+$, up to a one-to-one relabeling of the outputs.

*Proof.* Write $G' = F^{\otimes (n-1)}$. Since $F^{\otimes n} = F \otimes G' = \begin{pmatrix} G' & 0 \\ G' & G' \end{pmatrix}$, the split $u = (a, b)$ into halves gives $x = (s \oplus t, t)$ with $s = a G'$ and $t = b G'$. So for each $j < M$, the pair $(y_j, y_{j+M})$ is the output of the one-step transform with inputs $(s_j, t_j)$.

Take $i < M$. The bits $b$ are all later than $u_i$, so they are uniform and unknown, and $t = b G'$ is uniform on $\mathrm{GF}(2)^M$ because $G'$ is invertible. So the $t_j$ are independent uniform bits, and the pairs $(y_j, y_{j+M})$ are independent outputs of $W^-$ with inputs $s_j$. The output $(y, u_0^{i-1})$ of $W_N^{(i)}$ is therefore the output of the $i$-th synthetic channel of $s = a G'$ over copies of $W^-$, with $y$ regrouped into the pairs.

Take $M + i$. Now all of $a$ is known, so $s = a G'$ is known, and $b$ plays the part of $u$ in a code of length $M$. Each triple $(y_j, y_{j+M}, s_j)$ is the output of $W^+$ with input $t_j$, independently for each $j$, and $(y, a, b_0^{i-1})$ is in one-to-one correspondence with $\bigl((y_j, y_{j+M}, s_j)_{j < M}, b_0^{i-1}\bigr)$. This is the $i$-th synthetic channel of $t = b G'$ over copies of $W^+$. $\square$

**Part 1.** By induction on $n$. For $n = 0$, $W_1^{(0)} = W$ is BEC($\varepsilon$). For $n \ge 1$, Lemma 1 shows that $W^-$ is BEC($2\varepsilon - \varepsilon^2$) and $W^+$ is BEC($\varepsilon^2$). By Lemma 2, $W_N^{(i)}$ for $i < M$ (first digit $b_1 = 0$) is the channel with index $(b_2 \ldots b_n)_2$ of length $M$ over BEC($2\varepsilon - \varepsilon^2$), and for $i \ge M$ ($b_1 = 1$) over BEC($\varepsilon^2$). The induction hypothesis applied to the remaining $n - 1$ digits gives the rule. $\square$

**Part 2.** Let $z_0, \ldots, z_{N-1}$ be the values at level $n$, and define the means

$$m_n = \frac{1}{N} \sum_i z_i, \qquad a_n = \frac{1}{N} \sum_i q(z_i), \qquad q(z) = z(1 - z).$$

Each $z$ at level $n$ has the two children $2z - z^2$ and $z^2$ at level $n + 1$. Their mean is $z$, so $m_n = \varepsilon$ for all $n$. For $q$, with $1 - (2z - z^2) = (1 - z)^2$ and $1 - z^2 = (1 - z)(1 + z)$,

$$\tfrac{1}{2}\bigl[q(2z - z^2) + q(z^2)\bigr] = \tfrac{1}{2}\, z(1 - z)\bigl[(2 - z)(1 - z) + z(1 + z)\bigr] = z(1 - z)(1 - z + z^2) = q(z)\bigl(1 - q(z)\bigr).$$

So $a_{n+1} = a_n - \frac{1}{N} \sum_i q(z_i)^2 \le a_n - a_n^2$, because the mean of the squares is at least the square of the mean. Now $a_0 = q(\varepsilon) \le 1/4$. The map $\varphi(x) = x - x^2$ is increasing on $[0, 1/2]$, so if $a_n \le 1/(n + 4)$ then

$$a_{n+1} \le \varphi\Bigl(\frac{1}{n + 4}\Bigr) = \frac{n + 3}{(n + 4)^2} < \frac{1}{n + 5},$$

because $(n + 3)(n + 5) = (n + 4)^2 - 1$. By induction $a_n \le 1/(n + 4)$ for all $n$. On $[\delta, 1 - \delta]$ we have $q(z) \ge \delta(1 - \delta)$, so the fraction $M_n(\delta)$ of indices there satisfies $M_n(\delta)\, \delta (1 - \delta) \le a_n$. $\square$

**Part 3.** Let $G_n(\delta)$ and $B_n(\delta)$ be the fractions of indices with $z_i < \delta$ and $z_i > 1 - \delta$. For $\delta \le 1/2$ the three sets are disjoint, so $G_n + B_n + M_n = 1$. From $m_n = \varepsilon$:

$$\varepsilon \ge (1 - \delta)\, B_n(\delta), \qquad \varepsilon \le \delta\, G_n(\delta) + M_n(\delta) + B_n(\delta) \le \delta + M_n(\delta) + B_n(\delta).$$

Fix $0 < \delta' < \delta$. An index with $z_i > 1 - \delta$ has $z_i > 1 - \delta'$ or lies in $[\delta', 1 - \delta']$, so $B_n(\delta') \le B_n(\delta) \le B_n(\delta') + M_n(\delta')$. With the two bounds above for $\delta'$,

$$\varepsilon - \delta' - M_n(\delta') \le B_n(\delta) \le \frac{\varepsilon}{1 - \delta'} + M_n(\delta').$$

By Part 2, $M_n(\delta') \to 0$. So $\varepsilon - \delta' \le \liminf B_n(\delta) \le \limsup B_n(\delta) \le \varepsilon / (1 - \delta')$ for each $\delta' \in (0, \delta)$, and with $\delta' \to 0$, $B_n(\delta) \to \varepsilon$. Then $G_n(\delta) = 1 - B_n(\delta) - M_n(\delta) \to 1 - \varepsilon$. $\blacksquare$

**The general case (sketch).** Let $b_1, b_2, \ldots$ be independent fair bits, and let $I_n$ and $Z_n$ be $I$ and $Z$ of the channel reached from $W$ by the steps $b_1, \ldots, b_n$, with $-$ for $0$ and $+$ for $1$. By Lemma 2, $I_n$ has the distribution of $I(W_N^{(i)})$ for a uniform index $i$. The identity $I(W^-) + I(W^+) = 2I(W)$ makes $I_n$ a bounded martingale, so it converges almost surely. The relation $Z(W^+) = Z(W)^2$, which happens with probability $1/2$ at each step, together with $Z(W^-) \ge Z(W)$, forces the limit of $Z_n$ to be in $\{0, 1\}$, and channels with $Z$ near $0$ have $I$ near $1$ and the reverse. The mean $\mathbb{E}[I_n] = I(W)$ then gives the limit fractions. The full proof is the proof of Theorem 1 in Arıkan (2009). The rate result needs a finer analysis of the random process $Z_n$; see Arıkan and Telatar (2009) and Şaşoğlu (2012, Chapter 2).

**Numbers.** On BEC($0.3$) with $\delta = 0.01$, the fractions of indices with $z < \delta$ are $0.406$, $0.582$, $0.655$ and $0.683$ for $n = 5, 10, 15, 20$, and the fractions in the middle are $0.531$, $0.224$, $0.087$ and $0.033$. The limits are $0.7$ and $0$. The convergence is slow: on BEC($0.5$) at $n = 20$, the fraction with $z \le 2^{-N^{0.4}}$ is $0.326$, still far from $0.5$.

## Consequences

- **Polar codes.** Put data on the $K$ indices with the smallest $Z(W_N^{(i)})$ and fix the others. Under successive cancellation decoding the block error probability is at most $\sum_{i \in \mathcal{A}} Z(W_N^{(i)})$ (Arıkan 2009). With the rate theorem, for each $R < I(W)$ and $\beta < 1/2$ this is at most $2^{-N^{\beta}}$ for large $N$. So [polar codes](/polar-code/) reach the symmetric capacity with $O(N \log N)$ encoding and decoding. On the BEC, Part 1 gives the exact construction.
- **Decoding order.** The theorem is about the channels that [successive cancellation decoding](/successive-cancellation-decoding/) sees. A decoder that does not decode in this order (for example a parallel bit-by-bit decoder) does not get these channels.
- **Capacity is conserved.** The sum $\sum_i I(W_N^{(i)}) = N I(W)$ is exact at each $n$, because each step keeps the sum. Polarization moves capacity between indices; it does not create it.
- **Reed-Muller codes.** For $N = 8$ on BEC($1/2$), the four best indices are 3, 5, 6 and 7, the rows of $F^{\otimes 3}$ of weight at least 4: the polar code is the [Reed-Muller code](/reed-muller-code/) RM(1, 3) there. For larger $N$ the two choices differ.

## Tightness

- **The exponent 1/2.** By Arıkan and Telatar, the probability $\Pr[Z_n \le 2^{-N^\beta}]$ tends to $0$ for each $\beta > 1/2$ when $I(W) < 1$. So the kernel $F$ gives an error probability of about $2^{-\sqrt N}$ and no better. Larger kernels can have larger exponents.
- **The BEC is the extreme case.** $Z(W^-) \le 2Z(W) - Z(W)^2$ holds for each binary-input memoryless channel, with equality for the BEC. On BSC($0.11$), $Z = 0.626$, and $Z(W^-) = 0.794$ while $2Z - Z^2 = 0.860$. So the BEC recursion is exact only for the BEC; for other channels it gives an upper bound when started at $Z(W)$, not the true values.
- **Finite length.** The middle fraction does not vanish for any finite $n$ when $0 < \varepsilon < 1$: the indices $0$ and $N - 1$ always have $z = 1 - (1 - \varepsilon)^N$ and $z = \varepsilon^N$, and many indices in between are far from both ends.

## History

Arıkan published channel polarization and polar codes in the IEEE Transactions on Information Theory in July 2009. The paper proved polarization for each binary-input memoryless channel, gave the exact BEC recursion, and showed a block error probability of $O(N^{-1/4})$ under successive cancellation. The same year, Arıkan and Telatar showed at ISIT 2009 that the rate is $2^{-N^\beta}$ for each $\beta < 1/2$ and not for $\beta > 1/2$. The result gave codes with an explicit construction and an $O(N \log N)$ decoder that provably reach the capacity of each binary-input symmetric memoryless channel.

## References
