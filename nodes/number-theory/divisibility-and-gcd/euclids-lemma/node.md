---
tag: ZE04R4
kind: theorem
slug: euclids-lemma
name: Euclid's lemma
aliases:
- Euclid's first theorem
- prime divides product lemma
area: number-theory/divisibility-and-gcd
level: core
summary: If a prime p divides ab, then p divides a or p divides b.
prereqs: [prime-number, divisibility, bezouts-identity]
see_also: [fundamental-theorem-of-arithmetic, coprime-integers, greatest-common-divisor, euclidean-domain, multiplicative-group-modulo-n, divisor]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.1, Elementary number-theoretic notions (the theorem that a prime dividing ab divides a or b, and unique factorization)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter 1 (Euclid's first theorem and the statement of the fundamental theorem) and Chapter 2 (its proof)
  - book: isbn:9780387973296
    title: Kenneth Ireland and Michael Rosen, A Classical Introduction to Modern Number Theory, second edition
    locator: Chapter 1, Sections 1.1 and 1.3 (the lemma in Z and in a principal ideal domain)
  - url: "https://mathcs.clarku.edu/~djoyce/java/elements/bookVII/propVII30.html"
    locator: Euclid's Elements, Book VII, Proposition 30, in the edition of D. E. Joyce
---

Euclid's lemma says that a [prime number](/prime-number/) that [divides](/divisibility/) a product of two integers divides at least one of the two factors. It is the property that sets primes apart from composite numbers, since $6 \mid 4 \cdot 9$ while $6 \nmid 4$ and $6 \nmid 9$. The lemma is the key step of the uniqueness part of the [fundamental theorem of arithmetic](/fundamental-theorem-of-arithmetic/). Its usual proof uses [Bézout's identity](/bezouts-identity/), and a second proof below needs only division with remainder.

## Statement

