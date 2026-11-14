---
tag: BW2EMP
kind: model
slug: pelgrom-mismatch-model
name: Pelgrom mismatch model
aliases:
- Pelgrom's law
area: eda/fpga-analog-and-emerging-technologies
level: core
summary: Pelgrom's model in which the standard deviation of the mismatch of two matched transistors falls as one over the square root of their gate area.
prereqs: [variance, shichman-hodges-model, central-limit-theorem]
see_also: [common-centroid-layout, analog-symmetry-constraint, monte-carlo-tolerance-analysis, analog-circuit-sizing, statistical-static-timing-analysis, expected-value]
sources:
  - paper: doi:10.1109/JSSC.1989.572629
    title: Marcel J. M. Pelgrom, Aad C. J. Duinmaijer and Anton P. G. Welbers, Matching properties of MOS transistors, IEEE Journal of Solid-State Circuits 24(5), 1433 to 1440, 1989
    locator: the derivation of the variance of a parameter difference from the spatial spectrum of the parameter, the law with an area term and a distance term, and the measured mismatch of the threshold voltage and of the current factor
  - paper: doi:10.1109/JSSC.2005.848021
    title: Peter R. Kinget, Device mismatch and tradeoffs in the design of analog circuits, IEEE Journal of Solid-State Circuits 40(6), 1212 to 1224, 2005
    locator: the mismatch models of MOS and bipolar devices, the minimum area that an accuracy needs, and the resulting tradeoff between bandwidth, accuracy and power
  - book: isbn:9780131464100
    title: Alan Hastings, The Art of Analog Layout, second edition, Prentice Hall, 2006
    locator: the chapters on matching (random and systematic mismatch, and the rules that reduce the systematic part)
  - paper: doi:10.1109/5.899053
    title: Georges G. E. Gielen and Rob A. Rutenbar, Computer-aided design of analog and mixed-signal integrated circuits, Proceedings of the IEEE 88(12), 1825 to 1854, 2000
    locator: the treatment of mismatch and yield in analog sizing and layout
---

The Pelgrom mismatch model gives the spread of the difference between two transistors that are drawn the same: the variance of the difference of a parameter $P$ is $A_P^2 / (WL) + S_P^2 D^2$, where $WL$ is the gate area and $D$ the distance between the devices. Its topic is analog sizing and layout, one of the five topics of this sub-area. Pelgrom, Duinmaijer and Welbers derived the form in 1989 from a model of the process as a random field, and checked it on measured transistor pairs. The two constants $A_P$ and $S_P$ are not derived: they are fitted for each process and each parameter, from measurements of many pairs.

## The machine

**The devices.** Two MOS transistors of the same type, with the same gate width $W$, length $L$ and orientation, at a distance $D$ from each other. A parameter $P$ of a device is a property such as the threshold voltage $V_T$ or the current factor $\beta = \mu C_{ox} W / L$ of the [square-law model](/shichman-hodges-model/). The *mismatch* is $\Delta P = P_1 - P_2$.

**The law.** The model treats $\Delta P$ as a random variable with mean zero (systematic offsets, such as those of the layout, are handled apart) and

$$\sigma^2(\Delta P) = \frac{A_P^2}{W L} + S_P^2 D^2.$$

For the threshold voltage, $\sigma(\Delta V_T) = A_{VT} / \sqrt{WL}$ when $D$ is small. $A_{VT}$ has the unit of a voltage times a length, such as mV µm. For the current factor the law is written for the relative mismatch, $\sigma(\Delta\beta/\beta) = A_\beta / \sqrt{WL}$, with $A_\beta$ in percent µm.

**Fitted and derived parts.** The form of the law is derived below from two assumptions on the process. The numbers $A_{VT}$, $S_{VT}$, $A_\beta$ and $S_\beta$ are fitted to measurements of a test chip, by a [linear regression](/linear-regression/) of the measured $\sigma^2(\Delta P)$ against $1/(WL)$ and $D^2$. They change from process to process, and from n-channel to p-channel devices. Foundries give them in their design kits as statistical device models. The square-law model of the current, with its own fitted parameters $\mu C_{ox}$, $V_{T0}$ and $\lambda$, is a second model on top of this one.

**Where the form comes from.** Let the parameter at a point $r$ of the die be $p(r) = \bar p + n(r) + \ell(r)$, and let a device take the mean of $p$ over its gate area $G$, $P = \frac{1}{|G|} \int_G p$.

