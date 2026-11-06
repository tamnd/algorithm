---
tag: R9GF09
kind: technique
slug: selberg-sieve
name: Selberg's sieve
aliases:
- Selberg upper bound sieve
- Selberg lambda-squared sieve
- Lambda-squared sieve
area: number-theory/sieves
level: research
summary: Bound the indicator of sifted numbers by a square of a short divisor sum with lambda_1 = 1, then choose the lambda_d to minimize the main term, a quadratic form whose minimum is 1/G(z).
prereqs: [sieve-theory, mobius-function, mobius-inversion, euler-totient]
see_also: [brun-sieve, large-sieve-inequality, buchstab-function, prime-gaps, dirichlet-convolution, legendre-phi-function, primes-in-range, chinese-remainder-theorem]
sources:
  - book: isbn:9780821849705
    title: John Friedlander and Henryk Iwaniec, Opera de Cribro, American Mathematical Society Colloquium Publications 57, 2010
    locator: Chapter 7, Selberg's sieve (pp. 89 to 138)
  - book: isbn:9780821836330
    title: Henryk Iwaniec and Emmanuel Kowalski, Analytic Number Theory, American Mathematical Society Colloquium Publications 53, 2004
    locator: Chapter 6, Elementary sieve methods (pp. 153 to 167)
  - book: isbn:9780521612753
    title: Alina Carmen Cojocaru and M. Ram Murty, An Introduction to Sieve Methods and Their Applications, London Mathematical Society Student Texts 66, Cambridge University Press, 2006
    locator: Chapter 7, Selberg's sieve (p. 113)
  - book: isbn:9780821898543
    title: Gérald Tenenbaum, Introduction to Analytic and Probabilistic Number Theory, third edition, American Mathematical Society, Graduate Studies in Mathematics 163, 2015
    locator: Part I, Chapter 4, Sieve methods (pp. 67 to 109)
  - paper: doi:10.4007/annals.2015.181.1.7
    title: James Maynard, Small gaps between primes, Annals of Mathematics 181, 2015
    locator: pages 383 to 413 (Selberg weights in several variables for prime k-tuples)
  - paper: doi:10.4007/annals.2014.179.3.7
    title: Yitang Zhang, Bounded gaps between primes, Annals of Mathematics 179(3), 2014
    locator: pages 1121 to 1174 (Goldston-Pintz-Yildirim weights with a level of distribution beyond one half)
---

Selberg's sieve gives upper bounds for the number of elements of a set $\mathcal{A}$ with no prime factor below $z$. Instead of truncating inclusion-exclusion as [Brun's sieve](/brun-sieve/) does, it uses the trivial inequality $[n = 1] \le \big(\sum_{d \mid n} \lambda_d\big)^2$, valid for any real numbers $\lambda_d$ with $\lambda_1 = 1$, and then chooses the $\lambda_d$, supported on $d < z$, to make the resulting main term as small as possible. The main term is a positive definite quadratic form in the $\lambda_d$; a diagonalizing change of variables and Cauchy-Schwarz show that its minimum is $1/G(z)$ with $G(z) = \sum_{d < z} \mu^2(d)/h(d)$, and the optimal weights satisfy $|\lambda_d| \le 1$, which keeps the remainder under control. The method gives the Brun-Titchmarsh bound $\pi(x + y) - \pi(x) \le (2 + o(1))\, y/\log y$, the right order for twin primes and other prime patterns, and its multidimensional form is the engine behind the bounded gaps theorems of Zhang and Maynard.

## In plain words

A sieve upper bound needs a weight that is at least 1 on the numbers you want to count and at least 0 on everything else. A square is never negative, so the square of any short sum over divisors works, as long as the sum equals 1 at the number 1.

That leaves a free choice of the coefficients in the sum. Selberg's idea is to pick them so that the total weight, summed over the whole set, is as small as possible. The total is a quadratic expression in the coefficients, so minimizing it is the same as finding the lowest point of a bowl, which can be done exactly. The minimum has a clean formula, and the best coefficients turn out to be small, so the errors they bring in stay small too.

## When it applies

