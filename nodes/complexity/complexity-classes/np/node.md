---
tag: 2GXX9T
kind: definition
slug: np
name: NP
aliases:
- nondeterministic polynomial time
area: complexity/complexity-classes
level: intro
summary: "Decision problems whose yes-instances have polynomial-length certificates that a polynomial-time verifier checks. Equivalently, problems a nondeterministic machine decides in polynomial time."
prereqs: [p, nondeterministic-turing-machine, decision-problem]
see_also: [p, co-np, np-complete, certificate, polynomial-time-verifier, p-versus-np-problem, cook-levin-theorem, fnp]
sources:
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 7.3, The class NP (verifiers, the equivalence with nondeterministic machines, CLIQUE and SUBSET-SUM)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach
    locator: Section 2.1, The class NP, with Section 2.1.2 on nondeterministic Turing machines
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity, Addison-Wesley, 1994
    locator: Chapter 9 (NP-complete problems) and Section 2.7 (nondeterministic machines)
  - paper: doi:10.1145/800157.805047
    title: Stephen A. Cook, The complexity of theorem-proving procedures, Proceedings of the 3rd Annual ACM Symposium on Theory of Computing (STOC 1971)
    locator: pp. 151 to 158
---

NP is the class of [decision problems](/decision-problem/) whose yes-instances have short proofs that are fast to check. A proof, or [certificate](/certificate/), has length polynomial in the input length, and a deterministic [polynomial-time verifier](/polynomial-time-verifier/) checks it. An equivalent definition uses a [nondeterministic Turing machine](/nondeterministic-turing-machine/) that runs in polynomial time. The name means "nondeterministic polynomial time", not "not polynomial": every problem in [P](/p/) is in NP, and whether $\mathsf{P} = \mathsf{NP}$ is the [P versus NP problem](/p-versus-np-problem/).

## Definition

Fix the alphabet $\{0, 1\}$ and write $|x|$ for the length of a string $x$. All machines are multitape Turing machines.

**By verifiers.** A language $L$ is in NP when there are a polynomial $p$ and a deterministic Turing machine $V$ that runs in time polynomial in $|x|$ on inputs $(x, u)$ with $|u| = p(|x|)$, such that for every string $x$

$$x \in L \iff \exists u \in \{0, 1\}^{p(|x|)} : V(x, u) = 1.$$

The string $u$ is a *certificate* (or *witness*) for $x$, and $V$ is the *verifier*. Two conditions matter. The certificate is short: its length is bounded by a polynomial in $|x|$. The check is fast: $V$ runs in time polynomial in $|x|$. Certificates of length at most $p(|x|)$ give the same class, because the verifier can ignore a padded tail.

**By nondeterministic machines.** For a function $f$, $\mathsf{NTIME}(f(n))$ is the set of languages decided by a nondeterministic Turing machine $N$ whose computation paths on every input $x$ all halt within $O(f(|x|))$ steps, and which accepts $x$ when at least one path accepts. Then

$$\mathsf{NP} = \bigcup_{k \ge 1} \mathsf{NTIME}(n^k).$$

**The two definitions agree.** Suppose that $L$ has a verifier $V$ with certificate length $p(n)$ and running time $t(n)$, a polynomial. A nondeterministic machine first writes a string $u$ of $p(|x|)$ bits, choosing each bit nondeterministically, and then runs $V$ on $(x, u)$. It has an accepting path exactly when some $u$ makes $V$ accept, so it decides $L$. Every path takes $O(p(n) + t(n))$ steps, a polynomial.

Conversely, suppose that a nondeterministic machine $N$ decides $L$ and every path halts within $q(n)$ steps, a polynomial. Let $d$ be the largest number of moves that the transition function allows from one configuration. A path is fixed by its sequence of choices, at most $q(n)$ numbers in $\{1, \ldots, d\}$, which is a string of $O(q(n))$ bits. The verifier $V(x, u)$ reads $u$ as such a sequence and simulates $N$ on $x$, taking the move that $u$ names at each step. It accepts when this path reaches the accept state, and it rejects when a choice is not allowed or the path rejects. Then $x \in L$ exactly when some $u$ leads to acceptance, and $V$ runs in time $O(q(n))$ times the cost of one simulated step, a polynomial. $\square$

**Basic facts.**

