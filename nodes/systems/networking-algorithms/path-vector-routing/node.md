---
tag: CAQP3D
kind: algorithm
slug: path-vector-routing
name: Path-vector routing
aliases:
- path vector protocol
- simple path vector protocol
- SPVP
area: systems/networking-algorithms
level: advanced
summary: "Routers advertise whole paths, drop any path that contains themselves, and pick the best permitted path by their own ranking. No loops form, but some rankings never settle."
solves: [routing-problem]
model: asynchronous-model
complexity:
  vars: {n: the number of nodes, m: the number of links, d: the largest degree of a node}
  time: {worst: O(n)}
  messages: {worst: O(n m)}
  space: {extra: O(d n^2)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 2002
  people: [Timothy G. Griffin, F. Bruce Shepherd, Gordon Wilfong]
  note: BGP made path vector the routing method between the networks of the Internet. Griffin, Shepherd and Wilfong (2002) modelled it as the stable paths problem and showed that policies can make it diverge.
prereqs: [routing-problem, distance-vector-routing, asynchronous-model]
see_also: [bgp, count-to-infinity, split-horizon-poison-reverse, link-state-routing, hot-potato-routing, nash-equilibrium, np-complete, stable-matching]
sources:
  - paper: "Timothy G. Griffin, F. Bruce Shepherd and Gordon Wilfong, The stable paths problem and interdomain routing, IEEE/ACM Transactions on Networking 10(2), 2002, pages 232 to 243"
    locator: the stable paths problem and stable assignments (page 234), DISAGREE with two solutions, BAD GADGET with none, GOOD GADGET and NAUGHTY GADGET (Figures 2 and 3), the NP-completeness of SPP solvability, dispute wheels, and SPVP
  - paper: "Lixin Gao and Jennifer Rexford, Stable Internet routing without global coordination, IEEE/ACM Transactions on Networking 9(6), 2001, pages 681 to 692"
    locator: the customer, peer and provider rules that guarantee convergence
  - url: https://www.rfc-editor.org/rfc/rfc4271
    title: Y. Rekhter, T. Li and S. Hares (editors), A Border Gateway Protocol 4 (BGP-4), RFC 4271, January 2006
    locator: Section 9.1.2 (routes whose AS_PATH contains the local AS are excluded) and Section 9.2.1.1 (MinRouteAdvertisementIntervalTimer)
  - paper: "Craig Labovitz, Abha Ahuja, Abhijit Bose and Farnam Jahanian, Delayed Internet routing convergence, ACM SIGCOMM 2000"
    locator: path exploration after a withdrawal, measured and bounded (page numbers not checked)
---

Path-vector routing is the routing method in which each router advertises, for each destination, the whole path that its route takes, not only its cost. A router refuses any path that already contains itself, so no loop can form. Among the remaining paths it picks the one that its own policy ranks first. It extends [distance-vector routing](/distance-vector-routing/): the same exchange with neighbours, but the path in each message removes the [count to infinity](/count-to-infinity/). It also lets each router rank routes by any rule it likes. This freedom is why the Internet uses it between autonomous systems, in [BGP](/bgp/). It is also its weakness: with some rankings the protocol never settles, and with others it settles in a state that depends on timing.

## In plain words

Each router tells its neighbours: "I can reach network X by this exact list of routers." When a router hears a list with its own name in it, it ignores the list, because using it would send packets in a circle. From the other lists, it adds its own name at the front, picks the one it likes best, and tells its neighbours.

"Likes best" can mean "shortest", but it can also mean "goes through a customer that pays me" or "avoids a network I do not trust". Each router decides alone. When every router just wants short paths, the protocol always settles on shortest paths. When routers have conflicting wishes, it may switch back and forth for ever.

## The problem

The network is a graph $G = (V, E)$ and one destination $d$; the protocol runs once for each destination. Each node $u \ne d$ has a set $\mathcal{P}^u$ of permitted simple paths from $u$ to $d$, with a strict ranking. A **path assignment** gives each node a path $\pi(u) \in \mathcal{P}^u$ or the empty path $\varepsilon$, with $\pi(d) = (d)$. It is **consistent** if $\pi(u) = u \cdot \pi(v)$ for the first hop $v$ of $\pi(u)$. It is **stable** if each $\pi(u)$ is the best permitted path among $u \cdot \pi(v)$ over the neighbours $v$. Finding a stable assignment is the **stable paths problem** (SPP) of Griffin, Shepherd and Wilfong. With shortest paths as the ranking, the shortest-path tree toward $d$ is the unique stable assignment, and the problem is the ordinary [routing problem](/routing-problem/).

## The algorithm

This is the simple path vector protocol (SPVP), the core of BGP. Node $u$ stores $\mathrm{rib}[u][v]$, the last path heard from neighbour $v$, and $\mathrm{best}[u]$.

```pseudo id=main
PATH-VECTOR(u)                     ▷ one destination d; rank(u, P) is nil if P is not permitted at u
L1  on START: if u = d then best[u] ← (d) and SEND-ALL(u) else best[u] ← ε
L2  on RECEIVE(v, P): rib[u][v] ← P               ▷ P = ε is a withdrawal
L3      RECOMPUTE(u)
L4  on LINK-DOWN(v): delete rib[u][v];  RECOMPUTE(u)

RECOMPUTE(u)
L5  if u = d then return
L6  C ← { u·P : P = rib[u][v] for a neighbour v, P ≠ ε, u ∉ P, rank(u, u·P) ≠ nil }   ▷ loop check
L7  new ← the path in C with the best rank, or ε if C is empty
L8  if new ≠ best[u] then best[u] ← new;  SEND-ALL(u)

SEND-ALL(u)
L9  after a short batching delay, send the current best[u] to every neighbour
L10 on LINK-UP(v): send best[u] to v
```

Line L6 is the loop check: a path that contains $u$ would close a loop, so $u$ never uses it. In BGP the "nodes" are autonomous systems and the check looks for the local AS number in the AS_PATH attribute (RFC 4271, Section 9.1.2). Line L9 sends only the latest best after a short delay. BGP's MinRouteAdvertisementInterval timer does the same, so that a burst of changes produces one update instead of many.

## Example

**Shortest paths, and a withdrawal.** Take a square $a - b - c - d$ with the extra link $a - c$, and destination $d$. $d$ sends $(d)$. $c$ takes $(c, d)$ and sends it. $b$ and $a$ take $(b, c, d)$ and $(a, c, d)$. When $b$ hears $(a, c, d)$ from $a$, it keeps $(b, c, d)$ because it is shorter. When $c$ hears $(b, c, d)$, the path contains $c$, so $c$ ignores it. Now let link $c - d$ fail. In distance-vector routing, $c$ would believe $b$'s old cost of 2 and count to infinity. Here $c$ sees that every path it has heard, $(b, c, d)$ and $(a, c, d)$, contains $c$ itself, so it has no route at once and sends a withdrawal. $a$ and $b$ may try each other's stale paths for a moment, $(a, b, c, d)$ for example, but these are dropped when the withdrawals arrive. Then every node has $\varepsilon$.

This brief trying of longer stale paths is **path exploration**. In a clique of $n$ routers it can try many paths before all routes are gone. Labovitz and others measured it in the Internet in 2000, and it is the reason why BGP withdrawals converge slowly.

**DISAGREE: two stable answers.** Nodes 1 and 2 are both linked to the destination 0 and to each other. Node 1 prefers $(1, 2, 0)$ to $(1, 0)$, and node 2 prefers $(2, 1, 0)$ to $(2, 0)$. Each would rather go through the other. There are exactly two stable assignments: $\{(1, 2, 0), (2, 0)\}$ and $\{(1, 0), (2, 1, 0)\}$. Which one the protocol reaches depends on which node speaks first. If both speak in lock step, they both switch to the indirect path, which then disappears for both, and they both switch back, for ever.

**BAD GADGET: no stable answer.** Nodes 1, 2 and 3 are each linked to 0 and form a ring with a fourth node. Each of 1, 2 and 3 prefers the path through its neighbour on the ring to its direct path:

| node | first choice | second choice |
|---|---|---|
| 1 | (1, 3, 0) | (1, 0) |
| 2 | (2, 1, 0) | (2, 0) |
| 3 | (3, 4, 2, 0) | (3, 0) |
| 4 | (4, 2, 0) | (4, 3, 0) |

Start with 1, 2 and 3 on their direct paths and 4 on $(4, 2, 0)$. Then 3 moves to $(3, 4, 2, 0)$. Now $(1, 3, 0)$ is gone, so 1 stays on $(1, 0)$, and 2 moves to $(2, 1, 0)$. That removes $(4, 2, 0)$, so 4 loses its path through 2, and 3 falls back to $(3, 0)$. Now 1 moves to $(1, 3, 0)$, 2 falls back to $(2, 0)$, 4 takes $(4, 2, 0)$ again, 3 takes $(3, 4, 2, 0)$ again, and the cycle repeats. Each choice destroys the reason for another. An exhaustive search of all assignments finds no stable one, and the protocol runs for ever on this instance. Swapping the preferences of node 4 gives NAUGHTY GADGET, which has one stable assignment but can still oscillate in lock step. Giving node 3 only its direct path gives GOOD GADGET, which converges from every order of events to $(1, 3, 0)$, $(2, 0)$, $(3, 0)$, $(4, 3, 0)$.

## Correctness

The full proof is in [the correctness proof](#proof-correctness). It has three parts.

1. **No loops ever.** Every path that a node holds or sends is simple, by line L6 and induction over events.
2. **Quiet means stable.** When no message is in flight, each $\mathrm{rib}[u][v]$ equals $\mathrm{best}[v]$. So line L7 says exactly that the bests form a stable assignment, and they are consistent, so the forwarding walk follows each path. Hence the protocol can only stop in a solution of SPP, and on an instance with no solution it never stops.
3. **Shortest paths converge.** With hop count (or additive cost) ranking and a fixed tie-break, the protocol converges after the last change. First, paths that use a failed link die out, by induction on their length: such a path can only be rebuilt from a shorter one of the same kind. Then every candidate is a real simple path, the best paths form a tree toward $d$, and each node locks onto its best path once its parent has.

Part 3 depends on the ranking. Griffin, Shepherd and Wilfong showed that the protocol converges whenever the preferences contain no **dispute wheel**, a cyclic pattern in which each node prefers a path through the next. BAD GADGET contains one.

## Complexity

With shortest-path ranking, in synchronous rounds, the invalid paths die out and the tree builds up in $O(n)$ rounds, and each round sends at most $2m$ messages, $O(nm)$ in all. A message carries a path of up to $n$ nodes. A node stores the last path from each neighbour for each of up to $n$ destinations, so $O(d n^2)$ space.

| measure | bound | case |
|---|---|---|
| rounds after the last change | $O(n)$ | shortest-path ranking |
| messages | $O(nm)$ | shortest-path ranking |
| space per node, all destinations | $O(d n^2)$ | worst case |
| rounds with general policies | unbounded | BAD GADGET never converges |

Deciding whether an SPP instance has a stable assignment is NP-complete (Griffin, Shepherd and Wilfong, 2002).

## Properties

- **Loop-free at every instant**, unlike distance vector. No count to infinity.
- **Policy is local.** Each node ranks paths by its own rule and need not reveal it.
- **Convergence is not guaranteed.** It depends on the rankings of all nodes together.
- **The outcome can depend on timing.** With DISAGREE, two runs of the same network can end in different states.
- **Larger messages.** Each route carries its path, of length up to the diameter.

## Variants and improvements

- **BGP.** The real protocol adds attributes, a multi-step decision process, iBGP inside each AS and export filters; see [BGP](/bgp/).
- **The Gao-Rexford conditions.** If each AS prefers routes from customers over routes from peers and providers, and exports routes so that paths are valley-free, then the preferences contain no dispute wheel and BGP converges (Gao and Rexford, 2001). The [BGP](/bgp/) page simulates this.
- **Route flap damping.** BGP routers can suppress a route that changes too often. This hides oscillation, but it can also delay real changes.
- **Monotone rankings.** If extending a path always makes it worse, as with path length or additive cost, the protocol converges to a unique answer, as in Part 3 of the proof.

## When to use it

Use path vector between networks that do not share a metric or a map and that want to apply their own policy, which is the case of autonomous systems in the Internet. It also suits overlays where nodes must avoid loops without a global view. Inside one network with one metric, [link-state routing](/link-state-routing/) converges faster and has no policy conflicts.

## Pitfalls

- **Assuming that it converges.** Only some combinations of policies converge. Policies that violate the Gao-Rexford rules can create BAD GADGET between real networks.
- **Unbatched updates.** Without a batching delay, each change sends its own update, and path exploration gets much longer. In the implementation, the DISAGREE and NAUGHTY instances oscillate for ever when every message takes exactly one step and nothing is batched.
- **Loop check on the wrong identifier.** The check must use the identifier that the path records. In BGP this is the AS number; inside one AS, iBGP needs other rules, because all routers share one AS number.
- **Path length as a cost.** Hop count in AS paths ignores the size and quality of each AS. A short AS path can be a long path in kilometres.

## Implementations

The Python code simulates the protocol with FIFO links, random delays and batched updates, for any ranking. It also solves small SPP instances by brute force and builds the graph of states reached when one node at a time re-selects its best path. The tests check, on seeded random graphs and after link failures and repairs, that the protocol reaches shortest paths with consistent suffixes and never holds a looping path. They also reproduce the gadgets of Griffin, Shepherd and Wilfong: DISAGREE has exactly two solutions and reaches both, BAD GADGET has none and the protocol cycles, and GOOD GADGET converges from every order of activation.

## History

Path vector came with inter-domain routing. EGP, the first exterior gateway protocol of the Internet, required a tree of networks. BGP, first specified in 1989, sent the list of autonomous systems with each route, so that the networks could form any graph without loops. BGP-4, the version in use today, is RFC 4271 (2006). In the 1990s Varadhan, Govindan and Estrin noted that BGP policies can oscillate. Griffin, Shepherd and Wilfong turned this into the stable paths problem and gave the gadgets on this page in 2002. Gao and Rexford found economic rules under which the Internet does converge (2001).

## References
