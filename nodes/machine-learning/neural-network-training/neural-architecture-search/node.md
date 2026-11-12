---
tag: Z1X9SG
kind: problem
slug: neural-architecture-search
name: Neural architecture search
aliases:
- NAS
- automated architecture design
area: machine-learning/neural-network-training
level: research
summary: "Search a space of network architectures for one with the best validation performance. Methods differ in search space, search strategy (RL, evolution, DARTS) and performance estimation."
prereqs: [hyperparameter-tuning, backpropagation, stochastic-gradient-descent]
see_also: [reinforce, evolutionary-computation, black-box-optimization, knowledge-distillation, neural-network-pruning, gradient-descent, genetic-algorithm, multi-armed-bandit]
sources:
  - url: https://arxiv.org/abs/1611.01578
    title: Barret Zoph and Quoc V. Le, Neural architecture search with reinforcement learning, ICLR 2017
    locator: Section 3 (a recurrent controller that emits architectures as token sequences, trained with REINFORCE on the validation accuracy)
  - url: https://arxiv.org/abs/1806.09055
    title: Hanxiao Liu, Karen Simonyan and Yiming Yang, DARTS, differentiable architecture search, ICLR 2019
    locator: Section 2 (the cell search space, the softmax relaxation of the choice of operation, the bilevel problem and its first and second order approximations, and the discretization)
  - url: https://arxiv.org/abs/1902.07638
    title: Liam Li and Ameet Talwalkar, Random search and reproducibility for neural architecture search, UAI 2019, PMLR 115
    locator: random search with early stopping and with weight sharing as baselines that match weight-sharing methods on standard benchmarks
  - url: https://jmlr.org/papers/v20/18-598.html
    title: Thomas Elsken, Jan Hendrik Metzen and Frank Hutter, Neural architecture search, a survey, Journal of Machine Learning Research 20(55), 2019
    locator: the three dimensions of search space, search strategy and performance estimation strategy
  - url: https://arxiv.org/abs/1802.01548
    title: Esteban Real, Alok Aggarwal, Yanping Huang and Quoc V. Le, Regularized evolution for image classifier architecture search, AAAI 2019
    locator: aging evolution, tournament selection that removes the oldest member
  - url: https://arxiv.org/abs/1802.03268
    title: Hieu Pham, Melody Y. Guan, Barret Zoph, Quoc V. Le and Jeff Dean, Efficient neural architecture search via parameter sharing, ICML 2018
    locator: weight sharing among all architectures as subgraphs of one large graph
  - url: https://arxiv.org/abs/1909.09656
    title: Arber Zela, Thomas Elsken, Tonmoy Saikia, Yassine Marrakchi, Thomas Brox and Frank Hutter, Understanding and robustifying differentiable architecture search, ICLR 2020
    locator: the failure of DARTS toward cells full of skip connections, and its link with the curvature of the validation loss in the architecture weights
  - url: https://arxiv.org/abs/1902.09635
    title: Chris Ying, Aaron Klein, Esteban Real, Eric Christiansen, Kevin Murphy and Frank Hutter, NAS-Bench-101, towards reproducible neural architecture search, ICML 2019
    locator: a tabular benchmark of trained and evaluated cell architectures
---

Neural architecture search (NAS) is the problem of choosing the structure of a neural network, such as its layers, their operations and their connections, to maximize validation accuracy, often under a limit on size or latency. It is [hyperparameter tuning](/hyperparameter-tuning/) with a large, structured, discrete space, where each evaluation is a full training run. Elsken, Metzen and Hutter (2019) describe each method by its *search space*, its *search strategy* and its *performance estimation strategy*. Strategies include reinforcement learning (Zoph and Le 2017), evolution (Real et al. 2019) and the gradient-based relaxation DARTS (Liu, Simonyan and Yang 2019); random search is a strong baseline (Li and Talwalkar 2019).

## In plain words

Designing a network means many choices: how many layers, what each layer does, and which layers feed which. Neural architecture search lets a program make these choices. It needs three things. A menu of what is allowed, which is the search space. A way to pick the next design to try, which is the search strategy. A way to judge a design without spending days training it, which is the performance estimate. Early methods trained thousands of designs and used huge amounts of compute. Later methods share training between designs and are much cheaper, but their judgments are less reliable. Simple random picking, done carefully, often does about as well.

## Definition

