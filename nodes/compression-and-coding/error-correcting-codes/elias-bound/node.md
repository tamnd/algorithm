---
tag: BBQKPZ
kind: theorem
slug: elias-bound
name: Elias bound
aliases:
- Elias-Bassalygo bound
- Bassalygo-Elias bound
area: compression-and-coding/error-correcting-codes
level: advanced
summary: "Averaging codewords over Hamming balls of the Johnson radius gives R <= 1 - h_q(J_q(delta)), below both the Hamming and the Plotkin bounds."
prereqs: [hamming-bound, plotkin-bound, binary-entropy-function]
see_also: [list-decoding, gilbert-varshamov-bound, delsarte-lp-bound, singleton-bound, griesmer-bound, golay-code]
sources:
  - paper: doi:10.1016/s0019-9958(67)91200-4
    title: C. E. Shannon, R. G. Gallager and E. R. Berlekamp, Lower bounds to error probability for coding on discrete memoryless channels II, Information and Control 10(5), 1967
    locator: pp. 522 to 552 (the minimum distance bound that the authors credit to Elias)
  - paper: "L. A. Bassalygo, New upper bounds for error-correcting codes, Problemy Peredachi Informatsii 1(4), 1965"
    locator: the bound obtained by counting codewords in a Hamming ball
  - paper: doi:10.1109/tit.1962.1057714
    title: S. M. Johnson, A new upper bound for error-correcting codes, IRE Transactions on Information Theory 8(3), 1962
    locator: pp. 203 to 207 (bounds on codes of constant weight, the source of the Johnson radius)
  - book: isbn:9780521845045
    title: Ron M. Roth, Introduction to Coding Theory, Cambridge University Press, 2006
    locator: Section 4.5 (asymptotic bounds, including the Elias bound)
  - paper: doi:10.1109/TIT.1977.1055688
    title: R. J. McEliece, E. R. Rodemich, H. Rumsey and L. R. Welch, New upper bounds on the rate of a code via the Delsarte-MacWilliams inequalities, IEEE Transactions on Information Theory 23(2), 1977
    locator: pp. 157 to 166 (the first linear programming bound, which improves on the Elias bound for most delta)
  - url: https://aeb.win.tue.nl/codes/binary-1.html
    title: A. E. Brouwer, Table of general binary codes
    locator: the values of A(n, d) used to check the bound
---

The Elias bound, also called the Elias-Bassalygo bound, is an upper bound on the size of a code that improves on both the [Hamming bound](/hamming-bound/) and the [Plotkin bound](/plotkin-bound/) for every relative distance $0 < \delta < 1 - 1/q$. It counts the codewords inside a Hamming ball of a well chosen radius. Some ball holds many codewords on average, but a ball smaller than the Johnson radius can hold only a few words that are pairwise far apart, by the Plotkin argument. In rates it gives $R \le 1 - h_q(J_q(\delta))$, where $J_q(\delta)$ is the Johnson radius. It holds for all codes, linear or not.

## Statement

Notation. $A_q(n, d)$ is the largest size of a code of length $n$ over $q$ symbols with minimum distance at least $d$, linear or not. $\theta = 1 - 1/q$. $V_q(n, r)$ is the number of words in a Hamming ball of radius $r$. $h_q$ is the $q$-ary entropy function, as in the [Gilbert-Varshamov bound](/gilbert-varshamov-bound/), and $h = h_2$.

**Lemma (codewords in a ball).** Let $C$ have minimum distance $d$, and let $r \le \theta n$ be such that $r^2 - 2\theta n r + \theta n d > 0$. Then every Hamming ball of radius $r$ contains at most

$$\frac{\theta n d}{r^2 - 2\theta n r + \theta n d}$$

words of $C$.

**Theorem (finite form, all codes).** For every $r$ as in the lemma,

$$A_q(n, d) \le \frac{\theta n d}{r^2 - 2\theta n r + \theta n d} \cdot \frac{q^n}{V_q(n, r)} .$$

**Johnson radius.** For $0 \le \delta \le \theta$ let

$$J_q(\delta) = \theta \left(1 - \sqrt{1 - \frac{\delta}{\theta}}\right),$$

the smaller root of $x^2 - 2\theta x + \theta\delta = 0$. For binary codes $J_2(\delta) = \tfrac12 (1 - \sqrt{1 - 2\delta})$. The condition of the lemma, divided by $n^2$, reads $x^2 - 2\theta x + \theta\delta > 0$ with $x = r/n$, which holds for $x < J_q(\delta)$.

**Asymptotic form.** For every family of codes over $q$ symbols with relative distance $\delta \le \theta$,

$$R \le 1 - h_q(J_q(\delta)) + o(1).$$

## In plain words

Draw a ball of some radius around every possible word. Each codeword lies in as many balls as a ball has words, so on average a ball holds the number of codewords times the ball size, divided by the number of all words. Some ball holds at least that many. But if the ball is small enough, its codewords are close to the centre and also far from each other, and the Plotkin counting argument says only a few such words can exist. Putting the two facts together limits the number of codewords. The best ball size is the Johnson radius.

## Proof

*Lemma.* Translate the code so that the ball is centred at the zero word; this keeps all distances. Let $y_1, \dots, y_K$ be the codewords in the ball, so each has weight at most $r$, and let $S = \sum_i \mathrm{wt}(y_i) \le K r$. Let $T$ be the sum of $d(y_i, y_j)$ over ordered pairs $i \ne j$. Then $T \ge K(K - 1) d$.

