---
title: The four-point kernel meets Peskin's conditions, spreading is the adjoint of interpolation, and spreading keeps total force and torque
proves: [correctness, termination]
status: full
---

**Setting.** The grid and the operators are those of the main page. Each velocity component lives on its own lattice of spacing $h$: the $u$ faces at $(ih, (j + \tfrac12)h)$ and the $v$ faces at $((i + \tfrac12)h, jh)$. Interpolation and spreading at a point $\mathbf{X}$ use

$$\delta_h(\mathbf{x} - \mathbf{X}) = \frac{1}{h^2}\,\phi\!\left(\frac{x - X}{h}\right)\phi\!\left(\frac{y - Y}{h}\right),$$

$$U(\mathbf{X}_l) = \sum_{\mathbf{x}} \mathbf{u}(\mathbf{x})\,\delta_h(\mathbf{x} - \mathbf{X}_l)\,h^2, \qquad \mathbf{f}(\mathbf{x}) = \sum_l \mathbf{F}_l\,\delta_h(\mathbf{x} - \mathbf{X}_l)\,\Delta s,$$

each component on its own lattice. The kernel is $\phi(r) = (3 - 2|r| + \sqrt{1 + 4|r| - 4r^2})/8$ for $|r| \le 1$, $\phi(r) = (5 - 2|r| - \sqrt{-7 + 12|r| - 4r^2})/8$ for $1 \le |r| \le 2$, and 0 otherwise.

**Lemma 1 (kernel conditions).** For every real $r$,

$$\sum_{j\ \text{even}}\phi(r - j) = \sum_{j\ \text{odd}}\phi(r - j) = \tfrac12, \qquad \sum_j (r - j)\,\phi(r - j) = 0, \qquad \sum_j \phi(r - j)^2 = \tfrac38.$$

In particular $\sum_j \phi(r - j) = 1$.

*Proof.* Replacing $r$ by $r + 1$ shifts the index $j$ by one, which swaps the even and odd sums and leaves the other two sums unchanged. So it is enough to take $0 \le r < 1$. Then only $j = -1, 0, 1, 2$ give nonzero terms, at the distances $r + 1$, $r$, $1 - r$ and $2 - r$. Let $\sigma = \sqrt{1 + 4r - 4r^2}$, which is real because $1 + 4r - 4r^2 \ge 1$ on $[0, 1]$. Put the distances into the formulas:

- $\phi(2 - r)$: here $-7 + 12(2 - r) - 4(2 - r)^2 = 1 + 4r - 4r^2$, so $\phi(2 - r) = (1 + 2r - \sigma)/8 =: t$.
- $\phi(r) = (3 - 2r + \sigma)/8 = \tfrac12 - t$.
- $\phi(1 - r)$: here $1 + 4(1 - r) - 4(1 - r)^2 = 1 + 4r - 4r^2$, so $\phi(1 - r) = (1 + 2r + \sigma)/8 = \tfrac{1 + 2r}{4} - t$.
- $\phi(1 + r)$: here $-7 + 12(1 + r) - 4(1 + r)^2 = 1 + 4r - 4r^2$, so $\phi(1 + r) = (3 - 2r - \sigma)/8 = \tfrac{1 - 2r}{4} + t$.

The even indices are $j = 0, 2$: $(\tfrac12 - t) + t = \tfrac12$. The odd indices are $j = -1, 1$: $\tfrac{1 - 2r}{4} + t + \tfrac{1 + 2r}{4} - t = \tfrac12$. The first moment is $(r + 1)\phi(1 + r) + r\phi(r) + (r - 1)\phi(1 - r) + (r - 2)\phi(2 - r) = r \cdot 1 + \phi(1 + r) - \phi(1 - r) - 2t = r + \tfrac{1 - 2r}{4} - \tfrac{1 + 2r}{4} + 2t - 2t = 0$. For the squares, write $a = \tfrac{1 - 2r}{4}$ and $b = \tfrac{1 + 2r}{4}$:

$$(a + t)^2 + (\tfrac12 - t)^2 + (b - t)^2 + t^2 = 4t^2 - (1 + 2r)t + a^2 + b^2 + \tfrac14,$$

since $2a - 2b - 1 = -(1 + 2r)$, and $a^2 + b^2 = (1 + 4r^2)/8$. The number $t$ is a root of $4t^2 - (1 + 2r)t + r^2/2 = 0$, because the roots are $((1 + 2r) \pm \sqrt{(1 + 2r)^2 - 8r^2})/8$ and $(1 + 2r)^2 - 8r^2 = 1 + 4r - 4r^2 = \sigma^2$. So the sum of squares is $-r^2/2 + (1 + 4r^2)/8 + \tfrac14 = \tfrac38$. $\square$

