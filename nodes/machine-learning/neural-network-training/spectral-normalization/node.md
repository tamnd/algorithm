---
tag: FFNMF4
kind: technique
slug: spectral-normalization
name: Spectral normalization
area: machine-learning/neural-network-training
level: research
summary: "Divide each weight matrix by its largest singular value, estimated with one power iteration step per update, so that each linear layer is 1-Lipschitz in the l2 norm."
prereqs: [power-iteration, singular-value-decomposition, matrix-norms, backpropagation]
see_also: [weight-normalization, batch-normalization, lipschitz-condition, rayleigh-quotient, gradient-clipping, adversarial-training, symmetric-eigenproblem]
sources:
  - url: https://arxiv.org/abs/1802.05957
    title: Takeru Miyato, Toshiki Kataoka, Masanori Koyama and Yuichi Yoshida, Spectral normalization for generative adversarial networks, ICLR 2018
    locator: Section 2 (the Lipschitz bound by the product of spectral norms, the normalized weight W/σ(W)), Section 2.1 (the power iteration estimate), Section 2.2 (the gradient), Appendix A (Algorithm 1)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 4 (the singular value decomposition), Lecture 5 (the 2-norm equals the largest singular value), Lecture 27 (power iteration)
  - url: https://arxiv.org/abs/1805.10408
    title: Hanie Sedghi, Vineet Gupta and Philip M. Long, The singular values of convolutional layers, ICLR 2019
    locator: the exact singular values of a multichannel convolution by the Fourier transform
---

Spectral normalization (Miyato, Kataoka, Koyama and Yoshida, 2018) replaces each weight matrix $W$ of a network by $W_{\mathrm{SN}} = W/\sigma(W)$, where $\sigma(W)$ is the largest [singular value](/singular-value-decomposition/) of $W$. Since $\sigma(W)$ is the [operator norm](/matrix-norms/) of $W$ for the Euclidean norm, the normalized layer $x \mapsto W_{\mathrm{SN}} x$ is 1-Lipschitz, and a network built from such layers and 1-Lipschitz activations is 1-Lipschitz. Computing $\sigma(W)$ exactly at every step costs a full singular value decomposition, so the method keeps one vector $u$ per layer and does one step of [power iteration](/power-iteration/) per training update. The weights move little between updates, so the estimate from one step stays close to $\sigma(W)$. The method was made for the discriminator of generative adversarial networks, where a Lipschitz bound keeps training stable.

## In plain words

A layer of a network multiplies its input by a table of weights. Some inputs get stretched more than others, and the largest stretch is one number that belongs to the table. Spectral normalization divides the whole table by that number, so no input is stretched by more than a factor of one. Then two inputs that are close give outputs that are at least as close, through every layer, and the network cannot react wildly to a small change in its input. Finding the largest stretch exactly is slow, so the method keeps a guess of the most stretched direction and improves the guess a little at each training step. As the weights change slowly, a little work each step is enough.

## When it applies

- **Architecture.** Dense layers, and convolutional layers with the kernel reshaped to a matrix. Mostly used in the discriminator or critic of a generative adversarial network, and in other models that need a bound on how fast the output changes with the input.
- **Part of the training loop.** The parameterization of each weight matrix: the forward pass uses $W/\tilde\sigma$, and [backpropagation](/backpropagation/) passes through the division.
- **What it controls.** The Lipschitz constant in the $\ell_2$ norm, not the scale of the activations. It does not depend on the batch, so it acts the same in training and in use.
- **Cost model.** Two products with $W$ per update, against the $\Theta(m k n)$ of the layer on a batch of $m$ examples.

## The template

Notation: $W$ is $n \times k$ with singular values $\sigma_1 \ge \sigma_2 \ge \dots \ge 0$ and top singular vectors $u_1, v_1$, so $W v_1 = \sigma_1 u_1$ and $\sigma_1 = \max_{\|x\| = 1}\|W x\|$. Each layer stores a unit vector $u \in \mathbb{R}^n$, drawn at random once and kept across updates.

```pseudo id=template
SN-STEP(W, u)                                       ▷ Algorithm 1 of Miyato et al., once per update
L1  v ← Wᵀu / ||Wᵀu||                               ▷ one power iteration step on WᵀW and WWᵀ
L2  u ← W v / ||W v||
L3  σ̃ ← uᵀ W v                                      ▷ equals ||W v||
L4  W_SN ← W / σ̃                                    ▷ the forward pass uses W_SN
L5  compute the loss and G = ∂L/∂W_SN by backpropagation
L6  ∂L/∂W ← (G − ⟨G, W_SN⟩ u vᵀ) / σ̃              ▷ u, v are treated as the singular vectors
L7  update W with ∂L/∂W; keep u for the next call
```

