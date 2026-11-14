---
title: Devgan's metric is an upper bound on the noise of an RC tree driven by aggressors of bounded slope
proves: [correctness]
status: full
---

**Model.** The victim net is a tree with nodes $0, 1, \ldots, n-1$ and $p(k) < k$ for $k \ge 1$. Node 0 is joined to ground by the holding resistance $r_0 > 0$ of the quiet driver, and node $k \ge 1$ is joined to $p(k)$ by a wire resistance $r_k > 0$. Node $k$ has a capacitance $c_k \ge 0$ to ground and a coupling capacitance $C_{k,a} \ge 0$ to aggressor $a$, with $\bar c_k = c_k + \sum_a C_{k,a} > 0$. Each aggressor is an ideal voltage source $u_a(t)$, continuous and piecewise continuously differentiable, constant for $t \le 0$, with $|u_a'(t)| \le s_a$. At $t = 0$ all victim voltages are 0.

Kirchhoff's current law at node $k$ gives $c_k v_k' + \sum_a C_{k,a}(v_k' - u_a') + (Gv)_k = 0$, that is

$$ C v'(t) + G v(t) = B u'(t), \qquad v(0) = 0, $$

with $C = \operatorname{diag}(\bar c_k)$, $B_{k,a} = C_{k,a}$, and $G$ the conductance matrix of the tree: $G_{kk}$ is the sum of the conductances at $k$ (with $1/r_0$ at node 0), and $G_{kj} = -1/r_j$ or $-1/r_k$ when $j$ and $k$ are joined by a wire. Write $I_k = \sum_a C_{k,a} s_a$ and $R_{ik}$ for the total resistance of the part that the paths from ground to $i$ and to $k$ share.

**Lemma 1 (the resistance matrix).** $G$ is symmetric positive definite and $G^{-1} = (R_{ik})$.

*Proof.* For any $x$, $x^T G x = x_0^2 / r_0 + \sum_{k \ge 1} (x_k - x_{p(k)})^2 / r_k$. This is 0 only if $x_0 = 0$ and $x_k = x_{p(k)}$ for all $k$, so only if $x = 0$. For the inverse, inject a unit current at node $k$ with all other injections 0. By current conservation the whole unit flows from $k$ to ground along the path from $k$, and no current flows elsewhere. The voltage at $i$ is the drop from $i$ to ground, which is the sum of $r_j$ over the edges of the path of $i$ that carry current, that is $R_{ik}$. So column $k$ of $G^{-1}$ is $(R_{ik})_i$. The [RC tree](/rc-tree/) page gives the same fact. $\square$

**Lemma 2 (positivity of the propagator).** Let $M = C^{-1} G$. For every $t \ge 0$, all entries of $e^{-Mt}$ are nonnegative, and $e^{-Mt} \to 0$ as $t \to \infty$.

*Proof.* The off-diagonal entries of $-M$ are $-G_{kj} / \bar c_k \ge 0$. Let $\mu = \max_k M_{kk}$ and $N = \mu I - M$, a matrix with nonnegative entries. Since $\mu I$ commutes with $N$, $e^{-Mt} = e^{-\mu t} e^{N t} = e^{-\mu t} \sum_{m \ge 0} (N t)^m / m!$, a sum of nonnegative matrices. Next, $M = C^{-1/2} S C^{1/2}$ with $S = C^{-1/2} G C^{-1/2}$ symmetric positive definite by Lemma 1. So $M$ has positive real eigenvalues $\lambda_1, \ldots, \lambda_n$ and is diagonalizable, and $e^{-Mt} = C^{-1/2} Q \operatorname{diag}(e^{-\lambda_m t}) Q^T C^{1/2} \to 0$. $\square$

**Lemma 3.** $\int_0^\infty e^{-M\sigma}\, d\sigma = M^{-1}$.

*Proof.* $\frac{d}{d\sigma}\left(-M^{-1} e^{-M\sigma}\right) = e^{-M\sigma}$, so $\int_0^T e^{-M\sigma} d\sigma = M^{-1}(I - e^{-MT})$, which tends to $M^{-1}$ by Lemma 2. $\square$

**Theorem 1 (the bound).** For all $t \ge 0$ and every node $i$,

$$ |v_i(t)| \;\le\; V_i \;=\; \sum_k R_{ik} I_k \;=\; (G^{-1} B s)_i . $$

If there is one aggressor and $0 \le u'(t) \le s$, then $0 \le v_i(t) \le V_i$.

*Proof.* By variation of constants, $v(t) = \int_0^t e^{-M(t-\tau)} C^{-1} B u'(\tau)\, d\tau$. Take absolute values entry by entry. Since $e^{-M(t-\tau)}$ and $C^{-1} B$ have nonnegative entries (Lemma 2),

$$ |v(t)| \le \int_0^t e^{-M(t-\tau)} C^{-1} B\, |u'(\tau)|\, d\tau \le \int_0^t e^{-M\sigma} d\sigma\; C^{-1} B s \le \int_0^\infty e^{-M\sigma} d\sigma\; C^{-1} B s . $$

