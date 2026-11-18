---
title: The gradient of the style-based IK objective is exact, each step decreases it, and without constraints the pose is the mean pose
proves: [correctness]
status: full
---

We use the notation of the page.
$E(x, y) = L_{IK}(x, y) + \frac{\lambda}{2} \lVert g(y) - p \rVert^2$, with $r = W (y - f(x))$ and $\sigma^2 = \sigma^2(x)$.
$K$ is symmetric positive definite, because the RBF kernel matrix is positive semidefinite and $\beta^{-1} I$ is positive definite.
The arithmetic is exact.

## The variance is positive

**Lemma 1.** $\sigma^2(x) \ge \beta^{-1} > 0$ for every $x$.

*Proof.*
Let $k_0$ be the vector of the RBF values $\alpha \exp(-\frac{\gamma}{2} \lVert x - x_j \rVert^2)$ and $G$ the RBF matrix of the training latents, so $K = G + \beta^{-1} I$.
If $x$ is not a training latent, then $k(x) = k_0$ and $k(x, x) = \alpha + \beta^{-1}$.
The matrix $\begin{pmatrix} \alpha & k_0^\top \\ k_0 & G \end{pmatrix}$ is an RBF kernel matrix, so it is positive semidefinite, and adding $\beta^{-1} I$ to its lower block gives $\begin{pmatrix} \alpha & k_0^\top \\ k_0 & K \end{pmatrix} \succeq 0$.
Its Schur complement $\alpha - k_0^\top K^{-1} k_0$ is therefore at least 0, and $\sigma^2 = \alpha - k_0^\top K^{-1} k_0 + \beta^{-1} \ge \beta^{-1}$.
The code uses $k(x, x) = \alpha + \beta^{-1}$ and $k(x) = k_0$ for every $x$, also at a training latent, which is the same formula, so the bound holds there too. $\square$

So $\ln \sigma^2$ and $1 / \sigma^2$ are smooth, and $E$ is a smooth function of $(x, y)$.

## The gradient

**Lemma 2.** With $a = K^{-1} k(x)$ and $\nabla k_j = -\gamma (x - x_j) k(x, x_j)$,
$$\nabla f_k = \sum_j (K^{-1} Y)_{jk} \nabla k_j, \qquad \nabla \sigma^2 = -2 \sum_j a_j \nabla k_j.$$

*Proof.*
$f_k = \mu_k + \sum_j (K^{-1} Y)_{jk} k_j(x)$ is linear in $k(x)$, which gives the first formula.
$\sigma^2 = \alpha + \beta^{-1} - k^\top K^{-1} k$, and the derivative of a quadratic form with the symmetric $K^{-1}$ is $2 (K^{-1} k)^\top \nabla k$.
The derivative of $\alpha \exp(-\frac{\gamma}{2} \lVert x - x_j \rVert^2)$ is $-\gamma (x - x_j)$ times the value. $\square$

**Theorem 1.** The gradient that `objective` returns is the gradient of $E$:
$$\nabla_y E = \frac{W r}{\sigma^2} + \lambda J^\top (g(y) - p), \qquad \nabla_x E = -\frac{(\nabla f)^\top W r}{\sigma^2} + \left(\frac{D}{2 \sigma^2} - \frac{\lVert r \rVert^2}{2 \sigma^4}\right) \nabla \sigma^2 + x.$$

*Proof.*
In $y$: $\nabla_y \frac{\lVert r \rVert^2}{2 \sigma^2} = W^\top r / \sigma^2 = W r / \sigma^2$, the other terms of $L_{IK}$ do not depend on $y$, and the gradient of $\frac{\lambda}{2} \lVert g(y) - p \rVert^2$ is $\lambda J^\top (g(y) - p)$.
In $x$: $r$ depends on $x$ through $-W f(x)$, so $\nabla_x \lVert r \rVert^2 = -2 (\nabla f)^\top W r$.
The quotient rule gives $\nabla_x \frac{\lVert r \rVert^2}{2 \sigma^2} = -\frac{(\nabla f)^\top W r}{\sigma^2} - \frac{\lVert r \rVert^2}{2 \sigma^4} \nabla \sigma^2$.
$\nabla_x \frac{D}{2} \ln \sigma^2 = \frac{D}{2 \sigma^2} \nabla \sigma^2$ and $\nabla_x \frac12 \lVert x \rVert^2 = x$.
For the planar chain, the end point is $g(y) = \sum_k \ell_k (\cos \theta_k, \sin \theta_k)$ with $\theta_k = y_1 + \cdots + y_k$, and $\partial \theta_k / \partial y_i = 1$ for $k \ge i$, so column $i$ of $J$ is $\sum_{k \ge i} \ell_k (-\sin \theta_k, \cos \theta_k)$, which is what `end_effector` returns. $\square$

