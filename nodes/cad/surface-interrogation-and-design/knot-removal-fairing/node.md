---
tag: GM71P6
kind: algorithm
slug: knot-removal-fairing
name: Fairing by knot removal and reinsertion
aliases:
- Farin-Sapidis fairing
area: cad/surface-interrogation-and-design
level: advanced
summary: Farin, Rein, Sapidis and Worsey's fairing that removes and reinserts the knot where the curvature plot jumps most, step by step, until the curve is fair.
model: real-ram
complexity:
  vars: {n: "the number of control points minus one", R: "the number of rounds"}
  time: {worst: O(R n^3)}
  space: {extra: Θ(n)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1987
  people: [Gerald Farin, Gerhard Rein, Nickolas Sapidis, Andrew Worsey]
  note: Farin, Rein, Sapidis and Worsey faired cubic B-spline curves locally by inverting knot insertion. Sapidis and Farin made the choice of the knots automatic in 1990, with the jump of the curvature derivative as the criterion.
prereqs: [b-spline, boehm-knot-insertion, curvature-comb]
see_also: [curvature-comb, energy-based-surface-fairing, smoothing-spline, reflection-lines, knot-refinement, parametric-continuity, minimum-variation-surface, least-squares-approximation]
sources:
  - paper: "Gerald Farin, Gerhard Rein, Nickolas Sapidis and Andrew J. Worsey, Fairing cubic B-spline curves, Computer Aided Geometric Design 4(1-2), 91 to 103, 1987"
    title: Farin, Rein, Sapidis and Worsey 1987
    locator: local fairing of cubic B-spline curves by inversion of knot insertion, judged by the curvature plot
  - paper: doi:10.1016/0010-4485(90)90006-X
    title: "Nickolas Sapidis and Gerald Farin, Automatic fairing algorithm for B-spline curves, Computer-Aided Design 22(2), 121 to 129, 1990"
    locator: repeated removal and reinsertion of knots chosen automatically by a fairness criterion
  - paper: doi:10.1109/38.19051
    title: "Gerald Farin and Nickolas Sapidis, Curvature and the fairness of curves and surfaces, IEEE Computer Graphics and Applications 9(2), 52 to 57, 1989"
    locator: the curvature plot as the measure of fairness, and few monotone pieces of curvature as the aim
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: the treatment of curve fairing and of knot removal
---

Fairing by knot removal and reinsertion smooths the curvature of a planar cubic B-spline curve, one knot at a time. At a simple knot a cubic spline is $C^2$, so its curvature is continuous, but the derivative of the curvature can jump. A large jump shows in the [curvature plot](/curvature-comb/) as a kink, and the eye sees it as a flat spot or a bump in the curve. The method finds the knot with the largest jump, removes that knot as if the curve were $C^3$ there, and inserts it again. The knot vector does not change, one control point moves, and after the step the curvature derivative is continuous at that knot. Farin, Rein, Sapidis and Worsey gave the method in 1987, and Sapidis and Farin made it automatic in 1990. A tolerance keeps the curve near the original.

## In plain words

A designer looks at a curve, for example a section of a car body, and sees a small dent. The dent is hard to see in the curve but easy to see in a plot of how sharply the curve bends: the plot has kinks and dips. The curve is made of cubic pieces that meet at knots. At each knot the method asks how much the bending rate jumps. It takes the knot with the largest jump and pretends that the two pieces there are really one cubic. It computes that single cubic from the control points on both sides, which do not see the dent, and splits it again at the same knot. This moves one control point, and the kink at that knot is gone. Then it looks again for the worst knot, until no step helps or the curve would move too far.

## The problem

**Input.** A planar cubic B-spline curve $c(t) = \sum_{i=0}^{n} N_i(t) d_i$ on a clamped knot vector $t_0 = \dots = t_3 < t_4 < \dots < t_n < t_{n+1} = \dots = t_{n+4}$, with simple inner knots. A tolerance $\varepsilon \ge 0$ and a number of rounds.

**Output.** New control points $\hat d_0, \dots, \hat d_n$ on the same knots with $|\hat d_i - d_i| \le \varepsilon$ for all $i$, and a curve that is fairer by the measure below.

**Measure.** Write $c' \times c'' = x' y'' - y' x''$. The signed curvature is $\kappa = (c' \times c'') / |c'|^3$, and its derivative is

