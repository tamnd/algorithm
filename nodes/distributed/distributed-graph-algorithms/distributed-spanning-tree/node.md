---
tag: J43X2M
kind: problem
slug: distributed-spanning-tree
name: Distributed spanning tree construction
aliases:
- distributed spanning tree
- spanning tree construction in networks
area: distributed/distributed-graph-algorithms
level: intro
summary: Each node of a network must learn its parent, and often its children, in a spanning tree of the network. From a given root, flooding solves it with O(m) messages and in D rounds.
prereqs: [spanning-tree, flooding, broadcast-problem, synchronous-model, asynchronous-model]
see_also: [flooding, echo-algorithm, breadth-first-search-distributed, distributed-mst, gallager-humblet-spira, convergecast, spanning-tree, awerbuch-leader-election]
sources:
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 2, Section 2.3 (flooding and building a spanning tree, synchronous and asynchronous, the tree that is not BFS)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 15, Section 15.3 (AsynchSpanningTree and the trees it can produce); Chapter 4, Section 4.2 (SynchBFS)
  - book: isbn:9780898714647
    title: David Peleg, Distributed Computing, A Locality-Sensitive Approach, SIAM, 2000
    locator: Chapter 5 (tree constructions, BFS trees and their costs)
  - paper: doi:10.1145/357195.357200
    title: Robert G. Gallager, Pierre A. Humblet and Philip M. Spira, A distributed algorithm for minimum-weight spanning trees, ACM Transactions on Programming Languages and Systems 5(1), 66-77, 1983
    locator: the fragment merging algorithm with O(m + n log n) messages and no designated root
---

In the distributed spanning tree problem, the nodes of a connected network must agree on a spanning tree of the network, using only messages along its edges. At the end, each node knows which of its incident edges are tree edges and, in the rooted form, which one leads to its parent. A spanning tree is the basic structure of distributed computing: once it exists, a [broadcast](/broadcast-problem/) costs $n - 1$ messages instead of $\Theta(m)$, and a [convergecast](/convergecast/) collects a global value at the root. With a given root, [flooding](/flooding/) solves the problem: every node takes the sender of its first message as its parent. Without a given root, the problem is as hard as leader election.

## In plain words

Picture a town where the roads form many loops. The town wants to choose a set of roads that still connects every house but has no loops, so that a message sent along these roads never comes back to where it started.

Nobody has a map. Each house can only send notes to its direct neighbours.

If one house starts by sending a note, each house can keep the road on which the first note came. These kept roads connect every house and form no loop. If nobody is in charge, the houses must first decide who starts, which is harder.

## Definition

**Model.** A connected undirected graph $G = (V, E)$ with $n$ nodes, $m$ edges, diameter $D$ and maximum degree $\Delta$. Nodes communicate by messages on the edges; channels are reliable and there are no failures. The timing can be [synchronous](/synchronous-model/) or [asynchronous](/asynchronous-model/). Nodes know their ports; whether they have identifiers depends on the variant.

**Input.** In the rooted variant, one node $r$ is marked as the root and starts. In the unrooted variant, any nonempty set of nodes may start, and nodes have distinct identifiers.

**Output.** Each node $v$ marks a set of its incident edges as tree edges, such that the marked edges form a [spanning tree](/spanning-tree/) $T$ of $G$, and both ends of each edge agree. In the rooted form, each $v \ne r$ also outputs the port of its parent in $T$ rooted at $r$, and often the ports of its children.

**Costs.** The number of messages, and the number of rounds (synchronous) or the time with delays of at most one unit (asynchronous).

## Variants

- **Rooted, any tree.** A root is given. This page's main case.
- **Rooted, with termination.** The root must also learn that the tree is complete. The [echo algorithm](/echo-algorithm/) does this.
- **BFS tree.** The tree must be a shortest path tree in hops from the root. This is [distributed breadth-first search](/breadth-first-search-distributed/); in the synchronous model flooding gives it for free, in the asynchronous model it costs more.
- **Minimum spanning tree.** Edges have weights and the tree must have minimum total weight. This is [distributed MST](/distributed-mst/), solved by [Gallager, Humblet and Spira](/gallager-humblet-spira/) with $O(m + n \log n)$ messages.
- **Unrooted.** No root is given; several nodes start at arbitrary times. The nodes must in effect elect a root, so the problem inherits the costs of leader election.
- **Other shapes.** Depth-first trees, trees of small degree, and low diameter trees are studied as separate problems.

## Examples

**Flooding from a root, synchronous.** On the graph with edges $\{0,1\}, \{0,2\}, \{1,2\}, \{1,3\}, \{2,4\}, \{3,4\}, \{4,5\}$ and root 0, nodes 1 and 2 hear the message in round 1, nodes 3 and 4 in round 2, and node 5 in round 3. Taking the first sender (the one on the smallest port in case of a tie) gives the parents $1 \to 0$, $2 \to 0$, $3 \to 1$, $4 \to 2$, $5 \to 4$, a BFS tree, after $2m - n + 1 = 9$ messages.

