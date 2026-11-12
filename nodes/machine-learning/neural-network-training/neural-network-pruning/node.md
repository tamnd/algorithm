---
tag: 8KRCTK
kind: technique
slug: neural-network-pruning
name: Neural network pruning
aliases:
- weight pruning
- network pruning
- neural network sparsification
area: machine-learning/neural-network-training
level: advanced
summary: "Remove weights, neurons or channels that matter least for the loss, then fine-tune. Scores range from the weight magnitude to the second order saliencies of optimal brain damage and surgeon."
prereqs: [backpropagation, gradient, positive-definite-matrix]
see_also: [lottery-ticket-hypothesis, knowledge-distillation, weight-decay, dropout, sparse-matrix, lasso-regression, sherman-morrison-formula, cost-complexity-pruning]
sources:
  - paper: "Yann LeCun, John S. Denker and Sara A. Solla, Optimal brain damage, Advances in Neural Information Processing Systems 2 (NIPS 1989), Morgan Kaufmann, 1990"
    locator: the second order Taylor expansion of the loss, the diagonal approximation of the Hessian and the saliency h_kk u_k^2 / 2
  - paper: "Babak Hassibi and David G. Stork, Second order derivatives for network pruning, optimal brain surgeon, Advances in Neural Information Processing Systems 5 (NIPS 1992), Morgan Kaufmann, 1993"
    locator: the constrained quadratic problem, the weight update and the saliency w_q^2 / (2 [H^-1]_qq), and the recursive computation of the inverse Hessian from gradient outer products
  - url: https://arxiv.org/abs/1506.02626
    title: Song Han, Jeff Pool, John Tran and William J. Dally, Learning both weights and connections for efficient neural networks, NIPS 2015
    locator: the train, prune, retrain loop with magnitude pruning, and the parameter reductions for AlexNet and VGG-16
  - url: https://arxiv.org/abs/1608.08710
    title: Hao Li, Asim Kadav, Igor Durdanovic, Hanan Samet and Hans Peter Graf, Pruning filters for efficient ConvNets, ICLR 2017
    locator: structured pruning of whole filters ranked by the L1 norm of their weights
  - url: https://arxiv.org/abs/2003.03033
    title: Davis Blalock, Jose Javier Gonzalez Ortiz, Jonathan Frankle and John Guttag, What is the state of neural network pruning?, MLSys 2020
    locator: the survey of pruning methods and the problems of comparing them
  - url: https://arxiv.org/abs/2301.00774
    title: Elias Frantar and Dan Alistarh, SparseGPT, massive language models can be accurately pruned in one-shot, ICML 2023
    locator: layer-wise pruning with optimal brain surgeon updates on the Hessian of the layer reconstruction loss
---

Neural network pruning removes parameters from a trained network: single weights (unstructured pruning) or whole neurons, channels, filters or attention heads (structured pruning). Each candidate gets a *saliency*, an estimate of how much the loss grows when it is removed, and the ones with the smallest saliency go. The simplest saliency is the absolute value of the weight. *Optimal brain damage* (LeCun, Denker and Solla 1990) and *optimal brain surgeon* (Hassibi and Stork 1993) derive the saliency from a second order expansion of the loss, and the surgeon also corrects the other weights. After pruning, the network is usually fine-tuned to recover accuracy.

## In plain words

A trained network often has many weights that do almost nothing. If you set them to zero, the network gives nearly the same answers, and it becomes smaller and can be faster. The question is which weights to remove. The easy rule is to remove the smallest weights. A better rule asks how much the error grows when a weight goes. A weight can be large and still be safe to remove, if the other weights can take over its job. The best rule also says how to change the remaining weights to make up for the loss. After removing a share of the weights, you train the network a little more, and you can repeat the cycle until the network is as small as you want.

## When it applies

The architecture can be a multilayer perceptron, a convolutional network or a transformer. Pruning changes the model after training, or at fixed points during training; it does not change the loss or the optimizer of the training loop itself. It needs:

- **A trained model with spare capacity.** Large networks often lose little accuracy when many of their weights are removed. This is an observation, not a theorem, and the share that can go depends on the task and the model.
- **A goal that sparsity serves.** Fewer nonzero weights mean less storage. They mean less time only when the hardware or the library can skip the zeros. A dense matrix product does not run faster on a matrix with scattered zeros. Structured pruning removes whole rows or channels, so the remaining model is a smaller dense model and runs faster on any hardware.
- **A local quadratic model, for the second order rules.** Optimal brain damage and surgeon assume that the network sits at a local minimum of the training loss, so the gradient is about zero and the Hessian describes the loss nearby.

## The template

Let $\theta = w \in \mathbb{R}^P$ be the weights of a trained network and $L(w)$ the training loss.

1. **Score.** For each weight $q$ (or each group of weights), compute a saliency $s_q$.
2. **Remove.** Set to zero the weights with the smallest saliency, up to a target fraction. Keep a 0/1 mask $M$ so that they stay at zero.
3. **Compensate or fine-tune.** Either apply a closed form correction to the other weights (optimal brain surgeon), or train the masked network $w \odot M$ for some steps.
4. **Repeat** steps 1 to 3 with a growing target fraction, until the target sparsity is reached or the accuracy falls too far.

