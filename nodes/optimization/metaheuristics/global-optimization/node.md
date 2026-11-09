---
tag: 59WBES
kind: problem
slug: global-optimization
name: Global optimization
aliases:
- global minimization
- function optimization
- global optimization problem
area: optimization/metaheuristics
level: intro
summary: Find a point where the objective takes its least value over the whole domain, not just a point that is best in its neighborhood. Hard in general, both in time and in the number of evaluations.
prereqs: [local-optimum, convex-function, lipschitz-condition]
see_also: [black-box-optimization, multimodal-optimization, interval-branch-and-bound, simulated-annealing, no-free-lunch-theorem, np-hard, gradient-descent, combinatorial-optimization-problem]
sources:
  - book: isbn:9783319915777
    title: Yurii Nesterov, Lectures on Convex Optimization, 2nd edition, Springer, 2018
    locator: Section 1.1.3 (the uniform grid method and the lower bound on the number of calls of a zero-order oracle for Lipschitz functions on a box)
  - paper: doi:10.1137/0709036
    title: Bruno O. Shubert, A sequential method seeking the global maximum of a function, SIAM Journal on Numerical Analysis 9(3), 1972
    locator: pages 379 to 388 (the sawtooth lower bound method for Lipschitz functions of one variable)
  - paper: doi:10.1007/BF00941892
    title: Donald R. Jones, Cary D. Perttunen and Bruce E. Stuckman, Lipschitzian optimization without the Lipschitz constant, Journal of Optimization Theory and Applications 79(1), 1993
    locator: pages 157 to 181 (the DIRECT algorithm)
  - paper: doi:10.1007/BF00120662
    title: Panos M. Pardalos and Stephen A. Vavasis, Quadratic programming with one negative eigenvalue is NP-hard, Journal of Global Optimization 1(1), 1991
    locator: pages 15 to 22
  - book: doi:10.1007/3-540-50871-6
    title: Aimo Törn and Antanas Žilinskas, Global Optimization, Lecture Notes in Computer Science 350, Springer, 1989
    locator: Chapter 1 (the classes of methods and the difficulty of the problem)
---

Global optimization is the problem of finding a point where an objective $f$ takes its least value over the whole domain, the global minimum, and not only a [local optimum](/local-optimum/), which is best only among nearby points. For a [convex function](/convex-function/) the two coincide, and the problem is easy. In general it is hard in two senses: some instances are [NP-hard](/np-hard/), and a method that sees only values of $f$ needs a number of evaluations that grows exponentially with the dimension, even when $f$ is [Lipschitz](/lipschitz-condition/). Exact methods use bounds on $f$; [metaheuristics](/metaheuristic/) such as [simulated annealing](/simulated-annealing/) give good points with no proof of optimality.

## In plain words

You want the lowest point of a whole landscape. Walking downhill takes you to the bottom of the valley you start in, but that may not be the lowest valley. To be sure you have the lowest one, you must in some way rule out every other valley.

This is easy when the landscape is a single bowl, since then every valley is the same valley. It is hard when there are many valleys. If you only learn the height at points you visit, a narrow deep hole can hide anywhere you did not look, and the number of places to look grows very fast with the number of directions.

## Definition

An instance is a set $D$, the domain, and a function $f : D \to \mathbb{R}$. Write $f^* = \inf_{x \in D} f(x)$.

- **Exact form.** Find $x^* \in D$ with $f(x^*) = f^*$, if one exists. It exists when $D$ is finite, or when $D$ is compact and $f$ is continuous.
- **Approximate form.** Given $\varepsilon > 0$, find $x \in D$ with $f(x) - f^* \le \varepsilon$.
- **Certified form.** Also return a lower bound $\ell \le f^*$ with $f(x) - \ell \le \varepsilon$, which proves that $x$ is an $\varepsilon$-approximate global minimum.

A point $x$ is a *local minimum* if $f(x) \le f(y)$ for all $y$ in a neighborhood of $x$, given by a metric on a continuous domain or by a move structure on a discrete one. Every global minimum is a local minimum, and the converse fails in general. Maximization is the same problem for $-f$.

