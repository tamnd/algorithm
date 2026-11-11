---
tag: 2CY7S7
kind: algorithm
slug: breadth-first-search-distributed
name: Distributed breadth-first search
aliases:
- distributed BFS
- synchronous distributed BFS
- SynchBFS
- layered BFS
area: distributed/distributed-graph-algorithms
level: core
summary: Build a BFS tree from a root, one layer per round, in D rounds and O(m) messages. Asynchronous forms trade messages for time, from O(nm) messages in O(D) time to O(m + nD) in O(D²).
solves: [distributed-spanning-tree]
model: synchronous-model
complexity:
  vars: {n: the number of nodes, m: the number of edges, D: the diameter of the network}
  time: {worst: O(D)}
  messages: {worst: 2m − n + 1}
  space: {extra: O(log n)}
properties: {deterministic: true, recursive: false}
prereqs: [breadth-first-search, flooding, synchronous-model, asynchronous-model, distributed-spanning-tree]
see_also: [breadth-first-search, parallel-bfs, distributed-bellman-ford, synchronizer, echo-algorithm, convergecast, distributed-shortest-paths, bfs-tree]
sources:
  - book: isbn:9780898714647
    title: David Peleg, Distributed Computing, A Locality-Sensitive Approach, SIAM, 2000
    locator: Chapter 5 (tree constructions, the distributed Bellman-Ford and the distributed Dijkstra (layered) BFS algorithms with their time and message bounds)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 4, Section 4.2 (SynchBFS); Chapter 15, Section 15.4 (AsynchBFS and LayeredBFS)
  - paper: doi:10.1145/4221.4227
    title: Baruch Awerbuch, Complexity of network synchronization, Journal of the ACM 32(4), 804-823, 1985
    locator: the BFS application of the synchronizers, compared with the layered algorithm
  - paper: doi:10.1145/73007.73054
    title: Baruch Awerbuch, Distributed shortest paths algorithms, Proceedings of the 21st ACM Symposium on Theory of Computing (STOC), 490-500, 1989
    locator: BFS in O(D^(1+ε)) time and O(m^(1+ε)) messages for every fixed ε > 0
  - paper: "Robert G. Gallager, Distributed minimum hop algorithms, Technical Report LIDS-P-1175, Laboratory for Information and Decision Systems, MIT, 1982"
    locator: the layer by layer BFS construction and the trade-off between its time and its message count
---

Distributed breadth-first search builds a tree in which every node knows its distance in hops from a root $r$ and a neighbour one hop closer, its parent. In the [synchronous model](/synchronous-model/) it is the [flooding](/flooding/) of a counter: in round $k$ the nodes at distance $k$ hear the counter for the first time and adopt the sender as parent. That takes $D$ rounds and exactly $2m - n + 1$ messages, and both are optimal up to constant factors. In the [asynchronous model](/asynchronous-model/) the first sender need not be the closest, and there are two classic repairs: the Bellman-Ford form corrects distances as better ones arrive, with $O(D)$ time but up to $O(nm)$ messages, and the layered form grows the tree one layer per phase under the control of the root, with $O(m + nD)$ messages but $O(D^2)$ time.

## In plain words

A teacher in a school wants every pupil to know how many handshakes away from the teacher they stand.

The teacher shakes hands with everyone close by and says "you are 1". Each of them then shakes hands with their neighbours and says "you are 2", and so on. A pupil keeps the first number they hear and remembers who said it.

When everyone moves in step, the first number a pupil hears is the right one, because shorter chains arrive first. When some handshakes are slow, a long chain can arrive first. Then the pupil must either fix the number when a smaller one comes, or wait for the teacher to finish each ring before the next ring starts.

## The problem

**Network.** A connected undirected graph $G = (V, E)$ with $n$ nodes, $m$ edges, diameter $D$ and maximum degree $\Delta$. Channels are reliable; there are no failures. One node, the root $r$, starts the run.

**Knowledge.** A node knows its ports. The synchronous algorithm needs no identifiers and no knowledge of $n$ or $D$. Messages hold one distance, $O(\log n)$ bits, so all forms run in the [CONGEST model](/congest-model/).

**Output.** Each node $v$ outputs $\mathrm{dist}(r, v)$ and, for $v \ne r$, a parent $u$ with $\mathrm{dist}(r, u) = \mathrm{dist}(r, v) - 1$. The parent edges form a BFS tree, a special [spanning tree](/distributed-spanning-tree/), the distributed form of the sequential [breadth-first search](/breadth-first-search/) tree.

**Costs.** Rounds in the synchronous model; in the asynchronous model, time with delays of at most one unit; messages in both. Write $e$ for the eccentricity of $r$, so $D/2 \le e \le D$, and $L_k$ for the set of nodes at distance $k$.

## The algorithm

```pseudo id=main
SYNC-BFS(v)                                ▷ synchronous rounds; r is the root
L1  round 0, at v = r: dist ← 0, parent ← r, send ⟨0⟩ to every neighbour
L2  in each round, on receipt of ⟨d⟩ from the neighbours in a set S:
L3      if dist = ∞ then
L4          dist ← d + 1, parent ← the sender in S on the smallest port
L5          send ⟨dist⟩ to every neighbour except parent
L6      else discard the messages
```

