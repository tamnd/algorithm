---
title: The three subproblems return exactly their solution sets, and the elbow arm solution returns exactly the inverse kinematics solutions
proves: [correctness]
status: full
---

We use the notation of the page.
The proof is in exact arithmetic, in the real RAM.
All axes have unit directions, and $R(\omega, \theta) = e^{[\omega]\theta}$ is the rotation by $\theta$ about $\omega$.
For a vector $x$, write $x' = x - \omega\omega^{\mathsf T}x$ for its part orthogonal to $\omega$.

**Lemma 0.** For every $x$, $R(\omega, \theta)x = \omega\omega^{\mathsf T}x + \cos\theta\,x' + \sin\theta\,\omega \times x'$.
So the rotation keeps $\omega^{\mathsf T}x$ and $|x'|$, and it turns $x'$ by the angle $\theta$ in the plane orthogonal to $\omega$, in the positive sense about $\omega$.

*Proof.*
This is Rodrigues' formula $R = I + \sin\theta[\omega] + (1 - \cos\theta)[\omega]^2$ with $[\omega]x = \omega \times x'$ and $[\omega]^2x = -x'$.
$\square$

## Subproblem 1

**Claim.** Let $u = p - r$ and $v = q - r$ with $u' \ne 0$.
A $\theta$ with $e^{[\xi]\theta}p = q$ exists if and only if $\omega^{\mathsf T}u = \omega^{\mathsf T}v$ and $|u'| = |v'|$, and then it is unique modulo $2\pi$ and equal to $\operatorname{atan2}(\omega^{\mathsf T}(u' \times v'), u'^{\mathsf T}v')$.

*Proof.*
The equation $e^{[\xi]\theta}p = q$ is $R(\omega, \theta)u = v$.
By Lemma 0, the part along $\omega$ gives $\omega^{\mathsf T}u = \omega^{\mathsf T}v$ and the orthogonal part gives $\cos\theta\,u' + \sin\theta\,\omega \times u' = v'$, which forces $|u'| = |v'|$.
Conversely, if both conditions hold, $u'$ and $\omega \times u'$ are an orthogonal basis of the plane with equal lengths, so $v' = \cos\theta\,u' + \sin\theta\,\omega \times u'$ for exactly one $\theta$ modulo $2\pi$.
Taking dot products with $u'$ and with $\omega \times u'$ gives $u'^{\mathsf T}v' = |u'|^2\cos\theta$ and $\omega^{\mathsf T}(u' \times v') = (\omega \times u')^{\mathsf T}v' = |u'|^2\sin\theta$.
Both have the positive factor $|u'|^2$, so atan2 returns $\theta$.
$\square$

If $u' = 0$, then $p$ is on the axis, every $\theta$ leaves it in place, and there is a solution if and only if $q = p$.

## Subproblem 2

**Claim.** Let the axes $(\omega_1, r)$ and $(\omega_2, r)$ meet at $r$ with $\omega_1 \ne \pm\omega_2$, let $u = p - r$, $v = q - r$, and suppose that $p$ is off axis 2 and $q$ is off axis 1.
Then the pairs $(\theta_1, \theta_2)$ modulo $2\pi$ with $e^{[\xi_1]\theta_1}e^{[\xi_2]\theta_2}p = q$ are in one to one correspondence with the real $\gamma$ that satisfy line L7, and L9 to L12 output exactly these pairs.

*Proof.*
Let $k = \omega_1^{\mathsf T}\omega_2$, so $|k| < 1$ and $|\omega_1 \times \omega_2|^2 = 1 - k^2 > 0$.
The three vectors $\omega_1$, $\omega_2$ and $\omega_1 \times \omega_2$ are a basis, so every vector has the form $z = \alpha\omega_1 + \beta\omega_2 + \gamma(\omega_1 \times \omega_2)$.

Suppose $(\theta_1, \theta_2)$ is a solution, and put $z = R(\omega_2, \theta_2)u$, so that $R(\omega_1, \theta_1)z = v$.
By Lemma 0, $\omega_2^{\mathsf T}z = \omega_2^{\mathsf T}u$, $\omega_1^{\mathsf T}z = \omega_1^{\mathsf T}v$ and $|z| = |u|$.
The first two equations read $\alpha k + \beta = \omega_2^{\mathsf T}u$ and $\alpha + \beta k = \omega_1^{\mathsf T}v$, a linear system with determinant $k^2 - 1 \ne 0$, whose solution is the pair $(\alpha, \beta)$ of line L6.
Since $\omega_1 \times \omega_2$ is orthogonal to $\omega_1$ and $\omega_2$, $|z|^2 = \alpha^2 + \beta^2 + 2\alpha\beta k + \gamma^2(1 - k^2)$, and $|z| = |u|$ is the equation of line L7.
So $z$ is one of the vectors built in L10.

Conversely, let $\gamma$ be a real root of L7 and $z$ the vector of L10, with $c = r + z$.
Then $\omega_2^{\mathsf T}z = \omega_2^{\mathsf T}u$ and $|z| = |u|$, so $|z'| = |u'|$ for the parts orthogonal to $\omega_2$.
Since $p$ is off axis 2, $u' \ne 0$, and the claim on subproblem 1 gives a unique $\theta_2$ with $R(\omega_2, \theta_2)u = z$.
In the same way, $\omega_1^{\mathsf T}z = \omega_1^{\mathsf T}v$ and $|z| = |u| = |v|$ give a unique $\theta_1$ with $R(\omega_1, \theta_1)z = v$; here $|u| = |v|$ is necessary for any solution, since rotations about lines through $r$ keep the distance to $r$.
So each root $\gamma$ gives one solution, and different roots give different $z$ and so different $\theta_2$.
Every solution arises in this way by the first part.
L7 has two real roots when $\gamma^2 > 0$, one when $\gamma^2 = 0$, and none when $\gamma^2 < 0$, which is the test of L8.
$\square$

