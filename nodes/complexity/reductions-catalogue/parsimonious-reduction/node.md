---
tag: M0434C
kind: definition
slug: parsimonious-reduction
name: Parsimonious reduction
aliases:
- one-to-one reduction
- parsimonious transformation
- solution-count-preserving reduction
area: complexity/reductions-catalogue
level: advanced
summary: A Karp reduction f between search problems such that x and f(x) always have the same number of solutions. It carries hardness from decision to counting.
prereqs: [polynomial-time-reduction, levin-reduction]
see_also: [model-counting, permanent-computation, tseitin-transformation, cook-levin-theorem, valiant-vazirani-theorem, toda-theorem, counting-problem, turing-reduction]
sources:
  - paper: doi:10.1007/3-540-08342-1_37
    title: "Janos Simon, On the difference between one and many, Automata, Languages and Programming (ICALP 1977), Lecture Notes in Computer Science 52, Springer, 1977, 480-491"
    locator: the definition of parsimonious reductions and the proof that standard NP-completeness reductions can be made parsimonious
  - paper: doi:10.1016/0304-3975(79)90044-6
    title: "Leslie G. Valiant, The complexity of computing the permanent, Theoretical Computer Science 8(2) (1979), 189-201"
    locator: the class #P, completeness for #P, and the #P-completeness of the permanent of 0-1 matrices under polynomial-time Turing reductions
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Section 7.3, The Complexity of Enumeration Problems (p. 167)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Section 2.3.6, the remark that the Cook-Levin reduction is parsimonious; the chapter on the complexity of counting
---

A parsimonious reduction from a search problem $R$ to a search problem $R'$ is a [Karp reduction](/polynomial-time-reduction/) $f$ such that every instance $x$ has exactly as many solutions as $f(x)$. So it reduces the counting problem "how many solutions does $x$ have?" to the counting problem for $R'$ with one question and no change to the answer. Simon (1977) introduced the term, and Valiant (1979) used such reductions in his theory of counting problems. Many textbook NP-completeness reductions are parsimonious or can be made so, but some important counting problems have no parsimonious reduction from SAT unless P = NP.

## Definition

Let $R$ and $R'$ be relations, with $R(x) = \{w : (x, w) \in R\}$ the set of solutions of $x$, as on [Levin reduction](/levin-reduction/). Write $\#R(x) = |R(x)|$.

**Definition.** A *parsimonious reduction* from $R$ to $R'$ is a polynomial-time computable function $f$ such that, for every $x$,

$$\#R(x) = \#R'(f(x)).$$

Taking the case $\#R(x) = 0$ shows that $f$ is a Karp reduction from $L_R$ to $L_{R'}$. Parsimonious reductions compose, since equal counts are kept at each step ([transitivity of reductions](/transitivity-of-reductions/)).

The definition asks only for equal numbers. In practice the proof gives a polynomial-time bijection $h_x : R(x) \to R'(f(x))$ with a polynomial-time inverse, which makes the reduction a Levin reduction as well.

**The counting class.** The class #P consists of the functions $x \mapsto \#R(x)$ for NP relations $R$ (Valiant 1979). A function is #P-complete under parsimonious reductions if its relation is the target of a parsimonious reduction from every NP relation. Counting satisfying assignments ([model counting](/model-counting/), or #SAT) is #P-complete in this sense.

## Examples and non-examples

### Examples

- **Cook-Levin.** The reduction in the [Cook-Levin theorem](/cook-levin-theorem/) is parsimonious when the verifier is fixed and deterministic: each certificate determines exactly one accepting computation, and each satisfying assignment of the formula encodes exactly one such computation (Arora and Barak, Section 2.3.6).
- **Tseitin encoding.** The [Tseitin transformation](/tseitin-transformation/) from a Boolean circuit to a CNF formula adds one variable per gate together with clauses that force the variable to equal the gate's output. Every input assignment extends in exactly one way, so the number of satisfying assignments is kept.
- **A clause with a defined variable.** The clause $(x_1 \lor x_2 \lor x_3 \lor x_4)$ has $15$ satisfying assignments. The formula
$$(\neg x_1 \lor z) \land (\neg x_2 \lor z) \land (\neg z \lor x_1 \lor x_2) \land (z \lor x_3 \lor x_4)$$
forces $z = x_1 \lor x_2$ and then states the original clause, so it also has $15$ satisfying assignments.

### Non-examples

- **Splitting a clause with a free variable.** The usual SAT to [3-SAT](/3-sat/) step replaces $(x_1 \lor x_2 \lor x_3 \lor x_4)$ by $(x_1 \lor x_2 \lor z) \land (\neg z \lor x_3 \lor x_4)$. This preserves satisfiability but not the count: of the $16$ assignments to $x_1, \ldots, x_4$, one has no valid $z$, $6$ have one valid $z$ and $9$ have two, for a total of $6 + 18 = 24$ instead of $15$. The variable $z$ is free whenever both halves are already true.
- **3-SAT to independent set.** For $\varphi = (x_1 \lor x_2 \lor \neg x_3) \land (\neg x_1 \lor x_2 \lor x_3) \land (\neg x_1 \lor \neg x_2 \lor \neg x_3)$, the standard graph $G_\varphi$ has $12$ independent sets of size $3$, but $\varphi$ has $5$ satisfying assignments. An assignment that makes two literals of a clause true gives a choice of vertex in that triangle.
- **A padding variable.** The map $\varphi \mapsto \varphi \land (z \lor \neg z)$ with a new variable $z$ doubles every count. For the same $\varphi$ it gives $10$ instead of $5$. Such a reduction still transfers counting hardness, because the count can be divided by $2$ afterwards, but it is not parsimonious.

### A barrier: easy decision, hard counting

Counting the perfect matchings of a bipartite graph is the [permanent](/permanent-computation/) of its 0-1 adjacency matrix, and Valiant (1979) proved it #P-complete. His proof uses polynomial-time Turing reductions ([Cook reductions](/turing-reduction/)), with several questions and arithmetic on the answers. A parsimonious reduction from #SAT to this problem is not possible unless P = NP. Such a reduction $f$ would satisfy: $\varphi$ is satisfiable if and only if the graph $f(\varphi)$ has a perfect matching. Deciding whether a [perfect matching](/perfect-matching/) exists takes polynomial time, so SAT would be in P. The same argument applies to every counting problem whose decision version is in P.

## Related definitions

- **[Levin reduction](/levin-reduction/)**: maps solutions back and forth in polynomial time. A Levin reduction whose forward map is a bijection is parsimonious.
- **[Cook reduction](/turing-reduction/)**: the reduction used for #P-completeness in general, as in the permanent example.
- **Counting reductions with a correction.** Some reductions satisfy $\#R(x) = a \cdot \#R'(f(x)) + b$ for polynomial-time computable $a$ and $b$, as in the padding example. They are enough for #P-hardness under Cook reductions.
- **Unique solutions.** The [Valiant-Vazirani theorem](/valiant-vazirani-theorem/) gives a randomized reduction from SAT to formulas with at most one solution. It is far from parsimonious: it kills almost all solutions, on purpose.
- **[Counting problems](/counting-problem/)** and [Toda's theorem](/toda-theorem/) place counting above the [polynomial hierarchy](/polynomial-hierarchy/).
- **Garey and Johnson** (1979, Section 7.3) treat enumeration problems and parsimonious transformations.

## References
