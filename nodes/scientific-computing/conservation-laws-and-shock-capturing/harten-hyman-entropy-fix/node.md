---
tag: QYXKT4
kind: technique
slug: harten-hyman-entropy-fix
name: Harten-Hyman entropy fix
aliases:
- Harten-Hyman fix
area: scientific-computing/conservation-laws-and-shock-capturing
level: advanced
summary: Modifies small wave speeds in the Roe flux so that transonic rarefactions do not become nonphysical expansion shocks.
prereqs: [roe-solver, lax-entropy-condition]
see_also: [roe-solver, hll-riemann-solver, exact-riemann-solver, burgers-equation, entropy-stable-scheme, godunov-method, rusanov-flux]
sources:
  - paper: "Amiram Harten and James M. Hyman, Self adjusting grid methods for one-dimensional hyperbolic conservation laws, Journal of Computational Physics 50(2) (1983) 235-269"
    locator: the entropy fix for Roe's scheme with speeds taken on the two sides of each wave; doi:10.1016/0021-9991(83)90066-9
  - book: isbn:9780521009249
    title: Randall J. LeVeque, Finite Volume Methods for Hyperbolic Problems, Cambridge University Press, 2002
    locator: Section 12.3 (transonic rarefactions and an entropy fix for scalar laws), Section 12.7 (E-schemes), Section 15.3 (approximate Riemann solvers for systems, with the Harten-Hyman entropy fix)
  - book: isbn:9783540252023
    title: Eleuterio F. Toro, Riemann Solvers and Numerical Methods for Fluid Dynamics, third edition, Springer, 2009
    locator: Chapter 11 (the Roe solver and the entropy fix of Harten and Hyman)
  - paper: "Ami Harten, High resolution schemes for hyperbolic conservation laws, Journal of Computational Physics 49 (1983) 357-393"
    locator: the earlier entropy fix with a fixed parameter delta in the numerical viscosity; doi:10.1016/0021-9991(83)90136-5
  - paper: "P. L. Roe, Approximate Riemann solvers, parameter vectors, and difference schemes, Journal of Computational Physics 43(2) (1981) 357-372"
    locator: the linearized solver that the fix modifies; doi:10.1016/0021-9991(81)90128-5
---

The [Roe solver](/roe-solver/) upwinds each wave by the sign of its averaged speed $\hat\lambda_k$. Where a rarefaction is transonic, the characteristic speed goes from negative on its left to positive on its right, and $\hat\lambda_k$ can be zero or nearly zero. The Roe flux then adds no dissipation for that wave, and a jump that should spread out as a fan can stay as an expansion shock, which violates the [entropy condition](/lax-entropy-condition/). Harten and Hyman (1983) fixed this by looking at the speeds $\lambda_l$ and $\lambda_r$ on the two sides of the wave. If $\lambda_l < 0 < \lambda_r$, the wave is treated as two parts that move at $\lambda_l$ and $\lambda_r$, so some of it goes each way and the fan opens. The fix changes nothing where no wave is transonic, so the Roe flux keeps its exact shocks and contacts.

## In plain words

A rarefaction is a wave that spreads out over time, like gas rushing into a lower pressure region. If the gas speed passes the speed of sound inside the wave, the wave sits across the cell face, with its left part moving left and its right part moving right. Roe's method looks only at one average speed for the whole wave. That average can be zero, and then the method thinks the wave does not move and keeps a sharp jump. The fix asks how fast the wave edges move. If one edge moves left and the other right, it sends part of the jump each way. The jump then breaks up into the smooth fan that physics wants.

## When it applies

- The scheme uses a linearized Riemann solver, Roe's or another, that upwinds each wave by the sign of one averaged speed.
- The flux has a genuinely nonlinear field, where shocks and rarefactions occur. For the Euler equations these are the two acoustic fields $u \mp c$. Linearly degenerate fields such as the contact never need the fix.
- The flow has a sonic point: a place where $u - c$ or $u + c$ changes sign inside a rarefaction. Signs in the output are a sharp density jump inside a rarefaction, a "dog leg" in the profile, or a jump that stays at rest where the exact solution is a fan.

## The template

```pseudo id=main
ROE-FLUX-WITH-FIX(U_L, U_R)
L1  (λ̂_k, r_k, α_k) <- ROE-WAVES(U_L, U_R)
L2  for each nonlinear field k: λ_l <- λ_k(state left of wave k); λ_r <- λ_k(state right of wave k)
L3  if λ_l < 0 < λ_r: β <- (λ_r - λ̂_k)/(λ_r - λ_l); s_k <- (1 - β) λ_r - β λ_l      ▷ HOLE: the fixed speed
L4  else s_k <- |λ̂_k|
L5  return (F(U_L) + F(U_R))/2 - (1/2) Σ_k s_k α_k r_k
```