All senders in one round carry the same value $d$, so the choice in line L4 only breaks a tie between equally good parents. If a node must also know its children, each node sends one extra message to its parent in the round after line L4 ($n - 1$ more messages, one more round).

**The asynchronous Bellman-Ford form.** A node keeps the smallest value it has heard. On receipt of $\langle d \rangle$ from $u$ with $d + 1 < \mathit{dist}$, it sets $\mathit{dist} \leftarrow d + 1$, $\mathit{parent} \leftarrow u$, and sends $\langle d + 1 \rangle$ to every neighbour except $u$. This is [distributed Bellman-Ford](/distributed-bellman-ford/) with unit weights.

**The asynchronous layered form.** The root runs phases $k = 1, 2, \dots$. In phase $k$ it broadcasts a PULSE down the tree built so far; each node of depth $k - 1$ sends EXPLORE to all neighbours other than its parent; a node not yet in the tree joins on its first EXPLORE with depth $k$ and answers ACK, and every other EXPLORE gets REJECT; then a [convergecast](/convergecast/) reports to the root whether any node joined. The root stops after the first phase in which none did.

## Example

Take the graph with edges $\{0,1\}, \{0,2\}, \{1,2\}, \{1,3\}, \{2,4\}, \{3,4\}, \{4,5\}$ and root $0$ ($n = 6$, $m = 7$, $e = 3$).

**Synchronous.** In round 1 nodes 1 and 2 hear $\langle 0 \rangle$ and set $\mathit{dist} = 1$. In round 2 nodes 3 and 4 hear $\langle 1 \rangle$ (from 1 and from 2) and set $\mathit{dist} = 2$; the copies between 1 and 2 are discarded. In round 3 node 5 hears $\langle 2 \rangle$ from 4 and sets $\mathit{dist} = 3$; the copies between 3 and 4 are discarded. The output is $\mathit{dist} = (0, 1, 1, 2, 2, 3)$ with parents $(0, 0, 0, 1, 2, 4)$, after $9 = 2 \cdot 7 - 5$ messages.

**Asynchronous Bellman-Ford.** Suppose the message $0 \to 2$ is slow. Then node 2 can first hear $\langle 1 \rangle$ from 1 and set $\mathit{dist}(2) = 2$, and node 4 can then set $\mathit{dist}(4) = 3$ and node 5 $\mathit{dist}(5) = 4$. When $\langle 0 \rangle$ from 0 arrives, node 2 corrects to 1 and sends again; 4 corrects to 2 and 5 to 3. The final tree is the same BFS tree, but the corrections cost extra messages.

**Asynchronous layered.** Phase 1: the root explores and 1 and 2 join. Phase 2: PULSE to 1 and 2; they explore; 3 and 4 join, and the EXPLOREs between 1 and 2 are rejected. Phase 3: PULSE through 1 and 2 to 3 and 4; node 5 joins. Phase 4 finds no new node and the root stops. No node ever holds a wrong distance.

## Correctness

**Synchronous.** By induction on $k$, the nodes that set $\mathit{dist}$ in round $k$ are exactly the nodes of $L_k$: a message that arrives in round $k$ comes from a node of $L_{k-1}$, so it reaches only nodes at distance at most $k$, and every node of $L_k$ has a neighbour in $L_{k-1}$ that sends to it.

**Bellman-Ford.** A value held by a node is the length of a walk from $r$, so it is never too small. The walk behind it is a path, since values at a node only decrease, so every value is at most $n - 1$. A node at distance $k$ gets the value $k$ from a neighbour at distance $k - 1$, by induction on $k$.

**Layered.** At the start of phase $k$ the tree is exactly the set of nodes at distance at most $k - 1$, with correct depths, and no message is in transit, since the root starts a phase only when the convergecast of the previous one is complete. A node joins in phase $k$ exactly if it is at distance $k$.

The [full proof](proofs/correctness/) gives every step of the three arguments, with the exact message counts and the time bounds.

## Complexity

All three forms are proved on the [proof page](proofs/correctness/); the other rows are cited.

| algorithm | model | time | messages |
|---|---|---|---|
| SYNC-BFS (this page) | synchronous | $e \le D$ rounds (last message by round $e + 1$) | exactly $2m - n + 1$ |
| Bellman-Ford form | asynchronous | at most $e + 1 \le D + 1$ | at most $\deg(r) + \sum_{v \ne r} (n - \mathrm{dist}(v))(\deg(v) - 1) = O(nm)$ |
| layered form | asynchronous | at most $(e + 1)(e + 2) = O(D^2)$ | exactly $2(2m - n + 1) + 2\sum_{k=1}^{e+1}(\lvert L_{\le k-1} \rvert - 1) = O(m + nD)$ |
| SYNC-BFS with the [α synchronizer](/synchronizer/) | asynchronous | $O(D)$ | $O(mD)$ |
| Awerbuch (1989), cited | asynchronous | $O(D^{1+\varepsilon})$ | $O(m^{1+\varepsilon})$ |

