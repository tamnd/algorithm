---
title: The K-round propagation decides dynamic controllability
proves: [correctness, termination]
status: full
---

This proof follows Morris (CP 2006, Sections 3.1 to 3.3). It uses three results of that paper, which we quote with their numbers: the reductions are sound and keep reduced distance (Section 3.1), Theorem 1 and Theorem 2 (Section 3.2) and Theorem 3 (Section 3.3). The semantics is the one of that paper: an execution decision at time $t$ may depend on the contingent durations that finished before or at $t$.

## Setting

Line L1 puts the network in normal form: each contingent link $A \Rightarrow C$ with bounds $[x, y]$ and $x > 0$ becomes a requirement link $A \to A'$ with bounds $[x, x]$ and a contingent link $A' \Rightarrow C$ with bounds $[0, y - x]$. Morris (Section 3.1) shows that a network is dynamically controllable (DC) exactly when its normal form is DC: the new point $A'$ is executed exactly $x$ after $A$, so a strategy for one network is a strategy for the other. After L1 every contingent link has the bounds $[0, y]$, and $K$ is the number of contingent links.

Line L2 builds the labelled distance graph. A requirement $lo \le t_v - t_u \le hi$ gives the ordinary edges $u \xrightarrow{hi} v$ and $v \xrightarrow{-lo} u$. A contingent link $A \Rightarrow C$ with $[0, y]$ gives the ordinary edges $A \xrightarrow{y} C$ and $C \xrightarrow{0} A$, the lower-case edge $A \xrightarrow{c:0} C$ and the upper-case edge $C \xrightarrow{C:-y} A$. The *reduced distance* of a path is the sum of its weights with the labels ignored. The *AllMax projection* is the STN with the ordinary edges and the upper-case edges, labels dropped. In the code, a lower-case edge is the triple `(a, c, i)` of the list `lower`, an upper-case edge is the key `(c, a, i)`, and an ordinary edge is the key `(u, v, None)`.

The reductions of Morris (2006) are the No-case, Upper-case, Lower-case and Cross-case reductions and Label removal. Each one adds an edge that every dynamic strategy satisfies, and each new edge has the reduced distance of the two edges it replaces. A path is *semi-reducible* if a sequence of reductions turns it into a path without lower-case edges.

- **Theorem 1 (Morris 2006).** The network is DC if and only if its labelled distance graph has no semi-reducible cycle of negative reduced distance.

For a lower-case edge $e$ in a path $P$, an edge $e'$ after $e$ is a *drop edge* if the reduced distance in $P$ from the end of $e$ to the end of $e'$ is negative. The first drop edge is the *moat edge*, and the subpath from the end of $e$ to the end of the moat edge is the *extension* of $e$. Every proper prefix of an extension has non-negative reduced distance. The moat edge is *usable* unless it is the upper-case edge of the same contingent link as $e$. An extension has a *breach* if it contains the upper-case edge of the link of $e$.

- **Theorem 2 (Morris 2006).** A path is semi-reducible if and only if every lower-case edge in it has a usable moat edge. In the proof, an innermost extension with a usable moat edge $e'$ reduces to one edge with the reduced distance of the extension, labelled as $e'$ (the interior labels are removed by Label removal, because all proper prefixes are non-negative), and then a Lower-case or Cross-case reduction with $e$ gives one edge from the start of $e$ with the same label as $e'$.
- **Theorem 3 (Morris 2006).** If there is a semi-reducible negative cycle, then there is one that is breach-free and in which all repetitions of a lower-case edge are flat. In such a cycle the extensions nest to depth at most $K$.

## Soundness of the added edges

**Lemma 1.** Every edge that line L10 adds is an edge that a sequence of reductions derives from the current graph. So the added edges do not change whether the network is DC.

*Proof.* Line L8 runs from $C$, the end of the lower-case edge $e = A \xrightarrow{c:0} C$. It uses ordinary edges and upper-case edges whose label is not the link $i$ of $e$ (the test `lab != own` in `_propagate`), and it never uses a lower-case edge, because lower-case edges are not in `edges`. A node is expanded only when its true distance from $C$ is non-negative (the test `du < 0` skips it). So every path that the search follows to record a value `moats[(C, v, lab)] = d` with $d < 0$ is a breach-free, lower-case-free path from $C$ whose proper prefixes all have non-negative reduced distance and whose last edge has the label `lab`. That last edge is the moat edge of $e$ on the path $e$ followed by this path, and it is usable because its label is not $i$. By the proof of Theorem 2 the path $e$ followed by the extension reduces to one edge $A \to v$ with weight $0 + d$ and the label `lab`. Line L9 keeps the smallest such weight and line L10 adds it. Reductions are sound and keep DC. $\square$

