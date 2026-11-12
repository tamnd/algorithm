---
tag: WKVPS7
kind: definition
slug: universal-code
name: Universal code
aliases:
- universal integer code
- universal codeword set
- asymptotically optimal universal code
area: compression-and-coding/entropy-coding
level: intro
summary: A prefix code for the positive integers whose expected length is within a constant factor of the entropy for every decreasing distribution. Delta and omega are also asymptotically optimal.
prereqs: [prefix-code, shannon-entropy]
see_also: [elias-gamma-coding, elias-delta-coding, elias-omega-coding, fibonacci-coding, exp-golomb-coding, unary-coding, kraft-inequality, variable-byte-encoding]
sources:
  - paper: doi:10.1109/TIT.1975.1055349
    title: Peter Elias, Universal codeword sets and representations of the integers, IEEE Transactions on Information Theory 21(2), 1975
    locator: pp. 194 to 203 (the definitions of a universal and an asymptotically optimal codeword set, and the codes gamma, delta and omega)
  - paper: doi:10.1109/TIT.1987.1057284
    title: Alberto Apostolico and Aviezri S. Fraenkel, Robust transmission of unbounded strings using Fibonacci representations, IEEE Transactions on Information Theory 33(2), 1987
    locator: pp. 238 to 245 (Fibonacci codes for the integers)
  - paper: doi:10.1145/3415148
    title: Giulio Ermanno Pibiri and Rossano Venturini, Techniques for inverted index compression, ACM Computing Surveys 53(6), Article 125, 2020
    locator: Section 2, Integer codes (arXiv:1908.10598v2)
---

A universal code is a [prefix code](/prefix-code/) for the positive integers that is good for every source whose probabilities decrease, without knowing which one. Peter Elias defined it in 1975: the expected codeword length must be within a constant factor of the [entropy](/shannon-entropy/), for every decreasing distribution at the same time. If the factor also tends to 1 as the entropy grows, the code is asymptotically optimal. The [Elias gamma code](/elias-gamma-coding/) and the [Fibonacci code](/fibonacci-coding/) are universal, and the [Elias delta](/elias-delta-coding/) and [Elias omega](/elias-omega-coding/) codes are also asymptotically optimal. The [unary code](/unary-coding/) is not universal.

## Definition

Notation: $x \ge 1$ is the integer coded, $\ell(x)$ is the length of its codeword in bits, logarithms are base 2, and $P$ is the distribution of a memoryless source on the positive integers. The expected length is $E_P[\ell] = \sum_x P(x)\,\ell(x)$ and the entropy is $H(P) = -\sum_x P(x) \log P(x)$.

A distribution $P$ is **decreasing** (Elias says monotone) if $P(1) \ge P(2) \ge P(3) \ge \cdots$. Any source can be put in this form by a sort of its symbols, so the condition only says that the coder and the decoder agree on the rank of each symbol, most likely first.

A prefix code $\ell$ for the positive integers is **universal** if there is a constant $K$ such that

$$\frac{E_P[\ell]}{\max(1, H(P))} \le K$$

for every decreasing $P$ with $H(P) < \infty$. It is **asymptotically optimal** if, in addition, the ratio is at most $R(H(P))$ for a function $R$ with $R(h) \to 1$ as $h \to \infty$.

The $\max(1, \cdot)$ is there because every codeword has at least one bit, so a source with entropy near 0 still costs at least 1 bit per symbol.

**The key lemma.** If $P$ is decreasing, then $x\,P(x) \le P(1) + \cdots + P(x) \le 1$, so $P(x) \le 1/x$ and $\log x \le \log (1/P(x))$. Taking the mean gives

$$E_P[\log x] \le H(P).$$

So a code with $\ell(x) \le f(\log x)$ for a nondecreasing concave $f$ has $E_P[\ell] \le f(E_P[\log x]) \le f(H(P))$, by Jensen's inequality. This reduces universality to a bound on each codeword:

- If $\ell(x) \le c_1 \log x + c_2$ for constants $c_1, c_2$, the code is universal, with $K = c_1 + c_2$.
- If $\ell(x) \le \log x + g(\log x)$ for a concave $g$ with $g(t)/t \to 0$, the code is asymptotically optimal.

**A lower limit.** No prefix code can have $\ell(x) \le \log x + \log \log x$ for all large $x$. The [Kraft inequality](/kraft-inequality/) needs $\sum_x 2^{-\ell(x)} \le 1$, but $\sum_x 1/(x \log x)$ diverges. So the term after $\log x$ in an asymptotically optimal code grows at least like $\log \log x$ infinitely often, and codes such as delta and omega spend $O(\log \log x)$ bits on it.

## Examples and non-examples

**Codes and their constants.** Each row gives a bound $\ell(x) \le f(\log x)$, and so $E_P[\ell] \le f(H(P))$ for each decreasing $P$.

