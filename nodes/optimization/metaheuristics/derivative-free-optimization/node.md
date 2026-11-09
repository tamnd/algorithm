---
tag: W0PN7Z
kind: concept
slug: derivative-free-optimization
name: Derivative-free optimization
aliases:
- direct search
- DFO
- zero-order methods
area: optimization/metaheuristics
level: advanced
summary: Methods that minimize a function using only its values, not its derivatives. Some, like pattern search, have convergence proofs for smooth functions; others, like Nelder and Mead, can fail.
prereqs: [black-box-optimization, gradient-descent, smoothness]
see_also: [finite-difference-method, coordinate-descent, cma-es, evolution-strategies, gaussian-process, hyperparameter-tuning, global-optimization, simulated-annealing]
sources:
  - book: doi:10.1137/1.9780898718768
    title: Andrew R. Conn, Katya Scheinberg and Luís N. Vicente, Introduction to Derivative-Free Optimization, SIAM, 2009
    locator: Chapter 2 (positive spanning sets and the cosine measure), Chapter 7 (directional direct search and its convergence), Chapter 8 (simplicial direct search and Nelder and Mead), Chapters 10 and 11 (trust-region methods with interpolation models)
  - paper: doi:10.1137/S003614450242889
    title: Tamara G. Kolda, Robert Michael Lewis and Virginia Torczon, Optimization by direct search, new perspectives on some classical and modern methods, SIAM Review 45(3), 2003
    locator: pages 385 to 482, Section 3 (the bound on the gradient after an unsuccessful poll, and global convergence of generating set search)
  - paper: doi:10.1093/comjnl/7.4.308
    title: John A. Nelder and Roger Mead, A simplex method for function minimization, The Computer Journal 7(4), 1965
    locator: pages 308 to 313
  - paper: doi:10.1137/S1052623496303482
    title: Ken I. M. McKinnon, Convergence of the Nelder-Mead simplex method to a nonstationary point, SIAM Journal on Optimization 9(1), 1998
    locator: pages 148 to 158 (a family of strictly convex functions in two dimensions on which the method fails)
  - paper: doi:10.1017/S0962492919000060
    title: Jeffrey Larson, Matt Menickelly and Stefan M. Wild, Derivative-free optimization methods, Acta Numerica 28, 2019
    locator: pages 287 to 404 (a survey of deterministic and randomized methods and their complexity bounds)
---

Derivative-free optimization (DFO) is the set of methods that minimize a function $f : \mathbb{R}^n \to \mathbb{R}$ using only its values $f(x)$, never its gradient. They are used when the gradient does not exist, cannot be computed, or is too noisy, which is the case when $f$ is the output of a simulation or an experiment. This is the [black-box](/black-box-optimization/) setting with a continuous domain. The main families are direct search, model-based methods, and randomized methods such as [evolution strategies](/evolution-strategies/) and [CMA-ES](/cma-es/). The guarantees differ by family and must be stated with their hypotheses: pattern search converges to stationary points of smooth functions, the Nelder and Mead method can fail even on a strictly convex function in two dimensions, and no method of this kind finds a global minimum in general.

## In plain words

You want the lowest point of a smooth landscape, but you cannot see the slope. You can only measure the height at points you choose. A simple plan is to step a fixed distance north, south, east and west, and to move to the first spot that is lower. If none is lower, you are close to a low point at the scale of your step, so you make the step shorter and try again.

Other plans fit a simple bowl to the heights you have measured and jump to its bottom, or throw a cloud of random points and move the cloud toward the lower ones. All of them use only heights.

## The idea

**Direct search with a set of directions.** Compass search, the simplest pattern search, keeps a point $x$ and a step $\alpha$. At each iteration it *polls* the $2n$ points $x \pm \alpha e_i$. If one of them has a lower value, it moves there. If none does, the poll is *unsuccessful* and it halves $\alpha$. It stops when $\alpha$ is below a tolerance.

The reason it works is a fact about the set $D = \{\pm e_1, \dots, \pm e_n\}$. Its *cosine measure* is
$$\kappa(D) = \min_{v \ne 0} \max_{d \in D} \frac{v^\top d}{\|v\| \|d\|} = \frac{1}{\sqrt{n}},$$
since the largest coordinate of a unit vector $v$ in absolute value is at least $1/\sqrt{n}$. So for every gradient $g \ne 0$ some $d \in D$ makes an angle with $-g$ whose cosine is at least $1/\sqrt{n}$, a descent direction. Any *positive spanning set* has $\kappa > 0$, and the same argument works with it.