**Input.** A search space $\mathcal{A}$ of architectures, training data, validation data, and a training procedure that, for each $a \in \mathcal{A}$, produces weights $w^\star(a) = \arg\min_w \mathcal{L}_{\text{train}}(w, a)$ (in practice, the result of a fixed training run). Optionally a cost function $c(a)$, such as the parameter count, the number of operations or the latency on a device, and a limit $C$.

**Objective.**

$$\min_{a \in \mathcal{A}} \ \mathcal{L}_{\text{val}}\big(w^\star(a), a\big) \quad \text{subject to} \quad c(a) \le C.$$

This is a bilevel problem: the inner problem trains the weights, the outer problem chooses the architecture.

**Search spaces.**

- *Chain or macro spaces.* A sequence of layers, each with a type (convolution, pooling), a width, a kernel size and optional skip connections to earlier layers. Zoph and Le encode an architecture as a sequence of such tokens.
- *Cell spaces.* Search a small directed acyclic graph, the *cell*, and stack copies of it in a fixed outer skeleton. In DARTS a cell has 2 input nodes and 4 intermediate nodes. Each intermediate node sums 2 of its predecessors, each passed through one of 7 operations (separable and dilated convolutions of size 3 and 5, max and average pooling, identity), plus "none" during search. There are two cell types, a normal cell and a reduction cell that halves the resolution.
- *Hierarchical spaces* compose cells of smaller motifs.

The space is designed by hand, and it fixes much of the result: a well designed space contains many good architectures.

**Performance estimation.** Full training of every candidate is exact but costs the most. Cheaper estimates train for fewer epochs, on less data, or at lower resolution; extrapolate learning curves; or share weights between candidates, so that each candidate is evaluated with weights inherited from a single large *supernet*.

## Variants

- **Multi-objective and hardware-aware NAS.** Optimize accuracy and latency or energy together, with the latency measured or predicted for the target device.
- **One-shot NAS.** Train one supernet that contains all architectures, then search using its weights without retraining each candidate.
- **NAS for other domains.** Recurrent cells for language modeling, architectures for detection and segmentation, and transformer variants.
- **Joint search.** Search the architecture together with the training hyperparameters or the data augmentation policy.
- **Tabular benchmarks.** Data sets of architectures with precomputed training results, such as NAS-Bench-101, turn NAS into a cheap lookup problem for comparing search strategies.

## Examples

**The size of the DARTS cell space.** With 7 operations, intermediate node $j = 1, \ldots, 4$ chooses 2 of its $j + 1$ predecessors and one operation for each chosen edge: $\binom{j+1}{2} \cdot 7^2$ choices. The product is $1 \cdot 3 \cdot 6 \cdot 10 \cdot 49^4 \approx 1.04 \times 10^9$ per cell, and about $10^{18}$ for the pair of normal and reduction cells, by this count without merging isomorphic cells.

**The DARTS mixed operation on one edge.** DARTS replaces the discrete choice on an edge by a softmax mixture:

$$\bar o(x) = \sum_{o \in \mathcal{O}} \frac{e^{\alpha_o}}{\sum_{o'} e^{\alpha_{o'}}}\, o(x).$$

The weights are positive and sum to 1, and adding a constant to all $\alpha_o$ does not change them. Take four toy operations, "none" ($0$), "skip" ($x$), "scale" ($2x$) and "relu", with $\alpha = (0, 1, 0.5, -1)$. The weights are $(0.174, 0.474, 0.288, 0.064)$. For $x = (1, -2, 0.5)$ the mixed output is about $(1.113, -2.098, 0.557)$. After the search the edge keeps the operation with the largest weight other than "none", here "skip".

