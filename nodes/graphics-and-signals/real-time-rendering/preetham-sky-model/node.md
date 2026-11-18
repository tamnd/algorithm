---
tag: PNVR3Y
kind: model
slug: preetham-sky-model
name: Preetham sky model
aliases:
- Preetham-Shirley-Smits sky model
area: graphics-and-signals/real-time-rendering
level: advanced
summary: "An analytic model of daylight sky radiance as a function of sun position, view direction and turbidity, fitted to simulated scattering."
prereqs: [participating-media]
see_also: [precomputed-atmospheric-scattering, participating-media, levenberg-marquardt, nonlinear-least-squares, color-spaces, tone-mapping, image-based-lighting, environment-mapping]
sources:
  - paper: doi:10.1145/311535.311545
    title: "A. J. Preetham, Peter Shirley and Brian Smits, A practical analytic model for daylight, SIGGRAPH 99, 91-100"
    locator: the sky luminance and chromaticity distributions in the Perez form with coefficients linear in turbidity, the zenith luminance in Appendix A.2, the definition of turbidity and the constants of the scattering simulation in the appendix
  - paper: doi:10.1016/0038-092X(93)90017-I
    title: "R. Perez, R. Seals and J. Michalsky, All-weather model for sky luminance distribution, preliminary configuration and validation, Solar Energy 50(3), 1993, 235-245"
    locator: the five parameter formula for the relative sky luminance (general locator)
  - url: https://www.cg.tuwien.ac.at/research/publications/2007/zotti-2007-wscg/zotti-2007-wscg-paper.pdf
    title: "Georg Zotti, Alexander Wilkie and Werner Purgathofer, A Critical Review of the Preetham Skylight Model, WSCG 2007"
    locator: Section 3 (negative zenith luminance outside the fitted range, Figure 1) and Section 6 (comparison with the CIE 2003 Standard General Sky and with measurements)
  - paper: doi:10.1145/2185520.2185591
    title: "Lukas Hosek and Alexander Wilkie, An analytic model for full spectral sky-dome radiance, ACM Transactions on Graphics 31(4), 2012 (SIGGRAPH 2012)"
    locator: the fit of an extended Perez formula to a brute force simulation, with ground albedo as a parameter (general locator)
---

The Preetham sky model gives the brightness and color of a clear daylight sky in any view direction with a few exponentials, cheap enough to evaluate per pixel. Its inputs are the position of the sun, the view direction and one number for the haze in the air, the turbidity $T$. Its output is the luminance $Y$ and the chromaticity $(x, y)$ of the sky in that direction. Preetham, Shirley and Smits (1999) built it in two steps. First they computed the sky with a numerical simulation of scattering in a model atmosphere, for many sun positions and turbidities. Then they fitted the results with the formula that Perez, Seals and Michalsky (1993) had proposed for measured sky luminance, with five coefficients that depend linearly on $T$. The formula is a fit, so its accuracy is a property of the fit and of the simulation behind it, not a physical law. It is valid only in the range of the fit, $2 \le T \le 6$, and Zotti, Wilkie and Purgathofer (2007) showed that it gives wrong and even negative values outside that range and that it differs from measured skies inside it. Because it has no tables and needs no precomputation, it suits a sky background and a light source for [image-based lighting](/image-based-lighting/) when the sky must change with the time of day.

## The machine

**Angles.** All angles are in radians.

| symbol | meaning | range |
|---|---|---|
| $\theta_s$ | zenith angle of the sun | $[0, \pi/2]$ |
| $\theta$ | zenith angle of the view direction | $[0, \pi/2)$ |
| $\varphi - \varphi_s$ | azimuth of the view relative to the sun | $[0, 2\pi)$ |
| $\gamma$ | angle between the view direction and the sun | $[0, \pi]$ |

The angle to the sun follows from the others: $\cos\gamma = \cos\theta \cos\theta_s + \sin\theta \sin\theta_s \cos(\varphi - \varphi_s)$.

**Turbidity.** $T = (\tau_m + \tau_h) / \tau_m$, where $\tau_m$ is the optical thickness of the molecules of the air and $\tau_h$ that of the haze. A sky of pure air has $T = 1$, and more haze gives a larger $T$. The fit covers $T$ from 2 to 6, so the valid range of the model is $2 \le T \le 6$.

**The distribution.** Each of the three outputs $Y$, $x$ and $y$ has the form of the Perez formula,

$$F(\theta, \gamma) = \left(1 + A e^{B / \cos\theta}\right)\left(1 + C e^{D\gamma} + E \cos^2\gamma\right),$$

scaled so that the value at the zenith is the zenith value:

$$Y(\theta, \gamma) = Y_z \frac{F(\theta, \gamma)}{F(0, \theta_s)}.$$

The first factor is the gradient from the zenith to the horizon. The second factor has a peak around the sun, the term $C e^{D\gamma}$, and a term $E \cos^2\gamma$ for light scattered forward and backward. The same formula, with other coefficients, gives $x$ and $y$ from their zenith values $x_z$ and $y_z$.

