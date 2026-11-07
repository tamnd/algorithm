---
title: Correctness, termination and local order of the Illinois method
proves: [correctness, termination, convergence-rate]
status: full
---

**Theorem 1 (the bracket).** Let $f$ be continuous on $[a_0, b_0]$ with $f(a_0) f(b_0) < 0$. At each test of line L3, $a$ and $b$ lie in $[a_0, b_0]$, $f(a) \ne 0$, $f(b) \ne 0$, $f(a)$ and $f(b)$ have opposite signs, and the stored value $f_a$ has the sign of $f(a)$. Hence there is a root $x^*$ of $f$ strictly between $a$ and $b$, and a return at L3 gives $|b - x^*| < |b - a| \le \max(\delta, 4\,\mathrm{ulp})$.

*Proof.* By induction on the number of passes. At the first test, $a = a_0$, $b = b_0$, $f_a = f(a)$, and the claim is the hypothesis. Suppose it holds at a test that does not return. Line L4 computes $x$ strictly between $a$ and $b$: the regula falsi point of two values of opposite signs lies between the ends in exact arithmetic, and the fallback to the midpoint covers the case where rounding puts it on or outside an end. (The midpoint is strictly inside since the width exceeds 4 ulps.) If $f(x) = 0$, line L6 returns a root. Otherwise there are two cases. If $f(x)$ and $f(b)$ have opposite signs (L7, L8), the new pair is $(b, x)$, with $f_a = f(b)$ fresh, so all claims hold. If they have the same sign, then $f(x)$ and $f(a)$ have opposite signs, the new pair is $(a, x)$, and $f_a/2$ has the sign of $f(a)$ (L9). In both cases the new points lie between the old ones, so in $[a_0, b_0]$. The intermediate value theorem gives a root strictly between $a$ and $b$. $\square$

**Theorem 2 (termination).** ILLINOIS ends after at most $k_{\max}$ passes of the loop, so after at most $k_{\max} + 2$ evaluations of $f$.

*Proof.* Each pass evaluates $f$ once at L5 and either returns or goes on to the next value of $k$; the loop has $k_{\max}$ values. $\square$

When it returns at L3 or L6, Theorem 1 bounds the error. When it reaches $k_{\max}$, it reports failure, and the current bracket still holds a root.

**Local analysis (the order $3^{1/3}$).** Let $f \in C^2$ near a simple root $x^*$ with $f'(x^*) \ne 0$ and $M = f''(x^*)/(2f'(x^*)) \ne 0$, and suppose the iterates are close to $x^*$. Write $e$ for errors and work to first order in the errors. Dowell and Jarratt (1971) make this rigorous; we give the derivation.

*Secant step.* If the stored values are exact, $f(u) = f'(x^*)(e_u + M e_u^2 + \cdots)$ and the same at $v$. The zero of the line through $(u, f(u))$ and $(v, f(v))$ has the error $e \approx M e_u e_v$, the classical error equation of the [secant method](/secant-method/). If $u$ and $v$ are on opposite sides, $e_u e_v < 0$, so the new point lies on the side of sign $-\operatorname{sign}(M)$, whatever the signs of $u$ and $v$.

*Halving step.* If the stored value at the far end $u$ is $f(u)/2$ and $|e_v| \ll |e_u|$, the zero of the line through $(u, f(u)/2)$ and $(v, f(v))$ has, to first order,

$$e = e_v - e_v \frac{e_v - e_u}{e_v - e_u/2} = e_v \frac{e_u/2}{e_v - e_u/2} = -e_v\,(1 + O(e_v/e_u) + O(e_u)).$$

So the new point lies on the other side of $x^*$ at almost the same distance.

*The cycle.* Suppose a halving step has just produced $x_k$ with $e_k \approx -e_{k-1}$, so $x_{k-1}$ and $x_k$ are on opposite sides. Step $k+1$ is a secant step between them (both values are exact), so $e_{k+1} \approx M e_{k-1} e_k$, on the side $-\operatorname{sign}(M)$. Since $x_{k-1}$ came from a secant step it was on the side $-\operatorname{sign}(M)$, so $x_k$ is on the side $\operatorname{sign}(M)$, and $x_{k+1}$ is on the side opposite to $x_k$: line L8 swaps, and step $k+2$ is a secant step between $x_k$ and $x_{k+1}$, with $e_{k+2} \approx M e_k e_{k+1}$, again on the side $-\operatorname{sign}(M)$, the same side as $x_{k+1}$. So line L9 halves the value at $x_k$, and step $k+3$ is a halving step with $e_{k+3} \approx -e_{k+2}$. The cycle repeats.

*The order.* Let $\ell_j = \log|e_j|$, ignoring the bounded terms $\log|M|$. In one cycle $\ell_k = \ell_{k-1}$, $\ell_{k+1} = \ell_k + \ell_{k-1} = 2\ell_{k-1}$, $\ell_{k+2} = \ell_{k+1} + \ell_k = 3\ell_{k-1}$, and $\ell_{k+3} = \ell_{k+2} = 3\ell_{k-1}$. Since $\ell_k = \ell_{k-1}$, this is $|e_{k+3}| \approx K |e_k|^3$ in each cycle of three evaluations: the method has order 3 for three evaluations, that is $3^{1/3} \approx 1.442$ in each evaluation, and efficiency index $3^{1/3}$.

This analysis is local: it assumes that the cycle has started. The tests check that $\log|e_{k+3}|/\log|e_k|$ is close to 3 near the root for several functions; the values observed on the page are 3.2 to 3.6. $\blacksquare$
