---
tag: G9XN5F
kind: concept
slug: neural-tangent-kernel
name: Neural tangent kernel
aliases:
- NTK
- NTK limit
area: machine-learning/neural-network-training
level: research
summary: "The kernel Theta(x, x') = <grad f(x), grad f(x')> of a network. In the infinite width limit it stays fixed during training, and gradient flow becomes kernel regression."
prereqs: [kernel-trick, kernel-ridge-regression, gradient-descent, backpropagation]
see_also: [gaussian-process, double-descent, relu, he-initialization, mercer-theorem, representer-theorem, positive-definite-matrix, stochastic-gradient-descent]
sources:
  - url: https://arxiv.org/abs/1806.07572
    title: Arthur Jacot, Franck Gabriel and Clément Hongler, Neural tangent kernel, convergence and generalization in neural networks, Advances in Neural Information Processing Systems 31 (NeurIPS 2018)
    locator: the NTK parameterization, Theorem 1 (the kernel at initialization tends to a deterministic limit), Theorem 2 (the kernel stays constant during training), and the section on least squares regression
  - paper: "Youngmin Cho and Lawrence K. Saul, Kernel methods for deep learning, Advances in Neural Information Processing Systems 22 (NIPS 2009)"
    locator: Section 2 (the arc cosine kernels k_n and the angular functions J_0 and J_1)
  - url: https://arxiv.org/abs/1812.07956
    title: Lénaïc Chizat, Edouard Oyallon and Francis Bach, On lazy training in differentiable programming, Advances in Neural Information Processing Systems 32 (NeurIPS 2019)
    locator: lazy training as an effect of scaling, the comparison of a model with its linearization, and the experiments where lazy training does worse
  - url: https://arxiv.org/abs/1810.02054
    title: Simon S. Du, Xiyu Zhai, Barnabás Póczos and Aarti Singh, Gradient descent provably optimizes over-parameterized neural networks, ICLR 2019
    locator: the Gram matrix of a two layer ReLU network, its positive definiteness, and linear convergence of gradient descent for large width
  - url: https://arxiv.org/abs/1902.06720
    title: Jaehoon Lee, Lechao Xiao, Samuel S. Schoenholz, Yasaman Bahri, Roman Novak, Jascha Sohl-Dickstein and Jeffrey Pennington, Wide neural networks of any depth evolve as linear models under gradient descent, NeurIPS 2019
    locator: the linearized network and the closed form of its training dynamics under gradient flow
  - url: https://arxiv.org/abs/1904.11955
    title: Sanjeev Arora, Simon S. Du, Wei Hu, Zhiyuan Li, Ruslan Salakhutdinov and Ruosong Wang, On exact computation with an infinitely wide neural net, NeurIPS 2019
    locator: the convolutional NTK and its exact computation
---

The neural tangent kernel (NTK) of a network $f(x; \theta)$ is the kernel $\Theta(x, x') = \langle \nabla_\theta f(x; \theta), \nabla_\theta f(x'; \theta) \rangle$. It describes how one step of [gradient descent](/gradient-descent/) on one example changes the output at every other input. Jacot, Gabriel and Hongler (2018) proved that for a multilayer perceptron in the *NTK parameterization*, the kernel at a random initialization tends to a fixed limit as the widths grow, and stays at that limit during training. In that limit, training by gradient flow on squared loss is [kernel regression](/kernel-ridge-regression/) with the limit kernel.

## In plain words

A network has many weights. When training moves the weights a little, the output for each input moves too. The tangent kernel is a table of numbers, one for each pair of inputs, that says how much a step that helps one input also moves the output for the other input. For a small network this table changes a lot while it trains, because the weights move far. For a very wide network, set up in the right way, each weight moves only a tiny amount, and the table hardly changes. Then the network behaves like a fixed kernel method: its final predictions are a weighted sum of the kernel values between the new input and the training inputs. This gives a way to study wide networks with the exact tools of kernel methods.

## The idea

**Setting and notation.** The architecture is a multilayer perceptron $f(\cdot; \theta) : \mathbb{R}^d \to \mathbb{R}$ with parameters $\theta \in \mathbb{R}^P$. There are $n$ training examples $(x_i, y_i)$ and the loss is the mean squared error $L(\theta) = \frac{1}{2n} \sum_{i=1}^n (f(x_i; \theta) - y_i)^2$. The method changes nothing in the training loop; it is a way to analyze plain gradient descent, taken in the limit of a small learning rate $\eta$ (gradient flow $\dot\theta_t = -\nabla L(\theta_t)$).

**The kernel moves the outputs.** For any differentiable network, the chain rule gives

$$\frac{d}{dt} f(x; \theta_t) = \nabla_\theta f(x; \theta_t)^\top \dot\theta_t = -\frac{1}{n} \sum_{i=1}^n \Theta_t(x, x_i)\,\big(f(x_i; \theta_t) - y_i\big),$$

