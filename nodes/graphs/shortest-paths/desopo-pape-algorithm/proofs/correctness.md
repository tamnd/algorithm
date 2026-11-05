---
title: The D'Esopo-Pape algorithm with edge counts is correct and ends
proves: [correctness, termination]
status: full
---

**Claim.** Let $G$ be a directed graph with real weights and a source $s$. DESOPO-PAPE ends on every input. It returns NEGATIVE-CYCLE if and only if a cycle of negative weight is reachable from $s$. Otherwise it returns $d[v] = \delta(s, v)$ for every $v$ (with $+\infty$ for vertices not reachable from $s$), and for each $v \ne s$ with $d[v] < \infty$, $d[v] = d[\pi[v]] + w(\pi[v], v)$.

None of the steps uses the position at which a vertex enters the deque; they hold for any rule that puts a vertex into the deque when its label drops and it is not already there.

**Step 1: labels are walk weights.** Number the label changes in time order. To each finite label assign a walk: $W_s = (s)$ for the initial $d[s] = 0$, and when line L7 sets $d[v] = d[u] + w(u, v)$, let $W_v$ be the current walk of $u$ followed by the edge $(u, v)$. By induction, at all times $d[v] = w(W_v)$ and $h[v]$ is the number of edges of $W_v$. In particular $d[v] \ge \delta(s, v)$ whenever no negative cycle is reachable from $s$, since then every walk from $s$ to $v$ weighs at least $\delta(s, v)$.

**Step 2: a repeated vertex means a negative cycle.** Every prefix of $W_v$ that ends at a vertex $x$ is the walk $W_x$ as it was at some earlier label setting of $x$, and the settings along $W_v$ are in increasing time from the start to the end. Suppose $x$ occurs twice in $W_v$, and the two prefixes ending there correspond to settings at times $t_1 < t_2$. Then $W_x(t_2) = W_x(t_1)\, C$ for a closed walk $C$ from $x$, and $d_{t_2}[x] = d_{t_1}[x] + w(C)$. Each setting strictly lowers the label, so $d_{t_2}[x] < d_{t_1}[x]$, and $w(C) < 0$. A closed walk of negative weight splits into simple cycles, one of which is negative, and it is reachable from $s$ along $W_v$.

**Step 3: soundness of the report.** Line L7 returns NEGATIVE-CYCLE only when $h[v] \ge n$, so $W_v$ has at least $n + 1$ vertex occurrences and repeats a vertex. By Step 2 a negative cycle is reachable from $s$.

**Step 4: termination.** As long as no report happens, every $W_v$ has at most $n - 1$ edges, so every label value is the weight of one of the finitely many walks from $s$ with at most $n - 1$ edges. Labels only decrease, strictly, so each vertex has finitely many label changes. Each entry into the deque, apart from the first entry of $s$, follows a label change, and each pass of line L3 removes one entry. So the loop ends.

**Step 5: an empty deque means no tense edge.** Call $(u, v)$ tense if $d[u] < \infty$ and $d[u] + w(u, v) < d[v]$. Invariant: every tense edge $(u, v)$ has $u$ in the deque. At the start only $s$ has a finite label and $s$ is in the deque. Scanning $u$ in lines L5 to L9 relaxes each edge out of $u$, after which none of them is tense, as long as $d[u]$ is unchanged; if a self-loop lowers $d[u]$ during the scan, $u$ is put back in the deque by line L9. An edge $(x, y)$ can become tense only when $d[x]$ drops (a drop of $d[y]$ cannot make it tense), and line L7 to L9 then puts $x$ into the deque unless it is already there. So the invariant holds, and when the loop ends with an empty deque, no edge is tense.

**Step 6: no negative cycle gives the distances.** Suppose no negative cycle is reachable from $s$. By Step 3 there is no report, and by Step 4 the loop ends. $d[s] = 0$: the label of $s$ is a walk weight from $s$ to $s$, at least $\delta(s, s) = 0$ by Step 1, and it starts at 0. For $v$ reachable from $s$, take a shortest path $s = v_0, \ldots, v_k = v$. By Step 5, $d[v_{i+1}] \le d[v_i] + w(v_i, v_{i+1})$ for each $i$, once $d[v_i] < \infty$, which holds by induction from $d[v_0] = 0$. Adding gives $d[v] \le \delta(s, v)$, and with Step 1, $d[v] = \delta(s, v)$. A vertex that is not reachable never gets a finite label, since a finite label is the weight of a walk from $s$. For the predecessors: when $d[v]$ was last set, $d[v] = d_{\text{then}}[\pi[v]] + w(\pi[v], v) \ge d[\pi[v]] + w(\pi[v], v)$, and the edge is not tense at the end, so equality holds.

**Step 7: a reachable negative cycle is reported.** Suppose a negative cycle $C = (c_0, \ldots, c_{k-1}, c_0)$ is reachable from $s$, and suppose the algorithm returns distances. By Step 4 it ended with an empty deque, so by Step 5 no edge is tense. Every vertex on a path from $s$ then has a finite label, by induction along the path as in Step 6, so all $c_i$ have finite labels and $d[c_{i+1}] \le d[c_i] + w(c_i, c_{i+1})$ for each $i$ (indices modulo $k$). Adding these $k$ inequalities, the labels cancel and $0 \le w(C)$, a contradiction. So the algorithm returns NEGATIVE-CYCLE.

Steps 3, 4, 6 and 7 give the claim. $\blacksquare$
