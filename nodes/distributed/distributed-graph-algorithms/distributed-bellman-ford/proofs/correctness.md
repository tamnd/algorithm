---
title: Distributed Bellman-Ford computes the distances
proves: [correctness]
status: full
---

The graph $G = (V, E)$ is connected and undirected, with weights $w(e) \ge 0$, and $s$ is the source. For $r \ge 0$ let $d_r(v)$ be the least weight of a walk from $s$ to $v$ with at most $r$ edges ($\infty$ if there is none). Then $d_0(s) = 0$ and $d_0(v) = \infty$ for $v \ne s$, and for $r \ge 1$

$$d_r(v) = \min\Big(d_{r-1}(v),\ \min_{u : \{u, v\} \in E} \big(d_{r-1}(u) + w(u, v)\big)\Big),$$

because a walk with at most $r$ edges either has at most $r - 1$ edges, or is a walk with at most $r - 1$ edges to a neighbour $u$ of $v$, followed by the edge $\{u, v\}$.

**Lemma 1 (synchronous rounds).** After round $r$ of the synchronous algorithm, $\text{dist}_v = d_r(v)$ for each node $v$. If $\text{dist}_v < \infty$ and $v \ne s$, then $\text{parent}_v = u$ is a neighbour with $\text{dist}_v = d_{r'}(u) + w(u, v)$ for the round $r' + 1 \le r$ in which line L6 last ran at $v$.

*Proof.* By induction on $r$. Line L1 gives the case $r = 0$. In round $r \ge 1$, line L3 sends the values at the end of round $r - 1$, which are $d_{r-1}(u)$ by the induction hypothesis, because all nodes send before any node computes. Lines L4 to L6 set $\text{dist}_v$ to the minimum of $d_{r-1}(v)$ and the values $d_{r-1}(u) + w(u, v)$, which is $d_r(v)$ by the recurrence. Line L6 sets the parent to the neighbour that gave the new minimum. $\square$

**Lemma 2.** $d_{n-1}(v) = d(s, v)$ for each $v$.

*Proof.* Each walk from $s$ to $v$ has weight at least $d(s, v)$, so $d_{n-1}(v) \ge d(s, v)$. A shortest walk can be taken without a repeated node: removing a closed sub-walk does not raise the weight, since all weights are non-negative. A walk without a repeated node has at most $n - 1$ edges, so $d_{n-1}(v) \le d(s, v)$. $\square$

**Theorem 1.** After the $n - 1$ rounds, $\text{dist}_v = d(s, v)$ for each $v$, and the parent edges form a shortest path tree rooted at $s$.

*Proof.* The first part follows from Lemmas 1 and 2. For the tree: let $v \ne s$ and $u = \text{parent}_v$. By Lemma 1, $d(s, v) = \text{dist}_v = \text{dist}_u^{\text{old}} + w(u, v)$, where $\text{dist}_u^{\text{old}} \ge \text{dist}_u = d(s, u)$ is the value of $u$ when it was sent. Also $d(s, v) \le d(s, u) + w(u, v)$. So $\text{dist}_u^{\text{old}} = d(s, u)$ and $d(s, v) = d(s, u) + w(u, v)$. Let $t_x$ be the last round in which line L6 ran at $x$, with $t_s = 0$ (the value of $s$ never changes, since $d + w \ge 0$). The value that $u$ sent in round $t_v$ was its value at the end of round $t_v - 1$, and it was already final, so $t_u \le t_v - 1 < t_v$. The rounds $t$ strictly decrease along the parent pointers, so the pointers have no cycle and every chain of them ends at $s$. They form a tree rooted at $s$ in which each tree path has weight $d(s, v)$. $\blacksquare$

**Theorem 2 (asynchronous version).** Assume that the channels are reliable and that each message arrives after a finite delay. Then the asynchronous algorithm sends finitely many messages, and when the last one is served, $\text{dist}_v = d(s, v)$ for each $v$.

*Proof.* *Lower bound.* Each finite value of $\text{dist}_v$ is the weight of a walk from $s$ to $v$: this holds at the start, and line L6 extends the walk of $u$ by the edge $\{u, v\}$. So $\text{dist}_v \ge d(s, v)$ at all times.

*Termination.* Let $W$ be the largest weight and $w_{\min}$ the smallest positive weight. Each value that $v$ takes after its first one is less than its first finite value, and it is the weight of a walk. A walk weight below a bound $L$ uses at most $L / w_{\min}$ positive edges, so it is a sum of at most $L / w_{\min}$ of the $m$ positive weights. There are finitely many such sums. The values of $v$ strictly decrease, so $v$ changes its value finitely often, and each change sends $\deg(v)$ messages. So the run sends finitely many messages, and each is served after a finite delay.

*Upper bound.* At the end, consider an edge $\{u, v\}$. Node $u$ sent each of its values to $v$, the last one included, and $v$ served it. After line L5, $\text{dist}_v \le \text{dist}_u + w(u, v)$, and $\text{dist}_v$ only goes down later, while $\text{dist}_u$ did not change after its last message. So at the end $\text{dist}_v \le \text{dist}_u + w(u, v)$ for every edge, in both directions. Take a shortest path $s = x_0, x_1, \ldots, x_k = v$. Then $\text{dist}_{x_0} = 0$, and by induction $\text{dist}_{x_i} \le d(s, x_i)$. With the lower bound, $\text{dist}_v = d(s, v)$. $\blacksquare$

**Count to infinity.** Take the chain $s, A, B$ with unit weights, so that $A$ holds 1 and $B$ holds 2. The link $\{s, A\}$ fails, and in each synchronous round each of $A$ and $B$ sets its value to 1 plus the old value of its one remaining neighbour, capped at $K$. *Claim:* for $1 \le r \le K - 2$, after round $r$ the two values are $r + 1$ and $r + 2$. *Proof.* After round 1 they are $A = 2 + 1 = 3$ and $B = 1 + 1 = 2$. If after round $r$ the values are $r + 1$ and $r + 2$ in some order, then the node with $r + 1$ gets $r + 3$ and the node with $r + 2$ keeps $r + 2$, which is the claim for $r + 1$. So after round $K - 2$ the values are $K - 1$ and $K$, and after round $K - 1$ both are $K$. With no cap, the values grow without bound and the run never stops. $\square$
