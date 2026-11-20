---
title: The maximum entropy image is unique, positive and of largest entropy among the images that fit the data
proves: [correctness]
status: full
---

**Setting.** $A$ is a real $m \times n$ matrix, $y \in \mathbb R^m$, $\sigma_i > 0$, $W = \operatorname{diag}(1/\sigma_i^2)$ and $m_j > 0$ is the default image. For $x \ge 0$ (with $0\log 0 = 0$),

$$E(x) = -S(x) = \sum_j \Big[x_j\log\frac{x_j}{m_j} - x_j + m_j\Big], \qquad \chi^2(x) = (Ax - y)^TW(Ax - y),$$

and $F_\lambda(x) = E(x) + \tfrac\lambda2\chi^2(x)$ for $\lambda > 0$. The algorithm is lines L1 to L10 of the page.

**Claim 1 (unique positive minimizer).** For every $\lambda > 0$, $F_\lambda$ has exactly one minimizer $x_\lambda$ over $x \ge 0$. All its entries are positive, and

$$x_{\lambda,j} = m_j\exp\big(-\lambda\,(A^TW(Ax_\lambda - y))_j\big).$$

*Proof.* Each term $e(t) = t\log(t/m_j) - t + m_j$ is continuous on $[0, \infty)$, strictly convex ($e'' = 1/t > 0$), at least $0$ (it is $0$ only at $t = m_j$) and grows like $t\log t$. $\chi^2$ is convex and at least $0$. So $F_\lambda$ is continuous, strictly convex, and $F_\lambda(x) \to \infty$ as $\lVert x\rVert \to \infty$ in the orthant. A continuous function with bounded sublevel sets on a closed set has a minimizer, and strict convexity makes it unique.

Suppose some $x_{\lambda,j} = 0$. Move pixel $j$ to $t > 0$. The derivative of $F_\lambda$ along this move is $\log(t/m_j) + \lambda\,(A^TW(Ax - y))_j$, where the second term stays bounded as $t \to 0^+$ and the first goes to $-\infty$. So $F_\lambda$ falls for small $t > 0$, a contradiction. Hence $x_\lambda > 0$, the minimizer is in the open orthant, the gradient vanishes there, and $\nabla F_\lambda = \log(x/m) + \lambda A^TW(Ax - y) = 0$ is the stated formula. $\square$

**Claim 2 (the Newton steps).** At $x > 0$, $H = \operatorname{diag}(1/x) + \lambda A^TWA$ is positive definite, $d = -H^{-1}g$ satisfies $g^Td < 0$ unless $g = 0$, and the search in line L8 ends with a positive point at which $F_\lambda$ is lower by at least $\tfrac14 t\,(-g^Td)$.

*Proof.* $\operatorname{diag}(1/x)$ is positive definite and $A^TWA$ is positive semidefinite, so $H$ is positive definite and so is $H^{-1}$. Then $g^Td = -g^TH^{-1}g < 0$ for $g \ne 0$. The set $x > 0$ is open, so $x + td > 0$ for all small $t$. $F_\lambda$ is differentiable at $x$, so $F_\lambda(x + td) = F_\lambda(x) + t g^Td + o(t)$, which is below $F_\lambda(x) + \tfrac14 t g^Td$ for small $t$. Halving $t$ reaches such a $t$ after finitely many steps. $\square$

So the values of $F_\lambda$ along the Newton iterates never increase; the tests check this at every step. Near $x_\lambda$ the Hessian is continuous and positive definite, and Newton's method with full steps converges quadratically there. We do not prove a global bound on the number of steps, because the entropy Hessian $1/x_j$ is unbounded near the boundary of the orthant; the code stops when the Newton decrement $-g^Td$ is below a tolerance, and the tests check the stationary condition of Claim 1 at the output.

**Claim 3 (maximum entropy among the images that fit).** Let $x_\lambda$ minimize $F_\lambda$ and let $C = \chi^2(x_\lambda)$. For every $x \ge 0$ with $\chi^2(x) \le C$, $S(x) \le S(x_\lambda)$. If $x \ne x_\lambda$, the inequality is strict.

