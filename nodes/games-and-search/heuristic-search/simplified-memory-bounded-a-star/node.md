---
tag: S5JTNJ
kind: algorithm
slug: simplified-memory-bounded-a-star
name: Simplified memory-bounded A*
aliases:
- SMA*
area: games-and-search/heuristic-search
level: advanced
summary: A* with a fixed number M of stored nodes. When memory is full, it deletes the worst leaf and keeps its f in the parent. It returns the cheapest solution that fits in memory.
solves: [state-space-search]
model: word-ram
complexity:
  vars: {M: the number of nodes that memory can hold, b: the largest number of successors of a state}
  time: {per-step: O(M + b)}
  space: {extra: O(M b)}
properties: {deterministic: true, recursive: false}
history:
  year: 1992
  people: [Stuart Russell]
  note: Russell gave SMA* at ECAI 1992 as a simpler form of the MA* algorithm of Chakrabarti, Ghose, Acharya and De Sarkar.
prereqs: [a-star-search, memory-bounded-heuristic-search]
see_also: [recursive-best-first-search, iterative-deepening-a-star, fringe-search, admissible-heuristic, open-list, search-tree, depth-first-branch-and-bound, sliding-tile-puzzle]
sources:
  - paper: Stuart Russell, Efficient memory-bounded search methods, Proceedings of the 10th European Conference on Artificial Intelligence (ECAI-92)
    locator: pp. 1 to 5 (SMA*, the deletion of the worst leaf, the backed-up values, and its completeness and optimality when memory holds a solution path)
  - paper: P. P. Chakrabarti, S. Ghose, A. Acharya and S. C. De Sarkar, Heuristic search in restricted memory, Artificial Intelligence 41(2) (1989)
    locator: pp. 197 to 221 (MA*, the earlier memory-bounded A* that SMA* simplifies)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, 4th edition
    locator: Section 3.5.5 (SMA* as a memory-bounded search that forgets the worst leaf and backs up its value)
---

Simplified memory-bounded A* (SMA*) is [A*](/a-star-search/) for the case where memory holds only $M$ nodes. It runs like A* on the [search tree](/search-tree/): it takes the stored node of least $f = g + h$ and makes one more of its children. When memory is full, it first deletes the stored leaf of highest $f$ and writes that $f$ into the parent, so the parent knows how good the forgotten subtree was. When the alternatives get worse than that value, the search makes the forgotten child again. So SMA* uses all the memory it has, unlike [IDA*](/iterative-deepening-a-star/) and [RBFS](/recursive-best-first-search/), which use only a path. With an [admissible heuristic](/admissible-heuristic/), it returns the cheapest solution that has at most $M - 1$ actions, so it is optimal when an optimal path fits in memory. Russell gave it in 1992.

## In plain words

You plan a trip with a notebook that has a fixed number of pages. Each page holds one place you might visit. You always work on the place that looks best so far and add one of the next places on a new page.

When the notebook is full, you tear out the page of the place that looks worst. Before you throw it away, you write its score on the page of the place that led to it, so you still know that something down there was that good. If later the other places start to look worse than that score, you write the torn-out place again.

The longest route you can keep in mind has as many places as the notebook has pages. If the best route is short enough, you find it.

## The problem

The input is a [state-space search](/state-space-search/) problem: a start state $s_0$, a function SUCCESSORS that gives the finite list of pairs $(m, c)$ of a next state and the positive cost of the action to it, a goal test IS-GOAL, an admissible heuristic $h$, and a memory size $M \ge 2$, the largest number of nodes that may be stored at one time. The graph is finite. The output is a path from $s_0$ to a goal that is cheapest among the paths with at most $M - 1$ actions, or *failure* when no such path exists. A path of $M - 1$ actions has $M$ nodes, so a longer path cannot be stored in full.

## The algorithm

Each stored node $x$ has a value $f(x)$ and one *slot* for each successor of its state that is not on the path from the root to $x$. A slot is empty, holds a stored child, or holds the value of a forgotten child.

