---
tag: AM4GS6
kind: theorem
slug: dix-formula
name: Dix formula
aliases:
- Dix equation
area: imaging-and-inverse-problems/seismic-imaging
level: core
summary: "In flat layers the interval velocity between two reflectors follows from their rms velocities and zero-offset times; the rms velocity is the small-offset moveout velocity."
prereqs: [normal-moveout-correction, snells-law]
see_also: [semblance-velocity-analysis, common-midpoint-stacking, seismic-reflection-model, traveltime-tomography, seismic-migration, condition-number, full-waveform-inversion, eikonal-equation]
sources:
  - paper: doi:10.1190/1.1438126
    title: C. Hewitt Dix, Seismic velocities from surface measurements, Geophysics 20(1), 1955, 68 to 86
    locator: the rms velocity of a stack of horizontal layers as the velocity of the small-offset moveout, and the interval velocity of a layer from the rms velocities and times at its top and bottom
  - paper: doi:10.1190/1.1440058
    title: M. Turhan Taner and Fulton Koehler, Velocity spectra, digital computer derivation and applications of velocity functions, Geophysics 34(6), 1969, 859 to 881
    locator: the series of the squared traveltime in powers of the squared offset for horizontal layers, with the rms velocity in the second term
  - book: isbn:9781560800941
    title: Oz Yilmaz, Seismic Data Analysis, Society of Exploration Geophysicists, 2001, Investigations in Geophysics 10
    locator: the chapter on velocity analysis (the Dix conversion from stacking to interval velocities)
---

The Dix formula turns the velocities that come out of [velocity analysis](/semblance-velocity-analysis/) into the velocities of the layers. For a stack of flat, horizontal layers, the reflection from the bottom of layer $n$ has, at small offsets, the hyperbolic [normal moveout](/normal-moveout-correction/) of a single medium whose velocity is the root-mean-square (rms) velocity $V_n$ of the layers above. The interval velocity of layer $n$ then follows from the rms velocities and zero-offset times at its top and bottom:
$$v_n^2 = \frac{V_n^2\, t_n - V_{n-1}^2\, t_{n-1}}{t_n - t_{n-1}}.$$
For $V = 2000$ m/s at $t = 1$ s and $V = 2500$ m/s at $t = 2$ s, the layer between has $v = \sqrt{(2500^2 \cdot 2 - 2000^2 \cdot 1)/1} = 2915.5$ m/s. The page states the formula as a theorem with its hypotheses. In practice the velocities that enter it are stacking velocities picked over a finite spread, which are not exactly rms velocities, so its use on real data is an approximation.

## Statement

