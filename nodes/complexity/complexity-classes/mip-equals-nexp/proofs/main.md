---
title: MIP = NEXP, the easy inclusion in full and the hard inclusion as a sketch
proves: [statement]
status: sketch
---

This file proves $\mathsf{MIP} \subseteq \mathsf{NEXP}$ in full and gives $\mathsf{NEXP} \subseteq \mathsf{MIP}$ as a sketch. The sketch follows Babai, Fortnow and Lund (1991), the main theorem and its proof, with the oracle view of Fortnow, Rompel and Sipser (1994). It does not prove that oracle-3-satisfiability is NEXP-complete, it does not analyze the multilinearity test, it does not give the parameters of the self-correction step, and it does not track the error through repetition. These steps are in Babai, Fortnow and Lund.

## MIP is a subset of NEXP, in full

Let $L \in \mathsf{MIP}$ with a verifier $V$ that uses $k$ provers, $R$ rounds and $\ell$ random bits, all polynomial in $n = |x|$.

*Deterministic provers suffice.* Fix the strategies of all provers except $P_i$. If $P_i$ uses its own coins, the acceptance probability is an average over these coins, so some fixed value of the coins gives at least the average. Do this for each prover in turn. So the best acceptance probability is reached by deterministic provers.

*A strategy is a table.* A deterministic $P_i$ maps the sequence of messages that $V$ has sent to it to its next answer. These sequences have polynomial length, so there are at most $2^{p(n)}$ of them for a polynomial $p$, and the strategy is a table of $2^{p(n)}$ entries of polynomial length.

*The NEXP machine.* Guess the $k$ tables, in time $2^{O(p(n))}$. For each $r \in \{0,1\}^\ell$, simulate $V$ with coins $r$ and answer its questions by lookups in the tables; one simulation takes polynomially many steps, each lookup takes time $2^{O(p(n))}$ on a multitape machine. Count the $r$ that make $V$ accept and accept if the count is at least $\tfrac23 2^\ell$. The total time is $2^{\mathrm{poly}(n)}$.

*Correctness.* If $x \in L$, deterministic provers that reach acceptance probability at least $2/3$ exist, and the machine can guess their tables. If $x \notin L$, every choice of tables gives acceptance probability at most $1/3$, so every branch rejects. $\square$

## NEXP is a subset of MIP, a sketch

**Step 1: an oracle machine is enough.** By Fortnow, Rompel and Sipser, it suffices to give a probabilistic polynomial-time oracle machine $M$ such that some oracle makes $M$ accept every $x \in L$ with probability $1$, and every oracle makes $M$ accept $x \notin L$ with probability at most $1 - 1/\mathrm{poly}(n)$. The step from the oracle to two provers is on [multi-prover interactive proofs](/multi-prover-interactive-proofs/): $P_1$ answers all queries, $P_2$ answers one random query, and the verifier compares. Repetition then lowers the error below $1/3$.

**Step 2: a NEXP-complete problem.** An instance of *oracle-3-satisfiability* is a 3-CNF formula $B$ in $r + 3s + 3$ variables. It is a yes-instance if some function $A : \{0,1\}^s \to \{0,1\}$ makes

$$B(w, A(b_1), A(b_2), A(b_3)) = 1 \quad \text{for every } w = (z, b_1, b_2, b_3) \in \{0,1\}^{r + 3s}.$$

The function $A$ is an exponentially long string, and the condition says that $2^{r+3s}$ local constraints on it hold. Every language in NEXP reduces to this problem by a polynomial-time many-one reduction, by a Cook-Levin argument on the exponential tableau of the machine, with $A$ as the tableau and $B$ as the check of one window. This step is left out.

**Step 3: arithmetization.** Work over $\mathbb{F}_p$ for a prime $p$ of polynomially many bits. The honest oracle is the multilinear extension

$$\tilde A(y) = \sum_{b \in \{0,1\}^s} A(b) \prod_{i=1}^s \big(b_i y_i + (1 - b_i)(1 - y_i)\big), \qquad y \in \mathbb{F}_p^s,$$

which agrees with $A$ on $\{0,1\}^s$ and has degree at most $1$ in each variable. Let $\tilde B$ be the arithmetization of $B$ as in [IP = PSPACE](/ip-equals-pspace/), and let $g(w) = 1 - \tilde B(w, \tilde A(b_1), \tilde A(b_2), \tilde A(b_3))$. Then $A$ is a solution exactly when $\tilde A(b)(1 - \tilde A(b)) = 0$ for all $b \in \{0,1\}^s$ and $g(w) = 0$ for all $w \in \{0,1\}^{r+3s}$.

**Step 4: zero on the cube, by sum-check.** To check that a polynomial $h$ vanishes on $\{0,1\}^N$, the verifier picks a uniform $t \in \mathbb{F}_p^N$ and checks

$$\sum_{w \in \{0,1\}^N} h(w) \prod_{i=1}^N (1 - w_i + t_i w_i) = 0.$$

The left side is the multilinear polynomial $\sum_w h(w)\, t^w$ in $t$, whose coefficients are the values $h(w)$. If some value is nonzero, the polynomial is nonzero, and it vanishes at a random $t$ with probability at most $N/p$ by the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/). The sum is checked with the sum-check protocol. Its prover can also be an oracle: a query is the transcript so far, and the answer is the next univariate polynomial. At the end the verifier needs $h$ at one random point. For $h = g$ this means $\tilde A$ at three points of $\mathbb{F}_p^s$, so three queries.

**Step 5: the multilinearity test.** Steps 3 and 4 assume that the oracle is a multilinear polynomial, but a cheating oracle is an arbitrary function $f : \mathbb{F}_p^s \to \mathbb{F}_p$. The verifier picks random axis-parallel lines and checks that $f$ restricted to each is linear, as in the example on the theorem page. Babai, Fortnow and Lund prove that if $f$ passes with high probability, then $f$ agrees with some multilinear function on all but a small fraction of $\mathbb{F}_p^s$. This analysis is the core of their paper and is left out. Later work replaced it by [low-degree tests](/low-degree-test/).

**Step 6: self-correction.** If $f$ is close to a multilinear $\tilde A'$, the verifier still cannot trust $f$ at the three specific points of Step 4. To read $\tilde A'(y)$, it picks a random line through $y$, queries $f$ at $s + 1$ other points of the line, each of which is uniform in $\mathbb{F}_p^s$, interpolates the polynomial of degree at most $s$ on the line, and evaluates it at $y$. If every query hits a point where $f$ agrees with $\tilde A'$, the value is correct. The parameters are left out.

**Step 7: soundness.** If $B$ has no solution, then either $f$ is far from multilinear, and Step 5 rejects with noticeable probability, or $f$ is close to some multilinear $\tilde A'$. In the second case, $\tilde A'$ is not the extension of a solution, so one of the two zero tests of Step 4 has a nonzero coefficient, and the sum-check protocol with the self-corrected values rejects except with small probability. With the oracle-to-two-provers step and repetition, the error falls below $1/3$. Completeness is $1$, because the honest oracle passes every test. $\square$
