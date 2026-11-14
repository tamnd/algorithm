---
tag: 2Z72PD
kind: technique
slug: springback-compensation
name: Springback compensation
aliases:
- displacement adjustment method
area: cad/manufacturing-process-planning
level: advanced
summary: Changes the die shape by the springback found in forming simulation, iteratively, so the part after release matches its target, as in Gan and Wagoner.
prereqs: [bend-allowance, fixed-point-iteration]
see_also: [k-factor, flat-pattern-development, bend-sequence-planning, banach-fixed-point-theorem, finite-element-method, computer-aided-process-planning]
sources:
  - paper: doi:10.1016/j.ijmecsci.2004.06.006
    title: Wei Gan and R. H. Wagoner, Die design method for sheet springback, International Journal of Mechanical Sciences 46(7), 2004, 1097 to 1113
    locator: the displacement adjustment iteration, in which the die is moved by the deviation of the simulated part from the target, and its comparison with the springforward method
  - paper: doi:10.1007/s12289-008-0369-5
    title: R. Lingbeek, W. Gan, R. H. Wagoner, T. Meinders and J. Weiher, Theoretical verification of the displacement adjustment and springforward algorithms for springback compensation, International Journal of Material Forming 1(3), 2008, 159 to 168
    locator: the analysis of both iterations on an analytical stretch-bending model, with the result that iterative displacement adjustment does better than springforward
  - title: Serope Kalpakjian and Steven R. Schmid, Manufacturing Processes for Engineering Materials, 5th edition, Pearson Prentice Hall, 2008
    locator: Chapter 7, the part on springback in bending, with R_i/R_f = 4 (R_i Y/E T)^3 - 3 (R_i Y/E T) + 1 and the springback factor K_s = (2 R_i/T + 1)/(2 R_f/T + 1) (general locator)
  - book: isbn:9780133128741
    title: Serope Kalpakjian and Steven R. Schmid, Manufacturing Engineering and Technology, 7th edition, Pearson, 2014
    locator: Chapter 16 (sheet-metal forming), the part on springback and its compensation by overbending, bottoming and stretch bending (general locator; the section number is not confirmed)
---

Springback compensation changes the shape of a forming tool so that the part, after it springs back on release, has the target shape. A bent sheet is partly elastic, so when the punch goes up the bend opens a little: the radius gets larger and the bend angle gets smaller. The technique predicts this change with a model or a [finite element](/finite-element-method/) simulation of forming and release, and moves the tool surface against it. The common form is an iteration, introduced for die design by Gan and Wagoner: simulate, measure the deviation of the released part from the target, add the deviation to the tool, and repeat. On this page it is called displacement adjustment (DA). The page derives the springback of a bend in the elastic-perfectly plastic model, and proves that DA converges for that model.

## In plain words

Bend a strip of metal and let it go, and it opens a little. To get a bend of 90 degrees, the press must bend it more than 90 degrees. The question is how much more.

For a simple bend there is a formula for the opening. For a part with a curved shape there is no formula, so the planner runs a simulation of the forming. The simulation says where the released part ends up. Where the part is too open, the planner bends the tool shape further by the same amount, and runs the simulation again. After a few rounds the released part is close to the target. The method does not always converge, so the planner must check the result.

## When it applies

- The part is formed by a tool (a punch and die, or a die face in a stamping) whose shape the planner can change, and the material springs back by a visible amount. High-strength steels and aluminium alloys spring back more than mild steel, because the ratio $Y/E$ of yield stress to elastic modulus is larger.
- There is a way to predict the released shape from a tool shape: a closed-form model for simple bends, a forming simulation, or a try-out of the real tool.
- The springback is a smooth function of the tool shape near the target, so that a small change of the tool gives a small change of the part. Where contact changes, wrinkles form or the part buckles, this fails.

## The template

Let $S_t$ be the target shape, let $D$ be the tool shape, and let $F(D)$ be the shape of the part after forming with $D$ and release. Shapes are compared at matching points, for example the nodes of a mesh, along a fixed direction.

```pseudo id=main
SPRINGBACK-COMPENSATION(S_t, F, tol, k_max)
L1  D ← S_t
L2  for k ← 0 to k_max - 1 do
L3      S ← F(D)
L4      e ← S_t - S
L5      if |e| ≤ tol then return D
L6      D ← D + e
L7  return D, with a warning that the tolerance was not met
```

The holes are the predictor $F$ (lines L3), the measure of the deviation (L4 and L5) and the update (L6). With the update of line L6 the iteration is DA. A fixed point of the iteration is a tool with $F(D) = S_t$.

