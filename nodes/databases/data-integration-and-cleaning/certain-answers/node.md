---
tag: ZTKR4H
kind: definition
slug: certain-answers
name: Certain answers
aliases:
- certain answer semantics
area: databases/data-integration-and-cleaning
level: advanced
summary: "The tuples that are answers to a query in every possible database consistent with the data and the mapping."
prereqs: [conjunctive-query, data-exchange-problem, universal-solution]
see_also: [consistent-query-answering, ontology-mediated-query-answering, sql-null-semantics, gav-and-lav, answering-queries-using-views, open-world-assumption, closed-world-assumption, co-np]
sources:
  - paper: doi:10.1145/1634.1886
    title: "Tomasz Imieliński and Witold Lipski, Incomplete information in relational databases, Journal of the ACM 31(4), 1984"
    locator: "pages 761-791, tables with nulls and the answers that hold in every represented database"
  - paper: doi:10.1016/j.tcs.2004.10.033
    title: "Ronald Fagin, Phokion G. Kolaitis, Renée J. Miller and Lucian Popa, Data exchange: semantics and query answering, Theoretical Computer Science 336(1), 2005"
    locator: certain answers in data exchange and naive evaluation on universal solutions
  - paper: doi:10.1145/275487.275516
    title: "Serge Abiteboul and Oliver M. Duschka, Complexity of answering queries using materialized views, PODS 1998"
    locator: "pages 254-263, certain answers under the open and the closed world assumption"
  - paper: doi:10.1145/543613.543644
    title: "Maurizio Lenzerini, Data integration: a theoretical perspective, PODS 2002"
    locator: "pages 233-246, certain answers in data integration"
  - book: isbn:9781107016163
    title: "Marcelo Arenas, Pablo Barceló, Leonid Libkin and Filip Murlak, Foundations of Data Exchange, Cambridge University Press, 2014"
    locator: "Chapter 7, Query answering and rewriting, and Chapter 8, Alternative semantics"
---

The certain answers of a query over incomplete data are the tuples that are answers in every complete database that the data allows. This page defines them for data exchange, data integration and tables with nulls, where the possible databases come from a mapping or from unknown values. [Consistent query answering](/consistent-query-answering/) uses the same "true in all" idea over the repairs of an inconsistent database, and [ontology-mediated query answering](/ontology-mediated-query-answering/) uses it over the models of an ontology. Here the data is consistent and there is no ontology: the unknowns are the values and the facts that the mapping leaves open.

## Definition

Let $\mathcal W$ be a set of complete databases, the *possible worlds*. For a query $q$ of arity $k$, the **certain answers** are

$$\mathrm{cert}(q, \mathcal W) = \bigcap_{W \in \mathcal W} q(W).$$

For a Boolean query, the certain answer is true if $q$ is true in every world. Set semantics holds. The set $\mathcal W$ comes from the setting.

- **Data exchange.** For a [schema mapping](/schema-mapping/) $\mathcal M$ and a source instance $I$, $\mathcal W$ is the set of solutions for $I$, and $\mathrm{cert}(q, I)$ is written for the certain answers.
- **Data integration.** $\mathcal W$ is the set of global databases that agree with the sources under the [GAV or LAV](/gav-and-lav/) mapping.
- **Tables with nulls.** A table $T$ holds constants and labeled nulls $\bot_1, \bot_2, \ldots$. A *valuation* $v$ replaces each null by a constant. Under the *closed world assumption*, $\mathcal W = \{ v(T) \}$ over all valuations. Under the *open world assumption*, $\mathcal W$ holds each database that contains some $v(T)$.

The answers in $\mathrm{cert}(q, \mathcal W)$ contain only constants, since a tuple with a null is not an answer in a world where that null has two different values.

**Naive evaluation.** Evaluate $q$ on an instance with nulls as if each null were a constant different from all others, then drop each tuple that holds a null.

**Theorem.** Let $q$ be a union of [conjunctive queries](/conjunctive-query/), written as rules $Q(x) \text{ :- } R_1(u_1), \ldots, R_m(u_m)$. Then the certain answers of $q$ are the result of naive evaluation:

