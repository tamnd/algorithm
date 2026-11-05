---
title: The MPM algorithm computes a maximum flow in O(n^3) time
proves: [correctness, termination, complexity]
status: full
---

**Setting.** $G = (V, E)$ is a directed graph with capacities $c \ge 0$, real or integer, and $s \ne t$. Each edge $e$ has a residual pair; $G_f$ is the residual graph of a flow $f$, with edges of positive residual capacity only. $d_f(v)$ is the distance from $s$ to $v$ in $G_f$. The level graph $L_f$ has the edges $(u, v)$ of $G_f$ with $d_f(v) = d_f(u) + 1$. In a phase, $L$ is a subgraph of $L_f$ whose residual capacities shrink as the phase pushes flow, and from which vertices and edges are deleted.

In $L$, $\mathrm{in}(v)$ and $\mathrm{out}(v)$ count only the edges of $L$ whose other end is still in $L$. Residual capacities of the edges of $L_f$ only decrease during a phase, because the phase sends flow only along edges of $L_f$, from one level to the next, and never along their reverses, which are not in $L_f$.

**Invariant of a phase.** At the start of each step of line L4: (a) the flow is a feasible flow of $G$; (b) every vertex of $L$ other than $s$ has $\mathrm{in}(v) > 0$, and every vertex other than $t$ has $\mathrm{out}(v) > 0$. Line L3 makes (b) true by deleting dead ends, and (a) holds at the start of the phase.

**Lemma 1 (a step succeeds).** Let $v$ be chosen at line L5 with $d = p(v)$. The push of line L7 moves exactly $d$ units from $v$ to $t$ along edges of $L$, and the pull of line L8 moves exactly $d$ units from $s$ to $v$; the flow stays feasible, and its value grows by $d$.

*Proof.* Consider the push. Let $v$ be at level $i$. We show by induction on $j \ge i$ that, when layer $j$ is processed, the total excess on layer $j$ is $d$, and each vertex $u$ of layer $j$ has excess $x_u \le d$. For $j = i$ the only vertex with excess is $v$, with $d$. Assume it for $j$. Each $u$ on layer $j$ other than $t$ has $x_u \le d \le p(u) \le \mathrm{out}(u)$, so walking its leaving edges and sending $\min(x, \text{residual})$ along each sends all of $x_u$ to layer $j + 1$; edges of $L$ go only from layer $j$ to layer $j + 1$. So layer $j + 1$ receives exactly $d$ in total, and each vertex there has excess at most $d$. When the layer of $t$ is reached, $t$ is the only vertex of $L$ at that layer, since line L3 removed all others at levels $\ge d_f(t)$ without leaving edges, so all $d$ units are at $t$. Each push along $(u, w)$ adds to the flow on the edge or cancels flow on its pair, within the residual capacity, and every vertex other than $v$ and $t$ sends exactly what it receives. The pull is the same argument with entering edges and layers $i, i - 1, \ldots, 0$: all $d$ units are drawn from $s$, and every vertex other than $s$ and $v$ keeps conservation. Together, $v$ receives $d$ and sends $d$, and the net effect is a flow of value $d$ from $s$ to $t$ added to $f$. $\square$

**Lemma 2 (the invariant is kept).** After line L9, (a) and (b) still hold, and $v$ has been deleted.

*Proof.* (a) is Lemma 1. The push lowers $\mathrm{out}(v)$ by $d$ and the pull lowers $\mathrm{in}(v)$ by $d$, and $d = \min(\mathrm{in}(v), \mathrm{out}(v))$, so after the step one of them is 0 and $v$ is deleted. The cascade deletes vertices until no vertex other than $s$ has $\mathrm{in} = 0$ and none other than $t$ has $\mathrm{out} = 0$, which is (b). $\square$

**Lemma 3 (a phase ends with a blocking flow).** Each phase stops after at most $n$ steps, and then every $s$-$t$ path of $L_f$ has an edge whose residual capacity is 0: the flow of the phase is blocking.

*Proof.* Each step deletes the chosen vertex, so there are at most $n$ steps, and the phase stops when $s$ or $t$ has been deleted. Suppose some $s$-$t$ path $P$ of $L_f$ has positive residual capacity on all its edges at the end; then it had positive capacity on them at all times of the phase. Some vertex of $P$ was deleted, since $s$ or $t$ was. Let $u$ be the first vertex of $P$ to be deleted. At that moment, its neighbors on $P$ were in $L$, so the edges of $P$ at $u$ were counted: if $u \ne s$, $\mathrm{in}(u) > 0$, and if $u \ne t$, $\mathrm{out}(u) > 0$. But a vertex is deleted only when it is $s$ with $\mathrm{out}(s) = 0$, $t$ with $\mathrm{in}(t) = 0$, or another vertex with $\mathrm{in} = 0$ or $\mathrm{out} = 0$, including the chosen $v$ after Lemma 2. This is a contradiction. $\square$

**Lemma 4 (distances grow).** Let $f'$ be the flow after a phase that started with $f$. Then $d_{f'}(t) > d_f(t)$.

*Proof.* This is the lemma of [Dinic's algorithm](/dinic/) and the [level graph](/level-graph/). Every edge of $G_{f'}$ is an edge of $G_f$ or the reverse of an edge of $L_f$, so it goes up at most one level of $d_f$, or down one level. A path from $s$ to $t$ in $G_{f'}$ of length $d_f(t)$ would have to go up exactly one level on every edge, so it would consist of edges of $L_f$ only, none of them reversed; it would be a path of $L_f$ that is not blocked, which contradicts Lemma 3. $\square$

**Theorem.** MPM returns a maximum flow and a minimum cut, after at most $n - 1$ phases, in $O(n^3)$ time.

*Proof.* By Lemma 4, $d_f(t)$ grows in each phase and is at most $n - 1$ while $t$ is reachable, so there are at most $n - 1$ phases. When line L2 finds $t$ unreachable, the set $S$ of vertices that $s$ reaches in $G_f$ is an $s$-$t$ cut whose leaving edges are full and whose entering edges are empty, so $|f| = c(S)$, and by the [max-flow min-cut theorem](/max-flow-min-cut-theorem/) $f$ is maximum and $S$ is a minimum cut.

Time per phase. Building $L$ and line L3 take $O(n + m)$. There are at most $n$ steps, and a scan for the least potential costs $O(n)$. In a push or pull, the edge pointer of a vertex moves past an edge only when the edge is saturated or leads to a deleted vertex, at most $2m$ times per phase in all; besides those, each vertex makes at most one push that does not saturate its edge per step, at most $n$ per step and $n^2$ per phase. The cascade at line L9 deletes each vertex once per phase and looks at each edge at most twice. So a phase takes $O(n^2 + m) = O(n^2)$, and the run takes $O(n^3)$. $\blacksquare$
