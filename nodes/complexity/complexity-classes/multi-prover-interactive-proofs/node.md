---
tag: 57XBNW
kind: definition
slug: multi-prover-interactive-proofs
name: MIP
area: complexity/complexity-classes
level: research
summary: "Multi-prover interactive proofs (MIP): a polynomial-time verifier questions two or more provers that cannot communicate. MIP = NEXP; with entangled provers, MIP* = RE."
prereqs: [interactive-proofs, nexptime]
see_also: [mip-equals-nexp, interactive-proofs, two-prover-one-round-game, parallel-repetition-theorem, probabilistically-checkable-proof, chsh-inequality, entanglement, qma]
sources:
  - paper: doi:10.1145/62212.62223
    title: Michael Ben-Or, Shafi Goldwasser, Joe Kilian and Avi Wigderson, Multi-prover interactive proofs, how to remove intractability assumptions, Proceedings of the 20th Annual ACM Symposium on Theory of Computing, 113 to 131 (1988)
    locator: the definition of multi-prover interactive proofs, and two provers suffice
  - paper: doi:10.1016/0304-3975(94)90251-8
    title: Lance Fortnow, John Rompel and Michael Sipser, On the power of multi-prover interactive protocols, Theoretical Computer Science 134(2), 545 to 557 (1994)
    locator: the characterization by probabilistic oracle machines, and MIP in NEXP; preliminary version in Structure in Complexity Theory 1988
  - paper: doi:10.1007/BF01200056
    title: László Babai, Lance Fortnow and Carsten Lund, Non-deterministic exponential time has two-prover interactive protocols, Computational Complexity 1(1), 3 to 40 (1991)
    locator: the main theorem, NEXP in MIP
  - paper: doi:10.1145/129712.129783
    title: Uriel Feige and László Lovász, Two-prover one-round proof systems, their power and their problems, Proceedings of the 24th Annual ACM Symposium on Theory of Computing, 733 to 744 (1992)
    locator: NEXP has two-prover proofs with one round
  - paper: arxiv:2001.04383
    title: Zhengfeng Ji, Anand Natarajan, Thomas Vidick, John Wright and Henry Yuen, MIP* = RE (2020)
    locator: the main theorem, and the consequence for the Connes embedding problem
---

Multi-prover interactive proofs (MIP) are [interactive proofs](/interactive-proofs/) in which a randomized polynomial-time verifier talks with two or more provers that cannot communicate with each other during the protocol. The class MIP is the set of languages that have such proofs. Ben-Or, Goldwasser, Kilian and Wigderson defined the model in 1988. Separate provers are much stronger than one: the verifier can ask the same thing in two ways and compare the answers, the way the police question two suspects in separate rooms. Babai, Fortnow and Lund proved that [MIP = NEXP](/mip-equals-nexp/).

## Definition

**Model.** There are $k \ge 2$ provers $P_1, \ldots, P_k$ of unlimited power and a verifier $V$, a probabilistic polynomial-time [multitape Turing machine](/multitape-turing-machine/). Before the protocol starts the provers can agree on a strategy, but after it starts each prover $P_i$ sees only $x$ and the messages that $V$ sends to it. Each answer of $P_i$ is a function of $x$ and of the messages to $P_i$ so far. The verifier's coins are private. The protocol has polynomially many rounds, and at the end $V$ accepts or rejects. Shared randomness does not help the provers, because for every fixed value of it they play a deterministic strategy, and one of these is at least as good as the average.

**Definition.** A language $L$ is in $\mathsf{MIP}$ if there is such a verifier, with a polynomial number of provers and rounds, such that

$$x \in L \Rightarrow \exists P_1, \ldots, P_k : \Pr\big[V \text{ accepts}\big] \ge \tfrac23, \qquad x \notin L \Rightarrow \forall P_1^*, \ldots, P_k^* : \Pr\big[V \text{ accepts}\big] \le \tfrac13.$$

The same class results with completeness $1$.

**Facts about the definition.**