## Each step decreases the objective

**Theorem 2.** Every accepted step decreases $E$, and the sequence of the values of $E$ is strictly decreasing until the method stops.

*Proof.*
If $\nabla E = 0$, the method stops at line L8.
Otherwise, the direction $d$ of line L6 has $d^\top \nabla E < 0$: either the BFGS direction has this property, or the code takes $d = -\nabla E$, for which $d^\top \nabla E = -\lVert \nabla E \rVert^2 < 0$.
$E$ is differentiable, so $E(z + t d) = E(z) + t d^\top \nabla E + o(t)$, and for every small enough $t > 0$, $E(z + t d) \le E(z) + 10^{-4} t d^\top \nabla E$, because $10^{-4} < 1$.
So the halving stops at some $t > 0$, unless $t$ falls below $10^{-16}$, in which case the method returns the current point without a step.
An accepted step satisfies $E(z + t d) \le E(z) + 10^{-4} t d^\top \nabla E < E(z)$. $\square$

The BFGS update keeps $H$ symmetric positive definite when $s^\top y_v > 0$, where $s$ is the step and $y_v$ the change of the gradient, and the code skips the update otherwise.
Then the BFGS direction is a descent direction, and the reset of line L6 only guards against rounding.

The method has no guarantee of a global minimum: $E$ is not convex, and the page shows two local minima for the same target.

## Without constraints, the pose is the mean pose

**Theorem 3.** Let $\lambda = 0$.
For a fixed $x$, the unique minimizer of $E(x, \cdot)$ is $y = f(x)$, and $(x^*, y^*)$ minimizes $E$ if and only if $y^* = f(x^*)$ and $x^*$ minimizes $h(x) = \frac{D}{2} \ln \sigma^2(x) + \frac12 \lVert x \rVert^2$.
At a stationary point of $E$, $y = f(x)$ and $\nabla h(x) = 0$.

*Proof.*
For a fixed $x$, $E(x, y) = \frac{\lVert W (y - f(x)) \rVert^2}{2 \sigma^2} + h(x)$, and the first term is at least 0, with equality exactly at $y = f(x)$, because $W$ is invertible.
So $\min_y E(x, y) = h(x)$, and $\min_{x, y} E = \min_x h$, with the minimizers as stated.
At a stationary point, $\nabla_y E = W r / \sigma^2 = 0$, so $r = 0$ and $y = f(x)$.
Then $\nabla_x E = \frac{D}{2 \sigma^2} \nabla \sigma^2 + x = \nabla h(x)$, which is 0. $\square$

The test compares the result of the solver with the best point of a grid search on $h$.

## The penalty

**Theorem 4.** Let $(x_1, y_1)$ and $(x_2, y_2)$ be global minimizers of $E$ for $\lambda_1 < \lambda_2$, and $c_i = \lVert g(y_i) - p \rVert^2$.
Then $c_2 \le c_1$.

*Proof.*
Write $E_\lambda = L + \frac{\lambda}{2} c$.
By the optimality of each point, $L_1 + \frac{\lambda_1}{2} c_1 \le L_2 + \frac{\lambda_1}{2} c_2$ and $L_2 + \frac{\lambda_2}{2} c_2 \le L_1 + \frac{\lambda_2}{2} c_1$.
Adding the two inequalities gives $\frac{\lambda_1 - \lambda_2}{2} (c_1 - c_2) \le 0$, and $\lambda_1 < \lambda_2$ gives $c_1 \ge c_2$. $\square$

## The check value

Take the latents $-1$ and $1$, the poses $(0, 0, 0)$ and $(1, 2, 3)$, $\alpha = \gamma = 1$ and $\beta = 100$.
Then $\mu = (0.5, 1, 1.5)$, the centered poses are $\mp (0.5, 1, 1.5)$, and $K = \begin{pmatrix} 1.01 & e^{-2} \\ e^{-2} & 1.01 \end{pmatrix}$, since $\lVert x_1 - x_2 \rVert^2 = 4$.
At $x = 0$, $k(0) = (e^{-1/2}, e^{-1/2})$, which is an eigenvector of $K$ with the eigenvalue $1.01 + e^{-2}$.
So $K^{-1} k(0) = k(0) / (1.01 + e^{-2})$, which has two equal entries, and $Y^\top K^{-1} k(0)$ is a multiple of $-(0.5, 1, 1.5) + (0.5, 1, 1.5) = 0$, so $f(0) = \mu$.
$k(0)^\top K^{-1} k(0) = 2 e^{-1} / (1.01 + e^{-2})$, so $\sigma^2(0) = 1.01 - 2 e^{-1} / (1.01 + e^{-2}) = 1.01 - 0.735759 / 1.145335 \approx 0.367604$.
