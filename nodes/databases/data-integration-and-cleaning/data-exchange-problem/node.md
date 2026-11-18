---
tag: H27N8G
kind: problem
slug: data-exchange-problem
name: Data exchange problem
aliases:
- data exchange
area: databases/data-integration-and-cleaning
level: advanced
summary: "Given a source instance and a schema mapping, build a target instance that satisfies the mapping and answer queries over it."
prereqs: [schema-mapping, tuple-generating-dependency, equality-generating-dependency, chase-algorithm]
see_also: [universal-solution, data-exchange-core-computation, weak-acyclicity, certain-answers, gav-and-lav, schema-mapping-composition, data-and-combined-complexity, undecidability]
sources:
  - paper: doi:10.1016/j.tcs.2004.10.033
    title: "Ronald Fagin, Phokion G. Kolaitis, Renée J. Miller and Lucian Popa, Data exchange: semantics and query answering, Theoretical Computer Science 336(1), 2005"
    locator: "pages 89-124, data exchange settings, universal solutions, the chase and certain answers"
  - book: isbn:9781107016163
    title: "Marcelo Arenas, Pablo Barceló, Leonid Libkin and Filip Murlak, Foundations of Data Exchange, Cambridge University Press, 2014"
    locator: "Chapters 4 to 7: the problem of relational data exchange, existence of solutions, good solutions, query answering and rewriting"
  - paper: doi:10.1145/1142351.1142357
    title: "Phokion G. Kolaitis, Jonathan Panttaja and Wang-Chiew Tan, The complexity of data exchange, PODS 2006"
    locator: pages 30-39
  - paper: doi:10.1145/275487.275516
    title: "Serge Abiteboul and Oliver M. Duschka, Complexity of answering queries using materialized views, PODS 1998"
    locator: "pages 254-263, conjunctive queries with inequalities"
---

The data exchange problem takes data structured under a source schema and a [schema mapping](/schema-mapping/) to a target schema, and asks for a target instance that satisfies the mapping, built for real, together with a way to answer queries over it. The mapping usually allows many target instances, so the problem also asks which one to build and which query answers are trustworthy. This page states the problem and its complexity. The [universal solution](/universal-solution/) page defines the preferred target instances, and [core computation](/data-exchange-core-computation/) gives the smallest of them. Unlike [GAV and LAV](/gav-and-lav/) integration, which leaves the target virtual, data exchange materializes it.

## In plain words

An airline sends its timetable to a travel site. The two systems store trips in different ways, and a set of rules says how one form becomes the other. Some rules need values the airline does not have, such as the airport of a stop. The site must still store something, so it stores placeholders for the unknown values.

Many target databases follow the rules, and they disagree on the placeholders. The site wants one that claims nothing beyond what the rules force, so that a question gets only the answers that hold whatever the unknown values are. For simple questions, one database built in a mechanical way does this. With rules on the target side as well, a solution may not exist at all, and in the worst case no program can decide whether it does.

## Definition

**Input.** A schema mapping $\mathcal M = (\mathbf S, \mathbf T, \Sigma_{st} \cup \Sigma_t)$, where $\Sigma_{st}$ is a set of source-to-target tgds $\forall x\, (\varphi_{\mathbf S}(x) \to \exists y\, \psi_{\mathbf T}(x, y))$ and $\Sigma_t$ is a set of target tgds and egds $\forall x\, (\varphi_{\mathbf T}(x) \to x_i = x_j)$. A source instance $I$ over constants. Set semantics holds throughout.

**Solutions.** A target instance $J$, over constants and labeled nulls $\bot_1, \bot_2, \ldots$, is a *solution* for $I$ if $(I, J)$ satisfies $\Sigma_{st} \cup \Sigma_t$.

**The three tasks.**

1. *Existence of solutions:* decide whether $I$ has a solution.
2. *Materialization:* build a solution, preferably a [universal solution](/universal-solution/), which has a homomorphism into every solution.
3. *Query answering:* for a target query $q$, compute the [certain answers](/certain-answers/) $\mathrm{cert}(q, I) = \bigcap \{\, q(J) : J \text{ a solution for } I \,\}$.

Complexity is measured in data complexity, with $\mathcal M$ and $q$ fixed and $I$ as the input, unless combined complexity is named.

## Variants

- **No target dependencies.** $\Sigma_t = \emptyset$. A solution always exists.
- **Target egds.** Keys and functional dependencies on the target. The chase can fail, and then no solution exists.
- **Weakly acyclic target tgds and egds.** The standard setting, where every chase stops; see [weak acyclicity](/weak-acyclicity/).
- **Arbitrary target tgds.** The chase may run forever.
- **Other semantics.** Closed world solutions, which allow only what the mapping justifies, give other certain answers, in particular for queries with negation.
- **Other data models.** XML data exchange, with tree patterns in the mapping.

