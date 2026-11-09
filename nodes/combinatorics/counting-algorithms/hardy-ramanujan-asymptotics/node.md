---
tag: 0J5YQ1
kind: theorem
slug: hardy-ramanujan-asymptotics
name: Hardy-Ramanujan asymptotic formula for partitions
aliases:
- partition asymptotics
- Hardy-Ramanujan-Rademacher formula
- asymptotic formula for p(n)
area: combinatorics/counting-algorithms
level: research
summary: Gives the asymptotic size of the partition function p(n).
prereqs: [integer-partition-counting, generating-functions]
see_also: [hardy-ramanujan-theorem, rademacher-formula, integer-partition-function, euler-pentagonal-recurrence, euler-pentagonal-number-theorem, integer-partition-counting, asymptotic-equivalence]
sources:
  - paper: doi:10.1112/plms/s2-17.1.75
    title: G. H. Hardy and S. Ramanujan, Asymptotic formulae in combinatory analysis, Proceedings of the London Mathematical Society (2) 17 (1918), 75-115
    locator: the whole paper (the asymptotic series for p(n) by the circle method)
  - book: isbn:9780521637664
    title: George E. Andrews, The Theory of Partitions, Cambridge University Press, 1998 (first published 1976)
    locator: Chapter 5, The Hardy-Ramanujan-Rademacher expansion of p(n)
  - book: isbn:9780387971278
    title: Tom M. Apostol, Modular Functions and Dirichlet Series in Number Theory, second edition, Springer, 1990
    locator: Chapter 5, Rademacher's series for the partition function
  - paper: doi:10.2307/1968802
    title: Paul Erdős, On an elementary proof of some asymptotic formulas in the theory of partitions, Annals of Mathematics 43 (1942), 437-450
    locator: the whole paper (p(n) ~ (a/n) exp(pi sqrt(2n/3)) by elementary means)
  - book: isbn:9780521898065
    title: Philippe Flajolet and Robert Sedgewick, Analytic Combinatorics, Cambridge University Press, 2009
    locator: Chapter VIII, Saddle-point asymptotics (integer partitions)
---

The Hardy-Ramanujan formula says that the number $p(n)$ of partitions of $n$ satisfies $p(n) \sim \frac{1}{4n\sqrt 3} e^{\pi\sqrt{2n/3}}$. So $p(n)$ grows faster than every polynomial and slower than every exponential $a^n$ with $a > 1$, and it has about $3.70\sqrt n$ bits. This size controls the cost of every exact partition counting algorithm: the [pentagonal recurrence](/euler-pentagonal-recurrence/) uses $\Theta(n^2)$ bit operations for the whole prefix, and the [Rademacher series](/rademacher-formula/) gets one value in time close to $\sqrt n$. This page proves the logarithmic form $\ln p(n) \sim \pi\sqrt{2n/3}$ with its exact constant from the generating function alone, and cites the full formula.

## Statement

**Notation.** $n \ge 1$ is an integer, $p(n)$ is the number of partitions of $n$, $c = \pi\sqrt{2/3} \approx 2.5651$, and $f(n) \sim g(n)$ means $f(n)/g(n) \to 1$ as $n \to \infty$ ([asymptotic equivalence](/asymptotic-equivalence/)).

**Theorem 1 (Hardy and Ramanujan, 1918).** As $n \to \infty$,

$$p(n) \sim \frac{1}{4n\sqrt 3}\, e^{c\sqrt n}.$$

**Theorem 2 (the exponent).** For every $n \ge 1$, $p(n) \le e^{c\sqrt n}$. Moreover $\ln p(n) \sim c\sqrt n$.

Theorem 2 is the part of Theorem 1 that fixes the exponential rate. It is proved in full below. Theorem 1 needs the modular transformation of the Dedekind eta function and the circle method, and its proof is in Andrews, Chapter 5, and Apostol, Chapter 5. Rademacher later turned the Hardy-Ramanujan asymptotic series into a convergent series whose rounded sum is exactly $p(n)$; see the [Rademacher formula](/rademacher-formula/).

## In plain words

The number of ways to split a whole number into a sum of parts, with no order on the parts, grows very fast. This theorem gives a simple formula that comes closer and closer to it, in the sense that their ratio tends to one. The count grows faster than any fixed power of the number, but slower than doubling at each step. Its number of digits grows like the square root of the number. So the count for one thousand has only 32 digits, even though listing all of those splits is far out of reach.

## Proof

We prove Theorem 2. Let $P(x) = \sum_{n \ge 0} p(n) x^n = \prod_{k \ge 1} (1 - x^k)^{-1}$ for $0 < x < 1$. All terms are positive, and the product converges because $\sum_k x^k < \infty$. Put $A = \pi^2/6 = \sum_{m \ge 1} 1/m^2$, so that $c = 2\sqrt A$. We write $x = e^{-t}$ with $t > 0$.

