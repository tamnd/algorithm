---
tag: JY6DNX
kind: algorithm
slug: chambolle-pock-algorithm
name: Chambolle-Pock algorithm
aliases:
- primal-dual hybrid gradient
- PDHG
- Chambolle-Pock primal-dual algorithm
area: imaging-and-inverse-problems/variational-and-learned-reconstruction
level: advanced
summary: Solve min F(Kx) + G(x) by alternating proximal steps on the primal and dual variables with an extrapolation, using only K and its adjoint.
solves: [image-denoising, image-deblurring]
model: real-ram
complexity:
  vars: {N: the number of iterations, n: the number of primal unknowns, m: the number of dual unknowns, k: the cost of one product with K and one with its adjoint, p: the cost of the two proximal steps}
  time: {worst: O(N (k + p))}
  space: {extra: O(m + n)}
properties: {deterministic: true, exact: false, iterative: true, matrix_free: true, ergodic_rate: O(1/N)}
history:
  year: 2011
  people: [Antonin Chambolle, Thomas Pock]
  note: Pock, Cremers, Bischof and Chambolle used the method in 2009 for the Mumford-Shah functional. Chambolle and Pock (2011) proved convergence for tau sigma ||K||^2 < 1, the ergodic O(1/N) rate and the accelerated variants. Esser, Zhang and Chan (2010) placed it in the family of primal-dual hybrid gradient methods of Zhu and Chan.
prereqs: [proximal-operator, convex-conjugate, fenchel-duality, total-variation-denoising]
see_also: [admm, proximal-gradient-method, split-bregman-method, augmented-lagrangian-method, total-generalized-variation, learned-primal-dual, minimax-theorem, lasso-regression]
sources:
  - paper: doi:10.1007/s10851-010-0251-1
    title: Antonin Chambolle and Thomas Pock, A first-order primal-dual algorithm for convex problems with applications to imaging, Journal of Mathematical Imaging and Vision 40(1), 2011
    locator: pages 120 to 145 (Algorithm 1 and Theorem 1 for convergence and the ergodic O(1/N) bound; Algorithm 2 and Theorem 2 for strongly convex G)
  - paper: doi:10.1137/09076934X
    title: Ernie Esser, Xiaoqun Zhang and Tony F. Chan, A general framework for a class of first order primal-dual algorithms for convex optimization in imaging science, SIAM Journal on Imaging Sciences 3(4), 2010
    locator: pages 1015 to 1046
  - paper: doi:10.1017/S096249291600009X
    title: Antonin Chambolle and Thomas Pock, An introduction to continuous optimization for imaging, Acta Numerica 25, 2016
    locator: pages 161 to 319
  - paper: doi:10.1137/100814494
    title: Bingsheng He and Xiaoming Yuan, Convergence analysis of primal-dual algorithms for a saddle-point problem, from contraction perspective, SIAM Journal on Imaging Sciences 5(1), 2012
    locator: pages 119 to 149 (the method as a proximal point step in a fixed metric)
  - paper: doi:10.1016/0167-2789(92)90242-F
    title: Leonid I. Rudin, Stanley Osher and Emad Fatemi, Nonlinear total variation based noise removal algorithms, Physica D 60(1-4), 1992
    locator: pages 259 to 268
---

The Chambolle-Pock algorithm solves convex problems of the form $\min_x F(Kx) + G(x)$, where $K$ is a linear operator and $F$ and $G$ are convex functions whose [proximal operators](/proximal-operator/) are cheap. It works on the saddle point form $\min_x \max_y \langle Kx, y\rangle + G(x) - F^*(y)$, with the [convex conjugate](/convex-conjugate/) $F^*$, and alternates a proximal ascent step in the dual variable $y$ with a proximal descent step in the primal variable $x$. An extrapolation $\bar x = 2x^{n+1} - x^n$ between the two steps is what makes it converge. It needs only products with $K$ and its adjoint $K^*$, never a linear solve, and it converges for every pair of steps with $\tau\sigma\|K\|^2 < 1$. The averages of the iterates have a primal-dual gap of $O(1/N)$ after $N$ steps. In imaging it is the standard solver for total variation, [total generalized variation](/total-generalized-variation/) and other nonsmooth models with a forward operator.

## In plain words

Many image problems have two parts: one part that wants the image to fit the measurements, and one part that wants the image to look clean, for example to have few edges. Each part is easy alone, but together they are hard, because the clean part acts on the edges of the image and not on its pixels. The method keeps two unknowns: the image, and a helper that lives on the edges and says how much each edge costs. It takes turns. The helper looks at the current image and updates its prices. Then the image takes a small step against those prices and toward the measurements. Before the helper looks again, the image is pushed a little further in the direction it just moved. This small push is the key detail. Without it the two turns can chase each other in circles.

