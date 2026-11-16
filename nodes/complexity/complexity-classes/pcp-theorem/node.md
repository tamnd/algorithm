---
tag: GE86ZW
kind: theorem
slug: pcp-theorem
name: PCP theorem
aliases:
- Arora-Safra theorem
- NP = PCP(log n, 1)
area: complexity/complexity-classes
level: research
summary: "NP = PCP(O(log n), O(1)): every NP statement has a proof that a verifier checks with O(log n) random bits and O(1) queries, with completeness 1 and soundness 1/2."
prereqs: [probabilistically-checkable-proof, np-complete, 3-sat]
see_also: [probabilistically-checkable-proof, gap-problem, max-3sat-inapproximability, hastad-3bit-pcp, gap-amplification, label-cover, clique-inapproximability, mip-equals-nexp]
sources:
  - paper: doi:10.1145/273865.273901
    title: Sanjeev Arora and Shmuel Safra, Probabilistic checking of proofs, a new characterization of NP, Journal of the ACM 45(1), 70 to 122 (1998)
    locator: NP is characterized by verifiers with logarithmic randomness and sublogarithmic queries, and proof composition; preliminary version in FOCS 1992, 2 to 12
  - paper: doi:10.1145/278298.278306
    title: Sanjeev Arora, Carsten Lund, Rajeev Motwani, Madhu Sudan and Mario Szegedy, Proof verification and the hardness of approximation problems, Journal of the ACM 45(3), 501 to 555 (1998)
    locator: NP = PCP(log n, 1), and the consequence that MAX 3SAT has no polynomial-time approximation scheme unless P = NP; preliminary version in FOCS 1992
  - paper: doi:10.1145/1236457.1236459
    title: Irit Dinur, The PCP theorem by gap amplification, Journal of the ACM 54(3), article 12 (2007)
    locator: the combinatorial proof by gap amplification; preliminary version in STOC 2006
  - paper: doi:10.1145/226643.226652
    title: Uriel Feige, Shafi Goldwasser, László Lovász, Shmuel Safra and Mario Szegedy, Interactive proofs and the hardness of approximating cliques, Journal of the ACM 43(2), 268 to 292 (1996)
    locator: the link between proof checking and approximation; preliminary version in FOCS 1991
  - paper: doi:10.1145/103418.103428
    title: László Babai, Lance Fortnow, Leonid A. Levin and Mario Szegedy, Checking computations in polylogarithmic time, Proceedings of the 23rd Annual ACM Symposium on Theory of Computing, 21 to 32 (1991)
    locator: proofs for NP checked in polylogarithmic time
  - paper: doi:10.1145/502090.502098
    title: Johan Håstad, Some optimal inapproximability results, Journal of the ACM 48(4), 798 to 859 (2001)
    locator: the three-query verifier with completeness 1 - epsilon and soundness 1/2 + epsilon
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 11, PCP theorem and hardness of approximation, an introduction (the statement and the equivalence with gap problems); Chapter 22, Proofs of PCP theorems and the Fourier transform technique (Dinur's proof)
---

The PCP theorem says that $\mathsf{NP} = \mathsf{PCP}(O(\log n), O(1))$: every NP statement has a proof that a randomized verifier can check by reading a constant number of its bits, with $O(\log n)$ random bits, so that a correct proof is always accepted and a wrong claim is rejected with probability at least $1/2$. An equivalent form is that for some constant $\varepsilon > 0$ it is NP-hard to tell a satisfiable 3-CNF formula from one in which every assignment violates at least an $\varepsilon$ fraction of the clauses. Arora and Safra and, building on their work, Arora, Lund, Motwani, Sudan and Szegedy proved it in 1992 with algebraic methods. Dinur gave a combinatorial proof in 2006.

## Statement

**Theorem (Arora and Safra; Arora, Lund, Motwani, Sudan and Szegedy).** $\mathsf{NP} = \mathsf{PCP}(\log n, 1)$.

In full: for every language $L \in \mathsf{NP}$ there are constants $a$ and $q$ and a non-adaptive [PCP verifier](/probabilistically-checkable-proof/) $V$, a probabilistic polynomial-time [multitape Turing machine](/multitape-turing-machine/) that uses $a \log_2 n$ random bits and reads $q$ bits of the proof, such that

- *completeness:* if $x \in L$, some proof $\pi$ makes $V$ accept with probability $1$;
- *soundness:* if $x \notin L$, every $\pi$ makes $V$ accept with probability at most $1/2$.

The soundness bound can be any constant in $(0, 1)$, with $q$ depending on it. The inclusion $\mathsf{PCP}(\log n, 1) \subseteq \mathsf{NP}$ is the easy part; it is proved on [probabilistically checkable proof](/probabilistically-checkable-proof/).

**Equivalent form.** For constants $0 < s < 1$, the promise problem $\text{gap-3SAT}[1, s]$ asks, for a 3-CNF formula, whether it is satisfiable or whether every assignment satisfies at most an $s$ fraction of its clauses ([gap problem](/gap-problem/)). The theorem is equivalent to: *there is a constant $\varepsilon > 0$ such that $\text{gap-3SAT}[1, 1 - \varepsilon]$ is NP-hard under polynomial-time many-one (Karp) reductions.*

## In plain words

Usually a checker must read a whole proof, because one wrong step can hide anywhere. The theorem says that every proof of a statement of the NP type can be rewritten, with only a polynomial growth in length, into a form that is very sensitive to errors. In the new form, a false claim cannot be supported by a proof that is wrong in only a few places: either the proof is right everywhere, or it is wrong in a large part. So a checker can pick a few random places, read a constant number of bits, and catch a false claim at least half of the time. Repeating the check makes the chance of being fooled as small as needed.

## Proof

The equivalence of the two forms is proved here in full. The hard inclusion $\mathsf{NP} \subseteq \mathsf{PCP}(\log n, 1)$ is given as a sketch in [proofs/main.md](proofs/main.md): the algebraic proof of Arora and Safra and of Arora, Lund, Motwani, Sudan and Szegedy, and the proof of Dinur by gap amplification.

### From verifiers to gap-3SAT

Assume $\mathsf{NP} \subseteq \mathsf{PCP}(\log n, 1)$. Since [3-SAT](/3-sat/) is NP-complete under Karp reductions ([NP-complete](/np-complete/)), it suffices to give a Karp reduction $f$ from 3-SAT to $\text{gap-3SAT}[1, 1 - \varepsilon]$. Let $V$ be a verifier for 3-SAT with $R = a \log_2 n$ random bits, $q$ queries, completeness $1$ and soundness $1/2$.

**The map $f$.** Given a formula $x$ of size $n$, for each random string $\rho \in \{0,1\}^R$:

1. Run $V$ on $x$ and $\rho$ to find the $q$ positions $i_1, \ldots, i_q$ that it reads. Each position of the proof becomes a Boolean variable $y_i$.
2. For each of the $2^q$ values of $(y_{i_1}, \ldots, y_{i_q})$, run $V$ to see whether it accepts. This gives the acceptance predicate $\phi_\rho$ as a CNF formula with at most $2^q$ clauses of width $q$: one clause excludes each rejected value.
3. Replace each clause $(\ell_1 \lor \cdots \lor \ell_q)$ of width $q > 3$ by the $q - 2$ clauses $(\ell_1 \lor \ell_2 \lor z_1), (\lnot z_1 \lor \ell_3 \lor z_2), \ldots, (\lnot z_{q-3} \lor \ell_{q-1} \lor \ell_q)$ with new variables $z_j$ for that clause.

$f(x)$ is the conjunction of the 3-CNF formulas of all $\rho$.

**Cost.** There are $2^R = n^a$ random strings, and each gives at most $K = q\, 2^q$ clauses, a constant. So $f(x)$ has at most $K n^a$ clauses, and computing it takes $2^q n^a$ runs of $V$, which is polynomial time.

**If $x$ is satisfiable, $f(x)$ is satisfiable.** Take a proof $\pi$ that $V$ accepts on every $\rho$, and set $y_i = \pi_i$. Then every $\phi_\rho$ holds, so in each width-$q$ clause some literal is true, and the variables $z_j$ can be set so that every clause of its chain holds.

**If $f(x)$ has an assignment that satisfies more than a $1 - 1/(2K)$ fraction of the clauses, then $x$ is satisfiable.** Take an arbitrary assignment to $f(x)$ and read off $\pi_i = y_i$. If $x$ were unsatisfiable, then by soundness $V$ would reject $\pi$ on at least $2^{R-1}$ strings $\rho$. For each such $\rho$ some width-$q$ clause of $\phi_\rho$ is false under $\pi$, and then its chain contains a false clause for every value of the $z_j$, because the chain can only be satisfied when one of the $\ell_k$ is true. So at least $2^{R-1}$ of the at most $K 2^R$ clauses are false, a fraction of at least $1/(2K)$. Contrapositively, if more than a $1 - 1/(2K)$ fraction can be satisfied, $x$ is satisfiable.

So $f$ is a Karp reduction to $\text{gap-3SAT}[1, 1 - \varepsilon]$ with $\varepsilon = 1/(2 q\, 2^q)$.

### From gap-3SAT to verifiers

Assume a Karp reduction $f$ from 3-SAT to $\text{gap-3SAT}[1, 1 - \varepsilon]$, and let $L \in \mathsf{NP}$. Compose the reduction from $L$ to 3-SAT with $f$; this maps $x$ to a formula $\psi$ with $m \le \mathrm{poly}(n)$ clauses. The proof is an assignment to $\psi$. The verifier computes $\psi$, picks a clause with $\lceil \log_2 m \rceil = O(\log n)$ random bits, reads its $3$ variables and accepts if the clause holds. If $x \in L$, a satisfying assignment is always accepted. If $x \notin L$, every assignment violates at least an $\varepsilon$ fraction of the clauses, so one run accepts with probability at most $1 - \varepsilon$. With $k = \lceil \ln 2 / \varepsilon \rceil$ independent runs, the acceptance probability is at most $(1 - \varepsilon)^k \le e^{-\varepsilon k} \le 1/2$. This uses $O(k \log n) = O(\log n)$ random bits and $3k = O(1)$ queries. $\square$

### Worked example

Take $5$ variables and the $8$ parity equations over $\mathrm{GF}(2)$:

$$\begin{aligned} &x_1 + x_3 + x_4 = 0, \quad x_2 + x_4 + x_5 = 1, \quad x_1 + x_2 + x_5 = 1, \quad x_2 + x_3 + x_5 = 0, \\ &x_1 + x_3 + x_5 = 0, \quad x_3 + x_4 + x_5 = 1, \quad x_1 + x_2 + x_3 = 1, \quad x_2 + x_3 + x_4 = 1. \end{aligned}$$

A verifier with $3$ random bits picks one equation, reads its $3$ variables and checks it; the proof is the $5$ bits. A search over all $32$ assignments shows that at most $7$ equations hold at once, so this system is a no-instance, and every proof is accepted with probability at most $7/8$.

*The map.* Here $q = 3$, so no new variables are needed. Each equation becomes the $4$ clauses that exclude its $4$ wrong values; for $x_1 + x_3 + x_4 = 0$ these are $(x_1 \lor x_3 \lor \lnot x_4)$, $(x_1 \lor \lnot x_3 \lor x_4)$, $(\lnot x_1 \lor x_3 \lor x_4)$ and $(\lnot x_1 \lor \lnot x_3 \lor \lnot x_4)$. The formula has $32$ clauses.

*Both directions on this instance.* An assignment that satisfies an equation satisfies all $4$ of its clauses, and an assignment that violates it violates exactly $1$ of them. The search confirms that for every one of the $32$ assignments, the number of satisfied clauses is $32$ minus the number of violated equations. So the best assignment, for example $x = (1, 0, 0, 1, 0)$, which violates only $x_1 + x_3 + x_5 = 0$, satisfies $31$ of the $32$ clauses, and no assignment does better: every assignment violates at least a $1/32$ fraction. Here $\varepsilon = 1/32$ is better than the general bound $1/(2 \cdot 3 \cdot 2^3) = 1/48$, because each equation rejects exactly half of its values.

## Consequences

- *Hardness of approximation.* The gap form says that MAX 3-SAT has no polynomial-time approximation scheme unless P = NP; see [MAX 3-SAT inapproximability](/max-3sat-inapproximability/). Through gap-preserving reductions this extends to many problems; see [APX-completeness](/apx-completeness/). [Håstad's 3-bit PCP](/hastad-3bit-pcp/) gives the optimal ratio $7/8 + \varepsilon$.
- *Clique and label cover.* With the FGLSS graph and [gap amplification](/gap-amplification/), maximum clique has no constant-factor approximation unless P = NP ([clique inapproximability](/clique-inapproximability/)). With parallel repetition, the theorem gives the NP-hardness of [label cover](/label-cover/) with any constant soundness.
- *Hypotheses for finer results.* The [unique games conjecture](/unique-games-conjecture/) and [Gap-ETH](/gap-eth/) are strengthenings that are not known to follow from the theorem.
- *Proof length.* The proof in the theorem has polynomial length. Dinur's method, combined with earlier work of Ben-Sasson and Sudan, gives proofs of length $n \cdot \mathrm{polylog}(n)$ with a constant number of queries.

## Tightness

- *Perfect completeness needs three queries.* With completeness $1$ and $2$ queries, each check is a constraint on $2$ bits, which is a [2-SAT](/2-sat/) clause set, so the language is in P by testing whether all checks can hold together. The same holds for $1$ query. So $3$ queries with completeness $1$ are needed unless P = NP, and the clause verifier above shows that $3$ suffice.
- *Perfect completeness and linear checks.* Håstad's verifier reads $3$ bits and checks one linear equation, with soundness $1/2 + \varepsilon$, but its completeness is $1 - \varepsilon$, not $1$. This is necessary unless P = NP: whether a system of linear equations over $\mathrm{GF}(2)$ is fully satisfiable is decided in polynomial time by [Gaussian elimination](/gaussian-elimination/). In the example above, elimination derives $0 = 1$, so it proves directly that the system has no solution, while it says nothing about how many equations can hold together.
- *Randomness.* With $o(\log n)$ random bits and $O(1)$ queries, only $n^{o(1)}$ proof bits matter, and trying all of them would solve 3-SAT in time $2^{n^{o(1)}}$. So $O(\log n)$ random bits are needed unless 3-SAT has such algorithms.

## History

The theorem came from a sequence of results on interactive proofs. Babai, Fortnow and Lund (1990) proved [MIP = NEXP](/mip-equals-nexp/), which says that exponentially long proofs can be checked in polynomial time. Babai, Fortnow, Levin and Szegedy (1991) scaled this down to NP with polylogarithmic checking time. Feige, Goldwasser, Lovász, Safra and Szegedy (1991) linked such verifiers to the hardness of approximating clique, with $O(\log n \log\log n)$ random bits and queries. Arora and Safra (FOCS 1992) introduced proof composition and characterized NP by verifiers with logarithmic randomness and sublogarithmic queries. Arora, Lund, Motwani, Sudan and Szegedy (FOCS 1992), using their work, reduced the queries to a constant and drew the consequences for approximation. Both papers appeared in the Journal of the ACM in 1998. Dinur (STOC 2006, journal 2007) gave a combinatorial proof by gap amplification.

## References
