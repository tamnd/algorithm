---
tag: 4CGSP7
kind: model
slug: gerstner-waves
name: Gerstner waves
aliases:
- trochoidal waves
area: graphics-and-signals/fluid-animation
level: intro
summary: Model ocean waves by moving surface points on circles, which gives sharp crests and flat troughs, summed over several wave trains.
history:
  year: 1802
  people: [Franz Joseph von Gerstner, Alain Fournier, William T. Reeves, Darwyn R. Peachey]
  note: Gerstner found the trochoidal wave as an exact solution for deep water in 1802. Fournier and Reeves, and Peachey, brought it to computer graphics at SIGGRAPH 86.
prereqs: [wave-equation]
see_also: [fft-ocean-synthesis, height-field-water, shallow-water-equations, navier-stokes-equations, fluid-simulation-for-animation]
sources:
  - paper: doi:10.1145/15922.15894
    title: Alain Fournier and William T. Reeves, A simple model of ocean waves, Proceedings of SIGGRAPH 86, 75-84, 1986
    locator: the whole paper (the Gerstner model of the surface and the orbits of the particles)
  - paper: doi:10.1145/15922.15893
    title: Darwyn R. Peachey, Modeling waves and surf, Proceedings of SIGGRAPH 86, 65-74, 1986
    locator: the whole paper (wave profiles, the depth of the water and spray)
  - book: "Randima Fernando (editor), GPU Gems, Addison-Wesley, 2004"
    title: Mark Finch, Effective water simulation from physical models
    locator: Chapter 1 (the sum of Gerstner waves, the steepness parameter Q and the condition against loops at the crests)
  - book: "Jerry Tessendorf, Simulating Ocean Water, SIGGRAPH course notes, 2001"
    title: Simulating Ocean Water
    locator: the notes as a whole (Gerstner waves and the dispersion relation, general locator)
---

A Gerstner wave moves each point of the water surface on a circle, so that the points crowd together at the crests and spread out in the troughs.
The surface that results is a trochoid: the crests are sharper and the troughs flatter than those of a sine wave of the same height.
Gerstner found in 1802 that this motion is an exact solution of the equations of an ideal fluid in deep water, with a free surface at a constant pressure.
In computer graphics, Fournier and Reeves (1986) and Peachey (1986) used trochoidal waves for the sea, and real-time water adds a few of them in different directions, as in Finch (2004).
The waves come from a closed formula, so there is no simulation and no grid.

## The machine

**One wave, the exact model.**
The water fills $z \le 0$ at rest and is deep compared with the wavelength.
Each water particle has a label $(a, b)$, its rest position, with $b \le 0$.
At the time $t$ it is at

$$x = a - A e^{kb}\sin\theta, \qquad z = b + A e^{kb}\cos\theta, \qquad \theta = ka - \omega t + \varphi,$$

and the surface is the curve of the particles with $b = 0$.
The parameters are:

- the amplitude $A \ge 0$ in m,
- the wave number $k = 2\pi/\lambda > 0$ in rad/m, for the wavelength $\lambda$ in m,
- the angular frequency $\omega$ in rad/s, fixed by the deep water dispersion relation $\omega^2 = g k$, with $g = 9.81$ m/s²,
- a phase $\varphi$ in rad,
- the steepness $kA$, with no loops for $kA \le 1$; the exact model needs $kA < 1$.

The wave runs in the $+x$ direction at the phase speed $c = \omega/k = (g/k)^{1/2}$.
The standing assumptions are deep water, an incompressible fluid with no viscosity, gravity as the only force, a constant pressure on the surface, no wind and no surface tension.
The surface is a parametric curve, not a height field, so it can hold a sharp crest.

**A sum of waves, the graphics model.**
On a 3D surface, the rest point $p = (p_x, p_y)$ moves to

$$\Big(p - Q\sum_i \hat d_i A_i \sin\theta_i,\ \sum_i A_i\cos\theta_i\Big), \qquad \theta_i = k_i\,\hat d_i\cdot p - \omega_i t + \varphi_i,$$

with a unit direction $\hat d_i$, an amplitude $A_i$ and a wave number $k_i$ for each wave, $\omega_i^2 = g k_i$, and a choppiness $Q \in [0, 1]$ that scales the horizontal motion.
For one wave and $Q = 1$, this is the exact model.
A sum of exact solutions of these nonlinear equations is not shown to be a solution, so the sum is a model for images, not a solution of the flow.

## What it counts

The model gives the position of the surface at each time: the height and the horizontal displacement of each rest point.
It also gives the velocity of each particle, $(A e^{kb}\omega\cos\theta,\ A e^{kb}\omega\sin\theta)$ for one wave, and so the motion of a floating object that follows the water.
The surface normal comes from the two tangents $\partial/\partial p_x$ and $\partial/\partial p_y$ of the formula.

