---
tag: 12WDFJ
kind: theorem
slug: gilbert-varshamov-bound
name: Gilbert-Varshamov bound
aliases:
- GV bound
- Gilbert bound
- Varshamov bound
area: compression-and-coding/error-correcting-codes
level: advanced
summary: "Codes with q^n / V_q(n, d - 1) words and distance d exist, also linear ones, so rate 1 - h_q(delta) is reachable. Random linear codes reach it."
prereqs: [minimum-distance, linear-code, binary-entropy-function]
see_also: [hamming-bound, elias-bound, delsarte-lp-bound, plotkin-bound, parity-check-matrix, probabilistic-method, hamming-code, list-decoding]
sources:
  - paper: doi:10.1002/j.1538-7305.1952.tb01393.x
    title: E. N. Gilbert, A comparison of signalling alphabets, Bell System Technical Journal 31(3), 1952
    locator: pp. 504 to 522 (the greedy argument for codes of given minimum distance)
  - paper: "R. R. Varshamov, Estimate of the number of signals in error correcting codes, Doklady Akademii Nauk SSSR 117, 1957, pages 739 to 741"
    locator: the construction of a parity-check matrix column by column
  - book: isbn:9780521845045
    title: Ron M. Roth, Introduction to Coding Theory, Cambridge University Press, 2006
    locator: Section 4.3 (the Gilbert-Varshamov bound) and Section 4.5 (asymptotic bounds)
  - paper: doi:10.1109/tit.1986.1057187
    title: J. H. Conway and N. J. A. Sloane, Lexicographic codes, error-correcting codes from game theory, IEEE Transactions on Information Theory 32(3), 1986
    locator: pp. 337 to 348 (the greedy codes in lexicographic order are linear over GF(2))
  - paper: doi:10.1109/tit.2004.831751
    title: Tao Jiang and Alexander Vardy, Asymptotic improvement of the Gilbert-Varshamov bound on the size of binary codes, IEEE Transactions on Information Theory 50(8), 2004
    locator: pp. 1655 to 1664 (a gain of a factor of order n over the Gilbert bound)
  - paper: doi:10.1002/mana.19821090103
    title: M. A. Tsfasman, S. G. Vladut and T. Zink, Modular curves, Shimura curves, and Goppa codes, better than Varshamov-Gilbert bound, Mathematische Nachrichten 109, 1982
    locator: pp. 21 to 28 (codes over square alphabets of size at least 49 above the GV line)
  - url: https://aeb.win.tue.nl/codes/binary-1.html
    title: A. E. Brouwer, Table of general binary codes
    locator: the values of A(n, d) in the table of this page
---

The Gilbert-Varshamov bound (GV bound) is a lower bound on the best size of a code. It says that a code of length $n$ over $q$ symbols with [minimum distance](/minimum-distance/) $d$ and at least $q^n / V_q(n, d - 1)$ words exists, where $V_q(n, r)$ is the number of words in a Hamming ball of radius $r$. Gilbert proved it with a greedy choice of words. Varshamov proved a version for [linear codes](/linear-code/), built by choosing the columns of a [parity-check matrix](/parity-check-matrix/) one at a time. In rates it says that $R = 1 - h_q(\delta)$ is reachable, and random linear codes reach it with high probability. For binary codes, no better lower bound on the rate is known.

## Statement

Notation. $A_q(n, d)$ is the largest size of a code of length $n$ over $q$ symbols with minimum distance at least $d$, linear or not. $V_q(n, r) = \sum_{i=0}^{r} \binom{n}{i} (q - 1)^i$. $\theta = 1 - 1/q$. $h_q(x) = x \log_q(q - 1) - x \log_q x - (1 - x)\log_q(1 - x)$ is the $q$-ary entropy function, and $h = h_2$ is the [binary entropy function](/binary-entropy-function/).

**Theorem (Gilbert, all codes).** For all $n$ and $1 \le d \le n$,

$$A_q(n, d) \ge \frac{q^n}{V_q(n, d - 1)} .$$

**Theorem (Varshamov, linear codes).** Let $q$ be a prime power. If

$$V_q(n - 1, d - 2) < q^{n - k},$$

