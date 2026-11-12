---
tag: 5QJWH3
kind: problem
slug: hmm-evaluation
name: HMM evaluation
aliases:
- likelihood computation for an HMM
area: machine-learning/probabilistic-inference
level: intro
summary: "Compute P(O | model), the probability that a hidden Markov model emits a given observation sequence. A direct sum has N^T terms; the forward algorithm takes O(T N^2)."
prereqs: [hidden-markov-model]
see_also: [forward-algorithm, hmm-decoding, hmm-parameter-learning, marginal-inference, forward-backward-algorithm, weighted-automaton, log-sum-exp-trick, profile-hmm]
sources:
  - paper: doi:10.1109/5.18626
    title: Lawrence R. Rabiner, A tutorial on hidden Markov models and selected applications in speech recognition, Proceedings of the IEEE 77(2), 1989, pages 257 to 286
    locator: "Section II.C (Problem 1 of the three basic problems), Section III.A (the direct sum, its cost of about 2T N^T operations, and the forward procedure with about N^2 T) and Section V.A (scaling)"
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: "Section 13.2.2 (the likelihood from the forward variables)"
---

HMM evaluation asks for the probability $P(O \mid \lambda)$ that a [hidden Markov model](/hidden-markov-model/) $\lambda = (\pi, A, B)$ emits a given observation sequence $O = o_1 \ldots o_T$. It is the first of the three basic HMM problems in Rabiner's tutorial. The definition is a sum over all $N^T$ hidden state paths, but the [forward algorithm](/forward-algorithm/) computes it in $\Theta(T N^2)$ time.

## In plain words

A model can make many different sequences. You have one sequence and you ask how likely the model was to make it. Each possible hidden path gives a part of the answer, and the answer is the total over all paths. There are far too many paths to list, but the total can be built step by step, keeping one number per state.

## Definition

**Input:** an HMM $\lambda = (\pi, A, B)$ with $N$ states and $M$ symbols, and a sequence $O = o_1 \ldots o_T$ of symbols.

**Output:** the likelihood

$$P(O \mid \lambda) = \sum_{q_1, \ldots, q_T} \pi_{q_1} B_{q_1}(o_1) \prod_{t=2}^{T} A_{q_{t-1} q_t} B_{q_t}(o_t).$$

For long sequences this number underflows, so the output is in practice $\log P(O \mid \lambda)$.

## Variants

- **Log-likelihood.** Return $\log P(O \mid \lambda)$, computed with scaling or with the [log-sum-exp trick](/log-sum-exp-trick/).
- **Filtering.** Return $P(q_t \mid o_1, \ldots, o_t)$ for each $t$. The same forward pass gives it.
- **Prefix probabilities.** Return $P(o_1, \ldots, o_t)$ for every $t$, for example to score a stream as it arrives.
- **Continuous outputs.** $B_j(o_t)$ is a density value. Then $P(O \mid \lambda)$ is a density, and the same algorithms apply.

## Examples

Take the rain and dry model of the HMM page: $\pi = (1/2, 1/2)$, $A = \begin{pmatrix} 0.7 & 0.3 \\ 0.2 & 0.8 \end{pmatrix}$, $B = \begin{pmatrix} 0.9 & 0.1 \\ 0.2 & 0.8 \end{pmatrix}$ with the symbols umbrella (u) and none (n). For $O = (u, u, n, u)$ there are $2^4 = 16$ paths. Their joint probabilities sum to $P(O) = 982301 / 20000000 = 0.04911505$, so $\log P(O) = -3.0136$. The single path R R R R contributes $0.01250235$, about a quarter of the total.

## Known algorithms

| Algorithm | Time | Space | Note |
|---|---|---|---|
| Sum over all paths | $\Theta(T N^T)$ | $\Theta(T)$ | the definition; Rabiner counts about $2 T N^T$ operations |
| [Forward algorithm](/forward-algorithm/) | $\Theta(T N^2)$ | $\Theta(N)$ | exact; scaled or in log space for long $T$ |
| Backward pass of [forward-backward](/forward-backward-algorithm/) | $\Theta(T N^2)$ | $\Theta(N)$ | $P(O) = \sum_i \pi_i B_i(o_1) \beta_1(i)$ |

The difference is large. Rabiner's example is $N = 5$ and $T = 100$: the direct sum needs about $10^{72}$ operations, and the forward algorithm about $N^2 T = 2500$.

## Bounds

An exact algorithm must read the $T$ symbols and, in general, all $N^2$ entries of $A$, so it needs $\Omega(T + N^2)$ time. The forward algorithm does a vector-matrix product at each step, $\Theta(T N^2)$ in all. With a sparse $A$ that has $E$ nonzero entries, the same algorithm takes $\Theta(T (N + E))$ time.

## Reductions

- **To marginal inference.** The HMM is a Bayesian network on a chain, and $P(O)$ is the probability of the evidence $O$. So HMM evaluation is a case of [marginal inference](/marginal-inference/), and variable elimination along the chain is the forward algorithm.
- **To a matrix product.** Let $D_k$ be the diagonal matrix with the entries $B_1(k), \ldots, B_N(k)$. Then $P(O) = \pi^\top D_{o_1} A D_{o_2} A \cdots A D_{o_T} \mathbf{1}$. This is the weight of the string $O$ in a [weighted automaton](/weighted-automaton/). Evaluating the product from the left is the forward algorithm, and from the right the backward pass.

## Applications

- **Classification.** Train one HMM per class, for example one per spoken word, and choose the class whose model gives the new sequence the largest likelihood.
- **Sequence family search.** A [profile HMM](/profile-hmm/) scores a protein sequence by its likelihood, compared with a background model.
- **Model selection and training.** The log-likelihood is the objective that [Baum-Welch](/baum-welch-algorithm/) increases, and the score that compares models with different numbers of states (see [HMM parameter learning](/hmm-parameter-learning/)).

## References
