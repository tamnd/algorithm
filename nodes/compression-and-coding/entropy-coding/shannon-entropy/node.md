---
tag: A13CS0
kind: definition
slug: shannon-entropy
name: Shannon entropy
aliases:
- information entropy
- empirical entropy
area: compression-and-coding/entropy-coding
level: intro
summary: H(X) = -sum p(x) log p(x), the average information of one outcome of a source; its empirical form H_k measures a single string.
prereqs: [discrete-probability-distribution, expected-value]
see_also: [self-information, binary-entropy-function, conditional-entropy, entropy-rate, source-coding-theorem, huffman-coding, arithmetic-coding, min-entropy]
sources:
  - paper: doi:10.1002/j.1538-7305.1948.tb01338.x
    title: C. E. Shannon, A mathematical theory of communication, Bell System Technical Journal 27(3), 1948
    locator: Section 6 (Choice, uncertainty and entropy), with Theorem 2 (the three properties that fix H) and its proof in Appendix 2
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Sections 2.1 (entropy) and 2.6 (the bound log of the alphabet size and the concavity of H)
  - paper: doi:10.1145/382780.382782
    title: Giovanni Manzini, An analysis of the Burrows-Wheeler transform, Journal of the ACM 48(3), 2001
    locator: The definitions of the empirical entropies H_0 and H_k of a string
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, Cambridge University Press, 2016
    locator: Chapter 2 (worst-case, Shannon, empirical and high-order entropy)
---

The Shannon entropy of a [discrete random variable](/discrete-probability-distribution/) $X$ is $H(X) = -\sum_x p(x) \log_2 p(x)$, the [expected value](/expected-value/) of the [self-information](/self-information/) $-\log_2 p(X)$. It is the average number of bits that an ideal lossless code needs for one outcome, and the [source coding theorem](/source-coding-theorem/) makes this exact. For a single string with no probability model, the empirical entropies $H_0$ and $H_k$ play the same role in the worst case.

## Definition

Notation. $\Sigma$ is a finite alphabet of size $\sigma$. $X$ takes values in $\Sigma$ with probabilities $p(x) = \Pr[X = x]$. Logarithms are base 2 unless stated. The model is a memoryless source: one draw of $X$, or a sequence of independent draws with the same law. Strings are the subject of the empirical part below, and there no probability model is assumed.

**Definition (Shannon 1948).** The entropy of $X$ is

$$H(X) = -\sum_{x \in \Sigma} p(x) \log_2 p(x) = \mathbb{E}\left[\log_2 \frac{1}{p(X)}\right],$$

with the convention $0 \log 0 = 0$, which is the limit of $p \log p$ as $p \to 0$. $H$ depends only on the list of probabilities, not on the values of $X$. So we also write $H(p_1, \ldots, p_\sigma)$.

**Units.** With $\log_2$ the unit is the *bit* (Shannon also wrote "binary digit"). With the natural logarithm the unit is the *nat*, and $H_{\text{nats}} = H_{\text{bits}} \cdot \ln 2$. A change of base multiplies $H$ by a constant: $H_b = H_2 / \log_2 b$.

### Properties

1. **Range.** $0 \le H(X) \le \log_2 \sigma$. $H(X) = 0$ exactly when one outcome has probability 1. $H(X) = \log_2 \sigma$ exactly when $X$ is uniform on $\Sigma$.
2. **Concavity.** $H$ is a concave function of the vector $(p_1, \ldots, p_\sigma)$: $H(t p + (1-t) q) \ge t H(p) + (1-t) H(q)$ for $0 \le t \le 1$.
3. **Additivity.** If $X$ and $Y$ are independent, $H(X, Y) = H(X) + H(Y)$. Without independence, the chain rule $H(X, Y) = H(Y) + H(X \mid Y)$ holds; see [conditional entropy](/conditional-entropy/).
4. **Grouping.** $H(p_1, p_2, p_3, \ldots) = H(p_1 + p_2, p_3, \ldots) + (p_1 + p_2) H\!\left(\frac{p_1}{p_1 + p_2}, \frac{p_2}{p_1 + p_2}\right)$.

