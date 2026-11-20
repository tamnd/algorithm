---
tag: KG5S6M
kind: algorithm
slug: lista
name: Learned ISTA
aliases:
- LISTA
area: imaging-and-inverse-problems/variational-and-learned-reconstruction
level: research
summary: "A fixed number of ISTA-shaped layers soft(W_e y + S x, theta) whose matrices and thresholds are trained on data, to approximate sparse codes in fewer steps than ISTA."
solves: [sparse-signal-recovery]
model: real-ram
complexity:
  vars: {K: the number of layers, m: the number of measurements, n: the number of unknowns}
  time: {worst: O(K (m n + n^2))}
  space: {extra: O(n)}
properties: {deterministic: true, iterative: true, learned: true, exact: false}
history:
  year: 2010
  people: [Karol Gregor, Yann LeCun]
  note: "Gregor and LeCun (ICML 2010) trained the matrices and thresholds of a truncated ISTA to predict the optimal sparse codes of image patches. Chen, Liu, Wang and Yin (NeurIPS 2018) proved that weights with linear convergence exist."
prereqs: [iterative-shrinkage-thresholding, backpropagation, sparse-signal-recovery]
see_also: [algorithm-unrolling, fista, approximate-message-passing, learned-primal-dual, lasso-regression, coordinate-descent, variational-network-mri, dictionary-learning]
sources:
  - url: https://icml.cc/Conferences/2010/papers/449.pdf
    title: "Karol Gregor and Yann LeCun, Learning fast approximations of sparse coding, Proceedings of the 27th International Conference on Machine Learning (ICML), 2010"
    locator: "pages 399 to 406 (eq. 2 for ISTA in the form h_theta(W_e X + S Z), Section 3 and Algorithms 3 and 4 for the LISTA forward and backward pass, Table 1 for the comparison with FISTA)"
  - paper: arxiv:1808.10038
    title: "Xiaohan Chen, Jialin Liu, Zhangyang Wang and Wotao Yin, Theoretical linear convergence of unfolded ISTA and its practical weights and thresholds, Advances in Neural Information Processing Systems 31 (NeurIPS), 2018"
    locator: Theorem 1 (the coupling of W and S is necessary) and Theorem 2 (LISTA-CP weights with linear convergence exist)
  - paper: doi:10.1137/080716542
    title: "Amir Beck and Marc Teboulle, A fast iterative shrinkage-thresholding algorithm for linear inverse problems, SIAM Journal on Imaging Sciences 2(1), 2009"
    locator: "Section 3, Theorem 3.1 (the O(1/k) bound of ISTA, which LISTA with the ISTA weights inherits)"
  - paper: doi:10.1109/MSP.2020.3016905
    title: "Vishal Monga, Yuelong Li and Yonina C. Eldar, Algorithm unrolling, interpretable, efficient deep learning for signal and image processing, IEEE Signal Processing Magazine 38(2), 2021"
    locator: "pages 18 to 44 (LISTA as the first unrolled network, and its later variants)"
---

Learned ISTA (LISTA) is a network of $K$ layers, each of the form $x \leftarrow \operatorname{soft}(W_e y + S x, \theta)$, that maps data $y$ to an approximate sparse code $x$. With the weights $W_e = A^T/L$, $S = I - A^TA/L$ and $\theta = \lambda/L$ it is exactly $K$ steps of [ISTA](/iterative-shrinkage-thresholding/) for the lasso $\min_x \tfrac12\|Ax - y\|^2 + \lambda\|x\|_1$. LISTA instead trains $W_e$, $S$ and $\theta$ on examples, so that a few layers give codes that ISTA needs many more steps to reach. Gregor and LeCun (2010) introduced it, and it was the first unrolled network (see [algorithm unrolling](/algorithm-unrolling/)). The equality with ISTA is a theorem. The speed-up is a measurement on a data distribution, and the trained network has no correctness guarantee for data outside that distribution.

## In plain words

