---
title: The Ramalingam-Reps algorithm keeps the exact distances
proves: [correctness]
status: full
---

All weights are positive. Write $d$ for the stored distances and $\mathrm{dist}$ for the true distances in the current graph; $\mathrm{dist}(s) = 0$, and $\mathrm{dist}(v) = \infty$ if $v$ is not reachable. The invariant is:

- **(D)** $d(v) = \mathrm{dist}(v)$ for every $v$.
- **(C)** For every $v \ne s$ with $d(v) < \infty$, $c(v)$ is the number of edges $(u, v)$ with $d(u) + w(u, v) = d(v)$.

Line L1 establishes both by Dijkstra's algorithm and direct counting. We use two standard facts.

**Fact 1 (the Bellman conditions).** Let $D$ be a function on $V$ with $D(s) = 0$, $D(v) \le D(u) + w(u, v)$ for every edge, and such that every $v \ne s$ with $D(v) < \infty$ has an in-edge $(u, v)$ with $D(u) + w(u, v) = D(v)$. Then $D = \mathrm{dist}$.

*Proof.* The first condition gives $D \le \mathrm{dist}$ by induction along a shortest path. For the reverse, follow tight in-edges back from $v$; the values $D$ strictly decrease along the way since weights are positive, so the walk does not repeat a vertex and must end at $s$, giving a path of length $D(v)$, so $\mathrm{dist}(v) \le D(v)$. $\square$

**Fact 2 (Dijkstra with fixed sources).** Let $S \subseteq V$, and let every vertex $x \in S$ start with a value $D_0(x)$, the least of the values $D(y) + w(y, x)$ over edges from vertices $y \notin S$ (fixed values). Dijkstra's algorithm restricted to edges inside $S$, started from all of $S$ with these values, ends with $D(x) = \min(D_0(x), \min_{(y, x), y \in S} D(y) + w(y, x))$ for all $x \in S$, and $D(x)$ is the least length of a walk that starts at a vertex $y \notin S$ with value $D(y)$ and then stays in $S$.

*Proof.* This is Dijkstra's algorithm on the graph $S$ plus a super source joined to each $x \in S$ by an edge of weight $D_0(x)$; all weights are non-negative. $\square$

Both facts imply the counts: once (D) holds, (C) holds if the counts are recomputed wherever a tight edge may have appeared or disappeared, and we check that below.

**Lemma 1 (decrease).** DECREASE$(u, v, w)$ keeps (D) and (C).

*Proof.* Let $\mathrm{dist}'$ be the new distances and $d$ the old ones. Distances can only drop. If $d(u) + w \ge d(v)$, then no path through the new edge is shorter than $d(v)$, and no vertex beyond $v$ improves: a path through $(u, v)$ to $z$ has length at least $d(u) + w + \mathrm{dist}(v, z) \ge d(v) + \mathrm{dist}(v, z) \ge d(z)$. So $\mathrm{dist}' = d$. The edge $(u, v)$ is the only one that can change its tightness, and line L2 adds one to $c(v)$ exactly when it becomes tight; it was not tight before, since its old weight was larger or it was absent.

Otherwise, let $C$ be the set of vertices with $\mathrm{dist}'(z) < d(z)$. Every shortest path to such a $z$ in the new graph uses $(u, v)$, so $\mathrm{dist}'(z) = d(u) + w + \mathrm{dist}'(v, z)$, where $\mathrm{dist}'(v, z)$ is a distance in the new graph, and the part of the path after $v$ consists of vertices of $C$ (each prefix of it is also shortest and uses the new edge, so its endpoint improved). Lines L3 and L4 are Dijkstra's algorithm from $v$ with initial value $d(u) + w$, where every other vertex starts at its old value $d(z)$ and only lower values are accepted. By the standard proof of Dijkstra's algorithm on non-negative weights, it ends with $D(z) = \min(d(z), d(u) + w + \mathrm{dist}'(v, z))$, which is $\mathrm{dist}'(z)$ for every $z$. So (D) holds.

For (C): an edge $(x, z)$ changes its tightness only if $d(x)$ or $d(z)$ changed. Line L5 recounts every changed vertex from all its in-edges. For an unchanged $z$ and a changed in-neighbor $x$, it removes the old tightness of $(x, z)$ and adds the new one, which is exactly the change of $c(z)$. $\square$

**Lemma 2 (increase: phase 1).** Suppose $(u, v)$ was tight and $c(v) - 1 = 0$ after line L6. Let $\mathrm{dist}'$ be the new distances. Phase 1 (line L7) ends with $A = \{z : \mathrm{dist}'(z) > d(z)\}$.

