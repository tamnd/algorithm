---
tag: T75G2W
kind: algorithm
slug: forward-algorithm
name: Forward algorithm
aliases:
- alpha recursion
- forward procedure for HMMs
area: machine-learning/probabilistic-inference
level: intro
summary: "Dynamic programming over time that computes the likelihood P(O) of an observation sequence under a hidden Markov model in O(T N^2) time."
solves: [hmm-evaluation]
model: real-ram
complexity:
  vars: {T: the length of the observation sequence, N: the number of hidden states}
  time: {worst: "Θ(T N^2)"}
  space: {extra: "Θ(T N)"}
properties: {deterministic: true, exact: true, online: true, recursive: false}
history:
  year: 1970
  people: [Leonard E. Baum, Ted Petrie, George Soules, Norman Weiss]
  note: The forward recursion appears in the work of Baum and his colleagues at the Institute for Defense Analyses on probabilistic functions of Markov chains, around 1967 to 1970. Rabiner's 1989 tutorial made its notation standard.
prereqs: [hidden-markov-model, hmm-evaluation]
see_also: [forward-backward-algorithm, viterbi-algorithm, baum-welch-algorithm, log-sum-exp-trick, filtering, hidden-semi-markov-model, dag-dynamic-programming, inside-outside-algorithm]
sources:
  - paper: doi:10.1109/5.18626
    title: Lawrence R. Rabiner, A tutorial on hidden Markov models and selected applications in speech recognition, Proceedings of the IEEE 77(2), 1989, pages 257 to 286
    locator: "Section III.A (Problem 1, the forward procedure and its cost) and Section V.A (scaling)"
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: "Section 13.2.2 (the alpha recursion) and Section 13.2.4 (scaling factors)"
  - book: isbn:9780262018029
    title: Kevin P. Murphy, Machine Learning, A Probabilistic Perspective, MIT Press, 2012
    locator: "Chapter 17, Section 17.4 (inference in HMMs, the forward algorithm)"
  - paper: doi:10.1214/aoms/1177697196
    title: Leonard E. Baum, Ted Petrie, George Soules and Norman Weiss, A maximization technique occurring in the statistical analysis of probabilistic functions of Markov chains, Annals of Mathematical Statistics 41(1), 1970, pages 164 to 171
    locator: the forward and backward quantities used to compute the re-estimation formulas
---

The forward algorithm computes the probability $P(O \mid \lambda)$ that a [hidden Markov model](/hidden-markov-model/) $\lambda = (\pi, A, B)$ emits a given observation sequence $O = o_1 \ldots o_T$. This is the [HMM evaluation](/hmm-evaluation/) problem. A direct sum over all $N^T$ hidden state paths is exponential in $T$, but the forward algorithm sums the paths one time step at a time and takes $\Theta(T N^2)$ time. It is the first half of the [forward-backward algorithm](/forward-backward-algorithm/), and its normalized form is exact [filtering](/filtering/) for a discrete HMM.

## In plain words

A hidden process moves between a few states, and at each step it shows you a symbol. You want the probability of the whole list of symbols that you saw. There are very many possible lists of hidden states, too many to try one by one.

The forward algorithm keeps one number for each state: the probability of the symbols seen so far, together with the event that the process is in that state now. To move one step ahead, each new number collects the old numbers of all states, weighted by the chance to move into the new state, and then multiplies by the chance that the new state shows the next symbol. At the end, the sum of the numbers is the answer. Long lists make the numbers tiny, so practical code rescales them at each step.

## The problem

The model has $N$ hidden states $1, \ldots, N$ and $M$ observation symbols $1, \ldots, M$. The parameters are the initial distribution $\pi_i = P(q_1 = i)$, the transition matrix $A_{ij} = P(q_{t+1} = j \mid q_t = i)$ and the emission matrix $B_j(k) = P(o_t = k \mid q_t = j)$. The query is the [marginal](/marginal-inference/) likelihood

$$P(O \mid \lambda) = \sum_{q_1, \ldots, q_T} \pi_{q_1} B_{q_1}(o_1) \prod_{t=2}^{T} A_{q_{t-1} q_t} B_{q_t}(o_t).$$

The forward variable is $\alpha_t(j) = P(o_1, \ldots, o_t, q_t = j \mid \lambda)$, the probability of the first $t$ observations and of state $j$ at time $t$. The page writes $T$ for the length of the sequence and $N$ for the number of states. The machine learning symbols $n$ and $d$ are not used.

## The algorithm

```pseudo id=main
FORWARD(π, A, B, o_1 .. o_T)
L1  for j ← 1 to N do α_1(j) ← π_j · B_j(o_1)
L2  for t ← 2 to T do
L3      for j ← 1 to N do
L4          s ← 0
L5          for i ← 1 to N do s ← s + α_{t−1}(i) · A_ij
L6          α_t(j) ← B_j(o_t) · s
L7  return α, Σ_j α_T(j)
```

