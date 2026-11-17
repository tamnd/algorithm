---
title: Momentum and energy of the PIC transfers
proves: [correctness]
status: full
---

We use the notation of the page, with exact real arithmetic.
The claims are about lines L2 and L5 at the same particle positions.
We prove them for the $u$ faces; the $v$ faces are the same with the roles of $x$ and $y$ exchanged.
The masses are $m_p > 0$, and $m_f = \sum_p w_{fp} m_p$ is the mass of face $f$ from line L2.

## The weights

**Claim 1.** For each particle, $w_{fp} \ge 0$ and $\sum_f w_{fp} = 1$.

*Proof.*
The code clamps the fractional sample coordinates $(f_x, f_y)$ into the sample range and picks the lower sample $(a_0, b_0)$ so that $s = f_x - a_0$ and $t = f_y - b_0$ are in $[0, 1]$.
The four weights are $(1-s)(1-t)$, $(1-s)t$, $s(1-t)$ and $st$, which are at least 0, and their sum is $((1-s) + s)((1-t) + t) = 1$.
These are the weights of the bilinear sample of the MAC grid page, so line L5 equals that sample. $\square$

**Claim 2.** If the $u$ weights of particle $p$ are not clamped, then $\sum_f w_{fp}\,x_f = x_p$ and $\sum_f w_{fp}\,y_f = y_p$, where $(x_f, y_f)$ is the center of face $f$.

*Proof.*
The faces are at $x_f = (a_0 + \alpha)\Delta x$ and $y_f = (b_0 + \beta + 1/2)\Delta x$ with $\alpha, \beta \in \{0, 1\}$.
The $x$ weights $(1-s, s)$ give $\sum_f w_{fp}\,x_f = (a_0 + s)\Delta x = x_p$ when $f_x = x_p/\Delta x$ is not clamped, and the same holds for $y$. $\square$

For the $u$ faces, no clamping means $y_p \in [\Delta x/2, (n_y - 1/2)\Delta x]$; for the $v$ faces, $x_p \in [\Delta x/2, (n_x - 1/2)\Delta x]$.
Line L6 keeps every particle in this range.

## Linear momentum

**Claim 3.** Line L2 gives $\sum_f m_f u_f = \sum_p m_p u_p$, and line L5 gives $\sum_p m_p u'_p = \sum_f m_f u_f$.

*Proof.*
A face with $m_f = 0$ has $w_{fp} = 0$ for every $p$, so it adds 0 to both sides.
For the others, $m_f u_f = \sum_p w_{fp} m_p u_p$, and the sum over $f$ is $\sum_p m_p u_p \sum_f w_{fp} = \sum_p m_p u_p$ by Claim 1.
For line L5, $\sum_p m_p u'_p = \sum_p m_p \sum_f w_{fp} u_f = \sum_f u_f \sum_p w_{fp} m_p = \sum_f m_f u_f$. $\square$

Claim 3 needs no hypothesis on clamping.

## Energy

**Claim 4.** $\frac12\sum_f m_f u_f^2 \le \frac12\sum_p m_p u_p^2$ after line L2, and $\frac12\sum_p m_p u_p'^2 \le \frac12\sum_f m_f u_f^2$ after line L5.

*Proof.*
For a face with $m_f > 0$, $u_f$ is the mean of the $u_p$ with the weights $w_{fp} m_p / m_f$, which are at least 0 and add up to 1.
By Jensen's inequality for the convex function $z \mapsto z^2$, $m_f u_f^2 \le \sum_p w_{fp} m_p u_p^2$.
The sum over $f$ and Claim 1 give the first inequality.
For line L5, $u'_p = \sum_f w_{fp} u_f$ is a mean with the weights $w_{fp}$, so $u_p'^2 \le \sum_f w_{fp} u_f^2$.
Multiply by $m_p$ and sum over $p$: $\sum_p m_p u_p'^2 \le \sum_f u_f^2 m_f$. $\square$

Equality in the first inequality needs all $u_p$ with $w_{fp} > 0$ to be equal for each face.
So a velocity field that varies inside the support of a face loses energy in each round trip, as the example of the page shows.

## Angular momentum

On the MAC grid, the angular momentum about the origin is $L = \sum_{v\text{ faces}} m_f x_f v_f - \sum_{u\text{ faces}} m_f y_f u_f$.

**Claim 5.** If no particle is clamped, line L2 gives the grid $L$ equal to $\sum_p m_p (x_p v_p - y_p u_p)$.

*Proof.*
$\sum_f m_f y_f u_f = \sum_f y_f \sum_p w_{fp} m_p u_p = \sum_p m_p u_p \sum_f w_{fp} y_f = \sum_p m_p u_p y_p$ by Claim 2.
In the same way, $\sum_f m_f x_f v_f = \sum_p m_p v_p x_p$. $\square$

Line L5 does not keep $L$ in general.
The particle value after line L5 is $\sum_p m_p\sum_f w_{fp}(x_p v_f - \dots)$, while the grid value is $\sum_p m_p\sum_f w_{fp}(x_f v_f - \dots)$.
The difference $\sum_p m_p\sum_f w_{fp}(x_p - x_f)v_f$ (and the term in $u$) is not 0 when $v_f$ varies over the stencil of a particle, and the example of the page shows a loss.

## Constant flows

**Claim 6.** If $u_p = U$ for every particle, then after lines L2 and L5, $u'_p = U$ for every particle.

*Proof.*
Each face with mass gets the mean $U$.
Each face in the stencil of a particle has $w_{fp} > 0$ and so has mass, or it has $w_{fp} = 0$ and adds nothing.
So $u'_p = \sum_f w_{fp} U = U$ by Claim 1. $\blacksquare$
