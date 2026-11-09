---
tag: 3NGE2G
kind: problem
slug: boolean-constraint-satisfaction
name: Boolean constraint satisfaction problem
aliases:
- generalized satisfiability
- Boolean CSP
- SAT(Gamma)
area: logic-and-constraints/constraint-satisfaction
level: advanced
summary: CSP in which every variable is Boolean and the constraints come from a fixed relation set.
prereqs: [sat, constraint-satisfaction-problem]
see_also: [schaefer-dichotomy-theorem, constraint-language-polymorphisms, horn-sat, 2-sat, xor-sat, counting-csp, one-in-three-sat, not-all-equal-sat]
sources:
  - paper: doi:10.1145/800133.804350
    title: Thomas J. Schaefer, The complexity of satisfiability problems, Proceedings of the 10th ACM Symposium on Theory of Computing (STOC 1978)
    locator: pages 216 to 226 (generalized satisfiability SAT(S), the six polynomial classes, and NP-completeness of all other cases)
  - book: isbn:9780898714791
    title: Nadia Creignou, Sanjeev Khanna and Madhu Sudan, Complexity Classifications of Boolean Constraint Satisfaction Problems, SIAM, 2001
    locator: the chapters on the classes of Boolean relations, on satisfiability, on counting and on optimization problems
  - paper: doi:10.1016/0020-0190(79)90002-4
    title: Bengt Aspvall, Michael F. Plass and Robert E. Tarjan, A linear-time algorithm for testing the truth of certain quantified Boolean formulas, Information Processing Letters 8(3), 1979
    locator: pages 121 to 123 (2-SAT by strongly connected components of the implication graph)
  - paper: "William F. Dowling and Jean H. Gallier, Linear-time algorithms for testing the satisfiability of propositional Horn formulae, Journal of Logic Programming 1(3), 1984, pages 267 to 284"
    locator: Horn satisfiability in time linear in the size of the formula
  - paper: "Eric Allender, Michael Bauland, Neil Immerman, Henning Schnoor and Heribert Vollmer, The complexity of satisfiability problems, refining Schaefer's theorem, Journal of Computer and System Sciences 75(4), 2009, pages 245 to 254"
    locator: the classification of SAT(Gamma) up to AC0 reductions into AC0, L, NL, parity L, P-complete and NP-complete cases
  - paper: "Nadia Creignou and Miki Hermann, Complexity of generalized satisfiability counting problems, Information and Computation 125(1), 1996, pages 1 to 12"
    locator: counting the solutions of SAT(Gamma) is in FP when Gamma is affine and #P-complete otherwise
---

