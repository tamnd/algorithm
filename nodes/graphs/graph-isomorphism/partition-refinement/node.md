---
tag: X7W7BR
kind: technique
slug: partition-refinement
name: Partition refinement
aliases:
- colour refinement
- equitable refinement
- coarsest partition refinement
area: graphs/graph-isomorphism
level: core
summary: Repeatedly split cells of a vertex partition by counts of neighbors in a splitter cell until stable; with the rule "skip the largest piece" it runs in O((n + m) log n) time.
prereqs: [equitable-partition, equivalence-relation]
see_also: [weisfeiler-leman, hopcroft-minimization, dfa-minimization, lexicographic-bfs, individualization-refinement, nauty, equitable-partition]
sources:
  - paper: doi:10.1137/0216062
    title: Robert Paige and Robert E. Tarjan, Three partition refinement algorithms, SIAM Journal on Computing 16(6), 973 to 989 (1987)
    locator: the whole paper (relational coarsest partition, the size-based splitting rule, and lexicographic sorting of strings)
  - paper: doi:10.1016/0304-3975(82)90016-0
    title: A. Cardon and M. Crochemore, Partitioning a graph in O(|A| log2 |V|), Theoretical Computer Science 19(1), 85 to 98 (1982)
    locator: the whole paper (coarsest equitable partition by refinement with the smaller pieces)
  - paper: "John E. Hopcroft, An n log n algorithm for minimizing states in a finite automaton, in Theory of Machines and Computations, Academic Press, 1971, 189 to 196"
    locator: the whole paper (the rule of processing all pieces but the largest)
  - paper: doi:10.1007/s00224-016-9686-0
    title: Christoph Berkholz, Paul Bonsma and Martin Grohe, Tight lower and upper bounds for the complexity of canonical colour refinement, Theory of Computing Systems 60(4), 581 to 614 (2017)
    locator: Sections 3 and 4 (the O((n + m) log n) algorithm and the lower bound)
---

Partition refinement is the technique of keeping a partition of a finite set and splitting its cells, again and again, by information that a chosen cell, the splitter, gives about the other elements, until no splitter changes anything. In graph isomorphism the information is the number of neighbors in the splitter, and the result is the coarsest [equitable partition](/equitable-partition/), which [color refinement](/weisfeiler-leman/) computes. The same template minimizes finite automata, computes bisimulation, and orders vertices in [lexicographic BFS](/lexicographic-bfs/). Hopcroft's rule, to skip the largest piece of each split cell as a future splitter, gives $O((n + m) \log n)$ time.

## In plain words

Start with all points in one group, or in groups given by their colors. Pick a group and use it as a test: count, for every point, how many links it has into the test group. If two points in the same group get different counts, cut their group into pieces by count. Every piece that a cut creates may be a useful test later, so put it on a list of tests to run. Keep testing until the list is empty. Then no group can be cut any more. A cut is never undone, so the groups only get smaller, and the work stops. A trick makes it fast: after a cut, you need not add the biggest piece to the list.

## When it applies

The technique fits when the answer is the coarsest partition with a stability property of the form "all elements of a cell behave the same way towards every cell", and when:

- the property is preserved under refinement in the right direction, so that splitting never needs to be undone;
- each splitting step uses only local information, such as the edges into one cell;
- the initial partition is given, for example by vertex colors, by accepting and rejecting states, or by labels.

It does not apply when cells must merge again, or when the stability test involves all cells at once in a way that a single splitter cannot express.

## The template

Input: a graph $G = (V, E)$ with $n$ vertices and $m$ edges, possibly directed, and an initial partition $\pi_0$ of $V$, for example by vertex colors. Output: the coarsest equitable partition that refines $\pi_0$. For directed graphs run the counting step with in-neighbors and with out-neighbors.

```pseudo id=main
REFINE(G, π0)
L1  π ← π0;  S ← a queue holding every cell of π0
L2  while S is not empty do
L3      X ← remove a cell from S
L4      for each vertex v with a neighbor in X: count(v) ← |N(v) ∩ X|
L5      for each cell Y of π that contains a vertex with count > 0 do
L6          split Y into the pieces Y1, ..., Yt of equal count (vertices not touched have count 0)
L7          if t > 1 and Y is in S then replace Y in S by Y1, ..., Yt
L8          else if t > 1 then add to S every piece except one of largest size
L9  return π
```

*Why skipping the largest piece is safe.* When $Y$ splits into $Y_1, \ldots, Y_t$ and $Y$ has already served as a splitter, every vertex $v$ has $|N(v) \cap Y_t| = |N(v) \cap Y| - \sum_{j < t} |N(v) \cap Y_j|$. So once the cells are stable with respect to $Y$ and to $Y_1, \ldots, Y_{t-1}$, they are stable with respect to $Y_t$ as well.

