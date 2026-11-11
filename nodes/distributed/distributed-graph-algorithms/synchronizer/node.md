---
tag: S5XWV5
kind: technique
slug: synchronizer
name: Synchronizer
aliases:
- alpha synchronizer
- beta synchronizer
- gamma synchronizer
- Awerbuch synchronizer
- network synchronizer
area: distributed/distributed-graph-algorithms
level: core
summary: Runs a synchronous algorithm on an asynchronous network by generating pulses. Per pulse, α costs O(m) messages and O(1) time, β O(n) and O(n), γ O(kn) and O(log_k n).
prereqs: [synchronous-model, asynchronous-model, convergecast, distributed-spanning-tree, round-complexity, message-complexity]
see_also: [breadth-first-search-distributed, convergecast, distributed-spanning-tree, low-diameter-decomposition, network-decomposition, sparse-neighborhood-cover, barrier-synchronization, bsp-model]
sources:
  - paper: doi:10.1145/4221.4227
    title: Baruch Awerbuch, Complexity of network synchronization, Journal of the ACM 32(4), 804-823, 1985
    locator: the synchronizers α, β and γ, their costs per pulse, the partition algorithm for γ, and the lower bound on the trade-off
  - book: isbn:9780898714647
    title: David Peleg, Distributed Computing, A Locality-Sensitive Approach, SIAM, 2000
    locator: Chapter 6 (synchronizers α, β and γ, and their analysis)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 16 (synchronizers, the local synchronizer and the safe synchronizers α, β and γ)
  - paper: doi:10.1109/FSCS.1990.89572
    title: Baruch Awerbuch and David Peleg, Network synchronization with polylogarithmic overhead, Proceedings of the 31st IEEE Symposium on Foundations of Computer Science (FOCS), 514-522, 1990
    locator: synchronizers with polylogarithmic time and message overheads per pulse, with sparse covers
---

A synchronizer lets an algorithm written for the [synchronous model](/synchronous-model/) run unchanged on an [asynchronous network](/asynchronous-model/). It gives every node a sequence of *pulses* that stand for the rounds, and it guarantees that a node starts pulse $p + 1$ only after all messages that the algorithm sent to it in pulse $p$ have arrived. Awerbuch (1985) gave three synchronizers. **α** checks this with each neighbour, at a cost of $O(m)$ messages and $O(1)$ time per pulse. **β** checks it through a rooted spanning tree, at a cost of $O(n)$ messages and $O(h)$ time per pulse, $h$ the height of the tree. **γ** combines the two on a partition into clusters, and for a parameter $k \ge 2$ costs $O(kn)$ messages and $O(\log_k n)$ time per pulse.

## In plain words

A band plays together because a conductor sets the beat. Without a conductor, each musician must not play the next bar before the bar of every neighbour has reached them.

One way: every musician tells each neighbour "I am done with this bar" and waits until all neighbours have said the same. That is quick but needs a lot of talking.

Another way: musicians report up a chain of section leaders to one leader, who then says "next bar" to everyone down the chain. That needs little talking but takes longer when the chain is long.

A mixed way uses small groups with a leader each, and leaders talk only to nearby leaders.

## When it applies

- **The algorithm is synchronous and failure free.** It proceeds in rounds: send, receive, compute. Synchronizers do not tolerate crashes; with failures, synchrony cannot be simulated in general, which is the content of results such as the [FLP impossibility](/flp-impossibility/).
- **The network is asynchronous and reliable.** Messages arrive after finite, unknown delays. Channels need not be FIFO. For time bounds, each delay is at most one unit.
- **Messages can be tagged.** Each message carries its pulse number modulo a small constant, and an acknowledgement is sent for each message.
- **Some preprocessing is allowed.** β needs a rooted spanning tree and γ a cluster partition. Their construction is a one-time cost, paid before the first pulse.
- **Cost model.** A synchronous algorithm with $T$ rounds and $M_S$ messages runs, with a synchronizer of message overhead $C_p$ and time overhead $T_p$ per pulse, in $O(T \cdot T_p)$ time with $M_S + O(T \cdot C_p)$ messages, plus the initialization.

## The template

