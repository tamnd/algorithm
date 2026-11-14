---
tag: 5HS98N
kind: definition
slug: vertical-constraint-graph
name: Vertical constraint graph
aliases:
- VCG
area: cad/routing
level: core
summary: A directed graph on the nets of a channel, with an edge when one net must take a higher track than another at some column. A cycle in it forces a dogleg.
prereqs: [channel-routing-problem, directed-acyclic-graph]
see_also: [channel-density, left-edge-algorithm, dogleg-channel-routing, yoshimura-kuh-algorithm, greedy-channel-router, dag-longest-path, cycle-detection, topological-sort]
sources:
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 6, Detailed Routing, the section on channel routing (horizontal and vertical constraint graphs and cyclic constraints; general locator)
  - book: isbn:9780792383932
    title: Naveed A. Sherwani, Algorithms for VLSI Physical Design Automation, third edition, Kluwer, 1999
    locator: the chapter on detailed routing, the part on channel routing (the vertical constraint graph and its cycles; general locator)
  - paper: "T. Yoshimura and E. S. Kuh, Efficient algorithms for channel routing, IEEE Transactions on Computer-Aided Design 1(1), 25 to 35, 1982"
    locator: the vertical constraint graph, its longest path as a lower bound and the merging of nets that keeps it short (general locator)
  - paper: "D. N. Deutsch, A dogleg channel router, Proceedings of the 13th Design Automation Conference, 425 to 433, 1976"
    locator: the use of doglegs to break the vertical constraints that join two nets in a cycle (general locator)
---

The vertical constraint graph records which net must lie above which in a [channel](/channel-routing-problem/). When a column has a pin of net $a$ on the top edge and a pin of net $b$ on the bottom edge, the branch of $a$ comes down from the top and the branch of $b$ comes up from the bottom in the same column, on the same layer. If each net has one trunk, the trunk of $a$ must be on a higher track than the trunk of $b$, or the two branches meet. The graph has one node for each net and one edge $a \to b$ for each such column. Its cycles tell when a channel has no routing without doglegs, and its longest path gives a second lower bound on the number of tracks, next to the [channel density](/channel-density/).

## Definition

**Channel.** Use the notation of the [channel routing problem](/channel-routing-problem/): columns $1, \ldots, n$, top pins $\mathrm{top}(c)$ and bottom pins $\mathrm{bot}(c)$, each a net label or 0, and tracks $1, \ldots, T$ numbered from the top. Trunks run on layer H and branches on layer V.

**Vertical constraint graph.** The vertical constraint graph $G_v$ is the directed graph whose nodes are the nets and whose edges are
$$ E_v = \{ (\mathrm{top}(c), \mathrm{bot}(c)) : 1 \le c \le n,\ \mathrm{top}(c) \ne 0,\ \mathrm{bot}(c) \ne 0,\ \mathrm{top}(c) \ne \mathrm{bot}(c) \}. $$
An edge $a \to b$ reads "$a$ above $b$". Several columns can give the same edge, and the graph keeps it once.

**Meaning without doglegs.** In a routing where each net $N$ has one trunk on track $t(N)$, every edge $a \to b$ forces $t(a) < t(b)$.

*Proof.* Let column $c$ give the edge. The top pin of $a$ is the point $(c, 0)$ on layer V, and layer V has only vertical edges, so the wire of $a$ goes down column $c$ on layer V until a via takes it to layer H. The only trunk of $a$ is on track $t(a)$, so the wire of $a$ holds the points $(c, y)$ for $0 \le y \le t(a)$ on layer V. In the same way, the wire of $b$ holds $(c, y)$ for $t(b) \le y \le T + 1$ on layer V. If $t(a) \ge t(b)$, the point $(c, t(b))$ on layer V belongs to both nets, which is not allowed. $\square$

**Path bound.** If $G_v$ has a path through $k$ nets $N_1 \to N_2 \to \cdots \to N_k$, then every routing without doglegs has $t(N_1) < t(N_2) < \cdots < t(N_k)$, so $T \ge k$. With the density bound, $T \ge \max(d, k_{\max})$, where $k_{\max}$ is the number of nets on a [longest path](/dag-longest-path/) of $G_v$.

