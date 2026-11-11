---
tag: 7YXJZ9
kind: algorithm
slug: scamp
name: SCAMP
aliases:
- scalable membership protocol
- Scalable Membership Protocol
area: distributed/gossip
level: advanced
summary: A membership protocol in which joins are forwarded at random and kept with probability 1/(1 + view size), so partial views grow to about (c + 1) ln n with no node knowing n.
solves: [random-peer-sampling, membership-management]
model: asynchronous-model
complexity:
  vars: {n: the number of nodes, c: the fault tolerance parameter}
  time: {expected: O(c^2 log^2 n)}
  space: {extra: O(c log n)}
properties: {deterministic: false, recursive: false}
prereqs: [random-peer-sampling, gossip-fanout, harmonic-series]
see_also: [membership-management, peer-sampling-service, cyclon, lpbcast, hyparview, gossip-fanout, probabilistic-broadcast, churn]
sources:
  - paper: doi:10.1109/TC.2003.1176982
    title: Ayalvadi J. Ganesh, Anne-Marie Kermarrec and Laurent Massoulié, Peer-to-peer membership management for gossip-based protocols, IEEE Transactions on Computers 52(2), 2003
    locator: pages 139 to 149 (subscription with c extra copies and the keep probability 1/(1 + size of the partial view), unsubscription, the mean partial view size (c + 1) log n, indirection, leases and isolation recovery)
  - paper: "Ayalvadi J. Ganesh, Anne-Marie Kermarrec and Laurent Massoulié, SCAMP: peer-to-peer lightweight membership service for large-scale group communication, Third International Workshop on Networked Group Communication (NGC), LNCS 2233, 2001"
    locator: the first version of the protocol
  - paper: "Anne-Marie Kermarrec, Laurent Massoulié and Ayalvadi J. Ganesh, Probabilistic reliable dissemination in large-scale systems, IEEE Transactions on Parallel and Distributed Systems 14(3), 2003"
    locator: the fanout log n + c and the limit probability exp(-exp(-c)) that gossip reaches every node
---

SCAMP (Scalable Membership Protocol) is a gossip membership protocol, from Ganesh, Kermarrec and Massoulié (2001, 2003), in which each node keeps a partial view whose size adapts by itself to about $(c + 1) \ln n$, where $n$ is the number of nodes and $c$ is a parameter, with no node knowing $n$. A new node subscribes through a contact, which forwards the subscription to all nodes of its partial view and to $c$ more random ones. A node that receives a forwarded subscription keeps it with probability $1/(1 + \text{size of its view})$ and forwards it otherwise. A fanout of $\ln n + c$ is what [gossip](/gossip-protocol/) needs to reach every node with probability about $e^{-e^{-c}}$, so SCAMP gives gossip the right fanout with no global knowledge.

## In plain words

When a newcomer joins a club, it tells one member. That member passes the news to every friend on its list, and to a few more friends picked at random. A friend who hears the news may add the newcomer to its own list, or pass the news on to someone else.

A member with a short list almost always adds the newcomer. A member with a long list usually passes the news on. So lists stay balanced, and they grow slowly as the club grows: a few names more each time the club gets nearly three times bigger.

This slow growth is exactly what gossip needs. To reach everyone, each member should pass a message to a number of friends that grows in this same slow way, and SCAMP gives every member a list of about that size without anyone counting the members.

## The problem

Gossip with fanout $k$ reaches all $n$ nodes with high probability only when $k$ is about $\ln n$ or more (see [gossip fanout](/gossip-fanout/)). The membership protocol must give each node a partial view of that size, with views close to random subsets, without a central server and without an estimate of $n$, and keep this under joins and leaves. See [membership management](/membership-management/).

## The algorithm

Each node $s$ keeps a PartialView, the nodes it sends gossip to, and an InView, the nodes that have $s$ in their PartialView. A forwarded subscription is a message that carries the identifier of the new node.