**The second order saliencies.** Expand the loss around $w$ for a change $\delta w$:

$$L(w + \delta w) - L(w) = g^\top \delta w + \tfrac12\, \delta w^\top H\, \delta w + O(\lVert \delta w \rVert^3),$$

with $g = \nabla L(w)$ and $H = \nabla^2 L(w)$. At a minimum $g = 0$, and the change is the quadratic term. Removing weight $q$ means the constraint $e_q^\top \delta w + w_q = 0$.

- **Magnitude pruning** ignores $H$: $s_q = |w_q|$.
- **Optimal brain damage (OBD)** changes only $w_q$, so $\delta w = -w_q e_q$, and keeps only the diagonal of $H$: $s_q = \tfrac12 h_{qq} w_q^2$. The diagonal costs about as much as one gradient.
- **Optimal brain surgeon (OBS)** lets all weights move. It solves

$$\min_{\delta w}\ \tfrac12\, \delta w^\top H\, \delta w \quad \text{subject to} \quad e_q^\top \delta w + w_q = 0.$$

**Proposition (Hassibi and Stork).** For $H$ symmetric positive definite, the minimizer and the minimum are

$$\delta w = -\frac{w_q}{[H^{-1}]_{qq}}\, H^{-1} e_q, \qquad L_q = \frac{w_q^2}{2\,[H^{-1}]_{qq}}.$$

*Proof.* The Lagrangian is $\tfrac12 \delta w^\top H \delta w + \lambda (e_q^\top \delta w + w_q)$. Its gradient in $\delta w$ is $H \delta w + \lambda e_q = 0$, so $\delta w = -\lambda H^{-1} e_q$. The constraint gives $-\lambda [H^{-1}]_{qq} + w_q = 0$, so $\lambda = w_q / [H^{-1}]_{qq}$, which is the update. Then $\tfrac12 \delta w^\top H \delta w = \tfrac12 \lambda^2 e_q^\top H^{-1} e_q = \tfrac12 w_q^2 / [H^{-1}]_{qq}$. The objective is strictly convex and the constraint is linear, so this stationary point is the unique minimizer. $\blacksquare$

On a loss that is exactly quadratic, $L(w) = L(w^*) + \tfrac12 (w - w^*)^\top H (w - w^*)$, the expansion has no remainder, so $L_q$ is the exact increase of the loss and the OBS update gives the best weights with $w_q = 0$.

**OBS never predicts more damage than OBD.** By the Cauchy-Schwarz inequality, $1 = (e_q^\top H^{1/2} H^{-1/2} e_q)^2 \le (e_q^\top H e_q)(e_q^\top H^{-1} e_q) = h_{qq} [H^{-1}]_{qq}$. So $L_q \le \tfrac12 h_{qq} w_q^2$, with equality when $e_q$ is an eigenvector of $H$, for example when $H$ is diagonal. On a quadratic loss at its minimum, the OBD saliency is the exact increase when $w_q$ is removed and the other weights stay; the OBS saliency is the exact increase when they move.

**Pruning several weights.** After weight $q$ is removed, the next OBS step works on the remaining set $R$, with the Hessian $H_{RR}$. Its inverse follows from the old one without a new inversion:

$$(H_{R'R'})^{-1} = (H^{-1})_{R'R'} - \frac{(H^{-1})_{R'q}\,(H^{-1})_{qR'}}{[H^{-1}]_{qq}}, \qquad R' = R \setminus \{q\}.$$

On a quadratic loss, a sequence of OBS steps on the sets $\{q_1\}, \{q_1, q_2\}, \ldots$ ends at the exact minimizer of $L$ subject to $w_{q_1} = \cdots = w_{q_k} = 0$, and the sum of the step saliencies is the exact increase. The choice of the set is greedy, so the final set need not be the best set of $k$ weights.

**Cost.** For $P$ weights: magnitude pruning needs $O(P)$ time to score and $O(P)$ to select a fraction (by selection, or $O(P \log P)$ by sorting). OBD needs the diagonal of $H$, about the cost of one extra backward pass per example. OBS needs $H^{-1}$, which is $P^2$ numbers and $O(P^3)$ time if formed directly; this is impossible for modern networks. Hassibi and Stork approximate $H$ by a sum of outer products of gradients (the Gauss-Newton or Fisher form) and build its inverse with one [Sherman-Morrison](/sherman-morrison-formula/) update per example. SparseGPT and related methods apply OBS layer by layer, where the Hessian of the layer's squared reconstruction error is $2 X X^\top$ for the layer inputs $X$ and has only the size of one layer's input.

## Classic examples

**Three weights on a quadratic loss.** Take $L(w) = \tfrac12 (w - w^*)^\top H (w - w^*)$ with