For one wave of wavelength 10 m on deep water, $k = 0.628319$ rad/m, $\omega = 2.482701$ rad/s, the period is $2.530786$ s and the phase speed is $3.951342$ m/s.
The table gives the values that the model predicts for three amplitudes of this wave, computed by the code.
The mean level is the mean surface height over $x$.

| $A$ (m) | $kA$ | mean level (m) | crest above the mean (m) | trough below the mean (m) | particle speed at the surface (m/s) | vorticity at the surface (1/s) | part of the wavelength above the mean |
|---|---|---|---|---|---|---|---|
| 0.3 | 0.189 | -0.028 | 0.328 | 0.272 | 0.745 | 0.183 | 0.470 |
| 0.8 | 0.503 | -0.201 | 1.001 | 0.599 | 1.986 | 1.679 | 0.426 |
| 1.592 | 1.000 | -0.796 | 2.387 | 0.796 | 3.951 | no limit | 0.391 |

The crest stands higher above the mean level than the trough falls below it, and it is narrower; at $kA = 1$ the crest is a cusp.
Five meters below the surface, the orbits of this wave have only $e^{-5k} = 4.3$ percent of the radius at the surface.

## Relation to other models

- **Linear (sine) waves.** For small $kA$, the height of a Gerstner wave at a fixed $x$ is $A\cos(kx - \omega t)$ plus terms of order $kA^2$. So to first order it is the sine wave of linear theory, with the same dispersion relation.
- **Stokes waves.** A wave that starts from water at rest in an ideal fluid has no vorticity, by the theorem of Kelvin. The Gerstner flow has vorticity, so it is not that wave; the periodic waves of the irrotational theory are the Stokes waves, which this page does not cover.
- **FFT ocean synthesis.** The choppy displacement of [FFT ocean synthesis](/fft-ocean-synthesis/) moves each point by $-\lambda\,\hat k$ times a sine term for each wave, the horizontal motion of a sum of Gerstner waves with random amplitudes and phases. FFT synthesis uses thousands of waves from a spectrum; a Gerstner sum uses a few that the artist chooses.
- **Height field water.** [Height field water](/height-field-water/) and the [shallow water equations](/shallow-water-equations/) simulate the water and so react to objects and to the ground, but have no sharp crests. A Gerstner wave reacts to nothing.
- **Shallow water.** Near a beach the deep water assumption fails. Fournier and Reeves, and Peachey, changed the waves with the depth of the water; with depth $d$, the linear dispersion relation becomes $\omega^2 = gk\tanh(kd)$, and for long waves the speed tends to $(gd)^{1/2}$, which is $3.13209$ m/s for $d = 1$ m.
- **Fluid equations.** The model is a special solution of the incompressible Euler equations, the [Navier-Stokes equations](/navier-stokes-equations/) with no viscosity.

## Known results in the model

The [proof page](proofs/correctness.md) has the proofs, and the tests check each result with the code.

- **Exact solution (proved).** With $\omega^2 = gk$ and $kA < 1$, the motion satisfies the Euler equations in Lagrangian form, with a pressure that depends on $b$ only. So the pressure is constant on the surface $b = 0$, as the free surface needs. With any other $\omega$, the equations fail.
- **Incompressible (proved).** The Jacobian of the map from $(a, b)$ to $(x, z)$ is $1 - k^2A^2e^{2kb}$, which does not change in time, so every part of the water keeps its area.
- **Circular orbits (proved).** Each particle moves on a circle of radius $Ae^{kb}$ about its label, once per period, so the radius falls by the factor $e^{-k}$ for each meter of depth.
- **Rotational flow (proved).** The vorticity is $2\omega s^2/(1 - s^2)$ with $s = kAe^{kb}$. It is not 0, and it turns the other way from the particles on their orbits.
- **Shape (proved).** The crest is at $z = A$ and the trough at $z = -A$, but the mean level of the surface over $x$ is $-kA^2/2$. The surface is stretched by the factor $1 - kA$ at the crest and $1 + kA$ at the trough, so the crest is sharp. At $kA = 1$ the crest is a cusp, and for $kA > 1$ the curve crosses itself and makes a loop. The part of the wavelength above the mean level is measured in the table.
- **Crest speed (proved).** At the crest the surface particle moves forward at $A\omega$, which equals the phase speed $\omega/k$ exactly when $kA = 1$.
- **No loops in a sum (proved).** If $Q\sum_i k_iA_i < 1$, the horizontal map $p \mapsto x(p)$ is one to one at every time, so the 3D surface does not fold over itself. Finch (2004) gives the same kind of condition: the sum of $Q_i k_i A_i$ at most 1, with one $Q_i$ for each wave. The condition is sufficient, not necessary.
- **Dispersion (law).** $\omega^2 = gk$ is the dispersion law of small waves on deep water, and the Gerstner wave has it for every amplitude.

## References
