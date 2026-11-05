---
tag: W41CXA
kind: concept
slug: implicit-graph
name: Implicit graph
aliases:
- Implicit vs explicit graphs
area: graphs/graph-representation
level: core
summary: A graph whose edges are not stored but computed on demand from a rule, such as the moves of a puzzle.
prereqs: [graph, adjacency-list]
see_also: [state-space-search, breadth-first-search, a-star-search, iterative-deepening-a-star, bidirectional-search, sliding-tile-puzzle, functional-graph, adjacency-query]
sources:
  - book: isbn:9783540779773
    title: Kurt Mehlhorn and Peter Sanders, Algorithms and Data Structures, The Basic Toolbox, Springer, 2008
    locator: Section 8.5 (Implicit representations), graphs given by a rule such as grid graphs and interval graphs, with the comparison to the explicit representations of Sections 8.1 to 8.4
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 3 (Solving problems by searching), Sections 3.1 to 3.4, the state space given by an initial state, actions and a transition model, and the space cost of uninformed search
  - paper: doi:10.1137/0405049
    title: Sampath Kannan, Moni Naor and Steven Rudich, Implicit representation of graphs, SIAM Journal on Discrete Mathematics 5(4), 1992
    locator: pages 596 to 603, the definition of an implicit representation by labels of O(log n) bits and the counting argument for which graph classes have one
---

An implicit graph is a [graph](/graph/) that is not stored as a list of [edges](/edge/) but given by a rule: a way to name the vertices and a procedure that, for a vertex $v$, computes its neighbours or tests whether two vertices are adjacent. The graph of the positions of a puzzle, with an edge for each legal move, is the typical case. An implicit graph costs no memory for its edges and can have far more vertices than any computer stores, so algorithms on it are measured by the vertices they reach, not by $n$ and $m$. The opposite is an explicit graph, stored as an [adjacency list](/adjacency-list/), an [adjacency matrix](/adjacency-matrix/) or an [edge list](/edge-list/).

## In plain words

Some graphs are too big to write down, or there is no reason to write them down. Think of all the positions of a sliding puzzle. Nobody makes a list of them. Instead, you have a rule: from this position, these moves are legal, and each move gives a new position. That rule is the graph.

A search program asks the rule for the next positions of the position it is at, and it remembers only the positions it has already seen. So the memory it uses depends on how far it goes, not on how many positions exist. Other graphs are implicit because a short label on each vertex is enough to tell if two vertices are joined.

## The idea

**Definition.** A graph $G = (V, E)$, directed or undirected, is *given implicitly* when the input is not $E$ but:

1. an encoding of the vertices, often as short strings, tuples or integers, and usually a start vertex $s$;
2. a *successor function* $\operatorname{succ}(v)$ that returns the list of out-neighbours of $v$, and for an undirected graph the list of neighbours; and, in some uses,
3. an *adjacency test* $\operatorname{adj}(u, v)$, a *goal test* on vertices, or a weight function on the edges.

Each call costs the time of the rule, not a memory access. The graph can be infinite, as long as each vertex has finitely many successors. An explicit graph is the case where the rule is a lookup in a stored table.

**What the representation costs.** Let $t$ be the time to compute $\operatorname{succ}(v)$ for one vertex and $b$ the most successors of a vertex, the *branching factor*.

| task | explicit adjacency list | implicit graph |
|---|---|---|
| store the graph | $\Theta(n + m)$ words | the size of the rule, often $O(1)$ |
| neighbours of $v$ | $\Theta(1 + d(v))$ | $t$ per call; nothing is cached |
| adjacency test | $O(d(u))$, or $O(1)$ with a matrix | the time of $\operatorname{adj}$, or of $\operatorname{succ}(u)$ and a scan |
| [BFS](/breadth-first-search/) from $s$ that reaches $r$ vertices | $O(n + m)$, with $\Theta(n)$ arrays | $O(r \cdot t)$ time, $\Theta(r)$ space for a hash set of seen vertices |
| depth-first search to depth $\ell$ without a seen set | | $O(b^{\ell} t)$ time, $O(\ell)$ frames of space |

So on an implicit graph, the arrays indexed by vertex that BFS and DFS use become a [hash table](/hash-table/) keyed by the encoding of the vertex, and the bound depends on $r$, the number of vertices reached. When even $r$ vertices do not fit in memory, depth-first search without a seen set, or [iterative-deepening A*](/iterative-deepening-a-star/), keeps only the current path and pays in time, since it may visit a vertex many times. [Bidirectional search](/bidirectional-search/) searches from both ends and reaches about $2 b^{\ell/2}$ vertices instead of $b^{\ell}$ when the goal is at distance $\ell$.

**Implicit representation by labels.** Kannan, Naor and Rudich use the word in a second, more exact sense. A class $\mathcal{C}$ of graphs has an *implicit representation* when there is one decoder $D$ such that each $G \in \mathcal{C}$ on $n$ vertices can be given labels $\ell(v)$ of $O(\log n)$ bits, with $u$ and $v$ adjacent exactly when $D(\ell(u), \ell(v)) = 1$. So the graph is stored only in its labels, in $O(n \log n)$ bits, and adjacency is decided from two labels alone. Examples:

- A rooted forest: label $v$ by the pair (number of $v$, number of the parent of $v$), so $2 \lceil \log_2 n \rceil$ bits, and $u, v$ are adjacent when one is the parent of the other.
- A graph of [degeneracy](/degeneracy/) at most $k$: orient each edge toward the vertex that comes later in the degeneracy order, so each vertex has at most $k$ out-neighbours, and label $v$ by its number and those of its out-neighbours, $(k + 1) \lceil \log_2 n \rceil$ bits. This covers planar graphs with $k = 5$.

Counting gives a limit. The labels of all $n$ vertices take $O(n \log n)$ bits in total, so a class with an implicit representation has at most $2^{O(n \log n)}$ graphs on $n$ labelled vertices. The class of all graphs has $2^{\binom{n}{2}}$, so it has none. The converse fails: Hatami and Hatami showed in 2022 that some hereditary classes with $2^{O(n \log n)}$ graphs on $n$ vertices have no implicit representation, which disproved the *implicit graph conjecture* of Kannan, Naor and Rudich.

## Examples

**The 2 × 2 sliding puzzle.** The board has four cells, three tiles 1, 2, 3 and a blank. A vertex is a placement of the tiles, encoded as the tuple of the cells read row by row, with 0 for the blank, and the successor function moves a tile next to the blank into it. There are $4! = 24$ vertices. Each vertex has exactly 2 successors, since a corner cell has 2 neighbour cells. A BFS from $s = (1, 2, 3, 0)$, the board with $1\,2$ on top and $3$ and the blank below, reaches $r = 12$ vertices, with 1 vertex at distance 0, 2 at each distance from 1 to 5, and 1 at distance 6. So the component of $s$ is a cycle of length 12, and the other 12 placements form a second component that $s$ cannot reach. The search stored 12 vertices; no edge list was ever built.

**The 15 puzzle.** The same rule on the $4 \times 4$ board gives $16! \approx 2.09 \times 10^{13}$ vertices in two components of $16!/2 = 10\,461\,394\,944\,000$ each, with branching factor 2, 3 or 4. An adjacency list of one component would take hundreds of terabytes, so the [sliding tile puzzle](/sliding-tile-puzzle/) is always searched implicitly, usually with [IDA*](/iterative-deepening-a-star/) and a heuristic.

**The hypercube.** $Q_d$ has the vertices $\{0, 1\}^d$, encoded as $d$-bit integers, and $\operatorname{succ}(v) = \{v \oplus 2^i : 0 \le i < d\}$, where $\oplus$ is bitwise exclusive or. So $n = 2^d$ and $m = d\, 2^{d-1}$, but the rule takes $O(1)$ space, lists the neighbours in $O(d)$ time and tests adjacency in $O(1)$ time: $u$ and $v$ are adjacent when $u \oplus v$ is a power of two.

**Grid graphs.** The cells $(i, j)$ of an $R \times C$ grid, with an edge between cells that differ by 1 in one coordinate. A maze or a game map stores only the blocked cells; the 4 neighbours of a cell are computed by adding $(\pm 1, 0)$ and $(0, \pm 1)$ and checking the bounds. This is the setting of [A*](/a-star-search/) on maps.

**A functional rule.** For a function $f$ on a finite set, such as $x \mapsto x^2 + 1 \bmod N$, the [functional graph](/functional-graph/) has the edges $(x, f(x))$. With $N$ near $10^{30}$ it cannot be stored, and [Floyd's cycle detection](/floyd-cycle-detection/) walks it in $O(1)$ space.

**Arrays as implicit trees.** A [binary heap](/binary-heap/) stores a complete binary tree in an array with no pointers: the children of index $i$ are $2i + 1$ and $2i + 2$, and its parent is $\lfloor (i - 1)/2 \rfloor$. The tree edges are computed, not stored.

## Where it is used

- **State-space search.** Planning, puzzles and model checking search a graph of states given by an initial state and a transition rule. See [state-space search](/state-space-search/), [A*](/a-star-search/) and [IDA*](/iterative-deepening-a-star/).
- **Games.** A [game tree](/game-tree/) is generated move by move during [minimax](/minimax/) search and is never stored in full.
- **Grids and geometry.** Pathfinding on maps and image processing on pixel grids compute the neighbours of a cell from its coordinates.
- **Combinatorial generation.** Graphs such as the hypercube, the [de Bruijn graph](/de-bruijn-graph/) and the graph of [Gray code](/gray-code/) steps are defined by rules on strings, and their Hamiltonian paths and cycles are found by rules too.
- **Cycle finding.** The iteration of a function in [Pollard's rho method](/pollard-rho/) walks an implicit functional graph.
- **Compact data structures.** Implicit trees in arrays, such as the binary heap, and labelling schemes for adjacency in distributed systems, avoid storing edges.

## References
