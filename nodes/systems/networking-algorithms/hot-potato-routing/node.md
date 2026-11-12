---
tag: P3PE21
kind: algorithm
slug: hot-potato-routing
name: Hot-potato routing
aliases:
- early-exit routing
- nearest-exit routing
area: systems/networking-algorithms
level: advanced
summary: "An AS sends traffic for another network out through the nearest exit by interior cost, among the exits whose BGP routes tie. One multi-source Dijkstra run gives every router its exit."
solves: [routing-problem]
model: word-ram
complexity:
  vars: {n: the number of routers in the AS, m: the number of interior links}
  time: {worst: O((n + m) log n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 2004
  people: [Renata Teixeira, Aman Shaikh, Timothy G. Griffin, Jennifer Rexford]
  note: The interior-cost tie-break of BGP makes each AS hand traffic to its neighbour as early as it can. Teixeira, Shaikh, Griffin and Rexford (2004) measured how interior changes then move traffic between exits.
prereqs: [bgp, link-state-routing, dijkstra]
see_also: [path-vector-routing, routing-problem, shortest-path-tree, binary-heap, ecmp-hashing, nash-equilibrium]
sources:
  - paper: "Renata Teixeira, Aman Shaikh, Timothy G. Griffin and Jennifer Rexford, Dynamics of hot-potato routing in IP networks, ACM SIGMETRICS 2004"
    locator: the model of hot-potato egress selection, and the measurements of BGP changes caused by IGP changes in a large ISP backbone (page numbers not checked)
  - url: https://www.rfc-editor.org/rfc/rfc4271
    title: Y. Rekhter, T. Li and S. Hares (editors), A Border Gateway Protocol 4 (BGP-4), RFC 4271, January 2006
    locator: Section 9.1.2.2, rule (e), prefer the route with the lowest interior cost to its NEXT_HOP, and rule (f), the lowest BGP Identifier
  - book: isbn:9780136681557
    title: James F. Kurose and Keith W. Ross, Computer Networking, A Top-Down Approach, eighth edition, Pearson, 2021
    locator: Chapter 5, Section 5.4 (hot-potato routing and the BGP route-selection algorithm)
  - paper: "Paul Baran, On distributed communications, RAND Corporation memorandum series RM-3420-PR and following, 1964"
    locator: the older meaning of the term, in which a node with no free buffer passes a packet on at once over any free link (volume and page not checked)
---

Hot-potato routing is the rule by which an autonomous system (AS) chooses where traffic leaves it: among the border routers that have equally good [BGP](/bgp/) routes to a destination, each router sends the traffic to the one with the least interior (IGP) cost from itself. The AS gets rid of the traffic as soon as it can, like a hot potato, and lets the next AS carry it the rest of the way. It is the interior-cost step of the BGP decision process (RFC 4271, Section 9.1.2.2, rule (e)). For one prefix, a single multi-source [Dijkstra](/dijkstra/) run from all candidate exits gives every router its exit and its next hop, and the choice is consistent: every router on the way to an exit picks the same exit. Because the choice depends on interior costs, a small IGP change can move traffic for many prefixes from one exit to another.

The name has a second, older meaning. In Paul Baran's 1964 design for a packet network, "hot-potato routing" meant that a node with no buffer space passes a packet on at once over any free link, even a poor one. That idea is now usually called deflection routing, and it is not the subject of this page.

## In plain words

Two big networks often meet in several cities. Suppose a network in New York has traffic for a customer of another network, and both networks meet in New York and in San Francisco. The first network can hand the traffic over in New York, or carry it across the country on its own links and hand it over in San Francisco.

Hot-potato routing says: hand it over at the nearest meeting point, New York. Your own links stay less busy, and the other network carries the traffic the long way. Every router asks only "which exit is closest to me?", using the costs of its own network. If those costs change, the answer can change, and a lot of traffic can move to another exit at once.

## The problem

The AS has an interior graph $G = (V, E)$ of $n$ routers and $m$ links with positive costs, as computed by its IGP, usually [link-state routing](/link-state-routing/). For one destination prefix, BGP has learned routes at several egress routers. The routes that tie in all steps of the decision process before the interior cost (local preference, AS path length, origin, MED, eBGP over iBGP) give a set $X$ of candidate egresses. For each router $v$, choose the egress

$$e(v) = \arg\min_{e \in X} \bigl(\delta(v, e), \mathrm{id}(e)\bigr),$$

the nearest by interior distance $\delta$, and among those the one with the lowest router id. Then choose a next hop toward it, so that forwarding inside the AS is loop-free.

## The algorithm

Run Dijkstra from all egresses at once. Each label is a pair (distance, egress) and pairs are compared in that order, so the tie-break by router id is part of the comparison.

```pseudo id=main
HOT-POTATO(G, X)                    ▷ X: the egresses whose BGP routes tie before the interior-cost step
L1  for each router v: label[v] ← (∞, nil);  next[v] ← nil
L2  for each egress e in X: label[e] ← (0, e);  insert e into the queue Q
L3  while Q is not empty do
L4      u ← the router in Q with the least label (distance first, then egress id)
L5      for each neighbour v of u do
L6          cand ← (label[u].distance + w(u, v), label[u].egress)
L7          if cand < label[v] then label[v] ← cand;  next[v] ← u;  insert v into Q or lower its key
L8  return label, next                ▷ v leaves the AS at label[v].egress, via next[v]
```

A real router does not run this for the whole AS. It already knows its IGP distance to every border router, and for each prefix it compares the distances to the egresses in $X$. The result is the same; the multi-source run computes it for all routers at once, which is how an operator or a planning tool predicts where traffic will leave. Since the choice depends only on the set $X$, prefixes with the same set of tied egresses share one run.

## Example

Four routers in a line, $D - C - A - B$, with costs $A - B$ 5, $A - C$ 3 and $C - D$ 4. Routers $B$ and $D$ are egresses, both with equally good BGP routes to a prefix of a neighbouring AS. $B$ is in New York and $D$ in San Francisco.

| router | distance to $B$ | distance to $D$ | exit |
|---|---|---|---|
| $A$ | 5 | 7 | $B$ |
| $B$ | 0 | 12 | $B$ |
| $C$ | 8 | 4 | $D$ |
| $D$ | 12 | 0 | $D$ |

Now the cost of $A - B$ rises to 9, perhaps for maintenance. Router $A$ now has distance 9 to $B$ and 7 to $D$, so it moves its exit to $D$. All traffic from $A$ for every prefix that has both exits now crosses the AS and leaves in San Francisco. Nothing changed in BGP, yet the neighbouring AS sees traffic arrive at another place, and $A$'s BGP routes for all these prefixes change.

## Correctness

The full proof is in [the correctness proof](#proof-correctness).

**The labels are right.** Add a new source $s$ with an arc to each egress $e$ of weight $(0, e)$, and give each link the weight $(w, 0)$. Path weights are then pairs (interior cost, first egress), compared lexicographically. Adding a link weight adds to the first component and keeps the second, so it preserves the order and never makes a path lighter. These are the only properties of weights that the proof of Dijkstra's algorithm uses. So lines L1 to L8 compute, for each $v$, the least pair $\min_e (\delta(v, e), e)$.

**Forwarding is consistent.** If $v$ chooses $e$ and $u$ is a neighbour on a shortest path from $v$ to $e$, then $u$ also chooses $e$. Its distance to $e$ is $\delta(v, e) - w(v, u)$. For any other egress $e'$, the triangle inequality gives $\delta(u, e') \ge \delta(v, e') - w(v, u) \ge \delta(u, e)$. If both are equal, then $v$ had a tie and chose $e$ for its lower id, and so does $u$. So a packet never switches exit inside the AS, and it reaches its exit along a shortest path.

## Complexity

One multi-source Dijkstra run, with a [binary heap](/binary-heap/), takes $O((n + m) \log n)$ time and $O(n)$ space for all routers and one set $X$. That is the cost of a single-source run, not $|X|$ runs. A router that already has its IGP distances decides each prefix in $O(|X|)$ time.

| measure | bound | case |
|---|---|---|
| all routers, one set of egresses | $O((n + m) \log n)$ | binary heap |
| one router, one prefix | $O(\lvert X \rvert)$ | IGP distances known |
| space | $O(n)$ | labels and next hops |

## Properties

- **Selfish but simple.** Each AS saves its own capacity. When both neighbours do the same, traffic between them often takes asymmetric paths: each direction leaves its source AS early.
- **Consistent inside the AS.** All routers on a path to an exit choose that exit, so plain hop-by-hop forwarding works without tunnels.
- **Coupled to the IGP.** An IGP change of cost or a link failure can change the exit for every prefix whose candidate egresses tie, all at once.
- **Last among the policy steps.** It only breaks ties. Local preference, AS path length and MED come first.

## Variants and improvements

- **Cold-potato routing.** Carry the traffic on your own network to the exit nearest the destination, for example by honouring the neighbour's MED or by setting local preference per exit. Content providers and networks with good backbones use it to control quality.
- **Tie-breaking with tunnels.** If routers tunnel traffic to the chosen exit, each router can choose by any rule, since the packet no longer follows the IGP next hops of other routers.
- **Decoupling from the IGP.** Teixeira and others proposed to make the egress choice depend on a separate, configurable cost, so that IGP maintenance does not move BGP traffic.
- **Multipath.** If two exits have the same cost, some routers split traffic between them with [ECMP hashing](/ecmp-hashing/) instead of taking the lowest id.

## When to use it

Hot-potato routing is the default for transit between ASes that peer in several places and have no agreement to do otherwise. It minimizes the load on the AS's own backbone. It is a poor fit when the AS cares about the quality of the whole path, as a content provider does, or when a peer insists on symmetric traffic; then operators use cold-potato routing through MED or local preference.

## Pitfalls

- **Unexpected traffic shifts.** IGP weight tuning, maintenance or a link failure can move large volumes of traffic to another peering point, and the neighbouring AS sees it as a change in its inbound load. Teixeira and others found that such interior changes caused a large share of the BGP route changes at some routers of the ISP they measured.
- **Delayed reaction.** A router may notice an IGP change only at its next scan of the BGP table. Until then, it can send traffic to an exit that is no longer the nearest.
- **Confusing the two meanings.** In older texts on packet switching, hot-potato routing means sending a packet on any free link when buffers are full. Check which meaning a source uses.
- **Assuming shortest paths between ASes.** Each AS chooses its own early exit, so the end-to-end path can be much longer than the shortest one, and the two directions of a connection often differ.

## Implementations

The Python code is the multi-source Dijkstra with labels compared as (distance, egress id), and a helper that keeps the egresses whose BGP keys tie. The tests compare the labels with one Dijkstra run per egress on seeded random graphs with many ties, follow the next hops from every router to check that they reach the chosen egress with the stated cost and that every router on the way chooses the same egress, and replay the exit shift of the example.

## History

Paul Baran used the name hot-potato routing in his 1964 RAND reports on distributed communications for a different idea, sending a packet on at once over any free link; the idea lives on as deflection routing in bufferless and optical networks. The present meaning came with BGP between commercial ISPs in the 1990s, when the interior-cost tie-break made each ISP hand traffic over at its nearest exit. Teixeira, Shaikh, Griffin and Rexford (2004) studied the effect in a large ISP and showed how IGP changes move traffic between exits.

## References
