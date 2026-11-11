---
tag: 7JPQ0Z
kind: definition
slug: entropy-rate
name: Entropy rate
aliases:
- entropy rate of a stochastic process
area: compression-and-coding/entropy-coding
level: advanced
summary: The entropy per symbol of a source with memory, lim H(X_1..X_n)/n. For a stationary Markov chain it is sum_i mu_i H(row i); it is the limit of lossless compression.
prereqs: [shannon-entropy, conditional-entropy, markov-chain, stationary-distribution]
see_also: [asymptotic-equipartition-property, source-coding-theorem, ziv-lempel-entropy-theorem, lempel-ziv-complexity, transition-matrix, ergodic-theorem, power-iteration]
sources:
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Chapter 4, Section 4.1 (stationary processes and Markov chains) and Section 4.2 (entropy rate, the two definitions, and the formula for a stationary Markov chain)
  - paper: doi:10.1002/j.1538-7305.1948.tb01338.x
    title: C. E. Shannon, A mathematical theory of communication, Bell System Technical Journal 27(3), 1948
    locator: Section 7 (The entropy of an information source), the entropy per symbol of a Markoff source
  - paper: doi:10.1002/j.1538-7305.1951.tb01366.x
    title: C. E. Shannon, Prediction and entropy of printed English, Bell System Technical Journal 30(1), 1951
    locator: Section 2 (the N-gram entropies F_N of English) and Section 6 (bounds from the prediction experiment)
---

The entropy rate of a random process $X_1, X_2, \ldots$ is the entropy per symbol in the long run, $\lim_{n \to \infty} \frac{1}{n} H(X_1, \ldots, X_n)$. For independent symbols it is the [entropy](/shannon-entropy/) of one symbol. For a source with memory it is smaller, because each symbol is partly predictable from the ones before it. For a stationary process it equals the limit of the [conditional entropy](/conditional-entropy/) of the next symbol given the past, and for a stationary [Markov chain](/markov-chain/) it has a closed form. It is the best rate of lossless compression for such a source.

## Definition

Notation. $\Sigma$ is a finite alphabet of size $\sigma$, and $X_1, X_2, \ldots$ is a random process with values in $\Sigma$. $X_i^j$ means $X_i, \ldots, X_j$. Logarithms are base 2. The model is a stationary process: the law of $(X_{1+t}, \ldots, X_{n+t})$ does not depend on the shift $t$, for every $n$. For the formula, the model is a stationary Markov chain of order 1 with transition matrix $P$ and stationary law $\mu$. A Markov source of order $k$ becomes one of order 1 on the alphabet $\Sigma^k$.

**Definition.** The entropy rate is

$$H(\mathcal{X}) = \lim_{n \to \infty} \frac{1}{n} H(X_1, \ldots, X_n)$$

when the limit exists. A second quantity is

$$H'(\mathcal{X}) = \lim_{n \to \infty} H(X_n \mid X_1, \ldots, X_{n-1}),$$

the uncertainty of the next symbol given the whole past.

**For a stationary process, both limits exist and are equal.**

*Proof.* Let $a_n = H(X_n \mid X_1^{n-1})$. Conditioning on less cannot lower the entropy, so $a_{n+1} = H(X_{n+1} \mid X_1^n) \le H(X_{n+1} \mid X_2^n)$, and by stationarity $H(X_{n+1} \mid X_2^n) = H(X_n \mid X_1^{n-1}) = a_n$. So $(a_n)$ is non-increasing and at least 0, and it has a limit $H'$. By the chain rule, $\frac{1}{n} H(X_1^n) = \frac{1}{n} \sum_{i=1}^{n} a_i$, and the averages of a convergent sequence converge to the same limit (Cesaro). So $H = H'$. $\square$

The proof also gives $\frac{1}{n} H(X_1^n) \ge H(\mathcal{X})$ for every $n$, since the $a_i$ decrease to $H'$. So the block entropy per symbol approaches the rate from above.

**Markov chains.** Let $X_1, X_2, \ldots$ be a Markov chain with transition matrix $P = (P_{ij})$ and with $X_1$ drawn from a [stationary distribution](/stationary-distribution/) $\mu$, so that $\mu P = \mu$ and the chain is stationary. Then

$$H(\mathcal{X}) = H(X_2 \mid X_1) = -\sum_{i} \mu_i \sum_{j} P_{ij} \log_2 P_{ij}.$$

*Proof.* By the Markov property, $H(X_n \mid X_1^{n-1}) = H(X_n \mid X_{n-1})$, and by stationarity this is $H(X_2 \mid X_1)$ for every $n \ge 2$. Given $X_1 = i$, $X_2$ has the law of row $i$ of $P$, and $X_1 = i$ has probability $\mu_i$. $\square$

The formula is the entropy of each row of $P$, weighted by how often the chain is in that state. Also $H(X_1^k) = H(\mu) + (k - 1) H(\mathcal{X})$ exactly, so $\frac{1}{k} H(X_1^k) - H(\mathcal{X}) = (H(\mu) - H(\mathcal{X})) / k$. If the chain is irreducible and aperiodic, it converges to $\mu$ from any start, and the rate is the same for any initial law.

