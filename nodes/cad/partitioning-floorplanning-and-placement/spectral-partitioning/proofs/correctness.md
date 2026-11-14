---
title: Spectral partitioning returns a valid split, its power iteration converges, and the second eigenvalue bounds every cut from below
proves: [correctness, termination, lower bound, running time]
status: full
---

Let $G = (V, E)$ have $n \ge 2$ vertices, weights $w(u, v) > 0$ and Laplacian $L = D - A$. For every real vector $x$,

$$ x^{\top} L x = \sum_{\{u, v\} \in E} w(u, v) \, (x_u - x_v)^2 \ge 0. $$

So $L$ is symmetric and positive semidefinite. By the [spectral theorem](/spectral-theorem/) it has an orthonormal basis of eigenvectors $u_1, \ldots, u_n$ with eigenvalues $0 = \lambda_1 \le \lambda_2 \le \cdots \le \lambda_n$, and we take $u_1 = \mathbf 1 / \sqrt n$. Let $U = \mathbf 1^{\perp}$, the vectors with sum 0. We assume exact real arithmetic; the implementation uses floating point and checks the residual in floating point.

**Lemma 1 (the largest eigenvalue).** $\lambda_n \le 2 \Delta$, where $\Delta = \max_v d(v)$.

*Proof.* Since $(x_u - x_v)^2 \le 2 x_u^2 + 2 x_v^2$, we get $x^{\top} L x \le 2 \sum_{\{u,v\} \in E} w(u, v) (x_u^2 + x_v^2) = 2 \sum_v d(v) x_v^2 \le 2 \Delta \, x^{\top} x$. The largest eigenvalue is the largest Rayleigh quotient, so $\lambda_n \le 2 \Delta$. $\square$

**Lemma 2 (the relaxation).** For $x \in U$, $x \ne 0$, $x^{\top} L x / x^{\top} x \ge \lambda_2$, with equality exactly when $x$ is an eigenvector of $\lambda_2$.

*Proof.* Write $x = \sum_{i \ge 2} \alpha_i u_i$, which is possible because $x \perp u_1$. Then $x^{\top} L x = \sum_{i \ge 2} \lambda_i \alpha_i^2 \ge \lambda_2 \sum_{i \ge 2} \alpha_i^2 = \lambda_2 \, x^{\top} x$, with equality exactly when $\alpha_i = 0$ for every $i$ with $\lambda_i > \lambda_2$. $\square$

**Theorem 1 (lower bounds).** If $n$ is even, every bisection $(A, B)$ has $\mathrm{cut}(A, B) \ge n \lambda_2 / 4$. Every split with $A, B \ne \emptyset$ has $\mathrm{cut}(A, B) / (|A| |B|) \ge \lambda_2 / n$.

*Proof.* For a bisection put $x_v = 1$ on $A$ and $x_v = -1$ on $B$. Then $x \in U$, $x^{\top} x = n$ and every cut edge contributes $w \cdot 2^2$, so $x^{\top} L x = 4 \, \mathrm{cut}(A, B)$. Lemma 2 gives $4 \, \mathrm{cut}(A, B) \ge \lambda_2 n$. For a general split put $x_v = |B|$ on $A$ and $x_v = -|A|$ on $B$. Then $x \in U$, $x^{\top} x = n |A| |B|$ and each cut edge contributes $w \, n^2$, so $n^2 \, \mathrm{cut}(A, B) \ge \lambda_2 \, n |A| |B|$. $\square$

**Theorem 2 (convergence of lines L2 to L6).** Let $c = 2 \Delta > 0$ and $\mu_i = c - \lambda_i$. Let $E_2$ be the eigenspace of $\lambda_2$ inside $U$, let $\lambda'$ be the least eigenvalue larger than $\lambda_2$, and $q = (c - \lambda')/(c - \lambda_2)$, or $q = 0$ if there is no such eigenvalue. Let $x_0$ be the vector of line L2 and write $x_0 = y_0 + z_0$ with $y_0 \in E_2$ and $z_0 \perp E_2$, $z_0 \in U$. If $y_0 \ne 0$, then after $k$ executions of line L6,

$$ \| L x_k - \rho_k x_k \| \le (\lambda_n - \lambda_2) \, \frac{\|z_0\|}{\|y_0\|} \, q^k, \qquad \rho_k = x_k^{\top} L x_k. $$

In particular $0 \le q < 1$ and the loop stops after finitely many steps for every $\tau > 0$.

