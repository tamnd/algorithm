---
tag: R2YTGF
kind: algorithm
slug: chambolle-projection-algorithm
name: Chambolle's projection algorithm
aliases:
- Chambolle dual algorithm for total variation
- Chambolle's semi-implicit dual iteration
area: imaging-and-inverse-problems/variational-and-learned-reconstruction
level: advanced
summary: Solve total variation denoising by a fixed point iteration on a dual field, which computes the projection of the noisy image onto the set of bounded divergence fields.
solves: [image-denoising]
model: real-ram
complexity:
  vars: {N: the number of pixels, K: the number of iterations}
  time: {worst: O(K N)}
  space: {extra: O(N)}
properties: {deterministic: true, exact: false, iterative: true, feasible_iterates: true, monotone_dual_objective: true, mean_preserving: true}
history:
  year: 2004
  people: [Antonin Chambolle]
  note: Chambolle wrote the total variation as a support function, so that denoising becomes a projection onto a convex set, and gave a semi-implicit step for the dual problem with a convergence proof for a step of at most 1/8.
prereqs: [total-variation-denoising, fenchel-duality, projected-gradient-descent, proximal-operator]
see_also: [chambolle-pock-algorithm, split-bregman-method, fista, proximal-gradient-method, total-generalized-variation, image-deblurring, image-denoising]
sources:
  - paper: doi:10.1023/B:JMIV.0000011325.36760.1e
    title: Antonin Chambolle, An algorithm for total variation minimization and applications, Journal of Mathematical Imaging and Vision 20(1-2), 2004
    locator: pages 89 to 97 (Section 3, the semi-implicit step and Theorem 3.1 for a step of at most 1/8)
  - paper: doi:10.1016/0167-2789(92)90242-F
    title: Leonid I. Rudin, Stanley Osher and Emad Fatemi, Nonlinear total variation based noise removal algorithms, Physica D 60(1-4), 1992
    locator: pages 259 to 268
  - paper: doi:10.1007/s002110050258
    title: Antonin Chambolle and Pierre-Louis Lions, Image recovery via total variation minimization and related problems, Numerische Mathematik 76(2), 1997
    locator: pages 167 to 188
  - paper: doi:10.1109/TIP.2009.2028250
    title: Amir Beck and Marc Teboulle, Fast gradient-based algorithms for constrained total variation image denoising and deblurring problems, IEEE Transactions on Image Processing 18(11), 2009
    locator: pages 2419 to 2434 (the accelerated projected gradient on the same dual problem)
  - paper: doi:10.1017/S096249291600009X
    title: Antonin Chambolle and Thomas Pock, An introduction to continuous optimization for imaging, Acta Numerica 25, 2016
    locator: pages 161 to 319
  - url: https://www.ipol.im/pub/art/2013/61/
    title: Joan Duran, Bartomeu Coll and Catalina Sbert, Chambolle's projection algorithm for total variation denoising, Image Processing On Line, 2013
---

Chambolle's projection algorithm computes the minimizer of the [total variation denoising](/total-variation-denoising/) energy $\tfrac12\|u - f\|^2 + \lambda\,\mathrm{TV}(u)$ without touching the nonsmooth total variation directly. It uses one fact from [convex duality](/fenchel-duality/): the discrete total variation is the largest value of $\langle u, \operatorname{div} p\rangle$ over the vector fields $p$ with length at most 1 at every pixel. So the denoised image is $u = f - \pi_{\lambda K}(f)$, where $\pi_{\lambda K}$ is the projection onto the closed convex set $\lambda K$ of divergences of such fields. The algorithm finds this projection by a simple fixed point step on the dual field $p$, with a denominator that keeps every iterate feasible. Chambolle proved in 2004 that the iterates converge for every step $\tau \le 1/8$. The output is the [proximal operator](/proximal-operator/) of $\lambda\,\mathrm{TV}$, so the same routine is the inner step of many deblurring and reconstruction methods.

## In plain words

A noisy image is a clean image plus a noise part. The method does not look for the clean image directly. It looks for the noise part, because the noise part has a simple description: it is built from a small arrow at each pixel, and no arrow may be longer than a fixed limit. The method keeps one arrow per pixel and improves all arrows at the same time. At each step every arrow turns toward the direction that removes more of the remaining noise, and a division shrinks it back so that it never passes the limit. When the arrows stop changing, the noise part is known, and the clean image is the noisy image minus the noise part. Each step only compares a pixel with its neighbors, so a step is cheap, but many steps can be needed.

