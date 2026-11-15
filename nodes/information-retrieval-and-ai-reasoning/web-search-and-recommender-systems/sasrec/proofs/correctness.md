---
title: The causal mask keeps each SASRec output a function of the past, and the hand-written backward pass is the gradient of the loss
proves: [correctness]
status: full
---

The notation is that of the page, with one block and one head. For a sequence $s_0, \dots, s_{T-1}$ and row vectors of length $d$,

$$E_t = M[s_t] + P_t, \quad X_t = \mathrm{LN}_1(E_t), \quad Q_t = X_t W_Q, \; K_t = X_t W_K, \; V_t = X_t W_V,$$

$$z_{t,u} = Q_t \cdot K_u / \sqrt d, \quad A_{t,u} = \frac{e^{z_{t,u}}}{\sum_{w \le t} e^{z_{t,w}}} \; (u \le t), \quad S_t = E_t + \sum_{u \le t} A_{t,u} V_u,$$

$$Y_t = \mathrm{LN}_2(S_t), \quad H_t = \mathrm{ReLU}(Y_t W_1 + c_1), \quad F_t = S_t + H_t W_2 + c_2,$$

where $\mathrm{LN}(x) = \gamma \odot \hat x + \beta$ with $\hat x = (x - \mu)\, \rho$, $\mu$ the mean of the entries of $x$, $v$ their variance and $\rho = (v + \epsilon)^{-1/2}$. The loss with positives $i_t$ and negatives $j_t$ is

$$\mathcal L = \sum_t -\ln \sigma(F_t \cdot M[i_t]) - \ln\bigl(1 - \sigma(F_t \cdot M[j_t])\bigr).$$

