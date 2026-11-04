---
tag: Q3DZ5B
kind: definition
slug: invertible-operation
name: Invertible operation
aliases:
- group operation
- reversible operation
area: data-structures/range-query-structures
level: intro
summary: Operation with an inverse, so a range aggregate can be computed as a difference of prefix aggregates.
prereqs: [monoid]
see_also: [prefix-sums, difference-array, fenwick-tree, idempotent-operation, finite-group, range-sum-query, mo-algorithm]
sources:
  - book: isbn:9780387953854
    title: Serge Lang, Algebra, revised third edition (Graduate Texts in Mathematics 211)
    locator: Chapter I, Sections 1 and 2 (monoids, invertible elements, the uniqueness of the inverse, and groups)
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook (free PDF edition)
    locator: Chapter 9, Range queries, Section 9.1 Static array queries (sum queries with a prefix sum array, and why minimum queries need another method)
  - paper: doi:10.1145/322290.322305
    title: "Michael L. Fredman, The Complexity of Maintaining an Array and Computing Its Partial Sums, Journal of the ACM 29(1) (1982), 250-260"
    locator: the group model of partial sums, in which the algorithm may subtract
---

An operation is invertible when each element $x$ has an inverse $x^{-1}$ that undoes it: $x \cdot x^{-1} = x^{-1} \cdot x = e$, where $e$ is the identity of the [monoid](/monoid/). A monoid with this property is a group, such as the integers with addition or the words with xor. Over a group, the value of a range is a quotient of two prefix values, $F(l, r) = P(l)^{-1} \cdot P(r)$, so [prefix sums](/prefix-sums/) answer static range queries in $O(1)$ time and a [Fenwick tree](/fenwick-tree/) answers dynamic ones with prefix queries only. Minimum, maximum and greatest common divisor have no inverse, and they need a [segment tree](/segment-tree/) or a [sparse table](/sparse-table/) instead.

## Definition

Let $(M, \cdot, e)$ be a monoid. An element $x \in M$ is **invertible** if there is a $y \in M$ with

$$ x \cdot y = e = y \cdot x. $$

Then $y$ is unique, and it is written $x^{-1}$. *Proof:* if $y$ and $y'$ both satisfy the equations, then $y = y \cdot e = y \cdot (x \cdot y') = (y \cdot x) \cdot y' = e \cdot y' = y'$. The operation $\cdot$ is **invertible** if every element of $M$ is invertible; then $(M, \cdot, e)$ is a **group**. For an additive group, $x^{-1}$ is written $-x$ and $x \cdot y^{-1}$ is written $x - y$.

Two rules follow from the definition: $(x \cdot y)^{-1} = y^{-1} \cdot x^{-1}$, because $(x \cdot y) \cdot (y^{-1} \cdot x^{-1}) = x \cdot e \cdot x^{-1} = e$ and the same holds in the other order, and a group is *cancellative*: $a \cdot x = a \cdot y$ implies $x = y$, by multiplying both sides on the left by $a^{-1}$.

**The prefix rule.** Let $A[0 \ldots n-1]$ be an array over a group. Put $P(0) = e$ and $P(i) = A[0] \cdot A[1] \cdots A[i-1]$, and let $F(l, r) = A[l] \cdots A[r-1]$ for $0 \le l \le r \le n$, with $F(l, l) = e$. Then

$$ F(l, r) = P(l)^{-1} \cdot P(r). $$

*Proof.* By the split law of a monoid, $P(r) = P(l) \cdot F(l, r)$. Multiply both sides on the left by $P(l)^{-1}$: $P(l)^{-1} \cdot P(r) = (P(l)^{-1} \cdot P(l)) \cdot F(l, r) = F(l, r)$. $\square$

When the group is commutative, the rule is the familiar $F(l, r) = P(r) - P(l)$. When it is not, the order of the factors is part of the rule: $P(r) \cdot P(l)^{-1}$ is a different element in general.

**Why it matters for range queries.** With the inverse, the $\binom{n+1}{2}$ range values are all determined by the $n + 1$ prefix values. A structure then needs to support only prefix queries, which is less than range queries. A static array needs $n + 1$ stored values and one operation per query. A dynamic array uses a Fenwick tree, whose PREFIX operation covers $(0, i]$ only. The inverse also gives the [difference array](/difference-array/): $D[i] = A[i-1]^{-1} \cdot A[i]$ turns a range update into two point updates. Without an inverse none of this works, and the structure must store values of inner ranges, as a segment tree does.