**The coefficients.** Each coefficient is linear in $T$. For the luminance:

| coefficient | value |
|---|---|
| $A$ | $0.1787\,T - 1.4630$ |
| $B$ | $-0.3554\,T + 0.4275$ |
| $C$ | $-0.0227\,T + 5.3251$ |
| $D$ | $0.1206\,T - 2.5771$ |
| $E$ | $-0.0670\,T + 0.3703$ |

For $x$ they are $A = -0.0193T - 0.2592$, $B = -0.0665T + 0.0008$, $C = -0.0004T + 0.2125$, $D = -0.0641T - 0.8989$, $E = -0.0033T + 0.0452$. For $y$ they are $A = -0.0167T - 0.2608$, $B = -0.0950T + 0.0092$, $C = -0.0079T + 0.2102$, $D = -0.0441T - 1.6537$, $E = -0.0109T + 0.0529$. All are tuning constants of the fit.

**The zenith.** The zenith luminance, in $\text{kcd}/\text{m}^2$, is

$$Y_z = (4.0453\,T - 4.9710) \tan\chi - 0.2155\,T + 2.4192, \qquad \chi = \left(\frac{4}{9} - \frac{T}{120}\right)(\pi - 2\theta_s).$$

The zenith chromaticities $x_z$ and $y_z$ are also fitted functions of $T$ and $\theta_s$, with their constants in the appendix of the paper.

**Evaluation.**

```pseudo id=main
PREETHAM-SKY(T, θ_s, θ, φ - φ_s)
L1  for each output c in (Y, x, y):  (A, B, C, D, E)_c ← linear functions of T     ▷ once per frame
L2  Y_z ← the zenith luminance of T and θ_s;  (x_z, y_z) ← the zenith chromaticity of T and θ_s
L3  γ ← acos(cos θ cos θ_s + sin θ sin θ_s cos(φ - φ_s))
L4  for each c:  F_c ← (1 + A_c e^{B_c / cos θ}) (1 + C_c e^{D_c γ} + E_c cos² γ)
L5  for each c:  c ← c_z · F_c / F_c(0, θ_s)                                        ▷ the denominator once per frame
L6  return (Y, x, y), then X ← x Y / y,  Z ← (1 - x - y) Y / y
```

**The simulation behind the fit.** The sky data came from a simulation in the style of Nishita and coauthors, for 12 sun positions and turbidities from 2 to 6, at 343 view directions per case, about 600 CPU hours in all. The air followed the US Standard Atmosphere with the haze profile of Elterman. The constants of the appendix include a refractive index of air of 1.0003, a molecular density of $2.545 \times 10^{25}\ \text{m}^{-3}$, a depolarization factor of 0.035 and a Junge exponent of 4 for the haze particles. The fit used [Levenberg-Marquardt](/levenberg-marquardt/), a [nonlinear least squares](/nonlinear-least-squares/) method.

**Assumptions.**
- A clear sky: no clouds, and the haze is uniform in the horizontal direction.
- Single and double scattering only. The third and higher orders of scattering were left out of the simulation.
- No light reflected from the ground. A bright ground, such as snow, makes the real sky brighter near the horizon.
- The observer is at the ground. The model has no altitude input, so it cannot render the sky seen from a plane or from space.
- The sun is above the horizon. There is no twilight.

## What it counts

The model counts luminance in $\text{kcd}/\text{m}^2$ and chromaticity in the CIE $xyY$ space, per view direction. A renderer converts $xyY$ to $XYZ$ at line L6, then to a linear RGB space, see [color spaces](/color-spaces/), and finally applies [tone mapping](/tone-mapping/) for display, because the sky is far brighter than a display.

The cost per direction is constant: one cosine, three pairs of exponentials and a few multiplications, $\Theta(1)$ time with no memory beyond the 15 coefficients and 3 zenith values. Lines L1 and L2 and the denominators of line L5 run once per change of the sun or the turbidity. A shader can evaluate the model per pixel for the sky background, or once per texel to fill a [cube map](/cube-map/) for [environment mapping](/environment-mapping/) and image-based lighting.

The model does not count the sun disk itself, which the paper treats with a separate model of sunlight, or the haze in front of distant objects.

## Relation to other models

- **The Perez model.** Perez, Seals and Michalsky (1993) proposed the formula for the luminance of real skies of all kinds, fitted to measurements. Preetham and coauthors kept the formula and refitted its coefficients to a simulation of clear skies, as functions of turbidity. The CIE 2003 Standard General Sky uses a modified form of the same formula with 15 fixed sets of coefficients, and it gives luminance only, without color.
- **Physical simulation.** The model replaces a simulation of scattering in [participating media](/participating-media/) by a fit to it. A simulation by [volumetric path tracing](/volumetric-path-tracing/) of a model atmosphere can include all orders of scattering and the ground, at a cost of hours, not microseconds.
- **Precomputed atmospheric scattering.** [Precomputed atmospheric scattering](/precomputed-atmospheric-scattering/) stores the result of the scattering integrals in tables, for any altitude and for the sun below the horizon, and computes several orders of scattering. It needs tables and a precomputation, and it models the atmosphere by physical parameters such as scale heights and scattering coefficients instead of turbidity.
- **Hosek and Wilkie (2012).** Their model keeps the idea of an analytic fit, but fits an extended Perez formula to a brute force simulation, per wavelength band, with the ground albedo as an extra input. Wilkie is also an author of the 2007 critical review of the Preetham model.

