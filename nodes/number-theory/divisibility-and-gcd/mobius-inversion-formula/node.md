---
tag: 16ZGJY
kind: theorem
slug: mobius-inversion-formula
name: Möbius inversion formula
aliases:
- Möbius inversion
area: number-theory/divisibility-and-gcd
level: core
summary: If g(n) = sum of f(d) over d | n, then f(n) = sum of mu(d) g(n/d) over d | n.
prereqs: [mobius-function, divisor]
see_also: [dirichlet-convolution, multiplicative-function, totient-divisor-sum, euler-totient, inclusion-exclusion-principle, mobius-sieve, dirichlet-hyperbola-method, prime-number-theorem]
sources:
  - book: isbn:9780387901633
    title: Tom M. Apostol, Introduction to Analytic Number Theory
    locator: Chapter 2, Section 2.7, Dirichlet inverses and the Möbius inversion formula, and Section 2.6, Dirichlet multiplication of arithmetical functions
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Section 16.4, The Möbius inversion formula, and Section 16.5, Further inversion formulae
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 4.9, Phi and Mu (the Möbius inversion principle and its use to count necklaces)
  - url: "https://en.wikipedia.org/wiki/M%C3%B6bius_inversion_formula"
    locator: lead and sections Statement of the formula, Repeated transformations, Multiplicative notation and Generalizations
---

