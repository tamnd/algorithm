---
tag: 52M5DS
kind: model
slug: shichman-hodges-model
name: Shichman-Hodges model
aliases:
- SPICE level 1 MOSFET model
- square-law MOSFET model
area: eda/logic-and-circuit-simulation
level: intro
summary: The square-law MOSFET model of Shichman and Hodges that gives drain current in the cutoff, linear and saturation regions, the first MOS model of SPICE.
prereqs: [kirchhoff-circuit-laws]
see_also: [dc-operating-point-analysis, modified-nodal-analysis, newton-method-for-systems, switch-level-simulation, elmore-delay, logical-effort, leakage-power, nonlinear-delay-model]
sources:
  - paper: doi:10.1109/JSSC.1968.1049902
    title: Harold Shichman and David A. Hodges, Modeling and simulation of insulated-gate field-effect transistor switching circuits, IEEE Journal of Solid-State Circuits 3(3), 285 to 289, 1968
    locator: the drain current equations of the model, with the body effect, and their use in the simulation of switching circuits
  - paper: "Laurence W. Nagel, SPICE2: A Computer Program to Simulate Semiconductor Circuits, Memorandum UCB/ERL M520, Electronics Research Laboratory, University of California, Berkeley, 1975"
    title: Laurence W. Nagel, SPICE2, A Computer Program to Simulate Semiconductor Circuits, Memorandum UCB/ERL M520, University of California, Berkeley, May 1975
    locator: the chapter on semiconductor device models (the MOSFET model)
  - url: "https://sourceforge.net/p/ngspice/ngspice/ci/master/tree/src/spicelib/devices/mos1/mos1load.c"
    title: ngspice source code, the MOS level 1 model, file src/spicelib/devices/mos1/mos1load.c
    locator: the drain current in the linear and saturation regions, both multiplied by (1 + lambda vds), and the body effect term of the threshold
  - book: "Jan M. Rabaey, Anantha Chandrakasan and Borivoje Nikolic, Digital Integrated Circuits: A Design Perspective, second edition, Prentice Hall, 2003"
    title: Jan M. Rabaey, Anantha Chandrakasan and Borivoje Nikolic, Digital Integrated Circuits, second edition, Prentice Hall, 2003
    locator: the chapter The Devices (the long-channel square-law model and its limits for short channels) and the chapter The CMOS Inverter (switching threshold and propagation delay)
---

The Shichman-Hodges model is the square-law model of a long-channel MOSFET: it gives the drain current as a function of the gate, drain and bulk voltages in three regions, cutoff, linear and saturation, with a quadratic law in the gate overdrive. Shichman and Hodges published it in 1968 for the simulation of switching circuits, and it became the level 1 MOSFET model of SPICE. It belongs to the circuit simulation half of the logic and circuit simulation sub-area, where a simulator evaluates it and its derivatives once per transistor in every Newton iteration of [DC operating point analysis](/dc-operating-point-analysis/) and transient analysis. It is accurate only for long channels; for modern short-channel devices it is a teaching and hand-analysis model.

## The machine

**Terminals and voltages.** An n-channel MOSFET has a drain D, a gate G, a source S and a bulk B. The model takes $V_{GS}$, $V_{DS} \ge 0$ and $V_{BS} \le 0$ and returns the drain current $I_D$, which flows into the drain, through the channel, and out of the source. The gate draws no DC current.

**Parameters.** The transconductance parameter $k = \mu C_{ox} W/L$ (in SPICE, KP times $W/L$) combines the carrier mobility $\mu$, the gate oxide capacitance per area $C_{ox}$, the channel width $W$ and the channel length $L$. $V_{T0}$ is the zero-bias threshold, $\gamma$ the body effect coefficient, $\Phi$ the surface potential (PHI in SPICE) and $\lambda$ the channel-length modulation coefficient.

**Threshold.** With the body effect,

$$V_T = V_{T0} + \gamma \left( \sqrt{\Phi - V_{BS}} - \sqrt{\Phi} \right),$$

and the overdrive is $V_{ov} = V_{GS} - V_T$.

**Drain current.** In the form that SPICE level 1 uses,

$$I_D = \begin{cases} 0 & \text{cutoff, } V_{ov} \le 0, \\ k \left( V_{ov} - \tfrac12 V_{DS} \right) V_{DS} \,(1 + \lambda V_{DS}) & \text{linear, } 0 < V_{DS} < V_{ov}, \\ \tfrac{k}{2}\, V_{ov}^2 \,(1 + \lambda V_{DS}) & \text{saturation, } 0 < V_{ov} \le V_{DS}. \end{cases}$$

