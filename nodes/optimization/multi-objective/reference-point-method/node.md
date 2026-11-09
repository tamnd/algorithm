---
tag: 28JK3G
kind: technique
slug: reference-point-method
name: Reference point method
aliases:
- reference point approach
- aspiration point method
- Wierzbicki reference point method
area: optimization/multi-objective
level: advanced
summary: Steers the search toward a user-specified reference point in objective space. In each round one achievement solve projects the point onto the Pareto front.
prereqs: [achievement-scalarizing-function, preference-articulation]
see_also: [weighted-tchebycheff-method, ideal-point, nadir-point, nsga-iii, scalarization]
sources:
  - paper: doi:10.1007/978-3-642-48782-8_32
    title: Andrzej P. Wierzbicki, The use of reference objectives in multiobjective optimization, in Multiple Criteria Decision Making Theory and Application, Lecture Notes in Economics and Mathematical Systems 177, Springer, 1980
    locator: pages 468 to 486 (the reference point approach and its achievement functions)
  - book: isbn:9780792382782
    title: Kaisa Miettinen, Nonlinear Multiobjective Optimization, Kluwer, 1999
    locator: Part II, Chapter 5 (interactive methods, the reference point method and classification-based methods)
  - book: doi:10.1007/978-3-540-88908-3
    title: Jürgen Branke, Kalyanmoy Deb, Kaisa Miettinen and Roman Słowiński (editors), Multiobjective Optimization, Interactive and Evolutionary Approaches, Lecture Notes in Computer Science 5252, Springer, 2008
    locator: Chapter 2 (introduction to interactive approaches)
  - paper: doi:10.1007/BF02591870
    title: Ralph E. Steuer and Eng-Ung Choo, An interactive weighted Tchebycheff procedure for multiple objective programming, Mathematical Programming 26(3), 1983
    locator: pages 326 to 344 (an interactive procedure based on weights instead of reference points)
---

The reference point method of Wierzbicki (1980) is an interactive method for [multi-objective optimization](/multi-objective-optimization/). The decision maker states aspiration levels for the objectives, a reference point $\bar{z}$. One solve of an [achievement scalarizing function](/achievement-scalarizing-function/) projects $\bar{z}$ onto the [Pareto front](/pareto-front/) and returns a Pareto optimal point. The decision maker looks at the answer, moves $\bar{z}$, and repeats until satisfied. No weights are asked for, and no part of the front is out of reach.

## In plain words

You tell the computer what you would like, for example "cost 500, delivery in 3 days". The computer shows you the best real option that comes closest to that wish. If your wish was too much, the option falls short of it a little in each goal. If your wish was modest, the option beats it.

Now you change your wish. Perhaps you accept a higher cost to get faster delivery. The computer shows a new option. After a few rounds you have learned what is possible, and you stop at an option you like.

You never have to say how much one goal is worth against another. You only say what you hope for.

## When it applies

**Convention.** All objectives are minimized unless a page says otherwise. The number of objectives is $p \ge 2$, $y = f(x)$ is the image of $x \in X$, and $Y = f(X)$. The achievement function is $s(y; \bar{z}, w, \rho) = \max_i w_i (y_i - \bar{z}_i) + \rho \sum_i w_i (y_i - \bar{z}_i)$ with $w > 0$ and a small $\rho > 0$.

Use it when:

- a person who decides is available during the search and can react to answers (see [preference articulation](/preference-articulation/));
- the decision maker can name levels of the objectives more easily than weights;
- each single-objective solve is cheap enough to run while the decision maker waits;
- the front is too large, or has too many objectives, to compute and show in full.

**Properties of each round.** These follow from the [achievement scalarizing function](/achievement-scalarizing-function/) page.

1. With $\rho > 0$, each answer is Pareto optimal. With $\rho = 0$, each answer is weakly Pareto optimal.
2. Every Pareto optimal point $\hat{y}$ is the answer to the reference point $\bar{z} = \hat{y}$ with $\rho = 0$. So the decision maker can reach any point of the front, supported or not.
3. With $\rho = 0$, the optimal value is $\le 0$ exactly when some attainable point is at least as good as $\bar{z}$ in every objective. The method can tell the decision maker whether the wish was realistic.

**What the method does not promise.** The method does not converge by itself. The decision maker can move $\bar{z}$ in any direction in each round, and the method follows. It stops when the decision maker is satisfied. This is on purpose: the decision maker's preferences are allowed to change as they learn about the problem. The quality of the result depends on the decision maker, and comparisons of interactive methods need experiments with people or with a simulated decision maker.

## The template

