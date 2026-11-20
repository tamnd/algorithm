---
tag: V9MV1X
kind: technique
slug: algorithm-unrolling
name: Algorithm unrolling
aliases:
- deep unfolding
- unrolled optimization
area: imaging-and-inverse-problems/variational-and-learned-reconstruction
level: research
summary: Turn a fixed number of iterations of a reconstruction algorithm into network layers and learn their parameters from training pairs.
prereqs: [gradient-descent, backpropagation, iterative-shrinkage-thresholding]
see_also: [lista, learned-primal-dual, variational-network-mri, proximal-gradient-method, admm, gradient-checkpointing, chebyshev-iteration, bilevel-learning-of-regularizers]
sources:
  - paper: doi:10.1109/MSP.2020.3016905
    title: "Vishal Monga, Yuelong Li and Yonina C. Eldar, Algorithm unrolling, interpretable, efficient deep learning for signal and image processing, IEEE Signal Processing Magazine 38(2), 2021"
    locator: "pages 18 to 44 (survey of the technique, its training, and unrolled networks for sparse coding, deblurring, tomography and other tasks)"
  - url: https://icml.cc/Conferences/2010/papers/449.pdf
    title: "Karol Gregor and Yann LeCun, Learning fast approximations of sparse coding, Proceedings of the 27th International Conference on Machine Learning (ICML), 2010"
    locator: "pages 399 to 406 (LISTA, the first unrolled iterative algorithm trained by backpropagation)"
---

Algorithm unrolling, also called deep unfolding, takes an iterative reconstruction method for $y = Ax + e$, keeps a fixed number $K$ of its iterations, and treats each iteration as one layer of a network. The step sizes, thresholds, matrices or small networks inside each iteration become trainable parameters $\theta_k$. Training fits them by backpropagation, so that the output after $K$ layers is close to the true image on training pairs $(x_i, y_i)$. The result is a network whose structure is that of the algorithm, with as many layers as iterations. Gregor and LeCun (2010) did this first, for ISTA in sparse coding, which gave [LISTA](/lista/). Monga, Li and Eldar (2021) survey the technique.

## In plain words

An iterative method repeats one simple update many times, and each update uses settings, such as a step size, that a person picks once for all problems. Unrolling writes down a fixed number of these updates in a row, and lets each update have its own settings. Then it tunes all the settings on examples where the right answer is known, so that the last update gives the best answer on those examples. The tuned chain is often much shorter than the original method needs, because the settings fit the kind of data that will come.

## When it applies

**Setting.** An iterative method $x_{k} = \Phi(x_{k-1}, y; \theta)$ for the problem, with parameters $\theta$, and training pairs $(x_i, y_i)$ from the same source as the test data. Each layer $\Phi_k = \Phi(\cdot, \cdot; \theta_k)$ must be differentiable in its input and its parameters, at least almost everywhere.

**The training problem.** With a loss $\ell$, such as the squared error,

$$\min_{\theta_1, \dots, \theta_K}\ \sum_i \ell\big(x_K(y_i; \theta), x_i\big), \qquad x_k = \Phi_k(x_{k-1}, y_i), \quad x_0 = 0.$$

Backpropagation through the $K$ layers gives the gradient. It runs the layers backward with the adjoints of their Jacobians, in the same way as backpropagation through time for a recurrent network.

**Fact 1 (the base method is a special case).** If every $\theta_k$ is set to the parameters of the base method, the unrolled network computes exactly $K$ iterations of it. So the best trained network is at least as good on the training data as $K$ steps of the base method, if training finds the global minimum. It does not always find it, and the training error does not bound the test error. This is a theorem about the model class, not about training.

**Fact 2 (what the gain is).** Learned parameters can make $K$ layers better than $K$ steps of the base method, often much better for small $K$, on data like the training data. On other data, there is no such guarantee, and the network can be worse than the base method. The size of the gain is a measurement for each task.

Use unrolling when a good iterative method exists, when there are training pairs, and when the reconstruction must be fast at test time. The layer structure keeps the forward map in every layer, which needs fewer parameters and less data than a generic network, and makes the network easier to read.

## The template

```pseudo id=main
UNROLLED(y, θ_1, ..., θ_K, x_0)
L1  x ← x_0
L2  for k = 1 to K                             ▷ a fixed number of layers
L3      x ← Φ(x, y; θ_k)                        ▷ hole: one iteration with learned parameters
L4  return x
```

The holes are the base iteration $\Phi$, which parameters to learn, whether the layers share them, the number of layers $K$ and the training loss. Each layer calls $A$ and $A^T$ as often as one iteration of the base method does, plus the cost of any small network inside it. Training stores the $K$ intermediate iterates for the backward pass, so memory grows as $O(Kn)$ for images with $n$ pixels; checkpointing trades this memory for recomputation.