- You want an upper bound for $S(\mathcal{A}, z) = \#\{a \in \mathcal{A} : \gcd(a, P(z)) = 1\}$, where $P(z)$ is the product of the sifting primes below $z$.
- For squarefree $d \mid P(z)$, $\mathcal{A}_d = \#\{a \in \mathcal{A} : d \mid a\} = g(d) X + r_d$ with $g$ multiplicative and $0 < g(p) < 1$ for the sifting primes.
- You control $\sum_{d < z^2} 3^{\omega(d)} |r_d|$: the level of distribution must reach $D = z^2$.
- An upper bound that is right up to a constant factor is enough. For lower bounds Selberg's sieve alone gives nothing (a square is never negative); one combines it with Buchstab's identity or uses a combinatorial sieve.

## The template

**Step 1: the inequality.** For any reals $\lambda_d$ with $\lambda_1 = 1$ and $\lambda_d = 0$ unless $d \mid P(z)$ and $d < z$,

$$S(\mathcal{A}, z) \le \sum_{a \in \mathcal{A}} \Big( \sum_{d \mid \gcd(a, P(z))} \lambda_d \Big)^2 = \sum_{d_1, d_2} \lambda_{d_1} \lambda_{d_2}\, \mathcal{A}_{[d_1, d_2]} = X\, Q(\lambda) + R(\lambda),$$

where $[d_1, d_2]$ is the least common multiple, $Q(\lambda) = \sum_{d_1, d_2} \lambda_{d_1} \lambda_{d_2}\, g([d_1, d_2])$ and $R(\lambda) = \sum_{d_1, d_2} \lambda_{d_1} \lambda_{d_2}\, r_{[d_1, d_2]}$.

**Step 2: diagonalize.** Since $g$ is multiplicative and $d_1, d_2$ are squarefree, $g([d_1, d_2]) = g(d_1) g(d_2) / g((d_1, d_2))$. Define $h$ multiplicative on squarefree numbers by $h(p) = (1 - g(p))/g(p)$, so that $1/g(m) = \prod_{p \mid m}(1 + h(p)) = \sum_{e \mid m} h(e)$. Then

$$Q(\lambda) = \sum_{d_1, d_2} \lambda_{d_1} g(d_1)\, \lambda_{d_2} g(d_2) \sum_{e \mid (d_1, d_2)} h(e) = \sum_{e} h(e)\, y_e^2, \qquad y_e = \sum_{d :\, e \mid d} \lambda_d\, g(d).$$

The new variables $y_e$ are supported on $e < z$, $e \mid P(z)$, and by [Möbius inversion](/mobius-inversion/) over multiples, $\lambda_d g(d) = \sum_{e :\, d \mid e} \mu(e/d)\, y_e$. The constraint $\lambda_1 = 1$ becomes $\sum_e \mu(e)\, y_e = 1$.

**Step 3: minimize.** By Cauchy-Schwarz,

$$1 = \Big( \sum_{e < z} \mu(e)\, y_e \Big)^2 \le \Big( \sum_{e < z} \frac{\mu^2(e)}{h(e)} \Big) \Big( \sum_{e} h(e)\, y_e^2 \Big) = G(z)\, Q(\lambda), \qquad G(z) = \sum_{\substack{e < z \\ e \mid P(z)}} \frac{\mu^2(e)}{h(e)},$$

so $Q(\lambda) \ge 1/G(z)$, with equality for $y_e = \mu(e)/(h(e)\, G(z))$. Going back,

$$\lambda_d = \frac{\mu(d)}{g(d)\, G(z)} \sum_{\substack{e < z,\ e \mid P(z) \\ d \mid e}} \frac{\mu^2(e)}{h(e)}.$$

**Step 4: the weights are small.** Write $e = d m$ with $(m, d) = 1$ and let $G_d(y) = \sum_{m < y,\ (m, d) = 1,\ m \mid P(z)} \mu^2(m)/h(m)$. Then $\lambda_d = \mu(d)\, G_d(z/d) / (g(d) h(d)\, G(z))$. Every $e < z$ of the form $k m$ with $k \mid d$ and $m < z/d$ coprime to $d$ is counted in $G(z)$, so

