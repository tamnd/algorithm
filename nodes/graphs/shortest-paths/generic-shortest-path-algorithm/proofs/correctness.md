---
title: The generic relaxation method is correct for every order
proves: [correctness, termination]
status: full
---

**Claim.** Let $G$ be a directed graph with real weights and a source $s$, and fix any rule for line L4. GENERIC-SSSP ends. It returns NEGATIVE-CYCLE if and only if a cycle of negative weight is reachable from $s$. Otherwise it returns $d[v] = \delta(s, v)$ for every $v$, with $+\infty$ for the vertices that $s$ does not reach, and $d[v] = d[\pi[v]] + w(\pi[v], v)$ for every $v \ne s$ with $d[v] < \infty$.

**Step 1: labels are walk weights.** Assign to each finite label a walk: $W_s = (s)$ for $d[s] = 0$, and when line L5 sets $d[v] = d[u] + w(u, v)$, let $W_v$ be the current $W_u$ followed by the edge $(u, v)$. By induction on the steps, $d[v] = w(W_v)$ and $h[v]$ is the number of edges of $W_v$ at all times. Hence, if no negative cycle is reachable from $s$, $d[v] \ge \delta(s, v)$ at all times.

**Step 2: a repeated vertex gives a negative cycle.** Every prefix of $W_v$ ending at a vertex $x$ is $W_x$ as it was at an earlier setting of $d[x]$, and these settings occur in increasing time along $W_v$. If $x$ occurs twice, at settings $t_1 < t_2$, then $W_x(t_2) = W_x(t_1)\, C$ for a closed walk $C$, and $d_{t_2}[x] = d_{t_1}[x] + w(C)$. Each setting strictly lowers the label (line L3 requires a tense edge), so $w(C) < 0$. A closed walk of negative weight contains a simple cycle of negative weight, and it is reachable from $s$ along $W_v$.

**Step 3: the report is sound.** Line L6 fires only when $W_v$ has at least $n$ edges, hence at least $n + 1$ vertex occurrences, and so repeats a vertex. By Step 2, a negative cycle is reachable from $s$.

**Step 4: termination.** As long as line L6 has not fired, every $W_v$ has at most $n - 1$ edges, so every label is the weight of one of the finitely many walks from $s$ with at most $n - 1$ edges. Each step strictly lowers one label, so the number of steps is finite. Each step either fires line L6 or loops back to line L3, which ends the loop when no tense edge is left. So the algorithm ends.

**Step 5: no negative cycle gives the distances.** Suppose no negative cycle is reachable from $s$. By Step 3, line L6 never fires, so by Step 4 the loop ends with no tense edge: $d[v] \le d[u] + w(u, v)$ for every edge with $d[u] < \infty$. The label $d[s]$ is the weight of a closed walk from $s$, at least $\delta(s, s) = 0$ by Step 1, and it starts at 0, so $d[s] = 0$. For a reachable $v$ with a shortest path $s = p_0, \ldots, p_r = v$, induction along the path gives $d[p_i] < \infty$ and $d[p_{i+1}] \le d[p_i] + w(p_i, p_{i+1})$, and adding up, $d[v] \le w(P) = \delta(s, v)$. With Step 1, $d[v] = \delta(s, v)$. An unreachable $v$ has no walk from $s$, so its label stays $\infty$. For the predecessor of $v \ne s$: when $d[v]$ was last set, $d[v] = d_{\text{then}}[\pi[v]] + w(\pi[v], v) \ge d[\pi[v]] + w(\pi[v], v)$ since labels only fall, and the edge is not tense at the end, so equality holds.

**Step 6: a reachable negative cycle is reported.** Suppose a negative cycle $C = (c_0, \ldots, c_{k-1}, c_0)$ is reachable from $s$ and the algorithm returns labels. By Step 4 the loop ended with no tense edge. As in Step 5, every vertex on a path from $s$ has a finite label, so $d[c_{i+1}] \le d[c_i] + w(c_i, c_{i+1})$ for each $i$ (indices modulo $k$); adding these, the labels cancel and $0 \le w(C) < 0$, a contradiction. So the algorithm returns NEGATIVE-CYCLE.

Steps 3 to 6 give the claim. $\blacksquare$
