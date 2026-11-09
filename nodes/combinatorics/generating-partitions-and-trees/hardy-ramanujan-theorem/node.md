---
tag: 2TARGZ
kind: theorem
slug: hardy-ramanujan-theorem
name: Hardy-Ramanujan asymptotic formula
aliases:
- Asymptotics of p(n)
- Hardy-Ramanujan formula for partitions
area: combinatorics/generating-partitions-and-trees
level: advanced
summary: The partition function satisfies p(n) ~ exp(pi sqrt(2n/3)) / (4n sqrt(3)); elementary bounds give log p(n) = Theta(sqrt n).
prereqs: [integer-partition-function, asymptotic-equivalence]
see_also: [rademacher-formula, hardy-ramanujan-asymptotics, integer-partitions, integer-partition-generation, euler-pentagonal-recurrence, stirling-approximation, generating-functions]
sources:
  - paper: doi:10.1112/plms/s2-17.1.75
    title: G. H. Hardy and S. Ramanujan, Asymptotic formulae in combinatory analysis, Proceedings of the London Mathematical Society (2) 17 (1918), 75-115
    locator: the whole paper (the asymptotic series for p(n) by the circle method)
  - book: isbn:9780521637664
    title: George E. Andrews, The Theory of Partitions, Cambridge University Press, 1998 (first published 1976)
    locator: Chapter 5, The Hardy-Ramanujan-Rademacher expansion of p(n), pages 68 to 87
  - book: isbn:9780387971278
    title: Tom M. Apostol, Modular Functions and Dirichlet Series in Number Theory, second edition, Springer, 1990
    locator: Chapter 3, The Dedekind eta function (the transformation formula), and Chapter 5, Rademacher's series for the partition function
  - book: isbn:9780521898065
    title: Philippe Flajolet and Robert Sedgewick, Analytic Combinatorics, Cambridge University Press, 2009
    locator: Chapter VIII, Saddle-point asymptotics (the saddle point estimate for integer partitions)
  - paper: doi:10.1307/mmj/1028998729
    title: D. J. Newman, A simplified proof of the partition formula, Michigan Mathematical Journal 9 (1962), 283-287
    locator: the whole paper
  - paper: doi:10.2307/1968802
    title: Paul Erdős, On an elementary proof of some asymptotic formulas in the theory of partitions, Annals of Mathematics 43 (1942), 437-450
    locator: the whole paper (p(n) ~ (a/n) exp(pi sqrt(2n/3)) by elementary means)
---

The Hardy-Ramanujan theorem gives the growth of the [partition function](/integer-partition-function/): $p(n) \sim \frac{1}{4n\sqrt 3} e^{\pi\sqrt{2n/3}}$ as $n \to \infty$. So the number of [partitions](/integer-partitions/) of $n$ grows faster than every polynomial and slower than every exponential $c^n$ with $c > 1$, and it has about $2.565\sqrt n$ nats, which is $\Theta(\sqrt n)$ bits. This page proves an upper and a lower bound of the form $e^{\Theta(\sqrt n)}$ with elementary tools, and gives the analytic proof of the exact constant as a cited sketch.

## Statement

Let $p(n)$ be the number of partitions of $n$, and let $C = \pi\sqrt{2/3} \approx 2.5651$.

**Theorem** (Hardy and Ramanujan, 1918). As $n \to \infty$,

$$p(n) \sim \frac{1}{4n\sqrt 3}\, e^{C\sqrt n}.$$

**Proposition** (elementary bounds). For every $n \ge 1$,

$$\frac{e^{2\sqrt n - 4}}{n} \le p(n) < e^{C\sqrt n}.$$

So $\ln p(n) = \Theta(\sqrt n)$ by the bounds alone, and $\ln p(n) = C\sqrt n - \ln n + O(1)$ by the theorem.

## In plain words

Count the ways to write a number as a sum of smaller numbers when the order does not matter. The count grows very fast, but not as fast as doubling at each step. The theorem gives a simple formula that comes closer and closer to the true count, in the sense that the ratio of the two goes to one. For one hundred the formula is about five percent too large, and for one thousand it is under two percent too large.

The number of digits of the count grows like the square root of the number. So listing all the partitions of a few hundred is impossible, but their count is a number that fits on one line.

## Proof

Write $P(x) = \sum_{n \ge 0} p(n) x^n = \prod_{m \ge 1} (1 - x^m)^{-1}$, which converges for $0 \le x < 1$. All coefficients are non-negative.

**Upper bound.** Fix $n \ge 1$ and $0 < x < 1$. Since $P(x) \ge p(0) + p(n) x^n > p(n) x^n$, we have $\ln p(n) < \ln P(x) - n \ln x$. Next,

$$\ln P(x) = \sum_{m \ge 1} -\ln(1 - x^m) = \sum_{m \ge 1} \sum_{j \ge 1} \frac{x^{mj}}{j} = \sum_{j \ge 1} \frac{1}{j} \cdot \frac{x^j}{1 - x^j},$$