```pseudo id=main
SYNCHRONIZER-α(v)                          ▷ runs the synchronous algorithm A at node v
L1  start of pulse p: run the sending step of round p of A; send each message x as ⟨p, x⟩; safe ← false
L2  on receipt of ⟨q, x⟩ from u: store (u, x) for pulse q; send ACK to u
L3  when every message of pulse p has been acknowledged: safe ← true; send SAFE(p) to every neighbour
L4  when safe and SAFE(p) has arrived from every neighbour:
L5      give A the stored messages of pulse p, run its round p step, and start pulse p + 1
```

A node is *safe* for pulse $p$ when all the messages it sent in pulse $p$ have arrived. Line L4 waits until the node and all its neighbours are safe.

**β, on a rooted spanning tree of height $h$.** Lines L1 to L3 stay, except that SAFE is not sent to the neighbours. Instead, a node that is safe and has received SUBTREE-SAFE($p$) from all its children sends SUBTREE-SAFE($p$) to its parent. When the root is safe and all its children have reported, it sends PULSE($p$) down the tree, and every node that receives it forwards it to its children and runs line L5.

**Correctness of α.** (1) *Nothing is missed.* Suppose $v$ runs line L5 for pulse $p$, and let $u$ have sent $x$ to $v$ in pulse $p$; then $u$ is a neighbour of $v$. Since $v$ has SAFE($p$) from $u$, all messages of $u$ in pulse $p$ have been acknowledged, and an ACK is sent only on arrival (line L2). So $x$ is stored at $v$. (2) *Nothing extra is used.* Messages are stored by their tag, so a message of pulse $p + 1$ that arrives early is kept for later. (3) *Same run as the synchronous one.* By induction on $p$, at the start of pulse $p$ every node of the simulation is in the state it has after round $p - 1$ of the synchronous run, because by (1) and (2) its round $p - 1$ step got exactly the same messages. (4) *Progress.* If all nodes start pulse $p$, all messages of pulse $p$ arrive and are acknowledged, all nodes become safe and send SAFE($p$), and these arrive, so all nodes start pulse $p + 1$. (5) *Small buffers.* A node starts pulse $p + 1$ only after SAFE($p$) from all neighbours, which they send in pulse $p$; so the pulses of two neighbours differ by at most 1, and a node stores messages of two pulses at most.

**Costs of α.** Each message of $A$ gets one ACK, which is $M_S$ messages in total. In each pulse each node sends SAFE on each edge, $2m$ messages per pulse. With delays of at most one unit, let $t_v(p)$ be the time at which $v$ starts pulse $p$. Its messages arrive by $t_v(p) + 1$, the ACKs return by $t_v(p) + 2$, and its SAFE($p$) messages arrive by $t_v(p) + 3$. So $t_v(p + 1) \le \max_{u \in N[v]} t_u(p) + 3$, where $N[v]$ is $v$ together with its neighbours. If all nodes start at time 0, every node finishes pulse $P$ by time $3P$.

**Correctness of β.** By induction up the tree, when $v$ sends SUBTREE-SAFE($p$), every node in its subtree is safe for $p$. So when the root sends PULSE($p$), every node of the network is safe, and every message of pulse $p$ has arrived at its destination. Steps (2) to (4) of the α proof apply unchanged. A neighbour can start pulse $p + 1$ and send to $v$ before PULSE($p$) reaches $v$; the tag keeps that message apart.

**Costs of β.** One ACK per message of $A$, $M_S$ in total. Per pulse, SUBTREE-SAFE crosses each tree edge once and PULSE crosses each tree edge once: $2(n - 1)$ messages. For time, let $S(p)$ be the time at which the root sends PULSE($p$). Every node gets it by $S(p) + h$, starts pulse $p + 1$ and is safe by $S(p) + h + 2$, and the reports climb $h$ levels, so $S(p + 1) \le S(p) + 2h + 2$. With all nodes starting pulse 1 at time 0, $S(1) \le h + 2$, and all nodes finish pulse $P$ by time $P(2h + 2)$. On a BFS tree $h \le D$, and in general $h \le n - 1$.

