---
title: The α-shortcut property of robust pruning and the approximation factor of greedy search
proves: [correctness]
status: full
---

Let $(P, \delta)$ be a finite metric space, $\alpha \ge 1$, and $N_{\text{out}}$ the out-lists of the graph.

**Lemma 1 (α-shortcut).** Let ROBUST-PRUNE$(p, V_0, \alpha, R)$ run and stop because $V$ became empty (not at line L9). Then for every $x \in (V_0 \cup N_{\text{out}}(p)) \setminus \{p\}$ that is not in the new $N_{\text{out}}(p)$, there is $p' \in N_{\text{out}}(p)$ with $\alpha \cdot \delta(p', x) \le \delta(p, x)$.

*Proof.* At line L6, $x \in V$. A point leaves $V$ only at line L8, by being added to $N_{\text{out}}(p)$, or at line L10. Since $x$ is not added and $V$ ends empty, $x$ is removed at line L10 in some round with kept point $p^*$, and the rule of that line gives $\alpha \cdot \delta(p^*, x) \le \delta(p, x)$. Take $p' = p^*$. $\square$

With full pruning, ROBUST-PRUNE$(p, P, \alpha, n)$ never stops at line L9, since $|N_{\text{out}}(p)| \le n - 1 < n$. So the lemma holds for every $x \in P \setminus \{p\}$ that is not an out-neighbor of $p$.

**Lemma 2 (greedy search stops at a local minimum).** With $L = 1$, GREEDY-SEARCH ends, and it returns a point $p$ such that $\delta(y, q) \ge \delta(p, q)$ for every $y \in N_{\text{out}}(p)$.

*Proof.* With $L = 1$ the list $\mathcal{L}$ holds one point after each step; call it the current point. Line L4 replaces the current point $p$ by the nearest of $\{p\} \cup N_{\text{out}}(p)$ (ties to the smaller index). If that is $p$ itself, $p \in V$ and the loop ends with $p$; then no out-neighbor is nearer to $q$ than $p$, up to ties broken in favor of $p$, so $\delta(y, q) \ge \delta(p, q)$ for all $y \in N_{\text{out}}(p)$. Otherwise the new point is strictly better in the order (distance, index), which can happen at most $n - 1$ times; so the loop ends. $\square$

**Theorem.** Suppose every out-list was built by ROBUST-PRUNE$(p, P, \alpha, n)$ with $\alpha > 1$. Let $x^*$ be a point of $P$ nearest to $q$ and $D = \delta(x^*, q)$. Greedy search with $L = 1$ from any start point returns $p$ with
$$\delta(p, q) \le \frac{\alpha + 1}{\alpha - 1} D.$$

*Proof.* Let $p$ be the returned point. If $p = x^*$, the bound holds. If $x^* \in N_{\text{out}}(p)$, Lemma 2 gives $\delta(p, q) \le \delta(x^*, q) = D$. Otherwise, by Lemma 1 there is $p' \in N_{\text{out}}(p)$ with $\alpha \cdot \delta(p', x^*) \le \delta(p, x^*)$. By Lemma 2 and the triangle inequality,
$$\delta(p, q) \le \delta(p', q) \le \delta(p', x^*) + D \le \frac{\delta(p, x^*)}{\alpha} + D \le \frac{\delta(p, q) + D}{\alpha} + D.$$
Multiply by $\alpha$ and collect the terms with $\delta(p, q)$: $(\alpha - 1)\,\delta(p, q) \le (\alpha + 1) D$. Since $\alpha > 1$, divide by $\alpha - 1$. $\blacksquare$
