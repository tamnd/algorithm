---
title: The Diophantine predictor of GPC is the optimal predictor of the CARIMA model, the move is the least-squares optimum, and the law is an RST controller with unit steady-state gain
proves: [correctness]
status: full
---

Polynomials are in the backward shift $q^{-1}$. The model is

$$A(q^{-1})\, y(t) = B(q^{-1})\, u(t-1) + \frac{e(t)}{\Delta}, \qquad \Delta = 1 - q^{-1},$$

with $A$ monic of degree $n_a$, $B$ of degree $n_b$, and $e$ a zero-mean white noise. Write $\tilde A = \Delta A$, which is monic of degree $n_a + 1$, and $\Delta u(t) = u(t) - u(t-1)$. Multiplying the model by $\Delta$ gives

$$\tilde A\, y(t) = B\, \Delta u(t-1) + e(t). \tag{1}$$

## Lemma 1: the Diophantine identity

For each $j \ge 1$ there are unique polynomials $E_j$ of degree at most $j - 1$ and $F_j$ of degree at most $n_a$ with

$$1 = E_j \tilde A + q^{-j} F_j.$$

$E_j$ is the first $j$ terms of the power series $1 / \tilde A$, and $F_j(1) = 1$.

*Proof.* Since $\tilde A$ is monic, $1/\tilde A$ is a power series $\sum_{i \ge 0} c_i q^{-i}$. Let $E_j = \sum_{i < j} c_i q^{-i}$. Then $1 - E_j \tilde A = \tilde A \sum_{i \ge j} c_i q^{-i}$ has no terms of order below $j$, and it is a polynomial of degree at most $j - 1 + n_a + 1 = j + n_a$. So it equals $q^{-j} F_j$ with $\deg F_j \le n_a$. Uniqueness: if $E \tilde A + q^{-j} F = 0$ with $\deg E < j$, then $E \tilde A$ has no terms of order below $j$; as $\tilde A$ has the constant term 1, the lowest nonzero term of $E$ would give a term of the same order in $E \tilde A$, so $E = 0$ and then $F = 0$. Finally, $\tilde A(1) = 0$ because of the factor $\Delta$, so setting $q^{-1} = 1$ gives $F_j(1) = 1$. $\square$

The routine `diophantine` is this long division: it subtracts $c_i q^{-i} \tilde A$ from the remainder for $i = 0, \dots, j - 1$ and reads $F_j$ from what is left (line L2).

## Lemma 2: the predictor

Let $G_j = E_j B$ (line L3). Then

$$y(t + j) = G_j\, \Delta u(t + j - 1) + F_j\, y(t) + E_j\, e(t + j).$$

The last term involves only $e(t+1), \dots, e(t+j)$, which are independent of the data up to time $t$. So $\hat y(t + j \mid t) = G_j\, \Delta u(t + j - 1) + F_j\, y(t)$ is the minimum mean square error predictor of $y(t + j)$ given the data up to $t$ and the future moves, and it is exact when $e$ is zero after time $t$.

*Proof.* Multiply (1), written at time $t + j$, by $E_j$ and use $E_j \tilde A = 1 - q^{-j} F_j$:

$$y(t + j) - F_j\, y(t) = E_j B\, \Delta u(t + j - 1) + E_j\, e(t + j).$$

$E_j$ has degree at most $j - 1$, so $E_j e(t+j)$ is a combination of $e(t+1), \dots, e(t+j)$. Given the past, the best predictor in mean square is the conditional mean, which removes exactly this term. $\square$

## Lemma 3: the split into forced and free response

The first $j$ coefficients of $G_j$ are $g_0, \dots, g_{j-1}$, the first coefficients of the power series $B / \tilde A$, which do not depend on $j$. Hence

$$\hat y(t + j \mid t) = \sum_{l=0}^{j-1} g_{j-1-l}\, \Delta u(t + l) + f_j, \qquad f_j = F_j\, y(t) + \sum_{i \ge j} G_{j,i}\, \Delta u(t + j - 1 - i).$$

