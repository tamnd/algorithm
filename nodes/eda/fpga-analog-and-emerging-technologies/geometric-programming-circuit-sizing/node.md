---
tag: 6XN9CP
kind: technique
slug: geometric-programming-circuit-sizing
name: Geometric programming circuit sizing
aliases:
- Hershenson-Boyd-Lee op-amp design
- posynomial circuit sizing
area: eda/fpga-analog-and-emerging-technologies
level: advanced
summary: Hershenson, Boyd and Lee's method that writes op-amp specifications as posynomials of device sizes, so sizing becomes a convex geometric program with a global optimum.
prereqs: [geometric-programming, analog-circuit-sizing, shichman-hodges-model, convex-optimization-problem]
see_also: [monomial, log-sum-exp-trick, interior-point-method, annealing-analog-sizing, gate-sizing, pelgrom-mismatch-model, convex-set, pareto-optimality]
sources:
  - paper: "Maria del Mar Hershenson, Stephen P. Boyd and Thomas H. Lee, Optimal design of a CMOS op-amp via geometric programming, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 20(1), 1 to 21, 2001"
    title: M. del Mar Hershenson, S. P. Boyd and T. H. Lee, Optimal design of a CMOS op-amp via geometric programming, IEEE TCAD 20(1), 1 to 21, January 2001
    locator: the two-stage op-amp, the posynomial and monomial forms of its specifications under the square-law device model, the global optimum by an interior-point method, the tradeoff curves, and the comparison with simulation
  - paper: doi:10.1007/s11081-007-9001-7
    title: Stephen Boyd, Seung-Jean Kim, Lieven Vandenberghe and Arash Hassibi, A tutorial on geometric programming, Optimization and Engineering 8(1), 67 to 127, 2007
    locator: the convex form of a geometric program, the modeling rules for posynomials, and the circuit design examples
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 4.5 (geometric programming and its convex form) and Section 4.2.2 (local optima of convex problems are global)
  - paper: "Walter Daems, Georges Gielen and Willy Sansen, Simulation-based generation of posynomial performance models for the sizing of analog integrated circuits, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 22(5), 517 to 534, 2003"
    title: W. Daems, G. Gielen and W. Sansen, Simulation-based generation of posynomial performance models for the sizing of analog integrated circuits, IEEE TCAD 22(5), 517 to 534, 2003
    locator: the fit of posynomial performance models to simulation data, so that the sizing problem becomes a geometric program
  - paper: doi:10.1109/5.899053
    title: Georges G. E. Gielen and Rob A. Rutenbar, Computer-aided design of analog and mixed-signal integrated circuits, Proceedings of the IEEE 88(12), 1825 to 1854, 2000
    locator: the section on analog circuit sizing (equation-based and simulation-based methods)
---

Geometric programming circuit sizing writes every specification of an analog circuit as a bound on a posynomial or a monomial of the device sizes and bias currents, so that sizing becomes a [geometric program](/geometric-programming/). Its topic is analog sizing and layout, one of the five topics of this sub-area. A geometric program is convex after a change of variables to logarithms, so an interior-point method finds its global optimum, or proves that no design meets the specifications. Hershenson, Boyd and Lee sized a two-stage CMOS op-amp this way in 2001. The optimum is the global optimum of the posynomial model, which is built on fitted device equations; it is not proved to be the optimum of the real circuit.

## In plain words

Sizing a circuit means choosing the widths and lengths of its transistors and its bias currents so that the circuit meets its targets: gain, speed, noise, power.

Many of these targets, written with the simple textbook formulas of a transistor, have one special form: each is a sum of terms, and each term is a positive number times a product of powers of the sizes. If every target has this form, the whole design question can be turned, by measuring every size on a log scale, into a smooth bowl-shaped problem. A bowl has one lowest point, so a solver finds the best design of the formulas, and if no design meets the targets, it says so.

The catch is the formulas. They are fitted approximations of real transistors, so the best design of the formulas must still be checked by a full simulation.

## When it applies

- The topology is fixed, and the unknowns are positive: widths, lengths, currents, capacitor values, bias voltages above a threshold.
- Each specification can be written, after rearranging, as $f(x) \le 1$ with $f$ a posynomial, or $g(x) = 1$ with $g$ a [monomial](/monomial/) in the sense of the geometric programming page (a positive constant times a product of real powers). A lower bound is allowed only on a monomial: $g(x) \ge b$ becomes $b / g(x) \le 1$.
- The objective is a posynomial to minimize, such as power, area or a weighted sum of them, or a monomial to maximize, such as the bandwidth.
- The device equations are monomials or posynomials. With the [square-law model](/shichman-hodges-model/) in saturation, the transconductance $g_m = \sqrt{2 k' (W/L) I}$, the overdrive $V_{ov} = \sqrt{2 I L / (k' W)}$, the output conductance $g_{ds} = \lambda I$ with $\lambda = \lambda_0 / L$, and the gate capacitance $C_{ox} W L$ are all monomials.

