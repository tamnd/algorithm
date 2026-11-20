---
tag: 8N7P4C
kind: algorithm
slug: learned-primal-dual
name: Learned primal-dual reconstruction
aliases:
- learned primal-dual
area: imaging-and-inverse-problems/variational-and-learned-reconstruction
level: research
summary: "An unrolled primal-dual scheme for inverse problems in which learned networks replace both proximal steps, and each of a fixed number of steps calls the forward operator and its adjoint once."
solves: [tomographic-reconstruction-problem]
model: real-ram
complexity:
  vars: {K: the number of steps, a: the cost of one call to A plus one call to its adjoint, g: the cost of one call to each of the two learned maps (outside this page), n: the number of unknowns, m: the number of data values, p: the number of primal channels, d: the number of dual channels}
  time: {worst: O(K (a + g))}
  space: {extra: O(p n + d m)}
properties: {deterministic: true, iterative: true, learned: true, matrix_free: true, exact: false}
history:
  year: 2018
  people: [Jonas Adler, Ozan Oktem]
  note: Adler and Oktem (2017) first learned a gradient-type scheme for nonlinear inverse problems. In 2018 they replaced both proximal steps of the primal-dual hybrid gradient method by convolutional networks and trained the whole scheme on low-dose CT data.
prereqs: [chambolle-pock-algorithm, algorithm-unrolling, backpropagation]
see_also: [lista, variational-network-mri, plug-and-play-priors, filtered-back-projection, landweber-iteration, sparse-view-ct-reconstruction, psnr, structural-similarity-index]
sources:
  - paper: doi:10.1109/TMI.2018.2799231
    title: "Jonas Adler and Ozan Oktem, Learned primal-dual reconstruction, IEEE Transactions on Medical Imaging 37(6), 2018 (arXiv 1707.06474)"
    locator: "pages 1322 to 1332 (Section III.C and Algorithm 3 for the scheme, Section III.D for the reduction to PDHG and to gradient descent, Section IV for the CT data and the networks, Section V for the results)"
  - paper: doi:10.1088/1361-6420/aa9581
    title: "Jonas Adler and Ozan Oktem, Solving ill-posed inverse problems using iterative deep neural networks, Inverse Problems 33(12), 2017"
    locator: article 124007 (the partially learned gradient scheme)
  - paper: doi:10.1007/s10851-010-0251-1
    title: "Antonin Chambolle and Thomas Pock, A first-order primal-dual algorithm for convex problems with applications to imaging, Journal of Mathematical Imaging and Vision 40(1), 2011"
    locator: "pages 120 to 145 (Algorithm 1 and Theorem 1, the method that learned primal-dual contains)"
  - paper: doi:10.1017/S0962492919000059
    title: "Simon Arridge, Peter Maass, Ozan Oktem and Carola-Bibiane Schonlieb, Solving inverse problems using data-driven models, Acta Numerica 28, 2019"
    locator: pages 1 to 174 (survey of learned iterative schemes)
---

Learned primal-dual reconstruction is an unrolled version of the [Chambolle-Pock algorithm](/chambolle-pock-algorithm/) for an inverse problem $y = Ax + e$. It runs a fixed number $K$ of steps. In each step a learned dual map $\Gamma_i$ takes the dual state, the forward projection $Ax$ and the data $y$, and a learned primal map $\Lambda_i$ takes the primal state and the back projection $A^Th$. The maps are small convolutional networks with separate weights in each step, and the primal and dual states have several channels that act as a memory. The whole scheme is trained end to end on pairs of images and data. Adler and Oktem (2018) introduced it for low-dose CT. With the maps set to the two proximal steps it is exactly Chambolle-Pock, and with other fixed maps it is gradient descent. For trained maps there is no convergence or correctness theorem; its accuracy is measured on test data.

## In plain words

A classical solver for an imaging problem goes back and forth many times. It compares its current image with the measured data, sends the mismatch back into image space, and corrects the image with a fixed rule. The rules are the same for every patient and every step.

