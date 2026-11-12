---
tag: AX7TK4
kind: problem
slug: hmm-decoding
name: HMM decoding
aliases:
- most likely state sequence
area: machine-learning/probabilistic-inference
level: intro
summary: "Find the hidden state path of highest probability given the observations of a hidden Markov model. A direct search has N^T paths; the Viterbi algorithm takes O(T N^2)."
prereqs: [hidden-markov-model]
see_also: [viterbi-algorithm, forward-backward-algorithm, hmm-evaluation, map-inference, max-product, maximum-likelihood-sequence-estimation, trellis, k-shortest-paths]
sources:
  - paper: doi:10.1109/5.18626
    title: Lawrence R. Rabiner, A tutorial on hidden Markov models and selected applications in speech recognition, Proceedings of the IEEE 77(2), 1989, pages 257 to 286
    locator: "Section II.C (Problem 2 of the three basic problems) and Section III.B (optimality criteria: the individually most likely states, which may not form a valid sequence, and the single best path found by the Viterbi algorithm)"
  - paper: doi:10.1109/PROC.1973.9030
    title: G. David Forney Jr., The Viterbi algorithm, Proceedings of the IEEE 61(3), 1973, pages 268 to 278
    locator: the most likely state sequence of a finite-state Markov process as a shortest path through a trellis
  - book: isbn:9780262018029
    title: Kevin P. Murphy, Machine Learning, A Probabilistic Perspective, MIT Press, 2012
    locator: "Section 17.4 (the most probable sequence of states, and the difference between MAP and max marginals)"
---

HMM decoding asks for the hidden state path that best explains an observation sequence $O = o_1 \ldots o_T$ under a [hidden Markov model](/hidden-markov-model/). The usual criterion is the single path of highest posterior probability, $\arg\max_Q P(Q \mid O, \lambda)$. It is the second of the three basic HMM problems in Rabiner's tutorial. There are $N^T$ paths, but the [Viterbi algorithm](/viterbi-algorithm/) finds the best one in $\Theta(T N^2)$ time.

## In plain words

You see the symbols, and you want to guess the hidden states that made them. One natural guess is the whole list of states that is most likely, taken together. You cannot try every list, because their number grows by a factor of $N$ with each step. But the best list that ends in a given state at a given step always extends a best list that ends one step earlier. So you can keep one best list per state and extend them step by step.

## Definition

**Input:** an HMM $\lambda = (\pi, A, B)$ with $N$ states and a sequence $O = o_1 \ldots o_T$ with $P(O \mid \lambda) > 0$.

**Output:** a path

$$Q^* \in \arg\max_{Q} P(Q \mid O, \lambda) = \arg\max_{Q} P(Q, O \mid \lambda),$$

where the two problems have the same solutions because $P(Q \mid O) = P(Q, O) / P(O)$ and $P(O)$ does not depend on $Q$. There may be several optimal paths; an algorithm states which one it returns.

## Variants

- **Posterior decoding.** Choose at each step the state with the largest $P(q_t = i \mid O)$. This maximizes the expected number of correct states, not the probability of the whole path. The resulting sequence can have probability zero. Rabiner (Section III.B) discusses this criterion.
- **The $k$ best paths.** Return the $k$ paths of highest probability, as in list decoding. This is a [$k$ shortest paths](/k-shortest-paths/) problem on the trellis.
- **Constrained decoding.** Fix some states in advance, or forbid some transitions, and find the best path that obeys the constraints.
- **Segment decoding.** In a [hidden semi-Markov model](/hidden-semi-markov-model/) the output is a list of segments, each with a state and a duration.

## Examples

In the rain (R) and dry (D) model of the HMM page, with $O = (u, u, n, u)$, the best path is R R R R with $P(Q, O) = 0.01250235$ and posterior $0.2546$. Posterior decoding gives R R D R, which has the posterior $0.2494$: a different answer, because R R D R has more expected correct states ($3.0136$ against $2.6308$).

The two criteria can disagree more strongly. With three states, $\pi = (0.4, 0.6, 0)$, the transition rows $(1, 0, 0)$, $(0, 0.5, 0.5)$ and $(0, 0, 1)$, one symbol, and $T = 2$, posterior decoding picks state 2 then state 1. The move from 2 to 1 has probability 0, so this sequence is impossible. The best path is state 1 then state 1, with probability $0.4$. The [forward-backward](/forward-backward-algorithm/) page tests this example.

## Known algorithms

| Algorithm | Criterion | Time | Space |
|---|---|---|---|
| Search of all paths | best path | $\Theta(T N^T)$ | $\Theta(T)$ |
| [Viterbi algorithm](/viterbi-algorithm/) | best path | $\Theta(T N^2)$ | $\Theta(T N)$ |
| [Forward-backward](/forward-backward-algorithm/), then the argmax at each step | most correct states | $\Theta(T N^2)$ | $\Theta(T N)$ |
| Beam search | best path, approximately | $\Theta(T N b)$ for beam width $b$ | $\Theta(T b)$ |

The Viterbi algorithm works in log space, so the scores do not underflow.

## Bounds

For a dense $A$, each step of an exact algorithm must in general look at all $N^2$ transitions, and the Viterbi algorithm uses $\Theta(T N^2)$ time. With $E$ nonzero transitions it takes $\Theta(T (N + E))$ time. Storing the backpointers takes $\Theta(T N)$ space; checkpointing trades space for a second pass.

## Reductions

- **To a shortest path.** Give each edge of the [trellis](/trellis/) from $(t - 1, i)$ to $(t, j)$ the length $-\log A_{ij} - \log B_j(o_t)$. The best path is a shortest path through this acyclic graph (Forney 1973).
- **To MAP inference.** HMM decoding is [MAP inference](/map-inference/) in a chain-shaped Bayesian network, and the Viterbi algorithm is [max-product](/max-product/) message passing on that chain.
- **In communications.** When the hidden states are the states of a channel or a convolutional encoder, the same problem is [maximum-likelihood sequence estimation](/maximum-likelihood-sequence-estimation/).

## Applications

- **Speech recognition.** The best path through a large HMM built from word and phone models gives the recognized words.
- **Tagging and segmentation.** Part-of-speech tagging and gene finding assign one label to each position of a sequence.
- **Decoding codes.** The best path through the trellis of a convolutional code gives the most likely sent bits.

## References
