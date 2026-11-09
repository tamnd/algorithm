---
title: The kd-tree search returns a nearest point
proves: [correctness, termination]
status: full
---

**Setting.** For a node $v$ let $S(v)$ be the set of points stored in the subtree of $v$ ($S(\mathrm{nil}) = \emptyset$). The tree property is: for every node $v$ with point $p$ and axis $a$, every $r \in S(v.\mathrm{left})$ has $r[a] \le p[a]$ and every $r \in S(v.\mathrm{right})$ has $r[a] \ge p[a]$. Write $\beta$ for the value of $best.d2$ ($\infty$ when no point has been seen). It never increases, because line L6 only replaces it by a smaller value.

**Lemma 1 (far side bound).** Let $v$ have point $p$, axis $a$, and $\mathrm{diff} = q[a] - p[a]$, and let $far$ be chosen by line L8. Then every $r \in S(far)$ satisfies $\|q - r\|^2 \ge \mathrm{diff}^2$.

*Proof.* If $\mathrm{diff} < 0$, then $far = v.\mathrm{right}$, so $r[a] \ge p[a] > q[a]$ and $r[a] - q[a] \ge p[a] - q[a] = -\mathrm{diff} > 0$. If $\mathrm{diff} \ge 0$, then $far = v.\mathrm{left}$, so $r[a] \le p[a] \le q[a]$ and $q[a] - r[a] \ge \mathrm{diff} \ge 0$. In both cases $(q[a] - r[a])^2 \ge \mathrm{diff}^2$, and $\|q - r\|^2 \ge (q[a] - r[a])^2$ because the other squared coordinate differences are non-negative. $\square$

**Lemma 2 (one call).** Let $\beta_0$ be the value of $best.d2$ when SEARCH$(v)$ starts and $\beta_1$ the value when it returns. Then $\beta_1 \le \min(\beta_0, \min_{r \in S(v)} \|q - r\|^2)$, and $best$ always holds a point of $P$ at squared distance $\beta$ from $q$ (once $\beta < \infty$).

*Proof.* By induction on the height of the subtree of $v$. For $v = \mathrm{nil}$ the call returns at once and $S(v) = \emptyset$, so $\beta_1 = \beta_0$. Otherwise, after line L6, $\beta \le \|q - p\|^2$. By induction, after line L9, $\beta \le \min_{r \in S(near)} \|q - r\|^2$. At line L10, if $\mathrm{diff}^2 < \beta$, the call on $far$ makes $\beta \le \min_{r \in S(far)} \|q - r\|^2$ by induction. If $\mathrm{diff}^2 \ge \beta$, then by Lemma 1 every $r \in S(far)$ has $\|q - r\|^2 \ge \mathrm{diff}^2 \ge \beta$, so the bound holds already. Since $S(v) = \{p\} \cup S(near) \cup S(far)$ and $\beta$ never increases, $\beta_1$ is at most the squared distance from $q$ to every point of $S(v)$, and $\beta_1 \le \beta_0$. The second claim holds because line L6 always stores a point together with its own squared distance. $\square$

**Termination.** Each call on a node makes at most two calls on its children, and the tree is finite, so each node is visited at most once and the search stops.

**Conclusion.** NEAREST starts with $\beta = \infty$ and calls SEARCH on the root, so by Lemma 2 the returned $\beta$ is at most $\|q - r\|^2$ for every $r \in P$. If $P \ne \emptyset$, the root's own point is compared in line L6, so $\beta < \infty$ and $best$ is a point of $P$ at squared distance $\beta$, which is therefore $\min_{r \in P} \|q - r\|^2$. If $P = \emptyset$, the result is none. $\blacksquare$
