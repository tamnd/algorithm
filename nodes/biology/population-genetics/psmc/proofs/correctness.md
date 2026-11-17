---
title: PSMC builds the HMM of the model, computes its likelihood exactly and never lowers it
proves: [correctness]
status: full
---

**Setting.** The breaks are $0 = t_0 < \cdots < t_k = \infty$, and $\lambda(t) = \lambda_j > 0$ on $I_j = [t_{j-1}, t_j)$. Let $\Lambda(t) = \int_0^t du/\lambda(u)$ and $G(x) = \int_0^x e^{\Lambda(u)} du$. The coalescence time $T$ of the two copies at a bin has the density $p(t) = e^{-\Lambda(t)}/\lambda(t)$, so $P(T \ge x) = e^{-\Lambda(x)}$. Given $T = t$, the bin is heterozygous with probability $1 - e^{-\theta t}$. Between two bins, with probability $e^{-\rho t}$ the next time is $t$, and otherwise the next time is $T'$, drawn as follows: $u$ is uniform on $(0, t)$, and given $u$, $P(T' \ge x) = e^{-(\Lambda(x) - \Lambda(u))}$ for $x \ge u$ and $1$ for $x < u$.

**Lemma 1.** For $t > 0$ and $x \ge 0$, $H(t, x) = \int_0^t P(T' \ge x \mid u)\, du$ is $e^{-\Lambda(x)} G(t)$ when $x \ge t$, and $e^{-\Lambda(x)} G(x) + (t - x)$ when $x < t$. Also $H(t, 0) = t$ and $H(t, \infty) = 0$.

*Proof.* If $x \ge t$, every $u$ in $(0, t)$ has $u \le x$, so the integrand is $e^{\Lambda(u) - \Lambda(x)}$, and the integral is $e^{-\Lambda(x)} G(t)$. If $x < t$, split at $x$: on $(0, x)$ the integrand is $e^{\Lambda(u) - \Lambda(x)}$, which gives $e^{-\Lambda(x)} G(x)$, and on $(x, t)$ it is 1, which gives $t - x$. With $x = 0$, $G(0) = 0$ and the value is $t$. As $x \to \infty$, $\Lambda(x) \to \infty$ while $G(t)$ is fixed, so $H(t, x) \to 0$. $\square$

**Lemma 2.** Let $J_{jl} = P(T \in I_j, T_{\text{next}} \in I_l)$ for the times of two neighbouring bins, with $T$ from the density $p$. Then

$$J_{jl} = [j = l] \int_{I_j} p(t) e^{-\rho t} dt + \int_{I_j} p(t) \frac{1 - e^{-\rho t}}{t} \big(H(t, t_{l-1}) - H(t, t_l)\big) dt,$$

and $\sum_l J_{jl} = \pi_j = P(T \in I_j)$.

*Proof.* Condition on $T = t$ in $I_j$. Without recombination, probability $e^{-\rho t}$, the next time is $t \in I_j$. With recombination, the next time is $T'$, and

$$P(T' \in I_l \mid t) = \frac{1}{t}\int_0^t \big(P(T' \ge t_{l-1} \mid u) - P(T' \ge t_l \mid u)\big) du = \frac{H(t, t_{l-1}) - H(t, t_l)}{t}.$$

Integrating against $p(t)$ over $I_j$ gives the formula. Summed over $l$, the differences telescope to $H(t, 0) - H(t, \infty) = t$ by Lemma 1, so $\sum_l J_{jl} = \int_{I_j} p(t)(e^{-\rho t} + 1 - e^{-\rho t}) dt = \pi_j$. $\square$

So $A_{jl} = J_{jl}/\pi_j$ is the transition matrix of the interval of $T$, and each row sums to 1. The code divides each row by its numerical sum, which is $\pi_j$ up to the error of the Simpson rule.

**Lemma 3.** For $c \ge 0$, $\int_{I_j} p(t) e^{-ct} dt = \frac{e^{-\Lambda(t_{j-1}) - c t_{j-1}}}{\lambda_j (1/\lambda_j + c)} \left(1 - e^{-(1/\lambda_j + c)(t_j - t_{j-1})}\right)$, with the last factor 1 when $t_j = \infty$. In particular, $\pi_j = e^{-\Lambda(t_{j-1})} - e^{-\Lambda(t_j)}$, and $e_j = 1 - \frac{1}{\pi_j} \int_{I_j} p(t) e^{-\theta t} dt$ is the probability that a bin is heterozygous given $T \in I_j$.

*Proof.* On $I_j$, $\Lambda(t) = \Lambda(t_{j-1}) + (t - t_{j-1})/\lambda_j$, so the integrand is $\frac{1}{\lambda_j} e^{-\Lambda(t_{j-1}) - c t_{j-1}} e^{-(1/\lambda_j + c)(t - t_{j-1})}$, an exponential whose integral over $I_j$ is the formula. With $c = 0$ it gives $\pi_j$. Given $T \in I_j$, $T$ has the density $p/\pi_j$ on $I_j$, and the probability of a homozygous bin is the mean of $e^{-\theta T}$. $\square$

Lemma 3 with $c = \rho$ gives the first term of Lemma 2. On $I_i$, $\int_{I_i \cap (0, x)} e^{\Lambda(u)} du = \lambda_i (e^{\Lambda(\min(x, t_i))} - e^{\Lambda(t_{i-1})})$, and $G(x)$ is the sum over $i$ of these terms. This is how the code computes $G$, with every exponent shifted by $-\Lambda(x)$ so that none is positive.

**Lemma 4.** For observations $o_1, \ldots, o_n$, with $b_i(j) = e_j$, $1 - e_j$ or $1$ for a heterozygous, homozygous or missing bin, lines L3 and L4 give $\prod_i c_i = P(o_1, \ldots, o_n)$, $\alpha_i(j)\beta_i(j) = P(S_i = j \mid o)$, and $\alpha_{i-1}(j) A_{jl} b_i(l) \beta_i(l)/c_i = P(S_{i-1} = j, S_i = l \mid o)$, where $S_i$ is the hidden state of bin $i$.

*Proof.* By induction, $\alpha_i(j) = P(S_i = j \mid o_1, \ldots, o_i)$ and $c_i = P(o_i \mid o_1, \ldots, o_{i-1})$: the unscaled vector $(\alpha_{i-1} A) \circ b_i$ is $P(S_i = j, o_i \mid o_1..o_{i-1})$ by the Markov property, and its sum is $c_i$. The product of the $c_i$ is $P(o)$ by the chain rule. Backward, $\beta_i(j) = P(o_{i+1}, \ldots, o_n \mid S_i = j) / P(o_{i+1}, \ldots, o_n \mid o_1, \ldots, o_i)$, again by induction from $\beta_n = 1$, because $\sum_l A_{jl} b_{i+1}(l) \beta_{i+1}(l)/c_{i+1}$ conditions on the next state. The two claims about posteriors follow by Bayes' rule, since given $S_i$ the observations before and after bin $i$ are independent. A missing bin multiplies every state by 1, which is the same as leaving it out of the product. $\square$

**Lemma 5.** Let $F_j$, $X_{jl}$, $H_j$ and $M_j$ be the posterior expected counts under $\lambda$ of line L5, and define $Q(\lambda')$ as on the page with $\pi$, $A$, $e$ from $\lambda'$. Then $\ell(\lambda') - \ell(\lambda) \ge Q(\lambda') - Q(\lambda)$, where $\ell$ is the log-likelihood.

*Proof.* For a path $s$ of states, $\ln P_{\lambda'}(s, o) = \ln \pi_{s_1} + \sum_i \ln A_{s_{i-1} s_i} + \sum_{i : o_i \ne \text{missing}} \ln b_i(s_i)$, so $Q(\lambda') = E_\lambda[\ln P_{\lambda'}(S, o) \mid o]$, with the expectation over the posterior $q(s) = P_\lambda(s \mid o)$ of Lemma 4. Then

$$\ell(\lambda') = \ln \sum_s P_{\lambda'}(s, o) \ge \sum_s q(s) \ln \frac{P_{\lambda'}(s, o)}{q(s)} = Q(\lambda') + \mathcal{H}(q)$$

by Jensen's inequality, where $\mathcal{H}(q)$ is the entropy of $q$, and equality holds at $\lambda' = \lambda$ because then $P_\lambda(s, o)/q(s) = P_\lambda(o)$ for every $s$. Subtracting the two gives the claim. $\square$

**Theorem.** Each iteration of lines L1 to L6 returns sizes $\lambda'$ with $\ell(\lambda') \ge \ell(\lambda)$, and the log-likelihoods that the implementation reports never decrease.

*Proof.* Line L6 starts from $\lambda' = \lambda$ and replaces one coordinate only when the new value has a strictly larger $Q$. So at the end $Q(\lambda') \ge Q(\lambda)$, and Lemma 5 gives $\ell(\lambda') \ge \ell(\lambda)$. The model matrices are those of Lemmas 2 and 3 computed with the same Simpson rule at every iteration, so the argument applies to the HMM that the code builds. $\square$

The theorem does not say that EM reaches the maximum likelihood: it can stop at a local maximum or a saddle point, and the result depends on the start.
