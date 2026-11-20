---
title: The Boris step solves the implicit midpoint equation, rotates the velocity without changing its length, keeps the E×B drift, is time reversible and preserves phase space volume
proves: [correctness]
status: full
---

We use the pseudocode of the page and exact arithmetic. Fix one pass of lines L2 to L8 at the position $\mathbf{x}$, with $\mathbf{e} = \mathbf{E}(\mathbf{x})$, $\mathbf{b} = \mathbf{B}(\mathbf{x})$, $a = q h / (2m)$, $\mathbf{t} = a \mathbf{b}$, $\tau = |\mathbf{t}|$ and $\mathbf{s} = 2\mathbf{t} / (1 + \tau^2)$. Write $\mathbf{v}$ for the velocity before the pass, $\mathbf{p} = \mathbf{v}^- = \mathbf{v} + a\mathbf{e}$, $\mathbf{u} = \mathbf{v}^+$, and $\mathbf{w} = \mathbf{u} + a\mathbf{e}$ for the velocity after line L7. We use $(\mathbf{a} \times \mathbf{b}) \times \mathbf{c} = \mathbf{b}(\mathbf{a} \cdot \mathbf{c}) - \mathbf{a}(\mathbf{b} \cdot \mathbf{c})$.

**Claim 1 (the midpoint equation).** $\mathbf{w}$ is the unique solution of $\mathbf{w} - \mathbf{v} = (q h / m) \bigl(\mathbf{e} + \tfrac{1}{2}(\mathbf{w} + \mathbf{v}) \times \mathbf{b}\bigr)$.

*Proof.* Since $\mathbf{w} - \mathbf{v} = \mathbf{u} - \mathbf{p} + 2a\mathbf{e}$ and $\mathbf{w} + \mathbf{v} = \mathbf{u} + \mathbf{p}$, the equation is the same as
$$\mathbf{u} - \mathbf{p} = (\mathbf{u} + \mathbf{p}) \times \mathbf{t}. \tag{R}$$
Uniqueness: if two solutions $\mathbf{u}_1$ and $\mathbf{u}_2$ exist, their difference $\mathbf{d}$ satisfies $\mathbf{d} = \mathbf{d} \times \mathbf{t}$, so $|\mathbf{d}|^2 = \mathbf{d} \cdot (\mathbf{d} \times \mathbf{t}) = 0$. Existence: lines L5 and L6 give $\mathbf{D} = \mathbf{u} - \mathbf{p} = \mathbf{v}' \times \mathbf{s}$ with $\mathbf{v}' = \mathbf{p} + \mathbf{p} \times \mathbf{t}$. Using $(\mathbf{p} \times \mathbf{t}) \times \mathbf{t} = \mathbf{t}(\mathbf{p} \cdot \mathbf{t}) - \tau^2 \mathbf{p}$,
$$\mathbf{D} = \frac{2}{1 + \tau^2} \bigl(\mathbf{p} \times \mathbf{t} + \mathbf{t}(\mathbf{p} \cdot \mathbf{t}) - \tau^2 \mathbf{p}\bigr).$$
Then $\mathbf{D} \times \mathbf{t} = \frac{2}{1 + \tau^2} \bigl(\mathbf{t}(\mathbf{p} \cdot \mathbf{t}) - \tau^2 \mathbf{p} - \tau^2 \, \mathbf{p} \times \mathbf{t}\bigr)$, and
$$(\mathbf{u} + \mathbf{p}) \times \mathbf{t} = 2\,\mathbf{p} \times \mathbf{t} + \mathbf{D} \times \mathbf{t} = \frac{2}{1 + \tau^2} \bigl((1 + \tau^2)\,\mathbf{p} \times \mathbf{t} + \mathbf{t}(\mathbf{p} \cdot \mathbf{t}) - \tau^2 \mathbf{p} - \tau^2 \, \mathbf{p} \times \mathbf{t}\bigr) = \mathbf{D}.$$
So $\mathbf{u}$ satisfies (R). $\square$

**Claim 2 (a rotation).** $|\mathbf{u}| = |\mathbf{p}|$, and if $\tau > 0$ then $\mathbf{u}$ is $\mathbf{p}$ turned about the unit vector $\mathbf{n} = \mathbf{t} / \tau$ by the angle $-2 \arctan \tau$ (right-hand rule). With $\mathbf{e} = 0$ the speed is conserved exactly.

*Proof.* The dot product of (R) with $\mathbf{u} + \mathbf{p}$ gives $|\mathbf{u}|^2 - |\mathbf{p}|^2 = 0$. The dot product of (R) with $\mathbf{t}$ gives $(\mathbf{u} - \mathbf{p}) \cdot \mathbf{t} = 0$, so the components along $\mathbf{n}$ agree. For the components $\mathbf{u}_\perp$ and $\mathbf{p}_\perp$ normal to $\mathbf{n}$, (R) reads $\mathbf{u}_\perp - \mathbf{p}_\perp = \tau J(\mathbf{u}_\perp + \mathbf{p}_\perp)$ with $J \mathbf{y} = \mathbf{y} \times \mathbf{n}$, which is the turn by $-\pi/2$ about $\mathbf{n}$ in the plane normal to $\mathbf{n}$. Identify that plane with $\mathbb{C}$ so that $J$ is multiplication by $-\mathrm{i}$. Then $\mathbf{u}_\perp = \frac{1 - \mathrm{i}\tau}{1 + \mathrm{i}\tau} \mathbf{p}_\perp$, and $\frac{1 - \mathrm{i}\tau}{1 + \mathrm{i}\tau} = e^{-2\mathrm{i} \arctan \tau}$. With $\mathbf{e} = 0$, $\mathbf{p} = \mathbf{v}$ and $\mathbf{w} = \mathbf{u}$, so $|\mathbf{w}| = |\mathbf{v}|$. $\square$

