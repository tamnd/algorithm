---
tag: A0Q681
kind: concept
slug: permutation-sign
name: Sign of a permutation
aliases:
- parity of a permutation
- signature of a permutation
area: combinatorics/generating-permutations
level: core
summary: +1 for even and -1 for odd permutations, determined by the number of transpositions.
prereqs: [permutation, inversion, permutation-cycle-decomposition]
see_also: [permutation-parity, symmetric-group, determinant, minimal-change-permutation-order, sliding-puzzle-solvability, lehmer-code, cayley-distance, heaps-algorithm]
sources:
  - book: isbn:9780471433347
    title: David S. Dummit and Richard M. Foote, Abstract Algebra, third edition, Wiley, 2004
    locator: Section 3.5, Transpositions and the alternating group (the sign homomorphism and its definition by a product over pairs)
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Section 1.3 (cycles and inversions of permutations)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, Sorting and Searching, second edition
    locator: Section 5.1.1, Inversions (inversion tables, and the change in the number of inversions when adjacent items are exchanged)
---

The sign of a [permutation](/permutation/) $\pi$ is $\operatorname{sgn}(\pi) = +1$ if $\pi$ is a product of an even number of transpositions and $-1$ if it is a product of an odd number. Every way to write $\pi$ as such a product has the same parity, so the sign is well defined, and it equals $(-1)^{\operatorname{inv}(\pi)}$, where $\operatorname{inv}(\pi)$ counts [inversions](/inversion/), and $(-1)^{n - c}$, where $c$ is the number of cycles. The sign is multiplicative, $\operatorname{sgn}(\sigma\tau) = \operatorname{sgn}(\sigma)\operatorname{sgn}(\tau)$. In lists of permutations it behaves in a simple way: it alternates in every [minimal-change order](/minimal-change-permutation-order/), and it can be kept up to date in $O(1)$ time per step in lexicographic order.

## In plain words

Put some cards in a row in a new order. You can get back to the start by swapping two cards at a time. Many different sequences of swaps work, and they can have different lengths. But either all of them use an even number of swaps, or all of them use an odd number. Orders of the first kind are even, and orders of the second kind are odd.

The sign is a plus for even orders and a minus for odd ones. It is a small fact with large effects: some puzzles can never be solved because one swap would change the sign, and the formula for the area or volume spanned by vectors adds and subtracts terms by this sign.

## The idea

**Why the parity is fixed.** Let $\operatorname{inv}(\pi)$ be the number of pairs of positions $i < j$ with $\pi_i > \pi_j$. An exchange of two adjacent entries changes $\operatorname{inv}$ by exactly 1, because only the order of that one pair changes. An exchange of the entries at positions $i < j$ is the same as $2(j - i) - 1$ adjacent exchanges: move the entry at $j$ left to position $i$ in $j - i$ steps, then the entry now at $i + 1$ right to position $j$ in $j - i - 1$ steps. So any transposition changes the parity of $\operatorname{inv}$. If $\pi$ is a product of $k$ transpositions, building $\pi$ from the identity, which has no inversions, changes the parity $k$ times, so $k \equiv \operatorname{inv}(\pi) \pmod 2$ for every such product.

**Equivalent formulas.** For a permutation $\pi$ of $[n]$:

$$\operatorname{sgn}(\pi) = (-1)^{\operatorname{inv}(\pi)} = (-1)^{n - c(\pi)} = \prod_{1 \le i < j \le n} \frac{\pi(j) - \pi(i)}{j - i} = \det P_\pi,$$

where $c(\pi)$ is the number of cycles, fixed points included, and $P_\pi$ is the permutation matrix. The cycle formula holds because a $k$-cycle is a product of $k - 1$ transpositions, $(a_1\ a_2\ \cdots\ a_k) = (a_1\ a_k) \cdots (a_1\ a_3)(a_1\ a_2)$ with the right factor first. So a permutation is even exactly when it has an even number of cycles of even length.

