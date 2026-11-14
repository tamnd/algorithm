---
tag: A4H89F
kind: algorithm
slug: annealing-analog-sizing
name: Annealing-based analog sizing
aliases:
- ASTRX/OBLX
- simulation-based analog synthesis
area: eda/fpga-analog-and-emerging-technologies
level: advanced
summary: Ochotta, Rutenbar and Carley's sizing that evaluates candidate circuits by fast AWE-based analysis and searches device sizes by simulated annealing.
solves: [analog-circuit-sizing]
model: real-ram
complexity:
  vars: {K: the number of temperatures, m: the number of moves per temperature, E: the time of one performance evaluation, d: the number of variables}
  time: {worst: O(K m (E + d))}
  space: {extra: O(d)}
properties: {deterministic: false, randomized: true, exact: false, iterative: true, anytime: true}
history:
  year: 1996
  people: [Emil S. Ochotta, Rob A. Rutenbar, L. Richard Carley]
  note: Ochotta, Rutenbar and Carley described ASTRX/OBLX at DAC in 1994 and in full in IEEE Transactions on CAD in 1996. It joined AWE for the performance of each candidate with simulated annealing over the sizes.
prereqs: [analog-circuit-sizing, simulated-annealing, asymptotic-waveform-evaluation, metropolis-criterion]
see_also: [geometric-programming-circuit-sizing, simulated-annealing-convergence, simulated-annealing-placement, shichman-hodges-model, modified-nodal-analysis, global-optimization, pelgrom-mismatch-model, local-search]
sources:
  - paper: doi:10.1109/43.489099
    title: Emil S. Ochotta, Rob A. Rutenbar and L. Richard Carley, Synthesis of high-performance analog circuits in ASTRX/OBLX, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 15(3), 273 to 294, 1996
    locator: the compilation of a circuit and its specifications into a cost function (ASTRX), the evaluation of each candidate by AWE, the relaxed-dc formulation, and the annealing search (OBLX)
  - paper: "Emil S. Ochotta, Rob A. Rutenbar and L. Richard Carley, ASTRX/OBLX: tools for rapid synthesis of high-performance analog circuits, Proceedings of the 31st Design Automation Conference, 24 to 30, 1994"
    title: E. S. Ochotta, R. A. Rutenbar and L. R. Carley, ASTRX/OBLX, tools for rapid synthesis of high-performance analog circuits, DAC 1994, 24 to 30
    locator: the conference version of the method
  - paper: doi:10.1109/43.45867
    title: Lawrence T. Pillage and Ronald A. Rohrer, Asymptotic waveform evaluation for timing analysis, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 9(4), 352 to 366, 1990
    locator: the moment matching by a Pade approximation that ASTRX/OBLX uses to evaluate the linear behavior of a candidate
  - paper: doi:10.1109/5.899053
    title: Georges G. E. Gielen and Rob A. Rutenbar, Computer-aided design of analog and mixed-signal integrated circuits, Proceedings of the IEEE 88(12), 1825 to 1854, 2000
    locator: the section on analog circuit sizing, with equation-based and simulation-based methods and the place of ASTRX/OBLX among them
---

Annealing-based analog sizing chooses the device sizes and biases of a fixed analog circuit by [simulated annealing](/simulated-annealing/): it scores each candidate by a cost that adds the objective and weighted penalties for the missed specifications, and it evaluates each candidate by a fast analysis instead of by hand-written design equations. Its topic is analog sizing and layout, one of the five topics of this sub-area. Ochotta, Rutenbar and Carley built it as ASTRX/OBLX in 1994 to 1996: ASTRX compiles the circuit and its specifications into a cost function, and OBLX anneals it, with [asymptotic waveform evaluation](/asymptotic-waveform-evaluation/) (AWE) for the linear behavior of each candidate. It is a heuristic: no bound on how far its result is from the best design is known.

## In plain words

To size a circuit by search, you need two things: a way to score a design, and a way to choose which design to try next.

The score adds up how much power or area the design uses and how badly it misses each target, with a large weight on the misses. A design that meets every target pays only for its power and area.

The search starts from a random design and keeps changing one size at a time. A change that lowers the score is kept. A change that raises it is sometimes kept too, more often early on and less often later, so that the search can climb out of a poor valley before it settles. The best design seen is the answer.

Each score needs an analysis of the circuit. ASTRX/OBLX made that analysis fast enough to run tens of thousands of times.

## The problem

The input is a circuit of fixed topology with $d$ unknowns $x = (x_1, \ldots, x_d)$ (widths, lengths, bias currents, capacitor values), each on a grid of allowed values, an evaluator that gives the performance vector $p(x)$, the specifications $p_i(x) \ge t_i$ (an upper bound is written the same way with $-p_i$), and an objective $f(x) \ge 0$ such as power or area. The output is a point $x$ that meets the specifications with a small $f$. This is the [analog circuit sizing](/analog-circuit-sizing/) problem with a penalty in place of the hard constraints:

