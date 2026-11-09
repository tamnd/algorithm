---
tag: 9EJ04Z
kind: theorem
slug: rademacher-formula
name: Rademacher's exact formula
aliases:
- Rademacher series for p(n)
- Hardy-Ramanujan-Rademacher formula
area: combinatorics/generating-partitions-and-trees
level: research
summary: A convergent series of Kloosterman-type sums times Bessel-type terms that gives p(n) exactly; its first term is the Hardy-Ramanujan formula.
prereqs: [hardy-ramanujan-theorem, integer-partition-function]
see_also: [integer-partitions, hardy-ramanujan-asymptotics, euler-pentagonal-recurrence, integer-partition-counting, big-integer, asymptotic-equivalence]
sources:
  - paper: doi:10.1073/pnas.23.2.78
    title: Hans Rademacher, A convergent series for the partition function p(n), Proceedings of the National Academy of Sciences 23 (1937), 78-84
    locator: the whole paper (announcement of the convergent series)
  - paper: doi:10.1112/plms/s2-43.4.241
    title: Hans Rademacher, On the partition function p(n), Proceedings of the London Mathematical Society (2) 43 (1937), 241-254
    locator: the whole paper (the proof of the convergent series)
  - book: isbn:9780521637664
    title: George E. Andrews, The Theory of Partitions, Cambridge University Press, 1998 (first published 1976)
    locator: Chapter 5, The Hardy-Ramanujan-Rademacher expansion of p(n), pages 68 to 87
  - book: isbn:9780387971278
    title: Tom M. Apostol, Modular Functions and Dirichlet Series in Number Theory, second edition, Springer, 1990
    locator: Chapter 3, The Dedekind eta function, and Chapter 5, Rademacher's series for the partition function
  - paper: doi:10.1090/s0002-9947-1939-0000410-9
    title: D. H. Lehmer, On the remainders and convergence of the series for the partition function, Transactions of the American Mathematical Society 46 (1939), 362-373
    locator: the whole paper (explicit bounds on the remainder after N terms)
  - paper: doi:10.1112/S1461157012001088
    title: Fredrik Johansson, Efficient implementation of the Hardy-Ramanujan-Rademacher formula, LMS Journal of Computation and Mathematics 15 (2012), 341-359
    locator: the whole paper (error bounds, the evaluation of A_k(n), and the cost of computing p(n))
---

Rademacher's formula writes the [partition function](/integer-partition-function/) $p(n)$ as an absolutely convergent infinite series. Each term is an exponential sum $A_k(n)$ times an explicit elementary function of $n$, and the first term alone is the [Hardy-Ramanujan](/hardy-ramanujan-theorem/) main term $\frac{1}{4n\sqrt 3} e^{\pi\sqrt{2n/3}}$ up to a factor $1 + O(n^{-1/2})$. With about $\sqrt n$ terms the partial sum is within $\frac12$ of $p(n)$, so rounding gives the exact value. This is the standard fast method to compute one large value of $p(n)$.

## Statement

**Notation.** For $x \in \mathbb{R}$ let $((x)) = x - \lfloor x \rfloor - \frac12$ if $x \notin \mathbb{Z}$ and $((x)) = 0$ if $x \in \mathbb{Z}$. For integers $k \ge 1$ and $h$ with $\gcd(h, k) = 1$, the Dedekind sum is

$$s(h, k) = \sum_{r=1}^{k-1} \Big(\Big(\frac{r}{k}\Big)\Big) \Big(\Big(\frac{h r}{k}\Big)\Big).$$

Put $\omega_{h,k} = e^{\pi i\, s(h, k)}$ and

$$A_k(n) = \sum_{\substack{0 \le h < k \\ \gcd(h, k) = 1}} \omega_{h,k}\, e^{-2\pi i n h / k}.$$

Let $C = \pi\sqrt{2/3}$ and $\lambda_n = \sqrt{n - \frac{1}{24}}$.

**Theorem** (Rademacher, 1937). For every integer $n \ge 1$,

$$p(n) = \frac{1}{\pi\sqrt 2} \sum_{k=1}^{\infty} A_k(n)\, \sqrt k\; \frac{d}{dn}\!\left( \frac{\sinh\!\big(C \lambda_n / k\big)}{\lambda_n} \right),$$

and the series converges absolutely.

**Remainder bound** (Lehmer, 1939, as used by Johansson, 2012). If $R(n, N)$ is the sum of the terms with $k > N$, then

