---
tag: 0XB7XD
kind: definition
slug: self-maintainable-view
name: Self-maintainable view
aliases:
- self-maintainability
area: databases/stream-and-incremental-processing
level: advanced
summary: "A materialized view that can be updated from its old contents and the base changes alone, without reading the base relations."
prereqs: [materialized-view, incremental-view-maintenance]
see_also: [delta-rules, deferred-view-maintenance, incremental-view-maintenance, view-maintenance, materialized-view, view-selection, functional-dependency, inclusion-dependency]
sources:
  - paper: "Ashish Gupta, H. V. Jagadish and Inderpal Singh Mumick, Data integration using self-maintainable views, Proceedings of EDBT 1996, Lecture Notes in Computer Science 1057"
    title: Data integration using self-maintainable views
    locator: "the definition of a view that is self-maintainable for a kind of change, and the conditions for select-project-join views (general locator, pages not checked)"
  - paper: doi:10.1109/PDIS.1996.568677
    title: "Dallan Quass, Ashish Gupta, Inderpal Singh Mumick and Jennifer Widom, Making views self-maintainable for data warehousing, Proceedings of PDIS 1996, pages 158 to 169"
    locator: "the auxiliary views that make a view and its helpers self-maintainable together, and the use of keys and referential integrity to make the auxiliary views small"
  - paper: "José A. Blakeley, Neil Coburn and Per-Åke Larson, Updating derived relations, detecting irrelevant and autonomously computable updates, ACM Transactions on Database Systems 14(3), 1989, 369 to 400"
    title: "Updating derived relations, detecting irrelevant and autonomously computable updates"
    locator: the updates that can be applied to a derived relation from its contents and the update alone (general locator)
  - paper: "Ashish Gupta and Inderpal Singh Mumick, Maintenance of materialized views, problems, techniques, and applications, IEEE Data Engineering Bulletin 18(2) (1995), 3 to 18"
    title: "Maintenance of materialized views, problems, techniques, and applications"
    locator: "the classification of maintenance problems by the information that is available, with the view and the change alone as the smallest case"
---

A *self-maintainable view* is a [materialized view](/materialized-view/) whose new contents after a change to the base relations are a function of its old contents and the change, so that maintenance never reads the base relations. It is a property of the view definition together with a kind of change (insertions, deletions or both) and the integrity constraints, not of an algorithm. [Delta rules](/delta-rules/) give the change of any view but usually read the old base relations, and [deferred view maintenance](/deferred-view-maintenance/) asks a related question about when the base relations are read.

## Definition

Let $\mathcal{L}$ be the set of legal databases (those that satisfy the constraints), and let $\mathcal{C}$ be a class of changes, for example the insertions into relation $R$. Write $D + \Delta$ for the database after the change $\Delta$. A view $V$ is *self-maintainable for $\mathcal{C}$* if, for all $D_1, D_2 \in \mathcal{L}$ and every $\Delta \in \mathcal{C}$ such that $D_1 + \Delta$ and $D_2 + \Delta$ are legal,

$$V(D_1) = V(D_2) \implies V(D_1 + \Delta) = V(D_2 + \Delta).$$

Equivalently, there is a function $F$ with $V(D + \Delta) = F(V(D), \Delta)$ for every legal $D$ and every applicable $\Delta \in \mathcal{C}$. The first form is the one that refutes self-maintainability: two databases with the same view and the same change that give different new views are a proof that no $F$ exists.

A set of views $\{V, A_1, \ldots, A_k\}$ is self-maintainable if the tuple of all their contents is: each new view is a function of the old contents of all of them and the change. The $A_i$ are *auxiliary views*. Their base case is the set of all base relations, which is always self-maintainable; the aim is to choose auxiliary views that are much smaller.

The answer depends on three choices: the class of changes, the semantics (sets or bags), and the constraints in $\mathcal{L}$. Keys and foreign keys, written as a [functional dependency](/functional-dependency/) and an [inclusion dependency](/inclusion-dependency/), make $\mathcal{L}$ smaller, so fewer pairs $D_1, D_2$ must agree and more views qualify.

## Examples and non-examples

$R(A, B)$ and $S(B, C)$ are base relations. Each "no" row gives a pair of databases that refutes the property.

