---
tag: KSAB3R
kind: algorithm
slug: viterbi-algorithm
name: Viterbi algorithm
aliases:
- Viterbi decoding
- Viterbi path algorithm
area: machine-learning/probabilistic-inference
level: core
summary: "Dynamic programming that finds the single most likely hidden state path of a hidden Markov model, or the most likely path through a code trellis, in O(T N^2) time."
solves: [hmm-decoding, maximum-likelihood-sequence-estimation]
model: real-ram
complexity:
  vars: {T: the length of the observation sequence, N: the number of hidden states}
  time: {worst: "Θ(T N^2)"}
  space: {extra: "Θ(T N)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1967
  people: [Andrew J. Viterbi, G. David Forney Jr.]
  note: Viterbi gave the algorithm in 1967 to decode convolutional codes. Forney showed in 1973 that it finds a shortest path through a trellis and that it is maximum likelihood sequence estimation.
prereqs: [hidden-markov-model, hmm-decoding, dag-shortest-paths]
see_also: [forward-algorithm, forward-backward-algorithm, max-product, map-inference, trellis, convolutional-code, traceback, dag-dynamic-programming]
sources:
  - paper: doi:10.1109/TIT.1967.1054010
    title: Andrew J. Viterbi, Error bounds for convolutional codes and an asymptotically optimum decoding algorithm, IEEE Transactions on Information Theory 13(2), 1967, pages 260 to 269
    locator: the decoding algorithm for convolutional codes and its asymptotic optimality
  - paper: doi:10.1109/PROC.1973.9030
    title: G. David Forney Jr., The Viterbi algorithm, Proceedings of the IEEE 61(3), 1973, pages 268 to 278
    locator: the algorithm as a shortest path through a trellis, its maximum likelihood property, and its applications
  - paper: "Jim K. Omura, On the Viterbi decoding algorithm, IEEE Transactions on Information Theory 15(1), 1969, pages 177 to 179"
    title: Omura 1969
    locator: the Viterbi algorithm as forward dynamic programming
  - paper: doi:10.1109/5.18626
    title: Lawrence R. Rabiner, A tutorial on hidden Markov models and selected applications in speech recognition, Proceedings of the IEEE 77(2), 1989, pages 257 to 286
    locator: "Section III.B (Problem 2, the optimal state sequence and the Viterbi algorithm, with the log form)"
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: "Section 13.2.5 (the Viterbi algorithm) and Section 8.4.5 (the max-sum algorithm)"
---

The Viterbi algorithm finds the single most likely sequence of hidden states $Q^* = \arg\max_Q P(Q \mid O)$ of a [hidden Markov model](/hidden-markov-model/) for an observation sequence $O = o_1 \ldots o_T$, which is the [HMM decoding](/hmm-decoding/) problem. It is [dynamic programming](/dag-dynamic-programming/) over time: for each time and state it keeps the score of the best path that ends there and a pointer to its previous state, and it reads the answer back along the pointers, in $\Theta(T N^2)$ time. Viterbi (1967) gave it to decode [convolutional codes](/convolutional-code/), and Forney (1973) showed that it finds a [shortest path](/dag-shortest-paths/) through a [trellis](/trellis/) and so solves [maximum likelihood sequence estimation](/maximum-likelihood-sequence-estimation/).

## In plain words

A hidden process moves between a few states and shows one symbol per step. You saw the symbols and want the one list of hidden states that best explains them.

There are far too many lists to try. But the best list that ends in a given state at a given step must start with the best list that ends in some state one step earlier. So for each step and each state, keep only the best score so far and remember which earlier state it came from. Move forward step by step. At the end, take the state with the best score and follow the remembered links back to the start. Scores are kept as sums of logarithms, so long inputs do not shrink them to zero.

## The problem

The model is an HMM $\lambda = (\pi, A, B)$ with $N$ states: $\pi_i = P(q_1 = i)$, $A_{ij} = P(q_{t+1} = j \mid q_t = i)$, $B_j(k) = P(o_t = k \mid q_t = j)$. The query is a [MAP](/map-inference/) assignment of all the hidden variables:

$$Q^* \in \arg\max_{q_1, \ldots, q_T} P(q_1, \ldots, q_T, O) = \arg\max_{q_1, \ldots, q_T} \Bigl[ \log \pi_{q_1} + \log B_{q_1}(o_1) + \sum_{t=2}^{T} \bigl( \log A_{q_{t-1} q_t} + \log B_{q_t}(o_t) \bigr) \Bigr].$$

Since $P(O)$ does not depend on $Q$, maximizing the joint is the same as maximizing the posterior $P(Q \mid O)$. We write $T$ for the length and $N$ for the number of states, and $\log 0 = -\infty$.

## The algorithm

The score $\delta_t(j)$ is the largest log probability of a path $q_1 \ldots q_t$ with $q_t = j$, together with $o_1 \ldots o_t$. The backpointer $\psi_t(j)$ is the state at time $t - 1$ on such a path.

```pseudo id=main
VITERBI(π, A, B, o_1 .. o_T)                      ▷ log space, log 0 = −∞
L1  for j ← 1 to N do δ_1(j) ← log π_j + log B_j(o_1)
L2  for t ← 2 to T do
L3      for j ← 1 to N do
L4          ψ_t(j) ← the smallest i that maximizes δ_{t−1}(i) + log A_ij
L5          δ_t(j) ← δ_{t−1}(ψ_t(j)) + log A_{ψ_t(j) j} + log B_j(o_t)
L6  q_T ← the smallest j that maximizes δ_T(j)
L7  for t ← T − 1 downto 1 do q_t ← ψ_{t+1}(q_{t+1})
L8  return q_1 .. q_T and δ_T(q_T)
```

Lines L1 to L5 are the [forward algorithm](/forward-algorithm/) with the sum replaced by a maximum, in log space, where products become sums. Line L4 stores the winner of each maximum. Line L6 picks the best final state, and line L7 is the [traceback](/traceback/): it follows the stored pointers from the end to the start. If $\delta_T(q_T) = -\infty$, every path has probability zero and there is no answer; the implementation raises an error.

**Tie rule.** Lines L4 and L6 take the smallest index among the maximizers. Then the output is the optimal path whose reversed sequence $(q_T, q_{T-1}, \ldots, q_1)$ is the smallest in lexicographic order. The tests compare the output, ties included, with a brute force search over all $N^T$ paths that uses this rule.

**The shortest path view.** Build a layered graph with a source $s$, one node $(t, j)$ for each time $t$ and state $j$, and a sink. Give the edge $s \to (1, j)$ the length $-\log \pi_j - \log B_j(o_1)$, the edge $(t-1, i) \to (t, j)$ the length $-\log A_{ij} - \log B_j(o_t)$, and each edge $(T, j) \to$ sink the length 0. A path from $s$ to the sink is a state sequence, and its length is $-\log P(Q, O)$. So $Q^*$ is a shortest path in this directed acyclic graph, and lines L1 to L5 relax the edges in [topological order](/dag-shortest-paths/). This is Forney's view (1973). For a code, the graph is the code [trellis](/trellis/) and the lengths come from the channel.

## Example

Use the rain (R) and dry (D) model of the forward algorithm page: $\pi = (1/2, 1/2)$, $A = \begin{pmatrix} 0.7 & 0.3 \\ 0.2 & 0.8 \end{pmatrix}$, $B = \begin{pmatrix} 0.9 & 0.1 \\ 0.2 & 0.8 \end{pmatrix}$ with the symbols umbrella (u) and none (n), and $O = (u, u, n, u)$. The table gives $e^{\delta_t(j)}$, the probability of the best path into each state.

| $t$ | $o_t$ | best into R | $\psi_t(R)$ | best into D | $\psi_t(D)$ |
|---|---|---|---|---|---|
| 1 | u | 0.45 | | 0.1 | |
| 2 | u | 0.2835 | R | 0.027 | R |
| 3 | n | 0.019845 | R | 0.06804 | R |
| 4 | u | 0.01250235 | R | 0.0108864 | D |

At $t = 4$ the score of R compares $0.019845 \cdot 0.7 = 0.0138915$ (from R) with $0.06804 \cdot 0.2 = 0.013608$ (from D), so $\psi_4(R) = R$ and the value is $0.0138915 \cdot 0.9 = 0.01250235$. Line L6 takes R, and the traceback gives R, R, R, R. The best path has $P(Q^*, O) = 0.01250235$ and $\log P(Q^*, O) = -4.38184$. Its posterior is $0.01250235 / 0.04911505 = 0.2546$.

The next best path is R R D R with $P = 0.0122472$. It is also the sequence of the states with the largest posterior at each step, from the [forward-backward algorithm](/forward-backward-algorithm/). The two decoders answer different questions, and here they disagree at $t = 3$.

## Correctness

The invariant is: after the pass of line L2 for time $t$, $\delta_t(j)$ is the maximum of $\log P(q_1, \ldots, q_t, o_1, \ldots, o_t)$ over the paths with $q_t = j$, and $\psi_t(j)$ is a state at time $t-1$ on such a path. The proof is by induction on $t$ and uses the [principle of optimality](/principle-of-optimality/): the log joint of a path that ends with $i \to j$ at time $t$ is the log joint of its prefix plus $\log A_{ij} + \log B_j(o_t)$, so the best path into $j$ extends a best path into some $i$. The traceback then rebuilds an optimal path, and an induction from $t = T$ down shows that it is the one chosen by the tie rule. The full proof is in the proofs file.

## Complexity

Line L4 looks at $N$ candidates for each of the $N$ states at each of the $T - 1$ steps, so the time is $\Theta(T N^2)$ in every case: $(T-1) N^2$ additions and comparisons for the maxima, plus $\Theta(T N)$ for line L5 and $\Theta(T)$ for the traceback. The backpointers take $\Theta(T N)$ space, and the scores need only two rows, $\Theta(N)$. The brute force search has $N^T$ paths, so it takes $\Theta(T N^T)$ time.

With a sparse transition matrix of $m$ nonzero entries, line L4 needs only the nonzero $A_{ij}$, and the time is $\Theta(T (m + N))$. In coding, $N = 2^\nu$ for a code with memory $\nu$ and each state has 2 successors for a rate $1/n$ code, so the work grows linearly in the length and exponentially in the memory.

## Properties

- **Exact.** It returns a path of the largest probability, not an approximation.
- **Max-product on a chain.** It is the [max-product](/max-product/) algorithm on the chain of the HMM, done in log space as max-sum. The forward algorithm is the sum-product version of the same recursion.
- **A consistent path.** The output always has positive probability when $P(O) > 0$. The sequence of per-step posterior maxima does not have this property: in the example on the [forward-backward algorithm](/forward-backward-algorithm/) page, with three states, it uses a transition of probability zero, while Viterbi returns a path of probability $0.4$.
- **Not online.** The traceback needs the end of the sequence. Decoders of codes on long streams fix a decision depth instead (see [convolutional code](/convolutional-code/)).
- **Free of underflow.** Log space turns products into sums, so no scaling is needed.

## Variants and improvements

- **Coding use.** On the [trellis](/trellis/) of a [convolutional code](/convolutional-code/) the same recursion is the [maximum likelihood](/maximum-likelihood-decoding/) sequence decoder. The coding pages give the branch metrics, the decision depth and the error bounds.
- **List Viterbi.** Keep the $k$ best scores per state and get the $k$ best paths. This is the [k shortest paths](/k-shortest-paths/) problem on the trellis.
- **Beam pruning.** Keep only the states whose score is near the best one at each step. Large speech recognizers do this. It is fast, but the result is no longer guaranteed optimal.
- **Viterbi training.** Replace the expected counts of [Baum-Welch](/baum-welch-algorithm/) by the counts along the Viterbi path. This is a hard version of EM, and it maximizes the joint of the best path, not the likelihood.
- **Other models.** The same recursion decodes a [hidden semi-Markov model](/hidden-semi-markov-model/) (with a maximum over durations), a linear chain [conditional random field](/conditional-random-field/), and a [profile HMM](/profile-hmm/).

## When to use it

Use Viterbi when you need one consistent labeling of the whole sequence: a word sequence in speech recognition, a gene structure in a genome, the bits of a convolutional code. Use [posterior decoding](/forward-backward-algorithm/) instead when the score is the number of correct labels at single positions, or when you need a confidence for each label. Use the [forward algorithm](/forward-algorithm/) when you need the probability of the observations, which sums over all paths instead of taking the best one.

## Pitfalls

- **Products in floating point.** Without logs, the scores of line L5 underflow to zero after a few hundred steps, and then all states tie. Work in log space, or rescale each row.
- **Ties.** With exact ties, different implementations return different optimal paths. State the rule (here, the smallest index in lines L4 and L6) and test it. With floats, two equal products can also differ in the last bit, so tests should compare path probabilities, not paths.
- **Taking the maximum over $j$ of $\delta_t(j)$ at each step.** This greedy choice does not give the best path. Only the final maximum of line L6 and the traceback of line L7 do.
- **Mixing it up with posterior decoding.** The path of the largest joint probability and the sequence of the largest marginals are different objects, and the second may be impossible.
- **Zeros in log space.** $\log 0 = -\infty$ must compare below every finite score. If every path has probability zero, there is no best path; report that instead of returning an arbitrary path.

## Implementations

## History

Andrew Viterbi published the algorithm in 1967 in a paper on error bounds for convolutional codes, where it served as a decoder that is asymptotically optimum. Jim Omura pointed out in 1969 that it is forward dynamic programming. G. David Forney's 1973 survey showed that it finds the shortest path through a trellis and that it gives the maximum likelihood estimate of the state sequence of a finite state Markov process seen through memoryless noise, which made it a standard tool beyond coding. Rabiner's 1989 tutorial gave its HMM form, with the log variant, as the solution of the second basic problem of HMMs.

## References
