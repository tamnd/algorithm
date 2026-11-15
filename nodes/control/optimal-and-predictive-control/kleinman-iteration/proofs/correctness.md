---
title: Kleinman iteration stays stabilizing, decreases monotonically and converges quadratically to the stabilizing solution of the CARE
proves: [correctness, termination]
status: full
---

Let $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$, $Q = Q^T \ge 0$ and $R = R^T > 0$, and put $G = B R^{-1} B^T$. Assume that $(Q^{1/2}, A)$ is detectable: there is no $v \ne 0$ with $A v = \lambda v$, $\operatorname{Re} \lambda \ge 0$ and $Q v = 0$ (the PBH test; $Q v = 0$ is the same as $Q^{1/2} v = 0$ because $Q \ge 0$). Let $K_0$ be a gain with $A - B K_0$ Hurwitz. For $k = 0, 1, 2, \dots$ the algorithm sets $A_k = A - B K_k$, solves

$$A_k^T P_k + P_k A_k + Q + K_k^T R K_k = 0 \tag{1}$$

and sets $K_{k+1} = R^{-1} B^T P_k$. Write $D_k = K_k - K_{k+1}$.

## Lemma 1: Lyapunov equations with a Hurwitz matrix

If $F$ is Hurwitz and $W = W^T$, then $F^T X + X F + W = 0$ has exactly one solution, $X = \int_0^\infty e^{F^T t} W e^{F t}\, dt$. It is symmetric, and $X \ge 0$ if $W \ge 0$.

*Proof.* The eigenvalues of the linear map $X \mapsto F^T X + X F$ are the sums $\lambda_i + \lambda_j$ of eigenvalues of $F$, which have negative real part, so the map is invertible and the solution is unique. The integral converges because $\|e^{F t}\| \le c e^{-\alpha t}$ for some $c$ and $\alpha > 0$. Its integrand $Y(t) = e^{F^T t} W e^{F t}$ satisfies $\dot Y = F^T Y + Y F$, so $F^T X + X F = \int_0^\infty \dot Y\, dt = -Y(0) = -W$. Symmetry and $X \ge 0$ for $W \ge 0$ are clear from the integrand. $\square$

## Lemma 2: the improvement identity

If $P_k$ solves (1) and $K_{k+1} = R^{-1} B^T P_k$, then

$$A_{k+1}^T P_k + P_k A_{k+1} + Q + K_{k+1}^T R K_{k+1} = -D_k^T R D_k. \tag{2}$$

*Proof.* $A_{k+1} = A_k + B D_k$, and $B^T P_k = R K_{k+1}$. So $A_{k+1}^T P_k + P_k A_{k+1} = A_k^T P_k + P_k A_k + D_k^T R K_{k+1} + K_{k+1}^T R D_k$. By (1) this is $-Q - K_k^T R K_k + D_k^T R K_{k+1} + K_{k+1}^T R D_k$. Add $Q + K_{k+1}^T R K_{k+1}$ and put $K_k = K_{k+1} + D_k$:

$$-(K_{k+1} + D_k)^T R (K_{k+1} + D_k) + D_k^T R K_{k+1} + K_{k+1}^T R D_k + K_{k+1}^T R K_{k+1} = -D_k^T R D_k. \qquad \square$$

## Lemma 3: every gain stabilizes

For every $k$, $A_k$ is Hurwitz and $P_k \ge 0$.

*Proof.* Induction on $k$. For $k = 0$, $A_0$ is Hurwitz by assumption. Suppose $A_k$ is Hurwitz. By Lemma 1, (1) has a unique solution and $P_k \ge 0$, since $Q + K_k^T R K_k \ge 0$. Let $A_{k+1} v = \lambda v$ with $v \ne 0$. Multiply (2) by $v^*$ on the left and $v$ on the right:

$$2 \operatorname{Re}(\lambda)\, v^* P_k v = -v^* Q v - (K_{k+1} v)^* R (K_{k+1} v) - (D_k v)^* R (D_k v).$$