**γ, on a cluster partition (cited).** Awerbuch (1985) partitions the nodes into clusters, each with a rooted spanning tree inside it, and chooses one *preferred edge* between each pair of neighbouring clusters. In each pulse, γ runs β inside every cluster; then neighbouring clusters exchange "cluster safe" over the preferred edges; then a second convergecast and broadcast in each cluster lets every node start the next pulse. The partition is built by growing one cluster at a time in BFS layers from an unclustered node: a new layer is added while it multiplies the size of the cluster by at least $k$, and the cluster stops at the first layer that does not. So the depth of every cluster tree is at most $\log_k n$, and the nodes just outside a cluster number less than $(k - 1)$ times its size, which bounds the number of preferred edges by $kn$ in total. The costs per pulse are $O(kn)$ messages and $O(\log_k n)$ time.

## Classic examples

**Synchronous BFS on an asynchronous network.** Synchronous [BFS](/breadth-first-search-distributed/) takes $D$ rounds and $O(m)$ messages. Under α it takes $O(D)$ time and $O(mD)$ messages; under β with a given tree of height $h$, $O(hD)$ time and $O(m + nD)$ messages, close to the layered BFS algorithm, which is in effect β on the part of the tree built so far. Awerbuch (1985) used this example to motivate γ.

**Local algorithms.** An algorithm of the [LOCAL model](/local-model/) or the [CONGEST model](/congest-model/) that runs in $T$ rounds, such as a coloring or a maximal independent set algorithm, runs under α in $O(T)$ time on any asynchronous network. The message cost is the reason to use β or γ instead.

**A comparison on the complete graph.** On $K_n$ with $P$ pulses of an algorithm that sends on every edge in every round, α adds $n(n - 1)P$ SAFE messages, while β on a star tree adds $2(n - 1)P$ messages and takes about $4$ time units per pulse. On a path, β on the path itself needs about $2n$ time units per pulse, while α needs 3.

## Variations

- **Synchronizers with polylogarithmic overheads.** Awerbuch and Peleg (1990) use sparse covers to get synchronizers whose time and message overheads per pulse are both polylogarithmic in $n$, at the price of more memory and a more complex initialization; see [sparse neighbourhood covers](/sparse-neighborhood-cover/) and [network decomposition](/network-decomposition/).
- **Lower bound on the trade-off.** Awerbuch (1985) also shows that on some graphs no synchronizer can have both a much smaller time overhead and a much smaller message overhead than γ.
- **Local synchronizers without acknowledgements.** If each node sends a message on every edge in every round (empty messages are allowed), a node can start pulse $p + 1$ when it has one pulse $p$ message from each neighbour. This is Lynch's local synchronizer; it costs $2m$ messages per pulse and needs no ACKs.
- **Synchronizers in shared memory.** The same idea is a [barrier](/barrier-synchronization/), and a superstep of the [BSP model](/bsp-model/) is a round ended by a global barrier.
- **Partial synchrony.** If delays have a known upper bound, a node can simply wait that long. This is not a synchronizer in the strict sense and fails when the bound is wrong.

## Pitfalls

- **Advancing on silence.** A node that has heard nothing from a neighbour does not know whether a message is on its way. Without the SAFE messages (or a message on every edge), the simulation can lose messages.
- **Forgetting the pulse tag.** A fast neighbour can be one pulse ahead. Without tags, its message of pulse $p + 1$ would be used in pulse $p$.
- **Counting the overhead per algorithm message.** α costs $2m$ messages per pulse even in pulses in which the algorithm sends nothing, for example in long quiet phases. β or γ is cheaper for such algorithms.
- **Ignoring initialization.** β and γ need a tree or a partition, which costs messages and time to build and must be counted when the algorithm runs only once.
- **Expecting fault tolerance.** One crashed node blocks α at all its neighbours and β at the whole network.

## Exercises

1. Show that under α the pulse numbers of any two nodes at distance $d$ differ by at most $d$.
2. Give the exact message overhead of α and β for an algorithm that runs $P$ pulses and sends $M_S$ messages, and decide which is smaller on a grid of $\sqrt{n} \times \sqrt{n}$ nodes.
3. Explain why α needs the acknowledgements. Construct a schedule in which a node without them starts pulse $p + 1$ before a pulse $p$ message has arrived.
4. Prove that the cluster growth rule of γ gives cluster trees of depth at most $\log_k n$.
5. A synchronous algorithm sends a message on every edge in every round. Show that it needs neither ACK nor SAFE messages to run asynchronously, and state the time per pulse.
6. Under β, why may a node acknowledge a message of pulse $p + 1$ before it has received PULSE($p$)?

## References
