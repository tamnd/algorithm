---
tag: KGQWGK
kind: problem
slug: cutting-parameter-optimization
name: Cutting parameter optimization
aliases:
- machining economics problem
- optimal cutting conditions
area: cad/manufacturing-process-planning
level: core
summary: Choose cutting speed, feed and depth that minimise cost or time per part under limits on power, force, surface finish and tool life.
prereqs: [taylor-tool-life-equation]
see_also: [geometric-programming, kkt-conditions, interior-point-method, golden-section-search, mixed-integer-programming, genetic-algorithm, computer-aided-process-planning, feedrate-scheduling]
sources:
  - book: isbn:9780133128741
    title: Serope Kalpakjian and Steven R. Schmid, Manufacturing Engineering and Technology, 7th edition, Pearson, 2014
    locator: Section 21.5 (the Taylor equation and its extended form), Section 21.3 (cutting forces and power, specific energy), Section 25.8 (machining economics)
  - paper: "W. W. Gilbert, Economics of machining, in Machining: Theory and Practice, American Society for Metals, Cleveland, 1950, 465 to 485"
    locator: the unconstrained single-pass problem, with the cutting speed as the only variable
  - paper: doi:10.1115/1.3428044
    title: D. S. Ermer, Optimization of the constrained machining economics problem by geometric programming, Journal of Engineering for Industry 93(4), 1971, 1067 to 1072
    locator: the single-pass problem with inequality constraints, solved as a geometric program
  - paper: doi:10.1115/1.3184513
    title: D. S. Ermer and S. Kromodihardjo, Optimization of multipass turning with constraints, Journal of Engineering for Industry 103(4), 1981, 462 to 468
    locator: the multi-pass turning problem, with the split of the total depth into passes as a variable
---

Cutting parameter optimization chooses the cutting speed, the feed and the depth of cut of a machining operation so that the cost or the time per part is as small as possible. The choice must respect the limits of the machine, the tool and the part: spindle power, cutting force, surface finish, tool life and the ranges of the machine. The tool life comes from the [Taylor tool life equation](/taylor-tool-life-equation/), which links the speed to the wear of the tool. With speed as the only variable and no constraint, the problem has a closed-form answer. With constraints and several passes, it is a small nonlinear program that planners solve with numerical methods. This page states the problem and works an example with an active constraint.

## In plain words

A faster cut takes less time, but the tool wears out sooner, and each new tool costs money and time to change. A slower cut saves tools but keeps the machine busy longer. Somewhere between them is the cheapest speed. The feed, which is how far the tool moves per turn of the part, matters too: a larger feed removes metal faster but leaves a rougher surface and needs more force. The machine has a power limit, the tool has a force limit, and the drawing gives a limit on roughness. The task is to pick the speed, the feed and the depth that give the lowest cost per part and stay inside all these limits. There is no single standard formal statement of this task.

## Definition

There is no standard formal statement of cutting parameter optimization. The following version for single-pass turning is the one that most of the cited work uses, with models that differ in detail.

**Input.**
- The part and the cut: diameter $D$, length $L$, and depth of cut $d$ (fixed in the single-pass version).
- The extended Taylor law $V T^n f^a d^b = C'$ with constants $n, a, b, C'$.
- Costs: $C_o$ per minute of machine and operator, $C_t$ per tool edge, $t_c$ minutes per tool change, and a handling time $t_h$ per part.
- Limits: speed range $[V_{\min}, V_{\max}]$, feed range $[f_{\min}, f_{\max}]$, spindle power $P_{\max}$, cutting force $F_{\max}$, surface roughness $R_{\max}$, and a smallest tool life $T_{\min}$.
- Process models: the cutting force $F_c(f, d)$, the power $P = F_c V$, and the roughness $R(f)$.

**Variables.** The cutting speed $V$ and the feed $f$ per turn.

