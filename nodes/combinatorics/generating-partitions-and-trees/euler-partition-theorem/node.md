---
tag: AYQC0V
kind: theorem
slug: euler-partition-theorem
name: Euler's partition theorem
aliases:
- Distinct and odd parts theorem
- Euler's odd-distinct theorem
area: combinatorics/generating-partitions-and-trees
level: intro
summary: The number of partitions of n into distinct parts equals the number of partitions of n into odd parts.
prereqs: [integer-partitions, generating-functions]
see_also: [conjugate-partition, ferrers-diagram, integer-partition-function, euler-pentagonal-number-theorem, bijective-proof, integer-partition-generation]
sources:
  - book: isbn:9780521637664
    title: George E. Andrews, The Theory of Partitions, Cambridge University Press, 1998 (first published 1976)
    locator: Chapter 1, The elementary theory of partitions, pages 1 to 15 (Euler's theorem by generating functions, Glaisher's bijection and its generalization)
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Section 1.8, Partition identities (distinct parts and odd parts, by generating functions and by a bijection)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.4, Generating all partitions (generating functions for restricted partitions and the exercises on partition identities)
  - paper: "J. W. L. Glaisher, A theorem in partitions, Messenger of Mathematics 12 (1883), 158-170"
    locator: the whole paper (the bijection by binary expansion of multiplicities, and the version for a modulus d)
---

Euler's partition theorem says that, for each $n \ge 0$, the number of [partitions](/integer-partitions/) of $n$ into distinct parts equals the number of partitions of $n$ into odd parts. For example, $8$ has six of each. Euler proved it with [generating functions](/generating-functions/) in 1748, and Glaisher gave a bijection in 1883 that turns one kind of partition into the other in linear time. It is the first example of a partition identity, and it shows the two standard ways to prove one: an equation of power series and a [bijective proof](/bijective-proof/).

## Statement

For an integer $n \ge 0$, let $q(n)$ be the number of partitions of $n$ into distinct parts (no part appears twice), and let $o(n)$ be the number of partitions of $n$ into odd parts (each part is odd, and repeats are allowed). The empty partition counts for $n = 0$.

**Theorem** (Euler). For each $n \ge 0$, $q(n) = o(n)$. Equivalently, as [formal power series](/generating-functions/) in $x$,

$$\prod_{k \ge 1} (1 + x^k) = \prod_{k \ge 1} \frac{1}{1 - x^{2k - 1}}.$$

**Theorem** (Glaisher). Let $d \ge 2$ be an integer. For each $n \ge 0$, the number of partitions of $n$ in which no part appears $d$ or more times equals the number of partitions of $n$ with no part divisible by $d$. The case $d = 2$ is Euler's theorem.

## In plain words

Take a number and split it into a sum. Count the splits in which all the terms are different. Then count the splits in which all the terms are odd, where a term may repeat. The two counts are always the same.

There is a direct way to see this. In a split into odd terms, collect the copies of each odd term. If the term three appears five times, write five as a sum of different powers of two: four plus one. Then glue four threes into one twelve and keep one three. Do this for each odd term. The new terms are all different, and you can undo the gluing because each term is an odd number times a power of two in exactly one way.

## Proof

**Proof 1 (generating functions).** Work in the ring of formal power series $\mathbb{Z}[[x]]$. The coefficient of $x^n$ in $\prod_{k \ge 1} (1 + x^k)$ is $q(n)$: to form $x^n$, choose from each factor either $1$ (part $k$ absent) or $x^k$ (part $k$ present once), and only finitely many factors contribute a term other than $1$ to any fixed power. Likewise $\frac{1}{1 - x^{j}} = \sum_{m \ge 0} x^{jm}$, so the coefficient of $x^n$ in $\prod_{j \text{ odd}} \frac{1}{1 - x^j}$ is the number of ways to choose multiplicities $m_j \ge 0$ for the odd $j$ with $\sum_j j m_j = n$, which is $o(n)$. Now use $1 + x^k = \frac{1 - x^{2k}}{1 - x^k}$:

$$\prod_{k \ge 1} (1 + x^k) = \prod_{k \ge 1} \frac{1 - x^{2k}}{1 - x^k} = \frac{\prod_{k \ge 1} (1 - x^{2k})}{\prod_{k \ge 1} (1 - x^{k})} = \prod_{k \text{ odd}} \frac{1}{1 - x^k}.$$

The last step cancels each factor $1 - x^{2k}$ of the numerator against the factor of the same even exponent in the denominator, and leaves the odd exponents. Each step is valid in $\mathbb{Z}[[x]]$: to check the coefficient of $x^n$, it is enough to take the finite products over $k \le n$, since every other factor is $1 + O(x^{n+1})$. For finite products the cancellation is an identity of rational functions. Comparing coefficients gives $q(n) = o(n)$. $\square$

