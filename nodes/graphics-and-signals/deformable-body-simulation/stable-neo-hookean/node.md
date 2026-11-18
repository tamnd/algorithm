---
tag: F0PH35
kind: model
slug: stable-neo-hookean
name: Stable neo-Hookean flesh
aliases:
- stable neo-Hookean model
area: graphics-and-signals/deformable-body-simulation
level: research
summary: "A neo-Hookean energy that is smooth and finite for flat and inverted elements, is at rest at F = I, and has a closed-form eigensystem of its Hessian."
prereqs: [neo-hookean-model]
see_also: [hyperelastic-material, st-venant-kirchhoff-model, invertible-finite-elements, corotational-fem, deformation-gradient, optimization-time-integration, incremental-potential-contact, finite-element-method]
sources:
  - paper: doi:10.1145/3180491
    title: Breannan Smith, Fernando de Goes and Theodore Kim, Stable neo-Hookean flesh simulation, ACM Transactions on Graphics 37(2), article 12, 2018
    locator: Section 3.3 (the energy with the log term and the rest value of alpha), Section 3.4 (the Lamé reparameterization) and Eq. 16 (the Poisson's ratio of the linear limit)
  - paper: doi:10.1145/1028523.1028541
    title: Geoffrey Irving, Joseph Teran and Ronald Fedkiw, Invertible finite elements for robust simulation of large deformation, Symposium on Computer Animation 2004, 131 to 140
    locator: the earlier approach, which extends an energy past a threshold on the singular values of F (general locator)
---

The stable neo-Hookean model of Smith, de Goes and Kim (2018) is a [neo-Hookean](/neo-hookean-model/) energy written so that it has a finite value and a smooth gradient for every deformation gradient, including flat and inverted elements.
In 3D, with $I_C = \operatorname{tr}(F^TF)$ and $J = \det F$,

$$\Psi(F) = \frac\mu2(I_C - 3) + \frac\lambda2(J - \alpha)^2 - \frac\mu2\log(I_C + 1), \qquad \alpha = 1 + \frac{3\mu}{4\lambda},$$

$$P(F) = \mu\Bigl(1 - \frac1{I_C + 1}\Bigr)F + \lambda(J - \alpha)\operatorname{cof}F.$$

The volume term is a quadratic in $J$, not in $\log J$, so it needs no $F^{-1}$; the cofactor matrix $\operatorname{cof}F$ is the derivative of $J$ for every $F$.
The shift $\alpha$ and the small log term put the rest state at $F = I$.
Because the terms change the linear limit, the model parameters come from the target Lamé parameters $\mu_0$, $\lambda_0$ by a remap, $\mu = \frac43\mu_0$ and $\lambda = \lambda_0 + \frac56\mu_0$.

## The machine

**Parameters.** From Young's modulus $E_Y$ and Poisson's ratio $\nu$, compute the Lamé parameters $\mu_0 = E_Y/(2(1 + \nu))$ and $\lambda_0 = E_Y\nu/((1 + \nu)(1 - 2\nu))$, then the model parameters $\mu$, $\lambda$ by the remap, then $\alpha$ from $\mu$ and $\lambda$.
For $E_Y = 1$ and $\nu = 0.3$: $\mu_0 = 0.384615$, $\lambda_0 = 0.576923$, $\mu = 0.512821$, $\lambda = 0.897436$ and $\alpha = 1.428571$.
Without the remap, the linear limit has the shear modulus $\frac34\mu$ and the Poisson's ratio $(\lambda - \frac58\mu)/(2(\lambda + \frac18\mu))$, which is 0.269231 instead of 0.3 for these values.

**Energy and stress.** The formulas above, for every real $3 \times 3$ matrix $F$.
Column $k$ of $\operatorname{cof}F$ is the cross product of the other two columns of $F$ in cyclic order, so the cost is a few multiplications and no division except $1/(I_C + 1)$, with $I_C + 1 \ge 1$.

**Forces of a linear element.** With $F = D_sD_m^{-1}$ and the rest volume $V_0$, the forces on the vertices 1 to 3 are the columns of $-V_0PD_m^{-T}$, and vertex 0 gets minus their sum.
Only the rest matrix $D_m$ is inverted, so the forces are defined for a flat or inverted current tetrahedron.

**The terms.** $\frac\mu2(I_C - 3)$ is the stretch term of the neo-Hookean model.
$\frac\lambda2(J - \alpha)^2$ is the volume term, a smooth function of $F$ everywhere.
$-\frac\mu2\log(I_C + 1)$ is a small term whose argument is never below 1.
At rest, $P(I) = (\frac34\mu + \lambda(1 - \alpha))I$, and $\alpha = 1 + \frac{3\mu}{4\lambda}$ makes this zero; the paper writes it as $1 + \frac\mu\lambda - \frac\mu{4\lambda}$, the same number.

## What it counts

$\Psi$ is the energy per unit rest volume, up to a constant: $\Psi(I) = \frac\lambda2(1 - \alpha)^2 - \frac\mu2\log4$ is not zero, and only differences matter.
It counts stretch through $I_C$ and the change of volume through $J$, and nothing for rotations.
It gives an inverted element a finite energy and a force back toward $J > 0$, so the simulation keeps going after an inversion.

**Example.** The bar $F = \operatorname{diag}(s, 1, 1)$ with $E_Y = 1$ and $\nu = 0.3$, so $P_{xx} = \mu s(s^2 + 2)/(s^2 + 3) + \lambda(s - \alpha)$.
The table gives $\Psi(F) - \Psi(I)$, $P_{xx}$, the linear stress $(2\mu_0 + \lambda_0)(s - 1)$ and the neo-Hookean stress with $\mu_0$, $\lambda_0$, which has no value for $s \le 0$.

| $s$ | $\Psi - \Psi(I)$ | $P_{xx}$ | linear $P_{xx}$ | neo-Hookean $P_{xx}$ |
|---|---|---|---|---|
| 1.5 | 0.170658 | 0.686813 | 0.673077 | 0.476461 |
| 1.2 | 0.027087 | 0.271656 | 0.269231 | 0.228680 |
| 1.0 | 0 | 0 | 0 | 0 |
| 0.8 | 0.026746 | $-0.266554$ | $-0.269231$ | $-0.333998$ |
| 0.577350 | 0.118522 | $-0.556662$ | $-0.568952$ | $-0.993015$ |
| 0.3 | 0.321955 | $-0.908763$ | $-0.942308$ | $-3.481999$ |
| 0 | 0.650688 | $-1.282051$ | $-1.346154$ | none |
| $-0.5$ | 1.447472 | $-1.908284$ | $-2.019231$ | none |
| $-1.0$ | 2.564103 | $-2.564103$ | $-2.692308$ | none |

The stress stays close to the linear one in this range and keeps its sign for every $s < 1$, so a flat or inverted bar is pushed back.
There is no barrier: the energy of the flat state is finite, so a strong load can still invert an element, and the model then recovers it instead of failing.

## Relation to other models

- **[Neo-Hookean model](/neo-hookean-model/).** It has a barrier, $\Psi \to \infty$ as $J \to 0$, and no value for $J \le 0$. The stable form gives up the barrier to get an energy that is defined everywhere.
- **[Invertible finite elements](/invertible-finite-elements/).** Irving, Teran and Fedkiw change an existing energy past a threshold on the singular values of $F$. The stable form needs no singular value decomposition and no threshold, because the energy itself is smooth through $J = 0$.
- **[St. Venant-Kirchhoff model](/st-venant-kirchhoff-model/).** It is also defined for every $F$, but its bar force reverses for $-1 < s < 0$ and pushes toward the mirror image; the stable form pushes toward $s = 1$ on the whole line.
- **[Corotational FEM](/corotational-fem/).** The corotated energy is defined for inverted elements only with a choice of the sign of $R$; the stable form needs no polar decomposition.
- **Remap for other energies.** Smith et al. note that the same linearization method can set the parameters of the other energies that they compare.

## Known results in the model

- **Exact gradient for every $F$ (proved).** $P = \partial\Psi/\partial F$ with $\partial J/\partial F = \operatorname{cof}F$, also at $J = 0$ and $J < 0$; the element forces are minus the gradient of the element energy for flat and inverted tetrahedra. See the [proof](proofs/correctness.md), Steps 1 and 2.
- **Objective and isotropic (proved).** $\Psi(QF) = \Psi(FQ) = \Psi(F)$, $P(QF) = QP(F)$ and $PF^T$ is symmetric. Proof, Step 3.
- **Rest state needs the right $\alpha$ (proved).** $P(I) = 0$ exactly for $\alpha = 1 + \frac{3\mu}{4\lambda}$. With $\alpha = 1$, $P(I) = \frac34\mu I$, and with $\alpha = 1 + \mu/\lambda$, the value without the log term, $P(I) = -\frac14\mu I$. Proof, Step 4.
- **Remap (proved).** The linear limit has the shear modulus $\frac34\mu$ and the first Lamé parameter $\lambda - \frac58\mu$, so $\mu = \frac43\mu_0$, $\lambda = \lambda_0 + \frac56\mu_0$ reproduce the target $\mu_0$, $\lambda_0$. Proof, Step 5.
- **Bar recovers from any compression (proved).** On the line $F = \operatorname{diag}(s, 1, 1)$, $P_{xx}$ is strictly increasing in $s$ and zero only at $s = 1$, so the force points to rest for every flat or inverted state on that line. Proof, Step 6.
- **Collapsed point (proved).** $P(0) = 0$, so an element collapsed to a point has no elastic force; $F = 0$ is a saddle of $\Psi$, and nearby the force moves $F$ toward $J > 0$. Proof, Step 7.
- **Hessian eigensystem (stated in the paper).** Smith et al. give the eigenvalues and eigenvectors of the energy Hessian in closed form, so a Newton solver can clamp the negative eigenvalues per element without a numerical eigensolver. This page does not check that result.
- **Choice of model (heuristic).** The name of the paper refers to flesh. Whether this energy fits a given material is a measurement for that material.

## References