The two holes are the side speeds of line L2 and the fixed speed of line L3.

- **Side speeds (line L2).** The states on the two sides of wave $k$ are the states of the linear Riemann solution: $U_L$, $U_L + \alpha_1 r_1$, $U_R - \alpha_3 r_3$ and $U_R$ for the Euler equations. Then $\lambda_l = \lambda_1(U_L)$ and $\lambda_r = \lambda_1(U_L + \alpha_1 r_1)$ for the left acoustic wave, and $\lambda_l = \lambda_3(U_R - \alpha_3 r_3)$, $\lambda_r = \lambda_3(U_R)$ for the right one. For a scalar law, $\lambda_l = f'(u_L)$ and $\lambda_r = f'(u_R)$.
- **Fixed speed (line L3).** The wave $\alpha_k r_k$ is split into a part $\beta\alpha_k r_k$ that moves at $\lambda_l$ and a part $(1 - \beta)\alpha_k r_k$ that moves at $\lambda_r$. The value of $\beta$ makes the mean speed equal to $\hat\lambda_k$: $\beta\lambda_l + (1 - \beta)\lambda_r = \hat\lambda_k$, which keeps property U and so keeps conservation. The flux $F_L + \sum(\text{left-going parts})$ is the form of line L5 with $s_k$ as given.

**Why it works.** Three facts follow from line L3 by short algebra.

1. *It only adds dissipation, when $\hat\lambda_k$ lies between $\lambda_l$ and $\lambda_r$.* Then $\beta \in [0, 1]$ and $s_k = (1 - \beta)|\lambda_r| + \beta|\lambda_l| \ge |\beta\lambda_l + (1 - \beta)\lambda_r| = |\hat\lambda_k|$ by the triangle inequality.
2. *It does not touch an admissible shock.* At a Lax shock of field $k$ the characteristics go into the shock, so $\lambda_l > \lambda_r$, and the test $\lambda_l < 0 < \lambda_r$ fails. The Roe flux, which is exact for a single shock, is used. A shock at rest stays exact.
3. *For Burgers' equation it gives an E-scheme.* With $f = u^2/2$, $\lambda_l = u_L$, $\lambda_r = u_R$ and $\hat\lambda = (u_L + u_R)/2$, so $\beta = \frac12$ and $s = (u_R - u_L)/2$. For $u_L < 0 < u_R$ the flux is $\frac14(u_L^2 + u_R^2) - \frac14(u_R - u_L)^2 = \frac12 u_L u_R$. That is the [HLL](/hll-riemann-solver/) flux with $S_L = u_L$ and $S_R = u_R$. It satisfies $F \le f(u)$ for every $u$ between $u_L$ and $u_R$, because $\frac12 u_L u_R < 0 \le \frac12 u^2$. In every other case the Roe flux of Burgers' equation is the Godunov flux. So the fixed scheme is an E-scheme, and by Osher's theorem (LeVeque 2002, Section 12.7) its limits satisfy the entropy condition.

For systems there is no such theorem. The fix removes the expansion shocks in the tests below, and the measured jump inside the fan shrinks with the cell size.

## Classic examples

The numbers below are measurements made with the code in `impl/python/` (Roe flux, forward Euler, Courant number 0.9, outflow boundaries).