$$|R(n, N)| < \frac{44\pi^2}{225\sqrt 3}\, N^{-1/2} + \frac{\pi\sqrt 2}{75} \left(\frac{N}{n - 1}\right)^{1/2} \sinh\!\left(\frac{C\sqrt n}{N}\right).$$

## In plain words

The number of ways to split a number into parts, when order does not matter, has an exact formula. The formula is an endless sum. The first term is a smooth curve that grows very fast, and it is already very close to the true count. Each later term is a small wave correction, and the corrections shrink quickly.

So a program can add up a modest number of terms and round to the nearest whole number. For one hundred, five terms are enough. The number of terms needed grows like the square root of the number, which is much less work than a table of all smaller counts.

## Proof

The identity needs the theory of modular forms. We prove two parts in full, absolute convergence and the size of the first term, and we cite the rest.

**Absolute convergence.** Since $|\omega_{h,k}| = 1$, $|A_k(n)| \le k$. Let $a = C/k$ and $u = n - \frac{1}{24}$, so the function in the term is $g(u) = \sinh(a\sqrt u)/\sqrt u = \sum_{m \ge 0} \frac{a^{2m+1} u^m}{(2m+1)!}$, and $\frac{d}{dn} = \frac{d}{du}$. Then

$$g'(u) = a^3 \sum_{m \ge 1} \frac{m\, (a^2 u)^{m-1}}{(2m+1)!}.$$

If $k \ge C\sqrt u$, then $a^2 u \le 1$, and $g'(u) \le a^3 \sum_{m \ge 1} \frac{m}{(2m+1)!} < \frac{a^3}{5}$. So for these $k$ the term $k$ has absolute value at most $\frac{1}{\pi\sqrt 2} \cdot k \cdot \sqrt k \cdot \frac{C^3}{5 k^3} = O(k^{-3/2})$, and the series converges absolutely. $\square$

**The first term.** For $k = 1$, $A_1(n) = 1$ (only $h = 0$). With $\lambda = \lambda_n$ and $\frac{d\lambda}{dn} = \frac{1}{2\lambda}$,

$$\frac{d}{dn} \frac{\sinh(C\lambda)}{\lambda} = \frac{1}{2\lambda} \left( \frac{C \cosh(C\lambda)}{\lambda} - \frac{\sinh(C\lambda)}{\lambda^2} \right) = \frac{C\, e^{C\lambda}}{4\lambda^2} \big(1 + O(\lambda^{-1})\big).$$

Dividing by $\pi\sqrt 2$ gives $\frac{e^{C\lambda_n}}{4\sqrt 3\, \lambda_n^2}(1 + O(n^{-1/2}))$. Since $C\lambda_n = C\sqrt n + O(n^{-1/2})$, this is the Hardy-Ramanujan term $\frac{e^{C\sqrt n}}{4\sqrt 3\, n}$ up to a factor $1 + O(n^{-1/2})$. For $k \ge 2$, $|A_k(n)| \le k$ and $\sinh(C\lambda_n/k) \le e^{C\sqrt n/2}$, so with the bound for large $k$ above, the sum of all terms with $k \ge 2$ is at most a power of $n$ times $e^{C\sqrt n/2}$. So the theorem implies the [Hardy-Ramanujan theorem](/hardy-ramanujan-theorem/).

**The identity (cited sketch).** Andrews (Chapter 5) and Apostol (Chapter 5) give the full proof. Its steps are:

1. Write $p(n)$ by Cauchy's formula as an integral of $P(x) x^{-n-1}$ over a circle of radius $e^{-2\pi/N^2}$, where $P(x) = \prod_m (1 - x^m)^{-1}$.
2. Cut the circle into the Ford arcs of the [Farey sequence](/farey-sequence/) of order $N$. The arc at $h/k$ is the part of the circle near the root of unity $e^{2\pi i h/k}$.
3. On the arc at $h/k$, the transformation formula of the Dedekind eta function (Apostol, Chapter 3) writes $P$ near $e^{2\pi i h/k}$ in terms of $P$ near $0$. The factor $\omega_{h,k}$ and an explicit exponential appear, and the rest is $1 + $ a small error.
4. The main parts of the arcs at $h/k$ with the same $k$ add up to $A_k(n)$ times an integral. Extending the integral gives a Bessel function, which is the elementary function in the statement because the Bessel index is $\frac32$.
5. The errors tend to $0$ as $N \to \infty$, which gives the convergent series.