## Known results in the model

The following are proved properties of the formulas, in exact arithmetic.
- **Zenith value.** At $\theta = 0$, the angle to the sun is $\gamma = \theta_s$, so $F(0, \gamma) = F(0, \theta_s)$ and $Y = Y_z$. The same holds for $x$ and $y$.
- **Horizon limit.** For $B < 0$, $B / \cos\theta \to -\infty$ as $\theta \to \pi/2$, so the gradient factor tends to 1. For luminance, $B < 0$ when $T > 0.4275 / 0.3554 \approx 1.203$, so in the whole valid range.
- **Brightening toward the horizon.** The derivative of $A e^{B/\cos\theta}$ in $\theta$ is $A B e^{B/\cos\theta} \sin\theta / \cos^2\theta$. For luminance, $A < 0$ when $T < 1.4630 / 0.1787 \approx 8.19$, so for $2 \le T \le 6$ both $A$ and $B$ are negative and the gradient factor grows from the zenith to the horizon. The gain is $1 / (1 + A e^{B})$, which is about 6.0 at $T = 2$ and about 1.08 at $T = 6$: a clear sky is much darker at the zenith than at the horizon, and a hazy sky is almost even.
- **The peak around the sun.** For luminance, $D < 0$ when $T < 2.5771 / 0.1206 \approx 21.4$, so $C e^{D\gamma}$ decreases with the angle to the sun throughout the valid range.
- **Positive zenith luminance in the valid range.** For $2 \le T \le 6$, the factor $4.0453\,T - 4.9710$ is positive, and $\chi$ lies in $[0, 0.43\pi]$, so $\tan\chi \ge 0$. Then $Y_z \ge 2.4192 - 0.2155 \cdot 6 \approx 1.126\ \text{kcd}/\text{m}^2$.
- **Negative zenith luminance outside it.** With the sun at the horizon, $\chi = 0$ and $Y_z = 2.4192 - 0.2155\,T$, which is negative for $T > 11.23$. With the sun at the zenith, $Y_z$ is negative for $T < 1.12$, because the factor of $\tan\chi$ is negative for $T < 1.229$ and $\tan\chi$ is large.

The following are measurements reported by Zotti, Wilkie and Purgathofer (2007), who compared the model with the CIE 2003 Standard General Sky and with their own luminance measurements of clear mid-European skies.
- The zenith luminance becomes negative near the borders of the input space; they advise against the model for exceptionally clear air ($T \lesssim 1.6$), for a sun lower than about $5°$ above the horizon, and for $T \gtrsim 10$.
- For $T < 2$ the horizon is far too bright, and even for $T \le 2.4$ the horizon is too bright when the sun is low ($\theta_s \ge 60°$).
- The model does not reproduce the darker sky opposite a low sun: its values there are about 2 to 5 times too high.
- The peak of brightness toward the sun is less steep than in measurements and in the CIE clear sky models.
- The CIE clear sky (type 12) is closest to the model with $T$ about 2.3 to 2.5.

**Example.** Take $T = 3$ and a sun $30°$ from the zenith. The luminance coefficients are $A = -0.9269$, $B = -0.6387$, $C = 5.2570$, $D = -2.2153$ and $E = 0.1693$. Then $\chi = 0.8785$ (about $50.3°$), $Y_z = 10.41\ \text{kcd}/\text{m}^2$ and $F(0, \theta_s) = 1.4170$.

| view direction | $\gamma$ | $F$ | $Y$ in $\text{kcd}/\text{m}^2$ |
|---|---|---|---|
| zenith | $30°$ | 1.4170 | 10.41 |
| next to the sun, $\theta = 30°$ | $0°$ | 3.5773 | 26.29 |
| $\theta = 60°$, toward the sun | $30°$ | 2.0581 | 15.12 |
| $\theta = 60°$, away from the sun | $90°$ | 0.8618 | 6.33 |
| $\theta = 85°$, toward the sun | $55°$ | 1.6816 | 12.36 |
| $\theta = 85°$, at right angles to the sun | $85.7°$ | 1.1917 | 8.76 |
| $\theta = 85°$, away from the sun | $115°$ | 1.0912 | 8.02 |

The sky is brightest around the sun and darkest about $90°$ from it. At the same angle to the sun, $30°$, the direction near the horizon is brighter than the zenith, because of the gradient factor. The value next to the sun is the bright sky around the sun, not the sun disk.

## References
