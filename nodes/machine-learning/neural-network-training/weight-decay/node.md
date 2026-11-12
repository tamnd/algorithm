---
tag: TNFCZV
kind: technique
slug: weight-decay
name: Weight decay
aliases:
- L2 regularization
area: machine-learning/neural-network-training
level: intro
summary: "Shrink the weights toward zero at each update. For plain SGD this equals an L2 penalty on the loss with a rescaled coefficient; for momentum and Adam the two forms differ."
prereqs: [regularization, stochastic-gradient-descent, ridge-regression]
see_also: [adamw, adam, momentum-method, learning-rate-schedule, batch-normalization, weight-normalization, dropout, early-stopping]
sources:
  - url: https://arxiv.org/abs/1711.05101
    title: Ilya Loshchilov and Frank Hutter, Decoupled weight decay regularization, ICLR 2019
    locator: Section 2 (Proposition 1, the equivalence for SGD with λ' = λ/α; Proposition 2, the difference for adaptive methods), Algorithm 1 (SGDW), Algorithm 2 (AdamW)
  - book: isbn:9780262035613
    title: Ian Goodfellow, Yoshua Bengio and Aaron Courville, Deep Learning, MIT Press, 2016
    locator: Section 7.1.1 (L2 parameter regularization, the shrinkage along the eigenvectors of the Hessian)
  - url: https://arxiv.org/abs/1706.05350
    title: Twan van Laarhoven, L2 regularization versus batch and weight normalization, arXiv:1706.05350, 2017
    locator: weight decay on scale-invariant weights changes the effective learning rate, not the function
---

Weight decay is a [regularization](/regularization/) method for models trained by gradient steps: at each update it shrinks every weight toward zero by a fixed fraction. There are two forms. The L2 penalty adds $\frac{\lambda'}{2}\|\theta\|^2$ to the loss, so its gradient $\lambda' \theta$ is added to the gradient of the loss and passes through the optimizer. Decoupled weight decay leaves the loss alone and multiplies the weights by $1 - \lambda$ at each step, next to the optimizer step. For plain [stochastic gradient descent](/stochastic-gradient-descent/) the two are the same algorithm with $\lambda = \alpha \lambda'$, where $\alpha$ is the step size. For [momentum](/momentum-method/) and adaptive methods such as [Adam](/adam/) they differ, and Loshchilov and Hutter (2019) found the decoupled form to work better with Adam, which led to [AdamW](/adamw/).

## In plain words

Large weights often mean that a model has learned the noise of its training data. Weight decay keeps the weights small. At each training step every weight loses a small fixed part of its size, as if it slowly leaks away, and only a weight that keeps helping to fit the data stays large. This can be written in two ways: as a cost on large weights that is added to the error, or as a direct shrink of the weights at each step. With the simplest training method both ways give the same result. With methods that change the step size of each weight on their own, the cost is changed by the method, but the direct shrink is not, so the two ways give different models.

## When it applies

- **Problem.** [Overfitting](/overfitting/) of a model with many weights, in particular when there are more weights than training examples.
- **Part of the training loop.** The parameter update. The L2 form changes the loss, the decoupled form changes the optimizer.
- **Which weights.** Usually the weight matrices of dense and convolutional layers. Biases and the scale and shift of normalization layers are often left out.
- **Typical values.** A decay $\lambda$ per step between about $10^{-5}$ and $10^{-3}$ of the weight, chosen by [cross-validation](/cross-validation/) or a [hyperparameter search](/hyperparameter-tuning/) together with the step size.

## The template

Notation: $f$ is the training loss, $g_t$ a (stochastic) gradient of $f$ at $\theta_{t-1}$, $\alpha_t$ the step size, and OPT an optimizer that maps a gradient to a step (plain SGD, momentum, Adam).

```pseudo id=template
L2-PENALTY-STEP(θ, g, OPT)
L1  g' ← g + λ' θ                            ▷ the gradient of f + (λ'/2)||θ||²
L2  θ ← θ − OPT(g')                          ▷ the penalty passes through the optimizer

DECOUPLED-DECAY-STEP(θ, g, OPT)
L3  θ ← (1 − λ) θ − OPT(g)                   ▷ the decay acts on the weights directly
```

**Cost.** $\Theta(n)$ extra arithmetic operations per step for $n$ weights, and no extra memory.

### The two forms for plain SGD

**Claim 1 (Loshchilov and Hutter, Proposition 1).** With OPT$(g) = \alpha g$, the two templates give the same iterates from the same start when $\lambda = \alpha \lambda'$.

*Proof.* Line L2 gives $\theta - \alpha(g + \lambda'\theta) = (1 - \alpha\lambda')\theta - \alpha g$, which is line L3 with $\lambda = \alpha\lambda'$. The gradients $g$ are computed at the same point, so by induction the iterates stay equal. $\blacksquare$

The equivalence holds step by step, so with a [learning rate schedule](/learning-rate-schedule/) $\alpha_t$ a fixed decay $\lambda$ equals an L2 penalty $\lambda'_t = \lambda/\alpha_t$ that changes with time. In the other direction, a fixed penalty $\lambda'$ gives a decay $\alpha_t\lambda'$ that falls with the step size. The name "weight decay" comes from the decoupled form (Hanson and Pratt, 1988, as cited by Loshchilov and Hutter).

### What the penalty does to a quadratic loss

**Claim 2.** Let $f(\theta) = \frac12(\theta - c)^\top H (\theta - c)$ with $H$ symmetric positive semidefinite, with eigenvalues $s_i$ and orthonormal eigenvectors $q_i$. The minimizer of $f + \frac{\lambda'}{2}\|\theta\|^2$, for $\lambda' > 0$, is

$$\theta^\star = (H + \lambda' I)^{-1} H c = \sum_i \frac{s_i}{s_i + \lambda'}\,(q_i^\top c)\, q_i .$$

*Proof.* The gradient $H(\theta - c) + \lambda'\theta$ vanishes at $(H + \lambda' I)\theta = H c$, and $H + \lambda' I$ is positive definite. In the basis $q_i$ both matrices are diagonal. $\blacksquare$

So the penalty keeps the components of $c$ along directions of high curvature ($s_i \gg \lambda'$) and shrinks those along directions of low curvature ($s_i \ll \lambda'$) almost to zero: the directions in which the loss barely changes are the ones the penalty gives up. For a least squares loss this is [ridge regression](/ridge-regression/), and SGD with decoupled decay converges, by Claim 1, to the same point.

### The two forms for momentum and adaptive methods

With heavy-ball momentum the L2 gradient $\lambda'\theta$ enters the momentum buffer and is applied again at later steps, while the decoupled decay is applied once per step. With no loss gradient, step size $\alpha = 0.1$, $\lambda' = 1$, momentum $\mu = 0.9$ and $\theta_0 = 1$, two steps of the L2 form give $\theta_2 = 0.72$, and two steps of the decoupled form with $\lambda = \alpha\lambda' = 0.1$ give $\theta_2 = 0.81$.

**Claim 3 (Loshchilov and Hutter, Proposition 2, simplified).** Let OPT$(g) = \alpha P g$ with a diagonal preconditioner $P$ that is held fixed during the step and is not a multiple of the identity. Then there is no $\lambda'$ for which the L2 form equals the decoupled form with a given $\lambda > 0$ for every $\theta$.

*Proof.* The L2 form gives $\theta - \alpha P g - \alpha\lambda' P\theta$ and the decoupled form gives $\theta - \alpha P g - \lambda\theta$. These are equal for every $\theta$ only if $\alpha\lambda' P = \lambda I$, which needs $P$ to be a multiple of $I$. $\blacksquare$

In Adam the preconditioner is $P = \operatorname{diag}(1/(\sqrt{\hat v_j} + \epsilon))$, where $\hat v_j$ is the running mean of the squared gradients of weight $j$. So with the L2 form, a weight with large past gradients gets a small effective decay and a weight with small past gradients gets a large one. With the decoupled form every weight is shrunk by the same factor $1 - \lambda$ at every step.

## Classic examples

**The first step of Adam.** Take $\theta = (1, 1)$, the gradient $g = (10, 0.1)$, step size 0.1 and decay coefficient 0.1. The first Adam step after bias correction is about $-\alpha\, g_j/|g_j|$ per weight, so without decay $\theta$ becomes $(0.9, 0.9)$. With the L2 form the gradient is $(10.1, 0.2)$, which has the same signs, so the step is again $(0.9, 0.9)$: the penalty has no effect on this step. With the decoupled form, implemented as $\theta \leftarrow (1 - \alpha\lambda)\theta - \alpha \cdot \text{(Adam step)}$, the result is $(0.89, 0.89)$.

**Shrinkage on a quadratic.** For $H = \operatorname{diag}(100, 1)$, $c = (1, 1)$ and $\lambda' = 0.1$, Claim 2 gives $\theta^\star = (1000/1001, 10/11) \approx (0.999, 0.909)$: the flat direction is shrunk by 9%, the steep one by 0.1%. Plain SGD with the decoupled decay $\lambda = 0.009 \cdot 0.1$ and step size 0.009 converges to this point, and so does Adam with the L2 penalty, since its fixed points are the zeros of the penalized gradient.

## Variations

- **[AdamW](/adamw/)** is Adam with decoupled weight decay; SGDW is SGD with momentum and decoupled weight decay (Loshchilov and Hutter, Algorithms 1 and 2).
- **Normalized weight decay.** Loshchilov and Hutter also scale $\lambda$ with the square root of the batch size divided by the number of training points and epochs, to make good values transfer between runs of different length.
- **L1 penalty.** A penalty $\lambda'\|\theta\|_1$ shrinks every weight by a constant amount instead of a constant fraction, and gives exact zeros, as in [lasso regression](/lasso-regression/).
- **Max-norm.** Instead of shrinking, project each weight vector back to a ball of fixed radius after each step, as used with [dropout](/dropout/).

## Pitfalls

- **The coefficient depends on the form.** A penalty $\lambda' = 10^{-4}$ in the loss and a decay $\lambda = 10^{-4}$ per step are different by the factor $\alpha$. Libraries also differ in whether the decay of AdamW is multiplied by the step size.
- **Weights in front of a normalization layer.** If [batch normalization](/batch-normalization/) or [weight normalization](/weight-normalization/) follows a layer, the function does not depend on the scale of its weights, and decay does not regularize that function. It only keeps the weights small, which makes the effective step size larger (van Laarhoven, 2017).
- **Decaying biases and normalization scales.** Shrinking the scale $\gamma$ of a normalization layer toward zero, or the biases, can hurt and is usually turned off.
- **Tuning with the step size.** In the L2 form with plain SGD, changing $\alpha$ also changes the decay per step. In the decoupled form the two are tuned more independently, which was one of the observations of Loshchilov and Hutter.

## Exercises

1. Write out three steps of heavy-ball momentum with the L2 penalty and with decoupled decay for a one-dimensional quadratic loss, and find the decay coefficient of the decoupled form, if any, that makes the first two steps equal.
2. Show that with momentum $\mu$, the L2 form applied to a constant $\theta$ gives the effective decay $\alpha\lambda'/(1 - \mu)$ per step in the long run, and compare it with the decoupled form.
3. Use Claim 2 to show that, for least squares with design matrix $X$, the penalized minimizer is the ridge estimator $(X^\top X + \lambda' I)^{-1}X^\top y$.
4. Give a two-dimensional loss and a sequence of gradients for which Adam with the L2 penalty shrinks one weight much less than the other, while decoupled decay shrinks both by the same factor.
5. For a layer followed by batch normalization, show that the gradient of the loss is orthogonal to the weights, and that one step of SGD with decay $\lambda$ changes the norm of the weights by a factor that depends on $\lambda$ and the gradient.

## References
