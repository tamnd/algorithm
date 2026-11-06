---
tag: EZSP4C
kind: theorem
slug: gcd-recursion-theorem
name: GCD recursion theorem
area: number-theory/divisibility-and-gcd
level: core
summary: For integers a and b with b nonzero, gcd(a, b) equals gcd(b, a mod b), which justifies Euclid's algorithm.
prereqs: [greatest-common-divisor, divisibility, integer-division]
see_also: [euclidean-algorithm, extended-euclidean-algorithm, binary-gcd, lames-theorem, continued-fraction, euclidean-domain, polynomial-euclidean-algorithm, gcd-of-two-integers]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.2, Greatest common divisor (the GCD recursion theorem and the procedure EUCLID)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.5.2, The Greatest Common Divisor (Algorithm A, the modern Euclidean algorithm, and its proof)
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 4.1, Divisibility (Euclid's algorithm as the recurrence gcd(0, n) = n and gcd(m, n) = gcd(n mod m, m))
  - url: "https://en.wikipedia.org/wiki/Euclidean_algorithm"
    locator: section History (Euclid, Elements, Book VII, Propositions 1 and 2)
---

The GCD recursion theorem says that for integers $a$ and $b$ with $b \ne 0$, $\gcd(a, b) = \gcd(b, a \bmod b)$. More strongly, $a$ and $b$ have exactly the same common divisors as $b$ and $a - qb$ for every integer $q$. This is the step of the [Euclidean algorithm](/euclidean-algorithm/): repeating it shrinks the pair until the second number is 0, and then the first number is the [greatest common divisor](/greatest-common-divisor/). The same identity drives the [extended Euclidean algorithm](/extended-euclidean-algorithm/), [continued fractions](/continued-fraction/) and the gcd in every [Euclidean domain](/euclidean-domain/).

## Statement

For integers $a$ and $b$ with $b \ne 0$, let $a \bmod b = a - b \lfloor a/b \rfloor$ be the remainder of [integer division](/integer-division/). For $b > 0$ it satisfies $0 \le a \bmod b < b$.

**Theorem.** For all integers $a$ and $b$ and every integer $q$, the common divisors of $a$ and $b$ are exactly the common divisors of $b$ and $a - qb$. Hence

$$\gcd(a, b) = \gcd(b, a - qb),$$

and in particular, for $b \ne 0$,

$$\gcd(a, b) = \gcd(b, a \bmod b).$$

The second form holds for any convention for the remainder that has the shape $a - qb$: the floored remainder above, the truncated remainder of C and Java (which can be negative), or the least absolute remainder.

**Corollary (Euclid's algorithm).** For integers $a \ge 0$ and $b \ge 0$, the loop "while $b \ne 0$: $(a, b) \leftarrow (b, a \bmod b)$" stops after at most $b$ iterations, and then $a = \gcd$ of the original pair. For arbitrary integers, run it on $|a|$ and $|b|$.

## In plain words

Any number that divides two numbers also divides their difference, and it divides the larger one minus any number of copies of the smaller one. The reverse is also true: a number that divides the smaller one and what is left over also divides the larger one. So taking away copies of the smaller number does not change the list of common divisors at all, and so the greatest one stays the same.

The remainder after division is exactly what is left after taking away as many copies as possible. It is smaller than the divisor, so the pair of numbers keeps getting smaller. When the remainder is zero, the smaller number divides the larger one, and it is the answer.

## Proof

**The theorem.** Let $q$ be an integer and $r = a - qb$.

1. If $d \mid a$ and $d \mid b$, then $a = d s$ and $b = d t$ for integers $s$ and $t$, so $r = d(s - qt)$ and $d \mid r$. Thus every common divisor of $a$ and $b$ is a common divisor of $b$ and $r$.
2. If $d \mid b$ and $d \mid r$, then $a = r + qb$ is a sum of multiples of $d$, so $d \mid a$. Thus every common divisor of $b$ and $r$ is a common divisor of $a$ and $b$.
3. So the two pairs have the same set of common divisors. If $a$ and $b$ are not both zero, then $b$ and $r$ are not both zero (if $b = r = 0$ then $a = 0$), and the two gcds are the maximum of the same set, so they are equal. If $a = b = 0$, then $r = 0$ and both gcds are $\gcd(0, 0) = 0$.
4. For $b \ne 0$, $a \bmod b = a - b\lfloor a/b \rfloor$ has the form $a - qb$ with $q = \lfloor a/b \rfloor$, so $\gcd(a, b) = \gcd(b, a \bmod b)$.

**The corollary.** We use the [loop invariant](/loop-invariant/) "$a \ge 0$, $b \ge 0$, and $\gcd(a, b) = G$", where $G$ is the gcd of the original pair.

- *Initialization.* It holds before the first iteration by the definition of $G$.
- *Maintenance.* In an iteration $b > 0$, so the new pair $(b, a \bmod b)$ has $b > 0$ and $0 \le a \bmod b < b$, and the theorem gives $\gcd(b, a \bmod b) = \gcd(a, b) = G$.
- *Termination.* The second number is a nonnegative integer, and each iteration replaces it by $a \bmod b \le b - 1$, so it drops by at least 1. Hence the loop stops after at most $b$ iterations of the original $b$.
- *Exit.* At the end $b = 0$, and $\gcd(a, 0) = a$ for $a \ge 0$. So $a = G$. $\blacksquare$

The bound of $b$ iterations is far from the truth: [Lamé's theorem](/lames-theorem/) shows that the number of iterations is $O(\log b)$, because the remainders fall at least as fast as Fibonacci numbers in reverse.

## Consequences

**Example.** For $(1071, 462)$: $1071 \bmod 462 = 147$, $462 \bmod 147 = 21$ and $147 \bmod 21 = 0$, so

$$\gcd(1071, 462) = \gcd(462, 147) = \gcd(147, 21) = \gcd(21, 0) = 21.$$

With $q = 2$ instead of the floor, $\gcd(1071, 462) = \gcd(462, 1071 - 2 \cdot 462) = \gcd(462, 147)$, the same step. For $a = -17$ and $b = 5$, the floored remainder is 3 and the truncated remainder is $-2$, and $\gcd(5, 3) = \gcd(5, -2) = 1 = \gcd(-17, 5)$.

- **The Euclidean algorithm.** The corollary is the correctness proof of the [Euclidean algorithm](/euclidean-algorithm/), in its recursive form $\gcd(a, 0) = a$, $\gcd(a, b) = \gcd(b, a \bmod b)$, and in its loop form.
- **The subtractive algorithm.** With $q = 1$: $\gcd(a, b) = \gcd(b, a - b)$. Euclid's own method subtracts the smaller number from the larger one. It is correct by the theorem, but it can take $\max(a, b)$ steps, for example on $(10^9, 1)$.
- **The extended algorithm.** If $a = qb + r$, any pair $(x, y)$ with $bx + ry = g$ gives $ay + b(x - qy) = g$. This back-substitution is the [extended Euclidean algorithm](/extended-euclidean-algorithm/), and it proves [Bézout's identity](/bezouts-identity/).
- **Continued fractions.** The quotients $\lfloor a/b \rfloor$ of the algorithm are the partial quotients of the [continued fraction](/continued-fraction/) of $a/b$.
- **Binary GCD.** The [binary GCD](/binary-gcd/) uses the case $q = 1$ together with $\gcd(2a, 2b) = 2\gcd(a, b)$ and $\gcd(2a, b) = \gcd(a, b)$ for odd $b$.
- **Other rings.** The proof uses only that $d \mid a$ and $d \mid b$ imply $d \mid a - qb$, which holds in every commutative ring. With division with remainder, it gives the [polynomial Euclidean algorithm](/polynomial-euclidean-algorithm/) and Euclid's algorithm in every [Euclidean domain](/euclidean-domain/).

## Tightness

The condition $b \ne 0$ is needed only for the form with $a \bmod b$, which is undefined for $b = 0$; the form with $a - qb$ holds for all integers. The theorem keeps the set of common divisors, not only the greatest one, and this cannot be strengthened to keep $a$ itself: $(1071, 462)$ and $(462, 147)$ are different pairs with the same gcd. The termination bound of $b$ iterations is reached by the subtractive version on $(n, 1)$, which takes $n$ steps, but not by the version with remainders, which finishes $(n, 1)$ in one step.

## History

The algorithm appears in Euclid's Elements, Book VII, Propositions 1 and 2, as repeated subtraction of the smaller number from the larger one. The name "GCD recursion theorem" is the one used by Cormen, Leiserson, Rivest and Stein in Section 31.2. Knuth, in Section 4.5.2, gives the form with remainders as Algorithm A and calls Euclid's algorithm the oldest nontrivial algorithm that has survived to the present day.

## References
