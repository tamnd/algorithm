---
tag: H7F89C
kind: model
slug: probabilistic-turing-machine
name: Probabilistic Turing machine
aliases:
- randomized Turing machine
- PTM
area: foundations/models-of-computation
level: advanced
summary: Turing machine that may flip fair coins; defines BPP, RP and related randomized classes.
prereqs: [turing-machine, multitape-turing-machine]
see_also: [nondeterministic-turing-machine, bpp, rp, zpp, pp, hoeffding-inequality, randomized-algorithm, p-poly]
sources:
  - book: isbn:9780521424264
    title: "Sanjeev Arora and Boaz Barak, Computational Complexity: A Modern Approach"
    locator: Chapter 7, Randomized computation
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 10.2, Probabilistic algorithms
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 4, Chernoff and Hoeffding bounds
  - title: John Gill, Computational complexity of probabilistic Turing machines, SIAM Journal on Computing, volume 6, issue 4, 1977
    locator: pp. 675 to 695
  - title: Wassily Hoeffding, Probability inequalities for sums of bounded random variables, Journal of the American Statistical Association, volume 58, 1963
    locator: pp. 13 to 30
---

A probabilistic Turing machine is a [Turing machine](/turing-machine/) that flips a fair coin at each step and uses the result to choose between two transition functions. On a fixed input, its answer is a random variable, and its complexity classes bound the probability of a wrong answer. The classes [BPP](/bpp/), [RP](/rp/), [ZPP](/zpp/) and [PP](/pp/) differ in the kind of error that they allow. Repetition with independent coins makes the error of BPP and RP exponentially small, which is why BPP is the usual class of problems that are efficiently solvable with randomness.

## The machine

A probabilistic machine $M$ has the parts of the deterministic [multitape machine](/multitape-turing-machine/), except that it has two transition functions $\delta_0$ and $\delta_1$ of the same type as the deterministic one. At each step, $M$ flips a fair coin. If the coin shows $b \in \{0, 1\}$, the machine applies $\delta_b$. The coins at different steps are independent. The machine has no other source of randomness. Equivalently, $M$ is a deterministic machine with an extra read-only tape that holds an infinite random string, and the head of that tape moves right at each coin flip.

A **run** of $M$ on an input $w$ is the computation for one coin sequence $r \in \{0,1\}^{\mathbb{N}}$. A run that halts ends in accept or in reject. A run may also never halt. When $M$ halts within $T$ steps on every coin sequence, only the first $T$ coins matter, and the probability space is $\{0,1\}^T$ with the uniform measure. We write $\Pr[M(w) = \text{accept}]$ for the probability that the run on $w$ accepts. Because the probability is a multiple of $2^{-T}$ for a bound $T$, a machine with fair coins cannot have acceptance probability exactly $1/3$ in bounded time. The thresholds in the definitions below are bounds on the error, so a machine may have any error at or below the bound. Exact values such as $1/3$ cannot be reached anyway.