| view | change | semantics | self-maintainable | reason or counterexample |
|---|---|---|---|---|
| $\sigma_{A > 0}(R)$ | insert or delete in $R$ | sets or bags | yes | $\Delta V = \sigma_{A > 0}(\Delta R)$ |
| $\pi_A(R)$ | insert in $R$ | sets | yes | add $\pi_A(\Delta R)$ |
| $\pi_A(R)$ | delete in $R$ | sets | no | $R_1 = \{(1, 1), (1, 2)\}$ and $R_2 = \{(1, 1)\}$ both give $\{1\}$; deleting $(1, 1)$ gives $\{1\}$ and $\emptyset$ |
| $\pi_A(R)$ | insert or delete in $R$ | bags | yes | the counts of the view are the counts of derivations, and $\Delta V = \pi_A(\Delta R)$ |
| $R \bowtie S$ | insert in $R$ | sets or bags | no | $R = \emptyset$ with $S = \{(10, x)\}$ or $S = \emptyset$ gives the empty view; inserting $(1, 10)$ gives one tuple or none |
| $R \bowtie S$ | delete in $R$ | sets | yes | remove the view tuples whose $A, B$ part is the deleted tuple |
| $R \bowtie S$ | delete in $R$ | bags | no | $R = \{(1, 10)\}, S = \{(10, x), (10, x)\}$ and $R = \{(1, 10), (1, 10)\}, S = \{(10, x)\}$ both give $(1, 10, x)$ twice; deleting one $(1, 10)$ gives 0 copies and 1 copy |
| $R \bowtie S$, with $B$ a key of $S$ and $R.B$ a foreign key to $S$ | insert in $S$ | sets or bags | yes | a new tuple of $S$ has a new key, which no tuple of $R$ references, so $\Delta V = \emptyset$ |
| $\gamma_{G;\, \mathrm{MAX}(X)}(R)$ | insert in $R$ | bags | yes | the new maximum is the larger of the old one and the inserted value |
| $\gamma_{G;\, \mathrm{MAX}(X)}(R)$ | delete in $R$ | bags | no | groups $\{5, 3\}$ and $\{5\}$ both give 5; deleting 5 gives 3 and no group |
| $\gamma_{G;\, \mathrm{SUM}(X)}(R)$ | delete in $R$ | bags | no | groups $\{2, 0\}$ and $\{2\}$ both give 2; deleting 2 gives 0 and no group |
| $\gamma_{G;\, \mathrm{SUM}(X), \mathrm{COUNT}(*)}(R)$ | insert or delete in $R$ | bags | yes | both are sums over the group, and a count of 0 says the group is gone |

**The join and auxiliary views.** $R \bowtie S$ is not self-maintainable for insertions into $R$, because the inserted tuple must meet tuples of $S$ that the view may not show. Under set semantics, the set $\{R \bowtie S, A\}$ with the auxiliary view $A = S$ is self-maintainable for insertions and deletions in $R$ and for deletions from $S$, at the cost of storing $A$. It is still not self-maintainable for insertions into $S$: a tuple of $R$ with no match is in neither view, and a new tuple of $S$ can match it. Quass, Gupta, Mumick and Widom derive such auxiliary views from the view definition, push the selections of the view into them, and use keys and referential integrity to drop the auxiliary views that the constraints make unnecessary, as in the foreign key row of the table.

**Bags change the answer.** The set projection fails for deletions and the bag projection does not, because the bag view holds the count that the set view lost. The bag join fails for deletions and the set join does not, because in a bag the count of a view tuple is a product of two base counts that the view cannot split.

## Related definitions

- [Delta rules](/delta-rules/) give $\Delta V$ for any view. A view is self-maintainable for a class of changes when its delta rules can be rewritten to read only $V$ and $\Delta$.
- [Incremental view maintenance](/incremental-view-maintenance/) is the algorithm that applies the delta. In a data warehouse the base relations are at remote sources, and a self-maintainable view, with its auxiliary views, can be maintained without queries to the sources.
- [Deferred view maintenance](/deferred-view-maintenance/) keeps logs of the base changes and refreshes later. A self-maintainable view needs only the logs, not the current base state.
- [View selection](/view-selection/) chooses which views to materialize. The auxiliary views of a self-maintainable set are a choice of this kind, with maintenance cost in place of query cost.
- In a stream system, a view that is self-maintainable for insertions can take a late tuple at any time, because the change needs no old base data. A view that is not must keep the base data, or a summary of it, for as long as late data can arrive.
- An *autonomously computable update*, in the sense of Blakeley, Coburn and Larson, is the same idea for one given update and one given view contents, not for all databases.

## References
