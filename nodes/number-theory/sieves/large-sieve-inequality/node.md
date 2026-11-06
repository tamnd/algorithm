---
tag: 516849
kind: theorem
slug: large-sieve-inequality
name: Large sieve inequality
aliases:
- Rényi-Montgomery large sieve
- large sieve
- Gallagher's large sieve
area: number-theory/sieves
level: research
summary: For well spaced points x_r, sum |S(x_r)|^2 <= (N - 1 + 1/delta) sum |a_n|^2. At the Farey fractions it bounds any set that avoids omega(p) classes mod each p by (N + Q^2)/L.
prereqs: [sieve-theory, discrete-fourier-transform, chinese-remainder-theorem, euler-totient]
see_also: [selberg-sieve, brun-sieve, primes-in-range, prime-number-theorem, mobius-function, prime-gaps, buchstab-function, legendre-phi-function]
sources:
  - paper: doi:10.1112/S0025579300007968
    title: P. X. Gallagher, The large sieve, Mathematika 14(1), 1967
    locator: pages 14 to 20 (the inequality with constant pi N + 1/delta via a Sobolev type lemma)
  - paper: doi:10.1112/S0025579300004708
    title: H. L. Montgomery and R. C. Vaughan, The large sieve, Mathematika 20(2), 1973
    locator: pages 119 to 134 (the constant N - 1 + 1/delta and the Brun-Titchmarsh bound 2y/log y)
  - paper: doi:10.1090/S0002-9904-1978-14497-8
    title: Hugh L. Montgomery, The analytic principle of the large sieve, Bulletin of the American Mathematical Society 84(4), 1978
    locator: pages 547 to 567 (survey of the analytic and arithmetic forms and their history)
  - paper: doi:10.1112/S0025579300005313
    title: E. Bombieri, On the large sieve, Mathematika 12(2), 1965
    locator: pages 201 to 225 (the large sieve for characters and the Bombieri-Vinogradov theorem)
  - book: isbn:9780821836330
    title: Henryk Iwaniec and Emmanuel Kowalski, Analytic Number Theory, American Mathematical Society Colloquium Publications 53, 2004
    locator: Chapter 7, Bilinear forms and the large sieve (pp. 169 to 195)
  - book: isbn:9780821849705
    title: John Friedlander and Henryk Iwaniec, Opera de Cribro, American Mathematical Society Colloquium Publications 57, 2010
    locator: Chapter 9, The large sieve (pp. 151 to 172)
  - book: isbn:9780521612753
    title: Alina Carmen Cojocaru and M. Ram Murty, An Introduction to Sieve Methods and Their Applications, London Mathematical Society Student Texts 66, Cambridge University Press, 2006
    locator: Chapter 8, The large sieve (p. 135)
---

