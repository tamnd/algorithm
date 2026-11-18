---
tag: V1W0JZ
kind: problem
slug: schema-matching
name: Schema matching
aliases:
- schema alignment
- attribute correspondence discovery
area: databases/data-integration-and-cleaning
level: core
summary: "Find the correspondences between the elements of two schemas that denote the same thing, as the first step of a mapping."
prereqs: [relational-model, edit-distance, assignment-problem]
see_also: [similarity-flooding, schema-mapping, gav-and-lav, entity-resolution, jaccard-similarity, hungarian-algorithm, stable-matching, subgraph-isomorphism]
sources:
  - paper: doi:10.1007/s007780100057
    title: "Erhard Rahm and Philip A. Bernstein, A survey of approaches to automatic schema matching, VLDB Journal 10(4), 2001"
    locator: "pages 334-350, the classification of matchers and their combination"
  - book: isbn:9780124160446
    title: "AnHai Doan, Alon Halevy and Zachary Ives, Principles of Data Integration, Morgan Kaufmann, 2012"
    locator: "Chapter 5, Schema Matching and Mapping"
  - paper: doi:10.1109/ICDE.2002.994702
    title: "Sergey Melnik, Hector Garcia-Molina and Erhard Rahm, Similarity flooding: a versatile graph matching algorithm and its application to schema matching, ICDE 2002"
    locator: pages 117-128
---

Schema matching is the problem of finding which elements of two schemas mean the same thing, for example that the column Name of one table holds the same data as the column FullName of another. The output is a set of correspondences, often with a confidence score. It has no exact formal goal: the right answer is the one a domain expert would accept, so all general methods are heuristics, judged by measurement. The correspondences are the input to the next step, where a person or a tool turns them into a [schema mapping](/schema-mapping/) with joins and new values.

## In plain words

Two companies merge, and each has a customer table. One calls a column "FullName", the other calls it "Name". One stores the date of birth as text, the other as a date. Before the data can be combined, someone must say which column of the first table goes with which column of the second.

A program can help by looking for clues. Similar names are one clue. Similar data types are another. Similar values in the columns, such as both holding mostly email addresses, are a strong clue. Tables that sit in the same place in both designs are a clue too. Each clue alone is often wrong, so good tools combine many of them and show the best guesses to a person, who makes the final choice.

## Definition

**Input.** Two schemas $S_1$ and $S_2$ with sets of elements $E_1$ and $E_2$: relations, attributes, and for nested schemas, the inner elements. Each element has a name and a type, and it sits in a structure, such as an attribute in a relation or a key in a foreign key. Optional inputs are instances of the schemas, dictionaries of synonyms and earlier matches.

**Output.** A *match*: a set of *correspondences* $(e_1, e_2, c)$ with $e_1 \in E_1$, $e_2 \in E_2$ and a confidence $c \in [0, 1]$. In the more general form a correspondence relates a set of elements to a set, as in "Name corresponds to First together with Last".

**Goal.** The correspondences that are semantically right, that is, that a domain expert would accept. This goal is not a function of the input, so the problem has no exact algorithm. A method is judged by measurement: its output is compared with a match made by hand, by precision (the share of the found correspondences that are right) and recall (the share of the right ones that are found).

Inside a method, the usual pipeline is formal. Each *matcher* computes a similarity matrix $\sigma : E_1 \times E_2 \to [0, 1]$. A *combination* step merges the matrices, and a *selection* step picks the correspondences from the merged matrix. The selection step alone is often an exact optimization problem; see Reductions.

## Variants

Rahm and Bernstein classify matchers along these lines.

- **Schema level or instance level.** A schema-level matcher uses only names, types, constraints and structure. An instance-level matcher uses the data, for example the overlap of the value sets.
- **Element or structure.** An element matcher compares two elements alone. A structure matcher compares the neighborhoods, as [similarity flooding](/similarity-flooding/) does.
- **Linguistic or constraint based.** A linguistic matcher compares names and text, with string similarity and dictionaries. A constraint matcher compares types, keys and value ranges.
- **Cardinality.** 1:1 correspondences, or 1:n and n:m, where one element matches a combination of several.
- **Single or combined.** A hybrid matcher uses several clues inside one algorithm. A composite matcher runs separate matchers and combines their results.

Other variants are matching many schemas at once, matching ontologies instead of database schemas, and the reuse of earlier matches.

