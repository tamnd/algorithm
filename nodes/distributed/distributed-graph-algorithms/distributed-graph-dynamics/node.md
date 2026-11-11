---
tag: AN42TN
kind: concept
slug: distributed-graph-dynamics
name: Dynamic distributed graph algorithms
aliases:
- dynamic distributed networks
- T-interval connectivity
- distributed computation in dynamic networks
area: distributed/distributed-graph-algorithms
level: research
summary: Distributed algorithms for networks whose links change while they run, from adversarial change in every round (T-interval connectivity) to repair after single edge updates and self-stabilization.
prereqs: [local-model, congest-model, flooding]
see_also: [dynamic-graph, temporal-graph, dynamic-connectivity, fully-dynamic-graph, flooding, rumor-spreading-problem, broadcast-problem, local-model]
sources:
  - paper: doi:10.1145/1806689.1806760
    title: Fabian Kuhn, Nancy Lynch and Rotem Oshman, Distributed computation in dynamic networks, STOC 2010, 513-522
    locator: Definition of T-interval connectivity (Section 2), one-token dissemination in n - 1 rounds (Proposition 3.1), counting and all-to-all token dissemination in O(n^2) rounds (Corollary 5.2), the speed-up for T-interval connected graphs (Section 6), and the lower bounds for token forwarding (Theorems 8.1 and 8.2)
  - paper: doi:10.1145/361179.361202
    title: Edsger W. Dijkstra, Self-stabilizing systems in spite of distributed control, Communications of the ACM 17(11), 643-644, 1974
    locator: the notion of a self-stabilizing system and token rings that reach a legal state from any state
  - paper: doi:10.1007/BF02278851
    title: Shlomi Dolev, Amos Israeli and Shlomo Moran, Self-stabilization of dynamic systems assuming only read/write atomicity, Distributed Computing 7(1), 3-16, 1993
    locator: self-stabilizing construction of a BFS spanning tree in a network whose topology can change
  - paper: doi:10.1109/SFCS.1987.7
    title: Yehuda Afek, Baruch Awerbuch and Eli Gafni, Applying static network protocols to dynamic networks, FOCS 1987, 358-370
    locator: the reset method that reruns a static protocol after topology changes
---

Dynamic distributed graph algorithms run on networks whose links change while the computation is going on. Mobile and wireless networks, peer-to-peer overlays and networks with failing links all behave this way. Unlike the [LOCAL](/local-model/) and [CONGEST](/congest-model/) models, where the graph is fixed, here the graph is a sequence of graphs, one per round, and the algorithm must be correct whatever the sequence is, within some guarantee of stability. There are three main views. In the *adversarial* view, an adversary may change all links in every round, and the guarantee is *T-interval connectivity* (Kuhn, Lynch and Oshman 2010): every $T$ consecutive rounds share a connected spanning subgraph. In the *update* view, changes are rare single edge insertions or deletions, and the algorithm repairs its output with few rounds and messages per change. In the *self-stabilization* view (Dijkstra 1974), the algorithm reaches a correct state from any state, so it recovers by itself after any change. The [dynamic graph](/dynamic-graph/) pages treat the different, centralized question of a data structure that is updated when the graph changes.

## In plain words

Picture people who move around and can only talk to whoever is near them at the moment. Who is near changes all the time, and nobody knows in advance who will be near next.

Can they still share news? If at every moment the group is linked up in some way, then each piece of news reaches at least one new person per step, so everyone hears it after as many steps as there are people, less one.

If the links stay put a little longer, news can travel in a stream, and many pieces can be shared faster.

A second view is a network that rarely changes, where the task is to fix the answer after each change. A third is a system that recovers by itself from any bad state.

## The idea

**Model of Kuhn, Lynch and Oshman (2010).** A fixed set of $n$ nodes with unique identifiers runs in synchronous rounds without failures. A *dynamic graph* is a sequence $G(1), G(2), \dots$ of undirected graphs on the same nodes; in round $r$ the links are the edges of $G(r)$. An adversary chooses $G(r)$ at the start of round $r$ and may look at the state of all nodes (it is *adaptive*). In each round a node *broadcasts* one message to all its current neighbours without knowing who they are, then receives their messages. Messages have $O(\log n)$ bits plus the size of one input. The diameter $D$ of a single $G(r)$ says little; the role of $D$ is played by how fast influence spreads over time, which is at most $n - 1$ rounds below.