*Proof.* By Lemma 1, $0 \le \mu_n \le \cdots \le \mu_2$ for the eigenvalues on $U$, and $\mu_i \le c - \lambda' = q \mu_2$ for every $i$ with $\lambda_i > \lambda_2$. Line L6 multiplies by $M = cI - L$, which maps $U$ to $U$ because $M \mathbf 1 = c \mathbf 1$ and $M$ is symmetric. So in exact arithmetic the mean removal changes nothing, and the normalization only scales. Hence $x_k = M^k x_0 / \|M^k x_0\|$. In the eigenbasis, $M^k y_0 = \mu_2^k y_0$ and $\|M^k z_0\| \le (q \mu_2)^k \|z_0\|$, since every component of $z_0$ is along some $u_i$ with $\lambda_i > \lambda_2$, and $0 \le \mu_i \le q \mu_2$ there. Write $x_k = y_k + z_k$ in the same way. Then

$$ \frac{\|z_k\|}{\|y_k\|} = \frac{\|M^k z_0\|}{\mu_2^k \|y_0\|} \le q^k \frac{\|z_0\|}{\|y_0\|}, $$

and since $\|x_k\| = 1$, $\|z_k\| \le \|z_k\| / \|y_k\|$ once $\|y_k\| \le 1$, which always holds. For a unit vector $x$, the value $\sigma = x^{\top} L x$ minimizes $\|L x - \sigma x\|$ over all real $\sigma$, because $\|Lx - \sigma x\|^2 = \|Lx\|^2 - 2 \sigma \, x^{\top} L x + \sigma^2$. So

$$ \|L x_k - \rho_k x_k\| \le \|(L - \lambda_2 I) x_k\| = \|(L - \lambda_2 I) z_k\| \le (\lambda_n - \lambda_2) \|z_k\|, $$

because $(L - \lambda_2 I) y_k = 0$ and $L - \lambda_2 I$ has norm at most $\lambda_n - \lambda_2$ on the span of the $u_i$ with $\lambda_i > \lambda_2$. Combining the two bounds gives the claim. $q < 1$ because $\lambda' > \lambda_2$. $\square$

If $\Delta = 0$ there are no edges, $L = 0$, every vector of $U$ is an eigenvector, and line L5 stops at once with residual 0. The set of starts with $y_0 = 0$ is the subspace $E_2^{\perp} \cap U$ of dimension less than $n - 1$; the start of line L2 is a continuous random vector projected onto $U$, so $y_0 \ne 0$ with probability 1.

**Theorem 3 (valid output).** Line L8 returns parts of sizes $\lfloor n/2 \rfloor$ and $\lceil n/2 \rceil$. Line L10 returns two nonempty parts, and the value $R_k$ of line L9 is the ratio cut of the split into the first $k$ sorted vertices and the rest.

*Proof.* Line L7 gives a permutation $v_1, \ldots, v_n$ of $V$. Line L8 returns $\{v_1, \ldots, v_{\lfloor n/2 \rfloor}\}$ and its complement. In line L9, let $S_k = \{v_1, \ldots, v_k\}$ and keep the invariant that the variable cut equals $\mathrm{cut}(S_k, V \setminus S_k)$. It holds for $S_0 = \emptyset$ with value 0. Moving $v = v_k$ from the second part to the first changes the side of $v$ only. An edge $\{v, u\}$ with $u \notin S_k$ becomes cut, and an edge $\{v, u\}$ with $u \in S_{k-1}$ stops being cut. Edges without $v$ do not change. The implementation adds $w$ for the first kind and subtracts $w$ for the second, so the invariant holds for $S_k$. For $1 \le k \le n - 1$ both $S_k$ and its complement are nonempty, so $R_k = \mathrm{cut}(S_k, V \setminus S_k)/(k(n - k))$ is the ratio cut, and line L10 returns the split of least $R_k$. $\blacksquare$

**Running time.** Building the adjacency lists, the degrees and $c$ takes $O(n + m)$. One loop step computes $Lx$ from the lists in $O(n + m)$ and the inner products and the mean in $O(n)$. Line L7 sorts in $O(n \log n)$. In line L9 each vertex is moved once, and the update scans its edges once, so the sweep takes $O(n + m)$ in total. With $t$ loop steps the time is $\Theta(t (n + m) + n \log n)$ and the space is $\Theta(n + m)$. By Theorem 2, $t \le 1 + \log\big((\lambda_n - \lambda_2) \|z_0\| / (\tau \|y_0\|)\big) / \log(1/q)$ when $q > 0$.

**What is not proved.** Nothing above says that the rounded split has a small cut compared with the optimum. The roach graphs of Guattery and Miller (1998) show that no such constant-factor statement holds for the median split.
