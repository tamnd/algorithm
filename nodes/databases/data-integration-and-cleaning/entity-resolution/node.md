---
tag: M02NHQ
kind: problem
slug: entity-resolution
name: Entity resolution
aliases:
- record linkage
- duplicate record detection
- merge-purge problem
area: databases/data-integration-and-cleaning
level: core
summary: "Find the records in one or more data sets that refer to the same real-world entity, and link or merge them. Exact methods compare all pairs; blocking and windows make it fast."
model: word-ram
complexity:
  vars: {n: the number of records}
  time: {worst: "O(n^2)"}
prereqs: [transitive-closure, connected-components]
see_also: [fellegi-sunter-model, entity-resolution-blocking, sorted-neighborhood-method, r-swoosh, collective-entity-resolution, correlation-clustering, truth-discovery, assignment-problem]
sources:
  - paper: doi:10.1080/01621459.1969.10501049
    title: "Ivan P. Fellegi and Alan B. Sunter, A theory for record linkage, Journal of the American Statistical Association 64(328), 1969, pages 1183 to 1210"
    locator: the statement of record linkage between two files as a decision on each pair of records (link, possible link or non-link), and the optimal rule
  - paper: "Howard B. Newcombe, James M. Kennedy, S. J. Axford and A. P. James, Automatic linkage of vital records, Science 130(3381), 1959, pages 954 to 959"
    locator: the early computer linkage of birth and marriage records with weights from the frequencies of agreement
  - paper: doi:10.1007/s00778-008-0098-x
    title: "Omar Benjelloun, Hector Garcia-Molina, David Menestrina, Qi Su, Steven Euijong Whang and Jennifer Widom, Swoosh: a generic approach to entity resolution, The VLDB Journal 18(1), 2009, pages 255 to 276"
    locator: the generic model with black-box match and merge functions and the definition of the result ER(I)
  - paper: "Ahmed K. Elmagarmid, Panagiotis G. Ipeirotis and Vassilios S. Verykios, Duplicate record detection: a survey, IEEE Transactions on Knowledge and Data Engineering 19(1), 2007, pages 1 to 16"
    locator: the survey of field comparison measures, probabilistic and rule-based matching, and methods to cut the number of comparisons
  - book: isbn:9783642311635
    title: "Peter Christen, Data Matching: Concepts and Techniques for Record Linkage, Entity Resolution, and Duplicate Detection, Springer, 2012"
    locator: the process of data matching (cleaning, indexing, comparison, classification, evaluation) and the measures of quality
---

Entity resolution (ER) is the problem of finding which records refer to the same real-world entity, such as one person, one company or one product, when the records have no shared identifier and their values differ by typos, abbreviations and missing fields. The output is a partition of the records into clusters, one for each entity, or a set of links between two files. This page states the problem and its parts. The pages for the methods each solve one part: [blocking](/entity-resolution-blocking/) and the [sorted neighborhood method](/sorted-neighborhood-method/) choose which pairs to compare, the [Fellegi-Sunter model](/fellegi-sunter-model/) decides each pair from field agreements, [R-Swoosh](/r-swoosh/) merges records with black-box rules, and [collective entity resolution](/collective-entity-resolution/) uses the links between records. ER decides which records describe one entity. [Truth discovery](/truth-discovery/) comes after it and decides which of their conflicting values is true.

## In plain words

You have two customer lists, or one list with many copies of the same people. Nobody wrote down a customer number, and the same person appears as "Jon Smith, 12 Main St" and "John Smith, 12 Main Street". You want to know which rows are the same person. You can compare two rows and say "probably the same" or "probably not", but comparing every row with every other row takes too long when there are millions. So the work has steps: pick the pairs worth comparing, compare them, decide, and then group the rows so that the groups make sense together.

## Definition

**Input.** A set $D$ of $n$ records, or two sets $A$ and $B$. Each record has attribute values, and there is a hidden map $e$ from records to entities.

**Output.** A partition of $D$ into clusters, with the aim that two records are in one cluster if and only if $e$ maps them to the same entity. For two files the output is a set of pairs in $A \times B$ (the *links*).

**What a method has.** No method sees $e$. It has a pairwise rule, given or learned: a function $\mathit{match}(r, s)$ that returns yes or no, or a score $\mathit{sim}(r, s)$. Under the *pairwise* reading, the output is the [connected components](/connected-components/) of the graph of matching pairs, that is, the [transitive closure](/transitive-closure/) of the rule. Under the *merge* reading of Benjelloun et al., matching records are merged and the merged records are compared again.

