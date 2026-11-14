---
tag: 1K07JP
kind: algorithm
slug: sat-based-fpga-routing
name: SAT-based FPGA detailed routing
aliases:
- Nam-Sakallah-Rutenbar routing
area: eda/fpga-analog-and-emerging-technologies
level: advanced
summary: Nam, Sakallah and Rutenbar's router that encodes the track choice of every net in every switch block as a SAT formula, proving routability or unroutability.
solves: [detailed-routing]
model: word-ram
complexity:
  vars: {W: the channel width, L: the number of pairs of a net and a segment of its global route, E: the number of edges of all route trees, P: the number of pairs of nets that share a segment (counted once per shared segment)}
  time: {encode: "O(W^2 (L + E) + W P)", solve: "O(2^(W L) W L (W^2 (L + E) + W P))"}
  space: {total: "O(W^2 (L + E) + W P)"}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1999
  people: [Gi-Joon Nam, Karem A. Sakallah, Rob A. Rutenbar]
  note: Nam, Sakallah and Rutenbar turned FPGA detailed routing with a fixed global routing into a CNF formula and solved it with a search-based SAT solver, so that a failure became a proof that no detailed routing exists.
prereqs: [detailed-routing, routing-resource-graph, fpga-switch-block, conjunctive-normal-form]
see_also: [cdcl, dpll, tseitin-transformation, graph-coloring, global-routing, minimum-channel-width, sequential-counter-encoding, negotiated-congestion-routing]
sources:
  - paper: doi:10.1109/TCAD.2002.1004311
    title: Gi-Joon Nam, Karem A. Sakallah and Rob A. Rutenbar, A new FPGA detailed routing approach via search-based Boolean satisfiability, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 21(6), 674 to 684, 2002
    locator: the routing constraints as a Boolean function (connectivity and exclusivity), their CNF form, and routability and unroutability results for a fixed global routing
  - paper: "Gi-Joon Nam, Karem A. Sakallah and Rob A. Rutenbar, Satisfiability-based layout revisited, detailed routing of complex FPGAs via search-based Boolean SAT, Proceedings of the ACM/SIGDA International Symposium on Field Programmable Gate Arrays (FPGA '99), 167 to 175, 1999"
    locator: the first version of the method
  - paper: doi:10.1145/369691.369777
    title: Gi-Joon Nam, Fadi Aloul, Karem A. Sakallah and Rob A. Rutenbar, A comparative study of two Boolean formulations of FPGA detailed routing constraints, Proceedings of the International Symposium on Physical Design (ISPD), 2001; journal version in IEEE Transactions on Computers 53(6), 2004
    locator: the track-based and the route-based formulations and their comparison (general locator)
  - paper: "R. Glenn Wood and Rob A. Rutenbar, FPGA routing and routability estimation via Boolean satisfiability, IEEE Transactions on Very Large Scale Integration Systems, 1998"
    locator: the earlier Boolean formulation of FPGA routing, solved with binary decision diagrams (general locator)
---

SAT-based FPGA detailed routing is an exact method of FPGA CAD for the [detailed routing](/detailed-routing/) of an [island-style FPGA](/island-style-fpga/): with the global routing of every net fixed, it writes the choice of a track for each net in each channel segment as a formula in [conjunctive normal form](/conjunctive-normal-form/), and gives it to a SAT solver. A model of the formula is a legal detailed routing, and an unsatisfiable formula proves that no legal detailed routing exists for that global routing at that channel width. Nam, Sakallah and Rutenbar introduced the method in 1999 and 2002.

## In plain words

After global routing, each net knows which stretches of channel it will use, but not which wire in each stretch. Two nets in the same stretch need different wires, and where a net turns a corner, its two wires must be joined by a switch in that corner.

A heuristic router tries choices and gives up after a while. When it gives up, nobody knows whether a routing exists.

The SAT approach writes every rule as a small logical statement: "this net uses one of these wires", "these two nets do not share this wire", "if the net is on this wire here, it is on a joined wire there". A SAT solver then either finds values that make all the statements true, which is a routing, or proves that no such values exist. The proof means that this global routing cannot be finished with this many wires.

## The problem

