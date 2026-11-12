---
tag: 2F4BBA
kind: technique
slug: learning-rate-schedule
name: Learning rate schedule
aliases:
- cosine annealing
- learning rate decay
- step decay
- learning rate annealing
- one cycle learning rate policy
area: machine-learning/neural-network-training
level: intro
summary: A rule that sets the step size of each optimizer step during training, such as step decay, cosine annealing, linear warmup, one cycle or inverse square root.
prereqs: [stochastic-gradient-descent, gradient-descent]
see_also: [adamw, layer-wise-adaptive-rate-scaling, lamb, radam, gradient-accumulation, robbins-monro-algorithm, step-size-selection, hyperparameter-tuning]
sources:
  - url: https://arxiv.org/abs/1608.03983
    title: Ilya Loshchilov and Frank Hutter, SGDR, stochastic gradient descent with warm restarts, ICLR 2017
    locator: Section 3, the cosine annealing formula with the cycle length T_i, the first length T_0 and the factor T_mult
  - url: https://arxiv.org/abs/1706.02677
    title: Priya Goyal, Piotr Dollár, Ross Girshick, Pieter Noordhuis, Lukasz Wesolowski, Aapo Kyrola, Andrew Tulloch, Yangqing Jia and Kaiming He, Accurate, large minibatch SGD, training ImageNet in 1 hour, arXiv 2017
    locator: Section 2.1 (the linear scaling rule and its argument) and Section 2.2 (gradual warmup over 5 epochs)
  - url: https://arxiv.org/abs/1803.09820
    title: Leslie N. Smith, A disciplined approach to neural network hyper-parameters, part 1, learning rate, batch size, momentum, and weight decay, arXiv 2018
    locator: Section 4.1 (the 1cycle policy and the learning rate range test) and Section 4.3 (cyclical momentum)
  - url: https://arxiv.org/abs/1706.03762
    title: Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser and Illia Polosukhin, Attention is all you need, NeurIPS 2017
    locator: Section 5.3, Equation 3 (the inverse square root schedule with warmup_steps = 4000)
  - paper: doi:10.1109/CVPR.2016.90
    title: Kaiming He, Xiangyu Zhang, Shaoqing Ren and Jian Sun, Deep residual learning for image recognition, CVPR 2016
    locator: Section 4.2 (CIFAR-10 schedule, 0.1 divided by 10 at 32k and 48k iterations, stop at 64k)
  - paper: doi:10.1214/aoms/1177729586
    title: Herbert Robbins and Sutton Monro, A stochastic approximation method, Annals of Mathematical Statistics 22(3), 1951
    locator: the conditions on the step sizes a_n (sum of a_n infinite, sum of a_n squared finite)
  - book: isbn:9780262035613
    title: Ian Goodfellow, Yoshua Bengio and Aaron Courville, Deep Learning, MIT Press, 2016
    locator: Section 8.3.1 (the learning rate of SGD, the sufficient conditions on its decay, and linear decay to a fixed step)
---

A learning rate schedule is a rule that gives the step size $\eta_t$ of each optimizer step $t$ of a training run. The optimizer ([SGD](/stochastic-gradient-descent/), the [momentum method](/momentum-method/), [Adam](/adam/), [AdamW](/adamw/)) still chooses the direction of the step; the schedule only chooses its length. The common rules are step decay, exponential and polynomial decay, cosine annealing with or without restarts, a linear warmup in front of any of them, the one cycle policy, and the inverse square root rule of the transformer. For a stochastic gradient method a decreasing schedule is necessary to converge to a point, but the particular shapes used in deep learning are heuristics, chosen because they work well in practice.

## In plain words

Training takes many small steps downhill. A large step moves fast but jumps around near the bottom, because each step only sees a noisy estimate of the slope. A small step settles well but moves slowly. A schedule uses large steps early and small steps late.

Some schedules cut the step at fixed points, for example to one tenth after half of the training. Some shrink it smoothly, along half of a cosine wave. Many start with tiny steps for a short time and grow them, because the first steps of a fresh network are the least reliable. The schedule is a fixed recipe written before training starts. It does not look at the loss, so it costs nothing to run, but its numbers must be chosen for each task.

## When it applies