**Quality.** With labels for a sample, *pairwise precision* is the fraction of the pairs in found clusters that are true pairs, and *pairwise recall* is the fraction of true pairs that are in found clusters. Their harmonic mean is the F1 score. Cluster-level measures also exist. All of these are measurements on a given data set.

## Variants

- **Deduplication.** One file, find the clusters (the merge/purge problem).
- **Record linkage.** Two files, each with at most one record for each entity, so the links are a one-to-one matching.
- **Reference disambiguation.** Many short references, such as author names in a bibliography, that must be mapped to entities through their context.
- **Online or incremental ER.** New records arrive and must be added to the clusters without starting again.
- **Schema heterogeneity.** The sources have different schemas, so [schema matching](/schema-matching/) must come first.

## Examples

Five records (name, city, birth year):

| record | name | city | year |
|---|---|---|---|
| r1 | Jon Smith | Boston | 1970 |
| r2 | John Smith | Boston | 1970 |
| r3 | J. Smith | Boston | |
| r4 | John Smith | Denver | 1985 |
| r5 | Ann Lee | Boston | 1970 |

The true clusters are {r1, r2, r3}, {r4} and {r5}. A rule "same city and name edit distance at most 1" matches only r1 and r2. A rule "same city and same last name" also brings r3, the right cluster. A rule "same name" puts r2 and r4 together, a false match. Each rule is a heuristic, and the choice of the rule decides the result more than the algorithm does.

## Known algorithms

- **All pairs and closure.** Call the rule on all $n(n-1)/2$ pairs and take the components with [union-find](/weighted-union-find/). This is the reference result that the fast methods approximate.
- **Pair selection.** [Blocking](/entity-resolution-blocking/) compares only records with the same key. The [sorted neighborhood method](/sorted-neighborhood-method/) compares records that are near in a sorted order. [Canopy clustering](/canopy-clustering/), [MinHash](/minhash/) with [locality-sensitive hashing](/locality-sensitive-hashing/), and [set similarity joins](/set-similarity-join/) find the pairs above a similarity threshold. These are heuristics for recall.
- **Pair decision.** The [Fellegi-Sunter model](/fellegi-sunter-model/) scores each pair by a likelihood ratio of field agreements, with weights fitted by [expectation maximization](/expectation-maximization/) when there are no labels. Learned classifiers such as [logistic regression](/logistic-regression/) use labelled pairs. Field comparisons use [edit distance](/edit-distance/), [Jaro-Winkler](/jaro-winkler-distance/) and [Soundex](/soundex/).
- **Merging.** [R-Swoosh](/r-swoosh/) merges matching records and compares the merged results. Under the ICAR properties it returns the exact result of the merge model.
- **Clustering.** When the pairwise scores are not transitive, [correlation clustering](/correlation-clustering/) or [agglomerative clustering](/agglomerative-clustering/) gives a consistent partition. [Collective entity resolution](/collective-entity-resolution/) adds the links between records.

## Bounds

**Black-box rules need all pairs.** *Theorem.* Any deterministic method that returns the components of the match graph exactly, and that only calls a black-box $\mathit{match}$, makes $n(n-1)/2$ calls in the worst case. *Proof.* Answer "no" to every call. If some pair $\{a, b\}$ is never asked, the answers are the same for the rule that matches no pair and the rule that matches only $a$ and $b$, but the correct outputs differ. So every pair must be asked. This is why every fast method uses something about the records, such as keys or similarity, and why its recall is a measurement, not a guarantee.

**Output size.** The output is one of the set partitions of $n$ records, whose number grows faster than any exponential $c^n$. The problem is to find the right one, not to list them.

**Clustering with inconsistent scores.** Finding the partition that disagrees with the fewest pairwise decisions is the correlation clustering problem, which is NP-hard.

## Reductions

- **To connected components.** With a yes-or-no rule that is taken as transitive, ER is the components of the graph of matching pairs.
- **To matching.** For two files with one record for each entity on each side, the links with the largest total score form a maximum weight matching, an instance of the [assignment problem](/assignment-problem/).
- **To correlation clustering.** With scores that are positive for "same" and negative for "different", the best partition is a correlation clustering of the complete signed graph.
- **To classification.** The pair decision alone is a binary classification of pairs, with the classes very unbalanced: most pairs are not matches.

## Applications

- **Census and health data.** Linking birth, death and hospital records for statistics, where the record linkage methods began.
- **Customer data.** Joining customer lists after a merger, and cleaning mailing lists.
- **Bibliographies and knowledge bases.** Finding which author names and which citations are the same.
- **Product catalogues.** Joining offers for the same product from many shops, as the input to [truth discovery](/truth-discovery/) on their values.

## References
