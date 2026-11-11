---
tag: 9B51BZ
kind: algorithm
slug: hyparview
name: HyParView
aliases:
- hybrid partial view
- HyParView membership protocol
area: distributed/gossip
level: advanced
summary: Membership protocol with a small symmetric active view used for flooding and a larger passive view used to replace failed neighbours, so broadcast survives massive failures.
solves: [membership-management]
model: asynchronous-model
complexity:
  vars: {a: the active view size, q: the passive view size, r: the active random walk length}
  time: {worst: O(a r)}
  space: {extra: O(a + q)}
properties: {deterministic: false, recursive: false}
prereqs: [peer-sampling-service, gossip-protocol, cyclon]
see_also: [scamp, cyclon, membership-management, peer-sampling-service, epidemic-broadcast-tree, failure-detection, churn, lpbcast]
sources:
  - paper: doi:10.1109/DSN.2007.56
    title: João Leitão, José Pereira and Luís Rodrigues, HyParView, a membership protocol for reliable gossip-based broadcast, 37th IEEE/IFIP International Conference on Dependable Systems and Networks (DSN), 2007
    locator: pages 419 to 429 (the active and passive views, JOIN and FORWARDJOIN with the active and passive random walk lengths, DISCONNECT, NEIGHBOR requests with priorities, SHUFFLE, and the evaluation with up to 95 percent failed nodes)
  - paper: "João Leitão, José Pereira and Luís Rodrigues, Epidemic broadcast trees, 26th IEEE International Symposium on Reliable Distributed Systems (SRDS), 2007"
    locator: Plumtree, which builds a broadcast tree over the HyParView active view
---

HyParView (hybrid partial view) is a gossip membership protocol, from Leitão, Pereira and Rodrigues (2007), in which each node keeps two views: a small symmetric active view, the neighbours it floods messages to over open connections, and a larger passive view, a reserve of addresses used only to replace failed neighbours. Because the active view is used for every message, a crashed neighbour is found at once, and the node replaces it from the passive view. With an active view of 5 and a passive view of 30, broadcast reaches all live nodes even after most of the nodes crash at the same time.

## In plain words

Each computer has two lists. The short list holds a few neighbours that it talks to all the time, and the friendship goes both ways. The long list is a reserve of addresses that it does not use yet.

A message is sent to every neighbour on the short list, and each of them passes it on in the same way. Because the computers talk to their neighbours all the time, a crashed neighbour is noticed at once. The computer then takes an address from its reserve and asks that computer to become a new neighbour.

From time to time, computers swap some addresses of their reserves with far away computers, so that the reserves stay fresh and mixed. Even if most computers crash at once, the survivors find each other again through their reserves.

## The problem

Gossip broadcast over a partial view loses messages when views point to crashed nodes, and protocols such as [SCAMP](/scamp/) or [Cyclon](/cyclon/) remove such entries only slowly. They also need a large fanout, about $\ln n$ plus a margin, because each message goes to random view members that may be dead. The goal is a membership protocol that gives a connected overlay with small degree, keeps it connected after many simultaneous failures, and so allows a deterministic flood with fanout equal to the active view size. See [membership management](/membership-management/).

## The algorithm

Each node $p$ keeps an active view of at most $a$ nodes and a passive view of at most $q$ nodes, disjoint and without $p$. Active links are symmetric: $x$ is in the active view of $y$ exactly when $y$ is in the active view of $x$. The parameters are the active random walk length ARWL and the passive random walk length PRWL, with PRWL < ARWL, and the shuffle sizes $k_a$ and $k_p$.

```pseudo id=main
HYPARVIEW-JOIN(n, contact)
L1  ADD-ACTIVE(contact, n)
L2  the contact sends FORWARDJOIN(n, ARWL) to every other node of its active view
ON-FORWARDJOIN(n, ttl) at p, from sender
L3  if ttl = 0 or |active(p)| = 1 then ADD-ACTIVE(p, n) and stop
L4  if ttl = PRWL then add n to passive(p)
L5  send FORWARDJOIN(n, ttl − 1) to a random node of active(p) other than sender
ADD-ACTIVE(p, x), done on both sides
L6  if active(p) is full: remove a random node r, send DISCONNECT to r, and p and r put each other into their passive views
ON-FAILURE(p, x) when the link to the active neighbour x breaks
L7  remove x from active(p)
L8  repeat: send NEIGHBOR to a random r of passive(p), with high priority if active(p) is empty; r accepts if the priority is high or active(r) is not full; a dead r is removed from passive(p); until some r accepts
SHUFFLE(p), periodically
L9  send p, k_a nodes of active(p) and k_p nodes of passive(p) on a random walk of ARWL steps; the last node answers with as many nodes of its passive view; both add what they get to their passive views, evicting first the nodes they sent
```

When $r$ accepts a NEIGHBOR request, both nodes run ADD-ACTIVE and remove each other from their passive views. Adding a node to a full passive view removes a random entry. The paper uses $a = 5$ (fanout 4 plus one), a passive view of 30 entries, ARWL = 6, PRWL = 3, $k_a = 3$ and $k_p = 4$ for 10000 nodes.

**Broadcast.** A node that gets a message for the first time sends it to every node of its active view except the one it came from. A send over a broken link triggers line L7.

