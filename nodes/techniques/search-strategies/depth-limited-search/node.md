---
tag: T1ZWEX
kind: algorithm
slug: depth-limited-search
name: Depth-limited search
aliases:
- bounded depth-first search
area: techniques/search-strategies
level: intro
summary: Depth-first search that refuses to expand states beyond a fixed depth bound.
solves: [state-space-search]
model: word-ram
complexity:
  vars: {b: the branching factor, l: the depth limit}
  time: {worst: O(b^l), best: O(1)}
  space: {extra: O(b l)}
properties: {deterministic: true, recursive: true}
prereqs: [depth-first-search, search-tree, recursion]
see_also: [iterative-deepening-search, depth-first-search, search-strategy, completeness-and-optimality-of-search, graph-search-vs-tree-search, iterative-deepening-a-star, minimax, branching-factor]
sources:
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 3, Section 3.4.4 (depth-limited and iterative deepening search, the values failure and cutoff, and the check for cycles)
  - paper: doi:10.1016/0004-3702(85)90084-0
    title: Richard E. Korf, Depth-first iterative-deepening, an optimal admissible tree search, Artificial Intelligence 27(1) (1985)
    locator: pp. 97 to 109 (depth-first search with a depth cutoff as the inner loop of iterative deepening, and its time and space in a tree of branching factor b)
  - book: isbn:9780201055948
    title: Judea Pearl, Heuristics, Intelligent Search Strategies for Computer Problem Solving
    locator: Chapter 2 (depth-first and backtracking search with a depth bound)
---

Depth-limited search is [depth-first search](/depth-first-search/) that treats each node at a fixed depth $\ell$ as if it had no children. It always stops, it uses memory linear in $\ell$, and it finds a goal if and only if some goal has a path of at most $\ell$ actions. Its answer has three values: a path, *cutoff* when the limit hid part of the space, or *failure* when no goal can be reached at all. It is the inner loop of [iterative deepening search](/iterative-deepening-search/).

## In plain words

You explore a cave system with a rope of fixed length. You always take the first passage you have not tried, and you go as deep as you can. When the rope ends, you do not go further: you come back one step and try the next passage.

If you find the treasure, you are done. If you do not, the rope tells you something. If the rope stopped you somewhere, the treasure may be deeper, and a longer rope may help. If the rope never stopped you, you have seen the whole cave, and there is no treasure.

You carry only the rope and the list of passages on your way back, so you need little memory. But the first treasure you find need not be the nearest one.

## The problem

The input is a [state-space search](/state-space-search/) problem: a start state $s_0$, a function SUCCESSORS that gives a finite list of next states, a goal test IS-GOAL, and a depth limit $\ell \ge 0$. The output is one of three values.

- A path from $s_0$ to a goal state with at most $\ell$ actions.
- *cutoff*: no goal is within depth $\ell$, and some path from $s_0$ has more than $\ell$ actions.
- *failure*: no goal can be reached from $s_0$.

Action costs play no part. The search counts actions only.

## The algorithm

The recursive version keeps a set *onpath* of the states on the current path, and skips a child whose state is already on it. This check for cycles is optional. Without it, the search is the pure tree-like version, and it still stops, but it reports *cutoff* on each space with a reachable cycle.

```pseudo id=main
DEPTH-LIMITED-SEARCH(s0, SUCCESSORS, IS-GOAL, ℓ)
L1  onpath ← { s0 }
L2  return DLS(s0, ℓ)

DLS(s, k)                                         ▷ k = the number of actions left
L3  if IS-GOAL(s) then return [s]
L4  if k = 0 then
L5      if some s' in SUCCESSORS(s) is not in onpath then return cutoff
L6      return failure
L7  cut ← false
L8  for each s' in SUCCESSORS(s) that is not in onpath do
L9      add s' to onpath
L10     r ← DLS(s', k − 1)
L11     remove s' from onpath
L12     if r is a path then return [s] followed by r
L13     if r = cutoff then cut ← true
L14 if cut then return cutoff else return failure
```

Line L5 is what separates *cutoff* from *failure*: a node at the limit reports *cutoff* only when the limit actually hides a child. Line L12 returns at once, so the search does not look for a better goal after the first one.

## Example

The graph has the directed edges S→A, S→G, A→B, A→C, B→D, C→D, C→G, D→G, and children are tried in this order. With the goal D, the limits 0, 1 and 2 give *cutoff*, and the limit 3 returns S-A-B-D after 4 goal tests. With a goal E that is not in the graph, the answers are:

| limit $\ell$ | answer | goal tests |
| --- | --- | --- |
| 0 | cutoff | 1 |
| 1 | cutoff | 3 |
| 2 | cutoff | 5 |
| 3 | cutoff | 8 |
| 4 | failure | 10 |

The longest path from S is S-A-B-D-G with 4 actions, so the limit 4 is the first that shows the whole space, and only then can the search report failure. The run with $\ell = 3$:

| call | $k$ | what happens | result |
| --- | --- | --- | --- |
| DLS(S, 3) | 3 | not a goal, try A then G | cutoff |
| DLS(A, 2) | 2 | try B then C | cutoff |
| DLS(B, 1) | 1 | try D | cutoff |
| DLS(D, 0) | 0 | limit reached, D has the child G | cutoff |
| DLS(C, 1) | 1 | try D then G | cutoff |
| DLS(D, 0) | 0 | limit reached, D has the child G | cutoff |
| DLS(G, 0) | 0 | limit reached, G has no child | failure |
| DLS(G, 2) | 2 | no child to try | failure |

The state D is tested twice, once on each path to it. Depth-limited search keeps no table of reached states, so it repeats work on a graph with many paths to a state.

