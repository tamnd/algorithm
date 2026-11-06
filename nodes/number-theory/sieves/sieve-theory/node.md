---
tag: RWWWWR
kind: concept
slug: sieve-theory
name: Sieve theory
aliases:
- analytic sieve methods
- sieve methods in analytic number theory
area: number-theory/sieves
level: research
summary: Methods that estimate how many elements of a set of integers have no prime factor below z, from how the set is spread over residue classes. They give upper bounds for twin primes and similar sets.
prereqs: [sieve-of-eratosthenes, inclusion-exclusion-principle, mobius-function]
see_also: [brun-sieve, selberg-sieve, large-sieve-inequality, legendre-phi-function, buchstab-function, prime-gaps, smooth-number, prime-number-theorem]
sources:
  - book: isbn:9780821849705
    title: John Friedlander and Henryk Iwaniec, Opera de Cribro, American Mathematical Society Colloquium Publications 57, 2010
    locator: Chapter 4, Sieve of Eratosthenes-Legendre (p. 31); Chapter 6, Brun's sieve (pp. 55 to 88); Chapter 7, Selberg's sieve (pp. 89 to 138); Chapter 9, The large sieve (pp. 151 to 172); Chapter 16, Asymptotic sieve and the parity principle (pp. 331 to 343)
  - book: isbn:9780821836330
    title: Henryk Iwaniec and Emmanuel Kowalski, Analytic Number Theory, American Mathematical Society Colloquium Publications 53, 2004
    locator: Chapter 6, Elementary sieve methods (pp. 153 to 167), and Chapter 7, Bilinear forms and the large sieve (pp. 169 to 195)
  - book: isbn:9780821898543
    title: Gérald Tenenbaum, Introduction to Analytic and Probabilistic Number Theory, third edition, American Mathematical Society, Graduate Studies in Mathematics 163, 2015
    locator: Part I, Chapter 4, Sieve methods (pp. 67 to 109)
  - book: isbn:9780521612753
    title: Alina Carmen Cojocaru and M. Ram Murty, An Introduction to Sieve Methods and Their Applications, London Mathematical Society Student Texts 66, Cambridge University Press, 2006
    locator: Chapter 5, The sieve of Eratosthenes (p. 63); Chapter 6, Brun's sieve (p. 80); Chapter 7, Selberg's sieve (p. 113); Chapter 8, The large sieve (p. 135)
  - paper: doi:10.4007/annals.2014.179.3.7
    title: Yitang Zhang, Bounded gaps between primes, Annals of Mathematics 179(3), 2014
    locator: pages 1121 to 1174 (a sieve with a level of distribution beyond x^(1/2) for smooth moduli)
  - paper: doi:10.4007/annals.2015.181.1.7
    title: James Maynard, Small gaps between primes, Annals of Mathematics 181, 2015
    locator: pages 383 to 413 (multidimensional Selberg weights)
  - paper: doi:10.2307/121034
    title: John Friedlander and Henryk Iwaniec, The polynomial X^2 + Y^4 captures its primes, Annals of Mathematics 148(3), 1998
    locator: the asymptotic sieve that gets past the parity barrier
---

