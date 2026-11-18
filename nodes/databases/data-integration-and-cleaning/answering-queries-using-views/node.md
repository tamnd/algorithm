---
tag: M2VGDE
kind: problem
slug: answering-queries-using-views
name: Answering queries using views
aliases:
- query rewriting using views
- view-based query answering
area: databases/data-integration-and-cleaning
level: advanced
summary: "Rewrite a query over a schema into one that uses only a given set of views, either equivalently or as a maximally contained rewriting."
prereqs: [conjunctive-query, query-containment-problem, chandra-merlin-theorem, gav-and-lav]
see_also: [view-rewriting-np-completeness, bucket-algorithm, inverse-rules-algorithm, minicon-algorithm, certain-answers, materialized-view, view-selection, data-exchange-problem]
sources:
  - paper: doi:10.1007/s007780100054
    title: "Alon Y. Halevy, Answering queries using views: a survey, The VLDB Journal 10(4), 2001"
    locator: "pages 270-294, the definitions of equivalent and maximally contained rewritings, the algorithms and the complexity results"
  - paper: doi:10.1145/212433.220198
    title: "Alon Y. Levy, Alberto O. Mendelzon, Yehoshua Sagiv and Divesh Srivastava, Answering queries using views, PODS 1995"
    locator: "pages 95-104, equivalent rewritings and their NP-completeness"
  - paper: doi:10.1145/275487.275516
    title: "Serge Abiteboul and Oliver M. Duschka, Complexity of answering queries using materialized views, PODS 1998"
    locator: "the complexity of certain answers under the open and the closed world assumption"
  - book: isbn:9780124160446
    title: "AnHai Doan, Alon Halevy and Zachary Ives, Principles of Data Integration, Morgan Kaufmann, 2012"
    locator: "Chapter 2, manipulating query expressions, and Chapter 3, describing data sources"
---

Answering queries using views asks how to compute a query when you can read only the stored results of some other queries, the views, and not the base relations. This page states the problem and its variants. The [NP-completeness theorem](/view-rewriting-np-completeness/) covers the hardness of the equivalent version, and the pages on the [bucket algorithm](/bucket-algorithm/), [MiniCon](/minicon-algorithm/) and [inverse rules](/inverse-rules-algorithm/) give the methods for the contained version. The problem is the core of local-as-view [data integration](/gav-and-lav/), where each source is described as a view over a global schema, and of query optimization with [materialized views](/materialized-view/).

## In plain words

A database keeps a few tables of answers to earlier questions, and a new question comes in. Can the new question be answered from the stored tables alone? Sometimes the stored tables give exactly the right answers. Sometimes they give only part of them, because a table forgot a value that the question needs.

In query optimization you want the exact answers, so the question is whether an exact plan from the stored tables exists. In data integration, the stored tables are the sources and they are all you have, so you want the plan that returns as many right answers as the sources allow, and never a wrong one.

## Definition

**Input.** A query $Q(\bar x) \text{ :- } R_1(\bar u_1), \ldots, R_n(\bar u_n)$ over a schema, in AHV notation, and a set $\mathcal V$ of views, each a conjunctive query $V(\bar Y) \text{ :- } S_1(\bar w_1), \ldots, S_r(\bar w_r)$ over the same schema. Set semantics holds. For a query $P$ over the view names, the *expansion* $P^{exp}$ replaces each view atom by the body of its view, with new variables for the existential variables of the view.

**Rewritings.**

- $P$ is an *equivalent rewriting* of $Q$ if $P^{exp} \equiv Q$: on every database, $P$ evaluated on the views gives $Q$.
- $P$ is a *contained rewriting* if $P^{exp} \subseteq Q$: it never gives a wrong answer.
- $P$ is a *maximally contained rewriting* in a query language $\mathcal L$ if $P \in \mathcal L$ is contained and every contained rewriting in $\mathcal L$ is contained in $P$.

Containment is tested by the [Chandra-Merlin theorem](/chandra-merlin-theorem/) when $P$ is a conjunctive query or a union of them.

**Certain answers.** A second form of the problem fixes a view instance $I$, a set of tuples for each view. Under the *open world assumption*, a database $D$ is possible if $I(V) \subseteq V(D)$ for each view, and under the *closed world assumption*, if $I(V) = V(D)$. The [certain answers](/certain-answers/) are the tuples that $Q$ returns on every possible $D$. Here the output is a set of tuples, not a query.

## Variants

- **Equivalent or maximally contained.** The first is the goal of query optimization, the second the goal of data integration.
- **Complete or partial.** A complete rewriting uses only views. A partial one may also use base relations, which matters in optimization, where the base relations are still there.
- **The query language.** The query and the views may be conjunctive queries, with or without comparisons, unions of them, or [Datalog](/datalog/) programs. The language of the rewriting matters too: for a recursive query, the maximally contained rewriting can need recursion.
- **Open or closed world.** The sources may hold only some of the tuples of their definition, or exactly those tuples.
- **Access patterns.** A source may answer only when some arguments are given, like a web form.
- **Bag semantics.** SQL counts duplicates, and rewritings under bags need stronger conditions. This page treats sets only.