Line L1 starts each state with the chance to begin there and to emit $o_1$. Lines L4 and L5 sum over the state $i$ at time $t-1$: each term is the probability of the first $t-1$ symbols with state $i$, times the chance to move from $i$ to $j$. Line L6 multiplies by the chance that $j$ emits $o_t$. So the recursion is

$$\alpha_t(j) = B_j(o_t) \sum_{i=1}^{N} \alpha_{t-1}(i) A_{ij}, \qquad P(O \mid \lambda) = \sum_{j=1}^{N} \alpha_T(j).$$

In floating point the $\alpha_t(j)$ shrink about geometrically in $t$ and underflow to zero after a few hundred steps. The scaled form (Rabiner, Section V.A) divides each row by its sum and keeps the logarithms of the sums:

```pseudo id=scaled
FORWARD-SCALED(π, A, B, o_1 .. o_T)
L8   ℓ ← 0; for t ← 1 to T do                ▷ at the end, ℓ = log P(O | λ)
L9       if t = 1 then for each j: a(j) ← π_j · B_j(o_1)
L10      else for each j: a(j) ← B_j(o_t) · Σ_i α̂_{t−1}(i) · A_ij
L11      n_t ← Σ_j a(j)                      ▷ n_t = P(o_t | o_1 .. o_{t−1})
L12      for each j: α̂_t(j) ← a(j) / n_t     ▷ α̂_t(j) = P(q_t = j | o_1 .. o_t)
L13      ℓ ← ℓ + log n_t
```

Rabiner's scale factor is $c_t = 1 / n_t$. A third form keeps $\log \alpha_t(j)$ and replaces the sum of line L5 by the [log-sum-exp trick](/log-sum-exp-trick/). It needs an exponential per term, so it is slower than scaling, but it also works when single entries of $A$ or $B$ are too small for a float.

## Example

Take $N = 2$ states, rain (R) and dry (D), and $M = 2$ symbols, umbrella (u) and no umbrella (n). Let $\pi = (1/2, 1/2)$,

$$A = \begin{pmatrix} 0.7 & 0.3 \\ 0.2 & 0.8 \end{pmatrix}, \qquad B = \begin{pmatrix} 0.9 & 0.1 \\ 0.2 & 0.8 \end{pmatrix},$$

with rows R, D and the columns of $B$ in the order u, n. The observations are $O = (u, u, n, u)$.

| $t$ | $o_t$ | $\alpha_t(R)$ | $\alpha_t(D)$ | $P(o_1 \ldots o_t)$ | $n_t$ | $\hat\alpha_t(R)$ |
|---|---|---|---|---|---|---|
| 1 | u | 0.45 | 0.1 | 0.55 | 0.55 | 0.8182 |
| 2 | u | 0.3015 | 0.043 | 0.3445 | 0.626364 | 0.8752 |
| 3 | n | 0.021965 | 0.09988 | 0.121845 | 0.353687 | 0.1803 |
| 4 | u | 0.03181635 | 0.0172987 | 0.04911505 | 0.403095 | 0.6478 |

For example, $\alpha_2(R) = 0.9 \cdot (0.45 \cdot 0.7 + 0.1 \cdot 0.2) = 0.9 \cdot 0.335 = 0.3015$. The answer is $P(O \mid \lambda) = 0.04911505 = 982301/20000000$, and $\log P(O \mid \lambda) = -3.013590$. The product of the column $n_t$ gives the same value. A sum over all $2^4 = 16$ state paths gives the same exact fraction.

## Correctness

The claim is $\alpha_t(j) = P(o_1, \ldots, o_t, q_t = j)$ for all $t$ and $j$, by induction on $t$. Line L1 is the case $t = 1$. For the step, split $P(o_{1:t}, q_t = j)$ by the value $i$ of $q_{t-1}$. The [conditional independences](/conditional-independence/) of the HMM give $P(q_t = j \mid q_{t-1} = i, o_{1:t-1}) = A_{ij}$ and $P(o_t \mid q_t = j, q_{t-1}, o_{1:t-1}) = B_j(o_t)$, which is line L6. The sum over $j$ at time $T$ is $P(O)$. For the scaled form, $\hat\alpha_t = \alpha_t / P(o_{1:t})$ and $n_t = P(o_{1:t}) / P(o_{1:t-1})$, so the sum of the $\log n_t$ telescopes to $\log P(O)$. The full proof is in the proofs file.

## Complexity

