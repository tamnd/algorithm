---
tag: 9D53Y5
kind: theorem
slug: griesmer-bound
name: Griesmer bound
area: compression-and-coding/error-correcting-codes
level: advanced
summary: "A linear [n, k, d] code over GF(q) has n >= the sum of ceil(d/q^i) for i from 0 to k - 1. Simplex codes meet it. It holds only for linear codes."
prereqs: [linear-code, minimum-distance]
see_also: [simplex-code, singleton-bound, plotkin-bound, hamming-bound, golay-code, reed-muller-code, hamming-code]
sources:
  - paper: doi:10.1147/rd.45.0532
    title: J. H. Griesmer, A bound for error-correcting codes, IBM Journal of Research and Development 4(5), 1960
    locator: pp. 532 to 542 (the bound for binary linear codes)
  - paper: doi:10.1016/S0019-9958(65)90080-X
    title: G. Solomon and J. J. Stiffler, Algebraically punctured cyclic codes, Information and Control 8(2), 1965
    locator: pp. 170 to 179 (the q-ary bound and codes that meet it, built by deleting subspaces from simplex codes)
  - book: isbn:9780521782807
    title: W. Cary Huffman and Vera Pless, Fundamentals of Error-Correcting Codes, Cambridge University Press, 2003
    locator: Chapter 2 (the Griesmer upper bound and the residual code)
---

The Griesmer bound is a lower bound on the length of a [linear code](/linear-code/). A linear $[n, k, d]_q$ code must have

$$n \ge g_q(k, d) = \sum_{i=0}^{k-1} \left\lceil \frac{d}{q^i} \right\rceil .$$

It holds only for linear codes. Its proof removes the support of a minimum weight codeword and repeats on the shorter code that remains. The [simplex codes](/simplex-code/) and many codes built from them meet it with equality, and for small dimensions it gives the exact shortest length.

## Statement

Notation. GF($q$) is the field with $q$ elements. A linear $[n, k, d]_q$ code is a $k$-dimensional subspace of GF($q$)$^n$ with [minimum distance](/minimum-distance/) $d$. $\theta = 1 - 1/q$.

**Theorem (linear codes only).** For every linear $[n, k, d]_q$ code with $k \ge 1$,

$$n \ge \sum_{i=0}^{k-1} \left\lceil \frac{d}{q^i} \right\rceil .$$

