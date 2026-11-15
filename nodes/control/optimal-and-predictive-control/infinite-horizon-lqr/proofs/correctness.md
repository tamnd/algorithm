---
title: The limit of the finite-horizon Riccati recursion is the stabilizing solution, and its gain is optimal on the infinite horizon
proves: [correctness]
status: full
---

Discrete time is treated in full; the continuous case follows the same three steps and is given at the end. Let $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$, $Q = Q^T \ge 0$, $R = R^T > 0$, and let $C = Q^{1/2}$, so $Q = C^T C$. Assume $(A, B)$ is stabilizable and $(C, A)$ is detectable. The plant is $x_{k+1} = A x_k + B u_k$ and the cost is $J(x_0, u) = \sum_{k \ge 0} (x_k^T Q x_k + u_k^T R u_k)$, which may be $+\infty$.

For $P = P^T \ge 0$ write $S(P) = R + B^T P B$, $K(P) = S(P)^{-1} B^T P A$ and

$$F(P) = Q + A^T P A - A^T P B K(P) = Q + K^T R K + (A - B K)^T P (A - B K), \qquad K = K(P).$$

The two forms are equal by Lemma 2 of the [finite-horizon proof](/finite-horizon-lqr/). The algorithm computes $P_0 = 0$ and $P_{j+1} = F(P_j)$. By that proof, $x^T P_j x$ is the minimum of the cost of horizon $j$ with terminal weight 0.

## Lemma 1: finite cost and detectability force $x_k \to 0$

If $J(x_0, u) < \infty$, then $x_k \to 0$.

*Proof.* Finite cost gives $\sum_k |C x_k|^2 < \infty$ and $\sum_k u_k^T R u_k < \infty$, so $C x_k \to 0$ and $u_k \to 0$, and both sequences are square summable. By detectability there is $L$ with $A - L C$ Schur. Write the plant as $x_{k+1} = (A - L C) x_k + w_k$ with $w_k = L C x_k + B u_k$. Then $w_k$ is square summable, hence $w_k \to 0$. The solution is $x_k = (A - LC)^k x_0 + \sum_{i < k} (A - LC)^{k-1-i} w_i$. Since $\|(A - LC)^k\| \le c \theta^k$ for some $c$ and $\theta < 1$, the first term tends to 0, and the second is the convolution of a summable sequence with a sequence that tends to 0, which tends to 0. $\square$

## Lemma 2: a stabilizing solution gives the optimal cost

Let $P = P^T \ge 0$ satisfy $P = F(P)$, and let $K = K(P)$ with $A - B K$ Schur. Then for every $x_0$, $\min_u J(x_0, u) = x_0^T P x_0$, attained by $u_k = -K x_k$ and by no other input sequence.

*Proof.* For any $x$ and $u$, completing the square as in Lemma 1 of the finite-horizon proof gives

$$x^T Q x + u^T R u + (A x + B u)^T P (A x + B u) = x^T F(P) x + (u + K x)^T S(P) (u + K x) = x^T P x + (u + K x)^T S(P) (u + K x).$$

Sum this from $k = 0$ to $N - 1$ along a trajectory. The terms $x_k^T P x_k$ telescope:

$$\sum_{k=0}^{N-1} (x_k^T Q x_k + u_k^T R u_k) = x_0^T P x_0 - x_N^T P x_N + \sum_{k=0}^{N-1} (u_k + K x_k)^T S(P) (u_k + K x_k).$$

If $J(x_0, u) = \infty$ there is nothing to prove. Otherwise $x_N \to 0$ by Lemma 1, so letting $N \to \infty$,

$$J(x_0, u) = x_0^T P x_0 + \sum_{k \ge 0} (u_k + K x_k)^T S(P) (u_k + K x_k) \ge x_0^T P x_0,$$

because $S(P) > 0$. The feedback $u_k = -K x_k$ gives a Schur closed loop, so $x_k \to 0$ geometrically and its cost is finite; for it the sum is 0. Equality for another sequence would need $u_k = -K x_k$ for every $k$. $\square$

In particular there is at most one stabilizing solution: two of them would both equal the optimal cost matrix.

## Lemma 3: the recursion from 0 converges

The sequence $P_j$ is nondecreasing, there is a fixed matrix $M$ with $0 \le P_j \le M$ for all $j$, and the sequence converges to a matrix $P_\infty \ge 0$ with $P_\infty = F(P_\infty)$.

*Proof.* Monotone: the cost of horizon $j + 1$ restricted to its first $j$ steps is a cost of horizon $j$ with terminal weight 0, and the last term is nonnegative. Minimizing gives $x^T P_{j+1} x \ge x^T P_j x$ for every $x$.

Bounded: by stabilizability there is $K_s$ with $A - B K_s$ Schur. The feedback $u = -K_s x$ has the finite infinite-horizon cost $x^T M x$, where $M = \sum_k ((A - BK_s)^T)^k (Q + K_s^T R K_s) (A - BK_s)^k$ converges. Its cost over the first $j$ steps is at most $x^T M x$ and at least $x^T P_j x$, so $P_j \le M$.