**Objective.** The machining time is $t_m = \pi D L / (V f)$, the tool life is $T(V, f) = (C' / (V f^a d^b))^{1/n}$, and the cost per part is

$$c(V, f) = C_o\,(t_h + t_m) + \frac{t_m}{T(V, f)}\,(C_o t_c + C_t).$$

The time per part is the same expression with $C_o = 1$ and $C_t = 0$.

**Constraints.**

$$V_{\min} \le V \le V_{\max}, \quad f_{\min} \le f \le f_{\max}, \quad F_c(f, d) \le F_{\max}, \quad F_c(f, d)\,V \le P_{\max}, \quad R(f) \le R_{\max}, \quad T(V, f) \ge T_{\min}.$$

Common process models are a power law $F_c = k\, f^{\alpha} d^{\beta}$, or $F_c = u\, f d$ with the specific cutting energy $u$, and the geometric roughness of a tool with nose radius $r$. That roughness is the height of a circular arc of radius $r$ over a chord of length $f$: $R_t = r - \sqrt{r^2 - f^2/4} \approx f^2 / (8 r)$ for $f \ll r$.

## Variants

- **Objective.** Minimum cost per part, minimum time per part (maximum production rate), or maximum profit rate. The two classic speeds of the [Taylor page](/taylor-tool-life-equation/) are the minimum cost and the minimum time of the unconstrained case.
- **Single pass, speed only.** Feed and depth fixed, no constraints. This is Gilbert's problem (1950), with a closed form.
- **Single pass with constraints.** Speed and feed as variables, with the constraints above (Ermer 1971).
- **Multi-pass turning.** A total depth $d_{\text{tot}}$ is removed in $k$ roughing passes and one finishing pass. The number of passes is an integer, and the depth, speed and feed of each pass are variables (Ermer and Kromodihardjo 1981). This makes the problem a mixed integer nonlinear program.
- **Milling and multi-tool operations.** The cost includes several tools and several operations on one machine, with shared limits.
- **Stochastic tool life.** Tool life is random, so a version adds a chance constraint: the probability of a failure before the end of the cut is small.

## Examples

**No constraint.** With $n = 0.25$, $C = 397$ m/min, $t_c = 2$ min, $C_t = 5$ dollars and $C_o = 1$ dollar per min, the speed of minimum cost is $V = 185.5$ m/min, with a tool life of 21 min. The [Taylor page](/taylor-tool-life-equation/) derives it.

**An active power limit.** Use the same tool with the basic law ($a = b = 0$), a bar with $D = 80$ mm and $L = 300$ mm, and a depth $d = 2$ mm. Assume a specific cutting energy of $u = 3$ W s/mm³, so the power is $P = u \cdot V f d = 100\, V f$ watts with $V$ in m/min and $f$ in mm. The limits are $P_{\max} = 4$ kW, a nose radius $r = 0.8$ mm and $R_{\max} = 10$ µm.

- The roughness limit gives $f^2 / (8 \times 0.8) \le 0.01$, so $f \le \sqrt{0.064} = 0.2530$ mm.
- The power limit gives $V f \le 40$.
- The cost without handling is $c = \dfrac{75.40}{V f}\left(1 + 7\left(\dfrac{V}{397}\right)^4\right)$ dollars, with $\pi D L = 75.40$ m mm.

For a fixed $V$, the cost falls when $f$ grows, so the best feed is the largest allowed one, $f = \min(0.2530, 40 / V)$. For $V \le 158.1$, that is $f = 0.2530$, and the cost in $V$ falls up to 185.5 m/min, so on this part the best $V$ is 158.1. For $V \ge 158.1$, $f = 40/V$, and the cost is $1.885\,(1 + 7 (V/397)^4)$, which grows with $V$. So the answer is $V = 158.1$ m/min and $f = 0.2530$ mm, with both limits active.

| point | $V$ (m/min) | $f$ (mm) | power (kW) | tool life (min) | cost (dollars) |
|---|---|---|---|---|---|
| unconstrained speed | 185.5 | 0.25 | 4.64 | 21.0 | 2.168 |
| optimum | 158.1 | 0.2530 | 4.00 | 39.7 | 2.217 |
| $f = 0.25$ on the power limit | 160.0 | 0.25 | 4.00 | 37.9 | 2.233 |

The unconstrained speed of the Taylor page needs 4.64 kW, more than the machine has. A grid search over $V$ in steps of 0.1 m/min and $f$ in steps of 0.001 mm finds a best grid point of $(158.7, 0.252)$ with cost 2.222, next to the exact optimum. In this model the tool life does not depend on the feed, so the feed is pushed to its limit first. With $a > 0$ in the extended law, the larger feed also costs tool life, and the balance moves.

## Known algorithms

- **Closed form.** For speed only and no constraint, the minimum is at the tool life $T = (1/n - 1)(t_c + C_t / C_o)$ (Gilbert 1950).
- **One variable with bounds.** The cost in $V$ alone has one minimum, so a bound or a constraint on $V$ moves the answer to the nearest feasible speed. A [golden section search](/golden-section-search/) also finds it.
- **[Geometric programming](/geometric-programming/).** With power law models, the cost and the constraints are posynomials in $V$ and $f$, and the single-pass problem is a geometric program (Ermer 1971). After the change of variables $x = \ln V$, $y = \ln f$ it is convex, and an [interior point method](/interior-point-method/) solves it. The [KKT conditions](/kkt-conditions/) show which constraints are active.
- **Multi-pass.** Ermer and Kromodihardjo (1981) split the problem into the choice of the number of passes and the parameters of each pass. Many later papers use [genetic algorithms](/genetic-algorithm/) and [simulated annealing](/simulated-annealing/) for the multi-pass and milling versions.

There are no standard benchmark instances for this problem. Published comparisons use test problems of their own, so their numbers cannot be compared from paper to paper.

## Bounds

The single-pass problem with posynomial models is a convex program after the logarithmic change of variables, so it is solvable in polynomial time to any fixed accuracy. No hardness result is known for the multi-pass version in the cited sources. Its size in practice is small: a few passes and two or three variables per pass. The difficulty in practice is the model, not the search: the constants of the Taylor law and of the force model have large scatter, so a planner adds a margin to each limit.

## Reductions

- **To geometric programming.** Each term of $c$ is a positive constant times a product of powers of $V$ and $f$, and each constraint of the power law models is a monomial bound, such as $k f^{\alpha} d^{\beta} V \le P_{\max}$, which is $(k d^{\beta} / P_{\max})\, V f^{\alpha} \le 1$. That is the standard form of a geometric program.
- **To one variable.** When all constraints except the bounds on $V$ do not involve $V$, fix $f$ at its best value first, as in the example, and solve the one-variable problem of the Taylor page.

## Applications

- **Process planning.** A [computer-aided process planning](/computer-aided-process-planning/) system picks the cutting conditions of each operation after it picks the tool, often from a handbook table, and then adjusts them with this model.
- **CAM.** The feed and the speed of each toolpath come from the same choice, and [feedrate scheduling](/feedrate-scheduling/) then changes the feed along the path.
- **Tool and machine costs.** By the formula for $T$, a higher machine cost per minute or a cheaper tool edge gives a shorter best tool life, so a faster cut. A planner uses this to set different speeds for the same tool on different machines.

## References
