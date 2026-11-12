---
title: The bootstrap filter gives an unbiased likelihood estimate and estimates with error O(1/sqrt N)
proves: [correctness]
status: full
---

**Setting.** The model is $x_0 \sim \mu$, $x_t \mid x_{t-1} \sim M_t(x_{t-1}, \cdot)$ and $y_t \mid x_t$ with density $g_t(y_t \mid x_t)$. The observations are fixed, so write $G_t(x) = g_t(y_t \mid x)$ and assume $0 \le G_t \le \|G_t\| < \infty$. For a bounded function $\varphi$ write $M_t \varphi(x) = \int \varphi(x') M_t(x, dx')$, and for a measure $\nu$ write $\nu(\varphi) = \int \varphi \, d\nu$.

The targets are the predictive law $\eta_t = $ law of $x_t$ given $y_{1:t-1}$, the filter $\pi_t = $ law of $x_t$ given $y_{1:t}$, and the likelihood $Z_T = p(y_{1:T})$. They satisfy $\eta_1 = \mu M_1$, $\pi_t(\varphi) = \eta_t(G_t \varphi) / \eta_t(G_t)$, $\eta_{t+1} = \pi_t M_{t+1}$, and $Z_T = \prod_{t=1}^T \eta_t(G_t)$, because $\eta_t(G_t) = p(y_t \mid y_{1:t-1})$. Assume $\eta_t(G_t) > 0$ for each $t$.

**The algorithm in this notation.** Let $\eta^N_t = \frac1N \sum_i \delta_{x^i_t}$ be the particles after line L4 at time $t$. Line L7 forms $\pi^N_t(\varphi) = \eta^N_t(G_t \varphi) / \eta^N_t(G_t)$, with any value in $[-\|\varphi\|, \|\varphi\|]$ when the denominator is $0$. Line L6 builds $\hat Z_T = \prod_{t=1}^T \eta^N_t(G_t)$. At time $t + 1$, lines L3 and L4 draw $N$ new particles independently, each from the mixture $\sum_i W^i_t M_{t+1}(x^i_t, \cdot) = \pi^N_t M_{t+1}$. So, with $\mathcal F_t$ the history up to the end of step $t$,

$$\mathbb E\bigl[\eta^N_{t+1}(\varphi) \mid \mathcal F_t\bigr] = \pi^N_t(M_{t+1} \varphi), \qquad \mathrm{Var}\bigl[\eta^N_{t+1}(\varphi) \mid \mathcal F_t\bigr] \le \frac{\|\varphi\|^2}{N}. \tag{1}$$

The variance bound holds because $\eta^N_{t+1}(\varphi)$ is the mean of $N$ conditionally independent values, each in $[-\|\varphi\|, \|\varphi\|]$. At $t = 1$ the particles are independent draws from $\mu M_1 = \eta_1$, so (1) holds with $\pi^N_0 M_1$ replaced by $\eta_1$.

**Theorem 1 (unbiased likelihood; Del Moral 2004).** $\mathbb E[\hat Z_T] = Z_T$.

*Proof.* Define the unnormalized measures $\gamma_t(\varphi) = \bigl[\prod_{s<t} \eta_s(G_s)\bigr]\, \eta_t(G_t \varphi)$ and their particle versions $\gamma^N_t(\varphi) = \bigl[\prod_{s<t} \eta^N_s(G_s)\bigr]\, \eta^N_t(G_t \varphi)$. Then $\gamma_T(1) = Z_T$ and $\gamma^N_T(1) = \hat Z_T$. We show $\mathbb E[\gamma^N_t(\varphi)] = \gamma_t(\varphi)$ for every bounded $\varphi \ge 0$ and every $t$, by induction.

For $t = 1$, $\mathbb E[\eta^N_1(G_1 \varphi)] = \eta_1(G_1 \varphi)$ because the particles are draws from $\eta_1$.

