---
tag: C390V9
kind: concept
slug: permutation-cycle-decomposition
name: Cycle decomposition of a permutation
aliases:
- cycle notation
- disjoint cycles
- cycle type
area: combinatorics/generating-permutations
level: core
summary: Writes a permutation as a product of disjoint cycles.
prereqs: [permutation]
see_also: [permutation-cycles, permutation-sign, stirling-numbers-first-kind, cycle-leader-permutation, permutation-power, symmetric-group, sattolo-algorithm, generating-involutions]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 1.3.3, Applications to permutations (cycle notation, products of permutations in cycle form, and the inverse of a permutation)
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Section 1.3 (the cycle type, the number of permutations of a given type, the standard representation and the fundamental bijection)
  - book: isbn:9780471433347
    title: David S. Dummit and Richard M. Foote, Abstract Algebra, third edition, Wiley, 2004
    locator: Section 1.3 (cycle decomposition in the symmetric group) and Section 4.3 (conjugacy classes of S_n correspond to cycle types)
---

The cycle decomposition writes a [permutation](/permutation/) $\pi$ of $[n]$ as a product of disjoint cycles: start at an item, follow $i \to \pi(i) \to \pi(\pi(i)) \to \cdots$ until the walk returns, and repeat from an item not yet seen. The cycles are unique, and they reveal what the one-line form hides: the [sign](/permutation-sign/), the order, the inverse, and the conjugacy class in the [symmetric group](/symmetric-group/). One pass with a visited mark finds all cycles in $O(n)$ time, and counting by cycle type explains the [Stirling numbers of the first kind](/stirling-numbers-first-kind/).

## In plain words

Give each person in a room a card with the name of another person, so that each name is on exactly one card. Start with one person, go to the person named on that card, then to the person named on the next card, and so on. You always come back to the start. This loop is a cycle.

If some people are not on that loop, start again with one of them. In the end the room splits into loops, and every person is in exactly one loop. The list of loops describes the whole card game, and many facts about it, such as how many rounds of passing the cards take to get back to the start, can be read from the loop lengths.

## The idea

**Cycles.** A $k$-cycle $(a_1\ a_2\ \cdots\ a_k)$ is the permutation that sends $a_1 \mapsto a_2 \mapsto \cdots \mapsto a_k \mapsto a_1$ and fixes all other items. Since $\pi$ is a bijection of a finite set, the walk $i, \pi(i), \pi^2(i), \ldots$ must return to $i$: the first repeated item cannot have two different predecessors on the walk. So the items split into disjoint orbits, and $\pi$ is the product of the cycles of the orbits. Disjoint cycles commute, so the order of the factors does not matter. The orbits, and so the cycles, are fixed by $\pi$, which makes the decomposition unique up to the order of the factors and the starting item of each cycle. The page on [permutation cycles](/permutation-cycles/) gives more detail.

**Writing cycles in a standard way.** Two common rules make the written form unique:

- smallest item first in each cycle, cycles in increasing order of their first items;
- largest item first in each cycle, cycles in increasing order of their first items. This is Stanley's *standard representation*. If the parentheses are erased, the result is a one-line permutation, and the cycles can be recovered: a new cycle starts at each item larger than all items before it. This *fundamental bijection*, also called Foata's transformation, maps permutations with $c$ cycles to permutations with $c$ left-to-right maxima.

**From one-line form to cycles.** Keep a boolean mark for each item. For $i = 1, \ldots, n$, if $i$ is not marked, follow the walk from $i$, mark each item, and write out the cycle. Each item is marked once, so this takes $\Theta(n)$ time and $n$ extra bits. Without extra memory, an item $i$ can test whether it is the smallest item of its cycle by walking the cycle; this is the method of [cycle leaders](/cycle-leader-permutation/).

**From cycles to one-line form.** For each cycle $(a_1\ \cdots\ a_k)$, set $\pi(a_j) = a_{j+1}$ and $\pi(a_k) = a_1$. This takes $\Theta(n)$ time. A product of cycles that are *not* disjoint must be composed one factor at a time; with the rule that the right factor acts first, $(1\ 2)(2\ 3) = (1\ 2\ 3)$, while $(2\ 3)(1\ 2) = (1\ 3\ 2)$. Knuth gives algorithms that multiply permutations given in cycle form.

**Cycle type.** The *cycle type* of $\pi$ is the multiset of its cycle lengths, an integer partition of $n$. If $m_k$ is the number of cycles of length $k$, then the number of permutations of $[n]$ with this type is

$$\frac{n!}{\prod_k k^{m_k}\, m_k!}.$$

*Reason.* Write the $n$ items in a row in any of $n!$ ways, and cut the row into cycles of the given lengths in a fixed pattern. Each permutation of the type arises $\prod_k k^{m_k} m_k!$ times: each $k$-cycle can start at any of its $k$ items, and the $m_k$ cycles of length $k$ can come in any of $m_k!$ orders.