Count $T$ by positions. In position $j$, let $s_j$ be the number of words with a nonzero symbol, and $k_a$ the number with symbol $a \ne 0$. The ordered pairs that differ there number $K^2 - (K - s_j)^2 - \sum_{a \ne 0} k_a^2$. By the Cauchy-Schwarz inequality $\sum_{a \ne 0} k_a^2 \ge s_j^2/(q - 1)$, so position $j$ adds at most $2K s_j - s_j^2/\theta$. Summing over $j$ and using $\sum_j s_j^2 \ge S^2/n$,

$$T \le 2KS - \frac{S^2}{\theta n} .$$

The right side increases in $S$ for $S \le \theta n K$, and $S \le Kr \le K\theta n$, so $T \le 2K^2 r - K^2 r^2/(\theta n)$. With $T \ge K(K - 1)d$ and division by $K$,

$$(K - 1) d \le K \left(2r - \frac{r^2}{\theta n}\right), \qquad \text{so} \qquad K\,(r^2 - 2\theta n r + \theta n d) \le \theta n d .$$

When the bracket is positive this gives the lemma.

*Theorem.* Let $C$ have $M$ words. Each codeword lies in exactly $V_q(n, r)$ of the $q^n$ balls of radius $r$, so the balls hold $M V_q(n, r)$ codewords in total, and some ball holds at least $M V_q(n, r)/q^n$. By the lemma this is at most $\theta n d/(r^2 - 2\theta n r + \theta n d)$, and the bound follows.

*Asymptotic form.* Fix $\varepsilon > 0$ and take $r = \lfloor (J_q(\delta) - \varepsilon) n \rfloor$. Then $r^2 - 2\theta n r + \theta n d \ge c\, n^2$ for some $c > 0$ that depends on $\varepsilon$ and $\delta$, so the first factor is at most $\theta \delta / c$, a constant. The ball estimate $V_q(n, r) \ge q^{n h_q(r/n)}/(n + 1)$ (see the [binary entropy function](/binary-entropy-function/) for $q = 2$; the $q$-ary case is the same) gives $\log_q A_q(n, d) \le n - n h_q(J_q(\delta) - \varepsilon) + O(\log n)$. Let $\varepsilon \to 0$ and use the continuity of $h_q$. $\blacksquare$

## Consequences

**Comparison of the asymptotic bounds.** For binary codes, the Elias bound is below the Hamming bound $1 - h(\delta/2)$, because $J_2(\delta) > \delta/2$, and below the Plotkin line $1 - 2\delta$. The table also shows the first MRRW bound $h(1/2 - \sqrt{\delta(1 - \delta)})$ from the [linear programming bound](/delsarte-lp-bound/), and the [Gilbert-Varshamov](/gilbert-varshamov-bound/) lower bound.

| $\delta$ | $J_2(\delta)$ | Hamming | Plotkin | Elias | MRRW (first) | GV |
|---|---|---|---|---|---|---|
| 0.05 | 0.0257 | 0.8313 | 0.9 | 0.8279 | 0.8582 | 0.7136 |
| 0.10 | 0.0528 | 0.7136 | 0.8 | 0.7019 | 0.7219 | 0.5310 |
| 0.20 | 0.1127 | 0.5310 | 0.6 | 0.4920 | 0.4690 | 0.2781 |
| 0.30 | 0.1838 | 0.3902 | 0.4 | 0.3117 | 0.2502 | 0.1187 |
| 0.40 | 0.2764 | 0.2781 | 0.2 | 0.1495 | 0.0815 | 0.0290 |
| 0.45 | 0.3419 | 0.2308 | 0.1 | 0.0734 | 0.0253 | 0.0072 |

The Elias bound is the best of these for small $\delta$. The first MRRW bound overtakes it near $\delta = 0.15$.

**Finite lengths.** For short codes the finite form is often weaker than the Hamming bound. It gains as $n$ and $d/n$ grow. The tests compute these values with exact fractions, minimizing over the integer radius $r$:

| $n$ | $d$ | Hamming | Elias |
|---|---|---|---|
| 12 | 4 | 315 | 311 |
| 23 | 7 | 4096 | 13763 |
| 24 | 10 | 1295 | 882 |
| 64 | 16 | 26184380591 | 17004939455 |
| 100 | 30 | 24141609256495 | 2033245478054 |

At $(23, 7)$ the Hamming bound is met by the [Golay code](/golay-code/), and the Elias bound is far from it.

**Johnson bound for list decoding.** The lemma says that a ball of radius $(J_q(\delta) - \varepsilon) n$ holds at most a constant number of codewords, where the constant depends only on $\varepsilon$ and $\delta$. This is the Johnson bound of [list decoding](/list-decoding/): every code with relative distance $\delta$ can be list decoded up to a fraction just below $J_q(\delta)$ of errors with lists of bounded size. As $q$ grows, $J_q(\delta)$ tends to $1 - \sqrt{1 - \delta}$, the radius up to which the Guruswami-Sudan algorithm decodes Reed-Solomon codes.

## Tightness

The bound is not tight. The linear programming bound of McEliece, Rodemich, Rumsey and Welch (1977) is lower for $\delta$ above about 0.15, and a second MRRW bound improves further. The gap between the best upper bounds and the GV lower bound remains open for binary codes. At the end points the bound is exact in rate: at $\delta = 0$ both sides give rate 1, and at $\delta = \theta$ the rate is 0, as the Plotkin bound also shows.
## History

Elias found the bound around 1960 but did not publish it. Shannon, Gallager and Berlekamp (1967) printed it with credit to Elias. Bassalygo (1965) published the same bound independently, which is why it carries both names. The count of codewords in a ball comes from Johnson's work on codes of constant weight (1962). The bound was the best known upper bound for small $\delta$ until the linear programming bounds of 1977.

## References
