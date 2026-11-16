---
tag: WKN7HQ
kind: definition
slug: pspace
name: PSPACE
aliases:
- polynomial space
area: complexity/complexity-classes
level: intro
summary: The decision problems that a deterministic Turing machine solves with polynomial space, with no limit on time. QSAT and many two-player games are complete for it.
prereqs: [space-complexity, multitape-turing-machine, np]
see_also: [qsat, savitch-theorem, alternating-turing-machine, ip-equals-pspace, polynomial-hierarchy, exptime, expspace, generalized-geography]
sources:
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition, Cengage (2013)
    locator: Section 8.2, The Class PSPACE; Section 8.3, PSPACE-Completeness
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 4, Space Complexity (PSPACE, PSPACE-completeness and games)
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity, Addison-Wesley (1994)
    locator: Chapter 19, Polynomial Space
  - paper: doi:10.1145/800125.804029
    title: Larry J. Stockmeyer and Albert R. Meyer, Word problems requiring exponential time, Proceedings of the 5th Annual ACM Symposium on Theory of Computing, 1 to 9 (1973)
    locator: the quantified Boolean formula problem is complete for polynomial space
  - paper: doi:10.1016/S0022-0000(70)80006-X
    title: Walter J. Savitch, Relationships between nondeterministic and deterministic tape complexities, Journal of Computer and System Sciences 4(2), 177 to 192 (1970)
    locator: the main theorem, which gives NPSPACE = PSPACE
  - paper: doi:10.1145/322234.322243
    title: Ashok K. Chandra, Dexter C. Kozen and Larry J. Stockmeyer, Alternation, Journal of the ACM 28(1), 114 to 133 (1981)
    locator: alternating polynomial time equals PSPACE
---

