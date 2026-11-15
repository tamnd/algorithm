---
title: The BPR step follows an unbiased estimate of the gradient of the mean triple loss, and the criterion bounds the AUC from below
proves: [correctness]
status: full
---

The notation is that of the page. $S$ is the set of positive pairs, $I_u^+ = \{i : (u, i) \in S\}$, and $D_S = \{(u, i, j) : i \in I_u^+, j \notin I_u^+\}$. The model is $x_{ui} = w_u^\top h_i$ and $x_{uij} = x_{ui} - x_{uj}$. The loss of one triple is

$$\ell(u, i, j) = -\ln \sigma(x_{uij}) + \tfrac12 \bigl(\lambda_W \lVert w_u \rVert^2 + \lambda_{H^+} \lVert h_i \rVert^2 + \lambda_{H^-} \lVert h_j \rVert^2\bigr),$$

and the code minimizes $L = \frac{1}{|D_S|} \sum_{(u,i,j) \in D_S} \ell(u, i, j)$, the mean over $D_S$. The sum of $\ln \sigma(x_{uij})$ over $D_S$ minus the penalty of each triple, which is the version of BPR-Opt that the updates of LearnBPR follow, equals $-|D_S| L$, so maximizing it and minimizing $L$ are the same problem. What can be proved is that each step of the algorithm is a correct stochastic gradient step for $L$, and what $L$ says about the AUC. Whether the learned ranking is good on real data is measured, not proved.

**Lemma 1 (the gradient).** Let $e = \sigma(-x_{uij})$ and $i \ne j$. Then

$$\frac{\partial \ell}{\partial w_u} = -e\,(h_i - h_j) + \lambda_W w_u, \qquad \frac{\partial \ell}{\partial h_i} = -e\, w_u + \lambda_{H^+} h_i, \qquad \frac{\partial \ell}{\partial h_j} = e\, w_u + \lambda_{H^-} h_j,$$

and $\ell$ does not depend on any other parameter.

*Proof.* $\frac{d}{dz} \ln \sigma(z) = \frac{\sigma'(z)}{\sigma(z)} = \frac{\sigma(z)(1 - \sigma(z))}{\sigma(z)} = 1 - \sigma(z) = \sigma(-z)$. By the chain rule, $\partial(-\ln \sigma(x_{uij}))/\partial \theta = -\sigma(-x_{uij})\, \partial x_{uij} / \partial \theta$. Since $x_{uij} = w_u^\top h_i - w_u^\top h_j$, the partial derivatives of $x_{uij}$ are $h_i - h_j$ for $w_u$, $w_u$ for $h_i$ and $-w_u$ for $h_j$, as in Section 4.3.1 of Rendle et al. The penalty $\frac12 \lambda \lVert v \rVert^2$ has gradient $\lambda v$. Only $w_u$, $h_i$ and $h_j$ appear in $\ell(u, i, j)$. $\square$

The update printed in Figure 4 of the paper reads $\Theta \leftarrow \Theta + \alpha \bigl(\frac{e^{-x}}{1 + e^{-x}} \frac{\partial x}{\partial \Theta} + \lambda \Theta\bigr)$. Lemma 1 shows that an ascent step on $\ln \sigma(x) - \frac12 \lambda \lVert \Theta \rVert^2$ has $-\lambda \Theta$ in that place, and $\frac{e^{-x}}{1 + e^{-x}} = \sigma(-x) = e$. Line L6 of the page uses the sign of Lemma 1.

**Lemma 2 (the sampler is uniform on $D_S$).** Lines L3 and L4 draw $(u, i)$ uniformly from $S$ and $j$ uniformly from the $n$ items, and draw again until $j \notin I_u^+$. The accepted triple is uniform on $D_S$.

*Proof.* One attempt produces a fixed triple $(u, i, j) \in D_S$ with probability $\frac{1}{|S|} \cdot \frac{1}{n}$, the same for every triple of $D_S$, and produces a triple outside $D_S$ otherwise. The attempts are independent, so the first accepted triple is distributed as one attempt conditioned on acceptance, which gives each triple of $D_S$ the probability $\frac{1 / (|S| n)}{|D_S| / (|S| n)} = \frac{1}{|D_S|}$. $\square$

Drawing $j$ uniformly from the unused items of the drawn user instead would give the triple the probability $\frac{1}{|S| (n - |I_u^+|)}$, which favors users with many positive items; the expectation in Theorem 3 would then be a weighted mean, not $L$.

**Theorem 3 (unbiased step).** Let $g$ be the vector that lines L5 and L6 subtract from the parameters, divided by the step size, with zeros for all parameters other than $w_u$, $h_i$ and $h_j$. Then $\mathbb{E}[g] = \nabla L$, where the expectation is over the triple drawn in this step, with the parameters fixed.

*Proof.* By Lemma 1, $g = \nabla \ell(u, i, j)$ as a vector over all parameters. By Lemma 2 the triple is uniform on $D_S$, so $\mathbb{E}[g] = \frac{1}{|D_S|} \sum_{D_S} \nabla \ell(u, i, j) = \nabla L$, by the linearity of the gradient. $\square$

**Proposition 4 (the criterion bounds the AUC).** For a user $u$ with $I_u^+$ and its complement both nonempty, let $D_u$ be the triples of $D_S$ with first entry $u$ and

$$\mathrm{AUC}(u) = \frac{1}{|D_u|} \sum_{(u,i,j) \in D_u} \delta(x_{uij} > 0).$$

Then $\mathrm{AUC}(u) \ge 1 + \frac{1}{\ln 2} \cdot \frac{1}{|D_u|} \sum_{(u, i, j) \in D_u} \ln \sigma(x_{uij})$.

*Proof.* It is enough to show $\delta(x > 0) \ge 1 + \log_2 \sigma(x)$ for every real $x$ and to average. If $x > 0$, the left side is 1 and $\log_2 \sigma(x) < 0$, so the right side is below 1. If $x \le 0$, the left side is 0, and $\sigma(x) \le \frac12$ gives $\log_2 \sigma(x) \le -1$, so the right side is at most 0. $\square$

So a larger mean of $\ln \sigma(x_{uij})$ forces a larger lower bound on the training AUC. This makes precise the remark of Section 4.1.1 of the paper that BPR-Opt is a smooth version of the AUC, with $\ln \sigma$ in place of the step function $\delta(x > 0)$. The bound is about the triples used in training; the AUC on held-out pairs is a measurement.

**Cost.** Lines L3 and L4 take $O(1)$ expected attempts when the users use at most a constant fraction of the items, since an attempt succeeds with probability $|D_S| / (|S| n)$, the mean fraction of unused items weighted by the number of positives. Lemma 1 costs $O(r)$, and so does line L6, so one step costs $O(r)$ expected time.

**What is not claimed.** $L$ is not convex in $(W, H)$, since $x_{uij}$ is a product of parameters. Theorem 3 is the property that the standard analysis of [stochastic gradient descent](/stochastic-gradient-descent/) assumes, but this page does not prove that LearnBPR converges, or that it reaches a global minimum. $\blacksquare$
