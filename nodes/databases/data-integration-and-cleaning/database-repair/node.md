---
tag: HJP9DJ
kind: problem
slug: database-repair
name: Database repair
aliases:
- minimum-cost repair
- constraint-based data repair
area: databases/data-integration-and-cleaning
level: advanced
summary: "Change a database that violates integrity constraints so that it satisfies them, by deletions, insertions or value updates that are minimal under a chosen measure of change."
prereqs: [functional-dependency, denial-constraint, vertex-cover, np-hard]
see_also: [consistent-query-answering, denial-constraint, conditional-functional-dependency, holoclean, maximum-independent-set, hitting-set, apx, functional-dependency-discovery]
sources:
  - paper: doi:10.1145/303976.303983
    title: "Marcelo Arenas, Leopoldo Bertossi and Jan Chomicki, Consistent query answers in inconsistent databases, PODS 1999"
    locator: "pages 68-79, repairs as consistent databases at a minimal distance from the given one"
  - paper: doi:10.1016/j.ic.2004.04.007
    title: "Jan Chomicki and Jerzy Marcinkowski, Minimal-change integrity maintenance using tuple deletions, Information and Computation 197(1-2), 2005"
    locator: "pages 90-121, repairs by deletions, the conflict hypergraph and repair checking"
  - paper: doi:10.1145/3196959.3196980
    title: "Ester Livshits, Benny Kimelfeld and Sudeepa Roy, Computing optimal repairs for functional dependencies, PODS 2018"
    locator: "pages 225-237, the dichotomy for optimal subset repairs under functional dependencies"
  - paper: doi:10.1145/3360904
    title: "Ester Livshits, Benny Kimelfeld and Sudeepa Roy, Computing optimal repairs for functional dependencies, ACM TODS 45(1), 2020"
    locator: "the journal version of the dichotomy and the simplification procedure"
  - paper: doi:10.1109/icde.2013.6544847
    title: "Xu Chu, Ihab F. Ilyas and Paolo Papotti, Holistic data cleaning: putting violations into context, ICDE 2013"
    locator: "pages 458-469, repair by value updates under denial constraints"
  - book: isbn:9783031007552
    title: "Leopoldo Bertossi, Database Repairing and Consistent Query Answering, Morgan and Claypool, 2011"
    locator: "the chapters on repair semantics"
---

Database repair asks for a consistent database that is as close as possible to a given database that violates its constraints. It differs from [consistent query answering](/consistent-query-answering/): there the repairs are only a way to define which answers are safe, and no repair is chosen, while here the output is one repaired database that later queries run on. The problem has many versions, one for each kind of change allowed and each way to measure the change. This page treats deletions of facts in detail and value updates more briefly.

## In plain words

A table breaks a rule, such as "each person has one department". You want to fix the table so that it follows the rule, and you want to change as little as you can, since most of the data is probably right.

There are several ways to fix it. You can delete rows until no rule is broken. You can delete as few rows as possible, or rows that you trust less. Or you can change single values in place, such as a misspelled department name. Each choice gives a different idea of the best fix, and some of them are easy to compute while others are as hard as the hardest search problems.

## Definition

Let $D$ be a finite database and $\Sigma$ a set of constraints. Set semantics holds. A *repair* is a database $D'$ that satisfies $\Sigma$ and is minimal for some measure of change. The main kinds are these.

- **Subset repair.** $D' \subseteq D$ is consistent and no consistent $D''$ has $D' \subsetneq D'' \subseteq D$. These are the repairs of Arenas, Bertossi and Chomicki when only deletions are needed, which is the case for [denial constraints](/denial-constraint/).
- **Cardinality repair.** $D' \subseteq D$ is consistent and has the largest number of facts among consistent subsets. With a weight $w(f) > 0$ for each fact, an *optimal subset repair* has the largest total weight.
- **Symmetric-difference repair.** For constraints that ask for facts to exist, such as inclusion dependencies, $D'$ may add facts, and $D \mathbin{\triangle} D'$ is minimal under inclusion.
- **Update repair.** $D'$ has the same facts as $D$ with some cell values changed. The measure is the number of changed cells, or a sum of costs per cell.

The computational questions are:

- **Repair checking.** Given $D$ and $D'$, is $D'$ a repair of $D$?
- **Finding.** Compute one repair, or an optimal one.
- **Counting and enumeration.** Count or list all repairs.

The constraints are fixed, so the complexity is data complexity unless stated.

**The conflict graph.** For functional dependencies, the facts are the vertices and an edge joins two facts that violate a dependency together. A subset of $D$ is consistent if and only if it is an independent set. So the subset repairs are the maximal independent sets, and the cardinality repairs are the [maximum independent sets](/maximum-independent-set/), the complements of the minimum [vertex covers](/vertex-cover/). For denial constraints with more than two tuple variables, the conflicts are hyperedges and the deleted facts form a [hitting set](/hitting-set/).

## Variants