*Why it is fast.* A vertex enters $S$ in a cell at most half the size of its previous splitter cell, except when it stays in a queued cell, so each vertex is in at most $O(\log n)$ splitters. Processing splitter $X$ costs $O(\sum_{x \in X} \deg x)$ with bucket arrays, so the total is $O((n + m) \log n)$. Berkholz, Bonsma and Grohe (2017) showed that no algorithm of this splitting kind does better on all graphs.

*Small run.* For the path $0 - 1 - 2 - 3$ and $\pi_0 = \{V\}$: the splitter $V$ gives counts $1, 2, 2, 1$, so $V$ splits into $\{0, 3\}$ and $\{1, 2\}$, and only $\{0, 3\}$ joins $S$ (both pieces have size 2; one is skipped). The splitter $\{0, 3\}$ gives counts $0, 1, 1, 0$, which split neither cell. $S$ is empty, and $\{0, 3\}, \{1, 2\}$ is the coarsest equitable partition.

## Classic examples

- **[Color refinement](/weisfeiler-leman/).** The template with $N(v)$ the neighbors in an undirected graph, from Cardon and Crochemore (1982). [nauty](/nauty/), Traces and [bliss](/bliss/) run it at every node of their search trees.
- **[DFA minimization](/dfa-minimization/).** [Hopcroft's algorithm](/hopcroft-minimization/) starts from accepting and rejecting states and splits by "has a transition on letter $a$ into $X$". The stable partition gives the minimal automaton in $O(k n \log n)$ time for $k$ letters. The "all but the largest" rule comes from this algorithm (1971).
- **Relational coarsest partition and bisimulation.** Paige and Tarjan (1987) split by "has some edge into $X$" instead of a count, with a three-way split on $X$ and $B \setminus X$, in $O(m \log n)$ time. This decides strong bisimulation of labeled transition systems.
- **[Lexicographic BFS](/lexicographic-bfs/).** The partition is an ordered sequence of cells; visiting a vertex splits each cell into neighbors and non-neighbors, placing the neighbors first. This gives linear-time recognition of chordal graphs.
- **Sorting strings.** Paige and Tarjan also cast [lexicographic sorting of strings](/string-sorting/) as partition refinement.
- **Modular decomposition and transitive orientation**, by refining with neighborhoods of chosen vertices (Habib, Paul and Viennot survey these uses).

## Variations

- **Ordered partitions.** Keep cells in a sequence and place pieces in a fixed order, for example by count. Then the result is canonical: isomorphic inputs give the same sequence of cell sizes. Individualization-refinement needs this.
- **Count splitting versus existence splitting.** Count splitting gives equitable partitions; existence splitting (edge into $X$ or not) gives bisimulation classes and suffices for Hopcroft's automaton minimization, where each state has exactly one transition per letter.
- **Weighted and labeled edges.** Split by the sum of weights or the multiset of labels into $X$. This gives lumping of Markov chains.
- **Naive round-based refinement.** Recompute all signatures in each round, as in the [WL page](/weisfeiler-leman/). It is simpler and parallel, but takes $O(n (n + m) \log n)$ time in the worst case.
- **Higher dimensions.** [$k$-dimensional Weisfeiler-Leman](/k-dimensional-weisfeiler-leman/) refines a partition of $k$-tuples instead of vertices.

## Pitfalls

- **Skipping a piece of a cell that is still in the queue.** Rule L7 must replace a queued cell by all its pieces. Skipping the largest piece of a queued cell loses information, since that cell never served as a splitter.
- **Using the wrong count after a split.** Compute all counts for splitter $X$ before splitting any cell, or a split of $X$ itself during the pass changes the counts.
- **Resetting counts in $O(n)$ per splitter.** Clearing a full array for each splitter costs $O(n)$ per step and $O(n^2)$ in total. Reset only the entries that the pass touched.
- **Non-canonical order of pieces.** For isomorphism testing on two graphs separately, pieces must be ordered by a rule that does not depend on vertex names, for example by count. Otherwise cell numbers mean different things in the two runs.
- **Expecting orbits.** The coarsest equitable partition can be coarser than the orbit partition of the automorphism group; on a regular graph it is a single cell.

## Exercises

1. Run the template on the star $K_{1,3}$ with $\pi_0 = \{V\}$. Which cells result, and which splitter is skipped?
2. Show that the coarsest equitable partition of a vertex-transitive graph is $\{V\}$, and give a regular graph that is not vertex-transitive with the same result.
3. Change line L4 to record only whether $v$ has a neighbor in $X$. Show that the result is then coarser in general, and give a graph where it differs from the equitable partition.

## References
