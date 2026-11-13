---
tag: ZC7VJE
kind: concept
slug: duplicate-detection
name: Duplicate detection
aliases:
- closed-list check
- transposition detection in search
area: games-and-search/heuristic-search
level: advanced
summary: Recognizing that a newly generated node has the state of a node that the search already holds, so that only one copy, the cheapest, is kept. It can be immediate, partial, delayed or structured.
prereqs: [graph-search-vs-tree-search, hash-table, open-list]
see_also: [transposition-table, zobrist-hashing, element-distinctness, external-memory-model, memory-bounded-heuristic-search, iterative-deepening-a-star, a-star-search, bidirectional-heuristic-search]
sources:
  - book: isbn:9780123725127
    title: Stefan Edelkamp and Stefan Schroedl, Heuristic Search, Theory and Applications
    locator: Chapter 3 (dictionary data structures for duplicate detection), Chapter 6 (memory restricted search) and Chapter 8 (external search with delayed and structured duplicate detection)
  - paper: Richard E. Korf, Best-first frontier search with delayed duplicate detection, Proceedings of the 19th National Conference on Artificial Intelligence (AAAI-04), 2004
    locator: pp. 650 to 657 (delayed duplicate detection, in which successors are written to disk and duplicates are removed later by sorting or hashing)
  - paper: Rong Zhou and Eric A. Hansen, Structured duplicate detection in external-memory graph search, Proceedings of the 19th National Conference on Artificial Intelligence (AAAI-04), 2004
    locator: pp. 683 to 688 (an abstraction of the state space that bounds the part of the search graph needed to check the duplicates of a block)
  - paper: doi:10.1145/1089023.1089024
    title: Richard E. Korf, Weixiong Zhang, Ignacio Thayer and Heath Hohwald, Frontier search, Journal of the ACM 52(5) (2005)
    locator: pp. 715 to 748 (search that stores only the open list, marks used operators to prevent regenerating closed nodes, and recovers the path by divide and conquer)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 3, Section 3.3.3 (redundant paths, the reached table, and checking only for cycles)
---

Duplicate detection is the part of a graph search that notices when a newly generated node has the same state as a node that the search already holds. In a state space with many paths to each state, such as a grid or a puzzle, most generated nodes are duplicates, and a search that keeps them all does exponentially more work than one that keeps one node per state. The standard method is *immediate* duplicate detection: a [hash table](/hash-table/) over the states of OPEN and CLOSED, checked at each generation. When memory is the limit, searches use *partial* detection, which checks only the current path or a cache, *delayed* detection, which collects successors on disk and removes duplicates in batches, or *structured* detection, which uses the structure of the space to keep only the relevant part of the table in memory.

## In plain words

You walk through a city and keep a list of the corners you have reached. At each corner, you look it up in your list. If it is there and you got there by a longer way this time, you forget this new way. If this way is shorter, you keep the new way and forget the old one.

Without the list, you would treat each way of getting to a corner as a new place. There are many ways to each corner, so you would do the same work again and again.

When the list is too long to keep in your head, you can write the new corners in a notebook and cross out the repeats once an hour. Or you can split the city into districts and keep in your head only the lists of the districts next to where you are.

## The idea

### What a duplicate is

A *node* of the [search tree](/search-tree/) is a path from the start, and a *state* is where the path ends. A newly generated node $n'$ with state $s$ is a *duplicate* if the search already holds a node with state $s$, in OPEN or in CLOSED. The decision whether to look for duplicates at all is the subject of [graph search versus tree search](/graph-search-vs-tree-search/). This page is about how to find them and what to do with them.

For a cheapest path search such as [A*](/a-star-search/), the rule on a duplicate is to compare costs. If the new $g$ is not smaller, drop the new node. If it is smaller, keep the new node with its parent pointer and drop the old one, and if the old one was in CLOSED, put the state back in OPEN. With a [consistent heuristic](/consistent-heuristic/) the last case never happens for a state in CLOSED, so CLOSED only needs to answer whether a state is in it.

### Immediate detection

A hash table keyed by the state, as in the [open list](/open-list/) of A*, finds a duplicate in $O(1)$ expected time per generated node, after the state is hashed. For board states, [Zobrist hashing](/zobrist-hashing/) updates the hash value in $O(1)$ per move. The table holds every generated state, so the memory grows with the number of states, which is the reason why A* runs out of memory before it runs out of time.

### Partial detection

Searches with little memory check for only some duplicates.

