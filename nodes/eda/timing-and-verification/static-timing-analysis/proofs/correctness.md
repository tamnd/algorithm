---
title: Static timing analysis computes the longest-path arrival times, the shortest-slack required times and the least path slack of every vertex in linear time
proves: [correctness, critical path, running time]
status: full
---

Let $G = (V, E)$ be a finite directed graph with a delay $d(e)$ in an ordered abelian group (integers, rationals or reals) on each edge. Parallel edges are allowed. A *start point* is a vertex with no in-edge and an *endpoint* is a vertex with no out-edge. Each start point $s$ has a value $AT_0(s)$ and each endpoint $t$ a value $RT_0(t)$. For a path $P$, $d(P)$ is the sum of the delays of its edges; a path with one vertex has $d(P) = 0$. Define
$$ A(v) = \max \{ AT_0(s) + d(P) : P \text{ a path from a start point } s \text{ to } v \}, $$
$$ R(v) = \min \{ RT_0(t) - d(P) : P \text{ a path from } v \text{ to an endpoint } t \}. $$

**Lemma 1 (the sets are finite and not empty).** If $G$ is acyclic, then every vertex is reached from some start point and reaches some endpoint, and there are finitely many paths. So $A(v)$ and $R(v)$ are well defined.

*Proof.* A path in an acyclic graph repeats no vertex, so it has at most $|V|$ vertices, and there are finitely many paths. From $v$, follow in-edges backward as long as possible. No vertex repeats, so the walk stops after fewer than $|V|$ steps, at a vertex with no in-edge. Reversed, the walk is a path from a start point to $v$. The same argument with out-edges gives a path from $v$ to an endpoint. $\square$

**Lemma 2 (line L1).** Line L1 succeeds if and only if $G$ is acyclic. If it succeeds, every edge $(u, v)$ has $u$ before $v$ in the order.

*Proof.* This is the correctness of [topological sorting](/topological-sort/): a topological order exists if and only if the graph has no directed cycle, and Kahn's algorithm outputs all vertices exactly when the graph is acyclic. $\square$

From now on $G$ is acyclic and the order of line L1 is fixed.

**Lemma 3 (forward pass).** When lines L2 to L4 finish, $AT(v) = A(v)$ for every vertex $v$.

*Proof.* By induction along the order. Let $v$ be the next vertex, and assume $AT(u) = A(u)$ for all vertices before $v$.

If $v$ has no in-edge, the only path that ends at $v$ and starts at a start point is the path with the single vertex $v$, since a longer path would enter $v$ by an edge. So $A(v) = AT_0(v)$, which line L3 assigns.

Otherwise, every path $P$ from a start point $s$ to $v$ has at least one edge, because $v$ is not a start point. Let $(u, v)$ be its last edge and $P'$ the rest, a path from $s$ to $u$. Then $AT_0(s) + d(P) = AT_0(s) + d(P') + d(u, v) \le A(u) + d(u, v)$. Conversely, for each in-edge $(u, v)$ and each path $P'$ from a start point to $u$, the path $P'$ followed by $(u, v)$ ends at $v$, since $G$ is acyclic and $v$ is not on $P'$ (otherwise $v$ would come before $u$ in the order). Hence
$$ A(v) = \max_{(u, v) \in E} \big( A(u) + d(u, v) \big). $$
All such $u$ come before $v$ by Lemma 2, so $AT(u) = A(u)$, and line L4 assigns exactly this value. $\square$

**Lemma 4 (backward pass).** When lines L5 to L7 finish, $RT(u) = R(u)$ for every vertex $u$.

*Proof.* The same induction along the reverse order. An endpoint has only the one-vertex path to an endpoint, so $R(t) = RT_0(t)$ (line L6). For any other $u$, splitting each path from $u$ at its first edge $(u, v)$ gives $R(u) = \min_{(u, v) \in E} (R(v) - d(u, v))$, and every such $v$ comes after $u$ in the order, so it was handled before $u$ in the reverse order. Line L7 assigns this value. $\square$

