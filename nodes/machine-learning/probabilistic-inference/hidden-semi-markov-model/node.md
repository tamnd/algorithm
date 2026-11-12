---
tag: YCP2N2
kind: model
slug: hidden-semi-markov-model
name: Hidden semi-Markov model
aliases:
- HSMM
- explicit-duration hidden Markov model
- variable-duration HMM
area: machine-learning/probabilistic-inference
level: advanced
summary: "An HMM in which each visit to a state lasts for a duration drawn from an explicit distribution, in place of the geometric durations of an HMM."
history:
  year: 1980
  people: [Jack D. Ferguson]
  note: Ferguson described the HMM with variable duration at the 1980 IDA symposium on hidden Markov models for text and speech. Yu (2010) surveys the later variants and algorithms.
prereqs: [hidden-markov-model, forward-algorithm]
see_also: [forward-backward-algorithm, viterbi-algorithm, baum-welch-algorithm, dynamic-bayesian-network, geometric-distribution, hmm-evaluation, hmm-decoding, state-space-model]
sources:
  - paper: "J. D. Ferguson, Variable duration models for speech, Proceedings of the Symposium on the Application of Hidden Markov Models to Text and Speech, Institute for Defense Analyses, Princeton, NJ, October 1980, pages 143-179"
    title: Ferguson 1980
    locator: the HMM with variable (explicit) state durations
  - paper: doi:10.1016/j.artint.2009.11.011
    title: Shun-Zheng Yu, Hidden semi-Markov models, Artificial Intelligence 174(2), 2010, pages 215 to 243
    locator: "Section 3.1 (the explicit duration HMM, with Ferguson as the first to consider it), equations (15) to (19) (the forward recursion with a self-transition probability of 0) and Section 3.1.1 (its cost, and the recursive product of the emissions)"
  - paper: doi:10.1109/5.18626
    title: Lawrence R. Rabiner, A tutorial on hidden Markov models and selected applications in speech recognition, Proceedings of the IEEE 77(2), 1989, pages 257 to 286
    locator: "Section IV (the inclusion of explicit state duration densities, the geometric duration of a plain HMM, and the extra cost)"
---

A hidden semi-Markov model (HSMM) is a [hidden Markov model](/hidden-markov-model/) in which a state, once entered, stays for a number of steps drawn from its own duration distribution $p_j(d)$, emits one symbol per step, and then moves to a different state. In a plain HMM the stay in state $j$ is always geometric, $P(d) = a_{jj}^{d-1} (1 - a_{jj})$, so the most likely stay is one step. An HSMM can give stays of any shape, for example a peak at 5 steps. The price is a forward recursion that also sums over the duration of the current segment: with durations up to $D$ it takes $O(T N^2 D + T N D)$ time in the direct form, and $O(T N^2 + T N D)$ when the segment starts are stored, against $O(T N^2)$ for an HMM.

## The machine

This page uses the explicit-duration HSMM of Ferguson (1980), as in Yu (2010, Section 3.1).

**Parameters.** States $1, \ldots, N$, symbols $1, \ldots, M$, and durations $1, \ldots, D$.

- $\pi_j$, the probability that the first segment has state $j$;
- $A_{ij}$, the probability that a segment of state $i$ is followed by a segment of state $j$, with $A_{ii} = 0$;
- $p_j(d)$, the probability that a segment of state $j$ lasts $d$ steps;
- $B_j(k)$, the probability that state $j$ emits $k$ at one step.

**How it makes a sequence.** Draw the first state $j_1$ from $\pi$. Then repeat: draw a duration $d$ from $p_{j}$, emit $d$ symbols, each drawn on its own from $B_j$, and draw the next state from the row $A_j$. Stop after $T$ symbols.

**The joint.** A segmentation is a list of segments $(j_1, d_1), \ldots, (j_K, d_K)$. If the durations sum to $T$, the probability of the segmentation together with $O$ is

$$\pi_{j_1} \prod_{k=2}^{K} A_{j_{k-1} j_k} \prod_{k=1}^{K} \Bigl( p_{j_k}(d_k) \prod_{t \in \text{segment } k} B_{j_k}(o_t) \Bigr).$$

There are two natural likelihoods.

- $P_{\text{end}}$: the last segment ends exactly at $T$. Sum the joint above over all segmentations.
- $P_{\text{cens}} = P(o_1, \ldots, o_T)$: the process goes on after $T$, so the last segment has lasted *at least* $d_K$ steps. In the last factor replace $p_j(d_K)$ by the survival $S_j(d_K) = \sum_{e \ge d_K} p_j(e)$. This is the right-censored likelihood. Over all $M^T$ sequences of length $T$ it sums to 1, and the tests check this.

**The forward recursion.** Let $\alpha_t(j) = P(o_1, \ldots, o_t, \text{a segment of } j \text{ ends at } t)$ and let $s_t(j)$ be the probability of $o_1, \ldots, o_{t-1}$ and a segment of $j$ that starts at $t$:

$$s_1(j) = \pi_j, \qquad s_t(j) = \sum_{i} \alpha_{t-1}(i) A_{ij} \quad (t \ge 2),$$

