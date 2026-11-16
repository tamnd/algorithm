---
title: SO3-LOG returns exponential coordinates of the input rotation
proves: [correctness]
status: full
---

We use the notation of the page.
For a unit vector $\hat\omega \in \mathbb{R}^3$, $[\hat\omega]$ is its skew-symmetric matrix, so $[\hat\omega] x = \hat\omega \times x$.
Two facts about $[\hat\omega]$ are used again and again.
First, $[\hat\omega]^2 = \hat\omega \hat\omega^{\mathsf T} - I$, which follows from $\hat\omega \times (\hat\omega \times x) = \hat\omega (\hat\omega \cdot x) - x$ for a unit $\hat\omega$.
Second, $\operatorname{tr}[\hat\omega] = 0$ and $\operatorname{tr}[\hat\omega]^2 = |\hat\omega|^2 - 3 = -2$.

The proof is in exact arithmetic.
The last section gives first-order error estimates for floating point.

## Every rotation has exponential coordinates

**Lemma 1.** Let $R \in SO(3)$.
Then there are a unit vector $\hat\omega$ and an angle $\theta \in [0, \pi]$ with $R = e^{[\hat\omega]\theta} = I + \sin\theta\,[\hat\omega] + (1 - \cos\theta)[\hat\omega]^2$.

