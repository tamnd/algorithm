---
tag: F7GAWF
kind: definition
slug: idempotent-operation
name: Idempotent operation
aliases:
- idempotence
area: data-structures/range-query-structures
level: intro
summary: Operation with op(x,x)=x, so overlapping ranges can be combined safely as in sparse-table queries.
prereqs: [monoid, associative-operator]
see_also: [sparse-table, range-minimum-query, invertible-operation, disjoint-sparse-table, bender-farach-colton-rmq, join-semilattice, range-gcd-query]
sources:
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook (free PDF edition)
    locator: Chapter 9, Range queries, Section 9.1 Static array queries (minimum queries with two overlapping ranges of length a power of two)
  - url: https://cp-algorithms.com/data_structures/sparse-table.html
    title: cp-algorithms, Sparse Table
    locator: the sections Range Minimum Queries (RMQ) and Similar data structures supporting more types of queries (idempotent functions)
  - paper: doi:10.1007/10719839_9
    title: "Michael A. Bender and Martin Farach-Colton, The LCA Problem Revisited, LATIN 2000, Lecture Notes in Computer Science 1776, 88-94"
    locator: Section 3 (the O(n log n) sparse table, where a query takes the minimum of two overlapping blocks)
---

A binary operation $\circ$ is idempotent when $x \circ x = x$ for every element $x$. For an [associative](/associative-operator/) idempotent operation, the value of a range is the combination of the values of any two ranges that overlap and together cover it, because the part that is counted twice does not change the result. This is why a [sparse table](/sparse-table/) answers a [range minimum query](/range-minimum-query/) with two lookups in $O(1)$ time, while a range sum, which is not idempotent, needs a different method. Minimum, maximum, greatest common divisor, bitwise and, bitwise or, and set union are idempotent; sum, product and xor are not.

## Definition

Let $S$ be a set and $\circ : S \times S \to S$ a binary operation.

- An element $x \in S$ is **idempotent** if $x \circ x = x$.
- The operation $\circ$ is **idempotent** if every element of $S$ is idempotent: $\forall x \in S : x \circ x = x$.

An associative idempotent operation makes $S$ a *band*. A band that is also commutative is a *semilattice*, see [join-semilattice](/join-semilattice/).

**The overlap rule.** Let $\circ$ be associative and idempotent, let $A[0 \ldots n-1]$ be an array over $S$, and for $l \le r$ write $F[l, r] = A[l] \circ A[l+1] \circ \cdots \circ A[r]$. Then for all $l \le a \le b \le r$,

$$ F[l, r] = F[l, b] \circ F[a, r]. $$

*Proof.* The two ranges $[l, b]$ and $[a, r]$ overlap in $[a, b]$, which is not empty. By general associativity (see [monoid](/monoid/)), $F[l, b] = L \circ F[a, b]$ and $F[a, r] = F[a, b] \circ R$, where $L = F[l, a-1]$ and $R = F[b+1, r]$, and where a factor $L$ or $R$ is left out when its range is empty. So

$$ F[l, b] \circ F[a, r] = L \circ \big(F[a, b] \circ F[a, b]\big) \circ R = L \circ F[a, b] \circ R = F[l, r], $$

by associativity, then by idempotence applied to the single element $F[a, b]$, then by associativity again. $\square$

Commutativity is not needed: the order $L$, middle, $R$ stays the same. Idempotence of all elements is more than the proof needs; it uses only that range values are idempotent.

**The sparse table query.** If $T[k][i] = F[i, i + 2^k - 1]$ is stored for each $k$ and $i$, and $k = \lfloor \lg(r - l + 1) \rfloor$, then the ranges $[l, l + 2^k - 1]$ and $[r - 2^k + 1, r]$ lie in $[l, r]$, and they overlap or touch, because $2 \cdot 2^k > r - l + 1$. The overlap rule gives $F[l, r] = T[k][l] \circ T[k][r - 2^k + 1]$, with one operation per query.

