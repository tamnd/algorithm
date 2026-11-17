---
tag: FD26PV
kind: algorithm
slug: meme-algorithm
name: MEME
aliases:
- multiple EM for motif elicitation
area: biology/gene-finding-and-motifs
level: core
summary: Fit a two-component mixture of motif and background by expectation maximization, starting from many seed l-mers, to find motifs.
solves: [motif-finding-problem]
model: word-ram
complexity:
  vars: {n: the number of sequences, G: the length of each sequence, L: the motif length, W: "the number of windows per sequence, G - L + 1", N: "the number of windows, n W", I: the number of EM iterations}
  time: {worst: O(n W^2 L + I n W L), per_iteration: O(N L)}
  space: {extra: O(N + L)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1994
  people: [Timothy L. Bailey, Charles Elkan]
  note: Bailey and Elkan built MEME on the EM method of Lawrence and Reilly (1990). It drops the rule of one site per sequence, starts EM from many strings in the data, and erases found sites to find several motifs.
prereqs: [motif-finding-problem, expectation-maximization, position-specific-scoring-matrix]
see_also: [gibbs-motif-sampler, randomized-motif-search, gaussian-mixture-model, maximum-likelihood-estimation, maximum-a-posteriori-estimation, motif-information-content, random-projection-motif-finding, sequence-logo]
sources:
  - paper: "Timothy L. Bailey and Charles Elkan, Fitting a mixture model by expectation maximization to discover motifs in biopolymers, Proceedings of the Second International Conference on Intelligent Systems for Molecular Biology (ISMB-94), AAAI Press, 1994, pp. 28-36"
    title: Fitting a mixture model by expectation maximization to discover motifs in biopolymers
    locator: the two-component mixture model, the E step and the M step with Dirichlet prior counts, the starting points from subsequences, and erasing
  - paper: doi:10.1002/prot.340070105
    title: Charles E. Lawrence and Andrew A. Reilly, An expectation maximization (EM) algorithm for the identification and characterization of common sites in unaligned biopolymer sequences, Proteins 7(1), 1990
    locator: pp. 41 to 51, EM with one site per sequence
  - paper: doi:10.1111/j.2517-6161.1977.tb01600.x
    title: Arthur P. Dempster, Nan M. Laird and Donald B. Rubin, Maximum likelihood from incomplete data via the EM algorithm, Journal of the Royal Statistical Society, Series B 39(1), 1977
    locator: pp. 1 to 22, the EM algorithm and the proof that each iteration does not lower the likelihood
---

MEME (multiple EM for motif elicitation) of Bailey and Elkan (1994) finds a motif by fitting a mixture model to all windows of length $L$ in the input. Each window comes either from a motif model, a [position-specific scoring matrix](/position-specific-scoring-matrix/) of letter probabilities, or from a background model of single letters. [Expectation maximization](/expectation-maximization/) alternates between the probability that each window is a site and new models fitted to these weights. EM finds a local optimum, so MEME starts it from many strings that occur in the data and keeps the best. This page gives the EM core for one motif.

## In plain words

Cut every sequence into all its overlapping pieces of length $L$. Some pieces are copies of a hidden word, and the rest are noise. You do not know which, so you guess a model of the hidden word, a table with the chance of each letter at each place.

Now repeat two steps. First, for each piece, work out how likely it is to be a copy, given the table and the letters of the noise. Second, build a new table from all pieces, where each piece counts as much as its chance of being a copy. Each round makes the model fit the data at least as well as before. A poor first guess can lead to a poor answer, so start from many guesses, each one taken from a piece of the data.

## The problem

**Input.** DNA sequences $s_1, \ldots, s_n$, each of length $G$, and a motif length $L$. Let $X_1, \ldots, X_N$ be all $N = nW$ windows, with $W = G - L + 1$. Positions are 1-based on this page and 0-based in the code. Let $\mu(a)$ be the frequency of the letter $a$ in the input.

**The model.** Each window is a motif site with probability $\lambda$, and then its letters are independent with probabilities $\theta_j(a)$ at column $j$. Otherwise it is background, with letter probabilities $\theta_0(a)$ at every column. So

$$P(X_k) = \lambda \prod_{j} \theta_j(X_{k,j}) + (1 - \lambda) \prod_{j} \theta_0(X_{k,j}).$$

The windows are treated as independent, though they overlap.

**Output.** The parameters $\theta, \theta_0, \lambda$ at a local maximum of the objective

$$F = \sum_{k=1}^{N} \log P(X_k) + \beta \sum_a \mu(a) \Big( \sum_j \log \theta_j(a) + \log \theta_0(a) \Big),$$

the log likelihood plus the log of a Dirichlet prior with $\beta\mu(a)$ prior counts, and the weights $z_k$, the posterior probability that window $k$ is a site.

## The algorithm

```pseudo id=main
MEME(s[1 .. n], L, β, m)
L1  X ← all N windows of length L, μ ← the letter frequencies of s
L2  for each start string u do
L3      θ_j(a) ← m if a = u_j, else (1 - m)/3; θ_0 ← μ; λ ← n/N
L4      do one E step (L7) and one M step (L8, L9), and keep the start with the largest F
L5  (θ, θ_0, λ) ← the parameters of the kept start
L6  repeat
L7      z_k ← λ Π_j θ_j(X_k,j) / (λ Π_j θ_j(X_k,j) + (1 - λ) Π_j θ_0(X_k,j)) for k ← 1 to N
L8      λ ← Σ_k z_k / N; c_j(a) ← Σ_k z_k [X_k,j = a]; c_0(a) ← Σ_k (1 - z_k) #{j : X_k,j = a}
L9      θ_j(a) ← (c_j(a) + βμ(a)) / (Σ_b c_j(b) + β); θ_0(a) ← (c_0(a) + βμ(a)) / (Σ_b c_0(b) + β)
L10 until the largest change of a θ_j(a) is below tol, or the cap on iterations is reached
L11 return θ, θ_0, λ, z
```

Line L7 is the E step, a use of [Bayes' theorem](/bayes-theorem/). Lines L8 and L9 are the M step: $\lambda$ is the mean weight, and the letter probabilities are the weighted counts plus the prior counts, divided by their total. Lines L2 to L5 pick the start: Bailey and Elkan derive starting points from the subsequences of the data and pick the best of them. Here each start gets one iteration, and the best value of $F$ after it decides.

**Choices of this code.** The start strings are the distinct windows of $s_1$ by default; the motif occurs in every sequence, so $s_1$ has a copy, and this keeps the start phase at $O(W)$ starts. The start probability $m = 0.7$ and the prior weight $\beta = 0.1$ are the choice of this code, picked on planted test data; they are not values from the paper. The code works in log space and clamps $\lambda$ into $(10^{-12}, 1 - 10^{-12})$. It leaves out three parts of MEME: the erasing of found sites to find more motifs, the smoothing that stops overlapping windows from all being sites, and the search over the start value of $\lambda$.

## Example

Take the five sequences of Rosalind problem BA2F with $L = 8$, so $N = 125$. The kept start is AACGGCCA, the window at position 25 of $s_1$. After 35 iterations the objective has grown from $-1367.755$ to $-1357.015$, and the model is:

| column | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| A | 0.768 | 0.630 | 0.005 | 0.002 | 0.117 | 0.006 | 0.310 | 0.761 |
| C | 0.227 | 0.086 | 0.194 | 0.126 | 0.004 | 0.532 | 0.683 | 0.235 |
| G | 0.003 | 0.163 | 0.799 | 0.308 | 0.490 | 0.230 | 0.005 | 0.003 |
| T | 0.002 | 0.121 | 0.002 | 0.564 | 0.389 | 0.233 | 0.002 | 0.002 |

Its consensus is AAGTGCCA, which is a [median string](/median-string-problem/) of this input, with total distance 9, the optimum. The window with the largest $z$ in each sequence is AACGGCCA (position 25, $z = 0.959$), AAGTGCCA (16, 0.995), AAGTATAC (19, 0.788), AAGTTTCA (7, 0.990) and CAGCTCCA (8, 0.934). The final $\lambda$ is 0.092, more than $n/N = 0.04$: the model counts about 11.4 windows as sites, since nothing stops it from taking two windows of one sequence.

**Measured success on planted motifs.** The test generator plants a motif with exactly $d$ changes in each of 10 random sequences. A run counts as a success when the consensus of $\theta$ equals the planted motif. Over seeds 0 to 19, with the defaults:

| $G$ | $(L, d)$ | consensus found | all planted starts found |
|---|---|---|---|
| 100 | (8, 1) | 16 of 20 | 9 of 20 |
| 100 | (10, 2) | 2 of 20 | 3 of 20 |
| 200 | (12, 3) | 0 of 20 | 0 of 20 |

The second column counts runs in which the window with the largest $z$ in each sequence is the planted one. These are measurements of this reduced code on these seeds, not of the MEME program. In every one of these 60 runs the objective did not decrease from one iteration to the next.

## Correctness

**Theorem (EM ascent).** No iteration of lines L7 to L9 lowers $F$.

*Proof.* Let $Q(\phi' \mid \phi) = \sum_k [z_k (\log \lambda' + \sum_j \log \theta'_j(X_{k,j})) + (1 - z_k)(\log (1 - \lambda') + \sum_j \log \theta'_0(X_{k,j}))]$ plus the prior term, where $z$ comes from the E step at $\phi$. For each $k$, $\log P_{\phi'}(X_k) = (\text{the } k\text{th term of } Q) - H_k$, with $H_k = z_k \log z'_k + (1 - z_k) \log (1 - z'_k)$ in terms of the posterior $z'$ at $\phi'$. By Gibbs' inequality, $H_k$ is largest at $z' = z$, that is, at $\phi' = \phi$. So $F(\phi') - F(\phi) \ge Q(\phi' \mid \phi) - Q(\phi \mid \phi)$. The M step maximizes $Q$: each term separates into a function of $\lambda'$, maximized at $\sum z / N$, and for each column a sum $\sum_a (c_j(a) + \beta\mu(a)) \log \theta'_j(a)$ over the simplex, maximized at $\theta'_j(a) \propto c_j(a) + \beta\mu(a)$, which is line L9. So $F$ does not drop. $\square$

This is the theorem of Dempster, Laird and Rubin, with the prior added. It gives convergence of $F$, since $F$ is bounded above, but only to a stationary point, usually a local maximum. Different starts reach different local maxima, which is why lines L2 to L5 try many.

**Theorem (the site rule).** $z_k > 1/2$ exactly when $\sum_j \log(\theta_j(X_{k,j}) / \theta_0(X_{k,j})) > \log((1 - \lambda)/\lambda)$.

*Proof.* Let $r$ be the left side. Line L7 gives $z_k = 1/(1 + e^{-(r - \log((1-\lambda)/\lambda))})$, and this is above $1/2$ exactly when the exponent is negative. $\square$

So the motif model is a [position-specific scoring matrix](/position-specific-scoring-matrix/) of log odds, and the threshold for a site depends on $\lambda$. The tests check the ascent on the sample and on random inputs, the E step against Bayes' theorem, the site rule, and that the M step maximizes $Q$ against 200 random and nearby parameters. The proofs are in proofs/correctness.md.

## Complexity

- **Time.** The E step computes $N$ products of $L$ terms, and the M step adds each window's letters with its weight, so an iteration takes $O(NL)$ time. Bailey and Elkan give the same linear cost per iteration. The start phase does one iteration for each of at most $W$ starts, $O(W N L) = O(n W^2 L)$, and $I$ main iterations add $O(I N L)$.
- **Space.** The weights take $N$ numbers and the models $4L + 4$ numbers, so $O(N + L)$ besides the input.
- **In practice.** On the BA2F sample the main run takes 35 iterations. On the planted $(8, 1)$ runs with $G = 100$ and seeds 0 to 5, it takes between 69 and 170.

## Properties

- **Deterministic.** There is no randomness; the result depends only on the input, the start strings and the parameters.
- **Soft assignment.** Every window has a weight between 0 and 1, so the model can use evidence from windows that only look a little like sites. The [randomized motif search](/randomized-motif-search/) is the same method with hard 0 or 1 weights and one site per sequence.
- **A local optimum.** EM stops at a stationary point of $F$, which depends on the start.
- **A mixture model.** The model is a two-component mixture, like a [Gaussian mixture model](/gaussian-mixture-model/) with discrete components, and EM is fitted the same way.

## Variants and improvements

- **OOPS, ZOOPS and TCM.** The MEME program offers three models of the sites: exactly one occurrence per sequence (the model of Lawrence and Reilly), zero or one per sequence, and any number. The code on this page fits the last, with no limit on the number of sites.
- **Erasing.** After a motif is found, MEME lowers the weights of the windows that it explains and runs again, to find the next motif.
- **A search over $\lambda$.** The start value of $\lambda$ matters, and MEME tries several and keeps the best by a statistical measure.
- **Better priors.** Dirichlet mixture priors help on protein sequences.
- **Discriminative and Bayesian versions.** Later work fits the motif against a set of control sequences, or samples the sites, as in the [Gibbs motif sampler](/gibbs-motif-sampler/).

## When to use it

Use MEME, or this EM core, when the motif may occur zero, one or several times per sequence, or when you want a probability model of the motif with weights for every window. It is deterministic, so a run can be repeated exactly. For a subtle planted motif, start the EM from the buckets of [PROJECTION](/random-projection-motif-finding/), which is what Buhler and Tompa did, since starts taken from single windows often lead EM to the wrong local optimum.

## Pitfalls

- **Overlapping windows.** The model treats the $N$ windows as independent, but they overlap. A strong site makes its shifted windows look like sites too, and $\lambda$ grows. MEME smooths the weights to fix this; the code on this page does not.
- **Zero probabilities.** Without prior counts, a letter that no site has gets probability 0, and the logarithm fails. Keep $\beta > 0$.
- **One iteration is not enough to judge a start.** Lines L2 to L5 rank starts after one iteration, which can favour a start near a shifted copy of the motif, and EM then converges to the shifted copy.
- **Underflow.** The product of $L$ probabilities underflows for long motifs. Work with sums of logarithms.
- **Reading $\lambda$ as the number of sites.** $\lambda N$ counts windows, and overlapping windows of one site each count.

## Implementations

## History

Lawrence and Reilly (1990) used EM to find a site in each of a set of unaligned protein and DNA sequences, with exactly one site per sequence. Bailey and Elkan (1994) made three changes: a mixture model over all windows, so that a sequence can have no site or several, many starting points taken from the subsequences of the data, and the erasing of found sites so that one run finds several motifs. The MEME program grew from this work and became one of the most used motif finders. The general EM method and its ascent property are due to Dempster, Laird and Rubin (1977).

## References
