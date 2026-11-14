---
tag: BEHABS
kind: problem
slug: analog-circuit-sizing
name: Analog circuit sizing
aliases:
- analog device sizing
- analog circuit synthesis
area: eda/fpga-analog-and-emerging-technologies
level: core
summary: Choose transistor widths, lengths, biases and passive values of a fixed analog topology so that gain, bandwidth, noise and power meet their specifications.
prereqs: [shichman-hodges-model, dc-operating-point-analysis, ac-small-signal-analysis, multi-objective-optimization]
see_also: [annealing-analog-sizing, geometric-programming-circuit-sizing, gate-sizing, pelgrom-mismatch-model, analog-symmetry-constraint, global-optimization, pareto-optimality, quadratic-programming]
sources:
  - paper: doi:10.1109/5.899053
    title: Georges G. E. Gielen and Rob A. Rutenbar, Computer-aided design of analog and mixed-signal integrated circuits, Proceedings of the IEEE 88(12), 1825 to 1854, 2000
    locator: the section on analog circuit sizing (the problem, the equation-based and simulation-based approaches, and the tools of each kind)
  - paper: doi:10.1109/43.489099
    title: Emil S. Ochotta, Rob A. Rutenbar and L. Richard Carley, Synthesis of high-performance analog circuits in ASTRX/OBLX, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 15(3), 273 to 294, 1996
    locator: the statement of sizing as the optimization of a cost over device sizes and node voltages, with specifications as penalties
  - paper: "Maria del Mar Hershenson, Stephen P. Boyd and Thomas H. Lee, Optimal design of a CMOS op-amp via geometric programming, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 20(1), 1 to 21, 2001"
    title: M. del Mar Hershenson, S. P. Boyd and T. H. Lee, Optimal design of a CMOS op-amp via geometric programming, IEEE TCAD 20(1), 1 to 21, 2001
    locator: the statement of op-amp sizing as a constrained optimization problem, with specifications as posynomial bounds
  - paper: doi:10.1109/JSSC.2005.848021
    title: Peter R. Kinget, Device mismatch and tradeoffs in the design of analog circuits, IEEE Journal of Solid-State Circuits 40(6), 1212 to 1224, 2005
    locator: the minimum area and power that a given accuracy and bandwidth need
---

Analog circuit sizing is the problem of choosing the transistor widths and lengths, the bias currents and voltages, and the resistor and capacitor values of an analog circuit whose topology is fixed, so that its performance meets a list of specifications, at the least power or area. Its topic is analog sizing and layout, one of the five topics of this sub-area. The performance of a design is not a formula of the sizes but the result of an analysis of the circuit, with device models whose constants are fitted to a process, so the problem is a nonlinear, in general nonconvex, optimization problem over a model of the circuit. This page states the problem; [annealing-based sizing](/annealing-analog-sizing/) and [geometric programming sizing](/geometric-programming-circuit-sizing/) are two ways to solve it.

## In plain words

An analog designer first picks a circuit: which transistors, and how they are wired. Then every transistor needs a width and a length, every branch a current, and every capacitor a value. These numbers decide how much the circuit amplifies, how fast it is, how noisy it is, and how much power it burns.

Sizing is the job of picking those numbers. The targets pull against each other: more current gives more speed but burns more power, and longer transistors give more gain but are slower. Some lists of targets cannot all be met by any choice of numbers, and then the answer is that no design exists.

The numbers are judged by a model of the transistors, not by the real chip, so even the best answer must be checked again.

## Definition

**Input.**

- A topology: a netlist of devices and nodes, with supplies and a load.
- The design variables $x \in D \subseteq \mathbb{R}^n_{>0}$: the width $W_k$ and length $L_k$ of each transistor, the bias currents, and the passive values. $D$ holds the process limits ($L_k \ge L_{\min}$, $W_k \ge W_{\min}$, a grid if the sizes are discrete) and the equalities that the topology asks for, such as $W_1 = W_2$ for a differential pair.
- The device models with their fitted parameters $\theta$: for the [square-law model](/shichman-hodges-model/) these are $k' = \mu C_{ox}$, $V_{T0}$, $\gamma$, $\Phi$ and $\lambda$; for a full model there are many more.
- The performance functions $p_1(x), \ldots, p_m(x)$, each defined by an analysis of the circuit at $x$ with the models: the [DC operating point](/dc-operating-point-analysis/) for the bias and the swing, [small-signal AC analysis](/ac-small-signal-analysis/) for the gain, the bandwidth and the phase margin, [noise analysis](/circuit-noise-analysis/), and transient analysis for the slew rate and the settling time.
- The specifications $p_i(x) \ge t_i$ for $i \in S$ (an upper bound is written with $-p_i$), and an objective $f(x)$, such as the supply current or the area.

