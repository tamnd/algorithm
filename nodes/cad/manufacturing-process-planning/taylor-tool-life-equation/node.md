---
tag: M54477
kind: model
slug: taylor-tool-life-equation
name: Taylor tool life equation
aliases:
- Taylor's tool life law
area: cad/manufacturing-process-planning
level: intro
summary: Taylor's empirical law V T^n = C linking cutting speed V and tool life T, the base of machining economics and of the choice of cutting speed.
see_also: [cutting-parameter-optimization, computer-aided-process-planning, toolpath-planning, feedrate-scheduling, linear-regression, convex-function, chvorinov-rule]
sources:
  - paper: "Frederick W. Taylor, On the art of cutting metals, Transactions of the American Society of Mechanical Engineers 28, 1907, 31 to 350"
    locator: the address of December 1906 that reports the cutting experiments on speed and tool life behind the law
  - book: isbn:9780133128741
    title: Serope Kalpakjian and Steven R. Schmid, Manufacturing Engineering and Technology, 7th edition, Pearson, 2014
    locator: Section 21.5 (tool life, the Taylor equation and Table 21.3 of the exponent n by tool material) and Section 25.8 (machining economics, the speed for minimum cost and for minimum time)
  - paper: "W. W. Gilbert, Economics of machining, in Machining: Theory and Practice, American Society for Metals, Cleveland, 1950, 465 to 485"
    locator: the cost per part as a function of cutting speed and the tool life for minimum cost and for maximum production rate
---

The Taylor tool life equation relates the cutting speed $V$ of a machining operation to the tool life $T$, the cutting time until the tool is worn out:

$$V T^n = C.$$

The exponent $n$ and the constant $C$ depend on the tool material, the work material and the other cutting conditions. F. W. Taylor found the relation in his cutting experiments and published it in 1907. It is a fit to data, not a law of physics. It is the base of machining economics: with a cost model, it gives the cutting speed of lowest cost and of highest production rate. Planners and [cutting parameter optimization](/cutting-parameter-optimization/) use it in this way.

## The machine

### The law

**Variables.** $V$ is the cutting speed in m/min, $T$ is the tool life in minutes of cutting, and $n$ and $C$ are constants. $C$ is the speed that gives a tool life of one minute.

**Tool life.** A tool is worn out when it meets a tool life criterion, for example a fixed width of the flank wear land. The value of $T$ depends on this criterion, so $C$ does too.

**Form.** Take the logarithm: $\ln V = \ln C - n \ln T$. On a log-log plot, the tool life curve is a straight line with slope $-1/n$ when $\ln T$ is plotted against $\ln V$. A small $n$ means that the tool life falls fast when the speed goes up: for $n = 0.125$, a speed that is 10 percent higher cuts the tool life by about 53 percent, since $1.1^{-1/0.125} = 0.47$. For $n = 0.5$, the cut is about 17 percent.

**Constants.** The exponent depends mostly on the tool material. Kalpakjian and Schmid (Table 21.3) give these ranges:

| tool material | $n$ |
|---|---|
| high-speed steel | 0.08 to 0.2 |
| cast alloys | 0.1 to 0.15 |
| carbides | 0.2 to 0.5 |
| ceramics | 0.5 to 0.7 |

These are ranges, not exact values. A shop measures $n$ and $C$ for its own tool, work material and criterion.

**Fit from two tests.** A turning test at $V_1 = 240$ m/min gives $T_1 = 7.5$ min, and a test at $V_2 = 160$ m/min gives $T_2 = 38$ min. Then

$$n = \frac{\ln(V_1/V_2)}{\ln(T_2/T_1)} = \frac{\ln 1.5}{\ln 5.067} = 0.250, \qquad C = V_1 T_1^{\,n} = 240 \times 7.5^{0.250} = 397 \text{ m/min}.$$

With more tests, fit the line $\ln V = \ln C - n \ln T$ by [least squares](/linear-regression/).

**The extended form.** The basic law fixes the feed $f$ and the depth of cut $d$. The extended form $V T^n f^a d^b = C'$ adds them, with more constants to fit. It is used when the feed and the depth are also variables of the plan.

## What it counts

The model counts minutes of cutting until the tool meets its wear criterion. It does not count the time of the tool in the air, the handling of the part, or a sudden failure of the tool. A planner turns this count into tool edges per part, $t_m / T$, and from there into tool cost and tool change time per part.

## Relation to other models

### Where it comes from

Taylor ran cutting experiments for many years at Midvale Steel and Bethlehem Steel, and reported them to the American Society of Mechanical Engineers in December 1906. The paper is in the Transactions of 1907, so both years are quoted. His aim was to set the speed, the feed and the depth of a cut from data instead of from the habits of the machinist. The same work led to high-speed steel tools.

The law is a fit. The tool wears by abrasion, adhesion, diffusion and oxidation, and each mechanism grows with temperature in its own way. The cutting temperature grows with the speed. Over a limited range of speeds one mechanism leads, and a power law fits the measured lives well. No derivation from the physics gives the form $V T^n = C$ or the value of $n$.

### Range of validity