where the order of the sums may change because all terms are positive. Since $1 - x^j = (1 - x)(1 + x + \cdots + x^{j-1}) \ge (1 - x)\, j\, x^{j-1}$, each term satisfies $\frac{x^j}{1 - x^j} \le \frac{x}{(1 - x)\, j}$. So

$$\ln P(x) \le \frac{x}{1 - x} \sum_{j \ge 1} \frac{1}{j^2} = \frac{\pi^2}{6} \cdot \frac{x}{1 - x}.$$

Put $x = e^{-t}$ with $t > 0$. Then $\frac{x}{1 - x} = \frac{1}{e^t - 1} < \frac{1}{t}$, so $\ln p(n) < \frac{\pi^2}{6t} + nt$. Choose $t = \pi/\sqrt{6n}$. Both terms are $\pi\sqrt{n/6}$, and the sum is $2\pi\sqrt{n/6} = C\sqrt n$. $\square$

**Lower bound.** Fix $n \ge 1$ and let $k = \lfloor \sqrt n \rfloor \ge 1$.

1. *Lattice points give partitions.* Each tuple $(a_2, \ldots, a_k)$ of non-negative integers with $\sum_{i=2}^{k} i\, a_i \le n$ gives the partition $k^{a_k} \cdots 2^{a_2}\, 1^{r}$ with $r = n - \sum_i i\, a_i$ ones. Different tuples give different partitions. So $p(n)$ is at least the number $L$ of such tuples.
2. *Lattice points against volume.* Let $S = \{x \in \mathbb{R}^{k-1} : x_i \ge 0,\ \sum_{i=2}^{k} i\, x_i \le n\}$. For $x \in S$, the point $\lfloor x \rfloor$ (floor in each coordinate) is one of the tuples in step 1. So $S$ is covered by the unit cubes $a + [0, 1)^{k-1}$ over those tuples $a$, and $L \ge \operatorname{vol}(S)$.
3. *The volume.* The substitution $y_i = i\, x_i / n$ maps $S$ onto the standard simplex $\{y_i \ge 0, \sum y_i \le 1\}$ of volume $1/(k-1)!$, with Jacobian $\prod_{i=2}^{k} (n/i) = n^{k-1}/k!$. So $\operatorname{vol}(S) = \frac{n^{k-1}}{(k-1)!\, k!} = \frac{k}{n} \cdot \frac{n^k}{(k!)^2}$.
4. *A bound on $k!$.* The function $\ln$ is concave, so on each $[j, j+1]$ its chord lies below it, and $\int_1^k \ln x\, dx \ge \sum_{j=1}^{k-1} \frac{\ln j + \ln(j+1)}{2} = \ln k! - \frac12 \ln k$. The integral is $k \ln k - k + 1$, so $(k!)^2 \le k^{2k}\, e^{-2k}\, e^2\, k$.
5. *Combine.* With steps 3 and 4, $\operatorname{vol}(S) \ge \frac{k}{n} \cdot \big(\frac{n}{k^2}\big)^{k} \cdot \frac{e^{2k-2}}{k} \ge \frac{e^{2k-2}}{n}$, since $k^2 \le n$. Finally $k > \sqrt n - 1$, so $2k - 2 > 2\sqrt n - 4$.

Hence $p(n) \ge L \ge \operatorname{vol}(S) > e^{2\sqrt n - 4}/n$. $\square$

**The asymptotic formula (cited sketch).** The full proof needs complex analysis. We give the steps of the saddle point proof; Andrews (Chapter 5) and Apostol (Chapter 5) prove the stronger [Rademacher formula](/rademacher-formula/), Newman (1962) gives a short direct proof, and Flajolet and Sedgewick (Chapter VIII) give the saddle point version.

1. *Cauchy's formula.* For $t > 0$, $p(n) = \frac{1}{2\pi} \int_{-\pi}^{\pi} P(e^{-\tau})\, e^{n\tau}\, d\theta$ with $\tau = t - i\theta$.
2. *The modular transformation.* The Dedekind eta function satisfies $\eta(-1/z) = \sqrt{-iz}\, \eta(z)$ (Apostol, Chapter 3). With $\eta(z) = e^{\pi i z/12} \prod_m (1 - e^{2\pi i m z})$ and $z = i\tau/(2\pi)$, this becomes, for $\operatorname{Re} \tau > 0$,
   $$P(e^{-\tau}) = \sqrt{\frac{\tau}{2\pi}}\; e^{\pi^2/(6\tau) - \tau/24}\; P(e^{-4\pi^2/\tau}).$$
   As $\tau \to 0$ in a sector around the positive axis, the last factor tends to $1$.