## The problem

Minimize $F(Kx) + G(x)$ over $x \in \mathbb{R}^n$, where:

- $K : \mathbb{R}^n \to \mathbb{R}^m$ is linear with norm $L = \|K\|$, given as two routines for $Kx$ and $K^*y$;
- $F : \mathbb{R}^m \to (-\infty, \infty]$ and $G : \mathbb{R}^n \to (-\infty, \infty]$ are closed, proper and convex, given by routines for $\operatorname{prox}_{\sigma F^*}$ and $\operatorname{prox}_{\tau G}$;
- the saddle function $\mathcal{L}(x, y) = \langle Kx, y\rangle + G(x) - F^*(y)$ has a saddle point $(x^*, y^*)$, so $x^*$ solves the primal problem and $y^*$ solves the dual problem $\max_y -F^*(y) - G^*(-K^*y)$ (see [Fenchel duality](/fenchel-duality/)).

The proximal step of the conjugate comes from the one of $F$ by Moreau's identity, $\operatorname{prox}_{\sigma F^*}(v) = v - \sigma\operatorname{prox}_{F/\sigma}(v/\sigma)$. The input is the routines, a start $(x^0, y^0)$, steps $\tau, \sigma > 0$ with $\tau\sigma L^2 < 1$ and a number of iterations $N$. The output is the last iterates and their averages.

The main example is total variation denoising, $\min_x \tfrac12\|x - f\|^2 + \lambda\sum_{ij}|(\nabla x)_{ij}|$. Here $K = \nabla$ (forward differences), $G(x) = \tfrac12\|x - f\|^2$ with $\operatorname{prox}_{\tau G}(v) = (v + \tau f)/(1 + \tau)$, and $F(q) = \lambda\sum|q_{ij}|$, whose conjugate is the indicator of $\{|y_{ij}| \le \lambda\}$, so $\operatorname{prox}_{\sigma F^*}$ projects each pixel pair onto the disk of radius $\lambda$. In two dimensions $\|\nabla\|^2 \le 8$, so $\tau = \sigma = 0.35$ is a valid choice ($0.35^2 \cdot 8 = 0.98 < 1$). The weight $\lambda$ is a design choice tuned for the class of images.

## The algorithm

```pseudo id=main
ChambollePock(K, K*, prox_τG, prox_σF*, x⁰, y⁰, τ, σ, N)
L1  x ← x⁰, y ← y⁰, x̄ ← x⁰, X ← 0, Y ← 0
L2  for n = 1 to N
L3      y ← prox_σF*(y + σ K x̄)             ▷ dual ascent step
L4      x_old ← x
L5      x ← prox_τG(x - τ K* y)              ▷ primal descent step
L6      x̄ ← x + θ (x - x_old)               ▷ extrapolation, θ = 1
L7      X ← X + x, Y ← Y + y
L8  return x, y, X / N, Y / N
```

Line L3 is a proximal step that increases $\mathcal{L}(\bar x, \cdot)$, and line L5 is a proximal step that decreases $\mathcal{L}(\cdot, y)$. Line L6 uses the new and the old primal iterate to predict the next one; with $\theta = 0$ the method is the Arrow-Hurwicz method, which has no convergence guarantee for these step sizes. Line L7 keeps the ergodic averages for which the rate is proved. Some texts write the primal step first: $x^{k+1} = \operatorname{prox}_{\tau G}(x^k - \tau K^*y^k)$, then $\bar x = 2x^{k+1} - x^k$, then the dual step with $\bar x$. This produces the same iterates with the dual index shifted by one.

## Example

Denoise the one-row signal $f = (0, 0, 3, 3)$ with $\lambda = 1$. Here $K$ is the difference operator with three active entries, $Kx = (x_2 - x_1, x_3 - x_2, x_4 - x_3)$, and $\|K\|^2 \le 4$, so $\tau = \sigma = 0.45$ is valid ($0.45^2 \cdot 4 = 0.81$). Start with $x^0 = f$ and $y^0 = 0$.