**Output.** A point $x^* \in D$ with $p_i(x^*) \ge t_i$ for all $i \in S$ and $f(x^*) \le f(x)$ for every such $x$; or the answer that no point of $D$ meets the specifications.

**Legal points.** The performance functions are defined through the circuit equations, so a point is legal only if the analysis has the intended solution there. A DC operating point can fail to exist or can be one of several; the problem fixes the intended one by region constraints, such as every transistor in saturation with an overdrive $V_{GS} - V_T \ge V_{\min}$ and $V_{DS} \ge V_{GS} - V_T$. These constraints are part of $S$.

**What the optimum means.** The output is an optimum of the model $p(x; \theta)$. A chip built at $x^*$ has the performance of the real devices, which differ from the model and from each other. So the problem is always paired with a check by simulation with the full models, at the process corners, and with mismatch.

## Variants

- **Multi-objective.** Two or more objectives, such as power and bandwidth. The answer is the set of [Pareto-optimal](/pareto-optimality/) designs, the tradeoff curve of the topology. See [multi-objective optimization](/multi-objective-optimization/).
- **Feasibility only.** Find any $x$ that meets the specifications, with no objective.
- **Worst-case sizing.** Meet each specification for every $\theta$ in a set of process corners and for every supply voltage and temperature in a range.
- **Yield-aware sizing.** The parameters $\theta$ vary from die to die and from device to device, with a mismatch model such as the [Pelgrom model](/pelgrom-mismatch-model/). Maximize the probability that all specifications hold, or meet them with that probability at least $1 - \epsilon$.
- **Discrete sizes.** $D$ is a grid, for example a width in steps of the layout grid or a whole number of unit transistors.
- **With layout effects.** The parasitic capacitances of the layout depend on the sizes and the placement, so the specifications are checked with layout parasitics, and the sizing is redone after layout.

**How it differs from its two sizers.** The problem fixes the input, the output and what counts as legal. [Annealing-based sizing](/annealing-analog-sizing/) is a heuristic for it: it replaces the hard specifications by penalties, evaluates the performance functions with a fast analysis, and returns a good point with no bound on its distance from the optimum. [Geometric programming sizing](/geometric-programming-circuit-sizing/) solves a restricted form of it: when every performance function is replaced by a posynomial or monomial model, it finds the global optimum of that model, or proves that the model has no feasible point. Neither gives the optimum of the real circuit.

## Examples

**A gain stage, by hand.** A common-source stage with an ideal current-source load drives $C_0 = 1$ pF. Use the square-law model, with $k' = 200$ µA/V² and $\lambda = \lambda_0 / L$ with $\lambda_0 = 0.1$ µm/V, both fitted to a process. The variables are $W$, $L$ and the current $I$. The specifications are a gain-bandwidth $g_m / (2\pi C_L) \ge 10$ MHz with $C_L = C_0 + c W L$ and $c = 5$ fF/µm², a gain $g_m / (\lambda I) \ge 100$, and an overdrive $V_{ov} \ge 0.15$ V. The objective is $I$.

- Since $g_m = 2 I / V_{ov}$ in this model, the bandwidth needs $I \ge \pi \cdot 10\text{ MHz} \cdot V_{ov} C_L \ge \pi \cdot 10^7 \cdot 0.15 \cdot 10^{-12}$ A, so $I \ge 4.712$ µA for every design. This is a lower bound on the optimum.
- The gain is $2 L / (\lambda_0 V_{ov})$, so with $V_{ov} = 0.15$ V the gain needs $L \ge 0.75$ µm. At $L = 0.75$ µm the bandwidth bound with the gate capacitance gives $I \approx 4.740$ µA and $W \approx 1.58$ µm, which is the optimum of this model ([geometric programming sizing](/geometric-programming-circuit-sizing/) proves it is global). It is 0.6 percent above the lower bound; the gap is the gate capacitance $c W L$.

**An infeasible list.** Add $L \le 0.6$ µm to the same stage. The gain is $2 L / (\lambda_0 V_{ov}) \le 2 \cdot 0.6 / (0.1 \cdot 0.15) = 80$ for every legal design, so no design has a gain of 100. The answer is that no point meets the specifications. Lowering the overdrive bound would raise the gain on paper, but it moves the transistor toward weak inversion, where the square-law model no longer holds.

