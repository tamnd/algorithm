---
tag: ZGQC1D
kind: problem
slug: generating-involutions
name: Generating involutions
aliases:
- self-inverse permutations
- listing involutions
area: combinatorics/generating-permutations
level: advanced
summary: Generate all permutations that are their own inverse, i.e. with cycles of length at most two.
model: word-ram
complexity:
  vars: {n: the number of items, N: the number of involutions of n items}
  time: {worst: Θ(N)}
prereqs: [permutation, permutation-cycle-decomposition, generic-backtracking-algorithm]
see_also: [generating-all-permutations, permutation-cycle-decomposition, permutation-inverse, standard-young-tableaux, exponential-generating-functions, perfect-matching, derangement, constant-amortized-time-generation]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, Sorting and Searching, second edition
    locator: Section 5.1.4, Tableaux and involutions (the numbers t_n of involutions, their recurrence, sum formula and asymptotic value, and the correspondence with tableaux)
  - book: isbn:9780521898065
    title: Philippe Flajolet and Robert Sedgewick, Analytic Combinatorics, Cambridge University Press, 2009
    locator: Chapter II, Labelled structures and exponential generating functions (permutations with restricted cycle lengths, the EGF exp(z + z^2/2) of involutions)
---

An involution is a [permutation](/permutation/) $\pi$ with $\pi(\pi(i)) = i$ for all $i$, so it is its own [inverse](/permutation-inverse/). In its [cycle decomposition](/permutation-cycle-decomposition/), every cycle has length 1 or 2: each item is fixed or exchanged with one partner. The problem is to list all involutions of $[n]$, each once. There are $t_n$ of them, with $t_n = t_{n-1} + (n - 1)\, t_{n-2}$, and a backtracking search lists them in lexicographic order in constant amortized time each.

## In plain words

Some people stand in a room. Each person either stays alone or holds hands with exactly one other person. A pairing plan says who holds hands with whom. You want to list every possible plan once.

Take the person with the smallest number who has no role yet. This person can stay alone, or hold hands with one of the other free people. Try each choice in turn, and for each choice fill in the rest of the plan the same way. Every plan comes out once. In number form, a plan is an order of the numbers in which swapping each pair back gives the start order.

## Definition

**Input.** An integer $n \ge 0$.

**Output.** A sequence of visits of an array $\pi[1 \ldots n]$, such that the arrays at the visits are the involutions of $[n] = \{1, \ldots, n\}$ in one-line form, each exactly once.

An involution with $k$ two-cycles is a matching of $2k$ items into pairs, with the other $n - 2k$ items fixed. So the count is

$$t_n = \sum_{k=0}^{\lfloor n/2 \rfloor} \frac{n!}{(n - 2k)!\, 2^k\, k!}.$$

The term for $k$ chooses the $2k$ paired items in $\binom{n}{2k}$ ways and pairs them in $(2k)!/(2^k k!) = (2k-1)(2k-3) \cdots 1$ ways. The count also satisfies $t_0 = t_1 = 1$ and $t_n = t_{n-1} + (n-1)\, t_{n-2}$ for $n \ge 2$: the item $n$ is fixed, which leaves an involution of $[n-1]$, or it is paired with one of the other $n - 1$ items, which leaves an involution of the remaining $n - 2$. The [exponential generating function](/exponential-generating-functions/) is

$$\sum_{n \ge 0} t_n \frac{x^n}{n!} = e^{x + x^2/2},$$

because an involution is a set of cycles of length 1 and 2, with EGFs $x$ and $x^2/2$. The asymptotic value is

$$t_n \sim \frac{1}{\sqrt 2}\, n^{n/2} e^{-n/2 + \sqrt{n} - 1/4}.$$

The ratio of $t_n$ to this value is $1.083$ for $n = 10$, $1.039$ for $n = 50$ and $1.028$ for $n = 100$, so it tends to 1 slowly. In particular $t_n$ is much smaller than $n!$: it is close to $\sqrt{n!}$, up to a factor $e^{O(\sqrt{n})}$.

## Variants

- **Fixed-point-free involutions.** No item is fixed, so $n$ is even and the involution is a [perfect matching](/perfect-matching/) of $[n]$. There are $(n-1)(n-3) \cdots 1$ of them. The same search without the "stay alone" choice lists them.
- **A fixed number of two-cycles.** List the involutions with exactly $k$ pairs.
- **Minimal change.** Consecutive involutions should differ by a small change, such as one pair made or broken.
- **Ranking and unranking.** The recurrence gives rank and unrank functions in the same way as for [combinatorial ranking and unranking](/combinatorial-ranking-and-unranking/) in general.
- **Counting only.** Compute $t_n$ exactly, as a [big integer](/big-integer/), or modulo a number. The recurrence takes $O(n)$ arithmetic operations.

