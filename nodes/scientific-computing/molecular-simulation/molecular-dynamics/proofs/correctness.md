---
title: The molecular dynamics loop is velocity Verlet, conserves momentum for pair forces, and is time-reversible
proves: [correctness]
status: full
---

We use the pseudocode of the page and exact arithmetic. Write $a_i(x) = f_i(x) / m_i$, and let $(x^s, v^s)$ be the state after step $s$, with $(x^0, v^0)$ the input. Without a box, let $\text{wrap}$ be the identity. With a box of side $L$, $\text{wrap}$ reduces each coordinate modulo $L$.

**Claim 1 (the loop is velocity Verlet).** For each $s \ge 1$,
$$v^{s - 1/2} = v^{s-1} + \tfrac{h}{2} a(x^{s-1}), \qquad x^s = \text{wrap}\bigl(x^{s-1} + h v^{s - 1/2}\bigr), \qquad v^s = v^{s - 1/2} + \tfrac{h}{2} a(x^s).$$

*Proof.* We show by induction that at the start of step $s$ the stored forces are $f(x^{s-1})$. For $s = 1$, line L1 computes $f(x^0)$. Line L5 of step $s$ computes $f(x^s)$ and no line changes $f$ after it, which gives the claim for $s + 1$. Given this, line L3 is the first equation. Line L4 uses the new velocity of the same atom, which line L3 has just computed, so it is the second equation. Line L5 computes $f(x^s)$ and line L6 is the third equation. The loops over atoms in lines L3, L4 and L6 read only the stored forces, which do not change inside them, so the order of the atoms does not matter. $\square$

So the map from $(x^{s-1}, v^{s-1})$ to $(x^s, v^s)$ is the velocity Verlet map of Swope, Andersen, Berens and Wilson, composed with a wrap of the positions. Its order 2 and its symplecticity are proved on the [Verlet integration](/verlet-integration/) page.

**Claim 2 (forces of the box do not depend on the wrap).** With the minimum image convention, $f(x) = f(x + L z)$ for each integer vector $z$ that shifts each coordinate of each atom by a multiple of $L$.

*Proof.* The Lennard-Jones forces depend on $x$ only through the minimum images $\text{mi}(x_i - x_j)$, where $\text{mi}(d) = d - L \, \text{round}(d / L)$ in each coordinate. A shift of $x_i$ and $x_j$ by multiples of $L$ changes $d = x_i - x_j$ by a multiple $cL$ of $L$, and $\text{round}((d + cL)/L) = \text{round}(d/L) + c$, so $\text{mi}(d)$ does not change. $\square$

So a wrap of the positions does not change any later force, and the dynamics with the wrap is the dynamics without it, followed by a wrap.

**Claim 3 (momentum).** If $f$ is a sum of pair forces, $f_i = \sum_{j \ne i} g_{ij}$ with $g_{ji} = -g_{ij}$, then $P = \sum_i m_i v_i$ is the same after every step.

*Proof.* The implementation computes $g_{ij}$ once for each pair $i < j$, adds it to $f_i$ and subtracts it from $f_j$, so $\sum_i f_i = 0$ for every $x$. Line L3 changes $P$ by $\sum_i m_i \cdot \frac{h}{2} f_i / m_i = \frac{h}{2} \sum_i f_i = 0$, and so does line L6. Line L4 does not change the velocities. $\square$

The spring field $f_i = -k x_i$ is an external force, so Claim 3 does not apply to it, and the momentum of a spring oscillates as it should.

**Claim 4 (time reversal).** Let one step map $(x, v)$ to $(x', v')$ without the wrap. Then one step maps $(x', -v')$ to $(x, -v)$. With the wrap, it maps $(\text{wrap}(x'), -v')$ to $(x + L z, -v)$ for an integer vector $z$.

*Proof.* Without the wrap, the step gives $w = v + \frac{h}{2} a(x)$, $x' = x + h w$ and $v' = w + \frac{h}{2} a(x')$. Start at $(x', -v')$. Line L3 gives $-v' + \frac{h}{2} a(x') = -w$. Line L4 gives $x' - h w = x$. Line L6 gives $-w + \frac{h}{2} a(x) = -v$. With the wrap, the start is $x' + L z'$ for some $z'$. By Claim 2 the forces are the same as at $x'$, so the velocities are the same as above, and the positions differ from those above by the multiple $L z'$ of $L$ and by the wraps. $\square$

By induction on the number of steps, $S$ steps from $(x^S, -v^S)$ return to $(x^0, -v^0)$, up to multiples of $L$ in the positions.

**Claim 5 (the recorded energy).** The $s$-th recorded value is $H(x^s, v^s) = \sum_i \frac12 m_i |v_i^s|^2 + U(x^s)$.

*Proof.* Line L1 records $K(v^0) + U(x^0)$. In step $s$, line L5 sets $U = U(x^s)$, line L6 sets the velocities to $v^s$, and line L7 records $K(v^s) + U(x^s)$. $\square$

**What is not claimed.** $H$ is not conserved exactly. For the spring $U = \frac{k}{2} x^2$ with $m = 1$ and $\omega^2 = k$, the method conserves the modified energy $v^2 + \omega^2 (1 - h^2 \omega^2 / 4) x^2$, as the [Verlet integration](/verlet-integration/) page proves, so $H$ differs from its start by $\frac{h^2 \omega^4}{8}(x^2 - x_0^2)$, which is $O(h^2)$ for all time when $h \omega < 2$. In floating-point arithmetic, Claims 3 and 4 hold up to rounding.
