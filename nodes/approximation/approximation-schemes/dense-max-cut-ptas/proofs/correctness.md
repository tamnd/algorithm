---
title: The sampling scheme loses at most n²/√t + n²/(2ℓ) edges in expectation
proves: [correctness, time.worst]
status: full
---

**Statement.** Let $G = (V, E)$ be a graph with $n$ vertices, and let $\ell \ge 2$ and $t \ge 1$ be integers with $\ell \le n$. Let $\mathrm{ALG}$ be the cut value returned by DENSE-MAX-CUT$(G, \ell, t)$ and $\mathrm{OPT}$ the maximum cut value. Then

$$\mathbb{E}[\mathrm{OPT} - \mathrm{ALG}] \le \frac{n^2}{\sqrt t} + \frac{n^2}{2\ell},$$

and the running time is $O(2^{\ell t}(nt + n^2))$ with an adjacency matrix. If $|E| \ge \delta n^2$ and $\ell = \lceil 2/(\varepsilon\delta) \rceil$, $t = \lceil 16/(\varepsilon\delta)^2 \rceil$, then $\mathbb{E}[\mathrm{ALG}] \ge (1 - \varepsilon)\,\mathrm{OPT}$, and the best of $r$ independent runs with these parameters for $\varepsilon/2$ is at least $(1 - \varepsilon)\,\mathrm{OPT}$ with probability at least $1 - 2^{-r}$.

**Notation.** A cut is a map $\sigma : V \to \{0, 1\}$. Line L1 gives parts $V_1, \ldots, V_\ell$, and line L2 gives, for each $j$, a list $u_{j,1}, \ldots, u_{j,t}$ of vertices drawn uniformly and independently from $W_j = V \setminus V_j$. Write $N_j = |W_j| \le n$. For a cut $\sigma$ and $v \in V_j$ let $d^b(v)$ be the number of neighbours $u \in W_j$ of $v$ with $\sigma(u) = b$, and $g_v = d^0(v) - d^1(v)$.

**Placement rule.** Given labels $s_{j,i} \in \{0,1\}$ for the samples, lines L5 and L6 compute $a_b(v) = |\{i : u_{j,i} \in N(v),\ s_{j,i} = b\}|$ and put $v$ on side 1 if and only if $a_0(v) \ge a_1(v)$. Define the estimate $\hat g_v = (N_j / t)(a_0(v) - a_1(v))$. Then $v$ goes to side 1 if and only if $\hat g_v \ge 0$.

**Hybrids.** Let $\sigma^*$ be a maximum cut. Define cuts $H_0, H_1, \ldots, H_\ell$ by $H_0 = \sigma^*$ and, for $j \ge 1$: label the samples of part $j$ by $s_{j,i} = H_{j-1}(u_{j,i})$; let $H_j$ agree with $H_{j-1}$ outside $V_j$ and place each $v \in V_j$ by the rule above. Then $H_j$ places $V_1, \ldots, V_j$ by the rule and $V_{j+1}, \ldots, V_\ell$ as $\sigma^*$.

**Lemma 1 (the hybrid is a guess).** The cut $H_\ell$ equals the output of lines L4 to L6 for one labelling tried in line L3. So $\mathrm{ALG} \ge \mathrm{cut}(H_\ell)$.

*Proof.* The placement of $V_j$ depends only on the labels of the samples of part $j$. In $H_\ell$, the part $V_j$ is placed by the labels $s_{j,i} = H_{j-1}(u_{j,i})$ and never changed later. Line L3 tries every labelling of all $\ell t$ sample slots, so it tries this one, and line L8 keeps a cut at least as large. $\square$

**Lemma 2 (one step).** For each $j$, with $g_v$ taken with respect to $H_{j-1}$,
$$\mathrm{cut}(H_j) \ge \mathrm{cut}(H_{j-1}) - \sum_{v \in V_j} |\hat g_v - g_v| - e(V_j),$$
where $e(V_j)$ is the number of edges with both ends in $V_j$.