The Boolean constraint satisfaction problem, also called *generalized satisfiability* and written SAT($\Gamma$), fixes a finite set $\Gamma$ of relations on $\{0, 1\}$, the *constraint language*. An instance is a set of Boolean variables and a list of constraints, each of which applies a relation of $\Gamma$ to some of the variables, and the question is whether some assignment satisfies all of them. It is the [constraint satisfaction problem](/constraint-satisfaction-problem/) with domain size 2. [SAT](/sat/) in CNF, [3-SAT](/3-sat/), [2-SAT](/2-sat/), [Horn-SAT](/horn-sat/), [XOR-SAT](/xor-sat/), [one-in-three SAT](/one-in-three-sat/) and [not-all-equal SAT](/not-all-equal-sat/) are all of this form, for different $\Gamma$. Schaefer (1978) introduced the problem and showed that each SAT($\Gamma$) is either in P or NP-complete ([Schaefer's dichotomy theorem](/schaefer-dichotomy-theorem/)).

## In plain words

Each unknown is a yes or a no. You get a short list of rule types, each one a table of the allowed yes and no patterns for a few unknowns, such as "at least one of these two is yes" or "exactly one of these three is yes". An instance uses these rule types many times, on different unknowns. You must decide if some choice of yes and no for every unknown follows all the rules.

The rule types decide how hard this is. If all rules are "at least one of two", there is a fast method. If the rules are "exactly one of three", the problem is as hard as any problem in NP. This page describes the problem for a given list of rule types, the classes of rule types that make it easy, and how each easy class is solved.

## Definition

A Boolean relation of arity $r$ is a set $R \subseteq \{0, 1\}^r$. A *constraint language* $\Gamma$ is a finite set of Boolean relations.

**SAT($\Gamma$).** *Input:* variables $x_1, \ldots, x_n$ and constraints $C_1, \ldots, C_m$, where each $C_k$ is a relation $R_k \in \Gamma$ of arity $r_k$ with a scope $(x_{i_1}, \ldots, x_{i_{r_k}})$. *Question:* is there an assignment $s \in \{0, 1\}^n$ with $(s_{i_1}, \ldots, s_{i_{r_k}}) \in R_k$ for every $k$? The size of an instance is $n + m$, as $\Gamma$ is fixed and each relation has constant size.

The search version asks for such an assignment, and the counting version, #SAT($\Gamma$), asks for the number of them.

**Schaefer's classes.** A relation $R$ is

- *0-valid* if $(0, \ldots, 0) \in R$, and *1-valid* if $(1, \ldots, 1) \in R$;
- *Horn* if $R$ is the set of models of a CNF formula in which each clause has at most one positive literal;
- *dual Horn* if the same holds with at most one negative literal per clause;
- *bijunctive* if $R$ is the set of models of a CNF formula with at most two literals per clause;
- *affine* if $R$ is the set of solutions of a system of linear equations over the field $\mathrm{GF}(2)$, that is, of XOR equations.

A language is in a class if every one of its relations is. Being in each class is the same as being closed under one operation applied coordinate by coordinate, a [polymorphism](/constraint-language-polymorphisms/): the constant 0, the constant 1, $x \wedge y$, $x \vee y$, the majority $\mathrm{maj}(x, y, z)$ and the minority $x \oplus y \oplus z$, in this order. The two constant cases are immediate for non-empty relations. The other four follow from the next proposition and its dual and from the two that follow it.

> **Proposition (Horn is closure under AND).** A relation $R \subseteq \{0, 1\}^r$ is Horn exactly when $u \wedge v \in R$ for all $u, v \in R$.
>
> *Proof.* (Only if.) Let $u$ and $v$ satisfy a Horn clause $\neg x_{a_1} \vee \cdots \vee \neg x_{a_k} \vee x_b$, the head $x_b$ being optional. If $u \wedge v$ falsifies every $\neg x_{a_j}$, then $u$ and $v$ have 1 at each $a_j$, so both have 1 at $b$, and so does $u \wedge v$. So the models of a Horn formula are closed under $\wedge$. (If.) Let $\phi$ be the conjunction of all Horn clauses over $x_1, \ldots, x_r$ that every tuple of $R$ satisfies. Every tuple of $R$ is a model of $\phi$. Let $t \notin R$, let $O$ be the set of places where $t$ is 1, and let $R_t = \{u \in R : u_i = 1 \text{ for all } i \in O\}$. If $R_t$ is empty, every $u \in R$ has a 0 in $O$, so $R$ satisfies the clause $\bigvee_{i \in O} \neg x_i$, and $t$ does not. Otherwise let $m$ be the $\wedge$ of all tuples of $R_t$; then $m \in R$ by closure, and $m$ is 1 on $O$. As $t \notin R$, $m \ne t$, so there is a place $j \notin O$ with $m_j = 1$. Every $u \in R$ satisfies $\bigvee_{i \in O} \neg x_i \vee x_j$: either $u$ has a 0 in $O$, or $u \in R_t$ and then $u_j \ge m_j = 1$. The tuple $t$ falsifies this clause. So in both cases $t$ is not a model of $\phi$, and $R$ is the set of models of $\phi$. $\square$

Swapping 0 and 1 turns Horn into dual Horn and $\wedge$ into $\vee$, so dual Horn is closure under $\vee$.

> **Proposition (bijunctive is closure under majority).** $R$ is bijunctive exactly when $\mathrm{maj}(u, v, w) \in R$ for all $u, v, w \in R$.
>
> *Proof.* (Only if.) If $u$, $v$, $w$ satisfy a clause $\ell_1 \vee \ell_2$, then at least two of them satisfy $\ell_1$ or at least two satisfy $\ell_2$, since each of the three satisfies one of the two literals. The majority takes the value shared by two of them, so it satisfies that literal. (If.) Let $t \notin R$, and suppose that no clause on at most two places is satisfied by all of $R$ and falsified by $t$. Then for every set $S$ of at most two places, some $u \in R$ agrees with $t$ on $S$; otherwise the clause that says "differ from $t$ somewhere on $S$" would be such a clause. We show by induction on $|S|$ that this holds for every set $S$ of places. For $|S| \ge 3$, pick three places $a, b, c \in S$ and tuples $u_a, u_b, u_c \in R$ that agree with $t$ on $S \setminus \{a\}$, $S \setminus \{b\}$ and $S \setminus \{c\}$. At each place of $S$, at least two of them agree with $t$, so $\mathrm{maj}(u_a, u_b, u_c) \in R$ agrees with $t$ on $S$. With $S$ all places, $t \in R$, a contradiction. So the 2-clauses that $R$ satisfies define $R$. $\square$

> **Proposition (affine is closure under minority).** $R$ is affine exactly when $u \oplus v \oplus w \in R$ for all $u, v, w \in R$.
>
> *Proof.* (Only if.) If $a \cdot u = a \cdot v = a \cdot w = c$ over $\mathrm{GF}(2)$, then $a \cdot (u \oplus v \oplus w) = c \oplus c \oplus c = c$. (If.) The empty relation is the solution set of $0 = 1$. Otherwise fix $t_0 \in R$ and let $U = \{u \oplus t_0 : u \in R\}$. Then $0 \in U$, and for $u \oplus t_0$ and $v \oplus t_0$ in $U$, their sum is $(u \oplus t_0 \oplus v) \oplus t_0 \in U$. So $U$ is a linear subspace of $\mathrm{GF}(2)^r$, the kernel of some matrix $A$, and $R = t_0 \oplus U = \{x : A x = A t_0\}$. $\square$

## Variants

- **With constants.** SAT$_C$($\Gamma$) also allows the unary relations $\{0\}$ and $\{1\}$, that is, fixing variables. The classes 0-valid and 1-valid no longer help, since $\{1\}$ is not 0-valid, and the other four classes stay polynomial. Schaefer stated his theorem for this version too.
- **Counting.** #SAT($\Gamma$) is in FP when $\Gamma$ is affine, with $2^{n - \mathrm{rank}}$ solutions or none, and #P-complete otherwise (Creignou and Hermann 1996). So #2-SAT and #Horn-SAT are hard although the decision problems are easy. The general case is the [counting CSP](/counting-csp/).
- **Optimization.** MAX-SAT($\Gamma$), MIN-ONES($\Gamma$) and related problems ask for the best assignment instead of a perfect one. Their approximability is classified in the book of Creignou, Khanna and Sudan (2001).
- **Quantified.** With $\forall$ and $\exists$ on the variables, the problem is in P for Horn, dual Horn, bijunctive and affine languages, and PSPACE-complete otherwise. Aspvall, Plass and Tarjan (1979) gave the linear-time algorithm for quantified 2-CNF.
- **Inside P.** Allender, Bauland, Immerman, Schnoor and Vollmer (2009) refined the polynomial side: up to AC$^0$ reductions, each SAT($\Gamma$) is in AC$^0$, or complete for L, NL, $\oplus$L or P, or NP-complete. For example 2-SAT is NL-complete, Horn-SAT is P-complete and XOR-SAT is $\oplus$L-complete.

## Examples

**Familiar problems as SAT($\Gamma$).**

| Problem | $\Gamma$ | Classes of $\Gamma$ |
|---|---|---|
| 3-SAT | the 8 relations of 3-clauses | none |
| 2-SAT | the 4 relations of 2-clauses, and unit clauses | bijunctive |
| Horn-SAT, clauses of up to 3 literals | clauses with at most one positive literal | Horn |
| XOR-SAT, 3 variables per equation | $x \oplus y \oplus z = 0$ and $= 1$ | affine |
| one-in-three SAT | $\{100, 010, 001\}$ | none |
| not-all-equal 3-SAT | $\{0, 1\}^3 \setminus \{000, 111\}$ | none |
| graph 2-colouring | $\{01, 10\}$ | bijunctive, affine |

**Ternary relations.** There are $2^8 = 256$ relations of arity 3. Of these, 128 are 0-valid, 128 are 1-valid, 122 are Horn, 122 are dual Horn, 166 are bijunctive and 52 are affine. Exactly 15 are in none of the six classes, among them one-in-three and not-all-equal; each of these alone gives an NP-complete problem. The implementation checks all of these counts.

**One relation per class is not enough.** $x \vee y$ is 1-valid, dual Horn and bijunctive. $\neg x \vee \neg y \vee \neg z$ is 0-valid and Horn. The language $\{x \vee y, \; \neg x \vee \neg y \vee \neg z\}$ is in no single class, so SAT of this language is NP-complete. A whole language must fit one class.

**Solving one instance in each class.**

- *Horn.* $x_0$, $x_0 \to x_1$, $x_1 \wedge x_2 \to x_3$, $\neg x_1 \vee \neg x_3$. Forward chaining sets $x_0 = 1$, then $x_1 = 1$, and no rule fires for $x_2$ or $x_3$. The last clause holds, so the least model $(1, 1, 0, 0)$ is a solution.
- *Bijunctive.* $x_0 \vee x_1$, $x_0 \to x_1$, $\neg x_1 \vee \neg x_2$, $x_2 \vee x_3$. The first two force $x_1 = 1$, then $x_2 = 0$ and $x_3 = 1$, and $x_0$ is free. The implication graph method returns $(1, 1, 0, 1)$; there are 2 solutions.
- *Affine.* $x_0 \oplus x_1 \oplus x_2 = 1$, $x_1 \oplus x_2 \oplus x_3 = 1$, $x_0 \oplus x_3 \oplus x_4 = 1$ on 5 variables. The three equations are independent, so the rank is 3 and there are $2^{5 - 3} = 4$ solutions, among them $(1, 1, 1, 1, 1)$.

## Known algorithms

For a fixed language, each constraint is first rewritten in its class: as the Horn, dual Horn or 2-clauses that its relation satisfies, which define it by the propositions above, or as the linear equations that it satisfies. A relation of arity $r$ has at most $3^r$ clauses and $2^{r+1}$ equations to test, a constant for fixed $\Gamma$.

| Class | Algorithm | Time |
|---|---|---|
| 0-valid, 1-valid | assign all 0, or all 1 | $O(n + m)$ |
| Horn | forward chaining to the least model (Dowling and Gallier 1984) | $O(n + m)$ |
| dual Horn | swap 0 and 1, then Horn | $O(n + m)$ |
| bijunctive | strongly connected components of the implication graph (Aspvall, Plass and Tarjan 1979) | $O(n + m)$ |
| affine | Gaussian elimination over $\mathrm{GF}(2)$ | $O(m n \min(m, n))$ bit operations |
| none of these | backtracking search, or a SAT solver | exponential in the worst case |

The proofs that these four algorithms are correct are on the [Schaefer's theorem](/schaefer-dichotomy-theorem/) page. Gaussian elimination also gives the number of solutions, $2^{n - \mathrm{rank}}$ when the system is consistent. Forward chaining finds the least model of a Horn formula, the solution that is below every other solution, which is the reason for its use in logic programming and [Datalog](/datalog/).

The Python implementation recognizes each class from its definition, by computing the clauses or the equations that a relation satisfies and checking that they define it. Its tests check that this agrees with closure under the six polymorphisms for every relation of arity up to 3 and for a sample of arity 4, and they compare each solver and the affine counter with a brute-force search over all $2^n$ assignments.

## Bounds

- **Upper.** SAT($\Gamma$) is in NP for every $\Gamma$, by checking a guessed assignment. It is in P, in linear time apart from the affine case, when $\Gamma$ is in one of the six classes.
- **Lower.** When $\Gamma$ is in none of the six classes, SAT($\Gamma$) is NP-complete (Schaefer 1978), so a polynomial algorithm for it would give P = NP. The affine case can be solved in the time of matrix multiplication; no linear-time algorithm is known for it.
- **Brute force.** Testing all $2^n$ assignments takes $O(2^n m)$ time, and better exponential algorithms exist for 3-SAT and its relatives.

## Reductions

- **From 3-SAT.** 3-SAT is SAT($\Gamma$) for the eight 3-clause relations. Schaefer showed that any $\Gamma$ outside the six classes can express, by conjunctions of its relations with some variables existentially quantified, every Boolean relation, or, when all relations of $\Gamma$ are closed under complement as not-all-equal is, every relation closed under complement. In the first case it expresses 3-SAT directly. In the second it expresses not-all-equal 4-SAT, and 3-SAT reduces to that by one extra variable $z$ that is placed in every clause and fixed to 0 after complementing a solution if needed. These expressions are the *primitive positive definitions* of the [polymorphism](/constraint-language-polymorphisms/) theory, and they give polynomial reductions.
- **One-in-three and NAE.** [One-in-three SAT](/one-in-three-sat/) and [not-all-equal SAT](/not-all-equal-sat/) are NP-complete with positive literals only, by this argument, which makes them common starting points for NP-hardness proofs.
- **To SAT.** Each constraint of arity $r$ is a CNF of at most $2^r$ clauses, so SAT($\Gamma$) reduces to [SAT](/sat/) with linear size growth.
- **From larger domains.** A CSP over a domain of size $d$ reduces to a Boolean CSP by encoding each value in $\lceil \log_2 d \rceil$ bits or by one Boolean variable per value. The new language usually lies in no Schaefer class, so the general case needs the [CSP dichotomy theorem](/csp-dichotomy-theorem/) instead.

## Applications

- **Logic programming and databases.** Horn clauses are the rules of Prolog and Datalog, and the least model computed by forward chaining is their meaning.
- **Scheduling and labelling.** Choices with two options each and pairwise conflicts are 2-SAT, for example in placing labels on a map, 2-colouring and some timetabling steps.
- **Coding and cryptanalysis.** Parity checks of linear codes and linear parts of ciphers are XOR constraints, solved by Gaussian elimination, and SAT solvers for cryptanalysis add Gaussian elimination on XOR clauses.
- **Complexity theory.** Schaefer's classification was the first dichotomy for a large family of problems and the model for later ones: the [CSP dichotomy theorem](/csp-dichotomy-theorem/), the [counting CSP](/counting-csp/) and the optimization variants.

## References
