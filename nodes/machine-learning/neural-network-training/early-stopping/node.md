---
tag: 56QAAE
kind: technique
slug: early-stopping
name: Early stopping
area: machine-learning/neural-network-training
level: intro
summary: "Stop training when the error on held-out data stops improving, and keep the best parameters seen. For gradient descent on least squares it acts like ridge regression."
prereqs: [gradient-descent, overfitting, ridge-regression]
see_also: [regularization, cross-validation, weight-decay, generalization-error, double-descent, hyperparameter-tuning, tikhonov-regularization, learning-rate-schedule]
sources:
  - book: isbn:9780262035613
    title: Ian Goodfellow, Yoshua Bengio and Aaron Courville, Deep Learning, MIT Press, 2016
    locator: Section 7.8 (Algorithm 7.1, early stopping with patience; Algorithms 7.2 and 7.3, using the validation data after stopping; early stopping as L2 regularization on a quadratic)
  - paper: doi:10.1007/3-540-49430-8_3
    title: Lutz Prechelt, Early stopping, but when?, in Neural Networks, Tricks of the Trade, LNCS 1524, Springer, 1998, pages 55 to 69
    locator: the stopping criteria GL (generalization loss), PQ (progress quotient) and UP (successive increases), and their comparison
  - paper: doi:10.1007/s00365-006-0663-2
    title: Yuan Yao, Lorenzo Rosasco and Andrea Caponnetto, On early stopping in gradient descent learning, Constructive Approximation 26(2), 289 to 315, 2007
    locator: gradient descent iterates as a spectral filter, the number of steps as the regularization parameter
---

Early stopping is a [regularization](/regularization/) method for models trained by an iterative method: a part of the data is held out as a validation set, the validation error is measured every few steps, and training stops when it has not improved for a while. The result is the parameters with the lowest validation error seen, not the last ones. The number of steps then plays the role of a regularization parameter, chosen on the fly with one training run. For [gradient descent](/gradient-descent/) on a least squares loss started at zero, this is more than an analogy: after $t$ steps with step size $\eta$ the iterate is a spectral filter of the data. When $\eta s_i \le 1$ for every eigenvalue $s_i$ of the data covariance, it is within a factor of two of [ridge regression](/ridge-regression/) with $\lambda = 1/(\eta t)$ on every eigendirection (Claim 3 below). Yao, Rosasco and Caponnetto (2007) use the same filter view to prove rates for early stopping.

## In plain words

When a model trains, its error on the training data keeps going down. Its error on new data goes down at first, as the model learns the real pattern, and then often goes up again, as the model starts to learn the noise of the training data. Early stopping keeps some data aside, checks the error on it from time to time, and remembers the best model so far. When the error on the kept data has not improved for a set number of checks, training stops and the best model is used. The model has had less time to grow large weights, so stopping early limits the model in a way like a cost on large weights.

## When it applies

- **Problem.** [Overfitting](/overfitting/) of a model trained by many small steps, such as a neural network trained with [stochastic gradient descent](/stochastic-gradient-descent/), boosting, or gradient descent on least squares.
- **Part of the training loop.** The outer loop: when to stop and which parameters to return.
- **Needs.** A validation set drawn from the same distribution as the test data, and a training curve with a minimum, which is common but not certain (see [double descent](/double-descent/)).
- **Cost model.** One evaluation on the validation set every $k$ steps, and one stored copy of the parameters.

## The template

Notation: STEP does one update of the parameters $\theta$, VAL($\theta$) is the error on the validation set, $k$ is the number of steps between checks, and $P$ is the patience.

```pseudo id=template
EARLY-STOPPING(θ, k, P, T_max)
L1  best ← VAL(θ); θ* ← θ; t* ← 0; bad ← 0; t ← 0
L2  while t < T_max and bad < P:
L3      do k times: θ ← STEP(θ); t ← t + 1
L4      v ← VAL(θ)
L5      if v < best: best ← v; θ* ← copy of θ; t* ← t; bad ← 0
L6      else: bad ← bad + 1
L7  return θ*, t*
```

This is Algorithm 7.1 of Goodfellow, Bengio and Courville.