```pseudo id=main
SMA*(s0, SUCCESSORS, IS-GOAL, h, M)
L1  MEM ← {the root s0 with f = h(s0)}
L2  loop: Q ← the nodes of MEM that are goals or have a slot with no stored child; if Q is empty, return failure
L3      n ← the node of Q of least f, ties to the deepest, then the newest
L4      if f(n) = ∞ then return failure
L5      if IS-GOAL(n) then return the path from the root to n
L6      i ← the first empty slot of n, or else its forgotten slot of least value; floor ← max(f(n), that value)
L7      s ← the child of slot i, with f(s) ← ∞ if s is not a goal and has depth M − 1 or no slots, else max(floor, g(s) + h(s))
L8      if MEM has M nodes then
L9          z ← the leaf of MEM other than the root and n of highest f, ties to the shallowest, then the oldest
L10         delete z from MEM, and store f(z) as the value of the slot of z in its parent
L11     put s in slot i of n and in MEM
L12     BACKUP(n): while each slot of n is full or forgotten, raise f(n) to the least value of its slots, and go on to the parent
```

Line L7 is where the memory limit enters the values. A node at depth $M - 1$ that is not a goal cannot lie on a solution that fits in memory, since its child would be node $M + 1$ of the path. So it gets $f = \infty$, and the search does not go below it. The *floor* of line L6 keeps a remade child at least as high as the value it had when it was forgotten, so the search does not have to learn that value again.

Line L12 is the backup of A* on a tree. When every child of $n$ has been made at least once, the least value over its slots is a better lower bound than $f(n)$, and the change can go up to the root. This page keeps one value per forgotten slot, which needs $O(b)$ space per node and makes line L6 simple.

## Example

The graph is the one of the page [A* search](/a-star-search/): the undirected edges S-A 2, S-B 3, S-F 1, A-C 4, A-D 3, B-C 2, B-E 2, C-G 2 and D-G 3, the goal G, and $h$ the Manhattan distance to G, with the values 6, 4, 4, 2, 2, 6, 7, 0 on S, A, B, C, D, E, F, G. The neighbors are taken in alphabetical order. $C^* = 7$, by the path S-B-C-G of 3 actions.

**Memory 4.** The table gives each step: the node $n$, the child it makes and the $f$ of that child, and the leaf deleted to free memory.

| step | $n$ | child, $f$ | deleted leaf, $f$ | after the step |
| --- | --- | --- | --- | --- |
| 1 | S | A, 6 | none | |
| 2 | A | C, 8 | none | |
| 3 | A | D, 7 | none | A backs up to 7 |
| 4 | S | B, 7 | C, 8 | A stores 8 for C |
| 5 | S | F, ∞ | B, 7 | S stores 7 for B and backs up to 7 |
| 6 | D | G, 8 | F, ∞ | D and A back up to 8 |
| 7 | S | B, 7 | G, 8 | B is made again |
| 8 | B | C, 7 | D, 8 | A stores 8 for D |
| 9 | C | A, ∞ | A, 8 | the new A is at depth 3, not a goal |
| 10 | C | G, 7 | A, ∞ | |

At step 5, F has no successor other than S, so it gets $f = \infty$. At step 9, A is the child of C at depth $3 = M - 1$, so it also gets $\infty$. After step 10, the node of least $f$ is the goal G with $f = 7$, and SMA* returns S-B-C-G of cost 7. It made 10 children and deleted 7 nodes, against 5 expansions for A*.

**Other memory sizes.** Each goal path in this graph has at least 3 actions, so with $M = 2$ or $M = 3$ no solution fits, and SMA* returns failure. With more memory it deletes less:

| $M$ | result | children made | deletions |
| --- | --- | --- | --- |
| 2 | failure | 3 | 2 |
| 3 | failure | 7 | 5 |
| 4 | cost 7 | 10 | 7 |
| 5 | cost 7 | 9 | 5 |
| 6 | cost 7 | 9 | 4 |
| 8 | cost 7 | 9 | 2 |

**The 8-puzzle.** The script draws 20 instances with `random.Random(2024)`: each one is the goal after 60 random moves, kept if a breadth-first search gives an optimal cost $d \ge 14$. The heuristic is the Manhattan distance. With $M = d$ each run returns failure, and with $M = d + 1$ each run returns a path of cost $d$. Over the 20 instances, SMA* made 11,605 children with $M = d + 1$, 12,666 with $M = 2d$, and 7,888 with $M = 200$. A* expanded 3,411 states. On these instances, more memory did not always mean fewer steps, since the order of deletions changes with $M$. These numbers are measured on these instances only.

