---
tag: 5WXKC7
kind: algorithm
slug: iterative-broadening
name: Iterative broadening
aliases:
- iterative broadening search
area: techniques/search-strategies
level: research
summary: Repeats a search with an increasing breadth limit at each node, so early choices are explored before later ones.
solves: [state-space-search]
model: word-ram
complexity:
  vars: {b: the branching factor, d: the depth of the tree}
  time: {worst: O((1 + b/d) b^d), best: O(1)}
  space: {extra: O(d)}
properties: {deterministic: true, recursive: true}
prereqs: [depth-first-search, iterative-deepening-search, search-tree]
see_also: [iterative-deepening-search, depth-limited-search, limited-discrepancy-search, generic-backtracking-algorithm, constraint-satisfaction-problem, beam-search, search-strategy, state-space-tree]
sources:
  - paper: doi:10.1016/0004-3702(92)90059-7
    title: Matthew L. Ginsberg and William D. Harvey, Iterative broadening, Artificial Intelligence 55(2-3) (1992)
    locator: pp. 367 to 383 (the breadth cutoff, the model with s successful children per successful node, the analysis of the expected time, and the experiments)
  - paper: "Matthew L. Ginsberg and William D. Harvey, Iterative broadening, Proceedings of the Eighth National Conference on Artificial Intelligence (AAAI-90) (1990)"
    title: Iterative broadening, AAAI-90
    locator: pp. 216 to 220 (Section 1 for the method, Section 2 for the formal model, Section 3 for the tables of speedups and Proposition 3.1, Section 4 for heuristic order)
  - paper: doi:10.1016/0004-3702(85)90084-0
    title: Richard E. Korf, Depth-first iterative-deepening, an optimal admissible tree search, Artificial Intelligence 27(1) (1985)
    locator: pp. 97 to 109 (iterative deepening, the scheme of repeated bounded searches that iterative broadening follows)
---

Iterative broadening is [depth-first search](/depth-first-search/) with a *breadth cutoff* $c$: each run looks only at the first $c$ children of each node, and the runs use $c = 2, 3, 4, \ldots$ until one finds a goal or prunes nothing. Ginsberg and Harvey introduced it for deep search trees with many goals, where a bad choice near the root can trap depth-first search in a large subtree with no goal. A narrow run gets out of such a subtree fast. Its name follows [iterative deepening](/iterative-deepening-search/), which bounds the depth instead of the breadth.

## In plain words

You look for a gift. Your plan has steps: pick a kind of gift, pick a shop, pick an item. A stubborn search tries every shop for the first kind of gift before it thinks of a second kind. If the first kind was a bad idea, you waste the whole day.

Iterative broadening gives up early. At each step it tries only the first two options and then goes back. If that fails, it starts again with three options at each step, then four. A bad first choice now costs little, because you leave it after two tries. When there are many good gifts, one of the narrow rounds often finds one. In the worst case, the extra rounds cost a little more than one full search.

## The problem

The input is a search problem whose [search tree](/search-tree/) is finite: a start state $s_0$, a function SUCCESSORS that gives the ordered list of children of a state, and a goal test IS-GOAL. Each path of the tree ends, as in a [constraint satisfaction problem](/constraint-satisfaction-problem/) with $n$ variables, where a path assigns the variables one by one. The output is a path from $s_0$ to a goal, or failure when the tree has no goal. The aim is to find any goal fast, not a best one.

## The algorithm

```pseudo id=main
ITERATIVE-BROADENING(s0, SUCCESSORS, IS-GOAL)
L1  for c ← 2, 3, 4, ... do
L2      pruned ← false
L3      r ← BOUNDED(s0, c)
L4      if r ≠ failure then return r
L5      if not pruned then return failure

BOUNDED(s, c)
L6  if IS-GOAL(s) then return [s]
L7  children ← SUCCESSORS(s)
L8  if |children| > c then pruned ← true
L9  for each s' among the first c of children do
L10     r ← BOUNDED(s', c)
L11     if r ≠ failure then return [s] followed by r
L12 return failure
```

The flag *pruned* plays the part of *cutoff* in [depth-limited search](/depth-limited-search/). A run that pruned no child was a full depth-first search, so its failure is final. Ginsberg and Harvey state the cutoff as a count of backtracks: after the search has come back to a node $c$ times, it goes back further, even if the node has children left. This is the same as trying only its first $c$ children.

## Example

The tree is the uniform tree of branching factor 3 and depth 3, whose nodes are the sequences of length at most 3 over $\{0, 1, 2\}$, with children in increasing order. The goals are the leaves $(1, 0, 1)$, $(1, 2, 2)$ and $(2, 1, 0)$. The subtree under $(0)$ has no goal.

| search | nodes goal-tested | path |
| --- | --- | --- |
| depth-first search | 18 | $(), (1), (1,0), (1,0,1)$ |
| iterative broadening, run $c = 2$ | 12 | $(), (1), (1,0), (1,0,1)$ |

The run with $c = 2$ tests $()$, then the 7 nodes $(0), (0,0), (0,0,0), (0,0,1), (0,1), (0,1,0), (0,1,1)$ of the cut subtree under $(0)$, then $(1), (1,0), (1,0,0), (1,0,1)$. Depth-first search tests all 13 nodes under $(0)$ before it leaves it.

### Random trees with many goals

Ginsberg and Harvey model a tree of branching factor $b$ and depth $d$ with goals only at depth $d$, in which each node with a goal below it has exactly $s$ children with a goal below them, at random places among its $b$ children. The table gives averages over 100 random trees of this kind, with the nodes goal-tested by each search.

