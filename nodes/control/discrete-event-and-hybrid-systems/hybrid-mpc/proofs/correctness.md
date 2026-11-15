---
title: Enumeration of the mode sequences returns the optimum of the hybrid MPC problem
proves: [correctness, termination]
status: partial
---

**Setting.** A piecewise affine system has modes $i = 1, \ldots, s$ with $x^+ = A_i x + B_i u + f_i$ on the closed cell $\mathcal{C}_i = \{x : H_i x \le h_i\}$, $x \in \mathbb{R}^n$, $u \in \mathbb{R}^m$. A mode sequence $\sigma = (\sigma_0, \ldots, \sigma_{N-1})$ and an input sequence $U = (u_0, \ldots, u_{N-1})$ are admissible from $x_0$ if the states $x_{k+1} = A_{\sigma_k} x_k + B_{\sigma_k} u_k + f_{\sigma_k}$ satisfy $x_k \in \mathcal{C}_{\sigma_k}$ for $k = 0, \ldots, N-1$, $u_{\min} \le u_k \le u_{\max}$, and $x_{\min} \le x_k \le x_{\max}$ for $k = 1, \ldots, N$. On a point shared by two cells either mode is admissible. The problem is

$$J^*(x_0) = \min_{\sigma, U \text{ admissible}} J(U, \sigma), \qquad J = \sum_{k=0}^{N-1} \left(x_k^T Q x_k + u_k^T R u_k\right) + x_N^T P x_N,$$

with $Q \succeq 0$, $P \succeq 0$ and $R \succ 0$. Lines L1 to L7 loop over all $s^N$ sequences, solve one QP per sequence and keep the least cost.

**Lemma 1 (condensing, line L4).** For a fixed $\sigma$, $x_k = d_k + \Gamma_k U$ for $k = 0, \ldots, N$, where $d_0 = x_0$, $\Gamma_0 = 0$, $d_{k+1} = A_{\sigma_k} d_k + f_{\sigma_k}$, and $\Gamma_{k+1} = A_{\sigma_k} \Gamma_k + B_{\sigma_k} E_k$, with $E_k$ the $m \times Nm$ matrix that picks $u_k$ out of $U$.

*Proof.* Induction on $k$. The case $k = 0$ holds. If $x_k = d_k + \Gamma_k U$, then $x_{k+1} = A_{\sigma_k}(d_k + \Gamma_k U) + B_{\sigma_k} E_k U + f_{\sigma_k} = d_{k+1} + \Gamma_{k+1} U$. $\blacksquare$

**Lemma 2 (the QP of one sequence).** For a fixed $\sigma$, $J(U, \sigma) = \frac12 U^T \mathcal{H} U + \phi^T U + c$ with

$$\mathcal{H} = 2\Big(\sum_{k=0}^{N} \Gamma_k^T W_k \Gamma_k + I_N \otimes R\Big), \qquad \phi = 2 \sum_{k=0}^{N} \Gamma_k^T W_k d_k, \qquad c = \sum_{k=0}^{N} d_k^T W_k d_k,$$

where $W_k = Q$ for $k < N$ and $W_N = P$. $\mathcal{H}$ is positive definite. The admissible set of $U$ for this $\sigma$ is the polyhedron of the rows that the code builds: the input bounds, $H_{\sigma_k}(d_k + \Gamma_k U) \le h_{\sigma_k}$ for $k = 1, \ldots, N-1$, and the state bounds on $d_k + \Gamma_k U$ for $k = 1, \ldots, N$, provided $x_0 \in \mathcal{C}_{\sigma_0}$.

*Proof.* Substitute Lemma 1 into $J$ and expand each quadratic form; the input terms give $U^T (I_N \otimes R) U$. The matrix $\mathcal{H}$ is a sum of a positive semidefinite part and $2(I_N \otimes R) \succ 0$. The cell condition at $k = 0$ does not depend on $U$; line L3 tests it and skips $\sigma$ if it fails. The other conditions are the admissibility conditions with $x_k$ replaced by Lemma 1. $\blacksquare$

**Quoted result (the QP solver, line L5).** Goldfarb and Idnani (1983) proved that their dual active set method, applied to a strictly convex QP, either stops at the optimum in a finite number of steps or detects that the constraints have no common point. The code follows this method. Separately, any $(U, \lambda)$ with $\mathcal{H} U + \phi + C^T \lambda = 0$, $CU \le b$, $\lambda \ge 0$ and $\lambda_i (b - CU)_i = 0$ is the unique optimum, since the QP is convex with $\mathcal{H} \succ 0$ (the [KKT conditions](/kkt-conditions/) are sufficient). The tests check these conditions on random problems and compare with an enumeration of active sets. The proof below assumes that line L5 returns the optimum of a feasible QP and None for an infeasible one; this is the step that is quoted, not proved here.

**Theorem.** If some admissible pair exists, line L7 returns $(U^*, \sigma^*, J^*)$ with $J(U^*, \sigma^*) = J^*(x_0)$ and $(U^*, \sigma^*)$ admissible. If none exists, it returns None.

*Proof.* Let $F_\sigma$ be the admissible set of $U$ for $\sigma$; by Lemma 2 it is empty if line L3 skips $\sigma$, and otherwise it is the feasible set of the QP of line L5. Every admissible pair has its $\sigma$ in the loop of line L2, so the admissible pairs are exactly the pairs $(U, \sigma)$ with $U \in F_\sigma$, and

$$J^*(x_0) = \min_{\sigma} \min_{U \in F_\sigma} J(U, \sigma).$$

For each $\sigma$ with $F_\sigma$ nonempty, line L5 returns the inner minimizer and the code adds back the constant $c$ of Lemma 2, so it has the inner minimum. Line L6 keeps the least value seen so far. After the loop, $best$ holds the outer minimum and a pair that attains it. If all $F_\sigma$ are empty, $best$ stays None (line L1). $\blacksquare$

**Termination.** The loop of line L2 has $s^N$ passes. Each pass builds $\mathcal{H}$, $\phi$ and the rows in polynomial time in $n$, $m$ and $N$, and the QP method stops in finitely many steps (quoted above; the code also stops with an error after a fixed number of iterations). The closed loop of lines L8 and L9 calls this a given number of times.

**What is not proved.** The theorem is about one sampling instant. Feasibility at the next instant and convergence of the closed loop need more: Bemporad and Morari (1999) use a terminal equality constraint at the equilibrium, and Lazar, Heemels, Weiland and Bemporad (2006) use a terminal cost and a terminal set. The example on the page has neither; its closed loop reaches the origin in the tests, which is a measurement, not a theorem. On a point shared by two cells, the optimizer may pick a mode that differs from the one the true system uses; then the predicted and true next states differ.