$$\kappa' = \frac{c' \times c'''}{|c'|^3} - 3 \frac{(c' \times c'')(c' \cdot c'')}{|c'|^5}.$$

At a simple knot $t_r$ only $c'''$ jumps, so $\kappa'$ jumps by $\Delta_r = c'(t_r) \times (c'''(t_r^+) - c'''(t_r^-)) / |c'(t_r)|^3$. The measure is $E = \sum_r \Delta_r^2$ over the inner knots. Fairness has no single definition. The measure $E$, the number of sign changes of the curvature and the energies of the other fairing methods are design criteria, not theorems: a curve that is better by one of them can look worse, and can be worse by another.

## The algorithm

The step at an inner knot $t_r$, $4 \le r \le n$, uses the three ratios of [Boehm insertion](/boehm-knot-insertion/) of $t_r$ into the knot vector without $t_r$:

$$\alpha_{r-3} = \frac{t_r - t_{r-3}}{t_{r+1} - t_{r-3}}, \qquad \alpha_{r-2} = \frac{t_r - t_{r-2}}{t_{r+2} - t_{r-2}}, \qquad \alpha_{r-1} = \frac{t_r - t_{r-1}}{t_{r+3} - t_{r-1}}.$$

Insertion makes $d_{r-3}$, $d_{r-2}$ and $d_{r-1}$ from four points of the curve without $t_r$. Removal inverts the first equation from the left and the last one from the right:

$$L = \frac{d_{r-3} - (1 - \alpha_{r-3}) d_{r-4}}{\alpha_{r-3}}, \qquad R = \frac{d_{r-1} - \alpha_{r-1} d_r}{1 - \alpha_{r-1}}.$$

Reinsertion gives back $d_{r-3}$ and $d_{r-1}$ unchanged and replaces the middle point by $\hat d_{r-2} = (1 - \alpha_{r-2}) L + \alpha_{r-2} R$.

```pseudo id=main
FAIR(t_0..t_{n+4}, d_0..d_n, ε, rounds)
L1  d⁰ ← d; E ← Σ_r Δ_r² over the inner knots
L2  repeat at most rounds times
L3    order the inner knots t_r by decreasing Δ_r²
L4    for each t_r in this order with Δ_r ≠ 0
L5      d̂ ← d with d_{r-2} replaced by (1 − α_{r-2}) L + α_{r-2} R
L6      if |d̂_i − d⁰_i| ≤ ε for every i and E(d̂) < E then
L7        d ← d̂; E ← E(d̂); go to the next round
L8    if no knot was accepted then stop
L9  return d
```

Lines L3 and L4 are the choice of Sapidis and Farin: try the worst knot first. Line L6 has two tests. The first keeps every control point within $\varepsilon$ of its first position, which keeps the curve within $\varepsilon$. The second is the rule of this implementation: a step is taken only if it lowers $E$, since fairing one knot changes the jumps at the four knots around it, and without the rule the loop can go round in a circle.

## Example

Take the uniform knots $(0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 6, 6, 6)$ and the nine control points $d_i = (i, \frac{(i - 4)^2}{4})$, a convex curve shaped like a parabola. Dent it by moving $d_4$ from $(4, 0)$ to $(4, \frac12)$. The point of the curve at $t = 3$ moves from $(4, \frac1{12})$ to $(4, \frac{5}{12})$, and the bottom of the curve becomes a shallow W: on $[2, 3]$ the function $c' \times c''$ is $1 - \frac32 (t - 2)$, so the curvature changes sign at $t = \frac83$ and, by symmetry, at $t = \frac{10}{3}$.