The factor $(1 + \lambda V_{DS})$ models channel-length modulation: in saturation the pinch-off point moves toward the source as $V_{DS}$ grows, so the current rises slowly instead of staying flat. Many textbooks put the factor in the saturation formula only. Then $I_D$ jumps by $\tfrac{k}{2}\lambda V_{ov}^3$ at $V_{DS} = V_{ov}$, which is why SPICE multiplies both regions by it.

**Symmetry and p-channel devices.** The device is symmetric. If $V_{DS} < 0$, the simulator swaps the roles of drain and source, evaluates the model, and negates the current. A p-channel device uses the same equations with all voltages and the current negated and a negative threshold.

## What it counts

The model maps three terminal voltages to one current and three small-signal conductances, at a constant cost per evaluation. In a simulator, each Newton iteration evaluates every transistor once and stamps its linearization into the [MNA](/modified-nodal-analysis/) matrix: the current $I_D$, the transconductance $g_m = \partial I_D / \partial V_{GS}$, the output conductance $g_{ds} = \partial I_D / \partial V_{DS}$ and the body transconductance $g_{mb} = \partial I_D / \partial V_{BS}$. With $\lambda$ in both regions:

$$g_m = \begin{cases} 0 \\ k V_{DS} (1 + \lambda V_{DS}) \\ k V_{ov} (1 + \lambda V_{DS}) \end{cases} \qquad g_{ds} = \begin{cases} 0 & \text{cutoff} \\ k (V_{ov} - V_{DS})(1 + \lambda V_{DS}) + k \lambda (V_{ov} - \tfrac12 V_{DS}) V_{DS} & \text{linear} \\ \tfrac{k}{2} \lambda V_{ov}^2 & \text{saturation} \end{cases}$$

and $g_{mb} = g_m \cdot \gamma / (2\sqrt{\Phi - V_{BS}})$, from the chain rule through $V_T$. So the device evaluation work of a DC or transient run is a constant times the number of transistors times the total number of Newton iterations.

**Worked example.** Take $k = 100\ \mu\text{A/V}^2$, $V_T = 1$ V (no body effect), $\lambda = 0.02\ \text{V}^{-1}$ and $V_{GS} = 3$ V, so $V_{ov} = 2$ V. At $V_{DS} = 5$ V the device is saturated and $I_D = 50\ \mu \cdot 4 \cdot 1.1 = 220\ \mu$A. At $V_{DS} = 1$ V it is linear and $I_D = 100\ \mu \cdot 1.5 \cdot 1 \cdot 1.02 = 153\ \mu$A. At the boundary $V_{DS} = 2$ V both formulas give $208\ \mu$A.

## Relation to other models

- **Later SPICE models.** Level 2 adds the change of the bulk charge along the channel and mobility degradation, level 3 is a semi-empirical short-channel model, and the BSIM family, EKV and PSP model velocity saturation, drain-induced barrier lowering, subthreshold conduction and many other effects. They all reduce to a square law for long channels at strong inversion.
- **Short-channel behavior.** When the lateral field is high, carriers reach their saturation velocity, and the saturation current grows roughly linearly in $V_{ov}$ instead of quadratically. The alpha-power law replaces the exponent 2 by a fitted exponent between 1 and 2.
- **Subthreshold.** The level 1 model gives zero current below threshold. Real devices conduct a current that falls exponentially with $V_T - V_{GS}$, which is the main source of [leakage power](/leakage-power/).
- **Digital abstractions.** [Switch-level simulation](/switch-level-simulation/) treats a transistor as a switch with a strength. Delay models such as [Elmore delay](/elmore-delay/) and [logical effort](/logical-effort/) replace an on transistor by an effective resistance, a constant that a square-law model can estimate, and table models such as the [nonlinear delay model](/nonlinear-delay-model/) are fitted to circuit simulation with full device models.
- **Diode-like devices.** Unlike a diode or a bipolar transistor, the square law has no exponential, so its Newton iteration cannot overflow; [junction voltage limiting](/junction-voltage-limiting/) is needed only for the junctions of the model, such as the bulk diodes.

## Known results in the model