**What the cycles tell.** Let $\pi$ have $c$ cycles, counting fixed points.

- *Sign.* $\operatorname{sgn}(\pi) = (-1)^{n - c}$, since a $k$-cycle is a product of $k - 1$ transpositions.
- *Order.* The smallest $m \ge 1$ with $\pi^m = \text{id}$ is the [least common multiple](/least-common-multiple/) of the cycle lengths.
- *Inverse.* $\pi^{-1}$ has the same cycles, each read backwards.
- *Powers.* $\pi^m$ splits a $k$-cycle into $\gcd(k, m)$ cycles of length $k / \gcd(k, m)$. See [permutation power](/permutation-power/).
- *Conjugacy.* Two permutations are conjugate in $S_n$, that is $\sigma = \tau \pi \tau^{-1}$ for some $\tau$, exactly when they have the same cycle type. So the conjugacy classes of $S_n$ match the partitions of $n$.
- *Distance.* The least number of transpositions whose product is $\pi$ is $n - c$. This is the [Cayley distance](/cayley-distance/) from $\pi$ to the identity.

**Generation by cycles.** The recurrence ${n \brack c} = {n-1 \brack c-1} + (n-1){n-1 \brack c}$ of the Stirling numbers is a recipe for listing permutations with $c$ cycles: either $n$ forms a cycle alone, or it is inserted just after one of the other $n - 1$ items in its cycle. Lists of permutations by cycle type, of [involutions](/generating-involutions/) (all cycles of length at most 2), of derangements (no cycle of length 1) and of cyclic permutations (one cycle of length $n$) all use the cycle view.

## Examples

**One permutation.** Let $\pi = 2\,4\,1\,3\,6\,5$, so $\pi(1) = 2$, $\pi(2) = 4$, and so on. The walk from 1 is $1 \to 2 \to 4 \to 3 \to 1$, and the walk from 5 is $5 \to 6 \to 5$. So

$$\pi = (1\ 2\ 4\ 3)(5\ 6).$$

The cycle type is $(4, 2)$, $c = 2$, the sign is $(-1)^{6 - 2} = +1$, the order is $\operatorname{lcm}(4, 2) = 4$, and $\pi^{-1} = (1\ 3\ 4\ 2)(5\ 6) = 3\,1\,4\,2\,6\,5$. In the standard representation, $\pi = (4\ 3\ 1\ 2)(6\ 5)$, and erasing the parentheses gives $4\,3\,1\,2\,6\,5$, whose left-to-right maxima 4 and 6 mark the two cycles.

**A single cycle.** $3\,1\,4\,5\,2 = (1\ 3\ 4\ 5\ 2)$, a 5-cycle. Its sign is $+1$ and its order is 5. Its standard representation is $(5\ 2\ 1\ 3\ 4)$, and the fundamental bijection maps it to $5\,2\,1\,3\,4$, which has one left-to-right maximum.

**Cycle types of $S_4$.**

| cycle type | example | count | sign |
|---|---|---|---|
| 1 1 1 1 | identity | 1 | + |
| 2 1 1 | (1 2) | 6 | − |
| 2 2 | (1 2)(3 4) | 3 | + |
| 3 1 | (1 2 3) | 8 | + |
| 4 | (1 2 3 4) | 6 | − |

The counts add to 24, and the 12 even permutations are the types 1111, 22 and 31. In $S_6$, the type $(3, 2, 1)$ has $720 / (3 \cdot 2 \cdot 1) = 120$ permutations, the type $(2, 2, 2)$ has $720 / (2^3 \cdot 3!) = 15$, and the 6-cycles number $720 / 6 = 120$. There are 11 types in all, one for each partition of 6.

**Number of cycles.** For $n = 5$, the numbers of permutations with $1, 2, 3, 4, 5$ cycles are $24, 50, 35, 10, 1$, the Stirling numbers ${5 \brack c}$.

## Where it is used

- **Permuting data in place.** To apply a permutation to an array without a second array, move the items around each cycle with one temporary item, as in the [cycle leader](/cycle-leader-permutation/) method and in in-place matrix transposition.
- **Sign and parity.** The [sign](/permutation-sign/) from the cycle count takes $O(n)$ time, faster than counting inversions. This decides the solvability of puzzles such as the [15-puzzle](/sliding-puzzle-solvability/).
- **Powers and orders.** The order of a permutation, and $\pi^m$ for a huge $m$, come from the cycle lengths, as when a card shuffle is repeated until the deck returns to its start.
- **Counting under symmetry.** The [Pólya enumeration theorem](/polya-enumeration-theorem/) and [Burnside's lemma](/burnside-lemma/) count objects up to symmetry by the cycle types of the symmetries.
- **Random permutations.** [Sattolo's algorithm](/sattolo-algorithm/) produces a uniform [random cyclic permutation](/random-cyclic-permutation/), one with a single $n$-cycle.

## References
