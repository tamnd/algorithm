---
tag: ASCCKX
kind: model
slug: statistical-query-model
name: Statistical query model
aliases:
- SQ model
- statistical query learning
area: machine-learning/supervised-learning
level: research
summary: "A learner that sees data only through estimates, within a tolerance tau, of expectations E[chi(x, c(x))]. SQ learners tolerate label noise; parity functions are not SQ learnable."
prereqs: [pac-learning, hoeffding-inequality]
see_also: [learning-parity-with-noise, fourier-analysis-of-boolean-functions, gaussian-elimination, halfspace-learning, agnostic-pac-learning, vc-dimension, perceptron, occams-razor]
sources:
  - paper: doi:10.1145/293347.293351
    title: Michael Kearns, Efficient noise-tolerant learning from statistical queries, Journal of the ACM 45(6), 1998
    locator: the definition of the STAT oracle, the simulation from noisy examples, the SQ learners for conjunctions and other classes, and the lower bound for parity
  - paper: doi:10.1145/195058.195147
    title: Avrim Blum, Merrick Furst, Jeffrey Jackson, Michael Kearns, Yishay Mansour and Steven Rudich, Weakly learning DNF and characterizing statistical query learning using Fourier analysis, STOC 1994
    locator: the statistical query dimension and the lower bound on queries for weak SQ learning
  - paper: "Avrim Blum, Adam Kalai and Hal Wasserman, Noise-tolerant learning, the parity problem, and the statistical query model, Journal of the ACM 50(4), 2003"
    locator: a class learnable with random classification noise that is not SQ learnable
  - book: isbn:9780262111935
    title: Michael J. Kearns and Umesh V. Vazirani, An Introduction to Computational Learning Theory, MIT Press, 1994
    locator: Chapter 5 (learning in the presence of noise, the statistical query model)
---

In the statistical query (SQ) model of Kearns (1998), the learner never sees an example. It asks questions of the form "what is the average of $\chi(x, y)$ over labeled examples?", and an oracle answers each one up to an error $\tau$ that the learner chooses. Any SQ learner can be run on random examples, and also on examples whose labels are flipped by random noise, so an SQ learner is automatically a noise-tolerant [PAC learner](/pac-learning/). Almost every known PAC algorithm fits the model. The main exception is learning parity functions, which needs [Gaussian elimination](/gaussian-elimination/) on single examples; a Fourier argument proves that no SQ learner can do it.

## The machine

**Setting.** Inputs come from a domain $X$ (here $\{0, 1\}^d$) with an unknown distribution $D$, and labels come from an unknown target $c \in C$, with $c : X \to \{0, 1\}$.

**The oracle.** A *statistical query* is a pair $(\chi, \tau)$, where $\chi : X \times \{0, 1\} \to [0, 1]$ is a function that can be evaluated in polynomial time, and $\tau > 0$ is the *tolerance*. The oracle $\mathrm{STAT}(c, D)$ returns some number $v$ with

$$\big| v - \mathbb{E}_{x \sim D}[\chi(x, c(x))] \big| \le \tau.$$

The oracle may choose any such $v$, so the learner must work for an adversarial oracle. Kearns uses $\{0, 1\}$-valued $\chi$; the $[0, 1]$-valued version is equivalent up to constant factors.

**The learner.** On input $\varepsilon$, the dimension $d$ and the size of the target, the learner asks queries (possibly chosen adaptively from earlier answers) and outputs a hypothesis $h$. It *SQ learns* $C$ if, for every $c \in C$, every $D$ and every valid oracle, $\Pr_{x \sim D}[h(x) \ne c(x)] \le \varepsilon$. It is *efficient* if the number of queries, $1/\tau$ for every query, and the running time are bounded by a polynomial in $1/\varepsilon$, $d$ and the size of $c$. There is no $\delta$: the oracle never fails, all the randomness is moved into the simulation below.

## What it counts

- **Queries**, $q$: the number of calls to STAT.
- **Tolerance**, $\tau$: the smallest tolerance used. A query with tolerance $\tau$ costs about $1/\tau^2$ examples when it is simulated, so $1/\tau$ is the real price of a query.
- **Time**, for choosing queries, evaluating $\chi$ and building $h$.

