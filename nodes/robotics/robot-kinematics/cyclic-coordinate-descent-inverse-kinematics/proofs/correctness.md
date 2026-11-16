---
title: Each CCD update is the best turn of its joint, the error never increases, and a sweep that changes nothing stops at a stationary point
proves: [correctness]
status: full
---

We use the notation of the page, in exact arithmetic.
The chain has revolute joints $1, \ldots, n$.
For a joint vector $\theta$, joint $i$ has the world position $p_i$ and the unit world axis $w_i$, and $e$ is the position of the end effector.
$R(w, \varphi)$ is the rotation about the unit vector $w$ by the angle $\varphi$, given by the [Rodrigues formula](/rodrigues-rotation-formula/).
The error is $E(\theta) = |e(\theta) - t|$.

## Claim 1: line L7 gives the best angle for one joint

Fix $i$, write $w = w_i$, $p = p_i$, $u = e - p$ and $v = t - p$, and let $u_\perp = u - (w \cdot u)w$ and $v_\perp = v - (w \cdot v)w$ be the parts perpendicular to $w$.
If joint $i$ turns by $\varphi$ and the other joints stay, the part of the chain after joint $i$ turns rigidly about the line through $p$ along $w$, so the end effector moves to $p + R(w, \varphi)u$.
Then
$$|p + R(w,\varphi)u - t|^2 = |u|^2 + |v|^2 - 2\,v \cdot R(w,\varphi)u.$$
The Rodrigues formula gives $R(w,\varphi)u = (w \cdot u)w + \cos\varphi\,u_\perp + \sin\varphi\,(w \times u_\perp)$.
So $v \cdot R(w,\varphi)u = (w \cdot u)(w \cdot v) + a\cos\varphi + b\sin\varphi$, with $a = u_\perp \cdot v_\perp$ and $b = v \cdot (w \times u_\perp) = w \cdot (u_\perp \times v_\perp)$, since $w \times u_\perp$ is perpendicular to $w$.

If $(a, b) \ne (0, 0)$, write $(a, b) = \rho(\cos\varphi^*, \sin\varphi^*)$ with $\rho > 0$; then $a\cos\varphi + b\sin\varphi = \rho\cos(\varphi - \varphi^*)$, which is largest exactly at $\varphi = \varphi^* + 2\pi j$.
So $\varphi^* = \operatorname{atan2}(b, a)$ of line L7 minimizes the distance, and it is the only minimizer up to multiples of $2\pi$.
If $a = b = 0$, the distance does not depend on $\varphi$, and $\varphi = 0$ is a minimizer.
$\square$

## Claim 2: line L8 keeps the end effector right

Turning joint $i$ moves only the links after joint $i$.
So the positions and axes of joints $1, \ldots, i - 1$, found by forward kinematics at line L3, do not change, and the joints that the sweep visits after joint $i$ can use them.
The end effector moves to $p_i + R(w_i, \varphi)(e - p_i)$, which is the value that line L8 stores.
By induction over the joints of the sweep, before each update $p_i$, $w_i$ and $e$ are the true values for the current $\theta$.
$\square$

## Claim 3: the error never increases

By Claim 1 with $\varphi = 0$ as one candidate, the update of joint $i$ gives an error at most the error before it.
By Claim 2, the error that the loop sees is the true error.
So the errors after each joint update form a nonincreasing sequence of numbers $\ge 0$, and it converges.
$\square$

The limit need not be 0, and Claim 3 does not say that the joint vectors converge.

## Claim 4: a sweep that changes nothing stops at a stationary point

Let a sweep give $\varphi = 0$ for every joint.
Then the sweep does not move the chain, so all joints see the same $\theta$.
By Claim 1, $\varphi = 0$ at joint $i$ means either $a_i = b_i = 0$, or $b_i = 0$ and $a_i > 0$; in both cases $b_i = 0$.
The partial derivative of $\tfrac12 E^2$ in $\theta_i$ is $(e - t) \cdot (w_i \times (e - p_i))$, the speed of the end effector along the error.
Since $w_i \times (e - p_i) = w_i \times u_\perp$ and $e - t = u - v$, this is $(u - v) \cdot (w_i \times u_\perp) = -v \cdot (w_i \times u_\perp) = -b_i = 0$.
So the gradient of $\tfrac12E^2$ is zero, and $\theta$ is a stationary point; moreover, each joint alone is at its best angle.
$\square$

A stationary point with $E > 0$ is not a solution.
For a target out of reach, the stretched chain that points at the target is such a point.
So these claims give no guarantee that CCD finds a solution when one exists, and the page makes no such claim.