where $\Theta_t(x, x') = \nabla_\theta f(x; \theta_t)^\top \nabla_\theta f(x'; \theta_t)$. This is an identity, not an approximation. The kernel $\Theta_t$ is a Gram matrix of gradients, so it is positive semidefinite. In general it depends on $\theta_t$ and changes as the network trains.

**The NTK parameterization.** Each layer computes $\alpha^{(l+1)} = \frac{1}{\sqrt{n_l}} W^{(l)} \sigma(\alpha^{(l)}) + \beta b^{(l)}$, where $n_l$ is the width of layer $l$ and all entries of $W^{(l)}$ and $b^{(l)}$ are drawn i.i.d. $N(0, 1)$. The factor $1/\sqrt{n_l}$ sits in the forward pass rather than in the variance of the initial weights. The function at initialization has the same law as with [He](/he-initialization/) or LeCun scaling, but the gradient with respect to each weight is $1/\sqrt{n_l}$ times smaller, so with a fixed $\eta$ each single weight moves by $O(1/\sqrt{n_l})$.

**Theorem (Jacot, Gabriel and Hongler 2018).** Let $\sigma$ be Lipschitz and twice differentiable with a bounded second derivative. Let the hidden widths $n_1, \ldots, n_{L-1}$ tend to infinity one after the other.

1. At initialization, $\Theta_0$ converges in probability to a deterministic kernel $\Theta_\infty$, given by a recursion over the layers.
2. For any $T$ such that the training direction stays bounded on $[0, T]$ (for squared loss it does), $\Theta_t$ converges uniformly on $[0, T]$ to the same $\Theta_\infty$.

The ReLU does not meet the smoothness hypothesis. Later work proved the same limits for ReLU networks, with widths that grow together and with explicit rates (for example Arora et al. 2019 and Lee et al. 2019).

**Training in the limit is kernel regression.** Replace $\Theta_t$ by a fixed $\Theta$ in the identity above. Let $u_t = (f(x_i; \theta_t))_i$, $K = (\Theta(x_i, x_j))_{ij}$, and assume $K$ is positive definite. The training outputs follow the linear system $\dot u_t = -\frac1n K (u_t - y)$, whose solution is

$$u_t = y + e^{-tK/n}(u_0 - y).$$

So the training error goes to 0 at the rate $e^{-\lambda_{\min}(K)\, t/n}$. For any input $x$, integrating the identity gives

$$f(x; \theta_t) = f(x; \theta_0) + \Theta(x, X)\, K^{-1} \big(I - e^{-tK/n}\big)\big(y - u_0\big),$$

and as $t \to \infty$,

$$f_\infty(x) = f(x; \theta_0) + \Theta(x, X)\, K^{-1}\big(y - f(X; \theta_0)\big).$$

This is kernel regression without a penalty (the limit $\lambda \to 0$ of [kernel ridge regression](/kernel-ridge-regression/)) with the kernel $\Theta$, fitted to the residual of the initial function. Since $f(\cdot; \theta_0)$ is random, the trained limit network is a random function. In the infinite width limit $f(\cdot; \theta_0)$ is a centered [Gaussian process](/gaussian-process/), so the trained function is a Gaussian process too, with mean $\Theta(x, X) K^{-1} y$.

**The two layer ReLU case in closed form.** Take $f(x) = \frac{1}{\sqrt m} \sum_{j=1}^m a_j\, \mathrm{relu}(w_j^\top x)$ with $w_j \sim N(0, I_d)$ and $a_j \sim N(0, 1)$. The gradients are $\partial f/\partial a_j = \mathrm{relu}(w_j^\top x)/\sqrt m$ and $\partial f/\partial w_j = a_j \mathbf{1}[w_j^\top x > 0]\, x/\sqrt m$. So the empirical NTK is the average of $m$ i.i.d. terms,

$$\Theta_m(x, x') = \frac1m \sum_{j=1}^m \Big( \mathrm{relu}(w_j^\top x)\,\mathrm{relu}(w_j^\top x') + a_j^2\, \mathbf{1}[w_j^\top x > 0]\,\mathbf{1}[w_j^\top x' > 0]\; x^\top x' \Big),$$

and by the law of large numbers it tends almost surely to its mean. Let $\vartheta$ be the angle between $x$ and $x'$. The arc cosine kernels of Cho and Saul (2009) are

