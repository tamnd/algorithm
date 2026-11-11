---
tag: Y75PP5
kind: model
slug: local-model
name: LOCAL model
aliases:
- LOCAL model of distributed computing
- synchronous message-passing model with unbounded messages
area: distributed/distributed-graph-algorithms
level: core
summary: Nodes of a graph with unique identifiers compute in synchronous rounds and send messages of any size to their neighbours. After r rounds a node knows exactly its radius-r ball.
prereqs: [synchronous-model, port-numbering, breadth-first-search]
see_also: [congest-model, congested-clique-model, port-numbering, round-complexity, linial-coloring-lower-bound, cole-vishkin, network-decomposition, locally-checkable-labeling]
sources:
  - paper: doi:10.1137/0221015
    title: Nathan Linial, Locality in distributed graph algorithms, SIAM Journal on Computing 21(1), 193-201, 1992
    locator: the synchronous model with unique identifiers and no limit on message size, the view of radius t, the lower bound for 3-colouring the ring and the O(Delta^2)-colouring in O(log* n) rounds
  - book: isbn:9780898714647
    title: David Peleg, Distributed Computing, A Locality-Sensitive Approach, SIAM, 2000
    locator: Chapter 2 (the model, the LOCAL and CONGEST variants, and the measures of time and communication)
  - url: https://jukkasuomela.fi/da2020/da2020.pdf
    title: Juho Hirvonen and Jukka Suomela, Distributed Algorithms 2020, online textbook
    locator: Chapter 4 (the LOCAL model, unique identifiers, and the gathering algorithm that solves every problem in O(diameter) rounds) and Chapter 8 (local neighbourhoods)
  - paper: "Moni Naor and Larry Stockmeyer, What can be computed locally?, SIAM Journal on Computing 24(6), 1259-1277, 1995"
    locator: locally checkable labellings and their computation in a constant number of rounds
  - paper: doi:10.1145/3357713.3384298
    title: Václav Rozhoň and Mohsen Ghaffari, Polylogarithmic-time deterministic network decomposition and distributed derandomization, STOC 2020
    locator: deterministic network decomposition in polylogarithmic rounds of the LOCAL model and its consequences
---

The LOCAL model is the standard model for the question "how far must a node look to solve a graph problem?". The network is the input graph itself. Each node has a unique identifier, all nodes work in synchronous rounds, and in each round every node can send a message of any size to each neighbour and do any amount of local computation. The only cost is the number of rounds. Linial (1992) introduced it to study *locality*, and Peleg (2000) named it LOCAL. The model has a simple and exact characterization: what a node knows after $r$ rounds is exactly its *ball* of radius $r$, so an $r$-round algorithm is the same thing as a map from radius-$r$ balls to outputs, and every solvable problem takes at most $D + 1$ rounds. The [CONGEST model](/congest-model/) is the same model with messages of $O(\log n)$ bits.

## The machine

**Notation.** The network is a simple connected undirected graph $G = (V, E)$ with $n = |V|$ nodes, $m = |E|$ edges, diameter $D$ and largest degree $\Delta$. The distance $d(u, v)$ is the number of edges on a shortest path, and $\mathrm{ecc}(v) = \max_u d(u, v)$.

**Nodes.** Each node $v$ is a processor with unbounded memory. It starts with:

- a unique identifier $\mathrm{id}(v)$ from $\{1, \dots, n^c\}$ for a constant $c$, so that an identifier fits in $O(\log n)$ bits;
- its degree and [port numbers](/port-numbering/) $1, \dots, \deg(v)$ for its edges, but not the identifiers of its neighbours (they can learn them in one round);
- a local input, if the problem has one;
- often the value of $n$, or a polynomial upper bound on it; algorithms that need it say so.

**Rounds.** Computation proceeds in synchronous rounds $1, 2, \dots$. In each round every node, at the same time,

1. sends one message on each port (or nothing),
2. receives the messages sent to it on its ports in this round,
3. does any local computation and updates its state.

Messages have no size limit. Local computation is free. There are no failures: no node crashes and no message is lost or changed. In the deterministic form there is no randomness; in the randomized form each node also has private random bits.

**Output.** Each node eventually stops with a local output, such as its colour, whether it is in the set, or the state of each incident edge. The outputs together must form a valid solution.

