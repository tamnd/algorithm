---
title: The scan returns the largest admissible index, and its error is within a constant factor of the best balance of approximation and noise errors on the grid
proves: [correctness, termination]
status: full
---

**Setting.** $A$ is a real $m \times n$ matrix with thin SVD $A = \sum_{i=1}^r s_iu_iv_i^T$, $s_1 \ge \dots \ge s_r > 0$. The data are $y = \bar y + e$ with $\bar y = Ax^\dagger$, $\lVert e\rVert \le \delta$, and $x^\dagger$ in the span of the $v_i$ (the minimum norm solution). For $\alpha > 0$, $x_\alpha = (A^TA + \alpha I)^{-1}A^Ty$ and $\bar x_\alpha$ is the same for $\bar y$. The grid is $\alpha_0 < \alpha_1 < \dots < \alpha_{N-1}$ and $\kappa \ge 1$. Write $x_j = x_{\alpha_j}$, $\psi_j = \delta/(2\sqrt{\alpha_j})$ and $\varphi_j = \lVert\bar x_{\alpha_j} - x^\dagger\rVert$. Call $j$ admissible if $\lVert x_j - x_i\rVert \le 4\kappa\psi_i$ for all $i < j$.

**Claim 1 (what the scan returns).** Lines L4 to L8 terminate and return the largest admissible index $\hat j$ together with $\alpha_{\hat j}$ and $x_{\hat j}$.

*Proof.* Line L2 stores the coefficients $c_{j,k} = s_kb_k/(s_k^2 + \alpha_j)$ of $x_j$ in the orthonormal basis $v_k$, so $\lVert c_j - c_i\rVert = \lVert x_j - x_i\rVert$. For a given $j$, lines L5 to L7 accept $j$ exactly when no $i < j$ violates the test, that is, when $j$ is admissible. The scan visits $j = N - 1, N - 2, \dots$ in decreasing order and returns at the first accepted $j$, which is therefore the largest admissible index. Index $0$ has no $i < 0$ to test, so it is admissible and the scan returns after at most $N$ outer passes, each with at most $N - 1$ inner tests. $\square$

**Claim 2 (the noise bound).** $\lVert x_\alpha - \bar x_\alpha\rVert \le \delta/(2\sqrt\alpha)$, and the bound is attained for some $e$ when $\sqrt\alpha$ is a singular value.

*Proof.* $x_\alpha - \bar x_\alpha = \sum_k s_k\langle u_k, e\rangle/(s_k^2 + \alpha)\,v_k$. By the inequality of arithmetic and geometric means, $s^2 + \alpha \ge 2s\sqrt\alpha$, so $s/(s^2 + \alpha) \le 1/(2\sqrt\alpha)$ for all $s > 0$, with equality at $s = \sqrt\alpha$. Hence the norm is at most $\lVert e\rVert/(2\sqrt\alpha) \le \delta/(2\sqrt\alpha)$. If $s_k = \sqrt\alpha$, take $e = \delta u_k$. $\square$

So $\lVert x_j - x^\dagger\rVert \le \varphi_j + \psi_j$ for every $j$.

**Claim 3 (monotonicity).** $\psi_j$ is strictly decreasing in $j$, and $\varphi_j$ is nondecreasing in $j$.

*Proof.* The first is clear. For the second, $\bar x_\alpha - x^\dagger = -\sum_k \alpha/(s_k^2 + \alpha)\,\xi_kv_k$ with $\xi_k = \langle x^\dagger, v_k\rangle$, since $\bar b_k = s_k\xi_k$ and $s_k^2\xi_k/(s_k^2 + \alpha) - \xi_k = -\alpha\xi_k/(s_k^2 + \alpha)$. Each factor $\alpha/(s_k^2 + \alpha)$ is increasing in $\alpha$. $\square$

**Claim 4 (oracle inequality).** Assume $\varphi_0 \le \psi_0$ and let $j^\ast = \max\{j : \varphi_j \le \psi_j\}$. Then $\hat j \ge j^\ast$ and

$$\lVert x_{\hat j} - x^\dagger\rVert \le (4\kappa + 2)\,\psi_{j^\ast}.$$

If moreover $\alpha_{j+1}/\alpha_j \le \rho$ for all $j$, then

$$\lVert x_{\hat j} - x^\dagger\rVert \le (4\kappa + 2)\sqrt\rho\,\min_{0 \le j < N}(\varphi_j + \psi_j).$$

*Proof.* First, $j^\ast$ is admissible. Let $i < j \le j^\ast$. By Claim 3 and the definition of $j^\ast$, $\varphi_j \le \varphi_{j^\ast} \le \psi_{j^\ast} \le \psi_j$. In the same way $\varphi_i \le \psi_i$. So

