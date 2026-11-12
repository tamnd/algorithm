---
tag: 66QJ8T
kind: concept
slug: lottery-ticket-hypothesis
name: Lottery ticket hypothesis
aliases:
- winning tickets
- winning lottery tickets
- iterative magnitude pruning with rewinding
area: machine-learning/neural-network-training
level: research
summary: "The empirical claim that a random dense network holds a sparse subnetwork that, reset to its initial weights, trains to the same accuracy. Found by iterative magnitude pruning."
prereqs: [neural-network-pruning, stochastic-gradient-descent]
see_also: [double-descent, neural-tangent-kernel, he-initialization, knowledge-distillation, subset-sum-problem, compressed-sensing, feature-selection]
sources:
  - url: https://arxiv.org/abs/1803.03635
    title: Jonathan Frankle and Michael Carbin, The lottery ticket hypothesis, finding sparse, trainable neural networks, ICLR 2019
    locator: Section 1 (the statement of the hypothesis and iterative pruning with reset to initialization), Sections 2 to 4 (fully connected and convolutional networks, random reinitialization controls, deeper networks with warmup)
  - url: https://arxiv.org/abs/1912.05671
    title: Jonathan Frankle, Gintare Karolina Dziugaite, Daniel M. Roy and Michael Carbin, Linear mode connectivity and the lottery ticket hypothesis, ICML 2020
    locator: the instability analysis, and rewinding to an early iteration instead of to the initialization
  - url: https://arxiv.org/abs/2002.00585
    title: Eran Malach, Gilad Yehudai, Shai Shalev-Shwartz and Ohad Shamir, Proving the lottery ticket hypothesis, pruning is all you need, ICML 2020
    locator: the main theorem (a random network of twice the depth and polynomially larger width contains, with high probability, a weight subnetwork that approximates any bounded target ReLU network without training)
  - url: https://arxiv.org/abs/2006.07990
    title: Ankit Pensia, Shashank Rajput, Alliot Nagle, Harit Vishwakarma and Dimitris Papailiopoulos, Optimal lottery tickets via SubsetSum, logarithmic over-parameterization is sufficient, NeurIPS 2020
    locator: the width bound that is a logarithmic factor larger than the target, through random subset sum
  - url: https://arxiv.org/abs/2006.12156
    title: Laurent Orseau, Marcus Hutter and Omar Rivasplata, Logarithmic pruning is all you need, NeurIPS 2020
    locator: the strong lottery ticket bound with a logarithmic overhead in width
  - url: https://arxiv.org/abs/1911.13299
    title: Vivek Ramanujan, Mitchell Wortsman, Aniruddha Kembhavi, Ali Farhadi and Mohammad Rastegari, What's hidden in a randomly weighted neural network?, CVPR 2020
    locator: the edge-popup algorithm that finds good subnetworks of untrained random networks
  - url: https://arxiv.org/abs/1810.05270
    title: Zhuang Liu, Mingjie Sun, Tinghui Zhou, Gao Huang and Trevor Darrell, Rethinking the value of network pruning, ICLR 2019
    locator: the experiments where pruned architectures trained from a new random initialization match the inherited weights
---

The lottery ticket hypothesis of Frankle and Carbin (2019) says that a randomly initialized dense network contains a sparse subnetwork, a *winning ticket*, that trains in isolation to the accuracy of the full network in at most the same number of steps, when it starts from the same initial weights that it had inside the full network. The tickets are found by *iterative magnitude pruning* (IMP): train, remove the smallest weights, reset the rest to their initial values, and repeat. The hypothesis is an empirical claim: there is no proof for trained networks, and for large networks such as ResNet-50 on ImageNet, IMP finds tickets only when the reset goes to an early iteration of training instead of to the initialization. A different and stronger statement, that a large enough random network contains a good subnetwork with no training at all, is a theorem (Malach et al. 2020).

## In plain words

Large networks can often lose most of their weights after training and still work, as [pruning](/neural-network-pruning/) shows. But if you build the small network from the start and train it with fresh random weights, it usually trains worse. The lottery ticket idea explains the gap: the large network holds many small subnetworks, each with its own random starting weights, and a few of them happen to start well. Training the large network finds one of these lucky subnetworks. If you keep only that subnetwork and put back its original starting weights, it trains as well as the large network. If you give it new random starting weights, it loses that advantage. This is a pattern seen in experiments, not a law.

## The idea

**The statement.** Let $f(x; \theta)$ be a network with initial weights $\theta_0$ drawn from the usual initialization, for example [He initialization](/he-initialization/). Training with [stochastic gradient descent](/stochastic-gradient-descent/) reaches test accuracy $a$ at iteration $j$. A subnetwork is given by a mask $m \in \{0, 1\}^{|\theta|}$, and the network $f(x; m \odot \theta)$ trains only the weights where $m = 1$. The hypothesis says that there is a mask with $\lVert m \rVert_0 \ll |\theta|$ such that training $f(x; m \odot \theta)$ from $m \odot \theta_0$ reaches an accuracy $a' \ge a$ at an iteration $j' \le j$.

**How tickets are found: iterative magnitude pruning.** With a pruning rate $p$ per round and a rewind iteration $k$ ($k = 0$ in the original paper):

1. Set $m = \mathbf{1}$. Train the dense network for $T$ iterations and save $\theta_k$ and the final weights $\theta_T$.
2. Among the weights with $m = 1$, set to 0 the fraction $p$ with the smallest $|\theta_T|$.
3. Reset: $\theta \leftarrow m \odot \theta_k$.
4. Train the masked network for $T - k$ iterations, keeping the pruned weights at 0, and call the result $\theta_T$.
5. Repeat steps 2 to 4 for $r$ rounds. After $r$ rounds about $(1 - p)^r$ of the weights remain.