**Timing.** The model is the fault-free case of the [synchronous model](/synchronous-model/). On an [asynchronous](/asynchronous-model/) network, a [synchronizer](/synchronizer/) gives the same round structure.

## What it counts

**Rounds.** The *round complexity* of an algorithm is the number of rounds until every node has stopped, as a function of $n$ and often $\Delta$, in the worst case over graphs, identifiers and inputs. For randomized algorithms, the rounds within which all nodes stop with probability at least $1 - 1/n$. See [round complexity](/round-complexity/).

**Nothing else.** Messages, bits and local work are free. This is deliberate: a lower bound in LOCAL holds for every model with less power, and it shows that the obstacle is the distance that information must travel, not bandwidth or computation.

**Balls.** For a node $v$ and $r \ge 0$, the *ball of radius $r$*, $B_r(v)$, consists of

- the identifier, input and degree of every node $u$ with $d(u, v) \le r$,
- every edge with an endpoint $u$ at $d(u, v) \le r - 1$, with its port numbers at both ends.

Edges between two nodes at distance exactly $r$ are not in the ball.

**Theorem 1 (locality, proved here).** For every deterministic algorithm and every $r \ge 0$, the state of $v$ after $r$ rounds is a function of $B_r(v)$. Conversely, the full-information algorithm, in which every node sends its whole state, with the port it sends on, in every round, learns $B_r(v)$ in $r$ rounds.

*Proof.* By induction on $r$. After 0 rounds the state of $v$ is a function of its identifier, input and degree, which are in $B_0(v)$. Let $r \ge 1$. The state of $v$ after round $r$ is computed from its state after round $r - 1$ and the messages of round $r$. The first is a function of $B_{r-1}(v) \subseteq B_r(v)$. The message on the edge $\{w, v\}$, sent by $w$ on its port $j$, is a function of $j$ and of the state of $w$ after round $r - 1$, so of $B_{r-1}(w)$. If $w$ is a neighbour of $v$, every node within distance $r - 1$ of $w$ is within distance $r$ of $v$, and every edge with an endpoint within distance $r - 2$ of $w$ has an endpoint within distance $r - 1$ of $v$; so $B_{r-1}(w) \subseteq B_r(v)$, and the edge $\{w, v\}$ with its ports is in $B_r(v)$ because $d(v, v) = 0 \le r - 1$. So the new state is a function of $B_r(v)$.

For the converse, also by induction: after round $r$, node $v$ holds the state of each neighbour $w$ after round $r - 1$, which contains $B_{r-1}(w)$, together with the port of $w$ and its own port for the edge. The union of these balls and the edges at $v$ is $B_r(v)$: a node at distance at most $r$ from $v$ is at distance at most $r - 1$ from some neighbour (or is $v$), and an edge with an endpoint at distance at most $r - 1$ from $v$ either is at $v$ or has an endpoint at distance at most $r - 2$ from some neighbour. ∎

So an $r$-round algorithm is exactly a function $f$ from balls of radius $r$ to outputs, and $r$ rounds are needed whenever the correct output at some node depends on something at distance $r$. Lower bounds in LOCAL are proofs that two nodes with identical balls of radius $r$ must give different outputs.

**Theorem 2 (every problem in $D + 1$ rounds, proved here).** Every problem whose valid outputs depend only on the graph, the identifiers and the inputs, and which has a valid output for every such instance, is solved deterministically in at most $D + 1$ rounds, and no knowledge of $n$ or $D$ is needed.

*Proof.* In round 1 each node sends its identifier, and then knows the identifiers of its neighbours by port. From round 2 on, each node sends all *records* it knows, where the record of $u$ is its identifier, input and list of neighbour identifiers. By induction on $k$, as in the converse part of Theorem 1, after round $k$ node $v$ has the records of exactly the nodes at distance at most $k - 1$. Node $v$ checks after each round whether every identifier that appears in a known record has a record too. After round $k \le \mathrm{ecc}(v)$ this fails, since a node at distance $k$ appears in the record of a node at distance $k - 1$ but has no record. After round $\mathrm{ecc}(v) + 1$ it holds, and the known records describe all of $G$, since $G$ is connected. Then $v$ computes the first valid solution in a fixed order of all candidate solutions, the same at every node, and outputs its own part. Every node stops by round $\max_v \mathrm{ecc}(v) + 1 = D + 1$. ∎

