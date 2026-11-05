---
title: TZ-QUERY returns an estimate with stretch at most 2k-1, and infinity exactly for disconnected pairs
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be undirected with weights $w : E \to \mathbb{R}_{\ge 0}$, and let $d$ be its distance function, with $d(u, v) = +\infty$ when $u$ and $v$ are in different components. Then $d(u, v) = d(v, u)$ and $d(u, x) \le d(u, y) + d(y, x)$ for all $u, x, y$. Let $V = A_0 \supseteq A_1 \supseteq \cdots \supseteq A_{k-1} \supseteq A_k = \emptyset$ be any nested sets; the proof does not use how they are sampled. Write $d(A, v) = \min_{a \in A} d(a, v)$, with $\min \emptyset = +\infty$.

**Fact 1 (pivots).** The Dijkstra run of line L3 from all of $A_i$ at once is Dijkstra on $G$ plus a new source joined to each vertex of $A_i$ by an edge of weight 0, so it gives $d(A_i, v)$, and $p_i(v)$ is a vertex of $A_i$ with $d(p_i(v), v) = d(A_i, v)$ whenever this is finite. Also $p_0(v) = v$ and $d(A_0, v) = 0$.

## Preprocessing

Fix $i$ and $w \in A_i \setminus A_{i+1}$, and let $b(x) = d(A_{i+1}, x)$ and $C(w) = \{x : d(w, x) < b(x)\}$.

**Lemma 2 (clusters are closed under shortest paths).** If $x \in C(w)$ and $y$ is on a shortest path from $w$ to $x$, then $y \in C(w)$.

*Proof.* $d(w, x) < b(x) < \infty$, so the path exists, and $d(w, y) + d(y, x) = d(w, x)$. Also $b(x) \le b(y) + d(y, x)$, by the triangle inequality for the nearest vertex of $A_{i+1}$ to $y$. So $d(w, y) = d(w, x) - d(y, x) < b(x) - d(y, x) \le b(y)$. $\square$

**Lemma 3 (line L6 settles exactly $C(w)$, with exact distances).** The search of line L6 settles $x$ with key $D$ if and only if $x \in C(w)$, and then $D = d(w, x)$.

*Proof.* Every key pushed is the weight of a walk from $w$, so every key of $x$ is at least $d(w, x)$. A key $D$ of $x$ is pushed only if $D < b(x)$, so a settled $x$ has $d(w, x) \le D < b(x)$, and $x \in C(w)$.

Conversely, let $x \in C(w)$ and let $w = y_0, y_1, \ldots, y_r = x$ be a shortest path; by Lemma 2 every $y_j \in C(w)$, so $d(w, y_j) < b(y_j)$. The search is Dijkstra on $G$ in which some pushes are not done, and every push not done has a key $D \ge b(y) > d(w, y)$ for its vertex $y$. We show by induction on $j$ that $y_j$ is settled with key $d(w, y_j)$. For $j = 0$: $d(w, w) = 0 < b(w)$, so the search starts with $w$ at key 0, which is the least possible key, and settles it with key 0. For $j \ge 1$: by induction $y_{j-1}$ is settled with key $d(w, y_{j-1})$, and it then relaxes the edge to $y_j$ with the key $D_j = d(w, y_{j-1}) + w(y_{j-1}, y_j) = d(w, y_j) < b(y_j)$. If $y_j$ was settled before $y_{j-1}$, its key is at most $d(w, y_{j-1}) \le D_j$, as keys are extracted in nondecreasing order. Otherwise the entry $D_j$ is pushed, or an entry of $y_j$ with a key at most $D_j$ is already in the heap, so $y_j$ is settled later with a key at most $D_j$, as its first extracted entry has the least key among its entries in the heap. In both cases its key is at most $d(w, y_j)$, and at least $d(w, y_j)$ by the first paragraph. $\square$

**Corollary 4.** After line L7, for every $v$, $B(v)$ holds exactly the vertices $w$ with $v \in C(w)$, for the $i$ with $w \in A_i \setminus A_{i+1}$, each with the value $d(w, v)$.

