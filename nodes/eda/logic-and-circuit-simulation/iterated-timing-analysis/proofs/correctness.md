---
title: Iterated timing analysis converges to the backward Euler solution when the node Jacobian is diagonally dominant
proves: [correctness]
status: full
---

We use the notation of the page. Fix one time point $t$ with step $h$ and previous voltages $v^n$. The unknown node voltages $v \in \mathbb{R}^N$ must satisfy the backward Euler node equations $F(v) = 0$, where $F_i(v)$ is the sum of the currents that leave node $i$: the capacitor currents $C(\Delta v_i - \Delta v_j)/h$ with $\Delta v = v - v^n$, and the resistive currents of resistors, controlled sources and transistor channels. The fixed nodes (ground, supplies, inputs) have known values at $t$. The Jacobian is

$$J(v) = \frac{1}{h} C + G(v),$$

where $C$ is the nodal capacitance matrix and $G(v)$ the Jacobian of the resistive currents. We assume $F$ is continuously differentiable; the level-1 MOSFET model is, since its current and first derivatives agree at the boundaries of its three regions. Let $v^\ast$ be a solution of $F(v) = 0$.

A *node update* of node $i$ changes only $v_i$. An *exact node update* sets $v_i$ to a root of $F_i$ with the other voltages fixed. A *Newton node update*, line L8 of the page, sets $v_i \leftarrow v_i - F_i(v)/J_{ii}(v)$. A *sweep* updates every unknown node once, in a fixed order, each with the newest values of the others: this is nonlinear [Gauss-Seidel](/gauss-seidel-method/) iteration. We use the maximum norm $\|e\| = \max_i |e_i|$.

**Dominance assumption.** On a convex set $\Omega$ that contains $v^\ast$ and the iterates, $J_{ii}(v) > 0$ and

$$\sum_{j \ne i} |J_{ij}(v)| \le \rho\, J_{ii}(v) \quad \text{for all } i \text{ and all } v \in \Omega,$$

for a constant $\rho < 1$, the sum taken over unknown nodes $j$. That is, $J$ is strictly [diagonally dominant](/diagonally-dominant-matrix/) by rows, uniformly on $\Omega$.

**Lemma 1 (a Newton node update is exact on a linear node equation).** If $F_i$ is affine in $v_i$, one Newton node update sets $F_i = 0$.

*Proof.* If $F_i(v) = a + J_{ii} v_i$ with $a$ and $J_{ii}$ independent of $v_i$, then $v_i - F_i(v)/J_{ii} = -a/J_{ii}$, the root. $\square$

So on a linear circuit (resistors, capacitors, linear controlled sources), the iteration of the page is exactly linear Gauss-Seidel on $J v = b$.

**Theorem 1 (contraction of a sweep).** Under the dominance assumption, a sweep of exact node updates maps $v$ to $v'$ with

$$\|v' - v^\ast\| \le \rho\, \|v - v^\ast\|.$$

*Proof.* Let node $i$ be updated when the current vector is $w$, which has the new values $v'_j$ for nodes earlier in the order and the old values $v_j$ for the others, and let $w'$ be $w$ with $w_i$ replaced by $v'_i$. Then $F_i(w') = 0 = F_i(v^\ast)$. Along the segment from $v^\ast$ to $w'$, which lies in $\Omega$,