- **L1.** The squared jumps at the knots $1, 2, 3, 4, 5$ are about $0.51, 1.88, 9, 1.88, 0.51$. At $t = 3$, $c' = (1, 0)$ and $c'''$ jumps from $(0, -\frac32)$ to $(0, \frac32)$, so $\Delta = 3$.
- **L3 to L5.** The worst knot is $t_6 = 3$, so $r = 6$. The ratios are $\alpha_3 = \frac34$, $\alpha_4 = \frac12$, $\alpha_5 = \frac14$. From $d_2 = (2, 1)$ and $d_3 = (3, \frac14)$, $L = (\frac{10}{3}, 0)$. From $d_5 = (5, \frac14)$ and $d_6 = (6, 1)$, $R = (\frac{14}{3}, 0)$. So $\hat d_4 = \frac12 L + \frac12 R = (4, 0)$.
- **L6, L7.** With $\varepsilon = 1$ the move $\frac12$ is allowed, and $E$ falls from about $13.77$ to about $0.885$. The curve is the undented curve again, with no sign change of curvature, and the point at $t = 3$ has moved by $\frac13$.
- **Next round.** The remaining jumps sit at the knots near the clamped ends, where the B-spline basis is not uniform. No step there lowers $E$ within the tolerance, so the loop stops.

The step restores the dent exactly because $L$ and $R$ depend only on $d_2$, $d_3$, $d_5$ and $d_6$, which lie on the undented curve, and the undented curve is $C^3$ at $t = 3$. With $\varepsilon = \frac14$ the point $d_4$ cannot move back. The method then takes four smaller steps, at the knots $2$, $4$, $3$ and $2$ in this order, which move $d_3$, $d_4$ and $d_5$ by less than $\frac14$ each. The result has no inflection either, but its measure $E$ is about $1.68$, and the bottom of the curve stays a little flatter than the parabola.

## Correctness

Three facts make the method sound. First, the step at $t_r$ is a real knot removal followed by insertion: $L$ and $R$, with the other points unchanged, are the control points of a cubic spline on the knots without $t_r$, and Boehm insertion of $t_r$ into it gives exactly the new points, with $d_{r-3}$ and $d_{r-1}$ unchanged by the choice of $L$ and $R$. That spline is one cubic polynomial on $(t_{r-1}, t_{r+1})$, so after the step the curve is $C^3$ at $t_r$ and $\Delta_r = 0$. Second, the curve on fixed knots depends on the control points through $N_i \ge 0$ with $\sum_i N_i = 1$, so the curve moves by at most $\max_i |\hat d_i - d^0_i| \le \varepsilon$, which line L6 checks. Third, every accepted step lowers $E$ strictly, and the number of rounds is bounded, so the loop ends. The method does not promise fewer inflections, since the measure is a design criterion: the tests contain a dent on a steep part of a curve where $E$ falls and both inflections stay. The proofs, with the count of sign changes, are in the proof file.

## Complexity

Let $n + 1$ be the number of control points and $R$ the number of rounds. The implementation computes the derivative curves for each jump, in $O(n)$, so the measure costs $O(n^2)$. In a round it may try all $n - 3$ knots and compute $E$ for each, so a round costs $O(n^3)$ and the whole run $O(R n^3)$. A step changes one control point, which changes the jumps at most at the five knots $t_{r-2}, \dots, t_{r+2}$. An implementation that keeps the jumps in a priority queue and updates only these five costs $O(\log n)$ per step after $O(n)$ set up. The extra space is the copy of the first control points, $\Theta(n)$.

## Properties

- **Local.** A step moves one control point, so the curve changes only on the four knot intervals of $N_{r-2}$, $[t_{r-2}, t_{r+2}]$.
- **Same representation.** The knot vector and the number of control points stay the same, so the faired curve can replace the original in a model without changes to the data structure.
- **Bounded change.** The curve never moves farther than the tolerance from the original.
- **Exact.** With rational input every step is rational, and the implementation is exact, including the count of curvature sign changes.
- **Fixed points.** A curve that is $C^3$ at a knot is not changed by the step there. A single cubic polynomial, written on any knots, is not changed at all.
- **Not invariant under reparametrization.** The step depends on the knots, so the same point set on other knots gives another result.

