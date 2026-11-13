---
tag: WJE1MW
kind: algorithm
slug: beam-search
name: Beam search
aliases:
- beam search with width k
- breadth-limited best-first search
area: games-and-search/heuristic-search
level: core
summary: Breadth-first search that keeps only the k best states of each layer by g + h. Time and memory per layer are bounded, but it can miss every path and is not optimal.
solves: [state-space-search]
model: word-ram
complexity:
  vars: {k: the beam width, b: the largest number of successors of a state, d: the number of layers the search builds}
  time: {worst: O(d k b log(k b))}
  space: {extra: O(d k + k b)}
properties: {deterministic: true, recursive: false}
history:
  year: 1976
  people: [Bruce Lowerre, Raj Reddy]
  note: Lowerre's Harpy speech recognition system at Carnegie Mellon kept only the best partial matches at each step, and the method became known as beam search.
prereqs: [best-first-search, breadth-first-search, heuristic-function]
see_also: [greedy-best-first-search, beam-stack-search, a-star-search, local-search, hill-climbing, viterbi-algorithm, limited-discrepancy-search, memory-bounded-heuristic-search]
sources:
  - paper: doi:10.1121/1.2003013
    title: Bruce Lowerre and Raj Reddy, Harpy, a connected speech recognition system, The Journal of the Acoustical Society of America 59(S1) (1976)
    locator: p. S97 (abstract of the Harpy system)
  - paper: Bruce T. Lowerre, The HARPY speech recognition system, PhD thesis, Carnegie Mellon University (1976)
    locator: the search of the Harpy network (general locator)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, 4th edition
    locator: Section 3.5.5 (beam search as a memory-bounded search that keeps the k nodes of best f) and Section 4.1.3 (local beam search)
---

Beam search is [breadth-first search](/breadth-first-search/) with a limit $k$ on the size of each layer. It builds the search one depth at a time, and from the successors of the current layer it keeps only the $k$ states with the least $f = g + h$, where $g$ is the cost so far and $h$ a [heuristic](/heuristic-function/) estimate of the cost to a goal. All the other successors are dropped for good. The number $k$ is the *beam width*. Each layer costs at most $k b$ successor calls, where $b$ bounds the number of successors, so the time and memory per layer do not grow with the size of the graph. The price is that beam search is neither complete nor optimal: the dropped states can hold every path to the goal. With $k = 1$ it is a form of [hill climbing](/hill-climbing/), and with no limit it is breadth-first search. Lowerre used it in the Harpy speech recognition system in 1976.

## In plain words

You walk through a maze with a few friends. At each step, everyone looks at the places one step ahead. You talk, and you keep only the few places that look closest to the exit. Each friend goes to one of them, and all the other places are forgotten.

This is fast and needs little memory, because the group never grows. But if the exit is behind a place that looked bad, nobody goes there. A larger group finds better ways and fails less often, but it costs more at each step. A group of one person simply goes where it looks best, and can walk into a dead end.

## The problem

The input is a [state-space search](/state-space-search/) problem: a start state $s_0$, a function SUCCESSORS that gives the finite list of pairs $(m, c)$ of a next state and the nonnegative cost of the action to it, a goal test IS-GOAL, a heuristic $h$, and a width $k \ge 1$. The output is a path from $s_0$ to a goal state, or *failure*. Beam search does not promise a path when one exists, nor the cheapest path when it finds one.

## The algorithm

```pseudo id=main
BEAM-SEARCH(s0, SUCCESSORS, IS-GOAL, h, k)
L1  if IS-GOAL(s0) then return the path (s0)
L2  LAYER ← [ s0 ], SEEN ← { s0 }, g[s0] ← 0
L3  while LAYER is not empty do
L4      CAND ← an empty map
L5      for each n in LAYER and each (m, c) in SUCCESSORS(n) with m ∉ SEEN do
L6          if m ∉ CAND or g[n] + c < the cost of m in CAND then record m in CAND with cost g[n] + c and parent n
L7      if some state of CAND is a goal then return the path to the cheapest such goal
L8      LAYER ← the k states of CAND with least g + h
L9      SEEN ← SEEN ∪ LAYER
L10 return failure
```