## The problem

The input is an image $f$ with $N = n_1 n_2$ pixels and a weight $\lambda > 0$. The output is the unique minimizer of

$$E(u) = \tfrac12\|u - f\|^2 + \lambda\,\mathrm{TV}(u), \qquad \mathrm{TV}(u) = \sum_{i,j} |(\nabla u)_{ij}|,$$

where $(\nabla u)_{ij} = (u_{i+1,j} - u_{ij},\; u_{i,j+1} - u_{ij})$ are forward differences with the Neumann rule (a difference that leaves the image is 0) and $|\cdot|$ is the Euclidean length, which gives the isotropic total variation. The divergence is defined by $\operatorname{div} = -\nabla^\top$, so $\langle \nabla u, p\rangle = -\langle u, \operatorname{div} p\rangle$ for every image $u$ and field $p$. With this choice

$$\mathrm{TV}(u) = \max\{\langle u, \operatorname{div} p\rangle : |p_{ij}| \le 1 \text{ for all } i, j\},$$

and the minimizer is $u = f - \lambda \operatorname{div} p^*$, where $p^*$ is any solution of the dual problem

$$\min_p \|\operatorname{div} p - f/\lambda\|^2 \quad\text{subject to}\quad |p_{ij}| \le 1 \text{ for all } i, j.$$

The dual solution $p^*$ need not be unique, but $\lambda\operatorname{div} p^* = \pi_{\lambda K}(f)$ is. The weight $\lambda$ is a design choice: it sets the size of the smallest feature that survives, and it is tuned for each class of images.

## The algorithm

```pseudo id=main
ChambolleProjection(f, λ, τ, K)
L1  p ← 0                                   ▷ one 2-vector per pixel
L2  for k = 1 to K
L3      v ← div p - f / λ                   ▷ the dual residual
L4      z ← ∇v
L5      at each pixel: p ← (p + τ z) / (1 + τ |z|)
L6  w ← λ div p                             ▷ the projection of f onto λK
L7  return u = f - w
```

The dual problem has the constraint $|p_{ij}| \le 1$, and its optimality condition at each pixel is $-z_{ij} + \alpha_{ij} p_{ij} = 0$ with a multiplier $\alpha_{ij} \ge 0$. In both cases ($|p_{ij}| < 1$, which forces $z_{ij} = 0$, and $|p_{ij}| = 1$) the multiplier is $\alpha_{ij} = |z_{ij}|$. Chambolle's step is a gradient step on this condition, with the multiplier term taken at the new point:

$$p^{n+1} = p^n + \tau\big(z^n - |z^n|\,p^{n+1}\big).$$

Solving for $p^{n+1}$ gives line L5. The denominator keeps the iterates feasible: if $|p| \le 1$, then $|p + \tau z| \le 1 + \tau|z|$. Line L4 is minus one half of the gradient of the dual objective, and lines L6 and L7 map the dual field back to the image. A practical stop is the duality gap $E(u^n) - D(p^n)$ with $D(p) = \tfrac12\|f\|^2 - \tfrac12\|f - \lambda\operatorname{div}p\|^2$, which bounds $\tfrac12\|u^n - u^*\|^2$.

## Example

Take the one-row image $f = (0, 0, 3, 3)$ with $\lambda = 1$. In one dimension the field has three entries $(p_1, p_2, p_3)$, one per difference, $\operatorname{div} p = (p_1,\, p_2 - p_1,\, p_3 - p_2,\, -p_3)$, and $\|\operatorname{div}\|^2 \le 4$, so the proof below covers $\tau \le 1/4$. Take $\tau = 1/4$.

Step 1: $p = 0$, so $v = -f = (0, 0, -3, -3)$ and $z = \nabla v = (0, -3, 0)$. Line L5 gives $p_2 = (0 - 3/4)/(1 + 3/4) = -3/7$, and the other entries stay 0. Then $\operatorname{div} p = (0, -3/7, 3/7, 0)$ and $u = (0,\ 0.4286,\ 2.5714,\ 3)$. The edge has started to shrink, but the flat parts have not moved yet, because the field is still 0 next to them.