## Examples

The mapping has $d_1 : \forall x, y\, (\text{Flight}(x, y) \to \exists z\, (\text{Leg}(x, z) \wedge \text{Leg}(z, y)))$ and $d_2 : \forall x, y\, (\text{Flight}(x, y) \to \exists u\, \text{Leg}(x, u))$.

**A solution by the chase.** For $I = \{\text{Flight}(a, b), \text{Flight}(b, c)\}$ with $\Sigma_t = \emptyset$, the chase gives

$$J = \{\text{Leg}(a, \bot_1), \text{Leg}(\bot_1, b), \text{Leg}(b, \bot_2), \text{Leg}(\bot_2, c), \text{Leg}(a, \bot_3), \text{Leg}(b, \bot_4)\}.$$

It is a universal solution. The query $Q(x, y) \text{ :- } \text{Leg}(x, z), \text{Leg}(z, y)$ has the certain answers $\{(a, b), (b, c)\}$: these are the null-free answers of $Q$ on $J$.

**A target egd that forces equalities.** Add the egd $\forall x, y, y'\, (\text{Leg}(x, y) \wedge \text{Leg}(x, y') \to y = y')$: each city has at most one next leg. The chase on the same $I$ merges $\bot_3$ with $\bot_1$ and $\bot_4$ with $\bot_2$, and the result is the first four facts of $J$, up to the names of the nulls.

**No solution.** With the same egd and $I' = \{\text{Flight}(a, b), \text{Flight}(a, c)\}$, every solution has $\text{Leg}(a, z_1), \text{Leg}(z_1, b), \text{Leg}(a, z_2), \text{Leg}(z_2, c)$. The egd gives $z_1 = z_2$ and then $b = c$. Two different constants cannot be equal, so the chase fails and $I'$ has no solution.

## Known algorithms

- **The chase.** Apply the dependencies as rules, with fresh nulls for the existential variables, until all hold. If it stops without failure, the result is a universal solution. If an egd equates two constants, there is no solution. For source-to-target tgds, the oblivious chase gives the *canonical universal solution*.
- **Core computation.** Shrink a universal solution to its core, the smallest universal solution; see [core computation for data exchange](/data-exchange-core-computation/).
- **Naive evaluation.** For a union of conjunctive queries, evaluate the query on any universal solution as if the nulls were constants and drop the tuples with nulls. The result is the certain answers.
- **Query rewriting.** For some classes of mappings and queries, rewrite the target query so that it runs on the source.

## Bounds

All bounds are in data complexity unless stated.

- **No target dependencies.** The canonical universal solution has polynomial size and takes polynomial time. Certain answers of unions of conjunctive queries take polynomial time (theorem, Fagin, Kolaitis, Miller and Popa).
- **Weakly acyclic target tgds with egds.** Each chase sequence has polynomial length, so the existence of solutions is decidable in polynomial time, and a universal solution is built in polynomial time when one exists (theorem, same paper). Certain answers of unions of conjunctive queries stay polynomial.
- **Combined complexity.** With the mapping as part of the input, the chase can make a number of nulls doubly exponential in the size of the mapping, even for weakly acyclic sets.
- **Arbitrary target tgds.** The existence of solutions is undecidable (theorem; see Arenas, Barceló, Libkin and Murlak, Chapter 5, and Kolaitis, Panttaja and Tan for the complexity of the problem).
- **Queries with inequalities.** For some fixed conjunctive queries with inequalities the certain answers are coNP-complete. Abiteboul and Duschka showed this for views, which is data exchange with LAV source-to-target tgds and no target dependencies.

## Reductions

- **Certain answers to naive evaluation.** For unions of conjunctive queries, $\mathrm{cert}(q, I)$ is the set of null-free tuples of $q(J)$ for any universal solution $J$. The reason is that $q$ is preserved by homomorphisms, and $J$ maps into each solution.
- **Data integration as data exchange.** With $\Sigma_t = \emptyset$, the solutions are the global databases of a data integration system with sound sources and the same mapping. So the certain answers are the same in both settings, and LAV query answering with views is a special case.
- **Existence of a universal solution.** When a solution exists and the chase stops, the chase result is universal. With weakly acyclic dependencies, a solution exists if and only if a universal solution exists.

## Applications

- **Extract, transform and load.** Moving data from operational systems into a warehouse is data exchange, with mappings written as rules.
- **Data migration.** Moving a database to a new schema, keeping what the old data says and no more.
- **Schema mapping tools.** Research prototypes generate mappings from [schema matching](/schema-matching/) correspondences and run them as data exchange programs.
- **Mapping management.** [Composition](/schema-mapping-composition/) and inversion of mappings build on the semantics of data exchange.

## References