Sieve theory is the part of analytic number theory that estimates the size of a sifted set: the number of elements of a finite set $\mathcal{A}$ of integers that have no prime factor below a bound $z$. It takes as input only how $\mathcal{A}$ is spread over residue classes modulo squarefree numbers $d$, and it turns that information into upper and lower bounds. It grew from the [sieve of Eratosthenes](/sieve-of-eratosthenes/) and Legendre's formula, and its main tools are [Brun's sieve](/brun-sieve/), [Selberg's sieve](/selberg-sieve/) and the [large sieve](/large-sieve-inequality/). It gives upper bounds of the right order for twin primes, Goldbach representations and primes in short intervals, and results such as Chen's theorem and bounded gaps between primes, but by itself it cannot tell primes from products of two primes: this is the parity problem.

## In plain words

The sieve of Eratosthenes removes the multiples of small primes from a list and keeps what is left. Sieve theory asks a softer question: about how many numbers are left, when the list is not the plain list of integers but, say, the numbers n for which both n and n plus 2 must avoid small prime factors.

You usually know, for each small number d, roughly how many members of the list are multiples of d. Adding and subtracting these counts in the right way gives the number left, but the small errors in each count pile up when there are too many terms. Each sieve method is a way to choose which terms to keep, or which weights to give them, so that the main count stays and the errors stay small. The answers are usually bounds rather than exact counts.

## The idea

**The setup.** Let $\mathcal{A}$ be a finite sequence of integers, $\mathcal{P}$ a set of primes, $z \ge 2$, and $P(z) = \prod_{p \in \mathcal{P},\, p < z} p$. The sifting function is

$$S(\mathcal{A}, \mathcal{P}, z) = \#\{ a \in \mathcal{A} : \gcd(a, P(z)) = 1 \}.$$

For squarefree $d$ write $\mathcal{A}_d = \#\{a \in \mathcal{A} : d \mid a\}$, and assume the model

$$\mathcal{A}_d = g(d)\, X + r_d \qquad (d \mid P(z)),$$

with $X$ an approximation to $|\mathcal{A}|$, a multiplicative density $g$ with $0 \le g(p) < 1$, and remainders $r_d$ that are small on average. For the integers in an interval of length $X$, $g(d) = 1/d$ and $|r_d| \le 1$. For $\mathcal{A} = \{n(n+2) : n \le x\}$, which is the twin prime problem, $g(2) = 1/2$, $g(p) = 2/p$ for odd $p$ and $|r_d| \le 2^{\omega(d)}$, where $\omega(d)$ counts the prime factors of $d$.

**Legendre's identity.** By the [Möbius function](/mobius-function/) identity $\sum_{d \mid m} \mu(d) = [m = 1]$,

$$S(\mathcal{A}, \mathcal{P}, z) = \sum_{d \mid P(z)} \mu(d)\, \mathcal{A}_d = X \prod_{p \mid P(z)} (1 - g(p)) + \sum_{d \mid P(z)} \mu(d)\, r_d.$$

The main term $X\,W(z)$, with $W(z) = \prod_{p \mid P(z)}(1 - g(p))$, is what one expects. But the error sum has $2^{\pi(z)}$ terms, so the identity is useful only for $z$ about $\log X$. This is the sieve of Eratosthenes-Legendre and, for $\mathcal{A} = \{1, \ldots, \lfloor x \rfloor\}$, it is [Legendre's phi function](/legendre-phi-function/).

**Truncation and weights.** Every sieve method replaces $\mu(d)$ by weights $\lambda_d$ supported on $d \le D$, the level of the sieve, such that $\sum_{d \mid m} \lambda_d$ is at least (or at most) $[m = 1]$ for every $m \mid P(z)$. Summing over $\mathcal{A}$ gives $S \le X \sum_d \lambda_d g(d) + \sum_{d \le D} |\lambda_d r_d|$, and the remainder now has few terms. Brun chose $\lambda_d = \mu(d)$ cut off by the number of prime factors of $d$; Selberg chose $\lambda$ as a square $(\sum_{d \mid m} \rho_d)^2$ and optimized the quadratic form; the large sieve works on the dual side, with exponential sums.

**Dimension.** If $g(p) \approx \kappa / p$ on average, the sieve has dimension $\kappa$. Primes in an interval are a sieve of dimension 1, twin primes and Goldbach of dimension 2. For dimension $\kappa$, $W(z) \asymp (\log z)^{-\kappa}$.

**Level of distribution.** The level $D$ is how far the remainders $r_d$ stay small on average. For integers in an interval, any $D$ up to about $X$ works; for the primes in progressions, the Bombieri-Vinogradov theorem gives $D = x^{1/2 - \varepsilon}$ on average over moduli, and Zhang went beyond $x^{1/2}$ for smooth moduli.

**The fundamental lemma.** If $z$ is small compared with the level, $s = \log D / \log z \to \infty$, then $S(\mathcal{A}, \mathcal{P}, z) = X W(z) (1 + O(e^{-s}))$ plus the remainder: the sifted count is the expected one. For $z$ comparable to the level, only bounds remain, given by the functions $F$ and $f$ of the linear sieve and related to the [Buchstab function](/buchstab-function/).

**The parity problem.** Selberg showed that sieve information alone cannot separate numbers with an even number of prime factors from numbers with an odd number. A sieve lower bound for primes is therefore impossible without extra input, and the best upper bound loses a factor of 2 in dimension 1. Chen's theorem (every large even number is $p + P_2$, with $P_2$ having at most two prime factors) and the result of Friedlander and Iwaniec that $X^2 + Y^4$ takes infinitely many prime values both use extra bilinear information to get past this.

## Examples

- **Legendre's sieve.** Sift $\{1, \ldots, 100\}$ by 2, 3, 5 and 7. The 16 terms $\mu(d) \lfloor 100/d \rfloor$ sum to $S = 22$: the number 1 and the 21 primes from 11 to 97. The main term is $100 \cdot \frac12 \cdot \frac23 \cdot \frac45 \cdot \frac67 = 22.86$.
- **A twin prime sieve.** Take $x = 10^6$ and sift $\{n(n+2) : n \le x\}$ by the ten primes below 30. Exactly $33185$ values of $n$ survive, and the main term is $x \cdot \frac12 \prod_{3 \le p \le 29}(1 - 2/p) = 33186.8$: here $z$ is tiny compared with $x$, and the fundamental lemma regime holds. The true number of twin prime pairs with $p + 2 \le 10^6$ is $8169$; the survivors include many $n$ whose $n$ or $n + 2$ has only prime factors above 29 but is not prime.
- **Bounds for primes in an interval.** In $(10^9, 10^9 + 10^6]$ there are $48155$ primes. Sifting by the primes below $z = 500$ leaves $89461$ numbers. Selberg's sieve with $z = 500$ gives the upper bound $132459$ plus a remainder that is at most $10426$ (and is in fact about $9$); the large sieve in its sharp form gives $154665$ at its best parameter $Q = 290$. All three bounds are of the right order, $N / \log N$, but not asymptotic.
- **Twin primes.** Brun's sieve gives $\pi_2(x) = O(x / \log^2 x)$ and so the convergence of $\sum 1/p$ over twin primes; the conjectured count, by Hardy and Littlewood, is $\sim 2 C_2\, x / \log^2 x$ with $C_2 = 0.66016\ldots$, which predicts about $8247$ pairs up to $10^6$ in its integral form, against the true $8169$.

## Where it is used

- **Upper bounds of the right order** for twin primes, prime $k$-tuples, Goldbach representations, primes in short intervals and in arithmetic progressions (the Brun-Titchmarsh inequality).
- **Almost primes.** Lower bound sieves show that many values of a polynomial have few prime factors, as in Chen's theorem, where $p + 2$ has at most two prime factors for infinitely many primes $p$.
- **Gaps between primes.** The Goldston-Pintz-Yıldırım method, Zhang's bounded gaps theorem and Maynard's multidimensional sieve all start from Selberg type weights; see [prime gaps](/prime-gaps/).
- **Large sieve applications.** The Bombieri-Vinogradov theorem, bounds on the least quadratic non-residue on average, and results in arithmetic geometry and group theory.
- **Computation.** Exact sifting functions drive the [Meissel-Lehmer algorithm](/meissel-lehmer-algorithm/); the distribution of numbers without small or large prime factors, described by the [Buchstab function](/buchstab-function/) and the [Dickman function](/dickman-function/), governs the cost of factoring algorithms.

## References