**Simulation from examples.** Given examples $(x, c(x))$ with $x \sim D$, answer each query with the mean of $\chi$ on

$$m = \Big\lceil \frac{\ln(2q/\delta)}{2\tau^2} \Big\rceil$$

fresh examples. By [Hoeffding's inequality](/hoeffding-inequality/) each answer is within $\tau$ except with probability $\delta/q$, so by the [union bound](/union-bound/) all $q$ answers are valid with probability $1 - \delta$. The total is $O(q \log(q/\delta)/\tau^2)$ examples. If the queries come from a fixed class of small VC dimension, one shared sample suffices (Kearns 1998).

## Relation to other models

- **SQ is inside PAC.** The simulation above turns an efficient SQ learner into an efficient PAC learner.
- **SQ is inside PAC with random classification noise.** In this model each label is flipped independently with probability $\eta < 1/2$. Write $s(x) = \chi(x, 0) + \chi(x, 1)$. A flipped label turns $\chi(x, c(x))$ into $\chi(x, 1 - c(x)) = s(x) - \chi(x, c(x))$, so

$$\mathbb{E}[\chi(x, y_{\text{noisy}})] = (1 - 2\eta)\, \mathbb{E}[\chi(x, c(x))] + \eta\, \mathbb{E}[s(x)].$$

Both $\mathbb{E}[\chi(x, y_{\text{noisy}})]$ and $\mathbb{E}[s(x)]$ can be estimated from noisy examples, since $s$ does not use the label. Estimate both to $t = \tau(1 - 2\eta)/2$ and solve for $\mathbb{E}[\chi(x, c(x))]$: the error is at most $t(1 + \eta)/(1 - 2\eta) = \tau(1 + \eta)/2 < \tau$. The cost grows as $1/(1 - 2\eta)^2$, polynomial as long as $\eta$ is bounded away from $1/2$. The code for this page assumes that $\eta$ is known; Kearns removes this by trying a grid of guesses for $\eta$ and testing the resulting hypotheses on held-out data.
- **SQ is strictly inside noisy PAC.** Blum, Kalai and Wasserman (2003) gave a class, parities on the first $O(\log d \log\log d)$ bits, that is learnable with random classification noise in polynomial time but is not SQ learnable.
- **Parity separates SQ from PAC.** Parity functions are PAC learnable without noise (solve a linear system over GF(2)), but not SQ learnable, as shown below. With noise, parity becomes [learning parity with noise](/learning-parity-with-noise/), which is believed hard and is used in cryptography.
- **Agnostic learning.** Queries can estimate the error of any fixed hypothesis, so SQ arguments also appear in [agnostic learning](/agnostic-pac-learning/), where the labels are arbitrary.

## Known results in the model

**Conjunctions are SQ learnable.** Let the target be a conjunction of literals over $d$ variables, and set $\tau = \varepsilon/(4d)$. For each of the $2d$ literals $\ell$, ask

$$p_\ell = \Pr[\ell(x) = 0 \text{ and } c(x) = 1], \qquad \chi_\ell(x, y) = \mathbf{1}[\ell(x) = 0 \wedge y = 1],$$

and keep $\ell$ if the answer is at most $\tau$. Output the conjunction $h$ of the kept literals.

*Proof.* A literal of the target is never false on a positive example, so its $p_\ell = 0$, its answer is at most $\tau$, and it is kept. So $h$ contains every literal of $c$, and $h(x) = 1$ implies $c(x) = 1$: there are no false positives. A kept literal has answer at most $\tau$, so $p_\ell \le 2\tau$. A false negative is an $x$ with $c(x) = 1$ where some kept literal is false, so the error is at most $\sum_{\ell \text{ kept}} p_\ell \le 2d \cdot 2\tau = \varepsilon$. $\blacksquare$

The learner uses $2d$ queries of tolerance $\varepsilon/(4d)$, so by the simulation above it also learns conjunctions from noisy labels. The code for this page checks it against oracles that move every answer by $+\tau$, by $-\tau$ or by a random sign, with exact errors by enumeration. With $d = 8$, $\varepsilon = 0.2$, the target $x_0 \wedge \neg x_2 \wedge x_4$ and a product distribution where $x_1 = 1$ with probability $0.97$ and $x_7 = 1$ with probability $0.99$, the oracle that answers $-\tau$ makes the learner keep the extra literals $x_1$ and $x_7$; the error is $0.0133 \le 0.2$, and all of it is false negatives. With $d = 3$, $\varepsilon = 0.5$, $\delta = 0.1$ and the target $x_0 \wedge \neg x_1$, the simulation uses 8274 clean examples in total, or 420918 examples with label noise $\eta = 0.2$; both runs return the target. Such counts are worst-case guarantees and are much larger than what the learner needs in practice.

**Other SQ learnable classes.** Kearns (1998) observed that most PAC algorithms of the time can be rewritten with statistical queries. Examples are $k$-CNF (treat each clause of at most $k$ literals as a new variable and learn a conjunction of them) and decision lists. Halfspaces in general are learnable with random classification noise by an SQ form of the [perceptron](/perceptron/) (Blum, Frieze, Kannan and Vempala 1998; see [halfspace learning](/halfspace-learning/)).

**Parity is not SQ learnable.** Let $D$ be uniform on $\{0, 1\}^d$ and let the targets be the $2^d$ parities $c_S(x) = \sum_{i \in S} x_i \bmod 2$. Every deterministic SQ learner that, for every $S$, outputs $h$ with error below $1/4$ must make at least

$$q \ge 4\tau^2 (2^d - 1)$$

queries, where $\tau$ is the largest tolerance it uses. With $\tau \ge 1/\mathrm{poly}(d)$ this is exponential in $d$.

*Proof.* Write a query as $\chi(x, y) = g(x) + y\, h(x)$ with $g(x) = \chi(x, 0)$ and $h(x) = \chi(x, 1) - \chi(x, 0) \in [-1, 1]$. Since $c_S(x) = (1 - (-1)^{S \cdot x})/2$,

$$\mathbb{E}[\chi(x, c_S(x))] = \mathbb{E}[g] + \tfrac12 \mathbb{E}[h] - \tfrac12 \hat h(S), \qquad \hat h(S) = \mathbb{E}[h(x)(-1)^{S \cdot x}],$$

where $\hat h(S)$ is a [Fourier coefficient](/fourier-analysis-of-boolean-functions/) of $h$. Let the oracle always answer $\mathbb{E}[g] + \frac12 \mathbb{E}[h]$, which does not depend on $S$. This answer is valid for target $c_S$ whenever $|\hat h(S)| \le 2\tau$. By Parseval, $\sum_S \hat h(S)^2 = \mathbb{E}[h^2] \le 1$, so at most $1/(4\tau^2)$ sets $S$ have $|\hat h(S)| > 2\tau$. Each query therefore rules out at most $1/(4\tau^2)$ targets, and after $q$ queries at least $2^d - q/(4\tau^2)$ targets are consistent with every answer. If two targets $c_S \ne c_{S'}$ remain, the learner saw the same answers for both and outputs the same $h$, and since $c_S$ and $c_{S'}$ differ on exactly half of the inputs, $h$ has error at least $1/4$ on one of them. So the learner needs $2^d - q/(4\tau^2) \le 1$. $\blacksquare$

The tests for this page check the identity for the answers, Parseval, and the count of ruled out parities for random queries and for queries that test one parity. Blum, Furst, Jackson, Kearns, Mansour and Rudich (1994) generalized this argument: the *SQ dimension* of a class under $D$ is the largest number of functions in it that are pairwise nearly uncorrelated, and even weak SQ learning needs a number of queries, or a $1/\tau$, polynomial in the SQ dimension. Parities have SQ dimension $2^d$. A consequence is that polynomial-size DNF and decision trees are not SQ learnable under the uniform distribution, because they contain parities on $O(\log d)$ variables, which already give a superpolynomial SQ dimension.

**Lower bounds for other problems.** SQ lower bounds are now used as evidence of hardness for problems where computational lower bounds are out of reach, such as planted clique and robust estimation in high dimension, because most known algorithms for these problems, including gradient methods with noisy gradients, can be written with statistical queries.

## References
