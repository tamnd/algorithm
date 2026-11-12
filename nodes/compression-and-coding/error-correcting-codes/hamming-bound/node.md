---
tag: 39271D
kind: theorem
slug: hamming-bound
name: Hamming bound
aliases:
- sphere-packing bound
- sphere packing bound
area: compression-and-coding/error-correcting-codes
level: core
summary: A code of length n over q symbols that corrects t errors has at most q^n / V_q(n, t) words, because the balls of radius t around its words are disjoint.
prereqs: [hamming-distance, minimum-distance]
see_also: [singleton-bound, plotkin-bound, elias-bound, gilbert-varshamov-bound, delsarte-lp-bound, hamming-code, golay-code, syndrome-decoding]
sources:
  - paper: doi:10.1002/j.1538-7305.1950.tb00463.x
    title: R. W. Hamming, Error detecting and error correcting codes, Bell System Technical Journal 29(2), 1950
    locator: pp. 147 to 160 (single error correcting codes, and the geometric model of the n-cube with the Hamming distance)
  - book: isbn:9780444851932
    title: F. J. MacWilliams and N. J. A. Sloane, The Theory of Error-Correcting Codes, North-Holland, 1977
    locator: Chapter 1 (the sphere packing bound and perfect codes) and Chapter 6 (the classification of perfect codes)
  - book: isbn:9780521845045
    title: Ron M. Roth, Introduction to Coding Theory, Cambridge University Press, 2006
    locator: Section 4.2 (the sphere-packing bound) and Section 4.5 (asymptotic bounds)
  - paper: doi:10.1137/0124010
    title: Aimo Tietäväinen, On the nonexistence of perfect codes over finite fields, SIAM Journal on Applied Mathematics 24(1), 1973
    locator: pp. 88 to 96 (the main theorem)
  - paper: "V. A. Zinoviev and V. K. Leontiev, The nonexistence of perfect codes over Galois fields, Problems of Control and Information Theory 2(2), 1973"
    title: The nonexistence of perfect codes over Galois fields
    locator: pp. 16 to 24 of the English translation (Russian original pp. 123 to 132)
  - book: isbn:9783540641339
    title: J. H. van Lint, Introduction to Coding Theory, third edition, Springer, 1999
    locator: Chapter 7 (perfect codes, and the history of the nonexistence theorem)
  - paper: "J. L. Vasil'ev, On nongroup close-packed codes, Problemy Kibernetiki 8, 1962"
    title: On nongroup close-packed codes
    locator: The construction of perfect single error correcting binary codes that are not linear
  - url: https://aeb.win.tue.nl/codes/binary-1.html
    title: Andries E. Brouwer, Table of general binary codes (bounds on A_2(n, d))
    locator: The table for d = 4 to 16 and n up to 28
---

The Hamming bound, or sphere packing bound, is an upper bound on the number of words of a code with a given length and minimum distance. It says that a code of length $n$ over $q$ symbols that corrects $t$ errors has at most $q^n / V_q(n, t)$ words, where $V_q(n, t)$ is the number of words in a [Hamming ball](/hamming-distance/) of radius $t$. It holds for all codes, linear or not. The codes that meet it with equality are the *perfect* codes, and over a finite field the only nontrivial ones have the parameters of the [Hamming codes](/hamming-code/) or of the two [Golay codes](/golay-code/).

## Statement

Notation. $\Sigma$ is an alphabet of size $q \ge 2$, and words are rows in $\Sigma^n$. The [Hamming distance](/hamming-distance/) $d(x, y)$ counts the positions where $x$ and $y$ differ. A code $C \subseteq \Sigma^n$ has [minimum distance](/minimum-distance/) $d$ if any two distinct words of $C$ are at distance at least $d$. $A_q(n, d)$ is the largest size of such a code, linear or not. A linear code is an $[n, k, d]_q$ code over GF($q$), and $t = \lfloor (d - 1)/2 \rfloor$. The ball of radius $r$ around $x$ is $B(x, r) = \{ y : d(x, y) \le r \}$, and its size does not depend on $x$:

$$V_q(n, r) = \sum_{i=0}^{r} \binom{n}{i} (q - 1)^i.$$

**Theorem (finite form, all codes).** For $q \ge 2$ and $1 \le d \le n$,

$$A_q(n, d) \le \left\lfloor \frac{q^n}{V_q(n, t)} \right\rfloor, \qquad t = \left\lfloor \frac{d - 1}{2} \right\rfloor.$$

