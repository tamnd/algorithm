---
tag: D91P2H
kind: theorem
slug: rational-root-theorem
name: Rational root theorem
aliases:
- rational root test
- rational zero theorem
area: numerical/root-finding
level: intro
summary: Any rational root p/q in lowest terms of an integer polynomial has p dividing the constant term and q dividing the leading coefficient.
prereqs: [euclids-lemma, factor-theorem]
see_also: [gauss-lemma, eisenstein-criterion, polynomial-factorization-over-integers, polynomial-root-finding, factor-theorem, real-root-isolation, quadratic-formula, integer-factorization]
sources:
  - book: isbn:9780471433347
    title: David S. Dummit and Richard M. Foote, Abstract Algebra, third edition, Wiley, 2004
    locator: Section 9.4, Irreducibility criteria, Proposition 11
  - book: "René Descartes, La Géométrie, 1637; English translation by D. E. Smith and M. L. Latham, The Geometry of René Descartes, Dover, 1954"
    locator: Book III, on finding the roots of an equation among the divisors of its last term
---

The rational root theorem limits the rational roots of a polynomial with integer coefficients to a finite, explicit list of fractions. If $s/t$ in lowest terms is a root, the numerator divides the constant term and the denominator divides the leading coefficient. So the rational roots can be found exactly by trying finitely many candidates, with no rounding and no iteration. It is the simplest case of [Gauss's lemma](/gauss-lemma/): a linear factor over $\mathbb{Q}$ can be chosen with integer coefficients.

## Statement

Let $p(x) = a_n x^n + a_{n-1} x^{n-1} + \cdots + a_1 x + a_0$ with $a_i \in \mathbb{Z}$, $n \ge 1$ and $a_n \ne 0$. Let $r = s/t$ with $s, t \in \mathbb{Z}$, $t \ge 1$ and $\gcd(s, t) = 1$. If $p(r) = 0$, then

1. $s \mid a_0$ and $t \mid a_n$;
2. moreover $(t x - s)$ divides $p(x)$ in $\mathbb{Z}[x]$, so for every integer $m$, $(t m - s) \mid p(m)$; in particular $(t - s) \mid p(1)$ and $(t + s) \mid p(-1)$.

**Corollary.** If $p$ is monic ($a_n = 1$), every rational root is an integer and divides $a_0$. If $a_0 \ne 0$, $p$ has at most $2\,d(|a_0|)\,d(|a_n|)$ candidate rational roots, where $d(m)$ is the number of positive divisors of $m$.

Notation on the root-finding pages: a root of $p$ is a value $x^*$ with $p(x^*) = 0$. Here the roots are exact rationals, and "$a \mid b$" means that $b = a k$ for an integer $k$ (so every integer divides $0$, and $0$ divides only $0$).

## In plain words

Suppose a fraction in lowest terms solves an equation whose coefficients are whole numbers. Clear the denominators: multiply the equation through by the denominator to the power $n$. Every term but the last then contains the numerator, so the numerator must divide the last term, which is the constant term times a power of the denominator. Since numerator and denominator share no factor, the numerator divides the constant term. The same argument from the other end shows the denominator divides the leading coefficient. So to find all rational roots, list the divisors, form the fractions, and test each one exactly.

## Proof

*Item 1.* Multiply $p(s/t) = 0$ by $t^n$:
$$a_n s^n + a_{n-1} s^{n-1} t + \cdots + a_1 s t^{n-1} + a_0 t^n = 0.$$
Every term except the last is a multiple of $s$, so $s \mid a_0 t^n$. Since $\gcd(s, t) = 1$, also $\gcd(s, t^n) = 1$, and [Euclid's lemma](/euclids-lemma/) gives $s \mid a_0$. Every term except the first is a multiple of $t$, so $t \mid a_n s^n$, and in the same way $t \mid a_n$. (If $s = 0$, then $a_0 = p(0) = 0$ and $s \mid a_0$ holds; $t = 1$ divides $a_n$.)

*Item 2.* By the [factor theorem](/factor-theorem/) over $\mathbb{Q}$, $p(x) = (x - s/t)\,g(x)$ with $g \in \mathbb{Q}[x]$, so $p(x) = (t x - s)\,h(x)$ with $h = g/t \in \mathbb{Q}[x]$. We show that $h$ has integer coefficients. Write $h(x) = b_{n-1} x^{n-1} + \cdots + b_0$ and compare coefficients:
$$a_n = t\, b_{n-1}, \qquad a_k = t\, b_{k-1} - s\, b_k \ (1 \le k \le n - 1), \qquad a_0 = -s\, b_0 .$$
Let $N$ be the least positive integer with $N h \in \mathbb{Z}[x]$, and suppose $N > 1$; let $\ell$ be a prime dividing $N$. Then $N p = (t x - s)(N h)$, the coefficients $c_k = N b_k$ are integers, and not all are divisible by $\ell$ (otherwise $N/\ell$ would do). The left side $N p$ has all coefficients divisible by $\ell$. Let $j$ be the largest index with $\ell \nmid c_j$. The coefficient of $x^{j+1}$ in $(t x - s)(N h)$ is $t c_j - s c_{j+1}$, and $\ell \mid c_{j+1}$ (or $c_{j+1} = 0$ when $j = n - 1$), so $\ell \mid t c_j$ and hence $\ell \mid t$. Let $i$ be the smallest index with $\ell \nmid c_i$; the coefficient of $x^i$ is $t c_{i-1} - s c_i$ (with $c_{-1} = 0$), so $\ell \mid s c_i$ and $\ell \mid s$. Then $\ell$ divides both $s$ and $t$, which contradicts $\gcd(s, t) = 1$. So $N = 1$ and $h \in \mathbb{Z}[x]$.

Evaluating $p(m) = (t m - s)\,h(m)$ at an integer $m$ gives $(t m - s) \mid p(m)$, since $h(m) \in \mathbb{Z}$. Item 2 also gives item 1 again: $a_n = t\, b_{n-1}$ and $a_0 = -s\, b_0$.

*Corollary.* If $a_n = 1$, then $t \mid 1$, so $t = 1$. The candidates are $\pm s'/t'$ with $s' \mid a_0$, $t' \mid a_n$ positive divisors, at most $2\,d(|a_0|)\,d(|a_n|)$ of them. $\blacksquare$

## Consequences

- **An exact finite test.** For $p(x) = 2x^3 - 3x^2 - 3x + 2$ the candidates are $\pm 1, \pm 2, \pm \tfrac12$. Exact evaluation gives $p(-2) = -20$, $p(-1) = 0$, $p(-\tfrac12) = \tfrac52$, $p(\tfrac12) = 0$, $p(1) = -2$ and $p(2) = 0$, so the roots are $-1, \tfrac12, 2$. Item 2 prunes before evaluating: $p(1) = -2$, and for $-2$ and $-\tfrac12$ the number $t - s$ is $3$, which does not divide $-2$, so both are rejected without evaluating $p$ there.
- **Irrationality.** $x^2 - 2$ has the candidates $\pm 1, \pm 2$, none a root, so $\sqrt 2$ is irrational. In the same way $\sqrt[n]{m}$ is rational only if $m$ is an $n$-th power of an integer.
- **Exact deflation.** After a rational root $s/t$ is found, dividing by $t x - s$ gives an integer quotient (item 2), and the search continues on a polynomial of lower degree with integer coefficients, without rounding. Compare [polynomial deflation](/polynomial-deflation/) in floating point.
- **A first step in factoring.** The linear factors of $p$ over $\mathbb{Q}$ are exactly the $t x - s$ found by the test; complete [factorization over the integers](/polynomial-factorization-over-integers/) handles the factors of higher degree.

## Tightness

- **The conditions are necessary, not sufficient.** For $x^2 - 2$ every candidate satisfies the divisibility conditions of item 1 and none is a root.
- **They cannot be sharpened in general.** For any coprime $s$ and $t \ge 1$, the polynomial $t x - s$ has the root $s/t$ with $s = -a_0$ and $t = a_n$ exactly, so no proper divisor of $a_0$ or $a_n$ will do.
- **Lowest terms are needed.** $2x - 1$ has the root $2/4$, but $2 \nmid -1$; the theorem applies to $1/2$.
- **The integer hypothesis is needed.** Over $\mathbb{Q}$ the coefficients can be rescaled at will, and over a ring without unique factorization, such as $\mathbb{Z}[\sqrt{-5}]$, the argument with Euclid's lemma breaks down. The theorem holds with the same proof over every unique factorization domain and its field of fractions.
- **The list can be long.** The number of candidates grows with the number of divisors of $a_0$ and $a_n$, and finding the divisors needs [integer factorization](/integer-factorization/). For large coefficients it is faster to isolate the real roots numerically ([real root isolation](/real-root-isolation/)) and test only the few fractions near each root, or to factor $p$ over $\mathbb{Z}$.

## History

The search for integer roots among the divisors of the last term of an equation appears in Descartes' La Géométrie (1637, Book III), and the test for rational roots is a standard result of elementary algebra. In modern algebra it is a special case of Gauss's lemma on primitive polynomials (Dummit and Foote, Section 9.4).

## References