**T-interval connectivity.** The dynamic graph is *$T$-interval connected* if for every $r \ge 1$ the graph $\left(V, \bigcap_{i=r}^{r+T-1} E(i)\right)$ is connected. For $T = 1$ this means every $G(r)$ is connected, and the graphs may differ arbitrarily from round to round. Larger $T$ means a connected spanning subgraph that is stable for $T$ rounds, although the other edges still change.

**Token dissemination.** In *$k$-token dissemination*, $k$ tokens start at some nodes and every node must learn all of them; *$n$-gossip*, or all-to-all dissemination, is the case where each node starts with its own token. *Counting* asks every node to learn $n$.

**One token, proved here.** Let every node that knows a token broadcast it in every round. On a 1-interval connected graph, in every round in which some node does not know the token, $G(r)$ is connected, so some edge joins a node that knows it to one that does not, and that node learns it. So the number of knowers grows by at least 1 per round, and all $n$ nodes know the token after at most $n - 1$ rounds (Kuhn, Lynch and Oshman 2010, Proposition 3.1). The bound is tight: if in every round $G(r)$ is a path that lists all knowers first, exactly one node learns the token per round, and $n - 1$ rounds are needed. The adversary is adaptive, and $D(G(r)) = n - 1$ in every round.

**Many tokens, proved here.** Suppose the nodes know $n$ and the number $k$ of tokens, and the tokens are ordered. Each node $v$ keeps the set $A_v$ of tokens it knows and a set $F_v$ of *finished* tokens. The algorithm runs $k$ phases of $n - 1$ rounds. In every round of a phase, $v$ broadcasts $\min(A_v \setminus F_v)$, if that set is not empty. At the end of the phase, $v$ adds $\min(A_v \setminus F_v)$ to $F_v$.

*Claim.* On every 1-interval connected dynamic graph, after phase $j$ every node knows the $j$ smallest tokens $\tau_1 < \dots < \tau_j$ and has $F_v = \{\tau_1, \dots, \tau_j\}$. *Proof.* By induction on $j$; for $j = 0$ all $F_v$ are empty. In phase $j$, all $F_v$ equal $\{\tau_1, \dots, \tau_{j-1}\}$, so for every node that knows $\tau_j$, the token $\tau_j$ is the smallest element of $A_v \setminus F_v$, and the node broadcasts it in every round of the phase. As in the one-token argument, the number of nodes that know $\tau_j$ grows by at least one per round while it is below $n$, so after $n - 1$ rounds all nodes know it. Then $\tau_j$ is the smallest unfinished token at every node, so every node adds exactly $\tau_j$ to $F_v$. ∎

So $k$-token dissemination takes at most $k(n - 1)$ rounds with messages of one token each, and $n$-gossip takes at most $n(n - 1) = O(n^2)$ rounds.

**Known results (cited, Kuhn, Lynch and Oshman 2010).**

- On 1-interval connected graphs, counting and $n$-gossip take $O(n^2)$ rounds even when $n$ is not known, with messages of $O(\log n)$ bits plus one input; hence every computable function of the inputs is computed in $O(n^2)$ rounds (Corollary 5.2 and the abstract).
- If the graph is $2T$-interval connected, a phase of $2T$ rounds in which each node broadcasts the smallest token it has not yet sent in that phase lets the $T$ smallest tokens advance together along the stable subgraph; after $\lceil n/T \rceil$ such phases all nodes know the $T$ smallest tokens. This gives counting and all-to-all dissemination in $O(n + n^2/T)$ rounds for known $T$, and $O(\min\{n^2, n \log n + n^2 \log n / T\})$ rounds for unknown $T$ (Section 6).
- Every deterministic *centralized* token-forwarding algorithm, which may choose each node's broadcast with knowledge of the whole state, needs $\Omega(n \log k)$ rounds for $k$-token dissemination on 1-interval connected graphs (Theorem 8.1).
- Every *knowledge-based* token-forwarding algorithm, whose choice at a node depends only on the tokens it has known so far, needs $\Omega(n + nk/T)$ rounds on $T$-interval connected graphs (Theorem 8.2). So the $O(n^2)$ bound for $k = n$ and $T = 1$ is tight for this class.

