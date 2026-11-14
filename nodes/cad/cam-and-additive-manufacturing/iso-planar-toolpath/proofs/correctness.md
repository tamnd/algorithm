---
title: On a bilinear patch with x growing in v, each drive plane cuts one exact curve, and the refinement stops with every chord passing its midpoint test
proves: [correctness, termination]
status: full
---

**Setting.** $S(u, v)$ is a bilinear patch on $[0, 1]^2$ with rational corners. Its first coordinate is $x(u, v) = A + Bu + Cv + Duv$, and the code requires $C > 0$ and $C + D > 0$. The drive planes are $x = c_k = x_{\min} + g/2 + kg$ with $c_k < x_{\max}$, where $x_{\min}$ and $x_{\max}$ are the smallest and largest $x$ of a corner. $\varepsilon > 0$ is the chord tolerance and $m$ the depth limit.

**Claim.** (a) $x_v(u) = C + Du > 0$ for all $u \in [0, 1]$, and for each $c$ the set $\Sigma_c = \{(u, v) \in [0, 1]^2 : x(u, v) = c\}$ is the graph of $v(u) = (c - A - Bu)/(C + Du)$ over the interval of line L2, or empty when line L2 finds no interval. (b) Every point the code returns lies exactly on the plane $x = c$ and on the patch. (c) The refinement of line L5 stops, returns at most $2^m$ chords, and every chord whose recursion did not hit the depth limit passes the midpoint test. (d) The loop of line L1 stops after at most $\lceil (x_{\max} - x_{\min})/g \rceil$ planes.

**Proof of (a).** $C + Du$ is affine in $u$, positive at $u = 0$ and at $u = 1$, so it is positive on $[0, 1]$. For a fixed $u$, $x(u, \cdot)$ is affine in $v$ with positive slope $C + Du$, so $x(u, v) = c$ has exactly one solution $v = v(u)$. That point is on the patch when $0 \le v(u) \le 1$. Multiplying by the positive denominator, this is $c - A - Bu \ge 0$ and $c - A - Bu \le C + Du$, two affine inequalities in $u$. The set of $u \in [0, 1]$ that satisfy two affine inequalities is an interval (possibly empty), and line L2 computes it by intersecting $[0, 1]$ with the half-line of each inequality: for $a u + b \ge 0$ it is $u \ge -b/a$ when $a > 0$, $u \le -b/a$ when $a < 0$, and all or nothing when $a = 0$. So $\Sigma_c$ is the graph of $v$ over this interval, which is a single connected curve.

**Proof of (b).** Each returned point is $S(u, v(u))$ with $u$ in the interval of (a), so it is on the patch, and $x(S(u, v(u))) = x(u, v(u)) = c$ by the choice of $v(u)$. The values are rationals, so both facts hold exactly.

**Proof of (c).** Each call either appends one end and returns, or makes two calls with the depth one smaller. A call at depth 0 never recurses, so the recursion tree has height at most $m$ and at most $2^m$ leaves, and each leaf appends one chord end. The chords are the parameter intervals of the leaves, which partition $[u_{\mathrm{lo}}, u_{\mathrm{hi}}]$ in order. A leaf reached with depth above 0 did not recurse, so its curve midpoint is within $\varepsilon$ of its chord.

**Proof of (d).** Each pass of the loop adds $g > 0$ to $c$, and the loop stops when $c \ge x_{\max}$. $\blacksquare$

**What is not proved.** The midpoint test does not bound the distance from every point of the curve to its chord, so the chord error is measured in the tests, not proved. The spacing of the passes on the surface is a first-order estimate: the gradient of $x$ along the surface has length $\sqrt{1 - n_x^2}$, where $n$ is the unit normal, so two level curves of $x$ that differ by $g$ lie about $g/\sqrt{1 - n_x^2}$ apart on the surface. For the plane $z = mx$ this is exact: the passes $x = c$ and $x = c + g$ are parallel lines at distance $g\sqrt{1 + m^2}$, and $n_x^2 = m^2/(1 + m^2)$. On a curved patch the tests measure the estimate within 10 percent for $g = 1/4$.