## Correctness

The [proof](proofs/correctness.md) shows, for positive costs, a finite graph and an admissible $h$:

- **Memory.** MEM never holds more than $M$ nodes, and line L9 always finds a leaf to delete.
- **Lower bounds.** Let $L(x)$ be the least cost of a goal path through the stored node $x$ with at most $M - 1$ actions. Every stored $f(x)$ is at most $L(x)$, and every value in a forgotten slot is at most the $L$ of the forgotten child.
- **The answer.** If SMA* returns a path, it is a real path to a goal with at most $M - 1$ actions, and it is cheapest among such paths. If it returns failure, no goal path has at most $M - 1$ actions.

The proof assumes that the search ends. Russell argued that it does on a finite graph. The proof on this site does not cover termination, and the implementation has a step limit as a guard.

## Complexity

Costs are in the [word RAM](/word-ram/), with each call of SUCCESSORS, IS-GOAL and $h$ counted as $O(1)$.

**Space.** SMA* stores at most $M$ nodes, and each node has at most $b$ slots, so it uses $O(M\,b)$ space. This is the point of the method: the memory is a parameter, not a result of the search.

**Time per step.** The implementation finds the node of least $f$ and the leaf of highest $f$ by linear scans, in $O(M)$ time, and makes the slots of a new child in $O(b)$ time, plus $O(M)$ to find the states on its path. Two priority queues, ordered by $f$ and depth, give $O(\log M)$ per step for the two choices.

**Number of steps.** There is no useful bound. When memory is small, SMA* can delete and remake the same nodes many times, and the number of steps can be much larger than the number of expansions of A*, as in the tables. When $M$ is so large that nothing is deleted, SMA* is A* on the search tree that makes one child per step.

## Properties

- **Optimal within memory**: it returns the cheapest solution with at most $M - 1$ actions, so it is optimal when an optimal path has at most $M - 1$ actions.
- **Uses all available memory**, unlike IDA* and RBFS.
- **Remakes** forgotten nodes, so it can take many more steps than A*.
- **Tree search**: it detects only the repeats of states on the current path.
- **Deterministic and not recursive.**

## Variants and improvements

- **MA*.** Chakrabarti, Ghose, Acharya and De Sarkar gave the first memory-bounded A* in 1989. SMA* keeps its idea of backed-up values and makes the rules for deletion simpler.
- **One value per node or per slot.** A version can keep only the least value of the forgotten children of a node, which saves space. The version on this page keeps one value per forgotten slot, which costs $O(b)$ per node and tells line L6 exactly which child to remake.
- **[RBFS](/recursive-best-first-search/)** uses the same backed-up values with only a path in memory.

## When to use it

Use SMA* when A* runs out of memory, the memory is known in advance, and the graph has short optimal paths compared to the memory, so that an optimal path fits. It is a good choice when memory is enough for most of the search but not for all of it, since then it deletes rarely. When memory is very small, it can spend most of its time on deletions and remakes, and IDA* with a consistent heuristic is often faster.

## Pitfalls

- **Deleting the node being expanded or the root.** Line L9 must leave out both, or the search loses its place.
- **Ties at line L3 and line L9.** When many leaves have the same $f$, a careless rule can pick the same node to expand and to delete. Russell and Norvig expand the newest best leaf and delete the oldest worst leaf. This page also breaks ties by depth in opposite directions.
- **Too little memory.** If $M - 1$ is below the number of actions of every solution, SMA* returns failure, though a goal can be reached. Choose $M$ larger than the expected solution length.
- **A solution that is not optimal.** When an optimal path is longer than $M - 1$ actions, SMA* returns the best path that fits, which can be worse than the optimum.
- **Counting the memory.** $M$ counts nodes. Each node also has $b$ slots, so the bytes needed grow with $M\,b$.

## Implementations

## History

Chakrabarti, Ghose, Acharya and De Sarkar presented MA* in 1989, a version of A* with a fixed limit on memory that backs up the values of the nodes it prunes. Russell gave SMA* at ECAI 1992, with simpler rules: expand the best leaf, delete the worst one, and keep its value in the parent. He showed that it is complete when the memory can hold a shallowest solution path and optimal when it can hold an optimal one. Russell and Norvig made it, next to IDA* and RBFS, the standard textbook example of a search that works with any amount of memory.

## References
