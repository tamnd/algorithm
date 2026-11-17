---
title: Squad passes through the keys, stays on the unit sphere and has a continuous first derivative
proves: [correctness]
status: full
---

We use the notation of the page.
Quaternions are in the Hamilton convention, scalar first.
For a unit quaternion $p = (\cos\varphi, \sin\varphi\,\hat u)$ with $\varphi \in [0, \pi]$, $\log p = (0, \varphi\hat u)$, and $\exp(0, v) = (\cos|v|, \sin|v|\, v/|v|)$.
So $\exp$ maps pure quaternions to unit quaternions, and $\exp(\log p) = p$.
We write $\operatorname{arc}(p, q, w) = p\exp(w\log(p^* q))$.
The keys are at the times $0, 1, \dots, n - 1$.

## Interpolation and unit length

**Lemma 1.** For unit quaternions $p$ and $q$, $\operatorname{arc}(p, q, w)$ is a unit quaternion, $\operatorname{arc}(p, q, 0) = p$ and $\operatorname{arc}(p, q, 1) = q$.

*Proof.*
$\exp$ of a pure quaternion has length 1, and a product of unit quaternions has length 1.
At $w = 0$ the factor is $\exp(0) = 1$.
At $w = 1$ it is $\exp(\log(p^* q)) = p^* q$, and $p p^* q = q$. $\square$

**Lemma 2.** Segment $i$ of squad starts at $q_i$ and ends at $q_{i+1}$, and every point has length 1.

*Proof.*
By Lemma 1, line L8 gives $A = q_i$ at $t = 0$ and $A = q_{i+1}$ at $t = 1$.
The weight $2t(1 - t)$ of line L10 is 0 at both ends, so by Lemma 1 the result is $A$ there.
All three arcs are unit quaternions by Lemma 1. $\square$

Lines L1 and L2 replace $q_k$ by $-q_k$ only, which is the same rotation, so the curve passes through the key rotations.

## The derivative of an arc

**Lemma 3.** Let $A(t)$ and $B(t)$ be differentiable curves of unit quaternions and $w(t)$ a differentiable weight with $w(t_0) = 0$.
Then $f(t) = \operatorname{arc}(A(t), B(t), w(t))$ has $f'(t_0) = A'(t_0) + w'(t_0)\, A(t_0)\log(A(t_0)^* B(t_0))$, if $A(t_0)^* B(t_0) \ne -1$.

*Proof.*
Write $L(t) = \log(A(t)^* B(t))$, which is differentiable near $t_0$ because $\log$ is smooth away from $-1$.
Then $f = A\exp(wL)$ and $f' = A'\exp(wL) + A\,\frac{d}{dt}\exp(wL)$.
At $t_0$, $\exp(wL) = 1$.
The derivative of $\exp$ at 0 is the identity on pure quaternions, so $\frac{d}{dt}\exp(wL) = (wL)' = w'L + wL' = w'L$ at $t_0$. $\square$

**Lemma 4.** For a pure quaternion $c$ with $|c| < \pi$ and $A(t) = p\exp(tc)$, $A'(t) = A(t)\,c$.

*Proof.*
The pure quaternions $tc$ for different $t$ commute, so $\exp((t + h)c) = \exp(tc)\exp(hc)$, and $\frac{d}{dh}\exp(hc) = c$ at $h = 0$. $\square$

## Continuity of the first derivative

Fix an inner key $i$, $1 \le i \le n - 2$, and let $a = \log(q_i^* q_{i+1})$, $b = \log(q_i^* q_{i-1})$ and $e = -(a + b)/4$, as in lines L5 to L7, so that $s_i = q_i\exp(e)$.
Assume that adjacent keys are not opposite rotations by a half turn, so that the logarithms are smooth where we use them.

**Lemma 5.** The right derivative at key $i$ is $q_i\frac{a - b}{2}$.

*Proof.*
On segment $i$, $A(t) = \operatorname{arc}(q_i, q_{i+1}, t) = q_i\exp(ta)$, so $A(0) = q_i$ and by Lemma 4 $A'(0) = q_i a$.
$B(0) = s_i$ by Lemma 1, $w(t) = 2t(1 - t)$, $w(0) = 0$ and $w'(0) = 2$.
$A(0)^* B(0) = q_i^* q_i\exp(e) = \exp(e)$, and since $|e| \le (|a| + |b|)/4 \le \pi/2$, $\log\exp(e) = e$.
By Lemma 3, $q'(i^+) = q_i a + 2q_i e = q_i(a - \frac{a + b}{2}) = q_i\frac{a - b}{2}$. $\square$

**Lemma 6.** The left derivative at key $i$ is $q_i\frac{a - b}{2}$.

*Proof.*
On segment $i - 1$, $A(t) = q_{i-1}\exp(tc)$ with $c = \log(q_{i-1}^* q_i)$.
Since $q_i^* q_{i-1} = (q_{i-1}^* q_i)^*$ and $\log(p^*) = -\log p$ for a unit $p$, $c = -b$.
By Lemma 4, $A'(1) = A(1)c = -q_i b$.
$B(1) = s_i$ by Lemma 1, $w(1) = 0$ and $w'(1) = -2$.
As in Lemma 5, $\log(A(1)^* B(1)) = e$.
By Lemma 3, $q'(i^-) = -q_i b - 2q_i e = q_i(-b + \frac{a + b}{2}) = q_i\frac{a - b}{2}$. $\square$

**Theorem.** With keys at equal time steps, squad is continuous with a continuous first derivative on $[0, n - 1]$.

*Proof.*
Inside each segment the curve is a composition of smooth maps.
At an inner key the two segments meet at $q_i$ by Lemma 2, and their derivatives agree by Lemmas 5 and 6. $\square$

The body angular velocity is $\omega = 2\,\mathrm{vec}(q^* q')$, so at key $i$ it is the vector part of $a - b$ from both sides.

## Independence of frames

**Lemma 7.** For unit quaternions $c$ and $d$, the keys $c\,q_k\,d$ give the control points $c\,s_k\,d$ and the curve $c\,q(u)\,d$.

*Proof.*
$(c q_k d)^*(c q_{k+1} d) = d^*(q_k^* q_{k+1})d$.
Conjugation by $d$ is a rotation of the pure quaternions and preserves the angle, so $\log(d^* p\, d) = d^*\log(p)\, d$ and $\exp(d^* v\, d) = d^*\exp(v)\, d$.
Then the control point is $c q_k d\, d^*\exp(e)d = c\, s_k\, d$.
The same identity gives $\operatorname{arc}(cpd, cqd, w) = c\operatorname{arc}(p, q, w)d$, and the three arcs of the query carry the factors through.
The dot products of line L1 do not change, since multiplication by unit quaternions is an isometry of $\mathbb{R}^4$. $\square$
