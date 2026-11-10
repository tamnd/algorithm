---
title: Coloring SCC outputs the strongly connected components and removes at least one per iteration
proves: [correctness, termination, complexity]
status: full
---

**Setting.** $G = (V_0, A)$ is a directed graph with $n$ vertices and $m$ arcs, and $\lambda$ gives distinct labels. $V$ is the set of remaining vertices at the start of an iteration. "$u$ reaches $v$ in $X$" means there is a directed path from $u$ to $v$ with all its vertices in $X$; every vertex reaches itself. For $v \in V$, let $\mu(v) = \max \{\lambda(u) : u \text{ reaches } v \text{ in } V\}$.

**Lemma 1 (paths inside an SCC).** If $u$ and $v$ are in the same SCC $C$ of $G$, every vertex on every path from $u$ to $v$ is in $C$.

*Proof.* A vertex $x$ on the path is reached from $u$ and reaches $v$, which reaches $u$. $\square$

**Lemma 2 (closed sets).** If $V$ is a union of SCCs of $G$, then $u, v \in V$ are in the same SCC of $G$ exactly when each reaches the other in $V$.

*Proof.* If they are in the same SCC $C \subseteq V$, the paths between them stay in $C$ by Lemma 1. The converse is clear. $\square$

**Lemma 3 (propagation).** When the loop of lines L3 and L4 stops, $color(v) = \mu(v)$ for every $v \in V$, and it stops after at most $|V|$ rounds.

*Proof.* Colors only grow, and each color is a label of a vertex that reaches $v$ in $V$: this holds at the start, and a new color of $v$ comes from an in-neighbour $u \in V$ whose color is the label of a vertex reaching $u$, hence reaching $v$. So $color(v) \le \mu(v)$ throughout. Now let $u$ reach $v$ in $V$ with $\lambda(u) = \mu(v)$, along a shortest path $u = x_0, x_1, \ldots, x_k = v$ in $V$. Count the initial colors as round 0, in which every vertex is in the frontier. By induction on $i$, after round $i$, $color(x_i) \ge \lambda(u)$. For $i = 0$ this holds because $color(u) = \lambda(u)$. For $i \ge 1$, let $j \le i - 1$ be the first round after which $color(x_{i-1}) \ge \lambda(u)$. Its color changed in round $j$ (or $j = 0$), so $x_{i-1}$ is in the frontier of round $j + 1 \le i$ and sends a color of at least $\lambda(u)$ along the arc to $x_i$; colors never decrease, so $color(x_i) \ge \lambda(u)$ after round $i$. So $color(v) \ge \mu(v)$ after $k < |V|$ rounds. When no color changes in a round, no later round changes any, so the loop stops by round $|V|$ with $color = \mu$. $\square$

**Lemma 4 (one root's SCC).** Let $V$ be a union of SCCs of $G$, and let $r$ be a root, $\mu(r) = \lambda(r)$. Then $S(r)$, the set of vertices of color $\lambda(r)$ that reach $r$ inside that color class, is the SCC $C$ of $r$.

*Proof.* Let $v \in C$. By Lemma 2, $u$ reaches $v$ in $V$ exactly when $u$ reaches $r$ in $V$, so $\mu(v) = \mu(r) = \lambda(r)$. A path from $v$ to $r$ stays in $C$ by Lemma 1, so all its vertices have color $\lambda(r)$, and $v \in S(r)$. Conversely, let $v \in S(r)$. Then $\mu(v) = \lambda(r)$, and the labels are distinct, so the vertex with this label, $r$, reaches $v$ in $V$. And $v$ reaches $r$. By Lemma 2, $v \in C$. $\square$

**Theorem 1 (correctness and termination).** COLORING-SCC outputs every SCC of $G$ exactly once, and stops after at most $n$ iterations.

*Proof.* Invariant: at the start of each iteration, $V$ is a union of SCCs of $G$, and the sets output so far are exactly the SCCs of $G$ outside $V$. It holds at the start with $V = V_0$. In an iteration, by Lemma 3 the colors equal $\mu$, and by Lemma 4 every set output in line L7 is an SCC of $G$ inside $V$. Two roots have different colors, since $color(r) = \lambda(r)$ and labels are distinct, so the sets $S(r)$ are disjoint and no SCC is output twice. Line L8 removes whole SCCs, so the invariant holds after the iteration.

The vertex $z$ with the largest label in $V$ has $\mu(z) = \lambda(z)$, so it is a root, and at least one SCC leaves per iteration. So there are at most $n$ iterations, and when $V$ is empty, every SCC has been output once. $\blacksquare$

**Theorem 2 (cost).** Let $r$ be the total number of rounds, counting the propagation rounds and, in each iteration, the rounds of the longest backward search. Then $W = O((n + m) r)$ and $S = O(r \log n)$, and $r \le n(n + 1)$.

*Proof.* A propagation round reads the out-arcs of the vertices that changed, at most $O(n + m)$, and applies the maximum writes and the pack of the next frontier in $O(\log n)$ span. The backward searches of one iteration run in disjoint color classes (the roots have different colors), so one round of all of them together reads each arc at most once: $O(n + m)$ work and $O(\log n)$ span per round. By Lemma 3 an iteration has at most $|V| \le n$ propagation rounds, a backward search has at most $n$ rounds, and by Theorem 1 there are at most $n$ iterations, so $r \le n \cdot n + n$. $\blacksquare$
