---
tag: H9E4HR
kind: theorem
slug: prime-number-theorem
name: Prime number theorem
aliases:
- PNT
area: number-theory/primality
level: advanced
summary: The number pi(x) of primes up to x satisfies pi(x) ~ x / ln x, so near x about one integer in ln x is prime. The integral li(x) is a better estimate; its error is tied to the Riemann hypothesis.
prereqs: [prime-number, prime-counting-function, asymptotic-equivalence]
see_also: [bertrands-postulate, prime-gaps, random-prime-generation, meissel-lehmer-algorithm, lcm-of-integers, mobius-function, legendre-formula, abel-summation]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 1.1.5 (Theorems 1.1.3 and 1.1.4, equations (1.2) to (1.4), Table 1.1), Section 1.4.1 (Conjecture 1.4.1, Theorem 1.4.3, relation (1.25)), Section 1.4.2, and Exercises 1.36 and 1.37
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition
    locator: Chapter 5, Section 5.1 (Theorems 5.1 and 5.4 to 5.7, Lemmas 5.2 and 5.3), Section 5.5.1 (Theorem 5.14), Section 5.5.2 (Theorem 5.15, Conjecture 5.16, Tables 5.1 and 5.2), Section 5.5.3 (Theorem 5.19) and Section 5.6
  - paper: doi:10.1080/00029890.1997.11990704
    title: Don Zagier, Newman's short proof of the prime number theorem, The American Mathematical Monthly 104 (1997)
    locator: pages 705 to 708
  - paper: doi:10.24033/bsmf.545
    title: Jacques Hadamard, Sur la distribution des zeros de la fonction zeta(s) et ses consequences arithmetiques, Bulletin de la Societe Mathematique de France 24 (1896)
    locator: pages 199 to 220
  - paper: doi:10.1215/ijm/1255631807
    title: J. Barkley Rosser and Lowell Schoenfeld, Approximate formulas for some functions of prime numbers, Illinois Journal of Mathematics 6 (1962)
    locator: pages 64 to 94
---

The prime number theorem says that the number $\pi(x)$ of [primes](/prime-number/) $p \le x$ satisfies $\pi(x) \sim x / \ln x$ as $x \to \infty$. Equivalently, the $n$th prime is about $n \ln n$, and near a large $x$ about one integer in $\ln x$ is prime. Gauss conjectured it about 1791, and Hadamard and de la Vallee Poussin proved it independently in 1896. In the analysis of algorithms it is the reason that a random $\ell$ bit integer is prime with probability about $1/(\ell \ln 2)$.

## Statement

Let $\pi(x)$ be the [prime counting function](/prime-counting-function/), the number of primes $p \le x$ for real $x$. Let $\vartheta(x) = \sum_{p \le x} \ln p$ and $\psi(x) = \sum_{p^k \le x} \ln p$ be Chebyshev's functions, and let $\operatorname{li}(x) = \int_2^x dt / \ln t$ for $x \ge 2$. Here $\ln$ is the natural logarithm and $f \sim g$ means $f/g \to 1$ ([asymptotic equivalence](/asymptotic-equivalence/)).

**Theorem** (prime number theorem; Hadamard and de la Vallee Poussin; Crandall and Pomerance, Theorem 1.1.4; Shoup, Theorem 5.14). As $x \to \infty$,
$$\pi(x) \sim \frac{x}{\ln x}.$$

**Equivalent forms.** Each of the following is equivalent to the theorem, by elementary arguments (step (VIII) of the proof below, the remark after it, and Shoup, Exercises 5.20 and 5.21):

- $\vartheta(x) \sim x$, that is, $\prod_{p \le x} p = e^{(1 + o(1)) x}$;
- $\psi(x) \sim x$, that is, $\operatorname{lcm}(1, 2, \ldots, n) = e^{(1 + o(1)) n}$;
- $p_n \sim n \ln n$, where $p_n$ is the $n$th prime;
- $\pi(x) \sim \operatorname{li}(x)$, since $\operatorname{li}(x) = x/\ln x + O(x/\ln^2 x)$.

**Chebyshev's theorem** (Crandall and Pomerance, Theorem 1.1.3; Shoup, Theorem 5.1). There are constants $A, B > 0$ with $A x/\ln x < \pi(x) < B x/\ln x$ for all $x \ge 3$. Crandall and Pomerance note that $A = 1/2$ and $B = 2$ work. This weaker result has an elementary proof, given below with the constants $A = (3 \ln 2)/8$ and $B = 4 \ln 2 + 2/e$.

