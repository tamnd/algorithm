---
tag: EXZCS6
kind: definition
slug: lempel-ziv-complexity
name: Lempel-Ziv complexity
aliases:
- LZ76 complexity
- LZ complexity
area: compression-and-coding/dictionary-compression
level: advanced
summary: The number of components in the exhaustive history of Lempel and Ziv (1976), a computable measure of how new each part of a sequence is.
prereqs: [lempel-ziv-factor, entropy-rate]
see_also: [kolmogorov-complexity, lempel-ziv-factorization, lz77, lz78-parsing, ziv-lempel-entropy-theorem, longest-previous-factor, shannon-entropy, incompressibility-method]
sources:
  - paper: doi:10.1109/TIT.1976.1055501
    title: Abraham Lempel and Jacob Ziv, On the complexity of finite sequences, IEEE Transactions on Information Theory 22(1), 75-81, 1976
    locator: the definitions of reproduction, production, production history, exhaustive history and complexity; the theorem that the exhaustive history has the fewest components; the upper bound on c(n)
  - paper: doi:10.1103/PhysRevA.36.842
    title: F. Kaspar and H. G. Schuster, Easily calculable measure for the complexity of spatiotemporal patterns, Physical Review A 36(2), 842-848, 1987
    locator: the scan that counts the components with symbol comparisons only, and the normalization by n / log_k n
  - paper: doi:10.1162/089976604322860677
    title: José M. Amigó, Janusz Szczepański, Elek Wajnryb and Maria V. Sanchez-Vives, Estimating the entropy rate of spike trains via Lempel-Ziv complexity, Neural Computation 16(4), 717-736, 2004
    locator: the normalized LZ76 complexity as an estimator of the entropy rate, its convergence, and tests on Markov sources
  - url: https://arxiv.org/abs/1311.0822
    title: E. Estevez-Rams, R. Lora Serrano, B. Aragón Fernández and I. Brito Reyes, Properties of maximum Lempel-Ziv complexity strings, arXiv 1311.0822
    locator: the statement of the Lempel-Ziv upper bound with eps(N) = 2(1 + log log(kN)) / log N, and the remark that it holds only where eps(N) < 1
---

The Lempel-Ziv complexity of a finite sequence, from Lempel and Ziv (1976), counts the steps of a simple copying process that builds the sequence from left to right. At each step the process copies as much as it can from what it has already built, and then adds one new symbol. The count, written $c(n)$ for a sequence of length $n$, is small for regular sequences and close to $n / \log_k n$ for random sequences over $k$ symbols. Unlike [Kolmogorov complexity](/kolmogorov-complexity/), it is easy to compute, and its normalized form $c(n) \log_k n / n$ is used as an estimate of the [entropy rate](/entropy-rate/) of a source, in fields from physics to neuroscience.

## Definition

Let $S = s_1 s_2 \cdots s_n$ be a sequence over an alphabet of $k$ symbols, and write $S(i, j) = s_i \cdots s_j$.

**Reproduction.** A sequence $S$ of length $n$ is *reproducible* from its prefix $S(1, j)$ when $S(j+1, n)$ is a substring of $S(1, n-1)$. So the rest is a copy of a part that starts at a position $p \le j$, and the copy may run into the part that it builds, symbol by symbol, as in [LZ77](/lz77/).

**Production.** $S$ is *producible* from $S(1, j)$ when $S(1, n-1)$ is reproducible from $S(1, j)$: a copy, and then one more symbol that can be anything.

**Production history.** A history of $S$ is a cut $S = H_1 H_2 \cdots H_m$ into *components* such that each prefix $H_1 \cdots H_i$ is producible from $H_1 \cdots H_{i-1}$. So each component is a copy of earlier text followed by one symbol, and the last component may be a copy only. The number of components is $c_H(S) = m$.

**Exhaustive history.** In the exhaustive history, each component is as long as possible: the component that starts at $s_i$ is the shortest $S(i, j)$ that is not a substring of $S(1, j-1)$, or $S(i, n)$ if there is none. In the terms of the [Lempel-Ziv factor](/lempel-ziv-factor/) page, it is the longest prefix of $S(i, n)$ that starts at an earlier position, plus the next symbol.

**Complexity.** The Lempel-Ziv complexity $c(S)$ is the number of components of the exhaustive history. Lempel and Ziv proved that no history has fewer components, so also
$$c(S) = \min_H c_H(S).$$
The reason is the usual greedy argument: if the exhaustive history has reached position $g$ after $m$ components and another history has reached $e \le g$, then the copy of the other history's next component, from $g$ on, still occurs earlier, so the exhaustive component reaches at least as far. We write $c(n)$ for the complexity of the prefix of length $n$ of a fixed sequence.

**Bounds.** $c(n) \le n$, and a sequence with $n$ different symbols reaches it. For $n \ge 2$, $c(n) \ge 2$, because the first component is always one symbol. Lempel and Ziv proved the upper bound
$$c(n) < \frac{n}{(1 - \varepsilon_n) \log_k n}, \qquad \varepsilon_n = \frac{2\,(1 + \log_k \log_k (k n))}{\log_k n},$$
for every sequence over $k$ symbols. The bound says something only when $\varepsilon_n < 1$, and $\varepsilon_n$ goes to 0 very slowly.