**Proposition 1 (causality).** For every $t$, $F_t$ depends only on $s_0, \dots, s_t$ and the parameters. In floating point the same holds exactly: changing $s_{t'}$ for some $t' > t$ leaves the computed $F_t$ bit for bit the same.

*Proof.* $E_u$, $X_u$, $Q_u$, $K_u$, $V_u$ depend only on $s_u$ and position $u$. $S_t$ uses $E_t$ and $K_u, V_u$ for $u \le t$ only, because the sums run over $u \le t$; that is the mask, which the code implements by never forming $z_{t,u}$ for $u > t$, rather than by adding $-\infty$. $Y_t$, $H_t$ and $F_t$ are computed from $S_t$ alone, position by position. So the expression for $F_t$ contains only values from positions $0, \dots, t$. The code evaluates exactly this expression, with the same operations in the same order whatever the later items are, so the floating-point result is the same. $\square$

The test changes the item at each position $t'$ to every other item and checks that $F_u$ for $u < t'$ is equal as floats.

For the gradient, every function in the chain is differentiable except ReLU at 0; the claims are at points where no entry of $Y_t W_1 + c_1$ is 0, and at 0 the code uses the derivative 0. Write $\bar a$ for $\partial \mathcal L / \partial a$.

**Lemma 2 (the output).** With $\ell^+ = F_t \cdot M[i_t]$ and $\ell^- = F_t \cdot M[j_t]$, $\partial \mathcal L / \partial \ell^+ = \sigma(\ell^+) - 1$ and $\partial \mathcal L / \partial \ell^- = \sigma(\ell^-)$. So $\bar F_t = (\sigma(\ell^+) - 1) M[i_t] + \sigma(\ell^-) M[j_t]$, and the prediction layer adds $(\sigma(\ell^+) - 1) F_t$ to the gradient of row $M[i_t]$ and $\sigma(\ell^-) F_t$ to row $M[j_t]$.

*Proof.* $-\ln \sigma(x) = \ln(1 + e^{-x})$ has derivative $-\sigma(-x) = \sigma(x) - 1$, and $-\ln(1 - \sigma(x)) = \ln(1 + e^x)$ has derivative $\sigma(x)$. The dot products are bilinear. $\square$

**Lemma 3 (layer normalization).** If $y = \gamma \odot \hat x + \beta$ and $g = \bar y$, then $\bar \gamma = g \odot \hat x$, $\bar \beta = g$, and with $h = g \odot \gamma$,

$$\bar x = \rho \bigl(h - \mathrm{mean}(h) - \hat x\, \mathrm{mean}(h \odot \hat x)\bigr).$$

*Proof.* The gain and bias formulas follow from $y_c = \gamma_c \hat x_c + \beta_c$. For $\bar x$, $\partial \mu / \partial x_a = 1/d$ and $\partial v / \partial x_a = 2 (x_a - \mu)/d$ (the term from $\mu$ sums to 0, since $\sum_c (x_c - \mu) = 0$), so $\partial \rho / \partial x_a = -\tfrac12 \rho^3 \cdot 2 (x_a - \mu)/d = -\rho^2 \hat x_a / d$. Then

$$\frac{\partial \hat x_c}{\partial x_a} = \rho\Bigl([a = c] - \frac1d\Bigr) + (x_c - \mu) \frac{\partial \rho}{\partial x_a} = \rho\Bigl([a = c] - \frac1d - \frac{\hat x_c \hat x_a}{d}\Bigr),$$

and $\bar x_a = \sum_c h_c\, \partial \hat x_c / \partial x_a = \rho\bigl(h_a - \mathrm{mean}(h) - \hat x_a\, \mathrm{mean}(h \odot \hat x)\bigr)$. $\square$

**Lemma 4 (softmax attention).** Fix $t$ and let $o_t = \sum_{u \le t} A_{t,u} V_u$ with $\bar o_t$ known. Then $\bar V_u \mathrel{+}= A_{t,u} \bar o_t$, and with $\alpha_u = \bar o_t \cdot V_u$,

$$\bar z_{t,u} = A_{t,u} \Bigl(\alpha_u - \sum_{w \le t} A_{t,w} \alpha_w\Bigr), \qquad \bar Q_t \mathrel{+}= \sum_{u \le t} \bar z_{t,u} K_u / \sqrt d, \qquad \bar K_u \mathrel{+}= \bar z_{t,u} Q_t / \sqrt d.$$

*Proof.* $o_t$ is linear in each $V_u$ with coefficient $A_{t,u}$ and in each $A_{t,u}$ with coefficient $V_u$, so $\bar A_{t,u} = \alpha_u$. The softmax has $\partial A_{t,w} / \partial z_{t,u} = A_{t,w}([w = u] - A_{t,u})$, so $\bar z_{t,u} = \sum_w \alpha_w A_{t,w} ([w = u] - A_{t,u})$, which is the stated form. $z_{t,u}$ is bilinear in $Q_t$ and $K_u$ with the factor $1/\sqrt d$. $\square$

**Theorem 5 (the backward pass is the gradient).** `loss_and_grad` returns $\mathcal L$ and $\partial \mathcal L / \partial \theta$ for every parameter $\theta$.

*Proof.* The code goes through the forward graph in reverse.

1. Lemma 2 gives $\bar F_t$ and the prediction-layer part of $\bar M$.
2. $F_t = S_t + H_t W_2 + c_2$ gives $\bar c_2 \mathrel{+}= \bar F_t$, $\bar W_2 \mathrel{+}= H_t^\top \bar F_t$, and $\bar H_t = \bar F_t W_2^\top$. The ReLU passes $\bar H_t$ where the pre-activation is positive, which gives $\bar c_1$, $\bar W_1 \mathrel{+}= Y_t^\top \bar P_t$ for that masked gradient $\bar P_t$, and $\bar Y_t = \bar P_t W_1^\top$. Lemma 3 turns $\bar Y_t$ into the gain and bias gradients of $\mathrm{LN}_2$ and a gradient in $S_t$.
3. $S_t$ reaches the loss through $F_t$ directly (the residual) and through $\mathrm{LN}_2$, and through nothing else, so $\bar S_t$ is the sum of $\bar F_t$ and the result of step 2. It is complete at this point.
4. $S_t = E_t + o_t$, so $\bar o_t = \bar S_t$ and $\bar E_t$ gets $\bar S_t$ from the residual. Lemma 4 for each $t$ adds the contributions to $\bar Q_t$, $\bar K_u$ and $\bar V_u$ for all $u \le t$. After all $t$ these sums are complete, since $K_u$ and $V_u$ reach the loss only through the $o_t$ with $t \ge u$.
5. $Q_t = X_t W_Q$ and the same for $K$ and $V$ give $\bar W_Q \mathrel{+}= X_t^\top \bar Q_t$ and the like, and $\bar X_t = \bar Q_t W_Q^\top + \bar K_t W_K^\top + \bar V_t W_V^\top$. Lemma 3 turns $\bar X_t$ into the $\mathrm{LN}_1$ gradients and a gradient in $E_t$, which is added to the residual part of step 4.
6. $E_t = M[s_t] + P_t$ adds $\bar E_t$ to the gradient of row $M[s_t]$ and of row $P_t$.

Each step is the chain rule for one node of the graph, applied after all the nodes that use its output, so every adjoint is complete when it is used. Each parameter that appears in several places ($M$ as input and output embedding, the shared weights at every position) gets the sum of its contributions, which is the derivative of a sum. $\square$

The tests compare every entry of this gradient with a central finite difference at two random points with gains and biases away from 1 and 0.

**A training step.** One step of `train` takes the exact gradient of the loss of one sequence, with one negative drawn per step from the items not in the sequence, and moves all parameters against it. The page uses plain gradient steps where the paper uses Adam. This page does not prove that the steps converge, or that the model ranks well; that is measured. $\blacksquare$
