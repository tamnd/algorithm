---
title: Under the independent cascade and linear threshold models the spread is monotone and submodular, so the greedy seeds reach at least 1 - 1/e of the optimum
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a directed graph with $n$ vertices. For a set $L \subseteq E$ of arcs and $S \subseteq V$, let $R_L(S)$ be the set of vertices reachable from $S$ using only arcs of $L$, with $S \subseteq R_L(S)$. The spread $\sigma(S)$ is the expected number of active vertices at the end of the process started from the seeds $S$.

**Termination.** Line L2 runs $\min(k, |V|)$ times and line L3 at most $|V|$ times per round, so GREEDY-IM makes at most $k|V| + 1$ calls to $\sigma$ and stops. Each round adds a vertex not in $S$, so $|S| = \min(k, |V|)$ at the end.

**Lemma 1 (live edges for the independent cascade).** Draw every arc $(u, v)$ live independently with probability $p_{uv}$, giving a random set $L$. Then for every $S$, the final active set of the cascade from $S$ has the same distribution as $R_L(S)$; so $\sigma(S) = \mathbb{E}[|R_L(S)|]$.

*Proof.* In the cascade, the coin of an arc $(u, v)$ is flipped at most once, when $u$ becomes active and $v$ is still inactive, and the coins are independent. Flip all the coins in advance instead and use each one when the cascade would flip it; this does not change the distribution of the run. With the coins fixed, a vertex is active at the end exactly when a path of live arcs leads to it from $S$: by induction on the step, every vertex activated at step $t$ is at live-arc distance $t$ from $S$, and every vertex at live-arc distance $t$ from $S$ is active by step $t$, since its predecessor on a shortest live path is active by step $t - 1$ and tries the live arc, unless the vertex was active already. Unused coins do not matter. $\square$

**Lemma 2 (live edges for the linear threshold model).** Let every vertex $v$ independently keep at most one of its in-arcs: the arc $(u, v)$ with probability $b_{uv}$, and none with probability $1 - \sum_u b_{uv}$. Let $L$ be the set of kept arcs. Then the final active set of the threshold process from $S$ has the same distribution as $R_L(S)$.

*Proof.* Let $A_0 = S$ and $A_t$ the active set after step $t$ in the threshold process, and let $A'_t$ be the set of vertices at $L$-distance at most $t$ from $S$ in the live-edge process. Both sequences increase and stop once two consecutive sets are equal. We show that $(A_t)$ and $(A'_t)$ have the same distribution, by showing that both are Markov chains on pairs $(A_{t-1}, A_t)$ with the same transitions.

*Threshold process.* Fix the history up to step $t$. A vertex $v \notin A_t$ is known only to have $\theta_v > \sum_{u \in A_{t-1}} b_{uv}$, and the thresholds are independent and uniform on $[0, 1]$; so, given the history, $\theta_v$ is uniform on $(\sum_{u \in A_{t-1}} b_{uv}, 1]$, independently for different $v$. Vertex $v$ joins at step $t + 1$ when $\theta_v \le \sum_{u \in A_t} b_{uv}$, with probability
$$\frac{\sum_{u \in A_t \setminus A_{t-1}} b_{uv}}{1 - \sum_{u \in A_{t-1}} b_{uv}}.$$

*Live-edge process.* Fix the history up to step $t$. A vertex $v \notin A'_t$ is known only to have kept no arc from $A_{t-1}'$, and the choices of different vertices are independent. Given that, its kept arc comes from $A'_t \setminus A'_{t-1}$ with the same probability as above, and $v$ joins at step $t + 1$ exactly in that case.

The two chains start at $(\emptyset, S)$, and each vertex outside the current set joins independently with the same probability. So they have the same distribution, and so do their final sets. $\square$

**Lemma 3 (coverage is monotone and submodular).** For a fixed $L$, the function $f_L(S) = |R_L(S)|$ is monotone and submodular.