PSPACE is the class of decision problems that a deterministic [multitape Turing machine](/multitape-turing-machine/) decides with a number of work cells bounded by a polynomial in the input length, with no bound on the time other than that it halts. Space can be reused and time cannot, so PSPACE is a large class: it contains NP, coNP and the whole [polynomial hierarchy](/polynomial-hierarchy/), and it is a subset of EXP. Nondeterminism adds nothing to it ([Savitch's theorem](/savitch-theorem/)), and neither does alternation in polynomial time. The canonical complete problem is [QSAT](/qsat/), the truth of quantified Boolean formulas, and the typical members are two-player games of polynomial length. It is known that $\mathsf{L} \ne \mathsf{PSPACE}$ and $\mathsf{NL} \ne \mathsf{PSPACE}$. Whether $\mathsf{P} = \mathsf{PSPACE}$ is open.

## Definition

**Model.** The machine is a deterministic multitape Turing machine that halts on every input. Its space on an input is the number of distinct work-tape cells it visits; see [space complexity](/space-complexity/). For bounds of at least $n$, it does not matter whether the input tape counts.

**Definition.** With $\mathsf{DSPACE}(s(n))$ as on the page for [L](/logspace/),

$$\mathsf{PSPACE} = \bigcup_{k \ge 1} \mathsf{DSPACE}(n^k).$$

$\mathsf{NPSPACE}$ is the same union over $\mathsf{NSPACE}(n^k)$, for [nondeterministic machines](/nondeterministic-turing-machine/).

**Robustness.** A one-tape machine can simulate a $k$-tape machine with the same space up to a constant factor, by keeping the $k$ tapes on $k$ tracks. Other standard models, such as the random-access machine with words of polynomial length, simulate each other with a polynomial increase in space. So the class does not depend on the model; see the [multitape simulation theorem](/multitape-simulation-theorem/).

**The time of a polynomial-space machine.** A machine with space $s(n) \ge n$ has at most $|Q| \cdot (n+2) \cdot s(n)^k \cdot |\Gamma|^{k\, s(n)} = 2^{O(s(n))}$ configurations, and a halting deterministic machine never repeats one. So a machine in space $n^k$ halts within $2^{O(n^k)}$ steps, and $\mathsf{PSPACE} \subseteq \mathsf{EXP}$.

**PSPACE-completeness.** A language $B$ is *PSPACE-hard* if $A \le_p B$ for every $A \in \mathsf{PSPACE}$, where $\le_p$ is the [polynomial-time many-one reduction](/polynomial-time-reduction/). It is *PSPACE-complete* if it is also in PSPACE. The standard complete problems are complete under logspace reductions too, and some texts use those. A PSPACE-complete problem is in P if and only if $\mathsf{P} = \mathsf{PSPACE}$, and in NP if and only if $\mathsf{NP} = \mathsf{PSPACE}$. Stockmeyer and Meyer (1973) proved that QSAT is PSPACE-complete; the proof is on the page for [QSAT](/qsat/).

## Examples and non-examples

**SAT, and all of NP.** A formula with $n$ variables can be tested on all $2^n$ assignments one after the other. The machine keeps an $n$-bit counter for the current assignment and erases its work space after each evaluation. For 20 variables the counter has 20 bits and runs through $2^{20} = 1048576$ assignments, but the space stays linear in the length of the formula. The same method works for any NP verifier: go through all certificates of length $p(n)$ and run the verifier on each. So $\mathsf{NP} \subseteq \mathsf{PSPACE}$, and since PSPACE is closed under complement, $\mathsf{coNP} \subseteq \mathsf{PSPACE}$.

**QSAT.** A formula $\exists x_1 \forall x_2 \cdots Q x_n\, \varphi$ is evaluated by a recursion on the first quantifier: try $x_1 = 0$ and $x_1 = 1$, evaluate the rest on each, and combine the answers with OR for $\exists$ and AND for $\forall$. The recursion depth is $n$ and each level stores one bit and a pointer, so the space is $O(n + |\varphi|)$, while the time is $2^n$ evaluations. QSAT is PSPACE-complete; see [QSAT](/qsat/) and, for practical solvers, [QBF](/qbf/).

**Games.** In a two-player game where every play ends within a polynomial number of moves, the question "does the first player have a winning strategy?" is in PSPACE. A depth-first [minimax](/minimax/) search stores only the current line of play, one position per move. Many such games are PSPACE-complete: [generalized geography](/generalized-geography/), and deciding the winner of [Hex](/hex-game/) from a given position on an $n \times n$ board.

**More PSPACE-complete problems.** Equivalence and universality of regular expressions and of nondeterministic finite automata ([regular expression equivalence](/regex-equivalence-pspace-completeness/), [NFA universality](/nfa-universality/)); plan existence in STRIPS planning ([STRIPS](/strips-plan-existence-pspace-complete/)); [LTL model checking](/ltl-model-checking-pspace-completeness/); and puzzles where the number of moves is not bounded by a polynomial, such as [Sokoban](/sokoban-problem/) and [Rush Hour](/rush-hour-problem/). In these puzzles a solution may be exponentially long, which is why they are not in NP as far as anyone knows.

**Regular expressions with squaring (not in PSPACE).** If regular expressions may also use a squaring operator, equivalence becomes EXPSPACE-complete (Meyer and Stockmeyer 1972). Since $\mathsf{PSPACE} \subsetneq \mathsf{EXPSPACE}$ by the [space hierarchy theorem](/space-hierarchy-theorem/), this problem is not in PSPACE. This is an unconditional non-example; see [EXPSPACE](/expspace/).

**EXP-complete problems (not known to be in PSPACE).** An [EXP](/exptime/)-complete problem is in PSPACE if and only if $\mathsf{PSPACE} = \mathsf{EXP}$, which is open.

## Related definitions

- **NPSPACE.** $\mathsf{NSPACE}(s) \subseteq \mathsf{DSPACE}(s^2)$ for $s(n) \ge \log n$, so $\mathsf{NSPACE}(n^k) \subseteq \mathsf{DSPACE}(n^{2k})$ and $\mathsf{NPSPACE} = \mathsf{PSPACE}$. See [Savitch's theorem](/savitch-theorem/).
- **Alternation.** $\mathsf{AP} = \mathsf{PSPACE}$, where AP is alternating polynomial time (Chandra, Kozen and Stockmeyer 1981). The proof is on the page for the [alternating Turing machine](/alternating-turing-machine/).
- **Interactive proofs.** $\mathsf{IP} = \mathsf{PSPACE}$. See [IP = PSPACE](/ip-equals-pspace/).
- **The polynomial hierarchy.** Each level $\Sigma_k^p$ is in PSPACE, so $\mathsf{PH} \subseteq \mathsf{PSPACE}$. Whether they are equal is open. If they are equal, then PH collapses to a finite level, because PSPACE has a complete problem and that problem would lie in some $\Sigma_k^p$. See [polynomial hierarchy](/polynomial-hierarchy/).
- **The chain.** $\mathsf{L} \subseteq \mathsf{NL} \subseteq \mathsf{P} \subseteq \mathsf{NP} \subseteq \mathsf{PH} \subseteq \mathsf{PSPACE} \subseteq \mathsf{EXP} \subseteq \mathsf{EXPSPACE}$. The known strict inclusions that involve PSPACE are $\mathsf{NL} \subsetneq \mathsf{PSPACE}$ and $\mathsf{PSPACE} \subsetneq \mathsf{EXPSPACE}$, both from the space hierarchy theorem. $\mathsf{P} \subsetneq \mathsf{EXP}$ by the [time hierarchy theorem](/time-hierarchy-theorem/), so at least one of $\mathsf{P} \ne \mathsf{PSPACE}$ and $\mathsf{PSPACE} \ne \mathsf{EXP}$ is true, but nobody knows which.

## References
