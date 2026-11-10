---
title: The Bar-Yehuda-Even algorithm returns a vertex cover of weight at most twice the optimum
proves: [correctness]
status: full
---

**Statement.** Let $G = (V, E)$ be a finite graph without self-loops and $w : V \to \mathbb{R}_{\ge 0}$. Let the edges be scanned in any order $e_1, \ldots, e_m$, and let $\varepsilon_i$ be the amount of line L3 at $e_i$. Then BAR-YEHUDA-EVEN returns a set $C$ such that:

1. $C$ is a vertex cover of $G$;
2. $w(S) \ge \sum_{i=1}^m \varepsilon_i$ for each vertex cover $S$;
3. $w(C) \le 2 \sum_{i=1}^m \varepsilon_i \le 2 \cdot \text{OPT}$.

**Invariant.** Let $r_i$ be the residual weight function after the step at $e_i$, and $r_0 = w$. We claim that for each $i$, $r_i \ge 0$ and

$$w = \sum_{k=1}^{i} \varepsilon_k (\mathbf{1}_{u_k} + \mathbf{1}_{v_k}) + r_i, \qquad (\ast)$$

where $e_k = u_k v_k$ and $\mathbf{1}_v$ is the function that is 1 on $v$ and 0 elsewhere. For $i = 0$ this is line L1. Assume it for $i - 1$. Line L3 sets $\varepsilon_i = \min(r_{i-1}(u_i), r_{i-1}(v_i)) \ge 0$, and line L4 gives $r_i = r_{i-1} - \varepsilon_i (\mathbf{1}_{u_i} + \mathbf{1}_{v_i})$; as $u_i \ne v_i$, each of the two entries goes down by $\varepsilon_i$ once. So $(\ast)$ holds for $i$. Both changed entries stay at least $\min(r_{i-1}(u_i), r_{i-1}(v_i)) - \varepsilon_i = 0$, and the other entries do not change, so $r_i \ge 0$.

**Step 1: $C$ is a cover.** After the step at $e_i$, the end of $e_i$ that gave the minimum in line L3 has residual weight 0. Each later step lowers a residual weight or keeps it, and it stays nonnegative by the invariant, so this end still has residual weight 0 at the end, and line L5 puts it into $C$.

**Step 2: the lower bound.** Let $S$ be a vertex cover and write $r = r_m$. By $(\ast)$ with $i = m$,

$$w(S) = \sum_{k=1}^{m} \varepsilon_k \, |S \cap \{u_k, v_k\}| + r(S).$$

Each $e_k$ has an end in $S$, so $|S \cap \{u_k, v_k\}| \ge 1$, and $\varepsilon_k \ge 0$ and $r(S) \ge 0$. So $w(S) \ge \sum_k \varepsilon_k$. With an optimal $S$, this gives $\sum_k \varepsilon_k \le \text{OPT}$.

**Step 3: the upper bound.** Apply the same identity to $C$. Each $|C \cap \{u_k, v_k\}| \le 2$, and $r(C) = 0$ because each vertex of $C$ has $r(v) = 0$. So

$$w(C) = \sum_{k=1}^{m} \varepsilon_k \, |C \cap \{u_k, v_k\}| + r(C) \le 2 \sum_{k=1}^{m} \varepsilon_k \le 2 \cdot \text{OPT},$$

where the last step is step 2.

**Termination.** Line L1 visits each vertex once and the loop of line L2 visits each edge once, with $O(1)$ work per edge. $\blacksquare$