The Möbius inversion formula says that if $g(n) = \sum_{d \mid n} f(d)$ for every positive integer $n$, then $f(n) = \sum_{d \mid n} \mu(d)\, g(n/d)$, and conversely. Here $\mu$ is the [Möbius function](/mobius-function/). In the language of [Dirichlet convolution](/dirichlet-convolution/) it says $g = f * \mathbf{1} \iff f = g * \mu$, because $\mu$ and the constant function $\mathbf{1}$ are inverse to each other. It turns a sum over divisors back into the summand, and it is the number-theoretic form of [inclusion-exclusion](/inclusion-exclusion-principle/): it derives the product formula for [Euler's totient](/euler-totient/), counts irreducible polynomials over finite fields and aperiodic necklaces, and counts coprime pairs.

## Statement

Let $f$ and $g$ be functions from the positive integers to an abelian group, for example the integers or the complex numbers under addition.

**Theorem.** The following are equivalent:

1. $g(n) = \sum_{d \mid n} f(d)$ for every positive integer $n$;
2. $f(n) = \sum_{d \mid n} \mu(d)\, g(n/d)$ for every positive integer $n$.

Both sums run over the positive divisors $d$ of $n$, and $\sum_{d \mid n} \mu(d)\, g(n/d) = \sum_{d \mid n} \mu(n/d)\, g(d)$.

**Convolution form.** With $(f * g)(n) = \sum_{d \mid n} f(d)\, g(n/d)$ and $\mathbf{1}(n) = 1$: $g = f * \mathbf{1}$ if and only if $f = g * \mu$.

**Multiplicative form.** For functions into the nonzero reals or any multiplicative abelian group: $g(n) = \prod_{d \mid n} f(d)$ for all $n$ if and only if $f(n) = \prod_{d \mid n} g(n/d)^{\mu(d)}$ for all $n$.

**Form over the reals.** For functions $F$ and $G$ on $[1, \infty)$: $G(x) = \sum_{n \le x} F(x/n)$ for all $x \ge 1$ if and only if $F(x) = \sum_{n \le x} \mu(n)\, G(x/n)$ for all $x \ge 1$. Hardy and Wright give this in Section 16.5.

## In plain words

Suppose for each number you add up some quantity over all of its divisors, and you are given only those totals. You can get back the quantity for each number by adding and subtracting the totals of the number divided by its prime factors, in the same pattern as counting with overlaps. Divide by one prime and subtract, divide by two different primes and add back, divide by three and subtract again, and so on. Divisions by a square never appear. The pattern of signs is exactly the Möbius function.

## Proof

The proof rests on the divisor sum of the Möbius function, proved on its page: $\sum_{d \mid m} \mu(d) = [m = 1]$.

**From 1 to 2.** Fix $n$. Substitute the formula for $g$:

$$\sum_{d \mid n} \mu(d)\, g(n/d) = \sum_{d \mid n} \mu(d) \sum_{e \mid n/d} f(e).$$

The pairs $(d, e)$ with $d \mid n$ and $e \mid n/d$ are exactly the pairs with $de \mid n$, which are also the pairs with $e \mid n$ and $d \mid n/e$. Exchange the order:

$$= \sum_{e \mid n} f(e) \sum_{d \mid n/e} \mu(d) = \sum_{e \mid n} f(e)\, [n/e = 1] = f(n).$$

**From 2 to 1.** Fix $n$. Substitute the formula for $f$ and write $d = e m$:

$$\sum_{d \mid n} f(d) = \sum_{d \mid n} \sum_{e \mid d} \mu(e)\, g(d/e) = \sum_{m \mid n} g(m) \sum_{e \mid n/m} \mu(e) = \sum_{m \mid n} g(m)\, [m = n] = g(n).$$

The middle step uses that the pairs $(e, m)$ with $em \mid n$ are the pairs with $m \mid n$ and $e \mid n/m$. $\blacksquare$

**The same proof with convolution.** Dirichlet convolution is associative and commutative, $\varepsilon(n) = [n = 1]$ is its identity, and $\mu * \mathbf{1} = \varepsilon$. So $g = f * \mathbf{1}$ gives $g * \mu = f * (\mathbf{1} * \mu) = f$, and $f = g * \mu$ gives $f * \mathbf{1} = g * \varepsilon = g$. Apostol, Section 2.7, proves the formula this way.

The multiplicative form is the same proof written with products and powers. The form over the reals has the same proof, with the pairs $(n, m)$ with $nm \le x$ in place of the pairs with $de \mid n$, and with the identity $\sum_{n \mid k} \mu(n) = [k = 1]$ applied to $k = nm$.

## Consequences

**The totient.** The [divisor sum of the totient](/totient-divisor-sum/), $\sum_{d \mid n} \varphi(d) = n$, inverts to

$$\varphi(n) = \sum_{d \mid n} \mu(d) \frac{n}{d} = n \prod_{p \mid n} \left(1 - \frac{1}{p}\right).$$

For $n = 12$: $12 - 6 - 4 + 2 = 4$. The product appears because only squarefree $d$ contribute.

**Irreducible polynomials.** Over the finite field with $q$ elements, every monic irreducible polynomial of degree $d$ divides $x^{q^n} - x$ exactly when $d \mid n$, and comparing degrees gives $q^n = \sum_{d \mid n} d\, I_q(d)$, where $I_q(d)$ is the number of monic irreducible polynomials of degree $d$. Inversion gives

$$I_q(n) = \frac{1}{n} \sum_{d \mid n} \mu(d)\, q^{n/d}.$$

For $q = 2$ and $n = 4$: $(16 - 4)/4 = 3$, namely $x^4 + x + 1$, $x^4 + x^3 + 1$ and $x^4 + x^3 + x^2 + x + 1$.

**Aperiodic necklaces and Lyndon words.** Each of the $k^n$ words of length $n$ over $k$ letters has a primitive period $d \mid n$, so $k^n = \sum_{d \mid n} d\, L_k(d)$, where $L_k(d)$ is the number of aperiodic necklaces (Lyndon words) of length $d$. The same inversion gives $L_k(n) = \frac{1}{n} \sum_{d \mid n} \mu(d) k^{n/d}$; for $k = 2$ and $n = 6$, $(64 - 8 - 4 + 2)/6 = 9$.

**Cyclotomic polynomials.** $x^n - 1 = \prod_{d \mid n} \Phi_d(x)$, so by the multiplicative form $\Phi_n(x) = \prod_{d \mid n} (x^{n/d} - 1)^{\mu(d)}$. For $n = 6$: $\Phi_6(x) = (x^6 - 1)(x - 1) / \big((x^3 - 1)(x^2 - 1)\big) = x^2 - x + 1$.

**Counting coprime pairs.** Since $[\gcd(i, j) = 1] = \sum_{d \mid \gcd(i, j)} \mu(d)$, the number of pairs $1 \le i, j \le N$ with $\gcd(i, j) = 1$ is $\sum_{d \le N} \mu(d) \lfloor N/d \rfloor^2$. For $N = 10$ it is 63. The same trick evaluates sums such as $\sum_{i, j \le N} \gcd(i, j)$ and, with the [Dirichlet hyperbola method](/dirichlet-hyperbola-method/), sums of [multiplicative functions](/multiplicative-function/).

**The form over the reals.** With $F(x) = 1$ for $x \ge 1$, $G(x) = \lfloor x \rfloor$, so $\sum_{n \le x} \mu(n) \lfloor x/n \rfloor = 1$ for all $x \ge 1$. With $F = \psi$, Chebyshev's function $\psi(x) = \sum_{p^j \le x} \log p$, one gets $G(x) = \log \lfloor x \rfloor!$, so $\psi(x) = \sum_{n \le x} \mu(n) \log \lfloor x/n \rfloor!$; identities of this kind are used in elementary bounds toward the [prime number theorem](/prime-number-theorem/).

**Computation.** Given $g(1), \ldots, g(N)$, the values $f(1), \ldots, f(N)$ follow without $\mu$: set $f \leftarrow g$, and for $d = 1, \ldots, N$ subtract $f(d)$ from $f(m)$ for every multiple $m = 2d, 3d, \ldots \le N$. When $d$ is reached, $f(d)$ is final, since all its proper divisors are smaller. This takes $\sum_{d \le N} \lfloor N/d \rfloor = O(N \log N)$ word operations. Starting from $g(n) = n$ it produces $\varphi(1), \ldots, \varphi(N)$; a [Möbius sieve](/mobius-sieve/) gives $\mu$ itself in $O(N)$.

**Multiplicativity.** If $g = f * \mathbf{1}$, then $f$ is multiplicative if and only if $g$ is, because $\mathbf{1}$ and $\mu$ are multiplicative and convolution keeps multiplicativity.

## Tightness

The equivalence needs the identity for every divisor of $n$, not only for $n$ itself. Knowing $g(n) = \sum_{d \mid n} f(d)$ at a single $n$ says nothing about $f(n)$ alone, since the other values $f(d)$ are free. What the proof uses is the identity at all divisors of $n$, so the theorem holds on any set of positive integers that is closed under taking divisors, for example $\{1, \ldots, N\}$ or the divisors of a fixed $m$.

The sum must run over all divisors. For sums over unitary divisors, or over the divisors in another partial order, the inverse is a different Möbius function: Rota's theory of Möbius functions of partially ordered sets gives the right one in each case, and for the subsets of a finite set ordered by inclusion it is the inclusion-exclusion principle.

## History

August Ferdinand Möbius introduced the function and the inversion formula in 1832, according to the Wikipedia article on the formula. Hardy and Wright give the formula and its variants in Sections 16.4 and 16.5, and Apostol develops it as the statement that $\mu$ is the Dirichlet inverse of $\mathbf{1}$ in Section 2.7. Gian-Carlo Rota extended it to all locally finite partially ordered sets in "On the foundations of combinatorial theory I. Theory of Möbius functions" (Zeitschrift für Wahrscheinlichkeitstheorie und verwandte Gebiete 2, 1964).

## References
