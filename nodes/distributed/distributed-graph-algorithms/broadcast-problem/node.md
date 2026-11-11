---
tag: MVTY8K
kind: problem
slug: broadcast-problem
name: Broadcast problem
aliases:
- single-source broadcast
- one-to-all broadcast
- information dissemination from one source
area: distributed/distributed-graph-algorithms
level: intro
summary: Deliver a message from one source to every node of a connected network. Needs Ω(D) rounds, and Ω(m) messages when nodes know only their ports; a spanning tree cuts it to n − 1.
prereqs: [synchronous-model, asynchronous-model, message-complexity, round-complexity]
see_also: [flooding, echo-algorithm, distributed-spanning-tree, convergecast, rumor-spreading-problem, byzantine-reliable-broadcast, message-complexity, breadth-first-search]
sources:
  - paper: doi:10.1145/77600.77618
    title: Baruch Awerbuch, Oded Goldreich, David Peleg and Ronen Vainish, A trade-off between information and communication in broadcast protocols, Journal of the ACM 37(2), 238-256, 1990
    locator: the knowledge levels KT0, KT1 and KT-ρ, the Ω(m) message lower bound for broadcast in KT1 for restricted algorithms, and the matching upper bounds
  - paper: doi:10.1145/2699440
    title: Shay Kutten, Gopal Pandurangan, David Peleg, Peter Robinson and Amitabh Trehan, On the complexity of universal leader election, Journal of the ACM 62(1), Article 7, 2015
    locator: the Ω(m) message lower bound for broadcast in KT0 that also holds for randomized algorithms
  - book: isbn:9780898714647
    title: David Peleg, Distributed Computing, A Locality-Sensitive Approach, SIAM, 2000
    locator: Chapter 3 (broadcast and convergecast, lower bounds on time and messages, broadcast on a tree)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 2, Sections 2.2 and 2.3 (broadcast on a spanning tree, flooding)
---

In the broadcast problem, one node of a network, the source, holds a message, and every other node must receive it, using only messages along the edges. It is the most basic task of distributed computing and the first one on which the two cost measures of a network, [rounds](/round-complexity/) and [messages](/message-complexity/), are compared. Two simple facts frame it. A node at distance $d$ from the source cannot get the message before round $d$, so $\Omega(D)$ rounds are needed in the worst case. And if nodes know only their own ports, every correct algorithm must send a message across every edge, so $m$ messages are needed; [flooding](/flooding/) gets both bounds within a factor of 2. A known [spanning tree](/distributed-spanning-tree/) brings the message count down to $n - 1$.

## In plain words

One person in a group has news, and everybody must hear it. People can only pass notes to the people they know directly.

The news cannot travel faster than one step of acquaintance at a time, so people far from the start hear it late.

If nobody knows who knows whom, then each person who has the news must try every acquaintance, because any one of them might be the only way to reach some other group. So about one note per acquaintance pair is needed. If a fixed chain of contact is already agreed, one note per person is enough.

## Definition

**Model.** A connected undirected graph $G = (V, E)$ with $n$ nodes, $m$ edges, diameter $D$ and maximum degree $\Delta$. Each edge is a reliable channel in both directions; there are no failures. Timing is [synchronous](/synchronous-model/) or [asynchronous](/asynchronous-model/).

**Knowledge.** The standard levels are those of Awerbuch, Goldreich, Peleg and Vainish (1990). In **KT0** a node knows its own identifier and its ports, but not the identifiers at the other ends of its ports. In **KT1** a node also knows the identifier of each neighbour. In **KT-ρ** a node knows the graph within distance $\rho$ of itself. Anonymous networks, with ports and no identifiers, are weaker than KT0; see [port numbering](/port-numbering/).

**Input.** A source $s$ holds a message $M$. Only $s$ starts; any other node does nothing until it receives a message (no spontaneous wake up).

