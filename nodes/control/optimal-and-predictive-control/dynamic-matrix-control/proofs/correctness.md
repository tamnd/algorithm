---
title: The DMC prediction is exact for a step-response plant with a constant output disturbance, the move is the least-squares optimum, and a convergent loop has no offset
proves: [correctness]
status: full
---

The model is the step response $s_1, \dots, s_{N_s}$, extended by $s_i = s_{N_s}$ for $i > N_s$. Write $\Delta u(k) = u(k) - u(k-1)$ and assume the input was constant before time 0, so only finitely many moves are nonzero. The model output is

$$\hat y(k) = \sum_{j \ge 1} s_j \, \Delta u(k - j).$$

This is exactly the output of a linear time-invariant plant whose step response is the extended sequence: a step of size $\Delta u(k-j)$ at time $k - j$ adds $s_j \Delta u(k-j)$ at time $k$, by superposition. A stable plant whose step response has settled after $N_s$ samples is of this form up to the truncation error $|s_i - s_{N_s}|$ for $i > N_s$.

## Lemma 1: the prediction

Suppose the plant output is $y(k) = \hat y(k) + d$ with a constant $d$ (the model is exact up to a constant output disturbance). Let $f_i$ be computed as in lines L4 and L5:

$$d(k) = y(k) - \hat y(k), \qquad f_i = \sum_{j \ge 1} s_{i + j} \, \Delta u(k - j) + d(k), \qquad i = 1, \dots, P.$$

Then for any future moves $\Delta u(k), \dots, \Delta u(k + M - 1)$, with $\Delta u(k + j) = 0$ for $j \ge M$,

$$y(k + i) = f_i + \sum_{j=0}^{M-1} S_{i, j+1} \, \Delta u(k + j), \qquad S_{i,j} = s_{i - j + 1} \ (i \ge j), \ S_{i, j} = 0 \ (i < j).$$

*Proof.* $d(k) = d$ by the assumption. Split the sum for $y(k+i) = \hat y(k+i) + d$ into the moves before time $k$ and the moves from time $k$ on. A past move $\Delta u(k - j)$, $j \ge 1$, is $i + j$ samples old at time $k + i$, so it contributes $s_{i+j} \Delta u(k-j)$; these terms and $d$ make up $f_i$. A future move $\Delta u(k + j)$ is $i - j$ samples old at time $k + i$; it contributes $s_{i-j} \Delta u(k+j)$ if $i - j \ge 1$ and nothing otherwise. With the column index $j + 1$ this is $S_{i, j+1}$. $\square$

The code stores the last $N_s$ moves and the sum of the older ones. A move older than $N_s$ samples has the coefficient $s_{N_s}$ at every horizon, so the stored sum times $s_{N_s}$ is its exact contribution.

## Lemma 2: the move

Let $e = r - f$ with $r$ the setpoint vector. For $\lambda > 0$, or for $\lambda = 0$ when $S$ has full column rank, the cost

$$J(\Delta U) = \|e - S \Delta U\|^2 + \lambda \|\Delta U\|^2$$

has the unique minimizer $\Delta U^* = (S^T S + \lambda I)^{-1} S^T e$.

*Proof.* $J$ is a quadratic with Hessian $2(S^T S + \lambda I)$, which is positive definite under either condition: $v^T (S^T S + \lambda I) v = \|S v\|^2 + \lambda \|v\|^2 > 0$ for $v \ne 0$. So $J$ is strictly convex, and its unique minimizer is the zero of the gradient $2(S^T S + \lambda I) \Delta U - 2 S^T e$. $\square$

Lines L1 and L2 compute the matrix $(S^T S + \lambda I)^{-1} S^T$ column by column, and line L6 applies its first row $K$ to $e$. So the first move is the first entry of $\Delta U^*$, and by Lemma 1 it is the first move of the sequence that minimizes the predicted tracking error plus the move penalty.

The full-rank condition holds when $s_1 \ne 0$. If the plant has a dead time of $\tau$ samples, so $s_1 = \dots = s_\tau = 0$, then $S$ has full column rank when $P \ge M + \tau$ and $s_{\tau + 1} \ne 0$, because the rows $\tau + 1, \dots, \tau + M$ form a lower triangular block with $s_{\tau+1}$ on the diagonal.

## Lemma 3: unconstrained DMC is a linear time-invariant controller

$K$ does not depend on $k$. $f$ is a fixed linear function of $y(k)$ and of the past moves, so $\Delta u(k)$ is a fixed linear function of $r$, $y(k)$ and the past moves. The controller is therefore a linear time-invariant system from $(r, y)$ to $u$, with $\Delta u(k) = K (r \mathbf{1} - f)$. Its stability with the plant is a property of the tuning $(P, M, \lambda)$ and must be checked; DMC itself gives no guarantee.

## Theorem: zero offset

Assume the setpoint $r$ and the output disturbance are constant from some time on, the plant is linear (not necessarily equal to the model), and the closed loop is asymptotically stable, so every signal converges. Assume also $K \mathbf{1} = \sum_i K_i \ne 0$. Then $y(k) \to r$.

*Proof.* The input converges, so $\Delta u(k) \to 0$. Since the controller uses only the last $N_s$ moves individually and the sum of the older ones, and the moves tend to 0 while their running sum $u(k) - u(-1)$ converges, the model output $\hat y(k)$ converges to some $\hat y_\infty$, and every term $\sum_{j \ge 1} s_{i+j} \Delta u(k-j)$ of the free response converges to the same limit $\hat y_\infty$ (the difference between them involves only the last $N_s$ moves, which tend to 0). The measured output converges to some $y_\infty$, so $d(k) \to y_\infty - \hat y_\infty$, and therefore $f_i \to y_\infty$ for every $i$. Passing to the limit in line L6,

$$0 = \lim \Delta u(k) = K (r \mathbf{1} - y_\infty \mathbf{1}) = (K \mathbf{1}) (r - y_\infty).$$

Since $K \mathbf{1} \ne 0$, $y_\infty = r$. $\square$

The argument does not use the plant model: any mismatch of gain or dynamics is absorbed into $d(k)$. This is the integral action of DMC. For $M = 1$ the condition $K \mathbf{1} \ne 0$ is $\sum_{i=1}^P s_i \ne 0$, which holds for every step response with nonnegative entries that are not all 0. For $M > 1$ it is read off the computed gain; in the example of the page $K \mathbf{1} = 1.8422$.
