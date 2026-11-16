---
tag: 8NEH7C
kind: definition
slug: probabilistically-checkable-proof
name: Probabilistically checkable proof
aliases:
- PCP
- PCP(r,q)
area: complexity/complexity-classes
level: advanced
summary: "A proof string that a polynomial-time verifier checks with r(n) random bits and q(n) queries. PCP(r, q) has completeness 1 and soundness 1/2; NP = PCP(log n, 1)."
prereqs: [np, polynomial-time-verifier, probabilistic-turing-machine]
see_also: [pcp-theorem, interactive-proofs, multi-prover-interactive-proofs, mip-equals-nexp, hastad-3bit-pcp, gap-problem, hadamard-code, linearity-test]
sources:
  - paper: doi:10.1145/273865.273901
    title: Sanjeev Arora and Shmuel Safra, Probabilistic checking of proofs, a new characterization of NP, Journal of the ACM 45(1), 70 to 122 (1998)
    locator: the definition of the classes PCP(r, q); preliminary version in FOCS 1992, 2 to 12
  - paper: doi:10.1145/278298.278306
    title: Sanjeev Arora, Carsten Lund, Rajeev Motwani, Madhu Sudan and Mario Szegedy, Proof verification and the hardness of approximation problems, Journal of the ACM 45(3), 501 to 555 (1998)
    locator: NP = PCP(log n, 1), and the verifier based on the Hadamard code; preliminary version in FOCS 1992
  - paper: doi:10.1145/226643.226652
    title: Uriel Feige, Shafi Goldwasser, László Lovász, Shmuel Safra and Mario Szegedy, Interactive proofs and the hardness of approximating cliques, Journal of the ACM 43(2), 268 to 292 (1996)
    locator: verifiers with bounded randomness and queries, and the reduction from a verifier to a clique gap
  - paper: doi:10.1007/BF01200056
    title: László Babai, Lance Fortnow and Carsten Lund, Non-deterministic exponential time has two-prover interactive protocols, Computational Complexity 1(1), 3 to 40 (1991)
    locator: NEXP has polynomial-time oracle verifiers, which gives PCP(poly, poly) = NEXP
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 11, PCP theorem and hardness of approximation, an introduction (the definition of PCP verifiers and the classes PCP(r, q))
---

A probabilistically checkable proof (PCP) is a proof string that a randomized polynomial-time verifier checks by reading only a few of its bits. The class $\mathsf{PCP}(r(n), q(n))$ contains the languages whose yes-instances have proofs that the verifier, with $O(r(n))$ random bits and $O(q(n))$ queries, always accepts, while for a no-instance every string is rejected with probability at least $1/2$. The two parameters give a scale between NP, where the verifier reads the whole proof, and fast randomized checking. The [PCP theorem](/pcp-theorem/) says that $\mathsf{NP} = \mathsf{PCP}(\log n, 1)$.

## Definition

**Verifier.** A *PCP verifier* $V$ is a probabilistic polynomial-time [multitape Turing machine](/multitape-turing-machine/) that has the input $x$, a random string $\rho$ of $r(|x|)$ bits and *oracle access* to a proof $\pi \in \{0,1\}^*$: it can write an index $i$ and read the bit $\pi_i$ in one step. On each $\rho$ it reads at most $q(|x|)$ bits of $\pi$ and then accepts or rejects. The verifier is *non-adaptive* if it computes all the indices from $x$ and $\rho$ before it reads any bit, and *adaptive* if later indices may depend on earlier bits. Write $V^\pi(x)$ for the output; it is a random variable over $\rho$.

**Definition.** A language $L$ is in $\mathsf{PCP}_{c,s}[r, q]$ if there is a non-adaptive verifier with $r(n)$ random bits and $q(n)$ queries such that

$$x \in L \Rightarrow \exists \pi : \Pr_\rho\big[V^\pi(x) = 1\big] \ge c, \qquad x \notin L \Rightarrow \forall \pi : \Pr_\rho\big[V^\pi(x) = 1\big] \le s.$$

The standard class is $\mathsf{PCP}(r, q) = \bigcup_{a > 0} \mathsf{PCP}_{1, 1/2}[a \cdot r, a \cdot q]$, with *perfect completeness* $c = 1$ and *soundness* $s = 1/2$. So $\mathsf{PCP}(\log n, 1)$ means $O(\log n)$ random bits and a constant number of queries.

**Remarks on the definition.**

- *Proof length.* On all $2^{r}$ random strings together, $V$ reads at most $q \cdot 2^{r}$ positions, so only that many bits of $\pi$ matter. With $r = O(\log n)$ and $q = O(1)$ the proof has polynomial length.
- *Soundness constant.* Running the verifier $k$ times with fresh random bits and accepting if all runs accept gives $\mathsf{PCP}_{1, s^k}[kr, kq]$. So any constant $s < 1$ gives the same class $\mathsf{PCP}(r, q)$. A soundness of the form $1 - 1/n$ does not, because it needs about $n$ repetitions.
- *Adaptivity.* An adaptive verifier with $q$ queries can be made non-adaptive with at most $2^q$ queries, by reading every position that some answers to the earlier queries could lead to. For $q = O(1)$ the classes are the same.
- *Comparison with interactive proofs.* A proof string is a prover that is fixed in advance: it cannot change an answer after seeing the other questions. This is the oracle form of [multi-prover interactive proofs](/multi-prover-interactive-proofs/) by Fortnow, Rompel and Sipser.

**Upper bound.** $\mathsf{PCP}(r, q) \subseteq \mathsf{NTIME}\big(2^{O(r(n))} \cdot \mathrm{poly}(n)\big)$.

