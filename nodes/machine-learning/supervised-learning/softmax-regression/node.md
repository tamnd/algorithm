---
tag: 789V98
kind: algorithm
slug: softmax-regression
name: Softmax regression
aliases:
- multinomial logistic regression
- multiclass logistic regression
- maximum entropy classifier
area: machine-learning/supervised-learning
level: intro
summary: Logistic regression for K classes. P(y = k | x) is the softmax of K linear scores, fit by minimizing cross-entropy, with gradient X^T(P - Y)/n.
solves: [multiclass-classification]
model: real-ram
complexity:
  vars: {n: the number of examples, d: the number of features, K: the number of classes, t: the number of iterations}
  time: {worst: O(t n K d)}
  space: {extra: Θ(K d)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1959
  people: [R. Duncan Luce, Daniel McFadden, David Cox]
  note: The softmax form is Luce's choice axiom (1959). Cox (1966) and McFadden (1974) used it as the multinomial logit model.
prereqs: [logistic-regression, log-sum-exp-trick]
see_also: [multiclass-classification, cross-entropy-loss, gradient-descent, stochastic-gradient-descent, generalized-linear-model, exponential-family-distribution, limited-memory-bfgs, regularization]
sources:
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: Section 4.3.4 (multiclass logistic regression, the softmax, the gradient and the Hessian)
  - book: isbn:9780262046824
    title: Kevin P. Murphy, Probabilistic Machine Learning, An Introduction, MIT Press, 2022
    locator: Section 10.3 (multinomial logistic regression, the overparameterization and the gradient)
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 4.4 (the multiclass logistic model with the last class as reference)
  - book: isbn:9780262035613
    title: Ian Goodfellow, Yoshua Bengio and Aaron Courville, Deep Learning, MIT Press, 2016
    locator: Section 4.1 (overflow and underflow, and the stable softmax) and Section 6.2.2.3 (softmax units for multinoulli output)
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 9.3 (gradient descent and its convergence for smooth convex functions)
---

Softmax regression is [logistic regression](/logistic-regression/) for $K \ge 2$ classes. It computes one linear score $z_k = b_k + w_k^\top x$ for each class and turns the scores into probabilities with the softmax function, $P(y = k \mid x) = e^{z_k}/\sum_j e^{z_j}$. The weights are fit by maximum likelihood, which is the same as minimizing the [cross-entropy loss](/cross-entropy-loss/). The loss is convex, its gradient is the simple matrix $\frac1n\tilde X^\top(P - Y)$, and it has no closed form minimizer, so it is fit by [gradient descent](/gradient-descent/), Newton or quasi-Newton methods. The model is overparameterized: adding the same vector to all $K$ weight vectors does not change any probability. For $K = 2$ it is exactly logistic regression.

## In plain words

You want to put each example into one of several classes, and you want a probability for each class. Softmax regression gives every class its own weighted sum of the inputs, a score. A higher score means a more likely class. To turn the scores into probabilities, it raises the number $e$ to the power of each score and divides each result by their total, so the probabilities are positive and add up to one.

The weights are chosen to make the true classes of the training examples as likely as possible. A simple method starts with all weights at zero. At each step, for each example, it compares the predicted probabilities with the true class and moves the weights a little to reduce the difference.

## The problem

The data are $(x_i, y_i)$, $i = 1, \dots, n$, with $x_i \in \mathbb{R}^d$ and $y_i \in \{1, \dots, K\}$. Write $\tilde x_i = (1, x_i)$ and let $\tilde X$ be the $n \times (d+1)$ matrix with rows $\tilde x_i^\top$. The parameters are $W \in \mathbb{R}^{(d+1) \times K}$, whose column $k$ is $\theta_k = (b_k, w_k)$. Let $Y$ be the $n \times K$ one-hot matrix with $Y_{ik} = 1$ when $y_i = k$. The model is

$$P(y = k \mid x_i) = P_{ik} = \frac{e^{z_{ik}}}{\sum_{j=1}^{K} e^{z_{ij}}}, \qquad z_i = W^\top\tilde x_i .$$

The fitting problem is to minimize the mean negative log-likelihood plus an optional L2 penalty on the weights (not on the biases):

$$J(W) = \frac1n\sum_{i=1}^{n}\Bigl[\log\sum_{j=1}^{K} e^{z_{ij}} - z_{i, y_i}\Bigr] + \frac{\lambda}{2}\sum_{k=1}^{K}\|w_k\|^2 .$$

**The gradient.** For one example, $\partial/\partial z_{ik}$ of $\log\sum_j e^{z_{ij}} - z_{i,y_i}$ is $P_{ik} - Y_{ik}$. By the chain rule,

$$\nabla_W J = \frac1n\tilde X^\top(P - Y) + \lambda\bar W,$$

where $\bar W$ is $W$ with its bias row set to 0. This has the same form as the gradient $\tilde X^\top(p - y)$ of logistic regression.

**Convexity.** The Hessian of $\log\sum_j e^{z_j}$ in $z$ is $\operatorname{diag}(p) - pp^\top$, which is positive semidefinite: $u^\top(\operatorname{diag}(p) - pp^\top)u$ is the variance of $u_k$ under the distribution $p$. A convex function of a linear map is convex, so $J$ is convex.

**The overparameterization.** Replacing each $\theta_k$ by $\theta_k + c$ for a fixed $c \in \mathbb{R}^{d+1}$ adds $c^\top\tilde x_i$ to every score of example $i$, and the softmax does not change. So the likelihood has a flat direction, and $J$ with $\lambda = 0$ is never strictly convex. Two common fixes:

- **Fix one class at 0.** Set $\theta_K = 0$ and fit the other $K - 1$ columns. Then $z_{ik}$ is the log-odds of class $k$ against class $K$, as in ESL Section 4.4. For $K = 2$ this gives logistic regression with $w = \theta_1$.
- **Penalize.** With $\lambda > 0$, the penalty $\sum_k\|w_k + c_w\|^2$ is smallest at $c_w = -\frac1K\sum_k w_k$. So each minimizer has $\sum_k w_k = 0$.

## The algorithm

Gradient descent with a fixed step $\eta = 1/L$, where $L$ bounds the Lipschitz constant of $\nabla J$.

```pseudo id=main
SOFTMAX-GD(X, y, K, λ, tol)
L1  W ← 0;  η ← 1 / L  with  L = ‖X̃‖_F² / (2n) + λ
L2  repeat
L3      for each i: z ← Wᵀx̃_i;  m ← max_k z_k;  P[i][k] ← e^{z_k − m} / Σ_j e^{z_j − m};   G ← X̃ᵀ(P − Y)/n + λ W̄
L4      compute ‖G‖_F
L5      if ‖G‖_F ≤ tol then return W
L6      W ← W − η G
L7  return W                                ▷ only if an iteration limit is reached
```

**The log-sum-exp trick.** Line L3 subtracts the largest score $m$ before it takes exponentials. This does not change $P$, because the factor $e^{-m}$ cancels, but now the largest exponent is $e^0 = 1$, so no exponential overflows, and the sum is at least 1, so it does not underflow to 0. The loss uses the same idea: $\log\sum_j e^{z_j} = m + \log\sum_j e^{z_j - m}$. See the [log-sum-exp trick](/log-sum-exp-trick/). Without it, a score of 710 already gives $e^{710} = \infty$ in double precision, and $P$ becomes $\infty/\infty$.

**The step size.** For each example the Hessian in $z$ is $\operatorname{diag}(p) - pp^\top$, and its largest eigenvalue is at most $1/2$: the variance of $u_k$ is at most $(\max_k u_k - \min_k u_k)^2/4 \le \|u\|^2/2$. So the Hessian of $J$ is at most $\frac1n\sum_i\frac12\|\tilde x_i\|^2 + \lambda = L$ in norm, and the step $1/L$ is safe.

**Staying in the right subspace.** The columns of $P - Y$ sum to zero in each row, so the columns of $\frac1n\tilde X^\top(P - Y)$ sum to the zero vector. Starting from $W = 0$, the sum of the columns of $W$ stays 0 for the data part, and the penalty part is $\lambda$ times that sum. So gradient descent never moves along the flat direction.

## Example

Three classes on a line, $K = 3$, $n = 6$, $\lambda = 0.1$:

| $x$ | $-2$ | $-1$ | 0 | 0 | 1 | 2 |
|---|---|---|---|---|---|---|
| $y$ | 1 | 1 | 2 | 2 | 3 | 3 |

At $W = 0$ all probabilities are $1/3$. The classes are balanced, so the bias gradients are 0, and the weight gradients are $\frac16\sum_i x_i(1/3 - Y_{ik}) = (0.5, 0, -0.5)$. Line L1 gives $L = \frac{1}{12}\sum_i(1 + x_i^2) + 0.1 = 16/12 + 0.1 = 1.4333$ and $\eta = 0.6977$.

| iteration | $(b_1, w_1)$ | $(b_2, w_2)$ | $(b_3, w_3)$ | $J$ |
|---|---|---|---|---|
| 0 | $(0, 0)$ | $(0, 0)$ | $(0, 0)$ | $\log 3 = 1.0986$ |
| 1 | $(0, -0.3488)$ | $(0, 0)$ | $(0, 0.3488)$ | 0.82736 |
| 2 | $(-0.0071, -0.5466)$ | $(0.0143, 0)$ | $(-0.0071, 0.5466)$ | 0.73486 |
| 10 | $(-0.1326, -1.0390)$ | $(0.2653, 0)$ | $(-0.1326, 1.0390)$ | 0.62047 |
| 100 | $(-0.2404, -1.2572)$ | $(0.4807, 0)$ | $(-0.2404, 1.2572)$ | 0.60778 |

After 174 iterations $\|G\|_F \le 10^{-9}$. In every row the three weights and the three biases add up to 0. The fitted probabilities are $(0.853, 0.142, 0.006)$ at $x = -2$, $(0.247, 0.507, 0.247)$ at $x = 0$ and $(0.006, 0.142, 0.853)$ at $x = 2$. One linear score per class is enough to make the middle class the most likely in the middle, because the softmax compares the scores: $z_2 = 0.48$ is a constant, and it beats $z_1$ and $z_3$ only near $x = 0$. Without the penalty these data are separable, and the weights would grow without bound, as in logistic regression.

## Correctness

$J$ is convex and its gradient is $L$-Lipschitz. For such a function, a gradient step with $\eta = 1/L$ lowers $J$ by at least $\frac{1}{2L}\|G\|^2$. Since $J \ge 0$, the sum of $\|G\|^2$ over all steps is finite, so $\|G\|$ falls below each tol $> 0$, and line L5 returns. A point with $G = 0$ is a global minimizer of the convex $J$. If a minimizer exists, $J(W_t) - \min J \le L\|W_0 - W^\star\|^2/(2t)$ (Boyd and Vandenberghe, Section 9.3). If none exists (separable data with $\lambda = 0$), $\|G\|$ still tends to 0, but $\|W\|$ grows. The proof below gives the details.

## Complexity

On a [real RAM](/real-ram/), one iteration computes $nK$ scores with $d + 1$ terms each, $nK$ exponentials and the product $\tilde X^\top(P - Y)$, in $\Theta(nKd)$ time. With $t$ iterations the time is $O(tnKd)$. The extra memory is $\Theta(Kd)$ for $W$ and $G$, since $P$ can be computed one row at a time. For $\lambda > 0$ and all classes present, $J$ is strongly convex on the subspace where the columns of $W$ add up to zero, and $t$ grows like $\kappa\log(1/\text{tol})$, where $\kappa$ is the condition number of $J$ there. Newton's method needs a Hessian of size $K(d+1)$, with $O(nK^2d^2 + K^3d^3)$ time per step. This is why first-order and quasi-Newton methods are the usual choice.

## Properties

- **$K = 2$ is logistic regression.** With columns $\theta_1, \theta_2$, $P(y = 2 \mid x) = \sigma((\theta_2 - \theta_1)^\top\tilde x)$. With a penalty, $\theta_1 = -\theta_2$ at the optimum, so $v = \theta_2 - \theta_1$ minimizes the logistic loss with the penalty $\frac{\lambda}{4}\|v\|^2$ on its weights.
- **Linear decision boundaries.** Class $k$ beats class $j$ exactly when $(\theta_k - \theta_j)^\top\tilde x > 0$. So the regions of the classes are convex polyhedra.
- **Log-linear model.** $\log P(y = k \mid x) = z_k - \log\sum_j e^{z_j}$. The model is the maximum entropy distribution whose expected features match the data, which gives the name maximum entropy classifier.
- **Bias calibration.** With unpenalized biases, the bias rows of the gradient give $\sum_i P_{ik} = \sum_i Y_{ik}$ for each $k$ at the optimum: the predicted class counts equal the observed ones.
- **Existence.** As for logistic regression, without a penalty the estimate does not exist when the data are separable by the class regions. With $\lambda > 0$ and each class present, a minimizer exists, and it is unique on the subspace where the columns add up to zero.
- **A GLM.** The categorical distribution is an exponential family, and the softmax is the inverse of its canonical link, so softmax regression is a multivariate [GLM](/generalized-linear-model/).

## Variants and improvements

- **Newton and IRLS.** The Hessian is $\frac1n\sum_i(\operatorname{diag}(p_i) - p_ip_i^\top) \otimes \tilde x_i\tilde x_i^\top$. Newton converges in few steps for small $Kd$.
- **[L-BFGS](/limited-memory-bfgs/).** The usual solver in libraries for moderate sizes.
- **[Stochastic gradient descent](/stochastic-gradient-descent/).** One example or a minibatch per step. The softmax layer with cross-entropy is the output layer of most neural network classifiers, trained this way.
- **One-vs-rest logistic regression.** $K$ separate binary models. It is simpler to fit, but its scores are not probabilities that add up to one.
- **Sparse and structured penalties.** An L1 or group lasso penalty on the rows of $W$ selects features for all classes at once (glmnet's multinomial family).
- **Hierarchical and sampled softmax.** For very many classes, as in language models, approximations reduce the cost of the sum over $K$.

## When to use it

Use softmax regression for a classification problem with more than two exclusive classes when you want calibrated probabilities from a linear model. It is the standard multiclass baseline and the last layer of neural classifiers. If the classes are not exclusive (an example can have several labels), use $K$ separate logistic regressions instead. If the classes are ordered, an ordinal model uses that order and needs fewer parameters.

## Pitfalls

- **Overflow without the log-sum-exp trick.** Compute the softmax and the loss with the maximum subtracted, as in line L3.
- **Computing $\log P_{ik}$ as $\log$ of the softmax.** For a very unlikely class, $P_{ik}$ underflows to 0 and its log is $-\infty$. Use $\log P_{ik} = z_{ik} - \operatorname{logsumexp}(z_i)$.
- **Expecting unique weights without a penalty.** With $\lambda = 0$, the weights are defined only up to a common vector. Compare differences $\theta_k - \theta_j$, or fix a reference class.
- **A class that never occurs.** With unpenalized biases, the bias of a class with no examples tends to $-\infty$, and gradient descent never stops at a finite point.
- **Too large a step.** Steps larger than $2/L$ can make gradient descent diverge. The bound of line L1 is cheap and safe.

## Implementations

## History

The softmax form appears as Luce's choice axiom (1959) in mathematical psychology, and as the multinomial logit model of Cox (1966) and McFadden (1974) in statistics and econometrics. McFadden received the 2000 Nobel prize in economics in part for this work on discrete choice. Bridle (1990) named the function softmax for neural networks. It is the same as the Boltzmann distribution of statistical physics, with the scores as negative energies.

## References