- *One prover gives IP.* With $k = 1$ the definition is the definition of IP, so $\mathsf{MIP}[1] = \mathsf{IP} = \mathsf{PSPACE}$.
- *Two provers suffice.* Ben-Or, Goldwasser, Kilian and Wigderson showed that every protocol with $k$ provers can be turned into one with $2$ provers.
- *Oracles.* Fortnow, Rompel and Sipser showed that $L \in \mathsf{MIP}$ if and only if a probabilistic polynomial-time oracle machine accepts $L$ in the following sense: on $x \in L$ some oracle makes it accept with probability at least $2/3$, and on $x \notin L$ every oracle makes it accept with probability at most $1/3$. An oracle is a prover that is fixed in advance and cannot adapt its answers to earlier questions. To turn an oracle protocol into a two-prover protocol, the verifier asks all its queries to $P_1$, then asks $P_2$ one of them at random and rejects if the answers differ. $P_2$ is asked only once, so its answer is a fixed function of the question, that is, an oracle. Let $O$ be the function that $P_2$ computes. If the answers of $P_1$ make $V$ accept but the answers of $O$ would not, then $P_1$ and $O$ differ on some query, and the check picks it with probability at least $1/q$ for $q$ queries. So the error is at most $1 - (1 - s)/q$, where $s$ is the error of the oracle machine, and repetition makes it small. This view leads to [probabilistically checkable proofs](/probabilistically-checkable-proof/).
- *One round suffices.* Feige and Lovász (1992) showed that NEXP, and so all of MIP, has two-prover proofs with one round: the verifier sends one question to each prover and gets one answer from each. These are [two-prover one-round games](/two-prover-one-round-game/).
- *Repetition.* Sequential repetition reduces the error as for one prover. Parallel repetition, which keeps one round, also reduces it, but the proof is hard and the rate depends on the answer length; see the [parallel repetition theorem](/parallel-repetition-theorem/).

## Examples and non-examples

**Examples.**

- *The clause-variable game.* Let $\varphi$ be a 3-CNF formula with $m$ clauses. The verifier picks a uniform clause $C$ and a uniform variable $v$ of $C$. It asks $P_1$ for values of the three variables of $C$ and asks $P_2$ for the value of $v$. It accepts if the values from $P_1$ satisfy $C$ and agree with $P_2$ on $v$. If $\varphi$ is satisfiable, both provers answer from one satisfying assignment and win with probability $1$. If $\varphi$ is unsatisfiable, the answers of $P_2$ form an assignment $a$, and $a$ violates some clause. That clause is chosen with probability at least $1/m$; then the answer of $P_1$ satisfies it, so it differs from $a$ on some variable of the clause, and that variable is chosen with probability at least $1/3$. So the provers win with probability at most $1 - 1/(3m)$.
- *A worked case.* Take the $8$ clauses on $x_1, x_2, x_3$ with all sign patterns, which no assignment satisfies, so $m = 8$. Exhaustive search over the $8$ deterministic strategies of $P_2$, each with the best answers of $P_1$, gives the value $23/24$, which equals the bound $1 - 1/(3 \cdot 8)$. A single prover that receives both questions wins with probability $1$: it answers with any assignment that satisfies $C$ and repeats its value for $v$. The separation of the provers is what makes the game sound.
- *Every language in NEXP.* By [MIP = NEXP](/mip-equals-nexp/). The proof applies the oracle view to an exponentially long proof that is encoded as a low-degree polynomial.

**Non-examples.**

- *Languages outside NEXP.* Since $\mathsf{MIP} \subseteq \mathsf{NEXP}$, an EXPSPACE-complete language is in MIP only if $\mathsf{EXPSPACE} = \mathsf{NEXP}$, and an undecidable language is never in MIP.
- *Provers that share entanglement.* If the provers share an entangled quantum state ([entanglement](/entanglement/)) and may measure it, the class is $\mathsf{MIP}^*$, not MIP. Entanglement can raise the value of a game: in the CHSH game the best classical value is $3/4$, and entangled provers reach $\cos^2(\pi/8) \approx 0.854$ ([CHSH inequality](/chsh-inequality/)). So a classical MIP protocol can lose soundness against entangled provers. Ji, Natarajan, Vidick, Wright and Yuen (2020) proved $\mathsf{MIP}^* = \mathsf{RE}$: the [halting problem](/halting-problem/) has a two-prover one-round proof with entangled provers. Since MIP = NEXP contains only decidable languages, $\mathsf{MIP}^*$ is strictly larger than MIP. As a consequence, they refuted the Connes embedding conjecture.
- *Provers that can communicate.* If the provers can talk during the protocol, they act as one prover, and the class is IP.

## Related definitions

- [IP](/interactive-proofs/) is the case of one prover. It equals PSPACE.
- A [probabilistically checkable proof](/probabilistically-checkable-proof/) is the oracle form with the verifier's randomness and number of queries counted. $\mathsf{PCP}(\mathrm{poly}, \mathrm{poly}) = \mathsf{NEXP}$ is the oracle form of MIP = NEXP.
- A [two-prover one-round game](/two-prover-one-round-game/) is the one-round form, and its value is the best acceptance probability of the provers. Gap versions of it start many hardness of approximation proofs.
- [QMA](/qma/) is a quantum class with one message from one prover; $\mathsf{MIP}^*$ keeps a classical verifier and gives the provers entanglement.

## References
