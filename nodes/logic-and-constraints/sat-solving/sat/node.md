---
tag: CA0ZDK
kind: problem
slug: sat
name: Boolean satisfiability problem
aliases:
- Boolean satisfiability
- CNF-SAT
- SAT
- propositional satisfiability
- satisfiability problem
area: logic-and-constraints/sat-solving
level: intro
summary: Decide whether a CNF formula has a satisfying assignment. The first problem shown NP-complete (Cook 1971, Levin 1973), and the target of CDCL solvers.
prereqs: [conjunctive-normal-form, np-complete]
see_also: [cook-levin-theorem, dpll, cdcl, 3-sat, 2-sat, walksat, max-sat, tseitin-transformation]
sources:
  - paper: doi:10.1145/800157.805047
    title: Stephen A. Cook, The complexity of theorem-proving procedures, Proceedings of the Third Annual ACM Symposium on Theory of Computing (STOC), 1971
    locator: pages 151 to 158 (every problem decided in nondeterministic polynomial time reduces to propositional satisfiability; the 3-CNF case)
  - paper: "Leonid A. Levin, Universal sequential search problems, Problemy Peredachi Informatsii 9(3), 1973; English translation in Problems of Information Transmission 9(3), 1973"
    locator: pages 265 to 266 of the translation (universal search problems, among them satisfiability)
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in R. E. Miller and J. W. Thatcher (eds.), Complexity of Computer Computations, Plenum Press, 1972
    locator: pages 85 to 103 (the reductions from SAT to 21 combinatorial problems)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Section 2.6 (Cook's theorem), Section 3.1.1 (3-SAT), and Appendix A9.1, problem LO1 (satisfiability)
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 1 (a history of satisfiability), Chapter 3 (complete algorithms), Chapter 4 (CDCL solvers), Chapter 7 (proof complexity) and Chapter 12 (worst-case analysis)
  - paper: doi:10.1006/jcss.2000.1727
    title: Russell Impagliazzo and Ramamohan Paturi, On the complexity of k-SAT, Journal of Computer and System Sciences 62(2), 2001
    locator: pages 367 to 375 (the exponential time hypothesis and the growth of the exponent of k-SAT with k)
  - paper: doi:10.1145/1066100.1066101
    title: Ramamohan Paturi, Pavel Pudlák, Michael E. Saks and Francis Zane, An improved exponential-time algorithm for k-SAT, Journal of the ACM 52(3), 2005
    locator: pages 337 to 364 (the PPSZ algorithm and its bounds)
  - paper: doi:10.1016/0304-3975(85)90144-6
    title: Armin Haken, The intractability of resolution, Theoretical Computer Science 39, 1985
    locator: pages 297 to 308 (exponential lower bound for resolution refutations of the pigeonhole formulas)
  - paper: "David Mitchell, Bart Selman and Hector Levesque, Hard and easy distributions of SAT problems, Proceedings of AAAI 1992, pages 459 to 465"
    locator: the measured peak of DPLL cost and the 50 percent satisfiability point of random 3-SAT near 4.3 clauses per variable
---

The Boolean satisfiability problem (SAT) asks whether a formula in [conjunctive normal form](/conjunctive-normal-form/) has an assignment of true and false to its variables that makes every [clause](/clause/) true. It was the first problem shown [NP-complete](/np-complete/), by Cook in 1971 and independently by Levin in 1973, and so no polynomial-time algorithm for it is known. Yet [CDCL](/cdcl/) solvers decide many industrial formulas with millions of clauses, which makes SAT the common back end of hardware and software verification, planning and combinatorial search.

## In plain words

You have a set of switches, each on or off, and a list of rules. Each rule names a few switches and says that at least one of them must be in a given position, for example "switch 1 on, or switch 2 off". The question is whether some setting of all switches obeys every rule at once.

If someone shows you a setting, checking it is fast: go through the rules one by one. Finding one is the hard part. Trying all settings doubles the work with each new switch, and no method is known that is fast on every list of rules. Many hard puzzles of computing can be written as such a list, so a fast method for this problem would give a fast method for all of them.

## Definition

Notation: $F$ is a CNF formula over the variables $x_1, \ldots, x_n$, with $m$ clauses, and $|F|$ is the number of literal occurrences.

**SAT (decision).** Input: a CNF formula $F$. Question: is there an assignment $\alpha : \{x_1, \ldots, x_n\} \to \{0, 1\}$ that satisfies every clause of $F$?

**SAT (search).** Output such an $\alpha$, a *model*, or report that none exists. By self-reduction, a decision procedure gives a search procedure with $n$ more calls: fix $x_1 = 1$, simplify, ask again, and keep the value that leaves the formula satisfiable.

**Certificates.** A model is checked in $O(|F|)$ time, so SAT is in [NP](/np/). An unsatisfiable formula has no known short certificate in general (that would put SAT in coNP and give NP = coNP), but solvers emit a refutation, such as a [DRAT proof](/drat-proof/), whose length is not bounded by a polynomial.

**Formulas in general.** Satisfiability of an arbitrary propositional formula reduces to CNF-SAT in linear time by the [Tseitin transformation](/tseitin-transformation/), so the two problems are equivalent up to linear time.

## Variants

| variant | question | complexity |
|---|---|---|
| [2-SAT](/2-sat/) | clauses of width at most 2 | linear time |
| [3-SAT](/3-sat/), [k-SAT](/k-sat/) for $k \ge 3$ | clauses of width at most $k$ | NP-complete |
| [Horn-SAT](/horn-sat/) | at most one positive literal per clause | linear time |
| [XOR-SAT](/xor-sat/) | clauses are parity constraints | polynomial, by Gaussian elimination |
| [Circuit-SAT](/circuit-sat/) | a Boolean circuit instead of a CNF | NP-complete |
| [MaxSAT](/max-sat/) | satisfy as many clauses, or as much weight, as possible | NP-hard |
| [#SAT](/model-counting/) | count the models | #P-complete |
| [QBF](/qbf/) | quantified Boolean formulas | PSPACE-complete |
| [pseudo-Boolean SAT](/pseudo-boolean-sat/) | linear inequalities over 0/1 variables | NP-complete |
| [SMT](/smt-problem/) | Boolean structure over theory atoms | depends on the theory |
| [incremental SAT](/incremental-sat/) | a sequence of related queries with assumptions | as SAT, per query |

By Schaefer's dichotomy theorem (1978), the classes of [Boolean constraint satisfaction](/boolean-constraint-satisfaction/) problems are either in P (2-CNF, Horn, dual Horn, affine, 0-valid and 1-valid) or NP-complete.

## Examples

**A satisfiable formula.** $F = \{x_1, \neg x_2\}, \{x_2, x_3\}, \{\neg x_1, \neg x_3\}, \{\neg x_2, x_3\}$. A check of all 8 assignments finds one model, $x_1 = 0, x_2 = 0, x_3 = 1$. The [DIMACS](/dimacs-cnf-format/) page has its file.

**An unsatisfiable formula.** The pigeonhole formula $\mathrm{PHP}^{h+1}_h$ says that $h + 1$ pigeons sit in $h$ holes, no two in one hole. It has a variable $p_{i,j}$ for "pigeon $i$ is in hole $j$", a clause $\{p_{i,1}, \ldots, p_{i,h}\}$ for each pigeon, and a clause $\{\neg p_{i,j}, \neg p_{i',j}\}$ for each hole and each pair of pigeons. For $h = 1, 2, 3$ it has 2, 6 and 12 variables and 3, 9 and 22 clauses, and brute force confirms that none of the three has a model. By the [pigeonhole principle](/pigeonhole-principle/) no instance does, but every [resolution](/binary-resolution/) proof of this needs exponential size ([Haken](/haken-resolution-lower-bound/)).

**Random 3-SAT.** Pick $m$ clauses of 3 distinct variables with random signs. For $n = 12$ and 1000 random formulas at each ratio $m/n$, brute force over the 4096 assignments gave these fractions of satisfiable formulas:

| $m/n$ | 2 | 3 | 4 | 4.26 | 5 | 6 | 8 |
|---|---|---|---|---|---|---|---|
| $m$ | 24 | 36 | 48 | 51 | 60 | 72 | 96 |
| satisfiable | 1.000 | 0.997 | 0.852 | 0.758 | 0.479 | 0.157 | 0.009 |

As $n$ grows the drop gets sharper, and the 50 percent point moves down toward about 4.27; at $n = 12$ it is still near 5. Mitchell, Selman and Levesque measured in 1992 that the cost of DPLL peaks near the same ratio. See [satisfiability threshold](/satisfiability-threshold/).

## Known algorithms

- **Brute force.** Try all $2^n$ assignments in $O(2^n |F|)$ time.
- **Resolution.** [Davis-Putnam elimination](/davis-putnam-elimination/) (1960) removes the variables one by one by resolution. It is exact but can need exponential space.
- **Backtracking.** [Plain backtracking](/dpll-backtracking-sat/) and [DPLL](/dpll/) (1962), which adds [unit propagation](/unit-propagation/) and [pure literal elimination](/pure-literal-elimination/).
- **CDCL.** [Conflict-driven clause learning](/cdcl/) (GRASP 1996, Chaff 2001, MiniSat 2003), with [clause learning](/clause-learning/), [non-chronological backtracking](/non-chronological-backtracking/), [two watched literals](/two-watched-literals/), [VSIDS](/vsids/) and [restarts](/restarts/). This is the method of nearly all complete solvers in use.
- **Look-ahead and cube-and-conquer.** [Look-ahead solvers](/lookahead-sat/) for hard combinatorial formulas, and [cube-and-conquer](/cube-and-conquer/), which splits a formula into many parts for CDCL.
- **Local search.** [GSAT](/gsat/), [WalkSAT](/walksat/) and [probSAT](/probsat/) flip variables to reduce the number of false clauses. They find models fast on many random satisfiable formulas but cannot prove unsatisfiability.
- **Exponential algorithms with proved bounds for k-SAT.** [Schöning's algorithm](/schoning-algorithm/) solves 3-SAT in $O^*((4/3)^n)$ expected time, and [PPSZ](/ppsz-algorithm/) in $O(1.308^n)$, with the analysis of Hertli (2011) for formulas with many models. See [exact exponential algorithms](/exact-exponential-algorithms/).

## Bounds

**NP-completeness.** SAT is NP-complete: it is in NP, and every problem in NP reduces to it in polynomial time (the [Cook-Levin theorem](/cook-levin-theorem/): Cook 1971, Levin 1973). Cook also showed that the restriction to 3-CNF stays NP-complete. So a polynomial-time algorithm for SAT exists if and only if P = NP.

**Exponential time.** The exponential time hypothesis of Impagliazzo and Paturi (2001) states that 3-SAT has no $2^{o(n)}$ algorithm. The [strong exponential time hypothesis](/strong-exponential-time-hypothesis/) states that for each $\varepsilon > 0$ some $k$ makes $k$-SAT need more than $(2 - \varepsilon)^n$ time. Both are open. For CNF formulas of unbounded width, no algorithm is known with time $O(c^n \cdot \mathrm{poly}(|F|))$ for a constant $c < 2$.

**DPLL and CDCL.** No worst-case bound better than $2^n$ times a polynomial is proved for DPLL or CDCL in general. A run of DPLL on an unsatisfiable formula gives a tree-like resolution refutation, and a run of CDCL gives a general resolution refutation of about the same size, so resolution lower bounds are lower bounds on their running time:

- Haken (1985): every resolution refutation of $\mathrm{PHP}^{h+1}_h$ has size $2^{\Omega(h)}$;
- Urquhart (1987): the same for the Tseitin formulas of suitable expander graphs, with $2^{\Omega(n)}$ in the number of variables;
- Chvátal and Szemerédi (1988): random 3-CNF formulas with $cn$ clauses, for a large constant $c$, are unsatisfiable and need resolution refutations of size $2^{\Omega(n)}$, with probability tending to 1.

In the other direction, CDCL with restarts can simulate any resolution proof with polynomial overhead (Pipatsrisawat and Darwiche 2011), see [CDCL simulates resolution](/cdcl-simulates-resolution/).

**Space.** A model needs $n$ bits. Solvers keep their learned clauses, and that store is the main memory cost; [clause database reduction](/clause-database-reduction/) bounds it in practice.

## Reductions

- **From every problem in NP.** The [Cook-Levin theorem](/cook-levin-theorem/) writes the run of a nondeterministic machine as a CNF of polynomial size. The reduction is a [Levin reduction](/levin-reduction/): models map back to witnesses.
- **SAT to 3-SAT.** Replace a clause $\{\ell_1, \ldots, \ell_k\}$ with $k > 3$ by $\{\ell_1, \ell_2, y_1\}, \{\neg y_1, \ell_3, y_2\}, \ldots, \{\neg y_{k-3}, \ell_{k-1}, \ell_k\}$ with new variables $y_i$. The result is equisatisfiable and has $O(|F|)$ size.
- **Circuit-SAT to SAT.** The [Tseitin transformation](/tseitin-transformation/), with one variable per gate.
- **SAT to other problems.** Karp (1972) reduced SAT to clique, vertex cover, chromatic number, Hamiltonian cycle and others, see [Karp's 21 NP-complete problems](/karps-21-np-complete-problems/).
- **Other problems to SAT, in practice.** Finite-domain constraints are encoded by direct or order encodings, cardinality constraints by the [sequential counter](/sequential-counter-encoding/) or the [totalizer](/totalizer-encoding/), and bounded runs of systems by unrolling, as in [bounded model checking](/bounded-model-checking/).

## Applications

- **Hardware and software verification.** [SAT-based bounded model checking](/sat-based-bounded-model-checking/) (Biere, Cimatti, Clarke and Zhu, 1999), equivalence checking of circuits, and [SMT](/smt-problem/) solvers built on [DPLL(T)](/dpll-t/).
- **Planning.** [SATPLAN](/satplan/) encodes [classical planning](/classical-planning/) with a fixed horizon as SAT (Kautz and Selman, 1992).
- **Combinatorics.** SAT solvers settled the Boolean Pythagorean triples problem (Heule, Kullmann and Marek, 2016) and other open cases of Ramsey-type questions, with proofs checked in the DRAT format.
- **Scheduling, configuration and dependency resolution.** Package managers and product configurators encode their constraints as SAT or [MaxSAT](/max-sat/).
- **Cryptanalysis.** Attacks on hash functions and stream ciphers write the cipher as a CNF, often with [XOR](/xor-sat/) clauses.

## References