## Examples

The values of $t_n$ for $n = 0, 1, \ldots, 12$ are 1, 1, 2, 4, 10, 26, 76, 232, 764, 2620, 9496, 35696, 140152, and $t_{20} = 23\,758\,664\,096$.

The 10 involutions of $[4]$ in lexicographic order, in one-line form and in cycle form, with fixed points left out:

| one-line | cycles |
|---|---|
| 1234 | identity |
| 1243 | (3 4) |
| 1324 | (2 3) |
| 1432 | (2 4) |
| 2134 | (1 2) |
| 2143 | (1 2)(3 4) |
| 3214 | (1 3) |
| 3412 | (1 3)(2 4) |
| 4231 | (1 4) |
| 4321 | (1 4)(2 3) |

There is 1 with no pair, 6 with one pair and 3 with two pairs, which matches the sum formula: $1 + 6 + 3 = 10$.

## Known algorithms

**Backtracking on the smallest free item.** Keep the free items in a doubly linked list. At each node of the search, take the smallest free item $i$. First set $\pi_i = i$, remove $i$, and recurse. Then for each other free item $j$ in increasing order, set $\pi_i = j$ and $\pi_j = i$, remove both, and recurse. Restore the list on return. When no item is free, visit $\pi$.

- *Correctness.* Every involution arises from exactly one path: at each node, the choice is fixed by $\pi_i$. Each leaf is an involution, because every item is fixed or paired.
- *Order.* Two involutions that split at the node for $i$ agree on all positions before $i$, which are already set, and differ at position $i$, where the smaller choice gives the smaller value. So the visits are in lexicographic order, as the table above shows.
- *Cost.* A node with $m \ge 2$ free items has $m \ge 2$ children, and a node with 1 free item has one child, which is a leaf. So the number of nodes with two or more children is less than the number of leaves, and the number of nodes with one child is at most the number of leaves. The tree has fewer than $3 t_n$ nodes. With the linked list, the work at a node is $O(1)$ per child, so the total time is $O(t_n)$. The search is [CAT](/constant-amortized-time-generation/). For $n = 12$ it has $315\,516$ nodes for $140\,152$ involutions, about $2.25$ per involution.
- *Delay.* After the last leaf of a subtree, the search can return through $\Theta(n)$ levels, so the worst-case delay is $\Theta(n)$.

**Generation from smaller lists.** The recurrence also gives a list: the involutions of $[n-1]$ with $n$ fixed, then for each $j < n$ the involutions of $[n] \setminus \{j, n\}$ with $j$ and $n$ paired. This needs the lists of smaller sizes, or a recursion with the same tree as above.

**Filtering all permutations.** Test each of the $n!$ permutations. This is correct but takes $\Theta(n!)$ time, much more than $t_n$.

## Bounds

- **Lower bound.** $\Omega(t_n)$ time in the visit model, since there are $t_n$ outputs, and $\Omega(n\, t_n)$ in the copy model.
- **Upper bound.** $O(t_n)$ total time by the backtracking search, so it is optimal in total time.
- **Changes.** Two distinct involutions differ in at least two positions. Making or breaking one pair changes exactly two positions.

## Reductions

- **To standard Young tableaux.** The Robinson-Schensted correspondence maps a permutation to a pair $(P, Q)$ of [standard Young tableaux](/standard-young-tableaux/) of the same shape, and $\pi$ is an involution exactly when $P = Q$. So $t_n$ is the number of standard Young tableaux with $n$ cells, and a list of involutions gives a list of tableaux.
- **From perfect matchings.** An involution is a choice of a set $S$ of $2k$ items and a perfect matching of $S$. So a generator for subsets and one for [perfect matchings](/perfect-matching/) combine into a generator for involutions.
- **From backtracking.** The search above is an instance of the [generic backtracking algorithm](/generic-backtracking-algorithm/) with a [state-space tree](/state-space-tree/) in which every branch leads to a solution.

## Applications

- **Symmetric structures.** An involution is the same as a symmetric 0-1 matrix with one 1 in each row and column, or a graph in which each vertex has degree at most 1 (a matching), with loops for fixed points.
- **Tableaux.** Through the Robinson-Schensted correspondence, a list of involutions gives all standard Young tableaux with $n$ cells, and the [hook length formula](/hook-length-formula/) summed over shapes gives $t_n$.
- **Symmetries of a design.** In problems where a solution must be its own mirror image under a swap of labels, the swaps to test are involutions.

## References
