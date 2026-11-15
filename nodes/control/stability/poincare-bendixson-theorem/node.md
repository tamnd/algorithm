---
tag: Z2TWP2
kind: theorem
slug: poincare-bendixson-theorem
name: Poincare-Bendixson theorem
aliases:
- Poincare-Bendixson criterion
area: control/stability
level: advanced
summary: In the plane, a solution that stays in a compact set with no equilibrium tends to a periodic orbit. With equilibria allowed, the limit can also be an equilibrium or equilibria joined by orbits.
prereqs: [limit-cycle]
see_also: [limit-cycle, lasalle-invariance-principle, positively-invariant-set, describing-function, region-of-attraction, equilibrium-point, jacobian-linearization, lyapunov-direct-method]
sources:
  - paper: doi:10.1007/BF02403068
    title: Ivar Bendixson, Sur les courbes définies par des équations différentielles, Acta Mathematica 24, 1-88, 1901
    locator: the complete proof of the theorem on limit sets in the plane, and the criterion with the divergence that excludes closed trajectories
  - paper: "H. Poincaré, Mémoire sur les courbes définies par une équation différentielle, Journal de Mathématiques Pures et Appliquées, Series 3, volumes 7 and 8 (1881, 1882), and Series 4, volumes 1 and 2 (1885, 1886)"
    locator: arcs without contact, consequents, and the limit cycles of planar vector fields
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 2.6, Existence of Periodic Orbits (the Poincaré-Bendixson criterion, Bendixson's criterion and the index method)
---

The Poincaré-Bendixson theorem gives a way to prove that a planar system has a periodic orbit without solving it. One finds a closed and bounded region of the plane that solutions cannot leave and that contains no equilibrium. Then the region contains a periodic orbit, and every solution in it approaches one. The usual region is a ring around an unstable equilibrium, with the vector field pointing inward on both edges. The theorem holds only for systems of dimension 2: its proof uses the Jordan curve theorem, which says that a closed curve divides the plane into an inside and an outside. In dimension 3 and more, bounded solutions can wind forever without closing, and chaos is possible. Bendixson's divergence criterion and Dulac's criterion do the opposite job: they prove that a region of the plane has no periodic orbit.

## Statement

**Setting.** $\dot x = f(x)$, with $f : D \to \mathbb{R}^2$ continuously differentiable on an open set $D \subseteq \mathbb{R}^2$. Let $x(t)$ be the solution with $x(0) = x_0$. If it is defined for all $t \ge 0$, its *omega-limit set* $\omega(x_0)$ is the set of points $p$ with $x(t_k) \to p$ for some sequence $t_k \to \infty$.

**Theorem (Poincaré-Bendixson).** Let $M \subset D$ be compact and positively invariant, and let $M$ contain no equilibrium of $f$. Then for every $x_0 \in M$, $\omega(x_0)$ is a periodic orbit. In particular, $M$ contains a periodic orbit. The same holds if only the positive half orbit of $x_0$ stays in a compact set $K \subset D$ that contains no equilibrium.

**Theorem (general form).** Let the positive half orbit of $x_0$ stay in a compact set $K \subset D$ that contains only finitely many equilibria. Then $\omega(x_0)$ is one of these:

1. a single equilibrium;
2. a periodic orbit;
3. a finite set of equilibria together with orbits, each of which tends to one of these equilibria as $t \to \infty$ and to one as $t \to -\infty$.

**Theorem (Bendixson's criterion).** Let $\Omega \subseteq D$ be simply connected. If $\operatorname{div} f = \partial f_1 / \partial x_1 + \partial f_2 / \partial x_2$ does not change sign in $\Omega$ and is not identically zero on any open subset of $\Omega$, then $\Omega$ contains no periodic orbit.

**Theorem (Dulac's criterion).** Under the same hypotheses on $\Omega$, if there is a continuously differentiable function $B : \Omega \to \mathbb{R}$ such that $\operatorname{div}(B f)$ does not change sign in $\Omega$ and is not identically zero on any open subset, then $\Omega$ contains no periodic orbit.

## In plain words

Imagine a flow of water on a flat table, with no sources, sinks or whirlpool centers in some fenced area, and water that cannot leave the fenced area. A floating leaf must keep moving forever, and it cannot leave. On a flat surface its path cannot cross itself, so it cannot wander in a complicated way. The only thing it can do in the long run is settle onto a closed loop and go around it. If the area does contain points where the water is still, the leaf can also stop at one of them, or follow a loop of paths that run from one still point to the next. A different test tells you that no loop can exist: if the water spreads out everywhere in a region without holes, or contracts everywhere, no closed loop fits in it.

## Proof

The proof of the first theorem follows the method of Poincaré and Bendixson. The steps use only the continuity of the flow and the Jordan curve theorem.

**Step 1: limit sets.** Since the half orbit stays in the compact set $K$, $\omega(x_0)$ is nonempty, compact, connected and invariant, and it lies in $K$ (Khalil 2002, Section 4.2, states this for any dimension).

**Step 2: transversal segments.** Let $p$ be a point with $f(p) \ne 0$. A short line segment $L$ through $p$, not parallel to $f(p)$, is *transversal*: $f$ is not tangent to $L$ at any of its points, and all solutions cross $L$ in the same direction. By continuity of the flow, every solution that starts close enough to $p$ crosses $L$ at a point close to $p$ within a short time.

**Step 3: monotone crossings.** Let a solution cross $L$ at successive times $t_1 < t_2 < t_3$, at points $y_1, y_2, y_3$. Then $y_2$ lies between $y_1$ and $y_3$ on $L$. Proof: the arc of the solution from $y_1$ to $y_2$ and the piece of $L$ between $y_1$ and $y_2$ form a closed curve $C$ without self-intersections. By the Jordan curve theorem $C$ divides the plane into an inside and an outside. Solutions can cross the piece of $L$ in only one direction, and they cannot cross the arc of the solution, by uniqueness. So after time $t_2$ the solution stays on one side of $C$, and its next crossing of $L$ lies beyond $y_2$, on the side away from $y_1$.

**Step 4: a limit set meets a transversal at most once.** If $\omega(x_0)$ met $L$ at two points $q_1 \ne q_2$, the solution from $x_0$ would cross $L$ near $q_1$ and near $q_2$ infinitely often, by Step 2. That contradicts the monotone order of Step 3.

**Step 5: $\omega(x_0)$ contains a periodic orbit.** Take $y \in \omega(x_0)$. Its whole orbit lies in $\omega(x_0)$ by invariance, so $\omega(y) \subseteq \omega(x_0) \subseteq K$, and $\omega(y)$ is nonempty. Take $z \in \omega(y)$. Since $K$ has no equilibrium, $f(z) \ne 0$; take a transversal $L$ through $z$. The orbit of $y$ comes close to $z$ infinitely often, so it crosses $L$ at least twice. But the orbit of $y$ lies in $\omega(x_0)$, which meets $L$ at most once. So the orbit of $y$ crosses $L$ twice at the same point, and $y$ is periodic. Let $\Gamma$ be its orbit.

**Step 6: $\omega(x_0) = \Gamma$.** Suppose $\omega(x_0) \setminus \Gamma$ is not empty. Since $\omega(x_0)$ is connected and $\Gamma$ is closed, there are points of $\omega(x_0) \setminus \Gamma$ arbitrarily close to some $q \in \Gamma$. Take a transversal $L$ through $q$. By Step 2, the orbits of these points, which lie in $\omega(x_0)$ and not on $\Gamma$, cross $L$ at points other than $q$. Then $\omega(x_0)$ meets $L$ at two points, which contradicts Step 4. $\square$

The general form uses the same steps. If $\omega(x_0)$ contains no equilibrium, Steps 5 and 6 apply. If it contains only equilibria, it is a single equilibrium, because it is connected and the equilibria in $K$ are finite in number. Otherwise, let $y \in \omega(x_0)$ be a point that is not an equilibrium. If $\omega(y)$ contained a point $z$ with $f(z) \ne 0$, Step 5 would make the orbit of $y$ periodic, and Step 6 would make $\omega(x_0)$ equal to that orbit, which contains no equilibrium. So $\omega(y)$ is a connected set of equilibria, which is a single equilibrium. The same argument in reverse time applies to the limit set of $y$ as $t \to -\infty$.

**Proof of Bendixson's criterion.** Suppose $\Gamma \subset \Omega$ is a periodic orbit of period $T$. It is a closed curve without self-intersections, and since $\Omega$ is simply connected, the region $R$ inside $\Gamma$ lies in $\Omega$. By Green's theorem,

$$\iint_R \operatorname{div} f\, dA = \oint_\Gamma (f_1\, dx_2 - f_2\, dx_1) = \int_0^T (f_1 f_2 - f_2 f_1)\, dt = 0 .$$

The integral on the left is not zero, because $\operatorname{div} f$ has one sign and is not identically zero on the open set $R$. This is a contradiction. For Dulac's criterion, apply the same computation to the vector field $B f$, whose line integral along $\Gamma$ is also zero because $B f$ is parallel to $f$. $\square$

## Consequences

**Trapping regions.** The usual way to use the theorem is a ring. Take $\dot r = r (1 - r^2) + \beta r \cos \theta$, $\dot \theta = 1$ in polar coordinates, with $0 < \beta < 1$. The only equilibrium is the origin, because $\dot \theta \ne 0$. For $r < \sqrt{1 - \beta}$, $\dot r \ge r (1 - r^2 - \beta) > 0$, and for $r > \sqrt{1 + \beta}$, $\dot r \le r (1 - r^2 + \beta) < 0$. So each ring $\{\sqrt{1 - \beta} - \epsilon \le r \le \sqrt{1 + \beta} + \epsilon\}$ with small $\epsilon > 0$ is compact, positively invariant and free of equilibria, and it contains a periodic orbit. For $\beta = 0.5$ the ring is $0.7071 \le r \le 1.2247$, and a simulation shows that the orbit stays in $0.7651 \le r \le 1.2110$. The theorem does not say how many periodic orbits the ring holds. The count needs a separate argument.

**A periodic orbit encloses an equilibrium.** With index theory one proves that the region inside a periodic orbit of a planar system contains at least one equilibrium (Khalil 2002, Section 2.6). So a simply connected region without equilibria has no periodic orbit.

**No chaos in the plane.** By the general form, a bounded solution of a planar autonomous system with finitely many equilibria converges to an equilibrium, to a periodic orbit, or to a cycle of equilibria and connecting orbits. Chaotic attractors need dimension at least 3.

**Using Bendixson's criterion.** For the damped oscillator $\dot x_1 = x_2$, $\dot x_2 = -g(x_1) - c x_2$ with $c > 0$, $\operatorname{div} f = -c < 0$ everywhere, so there is no periodic orbit. For the van der Pol equation $\dot x_1 = x_2$, $\dot x_2 = -x_1 + \mu (1 - x_1^2) x_2$, $\operatorname{div} f = \mu (1 - x_1^2)$, which is positive in the strip $|x_1| < 1$. So the [limit cycle](/limit-cycle/) of the van der Pol equation must leave the strip.

**Using Dulac's criterion.** For the competition model $\dot x_1 = x_1 (a - b x_1 - c x_2)$, $\dot x_2 = x_2 (d - e x_2 - g x_1)$ with $b, e > 0$, take $B = 1 / (x_1 x_2)$ in the open positive quadrant. Then

$$\operatorname{div}(B f) = \frac{\partial}{\partial x_1} \frac{a - b x_1 - c x_2}{x_2} + \frac{\partial}{\partial x_2} \frac{d - e x_2 - g x_1}{x_1} = -\frac{b}{x_2} - \frac{e}{x_1} < 0 ,$$

so the quadrant contains no periodic orbit.

**Rule of thumb, not a theorem: approximate methods.** In control, the [describing function](/describing-function/) method is often used to guess where a limit cycle is. Its prediction is not a proof. The Poincaré-Bendixson theorem with a trapping region, or a computation of the Floquet multipliers, is needed to confirm it.

## Tightness

**Equilibria in the set.** Without the hypothesis that $K$ contains no equilibrium, the limit set need not be a periodic orbit. Take the double well $H(x) = \tfrac12 x_2^2 - \tfrac12 x_1^2 + \tfrac14 x_1^4$ and

$$\dot x_1 = x_2, \qquad \dot x_2 = x_1 - x_1^3 - k\, x_2\, H(x), \qquad k > 0 .$$

Along solutions, $\dot H = -k x_2^2 H$, so $H$ moves toward $0$ from both sides. The level set $\{H = 0\}$ is a figure eight: the saddle at the origin and two orbits that leave it and return to it. A solution that starts inside the right loop, other than the equilibrium $(1, 0)$, spirals outward toward that loop. Its omega-limit set is the loop, which is case 3 of the general form and not a periodic orbit. The compact set $\{H \le 0, x_1 \ge 0\}$ is positively invariant, but it contains the equilibria $(0, 0)$ and $(1, 0)$.

**Dimension 3.** The theorem fails in $\mathbb{R}^3$. Use coordinates $(\theta, \phi, \rho)$ near a torus in space: $\theta$ is the angle around the vertical axis, $\phi$ the angle around the tube, and $\rho$ the distance from the center circle of the tube, which has radius $2$. In the shell $\{1/2 \le \rho \le 3/2\}$ take $\dot \theta = 1$, $\dot \phi = \sqrt 2$, $\dot \rho = \rho (1 - \rho)$. The shell is compact and positively invariant, and there is no equilibrium. A periodic orbit would need a time $T$ with $T$ and $\sqrt 2\, T$ both multiples of $2\pi$, which is impossible. Every solution approaches the torus $\rho = 1$, and each solution on the torus is dense in it. The Lorenz equations give another failure, with a chaotic limit set.

**Other surfaces.** The same irrational flow on a torus shows that the theorem fails on surfaces that are not the plane or the sphere. The proof needs the Jordan curve theorem, which is false on a torus.

**Uniqueness of solutions.** The proof uses the fact that solutions cannot cross. If $f$ is only continuous, solutions need not be unique, and the argument of Step 3 breaks.

**The divergence criteria need simple connectivity.** For $\dot r = r (1 - r^2)$, $\dot \theta = 1$, the divergence is $2 - 4 r^2$, which is negative in the ring $\{0.8 < r < 1.2\}$. Yet the unit circle is a periodic orbit in that ring. The ring has a hole, and the region inside the circle is not part of it.

## History

Poincaré introduced the qualitative study of planar differential equations in his memoir of 1881 to 1886. He used arcs without contact, which are the transversal segments of the proof, and the sequence of consequents, which is the Poincaré map, and he named the limit cycles. Bendixson (1901) gave a complete proof of the theorem, including the cases with equilibria, and proved the divergence criterion. Dulac later generalized the criterion with a weight function $B$. In control, it is a standard tool for the phase plane analysis of second-order systems, and Khalil (2002, Section 2.6) presents it with the index method.

## References