**The springback of a bend.** For one bend, the shape is the curvature $\kappa = 1/\rho$ of the neutral axis. Take a sheet of thickness $t$ and width $w$ of an elastic-perfectly plastic material with modulus $E$ and yield stress $Y$. Assume pure bending (no tension), plane sections stay plane, the neutral axis is at mid-thickness, the sheet does not get thinner, and the stress is uniaxial. At the distance $y$ from the neutral axis the strain is $y/\rho$. It is elastic for $|y| \le c$ with $c = Y \rho / E$, and the stress is $\pm Y$ outside. For $c \le t/2$ the bending moment is

$$M = 2w\left(\int_0^c \frac{E y^2}{\rho}\, dy + \int_c^{t/2} Y y \, dy\right) = w Y\left(\frac{t^2}{4} - \frac{c^2}{3}\right).$$

On release the moment goes to zero and the sheet unloads elastically, so the curvature drops by $\Delta\kappa = M/(EI)$ with $I = w t^3/12$:

$$\Delta\kappa = \frac{3Y}{E t} - \frac{4 Y^3 \rho^2}{E^3 t^3}.$$

With $x = \rho_i Y/(E t)$ for the radius $\rho_i$ under load and $\rho_f$ after release, $\kappa_f = \kappa_i - \Delta\kappa$ gives

$$\frac{\rho_i}{\rho_f} = 4x^3 - 3x + 1, \qquad 0 \le x \le \tfrac12.$$

This is the formula that Kalpakjian and Schmid give with the inside radius in place of $\rho$. The right side falls from 1 at $x = 0$ to 0 at $x = 1/2$, where the whole section is elastic and the bend springs back flat. For $x > 1/2$ the bend is elastic and $\Delta\kappa = \kappa_i$. The neutral axis keeps its length, so the bend angles satisfy $\rho_i \alpha_i = \rho_f \alpha_f$, and the springback factor is $K_s = \alpha_f/\alpha_i = \rho_i/\rho_f$, which is Kalpakjian's $(2R_i/T + 1)/(2R_f/T + 1)$ with $\rho = R + T/2$.

**What the model ignores.** Work hardening, the tension that a die applies while it bends (stretch bending reduces springback a lot), the shift of the neutral axis and the thinning, the Bauschinger effect and the nonlinear unloading of real metals, plane strain (which replaces $E$ by $E/(1 - \nu^2)$), anisotropy, friction and the contact with the die. The values of $Y$ and $E$ also scatter from coil to coil. So the formula gives the size and the trend of springback, not the exact value, and production uses simulation and try-out.

**DA converges for this model.** Write the predictor in curvature: $\kappa_f(\kappa) = \kappa - \Delta\kappa(\kappa)$, with $\Delta\kappa(\kappa) = \kappa$ for $\kappa \le \kappa_e = 2Y/(Et)$ and the formula above for $\kappa > \kappa_e$. The two parts agree at $\kappa_e$. Line L6 is $\kappa^{k+1} = \kappa^k + \kappa_t - \kappa_f(\kappa^k)$, that is

$$\kappa^{k+1} = g(\kappa^k), \qquad g(\kappa) = \kappa_t + \Delta\kappa(\kappa), \qquad \kappa^0 = \kappa_t > 0.$$

*Claim.* The sequence increases to the unique tool curvature $\kappa^*$ with $\kappa_f(\kappa^*) = \kappa_t$, and the error falls at the linear rate $8x_*^3 < 1$, where $x_* = Y/(E t \kappa^*)$.

*Proof.* $\Delta\kappa$ is continuous and non-decreasing: its slope is 1 in the elastic part, and $8Y^3/(E^3 t^3 \kappa^3) = 8x^3 \in (0, 1)$ in the plastic part, where $x = Y/(Et\kappa) < 1/2$. So $g$ is non-decreasing. Since $\Delta\kappa \ge 0$, $\kappa^1 = g(\kappa^0) \ge \kappa_t = \kappa^0$, and by induction $\kappa^{k+1} = g(\kappa^k) \ge g(\kappa^{k-1}) = \kappa^k$. Also $\Delta\kappa < 3Y/(Et)$, so the sequence is bounded by $\kappa_t + 3Y/(Et)$. A bounded increasing sequence has a limit $\kappa^*$, and the continuity of $g$ gives $g(\kappa^*) = \kappa^*$, that is $\kappa_f(\kappa^*) = \kappa_t$. This root is unique: in the elastic part $\kappa_f = 0 < \kappa_t$, and in the plastic part $\kappa_f$ has slope $1 - 8x^3 > 0$, so it is strictly increasing. Near $\kappa^*$, $g$ has the slope $8x_*^3$, and $x_* < 1/2$ because $\kappa^* > \kappa_e$. So the error is multiplied by about $8x_*^3 < 1$ per step, as in the [fixed-point iteration](/fixed-point-iteration/) theorem. $\square$

