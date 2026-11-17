---
tag: CF8MA0
kind: theorem
slug: turing-instability
name: Turing instability
aliases:
- diffusion-driven instability
area: biology/epidemic-and-ecological-models
level: advanced
summary: A stable equilibrium of a two-species reaction can become unstable with diffusion when the inhibitor diffuses fast enough, giving spatial patterns.
history:
  year: 1952
  people: [Alan M. Turing]
  note: Turing (1952) showed that two reacting and diffusing chemicals can leave a uniform state and form a stationary wave pattern, as a model for the start of form in an embryo.
prereqs: [jacobian-linearization, heat-equation, eigenvalue]
see_also: [fisher-kpp-equation, heat-equation, jacobian-linearization, lyapunov-stability, eigenvalue, discrete-fourier-transform, von-neumann-stability-analysis, method-of-lines]
sources:
  - paper: doi:10.1098/rstb.1952.0012
    title: Alan M. Turing, The chemical basis of morphogenesis, Philosophical Transactions of the Royal Society of London B 237(641), 1952
    locator: the linear analysis of two morphogens that react and diffuse, and the conditions for stationary waves to grow from a uniform state
  - book: isbn:9780387952284
    title: James D. Murray, Mathematical Biology II, Spatial Models and Biomedical Applications, third edition, Springer, 2003
    locator: Chapter 2, Spatial Pattern Formation with Reaction Diffusion Systems (the conditions for diffusion-driven instability, the band of unstable wave numbers, and the effect of the domain size)
  - book: isbn:9780387952239
    title: James D. Murray, Mathematical Biology I, An Introduction, third edition, Springer, 2002
    locator: Chapter 11, Reaction Diffusion, Chemotaxis, and Nonlocal Mechanisms (reaction-diffusion systems and their linear stability)
---

Diffusion usually smooths a system out. Turing (1952) found the opposite effect. Take two chemicals, or two species, whose reaction has a stable uniform equilibrium. Let them diffuse at different rates. Then a small disturbance with a wavelength in a certain band can grow, and the uniform state gives way to a stationary pattern of peaks and troughs. The theorem below gives the exact conditions for two species. They need one species that promotes growth near the equilibrium and another that holds it back, and the second species must diffuse sufficiently faster than the first. With equal diffusion coefficients, diffusion can never destabilize a stable equilibrium.

## Statement

**The system.** Two concentrations $u(x, t)$ and $v(x, t)$ react and diffuse on the line:

$$u_t = d_u\, u_{xx} + f(u, v), \qquad v_t = d_v\, v_{xx} + g(u, v),$$

with $d_u, d_v > 0$. Let $(u^*, v^*)$ be a uniform equilibrium, $f(u^*, v^*) = g(u^*, v^*) = 0$, and let

$$J = \begin{pmatrix} a_{11} & a_{12} \\ a_{21} & a_{22} \end{pmatrix} = \begin{pmatrix} f_u & f_v \\ g_u & g_v \end{pmatrix}\Bigg|_{(u^*, v^*)}$$

be the [Jacobian](/jacobian-linearization/) of the reaction there. Let $D = \operatorname{diag}(d_u, d_v)$. A small disturbance $w(x, t) = (u - u^*, v - v^*)$ follows the linear system $w_t = D w_{xx} + J w$, and the mode $w = \hat w\, e^{\lambda t} \cos(k x)$ solves it if and only if $\lambda$ is an [eigenvalue](/eigenvalue/) of

$$A(k^2) = J - k^2 D.$$

Call the equilibrium **stable without diffusion** if both eigenvalues of $J$ have a negative real part, which for a real $2 \times 2$ matrix means $\operatorname{tr} J < 0$ and $\det J > 0$. Call it **Turing unstable** if it is stable without diffusion and $A(k^2)$ has an eigenvalue with a positive real part for some $k > 0$.

**Theorem (Turing).** Let $\operatorname{tr} J < 0$ and $\det J > 0$, and let $s = d_v a_{11} + d_u a_{22}$. The equilibrium is Turing unstable if and only if

$$s > 0 \qquad \text{and} \qquad s^2 > 4\, d_u d_v \det J.$$

Then the unstable modes are those with $k^2$ in the open interval $(q_-, q_+)$, where $q_\pm$ are the roots of $h(q) = d_u d_v q^2 - s q + \det J$. For each such mode, $A(k^2)$ has one positive and one negative real eigenvalue, so the mode grows without oscillation.

**Corollary.** Turing instability needs $d_u \ne d_v$. More exactly, $a_{11}$ and $a_{22}$ have opposite signs; if $a_{11} > 0 > a_{22}$, then $d_v > d_u$, and in fact $d_v / d_u > -a_{22} / a_{11} > 1$.

