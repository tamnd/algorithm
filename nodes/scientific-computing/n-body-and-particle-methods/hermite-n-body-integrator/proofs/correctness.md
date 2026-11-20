---
title: The Hermite corrector integrates the cubic Hermite interpolant of the acceleration, and the scheme is fourth order
proves: [correctness]
status: full
---

We write one body and suppress its index; the statements hold for each body and each coordinate. Let $\mathbf{a}(t)$ be the acceleration along the exact solution, and assume that it has four continuous derivatives on the step $[0, h]$. Write $\mathbf{a}_0 = \mathbf{a}(0)$, $\mathbf{j}_0 = \dot{\mathbf{a}}(0)$, and $\mathbf{a}_1$, $\mathbf{j}_1$ for the values that line L3 computes at the end of the step.

**Lemma 1 (the jerk).** For the pair term $\mathbf{f} = G m\, \mathbf{r} / s^{3/2}$ with $\mathbf{r} = \mathbf{x}_q - \mathbf{x}_p$, $\mathbf{u} = \mathbf{v}_q - \mathbf{v}_p$ and $s = |\mathbf{r}|^2 + \epsilon^2$, the time derivative is $\dot{\mathbf{f}} = G m \left( \mathbf{u} / s^{3/2} - 3 (\mathbf{r} \cdot \mathbf{u})\, \mathbf{r} / s^{5/2} \right)$, as in line L10.

*Proof.* $\dot{\mathbf{r}} = \mathbf{u}$ and $\dot{s} = 2\, \mathbf{r} \cdot \mathbf{u}$, so $\frac{d}{dt} s^{-3/2} = -\frac{3}{2} s^{-5/2} \cdot 2\, \mathbf{r} \cdot \mathbf{u}$. Apply the product rule. $\square$

**Lemma 2 (the fitted derivatives).** There is exactly one cubic $\mathbf{p}(t) = \mathbf{a}_0 + \mathbf{j}_0 t + \mathbf{a}^{(2)} t^2 / 2 + \mathbf{a}^{(3)} t^3 / 6$ with $\mathbf{p}(h) = \mathbf{a}_1$ and $\dot{\mathbf{p}}(h) = \mathbf{j}_1$, and its coefficients are those of lines L4 and L5:

$$\mathbf{a}^{(2)} = \frac{-6(\mathbf{a}_0 - \mathbf{a}_1) - h(4\mathbf{j}_0 + 2\mathbf{j}_1)}{h^2}, \qquad \mathbf{a}^{(3)} = \frac{12(\mathbf{a}_0 - \mathbf{a}_1) + 6h(\mathbf{j}_0 + \mathbf{j}_1)}{h^3}.$$

*Proof.* The two conditions are the linear system $\frac{h^2}{2} \mathbf{a}^{(2)} + \frac{h^3}{6} \mathbf{a}^{(3)} = \mathbf{a}_1 - \mathbf{a}_0 - h \mathbf{j}_0$ and $h \mathbf{a}^{(2)} + \frac{h^2}{2} \mathbf{a}^{(3)} = \mathbf{j}_1 - \mathbf{j}_0$. Its determinant is $\frac{h^4}{4} - \frac{h^4}{6} = \frac{h^4}{12} \ne 0$, so the solution is unique. Substituting the formulas: the second equation gives $\frac{-6\Delta - 4h\mathbf{j}_0 - 2h\mathbf{j}_1 + 6\Delta + 3h(\mathbf{j}_0 + \mathbf{j}_1)}{h} = \mathbf{j}_1 - \mathbf{j}_0$, with $\Delta = \mathbf{a}_0 - \mathbf{a}_1$; the first gives $-3\Delta - h(2\mathbf{j}_0 + \mathbf{j}_1) + 2\Delta + h(\mathbf{j}_0 + \mathbf{j}_1) = -\Delta - h\mathbf{j}_0$. Both hold. $\square$

**Lemma 3 (the corrector).** Lines L1, L2, L6 and L7 give