$$C(x) = f(x) + \sum_i w_i \max\Big(0, \frac{t_i - p_i(x)}{t_i}\Big).$$

## The algorithm

ASTRX reads the circuit, the device models and the specifications, and writes the cost function. OBLX runs the annealing over it.

```pseudo id=main
ANNEAL-SIZE(grids, C, T0, α, m, T_min, rng)
L1  x ← a random point of the grids; c ← C(x); best ← x
L2  T ← T0
L3  while T > T_min
L4      repeat m times
L5          y ← x with one variable moved by a random number of grid steps, at most r(T)
L6          δ ← C(y) − c                  ▷ evaluates p(y): AWE in OBLX, a closed form here
L7          if δ ≤ 0 or rng() < exp(−δ / T) then x ← y; c ← c + δ
L8          if c < C(best) then best ← x
L9      T ← α T
L10 return best and C(best)
```

Line L7 is the [Metropolis rule](/metropolis-criterion/). Line L5 shrinks the reach $r(T)$ as the temperature falls, so the search takes long jumps early and small steps late. This rule is a simple choice of this page; OBLX has its own move set and schedule. Line L8 keeps the best point seen, which can differ from the point where the run ends.

**What ASTRX/OBLX adds to this loop.** Three ideas made the loop practical for real circuits.

- **AWE for the small-signal behavior.** A candidate's gain, bandwidth and phase margin come from its linearized circuit. AWE gives a low-order [Padé](/pade-approximation/) model of a transfer function from a few moments of the circuit, much faster than a full AC sweep with a simulator.
- **The relaxed-dc formulation.** Solving the nonlinear DC operating point for every candidate is slow. ASTRX/OBLX makes the node voltages extra variables of the search, and adds the violation of Kirchhoff's current law at each node to the cost. At the end of a good run these terms are near zero, so the circuit is biased where the search left it, without a Newton solve in the loop.
- **Real device models.** The transistors are evaluated with full device models, not with hand-derived equations, so a new circuit needs no new design equations. The models still have fitted parameters, and the result is checked by simulation.

## Example

The code of this page sizes a common-source stage with a current-source load and a 1 pF load capacitor. The unknowns are $W$ (41 values from 0.5 to 50 µm), $L$ (41 values from 0.5 to 2.5 µm) and the bias current $I$ (201 values from 1 to 100 µA). The evaluator is the [square-law model](/shichman-hodges-model/), not AWE, with $g_m = \sqrt{2 k' (W/L) I}$, $V_{ov} = \sqrt{2 I L / (k' W)}$, gain $g_m / (\lambda I)$ with $\lambda = \lambda_0 / L$, and bandwidth $g_m / (2 \pi (C_0 + c W L))$. Two constants are fitted to a process, $k' = 200$ µA/V² and $\lambda_0 = 0.1$ µm/V; the gate capacitance $c = 5$ fF/µm² is a process value. The specifications are a gain-bandwidth of at least 10 MHz, a gain of at least 100 and an overdrive of at least 0.15 V, each with weight 10. The objective is $I / (10\ \mu\text{A}) + W L / (100\ \mu\text{m}^2)$.

A run with `random.Random(0)`, $T_0 = 1$, $\alpha = 0.95$ and $m = 100$:

| step | $T$ | $W$ (µm) | $L$ (µm) | $I$ (µA) | cost $c$ | best so far |
|---|---|---|---|---|---|---|
| start | 1 | 7.924 | 1.80 | 1.259 | 9.709 | 9.709 |
| after temperature 1 | 1 | 5.000 | 1.40 | 8.128 | 0.883 | 0.677 |
| after temperature 11 | 0.599 | 6.295 | 2.50 | 4.898 | 1.349 | 0.588 |
| after temperature 61 | 0.046 | 1.991 | 1.05 | 5.370 | 0.558 | 0.509 |
| end (180 temperatures) | 0.0001 | 1.991 | 0.95 | 4.898 | 0.509 | 0.502 |

The start misses two specifications: its overdrive is 0.053 V and its bandwidth 6.99 MHz, which cost $10 \cdot 0.643 + 10 \cdot 0.300 = 9.44$, plus 0.269 for current and area. At high temperature the run accepts about half of its moves, including some that raise the cost: after temperature 11 it sits at 1.349, with the best at 0.588. It ends in a local minimum of cost 0.509, but line L8 kept a better point it passed, $W \approx 2.233$ µm, $L = 1.05$ µm, $I \approx 4.786$ µA, of cost 0.502. An exhaustive search of all $41 \cdot 41 \cdot 201$ grid points confirms that this is the least cost on the grid. It meets every specification, with a gain of 140, a bandwidth of 10.04 MHz and an overdrive of 0.150 V.

The [geometric program](/geometric-programming-circuit-sizing/) with the same model and continuous sizes needs 4.74 µA. The grid needs 4.79 µA, because $W$ and $L$ can take only grid values.

## Correctness

The proofs are in the proof file. What is proved:

