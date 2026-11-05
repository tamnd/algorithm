---
tag: TQQ5YH
kind: problem
slug: airline-scheduling
name: Airline scheduling
aliases:
- fleet sizing
- vehicle scheduling with a fixed timetable
area: graphs/flows-and-cuts
level: core
summary: Decides whether a set of flight segments can be served by a limited number of planes, modeled as a circulation with demands.
prereqs: [circulation-problem, max-flow-problem, flow-integrality-theorem]
see_also: [minimum-path-cover-problem, path-cover-by-bipartite-matching, dilworth-theorem, bipartite-matching, directed-acyclic-graph, flow-decomposition, vehicle-routing-problem]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 7.9, Airline Scheduling (the circulation with lower bounds, its correctness, and the extensions)
  - paper: doi:10.1002/nav.3800010309
    title: George B. Dantzig and Delbert R. Fulkerson, Minimizing the number of tankers to meet a fixed schedule, Naval Research Logistics Quarterly 1(3), 217 to 222 (1954)
    locator: the whole paper (the fleet size problem for a fixed timetable)
---

The airline scheduling problem asks whether $k$ planes can fly a given set of flights, each with a fixed origin, destination and time, when a plane can take a later flight only if it can get to that flight's origin in time. It is modeled as a [circulation with demands](/circulation-problem/) and lower bounds: each flight is an edge that must carry exactly one plane, and the planes are units of flow from a source to a sink. One [maximum flow](/max-flow-problem/) decides it, and the [integrality theorem](/flow-integrality-theorem/) turns the flow into a route for each plane. The fewest planes needed is the size of a [minimum path cover](/minimum-path-cover-problem/) of the graph of possible connections.

## In plain words

An airline has a list of flights for tomorrow and a few planes. A plane can fly one flight and then another if it lands where the next one starts in time, or if it can fly there empty in time. Can the planes cover all the flights?

Think of each plane as a token that starts the day, takes some flights in order, and ends the day. Each flight must be taken by exactly one token. Put a must-use pipe for each flight, a link from the end of one flight to the start of any flight that can follow it, a pipe from a start point into each flight, and a pipe from each flight to an end point. Then ask whether $k$ tokens can flow so that every must-use pipe is used. A flow method answers this, and the tokens' paths are the planes' days.

## Definition

**Input.** A set of $n$ flights; flight $i$ has an origin, a destination, a departure time and an arrival time. A relation "$j$ is reachable from $i$": one plane can fly $i$ and later $j$. Typically $j$ is reachable from $i$ if the destination of $i$ is the origin of $j$ and the departure of $j$ is at least the arrival of $i$ plus a turnaround time, or if a plane can fly empty from the destination of $i$ to the origin of $j$ in time. A number $k \ge 0$ of planes.

**Output.** Yes if $k$ planes can fly all the flights, each flight by one plane, each plane flying a sequence $i_1, i_2, \dots$ with each $i_{r+1}$ reachable from $i_r$; and such an assignment. The relation is acyclic, since it goes forward in time.

**The circulation.** The network is directed and all bounds are integers:

- nodes $u_i$ and $v_i$ for each flight $i$, with an edge $u_i \to v_i$ of lower bound 1 and capacity 1;
- an edge $v_i \to u_j$ of capacity 1 when $j$ is reachable from $i$;
- edges $s \to u_i$ and $v_i \to t$ of capacity 1 for each $i$ (a plane may start or end its day at any flight);
- an edge $s \to t$ of capacity $k$ (a plane may stay idle);
- demands $d(s) = -k$, $d(t) = k$, and 0 elsewhere.

There are no antiparallel edges: $v_i \to u_j$ and $v_j \to u_i$ would need $j$ after $i$ and $i$ after $j$.

**Theorem.** The flights can be flown with $k$ planes if and only if this circulation is feasible.

*Proof.* Given $k$ planes, send one unit of flow along $s \to u_{i_1} \to v_{i_1} \to u_{i_2} \to \dots \to v_{i_r} \to t$ for each plane that flies $i_1, \dots, i_r$, and the unused units along $s \to t$. Each flight edge carries exactly 1, each connection edge at most 1, and the demands hold. Conversely, take a feasible circulation; by the integrality theorem for circulations it can be taken integral. It is then an s-t flow of value $k$ in which each $u_i \to v_i$ carries 1. Since the network is acyclic, the [flow decomposition](/flow-decomposition/) has no cycles and gives $k$ paths from $s$ to $t$ of value 1 each; each path passes through flight edges in reachable order, which is one plane's day, and each flight edge lies on exactly one path. $\square$