Since $\tau = |q| |\mathbf{b}| h / (2m)$, the angle is $2 \arctan(|\Omega| h / 2)$, with the sense of $-q\mathbf{b}$.

**Claim 3 (the drift).** If $\mathbf{e} \cdot \mathbf{b} = 0$, $\mathbf{b} \ne 0$ and $\mathbf{v} = \mathbf{v}_d = \mathbf{e} \times \mathbf{b} / |\mathbf{b}|^2$, then $\mathbf{w} = \mathbf{v}_d$.

*Proof.* $\mathbf{v}_d \times \mathbf{b} = ((\mathbf{e} \times \mathbf{b}) \times \mathbf{b}) / |\mathbf{b}|^2 = (\mathbf{b}(\mathbf{e} \cdot \mathbf{b}) - \mathbf{e} |\mathbf{b}|^2) / |\mathbf{b}|^2 = -\mathbf{e}$. So $\mathbf{w} = \mathbf{v}_d$ makes both sides of the equation of Claim 1 zero, and by uniqueness it is the result. $\square$

**Claim 4 (time reversibility).** Write $K_{\mathbf{B}}(\mathbf{x}, \mathbf{v})$ for the result of lines L3 to L7. Then $K_{-\mathbf{B}}(\mathbf{x}, -K_{\mathbf{B}}(\mathbf{x}, \mathbf{v})) = -\mathbf{v}$. Let the forward run produce $\mathbf{x}_0, \ldots, \mathbf{x}_T$ and $\mathbf{v}_{-1/2}, \ldots, \mathbf{v}_{T+1/2}$ (one more kick after the last pass). Then $T$ passes with $\mathbf{B}$ replaced by $-\mathbf{B}$, from $(\mathbf{x}_T, -\mathbf{v}_{T+1/2})$, return $(\mathbf{x}_0, -\mathbf{v}_{1/2})$.

*Proof.* Let $\mathbf{w} = K_{\mathbf{B}}(\mathbf{x}, \mathbf{v})$. By Claim 1, $K_{-\mathbf{B}}(\mathbf{x}, -\mathbf{w})$ is the unique $\mathbf{z}$ with $\mathbf{z} + \mathbf{w} = (q h / m)(\mathbf{e} + \tfrac{1}{2}(\mathbf{z} - \mathbf{w}) \times (-\mathbf{b}))$. Put $\mathbf{z} = -\mathbf{v}$: the equation becomes $\mathbf{w} - \mathbf{v} = (q h / m)(\mathbf{e} + \tfrac{1}{2}(\mathbf{v} + \mathbf{w}) \times \mathbf{b})$, which holds. For the run, show by induction on $k$ that the backward state after $k$ passes is $(\mathbf{x}_{T-k}, -\mathbf{v}_{T-k+1/2})$. It holds for $k = 0$. If it holds for $k$, the kick gives $K_{-\mathbf{B}}(\mathbf{x}_{T-k}, -\mathbf{v}_{T-k+1/2}) = -\mathbf{v}_{T-k-1/2}$, because $\mathbf{v}_{T-k+1/2} = K_{\mathbf{B}}(\mathbf{x}_{T-k}, \mathbf{v}_{T-k-1/2})$. The drift gives $\mathbf{x}_{T-k} - h \mathbf{v}_{T-k-1/2} = \mathbf{x}_{T-k-1}$. $\square$

**Claim 5 (phase space volume).** The map $(\mathbf{x}, \mathbf{v}) \mapsto (\mathbf{x}', \mathbf{w})$ of one pass, with $\mathbf{x}' = \mathbf{x} + h \mathbf{w}$, has Jacobian determinant 1 when $\mathbf{E}$ and $\mathbf{B}$ are differentiable.

*Proof.* The pass is the composition of four maps of $\mathbb{R}^6$: (1) $(\mathbf{x}, \mathbf{v}) \mapsto (\mathbf{x}, \mathbf{v} + a\mathbf{E}(\mathbf{x}))$; (2) $(\mathbf{x}, \mathbf{p}) \mapsto (\mathbf{x}, R(\mathbf{x})\mathbf{p})$, where $R(\mathbf{x})$ is the rotation of Claim 2; (3) $(\mathbf{x}, \mathbf{u}) \mapsto (\mathbf{x}, \mathbf{u} + a\mathbf{E}(\mathbf{x}))$; (4) $(\mathbf{x}, \mathbf{w}) \mapsto (\mathbf{x} + h\mathbf{w}, \mathbf{w})$. The Jacobians of (1) and (3) are block lower triangular with identity blocks on the diagonal, and that of (4) is block upper triangular with identity blocks, so all three have determinant 1. The Jacobian of (2) is block lower triangular with the diagonal blocks $I$ and $R(\mathbf{x})$, and $\det R(\mathbf{x}) = 1$ because $R(\mathbf{x})$ is a rotation. By the chain rule the determinant of the composition is the product, which is 1. $\blacksquare$