**Output.** Every node receives $M$. The run must terminate: from some point on no message is sent. A stronger form also asks that $s$ learns that every node has $M$ (acknowledged broadcast).

**Costs.** Messages; rounds or time with delays of at most one unit.

## Variants

- **Acknowledged broadcast.** The source must learn that the broadcast is complete. The [echo algorithm](/echo-algorithm/) and broadcast followed by [convergecast](/convergecast/) solve it.
- **Broadcast on a known tree.** A spanning tree is part of the input; the cost is $n - 1$ messages and the height of the tree in rounds.
- **Multi-message broadcast.** The source has $k$ messages; in the [CONGEST model](/congest-model/) pipelining on a BFS tree delivers them in $O(k + D)$ rounds.
- **Gossip, or all-to-all broadcast.** Every node has a message for all. In a static network this is $n$ broadcasts; in [dynamic networks](/distributed-graph-dynamics/) it is the token dissemination problem.
- **Rumour spreading.** Each node calls one random neighbour per round; see the [rumour spreading problem](/rumor-spreading-problem/).
- **Fault tolerant broadcast.** With crashed or Byzantine nodes, the problem becomes [reliable broadcast](/byzantine-reliable-broadcast/), with an agreement requirement instead of reachability.
- **Radio networks.** A node hears a message only if exactly one neighbour sends in that round, which changes both bounds.

## Examples

**Flooding.** On the graph with edges $\{0,1\}, \{0,2\}, \{1,2\}, \{1,3\}, \{2,4\}, \{3,4\}, \{4,5\}$ and source 0, [flooding](/flooding/) reaches nodes $1, 2$ in round 1, $3, 4$ in round 2 and $5$ in round 3, with $2m - n + 1 = 9$ messages. Each edge carries at least one message.

**Tree broadcast.** On the same graph with the tree $\{0,1\}, \{0,2\}, \{1,3\}, \{2,4\}, \{4,5\}$ known in advance, the source sends to 1 and 2, they send to their children, and so on: $5 = n - 1$ messages in 3 rounds.

**Why the edges between 1 and 2 matter.** In the tree broadcast, edge $\{1,2\}$ carries nothing, which is fine because the tree is known. Without the tree, nodes 1 and 2 cannot know that the other end of their shared port is already informed, and the lower bound below shows that some message must cross it.

## Known algorithms

| algorithm | knowledge | messages | rounds or time |
|---|---|---|---|
| [flooding](/flooding/) | ports only | exactly $2m - n + 1$ | $e \le D$ |
| [echo algorithm](/echo-algorithm/) | ports only, acknowledged | exactly $2m$ | at most $2e + 1$ rounds; $O(n)$ time |
| broadcast on a known spanning tree | a tree | exactly $n - 1$ | the height of the tree, $e$ on a BFS tree |
| depth-first token carrying the set of visited nodes | KT1 | $2(n - 1)$ | $2(n - 1)$ |
| Awerbuch, Goldreich, Peleg and Vainish (1990), cited | KT-ρ | $O(\min\{m, n^{1 + c/\rho}\})$ for a constant $c$ | not the point of the result |
| King, Kutten and Thorup (2015), cited | KT1, randomized | $\tilde O(n)$ | not the point of the result |

Here $e$ is the eccentricity of the source. The first three rows are proved on their pages.

## Bounds

**Rounds and time (proved).** Every algorithm needs at least $\mathrm{dist}(s, v)$ rounds to inform $v$, since a message moves at most one edge per round; so $e$ rounds, and $D$ for the worst source up to a factor of 2. In the asynchronous model, delays of exactly one unit give the same bound in time.

**Messages in KT0 (proved here for deterministic algorithms).** Assume: KT0 knowledge; nodes do not know $n$, $m$ or the graph; only $s$ starts; identifiers are distinct and come from a set with more than $2n$ values; the algorithm is deterministic and correct on every connected graph. Then in every execution on every connected graph $G$, every edge carries at least one message, so at least $m$ messages are sent.