Learned primal-dual keeps the back and forth but lets small networks make the corrections. On the data side, a network looks at the old data-side state, at what the current image predicts, and at the real measurement, and decides on a new data-side state. On the image side, another network looks at the old image and at the sent-back mismatch, and decides on a new image. It does this a fixed number of times, for example ten, and each step has its own networks. The networks are trained on many examples so that the final image is close to the true one.

## The problem

The model is $y = Ax + e$ with $x \in \mathbb{R}^n$ the image, $y \in \mathbb{R}^m$ the data and $A$ the forward operator, for example a discrete [Radon transform](/radon-transform/). The variational approach minimizes $F_y(Ax) + G(x)$, for example $\tfrac12\|Ax - y\|^2 + \lambda\|\nabla x\|_1$. The learned approach instead looks for a reconstruction operator $R_\Theta : \mathbb{R}^m \to \mathbb{R}^n$ with parameters $\Theta$ that minimizes the empirical risk $\frac1N\sum_{j=1}^N \|R_\Theta(y_j) - x_j\|^2$ over training pairs $(x_j, y_j)$. Learned primal-dual is a choice of $R_\Theta$ that uses $A$ and $A^T$ inside.

The input of the algorithm is the data $y$, functions that apply $A$ and $A^T$, and the trained maps $\Gamma_1, \ldots, \Gamma_K$ and $\Lambda_1, \ldots, \Lambda_K$. The output is an image $x \in \mathbb{R}^n$.

## The algorithm

The primal state $x = (x^{(1)}, \ldots, x^{(p)})$ has $p$ images, and the dual state $h = (h^{(1)}, \ldots, h^{(d)})$ has $d$ vectors in data space. This is Algorithm 3 of Adler and Oktem for a linear operator, where the adjoint of the derivative is $A^T$.

```pseudo id=main
LEARNED-PRIMAL-DUAL(y, A, A^T, Γ_1..Γ_K, Λ_1..Λ_K, x_0, h_0)
L1  x ← x_0, h ← h_0                        ▷ usually all zero
L2  for i = 1 to K
L3      h ← Γ_i(h, A x^(2), y)               ▷ dual update, a given network
L4      x ← Λ_i(x, A^T h^(1))                ▷ primal update, a given network
L5  return x^(1)
```

Line L3 is the only place where the data enters. The dual map sees the old dual state, the forward projection of the second primal channel and the data. Line L4 is the only place where the adjoint enters: the primal map sees the old primal state and the back projection of the first dual channel. Each line calls the operator once, so a step costs one call to $A$ and one call to $A^T$, as a step of Chambolle-Pock does.

**Chambolle-Pock as a special case.** Take $p = 2$, $d = 1$, and for every step

$$\Gamma_i(h, z, y) = \operatorname{prox}_{\sigma F_y^*}(h + \sigma z),\qquad \Lambda_i\big((x^{(1)}, x^{(2)}), w\big) = \big(u,\ 2u - x^{(1)}\big),\quad u = \operatorname{prox}_{\tau G}(x^{(1)} - \tau w).$$

Then $x^{(1)}$ is the Chambolle-Pock iterate and $x^{(2)}$ is the extrapolated point $\bar x$. This is Section III.D of the paper.

**Gradient descent as a special case.** Take $p = d = 1$, $\Gamma_i(h, z, y) = z - y$ and $\Lambda_i(x, w) = x - \omega w$. Then each step is $x \leftarrow x - \omega A^T(Ax - y)$, the [Landweber iteration](/landweber-iteration/).

**The trained version.** Adler and Oktem use $p = d = 5$ and $K = 10$. Each map is a residual network: the identity plus three $3 \times 3$ convolution layers, with PReLU activations after the first two. The input of a dual map has 7 channels (5 dual channels, $Ax^{(2)}$ and $y$), and the input of a primal map has 6 (5 primal channels and $A^Th^{(1)}$). The ten steps have separate weights, about $2.4 \cdot 10^5$ parameters in total. Training minimizes the mean squared error by Adam, with gradients from [backpropagation](/backpropagation/) through all steps, including through $A$ and $A^T$.

## Example

