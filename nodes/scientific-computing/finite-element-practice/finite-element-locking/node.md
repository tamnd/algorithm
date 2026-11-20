---
tag: 1WPN43
kind: concept
slug: finite-element-locking
name: Locking in finite elements
aliases:
- shear locking
- volumetric locking
area: scientific-computing/finite-element-practice
level: core
summary: A loss of accuracy when low order elements cannot meet a constraint such as incompressibility or thin-plate shear without an overly stiff response.
prereqs: [finite-element-method, galerkin-method]
see_also: [corotational-fem, hyperelastic-material, neo-hookean-model, mixed-finite-element-method, inf-sup-condition, taylor-hood-element, cea-lemma, patch-test]
sources:
  - paper: doi:10.1007/BF01396238
    title: Ivo Babuška and Manil Suri, Locking effects in the finite element approximation of elasticity problems, Numerische Mathematik 62 (1992) 439-463
    locator: the definition of locking as a loss of uniformity of the convergence rate with respect to a parameter, and the analysis of volumetric locking for the h and p versions
  - paper: doi:10.1016/0045-7825(78)90005-1
    title: "David S. Malkus and Thomas J. R. Hughes, Mixed finite element methods: reduced and selective integration techniques: a unification of concepts, Computer Methods in Applied Mechanics and Engineering 15(1) (1978) 63-81"
    locator: the equivalence of reduced and selective integration with mixed methods for nearly incompressible problems
  - book: isbn:9783642365188
    title: Daniele Boffi, Franco Brezzi and Michel Fortin, Mixed Finite Element Methods and Applications, Springer Series in Computational Mathematics 44, Springer, 2013
    locator: Chapter 8 (incompressible materials and flow problems) and Chapter 9 (complements on elasticity problems)
---

Locking is the effect that makes a finite element model much too stiff when the material or the geometry forces a constraint: a thin beam or shell meshed with linear elements hardly bends, and a nearly incompressible solid such as rubber or soft tissue, meshed with linear tetrahedra, hardly deforms. In a graphics deformable body simulation with [corotational](/corotational-fem/) or [hyperelastic](/hyperelastic-material/) linear tetrahedra it shows as objects that are too stiff on coarse meshes, and that get stiffer as the Poisson ratio of a [neo-Hookean](/neo-hookean-model/) material approaches 1/2. What the numerical analysis adds to the graphics practice is a precise test, an error bound that must hold uniformly as the thickness goes to 0 or the Poisson ratio goes to 1/2, and remedies, mostly [mixed methods](/mixed-finite-element-method/) and reduced integration, that are proved to pass it.

## In plain words

Some materials or shapes come with a rule the motion must almost obey. A thin beam bends but almost does not shear. Rubber changes shape but almost does not change volume. A coarse mesh of simple elements has few ways to move. If the rule is checked at too many places in each element, the only motions that obey it are the motions that do almost nothing, so the model comes out far too stiff. A finer mesh helps, but much less than it should, and the thinner the beam or the more incompressible the material, the worse it gets. The fix is to check the rule at fewer places, or to treat the quantity behind the rule as a separate unknown.

## The idea

Many problems have a parameter $\varepsilon$ and an energy of the form

$$E(u) = \tfrac12 a(u, u) + \frac{1}{2\varepsilon}\|Cu\|^2 - f(u),$$

where $C$ is a constraint operator. For a Timoshenko beam with thickness $t$, $Cu = w' - \theta$ is the shear strain and $\varepsilon \sim t^2$. For linear elasticity with Lamé constants $\lambda$ and $\mu$, $Cu = \nabla\cdot u$ and $\varepsilon = 1/\lambda$, which goes to 0 as the Poisson ratio goes to 1/2. As $\varepsilon \to 0$, the exact solution approaches the solution with $Cu = 0$, and this limit is well behaved. The discrete solution in a space $V_h$ approaches the best function in $\{v_h \in V_h : Cv_h = 0\}$. If that subspace is too small, for example $\{0\}$, the discrete solution goes to the wrong limit.

**Definition (Babuška and Suri 1992).** A family of finite element methods is free of locking for a parameter range if the error satisfies $\|u_\varepsilon - u_{\varepsilon, h}\| \le C h^k$ for the data of interest with $C$ and $k$ independent of $\varepsilon$. It locks if the constant grows without bound as $\varepsilon \to 0$, or if the rate $k$ for small $\varepsilon$ is lower than for $\varepsilon = 1$. In terms of [Céa's lemma](/cea-lemma/), the ratio of continuity to coercivity constants grows like $1/\varepsilon$, so the bound is uniform in $h$ but not in $\varepsilon$.

**The constraint count (heuristic).** Compare the number of unknowns of $V_h$ with the number of independent conditions that $Cv_h = 0$ imposes. If the conditions are as many as the unknowns, or more, expect locking. This count is fast and often right, but it does not prove anything in either direction.

**The cure.** Replace $\|Cu\|^2/\varepsilon$ by $\|P_hCu\|^2/\varepsilon$, where $P_h$ is a projection onto a smaller space $Q_h$, which is what reduced integration does, or introduce $p = Cu/\varepsilon$ as an unknown in $Q_h$, which gives a [mixed method](/mixed-finite-element-method/). The two are often the same discrete method (theorem, Malkus and Hughes 1978). The method is free of locking when the pair $V_h$, $Q_h$ satisfies the [Babuška-Brezzi conditions](/inf-sup-condition/) uniformly in $h$.

## Examples

**Shear locking of a Timoshenko cantilever, by hand.** A beam of length $L$ is clamped at $x = 0$ and loaded by a force $P$ at $x = L$. The unknowns are the deflection $w$ and the rotation $\theta$, and the energy is $\frac12\int EI\,\theta'^2 + \frac12\int \kappa GA\,(w' - \theta)^2 - Pw(L)$. Let $\phi = 12EI/(\kappa GAL^2)$, which is $Et^2/(\kappa GL^2)$ for a rectangular section of thickness $t$. The exact tip deflection is $w(L) = \frac{PL^3}{3EI}(1 + \phi/4)$. Use one element with linear $w$ and $\theta$, $L = EI = P = 1$ and $s = \kappa GA = 12/\phi$. The unknowns are $w_1 = w(1)$ and $\theta_1 = \theta(1)$, the shear strain is $w_1 - \theta_1x$, and the bending energy is $\frac12\theta_1^2$.