$$H = \begin{pmatrix} 4 & 2 & 0 \\ 2 & 3 & 1 \\ 0 & 1 & 2 \end{pmatrix}, \qquad w^* = \big(\tfrac12, -1, \tfrac34\big), \qquad H^{-1} = \begin{pmatrix} 5/12 & -1/3 & 1/6 \\ -1/3 & 2/3 & -1/3 \\ 1/6 & -1/3 & 2/3 \end{pmatrix}.$$

| weight $q$ | magnitude $\lvert w_q \rvert$ | OBD $\tfrac12 h_{qq} w_q^2$ | OBS $w_q^2 / (2[H^{-1}]_{qq})$ |
|---|---|---|---|
| 1 | 1/2 | 1/2 | 3/10 |
| 2 | 1 | 3/2 | 3/4 |
| 3 | 3/4 | 9/16 | 27/64 |

All three rules remove $w_1$ first. Without compensation the loss rises by $1/2$. The OBS update is $\delta w = -\tfrac{1/2}{5/12} H^{-1} e_1 = (-\tfrac12, \tfrac25, -\tfrac15)$, which gives $w = (0, -\tfrac35, \tfrac{11}{20})$ and a loss of exactly $3/10$, 40 percent less. A second OBS step removes $w_3$ and adds $121/480$, which ends at $w = (0, -\tfrac{5}{12}, 0)$ with the loss $53/96 \approx 0.552$. Magnitude pruning of the same two weights without retraining leaves $w = (0, -1, 0)$ with the loss $17/16$. Retraining $w_2$ alone after magnitude pruning would reach the same $53/96$, because here both rules removed the same set.

**Magnitude pruning of large convolutional networks.** Han, Pool, Tran and Dally (2015) trained a network, removed the weights below a threshold, retrained the rest, and repeated. They report 9 times fewer parameters for AlexNet and 13 times fewer for VGG-16 on ImageNet with no loss of accuracy. The pruned layers are sparse, so the speed gain needs sparse kernels.

**Structured pruning of filters.** Li et al. (2017) rank the filters of each convolutional layer by the $L_1$ norm of their weights, remove whole filters and the matching input channels of the next layer, and retrain. The result is a thinner dense network that runs faster with standard libraries.

## Variations

- **Global or per layer.** A global threshold compares weights across layers; a per layer fraction protects small layers such as the first and the last. The magnitudes of different layers are on different scales, so a global threshold can empty a layer.
- **Gradual pruning.** Raise the sparsity in small steps during training, for example along a cubic schedule, instead of one large cut.
- **Pruning at initialization and rewinding.** Choose the mask early and train only the kept weights. The [lottery ticket hypothesis](/lottery-ticket-hypothesis/) is the claim that such masks exist; it uses iterative magnitude pruning with a reset of the kept weights.
- **Sparsity by penalty.** An $L_1$ penalty, as in the [lasso](/lasso-regression/), or a group penalty on rows drives weights or groups to zero during training. [Weight decay](/weight-decay/) alone shrinks weights but does not make them zero.
- **Semi-structured sparsity.** Keep $N$ nonzero weights in each block of $M$, for example 2 of 4, a pattern that some GPUs run at higher speed.
- **Other compression.** Pruning combines with quantization of the remaining weights and with [knowledge distillation](/knowledge-distillation/) into a smaller dense student.

## Pitfalls

- **Sparse is not fast.** Unstructured sparsity reduces the parameter count, but the time falls only with sparse kernels and a high sparsity. Report the time or the operation count on the target hardware, not only the number of zeros.
- **Not at a minimum.** The OBD and OBS saliencies drop the gradient term. After a short training, or with early stopping, $g \neq 0$ and the first order term $g_q w_q$ can dominate.
- **A singular Hessian.** The Hessian of a large network has many zero or negative eigenvalues. OBS then needs a damped Hessian $H + \lambda I$ or a Gauss-Newton approximation, and its saliency is no longer exact.
- **Unfair comparisons.** Methods are often compared with different fine-tuning budgets, data sets and baselines (Blalock et al. 2020). A pruned large model must be compared with a small dense model trained with the same budget.
- **Normalization statistics.** After structured pruning, the running statistics of [batch normalization](/batch-normalization/) no longer match; recompute them on training data.
- **The mask must persist.** Fine-tuning with a plain optimizer revives pruned weights unless the gradient or the weight is masked after each step.

## Exercises

1. Show that on a quadratic loss at its minimum, the OBD saliency $\tfrac12 h_{qq} w_q^2$ is the exact increase of the loss when only $w_q$ is set to zero.
2. Prove the update rule for $(H_{R'R'})^{-1}$ from the block inverse formula, and use it to show that two OBS steps reach the minimizer subject to two zero weights.
3. Find a symmetric positive definite $2 \times 2$ matrix $H$ and a vector $w^*$ for which magnitude pruning and OBS remove different weights.
4. A layer has a $512 \times 512$ weight matrix. How many numbers does the full OBS inverse Hessian for this layer hold, and how many does the layer-wise reconstruction Hessian hold?

## References
