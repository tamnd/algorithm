---
title: Two-bone IK keeps the bone lengths, reaches every reachable target, and stretches toward an unreachable one
proves: [correctness]
status: full
---

We use the notation of the page.
The arithmetic is exact, $l_1, l_2 > 0$, and $t \ne a$.
Let $d_0 = |t - a|$ be the distance before line L2 and $d$ the distance after it.

## The triangle exists

**Lemma 1.** After line L2, $|l_1 - l_2| \le d \le l_1 + l_2$ and $-1 \le \cos\alpha \le 1$.

*Proof.*
The clamp gives the first claim.
If $d = 0$, then $l_1 = l_2$; the code sets $\cos\alpha = 1$, and the claims below hold with $f = a$.
Otherwise $\cos\alpha \le 1$ is $l_1^2 + d^2 - l_2^2 \le 2 l_1 d$, that is $(l_1 - d)^2 \le l_2^2$, that is $|l_1 - d| \le l_2$, which follows from $d \ge l_1 - l_2$ and $d \le l_1 + l_2$.
$\cos\alpha \ge -1$ is $(l_1 + d)^2 \ge l_2^2$, which follows from $d \ge l_2 - l_1$. $\square$

So $\sin\alpha = \sqrt{1 - \cos^2\alpha}$ is real and nonnegative.

## Bone lengths

**Lemma 2.** $x$ and $y$ of lines L3 and L4 are orthonormal.

*Proof.*
$|x| = 1$ by line L3.
Let $w = (p - a) - ((p - a)\cdot x)\,x$; then $w \cdot x = (p - a)\cdot x - (p - a)\cdot x = 0$, and $y = w / |w|$ for $w \ne 0$. $\square$

**Lemma 3.** $|e - a| = l_1$ and $|f - e| = l_2$.

*Proof.*
By line L6 and Lemma 2, $|e - a|^2 = l_1^2 (\cos^2\alpha + \sin^2\alpha) = l_1^2$.
By line L7, $f - e = (d - l_1\cos\alpha)\,x - l_1 \sin\alpha\, y$, so
$|f - e|^2 = d^2 - 2 d l_1 \cos\alpha + l_1^2 = d^2 - (l_1^2 + d^2 - l_2^2) + l_1^2 = l_2^2$
by line L5. $\square$

## Reaching the target

**Lemma 4.** If $|l_1 - l_2| \le d_0 \le l_1 + l_2$, then $f = t$.

*Proof.*
The clamp leaves $d = d_0$, and $f = a + d_0 (t - a)/d_0 = t$. $\square$

**Lemma 5.** If $d_0 > l_1 + l_2$, then $e = a + l_1 x$ and $f = a + (l_1 + l_2) x$: the limb is straight and points at the target.

*Proof.*
Then $d = l_1 + l_2$, and $\cos\alpha = \frac{l_1^2 + (l_1 + l_2)^2 - l_2^2}{2 l_1 (l_1 + l_2)} = \frac{2 l_1^2 + 2 l_1 l_2}{2 l_1 (l_1 + l_2)} = 1$, so $\sin\alpha = 0$. $\square$

Of all the points that the end can reach, which are the points at a distance in $[|l_1 - l_2|, l_1 + l_2]$ from $a$, the point $a + (l_1 + l_2)\,x$ is the nearest to $t$, because the distance from $t$ to a point at the distance $r$ from $a$ is at least $|d_0 - r|$, with equality on the ray toward $t$.
The same argument gives the nearest point $a + |l_1 - l_2|\, x$ for $d_0 < |l_1 - l_2|$.

## The plane and the side

**Lemma 6.** $e$ lies in the plane through $a$ spanned by $x$ and $p - a$, and $(e - a) \cdot w \ge 0$.

*Proof.*
$e - a = l_1(\cos\alpha\,x + \sin\alpha\,y)$, and $y$ is a combination of $x$ and $p - a$.
$(e - a)\cdot w = l_1 \sin\alpha\, |w| \ge 0$, by Lemma 2 and $\sin\alpha \ge 0$. $\square$

## The planar closed form

**Lemma 7.** For a reachable $(x, y) \ne (0, 0)$ in the plane, $\theta_2 = \pm\arccos\frac{x^2 + y^2 - l_1^2 - l_2^2}{2 l_1 l_2}$ and $\theta_1 = \operatorname{atan2}(y, x) - \operatorname{atan2}(l_2 \sin\theta_2, l_1 + l_2 \cos\theta_2)$ satisfy $l_1(\cos\theta_1, \sin\theta_1) + l_2(\cos(\theta_1 + \theta_2), \sin(\theta_1 + \theta_2)) = (x, y)$.

*Proof.*
In complex numbers the left side is $e^{i\theta_1}(l_1 + l_2 e^{i\theta_2})$.
Its length squared is $l_1^2 + l_2^2 + 2 l_1 l_2 \cos\theta_2 = x^2 + y^2$, by the choice of $\theta_2$.
Its argument is $\theta_1 + \arg(l_1 + l_2 e^{i\theta_2}) = \operatorname{atan2}(y, x)$, by the choice of $\theta_1$.
Two complex numbers with the same length and the same argument are equal. $\square$

For $l_1 = l_2 = 1$ and $(x, y) = (1, 1)$, $\cos\theta_2 = 0$.
For $\theta_2 = \pi/2$, $\theta_1 = \pi/4 - \operatorname{atan2}(1, 1) = 0$, and for $\theta_2 = -\pi/2$, $\theta_1 = \pi/4 + \pi/4 = \pi/2$.
These are the check values $(0, \pi/2)$ and $(\pi/2, -\pi/2)$, and the inner elbow angle is $\beta = \pi - |\theta_2| = \pi/2$.