## Example

**A join.** Node $n$ joins through contact $c$, whose active view is $\{u, v, w\}$. Line L1 links $c$ and $n$. Line L2 sends FORWARDJOIN($n$, 6) to $u$, $v$ and $w$. Each of these walks takes six random steps over active views. At the step where ttl is 3, the current node puts $n$ into its passive view. At the end of each walk, the last node links to $n$, dropping a random neighbour into its passive view if its active view was full. So $n$ gets up to four active neighbours, and its address is in about three passive views.

**Massive failure.** The implementation builds an overlay of 1000 nodes with the paper's parameters, runs five shuffle rounds, and lets every node fill its active view. The mean active view is 4.97 and the mean passive view is 29.5. Then a random set of nodes crashes. Every live node detects its broken links, as an open TCP connection would show, and runs lines L7 and L8. The largest connected part of the live nodes, over three seeds:

| crashed | live | largest part before repair | largest part after one repair |
|---|---|---|---|
| 50 % | 500 | 467 to 470 | 498 to 500 |
| 70 % | 300 | 97 to 143 | 298 to 300 |
| 80 % | 200 | 10 to 26 | 200 |
| 90 % | 100 | 4 to 7 | 99 to 100 |
| 95 % | 50 | 3 to 4 | 39 to 43 |

After the repair, a flood from any live node reaches every node of the largest part. At 95 percent the passive views of some nodes hold no live node at all, and those nodes stay alone until a shuffle or a new join reaches them.

## Correctness

The proved claims are: the views stay valid (bounded, disjoint, without the owner); active links stay symmetric; a join gives the new node at least one active neighbour; when the repair of a node ends, its active view is not empty unless its passive view holds no live node, because a high priority request is always accepted; and after a repair round in which every live node checks its links, no live node has a crashed node in its active view. The full proof is below.

Connectivity of the whole live overlay after a massive failure is not proved. It is the result of the measurements in the paper and on this page.

## Complexity

- **Join.** At most $a - 1$ walks of ARWL steps, so $O(a \cdot \text{ARWL})$ messages.
- **Repair.** One NEIGHBOR request per tried passive node, so at most $q$ requests per failed link.
- **Shuffle.** One walk of ARWL steps and one answer with $k_a + k_p + 1$ entries.
- **Broadcast.** Each node sends each message to at most $a - 1$ neighbours, so a flood costs at most $(a - 1) n + 1$ messages. Only $n - 1$ of them bring the message to a node for the first time, so with $a = 5$ about three quarters are duplicates.
- **Space.** $O(a + q)$ entries per node.

## Properties

- **Symmetric active view.** Every link is a connection used in both directions, so a node knows who sends to it, and the overlay is an undirected graph with degree at most $a$.
- **Fast failure detection.** Active links carry every message, so a crashed neighbour is found at the first send, or by the transport layer. No separate [failure detector](/failure-detector/) is needed.
- **Deterministic flood.** Since the active view is small and accurate, a broadcast can be sent to all active neighbours instead of a random subset, and a tree protocol such as [epidemic broadcast trees](/epidemic-broadcast-tree/) can run on top.
- **Reserve for repair.** The passive view is kept fresh by the shuffle, which mixes it like [Cyclon](/cyclon/), so after a massive failure most nodes still find live replacements.

## Variants and improvements

- **Refill without failure.** The paper repairs the active view only when a link breaks. After a DISCONNECT, a node can be left with fewer than $a$ neighbours, and in rare cases with none. Many implementations, and the `refill` option of the implementation here, also refill an active view that is not full from the passive view.
- **Plumtree.** Epidemic broadcast trees use the HyParView active view as the base overlay and prune it to a spanning tree for payloads, keeping the other links for lazy announcements.
- **X-BOT and other optimizers.** Later protocols swap active neighbours to reduce latency or follow the network topology, keeping the passive view for repair.

## When to use it

Use HyParView when a group of hundreds to tens of thousands of nodes must broadcast reliably even under large failures, and nodes can keep a few open connections each. It is the membership layer of several gossip systems and of libraries such as Partisan for Erlang. If nodes cannot keep connections, or a uniform sample of the whole group is needed, a [peer sampling service](/peer-sampling-service/) such as [Cyclon](/cyclon/) fits better.

## Pitfalls

- **Too small a passive view.** After a large failure, a node whose passive view holds no live node cannot repair itself. The table shows this at 95 percent.
- **No shuffle.** Without the shuffle, passive views fill with the addresses seen at join time and get old, so they hold many dead nodes after churn.
- **Asymmetric links.** If only one side adds the other to its active view, the failure detection and the DISCONNECT logic break, and nodes with no inbound link appear.
- **Low priority loops.** A node with a non-empty active view sends low priority requests, which full nodes reject. It must stop after trying its passive view once, or it loops.

## Implementations

## History

Leitão, Pereira and Rodrigues presented HyParView at DSN 2007, with an evaluation in a simulator of 10000 nodes that compared it with [SCAMP](/scamp/) and [Cyclon](/cyclon/) under failures of up to 95 percent of the nodes. In the same year they presented epidemic broadcast trees (Plumtree), which build on the HyParView active view. The protocol was later used in Partisan, a distribution layer for Erlang, and in other gossip libraries.

## References
