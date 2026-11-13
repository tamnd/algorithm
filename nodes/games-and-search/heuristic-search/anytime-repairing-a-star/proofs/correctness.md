---
title: Each search of ARA* gives a path of cost at most eps' C*, and the last one is optimal
proves: [correctness]
status: full
---

We use the pseudocode of the page. The graph is directed, the set of states reachable from $s_0$ is finite, each action cost $c(u, v)$ is positive, and $h$ is consistent with $h(s_g) = 0$. We write $g^*(u)$ for the cost of a cheapest path from $s_0$ to $u$, $d(u, v)$ for the cost of a cheapest path from $u$ to $v$, and $C^* = g^*(s_g)$. A call of IMPROVE-PATH with weight $\varepsilon$ uses the key fvalue$(u) = g[u] + \varepsilon\,h(u)$.

For a state $u$, let $v(u)$ be the value of $g[u]$ at the last expansion of $u$ (line L13), and $v(u) = \infty$ if $u$ was never expanded. Since $g$ only goes down, $g[u] \le v(u)$. We call $u$ *settled* if $g[u] = v(u) < \infty$: it was expanded and its value has not dropped since.

**Fact 1 (real paths).** Each value $g[u] < \infty$ is the cost of a path from $s_0$ to $u$, so $g[u] \ge g^*(u)$. The parent pointers from $s_g$ lead back to $s_0$ along a path of cost at most $g[s_g]$.

*Proof.* Line L16 sets $g[u] = g[s] + c(s, u)$ and parent$[u] = s$, and $g[s]$ is the cost of a path by induction. Later $g[s]$ can only drop, so each pointer satisfies $g[u] \ge g[s] + c(s, u)$. The costs are positive, so $g$ falls strictly along the pointers, the pointers form no cycle, and they end at $s_0$, the only state with no parent ($g[s_0] = 0$ is never lowered). Adding the inequalities along the chain gives a path of cost at most $g[s_g]$. $\square$

**Fact 2 (bookkeeping).** At each test of line L12, during a call:

1. a state that was expanded in this call is in CLOSED, and it is never put in OPEN again in this call;
2. a state that has a value $g$, is not settled, and was not expanded in this call is in OPEN;
3. a state that was expanded in this call and is not settled is in INCONS;
4. once $g[s_g] < \infty$, the goal is in OPEN and is never expanded.

*Proof.* Part 1 is lines L13 and L17. For parts 2 and 3, a state loses its settled status only when line L16 lowers its $g$, and then line L17 puts it in OPEN, or line L18 puts it in INCONS if it is in CLOSED. A state leaves OPEN only by an expansion, which makes it settled, and $s_0$ starts in OPEN. Between calls, line L8 moves INCONS into OPEN and line L9 empties CLOSED, so parts 2 and 3 hold at the start of the next call. For part 4, the goal is never in CLOSED before it has a finite $g$, so line L17 puts it in OPEN. While it is in OPEN, the least key in OPEN is at most fvalue$(s_g)$, so the state that line L13 removes has a key strictly below fvalue$(s_g)$ and is not the goal. $\square$

By part 1, each call expands each state at most once. The reachable set is finite, so each call ends, and the schedule is finite, so ARA* ends.

**Lemma 3 (a good state in OPEN).** Consider a test of line L12 in a call with weight $\varepsilon$, and suppose that each state expanded so far in this call had $g \le \varepsilon\,g^*$ at its expansion. Let $P = (p_0, \ldots, p_k)$ be a cheapest path from $s_0$, and suppose that $p_k$ has no value $g$ or has $g[p_k] > \varepsilon\,g^*(p_k)$. Then some $p_j$ with $j < k$ is in OPEN and has $g[p_j] \le \varepsilon\,g^*(p_j)$.

*Proof.* Let $i$ be the least index such that $p_i$ has no value $g$ or has $g[p_i] > \varepsilon\,g^*(p_i)$. Then $i \ge 1$, since $g[s_0] = 0$, and $p_{i-1}$ has $g[p_{i-1}] \le \varepsilon\,g^*(p_{i-1})$. We show that $p_{i-1}$ is in OPEN, which proves the lemma with $j = i - 1$.

Suppose that $p_{i-1}$ was expanded in this call. Its value at that time was at most $\varepsilon\,g^*(p_{i-1})$, and the expansion looked at the action to $p_i$, so afterwards
$$g[p_i] \le \varepsilon\,g^*(p_{i-1}) + c(p_{i-1}, p_i) \le \varepsilon\,\bigl(g^*(p_{i-1}) + c(p_{i-1}, p_i)\bigr) = \varepsilon\,g^*(p_i),$$
using $\varepsilon \ge 1$ and the fact that a part of a cheapest path is a cheapest path. This contradicts the choice of $i$. Suppose next that $p_{i-1}$ is settled. Its last expansion had the value $g[p_{i-1}]$ and looked at the action to $p_i$, so $g[p_i] \le g[p_{i-1}] + c(p_{i-1}, p_i) \le \varepsilon\,g^*(p_i)$ by the same computation, again a contradiction. So $p_{i-1}$ has a value $g$, is not settled, and was not expanded in this call, and Fact 2 part 2 puts it in OPEN. $\square$

**Theorem 4 (the weight bound).** In a call with weight $\varepsilon$, each state $s$ expanded at line L13 has $g[s] \le \varepsilon\,g^*(s)$ at that time. If the goal is reachable, then at the end of the call $g[s_g] \le \varepsilon\,C^*$.

