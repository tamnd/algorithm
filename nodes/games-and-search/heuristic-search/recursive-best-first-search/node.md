---
tag: TDF1Y3
kind: algorithm
slug: recursive-best-first-search
name: Recursive best-first search
aliases:
- RBFS
area: games-and-search/heuristic-search
level: advanced
summary: A recursive best-first search in linear space. It explores the best child under a bound set by the best alternative, and on return it stores the best f found below that child.
solves: [state-space-search]
model: word-ram
complexity:
  vars: {b: the largest number of successors of a state, d: the largest number of actions on a path that the search follows}
  time: {per-expansion: O(b log b)}
  space: {extra: O(b d)}
properties: {deterministic: true, recursive: true}
history:
  year: 1993
  people: [Richard E. Korf]
  note: Korf introduced RBFS in a 1993 paper on linear-space best-first search, together with the simpler SRBFS.
prereqs: [iterative-deepening-a-star, best-first-search]
see_also: [a-star-search, simplified-memory-bounded-a-star, memory-bounded-heuristic-search, fringe-search, depth-first-branch-and-bound, admissible-heuristic, consistent-heuristic, sliding-tile-puzzle]
sources:
  - paper: doi:10.1016/0004-3702(93)90045-D
    title: Richard E. Korf, Linear-space best-first search, Artificial Intelligence 62(1) (1993)
    locator: pp. 41 to 78 (SRBFS and RBFS, the inheritance of stored values, best-first order for monotone and nonmonotone cost functions, and the optimality with an admissible heuristic)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, 4th edition
    locator: Section 3.5.5 (recursive best-first search, its pseudocode and its regeneration of forgotten subtrees)
---

Recursive best-first search (RBFS) imitates [A*](/a-star-search/) with memory linear in the depth. It is a recursive search on the tree of paths, like [IDA*](/iterative-deepening-a-star/), but it does not use one global threshold. At a node $n$, it keeps a stored value $F$ for each child, explores the child of least $F$, and gives that call a bound: the least $F$ of the other children, or the bound of $n$ if that is smaller. When the call finds that every path below its child exceeds the bound, it returns, and the child's stored value becomes the least $f$ it saw at the edge of its subtree. So RBFS forgets a subtree but remembers how good it was, and comes back to it when the alternatives get worse. With an [admissible heuristic](/admissible-heuristic/), it returns a cheapest path. Korf introduced it in 1993.

## In plain words

You explore a cave with branching tunnels, and you can only remember the tunnels on your way back to the entrance. At each fork, you take the tunnel that looks best. You also keep in mind how good the second-best tunnel at that fork looked.

As you go deeper, the tunnel can start to look worse. Once it looks worse than that second-best tunnel, you go back to the fork. You forget the details of what you saw, but you write one number on the wall: how good the best spot down there looked. Then you try the other tunnel. If it also gets worse than that number, you come back and go down the first tunnel again.

## The problem

The input is a [state-space search](/state-space-search/) problem: a start state $s_0$, a function SUCCESSORS that gives the finite list of pairs $(m, c)$ of a next state and the positive cost of the action to it, a goal test IS-GOAL, and an admissible heuristic $h$. The graph is finite. The output is a cheapest path from $s_0$ to a goal state, or *failure* when no goal can be reached.

## The algorithm

```pseudo id=main
RBFS-SEARCH(s0, SUCCESSORS, IS-GOAL, h)
L1  RBFS(s0, 0, h(s0), ∞)
L2  return the recorded path, or failure if none was recorded

RBFS(n, g, F, B)                              ▷ F is the stored value of n, B its bound
L3  if f(n) = g + h(n) > B then return f(n)
L4  if IS-GOAL(n) then record PATH + n and stop the whole search
L5  KIDS ← the pairs (m, c) of SUCCESSORS(n) with m not on PATH, each with g(m) = g + c
L6  if KIDS is empty then return ∞
L7  for each child m: if f(n) < F then F[m] ← max(F, f(m)) else F[m] ← f(m)
L8  while the least stored value F[m1] ≤ B and F[m1] < ∞ do
L9      F2 ← the second least stored value, or ∞ if n has one child
L10     F[m1] ← RBFS(m1, g(m1), F[m1], min(B, F2))
L11 return the least stored value F[m1]
```