**On a bounded interval.** On $[0, L]$ with no flux at the ends, the modes are $\cos(n \pi x / L)$ with $n = 0, 1, 2, \ldots$, so $k$ takes only the values $n\pi/L$. The equilibrium is unstable if and only if some $(n\pi/L)^2$ falls in $(q_-, q_+)$.

**A hand example.** Take

$$J = \begin{pmatrix} 1 & -1 \\ 3 & -2 \end{pmatrix}, \qquad d_u = 1, \quad d_v = 10.$$

Here $u$ is the activator ($a_{11} = 1 > 0$) and $v$ the inhibitor ($a_{22} = -2 < 0$, $a_{12} = -1 < 0$). Then $\operatorname{tr} J = -1 < 0$ and $\det J = -2 + 3 = 1 > 0$, so the reaction alone is stable. Next, $s = 10 \cdot 1 + 1 \cdot (-2) = 8 > 0$ and $s^2 = 64 > 4 \cdot 1 \cdot 10 \cdot 1 = 40$. So the equilibrium is Turing unstable. The function $h(q) = 10 q^2 - 8 q + 1$ has the roots $q_\pm = (8 \pm \sqrt{24})/20$, that is $q_- = 0.15505$ and $q_+ = 0.64495$, and its minimum $h(0.4) = -0.6$. At $k^2 = 0.4$,

$$A(0.4) = \begin{pmatrix} 0.6 & -1 \\ 3 & -6 \end{pmatrix}, \qquad \lambda = \frac{-5.4 + \sqrt{5.4^2 + 4 \cdot 0.6}}{2} = 0.10891,$$

so the mode with $k = 0.63246$ and the wavelength $2\pi/k = 9.93$ grows like $e^{0.109\, t}$. The growth rate is largest, about $0.1162$, near $k^2 = 0.336$, not exactly where $h$ is smallest. With $d_v = 7$ in place of $10$, $s = 5$ and $s^2 = 25 < 28$, so the same reaction stays stable. The critical value is $d_v = 4 + 2\sqrt3 = 7.4641$.

## In plain words

Picture two substances. The first makes more of itself and also makes the second. The second holds the first back. Without movement, they settle at a steady mix. Now let both spread out, the second much faster than the first. A small local rise in the first substance grows, because the second substance that it makes leaves quickly to the sides. Around the rise, that second substance then stops the first from growing. So a peak forms with a valley next to it, then another peak, at a fixed spacing. The spacing comes from the reaction rates and the speeds of spreading, not from the size of the region. If both substances spread at the same speed, this cannot happen: the spreading then damps every disturbance.

## Proof

**Step 1: the modes.** The system $w_t = D w_{xx} + J w$ is linear with constant coefficients. A mode $\hat w(t) \cos(kx)$ has $w_{xx} = -k^2 w$, so $\hat w' = (J - k^2 D)\hat w = A(k^2) \hat w$. Every bounded disturbance is a sum or integral of such modes (by the Fourier transform on the line, or by a cosine series on $[0, L]$ with no flux). So the equilibrium is linearly unstable if and only if some admissible $k$ gives an eigenvalue of $A(k^2)$ with a positive real part. The mode $k = 0$ has $A(0) = J$, which is stable by assumption.

**Step 2: the trace stays negative.** For $q = k^2 \ge 0$, $\operatorname{tr} A(q) = \operatorname{tr} J - q(d_u + d_v) < 0$. For a real $2 \times 2$ matrix with a negative trace, the eigenvalues are either complex with the real part $\operatorname{tr}/2 < 0$, or real with a negative sum. In the real case, one of them is positive if and only if their product, the determinant, is negative. So $A(q)$ has an eigenvalue with a positive real part if and only if $\det A(q) < 0$, and then both eigenvalues are real, one positive and one negative.

**Step 3: the determinant.** Expand:

$$\det A(q) = (a_{11} - d_u q)(a_{22} - d_v q) - a_{12} a_{21} = d_u d_v\, q^2 - (d_v a_{11} + d_u a_{22})\, q + \det J = h(q).$$

$h$ is a parabola that opens upward, with $h(0) = \det J > 0$. Its minimum is at $q_m = s / (2 d_u d_v)$, with the value $h(q_m) = \det J - s^2/(4 d_u d_v)$. So $h(q) < 0$ for some $q > 0$ if and only if $q_m > 0$ and $h(q_m) < 0$, that is $s > 0$ and $s^2 > 4 d_u d_v \det J$. Then $h < 0$ exactly between its two roots. $\square$

