---
title: The hand-written backward pass of NeuMF is the gradient of the log loss, and matrix factorization is a special case of the model
proves: [correctness]
status: full
---

The notation is that of the page. For one example $(u, i, y)$ with $y \in \{0, 1\}$, the forward pass computes

$$g = p_u^G \odot q_i^G, \quad z_0 = [p_u^M; q_i^M], \quad a_l = W_l z_{l-1} + b_l, \quad z_l = \mathrm{ReLU}(a_l) \; (l = 1, \dots, L), \quad \varphi = [g; z_L], \quad s = h^\top \varphi,$$

and the loss is $\ell = -y \ln \sigma(s) - (1 - y) \ln(1 - \sigma(s))$. The claims are about exact arithmetic and about points where no entry of any $a_l$ is 0; at such a point every function in the chain is differentiable. At an entry $a_l = 0$ the code uses the derivative 0 for ReLU, which is one element of its subdifferential.

**Lemma 1 (the output).** $\partial \ell / \partial s = \sigma(s) - y$.

*Proof.* $1 - \sigma(s) = \sigma(-s)$, so $\ell = y \ln(1 + e^{-s}) + (1 - y) \ln(1 + e^{s})$. The derivative of $\ln(1 + e^{-s})$ is $-\sigma(-s) = \sigma(s) - 1$ and that of $\ln(1 + e^{s})$ is $\sigma(s)$. So $\partial \ell / \partial s = y (\sigma(s) - 1) + (1 - y) \sigma(s) = \sigma(s) - y$. $\square$

Write $\delta = \sigma(s) - y$.

**Lemma 2 (the top layer and the GMF part).** $\partial \ell / \partial h = \delta\, \varphi$ and $\partial \ell / \partial \varphi = \delta\, h$. With $h = [h^G; h^M]$ split like $\varphi$, $\partial \ell / \partial g = \delta h^G$, and

$$\frac{\partial \ell}{\partial p_u^G} = \delta\, h^G \odot q_i^G, \qquad \frac{\partial \ell}{\partial q_i^G} = \delta\, h^G \odot p_u^G.$$

*Proof.* $s = h^\top \varphi$ is bilinear, so its partial derivatives are $\varphi$ and $h$; multiply by $\delta$ (chain rule). Entry $c$ of $g$ is $p_{uc}^G q_{ic}^G$, which depends only on entry $c$ of each vector, with partial derivatives $q_{ic}^G$ and $p_{uc}^G$. $\square$

**Lemma 3 (one ReLU layer).** Let $d_l = \partial \ell / \partial z_l$ be known. Then, with $D_l$ the diagonal matrix with entries $1$ where $a_l > 0$ and $0$ where $a_l < 0$,

$$\frac{\partial \ell}{\partial a_l} = D_l d_l, \qquad \frac{\partial \ell}{\partial W_l} = (D_l d_l) z_{l-1}^\top, \qquad \frac{\partial \ell}{\partial b_l} = D_l d_l, \qquad d_{l-1} = W_l^\top D_l d_l.$$

*Proof.* $z_l = \mathrm{ReLU}(a_l)$ acts entry by entry with derivative 1 or 0 away from 0, which gives the first formula. Entry $r$ of $a_l$ is $\sum_c W_{l, rc} z_{l-1, c} + b_{l, r}$, so $\partial a_{l, r} / \partial W_{l, rc} = z_{l-1, c}$, $\partial a_{l, r} / \partial b_{l, r} = 1$, and $\partial a_{l, r} / \partial z_{l-1, c} = W_{l, rc}$; no other entry of $a_l$ depends on $W_{l, rc}$ or $b_{l, r}$. The chain rule gives the three formulas. $\square$

**Theorem 4 (the backward pass is the gradient).** The function `backward` adds to its buffers exactly $\partial \ell / \partial \theta$ for every parameter $\theta$: the entries of $h$, $W_l$, $b_l$, of the rows $p_u^G, q_i^G, p_u^M, q_i^M$, and zero for every other row of the embedding tables.

*Proof.* `backward` receives $\delta$ (Lemma 1) and computes the derivatives of Lemma 2. It sets $d_L = \delta h^M$ and applies Lemma 3 for $l = L, L - 1, \dots, 1$, which is induction on the layers from the top: each step uses $d_l$, correct by the previous step, and produces $d_{l-1}$. At the end $d_0 = \partial \ell / \partial z_0$, and since $z_0 = [p_u^M; q_i^M]$ is a concatenation, its first half is $\partial \ell / \partial p_u^M$ and its second half is $\partial \ell / \partial q_i^M$. The other rows of the tables do not appear in the forward pass of $(u, i)$, so their derivative is 0. For a set of examples the loss is a sum, and `gradient` adds the per-example gradients. $\square$

The tests compare every entry of this gradient with a central finite difference on a model with two hidden layers, one hidden layer, and no hidden layer.

**Proposition 5 (matrix factorization is a special case).** If $h^G = \mathbf{1}$ and $h^M = 0$, then $s = (p_u^G)^\top q_i^G$, the score of [matrix factorization](/matrix-factorization-recommendation/). If only $h^M = 0$, then $s = \sum_c h^G_c\, p_{uc}^G q_{ic}^G$, the GMF model of He et al.

*Proof.* $s = h^{G\top} (p_u^G \odot q_i^G) + h^{M\top} z_L$, and with $h^M = 0$ the second term vanishes; with $h^G = \mathbf{1}$ the first term is $\sum_c p_{uc}^G q_{ic}^G$. $\square$

So the set of score functions of NeuMF contains those of matrix factorization. This does not imply that training NeuMF finds a better score function than training matrix factorization does: the training problem is not convex, the larger model has more parameters to fit from the same data, and the comparison is an empirical question.

**A training step.** One step of `train` computes the gradient of the loss of one example by Theorem 4 and moves the parameters that the example uses against it. For an example drawn uniformly from the examples of an epoch, the expected gradient at fixed parameters is the gradient of the mean loss over those examples, by the linearity of the gradient. This page does not prove that the steps converge, or that they reach a good minimum. $\blacksquare$
