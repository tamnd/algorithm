---
title: The routing formula is satisfiable exactly when the fixed global routing has a legal detailed routing at width W, with models and routings in one-to-one correspondence
proves: [correctness]
status: full
---

## Setting

The width is $W \ge 1$, and every channel segment has the tracks $0, \ldots, W - 1$. The global routing is fixed: net $n$ has a set $\mathrm{Seg}(n)$ of distinct segments and a set $\mathrm{E}(n)$ of edges $(s, s', \kappa)$ with $s, s' \in \mathrm{Seg}(n)$, where $\kappa$ names the two sides of the switch block at which $s$ and $s'$ meet. The switch pattern gives, for each $\kappa$ and each track $t$, a set $P(\kappa, t) \subseteq \{0, \ldots, W - 1\}$ of tracks of $s'$ that a switch joins to track $t$ of $s$. The pins reach every track of their segments (the connection blocks are full), so the pins add no constraint.

A **detailed routing** is a map $\rho$ from the pairs $(n, s)$ with $s \in \mathrm{Seg}(n)$ to tracks. It is **legal** when

1. (exclusivity) $\rho(n, s) \ne \rho(m, s)$ for all nets $n \ne m$ that both use $s$, and
2. (connectivity) $\rho(n, s') \in P(\kappa, \rho(n, s))$ for every edge $(s, s', \kappa) \in \mathrm{E}(n)$.

The formula $F$ has a variable $x_{n,s,t}$ for each pair $(n, s)$ and each track $t$, and these clauses:

- (L2) $\bigvee_t x_{n,s,t}$ for each pair $(n, s)$;
- (L3) $\neg x_{n,s,t} \vee \neg x_{n,s,u}$ for each pair $(n, s)$ and tracks $t < u$;
- (L4) $\neg x_{n,s,t} \vee \neg x_{m,s,t}$ for each segment $s$, nets $n \ne m$ that use $s$, and track $t$;
- (L5) $\neg x_{n,s,t} \vee \bigvee_{u \in P(\kappa, t)} x_{n,s',u}$ for each edge $(s, s', \kappa) \in \mathrm{E}(n)$ and track $t$.

These are the clauses that `encode` builds, line by line.

## The correspondence

For a detailed routing $\rho$, let $\alpha_\rho$ be the assignment with $x_{n,s,t}$ true exactly when $\rho(n, s) = t$. For an assignment $\alpha$ that satisfies the clauses L2 and L3, let $\rho_\alpha(n, s)$ be the one track $t$ with $x_{n,s,t}$ true; L2 says there is at least one and L3 says there is at most one.

**Lemma 1.** If $\rho$ is legal, then $\alpha_\rho$ satisfies $F$.

*Proof.* Take each clause in turn. L2: $x_{n,s,\rho(n,s)}$ is true. L3: at most one of $x_{n,s,t}$ and $x_{n,s,u}$ with $t \ne u$ equals $\rho(n, s)$, so one of the negations is true. L4: if both $x_{n,s,t}$ and $x_{m,s,t}$ were true, then $\rho(n, s) = t = \rho(m, s)$, against exclusivity. L5: if $x_{n,s,t}$ is false the clause holds; otherwise $t = \rho(n, s)$, and by connectivity $u = \rho(n, s') \in P(\kappa, t)$, so $x_{n,s',u}$ is a true literal of the clause. $\square$

**Lemma 2.** If $\alpha$ satisfies $F$, then $\rho_\alpha$ is legal.

*Proof.* $\rho_\alpha$ is well defined by L2 and L3. Exclusivity: if $\rho_\alpha(n, s) = \rho_\alpha(m, s) = t$ for $n \ne m$, then $x_{n,s,t}$ and $x_{m,s,t}$ are both true, and the L4 clause for $(s, n, m, t)$ is false, a contradiction. Connectivity: for an edge $(s, s', \kappa)$ of net $n$, let $t = \rho_\alpha(n, s)$. Then $x_{n,s,t}$ is true, so the L5 clause for this edge and $t$ needs some true $x_{n,s',u}$ with $u \in P(\kappa, t)$. The only true variable of the pair $(n, s')$ is the one with $u = \rho_\alpha(n, s')$, so $\rho_\alpha(n, s') \in P(\kappa, t)$. $\square$

**Theorem 3.** $F$ is satisfiable if and only if the global routing has a legal detailed routing at width $W$. The maps $\rho \mapsto \alpha_\rho$ and $\alpha \mapsto \rho_\alpha$ are inverse bijections between the legal detailed routings and the models of $F$.

*Proof.* Lemmas 1 and 2 give both directions of the equivalence. For the bijection: $\rho_{\alpha_\rho} = \rho$, since in $\alpha_\rho$ the true variable of the pair $(n, s)$ is the one of track $\rho(n, s)$. And $\alpha_{\rho_\alpha} = \alpha$ for every model $\alpha$, since L2 and L3 make $x_{n,s,t}$ true exactly for $t = \rho_\alpha(n, s)$, and $F$ has no other variables. $\square$

**Corollary 4 (what UNSAT proves).** If a complete SAT solver reports that $F$ is unsatisfiable, then no legal detailed routing exists for this global routing at width $W$.

*Proof.* A complete solver reports unsatisfiable only when $F$ has no model; by Theorem 3 no legal detailed routing exists. $\square$

The corollary is about the fixed global routing only. Another global routing of the same netlist may route at width $W$, so UNSAT does not prove that the circuit is unroutable on the device at width $W$. If a solver returns a model, line L8 reads $\rho_\alpha$ from it, and Lemma 2 shows that it is legal.

## A legal detailed routing is a routing on the routing resource graph

Let the [routing resource graph](/routing-resource-graph/) have a node for each track of each segment and an edge for each switch. For net $n$, the nodes $(s, \rho(n, s))$ with $s \in \mathrm{Seg}(n)$ are joined by the switches of the edges of $\mathrm{E}(n)$, by connectivity; if these edges form a tree over $\mathrm{Seg}(n)$, so do the chosen nodes. By exclusivity, two nets never use the same node. So a legal detailed routing gives vertex-disjoint trees, one per net, which is a legal routing on that graph, and the pins reach the trees because the connection blocks are full.

## The disjoint pattern

**Theorem 5.** Let $P(\kappa, t) = \{t\}$ for all $\kappa$ and $t$, and let the edges of every net connect its segments. Build the conflict graph $G$ with a vertex per net and an edge between two nets that share a segment. Then the global routing has a legal detailed routing at width $W$ if and only if $G$ has a proper [coloring](/graph-coloring/) with $W$ colors.

*Proof.* If $\rho$ is legal, connectivity gives $\rho(n, s') = \rho(n, s)$ along each edge of net $n$, and since the edges connect $\mathrm{Seg}(n)$, net $n$ has one track $c(n)$ on all its segments. Two nets that share a segment $s$ have $c(n) = \rho(n, s) \ne \rho(m, s) = c(m)$ by exclusivity, so $c$ is a proper coloring. Conversely, a proper coloring $c$ with colors $0, \ldots, W - 1$ gives $\rho(n, s) = c(n)$, which satisfies connectivity because the track never changes and exclusivity because nets that share a segment have different colors. $\square$

In the abstract model of this page, where a route is any connected set of segments, every graph is a conflict graph: give each edge $\{u, v\}$ of the graph its own segment, and let net $u$ use the segments of its edges, joined in a path. So with the disjoint pattern and $W = 3$, deciding whether a legal detailed routing exists is NP-complete by the NP-completeness of 3-coloring. This does not say which graphs arise from the geometry of a real FPGA. $\blacksquare$
