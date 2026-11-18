---
tag: A26C5V
kind: concept
slug: gav-and-lav
name: Global-as-view and local-as-view
aliases:
- GAV
- LAV
- GLAV mappings
area: databases/data-integration-and-cleaning
level: core
summary: "Two ways to relate sources to a mediated schema: define each global relation as a view of sources, or each source as a view of the global schema."
prereqs: [conjunctive-query, schema-mapping, materialized-view]
see_also: [answering-queries-using-views, inverse-rules-algorithm, minicon-algorithm, bucket-algorithm, certain-answers, data-exchange-problem, open-world-assumption, ontology-mediated-query-answering]
sources:
  - paper: doi:10.1145/543613.543644
    title: "Maurizio Lenzerini, Data integration: a theoretical perspective, PODS 2002"
    locator: "pages 233-246, the GAV and LAV approaches and sound, complete and exact sources"
  - book: isbn:9780124160446
    title: "AnHai Doan, Alon Halevy and Zachary Ives, Principles of Data Integration, Morgan Kaufmann, 2012"
    locator: "Chapter 3, Describing Data Sources"
  - paper: doi:10.1145/275487.275516
    title: "Serge Abiteboul and Oliver M. Duschka, Complexity of answering queries using materialized views, PODS 1998"
    locator: "pages 254-263, the open and the closed world assumption"
---

Global-as-view (GAV) and local-as-view (LAV) are the two classic ways to state how data sources relate to the mediated, or global, schema of a data integration system. In GAV, each global relation is defined as a query over the sources. In LAV, each source is described as a query over the global schema. Both are special forms of a [schema mapping](/schema-mapping/): that page defines mappings in general and their semantics, while this page is about the two forms and what each one means for answering queries.

## In plain words

A travel site shows one list of routes, but the routes come from many airline databases. Someone must write down how the site's list relates to the airlines' data.

One way is to say, for each list on the site, which airline data fills it. This is global-as-view. Answering a question is then easy: replace each list by the recipe that fills it. But a new airline means changing the recipes.

The other way is to say, for each airline database, what part of the site's lists it shows. This is local-as-view. A new airline only needs its own description. But the site now knows the data only in part, for example "there is some stop between these two cities", and it must reason about what is surely true.

## The idea

A data integration system has a global schema $\mathbf G$, a source schema $\mathbf S$ and a mapping between them. The data stays in the sources. A user asks a query over $\mathbf G$, and the system answers it from the source data. Each global database that agrees with the sources under the mapping is a possible world, and the system returns the [certain answers](/certain-answers/): the tuples that are answers in every possible world.

**GAV.** Each global relation $g$ gets a query $q_{\mathbf S}$ over the sources. As a dependency this is $\forall x\, (q_{\mathbf S}(x) \to g(x))$, with one global atom in the head and no existential variable. If the global schema has no constraints, the global database is fixed by the sources: it is the result of the definitions. A query over $\mathbf G$ is answered by *unfolding*: each global atom is replaced by its definition, and the result runs on the sources.

**LAV.** Each source relation $s$ gets a query $q_{\mathbf G}$ over the global schema. As a dependency this is $\forall x\, (s(x) \to \exists y\, q_{\mathbf G}(x, y))$, with one source atom in the body. The sources now fix the global database only in part, and query answering is [answering queries using views](/answering-queries-using-views/) under incomplete information. For sound sources with conjunctive view definitions and conjunctive queries, a maximally contained rewriting, found for example by the [inverse rules](/inverse-rules-algorithm/), [bucket](/bucket-algorithm/) or [MiniCon](/minicon-algorithm/) algorithm, gives the certain answers.

**Sound, complete and exact sources.** Lenzerini distinguishes three readings of a source description. A *sound* source holds a subset of the tuples of its query, a *complete* source a superset, and an *exact* source exactly those tuples. The common default is sound sources, which is the [open world assumption](/open-world-assumption/). Exact sources give the closed world assumption, and there Abiteboul and Duschka showed that the certain answers of conjunctive queries over conjunctive views are coNP-complete in data complexity. Under the open world assumption the same problem takes polynomial time in data complexity.

**The trade-off.** GAV makes query answering simple and puts the work in the definitions: a new source can change many of them. LAV makes adding a source local and puts the work in query answering. The general form, with a conjunction of source atoms in the body and a conjunction of global atoms in the head, contains both. It is the source-to-target tgd of [data exchange](/data-exchange-problem/), where the target is built instead of left virtual.

## Examples

The global schema has $\text{Route}(x, y)$, a flight leg from $x$ to $y$. Source Direct lists some direct routes. Source TwoHop lists pairs of cities with a connection through exactly one unnamed stop. The data is $\text{Direct} = \{(a, b)\}$ and $\text{TwoHop} = \{(b, d)\}$.

**LAV.** The descriptions are

$$\forall x, y\, (\text{Direct}(x, y) \to \text{Route}(x, y)),$$
$$\forall x, y\, (\text{TwoHop}(x, y) \to \exists z\, (\text{Route}(x, z) \wedge \text{Route}(z, y))).$$

Every possible world contains $\text{Route}(a, b)$, $\text{Route}(b, \bot)$ and $\text{Route}(\bot, d)$ for some value $\bot$. The query $Q(x, y) \text{ :- } \text{Route}(x, z_1), \text{Route}(z_1, z_2), \text{Route}(z_2, y)$ has the certain answer $(a, d)$, along $a, b, \bot, d$. The rewriting $Q'(x, y) \text{ :- } \text{Direct}(x, z), \text{TwoHop}(z, y)$ over the sources finds it. The query $\text{Route}(x, y)$ has only the certain answer $(a, b)$, because the stop is unknown.

**GAV.** A global relation must be a query over the sources, so the unnamed stop of TwoHop cannot become a Route fact. A GAV design adds a global relation $\text{Conn2}(x, y)$ for "a connection with one stop" and defines

$$\forall x, y\, (\text{Direct}(x, y) \to \text{Route}(x, y)),$$
$$\forall x, y\, (\text{TwoHop}(x, y) \to \text{Conn2}(x, y)),$$
$$\forall x, y, z\, (\text{Direct}(x, z) \wedge \text{Direct}(z, y) \to \text{Conn2}(x, y)).$$

A query over Conn2 unfolds to the union of TwoHop and the self-join of Direct. A new source of three-leg trips means a new global relation and new definitions.

## Where it is used

- **Mediator systems.** Early research mediators each took one side: some defined the global relations over the sources, others described each source over a global schema. The book of Doan, Halevy and Ives compares both and the general form.
- **Data exchange.** The same dependencies, read as rules to build a target instance, define the [data exchange problem](/data-exchange-problem/).
- **Ontology-based data access.** Systems that answer queries over an ontology often map the data to the ontology with GAV rules and leave the incomplete part to the ontology; see [ontology-mediated query answering](/ontology-mediated-query-answering/).
- **Query rewriting with views.** LAV query answering is the theory behind rewriting queries with [materialized views](/materialized-view/).

## References
