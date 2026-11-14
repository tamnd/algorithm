---
title: The level set iteration keeps the volume bound, keeps the design under reinitialization, and is exact on linear functions
proves: [correctness, termination]
status: full
---

**Setting.** The grid has $n$ elements and $\phi$ has one value per element. An element is solid if $\phi_e < 0$. Let $N(\phi) = \#\{e : \phi_e < 0\}$. The load $f$ is not zero, the supports remove the rigid body motions, $\varepsilon > 0$, $\Delta t > 0$, and $N(\phi_0) \le B$. The proof uses exact real arithmetic.

**Claim.**

1. Every system of line L4 has a unique solution, and the values $w_e$ of line L5 satisfy $0 \le w_e \le 1$.
2. Every design of the iteration has at most $B$ solid elements.
3. REINIT does not change the set of solid elements.
4. If $\phi_e = a i + b j + c$ on the element $(i, j)$, then at every element that is not on the edge of the grid, $\nabla^+ = \nabla^- = \sqrt{a^2 + b^2}$, and STEP gives $\phi_e - \Delta t\, V_e \sqrt{a^2 + b^2}$.
5. The method stops after iters iterations.

**Step 1 (claim 1).** Every element has a stiffness factor $s_e \ge \varepsilon > 0$, so $K(s)$ is positive definite on the free degrees of freedom and line L4 has a unique solution $u$. Since $f \ne 0$, $u \ne 0$, and $u^{\mathsf T} K u = \sum_e s_e\, u_e^{\mathsf T} k_0 u_e > 0$. The matrix $k_0$ is positive semidefinite, so every $u_e^{\mathsf T} k_0 u_e \ge 0$ and at least one is positive. The mean over neighbours keeps the values at least 0 and keeps a positive value positive (each mean includes the element itself). So the maximum is positive, and after the division $0 \le w_e \le 1$.

**Step 2 (STEP is monotone in the speed).** Fix $\phi$. The values $a_e = \nabla^+_e$ and $b_e = \nabla^-_e$ of line L11 depend only on $\phi$ and are at least 0. Let $g(v) = \max(v, 0)\, a_e + \min(v, 0)\, b_e$. For $v \ge 0$, $g(v) = a_e v$, and for $v \le 0$, $g(v) = b_e v$. Both pieces are nondecreasing and agree at 0, so $g$ is nondecreasing. Line L12 gives $\phi_e - \Delta t\, g(V_e)$, which is nonincreasing in $V_e$. With $V_e = w_e - \ell$, the new value is nondecreasing in $\ell$. So if $\ell \le \ell'$, every element that is solid after the step with $\ell'$ is solid after the step with $\ell$, and $N(\text{STEP}(\phi, w - \ell)) \ge N(\text{STEP}(\phi, w - \ell'))$.

**Step 3 (claim 2).** Suppose $N(\phi) \le B$ at the start of an iteration. With $\ell = 1$, $V_e = w_e - 1 \le 0$ by Step 1, so $g(V_e) \le 0$ and the new $\phi_e$ is at least the old one. So no element becomes solid, and $N(\text{STEP}(\phi, w - 1)) \le N(\phi) \le B$. The code tests $\ell = 1$ first, and this test passes. The bisection keeps the invariant $N(\text{STEP}(\phi, w - h)) \le B$ for its upper end $h$: it moves $h$ only to a midpoint where the count is at most $B$. Line L7 uses $\ell = h$, so the new design has at most $B$ solid elements. By Step 4 below, line L8 does not change the count. By induction from $N(\phi_0) \le B$, claim 2 holds. By Step 2, the count is nonincreasing in $\ell$, so the set of feasible $\ell$ in $[0, 1]$ is an interval that contains 1, and the bisection approaches its left end.

**Step 4 (claim 3).** A point of $P$ lies on the segment from the center of an element $a$ with $\phi_a < 0$ to the center of a neighbour $b$ with $\phi_b \ge 0$, at the fraction $t = \phi_a / (\phi_a - \phi_b)$ from $a$. Since $\phi_a < 0 \le \phi_b$, the denominator is negative and $0 < t \le 1$. So no point of $P$ is the center of a solid element: a point with $t < 1$ is strictly inside a segment of length 1, and a point with $t = 1$ is the center of $b$, which is not solid. Hence for a solid element $e$, the distance $d_e$ to the nearest point of $P$ is positive, and line L14 sets $\phi_e = -d_e < 0$. For an element with $\phi_e \ge 0$, line L14 sets $\phi_e = d_e \ge 0$. So the set of solid elements does not change. If $P$ is empty, the code leaves $\phi$ unchanged.

**Step 5 (claim 4).** For $\phi_e = a i + b j + c$ and an element away from the edge of the grid, $D^-x = D^+x = a$ and $D^-y = D^+y = b$. If $a \ge 0$, then $\max(D^-x, 0)^2 + \min(D^+x, 0)^2 = a^2 + 0$, and if $a < 0$ it is $0 + a^2$. The same holds with max and min swapped, and for $b$. So both squared gradients are $a^2 + b^2$. Then line L12 gives $\phi_e - \Delta t\, (\max(V_e, 0) + \min(V_e, 0)) \sqrt{a^2 + b^2} = \phi_e - \Delta t\, V_e \sqrt{a^2 + b^2}$, which is the exact solution of $\phi_t + V |\nabla \phi| = 0$ for a constant speed over the time $\Delta t$ on a linear $\phi$.

**Step 6 (claim 5).** The loop of line L2 runs iters times. Each iteration has one solve, at most steps $+ 1$ calls of STEP, and at most one REINIT, each with a finite number of operations.

**Remark.** The claims are about the bookkeeping of the method. The compliance of the iterates is not proved to decrease, and the tests measure that it can rise. The test of claim 4 uses exact fractions, and the other tests use floats. $\blacksquare$
