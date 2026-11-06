---
tag: EXMWJN
kind: theorem
slug: totient-divisor-sum
name: Divisor sum property of Euler's totient
aliases:
- Divisor sum property of totient
area: number-theory/divisibility-and-gcd
level: intro
summary: The sum of Euler's totient over all divisors d of n equals n.
prereqs: [euler-totient, divisor, greatest-common-divisor]
see_also: [mobius-inversion-formula, mobius-function, multiplicative-function, primitive-root, cyclic-group, totient-values-up-to-n, farey-sequence, dirichlet-convolution]
sources:
  - book: isbn:9780387901633
    title: Tom M. Apostol, Introduction to Analytic Number Theory
    locator: Chapter 2, Section 2.3, The Euler totient function (the divisor sum of the totient), and Section 2.4, A relation connecting the totient and the Möbius function
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 4.9, Phi and Mu (the proof by reducing the fractions k/n and grouping them by denominator)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter 16, Section 16.1, The function phi(n), and Section 16.2
  - url: "https://en.wikipedia.org/wiki/Euler%27s_totient_function"
    locator: section Divisor sum (the property attributed to Gauss, Disquisitiones Arithmeticae, Article 39)
---

The divisor sum property of [Euler's totient](/euler-totient/) says that for each positive integer $n$, the values $\varphi(d)$ over the positive [divisors](/divisor/) $d$ of $n$ add up to $n$. The reason is a count: the numbers $1, \ldots, n$ fall into classes by their [gcd](/greatest-common-divisor/) with $n$, and the class for each divisor has $\varphi$ of the complementary divisor as its size. By [Möbius inversion](/mobius-inversion-formula/) the identity is equivalent to the product formula $\varphi(n) = n \prod_{p \mid n} (1 - 1/p)$, and it is the counting step in the proof that every prime has a [primitive root](/primitive-root/).

## Statement

Euler's totient $\varphi(m)$, for an integer $m \ge 1$, is the number of integers $k$ with $1 \le k \le m$ and $\gcd(k, m) = 1$. So $\varphi(1) = 1$.

**Theorem.** For every integer $n \ge 1$,

$$\sum_{d \mid n} \varphi(d) = n,$$

where the sum runs over the positive divisors $d$ of $n$.

**Uniqueness.** $\varphi$ is the only function $f$ from the positive integers to the integers with $\sum_{d \mid n} f(d) = n$ for all $n \ge 1$. In the language of [Dirichlet convolution](/dirichlet-convolution/), $\varphi * \mathbf{1} = \mathrm{id}$.

## In plain words

Write down the fractions one over twelve, two over twelve, and so on up to twelve over twelve, and reduce each one to lowest terms. Each reduced fraction has a bottom that divides twelve. For each such bottom, the tops that appear are exactly the numbers below it that share no factor with it, and each of those appears once. The count of those tops is the totient of the bottom.

So the twelve fractions split into groups, one group for each divisor of twelve, and the size of each group is the totient of that divisor. Adding the group sizes gives back twelve.

## Proof

Fix $n \ge 1$, and let $S = \{1, 2, \ldots, n\}$. For each positive divisor $d$ of $n$, let

$$S_d = \{ k \in S : \gcd(k, n) = n/d \}.$$

1. **The $S_d$ split $S$.** For each $k \in S$, $g = \gcd(k, n)$ is a positive divisor of $n$, and $d = n/g$ is the unique divisor with $k \in S_d$. So the sets $S_d$ are disjoint and their union is $S$.
2. **$|S_d| = \varphi(d)$.** Let $g = n/d$. If $k \in S_d$, then $g \mid k$, so $k = g j$ with $1 \le j \le d$ (because $1 \le k \le n = gd$). Also $\gcd(gj, gd) = g \gcd(j, d)$, so $\gcd(k, n) = g$ holds if and only if $\gcd(j, d) = 1$. Hence $k \mapsto k/g$ is a bijection from $S_d$ onto $\{ j : 1 \le j \le d,\ \gcd(j, d) = 1 \}$, which has $\varphi(d)$ elements.
3. **Add.** By steps 1 and 2, $n = |S| = \sum_{d \mid n} |S_d| = \sum_{d \mid n} \varphi(d)$.

**Uniqueness.** If $\sum_{d \mid n} f(d) = n$ for all $n$, then $f(1) = 1$ and $f(n) = n - \sum_{d \mid n, d < n} f(d)$. By strong induction on $n$, $f(n)$ is determined by its values at smaller arguments, so any two such functions agree. $\blacksquare$

**The same proof with fractions.** Step 2 says that the fractions $k/n$, $1 \le k \le n$, in lowest terms, are exactly the fractions $j/d$ with $d \mid n$, $1 \le j \le d$ and $\gcd(j, d) = 1$, each once. This is the proof in Concrete Mathematics, Section 4.9.

**A proof with groups.** In the cyclic group $\mathbb{Z}_n$ under addition, each element generates a subgroup, and for each $d \mid n$ there is exactly one subgroup of order $d$, which is cyclic and has $\varphi(d)$ generators. Counting the elements by the order of the subgroup they generate gives the identity again. See [cyclic group](/cyclic-group/).

## Consequences

**Examples.** For $n = 12$ the divisors are 1, 2, 3, 4, 6 and 12, with totients 1, 1, 2, 2, 2 and 4, and $1 + 1 + 2 + 2 + 2 + 4 = 12$. For $n = 20$, the classes of the proof are:

| $d$ | $\varphi(d)$ | $k \in \{1, \ldots, 20\}$ with $\gcd(k, 20) = 20/d$ |
| --- | --- | --- |
| 1 | 1 | 20 |
| 2 | 1 | 10 |
| 4 | 2 | 5, 15 |
| 5 | 4 | 4, 8, 12, 16 |
| 10 | 4 | 2, 6, 14, 18 |
| 20 | 8 | 1, 3, 7, 9, 11, 13, 17, 19 |

For a prime $p$, the identity reads $\varphi(1) + \varphi(p) = p$, so $\varphi(p) = p - 1$.

- **The product formula.** By the [Möbius inversion formula](/mobius-inversion-formula/), $\sum_{d \mid n} \varphi(d) = n$ is equivalent to $\varphi(n) = \sum_{d \mid n} \mu(d)\, n/d$. Since $\mu(d) = 0$ unless $d$ is a product of distinct primes, the sum factors as $n \prod_{p \mid n} (1 - 1/p)$. For $n = 12$: $12 \cdot \tfrac12 \cdot \tfrac23 = 4$.
- **Multiplicativity.** The identity $\varphi * \mathbf{1} = \mathrm{id}$ with $\mathbf{1}$ and $\mathrm{id}$ [multiplicative](/multiplicative-function/) shows that $\varphi = \mathrm{id} * \mu$ is multiplicative, since the Dirichlet convolution of multiplicative functions is multiplicative.
- **Primitive roots.** In the group of units modulo a prime $p$, of order $p - 1$, let $\psi(d)$ be the number of elements of order $d$. If $\psi(d) > 0$, an element of order $d$ gives $d$ roots of $x^d = 1$, which are all the roots since a polynomial of degree $d$ over a field has at most $d$ roots; among them exactly $\varphi(d)$ have order $d$. So $\psi(d) \le \varphi(d)$ for each $d \mid p - 1$. But $\sum_{d \mid p-1} \psi(d) = p - 1 = \sum_{d \mid p-1} \varphi(d)$, so $\psi(d) = \varphi(d)$ for all $d$, and in particular $\psi(p - 1) = \varphi(p - 1) \ge 1$: a [primitive root](/primitive-root/) exists. See [existence of primitive roots](/primitive-roots-existence/).
- **Sieving the totient.** The recurrence $\varphi(n) = n - \sum_{d \mid n, d < n} \varphi(d)$ computes all of $\varphi(1), \ldots, \varphi(N)$ in $O(N \log N)$ word operations by subtracting $\varphi(d)$ from each multiple of $d$; faster sieves are on the page [totient values up to n](/totient-values-up-to-n/).
- **Farey sequences.** Summing step 2 over all $n \le N$ counts the reduced fractions in $(0, 1]$ with denominator at most $N$; this number is $\sum_{d \le N} \varphi(d)$, the length of the [Farey sequence](/farey-sequence/) of order $N$ minus one.

## History

The property is attributed to Gauss, who proved it in Article 39 of the Disquisitiones Arithmeticae (1801), as recorded in the Wikipedia article on the totient. Apostol gives it in Section 2.3 and uses it with Möbius inversion to derive the product formula. Hardy and Wright treat the totient and its properties in Sections 16.1 and 16.2.

## References
