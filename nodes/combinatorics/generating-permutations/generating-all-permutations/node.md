---
tag: MZ3GWV
kind: problem
slug: generating-all-permutations
name: Generating all permutations
aliases:
- permutation enumeration
- listing permutations
area: combinatorics/generating-permutations
level: intro
summary: Output every permutation of n items exactly once, in some order.
model: word-ram
complexity:
  vars: {n: the number of items}
  time: {worst: Ω(n!)}
prereqs: [permutation, factorial]
see_also: [next-permutation, heaps-algorithm, steinhaus-johnson-trotter, minimal-change-permutation-order, multiset-permutations, permutation-unranking, combinatorial-generation, constant-amortized-time-generation]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.2.1.2, Generating all permutations (Algorithm L for lexicographic order, Algorithm P for plain changes, Heap's method and Ehrlich swaps)
  - paper: doi:10.1145/356689.356692
    title: Robert Sedgewick, Permutation generation methods, ACM Computing Surveys 9(2) (1977) 137-164
    locator: the whole survey (exchange methods, adjacent exchanges, lexicographic methods, and the comparison of running times)
  - book: isbn:9780849339882
    title: Donald L. Kreher and Douglas R. Stinson, Combinatorial Algorithms, Generation, Enumeration and Search, CRC Press, 1999
    locator: Chapter 2 (generating permutations in lexicographic and in Trotter-Johnson order, with successor, rank and unrank)
---

The problem of generating all permutations asks for a list of all $n!$ [permutations](/permutation/) of $n$ items, each exactly once. The list has [factorial](/factorial/) length, so every method takes $\Omega(n!)$ time, and the goal is to spend $O(1)$ time per permutation. The main solutions are [next permutation](/next-permutation/) for lexicographic order, [Heap's algorithm](/heaps-algorithm/) with one exchange per step, and the [Steinhaus-Johnson-Trotter algorithm](/steinhaus-johnson-trotter/) with one exchange of neighbors per step.

## In plain words

You have a few different things, for example the letters A, B and C. You want to write down every order in which they can stand in a row, and you want each order to appear once. For three letters there are six orders. For ten letters there are more than three million.

The number of orders grows very fast, so the list is only possible for small groups. A good method makes each new order from the last one with very little work, often with one swap of two things. It must also know when it has made every order, without keeping the whole list in memory.

## Definition

**Input.** An integer $n \ge 0$, or a list of $n$ distinct items $x_1, \ldots, x_n$.

**Output.** A sequence of $N = n!$ visits of an array $A[1 \ldots n]$, such that the arrays at the visits are the $n!$ permutations of the items, each exactly once.

Two output models are common. In the *visit in place* model, the algorithm changes one array and calls a visit procedure at each permutation; the visit may read the array but must not change it. In the *copy* model, the algorithm writes out each permutation in full, which costs $\Theta(n)$ per permutation. The cost of a method is measured by its total time, by its amortized time per permutation, and by its *delay*, the worst-case time between two consecutive visits. A method is [CAT](/constant-amortized-time-generation/) when the total time in the visit model is $O(N)$, and [loopless](/loopless-generation/) when the delay is $O(1)$ after an $O(n)$ start.

Lists of permutations of distinct items reduce to lists of permutations of $[n] = \{1, \ldots, n\}$: generate the permutations of the indices, and read the items through them.

## Variants

- **A fixed order.** The output must follow a given order, most often [lexicographic order](/lexicographic-order/). Then the list is unique.
- **Minimal change.** Consecutive permutations must differ by one transposition, or by one exchange of adjacent items. This is the [minimal-change order](/minimal-change-permutation-order/) problem.
- **Repeated items.** The items form a multiset, and each distinct arrangement must appear once. This is [multiset permutations](/multiset-permutations/).
- **Restricted permutations.** Only the permutations with a property are wanted, such as [derangements](/derangement/) or [involutions](/generating-involutions/). A [backtracking](/generic-backtracking-algorithm/) search that extends prefixes and prunes the bad ones is the usual method.
- **Successor, rank and unrank.** Instead of the whole list, return the next permutation of a given one ([lexicographic successor](/lexicographic-permutation-successor/)), the position of a permutation ([ranking](/permutation-ranking/)), or the permutation at a position ([unranking](/permutation-unranking/)).
- **Random order.** Output one permutation chosen uniformly at random. This is a [random permutation](/random-permutation/), not a list.

## Examples

The six permutations of $1\,2\,3$ in three common orders:

| step | lexicographic | Heap's algorithm | Steinhaus-Johnson-Trotter |
|---|---|---|---|
| 1 | 123 | 123 | 123 |
| 2 | 132 | 213 | 132 |
| 3 | 213 | 312 | 312 |
| 4 | 231 | 132 | 321 |
| 5 | 312 | 231 | 231 |
| 6 | 321 | 321 | 213 |

In lexicographic order, the step from 132 to 213 changes all three positions. In Heap's order, each step exchanges two positions, such as positions 1 and 3 from 213 to 312. In the Steinhaus-Johnson-Trotter order, each step exchanges two neighbors.

The size of the list limits the problem to small $n$. There are $10! = 3\,628\,800$ permutations of 10 items, $12! = 479\,001\,600$ of 12 items, and more than $6 \times 10^9$ of 13 items.

## Known algorithms

| algorithm | order | change per step | time |
|---|---|---|---|
| [next permutation](/next-permutation/) (Knuth's Algorithm L) | lexicographic | a swap and a suffix reversal | $\Theta(1)$ amortized, $\Theta(n)$ delay |
| [Heap's algorithm](/heaps-algorithm/) | Heap's order | one transposition | $\Theta(1)$ amortized |
| [Steinhaus-Johnson-Trotter](/steinhaus-johnson-trotter/) | plain changes | one adjacent transposition | $\Theta(1)$ amortized, loopless forms exist |
| Ehrlich swaps (Knuth's Algorithm E) | star transpositions | exchange of the first item with another | $\Theta(1)$ delay |
| unrank each rank $0, \ldots, n! - 1$ | any rankable order | the whole array | $O(n \log n)$ per permutation |

The first three are the standard choices. [Next permutation](/next-permutation/) also works for multisets and needs no extra memory. Heap's algorithm makes the fewest changes per step in practice. The Steinhaus-Johnson-Trotter algorithm is the one to use when only neighbors may be exchanged. Unranking with the [permutation rank and unrank algorithm](/permutation-rank-unrank/) is slower, but it lets each processor of a parallel computer start at its own rank.

## Bounds

- **Lower bound.** The output has $n!$ permutations, so each method takes $\Omega(n!)$ time in the visit model, and $\Omega(n \cdot n!)$ time in the copy model.
- **Upper bounds.** The three main algorithms run in $O(n!)$ total time in the visit model, so they are optimal. Loopless methods reach $O(1)$ worst-case delay.
- **Changes.** Two distinct permutations differ in at least two positions, so each step changes at least two positions. Heap's algorithm and the Steinhaus-Johnson-Trotter algorithm reach this bound at every step, with $n! - 1$ transpositions in total. Lexicographic order cannot: the step from $1\,n\,(n-1) \cdots 2$ to $2\,1\,3 \cdots n$ changes at least $n - 1$ positions, and for $n = 3$ the step from 132 to 213 changes all three.
- **Space.** $\Theta(n)$ words are enough for each of the main algorithms. Next permutation needs only $O(1)$ words beyond the array.

## Reductions

- **From successor.** Repeated calls of a successor function, from the first permutation until it reports the end, solve the problem. The cost is the sum of the successor costs.
- **From unranking.** Unranking each of $0, \ldots, n! - 1$ solves the problem in any order that has an unranking function.
- **To multiset permutations.** A list of distinct items is a multiset with all multiplicities 1, so each method for [multiset permutations](/multiset-permutations/) also solves this problem.
- **To Hamiltonian paths.** A minimal-change list is a [Hamiltonian path](/hamiltonian-path/) in the graph whose vertices are the permutations and whose edges join permutations that differ by one allowed exchange.

## Applications

- **Brute force over orders.** The exact solution of a small [traveling salesman problem](/traveling-salesman-problem/) or [assignment problem](/assignment-problem/) can try all orders. With a minimal-change order, the cost of the next order can be updated from the cost of the last one.
- **The Leibniz formula.** The [determinant](/determinant/) of an $n \times n$ matrix is the sum over all permutations $\sigma$ of $\operatorname{sgn}(\sigma) \prod_i a_{i \sigma(i)}$. With a transposition order the [sign](/permutation-sign/) alternates, so it needs no extra work. This is practical only for small $n$.
- **Testing.** A sort, or another program that takes a sequence, can be tested on all $n!$ input orders for small $n$.
- **Puzzles and search.** Many puzzles ask for an order with a property, such as the [n-queens problem](/n-queens-problem/), where the queens of the rows form a permutation of the columns.

## References
