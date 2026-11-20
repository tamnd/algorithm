---
tag: ZV36YT
kind: algorithm
slug: compressed-sensing-generative-models
name: Compressed sensing with generative models
aliases:
- CSGM
area: imaging-and-inverse-problems/variational-and-learned-reconstruction
level: research
summary: Recover a signal from few linear measurements by searching the latent space of a trained generator for the output that best fits the measurements.
model: real-ram
complexity:
  vars: {s: the number of starting codes, T: the number of gradient steps per start, a: the cost of one call to A plus one call to its adjoint, g: the cost of one call to the generator plus one vector-Jacobian product (outside this page), n: the signal length, m: the number of measurements, k: the latent dimension}
  time: {worst: O(s T (a + g))}
  space: {extra: O(n + m + k)}
properties: {deterministic: true, iterative: true, learned: true, matrix_free: true, exact: false}
history:
  year: 2017
  people: [Ashish Bora, Ajil Jalal, Eric Price, Alexandros G. Dimakis]
  note: "Bora, Jalal, Price and Dimakis replaced the sparsity model of compressed sensing by the range of a trained generator, proved a recovery bound for Lipschitz generators under a set-restricted eigenvalue condition, and solved the latent search by gradient descent with restarts."
prereqs: [compressed-sensing, restricted-isometry-property, gradient-descent, backpropagation]
see_also: [deep-image-prior, diffusion-posterior-sampling, variational-autoencoder, lasso-regression, sparse-signal-recovery, iterative-hard-thresholding, compressed-sensing-mri, lista]
sources:
  - paper: arxiv:1703.03208
    title: "Ashish Bora, Ajil Jalal, Eric Price and Alexandros G. Dimakis, Compressed sensing using generative models, Proceedings of the 34th International Conference on Machine Learning, PMLR 70, 2017"
    locator: "pages 537 to 546 (Definition 1 of S-REC, Lemmas 4.1 to 4.3 and Theorems 1.1 and 1.2 for the bounds, Section 6 and Figure 1 for the experiments)"
---

Compressed sensing with generative models (CSGM) recovers a signal $x^* \in \mathbb{R}^n$ from $m \ll n$ noisy linear measurements $y = Ax^* + \eta$. Classical [compressed sensing](/compressed-sensing/) assumes that $x^*$ is sparse. CSGM assumes instead that $x^*$ is close to the range of a trained generator $G : \mathbb{R}^k \to \mathbb{R}^n$ with $k \ll n$, such as the decoder of a [variational autoencoder](/variational-autoencoder/) or a GAN generator. It minimizes $\|AG(z) - y\|^2 + \lambda\|z\|^2$ over the latent code $z$ by gradient descent from several random starts, and it returns $G(\hat z)$. Bora, Jalal, Price and Dimakis (2017) proved that, for a Gaussian $A$ and an $L$-Lipschitz generator, $m = O(k\log(Lr/\delta))$ measurements are enough for any near minimizer to be close to $x^*$. The search itself is nonconvex, and the bound says nothing about whether gradient descent finds a near minimizer.

## In plain words

Suppose you want to take a picture of a face with far fewer sensor readings than there are pixels. In general this is impossible: many images fit the same readings. But faces are not arbitrary images. A trained generator can make a face from a short list of numbers, the code.

CSGM uses this. It looks for the code whose face, after you take the readings of it, matches the readings that you measured. It starts from a random code and changes it a little at a time to reduce the mismatch. Because the search can get stuck, it tries several random starts and keeps the best result. The answer is always a face that the generator can make, so it can only be as good as the generator is.

## The problem

The input is the matrix $A \in \mathbb{R}^{m \times n}$ (or functions that apply $A$ and $A^T$), the data $y \in \mathbb{R}^m$, a generator $G$ with its vector-Jacobian product $v \mapsto J_G(z)^Tv$, a penalty weight $\lambda \ge 0$, a step size $\eta$, a number of steps $T$ and a list of starting codes. The output is $\hat x = G(\hat z)$, where $\hat z$ is the code with the lowest final loss

$$f(z) = \|AG(z) - y\|^2 + \lambda\|z\|^2.$$

This is the problem of [sparse signal recovery](/sparse-signal-recovery/) with the set of sparse vectors replaced by $S = G(B^k(r))$, the image of a ball of codes. The penalty $\lambda\|z\|^2$ keeps the code where the generator was trained, since its codes were drawn from $N(0, I)$ during training.

## The algorithm

```pseudo id=main
CSGM(y, A, G, J_G^T, starts, η, T, λ)
L1  best ← none, best_loss ← ∞
L2  for each start z_0 in starts
L3      z ← z_0
L4      for t = 1 to T
L5          g ← 2 J_G(z)^T A^T (A G(z) - y) + 2 λ z     ▷ the gradient of f
L6          z ← z - η g
L7      if f(z) < best_loss then best ← z, best_loss ← f(z)
L8  return G(best)
```

