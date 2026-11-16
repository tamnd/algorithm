---
title: TOPP-RA returns an admissible parameterization of the discretized path if and only if one exists
proves: [correctness]
status: full
---

We use the notation of the page. The grid is $s_0 < s_1 < \dots < s_N$ with steps $\Delta_i = s_{i+1} - s_i > 0$. At grid point $i$ the admissible set $\Omega_i$ is the set of pairs $(u, x)$ with $x \ge 0$ and $\ell \le a u + b x + c \le h$ for every row $(a, b, c, \ell, h)$ at $s_i$. It is an intersection of finitely many closed half-planes, so it is a closed convex polygon (possibly unbounded or empty). The end states $x_{\text{start}}$ and $x_{\text{end}}$ are given and are not negative.

**Definition.** An admissible parameterization is a sequence $x_0, \dots, x_N$ and $u_0, \dots, u_{N-1}$ with $x_0 = x_{\text{start}}$, $x_N = x_{\text{end}}$, $(u_i, x_i) \in \Omega_i$ and $x_{i+1} = x_i + 2\Delta_i u_i$ for $i < N$.

The controllable sets are defined backward: $K_N = \{x_{\text{end}}\}$, and for $i < N$

$$K_i = \{x : \text{there is } u \text{ with } (u, x) \in \Omega_i \text{ and } x + 2\Delta_i u \in K_{i+1}\}.$$

Line L1 sets $K_N$, and line L3 computes $K_i$ from $K_{i+1}$.

## The sets are intervals and line L3 computes them exactly

**Lemma 1.** Each $K_i$ is empty or a closed interval $[\ell_i, h_i]$ with $0 \le \ell_i$. If $K_{i+1}$ is a closed interval, `one_step_set` returns exactly $K_i$, or "empty" when $K_i$ is empty.

*Proof.* By backward induction. $K_N = [x_{\text{end}}, x_{\text{end}}]$. Let $K_{i+1} = [\ell, h]$. The set

$$P = \Omega_i \cap \{(u, x) : \ell \le x + 2\Delta_i u \le h\}$$

is an intersection of finitely many closed half-planes $\alpha u + \beta x \le \gamma$, and $K_i$ is its projection on the $x$ axis. For a fixed $x$, the half-planes with $\alpha > 0$ give upper bounds $u \le (\gamma - \beta x)/\alpha$, those with $\alpha < 0$ give lower bounds $u \ge (\gamma - \beta x)/\alpha$, and those with $\alpha = 0$ do not involve $u$ and say $\beta x \le \gamma$. A $u$ exists if and only if every row with $\alpha = 0$ holds and every lower bound is at most every upper bound. For a pair with $\alpha_i > 0 > \alpha_j$, multiply the first inequality by $-\alpha_j > 0$ and the second by $\alpha_i > 0$; the condition "lower bound $\le$ upper bound" becomes

$$(\alpha_i \beta_j - \alpha_j \beta_i)\, x \le \alpha_i \gamma_j - \alpha_j \gamma_i,$$

which is the row that `_x_interval` forms (Fourier-Motzkin elimination of $u$). The two rows from $K_{i+1}$ have $\alpha = 2\Delta_i > 0$ and $\alpha = -2\Delta_i < 0$, so both kinds of bound are always present. So $x \in K_i$ if and only if $x$ meets finitely many rows of the form $c x \le d$. Their solution set is a closed interval or empty, and `_x_interval` intersects them: a row with $c > 0$ lowers the upper end, a row with $c < 0$ raises the lower end, and a row with $c = 0$ and $d < 0$ makes the set empty. The row $x \ge 0$ is always present, so $\ell_i \ge 0$. $\square$

**Lemma 2.** $x \in K_i$ if and only if there are $u_i, \dots, u_{N-1}$ such that the states $x_i = x$, $x_{j+1} = x_j + 2\Delta_j u_j$ satisfy $(u_j, x_j) \in \Omega_j$ for $i \le j < N$ and $x_N = x_{\text{end}}$.

*Proof.* By backward induction on $i$. For $i = N$ both sides say $x = x_{\text{end}}$. For $i < N$: if $x \in K_i$, take $u_i$ from the definition; then $x_{i+1} \in K_{i+1}$ and the induction hypothesis gives the rest of the controls. Conversely, if such controls exist, then $(u_i, x) \in \Omega_i$ and $x_{i+1}$ has a valid tail, so $x_{i+1} \in K_{i+1}$ by the induction hypothesis and $x \in K_i$ by the definition. $\square$

## The algorithm reports infeasible only when nothing is admissible

**Lemma 3.** If the algorithm returns at line L4 or line L5, no admissible parameterization exists.

*Proof.* An admissible parameterization gives, by Lemma 2 with $i = 0$, that $x_{\text{start}} \in K_0$. If some $K_i$ is empty, then $K_{i-1}, \dots, K_0$ are all empty by the definition, so $K_0$ is empty and the return at line L4 is correct. If $x_{\text{start}} \notin K_0$, the return at line L5 is correct. (The check of $x_{\text{end}}$ against the rows at $s_N$ before line L1 is the same argument for the last point.) $\square$

## The forward pass stays in the controllable sets

**Lemma 4.** If the algorithm passes line L5, then for every $i$ the control $u_i$ of line L8 exists, $(u_i, x_i) \in \Omega_i$, and $x_{i+1} \in K_{i+1}$.

*Proof.* We show $x_i \in K_i$ for all $i$ by induction. $x_0 = x_{\text{start}} \in K_0$ by line L5. If $x_i \in K_i$, the set

$$U_i = \{u : (u, x_i) \in \Omega_i,\ x_i + 2\Delta_i u \in K_{i+1}\}$$

is not empty by the definition of $K_i$. It is an intersection of closed intervals of $u$ (each row with $a \ne 0$ gives one, rows with $a = 0$ hold because $x_i$ is the $x$ of a point of $\Omega_i$), and it is bounded above by $(h_{i+1} - x_i)/(2\Delta_i)$. So it has a largest element, which `greedy_control` returns: it intersects the same intervals and returns the upper end. Then $(u_i, x_i) \in \Omega_i$ and $x_{i+1} = x_i + 2\Delta_i u_i \in K_{i+1}$. The clamp at $0$ in line L9 does nothing, because $K_{i+1} \subseteq [0, \infty)$ by Lemma 1. $\square$

## Theorem

**Theorem.** The algorithm returns an admissible parameterization of the discretized problem if one exists, and returns "infeasible" otherwise.

*Proof.* If no admissible parameterization exists, the algorithm cannot return a profile: by Lemma 4 any profile it returns is admissible, since $x_N \in K_N = \{x_{\text{end}}\}$. So it returns at line L4 or line L5. If an admissible parameterization exists, Lemma 3 shows that the algorithm does not return at lines L4 or L5, and Lemma 4 shows that the forward pass builds a profile with $(u_i, x_i) \in \Omega_i$ for all $i < N$ and $x_N = x_{\text{end}}$, which is admissible. $\blacksquare$

## What this proof does not show

The theorem is about feasibility and admissibility. It does not say that the greedy forward pass gives the least traversal time of the discretized problem. Pham and Pham (2018) prove optimality separately (their Theorem 2), when the path has no zero-inertia points and the step is below a threshold, and they bound the excess time by $O(\Delta)$ when zero-inertia points are present (their Theorem 3). The tests compare the result with a brute force over a lattice of states with a tolerance, not with equality, for this reason.

In floating point, the bounds of the sets have rounding errors. The code accepts a state that lies outside a set by at most a relative tolerance of $10^{-12}$, and the constraint violation of the returned profile is of the same order.