The stored value $F$ of a node is its $f$ the first time the search sees it, and the value backed up from below after the search has explored it. Line L7 is the trick that makes RBFS more than a simple recursion. If $f(n) < F$, the node $n$ was explored before, and the search then saw nothing below it with a value less than $F$. So its children inherit $F$ as a lower bound, which saves a slow climb back up to the old value. Without line L7, the simpler version SRBFS still works, but it expands new nodes in best-first order only when $f$ never falls along a path.

PATH is the current path, kept next to the recursion with a hash set. Line L5 skips the states that are on it, so the search runs on the finite tree of simple paths. Ties at lines L8 and L9 go to the child generated first.

## Example

The graph is the one of the page [A* search](/a-star-search/): the undirected edges S-A 2, S-B 3, S-F 1, A-C 4, A-D 3, B-C 2, B-E 2, C-G 2 and D-G 3, the goal G, and $h$ the Manhattan distance to G, with the values 6, 4, 4, 2, 2, 6, 7, 0 on S, A, B, C, D, E, F, G. The neighbors are generated in alphabetical order. $C^* = 7$.

1. RBFS(S, 0, 6, ∞) expands S. The children get A 6, B 7 and F 8. The best is A, and the second best is 7, so the call on A gets the bound 7.
2. RBFS(A, 2, 6, 7) expands A. The children get C $6 + 2 = 8$ and D $5 + 2 = 7$. The call on D gets the bound $\min(7, 8) = 7$.
3. RBFS(D, 5, 7, 7) expands D. Its only child not on the path is G, with $f = 8 + 0 = 8 > 7$, so the loop does not run and D returns 8.
4. Back at A, D now stores 8 and C stores 8. Both exceed the bound 7, so A returns 8.
5. Back at S, A now stores 8. The best child is B with 7, and the second best is 8, so the call on B gets the bound 8. RBFS(B, 3, 7, 8) expands B, with the children C $5 + 2 = 7$ and E $5 + 6 = 11$. C gets the bound $\min(8, 11) = 8$.
6. RBFS(C, 5, 7, 8) expands C, with the children A $9 + 4 = 13$ and G $7 + 0 = 7$. The call on G has $f = 7 \le 8$, and G is a goal. RBFS returns S-B-C-G of cost 7.

| expansion | path | $f$ |
| --- | --- | --- |
| 1 | S | 6 |
| 2 | S, A | 6 |
| 3 | S, A, D | 7 |
| 4 | S, B | 7 |
| 5 | S, B, C | 7 |

These are the same 5 expansions as those of A*, in the same order. A* keeps all of them in memory. RBFS kept at most three levels of stored values, and the subtree below A was reduced to the single number 8 when the search left it.

**The 8-puzzle.** The script draws 20 instances with `random.Random(2024)`: each one is the goal after 60 random moves, kept if a breadth-first search gives an optimal cost $d \ge 14$. The heuristic is the Manhattan distance. Over the 20 instances, A* expanded 3,411 states, IDA* 8,229 and RBFS 7,494. Both linear-space methods regenerate forgotten subtrees, and here RBFS did a little better than IDA*. These numbers are measured on these instances only.

## Correctness

The [proof](proofs/correctness.md) shows, for positive costs, a finite graph and an admissible $h$:

- **Stored values are lower bounds.** Let $c^*(m)$ be the least cost of a goal path that extends the current path through $m$. Then every stored value $F[m]$ satisfies $F[m] \le c^*(m)$. Line L7 keeps this, because $F \le c^*(n) \le c^*(m)$ for each child $m$ of $n$, and a returned value is at most the $c^*$ of its node.
- **Termination.** Each pass of the loop at line L8 strictly raises one stored value, and the values come from a finite set, so each call ends.
- **Completeness.** A child with a goal path below it has a finite stored value, so the top call cannot end without finding a goal when one is reachable.
- **Optimality.** At each level of the recursion, a child on an optimal path that is not the one explored caps the bound at $C^*$. So the goal that line L4 accepts has $g = f \le C^*$.

