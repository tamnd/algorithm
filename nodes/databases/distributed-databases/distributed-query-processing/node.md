---
tag: E70YMS
kind: problem
slug: distributed-query-processing
name: Distributed query processing problem
aliases:
- distributed query optimization
area: databases/distributed-databases
level: core
summary: "Compute a query over relations stored at several sites while minimizing data shipped, response time or total cost."
prereqs: [query-optimization, semijoin, horizontal-fragmentation]
see_also: [sdd1-semijoin-optimization, bloom-join, yannakakis-algorithm, parallel-hash-join, join-ordering, data-allocation-problem, exchange-operator, hypercube-shares-join]
sources:
  - paper: doi:10.1145/371578.371598
    title: Donald Kossmann, The state of the art in distributed query processing, ACM Computing Surveys 32(4), 2000, pages 422 to 469
    locator: the survey of the architectures, the cost models and the techniques of distributed query processing
  - paper: doi:10.1145/319628.319650
    title: Philip A. Bernstein, Nathan Goodman, Eugene Wong, Christopher L. Reeve and James B. Rothnie Jr., Query processing in a system for distributed databases (SDD-1), ACM Transactions on Database Systems 6(4), 1981, pages 602 to 625
    locator: the cost model that counts only the data sent between sites, and Algorithm OPT, which builds a semijoin program and then sends the reduced relations to one site
  - paper: doi:10.1145/322234.322238
    title: Philip A. Bernstein and Dah-Ming W. Chiu, Using semi-joins to solve relational queries, Journal of the ACM 28(1), 1981, pages 25 to 40
    locator: tree queries and the semijoin programs that fully reduce them
  - paper: doi:10.1137/0210059
    title: Philip A. Bernstein and Nathan Goodman, Power of natural semijoins, SIAM Journal on Computing 10(4), 1981, pages 751 to 771
    locator: the power of semijoin programs on cyclic queries, which in general have no full reducer
  - book: isbn:9783030262525
    title: M. Tamer Özsu and Patrick Valduriez, Principles of Distributed Database Systems, fourth edition, Springer, 2020
    locator: Chapter 4, Distributed Query Processing (query decomposition, data localization, join ordering in distributed queries, and semijoin based algorithms)
---

The distributed query processing problem asks how to compute a query when its relations, or the fragments of its relations, are stored at different sites of a network. The answer does not depend on where the data is, but the cost does: a plan must also say at which site each operator runs and which data moves between sites. Moving data costs time and bandwidth, so the classic goal is to ship as little data as possible; other cost models count the total work of all sites, or the response time when the sites work in parallel. The problem contains centralized [query optimization](/query-optimization/), and so it is NP-hard in general. The main tools are the rewriting of a query on the fragments, the choice of join order and join site, and [semijoins](/semijoin/) that reduce a relation before it is sent.

## In plain words

A question asks about tables that are kept in different cities. To answer it, some data must travel from one city to another, and travel is slow and costly. The same answer can be found in many ways. You can send a whole table to the city of another table and combine them there. Or you can first send only a short list of the values that matter, so that the other city sends back only the rows that match. You can also skip the pieces of a table that cannot hold an answer at all. The problem is to choose the way that sends the least data, or that does the least total work, or that gives the answer the soonest. There are very many ways, so systems use good rules and estimates, not a full search.

## Definition

**Input.**

- A query $Q$ over global relations, for example a select, project and join query in [relational algebra](/relational-algebra/).
- A fragmentation of each global relation, [horizontal](/horizontal-fragmentation/), [vertical](/vertical-fragmentation/) or both, and an allocation of the fragments and their copies to sites, as on the page of the [data allocation problem](/data-allocation-problem/).
- The site where the result is needed.
- Statistics for a [cost model](/cost-model/): sizes, [selectivities](/selectivity/) and the costs of local work and of messages.