$$G(z) \ge \sum_{k \mid d} \frac{1}{h(k)}\, G_d(z/d) = \prod_{p \mid d} \frac{1}{1 - g(p)}\, G_d(z/d) = \frac{G_d(z/d)}{g(d) h(d)},$$

since $1 + 1/h(p) = 1/(1 - g(p))$ and $g(p) h(p) = 1 - g(p)$. Hence $|\lambda_d| \le 1$.

**Step 5: the result.** With these weights,

$$S(\mathcal{A}, z) \le \frac{X}{G(z)} + \sum_{\substack{d < z^2 \\ d \mid P(z)}} 3^{\omega(d)} |r_d|,$$

because $|\lambda_{d_1} \lambda_{d_2}| \le 1$ and each squarefree $d$ is the least common multiple of exactly $3^{\omega(d)}$ ordered pairs.

**Step 6: bound $G(z)$ from below.** For $g(d) = 1/d$ (integers in an interval), $h = \varphi$ and $\mu^2(d)/\varphi(d) = d^{-1} \sum_{k :\, \mathrm{rad}(k) \mid d} k^{-1}$. Writing each $n < z$ as $n = \mathrm{rad}(n) \cdot (n / \mathrm{rad}(n))$ shows $G(z) \ge \sum_{n < z} 1/n \ge \log z$. In dimension $\kappa$ one gets $G(z) \asymp (\log z)^\kappa$.

## Classic examples

- **The weights for $z = 6$.** With $g(d) = 1/d$ and sifting primes 2, 3, 5, the squarefree $e < 6$ are 1, 2, 3, 5, with $\varphi(e) = 1, 1, 2, 4$, so $G = 1 + 1 + \frac12 + \frac14 = \frac{11}{4}$. Step 3 gives $\lambda_1 = 1$, $\lambda_2 = -\frac{8}{11}$, $\lambda_3 = -\frac{6}{11}$, $\lambda_5 = -\frac{5}{11}$, all of absolute value at most 1. The square $(\sum_{d \mid n} \lambda_d)^2$ equals 1 when $\gcd(n, 30) = 1$, equals 0 when $n$ is divisible by 3 and 5 but not 2, and takes the values $\frac{4}{121}, \frac{9}{121}, \frac{25}{121}, \frac{36}{121}, \frac{64}{121}$ in the other cases. The quadratic form is exactly $Q = \frac{4}{11} = 1/G$. Summed over $n \le 3000$ the weights give $3000 \cdot \frac{4}{11} = 1090.9$, an upper bound for the 800 integers up to 3000 coprime to 30. The loss against the density $\frac{4}{15}$ comes from the low level $z^2 = 36$.
- **Primes in a short interval.** For the $10^6$ integers in $(10^9, 10^9 + 10^6]$ and $z = 500$: $G(500) = 7.5495$, the main term is $10^6/G = 132459$, the crude remainder bound $(\sum_d |\lambda_d|)^2$ is $10426$, and the bound is $142885$. The exact weighted sum is $132468.1$, so the true remainder is only about 9. There are $89461$ integers in the interval with no prime factor below 500 and $48155$ primes. Numerically $G(z) - \log z$ is about $1.333$ for $z$ from $10^4$ to $10^6$ ($G = 10.5433, 12.8455, 15.1481$).
- **Brun-Titchmarsh.** For any interval of length $y$, $X = y$, $|r_d| \le 1$, and the remainder is at most $(\sum_{d < z} |\lambda_d|)^2 \le z^2$. Taking $z = y^{1/2}/\log y$ gives $\pi(x + y) - \pi(x) \le (2 + o(1))\, y / \log y$, uniformly in $x$. The same argument in an arithmetic progression gives the Brun-Titchmarsh inequality for $\pi(x; q, a)$. The constant 2 is the limit of the method: Selberg's examples related to the parity problem show that sieve information alone cannot give a constant below 2 here.
- **Twin primes.** For $\mathcal{A} = \{n(n+2) : n \le x\}$, $g(p) = 2/p$ for odd $p$, and $G(z)$ grows like $(\log z)^2 / (4 C_2)$, where $C_2 = 0.66016\ldots$ is the twin prime constant. With $z$ just below $x^{1/2}$ this gives $\pi_2(x) \le (16 C_2 + o(1))\, x/\log^2 x$, which is 8 times the conjectured Hardy-Littlewood count $2 C_2\, x/\log^2 x$. Sifting the shifted primes $\{p + 2\}$ instead, with the Bombieri-Vinogradov theorem as the level of distribution, lowers the factor to 4.
- **Bounded gaps.** Goldston, Pintz and Yıldırım used weights $\big(\sum_{d \mid (n+h_1)\cdots(n+h_k)} \lambda_d\big)^2$ with $\lambda_d$ a smoothed version of Selberg's choice, and detected primes among $n + h_i$ by comparing two weighted sums. Zhang pushed the level of distribution past $x^{1/2}$ for smooth moduli to get a bounded gap, below $7 \cdot 10^7$, and Maynard's weights $\lambda_{d_1, \ldots, d_k}$ with one divisor variable per linear form gave gaps of at most 600 without that input; see [prime gaps](/prime-gaps/).