## The template

1. Choose the variables $x \in \mathbb{R}^n_{>0}$: the $W$ and $L$ of each transistor (with monomial equations $W_1 = W_2$ for matched devices), the bias currents, and the compensation capacitor.
2. Write each device quantity with the fitted device model, as a monomial or a posynomial of $x$.
3. Write each specification as a posynomial upper bound or a monomial equation. For example, a gain $A \ge A_0$ with $A$ a monomial becomes $A_0 / A \le 1$. A bandwidth $g_m / C \ge \omega_0$, with a posynomial capacitance $C$, becomes $\omega_0 C / g_m \le 1$, which is a posynomial divided by a monomial, so a posynomial.
4. Add the constraints that keep every device in the region where its model holds, such as $V_{ov} \ge V_{\min}$ for saturation, and the limits of the process, such as $L \ge L_{\min}$.
5. Solve the geometric program with an interior-point method in the variables $u = \log x$.
6. Check the result by circuit simulation with the full device models, and adjust the fitted constants or the margins if the two disagree.

**Theorem (the optimum is global for the model).** Let the problem of steps 1 to 4 have a feasible point. Every local minimum of it is a global minimum of the posynomial model.

*Proof.* Put $x = e^u$, componentwise. This is a bijection from $\mathbb{R}^n$ onto $\mathbb{R}^n_{>0}$, and a continuous one in both directions, so local and global minima correspond. A posynomial $f(x) = \sum_k c_k x^{a_k}$ becomes $\sum_k e^{a_k^\top u + \log c_k}$, and $\log f(e^u)$ is the log-sum-exp function of an affine map of $u$, which is convex (see the [log-sum-exp trick](/log-sum-exp-trick/)). A constraint $f(x) \le 1$ becomes $\log f(e^u) \le 0$, a sublevel set of a convex function, so a [convex set](/convex-set/). A monomial equation $g(x) = 1$ becomes $a^\top u + \log c = 0$, an affine set. Minimizing $f_0$ is the same as minimizing the convex function $\log f_0(e^u)$. So the problem in $u$ is a [convex optimization problem](/convex-optimization-problem/). Let $u^*$ be a local minimum, and suppose a feasible $v$ has a smaller objective $\phi(v) < \phi(u^*)$. The points $u^* + t(v - u^*)$, $0 < t \le 1$, are feasible, because the feasible set is convex, and $\phi(u^* + t(v - u^*)) \le (1 - t)\phi(u^*) + t \phi(v) < \phi(u^*)$, because $\phi$ is convex. For small $t$ these points are as close to $u^*$ as we like, which contradicts local minimality. $\square$

What the theorem does not say. The device equations of step 2 are fitted: the square law with its constants $k' = \mu C_{ox}$, $V_{T0}$ and $\lambda_0$, or a posynomial fitted to simulation data. The theorem says nothing about the distance between the posynomial model and the circuit. That distance is measured, by simulation of the result, and it is the main source of error of the method.

## Classic examples

**A single-transistor gain stage.** Size a common-source stage with a load $C_0 = 1$ pF so that its gain-bandwidth $g_m / (2 \pi C_L)$ is at least 10 MHz and its gain $g_m / g_{ds}$ is at least 100, with the least bias current $I$. The variables are $W$, $L$ and $I$. The load is $C_L = C_0 + c W L$, a posynomial. The constants:

| constant | value | where it comes from |
|---|---|---|
| $k' = \mu C_{ox}$ | 200 µA/V² | fitted to the process |
| $\lambda_0$ in $\lambda = \lambda_0 / L$ | 0.1 µm/V | fitted to the process |
| $c$, the gate capacitance per area | 5 fF/µm² | a process value |
| $C_0$, $\omega_0 = 2\pi \cdot 10$ MHz, $A_0 = 100$ | | the specifications |
| $V_{\min} = 0.15$ V, $L_{\min} = 0.5$ µm | | a design margin and a process limit |

