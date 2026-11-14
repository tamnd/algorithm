---
tag: AMPEFR
kind: problem
slug: function-generation
name: Function generation
aliases:
- function generation synthesis
area: cad/mechanism-and-assembly-design
level: core
summary: Find a linkage whose output angle is a given function of its input angle, exactly at precision points and approximately in between.
prereqs: [kinematic-synthesis, four-bar-linkage]
see_also: [freudenstein-equation, chebyshev-spacing, optimization-based-linkage-synthesis, path-generation, motion-generation, slider-crank-mechanism, minimax-approximation, transmission-angle]
sources:
  - paper: "Ferdinand Freudenstein, Approximate synthesis of four-bar linkages, Transactions of the ASME 77(8), 1955, 853 to 861"
    locator: function generation with precision points, the structural error, and the spacing of the precision points
  - book: isbn:9781260113310
    title: Robert L. Norton, Design of Machinery, 6th edition, McGraw-Hill, 2019
    locator: Section 3.2 (p. 100, function generation as one of the three tasks) and Section 5.13 (p. 267, analytical synthesis of a fourbar function generator)
  - book: isbn:0130408727
    title: Arthur G. Erdman, George N. Sandor and Sridhar Kota, Mechanism Design, Analysis and Synthesis, Volume 1, 4th edition, Prentice Hall, 2001
    locator: Chapter 8, Introduction to Kinematic Synthesis (function generation, precision points and the structural error)
  - book: "Richard S. Hartenberg and Jacques Denavit, Kinematic Synthesis of Linkages, McGraw-Hill, New York, 1964"
    locator: the chapters on function generation and on the accuracy of precision point designs (general locator)
---

Function generation is the [kinematic synthesis](/kinematic-synthesis/) task in which the output link of a mechanism must turn by an angle that is a given function of the angle of the input link. A given relation $y = f(x)$ is mapped to angles by two linear scales, and the goal is a mechanism, usually a [four-bar linkage](/four-bar-linkage/), whose output angle follows the scaled function. A four-bar has only a few free dimensions, so it meets a general function exactly only at a few precision points, and the difference in between is the structural error. This page states the problem; the methods that solve it are linked from Known algorithms.

## In plain words

You want a machine part that turns in a fixed relation to another part. When the first part turns by some amount, the second part must turn by an amount that a formula gives. Before computers, linkages of this kind did calculations, for example a square root or a logarithm, in gun sights and other instruments.

A four-bar linkage has only a few lengths to choose. It cannot follow most formulas exactly. You pick a few values where it must be exact, and accept a small error between them. The design question is how to choose the lengths, and where to put the exact values, so that the error stays small over the whole range.

## Definition

**Input.**

- A function $f$ on an interval $[x_0, x_1]$, with $y_0 = f(x_0)$ and $y_1 = f(x_1)$, $y_0 \ne y_1$.
- An input range: a start angle $\varphi_0$ and a sweep $\Delta\varphi$.
- An output range: a start angle $\psi_0$ and a sweep $\Delta\psi$.
- A type of mechanism, usually the four-bar, sometimes the [slider-crank](/slider-crank-mechanism/) (with a slide in place of the output angle) or a six-bar.

The scales map the variable and the value of $f$ to angles:

$$\varphi(x) = \varphi_0 + \frac{x - x_0}{x_1 - x_0}\,\Delta\varphi, \qquad \psi_d(x) = \psi_0 + \frac{f(x) - y_0}{y_1 - y_0}\,\Delta\psi.$$

**Output.** The dimensions of the mechanism. For the four-bar in the notation of the four-bar page these are the input $a$, coupler $b$, output $c$ and ground $d$, with the input pivot at $O_2 = (0, 0)$, the output pivot at $O_4 = (d, 0)$, and both angles counterclockwise from the ground line. One length sets the scale, so $d = 1$ can be fixed.

**Error.** Let $\psi(\varphi)$ be the output angle of the mechanism on one fixed branch of its assembly. The structural error is

$$e(x) = \psi(\varphi(x)) - \psi_d(x), \qquad x_0 \le x \le x_1.$$

It is the error of an ideal mechanism with exact dimensions; the error from tolerances and clearances (the mechanical error) is a separate question.

**Two forms of the problem.**

- *Precision points.* Given $x_1 < x_2 < \cdots < x_n$ in the interval, find a mechanism with $e(x_j) = 0$ for all $j$, assembled on one branch over the whole range.
- *Approximation.* Find a mechanism that minimizes $\max_x |e(x)|$ (the uniform or minimax form) or $\int e(x)^2\,dx$ (the least squares form), with the same assembly condition.

The [transmission angle](/transmission-angle/) and the link length ratios are usually constrained too.

## Variants

- **Fixed or free ranges.** With $\varphi_0$, $\psi_0$, $\Delta\varphi$, $\Delta\psi$ fixed, the four-bar has three free ratios. With the start angles free there are five unknowns, so up to five precision points.
- **Output as a slide.** A slider-crank turns an angle into a linear position $s(x)$.
- **Infinitesimal precision points.** Ask that $e$ and some of its derivatives vanish at one value of $x$, so that the mechanism matches $f$, $f'$ and $f''$ there.
- **Multiple loops.** Six-bars and geared linkages give more dimensions and so more precision points, at the cost of a harder system.
- **Function generation by inversion.** Seen from the input link, the output link makes a rigid motion, so the task is a case of [motion generation](/motion-generation/) for the output link relative to the input link.

## Examples

