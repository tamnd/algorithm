---
tag: BYQ21H
kind: problem
slug: counting-parenthesizations
name: Counting the number of parenthesizations
aliases:
- number of bracketings
- counting full parenthesizations
area: combinatorics/counting-algorithms
level: intro
summary: Counting the ways to fully parenthesize a product of n matrices, which grows exponentially and equals a Catalan number.
prereqs: [catalan-numbers, parenthesization]
see_also: [parenthesization, matrix-chain-multiplication, catalan-numbers, counting-balanced-bracket-sequences, catalan-triangulation-theorem, binary-tree, interval-dp, symbolic-method]
sources:
  - book: isbn:9780262046305
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, fourth edition, MIT Press, 2022
    locator: Section 14.2, Matrix-chain multiplication (counting the number of parenthesizations)
  - book: isbn:9781107427747
    title: Richard P. Stanley, Catalan Numbers, Cambridge University Press, 2015
    locator: Chapter 1, Basic properties, and Chapter 2, Bijective exercises (binary parenthesizations of a string)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 2.3.4.4, Enumeration of trees (binary trees and the Catalan numbers)
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 7.5, Convolutions (the Catalan numbers from their generating function)
---

Counting parenthesizations asks in how many ways a product $x_1 x_2 \cdots x_n$ of $n$ factors can be fully parenthesized, so that each step multiplies exactly two neighbouring parts. The answer $P(n)$ is the [Catalan number](/catalan-numbers/) $C_{n-1}$, which grows like $4^n / n^{3/2}$. This exponential growth is the reason [matrix chain multiplication](/matrix-chain-multiplication/) uses a dynamic program over intervals and not a search over all parenthesizations. Related counts, for brackets of any size or for a commutative product, give the Schröder and Wedderburn-Etherington numbers.

## In plain words

You must multiply a row of several matrices, and you may only multiply two neighbours at a time. Brackets show the order: for four matrices, $((AB)C)D$ and $(AB)(CD)$ are two of the possible orders. The question is how many orders there are. Each order is fixed by the last product, which splits the row into a left part and a right part, and then by an order for each part. So the count for a row is a sum of products of counts for shorter rows. These counts grow almost by a factor of four for each extra matrix.

## Definition

**Notation.** $n \ge 1$ is the number of factors, $C(n, k)$ is the binomial coefficient, $[n] = \{1, \ldots, n\}$, and $C_n = \frac{1}{n + 1} C(2n, n)$ is the $n$-th Catalan number.

A *full parenthesization* of $x_1 x_2 \cdots x_n$ is defined recursively: for $n = 1$ it is $x_1$, and for $n \ge 2$ it is $(L)(R)$ for some $k \in [n - 1]$, a full parenthesization $L$ of $x_1 \cdots x_k$ and a full parenthesization $R$ of $x_{k+1} \cdots x_n$. Equivalently, it is a binary tree whose leaves are $x_1, \ldots, x_n$ from left to right and whose internal nodes are the $n - 1$ products, see [parenthesization](/parenthesization/).

**Input:** $n$, and in the variants a rule for which bracketings count, or a modulus.

**Output:** the number $P(n)$ of full parenthesizations, exactly or modulo the given number.

**Theorem.** $P(1) = 1$, $P(n) = \sum_{k=1}^{n-1} P(k)\, P(n - k)$ for $n \ge 2$, and $P(n) = C_{n-1}$.

*Proof.* The recurrence follows from the definition: the last product splits the factors after position $k$, and the choices for the two parts are independent. For the closed form, use induction on $n$. $P(1) = 1 = C_0$. For $n \ge 2$, by the induction hypothesis,

$$P(n) = \sum_{k=1}^{n-1} C_{k-1}\, C_{n-k-1} = \sum_{i=0}^{n-2} C_i\, C_{n-2-i} = C_{n-1},$$

by the Catalan recurrence $C_{m+1} = \sum_{i=0}^{m} C_i C_{m-i}$ with $m = n - 2$, see [counting balanced bracket sequences](/counting-balanced-bracket-sequences/). $\square$

## Variants

