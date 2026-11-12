---
title: Backpropagation returns the gradient of the loss with respect to every weight and bias
proves: [correctness, termination]
status: full
---

We use the pseudocode BACKPROP of the page. The network has layers $l = 1, \ldots, L$ with $L \ge 1$, widths $d_0, \ldots, d_L$, weights $W_l \in \mathbb{R}^{d_l \times d_{l-1}}$, biases $b_l \in \mathbb{R}^{d_l}$ and elementwise activations $f_l$. The loss of one example is $\ell(a_L, y)$. Fix the input $x$ and the label $y$, and view the loss as a function of all parameters:

$$J(W_1, b_1, \ldots, W_L, b_L) = \ell(a_L, y), \quad a_0 = x, \quad z_l = W_l a_{l-1} + b_l, \quad a_l = f_l(z_l).$$

**Hypotheses.** $\ell(\cdot, y)$ is differentiable at the computed $a_L$, and for each $l$ and each unit $i$, the scalar function $f_l$ is differentiable at the computed $(z_l)_i$. At a point where an activation has a kink (ReLU at 0), the algorithm still runs, but it returns the derivative of the program with the chosen value of $f'$ there, not a gradient of $J$.

**Notation.** For $l = 1, \ldots, L$ let $\delta^\ast_l = \partial J / \partial z_l \in \mathbb{R}^{d_l}$ be the derivative of the loss with respect to the pre-activation $z_l$, where $z_l$ is treated as a free variable and the layers $l+1, \ldots, L$ are recomputed from it. Write $\odot$ for the elementwise product and $f_l'(z_l)$ for the vector $(f_l'((z_l)_i))_i$.

**Claim.** When BACKPROP returns, for every $l$: $G_l = \partial J / \partial W_l$ and $g_l = \partial J / \partial b_l$. It returns after $L$ rounds of each loop.

*Step 1: the forward loop.* Lines L1 to L4 compute $a_0 = x$ and then, for $l = 1, \ldots, L$ in order, $z_l$ and $a_l$ from $a_{l-1}$, exactly as in the definition of $J$. Each round uses only $a_{l-1}$, which the round before has computed. So after line L4 all $z_l$ and $a_l$ hold their values at the current parameters.

*Step 2: the invariant of the backward loop.* We show: at the start of the round with index $l$ of the loop at line L6, the variable $\delta$ equals $\delta^\ast_l$. We use induction on $l$ from $L$ down to $1$.

*Base, $l = L$.* $J = \ell(f_L(z_L), y)$, and $f_L$ acts on each coordinate separately, so $\partial (a_L)_i / \partial (z_L)_k = f_L'((z_L)_i)$ when $i = k$ and $0$ otherwise. By the chain rule,

$$\frac{\partial J}{\partial (z_L)_k} = \sum_i \frac{\partial \ell}{\partial (a_L)_i} \frac{\partial (a_L)_i}{\partial (z_L)_k} = \frac{\partial \ell}{\partial (a_L)_k} f_L'((z_L)_k).$$

This is line L5, so $\delta = \delta^\ast_L$ at the first round.

*Step, from $l$ to $l - 1$ for $l \ge 2$.* Assume $\delta = \delta^\ast_l$ at the start of round $l$. The loss depends on $z_{l-1}$ only through $a_{l-1} = f_{l-1}(z_{l-1})$, and $a_{l-1}$ enters the rest of the network only through $z_l = W_l a_{l-1} + b_l$. So $\partial (z_l)_i / \partial (a_{l-1})_j = (W_l)_{ij}$, and by the chain rule

$$\frac{\partial J}{\partial (a_{l-1})_j} = \sum_{i=1}^{d_l} (\delta^\ast_l)_i (W_l)_{ij} = (W_l^\top \delta^\ast_l)_j, \qquad \frac{\partial J}{\partial (z_{l-1})_j} = (W_l^\top \delta^\ast_l)_j \, f_{l-1}'((z_{l-1})_j).$$

Line L8 computes exactly $(W_l^\top \delta) \odot f'_{l-1}(z_{l-1})$, and line L7 does not change $\delta$. By the hypothesis $\delta = \delta^\ast_l$, so at the start of round $l - 1$ the variable $\delta$ equals $\delta^\ast_{l-1}$. Line L8 reads $z_{l-1}$ and $W_l$, which no line of the backward loop writes, so they still hold the values of Step 1.

*Step 3: the outputs.* In round $l$, the parameters $W_l$ and $b_l$ enter $J$ only through $z_l$, and $(z_l)_i = \sum_j (W_l)_{ij} (a_{l-1})_j + (b_l)_i$. So $\partial (z_l)_i / \partial (W_l)_{ij} = (a_{l-1})_j$, $\partial (z_l)_i / \partial (b_l)_i = 1$, and no other coordinate of $z_l$ depends on $(W_l)_{ij}$ or $(b_l)_i$. The chain rule gives

$$\frac{\partial J}{\partial (W_l)_{ij}} = (\delta^\ast_l)_i (a_{l-1})_j, \qquad \frac{\partial J}{\partial (b_l)_i} = (\delta^\ast_l)_i,$$

that is, $\partial J / \partial W_l = \delta^\ast_l a_{l-1}^\top$ and $\partial J / \partial b_l = \delta^\ast_l$. By Step 2, line L7 computes these values. Each $G_l$ and $g_l$ is written once, in round $l$, and is not changed later.

*Step 4: termination.* The forward loop runs $L$ rounds and the backward loop runs $L$ rounds, each with a finite number of arithmetic operations on vectors and matrices of fixed size. So BACKPROP stops, and by Step 3 it returns $\nabla J$. $\blacksquare$

**Remark on a batch.** For the mean loss $\frac{1}{B} \sum_{s=1}^{B} \ell(a_L^{(s)}, y^{(s)})$ the gradient is the mean of the per-example gradients, by linearity of the derivative. In matrix form, with the examples as the columns of $A_{l-1}$ and $\Delta_l$, the batch gradient is $\frac{1}{B} \Delta_l A_{l-1}^\top$, and the recursion is $\Delta_{l-1} = (W_l^\top \Delta_l) \odot f'_{l-1}(Z_{l-1})$.
