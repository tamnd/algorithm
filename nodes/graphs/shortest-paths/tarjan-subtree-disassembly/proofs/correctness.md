---
title: Subtree disassembly returns the distances or a reachable negative cycle
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ have $n$ vertices, real weights $w$ and source $s$. Line numbers refer to SUBTREE-DISASSEMBLY on the main page. A *label change* is one execution of line L9. A vertex is *active* if it is in the tree $T$, and *inactive* if it has a finite label but is not in $T$.

**Invariant 1 (structure).** At the test of line L2: (a) $T$ is a tree rooted at $s$ whose arcs are arcs of $G$, given by $\pi$; (b) every tree arc is tight, $d(x) = d(\pi(x)) + w(\pi(x), x)$; (c) $d(s) = 0$ and $s$ is in $T$; (d) every vertex in $Q$ is in $T$.

*Proof.* At the start $T = \{s\}$ and all four parts hold. Consider a label change of $v$ through the arc $(u, v)$ during the scan of $u$. The scan runs only for $u \in T$, and $u$ stays in $T$ during its own scan: it could leave $T$ only at line L8 as a proper descendant of some $v$, but then line L6 would have returned. Line L6 has failed, so $v \ne u$ and $v$ is not an ancestor of $u$. Line L8 removes the proper descendants of $v$ from $T$ and from $Q$; the rest of $T$ is still a tree, and all its arcs are unchanged and tight. Line L9 then lowers $d(v)$ and makes $v$ a child of $u$. The vertex $u$ is not in the subtree of $v$, so no cycle is created and $T$ stays a tree. The only arcs with head or tail $v$ in $T$ are now $(u, v)$, which is tight by line L9, since $v$ has no children after line L8. So (a) and (b) hold. For (c): $v = s$ would need $s$ to be an ancestor-or-equal of $u$, which is always the case, so line L6 returns before $d(s)$ changes. Part (d) holds because line L8 removes from $Q$ every vertex it removes from $T$, and line L10 adds $v$, which is in $T$. $\square$

**Fact 2 (labels are path weights).** At all times, every finite label $d(x)$ is the weight of a simple path from $s$ to $x$.

*Proof.* For $x \in T$, by Invariant 1 (b) and (c), summing the tight arcs along the tree path gives $d(x) = w(\text{tree path from } s \text{ to } x)$, which is a simple path. An inactive vertex keeps the label it had when it was last in $T$, which was such a weight then. $\square$

**Lemma 3 (returned cycles).** If line L7 returns, the returned cycle is a negative cycle reachable from $s$.

*Proof.* If $v = u$, the cycle is the self-loop $(u, u)$ with $w(u, u) < d(u) - d(u) = 0$. Otherwise $v$ is a proper ancestor of $u$ in $T$, and the tree path $P$ from $v$ to $u$ has weight $d(u) - d(v)$ by tightness. With the arc $(u, v)$, it closes a cycle of distinct vertices (a tree path is simple) of weight $d(u) - d(v) + w(u, v) < 0$ by the test of line L5. Its vertices are in $T$, so they are reachable from $s$. $\square$

**Lemma 4 (termination).** The algorithm terminates.

*Proof.* By Fact 2 every finite label is the weight of one of the finitely many simple paths from $s$. Each label change makes a label strictly smaller, so each vertex has finitely many label changes, and line L10 adds finitely many entries to $Q$. Each iteration of line L2 removes one entry. $\square$

**Invariant 5 (violated arcs).** At the test of line L2, every arc $(x, y)$ with $d(x) < \infty$ and $d(x) + w(x, y) < d(y)$ has $x \in Q$ or $x$ inactive.

*Proof.* At the start only $d(s)$ is finite and $s \in Q$. When $x$ is scanned, each arc out of $x$ is relaxed and becomes non-violated; a later label change in the same scan lowers only the label of some head $v \ne x$ (the case $v = x$ returns), which cannot violate an arc out of $x$. When $d(v)$ goes down at line L9, the arcs out of $v$ may become violated, and line L10 puts $v$ in $Q$. A vertex removed at line L8 leaves $Q$ but becomes inactive. Lowering $d(y)$ never violates an arc into $y$. $\square$

**Lemma 6 (no inactive vertex at the end).** If the loop of line L2 ends because $Q$ is empty, no vertex is inactive.

*Proof.* For an inactive vertex $y$, look at the last time $\tau(y)$ it was removed at line L8, during the label change of some vertex $a$, and let $p(y)$ be its parent just before that removal, so that $p(y)$ is $a$ or a vertex removed at the same time, and the arc $(p(y), y)$ was tight with the labels just before time $\tau(y)$. Let $h(y)$ be the depth of $y$ below $a$ at that moment. Since $y$ is inactive, $d(y)$ has not changed since $\tau(y)$.

Suppose $Q$ is empty at the end and $I$, the set of inactive vertices, is not empty. Take $y \in I$ and $p = p(y)$. Two cases.

- $d(p)$ is now smaller than just before $\tau(y)$. This holds if $p = a$, whose label went down at time $\tau(y)$, or if $p \ne a$ had a label change after $\tau(y)$. Then $d(p) + w(p, y) < d(y)$, the arc is violated, and by Invariant 5 with $Q$ empty, $p \in I$. In this case the last removal of $p$ came after time $\tau(y)$: for $p = a$, $a$ was active right after $\tau(y)$; for $p \ne a$, $p$ was put back in $T$ by a label change after $\tau(y)$. So $\tau(p) > \tau(y)$.
- $d(p)$ is unchanged since just before $\tau(y)$. Then $p \ne a$, $p$ was removed at time $\tau(y)$ and has not been put back in $T$, so $p \in I$ with $\tau(p) = \tau(y)$ and $h(p) = h(y) - 1$.

In both cases $p(y) \in I$ and the pair $(\tau(p), -h(p))$ is lexicographically larger than $(\tau(y), -h(y))$. Starting from any $y \in I$ and applying $p$ again and again gives an infinite sequence in the finite set $I$ with strictly increasing pairs, which is impossible. $\square$

**Theorem.** The algorithm terminates. If it returns a cycle, that cycle is a negative cycle reachable from $s$. If it returns $d$ and $\pi$, then no negative cycle is reachable from $s$, $d(v) = \delta(s, v)$ for all $v$, with $\infty$ exactly for the unreachable vertices, and $\pi$ is a shortest-path tree. So it returns a cycle if and only if a negative cycle is reachable from $s$.

*Proof.* Termination is Lemma 4, and the claim on returned cycles is Lemma 3. Suppose it returns at line L11, with $Q$ empty. By Lemma 6 there is no inactive vertex, so by Invariant 5 no arc with a finite tail is violated. As in the proof for SPFA, a reachable vertex with label $\infty$ would give a violated arc on a path from $s$, so exactly the reachable vertices have finite labels. Summing the inequalities $d(c_i) \le d(c_{i-1}) + w(c_{i-1}, c_i)$ around any cycle through reachable vertices gives a nonnegative weight, so no negative cycle is reachable from $s$. By Invariant 1 (c) $d(s) = 0$, by Fact 2 each finite label is the weight of a path from $s$, and the triangle inequality holds on every arc with a reachable tail; Theorem B of the [optimality conditions](/shortest-path-optimality-conditions/) gives $d = \delta(s, \cdot)$. All reachable vertices are in $T$, which is a tree of tight arcs by Invariant 1, so each tree path has weight $d(v) = \delta(s, v)$, and $T$ is a shortest-path tree. Finally, if a negative cycle is reachable from $s$, the run cannot return at line L11, so it returns a cycle. $\blacksquare$
