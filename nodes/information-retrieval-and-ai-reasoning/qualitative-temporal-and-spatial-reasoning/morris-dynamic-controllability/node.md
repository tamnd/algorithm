---
tag: KN0N0A
kind: algorithm
slug: morris-dynamic-controllability
name: Morris's dynamic controllability algorithm
aliases:
- Morris-Muscettola-Vidal algorithm
area: information-retrieval-and-ai-reasoning/qualitative-temporal-and-spatial-reasoning
level: research
summary: Morris's 2006 check of dynamic controllability for an STNU. It runs K rounds of shortest-path propagation from the lower-case edges and tests the AllMax projection, in O(N^4) time.
model: word-ram
complexity:
  vars: {N: the number of time points after the normal form, K: the number of contingent links}
  time: {worst: O(N^4)}
  space: {extra: O(N^2)}
properties: {deterministic: true, exact: true, in_place: false, online: false, recursive: false}
history:
  year: 2006
  people: [Paul Morris]
  note: Morris (CP 2006) characterised dynamic controllability by semi-reducible negative cycles and gave this O(N^4) check. It improved the O(N^5) algorithm of Morris and Muscettola (2005), which followed the pseudo-polynomial algorithm of Morris, Muscettola and Vidal (2001).
prereqs: [simple-temporal-network-with-uncertainty, dynamic-controllability, bellman-ford, dijkstra]
see_also: [simple-temporal-problem, johnson, potential-function-reduced-costs, negative-cycle-detection, difference-constraints, temporal-planning]
sources:
  - paper: doi:10.1007/11889205_28
    title: Paul Morris, A structural characterization of temporal dynamic controllability, CP 2006, Lecture Notes in Computer Science 4204, Springer, 2006
    locator: pages 375 to 389 (Section 3.1 the reductions and the normal form, Section 3.2 Theorems 1 and 2 on semi-reducible paths and moat edges, Section 3.3 Theorem 3 and the procedure fastDCcheck with its O(N^4) bound, Section 4 execution)
  - paper: "Paul Morris and Nicola Muscettola, Temporal dynamic controllability revisited, Proceedings of AAAI-05, AAAI Press, 2005"
    locator: pages 1193 to 1198 (the labelled distance graph, the AllMax projection and the first strongly polynomial check, in O(N^5) time)
  - paper: "Paul Morris, Nicola Muscettola and Thierry Vidal, Dynamic control of plans with temporal uncertainty, Proceedings of IJCAI-01, Morgan Kaufmann, 2001"
    locator: pages 494 to 502 in dblp (the definition of dynamic controllability, the reductions with waits, and a pseudo-polynomial check)
  - paper: doi:10.1007/978-3-319-07046-9_33
    title: Paul Morris, Dynamic controllability and dispatchability relationships, CPAIOR 2014, Lecture Notes in Computer Science 8451, Springer, 2014
    locator: pages 464 to 479 (an O(N^3) check that processes the negative nodes one at a time)
  - paper: doi:10.4230/LIPIcs.TIME.2018.8
    title: Massimo Cairo, Luke Hunsberger and Romeo Rizzi, Faster dynamic controllability checking for simple temporal networks with uncertainty, TIME 2018, LIPIcs 120, 2018
    locator: pages 8:1 to 8:16 (the RUL- algorithm, in O(mn + k^2 n + kn log n) time)
  - paper: doi:10.1109/TIME.2009.25
    title: Luke Hunsberger, Fixing the semantics for dynamic controllability and providing a more practical characterization of dynamic execution strategies, TIME 2009, IEEE, 2009
    locator: pages 155 to 162 (a precise definition of dynamic execution strategies and the instantaneous reaction semantics)
  - paper: doi:10.1080/095281399146607
    title: Thierry Vidal and Hélène Fargier, Handling contingency in temporal constraint networks, from consistency to controllabilities, Journal of Experimental and Theoretical Artificial Intelligence 11(1), 1999
    locator: pages 23 to 45 (strong, weak and dynamic controllability, used here for the reference checks)
---