- **Partial bracketings.** Allow a bracket to enclose two or more parts, as in $(x_1 x_2 x_3)$, and count the bracketings of $n$ factors in which every bracket has at least two parts and the whole product is one bracket. These are the plane trees with $n$ leaves in which every internal node has at least two children. Their counts for $n = 1, \ldots, 10$ are the little Schröder numbers $1, 1, 3, 11, 45, 197, 903, 4279, 20793, 103049$ (OEIS A001003). Their generating function $S(z)$ satisfies $S = z + \frac{S^2}{1 - S}$: a tree is a leaf, or a root with a sequence of at least two subtrees, see the [symbolic method](/symbolic-method/).
- **A commutative product.** If $xy = yx$ but the product is not associative, count the bracketings of $x^n$ up to swapping the two sides of a product. These are the binary trees with $n$ unlabeled leaves and unordered children, counted by the Wedderburn-Etherington numbers $1, 1, 1, 2, 3, 6, 11, 23, 46, 98, 207$ for $n = 1, \ldots, 11$ (OEIS A001190). For $n = 4$ the two are $((xx)x)x$ and $(xx)(xx)$.
- **Distinct factors in any order.** If the $n$ factors are distinct and may be put in any order, there are $n!\, C_{n-1} = (2n - 2)!/(n - 1)!$ ways: $1, 2, 12, 120, 1680, 30240$ for $n = 1, \ldots, 6$ (OEIS A001813). If, in addition, the two sides of each product are not ordered, the count is $(2n - 3)!! = 1 \cdot 3 \cdots (2n - 3)$: $1, 1, 3, 15, 105, 945$ (OEIS A001147). *Proof.* Insert factor $x_n$ into a tree for $x_1, \ldots, x_{n-1}$ as the sibling of any of its $2n - 3$ nodes. Each tree for $n$ factors arises once, from the tree obtained by removing $x_n$ and its parent. $\square$
- **Modulo a prime.** Compute $C_{n-1} \bmod p$ for huge $n$, as for the Catalan numbers.

## Examples

**Example 1.** The $P(4) = C_3 = 5$ parenthesizations of $ABCD$ are $((AB)C)D$, $(A(BC))D$, $(AB)(CD)$, $A((BC)D)$ and $A(B(CD))$.

**Example 2.** For $n = 1, \ldots, 10$ factors, $P(n) = 1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862$ (OEIS A000108, shifted by one).

**Example 3: why search fails.** A chain of $n = 20$ matrices has $P(20) = C_{19} = 1767263190$ parenthesizations. The interval dynamic program for matrix chain multiplication examines each interval with each of its split points once, which is $\sum_{\ell=2}^{n} (n - \ell + 1)(\ell - 1) = C(n + 1, 3) = 1330$ cases.

## Known algorithms

**Closed form.** $P(n) = C_{n-1} = \frac{(2n - 2)!}{(n - 1)!\, n!}$. Exactly, the product formula costs $O(n)$ multiplications and divisions of an $O(n)$-bit number by an $O(\log n)$-bit number, so $O(n^2)$ word operations, and the result has fewer than $2n$ bits. Modulo a prime $p \ge 2n - 1$ it costs $O(n)$ operations with a factorial table.

**Recurrence.** Fill $P(1), \ldots, P(n)$ by the recurrence with $O(n^2)$ additions and multiplications. This is the natural method when the rule changes, for example when only some splits are allowed, and it is an [interval DP](/interval-dp/) with all intervals of the same length treated alike.

**Listing.** Generating all binary trees with $n$ leaves takes time proportional to $C_{n-1}$ times the cost per tree. Use it only to test counts for small $n$.

## Bounds

- **Growth.** $C_{n-1} \sim \frac{4^{n-1}}{\sqrt{\pi}\, (n - 1)^{3/2}}$, so $P(n) = \Theta(4^n / n^{3/2})$.
- **A simple lower bound.** $P(n) \ge 2^{n-2}$ for $n \ge 2$. *Proof.* $C_1 = 1$ and $C_{k+1}/C_k = \frac{2(2k + 1)}{k + 2} \ge 2$ for $k \ge 1$, so $C_k \ge 2^{k-1}$ for $k \ge 1$. $\square$ This alone shows that trying all parenthesizations takes exponential time.
- **Size of the answer.** $P(n) < 4^{n-1}$ for $n \ge 2$, so it has fewer than $2n - 2$ bits.

## Reductions

- Full parenthesizations of $n$ factors correspond one to one to binary trees with $n - 1$ internal nodes, to triangulations of a convex polygon with $n + 1$ sides (the [Catalan triangulation theorem](/catalan-triangulation-theorem/)), and to balanced bracket sequences with $n - 1$ pairs. All these families satisfy the same recurrence with the same start, so the counts agree.
- The parenthesizations are the vertices of the associahedron, and two are adjacent when one application of the associative law $(xy)z = x(yz)$ turns one into the other. In terms of binary trees, this move is a rotation.
- Counting parenthesizations is the counting version of [matrix chain multiplication](/matrix-chain-multiplication/): the same interval recurrence with sum and product in place of minimum and addition.

## Applications

- **Matrix chain multiplication.** The count shows that the cost of the obvious search is exponential and motivates the $O(n^3)$ dynamic program.
- **Join ordering in databases.** The bushy plans for joining $n$ relations, with the order of the relations free, are the parenthesizations of $n$ distinct factors in any order, counted by $n!\, C_{n-1}$.
- **Floating-point summation.** The order of additions in a sum of $n$ floating-point numbers changes the rounding error, and the number of possible orders without reordering the terms is $C_{n-1}$.
- **Teaching recurrences.** It is a standard first example of a convolution recurrence and of a quantity counted by Catalan numbers.

## References
