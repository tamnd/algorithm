---
tag: T9HDCH
kind: technique
slug: convergecast
name: Convergecast
aliases:
- tree aggregation
- upward aggregation
- upcast
area: distributed/distributed-graph-algorithms
level: intro
summary: Values flow from the leaves of a rooted tree to the root and are combined at each node. Exactly n − 1 messages and as many rounds as the tree is deep; it pairs with a broadcast.
prereqs: [distributed-spanning-tree, broadcast-problem, synchronous-model, asynchronous-model]
see_also: [echo-algorithm, flooding, distributed-spanning-tree, breadth-first-search-distributed, synchronizer, dijkstra-scholten, gossip-aggregation, parallel-reduction]
sources:
  - book: isbn:9780898714647
    title: David Peleg, Distributed Computing, A Locality-Sensitive Approach, SIAM, 2000
    locator: Chapter 3 (broadcast and convergecast on a tree, message and time bounds); Chapter 4 (downcasts and upcasts of many values)
  - paper: doi:10.1109/TIT.1983.1056620
    title: Adrian Segall, Distributed network protocols, IEEE Transactions on Information Theory 29(1), 23-35, 1983
    locator: the protocol PIF (propagation of information with feedback) on a tree and on a general network
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 2, Section 2.2 (broadcast and convergecast on a spanning tree)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 15, Section 15.3 (broadcast and convergecast on a spanning tree, AsynchBcastAck)
---

A convergecast collects information from all the nodes of a network at one node, the root, along a rooted spanning tree. Each leaf sends its value to its parent; each inner node waits until every child has reported, combines the children's values with its own, and sends the result to its parent. When the root has heard from all its children it holds the combination of all values: a sum, a count, a maximum, a logical AND, or any other result of an associative and commutative operation. The cost is exactly $n - 1$ messages, one per tree edge, and as many rounds or time units as the height of the tree. It is the reverse of a broadcast on the tree, and the pair "broadcast down, convergecast up" is the basic pattern of distributed computing on trees.

## In plain words

Think of a family tree in which everyone must report how much money they have, and the oldest ancestor wants the total.

People with no children send their amount to their parent. A parent waits until every child has sent a number, adds the numbers to their own amount, and sends the result up to their own parent.

The oldest ancestor gets one number from each child and adds them up. That is the total for the whole family. Each person sends exactly one message, and the time is set by the longest line of descent.

## When it applies

- **A rooted spanning tree is known.** Each node knows its parent and how many children it has. If a node knows only its parent, a broadcast with acknowledgements on the tree first tells each node its children (see the pitfalls).
- **The function decomposes over subtrees.** The result must be computable from partial results of the subtrees, by an operation $\oplus$ that is associative and commutative. Sums, counts, minima, maxima, AND, OR, and pairs of these (for example sum and count for a mean) qualify. A median does not, unless the messages may hold whole lists.
- **Messages can hold a partial result.** In the [CONGEST model](/congest-model/), a partial result must fit in $O(\log n)$ bits; a sum of $n$ numbers of $O(\log n)$ bits does.
- **Timing.** The technique works in the [synchronous model](/synchronous-model/) and in the [asynchronous model](/asynchronous-model/), since a node acts on the arrival of messages and not on a clock. It needs no identifiers beyond the tree; no failures are assumed.

## The template

```pseudo id=main
CONVERGECAST(v)                            ▷ known: parent(v), the number c(v) of children, value x(v)
L1  on start: acc ← x(v), waiting ← c(v); if waiting = 0 then FINISH
L2  on receipt of y from a child: acc ← acc ⊕ y, waiting ← waiting − 1
L3      if waiting = 0 then FINISH
L4  FINISH: if v is the root then output acc
L5      else send acc to parent(v)
```

**Invariant.** When $v$ runs FINISH, $\mathit{acc}$ equals $\bigoplus_{u \in T_v} x(u)$, where $T_v$ is the subtree of $v$. This holds for a leaf at line L1, and for an inner node because each child $c$ sends the value for $T_c$ (by induction on the height) and the subtrees of the children together with $v$ make up $T_v$. Associativity and commutativity make the order of arrival irrelevant.

**Messages.** Each node other than the root sends exactly one message, at line L5. So the run sends exactly $n - 1$ messages.

**Time.** Let $\mathrm{ht}(v)$ be the height of the subtree of $v$ and $h$ the height of the tree. In the synchronous model a leaf sends in round 1, and a node of height $k$ receives its last child value in round $k$ and sends in round $k + 1$; the root outputs in round $h$. In the asynchronous model with delays of at most 1, node $v$ finishes by time $\mathrm{ht}(v)$, so the root outputs by time $h$. Both are proved by induction on the height.