## Subproblem 3

**Claim.** Let $u = p - r$ and $v = q - r$ with $u' \ne 0$ and $v' \ne 0$.
The set of $\theta$ with $|e^{[\xi]\theta}p - q| = \delta$ is $\{\theta_0 \pm \arccos c\}$ modulo $2\pi$ if $|c| \le 1$ and empty otherwise, with $\theta_0$ and $c$ from lines L15 and L16.

*Proof.*
By Lemma 0, $e^{[\xi]\theta}p - q = R(\omega, \theta)u - v = \omega\,\omega^{\mathsf T}(u - v) + (R(\omega, \theta)u' - v')$, a sum of two orthogonal parts.
So $|e^{[\xi]\theta}p - q|^2 = (\omega^{\mathsf T}(p - q))^2 + |R(\omega, \theta)u' - v'|^2$.
The vector $R(\omega, \theta)u'$ has length $|u'|$ and makes the signed angle $\theta_0 - \theta$ with $v'$, where $\theta_0$ is the signed angle from $u'$ to $v'$ (by the computation in subproblem 1).
By the law of cosines, $|R(\omega, \theta)u' - v'|^2 = |u'|^2 + |v'|^2 - 2|u'||v'|\cos(\theta_0 - \theta)$.
So the equation is $\cos(\theta_0 - \theta) = c$ with $c = (|u'|^2 + |v'|^2 - \delta'^2)/(2|u'||v'|)$ and $\delta'^2 = \delta^2 - (\omega^{\mathsf T}(p - q))^2$.
For $|c| > 1$ it has no solution, and otherwise its solutions are $\theta = \theta_0 \pm \arccos c$, which coincide when $|c| = 1$.
$\square$

## The elbow arm

Let the arm be $T(\theta) = e^{[\mathcal S_1]\theta_1}\cdots e^{[\mathcal S_6]\theta_6}M$, with axis 1 through $q_s$, axes 2 and 3 parallel, axis 2 through $q_s$, and axes 4, 5 and 6 through $q_w$.
Write $E_i = e^{[\mathcal S_i]\theta_i}$.
We assume that the target is generic in the sense that each point given to a subproblem is off the axes of that subproblem; the code checks no more than this.

**Claim.** The four steps of the page return exactly the set of $\theta$ modulo $2\pi$ with $T(\theta) = T_d$.

*Proof.*
Let $\theta$ be a solution and $g_1 = T_dM^{-1} = E_1E_2\cdots E_6$.
The rotations $E_4$, $E_5$ and $E_6$ fix $q_w$, so $p_w = g_1q_w = E_1E_2E_3q_w$.
The rotations $E_1$ and $E_2$ fix $q_s$ and keep distances, so $|E_3q_w - q_s| = |E_1E_2E_3q_w - q_s| = |p_w - q_s|$, and $\theta_3$ is among the outputs of step 1 by the claim on subproblem 3.
Then $E_1E_2(E_3q_w) = p_w$, so $(\theta_1, \theta_2)$ is among the outputs of step 2 by the claim on subproblem 2.
Next $g_2 = (E_1E_2E_3)^{-1}g_1 = E_4E_5E_6$, and for a point $p$ on axis 6, $E_6p = p$, so $E_4E_5p = g_2p$ and $(\theta_4, \theta_5)$ is among the outputs of step 3.
Finally $(E_4E_5)^{-1}g_2 = E_6$, and step 4 returns $\theta_6$ by the claim on subproblem 1.

Conversely, take an output of the four steps.
Step 4 gives $E_6 = (E_4E_5)^{-1}g_2$ on the point $p'$ used there, and we must show it on all points.
Both sides are rigid motions that fix $q_w$: the left side because $q_w$ is on axis 6, and the right side because $E_4$ and $E_5$ fix $q_w$ and step 3 ensures $g_2p = E_4E_5p$ for the point $p \ne q_w$ on axis 6, while $g_2q_w = (E_1E_2E_3)^{-1}g_1q_w = (E_1E_2E_3)^{-1}p_w = q_w$ by step 2.
So $H = E_4E_5E_6$ and $g_2$ are two rigid motions that agree on $q_w$, on $p$ (since $E_6$ fixes $p$) and on $p'$.
These three points are not on one line, because $p'$ is off axis 6 and $q_w$ and $p$ span that axis.
A rigid motion of space that preserves orientation is fixed by the images of three points not on a line, so $H = g_2$.
Then $E_1E_2E_3E_4E_5E_6 = E_1E_2E_3g_2 = g_1$, and $T(\theta) = g_1M = T_d$.
$\square$

**Counting.** Step 1 gives at most 2 values, and steps 2 and 3 at most 2 each, while step 4 gives 1, so there are at most $2 \cdot 2 \cdot 2 = 8$ solutions.
The example of the page, and the test against a multi-start Newton search, show a target with all 8.