- **The constraints.** Functional dependencies, keys, [conditional functional dependencies](/conditional-functional-dependency/), denial constraints, or inclusion dependencies.
- **The kind of change.** Deletions, insertions, updates of values, or a mix.
- **The measure.** Minimal under inclusion, smallest number, smallest total weight, or a cost per changed cell that depends on how far the new value is from the old one.
- **Priorities.** A preference among conflicting facts, for example the newer fact wins, which narrows the set of repairs.
- **Statistical repair.** Choose the most likely values under a model learned from the data, as [HoloClean](/holoclean/) does. This drops the exact notion of minimality.

## Examples

The table Emp has the attributes name, dept and phone, and the functional dependency name $\to$ dept.

| row | name | dept | phone |
|---|---|---|---|
| 0 | ann | sales | 1 |
| 1 | ann | sales | 2 |
| 2 | ann | hr | 3 |
| 3 | bob | it | 4 |

- **Subset repairs.** Row 2 conflicts with rows 0 and 1. There are two subset repairs: rows {0, 1, 3} and rows {2, 3}. Both are maximal: adding any deleted row brings back a conflict.
- **Cardinality repair.** Rows {0, 1, 3}, with one deletion. The subset repair {2, 3} needs two.
- **Weighted repair.** If row 2 comes from a trusted source with weight 3 and the others have weight 1, the optimal subset repair is {2, 3}, with weight 4 against 3.
- **Update repairs.** Changing the dept of row 2 to sales fixes the table with one changed cell. So does changing the name of row 2 to a new value. The second fix is cheap by count but probably wrong, which is why update repairs often fix which attributes may change or give each change a cost.

## Known algorithms

- **One subset repair.** Start from the empty set and add the facts of $D$ one at a time, keeping a fact when the set stays consistent. Under denial constraints the result is a subset repair: a fact skipped at some step conflicts with facts already kept, and those stay. The time is polynomial for fixed constraints.
- **Repair checking for subset repairs.** Under denial constraints, $D'$ is a subset repair if and only if it is consistent and $D' \cup \{f\}$ is inconsistent for each $f \in D \setminus D'$. A larger consistent superset would make $D' \cup \{f\}$ consistent for each of its new facts, since deleting facts keeps denial constraints. Both checks take polynomial time.
- **One functional dependency.** For $X \to Y$, the groups of facts with the same $X$ value are independent. Within a group, a consistent subset uses one $Y$ value. So the optimal subset repair keeps, in each group, the $Y$ value with the largest total weight, in $O(|D|)$ time with hashing.
- **Two dependencies $A \to B$ and $B \to A$.** A consistent subset pairs each $A$ value with at most one $B$ value and back. Give the edge $(a, b)$ of a bipartite graph the total weight of the facts with $A = a$ and $B = b$. The optimal subset repairs are the maximum weight matchings, found in polynomial time.
- **Approximation.** For functional dependencies, delete a vertex cover of the conflict graph found by the matching method: take both ends of each edge of a maximal matching. This gives a consistent subset with at most twice the smallest number of deletions. With $k$ tuple variables per constraint, the same method on hyperedges gives a factor $k$.
- **Update repairs.** Holistic data cleaning by Chu, Ilyas and Papotti chooses value changes for all violations of a set of denial constraints together. It is a heuristic, with no guarantee of the smallest change.

## Bounds

All bounds are theorems in data complexity.

- **Repair checking.** Polynomial for subset repairs under denial constraints, as shown above.
- **Number of repairs.** Under one key, a database with $s$ blocks of 2 facts each has $2^s$ subset repairs, so listing them all takes exponential time.
- **Optimal subset repairs under functional dependencies.** For each fixed set of functional dependencies, computing an optimal subset repair is either in polynomial time or APX-complete, and a simplification procedure on the dependencies decides which (Livshits, Kimelfeld and Roy). The two easy cases above are instances of the polynomial side. In the [APX](/apx/)-complete cases, the factor 2 of the vertex cover method holds, but no polynomial-time approximation scheme exists unless P = NP.
- **Cardinality repairs in general.** Every cardinality repair problem under functional dependencies is a minimum vertex cover problem on the conflict graph, so it is in NP as a decision problem for any fixed set.

## Reductions

- **To vertex cover and hitting set.** A cardinality repair under functional dependencies is the complement of a minimum vertex cover of the conflict graph. Under denial constraints with $k$ tuple variables, it is the complement of a minimum hitting set of a hypergraph with edges of size at most $k$.
- **Hardness.** For the hard sets of dependencies, Livshits, Kimelfeld and Roy prove APX-hardness by reductions from known APX-hard problems to the optimal subset repair.
- **To consistent query answering.** The set of subset repairs is the set of possible worlds over which consistent query answering takes the intersection of the answers.

## Applications

- **Data cleaning.** Repair a table before analysis, either by deleting the facts in conflict or by changing values. Systems in this line include holistic data cleaning and HoloClean.
- **Data integration.** Merging sources that disagree on a key gives a table with conflicts, which a repair resolves.
- **Error reports.** The conflict graph and a small vertex cover point a person to the few facts most likely to be wrong.
- **Constraint maintenance.** After a load that breaks a constraint, a repair restores it with few changes.

## References