*Proof.* By induction on the expansions of the call. Suppose that the claim holds for the earlier expansions of the call and that line L13 removes $s$ with $g[s] > \varepsilon\,g^*(s)$. Lemma 3, applied to a cheapest path to $s$, gives $p_j$ in OPEN with $g[p_j] \le \varepsilon\,g^*(p_j)$. Consistency gives $h(p_j) \le d(p_j, s) + h(s)$, so
$$\mathrm{fvalue}(p_j) \le \varepsilon\,g^*(p_j) + \varepsilon\,\bigl(d(p_j, s) + h(s)\bigr) = \varepsilon\,g^*(s) + \varepsilon\,h(s) < g[s] + \varepsilon\,h(s) = \mathrm{fvalue}(s),$$
because $g^*(p_j) + d(p_j, s) = g^*(s)$ on a cheapest path. This contradicts the choice of $s$ as a state of least key.

At the end of the call, the test of line L12 fails: OPEN is empty, or fvalue$(s_g)$ is at most the least key in OPEN. Suppose that $s_g$ has no value $g$ or $g[s_g] > \varepsilon\,C^*$. Lemma 3, applied to a cheapest path to $s_g$, gives $p_j$ in OPEN, so OPEN is not empty, and
$$\mathrm{fvalue}(p_j) \le \varepsilon\,g^*(p_j) + \varepsilon\,h(p_j) \le \varepsilon\,g^*(p_j) + \varepsilon\,d(p_j, s_g) = \varepsilon\,C^* < g[s_g] = \mathrm{fvalue}(s_g),$$
using $h(p_j) \le d(p_j, s_g) + h(s_g)$ and $h(s_g) = 0$. So the test of line L12 would not fail, a contradiction. $\square$

**Corollary 5 (failure).** ARA* returns failure at line L4 if and only if the goal cannot be reached.

*Proof.* If the goal can be reached, Theorem 4 gives $g[s_g] \le \varepsilon_1 C^* < \infty$ after the first call. If it cannot be reached, Fact 1 shows that $g[s_g]$ stays $\infty$. $\square$

**Lemma 6 (a lower bound on $C^*$).** If the goal is reachable, then at the end of each call
$$L = \min_{u \in \mathrm{OPEN} \cup \mathrm{INCONS}} \bigl(g[u] + h(u)\bigr) \le C^*.$$

*Proof.* This is Lemma 3 with weight 1, but with INCONS added. Let $P = (p_0, \ldots, p_k)$ be a cheapest path from $s_0$ to $s_g$. If $g[p_i] = g^*(p_i)$ for each $i$, then $g[s_g] = C^*$, and the goal is in OPEN by Fact 2 part 4, so $L \le g[s_g] + h(s_g) = C^*$. Otherwise let $i$ be the least index such that $p_i$ has no value $g$ or $g[p_i] > g^*(p_i)$. Then $i \ge 1$ and $g[p_{i-1}] = g^*(p_{i-1})$ by Fact 1. If $p_{i-1}$ were settled, its last expansion would give $g[p_i] \le g^*(p_{i-1}) + c(p_{i-1}, p_i) = g^*(p_i)$, which is false. So $p_{i-1}$ is not settled, and by Fact 2 parts 2 and 3 it is in OPEN or in INCONS. Consistency gives $h(p_{i-1}) \le d(p_{i-1}, s_g)$, so $L \le g^*(p_{i-1}) + d(p_{i-1}, s_g) = C^*$. $\square$

**Theorem 7 (the reported bound).** Let the goal be reachable. After each call, the path of line L5 or L11 costs at most $g[s_g]$, and $g[s_g] \le \varepsilon' C^*$ with $\varepsilon' = \min(\varepsilon, g[s_g] / L)$. Also $\varepsilon' \ge 1$.

*Proof.* The path costs at most $g[s_g]$ by Fact 1. Theorem 4 gives $g[s_g] \le \varepsilon\,C^*$. If $L > 0$, Lemma 6 gives $g[s_g] = (g[s_g] / L)\,L \le (g[s_g] / L)\,C^*$. Together, $g[s_g] \le \varepsilon' C^*$. If $L = 0$, BOUND gives $\varepsilon' = \varepsilon$ and the first inequality is enough. Finally $g[s_g] \ge C^* \ge L$ by Fact 1 and Lemma 6, so $g[s_g] / L \ge 1$, and $\varepsilon \ge 1$. $\square$

**Theorem 8 (monotone values and optimality).** The values $g[s_g]$ that ARA* publishes never increase. When ARA* stops after a call that published a path, that path costs exactly $C^*$.

*Proof.* The value $g[s_g]$ only goes down, at line L16. The loop of line L6 stops when $\varepsilon' \le 1$, which happens at the latest after the call with $\varepsilon_k = 1$, since then $\varepsilon' \le \varepsilon = 1$. By Theorem 7 the last path costs at most $g[s_g] \le \varepsilon' C^* \le C^*$, and it costs at least $C^*$ because it is a path from $s_0$ to $s_g$. $\square$

**Remark.** The published path can cost less than the published value $g[s_g]$: this happens when a state on the path got a lower $g$ after its successor on the path was last updated, and it waits in INCONS for the next call. The bound of Theorem 7 holds for both numbers. The proof needs consistency only in Lemma 3 through Theorem 4 and Lemma 6. With an admissible $h$ that is not consistent, a call can need to reexpand a state to keep the bound, and line L18 forbids that.
