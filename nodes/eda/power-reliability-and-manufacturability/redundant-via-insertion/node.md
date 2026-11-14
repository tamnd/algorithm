---
tag: TMF5WW
kind: technique
slug: redundant-via-insertion
name: Redundant via insertion
aliases:
- double via insertion
- via doubling
area: eda/power-reliability-and-manufacturability
level: advanced
summary: Adds a second via next to single vias after routing, chosen by matching or integer programming, to raise yield and reliability without breaking design rules.
prereqs: [maximum-independent-set, bipartite-matching]
see_also: [line-graph, maximum-matching, hopcroft-karp, binary-integer-programming, r-tree, poisson-yield-model, critical-area, black-equation]
sources:
  - paper: "Kuang-Yao Lee and Ting-Chi Wang, Post-routing redundant via insertion for yield/reliability improvement, Proceedings of the Asia and South Pacific Design Automation Conference (ASP-DAC), 2006, from page 303"
    locator: Problem 1 (insert as many double vias as possible after routing), Definition 1 (feasible double via), Definition 2 (conflict graph), Lemma 1 (reduction to maximum independent set), Fig. 3 (limits of bipartite matching) and the H2K heuristic
  - paper: "Kuang-Yao Lee, Cheng-Kok Koh, Ting-Chi Wang and Kai-Yuan Chao, Optimal post-routing redundant via insertion, Proceedings of the International Symposium on Physical Design (ISPD), 111 to 117, 2008"
    locator: the exact solution of double-cut via insertion as a 0-1 integer linear program, with methods that reduce the problem size and the number of constraints
  - paper: "Gang Xu, Li-Da Huang, David Z. Pan and Martin D. F. Wong, Redundant-via enhanced maze routing for yield improvement, Proceedings of the Asia and South Pacific Design Automation Conference (ASP-DAC), 2005"
    locator: redundant via insertion considered during routing rather than after it
---

Redundant via insertion adds a second via cut next to each single via of a routed layout where the design rules allow it. A via joins wires on two metal layers through one small cut, and a cut can fail open from a defect or a void, or wear out by electromigration. Two cuts in parallel fail only if both fail, so doubling vias raises yield and reliability at little cost. Because candidate positions of nearby vias compete for the same space, the choice is a combinatorial problem: Lee and Wang (2006) reduced it exactly to a [maximum independent set](/maximum-independent-set/) on a conflict graph, and in a special case it becomes [bipartite matching](/bipartite-matching/).

## In plain words

A via is a tiny plug of metal that joins a wire on one layer to a wire on the next. If the plug is bad, the connection is broken. Putting a second plug right next to the first means the connection survives if either one is good.

Each plug usually has a few places where a second one could go: above, below, left or right. But a new plug must keep its distance from wires and plugs of other signals, and two new plugs near each other may get in each other's way.

So the job is to pick at most one spot for each plug, such that no two picks clash, and to pick as many as possible. Choosing greedily, one at a time, can block better choices later.

## When it applies

- After detailed routing, when the routes are fixed and free space around vias is known. Rerouting is not allowed in the basic problem.
- When the foundry recommends or requires double cuts, and the yield gain is worth the added metal and the capacitance it brings.
- When the design rules that a new cut can break involve one new cut, or two new cuts together. This is the condition under which the conflict graph below is exact.
- Not for vias that already sit in a via array, and with care for vias on critical nets, where an off-track cut adds a metal stub.

## The template

For a single via $i$ and a direction $j \in \{\text{up}, \text{down}, \text{left}, \text{right}\}$, the *double via* $dv(i, j)$ is the via $i$ with one extra cut in direction $j$ and the metal extensions that cover it on both layers. It is *feasible* if it breaks no design rule when it is the only change to the layout (Lee and Wang, Definition 1).

```pseudo id=main
REDUNDANT-VIA-INSERTION(routed layout, design rules)
L1  V ← ∅; E ← ∅
L2  for each single via i, for each direction j
L3      if dv(i, j) is feasible then add vertex v(i, j) to V
L4  for each pair v(i, j), v(i, j′) of the same via: add an edge
L5  for each pair v(i, j), v(i′, j′) of nearby vias, found with a spatial index
L6      if dv(i, j) and dv(i′, j′) together break a rule then add an edge
L7  S ← an independent set of G = (V, E), as large as possible
L8  for each v(i, j) in S: replace via i with dv(i, j)
L9  return the layout
```