*Proof.* $H_{j-1}$ and $H_j$ agree on $W_j$, so edges with both ends in $W_j$ contribute the same to both cuts. Edges inside $V_j$ contribute between $0$ and $e(V_j)$ to each cut, so they lose at most $e(V_j)$. For an edge from $v \in V_j$ to $W_j$, the contribution depends only on the side of $v$: if $v$ is on side $b$, then $v$ cuts $c_v(b) = d^{1-b}(v)$ such edges, and $c_v(1) - c_v(0) = g_v$. The rule picks side 1 if and only if $\hat g_v \ge 0$. If $\hat g_v$ and $g_v$ have the same sign, or $g_v = 0$, the rule picks a side with $c_v = \max(c_v(0), c_v(1))$. Otherwise it loses $|g_v| \le |\hat g_v - g_v|$ against the better side. In both cases the new contribution is at least the old one minus $|\hat g_v - g_v|$. Summing over $v \in V_j$ gives the claim. $\square$

**Lemma 3 (the sampling error).** Fix the samples of parts $1, \ldots, j-1$, so that $H_{j-1}$ is fixed. Then for each $v \in V_j$, $\mathbb{E}\,|\hat g_v - g_v| \le N_j/\sqrt t$, the expectation over the samples of part $j$.

*Proof.* Let $X_i = 1$ if $u_{j,i}$ is a neighbour of $v$ with $H_{j-1}(u_{j,i}) = 0$, $X_i = -1$ if it is a neighbour with $H_{j-1}(u_{j,i}) = 1$, and $X_i = 0$ otherwise. The samples are uniform on $W_j$ and independent of $H_{j-1}$, so the $X_i$ are independent with $\mathbb{E} X_i = g_v / N_j$ and $\mathbb{E} X_i^2 \le 1$. Now $\hat g_v = (N_j/t) \sum_i X_i$ has mean $g_v$ and variance at most $N_j^2/t$. By the Cauchy-Schwarz inequality, $\mathbb{E}\,|\hat g_v - g_v| \le \sqrt{\mathrm{Var}\,\hat g_v} \le N_j/\sqrt t$. $\square$

**Proof of the bound.** By Lemma 1 and a telescoping sum of Lemma 2,
$$\mathrm{OPT} - \mathrm{ALG} \le \mathrm{cut}(H_0) - \mathrm{cut}(H_\ell) \le \sum_{j=1}^{\ell} \Big( \sum_{v \in V_j} |\hat g_v - g_v| + e(V_j) \Big).$$
Take expectations step by step, conditioning on the earlier samples. Lemma 3 bounds the first sum by $|V_j|\, n/\sqrt t$, and these add up to $n^2/\sqrt t$. Each part has $|V_j| \le n/\ell + 1$ vertices, so $e(V_j) \le |V_j|(|V_j| - 1)/2 \le |V_j|\, n/(2\ell)$, and these add up to $n^2/(2\ell)$.

**The parameters.** A cut with at least $|E|/2$ edges exists (put each vertex on the side that cuts more of its edges to the vertices placed before it), so $\mathrm{OPT} \ge \delta n^2/2$ when $|E| \ge \delta n^2$. With $\ell \ge 2/(\varepsilon\delta)$ and $t \ge 16/(\varepsilon\delta)^2$, we get $1/(2\ell) \le \varepsilon\delta/4$ and $1/\sqrt t \le \varepsilon\delta/4$, so $\mathbb{E}[\mathrm{OPT} - \mathrm{ALG}] \le \varepsilon\delta n^2/2 \le \varepsilon\,\mathrm{OPT}$.

**Amplification.** Run with the parameters for $\varepsilon/2$. The loss $\mathrm{OPT} - \mathrm{ALG}$ is non-negative with mean at most $(\varepsilon/2)\,\mathrm{OPT}$, so by Markov's inequality $\Pr[\mathrm{OPT} - \mathrm{ALG} > \varepsilon\,\mathrm{OPT}] \le 1/2$. The runs are independent, so all $r$ of them fail with probability at most $2^{-r}$.

**Time.** Lines L1 and L2 cost $O(n + \ell t)$. Line L3 tries $2^{\ell t}$ labellings. For each one, lines L4 to L6 cost $O(nt)$, since each vertex checks $t$ samples with an $O(1)$ adjacency test, and line L7 costs $O(n^2)$. The total is $O(2^{\ell t}(nt + n^2))$. With the parameters above, $\ell t = O(1/(\varepsilon\delta)^3)$, so the time is $2^{O(1/(\varepsilon\delta)^3)} n^2$ when $t \le n$. $\blacksquare$