The setting is any training loop of a neural network (a multilayer perceptron, a convolutional network, a recurrent network or a transformer) that takes steps of the form

$$\theta_{t+1} = \theta_t - \eta_t\,u_t, \qquad t = 0, 1, \ldots, T-1,$$

where $u_t$ is the direction the optimizer computes from a minibatch gradient of the empirical risk $L(\theta)$, for example $u_t = \nabla L_{B_t}(\theta_t)$ for SGD or the normalized moment ratio of Adam. The schedule changes only the scalar $\eta_t$. Here $t$ counts optimizer steps, not epochs and not micro batches (see [gradient accumulation](/gradient-accumulation/)), and $T$ is the planned number of steps. Notation: $\theta$ the parameters, $L$ the mean loss, $\eta$ the learning rate, $T$ the number of steps, $W$ the number of warmup steps.

The theory that applies is stochastic approximation. For SGD with unbiased gradients of bounded variance, a constant $\eta$ does not converge to a minimizer: on a strongly convex smooth problem the iterates reach a region around the minimizer whose size grows with $\eta$, and then move about in it. Robbins and Monro (1951) gave the classical sufficient conditions on the steps,

$$\sum_{t} \eta_t = \infty, \qquad \sum_t \eta_t^2 < \infty,$$

for example $\eta_t = c/(t + 1)$; see the [Robbins-Monro algorithm](/robbins-monro-algorithm/). The first condition lets the iterates travel any distance, the second makes the injected noise summable. Deep networks are not convex, and the schedules below are not chosen to meet these conditions: they run for a fixed horizon $T$ and are tuned by experiment. No theorem says that one of them is best in general.

## The template

```pseudo id=main
TRAIN-WITH-SCHEDULE(θ, schedule, optimizer, T)
L1  for t ← 0 to T − 1 do
L2      B ← the next minibatch
L3      g ← ∇L_B(θ)                          ▷ backpropagation
L4      u ← optimizer.direction(g)           ▷ SGD, momentum, Adam, ...
L5      η ← schedule(t)                      ▷ the only line a schedule changes
L6      θ ← θ − η u
L7  return θ
```

The hole is the function `schedule(t)`. These are the standard choices, with $\eta_0$ or $\eta_{\max}$ the peak rate.

| schedule | $\eta_t$ | parameters |
|---|---|---|
| constant | $\eta_0$ | $\eta_0$ |
| step decay | $\eta_0\,\gamma^{\lfloor t/s \rfloor}$ | factor $\gamma < 1$, period $s$ |
| multi step | $\eta_0\,\gamma^{\lvert\{m \in M : m \le t\}\rvert}$ | milestones $M$ |
| exponential | $\eta_0\,\gamma^{t}$ | $\gamma$ close to 1 |
| polynomial | $\eta_{\text{end}} + (\eta_0 - \eta_{\text{end}})(1 - t/T)^p$ | power $p$ |
| cosine annealing | $\eta_{\min} + \tfrac12(\eta_{\max} - \eta_{\min})(1 + \cos(\pi t/T))$ | $\eta_{\min}$ |
| linear warmup | $\eta_{\text{start}} + (\eta_{\text{peak}} - \eta_{\text{start}})\,t/W$ for $t < W$ | $W$ |
| inverse square root | $d_{\text{model}}^{-1/2}\min(t^{-1/2},\ t\,W^{-3/2})$, $t \ge 1$ | $d_{\text{model}}$, $W$ |