Each of the $T - 1$ steps of line L2 runs line L5 for $N^2$ pairs $(i, j)$ and line L6 for $N$ states. With line L1 this is $(T-1)(N^2 + N) + N$ multiplications and $(T-1) N (N-1) + (N - 1)$ additions, so the time is $\Theta(T N^2)$ in every case. The table $\alpha$ takes $\Theta(T N)$ space. If only $P(O)$ is needed, two rows suffice and the space is $\Theta(N)$. The scaled form adds $N$ divisions and one logarithm per step, so it is also $\Theta(T N^2)$.

The sum over paths costs $\Theta(T N^T)$: there are $N^T$ paths and each has $2T - 1$ factors. Rabiner (Section III.A) gives the scale of the difference: for $N = 5$ and $T = 100$ the direct sum needs about $10^{72}$ operations, the forward algorithm about 3000.

When $A$ is sparse with $m$ nonzero entries, line L5 needs only the nonzero $A_{ij}$, and the time is $\Theta(T (m + N))$. A left-to-right speech model has $m = O(N)$.

## Properties

- **Exact.** With exact arithmetic it returns $P(O \mid \lambda)$ itself, not an estimate.
- **Online.** Row $t$ needs only row $t-1$ and $o_t$, so the algorithm can run as the symbols arrive. The scaled row $\hat\alpha_t$ is the filtered distribution $P(q_t \mid o_{1:t})$.
- **A sum-product pass.** It is [belief propagation](/belief-propagation/) on a chain, with messages sent from left to right. Replace the sum of line L5 by a maximum and the result is the [Viterbi algorithm](/viterbi-algorithm/).
- **Shortest path view.** The values are path sums over a layered graph with $T$ layers of $N$ nodes, computed in [topological order](/dag-dynamic-programming/).

## Variants and improvements

- **Backward algorithm.** The mirror recursion $\beta_t(i) = \sum_j A_{ij} B_j(o_{t+1}) \beta_{t+1}(j)$ also gives $P(O)$, and with $\alpha$ it gives the posterior of each state: the [forward-backward algorithm](/forward-backward-algorithm/).
- **Continuous emissions.** Replace $B_j(o_t)$ by a density $b_j(o_t)$, for example a Gaussian or a mixture. The recursion does not change.
- **Explicit durations.** For a [hidden semi-Markov model](/hidden-semi-markov-model/), the recursion sums over the length of the last segment as well as its state.
- **Factored states.** For a [dynamic Bayesian network](/dynamic-bayesian-network/), the state is a vector of variables, and the frontier algorithm adds and removes one variable at a time instead of using the full product state.
- **Other structures.** The [inside-outside algorithm](/inside-outside-algorithm/) is the same idea for probabilistic context-free grammars, and the forward algorithm of a [weighted automaton](/weighted-automaton/) generalizes it to any semiring.

## When to use it

Use it whenever you need the likelihood of a sequence under a known HMM: to compare models (pick the word model with the largest likelihood, as in isolated word recognition), to score a sequence against a [profile HMM](/profile-hmm/), or to monitor the state online. For the most likely state path use Viterbi. For the posterior of every state use forward-backward. For long sequences always use the scaled or the log form.

## Pitfalls

- **Underflow.** The plain floats of line L6 reach zero for long sequences. In the test of the implementation, a model with three states and three symbols gives $\log P(O) = -2224.48$ for $T = 2000$. The plain recursion gives about $1.5 \times 10^{-291}$ after 600 symbols and exactly $0.0$ after 700, because a double cannot hold a value below about $4.9 \times 10^{-324}$. Use lines L8 to L13.
- **Logs of zero.** In the log form, $\log 0 = -\infty$. A log-sum-exp that subtracts the maximum must return $-\infty$ when all terms are $-\infty$, not NaN.
- **The emission at time 1.** Line L1 multiplies $\pi_j$ by $B_j(o_1)$. Code that starts with $\alpha_0 = \pi$ and then applies the step $T$ times also applies a transition before $o_1$, which is a different model.
- **The order of the indices.** $A_{ij}$ is the move from $i$ to $j$, so line L5 sums down column $j$. Swapping the indices gives wrong values that still look like probabilities.
- **Comparing likelihoods of different lengths.** $\log P(O)$ falls about linearly in $T$. Compare per-symbol values $\frac{1}{T} \log P(O)$ when the lengths differ.

## Implementations

## History

The forward recursion comes from the work of Leonard Baum and his coworkers at the Institute for Defense Analyses in Princeton on probabilistic functions of Markov chains, published from 1966 to 1972. It is the inner step of their re-estimation method (Baum, Petrie, Soules and Weiss 1970). Rabiner's 1989 tutorial stated the three basic problems of HMMs, wrote this solution of the first problem as the "forward procedure", and gave the scaling method in Section V.A.

## References
