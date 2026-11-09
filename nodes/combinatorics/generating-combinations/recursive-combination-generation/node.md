---
tag: PHDE76
kind: algorithm
slug: recursive-combination-generation
name: Recursive generation of combinations
aliases:
- backtracking combinations
- nested-loop combination enumeration
- choose or skip recursion
area: combinatorics/generating-combinations
level: intro
summary: Choose or skip each element recursively, emitting the set when k elements are chosen.
solves: [k-subset-enumeration]
model: word-ram
complexity:
  vars: {n: the size of the ground set, k: the size of each subset, N: the number of k-subsets}
  time: {worst: Θ(N*n/(n-k+1)), amortized: Θ(n/(n-k+1))}
  space: {extra: Θ(n)}
properties: {in_place: true, deterministic: true, comparison: false, recursive: true}
prereqs: [k-subset-enumeration, recursion]
see_also: [lexicographic-combinations, power-set-by-recursion, generic-backtracking-algorithm, search-tree-pruning, state-space-tree, pascal-triangle-dp, hockey-stick-identity, k-subset-enumeration]
sources:
  - book: isbn:9780849339882
    title: Donald L. Kreher and Douglas R. Stinson, Combinatorial Algorithms, Generation, Enumeration, and Search, CRC Press, 1999
    locator: Chapter 4, Backtracking algorithms (the general backtracking scheme and pruning)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.3, Generating all combinations (lexicographic order and the recursive structure of the list)
  - book: isbn:9783030542559
    title: Steven S. Skiena, The Algorithm Design Manual, third edition, Springer, 2020
    locator: Chapter 9, Combinatorial search (backtracking and the construction of all subsets), and Section 17.5, Generating subsets
---

This algorithm lists the $k$-subsets of $[n] = \{1, \ldots, n\}$ by a recursion over the elements. For each element $i$ in turn it first takes $i$ and lists the rest, then skips $i$ and lists the rest. A call stops when it has $k$ elements, and it also stops when too few elements are left to reach $k$. It visits the subsets in lexicographic order, the same order as the [lexicographic successor](/lexicographic-combinations/), and it makes exactly $2N - 1 + 2C(n, k-1)$ calls for $N = C(n, k)$ and $k \ge 1$.

## In plain words

You must pick $k$ people from a line of $n$. Walk along the line. At each person you ask one question: "do I take this one?" First you say yes, and you go on to pick the rest from the people after this one. When you come back, you say no, and you go on again.

When you have $k$ people, you write the team down and go back. When there are fewer people left in the line than you still need, you go back at once, because no team can come from this branch. This early stop is the reason the method is fast.

## The problem

Given $0 \le k \le n$, visit each $k$-subset of $[n]$ once. The current subset is a stack $a[1 \ldots m]$ of the chosen elements in increasing order. This is [k-subset enumeration](/k-subset-enumeration/).

## The algorithm

The call CHOOSE$(i)$ has chosen $a[1 \ldots m]$ from $\{1, \ldots, i-1\}$ and must choose $k - m$ more elements from $\{i, \ldots, n\}$, which has $n - i + 1$ elements.

```pseudo id=main
REC-COMBINATIONS(n, k)
L1  m ← 0, CHOOSE(1)

CHOOSE(i)                                  ▷ a[1 .. m] is chosen from {1, …, i − 1}
L2  if m = k then visit a[1 .. k], return
L3  if n − i + 1 < k − m then return       ▷ too few elements are left
L4  m ← m + 1, a[m] ← i                    ▷ take i
L5  CHOOSE(i + 1)
L6  m ← m − 1                              ▷ skip i
L7  CHOOSE(i + 1)
```

Line L3 is the pruning test. Without it, the recursion needs a stop at $i > n$ and visits many dead branches. Line L2 comes before line L3, so a call that has its $k$ elements visits them even when $i > n$.

## Example

Take $n = 5$ and $k = 3$. The tree below shows the calls by their chosen prefix. A call with prefix $12$ and $i = 3$ takes $3$ and visits $123$, then skips $3$, takes $4$ and visits $124$, then skips $4$, takes $5$ and visits $125$. Then it calls CHOOSE$(6)$ with $m = 2$, and line L3 stops this call, because $5 - 6 + 1 = 0 < 1$.

| prefix after L4 | subsets visited below it |
| --- | --- |
| $1$ | $123, 124, 125, 134, 135, 145$ |
| $2$ | $234, 235, 245$ |
| $3$ | $345$ |

The visits are $123, 124, 125, 134, 135, 145, 234, 235, 245, 345$, in lexicographic order. The prefix $4$ is never made: at $i = 4$ with $m = 0$, only $2$ elements are left, and line L3 stops.

The recursion makes $39$ calls. The formula gives $2 \cdot 10 - 1 + 2 \cdot C(5, 2) = 19 + 20 = 39$: the $10$ visits, $10$ calls stopped by line L3, and $19$ calls that branch.

## Correctness