*Proof.* $E(x_\lambda) + \tfrac\lambda2 C = F_\lambda(x_\lambda) \le F_\lambda(x) = E(x) + \tfrac\lambda2\chi^2(x) \le E(x) + \tfrac\lambda2 C$. So $E(x_\lambda) \le E(x)$, that is $S(x) \le S(x_\lambda)$. If $x \ne x_\lambda$, the first inequality is strict by uniqueness. $\square$

So the output of the bisection, with $\chi^2(x_\lambda) = C$, is the unique solution of the constrained problem $\max S$ subject to $\chi^2 \le C$, and also of the problem with $\chi^2 = C$ when it exists.

**Claim 4 (monotone trade-off).** If $0 < \lambda_1 < \lambda_2$, then $\chi^2(x_{\lambda_2}) \le \chi^2(x_{\lambda_1})$ and $S(x_{\lambda_2}) \le S(x_{\lambda_1})$.

*Proof.* Write $E_k = E(x_{\lambda_k})$ and $c_k = \tfrac12\chi^2(x_{\lambda_k})$. Optimality of each minimizer gives $E_1 + \lambda_1c_1 \le E_2 + \lambda_1c_2$ and $E_2 + \lambda_2c_2 \le E_1 + \lambda_2c_1$. Adding them gives $(\lambda_2 - \lambda_1)(c_2 - c_1) \le 0$, so $c_2 \le c_1$. Then the first inequality gives $E_1 - E_2 \le \lambda_1(c_2 - c_1) \le 0$, so $E_2 \ge E_1$, that is $S(x_{\lambda_2}) \le S(x_{\lambda_1})$. $\square$

**Claim 5 (existence of $\lambda$ and the bisection).** The map $\lambda \mapsto \chi^2(x_\lambda)$ is continuous on $(0, \infty)$, tends to $\chi^2(m)$ as $\lambda \to 0$, and tends to $\inf_{x \ge 0}\chi^2(x)$ as $\lambda \to \infty$. So if $\inf_{x\ge0}\chi^2 < C < \chi^2(m)$, some $\lambda$ gives $\chi^2(x_\lambda) = C$, and bisection on $\lambda$ converges to such a value.

*Proof.* Continuity: $F_\lambda(x)$ is jointly continuous in $(\lambda, x)$, the minimizer is unique, and for $\lambda$ in a compact interval of $(0, \infty)$ the minimizers stay in a bounded set (since $F_\lambda(x_\lambda) \le F_\lambda(m) = \tfrac\lambda2\chi^2(m)$ bounds $E(x_\lambda)$, and $E$ has bounded sublevel sets). A standard argument (every limit point of $x_{\lambda_k}$ minimizes the limit function, which has one minimizer) gives continuity of $\lambda \mapsto x_\lambda$, hence of $\chi^2(x_\lambda)$.

$\lambda \to 0$: $E(x_\lambda) \le F_\lambda(m) = \tfrac\lambda2\chi^2(m) \to 0$, and $E$ is $0$ only at $m$ and has bounded sublevel sets, so $x_\lambda \to m$.

$\lambda \to \infty$: for any $z \ge 0$, $\tfrac\lambda2\chi^2(x_\lambda) \le F_\lambda(x_\lambda) \le E(z) + \tfrac\lambda2\chi^2(z)$, so $\chi^2(x_\lambda) \le \chi^2(z) + 2E(z)/\lambda$. Taking $z$ close to the infimum of $\chi^2$ and then $\lambda$ large shows that $\chi^2(x_\lambda)$ approaches the infimum.

By Claim 4 the map is nonincreasing, and by continuity it takes the value $C$ (intermediate value theorem). Line L1 finds $hi$ with $\chi^2(x_{hi}) \le C$, and the invariant $\chi^2(x_{lo}) > C \ge \chi^2(x_{hi})$ holds through line L9. The interval $[lo, hi]$ shrinks geometrically in $\log\lambda$ and contains a point where $\chi^2 = C$, so by continuity $\chi^2(x_\lambda) \to C$ along the bisection. $\square$

The tests check Claim 1 (the stationary formula, positivity, and a comparison with a per-pixel bisection when $A = I$), Claim 2 (no increase of $F_\lambda$), Claim 3 (by random positive images with $\chi^2 \le C$), Claim 4 on a grid of $\lambda$, the two-pixel example of the page in closed form, and the gradient against central finite differences.