Here $L_{\le j}$ is the set of nodes at distance at most $j$. The time of the Bellman-Ford form assumes delays of at most one unit; many texts state it as $O(n)$, which also covers models in which local steps take time. The layered form trades messages for time: its messages are at most $4m + 2(e + 1)(n - 1)$.

**Lower bounds.** Every algorithm needs $e$ rounds, since a node at distance $e$ cannot learn anything about $r$ earlier, and $\Omega(m)$ messages in the setting of the [broadcast problem](/broadcast-problem/), since BFS solves broadcast. So SYNC-BFS is optimal in both measures up to constant factors, and the open question in the asynchronous model was how close to $O(D)$ time and $O(m)$ messages one can get at the same time. Awerbuch (1989) gave $O(D^{1+\varepsilon})$ time with $O(m^{1+\varepsilon})$ messages for every fixed $\varepsilon > 0$.

**Space.** A node stores its distance and its parent, $O(\log n)$ bits; the layered form adds the list of children and two counters.

## Properties

- **Deterministic** in all three forms.
- **Synchronous form needs no identifiers** and runs in the anonymous [port numbering](/port-numbering/) model.
- **CONGEST friendly.** Every message holds one distance or one phase number.
- **The Bellman-Ford form does not detect its own end.** Nodes keep values that may still change; the layered form ends with the root knowing that the tree is complete.
- **The layered form is a synchronizer in disguise.** Each phase is one synchronous round, simulated by a broadcast and a convergecast on the tree, the pattern of the [β synchronizer](/synchronizer/).

## Variants and improvements

- **Synchronizers.** Running SYNC-BFS under the α synchronizer gives $O(D)$ time and $O(m)$ extra messages per round, $O(mD)$ in total. The layered form is close to the β synchronizer, run on the part of the tree built so far, so each pulse costs $O(n)$ messages and time equal to the current depth. Awerbuch (1985) introduced the γ synchronizer to get costs between the two.
- **Strips.** A phase can grow the tree by a strip of $\ell$ layers, with Bellman-Ford corrections inside the strip and a convergecast at its end. With $\ell = 1$ this is the layered form, with $\ell = D$ it is Bellman-Ford, and values in between trade the two costs. Awerbuch and Gallager (1987) and Awerbuch (1989) refine this kind of trade-off into the near-optimal bounds.
- **Weighted edges.** With edge weights the same two ideas give [distributed Bellman-Ford](/distributed-bellman-ford/) and distributed forms of Dijkstra's algorithm; see [distributed shortest paths](/distributed-shortest-paths/).
- **Many sources.** BFS from $k$ sources at the same time runs in $O(k + D)$ rounds in the CONGEST model by pipelining, the basis of exact all-pairs shortest paths in $O(n)$ rounds on unweighted graphs.
- **Shared memory.** The parallel counterpart is level-synchronous [parallel BFS](/parallel-bfs/), in which a barrier plays the role of the round.

## When to use it

Use SYNC-BFS whenever rounds are synchronous: it is optimal and simple, and the BFS tree it leaves is the standard backbone for later [broadcasts and convergecasts](/convergecast/) of depth $e \le D$. In an asynchronous network, use the Bellman-Ford form when messages are cheap and latency matters, and the layered form when the graph is dense and $D$ is small, since its message count is $O(m)$ plus a term that does not depend on $m$. If only some spanning tree is needed, [flooding](/flooding/) or the [echo algorithm](/echo-algorithm/) is cheaper.

## Pitfalls

- **Treating the asynchronous flooding tree as a BFS tree.** In an asynchronous network the first copy can come along a long path; see the example above and the page on [distributed spanning trees](/distributed-spanning-tree/).
- **Carrying the weighted worst case over.** Asynchronous Bellman-Ford can send exponentially many messages on weighted graphs under bad schedules, but with unit weights each node changes its value at most $n - \mathrm{dist}(v)$ times, which gives the $O(nm)$ bound.
- **Starting a phase too early.** In the layered form, the root must wait for the convergecast; otherwise an EXPLORE of phase $k + 1$ can overtake one of phase $k$ and a node can join one layer too deep.
- **Counting rounds versus time.** The synchronous bound is in rounds; the asynchronous bounds are in time units with delays of at most 1. The two meet only through a [synchronizer](/synchronizer/).

## Implementations

## History

The synchronous algorithm is folklore and appears as SynchBFS in Lynch (1996). The asynchronous trade-off between the Bellman-Ford form and the layer by layer construction was studied in Gallager's report on minimum hop algorithms (1982), and Awerbuch (1985) used BFS as the main application of his synchronizers. Awerbuch and Gallager (1987) and then Awerbuch (1989) brought the asynchronous costs close to the lower bounds, $O(D^{1+\varepsilon})$ time with $O(m^{1+\varepsilon})$ messages. Peleg (2000, Chapter 5) presents the two classic forms under the names distributed Bellman-Ford and distributed Dijkstra.

## References