*Proof.* (1) For $0 \le p \le 1$, $-p \log p \ge 0$, with equality only at $p \in \{0, 1\}$. So $H \ge 0$, with equality only when every $p(x)$ is 0 or 1. For the upper bound, let $S$ be the set of $x$ with $p(x) > 0$. The function $\log$ is concave, so by [Jensen's inequality](/jensens-inequality/), $H = \sum_{x \in S} p(x) \log \frac{1}{p(x)} \le \log \sum_{x \in S} p(x) \frac{1}{p(x)} = \log |S| \le \log \sigma$. Jensen's inequality for the strictly concave $\log$ is an equality only when $1/p(x)$ is the same for all $x \in S$, and the last step is an equality only when $S = \Sigma$. So equality needs the uniform law. (2) The function $f(p) = -p \log_2 p$ has $f''(p) = -1/(p \ln 2) < 0$ on $(0, 1]$, so it is concave on $[0, 1]$, and $H$ is a sum of concave functions of the coordinates. (3) With $p(x, y) = p(x) q(y)$, $\log \frac{1}{p(x) q(y)} = \log \frac{1}{p(x)} + \log \frac{1}{q(y)}$; take expectations. (4) Write $s = p_1 + p_2$. The terms for $p_3, \ldots$ are the same on both sides, and $-p_1 \log p_1 - p_2 \log p_2 = -s \log s + s\left(-\frac{p_1}{s} \log \frac{p_1}{s} - \frac{p_2}{s} \log \frac{p_2}{s}\right)$ by $\log p_i = \log s + \log (p_i / s)$. $\square$

**The H theorem.** Shannon asked for a measure $H(p_1, \ldots, p_\sigma)$ that is continuous in the $p_i$, that grows with $\sigma$ on uniform laws, and that obeys the grouping rule 4 for any split of a choice into two successive choices. Theorem 2 of his paper says that the only such measure is $H = -K \sum p_i \log p_i$ for a constant $K > 0$; the constant only fixes the unit. The proof is in Appendix 2 of the paper.

### Empirical entropy of a string

Let $s$ be a string of length $n$ over $\Sigma$, and let $n_c$ be the number of times the symbol $c$ occurs in $s$.

- The *zero-order empirical entropy* is $H_0(s) = \sum_{c} \frac{n_c}{n} \log_2 \frac{n}{n_c}$, the entropy of the symbol frequencies of $s$.
- For $k \ge 1$ and each string $w$ of length $k$, let $w_s$ be the string of the symbols that follow the occurrences of $w$ in $s$. The *$k$-th order empirical entropy* (Manzini 2001) is $H_k(s) = \frac{1}{n} \sum_{w \in \Sigma^k} |w_s| \, H_0(w_s)$.

These are worst-case measures: they are defined for every string, with no source. $n H_0(s)$ is a lower bound on the length of $s$ under any code that gives each symbol one fixed codeword: by the Gibbs inequality, $\sum_c n_c \ell_c \ge \sum_c n_c \log_2 (n / n_c)$ whenever $\sum_c 2^{-\ell_c} \le 1$, which every [prefix code](/prefix-code/) meets by the [Kraft inequality](/kraft-inequality/). In the same way, $n H_k(s)$ bounds any code that picks the codeword of a symbol from the $k$ symbols before it, except the first $k$ symbols. $H_k$ is non-increasing in $k$: splitting the context $w$ into the contexts $aw$ splits $w_s$ into parts (with at most one symbol left over, at the start of $s$), and the sum of $|x| H_0(x)$ over the parts of a string is at most $|x| H_0(x)$ of the whole, by the concavity of property 2. For large $k$, $H_k(s)$ reaches 0, so a bound in $H_k$ is useful only for $k$ small compared with $\log_\sigma n$. Compressed indexes and the [Burrows-Wheeler transform](/burrows-wheeler-transform/) are analysed with $n H_k(s)$.

## Examples and non-examples

**Distributions.**

| distribution | $H$ in bits |
|---|---|
| a fair coin $(1/2, 1/2)$ | 1 |
| a fair die, 6 outcomes | $\log_2 6 = 2.585$ |
| $(1/2, 1/4, 1/8, 1/8)$ | $0.5 \cdot 1 + 0.25 \cdot 2 + 2 \cdot 0.125 \cdot 3 = 1.75$ |
| $(1/2, 1/3, 1/6)$ | $1.459$, which is $H(1/2, 1/2) + \frac{1}{2} H(2/3, 1/3)$ by grouping |
| a biased coin $(0.1, 0.9)$ | $0.469$; see the [binary entropy function](/binary-entropy-function/) |
| any law with one sure outcome | 0 |

For $(1/2, 1/4, 1/8, 1/8)$ the prefix code $0, 10, 110, 111$ has mean length exactly 1.75 bits, because each length equals $\log_2 (1/p)$. For the fair die no code of single symbols reaches 2.585 bits: the best (a [Huffman code](/huffman-coding/)) has mean length $8/3 = 2.667$ bits. Codes on blocks of symbols, or [arithmetic coding](/arithmetic-coding/), close the gap.

**Strings.**

| $s$ | $H_0$ | $H_1$ | $H_2$ | $H_5$ |
|---|---|---|---|---|
| mississippi | 1.823 | 0.796 | 0.182 | 0 |
| abracadabra | 2.040 | 0.545 | 0 | 0 |

For mississippi, the counts are 4, 4, 2, 1 for i, s, p, m. So $n H_0 = 2 \cdot 4 \log_2 \frac{11}{4} + 2 \log_2 \frac{11}{2} + \log_2 11 = 20.05$ bits. For $H_1$ of abracadabra, only the context a has mixed followers (b, c, d, b), which costs $4 \cdot 1.5 = 6$ bits, so $H_1 = 6/11$.

**Non-examples.**

- The string abababab has $H_0 = 1$ but $H_1 = 0$. The zero-order measure does not see the order of the symbols. A low $H_0$ is not the same as compressible, and a high $H_0$ is not the same as random.
- The entropy of a random string is not the empirical entropy of the string that was drawn. For a long string drawn from a memoryless source, $H_0$ of the string is close to $H(X)$ with high probability, but for a short string it is often lower, because the empirical frequencies fit the string.
- $H$ is not the number of bits of a value. A variable with 1000 possible values, one of probability $0.999$, has entropy about $0.02$ bits, not $\log_2 1000$.
- The integral $-\int f \log f$ for a density $f$ (differential entropy) is a different quantity: it can be negative and it changes when the variable is scaled.

## Related definitions

- [Self-information](/self-information/) is the information of one outcome; $H$ is its mean.
- The [binary entropy function](/binary-entropy-function/) is $H$ for two outcomes, as a function of one probability.
- [Conditional entropy](/conditional-entropy/) $H(X \mid Y)$, the chain rule and mutual information measure how much one variable tells about another.
- The [entropy rate](/entropy-rate/) extends $H$ to sources with memory, per symbol.
- The [asymptotic equipartition property](/asymptotic-equipartition-property/) and the [source coding theorem](/source-coding-theorem/) give $H$ its meaning as the limit of lossless compression.
- [Min-entropy](/min-entropy/) $H_\infty(X) = -\log_2 \max_x p(x)$ is at most $H(X)$; it measures the best single guess and is the measure used for randomness extraction.
- [Von Neumann entropy](/von-neumann-entropy/) is the quantum analogue, the entropy of the eigenvalues of a density matrix.
- [Cross-entropy loss](/cross-entropy-loss/) $-\sum p \log q$ is the mean code length when a code built for $q$ is used on data from $p$; it is at least $H(p)$.
- The [entropy estimation problem](/entropy-estimation-problem/) asks for $H_0$ of a stream in small space.

## References