then a linear $[n, k]$ code over GF($q$) with minimum distance at least $d$ exists. With the largest such $k$, the code has at least $q^{n-1}/V_q(n - 1, d - 2) \ge q^n / V_q(n, d - 1)$ words, so a linear code reaches the Gilbert bound.

**Asymptotic form.** For $0 \le \delta < \theta$ and $n \to \infty$, there are linear codes with relative distance at least $\delta$ and rate

$$R \ge 1 - h_q(\delta) - o(1).$$

**Random linear codes.** For every $\varepsilon > 0$, a random $k \times n$ generator matrix over GF($q$) with $k \le (1 - h_q(\delta) - \varepsilon) n$ gives a code of rank $k$ and minimum distance at least $\delta n$ with probability $1 - q^{-\varepsilon n + o(n)}$.

## In plain words

Pick codewords one at a time. Each new word must be far from all the words picked so far, so each pick rules out a ball of nearby words. Stop when nothing is left. At that point the balls around the chosen words cover every word, so there must be many chosen words: at least the total number of words divided by the size of one ball. Varshamov did the same with the columns of a check matrix, which gives a linear code. Picking a code at random does just as well, and nobody knows a binary code family that does much better.

## Proof

*Gilbert.* Let $C$ be a code with minimum distance at least $d$ to which no word can be added, for example the result of the greedy choice. Every word $w$ is at distance at most $d - 1$ from some word of $C$, since otherwise $w$ could be added. So the balls of radius $d - 1$ around the words of $C$ cover all $q^n$ words, and $|C| \cdot V_q(n, d - 1) \ge q^n$.

*Varshamov.* Let $r = n - k$. Choose columns $h_1, \dots, h_n \in$ GF($q$)$^r$ one at a time. When choosing $h_j$, forbid every linear combination of at most $d - 2$ of $h_1, \dots, h_{j-1}$, including the zero vector. There are at most $\sum_{i=0}^{d-2} \binom{j-1}{i}(q - 1)^i = V_q(j - 1, d - 2) \le V_q(n - 1, d - 2) < q^r$ such combinations, so a column is always left. Now any $d - 1$ of the chosen columns are linearly independent: in a nontrivial relation, the column with the largest index would be a combination of at most $d - 2$ earlier ones. So the code $\{x : \sum_j x_j h_j = 0\}$ has no nonzero word of weight below $d$. Its dimension is at least $n - r = k$.

For the size, take the largest $k$ with $V = V_q(n - 1, d - 2) < q^{n - k}$. Then $q^{n - k - 1} \le V$, so $q^k \ge q^{n - 1}/V$. By Pascal's rule, $V_q(n, d - 1) - q V_q(n - 1, d - 2) = \binom{n-1}{d-1}(q - 1)^{d-1} \ge 0$, so $q^{n-1}/V \ge q^n / V_q(n, d - 1)$.

*Ball estimate.* For $0 \le p \le \theta$, $V_q(n, pn) \le q^{n h_q(p)}$. By the binomial theorem,

$$1 = \sum_{i=0}^{n} \binom{n}{i} p^i (1 - p)^{n-i} \ge \sum_{i \le pn} \binom{n}{i} (q - 1)^i \left(\frac{p}{q - 1}\right)^{i} (1 - p)^{n - i} .$$

Since $p \le \theta$, the ratio $p / ((q - 1)(1 - p))$ is at most 1, so for $i \le pn$ the factor $(p/(q - 1))^i (1 - p)^{n-i}$ is at least $(p/(q - 1))^{pn} (1 - p)^{(1-p)n} = q^{-n h_q(p)}$. So $1 \ge V_q(n, pn) \, q^{-n h_q(p)}$.

*Asymptotic form.* With $d = \lceil \delta n \rceil$, Varshamov's code has $k \ge n - 1 - \log_q V_q(n, d) \ge n - 1 - n h_q(\delta + 1/n)$, so $k/n \ge 1 - h_q(\delta) - o(1)$.

*Random linear codes.* For a fixed nonzero message $m$ and a uniform random matrix $G$, the word $mG$ is uniform on GF($q$)$^n$. So $P(\mathrm{wt}(mG) < d) = V_q(n, d - 1)/q^n$. By the [union bound](/union-bound/) over the $q^k - 1$ messages, the probability that some nonzero message gives a word of weight below $d$, including the zero word, is less than $q^k V_q(n, d - 1)/q^n \le q^{k - n + n h_q(\delta)} \le q^{-\varepsilon n}$. Outside this event $G$ has rank $k$ and the code has distance at least $d$. $\blacksquare$