$$\lVert x_j - x_i\rVert \le \lVert x_j - x^\dagger\rVert + \lVert x_i - x^\dagger\rVert \le \varphi_j + \psi_j + \varphi_i + \psi_i \le 2\psi_j + 2\psi_i \le 4\psi_i \le 4\kappa\psi_i,$$

using $\psi_j < \psi_i$. With $j = j^\ast$ this shows that $j^\ast$ is admissible, so $\hat j \ge j^\ast$ by Claim 1.

If $\hat j = j^\ast$, the error is at most $\varphi_{j^\ast} + \psi_{j^\ast} \le 2\psi_{j^\ast}$. Otherwise $j^\ast < \hat j$, and the admissibility of $\hat j$ at $i = j^\ast$ gives $\lVert x_{\hat j} - x_{j^\ast}\rVert \le 4\kappa\psi_{j^\ast}$. So

$$\lVert x_{\hat j} - x^\dagger\rVert \le \lVert x_{\hat j} - x_{j^\ast}\rVert + \lVert x_{j^\ast} - x^\dagger\rVert \le 4\kappa\psi_{j^\ast} + 2\psi_{j^\ast}.$$

For the second bound, take any $j$. If $j \le j^\ast$, then $\varphi_j + \psi_j \ge \psi_j \ge \psi_{j^\ast}$. If $j > j^\ast$, then $\varphi_j \ge \varphi_{j^\ast + 1} > \psi_{j^\ast + 1}$ by the maximality of $j^\ast$ and Claim 3, and $\psi_{j^\ast + 1} = \psi_{j^\ast}\sqrt{\alpha_{j^\ast}/\alpha_{j^\ast + 1}} \ge \psi_{j^\ast}/\sqrt\rho$. In both cases $\varphi_j + \psi_j \ge \psi_{j^\ast}/\sqrt\rho$. Insert this in the first bound. $\square$

**Claim 5 (order optimality without knowing the smoothness).** Let $x^\dagger = (A^TA)^\nu w$ with $0 < \nu \le 1$. Then $\varphi(\alpha) \le \alpha^\nu\lVert w\rVert$. If the geometric grid with ratio $\rho$ satisfies $\varphi_0 \le \psi_0$ and $\alpha_{N-1} \ge \alpha_{\mathrm{bal}}$, where $\alpha_{\mathrm{bal}} = (\delta/(2\lVert w\rVert))^{2/(2\nu + 1)}$ solves $\alpha^\nu\lVert w\rVert = \delta/(2\sqrt\alpha)$, then

$$\lVert x_{\hat j} - x^\dagger\rVert \le 2(4\kappa + 2)\rho^{3/2}\,\lVert w\rVert^{1/(2\nu + 1)}(\delta/2)^{2\nu/(2\nu + 1)}.$$

*Proof.* The coefficient of $\bar x_\alpha - x^\dagger$ on $v_k$ is $-\alpha s_k^{2\nu}\omega_k/(s_k^2 + \alpha)$ with $\omega_k = \langle w, v_k\rangle$. For $0 \le \nu \le 1$, $\alpha s^{2\nu}/(s^2 + \alpha) \le \alpha^\nu$: with $u = s^2/\alpha$ this is $u^\nu \le 1 + u$, true for $u \le 1$ because $u^\nu \le 1$ and for $u \ge 1$ because $u^\nu \le u$. So $\varphi(\alpha) \le \alpha^\nu\lVert w\rVert$. Let $j$ be the smallest grid index with $\alpha_j \ge \alpha_{\mathrm{bal}}$; it exists by assumption. If $j = 0$, then $\alpha_0 \ge \alpha_{\mathrm{bal}}$, so $\psi_0 \le \psi(\alpha_{\mathrm{bal}})$, and $\varphi_0 \le \psi_0$ by assumption. If $j > 0$, then $\alpha_{\mathrm{bal}} \le \alpha_j \le \rho\,\alpha_{\mathrm{bal}}$, so $\psi_j \le \psi(\alpha_{\mathrm{bal}})$ and $\varphi_j \le \rho^\nu\alpha_{\mathrm{bal}}^\nu\lVert w\rVert = \rho^\nu\psi(\alpha_{\mathrm{bal}}) \le \rho\,\psi(\alpha_{\mathrm{bal}})$. In both cases $\varphi_j + \psi_j \le 2\rho\,\psi(\alpha_{\mathrm{bal}})$, and $\psi(\alpha_{\mathrm{bal}}) = \lVert w\rVert^{1/(2\nu + 1)}(\delta/2)^{2\nu/(2\nu + 1)}$. The second bound of Claim 4 multiplies this by $(4\kappa + 2)\sqrt\rho$. $\square$

So the rule gives the rate $O(\delta^{2\nu/(2\nu + 1)})$ for every $\nu \in (0, 1]$, which is the optimal order for Tikhonov regularization, and it does not use $\nu$. The constants are worst-case constants. In the example on the page the rule is well inside its bound but still over-smooths compared with the best grid point; that is a measurement.
