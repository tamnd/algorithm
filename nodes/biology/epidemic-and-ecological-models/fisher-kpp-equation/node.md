---
tag: 2NM058
kind: model
slug: fisher-kpp-equation
name: Fisher-KPP equation
aliases:
- Fisher's equation
- Kolmogorov-Petrovsky-Piskunov equation
area: biology/epidemic-and-ecological-models
level: advanced
summary: The equation u_t = D u_xx + r u (1 - u) has fronts for every speed c >= 2 sqrt(r D), and a start of bounded extent spreads at the minimal speed 2 sqrt(r D).
history:
  year: 1937
  people: [Ronald A. Fisher, Andrey N. Kolmogorov, Ivan G. Petrovsky, Nikolai S. Piskunov]
  note: Fisher (1937) used the equation for the spread of an advantageous gene, and Kolmogorov, Petrovsky and Piskunov (1937) proved the existence of the fronts and the minimal speed in the same year.
prereqs: [heat-equation, logistic-growth-model]
see_also: [logistic-growth-model, heat-equation, method-of-lines, finite-difference-method, von-neumann-stability-analysis, turing-instability, kermack-mckendrick-sir-model, wright-fisher-model]
sources:
  - paper: doi:10.1111/j.1469-1809.1937.tb02153.x
    title: Ronald A. Fisher, The wave of advance of advantageous genes, Annals of Eugenics 7(4), 1937
    locator: the equation for the frequency of an advantageous gene in a population spread along a line, and the speed of its wave of advance
  - paper: "A. N. Kolmogorov, I. G. Petrovsky and N. S. Piskunov, Étude de l'équation de la diffusion avec croissance de la quantité de matière et son application à un problème biologique, Bulletin de l'Université d'État à Moscou, Série internationale, Section A, Mathématiques et Mécanique, volume 1, 1937"
    title: Kolmogorov, Petrovsky and Piskunov 1937
    locator: the existence of travelling fronts for each speed from the minimal one, and the convergence of the solution from a step to the front of minimal speed
  - paper: doi:10.1016/0001-8708(78)90130-5
    title: Donald G. Aronson and Hans F. Weinberger, Multidimensional nonlinear diffusion arising in population genetics, Advances in Mathematics 30(1), 1978
    locator: pages 33 to 76 (the asymptotic speed of spread for initial data of bounded support)
  - book: isbn:9780387952239
    title: James D. Murray, Mathematical Biology I, An Introduction, third edition, Springer, 2002
    locator: Chapter 13, Biological Waves, Single-Species Models (the Fisher-KPP equation, its travelling waves and the exact solution)
---

The Fisher-KPP equation $u_t = D u_{xx} + r u (1 - u)$ joins [logistic growth](/logistic-growth-model/) to random movement, modelled by the [heat equation](/heat-equation/). It describes a species, or an advantageous gene, that invades empty space. Its main objects are travelling fronts $u = U(x - c t)$ that move the state $u = 1$ into the state $u = 0$ at a constant speed $c$. Fronts exist for every speed $c \ge 2\sqrt{rD}$ and for no smaller speed. A population that starts in a bounded region spreads at the smallest of these speeds, $2\sqrt{rD}$, which depends only on the growth of small populations and on their diffusion.

## The machine

**The state.** $u(x, t) \in [0, 1]$ is a density relative to the carrying capacity, at the place $x \in \mathbb{R}$ and the time $t \ge 0$. In Fisher's reading, $u$ is the frequency of a new gene that gives a small advantage.

**The parameters.**

- $D > 0$, in length squared per time: the diffusion coefficient. An individual that moves at random spreads with a mean square distance of $2 D t$ after the time $t$.
- $r > 0$, in 1 per time: the growth rate of a small population.

**The equation.**

$$\frac{\partial u}{\partial t} = D \frac{\partial^2 u}{\partial x^2} + r\,u\,(1 - u).$$

**The assumptions.** Each place grows logistically, and individuals move by diffusion with no direction. The habitat is uniform and has one dimension; the same equation with $D\,\Delta u$ holds in more dimensions. The density is a continuous quantity, so the model is a large population limit, and very small densities in the far tail still grow.