$$0 = F_i(w') - F_i(v^\ast) = \sum_j \bar J_{ij} (w'_j - v^\ast_j), \qquad \bar J_{ij} = \int_0^1 J_{ij}\big(v^\ast + s(w' - v^\ast)\big)\, ds.$$

Integration keeps the dominance: $\sum_{j \ne i} |\bar J_{ij}| \le \int_0^1 \sum_{j \ne i} |J_{ij}|\, ds \le \rho \int_0^1 J_{ii}\, ds = \rho\, \bar J_{ii}$, and $\bar J_{ii} > 0$. So

$$|v'_i - v^\ast_i| \le \frac{1}{\bar J_{ii}} \sum_{j \ne i} |\bar J_{ij}|\, |w_j - v^\ast_j| \le \rho \max_{j \ne i} |w_j - v^\ast_j|.$$

By induction on the order, every new value satisfies $|v'_j - v^\ast_j| \le \rho \|v - v^\ast\| \le \|v - v^\ast\|$, so every entry of $w$ is within $\|v - v^\ast\|$ of $v^\ast$, and the bound for node $i$ is $\rho \|v - v^\ast\|$. $\square$

With $\rho < 1$ the sweeps converge to $v^\ast$, and $v^\ast$ is the only solution in $\Omega$: a second solution would be a fixed point of the sweep, and the contraction gives distance 0. For a linear circuit Theorem 1 is the classical convergence of Gauss-Seidel for a strictly diagonally dominant matrix.

**Corollary 1 (stopping test).** If a sweep moves no node by more than $\tau$, that is $\|v' - v\| \le \tau$, then $\|v' - v^\ast\| \le \frac{\rho}{1 - \rho} \tau$.

*Proof.* $\|v - v^\ast\| \le \|v - v'\| + \|v' - v^\ast\| \le \tau + \rho \|v - v^\ast\|$, so $\|v - v^\ast\| \le \tau/(1 - \rho)$ and $\|v' - v^\ast\| \le \rho \tau/(1 - \rho)$. $\square$

**Theorem 2 (one Newton step per node converges locally).** Under the dominance assumption at $v^\ast$ (that is, for $J(v^\ast)$), sweeps of Newton node updates converge to $v^\ast$ from every start close enough to $v^\ast$, at a rate of at most $\rho$ per sweep in the limit.

*Proof.* Let $\Phi$ be the sweep map. Update $i$ computes $\phi_i(w) = w_i - F_i(w)/J_{ii}(w)$. Since $F_i(v^\ast) = 0$ and $1/J_{ii}$ is continuous with $J_{ii}(v^\ast) > 0$,

$$\phi_i(w) - v^\ast_i = (w_i - v^\ast_i) - \frac{1}{J_{ii}(w)}\big(F_i(w) - F_i(v^\ast)\big) = -\frac{1}{J_{ii}(v^\ast)} \sum_{j \ne i} J_{ij}(v^\ast) (w_j - v^\ast_j) + o(\|w - v^\ast\|).$$

So $\Phi$ is differentiable at its fixed point $v^\ast$, and $\Phi'(v^\ast)$ is the sweep map of linear Gauss-Seidel on $J(v^\ast)$, the matrix $-(D + L)^{-1} U$ for the splitting $J(v^\ast) = D + L + U$. Theorem 1, applied to the linear map $v \mapsto J(v^\ast) v$ (dominance holds everywhere for a constant matrix), gives $\|\Phi'(v^\ast) e\| \le \rho \|e\|$ for every $e$, so the spectral radius of $\Phi'(v^\ast)$ is at most $\rho < 1$. By Ostrowski's theorem on points of attraction (Ortega and Rheinboldt, Chapter 10), $v^\ast$ attracts all starts in a neighbourhood, with asymptotic rate at most $\rho$. $\square$

**Theorem 3 (small steps give dominance).** Suppose every unknown node $i$ has a capacitance $c_i > 0$ to ground or to a fixed node, let $\kappa_i \ge 0$ be the total capacitance from $i$ to other unknown nodes, so that $C_{ii} \ge c_i + \kappa_i$ and $\sum_{j \ne i} |C_{ij}| = \kappa_i$, and suppose that on $\Omega$, $\sum_{j \ne i} |G_{ij}(v)| \le a_i$ and $G_{ii}(v) \ge -b_i$ with $a_i, b_i \ge 0$. Then for $h > 0$ with $h(a_i + b_i) < c_i$ for all $i$, the dominance assumption holds with

$$\rho = \max_i \frac{\kappa_i + h a_i}{C_{ii} - h b_i} < 1,$$

and $\rho \to \max_i \kappa_i / C_{ii}$ as $h \to 0$.

*Proof.* In row $i$ of $hJ$, the diagonal is $C_{ii} + h G_{ii} \ge C_{ii} - h b_i > 0$ and the off-diagonal sum is at most $\kappa_i + h a_i$. The ratio is below 1 exactly when $\kappa_i + h a_i < C_{ii} - h b_i$, which follows from $C_{ii} \ge c_i + \kappa_i$ and $h(a_i + b_i) < c_i$. $\square$

For a node at the drain or source of a MOSFET, the channel current contributes $\partial I/\partial v_i \ge 0$ to $G_{ii}$ (the output conductance, plus the transconductance at the source), so $b_i = 0$ unless a controlled source or a transistor gate on the node itself makes $G_{ii}$ negative. The off-diagonal terms $a_i$ include the transconductances of the transistors whose gates are driven by other nodes. So the bound says: ITA converges when the time step is small against $c_i / a_i$, the time constant of the grounded capacitance with the transconductances that couple the node to its neighbours. This is why relaxation-based simulators couple the time step and the relaxation.

**Theorem 4 (the event-driven loop is Gauss-Seidel in a data-driven order).** Every node update in lines L5 to L9 is a Newton node update with the newest voltages. When the queue becomes empty, the last update of every node moved it by at most $\tau$, and every later update of a node it reads also moved that node by at most $\tau$.

*Proof.* Line L7 evaluates $F_i$ and $J_{ii}$ at the current vector, which holds the newest value of every node, and line L8 is the Newton node update. A node $j$ that reads $v_i$, which means that $F_j$ depends on $v_i$, is in the fanout of $i$, so any update of $i$ by more than $\tau$ puts $j$ back in the queue (line L9), and $i$ is in its own fanout. If the queue is empty, no update after the last update of $j$ was larger than $\tau$ on any node that $j$ reads, and the last update of $j$ was not larger than $\tau$ either, otherwise $j$ would be in the queue. $\square$

Theorem 4 is weaker than Corollary 1: many small updates of a neighbour, each below $\tau$, can add up, and nodes that did not move by more than $\tau$ in the previous step are not evaluated at all (latency). The distance between the result and the backward Euler solution is not bounded here; the tests measure it against a full Newton solve, and it grows linearly with $\tau$ (about $3 \tau$ on the four-stage inverter chain).

Together, Lemma 1 and Theorems 1 to 3 show that, for steps small enough to make the node Jacobian dominant, iterating the node updates to convergence computes the backward Euler solution of [transient circuit analysis](/transient-circuit-analysis/) at each time point; Theorem 4 shows that the event-driven loop performs only such updates and stops only when all of them are below $\tau$.