## Examples and non-examples

- **Integer addition.** $(\mathbb{Z}, +, 0)$ is a commutative group with $x^{-1} = -x$. For $A = [3, -1, 4, 1, -5, 9]$, the prefix values are $P = [0, 3, 2, 6, 7, 2, 11]$, and $F(2, 5) = P(5) - P(2) = 2 - 2 = 0$, which is $4 + 1 - 5$.
- **Addition modulo $m$.** $(\mathbb{Z}/m, +, 0)$ is a group, with $-x = m - x$ for $x \ne 0$. This is the group of hash sums and of counts kept modulo a prime.
- **Xor.** The $w$-bit words with $\oplus$ and $0$ form a group in which each element is its own inverse. For $A = [5, 3, 6, 2]$, $P = [0, 5, 6, 0, 2]$, and $F(1, 3) = P(1) \oplus P(3) = 5 \oplus 0 = 5 = 3 \oplus 6$.
- **Multiplication of non-zero numbers modulo a prime $p$.** $(\{1, \ldots, p-1\}, \cdot, 1)$ is a group, and the inverse of $x$ is $x^{p-2} \bmod p$ by Fermat's little theorem. Multiplication on all of $\mathbb{Z}/p$ is not a group, because $0$ has no inverse. A range product with zeros is computed from the count of zeros in the range and the product of the non-zero items.
- **Invertible matrices, a group that is not commutative.** Take $A_0 = \begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}$, $A_1 = \begin{pmatrix} 1 & 0 \\ 1 & 1 \end{pmatrix}$ and $A_2 = \begin{pmatrix} 2 & 1 \\ 1 & 1 \end{pmatrix}$. Then $F(1, 3) = A_1 A_2 = \begin{pmatrix} 2 & 1 \\ 3 & 2 \end{pmatrix}$, and $P(1)^{-1} P(3)$ gives the same matrix, but $P(3) P(1)^{-1} = \begin{pmatrix} 5 & -2 \\ 3 & -1 \end{pmatrix}$.
- **Minimum, a non-example.** $(\mathbb{Z} \cup \{+\infty\}, \min, +\infty)$ is a monoid, but $\min(x, y) = +\infty$ forces $x = +\infty$, so no finite $x$ has an inverse. Prefix minima do not determine range minima: the arrays $[1, 5]$ and $[1, 7]$ have the same prefix minima, $1$ and $1$, but the minimum of the last item is 5 in one and 7 in the other. Minimum is an [idempotent operation](/idempotent-operation/) instead, and in a group only the identity is idempotent.
- **Maximum, gcd, bitwise or and bitwise and, non-examples.** None has inverses: $\gcd(x, y) = 0$ forces $x = 0$, and $x \lor y = 0$ forces $x = 0$.
- **Concatenation of strings, a non-example.** Only the empty string has an inverse. String hashing works around this by mapping strings to a group of numbers modulo a prime, where the hash of a substring is a quotient of two prefix hashes.
- **Floating-point addition, an approximate group.** In exact arithmetic the reals form a group, but floating-point addition is not associative and the subtraction loses the low digits. For $A = [10^{16}, 1, 1]$ in double precision, $P(1) = P(2) = P(3) = 10^{16}$, so $P(3) - P(1) = 0$ while $F(1, 3) = 2$.

## Related definitions

- **[Monoid](/monoid/).** The structure without the inverse law. Every group is a monoid.
- **[Finite group](/finite-group/).** The algebra page for groups with finitely many elements.
- **[Idempotent operation](/idempotent-operation/).** The other property that gives fast static range queries, by overlap instead of subtraction.
- **[Prefix sums](/prefix-sums/) and [difference array](/difference-array/).** The two inverse maps between an array and its prefix values, both defined over any group.
- **Group model of partial sums.** In the lower bounds for the [dynamic partial sums](/dynamic-partial-sums-lower-bound/) problem, the *group model* allows subtraction and the *semigroup model* does not. Logarithmic lower bounds are known in both models.

## References
