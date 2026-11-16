---
tag: 3NZ6Z2
kind: theorem
slug: mip-equals-nexp
name: MIP = NEXP
aliases:
- multi-prover characterization of NEXP
area: complexity/complexity-classes
level: research
summary: "Multi-prover interactive proofs with a polynomial-time verifier decide exactly the languages in NEXP (Babai, Fortnow and Lund 1991). Two provers and one round suffice."
prereqs: [multi-prover-interactive-proofs, ip-equals-pspace, nexptime]
see_also: [multi-prover-interactive-proofs, ip-equals-pspace, probabilistically-checkable-proof, pcp-theorem, low-degree-test, reed-muller-code, two-prover-one-round-game, relativization]
sources:
  - paper: doi:10.1007/BF01200056
    title: László Babai, Lance Fortnow and Carsten Lund, Non-deterministic exponential time has two-prover interactive protocols, Computational Complexity 1(1), 3 to 40 (1991)
    locator: the main theorem (NEXP in MIP), the multilinearity test and its analysis; preliminary version in FOCS 1990
  - paper: doi:10.1016/0304-3975(94)90251-8
    title: Lance Fortnow, John Rompel and Michael Sipser, On the power of multi-prover interactive protocols, Theoretical Computer Science 134(2), 545 to 557 (1994)
    locator: MIP in NEXP, and the equivalence of multi-prover protocols and probabilistic oracle machines
  - paper: doi:10.1145/62212.62223
    title: Michael Ben-Or, Shafi Goldwasser, Joe Kilian and Avi Wigderson, Multi-prover interactive proofs, how to remove intractability assumptions, Proceedings of the 20th Annual ACM Symposium on Theory of Computing, 113 to 131 (1988)
    locator: the definition of MIP and the reduction to two provers
  - paper: doi:10.1145/129712.129783
    title: Uriel Feige and László Lovász, Two-prover one-round proof systems, their power and their problems, Proceedings of the 24th Annual ACM Symposium on Theory of Computing, 733 to 744 (1992)
    locator: NEXP has two-prover one-round proofs with exponentially small error
  - paper: doi:10.1145/103418.103428
    title: László Babai, Lance Fortnow, Leonid A. Levin and Mario Szegedy, Checking computations in polylogarithmic time, Proceedings of the 23rd Annual ACM Symposium on Theory of Computing, 21 to 32 (1991)
    locator: the scaled-down form of the result for NP
  - paper: doi:10.1145/226643.226652
    title: Uriel Feige, Shafi Goldwasser, László Lovász, Shmuel Safra and Mario Szegedy, Interactive proofs and the hardness of approximating cliques, Journal of the ACM 43(2), 268 to 292 (1996)
    locator: the scaled-down protocol and its use for the hardness of approximating clique; preliminary version in FOCS 1991
---

The theorem MIP = NEXP says that the languages with a [multi-prover interactive proof](/multi-prover-interactive-proofs/) are exactly the languages accepted by a nondeterministic machine in exponential time ([NEXP](/nexptime/)). Babai, Fortnow and Lund proved the hard direction in 1990, at the same conference as [IP = PSPACE](/ip-equals-pspace/), with the same algebraic tools. The easy direction is due to Fortnow, Rompel and Sipser. The theorem shows that a verifier can check an exponentially long proof by reading a few of its symbols, which is the idea behind the [PCP theorem](/pcp-theorem/).

## Statement

**Theorem (Babai, Fortnow and Lund; Fortnow, Rompel and Sipser).** $\mathsf{MIP} = \mathsf{NEXP}$.

Here MIP is the class of languages that have an interactive proof with a probabilistic polynomial-time verifier on a [multitape Turing machine](/multitape-turing-machine/) and polynomially many provers that cannot communicate, with completeness at least $2/3$ and soundness error at most $1/3$. NEXP is $\bigcup_c \mathsf{NTIME}(2^{n^c})$. The proof gives a stronger form of the inclusion $\mathsf{NEXP} \subseteq \mathsf{MIP}$: two provers, perfect completeness and polynomially many rounds. Feige and Lovász (1992) reduced the protocol to one round with two provers and exponentially small error.

The provers here are classical. If they share entanglement, the class is $\mathsf{MIP}^*$, which equals RE and is a different result; see [multi-prover interactive proofs](/multi-prover-interactive-proofs/).

## In plain words

A prover wants to show that a huge puzzle has a solution, so huge that writing it out takes exponential time. The verifier cannot read the solution. It asks two provers who cannot talk to each other. The provers must describe the solution as a smooth algebraic object, so that an error in one place shows up almost everywhere. The verifier checks the smoothness at a few random places, then runs a counting protocol that needs the solution at only three random points. It asks one prover for these values and asks the other prover a single check question. A prover that lies must lie in a way that the other one cannot predict, so the lie is caught. The reverse direction is easier: a nondeterministic exponential-time machine can guess the provers' complete answer tables and compute the acceptance probability.