**Output.** A distributed plan: a tree of operators on fragments, each operator at a site, with a transfer operator for each edge between two sites. The plan must compute $Q$ on every database that matches the fragmentation, with bag semantics, and must deliver the result to the result site.

**Cost.** One of the following, with estimates from [cardinality estimation](/cardinality-estimation/).

- *Communication cost.* The number of bytes, or the number of messages and bytes, sent between sites. This is the model of SDD-1, which was built for slow wide area networks.
- *Total cost.* The sum of the local processor and disk work at all sites and the communication cost.
- *Response time.* The time from the start of the query to the last row of the result, where work at different sites can overlap.

The goal is a plan of least estimated cost. Most systems split the work into four steps: *decomposition* rewrites the query in algebra on the global relations, *localization* replaces each global relation by its fragments and removes the fragments that cannot contribute, *global optimization* chooses the join order, the sites and the transfers, and *local optimization* chooses the plan at each site.

## Variants

- **Wide area or local network.** On a slow network, communication dominates and the cost counts only shipped data. On a fast network, local work matters as much, and the total cost or the response time is used.
- **Data shipping, query shipping or hybrid shipping.** The plan can bring the data to the site of the query, send the query to the data, or mix the two, as Kossmann (2000) surveys.
- **Parallel query processing.** In a [shared-nothing](/shared-nothing-architecture/) parallel system, all sites are in one cluster and the goal is the response time. Plans repartition the data with [exchange operators](/exchange-operator/) and run joins such as the [parallel hash join](/parallel-hash-join/) on all nodes at once.
- **One round of communication.** In massively parallel models, the goal is the largest amount of data that any one server receives. The [hypercube shares join](/hypercube-shares-join/) computes a multiway join in one round.
- **Autonomous sites.** In a federation of independent databases, the optimizer has few statistics and the sites can refuse some plans, so plans adapt during execution.

## Examples

**Localization.** The relation $ACCOUNT$ is fragmented by branch into $A_{Paris}$ at site 1, $A_{Lyon}$ at site 2 and $A_{Other}$ at site 3. The query $\sigma_{branch = Lyon}(ACCOUNT)$ becomes $\sigma_{branch = Lyon}(A_{Paris} \cup A_{Lyon} \cup A_{Other})$. The predicates of $A_{Paris}$ and $A_{Other}$ contradict $branch = Lyon$, so localization reduces the query to $\sigma_{branch = Lyon}(A_{Lyon})$, which runs at site 2 alone.

**Shipping a relation or a semijoin.** The query is $R \bowtie_B S$, with the result needed at site 2. The relation $R(A, B)$ is at site 1, with 1000 rows of 20 bytes each. The relation $S(B, C)$ is at site 2, and its column $B$ has 50 distinct values of 4 bytes each. Assume that 100 rows of $R$ have a $B$ value that occurs in $S$.

| plan | data shipped |
|---|---|
| send $R$ to site 2 and join there | $1000 \cdot 20 = 20000$ bytes |
| send $\pi_B(S)$ to site 1, compute $R \ltimes S$, send it to site 2 and join | $50 \cdot 4 + 100 \cdot 20 = 2200$ bytes |

The semijoin plan ships about a ninth of the data. If 900 rows of $R$ matched, the semijoin plan would ship $200 + 18000 = 18200$ bytes, and its saving would be small. Algorithms such as [SDD-1](/sdd1-semijoin-optimization/) estimate this benefit for each semijoin and use a semijoin only when the benefit is larger than its cost. A [Bloom join](/bloom-join/) sends a [Bloom filter](/bloom-filter/) in place of $\pi_B(S)$, which is smaller but lets some extra rows through.