**Theorem (Euclid's lemma).** Let $p$ be a prime number and let $a, b$ be integers. If $p \mid ab$, then $p \mid a$ or $p \mid b$.

**Corollary (several factors).** If $p$ is prime and $p \mid a_1 a_2 \cdots a_k$ for some $k \ge 1$, then $p \mid a_i$ for some $i$.

**Converse.** Let $n > 1$ be an integer such that for all integers $a, b$, $n \mid ab$ implies $n \mid a$ or $n \mid b$. Then $n$ is prime.

**Generalization (Gauss's lemma).** For integers $n, a, b$: if $n \mid ab$ and $\gcd(n, a) = 1$, then $n \mid b$. Euclid's lemma is the case where $n = p$ is prime, because for a prime $p$, either $p \mid a$ or $\gcd(p, a) = 1$.

The statement allows $a$ or $b$ to be zero or negative. If $a = 0$, then $p \mid a$ and there is nothing to prove.

## In plain words

A prime number cannot be split into smaller whole factors. The lemma says that because of this, a prime that goes into a product must go into one of the two numbers that were multiplied. It cannot take a piece from one factor and a piece from the other, because it has no pieces.

A number that is not prime can do exactly that. Six goes into four times nine, which is thirty-six, but six goes into neither four nor nine: the two comes from the four and the three comes from the nine. The lemma is what makes the prime factors of a number unique.

## Proof

**Proof by Bézout's identity.** Assume $p \mid ab$ and $p \nmid a$. The positive divisors of $p$ are $1$ and $p$, and $p$ does not divide $a$, so $\gcd(p, a) = 1$. By [Bézout's identity](/bezouts-identity/) there are integers $x, y$ with $px + ay = 1$. Multiply by $b$:

$$b = pbx + (ab)y.$$

The first term is a multiple of $p$, and the second term is a multiple of $p$ because $p \mid ab$. So $p \mid b$. $\square$

The same argument with $n$ in place of $p$ proves Gauss's lemma: from $nx + ay = 1$ we get $b = nbx + aby$, and $n$ divides both terms.

**A proof that needs only division with remainder.** Assume $p \mid ab$ and $p \nmid a$; we show $p \mid b$. If $b = 0$ this is true, so let $b \ne 0$. Let

$$S = \{ n \in \mathbb{Z} : n \ge 1 \text{ and } p \mid nb \}.$$

Both $p$ and $|a|$ are in $S$ ($|a| \ge 1$ because $p \nmid a$ excludes $a = 0$). By the well-ordering principle, $S$ has a least element $m$.

*Step 1: $m$ divides each element of $S$.* Let $n \in S$, and write $n = qm + r$ with $0 \le r < m$. Then $rb = nb - q(mb)$, and $p$ divides $nb$ and $mb$, so $p \mid rb$. If $r \ge 1$, then $r \in S$ and $r < m$, against the choice of $m$. So $r = 0$ and $m \mid n$.

*Step 2: $m = 1$.* By step 1, $m \mid p$ and $m \mid |a|$. Since $p$ is prime and $m \ge 1$, $m = 1$ or $m = p$. If $m = p$, then $p \mid |a|$, so $p \mid a$, which is false. So $m = 1$.

*Step 3.* Since $1 \in S$, $p \mid 1 \cdot b = b$. $\square$

**Proof of the corollary.** By induction on $k$. For $k = 1$ there is nothing to prove. For $k \ge 2$, write $a_1 \cdots a_k = (a_1 \cdots a_{k-1}) \cdot a_k$. By the lemma, $p \mid a_k$ or $p \mid a_1 \cdots a_{k-1}$, and in the second case the induction hypothesis gives an $i \le k - 1$ with $p \mid a_i$. $\square$

**Proof of the converse.** Let $n > 1$ be composite, so $n = ab$ with $1 < a, b < n$. Then $n \mid ab$, but $n \nmid a$ and $n \nmid b$, because a positive multiple of $n$ is at least $n$. So a composite $n$ does not have the property, and an $n > 1$ that has it is prime. $\blacksquare$

## Consequences

- **Uniqueness of prime factorization.** If $p_1 \cdots p_r = q_1 \cdots q_s$ with all factors prime, then $p_1$ divides some $q_j$ by the corollary, so $p_1 = q_j$, since a prime's only divisor greater than $1$ is itself. Cancel and repeat. This is the uniqueness half of the [fundamental theorem of arithmetic](/fundamental-theorem-of-arithmetic/), and through it the description of all [divisors](/divisor/) of $n$.
- **Prime powers.** If $p \mid a^k$ then $p \mid a$. For example, $\sqrt 2$ is irrational: from $a^2 = 2b^2$ in lowest terms, $2 \mid a^2$ gives $2 \mid a$, then $4 \mid 2b^2$ gives $2 \mid b$, against $\gcd(a, b) = 1$.
- **Arithmetic modulo a prime.** If $ab \equiv 0 \pmod p$ then $a \equiv 0$ or $b \equiv 0$. So the integers modulo $p$ have no zero divisors and form a field, and the [multiplicative group modulo](/multiplicative-group-modulo-n/) $p$ has all $p - 1$ non-zero residues. A polynomial of degree $d$ then has at most $d$ roots modulo $p$.
- **Cancellation.** If $ac \equiv bc \pmod p$ and $p \nmid c$, then $a \equiv b \pmod p$, because $p \mid (a - b)c$.
- **Coprimality of products.** If $\gcd(a, m) = \gcd(b, m) = 1$ then $\gcd(ab, m) = 1$: a prime dividing $ab$ and $m$ would divide $a$ or $b$, see [coprime integers](/coprime-integers/).

## Tightness

**Composite divisors.** The hypothesis "prime" cannot be dropped: $6 \mid 4 \cdot 9 = 36$, but $6 \nmid 4$ and $6 \nmid 9$. The converse above shows that each composite $n$ has such a counterexample.

**Other rings.** In a ring where factorization is not unique, an element that cannot be factored can still fail the lemma. In $\mathbb{Z}[\sqrt{-5}] = \{ x + y\sqrt{-5} : x, y \in \mathbb{Z} \}$,

$$6 = 2 \cdot 3 = (1 + \sqrt{-5})(1 - \sqrt{-5}).$$

The element $2$ divides the product $(1 + \sqrt{-5})(1 - \sqrt{-5}) = 6$, but it divides neither factor, because $(1 \pm \sqrt{-5})/2$ does not have integer coordinates. Yet $2$ has no factorization into two non-units: the norm $N(x + y\sqrt{-5}) = x^2 + 5y^2$ is multiplicative, $N(2) = 4$, and no element has norm $2$. So "cannot be factored" (irreducible) and "satisfies Euclid's lemma" (prime) are different properties in general. They agree in $\mathbb{Z}$, and more generally in each principal ideal domain and each [Euclidean domain](/euclidean-domain/), because the Bézout proof works there.

## History

The lemma is Proposition 30 of Book VII of Euclid's *Elements*: if two numbers multiplied make a number and a prime measures the product, then it also measures one of the original numbers. Euclid states it for positive whole numbers. Hardy and Wright call it Euclid's first theorem. Euclid does not state the fundamental theorem of arithmetic in its modern form; the lemma became the standard route to it in later centuries, and Gauss gave the uniqueness proof in the form used today in his *Disquisitiones Arithmeticae* (1801).

## References
