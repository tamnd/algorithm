---
tag: JYNY94
kind: algorithm
slug: forward-backward-algorithm
name: Forward-backward algorithm
aliases:
- forward-backward procedure
area: machine-learning/probabilistic-inference
level: core
summary: "Two passes over a hidden Markov model, one forward and one backward, that give the posterior of each hidden state and of each pair of neighbors in O(T N^2) time."
solves: [smoothing, marginal-inference]
model: real-ram
complexity:
  vars: {T: the length of the observation sequence, N: the number of hidden states}
  time: {worst: "Θ(T N^2)"}
  space: {extra: "Θ(T N)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1970
  people: [Leonard E. Baum, Ted Petrie, George Soules, Norman Weiss]
  note: Baum and his colleagues at the Institute for Defense Analyses used the forward and backward quantities to get the expected counts of their re-estimation method. Bahl, Cocke, Jelinek and Raviv used the same recursion for codes in 1974.
prereqs: [forward-algorithm, hidden-markov-model]
see_also: [viterbi-algorithm, baum-welch-algorithm, smoothing, bcjr-algorithm, symbol-by-symbol-map-decoding, rauch-tung-striebel-smoother, belief-propagation, inside-outside-algorithm]
sources:
  - paper: doi:10.1109/5.18626
    title: Lawrence R. Rabiner, A tutorial on hidden Markov models and selected applications in speech recognition, Proceedings of the IEEE 77(2), 1989, pages 257 to 286
    locator: "Section III.A (the backward procedure), Section III.B (the individually most likely states and why they may not form a valid sequence), Section III.C (the pair posteriors) and Section V.A (scaling)"
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: "Section 13.2.2 (the forward-backward algorithm) and Section 13.2.4 (scaling factors)"
  - book: isbn:9780262018029
    title: Kevin P. Murphy, Machine Learning, A Probabilistic Perspective, MIT Press, 2012
    locator: "Chapter 17, Section 17.4 (inference in HMMs: the forward-backward algorithm, and the difference between MAP and max marginals)"
  - paper: doi:10.1214/aoms/1177697196
    title: Leonard E. Baum, Ted Petrie, George Soules and Norman Weiss, A maximization technique occurring in the statistical analysis of probabilistic functions of Markov chains, Annals of Mathematical Statistics 41(1), 1970, pages 164 to 171
    locator: the forward and backward quantities used to compute the re-estimation formulas
  - paper: doi:10.1109/TIT.1974.1055186
    title: Lalit R. Bahl, John Cocke, Frederick Jelinek and Josef Raviv, Optimal decoding of linear codes for minimizing symbol error rate, IEEE Transactions on Information Theory 20(2), 1974, pages 284 to 287
    locator: the same two-pass recursion on a code trellis
---

The forward-backward algorithm computes, for a [hidden Markov model](/hidden-markov-model/) and an observation sequence $O = o_1 \ldots o_T$, the posterior $\gamma_t(i) = P(q_t = i \mid O)$ of each hidden state at each time, and the posterior $\xi_t(i, j) = P(q_t = i, q_{t+1} = j \mid O)$ of each pair of neighbors. It runs the [forward algorithm](/forward-algorithm/) from left to right and a backward recursion from right to left, and multiplies the two results, in $\Theta(T N^2)$ time. For a discrete HMM this is exact fixed-interval [smoothing](/smoothing/), and its outputs are the expected counts that the [Baum-Welch algorithm](/baum-welch-algorithm/) needs.

## In plain words

A hidden process moves between a few states and shows one symbol per step. After you have seen the whole list of symbols, you ask: how likely was each state at each step? The answer at one step depends on the symbols before it and on the symbols after it.

The forward pass, from the first step to the last, gives for each state the weight of everything seen up to now. The backward pass, from the last step to the first, gives for each state the weight of everything still to come. At each step, multiply the two weights of each state and divide by the total. The same product, taken over two neighboring steps, gives the chance of each move between states.

## The problem

The model is an HMM $\lambda = (\pi, A, B)$ with $N$ states, with $\pi_i = P(q_1 = i)$, $A_{ij} = P(q_{t+1} = j \mid q_t = i)$ and $B_j(k) = P(o_t = k \mid q_t = j)$. The input is $O$ with $P(O) > 0$. The query is the [marginal](/marginal-inference/) posterior of each single state and of each pair of neighbors:

$$\gamma_t(i) = P(q_t = i \mid O), \quad 1 \le t \le T, \qquad \xi_t(i, j) = P(q_t = i, q_{t+1} = j \mid O), \quad 1 \le t < T.$$

The page writes $T$ for the length and $N$ for the number of states; the symbols $n$ and $d$ of other machine learning pages are not used.

## The algorithm

The forward variable is $\alpha_t(i) = P(o_1, \ldots, o_t, q_t = i)$, from the forward algorithm. The backward variable is $\beta_t(i) = P(o_{t+1}, \ldots, o_T \mid q_t = i)$, with $\beta_T(i) = 1$.

```pseudo id=main
FORWARD-BACKWARD(π, A, B, o_1 .. o_T)
L1  run FORWARD to get α_t(j) for all t and j; P ← Σ_j α_T(j)
L2  for i ← 1 to N do β_T(i) ← 1
L3  for t ← T − 1 downto 1 do
L4      for i ← 1 to N do
L5          β_t(i) ← Σ_j A_ij · B_j(o_{t+1}) · β_{t+1}(j)
L6  for each t and i: γ_t(i) ← α_t(i) · β_t(i) / P
L7  for each t < T and i, j: ξ_t(i, j) ← α_t(i) · A_ij · B_j(o_{t+1}) · β_{t+1}(j) / P
L8  return γ, ξ
```

Line L5 is the backward recursion. It looks one step ahead: from state $i$ at time $t$, move to $j$, emit $o_{t+1}$ from $j$, and then emit the rest from $j$. Line L6 joins the past and the future of state $i$ at time $t$. Line L7 joins the past of $i$ at time $t$, the move $i \to j$ with its emission, and the future of $j$ at time $t+1$.

**Scaling.** For long sequences use the normalized forward rows $\hat\alpha_t(i) = \alpha_t(i) / P(o_{1:t})$ with the step factors $n_t = P(o_t \mid o_{1:t-1})$, as on the forward algorithm page, and divide each backward row by the factor of the next step:

$$\hat\beta_T(i) = 1, \qquad \hat\beta_t(i) = \frac{1}{n_{t+1}} \sum_j A_{ij} B_j(o_{t+1}) \hat\beta_{t+1}(j).$$

Then $\gamma_t(i) = \hat\alpha_t(i) \hat\beta_t(i)$ and $\xi_t(i, j) = \hat\alpha_t(i) A_{ij} B_j(o_{t+1}) \hat\beta_{t+1}(j) / n_{t+1}$, with no division by $P$, and $\log P(O) = \sum_t \log n_t$.

## Example

Use the rain (R) and dry (D) model of the forward algorithm page: $\pi = (1/2, 1/2)$, $A = \begin{pmatrix} 0.7 & 0.3 \\ 0.2 & 0.8 \end{pmatrix}$, $B = \begin{pmatrix} 0.9 & 0.1 \\ 0.2 & 0.8 \end{pmatrix}$ with the symbols umbrella (u) and none (n), and $O = (u, u, n, u)$. Then $P(O) = 0.04911505$.

| $t$ | $o_t$ | $\alpha_t(R)$ | $\alpha_t(D)$ | $\beta_t(R)$ | $\beta_t(D)$ | $\gamma_t(R)$ | $\gamma_t(D)$ |
|---|---|---|---|---|---|---|---|
| 1 | u | 0.45 | 0.1 | 0.095721 | 0.060406 | 0.8770 | 0.1230 |
| 2 | u | 0.3015 | 0.043 | 0.1299 | 0.2314 | 0.7974 | 0.2026 |
| 3 | n | 0.021965 | 0.09988 | 0.69 | 0.34 | 0.3086 | 0.6914 |
| 4 | u | 0.03181635 | 0.0172987 | 1 | 1 | 0.6478 | 0.3522 |

For example, $\beta_3(R) = 0.7 \cdot 0.9 + 0.3 \cdot 0.2 = 0.69$ and $\gamma_3(D) = 0.09988 \cdot 0.34 / 0.04911505 = 0.6914$. The pair posteriors from $t = 2$ to $t = 3$ are $\xi_2(R, R) = 0.2965$, $\xi_2(R, D) = 0.5009$, $\xi_2(D, R) = 0.0121$ and $\xi_2(D, D) = 0.1905$. Their row sums are $\gamma_2(R)$ and $\gamma_2(D)$.

The state with the largest $\gamma_t$ at each step gives the sequence R R D R. Its posterior probability is $0.2494$. The single most likely path, from the [Viterbi algorithm](/viterbi-algorithm/), is R R R R with posterior $0.2546$. The two answers differ: R R D R has more expected correct states ($3.0136$ against $2.6308$), and R R R R is the more likely whole path.

## Correctness

Write the joint as a product, $P(Q, O) = \pi_{q_1} B_{q_1}(o_1) \prod_{s=2}^{T} A_{q_{s-1} q_s} B_{q_s}(o_s)$. Fix $q_t = i$. The factors with $s \le t$ involve only $q_1, \ldots, q_t$, and the factors with $s > t$ involve only $q_t, \ldots, q_T$. So by the distributive law, the sum of $P(Q, O)$ over all paths with $q_t = i$ is the sum of the first part, which is $\alpha_t(i)$, times the sum of the second part, which is $\beta_t(i)$. This gives $P(q_t = i, O) = \alpha_t(i) \beta_t(i)$ and line L6. Fixing $q_t = i$ and $q_{t+1} = j$ splits the product into three parts in the same way, which gives line L7. Line L5 is correct by induction from $t = T$ down. The full proof, with the scaled form, is in the proofs file.

## Complexity

The forward pass and the backward pass each do $N^2$ products and sums per step, so each takes $\Theta(T N^2)$ time. Line L6 takes $\Theta(T N)$ and line L7 takes $\Theta(T N^2)$. The total is $\Theta(T N^2)$ time in every case.

The tables $\alpha$ and $\beta$ take $\Theta(T N)$ space. If all $\xi_t$ are stored, they take $\Theta(T N^2)$ more. Baum-Welch needs only $\sum_t \xi_t(i, j)$, so it can add each $\xi_t$ to an $N \times N$ total as soon as it is computed. With checkpoints (keep every $\lceil \sqrt T \rceil$-th forward row and recompute the rows between two checkpoints during the backward pass) the space drops to $\Theta(N \sqrt T)$ at the cost of a second forward pass.

## Properties

- **Exact.** With exact arithmetic the outputs are the true posteriors. The tests check them against a sum over all $N^T$ paths.
- **Not online.** Each $\gamma_t$ depends on all of $O$, so the algorithm needs the full sequence. Fixed-lag smoothing runs the backward pass over a window of the last few steps instead.
- **Consistent marginals.** $\sum_j \xi_t(i, j) = \gamma_t(i)$ and $\sum_i \xi_t(i, j) = \gamma_{t+1}(j)$.
- **Sum-product on a chain.** The algorithm is [belief propagation](/belief-propagation/) on the chain of the HMM: $\alpha$ holds the messages from the left and $\beta$ the messages from the right.
- **Same recursion in coding.** The [BCJR algorithm](/bcjr-algorithm/) of Bahl, Cocke, Jelinek and Raviv (1974) is this recursion on a code [trellis](/trellis/), where it gives the posterior of each bit for [symbol-by-symbol MAP decoding](/symbol-by-symbol-map-decoding/).

## Variants and improvements

- **Posterior decoding.** Choose $\hat q_t = \arg\max_i \gamma_t(i)$ at each step. This maximizes the expected number of correct states, but the sequence need not be a possible path (see Pitfalls). The [Viterbi algorithm](/viterbi-algorithm/) maximizes the probability of the whole path instead.
- **Log space.** Keep $\log \alpha$ and $\log \beta$ and use the [log-sum-exp trick](/log-sum-exp-trick/). This is slower than scaling but safe when single parameters are very small.
- **Linear Gaussian models.** With continuous Gaussian states the same two passes are the [Kalman filter](/kalman-filter/) and the [Rauch-Tung-Striebel smoother](/rauch-tung-striebel-smoother/).
- **Grammars.** The [inside-outside algorithm](/inside-outside-algorithm/) is the analog for probabilistic context-free grammars.
- **Factored and semi-Markov models.** A [dynamic Bayesian network](/dynamic-bayesian-network/) or a [hidden semi-Markov model](/hidden-semi-markov-model/) has its own forward and backward passes with the same structure.

## When to use it

Use it to get the uncertainty of each hidden state after the whole sequence is known: for smoothing, for the E step of Baum-Welch, for confidence values on each label, and for posterior decoding when the score is the number of correct labels. When you need one consistent path, use Viterbi. When the states arrive online and you need only the present state, the forward pass alone (filtering) is enough.

## Pitfalls

- **Posterior decoding can give an impossible path.** Take three states and one symbol, $\pi = (0.4, 0.6, 0)$, rows $A_1 = (1, 0, 0)$, $A_2 = (0, 0.5, 0.5)$, $A_3 = (0, 0, 1)$, and $T = 2$. The paths $(1, 1)$, $(2, 2)$ and $(2, 3)$ have the probabilities $0.4$, $0.3$ and $0.3$. So $\gamma_1 = (0.4, 0.6, 0)$ and $\gamma_2 = (0.4, 0.3, 0.3)$, and the argmax sequence is $(2, 1)$, which uses $A_{21} = 0$ and has probability zero. Viterbi returns $(1, 1)$ with probability $0.4$. Rabiner (Section III.B) points out this problem.
- **Scaling the backward pass with the wrong factor.** $\hat\beta_t$ must be divided by $n_{t+1}$, the factor of the next step, and $\xi_t$ needs the extra $1/n_{t+1}$. With $n_t$ in place of $n_{t+1}$, each $\hat\beta_t$ is off by the factor $n_T / n_t$, so $\gamma_t$ is wrong by that factor and in general its entries no longer sum to 1.
- **Forgetting the emission in line L5.** $\beta_t(i)$ needs $B_j(o_{t+1})$ inside the sum. Without it, $\alpha_t \beta_t$ does not depend on the future symbols.
- **A sequence of probability zero.** Then $P = 0$ and lines L6 and L7 divide by zero. Check $P > 0$ first; the implementation raises an error.

## Implementations

## History

Baum and his coworkers at the Institute for Defense Analyses in Princeton used the forward and backward quantities in the late 1960s to compute the expected counts of their re-estimation method for probabilistic functions of Markov chains (Baum, Petrie, Soules and Weiss 1970). Bahl, Cocke, Jelinek and Raviv (1974) used the same recursion to decode linear and convolutional codes with the least bit error rate. Rabiner's 1989 tutorial made the notation $\alpha$, $\beta$, $\gamma$ and $\xi$ standard and gave the scaling method.

## References
