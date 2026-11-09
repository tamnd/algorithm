---
title: Each cut keeps the set and shrinks the volume, so the ellipsoid method is correct
proves: [correctness, termination]
status: full
---

**Statement.** Let $n \ge 2$ (for $n = 1$ the method is bisection, and the claims below hold with the ratio $1/2$). Let $E = E(x, P)$ with $P$ positive definite, let $g \ne 0$, and let $x', P'$ be computed by lines L5 to L7. Then:

1. $P'$ is positive definite, and $E' = E(x', P')$ contains $E \cap \{z : g^\top z \le g^\top x\}$.
2. $\operatorname{vol} E' / \operatorname{vol} E = \frac{n}{n+1} \left(\frac{n^2}{n^2-1}\right)^{(n-1)/2} < e^{-1/(2(n+1))}$.
3. If $K \subseteq B(0, R)$ is convex and either empty or contains a ball of radius $r$, then ELLIPSOID returns a point of $K$, or returns EMPTY and $K$ is empty.

**Step 1 (reduction to the unit ball).** Let $J$ be a matrix with $P = JJ^\top$ (for example the Cholesky factor). The map $u \mapsto x + Ju$ sends the unit ball $U$ onto $E$. Let $h = J^\top g / \|J^\top g\|$ and let $Q$ be an orthogonal matrix with $Q e_1 = h$. Replace $J$ by $JQ$; this does not change $P$, and now $J^\top g = \|J^\top g\| e_1$. In $u$-coordinates the cut $g^\top z \le g^\top x$ is $u_1 \le 0$, and

$$\tilde b = \frac{Pg}{\sqrt{g^\top P g}} = \frac{J J^\top g}{\|J^\top g\|} = J e_1.$$

So $x' = x + J(-e_1/(n+1))$ and $P' = J D J^\top$ with $D = \frac{n^2}{n^2-1}\left(I - \frac{2}{n+1} e_1 e_1^\top\right)$. The matrix $D$ is diagonal with $D_{11} = \frac{n^2}{n^2-1} \cdot \frac{n-1}{n+1} = \frac{n^2}{(n+1)^2}$ and $D_{ii} = \frac{n^2}{n^2-1}$ for $i \ge 2$, all positive, so $P'$ is positive definite. In $u$-coordinates, $E'$ is

$$U' = \left\{u : \left(\tfrac{n+1}{n}\right)^2 \left(u_1 + \tfrac{1}{n+1}\right)^2 + \tfrac{n^2-1}{n^2} \sum_{i \ge 2} u_i^2 \le 1\right\}.$$

Affine maps keep containment and multiply all volumes by the same factor $|\det J|$, so it is enough to prove claims 1 and 2 for $U$, the half-ball $H = U \cap \{u_1 \le 0\}$ and $U'$.

**Step 2 (claim 1).** Let $u \in H$, so $\sum_i u_i^2 \le 1$ and $-1 \le u_1 \le 0$. Then $\sum_{i \ge 2} u_i^2 \le 1 - u_1^2$, and

$$\left(\tfrac{n+1}{n}\right)^2 \left(u_1 + \tfrac{1}{n+1}\right)^2 + \tfrac{n^2-1}{n^2} (1 - u_1^2) = \frac{(n+1)^2 u_1^2 + 2(n+1) u_1 + 1 + (n^2 - 1) - (n^2-1) u_1^2}{n^2} = \frac{2(n+1)\, u_1 (u_1 + 1) + n^2}{n^2}.$$

Since $-1 \le u_1 \le 0$, $u_1(u_1 + 1) \le 0$, so the value is at most $1$, and $u \in U'$.

**Step 3 (claim 2).** $U'$ has the semi-axes $\frac{n}{n+1}$ and, $n - 1$ times, $\frac{n}{\sqrt{n^2-1}}$, so $\operatorname{vol} U' / \operatorname{vol} U = \frac{n}{n+1} \left(\frac{n^2}{n^2-1}\right)^{(n-1)/2}$. With $1 + t < e^t$ for $t \ne 0$:

$$\frac{n}{n+1} = 1 - \frac{1}{n+1} < e^{-1/(n+1)}, \qquad \left(\frac{n^2}{n^2-1}\right)^{(n-1)/2} = \left(1 + \frac{1}{n^2-1}\right)^{(n-1)/2} < e^{\frac{n-1}{2(n^2-1)}} = e^{\frac{1}{2(n+1)}}.$$

The product is less than $e^{-1/(n+1) + 1/(2(n+1))} = e^{-1/(2(n+1))}$.

**Step 4 (claim 3).** Let $E_k$ be the ellipsoid at step $k$ of line L2, with $E_0 = B(0, R)$. By induction, $K \subseteq E_k$: this holds for $k = 0$, and if $K \subseteq E_k$, then $K \subseteq E_k \cap \{z : g^\top z \le g^\top x_k\} \subseteq E_{k+1}$ by the oracle property and claim 1. By claim 2, $\operatorname{vol} E_k < e^{-k/(2(n+1))} \operatorname{vol} B(0, R)$ for $k \ge 1$.

A returned point was accepted by the oracle, so it lies in $K$. Suppose the method returns EMPTY. Then it made $N + 1 \ge N$ cuts with $N \ge 2n(n+1) \ln(R/r)$, so $\operatorname{vol} E_N < e^{-n \ln(R/r)} \operatorname{vol} B(0, R) = (r/R)^n \operatorname{vol} B(0, R) = \operatorname{vol} B(0, r)$. If $K$ contained a ball of radius $r$, then that ball would lie in $E_N$, which has a smaller volume. So $K$ contains no such ball, and by the promise $K$ is empty. $\blacksquare$

**Remark.** The proof is in exact arithmetic. For a version with rounding, see Khachiyan (1980), Bland, Goldfarb and Todd (1981, Section 3), or Grötschel, Lovász and Schrijver (Chapter 3): the matrix is blown up by a factor slightly above $1$ to absorb the rounding errors, and the volume still shrinks by a factor $e^{-1/(5n)}$ per step or similar.