| $b$ | $d$ | $s$ | depth-first search | iterative broadening | speedup |
| --- | --- | --- | --- | --- | --- |
| 4 | 6 | 2 | 1,121.15 | 340.96 | 3.29 |
| 6 | 6 | 2 | 14,924.16 | 5,560.82 | 2.68 |
| 6 | 6 | 3 | 9,121.24 | 746.70 | 12.22 |

The gain grows with $s$, the number of good choices at each step. Ginsberg and Harvey report speedups of the same order in their experiments, and larger ones for deeper trees.

## Correctness

The proofs below show three facts, for a finite tree.

- **Soundness.** A returned list is a path of the tree from $s_0$ to a goal, because BOUNDED adds a state in front of a path only when that path starts at one of its children.
- **Termination.** Each run is a depth-first search of a finite tree. Let $B$ be the largest number of children of a node. The run with $c = \max(2, B)$ prunes nothing, so the loop ends by that run at the latest.
- **Completeness.** A run that prunes nothing visits every node of the tree, so it finds a goal when one exists. Failure is returned only after such a run.

## Complexity

The costs are in the [word RAM](/word-ram/), with each call of SUCCESSORS and IS-GOAL counted as $O(1)$. Take the uniform tree of branching factor $b \ge 2$ and depth $d$. The run with cutoff $c$ visits the tree cut to breadth $c$, with $c^d$ leaves and $(c^{d+1} - 1)/(c - 1) \le 2c^d$ nodes. In the worst case, when the only goal is the last leaf of the full depth-first order, all runs $c = 2, \ldots, b$ take place. Their leaves number
$$ \sum_{c=2}^{b} c^d \le b^d + \int_{1}^{b} x^d \, dx < b^d + \frac{b^{d+1}}{d+1} = \Bigl(1 + \frac{b}{d+1}\Bigr) b^d , $$
because $c^d \le \int_c^{c+1} x^d\,dx$ for the terms $c \le b - 1$. So the worst-case time is $O((1 + b/d)\, b^d)$, against $\Theta(b^d)$ for one depth-first search. For deep trees, with $d \ge b$, the overhead is at most a factor of about 2. The table compares the total number of nodes of all runs with the nodes of one full search.

| $b$ | $d$ | nodes, all runs | nodes, one full run | ratio | $1 + b/(d+1)$ |
| --- | --- | --- | --- | --- | --- |
| 3 | 3 | 55 | 40 | 1.375 | 1.75 |
| 4 | 7 | 25,380 | 21,845 | 1.162 | 1.5 |
| 6 | 6 | 82,199 | 55,987 | 1.468 | 1.857 |
| 10 | 5 | 249,627 | 111,111 | 2.247 | 2.667 |

The space is that of one depth-first search: $O(d)$ frames, or $O(bd)$ when SUCCESSORS returns lists. In the best case $s_0$ is a goal, and the search does $O(1)$ work.

The gain is in expectation over the place of the goals. In the model with $s$ good children per good node, Ginsberg and Harvey estimate that, for large $d$, iterative broadening beats depth-first search whenever the number of goal leaves exceeds about $e^{b/2}$ (their Proposition 3.1). With a single goal at a random leaf, depth-first search is better, and they observed iterative broadening to be about 2 times slower.

## Properties

- **Complete on finite trees.** The last run is a full depth-first search.
- **Not complete on infinite trees.** A run can follow an infinite path. Combine it with a depth limit for such spaces.
- **Not optimal.** It returns some goal, not a shallowest or cheapest one.
- **Linear memory.** Like depth-first search.
- **Uses the order of the children.** The first $c$ children are the ones a heuristic ranks first, so a good value order helps it more than it helps plain depth-first search. Ginsberg and Harvey found that with a weak ordering heuristic, it was the better method in their experiments even with a single goal, once the branching factor and the depth were large enough.

## Variants and improvements

- **[Limited discrepancy search](/limited-discrepancy-search/).** Harvey and Ginsberg later bounded the number of times a path departs from the heuristic's first choice, instead of the number of children per node. It shares the idea that early mistakes should be cheap to undo.
- **Iterative widening.** The same scheme for game-tree search, where the breadth cutoff limits the moves considered at each position.
- **Combination with depth limits.** Bound both the depth and the breadth, and increase them together, for trees that are deep or infinite.
- **Other start values.** Starting at $c = 1$ adds a greedy probe down the leftmost path, which costs only $d + 1$ nodes.

## When to use it

Use iterative broadening for depth-first search of deep, finite trees with many solutions, such as [constraint satisfaction](/constraint-satisfaction-problem/) and scheduling problems, when a wrong early choice is costly and the value order is informative. Do not use it when the tree has one goal at a random place, or when a shortest or cheapest path is needed.

## Pitfalls

- **Stopping on failure of a pruned run.** Failure of a run that pruned a child says nothing about the full tree. The flag *pruned* is needed for a correct answer.
- **Infinite trees.** Without a depth bound, a run can go down an infinite path and never return.
- **Reordering the children between runs.** The analysis and the reuse of the order assume the same order in each run. Changing it can make a later run miss the parts that an earlier run cut.
- **Expecting a gain with few goals.** With one goal, the extra runs only cost time, up to the factor $1 + b/(d+1)$ above.

## Implementations

## History

Ginsberg and Harvey presented iterative broadening at AAAI-90 and in the journal Artificial Intelligence in 1992. They argued that the usual model of goals spread at random over the leaves is often wrong, and that a better model gives equal weight to the decisions at each level. They named the method after Korf's iterative deepening. Their later work on [limited discrepancy search](/limited-discrepancy-search/) developed the same idea.

## References
