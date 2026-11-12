---
tag: PY83ZY
kind: theorem
slug: plotkin-bound
name: Plotkin bound
area: compression-and-coding/error-correcting-codes
level: advanced
summary: "When the minimum distance d is more than half the length n, a binary code has at most 2 floor(d/(2d - n)) words. Hadamard codes meet it."
prereqs: [minimum-distance, hamming-distance]
see_also: [hadamard-code, singleton-bound, hamming-bound, elias-bound, griesmer-bound, gilbert-varshamov-bound, delsarte-lp-bound, simplex-code]
sources:
  - paper: doi:10.1109/TIT.1960.1057584
    title: M. Plotkin, Binary codes with specified minimum distance, IRE Transactions on Information Theory 6(4), 1960
    locator: pp. 445 to 450 (the bound for binary codes with 2d > n)
  - paper: "V. I. Levenshtein, The application of Hadamard matrices to a problem in coding, Problemy Kibernetiki 5, 1961, pages 123 to 136; English translation in Problems of Cybernetics 5, 1964, pages 166 to 184"
    locator: the construction of codes that meet the Plotkin bound from Hadamard matrices
  - book: isbn:9780444851932
    title: F. J. MacWilliams and N. J. A. Sloane, The Theory of Error-Correcting Codes, North-Holland, 1977
    locator: Chapter 2 (the Plotkin bound, Hadamard matrices and Hadamard codes, Levenshtein's theorem)
  - book: isbn:9780521782807
    title: W. Cary Huffman and Vera Pless, Fundamentals of Error-Correcting Codes, Cambridge University Press, 2003
    locator: Chapter 2 (the Plotkin upper bound and its asymptotic form)
  - url: https://aeb.win.tue.nl/codes/binary-1.html
    title: A. E. Brouwer, Table of general binary codes
    locator: the values of A(n, d) for d = 4 to 12 used in the table of this page
---

The Plotkin bound limits the size of a code whose [minimum distance](/minimum-distance/) is a large fraction of its length. For binary codes it says that if $2d > n$, a code of length $n$ and minimum distance $d$ has at most $2\lfloor d/(2d - n) \rfloor$ words. It holds for all codes, linear or not. In the range $\delta = d/n > 1/2$ a binary code can have only a bounded number of words, and the [Hadamard codes](/hadamard-code/) meet the bound with equality. Its asymptotic form, $R \le 1 - 2\delta$, is the first bound that goes to zero rate at $\delta = 1/2$.

## Statement

Notation. $A_q(n, d)$ is the largest size of a code of length $n$ over an alphabet of $q$ symbols with minimum distance at least $d$, linear or not. $\theta = 1 - 1/q$, so $\theta = 1/2$ for binary codes. Rate is $R = \log_q |C| / n$ and relative distance is $\delta = d/n$.

**Theorem (binary).** If $2d > n$, then

$$A_2(n, d) \le 2 \left\lfloor \frac{d}{2d - n} \right\rfloor .$$

Also $A_2(2d, d) \le 4d$ for every $d$.

**Theorem ($q$-ary).** If $d > \theta n$, then

$$A_q(n, d) \le \frac{d}{d - \theta n}.$$

**Asymptotic form.** For every family of codes over $q$ symbols with relative distance $\delta \le \theta$,

$$R \le 1 - \frac{\delta}{\theta} + o(1), \qquad \text{so } R \le 1 - 2\delta \text{ for binary codes.}$$

For $\delta > \theta$ the size is bounded by a constant, so the rate goes to 0.

**Odd distance.** For binary codes $A_2(n, d) = A_2(n + 1, d + 1)$ when $d$ is odd (add an overall parity bit, or delete one position). So for odd $d$ and $n < 2d + 1$, $A_2(n, d) \le 2\lfloor (d + 1)/(2d + 1 - n) \rfloor$, and $A_2(2d + 1, d) \le 4d + 4$. This is the form in MacWilliams and Sloane, Chapter 2.

## In plain words

Add up the distances between all pairs of codewords. Each pair is far apart, so the total is large. Now count the same total column by column. In one column, a pair adds one only when the two words disagree there, and at most about half of all pairs can disagree in a single column. So the total is also small. When the required distance is more than half the length, these two counts can agree only if the code has few words. Codes built from Hadamard matrices, whose rows disagree in exactly half their places, reach this limit.

## Proof

*Double counting.* Let $C$ have $M$ words and minimum distance $d$. Let $S$ be the sum of $d(x, y)$ over all ordered pairs of distinct words $x, y \in C$. Each pair is at distance at least $d$, so $S \ge M(M - 1) d$.

Now count by positions. Fix a position $j$ and let $m_a$ be the number of words with symbol $a$ there, so $\sum_a m_a = M$. The ordered pairs that disagree at $j$ number $\sum_a m_a (M - m_a) = M^2 - \sum_a m_a^2$. By the Cauchy-Schwarz inequality, $\sum_a m_a^2 \ge M^2/q$, so position $j$ adds at most $\theta M^2$ to $S$, and $S \le n \theta M^2$.

*$q$-ary bound.* From $M(M - 1) d \le n \theta M^2$ we get $(M - 1) d \le n \theta M$, that is $M (d - \theta n) \le d$. When $d > \theta n$ this gives $M \le d/(d - \theta n)$.

*Binary bound.* For $q = 2$, position $j$ adds $2m(M - m)$, where $m$ is the number of zeros. This is at most $M^2/2$ if $M$ is even and $(M^2 - 1)/2$ if $M$ is odd. If $M$ is even, $M(M - 1)d \le nM^2/2$ gives $M \le 2d/(2d - n)$, and since $M$ is even, $M \le 2\lfloor d/(2d - n) \rfloor$. If $M$ is odd, $M(M - 1) d \le n(M^2 - 1)/2$ gives $Md \le n(M + 1)/2$, so $M \le n/(2d - n) = 2d/(2d - n) - 1$. Since $\lfloor 2x \rfloor \le 2\lfloor x \rfloor + 1$, again $M \le 2\lfloor d/(2d - n) \rfloor$.

*Length $2d$.* Split a binary code of length $2d$ by its last symbol and keep the larger half without that symbol. The result is a code of length $2d - 1$ with distance at least $d$ and at least $M/2$ words. The binary bound with $2d - (2d - 1) = 1$ gives at most $2d$ words, so $M \le 4d$.

*Asymptotic form.* Let $m$ be the largest integer with $\theta m < d$, and let $n \ge m$. Group the words of $C$ by their last $n - m$ symbols. Some group has at least $M/q^{n - m}$ words. They agree on the last $n - m$ positions, so their first $m$ symbols form a code of length $m$ with distance at least $d$. The $q$-ary bound applies, and $d - \theta m \ge 1/q$ because $qd - (q - 1)m$ is a positive integer. So $M \le q^{n - m} \cdot q d$. With $m \ge d/\theta - 1$,

$$\frac{\log_q M}{n} \le 1 - \frac{d}{\theta n} + \frac{2 + \log_q d}{n} = 1 - \frac{\delta}{\theta} + O\!\left(\frac{\log n}{n}\right).$$

$\blacksquare$

## Consequences

**Bounded codes above half the length.** For binary codes with $\delta > 1/2$, $A_2(n, d) \le 2\lfloor \delta/(2\delta - 1) \rfloor$ does not grow with $n$. So all good long codes have $\delta \le 1/2$, and in the $q$-ary case $\delta \le \theta$.

**Comparison with other bounds.** The table shows the asymptotic binary bounds on $R$. The Plotkin line $1 - 2\delta$ is below the [Hamming bound](/hamming-bound/) $1 - h(\delta/2)$ for $\delta$ above about $0.313$ and is far below the [Singleton bound](/singleton-bound/) $1 - \delta$. The [Elias bound](/elias-bound/) improves on both.

| $\delta$ | Singleton | Hamming | Plotkin | Elias |
|---|---|---|---|---|
| 0.10 | 0.9 | 0.7136 | 0.8 | 0.7019 |
| 0.20 | 0.8 | 0.5310 | 0.6 | 0.4920 |
| 0.30 | 0.7 | 0.3902 | 0.4 | 0.3117 |
| 0.40 | 0.6 | 0.2781 | 0.2 | 0.1495 |
| 0.45 | 0.55 | 0.2308 | 0.1 | 0.0734 |
| 0.50 | 0.5 | 0.1887 | 0 | 0 |

For $q = 3$ the Plotkin bound is $1 - 3\delta/2$: at $\delta = 0.4$ it gives $0.4$, against $0.4183$ for the Hamming bound.

**A step in other proofs.** The Elias bound applies the same double count to the words that fall in one Hamming ball. The [Griesmer bound](/griesmer-bound/) for linear codes has the same asymptotic line $1 - \delta/\theta$.

## Tightness

**Hadamard codes.** A Hadamard matrix $H$ of order $n$ has entries $\pm 1$ and $H H^T = nI$, so two different rows agree in exactly $n/2$ places. Normalize $H$ so that its first column is all $+1$, and map $+1 \to 0$ and $-1 \to 1$. Three codes follow:

| code | length | words | distance | bound |
|---|---|---|---|---|
| rows, first column deleted | $n - 1$ | $n$ | $n/2$ | $2\lfloor (n/2)/1 \rfloor = n$ |
| those words and their complements | $n - 1$ | $2n$ | $n/2 - 1$ | $4d + 4 = 2n$ (odd form) |
| rows and their complements | $n$ | $2n$ | $n/2$ | $4d = 2n$ |

All three meet the bound with equality. The tests build them from the Sylvester matrices of orders 8 and 16 and from the Paley matrices of orders 12 and 20, and find the stated sizes and distances. The Paley matrix of order 12 gives an $(11, 12, 6)$ code and a $(12, 24, 6)$ code, which no linear code can match, since a linear code has a power of 2 as its size.

**Levenshtein's theorem.** Levenshtein (1961) proved that for even $d$ and $n < 2d$, and for $n = 2d$, the bound is met whenever Hadamard matrices of suitable orders exist. He combines Hadamard codes of two lengths by placing their words side by side. With the odd form, this covers odd $d$ too. So, if the Hadamard conjecture is true (a Hadamard matrix of every order divisible by 4 exists), the Plotkin bound gives the exact value of $A_2(n, d)$ in the whole range $n \le 2d$. The table compares the bound with the values in Brouwer's table for $d = 8, 10, 12$:

| $n$ | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $A_2(n, 8)$ | 4 | 4 | 8 | 16 | 32 | | | | | | | | |
| $A_2(n, 10)$ | 2 | 2 | 2 | 4 | 4 | 6 | 10 | 20 | 40 | | | | |
| $A_2(n, 12)$ | 2 | 2 | 2 | 2 | 2 | 2 | 4 | 4 | 6 | 8 | 12 | 24 | 48 |

Every entry equals the Plotkin bound (with $4d$ at $n = 2d$). The tests check all entries with $d$ even from 4 to 12 and $n \le 2d$, and the odd-distance values one length shorter.

**The $q$-ary bound.** For $q > 2$ the bound is met by codes from other designs, for example the simplex codes. The [simplex code](/simplex-code/) $[(q^k - 1)/(q - 1), k, q^{k - 1}]_q$ has every nonzero word of weight $q^{k-1}$, and here $d - \theta n = q^{k-1} - (q^k - 1)/q = 1/q$, so $d/(d - \theta n) = q^k$, the size of the code.

## History

Plotkin published the bound for binary codes in 1960, with the double counting of distances. Levenshtein (1961, translated in 1964) showed that Hadamard matrices give codes that meet it in the whole range $2d \ge n$, assuming the matrices exist. The $q$-ary form and the asymptotic line $1 - \delta/\theta$ follow from the same count (Huffman and Pless, Chapter 2). Later bounds, from the Elias bound to the [linear programming bound](/delsarte-lp-bound/), improve on it for $\delta < 1/2$.

## References
