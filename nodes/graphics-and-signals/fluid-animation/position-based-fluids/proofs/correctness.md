---
title: The Newton step of one constraint and the linear momentum law of PBF
proves: [correctness]
status: full
---

We use the notation of the page.
All particles have the mass $m > 0$, and the arithmetic is exact real arithmetic.
The pairs $P$ of line L2 are unordered and fixed during the step.
The spiky kernel is radial, so $\nabla W_{ij}$ is parallel to $x^*_i - x^*_j$ and $\nabla W_{ji} = -\nabla W_{ij}$.
PBF runs a fixed number of passes and has no proof of convergence; the claims below hold for every run.

## The Newton step of one constraint

**Claim 1.** Let $\varepsilon = 0$ and let the gradient $\nabla C_i = (\nabla_{x_k} C_i)_k$ be nonzero. Among all moves $\Delta x = (\Delta x_k)_k$ with $C_i + \nabla C_i\cdot\Delta x = 0$, the shortest is $\Delta x_k = \lambda_i\nabla_{x_k} C_i$ with $\lambda_i = -C_i/\sum_k|\nabla_{x_k} C_i|^2$.

*Proof.*
The set of moves with $C_i + \nabla C_i\cdot\Delta x = 0$ is an affine hyperplane with normal $\nabla C_i$.
The point of a hyperplane closest to the origin lies along its normal, so $\Delta x = \lambda\nabla C_i$ for a scalar $\lambda$.
Then $C_i + \lambda|\nabla C_i|^2 = 0$ gives $\lambda = \lambda_i$. $\square$

With $\varepsilon > 0$, the same move with $\lambda_i = -C_i/(|\nabla C_i|^2 + \varepsilon)$ leaves the linear model at $C_i\,\varepsilon/(|\nabla C_i|^2 + \varepsilon)$, a fraction of $C_i$.

**Claim 2.** The move of line L6 is the sum over constraints of these moves: $\Delta x_i = \lambda_i\nabla_{x_i} C_i + \sum_j \lambda_j\nabla_{x_i} C_j$, plus the artificial pressure term.

*Proof.*
By the gradients of the page, $\lambda_i\nabla_{x_i} C_i = (m/\rho_0)\sum_j \lambda_i\nabla W_{ij}$.
For a neighbor $j$, $\nabla_{x_i} C_j = -(m/\rho_0)\nabla W_{ji} = (m/\rho_0)\nabla W_{ij}$.
The sum is $(m/\rho_0)\sum_j(\lambda_i + \lambda_j)\nabla W_{ij}$, which is line L6 without $s_{corr}$. $\square$

In the one-sided form, a constraint with $C_i \le 0$ has $\lambda_i = 0$ and adds no move.

## Linear momentum

**Claim 3.** With $g = 0$ and no walls, one step keeps $\sum_i m v_i$, for any number of passes, any $\varepsilon \ge 0$, any $s_{corr}$, either form of line L4 and any $c$.

*Proof.*
Let $X = \sum_i m x^*_i$.
In line L6 the pair $\{i, j\}$ adds $(m/\rho_0)s\,\nabla W_{ij}$ to $\Delta x_i$ and $(m/\rho_0)s\,\nabla W_{ji} = -(m/\rho_0)s\,\nabla W_{ij}$ to $\Delta x_j$, with the same scalar $s = \lambda_i + \lambda_j + s_{corr,ij}$, because $s_{corr}$ depends only on $|x^*_i - x^*_j|$.
So $\sum_i m\Delta x_i = 0$, and line L7 does not change $X$.
After line L1, $X = \sum_i m(x_i + \Delta t\,v_i)$.
By line L8, $\sum_i m v_i' = (X - \sum_i m x_i)/\Delta t = \sum_i m v_i$, the momentum after line L1, which equals the momentum before the step since $g = 0$.
In line L9, the pair adds $c(m/\rho_0)W(v_j - v_i)$ to $v_i$ and $c(m/\rho_0)W(v_i - v_j)$ to $v_j$, with the same $W$ for both, and the sum is 0. $\square$

## Angular momentum

The angular momentum is not kept exactly.
With $g = 0$, no walls and $c = 0$, the angular momentum after the step is $L' = \sum_i m\,x'_i\times v'_i$ with $x'_i = x^*_i$ and $v'_i = (x^*_i - x_i)/\Delta t$, so $L' = \sum_i m\,x_i\times x^*_i/\Delta t$.
Before the passes, the same formula with the predicted positions of line L1 gives $L$.
The difference is $\sum_i m\,x_i\times(\text{sum of the moves of }i)/\Delta t$.
A pair adds $(m/\rho_0)s\,m\,(x_i - x_j)\times\nabla W_{ij}/\Delta t$, and $\nabla W_{ij}$ is parallel to $x^*_i - x^*_j = x_i - x_j + \Delta t(v_i - v_j)$, so the term is $-(m/\rho_0)s\,m\,(v_i - v_j)\times\nabla W_{ij}$ and is not 0 in general. $\blacksquare$
