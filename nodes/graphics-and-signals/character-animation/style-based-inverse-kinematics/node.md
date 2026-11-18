---
tag: 1FCH43
kind: algorithm
slug: style-based-inverse-kinematics
name: Style-based inverse kinematics
aliases:
- style-based IK
area: graphics-and-signals/character-animation
level: research
summary: Solve inverse kinematics by choosing the most likely pose under a scaled Gaussian process latent variable model learned from motion capture.
solves: [inverse-kinematics]
model: real-ram
complexity:
  vars: {N: "the number of training poses", D: "the number of pose coordinates", d: "the latent dimension", I: "the number of optimizer iterations"}
  time: {training: "O(N^3 + N^2 D)", query: "O(I (N^2 + N D d + (D + d)^2))"}
  space: {extra: "O(N^2 + N D + (D + d)^2)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
prereqs: [inverse-kinematics, gaussian-process]
see_also: [damped-least-squares-inverse-kinematics, jacobian-pseudoinverse-method, bfgs, principal-component-analysis, kernel-trick, motion-retargeting, spacetime-constraints, verbs-and-adverbs]
sources:
  - paper: doi:10.1145/1015706.1015755
    title: "Keith Grochow, Steven L. Martin, Aaron Hertzmann and Zoran Popović, Style-based inverse kinematics, ACM Transactions on Graphics 23(3), SIGGRAPH 2004, pages 522 to 531"
    locator: "the SGPLVM kernel with its predictive mean and variance, the objective L_IK in equation (3), and the optimization with SQP and L-BFGS in Section 6.2"
---

Style-based inverse kinematics finds a pose of a character that meets a few constraints, such as a hand on a target, and also looks like the poses of a motion capture example.
Plain [inverse kinematics](/inverse-kinematics/) has many solutions for a redundant chain, and most of them look wrong for a human.
Grochow, Martin, Hertzmann and Popović (2004) learn a probability model of poses from the example, a scaled Gaussian process latent variable model (SGPLVM), and then return the pose of the highest likelihood that meets the constraints.
The same constraints give a different pose for a model learned from a different style, for example a throw or a walk.

## In plain words

Many poses put the hand at the same place, and the solver must choose one.
This method lets a set of example poses choose.
It learns a smooth map from a few hidden numbers, the latent point, to a full pose.
The map is a [Gaussian process](/gaussian-process/): at each latent point it gives a mean pose and a variance, and the variance is small near the examples and large far from them.
The cost of a pose has three parts.
It is small when the pose is near the mean pose, when the variance is small, and when the latent point is near the origin.
The solver moves the latent point and the pose together, so that the cost is small and the hand is at the target.
The result is a pose like the examples, not only a pose that reaches.

## The problem

The input is a trained model and the constraints.
The model has the latent points $x_1, \ldots, x_N \in \mathbb{R}^d$ of $N$ training poses $y_1, \ldots, y_N \in \mathbb{R}^D$, their mean $\mu$, a scale $w_k > 0$ for each pose coordinate, and the kernel
$$k(x, x') = \alpha \exp\left(-\tfrac{\gamma}{2} \lVert x - x' \rVert^2\right) + \delta_{x, x'} \beta^{-1}.$$
With $K_{ij} = k(x_i, x_j)$, $Y$ the centered poses as rows, and $k(x)$ the vector of $k(x, x_j)$, the model predicts at any latent point $x$ the mean pose and the variance
$$f(x) = \mu + Y^\top K^{-1} k(x), \qquad \sigma^2(x) = k(x, x) - k(x)^\top K^{-1} k(x).$$
The negative log likelihood of a pose $y$ at the latent point $x$ is, up to a constant,
$$L_{IK}(x, y) = \frac{\lVert W (y - f(x)) \rVert^2}{2 \sigma^2(x)} + \frac{D}{2} \ln \sigma^2(x) + \frac12 \lVert x \rVert^2,$$
with $W = \operatorname{diag}(w_k)$.
The constraints are written as $g(y) = p$ for the [forward kinematics](/forward-kinematics/) map $g$ of the end effector.
The output is the pair $(x, y)$ that minimizes $L_{IK}$ subject to the constraints.

The latent points and the hyperparameters $\alpha, \gamma, \beta, w$ are inputs here.
The paper learns them from the motion capture data by maximizing the likelihood of the model, which is a separate optimization done once per style.
The code in `impl/python` takes them as given, uses a planar chain of three links as the character, and replaces the hard constraint by the penalty $\frac{\lambda}{2} \lVert g(y) - p \rVert^2$.

## The algorithm

```pseudo id=main
STYLE-IK(model, target p, start x₀, weight λ)
L1  z ← (x₀, f(x₀));  H ← I
L2  E, ∇E ← objective at z
L3  repeat:
L4      L_IK(x, y) ← ‖W (y - f(x))‖² / (2σ²(x)) + (D/2) ln σ²(x) + ½‖x‖²
L5      E ← L_IK(x, y) + (λ/2) ‖g(y) - p‖²
L6      d ← -H ∇E;  halve the step t from 1 until E(z + t d) ≤ E(z) + 10⁻⁴ t dᵀ∇E
L7      z ← z + t d;  update H by the BFGS formula
L8  until ‖∇E‖ is small or the step is below the rounding level of z
L9  return z = (x, y)
```

Lines L4 and L5 are evaluated inside the objective of lines L2 and L6.
The gradient is analytic.
With $r = W (y - f(x))$, the gradient in $y$ is $W r / \sigma^2 + \lambda J^\top (g(y) - p)$, where $J$ is the Jacobian of $g$.
The gradient in $x$ uses $\nabla f$ and $\nabla \sigma^2 = -2 \nabla k(x)^\top K^{-1} k(x)$, and $\nabla k(x, x_j) = -\gamma (x - x_j) k(x, x_j)$.
The matrix $K^{-1}$ and the product $K^{-1} Y$ are computed once, when the model is built.

The paper solves the constrained problem with SQP, and also uses L-BFGS.
The code uses [BFGS](/bfgs/) with a [backtracking line search](/backtracking-line-search/) on the penalty form, which is simpler and enough for a small chain.
If the BFGS direction is not a descent direction, the code resets $H$ to the identity and takes the steepest descent direction.

## Example

The tests use a chain of three links of lengths 1, 0.8 and 0.6, with joint angles $y = (y_1, y_2, y_3)$.
The style is a curve of nine poses $y(s) = (0.2 + 0.8 s,\ 0.5 - 0.3 s + 0.2 s^2,\ 0.9 s)$ at $s = -1, -0.75, \ldots, 1$, with the latent point $x = s$ and $\alpha = 1$, $\gamma = 2$, $\beta = 1000$.

Put the target at the end effector of the training pose at $s = 0.5$, which is $y = (0.6, 0.4, 0.45)$.
From the start $x_0 = 0.25$ with $\lambda = 10^5$, BFGS takes 21 steps and returns $x = 0.5001$ and $y = (0.5999, 0.4003, 0.4496)$, which is the training pose.
Plain inverse kinematics, with minimum norm Newton steps from the training pose at $s = -1$, reaches the same target exactly, but with $y = (0.619, 0.781, -0.514)$.
That pose is valid for the chain, but it is not in the style.

A check value for a small model: two training poses $(0, 0, 0)$ and $(1, 2, 3)$ at the latents $-1$ and $1$, with $\alpha = \gamma = 1$ and $\beta = 100$.
At $x = 0$, the two kernel values are equal, so $f(0)$ is the mean $(0.5, 1, 1.5)$, and
$$\sigma^2(0) = 1.01 - \frac{2 e^{-1}}{1.01 + e^{-2}} \approx 0.3676.$$

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md).
- **The gradient is exact.** The formulas above follow from the chain rule, and the tests compare them with central differences.
- **The objective decreases.** Each accepted step satisfies the Armijo condition along a descent direction, so $E$ decreases at every step, and the method stops at a point where the gradient is small or no step decreases $E$ at the rounding level.
- **Without constraints, the pose is the mean pose.** With $\lambda = 0$, the minimizer in $y$ for a fixed $x$ is $y = f(x)$, and the problem reduces to minimizing $\frac{D}{2} \ln \sigma^2(x) + \frac12 \lVert x \rVert^2$ over $x$. The tests check this against a grid search.
- **The penalty approaches the constraint.** For a larger $\lambda$, the end effector error at the global minimizer does not increase. The tests check this for the local minima that the solver finds.

The objective is not convex, so the method finds a local minimum, as any gradient based solver of this problem.

## Complexity

The costs are in the real RAM model.
Building the model inverts $K$ in $O(N^3)$ and forms $K^{-1} Y$ in $O(N^2 D)$.
One evaluation of the objective costs $O(N^2)$ for $K^{-1} k(x)$ and $O(N D d)$ for $f$ and its gradient, plus $O(D)$ for the forward kinematics of a chain.
The BFGS update costs $O((D + d)^2)$.
With a bounded number of line search steps, a query with $I$ iterations costs $O(I (N^2 + N D d + (D + d)^2))$.
The cost grows with $N$, so for interactive use the model is built on a moderate number of poses, for example a subset of the frames of the motion capture.

## Properties

- Learned prior: the pose comes from a model of the example motion, not from a hand made cost such as the distance to a rest pose.
- Same constraints, different styles: changing the model changes the pose, without changing the constraints.
- Probabilistic: the variance tells how far a pose is from the data, and the cost grows when the solver leaves the data.
- Local: the solver finds a local minimum, which depends on the start.
- Smooth: the objective is smooth in $x$ and $y$, so gradient based solvers apply.

## Variants and improvements

- **Hard constraints.** Solve the constrained problem with SQP, as in the paper, instead of the penalty. The penalty with a large $\lambda$ is close, but it never meets the constraint exactly.
- **Learning the model.** Fit the latent points and the hyperparameters by maximizing the likelihood of the training data, starting from [principal component analysis](/principal-component-analysis/) of the poses.
- **Style interpolation.** Blend two learned models to get poses between two styles.
- **Dynamics.** Later work adds a model of motion in the latent space, so that a sequence of poses is likely as a motion and not only pose by pose.
- **Other priors.** A simple prior, such as the distance to a rest pose or a Gaussian on the joint angles, also chooses among the solutions, but it does not know the style.

## When to use it

Use style-based inverse kinematics when an animator or a game must pose a character from a few constraints, and the result must look like a known kind of motion.
It needs motion capture of the style, and a training step per style.
For a pose that only has to reach, plain solvers such as [damped least squares](/damped-least-squares-inverse-kinematics/) or the [Jacobian pseudoinverse](/jacobian-pseudoinverse-method/) are simpler and faster.
For a whole motion that meets constraints over time, see [spacetime constraints](/spacetime-constraints/) and [motion retargeting](/motion-retargeting/).

## Pitfalls

- **Local minima.** In the example, from the start $x_0 = 0$ the solver goes to $x \approx 1.54$, outside the training latents, with $E \approx -0.36$, while the start $x_0 = 0.25$ gives the training pose with $E \approx -9.61$. Start from the latent point of a training pose that is near the target.
- **Leaving the data.** Far from the training latents, $\sigma^2$ goes to $\alpha + \beta^{-1}$ and $f$ goes to the mean pose, so a far target gives a pose that is close to the mean and does not reach well.
- **Penalty weight.** A small $\lambda$ misses the target; a large $\lambda$ makes the problem badly conditioned and needs more iterations.
- **Joint angles.** The model is a Gaussian process on the pose coordinates, so the coordinates must be smooth in the motion, for example without jumps of $2\pi$ in the angles.
- **Cancellation in the variance.** $\sigma^2$ is a difference of two numbers close to $\alpha$, so near the training latents it has a large relative rounding error. Keep $\beta$ moderate.

## Implementations

## History

Inverse kinematics for characters used hand made costs for a long time, such as joint limits and the distance to a rest pose.
Lawrence introduced the Gaussian process latent variable model in 2003 and 2004 as a nonlinear form of probabilistic PCA.
Grochow, Martin, Hertzmann and Popović (2004) scaled it to poses, learned a model per style from motion capture, and used its likelihood as the cost of inverse kinematics, with an interactive solver.
Later work used Gaussian process models with dynamics for tracking people in video and for animation.

## References