For a linear $[n, k, d]_q$ code this reads $q^{n-k} \ge V_q(n, t)$: the $n - k$ check symbols must name at least as many syndromes as there are error patterns of weight at most $t$.

**Theorem (asymptotic form).** Let $h_q(x) = x \log_q (q - 1) - x \log_q x - (1 - x) \log_q (1 - x)$ be the $q$-ary entropy function, with $h_2 = h$, the [binary entropy function](/binary-entropy-function/). For each $\delta \in [0, 1]$,

$$\limsup_{n \to \infty} \frac{1}{n} \log_q A_q(n, \lceil \delta n \rceil) \le 1 - h_q(\delta / 2).$$

So a family of codes with relative distance $\delta = d/n$ has rate $R \le 1 - h_q(\delta/2) + o(1)$.

**Definition (perfect code).** A code with minimum distance $d = 2t + 1$ is perfect if $|C| \cdot V_q(n, t) = q^n$, that is, if the balls of radius $t$ around its words fill $\Sigma^n$ with no overlap.

**Theorem (perfect codes over prime power alphabets; Tietäväinen 1973, Zinoviev and Leontiev 1973, after van Lint).** Let $q$ be a prime power. A perfect code over an alphabet of $q$ symbols with $t \ge 1$ and at least two words has the parameters of one of:

1. a Hamming code, $n = (q^r - 1)/(q - 1)$, $|C| = q^{n - r}$, $d = 3$;
2. the binary Golay code, $n = 23$, $|C| = 2^{12}$, $d = 7$;
3. the ternary Golay code, $n = 11$, $|C| = 3^6$, $d = 5$;
4. a binary repetition code of odd length $n$, $|C| = 2$, $d = n$.

The theorem is about parameters only. Perfect binary codes with the parameters of Hamming codes that are not linear exist for every length $2^r - 1 \ge 15$, so the theorem does not say that each perfect code is a Hamming code.

## In plain words

Put a ball around each codeword: the ball holds every word that is at most a few changes away. If the code can correct that many changes, no two balls can touch, because a received word in two balls would have two equally good answers. All balls have the same size, and they all fit in the space of all words. So the number of codewords times the size of one ball is at most the number of all words.

A code that fills the space with its balls, with no gap and no overlap, is perfect. Such codes are very rare: apart from trivial ones, only the Hamming codes and the two Golay codes have the right sizes.

## Proof

