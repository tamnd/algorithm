---
tag: 9GE7DP
kind: definition
slug: monoid
name: Monoid
aliases:
- associative operation with identity
area: data-structures/range-query-structures
level: intro
summary: Associative binary operation with an identity element, the algebraic requirement for combining range aggregates.
prereqs: [associative-operator]
see_also: [invertible-operation, idempotent-operation, segment-tree, fenwick-tree, lazy-propagation, disjoint-sparse-table, blelloch-scan, segment-tree-maximum-subsegment-sum]
sources:
  - book: isbn:9780387953854
    title: Serge Lang, Algebra, revised third edition (Graduate Texts in Mathematics 211)
    locator: Chapter I, Section 1 (Monoids), including the general associativity of a product of n elements
  - paper: "Guy E. Blelloch, Prefix Sums and Their Applications, Technical Report CMU-CS-90-190, Carnegie Mellon University, 1990"
    locator: Section 1 (the scan of a binary associative operator with an identity)
  - url: https://cp-algorithms.com/data_structures/segment_tree.html
    title: cp-algorithms, Segment Tree
    locator: the sections on other combining operations (minimum, greatest common divisor, the maximal subsegment sum)
---

A monoid is a set with a binary operation that is [associative](/associative-operator/) and has an identity element. The identity is the value of an empty product, and associativity means that a product of many elements does not depend on where the brackets go. These two laws are exactly what a [segment tree](/segment-tree/), a [disjoint sparse table](/disjoint-sparse-table/) or a parallel [scan](/blelloch-scan/) needs to combine the aggregates of adjacent ranges in any grouping. Sum, product, minimum, maximum, greatest common divisor, string concatenation and matrix product are monoids; subtraction and the mean are not.

## Definition

A **monoid** is a triple $(M, \cdot, e)$ of a set $M$, a function $\cdot : M \times M \to M$ and an element $e \in M$ such that for all $x, y, z \in M$:

$$ (x \cdot y) \cdot z = x \cdot (y \cdot z) \qquad \text{(associativity)} $$

$$ e \cdot x = x = x \cdot e \qquad \text{(identity)} $$

