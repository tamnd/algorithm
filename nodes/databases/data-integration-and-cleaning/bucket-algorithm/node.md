---
tag: GBX8BH
kind: algorithm
slug: bucket-algorithm
name: Bucket algorithm
aliases:
- Levy bucket algorithm
area: databases/data-integration-and-cleaning
level: advanced
summary: "Rewrite a query using views: put in a bucket for each subgoal the views that can cover it, then test each combination of bucket entries for containment."
solves: [answering-queries-using-views]
model: word-ram
complexity:
  vars: {n: the number of subgoals of the query, m: the largest number of subgoals of a view, k: the number of views, a: the largest arity of a predicate}
  time: {worst: O(a n (k m)^(2n) (n m)^(3n))}
  space: {extra: O(a n (k m)^n (n m)^n)}
properties: {deterministic: true, exact: true, online: false, in_place: false, recursive: false}
history:
  year: 1996
  people: [Alon Y. Levy, Anand Rajaraman, Joann J. Ordille]
  note: "Levy, Rajaraman and Ordille used the bucket algorithm in the Information Manifold, a system that queried many web sources described as views, and presented it at VLDB 1996."
prereqs: [conjunctive-query, query-containment-problem, answering-queries-using-views]
see_also: [minicon-algorithm, inverse-rules-algorithm, chandra-merlin-theorem, view-rewriting-np-completeness, gav-and-lav, certain-answers, conjunctive-query-minimization, materialized-view]
sources:
  - paper: doi:10.1007/s007780100048
    title: "Rachel Pottinger and Alon Halevy, MiniCon: a scalable algorithm for answering queries using views, The VLDB Journal 10(2), 2001"
    locator: "pages 182-198, the description of the bucket algorithm, its running example and the experimental comparison"
  - paper: doi:10.1007/s007780100054
    title: "Alon Y. Halevy, Answering queries using views: a survey, The VLDB Journal 10(4), 2001"
    locator: "pages 270-294, the bucket algorithm among the algorithms for data integration"
  - book: isbn:9780124160446
    title: "AnHai Doan, Alon Halevy and Zachary Ives, Principles of Data Integration, Morgan Kaufmann, 2012"
    locator: "Chapter 2, answering queries using views, the bucket algorithm"
---

The bucket algorithm rewrites a [conjunctive query](/conjunctive-query/) into a union of conjunctive queries over a set of views, for [answering queries using views](/answering-queries-using-views/) in local-as-view integration. It was the first practical algorithm for this task. It differs from [MiniCon](/minicon-algorithm/) in where it does the work: the bucket algorithm considers each subgoal alone when it chooses views, and then pays with a [containment test](/query-containment-problem/) for every combination. MiniCon looks at the joins first and needs no test at the end.

## In plain words

Each part of the question, such as "x cites y", gets a bucket. Into the bucket go all the views that hold facts of that kind and that keep the values the answer needs. Then the algorithm tries every way to take one view from each bucket.

A choice can still be wrong, because two parts of the question may need to join on a value that a view does not keep. So the algorithm checks each choice: it writes out what the chosen views really say and tests whether that is enough to answer the question. Sometimes a choice works only after two of its variables are made the same, and the algorithm tries that too.

## The problem

The input is a query $Q(\bar x) \text{ :- } R_1(\bar u_1), \ldots, R_n(\bar u_n)$ in AHV notation and a set of views, each of the form $V(\bar Y) \text{ :- } S_1(\bar w_1), \ldots, S_r(\bar w_r)$. All terms are variables, there are no comparisons, and set semantics holds. A variable of a view is distinguished if it is in the head and existential otherwise. A rewriting is a conjunctive query over the view names, and it is contained in $Q$ when its expansion, with each view atom replaced by the view body and new existential variables, is contained in $Q$. The output is a union of contained rewritings that contains every other contained union of conjunctive queries.

## The algorithm

```pseudo id=main
BUCKET(Q, Views)
L1  for each subgoal g of Q do
L2      bucket[g] <- empty
L3      for each view V and each subgoal v of V with the predicate of g do
L4          if g unifies with v and each head variable of Q in g meets a head variable of V then
L5              add the head of V under the unifier to bucket[g], with fresh variables for unmatched positions
L6  result <- empty
L7  for each choice (a_1, ..., a_n) in bucket[g_1] × ... × bucket[g_n] do
L8      Q' <- Q(X) :- a_1, ..., a_n
L9      for each most general equating theta of variables of Q' with theta(Q') contained in Q do
L10         add theta(Q'), with redundant atoms removed, to result
L11 return result without the members that are contained in other members
```