**A matching specification.** A current mirror with an overdrive of 0.2 V must copy its current with a spread $\sigma(\Delta I / I) \le 1$ percent. With the [Pelgrom model](/pelgrom-mismatch-model/) and the threshold term alone, $\sigma(\Delta I / I) = 2 \sigma(\Delta V_T) / V_{ov}$, so $\sigma(\Delta V_T) \le 1$ mV. With an assumed $A_{VT} = 5$ mV µm, a fitted value chosen here for the example, the gate area must be $W L \ge (5 / 1)^2 = 25$ µm² for each device.

## Known algorithms

- **[Annealing-based sizing](/annealing-analog-sizing/)** (Ochotta, Rutenbar and Carley, ASTRX/OBLX, 1996). Simulated annealing over the sizes, with a penalty cost and AWE for the performance. Heuristic: it returns a point that is never better than the optimum, with no bound on the gap.
- **[Geometric programming sizing](/geometric-programming-circuit-sizing/)** (Hershenson, Boyd and Lee, 2001). The specifications are written as posynomial bounds, and an interior-point method solves the convex form. Exact for the posynomial model, to a set accuracy in polynomial time; not exact for the circuit.
- **Equation-based local optimization.** Hand-derived design equations, solved by a gradient or Newton method with constraints. Each run finds a local optimum of the equations; with nonconvex equations it can miss the global one. The survey of Gielen and Rutenbar describes the tools of this kind.
- **Knowledge-based design plans.** A fixed sequence of design steps, written by an expert for one topology. Fast, with no optimality guarantee, and only for the topologies that have a plan.
- **Simulation in the loop.** Any search, local or global, that calls a full circuit simulator for each candidate. The most accurate performance, at the highest cost per candidate.

## Bounds

- **Hardness.** This page knows of no hardness theorem for analog sizing as such. The general problem class, a nonconvex nonlinear program, contains NP-hard problems: [quadratic programming](/quadratic-programming/) with an indefinite matrix is already NP-hard. So no method is known that finds the global optimum of every sizing problem under every device model in polynomial time, and the methods above either restrict the model or give up the guarantee.
- **Convex restrictions.** When every performance function is a posynomial or monomial of the sizes, the problem is a [geometric program](/geometric-programming/), which is convex after the change of variables $x = e^u$ and solvable to accuracy $\epsilon$ in time polynomial in its size and $\log(1/\epsilon)$ by an [interior-point method](/interior-point-method/).
- **Lower bounds from the device.** For a square-law transistor, $g_m / I = 2 / V_{ov}$, so a bandwidth $\omega$ into a load $C$ costs $I \ge \omega C V_{ov} / 2$, as in the example. Such bounds hold for every design of the model and show how far a design is from the limit of the topology.
- **Accuracy costs power.** Kinget shows that the area that a matching accuracy needs (the Pelgrom bound $W L \ge A_{VT}^2 / \sigma^2$) sets a gate capacitance, and with it a minimum power for a given speed and accuracy. No sizing can beat this bound in that model.

## Reductions

- **To a geometric program.** Under the square-law model with the overdrive as a variable, gain, bandwidth, overdrive and area are monomials or posynomials of $W$, $L$ and $I$. The example above is then a geometric program in three variables; the [geometric programming sizing](/geometric-programming-circuit-sizing/) page solves it.
- **To unconstrained minimization.** A cost $f(x) + \sum_i w_i \max(0, (t_i - p_i(x)) / t_i)$ turns the problem into one without constraints. On a finite grid, large enough weights make the minima of the cost exactly the optima of the problem; this is proved on the [annealing-based sizing](/annealing-analog-sizing/) page.
- **Relaxed DC.** Make the node voltages extra variables and the DC equations of [modified nodal analysis](/modified-nodal-analysis/) extra equality constraints. Then the performance functions are explicit in $(x, v)$, and no DC solve is needed inside the search.
- **Digital gate sizing.** [Gate sizing](/gate-sizing/) is the same problem for logic gates, with delay in place of the analog specifications. Under the RC delay model it is a geometric program too.

## Applications

Sizing is done for every analog block of a chip: operational and transconductance amplifiers, comparators, the stages of data converters, filters, oscillators, low-noise amplifiers and bias circuits. It comes after the choice of topology and before layout. The layout then has its own constraints, such as [mirror symmetry](/analog-symmetry-constraint/) and [common-centroid placement](/common-centroid-layout/) of matched devices, and its parasitics send the design back to sizing. When the circuit is moved to a new process, the topology often stays and only the sizing is redone.

## References