Line L5 skips the states that an earlier layer kept, so the search cannot go in circles and each layer adds new states to SEEN. Line L6 keeps, for each candidate, the cheapest way to it from the layer. Line L7 tests the goal on the whole candidate set before line L8 prunes it, so a goal one step away is never dropped. Line L8 is the only place where beam search throws work away. The implementation breaks ties in $g + h$ toward the candidate that was generated first, and with no width it keeps every candidate.

In a graph where each action costs 1, all states of a layer have the same $g$, so ranking by $g + h$ is the same as ranking by $h$. With general costs, $g + h$ keeps a cheap path from being dropped in favor of an expensive one that happens to point at the goal.

## Example

The grid has 5 rows and 6 columns, and each move to one of the four neighbors costs 1. S is at $(0, 0)$ in the top left, G at $(5, 4)$ in the bottom right, and # is a wall. The script draws it with `random.Random(804)`, each cell a wall with probability 0.3. The heuristic is the Manhattan distance to G.

```
S . . . . .
. . . # # .
. . . # . .
. . # . # #
# . . . . G
```

The cheapest path costs 9. It goes down column 1 and then right along the bottom row.

**Width 1.** Each layer is one state, the successor of least $h$. Ties go to the first one generated, which here is the move to the right. The layers are $(0,0)$, $(1,0)$, $(2,0)$, $(3,0)$, $(4,0)$, $(5,0)$, $(5,1)$, $(5,2)$ and $(4,2)$, with $h$ = 9, 8, 7, 6, 5, 4, 3, 2, 3. The state $(4,2)$ has walls above it, below it and to its left, and its last neighbor is in SEEN. The next layer is empty, and the search fails although a path exists.

**Width 2.** The beam holds the same states along the top row, plus a second state at each depth: $(0,1)$, $(1,1)$, $(2,1)$, $(2,2)$, $(1,2)$, $(1,3)$, $(1,4)$, $(2,4)$. When the top row is stuck at $(4,2)$, the second state goes on and reaches G with the path S, $(1,0)$, $(2,0)$, $(2,1)$, $(2,2)$, $(1,2)$, $(1,3)$, $(1,4)$, $(2,4)$, $(3,4)$, $(4,4)$, G of cost 11. It is a path, but not the cheapest one. At depth 3 the candidates $(3,0)$, $(2,1)$ and $(1,2)$ all have $h = 6$, and $(1,2)$, the state of the cheapest path, was generated last and dropped. The beam reaches $(1,2)$ again only at depth 5.

**Width 3.** The beam now keeps $(1,1)$ at depth 2 and $(1,2)$ at depth 3, and the search returns a path of cost 9. On this grid width 3 already gives the same answer as breadth-first search.

**The 8-puzzle.** The script draws 20 instances with `random.Random(2024)`: each one is the goal after 60 random moves, kept if a breadth-first search gives an optimal cost $d \ge 14$. The heuristic is the Manhattan distance.

| width | instances solved | mean cost divided by $d$ |
| --- | --- | --- |
| 1 | 7 of 20 | 3.155 |
| 10 | 20 of 20 | 1.258 |
| 100 | 20 of 20 | 1 |

With width 1, the search fails on 13 of the 20 instances: the single state runs out of new successors. These numbers are measured on these 20 instances only.

## Correctness

Beam search has no optimality theorem, but the [proof](proofs/correctness.md) shows two facts for any width, and completeness for no width limit.

- **A returned path is a real path to a goal.** Each candidate records its parent in the layer before, with the cost $g[n] + c$ of the action used, so following the parents from a goal gives a path from $s_0$ whose cost is the returned $g$. Line L7 returns only a goal.
- **It stops on a finite graph.** Each layer that line L8 builds is not empty only if it adds at least one new state to SEEN, so there are at most $N$ layers on a graph of $N$ states.

With no width limit, line L8 keeps every candidate, the layers are the layers of breadth-first search, and the search is complete. If each action costs 1, it also returns a cheapest path, since line L7 sees the goals of least depth first. With a finite width, neither claim holds, as the example shows.

## Complexity

Costs are in the [word RAM](/word-ram/), with each call of SUCCESSORS, IS-GOAL and $h$ counted as $O(1)$ and SEEN a [hash table](/hash-table/).