**A different sense.** A function $f : X \to X$ is called idempotent when $f \circ f = f$, for example rounding, or an HTTP request that has the same effect when repeated. This is idempotence of the element $f$ in the monoid of functions under composition, and it is not the property used for range queries.

## Examples and non-examples

Take $A = [5, 2, 8, 6, 3, 7, 9, 1]$ with indices 0 to 7, and the query $[1, 6]$ of length 6. Then $k = 2$, and the two ranges are $[1, 4]$ and $[3, 6]$, which overlap in $[3, 4]$.

- **Minimum.** $\min(2, 8, 6, 3) = 2$ and $\min(6, 3, 7, 9) = 3$, so the answer is $\min(2, 3) = 2$, which is the minimum of $A[1 \ldots 6]$.
- **Maximum.** $\max(2, 8, 6, 3) = 8$ and $\max(6, 3, 7, 9) = 9$, so the answer is 9.
- **Sum, a non-example.** The two parts have sums 19 and 25. Their sum 44 is not the true sum 35 of $A[1 \ldots 6]$: the overlap $6 + 3 = 9$ is counted twice. Addition is not idempotent, since $x + x = 2x$.
- **Greatest common divisor.** For $[12, 18, 30, 42]$ and the query $[0, 3]$, the ranges $[0, 2]$ and $[1, 3]$ give $\gcd(12, 18, 30) = 6$ and $\gcd(18, 30, 42) = 6$, and $\gcd(6, 6) = 6$. This is the [range gcd query](/range-gcd-query/) in $O(1)$ lookups. The least common multiple is idempotent too.
- **Bitwise and, bitwise or, set union and set intersection.** Each is associative, commutative and idempotent: $x \mathbin{\&} x = x$ and $X \cup X = X$.
- **Arg-min.** The pairs (value, index) under the lexicographic minimum are a band. A sparse table over these pairs returns the position of the leftmost minimum.
- **A band that is not commutative.** On any set, the rule $x \circ y = x$ is associative and idempotent but not commutative. Then $F[l, r] = A[l]$, and the overlap rule gives $A[l] \circ A[a] = A[l]$, as it must.
- **Xor, a non-example.** $x \oplus x = 0$, so the overlap cancels. Xor is a group operation, see [invertible operation](/invertible-operation/): a range xor is the xor of two prefix values instead.
- **Product and counting, non-examples.** $x \cdot x = x$ only for $x \in \{0, 1\}$, and a count adds the overlap twice.
- **The mean, idempotent but not associative.** $(x + x)/2 = x$, but the mean is not associative (see [monoid](/monoid/)), so the overlap rule fails: for $[0, 0, 6]$, the means of $[0, 1]$ and $[1, 2]$ are 0 and 3, and their mean is 1.5, but the mean of the array is 2.
- **Groups.** In a group, the only idempotent element is the identity: from $x \circ x = x$, multiply by $x^{-1}$ to get $x = e$. So no operation is both invertible and idempotent, except on a one-element set. The two properties give two different methods, and each common range query uses one of them.

## Related definitions

- **[Monoid](/monoid/) and [associative operator](/associative-operator/).** The overlap rule needs associativity. An identity is not needed, because no range in it is empty.
- **[Invertible operation](/invertible-operation/).** The other way to get fast static range queries: subtract a prefix instead of overlapping two ranges.
- **[Sparse table](/sparse-table/).** Stores $F$ on all ranges of length a power of two, $O(n \log n)$ values, and answers idempotent queries in $O(1)$.
- **[Disjoint sparse table](/disjoint-sparse-table/).** Splits each query into two disjoint ranges, so it gives $O(1)$ queries for any associative operation, idempotent or not.
- **[Bender-Farach-Colton RMQ](/bender-farach-colton-rmq/).** Uses the overlap rule inside and across blocks to get $O(n)$ preprocessing and $O(1)$ range minimum queries.
- **[Join-semilattice](/join-semilattice/).** A commutative band, the order-theoretic view of $\max$, $\lor$ and $\cup$.

## References
