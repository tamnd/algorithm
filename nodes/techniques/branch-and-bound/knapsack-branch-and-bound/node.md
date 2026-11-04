---
tag: 0VCNY1
kind: algorithm
slug: knapsack-branch-and-bound
name: Knapsack branch and bound
aliases:
- Horowitz-Sahni knapsack algorithm
- 0-1 knapsack branch and bound
area: techniques/branch-and-bound
level: core
summary: Branch and bound for 0-1 knapsack using the fractional-greedy relaxation as the upper bound.
solves: [knapsack-problem]
model: word-ram
complexity:
  vars: {n: the number of items}
  time: {worst: O(n 2^n), best: O(n^2)}
  space: {extra: O(n^2)}
properties: {deterministic: true, recursive: false}
prereqs: [knapsack-problem, fractional-knapsack, depth-first-branch-and-bound]
see_also: [greedy-fractional-knapsack, knapsack-dynamic-programming, bounding-function, incumbent-solution, best-first-branch-and-bound, dominance-pruning, lp-relaxation]
sources:
  - paper: doi:10.1145/321812.321823
    title: Ellis Horowitz and Sartaj Sahni, Computing partitions with applications to the knapsack problem, Journal of the ACM 21(2), 1974
    locator: pp. 277 to 292
  - paper: doi:10.1287/mnsc.13.9.723
    title: Peter J. Kolesar, A branch and bound algorithm for the knapsack problem, Management Science 13(9), 1967
    locator: pp. 723 to 735
  - book: isbn:9780471924203
    title: Silvano Martello and Paolo Toth, Knapsack Problems, Algorithms and Computer Implementations
    locator: Chapter 2, 0-1 knapsack problem (upper bounds and branch-and-bound algorithms)
  - book: isbn:9780929306414
    title: Ellis Horowitz, Sartaj Sahni and Sanguthevar Rajasekaran, Computer Algorithms, second edition
    locator: Chapter 8, Branch-and-Bound (0/1 knapsack problem)
  - paper: doi:10.1287/opre.28.6.1402
    title: Vasek Chvatal, Hard knapsack problems, Operations Research 28(6), 1980
    locator: pp. 1402 to 1411
---

Knapsack branch and bound solves the 0-1 [knapsack problem](/knapsack-problem/) by a depth-first search over the decisions "take item $k$" and "leave item $k$", with the items sorted by value per unit weight. At each node it computes the optimum of the [fractional knapsack](/fractional-knapsack/) relaxation of what is left, which is an upper bound on every completion, and it drops the node when this bound is not above the best packing found so far. This is the scheme of the Horowitz-Sahni algorithm, and the base of most exact knapsack codes. It is exponential in the worst case, but on many instances it looks at only a small part of the $2^n$ subsets.

## In plain words

You must fill a bag with a weight limit, and each item has a value and a weight. Sort the items so that the items with the most value for each unit of weight come first. Then decide the items one at a time: take it, or leave it. Try "take" first.

Every partly filled bag is already a real answer, so you keep the best bag seen so far. At each step you also compute a quick limit: fill the rest of the bag with the best items, and cut the last item into a piece if it does not fit whole. No real answer below this step can beat this limit. If the limit is not above your best bag, you stop on this branch and go back.

## The problem

Given values $v_1, \ldots, v_n \ge 0$, weights $w_1, \ldots, w_n \ge 0$ and a capacity $W \ge 0$, all integers, find $X \subseteq \{1, \ldots, n\}$ with $\sum_{i \in X} w_i \le W$ that maximizes $\sum_{i \in X} v_i$. The problem is [NP-hard](/np-hard/), and it has a pseudo-polynomial [dynamic program](/knapsack-dynamic-programming/) in $O(n W)$ time.

## The algorithm

Sort the items so that $v_1 / w_1 \ge v_2 / w_2 \ge \cdots \ge v_n / w_n$, with items of weight 0 first. A node is a tuple $(k, c_w, c_v, X)$: items $1, \ldots, k$ are decided, $X$ is the set taken, $c_w$ its weight and $c_v$ its value. The bound $U(k, c_w, c_v)$ is $c_v$ plus the optimum of the fractional knapsack on items $k + 1, \ldots, n$ with capacity $W - c_w$: add the items $k + 1, k + 2, \ldots$ in order while they fit, then add the fraction $r / w_j$ of the first item $j$ that does not fit, where $r$ is the room left. Since all values are integers, the code rounds $U$ down.