**What an unsuccessful poll proves.** Let $\nabla f$ be Lipschitz with constant $L$ (see [smoothness](/smoothness/)), and assume that $f(x + \alpha d) \ge f(x)$ for all $d \in D$. Pick $d \in D$ with $-\nabla f(x)^\top d \ge \kappa \|\nabla f(x)\|$, and recall that $\|d\| = 1$. By the descent lemma,
$$f(x) \le f(x + \alpha d) \le f(x) + \alpha \nabla f(x)^\top d + \tfrac{L}{2}\alpha^2 \le f(x) - \alpha\kappa\|\nabla f(x)\| + \tfrac{L}{2}\alpha^2,$$
so
$$\|\nabla f(x)\| \le \frac{L\alpha}{2\kappa} = \frac{\sqrt{n}\, L\alpha}{2}.$$
The step size is a certificate: when $\alpha$ is small after an unsuccessful poll, the gradient is small. If the level set $\{f \le f(x_0)\}$ is bounded, and a step is accepted only on a decrease that is large enough, or on a rational lattice as in classical pattern search, then $\alpha \to 0$ along the unsuccessful iterations, and the gradient at those points tends to 0. This is the global convergence result of Torczon, and of Kolda, Lewis and Torczon. It is convergence to a *stationary point*, not to a global minimum.

**Simplex methods.** The Nelder and Mead method keeps $n + 1$ points, a simplex, and replaces the worst point by its reflection through the centroid of the others, with expansion and contraction steps. It is popular and often works well in low dimension, but it has no general convergence guarantee. McKinnon gave strictly convex functions of two variables on which it converges to a point that is not stationary. Lagarias, Reeds, Wright and Wright proved convergence for strictly convex functions of one variable.

**Model-based methods.** Fit a linear or quadratic model of $f$ to values at well-placed points, minimize the model in a trust region, and update the region by the ratio of the actual to the predicted decrease. With fully linear models, these methods have convergence results like those of gradient methods. Powell's NEWUOA and BOBYQA are widely used examples.

**Finite differences.** A forward difference $(f(x + h e_i) - f(x))/h$ costs $n$ values for a gradient and has an error of order $h$ from the curvature, plus an error of order $\epsilon_f/h$ from noise or rounding of size $\epsilon_f$. A good $h$ is near $\sqrt{\epsilon_f}$ for forward differences. With it, any [gradient method](/gradient-descent/) becomes derivative-free, see [finite difference method](/finite-difference-method/).

**Randomized methods.** Random search, [evolution strategies](/evolution-strategies/), [CMA-ES](/cma-es/), the [cross-entropy method](/cross-entropy-method/) and [simulated annealing](/simulated-annealing/) sample points from a distribution and adapt it. Some of them use only comparisons of values, which makes them invariant under increasing transformations of $f$.

## Examples

**Compass search on a quadratic.** Let $f(x, y) = (x - 0.3)^2 + 10(y + \pi)^2$, start at $(0, 0)$ with $\alpha = 1$, poll in the order $+e_1, -e_1, +e_2, -e_2$, move to the first point that is lower, and stop when $\alpha < 10^{-6}$. The run used 136 values of $f$ and 20 unsuccessful polls, and ended at $(0.2999992, -3.1415920)$ with $f = 4.5 \times 10^{-12}$. Here $L = 20$, and at each unsuccessful poll the ratio of $\|\nabla f(x)\|$ to the bound $\sqrt{2} \cdot 20 \alpha / 2$ was at most $0.70$, as the bound says it must be at most 1.

**Compass search on the Rosenbrock function.** On $f(x, y) = 100(y - x^2)^2 + (1 - x)^2$ from $(-1.2, 1)$, with the same rules, the run used 17371 values of $f$ and ended at $(0.99967, 0.99935)$ with $f = 1.07 \times 10^{-7}$. The narrow curved valley forces many short steps, since no coordinate direction follows it.

**The step of a finite difference.** For $f = \exp$ at $x = 1$, where $f' = e$, the error of the forward difference is $0.141$ for $h = 0.1$, $1.4 \times 10^{-4}$ for $h = 10^{-4}$, $6.6 \times 10^{-9}$ for $h = 10^{-8}$, and $4.3 \times 10^{-4}$ for $h = 10^{-12}$, where rounding dominates. In double precision $\sqrt{\epsilon_f}$ is about $10^{-8}$.

**A non-example.** Gradient descent with the exact gradient is not derivative-free, even if the gradient is cheap. Gradient descent with finite differences is.

## Where it is used

- **Simulation-based design.** Engineering design, where each value of $f$ is the output of a simulation code without derivatives.
- **[Hyperparameter tuning](/hyperparameter-tuning/).** The validation error of a learning method as a function of its settings, often with Bayesian optimization based on a [Gaussian process](/gaussian-process/).
- **Calibration.** Fitting the parameters of a model in physics, biology or economics to data, when the model is a program.
- **Noisy and nonsmooth problems.** Where gradients do not exist or are unreliable, direct search with a mesh, such as mesh adaptive direct search, has convergence results for nonsmooth $f$ in terms of generalized derivatives.
- **Policy search.** In reinforcement learning, evolution strategies are used as derivative-free optimizers of the return.

## References