**Theorem 1 (slack).** For every vertex $v$,
$$ RT(v) - AT(v) = \min \{ RT_0(t) - AT_0(s) - d(P) : P \text{ a path from a start point } s \text{ to an endpoint } t \text{ through } v \}. $$
In particular $\min_v \mathrm{slack}(v)$ is the least slack of a start-to-end path.

*Proof.* A start-to-end path $P$ through $v$ splits at $v$ into a path $P_1$ from $s$ to $v$ and a path $P_2$ from $v$ to $t$, with $d(P) = d(P_1) + d(P_2)$. Conversely, any such $P_1$ and $P_2$ join into a path, because $G$ is acyclic: a vertex on both would close a cycle through $v$. So the set of start-to-end paths through $v$ is the set of pairs $(P_1, P_2)$, with no constraint between the two parts. Hence
$$ \min_{P \ni v} \big( RT_0(t) - d(P_2) - (AT_0(s) + d(P_1)) \big) = \min_{P_2} \big( RT_0(t) - d(P_2) \big) - \max_{P_1} \big( AT_0(s) + d(P_1) \big) = R(v) - A(v), $$
which is $RT(v) - AT(v)$ by Lemmas 3 and 4. Every start-to-end path passes through some vertex, so the least vertex slack is the least path slack. $\square$

**Theorem 2 (critical path).** Let $t$ be an endpoint of least slack. The backtrace from $t$ always finds an in-edge $(u, v)$ with $AT(u) + d(u, v) = AT(v)$ while $v$ is not a start point, and it ends at a start point $s$ after at most $|V| - 1$ steps. The path $P$ it returns has $\mathrm{slack}(P) = \min_w \mathrm{slack}(w)$, and every vertex of $P$ has this slack.

*Proof.* By Lemma 3 the maximum in line L4 is attained by some in-edge, so the step is always possible. Each step moves to a vertex earlier in the order, so the walk ends, at a vertex with no in-edge. Adding the equalities along the path gives $AT(t) = AT_0(s) + d(P)$, so $\mathrm{slack}(P) = RT_0(t) - AT(t) = \mathrm{slack}(t)$, since $RT(t) = RT_0(t)$. Let $m = \min_w \mathrm{slack}(w)$. By Theorem 1, $m$ is the least path slack, and some path ends at an endpoint whose slack is $m$, so $\mathrm{slack}(t) = m$. For a vertex $w$ of $P$, Theorem 1 gives $\mathrm{slack}(w) \le \mathrm{slack}(P) = m$, and $\mathrm{slack}(w) \ge m$ by the choice of $m$. $\square$

**Theorem 3 (early mode).** If line L4 takes the minimum, line L7 the maximum and line L8 computes $AT(v) - RT(v)$, then $AT(v)$ is the least value of $AT_0(s) + d(P)$, $RT(v)$ is the largest value of $RT_0(t) - d(P)$, and $AT(v) - RT(v)$ is the least value of $AT_0(s) + d(P) - RT_0(t)$ over start-to-end paths through $v$.

*Proof.* Apply Lemmas 3 and 4 and Theorem 1 to the delays $-d$, the start values $-AT_0$ and the end values $-RT_0$. Negation swaps max and min, and the slack of the negated problem is $(-RT(v)) - (-AT(v)) = AT(v) - RT(v)$. No step of the proofs used a sign condition on the delays. $\square$

**Theorem 4 (running time).** With in-lists and out-lists, the algorithm takes $\Theta(V + E)$ time and $\Theta(V)$ extra space, counting each addition and comparison of delays as one step.

*Proof.* Line L1 takes $\Theta(V + E)$ time with Kahn's algorithm. Lines L2 to L4 do $O(1)$ work per vertex plus $O(1)$ work per in-edge, and each edge is the in-edge of one vertex, so $\Theta(V + E)$. The same holds for lines L5 to L7 with out-edges, and line L8 is $\Theta(V)$. The arrays $AT$, $RT$, slack, the order and the in-degree counters of Kahn's algorithm take $\Theta(V)$ space. Every vertex and edge must be read, so no algorithm does better than $\Omega(V + E)$ in the worst case. $\blacksquare$
