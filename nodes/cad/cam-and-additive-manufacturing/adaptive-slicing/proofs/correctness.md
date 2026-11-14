---
title: Greedy adaptive slicing keeps the cusp bound in every feasible layer and stops
proves: [correctness, termination]
status: full
---

**Claim.** Let $M$ be a triangle mesh with exact (integer or rational) vertices, let $0 < t_1 < \dots < t_r$ be the allowed thicknesses and let $c > 0$. For a height $z$ and a thickness $s$, call the layer $(z, s)$ feasible if every facet $f$ with $z_{\min}(f) < z + s$ and $z_{\max}(f) > z$ has $s\,|n_{f,z}| / \|n_f\| \le c$. Then ADAPTIVE-SLICE$(M, T, c)$ stops after at most $\lceil (z_{\max}(M) - z_{\min}(M)) / t_1 \rceil$ layers, the last output is at least $z_{\max}(M)$, and each layer $(z, t)$ that it outputs satisfies:

1. if some allowed thickness gives a feasible layer at $z$, then $t$ is the largest such thickness, and the layer $(z, t)$ is feasible;
2. otherwise $t = t_1$.

**Step 1 (the test is exact).** For a facet with normal $n \ne 0$ and $s > 0$, both $s\,|n_z| / \|n\|$ and $c$ are non-negative. For non-negative reals $a$ and $b$, $a \le b$ if and only if $a^2 \le b^2$. So $s\,|n_z| / \|n\| \le c$ if and only if $s^2 n_z^2 \le c^2 \|n\|^2$, after multiplying by $\|n\|^2 > 0$. Both sides are polynomials in the exact input, so line L9 decides the condition without error. Line L9 also checks the slab condition exactly as in the definition. So FEASIBLE$(z, s)$ returns false if and only if some facet in the open slab breaks the bound, that is, if and only if the layer $(z, s)$ is not feasible. (A facet with $n = 0$, a degenerate triangle, has $n_z = 0$ and $\|n\| = 0$, so line L9 never rejects it, which is the right answer for a facet of zero area.)

**Step 2 (monotonicity).** Let $(z, s)$ be feasible and $0 < s' < s$. A facet in the slab $(z, z + s')$ has $z_{\min}(f) < z + s' < z + s$ and $z_{\max}(f) > z$, so it is also in the slab $(z, z + s)$. Then $s'^2 n_z^2 \le s^2 n_z^2 \le c^2 \|n\|^2$. So $(z, s')$ is feasible. In other words, the set of allowed thicknesses that are feasible at $z$ is $\{t_1, \dots, t_q\}$ for some $q \in \{0, \dots, r\}$.

**Step 3 (one layer).** Fix one pass of the loop of line L2, with current height $z$. Lines L4 and L5 call FEASIBLE with $t_r, t_{r-1}, \dots$ in this order and stop at the first true answer. By Steps 1 and 2, the calls return false for $t_r, \dots, t_{q+1}$ and true for $t_q$ if $q \ge 1$. So if $q \ge 1$, the pass sets $t = t_q$, the largest feasible thickness, and the layer $(z, t_q)$ is feasible. If $q = 0$, no call returns true, and $t$ keeps the value $t_1$ of line L3. This proves parts 1 and 2 for this layer.

**Step 4 (termination and cover).** Let $z^{(0)} = z_{\min}(M)$ and let $z^{(i)}$ be the value of $z$ after $i$ passes. Each pass adds an allowed thickness, so $z^{(i)} \ge z^{(0)} + i\, t_1$. The loop runs only while $z < z_{\max}(M)$. So if $i$ passes have run, then $z^{(i-1)} < z_{\max}(M)$, and $z^{(0)} + (i - 1) t_1 < z_{\max}(M)$, which gives $i < (z_{\max} - z_{\min}) / t_1 + 1$, that is $i \le \lceil (z_{\max} - z_{\min}) / t_1 \rceil$. When the loop stops, $z \ge z_{\max}(M)$, so the last output is at least $z_{\max}(M)$. If $z_{\max}(M) = z_{\min}(M)$, the loop does not run, and the output is empty, which is correct for a flat mesh. Each call of FEASIBLE scans a finite list, so each pass stops. $\blacksquare$