## Examples

Take $Q(x) \text{ :- } \text{cites}(x, y), \text{cites}(y, x), \text{sameTopic}(x, y)$ and the views

- $V_4(a) \text{ :- } \text{cites}(a, b), \text{cites}(b, a)$,
- $V_5(c, d) \text{ :- } \text{sameTopic}(c, d)$,
- $V_6(f, h) \text{ :- } \text{cites}(f, g), \text{cites}(g, h), \text{sameTopic}(f, g)$.

| candidate | expansion | status |
|---|---|---|
| $Q'(x) \text{ :- } V_6(x, x)$ | cites$(x, g)$, cites$(g, x)$, sameTopic$(x, g)$ | equivalent to $Q$ |
| $Q'(x) \text{ :- } V_4(x), V_5(x, y)$ | cites$(x, b)$, cites$(b, x)$, sameTopic$(x, y)$ | not contained: nothing says $y = b$ |
| $Q'(x) \text{ :- } V_6(x, x), V_4(x)$ | the first one plus cites$(x, b')$, cites$(b', x)$ | equivalent too, but the $V_4$ atom is redundant |

The first rewriting is equivalent to $Q$, so it is also a maximally contained rewriting among unions of conjunctive queries. The third one maps onto the first with $b' \mapsto g$, so dropping its $V_4$ atom keeps it equivalent.

For the chain $Q(x, w) \text{ :- } e(x, y), e(y, z), e(z, w)$ with only the view $V_1(a, c) \text{ :- } e(a, b), e(b, c)$, no contained rewriting exists. In an expansion, each edge joins a view argument to a fresh middle variable, so every walk between two head variables has even length, and the path of length 3 in $Q$ cannot map into it. The maximally contained rewriting is the empty union. Adding $V_2(a, b) \text{ :- } e(a, b)$ gives the equivalent rewriting $Q'(x, w) \text{ :- } V_2(x, y), V_2(y, z), V_2(z, w)$. The rewritings $Q'(x, w) \text{ :- } V_1(x, y), V_2(y, w)$ and $Q'(x, w) \text{ :- } V_2(x, y), V_1(y, w)$ are equivalent too, and the bucket algorithm returns all three.

## Known algorithms

- **Bounded search for equivalent rewritings.** By the theorem of Levy, Mendelzon, Sagiv and Srivastava, it suffices to try rewritings with at most $n$ view atoms and test each for equivalence.
- **[Bucket algorithm](/bucket-algorithm/).** For each subgoal, collect the views that can cover it, then test each combination for containment.
- **[MiniCon](/minicon-algorithm/).** Form, for each view, the smallest sets of subgoals it must cover together, then combine disjoint sets. No containment test is needed at the end.
- **[Inverse rules](/inverse-rules-algorithm/).** Turn the views into Datalog rules with Skolem terms and evaluate the query. This handles recursive queries and gives the certain answers under the open world assumption.

## Bounds

All results are for conjunctive views. Each is a theorem, and each says whether it is in data or combined complexity.

- **Existence of an equivalent rewriting.** NP-complete in combined complexity for conjunctive queries and views, with rewritings of at most $n$ view atoms (Levy, Mendelzon, Sagiv and Srivastava).
- **Maximally contained rewriting.** For a conjunctive query, it always exists among unions of conjunctive queries and can be computed, for example by MiniCon. The number of disjuncts can be exponential in $n$.
- **Certain answers, open world.** For a conjunctive or Datalog query, polynomial time in data complexity, by the inverse rules or by evaluating the maximally contained rewriting (Duschka and Genesereth; Abiteboul and Duschka). For a conjunctive query with inequalities $\ne$, coNP-complete in data complexity (Abiteboul and Duschka).
- **Certain answers, closed world.** For conjunctive queries and views, coNP-complete in data complexity (Abiteboul and Duschka).

## Reductions

- **From containment.** Containment of Boolean conjunctive queries reduces to the existence of an equivalent rewriting with one view, which gives the NP-hardness.
- **To containment.** In the other direction, the bounded search reduces the existence of an equivalent rewriting to a polynomial-size guess and two containment checks.
- **To data exchange.** A local-as-view setting is a [data exchange](/data-exchange-problem/) setting with the source-to-target dependencies $V(\bar Y) \to \exists \bar z\, \text{body}(V)$, read in the open world. The certain answers are the same, and the instance built by the inverse rules is, after the Skolem terms are read as labeled nulls, the result of the [chase](/chase-algorithm/).
- **To certain answers.** For conjunctive queries and views under the open world assumption, evaluating the maximally contained rewriting on the view instance gives exactly the certain answers.

## Applications

- **Data integration.** Systems such as the Information Manifold described each web source as a view over a global schema and used the bucket algorithm to plan queries.
- **Query optimization.** Database systems use materialized views to answer queries faster, which needs equivalent rewritings, often partial ones.
- **[View selection](/view-selection/).** Choosing which views to store for a workload needs to know which queries the views can answer.
- **Semantic caching.** A client keeps answers of earlier queries and answers new queries from them when it can.

## References