- *Exact integration of the shear term.* $\int_0^1(w_1 - \theta_1x)^2\,dx = w_1^2 - w_1\theta_1 + \theta_1^2/3$, so the equations are $sw_1 - \frac{s}{2}\theta_1 = 1$ and $-\frac{s}{2}w_1 + (1 + \frac{s}{3})\theta_1 = 0$. The solution is $w_1 = \phi(\phi + 4)/(12(\phi + 1))$, and the ratio to the exact value is $\phi/(1 + \phi)$. For $\phi = 1/100$ it is $1/101$: the element is about 100 times too stiff, and it gets worse as the beam gets thinner.
- *One-point integration of the shear term.* The shear term becomes $(w_1 - \theta_1/2)^2$, the equations are $sw_1 - \frac{s}{2}\theta_1 = 1$ and $-\frac{s}{2}w_1 + (1 + \frac{s}{4})\theta_1 = 0$, and $w_1 = 1/s + 1/4 = (\phi + 3)/12$. The ratio is $(\phi + 3)/(\phi + 4)$, which is $301/401$ for $\phi = 1/100$ and $3/4$ in the thin limit.

The reason is the constraint count. With exact integration, $w' - \theta = 0$ on the whole element means $w_1 = \theta_1x$ for all $x$, so $w_1 = \theta_1 = 0$. With one point, only $w_1 = \theta_1/2$ is imposed, and a bending mode is left.

**The same beam with $m$ elements (measurement).** The table gives the ratio of the computed to the exact tip deflection, computed exactly in rational arithmetic. For all entries the values agree with the closed forms $m^2\phi/(1 + m^2\phi)$ for exact integration and $1 - 1/(m^2(4 + \phi))$ for one-point shear integration.

| $\phi$ | integration | $m = 1$ | $2$ | $4$ | $8$ | $16$ |
|---|---|---|---|---|---|---|
| $1$ | exact | 0.5 | 0.8 | 0.9412 | 0.9846 | 0.9961 |
| $1$ | one point | 0.8 | 0.95 | 0.9875 | 0.9969 | 0.9992 |
| $1/100$ | exact | 0.0099 | 0.0385 | 0.1379 | 0.3902 | 0.7191 |
| $1/100$ | one point | 0.7506 | 0.9377 | 0.9844 | 0.9961 | 0.999 |
| $10^{-4}$ | exact | 0.0001 | 0.0004 | 0.0016 | 0.0064 | 0.025 |
| $10^{-4}$ | one point | 0.75 | 0.9375 | 0.9844 | 0.9961 | 0.999 |

With exact integration the error for a fixed mesh goes to 100 percent as $\phi \to 0$, and the mesh needed for a given accuracy grows like $1/\sqrt\phi$, which is $1/t$. With one-point integration the error is at most $1/(4m^2)$ for every $\phi$, so the method is free of locking in the sense of Babuška and Suri.

**Volumetric locking of linear triangles (heuristic count).** Divide the unit square into an $N \times N$ grid of squares and each square into two triangles, and fix the displacement on the boundary. The continuous piecewise linear displacements have $2(N - 1)^2$ unknowns, and the condition $\nabla\cdot u_h = 0$ is one condition on each of the $2N^2$ triangles. There are more conditions than unknowns, so in the incompressible limit the computed displacement is close to $0$, whatever the load. The same count applies to linear tetrahedra in 3D.

**Remedies that pass the test.** For nearly incompressible elasticity, a displacement-pressure mixed method with the [Taylor-Hood element](/taylor-hood-element/), selective reduced integration of the volumetric term on quadrilaterals, and the B-bar method of Hughes all remove the locking. For the h version on triangles, Babuška and Suri showed that polynomial degree $p \ge 4$ is free of volumetric locking, in line with the theorem of Scott and Vogelius on the divergence of such spaces.

## Where it is used

- **Thin structures.** Beams, plates and shells with Reissner-Mindlin or Timoshenko kinematics. Shell elements in practice use reduced integration, assumed strains such as the MITC elements, or mixed interpolation of the shear strain.
- **Nearly incompressible solids.** Rubber, biological tissue and metal plasticity, where the plastic flow keeps the volume. Codes use mixed displacement-pressure elements, the B-bar method or the F-bar method in large deformation.
- **Graphics deformable bodies.** Linear tetrahedra in [corotational](/corotational-fem/) and [neo-Hookean](/neo-hookean-model/) simulations lock in bending on coarse meshes and as the bulk modulus grows. Practical fixes include higher order or mixed elements and a separate treatment of the volume term.
- **Incompressible flow.** The Stokes problem is the limit $\varepsilon = 0$ of the elasticity problem, and the same pairs that avoid locking are the stable pairs for Stokes flow.
- **Reduced integration has a cost.** In 2D and 3D solids, one-point integration of the whole stiffness gives zero energy modes, called hourglass modes, that need a stabilization term. The [patch test](/patch-test/) checks that a modified element still reproduces constant strain states.

## References
