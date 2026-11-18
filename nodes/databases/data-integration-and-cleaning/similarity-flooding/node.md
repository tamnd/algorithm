---
tag: BY6RCV
kind: algorithm
slug: similarity-flooding
name: Similarity flooding
aliases:
- Melnik similarity flooding
area: databases/data-integration-and-cleaning
level: advanced
summary: "Match two schema graphs by propagating initial similarities of nodes to their neighbors until a fixpoint, then filtering the pairs."
solves: [schema-matching]
model: word-ram
complexity:
  vars: {v: the number of map pairs, e: the number of edges of the pairwise connectivity graph, s: the number of fixpoint steps}
  time: {worst: O(s(v + e) + v log v)}
  space: {extra: O(v + e)}
properties: {deterministic: true, exact: false, online: false, in_place: false, recursive: false}
history:
  year: 2002
  people: [Sergey Melnik, Hector Garcia-Molina, Erhard Rahm]
  note: "Melnik, Garcia-Molina and Rahm presented similarity flooding at ICDE 2002 as a generic graph matcher for schema matching."
prereqs: [schema-matching, fixed-point-iteration, power-iteration, gale-shapley]
see_also: [perron-frobenius-theorem, pagerank, stable-matching, assignment-problem, hungarian-algorithm, schema-mapping, edit-distance]
sources:
  - paper: doi:10.1109/ICDE.2002.994702
    title: "Sergey Melnik, Hector Garcia-Molina and Erhard Rahm, Similarity flooding: a versatile graph matching algorithm and its application to schema matching, ICDE 2002"
    locator: pages 117-128
  - paper: doi:10.1007/s007780100057
    title: "Erhard Rahm and Philip A. Bernstein, A survey of approaches to automatic schema matching, VLDB Journal 10(4), 2001"
    locator: the classification of matchers
  - book: isbn:9780898714548
    title: "Carl D. Meyer, Matrix Analysis and Applied Linear Algebra, SIAM, 2000"
    locator: "Chapter 8, Perron-Frobenius theory"
---

Similarity flooding is a heuristic for [schema matching](/schema-matching/). It turns two schemas into labeled graphs, starts from a guess of how similar each pair of nodes is, and lets the similarity of a pair flow to the pairs next to it until the values settle. A filter then keeps one partner for each node. The method knows nothing about schemas in particular, so it matches any two labeled graphs.

## In plain words

Two tables describe the same people with different names. You are fairly sure that the type "string" of one schema is the type "varchar" of the other. If two columns have similar types, the columns are a bit more likely to match. If two tables have columns that match, the tables are more likely to match, and that in turn makes their other columns more likely to match.

Similarity flooding repeats this reasoning in rounds. Each pair of nodes passes part of its score to the pairs that sit next to it in both graphs at the same time. After each round the scores are scaled so that the best one is 1. When the scores stop changing, a final step picks, for each node, at most one partner with a high score.

## The problem

The input is two directed graphs $A$ and $B$ with labeled edges $a \xrightarrow{l} a'$, and an initial similarity $\sigma^0(a, b) \ge 0$ for some pairs of a node $a$ of $A$ and a node $b$ of $B$. A schema becomes such a graph with nodes for tables, columns and types, and labels such as `col` and `type`. The initial values usually come from a string matcher on the names, for example [edit distance](/edit-distance/). The output is a set of pairs $(a, b)$ in which each node occurs at most one time. This is a heuristic answer to [schema matching](/schema-matching/), so there is no exact optimum to compare with.

The method uses these objects.

- A **map pair** is a pair $(a, b)$ of a node of $A$ and a node of $B$.
- The **pairwise connectivity graph** has an edge $(a, b) \xrightarrow{l} (a', b')$ for each edge $a \xrightarrow{l} a'$ of $A$ and each edge $b \xrightarrow{l} b'$ of $B$ with the same label $l$.
- The **propagation graph** has, for each such edge, a forward edge from $(a, b)$ to $(a', b')$ with weight $1/\mathrm{out}_l(a, b)$ and a backward edge from $(a', b')$ to $(a, b)$ with weight $1/\mathrm{in}_l(a', b')$. Here $\mathrm{out}_l(x)$ and $\mathrm{in}_l(x)$ count the $l$-edges out of and into $x$ in the pairwise connectivity graph. So a pair splits its score equally among its neighbors of each label. This weight rule is one choice, and other rules are possible.
- The **propagation step** is $\varphi(\sigma)(y) = \sum w \cdot \sigma(x)$ over the edges $x \to y$ of the propagation graph with weight $w$.

The fixpoint formulas differ in what is added back in each step.

