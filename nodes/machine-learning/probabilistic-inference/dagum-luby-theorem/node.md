---
tag: 03QBR6
kind: theorem
slug: dagum-luby-theorem
name: Dagum-Luby theorem
aliases:
- NP-hardness of approximate Bayesian network inference
area: machine-learning/probabilistic-inference
level: research
summary: "With evidence, approximating P(X = x | e) in a Bayesian network within any absolute error below 1/2 is NP-hard. A relative approximation is NP-hard even with no evidence."
prereqs: [cooper-theorem, rp]
see_also: [marginal-inference, likelihood-weighting, rejection-sampling, ancestral-sampling, self-reducibility, hoeffding-inequality, fpras, gibbs-sampling]
sources:
  - paper: doi:10.1016/0004-3702(93)90036-B
    title: "Paul Dagum and Michael Luby, Approximating probabilistic inference in Bayesian belief networks is NP-hard, Artificial Intelligence 60(1), 1993, pages 141 to 153"
    locator: the hardness of absolute and relative approximation of a posterior probability, deterministic and randomized
  - paper: doi:10.1016/0004-3702(90)90060-D
    title: "Gregory F. Cooper, The computational complexity of probabilistic inference using Bayesian belief networks, Artificial Intelligence 42(2-3), 1990, pages 393 to 405"
    locator: the network built from a 3-CNF formula that the reduction uses
  - book: isbn:9780262013192
    title: Daphne Koller and Nir Friedman, Probabilistic Graphical Models, Principles and Techniques, MIT Press, 2009
    locator: "Section 9.1, the complexity of approximate inference: absolute and relative error, with and without evidence"
---

