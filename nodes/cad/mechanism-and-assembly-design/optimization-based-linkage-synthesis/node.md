---
tag: N2SRNH
kind: technique
slug: optimization-based-linkage-synthesis
name: Optimization-based dimensional synthesis
aliases:
- approximate linkage synthesis
area: cad/mechanism-and-assembly-design
level: advanced
summary: Fits link dimensions so a coupler point follows many target points in least squares, by gradient, evolutionary or continuation methods, beyond exact precision points.
prereqs: [path-generation, nonlinear-least-squares]
see_also: [nine-point-path-synthesis, function-generation, motion-generation, chebyshev-spacing, levenberg-marquardt, differential-evolution, genetic-algorithm, transmission-angle]
sources:
  - paper: "R. L. Fox and K. D. Willmert, Optimum design of curve-generating linkages with inequality constraints, ASME Journal of Engineering for Industry 89(1), 1967, 144 to 152"
    locator: the formulation of path synthesis as constrained minimization of a tracking error, with inequality constraints on the linkage
  - paper: "Imtiaz Ullah and Sridhar Kota, Optimal synthesis of mechanisms for path generation using Fourier descriptors and global search methods, ASME Journal of Mechanical Design 119(4), 1997, 504 to 510"
    locator: the Fourier descriptor error that compares the shape of the curve apart from its position, orientation and size, and the global search followed by a local method
  - paper: doi:10.1016/S0094-114X(02)00051-4
    title: J. A. Cabrera, A. Simón and M. Prado, Optimal synthesis of mechanisms with genetic algorithms, Mechanism and Machine Theory 37(10), 2002, 1165 to 1177
    locator: the genetic algorithm formulation of four-bar path synthesis (general locator)
  - paper: doi:10.1016/j.mechmachtheory.2009.03.003
    title: S. K. Acharyya and M. Mandal, Performance of EAs for four-bar linkage synthesis, Mechanism and Machine Theory 44(9), 2009, 1784 to 1794
    locator: the comparison of a genetic algorithm, particle swarm optimization and differential evolution on four-bar path synthesis test cases
  - paper: doi:10.5194/ms-13-79-2022
    title: Yao, Wang, Sun, Kong and Lin, Optimal synthesis of four-bar linkages for path generation using the individual repairing method, Mechanical Sciences 13, 2022, 79 to 87
    locator: the tracking error with free input angles, the Grashof, order and bound constraints, the repair of infeasible candidates instead of penalties, and the remarks on how earlier papers reported their errors
  - paper: "Charles W. Wampler, Alexander P. Morgan and Andrew J. Sommese, Complete solution of the nine-point path synthesis problem for four-bar linkages, ASME Journal of Mechanical Design 114(1), 1992, 153 to 159"
    locator: the 4326 four-bars (1442 cognate triples) through nine generic points, which are the zero-error designs of the nine-point problem
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, 2nd edition, Springer, 2006
    locator: Chapter 10, Least-Squares Problems (the Gauss-Newton and Levenberg-Marquardt methods and their local and global convergence)
---

Optimization-based dimensional synthesis chooses the dimensions of a linkage by minimizing a measure of how far its motion is from the task, instead of solving for exact precision points. The task usually gives more data than the linkage has free dimensions: twenty points on a path for a four-bar that has nine, a whole function over an interval, or a dozen poses of a part. Then no linkage meets the task exactly, and the designer picks three things: an error measure, a set of constraints that make the linkage buildable, and an optimizer. Fox and Willmert set the problem up this way in 1967, with inequality constraints, and since then many families of optimizers have been applied to it, from Gauss-Newton to genetic algorithms. It serves [path generation](/path-generation/), [function generation](/function-generation/) and [motion generation](/motion-generation/) alike.

The technique gives a design, not a certificate. A few things about the problem can be proved: what the error function looks like, why its minimum is never unique, and what local methods guarantee. Everything said about which optimizer works best is measured, on a handful of test cases that recur in the literature but are not a standard benchmark. This page keeps the two apart.

