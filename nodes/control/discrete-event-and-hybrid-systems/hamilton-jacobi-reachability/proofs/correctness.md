---
title: The Lax-Friedrichs scheme for the reachability equation is monotone, stable and consistent
proves: [correctness, termination]
status: partial
---

**Setting.** The system is $x' = f(x, u, d)$ with $u \in U$ and $d \in D$ compact, and $f$ bounded and Lipschitz in $x$. The target is $\{x : g(x) \le 0\}$ with $g$ Lipschitz. In time to go $\tau \ge 0$ the value function solves

$$V_\tau = \min(0, H(x, \nabla V)), \qquad V(x, 0) = g(x), \qquad H(x, p) = \min_{u \in U} \max_{d \in D} p \cdot f(x, u, d).$$

Write $G = -H$, so that $V_\tau = -\max(0, G(x, \nabla V))$. The grid has steps $\Delta x_i$ on the axes $i = 1, \ldots, n$. Lines L5 to L7 compute, at each node $j$,

$$V_j^{new} = V_j - \Delta\tau \max\Big(0, \hat G_j\Big), \qquad \hat G_j = G\Big(x_j, \frac{p^+ + p^-}{2}\Big) - \sum_i \alpha_i \frac{p_i^+ - p_i^-}{2},$$

with $p_i^\pm$ the one-sided differences of $V$ along axis $i$. Assume $\alpha_i \ge \sup |\partial G / \partial p_i|$ (or, if $G$ is only Lipschitz in $p$, that $|G(x, p) - G(x, q)| \le \sum_i \alpha_i |p_i - q_i|$), and the CFL condition $\Delta\tau \sum_i \alpha_i / \Delta x_i \le 1$ of line L2.

This file proves the properties of the scheme at nodes away from the edge of the grid. The convergence to the viscosity solution and the meaning of its zero sublevel set are theorems of the literature, quoted at the end; this is why the status is partial.

**Lemma 1 (monotone).** At an inner node, $V_j^{new}$ is a nondecreasing function of $V_j$ and of each neighbor value $V_{j \pm e_i}$.

*Proof.* Write $\hat G_j$ as a function of the values. The point $(p^+ + p^-)/2$ has entries $(V_{j + e_i} - V_{j - e_i}) / (2 \Delta x_i)$, which do not depend on $V_j$, and $p_i^+ - p_i^- = (V_{j + e_i} - 2V_j + V_{j - e_i}) / \Delta x_i$. Raise $V_{j + e_i}$ by $\epsilon > 0$. The first term of $\hat G_j$ changes by at most $\alpha_i \epsilon / (2\Delta x_i)$ by the Lipschitz bound, and the second term drops by exactly $\alpha_i \epsilon / (2\Delta x_i)$. So $\hat G_j$ does not increase. The same holds for $V_{j - e_i}$. Since $\max(0, \cdot)$ is nondecreasing, $-\Delta\tau \max(0, \hat G_j)$ does not decrease. Now raise $V_j$ by $\epsilon$. Only the second term of $\hat G_j$ changes, and it rises by $\epsilon \sum_i \alpha_i / \Delta x_i$. As $\max(0, \cdot)$ is 1-Lipschitz, $V_j^{new}$ changes by at least $\epsilon - \Delta\tau \epsilon \sum_i \alpha_i / \Delta x_i \ge 0$ by the CFL condition. $\blacksquare$

**Lemma 2 (stable).** The update commutes with adding a constant: if $W = V + c$, then $W^{new} = V^{new} + c$. With Lemma 1, this gives $\max_j |V_j^{new} - W_j^{new}| \le \max_j |V_j - W_j|$ for any two grid functions, at inner nodes whose neighbors are inner nodes or obey the same bound.

*Proof.* The differences $p^\pm$ do not change when a constant is added, so $\hat G_j$ does not change. For the bound, let $c = \max |V - W|$. Then $W - c \le V \le W + c$, and Lemma 1 with the first part gives $W^{new} - c \le V^{new} \le W^{new} + c$. $\blacksquare$

**Lemma 3 (consistent).** If $V$ is the restriction of a smooth function $\phi$, then $\hat G_j = G(x_j, \nabla\phi(x_j)) + O(\max_i \Delta x_i)$, so the update is a consistent first order scheme for $V_\tau = -\max(0, G(x, \nabla V))$.

*Proof.* $(p^+ + p^-)/2$ is the central difference, equal to $\nabla \phi(x_j) + O(\Delta x^2)$, and $G$ is Lipschitz in $p$. $p_i^+ - p_i^- = \Delta x_i \, \partial_{ii}\phi(x_j) + O(\Delta x_i^2)$, so the second term is $O(\Delta x)$. $\blacksquare$

**Lemma 4 (the tube grows).** $V_j^{new} \le V_j$ at every node, so the computed set $\{V \le 0\}$ never shrinks as $\tau$ grows.

*Proof.* $\Delta\tau \max(0, \hat G_j) \ge 0$. $\blacksquare$

**Termination.** Line L2 sets $K = \lceil T \sum_i \alpha_i / \Delta x_i \rceil$ steps of length $\Delta\tau = T / K$, which meets the CFL condition. Each step visits each of the $M = \prod_i k_i$ nodes once and does $O(n)$ work plus one evaluation of $G$. So the program stops after $O(K n M)$ operations and evaluations.

**Results quoted from the literature.**

- Crandall and Lions (1984) prove that a monotone and consistent scheme of the form $u^{new} = u - \Delta t \, \hat H(p^+, p^-)$ for $u_t + H(Du) = 0$ converges to the viscosity solution, with an error of order $\sqrt{\Delta x}$ in the maximum norm when the initial data are Lipschitz and $\Delta\tau / \Delta x$ is fixed. Lemmas 1 to 3 are the hypotheses of this kind of result. The implementation also covers Hamiltonians that depend on $x$; the tests check such a case against its exact solution.
- Mitchell, Bayen and Tomlin (2005) prove that the zero sublevel set of the viscosity solution of $V_\tau = \min(0, H(x, \nabla V))$, $V(\cdot, 0) = g$, is the backward reachable tube of horizon $T$: the states from which the target can be reached within time $T$, when the other player may react to the current input (a nonanticipative strategy). They state it with the roles of the players swapped; swapping the roles swaps $\min$ and $\max$ in $H$.

**At the edge of the grid.** The missing neighbor is filled by linear extrapolation, which makes $p^+ = p^-$ there. This update is not monotone. An inner node at distance $d$ nodes from the edge does not depend on the edge values during the first $d$ steps, because each step looks one node to each side. So Lemmas 1 and 2 hold for the nodes that are more than $K$ nodes from the edge. A test of the implementation checks the order of two solutions only at these nodes, and it fails near the edge for rough initial data.

**What is not proved.** The computed set $\{V_j \le 0\}$ is an approximation. It is not proved to contain, or to be contained in, the true tube on a given grid. In the tests, it lies inside the true tube or on its boundary.