The large sieve inequality bounds the mean square of a trigonometric polynomial $S(x) = \sum_{M < n \le M + N} a_n e(nx)$ over a set of well spaced points: if the points are $\delta$ apart modulo 1, the sum of $|S(x_r)|^2$ is at most $(N - 1 + \delta^{-1}) \sum |a_n|^2$. It is an approximate form of Parseval's identity, and it holds for every choice of the coefficients. Taking the points to be the fractions $a/q$ with $q \le Q$, which are $Q^{-2}$ apart, turns it into an arithmetic statement: a set of integers in an interval of length $N$ that misses $\omega(p)$ residue classes modulo every prime $p \le Q$ has at most $(N + Q^2)/L$ elements, with $L = \sum_{q \le Q} \mu^2(q) \prod_{p \mid q} \omega(p)/(p - \omega(p))$. Unlike [Brun's](/brun-sieve/) and [Selberg's](/selberg-sieve/) sieves it handles sets that miss many classes for each prime, and its form for Dirichlet characters is the main input to the Bombieri-Vinogradov theorem.

## Statement

Write $e(t) = e^{2\pi i t}$ and $\|t\|$ for the distance from $t$ to the nearest integer. Let $a_n$, $M < n \le M + N$, be complex numbers, and $S(x) = \sum_{M < n \le M + N} a_n e(nx)$.

**Theorem (analytic large sieve).** Let $x_1, \ldots, x_R$ be real numbers with $\|x_r - x_s\| \ge \delta$ for $r \ne s$, where $0 < \delta \le 1$. Then

$$\sum_{r=1}^{R} |S(x_r)|^2 \le \Delta \sum_{M < n \le M + N} |a_n|^2$$

with $\Delta = \delta^{-1} + \pi N$ (Gallagher), and with $\Delta = N - 1 + \delta^{-1}$ (Montgomery and Vaughan; Selberg).

**Corollary (arithmetic form).** For $Q \ge 1$,

$$\sum_{q \le Q} \ \sum_{\substack{a = 1 \\ (a, q) = 1}}^{q} \Big| S\Big(\frac{a}{q}\Big) \Big|^2 \le \Delta \sum_{n} |a_n|^2 \qquad \text{with } \delta = Q^{-2}.$$

**Corollary (sieve form, Montgomery).** Let $\mathcal{A}$ be a set of integers in $(M, M + N]$, and suppose that for each prime $p \le Q$ the set $\mathcal{A}$ meets at most $p - \omega(p)$ residue classes modulo $p$, where $0 \le \omega(p) < p$. Then

$$|\mathcal{A}| \le \frac{\Delta}{L}, \qquad L = \sum_{q \le Q} \mu^2(q) \prod_{p \mid q} \frac{\omega(p)}{p - \omega(p)},$$

with $\Delta = \pi N + Q^2$, or $\Delta = N - 1 + Q^2$ using the sharp constant.

The proof below gives the constant $\delta^{-1} + \pi (N - 1)$, which is slightly better than Gallagher's $\delta^{-1} + \pi N$. The sharp constant $N - 1 + \delta^{-1}$ needs a different argument (a generalized Hilbert inequality, or Beurling-Selberg extremal functions) and is not proved here.

## In plain words

Take a list of numbers and form a wave from them, one frequency per number. If you measure the wave's strength at a few points that are spread far apart, the total you get cannot be much more than the total energy of the list. Points close together could all catch the same peak, but spread out points cannot.

The fractions with small denominators are spread out in this way. Measuring the wave at them tells you how the list is distributed among remainders modulo small numbers. If a set of integers stays away from many remainders, its wave has big values at these fractions, more than the energy bound allows unless the set is small. That is how the inequality becomes a sieve: sets that avoid many remainder classes for every small prime must be thin.

## Proof

**Step 1: a Sobolev type lemma (Gallagher).** Let $f$ be continuously differentiable on an interval $I$ of length $\delta$ with midpoint $u$. Then

$$|f(u)| \le \frac{1}{\delta} \int_I |f(t)|\, dt + \frac{1}{2} \int_I |f'(t)|\, dt.$$

For $t \in I$, $f(u) = f(t) - \int_u^t f'(s)\, ds$, so $|f(u)| \le |f(t)| + \big|\int_u^t |f'(s)|\, ds\big|$. Average over $t \in I$. The first term gives $\delta^{-1}\int_I |f|$. For $t$ in the right half of $I$, $\int_u^t |f'| \le \int_u^{u + \delta/2} |f'|$, and the right half has length $\delta/2$; likewise for the left half. So the second term is at most $\delta^{-1} \cdot \frac{\delta}{2} \int_I |f'| = \frac{1}{2}\int_I |f'|$.

**Step 2: center the frequencies.** Let $K = M + (N + 1)/2$ and $T(x) = \sum_n a_n e((n - K) x)$. Then $|T(x)| = |S(x)|$ for every real $x$, and $|n - K| \le (N - 1)/2$ for every $n$ in the range. Both $|T|$ and $|T'|$ are periodic with period 1, since $T(x + 1) = e(-K) T(x)$ and $T'(x + 1) = e(-K) T'(x)$.

**Step 3: apply the lemma to $T^2$.** Let $I_r$ be the interval of length $\delta$ centered at $x_r$. Since the points are $\delta$ apart modulo 1, the intervals $I_r$ do not overlap modulo 1. Step 1 with $f = T^2$, $f' = 2 T T'$, gives

$$|S(x_r)|^2 = |T(x_r)|^2 \le \frac{1}{\delta} \int_{I_r} |T|^2 + \int_{I_r} |T|\,|T'|.$$

Summing over $r$ and using periodicity and disjointness,

$$\sum_r |S(x_r)|^2 \le \frac{1}{\delta} \int_0^1 |T|^2 + \int_0^1 |T|\,|T'|.$$

**Step 4: Parseval and Cauchy-Schwarz.** The frequencies $n - K$ differ by integers, so the cross terms integrate to zero over a period, and

$$\int_0^1 |T|^2 = \sum_n |a_n|^2, \qquad \int_0^1 |T'|^2 = 4\pi^2 \sum_n (n - K)^2 |a_n|^2 \le \pi^2 (N - 1)^2 \sum_n |a_n|^2.$$

By Cauchy-Schwarz, $\int_0^1 |T|\,|T'| \le \big(\int |T|^2\big)^{1/2} \big(\int |T'|^2\big)^{1/2} \le \pi (N - 1) \sum_n |a_n|^2$. Therefore

