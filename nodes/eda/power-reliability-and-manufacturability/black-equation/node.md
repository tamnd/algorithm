---
tag: 4HRA40
kind: model
slug: black-equation
name: Black's equation
aliases:
- Black's law
- electromigration lifetime model
area: eda/power-reliability-and-manufacturability
level: core
summary: Black's model of electromigration lifetime of a wire, MTTF = A J^(-n) e^(Ea / kT), with J the current density, Ea an activation energy and T the temperature.
prereqs: [power-grid-analysis]
see_also: [blech-length, compact-thermal-model, nbti-reaction-diffusion-model, dynamic-power-dissipation, leakage-power, soft-error-masking]
sources:
  - paper: doi:10.1109/T-ED.1969.16754
    title: James R. Black, Electromigration, a brief survey and some recent results, IEEE Transactions on Electron Devices 16(4), 338 to 347, 1969
    locator: the section on recent results, where the median time to failure of aluminum conductors is fitted as A J^(-2) exp(phi / kT), with the activation energies found for different grain structures
  - paper: doi:10.1063/1.336731
    title: Michael Shatzkes and James R. Lloyd, A model for conductor failure considering diffusion concurrently with electromigration resulting in a current exponent of 2, Journal of Applied Physics 59(11), 3890 to 3893, 1986
    locator: the whole paper, a derivation of the current exponent n = 2 from a model of void nucleation by diffusion and electromigration
  - paper: doi:10.1063/1.322842
    title: Ilan A. Blech, Electromigration in thin aluminum films on titanium nitride, Journal of Applied Physics 47(4), 1203 to 1208, 1976
    locator: the threshold product of current density and length below which no drift occurs, which Black's equation does not contain
---

Black's equation is the standard empirical model of the lifetime of a metal wire that fails by *electromigration*. It says that the median time to failure of a population of identical wires, held at a constant current density $J$ and absolute temperature $T$, is

$$ t_{50} = A\, J^{-n} \exp\!\Big(\frac{E_a}{k T}\Big), $$

where $k$ is Boltzmann's constant and $A$, $n$ and $E_a$ are constants fitted to accelerated tests of one wire technology. Black proposed it in 1969 for aluminum lines with $n = 2$. Chip design flows use it to turn a lifetime target into limits on the current density of every wire and via, at the temperature that the chip reaches.

The model is empirical. Its form has a physical motivation, but $A$, $n$ and $E_a$ are not computed from first principles: they come from fits to test data, they change with the metal, the barrier, the cap layer, the grain structure and the geometry, and the fitted values hold only near the range of the tests. Every number on this page that is not a result of algebra is such a fitted value or an assumption for the example.

## The machine

**Electromigration.** The electrons of a current transfer momentum to the metal ions they scatter on, the so-called *electron wind*. This gives a small net force on the ions in the direction of the electron flow, $F = Z^* e \rho J$, where $\rho$ is the resistivity, $e$ the elementary charge and $Z^*$ an effective charge number, itself a material constant that is measured. The ions drift by thermally activated diffusion with a diffusivity $D = D_0 e^{-E_a/kT}$, so the atom flux is of the form $\frac{C D}{kT} Z^* e \rho J$ (the Nernst and Einstein relation, with $C$ the atom concentration). Where the flux diverges, at grain boundaries, at the ends of a line, at a via, atoms pile up or deplete. Depletion makes *voids*, which raise the resistance or open the line. Pile-up makes *hillocks* or extrusions, which can short to a neighbor wire. In copper interconnect, most transport runs along the interface between the copper and its dielectric cap, and the via is the common failure site.

**Inputs.** For a wire segment: its current density $J$ (current divided by cross-section area, in A/cm²), its temperature $T$ in kelvin, and the three fitted constants of the technology. In a chip flow, $J$ comes from [power grid analysis](/power-grid-analysis/) for supply wires and from switching currents ([dynamic power](/dynamic-power-dissipation/)) for signal wires, and $T$ comes from a [compact thermal model](/compact-thermal-model/) plus the self-heating of the wire.

**Output.** The time to failure $t_{50}$. Black wrote it as the mean time to failure (MTTF), and the name stayed, but current practice fits it as the median of the failure times.

**Fitted constants.**

- $A$ holds the geometry, the microstructure and the failure criterion (for example a 10 or 20 percent resistance rise). It has no meaning across technologies.
- $n$, the current exponent. Black found $n = 2$ for aluminum. Measured values run from about 1 to above 2. A value near 1 is usually read as a lifetime set by void growth, and a value near 2 as a lifetime set by void nucleation. Shatzkes and Lloyd derived $n = 2$ from a model of nucleation.
- $E_a$, the activation energy of the dominant diffusion path, in eV. Black reported values near 0.5 eV for the fine-grained aluminum films of his time. Copper with a dielectric cap is often fitted with values near 0.9 eV, but each process measures its own.

**The physical motivation, and why it is not a derivation.** The exponential is the Arrhenius law of the diffusivity. Black argued for $J^{-2}$ from the number of electrons times their momentum transfer. The drift flux above is linear in $J$ and has a $1/T$ prefactor that the equation drops. The equation is the form that fits the data, not a consequence of the drift law.

## What it counts