**The derivative in the architecture weights.** Since $\partial w_o / \partial \alpha_{o'} = w_o(\mathbb{1}[o = o'] - w_{o'})$, the gradient of a loss $\mathcal{L}$ is

$$\frac{\partial \mathcal{L}}{\partial \alpha_o} = w_o \left\langle \frac{\partial \mathcal{L}}{\partial \bar o},\ o(x) - \bar o(x) \right\rangle,$$

which sums to zero over $o$. An operation gains weight when its output points in a better direction than the current mixture. This is how [backpropagation](/backpropagation/) reaches the architecture weights.

**Discretization can surprise.** For each intermediate node, DARTS keeps the 2 incoming edges whose best non-"none" weight is largest. An edge with $\alpha = (4, 0, 0, 0, 2)$, where "none" dominates, has best real weight $e^2 / (e^4 + 3 + e^2) \approx 0.11$, below an edge with uniform $\alpha$ (weight $0.2$). So an edge that the search found important, through the "none" weight, can be dropped.

## Known algorithms

- **Reinforcement learning.** A recurrent controller samples an architecture as a token sequence; the child network is trained, and its validation accuracy is the reward for [REINFORCE](/reinforce/) (Zoph and Le 2017). The first results matched hand designed networks on CIFAR-10 and Penn Treebank, at the cost of training thousands of child networks on hundreds of GPUs.
- **Evolution.** Keep a population of architectures, mutate the best ones (change an operation or a connection), and train the children. Aging evolution removes the oldest member instead of the worst, which favors architectures that train well again and again (Real et al. 2019). See [evolutionary computation](/evolutionary-computation/).
- **Weight sharing.** ENAS treats every architecture as a subgraph of one large graph with shared weights, so a sampled child is evaluated without training it from scratch (Pham et al. 2018). The cost falls by orders of magnitude.
- **DARTS.** Relax every edge to the mixed operation, so the supernet has weights $w$ and architecture weights $\alpha$. Solve the bilevel problem $\min_\alpha \mathcal{L}_{\text{val}}(w^\star(\alpha), \alpha)$ with $w^\star(\alpha) = \arg\min_w \mathcal{L}_{\text{train}}(w, \alpha)$ approximately, by alternating a [gradient](/gradient-descent/) step on $w$ with the training loss and a step on $\alpha$ with the validation loss. The second order version approximates $w^\star(\alpha)$ by one step $w - \xi \nabla_w \mathcal{L}_{\text{train}}$ and needs a Hessian-vector product, computed by finite differences; the first order version sets $\xi = 0$. At the end, discretize and retrain the chosen architecture from scratch. The search takes a few GPU days.
- **Random search baselines.** Sample architectures uniformly from the space and evaluate them with early stopping or with shared weights. Li and Talwalkar (2019) found that this matched ENAS and DARTS on the standard CIFAR-10 and Penn Treebank benchmarks, which shows how much of the result comes from the search space and the training setup.
- **Bayesian optimization and successive halving.** Surrogate models over architectures, using graph kernels or learned encodings, and the multi-fidelity methods of [hyperparameter tuning](/hyperparameter-tuning/) apply directly.

## Bounds

There is no theory that guarantees that any practical NAS method finds a near-optimal architecture. As a [black-box](/black-box-optimization/) problem over a finite space, the worst case needs an evaluation of every architecture, and with $10^{18}$ candidates any method relies on structure. The cost of one exact evaluation is a full training run, so the total cost of exact search is the number of evaluations times the training cost; this is why performance estimation dominates the design of methods. Cheap estimates change the problem: if the ranking by shared weights or short training differs from the ranking after full training, the search optimizes the wrong objective. Reports that this ranking correlation can be low, and the strength of random baselines, are observations from benchmarks, not theorems.

## Reductions

- **To hyperparameter tuning.** An architecture is a vector of categorical and conditional hyperparameters, so every method of [hyperparameter tuning](/hyperparameter-tuning/) applies, and NAS is a special case of it.
- **To reinforcement learning.** Generating an architecture token by token is a sequential decision problem with a reward at the end; the policy gradient method [REINFORCE](/reinforce/) trains the generator.
- **To continuous bilevel optimization.** The softmax relaxation of DARTS turns the discrete choice into a continuous problem in $\alpha$, at the cost of a gap between the relaxed supernet and the discretized network.
- **To bandits.** Successive halving over sampled architectures is best arm identification, as in Hyperband.

## Applications

- Image classification cells found by search transfer from CIFAR-10 to ImageNet when stacked more times, and searched cells have been used in production image models.
- Hardware-aware search for mobile and embedded devices, where latency, memory and energy limits make hand design hard.
- Search for recurrent cells for language modeling, and for parts of transformer models.
- Combined with [pruning](/neural-network-pruning/) and [knowledge distillation](/knowledge-distillation/) to design small, fast models.
- Benchmarks such as NAS-Bench-101 serve to test search strategies themselves at low cost.

**Pitfalls in practice.** DARTS can collapse to cells made mostly of skip connections and parameter-free operations, especially with long searches; Zela et al. (2020) link this to high curvature of the validation loss in $\alpha$ and propose early stopping and regularization. Results depend on seeds, and comparisons need the same search space, training pipeline and compute budget, with a random search baseline.

## References