**Model.** The earth is a stack of flat, horizontal layers $k = 1, 2, \ldots$ with constant velocities $v_k > 0$ and thicknesses $h_k > 0$, the depth $z$ positive down. Source and receiver are on the surface $z = 0$ at offset $x$, and only the primary reflection from the bottom of layer $n$ is considered, along the ray that obeys [Snell's law](/snells-law/) at each boundary. Let $\Delta\tau_k = 2 h_k / v_k$ be the two-way vertical time in layer $k$ and $t_n = \sum_{k \le n} \Delta\tau_k$ the zero-offset two-way time of reflector $n$. Define the rms velocity by
$$V_n^2 = \frac{1}{t_n} \sum_{k=1}^{n} v_k^2\, \Delta\tau_k .$$

**Theorem.**

1. (Small-offset moveout.) The two-way time $t_n(x)$ of the reflection from the bottom of layer $n$ satisfies
$$t_n(x)^2 = t_n^2 + \frac{x^2}{V_n^2} + O(x^4) \qquad (x \to 0).$$
More precisely, $t_n(x)^2 = t_n^2 + x^2/V_n^2 + C_n x^4 + O(x^6)$ with $C_n = (\mu_2^2 - \mu_4)/(4\, t_n^2 \mu_2^4) \le 0$, where $\mu_j = t_n^{-1} \sum_{k \le n} v_k^j \Delta\tau_k$, and $C_n = 0$ if and only if all $v_k$, $k \le n$, are equal.
2. (Dix formula.) For $n \ge 2$, $V_n^2 t_n - V_{n-1}^2 t_{n-1} = v_n^2 (t_n - t_{n-1})$, so
$$v_n = \sqrt{\frac{V_n^2\, t_n - V_{n-1}^2\, t_{n-1}}{t_n - t_{n-1}}}, \qquad h_n = \tfrac{1}{2}\, v_n\, (t_n - t_{n-1}).$$
For $n = 1$, $v_1 = V_1$.

Part 1 says what velocity analysis measures in the limit of small offsets; part 2 is an identity between the rms velocities and the interval velocities.

## In plain words

Sound goes down through layers of rock, each with its own speed, and bounces back from the bottom of a layer. If you move the receiver away from the source, the echo comes a bit later, and the delay grows in a way that looks as if all the rock above were one block with a single speed. That speed is a kind of average of the layer speeds, with fast layers counting more. Velocity analysis measures this average for each echo. The Dix formula takes the averages for the top and the bottom of one layer, with the echo times, and recovers the speed inside that layer alone, like peeling the layers one by one from the top. It assumes flat layers and short offsets, and small errors in the averages give large errors for thin layers.

## Proof

**Part 1.** Let $p$ be the ray parameter, constant along the ray by Snell's law, with $p\, v_k = \sin\theta_k$, where $\theta_k$ is the angle of the ray from the vertical in layer $k$. Take $0 \le p < 1/\max_{k \le n} v_k$, so the ray reaches the reflector. In layer $k$ the ray goes down and up, each time over the horizontal distance $h_k \tan\theta_k$, in the time $h_k/(v_k \cos\theta_k)$. With $\cos\theta_k = \sqrt{1 - p^2 v_k^2}$ and $h_k = v_k \Delta\tau_k/2$,
$$x(p) = p \sum_{k \le n} \frac{v_k^2\, \Delta\tau_k}{\sqrt{1 - p^2 v_k^2}}, \qquad t(p) = \sum_{k \le n} \frac{\Delta\tau_k}{\sqrt{1 - p^2 v_k^2}} .$$
Both are analytic in $p$ near $0$; $x$ is odd and $t$ is even. With $(1 - u)^{-1/2} = 1 + u/2 + 3u^2/8 + O(u^3)$,
$$x = p\, t_n \big(\mu_2 + \tfrac{1}{2} p^2 \mu_4\big) + O(p^5), \qquad t = t_n \big(1 + \tfrac{1}{2} p^2 \mu_2 + \tfrac{3}{8} p^4 \mu_4\big) + O(p^6).$$
Since $x'(0) = t_n \mu_2 > 0$, $x(p)$ has an analytic odd inverse near $0$, so $t^2$ is an analytic even function of $x$ near $0$, a series in $x^2$. To find its terms, square:
$$t^2 = t_n^2 \big(1 + p^2 \mu_2 + p^4 (\tfrac{1}{4}\mu_2^2 + \tfrac{3}{4}\mu_4)\big) + O(p^6), \qquad x^2 = p^2 t_n^2 \mu_2^2 + p^4 t_n^2 \mu_2 \mu_4 + O(p^6).$$
Put $t^2 = t_n^2 + A x^2 + C x^4 + O(x^6)$ and compare the coefficients of $p^2$ and $p^4$. The $p^2$ terms give $t_n^2 \mu_2 = A t_n^2 \mu_2^2$, so $A = 1/\mu_2 = 1/V_n^2$, because $\mu_2 = V_n^2$ by the definition. The $p^4$ terms give $t_n^2 (\tfrac14 \mu_2^2 + \tfrac34 \mu_4) = A t_n^2 \mu_2 \mu_4 + C t_n^4 \mu_2^4$, so $C = (\mu_2^2 - \mu_4)/(4 t_n^2 \mu_2^4)$. The weights $\Delta\tau_k / t_n$ are positive and sum to 1, so by the Cauchy-Schwarz inequality $\mu_2^2 = \big(\sum_k (\Delta\tau_k/t_n)\, v_k^2\big)^2 \le \sum_k (\Delta\tau_k/t_n)\, v_k^4 = \mu_4$, with equality if and only if all $v_k^2$ are equal. $\square$

**Part 2.** By the definition, $V_n^2 t_n = \sum_{k \le n} v_k^2 \Delta\tau_k$. Subtract the same sum for $n - 1$: $V_n^2 t_n - V_{n-1}^2 t_{n-1} = v_n^2 \Delta\tau_n = v_n^2 (t_n - t_{n-1})$. Divide by $t_n - t_{n-1} = \Delta\tau_n > 0$ and take the positive root. The thickness is $h_n = v_n \Delta\tau_n / 2$ by the definition of $\Delta\tau_n$. For $n = 1$ the sum has one term. $\square$

**Check.** Two layers, 400 m at 2000 m/s over 600 m at 3000 m/s: $\Delta\tau_1 = \Delta\tau_2 = 0.4$ s, $t_2 = 0.8$ s and $V_2^2 = (2000^2 + 3000^2)/2$, so $V_2 = 2549.5$ m/s. The Dix formula gives $v_2^2 = (2549.5^2 \cdot 0.8 - 2000^2 \cdot 0.4)/0.4 = 9 \times 10^6$, that is $3000$ m/s exactly.

## Consequences

- Layer stripping: from rms velocities picked at the times of several reflectors, the formula gives the velocity and thickness of each layer from the top down, and so a depth model from time data (a theorem under the model).
- Under the model, $V_n^2 t_n$ is nondecreasing in $t_n$, so picks with $V_n^2 t_n < V_{n-1}^2 t_{n-1}$ cannot come from flat layers; the formula then gives an imaginary velocity. Such picks show a picking error or a failed hypothesis (a theorem for the first part, a heuristic for the diagnosis).
- Sensitivity: to first order, $\partial (v_n^2)/\partial (V_n^2) = t_n / (t_n - t_{n-1})$. So the relative error of $v_n$ is about $\tfrac{t_n}{t_n - t_{n-1}} \cdot \tfrac{V_n^2}{v_n^2}$ times the relative error of $V_n$ (a theorem, by differentiation). For $V = 2000$ at 1 s and $2500$ at 2 s, a 1% error in the second, $2525$ m/s, gives $2958.3$ m/s, an error of 1.5%. For a thin layer, $V = 2400$ at 1.9 s and $2450$ at 2.0 s give $3257.3$ m/s, and a 1% error at 2.0 s gives $3608.7$ m/s, an error of 10.8%, close to the first-order factor $20 \times 0.566 = 11.3$.
- So interval velocities of thin layers from Dix are noisy, and they are usually computed over smoothed velocity functions or by a regularized inversion of all picks together (a heuristic in practice).
- With the [convolutional model](/seismic-reflection-model/), the interval velocities and the reflection coefficients together describe the layers; [traveltime tomography](/traveltime-tomography/) and [full waveform inversion](/full-waveform-inversion/) replace the Dix conversion where the layers are not flat.

## Tightness

- The $x^4$ term is not zero when the layers differ, and it is negative, so at finite offsets the reflection comes earlier than the rms hyperbola. For the two-layer check model, $C_2 = -1.37 \times 10^{-15}$ s²/m⁴, and the true time is earlier than the hyperbola by 0.7 ms at 1000 m, 8.5 ms at 2000 m and 28.5 ms at 3000 m (a measurement, by ray tracing with the formulas of the proof).
- So a hyperbola fitted over a spread is faster than $V_n$. Fitting $t^2$ against $x^2$ by least squares, with $t_n$ free, at 41 equally spaced offsets from 0 to $x_{\max}$ gives the velocity $2559.2$, $2585.2$ and $2619.9$ m/s for $x_{\max} = 1000$, $2000$ and $3000$ m, against $V_2 = 2549.5$ m/s. Put into the Dix formula with the exact $V_1 = 2000$, these give $3016.4$, $3060.4$ and $3118.9$ m/s for the second layer, against the true 3000 m/s (measurements). The bias grows with the spread; this is why the formula is a small-offset result.
- A negative argument: $V = 2500$ m/s at 1 s and $1700$ m/s at 2 s give $1700^2 \cdot 2 - 2500^2 \cdot 1 = -470000 < 0$, so no real interval velocity fits, as the second consequence predicts.
- Dip breaks the model: for one plane reflector dipping at the angle $\varphi$ in a constant velocity $v$, with the line along the dip, $t^2 = t_0^2 + x^2 \cos^2\varphi / v^2$ exactly (a theorem, by the image of the source in the reflector), so the moveout velocity is $v/\cos\varphi$, not $v$. The Dix formula applied to such velocities is wrong unless the dip is corrected first.
- Lateral changes of velocity, anisotropy and curved rays at large offsets also make the stacking velocity differ from the rms velocity; then the formula is only a first estimate.

## History

Dix (1955) gave the result in "Seismic velocities from surface measurements". He showed that for horizontal layers the moveout of a reflection at small offsets is governed by the rms velocity of the layers above it, and gave the formula for the interval velocity of a layer from the rms velocities at its top and bottom. Taner and Koehler (1969) wrote the squared traveltime as a series in the squared offset, with the rms velocity in the second term, and computed velocity spectra by digital computer; the Dix conversion of picked stacking velocities to interval velocities became a standard step of seismic processing.

## References