## Variants and improvements

- **Several knots at a time.** Removing two or more neighbouring knots and reinserting them changes more control points and smooths over a longer stretch.
- **Other removal steps.** The step here takes the left estimate for one side and the right estimate for the other. Sapidis and Farin give a new knot removal algorithm for this use, and the general knot removal of Lyche and Mørken removes knots within a tolerance in a norm.
- **Fairing to a target curvature.** Later methods move the control points so that the curvature plot approaches a smooth target plot.
- **Local energy fairing.** Eck and Hadenfeld, motivated by this method, change the curve locally to lower an energy, which is a local form of [energy-based fairing](/energy-based-surface-fairing/) for curves.
- **Surfaces.** The same idea, applied to the iso-parameter curves of a tensor product surface, fairs surfaces row by row, but the rows interact, and global energy methods are more usual.
- **Space curves.** For a curve in space the jump of the curvature derivative uses $|c' \times c''|$ and needs a square root, but the step itself is the same.

## When to use it

Use the method to remove small local defects from a cubic B-spline curve that is already close to the wanted shape, such as a curve interpolated through measured points with noise, when the curve must keep its knots and stay within a tolerance. It is cheap, local and easy to control. It does not fix the global shape: for that, a [smoothing spline](/smoothing-spline/) or an energy minimization over all control points is better. For curves with large wiggles the tolerance stops it before it can help.

## Pitfalls

- **Measure is not shape.** A lower $E$ does not mean fewer inflections, and fewer inflections is not always the aim. Check the result with a [curvature comb](/curvature-comb/) or [reflection lines](/reflection-lines/).
- **End knots.** Near a clamped end the basis is not uniform, and even a fair curve has jumps there. The rule that $E$ must fall stops the loop from wasting the tolerance on them.
- **Cycles.** Without a rule that the measure must fall, fairing one knot can undo another, and the loop runs to its limit of rounds.
- **Weighting.** The jump is divided by $|c'|^3$, so knots where the parameter speed is high count less. A defect on a fast part of the curve may never be chosen.
- **Multiple knots.** At a double knot the curve is only $C^1$, and the step above does not apply. The implementation rejects such curves.
- **Tolerance used up.** The tolerance is measured from the original points, so many small steps can use it up and block a later, more useful step.

## Implementations

The Python file in this folder has `fair_by_knot_removal(knots, ctrl, tol, rounds)`, which returns the new control points and the list of faired knots, `remove_and_reinsert` for one step, `kappa_jump` for the squared jump of the curvature derivative, `fairness` for the measure $E$, and `curvature_sign_changes`, which counts the sign changes of the curvature exactly: on each knot interval of a cubic, $c' \times c''$ is a polynomial of degree at most $2$, and its signs at the ends and at its vertex give every change. The shared helper `si3spline.py` holds the evaluation and the derivative curves. The tests check the worked example, that one step changes one control point and makes the third derivative continuous at the knot, that dents near the bottom of a parabola lose their inflections, that the curve never moves more than the tolerance at random points, that the measure never rises, the sign change counter against dense sampling, and the steep dent where the measure falls but the inflections stay.

## History

Fairing by hand, with splines and weights on the loft floor, is old, and the curvature plot became the tool for judging fairness in CAD in the 1980s. Farin, Rein, Sapidis and Worsey published fairing of cubic B-spline curves by inverting knot insertion in 1987, and in the same year Sapidis wrote a master's thesis on local fairing at the University of Utah. Farin and Sapidis described the curvature plot as the measure of fairness in 1989, and in 1990 Sapidis and Farin gave the automatic algorithm that picks the knots by the fairness criterion and repeats.

## References
