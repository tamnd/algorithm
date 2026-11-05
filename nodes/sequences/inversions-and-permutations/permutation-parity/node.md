---
tag: DK3GQC
kind: concept
slug: permutation-parity
name: Parity of a permutation
aliases:
- sign of a permutation
area: sequences/inversions-and-permutations
level: core
summary: Even or odd according to the parity of its inversion count or number of transpositions.
prereqs: [inversion, permutation-cycles]
see_also: [permutation-sign, symmetric-group, cayley-distance, determinant, sliding-puzzle-solvability, rubiks-cube-problem, mahonian-numbers, sorting-by-adjacent-swaps]
sources:
  - book: isbn:9780471433347
    title: David S. Dummit and Richard M. Foote, Abstract Algebra, third edition, Wiley, 2004
    locator: Section 3.5 (transpositions and the alternating group, the sign of a permutation)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.3.3 (applications to permutations, products of cycles)
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Chapter 1, Section 1.3 (cycles and inversions of permutations)
---

A [permutation](/permutation/) is even if it has an even number of [inversions](/inversion/) and odd otherwise, and its sign is $\operatorname{sgn}(\pi) = (-1)^{\operatorname{inv}(\pi)}$. The same parity is the parity of $n$ minus the number of [cycles](/permutation-cycles/), and of the length of every way to write $\pi$ as a product of transpositions. The sign is multiplicative, $\operatorname{sgn}(\sigma\tau) = \operatorname{sgn}(\sigma)\operatorname{sgn}(\tau)$, which makes it the basic invariant behind the [determinant](/determinant/), the solvability of the [fifteen puzzle](/sliding-puzzle-solvability/) and the alternating group. From the cycles it takes $\Theta(n)$ time, faster than counting the inversions.

## In plain words

Shuffle a row of numbered cards by swapping two cards at a time. Some shuffles can be done in an even number of swaps and some in an odd number, and no shuffle can be done both ways. That is the parity of the shuffle.

One way to see it is to count the pairs of cards in the wrong order. Swapping two cards always changes this count by an odd amount, so each swap flips the count between even and odd. A sorted row has zero wrong pairs, an even number.

So the parity can be read off from the wrong pairs. It can also be read off from the loops of the shuffle: a loop of $k$ cards takes $k - 1$ swaps to undo. Puzzles use this: a sliding puzzle position with the wrong parity can never be solved.

## The idea

**Definition.** For $\pi \in S_n$, $\operatorname{sgn}(\pi) = (-1)^{\operatorname{inv}(\pi)}$. The permutation is *even* when $\operatorname{sgn}(\pi) = 1$ and *odd* when $\operatorname{sgn}(\pi) = -1$. The [sign of a permutation](/permutation-sign/) page treats the sign as a function to compute.

**The product formula.** For every $\pi \in S_n$,
$$\operatorname{sgn}(\pi) = \prod_{1 \le i < j \le n} \frac{\pi(j) - \pi(i)}{j - i}.$$
The pairs $\{\pi(i), \pi(j)\}$ run over all pairs of distinct values exactly once, so the absolute value of the numerator equals the denominator. The factor for $(i, j)$ is negative exactly when $(i, j)$ is an inversion.

**Theorem (multiplicativity).** $\operatorname{sgn}(\sigma\tau) = \operatorname{sgn}(\sigma)\operatorname{sgn}(\tau)$ for all $\sigma, \tau \in S_n$.

*Proof.* Write
$$\operatorname{sgn}(\sigma\tau) = \prod_{i<j} \frac{\sigma(\tau(j)) - \sigma(\tau(i))}{\tau(j) - \tau(i)} \cdot \prod_{i<j} \frac{\tau(j) - \tau(i)}{j - i}.$$
The second product is $\operatorname{sgn}(\tau)$. In the first, the factor $\frac{\sigma(y) - \sigma(x)}{y - x}$ does not change when $x$ and $y$ are exchanged, and as $(i, j)$ runs over the pairs $i < j$, the set $\{x, y\} = \{\tau(i), \tau(j)\}$ runs over all pairs of distinct items once. So the first product is $\prod_{x < y} \frac{\sigma(y) - \sigma(x)}{y - x} = \operatorname{sgn}(\sigma)$. $\square$

**Transpositions are odd.** The transposition $(i\ j)$ with $i < j$ has $2(j - i - 1) + 1$ inversions: the pair $(i, j)$ itself, and for each $k$ between $i$ and $j$ the two pairs $(i, k)$ and $(k, j)$. So its sign is $-1$. On the [inversion](/inversion/) page the same fact appears as: exchanging two entries of any sequence changes the inversion count by an odd number.

**Consequences.**

