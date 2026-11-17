---
tag: VKD5N6
kind: definition
slug: data-and-combined-complexity
name: Data complexity and combined complexity
aliases:
- data complexity
- combined complexity
area: databases/relational-theory
level: advanced
summary: "Vardi's measures of the cost of query evaluation: with the query fixed and only the database as input (data), with both as input (combined), or with the database fixed (expression)."
prereqs: [relational-calculus, np-complete]
see_also: [conjunctive-query, chandra-merlin-theorem, datalog, yannakakis-algorithm, ac0, pspace, qsat, dalvi-suciu-dichotomy]
sources:
  - paper: doi:10.1145/800070.802186
    title: Moshe Y. Vardi, The complexity of relational query languages (extended abstract), Proceedings of the 14th Annual ACM Symposium on Theory of Computing (STOC), 137 to 146 (1982)
    locator: the definitions of data complexity and expression complexity, and the bounds for the calculus, its fixpoint extensions and the algebra with loops
  - paper: doi:10.1145/800105.803397
    title: Ashok K. Chandra and Philip M. Merlin, Optimal implementation of conjunctive queries in relational data bases, Proceedings of the 9th Annual ACM Symposium on Theory of Computing (STOC), 77 to 90 (1977)
    locator: the evaluation of conjunctive queries is NP-complete when the query is part of the input
  - book: isbn:9783540212027
    title: Leonid Libkin, Elements of Finite Model Theory, Springer (2004)
    locator: Chapter 6 (complexity of first-order logic), Section 6.1 (data, expression and combined complexity) and Section 6.5 (combined complexity of FO), with the AC0 bound for data complexity
  - paper: doi:10.1145/502807.502810
    title: Evgeny Dantsin, Thomas Eiter, Georg Gottlob and Andrei Voronkov, Complexity and expressive power of logic programming, ACM Computing Surveys 33(3), 374 to 425 (2001)
    locator: data complexity P-complete and combined complexity EXPTIME-complete for Datalog
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 6 (the complexity of conjunctive query evaluation) and Part E (expressiveness and complexity of query languages)
  - paper: "Mihalis Yannakakis, Algorithms for acyclic database schemes, Proceedings of the 7th International Conference on Very Large Data Bases (VLDB), 82 to 94 (1981)"
    locator: evaluation of acyclic conjunctive queries in time polynomial in the input and the output
  - paper: "Christos H. Papadimitriou and Mihalis Yannakakis, On the complexity of database queries, Journal of Computer and System Sciences 58(3), 407 to 427 (1999)"
    locator: parameterized complexity of query evaluation, with the size of the query as the parameter
---

Data complexity and combined complexity are two ways to measure how hard it is to evaluate the queries of a query language. Data complexity fixes the query and counts the cost as a function of the size of the database only; combined complexity counts it as a function of the sizes of both the query and the database. Vardi defined them in 1982, with a third measure, expression complexity, which fixes the database. The difference matters because queries are short and databases are large: first-order queries are cheap in data complexity (in [AC0](/ac0/)) but [PSPACE](/pspace/)-complete in combined complexity.

## Definition

Let $\mathcal{L}$ be a query language, such as the [relational calculus](/relational-calculus/) (FO), the [conjunctive queries](/conjunctive-query/) (CQ) or [Datalog](/datalog/). Its *evaluation problem* is the set

$$\mathrm{Eval}_{\mathcal{L}} = \{\, (Q, I, t) \mid Q \in \mathcal{L},\ I \text{ an instance},\ t \in Q(I) \,\},$$

under set semantics; for a Boolean query, $t$ is the empty tuple and the question is whether $Q$ is true on $I$. The size $|I|$ is the length of a standard encoding of the instance, about the number of tuples times the arity times the length of a constant; $|Q|$ is the length of the query. Let $\mathcal{C}$ be a complexity class.

- **Data complexity.** For each fixed $Q \in \mathcal{L}$, consider the problem $\mathrm{Eval}_Q = \{(I, t) \mid t \in Q(I)\}$, with input size $|I| + |t|$. $\mathcal{L}$ has data complexity in $\mathcal{C}$ if $\mathrm{Eval}_Q \in \mathcal{C}$ for every $Q \in \mathcal{L}$. It is $\mathcal{C}$-complete if, in addition, $\mathrm{Eval}_Q$ is $\mathcal{C}$-hard for some $Q$.
- **Combined complexity.** The problem $\mathrm{Eval}_{\mathcal{L}}$ itself, with input size $|Q| + |I| + |t|$.
- **Expression complexity** (also called query complexity). For each fixed $I$, the problem $\{(Q, t) \mid t \in Q(I)\}$; $\mathcal{L}$ has expression complexity in $\mathcal{C}$ if this is in $\mathcal{C}$ for every $I$, and $\mathcal{C}$-complete if it is also $\mathcal{C}$-hard for some $I$.

The data complexity of a language is a statement about each query separately: "polynomial" means that for each $Q$ there is a polynomial $p_Q$, and the degree of $p_Q$ may grow with $Q$. Combined complexity is the worst case over all pairs. Combined complexity is always at least as high as each of the other two.

**The standard bounds.**