The scalar problem $A = 1$, $y = 1$, $F_y(z) = \tfrac12(z - 1)^2$ and $G(x) = \tfrac12|x|$, that is $\min_x \tfrac12(x - 1)^2 + \tfrac12|x|$, has the solution $x^\star = 1/2$. The optimal dual value is $h^\star = Ax^\star - y = -1/2$. With $\tau = \sigma = 1/2$ (so $\tau\sigma\|A\|^2 = 1/4 < 1$), $\operatorname{prox}_{\sigma F_y^*}(v) = (v - \sigma y)/(1 + \sigma)$ and $\operatorname{prox}_{\tau G}$ the soft threshold at $\tau/2 = 1/4$. The Chambolle-Pock maps, started from zero, give:

| step $i$ | $h$ | $x^{(1)}$ | $x^{(2)} = \bar x$ |
|---|---|---|---|
| 1 | $-1/3$ | $0$ | $0$ |
| 2 | $-5/9$ | $1/36$ | $1/18$ |
| 3 | $-37/54$ | $13/108$ | 0.2130 |
| 4 | $-233/324$ | $149/648$ | 0.3395 |
| 10 | $-0.5130$ | $0.5199$ | 0.5263 |

In step 1, line L3 gives $h = (0 + 0 - 1/2)/(3/2) = -1/3$, and line L4 gives $u = \operatorname{soft}(0 + 1/6, 1/4) = 0$. In step 2, $h = (-1/3 - 1/2)/(3/2) = -5/9$ and $u = \operatorname{soft}(5/18, 1/4) = 1/36$. The iterates converge to $(1/2, -1/2)$. A learned scheme with the same two calls per step could, for example, learn to take larger corrections in the first steps.

With the gradient maps, $A = 1$, $y = 1$ and $\omega = 0.01$, the scheme gives $1 - 0.99^{K}$ after $K$ steps, which is 0.63397 for $K = 100$: the Landweber filter factor for $\omega\sigma^2 = 0.01$.

## Correctness

For trained maps there is no correctness theorem. The network maps have no convexity, no fixed point and no stopping rule, and the scheme is only as good as its training data. What is proved is in the proof file below. With the Chambolle-Pock maps, the scheme produces the Chambolle-Pock iterates exactly, by induction on the step; so it converges for $\tau\sigma\|A\|^2 < 1$ by the theorem of Chambolle and Pock (2011, Theorem 1). With the gradient maps, it produces the Landweber iterates.

Adler and Oktem conclude that, since the class of schemes contains these methods, a trained scheme should do at least as well as they do with the same number of steps. This is a heuristic: it needs the networks to approximate the proximal maps well, and it needs the nonconvex training to find good weights.

## Complexity

The model is real-ram. Each of the $K$ steps calls $A$ once, $A^T$ once and each learned map once. So the time is $O(K(a + g))$, where $a$ is the cost of one call to $A$ and one to $A^T$, and $g$ is the cost of the two networks. The cost of the networks depends on their architecture and is outside this page; for convolutional maps on an image of $n$ pixels it is linear in $n$ times the number of channels and weights. The extra space is $O(pn + dm)$ for the states. Training needs the gradient through all $K$ steps, which by backpropagation costs a constant times the forward pass and stores all intermediate states, $O(K(pn + dm))$ memory, unless gradient checkpointing trades time for memory.

For comparison, Chambolle-Pock with the same $K$ costs $O(Ka)$ plus two proximal steps per iteration, but it needs hundreds of iterations where the learned scheme uses ten.

## Properties

- **Uses the physics.** Every step calls $A$ and $A^T$, so the network never has to learn the forward model. This is the difference from post-processing networks that only clean up a [filtered back projection](/filtered-back-projection/).
- **Fixed cost.** The number of steps is fixed before training, so the reconstruction time is known in advance.
- **Contains classical schemes.** Chambolle-Pock and gradient descent are special cases, as shown above.
- **Measured results.** Adler and Oktem report two CT tests. The first uses random ellipse phantoms on a $128 \times 128$ grid, a parallel beam geometry with 30 views and 182 detector pixels, and 5 percent Gaussian noise, with the Shepp-Logan phantom for validation. The second uses human abdomen images of $512 \times 512$ pixels from the Mayo Clinic low-dose CT challenge, a fan beam geometry with 1000 angles and Poisson noise with $10^4$ incident photons per pixel. In both tests learned primal-dual had the highest [PSNR](/psnr/) and [SSIM](/structural-similarity-index/) among the methods compared, which included FBP, TV regularization and a learned post-processing network. On the ellipse data the gain over the learned gradient scheme and the post-processing network was more than 6 dB. The learned methods that call the operator were about 6 times slower than FBP plus a network, and at least 100 times faster than TV with 1000 iterations. These are measurements on those data sets, not properties of the algorithm.

