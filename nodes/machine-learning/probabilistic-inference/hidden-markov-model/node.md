---
tag: A7E9ZX
kind: model
slug: hidden-markov-model
name: Hidden Markov model
aliases:
- HMM
area: machine-learning/probabilistic-inference
level: intro
summary: "A Markov chain of hidden states, each of which emits one observed symbol. The parameters are the start, transition and emission probabilities (pi, A, B)."
history:
  year: 1966
  people: [Leonard E. Baum, Ted Petrie]
  note: Baum and Petrie studied probabilistic functions of finite Markov chains at the Institute for Defense Analyses. In the 1970s Baker and Jelinek used the model for speech recognition.
prereqs: [markov-chain, conditional-independence]
see_also: [forward-algorithm, viterbi-algorithm, baum-welch-algorithm, hidden-semi-markov-model, dynamic-bayesian-network, stationary-distribution, profile-hmm, gaussian-mixture-model]
sources:
  - paper: doi:10.1214/aoms/1177699147
    title: Leonard E. Baum and Ted Petrie, Statistical inference for probabilistic functions of finite state Markov chains, Annals of Mathematical Statistics 37(6), 1966, pages 1554 to 1563
    locator: the model, and the consistency and asymptotic normality of the maximum likelihood estimate
  - paper: doi:10.1109/5.18626
    title: Lawrence R. Rabiner, A tutorial on hidden Markov models and selected applications in speech recognition, Proceedings of the IEEE 77(2), 1989, pages 257 to 286
    locator: "Section II (from Markov chains to HMMs, the elements (pi, A, B) and the three basic problems) and Section III (the solutions of the three problems)"
  - paper: "Frederick Jelinek, Continuous speech recognition by statistical methods, Proceedings of the IEEE 64(4):532-556, 1976"
    title: Jelinek 1976
    locator: the IBM statistical approach to speech recognition with Markov source models
  - paper: "James K. Baker, The DRAGON system, an overview, IEEE Transactions on Acoustics, Speech, and Signal Processing 23(1):24-29, 1975"
    title: Baker 1975
    locator: a speech recognizer built on a probabilistic network of Markov states
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: "Section 13.1 (Markov models) and Section 13.2 (hidden Markov models: the graph, the joint distribution and ancestral sampling)"
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: "Chapter 3 (Markov chains and hidden Markov models) and Chapter 5 (profile HMMs)"
---

A hidden Markov model (HMM) is a [Markov chain](/markov-chain/) whose states you cannot see. At each step the hidden state emits one symbol that you can see, with probabilities that depend only on that state. A discrete HMM with $N$ states and $M$ symbols has three parameters, written $\lambda = (\pi, A, B)$: the start probabilities $\pi$, the transition matrix $A$ and the emission matrix $B$. The probability of a state path together with an observation sequence is a product of one start term, $T - 1$ transition terms and $T$ emission terms. The three standard tasks on the model are [evaluation](/hmm-evaluation/), [decoding](/hmm-decoding/) and [parameter learning](/hmm-parameter-learning/), and each has an $O(T N^2)$ algorithm in place of a sum or maximum over $N^T$ paths.

## The machine

**Parameters.** There are states $1, \ldots, N$ and output symbols $1, \ldots, M$.

- $\pi_i = P(q_1 = i)$, the start distribution;
- $A_{ij} = P(q_{t+1} = j \mid q_t = i)$, an $N \times N$ matrix whose rows sum to 1;
- $B_j(k) = P(o_t = k \mid q_t = j)$, an $N \times M$ matrix whose rows sum to 1.

So the model has $(N - 1) + N (N - 1) + N (M - 1)$ free numbers. The same $A$ and $B$ are used at every step: the model is homogeneous in time. With continuous outputs, each row of $B$ is replaced by a density, for example a Gaussian or a [Gaussian mixture](/gaussian-mixture-model/).