**Flooding from a root, asynchronous: the tree need not be BFS.** Take the triangle on nodes 0, 1, 2 with root 0. The root sends to 1 and 2. If the message $0 \to 2$ is delayed by one time unit while $0 \to 1$ and $1 \to 2$ each take a tenth of a unit, node 2 hears first from 1 and takes 1 as its parent. The tree is the path $0, 1, 2$ of depth 2, although node 2 is a neighbour of the root. On the complete graph $K_n$, delays of this kind can produce a Hamiltonian path of depth $n - 1$, although $D = 1$. The result is a spanning tree in every case, since a parent is always reached before its child.

**Non-example.** Let every node pick as its parent the neighbour with the smallest identifier, without any message from a root. In a triangle with identifiers $1, 2, 3$, node 1 picks 2, and nodes 2 and 3 pick 1. Nodes 1 and 2 point at each other, so the pointers contain a cycle and there is no root. A purely local rule cannot see such cycles; a root together with the order in which messages arrive excludes them.

## Known algorithms

| algorithm | setting | messages | time |
|---|---|---|---|
| [flooding](/flooding/) with parent pointers | rooted, any timing | exactly $2m - n + 1$ | $e \le D$ rounds (synchronous); at most $e$ (asynchronous) |
| flooding plus one message to the parent | rooted, children known | $2m$ | one round more |
| [echo algorithm](/echo-algorithm/) | rooted, root detects the end | exactly $2m$ | at most $2e + 1$ rounds; $O(n)$ asynchronous |
| [distributed BFS](/breadth-first-search-distributed/) | rooted, BFS tree, asynchronous | $O(nm)$ or $O(m + nD)$ | $O(D)$ or $O(D^2)$ |
| depth-first token | rooted, DFS tree | $2m$ (or $O(n)$ when nodes know the identifiers of their neighbours) | $O(m)$ (or $O(n)$) |
| [Gallager, Humblet and Spira](/gallager-humblet-spira/) | unrooted, minimum weight, distinct weights | $O(m + n \log n)$ | $O(n \log n)$ |
| [Awerbuch](/awerbuch-leader-election/) (1987) | unrooted, leader and tree | $O(m + n \log n)$ | $O(n)$ |

Here $e$ is the eccentricity of the root. The bounds for flooding and the echo algorithm are proved on their pages; the others are cited there.

## Bounds

**Rounds.** $\Omega(e)$ rounds, and $\Omega(D)$ for the worst choice of root, since a node at distance $e$ from the root cannot hear from it earlier. Flooding meets this bound.

**Messages, rooted.** A spanning tree from $r$ solves the [broadcast problem](/broadcast-problem/) from $r$ with no extra messages (each node's first message carries the broadcast), so the broadcast lower bound applies: when nodes know only their ports and do not know the graph, every algorithm sends at least $m$ messages in the worst case, and flooding is optimal up to a factor of 2. With more knowledge, such as the identifiers of the neighbours, the bound depends on the class of algorithms; see the broadcast page.

**Messages, unrooted.** Any spanning tree algorithm without a root can elect a leader at the cost of $O(n)$ more messages (a convergecast of the maximum identifier on the tree), so the $\Omega(n \log n)$ message lower bound for leader election in rings and the $\Omega(m)$ broadcast bound carry over, giving $\Omega(m + n \log n)$. Gallager, Humblet and Spira, and Awerbuch, match it.

## Reductions

- **Broadcast to spanning tree.** Flooding is a broadcast, and its first messages define the tree. Conversely, a tree gives a broadcast with $n - 1$ messages.
- **Spanning tree to leader election and back.** With a tree, a convergecast of identifiers elects a leader with $O(n)$ messages and $O(h)$ time, $h$ the height of the tree. With a leader, flooding from it builds a tree with $O(m)$ messages.
- **Spanning tree to termination.** A rooted tree turns every broadcast into an acknowledged broadcast, by a [convergecast](/convergecast/) of "done".
- **MST to spanning tree.** Every minimum spanning tree algorithm solves this problem; the converse needs weights to be taken into account and costs more.

## Applications

- **Broadcast and aggregation backbone.** Repeated broadcasts, global sums, counting $n$ and computing the maximum all run on a tree with $n - 1$ messages each.
- **Synchronizers.** The [β synchronizer](/synchronizer/) runs each simulated round as a convergecast and a broadcast on a spanning tree.
- **Termination detection.** Tree based schemes, such as the [Dijkstra-Scholten algorithm](/dijkstra-scholten/), build a tree of the active part of a computation.
- **Network protocols.** The spanning tree protocol of Ethernet bridges chooses a root by identifiers and builds a shortest path tree to it, so that broadcast frames do not loop.

## References