ISTA finds a sparse code by small steps. Each step does a fixed matrix product, adds a fixed vector made from the data, and then sets the small entries to zero and shrinks the others. It needs many steps, because the step rules were chosen to work for every possible input.

LISTA keeps the shape of one step but lets a computer tune its numbers from examples. You run the tuned step a few times, for example three times, and stop. If the new inputs look like the examples, the tuned steps reach a good code much sooner than the general ones. If they do not, nothing promises a good answer.

## The problem

The input is a vector $y \in \mathbb{R}^m$ and trained weights: for each layer $k = 1, \ldots, K$ an $n \times m$ matrix $W_e^k$, an $n \times n$ matrix $S^k$ and a vector $\theta^k \ge 0$ of $n$ thresholds. With tied weights all layers share one triple. The output is a code $x \in \mathbb{R}^n$.

The training problem behind the weights is this. For a dictionary or forward operator $A \in \mathbb{R}^{m \times n}$ and a weight $\lambda > 0$, let $x^\star(y)$ be the lasso solution $\arg\min_x \tfrac12\|Ax - y\|^2 + \lambda\|x\|_1$ (see [sparse signal recovery](/sparse-signal-recovery/) and [lasso regression](/lasso-regression/)). Gregor and LeCun choose the weights that minimize the mean of $\tfrac12\|x^K(y) - x^\star(y)\|^2$ over a training set of data vectors $y$. Other papers train against the true sparse signal instead of the lasso solution.

## The algorithm

Here $\operatorname{soft}(v, \theta)_i = \operatorname{sign}(v_i)\max(|v_i| - \theta_i, 0)$.

```pseudo id=main
LISTA(y, (W_e^k, S^k, θ^k) for k = 1..K)
L1  x ← 0
L2  for k = 1 to K
L3      c ← W_e^k y + S^k x                ▷ linear part of layer k
L4      x ← soft(c, θ^k)                   ▷ shrinkage with learned thresholds
L5  return x
```

Line L3 is the only place where the data enters. With tied weights the vector $W_e y$ is computed once before the loop. Gregor and LeCun write the first layer as $\operatorname{soft}(W_e y, \theta)$; it is the case $x = 0$ of line L3.

**The ISTA weights.** ISTA for the lasso with step $1/L$, $L \ge \|A\|^2$, is $x \leftarrow \operatorname{soft}(x - \tfrac1L A^T(Ax - y), \lambda/L)$. Expand the argument: $x - \tfrac1L A^TAx + \tfrac1L A^Ty = Sx + W_e y$ with $W_e = A^T/L$ and $S = I - A^TA/L$. So one layer with these weights and $\theta = (\lambda/L)\mathbf{1}$ is one ISTA step.

**Training.** The weights are fitted by stochastic gradient descent on the loss above. The gradient comes from [backpropagation](/backpropagation/) through lines L3 and L4: soft thresholding passes the gradient through the active entries ($|c_i| > \theta_i$) and blocks it at the others, and its derivative in $\theta_i$ is $-\operatorname{sign}(c_i)$ on the active entries. The implementation writes these formulas by hand and checks them against finite differences.

## Example

Take $A = \begin{pmatrix}1 & 0 & 0.6\\ 0 & 1 & 0.8\end{pmatrix}$, $y = (0.6, 0.8)$ and $\lambda = 0.1$. The third column of $A$ has norm 1 and equals $y$. The lasso solution is $x^\star = (0, 0, 0.9)$: at this point the residual is $y - Ax^\star = (0.06, 0.08)$ and $A^T(y - Ax^\star) = (0.06, 0.08, 0.1)$, which is $\lambda$ on the support and less than $\lambda$ in absolute value elsewhere. The matrix $AA^T$ has the eigenvalues 2 and 1, so $L = \|A\|^2 = 2$ and $\theta = 0.05$.

LISTA with the ISTA weights, run for $K$ layers, gives the ISTA iterates:

| $K$ | $x^K$ | $\|x^K - x^\star\|$ |
|---|---|---|
| 1 | (0.25, 0.35, 0.45) | 0.6225 |
| 2 | (0.24, 0.345, 0.46) | 0.6085 |
| 10 | (0.188016, 0.283988, 0.54) | 0.4956 |
| 40 | (0.008, 0.044, 0.84) | 0.0748 |
| 46 | (0, 0, 0.889332) | 0.0107 |
| 50 | (0, 0, 0.899333) | 0.000667 |

The first layer gives $\operatorname{soft}(A^Ty/2, 0.05) = \operatorname{soft}((0.3, 0.4, 0.5), 0.05)$. The false entries $x_1$ and $x_2$ fall slowly, and ISTA finds the correct support only at step 46. After that the error halves at each step, because on the support the step multiplies the error by $1 - \|a_3\|^2/L = 1/2$. Step 50 is the first with an error below 0.001.

Now take a hand-made network of one layer: $W_e$ has the rows $(0, 0)$, $(0, 0)$ and $(0.6, 0.8)$, $S = 0$ and $\theta = (0, 0, 0.1)$. For every $y = t\,(0.6, 0.8)$ with $t > 0.1$ it returns $(0, 0, t - 0.1)$, and this is the lasso solution for that $y$ by the same check as above. So on this family of inputs one layer does the work of 50 ISTA steps. For $y = (1, 0)$, outside the family, the lasso solution is $(0.9, 0, 0)$, but the same layer returns $(0, 0, 0.5)$. This is the whole story of LISTA in small form: weights fitted to a family of inputs can be much faster than ISTA on it, and can be wrong off it.

## Correctness

Three statements are proved in the proof file below. First, one layer with the ISTA weights is one ISTA step, so the network is ISTA by induction. Second, with these weights the fixed points of a layer are exactly the lasso solutions, because soft thresholding is the [proximal operator](/proximal-operator/) of the $\ell_1$ norm. Third, the backpropagation formulas give the gradient of the training loss wherever no entry sits exactly on a threshold.

For trained weights there is no correctness theorem. What is known is about existence. Chen, Liu, Wang and Yin (2018) assume a noise level, entries of $x^\star$ bounded by $B$ and at most $s$ nonzero entries. Theorem 1 of their paper: if a network recovers every such $x^\star$ from noiseless data as $K \to \infty$, with bounded weights, then $S^k - (I - W_e^kA) \to 0$ and $\theta^k \to 0$. This coupling motivates LISTA-CP, with layers $x \leftarrow \operatorname{soft}(x + (W^k)^T(y - Ax), \theta^k)$. Theorem 2: if $s$ is small enough, there are weights and thresholds for LISTA-CP with $\|x^k - x^\star\| \le sB e^{-ck} + C\sigma$ for constants $c, C > 0$ and a noise bound $\sigma$. The theorem does not say that training finds these weights.

## Complexity

The model is real-ram. A layer with general weights costs one product with $W_e^k$ ($mn$ operations), one with $S^k$ ($n^2$ operations) and $O(n)$ for the threshold. So $K$ layers cost $O(K(mn + n^2))$ time and $O(n)$ extra space, and with tied weights $O(mn + Kn^2)$. The weights take $O(K(mn + n^2))$ memory, or $O(mn + n^2)$ when tied.

One ISTA step costs one product with $A$ and one with $A^T$: $O(mn)$ for a dense matrix, or the cost of these two calls for a matrix-free operator. So a layer of LISTA costs about the same as a step of ISTA when $n$ is close to $m$, and more when $n \gg m$, because $S$ is a dense $n \times n$ matrix. LISTA-CP and ALISTA keep the form $x + W^T(y - Ax)$, which costs $O(mn)$ per layer and stores $A$ only once.

Training is outside the cost of the reconstruction. By backpropagation, one gradient on one example costs a small constant times the forward pass, and it stores the $K$ intermediate vectors $c^k$, so $O(Kn)$ memory.

## Properties