- on a table $T$, under the open and under the closed world assumption (Imieliński and Lipski);
- on any [universal solution](/universal-solution/) of a data exchange problem (Fagin, Kolaitis, Miller and Popa).

*Why.* A union of conjunctive queries is preserved by homomorphisms: if $h : J \to W$ is the identity on constants and $t \in q(J)$, then $h(t) \in q(W)$. A universal solution maps into each solution, so each null-free answer on it is an answer in each world. In the other direction, the universal solution with its nulls read as new constants is itself a possible world, so a certain answer is an answer there.

**Complexity, in data complexity.** For unions of conjunctive queries the certain answers take polynomial time in the settings above, with weakly acyclic target dependencies for data exchange. For some fixed conjunctive queries with inequalities they are coNP-complete under the open world assumption, and for some fixed conjunctive queries over views they are coNP-complete under the closed world assumption (Abiteboul and Duschka). With negation, naive evaluation is no longer correct.

## Examples and non-examples

The mapping has $d_1 : \forall x, y\, (\text{Flight}(x, y) \to \exists z\, (\text{Leg}(x, z) \wedge \text{Leg}(z, y)))$ and $d_2 : \forall x, y\, (\text{Flight}(x, y) \to \exists u\, \text{Leg}(x, u))$, and $I = \{\text{Flight}(a, b), \text{Flight}(b, c)\}$. The chase gives the universal solution

$$J = \{\text{Leg}(a, \bot_1), \text{Leg}(\bot_1, b), \text{Leg}(b, \bot_2), \text{Leg}(\bot_2, c), \text{Leg}(a, \bot_3), \text{Leg}(b, \bot_4)\}.$$

| query | naive answers on $J$ | certain answers |
|---|---|---|
| $Q(x, y) \text{ :- } \text{Leg}(x, z), \text{Leg}(z, y)$ | $(a, b)$, $(b, c)$ and tuples with nulls | $\{(a, b), (b, c)\}$ |
| $Q(x) \text{ :- } \text{Leg}(x, y)$ | $a$, $b$, $\bot_1$, $\bot_2$ | $\{a, b\}$ |
| $Q(x, y) \text{ :- } \text{Leg}(x, y)$ | only tuples with nulls | $\emptyset$ |

The last row is the point of certain answers: each flight surely has two legs, but no single leg is known.

**Non-example: negation.** Let $q$ be the Boolean query "no $x$ has $\text{Leg}(x, x)$". Naive evaluation on $J$ says true, since no fact of $J$ has two equal values. But $J_1 = \{\text{Leg}(a, b), \text{Leg}(b, b), \text{Leg}(b, c), \text{Leg}(c, c)\}$ is a solution, and there $q$ is false. So the certain answer is false, and naive evaluation on a universal solution is wrong for this query.

**Non-example: possible answers.** The tuple $(a, c)$ is an answer of the first query on the solution $\{\text{Leg}(a, d), \text{Leg}(d, b), \text{Leg}(b, d), \text{Leg}(d, c)\}$. It is a *possible* answer, true in some world, but not a certain one.

**Non-example: SQL nulls.** A table $R = \{(a, \text{NULL})\}$ and the query "the $x$ with $R(x, y)$ and ($y = 1$ or $y \neq 1$)". In every world the condition is true, so $a$ is a certain answer. SQL gives each comparison with NULL the value unknown, and unknown or unknown is unknown, so SQL returns nothing. See [SQL null semantics](/sql-null-semantics/).

## Related definitions

- **Possible answers.** The union of $q(W)$ over all worlds instead of the intersection.
- **Consistent answers.** The intersection over the repairs of an inconsistent database; see [consistent query answering](/consistent-query-answering/) and [database repair](/database-repair/).
- **Ontology-mediated answers.** The intersection over the models of a set of data facts and an ontology; see [ontology-mediated query answering](/ontology-mediated-query-answering/).
- **Answering queries using views.** For LAV sources, a maximally contained rewriting of a conjunctive query computes its certain answers; see [answering queries using views](/answering-queries-using-views/).
- **Closed world semantics for data exchange.** Restricting the worlds to those justified by the mapping changes the certain answers of queries with negation.

## References