- The run returns a grid point and its cost, and that cost is at most the cost of every point it visited. So it never beats an exhaustive search of the grid.
- On a finite grid, the penalty is exact when the weights are large enough: if each $w_i$ exceeds the least feasible objective divided by the least positive violation on the grid, then every point of least cost is feasible and has the least objective among the feasible points. With continuous sizes this fails, and a point of least cost can miss a specification by a little.

What is not proved: that the run finds the least cost. The [convergence theorem](/simulated-annealing-convergence/) of annealing needs a logarithmic schedule and an unbounded run; ASTRX/OBLX and the code use a fixed number of geometric steps. And the least cost is a property of the evaluator: the result is the best design for the model of the circuit, and it is checked by a full simulation.

What is measured, on the toy of the example (not a benchmark): the grid has 31 local minima under moves of one step in one variable. With the schedule above, 38 of the 40 runs with seeds 0 to 39 reached the grid optimum, and the other two ended within 0.018 in cost. With $\alpha = 0.5$ and 10 moves per temperature, none of the 40 did. Ochotta, Rutenbar and Carley report circuits sized by ASTRX/OBLX and checked by simulation; those are their measurements, on their circuits, and this page does not repeat their numbers.

## Complexity

With $K$ temperatures, $m$ moves per temperature, $d$ variables and an evaluation time $E$, a run takes $O(K m (E + d))$ time and $O(d)$ extra space beyond the evaluator. With $T$ falling from $T_0$ to $T_{\min}$ by a factor $\alpha$, $K = \lceil \log(T_{\min}/T_0) / \log \alpha \rceil$; the example has $K = 180$ and $m = 100$, so 18,000 evaluations, against 337,881 for the exhaustive search of its grid. The cost is all in $E$. For a closed-form model, $E$ is constant. For AWE, $E$ is one sparse factorization of the linearized circuit plus a few solves for the moments. A full simulation of each candidate would make $E$ much larger, which is why ASTRX/OBLX used AWE.

## Properties

- **Randomized.** The result depends on the seed. Several runs with different seeds give a spread of results; the best of them is kept.
- **Anytime.** The best point so far is always available.
- **No design equations.** A new topology needs a netlist and specifications, not a new set of equations. This is the main difference from [geometric programming sizing](/geometric-programming-circuit-sizing/), which needs every specification in posynomial form, but which proves that its optimum is global for its model.
- **Any specification.** The cost does not need to be convex or smooth, so phase margin, slew rate and noise enter as they are.

## Variants and improvements

- **Other evaluators.** Later simulation-based sizers call a full circuit simulator for each candidate, which removes the AWE approximation but costs more per evaluation.
- **Other searches.** The same cost has been searched with a [genetic algorithm](/genetic-algorithm/), with [local search](/local-search/) from many starts, and with models fitted to simulation data, as in the [response surface method](/response-surface-methodology/).
- **Yield.** Draw the device parameters from a mismatch model such as the [Pelgrom model](/pelgrom-mismatch-model/), and score a candidate by the fraction of samples that meet the specifications.
- **Hybrid with geometric programming.** Use a geometric program on fitted posynomials to find a starting point, and anneal from there against the full evaluator.

## When to use it

Use it when the specifications do not fit a convex form, or when the device models are too detailed for hand equations, and when each evaluation is cheap enough to run many thousands of times. When the specifications can be written as posynomials of the sizes, a geometric program is faster and gives the global optimum of its model, so it is the better first choice.

## Pitfalls

- **Cooling too fast.** With a fast schedule the run stops in a local minimum. On the toy of the example, $\alpha = 0.5$ with 10 moves per temperature never reached the optimum in 40 runs.
- **Weights too small.** With small penalty weights the least cost can be a design that misses a specification by a little, and the run reports it as the answer. Check the feasibility of the result, not only its cost.
- **Trusting the evaluator.** AWE and the device models are approximations, and the device models have fitted constants. Simulate the result with the full models, and at the process corners.
- **Leaving the region of the model.** A search over sizes can move a transistor out of saturation, where a small-signal model of the gain is wrong. Add specifications that keep each device in its region, as the overdrive bound of the example does.
- **Relaxed-dc residue.** With node voltages as variables, a run that stops early leaves a design whose Kirchhoff's current law residue is not zero. Solve the DC operating point of the final design and check that it is the one the search assumed.

## Implementations

## History

Earlier sizing tools, the equation-based and knowledge-based tools surveyed by Gielen and Rutenbar, used design equations derived by hand for each topology. Ochotta, Rutenbar and Carley presented ASTRX/OBLX at DAC in 1994 and in IEEE Transactions on CAD in 1996. It replaced the hand equations by a compiled cost function, evaluated with AWE (Pillage and Rohrer 1990), the relaxed-dc formulation and full device models, and searched it with simulated annealing. Hershenson, Boyd and Lee took the opposite route in 2001, with hand equations in posynomial form and a convex solver.

## References