**Scaling.** With $x' = x \sqrt{r/D}$ and $t' = r t$, the equation becomes $u_{t'} = u_{x'x'} + u (1 - u)$, with no parameters. A speed $c'$ in the scaled units is the speed $c = c' \sqrt{rD}$ in the original units. So the minimal speed $2\sqrt{rD}$ is the minimal speed $2$ of the scaled equation.

**The KPP class.** The results below hold for every growth term $f(u)$ with $f(0) = f(1) = 0$, $f(u) > 0$ on $(0, 1)$, and $f(u) \le f'(0)\,u$, with $f'(0)$ in place of $r$. The logistic term $r u (1 - u)$ is the standard case.

**A numerical solution.** The implementation uses the [method of lines](/method-of-lines/): second differences on a grid of step $\Delta x$, and explicit Euler in time with step $\Delta t$. The two ends mirror their neighbours, which is a no-flux boundary. Let $\mu = D\,\Delta t / \Delta x^2$.

```pseudo id=main
FISHER-KPP-FRONT(u, Δx, Δt, T)          ▷ u: grid values; mirror ends
L1  μ ← D Δt / Δx²
L2  repeat T / Δt times
L3      for each grid point i
L4          v_i ← u_i + μ (u_{i-1} - 2 u_i + u_{i+1}) + Δt r u_i (1 - u_i)
L5      u ← v
L6  x_f ← the first point where u falls through 1/2 (linear interpolation)
L7  return x_f
```

Each step costs $O(n)$ for $n$ grid points, so a run to the time $T$ costs $O(n T / \Delta t)$. The scheme keeps $0 \le u \le 1$ when $2\mu + r\,\Delta t \le 1$ (proof below), which also makes it stable in the sense of [von Neumann](/von-neumann-stability-analysis/). The front position $x_f$ at two times gives a measured speed.

## What it counts

- The travelling fronts $u(x, t) = U(x - c t)$ with $U(-\infty) = 1$ and $U(+\infty) = 0$, and the set of speeds $c$ for which they exist.
- The minimal speed $c^* = 2\sqrt{rD}$.
- The speed at which a population that starts in a bounded region spreads.
- The shape of the front: its width is of order $\sqrt{D/r}$.

**An example.** Take $D = r = 1$, so $c^* = 2$. On $[0, 100]$ with $\Delta x = 0.25$ and $\Delta t = 0.01$, so that $2\mu + r\Delta t = 0.33$, start from $u = 1$ for $x < 10$ and $u = 0$ after it. The front crosses $u = 1/2$ at these points:

| $t$ | 10 | 20 | 30 | 40 |
|---|---|---|---|---|
| front position $x_f$ | 24.27 | 42.95 | 62.17 | 81.60 |
| speed over the last 10 time units | | 1.868 | 1.922 | 1.942 |

The speed rises toward its limit from below and slowly. The limit for this grid is not exactly $2$: the linearized scheme spreads at $1.9854$ (see below). With $\Delta x = 0.5$ and $\Delta t = 0.05$ that value is $1.9250$, so the grid matters at the level of a few percent.

**A front with a known formula.** For $D = r = 1$, the function

$$U(z) = \left(1 + e^{z/\sqrt{6}}\right)^{-2}$$

is a front with the speed $c = 5/\sqrt 6 = 2.0412$. Started from this profile, the scheme above moves the front at $2.0278$ between $t = 5$ and $t = 20$, close to $5/\sqrt6$ and above $2$.

## Relation to other models

- **[Logistic growth](/logistic-growth-model/).** With $D = 0$, every point grows on its own logistically. Diffusion couples the points and turns the growth into a moving front.
- **[The heat equation](/heat-equation/).** With $r = 0$, a density spreads but does not grow, and the spread is like $\sqrt{t}$, not like $t$. The combination gives a linear spread in time.
- **Exponential growth with diffusion.** The linear equation $w_t = D w_{xx} + r w$ has the solution $w = e^{rt}$ times a solution of the heat equation. It spreads at the same speed $2\sqrt{rD}$. For the Fisher-KPP equation, the front is pulled by its leading edge, where $u$ is small and the equation is close to this linear one.
- **The bistable equation.** With an Allee effect, $f(u) = r u (1 - u)(u - a)$ and $0 < a < 1/2$, small densities decline, and $f(u) \le f'(0) u$ fails. Then there is only one front speed: for $D = r = 1$ it is $(1 - 2a)/\sqrt 2$, with the front $U(z) = 1/(1 + e^{z/\sqrt2})$. This front is pushed by the region behind it, not pulled by its edge.
- **Epidemic waves.** The [SIR model](/kermack-mckendrick-sir-model/) with diffusion of the infected, $I_t = D I_{xx} + \beta S I - \gamma I$, has the same linearization at the front edge, with $\beta S_0 - \gamma$ in place of $r$. So an epidemic wave into a population of density $S_0$ moves at $2\sqrt{D(\beta S_0 - \gamma)}$, and no wave forms if $\beta S_0 < \gamma$.
- **[Turing instability](/turing-instability/).** A system of two reaction-diffusion equations can form stationary patterns. The scalar Fisher-KPP equation cannot: it has fronts, but no stable pattern.
- **Gene frequencies.** In Fisher's reading, $u$ is the frequency of a gene with a small selective advantage $r$ in a population spread along a line. The [Wright-Fisher model](/wright-fisher-model/) is the model of the same frequency in one well-mixed population with random drift.

## Known results in the model

**The front equation.** $u = U(x - c t)$ is a solution if and only if $U$ solves the ordinary equation

$$D U'' + c U' + r U (1 - U) = 0,$$

with $' = d/dz$ and $z = x - c t$. This follows from $u_t = -c U'$ and $u_{xx} = U''$.

**No front is slower than $2\sqrt{rD}$.** If $0 \le U \le 1$ is a front with $U(+\infty) = 0$, then $c \ge 2\sqrt{rD}$.

*Proof.* Write the front equation as the system $U' = V$, $V' = -(c V + r U (1 - U))/D$ in the plane. Near $(0, 0)$ its linearization has the characteristic equation $D \lambda^2 + c \lambda + r = 0$, with the roots $\lambda = (-c \pm \sqrt{c^2 - 4 r D})/(2D)$. If $c < 2\sqrt{rD}$, the roots are complex with a negative real part, so $(0, 0)$ is a stable focus, and every solution that tends to it turns around it. Then $U$ changes sign infinitely often, which a density cannot do. $\square$

**A front exists for every $c \ge 2\sqrt{rD}$.** For each such $c$, there is a decreasing front $U$ with $U(-\infty) = 1$ and $U(+\infty) = 0$.

*Proof.* Let $\mu = c/(2D)$ and let $T$ be the triangle $0 \le U \le 1$, $-\mu U \le V \le 0$. On its three sides the field points into $T$:

- on $V = 0$ with $0 < U < 1$: $V' = -r U (1 - U)/D < 0$;
- on $U = 1$ with $V < 0$: $U' = V < 0$;
- on $V = -\mu U$: $\frac{d}{dz}(V + \mu U) = U\left(\frac{c\mu}{D} - \frac{r(1 - U)}{D} - \mu^2\right) \ge \frac{U}{D}\left(c\mu - r - D \mu^2\right) = \frac{U}{D}\left(\frac{c^2}{4D} - r\right) \ge 0$.

So no solution leaves $T$ once it is inside. The point $(1, 0)$ is a saddle: with $U = 1 - w$, the linearization has the roots of $D\lambda^2 + c\lambda - r = 0$, one positive and one negative. The branch of its unstable manifold with $U < 1$ leaves $(1, 0)$ along the direction $V = \lambda_+ (U - 1) < 0$ and so enters $T$. In $T$, $U' = V \le 0$, so $U$ decreases and is bounded below by $0$; the solution converges, and its limit is an equilibrium in $T$ other than $(1, 0)$, which is $(0, 0)$. This solution is the front. $\square$

For each speed the front is unique up to a shift in $z$. For $c > c^*$ it decays like $e^{-\lambda z}$ with the smaller root $\lambda = (c - \sqrt{c^2 - 4rD})/(2D) < \sqrt{r/D}$; for $c = c^*$ it decays like $z\,e^{-\sqrt{r/D}\, z}$.

**The exact front.** For $D = r = 1$, $U(z) = (1 + e^{bz})^{-2}$ with $b = 1/\sqrt 6$ solves the front equation with $c = 5/\sqrt6$.

*Proof.* Let $w = e^{bz}$, so $U = (1 + w)^{-2}$ and $w' = b w$. Then $U' = -2 b w (1 + w)^{-3}$ and $U'' = -2b^2 w (1 + w)^{-3} + 6 b^2 w^2 (1 + w)^{-4}$, and $U(1 - U) = (2w + w^2)(1 + w)^{-4}$. Multiply the front equation by $(1 + w)^4$. The coefficient of $w$ is $-2b^2 - 2bc + 2$ and that of $w^2$ is $4b^2 - 2bc + 1$. Both are zero if and only if $6 b^2 = 1$ and $2 b c = 2 - 2b^2 = 5/3$, so $b = 1/\sqrt6$ and $c = 5/(6b) = 5/\sqrt6$. $\square$

Its tail is $U \approx e^{-2z/\sqrt6}$, with $\lambda = 2/\sqrt6 < 1$, and indeed $\lambda + 1/\lambda = 5/\sqrt6$.

**The speed from the leading edge.** A tail $u \approx e^{-\lambda (x - ct)}$ solves the linear equation $u_t = D u_{xx} + r u$ if and only if

$$c = c(\lambda) = D \lambda + \frac{r}{\lambda}.$$

The minimum of $c(\lambda)$ over $\lambda > 0$ is at $\lambda^* = \sqrt{r/D}$, with the value $2\sqrt{rD}$. A start with a tail $e^{-\lambda x}$ that is less steep than $e^{-\lambda^* x}$ moves at the speed $c(\lambda) > c^*$; this is why the exact front above keeps its speed $5/\sqrt6$. A start with bounded support has no tail at all, and it takes the minimal speed.

**A start of bounded extent spreads at $2\sqrt{rD}$.** Let $0 \le u(x, 0) \le 1$ be zero outside a bounded interval and not zero everywhere. Then for each $c > 2\sqrt{rD}$, $\sup_{|x| \ge ct} u(x, t) \to 0$, and for each $0 < c < 2\sqrt{rD}$, $\inf_{|x| \le ct} u(x, t) \to 1$ as $t \to \infty$ (Aronson and Weinberger 1978, who prove it in any number of dimensions).

*Proof of the first half.* Since $u (1 - u) \le u$, the comparison principle for parabolic equations gives $u \le w$, where $w_t = D w_{xx} + r w$ with the same start. Let the start vanish outside $[-a, a]$. Then

$$w(x, t) = \frac{e^{rt}}{\sqrt{4\pi D t}} \int_{-a}^{a} e^{-(x - y)^2/(4Dt)}\, u(y, 0)\, dy \le \frac{2a\, e^{rt}}{\sqrt{4\pi D t}}\, e^{-(|x| - a)^2/(4Dt)} \quad \text{for } |x| \ge a.$$

At $|x| \ge c t$ with $ct > a$, the exponent is at most $r t - (ct - a)^2/(4Dt) = t\,(r - c^2/(4D)) + O(1)$, which tends to $-\infty$ when $c > 2\sqrt{rD}$. $\square$

The second half needs a lower bound that grows, and Aronson and Weinberger build it from the fronts above. Kolmogorov, Petrovsky and Piskunov proved that the solution from a step start converges in shape to the front of minimal speed.

**The scheme keeps $u$ in $[0, 1]$.** If $2\mu + r\Delta t \le 1$ and $0 \le u_i \le 1$ for all $i$, then $0 \le v_i \le 1$.

*Proof.* Write $v_i = g(u_i) - 2\mu u_i + \mu (u_{i-1} + u_{i+1})$ with $g(u) = u + r\Delta t\, u (1 - u)$. For the lower bound, $v_i \ge u_i (1 - 2\mu + r\Delta t(1 - u_i)) \ge 0$, since $2\mu \le 1$. For the upper bound, $v_i \le g(u_i) + 2\mu(1 - u_i)$ and $1 - g(u) = (1 - u)(1 - r\Delta t\, u) \ge (1 - u)(1 - r \Delta t) \ge 2\mu (1 - u)$, so $v_i \le 1$. $\square$

**The speed of the scheme.** The grid has its own spreading speed. A mode $e^{-\lambda x}$ grows per step by the factor $g(\lambda) = 1 + r\Delta t + 2\mu(\cosh(\lambda\Delta x) - 1)$, so the linearized scheme spreads at $\min_{\lambda > 0} \ln g(\lambda) / (\lambda \Delta t)$. This is $1.9854$ for $(\Delta x, \Delta t) = (0.25, 0.01)$ and $1.9250$ for $(0.5, 0.05)$, both below $2$, and it tends to $2\sqrt{rD}$ as both steps go to zero. The test checks that the measured speed from the step lies between $1.9$ and this value.

## References
