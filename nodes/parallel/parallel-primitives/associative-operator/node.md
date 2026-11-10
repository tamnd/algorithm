---
tag: TY4KFS
kind: definition
slug: associative-operator
name: Associative operator
aliases:
- semigroup operation
area: parallel/parallel-primitives
level: intro
summary: A binary operation with (a·b)·c = a·(b·c), needed for parallel reduction and scan.
prereqs: [induction]
see_also: [monoid, parallel-reduce, all-prefix-sums, segmented-scan, idempotent-operation, invertible-operation, floating-point-summation, reproducible-summation]
sources:
  - book: isbn:9780387953854
    title: Serge Lang, Algebra, revised third edition (Graduate Texts in Mathematics 211), Springer, 2002
    locator: Chapter I, Section 1 (monoids, and the general associativity of a product of n elements)
  - url: https://www.cs.cmu.edu/~guyb/papers/Ble93.pdf
    title: Guy E. Blelloch, Prefix Sums and Their Applications, Technical Report CMU-CS-90-190, Carnegie Mellon University, 1990; also Chapter 1 of John H. Reif (editor), Synthesis of Parallel Algorithms, Morgan Kaufmann, 1993
    locator: Section 1.1 (the scan of a binary associative operator) and Section 1.2 (the reduce needs associativity but not commutativity, because the order of the operands is kept)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 4, Summation (the error of recursive and pairwise summation depends on the order of the additions)
  - paper: doi:10.1145/103162.103163
    title: David Goldberg, What every computer scientist should know about floating-point arithmetic, ACM Computing Surveys 23(1), 1991
    locator: Section 1 (rounding error, ulps and relative error) and Section 3, Systems Aspects (the part on compiler optimizations, which must not regroup floating-point sums)
---

An associative operator is a binary operation $\oplus$ on a set $S$ with $(a \oplus b) \oplus c = a \oplus (b \oplus c)$ for all $a, b, c \in S$. By [induction](/induction/), this law of three elements gives the same result for every bracketing of a longer expression $a_1 \oplus a_2 \oplus \cdots \oplus a_n$, as long as the order of the operands does not change. This is the property that lets a [parallel reduce](/parallel-reduce/) or a parallel [scan](/all-prefix-sums/) group the operands in a balanced tree instead of from left to right. Commutativity is not necessary, but floating-point addition, which is commutative, is not associative, so parallel sums of floating-point numbers can differ from sequential ones.

## Definition

Let $S$ be a set and let $\oplus : S \times S \to S$ be a function, written in infix form. The operation $\oplus$ is **associative** if

$$ (a \oplus b) \oplus c = a \oplus (b \oplus c) \qquad \text{for all } a, b, c \in S. $$

The pair $(S, \oplus)$ is then a *semigroup*, and $\oplus$ is a semigroup operation. An element $e \in S$ is an **identity** if $e \oplus a = a = a \oplus e$ for all $a \in S$. A semigroup with an identity is a [monoid](/monoid/). The identity is unique when it exists: if $e$ and $e'$ are both identities, then $e = e \oplus e' = e'$. The operation is **commutative** if $a \oplus b = b \oplus a$ for all $a, b$. Associativity and commutativity are independent laws: each one can hold without the other.

### Any bracketing gives the same result

A *bracketing* of the sequence $a_1, \ldots, a_n$ (with $n \ge 1$) is a full binary tree whose leaves are $a_1, \ldots, a_n$ from left to right. Each inner node applies $\oplus$ to the values of its left and right subtrees, in that order. For $n = 4$ there are 5 bracketings, and in general there are $C_{n-1}$ of them, where $C_k$ is the $k$-th [Catalan number](/catalan-numbers/). Define the left fold $L(a_1, \ldots, a_n)$ by $L(a_1) = a_1$ and $L(a_1, \ldots, a_n) = L(a_1, \ldots, a_{n-1}) \oplus a_n$.

**Lemma.** If $\oplus$ is associative, then $L(a_1, \ldots, a_k) \oplus L(a_{k+1}, \ldots, a_n) = L(a_1, \ldots, a_n)$ for all $1 \le k < n$.