The two formulas agree at $|r| = 1$ (both give $1/4$) and the outer one is 0 at $|r| = 2$, so $\phi$ is continuous with support $[-2, 2]$. The test file checks the four conditions at 205 values of $r$ to $10^{-14}$.

**Corollary (moments of $\delta_h$).** On each lattice and for every point $\mathbf{X}$, $\sum_{\mathbf{x}}\delta_h(\mathbf{x} - \mathbf{X})h^2 = 1$ and $\sum_{\mathbf{x}}(\mathbf{x} - \mathbf{X})\,\delta_h(\mathbf{x} - \mathbf{X})h^2 = 0$, where $\mathbf{x}$ runs over the lattice points near $\mathbf{X}$ without wrapping.

*Proof.* The sum factors into a sum over $i$ and a sum over $j$. A lattice offset ($\tfrac12$ in one direction) only shifts $r$, and Lemma 1 holds for every real $r$. For the first moment in $x$, the $x$ factor is $h\sum_i (r - i)\phi(r - i) = 0$ up to sign and the $y$ factor is 1. $\square$

**Theorem 1 (spreading is the adjoint of interpolation).** For all grid velocities $\mathbf{u}$, point forces $\mathbf{F}_l$ and points $\mathbf{X}_l$,

$$\sum_{\mathbf{x}} \mathbf{f}(\mathbf{x})\cdot\mathbf{u}(\mathbf{x})\,h^2 = \sum_l \mathbf{F}_l\cdot U(\mathbf{X}_l)\,\Delta s.$$

*Proof.* Both sides equal $\sum_l\sum_{\mathbf{x}} \mathbf{F}_l\cdot\mathbf{u}(\mathbf{x})\,\delta_h(\mathbf{x} - \mathbf{X}_l)\,h^2\Delta s$, component by component on each lattice; the two sides only sum in a different order. Periodic wrapping of the stencil does not matter, because both operators use the same wrapped indices and weights. $\square$

So the power that the membrane puts into the fluid, computed on the grid, equals the power computed at the points. This is the discrete form of the identity that gives energy balance for the continuous immersed boundary equations. The test file checks it with random data to $10^{-12}$, with points near the edges of the box.

**Theorem 2 (total force and torque).** If no stencil wraps around the box, then $\sum_{\mathbf{x}}\mathbf{f}h^2 = \sum_l\mathbf{F}_l\Delta s$ and $\sum_{\mathbf{x}}(x f_v - y f_u)h^2 = \sum_l (X_l F_{y,l} - Y_l F_{x,l})\Delta s$, with $f_u$ summed over the $u$ lattice and $f_v$ over the $v$ lattice.

*Proof.* Swap the sums: $\sum_{\mathbf{x}}\mathbf{f}h^2 = \sum_l \mathbf{F}_l\Delta s\sum_{\mathbf{x}}\delta_h(\mathbf{x} - \mathbf{X}_l)h^2 = \sum_l\mathbf{F}_l\Delta s$ by the corollary. For the torque, $\sum_{\mathbf{x}} x\,\delta_h(\mathbf{x} - \mathbf{X}_l)h^2 = X_l$ on the $v$ lattice by the two moment conditions, and the same for $y$ on the $u$ lattice. $\square$

**Theorem 3 (incompressibility).** After every step the grid velocity satisfies $D\mathbf{u} = 0$, for every membrane force.

*Proof.* Line L4 is the projection of the [Chorin projection method](/chorin-projection-method/), whose proof shows that $-DG$ is the periodic 5-point matrix, that the right side $-D\mathbf{u}^*$ sums to zero, and that $D(\mathbf{u}^* - Gq) = 0$ for the solution $q$. The spread force enters only $\mathbf{u}^*$. $\square$

**Termination.** One step evaluates $m$ spring forces, spreads and interpolates over 16 grid points per component per membrane point, and solves one Poisson equation with conjugate gradients, which stops after at most its iteration limit. So each step ends after a bounded amount of work.

**What is not proved.** The discrete pressure jump of a static circle is measured, not proved: the spread force is not exactly a discrete gradient, so a small divergence-free part remains. The stability of the explicit step and the accuracy of the method near the membrane (first order in $h$ for the velocity in general, because the force is singular) are not proved here.