The model of computation matters. In the *white-box* model, $f$ is given by a formula, so bounds on $f$ over a region can be computed. In the [black-box](/black-box-optimization/) model, an algorithm learns $f$ only through the values $f(x)$ at points that it chooses, and its cost is the number of such values.

## Variants

- **Continuous, box constrained.** $D = [a_1, b_1] \times \dots \times [a_n, b_n] \subset \mathbb{R}^n$, often with $f$ Lipschitz or smooth.
- **Combinatorial.** $D$ is finite but huge, as in the [traveling salesman problem](/traveling-salesman-problem/) or [maximum cut](/maximum-cut/), see [combinatorial optimization problem](/combinatorial-optimization-problem/).
- **Constrained.** $D = \{x : g_i(x) \le 0\}$ with nonconvex $g_i$.
- **Several optima.** Find all global minima, or many good local ones, see [multimodal optimization](/multimodal-optimization/).
- **Noisy.** Each evaluation returns $f(x)$ plus random noise.

## Examples

**The Rastrigin function.** $f(x) = 10n + \sum_{i=1}^n (x_i^2 - 10\cos(2\pi x_i))$ on $[-5.12, 5.12]^n$ has the global minimum $f(0) = 0$. In one dimension, a scan with step $10^{-4}$ finds 11 local minima, near the integers $-5, \dots, 5$, at $x \approx \pm 0.995, \pm 1.990, \dots, \pm 4.975$ with the values $0.995, 3.980, 8.955, 15.919, 24.874$. Since $f$ is a sum over the coordinates, a point is a local minimum exactly when each coordinate is, so the box has $11^n$ local minima and one global minimum. Gradient descent with step $0.001$ and 2000 steps from 100 uniform random starts (seeds 0 to 99) reached the global minimum from 16 starts for $n = 1$, from 1 start for $n = 2$ and from none for $n = 5$.

**A grid on a Lipschitz function.** Let $f(x) = |x - 0.3| + 0.5|\sin 7x|$ on $[0, 1]$. It is Lipschitz with $L = 1 + 3.5 = 4.5$. The grid of the $p$ cell centers $(2i - 1)/(2p)$ has a point within $1/(2p)$ of every $x$, so its best value is within $L/(2p)$ of $f^*$. For $\varepsilon = 0.1$, $p = \lceil L/(2\varepsilon) \rceil = 23$ points give the error $0.035$, measured against a scan with $10^6 + 1$ points, which gives $f^* \approx 0.1488$. For $\varepsilon = 0.01$, $p = 225$ points give the error $0.0053$.

**A convex non-example.** For $f(x) = \|x\|^2$, every local minimum is global, and gradient descent from any start converges to it. The global problem is no harder than the local one.

## Known algorithms