**Cost.** The run does at most $t^* + kP$ steps of training, where $t^*$ is the step of the best check, and $\lceil t/k \rceil$ evaluations. The memory is one extra copy of $\theta$.

**Claim 1.** EARLY-STOPPING returns the parameters with the lowest validation error among all checks it made, and it stops at the $P$-th check in a row with no improvement, or at $T_{\max}$.

*Proof.* Lines L5 and L6 keep the invariant that $\theta^*$ is a copy of the parameters at the best check so far and that bad counts the checks since then. The loop ends when bad reaches $P$ or $t$ reaches $T_{\max}$. $\blacksquare$

The patience trades training time against the risk of stopping in a small bump of a noisy validation curve. Prechelt (1998) compares other rules. His generalization loss is $GL(t) = 100\,(E_{\mathrm{va}}(t)/E_{\mathrm{opt}}(t) - 1)$, where $E_{\mathrm{opt}}(t)$ is the lowest validation error up to step $t$, and the rule $GL_\alpha$ stops at the first $t$ with $GL(t) > \alpha$. The rule $UP_s$ stops after the validation error has gone up at the end of $s$ strips of training in a row, and $PQ_\alpha$ divides $GL$ by a measure of how much the training error still falls. In his experiments, rules that stop later gave small gains in generalization on average for much more training time.

### Early stopping as a spectral filter

Let the training loss be $f(w) = \frac12 w^\top \Sigma w - c^\top w$ with $\Sigma = X^\top X/n$ and $c = X^\top y/n$; this is half the mean squared error of a [least squares problem](/least-squares-problem/), up to a constant. Write $\Sigma = \sum_i s_i q_i q_i^\top$ with eigenvalues $s_i \ge 0$ and orthonormal eigenvectors $q_i$.

**Claim 2.** Gradient descent $w_{t+1} = w_t - \eta(\Sigma w_t - c)$ with $w_0 = 0$ gives

$$w_t = \eta \sum_{j=0}^{t-1} (I - \eta\Sigma)^j c = \sum_i g_t(s_i)\, (q_i^\top c)\, q_i, \qquad g_t(s) = \frac{1 - (1 - \eta s)^t}{s},$$

with $g_t(0) = \eta t$. Ridge regression, the minimizer of $f + \frac{\lambda}{2}\|w\|^2$, is the same sum with the filter $r_\lambda(s) = 1/(s + \lambda)$.

*Proof.* The update is $w_{t+1} = (I - \eta\Sigma) w_t + \eta c$, and induction from $w_0 = 0$ gives the first sum. On the eigenvector $q_i$, $I - \eta\Sigma$ acts as $1 - \eta s_i$, and the geometric sum $\eta\sum_{j<t}(1 - \eta s_i)^j$ is $g_t(s_i)$. For ridge regression, $(\Sigma + \lambda I) w = c$ gives $1/(s_i + \lambda)$ on $q_i$. $\blacksquare$

As $t \to \infty$, with $0 < \eta s_i < 2$, $g_t(s_i) \to 1/s_i$, the filter of the least squares solution. A small $t$ keeps the components with large $s_i$, which are learned in a few steps, and leaves out those with small $s_i$, which are the most sensitive to noise. Ridge regression does the same with a smooth cut at $s \approx \lambda$.

**Claim 3.** If $0 \le \eta s \le 1$ and $\lambda = 1/(\eta t)$, then $r_\lambda(s) \le g_t(s) \le 2\, r_\lambda(s)$.

*Proof.* Multiply by $s$ and set $x = \eta s \in [0, 1]$. Then $s\, r_\lambda(s) = t x/(1 + t x)$ and $s\, g_t(s) = 1 - (1 - x)^t$. For the lower bound, $(1 - x)^t \le e^{-tx} \le 1/(1 + tx)$, since $e^{u} \ge 1 + u$. For the upper bound, Bernoulli's inequality $(1 - x)^t \ge 1 - tx$ gives $1 - (1 - x)^t \le \min(1, tx)$, and $\min(1, tx) \le 2tx/(1 + tx)$, by checking the cases $tx \le 1$ and $tx \ge 1$. At $s = 0$ both sides are equal to $\eta t$ and $1/\lambda = \eta t$. $\blacksquare$

