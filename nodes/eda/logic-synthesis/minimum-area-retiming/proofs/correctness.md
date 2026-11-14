---
title: The flow dual gives a legal retiming with the fewest registers
proves: [correctness]
status: full
---

We use the notation of the page. $S$ is the set of constraints $(u, v, b)$, each meaning $r(u) - r(v) \le b$, built by lines L1, L4 and L6. The vertex set $X$ is $V$ plus the mirror vertices. $B$ is the set of objective edges with their breadths $\beta(e) > 0$ after the scaling of line L5, and $a(x)$ is the coefficient of line L7. Write $\lambda$ for the scale factor of line L5, with $\lambda = 1$ for the per-edge count.

**Lemma 1 (the feasible set).** A map $r : V \to \mathbb{Z}$ with $r(h) = 0$ is a legal retiming with $c(G_r) \le c$ exactly when it extends to $X$ so that all constraints of $S$ hold. Without a period bound, drop "$c(G_r) \le c$".

*Proof.* The constraints of lines L1 and L6 are those of Theorem 1 on the retiming correctness page, so on $V$ they hold exactly for the legal retimings with $c(G_r) \le c$. A constraint of line L4 has the form $r(v_i) - r(m_u) \le w_{\max}(u) - w(e_i)$, a lower bound on $r(m_u)$. Each mirror vertex appears only in these lower bounds, so a large enough integer $r(m_u)$ meets them, and they never exclude a value of $r$ on $V$. $\square$

**Lemma 2 (the objective).** For every $r$ on $X$ that meets $S$, $\sum_{e \in B} \beta(e)\, w_r(e) = \lambda N(r) + (\text{terms that are} \ge 0)$, with equality on the per-edge model, and on the shared model when each $r(m_u)$ is the least value that meets line L4. Here $N$ is the count of the chosen model.

*Proof.* For the per-edge count, $B = E$ with $\beta = 1$, and the sum is $N(r)$. For the shared count, let $u$ have $k \ge 2$ fanout edges $e_i = (u, v_i)$ and let $g_i = (v_i, m_u)$ with $w(g_i) = w_{\max}(u) - w(e_i)$. By Lemma 1 of the retiming proof, the path $e_i g_i$ has $w_r(e_i) + w_r(g_i) = w(e_i) + w(g_i) + r(m_u) - r(u) = w_{\max}(u) + r(m_u) - r(u)$, the same value $T_u$ for every $i$. With breadth $\lambda / k$ on each of the $2k$ edges, these terms add up to $\lambda T_u$. Since $w_r(g_i) \ge 0$ by line L4, $T_u \ge w_r(e_i)$ for every $i$, so $T_u \ge \max_i w_r(e_i)$. The least $r(m_u)$ that meets line L4 makes some $w_r(g_i) = 0$, so it gives $T_u = \max_i w_r(e_i)$. A gate with one fanout edge $e$ keeps $\beta(e) = \lambda$ and contributes $\lambda w_r(e)$. Summing over $u$ gives the claim, with $\lambda N_s(r)$ as the main term. $\square$

So by Lemmas 1 and 2, the problem is the linear program
$$(P)\quad \min \sum_{x \in X} a(x)\, r(x) \quad \text{subject to} \quad r(u) - r(v) \le b \text{ for } (u, v, b) \in S,\ r \in \mathbb{Z}^X,$$
since $\sum_{e \in B} \beta(e) w_r(e) = \sum_{e \in B} \beta(e) w(e) + \sum_x a(x) r(x)$ by the same telescoping as on the page, and a minimizer may take each $r(m_u)$ at its least value without loss.

**Lemma 3 (bounded).** If $S$ is feasible, $(P)$ and its relaxation over $\mathbb{R}^X$ are bounded below.

*Proof.* On the feasible set, every $w_r(e)$ with $e \in B$ is at least 0, by line L1 for the edges of $G$ and by line L4 for the mirror edges. So the objective is at least $-\sum_{e \in B} \beta(e) w(e)$. $\square$

**Lemma 4 (duality).** The dual of the relaxation of $(P)$ is
$$(F)\quad \min \sum_{(u,v,b) \in S} b\, f_{uvb} \quad \text{subject to} \quad \mathrm{in}_f(x) - \mathrm{out}_f(x) = a(x) \text{ for all } x,\ f \ge 0,$$
the min-cost flow problem of lines L8 and L9, where the constraint $(u, v, b)$ is an arc $u \to v$. A pair of feasible solutions $r$ and $f$ is optimal exactly when $f > 0$ only on arcs with $r(u) - r(v) = b$.

