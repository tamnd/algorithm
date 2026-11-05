---
tag: 8VRRS9
kind: problem
slug: max-sum-non-adjacent-subsequence
name: Maximum-weight subsequence with no two adjacent elements
aliases:
- house robber
- maximum weight independent set on a path
area: sequences/subsequence-problems
level: intro
summary: Choose a subsequence of weighted elements with no two consecutive picks, maximizing total weight, in linear time.
prereqs: [subsequence, optimal-substructure, tabulation]
see_also: [independent-set, independent-set-on-trees, weighted-interval-scheduling, kadane-algorithm, traceback, fibonacci-numbers]
sources:
  - book: isbn:9780999282946
    title: Tim Roughgarden, Algorithms Illuminated, Part 3, Greedy Algorithms and Dynamic Programming
    locator: Chapter 16, Introduction to dynamic programming (the weighted independent set problem in path graphs, the linear-time algorithm and the reconstruction)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 6.1, Weighted interval scheduling (the same two-way recurrence, of which this problem is a special case)
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Chapter 15, Problem 15-6, Planning a company party (the version on a tree)
---

This problem takes a sequence of weights $w_1, \ldots, w_n$ and asks for a [subsequence](/subsequence/) of maximum total weight that never takes two neighbouring positions. In graph terms, it is a maximum-weight [independent set](/independent-set/) of a path with $n$ vertices. The recurrence $W_i = \max(W_{i-1},\ W_{i-2} + w_i)$ solves it in $\Theta(n)$ time and $O(1)$ extra space. It is the first example of dynamic programming in several textbooks, because the obvious greedy rules fail on it, and because the number of feasible choices grows like the [Fibonacci numbers](/fibonacci-numbers/).

## In plain words

A row of houses holds some money each. You may take the money from any houses you like, but never from two houses next to each other. You want as much money as you can get.

Look at the last house. Either you skip it, and then the best you can do is the best for the other houses; or you take it, and then you must skip the house before it, so you add its money to the best for the houses before that one. Work from left to right and keep the best totals for the last two prefixes. Each step needs only these two numbers.

## Definition

**Input.** Real weights $w_1, \ldots, w_n$, with $n \ge 0$.

**Output.** A set $S \subseteq \{1, \ldots, n\}$ with no two consecutive indices ($i \in S \Rightarrow i + 1 \notin S$) that maximizes $w(S) = \sum_{i \in S} w_i$. The empty set is allowed, so the optimum is at least 0. The value-only version outputs $W_n = \max_S w(S)$.

**The recurrence.** Let $W_i$ be the optimum for the prefix $w_1, \ldots, w_i$. Then

$$W_0 = 0, \qquad W_1 = \max(0, w_1), \qquad W_i = \max(W_{i-1},\ W_{i-2} + w_i) \quad (i \ge 2).$$

*Proof.* $W_0 = 0$ because only the empty set is feasible, and $W_1 = \max(0, w_1)$ because the feasible sets are $\emptyset$ and $\{1\}$. Let $i \ge 2$ and let $S$ be an optimal set for the prefix of length $i$. If $i \notin S$, $S$ is feasible for the prefix of length $i - 1$, so $w(S) \le W_{i-1}$. If $i \in S$, then $i - 1 \notin S$, so $S \setminus \{i\}$ is feasible for the prefix of length $i - 2$, and $w(S) \le W_{i-2} + w_i$. So $W_i \le \max(W_{i-1}, W_{i-2} + w_i)$. Conversely, an optimal set for the prefix of length $i - 1$ is feasible for length $i$; and an optimal set $S'$ for length $i - 2$ uses no index above $i - 2$, so $S' \cup \{i\}$ is feasible for length $i$ with weight $W_{i-2} + w_i$. So $W_i \ge \max(W_{i-1}, W_{i-2} + w_i)$. $\square$

This is the [optimal substructure](/optimal-substructure/) of the problem: an optimal set is an optimal set of a shorter prefix, with or without the last item.

```pseudo id=path
MAX-NON-ADJACENT(w[1 .. n])
L1  a ← 0, b ← 0                 ▷ a = W[i − 2], b = W[i − 1]
L2  for i ← 1 to n do
L3      (a, b) ← (b, max(b, a + w[i]))
L4  return b
```

To output the set, keep all of $W_0, \ldots, W_n$ and walk back: at $i$, if $W_{i-1} \ge W_{i-2} + w_i$ (with $W_{-1} = 0$), skip $i$ and go to $i - 1$; else take $i$ and go to $i - 2$. This is the [traceback](/traceback/) of the table.

## Variants

