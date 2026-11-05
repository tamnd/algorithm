---
title: The FIFO push-relabel algorithm returns a maximum flow in O(n^3 + nm) time
proves: [correctness, termination, complexity]
status: full
---

**Setting.** $G = (V, E)$ is a directed graph with $n \ge 2$ vertices, $m$ edges, real capacities $c(e) \ge 0$, a source $s$ and a sink $t \ne s$. Self-loops are removed. The residual graph $G_f$ has, for each edge $e = (u, w)$, a forward edge $(u, w)$ of capacity $c(e) - f(e)$ and a backward edge $(w, u)$ of capacity $f(e)$, and contains the edges of positive residual capacity. A labeling $h$ is *valid* for $f$ if $h(s) = n$, $h(t) = 0$, and $h(u) \le h(w) + 1$ for each edge $(u, w)$ of $G_f$. A residual edge $(u, w)$ is admissible if $h(u) = h(w) + 1$. A vertex $v \notin \{s, t\}$ is active if $e(v) > 0$.

**Lemma 1 (invariants).** At all times, $f$ is a preflow and $h$ is valid for $f$. Heights never decrease, and $h(s) = n$, $h(t) = 0$ throughout.

*Proof.* After lines L1 and L2, every edge out of $s$ is full, so $G_f$ has no edge out of $s$ except backward edges of edges into $s$, which carry no flow and so are absent. All other residual edges join vertices of height 0, or go into $s$ from height 0. So $h$ is valid, and $e(v) \ge 0$ for $v \ne s$.

*Push* along an admissible $r = (u, w)$ by $\delta = \min(e(u), c_f(r))$ keeps $0 \le f \le c$ and $e(u) \ge 0$, and raises $e(w)$. It may add the residual edge $(w, u)$, for which $h(w) = h(u) - 1 \le h(u) + 1$; it may remove $(u, w)$, which keeps validity.

*Relabel* of $u$ happens at line L8 only when the current edge has passed the end of the list. Claim: then $u$ has no admissible edge. Each edge was passed over at line L10 only when it was not admissible, and an edge $(u, w)$ can become admissible only if $h(u)$ rises (only a relabel of $u$ does that, which resets the pointer) or if $(u, w)$ newly enters $G_f$ or $h(w)$ falls. Heights never fall; $(u, w)$ enters $G_f$ only by a push along $(w, u)$, which needs $h(w) = h(u) + 1$, after which $(u, w)$ is not admissible. So no admissible edge out of $u$ exists. By validity, $h(u) \le h(w) + 1$ for every residual $(u, w)$, and since none is admissible, $h(u) \le h(w)$. Lemma 3 below shows that the set of residual edges out of $u$ is not empty. So the new value $1 + \min h(w)$ is larger than $h(u)$, and it keeps $h(u) \le h(w) + 1$ for edges out of $u$. Edges into $u$, $(x, u)$, stay valid because $h(u)$ only grew. The vertices $s$ and $t$ are never active, so they are never relabeled. $\square$

**Lemma 2 (no augmenting path).** For a valid labeling, $G_f$ has no $s$-$t$ path.

*Proof.* A simple path has at most $n - 1$ edges, each lowers $h$ by at most 1, and $h(s) - h(t) = n$. $\square$

**Lemma 3 (active vertices reach the source).** If $e(v) > 0$ for $v \ne s$, then $G_f$ has a path from $v$ to $s$.

*Proof.* Let $U$ be the set of vertices that $v$ reaches in $G_f$, and suppose $s \notin U$. No residual edge leaves $U$, so edges from $U$ to $V \setminus U$ are full and edges from $V \setminus U$ to $U$ are empty. Summing excesses over $U$, the edges inside $U$ cancel, and $\sum_{x \in U} e(x) = f(V \setminus U, U) - f(U, V \setminus U) \le 0$. Every term is at least 0 since $s \notin U$, and $e(v) > 0$, a contradiction. $\square$

**Lemma 4 (height bound).** Always $h(v) \le 2n - 1$ for every $v$.

*Proof.* Heights change only by relabels of active vertices. When $u$ is relabeled it is active, so by Lemma 3 a simple residual path from $u$ to $s$ of at most $n - 1$ edges exists. Validity after the relabel gives $h(u) \le h(s) + n - 1 = 2n - 1$. $\square$

**Lemma 5 (operation counts).**
(a) There are at most $(2n - 1)(n - 2) < 2n^2$ relabels, and each raises one height by at least 1.
(b) There are at most $2nm$ saturating pushes.
(c) With the FIFO queue there are at most $4n^2$ passes, and at most $4n^3$ nonsaturating pushes.

*Proof.* (a) Only the $n - 2$ inner vertices are relabeled, each starts at 0 and ends at most $2n - 1$ by Lemma 4.

(b) Fix an edge $e$ of $G$ with ends $u$, $w$, and consider the saturating pushes from $u$ to $w$ along a residual edge of $e$. At such a push $h(u) = h(w) + 1$. Before the next one from $u$ to $w$, some push from $w$ to $u$ must restore residual capacity, which needs $h(w) = h(u) + 1$ at that time; since heights never fall, $h(w)$ has grown by at least 2 between the two pushes from $u$ to $w$. At each such push $h(w) = h(u) - 1 \le 2n - 2$. So there are at most $n$ saturating pushes from $u$ to $w$, and at most $n$ from $w$ to $u$, for each edge of $G$: at most $2nm$ in total.

(c) Pass 1 discharges the vertices in $Q$ after line L3, and pass $i + 1$ discharges the vertices enqueued during pass $i$. A vertex is in $Q$ at most once at a time, so each pass discharges each vertex at most once. A discharge ends when $e(u) = 0$, and only its last push can be nonsaturating; so each pass has at most $n$ nonsaturating pushes. Let $\Phi$ be the largest height of an active vertex, or 0 if there is none; $\Phi = 0$ at the start. If a pass has no relabel, every vertex active at its start loses all excess to vertices one level lower, and heights do not change, so $\Phi$ falls by at least 1 over the pass. If a pass has relabels, $\Phi$ grows by at most the total height increase of that pass. By (a) the total height increase over the run is less than $2n^2$. Hence there are fewer than $2n^2$ passes with a relabel and at most $2n^2$ passes without one, at most $4n^2$ in all, and at most $4n^3$ nonsaturating pushes. $\square$

**Lemma 6 (running time).** The FIFO algorithm runs in $O(n^3 + nm)$ time.

*Proof.* A push is $O(1)$, so pushes cost $O(nm + n^3)$ by Lemma 5. A relabel of $u$ scans its list in $O(\deg u)$; with at most $2n$ relabels per vertex this is $O(n \sum_u \deg u) = O(nm)$. Between two relabels of $u$ the current pointer advances at most $\deg u$ times, which is $O(nm)$ in total. $\square$

**Theorem.** The algorithm stops, and returns a maximum flow $f$ and a minimum cut $S$.

*Proof.* By Lemma 5 the number of operations is finite, so the loop stops; then $Q$ is empty. Every vertex that becomes active is enqueued at that moment (line L9), and a dequeued vertex is discharged until its excess is 0; so when $Q$ is empty no vertex is active, and $f$ is a flow by conservation at every inner vertex. By Lemmas 1 and 2, $G_f$ has no $s$-$t$ path, so $f$ is maximum by the max-flow min-cut theorem, and the set $S$ of vertices that $s$ reaches in $G_f$ satisfies $t \notin S$ and $c(S) = |f|$, so it is a minimum cut. $\blacksquare$