```pseudo id=main
SCAMP-SUBSCRIBE(s, contact)
L1  PartialView(s) ← {contact}
L2  the contact sends a forwarded subscription for s to every node of its PartialView
L3  the contact sends c more forwarded subscriptions for s to random nodes of its PartialView
ON-FORWARDED-SUBSCRIPTION(s) at node j
L4  if s ≠ j and s ∉ PartialView(j) then
L5      with probability 1 / (1 + |PartialView(j)|): add s to PartialView(j), add j to InView(s), and stop
L6  send the forwarded subscription to a random node of PartialView(j)
SCAMP-UNSUBSCRIBE(s)
L7  let i_1, ..., i_l be PartialView(s) and j_1, ..., j_l' be InView(s)
L8  for k = 1 to l' − c − 1: ask j_k to replace s by i_{k mod l} in its PartialView
L9  ask j_{l'−c}, ..., j_l' to remove s from their PartialView
```

In line L8, if $j_k$ already holds $i_{k \bmod l}$ or is that node, it only removes $s$.

**Indirection.** The join analysis needs a contact that is a uniform random node, but a newcomer usually knows only a few fixed nodes. With indirection, the node that receives the join does not act as the contact itself; it forwards the subscription on a short random path, and the node at the end of the path acts as the contact.

**Leases.** Every subscription has a finite lifetime. When it expires, the nodes that hold it drop it, and the subscriber subscribes again, through a node of its own PartialView. A crashed node cannot subscribe again, so all arcs to it vanish within one lease period, without any failure detector. Resubscription also rebalances the views after many leaves.

**Isolation recovery.** A node that receives no gossip for a long time assumes that no node holds it, and subscribes again through any node it knows.

**Gossip.** To broadcast, a node sends the message to every node of its PartialView, and every node does the same the first time it receives the message.

## Example

**The size law in outline.** Count the arcs $M_n$ (the sum of all PartialView sizes) when $n$ nodes are present. A join through a uniform contact with PartialView size $d$ creates $d + c$ forwarded copies, and each copy is kept by exactly one node, unless it is lost. The new node also gets one arc to its contact. So $M_{n+1} = M_n + d + c + 1$, and $\mathbb{E}[d] = M_n / n$. For the mean view $a_n = M_n / n$ this gives

$$\mathbb{E}[a_{n+1}] = \mathbb{E}[a_n] + \frac{c + 1}{n + 1}, \qquad \text{so} \qquad \mathbb{E}[a_n] = a_{n_0} + (c + 1)(H_n - H_{n_0}) \approx (c + 1) \ln n,$$

where $H_n$ is the $n$-th [harmonic number](/harmonic-series/). Ganesh, Kermarrec and Massoulié state the result as a mean partial view size of $(c + 1) \log n$; the full proof of the expectation is below. An unsubscription removes about $a + c + 1$ arcs, the out arcs of the leaver and the $c + 1$ in arcs that are dropped, which matches the decrease of $(c + 1) \ln n$ when $n$ falls by one.

**Simulation.** Six runs grow a group from 50 to 1000 nodes through uniform contacts, with no lost copies after 50 nodes:

| $c$ | mean PartialView at $n = 1000$ | prediction $a_{50} + (c + 1)(H_{1000} - H_{50})$ | $(c + 1) \ln 1000$ |
|---|---|---|---|
| 1 | 12.40 | 12.57 | 13.82 |
| 2 | 18.45 | 18.29 | 20.72 |
| 4 | 27.06 | 27.45 | 34.54 |

The views are below $(c + 1) \ln n$ by a constant, because the first nodes cannot keep all copies: with 3 nodes there are not enough places for $d + c$ copies, some copies are lost, and these early losses are inherited by all later sizes. The growth after 50 nodes matches the prediction.

With $c = 1$ and 800 nodes, 240 random unsubscriptions leave the remaining 560 nodes connected, with no arc to a node that left. After 180 of 600 nodes crash, about 1400 arcs point to crashed nodes; one lease period removes all of them.

## Correctness

The proved claims are: the views stay consistent (no node holds itself, and the PartialView and InView relations match); a join with no lost copy adds exactly $d + c + 1$ arcs; with uniform contacts the expected mean PartialView size is $a_{n_0} + (c + 1)(H_n - H_{n_0})$; an unsubscription leaves no arc to the leaver; and one lease period removes every arc to a crashed node. The full proof is below.