3. *The saddle point.* The exponent $f(\tau) = \frac{\pi^2}{6\tau} + n\tau$ has its minimum on the real axis at $t_0 = \pi/\sqrt{6n}$, with $f(t_0) = C\sqrt n$ and $f''(t_0) = \frac{\pi^2}{3 t_0^3}$. Take $t = t_0$.
4. *The main arc.* For $|\theta| \le t_0^{3/2 - \varepsilon}$, the integrand is $\sqrt{t_0/(2\pi)}\, e^{f(t_0) - f''(t_0)\theta^2/2}\,(1 + o(1))$, and the Gaussian integral gives
   $$\frac{1}{2\pi} \sqrt{\frac{t_0}{2\pi}}\, e^{C\sqrt n} \sqrt{\frac{2\pi}{f''(t_0)}} = \frac{1}{2\pi} \sqrt{\frac{3 t_0^4}{\pi^2}}\, e^{C\sqrt n} = \frac{\sqrt 3\, t_0^2}{2\pi^2}\, e^{C\sqrt n} = \frac{e^{C\sqrt n}}{4\sqrt 3\, n}.$$
5. *The rest of the circle.* For larger $|\theta|$, $|P(e^{-\tau})|$ is smaller than $P(e^{-t_0})$ by a factor $e^{-c\, n^{\delta}}$ for some $c, \delta > 0$, so this part is negligible against the main term.

Steps 4 and 5 need careful error bounds, which the cited sources give. $\blacksquare$

## Consequences

- **Bit size.** $\log_2 p(n) = \frac{C}{\ln 2}\sqrt n - \log_2 n + O(1)$, about $3.70\sqrt n$. For $n = 1000$, $\log_2 H(n) \approx 104.3$ with $H(n)$ as in the table below, and $p(1000)$ has $105$ bits. Exact arithmetic on $p(n)$ costs big integer operations on $\Theta(\sqrt n)$ bits.
- **Feasibility of generation.** A constant amortized time generator such as [Algorithm P](/integer-partition-generation/) runs in $\Theta(p(n)) = e^{\Theta(\sqrt n)}$ time. Listing all partitions is feasible up to about $n = 100$, where $p(100) \approx 1.9 \times 10^8$, and not beyond a few hundred.
- **Ratios.** $p(n - 1)/p(n) \to 1$, since $\sqrt{n} - \sqrt{n - 1} \to 0$. For example $p(1000)/p(999) \approx 1.040$. So a fixed shift of $n$ changes $p(n)$ by a factor close to $1$. The analysis of Algorithm P uses this: its fast branch runs $p(n - 2)$ times out of $p(n)$ steps.
- **Comparison with compositions.** There are $2^{n-1}$ [compositions](/integer-compositions/) of $n$, so the fraction of compositions that are sorted, $p(n)/2^{n-1}$, tends to $0$ exponentially fast.
- **The polynomial factor.** The upper bound $e^{C\sqrt n}$ is larger than $p(n)$ by a factor $\sim 4\sqrt 3\, n$. For $n = 100$ it is $1.38 \times 10^{11}$ against $p(100) = 1.91 \times 10^8$.

## Tightness

**The constant in the exponent.** The constant $C = \pi\sqrt{2/3}$ in the upper bound cannot be lowered: if $p(n) < e^{C'\sqrt n}$ for all large $n$ with $C' < C$, then $p(n)\, 4\sqrt 3\, n\, e^{-C\sqrt n} \to 0$, against the theorem. The lower bound has the constant $2$ instead of $C$, and loses this much because it counts only partitions with parts at most $\sqrt n$.

**The error of the formula.** The relative error is not small for small $n$. Let $H(n) = \frac{e^{C\sqrt n}}{4\sqrt 3\, n}$.

| $n$ | $p(n)$ | $H(n)$ | $H(n)/p(n)$ |
| --- | --- | --- | --- |
| $10$ | $42$ | $48.10$ | $1.1453$ |
| $50$ | $204226$ | $2.1759 \times 10^{5}$ | $1.0654$ |
| $100$ | $190569292$ | $1.9928 \times 10^{8}$ | $1.0457$ |
| $200$ | $3972999029388$ | $4.1003 \times 10^{12}$ | $1.0320$ |
| $1000$ | $\approx 2.4061 \times 10^{31}$ | $2.4402 \times 10^{31}$ | $1.0142$ |

In this table $(H(n)/p(n) - 1)\sqrt n$ stays between $0.44$ and $0.47$, so the relative error decreases like $1/\sqrt n$. The formula never gives $p(n)$ exactly. The Hardy-Ramanujan series with more terms, and the convergent [Rademacher series](/rademacher-formula/), do.

**The elementary bounds.** Both bounds hold for $n = 1$ to $1000$, and both are far from $p(n)$: at $n = 100$ they give $8.9 \times 10^{4} \le p(100) < 1.4 \times 10^{11}$.

## History

Hardy and Ramanujan published the formula in 1918, as the first term of an asymptotic series that they found with the circle method. With a fixed number of terms of order $\sqrt n$, their series gives $p(n)$ with an error that tends to $0$, so rounding gives the exact value for large $n$; they checked this against MacMahon's table up to $p(200)$. Rademacher turned the series into a convergent one in 1937. Erdős in 1942 proved $p(n) \sim \frac{a}{n} e^{C\sqrt n}$ by elementary means, with a constant $a$ that his method did not give; the theorem shows $a = 1/(4\sqrt 3)$. Newman gave a short analytic proof in 1962.

## References
