---
title: The scenario tree LP solves the feedback min-max problem over the whole disturbance polytope, and the receding horizon loop stays feasible
proves: [correctness]
status: full
---

**Setting.** The plant is $x_{k+1} = A x_k + B u_k + w_k$ with $w_k \in W = \mathrm{conv}\{w^1, \dots, w^V\}$. The horizon is $N \ge 1$. The constraints are $x_k \in X = \{x : |x_i| \le \bar x_i\}$ for $0 \le k \le N$, $u_k \in U = \{u : |u_j| \le \bar u_j\}$ for $k < N$, and $x_N \in X_f = \{x : F x \le f\}$. The cost of one trajectory $\tau = (x_0, u_0, \dots, u_{N-1}, x_N)$ is

$$J(\tau) = \sum_{k < N} \left(\|Q x_k\|_1 + \|R u_k\|_1\right) + \|P x_N\|_1.$$

$J$ is a convex function of $\tau$, and the constraint set $\mathcal{C} = \{\tau : x_k \in X, u_k \in U, x_N \in X_f\}$ is convex.

A **causal policy** is a list of maps $\pi_k : W^k \to \mathbb{R}^m$, so that $u_k = \pi_k(w_0, \dots, w_{k-1})$. It is **admissible** from $x_0$ if the trajectory meets $\mathcal{C}$ for every $(w_0, \dots, w_{N-1}) \in W^N$. The feedback min-max value is

$$J^*(x_0) = \inf_{\pi \text{ admissible}} \ \sup_{w \in W^N} J(\tau(x_0, \pi, w)).$$

The **open-loop** value $J^*_{\rm ol}(x_0)$ is the same with each $\pi_k$ a constant.

**The tree.** A node is a sequence $s = (s_0, \dots, s_{k-1})$ of vertex indices with $0 \le k \le N$; its depth is $|s| = k$. The root is the empty sequence. A node of depth $N$ is a leaf. The LP of `min_max_mpc` (feedback form) has a state $x_s$ at each node with $x_{()} = x_0$, a control $u_s$ at each inner node, the constraints

$$x_{s i} = A x_s + B u_s + w^i, \quad x_s \in X, \quad u_s \in U, \quad x_\ell \in X_f \text{ at each leaf } \ell, \tag{1}$$

and the objective $\min t$ with $t \ge J(\tau_\ell)$ for each leaf $\ell$, where $\tau_\ell$ is the trajectory along the path from the root to $\ell$: $\tau_\ell = (x_{()}, u_{()}, x_{\ell_{:1}}, u_{\ell_{:1}}, \dots, x_\ell)$ with $\ell_{:k}$ the prefix of length $k$. In the open-loop form, all inner nodes of the same depth share one control.

## Part 1: the epigraph rows

The code writes $t \ge J(\tau_\ell)$ with nonnegative variables: $s_{p,r} \ge \pm (P \text{ or } Q)_r x_p$ for each node $p$ and row $r$, $\rho_{p,r} \ge \pm R_r u_p$ for each inner node, and $t \ge \sum_{p \text{ on the path to } \ell} \left(\sum_r s_{p,r} + \sum_r \rho_{p,r}\right)$ (line L5).

**Lemma 1.** For fixed $(x_s, u_s)$ that meet (1), the least $t$ that is feasible with some choice of the epigraph variables is $\max_\ell J(\tau_\ell)$.

*Proof.* Each $s_{p,r} \ge |(\cdot)_r x_p|$ and each $\rho_{p,r} \ge |R_r u_p|$, so every feasible $t$ is at least $J(\tau_\ell)$ for each $\ell$. Setting every epigraph variable equal to its absolute value is feasible and gives $t = \max_\ell J(\tau_\ell)$. $\square$

So the optimal value of the LP is

$$J^{\rm LP}(x_0) = \min\left\{\max_\ell J(\tau_\ell) : (x_s, u_s) \text{ meet } (1)\right\}, \tag{2}$$

and the LP is infeasible exactly when (1) has no solution.