## Examples

Schema 1 has Emp(Name: string, Dept: int), and schema 2 has Staff(FullName: varchar, Unit: integer). Take two matchers on the attributes.

- **Name matcher.** The similarity is $1 - d/\ell$, where $d$ is the [edit distance](/edit-distance/) of the lower-case names and $\ell$ is the length of the longer name.
- **Type matcher.** 1 if the two types are compatible (string with varchar, int with integer), else 0.

| pair | edit distance | name | type | average |
|---|---|---|---|---|
| Name, FullName | 4 | 0.5 | 1 | 0.75 |
| Name, Unit | 4 | 0 | 0 | 0 |
| Dept, FullName | 8 | 0 | 0 | 0 |
| Dept, Unit | 3 | 0.25 | 1 | 0.625 |

The name matcher alone gives Dept and Unit only 0.25, which a threshold of 0.5 would drop. The average of the two matchers keeps both right pairs. A 1:1 selection with the largest total similarity picks (Name, FullName) and (Dept, Unit), with total 1.375, against 0 for the other assignment. On the same schemas as graphs, similarity flooding finds the same pairs from seeds on the types and from the table structure, with no help from the names.

A harder case shows why matching is heuristic. If schema 2 also had a column ManagerName: varchar, the name and type matchers would rate (Name, ManagerName) almost as high as (Name, FullName). Only instance data or a person can tell them apart.

## Known algorithms

All of these are heuristics.

- **Name and text matchers.** [Edit distance](/edit-distance/), [Jaro-Winkler distance](/jaro-winkler-distance/), q-grams, token sets with [Jaccard similarity](/jaccard-similarity/), [tf-idf](/tf-idf/) with [cosine similarity](/cosine-similarity/), and synonym dictionaries.
- **Instance matchers.** The overlap of value sets, statistics of the values such as length and character classes, and classifiers trained on earlier matches.
- **Structure matchers.** [Similarity flooding](/similarity-flooding/), and methods that raise the similarity of two elements when their parents or children are similar.
- **Combination.** The weighted average, the maximum or the minimum of the matcher scores, with weights set by hand or learned.
- **Selection.** A threshold, the top $k$ partners of each element, a [stable matching](/stable-matching/), or a maximum-weight 1:1 match by the [Hungarian algorithm](/hungarian-algorithm/).

## Bounds

The full problem has no complexity bound, because its goal is not formal. Bounds exist for the formal steps.

- **Matchers.** A matcher that compares all pairs makes $|E_1| \cdot |E_2|$ comparisons. With edit distance on names of length at most $\ell$, this is $O(|E_1| |E_2| \ell^2)$ time.
- **1:1 selection.** A maximum-weight 1:1 match on an $n \times n$ matrix takes $O(n^3)$ time with the Hungarian algorithm (theorem). A stable matching takes $O(n^2)$ time with Gale-Shapley (theorem).
- **Exact structure matching.** If a match must keep the structure exactly, so that the graph of one schema maps edge for edge into the graph of the other, the problem contains [subgraph isomorphism](/subgraph-isomorphism/) and is NP-complete. This is one reason why structure matchers use similarity scores instead of exact embeddings.

## Reductions

- **Selection to assignment.** Choosing a 1:1 match with the largest total similarity is the [assignment problem](/assignment-problem/), a maximum-weight [bipartite matching](/bipartite-matching/).
- **From subgraph isomorphism.** A graph $H$ is a subgraph of a graph $G$ if and only if the schema graph of $H$ matches into that of $G$ under the exact structure rule. So that version is NP-hard.
- **Relation to entity resolution.** [Entity resolution](/entity-resolution/) matches records, schema matching matches the elements that describe them. Both use the same similarity functions and the same pipeline of comparison, combination and selection, and an instance matcher often runs entity resolution on samples of the data.

## Applications

- **Mapping design.** Correspondences are the first step of a [schema mapping](/schema-mapping/), for data exchange or for [GAV and LAV](/gav-and-lav/) integration.
- **Data warehouses.** Loading data from many operational systems into one warehouse needs the correspondences of each source with the warehouse schema.
- **Schema evolution and merging.** Matching an old and a new version of a schema, or two schemas that must become one.
- **Ontology alignment.** Matching the concepts of two ontologies uses the same kinds of matchers.

## References