| code | length bound $f(t)$ | universal | asymptotically optimal |
|---|---|---|---|
| [Elias gamma](/elias-gamma-coding/) | $2t + 1$ | yes, $K = 3$ | no, the ratio tends to 2 |
| [Exp-Golomb](/exp-golomb-coding/), order $k$ | $2t + k + 1$ | yes | no, the ratio tends to 2 |
| [Fibonacci](/fibonacci-coding/) | $t / \log \varphi + 2 \approx 1.44t + 2$ | yes | no, the ratio tends to about 1.44 |
| [Variable-byte](/variable-byte-encoding/) | $\tfrac{8}{7} t + 8$ | yes | no, the ratio tends to $8/7$ |
| [Elias delta](/elias-delta-coding/) | $t + 2\log(t + 1) + 1$ | yes, $K = 4$ | yes |
| [Elias omega](/elias-omega-coding/) | $t + 2\log(t+1) + 4$ | yes | yes |
| [Unary](/unary-coding/) | $2^t$ | no | no |

Here $\varphi = (1 + \sqrt 5)/2$. The limits in the last column are those of uniform laws on $\{1, \ldots, N\}$ as $N$ grows. The omega bound is loose: its codeword length is $\log x + \log \log x + \cdots$ plus one bit per level of recursion, but the simple bound is enough for the definition.

**Ratios on some sources.** The ratio $E_P[\ell] / \max(1, H(P))$ for some decreasing laws on $\{1, \ldots, 2^{16}\}$, computed by the harness of this page:

| source | $H(P)$ | unary | gamma | delta | omega | Fibonacci |
|---|---|---|---|---|---|---|
| geometric, $\theta = 0.5$ | 2.00 | 1.00 | 1.13 | 1.32 | 1.19 | 1.41 |
| geometric, $\theta = 0.99$ | 8.08 | 12.38 | 1.46 | 1.33 | 1.48 | 1.19 |
| Zipf, $P(x) \propto 1/x$ | 11.14 | 504.2 | 1.38 | 1.14 | 1.20 | 1.10 |
| power law, $P(x) \propto 1/x^2$ | 2.36 | 3.00 | 1.04 | 1.13 | 1.09 | 1.26 |
| uniform | 16.00 | 2048 | 1.81 | 1.37 | 1.37 | 1.38 |

The geometric law with $\theta = 0.5$ is $P(x) = 2^{-x}$, for which unary is the optimal code. No single code is the best on every row; universality is a guarantee for the worst case, not a promise to be the best.

**The limit of the ratio.** For the uniform law on $\{1, \ldots, 2^m - 1\}$, $H(P) = \log(2^m - 1)$, and the ratios are:

| $m$ | gamma | delta | omega | variable-byte |
|---|---|---|---|---|
| 16 | 1.8125 | 1.3748 | 1.3747 | 1.3740 |
| 256 | 1.9883 | 1.0547 | 1.0508 | 1.1543 |
| 4096 | 1.9993 | 1.0054 | 1.0044 | 1.1435 |
| 65536 | 2.0000 | 1.0005 | 1.0003 | 1.1429 |

The gamma ratio tends to 2 and the variable-byte ratio to $8/7$, so these codes are universal but not asymptotically optimal. The delta and omega ratios tend to 1.

**Non-examples.**

- *The unary code is not universal.* On the Zipf law over $\{1, \ldots, N\}$, the expected unary length is about $N / \ln N$ while the entropy is about $\tfrac12 \log N + \log \ln N$, so no constant $K$ works. On the law $P(x) \propto 1/x^2$ over all $x \ge 1$, the entropy is finite but the expected unary length is infinite.
- *A Golomb or Rice code with a fixed parameter is not universal,* for the same reason: its length grows linearly in $x$.
- *A [Huffman code](/huffman-coding/) built for one source is not universal.* It is optimal for that source, but it covers only a finite alphabet and has no guarantee for any other source.
- *Plain binary is not a prefix code,* so it is not a candidate.

**Levenshtein's code.** In 1968, before Elias, Vladimir Levenshtein gave a recursive code for the integers that is asymptotically optimal in this sense. It codes 0 as `0`. For $x \ge 1$ it writes the binary digits of $x$ without the leading one, then does the same for the number of digits just written, and repeats until that number is 0. A count $C$ of the steps goes first, in unary. Its length is $\log x + \log \log x + \cdots$, plus $O(\log^* x)$ bits, like the [Elias omega code](/elias-omega-coding/).

## Related definitions

- [Prefix code](/prefix-code/), [uniquely decodable code](/uniquely-decodable-code/) and the [Kraft inequality](/kraft-inequality/): every universal code is a prefix code for an infinite alphabet, and the Kraft inequality limits how short its codewords can be.
- [Shannon entropy](/shannon-entropy/) and the [source coding theorem](/source-coding-theorem/): no uniquely decodable code has $E_P[\ell] < H(P)$, so an asymptotically optimal code is within a factor $1 + o(1)$ of the best possible.
- [Elias gamma](/elias-gamma-coding/), [Elias delta](/elias-delta-coding/) and [Elias omega](/elias-omega-coding/) coding: Elias's three codes from the 1975 paper.
- [Fibonacci coding](/fibonacci-coding/) and [exp-Golomb coding](/exp-golomb-coding/): universal codes with other trade-offs, robust resynchronization for Fibonacci, and a tunable first bucket for exp-Golomb.
- [Adaptive modeling](/adaptive-modeling/) and [arithmetic coding](/arithmetic-coding/): the other route to a code that works without a known source, by learning the source as it goes.
- [Kolmogorov complexity](/kolmogorov-complexity/): self-delimiting descriptions of integers use the same kind of length prefix as the Elias codes.

## References