*Proof.* Write the constraints as $A r \le b$, where the row of $(u, v, b)$ has $+1$ at $u$ and $-1$ at $v$. The dual of $\min a^T r$ subject to $A r \le b$ with $r$ free is $\max b^T y$ subject to $A^T y = a$ and $y \le 0$. Put $f = -y \ge 0$. Then $(A^T f)_x$ is the flow out of $x$ minus the flow into $x$, so $A^T y = a$ reads $\mathrm{in}_f(x) - \mathrm{out}_f(x) = a(x)$, and the objective is $-\min b^T f$. The last claim is complementary slackness, from the [complementary slackness](/complementary-slackness/) page. $\square$

**Lemma 5 (the cases of line L10).** If the constraint graph has a negative cycle, $(P)$ is infeasible. Otherwise $(F)$ has an optimal solution.

*Proof.* A negative cycle of arcs $u \to v$ of cost $b$ gives a sum of constraints whose left sides cancel and whose right side is negative, so $S$ has no solution, by the theorem on the [difference constraints](/difference-constraints/) page. If there is no negative cycle, $S$ is feasible by the same theorem, $(P)$ is bounded by Lemma 3, so the relaxation has an optimum, and by [LP duality](/lp-duality/) $(F)$ is feasible and has an optimum of the same value. $\square$

So line L10 returns "infeasible" exactly when no legal retiming meets the bound: when there is no negative cycle, successive shortest paths finds a flow, by the next lemma, and it cannot report a missing flow.

**Lemma 6 (successive shortest paths).** If the arcs have no negative cycle and $(F)$ is feasible, line L9 returns an optimal flow $f$, and the residual graph of $f$ has no negative cycle.

*Proof.* Add a super source joined to each $x$ with $a(x) < 0$ by an arc of capacity $-a(x)$ and cost 0, and a super sink reached from each $x$ with $a(x) > 0$ by an arc of capacity $a(x)$. Give each real arc the capacity $U + 1$, where $U = \sum_x \max(a(x), 0)$. A flow of value $U$ that meets the demands never puts more than $U$ on an arc in an optimal solution with no flow cycles, and $(F)$ has such an optimal solution because removing a cycle of flow does not raise the cost when there is no negative cycle. So the capacity does not change the optimum. By the theorem on the [successive shortest path](/successive-shortest-path/) page, the method keeps a flow whose residual graph has no negative cycle, and after $U$ units it has a flow of value $U$ of least cost. Its restriction to the real arcs is optimal for $(F)$. $\square$

**Lemma 7 (potentials).** Let $\pi$ be the shortest distances of line L11, in the residual graph of $f$ restricted to $X$, from a virtual source with a 0 arc to every vertex. Then $r = \pi(h) - \pi$ satisfies $S$ and is tight on every arc with $f > 0$.

*Proof.* The residual graph has no negative cycle by Lemma 6, so the distances exist, and they are integers because all costs are integers. Every real arc $u \to v$ of cost $b$ stays in the residual graph, since its flow is at most $U$ and its capacity is $U + 1$. So $\pi(v) \le \pi(u) + b$, that is $r(u) - r(v) = \pi(v) - \pi(u) \le b$, and $S$ holds. If $f > 0$ on the arc, the reverse arc $v \to u$ of cost $-b$ is in the residual graph, so $\pi(u) \le \pi(v) - b$. Together, $\pi(v) - \pi(u) = b$, and the constraint is tight. Adding the constant $\pi(h)$ keeps all differences. $\square$

**Theorem.** If some legal retiming meets the period bound, MIN-AREA-RETIMING returns an integer legal retiming $r$ with $r(h) = 0$ and $c(G_r) \le c$ whose register count is the least over all such retimings, in the chosen model. Otherwise it returns "infeasible".

*Proof.* The second claim is Lemma 5 with Lemma 1. For the first, $f$ is feasible for $(F)$ by Lemma 6, and $r$ is feasible for the relaxation of $(P)$ and tight wherever $f > 0$ by Lemma 7. By Lemma 4, $r$ is optimal for the relaxation, and it is an integer vector, so it is optimal for $(P)$. The integrality also follows from the fact that $A$ is the transpose of a network matrix and so [totally unimodular](/total-unimodularity/). Lowering each $r(m_u)$ to its least value keeps $S$ and does not raise the objective, since $a(m_u) = \sum_i \beta(g_i) > 0$ counts only edges into $m_u$, so $r$ already has these least values at an optimum or another optimum has them with the same values on $V$. By Lemmas 1 and 2, the restriction of $r$ to $V$ is a legal retiming that meets the bound and minimizes $\lambda N$, hence $N$. $\blacksquare$
