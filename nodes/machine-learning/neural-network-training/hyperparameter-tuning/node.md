---
tag: 47B9Z8
kind: problem
slug: hyperparameter-tuning
name: Hyperparameter tuning
aliases:
- hyperparameter optimization
- HPO
- hyperparameter search
area: machine-learning/neural-network-training
level: intro
summary: "Choose the settings fixed before training, such as the learning rate, to minimize validation loss. An expensive noisy black box; solved by grid, random search, successive halving, Hyperband."
prereqs: [cross-validation, black-box-optimization]
see_also: [gaussian-process, multi-armed-bandit, neural-architecture-search, early-stopping, derivative-free-optimization, evolutionary-computation, learning-rate-schedule, overfitting]
sources:
  - url: https://jmlr.org/papers/v13/bergstra12a.html
    title: James Bergstra and Yoshua Bengio, Random search for hyper-parameter optimization, Journal of Machine Learning Research 13, 2012
    locator: pp. 281 to 305 (low effective dimensionality, and random search against grid search)
  - url: https://jmlr.org/papers/v18/16-558.html
    title: Lisha Li, Kevin Jamieson, Giulia DeSalvo, Afshin Rostamizadeh and Ameet Talwalkar, Hyperband, a novel bandit-based approach to hyperparameter optimization, Journal of Machine Learning Research 18(185), 2018
    locator: Algorithm 1 (Hyperband), Table 1 (the brackets for R = 81 and eta = 3), and the theoretical analysis of Section 5
  - url: https://proceedings.mlr.press/v51/jamieson16.html
    title: Kevin Jamieson and Ameet Talwalkar, Non-stochastic best arm identification and hyperparameter optimization, AISTATS 2016, PMLR 51
    locator: pp. 240 to 248 (successive halving for hyperparameter optimization as non-stochastic best arm identification)
  - url: https://proceedings.mlr.press/v28/karnin13.html
    title: Zohar Karnin, Tomer Koren and Oren Somekh, Almost optimal exploration in multi-armed bandits, ICML 2013, PMLR 28(3)
    locator: pp. 1238 to 1246 (sequential halving for best arm identification with a fixed budget)
  - url: https://arxiv.org/abs/1206.2944
    title: Jasper Snoek, Hugo Larochelle and Ryan P. Adams, Practical Bayesian optimization of machine learning algorithms, NIPS 2012
    locator: Gaussian process surrogates and expected improvement for tuning learning algorithms
  - url: https://arxiv.org/abs/1807.01774
    title: Stefan Falkner, Aaron Klein and Frank Hutter, BOHB, robust and efficient hyperparameter optimization at scale, ICML 2018
    locator: Hyperband brackets with configurations proposed by a model instead of at random
  - url: https://arxiv.org/abs/1711.09846
    title: Max Jaderberg, Valentin Dalibard, Simon Osindero and others, Population based training of neural networks, 2017
    locator: the exploit and explore steps that copy weights and perturb hyperparameters during training
  - paper: doi:10.1007/978-3-030-05318-5_1
    title: Matthias Feurer and Frank Hutter, Hyperparameter optimization, in Automated Machine Learning, Springer, 2019
    locator: Chapter 1 (the problem statement, black-box and multi-fidelity methods)
---

Hyperparameter tuning chooses the settings of a learning algorithm that are fixed before training, such as the learning rate, the weight decay, the batch size or the number of layers, so that the trained model has the lowest loss on validation data. Each evaluation of a setting is a full training run, so the objective is an expensive, noisy black box with no gradient. Grid search and random search treat it as plain [black-box optimization](/black-box-optimization/); successive halving and Hyperband save time by stopping bad settings early, after a small budget. Random search is a strong baseline because the loss usually depends strongly on only a few of the hyperparameters (Bergstra and Bengio 2012).

## In plain words

Before you train a network, you must pick numbers such as how big each training step is and how strongly to keep the weights small. Training does not choose them for you. You try some choices, train with each, and keep the one that scores best on data held back from training. The trouble is that each try is a full training run, which can take hours. Trying every combination on a grid wastes most tries. Picking choices at random is often better. Even better, start many tries, stop the poor ones early, and give their time to the good ones.

## Definition

**Input.** A learning algorithm $\mathcal{A}$, training data $D_{\text{train}}$, validation data $D_{\text{val}}$ (or a [cross-validation](/cross-validation/) scheme), and a configuration space $\Lambda = \Lambda_1 \times \cdots \times \Lambda_d$. Each $\Lambda_j$ is an interval of reals (often on a log scale, such as a learning rate in $[10^{-5}, 1]$), a set of integers, or a finite set of categories. Some hyperparameters are *conditional*: they exist only for some values of others, such as the momentum of an optimizer that is only one of the choices.

**Objective.** The validation loss