**Cost.** Lines L1 to L4 and L6 take $\Theta(nk)$ arithmetic operations, the cost of a few passes over $W$, independent of the batch size. The memory is one vector of length $n$ per layer. A full singular value decomposition would cost $\Theta(nk\min(n,k))$ at every update.

### The Lipschitz bound

**Claim 1.** For any matrix $W$ with $\sigma(W) > 0$, $\|W_{\mathrm{SN}} x - W_{\mathrm{SN}} y\| \le \|x - y\|$, with equality for $x - y$ parallel to $v_1$. For a network $f = W_L \circ \phi \circ W_{L-1} \circ \dots \circ \phi \circ W_1$ in which $\phi$ is 1-Lipschitz (ReLU, leaky ReLU with slope at most 1, tanh), $\|f(x) - f(y)\| \le \prod_l \sigma(W_l)\, \|x - y\|$.

*Proof.* $\|W x\| \le \sigma_1 \|x\|$ for every $x$, since $\sigma_1$ is the $\ell_2$ operator norm, with equality at $x = v_1$. Dividing by $\sigma_1$ gives the first part, applied to $x - y$. For the network, each map in the composition is Lipschitz, and the Lipschitz constant of a composition is at most the product of the constants. A ReLU is 1-Lipschitz coordinatewise, $|\max(a,0) - \max(b,0)| \le |a - b|$, so it is 1-Lipschitz in $\ell_2$. $\blacksquare$

With every $W_l$ normalized, the bound is 1. It can be loose: the product bounds each layer at its own worst direction, and the worst directions of consecutive layers need not line up.

### The power iteration estimate

**Claim 2.** After lines L1 to L3, $\tilde\sigma = \|W v\| \le \sigma_1$. If $u$ has a nonzero component along $u_1$ and $\sigma_1 > \sigma_2$, repeated calls with a fixed $W$ give $\tilde\sigma \to \sigma_1$, with an error that shrinks by about the factor $(\sigma_2/\sigma_1)^2$ per call.

*Proof.* $u = W v/\|W v\|$ gives $u^\top W v = \|W v\|$, and $\|W v\| \le \sigma_1$ because $\|v\| = 1$. One call maps $u$ to a multiple of $W W^\top u$, which is one step of power iteration for the symmetric matrix $W W^\top$, whose eigenvalues are $\sigma_i^2$. The component of $u$ along $u_i$ is multiplied by $\sigma_i^2$ at each step, so the direction of $u$ converges to $\pm u_1$ at the rate $(\sigma_2/\sigma_1)^2$, and $v$ to $\pm v_1$. Then $\|W v\| \to \sigma_1$. $\blacksquare$

During training $W$ changes by a small step between calls, so the vector $u$ from the last call is already close to the new $u_1$, and one step keeps it close. The estimate lags by about one step of the optimizer and is always from below.

### The gradient

**Claim 3.** If $\sigma_1$ is a simple singular value, then $\partial \sigma_1/\partial W = u_1 v_1^\top$, and for a loss $L(W_{\mathrm{SN}})$ with $G = \partial L/\partial W_{\mathrm{SN}}$,

$$\frac{\partial L}{\partial W} = \frac{1}{\sigma_1}\Big(G - \langle G, W_{\mathrm{SN}}\rangle\, u_1 v_1^\top\Big), \qquad \langle A, B\rangle = \sum_{ij} A_{ij} B_{ij}.$$

*Proof.* $\sigma_1 = u_1^\top W v_1$ with unit vectors $u_1, v_1$. Differentiating, $d\sigma_1 = du_1^\top W v_1 + u_1^\top dW\, v_1 + u_1^\top W dv_1$. The first term is $\sigma_1 du_1^\top u_1 = 0$, since $u_1$ stays a unit vector, and in the same way the third term is $\sigma_1 v_1^\top dv_1 = 0$. So $d\sigma_1 = u_1^\top dW\, v_1 = \langle u_1 v_1^\top, dW\rangle$. For $W_{\mathrm{SN}} = W/\sigma_1$, $dW_{\mathrm{SN}} = dW/\sigma_1 - W\, d\sigma_1/\sigma_1^2$, so $dL = \langle G, dW\rangle/\sigma_1 - \langle G, W\rangle \langle u_1 v_1^\top, dW\rangle/\sigma_1^2$, which is the formula. $\blacksquare$

The second term removes from $G$ the part that only changes the top singular value: a step along $u_1 v_1^\top$ would change $\sigma_1$ and $W$ together and leave $W_{\mathrm{SN}}$ the same. Miyato et al. (Section 2.2) read the second term as a penalty that keeps the layer from using only one direction. In line L6 the estimates $u, v$ replace $u_1, v_1$.

## Classic examples

