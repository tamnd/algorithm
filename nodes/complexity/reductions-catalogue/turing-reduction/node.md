---
tag: 8ZQ9Q3
kind: definition
slug: turing-reduction
name: Cook reduction
aliases:
- Polynomial-time Turing reduction
- Turing reduction
- oracle reduction
area: complexity/reductions-catalogue
level: core
summary: A Cook reduction decides A in polynomial time with an oracle for B. It may ask many questions and combine the answers, which a Karp reduction cannot do.
prereqs: [polynomial-time-reduction]
see_also: [oracle-turing-machine, turing-degrees, search-to-decision-reduction, self-reducibility, transitivity-of-reductions, np-hard, polynomial-hierarchy, reduction]
sources:
  - paper: doi:10.1145/800157.805047
    title: "Stephen A. Cook, The complexity of theorem-proving procedures, Proceedings of the 3rd Annual ACM Symposium on Theory of Computing (STOC), 1971, 151-158"
    locator: the definition of P-reducibility with a query machine, and the proof that every set accepted in nondeterministic polynomial time is P-reducible to the tautologies
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Section 5.1, Turing Reducibility and NP-Hard Problems (p. 109), and Section 5.2, A Terminological History
  - paper: doi:10.1016/0304-3975(75)90016-X
    title: "Richard E. Ladner, Nancy A. Lynch and Alan L. Selman, A comparison of polynomial time reducibilities, Theoretical Computer Science 1(2) (1975), 103-123"
    locator: the definitions of polynomial-time Turing, truth-table and many-one reducibility and the sets that separate them
  - book: isbn:9780521884730
    title: Oded Goldreich, Computational Complexity, A Conceptual Perspective, Cambridge University Press, 2008
    locator: Section 2.2.1, the general notion of a reduction (Cook reductions, with Karp reductions as a special case)
---

This page is about polynomial-time Turing reductions, also called Cook reductions. A Cook reduction from a problem $A$ to a problem $B$ is a polynomial-time algorithm that decides $A$ and may ask questions of the form "is $y$ in $B$?" to a solver for $B$, with each answer given in one step. It is written $A \le_T^p B$. In computability theory, a Turing reduction is the same idea with no time bound: an [oracle Turing machine](/oracle-turing-machine/) with oracle $B$ decides $A$, and the classes of sets that reduce to each other are the [Turing degrees](/turing-degrees/).

## Definition

An *oracle Turing machine* $M$ is a deterministic Turing machine with an extra *query tape* and three extra states $q_?$, $q_{\text{yes}}$ and $q_{\text{no}}$. For a language $B \subseteq \{0,1\}^*$, the machine $M^B$ runs as follows: when $M$ enters $q_?$ with a string $y$ on the query tape, in the next step it is in state $q_{\text{yes}}$ if $y \in B$ and in $q_{\text{no}}$ if $y \notin B$. The query costs one step. The details of the model, such as whether the query tape is erased after a query, do not change the class of polynomial-time reductions.

**Definition.** Let $A, B \subseteq \{0,1\}^*$. A *Cook reduction* (polynomial-time Turing reduction) from $A$ to $B$ is an oracle Turing machine $M$ and a polynomial $p$ such that, for every input $x$,

1. $M^B$ halts within $p(|x|)$ steps, and
2. $M^B$ accepts $x$ if and only if $x \in A$.

We write $A \le_T^p B$ when such an $M$ exists.

Because $M$ runs for at most $p(|x|)$ steps, it asks at most $p(|x|)$ questions, and each question has length at most $p(|x|)$. The answers can be used in any way: the machine can negate them, combine them, and choose the next question from the earlier answers (an *adaptive* reduction).

**Special cases.**

- A *truth-table reduction* ($A \le_{tt}^p B$) is a Cook reduction whose questions depend only on $x$, not on earlier answers. It computes a list of questions $y_1, \ldots, y_k$ and a Boolean function, then applies the function to the answers.
- A [Karp reduction](/polynomial-time-reduction/) ($A \le_m^p B$) is a Cook reduction that asks exactly one question, $f(x)$, and accepts exactly when the answer is yes.

So $A \le_m^p B \Rightarrow A \le_{tt}^p B \Rightarrow A \le_T^p B$. Ladner, Lynch and Selman (1975) constructed decidable sets that show that these three relations, and several between them, are all different.

**Basic properties.** For all languages $A$, $B$ and $C$:

- $\le_T^p$ is reflexive and transitive. The machine for $A \le_T^p C$ runs the machine for $A \le_T^p B$ and answers each of its questions by running the machine for $B \le_T^p C$. The time bound is on [transitivity of reductions](/transitivity-of-reductions/).
- $\bar A \le_T^p A$, where $\bar A$ is the complement: ask "is $x$ in $A$?" and negate the answer. More generally, $A \le_T^p B$ if and only if $A \le_T^p \bar B$.
- If $A \le_T^p B$ and $B \in$ [P](/p/), then $A \in$ P: replace each question by a run of the polynomial-time algorithm for $B$.
- [NP](/np/) is closed under Cook reductions if and only if NP = [coNP](/co-np/). If NP is closed, then $\overline{\mathrm{SAT}} \le_T^p \mathrm{SAT}$ puts $\overline{\mathrm{SAT}}$ in NP. Conversely, if NP = coNP, a nondeterministic machine can guess all the oracle answers together with certificates for the yes answers and for the no answers.

## Examples and non-examples

### Examples

- **Unsatisfiability from satisfiability, one question.** On input $\varphi$, ask whether $\varphi \in \mathrm{SAT}$ and return the opposite answer. This is a Cook reduction from $\overline{\mathrm{SAT}}$ to SAT. A Karp reduction between these two exists if and only if NP = coNP (the proof is on [reduction](/reduction/)). So the tautology problem TAUT is [NP-hard](/np-hard/) under Cook reductions, and it is not known to be NP-hard under Karp reductions.
- **The clique number, by binary search.** The problem "is the size of the largest clique of $G$ equal to $k$?" Cook-reduces to [CLIQUE](/clique-problem/) ("does $G$ have a clique of size at least $k$?"). Binary search over $k$ finds the clique number $\omega(G)$ with $\lceil \log_2 n \rceil$ questions. Take the graph on vertices $0, \ldots, 6$ with $11$ edges: all edges inside $\{0,1,2,3\}$, the triangle $\{4,5,6\}$, and the edges $3$-$4$ and $2$-$5$. The search asks $k = 4$ (yes), $k = 6$ (no) and $k = 5$ (no), so $\omega(G) = 4$, with $3 = \lceil \log_2 7 \rceil$ questions. The questions are adaptive: the second depends on the first answer.
- **Finding a solution.** A Cook reduction may also compute a function. The [search-to-decision reduction](/search-to-decision-reduction/) for SAT fixes the variables one at a time and asks $n + 1$ questions to a SAT oracle to find a satisfying assignment. Such reductions are the subject of [self-reducibility](/self-reducibility/).
- **Truth-table form.** "Is $\omega(G) = k$?" can also be decided with two fixed questions, "clique of size $k$?" and "clique of size $k+1$?", accepting when the answers are yes and no. This is a truth-table reduction with $2$ questions.

### Non-examples

- **Too many questions.** Deciding SAT by asking a "does this assignment satisfy $\varphi$?" oracle about all $2^n$ assignments uses exponential time, so it is not a Cook reduction, even though each question is easy.
- **A guessing machine.** A nondeterministic polynomial-time machine with an oracle for $B$ defines the class $\mathsf{NP}^B$, not a Cook reduction. For example, every language in $\mathsf{NP}^{\mathrm{SAT}} = \Sigma_2^p$ of the [polynomial hierarchy](/polynomial-hierarchy/) reduces to SAT this way, but these languages are not known to Cook-reduce to SAT.
- **Expected polynomial time.** A randomized algorithm with an oracle is a randomized reduction, not a Cook reduction. Examples are the [Valiant-Vazirani theorem](/valiant-vazirani-theorem/) and parts of [Toda's theorem](/toda-theorem/).

## Related definitions

- **[Karp reduction](/polynomial-time-reduction/)**: the one-question special case. NP-completeness is defined with Karp reductions, and most hardness proofs give one even when only a Cook reduction is needed.
- **NP-hard under Cook reductions**: Garey and Johnson (1979, Section 5.1) call a problem NP-hard when SAT Cook-reduces to it. This covers search and optimization problems, which are not languages. For decision problems, Karp-hardness implies Cook-hardness.
- **$\mathsf{P}^B$**: the set of languages that Cook-reduce to $B$. For example, $\mathsf{P}^{\mathrm{SAT}}$ is the class $\Delta_2^p$ of the [polynomial hierarchy](/polynomial-hierarchy/).
- **[Levin reduction](/levin-reduction/)** and **[parsimonious reduction](/parsimonious-reduction/)**: Karp reductions with extra conditions on solutions. Counting problems such as the [permanent](/permanent-computation/) are hard for #P under Cook reductions, not under parsimonious ones.
- **Logspace Turing reduction**: the oracle machine has $O(\log n)$ work space and a write-only query tape. It is used below P, together with [logspace](/logspace/) many-one reductions.
- **[Turing reducibility](/turing-degrees/)** in computability theory: the same oracle machine with no time bound.
- **[Optimization to decision](/optimization-to-decision-reduction/)**: the Cook reductions that find an optimal value by binary search on a bound, as in the clique example.

## References
