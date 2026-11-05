---
tag: ZBG6RS
kind: concept
slug: symmetric-group
name: Symmetric group
aliases:
- permutation group S_n
area: sequences/inversions-and-permutations
level: core
summary: The group of all permutations of n elements under composition.
prereqs: [permutation, permutation-cycles, permutation-inverse]
see_also: [finite-group, subgroup, permutation-parity, cayley-distance, sorting-by-adjacent-swaps, pancake-sorting, permutation-power, rubiks-cube-problem]
sources:
  - book: isbn:9780471433347
    title: David S. Dummit and Richard M. Foote, Abstract Algebra, third edition, Wiley, 2004
    locator: Section 1.3 (the symmetric groups), Section 3.5 (transpositions and the alternating group) and Section 4.3 (conjugacy classes in S_n)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.3.3 (applications to permutations, multiplication of permutations and cycle notation)
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Chapter 1, Section 1.3 (cycle type and the number of permutations of a given type)
---

The symmetric group $S_n$ is the set of all $n!$ [permutations](/permutation/) of $[n] = \{1, \ldots, n\}$, with composition as the operation. It is a [finite group](/finite-group/): composition is associative, the identity permutation is the neutral element, and every permutation has an [inverse](/permutation-inverse/). For $n \ge 3$ it is not commutative. Its structure is read from [cycles](/permutation-cycles/): conjugacy classes are cycle types, the order of an element is the least common multiple of its cycle lengths, and the [parity](/permutation-parity/) splits it into two halves. Many sorting and puzzle problems are shortest-path problems in $S_n$ with a fixed set of allowed moves.

## In plain words

Take $n$ objects in a row. Every way to rearrange them is a member of the group, so there are $n$ factorial members. Doing one rearrangement and then another is again a rearrangement, so members combine. Doing nothing is a member, and every rearrangement can be undone by another.

The order of combining matters. Swap the first two objects and then the last two, and you get a different row than if you do the two swaps the other way round.

A whole area of algorithms lives here. Sorting by swapping neighbors, by flipping the top of a stack, or by any swap at all, asks for the shortest way to undo a member of this group using only certain moves. Puzzles like the Rubik's cube work the same way with a smaller set of reachable members.

## The idea

**The group.** For $\sigma, \tau \in S_n$, the product $\sigma\tau$ is the composition $(\sigma\tau)(i) = \sigma(\tau(i))$: apply $\tau$ first. Some books use the other order; both give the same group, with each product written in reverse. In one-line notation the product takes $O(n)$ time, as does the inverse.

**Size and subgroups.** $|S_n| = n!$. By Lagrange's theorem the size of every [subgroup](/subgroup/) divides $n!$. The even permutations form the *alternating group* $A_n$, a subgroup of size $n!/2$ for $n \ge 2$. Cayley's theorem says that every group $G$ of size $n$ is isomorphic to a subgroup of $S_n$, by letting each $g$ act on the elements of $G$ by $x \mapsto gx$. So the symmetric groups contain all finite groups.

**Generators.** Each of these sets generates $S_n$:

- the transpositions $(i\ j)$, since a $k$-cycle is a product of $k - 1$ of them;
- the adjacent transpositions $s_i = (i\ \ i+1)$, $1 \le i < n$, since $(i\ j)$ with $i < j$ is $s_i s_{i+1} \cdots s_{j-2}\, s_{j-1}\, s_{j-2} \cdots s_i$;
- the prefix reversals, which give the [pancake graph](/pancake-sorting/);
- the two permutations $(1\ 2)$ and $(1\ 2\ \cdots\ n)$, since conjugating $(1\ 2)$ by powers of the $n$-cycle gives every $s_i$.

The adjacent transpositions satisfy $s_i^2 = 1$, $s_i s_{i+1} s_i = s_{i+1} s_i s_{i+1}$ and $s_i s_j = s_j s_i$ for $|i - j| \ge 2$, and these relations define $S_n$: it is the Coxeter group of type $A_{n-1}$. The least number of adjacent transpositions whose product is $\pi$, the *length* of $\pi$, is $\operatorname{inv}(\pi)$.

**Cayley graphs and distances.** For a generating set $X$ closed under inverses, the Cayley graph has the $n!$ permutations as vertices and an edge from $\pi$ to $\pi x$ for each $x \in X$. Its distance from $\pi$ to the identity is the least number of moves from $X$ that sort $\pi$:

| generators | distance to the identity | page |
| --- | --- | --- |
| adjacent transpositions | $\operatorname{inv}(\pi)$ | [sorting by adjacent swaps](/sorting-by-adjacent-swaps/) |
| all transpositions | $n$ minus the number of cycles | [Cayley distance](/cayley-distance/) |
| prefix reversals | the pancake distance, NP-hard | [pancake sorting](/pancake-sorting/) |
| all reversals | the reversal distance, NP-hard | [sorting by reversals](/sorting-by-reversals/) |
| block transpositions | the transposition distance, NP-hard | [sorting by transpositions](/sorting-by-transpositions/) |

Since $\pi \mapsto \rho\pi$ is an automorphism of every Cayley graph, the distance between $\sigma$ and $\tau$ is the distance from $\tau^{-1}\sigma$ to the identity. This turns each distance between two arrangements into a sorting problem.

**Conjugacy classes.** $\rho\pi\rho^{-1}$ has the cycles of $\pi$ with every item $x$ renamed $\rho(x)$. So two permutations are conjugate exactly when they have the same cycle type, and the conjugacy classes of $S_n$ correspond to the partitions of $n$. The number of permutations with $m_k$ cycles of length $k$ for each $k$ is
$$\frac{n!}{\prod_k k^{m_k}\, m_k!},$$
because each of the $n!$ ways to fill the cycle pattern with items in order is counted once for each of the $k$ starting points of each $k$-cycle and each of the $m_k!$ orders of the cycles of length $k$.

**Orders of elements.** The order of $\pi$ is the least common multiple of its cycle lengths, see [powers of a permutation](/permutation-power/). The largest order of an element of $S_n$ is Landau's function $g(n)$, the largest least common multiple of a partition of $n$: $1, 2, 3, 4, 6, 6, 12, 15, 20, 30$ for $n = 1, \ldots, 10$. It grows like $e^{(1 + o(1))\sqrt{n \ln n}}$.

**Algorithms on subgroups.** A subgroup of $S_n$ given by a few generators can have size up to $n!$, but its order, a membership test and a way to write an element in terms of the generators can be computed in time polynomial in $n$ and the number of generators by the Schreier-Sims algorithm, which builds a chain of point stabilizers. Computer algebra systems use it for puzzles such as the [Rubik's cube](/rubiks-cube-problem/).

## Examples

**$S_3$.** Its six elements are the identity $123$, the transpositions $213 = (1\ 2)$, $132 = (2\ 3)$, $321 = (1\ 3)$, and the 3-cycles $231 = (1\ 2\ 3)$ and $312 = (1\ 3\ 2)$. It is not commutative: $(1\ 2)(2\ 3) = 231$, while $(2\ 3)(1\ 2) = 312$. The alternating group $A_3 = \{123, 231, 312\}$ is a cyclic subgroup of order 3.

**Conjugacy classes of $S_4$.** The five partitions of 4 give five classes:

| cycle type | example | size |
| --- | --- | --- |
| $1^4$ | the identity | 1 |
| $2\,1^2$ | $(1\ 2)$ | 6 |
| $2^2$ | $(1\ 2)(3\ 4)$ | 3 |
| $3\,1$ | $(1\ 2\ 3)$ | 8 |
| $4$ | $(1\ 2\ 3\ 4)$ | 6 |

The sizes add up to $24 = 4!$, and each matches the formula, for example $4!/(2^2 \cdot 2!) = 3$. The even classes are $1^4$, $2^2$ and $3\,1$, with $1 + 3 + 8 = 12$ elements, the group $A_4$.

**An element of order 6 in $S_5$.** $(1\ 2\ 3)(4\ 5)$ has order $\operatorname{lcm}(3, 2) = 6$, the largest possible in $S_5$ and in $S_6$.

**A transposition from adjacent ones.** $(1\ 3) = s_1 s_2 s_1$: applying $s_1$, then $s_2$, then $s_1$ to $1\,2\,3$ moves the entries $1\,2\,3 \to 2\,1\,3 \to 2\,3\,1 \to 3\,2\,1$. This uses 3 adjacent swaps, the number of inversions of $321$.

## Where it is used

- **Sorting and rearrangement.** Every sorting problem with a fixed kind of move is a distance problem in a Cayley graph of $S_n$, as in the table above.
- **Ranking comparison.** Distances between rankings such as the [Kendall tau distance](/kendall-tau-distance/) and the [Cayley distance](/cayley-distance/) are invariant under relabeling, which is the group action $\pi \mapsto \rho\pi$.
- **Puzzles.** The Rubik's cube group and the fifteen puzzle are subgroups of symmetric groups, and their solvability conditions come from parity and from the subgroup structure.
- **Determinants and algebra.** The Leibniz formula sums over $S_n$, and the representation theory of $S_n$ underlies the combinatorics of Young tableaux.
- **Card shuffling.** A shuffle is a random walk on $S_n$, and the number of shuffles needed to mix a deck is a question about this walk.

## References
