---
tag: 2Y0M90
kind: algorithm
slug: beam-stack-search
name: Beam-stack search
area: games-and-search/heuristic-search
level: research
summary: Beam search that records, for each layer, the range of f values it kept, and backtracks to the next range when a layer is empty. It finds better paths over time and ends with an optimal one.
solves: [state-space-search]
model: word-ram
complexity:
  vars: {k: the beam width, b: the largest number of successors of a state, n: the number of reachable states, t: "the number of layers that the search builds, counting the ones it builds again"}
  time: {worst: O(t b n log n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
history:
  year: 2005
  people: [Rong Zhou, Eric A. Hansen]
  note: Zhou and Hansen presented beam-stack search at ICAPS 2005 as a complete, anytime form of beam search for planning.
prereqs: [beam-search, depth-first-branch-and-bound]
see_also: [anytime-repairing-a-star, iterative-deepening-a-star, memory-bounded-heuristic-search, breadth-first-branch-and-bound, limited-discrepancy-search, duplicate-detection, consistent-heuristic]
sources:
  - paper: Rong Zhou and Eric A. Hansen, Beam-stack search, integrating backtracking with beam search, Proceedings of the 15th International Conference on Automated Planning and Scheduling (ICAPS 2005)
    locator: pp. 90 to 98 (the beam stack of ranges [fmin, fmax), backtracking, the proof of optimality, and divide-and-conquer beam-stack search)
---

Beam-stack search makes [beam search](/beam-search/) complete and, in the end, optimal. Plain beam search keeps only the $k$ best successors of each layer and forgets the rest, so it can miss every path to the goal. Beam-stack search keeps a stack with one item per layer, the range $[f_{\min}, f_{\max})$ of values $f = g + h$ that the layer admitted. When a layer comes out empty, or a goal is found, the search goes back to the deepest layer that still has unexplored successors and builds it again from the next range $[f_{\max}, U)$, where $U$ is the cost of the best path so far. It is [depth-first branch and bound](/depth-first-branch-and-bound/) over slices of layers instead of single states. Like beam search, it finds a first path fast. Each new path is cheaper, and when the stack is empty the last path is optimal. Zhou and Hansen introduced it in 2005.

## In plain words

Beam search walks forward with a small group and forgets every place the group did not choose. If it reaches a dead end, it gives up.

Beam-stack search writes a note at each step: "here we took the best few places, up to this score". At a dead end, it goes back one step, reads the note, and now takes the next few places, the ones it skipped. If those also fail, it goes back further. When it finds a way out, it remembers how long that way was and from then on ignores any place that cannot lead to a shorter way. When there are no notes left, nothing it skipped could have been shorter, so the best way it found is the best way there is.

## The problem

The input is a [state-space search](/state-space-search/) problem in which each action costs 1: a start state $s_0$, a function SUCCESSORS that gives the finite list of next states, a goal test IS-GOAL, a [consistent heuristic](/consistent-heuristic/) $h$ with $h = 0$ at goals, and a width $k \ge 1$. The output is a sequence of paths to a goal, each cheaper than the one before, and the last one is optimal. If no goal is reachable, the output is empty. This page and its implementation assume unit costs, so the cost of a state in layer $i$ is $i$.

## The algorithm

```pseudo id=main
BEAM-STACK-SEARCH(s0, SUCCESSORS, IS-GOAL, h, k)
L1  U ← ∞
L2  LAYERS ← [ [s0] ], STACK ← an empty stack
L3  loop
L4      i ← the number of layers; if STACK has fewer than i items then push [0, U) for layer i
L5      [fmin, fmax) ← the top item; CAND ← successors m of layer i − 1 that are in no stored layer
L6      keep m in CAND only if fmin ≤ f(m) = i + h(m) < fmax and f(m) < U
L7      if CAND has a goal m then U ← i, publish the path to m, KEEP ← ∅
L8      else KEEP ← CAND; if |CAND| > k then KEEP ← the states of CAND with f below the f of the (k + 1)-th best
L9          and set fmax of the top item to that f
L10     if KEEP ≠ ∅ then append KEEP as layer i and go to L3
L11     pop the items whose fmax ≥ U
L12     if STACK is empty then return the last published path, or failure
L13     replace the top item [fmin, fmax) by [fmax, U)
L14     delete the stored layers above the top item
```

The item for layer $i$ says which slice of the successors of layer $i - 1$ the stored layer $i$ holds. Line L8 cuts at the $f$ of the best state it drops, so the kept slice is exactly the candidates with $f$ in the new range $[f_{\min}, f_{\max})$, and the dropped ones are exactly those with $f \ge f_{\max}$. Line L13 then moves on to them. Line L11 removes an item when its range has reached $U$: every successor with $f < U$ of that layer has had its turn.

**A tie rule.** If the $k + 1$ best candidates all have the same $f$, line L8 would keep nothing. The implementation then keeps all the candidates of least $f$ and sets $f_{\max}$ to the next larger $f$ value. This rule is ours: it keeps each slice nonempty, at the cost of a layer that can hold more than $k$ states.

**Duplicates.** A successor that is in a stored layer is dropped at line L5. The stored layers are the layers of the current beam, so they play the part of the closed list. In the paper, keeping only some of these layers gives divide-and-conquer beam-stack search, which needs less memory and rebuilds the path at the end.

The search also skips the expansion of a state $n$ of layer $i - 1$ with $i - 1 + h(n) \ge U$, since with a consistent $h$ none of its successors can have $f < U$.

## Example

The 8-puzzle instance comes from `random.Random(2024)`: the goal after 60 random moves. It is the state 0 2 6 / 8 3 5 / 1 7 4, read by rows with 0 for the blank, and its optimal cost is 18. The heuristic is the Manhattan distance, which is consistent. The table gives the costs of the paths that the search publishes, in order, the number of expanded states, the number of backtracks (visits of line L13) and the largest number of stored states.

| width | published costs | expanded | backtracks | most states stored |
| --- | --- | --- | --- | --- |
| 1 | 22, 18 | 144 | 10 | 50 |
| 2 | 22, 18 | 149 | 10 | 53 |
| 5 | 36, 32, 22, 18 | 481 | 17 | 131 |
| 20 | 18 | 201 | 0 | 201 |
| 100 | 18 | 857 | 0 | 857 |
| 1000 | 18 | 6,032 | 0 | 6,032 |

Each run ends with cost 18. With small widths, the first path is poor and the search backtracks to improve it. With width 20 and more, the first beam already holds an optimal path, and the search only has to show that nothing cheaper exists, which here takes no backtrack: when the goal is found at depth 18, each stored range reaches $U = 18$ and line L11 pops them all. Larger widths cost more because each layer holds more states.

Plain beam search on the same instance returns a path of cost 32 with width 1, 22 with widths 2 and 5, and 18 with width 20 and more, and then stops. With width 1, beam-stack search finds 22 at once, not 32, because the tie rule keeps all candidates that tie for the least $f$.

Over the first 10 instances of the same generator with optimal cost $d \ge 14$, each run of beam-stack search ended with an optimal path:

| width | expanded, all 10 | backtracks, all 10 | most states stored in one run | mean of first cost divided by $d$ |
| --- | --- | --- | --- | --- |
| 1 | 49,153 | 3,786 | 378 | 3.93 |
| 5 | 39,622 | 1,566 | 321 | 2.92 |
| 20 | 9,656 | 85 | 692 | 1.475 |
| 100 | 7,658 | 0 | 932 | 1 |

On these instances, a small width gave a poor first path and many backtracks, and a large width gave a good first path at a higher memory cost. These numbers are measured on these instances only.

## Correctness

The [proof](proofs/correctness.md) shows, for unit costs and a consistent $h$:

- **Valid and improving paths.** Each published path is a real path to a goal of cost $U$, and each one is cheaper than the one before.
- **Termination.** The list of $f_{\min}$ values on the stack grows in lexicographic order at each step, and it has finitely many values, so the search stops on a finite graph.
- **Optimality.** For an optimal path $p_0, \ldots, p_D$, as long as $U > D$, the search builds a layer $j + 1$ that holds $p_{j+1}$ before it drops the item of a layer $j$ that holds $p_j$. So it cannot empty the stack with $U > D$.

## Complexity

Costs are in the [word RAM](/word-ram/), with each call of SUCCESSORS, IS-GOAL and $h$ counted as $O(1)$.

**One layer.** A layer holds at most $k$ states unless the tie rule applies, and at most $n$ states in any case. Building the next layer looks at $O(k b)$ successors and sorts them, so it takes $O(k b \log(k b))$ time, or $O(b\,n \log n)$ in the worst case.

**All layers.** The search builds $t$ layers in all, counting each layer it builds again after a backtrack, so the time is $O(t\,b\,n \log n)$, and $O(t\,k\,b \log(k b))$ without large ties. The number $t$ is finite but has no good bound: as in depth-first branch and bound, the number of backtracks can grow exponentially with the depth. In the tables, it falls fast as the width grows.

**Space.** The stored layers are disjoint, so they hold at most $n$ states. Without large ties they hold $O(d\,k)$ states for a deepest layer $d$, and the stack holds $d$ items. This is the point of the method: the memory is set by the width, not by the size of the graph. Divide-and-conquer beam-stack search keeps only a few layers and so uses even less.

## Properties

- **Complete and optimal** on a finite graph, for unit costs and a consistent $h$.
- **Anytime.** It publishes a first path soon, then only cheaper ones.
- **Memory bounded by the width**, apart from ties: about $k$ states per layer.
- **Deterministic**, with the tie rule and the order of SUCCESSORS.
- **Not recursive.** The beam stack replaces the call stack of a depth-first search.

## Variants and improvements

- **Divide-and-conquer beam-stack search.** Zhou and Hansen store only a few layers, as in breadth-first heuristic search, and rebuild the path by solving smaller problems. Memory then grows with the width and not with the depth.
- **[Limited discrepancy search](/limited-discrepancy-search/)** is another way to undo the choices of a greedy search, by the number of times it goes against the heuristic instead of by ranges of $f$.
- **[Anytime repairing A*](/anytime-repairing-a-star/)** also improves paths over time, with a proved bound on each path, but it stores the whole graph that it has seen.

## When to use it

Use beam-stack search when you want the first path of a beam search but must prove optimality in the end, and the graph is too large for [A*](/a-star-search/). Planning and scheduling problems with deep search spaces and a consistent heuristic are the typical case. If memory is not the limit, A* or ARA* is simpler. If the graph has few duplicates, [IDA*](/iterative-deepening-a-star/) needs even less memory.

## Pitfalls

- **Empty slices.** If the $k + 1$ best candidates tie, the cut of line L8 keeps nothing, and the search can backtrack forever on the same range. Use a tie rule such as the one above.
- **Inconsistent heuristics.** The skip of states with $f \ge U$ and the order of ranges assume that $f$ does not fall along a path. With an inconsistent $h$, an optimal path can be cut.
- **Mixing up the ranges after $U$ drops.** Line L11 must compare each $f_{\max}$ with the current $U$, which is smaller than the $U$ that was in force when the item was pushed.
- **Forgetting to delete the layers above the backtrack point.** They belong to the old slice and give wrong duplicates for the new one.
- **Small widths.** Width 1 is often not the cheapest choice: in the tables it needed thousands of backtracks.

## Implementations

## History

Beam-stack search builds on breadth-first heuristic search, a layered search by the same authors that keeps only a few layers in memory. In 2005, at ICAPS, Zhou and Hansen added the beam stack to a beam search of this kind and showed that the result is complete and optimal, and that it improves its path over time. They also gave the divide-and-conquer form with memory bounded by the width. The method joins two old ideas: the bounded memory of the beam search of Lowerre's Harpy system (1976), and the systematic backtracking of depth-first branch and bound.

## References