This proof needs a predictor that is monotone, with a slope of springback less than 1. For a 3D part in a finite element simulation there is no such guarantee. Lingbeek, Gan, Wagoner, Meinders and Weiher verify DA on an analytical stretch-bending model, and find the iterated DA better than the springforward method.

## Classic examples

**Air bending of a strip.** Sheet with $t = 1$ mm and $Y/E = 0.002$ (for example $Y = 140$ MPa and $E = 70$ GPa, an assumed aluminium alloy). The target is a bend of 90 degrees with neutral radius $\rho_t = 50$ mm, so $x = 0.1$. A tool with the target shape gives $\rho_i/\rho_f = 0.704$: the part has radius 71.02 mm and angle 63.36 degrees. DA in curvature form gives:

| step $k$ | tool radius (mm) | released radius (mm) | error in radius (mm) |
|---|---|---|---|
| 0 | 50.0000 | 71.0227 | 21.0227 |
| 1 | 38.5802 | 50.0811 | 0.0811 |
| 2 | 38.5321 | 50.0003 | 0.0003 |
| 3 | 38.5319 | 50.0000 | below 0.0001 |

The fixed point has $x_* = 0.0771$ and rate $8x_*^3 = 0.0037$, so each step gains more than two digits. The tool angle follows from the neutral length: $\alpha_i = 90 \times 50 / 38.5319 = 116.79$ degrees.

**A large radius.** With $\rho_t = 400$ mm, the first tool ($x = 0.8$) is elastic, and the strip springs back flat. The elastic part of the proof applies: $\kappa^1 = 2\kappa_t$, a tool radius of 200 mm. Then the iteration goes 138.50, 126.81, 125.23, 125.03 mm, to the fixed point 125 mm with $x_* = 0.25$ and rate $0.125$. The convergence is slower as $x_*$ gets close to $1/2$.

**Die faces in stamping.** Gan and Wagoner apply the same loop to the nodes of a die face, with $F$ a finite element simulation of forming and release. The tool and the part are meshes, and $e$ is the deviation of each node along a fixed direction.

## Variations

- **Springforward.** Take the internal forces of the formed part at the end of forming, apply them with the opposite sign to the target shape, and use the resulting shape as the tool. It needs one simulation per step, and in the analysis of Lingbeek and coauthors it does worse than iterated DA.
- **Compensation factor.** Replace line L6 by $D \leftarrow D + \lambda e$. A value $\lambda > 1$ can speed up a slow iteration, and $\lambda < 1$ can damp an oscillation. In the model above the best fixed $\lambda$ is $1/(1 - 8x_*^3)$, the reciprocal of the slope of $\kappa_f$ at the fixed point, which is close to 1 for small $x_*$.
- **Overbending by a table.** On a press brake the operator bends to the angle $\alpha_i = \alpha_f / K_s$, with $K_s$ from a chart of the material. This is one step of the template with a closed-form predictor.
- **Changing the process.** Bottoming, coining and stretch bending reduce springback, so that less compensation is needed. They change $F$, not the update.

## Pitfalls

- A compensated die face may not be smooth, may have an [undercut](/undercut-detection/) for the press direction, or may change the contact between the die and the sheet, so the next simulation is a different problem.
- The deviation $e$ must be measured at matching points. When the part moves as a rigid body after release, the mesh nodes do not match points of the target unless the shapes are first aligned.
- The predictor is only as good as the material model. A compensation that is exact in the simulation can be wrong on the press by the error of the material model, and try-out is still needed.
- The iteration needs one full forming simulation per step, so the number of steps is the cost. Stop at a tolerance on the part, not on the tool.
- Springback compensation does not change the blank length in the [bend allowance](/bend-allowance/) model, because the neutral axis keeps its length.

## Exercises

1. Show that for $x \le 1/2$ the function $4x^3 - 3x + 1$ equals $(1 - 2x)^2(1 + x)$, and use it to show that the released radius is always larger than the radius under load.
2. Find the tool radius for $\rho_t = 200$ mm with the data of the first example. (The iteration goes 200, 102.88, 93.80, 93.30 mm, to about 93.27 mm.)
3. Show that a fixed compensation factor $\lambda$ with $0 < \lambda < 2/(1 - 8x_*^3)$ also gives local convergence in the model.

## References