If $\operatorname{Re} \lambda \ge 0$, the left side is at least 0 and the right side is at most 0, so both are 0. Then $Q v = 0$ (as $Q \ge 0$) and $K_{k+1} v = 0$ (as $R > 0$). So $A v = A_{k+1} v + B K_{k+1} v = \lambda v$ with $Q v = 0$ and $\operatorname{Re} \lambda \ge 0$, which detectability excludes. Hence $A_{k+1}$ is Hurwitz. $\square$

## Lemma 4: monotone decrease

For every $k$, $P_k - P_{k+1} \ge 0$.

*Proof.* Equation (1) for $k + 1$ reads $A_{k+1}^T P_{k+1} + P_{k+1} A_{k+1} + Q + K_{k+1}^T R K_{k+1} = 0$. Subtract it from (2):

$$A_{k+1}^T (P_k - P_{k+1}) + (P_k - P_{k+1}) A_{k+1} + D_k^T R D_k = 0.$$

$A_{k+1}$ is Hurwitz by Lemma 3 and $D_k^T R D_k \ge 0$, so Lemma 1 gives $P_k - P_{k+1} \ge 0$. $\square$

## Lemma 5: the limit is the stabilizing solution

The sequence $P_k$ converges to a matrix $P$ that solves the CARE $A^T P + P A - P G P + Q = 0$, and $A - G P$ is Hurwitz.

*Proof.* By Lemmas 3 and 4, $P_0 \ge P_1 \ge \dots \ge 0$. For each $x$, the numbers $x^T P_k x$ decrease and are at least 0, so they converge. By polarization, $x^T P_k y = \frac14 ((x + y)^T P_k (x + y) - (x - y)^T P_k (x - y))$ converges for all $x$, $y$, so every entry of $P_k$ converges. Let $P$ be the limit. Then $K_{k+1} = R^{-1} B^T P_k \to K := R^{-1} B^T P$, and taking the limit in (1) gives $(A - B K)^T P + P (A - B K) + Q + K^T R K = 0$. With $B K = G P$ and $K^T R K = P G P$ this is $A^T P + P A - 2 P G P + P G P + Q = 0$, the CARE. Also $P \ge 0$. For stability, let $(A - G P) v = \lambda v$ with $v \ne 0$; the limit equation gives $2 \operatorname{Re}(\lambda) v^* P v = -v^* Q v - (K v)^* R (K v)$. If $\operatorname{Re} \lambda \ge 0$, both sides are 0, so $Q v = 0$ and $K v = 0$, hence $A v = \lambda v$, which detectability excludes. $\square$

A stabilizing solution of the CARE is unique (two of them, $P$ and $P'$, give $(A - G P)^T (P - P') + (P - P')(A - G P') = 0$, a Sylvester equation with a unique solution 0 because the two matrices are Hurwitz). So the limit is the stabilizing solution, whatever stabilizing $K_0$ is used.

## Lemma 6: the error identity and quadratic convergence

Let $E_k = P_k - P$. Then

$$A_{k+1}^T E_{k+1} + E_{k+1} A_{k+1} + E_k G E_k = 0, \tag{3}$$

so $E_k \ge 0$ for $k \ge 1$, and there is a constant $c$ with $\|E_{k+1}\| \le c \|E_k\|^2$ for all $k$.

*Proof.* Let $K = R^{-1} B^T P$. For any gain $L$, the CARE can be written as

$$(A - B L)^T P + P (A - B L) + Q + L^T R L = (L - K)^T R (L - K),$$

because the left side minus the right side equals $A^T P + P A + Q - K^T R K$ after expanding with $B^T P = R K$, and $K^T R K = P G P$. Take $L = K_{k+1}$ and subtract this from (1) for $k + 1$. Since $K_{k+1} - K = R^{-1} B^T (P_k - P) = R^{-1} B^T E_k$, the right side is $E_k B R^{-1} R R^{-1} B^T E_k = E_k G E_k$, and (3) follows. As $A_{k+1}$ is Hurwitz and $E_k G E_k \ge 0$, Lemma 1 gives $E_{k+1} \ge 0$.