$$\sum_r |S(x_r)|^2 \le \big(\delta^{-1} + \pi (N - 1)\big) \sum_n |a_n|^2.$$

**Step 5: Farey fractions are well spaced.** If $a/q \ne a'/q'$ are reduced fractions in $[0, 1)$ with $q, q' \le Q$, then $a q' - a' q$ is a nonzero integer, so $\|a/q - a'/q'\| \ge 1/(q q') \ge Q^{-2}$ (the same argument applies to $a/q - a'/q' \pm 1$). Step 4 with $\delta = Q^{-2}$ gives the arithmetic form.

**Step 6: one prime.** Let $a_n$ be supported on $\mathcal{A}$, and fix a prime $p$. Put $Z_h = \sum_{n \in \mathcal{A},\, n \equiv h \bmod p} a_n$. Then $S(c/p) = \sum_{h \bmod p} Z_h\, e(ch/p)$, and by orthogonality of the characters $e(ch/p)$,

$$\sum_{c=0}^{p-1} |S(c/p)|^2 = p \sum_{h} |Z_h|^2.$$

Only $p - \omega(p)$ of the $Z_h$ can be nonzero, so by Cauchy-Schwarz $|S(0)|^2 = |\sum_h Z_h|^2 \le (p - \omega(p)) \sum_h |Z_h|^2$. Hence

$$\sum_{c=1}^{p-1} |S(c/p)|^2 = p \sum_h |Z_h|^2 - |S(0)|^2 \ge \Big( \frac{p}{p - \omega(p)} - 1 \Big) |S(0)|^2 = \frac{\omega(p)}{p - \omega(p)}\, |S(0)|^2.$$

**Step 7: squarefree moduli.** We show by induction on the number of prime factors that, for squarefree $q$ composed of primes $p \le Q$,

$$\sum_{\substack{a = 1 \\ (a, q) = 1}}^{q} |S(a/q)|^2 \ge \prod_{p \mid q} \frac{\omega(p)}{p - \omega(p)}\, |S(0)|^2$$

for every coefficient sequence supported on $\mathcal{A}$. The case $q = 1$ is trivial. Let $q = q_1 p$ with $p \nmid q_1$. By the [Chinese remainder theorem](/chinese-remainder-theorem/), the reduced fractions $a/q$ modulo 1 are exactly the numbers $b/q_1 + c/p$ with $(b, q_1) = 1$ and $1 \le c \le p - 1$, each once. For fixed $b$, apply Step 6 to the coefficients $a_n e(nb/q_1)$, which are still supported on $\mathcal{A}$; their sum at $x$ is $S(x + b/q_1)$. This gives $\sum_{c=1}^{p-1} |S(b/q_1 + c/p)|^2 \ge \frac{\omega(p)}{p - \omega(p)} |S(b/q_1)|^2$. Summing over $b$ and applying the induction hypothesis to $q_1$ proves the claim.

**Step 8: the sieve form.** Take $a_n = 1$ on $\mathcal{A}$ and $0$ elsewhere, so $S(0) = |\mathcal{A}|$ and $\sum |a_n|^2 = |\mathcal{A}|$. Summing Step 7 over squarefree $q \le Q$ and comparing with the arithmetic form,

$$L\, |\mathcal{A}|^2 \le \sum_{q \le Q} \sum_{(a, q) = 1} |S(a/q)|^2 \le \Delta\, |\mathcal{A}|,$$

and dividing by $L |\mathcal{A}|$ gives $|\mathcal{A}| \le \Delta / L$. $\blacksquare$

## Consequences