## In plain words

Exact methods make a linkage pass through a few chosen points and hope it behaves between them. Here you list many points, or the whole curve, and ask a computer to make the misses as small as possible.

You write down a score: how far the linkage's point is from each target, added up. You write down rules: the linkage must hold together, turn all the way round if it should, and never jam. Then a search program changes the link lengths and the pivot places to lower the score.

The score has many valleys. A program that walks downhill stops in the nearest one, so you start it from many places, or use a search that jumps about. Neither kind can promise the deepest valley. What you get is a good linkage, checked by drawing its whole motion, not a proof that it is the best.

## When it applies

- The task has more conditions than the linkage has free dimensions: more than nine points of a four-bar path without timing or five with timing (see [path generation](/path-generation/)), or more than five poses of a part (see [Burmester theory](/burmester-theory/)).
- The task is a curve or a function on an interval rather than a list of points, and the goal is a small error over all of it.
- The design must meet conditions that the exact methods cannot impose: a crank that turns fully (the [Grashof condition](/grashof-condition/)), a lower bound on the [transmission angle](/transmission-angle/), pivots inside a region, link ratios within limits.
- There are several goals at once, such as small error, small size and a good transmission angle.

The signals in a problem are words like "as close as possible", "within a tolerance over the range" and "best fit". The technique does not apply when every exact solution is wanted, as in [nine-point path synthesis](/nine-point-path-synthesis/), where [homotopy continuation](/homotopy-continuation/) is the tool.

## The template

The holes are the parameter vector PARAMS, the error measure ERROR, the constraints FEASIBLE, the global search SEARCH and the local method LOCAL. The input is the target data and the number $m$ of starts.

```pseudo id=main
FIT-LINKAGE(targets, PARAMS, ERROR, FEASIBLE, SEARCH, LOCAL, m)
L1  x ← PARAMS(targets)    ▷ the dimensions, plus one input angle per target when the timing is free
L2  define f(x):
L3      for each target j, assemble the linkage at its input angle θj on the chosen branch
L4      v ← total closure violation;  e ← ERROR(computed points, targets)
L5      return e + w·v + a penalty for each violated FEASIBLE condition
L6  S ← m start points (random in the bounds, from exact syntheses, or from a library)
L7  C ← SEARCH(f, S)    ▷ the global phase: evolutionary, swarm, annealing, or none
L8  for each c in C: c ← LOCAL(f, c)    ▷ Gauss-Newton or Levenberg-Marquardt when e is a sum of squares
L9  for each c in C: trace the full cycle; reject branch, order and circuit defects; check the Grashof type and transmission angle
L10 return the designs that pass, ranked by their measured error
```

Line L1 fixes what is optimized. For a [four-bar](/four-bar-linkage/) path generator the dimensions are the two ground pivots (4 reals), the input, coupler and output lengths (3 reals) and the coupler point in the coupler frame (2 reals), as on the [path generation](/path-generation/) page. With prescribed timing only the start angle of the input is added, if the data gives rotations rather than angles. Without timing every target $P_j$ gets its own input angle $\theta_j$, so $N$ targets give $9 + N$ unknowns.

Lines L2 to L5 are the objective. Line L3 is a position analysis: for a four-bar, the moving pivot of the output is the intersection of two circles, found by [vector loop closure](/vector-loop-closure/) or by the formula of the [four-bar](/four-bar-linkage/) page, and one of the two intersections is chosen by a fixed sign. If the circles do not meet, the linkage cannot be assembled at that angle, and line L4 measures by how much instead of failing. Line L5 adds the penalties. This is the [penalty method](/penalty-method/): the weight $w$ trades feasibility against error and is set by hand.

Lines L6 to L8 are the search. A local method alone finds the minimum nearest its start, so L6 supplies many starts and L7 may run a population method first. Line L9 is not optional. The objective only sees the targets and the sign chosen in L3, so a design can score well and still be useless: it may reach the targets on two different circuits, in the wrong order, or through a toggle position.