The Dagum-Luby theorem says that approximate inference in [Bayesian networks](/bayesian-network/) is as hard as exact inference once there is evidence. Dagum and Luby (1993) showed that a posterior probability $P(X = x \mid e)$ cannot be approximated within any absolute error below $\tfrac12$ in polynomial time unless P = NP, and that a relative approximation is NP-hard too. The proof uses the network of [Cooper's theorem](/cooper-theorem/) and a self-reduction: an approximate answer, asked one variable at a time, builds a satisfying assignment.

## Statement

Let $P$ be the distribution of a Bayesian network over binary variables with rational tables, let $X$ be a node, and let $E = e$ be evidence with $P(e) > 0$. A number $Z$ is an *absolute $\varepsilon$-approximation* of $p = P(X = 1 \mid e)$ when $|Z - p| \le \varepsilon$, and a *relative $\varepsilon$-approximation* when $p/(1 + \varepsilon) \le Z \le (1 + \varepsilon)\, p$.

**Theorem (Dagum and Luby 1993).**

1. For every fixed $\varepsilon$ with $0 \le \varepsilon < \tfrac12$, computing an absolute $\varepsilon$-approximation of $P(X = 1 \mid e)$ is [NP-hard](/np-hard/). The proof below needs one query node and one evidence node.
2. For every fixed $\varepsilon > 0$, computing a relative $\varepsilon$-approximation of $P(X = 1 \mid e)$ is NP-hard. This holds even with no evidence.
3. If a randomized algorithm runs in polynomial time and outputs an absolute $\varepsilon$-approximation with $\varepsilon < \tfrac12$ with probability at least $\tfrac12 + \delta$, for a fixed $\delta > 0$, then NP $\subseteq$ [RP](/rp/).

The bound $\tfrac12$ in part 1 is the best possible, because the answer $Z = \tfrac12$ is within $\tfrac12$ of every probability. Part 3 is stated here in the form that the proof below gives. The exact success probability and the exact form of the relative error in the paper are not checked here against its text.

## In plain words

Exact answers are hard, as Cooper showed. One could hope that rough answers are easy. This theorem says no, as soon as some facts are given as evidence.

Take the puzzle network of Cooper's theorem and give it the fact that all the rules hold. Ask a rough method how likely the first switch is to be on. If the method is wrong by less than one half, its answer tells which setting of the first switch still leaves a solution. Fix that switch and ask about the next one. After one question per switch you have a solution, so the rough method would solve a hard puzzle.

A method that is right only most of the time is no help either: ask several times, take the middle answer, and check the solution at the end.

Without evidence, rough answers in the absolute sense are easy, by simple sampling.

## Proof

Let $\varphi$ be a 3-CNF formula over $q_1, \ldots, q_n$ with $m$ clauses, and let $B_\varphi$ be Cooper's network: fair roots $Q_1, \ldots, Q_n$, one OR node per clause, and a chain of AND nodes that ends in $Y$. By Cooper's lemma, every full assignment of positive probability is fixed by its $q$ part, and
$$P(Q = q,\ Y = 1) = 2^{-n}\, [\,q \text{ satisfies } \varphi\,].$$
Here the roots may have other priors in $\{0, \tfrac12, 1\}$: the same argument gives $P(Q = q, Y = 1) = P(Q = q)\,[\,q \text{ satisfies } \varphi\,]$.

**Part 1: the self-reduction.** Suppose an algorithm $\mathcal A$ returns an absolute $\varepsilon$-approximation with $\varepsilon < \tfrac12$. Run:

1. Set $B \leftarrow B_\varphi$.
2. For $i = 1, \ldots, n$: let $z_i = \mathcal A(B, Q_i, Y = 1)$; set $b_i = 1$ if $z_i \ge \tfrac12$ and $b_i = 0$ if not; change the prior of $Q_i$ in $B$ to $P(Q_i = b_i) = 1$.
3. Accept if and only if $b = (b_1, \ldots, b_n)$ satisfies $\varphi$.

Each change keeps the network valid and keeps the evidence the one node $Y = 1$. If $\varphi$ is unsatisfiable, step 3 rejects, whatever $\mathcal A$ returns, even where $P(Y = 1) = 0$ makes the question undefined.

Now let $\varphi$ be satisfiable. *Claim:* before round $i$, $P_B(Y = 1) > 0$. It holds for $i = 1$. Assume it before round $i$, and let $p = P_B(Q_i = 1 \mid Y = 1)$, which is defined. If $z_i \ge \tfrac12$ then $p \ge z_i - \varepsilon \ge \tfrac12 - \varepsilon > 0$, so $P_B(Q_i = 1, Y = 1) > 0$. If $z_i < \tfrac12$ then $p < \tfrac12 + \varepsilon < 1$, so $P_B(Q_i = 0, Y = 1) > 0$. In both cases some $q$ with $q_i = b_i$ satisfies $\varphi$ and has positive probability in $B$. Setting the prior of $Q_i$ to $P(Q_i = b_i) = 1$ multiplies the weight of each such $q$ by $2$ and keeps it positive, so the claim holds before round $i + 1$. After round $n$, every root is fixed to $b$ and $P_B(Y = 1) > 0$, so $b$ satisfies $\varphi$ and step 3 accepts.

So the procedure decides 3SAT with $n$ calls to $\mathcal A$ and polynomial extra work, and an algorithm for part 1 in polynomial time would give P = NP. This is a [self-reduction](/self-reducibility/) of the search problem, guided by approximate answers.

**Part 2.** $P(Y = 1) = \#\varphi / 2^n$ is $0$ exactly when $\varphi$ is unsatisfiable. A relative approximation $Z$ satisfies $Z = 0$ if and only if $P(Y = 1) = 0$, so one call decides 3SAT. For a posterior, take as evidence any node with probability 1, or a fresh root with prior $\tfrac12$ and no children: the posterior of $Y$ equals $P(Y = 1)$.

**Part 3: randomized algorithms.** Let $\mathcal A$ be right, within $\varepsilon$, with probability at least $\tfrac12 + \delta$, with fresh coins on each call. Replace each call in step 2 by $k$ independent calls with $k$ odd and take the median. If more than $k/2$ of the answers lie in the interval $[p - \varepsilon, p + \varepsilon]$, then so does the median. By the [Hoeffding inequality](/hoeffding-inequality/), the number of right answers is at most $k/2$ with probability at most $e^{-2\delta^2 k}$. Take $k \ge \ln(4n)/(2\delta^2)$. By the union bound, all $n$ medians are right with probability at least $\tfrac34$, and then the procedure accepts a satisfiable $\varphi$. Step 3 still rejects every unsatisfiable $\varphi$ with probability 1. So 3SAT has a polynomial-time algorithm with one-sided error, 3SAT $\in$ RP, and since RP is closed under polynomial-time reductions, NP $\subseteq$ RP. $\blacksquare$

**An example.** Take $\varphi = (q_1 \vee q_2 \vee \neg q_3) \wedge (\neg q_1 \vee q_3 \vee q_4) \wedge (\neg q_2 \vee \neg q_3 \vee \neg q_4)$, with 10 models out of 16, and an approximation with $\varepsilon = 0.3$.

| round | exact $P(Q_i = 1 \mid Y = 1)$ | answer $z_i$ | fixed value |
|---|---|---|---|
| 1 | $5/10 = 0.5$ | 0.6 | $q_1 = 1$ |
| 2 | $2/5 = 0.4$ | 0.65 | $q_2 = 1$ |
| 3 | $1/2 = 0.5$ | 0.2 | $q_3 = 0$ |
| 4 | $1$ | 0.7 | $q_4 = 1$ |

Each answer is within $0.3$ of the exact value, and the last assignment $(1, 1, 0, 1)$ satisfies all three clauses. In round 2 the answer is on the wrong side of the exact value, but the choice is still safe.

## Consequences

- **Sampling with evidence has no general guarantee.** [Likelihood weighting](/likelihood-weighting/), [rejection sampling](/rejection-sampling/), [Gibbs sampling](/gibbs-sampling/) and every other polynomial-time method fail to get within $\tfrac12$ on some networks with evidence, unless NP $\subseteq$ RP. In the network above, rejection sampling keeps a sample only when $Y = 1$, which has probability $\#\varphi / 2^n$, so it may need about $2^n$ samples.
- **No FPRAS in general.** A fully polynomial randomized approximation scheme ([FPRAS](/fpras/)) for $P(e)$ would give each posterior $P(Q_i = 1 \mid Y = 1)$, as the ratio of the estimates of $P(Q_i = 1, Y = 1)$ and $P(Y = 1)$, within absolute error $\tfrac14$ with probability above $\tfrac34$. Part 3 then gives NP $\subseteq$ RP. So no such scheme exists for all networks unless NP $\subseteq$ RP.
- **What can be done.** Guarantees need extra conditions: bounded treewidth for exact methods, or bounds on how small the conditional probabilities and the evidence probability are for sampling methods. Dagum and Luby (1997) studied such conditions.
- **Exact versus approximate.** Together with Cooper's theorem, the result shows that evidence makes [marginal inference](/marginal-inference/) hard to approximate in the absolute sense, while without evidence simple sampling gives absolute approximations. A relative approximation is hard even with no evidence (part 2).

## Tightness

- **Error $\tfrac12$.** The constant answer $\tfrac12$ is an absolute $\tfrac12$-approximation of every probability, so part 1 fails at $\varepsilon = \tfrac12$. The self-reduction also breaks: with the answer $\tfrac12$ it may fix a variable to a value that leaves no solution.
- **No evidence, absolute error.** Without evidence, [ancestral sampling](/ancestral-sampling/) draws each node given its parents. The share of $N$ samples with $X = 1$ is within $\varepsilon$ of $P(X = 1)$ with probability at least $1 - \delta$ when $N \ge \ln(2/\delta)/(2\varepsilon^2)$, by the Hoeffding inequality. So absolute approximation of a prior marginal takes polynomial time for every fixed $\varepsilon > 0$, and part 1 needs evidence.
- **Relative error needs no evidence.** Part 2 holds without evidence because $P(Y = 1)$ can be $0$ or as small as $2^{-n}$.

## History

Cooper (1990) showed that exact inference is NP-hard and suggested approximation as a way out. Dagum and Luby (1993) closed that way for the worst case: approximation within absolute error below $\tfrac12$ with evidence, and relative approximation, are NP-hard, and randomized approximation is hard unless NP $\subseteq$ RP. Roth (1996) gave further results on the hardness of approximate reasoning, and Dagum and Luby (1997) gave a randomized approximation algorithm with guarantees under conditions on the network. Koller and Friedman (2009, Section 9.1) present the absolute and relative results with Cooper's network.

## References