**Example: matrix product (a one-sided test).** The machine gets three $n \times n$ matrices $A$, $B$, $C$ with integer entries. It picks $r \in \{0,1\}^n$ with $n$ coin flips and accepts if and only if $A(Br) = Cr$. This takes $O(n^2)$ arithmetic operations (on a RAM; on a Turing machine the step count also depends on the bit length of the entries, and it stays polynomial). If $AB = C$, it always accepts. If $AB \ne C$, let $D = AB - C \ne 0$, and choose $(i, j)$ with $D_{ij} \ne 0$. Fix all coins except $r_j$. The value $(Dr)_i = D_{ij} r_j + s$, for a number $s$ fixed by the other coins, is zero for at most one of the two values of $r_j$. So the machine accepts with probability at most $1/2$. For $A = \begin{pmatrix}1&2\\3&4\end{pmatrix}$, $B = \begin{pmatrix}0&1\\1&0\end{pmatrix}$ and $C = \begin{pmatrix}2&1\\4&4\end{pmatrix}$ we have $AB = \begin{pmatrix}2&1\\4&3\end{pmatrix}$. Two of the four vectors $r$ give $A(Br) = Cr$, so the acceptance probability is exactly $1/2$, and the bound is tight. See [Freivalds' algorithm](/freivalds-algorithm/).

## What it counts

The **time** of $M$ on $w$ is the number of steps of a run. The machine runs in time $T(n)$ if every run on every input of length $n$ halts within $T(n)$ steps. The **randomness** is the number of coin flips of a run. The **error** on $w$ is the probability that the run gives the wrong verdict for the language that $M$ is meant to decide. A machine has *expected* time $T(n)$ if the average over the coins of the running time on each input of length $n$ is at most $T(n)$, even when some runs are much longer.

Let $L \subseteq \Sigma^*$. Each class below needs a polynomial $p$ and a machine $M$ that meets the time condition for all inputs $w$.

- $L \in \mathrm{BPP}$ if $M$ runs in time $p(|w|)$ and $w \in L \Rightarrow \Pr[M(w) \text{ accepts}] \ge 2/3$ and $w \notin L \Rightarrow \Pr[M(w) \text{ accepts}] \le 1/3$.
- $L \in \mathrm{RP}$ if $M$ runs in time $p(|w|)$ and $w \in L \Rightarrow \Pr[M(w) \text{ accepts}] \ge 1/2$ and $w \notin L \Rightarrow \Pr[M(w) \text{ accepts}] = 0$.
- $L \in \mathrm{coRP}$ if $\Sigma^* \setminus L \in \mathrm{RP}$. That is, a yes-input is always accepted, and a no-input is accepted with probability at most $1/2$.
- $L \in \mathrm{ZPP}$ if the expected time of $M$ on $w$ is at most $p(|w|)$, and $M$ accepts if $w \in L$ and rejects if $w \notin L$ on every run that halts. A run of $M$ is never wrong. It can be long.
- $L \in \mathrm{PP}$ if $M$ runs in time $p(|w|)$ and $w \in L \Leftrightarrow \Pr[M(w) \text{ accepts}] > 1/2$.

BPP and RP have a bounded gap between the two cases: the probabilities $2/3$ and $1/3$, or $1/2$ and $0$. PP has no gap. A machine for PP may accept a yes-input with probability $1/2 + 2^{-p(n)}$, and a no-input with probability $1/2$. Such probabilities, $1/2 + 2^{-n}$ and $1/2$, do not show that a language is in BPP: they are too close for the reduction below.

## Relation to other models

A deterministic machine is a probabilistic machine with $\delta_0 = \delta_1$, so $\mathrm{P} \subseteq \mathrm{ZPP}$. The chain of inclusions is

$$
\mathrm{P} \subseteq \mathrm{ZPP} \subseteq \mathrm{RP} \subseteq \mathrm{BPP} \subseteq \mathrm{PP}, \qquad \mathrm{RP} \subseteq \mathrm{NP} \subseteq \mathrm{PP}.
$$

The inclusion $\mathrm{BPP} \subseteq \mathrm{PP}$ holds because $2/3 > 1/2$ and $1/3 \le 1/2$. The inclusion $\mathrm{RP} \subseteq \mathrm{BPP}$ holds because running an RP machine twice and accepting if one run accepts gives acceptance probability at least $3/4$ on a yes-input and $0$ on a no-input. The inclusion $\mathrm{ZPP} \subseteq \mathrm{RP}$ is part of the theorem below.

The [nondeterministic machine](/nondeterministic-turing-machine/) and the probabilistic machine have the same tree of runs. They differ in the verdict. The nondeterministic machine accepts if some path accepts, which is acceptance probability above $0$. The probabilistic machine looks at the fraction of accepting paths. This gives $\mathrm{RP} \subseteq \mathrm{NP}$: a coin sequence on which an RP machine accepts is a certificate. It also gives $\mathrm{NP} \subseteq \mathrm{PP}$. Let $N$ be an NP machine with two choices at each step and time $t(n)$. The PP machine first flips one coin. On heads, it accepts. On tails, it runs $N$ with $t(n)$ coins as the choices and accepts if $N$ accepts. If $w \in L$, an accepting path exists and has probability at least $2^{-t(n)}$, so the acceptance probability is at least $1/2 + 2^{-t(n)-1} > 1/2$. If $w \notin L$, it is exactly $1/2$.

An alternating machine (see [alternating Turing machine](/alternating-turing-machine/)) is a different change of the verdict, with a quantifier instead of a probability. A [Boolean circuit](/boolean-circuit/) family is a non-uniform model, and the last result below relates it to BPP. The [quantum Turing machine](/quantum-turing-machine/) replaces probabilities by amplitudes.

## Known results in the model

**Theorem (error reduction).** Let $M$ be a machine that runs in time $T(n)$, and let $\gamma \in (0, 1/2)$. Assume that on every input $w$ the verdict of $M$ is wrong with probability at most $1/2 - \gamma$. For an odd $k$, let $M_k$ run $M$ on $w$ for $k$ times with independent coins, and accept if and only if more than $k/2$ of the runs accept. Then on every input

$$
\Pr[M_k \text{ gives the wrong verdict}] \le e^{-2\gamma^2 k}.
$$

*Proof.* Fix $w$. Let $X_i = 1$ if run $i$ gives the wrong verdict, and $X_i = 0$ otherwise. The $X_i$ are independent, because the runs use different coins, and $\mathbb{E}[X_i] \le 1/2 - \gamma$. Let $S = X_1 + \cdots + X_k$, so $\mathbb{E}[S] \le k(1/2 - \gamma)$. The majority is wrong if and only if more than $k/2$ runs are wrong, so only if $S \ge k/2$. Then $S - \mathbb{E}[S] \ge k/2 - k(1/2 - \gamma) = \gamma k$. The Chernoff-Hoeffding bound, in the additive form of [Hoeffding's inequality](/hoeffding-inequality/), says that for independent variables in $[0,1]$, $\Pr[S - \mathbb{E}[S] \ge \lambda] \le e^{-2\lambda^2/k}$. With $\lambda = \gamma k$ the probability is at most $e^{-2\gamma^2 k}$. $\square$

For BPP, $\gamma = 1/6$, so the error of $M_k$ is at most $e^{-k/18}$. The exact error of a majority of $k$ runs, each wrong with probability $1/3$, is smaller than the bound:

| $k$ | exact error | bound $e^{-k/18}$ |
|---|---|---|
| 1 | 0.333 | 0.946 |
| 11 | 0.122 | 0.543 |
| 25 | 0.0415 | 0.249 |
| 101 | 0.000272 | 0.00366 |

To get error at most $2^{-20}$, the bound needs $k \ge 18 \cdot 20 \ln 2 \approx 249.5$, so $k = 251$ is enough. The exact computation shows that $k = 193$ is the least odd value. The same proof works for any $\gamma \ge 1/q(n)$ with a polynomial $q$: then $k = O(q(n)^2 \cdot r(n))$ runs give error $2^{-r(n)}$, in time $k\,T(n) + O(kn)$, still polynomial. So the constants $2/3$ and $1/3$ of BPP can be replaced by $1/2 + 1/q(n)$ and $1/2 - 1/q(n)$, and also by $1 - 2^{-n}$ and $2^{-n}$, without a change of the class. For PP, the gap $\gamma$ may be as small as $2^{-p(n)}$ for a polynomial $p$, and the bound gives nothing before $k \approx 2^{2p(n)}$, so repetition does not help.

For RP, let $M_k$ accept if and only if some run accepts. A no-input is never accepted. A yes-input is rejected only when all $k$ runs reject, which has probability at most $2^{-k}$. No bound of Hoeffding type is needed.

**Theorem.** $\mathrm{ZPP} = \mathrm{RP} \cap \mathrm{coRP}$.

*Proof.* Let $L \in \mathrm{ZPP}$ via $M$ with expected time at most $p(n)$. Let $M_1$ run $M$ for at most $2p(n)$ steps, accept if $M$ halts in accept in that time, and reject in all other cases. By [Markov's inequality](/markov-inequality/), $M$ does not halt within $2p(n)$ steps with probability at most $1/2$. If $w \in L$, then $M$ never rejects, so $M_1$ accepts with probability at least $1/2$. If $w \notin L$, then $M$ never accepts, so $M_1$ never accepts. So $L \in \mathrm{RP}$. The machine $M_2$ that rejects only if $M$ halts in reject within $2p(n)$ steps shows $L \in \mathrm{coRP}$ in the same way.

Conversely, let $A$ be an RP machine and $B$ a coRP machine for $L$. A machine $M$ repeats this round with fresh coins: run $A$ and accept if $A$ accepts, then run $B$ and reject if $B$ rejects. Machine $A$ never accepts a word that is not in $L$, and $B$ never rejects a word in $L$, so each stop of $M$ is correct. If $w \in L$, $A$ accepts with probability at least $1/2$. If $w \notin L$, $B$ rejects with probability at least $1/2$. So a round stops with probability at least $1/2$, the expected number of rounds is at most $2$, and the expected time is polynomial. $\square$

More results:

- **BPP is in P/poly.** Every language in BPP has polynomial-size circuits ([P/poly](/p-poly/)). With $r(n) = n + 1$ in the reduction, the error on each input of length $n$ is at most $2^{-n-1}$. By the union bound over the $2^n$ inputs, the probability that some input of length $n$ gets a wrong verdict is at most $1/2 < 1$. So some fixed coin sequence is right on all inputs of length $n$, and it can be hard-wired as advice. Adleman gave this result in 1978.
- **Names and variants.** Gill (1977) defined the probabilistic Turing machine and the classes PP, BPP, ZPP and RP. An algorithm of type RP or BPP is also called a Monte Carlo algorithm, and an algorithm of type ZPP is called a Las Vegas algorithm. The logarithmic-space versions of RP and BPP are called RL and BPL.
- **Upper bounds.** $\mathrm{PP} \subseteq \mathrm{PSPACE}$, because a deterministic machine tries all coin sequences one after the other and counts the accepting ones with a counter. The same holds for BPP. BPP is in the second level of the [polynomial hierarchy](/polynomial-hierarchy/): $\mathrm{BPP} \subseteq \Sigma_2^p \cap \Pi_2^p$ (Sipser, Gács and Lautemann).
- **Open.** Whether $\mathrm{BPP} = \mathrm{P}$ is open. So is the question whether $\mathrm{BPP} \subseteq \mathrm{NP}$.

## References