*Proof.* By induction on $n - k$. If $n - k = 1$, the right operand is $a_n$, and the equation is the definition of $L$. If $n - k \ge 2$, write $u = L(a_1, \ldots, a_k)$ and $v' = L(a_{k+1}, \ldots, a_{n-1})$. By the definition of $L$, the left side is $u \oplus (v' \oplus a_n)$. Associativity turns it into $(u \oplus v') \oplus a_n$. The induction hypothesis for the pair $(k, n - 1)$, whose difference is $n - 1 - k$, gives $u \oplus v' = L(a_1, \ldots, a_{n-1})$. So the left side is $L(a_1, \ldots, a_{n-1}) \oplus a_n = L(a_1, \ldots, a_n)$. $\square$

**Theorem (general associativity).** If $\oplus$ is associative, then every bracketing of $a_1, \ldots, a_n$ has the value $L(a_1, \ldots, a_n)$.

*Proof.* By strong induction on $n$. For $n = 1$ the only bracketing is the leaf $a_1 = L(a_1)$. For $n \ge 2$, the root of the tree splits the leaves at some $k$ with $1 \le k < n$: the left subtree is a bracketing of $a_1, \ldots, a_k$ and the right subtree is a bracketing of $a_{k+1}, \ldots, a_n$. Both have fewer than $n$ leaves, so by the induction hypothesis their values are $L(a_1, \ldots, a_k)$ and $L(a_{k+1}, \ldots, a_n)$. The root combines them, and the lemma gives $L(a_1, \ldots, a_n)$. $\blacksquare$

So the expression $a_1 \oplus \cdots \oplus a_n$ has one meaning, and an algorithm may evaluate it in any tree shape. A balanced tree has depth $\lceil \lg n \rceil$, which is why a reduce has [span](/work-and-span/) $O(\log n)$. Each output of a scan is a prefix $a_1 \oplus \cdots \oplus a_i$, and the theorem lets a scan algorithm build that prefix from partial results of other prefixes and of blocks.

### The identity element

An identity is not needed to define the reduce of a non-empty sequence or the inclusive scan. It is needed for three common things: the value of the reduce of an empty sequence, the first output of an exclusive scan (the empty prefix), and the padding of an input to a power of two, as in the [Blelloch scan](/blelloch-scan/). A semigroup without an identity can always get one. Add a new element $e \notin S$ and define $e \oplus x = x \oplus e = x$ for all $x \in S \cup \{e\}$. The extended operation is associative: in a check of $(x \oplus y) \oplus z = x \oplus (y \oplus z)$, each operand equal to $e$ can be removed from both sides, and the remaining case is the law in $S$.

### Commutativity is not needed

A reduce or a scan that keeps the operands in their input order never uses $a \oplus b = b \oplus a$. The theorem above only moves brackets. So string concatenation and the product of matrices, which are not commutative, are correct operators for a tree reduce and for every scan algorithm in this area, as long as each combine puts the left part on the left. Commutativity becomes necessary only when the algorithm changes the order of the operands. Examples are a sum into one memory cell by atomic adds from many threads in any order, a reduce that combines partial results in the order in which they finish, and a hash-partitioned reduce in [MapReduce](/mapreduce-model/), where the values of one key arrive in no fixed order.

## Examples and non-examples

**Associative operators.**

| operator on $S$ | identity | commutative |
|---|---|---|
| $+$ and $\times$ on the integers | $0$ and $1$ | yes |
| $\max$ and $\min$ on the integers | $-\infty$ and $+\infty$ (adjoined) | yes |
| $\gcd$ on the non-negative integers | $0$ | yes |
| and, or, exclusive or on booleans | true, false, false | yes |
| concatenation of strings | the empty string | no |
| product of $2 \times 2$ matrices | the identity matrix | no |
| composition of functions $S \to S$ | the identity function | no |
| $a \oplus b = a$ (keep the first) | none | no |

The last row is a semigroup with no identity: $(a \oplus b) \oplus c = a = a \oplus (b \oplus c)$, but $e \oplus a = e$, so no $e$ works for all $a$. A segmented scan uses it to copy the first element of each segment to the whole segment.

**Linear recurrences.** The recurrence $x_i = m_i x_{i-1} + c_i$ looks sequential. Represent step $i$ by the pair $(m_i, c_i)$, which stands for the map $x \mapsto m_i x + c_i$. Doing step $(m_1, c_1)$ and then step $(m_2, c_2)$ is the map $x \mapsto m_2(m_1 x + c_1) + c_2$, so define $(m_1, c_1) \oplus (m_2, c_2) = (m_1 m_2, m_2 c_1 + c_2)$. This is the composition of affine maps, so it is associative, and a scan of the pairs gives every $x_i$. The [carry-lookahead adder](/carry-lookahead-adder/) uses the same idea with the (generate, propagate) pairs of the bits, and the [segmented scan](/segmented-scan/) uses it with (flag, value) pairs.

**Subtraction is not associative.** $(5 - 3) - 1 = 1$ but $5 - (3 - 1) = 3$. The 5 bracketings of $8 - 4 - 2 - 1$ give the values 1, 5, 3, 7 and 5. A parallel reduce with $-$ therefore gives a value that depends on the tree. Division, exponentiation ($(2^3)^2 = 64$ but $2^{(3^2)} = 512$) and the mean of two numbers are not associative either. A sum of differences can still be computed in parallel: rewrite $a_1 - a_2 - \cdots - a_n$ as $a_1 + (-a_2) + \cdots + (-a_n)$.

**Floating-point addition is not associative.** In [IEEE 754](/ieee-754/) double precision with rounding to nearest, each addition rounds its exact result. So

$$ (0.1 + 0.2) + 0.3 = 0.6000000000000001, \qquad 0.1 + (0.2 + 0.3) = 0.6. $$

A larger effect comes from the spacing of doubles. Near $10^{16}$ the distance between two doubles is 2, so $10^{16} + 1$ is a tie, and [round to nearest even](/round-to-nearest-even/) gives $10^{16}$. Then

$$ (10^{16} + 1) + 1 = 10^{16}, \qquad 10^{16} + (1 + 1) = 10^{16} + 2. $$

Take the list of nine numbers $10^{16}, 1, 1, 1, 1, 1, 1, 1, 1$, with exact sum $10^{16} + 8$. A sequential left-to-right loop gives $10^{16}$, because each $+1$ is lost. A balanced tree that splits each part into a left part of $\lceil n/2 \rceil$ items and a right part gives $10^{16} + 6$. A sum that adds the eight ones first gives the exact $10^{16} + 8$. Floating-point addition is commutative, so the difference comes only from the brackets.

The consequences for parallel code:

- A parallel sum of floating-point numbers is in general not equal to the sequential sum. It can also change from run to run when the tree shape depends on the number of threads, the chunk size or the schedule.
- The error bound of a sum depends on its tree. For recursive (left-to-right) summation the bound grows with $n$, and for [pairwise summation](/pairwise-summation/) it grows with $\lg n$, so a balanced tree is often more accurate than the sequential loop (Higham, Chapter 4).
- A program that needs the same bits on each run must fix the tree shape independently of the number of processors, or use [reproducible summation](/reproducible-summation/). [Compensated summation](/kahan-summation/) reduces the error but does not by itself make the result independent of the order.

The maximum and the minimum of floating-point numbers are associative, because they only compare and never round, as long as no operand is a NaN.

## Related definitions

- **[Monoid](/monoid/).** An associative operator with an identity. Most scan algorithms assume a monoid.
- **Commutative operator.** $a \oplus b = b \oplus a$. Not needed for an ordered reduce or scan. Needed when partial results are combined in an order that the program does not control.
- **[Idempotent operation](/idempotent-operation/).** $a \oplus a = a$, as for $\max$, $\min$ and $\gcd$. With idempotence, overlapping parts can be combined, as in a sparse table.
- **[Invertible operation](/invertible-operation/).** Each element has an inverse, as for $+$ on the integers. Then a range result is a difference of two prefix results, as in [prefix sums](/prefix-sums/).
- **Semiassociative operator.** Blelloch uses a weaker law for a pair of operators, one of them associative, to solve recurrences by a scan (Prefix Sums and Their Applications, Section 1.4).
- **The users.** [Parallel reduce](/parallel-reduce/), [all-prefix-sums](/all-prefix-sums/), the [Hillis-Steele scan](/hillis-steele-scan/), the [Blelloch scan](/blelloch-scan/), [parallel prefix](/parallel-prefix/) circuits and the [segmented scan](/segmented-scan/) all need an associative operator, and give a result that does not depend on the tree only because of the theorem above.

## References