**Input.** A channel width $W$, so that every channel segment has the tracks $0, \ldots, W - 1$. A global routing: for each net $n$, a set $\mathrm{Seg}(n)$ of channel segments and a set of edges $(s, s', \kappa)$ that join them into a tree, where $s$ and $s'$ meet at a switch block and $\kappa$ names the two sides of that block, such as WN for west to north. A switch pattern: for each $\kappa$ and track $t$, the set $P(\kappa, t)$ of tracks of $s'$ that a switch joins to track $t$ of $s$ (see [FPGA switch block](/fpga-switch-block/)).

**Output.** A legal detailed routing: a track $\rho(n, s)$ for each net $n$ and segment $s \in \mathrm{Seg}(n)$, such that two nets that share a segment use different tracks on it (exclusivity), and $\rho(n, s') \in P(\kappa, \rho(n, s))$ for each edge (connectivity). Or a proof that none exists.

The model takes the connection blocks to be full, so every pin reaches every track of its segment. The global routing is part of the input; finding it is a separate problem, [global routing](/global-routing/). The method reduces this decision problem to [SAT](/sat/).

## The algorithm

Variable $x_{n,s,t}$ says that net $n$ uses track $t$ of segment $s$.

```pseudo id=main
SAT-ROUTE(nets with their route trees, W, P)
L1  make a variable x[n, s, t] for each net n, each segment s of its route and each track t
L2  for each pair (n, s): add the clause x[n,s,0] ∨ … ∨ x[n,s,W−1]
L3  for each pair (n, s) and tracks t < u: add the clause ¬x[n,s,t] ∨ ¬x[n,s,u]
L4  for each segment s, nets n ≠ m that use s, and track t: add ¬x[n,s,t] ∨ ¬x[m,s,t]
L5  for each edge (s, s', κ) of net n and track t: add ¬x[n,s,t] ∨ ⋁ over u in P(κ, t) of x[n,s',u]
L6  run a complete SAT solver on the clauses
L7  if it reports UNSAT: return "no detailed routing of this global routing at width W"
L8  return ρ(n, s) = the track t with x[n,s,t] true
```

Lines L2 and L3 say that the net uses exactly one track per segment; line L3 is the pairwise at-most-one encoding, and the [sequential counter](/sequential-counter-encoding/) is a smaller alternative for large $W$. Line L4 is exclusivity and line L5 is connectivity, which is already a clause, so no [Tseitin transformation](/tseitin-transformation/) is needed. The solver of line L6 can be any complete solver, such as [DPLL](/dpll/) or [CDCL](/cdcl/); the implementation uses a small DPLL with unit propagation. To find the least width at which the global routing routes, run SAT-ROUTE for $W = 1, 2, \ldots$ until it succeeds.

With the disjoint switch block, $P(\kappa, t) = \{t\}$, so a net keeps one track number along its whole route, and the problem becomes [graph coloring](/graph-coloring/) of the conflict graph: a vertex per net, and an edge between nets that share a segment.

## Example

One switch block has segments on its west (W), north (N) and east (E) sides, with $W = 2$ tracks each. Net A goes from W to N, net B from N to E, and net C from E to W, straight through. Each side carries two nets, so the channel density is 2.

**Disjoint pattern.** Each net keeps one track, and the three nets pairwise share a segment, so the conflict graph is a triangle. A triangle needs 3 colors, so the formula at $W = 2$ is unsatisfiable, and the SAT solver proves that this global routing does not route at width 2. At $W = 3$ it routes, with A, B and C on tracks 0, 1 and 2.

**A twisted pattern.** Change only the turn between W and N, so that track $t$ meets track $1 - t$. The formula has $3 \cdot 2 \cdot 2 = 12$ variables and 24 clauses: 6 of line L2, 6 of line L3, 6 of line L4 and 6 of line L5. For net A, L5 gives $\neg x_{A,W,0} \vee x_{A,N,1}$ and $\neg x_{A,W,1} \vee x_{A,N,0}$. The solver finds A on track 0 in W and track 1 in N, B on track 0 in N and E, and C on track 1 in E and W. Every side has two different tracks in use, and each net's tracks are joined by its switch. The same global routing that needs width 3 with the disjoint block routes at width 2 here. This is why switch blocks that change tracks, such as the [universal switch block](/universal-switch-block/), can lower the width.

## Correctness

The [full proof](proofs/correctness.md) proves the following, for a fixed global routing and width $W$.

- **A model is a routing.** If an assignment satisfies the clauses, then each pair $(n, s)$ has exactly one true variable, by L2 and L3, and the tracks they name meet exclusivity by L4 and connectivity by L5.
- **A routing is a model.** Setting $x_{n,s,t}$ true exactly when $\rho(n, s) = t$ satisfies every clause when $\rho$ is legal.
- **One to one.** These two maps are inverse to each other, so the models and the legal routings are in bijection. The tests check this by counting both on small instances.
- **UNSAT is a proof.** A complete solver reports UNSAT only if no model exists, so no legal detailed routing of this global routing exists at width $W$. It says nothing about other global routings of the same netlist.
- **The routing is a routing on the graph.** A legal detailed routing gives vertex-disjoint trees in the [routing resource graph](/routing-resource-graph/), one per net.
- **Disjoint pattern.** With $P(\kappa, t) = \{t\}$, routability at width $W$ is the $W$-colorability of the conflict graph. Every graph is a conflict graph in the abstract model, so the problem is [NP-complete](/np-complete/) for $W = 3$ there.

The tests compare the router with exhaustive search over all track assignments: 60 satisfiable and 60 unsatisfiable seeded random instances agreed, with random switch patterns and widths 1 to 3. This is a check of the implementation, not a measure of speed.

## Complexity

Let $L$ be the number of pairs of a net and a segment, $E$ the number of route edges and $P$ the number of pairs of nets that share a segment. The formula has $W L$ variables. Line L2 gives $L$ clauses of $W$ literals, line L3 gives $L W (W - 1) / 2$ clauses of 2, line L4 gives $P W$ clauses of 2, and line L5 gives $E W$ clauses of at most $W + 1$. So encoding takes $O(W^2 (L + E) + W P)$ time and space.

SAT is NP-complete, and this restricted form is NP-complete too by the coloring result, so no polynomial bound on the solve is known. The small DPLL of the implementation explores at most $2^{W L}$ partial assignments, with unit propagation in $O(W L)$ passes over the formula at each, which gives the bound in the front matter. Modern CDCL solvers are far faster on the formulas of real routing problems, but that is measured, not proved.

## Properties

- **Exact.** The router succeeds whenever a detailed routing of the given global routing exists, and its failure is a proof.
- **Only detailed routing.** It does not change the global routing. An UNSAT answer may be fixed by a new global routing, which the method does not search.
- **Pattern-independent.** Any switch block that the sets $P(\kappa, t)$ describe fits the same encoding; only the clauses of line L5 change.
- **All nets at once.** Unlike a router that routes one net at a time, the solver decides all tracks together, so it does not get stuck on an early bad choice.

## Variants and improvements

- **Route-based formulation.** Nam, Aloul, Sakallah and Rutenbar (2001, 2004) compared the track-based formulation with one that has a variable per candidate detailed route of a net, and found the route-based one better on their benchmarks.
- **Symmetry breaking.** With the disjoint pattern, the track numbers can be permuted in any solution, so clauses that fix the track of one net cut the search; see [symmetry breaking](/symmetry-breaking/).
- **Incremental width search.** When the width search tries $W, W + 1, \ldots$, an [incremental SAT](/incremental-sat/) solver can keep learned clauses between calls.
- **Smaller at-most-one clauses.** For large $W$, a sequential counter or a log encoding of the track number replaces the $W^2 / 2$ clauses of line L3.

## When to use it

Use a SAT router when a proof matters: to show that a global routing cannot be completed at a width, to check the routability of a small architecture, or to finish the last few nets that a heuristic router cannot place. For whole designs, use [PathFinder](/negotiated-congestion-routing/), which routes globally and in detail at once and scales to large designs, but which cannot prove that a routing does not exist.

## Pitfalls

- **Reading UNSAT as "the circuit is unroutable".** UNSAT is about one global routing at one width. A different global route can succeed.
- **Leaving out at-most-one.** Without line L3 a model may put a net on two tracks of a segment. A routing can still be read from such a model, but the bijection with routings is lost and the decoder must pick one track.
- **One direction of a switch.** Line L5 constrains the track of $s'$ from that of $s$. With at-most-one in place one direction is enough, but the sets $P(\kappa, t)$ must be those of the real switch block on that pair of sides.
- **Assuming full connection blocks.** With sparse connection blocks, a pin reaches only some tracks, and the formula needs clauses for the pins too.

## Implementations

## History

Wood and Rutenbar (1998) wrote FPGA routing as a Boolean function and solved it with binary decision diagrams. Nam, Sakallah and Rutenbar (1999) wrote the routing constraints of a fixed global routing in conjunctive normal form and solved them with a search-based SAT solver instead, so that a failure became a proof of unroutability for that global routing; the journal version appeared in 2002. With Aloul, they compared track-based and route-based formulations in 2001 and 2004. Later work used SAT for other exact layout tasks, while production FPGA routers stayed with negotiated congestion.

## References