Line L4 unifies the query subgoal with the view subgoal position by position, so that query variables and view variables that meet fall into one class. The test asks that every head variable of $Q$ in the subgoal lands in a class with a distinguished view variable. Otherwise the view cannot return the value that the answer needs. Line L5 writes the view atom with, at each head position, a query variable of its class, or a new variable if no query variable reached that position.

Line L9 is the containment test. It expands $Q'$ and looks for a containment mapping from $Q$ into the expansion, by the [Chandra-Merlin theorem](/chandra-merlin-theorem/). The search may equate variables of $Q'$, but never an existential variable of the expansion with anything other than a query variable. Each search branch that succeeds gives the least equating for that branch. Line L10 removes atoms while the query stays equivalent, the same step as [conjunctive query minimization](/conjunctive-query-minimization/). Line L11 drops rewritings that add no answers.

## Example

The query and views are the running example of Pottinger and Halevy. $Q(x) \text{ :- } \text{cites}(x, y), \text{cites}(y, x), \text{sameTopic}(x, y)$, with

- $V_4(a) \text{ :- } \text{cites}(a, b), \text{cites}(b, a)$,
- $V_5(c, d) \text{ :- } \text{sameTopic}(c, d)$,
- $V_6(f, h) \text{ :- } \text{cites}(f, g), \text{cites}(g, h), \text{sameTopic}(f, g)$.

Lines L1 to L5 give these buckets. The fresh variables are $u_1, u_2, u_3$.

| subgoal | bucket |
|---|---|
| cites$(x, y)$ | $V_4(x)$, $V_6(x, u_1)$ |
| cites$(y, x)$ | $V_4(x)$, $V_6(u_2, x)$ |
| sameTopic$(x, y)$ | $V_5(x, y)$, $V_6(x, u_3)$ |

$V_4$ is in the first bucket by cites$(a, b)$, with $x \mapsto a$. Its other subgoal cites$(b, a)$ would put $x$ on the existential $b$, so line L4 rejects it. Line L7 makes $2 \cdot 2 \cdot 2 = 8$ candidates. None of them is contained in $Q$ as it stands.

| candidate | line L9 | line L10 |
|---|---|---|
| $V_4(x), V_4(x), V_5(x, y)$ | $y$ must be the existential $b$ of $V_4$ and also the variable $y$ of $V_5$: no equating | none |
| $V_6(x, u_1), V_6(u_2, x), V_6(x, u_3)$ | map all three subgoals into the expansion of one $V_6$ atom, which equates its free argument with $x$ | $V_6(x, x)$ |
| $V_4(x), V_4(x), V_6(x, u_3)$ | map all three subgoals into the expansion of $V_6(x, u_3)$: $u_3 = x$ | $V_4(x), V_6(x, x)$ |
| $V_6(x, u_1), V_6(u_2, x), V_5(x, y)$ | the same with the first atom: $u_1 = x$ | $V_6(x, x), V_5(x, y)$ |
| the 4 other candidates | each holds a $V_6$ atom and gets the same kind of equating | $V_6(x, x)$ with $V_4(x)$, $V_5(x, y)$ or both |

Line L10 cannot remove $V_4(x)$ or $V_5(x, y)$, since each one adds a condition. But each of these rewritings is contained in $V_6(x, x)$, so line L11 leaves one rewriting, $Q'(x) \text{ :- } V_6(x, x)$, the same as MiniCon gives. The work was 8 candidates with a containment search each, where MiniCon formed two descriptions and one combination.

**A chain.** For $Q(x, w) \text{ :- } e(x, y), e(y, z), e(z, w)$ with $V_1(a, c) \text{ :- } e(a, b), e(b, c)$ and $V_2(a, b) \text{ :- } e(a, b)$, the buckets are $\{V_1(x, u_1), V_2(x, y)\}$, $\{V_1(y, u_2), V_1(u_3, z), V_2(y, z)\}$ and $\{V_1(u_4, w), V_2(z, w)\}$, so there are 12 candidates. The ones made only of $V_1$ atoms admit no equating. The result, after line L11, is $V_1(x, u), V_2(u, w)$, then $V_2(x, y), V_1(y, w)$, then $V_2(x, y), V_2(y, z), V_2(z, w)$.

