---
tag: NZBKF8
kind: technique
slug: rip-up-and-reroute
name: Rip-up and reroute
aliases:
- rip-up and retry
area: eda/routing
level: core
summary: Removes the routes of nets that cause overflow or violations and routes them again in a new order or with new costs, until the routing is legal.
prereqs: [global-routing, lee-maze-routing]
see_also: [global-routing, detailed-routing, negotiated-congestion-routing, lee-maze-routing, pattern-routing, local-search, multicommodity-flow-global-routing]
sources:
  - paper: doi:10.1109/DAC.1982.1585535
    title: William A. Dees Jr. and Patrick G. Karger, Automated rip-up and reroute techniques, Proceedings of the 19th Design Automation Conference, 432 to 439, 1982
    locator: the removal of routed connections that block a failed connection and the rerouting of both (general locator)
  - paper: "Ravi Nair, A simple yet effective technique for global wiring, IEEE Transactions on Computer-Aided Design CAD-6(2), 165 to 172, 1987"
    locator: the iterative rerouting of every net, one at a time, with the other nets in place (general locator)
  - paper: doi:10.1145/201310.201328
    title: Larry McMurchie and Carl Ebeling, PathFinder, a negotiation-based performance-driven router for FPGAs, Proceedings of the ACM Symposium on Field-Programmable Gate Arrays (FPGA '95), 111 to 117, 1995
    locator: the rerouting of all nets with present and history congestion costs
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 5, Section 5.7 Full-Netlist Routing (rip-up and reroute) and Section 5.8 Modern Global Routing
---

Rip-up and reroute (RRR) is a technique for routing many nets on shared resources. A first routing, usually net by net, leaves some edges overflowed or some design rules broken. RRR then removes the routes of some nets that touch the bad spots, changes the order or the costs, and routes those nets again with a shortest path search such as [Lee's maze router](/lee-maze-routing/). It repeats this until the routing is legal or a limit is reached. It is used in almost every [global](/global-routing/) and [detailed](/detailed-routing/) router, and it has no general guarantee that it ends with a legal routing: its value is measured on benchmarks.

## In plain words

When you route wires one at a time, the first wires take the best places, and a later wire may find its way blocked. Rip-up and reroute is the fix that a person would try by hand: pull out some wires that are in the way, and lay them again in a better order or with a reason to avoid the crowded spots.

The router repeats this. Each time it looks for the places with too many wires, removes some of the wires there, and routes them again while it treats the crowded places as more expensive. Often the crowding moves away and disappears after a few rounds.

Nothing makes this always work. The wires can trade places forever, or the problem can have no answer at all, so the router needs a limit on the number of rounds.

## When it applies

- Many nets compete for edges or cells with a capacity, and a single-net router is available: a maze search, [A* search](/a-star-search/) or [pattern routing](/pattern-routing/).
- A sequential router gives a routing with a few local problems, not a routing that is bad everywhere.
- The cost of one reroute is small next to the cost of routing the whole netlist again.
- The quality goal can be measured after each round: total overflow in global routing, or the number of rule violations in detailed routing.

## The template

The input is a routing graph with capacities, a set of nets, and a single-net router $\textsc{Route}(i, \mathrm{cost})$ that returns a cheapest route of net $i$ under the given edge costs.

1. **Initial routing.** Route every net once, in some order, for example by increasing bounding box. Record the usage $u_e$ of each edge.
2. **Find the violations.** Let $F$ be the set of edges with $u_e > c_e$ (or the rule violations of a detailed routing). If $F$ is empty, stop.
3. **Choose the victims.** Pick a set $Q$ of nets to rip up. Common choices: all nets that use an edge of $F$; only the nets that are cheapest to move; or the failed net and the nets that block it.
4. **Rip up.** Remove the routes of the nets in $Q$ and lower the usage.
5. **Change the costs or the order.** Raise the cost of the edges in $F$, keep a history of how often each edge was overflowed, or move the victims to the front of the order.
6. **Reroute.** Route each net of $Q$ with $\textsc{Route}$ under the new costs, and update the usage after each net.
7. **Decide.** Keep the new routing, or keep it only if the total overflow went down. Go back to step 2 until a round limit or a time limit is reached.

**A termination fact.** Suppose step 7 keeps a new routing only when the total overflow $\mathrm{TOF}$ drops. $\mathrm{TOF}$ is a nonnegative integer, so it drops by at least 1 at each accepted round, and at most $\mathrm{TOF}_0$ rounds are accepted, where $\mathrm{TOF}_0$ is the overflow of the initial routing. This rule stops the loop, but it can stop at a routing with overflow that a worse intermediate step would have fixed. Routers that accept worse rounds, as in [negotiated congestion routing](/negotiated-congestion-routing/), give up this argument and need a round limit.

## Classic examples

**Two nets in the wrong order.** Take a $3 \times 3$ grid of gcells with capacity 1 on each edge, with gcells $(x, y)$. Net A joins $(1,0)$ and $(0,1)$, and net B joins $(0,0)$ and $(2,2)$. The single-net router is a shortest path search that avoids full edges when it can, with ties broken to the lower node index.

- Initial routing, A first. A takes the route through the corner, on edges $(0,0)(1,0)$ and $(0,0)(0,1)$. Both edges of the corner gcell $(0,0)$ are now full, so B must cross one of them. B takes $(0,0)$, $(1,0)$, $(2,0)$, $(2,1)$, $(2,2)$, and the edge $(0,0)(1,0)$ has usage 2. $\mathrm{TOF} = 1$, $\mathrm{WL} = 6$.
- Round 1. $F = \{(0,0)(1,0)\}$, and both nets use it, so $Q = \{A, B\}$. Rip up both and reroute the failed net B first. B takes the same route along the bottom row and the right column. Then A finds $(0,0)(1,0)$ full and takes the route through the center, on $(1,0)(1,1)$ and $(1,1)(0,1)$.
- The result has $\mathrm{TOF} = 0$ and $\mathrm{WL} = 6$. Over all $8 \cdot 12 = 96$ pairs of routes of the two nets, this is the least wirelength of a legal routing.

Ripping up only the blocker A and rerouting it with B in place gives a legal routing of the same length here.

**Dees and Karger (1982).** A connection that the maze router cannot complete is not left open. The router removes connections that block it, routes the failed one, and then tries to route the removed ones again.

**Nair (1987).** Every net is rerouted in turn, one at a time, with all other nets in place and with costs that reflect their congestion. The passes repeat over the whole netlist, not only over the failed nets. LocusRoute used this scheme.

**PathFinder (1995).** [Negotiated congestion routing](/negotiated-congestion-routing/) reroutes every net in each round. The cost of a resource grows with its present sharing and with its history of overuse, so the nets negotiate who gets a crowded resource. It is the base of many FPGA routers and of global routers such as NTHU-Route 2.0.

## Variations

- **Victim choice.** Rip up all nets through the violations; only the net with the smallest extra cost to move; or a random subset, which can break cycles.
- **Cost update.** A fixed penalty on full edges; a penalty that grows each round; or a history term that never decreases, as in negotiated congestion. A history term remembers spots that were crowded in earlier rounds, so the nets do not come back to them.
- **Order.** Reroute the failed nets first, nets with large bounding boxes first, or a random order in each round.
- **Region of the reroute.** Reroute only a window around the violation, which is the usual form in [detailed routing](/detailed-routing/) where the router fixes rule violations ("search and repair").
- **Acceptance.** Always keep the new routing, keep it only when it is better, or keep it with a probability, as in [simulated annealing](/simulated-annealing/). The last two make RRR a form of [local search](/local-search/).
- **Combination with exact methods.** A fractional solution from [multicommodity flow routing](/multicommodity-flow-global-routing/) is rounded, and RRR removes the overflow that the rounding leaves.

## Pitfalls

- **No legal routing exists.** On the $2 \times 2$ grid with capacity 1, two nets that join opposite corners always share an edge. RRR then never reaches $\mathrm{TOF} = 0$, so it must have a round limit and report the best routing seen.
- **Cycling.** With costs that depend only on the present usage, two nets can move back and forth between the same two routes, each one leaving the place the other one just took. A history cost, a random order or a rule that rips up fewer nets breaks the cycle.
- **Ripping up too much.** Removing every net near a violation often gives the same routing again, because the same order and costs lead to the same choices.
- **Wirelength growth.** Each reroute avoids crowded edges, so routes get longer. A router should track wirelength as well as overflow and stop when the overflow no longer drops.
- **No proof of quality.** The order and the costs are heuristics. Claims about RRR come from benchmark runs, such as the ISPD 2007 and 2008 global routing contests, not from theorems.
- **Same router, same answer.** If the single-net router and its costs do not change between rounds, rerouting a net with the others in place gives back its old route. Something must change: the order, the costs or the set of nets in place.

## Exercises

1. Prove the termination fact above, and give an instance on which the "accept only if better" rule stops with $\mathrm{TOF} > 0$ while a legal routing exists.
2. Suppose the reroute is deterministic and the costs depend only on the present routes. Show that the sequence of routings is eventually periodic, so the loop either stays at one routing or repeats a cycle forever.
3. Add a history cost $h_e$ that grows by 1 in each round in which edge $e$ is overflowed. Show that the pair (routing, history) never repeats while the overflow is positive. Does this prove that the loop reaches zero overflow?
4. In the $3 \times 3$ example, list all legal routings with wirelength 6 and check that there are exactly two.
5. Explain why RRR on the crossing nets of the $2 \times 2$ grid cannot end with zero overflow, by counting the edges that the two routes must share.

## References
