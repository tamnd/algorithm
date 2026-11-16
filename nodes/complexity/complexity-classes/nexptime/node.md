---
tag: 9H4YP2
kind: definition
slug: nexptime
name: NEXP (NEXPTIME)
aliases:
- NEXP
- nondeterministic exponential time
area: complexity/complexity-classes
level: advanced
summary: "Decision problems that a nondeterministic Turing machine decides in time 2 to the power of a polynomial. NP is a proper subset, and P = NP would imply EXP = NEXP."
prereqs: [np, exptime]
see_also: [exptime, np, mip-equals-nexp, multi-prover-interactive-proofs, hypercube-hamiltonian-cycle, circuit-complexity, expspace, class-inclusions-chain]
sources:
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach
    locator: Section 2.6.2, EXP and NEXP (with the padding argument)
  - paper: doi:10.1016/S0019-9958(86)80009-2
    title: Christos H. Papadimitriou and Mihalis Yannakakis, A note on succinct representations of graphs, Information and Control 71(3) (1986), 181 to 185
    locator: succinct versions of graph problems are NEXP-complete
  - paper: "Stephen A. Cook, A hierarchy for nondeterministic time complexity, Journal of Computer and System Sciences 7(4) (1973), 343 to 353"
    locator: the first nondeterministic time hierarchy
  - paper: "Michael J. Fischer and Michael O. Rabin, Super-exponential complexity of Presburger arithmetic, in R. M. Karp (editor), Complexity of Computation, SIAM-AMS Proceedings 7 (1974)"
    locator: the lower bound for nondeterministic time
  - paper: doi:10.1145/322047.322061
    title: Joel I. Seiferas, Michael J. Fischer and Albert R. Meyer, Separating nondeterministic time complexity classes, Journal of the ACM 25(1) (1978), 146 to 167
    locator: the nondeterministic time hierarchy
  - paper: doi:10.1016/0304-3975(83)90015-4
    title: Stanislav Žák, A Turing machine time hierarchy, Theoretical Computer Science 26(3) (1983), 327 to 333
    locator: the nondeterministic time hierarchy
  - paper: doi:10.1007/BF01200056
    title: László Babai, Lance Fortnow and Carsten Lund, Non-deterministic exponential time has two-prover interactive protocols, Computational Complexity 1(1) (1991), 3 to 40
    locator: MIP = NEXP
  - paper: doi:10.1145/2559903
    title: Ryan Williams, Nonuniform ACC circuit lower bounds, Journal of the ACM 61(1) (2014), 1 to 32
    locator: NEXP does not have polynomial-size ACC0 circuits
---

NEXP, also written NEXPTIME, is the class of [decision problems](/decision-problem/) that a [nondeterministic Turing machine](/nondeterministic-turing-machine/) decides in time $2^{p(n)}$ for some polynomial $p$. It is to [EXP](/exptime/) what [NP](/np/) is to [P](/p/). Its typical complete problems are NP-complete problems on inputs given in a compressed form, such as graphs with exponentially many vertices described by a small circuit. NEXP appears in three well known results: $\mathsf{NP} \ne \mathsf{NEXP}$, $\mathsf{MIP} = \mathsf{NEXP}$, and the lower bound of Williams for ACC0 circuits.

## Definition

Fix the alphabet $\{0, 1\}$, and let $\mathsf{NTIME}(f(n))$ be the set of languages decided by a nondeterministic multitape Turing machine whose paths all halt within $O(f(n))$ steps on inputs of length $n$. Then

$$\mathsf{NEXP} = \bigcup_{k \ge 1} \mathsf{NTIME}\left(2^{n^k}\right).$$

**By verifiers.** As for NP, $L \in \mathsf{NEXP}$ exactly when there are a constant $k$ and a deterministic machine $V$ such that $x \in L$ if and only if some certificate $u$ of length $2^{|x|^k}$ makes $V(x, u)$ accept, and $V$ runs in time $2^{O(|x|^k)}$. The proof is the same as for NP: the certificate is the list of nondeterministic choices. The certificate may now be exponentially long.

**Inclusions.** $\mathsf{NP} \subseteq \mathsf{EXP} \subseteq \mathsf{NEXP} \subseteq \mathsf{EXPSPACE}$. The second inclusion holds because a deterministic machine is a nondeterministic one. The third holds because a deterministic machine can try all certificates of length $2^{n^k}$ one after the other, reusing the same exponential space.

**$\mathsf{NP} \ne \mathsf{NEXP}$.** The nondeterministic time hierarchy (Cook, 1973; Seiferas, Fischer and Meyer, 1978; Žák, 1983) says that $\mathsf{NTIME}(f(n)) \subsetneq \mathsf{NTIME}(g(n))$ when $g$ is time-constructible and $f(n + 1) = o(g(n))$. Every $n^k$ is $O(2^n)$, so $\mathsf{NP} \subseteq \mathsf{NTIME}(2^n)$. With $f(n) = 2^n$ and $g(n) = 2^{2n}$, $f(n + 1) = 2 \cdot 2^n = o(2^{2n})$, so $\mathsf{NTIME}(2^n) \subsetneq \mathsf{NTIME}(2^{2n}) \subseteq \mathsf{NEXP}$. Hence $\mathsf{NP} \subsetneq \mathsf{NEXP}$. The relations of NEXP with EXP and with PSPACE are open.