**With an error term.** The proof of 1896 gives more (Crandall and Pomerance, equation (1.2)): for some $c > 0$,
$$\pi(x) = \operatorname{li}(x) + O\big(x e^{-c \sqrt{\ln x}}\big).$$
The best known error term is $O(x e^{-c \kappa(x)})$ with $\kappa(x) = (\ln x)^{3/5} (\ln \ln x)^{-1/5}$ (Shoup, Theorem 5.15, due to Walfisz). Both are $o(x / \ln^k x)$ for every fixed $k$.

**Under the Riemann hypothesis.** The Riemann hypothesis is equivalent to $\pi(x) = \operatorname{li}(x) + O(x^{1/2 + \epsilon})$ for every fixed $\epsilon > 0$ (Riemann; Crandall and Pomerance, relation (1.25)), and to $|\pi(x) - \operatorname{li}(x)| < x^{1/2} \ln x$ for all $x \ge 2.01$ (von Koch; Crandall and Pomerance, Exercise 1.37; Shoup, Conjecture 5.16 and Section 5.6). Schoenfeld showed that, under the hypothesis, $|\pi(x) - \operatorname{li}_0(x)| < x^{1/2} \ln x / (8 \pi)$ for $x \ge 2657$, where $\operatorname{li}_0(x) = \operatorname{li}(x) + 1.0451637801\ldots$ (Crandall and Pomerance, Exercise 1.37). These are conditional results.

**Explicit bounds with no conditions** (Rosser and Schoenfeld 1962; Shoup, Theorem 5.19):
$$\frac{x}{\ln x}\Big(1 + \frac{1}{2 \ln x}\Big) < \pi(x) < \frac{x}{\ln x}\Big(1 + \frac{3}{2 \ln x}\Big) \quad (x \ge 59),$$
$$n(\ln n + \ln \ln n - 3/2) < p_n < n(\ln n + \ln \ln n - 1/2) \quad (n \ge 20).$$

## In plain words

Primes get rarer as numbers grow, but slowly and in a regular way. Among numbers near a thousand, about one in seven is prime. Near a million, about one in fourteen. Near a billion, about one in twenty one. Each time the numbers get a thousand times larger, the gap between primes grows by about the same amount, close to seven. The theorem makes this exact: the average spacing near a number grows like its natural logarithm, that is, like its number of digits times a constant. So to find a prime with a few hundred digits, one tries a few hundred random candidates, not millions. The theorem says nothing about where each single prime falls; it describes only the average.

## Proof

We first prove Chebyshev's theorem, which is elementary, and then the prime number theorem by the short analytic proof of Newman, in the form given by Zagier (1997). The second part uses standard complex analysis: Cauchy's integral theorem, the uniqueness of analytic continuation, and the fact that the zeros of a holomorphic function that is not identically zero are isolated.

**Lemma 1** (Shoup, Theorem 5.6). $\vartheta(x) < 2 (\ln 2) x$ for every real $x \ge 1$. Equivalently, $\prod_{p \le x} p < 4^x$.

*Proof.* As $\vartheta(x) = \vartheta(\lfloor x \rfloor)$, it suffices to prove $\vartheta(n) < 2 (\ln 2) n$ for integers $n \ge 1$, by induction. For $n = 1$ and $n = 2$ it is direct. If $n > 2$ is even, $n$ is not prime, so $\vartheta(n) = \vartheta(n - 1) < 2 (\ln 2)(n - 1)$. If $n = 2m + 1$ is odd, let $M = \binom{2m+1}{m}$. Every prime $p$ with $m + 1 < p \le 2m + 1$ divides $(2m + 1)!/(m + 1)!$ and does not divide $m!$, so it divides $M$. The binomial coefficient $M$ appears twice in the expansion of $(1 + 1)^{2m+1}$, so $M < 2^{2m+1}/2 = 4^m$. Hence $\vartheta(2m + 1) - \vartheta(m + 1) \le \ln M < 2 (\ln 2) m$, and with the induction hypothesis for $m + 1 < n$, $\vartheta(n) < 2 (\ln 2) m + 2 (\ln 2)(m + 1) = 2 (\ln 2) n$. $\square$