**How it makes a sequence.** For a length $T$:

1. draw $q_1$ from $\pi$;
2. for $t = 1, \ldots, T$: draw $o_t$ from the row $B_{q_t}$, and if $t < T$ draw $q_{t+1}$ from the row $A_{q_t}$.

This is [ancestral sampling](/ancestral-sampling/) on the graph of the model, a chain $q_1 \to q_2 \to \cdots \to q_T$ with one edge $q_t \to o_t$ at each step. The implementation does exactly this, with a seeded `random.Random`.

**Two conditional independences.** The model makes two assumptions, and everything else follows from them.

1. *The hidden chain is Markov.* Given the present state, the next state does not depend on the earlier states or on any output so far: $P(q_{t+1} \mid q_1, \ldots, q_t, o_1, \ldots, o_t) = A_{q_t q_{t+1}}$.
2. *Each output depends only on its own state.* Given $q_t$, the output $o_t$ is independent of all other states and outputs: $P(o_t \mid q_1, \ldots, q_T, o_1, \ldots, o_{t-1}, o_{t+1}, \ldots, o_T) = B_{q_t}(o_t)$.

**The joint as a product.** By the chain rule and the two assumptions, for $Q = q_1 \ldots q_T$ and $O = o_1 \ldots o_T$,

$$P(Q, O \mid \lambda) = \pi_{q_1} B_{q_1}(o_1) \prod_{t=2}^{T} A_{q_{t-1} q_t} B_{q_t}(o_t),$$

and the likelihood of the outputs alone is the sum over all $N^T$ paths, $P(O \mid \lambda) = \sum_Q P(Q, O \mid \lambda)$. The tests check, in exact arithmetic, that this joint sums to 1 over all pairs $(Q, O)$ and that it has both conditional independences.

**Example.** Take the states rain (R) and dry (D) and the outputs umbrella (u) and none (n), with

$$\pi = (1/2, 1/2), \qquad A = \begin{pmatrix} 0.7 & 0.3 \\ 0.2 & 0.8 \end{pmatrix}, \qquad B = \begin{pmatrix} 0.9 & 0.1 \\ 0.2 & 0.8 \end{pmatrix}.$$

For $O = (u, u, n, u)$ and $Q = (R, R, R, R)$ the joint is $0.5 \cdot 0.9 \cdot (0.7 \cdot 0.9) \cdot (0.7 \cdot 0.1) \cdot (0.7 \cdot 0.9) = 0.01250235$. The sum over all $2^4 = 16$ paths gives $P(O) = 0.04911505$. The hidden chain has the [stationary distribution](/stationary-distribution/) $(0.4, 0.6)$. The outputs alone are not a Markov chain: $P(o_3 = u \mid o_1 = u, o_2 = u) = 0.6463$, but $P(o_3 = u \mid o_1 = n, o_2 = u) = 0.5525$, so $o_3$ depends on $o_1$ even when $o_2$ is known.

## What it counts

The size of a task is measured by $T$, the length of the sequence, $N$, the number of states, and $M$, the number of symbols. One step of an algorithm is one arithmetic operation on real numbers, as on the [real RAM](/real-ram/). A direct sum or maximum over all paths takes $\Theta(T N^T)$ steps. The useful algorithms exploit the chain structure: the factors of the joint that mention $q_t$ also mention only $q_{t-1}$ and $o_t$, so sums and maxima can be pushed inside the product one step at a time.

| Task | Question | Algorithm | Cost |
|---|---|---|---|
| [Evaluation](/hmm-evaluation/) | $P(O \mid \lambda)$ | [forward algorithm](/forward-algorithm/) | $\Theta(T N^2)$ |
| Filtering | $P(q_t \mid o_1, \ldots, o_t)$ | forward algorithm, normalized | $\Theta(T N^2)$ |
| Smoothing | $P(q_t \mid O)$ | [forward-backward algorithm](/forward-backward-algorithm/) | $\Theta(T N^2)$ |
| [Decoding](/hmm-decoding/) | $\arg\max_Q P(Q \mid O)$ | [Viterbi algorithm](/viterbi-algorithm/) | $\Theta(T N^2)$ |
| [Learning](/hmm-parameter-learning/) | $\arg\max_\lambda P(O \mid \lambda)$, locally | [Baum-Welch algorithm](/baum-welch-algorithm/) | $\Theta(T N^2)$ per round |