Pruning in many small rounds finds smaller tickets than one cut to the same size (Frankle and Carbin 2019). The cost is $r$ full trainings, which is why IMP is a tool for studying networks and not a cheap way to make them small.

**What the experiments show (observed).** For fully connected networks on MNIST and small convolutional networks on CIFAR-10, Frankle and Carbin found tickets with 10 to 20 percent of the weights that train faster and reach equal or higher test accuracy. The control experiment is decisive: the same mask with a new random initialization trains worse and more slowly. So both the structure and the initial values matter. For deeper networks, such as VGG-19 and ResNet-18, IMP with reset to $\theta_0$ found tickets only with a lower learning rate or with learning rate warmup.

**Rewinding and stability (observed).** Frankle, Dziugaite, Roy and Carbin (2020) reset the weights to $\theta_k$ for a small $k$, early in training, instead of to $\theta_0$. Then IMP finds matching subnetworks for large networks on ImageNet too. They link success to *stability to SGD noise*: train two copies from $\theta_k$ with different data orders, and look at the test error along the straight line between the two results. If the error does not rise along the line (the two copies are *linearly mode connected*), IMP from $\theta_k$ finds a matching subnetwork; if it rises, it does not. For large networks the dense network becomes stable only after some training, which explains why $k = 0$ fails there. This is a correlation found in experiments.

**Doubts (observed).** Liu et al. (2019) found that, for structured pruning and with the standard learning rates of large networks, the pruned architecture trained from a new random initialization often matches the inherited weights. So the role of the initial values depends on the setting, the learning rate and the kind of pruning.

**What is proved: the strong lottery ticket.** The *strong* form asks for a subnetwork of a random network that is already good, with no training. Malach, Yehudai, Shalev-Shwartz and Shamir (2020) proved it for ReLU networks:

> Let $F$ be a ReLU network of depth $l$ with bounded weights, on inputs of bounded norm. A random network $G$ of depth $2l$, with weights drawn independently from a fixed distribution and a width that is polynomial in the input dimension, in the width and depth of $F$, in $1/\epsilon$ and in $\log(1/\delta)$, contains with probability at least $1 - \delta$ a subnetwork $\tilde G$, obtained by removing weights only, with $\sup_x |\tilde G(x) - F(x)| \le \epsilon$.

The proof approximates each target weight by one of many random weights through a pair of layers. Pensia et al. (2020) and Orseau, Hutter and Rivasplata (2020) reduced the overhead in width to a logarithmic factor. Pensia et al. use the fact that a sum of a random subset of $O(\log(1/\epsilon))$ uniform random numbers can approximate any target number in an interval, a random version of the [subset sum problem](/subset-sum-problem/). The theorem is an existence result: it does not say how to find the subnetwork, and finding the best mask is a hard combinatorial search. Ramanujan et al. (2020) find such masks in practice by training a score per weight while the weights stay at their random values.

**What is not proved.** No theorem says that IMP on a trained network finds a ticket, or that winning tickets exist for the weak form (train from $m \odot \theta_0$) in the networks used in practice. The weak form is a hypothesis supported by experiments, with the rewinding fix for large networks.

## Examples

**IMP on a sparse linear model.** A toy shows the mechanics. Take $n = 30$ samples of $p = 40$ Gaussian features, a true coefficient vector with 5 nonzero entries $(2, -1.5, 1, -0.8, 0.6)$, noise of standard deviation 0.1, the initial weights $\theta_0 \sim N(0, 0.25)$, 300 steps of [gradient descent](/gradient-descent/) with step 0.05 on the squared error, and 20 percent pruning per round (seed `random.Random(7)`). The test loss is the squared error on 200 new samples, halved.

| weights left | IMP ticket test loss | random mask of the same size |
|---|---|---|
| 40 | 5.45 | 5.45 |
| 26 | 4.83 | 5.03 |
| 17 | 1.21 | 6.95 |
| 12 | 0.17 | 2.90 |
| 8 | 0.034 | 3.90 |

With $p > n$ the dense model fits the noise and the irrelevant features; IMP removes the irrelevant ones and keeps all 5 true features at 8 weights. The weights left follow $40, 32, 26, 21, 17, 14, 12, 10, 8$, the floor of 20 percent per round. This toy is convex, so the result after training does not depend much on $\theta_0$: it shows how IMP works and that a found mask beats a random one, not why the initialization matters in deep networks.

**Small vision networks (Frankle and Carbin 2019).** For the LeNet-300-100 fully connected network on MNIST, tickets with fewer than 20 percent of the weights match the dense network, and tickets of moderate size learn faster and reach a higher test accuracy. Reinitialized copies of the same tickets fall behind as the sparsity grows.

**Large networks with rewinding (Frankle et al. 2020).** For ResNet-50 on ImageNet, reset to $\theta_0$ fails, but reset to an iterate a few percent into training finds subnetworks with a large fraction of the weights removed that match the dense accuracy.

## Where it is used

- **Understanding training.** The hypothesis is mainly a lens on why overparameterized networks train well: a large network gives many chances for a good subnetwork, a view that sits beside [double descent](/double-descent/) and the [neural tangent kernel](/neural-tangent-kernel/).
- **Pruning research.** It motivated pruning at or near initialization, and rewinding is now a standard baseline step in [neural network pruning](/neural-network-pruning/) studies.
- **Transfer of tickets.** Tickets found on one data set or task have been reused on others, and tickets in pretrained language models have been studied in the same way.
- **Not a speedup on its own.** IMP needs many full trainings, so it does not save compute when the goal is one trained model. The savings come only if a ticket can be found cheaply or reused.

## References