*Proof.* Fix $G$, $s$ and an execution $\mathcal{E}$, and suppose no message crosses the edge $e = \{u, v\}$, using port $p$ at $u$ and port $q$ at $v$. If $e$ is a bridge, the side of $G - e$ without $s$ is nonempty and its nodes are reached only through $e$, so they never receive $M$, a contradiction. Otherwise build $G'$: take $G$ and a copy $G^*$ of it with new identifiers, remove $e$ and its copy $\{u^*, v^*\}$, and add the edges $\{u, v^*\}$ (on port $p$ of $u$ and port $q$ of $v^*$) and $\{u^*, v\}$ (on port $p$ of $u^*$ and port $q$ of $v$). Since $e$ is not a bridge, $G - e$ and $G^* - e^*$ are connected, and $G'$ is connected. Every node of $G'$ has the same identifier, degree and ports as its original, and in KT0 that is all it knows at the start. Run the algorithm on $G'$ with source $s$ and the delays of $\mathcal{E}$ on the edges of the first copy. By induction on events, the nodes of the first copy do exactly what they do in $\mathcal{E}$: they receive the same messages, on the same ports, at the same times. In $\mathcal{E}$ no message leaves $u$ on port $p$ or $v$ on port $q$, so in $G'$ no message crosses the two new edges, the nodes of $G^*$ never wake up, and they never receive $M$. This contradicts the correctness on $G'$. ∎

The hypotheses matter. If nodes knew $n$, the nodes of the first copy could tell $G$ from $G'$ in some cases. If nodes knew their neighbours' identifiers (KT1), the swap would change what $u$ and $v$ know.

**Messages in KT0 for randomized algorithms (cited).** Kutten, Pandurangan, Peleg, Robinson and Trehan (2015) show that $\Omega(m)$ expected messages are needed in KT0 also by randomized algorithms, in both timing models.

**Messages in KT1 (cited).** Awerbuch, Goldreich, Peleg and Vainish (1990) prove $\Omega(m)$ messages in synchronous KT1 networks for algorithms whose messages carry a constant number of identifiers and only compare identifiers, and for general deterministic algorithms when identifiers come from a very large set. The restrictions are needed: King, Kutten and Thorup (2015) broadcast in KT1 with $\tilde O(n)$ messages by computing with identifiers, and the depth-first token in the table uses $O(n)$ messages that carry long lists. The same paper gives $O(\min\{m, n^{1 + c/\rho}\})$ messages in KT-ρ, which explains the title: more knowledge, fewer messages.

**With a tree.** With a known spanning tree, $n - 1$ messages are needed and enough, since each node other than $s$ must receive at least one message.

## Reductions

- **Broadcast and spanning tree.** The first messages of flooding define a [spanning tree](/distributed-spanning-tree/); a spanning tree gives a broadcast with $n - 1$ messages. So the broadcast lower bounds apply to spanning tree construction from a root.
- **Broadcast and BFS.** A synchronous [distributed BFS](/breadth-first-search-distributed/) is a broadcast of a counter, and every broadcast algorithm solves the reachability part of BFS.
- **Broadcast in leader election.** Many election algorithms, such as [FloodMax](/floodmax/), are $n$ broadcasts that compete, and the KT0 message bound for broadcast gives $\Omega(m)$ for them.
- **Acknowledged broadcast and termination.** Acknowledged broadcast is the special case of [termination detection](/termination-detection/) for a computation that is itself a broadcast.

## Applications

- **Network wide announcements.** Link state routing floods each change of a link to all routers with sequence numbers.
- **Start signals.** A broadcast starts a distributed algorithm at all nodes, or tells all nodes a global value such as $n$ or a leader identifier.
- **Phases of other algorithms.** Distributed BFS by layers, the [β synchronizer](/synchronizer/), and MST algorithms use broadcast and convergecast on a tree in every phase.

## References
