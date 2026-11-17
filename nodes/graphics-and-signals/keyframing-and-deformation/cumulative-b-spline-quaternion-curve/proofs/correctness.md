---
title: The cumulative B-spline quaternion curve is a C2 curve of unit quaternions
proves: [correctness]
status: full
---

We use the notation of the page.
Quaternions are in the Hamilton convention, scalar first.
For a pure quaternion $\omega = (0, \varphi\hat u)$ with a unit vector $\hat u$, $\exp(x\omega) = (\cos x\varphi, \sin x\varphi\,\hat u)$ for real $x$, which is a unit quaternion and a smooth function of $x$.
The uniform cubic B-splines $B_0, \dots, B_{n-1}$ are $C^2$ piecewise cubics on the knots $\dots, -1, 0, 1, \dots$, numbered so that on $[j, j + 1]$ the active ones are $B_j, \dots, B_{j+3}$, with $B_{j+k}(j + u) = b_k(u)$ for

$$b_0 = \tfrac16(1 - u)^3, \quad b_1 = \tfrac16(3u^3 - 6u^2 + 4), \quad b_2 = \tfrac16(-3u^3 + 3u^2 + 3u + 1), \quad b_3 = \tfrac16 u^3.$$

They sum to 1 on $[0, n - 3]$.

## The cumulative basis

**Lemma 1.** Let $\tilde B_i = \sum_{l \ge i} B_l$. On $[j, j + 1]$, $\tilde B_i = 1$ for $i \le j$, $\tilde B_i = 0$ for $i \ge j + 4$, and $\tilde B_{j+k}(j + u) = \sum_{l \ge k} b_l(u)$ for $k = 1, 2, 3$, which gives the three polynomials $\tilde B_1, \tilde B_2, \tilde B_3$ of the page.

*Proof.*
On $[j, j + 1]$ only $B_j, \dots, B_{j+3}$ are nonzero.
For $i \le j$ the sum contains all of them, so it is 1.
For $i \ge j + 4$ it contains none of them.
For $i = j + k$ it is $\sum_{l = k}^{3} b_l$.
Adding the polynomials gives $b_3 = \frac16u^3$, $b_2 + b_3 = \frac16(1 + 3u + 3u^2 - 2u^3)$ and $b_1 + b_2 + b_3 = 1 - b_0 = \frac16(5 + 3u - 3u^2 + u^3)$. $\square$

**Lemma 2.** Each $\tilde B_i$ is $C^2$ on $[0, n - 3]$.

*Proof.*
It is a finite sum of $C^2$ functions. $\square$

## The segment form

**Lemma 3.** After lines L1 to L3, $\exp(\omega_k) = q_{k-1}^* q_k$ for each $k$.

*Proof.*
Line L2 makes $q_{k-1}\cdot q_k \ge 0$, so $q_{k-1}^* q_k$ has a scalar part $q_{k-1}\cdot q_k \ge 0$ and its angle $\varphi$ is in $[0, \pi/2]$.
On such unit quaternions, $\exp(\log p) = p$. $\square$

**Lemma 4.** On $[j, j + 1]$ the global curve $q(t) = q_0 \prod_{i=1}^{n-1}\exp(\omega_i\tilde B_i(t))$ equals the segment form of lines L4 to L8 with $u = t - j$.

*Proof.*
By Lemma 1 the factors with $i \le j$ are $\exp(\omega_i) = q_{i-1}^* q_i$ by Lemma 3, and the factors with $i \ge j + 4$ are $\exp(0) = 1$.
The product $q_0 \prod_{i=1}^{j} q_{i-1}^* q_i$ telescopes to $q_j$, because $q_i q_i^* = 1$.
The remaining factors are those of line L7, in the same order. $\square$

## Smoothness and unit length

**Theorem.** $q(t)$ is a unit quaternion for every $t \in [0, n - 3]$, and $q$ is $C^2$.

*Proof.*
Each factor is a unit quaternion, and a product of unit quaternions has length 1.
The factor $\exp(\omega_i\tilde B_i(t))$ is the composition of the smooth map $x \mapsto \exp(x\omega_i)$ with the $C^2$ function $\tilde B_i$ of Lemma 2, so it is $C^2$.
The quaternion product is bilinear, so a product of finitely many $C^2$ curves is $C^2$ by the product rule. $\square$

By Lemma 4, the segments of the page join with matching values and first and second derivatives at the integer parameters, because they are pieces of one $C^2$ function.

## Derivatives

**Lemma 5.** With $A_k = \exp(\tilde B_k(u)\,\omega_{j+k})$, $A_k' = A_k\,\tilde B_k'(u)\,\omega_{j+k}$, and the body angular velocity on segment $j$ is

$$2q^* q' = 2\bigl(A_3^* A_2^*\,\tilde B_1'\omega_{j+1}\,A_2 A_3 + A_3^*\,\tilde B_2'\omega_{j+2}\,A_3 + \tilde B_3'\omega_{j+3}\bigr).$$

*Proof.*
$A_k$ is a function of the commuting family $x\omega_{j+k}$, so its derivative is $A_k\,\omega_{j+k}\tilde B_k'$ by the chain rule.
The product rule gives $q' = q_j(A_1'A_2A_3 + A_1A_2'A_3 + A_1A_2A_3')$.
Multiplying on the left by $q^* = A_3^*A_2^*A_1^*q_j^*$ and using $A_k^*A_k = 1$ gives the formula. $\square$

## Rotations about one axis

**Lemma 6.** If every $q_k$ is a rotation about the same unit axis $\hat a$, with angles $\theta_k$ and $|\theta_k - \theta_{k-1}| < \pi$, then $q(t)$ is the rotation about $\hat a$ by $\sum_l \theta_l B_l(t)$.

*Proof.*
After the sign test, $q_k = (\cos\frac{\theta_k}2, \sin\frac{\theta_k}2\hat a)$ up to a common sign choice, and $\omega_k = (0, \frac12(\theta_k - \theta_{k-1})\hat a)$.
All factors are rotations about $\hat a$, so they commute and their half angles add:
$\frac12(\theta_0 + \sum_{i \ge 1}(\theta_i - \theta_{i-1})\tilde B_i) = \frac12\sum_l \theta_l B_l$ by summation by parts, since $\tilde B_0 = 1$ on the domain. $\square$

## Independence of frames

**Lemma 7.** For unit quaternions $a$ and $b$, the control quaternions $a\,q_k\,b$ give the curve $a\,q(t)\,b$.

*Proof.*
$(aq_{k-1}b)^*(aq_kb) = b^*(q_{k-1}^*q_k)b$, and conjugation by $b$ is a rotation of the pure quaternions, so the new $\omega_k$ is $b^*\omega_kb$ and $\exp(x\,b^*\omega_kb) = b^*\exp(x\omega_k)b$.
In the product $a\,q_j\,b\,\prod_k b^*A_kb$, the inner factors $b\,b^*$ cancel, which leaves $a\,q_j A_1A_2A_3\,b$.
The dot products of line L1 do not change, because multiplication by unit quaternions is an isometry of $\mathbb{R}^4$. $\square$