| Language | Data complexity | Combined complexity |
|---|---|---|
| CQ | in AC0 | NP-complete (Chandra and Merlin 1977) |
| acyclic CQ | in AC0 | polynomial (Yannakakis 1981) |
| FO (algebra, calculus) | in AC0 | PSPACE-complete (Vardi 1982) |
| Datalog | P-complete | EXPTIME-complete |

The AC0 bound and the PSPACE bound for FO are in Libkin (2004), Chapter 6; Vardi (1982) gave the bound LOGSPACE for the data complexity of FO, and AC0 is smaller. The Datalog bounds are in Vardi (1982) and in the survey of Dantsin, Eiter, Gottlob and Voronkov (2001). For FO and for CQ, the expression complexity is as high as the combined complexity, by the reductions below, which use a fixed database.

## Examples and non-examples

- **FO is polynomial in data complexity.** Fix an FO query $Q$. Evaluate it bottom up under active domain semantics: for each subformula with $m$ free variables, store the table of the valuations into the active domain that make it true. With $n$ values, the table has at most $n^m$ rows, and each connective or quantifier builds a table from smaller ones in time polynomial in $n^m$. If $w$ is the largest number of free variables of a subformula, the time is $|Q| \cdot n^{O(w)}$. For a fixed $Q$, $w$ is a constant, so the time is polynomial in $|I|$; but $w$ grows with the query, so this bound says nothing in combined complexity.
- **CQ is NP-hard in combined and in expression complexity.** Take the fixed database $K_3$: one binary relation $E$ with the 6 pairs $(a, b)$ of distinct values from $\{1, 2, 3\}$. For a graph $G$ with nodes $v_1, \ldots, v_n$, let $Q_G$ be the Boolean CQ with one variable per node and one atom $E(x_u, x_v)$ per edge. A valuation that makes the body true is a map from the nodes to $\{1, 2, 3\}$ that gives different colors to the ends of each edge. So $Q_G$ is true on $K_3$ if and only if $G$ is [3-colorable](/three-coloring/). For the cycle of length 5 there are 30 such valuations and $Q_G$ is true; for the complete graph $K_4$ there are none and $Q_G$ is false. The database never changes, so the expression complexity is NP-hard; membership in [NP](/np/) holds because a valuation is a certificate. This is the hard half of the result of [Chandra and Merlin](/chandra-merlin-theorem/).
- **FO is PSPACE-hard in combined and in expression complexity.** Take the fixed database with $\mathrm{Bool} = \{0, 1\}$ and $\mathrm{One} = \{1\}$. A [quantified Boolean formula](/qsat/) $\forall p_1 \exists p_2 \cdots \theta$ becomes the Boolean FO query $\forall x_1 (\mathrm{Bool}(x_1) \rightarrow \exists x_2 (\mathrm{Bool}(x_2) \land \cdots \theta'))$, where $\theta'$ replaces each $p_i$ by $\mathrm{One}(x_i)$. The query is true on the database if and only if the formula is true. Membership in PSPACE: evaluate the formula by recursion on its structure, with one value per quantified variable on the stack, in space $O(|Q| \log |I|)$.
- **Datalog is P-complete in data complexity.** One fixed program, the alternating path or the monotone circuit value program, is P-hard. Every fixed program reaches its least fixed point after a polynomial number of rounds, each of polynomial time; see [Datalog evaluation](/datalog-evaluation/).
- **Non-example: a bound with the wrong measure.** "CQ evaluation is NP-complete" and "CQ evaluation is in AC0" are both true, under different measures. A statement of a bound that does not name its measure is incomplete. The same holds for probabilistic databases: the [Dalvi-Suciu dichotomy](/dalvi-suciu-dichotomy/) is a statement in data complexity, so a "polynomial-time" query there may still take time exponential in the query.
- **Non-example: a constant that hides the query.** A naive evaluator of a CQ with $k$ variables over $n$ values tries $n^k$ valuations, for example $10^6$ for $n = 10$ and $k = 6$. In data complexity this is "polynomial". Papadimitriou and Yannakakis (1999) showed that CQ evaluation, with the query size as parameter, is complete for the parameterized class W[1], so a bound of the form $f(k) \cdot n^{c}$ with $c$ independent of $k$ is unlikely.

## Related definitions

- **Classes.** [AC0](/ac0/), [LOGSPACE](/logspace/), [P](/p/), [NP](/np/), [PSPACE](/pspace/) and [EXPTIME](/exptime/) are the classes of the table above.
- **Query containment.** The complexity of [query containment](/query-containment-problem/) is a statement about pairs of queries, with no database; for CQs it equals the combined complexity of evaluation, by the canonical database of the [Chandra-Merlin theorem](/chandra-merlin-theorem/).
- **Tractable classes in combined complexity.** Acyclic CQs are evaluated by the [Yannakakis algorithm](/yannakakis-algorithm/) in time polynomial in the query, the input and the output. Bounded [hypertree width](/hypertree-width/) extends this.
- **Codd's theorem.** The FO bounds hold for relational algebra too, by [Codd's theorem](/codds-theorem/), whose translations are polynomial in size.
- **Counting and probability.** For a probabilistic database the question is the probability of the answer, and the class is the counting class #P (see [model counting](/model-counting/)) rather than a decision class; see [probabilistic database](/probabilistic-database/).

## References