## Correctness

**Theorem.** For conjunctive queries and views without comparisons, the union of the rewritings that BUCKET returns is a maximally contained rewriting of $Q$ among unions of conjunctive queries over the views.

The [proof file](proofs/correctness.md) proves it in full. Soundness holds because line L9 only keeps equatings that pass the containment test. For completeness, take a contained rewriting $P$ and a containment mapping of $Q$ into its expansion. Each subgoal lands in the expansion of one view atom of $P$, so it passes line L4 for that view, and the entries of these views form a candidate. The containment mapping tells the search of line L9 which atoms to use, and the equating it finds is more general than the one that turns the candidate into a part of $P$. So $P$ is contained in a rewriting that line L10 adds.

Under the open world assumption, the maximally contained rewriting gives the [certain answers](/certain-answers/) of a conjunctive query over conjunctive views, by the results of Abiteboul and Duschka.

## Complexity

All bounds are in combined complexity, and all are theorems proved in the proof file.

- **Time.** Each bucket has at most $k m$ entries, so there are at most $(k m)^n$ candidates. The search of line L9 has at most $(n m)^n$ branches per candidate. With the containment tests of lines L10 and L11, the total is $O(a\, n\, (k m)^{2n} (n m)^{3n})$.
- **Space.** $O(a\, n\, (k m)^n (n m)^n)$ for the rewritings found before line L11.

Deciding whether an equivalent rewriting exists is [NP-complete](/view-rewriting-np-completeness/), so an exponent in $n$ is expected. The product of line L7 is the part that hurts in practice: Pottinger and Halevy measured (a measurement) that the bucket algorithm slows down sharply as the number of views grows, while MiniCon does not.

## Properties

- **Exact.** The output is the maximally contained rewriting.
- **Deterministic.** The order of views and subgoals fixes the order of the output.
- **Local first step.** Line L4 looks at one subgoal at a time, so a bucket can hold a view that fails for every combination.
- **Containment per candidate.** Each candidate costs a search that is exponential in the worst case.

## Variants and improvements

- **Comparison predicates.** Levy, Rajaraman and Ordille also check that the comparisons of the query are consistent with those of the view before an entry goes into a bucket.
- **MiniCon.** [MiniCon](/minicon-algorithm/) moves the join check of line L9 into the first step, so it never builds the candidates that fail.
- **Inverse rules.** The [inverse rules algorithm](/inverse-rules-algorithm/) skips the rewriting and computes the same answers with a Datalog program.

## When to use it

Use it for teaching, and when there are few views and short queries, where the candidates are few and the code is simple. For many views, MiniCon gives the same output much faster. When only the answers on one view instance are needed, inverse rules are simpler.

## Pitfalls

- **No containment test.** If line L9 accepts every candidate, the result is not contained in $Q$. In the example, $V_4(x), V_4(x), V_5(x, y)$ would be returned, but it does not say that the paper $y$ of sameTopic is the one that $x$ cites.
- **No equating.** If line L9 tests only the candidate as it is, with $\theta$ the identity, the example returns nothing, since none of the 8 candidates is contained in $Q$ without $u_1 = x$. The answer $V_6(x, x)$ is lost.
- **Distinguished variables in the bucket.** If line L4 does not check the head variables of $Q$, $V_4$ enters the first bucket through cites$(b, a)$ as $V_4(y)$, with $x$ on the hidden $b$. Line L9 still keeps only contained rewritings, so the output stays right, but the number of candidates grows.
- **Line L11.** Without it, the output can hold rewritings contained in others. The answers are the same, but the union is larger than needed.

## Implementations

## History

Levy, Rajaraman and Ordille described the bucket algorithm at VLDB 1996 as the query planner of the Information Manifold, a system that answered queries over many web sources described as views. Duschka and Genesereth gave the inverse rules algorithm in 1997. Pottinger and Levy presented MiniCon at VLDB 2000 and compared it with both. Halevy's 2001 survey describes all three.

## References