Step 1: $K\bar x = (0, 3, 0)$, so the dual step projects $0.45 \cdot (0, 3, 0) = (0, 1.35, 0)$ onto $[-1, 1]$ and gives $y = (0, 1, 0)$. Then $K^*y = (0, -1, 1, 0)$ and $x - \tau K^*y = (0, 0.45, 2.55, 3)$. The primal step averages this with $f$: $x = ((0, 0.45, 2.55, 3) + 0.45 f)/1.45 = (0, 0.3103, 2.6897, 3)$. The edge has started to shrink, and the dual entry at the edge already sits at its bound $\lambda = 1$.

| $n$ | $x$ | $y$ | energy |
|---|---|---|---|
| 1 | $(0, 0.3103, 2.6897, 3)$ | $(0, 1, 0)$ | 3.0963 |
| 2 | $(0.0867, 0.4377, 2.5623, 2.9133)$ | $(0.2793, 1, 0.2793)$ | 3.0257 |
| 3 | $(0.2012, 0.4708, 2.5292, 2.7988)$ | $(0.4556, 1, 0.4556)$ | 2.8598 |
| 5 | $(0.3863, 0.4577, 2.5423, 2.6137)$ | $(0.5638, 1, 0.5638)$ | 2.5861 |
| 10 | $(0.4937, 0.4819, 2.5181, 2.5063)$ | $(0.4992, 1, 0.4992)$ | 2.5358 |
| 20 | $(0.4997, 0.4997, 2.5003, 2.5003)$ | $(0.5001, 1, 0.5001)$ | 2.5001 |