- **Parent pruning.** Do not generate the parent of a node as its child. It costs nothing and removes the shortest cycles.
- **Cycle check.** Compare the new state with the states on the current path, as [depth-limited search](/depth-limited-search/) and [IDA*](/iterative-deepening-a-star/) often do. It removes all cycles but not other duplicates.
- **A bounded cache.** Keep a table of recent states and replace old entries. A [transposition table](/transposition-table/) in game search is this kind of cache, and it stores the value and depth of a position, not only the fact that it was seen.
- **Hashing with loss.** Keep only a bit per hash value, as in the bitstate hashing of some model checkers. Two states with the same hash then look like duplicates, so states can be missed, and the search is no longer complete.

### Delayed detection

Korf (2004) introduced delayed duplicate detection for searches whose states do not fit in memory. A breadth-first or best-first layer writes all the successors that it generates to disk, duplicates included. Then the file is sorted, or split by a hash of the state into parts that fit in memory, and the duplicates within the file and those that are already in the earlier layers are removed in one pass. Each node costs a few sequential passes over disk instead of a random access, which suits the [external memory model](/external-memory-model/).

### Structured detection

Zhou and Hansen (2004) partition the states by an abstraction, a map $\phi$ from states to a small set of blocks. If the successors of each state in block $B$ lie in the blocks next to $B$ in the abstract graph, then the duplicates of a node generated from $B$ can only be in that *duplicate detection scope*. The search expands one block at a time and keeps in memory only the blocks in its scope.

### Detection without a closed list

Frontier search (Korf, Zhang, Thayer and Hohwald, 2005) keeps only OPEN. With each node it stores which operators lead back to a node that was already expanded, and it never applies them. In an undirected graph this is enough to stop the search from generating a CLOSED state again, and the path is rebuilt afterwards by divide and conquer.

### Not element distinctness

[Element distinctness](/element-distinctness/) is the decision problem "are the $n$ given numbers all different?". It is offline: the whole set is known at the start, and the lower bound of $\Omega(n \log n)$ comparisons holds for it. Duplicate detection in search is an online membership test on a set that grows, interleaved with the generation of the states, and with a hash table each test is $O(1)$ expected time. Delayed detection turns the online problem back into the offline one, a batch of states sorted and compared, which is why it can use sorting.

## Examples

On an empty 4-connected grid, search from one cell to a depth of 10 moves.

| method | nodes generated |
| --- | --- |
| no detection | $\sum_{i=0}^{10} 4^i = 1{,}398{,}101$ |
| parent pruning | $1 + \sum_{i=1}^{10} 4 \cdot 3^{i-1} = 118{,}097$ |
| immediate detection | $2 \cdot 10^2 + 2 \cdot 10 + 1 = 221$ |

The count with full detection is the number of cells within Manhattan distance 10, which grows as $2d^2$, while the counts without it grow as $4^d$ and $3^d$. Parent pruning saves a factor of about $(4/3)^d$, but each cell is still reached by very many paths.

In the 8-puzzle, all 181,440 states that can reach the goal lie within 31 moves of it. A search that detects duplicates holds at most 181,440 nodes. A tree search with parent pruning from a state with the blank in a corner generates 86,093,439 nodes to depth 31, counted exactly by the moves of the blank, which is about 474 times as many. Its layers grow by factors of 2 and 1.5 in turn, so by about $\sqrt{3} \approx 1.732$ per move on average.

In A* on the graph of the page [A* search](/a-star-search/), the state C is generated twice: first from A with $g = 6$, then from B with $g = 5$. Duplicate detection finds the first copy in OPEN and lowers its cost. The state S is generated again from A with $g = 4$ and from B with $g = 6$, and both copies are dropped because S has $g = 0$.

## Where it is used

- **A* and uniform-cost search** on explicit or implicit graphs, with a hash table over OPEN and CLOSED.
- **Breadth-first search of puzzles** to find the diameter of the state space or to build [pattern databases](/pattern-database/). Delayed and structured duplicate detection on disk made searches with billions of states possible.
- **Game programs.** The transposition table of a chess program detects positions reached by different move orders and reuses their values.
- **Model checking.** Explicit state model checkers store the visited states with full or lossy hashing.
- **Memory-bounded search.** [Memory-bounded heuristic searches](/memory-bounded-heuristic-search/) trade the completeness of duplicate detection for memory, and frontier search keeps only the boundary of the explored region.

## References
