---
title: The MuZero search terminates, keeps exact visit statistics, visits every action, and never overestimates with an exact model
proves: [correctness, termination]
status: full
---

We use the notation of the page. The model gives $g(s, a) = (r, s')$ and $f(s) = (p, v)$, the number of actions $A$ is finite, $0 \le \gamma < 1$, and the values $v$ and rewards $r$ that the model returns are bounded in absolute value. For a node $u$ with parent $w$, the value of $u$ seen from $w$ is $x(u) = r(u) + \gamma W(u)/N(u)$ when $N(u) > 0$. The root has $r = 0$.

**Termination.** A simulation with index $i$ starts with a tree of at most $1 + (i - 1)A$ nodes, so lines L4 and L5 stop after at most that many steps. Each node they reach has children. The node reached last has none, because the loop stops there. Lines L6 to L9 do a bounded amount of work for each node on the path. So each simulation, and the search, terminate. Each simulation expands exactly one node, the leaf, and gives it $A$ children, so after $N$ simulations the tree has $1 + (N + 1)A$ nodes at most.

**Lemma 1 (the statistics).** After any number of simulations, for every node $u$, $N(u)$ is the number of simulations whose path contains $u$, and $W(u)$ is the sum, over these simulations, of

$$G_u = \sum_{j=1}^{d - k}\gamma^{j - 1} r(u_{k + j}) + \gamma^{d - k} v,$$

where the path of the simulation is $u_0 = \text{root}, u_1, \ldots, u_d$, $u = u_k$, and $v$ is the value that line L7 got for the leaf $u_d$.

*Proof.* Line L9 changes $N(u)$ and $W(u)$ only for the nodes on the path, adding 1 to $N(u)$ for each. The loop of line L8 visits $u_d, u_{d-1}, \ldots, u_0$, with $G = v$ at $u_d$ and $G \leftarrow r(u_j) + \gamma G$ after $u_j$. By induction on $d - k$, the value of $G$ when the loop reaches $u_k$ is $G_{u_k}$: for $k = d$ it is $v$, and $G_{u_{k-1}} = r(u_k) + \gamma G_{u_k}$ is the formula for $k - 1$. $\square$

**Lemma 2 (bounded normalized values).** There is a constant $B$ such that $|\bar Q(u, a)| \le B$ for every node and action at every time.

*Proof.* If a child is unvisited, $\bar Q = 0$. Otherwise the last backup through the child $c$ fed $x(c)$ to the min-max statistics in line L9, and $x(c)$ has not changed since, so $\mathrm{lo} \le x(c) \le \mathrm{hi}$. If $\mathrm{hi} > \mathrm{lo}$, the normalized value is in $[0, 1]$. If $\mathrm{hi} = \mathrm{lo}$, every value fed so far equals the first value $x_0$, and $\bar Q = x_0$. Once $\mathrm{hi} > \mathrm{lo}$ it stays so. So $B = \max(1, |x_0|)$ works, and $x_0$ is bounded because the rewards and values are. $\square$

**Lemma 3 (every action is tried infinitely often).** Suppose all priors are positive. Let $u$ be a node with $N(u) \to \infty$ as the number of simulations grows. Then every child of $u$ is selected infinitely often.

*Proof.* Write $L(n) = c_1 + \log((n + c_2 + 1)/c_2)$, which is positive and grows like $\log n$. A simulation that passes through $u$ after $u$ has children selects one child of $u$, and $N(u)$ grows by 1 each time. Suppose some child $b$ is selected only finitely often, at most $m$ times in total. Let $I$ be the set of children that are selected infinitely often. It is not empty. Choose $T_0$ such that after $u$ has $T_0$ visits, no child outside $I$ is selected again. When $N(u) = n$ with $n$ large, some child $c \in I$ has $N(c) \ge (n - T_0)/|I|$. Let $t \le n$ be the value of $N(u)$ at the last selection of $c$, so $N(c) \ge (n - T_0)/|I| - 1$ at that time, and $t \ge N(c)$. At that moment the score of $c$ was at most

$$B + P_c\frac{\sqrt{t}}{1 + N(c)}L(t) \le B + \frac{\sqrt{n}\,L(n)}{(n - T_0)/|I|},$$

which tends to $B$ as $n \to \infty$. The score of $b$ at the same moment was at least

$$-B + P_b\frac{\sqrt{t}}{1 + m}c_1 \ge -B + \frac{P_b c_1}{1 + m}\sqrt{\frac{n - T_0}{|I|} - 1},$$

which tends to infinity. So for large $n$ the score of $b$ was larger than that of $c$, and the rule of line L5 could not select $c$, a contradiction. $\square$

**Corollary.** The root has $N(\text{root}) = $ the number of simulations, so by Lemma 3 and induction on the depth, every node of the infinite tree of action sequences is created, and visited infinitely often, as the number of simulations grows.

**Lemma 4 (no overestimate with an exact model).** Suppose that $g$ is the true deterministic transition and reward function of an MDP, with the hidden state equal to the true state, and that $f$ returns the exact optimal values $v(s) = V^*(s)$. Then at every time, for every action $a$ at the root with child $c$ and $N(c) > 0$,

$$x(c) \le Q^*(\text{root}, a),$$

with equality after the first simulation that passes through $c$, if no other simulation has passed through $c$ yet.

*Proof.* By Lemma 1, each return $G_c$ added to $W(c)$ is $\sum_{j=1}^{d-1}\gamma^{j-1}r(u_{1+j}) + \gamma^{d-1}V^*(s(u_d))$, the return of following the actions of the path from the state of $c$ for $d - 1$ steps and then acting optimally. This is the value of some policy from the state $s(c)$, so it is at most $V^*(s(c))$. Hence $W(c)/N(c) \le V^*(s(c))$ and $x(c) = r(c) + \gamma W(c)/N(c) \le r(c) + \gamma V^*(s(c)) = Q^*(\text{root}, a)$, since $(r(c), s(c)) = g(\text{root state}, a)$ is exact. In the first simulation through $c$, $c$ is the leaf, so $G_c = V^*(s(c))$ and the bound holds with equality. $\blacksquare$

**What is not claimed.** The search returns the action with the most visits. Lemma 4 shows that the estimates are pulled below $Q^*$ by simulations that explore poor actions deeper in the tree, so the action with the most visits need not be optimal after finitely many simulations. The tests check on 500 random MDPs with a gap of at least 1 at the root that, with an exact model, exact values and uniform priors, 100 simulations find the optimal action, and the example on the page shows a case where a wrong prior needs hundreds of simulations.