- **[Burgers' equation](/burgers-equation/), $u_L = -1$, $u_R = 1$.** Without the fix, $a = 0$, every face has the flux $\frac12$ and the jump never moves: the $L^1$ error against the fan $u = x/t$ on $[-1, 1]$ at $t = 0.5$ is $0.5$ for every grid. With the fix, the center face has the flux $-\frac12$, the jump opens, and the error is $0.0435$, $0.0273$ and $0.0168$ for 50, 100 and 200 cells. The test checks $F = \frac12 u_L u_R$ exactly in `Fraction` arithmetic on 50 random pairs.
- **[Euler equations](/euler-equations-of-gas-dynamics/), shocks at rest.** A Mach 2 shock at rest, $W_L = (\rho, u, p) = (1, 2\sqrt{1.4}, 1)$ and $W_R = (8/3, 0.88741, 4.5)$, is kept to $10^{-12}$ over 30 steps with the fix, as without it: here $\lambda_l = 1.18322 > 0 > \lambda_r = -0.64963$. With the two states swapped, the jump is an expansion shock at rest. The plain Roe scheme keeps it to $10^{-12}$. With the fix, $\lambda_l = -0.64963 < 0 < \lambda_r = 1.18322$, and after 30 steps the density has changed by more than 0.3.
- **Sod's tube with $u_L = 0.75$** (the first test of Toro 2009): $W_L = (1, 0.75, 1)$ and $W_R = (0.125, 0, 0.1)$, the jump at $x = 0.3$, $t = 0.2$. The left rarefaction is transonic: its head moves at $-0.43322$ and the exact solution has its sonic point at $x/t = 0$. Without the fix, the largest density drop between two neighbor cells inside the fan is 0.130, 0.123 and 0.122 on 100, 200 and 400 cells: a jump that does not shrink. With the fix it is 0.047, 0.025 and 0.013, halving with the cell size. The $L^1$ density error goes from 0.01315, 0.00907, 0.00681 to 0.01187, 0.00773, 0.00546. On 100 cells, the densities in cells 27 to 34 (counting from 1 at the left) are $0.857, 0.835, 0.814, 0.798, 0.668, 0.663, 0.652, 0.639$ without the fix and $0.849, 0.823, 0.796, 0.766, 0.719, 0.688, 0.665, 0.646$ with it.
- **Sod's tube as given.** The rarefaction is not transonic (its tail moves at $-0.0703$), so the fix gives the same flux as plain Roe. The test checks this at the first face.

## Variations

- **Harten's fix with a parameter.** Harten (1983) replaced $|\lambda|$ by $(\lambda^2 + \delta^2)/(2\delta)$ when $|\lambda| < \delta$, with a fixed small $\delta$. It is simpler but adds dissipation at every slow wave, contacts and shocks included, and $\delta$ is a free choice that the user must tune.
- **A data-dependent threshold.** A common simple form sets $\delta_k = \max(0, \hat\lambda_k - \lambda_l, \lambda_r - \hat\lambda_k)$ and replaces $|\hat\lambda_k|$ by $\delta_k$ when $|\hat\lambda_k| < \delta_k$. It uses the same side speeds as line L2, and some texts also call it the Harten-Hyman fix.
- **HLL in place of Roe.** The [HLL](/hll-riemann-solver/) solver opens transonic rarefactions without any fix, at the cost of smearing contacts.
- **Entropy stable fluxes.** An [entropy stable scheme](/entropy-stable-scheme/) builds a flux with a proven entropy inequality for the system, for example an entropy conservative flux plus a dissipation matrix.

## Pitfalls

- **$\hat\lambda_k$ outside $[\lambda_l, \lambda_r]$.** With Roe averages this can happen: at the first face of the transonic Sod test, $\lambda_l = -0.43322$, $\lambda_r = 0.04402$ and $\hat\lambda_1 = -0.60718$, so $\beta = 1.36453$ and line L3 gives $s_1 = 0.57509$, less than $|\hat\lambda_1|$. The split then has a part with negative weight. The flux is still conservative and the run above is clean, but fact 1 does not hold there. Some codes clamp $\beta$ to $[0, 1]$.
- **Side speeds from the wrong states.** Taking $\lambda_r = \lambda_1(U_R)$ for the left acoustic wave mixes in the other waves. Use the intermediate states of the linear solution.
- **A fix on the contact.** The contact field is linearly degenerate, so $\lambda_l = \lambda_r$ and no expansion shock can form. A fix there only smears the contact.
- **A fixed $\delta$ that is too large.** With Harten's parameter form, a large $\delta$ makes the scheme as diffusive as a Rusanov flux on slow waves. A small one does not remove the glitch. The value is a choice that must be tuned for each problem.
- **Negative pressure in the side states.** The intermediate states $U_L + \alpha_1 r_1$ and $U_R - \alpha_3 r_3$ can have negative pressure near vacuum. The code then takes $c = 0$ for the side speed, which is a guard, not a cure: near vacuum use HLL.

## Exercises

1. Show that for a scalar convex law, with $\lambda_l = f'(u_L)$ and $\lambda_r = f'(u_R)$, the fixed flux for $u_L < u_R$ with $f'(u_L) < 0 < f'(u_R)$ equals the HLL flux with $S_L = f'(u_L)$ and $S_R = f'(u_R)$.
2. For the Mach 2 shock at rest above, compute $\lambda_l$ and $\lambda_r$ of the acoustic wave that carries the jump, and check that the fix leaves the flux unchanged.
3. Run the transonic Sod test with Harten's parameter form for $\delta = 0.05$, $0.2$ and $0.5$, and compare the jump inside the fan and the width of the contact with the results above.

## References