Korf also proved that RBFS expands nodes for the first time in best-first order, also when $f$ is not monotone. The proof on this site covers optimality, not that claim.

## Complexity

Costs are in the [word RAM](/word-ram/), with each call of SUCCESSORS, IS-GOAL and $h$ counted as $O(1)$.

**Space.** Each level of the recursion keeps the stored values of the children of one node of PATH, so RBFS keeps $O(b\,d)$ values for paths of at most $d$ actions. This is the main point of the method.

**Time.** An expansion generates at most $b$ children and keeps them sorted by stored value, in $O(b \log b)$ time, or $O(b)$ per pass with a linear scan for the two least values. The number of expansions has no useful bound in terms of the expansions of A*. Each time the search leaves a subtree and comes back, it expands the nodes of that subtree again. When the stored values change by small steps, as with many distinct costs, RBFS can switch between two subtrees many times, like the many iterations of IDA* in the same case. Like IDA*, it does not detect duplicates that are not on the current path, so on graphs with many paths to each state it can be far slower than A*.

## Properties

- **Optimal** with an admissible heuristic, and **complete** on finite graphs.
- **Linear space**: $O(b\,d)$ stored values.
- **Best-first order** of new expansions, by Korf's theorem: the nodes of the tree of paths are expanded for the first time in order of their values, as a best-first search on that tree would expand them.
- **Regenerates** forgotten subtrees, and uses no extra memory to avoid it.
- **No duplicate detection** beyond the current path.
- **Deterministic and recursive.**

## Variants and improvements

- **SRBFS.** The simple version without the inheritance of line L7. It is correct, but with a nonmonotone $f$ it explores new nodes out of best-first order.
- **[SMA*](/simplified-memory-bounded-a-star/) and MA*.** These use all the memory that is available, not only a path, and so regenerate less. They keep backed-up values in the same way when they forget a subtree.
- **[IDA*](/iterative-deepening-a-star/).** Simpler, with one global threshold. With a consistent heuristic, it often expands about as many nodes as RBFS and costs less per node, since it keeps no stored values.
- **[Fringe search](/fringe-search/).** Keeps the frontier between thresholds, which uses more memory and saves the restarts.

## When to use it

Use RBFS when memory is very limited, an optimal path is needed, and the heuristic is not consistent, or when the order in which nodes are first expanded matters, as it does for a search that should spend its time on the most promising nodes first. In most puzzle searches with a consistent heuristic, IDA* is simpler and about as fast. If more memory is available, a method that uses it, such as SMA* or plain A*, regenerates less.

## Pitfalls

- **Forgetting line L7.** Then the search is SRBFS, which is correct but slower with a nonmonotone $f$.
- **Taking the second least value of the wrong set.** The bound at line L10 uses the second least stored value among the children of $n$, after each update, and must be capped by $B$.
- **Ending the loop at ∞.** If all children store ∞, there is no goal below $n$, and the loop must end even when $B = \infty$, as at the top call. Otherwise the search never stops.
- **Testing the goal before the bound.** As in IDA*, line L4 must come after line L3, or RBFS can return a goal with $f$ above its bound, which need not be optimal.
- **Deep recursion.** The recursion depth is the length of PATH. The implementation in Python is for paths well under the limit of about 1,000 frames.

## Implementations

## History

Korf published RBFS in 1993, in a paper on best-first search in linear space. He first gave SRBFS, which explores the best child with the second-best value as a bound, and then RBFS, which also passes stored values down to the children of a node it has explored before. He proved that RBFS expands new nodes in best-first order for any cost function and that it finds optimal solutions with an admissible heuristic, and compared it with IDA* on sliding-tile puzzles. Russell and Norvig made it the standard textbook example of a recursive memory-bounded search, next to IDA* and SMA*.

## References