- **Exhaustive search** on a finite domain, exact and in time $|D|$.
- **Branch and bound.** Split the domain, compute a lower bound on each part, and discard the parts whose bound is above the best value found. [Interval branch and bound](/interval-branch-and-bound/) gets the bounds from interval arithmetic, and Lipschitz methods from $f(x) - L\|y - x\|$. The Piyavskii and Shubert method (1972) does this in one dimension, and DIRECT (Jones, Perttunen and Stuckman, 1993) works without knowing $L$.
- **Multistart.** Run a local method, such as [gradient descent](/gradient-descent/), from many random starts and keep the best result.
- **Bayesian optimization.** Fit a [Gaussian process](/gaussian-process/) to the values seen and choose the next point by an acquisition rule. Used when each value is expensive.
- **Metaheuristics.** [Simulated annealing](/simulated-annealing/), [threshold accepting](/threshold-accepting/), [genetic algorithms](/genetic-algorithm/), [differential evolution](/differential-evolution/), [CMA-ES](/cma-es/) and [particle swarm optimization](/particle-swarm-optimization/). They give no certificate. Simulated annealing with a logarithmic schedule has a convergence theorem, see [Hajek's theorem](/simulated-annealing-convergence/), which says nothing about a finite budget.

## Bounds

**Finite domain, black box.** With $|D| = N$ and no structure, a deterministic algorithm must evaluate all $N$ points to be sure of the minimum: if a point $z$ is never evaluated, the function that agrees with the values seen and has a lower value at $z$ gives the same run. On the $N$ needle functions, with one low point, every algorithm needs $(N + 1)/2$ evaluations on average to find it, see the [no free lunch theorem](/no-free-lunch-theorem/).

**Lipschitz functions on a box.** Let $f : [0, 1]^n \to \mathbb{R}$ satisfy $|f(x) - f(y)| \le L\|x - y\|_\infty$, and let $p = \lfloor L/(2\varepsilon) \rfloor \ge 1$. No method that sees only values can guarantee $f(x) - f^* < \varepsilon$ with fewer than $p^n$ values, counting the point it returns. *Proof.* Split the box into $p^n$ cubes of side $1/p$. With fewer than $p^n$ points, some cube has none of them in its interior. Answer $f = 0$ at every point that the method asks for. The function $f(x) = \min(0, L\|x - c\|_\infty - L/(2p))$, with $c$ the center of the empty cube, is $L$-Lipschitz, is 0 outside that open cube, and so agrees with every answer. Its minimum is $-L/(2p) \le -\varepsilon$, while the returned point has value 0, so the error is at least $\varepsilon$. $\square$ The grid of cell centers with $\lceil L/(2\varepsilon) \rceil$ points per coordinate reaches the error $\varepsilon$, so the bound is tight up to the rounding in each coordinate. For $L = 1$, $\varepsilon = 0.01$ and $n = 10$, this is $50^{10} \approx 10^{17}$ values. Nesterov gives this bound in Section 1.1.3 of his book.

**Hardness in the white-box model.** Minimizing a quadratic function over a box is NP-hard, see the reduction below, and Pardalos and Vavasis showed that it stays NP-hard when the matrix has only one negative eigenvalue. So no polynomial time algorithm is known for the exact problem in general, and none exists unless P = NP.

**Convex case.** If $D$ and $f$ are convex, every local minimum is global, and methods such as gradient descent and interior point methods reach accuracy $\varepsilon$ in a number of steps that grows like a polynomial in $\log(1/\varepsilon)$ or $1/\varepsilon$ under standard assumptions, see [convergence rate](/convergence-rate/).

## Reductions

- **Maximum cut to a quadratic over a box.** For a graph with weights $w_{ij} \ge 0$, the maximum cut is $\max_{s \in \{-1, 1\}^n} \tfrac{1}{2}\sum_{i<j} w_{ij}(1 - s_i s_j)$. The function $q(x) = \tfrac{1}{2}\sum_{i<j} w_{ij}(1 - x_i x_j)$ is affine in each $x_i$ when the others are fixed, so its maximum over $[-1, 1]^n$ is reached at a vertex, which is a point of $\{-1, 1\}^n$. So the global maximum of $q$ over the box is the maximum cut, and a global minimizer of $-q$ gives a maximum cut. Since [maximum cut](/maximum-cut/) is NP-hard, so is this global problem.
- **Constraints to penalties.** $\min\{f(x) : g(x) \le 0\}$ becomes $\min f(x) + \mu \max(0, g(x))$, exact for a large $\mu$ under conditions on $f$ and $g$.
- **Integer variables.** $x_i \in \{0, 1\}$ is the same as the nonconvex constraint $x_i(1 - x_i) = 0$, so integer programming is a special case.

## Applications

Global optimization appears in molecular conformation and protein folding (the least energy state), in the calibration of models with many parameters, in the design of circuits and structures, in the tuning of the [hyperparameters](/hyperparameter-tuning/) of learning methods, in chemical process design, and in finding the ground state of spin systems such as the [Ising model](/ising-model/).

## References