Rademacher's change from Hardy and Ramanujan is the choice of the Ford arcs and the exact form of the main term in step 4. With these choices the error terms go to $0$ instead of only staying bounded. $\blacksquare$

## Consequences

**Partial sums.** The table gives the partial sums $S_N$ of the series for $n = 100$, where $p(100) = 190569292$, and for $n = 200$, where $p(200) = 3972999029388$.

| $N$ | $S_N$ for $n = 100$ | $S_N$ for $n = 200$ |
| --- | --- | --- |
| $1$ | $190568944.78$ | $3972998993185.90$ |
| $2$ | $190569293.65$ | $3972999029468.88$ |
| $3$ | $190569291.06$ | $3972999029381.30$ |
| $4$ | $190569291.74$ | $3972999029386.44$ |
| $5$ | $190569292.06$ | $3972999029387.87$ |
| $6$ | $190569292.00$ | $3972999029387.94$ |
| $8$ | $190569291.99$ | $3972999029387.98$ |
| $10$ | $190569292.00$ | $3972999029388.02$ |

So rounding $S_N$ gives $p(100)$ from $N = 4$ on and $p(200)$ from $N = 5$ on in these runs. The terms are not monotone in size, and some are $0$: $A_5(1) = A_7(1) = 0$, $A_{11}(100) = A_{13}(100) = 0$, and $A_7(200) = A_{11}(200) = 0$.

**Exact computation of one value.** Lehmer's bound shows that $N = \Theta(\sqrt n)$ terms make $|R(n, N)| < \frac12$. The bound first drops below $\frac12$ at $N = 10$ for $n = 100$ and at $N = 12$ for $n = 200$, so it is safe but larger than the true error in the table. Each term needs $A_k(n)$, which a direct sum computes in $O(k^2)$ operations and which has faster formulas, and a real number to about $C\sqrt n / \ln 2 \approx 3.7\sqrt n$ bits for the first term, with fewer bits for later terms because their size drops fast. Johansson (2012) organizes this so that the total cost is close to linear in the $\Theta(\sqrt n)$ bits of $p(n)$. A table of all $p(m)$ for $m \le n$ by [Euler's recurrence](/euler-pentagonal-recurrence/) costs $O(n^2)$ bit operations instead, so the series wins when you need one large value.

**The first term.** $A_1 = 1$ and $A_2(n) = (-1)^n$, so the second term alternates in sign with $n$. Its size is about $e^{C\sqrt n/2}$, the square root of the first term. This is the first visible correction to the Hardy-Ramanujan formula: $348.87$ for $n = 100$ and $36282.98$ for $n = 200$.

## Tightness

- **The series does not stop.** Infinitely many $A_k(n)$ are nonzero for each $n$, so no finite sum of these terms equals $p(n)$ identically; the exact value comes from rounding a partial sum whose error is known to be less than $\frac12$.
- **Floating point precision.** The first term must be computed to more bits than $p(n)$ has. In double precision, with a $53$-bit significand, the first term alone has an absolute rounding error of order $p(n)\, 2^{-53}$, so rounding the sum is unreliable once $p(n)$ comes near $2^{53}$. This happens soon: $p(n) < 2^{53}$ holds exactly for $n \le 299$, with $p(299) \approx 8.6 \times 10^{15}$. For larger $n$ use arbitrary precision arithmetic with a proven error bound, as in Johansson (2012).
- **The number of terms.** The bound $N = \Theta(\sqrt n)$ comes from the second part of Lehmer's bound. With $N = \alpha \sqrt n$, that part is about $(\alpha / \sqrt n)^{1/2} \sinh(C/\alpha)$, so a constant $\alpha$ is enough for large $n$, and a fixed $N$ is not, since $\sinh(C\sqrt n / N)$ then grows without bound.

## History

Hardy and Ramanujan found in 1918 an asymptotic series of the same shape with the exponential $e^{C\lambda_n/k}$ in place of the hyperbolic sine, and showed that about $\sqrt n$ terms give $p(n)$ within a small error. Lehmer later showed that their series diverges. Rademacher announced the convergent version in 1937 and published the proof in the Proceedings of the London Mathematical Society. Lehmer gave explicit bounds on its remainder in 1939. Rademacher simplified the proof in 1943, and the textbook versions in Andrews and Apostol follow a proof of this kind. Johansson (2012) gave a fast implementation with proven error bounds.

## References