**A 2 by 2 matrix.** Take $W = \begin{pmatrix} 3 & 0 \\ 4 & 5 \end{pmatrix}$. Then $W^\top W = \begin{pmatrix} 25 & 20 \\ 20 & 25 \end{pmatrix}$ has eigenvalues 45 and 5, so $\sigma_1 = 3\sqrt5 \approx 6.708204$ and $\sigma_2 = \sqrt5$, with $v_1 = (1, 1)/\sqrt2$. Start from $u = (1, 0)$. The first call gives $v = (1, 0)$, $W v = (3, 4)$, so $\tilde\sigma = 5$ and $u = (0.6, 0.8)$. The next calls give:

| call | $\tilde\sigma$ | $\sigma_1 - \tilde\sigma$ |
|---|---|---|
| 1 | 5.000000 | 1.71 |
| 2 | 6.671746 | 0.0365 |
| 3 | 6.707750 | 0.000454 |
| 4 | 6.708198 | 0.00000561 |
| 5 | 6.708204 | 0.0000000693 |

The error of $\tilde\sigma$ falls by a factor of about 81 per call. The angle between $v$ and $v_1$ falls by about $(\sigma_2/\sigma_1)^2 = 1/9$ per call, and the error of $\tilde\sigma$ is of the order of the square of that angle.

**A slowly moving matrix.** A random $5 \times 4$ matrix, warmed up with 30 calls and then changed by Gaussian noise of standard deviation 0.001 per entry before each call, keeps an estimate within 0.1% of the exact $\sigma_1$ over 50 updates, with one power step per update.

**A normalized ReLU network.** Three random layers of sizes $4 \to 6 \to 5 \to 3$, each divided by its exact $\sigma_1$, with ReLU between them, never increase the distance of two random inputs, as Claim 1 says.

## Variations

- **More power steps.** Some implementations do several steps per update, or several at the first update to warm up $u$.
- **Convolutions.** Miyato et al. reshape the kernel of shape $c_{\mathrm{out}} \times c_{\mathrm{in}} \times h \times w$ to a matrix of size $c_{\mathrm{out}} \times c_{\mathrm{in}} h w$. Running power iteration on the convolution itself, with a convolution and a transposed convolution in place of $W$ and $W^\top$, bounds the true operator norm. Sedghi, Gupta and Long (2019) compute all singular values of a convolution with periodic padding by the Fourier transform.
- **A soft bound.** Divide by $\max(1, \tilde\sigma/c)$ instead of $\tilde\sigma$, so that only layers with norm above $c$ are scaled down.
- **[Weight normalization](/weight-normalization/)** divides each row by its own norm, which is a different bound: the largest row norm is at most $\sigma_1$, and $\sigma_1$ is at most $\sqrt{n}$ times the largest row norm.

## Pitfalls

- **The estimate is from below.** Claim 2 gives $\tilde\sigma \le \sigma_1$, so $\sigma(W/\tilde\sigma) = \sigma_1/\tilde\sigma \ge 1$. The layer is 1-Lipschitz only in the limit; with a poor or fresh $u$ the bound can fail by a large factor.
- **Do not reset $u$.** Drawing a new $u$ at each update makes the single step a poor estimate. The vector $u$ is state that belongs to the layer, like the running statistics of [batch normalization](/batch-normalization/), and must be saved with the model.
- **The reshaped kernel is not the convolution.** For one channel and a $3 \times 3$ kernel of ones, the reshaped matrix is one row with norm 3, but the convolution with periodic padding maps a constant image to 9 times itself, so its operator norm is 9. For one channel the gap can be a factor up to $\sqrt{h w}$.
- **Gradient through $u$ and $v$.** Claim 3 holds without differentiating through the power step only because $u_1, v_1$ are exact singular vectors. Treating the estimates as constants is the usual choice and gives a small error while they lag.
- **Equal top singular values.** If $\sigma_1 = \sigma_2$, $\sigma_1$ is not differentiable at $W$, and power iteration converges only to a vector in the top singular subspace. The value $\tilde\sigma$ still converges.
- **The bound is on the network, not on the loss.** A 1-Lipschitz network can still have a steep loss if the loss itself is steep in its input.

## Exercises

1. Show that $\sigma_1(W) = \max_{\|x\| = \|y\| = 1} y^\top W x$, and use it to give a second proof that $\tilde\sigma \le \sigma_1$.
2. For $W = \begin{pmatrix} 2 & 0 \\ 0 & 1 \end{pmatrix}$ and $u = (1, 1)/\sqrt2$, compute $\tilde\sigma$ after one and two calls of SN-STEP.
3. Show that the gradient in Claim 3 satisfies $\langle \partial L/\partial W, W\rangle = 0$. Explain this from the fact that $L(c W) = L(W)$ for every $c > 0$.
4. Give two $2 \times 2$ matrices $A$, $B$ with $\sigma(A) = \sigma(B) = 1$ and $\sigma(AB) < 1/2$, which shows that the bound of Claim 1 can be loose.
5. Compute the singular values of the circular convolution of a length 4 signal with the kernel $(1, 1, 0, 0)$, and compare the largest with the norm of the kernel.

## References
