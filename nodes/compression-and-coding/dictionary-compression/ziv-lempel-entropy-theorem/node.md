---
tag: X1WQQT
kind: theorem
slug: ziv-lempel-entropy-theorem
name: Ziv-Lempel asymptotic optimality theorem
aliases:
- LZ asymptotic optimality
- Ziv-Lempel universality
area: compression-and-coding/dictionary-compression
level: advanced
summary: For a stationary ergodic source, the LZ78 code length per symbol tends to the entropy rate with probability 1, with no model of the source.
prereqs: [lz78-parsing, entropy-rate, ergodic-theorem, asymptotic-equipartition-property]
see_also: [lz78, lempel-ziv-complexity, universal-code, kraft-inequality, source-coding-theorem, lz77, kolmogorov-complexity, markov-chain]
sources:
  - paper: doi:10.1109/TIT.1978.1055934
    title: Jacob Ziv and Abraham Lempel, Compression of individual sequences via variable-rate coding, IEEE Transactions on Information Theory 24(5), 530-536, 1978
    locator: the incremental parsing and the theorem that the compression ratio of the code reaches the finite-state compressibility of every individual sequence, with the stationary ergodic case as a consequence
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: "Section 13.4 (the LZ78 algorithm) and Section 13.5, in particular Section 13.5.2 (the bound on the number of phrases of a distinct parsing, Ziv's inequality, and the proof that the LZ78 code length per symbol tends to the entropy rate)"
  - paper: "Aaron D. Wyner and Jacob Ziv, The sliding-window Lempel-Ziv algorithm is asymptotically optimal, Proceedings of the IEEE 82(6), 872-877, 1994"
    locator: the optimality of LZ77 with a sliding window for stationary ergodic sources
  - paper: "Guy Louchard and Wojciech Szpankowski, On the average redundancy rate of the Lempel-Ziv code, IEEE Transactions on Information Theory 43(1), 2-8, 1997"
    locator: the main theorem (for a memoryless source the average redundancy of LZ78 is of order 1/log n)
  - paper: "Serap A. Savari, Redundancy of the Lempel-Ziv incremental parsing rule, IEEE Transactions on Information Theory 43(1), 9-21, 1997"
    locator: the redundancy of LZ78 for memoryless and Markov sources
---

The Ziv-Lempel asymptotic optimality theorem says that the [LZ78](/lz78/) code compresses the output of any stationary ergodic source to its [entropy rate](/entropy-rate/), in the limit and with probability 1. The coder has no model of the source and no parameters; it learns the source from the text alone. So LZ78 is a [universal code](/universal-code/) for this whole class of sources. Ziv and Lempel proved it in 1978, in a stronger form for individual sequences. The convergence is real but slow: on a fair coin, the code still uses 12% more bits than the entropy after a million symbols.

## Statement

Let $X = (X_i)$ be a stationary ergodic process over a finite alphabet of $k$ symbols with entropy rate $H$ (in bits per symbol). Let $c(n)$ be the number of phrases of the [LZ78 parse](/lz78-parsing/) of $X_1^n$, and let $l_n(X_1^n)$ be the length in bits of the LZ78 code, which writes for phrase $j$ the index of its prefix phrase in $\lceil \log_2 j \rceil$ bits and the new symbol in $\lceil \log_2 k \rceil$ bits.

**Theorem.** With probability 1,
$$\lim_{n \to \infty} \frac{l_n(X_1^n)}{n} = H \qquad \text{and} \qquad \lim_{n \to \infty} \frac{c(n) \log_2 c(n)}{n} = H.$$

The proof in Cover and Thomas (Section 13.5) shows the upper half, $\limsup l_n / n \le H$ almost surely, for a binary alphabet; the lower half holds for every prefix-free code, and the proof below includes it. Two facts carry the proof:

- **Few phrases.** Every distinct parsing of a binary string of length $n \ge 4$ has $c \le n / ((1 - \varepsilon_n) \log_2 n)$, with $\varepsilon_n = \min\{1, (\log_2 \log_2 n + 4)/\log_2 n\} \to 0$. Cover and Thomas state it as a lemma in Section 13.5; the lemma number is not checked here.
- **Ziv's inequality.** For every $k$-th order Markov law $Q_k$ and every distinct parsing, $\log_2 Q_k(x_1^n \mid s_0) \le -\sum_{\ell, s} c_{\ell s} \log_2 c_{\ell s}$, where $c_{\ell s}$ counts the phrases of length $\ell$ that follow the state $s$.

## In plain words

LZ78 cuts the text into pieces. Each piece is an earlier piece plus one more letter, so all pieces are different. It writes each piece as "earlier piece number, plus a letter".

If the text is predictable, the pieces grow long fast, so there are few of them, and the cost per letter is small. The theorem says that the cost per letter goes down to the true unpredictability of the source, its entropy rate, for every source whose statistics do not change over time and do not split into separate behaviours. No compressor that knows the source can do better in the long run, and LZ78 gets there without knowing anything.

The catch is the speed. The extra cost goes down only like one over the number of digits of the text length, so it stays visible for very long texts.

## Proof

The full proof is in the proof file below. It has six steps, in the plan of Cover and Thomas.

1. **Few phrases.** A distinct parsing uses each string at most once. Its phrase count is largest when it uses all short strings, and counting them gives $c \le n / ((1 - \varepsilon_n) \log n)$. So $c/n = O(1/\log n)$ for every string.
2. **An entropy bound.** A random variable on the positive integers with mean $\mu$ has entropy at most $\log(\mu + 1) + \log e$ (the geometric law is the worst case).
3. **Ziv's inequality.** Write $Q_k(x_1^n)$ as the product of the probabilities of the phrases given their states. In a group of phrases with the same length and state, the phrases are distinct, so their probabilities sum to at most 1. Jensen's inequality for the logarithm gives the bound.
4. **The phrase count.** Write $\sum c_{\ell s} \log c_{\ell s} = c \log c - c H(U, V)$, where $(U, V)$ is the empirical law of (length, state). The mean phrase length is $n/c$, so step 2 and step 1 give $\frac{c}{n} H(U, V) \to 0$, and
$$\frac{c \log c}{n} \le -\frac{1}{n} \log Q_k(x_1^n \mid s_0) + \delta_k(n), \qquad \delta_k(n) \to 0.$$
5. **The ergodic theorem.** With the true $k$-th order conditional law as $Q_k$, the [ergodic theorem](/ergodic-theorem/) makes the right side tend to $H(X_0 \mid X_{-k}^{-1})$ almost surely, and this decreases to $H$ as $k \to \infty$. The code length is $c \log c + O(c)$ bits and $c = o(n)$, so $\limsup l_n / n \le H$.
6. **The lower bound.** The LZ78 codewords for a fixed $n$ are prefix-free. By the [Kraft inequality](/kraft-inequality/), the chance that a prefix-free code beats $-\log P(X_1^n)$ by $2 \log n$ bits is at most $n^{-2}$, so by the Borel-Cantelli lemma this happens only finitely often. The Shannon-McMillan-Breiman theorem ([asymptotic equipartition property](/asymptotic-equipartition-property/)) gives $-\frac{1}{n} \log P(X_1^n) \to H$, so $\liminf l_n / n \ge H$. $\square$

**A Monte Carlo check.** The implementation has a real LZ78 bit coder and decoder for binary input. With the seed $e$ for $n = 2^e$, it gives these code lengths per symbol:

| $n$ | fair coin, $H = 1$ | $P(1) = 0.1$, $H = 0.4690$ | Markov, $P(0 \to 1) = 0.05$, $P(1 \to 0) = 0.2$, $H = 0.3735$ |
|---|---|---|---|
| $2^{12}$ | 1.2324 | 0.6416 | 0.5659 |
| $2^{14}$ | 1.1904 | 0.6028 | 0.5243 |
| $2^{16}$ | 1.1661 | 0.5901 | 0.5001 |
| $2^{18}$ | 1.1421 | 0.5749 | 0.4873 |
| $2^{20}$ | 1.1223 | 0.5606 | 0.4688 |