*Proof.* Let $V$ use $a \cdot r$ random bits. A nondeterministic machine runs $V$ on $x$ for each of the $2^{a r}$ random strings and lists the at most $2^{ar} \cdot aq$ queried positions; since $V$ runs in polynomial time, $q$ is at most polynomial. It guesses one bit for each listed position, and accepts if $V$ accepts on every random string with these bits. If $x \in L$, the restriction of a correct proof makes every run accept, by perfect completeness. If $x \notin L$, every proof is rejected on at least half of the random strings, so every guess leads to rejection. The time is $2^{O(r)} \cdot \mathrm{poly}(n)$. $\square$

## Examples and non-examples

**Known classes.**

| class | equals | reason |
|---|---|---|
| $\mathsf{PCP}(0, 0)$ | P | no randomness and no proof: a polynomial-time machine |
| $\mathsf{PCP}(\log n, 0)$ | P | run all $2^{O(\log n)}$ random strings |
| $\mathsf{PCP}(0, \log n)$ | P | try all $2^{O(\log n)}$ proofs |
| $\mathsf{PCP}(\mathrm{poly}, 0)$ | coRP | randomized, no proof, one-sided error on no-instances |
| $\mathsf{PCP}(0, \mathrm{poly})$ | NP | the verifier reads a certificate deterministically |
| $\mathsf{PCP}(\log n, 1)$ | NP | the [PCP theorem](/pcp-theorem/) |
| $\mathsf{PCP}(\mathrm{poly}, \mathrm{poly})$ | NEXP | [MIP = NEXP](/mip-equals-nexp/) |

The inclusions "$\subseteq$" in the first, second, third and fifth rows follow from the upper bound above, or from running the verifier directly. The $\supseteq$ direction of $\mathsf{PCP}(\log n, 1) = \mathsf{NP}$ is the hard part of the PCP theorem.

**Examples.**

- *The clause verifier for 3-SAT.* The proof is an assignment to the $n$ variables of a 3-CNF formula with $m$ clauses. The verifier uses $\lceil \log_2 m \rceil$ random bits to pick a clause, reads its $3$ variables and accepts if the clause is satisfied. A satisfying assignment is always accepted. But an unsatisfiable formula may have an assignment that violates only $1$ clause, so the soundness is only $1 - 1/m$, and reaching $1/2$ needs about $0.69\, m$ repetitions, that is $O(m \log m)$ random bits and $O(m)$ queries. The PCP theorem is exactly the statement that 3-SAT instances can be first transformed so that this simple verifier has constant soundness; see [gap problems](/gap-problem/).
- *A worked case.* Take the $8$ clauses on $x_1, x_2, x_3$ with all sign patterns. Every assignment violates exactly one clause, so the clause verifier with $3$ random bits and $3$ queries accepts every proof with probability exactly $7/8$. With $k$ independent runs the acceptance probability is $(7/8)^k$: $0.875$, $0.766$, $0.670$, $0.586$ and $0.513$ for $k = 1, \ldots, 5$, and $0.449$ for $k = 6$. So $6$ runs, with $18$ random bits and $18$ queries, give soundness below $1/2$.
- *The Hadamard verifier.* Arora, Lund, Motwani, Sudan and Szegedy gave a verifier for an NP-complete problem with a proof of exponential length: the [Hadamard code](/hadamard-code/) of an assignment and of its tensor square. It uses $\mathrm{poly}(n)$ random bits and a constant number of queries, with a [linearity test](/linearity-test/) and a consistency check. So $\mathsf{NP} \subseteq \mathsf{PCP}(\mathrm{poly}, 1)$. This verifier is the inner verifier of their proof of the PCP theorem.
- *Optimal three-bit verifiers.* Håstad's verifier reads $3$ bits and checks one linear equation, with completeness $1 - \varepsilon$ and soundness $1/2 + \varepsilon$; see [Håstad's 3-bit PCP](/hastad-3bit-pcp/).

**Non-examples.**

- *Interactive proofs.* In an [interactive proof](/interactive-proofs/) the prover answers after it sees the verifier's messages, so it is not a fixed string. The difference shows in the classes: with polynomial randomness and polynomially many queries, a fixed proof gives NEXP, while one adaptive prover gives only $\mathsf{IP} = \mathsf{PSPACE}$. A fixed string cannot cheat by adapting its answers, so the verifier can trust more of it.
- *Soundness that tends to $1$.* A verifier with soundness $1 - 1/m$, such as the clause verifier above, does not show membership in $\mathsf{PCP}(\log n, 1)$.
- *Verifiers with imperfect completeness.* A verifier that may reject a correct proof is in $\mathsf{PCP}_{c,s}$ with $c < 1$. Such verifiers are useful (Håstad's verifier is one), but they are not in the standard class without a separate argument.

## Related definitions

- The [PCP theorem](/pcp-theorem/) states $\mathsf{NP} = \mathsf{PCP}(\log n, 1)$ and is equivalent to the NP-hardness of a gap version of MAX 3-SAT.
- [Multi-prover interactive proofs](/multi-prover-interactive-proofs/) are the interactive form; a fixed proof string is the oracle in the Fortnow, Rompel and Sipser view.
- A [two-prover one-round game](/two-prover-one-round-game/) is a PCP with $2$ queries over a large alphabet, and [label cover](/label-cover/) is its constraint form.
- [Locally decodable codes](/locally-decodable-codes/) and [low-degree tests](/low-degree-test/) are the coding tools of PCP constructions.
- The FGLSS reduction turns a PCP verifier into a graph whose clique number reflects the acceptance probability; see [clique inapproximability](/clique-inapproximability/).

## References