- **Cycle (house robber II).** The positions are on a circle, so $1$ and $n$ are neighbours too. Solve the path $w_1, \ldots, w_{n-1}$ and the path $w_2, \ldots, w_n$, and take the larger answer: an optimal set misses position 1 or position $n$.
- **Tree.** Neighbours are the edges of a tree. Each vertex keeps two values, the best of its subtree with and without it. This is the company party problem of CLRS, and the [independent set on trees](/independent-set-on-trees/) page.
- **Gap at least $k$.** Picked indices must differ by more than $k$. Then $W_i = \max(W_{i-1}, W_{i-k-1} + w_i)$.
- **Exactly or at most $k$ picks.** Add the number of picks to the state: $O(nk)$ time.
- **General graphs.** For an arbitrary graph, maximum-weight independent set is NP-hard. The path and the tree are special cases with a linear-time DP.
- **Intervals.** A pick that blocks a window of neighbours of any length is [weighted interval scheduling](/weighted-interval-scheduling/), with the recurrence $W_j = \max(W_{j-1}, W_{p(j)} + w_j)$.

## Examples

For each input, the row $W_0, W_1, \ldots, W_n$ and the optimum:

| weights | $W_0, \ldots, W_n$ | optimum | a best set (1-based) |
| --- | --- | --- | --- |
| 5, 1, 1, 5 | 0, 5, 5, 6, 10 | 10 | {1, 4} |
| 2, 7, 9, 3, 1 | 0, 2, 7, 11, 11, 12 | 12 | {1, 3, 5} |
| 1, 4, 5, 4 | 0, 1, 4, 6, 8 | 8 | {2, 4} |
| 3, 4, 3 | 0, 3, 4, 6 | 6 | {1, 3} |
| 3, −2, 5, −1, 4, 2, −7, 6 | 0, 3, 3, 8, 8, 12, 12, 12, 18 | 18 | {1, 3, 5, 8} |

**Greedy rules that fail.**

- *Heaviest first.* On 3, 4, 3, take 4, which blocks both neighbours: total 4, but the optimum is 6.
- *Odd or even positions.* On 5, 1, 1, 5, the odd positions give 6 and the even positions give 6, but the optimum $\{1, 4\}$ gives 10.

**Brute force is exponential.** The number of feasible sets on a path of $n$ vertices, the empty set included, is $F_{n+2}$, a [Fibonacci number](/fibonacci-numbers/): 2, 3, 5, 8, 13, 21, 34, 55, 89, 144 for $n = 1$ to 10. The reason is the same split: a feasible set either avoids $n$ (a set for $n - 1$) or contains $n$ (a set for $n - 2$, plus $n$). So the search of all sets takes time about $1.618^n$.

## Known algorithms

- **Linear DP.** MAX-NON-ADJACENT does $n$ steps with one addition and one comparison each: $\Theta(n)$ time and $O(1)$ extra space for the value. With the traceback, $\Theta(n)$ space.
- **Memoized recursion.** The recurrence with [memoization](/memoization/) also takes $\Theta(n)$ time, with recursion depth $n$.
- **Plain recursion.** Without a table, the recursion $W(i) = \max(W(i-1), W(i-2) + w_i)$ makes a number of calls that grows like the Fibonacci numbers, so it is exponential.

## Bounds

- **Upper bound.** $\Theta(n)$ time by the DP.
- **Lower bound.** Each algorithm must read each weight, so $\Omega(n)$. If a positive weight $w_i$ is never read, raising it a lot changes the optimum, and the algorithm cannot notice.
- **Space.** $O(1)$ words for the value, because each step reads only the last two values.

## Reductions

- **To weighted interval scheduling.** Give position $i$ the closed interval $[i, i+1]$ with weight $w_i$. Two intervals overlap exactly when their positions are neighbours, so a feasible set of intervals is a non-adjacent set of positions.
- **To DAG longest path.** Vertices $0, \ldots, n$, an edge $i - 1 \to i$ of weight 0 (skip) and an edge $i - 2 \to i$ of weight $w_i$ (take) give a [longest path](/dag-longest-path/) problem whose optimum is $W_n$.
- **Relation to the maximum subarray.** The [maximum subarray problem](/maximum-subarray-problem/) asks for a contiguous block, this problem for a set with gaps; both have a one-pass DP with $O(1)$ state, like [Kadane's algorithm](/kadane-algorithm/).

## Applications

- **Scheduling with rest periods.** Pick jobs, shifts or ads on a timeline where two neighbouring slots cannot both be used.
- **Teaching.** It is the standard first example of how a recurrence, a table and a traceback replace a search of exponentially many sets.

## References