## Variations

- **Smoothed weights.** Replacing the exact optimum by $\lambda_d = \mu(d)\, F(\log(z/d)/\log z)$ for a smooth $F$ loses little and makes the weights easy to sum; this form is the one used in the Goldston-Pintz-Yıldırım method.
- **Multidimensional weights.** Maynard's sieve optimizes $\lambda_{d_1, \ldots, d_k}$ for $k$ linear forms at once, which reduces the problem of finding many primes among $n + h_1, \ldots, n + h_k$ to an eigenvalue problem for an integral operator.
- **Selberg's lower bound sieve.** Combining the upper bound with the Buchstab identity $S(\mathcal{A}, z) = S(\mathcal{A}, w) - \sum_{w \le p < z} S(\mathcal{A}_p, p)$ gives lower bounds; this is how the linear sieve functions $F$ and $f$ arise.
- **Duality with the large sieve.** The minimum $1/G(z)$ is the same quantity that appears in the denominator of the arithmetic [large sieve](/large-sieve-inequality/), $L = \sum_{q \le Q} \mu^2(q) \prod_{p \mid q} \omega(p)/(p - \omega(p))$; the two methods give comparable bounds by dual arguments.
- **Sieving with weights.** One may put arbitrary nonnegative weights on the elements of $\mathcal{A}$; the derivation is unchanged.

## Pitfalls

- **Level versus support.** Weights supported on $d < z$ need the level of distribution $z^2$, not $z$: the products $[d_1, d_2]$ go up to $z^2$. Choosing $z$ larger than the square root of the level makes the remainder dominate.
- **Mixing up $g$ and $h$.** The diagonalizing function is $h(p) = (1 - g(p))/g(p)$, so $h = \varphi$ when $g(d) = 1/d$; using $1/g$ instead gives a wrong $G(z)$.
- **No lower bounds.** A square cannot be pushed below zero, so the method by itself never shows that a sifted set is nonempty.
- **Expecting asymptotics.** Even with perfect remainders, the bound is $X/G(z)$, which is twice the truth for primes in an interval: the factor is a real limit of sieve methods, not an artifact of the proof.
- **Ignoring the dependence on $\omega(p)$.** For sets where $g(p) = \omega(p)/p$ with $\omega(p)$ large for some $p$, the condition $g(p) < 1$ fails and those primes must be removed from the sieve.

## Exercises

1. Verify $\lambda_2 = -\frac{8}{11}$, $\lambda_3 = -\frac{6}{11}$, $\lambda_5 = -\frac{5}{11}$ for $z = 6$, and check that $Q(\lambda) = \frac{4}{11}$ by expanding $\sum_{d_1, d_2} \lambda_{d_1}\lambda_{d_2}/[d_1, d_2]$.
2. Show that for $g(d) = 1/d$ the optimal $\lambda_d$ equals $\mu(d)\, \frac{d}{\varphi(d)}\, G_d(z/d)/G(z)$.
3. Derive $\pi(x + y) - \pi(x) \le (2 + o(1))\, y/\log y$ from Step 5 and Step 6.

## References