$$f(\lambda) = \mathcal{L}\big(\mathcal{A}_\lambda(D_{\text{train}}),\ D_{\text{val}}\big), \qquad \lambda \in \Lambda,$$

where $\mathcal{A}_\lambda(D_{\text{train}})$ is the model trained with configuration $\lambda$. The problem is to find $\lambda^\star \in \arg\min_{\lambda \in \Lambda} f(\lambda)$, or a $\lambda$ with $f(\lambda)$ close to the minimum, within a total compute budget.

**Access model.** $f$ is a black box: one query trains a model, it costs the same as training, the answer is noisy (random initialization, data order), and there is in general no gradient with respect to $\lambda$. In the *multi-fidelity* model, one can also query $f(\lambda, r)$ with a smaller *resource* $r \le R$, such as fewer epochs or a subset of the data, at a cost proportional to $r$, with $f(\lambda, R) = f(\lambda)$.

**Output.** A configuration $\hat\lambda$, usually retrained on all the training data. Its validation loss $f(\hat\lambda)$ is optimistically biased, because $\hat\lambda$ was chosen to minimize it; a separate test set or nested cross-validation estimates the true performance.

## Variants

- **Single-fidelity black box.** Only full training runs are possible.
- **Multi-fidelity.** Cheap, partial runs give noisy early estimates. Successive halving and Hyperband use this.
- **Sequential or parallel.** With many workers, asynchronous methods avoid waiting for the slowest run.
- **Multi-objective.** Trade validation loss against model size, latency or energy.
- **Gradient-based tuning.** For continuous hyperparameters of a differentiable training procedure, the hypergradient $\partial f / \partial \lambda$ can be computed by differentiating through training, or by implicit differentiation at the trained optimum.
- **Neural architecture search.** The configuration space is a space of network architectures; see [neural architecture search](/neural-architecture-search/).
- **Combined algorithm selection and tuning.** The first, categorical hyperparameter is the choice of algorithm, and the rest are conditional on it.

## Examples

**Grid against random search.** Let $f(\text{lr}, \text{wd}) = (\text{lr} - 0.37)^2 + 0.001\, \text{wd}$ on $[0, 1]^2$, so only the learning rate matters much. A $3 \times 3$ grid on $\{0.1, 0.5, 0.9\}^2$ uses 9 runs but tries only 3 learning rates, and its best is $\text{lr} = 0.5$. Nine random points try 9 different learning rates. This is the argument of Bergstra and Bengio (2012): with low *effective dimensionality*, a grid wastes runs on repeated values of the important coordinate.

**How many random tries.** If the configurations with a loss in the best 5 percent of the space have probability $q = 0.05$ under the sampling distribution, then $T$ independent random tries hit that region with probability $1 - (1 - q)^T$. For $T = 60$ this is $1 - 0.95^{60} \approx 0.954$, whatever the number of hyperparameters. The guarantee is about the quantile, not about the distance to the optimum: if the top 5 percent is still poor, so is the result.

**The Hyperband schedule for $R = 81$, $\eta = 3$.** Here $s_{\max} = \lfloor \log_3 81 \rfloor = 4$ and $B = (s_{\max} + 1) R = 405$. Bracket $s$ starts $n = \lceil \tfrac{B}{R} \tfrac{\eta^s}{s + 1} \rceil$ configurations with resource $r = R \eta^{-s}$ each, and round $i$ runs $n_i = \lfloor n \eta^{-i} \rfloor$ configurations with $r_i = r \eta^i$:

| round $i$ | $s = 4$: $n_i$, $r_i$ | $s = 3$ | $s = 2$ | $s = 1$ | $s = 0$ |
|---|---|---|---|---|---|
| 0 | 81, 1 | 34, 3 | 15, 9 | 8, 27 | 5, 81 |
| 1 | 27, 3 | 11, 9 | 5, 27 | 2, 81 | |
| 2 | 9, 9 | 3, 27 | 1, 81 | | |
| 3 | 3, 27 | 1, 81 | | | |
| 4 | 1, 81 | | | | |
| budget $\sum_i n_i r_i$ | 405 | 363 | 351 | 378 | 405 |

The five brackets use $1902$ units of resource, at most $B = 405$ each, which is the cost of about 23.5 full runs. Bracket $s = 4$ is the most aggressive: it looks at 81 configurations after one unit each. Bracket $s = 0$ is random search with 5 full runs. Hyperband runs all of them because it does not know in advance whether early losses predict final losses.

## Known algorithms

