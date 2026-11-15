---
tag: W2EZWK
kind: theorem
slug: cook-levin-theorem
name: Cook-Levin theorem
aliases:
- Cook's theorem
- Levin's theorem
- SAT is NP-complete
area: complexity/np-completeness
level: intro
summary: SAT is NP-complete. Every NP problem reduces to SAT by a Karp reduction that writes the run of a verifier as a CNF formula. This was the first NP-completeness result.
prereqs: [np, sat, polynomial-time-reduction, nondeterministic-turing-machine, conjunctive-normal-form]
see_also: [np-complete, 3-sat, circuit-sat, tseitin-transformation, karps-21-np-complete-problems, levin-reduction, parsimonious-reduction, pcp-theorem]
sources:
  - paper: doi:10.1145/800157.805047
    title: Stephen A. Cook, The complexity of theorem-proving procedures, Proceedings of the 3rd ACM Symposium on Theory of Computing (1971), 151 to 158
    locator: Theorem 1 (every set accepted by a nondeterministic machine in polynomial time is P-reducible to the DNF tautologies) and Theorem 2
  - paper: "Leonid A. Levin, Universal sequential search problems, Problemy Peredachi Informatsii 9(3) (1973), 115 to 116; English translation in Problems of Information Transmission 9(3), 265 to 266"
    locator: the definition of universal search problems and the list of universal problems
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in R. E. Miller and J. W. Thatcher (eds.), Complexity of Computer Computations, Plenum Press (1972), 85 to 103
    locator: Theorem 2 (Cook's theorem with many-one reductions) and Corollary 1
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness
    locator: Section 2.6 (Cook's theorem, proved for the nondeterministic one-tape machine with a guessing stage)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 7.4 (the Cook-Levin theorem, the tableau proof with 2 by 3 windows)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach
    locator: "Section 2.3 (the Cook-Levin theorem: computation is local)"
  - paper: doi:10.1016/0020-0190(88)90152-4
    title: Stephen A. Cook, Short propositional formulas represent nondeterministic computations, Information Processing Letters 26(5), 269 to 270 (1988)
    locator: the main result (a CNF with O(t log t) literals for a time t machine)
---

The Cook-Levin theorem says that [SAT](/sat/), the satisfiability problem for formulas in [conjunctive normal form](/conjunctive-normal-form/), is [NP-complete](/np-complete/). Every problem in [NP](/np/) reduces to SAT by a [polynomial-time reduction](/polynomial-time-reduction/): the reduction writes the run of a verifier on $x$ and an unknown [certificate](/certificate/) as a CNF formula that is satisfiable exactly when some certificate is accepted. It was the first NP-completeness result. Every later one, such as [Karp's 21 problems](/karps-21-np-complete-problems/), is proved by a chain of reductions that starts at SAT.

## Statement

**Theorem (Cook 1971, Levin 1973, in the form of Karp 1972).** SAT is NP-complete under polynomial-time many-one (Karp) reductions. That is, SAT is in NP, and for every language $L \in \mathsf{NP}$ there is a function $f$, computable in polynomial time on a deterministic [multitape Turing machine](/multitape-turing-machine/), such that for every string $x$,
$$x \in L \iff f(x) \text{ is a satisfiable CNF formula.}$$

The model: $L$ is given by a deterministic single-tape Turing machine $M$ that checks a pair $(x, y)$ with $|y| = p(|x|)$ within $T = t(|x|)$ steps, for polynomials $p$ and $t$. This is the [verifier](/polynomial-time-verifier/) form of NP. It is the same as a [nondeterministic Turing machine](/nondeterministic-turing-machine/) with a guessing stage followed by a deterministic checking stage, which is the model of Garey and Johnson (Section 2.6). A multitape verifier becomes a single-tape one with at most a quadratic slowdown ([multitape simulation theorem](/multitape-simulation-theorem/)), so the choice of model does not change the statement.

The formula $f(x)$ has $O(T^2)$ variables and $O(T^3)$ clauses with the construction below. The reduction is also a [Levin reduction](/levin-reduction/) (certificates and satisfying assignments map to each other in polynomial time) and is [parsimonious](/parsimonious-reduction/) (the number of satisfying assignments equals the number of accepted certificates). The same holds for [3-SAT](/3-sat/): each long clause splits into clauses of 3 literals with new variables, so 3-SAT is NP-complete too.

## In plain words

Every problem in NP has a checking program: given a proposed solution, it decides quickly whether the solution is right. A run of that program is a table. Each row is the full state of the machine at one moment: which step it is on, where it is reading, and what is written on its tape. The rules that link one row to the next are local. Each one talks only about a few neighboring entries. All of these rules, together with "the first row holds the input" and "the last row says accept", can be written as one long logic formula. The formula has a true setting exactly when some proposed solution makes the program accept. So a fast method for [satisfiability](/sat/) would give a fast method for every problem in NP.

## Proof

The full proof is in [the proof page](proofs/main.md). This is its outline.

**Membership.** An assignment to the variables is a certificate, and a verifier checks every clause in time polynomial in the length of the formula.

**The map.** Fix $L \in \mathsf{NP}$, the single-tape machine $M$ with states $Q$ and tape alphabet $\Gamma$, and an input $x$ of length $n$. The head starts on cell 0 and moves at most one cell per step, so in $T$ steps it uses only cells $0, \ldots, T$. The formula has variables $Q_{s,q}$ (state $q$ at time $s$), $H_{s,i}$ (head on cell $i$ at time $s$) and $S_{s,i,a}$ (symbol $a$ on cell $i$ at time $s$) for $0 \le s, i \le T$, and five groups of clauses:
1. exactly one state, one head position and one symbol per cell at each time;
2. the start configuration: $x$, then $\#$, then $p(n)$ cells that may hold 0 or 1 (the certificate), then blanks;
3. moves: if at time $s$ the head is on cell $i$ in state $q$ reading $a$, and $\delta(q, a) = (q', b, d)$, then at time $s + 1$ the state is $q'$, cell $i$ holds $b$ and the head is on cell $i + d$ (on cell 0 if $i + d = -1$); halting states repeat;
4. frame: a cell that is not under the head keeps its symbol;
5. accept: the state at time $T$ is $q_{\mathrm{acc}}$.

Each clause of groups 3 and 4 mentions one cell and its time step, which is the sense in which computation is local.

**Cost.** There are $O(T^2)$ variables and $O(T^3)$ clauses; the cubic term comes from the pairwise clauses "the head is not on both cell $i$ and cell $j$". The map runs in time polynomial in $T$ and so in $n$.

**Both directions.** If a certificate $y$ makes $M$ accept, the run of $M$ on $x \# y$ gives a satisfying assignment. Conversely, take any satisfying assignment. Group 1 turns it into a sequence of configurations, group 2 makes the first one the start configuration on $x \# y$ for some $y \in \{0,1\}^{p(n)}$, groups 3 and 4 force each configuration to follow from the one before it by induction on the time, and group 5 makes the last one accepting. So $M$ accepts $x \# y$, and $x \in L$. $\blacksquare$

**Worked example.** A script built the formula for a small verifier and checked it with a model-counting DPLL search. The language is "$x$ contains a 1"; a certificate $y$ of the same length as $x$ marks a position $i$ with $x_i = y_i = 1$. The machine reads the pair as $x_1 y_1 x_2 y_2 \cdots$ (this changes only the start clauses), has 5 states (scan, skip, check, accept, reject) and 3 tape symbols, and runs $T = 2n + 1$ steps. For $n = 2$:

| $x$ | variables | clauses | satisfying assignments | accepted certificates |
|---|---|---|---|---|
| 00 | 174 | 1705 | 0 | none |
| 01 | 174 | 1705 | 2 | 01, 11 |
| 10 | 174 | 1705 | 2 | 10, 11 |
| 11 | 174 | 1705 | 3 | 01, 10, 11 |

The 1705 clauses split into 66 for the states, 96 for the head, 144 for the symbols, 8 for the start, 1300 for the moves, 90 for the frame and 1 for acceptance. The number of satisfying assignments equals the number of accepted certificates in each row, as parsimony says. For the same machine and $x = 0^n$, the counts grow as follows:

| $n$ | $T$ | variables | clauses | head clauses |
|---|---|---|---|---|
| 2 | 5 | 174 | 1705 | 96 |
| 4 | 9 | 450 | 5213 | 460 |
| 8 | 17 | 1386 | 18805 | 2772 |
| 16 | 33 | 4794 | 77669 | 19108 |

The variables grow as $T^2$ and the head clauses as $T^3$.

## Consequences

- **NP-completeness proofs.** A problem $B$ in NP is NP-complete as soon as SAT, or any problem already known to be NP-complete, reduces to $B$. [3-SAT](/3-sat/), [circuit SAT](/circuit-sat/), [Karp's 21 problems](/karps-21-np-complete-problems/) and the problems of the [Garey and Johnson compendium](/garey-johnson-compendium/) were all proved this way. See [NP-completeness proof](/np-completeness-proof/).
- **P versus NP.** $\mathsf{P} = \mathsf{NP}$ if and only if $\mathrm{SAT} \in \mathsf{P}$ (Karp 1972, Corollary 1). The [P versus NP problem](/p-versus-np-problem/) is the question of one problem.
- **Circuits and 3-SAT.** The same tableau, written as a [Boolean circuit](/boolean-circuit/), shows that [circuit SAT](/circuit-sat/) is NP-complete, and the [Tseitin transformation](/tseitin-transformation/) turns a circuit into an equisatisfiable 3-CNF formula of linear size.
- **Search and counting.** Because the reduction is a Levin reduction, finding a satisfying assignment is as hard as finding a certificate for any NP problem ([search problem](/search-problem/), [FNP](/fnp/)). Because it is parsimonious, counting satisfying assignments ([model counting](/model-counting/)) is as hard as counting certificates of any NP problem; this is the start of the theory of the counting class #P (no page here).
- **SAT solvers as general tools.** Any NP problem can be solved in practice by writing it as a CNF formula and calling a [DPLL](/dpll/) or [CDCL](/cdcl/) solver, which is the method of the worked example above.
- **Stronger forms.** The [PCP theorem](/pcp-theorem/) gives a reduction to formulas in which, for no-instances, every assignment falsifies a constant fraction of the clauses.

## Tightness

- **Size.** The construction above has $O(T^3)$ clauses, or $O(T^2)$ with the 2 by 3 windows of Sipser (Section 7.4), which constrain six cells at once instead of naming the head position by number. Cook (1988) gave CNF formulas with $O(T \log T)$ literals for a nondeterministic machine with time bound $T$, using the oblivious simulation of Pippenger and Fischer (1979). No reduction of size $O(T)$ is known for general machines.
- **Clause width.** Clauses of width 3 suffice (3-SAT is NP-complete). Width 2 does not suffice unless P = NP, because [2-SAT](/2-sat/) is in P. Cook (1971) made the same remark: DNF tautology with at most 2 literals per term, which is the complement of 2-SAT, is decidable in polynomial time.
- **Reduction type.** The theorem holds with Karp reductions, which is stronger than the Cook-reduction form that Cook proved. It also holds with logspace reductions, because each clause depends only on $x$, $T$ and a fixed table of $M$; this needs a separate argument that the loops run in logarithmic space.

## History

Cook presented the theorem at STOC in May 1971 (Cook 1971). He showed that every set accepted by a nondeterministic Turing machine in polynomial time is "P-reducible" to the set of DNF tautologies, where P-reducibility is a polynomial-time Turing reduction by a query machine. His proof uses propositional variables for the symbol on each square at each step, the state and the head position, the same as the variables above. His Theorem 2 adds that the tautologies, the DNF tautologies, D3 (DNF tautologies with 3 literals per term) and the subgraph problem are all P-reducible to each other. Cook also noted that he could not add primality or graph isomorphism to this list.

Karp (1972) restated the result for many-one reductions (his Theorem 2, which he credits to Cook and states for SAT) and noted that Cook used a weaker notion of reducibility. Karp's Corollary 1 says that P = NP if and only if SAT is in P. In the Soviet Union, Levin independently defined universal search problems and showed that several natural search problems are universal (Levin 1973); his reductions map instances and also map solutions back. The name "Cook-Levin theorem" credits both. The terms "NP-hard" and "NP-complete" came later, from a poll that Knuth reported in 1974 (see [NP-complete](/np-complete/)).

## References
