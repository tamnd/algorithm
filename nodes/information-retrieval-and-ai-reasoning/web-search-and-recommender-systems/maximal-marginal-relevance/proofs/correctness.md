---
title: The incremental MMR loop picks the item of the MMR formula at every step
proves: [correctness]
status: full
---

Let $R$ be a finite set of candidate ids with a total order, $\mathrm{rel} : R \to \mathbb{R}$, $\mathrm{sim} : R \times R \to \mathbb{R}$ and $\lambda \in [0, 1]$. For a chosen list $S$ (as a set) and $d \in R \setminus S$, define the penalty $\pi_S(d) = \max_{j \in S} \mathrm{sim}(d, j)$ for $S \ne \emptyset$ and $\pi_\emptyset(d) = 0$, and the MMR score

$$\mathrm{MMR}_S(d) = \lambda\, \mathrm{rel}(d) - (1 - \lambda)\, \pi_S(d).$$

The MMR selection of Carbonell and Goldstein, with the tie rule of this page, is the list $s_1, \ldots, s_m$ with $m = \min(k, |R|)$, where $s_t$ is the smallest id among the maximizers of $\mathrm{MMR}_{S_{t-1}}$ over $R \setminus S_{t-1}$ and $S_t = \{s_1, \ldots, s_t\}$.

**Lemma 1 (invariant).** At the start of each pass of the loop of line L4, with $S$ the set of ids chosen so far, $\mathrm{closest}[d] = \pi_S(d)$ for every remaining $d$.

*Proof.* By induction on $|S|$. For $S = \emptyset$, line L3 sets every value to $0 = \pi_\emptyset(d)$. Suppose the claim holds before a pass that adds $b$, so $S' = S \cup \{b\}$. If $S = \emptyset$, lines L8 and L9 set $\mathrm{closest}[d] = \mathrm{sim}(d, b) = \pi_{\{b\}}(d)$ for every remaining $d$, whatever its sign. Otherwise they set $\mathrm{closest}[d] = \max(\pi_S(d), \mathrm{sim}(d, b)) = \pi_{S'}(d)$, because the maximum over $S'$ is the larger of the maximum over $S$ and the new term. $\square$

**Theorem 2 (output).** The procedure returns $s_1, \ldots, s_m$, each with its score $\mathrm{MMR}_{S_{t-1}}(s_t)$.

*Proof.* By Lemma 1, line L6 computes $\mathrm{MMR}_S(d)$ for each remaining $d$. Line L1 sorts the ids, and the scan of line L5 replaces the current best only on a strictly larger score, so it keeps the smallest id among the maximizers, which is $s_t$. Line L7 records it with its score and removes it. The loop runs while ids remain and fewer than $k$ are chosen, so it makes $m$ passes. $\square$

**Corollary 3 (the ends of the range of lambda).** For $\lambda = 1$ the output is the first $m$ ids in the order rel descending, then id ascending. For $\lambda = 0$ the first pick is the smallest id, because every score is $0$, and each later pick minimizes the largest similarity to the chosen ids.

*Proof.* For $\lambda = 1$ the score is $\mathrm{rel}(d)$ and does not depend on $S$, so the picks are the remaining maxima in turn. For $\lambda = 0$ the score is $-\pi_S(d)$. $\square$

**Cost.** Let $n = |R|$. Each of the $m \le k$ passes scores at most $n$ ids in line L6 and calls $\mathrm{sim}$ at most $n$ times in line L8, so the procedure makes at most $nk$ calls of $\mathrm{sim}$ and $O(nk)$ other operations, after the sort of line L1 in $O(n \log n)$. It keeps one value for each id, $O(n)$ extra space. The direct form of the formula recomputes $\pi_S$ from scratch and calls $\mathrm{sim}$ $O(nk^2)$ times.

The test file checks Theorem 2 step by step against that direct form, on the toy collection and on random instances, many of them with values on a grid of $0.25$ so that ties are frequent.
