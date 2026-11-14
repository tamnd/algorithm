---
tag: 74JRDG
kind: definition
slug: blech-length
name: Blech length
aliases:
- Blech effect
- short-length immortality
area: eda/power-reliability-and-manufacturability
level: advanced
summary: A wire whose length times current density is below a critical product does not fail by electromigration, since back stress balances the electron wind.
prereqs: [black-equation]
see_also: [power-grid-analysis, compact-thermal-model, heat-equation, dynamic-power-dissipation]
sources:
  - paper: doi:10.1063/1.322842
    title: Ilan A. Blech, Electromigration in thin aluminum films on titanium nitride, Journal of Applied Physics 47(4), 1203 to 1208, 1976
    locator: the drift measurements on aluminum stripes of different lengths on a titanium nitride underlayer, the threshold current density that is inversely proportional to the stripe length, and its explanation by a stress gradient that opposes the drift
  - paper: doi:10.1109/T-ED.1969.16754
    title: James R. Black, Electromigration, a brief survey and some recent results, IEEE Transactions on Electron Devices 16(4), 338 to 347, 1969
    locator: the lifetime model that the Blech condition supplements with a threshold
---

## Definition

Take a straight metal line of length $L$ that carries a current density $j$ in one direction, with both ends blocked for metal atoms (for example by the barrier at a via). The electron wind pushes atoms toward the anode end, and they cannot leave. Atoms pile up at the anode and deplete at the cathode, so a compressive stress builds at one end and a tensile stress at the other. The stress gradient pushes atoms back.

The atom flux along the line, in one dimension, is

$$ J_a = \frac{C D}{k T} \Big( Z^* e \rho j - \Omega \frac{\partial \sigma}{\partial x} \Big), $$

where $C$ is the atom concentration, $D$ the diffusivity, $Z^*$ the effective charge number, $e$ the elementary charge, $\rho$ the resistivity, $\Omega$ the atomic volume and $\sigma$ the hydrostatic stress, positive in compression. A steady state has $J_a = 0$ at every point, so $\partial \sigma / \partial x = Z^* e \rho j / \Omega$, a constant. The stress is linear along the line, and the stress difference between its ends is

$$ \Delta \sigma = \frac{Z^* e \rho\, j L}{\Omega}. $$

Let $\Delta \sigma_c$ be the largest end-to-end stress difference that the line can hold without forming a void at the cathode or an extrusion at the anode. Then the line reaches a steady state without damage if

$$ j L < (jL)_c = \frac{\Omega\, \Delta \sigma_c}{Z^* e \rho}. $$

The product $(jL)_c$ is the *critical product* (or Blech product). For a given $j$, the *Blech length* is $L_B = (jL)_c / j$, and lines shorter than $L_B$ are called *immortal*: [Black's equation](/black-equation/) does not apply to them, because no net drift continues. For a given $L$, the threshold current density is $j_c = (jL)_c / L$, inversely proportional to the length. Blech observed this inverse law in 1976, on aluminum stripes on titanium nitride.

**What is fitted.** The steady-state law above is a simple consequence of the flux equation under its assumptions: one dimension, blocking ends, constant $Z^*$, $\rho$ and $\Omega$, and a stress that the line can hold elastically. The quantities in $(jL)_c$ are not known well enough to compute it. $Z^*$ is measured indirectly, and $\Delta \sigma_c$ depends on the initial residual stress, the cap, the liner and the defects that nucleate voids. Design rules therefore use a measured critical product for each metal level and technology. Some treatments define $\Delta \sigma_c$ from the initial stress and the stress at each end. This changes the meaning of the constant, not the form $jL < (jL)_c$.

## Examples and non-examples

**Example (assumed critical product).** Let $(jL)_c = 3000$ A/cm be the measured value for one metal level. A line at $j = 1$ MA/cm² has $L_B = 3000 / 10^6$ cm $= 30$ µm. At 2 MA/cm² the Blech length is 15 µm. A 20 µm segment at 1 MA/cm² has $jL = 2000$ A/cm and is immortal. Its threshold current density is $3000 / (20 \times 10^{-4}) = 1.5$ MA/cm².

**Example (the arithmetic of the formula).** With the assumed values $\Omega = 1.18 \times 10^{-29}$ m³ (the atomic volume of copper), $\Delta \sigma_c = 400$ MPa, $\rho = 2.5 \times 10^{-8}$ Ω m and $Z^* = 4$, the formula gives $(jL)_c = 4.72 \times 10^{-21} / (4 \times 1.602 \times 10^{-19} \times 2.5 \times 10^{-8}) \approx 2.9 \times 10^5$ A/m, or about 2900 A/cm. A different but equally plausible $Z^*$ or $\Delta \sigma_c$ changes the result by a factor of several, which is why the product is measured and not computed.

**Non-example (segments in series).** Two segments of the same cross-section, each 20 µm long at 1 MA/cm² in the same direction, meet at a junction through which atoms can pass, and only the two far ends are blocked. Each segment alone has $jL = 2000 < 3000$ A/cm. In the steady state the stress is continuous at the junction and has the same slope in each segment, so the end-to-end difference adds up to $4000$ A/cm times $Z^* e \rho / \Omega$, above the limit. The pair is not immortal. In general, the immortality of a tree of segments needs the stress analysis of the whole tree, not the $jL$ of each segment.

**Non-example (opposite currents).** If the two segments of the last example carry current in opposite directions, for example a line fed at its middle, the stress slopes have opposite signs and the end-to-end difference is 0. Each half is then checked against its own blocked end and the junction.

**Non-example (no blocking end).** A line whose ends let atoms flow into a large reservoir builds no back stress, and the Blech condition does not apply.

## Related definitions

- **Black's equation.** The empirical lifetime of a line that is not immortal, see [Black's equation](/black-equation/). A common combination uses $(j - j_c)^{-n}$ in place of $j^{-n}$, so the lifetime becomes infinite at the threshold.
- **Stress evolution.** Before the steady state, the stress obeys a diffusion equation of the same type as the [heat equation](/heat-equation/), with the electron wind as a boundary flux. Its time constant is of order $L^2$ divided by an effective diffusivity, so short lines reach the steady state fast.
- **Current density in design.** [Power grid analysis](/power-grid-analysis/) gives the current in each segment of the supply network, and the segment lengths come from the layout. Electromigration checkers use the Blech condition to relax the current limit on short segments, and use Black's equation for the others.
- **Temperature.** The critical product depends on temperature through $\rho$ and through the residual stress, so the check uses the temperature map from the [compact thermal model](/compact-thermal-model/).

## References
