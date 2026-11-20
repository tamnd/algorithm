---
title: Implicit Monte Carlo conserves energy and solves the time-discrete Fleck-Cummings problem
proves: [correctness]
status: full
---

We assume exact arithmetic and exact independent uniform random numbers. We prove three things: the Fleck factor is the result of a backward Euler linearization, one step conserves energy exactly, and in one zone the expected census energy is the solution of the time-discrete equation. The accuracy of the time discretization is not a theorem of this page; Larsen and Mercier (1987), cited on the page, prove a maximum principle for small time steps and show that it can fail for large ones.

**Lemma 1 (the Fleck factor).** Let $u = aT^4$ and $\beta = 4aT_n^3/c_v$, frozen at the start of the step. The backward Euler step $u^{n+1} = u^n + \beta c\sigma\Delta t\,(E_r - u^{n+1})$ of the linearized material equation $du/dt = \beta c\sigma (E_r - u)$ gives $u^{n+1} = f u^n + (1 - f) E_r$ with $f = 1/(1 + \beta c\sigma\Delta t)$.

*Proof.* The material equation is $c_v\, dT/dt = c\sigma(E_r - u)$. By the chain rule $du/dt = (du/dT)(dT/dt) = 4aT^3 \cdot c\sigma(E_r - u)/c_v$, which is $\beta c\sigma(E_r - u)$ with $\beta$ frozen at $T_n$. The backward Euler step gives $u^{n+1}(1 + \beta c\sigma\Delta t) = u^n + \beta c\sigma\Delta t\, E_r$. Divide by $1 + \beta c\sigma\Delta t$ and use $\beta c\sigma\Delta t\, f = 1 - f$. $\square$

Putting $u^{n+1}$ in place of $aT^4$ in the emission term $c\sigma aT^4$ of the radiation equation gives $c\sigma f u^n + c\sigma(1 - f)E_r$. The second term equals the part $c\sigma(1 - f)E_r$ of the absorption $c\sigma E_r$, so the two cancel as a scattering with opacity $(1 - f)\sigma$, and what remains is the emission $f c\sigma u^n$ and the absorption with opacity $f\sigma$. The time-discrete problem of IMC is the transport problem over the step with these frozen coefficients.

**Lemma 2 (each collision).** At a collision, line L7 absorbs the particle with probability $f$, and line L8 keeps it with probability $1 - f$. So the distance to the next real absorption, measured along the path, is exponential with rate $f\sigma$, and the particle moves at speed $c$ between collisions.

*Proof.* Collisions happen at the rate $\sigma$ along the path by line L5. Thinning a Poisson process of rate $\sigma$ by independent coin flips with probability $f$ gives a Poisson process of rate $f\sigma$. In one zone the direction plays no role. $\square$

**Theorem 1 (energy conservation).** Let $E_m = c_v T$ be the material energy, $E_c$ the energy in the census and $E_{\mathrm{out}}$ the energy that left through boundaries. After a step, $E_m + E_c + E_{\mathrm{out}}$ equals its value before the step.

*Proof.* Every particle of the old census and of the emission ends the step in exactly one of three ways: absorbed in line L7, put in the new census in line L5, or (in a code with space) gone through a boundary. Line L8 does not change the weight. So the energy of the old census plus $E_{\mathrm{em}}$ equals $E_{\mathrm{abs}}$ plus the new census energy plus the energy that left. Line L9 changes $E_m$ by $E_{\mathrm{abs}} - E_{\mathrm{em}}$. Adding the two equalities gives the claim. Line L10 replaces the census by particles with the same total weight. $\blacksquare$

**Theorem 2 (the expected step in one zone).** In an infinite uniform zone, with old census energy $E_r$ and emission $E_{\mathrm{em}} = f c\sigma u^n\Delta t$ at uniform birth times, the expected new census energy is

$$E_r e^{-f c\sigma\Delta t} + u^n\big(1 - e^{-f c\sigma\Delta t}\big),$$

which is the exact solution at time $\Delta t$ of $dE/dt = f c\sigma(u^n - E)$, $E(0) = E_r$. The expected new temperature follows from Theorem 1: $c_v T^{n+1} = c_v T^n + E_r - E[\text{new census}]$ in expectation.

*Proof.* By Lemma 2 a particle with time $\tau$ left in the step survives to census with probability $e^{-f c\sigma\tau}$, because it travels the distance $c\tau$. The old census particles have $\tau = \Delta t$, which gives the first term. An emitted particle born at time $s$, uniform in $[0, \Delta t]$, has $\tau = \Delta t - s$, also uniform. So the expected surviving emitted energy is

$$E_{\mathrm{em}} \frac{1}{\Delta t}\int_0^{\Delta t} e^{-f c\sigma\tau}\, d\tau = f c\sigma u^n \cdot \frac{1 - e^{-f c\sigma\Delta t}}{f c\sigma} = u^n\big(1 - e^{-f c\sigma\Delta t}\big).$$

By linearity of expectation, the expected census energy is the sum. The ODE solution is checked by substitution. $\blacksquare$

**Consequences.** The radiation part of the step is solved exactly in expectation, and the only errors are the statistical noise and the frozen coefficients $\beta$, $f$ and $u^n$, which make the method first order in $\Delta t$. For a large step, $f c\sigma\Delta t = c\sigma\Delta t/(1 + \beta c\sigma\Delta t)$ tends to $1/\beta$, so the expected census energy tends to $E_r e^{-1/\beta} + u^n(1 - e^{-1/\beta})$, a bounded combination, instead of the explicit emission $c\sigma u^n\Delta t$, which grows without bound. This is why the explicit step with $f = 1$ oscillates in the example and the IMC step does not. When $\beta$ is small (a cold material), $e^{-1/\beta}$ is tiny and almost all of $E_r$ is absorbed, so the material can end hotter than the radiation: the maximum principle fails, as Larsen and Mercier showed.