Sampling and computing the joint of one given pair each take $\Theta(T)$ steps (plus $\Theta(N + M)$ per draw for the inverse-CDF sampler).

## Relation to other models

- **Markov chain.** If $B$ is the identity, every state shows itself and the HMM is a plain Markov chain.
- **Mixture model.** If every row of $A$ equals $\pi$, the states are independent from step to step, and the outputs are independent draws from a mixture with weights $\pi$. A Gaussian HMM is thus a Gaussian mixture whose component labels follow a Markov chain.
- **Bayesian network.** The HMM is the [Bayesian network](/bayesian-network/) on the chain with emissions, unrolled for $T$ steps. It is the simplest [dynamic Bayesian network](/dynamic-bayesian-network/), with one discrete hidden variable and one observed variable per slice.
- **State-space model.** A [state-space model](/state-space-model/) has the same graph with continuous states. With linear Gaussian dynamics and outputs, the forward pass becomes the [Kalman filter](/kalman-filter/).
- **Hidden semi-Markov model.** In an HMM the time spent in state $i$ is geometric, $P(d) = A_{ii}^{d-1} (1 - A_{ii})$. A [hidden semi-Markov model](/hidden-semi-markov-model/) gives each state an explicit duration distribution.
- **Conditional random field.** A linear-chain [conditional random field](/conditional-random-field/) has the same chain shape but models $P(Q \mid O)$ directly instead of the joint.
- **Automata.** An HMM is a [probabilistic finite automaton](/probabilistic-finite-automaton/) whose outputs are tied to states. Biological sequence analysis uses special shapes: the [profile HMM](/profile-hmm/) for a family of sequences and the [pair HMM](/pair-hmm/) for the alignment of two sequences.

## Known results in the model

- **The three problems.** Rabiner's tutorial (Sections II and III) organizes the use of HMMs around evaluation, decoding and learning. The first two are solved exactly in $\Theta(T N^2)$ time by dynamic programming. The third is harder: the likelihood can have many local maxima, and Baum-Welch increases it in each round but in general stops at a local maximum.
- **Maximum likelihood is consistent.** For a finite state space and a finite output alphabet, Baum and Petrie (1966) proved that the maximum likelihood estimate of the parameters is consistent and asymptotically normal, under conditions that include positive parameters.
- **Identifiability up to a relabeling.** Any permutation of the states, applied to $\pi$, to the rows and columns of $A$ and to the rows of $B$, gives the same distribution of outputs. So the parameters can be recovered at best up to this relabeling.
- **Geometric durations.** The number of consecutive steps in state $i$ is geometric with mean $1 / (1 - A_{ii})$. In the example the mean stay is $10/3$ steps for R and 5 for D.
- **Long-run behavior.** If the hidden chain is irreducible and aperiodic, the distribution of $q_t$ tends to the stationary distribution of $A$, and the distribution of $o_t$ tends to that distribution times $B$.
- **The outputs are not Markov.** In general $P(o_t \mid o_1, \ldots, o_{t-1})$ depends on the whole past. The example above shows this for one step. This is why an HMM can model longer dependence than a Markov chain on the outputs, with few parameters.
- **Applications.** Baker's DRAGON system and Jelinek's group at IBM used HMMs for speech recognition in the 1970s. The same models are used for part-of-speech tagging, gene finding and protein family search, where profile HMMs model each family (Durbin et al., Chapter 5).

## References