Line L5 is the chain rule: the residual $AG(z) - y$ goes back through $A^T$ and then through the generator by one [backpropagation](/backpropagation/) pass. Line L6 is a [gradient descent](/gradient-descent/) step; Bora et al. use the Adam optimizer instead, and any first-order method works here. Line L7 is the random restart rule: the run with the lowest loss wins, because the loss is the only thing the method can measure without $x^*$.

## Example

Take $n = 2$, $k = 1$, the generator $G(z) = (\tanh z, \tanh 2z)$, one measurement $A = (1\ \ 1)$, no noise and no penalty. The true code is $z^* = 0.5$, so $x^* = (0.462117, 0.761594)$ and $y = 1.2237113$. One measurement of two unknowns is not enough in general, but here $AG(z) = \tanh z + \tanh 2z$ is strictly increasing in $z$, so only one code fits.

From $z_0 = 0$ with step $\eta = 0.1$: at $z = 0$ the residual is $-1.2237$ and $J_G(0)^TA^T = 1 + 2 = 3$, so $g = 2 \cdot 3 \cdot (-1.2237) = -7.3423$ and $z_1 = 0.734227$. The next steps are:

| step $t$ | $z_t$ | loss $f(z_t)$ |
|---|---|---|
| 1 | 0.734227 | 0.0907 |
| 2 | 0.674517 | 0.0567 |
| 3 | 0.620850 | 0.0303 |
| 4 | 0.576863 | 0.0134 |
| 5 | 0.544763 | 0.00484 |
| 10 | 0.501374 | |
| 20 | 0.500001 | |

The first step overshoots, and the later steps approach $z^* = 0.5$ from above. The output is $G(0.5) = x^*$ exactly.

**A non-example.** With $A = (1\ \ {-1})$ the measured value is $\tanh z - \tanh 2z$. This function is 0 at $z = 0$, has its minimum $-0.30028$ near $z = 0.531$, and goes back to 0 as $z$ grows. So the value $y = -0.2$ is fitted exactly by $z = 0.22411$, which gives $x = (0.22043, 0.42043)$, and by $z = 1.00875$, which gives $x = (0.76524, 0.96524)$. A start at $0.1$ finds the first and a start at $2$ finds the second. Both have zero loss, so the restart rule cannot choose between them. Here the measurement does not separate points of the range, which is exactly what the S-REC condition below forbids.

## Correctness

The proof file proves the deterministic part of the guarantee (Bora et al., Lemma 4.3), which is a theorem.

**Definition.** $A$ satisfies $\text{S-REC}(S, \gamma, \delta)$ if $\|A(x_1 - x_2)\| \ge \gamma\|x_1 - x_2\| - \delta$ for all $x_1, x_2 \in S$.

**Theorem.** Let $A$ satisfy $\text{S-REC}(S, \gamma, \delta)$, let $\bar x \in S$ be closest to $x^*$, and suppose $\|A(x^* - \bar x)\| \le 2\|x^* - \bar x\|$. If $\hat x \in S$ fits the data within $\varepsilon$ of the best fit in $S$, then

$$\|\hat x - x^*\| \le \Big(\frac4\gamma + 1\Big)\min_{x \in S}\|x^* - x\| + \frac1\gamma\big(2\|\eta\| + \varepsilon + \delta\big).$$

The proof uses S-REC once for $\hat x - \bar x$ and the triangle inequality twice. The first term is the error of the model: if $x^*$ is far from the range, no number of measurements helps. Bora et al. show (Lemma 4.1, a theorem) that a Gaussian $A$ with $N(0, 1/m)$ entries satisfies S-REC with $\gamma$ near 1, with high probability, once $m = \Omega(k\log(Lr/\delta))$ for an $L$-Lipschitz $G$ on codes of norm at most $r$. For a $d$-layer ReLU network, $m = O(kd\log n)$ suffices with $\delta = 0$ (Theorem 1.1). Their Theorem 1.2 states the combined result as $\|G(\hat z) - x^*\| \le 6\min_{\|z\| \le r}\|G(z) - x^*\| + 3\|\eta\| + 2\varepsilon + 2\delta$ with probability $1 - e^{-\Omega(m)}$.

The bound is about any near minimizer. It does not say that lines L4 to L6 find one: $f$ is not convex in $z$, and gradient descent can stop at a spurious stationary point or, with $\lambda = 0$, run off to a region where the generator saturates. The tests show both cases on a seeded problem. That restarts find a good minimizer in practice is a heuristic; Bora et al. report it as an observation.

The proof file also shows that line L5 is the exact gradient of $f$, so lines L5 and L6 are true gradient steps.

## Complexity

