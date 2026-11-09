---
tag: QWQCF9
kind: algorithm
slug: proximal-gradient-method
name: Proximal gradient method
aliases:
- ISTA
- forward-backward splitting
- iterative shrinkage-thresholding algorithm
- proximal gradient descent
area: optimization/gradient-methods
level: advanced
summary: Alternates a gradient step on the smooth part with a proximal step on the nonsmooth part.
solves: [composite-minimization]
model: real-ram
complexity:
  vars: {n: the number of variables, k: the number of iterations, g: "the cost of one gradient of f plus one prox of h", ε: "the target accuracy F(x_k) - F* ≤ ε", R: "the distance from x_0 to the nearest minimizer", β: "the smoothness constant L_f of f (the step is 1/L_f)"}
  time: {worst: O(k (g + n))}
  space: {extra: Θ(n)}
  steps: {worst: "⌈β R^2 / (2ε)⌉"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1979
  people: [Pierre-Louis Lions, Bertrand Mercier, Gregory B. Passty, Ingrid Daubechies, Michel Defrise, Christine De Mol]
  note: Lions and Mercier (1979) and Passty (1979) studied forward-backward splitting for monotone operators; Daubechies, Defrise and De Mol (2004) proved convergence of iterative soft thresholding for sparse inverse problems.
prereqs: [composite-minimization, proximal-operator, gradient-descent]
see_also: [fista, projected-gradient-descent, proximal-point-method, admm, lasso-regression, coordinate-descent, backtracking-line-search, mirror-descent]
sources:
  - book: isbn:9781611974980
    title: Amir Beck, First-Order Methods in Optimization, SIAM, 2017
    locator: Chapter 10, The proximal gradient method (the sufficient decrease lemma, the O(1/k) rate in the convex case and the linear rate in the strongly convex case)
  - paper: doi:10.1137/080716542
    title: Amir Beck and Marc Teboulle, A fast iterative shrinkage-thresholding algorithm for linear inverse problems, SIAM Journal on Imaging Sciences 2(1), 2009
    locator: Section 3, Theorem 3.1 (the O(1/k) rate of ISTA with a constant step or with backtracking)
  - paper: doi:10.1137/050626090
    title: Patrick L. Combettes and Valérie R. Wajs, Signal recovery by proximal forward-backward splitting, Multiscale Modeling and Simulation 4(4), 2005
    locator: Section 3 (convergence of the forward-backward iteration with step sizes in (0, 2/L))
  - paper: doi:10.1002/cpa.20042
    title: Ingrid Daubechies, Michel Defrise and Christine De Mol, An iterative thresholding algorithm for linear inverse problems with a sparsity constraint, Communications on Pure and Applied Mathematics 57(11), 2004
    locator: pages 1413 to 1457, convergence of iterative soft thresholding
  - paper: doi:10.1007/s10107-012-0629-5
    title: Yurii Nesterov, Gradient methods for minimizing composite functions, Mathematical Programming 140(1), 2013
    locator: Sections 2 and 3 (the composite gradient mapping and the primal gradient method)
  - paper: doi:10.1137/0716071
    title: P. L. Lions and B. Mercier, Splitting algorithms for the sum of two nonlinear operators, SIAM Journal on Numerical Analysis 16(6), 1979
    locator: pages 964 to 979
  - paper: "Gregory B. Passty, Ergodic convergence to a zero of the sum of monotone operators in Hilbert space, Journal of Mathematical Analysis and Applications 72(2), 1979, pages 383 to 390"
    locator: the forward-backward iteration with averaging
---

The proximal gradient method minimizes a sum $F = f + h$, where $f$ is convex and smooth and $h$ is convex but possibly nonsmooth, such as the $\ell_1$ norm. Each step takes a [gradient descent](/gradient-descent/) step on $f$ and then applies the [proximal operator](/proximal-operator/) of $h$. With the step $1/L_f$, it reaches $F(x_k) - F^* \le L_f\lVert x_0 - x^*\rVert^2/(2k)$, the same rate as gradient descent on a smooth function, and it converges linearly when $f$ is strongly convex. For the $\ell_1$ norm it is called ISTA, the iterative shrinkage-thresholding algorithm.

## In plain words

Some objectives have two parts. One part is smooth, so its slope tells you which way is down. The other part has corners, like the sum of absolute values, which pulls small entries toward zero. A plain slope step does not work well at a corner.

The method handles each part with the tool that fits it. First it moves downhill on the smooth part, as plain gradient descent does. Then it fixes the result for the second part. It asks: which point is close to where I landed, but also makes the second part small? For the sum of absolute values, the answer is to move each entry toward zero by a fixed amount, and to set it to zero when it would cross zero. This is why the method finds solutions with many exact zeros.

## The problem

The input is the [composite minimization](/composite-minimization/) problem: minimize $F(x) = f(x) + h(x)$ over $x \in \mathbb{R}^n$. Here $f$ is convex and differentiable with an $L_f$-Lipschitz gradient ([smoothness](/smoothness/)), and $h$ is proper, closed and convex. The method needs an oracle for $\nabla f$ and for $\operatorname{prox}_{th}$. We assume that a minimizer $x^*$ exists, and we write $F^* = F(x^*)$ and $R = \lVert x_0 - x^*\rVert$.

Notation: $n$ is the number of variables, $k$ counts iterations, $L_f$ and $\mu$ are the smoothness and strong convexity constants of $f$, $\kappa = L_f/\mu$, and $\varepsilon$ is the target accuracy for $F(x_k) - F^*$.

## The algorithm

```pseudo id=main
PROXIMAL-GRADIENT(∇f, prox_h, x₀, t, K)     ▷ 0 < t ≤ 1/L_f
L1  for k ← 0 to K − 1 do
L2      y ← x_k − t ∇f(x_k)                  ▷ forward (gradient) step on f
L3      x_{k+1} ← prox_{t h}(y)              ▷ backward (proximal) step on h
L4  return x_K
```

The two steps together can be written as one minimization:

$$x_{k+1} = \operatorname*{argmin}_{u} \Big\{ f(x_k) + \langle \nabla f(x_k), u - x_k\rangle + \frac{1}{2t}\lVert u - x_k\rVert^2 + h(u) \Big\}.$$

So the method keeps $h$ exact and replaces $f$ by its quadratic upper model at $x_k$. For the lasso, $f(x) = \frac{1}{2}\lVert Ax - b\rVert^2$, $\nabla f(x) = A^\top(Ax - b)$, $L_f = \lambda_{\max}(A^\top A)$, and line L3 is soft thresholding by $t\lambda$. For $h = 0$ the method is gradient descent, and for $h$ the indicator of a convex set it is [projected gradient descent](/projected-gradient-descent/).

## Example

Take the lasso with $A = \begin{pmatrix} 2 & 0 \\ 1 & 1\end{pmatrix}$, $b = (2, 0.5)$ and $\lambda = 1$. Then $A^\top A = \begin{pmatrix} 5 & 1 \\ 1 & 1\end{pmatrix}$, with largest eigenvalue $3 + \sqrt{5} \approx 5.236$. We use the bound $L = \operatorname{tr}(A^\top A) = 6$, so $t = 1/6$. The solution is $x^* = (0.7, 0)$ with $F^* = 0.9$: at $x^*$, $A^\top(b - Ax^*) = (1, -0.2)$, so the first entry equals $\lambda \operatorname{sign}(0.7)$ and the second lies in $[-\lambda, \lambda]$.

Start at $x_0 = (0, 0)$. Then $\nabla f(x_0) = -A^\top b = (-4.5, -0.5)$ and line L2 gives $y = (0.75, 0.0833)$. Line L3 subtracts $t\lambda = 1/6$ in absolute value, so $x_1 = (0.5833, 0)$: the second entry is cut to zero in the first step.

| $k$ | $x_k$ | $F(x_k)$ | $F(x_k) - F^*$ | bound $L R^2/(2k)$ |
|---|---|---|---|---|
| 0 | (0, 0) | 2.125 | 1.225 | |
| 1 | (0.58333, 0) | 0.934028 | 3.40e-2 | 1.47 |
| 2 | (0.68056, 0) | 0.900945 | 9.45e-4 | 0.735 |
| 3 | (0.69676, 0) | 0.900026 | 2.63e-5 | 0.49 |
| 4 | (0.69946, 0) | 0.900001 | 7.29e-7 | 0.3675 |

The gap is far under the bound, because once the zero entry is fixed, the method is gradient descent on the one-variable problem $\frac{5}{2}x_1^2 - 4.5x_1 + x_1 + \text{const}$, and the error $0.7 - x_{k,1}$ drops by the factor $1 - 5/6 = 1/6$ in each step: $0.1167$, $0.0194$, $0.0032$. The bound $L R^2/(2k)$ is for the worst case over all problems.

## Correctness

The proof rests on one inequality for a single step with $t \le 1/L_f$: for every $z$,

$$F(x_{k+1}) \le F(z) + \frac{1}{2t}\big(\lVert x_k - z\rVert^2 - \lVert x_{k+1} - z\rVert^2\big).$$

It comes from the descent lemma for $f$, convexity of $f$, and the subgradient that the prox step gives for $h$. With $z = x_k$, it shows that $F$ decreases at each step. With $z = x^*$, it shows that the distance to $x^*$ does not grow, and the sum over $k$ steps telescopes to $\sum_{i=1}^k (F(x_i) - F^*) \le \lVert x_0 - x^*\rVert^2/(2t)$. Since $F(x_i)$ decreases, $F(x_k) - F^* \le \lVert x_0 - x^*\rVert^2/(2tk)$. A fixed point of the step is a minimizer, because it satisfies $0 \in \nabla f(x) + \partial h(x)$. The full proof, with the strongly convex case, is below.

## Complexity

Each iteration costs one gradient of $f$, one prox of $h$, and $O(n)$ vector work. For the lasso with a dense $m \times n$ matrix, the gradient costs $O(mn)$ and the prox $O(n)$.

- **Convex $f$.** With $t = 1/L_f$, $F(x_k) - F^* \le L_f R^2/(2k)$. So $\lceil L_f R^2/(2\varepsilon)\rceil$ iterations give accuracy $\varepsilon$. This is a sublinear rate, $O(1/k)$.
- **Strongly convex $f$.** With $t = 1/L_f$, $\lVert x_k - x^*\rVert^2 \le (1 - 1/\kappa)^k R^2$, a linear rate. So $O(\kappa\log(1/\varepsilon))$ iterations suffice.
- **Lower bound.** On smooth convex problems ($h = 0$), no first-order method can beat $\Omega(L_f R^2/k^2)$ in the worst case for $k$ up to about $n/2$ ([first-order lower bound](/first-order-lower-bound/)). [FISTA](/fista/) reaches $O(L_f R^2/k^2)$ for the composite problem, so the plain method is not optimal.
- **Space.** $\Theta(n)$ besides the data.

## Properties

- **Monotone.** $F(x_{k+1}) \le F(x_k) - \frac{1}{2t}\lVert x_{k+1} - x_k\rVert^2$. FISTA does not have this property.
- **Fejér monotone.** $\lVert x_{k+1} - x^*\rVert \le \lVert x_k - x^*\rVert$ for each minimizer $x^*$. The iterates converge to a minimizer (Combettes and Wajs 2005).
- **Sparse iterates for $\ell_1$.** Soft thresholding sets small entries to exactly zero, so the iterates are sparse, unlike the iterates of a subgradient method.
- **Rate does not depend on $h$.** The bound is the same as for gradient descent on $f$ alone. The nonsmooth part costs nothing in the rate, only one prox per step.

## Variants and improvements

- **Backtracking.** If $L_f$ is not known, start with a guess $L$, and multiply it by $\eta > 1$ until $f(x^+) \le f(x) + \langle\nabla f(x), x^+ - x\rangle + \frac{L}{2}\lVert x^+ - x\rVert^2$. The rate becomes $\eta L_f R^2/(2k)$ (Beck and Teboulle 2009, Theorem 3.1). See [backtracking line search](/backtracking-line-search/).
- **Larger steps.** The iterates still converge for $t < 2/L_f$, but the proof above needs $t \le 1/L_f$.
- **Acceleration.** [FISTA](/fista/) adds a momentum step and gets $O(1/k^2)$.
- **Bregman geometry.** Replace the squared distance by a [Bregman divergence](/bregman-divergence/), as in [mirror descent](/mirror-descent/).
- **Stochastic versions.** For a finite sum $f$, use a stochastic gradient in line L2. With [SVRG](/svrg/) or [SAGA](/saga/) gradients, the linear rate stays.
- **Block versions.** Update one block of coordinates at a time, as in [coordinate descent](/coordinate-descent/) for the lasso.

## When to use it

Use it when the objective is a smooth loss plus a simple regularizer or a simple constraint: lasso, group lasso, nonnegative least squares, logistic regression with an $\ell_1$ penalty. "Simple" means that the prox is cheap, usually $O(n)$. If the prox needs its own iterative solver, the method loses most of its appeal. When speed matters, use FISTA, which has the same cost per step.

## Pitfalls

- **Step too long.** With $t > 2/L_f$ the method can diverge. For the lasso, $L_f$ is the largest eigenvalue of $A^\top A$, not the largest entry of $A$. The trace or $\lVert A\rVert_F^2$ is a safe upper bound.
- **Wrong threshold.** The prox in line L3 is $\operatorname{prox}_{th}$, so the soft threshold is $t\lambda$, not $\lambda$.
- **Gradient of the wrong part.** The gradient in line L2 is of $f$ only. Adding a subgradient of $h$ there is a subgradient method, with a $O(1/\sqrt{k})$ rate.
- **Stopping on the step length alone.** A small $\lVert x_{k+1} - x_k\rVert$ is the norm of $t$ times the gradient mapping. It is a good test only relative to the scale of the problem.

## Implementations

## History

Forward-backward splitting for the sum of two monotone operators goes back to Lions and Mercier (1979) and Passty (1979). For sparse recovery, Daubechies, Defrise and De Mol (2004) proved that iterative soft thresholding converges. Combettes and Wajs (2005) gave the general convex framework with proximal operators. Beck and Teboulle (2009) proved the $O(1/k)$ rate for the function values and introduced the accelerated version, FISTA. Nesterov (2013) analyzed the same method as a gradient method for composite functions.

## References