Converges: for each $x$, $x^T P_j x$ is nondecreasing and bounded, so it converges. By polarization, $x^T P y = \frac{1}{4}((x + y)^T P (x + y) - (x - y)^T P (x - y))$ for symmetric $P$, so every entry of $P_j$ converges, and $P_j \to P_\infty$ with $0 \le P_\infty \le M$.

Fixed point: $F$ is continuous on the set of positive semidefinite matrices, because $S(P) \ge R > 0$ is invertible there and inversion is continuous. Taking the limit in $P_{j+1} = F(P_j)$ gives $P_\infty = F(P_\infty)$. $\square$

## Lemma 4: the limit stabilizes

Let $P = P^T \ge 0$ satisfy $P = F(P)$ and let $K = K(P)$. Then $A - B K$ is Schur.

*Proof.* Let $A_K = A - B K$, and let $A_K v = \lambda v$ with $v \ne 0$ complex. The second form of $F$ gives $P = Q + K^T R K + A_K^T P A_K$. Multiply by $v^*$ on the left and $v$ on the right:

$$v^* P v = v^* Q v + v^* K^T R K v + |\lambda|^2 v^* P v, \qquad \text{so} \qquad (1 - |\lambda|^2)\, v^* P v = |C v|^2 + (K v)^* R (K v).$$

Suppose $|\lambda| \ge 1$. The left side is at most 0 and the right side is at least 0, so both are 0. Then $C v = 0$ and, since $R > 0$, $K v = 0$. So $A v = A_K v + B K v = \lambda v$ with $C v = 0$ and $|\lambda| \ge 1$. By the [PBH test](/popov-belevitch-hautus-test/) for detectability, no such $v$ exists. So every eigenvalue of $A_K$ has $|\lambda| < 1$. $\square$

## Theorem

Under the hypotheses, the recursion from $P_0 = 0$ converges to the unique stabilizing solution $P$ of the DARE, $K(P)$ is the optimal constant gain, and $x_0^T P x_0$ is the optimal cost of the infinite horizon.

*Proof.* Lemma 3 gives the limit $P_\infty$, Lemma 4 shows that it is stabilizing, and Lemma 2 shows that it gives the optimal cost and the optimal feedback. Uniqueness follows from Lemma 2. $\blacksquare$

**What the code checks.** The loop stops after finitely many passes, when $\|P_{j+1} - P_j\|_F \le \text{tol}\, \|P_{j+1}\|_F$, so the returned matrix is an approximation of $P_\infty$. Line L8 tests the closed loop with the computed gain. If the hypotheses fail, Lemma 4 can fail: for $a = 2$, $b = 1$, $q = 0$, $r = 1$, $P_j = 0$ for all $j$ and $A - BK = 2$, which is what the code reports.

## Continuous time

The same steps work with $\dot x = A x + B u$ and $J = \int_0^\infty (x^T Q x + u^T R u)\, dt$, with $G = B R^{-1} B^T$ and $\mathcal{R}(P) = A^T P + P A - P G P + Q$.

1. Finite cost forces $x(t) \to 0$. With $L$ such that $A - L C$ is Hurwitz, $x$ solves $\dot x = (A - LC) x + w$ with $w = L C x + B u \in L^2$, so $x \in L^2$, and $\dot x$ is in $L^2$ as well. A function with $x, \dot x \in L^2$ satisfies $|x(t)|^2 = |x(s)|^2 + 2 \int_s^t x^T \dot x$, so $|x(t)|^2$ has a limit, which must be 0 because $x \in L^2$.
2. If $\mathcal{R}(P) = 0$, $P \ge 0$ and $A - G P$ is Hurwitz, then Lemma 4 of the finite-horizon proof gives $\int_0^T (x^T Q x + u^T R u)\, dt = x_0^T P x_0 - x(T)^T P x(T) + \int_0^T (u + K x)^T R (u + K x)\, dt$ with $K = R^{-1} B^T P$. Let $T \to \infty$ and use step 1.
3. The solution $P(\tau)$ of $dP/d\tau = \mathcal{R}(P)$, $P(0) = 0$, is the cost matrix of horizon $\tau$. It is nondecreasing in $\tau$ and bounded by the cost of a stabilizing gain, so it converges to some $P_\infty$. Its derivative $\mathcal{R}(P(\tau))$ converges to $\mathcal{R}(P_\infty)$; if this limit were not 0, $P(\tau)$ would grow without bound in some entry, so $\mathcal{R}(P_\infty) = 0$.
4. With $A_K = A - B K$, the CARE reads $A_K^T P + P A_K = -(Q + K^T R K)$. If $A_K v = \lambda v$, then $2 \operatorname{Re}(\lambda)\, v^* P v = -|C v|^2 - (Kv)^* R (Kv)$. If $\operatorname{Re} \lambda \ge 0$, both terms on the right vanish, so $C v = 0$ and $A v = \lambda v$, which contradicts detectability. So $A - B K$ is Hurwitz.

The implementation integrates step 3 with RK4 and stops on the CARE residual. Its last check, that $A - BK$ is Hurwitz, plays the role of Lemma 4 for the computed matrix.