- **ISTA is a special case.** With the ISTA weights, LISTA is ISTA, so it inherits the bound $F(x^K) - F^\star \le L\|x^\star\|^2/(2K)$ of Beck and Teboulle (2009, Theorem 3.1) for the start $x^0 = 0$.
- **Fixed depth.** The number of layers is chosen before training, so the cost of a reconstruction is known in advance. There is no stopping rule.
- **Learned for a distribution.** The speed-up holds on data like the training data. Gregor and LeCun measured it on $10 \times 10$ patches of natural images from the Berkeley data set, with $\lambda = 0.5$ and the squared error to the optimal code as the metric: for 100 code units FISTA needed 18 steps to reach the error of one LISTA layer, and for 400 code units 35 steps. This is a measurement, not a property of the algorithm.
- **Not a lasso solver.** With trained weights the output is in general not a lasso solution for any $\lambda$, even when it is close to one.

## Variants and improvements

- **Untied layers.** Each layer has its own $(W_e^k, S^k, \theta^k)$. This is the form of the pseudocode above.
- **LISTA-CP and LISTA-CPSS** (Chen, Liu, Wang and Yin 2018). Couple $S^k = I - W^kA$, as Theorem 1 requires, and optionally keep the largest entries out of the threshold (support selection).
- **ALISTA** (Liu, Chen, Wang and Yin, ICLR 2019). Compute $W$ from $A$ by a data-free optimization and train only one step size and one threshold per layer.
- **Learned coordinate descent (LCoD).** In the same paper, Gregor and LeCun truncate and train [coordinate descent](/coordinate-descent/) in the same way.
- **Learned AMP.** Unfold [approximate message passing](/approximate-message-passing/) instead of ISTA.
- **Unrolling in general.** Any iterative solver can be truncated and trained in the same way; see [algorithm unrolling](/algorithm-unrolling/) and [learned primal-dual](/learned-primal-dual/).

## When to use it

Use LISTA when you must compute sparse codes for many inputs from one distribution under a fixed time budget, and you have enough training data from that distribution. Typical uses are fast feature extraction and the encoder of a sparse autoencoder. Do not use it when the inputs change their statistics, when you need the exact lasso solution, or when the forward operator $A$ changes from case to case: then use [ISTA](/iterative-shrinkage-thresholding/) or [FISTA](/fista/), which work for every input.

## Pitfalls

- **Wrong scaling of the ISTA start.** Initializing with $L < \|A\|^2$ gives a network that does not even match a convergent ISTA. Compute $\|A\|^2$ by power iteration and add a small margin.
- **Negative thresholds.** A gradient step can push $\theta_i$ below 0, which turns shrinkage into expansion. Project the thresholds to $\theta \ge 0$ after each step.
- **Kinks.** Soft thresholding is not differentiable at $|c_i| = \theta_i$. A finite difference check at such a point fails for a correct gradient; test at random points.
- **Reading a measured speed-up as a rate.** "One layer is worth 18 FISTA steps" was measured on one data set and one $\lambda$. It is not a bound.
- **Evaluating on the training data.** The loss must be measured on held-out examples; the example above shows how a network can be exact on its family and wrong off it.

## Implementations

The network is a given input: the code takes the list of layer weights $(W_e^k, S^k, \theta^k)$ as an argument and runs lines L1 to L5 around it. The tests build the weights by hand (the ISTA weights and the one-layer network of the example) or from a fixed seed, and train small tied networks on synthetic data. No real data and no downloaded weights are used. The tests check that LISTA with the ISTA weights equals an independent ISTA for 1 to 11 layers, the example values, the backpropagation formulas against central differences, and that a trained 3-layer network has less than a quarter of the loss of 3 ISTA steps on its training set.

## History

Gregor and LeCun (2010) observed that sparse coding by ISTA or coordinate descent is too slow for real-time feature extraction, wrote ISTA as a recurrent network with the matrices $W_e$ and $S$, and trained a truncated version to predict the optimal codes. This started the line of work now called algorithm unrolling or deep unfolding, surveyed by Monga, Li and Eldar (2021). Chen, Liu, Wang and Yin (2018) gave the first convergence theory, with the coupled form LISTA-CP, and ALISTA (2019) reduced the trained parameters to a few scalars per layer.

## References