$$\alpha_t(j) = \sum_{d=1}^{\min(D, t)} s_{t-d+1}(j) \, p_j(d) \prod_{u = t-d+1}^{t} B_j(o_u).$$

Then $P_{\text{end}} = \sum_j \alpha_T(j)$, and $P_{\text{cens}}$ is the same sum at $t = T$ with $S_j(d)$ in place of $p_j(d)$. This is the recursion of Yu (2010, equations (15) to (19)), with $s_t$ in the role of Yu's $\alpha^*$. The implementation runs it in exact arithmetic and in log space, and the tests compare it with a list of all segmentations.

**Example.** Keep $\pi = (1/2, 1/2)$ and $B = \begin{pmatrix} 0.9 & 0.1 \\ 0.2 & 0.8 \end{pmatrix}$ from the rain (R) and dry (D) example of the HMM page. A segment must switch state, so $A_{RD} = A_{DR} = 1$. Let rain last 1, 2 or 3 days with the probabilities $(0.2, 0.3, 0.5)$, and dry with $(0.5, 0.25, 0.25)$. For $O = (u, u, n, u)$:

| $t$ | $o_t$ | $\alpha_t(R)$ | $\alpha_t(D)$ |
|---|---|---|---|
| 1 | u | 0.09 | 0.05 |
| 2 | u | 0.1305 | 0.014 |
| 3 | n | 0.02188 | 0.0598 |
| 4 | u | 0.013167 | 0.008128 |

For example $\alpha_2(R) = s_2(R) \, p_R(1) B_R(u) + s_1(R) \, p_R(2) B_R(u)^2 = 0.05 \cdot 0.2 \cdot 0.9 + 0.5 \cdot 0.3 \cdot 0.81 = 0.1305$, where $s_2(R) = \alpha_1(D) = 0.05$. Then $P_{\text{end}} = 0.021295$ and $P_{\text{cens}} = 0.072389$.

## What it counts

The size measures are $T$, the length of the sequence, $N$, the number of states, and $D$, the longest duration. One step is one arithmetic operation, as on the [real RAM](/real-ram/).

- **Forward pass.** The direct form, which writes $s_{t-d+1}(j)$ as a sum over $i$ inside the sum over $d$, costs $O(T N^2 D)$ for the transitions and $O(T N D)$ for the durations, so $O(T N^2 D + T N D)$. Computing each $s_t(j)$ once and reusing it, as the implementation does, brings the first term down to $O(T N^2)$. The product of the emissions is extended by one factor each time $d$ grows, so the duration term stays $O(T N D)$. Recomputing that product for each $d$ costs $O(T N D^2)$ instead; Yu (2010, Section 3.1.1) gives the cost in this form, and describes the recursive product that removes the extra factor $D$.
- **Memory.** $O(T N)$ for $\alpha$ and $s$, plus $O(N D)$ for the durations.
- **Other tasks.** The backward pass, the Viterbi algorithm over segmentations, and EM all have the same structure and the same cost per pass as the forward pass. EM also re-estimates each $p_j(d)$ from the expected number of segments of $j$ with length $d$.

## Relation to other models

- **The HMM is a special case.** Give state $j$ the geometric durations $p_j(d) = a^{d-1} (1 - a)$, with $a = a_{jj}$ of an HMM, and the transitions $A'_{ij} = a_{ij} / (1 - a_{ii})$ for $j \ne i$. Then the censored likelihood of the HSMM equals the HMM likelihood $P(O)$, and $P_{\text{end}}$ equals the probability that the HMM changes state after step $T$. The implementation builds this HSMM, with the duration table cut at $D = T + 1$ and the whole tail mass in the last entry, and the tests check both equalities exactly.
- **An HSMM is an HMM on a larger state space.** With durations at most $D$, use the pairs (state, steps left in the segment) as states. This gives an HMM with $N D$ states and a sparse transition matrix, so HSMM algorithms can be seen as HMM algorithms that exploit this sparsity.
- **Dynamic Bayesian networks.** The counter of steps left can be a second hidden variable in each time slice, so an HSMM is a [dynamic Bayesian network](/dynamic-bayesian-network/) with two hidden variables per slice.
- **Other variants.** Yu (2010) also describes models in which the next state depends on the duration, models with a residual-time variable, and segment models in which the symbols of one segment are not independent.

## Known results in the model

- **HMM durations are geometric.** In an HMM the probability of a stay of $d$ steps decreases with $d$, so the most likely stay is always 1. This is a poor fit for many real durations, such as the length of a phone in speech. Rabiner (Section IV) gives this as the motivation for explicit durations.
- **First description.** Yu (2010, Section 3.1) credits Ferguson (1980) as the first to consider the HSMM, which Ferguson called an HMM with variable duration.
- **The cost of explicit durations.** Exact inference adds the $O(T N D)$ duration term to the $O(T N^2)$ cost of an HMM. When $D$ is large this term dominates, so applications often cap $D$ or use a parametric duration family with few parameters.
- **Exactness of the reduction.** The geometric HSMM above gives the same likelihood as the HMM for every sequence, in exact arithmetic. So any HSMM algorithm, applied to it, must agree with the HMM algorithm, which is a useful test.
- **Uses.** Explicit duration models are used in speech recognition, in gene finding and in other segmentation tasks where the lengths of the segments matter.

## References