## Variants

- **Fewest planes.** The least feasible $k$ is the size of a minimum path cover of the DAG of flights and reachability. It equals $n$ minus a maximum matching in the bipartite graph with an edge from $v_i$ to $u_j$ when $j$ is reachable from $i$; see [path cover by bipartite matching](/path-cover-by-bipartite-matching/). When reachability is transitive, Dilworth's theorem says it also equals the largest set of pairwise unreachable flights.
- **Plane types, maintenance and crews.** Planes must visit a base for maintenance, or crews have legal duty limits. These side constraints break the pure flow model and lead to integer programs, often solved by column generation.
- **Costs.** With a cost on each empty repositioning flight, a [min-cost circulation](/min-cost-flow-problem/) finds the cheapest schedule for $k$ planes.
- **Fixed start and end bases.** Replace the single $s$ and $t$ by nodes per airport with supplies and demands, which is again a circulation with demands.

## Examples

**Five flights.** Turnaround time 1 hour, no empty flights:

| flight | route | departs | arrives |
|---|---|---|---|
| 1 | BOS to DCA | 6:00 | 7:00 |
| 2 | DCA to ATL | 9:00 | 11:00 |
| 3 | PHL to ATL | 7:00 | 9:00 |
| 4 | ATL to SFO | 12:00 | 17:00 |
| 5 | PHL to BOS | 11:00 | 12:00 |

The reachable pairs are $1 \to 2$ (at DCA, 9:00 is at least 7:00 plus 1 hour), $2 \to 4$ and $3 \to 4$ (at ATL). Flight 5 has no successor or predecessor.

*Three planes suffice.* Plane 1 flies 1, 2, 4; plane 2 flies 3; plane 3 flies 5. In the reduced maximum flow instance of the [circulation problem](/circulation-problem/), the lower bounds turn each $v_i$ into a supply of 1 and each $u_i$ into a demand of 1, so the total demand is $D = n + k = 8$, and the maximum flow is 8.

*Two planes do not.* With $k = 2$ the maximum flow is 6, below $D = 7$. Indeed flights 1, 3 and 5 are pairwise unreachable from one another, so no plane flies two of them. A maximum matching in the connection graph has size 2 ($1 \to 2$ and $2 \to 4$, or $1 \to 2$ and $3 \to 4$), and $5 - 2 = 3$ planes are needed.

*Four planes.* With $k = 4$ the extra plane takes the edge $s \to t$ and stays idle; the circulation is feasible.

**No planes.** With $k = 0$ the edge $s \to t$ has capacity 0, and the demands of $s$ and $t$ are 0. If there is at least one flight, its edge needs flow 1, which must come from $s$; the circulation is infeasible. With no flights and $k = 0$, the zero circulation is feasible.

**No connections at all.** If no flight is reachable from another, each plane flies at most one flight, and $k$ planes suffice exactly when $k \ge n$.

## Known algorithms

- **Circulation by maximum flow.** Remove the lower bounds, add a super-source and super-sink, and run one maximum flow; the network has $2n + 2$ nodes and $O(n^2)$ edges. With unit capacities, [Dinic's algorithm](/dinic/) runs in $O(m \sqrt m)$ for $m = O(n^2)$ edges.
- **Matching.** For the least $k$, a maximum bipartite matching by [Hopcroft-Karp](/hopcroft-karp/) gives the minimum path cover in $O(m \sqrt n)$ time.
- **Reading the schedule.** Decompose the integral flow into paths; each path is one plane.

## Bounds

The connection graph can have $\Theta(n^2)$ edges, so building it takes $\Theta(n^2)$ time in the worst case. When reachability depends only on airports and times, a compact network with one node per airport and time point (a time-expanded network) has $O(n)$ edges, and the fleet size problem then becomes a minimum flow in that network.

## Reductions

- **To [circulation with demands](/circulation-problem/)** and from there to maximum flow, as above.
- **To minimum path cover in a DAG**, and from there to bipartite matching, for the least number of planes.
- **Generalizes interval scheduling on machines.** If every flight can follow every flight that departs after it lands, the least number of planes is the largest number of flights in the air at once, the interval partitioning bound.

## Applications

Fleet sizing for airlines, buses, trains and delivery trucks with fixed timetables; Dantzig and Fulkerson's 1954 problem of the fewest tankers for a fixed shipping schedule; and assignment of rooms or machines to jobs with fixed times and setup rules.

## References