The program is: minimize $I$ subject to $\omega_0 (C_0 + c W L) / g_m \le 1$, $A_0 \lambda_0 I / (g_m L) \le 1$, $V_{\min} / V_{ov} \le 1$ and $L_{\min} / L \le 1$. A numerical solution gives $V_{ov} = 0.15$ V, $L = 0.75$ µm, $W \approx 1.58$ µm and $I \approx 4.74$ µA. The gain $2L / (\lambda_0 V_{ov})$ is exactly 100, so the gain sets $L$, above the minimum length. The bandwidth is exactly 10 MHz. A lower overdrive would give more $g_m$ per unit of current, so the overdrive bound is tight too.

**What the model does outside its region.** Drop the bound $V_{ov} \ge V_{\min}$. The same program then has its optimum near $I \approx 50$ nA with $V_{ov} \approx 0.9$ mV and $W \approx 317$ µm. This is the global optimum of the model, but the square law does not hold at such a small overdrive: the transistor is in weak inversion, where its $g_m$ is far below the square-law value. The real stage would miss the bandwidth. Step 4 is not optional.

**The two-stage op-amp.** Hershenson, Boyd and Lee size the classic two-stage CMOS op-amp with a Miller capacitor. The variables are the widths and lengths of the transistors, the bias current and the compensation capacitor. They write the gain, the unity-gain bandwidth, the phase margin (with an approximation that makes it a posynomial bound), the slew rate, the common-mode range, the output swing, the noise, the power and the area as posynomial bounds or monomial equations. The geometric program is small, and an interior-point method solves it fast enough to solve it many times. Because each solve gives the global optimum, they trace optimal tradeoff curves, such as the best bandwidth for each power, which show the best that the topology can do under the model.

## Variations

- **Fitted posynomial models.** Daems, Gielen and Sansen fit posynomials to the simulated performance of a circuit, instead of writing the equations by hand. This lowers the model error, but the fit is still an approximation, with its own error that must be measured.
- **Digital gate sizing.** The delay of a gate under an RC model is a posynomial of the gate sizes, so [gate sizing](/gate-sizing/) with continuous sizes is also a geometric program.
- **Robust design.** Ranges or ellipsoids of the fitted constants can be added as robust constraints, so that the design meets its specifications for every value in the set.
- **Non-posynomial specifications.** A specification that is not a posynomial bound can be approximated by one, or handled by a sequence of geometric programs that each replace it by a local monomial fit. Each subproblem is solved globally, but the sequence is a local method.
- **Tradeoff curves.** Fix one specification at a series of values and solve each geometric program, to trace a [Pareto](/pareto-optimality/) curve of the model.
- **Matching.** A minimum area $W L \ge A_{VT}^2 / \sigma_0^2$ from the [Pelgrom model](/pelgrom-mismatch-model/) is a monomial bound, so offset targets fit the method.

## Pitfalls

- **Reading the optimum as the optimum of the circuit.** The global optimum is a property of the posynomial model. A design that is optimal for the model can miss a specification in simulation, and a better circuit design may exist that the model ranks lower.
- **Leaving the region of the model.** Without bounds such as $V_{ov} \ge V_{\min}$ and $V_{DS} \ge V_{ov}$, the solver moves into regions where the fitted equations are wrong, as in the example above.
- **Lower bounds on posynomials.** A constraint $f(x) \ge 1$ with a posynomial $f$ of more than one term is not convex after the change of variables. For example $x_1 + x_2 \ge 1$ becomes $e^{u_1} + e^{u_2} \ge 1$, whose feasible set is not convex. Such a specification must be rewritten, approximated, or left out.
- **Differences of terms.** A quantity such as $V_{DD} - V_{ov}$ is not a posynomial. Bounds on it need a rewrite, for example $V_{ov} + V_{\text{margin}} \le V_{DD}$, which is a posynomial upper bound.
- **Fitted constants.** $k'$, $\lambda_0$ and the threshold differ between process corners and drift with the bias. A design sized at one set of constants can fail at another. Use the worst corner, or robust constraints.

## Exercises

1. Show that the gain $A = g_m / g_{ds}$ of the example is the monomial $2 L / (\lambda_0 V_{ov})$, and that it equals $\sqrt{2 k' W L / I} / \lambda_0$.
2. Show that $\omega_0 (C_0 + c W L) / g_m \le 1$ is a posynomial bound, and write it in the variables $u = \log x$ as a log-sum-exp bound.
3. In the example, explain without a solver why the bound $V_{ov} \ge V_{\min}$ must be tight at the optimum. Then find $L$ from the gain bound, and $I$ from the bandwidth bound, and check the values above.
4. Show that the set $\{u : e^{u_1} + e^{u_2} \ge 1\}$ is not convex, by finding two points in it whose midpoint is not.
5. Add the area $W L \le 1\ \mu\text{m}^2$ to the example. Is the program still feasible? Which bound is then the most costly?

## References