## Proof

The inclusion $\mathsf{MIP} \subseteq \mathsf{NEXP}$ is proved in full in [proofs/main.md](proofs/main.md). The provers can be taken deterministic, so their strategies are tables of exponential size. An NEXP machine guesses the tables, runs the verifier on all random strings, and accepts if at least $2/3$ of them accept.

The inclusion $\mathsf{NEXP} \subseteq \mathsf{MIP}$ is given there as a sketch, with each step named and the steps left out listed. It goes through probabilistic oracle machines (Fortnow, Rompel and Sipser), a succinct form of 3-SAT that is NEXP-complete, the multilinear extension of the assignment, the sum-check protocol of [IP = PSPACE](/ip-equals-pspace/), and the multilinearity test of Babai, Fortnow and Lund, which is the hard part. It closes with the step from an oracle to two provers.

**Worked example (the easy direction).** In the clause-variable game on the $8$ clauses over $x_1, x_2, x_3$ with all sign patterns, the first prover answers each clause with one of its $7$ satisfying assignments, so it has $7^8 = 5764801$ strategies, and the second prover has $2^3 = 8$. A machine that guesses one pair of tables and checks all $8 \cdot 3 = 24$ questions finds that the best pair wins on $23$ of them, so the value is $23/24$.

**Worked example (the multilinearity test).** A multilinear function on $\mathbb{F}_5^2$ is linear on every axis-parallel line. Pick one of the $10$ axis-parallel lines and $3$ distinct points on it at random, and reject if the three values are not collinear, which gives $100$ equally likely tests. For $f(x, y) = 2 + 3x + y + 4xy$ the test never rejects. If the value at one point is changed, the $12$ tests that use that point together with two other points on one of its two lines reject, a probability of $3/25$. For $f(x, y) = x^2$, which is quadratic in $x$, all $50$ tests on horizontal lines reject and none of the $50$ on vertical lines do, a probability of $1/2$.

## Consequences

- *Scaled-down versions give PCPs.* Babai, Fortnow, Levin and Szegedy (1991) scaled the protocol down to NP, with proofs checked in polylogarithmic time. The scaled-down form with $O(\log n)$ random bits leads to the [PCP theorem](/pcp-theorem/), and $\mathsf{PCP}(\mathrm{poly}, \mathrm{poly}) = \mathsf{NEXP}$ is the oracle form of this theorem ([probabilistically checkable proof](/probabilistically-checkable-proof/)).
- *Hardness of approximation.* The one-round form, together with scaling, gave the first results that some optimization problems are hard to approximate (Feige, Goldwasser, Lovász, Safra and Szegedy). See [two-prover one-round games](/two-prover-one-round-game/).
- *Interaction and nondeterminism.* With one prover, interaction gives PSPACE. With two, it gives NEXP. So the question whether a second prover adds power is the open question whether PSPACE differs from NEXP.
- *Low-degree tests.* The multilinearity test started the study of [low-degree tests](/low-degree-test/) for [Reed-Muller codes](/reed-muller-code/), which are used in all algebraic PCP constructions.

## Tightness

- *One prover is weaker, unless the classes collapse.* With one prover the class is PSPACE. A proof that one prover suffices for NEXP would give $\mathsf{NEXP} = \mathsf{PSPACE}$, which is not known to be false but would be a major collapse.
- *Entangled provers break the protocol.* The proof of soundness assumes that the provers' answers are fixed functions of their questions. Provers who share entanglement are not of this form, and for them the class is $\mathsf{MIP}^* = \mathsf{RE}$ (Ji, Natarajan, Vidick, Wright and Yuen 2020), which contains undecidable languages.
- *The test needs a large field.* The multilinearity test and the sum-check protocol need a field much larger than the degree. In the example above, the field $\mathbb{F}_5$ lets one changed point escape with probability $1 - 3/25 = 22/25$ per test. Real protocols use fields of size polynomial in the input length, or larger.

## History

Ben-Or, Goldwasser, Kilian and Wigderson (STOC 1988) defined multi-prover proofs, to get zero-knowledge proofs without assumptions about one-way functions, and showed that two provers suffice. Fortnow, Rompel and Sipser (Structure in Complexity Theory 1988, journal 1994) gave the oracle view and proved $\mathsf{MIP} \subseteq \mathsf{NEXP}$. After the arithmetization of Lund, Fortnow, Karloff and Nisan and the theorem of Shamir, Babai, Fortnow and Lund proved $\mathsf{NEXP} \subseteq \mathsf{MIP}$ at FOCS 1990. Babai, Fortnow, Levin and Szegedy, and Feige, Goldwasser, Lovász, Safra and Szegedy scaled the result down in 1991, and Feige and Lovász (1992) reduced it to one round. These steps led to the PCP theorem in 1992.

## References