The solution is $x^* = (0.5, 0.5, 2.5, 2.5)$ with energy $\tfrac12 \cdot 4 \cdot 0.25 + 2 = 2.5$, and $y^* = (0.5, 1, 0.5)$. This is $-\lambda$ times the dual field of [Chambolle's projection algorithm](/chambolle-projection-algorithm/) on the same signal. After 100 steps the averaged iterate is only $(0.4833, 0.4944, 2.5056, 2.5167)$, while the last iterate has been exact to many digits since about step 50. The rate theorem is for the averages, but on this kind of problem the last iterate is usually much better; this is a measurement, not a theorem.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The two proximal steps are subgradient inequalities for $F^*$ and $G$. Adding them and using the identity $2\langle a - b, c - b\rangle = \|a - b\|^2 + \|c - b\|^2 - \|a - c\|^2$ gives, for every $(x, y)$, a bound on $\mathcal{L}(x^{n+1}, y) - \mathcal{L}(x, y^{n+1})$ by a difference of the weighted distances $\|x - x^n\|^2/(2\tau) + \|y - y^n\|^2/(2\sigma)$ at steps $n$ and $n+1$, plus the cross term $\langle K(x^{n+1} - \bar x^n), y - y^{n+1}\rangle$. With the extrapolation, the cross term telescopes up to a remainder bounded by $L\sqrt{\tau\sigma}$ times squared step lengths, and the condition $L\sqrt{\tau\sigma} \le 1$ makes the remainder harmless. Summing and using convexity gives, for every $(x, y)$,

$$\mathcal{L}(X_N, y) - \mathcal{L}(x, Y_N) \le \frac1N\left(\frac{\|x - x^0\|^2}{2\tau} + \frac{\|y - y^0\|^2}{2\sigma}\right),$$

with the averages $X_N$ and $Y_N$ of line L8 (Theorem 1 of Chambolle and Pock). With strict inequality $\tau\sigma L^2 < 1$, the same sum at a saddle point shows that the iterates are bounded and the step lengths are square summable. Limit points satisfy the fixed point equations of lines L3 and L5, so they are saddle points, and a restart of the sum at such a limit point shows that the whole sequence converges.

## Complexity

Each iteration costs one product with $K$, one with $K^*$, the two proximal steps and $O(m + n)$ vector operations. For total variation on an image with $P$ pixels all of these are $O(P)$, so $N$ iterations cost $O(NP)$ time and $O(P)$ extra memory. The number of iterations for a gap $\varepsilon$ is $O(1/\varepsilon)$ by the ergodic bound. If $G$ is $\gamma$-strongly convex, the accelerated variant (Algorithm 2 of the paper) reaches $\|x^N - x^*\| = O(1/N)$, which is a gap of $O(1/N^2)$, and if both $G$ and $F^*$ are strongly convex a fixed choice of steps gives a linear rate. These are theorems of Chambolle and Pock (2011), cited here without proof.

## Properties

- It is matrix free: only $K$, $K^*$ and the two proximal steps are used, so a forward operator such as a blur or a Radon transform can be applied as a function.
- The steps are fixed and need only a bound on $\|K\|$, which a few steps of the power method on $K^*K$ estimate.
- Written with the primal step first, the method is the [proximal point method](/proximal-point-method/) in the metric $M = \begin{pmatrix} I/\tau & -K^* \\ -K & I/\sigma\end{pmatrix}$, and $M$ is positive definite exactly when $\tau\sigma\|K\|^2 < 1$ (He and Yuan 2012). This explains the step condition.
- It is not a descent method: neither the primal energy nor the gap of the last iterates is monotone in general. The bound above holds for the averages.
- The dual iterate gives a certificate: with $y^n$ in the domain of $F^*$, the dual value $-F^*(y^n) - G^*(-K^*y^n)$ is a lower bound of the optimal value.

## Variants and improvements

- Accelerated (Algorithm 2): for $\gamma$-strongly convex $G$, use $\theta_n = 1/\sqrt{1 + 2\gamma\tau_n}$, $\tau_{n+1} = \theta_n\tau_n$, $\sigma_{n+1} = \sigma_n/\theta_n$. The implementation includes this form.
- Preconditioned steps: Pock and Chambolle (2011) give diagonal step matrices from the row and column sums of $|K|$, which removes the need for $\|K\|$ and helps when $K$ is badly scaled.
- Linesearch and adaptive steps balance $\tau$ and $\sigma$ during the run when the scale of the dual variable is not known in advance.
- Condat and Vu added a smooth term $H(x)$ treated by its gradient, with a step condition that also involves the Lipschitz constant of $\nabla H$.
- Relation to other methods: with $\theta = 0$ and varying steps it is the primal-dual hybrid gradient method of Zhu and Chan (2008), which first carried the name PDHG; with $K = I$ and $\tau\sigma = 1$ it is a form of Douglas-Rachford splitting; and Esser, Zhang and Chan (2010) show that it equals a linearized form of [ADMM](/admm/), the split inexact Uzawa method. [Split Bregman](/split-bregman-method/) instead solves a linear system with $K$ in each step.
- Unrolled networks: [learned primal-dual](/learned-primal-dual/) replaces the two proximal steps by trained networks and keeps the structure of the loop.

## When to use it

Use it for a convex model with a nonsmooth term on $Kx$, such as total variation, total generalized variation, $\ell_1$ of wavelet or frame coefficients, or a hard constraint, when $K$ and $K^*$ are cheap but solving a system with $K^*K$ is not. Compared with ADMM and [split Bregman](/split-bregman-method/), it has no inner linear solve; compared with the [proximal gradient method](/proximal-gradient-method/), it does not need the prox of $F \circ K$, which is itself an iterative problem for total variation. When the system with $K^*K$ is cheap, for example a convolution solved with the FFT, split Bregman or ADMM can need fewer iterations.

## Pitfalls

- The step condition is on $\tau\sigma\|K\|^2$, not on each step alone. For the 2D forward difference gradient $\|\nabla\|^2 \le 8$, but with a forward operator $A$ stacked on top the norm of the stacked $K$ is larger, and $K$ must then be scaled or the norm estimated.
- The ratio $\tau/\sigma$ is a free parameter, and a bad ratio slows the method by orders of magnitude, even though the theorem still holds. Balance it so that the primal and dual residuals decrease at similar speeds.
- $K^*$ must be the exact adjoint of $K$, including the border rules. Test $\langle Kx, y\rangle = \langle x, K^*y\rangle$ on random vectors.
- Moreau's identity has a scaling: $\operatorname{prox}_{\sigma F^*}(v) = v - \sigma\operatorname{prox}_{F/\sigma}(v/\sigma)$, and the factor inside is easy to get wrong.
- The rate is for the averages. A stop rule on the last iterates needs a computable gap, which requires the domain of $F^*$ to be bounded or a restriction to a bounded set.

## Implementations

## History

Arrow, Hurwicz and Uzawa studied primal-dual gradient steps for saddle point problems in 1958. Zhu and Chan (2008) proposed the primal-dual hybrid gradient method for total variation restoration, with good results but no general proof. Pock, Cremers, Bischof and Chambolle (2009) used the extrapolated form for a convex relaxation of the Mumford-Shah functional, and Esser, Zhang and Chan (2010) related the family to ADMM and to the split inexact Uzawa method. Chambolle and Pock (2011) gave the general algorithm with the extrapolation, the convergence proof for $\tau\sigma\|K\|^2 < 1$, the ergodic $O(1/N)$ bound and the accelerated variants, and showed many imaging applications. He and Yuan (2012) interpreted it as a proximal point method in a fixed metric. It became the default first order solver for nonsmooth convex imaging models.

## References
