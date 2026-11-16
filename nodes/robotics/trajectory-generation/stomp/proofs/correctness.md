---
title: The noise of STOMP has covariance proportional to the inverse of the smoothness matrix, each update is bounded by the noise, and the returned trajectory is never worse than the start
proves: [correctness]
status: full
---

We use the notation of the page and of the code. There are $n$ free waypoints $\theta_1, \dots, \theta_n \in \mathbb R^2$ between the fixed ends $q_0$ and $q_{n+1}$. $A$ is the $n \times n$ tridiagonal matrix with $-2$ on the diagonal and $1$ next to it, and $R = A^{\mathsf T} A$. The total cost is $Q(\theta) = \sum_t q(\theta_t) + \frac w2 \sum_t \|\theta_{t-1} - 2\theta_t + \theta_{t+1}\|^2$ with $\theta_0 = q_0$ and $\theta_{n+1} = q_{n+1}$, for an arbitrary state cost $q$. STOMP gives no convergence guarantee. The statements below are what can be proved about one iteration and about the returned trajectory.

## Step 1: the noise has covariance $\sigma^2 R^{-1}$

$A$ is nonsingular: $-A$ has eigenvalues $2 - 2\cos(k\pi/(n+1)) > 0$ for $k = 1, \dots, n$. Line L3 draws $z \sim N(0, I_n)$ for each coordinate and sets $\varepsilon = \sigma A^{-1} z$. A linear map of a Gaussian vector is Gaussian, with mean $0$ and covariance

$$\sigma^2 A^{-1} I (A^{-1})^{\mathsf T} = \sigma^2 (A^{\mathsf T} A)^{-1} = \sigma^2 R^{-1}.$$

So the noise is a zero-mean Gaussian whose density is proportional to $\exp(-\frac{1}{2\sigma^2}\varepsilon^{\mathsf T} R \varepsilon)$: noise with a large sum of squared second differences is unlikely. The two coordinates are independent. $\square$

## Step 2: the entries of $R^{-1}$ and of $M$ are positive

$-A$ is a symmetric, positive definite matrix with nonpositive entries off the diagonal and an irreducible (connected) pattern, so its inverse has only positive entries (a standard property of such M-matrices; it also follows from the explicit inverse $(-A)^{-1}_{ij} = \min(i,j)(n+1-\max(i,j))/(n+1)$, which one checks by multiplying). Then $R^{-1} = A^{-1} A^{-1} = (-A)^{-1}(-A)^{-1}$ has positive entries too. The code builds $M$ by dividing column $j$ of $R^{-1}$ by $n$ times its largest entry, so $0 < M_{ij} \le 1/n$ for all $i, j$, and each column has an entry equal to $1/n$. $\square$

## Step 3: the weights

For one waypoint $t$, line L6 sets $P_k = e^{-S_k/\lambda} / \sum_j e^{-S_j/\lambda}$ with $\lambda > 0$. The code subtracts $\min_j S_j$ first; this multiplies numerator and denominator by the same factor and does not change $P$.

(a) $P_k > 0$ and $\sum_k P_k = 1$.

(b) Adding the same constant to all $S_k$ does not change $P$ (the same argument as for the subtraction of the minimum).

(c) If $S_k < S_l$ then $P_k > P_l$: the cheaper sample gets more weight.

(d) If all $S_k$ are equal, $P_k = 1/K$ for all $k$.

(e) As $\lambda \to 0$, $P$ tends to the uniform distribution on the set of samples with the smallest cost: for such a sample, $e^{-(S_k - \min S)/\lambda} = 1$, and for the others it tends to $0$. $\square$

## Step 4: one update is bounded by the noise

Fix a coordinate. By line L7, $\tilde\delta_t = \sum_k P_{k,t}\, \varepsilon_{k,t}$ is a convex combination of the noise values at waypoint $t$ (Step 3(a)), so $|\tilde\delta_t| \le \max_k |\varepsilon_{k,t}|$. Line L8 adds $(M\tilde\delta)_i = \sum_j M_{ij} \tilde\delta_j$ to waypoint $i$. By Step 2,

$$|(M\tilde\delta)_i| \le \sum_{j=1}^n \frac1n |\tilde\delta_j| \le \max_{j,k} |\varepsilon_{k,j}|.$$

So in one iteration no coordinate of any waypoint moves by more than the largest noise value drawn in that iteration. The ends $q_0$ and $q_{n+1}$ are not variables and never move. $\square$

## Step 5: with no information in the costs, the expected update is zero

If at every waypoint all $K$ samples have the same state cost, then $P_{k,t} = 1/K$ by Step 3(d), and $\tilde\delta_t$ is the mean of $K$ independent draws with mean $0$. So the expected update $E[M\tilde\delta]$ is $0$, but the update itself is a nonzero random vector with covariance $\frac{\sigma^2}{K} M R^{-1} M^{\mathsf T}$ per coordinate. Repeated over many iterations, the iterate performs a random walk. In particular the iterates do not converge, and the smoothness part of $Q$, which line L6 never sees, can grow. $\square$

## Step 6: the returned trajectory

**Theorem.** Let $\theta^{(0)}$ be the start and $\theta^{(1)}, \dots, \theta^{(I)}$ the iterates after each pass of lines L2 to L8. The trajectory returned by line L10 is an iterate $\theta^{(i^*)}$ with

$$Q(\theta^{(i^*)}) = \min_{0 \le i \le I} Q(\theta^{(i)}) \le Q(\theta^{(0)}).$$

*Proof.* By induction on the number of passes, after pass $i$ the stored trajectory is an iterate among $\theta^{(0)}, \dots, \theta^{(i)}$ with the smallest $Q$. This holds before the loop, where the stored trajectory is $\theta^{(0)}$. Line L9 replaces it by $\theta^{(i+1)}$ exactly when $Q(\theta^{(i+1)})$ is smaller, which keeps the invariant. At the end, take $i = I$; the inequality is the case $i = 0$ of the minimum. $\blacksquare$

## What is not proved

There is no statement that $Q$ decreases from one iterate to the next, that the iterates converge, or that the result is free of collision. Step 5 shows that the iterates keep moving at random once the state cost is flat near them, and the example on the page shows $Q$ of the iterates going up and down. The weighted average of line L7 is a stochastic estimate of a descent direction only when the noise is small and the costs vary across the samples; the method is local, like the other trajectory optimizers. The choice of $K$, $\sigma$, $\lambda$ and $w$ is a matter of tuning, not of this proof.