**Padding: if $\mathsf{P} = \mathsf{NP}$, then $\mathsf{EXP} = \mathsf{NEXP}$.** Let $L \in \mathsf{NEXP}$ be decided by a nondeterministic machine $N$ within $2^{n^k}$ steps. Define the padded language

$$L' = \{ x \, 0 \, 1^{2^{|x|^k}} : x \in L \}.$$

A string $y$ splits into $x$, a single $0$ and a block of ones in at most one way: the block of ones is the longest run of ones at the end of $y$. So a deterministic machine checks in time polynomial in $|y|$ that $y$ has the right form. Then $L' \in \mathsf{NP}$: on input $y$, check the form, find $x$, and run $N$ on $x$ for $2^{|x|^k} < |y|$ steps. If $\mathsf{P} = \mathsf{NP}$, a deterministic machine $D$ decides $L'$ in time $|y|^c$. To decide $L$ deterministically on input $x$, write $y = x \, 0 \, 1^{2^{|x|^k}}$ in time $O(2^{|x|^k})$ and run $D$ on $y$, in time $(|x| + 1 + 2^{|x|^k})^c = 2^{O(|x|^k)}$. So $L \in \mathsf{EXP}$. $\square$

The contrapositive says: if $\mathsf{EXP} \ne \mathsf{NEXP}$, then $\mathsf{P} \ne \mathsf{NP}$. Padding moves equalities upward, from small classes to large ones. It does not move separations upward, and it does not move equalities downward: $\mathsf{EXP} = \mathsf{NEXP}$ is not known to imply $\mathsf{P} = \mathsf{NP}$.

## Examples and non-examples

**Examples.**

- *Succinct problems.* A *succinct* graph on $2^k$ vertices is given by a Boolean circuit $C$ with $2k$ inputs: vertices $u$ and $v$ are adjacent when $C(u, v) = 1$. The input is the circuit, so the graph can be exponentially larger than the input. Papadimitriou and Yannakakis (1986) showed that graph properties that are NP-complete for graphs given in the usual way become NEXP-complete for graphs given in this succinct way, when the NP-completeness reduction is simple enough (a projection). This holds for the standard NP-complete graph problems, such as Hamiltonian cycle and 3-coloring. Succinct Hamiltonian cycle is in NEXP because a certificate lists the $2^k$ vertices of a cycle, with $k \cdot 2^k$ bits, and the verifier checks each edge with one evaluation of $C$.
- *The hypercube as a succinct graph.* The $k$-dimensional hypercube has the vertices $\{0, 1\}^k$, and two vertices are adjacent when they differ in exactly one bit. A circuit of size $O(k)$ computes the exclusive or of $u$ and $v$ and tests that exactly one bit is 1. For $k = 4$ it describes 16 vertices and 32 edges. For $k = 20$ it describes $1{,}048{,}576$ vertices and $10{,}485{,}760$ edges, while the circuit stays of size $O(k)$. The [hypercube has a Hamiltonian cycle](/hypercube-hamiltonian-cycle/) for $k \ge 2$, and the reflected [Gray code](/gray-code/) lists it. For $k = 4$ the cycle is $0, 1, 3, 2, 6, 7, 5, 4, 12, 13, 15, 14, 10, 11, 9, 8$, in decimal. Here the certificate has a short description, but in general it does not.
- *Bounded halting, nondeterministic version.* $\{ \langle N, x, t \rangle : \text{some path of } N \text{ accepts } x \text{ within } t \text{ steps} \}$, with $N$ nondeterministic and $t$ in binary, is NEXP-complete by the same argument as the deterministic version on the page on [EXP](/exptime/).
- *Every problem in EXP.*

**Non-examples and open cases.**

- *NP-complete problems* are not NEXP-complete: an NEXP-complete problem in NP would give $\mathsf{NEXP} \subseteq \mathsf{NP}$, which the hierarchy rules out. Their succinct versions are NEXP-complete.
- *Doubly exponential problems.* [Presburger arithmetic](/presburger-arithmetic/) needs nondeterministic time $2^{2^{cn}}$ (Fischer and Rabin, 1974), so it is not in NEXP.
- *Open cases.* Problems complete for EXP or for [PSPACE](/pspace/) are not known to be NEXP-complete, and problems complete for NEXP are not known to be outside EXP.

## Related definitions

- [EXP](/exptime/) is the deterministic version. $\mathsf{EXP} \subseteq \mathsf{NEXP}$, and equality is open. By padding, $\mathsf{P} = \mathsf{NP}$ implies $\mathsf{EXP} = \mathsf{NEXP}$.
- [Multi-prover interactive proofs](/multi-prover-interactive-proofs/) capture NEXP: [$\mathsf{MIP} = \mathsf{NEXP}$](/mip-equals-nexp/) (Babai, Fortnow and Lund, 1991). A polynomial-time verifier that questions two provers who cannot talk to each other can check an exponentially long certificate.
- In [circuit complexity](/circuit-complexity/), Williams (2014) proved that NEXP does not have polynomial-size ACC0 circuits: constant-depth circuits with AND, OR, NOT and MOD $m$ gates. Whether NEXP has polynomial-size general circuits, $\mathsf{NEXP} \subseteq \mathsf{P/poly}$, is open.
- [EXPSPACE](/expspace/) contains NEXP. Whether the inclusion is strict is open.

## References