Each column goes down toward $H$, slowly. The tests run the rows $2^{12}$, $2^{14}$ and $2^{16}$ with these seeds and check that the values decrease, stay above $H$, and are within 0.25 of $H$ at $2^{16}$. These are single samples, not averages, and the tolerance is loose on purpose. The tests also check the phrase bound of step 1 and Ziv's inequality on random Markov laws.

## Consequences

- **LZ78 is universal.** One fixed code reaches the entropy rate of every stationary ergodic source, with no parameter to tune. Practical variants such as [LZW](/lzw/) change the coding of the phrases, and need their own analysis.
- **The phrase count estimates the entropy.** $c(n) \log_2 c(n) / n \to H$ almost surely, so the LZ78 phrase count, like the [Lempel-Ziv complexity](/lempel-ziv-complexity/) of the 1976 parse, is a consistent estimator of the entropy rate.
- **LZ77.** Wyner and Ziv (1994) proved that [LZ77](/lz77/) with a sliding window is also asymptotically optimal for stationary ergodic sources, with a different proof that does not use Ziv's inequality.
- **A Markov bound for each sequence.** Inequality (1) of the proof holds for every individual sequence: $c \log c / n$ is at most the per-symbol code length of the best $k$-th order Markov model fitted to that sequence, plus a term that goes to 0. So LZ78 competes with every finite-memory model at once.

## Tightness

- **The speed.** For a memoryless source the average redundancy of LZ78, the excess of $\mathbb{E}[l_n]/n$ over $H$, is of order $1/\log n$ (Louchard and Szpankowski 1997; Savari 1997). Codes that know the class of memoryless sources reach a redundancy of order $(\log n)/n$. So the universality of LZ78 has a price, and the table above shows it.
- **The phrase bound is sharp up to a constant.** For the string made of all binary strings of length 1, 2, 3, and so on, in order, the LZ78 parse has at least $n / \log_2 n$ phrases; the tests check this for $n = 2^{10}$ to $2^{18}$. The implementation finds 6142 phrases for $n = 2^{16}$, where $n/\log_2 n = 4096$ and the bound of step 1 is 8192.
- **Ergodicity is needed.** Take a source that, with probability 1/2, emits all zeros forever and, with probability 1/2, emits fair coin flips. It is stationary but not ergodic, and its entropy rate is 1/2. LZ78 gives $l_n / n \to 0$ on the first branch and $\to 1$ on the second, so the limit is a random variable, not the constant $H$. The proof breaks at step 5, where the ergodic theorem gives a random limit.
- **Finite $n$.** The theorem says nothing about a fixed length. On a short input LZ78 can expand the data: the 13 bits `1011010100010` parse into 7 phrases and code into 21 bits.
- **Zero entropy.** On a constant sequence, the phrases have lengths $1, 2, 3, \ldots$, so $c(n) \approx \sqrt{2n}$ and $l_n/n \to 0 = H$, but only at the rate $(\log n)/\sqrt{n}$.

## History

Jacob Ziv and Abraham Lempel introduced the incremental parse in 1978 and proved that, for every individual sequence, the compression ratio of their code reaches the smallest ratio that any finite-state compressor can reach on it. For a stationary ergodic source, this ratio equals the entropy rate with probability 1, which is the theorem here. Their earlier papers defined the 1976 complexity measure and the 1977 sliding-window method. Cover and Thomas give the direct proof with Ziv's inequality in Section 13.5 of their textbook. Wyner and Ziv extended the optimality to LZ77 in 1994, and Louchard, Szpankowski and Savari found the exact order of the redundancy of LZ78 in 1997.

## References