The holes are the rule checker in lines L3 and L6, the spatial index in line L5 (Lee and Wang use an [R-tree](/r-tree/) and sort the vias by $x$), and the solver in line L7: an exact [0-1 integer program](/binary-integer-programming/), a heuristic for the maximum independent set, or a matching when the special case below holds.

**Assumption P (pairwise rules).** A set $D$ of double vias, at most one per single via, breaks a rule if and only if some member breaks a rule alone, or some two members break a rule together.

The "if" half says that adding metal never repairs a violation, which holds for spacing rules. The "only if" half says that no violation needs three or more new cuts. Rules on via density in a window, or on a line end with two neighbors, can break it.

**Claim 1 (the conflict graph is exact).** Under assumption P, the sets of double vias that may be inserted together are exactly the sets $\{dv(i, j) : v(i, j) \in S\}$ for independent sets $S$ of $G$, and the number of inserted double vias equals $|S|$. Hence a maximum independent set of $G$ gives the largest number of redundant vias that can be inserted with no violation.

*Proof.* Let $D$ be a legal insertion: it has at most one double via per single via, and the layout with all of $D$ breaks no rule. By the "if" half of P, no member breaks a rule alone, so each member is feasible and has a vertex by line L3. No two members break a rule together, so no edge of line L6 joins them, and no two share a via, so no edge of line L4 joins them. Thus the vertices of $D$ form an independent set of the same size.

Conversely, let $S$ be independent. By line L4 it has at most one vertex per via, so it describes a valid choice with $|S|$ double vias. Each is feasible by line L3, and no two break a rule together, since the edge of line L6 would be present. By the "only if" half of P, the whole set breaks no rule. The two maps are inverse to each other, so the maximum sizes agree. $\square$

Lee and Wang state this reduction as their Lemma 1. Maximum independent set is NP-hard in general graphs, so exact solvers are integer programs, which Lee, Koh, Wang and Chao (2008) made fast enough for real designs by shrinking the problem first.

**Claim 2 (when matching is exact).** Suppose every conflict of line L6 comes from two double vias whose extra cuts use the same grid site. Let $B$ be the bipartite graph whose left vertices are the single vias, whose right vertices are the candidate sites, and with an edge from via $i$ to site $s$ for each feasible double via that puts its extra cut on $s$. Then $G$ is the [line graph](/line-graph/) of $B$, and the independent sets of $G$ are exactly the matchings of $B$. So a [maximum matching](/maximum-matching/) of $B$, found in polynomial time, for example by [Hopcroft-Karp](/hopcroft-karp/), solves the problem.

*Proof.* Each vertex of $G$ is a feasible double via, which is one edge of $B$. Two vertices of $G$ are adjacent if they belong to the same via (line L4) or, by the supposition, if they use the same site. Those are exactly the cases in which the two edges of $B$ share an endpoint. So $G$ is the line graph of $B$, and a set of edges of $B$ with no shared endpoint, a matching, is the same as a set of vertices of $G$ with no edge between them. $\square$

**Why matching fails in general.** A line graph has no *claw*, an induced star with three leaves. If a vertex of $G$, an edge $uv$ of $B$, has three neighbors, each shares $u$ or $v$ with it, so two of them share the same endpoint and are adjacent. Now let the redundant cut of via $V_0$ sit in a gap where it is too close to the redundant cuts of three neighbor vias of other nets, $V_1$, $V_2$ and $V_3$, which are far from one another. Then $G$ contains a claw, so no bipartite graph $B$ has $G$ as its line graph, and no matching model of this kind is exact. Lee and Wang give a concrete case (their Fig. 3) where the bipartite models proposed earlier either allow an illegal pair or miss the optimum.

## Classic examples

**Greedy order matters.** Via $A$ has free sites on its left and on its right; via $B$, just to the right of $A$, can only use that same middle site. The vertices are $a_L$, $a_M$ and $b_M$, with edges $a_L a_M$ (same via) and $a_M b_M$ (same site). A greedy pass that takes $a_M$ first ends with one redundant via. The maximum independent set $\{a_L, b_M\}$ gives two. This graph is a path, a line graph, so matching finds the optimum. Lee and Wang show a larger case (their Fig. 1) where a poor choice inserts four redundant vias and the best choice inserts five.