| $k$ | $p$ | $u$ | gap $E(u) - D(p)$ |
|---|---|---|---|
| 1 | $(0, -0.4286, 0)$ | $(0, 0.4286, 2.5714, 3)$ | 2.0816 |
| 2 | $(-0.0968, -0.6279, -0.0968)$ | $(0.0968, 0.5311, 2.4689, 2.9032)$ | 1.5057 |
| 3 | $(-0.1852, -0.7493, -0.1852)$ | $(0.1852, 0.5641, 2.4359, 2.8148)$ | 1.0865 |
| 10 | $(-0.4469, -0.9830, -0.4469)$ | $(0.4469, 0.5362, 2.4638, 2.5531)$ | 0.1315 |
| 20 | $(-0.4963, -0.9997, -0.4963)$ | $(0.4963, 0.5034, 2.4966, 2.5037)$ | 0.0078 |
| 50 | $(-0.5, -1, -0.5)$ | $(0.5, 0.5, 2.5, 2.5)$ | $1.5 \cdot 10^{-6}$ |

The limit is $p^* = (-1/2, -1, -1/2)$ and $u^* = (1/2, 1/2, 5/2, 5/2)$: each side moves toward the other by $\lambda$ divided by its length 2, as the [total variation denoising](/total-variation-denoising/) page derives. At the edge $\nabla u^* = 2$ and $p^*_2 = -1$, so $-\nabla u^* = |\nabla u^*|\,p^*$ there, which is the optimality condition. With $\tau = 1/8$ the same gap needs about 100 steps instead of 50.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). Let $F(p) = \|\operatorname{div} p - f/\lambda\|^2$ and let $\kappa$ bound $\|\operatorname{div}\|^2$, with $\kappa = 8$ in two dimensions. Write one step as $p' = p + \tau\eta$ with $\eta = z - |z|p'$. Then

$$F(p') \le F(p) - \tau\Big(\sum_{i,j} |z_{ij}|^2\big(1 - |p'_{ij}|^2\big) + (1 - \tau\kappa)\|\eta\|^2\Big),$$

so for $\tau \le 1/\kappa$ the dual objective does not increase (a theorem). If it does not decrease, the step does not move: at each pixel either $z = 0$, or $|p'| = 1$, and then the triangle inequality forces $p = z/|z| = p'$. This is the case $\tau = 1/8$ that needs care. A fixed point satisfies $-\nabla u = |\nabla u|\,p$ at each pixel for $u = f - \lambda\operatorname{div} p$, so $\langle u, \lambda\operatorname{div}p\rangle = \lambda\,\mathrm{TV}(u)$, and this makes $u$ the minimizer with $E(v) \ge E(u) + \tfrac12\|v - u\|^2$ for all $v$. The step map is continuous and the iterates are bounded, so every limit point of $(p^n)$ is a fixed point and $u^n \to u^*$. The field $p^n$ itself need not converge, because the dual solution is not unique.

## Complexity

One iteration computes a divergence, a gradient and a pixelwise update: $\Theta(N)$ arithmetic operations and $\Theta(N)$ extra memory for $p$ and two work images. $K$ iterations cost $\Theta(K N)$. Theorem 3.1 of Chambolle's paper gives convergence but no rate. Treated as [projected gradient descent](/projected-gradient-descent/) on the dual, the same dual problem has objective error $O(1/K)$, and with the acceleration of Beck and Teboulle $O(1/K^2)$; the gap bound above turns a dual error $e$ into $\|u - u^*\|^2 \le 2e$. After $k$ steps the field at a pixel depends only on the data within about $2k$ pixels, because each step looks at the neighbors twice. So a flat region of width $w$ needs at least about $w/2$ steps before the value at one end can depend on the data at the other end, which it must do to become the regional mean.

## Properties