- **Cosine annealing with warm restarts (SGDR).** Loshchilov and Hutter (2017) run the cosine over cycles. Inside cycle $i$, with $T_{\text{cur}}$ the steps since the last restart and $T_i$ the cycle length,
$$\eta_t = \eta_{\min} + \tfrac12(\eta_{\max} - \eta_{\min})\Bigl(1 + \cos\bigl(\pi\,T_{\text{cur}}/T_i\bigr)\Bigr), \qquad T_i = T_0\,T_{\text{mult}}^{\,i}.$$
At a restart, $T_{\text{cur}}$ returns to $0$ and the rate jumps back to $\eta_{\max}$. With one cycle of length $T$ this is plain cosine annealing.
- **Linear warmup and the linear scaling rule.** Goyal et al. (2017) train ResNet-50 with minibatches of up to 8192 images. Their rule: when the minibatch size is multiplied by $k$, multiply the learning rate by $k$. Their reason: $k$ SGD steps with rate $\eta$ on batches $B_1, \ldots, B_k$ of size $n$ give
$$\theta_{t+k} = \theta_t - \eta\,\frac1n\sum_{j<k}\sum_{x \in B_j}\nabla\ell(x, \theta_{t+j}),$$
while one step with rate $k\eta$ on their union, of size $kn$, gives $\theta_t - k\eta\,\frac{1}{kn}\sum_{j}\sum_{x}\nabla\ell(x, \theta_t)$. The two are equal when $\nabla\ell(x, \theta_{t+j}) = \nabla\ell(x, \theta_t)$ for $j < k$. That holds approximately when the weights change slowly, and fails most at the start of training, where they change fast. So they start at the small batch rate and raise it linearly to $k$ times that rate over the first 5 epochs.
- **Inverse square root.** Vaswani et al. (2017), Equation 3, train the transformer with Adam and $W = 4000$. The rate grows linearly for $W$ steps, reaches its peak $(d_{\text{model}}W)^{-1/2}$ at step $t = W$, and then falls as $t^{-1/2}$. The steps count from $1$; at $t = 0$ the formula divides by zero.
- **One cycle.** Smith (2018, Section 4.1) uses one cycle that is a little shorter than the run. In its first half the rate rises linearly from a low value to the peak, which he finds with a learning rate range test; in its second half it falls back linearly. For the remaining steps it falls to several orders of magnitude below the start. The momentum coefficient moves the opposite way, for example from 0.95 down to 0.85 and back (Section 4.3).

## Classic examples

**A table of five schedules.** Take $T = 100$ steps and peak $0.1$. The columns are: multi step with $\gamma = 0.1$ at milestones $50$ and $75$; exponential with $\gamma = 0.97$; cosine with $\eta_{\min} = 0$; $W = 10$ steps of linear warmup from $0$ and then cosine over the last $90$ steps; one cycle with a cycle of $90$ steps, a low value of $0.01$ and a final value of $10^{-5}$.

| $t$ | multi step | exponential | cosine | warmup and cosine | one cycle |
|---|---|---|---|---|---|
| 0 | 0.1 | 0.1 | 0.1 | 0 | 0.01 |
| 10 | 0.1 | 0.073742 | 0.097553 | 0.1 | 0.03 |
| 25 | 0.1 | 0.046697 | 0.085355 | 0.093301 | 0.06 |
| 50 | 0.01 | 0.021807 | 0.05 | 0.058682 | 0.09 |
| 75 | 0.001 | 0.010183 | 0.014645 | 0.017861 | 0.04 |
| 90 | 0.001 | 0.006448 | 0.002447 | 0.003015 | 0.01 |
| 99 | 0.001 | 0.004902 | 0.000025 | 0.00003 | 0.001009 |

The one cycle rate peaks at $0.1$ at step $45$, the middle of the cycle. The cosine is symmetric about the middle of the run: $\eta_t + \eta_{T-t} = \eta_{\max} + \eta_{\min}$ for each $t$, because $\cos(\pi - x) = -\cos x$. So the mean rate over a full cycle is $(\eta_{\max} + \eta_{\min})/2$, the same as a linear decay between the two ends; the cosine spends more steps near both ends and fewer in the middle.

**Restarts.** With $T_0 = 10$ and $T_{\text{mult}} = 2$, the cycles have lengths $10, 20, 40, 80, \ldots$, so the restarts are at steps $10, 30, 70, 150$. At step $29$, the last step of the second cycle, the rate is $0.000616$, and at step $30$ it is $0.1$ again.

**The transformer schedule.** For $d_{\text{model}} = 512$ and $W = 4000$:

| step | 1 | 1000 | 4000 | 16000 | 100000 |
|---|---|---|---|---|---|
| $\eta_t$ | $1.747 \times 10^{-7}$ | $1.747 \times 10^{-4}$ | $6.988 \times 10^{-4}$ | $3.494 \times 10^{-4}$ | $1.398 \times 10^{-4}$ |

The rate at step $1000$ is a quarter of the peak (linear part), and at step $16000$ it is half of the peak ($t^{-1/2}$ part).