The search uses the potential $h$ of line L4 to run Dijkstra's method on the weights $w + h_u - h_v \ge 0$; `du` recovers the true distance $\text{red}_u + h_u - h_{\text{start}}$. Since $h$ is a feasible potential for all edges present during the round, and the new edges are added only after the round (line L10), these reweighted weights stay non-negative during the round, so each distance is a shortest distance over the allowed paths.

**Lemma 2.** If line L5 returns false, the network is not DC.

*Proof.* By Lemma 1 the current graph is the original graph plus edges that every dynamic strategy must satisfy. Line L4 found a negative cycle among ordinary and upper-case edges. A negative cycle without lower-case edges is semi-reducible (no reduction is needed), so by Theorem 1 the extended network, and by Lemma 1 the original network, is not DC. $\square$

## Completeness

**Lemma 3.** Suppose the graph at the start of a round has a breach-free semi-reducible negative cycle $P$ with flat repetitions whose extensions nest to depth $m \ge 1$. Then the graph at the end of the round has a semi-reducible negative cycle whose extensions nest to depth at most $m - 1$.

*Proof.* Take an innermost extension $Q$ of a lower-case edge $e = A \xrightarrow{c:0} C$ in $P$, with moat edge $e'$ ending at $v$. $Q$ has no lower-case edge (it is innermost), no upper-case edge with the label of $e$ (breach-free), all proper prefixes non-negative and a negative total. So $Q$ is one of the paths that line L8 may follow from $C$, and the search finds a value $d \le D(Q)$ for some key $(C, u, \text{lab})$ on its way. Two cases.

- The search reaches $v$ through the last edge of $Q$ or a shorter allowed path with the same last label, and line L10 adds $A \to v$ with weight at most $D(Q) < 0$ and the label of $e'$.
- The search stops at an earlier node $u$ of $Q$ with a negative distance, so it adds $A \to u$ with a negative weight $d_u$. The prefix of $Q$ up to $u$ has non-negative reduced distance, so $d_u$ is smaller than it, and the rest of $Q$ after $u$ keeps the cycle negative. This is Morris's remark in Section 3.3: propagating over shortest allowed paths only finds tighter edges earlier.

In both cases replace $e$ and the covered part of $Q$ in $P$ by the new edge. The reduced distance does not grow, so the cycle is still negative. The new edge is ordinary or upper-case with a label different from every lower-case edge that it can be the moat of in $P$, because the old moat edges of the outer extensions are kept (the new edge lies inside an extension, and the prefix/postfix property of the outer extensions is kept since the new weight is at most the weight of the part it replaces). By Theorem 2 the cycle is still semi-reducible. Every innermost extension is removed in the same round, since line L7 runs over every lower-case edge, so the depth drops by one. Theorem 3 applied to the new cycle gives again a breach-free cycle with flat repetitions and depth at most $m - 1$. $\square$

**Lemma 4.** If the network is not DC, line L5 returns false in one of the $K + 1$ checks.

*Proof.* By Theorem 1 and Theorem 3 the graph has a breach-free semi-reducible negative cycle with flat repetitions and nesting depth $m \le K$. By Lemma 3 after $m$ rounds there is a negative cycle of depth 0, which is a cycle without lower-case edges, so it is a negative cycle of the AllMax projection. The check of line L4 at the start of round $m$ finds it. Since $m \le K$ and the loop of line L3 runs the checks for the rounds $0, 1, \ldots, K$, the check happens. $\square$

The check after the last round matters. If the check runs only at the start of each of $K$ rounds, the edges added in the last round are never tested. The example with one contingent link $A \Rightarrow C$ in $[1, 3]$ and the requirement $t_B - t_C = -1$ (point $B$ one unit before $C$) needs exactly one round of edges and then a check: with $K = 1$ and no final check, it is accepted, which is wrong.

**Theorem.** `morris_dc` returns true if and only if the network is DC.

*Proof.* If it returns false, then by Lemma 2 the network is not DC. If the network is not DC, then by Lemma 4 it returns false. $\square$

## Termination

The loop of line L3 runs at most $K + 1$ times. In each round, line L7 runs over $K$ lower-case edges, and each call of line L8 is one Dijkstra run over at most $N$ nodes, where $N$ is the number of nodes after line L1. Bellman-Ford in line L4 makes at most $N$ passes. All loops are finite, so the algorithm stops. $\blacksquare$