For the bound, let $\mathcal{L}_k(X) = A_k^T X + X A_k$. Then $E_{k+1} = -\mathcal{L}_{k+1}^{-1}(E_k G E_k)$ and $\|E_{k+1}\| \le \|\mathcal{L}_{k+1}^{-1}\| \|G\| \|E_k\|^2$. The matrices $A_{k+1} = A - G P_k$ converge to $A - G P$, which is Hurwitz, and $F \mapsto \|\mathcal{L}_F^{-1}\|$, with $\mathcal{L}_F(X) = F^T X + X F$, is continuous on the open set of Hurwitz matrices $F$. A convergent sequence of Hurwitz matrices whose limit is Hurwitz stays in a compact subset of that set, so $\|\mathcal{L}_{k+1}^{-1}\|$ is bounded by some $M$, and $c = M \|G\|$ works. $\square$

## Theorem

Under the assumptions above, Kleinman's iteration is well defined, every $A - B K_k$ is Hurwitz, $P_0 \ge P_1 \ge P_2 \ge \dots \ge P$, and $P_k$ converges to the stabilizing solution $P$ of the CARE with $\|P_k - P\| \le c \|P_{k-1} - P\|^2$. The implementation stops after at most `max_iter` steps, or when two successive matrices differ by at most `tol` times the size of the last one, which happens after finitely many steps because the sequence converges.

*Proof.* Lemma 3 gives well definedness and stability, Lemma 4 the monotone decrease, Lemma 5 the limit, Lemma 6 the lower bound $P_k \ge P$ for $k \ge 1$ (and for $k = 0$ from $P_0 \ge P_1$) and the quadratic rate. Termination: the loop runs at most `max_iter` times. $\blacksquare$

## The discrete-time version (Hewer)

Assume $(Q^{1/2}, A)$ detectable in the discrete sense (no $v \ne 0$ with $A v = \lambda v$, $|\lambda| \ge 1$, $Q v = 0$) and $A - B K_0$ Schur. Hewer's iteration solves $P_k = A_k^T P_k A_k + Q + K_k^T R K_k$ and sets $K_{k+1} = S_k^{-1} B^T P_k A$ with $S_k = R + B^T P_k B$. The same steps hold with these changes.

- Lemma 1 becomes: for $F$ Schur, $X = F^T X F + W$ has the unique solution $\sum_{j \ge 0} (F^T)^j W F^j$.
- Lemma 2 becomes $A_{k+1}^T P_k A_{k+1} + Q + K_{k+1}^T R K_{k+1} = P_k - D_k^T S_k D_k$. Proof: $f(L) = (A - B L)^T P_k (A - B L) + Q + L^T R L = L^T S_k L - L^T B^T P_k A - A^T P_k B L + A^T P_k A + Q$, and completing the square gives $f(L) = f(K_{k+1}) + (L - K_{k+1})^T S_k (L - K_{k+1})$. Put $L = K_k$, where $f(K_k) = P_k$.
- Lemma 3: for $A_{k+1} v = \lambda v$, the identity gives $(|\lambda|^2 - 1) v^* P_k v = -v^* Q v - (K_{k+1} v)^* R (K_{k+1} v) - (D_k v)^* S_k (D_k v)$, and $|\lambda| \ge 1$ leads to the same contradiction.
- Lemma 4: $P_k - P_{k+1} = A_{k+1}^T (P_k - P_{k+1}) A_{k+1} + D_k^T S_k D_k \ge 0$.
- Lemma 5 is the same, with the limit equation $P = (A - B K)^T P (A - B K) + Q + K^T R K$, $K = (R + B^T P B)^{-1} B^T P A$, which is the DARE.
- Lemma 6: with $S = R + B^T P B$, the DARE gives $(A - B L)^T P (A - B L) + Q + L^T R L = P + (L - K)^T S (L - K)$, so $E_{k+1} = A_{k+1}^T E_{k+1} A_{k+1} + (K_{k+1} - K)^T S (K_{k+1} - K)$. The gain $K_{k+1} = S_k^{-1} B^T P_k A$ is a smooth function of $P_k$ that equals $K$ at $P_k = P$, so $\|K_{k+1} - K\| \le c' \|E_k\|$ near the limit, and $\|E_{k+1}\| \le c \|E_k\|^2$.