**ResNet on CIFAR-10.** He et al. (2016, Section 4.2) start at $0.1$, divide by $10$ at $32$k and $48$k iterations, and stop at $64$k. This multi step schedule was the standard for convolutional networks before cosine annealing became common.

**Large batches.** With the linear scaling rule and the reference $0.1$ for a batch of $256$, a batch of $8192$ gets $0.1 \times 8192/256 = 3.2$, reached after 5 epochs of warmup.

**A one dimensional check.** On $f(w) = w^2/2$ with gradient $w$, gradient descent gives $w_{t+1} = (1 - \eta_t)w_t$, so $w_T = w_0\prod_{t<T}(1 - \eta_t)$. With step decay $\eta_t = \frac12 \cdot (\frac12)^{\lfloor t/2 \rfloor}$ and $w_0 = 1$, the iterates are $1, \frac12, \frac14, \frac{3}{16}, \frac{9}{64}$: each cut of the rate slows the progress, which on a noisy problem buys a smaller final noise.

## Variations

- **Schedules on the loss.** Reduce on plateau multiplies the rate by a factor when the validation loss has not improved for a number of epochs. It is not a function of $t$ alone, so the run is harder to reproduce. [Early stopping](/early-stopping/) uses the same signal to end the run.
- **Schedules for other hyperparameters.** The one cycle policy also schedules the momentum. [AdamW](/adamw/) multiplies its weight decay by the same schedule multiplier as the step. [LARS](/layer-wise-adaptive-rate-scaling/) uses polynomial decay with power 2, and [LAMB](/lamb/) uses linear decay with warmup.
- **Warmup as a variance fix.** For Adam, part of the benefit of warmup comes from the high variance of the second moment estimate in the first steps; [RAdam](/radam/) replaces the warmup by an explicit correction.
- **Per layer rates.** [LARS](/layer-wise-adaptive-rate-scaling/) and [LAMB](/lamb/) multiply the global schedule by a ratio computed for each layer at each step.
- **Classical decreasing rules.** $\eta_t = c/(t + t_0)$ meets the Robbins-Monro conditions, and $\eta_t = c/\sqrt{t + 1}$ is the usual choice in the analysis of SGD on convex Lipschitz problems; see [stochastic gradient descent](/stochastic-gradient-descent/).

## Pitfalls

- **Steps or epochs.** A schedule written per epoch and called per step (or the reverse) runs a very different curve. Count the optimizer steps, not the micro batches of gradient accumulation.
- **Off by one at the ends.** Is the first step $t = 0$ or $t = 1$? The inverse square root rule divides by zero at $0$, and a warmup that starts at exactly $0$ wastes its first step.
- **The horizon is a parameter.** Cosine and polynomial schedules reach their end value at $T$. If the run is extended, the rate stays at the end value or, with some code, rises again; resume a run from a checkpoint with the same $T$ and the same step counter.
- **Changing the batch size without the rate.** Under the linear scaling rule the peak rate depends on the batch size, and the rule breaks down for very large batches, where per layer methods such as LARS and LAMB are used.
- **Warmup is not optional for some setups.** Transformers trained with Adam and large peak rates often diverge in the first steps without warmup; this is an observation from practice, not a theorem.
- **Comparing schedules at one horizon.** A schedule that wins for $T$ steps can lose for $2T$ steps; compare at the length you will use.

## Exercises

1. Show that the multi step schedule with $\gamma = 0.1$ at milestones $50$ and $75$ and the cosine schedule with $\eta_{\min} = 0$ over $T = 100$ steps have sums $\sum_{t<100}\eta_t$ of $5.275$ and $5.05$.
2. Prove that the linear warmup from $\eta_0$ to $k\eta_0$ over $W$ steps has mean rate $\frac{(k+1)\eta_0}{2}$ up to a term of order $\eta_0 k/W$.
3. For the inverse square root rule, show that $\eta_t$ is largest at $t = W$, and find $t$ with $\eta_t = \eta_W/10$.
4. With $T_0 = 10$ and $T_{\text{mult}} = 2$, find the cycle and the position in the cycle of step $1000$.
5. On $f(w) = w^2/2$, show that a constant rate $\eta \in (0, 2)$ converges and $\eta > 2$ diverges, and relate this to the largest safe peak of a schedule.

## References