*Proof.* $R_L(S) = \bigcup_{s \in S} R_L(\{s\})$, so $f_L$ counts the union of the sets $R_L(\{s\})$, which grows with $S$. For $S \subseteq T$ and $v \notin T$, $f_L(S \cup \{v\}) - f_L(S) = |R_L(\{v\}) \setminus R_L(S)| \ge |R_L(\{v\}) \setminus R_L(T)| = f_L(T \cup \{v\}) - f_L(T)$, because $R_L(S) \subseteq R_L(T)$. $\square$

**Lemma 4.** In both models, $\sigma$ is monotone and submodular, and $\sigma(\emptyset) = 0$.

*Proof.* By Lemma 1 or Lemma 2, $\sigma(S) = \sum_L \Pr[L]\, f_L(S)$, a sum over the finitely many arc sets with non-negative coefficients. Monotonicity and the submodular inequality are linear inequalities, so they carry over from each $f_L$ (Lemma 3) to the sum. $R_L(\emptyset) = \emptyset$. $\square$

**Theorem (Nemhauser, Wolsey and Fisher).** Let $f$ be monotone and submodular on the subsets of $V$, with $f(\emptyset) = 0$, and let $S^\ast$ maximize $f$ over the sets of size $k \le |V|$. With an exact oracle $\sigma = f$, GREEDY-IM returns $S_k$ with
$$f(S_k) \ge \Bigl(1 - \bigl(1 - \tfrac1k\bigr)^k\Bigr) f(S^\ast) \ge \Bigl(1 - \frac1e\Bigr) f(S^\ast).$$

*Proof.* Let $S_i$ be the set after $i$ rounds and $g_i = f(S^\ast) - f(S_i)$. Write $S^\ast \setminus S_i = \{v_1, \dots, v_j\}$ with $j \le k$. By monotonicity and then a telescoping sum,
$$f(S^\ast) \le f(S_i \cup S^\ast) = f(S_i) + \sum_{l=1}^{j} \bigl(f(S_i \cup \{v_1, \dots, v_l\}) - f(S_i \cup \{v_1, \dots, v_{l-1}\})\bigr).$$
By submodularity each term is at most $f(S_i \cup \{v_l\}) - f(S_i)$, and line L5 chose $u$ with the largest such gain, so each term is at most $f(S_{i+1}) - f(S_i)$. Hence $g_i \le k (g_i - g_{i+1})$, that is $g_{i+1} \le (1 - 1/k) g_i$. With $g_0 = f(S^\ast)$, we get $g_k \le (1 - 1/k)^k f(S^\ast) \le e^{-1} f(S^\ast)$, using $1 - x \le e^{-x}$. $\square$

**Corollary.** With an exact spread oracle, GREEDY-IM returns, under the independent cascade model or the linear threshold model, a set $S$ of size $\min(k, n)$ with $\sigma(S) \ge (1 - 1/e) \max_{|T| = k} \sigma(T)$. If $k \ge n$, it returns $V$, which is optimal by monotonicity. This follows from Lemma 4 and the theorem.

**Approximate oracles.** Suppose every call returns a value within $\pm \delta$ of the truth (additive). Then each computed gain is within $\pm 2\delta$ of the true gain, so the true gain of the chosen vertex is at least the largest true gain minus $4\delta$. The recurrence becomes $g_i \le k(g_i - g_{i+1} + 4\delta)$, that is $g_{i+1} \le (1 - 1/k) g_i + 4\delta$, and summing the geometric series gives $f(S_k) \ge (1 - 1/e) f(S^\ast) - 4k\delta$. Since $f(S^\ast) \ge k$ when $k \le n$ (the seeds count themselves), choosing $\delta = \varepsilon/4$ gives $f(S_k) \ge (1 - 1/e - \varepsilon) f(S^\ast)$. Monte Carlo estimates reach this accuracy with high probability by the Hoeffding inequality.

∎