- **Primes in short intervals.** The primes in $(M, M + N]$ that exceed $Q$ avoid the class $0$ modulo every $p \le Q$, so $\omega(p) = 1$ and $L = \sum_{q \le Q} \mu^2(q)/\varphi(q) \ge \log Q$. With the sharp constant and $Q$ near $(N/\log N)^{1/2}$, this gives $\pi(M + N) - \pi(M) \le (2 + o(1)) N/\log N$; Montgomery and Vaughan proved the clean form $\pi(x + y) - \pi(x) \le 2y/\log y$ for all $y > 1$. For the interval $(10^9, 10^9 + 10^6]$, which holds $48155$ primes, the sharp form gives $154665$ at its best $Q$, near 290 ($Q = 300$ gives $L = 7.0328$ and $154987$), and Gallagher's constant gives $448702$ at its best $Q$, near 470. The quantity $L$ is the same $G$ that appears in [Selberg's sieve](/selberg-sieve/).
- **Sets that avoid half the classes.** A set of integers in $[1, N]$ that, for each odd prime $p \le Q$, lies in at most $(p + 1)/2$ classes has $\omega(p)/(p - \omega(p)) \ge (p - 1)/(p + 1)$, so $L$ is at least of order $Q / \log Q$, and $Q = N^{1/2}$ gives $|\mathcal{A}| \ll N^{1/2} \log N$. The squares are such a set. For $N = 10^6$ the bound is $6511$, at $Q = 1013$, against the $1000$ squares up to $10^6$. This is the shape of Linnik's original use of the method: if every prime below $p^{\varepsilon}$ were a quadratic residue modulo $p$ for many primes $p$, then all integers built from such small primes would lie in only $(p + 1)/2$ classes modulo each of these $p$, and there are too many such integers for that.
- **The multiplicative large sieve.** By expanding $e(an/q)$ in Dirichlet characters, the arithmetic form implies $\sum_{q \le Q} \frac{q}{\varphi(q)} \sum_{\chi \bmod q}^{*} \big|\sum_n a_n \chi(n)\big|^2 \le \Delta \sum_n |a_n|^2$, where the inner sum is over primitive characters.
- **Bombieri-Vinogradov.** The multiplicative form, combined with an identity for $\Lambda(n)$ that splits it into bilinear pieces, gives: for every $A > 0$ there is $B$ with $\sum_{q \le x^{1/2} (\log x)^{-B}} \max_{(a, q) = 1} |\pi(x; q, a) - \mathrm{li}(x)/\varphi(q)| \ll_A x (\log x)^{-A}$. This is the generalized Riemann hypothesis on average over moduli, and it is the level of distribution used in most sieve applications to primes.

## Tightness

- **The constant $N - 1 + \delta^{-1}$ is attained.** Let $R$ be a positive integer, $x_r = r/R$ for $r = 0, \ldots, R - 1$ (so $\delta = 1/R$), $N = kR + 1$, and $a_n = 1$ for $n = 0, R, 2R, \ldots, kR$ and $0$ otherwise. Then $S(r/R) = k + 1$ for every $r$, the left side is $R (k + 1)^2$, and $\sum |a_n|^2 = k + 1$, so the ratio is $R(k + 1) = N - 1 + \delta^{-1}$. A script confirms this for $(R, k) = (5, 3), (7, 2), (10, 4)$.
- **Each of the two terms is needed.** One point and $a_n = e(-n x_1)$ give the ratio $N$; the $R$ points $r/R$ and a single nonzero $a_n$ give the ratio $R = \delta^{-1}$. So $\Delta \ge \max(N, \delta^{-1})$, and any valid constant is within a factor 2 of $N - 1 + \delta^{-1}$.
- **The sieve form loses a factor 2 for primes.** In the interval example above the bound is about $2N/\log N$, twice the truth. Selberg's parity examples show that no argument using only the number of avoided classes can do better for the primes.

## History

Linnik introduced the method in 1941 to show that the least quadratic non-residue modulo $p$ is small for almost all primes $p$; Rényi developed it into a general sieve in the following years. Roth and Bombieri, in 1965, turned it into an inequality for trigonometric sums of the shape above, and Bombieri used the character version to prove the theorem now called Bombieri-Vinogradov, found independently by A. I. Vinogradov. Davenport and Halberstam gave the analytic form with spaced points. Gallagher's 1967 paper gave the short proof reproduced here, with the constant $\pi N + \delta^{-1}$. Montgomery derived the sieve form with $\omega(p)$ classes, the step that makes the inequality a sieve in the usual sense, and Montgomery and Vaughan proved the sharp constant $N - 1 + \delta^{-1}$ in 1973; Selberg obtained the same constant with extremal functions of Beurling's type. Montgomery's 1978 survey tells the story in detail.

## References