```pseudo id=main
KNAPSACK-BB(v, w, W)                        ▷ items sorted by v_i / w_i, largest first
L1  z ← 0; best ← ∅                          ▷ the empty set is feasible
L2  S ← a stack that holds (0, 0, 0, ∅)
L3  while S is not empty do
L4      (k, c_w, c_v, X) ← POP(S)
L5      if c_v > z then z ← c_v; best ← X    ▷ every node is a feasible packing
L6      if k = n or U(k, c_w, c_v) ≤ z then continue
L7      if U(k + 1, c_w, c_v) > z then        ▷ the child that leaves item k + 1
L8          PUSH(S, (k + 1, c_w, c_v, X))
L9      if c_w + w_{k+1} ≤ W then              ▷ the child that takes item k + 1
L10         PUSH(S, (k + 1, c_w + w_{k+1}, c_v + v_{k+1}, X ∪ {k + 1}))
L11 return (z, best)
```

The child that takes item $k + 1$ is pushed last, so it is explored first. It needs no bound test: when item $k + 1$ fits, the fractional greedy fill of the parent takes it whole first, so the child has the same bound as the parent, which passed line L6. Two features set this apart from the generic [depth-first branch and bound](/depth-first-branch-and-bound/): the incumbent is updated at every node (line L5), because every node is a feasible packing, and the search may stop below depth $n$.

## Example

Capacity $W = 16$ and four items, already in ratio order:

| item | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| value | 40 | 30 | 50 | 10 |
| weight | 2 | 5 | 10 | 5 |
| value / weight | 20 | 6 | 5 | 2 |

At the root, the greedy fill takes items 1 and 2, weight 7, and then $9/10$ of item 3: $U = 40 + 30 + 45 = 115$.

| step | node popped: items taken, depth | $c_v$ | $z$ after L5 | $U$ | action |
|---|---|---|---|---|---|
| 1 | $\{\}$, 0 | 0 | 0 | 115 | push leave (82), push take 1 |
| 2 | $\{1\}$, 1 | 40 | 40 | 115 | push leave (98), push take 2 |
| 3 | $\{1, 2\}$, 2 | 70 | 70 | 115 | push leave (80); item 3 does not fit |
| 4 | $\{1, 2\}$, 3 | 70 | 70 | 80 | leave gives 70: not pushed; push take 4 |
| 5 | $\{1, 2, 4\}$, 4 | 80 | 80 | 80 | depth 4 |
| 6 | $\{1\}$, 2 | 40 | 80 | 98 | leave gives 50: not pushed; push take 3 |
| 7 | $\{1, 3\}$, 3 | 90 | 90 | 98 | leave gives 90: not pushed; item 4 does not fit |
| 8 | $\{\}$, 1 | 0 | 90 | 82 | $82 \le 90$: fathomed |

The answer is items 1 and 3, weight 12, value 90. The search pops 8 nodes and never holds more than 3 on the stack. The tree of all feasible decisions has 26 nodes. The generic depth-first branch and bound with the same bound, which updates the incumbent only at depth $n$, expands 6 nodes and holds up to 4.

## Correctness

Three facts give the result. First, the greedy fill solves the fractional knapsack exactly (the [greedy fractional knapsack](/greedy-fractional-knapsack/) theorem), and a 0-1 packing is a fractional packing, so $U(k, c_w, c_v) \ge c_v + \text{(value of any feasible way to complete } X)$; since values are integers, so is the rounded-down bound. Second, the child that takes item $k+1$ has the same bound as the parent, so pushing it without a test loses nothing. Third, at the start of each iteration, every feasible set with value above $z$ extends the set $X$ of some node on the stack, in the sense that it agrees with $X$ on the decided items. Nodes leave the stack only when they cannot hold such a set. When the stack is empty, no feasible set beats $z$, and $z$ is the value of the feasible set $best$. The [proof](proofs/correctness.md) gives the details.

## Complexity