- **Products of transpositions.** If $\pi = t_1 t_2 \cdots t_m$ with transpositions $t_k$, then $\operatorname{sgn}(\pi) = (-1)^m$. So every such product for $\pi$ has a length of the same parity, the parity of $\operatorname{inv}(\pi)$.
- **Cycles.** A $k$-cycle is a product of $k - 1$ transpositions, so its sign is $(-1)^{k-1}$, and a permutation with $c$ cycles, fixed points included, has $\operatorname{sgn}(\pi) = (-1)^{n - c}$. Equivalently, $\pi$ is odd exactly when it has an odd number of cycles of even length.
- **The minimum.** The fewest transpositions that give $\pi$ is $n - c$, the [Cayley distance](/cayley-distance/) to the identity, and the fewest adjacent transpositions is $\operatorname{inv}(\pi)$, by [sorting by adjacent swaps](/sorting-by-adjacent-swaps/). Both have the parity of $\pi$.
- **Inverse and conjugates.** $\operatorname{sgn}(\pi^{-1}) = \operatorname{sgn}(\pi)$ and $\operatorname{sgn}(\rho\pi\rho^{-1}) = \operatorname{sgn}(\pi)$.
- **The alternating group.** For $n \ge 2$, the even permutations form a subgroup $A_n$ of the [symmetric group](/symmetric-group/), the kernel of $\operatorname{sgn}$, with $n!/2$ elements. The map $\pi \mapsto \pi \cdot (1\ 2)$ is a bijection from the even permutations onto the odd ones.
- **Generating function.** Setting $z = -1$ in $\sum_{\pi} z^{\operatorname{inv}(\pi)} = \prod_{k=1}^{n}(1 + z + \cdots + z^{k-1})$ gives $\sum_\pi \operatorname{sgn}(\pi) = 0$ for $n \ge 2$, because the factor for $k = 2$ is $1 + z$. In terms of the [Mahonian numbers](/mahonian-numbers/), the permutations with an even and with an odd number of inversions are equally many.

**Computing the parity.** Counting the inversions takes $O(n \log n)$ time. The cycles give it in $O(n)$:

```pseudo
PARITY(π[1 .. n])                    ▷ returns 0 for even, 1 for odd
1  seen[1 .. n] ← false, c ← 0
2  for i ← 1 to n do
3      if not seen[i] then
4          c ← c + 1, j ← i
5          while not seen[j] do seen[j] ← true, j ← π[j]
6  return (n − c) mod 2
```

Each item is marked once, so the time is $\Theta(n)$, with $n$ extra bits. Another linear method sorts $\pi$ in place by swapping $\pi[i]$ into position $\pi[i]$ while it is not there, and counts the swaps: each swap puts one item in its place, it makes $n - c$ swaps in total, and it destroys the array.

## Examples

**Even.** $\pi = 3\,1\,4\,5\,2$ has 4 inversions and is the single 5-cycle $(1\ 3\ 4\ 5\ 2)$, with $n - c = 5 - 1 = 4$. Both give even. It is the product of the 4 transpositions $(1\ 2)(1\ 5)(1\ 4)(1\ 3)$, applied from the right.

**Even with two cycles.** $\sigma = 2\,4\,1\,3\,6\,5 = (1\ 2\ 4\ 3)(5\ 6)$ has 4 inversions, and $n - c = 6 - 2 = 4$. Its two cycles have even length, an even number of them.

**Odd.** The transposition $(1\ 4)$ in $S_4$ is $4\,2\,3\,1$, with the 5 inversions $(4,2), (4,3), (4,1), (2,1), (3,1)$, which is $2(4 - 1 - 1) + 1$. It has 3 cycles, $(1\ 4)(2)(3)$, and $4 - 3 = 1$ is odd.

**All of $S_3$.** The even permutations are $123, 231, 312$, the identity and the two 3-cycles, with 0, 2 and 2 inversions. The odd ones are $132, 213, 321$, the three transpositions, with 1, 1 and 3 inversions.

**Non-example.** The number of [descents](/descents/) does not give the parity: $1\,3\,2$ and $2\,3\,1$ both have one descent, but the first is odd and the second is even.

## Where it is used

- **[Determinants](/determinant/).** The Leibniz formula $\det A = \sum_{\pi \in S_n} \operatorname{sgn}(\pi) \prod_i a_{i, \pi(i)}$ weights each term by the sign. Exchanging two rows changes the sign of the determinant because it multiplies each $\pi$ by a transposition.
- **[Sliding puzzles](/sliding-puzzle-solvability/).** In the fifteen puzzle each move is a transposition of the blank with a tile, so the parity of the tile permutation together with the position of the blank decides whether a position is solvable. Half of all arrangements cannot be solved.
- **[Rubik's cube](/rubiks-cube-problem/).** A quarter turn permutes the corner pieces by a 4-cycle and the edge pieces by a 4-cycle, so the two permutations always have the same parity, and a cube with a single pair of edges exchanged cannot be solved.
- **Checking swap sequences.** Two arrangements of distinct items are related by an even number of swaps exactly when the permutation between them is even, which is a quick test in contest problems about reachability by swaps or by 3-cycles.
- **Group theory.** The sign is the only nontrivial homomorphism from $S_n$ to $\{\pm 1\}$, and $A_n$ is the basic example of a simple group for $n \ge 5$.

## References
