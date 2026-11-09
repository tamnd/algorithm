---
tag: SQBTS9
kind: concept
slug: minimal-change-permutation-order
name: Minimum change order for permutations
aliases:
- Minimum change order
- minimal-change order of permutations
- Gray code for permutations
area: combinatorics/generating-permutations
level: core
summary: An ordering of all permutations in which consecutive permutations differ by a single adjacent swap, as in the Steinhaus-Johnson-Trotter algorithm.
prereqs: [permutation, generating-all-permutations, gray-code]
see_also: [steinhaus-johnson-trotter, heaps-algorithm, gray-code, permutation-sign, hamiltonian-cycle, sorting-by-adjacent-swaps, binary-reflected-gray-code, combinatorial-generation]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.2.1.2 (plain changes, Algorithm P; Heap's method; Ehrlich swaps, Algorithm E)
  - paper: doi:10.1145/356689.356692
    title: Robert Sedgewick, Permutation generation methods, ACM Computing Surveys 9(2) (1977) 137-164
    locator: the sections on methods based on exchanges and on adjacent exchanges
  - paper: doi:10.1137/S0036144595295272
    title: Carla Savage, A survey of combinatorial Gray codes, SIAM Review 39(4) (1997) 605-629
    locator: the section on permutations (transposition Gray codes and the Cayley graph view)
---

A minimal-change order for [permutations](/permutation/) lists all $n!$ permutations of $n$ items so that each one differs from the one before it as little as possible: by the exchange of two items. In the strongest common form, the two items must be neighbors, and the [Steinhaus-Johnson-Trotter algorithm](/steinhaus-johnson-trotter/) gives such an order for every $n$. Such an order is a [Gray code](/gray-code/) for permutations, and in graph terms it is a [Hamiltonian path](/hamiltonian-path/) through all permutations.

## In plain words

You want to visit every order of a few things, one order at a time. Between two visits you want to do as little as possible. Two different orders always differ in at least two places, so the best you can hope for is to swap two things at each step.

Such lists exist. You can even ask that the two things you swap stand next to each other. Bell ringers found such lists centuries ago: at each change, two bells that ring one after the other trade places. Lists like this help when each step costs effort, or when a value can be updated from the last order instead of being computed again.

## The idea

**The best possible change.** Two distinct permutations of the same items differ in at least two positions. A transposition, the exchange of two positions, changes exactly two. So an order of all permutations in which each step is one transposition makes the least possible change at each step. Lexicographic order does not: the step from $1\,3\,2$ to $2\,1\,3$ changes all three positions.

**Kinds of transpositions.** Three sets of allowed exchanges are common:

| allowed exchange | example method | steps needed between two permutations |
|---|---|---|
| any two positions | [Heap's algorithm](/heaps-algorithm/) | $n$ minus the number of cycles |
| adjacent positions $i, i+1$ | [Steinhaus-Johnson-Trotter](/steinhaus-johnson-trotter/) | the number of inversions |
| position 1 with any other (star) | Ehrlich swaps (Knuth's Algorithm E) | depends on the cycles and on position 1 |

The last column is the distance between two permutations when only these exchanges are allowed: for any transpositions it is the [Cayley distance](/cayley-distance/), and for adjacent ones it is the [Kendall tau distance](/kendall-tau-distance/), the number of [inversions](/inversion/) that separate them.

**The graph view.** Make a graph whose vertices are the $n!$ permutations, with an edge between two permutations when an allowed exchange turns one into the other. This is a Cayley graph of the [symmetric group](/symmetric-group/). A minimal-change order is a Hamiltonian path in this graph, and a cyclic order, in which the last permutation also differs from the first by one allowed exchange, is a [Hamiltonian cycle](/hamiltonian-cycle/). For all three sets of exchanges, Hamiltonian paths exist for every $n$, and Hamiltonian cycles for every $n \ge 3$.

**Signs alternate.** Each transposition changes the [sign](/permutation-sign/) of a permutation. So in a minimal-change order the signs alternate $+, -, +, -, \ldots$, and the graph is bipartite, with the $n!/2$ even permutations on one side and the $n!/2$ odd ones on the other. A Hamiltonian cycle in a bipartite graph needs two sides of equal size, and here they are equal. The alternation is also a useful check on any claimed minimal-change order.

**The recursive idea.** Most constructions extend an order for $n - 1$ items. The Steinhaus-Johnson-Trotter order takes each permutation of $[n-1]$ in turn and moves $n$ across it, right to left, then left to right, in a zigzag. This is the same reflection idea as in the [binary reflected Gray code](/binary-reflected-gray-code/). Heap's algorithm instead holds one item at the end while it permutes the others, and then exchanges that item with another.

**Cyclic or not.** The Steinhaus-Johnson-Trotter order is cyclic for all $n \ge 2$: it ends with $2\,1\,3 \cdots n$, one adjacent exchange from the start. The order of Heap's algorithm is cyclic for odd $n$ and for $n = 2$, but for $n = 4$ it ends with $2\,3\,4\,1$, which differs from $1\,2\,3\,4$ in all four positions.

**Cost.** Because only two positions change, a program can keep a value that depends on the permutation and update it in $O(1)$ time per step, if the value changes in a simple way under an exchange. Good algorithms for minimal-change orders also find the next exchange in $O(1)$ amortized time, and loopless ones in $O(1)$ worst-case time.

## Examples

The six permutations of $1\,2\,3$ in two minimal-change orders. The column "exchange" gives the two positions that change on the step to the next row.

| Steinhaus-Johnson-Trotter | exchange | Heap's algorithm | exchange | sign |
|---|---|---|---|---|
| 123 | 2, 3 | 123 | 1, 2 | + |
| 132 | 1, 2 | 213 | 1, 3 | − |
| 312 | 2, 3 | 312 | 1, 2 | + |
| 321 | 1, 2 | 132 | 1, 3 | − |
| 231 | 2, 3 | 231 | 1, 2 | + |
| 213 | 1, 2 | 321 | 1, 3 | − |

The last row returns to the first with the exchange shown, so both orders are cyclic for $n = 3$. Every exchange in the Steinhaus-Johnson-Trotter order is of neighbors. For $n = 3$, Heap's order also involves position 1 in every exchange, so it is a star transposition order as well. The signs alternate in both lists, at the same rows, as they must.

For $n = 4$, the Steinhaus-Johnson-Trotter order begins 1234, 1243, 1423, 4123, 4132, 1432, 1342, 1324, 3124, and the item 4 moves at three of every four steps.

## Where it is used

- **Change ringing.** English bell ringers ring the bells of a tower in all orders, and a bell can only move one place in the order from one change to the next. Plain changes, the Steinhaus-Johnson-Trotter order, is the oldest such method.
- **Sums over all permutations.** The [determinant](/determinant/) by the Leibniz formula, or the length of every tour in a small [traveling salesman problem](/traveling-salesman-problem/), can be updated in $O(1)$ or $O(n)$ time per permutation instead of recomputed in $\Theta(n)$ time.
- **Testing and hardware.** When each change of a physical setup costs effort, as in the order of plugs or of parts, a minimal-change order keeps the total effort small.
- **Search over orders.** Local moves in search heuristics for orders, such as the exchange of neighbors, are the edges of the same graphs. A minimal-change order visits all permutations by local moves only.

## References
