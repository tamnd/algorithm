---
title: Selection combining outputs the best branch, and for independent Rayleigh branches its outage, mean SNR and BPSK error rate have closed forms
proves: [correctness]
status: full
---

Branch $l = 1, \ldots, L$ receives $y_l = h_l x + w_l$ with $E|x|^2 = E_s$ and $w_l \sim CN(0, N_{0,l})$, independent of each other and of $x$. The gains are known and not all zero. Write $\gamma_l = |h_l|^2 E_s/N_{0,l}$.

**Lemma 1 (the output).** Let $k$ be the branch chosen in line L2. Then $\hat x = x + n$ with $n \sim CN(0, N_{0,k}/|h_k|^2)$, so the output SNR is $\gamma_k = \max_l \gamma_l$. With no noise, $\hat x = x$.

*Proof.* Line L2 picks $k$ with the largest $|h_l|^2/N_{0,l}$, hence the largest $\gamma_l$, and $h_k \ne 0$ because not all gains are zero. Line L3 gives $\hat x = \overline{h_k}(h_k x + w_k)/|h_k|^2 = x + \overline{h_k} w_k/|h_k|^2$, and the noise term is circular Gaussian with variance $|h_k|^2 N_{0,k}/|h_k|^4$. $\square$

No receiver that uses one branch does better: for branch $l$, the best SNR of any scaling of $y_l$ is $\gamma_l$, and $\gamma_k$ is the largest of these.

From here on, the $h_l$ are independent $CN(0, \Omega)$ and all $N_{0,l} = N_0$, so the $\gamma_l$ are independent exponential with mean $\bar\gamma = \Omega E_s/N_0$, and $\Pr[\gamma_l < x] = 1 - e^{-x/\bar\gamma}$ for $x \ge 0$.

**Theorem 1 (outage).** $\Pr[\gamma_{\mathrm{SC}} < x] = (1 - e^{-x/\bar\gamma})^L$.

*Proof.* $\max_l \gamma_l < x$ if and only if $\gamma_l < x$ for every $l$. By independence, the probability is the product of the $L$ factors $1 - e^{-x/\bar\gamma}$. $\square$

**Theorem 2 (mean output SNR).** $E[\gamma_{\mathrm{SC}}] = \bar\gamma H_L$ with $H_L = \sum_{i=1}^{L} 1/i$.

*Proof.* For a nonnegative variable, $E\gamma = \int_0^\infty \Pr[\gamma > x]\, dx = \int_0^\infty (1 - (1 - e^{-x/\bar\gamma})^L)\, dx$. Substitute $t = 1 - e^{-x/\bar\gamma}$, so $dx = \bar\gamma\, dt/(1 - t)$ and $t$ runs from 0 to 1: $E\gamma = \bar\gamma\int_0^1 \frac{1 - t^L}{1 - t}\, dt = \bar\gamma \int_0^1 \sum_{i=0}^{L-1} t^i\, dt = \bar\gamma\sum_{i=0}^{L-1}\frac{1}{i+1}$. $\square$

**Theorem 3 (BPSK error rate).** With coherent BPSK on the selected branch, $P_b = \frac12 \sum_{k=0}^{L} (-1)^k \binom{L}{k} \sqrt{\bar\gamma/(\bar\gamma + k)}$.

*Proof.* Given $\gamma_{\mathrm{SC}} = \gamma$, the error probability is $Q(\sqrt{2\gamma})$, by Lemma 1. Let $F(\gamma) = (1 - e^{-\gamma/\bar\gamma})^L$ be the distribution function of Theorem 1. Integration by parts gives $P_b = E[Q(\sqrt{2\gamma})] = \int_0^\infty F(\gamma)\, \big(-\tfrac{d}{d\gamma}Q(\sqrt{2\gamma})\big)\, d\gamma$, because $F(0) = 0$ and $Q(\sqrt{2\gamma}) \to 0$ as $\gamma \to \infty$. The derivative is $-\frac{d}{d\gamma}Q(\sqrt{2\gamma}) = \frac{e^{-\gamma}}{2\sqrt{\pi\gamma}}$. Expand $F(\gamma) = \sum_{k=0}^{L}\binom{L}{k}(-1)^k e^{-k\gamma/\bar\gamma}$. For each $k$, with $b = 1 + k/\bar\gamma$, $\int_0^\infty \frac{e^{-b\gamma}}{2\sqrt{\pi\gamma}}\, d\gamma = \frac{1}{2\sqrt{b}}$, by the substitution $\gamma = u^2/b$ and $\int_0^\infty e^{-u^2}\, du = \sqrt\pi/2$. Since $1/\sqrt b = \sqrt{\bar\gamma/(\bar\gamma + k)}$, the sum is the claim. $\square$

For $L = 1$ the sum is $\frac12(1 - \sqrt{\bar\gamma/(1 + \bar\gamma)})$, the error rate of one Rayleigh branch. The test file compares Theorem 3 with a direct Simpson integral of $Q(\sqrt{2\gamma})$ against the density of the maximum, for $L = 1, \ldots, 4$ and 0 to 20 dB, within a relative error of $10^{-6}$.

**Remark (diversity order).** For $x$ fixed and $\bar\gamma \to \infty$, $1 - e^{-x/\bar\gamma} = x/\bar\gamma + O(\bar\gamma^{-2})$, so $\Pr[\gamma_{\mathrm{SC}} < x] = (x/\bar\gamma)^L(1 + O(1/\bar\gamma))$, and $-\log \Pr / \log \bar\gamma \to L$.