So the round complexity of every problem in LOCAL lies between 0 and $D + 1$. The interesting questions are the problems that need far fewer than $D$ rounds, such as colouring a ring in $O(\log^* n)$ rounds while $D = \lfloor n/2 \rfloor$, and lower bounds that hold even on graphs of small degree.

## Relation to other models

- **[CONGEST](/congest-model/).** The same model with $O(\log n)$-bit messages. Every CONGEST algorithm is a LOCAL algorithm, so LOCAL lower bounds hold in CONGEST. Problems such as [MST](/distributed-mst/), [diameter](/distributed-diameter/) and [APSP](/distributed-apsp/) take $O(D)$ rounds in LOCAL by Theorem 2 but $\tilde{\Omega}(\sqrt{n} + D)$ or $\tilde{\Omega}(n)$ rounds in CONGEST.
- **[Port numbering](/port-numbering/).** LOCAL without identifiers. Many problems become unsolvable, for example breaking the symmetry of a ring; identifiers are a strict addition.
- **[Congested clique](/congested-clique-model/).** The communication graph is complete, the input graph is separate, and messages have $O(\log n)$ bits. LOCAL on a complete graph is trivial: everyone learns everything in one round.
- **SLOCAL and network decomposition.** In the sequential local model, nodes are processed one by one and each reads a ball of radius $r$. A [network decomposition](/network-decomposition/) with $O(\log n)$ colours and $O(\log n)$ diameter turns $O(\log n)$-radius SLOCAL algorithms into $\mathrm{poly}\log n$-round LOCAL algorithms.
- **Synchronous and asynchronous models.** LOCAL is the [synchronous model](/synchronous-model/) without failures and with no limit on messages; fault tolerance and the [asynchronous model](/asynchronous-model/) are treated in the consensus pages.
- **Parallel models.** Collecting a ball of radius $r$ is like reading the $r$-th power of the graph; in [PRAM](/pram-model/) and MPC terms this is graph exponentiation, and LOCAL lower bounds give conditional lower bounds there.

## Known results in the model

All bounds below are cited unless the page links a proof. $n$ is the number of nodes and $\Delta$ the largest degree.

| problem | upper bound | lower bound |
|---|---|---|
| any solvable problem | $D + 1$ (Theorem 2) | depends on the problem |
| 3-colouring a ring or a path | $O(\log^* n)$, [Cole and Vishkin](/cole-vishkin/) (1986) | $\Omega(\log^* n)$, [Linial](/linial-coloring-lower-bound/) (1992) |
| $O(\Delta^2)$-colouring | $O(\log^* n)$, [Linial](/linial-algorithm/) (1992) | $\Omega(\log^* n)$ |
| $(\Delta+1)$-[colouring](/distributed-vertex-coloring/), [MIS](/distributed-mis/), [maximal matching](/distributed-maximal-matching/) | $O(\log n)$ randomized ([Luby](/luby-mis/) 1986); $\mathrm{poly}\log n$ deterministic (via [network decomposition](/network-decomposition/), Rozhoň and Ghaffari 2020) | $\Omega\left(\min\left\{\sqrt{\log n / \log\log n}, \log\Delta/\log\log\Delta\right\}\right)$ for MIS and maximal matching ([KMW](/kmw-lower-bound/)) |
| [sinkless orientation](/sinkless-orientation/), minimum degree 3 | $O(\log n)$ deterministic, $O(\log\log n)$ randomized | the same, up to constants |
| [locally checkable labellings](/locally-checkable-labeling/) on bounded degree graphs | constant time for some, $\Theta(\log^* n)$ for others (Naor and Stockmeyer 1995 and later) | gaps between the classes |

Naor and Stockmeyer (1995) showed that for locally checkable problems, constant-round algorithms can be assumed to depend only on the relative order of identifiers, and that some LCLs cannot be solved in constant time. Later work classified the possible complexities of LCLs; see [locally checkable labeling](/locally-checkable-labeling/).

The tests of the implementation check Theorems 1 and 2 on small graphs: the state of the full-information algorithm after $r$ rounds equals the view computed from $B_r(v)$ alone; any change of the graph, the identifiers or the inputs outside $B_r(v)$ leaves it unchanged; a change of an input at distance $r$ changes it; and the gathering algorithm of Theorem 2 stops at node $v$ after exactly $\mathrm{ecc}(v) + 1$ rounds. The same simulator in CONGEST mode accepts synchronous BFS and rejects gathering.

## References