1. The short-range part $n$ is a stationary random field with mean 0 and a covariance $C(r - r')$ whose range is much smaller than the device, with $\kappa = \int C(u)\, du$ finite. Dopant atoms, oxide charges and grain boundaries give such a field.
2. The long-range part $\ell$ is smooth over the distance between the devices, so near them it is $\ell(r) = \ell_0 + g \cdot r$, with a gradient $g$ that is random from die to die, mean 0, and $E[(g \cdot u)^2] = s^2$ for every unit vector $u$.

Then $\mathrm{Var}(\frac{1}{|G|}\int_G n) = \frac{1}{|G|^2} \int_G \int_G C(r - r')\, dr\, dr'$. When $G$ is large compared with the range of $C$, the inner integral is $\kappa$ for all $r$ except near the edge, so the variance is $\kappa / |G|$ up to a term of the order of the perimeter over $|G|^2$. Two devices further apart than the range of $C$ have uncorrelated short-range parts, so this part of $\Delta P$ has the variance $2\kappa / (WL)$. The long-range part of $\Delta P$ is $g \cdot (c_1 - c_2)$, where $c_i$ are the centers, with the variance $s^2 D^2$. The two parts are independent. So $A_P^2 = 2\kappa$ and $S_P^2 = s^2$. This derivation is proved under the two assumptions; that real processes meet them is what Pelgrom's measurements test.

## What it counts

The model counts one number: the standard deviation of the difference of a parameter between two matched devices, as a function of their area and their distance. A single device differs from the mean of the two by $\Delta P / 2$, and from the nominal value by a variable whose variance is half that of $\Delta P$ in the area term.

**The area needed for an accuracy.** If the area term dominates, $\sigma(\Delta P) \le \sigma_0$ needs $WL \ge A_P^2 / \sigma_0^2$. Halving the mismatch costs four times the area. With an assumed $A_{VT} = 5$ mV µm (a value chosen here for the example, not taken from a source), a pair of $10\ \mu\text{m} \times 1\ \mu\text{m}$ has $\sigma(\Delta V_T) = 5 / \sqrt{10} \approx 1.58$ mV. For $\sigma = 0.5$ mV it needs $WL = 100\ \mu\text{m}^2$.

**The current of a pair.** In saturation, with the square law $I = \frac{\beta}{2}(V_{GS} - V_T)^2$ and the overdrive $V_{ov} = V_{GS} - V_T$, a small mismatch gives

$$\frac{\Delta I}{I} = \frac{\Delta \beta}{\beta} - \frac{2 \Delta V_T}{V_{ov}}.$$

If the two mismatches are independent, $\sigma^2(\Delta I / I) = \sigma^2(\Delta\beta/\beta) + 4 \sigma^2(\Delta V_T)/V_{ov}^2$. With the pair above, $V_{ov} = 0.2$ V and an assumed $A_\beta = 1$ percent µm, the two terms are $0.316$ percent and $1.58$ percent, and $\sigma(\Delta I/I) \approx 1.61$ percent. The threshold term dominates at small overdrive, so a current mirror is biased with a large overdrive and a differential pair with a small one, where the input offset is $\Delta V_T$ plus a $\beta$ term scaled by $V_{ov}/2$.

**Yield.** A circuit whose offset must stay within $\pm 3\sigma$ passes on about 99.7 percent of the dies if the offset is normal, a property that the model assumes and that the [central limit theorem](/central-limit-theorem/) makes plausible, because $\Delta P$ is an average over many small independent sources.

## Relation to other models

- **The square-law model.** The [Shichman-Hodges model](/shichman-hodges-model/) gives the current of one device from fitted constants. The Pelgrom model gives the spread of those constants between two devices. A statistical device model in a design kit joins them: each device gets its own $V_T$ and $\beta$, drawn with variances from the area law.
- **Common-centroid layout.** In the derivation, a linear long-range part adds $g \cdot (c_1 - c_2)$ to the mismatch. A [common-centroid layout](/common-centroid-layout/) makes $c_1 = c_2$ and removes this term for every $g$, which leaves only the area term. A layout that puts the two devices far apart has a large $S_P D$ term.
- **Mirror symmetry.** A pair that meets the [symmetry constraint](/analog-symmetry-constraint/) has $c_1 - c_2$ across the axis, so a gradient across the axis stays. A gradient along the axis cancels.
- **Monte Carlo analysis.** [Monte Carlo tolerance analysis](/monte-carlo-tolerance-analysis/) draws device parameters from such a model and simulates the circuit many times, to estimate the yield of a sized design.
- **Timing.** [Statistical static timing analysis](/statistical-static-timing-analysis/) treats delays as random variables with a global part, shared by nearby gates, and a local random part, which is the same split as $\ell$ and $n$ above.
- **Bipolar devices.** The same form holds for the base-emitter voltage of bipolar transistors, with the emitter area in place of $WL$ and its own fitted constant.

## Known results in the model

- **The area law.** Pelgrom, Duinmaijer and Welbers measured the threshold and current-factor mismatch of transistor pairs of many sizes and distances and found the $1/\sqrt{WL}$ law and the distance term. These are measurements on the processes of that time; the constants of a newer process must be measured again.
- **Small devices.** The derivation drops a term of the order of the perimeter over the area squared, and assumes the device is large compared with the range of the short-range field. For very short or narrow devices neither holds, so the area law is an approximation there, and the constants are fitted over the sizes that a design uses.
- **The bandwidth, accuracy and power tradeoff.** Kinget shows that the minimum area that an accuracy needs sets a minimum gate capacitance, and with it a minimum power for a given bandwidth and accuracy, fixed by process constants such as $A_{VT}$. So an accuracy target cannot be bought for free by a better circuit at the same power and speed.
- **Sizing.** The minimum area $A_P^2 / \sigma_0^2$ is a lower bound on $WL$ that [analog circuit sizing](/analog-circuit-sizing/) adds as a constraint for each matched pair, next to the performance constraints.

## References
