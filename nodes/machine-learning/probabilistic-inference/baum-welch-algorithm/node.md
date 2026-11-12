---
tag: X13Y7R
kind: algorithm
slug: baum-welch-algorithm
name: Baum-Welch algorithm
aliases:
- forward-backward EM for HMMs
- Baum-Welch re-estimation
area: machine-learning/probabilistic-inference
level: core
summary: "Expectation-maximization for the parameters of a hidden Markov model: expected counts from forward-backward, then normalized counts. The likelihood never decreases."
solves: [hmm-parameter-learning]
model: real-ram
complexity:
  vars: {K: the number of rounds, T: the total number of observed symbols, N: the number of hidden states, M: the number of output symbols}
  time: {worst: "Θ(K (T N^2 + N M))"}
  space: {extra: "Θ(T N + N^2 + N M)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1970
  people: [Leonard E. Baum, Ted Petrie, George Soules, Norman Weiss]
  note: Baum and his colleagues at the Institute for Defense Analyses proved that the re-estimation step increases the likelihood of a probabilistic function of a Markov chain. Dempster, Laird and Rubin later showed that it is a case of the EM algorithm.
prereqs: [forward-backward-algorithm, expectation-maximization, hmm-parameter-learning]
see_also: [hidden-markov-model, forward-algorithm, viterbi-algorithm, gaussian-mixture-model, maximum-likelihood-estimation, jensens-inequality, inside-outside-algorithm, hidden-semi-markov-model]
sources:
  - paper: doi:10.1214/aoms/1177697196
    title: Leonard E. Baum, Ted Petrie, George Soules and Norman Weiss, A maximization technique occurring in the statistical analysis of probabilistic functions of Markov chains, Annals of Mathematical Statistics 41(1), 1970, pages 164 to 171
    locator: the re-estimation transformation and the proof that it does not decrease the likelihood
  - paper: doi:10.1109/5.18626
    title: Lawrence R. Rabiner, A tutorial on hidden Markov models and selected applications in speech recognition, Proceedings of the IEEE 77(2), 1989, pages 257 to 286
    locator: "Section III.C (the re-estimation formulas and the auxiliary function), Section V.A (scaling) and Section V.B (multiple observation sequences)"
  - paper: "A. P. Dempster, N. M. Laird and D. B. Rubin, Maximum likelihood from incomplete data via the EM algorithm, Journal of the Royal Statistical Society, Series B 39(1):1-38, 1977"
    title: Dempster, Laird and Rubin 1977
    locator: the general EM algorithm and its monotone likelihood
  - paper: "C. F. Jeff Wu, On the convergence properties of the EM algorithm, Annals of Statistics 11(1):95-103, 1983"
    title: Wu 1983
    locator: conditions under which the limit points of EM are stationary points
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: "Section 13.2.1 (maximum likelihood for the HMM by EM)"
---

The Baum-Welch algorithm fits the parameters $(\pi, A, B)$ of a [hidden Markov model](/hidden-markov-model/) to observation sequences when the state paths are not seen. It is the [expectation-maximization](/expectation-maximization/) algorithm for this model. The E step runs the [forward-backward algorithm](/forward-backward-algorithm/) to get the expected number of starts, moves and emissions of each kind. The M step sets each probability to its expected count divided by the row total. One round costs $\Theta(T N^2)$ time, the likelihood never decreases from one round to the next, and the end point is in general a local maximum only.

## In plain words

If you could see the hidden states, training would be counting: count how often each state follows each state, and how often each state shows each symbol, then divide by the totals. You cannot see the states, so you guess a model first. With that guess, forward-backward tells you how likely each state was at each step. Count with these weights in place of the true states and divide, which gives a new model. Repeat. Each round fits the data at least as well as the round before, but where you end up depends on the first guess.

## The problem

The input is $R \ge 1$ sequences $O^{(1)}, \ldots, O^{(R)}$ over the symbols $1, \ldots, M$, the number $N$ of hidden states, and starting parameters $\lambda^{(0)}$ with $P(O^{(r)} \mid \lambda^{(0)}) > 0$ for all $r$. The goal of [HMM parameter learning](/hmm-parameter-learning/) is the [maximum likelihood](/maximum-likelihood-estimation/) estimate

$$\hat\lambda = \arg\max_\lambda L(\lambda), \qquad L(\lambda) = \sum_{r=1}^{R} \log P(O^{(r)} \mid \lambda).$$

$L$ can have many local maxima, and Baum-Welch does not promise the global one. It returns a sequence of parameters $\lambda^{(1)}, \lambda^{(2)}, \ldots$ with $L(\lambda^{(k+1)}) \ge L(\lambda^{(k)})$. $T$ is the total number of symbols, $\sum_r T_r$.

## The algorithm

For one sequence, $\gamma_t(i) = P(q_t = i \mid O, \lambda)$ and $\xi_t(i, j) = P(q_t = i, q_{t+1} = j \mid O, \lambda)$ are the outputs of forward-backward.

```pseudo id=main
BAUM-WELCH(π, A, B, O^(1) .. O^(R))
L1  repeat until the gain in L is small or a round limit is reached
        set all counts s_i, e_ij, f_jk to 0
L2      for r ← 1 to R do
L3          run FORWARD-BACKWARD on O^(r) to get γ_t(i), ξ_t(i, j) and log P(O^(r))
L4          s_i += γ_1(i);  e_ij += Σ_{t<T_r} ξ_t(i, j);  f_jk += Σ_{t: o_t = k} γ_t(j)
L5      π_i ← s_i / Σ_i' s_i'                      (this is s_i / R)
L6      A_ij ← e_ij / Σ_j' e_ij'
L7      B_j(k) ← f_jk / Σ_k' f_jk'
L8  return π, A, B and the history of L
```

Lines L2 to L4 are the E step and lines L5 to L7 are the M step. The counts in line L4 are expected counts under the current model: $\sum_t \xi_t(i, j)$ is the expected number of moves from $i$ to $j$, and $\sum_{t : o_t = k} \gamma_t(j)$ is the expected number of times that $j$ emits $k$. For long sequences the forward-backward pass in line L3 must use scaling (or log space), and $\log P(O^{(r)})$ is then the sum of the logs of the scale factors.

If a row has a total of zero (a state with no expected visits), the implementation keeps the old row; any stochastic row is then equally good.

## Example

Start from the rain (R) and dry (D) model of the forward algorithm page, $\pi = (1/2, 1/2)$, $A = \begin{pmatrix} 0.7 & 0.3 \\ 0.2 & 0.8 \end{pmatrix}$, $B = \begin{pmatrix} 0.9 & 0.1 \\ 0.2 & 0.8 \end{pmatrix}$ over the symbols umbrella (u) and none (n), and train on the one sequence $O = (u, u, n, u)$. Forward-backward gives

| $t$ | $o_t$ | $\gamma_t(R)$ | $\gamma_t(D)$ |
|---|---|---|---|
| 1 | u | 0.8770 | 0.1230 |
| 2 | u | 0.7974 | 0.2026 |
| 3 | n | 0.3086 | 0.6914 |
| 4 | u | 0.6478 | 0.3522 |

and the pair posteriors $\xi_1, \xi_2, \xi_3$ of the forward-backward page. The expected counts are:

- Starts: $s = (0.8770, 0.1230)$, so the new $\pi = (0.8770, 0.1230)$.
- Moves out of R: $e_{RR} = 0.7498 + 0.2965 + 0.2817 = 1.3280$ and $e_{RD} = 0.1272 + 0.5009 + 0.0268 = 0.6549$. The total $1.9829$ is $\gamma_1(R) + \gamma_2(R) + \gamma_3(R)$, so $A_{RR} = 0.6697$ and $A_{RD} = 0.3303$. In the same way the row of D becomes $(0.4186, 0.5814)$.
- Emissions of R: u at $t = 1, 2, 4$ gives $0.8770 + 0.7974 + 0.6478 = 2.3222$, and n at $t = 3$ gives $0.3086$. So $B_R = (0.8827, 0.1173)$. In the same way $B_D = (0.4950, 0.5050)$.

The log-likelihood goes from $\log 0.04911505 = -3.0136$ to $-2.1694$ after one round. With one short sequence, further rounds go on to raise it by fitting this one sequence ever more closely. That is overfitting, not progress: real training uses many sequences.

## Correctness

The proof is in the proofs file. In outline: by the linearity of expectation, line L4 computes the expected counts of starts, moves and emissions under $P(Q \mid O, \lambda)$. The log of the joint of an HMM is a sum of count times log parameter, so the expected complete-data log-likelihood $\mathcal{Q}(\lambda')$ splits into one term per row, and Gibbs' inequality shows that normalized counts maximize each term. By [Jensen's inequality](/jensens-inequality/), $L(\lambda') - L(\lambda) \ge \mathcal{Q}(\lambda') - \mathcal{Q}(\lambda)$, so the new parameters have $L$ at least as large as the old. Each row of counts is non-negative and is divided by its sum, so the new rows are stochastic.

This proves only that $L$ goes up. It does not prove that the limit is the maximum likelihood estimate: it can be a local maximum or a saddle point.

## Complexity

One round runs forward-backward on each sequence, which takes $\Theta(T_r N^2)$ time for a sequence of length $T_r$, so $\Theta(T N^2)$ for all of them. Adding the emission counts takes $\Theta(T N)$, and the M step takes $\Theta(N^2 + N M)$. So one round costs $\Theta(T N^2 + N M)$, and $K$ rounds cost $K$ times that.

The space is $\Theta(T_r N)$ for the forward and backward tables of one sequence at a time, plus $\Theta(N^2 + N M)$ for the counts and the parameters. The $\xi_t$ never need to be stored, since only their sums are used. The number of rounds $K$ is not bounded in advance: EM converges linearly near a maximum, and slowly when the states overlap a lot.

## Properties

- **Monotone.** $L(\lambda^{(k+1)}) \ge L(\lambda^{(k)})$ in every round. The tests check this on seeded runs.
- **Stays a valid model.** All rows of $\pi$, $A$ and $B$ stay non-negative and sum to 1.
- **Zeros stay zero.** If a parameter is 0, its expected count is 0, so it stays 0. This keeps a structure, such as a left-to-right model, in place.
- **Local only.** The result depends on the start. A symmetric start, with uniform $\pi$ and $A$ and equal rows of $B$, is a fixed point from which the algorithm never moves.
- **No step size.** Unlike gradient ascent, each round jumps to the maximizer of $\mathcal{Q}$, with no learning rate to tune.

## Variants and improvements

- **Several sequences.** Add the counts of all sequences before the M step, as in the pseudocode (Rabiner, Section V.B).
- **Continuous outputs.** With Gaussian or [Gaussian mixture](/gaussian-mixture-model/) emissions the M step for $B$ becomes a weighted mean and covariance per state, with $\gamma_t(j)$ as the weights.
- **Priors.** Add pseudocounts to each row of counts. This is MAP estimation with Dirichlet priors and prevents rows of zeros from short data.
- **Viterbi training.** Replace the expected counts by the counts along the single [Viterbi](/viterbi-algorithm/) path. It is faster and gives a hard segmentation, but it does not maximize $L$.
- **Explicit durations.** A [hidden semi-Markov model](/hidden-semi-markov-model/) has its own forward-backward pass and its own re-estimation of the duration distributions.
- **Grammars.** The [inside-outside algorithm](/inside-outside-algorithm/) is the same EM idea for probabilistic context-free grammars.

## When to use it

Use Baum-Welch when you have unlabeled sequences and a fixed number of hidden states, and want a generative model of them. If you have labeled state paths, do not use it: count and normalize once. Because it finds a local maximum only, run it from several starts, or from a start built from domain knowledge, and keep the best $L$. Check the result on held-out data, because a large $N$ can fit the training sequences very well and others badly.

## Pitfalls

- **Local maxima.** Different starts give different models with different likelihoods. One run is not enough.
- **A zero in the start is permanent.** A transition or emission set to 0 at the start can never come back. Start with all allowed parameters positive.
- **Underflow.** Unscaled $\alpha$ and $\beta$ go to 0 for long sequences, and then $\gamma$ and $\xi$ become $0/0$. Use scaling or log space.
- **The stopping test.** Stop on a small gain in $L$, not on a small change in the parameters alone. In flat regions $L$ can rise very slowly for many rounds.
- **The state labels are not identified.** Any permutation of the states gives the same likelihood. Two runs can find the same model with the states in a different order.
- **The number of states.** EM does not choose $N$. A larger $N$ never fits the training data worse, so choose $N$ on held-out data or with a penalty such as BIC.

## Implementations

## History

Baum and Petrie (1966) studied maximum likelihood for probabilistic functions of finite Markov chains. Baum, Petrie, Soules and Weiss (1970), working at the Institute for Defense Analyses in Princeton, gave the re-estimation transformation and proved that it never decreases the likelihood, using the forward and backward quantities to compute it. The name Baum-Welch also honors Lloyd Welch, who worked with Baum at IDA. Dempster, Laird and Rubin (1977) gave the general EM algorithm, of which this method is an early case, and Wu (1983) gave a correct account of its convergence. Rabiner's 1989 tutorial gave the form most used today, with scaling and with several training sequences.

## References