| formula | the next vector before scaling |
|---|---|
| basic | $\sigma + \varphi(\sigma)$ |
| A | $\sigma^0 + \varphi(\sigma)$ |
| B | $\varphi(\sigma^0 + \sigma)$ |
| C | $(\sigma^0 + \sigma) + \varphi(\sigma^0 + \sigma)$ |

## The algorithm

```pseudo id=main
SIMILARITY-FLOODING(A, B, sigma0, formula, theta, eps, limit)
L1  P <- the pairwise connectivity graph of A and B
L2  for each edge x -l-> y of P do
L3      add x -> y with weight 1/out_l(x), and y -> x with weight 1/in_l(y)
L4  sigma <- sigma0
L5  repeat
L6      choose the base and the argument of the formula
L7      next <- base + phi(argument)
L8      next <- next / max(next)                  ▷ only if max(next) > 0
L9      r <- the Euclidean distance from next to sigma; sigma <- next
L10 until r < eps or limit steps are done
L11 run Gale-Shapley on the pairs with sigma >= theta and sigma > 0
L12 return the stable pairs
```

Line L1 builds the pairs of edges with the same label. Lines L2 and L3 give each edge a forward and a backward weight. Lines L5 to L10 iterate the chosen formula, and each step scales the vector so that its largest value is 1. Lines L11 and L12 are the filter. Here the filter is a [stable matching](/stable-matching/) found by [Gale-Shapley](/gale-shapley/): each node of $A$ ranks the nodes of $B$ by the similarity, each node of $B$ ranks the nodes of $A$ the same way, and ties are broken by the node order.

## Example

Schema $A$ has a table Emp with the columns Name of type string and Dept of type int. Schema $B$ has a table Staff with the columns FullName of type varchar and Unit of type integer. The graph of $A$ has the edges Emp $\xrightarrow{col}$ Name, Emp $\xrightarrow{col}$ Dept, Name $\xrightarrow{type}$ string and Dept $\xrightarrow{type}$ int, and $B$ is the same with its names. The initial similarity is $\sigma^0(\text{string}, \text{varchar}) = \sigma^0(\text{int}, \text{integer}) = 1$, and 0 for all other pairs. The names of the tables and the columns have nothing in common, so a name matcher gives them nothing.

The pairwise connectivity graph has 8 edges. The pair (Emp, Staff) has 4 `col` edges, to (Name, FullName), (Name, Unit), (Dept, FullName) and (Dept, Unit), so each forward weight from (Emp, Staff) is $1/4$. Each column pair has one `type` edge, for example (Name, FullName) $\xrightarrow{type}$ (string, varchar), and all the other weights are 1.

The first three steps of the basic formula give these values after scaling.

| step | (Emp, Staff) | (Name, FullName), (Dept, Unit) | (Name, Unit), (Dept, FullName) | (string, varchar), (int, integer) | (string, integer), (int, varchar) |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 0 | 1 | 0 |
| 2 | 1 | 1 | 0 | 1 | 0 |
| 3 | 1 | 0.75 | 0.0833 | 0.6667 | 0 |

In step 3, before scaling, (Emp, Staff) has $1 + 1 + 1 = 3$, (Name, FullName) has $1 + 1/4 + 1 = 2.25$ and (Name, Unit) has $0 + 1/4 = 0.25$. Division by 3 gives the row.

The basic formula goes on for 104 steps with $\varepsilon = 10^{-9}$. It ends with (Emp, Staff) at 1, all four column pairs at 0.3536, and all four type pairs at 0.25. The right column pairs and the wrong ones end with the same value, because the basic formula forgets $\sigma^0$ (see Correctness). Formula C stops after 43 steps with these values.

| pair | value |
|---|---|
| (Emp, Staff) | 1 |
| (Name, FullName), (Dept, Unit) | 0.9653 |
| (string, varchar), (int, integer) | 0.8876 |
| (Name, Unit), (Dept, FullName) | 0.1418 |
| (string, integer), (int, varchar) | 0.0640 |

The filter with $\theta = 0.5$ keeps (Emp, Staff), (Name, FullName), (Dept, Unit), (string, varchar) and (int, integer). The column pairs are found only through the types and the table, which is the point of the method.

## Correctness

There is no correct output to prove, because the matching itself is a heuristic. The [proof file](proofs/correctness.md) proves what the procedure guarantees.