$$\mathbf{v}_1 = \mathbf{v}_0 + \int_0^h \mathbf{p}(t)\, dt = \mathbf{v}_0 + \frac{h}{2}(\mathbf{a}_0 + \mathbf{a}_1) + \frac{h^2}{12}(\mathbf{j}_0 - \mathbf{j}_1),$$
$$\mathbf{x}_1 = \mathbf{x}_0 + \mathbf{v}_0 h + \int_0^h (h - t)\, \mathbf{p}(t)\, dt = \mathbf{x}_0 + \mathbf{v}_0 h + \frac{h^2}{20}(7\mathbf{a}_0 + 3\mathbf{a}_1) + \frac{h^3}{60}(3\mathbf{j}_0 - 2\mathbf{j}_1).$$

*Proof.* Lines L2 and L7 add up to $\mathbf{v}_0 + \mathbf{a}_0 h + \mathbf{j}_0 h^2/2 + \mathbf{a}^{(2)} h^3/6 + \mathbf{a}^{(3)} h^4/24$, which is the integral of the cubic term by term. Lines L1 and L6 add up to $\mathbf{x}_0 + \mathbf{v}_0 h$ plus the terms $h^{n+2}/(n+2)!$ times the coefficients of $\mathbf{p}$, which is the double integral. Substituting Lemma 2 and collecting the terms in $\mathbf{a}_0$, $\mathbf{a}_1$, $\mathbf{j}_0$ and $\mathbf{j}_1$ gives the closed forms. For example, the coefficient of $h^2$ in $\mathbf{x}_1$ is $\frac{1}{2}\mathbf{a}_0 - \frac{1}{4}\Delta + \frac{1}{10}\Delta = \frac{7}{20}\mathbf{a}_0 + \frac{3}{20}\mathbf{a}_1$. $\square$

**Theorem (local and global order).** Assume that the force is smooth with bounded derivatives near the solution. Then one step has local errors $O(h^5)$ in velocity and position, and over a fixed time $T$ with $T/h$ steps the error is $O(h^4)$.

*Proof.* First assume exact end values $\mathbf{a}_1 = \mathbf{a}(h)$ and $\mathbf{j}_1 = \dot{\mathbf{a}}(h)$. Then $\mathbf{p}$ is the cubic Hermite interpolant of $\mathbf{a}$ at $0$ and $h$, with the error $\mathbf{a}(t) - \mathbf{p}(t) = \frac{\mathbf{a}^{(4)}(\xi_t)}{24} t^2 (t - h)^2$ in each coordinate. Since $\int_0^h t^2 (t-h)^2\, dt = h^5 / 30$, Lemma 3 gives a velocity error of at most $\frac{h^5}{720} \max |\mathbf{a}^{(4)}|$ and a position error of $O(h^6)$, because the exact solution satisfies the same integral identities with $\mathbf{a}$ in place of $\mathbf{p}$.

The predictor of lines L1 and L2 is the Taylor polynomial to the jerk, so $\mathbf{x}_p - \mathbf{x}(h) = O(h^4)$ and $\mathbf{v}_p - \mathbf{v}(h) = O(h^3)$. The acceleration depends on positions only, so $\mathbf{a}_1 - \mathbf{a}(h) = O(h^4)$; the jerk depends on positions and velocities, so $\mathbf{j}_1 - \dot{\mathbf{a}}(h) = O(h^3)$. In the closed forms of Lemma 3, $\mathbf{a}_1$ enters with the factor $h$ and $\mathbf{j}_1$ with the factor $h^2$, so these errors add $O(h^5)$ to $\mathbf{v}_1$ and $O(h^5)$ or less to $\mathbf{x}_1$. So the local error is $O(h^5)$.

The step map is Lipschitz in $(\mathbf{x}, \mathbf{v})$ with constant $1 + O(h)$, since it is built from the force and its derivative. The standard argument for one-step methods (see [global error](/global-error/)) then turns a local error $O(h^5)$ into a global error $O(h^4)$ over a fixed time. $\square$

**Remarks.** The momentum is conserved up to rounding, because each pair adds opposite terms to $\mathbf{a}$ and $\mathbf{j}$ (lines L9 and L10), so the update of the total momentum $\sum m \mathbf{v}$ by Lemma 3 is zero. The energy is not conserved exactly: the scheme is not symplectic, and for a fixed step its energy error grows linearly in time.
