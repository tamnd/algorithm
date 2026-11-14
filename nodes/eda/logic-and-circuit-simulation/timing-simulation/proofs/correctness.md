---
title: The node equations of backward Euler have unique solutions, a triangular order gives backward Euler in one sweep, and one Newton step is accurate to third order in h
proves: [correctness]
status: partial
---

**Setting.** Node $i$ has capacitance $C_i > 0$ and current $I_i(v)$, the sum over the transistors whose channel touches $i$ of the current flowing into $i$. The transistors follow the square-law model of the page with parameter $k > 0$ and threshold $V_T$. Backward Euler with step $h$ asks for $v^{n+1}$ with $G_i(v^{n+1}) = 0$ for all $i$, where $G_i(v) = C_i (v_i - v_i^n)/h - I_i(v)$. For fixed values of the other nodes, write $g(x) = G_i(\ldots, x, \ldots)$ for the node equation of $i$. Lines L1 to L11 refer to the pseudocode of the page.

**Lemma 1 (the device).** For one transistor, the current into a channel terminal $i$ is a continuously differentiable function of the terminal voltages. Its derivative in $v_i$ is at most 0, and it is Lipschitz in $v_i$ with constant $k$, as long as the gate of the transistor is not node $i$.

*Proof.* Take an n transistor; the p case is the same with all voltages negated. Let $V_{ov} = v_g - v_s - V_T$ and $V_{DS} = v_d - v_s \ge 0$, where the source $s$ is the lower channel terminal. The current from drain to source is $f = 0$ for $V_{ov} \le 0$, $f = k(V_{ov} V_{DS} - V_{DS}^2/2)$ for $0 \le V_{DS} \le V_{ov}$ and $f = k V_{ov}^2/2$ for $V_{DS} \ge V_{ov} \ge 0$. On the boundaries the pieces and their first derivatives agree: at $V_{DS} = V_{ov}$ both give $k V_{ov}^2/2$, $\partial f/\partial V_{ov} = k V_{ov}$ and $\partial f/\partial V_{DS} = 0$; at $V_{ov} = 0$ all are 0. Write $g_m = \partial f / \partial V_{ov} \ge 0$ and $g_{ds} = \partial f / \partial V_{DS} \ge 0$. If $i$ is the drain, the current into $i$ is $-f$ and its derivative in $v_i$ is $-g_{ds} \le 0$. If $i$ is the source, the current into $i$ is $f$ and its derivative is $-(g_m + g_{ds}) \le 0$. At $v_d = v_s$ the two roles meet, and both derivatives equal $-k \max(V_{ov}, 0)$, so the derivative is continuous there. In each region, $g_{ds}$ and $g_m + g_{ds}$ are 0, $k V_{ov}$ or $k(V_{ov} - V_{DS})$, and as functions of $v_i$ alone they are piecewise linear with slopes in $\{0, k, -k\}$ when $i$ is not the gate. A continuous piecewise linear function with slopes of size at most $k$ is Lipschitz with constant $k$. $\square$

**Theorem 1 (one solution per node).** If no transistor at node $i$ has its gate on $i$, then for all values of the other nodes, $g'(x) \ge C_i/h$, and $g$ has exactly one root. The denominator $C_i - hD$ of line L7 is at least $C_i$.

*Proof.* $g'(x) = C_i/h - \partial I_i / \partial v_i$, and $\partial I_i / \partial v_i = D \le 0$ by Lemma 1, summed over the transistors at $i$. So $g$ is continuous and strictly increasing with slope at least $C_i/h$. It tends to $-\infty$ and $+\infty$ at the two ends, so it has exactly one root. $C_i - hD = h g'(x) \ge C_i$. $\square$

**Theorem 2 (triangular order).** Suppose that, in the order of line L4, each $I_i$ depends only on $v_i$, on the inputs and on nodes earlier in the order, and that Theorem 1 applies to every node. Then the backward Euler system has exactly one solution $v^{n+1}$, and the sweep that solves each node equation exactly, with the newest values of the earlier nodes, returns it.

*Proof.* Induction along the order. Node 1 depends only on itself and the inputs at $t^{n+1}$, so its equation, alone, has one root, and every solution of the system must take this value. Suppose nodes $1, \ldots, i-1$ have the unique values that every solution must take, and that the sweep has computed them. Then the equation of node $i$ involves only these values, the inputs and $v_i$, so it has one root by Theorem 1, every solution takes it, and the sweep computes it. $\square$

**Theorem 3 (one Newton step).** Let Theorem 1 apply to node $i$, fix the other voltages, let $x_0 = v_i^n$, let $x^*$ be the root of $g$, and let $x_1 = x_0 - g(x_0)/g'(x_0)$ be the result of line L7. Let $I = I_i$ at $x_0$ and let $L$ be the sum of $k$ over the transistors at node $i$. Then
$$|x_0 - x^*| \le \frac{h |I|}{C_i}, \qquad |x_1 - x^*| \le \frac{L h^3 I^2}{2 C_i^3}.$$

*Proof.* $g(x_0) = -I$, and $g' \ge m = C_i / h$, so $|g(x_0)| = |g(x_0) - g(x^*)| \ge m |x_0 - x^*|$, which is the first bound. By Lemma 1, $g' = C_i/h - \partial I_i/\partial v_i$ is Lipschitz with constant $L$. Then
$$x_1 - x^* = \frac{g'(x_0)(x_0 - x^*) - (g(x_0) - g(x^*))}{g'(x_0)} = \frac{1}{g'(x_0)} \int_{x^*}^{x_0} \left(g'(x_0) - g'(\xi)\right) d\xi,$$
and the integrand is at most $L|x_0 - \xi|$ in size, so the integral is at most $L |x_0 - x^*|^2 / 2$. Dividing by $g'(x_0) \ge m$ and using the first bound gives the second. $\square$

For the example of the page, $L = 400\ \mu\mathrm{A/V^2}$, $C_i = 10$ fF, $h = 10^{-3}$ ns and $|I| \le 169\ \mu$A give a bound of about $5.7\ \mu$V per node and step.

**What is not proved here.** Theorem 3 bounds the gap between one Newton step and the exact node solve in one step, with the other voltages fixed. Adding these gaps over the steps, and showing that the backward Euler map does not amplify them, would show that one Newton step per node keeps the first-order accuracy of backward Euler on a triangular circuit; that argument is not given here, and the tests measure it instead (a gap of 1.2 mV to full backward Euler at $h = 2$ ps, and error ratios near 2 when $h$ halves). For circuits with two-way coupling, the single Gauss-Seidel sweep is not exact even with exact node solves, and its error depends on the circuit; Newton and Sangiovanni-Vincentelli (1984) analyze the convergence of the repeated sweep, which this page cites and does not prove.