- **Manual search.** An expert changes one or two settings at a time, guided by learning curves. Still common, hard to reproduce.
- **Grid search.** Try every point of $\Lambda_1' \times \cdots \times \Lambda_d'$ for finite subsets $\Lambda_j'$ with $k$ values each: $k^d$ runs. Simple and parallel, but exponential in $d$, and only $k$ values per coordinate.
- **Random search.** Draw $T$ configurations independently from a distribution on $\Lambda$, such as log-uniform for scale parameters. Parallel, anytime, and robust to unimportant coordinates. Quasi-random sequences (Sobol, Latin hypercube) spread the points more evenly.
- **Bayesian optimization.** Fit a surrogate model of $f$, such as a [Gaussian process](/gaussian-process/) or a tree-based model, to the runs so far, and choose the next configuration by an acquisition function, such as expected improvement, that balances exploration and exploitation (Snoek, Larochelle and Adams 2012). It needs fewer runs than random search when runs are few and the space is small and continuous; it is sequential by nature.
- **Successive halving.** Start $n$ configurations with a small resource $r$, keep the best $1/\eta$ of them, multiply the resource by $\eta$, and repeat until one remains or the resource reaches $R$ (Karnin, Koren and Somekh 2013; Jamieson and Talwalkar 2016). The total cost per round is about $n r$, so a bracket costs about $n r \log_\eta n$.
- **Hyperband.** Successive halving needs a choice of $n$ for a given budget: many configurations with little resource each, or few with much. Hyperband runs successive halving for every trade-off $s = s_{\max}, \ldots, 0$ as in the table above (Li et al. 2018).
- **Hybrids and variants.** BOHB samples the configurations of the Hyperband brackets from a model (Falkner, Klein and Hutter 2018). ASHA is an asynchronous successive halving for many workers. Learning curve extrapolation stops runs whose predicted final loss is poor.
- **Evolutionary and population methods.** [Evolutionary computation](/evolutionary-computation/) and CMA-ES evolve populations of configurations. Population based training trains a population in parallel and, at intervals, copies the weights of good members into poor ones and perturbs their hyperparameters, so the hyperparameters form a schedule (Jaderberg et al. 2017).

## Bounds

- **Black box lower bounds.** With no assumption on $f$, no method can do better than enumerating $\Lambda$. For an $L$-Lipschitz $f$ on $[0, 1]^d$, finding an $\epsilon$-optimal point needs about $(L / \epsilon)^d$ evaluations in the worst case. So any useful guarantee needs structure such as low effective dimension or smoothness.
- **Random search.** $T \ge \log \delta / \log(1 - q)$ tries reach the top $q$ quantile with probability at least $1 - \delta$; $T = 60$ suffices for $q = \delta = 0.05$. The bound does not depend on $d$.
- **Grid search.** A grid with $T$ points has only $T^{1/d}$ values per coordinate. If $f$ depends only on one coordinate, the grid acts like $T^{1/d}$ tries and random search like $T$ tries.
- **Successive halving.** In the stochastic bandit model, sequential halving identifies the best of $n$ arms with a budget that is optimal up to logarithmic factors (Karnin, Koren and Somekh 2013). In the non-stochastic model, where each configuration's loss converges to a limit as $r$ grows at an unknown rate, it returns the best configuration once the budget is large enough relative to how fast the losses separate (Jamieson and Talwalkar 2016).
- **Hyperband.** Each bracket uses at most about $B = (s_{\max} + 1) R$ resource, so the total is about $(s_{\max} + 1)^2 R$. Li et al. (2018) show that, under their assumptions on the convergence of the losses, Hyperband needs at most a logarithmic factor more budget than the best single bracket chosen in hindsight.

## Reductions

- **To black-box optimization.** Single-fidelity tuning is [black-box](/black-box-optimization/) and [derivative-free optimization](/derivative-free-optimization/) of a noisy, expensive function. Any such method applies.
- **To best arm identification.** With a finite set of sampled configurations, multi-fidelity tuning is a [multi-armed bandit](/multi-armed-bandit/) problem: each configuration is an arm, and pulling it trains it further. The losses are not independent draws but converge along a learning curve, which is why Jamieson and Talwalkar use a non-stochastic model.
- **From model selection.** Choosing among a few fixed models by [cross-validation](/cross-validation/) is the special case with a finite $\Lambda$ and full runs.
- **Early stopping as tuning.** The number of training steps is a hyperparameter, and [early stopping](/early-stopping/) chooses it with the validation loss during one run.

## Applications

- Tuning the learning rate, its [schedule](/learning-rate-schedule/), the [weight decay](/weight-decay/), the batch size and the [dropout](/dropout/) rate of deep networks; the learning rate usually matters most.
- Choosing the regularization constant and kernel width of support vector machines and kernel methods, and the depth and learning rate of gradient boosted trees.
- AutoML systems that choose the algorithm, the preprocessing and the hyperparameters together.
- Tuning reinforcement learning agents, where single runs are very noisy and population based training is common.
- A tuned baseline is needed for any fair comparison of methods: a new method compared with an untuned baseline shows the effect of tuning, not of the method, and the validation data used for tuning must not be reused for the final evaluation, or the reported result shows [overfitting](/overfitting/) to the validation set.

## References