- $\mathsf{P} \subseteq \mathsf{NP}$: for $L \in \mathsf{P}$, the verifier ignores $u$ and decides $x$ itself.
- $\mathsf{NP} \subseteq \mathsf{EXP}$: a deterministic machine tries all $2^{p(n)}$ certificates and runs $V$ on each. The time is $2^{p(n)} \cdot t(n + p(n)) = 2^{O(n^k)}$ for some $k$. A finer argument, which reuses space between certificates, gives $\mathsf{NP} \subseteq \mathsf{PSPACE}$. See [the chain of inclusions](/class-inclusions-chain/).
- NP is closed under union, intersection, concatenation, Kleene star and polynomial-time many-one reductions: if $A \le_p B$ and $B \in \mathsf{NP}$, then $A \in \mathsf{NP}$. It is not known to be closed under complement. The complements of NP languages form [coNP](/co-np/), and $\mathsf{NP} = \mathsf{coNP}$ is open.
- The definition is asymmetric. Only yes-instances need certificates. A no-instance is one where no string makes the verifier accept.
- Like P, the class does not depend on the model: one-tape machines, multitape machines and nondeterministic RAMs with the logarithmic cost give the same NP ([multitape simulation theorem](/multitape-simulation-theorem/), [RAM and Turing machine equivalence](/ram-turing-equivalence/)).

## Examples and non-examples

**Examples.**

- *Subset sum.* An instance is a list of integers and a target, and the question is whether some sublist sums to the target. A certificate is the sublist, and the verifier adds it up. For the list $3, 34, 4, 12, 5, 2$ with target $9$, there are $2^6 = 64$ sublists, and exactly two of them are certificates: $\{4, 5\}$ and $\{3, 4, 2\}$. Checking one takes a few additions. Trying all sublists of a list of 40 numbers means $2^{40} = 1{,}099{,}511{,}627{,}776$ sums, about 1100 seconds at $10^9$ sums per second. See [the subset sum problem](/subset-sum-problem/).
- *SAT.* A Boolean formula is satisfiable when some assignment makes it true. The certificate is the assignment, and the verifier evaluates the formula. [SAT](/sat/) and [3-SAT](/3-sat/) are NP-complete by the [Cook-Levin theorem](/cook-levin-theorem/).
- *Graph problems.* A [clique](/clique-decision/) of size $k$, a [3-coloring](/three-coloring/) and a [Hamiltonian cycle](/hamiltonian-cycle-problem/) are certificates that a verifier checks in polynomial time. These three problems are NP-complete.
- *Composite numbers.* An integer $N > 1$ in binary is composite when it has a divisor $d$ with $1 < d < N$. The certificate is $d$, and the verifier divides. Primality is in NP too, by [Pratt certificates](/pratt-certificate/), and in P by the [AKS test](/aks-primality-test/).
- *Every problem in P.* The certificate is the empty string.

**Non-examples and open cases.**

- *Undecidable problems.* The [halting problem](/halting-problem/) is not in NP. Every language in NP is decidable, by the exhaustive search above.
- *Provably outside NP.* The nondeterministic time hierarchy gives $\mathsf{NP} \subsetneq \mathsf{NEXP}$, so every problem complete for [NEXP](/nexptime/) under polynomial-time reductions is not in NP.
- *Not known to be in NP.* Tautology (is a formula true under every assignment?) is in coNP. A short certificate for a tautology is not known, and if tautology is in NP then $\mathsf{NP} = \mathsf{coNP}$. See [coNP-complete](/co-np-complete/).
- *A wrong certificate.* For the traveling salesman decision problem "is there a tour of length at most $B$?", a tour is a certificate. For "is the shortest tour of length exactly $B$?", a tour of length $B$ is not enough, because it does not show that no shorter tour exists. This problem is not known to be in NP.
- *NP does not mean exponential.* A problem in NP may have a fast algorithm. Showing that a problem is in NP gives an upper bound, not a lower bound.

## Related definitions

- A [certificate](/certificate/) is the short proof, and a [polynomial-time verifier](/polynomial-time-verifier/) is the checking algorithm. NP is the class of languages that have both.
- A problem is [NP-hard](/np-hard/) when every problem in NP reduces to it by polynomial-time many-one (Karp) reductions, and [NP-complete](/np-complete/) when it is also in NP. Cook (1971) used polynomial-time Turing reductions. Karp (1972) used many-one reductions, which is the standard today.
- [coNP](/co-np/) contains the complements of NP languages. $\mathsf{P} \subseteq \mathsf{NP} \cap \mathsf{coNP}$, and problems in $\mathsf{NP} \cap \mathsf{coNP}$ have a [good characterization](/good-characterization/).
- [FNP](/fnp/) is the class of search problems that go with NP: given $x$, find a certificate $u$ with $V(x, u) = 1$, or report that none exists. See [search problems](/search-problem/) and [self-reducibility](/self-reducibility/).
- If $\mathsf{P} \ne \mathsf{NP}$, then NP contains problems that are neither in P nor NP-complete ([Ladner's theorem](/ladner-theorem/), [NP-intermediate](/np-intermediate/)).
- NP is the first level $\Sigma_1^p$ of the [polynomial hierarchy](/polynomial-hierarchy/). [MA](/merlin-arthur/) and the [PCP theorem](/pcp-theorem/) give randomized ways to check NP certificates.

## References