Morris's algorithm decides whether a [simple temporal network with uncertainty](/simple-temporal-network-with-uncertainty/) is [dynamically controllable](/dynamic-controllability/): whether an agent that sees each contingent duration when it ends can always schedule its own time points so that every constraint holds. This page gives the version of Morris (CP 2006), which runs in $O(N^4)$ time. It finds negative cycles of a special kind, called semi-reducible, by $K$ rounds of shortest-path propagation from the lower-case edges, where $K$ is the number of contingent links. It does not compute an execution strategy; Morris's paper gives separate steps for that.

## In plain words

Some durations in a plan are set by the world. A truck trip takes between 1 and 3 hours, and you only learn the real time when the truck arrives. Your own actions can wait for what you have seen so far, but not for the future.

The plan is drawn as a graph of distances between moments. A plain cycle with a negative total means the plan is impossible. With uncertain durations, some negative cycles are harmless, because they assume that you know an arrival time before it happens. The algorithm finds the cycles that are really a problem. Starting from the end of each uncertain trip, it looks for the first place where the path goes below zero, adds a shortcut edge for that piece, and repeats. After at most one round for each uncertain trip, a bad cycle shows up as a plain negative cycle.

## The problem

An STNU has time points $0, \ldots, n-1$, requirement links $lo \le t_v - t_u \le hi$ (either bound may be missing), and $K$ contingent links $A \Rightarrow C$ with integer bounds $0 \le x \le y$: the agent executes the activation point $A$, and nature then chooses $t_C - t_A \in [x, y]$. The contingent points $C$ are distinct, and every other point is executed by the agent. The question is whether a dynamic execution strategy exists. We use the semantics of Morris (2006): the decision to execute a point at time $t$ may depend on the contingent durations that ended before or at $t$. The input is the list of links; the output is true or false.

Cost is counted on a word-RAM with $N = n + K$ nodes, since the normal form adds at most one node for each contingent link.

## The algorithm

The algorithm works on the *labelled distance graph*. A requirement $lo \le t_v - t_u \le hi$ gives the ordinary edges $u \xrightarrow{hi} v$ and $v \xrightarrow{-lo} u$. A contingent link $A \Rightarrow C$ with bounds $[0, y]$ gives the ordinary edges $A \xrightarrow{y} C$ and $C \xrightarrow{0} A$, the *lower-case edge* $A \xrightarrow{c:0} C$ (nature may choose the smallest duration) and the *upper-case edge* $C \xrightarrow{C:-y} A$ (nature may choose the largest one). The *AllMax projection* is the [simple temporal problem](/simple-temporal-problem/) made of the ordinary and the upper-case edges, with the labels dropped.

```pseudo id=main
MORRIS-DC(STNU)
L1  put the network in normal form: each A ⇒ C in [x, y] with x > 0 becomes A → A' in [x, x] and A' ⇒ C in [0, y - x]
L2  build the labelled distance graph G; K ← the number of contingent links
L3  for round ← 0 to K do
L4      h ← Bellman-Ford potential of the AllMax projection of G
L5      if the AllMax projection has a negative cycle then return false
L6      if round = K then return true
L7      for each lower-case edge e = A --c:0--> C do
L8          from C, find shortest paths over ordinary edges and over upper-case edges not labelled C, expanding only nodes at distance ≥ 0
L9          for each node v first reached at distance d < 0 by an edge with label ℓ, record the edge A → v with weight d and label ℓ
L10     add the recorded edges to G
```

Line L1 moves each positive lower bound onto a new requirement link. Morris (2006, Section 3.1) shows that this keeps dynamic controllability, and it makes every lower-case edge have weight 0. Line L2 builds the graph as above.

Lines L4 and L5 test the AllMax projection with [Bellman-Ford](/bellman-ford/). A negative cycle there is a contradiction that holds even if the agent knew every duration in advance. If there is no such cycle, $h$ is a feasible potential.

Lines L7 to L9 are one round of propagation. For a lower-case edge $e$ from $A$ to $C$, line L8 runs [Dijkstra's algorithm](/dijkstra/) from $C$ on the weights $w + h_u - h_v$, which are non-negative, as in [Johnson's algorithm](/johnson/). It skips lower-case edges and the upper-case edge of the same link, and it stops at the first node of each path whose true distance from $C$ is negative. That node ends the *extension* of $e$, and the last edge is its *moat edge*. Line L9 records the edge from $A$ that the reductions of Morris derive from $e$ followed by the extension: its weight is the distance $d$ and its label is the label of the moat edge, ordinary or upper-case.