So $t$ steps of gradient descent shrink each component as ridge regression with $\lambda = 1/(\eta t)$ does, up to a factor of two: more steps mean less regularization. Yao, Rosasco and Caponnetto (2007) use this filter view to prove rates of convergence for early stopping in reproducing kernel Hilbert spaces, with the number of steps as the regularization parameter.

## Classic examples

**A noisy regression with almost as many features as examples.** Draw 30 training rows and 200 validation rows with 25 Gaussian features each, the target $\sum_j x_j/j$ plus Gaussian noise of standard deviation 1 (`random.Random(0)`). Full-batch gradient descent on the training mean squared error, step size 0.01 from $w = 0$, gives:

| step | training error | validation error |
|---|---|---|
| 0 | 2.159 | 2.256 |
| 20 | 0.860 | 1.891 |
| 63 | 0.447 | 1.791 |
| 100 | 0.358 | 1.812 |
| 1000 | 0.251 | 1.998 |
| at convergence (least squares) | 0.250 | 2.062 |

With patience 20 and a check at every step, early stopping stops at step 83 and returns the parameters of step 63. Ridge regression with $\lambda = 1/(\eta t) \approx 0.79$, the value from Claim 3 for $t = 63$ and the loss scaled as in Claim 2 (so $\eta = 0.02$), has validation error 1.767; the best $\lambda$ on a coarse grid gives 1.741.

**Neural networks.** The usual way to train a deep network is to check the validation loss once per epoch, keep the best checkpoint, and stop after a patience of some epochs.

## Variations

- **Retraining on all data** (Goodfellow et al., Algorithm 7.2). After early stopping finds $t^*$, train again on the training and validation data together for $t^*$ steps, or for the same number of passes over the data.
- **Continuing from the stopped model** (Algorithm 7.3). Keep training on all data until the loss on the validation set falls below the training loss at the stop.
- **Stopping on a different metric.** Stop on accuracy, AUC or another target metric instead of the loss, since the two can reach their best at different times.
- **Early stopping in boosting.** The number of rounds of a boosting method is chosen in the same way.

## Pitfalls

- **The validation error is now biased.** The stopping step is chosen to make the validation error small, so that error is optimistic. Report the error on a separate test set, or use nested [cross-validation](/cross-validation/).
- **Returning the last parameters.** The run ends $kP$ steps after the best check. The parameters at the end are worse on the validation set, so the best ones must be stored.
- **Noise in the validation curve.** With a small validation set, or a check after each mini-batch, the curve is noisy, and a small patience stops too early. Smooth the curve, check less often, or use a larger patience.
- **A schedule that ends late.** With a [learning rate schedule](/learning-rate-schedule/) that decays the step size, the validation error can fall again after a plateau, so a stop during the plateau loses that gain.
- **Claim 3 needs the conditions.** The factor-two link with ridge regression is for gradient descent from zero on a quadratic loss with $\eta s \le 1$. For a neural network the effect of early stopping is not an exact penalty.

## Exercises

1. Show that the iterate $w_t$ of Claim 2 lies in the space spanned by $c, \Sigma c, \dots, \Sigma^{t-1} c$, and give a $2 \times 2$ example where $w_2$ does not minimize $f$ over that space.
2. For $\Sigma = \begin{pmatrix} 5 & 3 \\ 3 & 5 \end{pmatrix}$, $c = (7, 1)$ and $\eta = 1/10$, compute $w_1$, $w_2$ and $w_3$ by the update and by the filter formula.
3. Show that $\|w_t\|$ is non-decreasing in $t$ in the setting of Claim 2 when $0 < \eta s_i \le 1$ for all $i$, and conclude that early stopping limits the norm of the parameters.
4. Prove the inequality $\min(1, u) \le 2u/(1 + u)$ for $u \ge 0$, and find where it is tight.
5. Show that the rule $GL_\alpha$ never stops while the validation error is at a new minimum, and give a validation curve on which $UP_2$ stops earlier than $GL_5$.

## References
