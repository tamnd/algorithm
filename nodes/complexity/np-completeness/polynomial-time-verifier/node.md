---
tag: RHDYZQ
kind: definition
slug: polynomial-time-verifier
name: Polynomial-time verifier
aliases:
- verifier
area: complexity/np-completeness
level: intro
summary: A deterministic polynomial-time machine V such that x is in L exactly when some certificate y of polynomial length makes V(x, y) accept. It defines NP.
prereqs: [decision-problem, certificate, polynomial-time, turing-machine]
see_also: [np, co-np, nondeterministic-turing-machine, interactive-proofs, probabilistically-checkable-proof, unambiguous-polynomial-time, polynomial-hierarchy, fnp]
sources:
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 7.3 (verifiers, the definition of NP by verifiers and its equivalence with nondeterministic machines)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach
    locator: Section 2.1 (the class NP, the verifier definition and the equivalence with NTIME), Section 2.6 (coNP by the universal quantifier)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 34.2 (polynomial-time verification, verification algorithms and the class NP)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness
    locator: Section 2.3 (the nondeterministic one-tape machine as a guessing stage followed by a checking stage)
---

A polynomial-time verifier for a language $L$ is a deterministic algorithm $V$ that takes an instance $x$ and a candidate [certificate](/certificate/) $y$, runs in time polynomial in $|x|$, and has this property: $x \in L$ exactly when some $y$ of length polynomial in $|x|$ makes $V$ accept. A language has a polynomial-time verifier if and only if it is in [NP](/np/); the NP page proves that this definition agrees with the one by [nondeterministic Turing machines](/nondeterministic-turing-machine/). The verifier is the checking machine; the certificate is the string that it checks.

## Definition

The model is the deterministic [multitape Turing machine](/multitape-turing-machine/). The input of $V$ is an encoding $\langle x, y\rangle$ of the pair, for example $x$, a separator symbol and $y$.

**Definition.** Let $L \subseteq \{0,1\}^*$. A polynomial-time verifier for $L$ is a deterministic Turing machine $V$ together with polynomials $p$ and $t$ such that:
1. On every input $\langle x, y\rangle$ with $|y| \le p(|x|)$, $V$ halts within $t(|x|)$ steps and outputs 1 (accept) or 0 (reject).
2. Completeness: if $x \in L$, then there is a $y$ with $|y| \le p(|x|)$ and $V(x, y) = 1$.
3. Soundness: if $x \notin L$, then $V(x, y) = 0$ for every $y$ with $|y| \le p(|x|)$.

A string $y$ with $V(x, y) = 1$ is a certificate for $x$. In one line,
$$x \in L \iff \exists y \in \{0,1\}^{\le p(|x|)} : V(x, y) = 1.$$
NP is the class of languages that have a polynomial-time verifier.

**Conventions.** Sipser measures the running time of $V$ in $|x|$ only. Arora and Barak require $|y| = p(|x|)$ exactly and a machine that runs in polynomial time. The definitions give the same class. A time bound in $|x| + |y|$ is a polynomial in $|x|$, because $|y| \le p(|x|)$. Certificates of length at most $p(|x|)$ become certificates of length exactly $p(|x|) + 1$ by appending $1 0 \cdots 0$, and $V$ strips this padding first. Classes P, NP and coNP do not change under the polynomial-time simulations of the [multitape simulation theorem](/multitape-simulation-theorem/) and of [RAM to Turing machine simulation](/ram-turing-equivalence/), so a verifier can be written as an ordinary algorithm on a RAM, as below.

**From a verifier to a nondeterministic machine and back.** Given $V$, a nondeterministic machine writes an arbitrary $y$ of length at most $p(n)$ and then runs $V$; it decides $L$ in time $O(p(n) + t(n))$. This is exactly the guessing stage and checking stage of Garey and Johnson (Section 2.3). Given a nondeterministic machine $N$ with time bound $t(n)$ and at most two choices per step, the sequence of its $t(n)$ choices is a certificate, and $V$ replays $N$ with those choices. Both directions are on the [NP](/np/) page.

**Deterministic simulation.** Trying every candidate decides $L$ in time $2^{p(n)+1} \cdot t(n)$, so $\mathsf{NP} \subseteq \mathsf{EXP}$. Reusing the same space for each candidate gives $\mathsf{NP} \subseteq \mathsf{PSPACE}$. No faster general method is known, and whether one exists in polynomial time is the [P versus NP problem](/p-versus-np-problem/).

