---
tag: JA3VM9
kind: algorithm
slug: partial-expansion-a-star
name: Partial expansion A*
aliases:
- PEA*
area: games-and-search/heuristic-search
level: research
summary: A* that stores only the children of a node with f at most its stored value F plus a cutoff C, and puts the node back in OPEN with F set to the least f it left out. It stores fewer nodes for a large b.
solves: [state-space-search]
model: word-ram
complexity:
  vars: {n: the number of states that get a value g, b: the largest number of successors of a state}
  time: {consistent: O(n b^2 + n b log n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
history:
  year: 2000
  people: [Takayuki Yoshizumi, Teruhisa Miura, Toru Ishida]
  note: Yoshizumi, Miura and Ishida introduced PEA* at AAAI 2000 for search problems with a large branching factor, such as multiple sequence alignment.
prereqs: [a-star-search, open-list]
see_also: [multiple-sequence-alignment, memory-bounded-heuristic-search, iterative-deepening-a-star, fringe-search, duplicate-detection, consistent-heuristic, branching-factor, multi-agent-pathfinding]
sources:
  - paper: Takayuki Yoshizumi, Teruhisa Miura and Toru Ishida, A* with partial expansion for large branching factor problems, Proceedings of the 17th National Conference on Artificial Intelligence (AAAI-2000)
    locator: pp. 923 to 929 (partial expansion with a cutoff value C, the stored value F of a node, its optimality, and the experiments on multiple sequence alignment)
  - paper: doi:10.1613/jair.4171
    title: Meir Goldenberg, Ariel Felner, Roni Stern, Guni Sharon, Nathan Sturtevant, Robert C. Holte and Jonathan Schaeffer, Enhanced partial expansion A*, Journal of Artificial Intelligence Research 50 (2014)
    locator: pp. 141 to 187 (PEA* and EPEA*, operator selection functions that generate only the children of a given f, and the experiments on puzzles and multi-agent path finding)
---

Partial expansion A* (PEA*) is [A*](/a-star-search/) for problems where each state has many successors, most of them with a high $f = g + h$. A* puts all the children of an expanded state in its [open list](/open-list/), even those with $f$ above the optimal cost $C^*$. It never expands them, but it stores them, and in a problem such as [multiple sequence alignment](/multiple-sequence-alignment/) these *surplus* nodes fill most of the memory. PEA* gives each state in OPEN a stored value $F$, which starts at its $f$. When it expands a state $n$, it generates all its children but stores only those with $f \le F(n) + C$, for a cutoff $C \ge 0$. If it left some child out, it puts $n$ back in OPEN with $F(n)$ raised to the least $f$ that it left out, so that $n$ is expanded again when that value is reached. With an [admissible heuristic](/admissible-heuristic/), PEA* still returns a cheapest path. With $C = 0$, it stores no child with $f > C^*$. Yoshizumi, Miura and Ishida introduced it in 2000.

## In plain words

A* is like a manager who, for each task, writes every possible next step on a board, also the ones that are clearly bad. The board fills up with steps that will never be done.

PEA* writes only the good next steps on the board, the ones that look as good as the task itself. For the rest, it writes one note on the task: how good the best step left out looked. The task stays on the board with that note. When the work on the board reaches that level, the task comes up again, and the next group of steps goes on the board.

The board stays much smaller. The price is that the same task is looked at several times.

## The problem

The input is a [state-space search](/state-space-search/) problem: a start state $s_0$, a function SUCCESSORS that gives the finite list of pairs $(m, c)$ of a next state and the positive cost of the action to it, a goal test IS-GOAL, an admissible heuristic $h$, and a cutoff $C \ge 0$. The output is a cheapest path from $s_0$ to a goal state, or *failure* when no goal can be reached. The proof of failure needs a finite graph.

## The algorithm

```pseudo id=main
PEA*(s0, SUCCESSORS, IS-GOAL, h, C)
L1  g[s0] ← 0; F[s0] ← h(s0)
L2  OPEN ← {s0}, a priority queue by F, ties to the larger g
L3  while OPEN is not empty do
L4      n ← the state of least F in OPEN; take it out of OPEN
L5      if IS-GOAL(n) then return the path to n by the parents
L6      REST ← ∞
L7      for each pair (m, c) of SUCCESSORS(n) do
L8          f(m) ← g[n] + c + h(m)
L9          if f(m) > F[n] + C then REST ← min(REST, f(m)) and skip m
L10         if m has no value g or g[n] + c < g[m] then
L11             g[m] ← g[n] + c; parent[m] ← n; F[m] ← f(m); put m in OPEN
L12     if REST < ∞ then F[n] ← REST and put n back in OPEN       ▷ else n is closed
L13 return failure
```

The value $F(n)$ is a lower bound on the $f$ of the children of $n$ that are not stored yet. Line L9 leaves out the children above $F(n) + C$, and line L12 records the least of them. When $n$ comes out of OPEN again, it generates all its children again, and line L10 skips the ones that are already stored with the same $g$. A state that gets a cheaper $g$ at line L11 starts again with $F = f$, so all its children are tried again with the new $g$.

With $C = \infty$, line L9 never skips a child, line L12 never puts $n$ back, and PEA* is A*. With $C = 0$, each expansion stores only the children with $f = F(n)$, or less if $h$ is not consistent. The cutoff trades memory for time: a small $C$ stores fewer nodes and expands each state more times.

## Example

The graph is the one of the page [A* search](/a-star-search/): the undirected edges S-A 2, S-B 3, S-F 1, A-C 4, A-D 3, B-C 2, B-E 2, C-G 2 and D-G 3, the goal G, and $h$ the Manhattan distance to G, with the values 6, 4, 4, 2, 2, 6, 7, 0 on S, A, B, C, D, E, F, G. The neighbors are taken in alphabetical order. $C^* = 7$.

With $C = 0$:

| step | $n$, $F(n)$ | children and their $f$ | stored | $n$ goes back with |
| --- | --- | --- | --- | --- |
| 1 | S, 6 | A 6, B 7, F 8 | A | $F = 7$ |
| 2 | A, 6 | C 8, D 7, S 10 | none | $F = 7$ |
| 3 | A, 7 | C 8, D 7, S 10 | D | $F = 8$ |
| 4 | D, 7 | A 12, G 8 | none | $F = 8$ |
| 5 | S, 7 | A 6, B 7, F 8 | B | $F = 8$ |
| 6 | B, 7 | C 7, E 11, S 12 | C | $F = 11$ |
| 7 | C, 7 | A 13, B 11, G 7 | G | $F = 11$ |

At step 5, A has $f = 6 \le 7$ but is already stored with the same $g$, so line L10 skips it. Then G comes out of OPEN with $F = 7$, and PEA* returns S-B-C-G of cost 7. At step 2, A is put back with $F = 7$ and S also has $F = 7$, and the tie goes to A, which has the larger $g$.

| search | expansions | children generated | states put in OPEN | largest $f$ put in OPEN |
| --- | --- | --- | --- | --- |
| PEA*, $C = 0$ | 7 | 20 | 6 | 7 |
| PEA*, $C = 1$ | 5 | 14 | 7 | 8 |
| A*, that is $C = \infty$ | 5 | 14 | 10 | 11 |

The counts of states put in OPEN include $s_0$. A* stores the surplus states F with $f = 8$, C with $f = 8$ by way of A, G with $f = 8$ by way of D, and E with $f = 11$. PEA* with $C = 0$ stores none of them, at the cost of 2 more expansions and 6 more children generated.

**The 8-puzzle.** The script draws 20 instances with `random.Random(2024)`: each one is the goal after 60 random moves, kept if a breadth-first search gives an optimal cost $d \ge 14$. The heuristic is the Manhattan distance. Over the 20 instances, A* put 5,633 states in OPEN and made 3,411 expansions. PEA* with $C = 0$ put 3,448 states in OPEN and made 4,500 expansions. The 8-puzzle has at most 4 successors per state, so the saving is small. It grows with the branching factor. These numbers are measured on these instances only.

## Correctness

The [proof](proofs/correctness.md) shows, for positive costs and an admissible $h$:

- **A good state in OPEN.** Until the search returns, OPEN holds a state $q$ on a cheapest path to a goal with its least $g$ and $F(q) \le C^*$. The key point is that each value $F(q)$ that line L12 sets is the $f$ of a child that was left out, and the next state on the cheapest path is such a child.
- **Optimality.** The goal that line L5 returns has $g = F \le C^*$, so the path costs $C^*$.
- **No surplus nodes.** Each child stored at line L11 has $f \le F(n) + C \le C^* + C$. With $C = 0$, no state with $f > C^*$ is ever put in OPEN.
- **Termination.** On a finite graph, the search ends, and it returns failure only when no goal can be reached.

## Complexity

Costs are in the [word RAM](/word-ram/), with each call of SUCCESSORS, IS-GOAL and $h$ and each operation of the hash table counted as $O(1)$.

**Space.** PEA* stores $O(n)$ states, as A* does, but $n$ is smaller. With $C = 0$, every stored state has $f \le C^*$, while A* also stores the children of high $f$ of every state it expands. When the [branching factor](/branching-factor/) $b$ is large and most children have a high $f$, these children are most of the memory of A*.

**Time.** Each expansion generates all $b$ children, and a state can be expanded once for each distinct value of $f$ among its children, so up to $b + 1$ times. With a consistent heuristic, each state is expanded with its least $g$ only, so there are $O(n\,b)$ expansions of $O(b)$ work each, plus $O(\log n)$ per operation on OPEN: $O(n\,b^2 + n\,b \log n)$ in all. The extra expansions make PEA* slower than A* when memory is not the limit.

## Properties

- **Optimal** with an admissible heuristic, and **complete** on finite graphs.
- **No surplus nodes** with $C = 0$: nothing with $f > C^*$ is stored.
- **Same cost as A*** for every cutoff, and the same search as A* for $C = \infty$.
- **Generates children again**: each expansion of a state generates all its children, so the time per state grows.
- **Deterministic and not recursive.**

## Variants and improvements

- **Enhanced partial expansion A* (EPEA*).** Felner and others proposed it in 2012, and Goldenberg and others gave the full version in 2014. For many domains, it is possible to know in advance which actions change $f$ by how much, with an *operator selection function*. EPEA* then generates only the children with $f = F(n)$, and gets the saving in memory without the cost of generating the other children. It is used in [multi-agent path finding](/multi-agent-pathfinding/), where the branching factor grows exponentially with the number of agents.
- **The cutoff $C$.** A value of $C$ between 0 and $\infty$ trades memory for time, as the table of the example shows.
- **Memory-bounded searches.** [IDA*](/iterative-deepening-a-star/) and [fringe search](/fringe-search/) save memory in other ways. PEA* keeps the duplicate detection of A*, which matters in graphs with many paths to each state.

## When to use it

Use PEA* when A* runs out of memory because of surplus nodes, that is, when each state has many successors and most have $f$ well above $C^*$, as in multiple sequence alignment of several sequences, or in path finding for many agents at once. If you can tell in advance which successors have which $f$, use EPEA* instead, since then the extra generations disappear. If the branching factor is small, as in the 8-puzzle, the saving is small and plain A* is faster.

## Pitfalls

- **Not resetting $F$ when $g$ falls.** A state that gets a cheaper $g$ must start again with $F = f$. If it keeps its raised $F$, children that are now cheaper may never be stored.
- **Storing a child twice.** Each expansion generates all children again. Line L10 must skip the ones that are already stored with a $g$ at most the new one.
- **Closing a state too soon.** A state is closed only when no child was left out at line L9. If it is closed after its first expansion, the children above $F(n) + C$ are lost and the search is not optimal.
- **Expecting a speedup.** PEA* saves memory, not time. Without an operator selection function, each expansion still generates all $b$ children, and some states are expanded many times.

## Implementations

## History

Yoshizumi, Miura and Ishida presented PEA* at AAAI 2000. They studied multiple sequence alignment, where the number of successors of a state grows exponentially with the number of sequences, and found that most of the memory of A* went to nodes it never expanded. Partial expansion with a cutoff removed most of them. In 2012, Felner and others showed at AAAI that in many domains an operator selection function can generate only the children of the right $f$, which gave EPEA*, and the journal version followed in 2014 in the Journal of Artificial Intelligence Research, with experiments on puzzles and multi-agent path finding.

## References