- **A limited speed range.** The straight line on the log-log plot holds over the range of the tests. At low speed a built-up edge can form on the tool, and at high speed a different wear mechanism can take over. Both bend the line. Do not extrapolate far.
- **One tool, one material, one criterion.** The constants hold for a tool material and grade, a work material in a given state, a tool geometry, a coolant and a wear criterion. A change in any of them needs new constants.
- **What it ignores.** The basic law ignores feed, depth of cut, tool geometry, coolant, the rigidity of the machine and chatter. It ignores interrupted cuts and the thermal shock that they cause. It also ignores sudden failure, such as chipping or fracture of the tool, which ends the tool life before the wear criterion.
- **Scatter.** Tool life is a random quantity. Tests at the same speed give different lives, so $T$ in the law is a typical value, not a guarantee. A planner who needs a low risk of failure in a cut picks a shorter life than the law gives.

## Known results in the model

### How planners use it

**The cost model.** Turn one part with machining time $t_m = K/V$, where $K = \pi D L / f$ for a diameter $D$, a length $L$ and a feed $f$ per turn. Let $C_o$ be the cost of the machine and the operator per minute, $t_c$ the time to change a worn tool, and $C_t$ the cost of a tool edge. A part uses $t_m / T$ tool edges. The cost per part, without the handling cost that does not depend on $V$, is

$$c(V) = C_o\, t_m + \frac{t_m}{T}\,(C_o\, t_c + C_t), \qquad t_m = \frac{K}{V}, \quad T = \left(\frac{C}{V}\right)^{1/n}.$$

**Tool life for minimum cost.** Substitute $t_m$ and $T$:

$$c(V) = \frac{C_o K}{V} + (C_o t_c + C_t)\,K\,C^{-1/n}\,V^{1/n - 1}.$$

Write it as $c(V) = a/V + b V^p$ with $a = C_o K > 0$, $b = (C_o t_c + C_t) K C^{-1/n} > 0$ and $p = 1/n - 1 > 0$, since $0 < n < 1$. Then $c'(V) = -a/V^2 + b p V^{p-1}$, and $c'(V) = 0$ if and only if $V^{p+1} = a/(bp)$. This has one positive root. For a smaller $V$ the derivative is negative, and for a larger $V$ it is positive, so the root is the only minimum. At the root:

$$-\frac{C_o K}{V^2} + (C_o t_c + C_t)\,K\,C^{-1/n}\left(\frac1n - 1\right)V^{1/n - 2} = 0.$$

Multiply by $V^2 / K$ and use $C^{-1/n} V^{1/n} = 1/T$:

$$C_o = (C_o t_c + C_t)\left(\frac1n - 1\right)\frac{1}{T}, \qquad\text{so}\qquad T_{\text{cost}} = \left(\frac1n - 1\right)\left(t_c + \frac{C_t}{C_o}\right).$$

This is the classic result of Gilbert (1950). The speed is then $V_{\text{cost}} = C / T_{\text{cost}}^{\,n}$.

**Tool life for maximum production rate.** The time per part is $t_m + (t_m / T)\,t_c$. This is the cost with $C_o = 1$ and $C_t = 0$, so the same steps give $T_{\text{time}} = (1/n - 1)\,t_c$. Since $C_t > 0$, $T_{\text{time}} < T_{\text{cost}}$: the fastest speed is higher than the cheapest one.

**Worked example.** Use the fitted tool, $n = 0.25$ and $C = 397$ m/min, with $t_c = 2$ min, $C_t = 5$ dollars and $C_o = 1$ dollar per min. A bar has $D = 80$ mm and $L = 300$ mm, and the feed is $0.25$ mm per turn, so $K = \pi \times 80 \times 300 / 0.25$ mm $= 301.6$ m.

- $T_{\text{cost}} = 3 \times (2 + 5) = 21$ min and $V_{\text{cost}} = 397 / 21^{0.25} = 185.5$ m/min.
- $T_{\text{time}} = 3 \times 2 = 6$ min and $V_{\text{time}} = 397 / 6^{0.25} = 253.7$ m/min.

| $V$ (m/min) | $t_m$ (min) | $T$ (min) | cost per part (dollars) | time per part (min) |
|---|---|---|---|---|
| 150 | 2.011 | 49.07 | 2.297 | 2.093 |
| 185.5 | 1.626 | 21.00 | 2.168 | 1.781 |
| 253.7 | 1.189 | 6.00 | 2.576 | 1.585 |
| 300 | 1.005 | 3.07 | 3.300 | 1.661 |

The cost is lowest at 185.5 m/min and the time is lowest at 253.7 m/min, as the formulas say. A grid search over the speed in steps of 0.1 m/min finds the same two minima. Between the two speeds lies the high-efficiency range, where a faster cut costs a little more per part.

**Limits of the model.** The result holds only for one pass with a fixed feed and depth, and only inside the range of validity of the law. A real plan must also meet the limits on power, force, surface finish and machine speed. When a limit is active, the best speed is on the limit, not at $V_{\text{cost}}$. That problem, with feed and depth as variables, is [cutting parameter optimization](/cutting-parameter-optimization/).

## References
