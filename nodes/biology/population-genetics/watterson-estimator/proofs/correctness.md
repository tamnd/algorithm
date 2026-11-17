---
title: Watterson's estimator counts the segregating sites and is unbiased for theta
proves: [correctness]
status: full
---

**Setting.** A sample of $n \ge 2$ sequences comes from the neutral infinite sites model: the genealogy is a Kingman coalescent tree, time is in units of $2N$ generations, and given the tree, mutations fall on the branches as a Poisson process of rate $\theta/2$ per unit of branch length. While $k$ lineages exist, the time $T_k$ is exponential with rate $\binom{k}{2}$, and $T_2, \ldots, T_n$ are independent. Write $a_n = \sum_{i=1}^{n-1} 1/i$ and $b_n = \sum_{i=1}^{n-1} 1/i^2$.

**Lemma 1.** WATTERSON returns $S / a_n$, where $S$ is the number of segregating sites.

*Proof.* Before line L2, $S = 0$. The loop visits each site $j$ once, and line L3 adds one exactly when column $j$ has two different non-missing characters, which is the definition of a segregating site. So after the loop $S$ is the number of segregating sites. Line L4 sets $a = a_n$, and line L5 returns $S / a_n$. $\square$

**Lemma 2.** Let $L = \sum_{k=2}^{n} k T_k$ be the total branch length. Then $E[L] = 2 a_n$ and $\operatorname{Var}[L] = 4 b_n$.

*Proof.* While $k$ lineages exist, $k$ branches each grow by $T_k$, so the total branch length is $\sum_k k T_k$. An exponential time with rate $\lambda$ has mean $1/\lambda$ and variance $1/\lambda^2$. With $\lambda = k(k-1)/2$,

$$E[k T_k] = \frac{2}{k - 1}, \qquad \operatorname{Var}[k T_k] = \frac{4}{(k - 1)^2}.$$

Summing over $k = 2, \ldots, n$ and using the independence of the $T_k$ for the variance, $E[L] = 2 \sum_{i=1}^{n-1} 1/i = 2 a_n$ and $\operatorname{Var}[L] = 4 \sum_{i=1}^{n-1} 1/i^2 = 4 b_n$. $\square$

**Lemma 3.** $E[S] = \theta a_n$, $\operatorname{Var}[S] = \theta a_n + \theta^2 b_n$, and $E[S(S-1)] = \theta^2 (a_n^2 + b_n)$.

*Proof.* Under the infinite sites model each mutation creates a new segregating site, and every segregating site comes from one mutation. So $S$ is the number of mutations on the tree, and given $L$ it is Poisson with mean $\theta L / 2$. By the laws of total expectation and total variance and Lemma 2,

$$E[S] = E\!\left[\frac{\theta L}{2}\right] = \theta a_n,$$

$$\operatorname{Var}[S] = E\!\left[\frac{\theta L}{2}\right] + \operatorname{Var}\!\left[\frac{\theta L}{2}\right] = \theta a_n + \frac{\theta^2}{4} \cdot 4 b_n = \theta a_n + \theta^2 b_n.$$

Then $E[S(S - 1)] = \operatorname{Var}[S] + E[S]^2 - E[S] = \theta^2 b_n + \theta^2 a_n^2$. $\square$

**Theorem.** Under the model, $E[\hat\theta_W] = \theta$ and $\operatorname{Var}[\hat\theta_W] = \theta / a_n + \theta^2 b_n / a_n^2$. The estimate

$$V = \frac{\hat\theta_W}{a_n} + \frac{b_n}{a_n^2} \cdot \frac{S(S - 1)}{a_n^2 + b_n}$$

has $E[V] = \operatorname{Var}[\hat\theta_W]$.

*Proof.* By Lemma 1, $\hat\theta_W = S / a_n$. By Lemma 3, $E[S / a_n] = \theta$ and $\operatorname{Var}[S / a_n] = \operatorname{Var}[S] / a_n^2 = \theta / a_n + \theta^2 b_n / a_n^2$. For $V$, $E[\hat\theta_W / a_n] = \theta / a_n$, and by Lemma 3, $E[S(S - 1) / (a_n^2 + b_n)] = \theta^2$. By linearity, $E[V] = \theta / a_n + \theta^2 b_n / a_n^2$. $\blacksquare$

**Remarks.** The proof of $E[S] = \theta a_n$ uses only the expected length of the tree of each site. With recombination, each site has its own tree, every local tree is a Kingman tree with the same expected length, and so $E[S] = \theta a_n$ still holds when $\theta$ is the rate of the whole region. Lemma 3 for the variance uses one tree for all sites, so with recombination the variance is smaller than the formula. The tests check $E[\hat\theta_W] = \theta$, the variance formula, $E[S(S-1)] = \theta^2(a_n^2 + b_n)$ and $E[V] = \operatorname{Var}[\hat\theta_W]$ on 20000 simulated samples with $n = 10$ and $\theta = 5$.