- The iterates stay feasible: $|p^n_{ij}| \le 1$ for all $n$, so $\lambda\operatorname{div}p^n \in \lambda K$ and the dual value $D(p^n)$ is a valid lower bound of $\min E$ at every step.
- For $\tau \le 1/8$ the dual objective $\|\operatorname{div}p^n - f/\lambda\|^2$ is nonincreasing.
- The mean is kept: $\sum_{ij} (\operatorname{div}p)_{ij} = -\langle \nabla 1, p\rangle = 0$, so $u^n$ has the mean of $f$ at every step.
- The output is $\operatorname{prox}_{\lambda\mathrm{TV}}(f)$. Moreau's identity reads here $f = \operatorname{prox}_{\lambda\mathrm{TV}}(f) + \pi_{\lambda K}(f)$, because the convex conjugate of $\mathrm{TV}$ is the indicator of $K$.
- The method needs no matrix, no linear solve and no smoothing of the total variation.
- A warm start from a previous $p$ is allowed, because the proof only needs $|p^0_{ij}| \le 1$.

## Variants and improvements

- Projected gradient on the dual: $p \leftarrow \pi_{|p| \le 1}(p + \tau z)$ at each pixel. Chambolle later used this form with $\tau < 1/4$ in two dimensions. It is [projected gradient descent](/projected-gradient-descent/) on $F$ with the step $\tau/2$, and the gradient of $F$ is Lipschitz with constant $2\kappa = 16$, so the classic condition step $< 2/16$ gives $\tau < 1/4$.
- Accelerated dual: Beck and Teboulle (2009) apply the [FISTA](/fista/) momentum to the projected dual gradient, which gives $O(1/K^2)$ for the dual objective.
- Anisotropic total variation: with $|\partial_1 u| + |\partial_2 u|$ the constraint is $|p_{1,ij}| \le 1$ and $|p_{2,ij}| \le 1$, and the step becomes a clip of each component.
- Weighted and color total variation: a pixel weight $w_{ij}$ changes the bound to $|p_{ij}| \le w_{ij}$, and a vectorial total variation couples the channels in the length of $p$.
- Inner solver: inside the [proximal gradient method](/proximal-gradient-method/) for deblurring, $\min \tfrac12\|Au - g\|^2 + \lambda\,\mathrm{TV}(u)$, each outer step needs $\operatorname{prox}_{s\lambda\mathrm{TV}}$, which this algorithm computes with a warm start.
- Primal-dual methods: the [Chambolle-Pock algorithm](/chambolle-pock-algorithm/) and [split Bregman](/split-bregman-method/) solve the same model and also handle a forward operator directly.

## When to use it

Use it when you need the proximal operator of total variation, as a short and safe subroutine, or as a reference solver for small images in tests. It has one parameter, every iterate is feasible, and the duality gap gives a stop rule with a guarantee. For large images or a high accuracy it is slow, and in reported experiments accelerated dual or primal-dual methods reach the same gap in fewer iterations; this is a measurement, not a theorem. If the problem has a forward operator, use a primal-dual method rather than nesting this one inside an outer loop.

## Pitfalls

- The divergence must be exactly $-\nabla^\top$, including the border rows and columns. A divergence with a different border rule breaks the duality and the proof, and the result is wrong near the border. Test $\langle \nabla u, p\rangle = -\langle u, \operatorname{div}p\rangle$ on random data.
- The proof covers $\tau \le 1/8$ in two dimensions. Chambolle remarks that $\tau = 1/4$ works better in practice, but there is no proof for that step size with this update.
- Some papers put the weight on the data term, $\tfrac\mu2\|u - f\|^2 + \mathrm{TV}(u)$. Then $\lambda = 1/\mu$.
- A stop rule on $\|p^{n+1} - p^n\|$ can stop too early when the steps are small. The duality gap is the safe stop rule.
- The field $p^n$ can move along a set of dual solutions without converging. Only $\operatorname{div}p^n$ and $u^n$ have a limit.
- For a large $\lambda$ the solution is nearly flat over large regions, and the number of iterations grows with the size of these regions.

## Implementations

## History

Rudin, Osher and Fatemi proposed total variation denoising in 1992, and Chambolle and Lions (1997) studied the model and its use for image recovery. Dual and primal-dual formulations followed, among them the Newton type primal-dual method of Chan, Golub and Mulet (1999). In 2004 Antonin Chambolle observed that total variation is the support function of the convex set $K$, so its proximal operator is the identity minus a projection, and gave the semi-implicit dual step on this page with a short convergence proof. The method became a standard building block because it is simple and has no smoothing parameter. Beck and Teboulle (2009) accelerated the dual approach, and Chambolle and Pock (2011) gave a primal-dual method that handles a general forward operator.

## References