**Step 1 (the logarithm of the generating function).** Expanding $-\ln(1 - y) = \sum_{m \ge 1} y^m / m$ and summing the geometric series in $k$,

$$\ln P(x) = \sum_{k \ge 1} \sum_{m \ge 1} \frac{x^{km}}{m} = \sum_{m \ge 1} \frac{1}{m} \cdot \frac{x^m}{1 - x^m}.$$

All terms are non-negative, so the order of summation can change.

**Step 2 (upper bound for $P$).** Since $1 - x^m = (1 - x)(1 + x + \cdots + x^{m-1}) \ge (1 - x)\, m\, x^{m-1}$, each term satisfies $\frac{x^m}{1 - x^m} \le \frac{x}{m(1 - x)}$. So $\ln P(x) \le \frac{x}{1 - x} \sum_m \frac{1}{m^2} = \frac{A}{e^t - 1} \le \frac{A}{t}$.

**Step 3 (the upper bound for $p(n)$).** Every term of $P(x)$ is at most the sum, so $p(n)\, e^{-tn} \le P(e^{-t}) \le e^{A/t}$, that is, $\ln p(n) \le A/t + nt$ for every $t > 0$. Take $t = \sqrt{A/n}$: $\ln p(n) \le 2\sqrt{An} = c\sqrt n$. This proves the first claim of Theorem 2, and also $\limsup \ln p(n) / (c\sqrt n) \le 1$.

**Step 4 (lower bound for $P$).** Since $1 - x^m = (1 - x)(1 + \cdots + x^{m-1}) \le m(1 - x)$, each term satisfies $\frac{x^m}{1 - x^m} \ge \frac{x^m}{m(1 - x)}$. Also $1 - e^{-t} \le t$. So

$$\ln P(e^{-t}) \ge \frac{1}{t} \sum_{m \ge 1} \frac{e^{-tm}}{m^2} = \frac{A - \varepsilon(t)}{t}, \qquad \varepsilon(t) = \sum_{m \ge 1} \frac{1 - e^{-tm}}{m^2}.$$

By monotone convergence, $\varepsilon(t) \to 0$ as $t \to 0^+$.

**Step 5 (where the mass of $P$ lies).** Let $h(s) = c\sqrt s - ts$ for real $s \ge 0$. By Step 3, $p(n) e^{-tn} \le e^{h(n)}$. Write $\sqrt s = (1 + u)\frac{c}{2t}$ with $u \ge -1$. Then

$$h(s) = \frac{c^2}{4t}\bigl(2(1 + u) - (1 + u)^2\bigr) = \frac{A}{t}(1 - u^2).$$

Fix $0 < \eta < 1$ and put $s_0 = c^2/(4t^2) = A/t^2$, $M = (1 - \eta)^2 s_0$ and $N = (1 + \eta)^2 s_0$. For $s \le M$ and for $s \ge N$ we have $|u| \ge \eta$, so $h(s) \le \frac{A}{t}(1 - \eta^2)$.

- *Head.* $\sum_{n \le M} p(n) e^{-tn} \le (M + 1)\, e^{A(1 - \eta^2)/t}$.
- *Tail.* $h$ is concave, so for $n \ge N$, $h(n) \le h(N) + h'(N)(n - N)$, where $h'(N) = \frac{c}{2\sqrt N} - t = -\frac{\eta t}{1 + \eta}$. Summing the geometric series, $\sum_{n \ge N} p(n) e^{-tn} \le e^{h(N)} \bigl(1 + \frac{1 + \eta}{\eta t}\bigr) \le \bigl(1 + \frac{2}{\eta t}\bigr) e^{A(1 - \eta^2)/t}$, using $\frac{1}{1 - e^{-a}} \le 1 + \frac{1}{a}$ for $a > 0$.
- *Middle.* $p$ is non-decreasing, because adding a part 1 maps the partitions of $n$ one to one into those of $n + 1$. So for $M < n < N$, $p(n) \le p(\lceil N \rceil)$, and $\sum_{M < n < N} p(n) e^{-tn} \le N\, p(\lceil N \rceil)\, e^{-tM}$.

**Step 6 (the lower bound for $p(n)$).** By Step 4, $P(e^{-t}) \ge e^{(A - \varepsilon(t))/t}$. The head and the tail together are at most $(M + 2 + \frac{2}{\eta t})\, e^{A(1 - \eta^2)/t}$. As $t \to 0^+$, $\varepsilon(t) < A\eta^2/2$ eventually, and $M + 2 + \frac{2}{\eta t}$ grows only like a power of $1/t$, so the head and the tail are at most $\frac12 P(e^{-t})$ for all small $t$. Then the middle is at least $\frac12 P(e^{-t})$:

$$N\, p(\lceil N \rceil)\, e^{-tM} \ge \tfrac12 e^{(A - \varepsilon(t))/t}.$$

Now take a large integer $N$ and choose $t = (1 + \eta)\sqrt{A/N}$, so that $N = (1 + \eta)^2 A/t^2$ is exactly the $N$ of Step 5 and $M = (1 - \eta)^2 A / t^2$. Then $tM = (1 - \eta)^2 A/t$ and $A/t = \frac{\sqrt{AN}}{1 + \eta} = \frac{c\sqrt N}{2(1 + \eta)}$, so

$$\ln p(N) \ge \frac{A}{t}\bigl(1 + (1 - \eta)^2\bigr) - \frac{\varepsilon(t)}{t} - \ln(2N) = c\sqrt N \cdot \frac{1 + (1 - \eta)^2}{2(1 + \eta)} - o(\sqrt N).$$

Since $t \to 0$ as $N \to \infty$, $\varepsilon(t)/t = o(1/t) = o(\sqrt N)$. So $\liminf \ln p(N)/(c\sqrt N) \ge \frac{1 + (1 - \eta)^2}{2(1 + \eta)}$ for every $\eta \in (0, 1)$. The right side tends to 1 as $\eta \to 0$. With Step 3, $\ln p(n) \sim c\sqrt n$. $\blacksquare$

The proof is the saddle point idea in its simplest form: $P(e^{-t})$ is dominated by the terms near $n = A/t^2$, so a lower bound on $P$ forces a lower bound on $p$ near that $n$.

## Consequences

- **Size of the answer.** $p(n)$ has $\frac{c}{\ln 2}\sqrt n + O(\log n) \approx 3.70\sqrt n$ bits. Any exact algorithm for $p(n)$ must spend $\Omega(\sqrt n)$ time to write it, and the prefix $p(0), \ldots, p(n)$ has $\Theta(n^{3/2})$ bits.
- **Cost of the pentagonal recurrence.** Each of the $\Theta(n^{3/2})$ additions of [Euler's pentagonal recurrence](/euler-pentagonal-recurrence/) acts on numbers of $O(\sqrt n)$ bits, so the exact prefix costs $\Theta(n^2)$ bit operations.
- **Listing is hopeless.** Any algorithm that lists all partitions of $n$ takes time at least $p(n) = e^{(c - o(1))\sqrt n}$, for example more than $10^{31}$ steps for $n = 1000$.
- **Superpolynomial but subexponential.** For each $k$, $p(n) > n^k$ for large $n$, and for each $a > 1$, $p(n) < a^n$ for large $n$.
- **Typical partitions.** The proof shows that under the weights $x^n$ with $x = e^{-t}$, almost all the mass of $P(x)$ sits at sizes $n$ near $A/t^2$. This is the basis of the Boltzmann model for random partitions.

## Tightness

- **The constant $c$ cannot be improved.** The bound $p(n) \le e^{c\sqrt n}$ of Theorem 2 has the right exponent: by Theorem 2 itself, $\ln p(n)/(c\sqrt n) \to 1$. The values of this ratio are about $0.461$, $0.743$, $0.891$ and $0.957$ for $n = 10$, $100$, $1000$ and $10000$. The convergence is slow because of the factor $\frac{1}{4n\sqrt 3}$ in Theorem 1.
- **The full formula is sharp in ratio.** The ratio of $p(n)$ to the right side of Theorem 1 is about $0.873$, $0.956$, $0.986$ and $0.996$ for $n = 10$, $100$, $1000$ and $10000$. The relative error is of order $1/\sqrt n$, and the further terms of the Hardy-Ramanujan series remove it.
- **The upper bound is off by a polynomial factor.** By Theorem 1, $e^{c\sqrt n}/p(n) \sim 4\sqrt 3\, n$, so the bound of Step 3 is never tight, but it is loose only by a factor linear in $n$.
- **Elementary methods reach the exponent, not the constant factor.** Erdős proved $p(n) \sim \frac{a}{n} e^{c\sqrt n}$ by elementary means, but the value $a = \frac{1}{4\sqrt 3}$ came from the analytic method.

## History

MacMahon computed $p(n)$ for $n \le 200$ with Euler's recurrence. Hardy and Ramanujan, in their 1918 paper, introduced the circle method to find an asymptotic series for $p(n)$ and found that a few of its terms gave $p(200) = 3972999029388$ exactly after rounding. Rademacher found a convergent form of the series in 1937. Erdős gave an elementary proof of the order $\frac{a}{n} e^{c\sqrt n}$ in 1942, and Newman gave a short analytic proof of Theorem 1 in 1962.

## References