**Proof 2 (Glaisher's bijection, for each $d \ge 2$).** Each integer $m \ge 1$ has a unique form $m = j\, d^{e}$ with $e \ge 0$ and $d \nmid j$. Each integer $c \ge 0$ has a unique base $d$ expansion $c = \sum_{e \ge 0} c_e d^e$ with digits $0 \le c_e \le d - 1$.

- *From "no part divisible by $d$" to "no part $d$ or more times".* Let $\mu$ have parts not divisible by $d$, and let $c_j$ be the multiplicity of part $j$. Write $c_j = \sum_e c_{j,e} d^e$ in base $d$. Replace the $c_j$ copies of $j$ by $c_{j,e}$ copies of $j d^e$ for each $e$. The sum of these new parts is $\sum_e c_{j,e}\, j d^e = j c_j$, so the total stays $n$. Call the result $\Phi(\mu)$.
- *$\Phi(\mu)$ has no part $d$ or more times.* A part $m$ of $\Phi(\mu)$ has a unique form $m = j d^e$ with $d \nmid j$, so it arises only from the copies of $j$ and from the digit $e$. Its multiplicity is the single digit $c_{j,e} \le d - 1$.
- *The inverse.* Let $\nu$ have no part $d$ or more times. Write each part as $j d^e$ with $d \nmid j$, and replace each copy of $j d^e$ by $d^e$ copies of $j$. This is $\Psi(\nu)$. It has no part divisible by $d$ and the same sum.
- *They are inverse.* $\Psi(\Phi(\mu))$ turns the $c_{j,e}$ copies of $j d^e$ back into $\sum_e c_{j,e} d^e = c_j$ copies of $j$, so it is $\mu$. In $\nu$, let $c_{j,e} \le d - 1$ be the multiplicity of $j d^e$. Then $\Psi(\nu)$ has $\sum_e c_{j,e} d^e$ copies of $j$, and by the uniqueness of base $d$ expansions, $\Phi$ recovers exactly the digits $c_{j,e}$, so $\Phi(\Psi(\nu)) = \nu$.

So $\Phi$ is a bijection between the two sets of partitions of $n$, and they have the same size. For $d = 2$, "no part twice" means distinct parts and "no part divisible by $2$" means odd parts. $\blacksquare$

**Cost of the bijection.** With the partition in multiplicity form, $\Phi$ takes $O(\sum_j (1 + \log_d c_j))$ steps, and $\Psi$ takes time linear in the number of parts it writes. So a generator of one family, followed by $\Phi$ or $\Psi$, generates the other family with $O(n)$ extra time for each object.

## Consequences

**A table.** For $n = 0, 1, \ldots, 20$, $q(n) = o(n)$ takes the values

$$1, 1, 1, 2, 2, 3, 4, 5, 6, 8, 10, 12, 15, 18, 22, 27, 32, 38, 46, 54, 64.$$

**The case $n = 8$.** Glaisher's map $\Phi$ sends the six odd partitions of $8$ to the six distinct partitions:

| odd parts | multiplicities in binary | distinct parts |
| --- | --- | --- |
| $7, 1$ | $7^1$, $1^1$ | $7, 1$ |
| $5, 3$ | $5^1$, $3^1$ | $5, 3$ |
| $5, 1, 1, 1$ | $5^1$, $1^{2+1}$ | $5, 2, 1$ |
| $3, 3, 1, 1$ | $3^{2}$, $1^{2}$ | $6, 2$ |
| $3, 1, 1, 1, 1, 1$ | $3^1$, $1^{4+1}$ | $4, 3, 1$ |
| $1^8$ | $1^{8}$ | $8$ |

A larger case: in $(3, 3, 3, 1, 1, 1, 1, 1)$ the multiplicities are $3 = 2 + 1$ and $5 = 4 + 1$, so $\Phi$ gives $(6, 3, 4, 1)$, sorted $(6, 4, 3, 1)$.

**Uses.**

- Generation: to list the partitions of $n$ into distinct parts, list the odd partitions with the recursion on the largest part of [integer partitions](/integer-partitions/), with only odd values allowed, and map each one by $\Phi$. A direct generator such as [Algorithm P](/integer-partition-generation/) lists all partitions and would need a filter.
- Glaisher's theorem with $d = 3$ says that the partitions with no part three or more times are as many as the partitions with no part divisible by $3$.
- The method of Proof 1, writing the condition on the parts as a product of simple factors, gives the generating function of every family of partitions with conditions on the parts and their multiplicities. The [pentagonal number theorem](/euler-pentagonal-number-theorem/) expands the reciprocal of the generating function of [all partitions](/integer-partition-function/).
- The same identity, through [conjugate partitions](/conjugate-partition/), relates the self-conjugate partitions to partitions into distinct odd parts.

## Tightness

The equality is exact for every $n$, so there is no bound to improve. Close variants are false, which shows that the pairing of "distinct" with "odd" is special:

- Distinct parts against even parts: for $n = 3$ there are two partitions into distinct parts, $(3)$ and $(2, 1)$, and none into even parts.
- Distinct parts against parts that are $1$ or $2$ modulo $3$: for $n = 3$ there are two of the first kind and two of the second, $(2, 1)$ and $(1, 1, 1)$, but for $n = 4$ there are two of the first kind, $(4)$ and $(3, 1)$, and four of the second, $(4)$, $(2, 2)$, $(2, 1, 1)$ and $(1, 1, 1, 1)$. The correct partner of "parts not divisible by $3$" is "no part three or more times", by Glaisher's theorem.
- Glaisher's theorem needs $d \ge 2$. For $d = 1$ both sides would be empty for $n \ge 1$, and the statement is trivially true but carries no content.

## History

Euler proved the identity with the product formula in his Introductio in analysin infinitorum of 1748, in the chapter on the partition of numbers. Sylvester gave a combinatorial proof, and Glaisher, in 1883, gave the bijection by base $d$ expansion and the general theorem for each modulus $d$. Andrews, in Chapter 1, gives both proofs and further refinements.

## References