## Part 2: the LP value is the min-max value

**Lemma 2 (restriction).** If $\pi$ is admissible from $x_0$, then $u_s = \pi_{|s|}(w^{s_0}, \dots, w^{s_{|s|-1}})$ and the resulting states meet (1), and $\max_\ell J(\tau_\ell) \le \sup_{w \in W^N} J(\tau(x_0, \pi, w))$.

*Proof.* The path to a leaf $\ell$ is the trajectory of $\pi$ under the vertex sequence $(w^{\ell_0}, \dots, w^{\ell_{N-1}}) \in W^N$. It meets $\mathcal{C}$ because $\pi$ is admissible, and its cost is one of the values in the supremum. Two nodes with the same prefix get the same control because $\pi$ is causal. $\square$

**Lemma 3 (interpolation).** Let $(x_s, u_s)$ meet (1). For each $k$ and each $w \in W$ fix weights $\lambda_i(w) \ge 0$ with $\sum_i \lambda_i(w) = 1$ and $\sum_i \lambda_i(w) w^i = w$. For a disturbance sequence $w_0, w_1, \dots$, let $\mu(s) = \prod_{j < |s|} \lambda_{s_j}(w_j)$ and define

$$\pi_k(w_0, \dots, w_{k-1}) = \sum_{|s| = k} \mu(s)\, u_s.$$

Then $\pi$ is causal, and for every $w \in W^N$ its trajectory is $\tau = \sum_\ell \mu(\ell)\, \tau_\ell$, a convex combination of the leaf trajectories. Hence $\pi$ is admissible and $J(\tau) \le \max_\ell J(\tau_\ell)$.

*Proof.* $\pi_k$ uses only $w_0, \dots, w_{k-1}$. The weights $\mu(s)$ over the nodes of one depth are nonnegative and sum to 1, and summing $\mu$ over the children $s i$ of $s$ gives $\mu(s)$. We show $x_k = \sum_{|s| = k} \mu(s) x_s$ by induction. It holds at $k = 0$. If it holds at $k$, then