### The error measures

Write $C(x, \theta)$ for the coupler point of design $x$ at input angle $\theta$.

- **Path generation with timing.** $e = \sum_j |C(x, \theta_j) - P_j|^2$ with the $\theta_j$ fixed by the data. This is a [nonlinear least squares](/nonlinear-least-squares/) problem in the 9 or 10 dimensions.
- **Path generation without timing.** $e = \sum_j |C(x, \theta_j) - P_j|^2$ with the $\theta_j$ as unknowns. For fixed $x$, minimizing over $\theta_j$ gives the squared distance from $P_j$ to the part of the coupler curve traced on the chosen branch, because that part is exactly the set of values $C(x, \theta)$. So this error is a sum of squared point-to-curve distances.
- **Function generation.** $e = \sum_j (\psi(x, \varphi_j) - \psi_d(\varphi_j))^2$ or, for the largest error, $\max_j |\psi(x, \varphi_j) - \psi_d(\varphi_j)|$, the [minimax](/minimax-approximation/) form used on the [Chebyshev spacing](/chebyshev-spacing/) page.
- **Motion generation.** Position errors plus weighted angle errors of the coupler. An angle is not a length, so the weight carries a length scale, and changing it changes the optimum.

### What is proved

**The minimum is never unique for path generation.** By the [Roberts-Chebyshev theorem](/roberts-chebyshev-theorem/), every four-bar coupler curve is traced by two other four-bars, its cognates. Any error that depends only on the traced curve, such as the timing-free error above, takes the same value on all three. With timing, one cognate still matches: in the Roberts construction one of its grounded links stays parallel to the input crank of the original, so it turns through the same angles. A parametrization that allows either grounded link to be the input doubles the count again. For nine generic targets without timing, the zero-error designs over the complex numbers are the 4326 four-bars in 1442 cognate triples found by Wampler, Morgan and Sommese, and in their four examples between 21 and 120 of the 1442 triples are real. With $N < 9$ targets there are $9 + N$ unknowns and only $2N$ residuals, so the Jacobian has more columns than rows, the Gauss-Newton step is not unique, and the zero-error designs form, in general, a set of dimension $9 - N$.

**The objective is not smooth everywhere.** Where the two circles of line L3 do not meet, there is no linkage; where they touch, the output link and the coupler are in line, the derivative of the output angle with respect to the input is unbounded, and the [transmission angle](/transmission-angle/) is $0°$ or $180°$. For a Grashof crank-rocker the two signs of L3 are the two circuits, and the crank turns fully on each. For a non-Grashof linkage a single circuit passes through such a toggle, where the sign must change, so a fixed sign cuts the circuit in two. That is why L4 measures a violation and L9 checks the circuit.

**A minimum exists in a bounded box, and may not exist without one.** With the violation of L4 and the intersection clamped to the line of centres when the circles miss, the penalized objective is continuous away from two degenerate cases, coincident circle centres and a coupler of zero length. So on a closed bounded set of designs where those cases do not occur, it attains its minimum. Without bounds the infimum may be approached only as a pivot goes to infinity: a four-bar whose output link grows without limit, with its pivot moving away in a fixed direction, tends to a [slider-crank](/slider-crank-mechanism/). If the targets suit a slider-crank best, the four-bar optimizer drifts outward and never stops.

**Local methods find stationary points.** Gauss-Newton and Levenberg-Marquardt with a line search or trust region converge, under standard assumptions (bounded level sets, a Lipschitz Jacobian), to a point where the gradient is zero, which may be a local minimum that is not global. Near a zero-residual minimum with a full-rank Jacobian Gauss-Newton converges quadratically; with a large residual it may converge slowly or not at all (Nocedal and Wright, Chapter 10).