**A group homomorphism.** If $\sigma$ is a product of $k$ transpositions and $\tau$ of $l$, then $\sigma\tau$ is a product of $k + l$. So $\operatorname{sgn} : S_n \to \{+1, -1\}$ is a homomorphism of groups. For $n \ge 2$ it takes both values, so its kernel, the *alternating group* $A_n$ of even permutations, has $n!/2$ elements. Also $\operatorname{sgn}(\pi^{-1}) = \operatorname{sgn}(\pi)$, and conjugate permutations have the same sign.

**Computing the sign.** The cycle formula gives the sign in $\Theta(n)$ time with $n$ mark bits: count the cycles by one pass over the [cycle decomposition](/permutation-cycle-decomposition/). Counting inversions takes $O(n \log n)$ time, so for the sign alone the cycle method is faster. Another linear method sorts $\pi$ by exchanges, putting each value into its place with one exchange per step, and counts the exchanges.

**The sign along a list of permutations.**

- *Minimal-change orders.* In [Heap's algorithm](/heaps-algorithm/), the [Steinhaus-Johnson-Trotter algorithm](/steinhaus-johnson-trotter/) and every other order in which each step is one transposition, the signs alternate $+, -, +, \ldots$, starting with $+$ at the identity.
- *Lexicographic order.* The sign is $(-1)^{c_1 + \cdots + c_n}$, where $(c_1, \ldots, c_n)$ is the [Lehmer code](/lehmer-code/), because the code digits add up to $\operatorname{inv}(\pi)$. The step of [next permutation](/next-permutation/) is one exchange followed by the reversal of a suffix of length $L$, and a reversal of $L$ entries is $\lfloor L/2 \rfloor$ exchanges. So the step multiplies the sign by $(-1)^{1 + \lfloor L/2 \rfloor}$, and a program can track the sign at no extra cost.

## Examples

| $\pi$ | cycles | $c$ | inversions | sign |
|---|---|---|---|---|
| 1 2 3 4 | identity | 4 | 0 | + |
| 2 1 3 4 | (1 2) | 3 | 1 | − |
| 2 3 1 4 | (1 2 3) | 2 | 2 | + |
| 2 3 4 1 | (1 2 3 4) | 1 | 3 | − |
| 2 1 4 3 | (1 2)(3 4) | 2 | 2 | + |
| 2 4 1 3 6 5 | (1 2 4 3)(5 6) | 2 | 4 | + |
| 3 1 4 5 2 | (1 3 4 5 2) | 1 | 4 | + |

Each row agrees with $(-1)^{\operatorname{inv}} = (-1)^{n - c}$. A cycle of odd length is even, and a cycle of even length is odd.

**Signs in lexicographic order.** For $n = 3$ the signs of 123, 132, 213, 231, 312, 321 are $+, -, -, +, +, -$. For $n = 4$, the 24 signs in lexicographic order are the pattern $+, -, -, +$ six times. So lexicographic order is not a minimal-change order: from 132 to 213 the sign does not change.

**Signs in plain changes.** The Steinhaus-Johnson-Trotter order for $n = 3$ is 123, 132, 312, 321, 231, 213, with signs $+, -, +, -, +, -$.

## Where it is used

- **Determinants.** The Leibniz formula $\det A = \sum_{\pi \in S_n} \operatorname{sgn}(\pi) \prod_i a_{i\,\pi(i)}$ defines the [determinant](/determinant/). It also explains why a matrix with two equal rows has determinant 0.
- **Puzzle solvability.** Each move of the [15-puzzle](/sliding-puzzle-solvability/) changes the sign of the arrangement and the color of the square of the blank together. So half of the arrangements cannot be reached, and a test in $O(n)$ time tells which half. A quarter turn of the [Rubik's cube](/rubiks-cube-problem/) changes the signs of the corner and of the edge permutations together, which rules out a single swap of two corners.
- **Exterior algebra and physics.** The Levi-Civita symbol $\varepsilon_{i_1 \ldots i_n}$ is the sign of $i_1 \cdots i_n$ when it is a permutation and 0 otherwise. It appears in cross products, volumes and the antisymmetry of fermion states.
- **Group theory.** The alternating group $A_n$, the kernel of the sign, is a central example of a simple group for $n \ge 5$.
- **Checks in generation.** In a claimed transposition order, the signs must alternate. This is a quick test of a generator.

## References