*Proof.* Distances can only grow. Let $T$ be the set of edges tight for $d$ in the old graph; with positive weights $T$ is acyclic, since $d$ strictly increases along a tight edge.

First, every $z \in A$ has $\mathrm{dist}'(z) > d(z)$. When $z$ enters $A$, every tight in-edge of $z$ in the new graph comes from a vertex of $A$ (the counter counts the tight in-edges not yet known to come from $A$, and for $v$, the edge $(u, v)$ no longer exists or is no longer tight). Order $A$ by entry time. By induction, suppose all earlier vertices of $A$ have $\mathrm{dist}' > d$. A shortest new path to $z$ of length $d(z)$ would end with an edge $(x, z)$ with $\mathrm{dist}'(x) + w(x, z) = d(z)$ and $\mathrm{dist}'(x) \ge d(x)$, and $d(x) + w(x, z) \ge d(z)$ by (D), so $(x, z)$ is tight with $\mathrm{dist}'(x) = d(x)$. But tight edges into $z$ come from $A$, whose vertices entered before $z$ or are $z$ itself; this contradicts the induction hypothesis (and $x = z$ is impossible). So $\mathrm{dist}'(z) > d(z)$.

Second, every $z$ with $\mathrm{dist}'(z) > d(z)$ is in $A$. Go by induction on $d(z)$. Such a $z$ is not $s$ and has $d(z) < \infty$. Each tight in-edge $(x, z)$ of the old graph either is $(u, v)$, which no longer counts, or comes from a vertex $x$ with $d(x) < d(z)$. If $\mathrm{dist}'(x) = d(x)$ for such an $x$, then $\mathrm{dist}'(z) \le d(x) + w(x, z) = d(z)$, a contradiction. So every such $x$ has $\mathrm{dist}'(x) > d(x)$ and, by induction, is in $A$. When $x$ was taken from $A$, phase 1 decreased $c(z)$ for the edge $(x, z)$. After all of them, together with the decrement of line L6 if $z = v$, $c(z) = 0$ and $z$ entered $A$. $\square$

**Lemma 3 (increase: phase 2).** After line L9, $d = \mathrm{dist}'$.

*Proof.* Outside $A$ the distances do not change by Lemma 2. For $x \in A$, a shortest new path to $x$ has a last vertex $y \notin A$ (possibly $s$, which is never in $A$), after which it stays in $A$. So $\mathrm{dist}'(x)$ is the least length of a walk that starts at some $y \notin A$ with value $\mathrm{dist}'(y) = d(y)$ and stays in $A$ after it. Line L8 gives each $x \in A$ the best one-edge start, and line L9 is Dijkstra's algorithm inside $A$, so by Fact 2 it computes exactly this least length; if no such walk exists, $x$ keeps $\infty$, which is right. $\square$

**Lemma 4 (increase: counts).** After line L10, (C) holds.

*Proof.* Tightness of an edge $(x, z)$ changes only if $(x, z) = (u, v)$, or $x \in A$, or $z \in A$. Vertices of $A$ are recounted from all their in-edges. For $z \notin A$: the change of $(u, v)$ was handled by line L6 if $z = v$. For an edge $(x, z)$ with $x \in A$, phase 1 removed its old tightness from $c(z)$ when $x$ was taken from $A$, and line L10 adds one if it is tight for the new values. If the edge was not tight before, phase 1 did not touch it, and line L10 adds its new tightness. If line L6 returns early, no distance changes, since $v$ keeps a tight in-edge from a vertex whose distance does not change (by the argument of Lemma 2 with $A$ empty), and only the edge $(u, v)$ changed its tightness, which line L6 recorded. $\square$

**Theorem.** After every update, (D) and (C) hold, so QUERY returns $\mathrm{dist}(v)$.

*Proof.* Every update is a decrease (an insertion, or a smaller weight) or an increase (a deletion, or a larger weight). An increase of a non-tight edge changes no distance by Fact 1, since $d$ still satisfies the Bellman conditions, and changes no count, since a non-tight edge stays non-tight. The other cases are Lemmas 1 to 4. By induction on the updates, (D) and (C) hold after each of them. $\blacksquare$