On the two states $u$ and $v$ with the moves $u \to v$ and $v \to u$ and no goal, the search with the check for cycles returns failure for each $\ell \ge 1$: from $v$, the only child $u$ is on the path. Without the check it returns cutoff for each $\ell$, because the path $u, v, u, \ldots$ is longer than every limit.

## Correctness

The search tree here is the tree of paths from $s_0$ that do not repeat a state (with the check for cycles) or of all paths (without it). The proofs below show three facts.

- **Termination.** Each call has a smaller $k$ than its caller, and each state has finitely many children, so the recursion tree is finite.
- **A returned path is a solution.** It starts at $s_0$, follows SUCCESSORS, ends at a goal and has at most $\ell$ actions.
- **The answer is exact.** The search returns a path if and only if some goal has a path of at most $\ell$ actions from $s_0$. It returns failure only when no goal is reachable at all.

The returned path need not be the shortest one, nor the cheapest. Above, with the goal G and $\ell = 4$, the search returns S-A-B-D-G with 4 actions, while S-G has 1.

## Complexity

The costs are in the [word RAM](/word-ram/), with each call of SUCCESSORS and IS-GOAL and each operation on *onpath* counted as $O(1)$ ($O(1)$ expected for a hash set). In a tree with [branching factor](/branching-factor/) $b \ge 2$, the search makes at most one call for each node of depth at most $\ell$, so it does at most
$$ N(b, \ell) = \sum_{i=0}^{\ell} b^i = \frac{b^{\ell+1} - 1}{b - 1} \le \frac{b}{b - 1} \, b^\ell $$
goal tests. This count, the number of nodes generated, is the time measure of Russell and Norvig, and it gives $O(b^\ell)$. A call also reads the children that the check for cycles skips. Their states are on the current path, so there are at most $\ell + 1$ of them per call when the children of a state are distinct, and the time with these reads is $O(\ell \, b^\ell)$ in the worst case. The bound is tight: in the uniform tree of branching factor $b$ with no goal, the search tests all $N(b, \ell)$ nodes. Every algorithm that finds each goal within depth $\ell$ must do the same on that tree, by an [adversary argument](/adversary-argument/): an untested node of depth at most $\ell$ could be the only goal.

The recursion has depth $\ell + 1$, and each frame holds a state, a counter and the place in the list of children. So the extra space is $O(\ell)$ when SUCCESSORS gives the children one at a time, and $O(b\ell)$ when it returns them as a list. The set *onpath* holds at most $\ell + 1$ states. In the best case $s_0$ is a goal, and the search does $O(1)$ work.

## Properties

- **Always stops**, on each problem with a finite branching factor, even on an infinite space.
- **Complete only within the limit.** It finds a goal when one exists at depth at most $\ell$. If the shallowest goal is deeper, it returns cutoff. Russell and Norvig rate it as not complete, since the limit can be too small.
- **Not optimal.** It returns the first goal in depth-first order, not a shallowest or a cheapest one.
- **Linear memory.** The space is $O(b\ell)$, against $O(b^d)$ for [breadth-first search](/breadth-first-search/).
- **Tree-like.** It keeps no table of reached states, so it can test the same state once for each path to it.

## Variants and improvements

- **[Iterative deepening search](/iterative-deepening-search/).** Run depth-limited search with $\ell = 0, 1, 2, \ldots$ until the answer is not cutoff. This gives a shallowest goal with linear memory.
- **Cost-limited search.** Replace the depth by the path cost $g$, or by $f = g + h$, and cut each node whose value is above the limit. This is the inner loop of [IDA*](/iterative-deepening-a-star/).
- **Depth-limited game-tree search.** [Minimax](/minimax/) and [alpha-beta pruning](/alpha-beta-pruning/) search the [game tree](/game-tree/) to a fixed depth and score the positions at the limit with an evaluation function, instead of returning cutoff.
- **Path check of bounded length.** Instead of the full set *onpath*, check only the last few states of the path. This removes short cycles at a lower cost.
- **Explicit stack.** The recursion can be replaced by a [stack](/stack/) of (node, depth) pairs, as in the version of Russell and Norvig. Then the cycle check walks the parent pointers of the node.

## When to use it

Use depth-limited search when you know a bound on the depth of a solution, for example the diameter of the state space or a bound from the problem, and memory is the limit. A good bound makes it complete. If you know no bound, use iterative deepening search, which finds the right limit by itself at a small extra cost. If the space has many paths to each state and memory is not a problem, a graph search such as breadth-first search avoids the repeated work.

## Pitfalls

- **Treating cutoff as failure.** Cutoff only says that no goal is within depth $\ell$. A program that reports "no solution" on cutoff is wrong. Iterative deepening search depends on the difference: it stops on failure and goes on after cutoff.
- **Reporting cutoff with no hidden child.** If line L5 returns cutoff for each node at the limit, the search never returns failure on a finite space, and iterative deepening on top of it never stops when no goal exists.
- **Off by one in the limit.** Decide whether $\ell$ counts actions or states and keep to it. Here the root has depth 0, and a path of $\ell$ actions is still found.
- **A global visited set.** Marking states as visited for the whole run, instead of only on the current path, makes the search miss goals: a state reached first by a deep path, close to the limit, is not explored again when a shorter path reaches it later.
- **The recursion limit.** In a language with a small call stack, a large $\ell$ overflows it. Use an explicit stack, or raise the limit as the reference implementation does.

## Implementations

## History

Depth-first search with a depth bound is one of the oldest search methods of artificial intelligence and of backtracking. It is used as a cut-off in game-playing programs and as the inner step of search with increasing bounds. Korf (1985) analysed it as the inner loop of depth-first iterative deepening, with time $O(b^d)$ and space $O(d)$. Russell and Norvig give it the three answers solution, cutoff and failure, which this page follows.

## References