$$k_0(x, x') = 1 - \frac{\vartheta}{\pi}, \qquad k_1(x, x') = \frac{\lVert x \rVert \lVert x' \rVert}{\pi}\big(\sin\vartheta + (\pi - \vartheta)\cos\vartheta\big),$$

and they satisfy $\mathbb{E}[\mathbf{1}[w^\top x > 0]\mathbf{1}[w^\top x' > 0]] = k_0/2$ and $\mathbb{E}[\mathrm{relu}(w^\top x)\,\mathrm{relu}(w^\top x')] = k_1/2$ for $w \sim N(0, I_d)$. With $\mathbb{E}[a_j^2] = 1$ and $a_j$ independent of $w_j$,

$$\Theta_\infty(x, x') = \tfrac12 k_1(x, x') + \tfrac12 k_0(x, x')\, x^\top x'.$$

The first term alone is the kernel of the Gaussian process that the network is at initialization (the NNGP kernel). The second term comes from training the first layer. At $x = x'$, $\vartheta = 0$ and $\Theta_\infty(x, x) = \lVert x \rVert^2$. Each term of $\Theta_m$ is bounded on bounded inputs, so the error $\Theta_m - \Theta_\infty$ has standard deviation of order $1/\sqrt m$.

**Lazy training.** Chizat, Oyallon and Bach (2019) showed that the kernel regime is not special to width. For any model $h(\theta)$, train $\alpha\, h(\theta)$ with the loss scaled by $1/\alpha^2$. As $\alpha \to \infty$, the trained model stays close to its linearization $h(\theta_0) + \nabla h(\theta_0)^\top(\theta - \theta_0)$, because a tiny move of $\theta$ is enough to fit the data. The $1/\sqrt{n_l}$ factor of the NTK parameterization is one such scaling. In the lazy regime the features do not change, so the network learns nothing that the fixed kernel cannot. With the *mean field* scaling $1/m$ instead of $1/\sqrt m$ in the last layer, a two layer network leaves the kernel regime and its hidden units move by order 1.

## Examples

**The limit kernel at one pair.** Take $x = (1, 0)$ and $x' = (0.6, 0.8)$, both of norm 1, so $\cos\vartheta = 0.6$ and $\vartheta = 0.9273$. Then $k_0 = 0.7048$, $k_1 = 0.6775$ and $\Theta_\infty(x, x') = 0.3388 + 0.5 \cdot 0.7048 \cdot 0.6 = 0.5502$. For orthogonal unit inputs $\vartheta = \pi/2$, $k_0 = 1/2$, $k_1 = 1/\pi$ and $\Theta_\infty = 1/(2\pi) = 0.1592$. For opposite inputs both kernels are 0: no hidden unit is active on both.

**The empirical kernel at finite width.** For the same pair, draw 20 networks of each width with `random.Random(s)`, $s = 0, \ldots, 19$, and compute $\Theta_m(x, x')$ exactly from the gradients.

| width $m$ | mean of $\Theta_m$ | standard deviation |
|---|---|---|
| 10 | 0.4556 | 0.3681 |
| 100 | 0.5524 | 0.1277 |
| 1000 | 0.5576 | 0.0328 |
| 10000 | 0.5517 | 0.0094 |

The spread falls by a factor of about $\sqrt{10} \approx 3.2$ for each factor of 10 in width, as the law of large numbers predicts, and the values gather around $0.5502$.

**The kernel during training.** Train the same network by full batch gradient descent with $\eta = 0.5$ for 150 steps on four inputs $(1, 0), (0.6, 0.8), (-0.5, 0.5), (0.3, -1.2)$ with targets $1, -1, 0.5, 0$, from `random.Random(5)`. Measure the change of the $4 \times 4$ kernel matrix in the Frobenius norm, relative to its initial value, and the relative change of $\theta$.

| width $m$ | final loss | kernel change | parameter change |
|---|---|---|---|
| 20 | $1.3 \times 10^{-4}$ | 0.286 | 0.383 |
| 200 | $9.2 \times 10^{-5}$ | 0.033 | 0.151 |
| 2000 | $9.0 \times 10^{-6}$ | 0.011 | 0.049 |

All three widths fit the data. The wide network does so with a small relative move of its parameters and an almost constant kernel, which is the lazy regime.

**Non-example.** A network in the mean field scaling, or a narrow network with a large learning rate, changes its kernel by order 1 during training. Its trained function is not the kernel regression above, and in many experiments it predicts better than the kernel limit, because it learns features from the data.

## Where it is used

- **Convergence proofs.** If the smallest eigenvalue of the limit Gram matrix $K$ is positive and the width is large enough, gradient descent on a two layer ReLU network reaches zero training loss at a linear rate (Du et al. 2019). Du et al. show that $K$ is positive definite when no two training inputs are parallel. The required width in these proofs is a polynomial in $n$ and $1/\lambda_{\min}(K)$, far above practical widths.
- **Kernels from architectures.** The limit kernel of a convolutional network (the CNTK of Arora et al. 2019) can be computed exactly and used in a kernel machine. This gives a baseline for what a network does without feature learning.
- **Generalization and double descent.** In the kernel limit, the trained network is a minimum norm interpolant in the kernel's feature space, so the theory of interpolating kernel fits and of [double descent](/double-descent/) applies to it.
- **Initialization and conditioning.** The spectrum of the NTK at initialization governs the speed of early training along each direction, which connects to the choice of [initialization](/he-initialization/) and of the learning rate.
- **Pitfalls.** The limit needs the NTK parameterization or another lazy scaling; with the usual parameterization and a learning rate tuned for a finite network, the kernel does change. The theorem holds for a fixed training time as the width grows, not uniformly in time. The empirical NTK of a trained network is a different kernel from the limit at initialization. The limit network is still random through $f(\cdot; \theta_0)$; ignoring that term gives the wrong predictions unless the initial output is set to 0.

## References