*Finite form.* Let $C$ have minimum distance $d \ge 2t + 1$. Suppose that $y \in B(x, t) \cap B(x', t)$ for distinct $x, x' \in C$. By the triangle inequality, $d(x, x') \le d(x, y) + d(y, x') \le 2t \le d - 1$, which contradicts $d(x, x') \ge d$. So the balls $B(x, t)$ for $x \in C$ are pairwise disjoint. Each has $V_q(n, t)$ words, because a word at distance exactly $i$ from $x$ is fixed by the choice of $i$ positions ($\binom{n}{i}$ ways) and of a new symbol at each of them ($(q-1)^i$ ways). The union lies in $\Sigma^n$, so $|C| \cdot V_q(n, t) \le q^n$. Since $|C|$ is an integer, $|C| \le \lfloor q^n / V_q(n, t) \rfloor$. This holds for every code with minimum distance $d$, so it holds for $A_q(n, d)$.

*Asymptotic form.* First a lower bound on the ball. For $0 \le t \le n$, the binomial estimate $\binom{n}{t} \ge 2^{n h(t/n)}/(n + 1)$ holds (proof on the page of the [binary entropy function](/binary-entropy-function/)). Since $n h_q(t/n) \log_2 q = n h(t/n) + t \log_2 (q - 1)$,

$$V_q(n, t) \ge \binom{n}{t} (q - 1)^t \ge \frac{q^{n h_q(t/n)}}{n + 1}.$$

Put this in the finite form: $\frac{1}{n} \log_q A_q(n, d) \le 1 - h_q(t/n) + \frac{\log_q (n + 1)}{n}$. With $d = \lceil \delta n \rceil$ and $t = \lfloor (d - 1)/2 \rfloor$, we have $|t/n - \delta/2| \le 2/n$, and $h_q$ is continuous on $[0, 1]$. The last term tends to 0. Taking the limit superior gives $1 - h_q(\delta/2)$. $\blacksquare$

The proof of the theorem on perfect codes uses Lloyd's theorem (the Lloyd polynomial of a perfect code has $t$ distinct integer zeros in $[1, n]$) and a long number theoretic case analysis; it is not given here. See Tietäväinen (1973) and van Lint, Chapter 7.

## Consequences

**Perfect codes decode with a table of coset leaders of weight at most t.** For a perfect linear code, every syndrome is the syndrome of exactly one error of weight at most $t$. So [syndrome decoding](/syndrome-decoding/) corrects every error of weight at most $t$ and never fails: it always outputs a codeword, and it is wrong whenever more than $t$ errors occur. The [Hamming code](/hamming-code/) $[7, 4, 3]$ has $2^3 = 8 = V_2(7, 1)$ syndromes, and the binary [Golay code](/golay-code/) $[23, 12, 7]$ has $2^{11} = 2048 = 1 + 23 + 253 + 1771 = V_2(23, 3)$.

**Values.** The table compares the bound with the true value of $A_2(n, d)$ from Brouwer's table. For even $d$ the binary bound is better when applied to $(n - 1, d - 1)$, since $A_2(n, d) = A_2(n - 1, d - 1)$.

| $n$ | $d$ | $\lfloor 2^n / V_2(n, t) \rfloor$ | $A_2(n, d)$ |
|---|---|---|---|
| 7 | 3 | 16 | 16 |
| 9 | 3 | 51 | 40 |
| 10 | 3 | 93 | 72 |
| 15 | 3 | 2048 | 2048 |
| 15 | 5 | 270 | 256 |
| 23 | 7 | 4096 | 4096 |

**The asymptotic curve.** For binary codes, with $R \le 1 - h(\delta/2)$, the bound against the [Gilbert-Varshamov](/gilbert-varshamov-bound/) existence bound $R \ge 1 - h(\delta)$:

| $\delta$ | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 |
|---|---|---|---|---|---|
| Hamming, $1 - h(\delta/2)$ | 0.7136 | 0.5310 | 0.3902 | 0.2781 | 0.1887 |
| Gilbert-Varshamov, $1 - h(\delta)$ | 0.5310 | 0.2781 | 0.1187 | 0.0290 | 0 |

The Hamming bound stays positive up to $\delta = 1$, but no binary family with $\delta > 1/2$ has positive rate, by the [Plotkin bound](/plotkin-bound/). For large $\delta$ the Plotkin, [Elias](/elias-bound/) and [linear programming](/delsarte-lp-bound/) bounds are much better.

## Tightness

- **Perfect codes meet it.** The Hamming codes of length $2^r - 1$, the binary Golay code $(23, 2^{12}, 7)$ and the ternary Golay code $(11, 3^6, 5)$ meet it with equality. The tests build each of them, check the minimum distance by enumeration, and check that the syndromes of all errors of weight at most $t$ are distinct and fill all $q^{n-k}$ syndromes.
- **The arithmetic condition is not enough.** A search over binary $n \le 1100$ and $t \le 8$ finds exactly three families where $V_2(n, t)$ is a power of 2 with $n > 2t + 1$: $t = 1$ with $n = 2^r - 1$, $(n, t) = (23, 3)$, and $(n, t) = (90, 2)$, where $V_2(90, 2) = 1 + 90 + 4005 = 2^{12}$. No $(90, 2^{78}, 5)$ code exists. Proof: translate the code so that it holds the zero word. Every other codeword has weight at least 5. Each of the 88 words of weight 3 with ones in positions 1 and 2 lies within distance 2 of exactly one codeword. That codeword is not the zero word, so it has weight 5, and it has ones in positions 1 and 2. A codeword of weight 5 with ones in positions 1 and 2 covers exactly 3 of these 88 words. So 3 divides 88, which is false.
- **Most parameters are far from it.** $A_2(9, 3) = 40$ while the bound is 51, and $A_2(15, 5) = 256$ while the bound is 270. For $d = 2t + 1$ with $t \ge 4$ and binary codes, no length has equality except the repetition codes, by the classification.

## History

Hamming (1950) introduced the distance that has his name, viewed codes as sets of vertices of the $n$-cube, and counted the vertices around a codeword to find the best single error correcting codes; the bound is named after him. Golay's note of 1949 already gave the perfect binary code of length 23 and the ternary one of length 11. The classification of perfect codes over prime power alphabets was finished in 1973 by Tietäväinen and, independently, by Zinoviev and Leontiev, after partial results of van Lint and others. Vasil'ev (1962) found the first perfect binary codes that are not linear, with the parameters of Hamming codes.

## References
