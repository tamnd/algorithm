---
tag: Y141B9
kind: definition
slug: npo-class
name: NPO
aliases:
- NP optimization class
- NP optimization problem
area: approximation/hardness-of-approximation
level: advanced
summary: The class of optimization problems whose instances and solutions are checkable in polynomial time and whose measure is computable in polynomial time. APX and PTAS are subclasses.
prereqs: [np, polynomial-time, approximation-ratio]
see_also: [apx-class, apx, ptas, fptas, approximation-preserving-reduction, gap-problem, decision-problem, fnp]
sources:
  - book: isbn:9783540654315
    title: Giorgio Ausiello, Pierluigi Crescenzi, Giorgio Gambosi, Viggo Kann, Alberto Marchetti-Spaccamela and Marco Protasi, Complexity and Approximation, Springer, 1999
    locator: Chapter 1, The Complexity of Optimization Problems (the definition of NPO and PO), and Chapter 3, Approximation Classes (APX, PTAS, FPTAS and their inclusions)
  - paper: doi:10.1137/S0097539795286612
    title: Sanjeev Khanna, Rajeev Motwani, Madhu Sudan and Umesh Vazirani, On syntactic versus computational views of approximability, SIAM Journal on Computing 28(1), 1998
    locator: Section 2, Definitions 1 and 2 (the error and the performance ratio of a solution of an NPO problem)
  - paper: doi:10.1016/0022-0000(91)90023-X
    title: Christos H. Papadimitriou and Mihalis Yannakakis, Optimization, approximation, and complexity classes, Journal of Computer and System Sciences 43(3), 1991
    locator: pp. 425 to 440, Section 2 (optimization problems and their decision versions)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, W. H. Freeman, 1979
    locator: Chapter 6, Coping with NP-Complete Problems (approximation algorithms and performance guarantees)
---

NPO is the class of NP optimization problems: the optimization problems whose instances and feasible solutions a polynomial-time machine can recognize and whose objective it can compute. It is the optimization analog of [NP](/np/), and its decision versions are exactly NP languages. The classes [APX](/apx-class/), [PTAS](/ptas/) and [FPTAS](/fptas/) are subclasses of NPO, and the [approximation-preserving reductions](/approximation-preserving-reduction/) are defined between NPO problems. This page follows the formal definition of Ausiello et al. (1999).

## Definition

**NPO problem.** An NP optimization problem is a quadruple $\Pi = (I, \mathrm{SOL}, m, \mathrm{goal})$ with these four parts.

1. $I \subseteq \{0,1\}^*$ is the set of *instances*, and membership in $I$ is decidable in [polynomial time](/polynomial-time/).
2. $\mathrm{SOL}$ maps each instance $x \in I$ to a set $\mathrm{SOL}(x)$ of *feasible solutions*. There is a polynomial $p$ such that $|y| \le p(|x|)$ for each $y \in \mathrm{SOL}(x)$, and for each pair $(x, y)$ with $|y| \le p(|x|)$, the question "$y \in \mathrm{SOL}(x)$?" is decidable in polynomial time.
3. The *measure* $m(x, y)$ is defined for $x \in I$ and $y \in \mathrm{SOL}(x)$, its value is a positive integer, and it is computable in polynomial time.
4. $\mathrm{goal} \in \{\min, \max\}$.

We also assume that $\mathrm{SOL}(x) \ne \emptyset$ for each $x \in I$, so that the optimum exists. The *optimum* of $x$ is

$$\mathrm{OPT}(x) = \mathrm{goal}\,\{\, m(x, y) : y \in \mathrm{SOL}(x) \,\},$$

and $y$ is an *optimal solution* when $m(x, y) = \mathrm{OPT}(x)$. **NPO** is the class of all NP optimization problems. **PO** is the subclass of the problems for which a polynomial-time algorithm returns an optimal solution of each instance.

**Notation and ratios.** On this page $n = |x|$ is the length of the instance. An algorithm returns a feasible solution with value ALG. For a minimization problem, a $\rho$-approximation has $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ with $\rho \ge 1$. For a maximization problem, an $\alpha$-approximation has $\mathrm{ALG} \ge \alpha \cdot \mathrm{OPT}$ with $\alpha \le 1$. Ausiello et al. use one *performance ratio* for both goals,

$$R(x, y) = \max\left( \frac{m(x, y)}{\mathrm{OPT}(x)},\ \frac{\mathrm{OPT}(x)}{m(x, y)} \right) \ge 1,$$

so a maximization ratio $\alpha$ on this site is $1/R$ in their book. The measure is positive, so both quotients are defined. All ratios here are absolute and worst case.

**Underlying decision problem.** For a maximization problem, $\Pi_D = \{ (x, k) : x \in I,\ \exists\, y \in \mathrm{SOL}(x) \text{ with } m(x, y) \ge k \}$. For a minimization problem, replace $\ge$ by $\le$.

**Proposition 1.** For each $\Pi \in$ NPO, $\Pi_D \in$ NP.

*Proof.* The [certificate](/certificate/) of $(x, k)$ is a feasible solution $y$ with $m(x, y) \ge k$ (or $\le k$). Its length is at most $p(|x|)$ by part 2. The verifier checks $x \in I$ (part 1), checks $y \in \mathrm{SOL}(x)$ (part 2), computes $m(x, y)$ (part 3) and compares it with $k$. Each step takes polynomial time. If $(x, k) \in \Pi_D$, some $y$ passes. If $(x, k) \notin \Pi_D$, no string passes, because each string that passes is a feasible solution with a good enough value. $\blacksquare$

**Proposition 2.** If P = NP, then PO = NPO.