Line L10 adds the new edges only after the round, so the potential $h$ stays valid during the round. Line L6 makes the last check after round $K - 1$: the loop tests the AllMax projection $K + 1$ times.

## Example

Take one contingent link $A \Rightarrow C$ with bounds $[1, 3]$ and a free point $B$ with the requirement $t_C - t_B = 1$. Every single duration has a schedule ($t_B = t_C - 1$), so the network is weakly controllable. But $B$ must be executed one unit before $C$, so the agent must fix $t_B$ before it sees $t_C$, and no choice works for both $t_C = t_A + 1$ and $t_C = t_A + 3$. Line L1 adds $A'$ with $t_{A'} = t_A + 1$ and the link $A' \Rightarrow C$ with bounds $[0, 2]$. The table shows the run, with the nodes $A$, $C$, $B$, $A'$.

| Step | State |
| --- | --- |
| L2 | ordinary edges $A \xrightarrow{1} A'$, $A' \xrightarrow{-1} A$, $A' \xrightarrow{2} C$, $C \xrightarrow{0} A'$, $B \xrightarrow{1} C$, $C \xrightarrow{-1} B$; upper-case edge $C \xrightarrow{C:-2} A'$; lower-case edge $A' \xrightarrow{c:0} C$; $K = 1$ |
| L4, round 0 | the AllMax projection is consistent; $h = (-3, 0, -1, -2)$ for $(A, C, B, A')$ |
| L8 from $C$ | $C \to B$ gives $-1$, a moat end; $C \to A'$ gives $0$, expanded; $A' \to A$ gives $-1$, a moat end |
| L9 | record $A' \xrightarrow{-1} B$ and $A' \xrightarrow{-1} A$ (the second is already in $G$) |
| L10 | add $A' \xrightarrow{-1} B$ |
| L4, round 1 | the cycle $A' \xrightarrow{-1} B \xrightarrow{1} C \xrightarrow{C:-2} A'$ has weight $-2$ |
| L5 | return false |

The new edge says that $B$ must come at least 1 after $A'$, because nature may end the link at once. Together with the case where nature waits the full 2 units, this is a contradiction. If the requirement is instead $0 \le t_B - t_C \le 1$, the round from $C$ finds only the moat end $A$ at distance $-1$, which adds nothing new, and the check of round 1 returns true: the agent waits for $C$ and then executes $B$. That network is dynamically controllable but not strongly controllable, since no fixed time for $B$ works for every duration.

## Correctness

The method rests on Theorem 1 of Morris (2006): an STNU is dynamically controllable if and only if its labelled distance graph has no *semi-reducible* negative cycle, that is, a negative cycle that the reductions of Morris can turn into a cycle without lower-case edges. Every edge that line L9 records is derived by those reductions, so the added edges never change the answer, and a negative cycle in the AllMax projection proves that the network is not controllable.

For the other direction, Theorem 3 of Morris (2006) says that a network with a semi-reducible negative cycle also has one whose extensions nest to depth at most $K$. Each round replaces every innermost extension by one edge, so the depth drops by one in each round, and after at most $K$ rounds the cycle has no lower-case edges. The check at line L4 then finds it. The proof, with the reason for the $K + 1$ checks, is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

Line L1 adds at most $K$ nodes, so $N \le n + K$. Every edge that line L10 adds starts at the start of a lower-case edge, and an upper-case edge labelled with a link always ends at the activation point of that link, because the reductions keep the target of an upper-case edge. So there are at most $N^2$ ordinary edges and at most $N K$ upper-case edges at any time, and the graph has $E = O(N^2)$ edges. This is also the space bound.

Morris (2006) counts $K + 1$ Bellman-Ford runs of $O(E N)$ each and $K$ Dijkstra runs per round of $O(E + N \log N)$ each with a heap. With $E \le E_0 + K N$ this gives $O(K E_0 N + K^2 N^2 + K^2 N \log N)$, and with $K \le N$ and $E_0 \le N^2$ it is $O(N^4)$ in the worst case. The implementation here uses the array form of Dijkstra's algorithm, $O(N^2)$ per run, so a round costs $O(N^3)$ for Bellman-Ford and $O(K N^2)$ for the searches, and the total is $O(K N^3)$, which is also $O(N^4)$.

## Properties

- **Exact.** It decides dynamic controllability under the semantics of Morris (2006), with no approximation and no dependence on the size of the bounds.
- **Strongly polynomial.** The running time does not depend on the numbers in the bounds, unlike the algorithm of Morris, Muscettola and Vidal (2001).
- **A decision only.** It does not return a strategy. To execute the network, Morris (2006, Section 4) adds the wait edges and the lower-case consequences in post-processing steps of the same cost.
- **Integer bounds are not needed.** The method works with real bounds; the tests use integers so that the results can be compared exactly.

## Variants and improvements

- **Morris, Muscettola and Vidal (2001).** The first check, with reductions that create waits, is pseudo-polynomial in the size of the bounds.
- **Morris and Muscettola (2005).** A labelled distance graph, the AllMax projection and a cutoff on the number of passes give the first strongly polynomial check, $O(N^5)$.
- **Morris (2014).** Processing one negative node at a time, with a backward search from each negative node, gives an $O(N^3)$ check.
- **Cairo, Hunsberger and Rizzi (2018).** The RUL- algorithm runs in $O(mn + k^2 n + kn \log n)$ time for $n$ points, $m$ edges and $k$ contingent links.
- **Semantics.** Hunsberger (2009) made the meaning of dynamic strategies precise. Some later work uses a stricter semantics in which a reaction must come strictly after the event it reacts to; a check for one semantics is not a check for the other.

## When to use it

Use it to test a plan with uncertain durations before it runs, when the agent will see each duration as it ends: in temporal planning, scheduling for robots and space missions, and workflow systems. For large networks, the $O(N^3)$ algorithm of Morris (2014) or the RUL- algorithm is faster. If there are no contingent links, the question is consistency of a [simple temporal problem](/simple-temporal-problem/), which [Bellman-Ford](/bellman-ford/) answers in $O(N E)$. If the agent cannot observe durations at all, test strong controllability, which is one STP check after a rewrite of the bounds. This page is the 2006 version; it is easier to prove than the 2014 one and has a published pseudocode.

## Pitfalls

- **Testing only at the start of each round.** If line L6 is moved before line L4, or the loop of line L3 runs only $K$ times, the edges from the last round are never tested. The example above has $K = 1$ and needs one round and then a check; with only $K$ checks it is accepted. Line L3 must run $K + 1$ checks, with line L6 after line L5.
- **Adding edges during the round.** If line L10 is merged into line L9, the potential $h$ of line L4 is no longer feasible for the new negative edges, and the Dijkstra run of line L8 can give wrong distances. Add the edges after all lower-case edges are done.
- **Using the upper-case edge of the same link.** If line L8 also follows $C \xrightarrow{C:-y} A$, then a single contingent link, which is always controllable, is reported as not controllable, because the path $C \to A$ is a drop at once. Line L8 must skip the upper-case edge labelled with the same link.
- **Expanding negative nodes.** If line L8 goes on past a node at negative distance, it records edges for paths that are not extensions, and the edges that line L9 adds are not derived by the reductions.
- **Skipping the normal form.** Line L9 assumes that the lower-case edge has weight 0. Without line L1 the weight $x$ of the edge must be added to $d$, and the label removal rule changes. The normal form keeps both simple.

## Implementations

## History

Vidal and Fargier (1999) defined strong, weak and dynamic controllability for networks with contingent durations. Morris, Muscettola and Vidal (2001) gave the first check for dynamic controllability, which is pseudo-polynomial. Morris and Muscettola (2005) introduced the labelled distance graph and the first strongly polynomial check, in $O(N^5)$. Morris (2006) characterised dynamic controllability by semi-reducible negative cycles, proved the nesting depth bound and gave the $O(N^4)$ algorithm on this page. Morris (2014) reduced the bound to $O(N^3)$, and Cairo, Hunsberger and Rizzi (2018) gave the RUL- algorithm.

## References