**Updates.** When changes are rare, the measures are the rounds and messages needed to restore a correct output after one change, often compared with recomputing from scratch. Afek, Awerbuch and Gafni (1987) gave a general *reset* method that turns a protocol for static networks into one for dynamic networks by restarting it in a controlled way after each change. Later work bounds the number of nodes whose output must change after one update, for example $O(1)$ in expectation for a [maximal independent set](/distributed-mis/) with a suitable random order.

**Self-stabilization.** An algorithm is *self-stabilizing* if, from any initial state of all nodes and channels, it reaches a legal state in finite time and stays legal while no fault happens (Dijkstra 1974). Such an algorithm recovers from any change of the topology by itself: once the changes stop, it stabilizes on the new graph. A simple example is a self-stabilizing [BFS](/breadth-first-search-distributed/) tree (Dolev, Israeli and Moran 1993 treat the harder case of read and write atomicity): the root keeps $d = 0$ and every other node repeatedly sets $d_v = 1 + \min_w d_w$ over its neighbours. *Sketch, in synchronous rounds from any non-negative values:* by induction, after round $k$ every node has $d_v \ge \min(\mathrm{dist}(v), k)$, and every node with $\mathrm{dist}(v) < k$ has $d_v = \mathrm{dist}(v)$; so all values are correct after $D + 1$ rounds, where $D$ is the diameter of the final graph.

## Examples

**The knowers-first path.** In every round the adversary lines up the nodes on a path, with all nodes that know the token first. Each $G(r)$ is connected, so the dynamic graph is 1-interval connected, but only the last knower has an edge to a new node. Flooding takes exactly $n - 1$ rounds, although in a fixed path with the token in the middle it would take $\lceil (n-1)/2 \rceil$. The tests check this for $n$ up to 15.

**Blocks of stable trees.** Cut the rounds into blocks of $T$, choose a spanning tree $S_b$ for each block $b$, and let every round of block $b$ contain $S_b \cup S_{b+1}$ plus random edges. A window of $T$ consecutive rounds meets at most two blocks $b$ and $b + 1$, and all its rounds contain $S_{b+1}$, so the sequence is $T$-interval connected. The tests check this with a brute-force checker and use such sequences for the pipelined algorithm with $2T$-interval connectivity.

**n-gossip.** With $n = 4$ and tokens $3 < 5 < 8 < 9$, one at each node, the phased algorithm spends phase 1 (3 rounds) on token 3, phase 2 on token 5, and so on; after 12 rounds every node knows all four tokens. The tests check, for each $j$, that after phase $j$ every node has finished exactly the $j$ smallest tokens, against several adaptive adversaries and random 1-interval connected sequences.

**Random versus adversarial change.** If links change at random, as in the [random phone call model](/random-phone-call-model/) of [rumor spreading](/rumor-spreading-problem/), one rumor reaches all nodes in $O(\log n)$ rounds with high probability. The $n - 1$ bound above is the price of a worst-case adversary.

## Where it is used

- **Mobile and wireless networks.** Ad hoc and vehicular networks have links that appear and disappear with motion and interference; T-interval connectivity is a worst-case model for them, and token dissemination is their basic task.
- **Temporal graphs.** A dynamic graph is a [temporal graph](/temporal-graph/): journeys that respect time replace paths, and the time for one token to spread is a temporal diameter.
- **Self-stabilizing systems.** Network protocols that must recover from arbitrary faults, such as spanning tree and routing protocols, use self-stabilization.
- **Repair of distributed structures.** Overlays, spanning trees, matchings and independent sets maintained under churn and link failures use the update view, related to [fully dynamic](/fully-dynamic-graph/) data structures such as [dynamic connectivity](/dynamic-connectivity/) on the centralized side.
- **Broadcast and gossip.** [Broadcast](/broadcast-problem/) and [flooding](/flooding/) in a changing network are the one-token case.

## References