By [induction](/induction/) on $n - i$: CHOOSE$(i)$ with prefix $a[1 \ldots m]$ visits each $k$-subset whose elements below $i$ are exactly $a[1 \ldots m]$, once each, in lexicographic order. Line L5 lists the subsets that contain $i$, line L7 the ones that do not. Each subset of the first group has $i$ as its next entry, the smallest value possible there, so it comes before each subset of the second group in lexicographic order. Line L3 returns only when no subset with this prefix exists. The full proof is in the proof file.

## Complexity

**The number of calls.** For $k \ge 1$ the recursion makes exactly
$$2N - 1 + 2\,C(n, k-1)$$
calls. Each call that reaches line L4 makes two calls, and each other call is a leaf. The leaves are the $N$ visits and the calls stopped by line L3. A call is stopped by line L3 only when it is the "skip" call of a parent that had exactly as many elements left as it needed. There are $C(n - k + m, m)$ such parents with $m$ chosen elements, and by the [hockey stick identity](/hockey-stick-identity/) their total is $C(n, k-1)$. A binary tree with $N + C(n, k-1)$ leaves has $2(N + C(n, k-1)) - 1$ nodes. For $k = 0$ there is one call.

**The total time.** Each call takes $O(1)$ time besides its calls, so the time is $\Theta(N + C(n, k-1)) = \Theta(N \cdot n/(n-k+1))$, the same as the [lexicographic successor](/lexicographic-combinations/). This is CAT for $k \le n/2$.

**Delay and space.** The recursion depth is at most $n + 1$, so the stack takes $\Theta(n)$ space. Between two visits the recursion can return and descend many levels, so the delay is $O(n)$ and not $O(1)$.

**The pruning matters.** For $n = 20$ and $k = 17$ there are $N = 1140$ subsets. With line L3 the recursion makes $11969$ calls. With only a stop at $i > n$ it makes $2096729$ calls, almost all of them in branches that cannot reach $17$ elements.

## Properties

- **Lexicographic order.** The list is the same as the list of the [lexicographic successor](/lexicographic-combinations/).
- **Prefix sharing.** All subsets with the same prefix are visited in one block. So work that depends only on the prefix, for example a partial sum, is done once for each prefix. This is the main reason to use the recursion.
- **In place.** The stack $a$ is the only data. The visit must copy it to keep it.
- **Not a Gray code.** Consecutive subsets can differ in all $k$ elements.

## Variants and improvements

- **Nested loops.** CHOOSE$(m, s)$ runs a loop over $v = s, \ldots, n - (k - m) + 1$, sets $a[m+1] \leftarrow v$, and calls CHOOSE$(m + 1, v + 1)$. The loop bound does the pruning. This form makes exactly $C(n + 1, k)$ calls, one for each prefix that can be completed. For $n = 5$ and $k = 3$ this is $20$ calls.
- **Skip first.** Make the call without $i$ before the call with $i$. Then the list is in reverse lexicographic order: $34, 24, 23, 14, 13, 12$ for $n = 4$ and $k = 2$. Other orders, such as [colexicographic order](/colexicographic-order/), come from a recursion on the largest element first.
- **The revolving door recursion.** Reverse the second half: list the $k$-subsets of $[n-1]$, then the $(k-1)$-subsets of $[n-1]$ in reverse order with $n$ added. This gives the [revolving door](/revolving-door-ordering/) Gray code.
- **Backtracking.** Add a test at each call that cuts branches with no valid completion, for example a partial sum that is already too large. This is the [generic backtracking algorithm](/generic-backtracking-algorithm/) on the [state space tree](/state-space-tree/) of subsets, with [search tree pruning](/search-tree-pruning/).
- **No size limit.** Drop the size test and visit at each leaf with $i > n$. This lists the whole power set, see [power set by recursion](/power-set-by-recursion/).

## When to use it

Use it when the work for each subset can be built along the prefix, or when branches can be cut early, as in subset sum or set cover with a size limit. Use it when a short, clear program matters more than a successor function. If you need to stop and restart from a given subset, a successor function such as the [lexicographic successor](/lexicographic-combinations/) is simpler.

## Pitfalls

- **No pruning.** Without line L3 the recursion explores all branches, up to about $2^{n+1}$ calls, even when $N$ is small.
- **The order of the tests.** Line L2 must come before line L3 and before any test of $i > n$. Otherwise the subsets that end at element $n$ are lost.
- **Copies at each call.** Passing a new list to each call, as in `choose(i + 1, a + [i])`, costs $\Theta(k)$ for each call. Use one shared stack and undo the change, as line L6 does.
- **Shared state.** The visit sees the shared stack. Copy it to store it.
- **Deep recursion.** The depth is up to $n + 1$. In languages with a small stack, use an explicit stack for large $n$.

## Implementations

## History

The recursion follows Pascal's rule $C(n, k) = C(n-1, k-1) + C(n-1, k)$: the subsets that contain an element and the subsets that do not. As a program it is a standard example of backtracking, and textbooks such as Kreher and Stinson and Skiena present it in that form. No single inventor is known.

## References
