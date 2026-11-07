---
title: Ridders' method keeps the bracket, at least halves it in every pass, and ends
proves: [correctness, termination, global-convergence]
status: full
---

Write $[a, b]$ for the bracket at the start of a pass, with $f(a)f(b) < 0$, $m = (a + b)/2$, $h = m - a$, and assume $f(m) \ne 0$ (otherwise line L3 returns an exact root). The arithmetic is exact except where floating point is mentioned.

## Claim 1: the Ridders point is in the bracket

Since $f(a)f(b) < 0$, $s^2 = f(m)^2 - f(a)f(b) > f(m)^2$, so $s > |f(m)| > 0$ and $|x - m| = h|f(m)|/s < h$. Hence $a < x < b$.

## Claim 2: the Ridders point lies in the half with the sign change

Suppose $f(a) < 0 < f(b)$, so $\operatorname{sign}(f(a) - f(b)) = -1$ and $x = m - h f(m)/s$. If $f(m) > 0$, the sign change is in $(a, m)$, and $x < m$, so $x \in (a, m)$. If $f(m) < 0$, the sign change is in $(m, b)$, and $x > m$, so $x \in (m, b)$. The case $f(a) > 0 > f(b)$ is the same with all signs reversed.

## Claim 3: the bracket is kept and at least halves

Let $H$ be the half, $[a, m]$ or $[m, b]$, whose ends have opposite signs; by Claim 2, $x \in H$. If $f(x) = 0$ the program returns an exact root. Otherwise, in line L7:

- If $f(m)$ and $f(x)$ have opposite signs, the new bracket is the interval between $m$ and $x$, which lies in $H$ and has a sign change.
- Otherwise $f(x)$ has the sign of $f(m)$, so it has the sign opposite to the far end of $H$, that is the end of $H$ other than $m$. If that end is $a$, the test $\operatorname{sign}(f(a)) \ne \operatorname{sign}(f(x))$ holds and the new bracket is $[a, x] \subset [a, m]$. If that end is $b$, then $f(x)$ has the sign of $f(a)$, the first two tests fail, and the new bracket is $[x, b] \subset [m, b]$.

In all cases the new bracket has a sign change and lies inside $H$, so its width is at most $(b - a)/2$.

## Claim 4: termination, the certificate and convergence

Each pass returns or increases $k \le k_{\max}$, so the loop ends. By Claim 3, after $k$ passes the width is at most $(b_0 - a_0)/2^k$, so with $\delta > 0$ line L8 stops after at most $\lceil \log_2((b_0 - a_0)/(2\delta)) \rceil$ passes, with at most two evaluations per pass and two at the start. When line L8 stops, $b - a \le 2\delta$ and $f(a)f(b) < 0$, so by the intermediate value theorem a root lies in $[a, b]$, within $(b - a)/2 \le \delta$ of the midpoint returned.

If the loop never stops, the nested brackets shrink to a point $z$, and $f(a_k)f(b_k) < 0$ with $a_k, b_k \to z$ gives $f(z)^2 \le 0$ by continuity, so $f(z) = 0$.

In floating point, Claims 1 to 3 hold for the computed values as long as the computed signs of $f$ are used consistently, because line L5 clamps $x$ into $[a, b]$ and line L7 only compares signs; but the halving in Claim 3 rests on Claim 2, whose sign argument uses the computed $f(m)$, $f(a)$, $f(b)$ and holds for them. When $a$ and $b$ are adjacent numbers, $m$ is not strictly between them and line L3 stops.

## Claim 5: exactness for an exponential times a line

If $f(x) = e^{\lambda x}(\alpha x + \beta)$, choose $Q = -\lambda$: then $g(x) = f(x)e^{Q(x - a)} = e^{\lambda a}(\alpha x + \beta)$ is linear, so the values at $a$, $m$, $b$ are collinear and the positive root $w$ of $f(b)w^2 - 2f(m)w + f(a) = 0$ is $e^{-\lambda h}$. The false position point of a linear function is its zero, so $x = -\beta/\alpha$.

## What is not proved

No rate of convergence is proved here. The quadratic rate claimed by Ridders and the one-sided behaviour of the examples are observations.