**Lemma 2** (Shoup, Theorem 5.4). $\pi(n) \ge \frac{\ln 2}{2} \cdot \frac{n}{\ln n}$ for every integer $n \ge 2$.

*Proof.* Let $m \ge 1$ and $N = \binom{2m}{m}$. By [Legendre's formula](/legendre-formula/), $\nu_p(N) = \sum_{k \ge 1} (\lfloor 2m/p^k \rfloor - 2 \lfloor m / p^k \rfloor)$. Each term is 0 or 1, and it is 0 when $p^k > 2m$, so $\nu_p(N) \le \ln(2m)/\ln p$. Only primes $p \le 2m$ divide $N$, so
$$\ln N = \sum_{p \le 2m} \nu_p(N) \ln p \le \pi(2m) \ln(2m).$$
$N$ is the largest of the $2m + 1$ terms of $(1 + 1)^{2m}$, and the two end terms are 1, so $4^m \le 2 + (2m - 1) N \le 2m N$, and $N \ge 4^m/(2m) \ge 2^m$. Thus $\pi(2m) \ln(2m) \ge m \ln 2$, which is the claim for $n = 2m$. For odd $n = 2m - 1 \ge 3$, $\pi(2m - 1) = \pi(2m)$, and $x / \ln x$ increases for $x \ge 3$, so the claim for $2m$ gives it for $2m - 1$. $\square$

**Chebyshev's theorem.** Let $x \ge 3$ be real and $n = \lfloor x \rfloor \ge 3$. As $t/\ln t$ increases for $t \ge 3$, $x/\ln x < (n + 1)/\ln n \le \frac43 n/\ln n$. So Lemma 2 gives $\pi(x) = \pi(n) \ge \frac{\ln 2}{2} \cdot \frac{n}{\ln n} > \frac{3 \ln 2}{8} \cdot \frac{x}{\ln x}$. For the upper bound, every prime in $(\sqrt x, x]$ has $\ln p > \frac12 \ln x$, so $\vartheta(x) \ge \frac12 \ln x \, (\pi(x) - \sqrt x)$. With Lemma 1,
$$\pi(x) < \sqrt x + \frac{4 (\ln 2) x}{\ln x} \le \Big(4 \ln 2 + \frac{2}{e}\Big) \frac{x}{\ln x},$$
since $\sqrt x \ln x / x = \ln x / \sqrt x \le 2/e$ for all $x > 1$. $\square$

We now prove the prime number theorem. For complex $s$ write $\sigma = \operatorname{Re} s$. Let
$$\zeta(s) = \sum_{n \ge 1} n^{-s}, \qquad \Phi(s) = \sum_p \frac{\ln p}{p^s} \qquad (\sigma > 1).$$
Both series converge absolutely and locally uniformly for $\sigma > 1$, so both functions are holomorphic there.

**(I) Euler product.** For $\sigma > 1$, $\zeta(s) = \prod_p (1 - p^{-s})^{-1}$. This follows from unique factorization by expanding each factor as a geometric series; the product converges absolutely, and no factor is zero, so $\zeta(s) \ne 0$ for $\sigma > 1$.

**(II) Continuation of $\zeta$.** The function $\zeta(s) - 1/(s - 1)$ extends to a holomorphic function on $\sigma > 0$. For $\sigma > 1$,
$$\zeta(s) - \frac{1}{s - 1} = \sum_{n \ge 1} \frac{1}{n^s} - \int_1^\infty \frac{dx}{x^s} = \sum_{n \ge 1} \int_n^{n+1} \Big(\frac{1}{n^s} - \frac{1}{x^s}\Big) dx.$$
Each term is entire in $s$, and
$$\Big|\int_n^{n+1} \Big(\frac{1}{n^s} - \frac{1}{x^s}\Big) dx\Big| = \Big|s \int_n^{n+1} \int_n^x \frac{du}{u^{s+1}} \, dx\Big| \le \frac{|s|}{n^{\sigma + 1}}.$$
So the series converges locally uniformly for $\sigma > 0$ and defines the continuation. Thus $\zeta$ is meromorphic on $\sigma > 0$ with one pole, a simple pole at $s = 1$.

**(III) $\vartheta(x) = O(x)$.** This is Lemma 1.

**(IV) No zeros on the line $\sigma = 1$.** The function $\zeta(s)$ has no zero with $\sigma \ge 1$, and $\Phi(s) - 1/(s - 1)$ is holomorphic on an open set that contains the closed half plane $\sigma \ge 1$.

For $\sigma > 1$, taking the logarithmic derivative of the Euler product,
$$-\frac{\zeta'(s)}{\zeta(s)} = \sum_p \frac{\ln p}{p^s - 1} = \Phi(s) + \sum_p \frac{\ln p}{p^s (p^s - 1)}.$$
The last sum converges locally uniformly for $\sigma > 1/2$, so by (II) $\Phi$ extends to a meromorphic function on $\sigma > 1/2$ whose only poles are at $s = 1$ and at the zeros of $\zeta$. At $s = 1$, $\zeta$ has a simple pole, so $\Phi$ has a simple pole with residue 1. At a zero of $\zeta$ of order $\mu$, $\Phi$ has a simple pole with residue $-\mu$.

Let $\alpha \ne 0$ be real, and let $\mu \ge 0$ and $\nu \ge 0$ be the orders of zero of $\zeta$ at $1 + i\alpha$ and $1 + 2i\alpha$ (order 0 if there is no zero; $\zeta$ has no pole there). Since $\zeta(\bar s) = \overline{\zeta(s)}$, the orders at $1 - i\alpha$ and $1 - 2i\alpha$ are also $\mu$ and $\nu$. As $\epsilon \to 0^+$, $\epsilon \, \Phi(1 + \epsilon + i r \alpha)$ tends to the residue: $1$ for $r = 0$, $-\mu$ for $r = \pm 1$, and $-\nu$ for $r = \pm 2$. For $\epsilon > 0$,
$$\sum_{r=-2}^{2} \binom{4}{2 + r} \Phi(1 + \epsilon + i r \alpha) = \sum_p \frac{\ln p}{p^{1 + \epsilon}} \big(p^{i\alpha/2} + p^{-i\alpha/2}\big)^4 \ge 0,$$
because $p^{i\alpha/2} + p^{-i\alpha/2} = 2 \cos(\tfrac{\alpha}{2} \ln p)$ is real. Multiply by $\epsilon$ and let $\epsilon \to 0^+$: $6 - 8\mu - 2\nu \ge 0$. So $\mu = 0$.

Thus the only pole of $\Phi$ on $\sigma \ge 1$ is $s = 1$, with residue 1, and $\Phi(s) - 1/(s - 1)$ is holomorphic on $\sigma \ge 1$. Since the set of zeros of $\zeta$ in $\sigma > 1/2$ is closed and does not meet $\sigma \ge 1$, it is holomorphic on an open set containing $\sigma \ge 1$.

**(V) Analytic theorem** (Newman). Let $f : [0, \infty) \to \mathbb{R}$ be bounded and locally integrable, and suppose the function $g(z) = \int_0^\infty f(t) e^{-zt} dt$, defined for $\operatorname{Re} z > 0$, extends to a holomorphic function on an open set containing $\operatorname{Re} z \ge 0$. Then $\int_0^\infty f(t) \, dt$ exists and equals $g(0)$.

*Proof.* Let $|f| \le K$. For $T > 0$ let $g_T(z) = \int_0^T f(t) e^{-zt} dt$; it is entire. We show $g_T(0) \to g(0)$. Fix $R > 0$. Choose $\delta > 0$ such that $g$ is holomorphic on and inside the closed curve $C$ that bounds the region $\{|z| \le R, \operatorname{Re} z \ge -\delta\}$. This is possible because the segment from $-iR$ to $iR$ is compact. By Cauchy's formula,
$$g(0) - g_T(0) = \frac{1}{2 \pi i} \oint_C \big(g(z) - g_T(z)\big) e^{zT} \Big(1 + \frac{z^2}{R^2}\Big) \frac{dz}{z}.$$
On $|z| = R$ we have $\big(1 + z^2/R^2\big)/z = (\bar z + z)/R^2 = 2 \operatorname{Re} z / R^2$ in absolute value.

On $C_+ = C \cap \{\operatorname{Re} z > 0\}$, a half circle of radius $R$, $|g(z) - g_T(z)| = \big|\int_T^\infty f(t) e^{-zt} dt\big| \le K e^{-\operatorname{Re} z \, T}/\operatorname{Re} z$. So the integrand is at most $2K/R^2$ in absolute value, and the part of the integral on $C_+$, divided by $2\pi$, is at most $K/R$.

On $C_- = C \cap \{\operatorname{Re} z < 0\}$ take the two terms apart. As $g_T$ is entire, its integral over $C_-$ equals its integral over the half circle $|z| = R$, $\operatorname{Re} z < 0$. There $|g_T(z)| \le \int_{-\infty}^T K e^{-\operatorname{Re} z \, t} dt = K e^{-\operatorname{Re} z \, T} / |\operatorname{Re} z|$, so the same estimate bounds this part by $K/R$. The remaining integral, of $g(z) e^{zT} (1 + z^2/R^2)/z$ over $C_-$, has an integrand that does not depend on $T$ except through $e^{zT}$, which tends to 0 at every point of $C_-$ apart from its two end points; by dominated convergence this integral tends to 0 as $T \to \infty$.

So $\limsup_{T \to \infty} |g(0) - g_T(0)| \le 2K/R$. As $R$ is arbitrary, $g_T(0) \to g(0)$. $\square$

**(VI) The integral $\int_1^\infty \frac{\vartheta(x) - x}{x^2} dx$ converges.** For $\sigma > 1$, [partial summation](/abel-summation/) (Stieltjes integration by parts, with $\vartheta(x) = O(x)$ from (III)) and the substitution $x = e^t$ give
$$\Phi(s) = \int_1^\infty x^{-s} \, d\vartheta(x) = s \int_1^\infty \frac{\vartheta(x)}{x^{s+1}} dx = s \int_0^\infty e^{-st} \vartheta(e^t) \, dt.$$
Let $f(t) = \vartheta(e^t) e^{-t} - 1$. It is bounded by (III) and locally integrable, and for $\operatorname{Re} z > 0$
$$g(z) = \int_0^\infty f(t) e^{-zt} dt = \frac{\Phi(z + 1)}{z + 1} - \frac{1}{z} = \frac{1}{z + 1}\Big(\Phi(z + 1) - \frac{1}{z}\Big) - \frac{1}{z + 1}.$$
By (IV) this is holomorphic on an open set containing $\operatorname{Re} z \ge 0$. By (V), $\int_0^\infty f(t) dt$ converges, and with $x = e^t$ it is the integral in the claim.

**(VII) $\vartheta(x) \sim x$.** Suppose that for some $\lambda > 1$ there are arbitrarily large $x$ with $\vartheta(x) \ge \lambda x$. Since $\vartheta$ does not decrease, for such $x$
$$\int_x^{\lambda x} \frac{\vartheta(t) - t}{t^2} dt \ge \int_x^{\lambda x} \frac{\lambda x - t}{t^2} dt = \int_1^\lambda \frac{\lambda - t}{t^2} dt > 0,$$
a fixed positive number. This is against the Cauchy criterion for the convergent integral of (VI). In the same way, if $\vartheta(x) \le \lambda x$ for some $\lambda < 1$ and arbitrarily large $x$, then
$$\int_{\lambda x}^{x} \frac{\vartheta(t) - t}{t^2} dt \le \int_{\lambda x}^{x} \frac{\lambda x - t}{t^2} dt = \int_\lambda^1 \frac{\lambda - t}{t^2} dt < 0,$$
again a contradiction. So $\vartheta(x)/x \to 1$.

**(VIII) From $\vartheta$ to $\pi$.** On the one hand $\vartheta(x) \le \pi(x) \ln x$. On the other hand, for $0 < \epsilon < 1$,
$$\vartheta(x) \ge \sum_{x^{1 - \epsilon} < p \le x} \ln p \ge (1 - \epsilon) \ln x \, \big(\pi(x) - x^{1 - \epsilon}\big).$$
So $\frac{\vartheta(x)}{x} \le \frac{\pi(x)}{x/\ln x} \le \frac{1}{1 - \epsilon} \frac{\vartheta(x)}{x} + \frac{\ln x}{x^{\epsilon}}$. By (VII) the lower bound tends to 1 and the upper bound to $1/(1 - \epsilon)$. As $\epsilon$ is arbitrary, $\pi(x) \ln x / x \to 1$. $\blacksquare$

The same inequalities show the converse, that $\pi(x) \sim x/\ln x$ implies $\vartheta(x) \sim x$. And $\psi(x) - \vartheta(x) = \sum_{k \ge 2} \vartheta(x^{1/k}) = O(\sqrt x \ln x)$ by Lemma 1, since only $k \le \lg x$ give nonzero terms, so $\psi(x) \sim x$ as well.

## Consequences

**Density of primes of a given length.** The theorem gives $\pi(2^\ell) - \pi(2^{\ell - 1}) \sim 2^{\ell - 1}/(\ell \ln 2)$. So an integer chosen at random with exactly $\ell$ binary digits is prime with probability about $1/(\ell \ln 2)$, and an odd one with probability about $2/(\ell \ln 2)$. This is the basis of the expected cost of [random prime generation](/random-prime-generation/): for $\ell = 1024$ it gives about $1/710$, or about one odd candidate in $355$. The table counts the primes with exactly $\ell$ binary digits; the counts were computed by a sieve.

| $\ell$ | primes with $\ell$ digits | $2^{\ell-1}$ divided by the count | $\ell \ln 2$ |
|---|---|---|---|
| 10 | 75 | 6.83 | 6.93 |
| 16 | 3030 | 10.81 | 11.09 |
| 20 | 38635 | 13.57 | 13.86 |
| 23 | 268216 | 15.64 | 15.94 |

**Values of $\pi(x)$.** The counts below are by a sieve for $x \le 10^7$, and from Shoup (Tables 5.1 and 5.2) and Crandall and Pomerance (Section 1.1.5) for larger $x$. The values of $\operatorname{li}(x) = \int_2^x dt/\ln t$ were computed by script to 60 digits with Ramanujan's series and agree with both books.

| $x$ | $\pi(x)$ | $x/\ln x$ | $\operatorname{li}(x)$ | $x/\pi(x)$ |
|---|---|---|---|---|
| $10^3$ | 168 | 144.8 | 176.6 | 5.952 |
| $10^6$ | 78498 | 72382.4 | 78626.5 | 12.739 |
| $10^9$ | 50847534 | 48254942.4 | 50849233.9 | 19.667 |
| $10^{12}$ | 37607912018 | 36191206825.3 | 37607950279.8 | 26.590 |
| $10^{18}$ | 24739954287740860 | 24127471216847323.8 | 24739954309690414.0 | 40.420 |
| $10^{21}$ | 21127269486018731928 | 20680689614440563221.5 | 21127269486616126181.3 | 47.332 |

The last column grows by about $\ln 1000 \approx 6.91$ per row step of a factor $1000$, as the theorem predicts. At $10^{18}$, $x/\ln x$ is off by about $2.5$ percent, while $\operatorname{li}(x)$ is off by less than $10^{-9}$ relative.

**The $n$th prime and products of primes.** $p_n \sim n \ln n$; Rosser showed $p_n > n \ln n$ for all $n \ge 1$ (Crandall and Pomerance, Section 1.4.2). The primorial $\prod_{p \le x} p = e^{\vartheta(x)}$ is $e^{(1 + o(1))x}$, and the [least common multiple](/lcm-of-integers/) of $1, \ldots, n$ is $e^{\psi(n)} = e^{(1 + o(1)) n}$. For example $\prod_{p \le 30} p = 6469693230 = e^{22.59\ldots}$, below the bound $4^{30} = e^{41.59\ldots}$ of Lemma 1. These estimates fix the size of the exponent for a bound $B$ in [Pollard's $p - 1$ method](/pollard-p-minus-1/) and similar algorithms, where an exponent is the product of all prime powers up to $B$.

**Bertrand's postulate for large $x$.** From the theorem, for every $\epsilon > 0$, $\pi((1 + \epsilon)x) - \pi(x) \sim \epsilon x/\ln x$, so for large $x$ there is a prime between $x$ and $(1 + \epsilon) x$ (Shoup, Exercise 5.22). [Bertrand's postulate](/bertrands-postulate/), a prime between $n$ and $2n$ for every $n \ge 1$, needs the elementary argument for small $n$.

**Average gap.** The average distance between consecutive primes near $x$ is $\ln x$. This is an average only; see [prime gaps](/prime-gaps/) for what is known about the largest and the smallest gaps.

**Size of tables and outputs.** A table of all primes below $x$ has about $x/\ln x$ entries. The [Meissel-Lehmer algorithm](/meissel-lehmer-algorithm/) and other methods compute $\pi(x)$ without listing the primes, and their running times are compared with this output size.

**The Mobius function.** The theorem is equivalent to $M(x) = \sum_{n \le x} \mu(n) = o(x)$, where $\mu$ is the [Mobius function](/mobius-function/), and the Riemann hypothesis is equivalent to $M(x) = O(x^{1/2 + \epsilon})$ for every fixed $\epsilon > 0$ (Crandall and Pomerance, Theorem 1.4.3).

## Tightness

**The constant 1 is forced.** Chebyshev knew that if $\pi(x)/(x/\ln x)$ has a limit, the limit must be 1 (Crandall and Pomerance, Section 1.1.5; Shoup, Exercise 5.10). The hard part of the theorem is that the limit exists.

**The error of $x/\ln x$.** It cannot be smaller than order $x/\ln^2 x$: $\pi(x) = x/\ln x + x/\ln^2 x + O(x/\ln^3 x)$, from $\operatorname{li}(x) = x/\ln x + x/\ln^2 x + O(x/\ln^3 x)$ and the error term of $\operatorname{li}$. So the relative error of $x/\ln x$ is about $1/\ln x$, which goes to 0 slowly. The best simple choice of the form $x/(\ln x - B)$ is $B = 1$, not Legendre's $B = 1.08366$ (Crandall and Pomerance, Section 1.1.5).

**The error of $\operatorname{li}(x)$.** The bound $O(x e^{-c \kappa(x)})$ is the best proved. The Riemann hypothesis would give $O(x^{1/2} \ln x)$. The error does not keep one sign: Littlewood proved that $\pi(x) - \operatorname{li}(x)$ changes sign infinitely often (Crandall and Pomerance, Exercise 1.36). Although $\pi(x) < \operatorname{li}(x)$ at every $x$ in the table above, the first $x$ with $\pi(x) > \operatorname{li}_0(x)$ is known to be below $1.4 \cdot 10^{316}$ (Bays and Hudson, cited in the same exercise).

**Chebyshev's constants.** The elementary method gives constants $A < 1 < B$ but cannot reach $A = B = 1$ alone. The values $A = 1/2$ and $B = 2$ stated by Crandall and Pomerance hold for every $3 \le x \le 10^7$; this was checked by script with a sieve. Lemma 1 also held there, with $\vartheta(10^7)/10^7 = 0.99952$, close to the limit 1 and far below $2 \ln 2 = 1.386$.

**Explicit bounds hold only from a point on.** Rosser and Schoenfeld's lower bound $\pi(x) > x/\ln x$ holds for $x \ge 17$ but fails at $x = 10$, where $\pi(10) = 4 < 4.34$. The bounds on $p_n$ for $n \ge 20$ fail for several $n < 20$. A script checked the bounds of Theorem 5.19 of Shoup for $p_n$ and $\pi(x)$ for all $x \le 10^7$ and all $p_n \le 10^7$.

**Pitfalls.**

- Some authors and software define $\operatorname{li}(x)$ with the integral from 0 (as $\operatorname{li}_0$), which adds about $1.0452$ (Shoup, Section 5.6). Check which one a table uses.
- The theorem is about $x \to \infty$. It gives no bound for a fixed $x$; use the explicit bounds for that.
- The theorem describes averages over long ranges. It does not show that every interval $[x, x + \ln x]$ contains a prime, and that is false.

## History

Gauss conjectured the theorem, in the form $\pi(x) \approx \operatorname{li}(x)$, from counts of primes in blocks of 1000; Crandall and Pomerance date this to 1791, but he published it much later. Legendre conjectured independently that $\pi(x) \approx x/(\ln x - 1.08366)$. Chebyshev proved in the middle of the 19th century that $\pi(x)$ has order $x/\ln x$ (Theorem 1.1.3 of Crandall and Pomerance), and that the constant must be 1 if a limit exists. Riemann's paper of 1859 linked $\pi(x)$ to the complex zeros of $\zeta(s)$ and stated the Riemann hypothesis. Hadamard and de la Vallee Poussin proved the theorem independently in 1896, with the error term of equation (1.2), by showing that $\zeta(s) \ne 0$ on the line $\sigma = 1$. Von Koch showed in 1901 that the Riemann hypothesis is equivalent to $\pi(x) = \operatorname{li}(x) + O(x^{1/2} \ln x)$ (Shoup, Section 5.6). Selberg and Erdos found an elementary proof, with no complex analysis, in 1949. Newman gave a short analytic proof in 1980, and Zagier's account of 1997 is the one followed above. Rosser and Schoenfeld (1962) gave the explicit bounds that are still widely used in the analysis of algorithms.

## References
