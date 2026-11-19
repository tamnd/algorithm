---
title: The scaled denominator recursion and the log-space numerator recursion give the LF-MMI objective and its exact gradient
proves: [correctness]
status: full
---

We use the notation of the page. A graph has emitting states $j$ with pdf ids $\mathrm{pdf}(j)$, arcs $i \to j$ with probabilities $w(i, j)$, initial probabilities $\mathrm{init}(j)$ and final probabilities $\mathrm{final}(j)$. The frames are $t = 1, \ldots, T$, the network outputs are $y_t(p)$, and $\eta \ge 0$ is the leaky coefficient. Write $e_t(j) = e^{y_t(\mathrm{pdf}(j)) - m_t}$ with $m_t = \max_p y_t(p)$.

**The leaky graph.** Let $w_\eta(i, j) = w(i, j) + \eta\, \mathrm{init}(j)$, the weight of the denominator graph with an extra arc from every state $i$ to every state $j$ of probability $\eta\, \mathrm{init}(j)$. For a graph with weights $w_\eta$, a path $q_1 \ldots q_T$ has the weight

$$\mathrm{init}(q_1) \prod_{t=2}^{T} w_\eta(q_{t-1}, q_t)\, \mathrm{final}(q_T) \prod_{t=1}^{T} e^{y_t(\mathrm{pdf}(q_t))},$$

and $Z$ is the sum of these weights. This is the $Z$ of the page; for $\eta = 0$ it is the plain graph.

**Lemma 1 (the scaled forward pass).** Let $\alpha_t(j)$ be the sum of the weights of the partial paths $q_1 \ldots q_t$ with $q_t = j$, without the final factor. Lines L3 and L4 give $c_t > 0$ and $\hat\alpha_t$ with

$$\alpha_t(j) = \hat\alpha_t(j) \prod_{s=1}^{t} c_s e^{m_s}, \qquad \sum_j \hat\alpha_t(j) = 1.$$

*Proof.* By induction on $t$. At $t = 1$, line L3 computes $a(j) = \mathrm{init}(j) e_1(j) = \alpha_1(j) e^{-m_1}$, and line L4 divides by $c_1 = \sum_j a(j)$. For $t \ge 2$, a partial path that ends in $j$ is a partial path that ends in some $i$ followed by an arc $i \to j$, so by distributivity

$$\alpha_t(j) = \Big( \sum_{i \to j} \alpha_{t-1}(i) w(i, j) + \eta\, \mathrm{init}(j) \sum_i \alpha_{t-1}(i) \Big) e_t(j) e^{m_t}.$$

Put in the induction hypothesis: the factor $\prod_{s < t} c_s e^{m_s}$ comes out of the bracket, and what is left is the value $a(j)$ of line L3, computed from $\hat\alpha_{t-1}$. Line L4 divides by $c_t = \sum_j a(j)$. If $c_t = 0$, no partial path has positive weight, and the code raises an error. $\square$

**Corollary 1.** $\ln Z = \sum_t (\ln c_t + m_t) + \ln \sum_j \hat\alpha_T(j)\, \mathrm{final}(j)$, which is line L5. This follows from Lemma 1 at $t = T$ and the definition of $Z$. The code never forms a product of $T$ probabilities, so the value does not underflow for long chunks: each $c_t$ is a sum of $\sum_j \hat\alpha_{t-1}(j) = 1$ times weights and outputs of one frame only.

**Lemma 2 (the scaled backward pass).** Let $\beta_t(i)$ be the sum, over the suffixes $q_{t+1} \ldots q_T$ after $q_t = i$, of $\prod_{\tau > t} w_\eta(q_{\tau-1}, q_\tau) e^{y_\tau(\mathrm{pdf}(q_\tau))}$ times $\mathrm{final}(q_T)$. Line L6 gives $\hat\beta_t$ with $\beta_t(i) = \hat\beta_t(i) \prod_{s > t} c_s e^{m_s}$.

*Proof.* By induction downwards. At $t = T$, $\hat\beta_T = \mathrm{final} = \beta_T$ and the product is empty. For $t < T$, $\beta_t(i) = \sum_j w_\eta(i, j) e_{t+1}(j) e^{m_{t+1}} \beta_{t+1}(j)$, and $\sum_j \eta\, \mathrm{init}(j) e_{t+1}(j) \hat\beta_{t+1}(j)$ is the same for every $i$, which is the term leak of the code. Dividing by $c_{t+1}$ as in line L6 keeps the stated relation. $\square$

**Lemma 3 (posteriors).** $\gamma^{\mathrm{den}}_t(p)$ of line L7 is the posterior probability, under the distribution on the paths in proportion to their weights, that the path is in a state of pdf $p$ at frame $t$.

*Proof.* The weight of the paths with $q_t = j$ is $\alpha_t(j) \beta_t(j)$. By Lemmas 1 and 2 this is $\hat\alpha_t(j) \hat\beta_t(j) \prod_{s=1}^{T} c_s e^{m_s}$, and by Corollary 1, $Z = \prod_s c_s e^{m_s} \sum_j \hat\alpha_T(j) \mathrm{final}(j)$. The common product cancels. $\square$

**The numerator.** Line L1 runs the log-space forward-backward on the numerator graph, with $y_t(\mathrm{pdf}(j))$ replaced by $-\infty$ at the frames outside the window of state $j$. The same argument as in Lemmas 1 to 3, with log_add for $+$ (see the proof on the [MMI page](/maximum-mutual-information-training/)), gives $\ln Z_{\mathrm{num}}$ as the log of the weight of the paths that respect the windows, and $\gamma^{\mathrm{num}}$ as their posteriors.

**Theorem.** Line L8 returns

$$F = \ln Z_{\mathrm{num}} - \ln Z_{\mathrm{den}} - \frac{c}{2} \sum_{t,p} y_t(p)^2, \qquad \frac{\partial F}{\partial y_t(p)} = \gamma^{\mathrm{num}}_t(p) - \gamma^{\mathrm{den}}_t(p) - c\, y_t(p).$$

*Proof.* The value follows from the numerator paragraph and Corollary 1. In both graphs, the log weight of a path depends on $y_t(p)$ only by the term $y_t(\mathrm{pdf}(q_t))$, with coefficient 1 if $\mathrm{pdf}(q_t) = p$ and 0 otherwise; the arc weights, including the leaky arcs, do not depend on $y$. So $\partial \ln Z / \partial y_t(p)$ is the expected value of that coefficient, which is the posterior of Lemma 3 (or of the numerator paragraph). The derivative of the penalty is $c\, y_t(p)$. $\square$

**Corollary 2.** If the numerator weights are the weights of the same states and arcs of the denominator (as in the code), every numerator path that respects the windows is a denominator path with the same weight, and a positive $\eta$ only adds paths to the denominator. So $Z_{\mathrm{num}} \le Z_{\mathrm{den}}$, and with $c = 0$, $F \le 0$. For each frame, $\sum_p \partial F / \partial y_t(p) = -c \sum_p y_t(p)$, since both posteriors sum to 1.