**Proof of the corollary.** Since $a_{11} + a_{22} < 0$ and $d_v a_{11} + d_u a_{22} > 0$, the two diagonal entries cannot both be negative (then $s < 0$) and cannot both be positive (then the trace is positive), and if one of them is zero the two conditions contradict each other. So they have opposite signs. Let $a_{11} > 0 > a_{22}$. Then $s > 0$ gives $d_v / d_u > -a_{22}/a_{11}$, and $\operatorname{tr} J < 0$ gives $-a_{22} > a_{11}$, so $-a_{22}/a_{11} > 1$. $\square$

**Proof for the bounded interval.** On $[0, L]$ with $u_x = v_x = 0$ at both ends, the cosines $\cos(n\pi x/L)$ satisfy the boundary condition and form a complete set, so Step 1 holds with $k = n\pi/L$ only. Steps 2 and 3 are unchanged. $\square$

## Consequences

- **Short-range activation, long-range inhibition.** In the usual case, $u$ activates itself ($a_{11} > 0$) and $v$ inhibits it, and the inhibitor diffuses faster: $d_v / d_u > -a_{22}/a_{11} > 1$. In the example, the ratio must exceed $7.46$.
- **The wavelength is set by the system.** At the start, the pattern is dominated by the fastest-growing mode, with $k^2$ inside $(q_-, q_+)$. Its wavelength depends on $J$, $d_u$ and $d_v$, not on the size of the domain. In the example, it is about $2\pi / \sqrt{0.336} = 10.8$ length units.
- **Small domains have no pattern.** On $[0, L]$, the first nonuniform mode has $k^2 = (\pi/L)^2$. In the example, if $L < \pi / \sqrt{q_+} = 3.91$, then $(\pi/L)^2 > q_+$, every admissible mode is stable, and the uniform state stays. For $L = 10$, the mode $n = 2$ has $k^2 = 0.395$, inside the band, so the pattern $\cos(2\pi x/10)$ grows: one full wave, with a peak at each end and a trough in the middle. Murray's second volume uses this dependence on size to discuss the coat patterns of animals.
- **Patterns, not oscillations.** By Step 2, the unstable eigenvalue is real. So the growing disturbance keeps its shape in space and grows in place. Diffusion of two species with $\operatorname{tr} J < 0$ cannot start a travelling or oscillating wave in this linear analysis.
- **The linear theorem does not give the final pattern.** It says that the uniform state is unstable and which wavelengths grow first. The amplitude and the final shape, such as spots or stripes in two dimensions, depend on the nonlinear terms in $f$ and $g$, and a numerical solution with the [method of lines](/method-of-lines/) is the usual way to see them.
- **One species is not enough.** For one equation $u_t = d u_{xx} + f(u)$, the mode $k$ grows at the rate $f'(u^*) - d k^2 \le f'(u^*)$. If the equilibrium is stable without diffusion, it stays stable. The [Fisher-KPP equation](/fisher-kpp-equation/) has fronts but no Turing patterns.

## Tightness

- **Equal diffusion never destabilizes, for any number of species.** If $D = d I$, then $A(q) = J - q d I$ has the eigenvalues $\lambda_i(J) - q d$, which have smaller real parts than those of $J$. So a stable equilibrium stays stable for all $q$. For two species this is also visible in the theorem: $s = d \operatorname{tr} J < 0$.
- **The conditions are sharp.** At $s^2 = 4 d_u d_v \det J$ with $s > 0$, $h$ has a double root at $q_m$, and $A(q_m)$ has a zero eigenvalue: this is the threshold, with no growing mode. In the example, this happens at $d_v = 4 + 2\sqrt3$, and for $d_v$ slightly above it the band $(q_-, q_+)$ is a narrow interval around $q = s/(2 d_u d_v)$.
- **The diffusion coefficients alone do not decide.** With $J$ that has $a_{11} < 0$ and $a_{22} < 0$, no ratio $d_v/d_u$ gives an instability, because then $s < 0$. The reaction must have one self-promoting species.
- **A bounded domain can hide the band.** The band $(q_-, q_+)$ is a property of the line. On $[0, L]$, the condition of the theorem is necessary but not sufficient: the interval $L < 3.91$ in the example satisfies the conditions on $J$ and $D$ and still has no unstable mode.

## History

Turing (1952) proposed that two chemicals, which he called morphogens, could set up a pattern in a tissue that starts almost uniform, and he showed by a linear analysis of a ring of cells and of a continuous ring that stationary waves can grow when the chemicals diffuse at different rates. The idea was taken up in developmental biology and ecology. Murray's books give the conditions in the form of the theorem above and apply them to animal coat patterns and other biological patterns.

## References