**Exact generators.** A few functions are generated with zero structural error. For the four-bar with $a = c$ and $b = d$, [Freudenstein's equation](/freudenstein-equation/) has the constants $K_1 = K_2 = k = d/a$ and $K_3 = 1$, and its half-angle quadratic factors. The two roots are

$$\tan\frac{\psi}{2} = \tan\frac{\varphi}{2} \qquad\text{and}\qquad \tan\frac{\psi}{2} = \frac{1 + k}{1 - k}\tan\frac{\varphi}{2}.$$

The first is the parallelogram, which generates $\psi = \varphi$. The second is the antiparallelogram, which for $a = 1$, $d = 2$ generates $\tan(\psi/2) = -3\tan(\varphi/2)$ exactly. Both pass through the change point where all four pins are on one line, at $\varphi = 0$ and $\varphi = 180°$. There the linkage can switch from one function to the other, which is why a physical parallelogram needs a guard at those points.

**A sine generator.** Let $f(x) = \sin x$ on $[0, \pi/2]$, with $\varphi$ from $90°$ to $210°$ ($\Delta\varphi = 120°$) and $\Delta\psi = 60°$, and $d = 1$. Take the three precision points at the [Chebyshev spacing](/chebyshev-spacing/) $x_j = \pi/4 - (\pi/4)\cos((2j - 1)\pi/6)$, which are $6.03°$, $45°$ and $83.97°$ in degrees of $x$. The table gives three choices of the output start angle $\psi_0$, the four-bar found by [Freudenstein's equation](/freudenstein-equation/) for each, and its largest $|e|$ on a grid of 1000 values of $x$ along the branch through the precision points.

| $\psi_0$ | $K_1, K_2, K_3$ | $a$, $b$, $c$ | max $\lvert e\rvert$ | at $x$ | transmission angle |
| --- | --- | --- | --- | --- | --- |
| $60°$ | $2.30958$, $1.72053$, $-0.31839$ | $0.4330$, $1.2983$, $0.5812$ | $0.679°$ | $0$ | $56.4°$ to $91.1°$ |
| $75°$ | $2.34444$, $1.81700$, $0.34900$ | $0.4265$, $1.1493$, $0.5504$ | $0.230°$ | $0$ | $69.6°$ to $109.0°$ |
| $90°$ | $2.40082$, $1.80388$, $1.01081$ | $0.4165$, $1.0070$, $0.5544$ | $0.438°$ | $1.127$ | $82.4°$ to $127.9°$ |

The precision points are the same in the three rows. Only the start of the output scale moves, and the largest error changes by a factor of three. So $\psi_0$, $\Delta\varphi$ and $\Delta\psi$ are design variables of the problem, not data. In the row $\psi_0 = 75°$ the error is $-0.230°$ at $x = 0$, $+0.131°$ at $x = \pi/2$, and the inner peaks are $+0.135°$ and $-0.074°$. These magnitudes are not equal, so this design is not the minimax design for these ranges.

**A count that rules out exactness.** With the ranges fixed, the four-bar outputs form a family with three parameters, and with free start angles five. A general $f$ given at six points is met at all six only for special data. So for most functions the structural error is not zero, and the question is how small it can be made.

## Known algorithms

- [Freudenstein's equation](/freudenstein-equation/) gives a $3 \times 3$ linear system for three precision points. It is exact at the points if the system is regular and the result assembles on one branch.
- [Chebyshev spacing](/chebyshev-spacing/) chooses the precision points from the zeros of a Chebyshev polynomial. It lowers the polynomial factor in the usual estimate of the structural error, but does not give the minimax linkage.
- With free start angles, four or five precision points give a polynomial system, solved by elimination or by [homotopy continuation](/homotopy-continuation/).
- Least squares on the residual of Freudenstein's equation over many points is linear in $K_1, K_2, K_3$. It minimizes the residual, not $e$.
- [Optimization-based dimensional synthesis](/optimization-based-linkage-synthesis/) minimizes $\max|e|$ or a sum of $e^2$ over many points directly, with local or global optimizers. A minimax design can be refined by an exchange of the error peaks, in the spirit of the [Remez algorithm](/remez-algorithm/), but the linkage problem is not linear in its parameters, so the guarantees of that algorithm do not carry over.

## Bounds

- **Exact points.** Three precision points for a four-bar with fixed ranges, five with free start angles. A Watt or Stephenson six-bar has more dimensions and so more points.
- **Lower bounds on the error.** For a linear family, [Chebyshev's equioscillation theorem](/chebyshev-equioscillation-theorem/) characterizes the best uniform approximation by the alternation of its error. The four-bar output is not a linear family in its dimensions, so that theorem does not apply directly, and the sources cited here give no general lower bound on the structural error of a four-bar for a given $f$.
- **Zeros.** A design with $n$ precision points has at least $n$ zeros of $e$ in the interval. It can have more: the error can cross zero at points that were not prescribed.

## Reductions

- **To a linear system.** For three precision points and fixed ranges, Freudenstein's equation is linear in $K_1, K_2, K_3$.
- **To motion generation.** Fix the input link as a new ground. The output link then moves through rigid positions, and a dyad that guides it is the coupler and output of the four-bar.
- **To polynomial interpolation, in an estimate.** If the mechanism has enough free parameters and $e$ is smooth, $e(x)$ is close to a constant times $\prod_j (x - x_j)$. This is the analogy with polynomial interpolation that motivates [Chebyshev spacing](/chebyshev-spacing/). It is an estimate, not an identity.

## Applications

Function generators computed the logarithm, the square, trigonometric functions and ballistic tables in mechanical analog computers and fire control instruments. Today the same task appears in steering linkages (the Ackermann relation between the angles of the two front wheels), throttle and valve linkages, and in any mechanism where an output must turn in a fixed nonlinear relation to an input. The study of linkages that approximate a motion led Chebyshev to his theory of best uniform approximation, which is now the theory on the [minimax approximation](/minimax-approximation/) page.

## References