For the step from $t$ to $t + 1$, the product $\prod_{s \le t} \eta^N_s(G_s)$ is known given $\mathcal F_t$. By (1),
$$\mathbb E\bigl[\gamma^N_{t+1}(\varphi) \mid \mathcal F_t\bigr] = \Bigl[\prod_{s \le t} \eta^N_s(G_s)\Bigr] \frac{\eta^N_t(G_t \, M_{t+1}(G_{t+1}\varphi))}{\eta^N_t(G_t)} = \gamma^N_t\bigl(M_{t+1}(G_{t+1}\varphi)\bigr).$$
The factor $\eta^N_t(G_t)$ cancels; if it is $0$, both sides are $0$. The same algebra on the exact quantities, with $\eta_{t+1} = \pi_t M_{t+1}$, gives $\gamma_{t+1}(\varphi) = \gamma_t(M_{t+1}(G_{t+1}\varphi))$. Take expectations and use the induction hypothesis with the bounded function $M_{t+1}(G_{t+1}\varphi)$. $\square$

The proof needs only that each resampling step is unbiased, $\mathbb E[N_i \mid W] = N W_i$, and that the new particles are drawn conditionally independently; multinomial resampling has both properties. By [Jensen's inequality](/jensens-inequality/), $\mathbb E[\log \hat Z_T] \le \log Z_T$, so the log of the estimate is biased down.

**Theorem 2 (mean squared error).** For each $t$ there are constants $c_t$ and $c'_t$, independent of $N$ and $\varphi$, such that for every bounded $\varphi$
$$\mathbb E\bigl[(\eta^N_t(\varphi) - \eta_t(\varphi))^2\bigr]^{1/2} \le \frac{c'_t \|\varphi\|}{\sqrt N}, \qquad \mathbb E\bigl[(\pi^N_t(\varphi) - \pi_t(\varphi))^2\bigr]^{1/2} \le \frac{c_t \|\varphi\|}{\sqrt N}.$$

*Proof.* Write $\|Y\|_2 = \mathbb E[Y^2]^{1/2}$, which obeys the triangle inequality.

Prediction. For $t = 1$, $c'_1 = 1$ by the variance of a mean of independent draws. For $t + 1$,
$$\eta^N_{t+1}(\varphi) - \eta_{t+1}(\varphi) = \bigl(\eta^N_{t+1}(\varphi) - \pi^N_t(M_{t+1}\varphi)\bigr) + \bigl(\pi^N_t(M_{t+1}\varphi) - \pi_t(M_{t+1}\varphi)\bigr).$$
The first term has $\|\cdot\|_2 \le \|\varphi\|/\sqrt N$ by (1). The second has $\|\cdot\|_2 \le c_t \|\varphi\| / \sqrt N$ by the induction hypothesis, since $\|M_{t+1}\varphi\| \le \|\varphi\|$. So $c'_{t+1} = 1 + c_t$.

Update. Using $\pi^N_t(\varphi)\, \eta^N_t(G_t) = \eta^N_t(G_t \varphi)$, a direct computation gives
$$\pi^N_t(\varphi) - \pi_t(\varphi) = \frac{\eta^N_t(G_t\varphi) - \eta_t(G_t\varphi)}{\eta_t(G_t)} + \pi^N_t(\varphi)\, \frac{\eta_t(G_t) - \eta^N_t(G_t)}{\eta_t(G_t)}.$$
The denominators are the fixed numbers $\eta_t(G_t)$, and $|\pi^N_t(\varphi)| \le \|\varphi\|$. By the prediction bound applied to $G_t\varphi$ and to $G_t$, $\|\pi^N_t(\varphi) - \pi_t(\varphi)\|_2 \le 2 c'_t \|G_t\| \|\varphi\| / (\eta_t(G_t) \sqrt N)$. So $c_t = 2 c'_t \|G_t\| / \eta_t(G_t)$. $\square$

The constants grow with $t$ in this proof. Under mixing conditions on $M_t$ they can be made independent of $t$ (Del Moral 2004), which is why the filter works over long runs in practice, while the likelihood estimate has a relative variance that grows with $T$ for fixed $N$.

**Cost.** Each step draws $N$ transitions and evaluates $N$ likelihoods, and multinomial resampling with a binary search over the cumulative weights costs $O(N \log N)$. The total is $O(T N \log N)$ time plus $T N$ evaluations of the model, and $O(N)$ memory.