**Global methods have no finite guarantee.** [Genetic algorithms](/genetic-algorithm/), [differential evolution](/differential-evolution/), [particle swarm optimization](/particle-swarm-optimization/) and [simulated annealing](/simulated-annealing/) carry no guarantee of reaching the global minimum within a given number of evaluations. The [no free lunch theorem](/no-free-lunch-theorem/) says that, averaged over all objectives, no search beats another; it says nothing about linkage objectives in particular, which is why the comparisons below are measurements.

### What is measured

Cabrera, Simón and Prado (2002) solved four-bar path synthesis with a genetic algorithm. Acharyya and Mandal (2009) compared a genetic algorithm, particle swarm optimization and differential evolution on four-bar test cases. Yao and co-workers (2022) replaced penalties by a repair of infeasible candidates and took their test cases from those two papers. They also point out that the earlier papers reported their errors inconsistently, for example the square root of the tracking error in place of the error itself.

These and similar papers each measure a few test cases, and they differ in the error measure (squared, root, largest), in whether timing is prescribed, in the bounds on the variables, in how constraints are handled and in the number of evaluations. So their numbers cannot be compared from one paper to the next without recomputing. The same few test cases recur, but the sources cited here use no standard benchmark: no agreed set of problems, error definitions and budgets exists for linkage synthesis, and a claim that one optimizer is better rests on the cases and settings of the paper that makes it.

**An illustration, not a benchmark.** A small run made for this page shows the shape of the problem. The targets were 12 points of the coupler curve of the reference four-bar used on the [path generation](/path-generation/) page (ground pivots $(0,0)$ and $(9,0)$, input 15, coupler 5, output 13, coupler point at the midpoint of the coupler), at input angles from $30°$ to $90°$, an arc about 14.8 long. The timing was free, so there were 21 unknowns. Levenberg-Marquardt with a finite-difference Jacobian and a closure penalty was started from 40 random points. The final root mean square errors ran from about $6 \times 10^{-4}$ to several units. The best 15 were all below $1.3 \times 10^{-2}$, yet they were very different linkages, with input links from about 2 to 16 long and one ground pivot nearly 200 units from the arc. None reached the zero error of the reference linkage, which was a valid answer. A short arc is fitted closely by many linkages, and a fit to the targets alone says little about the curve outside them.

### Cost

One evaluation of $f$ costs one position analysis per target, $O(N)$ for a four-bar. A Gauss-Newton step with a finite-difference Jacobian costs $O(nN)$ evaluations of the analysis for $n$ unknowns, plus $O(n^2 N + n^3)$ arithmetic for the linear system. A population method costs its population size times its number of generations in evaluations of $f$. The budget, not the problem, decides when the search stops.

## Classic examples