- Lines L1 to L3 build exactly the propagation graph of the definition.
- Each step keeps all values in $[0, 1]$ with the largest equal to 1, unless the vector is 0. Only formula B can reach 0.
- The loop stops after at most the step limit.
- For the basic formula, assume the propagation graph is connected and $\sigma^0$ is nonnegative and not zero. Then the iteration is [power iteration](/power-iteration/) with the matrix $I + M$, where $M$ holds the weights. Each edge has a backward edge, so $M$ is irreducible, and $I + M$ is primitive. By the [Perron-Frobenius theorem](/perron-frobenius-theorem/), the vector converges to the Perron vector of $I + M$, scaled to a largest value of 1. The limit does not depend on $\sigma^0$.
- The filter returns a stable matching of the pairs at or above the threshold.

The last point but one is a theorem, and it explains the example: the basic formula forgets the initial similarities. Formulas A and C add $\sigma^0$ in each step, and B adds it inside $\varphi$. Their convergence is not proved here. That they give better matches is a heuristic claim, and only measurements on real schemas can support it.

## Complexity

Let $v$ be the number of map pairs that occur in the pairwise connectivity graph or in $\sigma^0$, let $e$ be the number of edges of that graph, and let $s$ be the number of steps.

- **Building the graphs.** With the edges of $B$ grouped by label, line L1 takes $O(|E_A| + |E_B| + e)$ time. The number $e$ is at most $|E_A| \cdot |E_B|$, and it is that large when all edges have the same label.
- **One step.** $\varphi$ visits each of the $2e$ weighted edges once, and the scaling and the distance visit each of the $v$ pairs, so a step takes $O(v + e)$ time.
- **The filter.** Sorting the preference lists takes $O(v \log v)$ time, and Gale-Shapley makes at most one proposal for each acceptable pair.
- **Total.** $O(s(v + e) + v \log v)$ time and $O(v + e)$ extra space.

The number of steps $s$ is not bounded by the analysis. For the basic formula it depends on the gap between the two largest eigenvalues of $I + M$. In practice the step limit bounds it.

## Properties

- **Deterministic.** The order of the nodes fixes the result, including the ties of the filter.
- **Not exact.** It is a heuristic and gives no guarantee on the quality of the match.
- **Generic.** It uses only the labeled graph. The meaning of the schemas enters through the graph encoding and through $\sigma^0$.
- **Symmetric.** Swapping $A$ and $B$ swaps the pairs and gives the same values. The weights depend only on the counts in the pairwise connectivity graph.
- **Structural.** A pair gets a high value when its neighbors in both graphs also have high values. Two nodes with no common label on their edges get no flow.

## Variants and improvements

- **Fixpoint formulas.** The four formulas of the table differ in how much of $\sigma^0$ they keep. Which one works best on a given kind of schema is a question for measurement.
- **Weight rules.** The equal split of this page is one rule. A rule can also weight an edge by the counts of both ends, or give some labels more weight than others.
- **Filters.** A plain threshold keeps all pairs above a value and allows many partners. The stable matching of this page gives at most one partner. A maximum-weight one-to-one match is the [assignment problem](/assignment-problem/), solved by the [Hungarian algorithm](/hungarian-algorithm/). Type rules can also forbid pairs, for example a table with a column.
- **Combination with other matchers.** In a matching system, similarity flooding is one structural matcher. Its output is combined with name, instance and constraint matchers, as in the survey of Rahm and Bernstein.

## When to use it

Use it when two schemas or models have a similar structure but poor name overlap, and you have a few confident seed pairs. It also fits other labeled graphs, such as XML schemas or two versions of the same model. Do not use it when the structures differ a lot, for example a flat table against a nested model of the same data, because the flow then goes along the wrong edges. Always show its output to a person for review, since it is a heuristic.

## Pitfalls

- **The basic formula forgets the seeds.** On a connected propagation graph it converges to a vector fixed by the graph shape alone, as in the example. Use a formula that adds $\sigma^0$ back.
- **Quadratic size.** The pairwise connectivity graph can have $|E_A| \cdot |E_B|$ edges when a few labels cover most edges. Fine labels, such as one label for each kind of edge, keep it small.
- **Global scaling.** All parts of the propagation graph are scaled by the same maximum. A small part that is not connected to the main part can fade toward 0 even when its seeds are good.
- **Stopping.** The loop may stop at the step limit with a vector that has not settled. Record the residual of line L9 and check it.
- **Ties in the filter.** Equal values are broken by the node order, and that choice is arbitrary. Two right answers and two wrong answers with the same value cannot be told apart by the filter.

## Implementations

## History

Sergey Melnik, Hector Garcia-Molina and Erhard Rahm presented similarity flooding at ICDE 2002. They described it as a generic graph matching algorithm and applied it to schema matching, where it plays the role of a structural matcher in the sense of the survey of Rahm and Bernstein from 2001. The idea that a node is similar to another when their neighbors are similar also drives other graph scores, and the fixpoint view links the method to [PageRank](/pagerank/) and to power iteration.

## References
