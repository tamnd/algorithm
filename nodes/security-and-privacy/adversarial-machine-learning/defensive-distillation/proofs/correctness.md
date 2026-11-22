---
title: Distillation of a linear model only scales its logits, so boundaries stay and gradients vanish
proves: [correctness]
status: full
---

The models are softmax regressions, $z(u) = Wu + b$ with $W \in \mathbb{R}^{K \times d}$, trained from zero by full-batch gradient descent on the mean tempered loss $\frac1n \sum_i H(q^i, \operatorname{softmax}(z(x^i)/T))$, where $H(q, p) = -\sum_k q_k \ln p_k$ (the function `train_softmax`). We compare a run at temperature $T$ with step size $T^2 \eta$ to a run at temperature $1$ with step size $\eta$, on the same data and the same targets.

**Lemma 1 (the gradient in the logits).** $\partial H(q, \operatorname{softmax}(z/T)) / \partial z = (\operatorname{softmax}(z/T) - q)/T$.

*Proof.* With $s = z/T$, the loss is $\ln \sum_k e^{s_k} - \sum_k q_k s_k$ because $\sum_k q_k = 1$. Its gradient in $s$ is $\operatorname{softmax}(s) - q$, and $\partial s / \partial z = 1/T$. $\square$

**Theorem 1 (temperature scaling).** Let $(W^{(1)}_t, b^{(1)}_t)$ be the weights after $t$ steps at temperature $1$ with step size $\eta$, and $(W^{(T)}_t, b^{(T)}_t)$ the weights after $t$ steps at temperature $T > 0$ with step size $T^2 \eta$, both on targets $q^i$. Then $W^{(T)}_t = T\, W^{(1)}_t$ and $b^{(T)}_t = T\, b^{(1)}_t$ for every $t$.

*Proof.* By induction on $t$. Both runs start at zero. Suppose the claim holds at $t$. Then $z^{(T)}(x^i) = T z^{(1)}(x^i)$, so $\operatorname{softmax}(z^{(T)}/T) = \operatorname{softmax}(z^{(1)})$, and by Lemma 1 the logit gradient of each sample in the run at $T$ is $1/T$ times the one in the run at $1$. The weight gradients are these logit gradients times $x^i$ (or times $1$ for $b$), averaged, so they are also $1/T$ times the gradients of the run at $1$. The step gives $W^{(T)}_{t+1} = T W^{(1)}_t - T^2\eta \cdot \tfrac1T G = T(W^{(1)}_t - \eta G) = T W^{(1)}_{t+1}$, where $G$ is the gradient of the run at $1$, and the same for $b$. $\square$

**Corollary 1 (the whole procedure).** Run `defensive_distillation` at temperature $T$ with step size $T^2 \eta$, and again at temperature $1$ with step size $\eta$. Then the student of the first run has logits $T$ times the logits of the student of the second run, at every input.

*Proof.* The teachers (line L2) are trained on the same hard labels, so by Theorem 1 the teacher at $T$ is $T$ times the teacher at $1$. The soft labels of line L3 are $\operatorname{softmax}(T z^{(1)}(x^i)/T) = \operatorname{softmax}(z^{(1)}(x^i))$ in the first run and the same in the second run. So the students (line L4) are trained on the same targets, and Theorem 1 applies again. $\square$

**Corollary 2 (no change in the boundaries).** The distilled student and the student trained at $T = 1$ give the same label to every input, have the same decision boundaries $\{u : z_i(u) = z_j(u)\}$, and give every input the same $\ell_2$ distance to the nearest boundary.

*Proof.* Multiplying all logits by $T > 0$ keeps their order and their sets of ties. The distance from $u$ to the boundary between $i$ and $j$ is $|z_i(u) - z_j(u)| / \lVert w_i - w_j \rVert_2$, and the factor $T$ cancels. $\square$

So a minimum-distance attack on the distilled model has the same optimum as on the model trained at $T = 1$. The defense does not move the boundary.

**Corollary 3 (the softmax gradient vanishes).** Let the student be used at temperature $1$, with logits $Z = T z$ where $z$ are the logits of the student trained at $T = 1$. Let $u$ have label $y$ with margin $\mu = z_y(u) - \max_{j \ne y} z_j(u) > 0$. Then the input gradient of the cross-entropy at the student satisfies $\lVert \nabla_u H(e_y, \operatorname{softmax}(Z(u))) \rVert_2 \le 2 (K - 1)\, T\, e^{-T\mu} \max_k \lVert w_k \rVert_2$, where $w_k$ are the rows of the student trained at $T=1$.

*Proof.* With $P = \operatorname{softmax}(Z)$, the gradient is $\sum_k (P_k - [k = y])\, T w_k$. The coefficients satisfy $\sum_k |P_k - [k = y]| = 2(1 - P_y)$. And $1 - P_y = \sum_{j \ne y} P_j \le \sum_{j \ne y} e^{Z_j - Z_y} \le (K - 1) e^{-T\mu}$, because $P_j / P_y = e^{Z_j - Z_y}$ and $P_y \le 1$. $\blacksquare$

The bound goes to $0$ fast as $T$ grows. In floating point, $P_y$ rounds to exactly $1$ when $T\mu$ is large, and the gradient that FGSM and PGD use is then exactly $0$. This is gradient masking: the attack loses its signal, but the model is not more robust. An attack on the logits $Z$ (as in the C&W attack) or on $Z/T$ sees the gradient $T w_k$, which does not vanish.

**What is not claimed.** The exact scaling needs the step size $T^2\eta$, linear models and full-batch gradient descent. For deep networks and other step sizes, Carlini and Wagner explain the effect of distillation in the same way, as logits that grow with $T$; that is an observation on those networks, not a theorem here.
