---
title: A learned Bloom filter has no false negatives
proves: [correctness, invariant, termination]
status: full
---

Fix the classifier $\sigma$, the threshold $\tau$ and the set $S$. BUILD and QUERY consist of a finite number of classifier evaluations and Bloom filter steps, so they end. Let $N = \{x \in S : \sigma(x) < \tau\}$. We use one fact about a [Bloom filter](/bloom-filter/): it accepts every key it holds, and under ideal hashing it accepts each fixed key that it does not hold with a probability, its per-key rate, that is the same for all such keys.

**Theorem 1 (no false negatives).** QUERY$(x)$ returns true for each $x \in S$.

*Proof.* If there is an initial filter, it holds $S$ by line L1, so it accepts $x$ and line L4 does not return false. If $\sigma(x) \ge \tau$, line L5 returns true. Otherwise $x \in N$ by line L2, the backup filter holds $x$ by line L3, and line L6 returns true. $\square$

**Model.** Let $\mathcal{D}$ be a distribution on $U \setminus S$. Assume ideal and independent hash functions for $F_0$ and $F_b$, chosen independently of $\sigma$, $\tau$, $S$ and $\mathcal{D}$. Let $\varepsilon_0$ be the per-key rate of $F_0$ (with $\varepsilon_0 = 1$ if there is no initial filter), $\varepsilon_b$ that of $F_b$, and $F_p = \Pr_{x \sim \mathcal{D}}[\sigma(x) \ge \tau]$.

**Theorem 2 (rate on the query distribution).** For $x \sim \mathcal{D}$, independent of the hash functions,
$$ \Pr[\text{QUERY}(x) = \text{true}] = \varepsilon_0 \big(F_p + (1 - F_p)\, \varepsilon_b\big). $$

*Proof.* Fix $x \notin S$. Then $x \notin N$, since $N \subseteq S$. Let $A_0$ be the event that $F_0$ accepts $x$ (always true without an initial filter) and $A_b$ the event that $F_b$ accepts $x$. By lines L4 to L6,
$$ \text{QUERY}(x) = \text{true} \iff A_0 \text{ and } \big(\sigma(x) \ge \tau \text{ or } A_b\big). $$
The value $\sigma(x)$ is fixed. $A_0$ depends only on the hash functions of $F_0$ and $A_b$ only on those of $F_b$, which are independent, with $\Pr[A_0] = \varepsilon_0$ and $\Pr[A_b] = \varepsilon_b$ because $x$ is held by neither filter. So
$$ \Pr[\text{QUERY}(x) = \text{true}] = \varepsilon_0 \big([\sigma(x) \ge \tau] + [\sigma(x) < \tau]\, \varepsilon_b\big). $$
Averaging over $x \sim \mathcal{D}$, which is independent of the hash functions, replaces $[\sigma(x) \ge \tau]$ by $F_p$ and $[\sigma(x) < \tau]$ by $1 - F_p$. $\square$

**Remark (no per-key bound).** For a fixed $x \notin S$ with $\sigma(x) \ge \tau$, the proof gives $\Pr[\text{QUERY}(x) = \text{true}] = \varepsilon_0$, which is 1 without an initial filter. So the filter has no per-key rate better than $\varepsilon_0$, and the bound of Theorem 2 holds only on average over $\mathcal{D}$. $\blacksquare$