## Consequences

**Finite values.** The table shows the three lower bounds for binary codes next to the true value $A_2(n, d)$ from Brouwer's table. The lexicode is the greedy code that scans the words in lexicographic order. The tests compute each entry except the last lexicode.

| $n$ | $d$ | Gilbert | Varshamov | lexicode | $A_2(n, d)$ |
|---|---|---|---|---|---|
| 7 | 3 | 5 | 16 | 16 | 16 |
| 10 | 3 | 19 | 64 | 64 | 72 |
| 12 | 4 | 14 | 32 | 128 | 144 |
| 15 | 5 | 17 | 64 | 128 | 256 |
| 16 | 6 | 10 | 32 | 128 | 256 |
| 23 | 7 | 58 | 128 | 4096 | 4096 |

For $d = 3$, Varshamov's construction picks distinct nonzero columns, and at $n = 2^r - 1$ it picks all of them: the [Hamming code](/hamming-code/). For short lengths the bound is weak, and greedy codes do much better than it promises. Conway and Sloane (1986) proved that binary lexicodes are always linear, and that the lexicode of length 23 and distance 7 is the Golay code.

**Asymptotic comparison.** For binary codes, the GV line lies below all known upper bounds. The table shows it next to the [Hamming bound](/hamming-bound/), the [Elias bound](/elias-bound/) and the first MRRW bound $h(1/2 - \sqrt{\delta(1 - \delta)})$, which come from the [linear programming bound](/delsarte-lp-bound/).

| $\delta$ | GV, $1 - h(\delta)$ | MRRW (first) | Elias | Hamming |
|---|---|---|---|---|
| 0.05 | 0.7136 | 0.8582 | 0.8279 | 0.8313 |
| 0.10 | 0.5310 | 0.7219 | 0.7019 | 0.7136 |
| 0.20 | 0.2781 | 0.4690 | 0.4920 | 0.5310 |
| 0.30 | 0.1187 | 0.2502 | 0.3117 | 0.3902 |
| 0.40 | 0.0290 | 0.0815 | 0.1495 | 0.2781 |
| 0.50 | 0 | 0 | 0 | 0.1887 |

**Codes that reach it.** The proof shows that almost all linear codes of rate $1 - h_q(\delta) - \varepsilon$ have relative distance $\delta$. So the bound is a statement about typical codes, and it is the benchmark for explicit constructions. Explicit binary families such as [concatenated codes](/concatenated-codes/) reach only lower curves (the Zyablov bound).

**Decoding.** A code at the GV bound with relative distance $\delta$ can correct $\delta n/2$ errors in principle. Decoding a random linear code is hard in general, which is why the GV bound for random codes also appears in code-based cryptography as the expected distance of a random code.

## Tightness

**Binary codes.** Whether $1 - h(\delta)$ is the true asymptotic rate of the best binary codes is a major open problem. The best upper bounds, from the [linear programming bound](/delsarte-lp-bound/), are well above it. For finite $n$, Jiang and Vardy (2004) improved the Gilbert bound for binary codes by a factor of order $n$, with a graph-theoretic version of the greedy argument. That gain does not change the asymptotic rate.

**Large alphabets.** For $q$ a square and $q \ge 49$, Tsfasman, Vladut and Zink (1982) built algebraic-geometry codes above the GV line in an interval of $\delta$. So the GV bound is not the true answer for those alphabets.

**Gilbert versus Varshamov.** The two bounds have the same asymptotic form. For finite lengths the Varshamov bound is never smaller, by the Pascal identity in the proof, and it also gives a linear code.

## History

Gilbert (1952) proved the bound for binary codes by the covering argument, in a study of signal sets. Varshamov (1957) gave the linear version with the parity-check matrix construction. The asymptotic form became the standard benchmark of coding theory, and the improvement over it for $q \ge 49$ by Tsfasman, Vladut and Zink (1982) was a surprise. For binary codes it has not been improved in rate.

## References