**Cycles.** If $G_v$ has a cycle, the inequalities along it give $t(N_1) < t(N_1)$, so no routing without doglegs exists. If $G_v$ is a [directed acyclic graph](/directed-acyclic-graph/), one net per track in a [topological order](/topological-sort/) is a routing, as the page on the [channel routing problem](/channel-routing-problem/) shows. So a routing without doglegs exists if and only if $G_v$ is acyclic. A [cycle detection](/cycle-detection/) by depth-first search decides this in $O(n + N)$ time for $N$ nets.

**Pieces of nets.** When a net may change track at its own pin columns, the nodes of the graph are the pieces of nets between two pin columns that follow each other, and an edge joins a piece of $a$ to a piece of $b$ when both hold a column with $a$ on top and $b$ at the bottom. This finer graph is the one that [dogleg channel routing](/dogleg-channel-routing/) uses.

## Examples and non-examples

**A graph with a long path.** Take the channel

| column | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| top | 1 | 0 | 3 | 1 | 0 | 4 | 6 | 4 | 0 | 5 |
| bottom | 3 | 6 | 0 | 2 | 2 | 0 | 3 | 6 | 5 | 2 |

Columns 1, 4, 7, 8 and 10 have pins of two different nets on top and bottom, and give the edges $1 \to 3$, $1 \to 2$, $6 \to 3$, $4 \to 6$ and $5 \to 2$. Column 9 has net 5 on the bottom only, and column 3 has net 3 on the top only, so they give no edge. The graph is acyclic. The longest path $4 \to 6 \to 3$ has 3 nets, so the path bound is 3, and the density of this channel is 4. The [left-edge algorithm](/left-edge-algorithm/) routes it in 4 tracks.

**When the path bound is larger than the density.** Take

| column | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| top | 5 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |
| bottom | 2 | 2 | 4 | 5 | 3 | 3 | 1 | 4 |

The edges are $5 \to 2$ from column 1 and $1 \to 5$ from column 4. Column 7 has net 1 on both sides and gives no edge. The path $1 \to 5 \to 2$ has 3 nets and the density is 3, so at least 3 tracks are needed, and 3 tracks are enough: net 1 on track 1, nets 3 and 5 on track 2, nets 2 and 4 on track 3.

**A cycle.** Take $n = 2$, top pins $1, 2$, bottom pins $2, 1$. The edges are $1 \to 2$ and $2 \to 1$. No routing without doglegs exists, though the density is 2. The page on [channel density](/channel-density/) shows that even jogs in any column need a third track here.

**Doglegs beat the path bound.** Take

| column | 1 | 2 | 3 | 4 | 5 | 6 |
| --- | --- | --- | --- | --- | --- | --- |
| top | 1 | 2 | 1 | 3 | 0 | 0 |
| bottom | 2 | 0 | 0 | 1 | 3 | 3 |

The edges are $1 \to 2$ and $3 \to 1$, a path through 3 nets, so every routing without doglegs needs 3 tracks. The density is 2. If net 1 changes track at its pin in column 3, the channel fits in 2 tracks, as the page on [dogleg channel routing](/dogleg-channel-routing/) shows. So the path bound holds only in the model without doglegs.

**Not an edge: the same net on both sides.** A column with net $a$ on top and on the bottom joins the two pins by one straight branch. It puts no constraint on the track of $a$ and gives no edge, not a loop $a \to a$.

**Not an edge: nets that only cross.** Two nets whose intervals meet need different tracks where they meet, but that is a horizontal constraint. It does not say which net is higher, so it is not an edge of $G_v$.

## Related definitions

- *Horizontal constraint graph.* The undirected graph on the nets with an edge when two intervals meet. It is an interval graph, and its largest clique has $d$ nets, the [channel density](/channel-density/).
- *Zones.* The maximal sets of nets that cross one column. The [Yoshimura-Kuh algorithm](/yoshimura-kuh-algorithm/) merges nets from different zones so that the longest path of $G_v$ stays short.
- *Constraint graph of pieces.* The graph of the pieces of nets in [dogleg channel routing](/dogleg-channel-routing/). A cycle of $G_v$ can disappear in it, but not always.
- *Transitive edges.* An edge $a \to c$ is implied when $a \to b$ and $b \to c$ are edges. It adds no constraint on the tracks, but routers keep it because it comes from a column.
- [Longest path in a DAG](/dag-longest-path/): computes the path bound in linear time.
- [Greedy channel router](/greedy-channel-router/): does not build $G_v$ at all, and handles the vertical constraints column by column.

## References