*Proof.*
Because $R R^{\mathsf T} = I$, we have $R - I = R(I - R^{\mathsf T})$.
With $\det R = 1$ this gives $\det(R - I) = \det((I - R)^{\mathsf T}) = \det(I - R) = -\det(R - I)$, where the last step uses that the matrix has the odd size 3.
So $\det(R - I) = 0$, and there is a unit vector $u$ with $R u = u$.
Choose unit vectors $a$ and $b = u \times a$ such that $(u, a, b)$ is a right-handed orthonormal basis.
$R$ keeps lengths and angles, so it maps the plane spanned by $a$ and $b$ to itself, and on this plane it is an orthogonal $2 \times 2$ map.
In the basis $(u, a, b)$, $R$ is block diagonal with the block $1$ for $u$, so the determinant of this map is $\det R = 1$, and it is a plane rotation by some angle $\varphi \in (-\pi, \pi]$: $R a = \cos\varphi\, a + \sin\varphi\, b$ and $R b = -\sin\varphi\, a + \cos\varphi\, b$.
If $\varphi < 0$, replace $u$ by $-u$, $b$ by $-b$ and $\varphi$ by $-\varphi$; the basis stays right-handed and the two formulas stay true.
Now set $\hat\omega = u$ and $\theta = \varphi \in [0, \pi]$.
The matrix $E = I + \sin\theta\,[u] + (1 - \cos\theta)[u]^2$ gives $E u = u$, because $[u] u = 0$.
It gives $E a = a + \sin\theta\, b - (1 - \cos\theta) a = \cos\theta\, a + \sin\theta\, b$, because $[u] a = u \times a = b$ and $[u]^2 a = -a$.
In the same way $E b = -\sin\theta\, a + \cos\theta\, b$.
So $E$ and $R$ agree on a basis, and $E = R$.
The formula for $E$ is the closed form of the matrix exponential $e^{[u]\theta}$ (see the page on Rodrigues' rotation formula). $\square$

**Lemma 2.** Let $R = e^{[\hat\omega]\theta}$ with a unit $\hat\omega$ and $\theta \in [0, \pi]$.
Then
(a) $\operatorname{tr} R = 1 + 2\cos\theta$;
(b) $\tfrac12 (R - R^{\mathsf T}) = \sin\theta\,[\hat\omega]$;
(c) $\tfrac12 (R + R^{\mathsf T}) - \cos\theta\, I = (1 - \cos\theta)\,\hat\omega\hat\omega^{\mathsf T}$.

*Proof.*
$[\hat\omega]$ is skew-symmetric and $[\hat\omega]^2$ is symmetric.
So the skew part of $R$ is $\sin\theta\,[\hat\omega]$, which is (b), and the symmetric part is $I + (1 - \cos\theta)[\hat\omega]^2$.
Insert $[\hat\omega]^2 = \hat\omega\hat\omega^{\mathsf T} - I$ in the symmetric part to get $\cos\theta\, I + (1 - \cos\theta)\hat\omega\hat\omega^{\mathsf T}$, which is (c).
The trace of $R$ is $3 + 0 + (1 - \cos\theta)(-2) = 1 + 2\cos\theta$, which is (a). $\square$

## The main result

**Theorem.** Let $R \in SO(3)$ and let $w$ be the output of SO3-LOG$(R)$.
If the branch of line L7 or line L12 returns, then $e^{[w]} = R$ and $|w| \in [0, \pi]$.
If the branch of line L5 returns, then $w = (1 + \epsilon)\, \theta\hat\omega$ with $e^{[\theta\hat\omega]} = R$ and $0 \le \epsilon < 3 \cdot 10^{-21}$.
For $\theta < \pi$ the output is the only vector $w$ with $|w| \le \pi$ and $e^{[w]} = R$.
For $\theta = \pi$ there are exactly two such vectors, $\pm\pi\hat\omega$, and the output is one of them.

*Proof.*
By Lemma 1, write $R = e^{[\hat\omega]\theta}$ with a unit $\hat\omega$ and $\theta \in [0, \pi]$.

Lines L1 to L3.
By Lemma 2(a), line L1 computes $c = \cos\theta \in [-1, 1]$, so the clamp has no effect in exact arithmetic.
By Lemma 2(b), the vector of line L2 is $s = \sin\theta\, \hat\omega$.
Because $\sin\theta \ge 0$ on $[0, \pi]$, we have $|s| = \sin\theta$.
The function $\operatorname{atan2}(y, x)$ with $y \ge 0$ returns the angle in $[0, \pi]$ whose cosine and sine are proportional to $x$ and $y$ with a positive factor.
With $x = \cos\theta$ and $y = \sin\theta$ that angle is $\theta$, so line L3 recovers $\theta$ exactly.

Line L5, for $\theta < \delta_0$.
If $\theta = 0$, then $s = 0$ and the output is $w = 0$, and $e^{[0]} = I = R$.
If $0 < \theta < \delta_0$, the exact answer is $w = (\theta / \sin\theta)\, s = \theta\hat\omega$.
The Taylor series of $\theta / \sin\theta$ is $1 + \theta^2/6 + 7\theta^4/360 + 31\theta^6/15120 + \cdots$, with only positive coefficients, so line L5 uses a value below the true ratio by $31\theta^6/15120 + O(\theta^8)$.
For $\theta < \delta_0 = 10^{-3}$ this relative difference is below $3 \cdot 10^{-21}$, far below the unit roundoff $2^{-53} \approx 1.1 \cdot 10^{-16}$ of double precision.
So in floating point line L5 gives the same result as the exact ratio.

Line L7, for $\delta_0 \le \theta \le \pi - \delta_\pi$.
Here $\sin\theta > 0$, so $|s| > 0$ and $(\theta / |s|)\, s = (\theta / \sin\theta)\sin\theta\,\hat\omega = \theta\hat\omega$.
Then $e^{[w]} = e^{[\hat\omega]\theta} = R$ and $|w| = \theta$.

Lines L8 to L12, for $\theta > \pi - \delta_\pi$.
Here $\theta > \pi/2$, so $1 - c > 1$.
By Lemma 2(c), the matrix of line L8 is $B = (1 - c)\,\hat\omega\hat\omega^{\mathsf T}$.
Its diagonal entries are $B_{ii} = (1 - c)\,\omega_i^2$.
Because $\omega_1^2 + \omega_2^2 + \omega_3^2 = 1$, the largest of them, chosen in line L9, has $\omega_k^2 \ge 1/3$.
Column $k$ of $B$ is $(1 - c)\,\omega_k\,\hat\omega$, a nonzero multiple of $\hat\omega$.
So line L10 sets $\hat\omega' = \sigma\hat\omega$ with $\sigma = \operatorname{sign}(\omega_k) \in \{-1, +1\}$.
If $\theta < \pi$, then $\hat\omega' \cdot s = \sigma\sin\theta$ with $\sin\theta > 0$.
Line L11 flips the sign when $\sigma = -1$, so after line L11 $\hat\omega' = \hat\omega$, and line L12 returns $\theta\hat\omega$.
If $\theta = \pi$, then $s = 0$ and line L11 does nothing.
The output is $\pi\sigma\hat\omega$.
Since $\sin\pi = 0$ and $[-\hat\omega]^2 = [\hat\omega]^2$, the formula of Lemma 1 gives $e^{[-\hat\omega]\pi} = I + 2[\hat\omega]^2 = e^{[\hat\omega]\pi}$.
So both signs give $R$.

Uniqueness.
Let $e^{[w']} = R$ with $|w'| = \theta' \le \pi$, and write $w' = \theta'\hat\omega'$ when $\theta' > 0$.
By Lemma 2(a), $\cos\theta' = c = \cos\theta$, and the cosine is one to one on $[0, \pi]$, so $\theta' = \theta$.
If $\theta = 0$, then $w' = 0 = w$.
If $0 < \theta < \pi$, Lemma 2(b) gives $\sin\theta\,[\hat\omega'] = \sin\theta\,[\hat\omega]$ with $\sin\theta \ne 0$, so $\hat\omega' = \hat\omega$ and $w' = w$.
If $\theta = \pi$, Lemma 2(c) gives $2\hat\omega'\hat\omega'^{\mathsf T} = 2\hat\omega\hat\omega^{\mathsf T}$, so $\hat\omega' = \pm\hat\omega$.
Both signs occur, as shown above. $\square$

## Floating point

This section gives first-order estimates in the [floating-point model](/floating-point-model/) with unit roundoff $u = 2^{-53}$.
It is not a full rounding error analysis.
Assume that the input $R$ is a rotation whose entries have absolute errors of order $u$.

The angle.
The trace and the skew part then have absolute errors of order $u$.
An error $\delta$ in $c$ changes $\arccos c$ by about $\delta / \sin\theta$, and near $c = \pm 1$ by up to $\sqrt{2\delta}$, because $\arccos(1 - \delta) \approx \sqrt{2\delta}$.
So the textbook formula $\theta = \arccos c$ can lose about half of the digits near $\theta = 0$ and near $\theta = \pi$.
The two arguments of atan2 have errors of order $u$, and the gradient of $\operatorname{atan2}(y, x)$ has length $1 / \sqrt{x^2 + y^2}$, which is close to 1 here.
So line L3 gives $\theta$ with an absolute error of order $u$ for every $\theta$.

The axis.
In line L7 the axis is $s / |s|$, and an absolute error of order $u$ in $s$ gives an axis error of order $u / \sin\theta$.
This is large only near $\theta = 0$, where the axis has little effect on $w = \theta\hat\omega$, and near $\theta = \pi$.
At the switch $\theta = \pi - \delta_\pi$, the error is about $u / \sin(10^{-2}) \approx 10^{-14}$.
In lines L8 to L10, the column of $B$ has length $(1 - c)|\omega_k| \ge 1/\sqrt{3}$ and an absolute error of order $u$, so the axis has an error of order $u$.
Line L11 uses only the sign of $\hat\omega' \cdot s$.
For $\theta < \pi$ that sign is right as long as $\sin\theta$ is larger than the error in $s$; when it is not, $\theta$ is within a few units of roundoff of $\pi$, where both signs give rotations that agree with $R$ to within a few units of roundoff.

The tests of the page check these estimates: the error of the output is below $10^{-14}\theta$ for small angles, below $10^{-12}$ near $\pi$, and the textbook formula loses accuracy where the estimates say it does.