- **Function generation past three points.** [Freudenstein's equation](/freudenstein-equation/) meets three precision points exactly. To make the largest error over the whole range small, the [Chebyshev spacing](/chebyshev-spacing/) design is used as a start and a search moves the dimensions or the precision points; the table on that page shows a simple pattern search beating the Chebyshev design.
- **Path generation with timing.** [Standard form dyad synthesis](/standard-form-dyad-synthesis/) gives a linkage through two or three of the points; the [Levenberg-Marquardt](/levenberg-marquardt/) method then fits all of them, with the dimensions as the only unknowns.
- **Path generation without timing.** For more than nine points the input angles become unknowns, and the run above shows the many nearly equal minima. Exact four-bars through nine of the points, from [nine-point path synthesis](/nine-point-path-synthesis/), are natural start points.
- **Evolutionary search.** Cabrera and co-workers used a [genetic algorithm](/genetic-algorithm/); Acharyya and Mandal compared it with [differential evolution](/differential-evolution/) and particle swarm optimization.
- **Motion generation with many poses.** [Burmester theory](/burmester-theory/) meets five poses exactly. With more, the dyads are fitted to all poses in least squares, often starting from Burmester solutions through five of them.
- **Six-bars.** A [Watt or Stephenson six-bar](/watt-and-stephenson-six-bar/) has more dimensions and more circuits. The template is the same, with a longer L1 and a harder L9.

## Variations

- **Error measures.** Least squares, the largest error, or a shape error. Ullah and Kota compared curves by Fourier descriptors, the coefficients of the [discrete Fourier transform](/discrete-fourier-transform/) of points sampled along the closed curve. The coefficients can be normalized so that position, orientation and size drop out, so the shape is fitted first and the placement afterwards.
- **Separating placement from shape.** In complex numbers, moving, turning and scaling a whole linkage maps every coupler point $z$ to $az + b$. With the input angles fixed, the best $a$ and $b$ for the targets solve the linear least squares problem $\min \sum_j |a z_j + b - P_j|^2$ in closed form. So four of the unknowns can be removed exactly, and only the shape is searched.
- **Constraint handling.** Penalties, the [augmented Lagrangian method](/augmented-lagrangian-method/), explicit inequality constraints as in Fox and Willmert, or repair of infeasible candidates as in Yao and co-workers.
- **Derivative-free local methods.** The Nelder-Mead simplex method keeps $n + 1$ trial points and replaces the worst one by its reflection through the centroid of the others, with expansions and contractions. It needs no derivatives, which suits objectives with kinks, but it has no general convergence guarantee, and McKinnon gave examples where it stalls at a point that is not stationary. See [derivative-free optimization](/derivative-free-optimization/).
- **Other global searches.** [Simulated annealing](/simulated-annealing/), [CMA-ES](/cma-es/), or many local runs from random starts.
- **Several goals.** Error, size and transmission angle traded against each other with a [multi-objective evolutionary algorithm](/multi-objective-evolutionary-algorithm/), which returns a set of designs none of which is better in every goal ([Pareto dominance](/pareto-dominance/)).
- **Optimizing the free choices of an exact method.** Exact synthesis often leaves free parameters, such as points on the Burmester curves or the free choices of the standard form. Searching over them keeps the precision points exact and optimizes a second goal.

## Pitfalls

- **Measuring only at the targets.** The error at the targets is what was minimized. Trace the whole cycle and measure the error along the curve, as in line L9.
- **Branch, circuit and order defects.** A design can reach its targets on two circuits, or in the wrong order when the input angles are free. Add the order of the $\theta_j$ as a constraint, and check the circuit.
- **Unbounded variables.** Without bounds a pivot can drift to infinity, as one did in the run above. Bound every dimension, and treat a design at a bound as a sign that another mechanism type may fit better.
- **Clustered targets.** Targets on a short arc constrain the curve weakly. Many different linkages fit them, and they differ away from the targets.
- **Penalty weight.** Too small a weight lets the optimizer use linkages that do not assemble; too large a weight makes cliffs in the objective that stop local methods.
- **Finite differences across a branch switch.** If a small step in the dimensions moves a target across a toggle, the finite-difference gradient is meaningless. Use steps that keep the sign of L3 and check the closure.
- **Comparing numbers across papers.** Check the error definition, the timing, the bounds and the budget before comparing two reported errors.
- **Calling the best run optimal.** Report the number of starts, the budget and the spread of results, not only the best value.

## Exercises

1. Prove that if a four-bar minimizes the timing-free path error, each of its two cognates also does. Which cognate keeps the timing, and why?
2. For fixed dimensions, show that a minimizing input angle $\theta_j$ inside its range satisfies $\operatorname{Re}\big(\overline{(C - P_j)}\,\partial C/\partial\theta\big) = 0$, so the error vector is perpendicular to the curve.
3. Derive the closed form of the placement fit $\min_{a, b} \sum_j |a z_j + b - P_j|^2$ and show that the minimizing $b$ makes the centroids agree.
4. Assume no four-bar coupler curve contains a segment of a straight line. Take twenty positions of the slider of a [slider-crank](/slider-crank-mechanism/) as targets, with its crank angles as the timing. Show that the infimum of the error over four-bars can be zero without being attained. What does an unbounded optimizer do?
5. Implement the template with Levenberg-Marquardt on twelve points of a coupler curve, run it from many starts, and plot the final errors. Then add bounds and the order constraint, and compare.

## References
