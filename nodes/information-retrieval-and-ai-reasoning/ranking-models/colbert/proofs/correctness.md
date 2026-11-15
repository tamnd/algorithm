---
title: Reranking a candidate set that holds the true top k gives the exhaustive result, and a missed document scores at most the sum of the k'-th token scores
proves: [correctness]
status: full
---

A query is a list of unit vectors $q_1, \ldots, q_n$ and document $d$ is a list of unit vectors $e_{d,1}, \ldots, e_{d,m_d}$, with $m_d \ge 1$. They are the outputs of the encoders, which this proof treats as given. The late interaction score is

$$S(q, d) = \sum_{i=1}^{n} \max_{j} q_i \cdot e_{d,j},$$

the sum of MaxSim of Khattab and Zaharia (2020), Equation (3), with the cosine similarity. A ranking of documents sorts by $S$, highest first, then by the smaller document id.

**Lemma 1.** The code computes $S(q, d)$, and $-n \le S(q, d) \le n$. A document that holds every query vector gets $S = n$.

*Proof.* `maxsim_score` takes, for each $q_i$, the largest inner product over the tokens of $d$, and sums them. Each inner product of unit vectors is in $[-1, 1]$ by the Cauchy-Schwarz inequality, and equals 1 for $e = q_i$. $\square$

Stage 1 (lines L1 to L4) takes, for each $q_i$, the $k'$ document tokens of largest $q_i \cdot e$ over the whole collection, with ties to the smaller document id and token position, and lets $C$ be the set of the documents that own one of these tokens. Stage 2 (lines L5 and L6) scores each document of $C$ exactly and returns the top $k$ of $C$. Let $T_k$ be the exhaustive top $k$ over all documents.

**Lemma 2 (a superset is enough).** If $T_k \subseteq C$, stage 2 returns $T_k$, in the exhaustive order.

*Proof.* Every document has the distinct key $(-S(q, d), d)$. $T_k$ is the set of the $k$ smallest keys of the collection. Since $T_k \subseteq C$, these are also the $k$ smallest keys of $C$, and both rankings list them in increasing key order. $\square$

**Corollary.** If $k'$ is at least the number of tokens in the collection, $C$ is every document, and end-to-end retrieval returns the exhaustive top $k$.

*Proof.* Each $q_i$ then keeps every token, and every document has at least one token, so $C$ is the whole collection. Apply Lemma 2. $\square$

**Lemma 3 (stage 1 can miss the best document).** For $k' < $ the number of tokens, Lemma 2 does not hold in general.

*Proof.* Take $q_1 = (1, 0)$ and $q_2 = (0, 1)$, document 0 with the tokens $(0.8, 0.6)$ and $(0.6, 0.8)$, document 1 with the token $(1, 0)$ and document 2 with the token $(0, 1)$. The scores are $S = 1.6, 1.0, 1.0$, so $T_1 = \{0\}$. With $k' = 1$, the best token for $q_1$ is the one of document 1 and the best for $q_2$ is the one of document 2, so $C = \{1, 2\}$ and stage 2 returns document 1. $\square$

Document 0 is good for both query vectors and best for neither, and stage 1 looks at each query vector alone.

**Lemma 4 (a certificate).** Let $\tau_i$ be the $k'$-th largest value of $q_i \cdot e$ over all document tokens. Every document $d \notin C$ has $S(q, d) \le \sum_i \tau_i$. So if the $k$-th score that stage 2 returns is larger than $\sum_i \tau_i$, the result equals the exhaustive top $k$.

*Proof.* If $d \notin C$, no token of $d$ is among the $k'$ kept for any $q_i$, so each of its tokens has $q_i \cdot e \le \tau_i$, and $\max_j q_i \cdot e_{d,j} \le \tau_i$. Sum over $i$. If the $k$-th returned score exceeds this bound, every document outside $C$ has a smaller score than each returned document, so the returned set holds the $k$ best documents of the collection and, by Lemma 2 applied to it, comes in the exhaustive order. $\square$

In the example of Lemma 3, $\tau_1 = \tau_2 = 1$, the bound is 2, and the returned score 1.0 does not certify the result, as it must not.

**Lemma 5 (training gradient).** For the pairwise loss $\ell = -\log \frac{e^{S^+}}{e^{S^+} + e^{S^-}}$ with $S^{\pm} = S(q, d^{\pm})$, at a point where each max has a unique argmax $j^{\pm}(i)$,

$$\frac{\partial \ell}{\partial q_i} = (p^+ - 1)\, e_{d^+, j^+(i)} + (1 - p^+)\, e_{d^-, j^-(i)}, \qquad p^+ = \frac{e^{S^+}}{e^{S^+} + e^{S^-}}.$$

*Proof.* Near such a point each max is the single term $q_i \cdot e_{d, j(i)}$, so $\partial S^{\pm} / \partial q_i = e_{d^{\pm}, j^{\pm}(i)}$. Also $\partial \ell / \partial S^+ = p^+ - 1$ and $\partial \ell / \partial S^- = 1 - p^+$. $\square$

The gradient is taken in the given vectors, not through the normalization, and only the winning token of each document gets a gradient for each query vector. Where two tokens tie, $S$ is not differentiable and any convex combination of their gradients is a subgradient of the max.

**What is outside the proof.** The encoders and the quality of the ranking they give are outside the code, and the effectiveness and latency figures of the paper are measurements. The paper's stage 1 uses an approximate index, so even the certificate of Lemma 4 is about the exact search used here.

The tests in `impl/python/test_colbert.py` check Lemma 1 against a double loop, the corollary and Lemma 2 on random collections, the counterexample of Lemma 3, Lemma 4 on random collections, Lemma 5 by central finite differences away from ties, the tie rule, and the worked example of the page.