**Smoothness.** Take $\gamma = 0$, so that $V_T = V_{T0}$. With $\lambda$ in both regions, $I_D(V_{GS}, V_{DS})$ is continuously differentiable on the whole domain $V_{DS} \ge 0$, and its first derivatives are Lipschitz continuous on bounded sets. *Proof.* Inside each region $I_D$ is a polynomial in $(V_{GS}, V_{DS})$. At $V_{DS} = V_{ov} > 0$ the linear formula gives $k (V_{ov}/2) V_{ov}(1 + \lambda V_{ov}) = \tfrac{k}{2} V_{ov}^2 (1 + \lambda V_{ov})$, the saturation value. Its $V_{DS}$ derivative there is $k \cdot 0 \cdot (1 + \lambda V_{ov}) + k\lambda \tfrac12 V_{ov}^2 = \tfrac{k}{2}\lambda V_{ov}^2$, the saturation value, and its $V_{GS}$ derivative $k V_{ov}(1 + \lambda V_{ov})$ also agrees. At the cutoff boundary $V_{ov} = 0$ the saturation current and both its derivatives are 0, as in cutoff. So the first derivatives are continuous, and on each region they are polynomials whose own derivatives are bounded on bounded sets. Along any segment in a bounded convex set, a first derivative is then a continuous function made of finitely many pieces, each with a bounded slope, so it is Lipschitz with the largest of these bounds. With $\gamma > 0$ the same holds on bounded sets with $\Phi - V_{BS}$ bounded away from 0, where $V_T$ is a smooth function of $V_{BS}$. The second derivative $\partial^2 I_D / \partial V_{GS}^2$ jumps from 0 to $k(1 + \lambda V_{DS})$ at threshold, so the model is not twice differentiable. $\square$ A Lipschitz Jacobian is the hypothesis of the local convergence theory of [Newton's method](/newton-method-for-systems/), so the [Kantorovich theorem](/kantorovich-theorem/) applies to circuits of these devices. If $\lambda$ multiplies only the saturation formula, $I_D$ is discontinuous and that theory does not apply.

**Square-law relations in saturation.** Let $\lambda = 0$. Then $g_m = k V_{ov} = \sqrt{2 k I_D} = 2 I_D / V_{ov}$. With $\lambda > 0$, $g_{ds} = \lambda I_D / (1 + \lambda V_{DS})$, and the intrinsic gain is $g_m / g_{ds} = 2(1 + \lambda V_{DS})/(\lambda V_{ov})$. In the example above, at $V_{DS} = 5$ V, $g_m = 220\ \mu$S and $g_{ds} = 4\ \mu$S, a gain of 55.

**Switching threshold of a CMOS inverter.** Let an n-channel device with $k_n$ and $V_{Tn} > 0$ and a p-channel device with $k_p$ and threshold $-|V_{Tp}|$ form an inverter with supply $V_{DD}$, and let $\lambda = 0$. At the switching threshold $V_M$, where input and output are equal, both devices are saturated and carry the same current:

$$\tfrac{k_n}{2} (V_M - V_{Tn})^2 = \tfrac{k_p}{2} (V_{DD} - V_M - |V_{Tp}|)^2.$$

Both bases are positive, so $\sqrt{k_n}(V_M - V_{Tn}) = \sqrt{k_p}(V_{DD} - V_M - |V_{Tp}|)$, and with $r = \sqrt{k_p/k_n}$,

$$V_M = \frac{V_{Tn} + r\,(V_{DD} - |V_{Tp}|)}{1 + r}.$$

A symmetric inverter, $k_p = k_n$ and $V_{Tn} = |V_{Tp}|$, switches at $V_{DD}/2$.

**Discharge time.** Let an n-channel device with $\lambda = 0$ discharge a load $C_L$ from $V_{DD}$, with its gate stepped to $V_{DD}$ at time 0, and let $V_T < V_{DD}/2$ and $V_{ov} = V_{DD} - V_T$. The output falls to $V_{DD}/2$ at

$$t_{pHL} = \frac{C_L}{k V_{ov}} \left( \frac{2 V_T}{V_{ov}} + \ln\!\left(3 - \frac{4 V_T}{V_{DD}}\right) \right).$$

*Proof.* While $V_{out} \ge V_{ov}$ the device is saturated and the current is the constant $\tfrac{k}{2}V_{ov}^2$, so the output falls by $V_T$ in time $2 C_L V_T / (k V_{ov}^2)$. Below $V_{ov}$ the device is linear, and $C_L\, dV/dt = -k(V_{ov} - V/2) V$. Partial fractions give $\int dV / ((V_{ov} - V/2)V) = \tfrac{1}{V_{ov}} \ln \tfrac{V}{V_{ov} - V/2}$, so the time from $V_{ov}$ to $V_{DD}/2$ is $\tfrac{C_L}{k V_{ov}} \big(\ln 2 - \ln \tfrac{V_{DD}/2}{V_{ov} - V_{DD}/4}\big) = \tfrac{C_L}{k V_{ov}} \ln \tfrac{4V_{ov} - V_{DD}}{V_{DD}}$, and $4V_{ov} - V_{DD} = 3V_{DD} - 4V_T$. $\square$ For $C_L = 100$ fF, $k = 100\ \mu\text{A/V}^2$, $V_{DD} = 5$ V and $V_T = 1$ V this gives $2.5 \times 10^{-10} (0.5 + \ln 2.2) \approx 322$ ps.

## References