**Normalization.** The normalized complexity is
$$C(n) = \frac{c(n)}{n / \log_k n} = \frac{c(n) \log_k n}{n}.$$
For a stationary ergodic source over $k$ symbols, $C(n)$ tends to the entropy rate (in units of $\log k$ bits per symbol) as $n \to \infty$, almost surely; Amigó et al. (2004) discuss this and use it as an estimator. One direction is easy: an [LZ78](/lz78-parsing/) parse is a production history, because each LZ78 phrase is an earlier phrase plus one symbol, so $c(n)$ is at most the number of LZ78 phrases, and the [Ziv-Lempel entropy theorem](/ziv-lempel-entropy-theorem/) bounds that number.

**What the implementation computes.** `lz76_complexity` returns $c(n)$ of the exhaustive history above: overlapping copies are allowed, there is no window, and the last component may end with the text without a new symbol. `kaspar_schuster` computes the same number with the scan of Kaspar and Schuster (1987), with symbol comparisons only, and `min_history` takes the minimum over all histories by dynamic programming. The tests check that the three agree on random, periodic and constant sequences, and on the empty sequence ($c = 0$) and a sequence of one symbol ($c = 1$). `normalized` returns $c(n) \log_k n / n$, with $k = 2$ by default.

## Examples and non-examples

- $S$ = `0001101001000101` has the exhaustive history `0`·`001`·`10`·`100`·`1000`·`101`, so $c = 6$. The component `001` is the copy `00` (from position 1, overlapping) plus `1`.
- $S$ = `010011101101100` has the history `0`·`1`·`00`·`11`·`101`·`101100`, so $c = 6$. The last component, at position 10, is a copy of `10110` from position 7, which overlaps it, plus the symbol `0`; it ends exactly at the end of $S$.
- A constant sequence `000...0` of length $n \ge 2$ has `0`·`00...0`, so $c = 2$ for every $n$: the second component copies itself.
- `0101010101` has `0`·`1`·`01010101`, so $c = 3$. In general, if $S$ has period $p$, at most one component starts at a position after $p$, so $c(S) \le c(S(1, p)) + 1$.
- `abcabcabd` has `a`·`b`·`c`·`abcabd`, so $c = 4$.
- Random binary sequences, one sample each with the seed $n$ (from the implementation):

| $n$ | $c(n)$, fair coin | $C(n)$, fair coin (rate 1) | $c(n)$, $P(1) = 0.1$ | $C(n)$, $P(1) = 0.1$ (rate 0.4690) |
|---|---|---|---|---|
| 1000 | 108 | 1.0763 | 48 | 0.4784 |
| 4000 | 351 | 1.0500 | 150 | 0.4487 |
| 16000 | 1175 | 1.0256 | 523 | 0.4565 |
| 64000 | 4092 | 1.0208 | 1836 | 0.4580 |

  The values approach the entropy rate, but slowly, and for the fair coin they lie above 1 at these lengths. The tests check the row $n = 16000$ with a tolerance of 0.05. The upper bound of Lempel and Ziv is 947.1 at $n = 1000$ and 11040.8 at $n = 64000$, far above the values seen.

- *Non-example.* The [LZ78](/lz78-parsing/) parse of `0001101001000101` is `0`·`00`·`1`·`10`·`100`·`1000`·`101`, with 7 phrases, not 6: each LZ78 phrase must extend a whole earlier phrase.
- *Non-example.* The [Lempel-Ziv factorization](/lempel-ziv-factorization/) of the same sequence, where a factor is a copy with no extra symbol, is `0`·`00`·`1`·`1`·`01`·`001`·`0001`·`01`, with 8 factors. Its count $z$ is a different number from $c$, although the two differ by at most a factor of 2.
- *Non-example.* A program that leaves out a last component that is still a copy when the text ends gives 2 for `0101010101`, not 3. The last step of the loop of Kaspar and Schuster ("if $v \ne 1$, add 1") counts this component. Check which rule a library uses before you compare values.

## Related definitions

- **Kaspar and Schuster's scan.** A loop with a start $u$ of the current component, a start $i$ of a trial copy and a match length $v$, which computes $c(n)$ in $O(n^2)$ comparisons in the worst case. With a [suffix tree](/suffix-tree/) or the [longest previous factor](/longest-previous-factor/) array, $c(n)$ takes $O(n)$ time after a suffix sort.
- **LZ77 phrases.** With an unbounded window, the phrases of the [LZ77](/lz77/) triple parse are the components of the exhaustive history, except at the end, where a coder may force an explicit last symbol.
- **Lempel-Ziv factors.** A [Lempel-Ziv factor](/lempel-ziv-factor/) is the copy without the extra symbol; the count $z$ satisfies $c \le z \le 2c$. Each factor is itself a valid component (its last symbol is the extra symbol), so the factorization is a history and $c \le z$. Each component is a copy and one symbol, so cutting each component in two gives a parse into earlier copies and single symbols, and the greedy factorization has at most as many pieces, so $z \le 2c$.
- **Kolmogorov complexity.** [Kolmogorov complexity](/kolmogorov-complexity/) is the length of the shortest program for a sequence. It is not computable. The exhaustive history gives a description of $S$ with a position, a length and a symbol per component, so $K(S) = O(c(n) \log n)$; in this sense $c(n)$ gives a computable upper estimate.
- **Entropy rate and LZ78.** The [Ziv-Lempel entropy theorem](/ziv-lempel-entropy-theorem/) states the matching result for the LZ78 parse and its code length.
- **Maximum LZ complexity normalization.** Some authors divide by the largest $c(n)$ over all sequences of length $n$, not by $n / \log_k n$, so that the normalized value lies in $[0, 1]$.

## References