**Time.** A layer has at most $k$ states, so lines L5 and L6 look at most $k b$ pairs, and line L8 sorts at most $k b$ candidates in $O(k b \log(k b))$ time. Over $d$ layers that is $O(d\,k\,b \log(k b))$. A selection algorithm instead of a sort makes line L8 linear, $O(d\,k\,b)$ in all. The depth $d$ is at most the depth of the goal that is found, or at most the number of states on a failure.

**Space.** CAND holds $O(k b)$ entries. SEEN and the parent pointers hold $O(d k)$ states. A version that drops SEEN keeps only the current layer and its parents, $O(k b)$ plus the path, but then it can revisit states and go in circles on a graph with cycles.

The width sets a fixed cost per layer. This is why beam search is used when the graph is huge or infinite, as in speech recognition and in the decoding of sequence models, where a full search is out of the question.

## Properties

- **Not complete** for a finite width: it can fail when a path exists.
- **Not optimal**: the path it finds can cost more than the cheapest one.
- **Bounded work per layer**: at most $k b$ successors and $k$ kept states.
- **Tuned by the width**: larger widths failed less and found better paths on the inputs above, but this is not guaranteed for every input.
- **Deterministic**, with the tie rule of the code.

## Variants and improvements

- **Threshold beams.** Instead of a fixed count, keep each candidate whose score is within a margin of the best score of the layer. Speech recognizers often use this form or both forms. The thesis of Lowerre is the usual reference for this kind of pruning in Harpy. The exact rule that Harpy used is not given here.
- **Local beam search.** In [local search](/local-search/), keep $k$ states, generate all their successors, and keep the best $k$, with no paths and no SEEN. Russell and Norvig describe it next to hill climbing, and a stochastic form picks the $k$ states at random with a bias toward good ones.
- **Beam search in decoding.** For a [hidden Markov model](/hidden-markov-model/) or a neural sequence model, each layer is one more output symbol and the score is the log probability so far. A beam prunes the [Viterbi algorithm](/viterbi-algorithm/) or replaces it when the state space is too large.
- **Complete forms.** [Beam-stack search](/beam-stack-search/) remembers what each layer dropped and comes back to it, so it finds an optimal path. Restarting with a doubled width also makes beam search complete on a finite graph, at the cost of repeated work.
- **[Greedy best-first search](/greedy-best-first-search/)** keeps all candidates in one queue ordered by $h$. It does not drop states, so it is complete on finite graphs, but its memory is not bounded.

## When to use it

Use beam search when the graph is too large for a complete search, a good path soon matters more than the best path, and you can tune the width on typical inputs: decoding in speech recognition and machine translation, planning in large puzzles, and scheduling problems with deep search trees. Do not use it when you need a proof of optimality or a guarantee to find a path. Then use [A*](/a-star-search/) or, if memory is the limit, an algorithm from [memory-bounded heuristic search](/memory-bounded-heuristic-search/).

## Pitfalls

- **Reading failure as "no path".** With a finite width, failure says nothing about the graph. The example fails with width 1 on a grid that has a path.
- **Testing the goal after the pruning.** If line L7 runs after line L8, a goal can be dropped because its $g + h$ was not among the $k$ best.
- **Ranking by $h$ alone with general costs.** Then a cheap path can be dropped for an expensive one. Rank by $g + h$, or accept the loss on purpose.
- **Dropping SEEN on a graph with cycles.** The beam can fill up with states it has already visited and never get out.
- **Expecting better results from each larger width.** A larger width helps on most inputs but can give a worse path on some, because the beam sees different states.

## Implementations

## History

Beam search comes from speech recognition. Bruce Lowerre's thesis at Carnegie Mellon in 1976 described the Harpy system, which matched spoken input against a network of word pronunciations and, at each time step, kept only the partial matches that scored near the best one. Lowerre and Reddy presented Harpy at a meeting of the Acoustical Society of America the same year. The name "beam" spread from there to artificial intelligence, where it is taught as a memory-bounded form of best-first search, and later to the decoding of statistical and neural models of language. Zhou and Hansen added a stack of the pruned layers in 2005 to make it complete, as [beam-stack search](/beam-stack-search/).

## References