The model is real-ram. Each gradient step calls $G$ once, its vector-Jacobian product once, $A$ once and $A^T$ once. With $s$ starts and $T$ steps per start, the time is $O(sT(a + g))$, where $a$ is the cost of $A$ plus $A^T$ ($O(mn)$ for a dense matrix) and $g$ is the cost of the generator plus one backward pass, which is outside this page. A backward pass costs a small constant times a forward pass. The extra space is $O(n + m + k)$ for the current signal, residual and code, plus the activations that the backward pass of the generator stores.

The cost to compare is the lasso solved by [ISTA](/iterative-shrinkage-thresholding/), with $O(mn)$ per step and no network. CSGM trades this for the much smaller number of measurements that a good generator allows.

## Properties

- **Fewer measurements.** The number of measurements scales with the latent dimension $k$ and the log of the Lipschitz constant, not with the sparsity level in a basis.
- **Bounded by the generator.** The output always lies in the range of $G$. If $x^*$ is far from the range, the error stays large however many measurements you take.
- **Not convex.** The latent search can end at different points from different starts.
- **Matrix free.** The method needs only functions for $A$, $A^T$, $G$ and $J_G^T$.
- **Measured results.** Bora et al. used a VAE with $k = 20$ on MNIST ($\lambda = 0.1$) and a DCGAN with $k = 100$ on celebA face images ($\lambda = 0.001$). With a Gaussian $A$, CSGM reached a given reconstruction error with 5 to 10 times fewer measurements than the lasso when $m$ was small. When $m$ was large, the lasso did better, because its error keeps going down while CSGM is limited by the range of the generator. These are measurements on those data sets.

## Variants and improvements

- **Sparse deviations.** Allow $x = G(z) + \nu$ with $\nu$ sparse, and penalize $\|\nu\|_1$, so that signals just outside the range can be recovered (Dhar, Grover and Ermon 2018).
- **Projected gradient.** Alternate a gradient step on $\|Ax - y\|^2$ in signal space with a projection onto the range of $G$, computed by an inner latent search or by a learned encoder (Shah and Hegde 2018).
- **Untrained generators.** Fit the weights of an untrained network instead of the code of a trained one; this is the [deep image prior](/deep-image-prior/).
- **Score-based priors.** Replace the generator by a diffusion model and sample instead of minimize; see [diffusion posterior sampling](/diffusion-posterior-sampling/).
- **Other measurement models.** The same latent search works for any differentiable forward model, for example phase retrieval or one-bit measurements, by changing the data term.

## When to use it

Use CSGM when signals of the target class are well described by a trained generator with a small latent space, when measurements are expensive, and when $A$ and the generator are both differentiable. Do not use it when the signals vary more than the generator can express, when you need recovery of fine detail that the generator did not learn, or when $m$ is large enough that the lasso or a variational method already works: then CSGM is slower and its error has a floor.

## Pitfalls

- **Representation error.** A small loss means that $AG(\hat z)$ fits the data, not that $G(\hat z)$ is close to $x^*$. Check on test signals that the range of $G$ contains good approximations.
- **No penalty.** With $\lambda = 0$ the code can grow without bound where $\tanh$ or other saturating layers are flat, and the gradient becomes too small to bring it back. A penalty keeps the code near the training distribution.
- **Step size.** The gradient scales with $\|A\|^2$ and with the Lipschitz constant of $G$. A step that is too large oscillates; the example above already overshoots in step 1.
- **Restarts are not free.** The cost grows linearly in the number of starts. Run them in parallel when possible.
- **Wrong scaling of $A$.** The theorems use $N(0, 1/m)$ entries. With $N(0, 1)$ entries the loss is $m$ times larger and the step must be $m$ times smaller.

## Implementations

The generator is a given function: the code takes $G$ and its vector-Jacobian product as arguments and runs lines L1 to L8 around them. The tests build the generator by hand, as $G(z) = (\tanh z, \tanh 2z)$, or as a one-layer network $\tanh(Wz + b)$ with weights from a fixed seed; no generator is trained. The tests check the vector-Jacobian product and the gradient against central differences, the example values above and the convergence to $z^* = 0.5$, the two exact answers of the non-example, agreement with a fine grid search when $k = 1$, exact recovery of a signal with $n = 20$, $k = 2$ and $m = 5$ for four seeds, and a seeded start that fails without restarts, while the best of four starts recovers the signal.

## History

Compressed sensing (Candes, Romberg and Tao 2006; Donoho 2006) recovers sparse signals from few random measurements, and model-based compressed sensing extended it to structured sparsity. Bora, Jalal, Price and Dimakis (2017) replaced sparsity by the range of a deep generator and gave the S-REC analysis. Later work proved that, for random ReLU generators with enough expansion, the latent loss has no stationary points except near the true code and near one negative multiple of it (Hand and Voroninski 2018), studied mismatch between the signal and the range, and moved from generators to score-based and diffusion priors.

## References