$$x_{k+1} = A x_k + B u_k + w_k = \sum_{|s| = k} \mu(s) (A x_s + B u_s) + \sum_i \lambda_i(w_k) w^i = \sum_{|s| = k} \sum_i \mu(s) \lambda_i(w_k) (A x_s + B u_s + w^i) = \sum_{|s'| = k + 1} \mu(s') x_{s'},$$

using $\sum_i \lambda_i(w_k) = 1$, $\sum_s \mu(s) = 1$ and (1). Since $\mu(s) = \sum_{\ell \text{ extends } s} \mu(\ell)$, both $x_k$ and $u_k$ equal the sums over the leaves of $\mu(\ell)$ times the entries of $\tau_\ell$, so $\tau = \sum_\ell \mu(\ell) \tau_\ell$. Every $\tau_\ell$ is in the convex set $\mathcal{C}$, so $\tau$ is too. $J$ is convex, so $J(\tau) \le \sum_\ell \mu(\ell) J(\tau_\ell) \le \max_\ell J(\tau_\ell)$. $\square$

**Theorem 1.** The LP is feasible if and only if an admissible causal policy exists, and then $J^{\rm LP}(x_0) = J^*(x_0)$. The infimum in $J^*$ is attained by the interpolated policy of Lemma 3 built from an optimal LP solution, and its first control is the $u_{()}$ that the code returns. The same holds for the open-loop form with $J^*_{\rm ol}$, and $J^*(x_0) \le J^*_{\rm ol}(x_0)$.

*Proof.* Lemma 2 gives $J^{\rm LP} \le \sup_w J$ for every admissible $\pi$, so $J^{\rm LP} \le J^*$. Lemma 3 applied to an optimal LP solution gives an admissible policy with $\sup_w J \le J^{\rm LP}$, so $J^* \le J^{\rm LP}$ and the infimum is attained. At $k = 0$ the sum in Lemma 3 has the one term $u_{()}$. In the open-loop form, the controls at one depth are equal, so the interpolated policy is constant, and Lemma 2 applied to a constant policy gives a point that meets the extra equalities; the same two inequalities follow. An open-loop policy is a causal policy, so $J^* \le J^*_{\rm ol}$. $\square$

## Part 3: the LP solver

`lp_min` splits each free variable into a difference of two nonnegative ones, adds a slack to each inequality, and multiplies a row by $-1$ when its right side is negative. A row that is an inequality with a nonnegative right side starts with its slack in the basis; every other row gets an artificial variable. Phase 1 minimizes the sum of the artificial variables; the LP is feasible exactly when this minimum is 0. An artificial variable that is still basic at level 0 is pivoted out on any nonzero entry outside the artificial columns; if its row has none, the row is a linear combination of the other rows and is dropped. Phase 2 starts from the resulting feasible basis with the true cost. Both phases use Bland's rule (the entering column is the first one with a negative reduced cost, and ties in the ratio test go to the smallest basic index), which ends after finitely many pivots (Bland 1977). Phase 2 ends at an optimal basis or finds a column with a negative reduced cost and no positive entry, which is a ray along which the cost decreases without bound. In the MPC LP the cost $t$ is bounded below by $0$, so this case does not happen there. With rational data and `tol = 0` all operations are exact; `_pivot` turns an integer pivot into a `Fraction` so that no float enters.

## Part 4: the receding horizon loop

Let the terminal set be robustly positively invariant under a local law $u = K x$: $X_f \subseteq X$, and for every $x \in X_f$, $K x \in U$ and $(A + B K) x + w \in X_f$ for all $w \in W$.

**Theorem 2.** If the feedback LP is feasible from $x_0$, then for every realized disturbance sequence in $W$ the LP of line L8 is feasible at every sample, and the closed loop meets $x_k \in X$ and $u_k \in U$ for all $k$.

*Proof.* Let the LP be feasible from $x$, with the interpolated optimal policy $\pi$ of Lemma 3, and let $w_0 \in W$ be the realized disturbance, so that the next state is $x^+ = A x + B \pi_0 + w_0$. Define a policy $\pi^+$ from $x^+$ by $\pi^+_k(w_1, \dots, w_k) = \pi_{k+1}(w_0, w_1, \dots, w_k)$ for $k < N - 1$ and $\pi^+_{N-1} = K x_N$, where $x_N$ is the state reached at depth $N$ of $\pi$. This is causal. For every $(w_1, \dots, w_N) \in W^N$, the first $N - 1$ steps follow $\pi$ under $(w_0, w_1, \dots, w_{N-1})$, so they meet $X$ and $U$ and reach $x_N \in X_f$; the last step uses $K x_N \in U$ and reaches $(A + B K) x_N + w_N \in X_f \subseteq X$. So $\pi^+$ is admissible from $x^+$, and by Theorem 1 the LP from $x^+$ is feasible. By induction every LP in the loop is feasible. The applied input is $u_{()} \in U$, and each state of the loop is the root of a feasible LP, so it is in $X$. $\square$

The open-loop form has no such argument, because the shifted policy needs the feedback $K x_N$, which is not a constant. In the example of the page, the open-loop problem with $N = 3$ is infeasible from every state while the feedback problem is feasible from $|x_0| \le 853/432$.

## Part 5: what the code computes

- **Line L1** lists the $1 + V + \dots + V^N$ nodes.
- **Line L2** makes one control per inner node (feedback) or per depth (open loop), and one state per node other than the root.
- **Line L3** writes the equalities of (1).
- **Line L4** writes the box rows of $X$ and $U$ and the rows of $X_f$ at the leaves, and returns `None` when the given $x_0$ breaks a constraint on the root.
- **Line L5** writes the epigraph rows of Part 1.
- **Lines L6 and L7** solve the LP and return its value $J^*(x_0)$ (Theorem 1), the first control and the tree.
- **Line L8** is the loop of Theorem 2.