**Lemma (residual code).** Let $C$ be a linear $[n, k, d]_q$ code with $k \ge 2$, and let $c \in C$ have weight $d$. Restrict every codeword to the $n - d$ positions where $c$ is zero. The result, the residual code of $C$ with respect to $c$, is a linear $[n - d, k - 1, d']_q$ code with $d' \ge \lceil d/q \rceil$.

**Asymptotic form.** For a family of linear codes with relative distance $\delta \le \theta$, the rate satisfies $R \le 1 - \delta/\theta + O(\log n / n)$. For binary codes this is $R \le 1 - 2\delta$, the same line as the asymptotic [Plotkin bound](/plotkin-bound/).

## In plain words

Pick a codeword of the least weight and look only at the places where it is zero. On those places the code still has one dimension less, and its words still have weight at least a fraction $1/q$ of the original distance. Repeat this. Each round uses up the support of one codeword, and the supports must fit inside the length, so their sizes add up to a lower bound on the length. The first round costs $d$ places, the next about $d/q$, the next about $d/q^2$, and so on, and each round costs at least one place.

## Proof

*Lemma.* The restriction map from $C$ to its residual code is linear, so the residual code is linear. Let $S$ be the support of $c$, with $|S| = d$.

Kernel. Let $x \in C$ be zero outside $S$. For each $j \in S$ the ratio $x_j / c_j$ is in GF($q$). Some value $\alpha$ is taken at least $d/q$ times, by the pigeonhole principle. The word $x - \alpha c$ is in $C$, is zero outside $S$, and is zero on at least $d/q$ places of $S$. So its weight is at most $d - d/q < d$, and it must be the zero word. So $x = \alpha c$, the kernel is spanned by $c$, and the residual code has dimension $k - 1$.

Distance. Let $x \in C$ have a nonzero restriction of weight $w'$. Choose $\alpha$ as above, taken $f \ge \lceil d/q \rceil$ times as a ratio on $S$. Then $x - \alpha c$ is a nonzero codeword, since it agrees with $x$ outside $S$. Its weight is $w' + (d - f)$, and this is at least $d$. So $w' \ge f \ge \lceil d/q \rceil$.

*Theorem.* Induction on $k$. For $k = 1$ the code has a word of weight $d$, so $n \ge d$. For $k \ge 2$, the lemma gives a code of length $n - d$, dimension $k - 1$ and distance $d' \ge \lceil d/q \rceil$. By induction, and because $g_q(k - 1, \cdot)$ does not decrease,

$$n - d \ge \sum_{i=0}^{k-2} \left\lceil \frac{\lceil d/q \rceil}{q^i} \right\rceil = \sum_{i=0}^{k-2} \left\lceil \frac{d}{q^{i+1}} \right\rceil ,$$

using $\lceil \lceil a/b \rceil / c \rceil = \lceil a/(bc) \rceil$ for positive integers. Adding $d$ gives the bound.

*Asymptotic form.* Let $m = \lceil \log_q d \rceil$. If $k > m$, then the terms with $i < m$ add up to at least $d(1 - q^{-m})/\theta \ge (d - 1)/\theta$, and the other $k - m$ terms are each at least 1. So $n \ge (d - 1)/\theta + k - m$, which gives $k/n \le 1 - \delta/\theta + (m + 2)/n$, and $m = O(\log n)$. If $k \le m$, the rate is $O(\log n / n)$. $\blacksquare$

## Consequences

**Stronger than the Singleton bound for linear codes.** Each term is at least 1, and the first is $d$, so $g_q(k, d) \ge d + k - 1$. This is the [Singleton bound](/singleton-bound/). The two agree only when $d \le q$, which is why MDS codes of large distance need large alphabets.

**Values for binary codes.** The table compares $g_2(k, d)$ with the shortest length of a binary linear code. The tests compute each entry.

| $k$ | $d$ | $g_2(k, d)$ | shortest $n$ | a code of that length |
|---|---|---|---|---|
| 4 | 3 | 7 | 7 | [Hamming code](/hamming-code/) $[7, 4, 3]$ |
| 4 | 4 | 8 | 8 | extended Hamming code $[8, 4, 4]$ |
| 4 | 8 | 15 | 15 | simplex code $[15, 4, 8]$ |
| 5 | 8 | 16 | 16 | [Reed-Muller code](/reed-muller-code/) $RM(1, 4)$ |
| 5 | 3 | 8 | 9 | shortened Hamming code $[9, 5, 3]$ |
| 12 | 7 | 22 | 23 | [Golay code](/golay-code/) $[23, 12, 7]$ |
| 12 | 8 | 23 | 24 | extended Golay code $[24, 12, 8]$ |

For $k = 5$ and $d = 3$, a code of length 8 would have $2^5 (1 + 8) = 288 > 2^8$, against the [Hamming bound](/hamming-bound/). The binary Golay code misses the Griesmer bound by one. No $[22, 12, 7]$ code exists by the Hamming bound, and no $[23, 12, 8]$ code exists because $A_2(23, 8) = 2048$ (Brouwer's table). The ternary Golay code $[11, 6, 5]_3$ meets it: $5 + 2 + 1 + 1 + 1 + 1 = 11$.

**Small dimensions.** A binary $[n, k]$ code with no zero column is a multiset of $n$ nonzero vectors in GF(2)$^k$. The tests search all such multisets and find that the shortest length equals $g_2(k, d)$ for $k \le 3$ and $d \le 8$, and for $k = 4$ and $d \le 4$.

## Tightness

**Simplex codes.** The $q$-ary simplex code has one column for each point of the projective space PG($k - 1, q$). It is a $[(q^k - 1)/(q - 1), k, q^{k-1}]_q$ code, and every nonzero word has weight $q^{k-1}$. Here $g_q(k, q^{k-1}) = q^{k-1} + q^{k-2} + \dots + 1 = (q^k - 1)/(q - 1)$, so the bound is met. The tests check this for $q = 2$ with $k \le 4$, for $q = 3$ with $k \le 3$ and for $q = 5$ with $k \le 2$.

**Deleting subspaces.** Solomon and Stiffler (1965) built more codes that meet the bound by deleting from copies of a simplex code the columns of disjoint subspaces. In the binary case with $k = 4$, deleting the nonzero points of a $u$-dimensional subspace from the $[15, 4, 8]$ simplex code leaves a $[15 - (2^u - 1), 4, 8 - 2^{u-1}]$ code. For $u = 1, 2, 3$ this gives $[14, 4, 7]$, $[12, 4, 6]$ and $[8, 4, 4]$, each of Griesmer length. A codeword misses its weight 8 only on the deleted points where it is 1, and these are $0$ or $2^{u-1}$ of them.

**When it fails.** The bound is not met in general, as the $[9, 5, 3]$ and Golay examples show. The codes that meet it are called Griesmer codes, and finding them for given $k$ and $d$ is a research topic in finite geometry.

**Nonlinear codes.** The bound does not hold for nonlinear codes, because the proof needs the residual code to be linear of dimension $k - 1$. The Paley Hadamard matrix of order 20 gives a nonlinear binary code of length 19 with 20 words and distance 10 (see the [Plotkin bound](/plotkin-bound/)). Any 16 of its words form a code with $2^4$ words, but a linear $[n, 4, 10]$ code needs $n \ge 10 + 5 + 3 + 2 = 20$.

## History

Griesmer (1960) proved the bound for binary linear codes, at IBM. Solomon and Stiffler (1965) gave the $q$-ary form and built codes that meet it by puncturing cyclic simplex codes on subspaces. The proof by the residual code is the standard one in textbooks (Huffman and Pless, Chapter 2).

## References