Each search ends, since it settles each vertex at most once and pushes at most once per edge scan; so preprocessing terminates.

## Queries

Fix a query $(u_0, v_0)$ and let $\delta = d(u_0, v_0)$. The pair $\{u, v\}$ is always $\{u_0, v_0\}$, so $d(u, v) = \delta$ at all times.

**Lemma 5 (a value returned is a walk).** If line L15 returns a value, it is $d(u, w) + d(w, v) \ge \delta$.

*Proof.* Line L15 runs with $w = p_i(u)$, where $p_0(u) = u$, so $d(A_i, u) = d(w, u) = d(u, w)$ by Fact 1. By Corollary 4, $B(v)[w] = d(w, v)$. The sum is at least $d(u, v) = \delta$ by the triangle inequality. $\square$

**Lemma 6 (the key step).** If $w \in A_i$ and $w$ is not a key of $B(v)$, then $d(A_{i+1}, v) \le d(w, v)$.

*Proof.* If $w \in A_{i+1}$ this is the definition of $d(A_{i+1}, v)$. Otherwise $w \in A_i \setminus A_{i+1}$, and by Corollary 4, $v \notin C(w)$, that is, $d(w, v) \ge d(A_{i+1}, v)$. $\square$

**Lemma 7 (invariant).** Each time line L10 tests $w$, $w = p_i(u)$, $w \in A_i$, and $d(w, u) \le i \delta$.

*Proof.* At the first test, $w = u = p_0(u)$ and $d(w, u) = 0$. Suppose the invariant holds at a test that fails, with values $u, v, w, i$. By Lemma 6 and the triangle inequality,

$$d(A_{i+1}, v) \le d(w, v) \le d(w, u) + d(u, v) \le i\delta + \delta = (i + 1)\delta.$$

Lines L11 and L12 set $i' = i + 1$, $u' = v$ and $v' = u$. If line L13 does not return, line L14 sets $w' = p_{i'}(u') = p_{i+1}(v) \in A_{i+1}$, and by Fact 1, $d(w', u') = d(A_{i+1}, v) \le (i + 1)\delta = i' \delta$. $\square$

**Theorem.** TZ-QUERY terminates. If $\delta < \infty$ it returns $\hat d$ with $\delta \le \hat d \le (2k - 1)\delta$; if $\delta = \infty$ it returns $\infty$. If $A_1 = \emptyset$, in particular if $k = 1$, it returns $\delta$.

*Proof.* Termination: each iteration of the loop increases $i$, and line L13 returns when $i = k$, so there are at most $k$ iterations.

Case $\delta < \infty$. Let $K$ be the component of $u_0$ and $v_0$, and let $j$ be the largest index with $A_j \cap K \ne \emptyset$; $j \ge 0$ as $A_0 = V$, and $j \le k - 1$ as $A_k = \emptyset$. Suppose the test of line L10 fails at level $i$. In the proof of Lemma 7, $d(A_{i+1}, v) \le (i + 1)\delta < \infty$ with $v \in K$, so $A_{i+1}$ meets $K$, and $i + 1 \le j \le k - 1$. Hence line L13 sees $i + 1 < k$ and $d(A_{i+1}, v) < \infty$, so $p_{i+1}(v)$ is defined and line L13 does not return. So the loop ends only at line L15, with $i \le j$. By Lemmas 5 and 7, the value is

$$\hat d = d(u, w) + d(w, v) \le d(u, w) + d(w, u) + d(u, v) \le 2i\delta + \delta = (2i + 1)\delta \le (2k - 1)\delta,$$

and $\hat d \ge \delta$. If $A_1 = \emptyset$, then $j = 0$, so $i = 0$ and $\hat d = \delta$.

Case $\delta = \infty$. If line L15 returned a value, by Lemma 5 it would be $d(u, w) + d(w, v)$ with $w$ a key of $B(v)$, so $d(w, v) < \infty$, and $w = p_i(u)$ with $p_i(u)$ defined, so $d(w, u) < \infty$; then $u$ and $v$ would be connected through $w$. So the loop ends at line L13, which returns $\infty$. $\blacksquare$
