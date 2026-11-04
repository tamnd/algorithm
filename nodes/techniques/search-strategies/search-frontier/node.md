---
tag: EFN36B
kind: concept
slug: search-frontier
name: Search frontier
aliases:
- open list
- fringe
- agenda
area: techniques/search-strategies
level: intro
summary: The set of generated but not yet expanded states, whose removal order defines the search strategy.
prereqs: [search-tree, queue, priority-queue]
see_also: [search-strategy, graph-search-vs-tree-search, open-list, binary-heap, hash-table, uniform-cost-search, breadth-first-search, depth-first-search]
sources:
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 3, Section 3.3 (the frontier and its separation property, and Section 3.3.2 on the queues that hold it)
  - book: isbn:9780201055948
    title: Judea Pearl, Heuristics, Intelligent Search Strategies for Computer Problem Solving
    locator: Chapter 2 (the OPEN and CLOSED lists of the basic search procedures)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.2 (the queue of breadth-first search) and Section 22.3 (the min-priority queue of Dijkstra's algorithm)
---

The frontier of a search is the set of nodes that the search has generated but not yet expanded. A [search strategy](/search-strategy/) is, in most cases, just the rule that removes the next node from the frontier: a FIFO [queue](/queue/) gives [breadth-first search](/breadth-first-search/), a [stack](/stack/) gives [depth-first search](/depth-first-search/), and a [priority queue](/priority-queue/) gives [uniform-cost](/uniform-cost-search/) and other [best-first](/best-first-search/) searches. The frontier separates the part of the [search tree](/search-tree/) already explored from the rest, and its size is often the memory bound of the search. Older texts call it the open list, the fringe or the agenda.

## In plain words

A search keeps a to-do list. Each entry is a place that the search knows about but has not yet looked behind. At each step the search takes one entry off the list, looks at it, and puts its neighbours on the list.

The list is the frontier. How the search takes the next entry decides the kind of search. Take the oldest entry and you search in rings around the start. Take the newest entry and you go deep first. Take the entry with the cheapest route so far and you find the cheapest route.

Every way from the start to a place you have not seen yet goes through an entry of the list. So the list is all the search needs to remember to go on. The list can also become very long, and then it fills the memory.

## The idea

### Definition

Let a search run the loop of the [search strategy](/search-strategy/) page: remove a node from the frontier, test it, and add its children. At the start of an iteration, the *frontier* $F$ is the set of nodes that were added and not yet removed. The nodes removed so far are the *expanded* nodes, and the generated nodes are the expanded nodes together with $F$. In graph search, a table *reached* (Russell and Norvig) or a *closed* list (Pearl) holds the states that the search has already seen, see [graph search versus tree search](/graph-search-vs-tree-search/).

### The separation property

**Claim (tree-like search).** At the start of each iteration, each node of the search tree is expanded, in $F$, or a descendant of a node in $F$.

*Proof.* By induction on the iterations. At the start, $F$ holds only the root, and each node is the root or one of its descendants. Assume the claim at the start of an iteration that removes $n$ from $F$ and adds all children of $n$. A node that was expanded stays expanded. The node $n$ becomes expanded. A proper descendant of $n$ is a child of $n$, now in $F$, or a descendant of a child of $n$. Each other node of $F$ stays in $F$, with its descendants. $\square$

**Claim (graph search).** Assume that each state in *reached* is either in $F$ or expanded, and that each child state of an expanded state is in *reached*. Then each path from $s_0$ to a state that is not in *reached* passes through a state in $F$.

*Proof.* Let $s_0, s_1, \ldots, s_k$ be such a path, with $s_k$ not reached. The state $s_0$ is reached, so there is a largest index $i < k$ with $s_i$ reached. Then $s_{i+1}$ is not reached. If $s_i$ were expanded, its child $s_{i+1}$ would be reached. So $s_i$ is in $F$. $\square$

The two hypotheses of the second claim hold for the graph search loop: a state enters *reached* exactly when its node enters $F$, and expanding a node puts each child state in *reached*. The property says that the frontier is a cut between the explored part and the unexplored part. Each unexplored solution is a continuation of a frontier node. It is why a search can stop with failure when $F$ is empty: no unexplored path remains.

### Data structures

The frontier needs three operations: test whether it is empty, remove the next node, and add a node. A separate membership test, by state, comes from the *reached* table, which is usually a [hash table](/hash-table/).

| frontier | remove | add | strategy |
| --- | --- | --- | --- |
| FIFO queue | $O(1)$, the oldest | $O(1)$ | breadth-first |
| LIFO stack | $O(1)$, the newest | $O(1)$ | depth-first |
| [binary heap](/binary-heap/) on $f$ | $O(\log \lvert F \rvert)$, least $f$ | $O(\log \lvert F \rvert)$ | best-first, uniform-cost, A* |
| array of buckets, integer $f$ in a small range | $O(1)$ amortized | $O(1)$ | uniform-cost with small integer costs |

A priority queue also meets the case when a cheaper path to a state already in $F$ appears. There are two ways to handle it. A *decrease-key* operation lowers the priority of the old node in place, and needs a map from states to heap positions. *Lazy insertion* adds a second node for the same state and leaves the old one in the heap. When an old node comes out later, its cost is larger than the cost in *reached*, and the search skips it. Lazy insertion is simpler and needs no map into the heap. It makes the heap hold up to one entry per generated node instead of one per state.

### Size

The frontier is often the memory bound. For tree-like search in a uniform tree with branching factor $b$:

- Breadth-first search, when it expands the last node of depth $d - 1$, has all $b^d$ nodes of depth $d$ in $F$. With a goal test at expansion instead of generation, it can also add most of depth $d + 1$, up to $b^{d+1}$ nodes.
- Depth-first search, which pushes all children of a node at once, holds at most $b - 1$ waiting siblings for each level of the current path, plus the children of the last node. So $|F| \le (b - 1)m + 1$ for a tree of depth $m$. This is the $O(bm)$ space of the [search strategy](/search-strategy/) table.
- Uniform-cost search holds the nodes whose cost is near the current cost bound. In the worst case this is $O(b^{1 + \lfloor C^*/\epsilon \rfloor})$.

## Examples

### A breadth-first frontier

In the tree of a uniform branching factor $b = 10$, the frontier of breadth-first search at depth $d$ holds $10^d$ nodes. If one node takes 100 bytes, the frontier at depth 8 takes $10^8 \times 100$ bytes, which is 10 gigabytes, while the depth-first frontier for the same depth holds at most $9 \cdot 8 + 1 = 73$ nodes. This gap is the reason for [iterative deepening search](/iterative-deepening-search/), which has the order of breadth-first search and the frontier of depth-first search.

### A priority-queue frontier with lazy insertion

The graph has the directed edges S→A 1, S→G 12, A→B 4, A→C 1, B→D 3, C→D 1, C→G 2, D→G 3. Uniform-cost search from S to G keeps the frontier in a heap ordered by the path cost $g$, and adds a node only if its state is new or its cost is lower than the cost in *reached*.

| step | frontier before the step, as path:$g$ | removed | reached after the step |
| --- | --- | --- | --- |
| 1 | S:0 | S | S 0, A 1, G 12 |
| 2 | S-A:1, S-G:12 | S-A | S 0, A 1, G 12, B 5, C 2 |
| 3 | S-A-C:2, S-A-B:5, S-G:12 | S-A-C | ..., G 4, D 3 |
| 4 | S-A-C-D:3, S-A-C-G:4, S-A-B:5, S-G:12 | S-A-C-D | unchanged |
| 5 | S-A-C-G:4, S-A-B:5, S-G:12 | S-A-C-G, a goal | |

At step 3 the cheaper path S-A-C-G (cost 4) to G is found. With lazy insertion, the old node S-G:12 stays in the heap as a stale entry. With decrease-key, the search would replace it, and the heap would hold G only once. At step 4 the path S-A-C-D-G costs 6, more than 4, so it is not added. The search stops when the goal leaves the frontier, not when it enters, which is why it returns cost 4 and not 12.

### The frontier as a cut

After step 2, the frontier holds the states C, B and G, and the state D is not yet reached. The two paths from S to D are S-A-B-D and S-A-C-D. The first passes through the frontier state B and the second through the frontier state C, as the separation property says. After step 3, every state is reached, and the property holds with no such path.

## Where it is used

Each [search strategy](/search-strategy/) is a frontier discipline, and the [open list](/open-list/) of A* and its variants is the frontier under another name. The frontier of [breadth-first search](/breadth-first-search/) on an explicit graph is one layer of vertices, and the frontier of [Dijkstra's algorithm](/dijkstra/) is its priority queue. [Bidirectional search](/bidirectional-search/) keeps two frontiers and stops when they meet. [Beam search](/beam-search/) keeps only the best $k$ nodes of each layer, a frontier of bounded size that gives up completeness. In [branch and bound](/best-first-branch-and-bound/), the frontier is the set of live nodes, and the node selection rule plays the part of the strategy.

## References