## Variants and improvements

- **Learned PDHG.** Keep $p = d = 1$, the update forms $h + \sigma Ax$ and $x - \tau A^Th$, and the over-relaxation, and learn only the two proximal maps (Algorithm 2 of the paper). It did about as well as classical methods in their tests.
- **Learned primal.** Fix the dual map to the residual $Ax^{(2)} - y$ and learn only the primal map. In the ellipse test it was the closest competitor, 1.3 dB behind.
- **Learned gradient** (Adler and Oktem 2017). Feed the gradient of the data term to a learned update; this is the earlier scheme.
- **Nonlinear forward models.** For a nonlinear operator $\mathcal{T}$, line L4 uses the adjoint of the derivative $[\partial\mathcal{T}(x^{(1)})]^*$. The paper treats the pre-log CT model $\mathcal{T}(x) = e^{-\mu Ax}$ this way.
- **Other unrolled schemes.** The [variational network](/variational-network-mri/) unrolls a gradient scheme for MRI, and [LISTA](/lista/) unrolls ISTA; see [algorithm unrolling](/algorithm-unrolling/).

## When to use it

Use learned primal-dual when the forward operator is known and fixed, when many training pairs from the same acquisition setting exist, and when the reconstruction must be fast and better than [FBP](/filtered-back-projection/) on undersampled or noisy data, as in low-dose or [sparse-view CT](/sparse-view-ct-reconstruction/). Do not use it when the geometry or the noise level changes from scan to scan without retraining, when no training data exist, or when you need a guarantee such as a bound on the data misfit. Then a variational method or a [plug-and-play](/plug-and-play-priors/) scheme with an explicit data term is safer.

## Pitfalls

- **Wrong adjoint.** The scheme backpropagates through $A^T$, and a back projector that is not the exact adjoint of the projector gives wrong training gradients. Check $|\langle Ax, h\rangle - \langle x, A^Th\rangle|$ on random vectors.
- **Distribution shift.** A network trained at one dose, one geometry or one anatomy can produce plausible but wrong structures elsewhere. Evaluate on held-out data from the target setting.
- **Memory of training.** Backpropagation through $K$ steps with large images stores all states; the memory, not the time, is often the limit.
- **Reading the PSNR as a guarantee.** A higher mean PSNR on a test set does not bound the error on any one image.
- **Scaling.** The data and the images must be scaled as in training; the network is not invariant to a change of units.

## Implementations

The update maps are given functions: the code takes the lists $\Gamma_1, \ldots, \Gamma_K$ and $\Lambda_1, \ldots, \Lambda_K$, and functions for $A$ and $A^T$, as arguments and runs lines L1 to L5 around them. The tests build the maps by hand, as the Chambolle-Pock maps and the gradient maps, or as small residual networks with weights from a fixed seed. No network is trained and no weights are downloaded. The tests check the adjoint of a periodic blur operator, the equality with a direct Chambolle-Pock loop on a matrix and on a blur, the example values above, convergence to the lasso solution $(0, 0, 0.9)$ of the [LISTA](/lista/) example, the Landweber check value 0.63397, and that a step calls $A$ and $A^T$ exactly once.

## History

Gregor and LeCun (2010) unrolled ISTA into a trained network, and Yang, Sun, Li and Xu (2016) and Hammernik et al. (2018) unrolled ADMM and gradient schemes for MRI. Adler and Oktem (2017) proposed a partially learned gradient scheme for nonlinear inverse problems, and in 2018 they introduced learned primal-dual, which replaces both proximal maps of the primal-dual hybrid gradient method by networks and keeps a memory of several channels. It became a common baseline for learned CT reconstruction. The survey of Arridge, Maass, Oktem and Schonlieb (2019) places it among the data-driven methods for inverse problems.

## References