```pseudo id=main
REFERENCE-POINT-METHOD(X, f, w, ρ)
L1  compute the ideal point y^I and an estimate of the nadir point y^N; show the ranges [y^I_i, y^N_i]
L2  ask the decision maker for a reference point z̄
L3  loop
L4      x̂ ← a minimizer of s(f(x); z̄, w, ρ) over X         ▷ one achievement solve
L5      show f(x̂), and whether z̄ was attainable
L6      if the decision maker accepts f(x̂) then return x̂
L7      ask the decision maker for a new reference point z̄
```

The holes are the weights $w$, usually $w_i = 1/(y^N_i - y^I_i)$ with the [ideal point](/ideal-point/) and the [nadir point](/nadir-point/), and the way the decision maker is asked in lines L2 and L7.

**Cost.** One single-objective solve per round, plus $p$ solves for the ideal point and an estimate of the nadir point. The number of rounds depends on the decision maker, and is typically small.

### A worked example

Take $a = (2, 9)$, $b = (3, 6)$, $c = (4, 7)$, $d = (5, 4)$, $e = (7, 3)$, $f = (8, 5)$ and $g = (9, 1)$. Line L1 shows the ranges $[2, 9]$ for the first objective and $[1, 9]$ for the second. Take $w = (1, 1)$ and $\rho = 0$ for clear numbers.

| round | reference point | values at $a, b, c, d, e, f, g$ | answer | the decision maker's reaction |
|---|---|---|---|---|
| 1 | $(4, 4)$ | $5, 2, 3, 1, 3, 4, 5$ | $d = (5, 4)$, value 1: not attainable | wants a smaller second objective |
| 2 | $(6, 2)$ | $7, 4, 5, 2, 1, 3, 3$ | $e = (7, 3)$, value 1: not attainable | asks whether $(8, 8)$ can be beaten |
| 3 | $(8, 8)$ | $1, -2, -1, -3, -1, 0, 1$ | $d = (5, 4)$, value $-3$: attainable | goes back to $e$ and accepts it |

In round 2 the method returns $e$, an unsupported point that no weighted sum finds. In round 3 the negative value shows that the wish was modest: $d$ beats it by at least 3 in each objective.

## Classic examples

- **Wierzbicki's reference point method (1980).** The template, with an order-approximating achievement function. In the version described by Miettinen, each round also shows $p$ more points, the projections of $\bar{z} + \delta e_j$ for $j = 1, \ldots, p$, where $e_j$ is the $j$-th unit vector and $\delta$ is the distance from $\bar{z}$ to the answer, so that the decision maker sees nearby alternatives.
- **The interactive weighted Tchebycheff procedure.** Steuer and Choo (1983) ask the decision maker to choose among a few points found with sampled weights, and then narrow the weight region. The [weighted Tchebycheff method](/weighted-tchebycheff-method/) is the achievement function with a fixed utopia point.
- **Classification methods.** Methods such as NIMBUS ask the decision maker to sort the objectives into those to improve, those to keep and those that may get worse. The classification is turned into a reference point or a set of bounds, and one solve follows (Miettinen, Part II, Chapter 5).
- **Reference points in evolutionary methods.** [NSGA-III](/nsga-iii/) and preference-based versions of [NSGA-II](/nsga-ii/) use reference points to focus a population on the part of the front that the decision maker cares about.

## Variations

- **Reservation levels.** The decision maker gives two points: aspiration levels and the worst acceptable levels. The achievement function is then piecewise linear in each objective, with a steeper slope beyond the reservation level.
- **Directions instead of points.** Moving $\bar{z}$ along a line and solving at many steps gives a path on the front that the decision maker can follow.
- **Approximation first.** If the front can be computed in advance, for example with an evolutionary method, the rounds can work on the stored points. Each round then costs a scan instead of a solve, but the answers are only approximately Pareto optimal.

## Pitfalls

- **Weakly Pareto optimal answers.** With $\rho = 0$ the solver can return a dominated point. Use $\rho > 0$ or a second stage.
- **Bad scaling.** Without weights from the ranges, the objective with the largest numbers decides the answer. A wrong nadir estimate gives wrong weights, and for $p \ge 3$ the estimate is often wrong.
- **Anchoring.** The decision maker may stop early near the first answer. Show the ranges first, and offer the shifted reference points of Wierzbicki to show alternatives.
- **No convergence proof.** Do not expect the rounds to settle on their own. The method is a tool for learning, and the decision maker must stop it.

## Exercises

1. Show that if the decision maker always gives a reference point that is a point of the front, the method returns that point when $\rho = 0$. *Answer:* this is property 2: the value at $\hat{y}$ is 0, no point has a negative value, and every optimum $y$ satisfies $y \leqq \hat{y}$, so $y = \hat{y}$.
2. In the example, which reference points on the line $\bar{z} = (t, t)$ return $d$ with $w = (1, 1)$ and $\rho = 0$? *Answer:* all of them. The value of a point $y$ is $\max(y_1, y_2) - t$, so the answer minimizes $\max(y_1, y_2)$, which is 5 at $d$ and at least 6 elsewhere.

## References