**Meaning.** For a stationary ergodic process, $-\frac{1}{n} \log_2 p(X_1^n) \to H(\mathcal{X})$ with probability 1 (the Shannon-McMillan-Breiman theorem, the general form of the [asymptotic equipartition property](/asymptotic-equipartition-property/)). So about $2^{n H(\mathcal{X})}$ strings of length $n$ carry most of the probability, and $n H(\mathcal{X})$ bits are needed and enough for lossless coding of $X_1^n$ as $n$ grows, as in the [source coding theorem](/source-coding-theorem/). The Lempel-Ziv codes reach $H(\mathcal{X})$ without knowing the law ([Ziv-Lempel entropy theorem](/ziv-lempel-entropy-theorem/)).

## Examples and non-examples

**A two-state chain.** Let $P = \begin{pmatrix} 0.9 & 0.1 \\ 0.3 & 0.7 \end{pmatrix}$. Solve $\mu P = \mu$: $\mu = (0.75, 0.25)$. With the [binary entropy function](/binary-entropy-function/) $h$, the rate is $0.75 \, h(0.1) + 0.25 \, h(0.3) = 0.75 \cdot 0.4690 + 0.25 \cdot 0.8813 = 0.5721$ bits per symbol. A memoryless source with the same symbol frequencies would have $h(0.25) = 0.8113$ bits per symbol, so the memory saves about 30%.

| $k$ | exact $\frac{1}{k} H(X_1^k)$ | measured on 100000 symbols |
|---|---|---|
| 1 | 0.8113 | 0.8176 |
| 2 | 0.6917 | 0.6984 |
| 4 | 0.6319 | 0.6387 |
| 8 | 0.6020 | 0.6087 |
| 16 | 0.5870 | |
| $\infty$ | 0.5721 | |

The exact column comes from $H(X_1^k) = H(\mu) + (k-1) H$. The measured column is the empirical entropy of the $k$-blocks of one sample path (seed 1 in the code on this page). The measured differences $\hat H(X_1^{k+1}) - \hat H(X_1^k)$ estimate $H(X_{k+1} \mid X_1^k)$, and they are already about 0.579 at $k = 1$, because the chain has order 1. The code finds $\mu$ by power iteration on the lazy chain $(I + P)/2$, which has the same stationary law and always converges for an irreducible chain.

**A three-state chain.** For $P = \begin{pmatrix} 0.5 & 0.5 & 0 \\ 0.2 & 0.3 & 0.5 \\ 0.1 & 0 & 0.9 \end{pmatrix}$, $\mu = (0.1892, 0.1351, 0.6757)$ and $H(\mathcal{X}) = 0.7068$ bits per symbol.

**English text (Shannon 1951).** Shannon measured the $N$-gram entropy $F_N$, the entropy of a letter given the $N - 1$ letters before it, from tables of English letter frequencies (Section 2 of the 1951 paper):

| alphabet | $F_0$ | $F_1$ | $F_2$ | $F_3$ | $F_{\text{word}}$ |
|---|---|---|---|---|---|
| 26 letters | 4.70 | 4.14 | 3.56 | 3.3 | 2.62 |
| 27 letters (with space) | 4.76 | 4.03 | 3.32 | 3.1 | 2.14 |

$F_0 = \log_2 26$ is the rate with no statistics at all. $F_{\text{word}}$ comes from word frequencies, divided by the mean word length. In Section 6, people guessed the next letter of a text after seeing the letters before it, and from these guesses Shannon got bounds of about 0.6 and 1.3 bits per letter for $N = 100$. These numbers are estimates for one corpus and one experiment, not exact values, but they show the falling sequence $F_N$ that the proof above predicts.

**Non-examples.**

- The entropy rate is not $H(X_1)$. They are equal only for an independent and identically distributed process; for the two-state chain they are 0.5721 and 0.8113.
- A process that is not stationary may have no entropy rate. Cut the indices into consecutive blocks of lengths $2, 4, 8, 16, \ldots$. Let the $X_i$ be independent, fair bits in the 1st, 3rd, 5th, ... block and constant 0 in the other blocks. Then $\frac{1}{n} H(X_1^n)$ swings between about $1/3$ and $2/3$ and does not converge.
- A periodic sequence such as $0101\ldots$ with a random phase has entropy rate 0, though $H(X_1) = 1$. A fixed rate of 0 does not mean the symbols are constant.
- The empirical $H_k$ of one string is not the entropy rate. For a long sample of a stationary ergodic source of order $k$ it converges to the rate, but it is a property of the string, defined with no source.

## Related definitions

- [Conditional entropy](/conditional-entropy/) gives the second definition $H'$.
- The [asymptotic equipartition property](/asymptotic-equipartition-property/), in the Shannon-McMillan-Breiman form, is the sample-path version: $-\frac{1}{n} \log_2 p(X_1^n)$ converges to the rate.
- [Lempel-Ziv complexity](/lempel-ziv-complexity/) of a sample path, suitably normalized, converges to the entropy rate for stationary ergodic sources.
- The [transition matrix](/transition-matrix/) and the [ergodic theorem](/ergodic-theorem/) give $\mu$ and the meaning of time averages.
- For a hidden Markov process, the rate has no closed form; Cover and Thomas, Section 4.5, give upper and lower bounds that meet in the limit.

## References