- **Time.** The sort takes $O(n \log n)$. The tree has at most $2^{n+1} - 1$ nodes, and each node costs $O(n)$ for its bounds, so the worst case is $O(n 2^n)$. Keeping prefix sums of weights and values and finding the first item that does not fit by [binary search](/binary-search/) makes each bound $O(\log n)$.
- **The worst case is reached.** Take $n$ even and $n$ items with $v_i = w_i = 2$, and $W = n + 1$. The optimum is $n$, but the fractional bound of every node that can still reach $n$ is $n + 1$, so nothing is fathomed until the remaining items are too few. The search pops $\binom{n+1}{n/2} - 1$ nodes: 461 for $n = 10$, 92 377 for $n = 18$, and 352 715 for $n = 20$, which grows like $2^n / \sqrt{n}$. Chvatal (1980) gave harder families on which a wide class of branch and bound methods take exponential time.
- **Best case.** If all items fit, the first path takes them all, $z$ reaches the bound of the root, and every other node is fathomed: $O(n)$ nodes at $O(n)$ each, so $O(n^2)$ time, or $O(n \log n)$ with the prefix sums.
- **Space.** When a node at depth $k$ is popped, the stack holds at most one node for each depth up to $k$, plus the two children; so it has at most $n + 1$ entries. Each holds a set of up to $n$ items, which is $O(n^2)$ words in total. A recursive form with one shared array for $X$ uses $O(n)$.

## Properties

- **Exact.** It returns an optimal packing.
- **Anytime.** The first dive is the greedy packing in ratio order, so the first incumbent is at least as good as that greedy solution.
- **Bound quality.** The fractional bound is at most the optimum plus the value of one item, $v_j$ for the first item $j$ that does not fit at the root. When values are large against $v_j$, the bound is tight and the tree is small.
- **Does not depend on $W$.** Unlike the dynamic program, the running time does not grow with the size of the numbers.

## Variants and improvements

- **Best-first order.** Kolesar (1967) gave the first branch and bound algorithm for the knapsack problem, which branches on the node with the largest bound, as in [best-first branch and bound](/best-first-branch-and-bound/). It uses more memory.
- **Horowitz and Sahni (1974).** Their depth-first algorithm adds whole runs of items in one forward step, as long as they fit, and backtracks by removing the last item taken; it is the base of many later codes.
- **Stronger bounds.** Martello and Toth improve the fractional bound by looking one item further, at the cases where the critical item is taken or left.
- **Core problems and reduction.** Fix in advance the items whose decision is clear from bounds, and search only over the items with ratios close to that of the critical item.
- **Dominance.** Two nodes at the same depth with $c_w \ge c_w'$ and $c_v \le c_v'$: the first is dominated and can be dropped. See [dominance pruning](/dominance-pruning/).

## When to use it

Use branch and bound for 0-1 knapsack when the capacity and weights are large, so that the $O(n W)$ dynamic program is too slow, and when the instance is not built to defeat the fractional bound. For small $W$, use the [dynamic program](/knapsack-dynamic-programming/). When an approximate answer is enough, a fully polynomial approximation scheme gives a $(1 - \varepsilon)$ guarantee.

## Pitfalls

- **Unsorted items.** The fractional bound and the "take child needs no test" argument both need the items in ratio order. Sort first, and map the indices back at the end.
- **Float ratios.** Comparing $v_i / w_i$ in floating point can break ties wrongly or round a bound below the truth. Compare $v_i w_j$ with $v_j w_i$, and compute the bound with integer division.
- **Weight 0.** An item with $w_i = 0$ has an infinite ratio. Put it first, or take it in advance.
- **Strict test.** With $U \le z$ the search finds one optimal packing; to list all optimal packings, fathom only on $U < z$.
- **Leaves only.** Updating the incumbent only at depth $n$ is still correct but wastes nodes, since every node is feasible.

## Implementations

## History

Kolesar (1967) published a branch and bound algorithm for the 0-1 knapsack problem with the fractional bound and best-first selection. Horowitz and Sahni (1974) gave a depth-first algorithm in the same paper in which they introduced the two-list method for knapsack and partition problems. Martello and Toth (1990) survey the later algorithms. Chvatal (1980) showed that some families of instances defeat a broad class of such methods.

## References