**Fewest options first.** A natural greedy rule serves first the vias with the fewest feasible double vias, then deletes the conflicting vertices. Lee and Wang implemented this rule, which they call FNF, for comparison. It solves the example above, since $B$ has one option and $A$ has two. Their own heuristic H2K repeatedly takes a small subgraph of high-priority vertices, finds a maximal independent set in it, adds it to the answer and deletes the neighbors. In their experiments it inserted up to 21.24% more redundant vias than a commercial tool and an earlier method.

**Effect on yield.** As an illustration with assumed numbers, suppose cuts fail open independently with probability $q$. A single via fails with probability $q$, a double via with $q^2$. With $N = 10^7$ vias and $q = 10^{-7}$, the expected number of failed single vias is $Nq = 1$, so the Poisson yield is $e^{-1} \approx 0.37$ (see the [Poisson yield model](/poisson-yield-model/)). If a fraction $f$ of the vias is doubled, the expected number of failures is $(1 - f) N q + f N q^2 \approx (1 - f) N q$, so the yield is about $e^{-(1 - f)}$: $0.90$ for $f = 0.9$ and $0.99$ for $f = 0.99$. The undoubled vias dominate, which is why the count of inserted vias is the objective. Real cut failures are not independent, since one large defect can cover both cuts, so this calculation is an upper estimate of the gain.

## Variations

- **Exact integer programming.** One 0-1 variable per vertex of $G$, at most one per via, and $x_u + x_v \le 1$ per conflict edge, maximizing the sum (Lee, Koh, Wang and Chao 2008). Via density limits in a window are linear constraints on the same variables, which is how rules that break assumption P can still be handled exactly.
- **On-track preference.** A redundant cut on the wire that already leaves the via needs no extra metal stub. Lee and Wang give two methods, a modified heuristic and a post processor, that raise the share of on-track cuts.
- **During routing.** Xu, Huang, Pan and Wong (2005) make the router itself leave room for redundant vias, which raises the number that can later be inserted.
- **With line-end extension or wire bending.** Later work by Lee, Wang and others allows small changes to the wires near the via, such as extending a line end or bending a wire, to create more feasible sites.
- **Via arrays.** Power and clock nets use arrays of many cuts; the same reliability reasoning applies to how many cuts a connection needs, under the current limits of the [Black equation](/black-equation/).

## Pitfalls

- **Triple conflicts.** A rule that three new cuts break together, but no two, is missed by the conflict graph. Run [design rule checking](/design-rule-checking/) after insertion, or add those rules as constraints of an integer program.
- **Same-net pairs.** Two double vias of the same net may sit close without a violation, as in Lee and Wang's Fig. 5. Line L6 must check the actual rule, not only the overlap of the search windows.
- **Greedy is not optimal.** Insertion in a fixed order can block better choices, as in the example. Use a better independent set heuristic, or the integer program on each connected component of the conflict graph.
- **Coupling and timing.** Extra metal changes capacitance. On critical nets an off-track redundant via may cost more delay than it saves in yield.
- **Assumed independence.** The yield gain is often quoted from $q$ to $q^2$, which holds only for independent failures. Defects that cover both cuts limit the gain, which is the [critical area](/critical-area/) of the via pair.

## Exercises

1. Draw the conflict graph for four vias in a row, each with one free site on each side, where adjacent vias share the site between them. Find a maximum independent set, and check it against a maximum matching of the bipartite graph of Claim 2.
2. Give a design rule that breaks assumption P, with three double vias that are pairwise legal but not legal together.
3. Show that every graph is the conflict graph of some layout if conflicts can be arbitrary pairs. Conclude that the general problem is as hard as maximum independent set.
4. Write the 0-1 integer program of the first variation for the example "Greedy order matters", and solve its linear relaxation. Is the relaxation integral?
5. With $N = 10^8$ vias and $q = 10^{-9}$, find the fraction of vias that must be doubled to reach a yield of $0.99$ under independent failures.

## References