*Proof.* $G_j = E_j B$ and $E_j$ agrees with $1/\tilde A$ up to order $j - 1$, so $G_j$ agrees with $B / \tilde A$ up to order $j - 1$. The coefficient $G_{j,i}$ multiplies $\Delta u(t + j - 1 - i)$. For $i \le j - 1$ this is a move at time $t + l$ with $l = j - 1 - i \ge 0$, a decision variable; for $i \ge j$ it is a move before time $t$, a known value. $\square$

The coefficients $g_i$ are the step response of the plant model $q^{-1} B / A$: the response of $y(t + 1 + i)$ to a unit step of $u$ at time $t$. The free response $f_j$ is computed by the code from the stored outputs and moves (line L5). Collecting $j = N_1, \dots, N_2$ gives $\hat y = G \Delta U + f$, with $G_{j, l} = g_{j-1-l}$ for $l \le j - 1$ and 0 otherwise.

## Lemma 4: the move

For $\lambda > 0$, or for $\lambda = 0$ when $G$ has full column rank, the cost $\|w \mathbf{1} - G \Delta U - f\|^2 + \lambda \|\Delta U\|^2$ has the unique minimizer $\Delta U^* = (G^T G + \lambda I)^{-1} G^T (w \mathbf{1} - f)$.

*Proof.* The Hessian $2 (G^T G + \lambda I)$ is positive definite under either condition, so the cost is strictly convex, and the minimizer is the zero of its gradient. $\square$

Line L4 stores the first row $K$ of $(G^T G + \lambda I)^{-1} G^T$, and line L6 computes $\Delta u(t) = K (w \mathbf{1} - f)$, the first entry of $\Delta U^*$.

## Theorem 1: the RST form and the steady-state gain

Write $K = (k_{N_1}, \dots, k_{N_2})$. The control law of line L6 is

$$R(q^{-1})\, \Delta u(t) = T\, w - S(q^{-1})\, y(t), \qquad S = \sum_j k_j F_j, \qquad T = \sum_j k_j, \qquad R = 1 + \sum_j k_j \sum_{i \ge j} G_{j,i}\, q^{-(1 + i - j)}.$$

With the model as the plant, the closed loop satisfies $P_c\, y(t) = q^{-1} B T\, w(t) + R\, e(t)$ with $P_c = \tilde A R + q^{-1} B S$. Moreover $S(1) = T$, so if $P_c$ has all its roots (as a polynomial in $z = q$) inside the unit circle, a constant setpoint gives $y \to w$ with no offset, also under a constant load disturbance and under model error that keeps the loop Schur.

*Proof.* Substitute the formula of $f_j$ from Lemma 3 into $\Delta u(t) = \sum_j k_j (w - f_j)$ and move the terms with past moves to the left. The move $\Delta u(t + j - 1 - i)$ with $i \ge j$ is $q^{-(1 + i - j)} \Delta u(t)$, which gives $R$; the output terms give $S$. For the closed loop, multiply (1) by $R$ and the control law by $q^{-1} B$, and add: $\tilde A R y = B R \Delta u(t-1) + R e$ and $B R \Delta u(t-1) = q^{-1} B (T w - S y)$, which gives $P_c y = q^{-1} B T w + R e$. By Lemma 1, $S(1) = \sum_j k_j F_j(1) = \sum_j k_j = T$. At $z = 1$, $\tilde A(1) = 0$, so the steady-state gain from $w$ to $y$ is $B(1) T / (B(1) S(1)) = 1$ when $B(1) \ne 0$ and $T \ne 0$. A constant load $v$ added to the output equation enters as $\Delta v$, which is 0 after one step, so it leaves no offset. For a plant $A_p y = B_p u(t-1)$ different from the model, the same law gives $(\Delta A_p R + q^{-1} B_p S) y = q^{-1} B_p T w$; at $z = 1$ the first term vanishes again because of $\Delta$, so the gain is still $B_p(1) T / (B_p(1) S(1)) = 1$ whenever this loop is Schur. $\square$

The theorem says nothing about the location of the roots of $P_c$. GPC with arbitrary horizons can give an unstable loop; the horizons and $\lambda$ must be chosen and the roots checked. Results that guarantee stability for special choices of the horizons are in the GPC literature and are not used here.