In code, the layer map $\Phi$ and any network inside it are given functions passed as arguments, and the parameters are given lists. A test builds them by hand or from a seed, so that the answer is known. On the [LISTA](/lista/) page, the tests set the layer weights to the ISTA weights and check that the network output equals ISTA, which is Fact 1. On the [learned primal-dual](/learned-primal-dual/) page, the tests build the update maps by hand as the Chambolle-Pock maps, or as small residual networks with seeded weights, and check that the first choice gives Chambolle-Pock. This page has no code of its own.

## Classic examples

**Learned step sizes, a worked example.** Minimize $f(x) = \tfrac12x^THx - b^Tx$ with $H = \operatorname{diag}(1, 4)$, by gradient steps $x_k = x_{k-1} - \mu_k\nabla f(x_{k-1})$. The error $e_k = x_k - x^\star$ satisfies $e_k = (I - \mu_kH)e_{k-1}$, so each eigen-component of the error is multiplied by $1 - \mu_k\lambda$ for $\lambda = 1$ and $4$. Unroll two steps and compare.

- The standard step $\mu = 1/L = 1/4$ gives the factors $0.75$ and $0$. After two steps the worst factor is $0.75^2 = 0.5625$.
- The best constant step $\mu = 2/(1 + 4) = 0.4$ gives the factors $0.6$ and $-0.6$. After two steps the worst factor is $0.36$.
- The learned steps $\mu_1 = 1$ and $\mu_2 = 1/4$ give the products $(1 - 1)(1 - 1/4) = 0$ and $(1 - 4)(1 - 1) = 0$. Two layers give the exact answer from any start.

Training the per-layer steps on the error after two layers can find such steps. This is the idea of Chebyshev and other polynomial acceleration methods, learned from data instead of computed from the spectrum. For a real problem, the spectrum is not this simple and the learned steps only reduce the error on the training data.

**LISTA.** Unrolled ISTA for sparse coding, with learned matrices and thresholds. On patches of natural images, Gregor and LeCun measured that FISTA needed 18 steps to reach the error of one LISTA layer for 100 code units. See [LISTA](/lista/).

**Variational networks and learned primal-dual.** Unrolled gradient descent on a variational objective with learned filters and penalties for MRI ([variational network](/variational-network-mri/)), and unrolled primal-dual steps with small networks in the primal and dual updates for tomography ([learned primal-dual](/learned-primal-dual/)).

**ADMM-Net and others.** Unrolled ADMM for compressed sensing MRI, and unrolled half-quadratic splitting with learned denoisers. Monga, Li and Eldar give a list.

## Variations

- **Shared or separate parameters.** One set of parameters for all layers gives a recurrent network with fewer parameters; separate sets per layer give more freedom.
- **Learned operators inside a layer.** Replace a proximal step by a small network, which gives unrolled forms of [plug-and-play](/plug-and-play-priors/) methods trained end to end.
- **Fixed point training.** Run the layer to its fixed point and differentiate through the fixed point by the implicit function theorem, which uses constant memory in the number of iterations.
- **Bilevel view.** If the unrolled method minimizes an objective with parameters $\theta$, training it is an approximation of [bilevel learning](/bilevel-learning-of-regularizers/) with the lower level solved by $K$ steps.

## Pitfalls

- **Generalization.** The network is tuned to the training data and to $K$. Different noise levels, forward maps or more iterations at test time can give worse results than the base method.
- **Lost guarantees.** After training, the layers are no longer iterations of a convergent method. Running more layers does not, in general, give a better result, and the output is not a minimizer of any stated objective.
- **Memory.** Backpropagation through many layers of a large problem needs a lot of memory. Use checkpointing or a smaller $K$.
- **Unfair comparisons.** Compare the network with the base method at the same number of calls to $A$, $A^T$ and any network, and with the base method run to convergence.

## Exercises

1. Prove Fact 1 for unrolled ISTA.
2. Verify the three factors in the worked example. For $H = \operatorname{diag}(1, 4, 9)$, find three steps that give the exact answer in three layers.
3. For the two-step example, write the error after two layers as a function of $(\mu_1, \mu_2)$ for a fixed start, and find its gradient by backpropagation through the two layers.
4. Show that training with memory $O(Kn)$ is enough for backpropagation through $K$ layers, and describe how checkpointing every $\sqrt K$ layers lowers the memory.
5. Use the learned steps $1$ and $1/4$ of the worked example on a problem with the eigenvalues $1$ and $5$. Show that the worst factor after two layers is $1$, while two steps of size $1/5$ give $0.64$.

## References