It counts time to failure of a wire under *steady* stress: constant $J$ and constant $T$, with $J$ in one direction. It gives one parameter of a distribution, the median of the failure times of many identical wires. The spread of the failure times is a separate fitted parameter. Failure times are usually fitted with a lognormal law, so the fraction $p$ of wires fails by $t_p = t_{50}\, e^{z_p \sigma}$, where $z_p$ is the standard normal quantile and $\sigma$ the fitted shape. Design targets a small fraction, for example 0.1 percent, and not the median.

**Time-varying currents.** For a current that flows in one direction but varies, flows usually use the average current density in Black's equation. Current that reverses direction, as in most signal wires, causes much less damage because of partial healing, and flows then check a separately fitted limit. The root mean square current sets the self-heating, which enters through $T$. These rules are engineering practice fitted to tests. They do not follow from the equation.

## Relation to other models

- **Blech length.** Black's equation predicts a finite lifetime for every $J > 0$. A short line does not fail at all if $J L$ is below a critical product, because mechanical back stress stops the drift. That is the [Blech length](/blech-length/) effect. Some flows use a modified form with $(J - J_c)^{-n}$, where $J_c$ is the threshold current density of the given length.
- **Stress-based models.** Physical models solve a diffusion equation for the stress in the line, of the same type as the [heat equation](/heat-equation/), and predict the nucleation time of a void. Black's equation is the compact empirical summary that design tools use in their place.
- **Thermal model.** Because $T$ enters through an exponential, the lifetime depends strongly on the temperature map from the [compact thermal model](/compact-thermal-model/), and that map depends on the [leakage power](/leakage-power/), which grows with temperature.
- **Other aging models.** Transistor aging, such as NBTI described by the [reaction-diffusion model](/nbti-reaction-diffusion-model/), is a separate wear-out mechanism with its own empirical laws. Both are part of a chip's reliability budget.

## Known results in the model

**Acceleration factor.** This is exact under the model. Tests run at a high stress current density $J_s$ and temperature $T_s$, and use conditions are $J_u$ and $T_u$. The constant $A$ cancels:

$$ \mathrm{AF} = \frac{t_{50}(J_u, T_u)}{t_{50}(J_s, T_s)} = \Big(\frac{J_s}{J_u}\Big)^{n} \exp\!\Big(\frac{E_a}{k}\Big(\frac{1}{T_u} - \frac{1}{T_s}\Big)\Big). $$

**Example.** Stress at 300 °C and 2 MA/cm². Use at 105 °C and 0.5 MA/cm². With $k = 8.617 \times 10^{-5}$ eV/K, $T_s = 573.15$ K and $T_u = 378.15$ K. The temperature part alone for $E_a = 0.9$ eV is $1.20 \times 10^4$, and the current part is $4^n$.

| $E_a$ (eV) | AF for $n = 1$ | AF for $n = 2$ |
|---|---|---|
| 0.7 | $5.97 \times 10^3$ | $2.39 \times 10^4$ |
| 0.8 | $1.70 \times 10^4$ | $6.79 \times 10^4$ |
| 0.9 | $4.82 \times 10^4$ | $1.93 \times 10^5$ |
| 1.0 | $1.37 \times 10^5$ | $5.48 \times 10^5$ |

An error of 0.1 eV in the fitted $E_a$ changes the predicted use lifetime by a factor of about 3, and the range 0.7 to 1.0 eV spans a factor of 23. This is why the fit of $E_a$, from tests at several temperatures, is the most important part of an electromigration qualification.

**Temperature sensitivity.** At 105 °C with $E_a = 0.9$ eV, a wire that is 5 K hotter, for example from self-heating, has 0.70 times the lifetime, and one that is 10 K hotter has 0.49 times the lifetime.

**Design limit.** Solving the equation for $J$ gives the largest current density that meets a target lifetime $t^*$ at temperature $T$, from a test median $t_s$ at $(J_s, T_s)$:

$$ J_{\max}(T) = J_s \Big(\frac{t_s}{t^*}\Big)^{1/n} \exp\!\Big(\frac{E_a}{n k}\Big(\frac{1}{T} - \frac{1}{T_s}\Big)\Big). $$

Here $t_s$ and $t^*$ refer to the same failure fraction. With a lognormal spread $\sigma = 0.5$, the 0.1 percent point is $e^{-3.09 \times 0.5} = 0.21$ times the median, so a target on the 0.1 percent point is a target about 4.7 times longer on the median. Tools apply $J_{\max}$, scaled by width and by via count, to each segment of the extracted wires.

**Fitting.** Taking logarithms gives $\ln t_{50} = \ln A - n \ln J + E_a / (kT)$, which is linear in the unknowns $\ln A$, $n$ and $E_a$. Medians from tests at two or more current densities and two or more temperatures give the three constants by least squares. If the tests do not vary $J$ and $T$ independently, for example because self-heating raises $T$ with $J$, the fitted $n$ absorbs part of the temperature effect and the model then extrapolates wrongly. Tests use test lines that heat little, and correct $T$ for Joule heating.

**Mean and median.** For a lognormal law with shape $\sigma$, the mean time to failure is $t_{50}\, e^{\sigma^2 / 2}$, which is 1.13 times the median for $\sigma = 0.5$. The names MTTF and median are often mixed up, so a quoted value must say which one it is.

## References