**Broadcast and convergecast.** A broadcast from the root on the same tree costs $n - 1$ messages and $h$ rounds, since each node forwards to its children only. A node starts its convergecast part when the broadcast reaches it. The pair costs $2(n - 1)$ messages and $2h$ rounds, and at the end the root knows that every node got the broadcast. On a breadth-first tree, $h$ is the eccentricity of the root, at most the diameter $D$. This is Segall's PIF (propagation of information with feedback) restricted to a tree.

## Classic examples

**Sum on a small tree.** Root 0 has children 1 and 2, and node 3 is a child of 1; the values are $x = (5, 3, 9, 4)$. In round 1 the leaves 2 and 3 send 9 and 4. Node 1 computes $3 + 4 = 7$ and sends it in round 2. The root outputs $5 + 9 + 7 = 21$ in round 2, which is the height of the tree, after $3 = n - 1$ messages.

**Counting the nodes.** With $x(v) = 1$ and $\oplus = +$, the root learns $n$. Then a broadcast tells every node the value of $n$, which many algorithms need.

**Leader election on a tree.** With $x(v) = \mathrm{id}(v)$ and $\oplus = \max$, the root learns the largest identifier, and a broadcast announces it. On a tree whose root is not known, a variant starts at the leaves and meets in the middle, as in [tree leader election](/tree-leader-election/).

**Acknowledged broadcast.** With $x(v) = $ "I have the message" and $\oplus = $ AND, the convergecast tells the root that the broadcast is complete. The [echo algorithm](/echo-algorithm/) does this on a general graph, building the tree on the way.

**Phases of a layered algorithm.** Distributed BFS by layers and the [β synchronizer](/synchronizer/) end each phase with a convergecast that reports "my subtree is done" and start the next phase with a broadcast from the root.

## Variations

- **Pipelined upcast of many values.** To collect $k$ separate values (not one combined value) at the root, each node forwards values one per round. In the CONGEST model the root receives all $k$ values in $O(k + h)$ rounds, because pipelining keeps every tree edge busy (Peleg 2000, Chapter 4).
- **Upcast of the $k$ smallest values.** If each node holds a set and the root needs the $k$ smallest elements of the union, each node can forward the smallest of its not yet forwarded elements in each round, which gives $O(k + h)$ rounds too; this is used in MST algorithms in the CONGEST model.
- **Convergecast without a root known in advance.** Leaves start; a node that has heard from all but one neighbour sends to that neighbour. The values meet at one node or on one edge, and the node or the two end nodes of that edge then hold the result. This is the saturation method of tree algorithms.
- **Convergecast on a graph.** Combined with [flooding](/flooding/), the echoes of the [echo algorithm](/echo-algorithm/) perform a convergecast on the tree that the flood builds, for $2m$ messages in total.
- **Gossip aggregation.** Without a tree and with failures, [gossip aggregation](/gossip-aggregation/) computes sums and averages approximately by random exchanges, at a higher cost and with a probability of error.
- **Parallel reduction.** In shared memory the same tree pattern is a [parallel reduction](/parallel-reduction/), with $O(\log n)$ span on a balanced tree.

## Pitfalls

- **Unknown number of children.** A node that knows only its parent cannot tell when all children have reported. First run a broadcast in which each node sends "child" to its parent, or "not child" to its other neighbours, so each node counts its children; or use the echo algorithm, which counts all incident edges.
- **Non-decomposable functions.** The median, the mode or the number of distinct values do not combine from partial results of fixed size. Sending whole lists breaks the $O(\log n)$ message size of the CONGEST model.
- **Overflow and repeated values.** In a sum, partial results grow. With $x(v) \le n^c$, partial sums stay below $n^{c+1}$ and fit in $O(\log n)$ bits. Operations that are not idempotent, such as a sum, must not count a node twice, which a tree guarantees but a graph with several paths does not.
- **Deep trees in asynchronous networks.** The time is the height of the tree, not the diameter. A tree built by asynchronous flooding can have height close to $n$ even when $D = 1$; build a breadth-first tree when time matters.
- **Failures.** One crashed node blocks the whole subtree under it. The technique assumes reliable nodes and channels.

## Exercises

1. Show that a convergecast on a tree of height $h$ needs at least $h$ rounds to compute the sum, for some inputs.
2. Compute the mean of the values with one convergecast. What pair of values does each node send?
3. On a path of $n$ nodes with the root at one end, how many rounds does a broadcast followed by a convergecast take? With the root in the middle?
4. A node knows its parent but not its children. Give a protocol that lets each node learn its number of children in two rounds on a synchronous network, and count its messages in terms of $m$.
5. The root wants the second largest value. Give a combining operation with messages of $O(\log n)$ bits.
6. Explain why the echo algorithm sends $2m$ messages while a broadcast and convergecast on a known tree sends $2(n - 1)$.

## References