## Examples and non-examples

**Subset sum.** Instance: positive integers $a_1, \ldots, a_n$ and a target $s$, all in binary. A certificate is a bit string $y \in \{0,1\}^n$. The verifier:

1. Reject if $|y| \ne n$.
2. Compute $\sigma = \sum_{i : y_i = 1} a_i$ with schoolbook addition.
3. Accept if $\sigma = s$, else reject.

With $b$ the largest bit length, step 2 takes $O(n(b + \log n))$ bit operations, which is polynomial in the input length. For $(3, 34, 4, 12, 5, 2)$ and $s = 9$, a script ran the verifier on all $2^6 = 64$ strings $y$; it accepted exactly 2 of them, the sets $\{4, 5\}$ and $\{3, 4, 2\}$. See [subset sum](/subset-sum-problem/).

**Clique.** Instance: a graph $G$ with $n$ vertices and an integer $k$. A certificate is a list of $k$ vertex numbers. The verifier checks that they are distinct and that each of the $\binom{k}{2}$ pairs is an edge, with an [adjacency matrix](/adjacency-matrix/) lookup per pair; this is $O(k^2)$ lookups plus the time to build the matrix. See the [clique problem](/clique-problem/).

**3-coloring.** For the Petersen graph (10 vertices, 15 edges), a certificate is a list of 10 colors and the verifier makes 15 edge checks. A script found that 120 of the $3^{10} = 59049$ lists pass. See [three-coloring](/three-coloring/).

**Verifiers that ignore the certificate.** If $L \in \mathsf{P}$, then the machine that decides $L$ and ignores $y$ is a verifier with $p = 0$. This shows $\mathsf{P} \subseteq \mathsf{NP}$. It also shows that NP does not mean "not polynomial": NP stands for nondeterministic polynomial time and contains every problem in P.

**Non-example: an unsound checker.** A machine that accepts $\langle x, y\rangle$ whenever $y$ is a proper coloring of some subgraph of $G$ is not a verifier for 3-colorability. It accepts the empty coloring for every graph, so the soundness condition fails on graphs that are not 3-colorable.

**Non-example: a certificate that is too long.** The truth table of a CNF formula with $n$ variables proves that it is unsatisfiable, and a machine can check it in time polynomial in $|x| + |y|$. But $|y| = 2^n$ is not bounded by a polynomial in $|x|$ when the formula is short, so this is not a polynomial-time verifier for unsatisfiability. Unsatisfiability is [coNP-complete](/co-np-complete/), so it has a polynomial-time verifier only if NP = coNP.

**Non-example: checking optimality.** A tour of a set of cities is easy to check against a bound $k$, so "is there a tour of length at most $k$?" has a verifier. "Is this tour the shortest?" asks that every other tour is at least as long; no polynomial-time verifier for it is known. The question is in coNP, because a shorter tour is a certificate for the answer no. See [traveling salesman (decision)](/traveling-salesman-decision/).

## Related definitions

- [Certificate](/certificate/): the string $y$, and the certificate relation $R = \{(x, y) : V(x, y) = 1\}$.
- [NP](/np/): the class of languages with a polynomial-time verifier, equal to the class decided by nondeterministic machines in polynomial time.
- [coNP](/co-np/): the same with the universal quantifier, $x \in L \iff \forall y \in \{0,1\}^{\le p(|x|)} : V(x, y) = 1$.
- [Polynomial hierarchy](/polynomial-hierarchy/): alternating quantifiers over polynomial-length strings in front of a polynomial-time verifier; $\Sigma_2^p$ uses $\exists \forall$.
- [UP](/unambiguous-polynomial-time/): a verifier for which every $x$ has at most one certificate.
- [FNP](/fnp/) and [search problems](/search-problem/): the task of finding an accepted certificate.
- Randomized verifiers: [interactive proofs](/interactive-proofs/) let the verifier talk to a prover and allow a small error; a [probabilistically checkable proof](/probabilistically-checkable-proof/) verifier reads only a few bits of $y$ at random positions.
- [Polynomial-time reductions](/polynomial-time-reduction/) and [Levin reductions](/levin-reduction/): the second kind also maps accepted certificates between two verifiers.

## References
