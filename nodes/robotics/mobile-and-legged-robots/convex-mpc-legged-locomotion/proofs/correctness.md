---
title: The convex MPC step solves a strictly convex QP of the linearized model
proves: [correctness]
status: partial
---

This file proves that each step of CONVEX-MPC computes the unique optimal force plan of the linear time-varying model that the method uses. It does not prove that the closed loop on the real robot, or on the full rigid body, is stable: the method has no terminal cost or terminal constraint, and the model is an approximation. Closed-loop stability is a measurement, made in simulation and on hardware.

**The model.** The state is $x = (\Theta, p, \omega, v, g) \in \mathbb{R}^{13}$, where $\Theta$ holds roll, pitch and yaw, $\omega$ is the angular velocity in the world frame, and $g = 9.81$ is a constant state. The exact relation between $\dot\Theta$ and $\omega$ for $R = R_z(\psi) R_y(\theta) R_x(\phi)$ is $\omega = E(\phi, \theta, \psi) \dot\Theta$ with a matrix $E$ that equals $R_z(\psi)$ when $\phi = \theta = 0$. The method uses $\dot\Theta = R_z(\psi)^T \omega$, so it assumes small roll and pitch. It also drops the gyroscopic term $\omega \times I \omega$ and uses $I_w = R_z(\psi) I_B R_z(\psi)^T$. With the yaw $\psi_k$ and the foot positions $r_{i,k}$ taken from the reference, the model on step $k$ is $\dot x = A_k x + B_k u$ with constant matrices, so the prediction is linear in the forces.

**Lemma 1 (exact discretization).** Let $A$ be the continuous matrix of line L1. Then $A^3 = 0$, and with the forces held constant over a step of length $\Delta t$, the exact discrete model is $x^+ = A_d x + B_d u$ with $A_d = I + A \Delta t + A^2 \Delta t^2 / 2$ and $B_d = (I \Delta t + A \Delta t^2 / 2 + A^2 \Delta t^3 / 6) B$.

*Proof.* The nonzero blocks of $A$ map $\omega$ to $\dot\Theta$, $v$ to $\dot p$ and $g$ to $\dot v$. The rows of $\omega$ and $g$ are zero. So $A^2$ has only the block that maps $g$ to $p$. The column of $A$ for $p$ is zero, because no derivative depends on $p$, so $A^3 = A A^2 = 0$. The solution of $\dot x = A x + B u$ with constant $u$ is $x(\Delta t) = e^{A \Delta t} x(0) + \int_0^{\Delta t} e^{A s} ds\, B u$, and both series end after the $A^2$ term. $\square$

**Lemma 2 (condensed prediction).** Let $X_{k+1} = A_k X_k + B_k u_k$ for $k = 0, \dots, H-1$ with $X_0 = x_0$. Then $X_k = \Phi_k x_0 + S_k U$, where $\Phi_k = A_{k-1} \cdots A_0$ and the block of $S_k$ for $u_j$ is $A_{k-1} \cdots A_{j+1} B_j$ for $j < k$ and zero otherwise.

*Proof.* By induction on $k$. It holds for $k = 0$ with $S_0 = 0$. If it holds for $k$, then $X_{k+1} = A_k \Phi_k x_0 + A_k S_k U + B_k u_k$, which is the claim for $k + 1$. The function `condense` computes exactly $x \leftarrow A_k x$ and $S \leftarrow A_k S$ plus $B_k$ in the columns of $u_k$. $\square$

**Lemma 3 (the friction constraints).** For each stance foot and step, the four rows $\pm f_x - \mu f_z \le 0$ and $\pm f_y - \mu f_z \le 0$ describe a pyramid with $k = 4$ edges that contains the Coulomb cone $\sqrt{f_x^2 + f_y^2} \le \mu f_z$. A force in the pyramid can have $\sqrt{f_x^2 + f_y^2} = \sqrt 2 \mu f_z$, so the pyramid is an outer approximation. Replacing $\mu$ by $\mu / \sqrt 2$ gives an inner one.

*Proof.* If $\sqrt{f_x^2 + f_y^2} \le \mu f_z$, then $|f_x| \le \mu f_z$ and $|f_y| \le \mu f_z$. The corner $f_x = f_y = \mu f_z$ is in the pyramid with tangential size $\sqrt 2 \mu f_z$. With $\mu' = \mu / \sqrt 2$, the pyramid gives $f_x^2 + f_y^2 \le 2 \mu'^2 f_z^2 = \mu^2 f_z^2$. $\square$

**Theorem (the QP step).** With diagonal weights $L \succeq 0$ and $\alpha > 0$, the problem

$$\min_U \sum_{k=1}^{H} (X_k - Y_k)^T L (X_k - Y_k) + \alpha |U|^2 \quad \text{subject to the rows of Lemma 3 and } f_{\min} \le f_z \le f_{\max}$$

is a strictly convex QP with Hessian $H_{qp} = 2(\sum_k S_k^T L S_k + \alpha I) \succ 0$ and linear term $g_{qp} = 2 \sum_k S_k^T L (\Phi_k x_0 - Y_k)$. If the feasible set is not empty, it has exactly one minimizer, and a point $U$ is that minimizer if and only if there are $z \ge 0$ with $H_{qp} U + g_{qp} + G^T z = 0$, $G U \le h$ and $z_i (h - G U)_i = 0$ for each row $i$.

*Proof.* Put Lemma 2 into the cost. The cost is $U^T (\sum_k S_k^T L S_k + \alpha I) U + 2 U^T \sum_k S_k^T L (\Phi_k x_0 - Y_k)$ plus a constant, which is $\frac12 U^T H_{qp} U + g_{qp}^T U$ plus a constant. The matrix $\sum_k S_k^T L S_k$ is positive semidefinite and $\alpha I$ is positive definite, so $H_{qp} \succ 0$ and the cost is strictly convex. The constraints are linear, so the feasible set is a closed convex polyhedron; a strictly convex quadratic that is bounded below on a nonempty closed convex set has exactly one minimizer. For a convex problem with linear constraints, the KKT conditions are necessary (no further constraint qualification is needed for linear constraints) and sufficient. $\square$

Lines L2 and L3 build $H_{qp}$ and $g_{qp}$ as in the theorem, line L4 builds the rows, and line L5 solves the QP. The interior point method of `solve_qp` stops only when the KKT residuals and the average complementarity are below the tolerance, so its output is a KKT point up to that tolerance, which by the theorem is the minimizer up to the same order. The convergence of the Mehrotra predictor-corrector method in a bounded number of steps is not proved here; the code raises an error if it does not converge in 100 iterations.

**What is not proved.** The method applies only the first step of the plan (line L6) and solves again at the next control period. Without a terminal cost or a terminal constraint, there is no general guarantee that the receding-horizon loop is stable or that the QP stays feasible, and the model errors (roll and pitch, the gyroscopic term, leg dynamics and foot placement) are not bounded. The tests and the published experiments show that the loop works for the tested gaits; this is evidence, not proof.