A set with an associative operation and no identity is a *semigroup*. A monoid is **commutative** if $x \cdot y = y \cdot x$ for all $x, y$. A **monoid homomorphism** from $(M, \cdot, e)$ to $(N, *, e')$ is a function $h$ with $h(x \cdot y) = h(x) * h(y)$ and $h(e) = e'$.

**The identity is unique.** If $e$ and $e'$ are both identities, then $e = e \cdot e' = e'$: the first step uses that $e'$ is an identity, the second that $e$ is one.

**The product of a sequence.** For $x_1, \ldots, x_n \in M$ define $\prod_{k=1}^{0} x_k = e$ and $\prod_{k=1}^{n} x_k = \left(\prod_{k=1}^{n-1} x_k\right) \cdot x_n$. *General associativity:* every way to put brackets in $x_1 \cdot x_2 \cdots x_n$, without a change of order, gives this same value. Proof by strong induction on $n$. For $n \le 2$ there is only one bracketing. For $n \ge 3$, a bracketing has an outer product $u \cdot v$, where $u$ is a bracketing of $x_1 \cdots x_m$ and $v$ of $x_{m+1} \cdots x_n$ for some $1 \le m < n$. By the hypothesis, $u = \prod_{k \le m} x_k$ and $v = \prod_{k = m+1}^{n} x_k$. If $m = n - 1$, then $v = x_n$ and $u \cdot v$ is the left product. If $m < n - 1$, write $v = v' \cdot x_n$ with $v' = \prod_{k=m+1}^{n-1} x_k$, by the hypothesis applied to the left product of $v$. Then $u \cdot v = u \cdot (v' \cdot x_n) = (u \cdot v') \cdot x_n$ by associativity, and $u \cdot v' = \prod_{k \le n-1} x_k$ by the hypothesis, so $u \cdot v$ is again the left product. Lang states this in Chapter I, Section 1.

**The rule for range queries.** For an array $A[0 \ldots n-1]$ over $M$, write $F(l, r) = A[l] \cdot A[l+1] \cdots A[r-1]$ for the half-open range $[l, r)$, with $F(l, l) = e$. General associativity gives the *split law*

$$ F(l, r) = F(l, m) \cdot F(m, r) \qquad \text{for each } l \le m \le r. $$

A segment tree stores $F$ on a fixed set of ranges and answers a query by the split law. The identity is the answer for an empty range, the value of the padding when the length is rounded up to a power of two, and the start value of a loop that folds a list of node values. The order of the factors matters when the monoid is not commutative: the query must combine the left part before the right part.

## Examples and non-examples

- **Sum.** $(\mathbb{Z}, +, 0)$ is a commutative monoid, and it is a group because each $x$ has the inverse $-x$. This makes it an [invertible operation](/invertible-operation/), so a range sum is a difference of two prefix sums, as in the [Fenwick tree](/fenwick-tree/).
- **Minimum and maximum.** $(\mathbb{Z} \cup \{+\infty\}, \min, +\infty)$ is a commutative monoid. Without $+\infty$, $(\mathbb{Z}, \min)$ is only a semigroup, because no integer $e$ has $\min(e, x) = x$ for all $x$. Minimum is also an [idempotent operation](/idempotent-operation/), since $\min(x, x) = x$.
- **Greatest common divisor.** $(\mathbb{N}, \gcd, 0)$ is a commutative monoid, because $\gcd(0, x) = x$. It is idempotent. It is the basis of the [range gcd query](/range-gcd-query/). The least common multiple gives $(\mathbb{N}_{\ge 1}, \operatorname{lcm}, 1)$.
- **Booleans and bits.** $(\{0, 1\}, \lor, 0)$, $(\{0, 1\}, \land, 1)$ and the words with bitwise xor and $0$ are monoids. Xor is a group, since $x \oplus x = 0$.
- **Strings.** The strings over an alphabet with concatenation and the empty string form a monoid that is not commutative: $ab \ne ba$. So a segment tree of strings or of string hashes must keep left and right apart.
- **Matrices.** The $2 \times 2$ integer matrices with matrix product and the identity matrix $I$ form a monoid that is not commutative. A range product of the matrices $\begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}$ is a power of it, as in [matrix exponentiation](/matrix-exponentiation/), and a segment tree of such matrices updates a linear recurrence in one place.
- **Affine maps.** The maps $x \mapsto a x + b$ with composition and the identity map form a monoid: applying $x \mapsto a_1 x + b_1$ first and $x \mapsto a_2 x + b_2$ after gives $x \mapsto a_2 a_1 x + (a_2 b_1 + b_2)$. These maps are the pending tags of [lazy propagation](/lazy-propagation/) for "multiply and add" updates.
- **Maximum subarray sum.** Map a range to the tuple $(s, p, q, b)$: its sum, its best prefix sum, its best suffix sum and its best subarray sum, all over non-empty parts. Combine with $s = s_1 + s_2$, $p = \max(p_1, s_1 + p_2)$, $q = \max(q_2, s_2 + q_1)$, $b = \max(b_1, b_2, q_1 + p_2)$, and use $(0, -\infty, -\infty, -\infty)$ as the identity. The range $[2, -5, 3]$ gives $(0, 2, 3, 3)$, the range $[4, -1, 2]$ gives $(5, 5, 5, 5)$, and their product is $(5, 5, 8, 8)$: the best subarray of $[2, -5, 3, 4, -1, 2]$ is $3 + 4 - 1 + 2 = 8$. This is the monoid of the [maximum subsegment sum](/segment-tree-maximum-subsegment-sum/) segment tree and of the [maximum subarray problem](/maximum-subarray-problem/) by divide and conquer.
- **Non-example: subtraction.** $(5 - 3) - 1 = 1$ but $5 - (3 - 1) = 3$, so subtraction is not associative, and a tree of differences gives a value that depends on the shape of the tree. Store sums and subtract at the end instead.
- **Non-example: the mean.** With $x \circ y = (x + y)/2$, $(1 \circ 2) \circ 3 = 2.25$ but $1 \circ (2 \circ 3) = 1.75$. Store the pair (sum, count), which is a monoid under componentwise addition, and divide at the end. This is a homomorphism trick: the mean is a function of a monoid value, not a monoid itself.
- **Non-example: powers.** $(2^3)^2 = 64$ but $2^{(3^2)} = 512$, so $x \circ y = x^y$ is not associative.
- **Non-example: positive integers with addition.** $(\mathbb{Z}_{\ge 1}, +)$ is a semigroup with no identity. Adding a new element $e$ with $e + x = x + e = x$ turns any semigroup into a monoid, which is how code adds a neutral value such as $+\infty$ or "none".

## Related definitions

- **[Associative operator](/associative-operator/).** The first law alone. A semigroup is enough for a [disjoint sparse table](/disjoint-sparse-table/) and for a [sparse table](/sparse-table/) of an idempotent operation, which never combine an empty range.
- **[Invertible operation](/invertible-operation/).** A monoid in which each element has an inverse is a group. Then range values are differences of prefix values.
- **[Idempotent operation](/idempotent-operation/).** A monoid with $x \cdot x = x$. Overlapping ranges can then be combined, which gives the $O(1)$ query of the sparse table.
- **[Join-semilattice](/join-semilattice/).** A commutative and idempotent semigroup, such as $\max$ or set union.
- **[Syntactic monoid](/syntactic-monoid/).** The monoid of a regular language in automata theory, an example of a monoid of functions under composition.
- **[Lazy propagation](/lazy-propagation/).** It needs two monoids: the values, and the updates, which act on the values and compose among themselves.

## References