*Proof.* Take $\Pi \in$ NPO with goal max; the min case is symmetric. The measure is computed in time $t(|x|)$ for a polynomial $t$, so $1 \le m(x, y) < 2^{t(|x|)}$. Let $L' = \{ (x, k, w) : \exists\, y \in \mathrm{SOL}(x),\ w \text{ is a prefix of } y,\ m(x, y) \ge k \}$. The certificate is $y$ itself, so $L' \in$ NP, and by the hypothesis $L' \in$ P. (1) A binary search on $k \in [1, 2^{t(|x|)})$ with the query $(x, k, \varepsilon)$, where $\varepsilon$ is the empty prefix, finds $\mathrm{OPT}(x)$ with $t(|x|)$ queries. (2) Start with $w = \varepsilon$. While $w \notin \mathrm{SOL}(x)$ or $m(x, w) < \mathrm{OPT}(x)$, one of $(x, \mathrm{OPT}(x), w0)$ and $(x, \mathrm{OPT}(x), w1)$ is in $L'$, because an optimal solution with prefix $w$ exists and is longer than $w$; append that bit to $w$. The invariant "some optimal solution has prefix $w$" holds at each step, and the length of $w$ grows by 1, so the loop stops after at most $p(|x|)$ steps with an optimal solution. Each step is a polynomial-time test, so $\Pi \in$ PO. $\blacksquare$

The two propositions show why the hardness results of this area assume P $\ne$ NP: without that assumption, every NPO problem is solvable exactly.

## Examples and non-examples

**Minimum vertex cover.** An instance is a graph $G = (V, E)$. $\mathrm{SOL}(G)$ is the set of [vertex covers](/vertex-cover/), the sets $C \subseteq V$ with $u \in C$ or $v \in C$ for each edge $uv$. The measure is $|C|$ and the goal is min. A cover has at most $|V|$ vertices, and the test "is $C$ a cover?" scans the edges. The set $V$ is always a cover, so $\mathrm{SOL}(G) \ne \emptyset$. For the 5-cycle $C_5$, there are 11 vertex covers, the optimum is 3, and 5 of the covers have size 3. The 2-approximation by a [maximal matching](/vertex-cover-2-approximation/) shows that the problem is in [APX](/apx-class/).

**Maximum 3-satisfiability.** An instance is a CNF formula with at most 3 literals in each clause. A solution is a truth assignment, and the measure is the number of satisfied clauses. With the convention that the measure is positive, add one clause that is always true, for example $(x \lor \lnot x)$; this shifts each value by 1. This is [MAX 3SAT](/max-sat/), the first APX-complete problem (see [APX-completeness](/apx-completeness/)).

**Knapsack.** An instance is a list of weights, profits and a capacity in binary. A solution is a set of items within the capacity, and the measure is the total profit, a number with polynomially many digits. Knapsack is in NPO, but it is not *polynomially bounded*: its optimum can be exponential in $n$. It has an [FPTAS](/knapsack-fptas/).

**Non-example: a solution of exponential length.** Take the problem "given $k$ disks, output a shortest legal sequence of moves for the Towers of Hanoi". The instance has $O(\log k)$ digits, but each solution has at least $2^k - 1$ moves (1023 moves for $k = 10$). Part 2 fails, because no polynomial in the instance length bounds the length of a solution.

**Non-example: feasibility that is hard to check.** Take "given a Boolean circuit, find a smallest circuit that computes the same function". The feasibility test is the equivalence of two circuits, which is coNP-complete. Part 2 asks for a polynomial-time test, so this problem is not known to be in NPO, unless P = NP. Its natural home is higher in the [polynomial hierarchy](/polynomial-hierarchy/).

**Non-example: a decision problem.** [SAT](/sat/) itself has no measure. Its optimization version MAX SAT is in NPO; SAT is the decision problem "is $\mathrm{OPT} = $ the number of clauses?".

## Related definitions

- **NPO-PB.** The polynomially bounded problems of NPO: there is a polynomial $q$ with $m(x, y) \le q(|x|)$ for each feasible $y$. MAX 3SAT, vertex cover and maximum clique are in NPO-PB; knapsack and TSP with binary weights are not.
- **The approximation classes.** With $\rho$ as above: [APX](/apx-class/) holds the problems with a polynomial-time $\rho$-approximation for some constant $\rho$; [PTAS](/ptas/) holds the problems with a $(1 + \varepsilon)$-approximation (or $(1 - \varepsilon)$ for max) for each fixed $\varepsilon > 0$; [FPTAS](/fptas/) asks for time polynomial in $n$ and $1/\varepsilon$. Then $\mathrm{PO} \subseteq \mathrm{FPTAS} \subseteq \mathrm{PTAS} \subseteq \mathrm{APX} \subseteq \mathrm{NPO}$, and each inclusion is strict if P $\ne$ NP (Ausiello et al., Chapter 3). For example, knapsack is in FPTAS but not in PO, and MAX 3SAT is in APX but not in PTAS, unless P = NP. Proposition 2 shows that all five classes are equal if P = NP.
- **FNP.** [FNP](/fnp/) is the class of search problems "find any $y$ with $(x, y) \in R$"; NPO adds a measure and asks for the best $y$.
- **Reductions.** [Approximation-preserving reductions](/approximation-preserving-reduction/) such as the [L-reduction](/l-reduction/) and the [PTAS-reduction](/ptas-reduction/) map an NPO problem to another one, with a map for the instances and a map back for the solutions.
- **Gap problems.** A [gap problem](/gap-problem/) is a promise version of $\Pi_D$ with two thresholds. It is the usual tool to show that an NPO problem is hard to approximate.

## References
