---
title: The profile of the integration method lies above every admissible profile, so it is time-optimal
proves: [correctness, optimality]
status: full
---

We use the notation of the page. The path parameter is $s \in [0, 1]$, the state is $x = \dot s^2 \ge 0$, and the control is $u = \ddot s$, so that $dx/ds = 2u$ wherever $x > 0$. At each $(s, x)$ the admissible controls form the interval $[L(s, x), U(s, x)]$, and the maximum velocity curve $\mathrm{MVC}(s)$ is the largest $x$ with $L(s, x) \le U(s, x)$.

**Definition.** An admissible profile is an absolutely continuous function $x : [0, 1] \to [0, \infty)$ with $x(0) = x(1) = 0$, $x(s) \le \mathrm{MVC}(s)$ for all $s$, and $2L(s, x(s)) \le x'(s) \le 2U(s, x(s))$ for almost every $s$. Its traversal time is $T(x) = \int_0^1 ds / \sqrt{x(s)}$.

**Hypotheses.** (H1) The constraint rows depend continuously on $s$, so $L$ and $U$ are continuous on the region below the MVC. (H2) $L$ and $U$ are Lipschitz in $x$ there. Both hold for torque limits: for fixed $s$, $L$ and $U$ are the largest and the smallest of finitely many affine functions of $x$. (H3) The algorithm is run with exact integration and an exact binary search, and it returns a profile. That is, every curve it integrates exists on the interval it needs, each binary search ends at an $L$ curve that touches the MVC at a point $(s_k, \mathrm{MVC}(s_k))$, and there are finitely many switches.

The proof does not use the RK4 step or the stopping tolerance of the code; their errors are discussed on the page.

## Comparison of curves

**Lemma 1 (forward comparison).** Let $A$ solve $A' = 2U(s, A)$ on $[a, b]$ and let $x$ be admissible. If $x(a) \le A(a)$, then $x(s) \le A(s)$ for $s \in [a, b]$.

*Proof.* Let $w = x - A$. Where $w > 0$, we have $w' \le 2U(s, x) - 2U(s, A) \le 2\lambda w$, with $\lambda$ the Lipschitz constant of (H2). Suppose $w(s_1) > 0$ for some $s_1$, and let $s_0 = \sup\{s \le s_1 : w(s) \le 0\}$, so $w(s_0) = 0$ and $w > 0$ on $(s_0, s_1]$. Gronwall's inequality on $(s_0, s_1]$ gives $w(s_1) \le w(s_0) e^{2\lambda(s_1 - s_0)} = 0$, a contradiction. $\square$

**Lemma 2 (backward comparison).** Let $D$ solve $D' = 2L(s, D)$ on $[a, b]$ and let $x$ be admissible. If $x(b) \le D(b)$, then $x(s) \le D(s)$ for $s \in [a, b]$.

*Proof.* Put $r = -s$. Then $dx/dr = -x'(s) \le -2L(s, x)$ and $dD/dr = -2L(s, D)$, and $-L$ is Lipschitz in $x$. Lemma 1 applied in the variable $r$ from $r = -b$ gives the claim. $\square$

## The structure of the result

Under (H3) the returned profile $x^*$ is made of pieces of two kinds. The switch points of type "L to U" are $0 = t_0 < t_1 < \dots < t_k$, where $t_0$ is the start and $t_1, \dots, t_k$ are the tangent points of line L8. The switch points of type "U to L" are $\sigma_1 < \dots < \sigma_{k+1}$ with $t_{j-1} < \sigma_j \le t_j$ for $j \le k$ and $t_k < \sigma_{k+1} \le 1$; they come from lines L10 and L5. On $[t_{j-1}, \sigma_j]$ the profile is the $U$ curve that starts at $(t_{j-1}, x^*(t_{j-1}))$ (lines L4 and L11). On $[\sigma_j, t_j]$ it is the $L$ curve that ends at the tangent point (line L9), and on $[\sigma_{k+1}, 1]$ it is the curve $F$ of line L1, an $L$ curve that ends at $(1, 0)$.

**Lemma 3.** $x^*$ is admissible.

*Proof.* $x^*$ is continuous, because each switch point is a point where the two curves meet (lines L5 and L10) and each tangent point is the end of one piece and the start of the next. Each piece solves $x' = 2U$ or $x' = 2L$, so $2L \le x^{*\prime} \le 2U$ holds on each piece. Every integration stops when a curve goes above the MVC (lines L4, L7 and L9), and the pieces that are kept are the parts below it, so $x^* \le \mathrm{MVC}$. Finally $x^*(0) = 0$ and $x^*(1) = 0$. $\square$

## Optimality

**Lemma 4.** Every admissible profile $x$ satisfies $x(s) \le x^*(s)$ for all $s \in [0, 1]$.

*Proof.* At every left end of an acceleration piece, $x \le x^*$: at $t_0 = 0$ both are $0$, and at a tangent point $t_j$ we have $x(t_j) \le \mathrm{MVC}(t_j) = x^*(t_j)$ because $x$ is admissible. Lemma 1 then gives $x \le x^*$ on each $[t_{j-1}, \sigma_j]$. At every right end of a deceleration piece, $x \le x^*$ for the same two reasons: at $s = 1$ both are $0$, and at $t_j$ the MVC bounds $x$. Lemma 2 then gives $x \le x^*$ on each $[\sigma_j, t_j]$ and on $[\sigma_{k+1}, 1]$. These intervals cover $[0, 1]$. $\square$

**Theorem.** Under (H1) to (H3), the profile $x^*$ returned by the algorithm is admissible and has the least traversal time among all admissible profiles.

*Proof.* Lemma 3 gives admissibility. By Lemma 4, $1/\sqrt{x^*(s)} \le 1/\sqrt{x(s)}$ wherever $x(s) > 0$, and where $x(s) = 0$ on a set of positive length, $T(x) = \infty$. So $T(x^*) \le T(x)$ for every admissible $x$. $\blacksquare$

## Remarks

The theorem is the optimality of the bang-bang structure: the fastest profile uses the largest or the smallest admissible acceleration at every point, and switches from the smallest to the largest only on the MVC. This is the result of Bobrow, Dubowsky and Gibson (1985) and of Shin and McKay (1985), in the form of Lynch and Park (Section 9.4).

Hypothesis (H3) is where the algorithm can fail. If the MVC has a flat part from a velocity limit, or a singular arc where the profile must follow the MVC with a control strictly between $L$ and $U$, no $L$ curve touches the MVC at a single point, and the binary search of line L7 does not end at a tangent point. Pfeiffer and Johanni (1987) and Pham (2014) treat these cases. The proof also assumes exact integration. With RK4 at step $h$, the computed curves differ from the exact ones by $O(h^4)$ where $L$ and $U$ are smooth, but only by $O(h)$ near the corners of the MVC and near switch points, where the right-hand side is not smooth; the tangent point is found only to the resolution of the grid.
