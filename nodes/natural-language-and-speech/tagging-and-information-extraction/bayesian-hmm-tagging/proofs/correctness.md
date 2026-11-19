---
title: "The collapsed conditional of the Bayesian HMM, and why the Gibbs sampler targets the posterior"
proves: [correctness]
status: full
---

Setting. Tags are $1, \ldots, k$, and $0$ marks the sentence boundary before the first word and after the last word of each sentence. Row $a \in \{0, \ldots, k\}$ has transition probabilities $\tau_a \sim \mathrm{Dirichlet}(\alpha, \ldots, \alpha)$ over the $K = k + 1$ outcomes $0, \ldots, k$. Tag $t$ has emission probabilities $\omega_t \sim \mathrm{Dirichlet}(\beta, \ldots, \beta)$ over the $V$ word types (the code calls this number W). All these vectors are independent. For a tagging $\mathbf t$ of a corpus $\mathbf w$, let $n_{a,b}$ be the number of transitions from $a$ to $b$ (with the boundary transitions), $n_a = \sum_b n_{a,b}$, $n_{t,w}$ the number of tokens of word $w$ with tag $t$, and $n_t = \sum_w n_{t,w}$. Write $x^{(n)} = x (x+1) \cdots (x+n-1)$ for the rising factorial, so $x^{(n)} = \Gamma(x+n)/\Gamma(x)$.

## Lemma 1: the marginal likelihood

$$P(\mathbf t, \mathbf w) = \prod_{a=0}^{k} \frac{\prod_{b=0}^{k} \alpha^{(n_{a,b})}}{(K\alpha)^{(n_a)}} \cdot \prod_{t=1}^{k} \frac{\prod_{w} \beta^{(n_{t,w})}}{(V\beta)^{(n_t)}}.$$

Proof. Given $\tau$ and $\omega$, the probability of $(\mathbf t, \mathbf w)$ is $\prod_{a,b} \tau_{a,b}^{n_{a,b}} \prod_{t,w} \omega_{t,w}^{n_{t,w}}$. The vectors are independent, so the expectation over the prior splits into one factor per row. For one row with a symmetric Dirichlet with parameter $\gamma$ on $D$ outcomes and counts $m_1, \ldots, m_D$ with sum $m$,

$$\mathbb E\Bigl[\prod_d \theta_d^{m_d}\Bigr] = \frac{\Gamma(D\gamma)}{\Gamma(\gamma)^D} \int \prod_d \theta_d^{m_d + \gamma - 1} \, d\theta = \frac{\Gamma(D\gamma)}{\Gamma(D\gamma + m)} \prod_d \frac{\Gamma(\gamma + m_d)}{\Gamma(\gamma)} = \frac{\prod_d \gamma^{(m_d)}}{(D\gamma)^{(m)}},$$

by the Dirichlet normalizing constant. Taking $D = K$, $\gamma = \alpha$ for the transition rows and $D = V$, $\gamma = \beta$ for the emission rows gives the formula. $\square$

## Lemma 2: the collapsed conditional

Fix a token at position $i$ of a sentence, with word $w$, left neighbour tag $a$ (or $0$ at the start) and right neighbour tag $b$ (or $0$ at the end). Let $n^{-}$ denote the counts of all other tokens and transitions: the counts of $\mathbf t$ without the transitions $(a, t_i)$ and $(t_i, b)$ and without the emission $(t_i, w)$. Then for $t \in \{1, \ldots, k\}$,

$$P(t_i = t \mid \mathbf t_{-i}, \mathbf w) \propto \frac{n^{-}_{t,w} + \beta}{n^{-}_t + V\beta} \cdot \frac{n^{-}_{a,t} + \alpha}{n^{-}_a + K\alpha} \cdot \frac{n^{-}_{t,b} + [a = t = b] + \alpha}{n^{-}_t{}' + [a = t] + K\alpha},$$

where $n^{-}_t{}'$ is the number of transitions out of $t$ in $n^{-}$ (the code keeps it as `out[t]`), and $[\cdot]$ is 1 when the condition holds and 0 otherwise.

Proof. The conditional is proportional, as a function of $t$, to the marginal $P(\mathbf t, \mathbf w)$ with $t_i = t$, since the other tags and the words are fixed. By Lemma 1 the marginal is a product of row factors, and each row factor can be built by adding the counts one at a time: adding one more outcome $d$ to a row with counts $m_d$ and total $m$ multiplies the factor by $(\gamma + m_d)/(D\gamma + m)$, because $\gamma^{(m_d + 1)} = \gamma^{(m_d)} (\gamma + m_d)$ and $(D\gamma)^{(m+1)} = (D\gamma)^{(m)} (D\gamma + m)$. The rows are exchangeable, so the order of adding does not matter.

Start from the counts $n^{-}$; the factor they give does not depend on $t$. Add the three events of position $i$ in this order:

1. The emission $(t, w)$ multiplies the emission row of $t$ by $(n^{-}_{t,w} + \beta)/(n^{-}_t + V\beta)$.
2. The transition $(a, t)$ multiplies the transition row of $a$ by $(n^{-}_{a,t} + \alpha)/(n^{-}_a + K\alpha)$. After this step, row $a$ has one more count in total and one more count at $t$.
3. The transition $(t, b)$ multiplies the transition row of $t$ by $(m_b + \alpha)/(m + K\alpha)$, where $m_b$ and $m$ are the counts of row $t$ after step 2. If $a \ne t$, step 2 changed another row, so $m_b = n^{-}_{t,b}$ and $m = n^{-}_t{}'$. If $a = t$, step 2 added one to the total of row $t$, and also one to its entry $b$ exactly when $b = t$. So $m = n^{-}_t{}' + [a = t]$ and $m_b = n^{-}_{t,b} + [a = t = b]$.

The product of the three multipliers is the stated formula. $\square$

Lines L4, L5 and L7 of the code implement Lemma 2: L4 removes the three events, L5 forms the product, and L7 adds the events back with the new tag. The test file checks Lemma 2 against the ratio of exact marginals of Lemma 1 in rational arithmetic, on random corpora and on the case $a = t = b$.

## Theorem: the sampler leaves the posterior invariant

Each update at L6 draws $t_i$ from its exact conditional $P(t_i \mid \mathbf t_{-i}, \mathbf w)$ and keeps the other tags. Such an update leaves $\pi(\mathbf t) = P(\mathbf t \mid \mathbf w)$ invariant: if $\mathbf t \sim \pi$, then $\mathbf t_{-i}$ has its marginal under $\pi$, and the new $t_i$ is drawn from $\pi(t_i \mid \mathbf t_{-i})$, so the new pair has law $\pi$. A sweep is a composition of such updates, so it also leaves $\pi$ invariant.

With $\alpha, \beta > 0$ every conditional gives positive probability to every tag, so one sweep can move from any tagging to any other with positive probability. The chain on the finite set of taggings is therefore irreducible and aperiodic (it can stay where it is), and by the convergence theorem for finite [Markov chains](/markov-chain/) the law of the state after $s$ sweeps converges to $\pi$ as $s \to \infty$. This is the standard argument for [Gibbs sampling](/gibbs-sampling/); it gives no bound on the number of sweeps, and on real corpora mixing is slow. The test file checks the invariance in practice: on a corpus of 4 tokens with 16 taggings, the frequencies of 20000 sweeps match the exact posterior, computed by enumeration with Lemma 1, within 0.01.