The last step adds the integral over $(t, \infty)$ of a vector with nonnegative entries. By Lemma 3 the right side is $M^{-1} C^{-1} B s = G^{-1} C C^{-1} B s = G^{-1} B s$, and Lemma 1 gives the form $\sum_k R_{ik} I_k$. With one aggressor and $u' \ge 0$, the integrand of $v(t)$ has nonnegative entries, so $v(t) \ge 0$. $\square$

**Theorem 2 (the bound is the best one that depends only on the slopes).** For one aggressor with $u'(t) = s$ for all $t \ge 0$, $v(t) = (I - e^{-Mt}) V \to V$. For a ramp of rise time $t_r$, $v(t_r) = (I - e^{-M t_r}) V$. For one node ($n = 1$) the peak is $V_0 (1 - e^{-t_r / \tau})$ with $\tau = r_0 \bar c_0$.

*Proof.* With constant $u' = s$, $v(t) = \int_0^t e^{-M\sigma} d\sigma\, C^{-1} B s = M^{-1}(I - e^{-Mt}) C^{-1} B s = (I - e^{-Mt}) V$, since $M^{-1}$ and $e^{-Mt}$ commute. Lemma 2 gives the limit. For $n = 1$, $v$ rises as $V_0(1 - e^{-t/\tau})$ until $t_r$, and after $t_r$ the input is constant and $v$ decays as $e^{-(t - t_r)/\tau}$. So the peak is at $t_r$. $\square$

So no bound that uses only the slope $s$ can be smaller than $V$ at any node, since the bound must also hold for longer and longer ramps. For a given finite ramp, the ratio of the true peak to $V$ is below 1, and it tends to 0 as $t_r / \tau \to 0$.

**Lemma 4 (the two passes compute $V$).** After lines L1 to L3, $I[k] = D_k = \sum_{j \in T(k)} I_j$, where $T(k)$ is the subtree of $k$. After lines L4 to L6, $V[i] = \sum_{j \in P(i)} r_j D_j = \sum_k R_{ik} I_k$, where $P(i)$ is the set of nodes on the path from node 0 to $i$, with $r_0$ for the driver.

*Proof.* L1 sets $I[k] = I_k$. Lines L2 and L3 visit $k = n-1, \ldots, 1$. Every proper descendant of $k$ has a larger index, so when the loop reaches $k$, every child $c$ of $k$ has already been visited, and by strong induction on decreasing index $I[c] = D_c$ when it was added to $I[k]$. Nothing is added to $I[k]$ after the loop visits it, because later indices are smaller and are not children of $k$. So $I[k] = I_k + \sum_{c} D_c = D_k$. Lines L4 to L6 visit nodes in increasing order, so $V[p(k)]$ is final when $V[k]$ is set, and by induction $V[i] = \sum_{j \in P(i)} r_j D_j$. Finally, $k \in T(j)$ if and only if $j \in P(k)$, so

$$ \sum_{j \in P(i)} r_j D_j = \sum_{j \in P(i)} r_j \sum_{k : j \in P(k)} I_k = \sum_k I_k \sum_{j \in P(i) \cap P(k)} r_j = \sum_k R_{ik} I_k . \;\square $$

**Theorem 3 (the bound survives backward Euler).** Let $h > 0$, $t_j = j h$, $v_0 = 0$ and $(C + hG) v_{j+1} = C v_j + B (u(t_{j+1}) - u(t_j))$. Then $|v_j| \le V$ for every $j$.

*Proof.* $A = C + hG$ has positive diagonal entries $d_k$, nonpositive off-diagonal entries, and row $k$ has $d_k - \sum_{j \ne k} |A_{kj}| = \bar c_k + h G_{kk} - h \sum_{j \ne k} |G_{kj}| \ge \bar c_k > 0$. Write $A = D - N$ with $D$ the diagonal and $N \ge 0$. The row sums of $D^{-1} N$ are below 1, so $\|D^{-1}N\|_\infty < 1$ and $A^{-1} = \sum_{m \ge 0} (D^{-1} N)^m D^{-1}$ has nonnegative entries. Now $|u_a(t_{j+1}) - u_a(t_j)| \le h s_a$. If $|v_j| \le V$, then

$$ |v_{j+1}| \le A^{-1} \left( C |v_j| + h B s \right) \le A^{-1}(C V + h G V) = A^{-1} A V = V, $$

using $B s = G V$. Induction on $j$ ends the proof. $\square$

Theorem 3 is why the tests can check the bound with no rounding at all: they run backward Euler in exact rational arithmetic and compare each state with $V$.

**Scope.** Theorem 1 uses only that $G$ is symmetric positive definite with nonpositive off-diagonal entries and that $C$ is diagonal and positive. So $|v| \le G^{-1} B s$ also holds for an RC mesh with grounded capacitors and at least one resistive path to ground. Only the form $\sum_k R_{ik} I_k$ and the two linear passes need a tree. The theorem needs ideal aggressor sources, a linear holding resistance for the victim driver and no inductance. It says nothing about a nonlinear driver, about aggressors whose waveform is changed by the victim, or about RLC lines, where the response can overshoot.