**A cyclic query that semijoins cannot reduce.** Let $R(A, B) = \{(0, 0), (1, 1)\}$, $S(B, C) = \{(0, 0), (1, 1)\}$ and $T(C, A) = \{(0, 1), (1, 0)\}$. Each pair of relations shares one attribute, and on it both relations have the values $\{0, 1\}$, so every semijoin keeps every row. But $R \bowtie S \bowtie T$ is empty: $R$ and $S$ give rows with $A = B = C$, and $T$ has no row with $C = A$. So a semijoin program must send all six rows, although the result is empty.

## Known algorithms

- **Semijoin programs.** SDD-1 (Bernstein, Goodman, Wong, Reeve and Rothnie 1981) adds the semijoin with the largest estimated benefit while the benefit is larger than the cost, and then sends the reduced relations to the site that holds the most data. It is a [hill climbing](/hill-climbing/) heuristic.
- **Full reducers for tree queries.** For a tree query, an acyclic query in the sense of [acyclic hypergraphs](/acyclic-hypergraph/), two passes of semijoins over a join tree remove every row that is not in the result. The [Yannakakis algorithm](/yannakakis-algorithm/) adds a join pass and computes the query in time linear in the input and the output.
- **Join ordering with sites.** The dynamic programming of centralized [join ordering](/join-ordering/) extends to plans in which each join also has a site and each input is shipped whole or row by row. The search space is larger, so large queries use greedy or randomized search.
- **Bloom joins.** A [Bloom join](/bloom-join/) is a semijoin with a compact, lossy filter; it costs less to send, and the false positives are removed by the final join.
- **Repartitioning joins.** In parallel and cluster systems, both inputs are hashed on the join key and sent to the nodes, as in the [parallel hash join](/parallel-hash-join/) and the [reduce-side join](/reduce-side-join/); a small input is sent to all nodes instead, as in the [map-side join](/map-side-join/).

## Bounds

**Theorem (NP-hard).** Distributed query optimization with the total cost is NP-hard. *Proof.* With one site, the communication cost is zero, and the problem is centralized join ordering, which is NP-hard by the results on [join ordering NP-hardness](/join-ordering-np-hardness/). $\square$

**Theorem (full reducers).** A query has a full reducer, a semijoin program that removes every row that is not in the result on every database, if and only if it is a tree query. Bernstein and Chiu (1981) gave the full reducers for tree queries, and Bernstein and Goodman (1981) showed that cyclic queries have none. The triangle example above shows the cyclic case.

**Optimality of the heuristics.** SDD-1 and the other greedy semijoin methods do not find the cheapest plan in general; Bernstein et al. (1981) say that the result of Algorithm OPT is, in general, suboptimal. Their quality is a measurement, and it depends on the accuracy of the size estimates.

## Reductions

**From centralized query optimization.** The one-site case is the centralized problem, as in the proof above. So every hardness result for [join ordering](/join-ordering/) also holds here.

**To queries on fragments.** A horizontally fragmented relation is the bag union of its fragments, and joins and selections distribute over bag unions: $(R_1 \cup R_2) \bowtie S = (R_1 \bowtie S) \cup (R_2 \bowtie S)$. A vertically fragmented relation is the join of its fragments on the key. Localization uses these rules to turn a query on global relations into a query on fragments, and then removes the terms that are empty by their predicates.

**To acyclic join evaluation.** For a tree query, the semijoin passes of a full reducer leave relations that join without empty intermediate rows, so the problem of what to ship reduces to [acyclic join evaluation](/acyclic-join-evaluation/) at the result site.

## Applications

- **Distributed database systems.** SDD-1 and later distributed systems optimize queries over fragments stored at several sites, and the textbook of Özsu and Valduriez organizes the problem in the four steps above.
- **Parallel databases and cloud data warehouses.** Shared-nothing systems plan repartitioning and broadcast joins on clusters to cut the response time.
- **Big data systems.** Joins in [MapReduce](/mapreduce-model/) and its successors are distributed joins with a cost that counts the data shuffled between machines.
- **Federated and mediator systems.** Queries over independent sources send subqueries to the sources and combine the answers.

## References