Concentration of the view sizes around the mean, and the reliability of gossip over the views, are not proved here. Ganesh, Kermarrec and Massoulié support them by analysis of a simplified model and by simulation.

## Complexity

- **Join.** The contact sends $d + c$ forwarded copies, where $d \approx (c + 1) \ln n$ is its view size. A node with view size $a$ keeps a copy with probability $1/(1 + a)$, so a copy is forwarded about $a \approx (c + 1) \ln n$ times before a node keeps it. So a join costs about $(d + c) \cdot a$ messages, which is $O(c^2 \log^2 n)$ in expectation for $c \ge 1$. In the implementation with $n = 1000$, a join takes 125 forwarding messages on average for $c = 1$, 219 for $c = 2$ and 551 for $c = 4$, which is below the estimate $(d + c) \cdot a$ (176, 341 and 865), because a copy stops sooner at nodes with small views. Lost copies are rare once the group has more than a few dozen nodes.
- **Unsubscription.** $l'$ messages, one to each node of the InView.
- **Space.** The PartialView has about $(c + 1) \ln n$ entries and the InView has the same mean size.
- **Gossip.** A broadcast over the views costs about $(c + 1) n \ln n$ messages.

## Properties

- **Self-sizing.** The view size follows $\ln n$ with no estimate of $n$, through the keep probability $1/(1 + |PartialView|)$.
- **No periodic traffic.** Messages are sent only at joins, leaves and lease expiry, unlike [Cyclon](/cyclon/) or [Newscast](/newscast/), which exchange views every cycle.
- **Reactive.** The views change only through joins and leaves. If nodes crash without unsubscribing, their arcs stay until the leases expire.
- **Balanced in-degree.** InView sizes have the same mean as PartialView sizes. An unsubscription keeps the in-degree of other nodes by redirecting $l' - c - 1$ arcs.

## Variants and improvements

- **Without indirection.** If all newcomers use the same contact, the views around that contact grow too large and the views are not random. Indirection fixes it.
- **Gossip-based membership with a fixed fanout.** [lpbcast](/lpbcast/) keeps a fixed view size and piggybacks membership on gossip messages.
- **Reactive views for broadcast.** [HyParView](/hyparview/) keeps a small active view for flooding and a larger passive view for repair, instead of a $\ln n$ sized view.
- **Weighted views.** Later work adds weights to subscriptions so that views follow node capacity.

## When to use it

Use SCAMP when nodes gossip to their whole view, the group size is unknown and changes over time, and joins and leaves are not too frequent. It gives the logarithmic fanout that flat gossip needs. When churn is heavy and crashes are common, a periodic protocol such as [Cyclon](/cyclon/), or a protocol with active failure detection such as [HyParView](/hyparview/), keeps the views cleaner.

## Pitfalls

- **Small groups.** In a group of a few nodes, the forwarded copies cannot all be kept, because every node already holds the newcomer. Copies must carry a hop limit or be dropped after a while.
- **Fixed contact without indirection.** The views of a few nodes grow far beyond $(c + 1) \ln n$.
- **Crashes without leases.** A crashed node never unsubscribes, so arcs to it stay forever and gossip sent to it is lost.
- **Choice of $c$.** The probability that gossip reaches everyone is about $e^{-e^{-c}}$, so $c = 1$ gives about 0.69 and $c = 4$ about 0.98 in the limit of large $n$. Larger $c$ costs more messages per broadcast.

## Implementations

## History

Ganesh, Kermarrec and Massoulié introduced SCAMP at the Networked Group Communication workshop in 2001, and published the full protocol with indirection, leases and the analysis in IEEE Transactions on Computers in 2003. The design rests on their analysis with the same coauthors of gossip with random fanout, published in IEEE Transactions on Parallel and Distributed Systems in 2003, which shows that a fanout of $\ln n + c$ reaches all nodes with probability tending to $e^{-e^{-c}}$, like the [connectivity threshold](/erdos-renyi-connectivity-threshold/) of random graphs.

## References
