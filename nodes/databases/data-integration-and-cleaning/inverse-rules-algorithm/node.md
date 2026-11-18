---
tag: TPC6ZK
kind: algorithm
slug: inverse-rules-algorithm
name: Inverse rules algorithm
aliases:
- inverse rules
area: databases/data-integration-and-cleaning
level: advanced
summary: "Turn each local-as-view definition into Datalog rules with Skolem terms that derive global facts from source facts, then evaluate the query and drop answers with Skolem terms."
solves: [answering-queries-using-views]
model: word-ram
complexity:
  vars: {N: the number of tuples in the view instance, r: the largest arity of a predicate, b: the largest number of body atoms in a rule}
  time: {worst: O(N^(r(b+1)))}
  space: {extra: O(N^r)}
properties: {deterministic: true, exact: true, online: false, in_place: false, recursive: false}
history:
  year: 1997
  people: [Oliver M. Duschka, Michael R. Genesereth]
  note: "Duschka and Genesereth gave the inverse rules at PODS 1997 and showed that they answer recursive Datalog queries over conjunctive views. The journal version with Levy appeared in 2000."
prereqs: [datalog, skolemization, gav-and-lav, answering-queries-using-views]
see_also: [bucket-algorithm, minicon-algorithm, certain-answers, chase-algorithm, datalog-evaluation, semi-naive-evaluation, view-rewriting-np-completeness, data-exchange-problem]
sources:
  - paper: doi:10.1145/263661.263674
    title: "Oliver M. Duschka and Michael R. Genesereth, Answering recursive queries using views, PODS 1997"
    locator: "pages 109-116, the inverse rules and the proof that they give the maximally contained Datalog rewriting"
  - paper: doi:10.1016/s0743-1066(99)00025-4
    title: "Oliver M. Duschka, Michael R. Genesereth and Alon Y. Levy, Recursive query plans for data integration, Journal of Logic Programming 43(1), 2000"
    locator: "pages 49-73, inverse rules, the removal of function symbols, and functional dependencies"
  - paper: doi:10.1007/s007780100054
    title: "Alon Y. Halevy, Answering queries using views: a survey, The VLDB Journal 10(4), 2001"
    locator: "pages 270-294, the inverse rules algorithm among the algorithms for data integration"
  - paper: doi:10.1145/275487.275516
    title: "Serge Abiteboul and Oliver M. Duschka, Complexity of answering queries using materialized views, PODS 1998"
    locator: "pages 254-263, certain answers under the open world assumption"
---

The inverse rules algorithm answers a query over a global schema when the sources are described as views over that schema, the local-as-view setting of [GAV and LAV](/gav-and-lav/) integration. It differs from the [bucket algorithm](/bucket-algorithm/) and [MiniCon](/minicon-algorithm/) in what it builds. Those two write a union of conjunctive queries over the views. Inverse rules write a [Datalog](/datalog/) program that runs the views backwards, so the query may itself be recursive. On a given view instance the program returns the [certain answers](/certain-answers/) under the open world assumption.

## In plain words

A view says "the source holds the pairs (a, c) such that a cites some b and b cites c". Read backwards, each stored pair tells you two facts of the global database: a cites something, and that something cites c. You do not know the something, so you give it a name built from the stored pair, such as "the paper between a and c".

The algorithm writes one backward rule for each atom of each view. It then runs the query on the facts that these rules produce, with the made up names in place of the unknown values. An answer that holds a made up name is not a real answer, so it is dropped. The rest are exactly the answers that hold in every database the sources allow.

## The problem

The input is a set of views $V(\bar Y) \text{ :- } p_1(\bar u_1), \ldots, p_r(\bar u_r)$ over global predicates, a view instance $I$ that gives a set of tuples for each view, and a query $Q$. $Q$ is a Datalog program over the global predicates with a goal predicate, for example a [conjunctive query](/conjunctive-query/) $Q(\bar x) \text{ :- } R_1(\bar u_1), \ldots, R_m(\bar u_m)$ in AHV notation. The views and the query have no constants and no comparisons. Set semantics holds. Under the open world assumption, a global database $D$ is possible if each view of $D$ contains the stored tuples. The output is the set of tuples of constants that $Q$ returns on every possible $D$.

## The algorithm

```pseudo id=main
INVERSE-RULES(Q, Views, I)
L1  R <- empty
L2  for each view V(Y) :- p_1(u_1), ..., p_r(u_r) do
L3      sigma <- the identity on Y, and u -> f_{V,u}(Y) for each existential variable u of V
L4      for j <- 1 to r do
L5          add the rule p_j(sigma(u_j)) :- V(Y) to R
L6  P <- the rules of Q together with R
L7  M <- the least fixpoint of P on the facts of I
L8  return the goal tuples of M that hold no function term
```

Line L3 is a [Skolemization](/skolemization/) of the view definition. The view says that for each stored tuple there exist values of its existential variables. The term $f_{V,u}(\bar Y)$ names the value of $u$ for one stored tuple, and different tuples give different names. Lines L4 and L5 split the body, so each rule derives one global atom from one view atom. These rules are not recursive, and their heads hold function terms of depth one only.

Line L7 is ordinary Datalog evaluation, by naive or [semi-naive](/semi-naive-evaluation/) iteration. The rules of $Q$ never build new function terms, so the fixpoint is finite. Line L8 removes answers that depend on a value that no source stores.

## Example

The views are the running example of Pottinger and Halevy:

- $V_4(a) \text{ :- } \text{cites}(a, b), \text{cites}(b, a)$,
- $V_5(c, d) \text{ :- } \text{sameTopic}(c, d)$,
- $V_6(f, h) \text{ :- } \text{cites}(f, g), \text{cites}(g, h), \text{sameTopic}(f, g)$.

Lines L1 to L5 give six rules:

| rule | head | body |
|---|---|---|
| R1 | cites$(a, f_{V_4,b}(a))$ | $V_4(a)$ |
| R2 | cites$(f_{V_4,b}(a), a)$ | $V_4(a)$ |
| R3 | sameTopic$(c, d)$ | $V_5(c, d)$ |
| R4 | cites$(f, f_{V_6,g}(f, h))$ | $V_6(f, h)$ |
| R5 | cites$(f_{V_6,g}(f, h), h)$ | $V_6(f, h)$ |
| R6 | sameTopic$(f, f_{V_6,g}(f, h))$ | $V_6(f, h)$ |

The query is $Q(x) \text{ :- } \text{cites}(x, y), \text{cites}(y, x), \text{sameTopic}(x, y)$, and the instance is $V_4 = \{(p_1)\}$, $V_5 = \{(p_1, p_2)\}$, $V_6 = \{(p_3, p_3), (p_4, p_5)\}$. Write $s_1 = f_{V_4,b}(p_1)$, $s_3 = f_{V_6,g}(p_3, p_3)$ and $s_4 = f_{V_6,g}(p_4, p_5)$.

| step | facts |
|---|---|
| R1, R2 on $V_4(p_1)$ | cites$(p_1, s_1)$, cites$(s_1, p_1)$ |
| R3 on $V_5(p_1, p_2)$ | sameTopic$(p_1, p_2)$ |
| R4 to R6 on $V_6(p_3, p_3)$ | cites$(p_3, s_3)$, cites$(s_3, p_3)$, sameTopic$(p_3, s_3)$ |
| R4 to R6 on $V_6(p_4, p_5)$ | cites$(p_4, s_4)$, cites$(s_4, p_5)$, sameTopic$(p_4, s_4)$ |
| rule of $Q$ | $Q(p_3)$ with $y = s_3$ |

$Q(p_1)$ is not derived. It would need sameTopic$(p_1, s_1)$, but the sources only say that $p_1$ has the same topic as $p_2$, and nothing says that $p_2$ is the paper that $p_1$ cites. $Q(p_4)$ would need cites$(s_4, p_4)$. So line L8 returns $\{(p_3)\}$. The rewriting $Q'(x) \text{ :- } V_6(x, x)$ that MiniCon finds gives the same answer.

**A recursive query.** Let $Q$ be the transitive closure path$(x, y) \text{ :- } e(x, y)$ and path$(x, y) \text{ :- } e(x, z), \text{path}(z, y)$, with views Hop$(a, c) \text{ :- } e(a, b), e(b, c)$ and Direct$(a, b) \text{ :- } e(a, b)$. With Hop $= \{(1, 3)\}$ and Direct $= \{(3, 4), (5, 1)\}$, the rules give $e(1, s)$, $e(s, 3)$, $e(3, 4)$ and $e(5, 1)$ for a Skolem term $s$. The fixpoint has path facts through $s$, and line L8 keeps $(1, 3)$, $(1, 4)$, $(3, 4)$, $(5, 1)$, $(5, 3)$ and $(5, 4)$. No finite union of conjunctive queries over the views gives these answers on all instances, since the paths can be of any length.

## Correctness

**Theorem (Duschka and Genesereth).** For a Datalog query and conjunctive views, INVERSE-RULES stops and returns exactly the certain answers of $Q$ on $I$ under the open world assumption.

The [proof file](proofs/correctness.md) proves it in full. The facts derived by lines L1 to L5 form a database $D_0$ in which the function terms play the role of labeled nulls, the same database the [chase](/chase-algorithm/) would build. $D_0$ is possible, since each stored tuple has its witness. $D_0$ maps into each possible database by a map that fixes the constants, since the witnesses of that database give the values of the function terms. Datalog answers are preserved by such maps. So a tuple of constants is an answer on $D_0$ if and only if it is an answer on every possible database.

Duschka and Genesereth also show that the program $P$ is the maximally contained rewriting of $Q$ among Datalog programs over the views, once the function terms are removed. For a conjunctive query, it is equivalent to the union that MiniCon returns.

## Complexity

The bounds are theorems, proved in the proof file. They are in data complexity: the query and the views are fixed and the view instance grows.

- **Time.** The model has $O(N)$ values and $O(N^r)$ possible facts. Naive evaluation makes at most $O(N^r)$ rounds of $O(N^{r b})$ work, so $O(N^{r(b+1)})$ in total. Semi-naive evaluation does better in practice.
- **Space.** $O(N^r)$ for the model.

Building the rules takes time linear in the size of the view definitions. In combined complexity, evaluating the Datalog program is EXPTIME-complete in general, as for any Datalog program.

## Properties

- **Exact.** It returns the certain answers, not an approximation.
- **Deterministic.** The rules and the fixpoint do not depend on any choice.
- **Recursive queries.** It works unchanged when $Q$ is recursive, where the bucket algorithm and MiniCon do not apply.
- **No rewriting search.** The rules come from the views alone, so they can be built once and reused for every query.
- **Repeated work.** The derived global database can be much larger than needed, because every view atom is unfolded for every stored tuple, even if the query never uses it.

## Variants and improvements

- **Removing function symbols.** Duschka, Genesereth and Levy turn the program into a Datalog program without function terms, by tracking which arguments hold which function symbol. The result is a rewriting over the views that a plain Datalog engine can run.
- **Functional dependencies and access patterns.** The same journal paper handles functional dependencies on the global schema and sources with binding patterns, where the maximally contained rewriting can need recursion even for a conjunctive query.
- **The chase.** In [data exchange](/data-exchange-problem/), the same idea appears as the chase of source-to-target dependencies, with labeled nulls in place of function terms.

## When to use it

Use inverse rules when the query is recursive, or when you have a Datalog engine and want the answers on a given view instance. For conjunctive queries where the rewriting itself is needed, for example to optimize the plan or to send subqueries to the sources, MiniCon is faster. In the experiments of Pottinger and Levy (a measurement), MiniCon was faster than the inverse rules when both had to produce a rewriting.

## Pitfalls

- **One null per variable, not per tuple.** If line L3 uses a constant name such as $b_{V_4}$ for the existential $b$, all tuples of $V_4$ share one unknown paper. Then $V_4(p_1)$ and $V_4(p_6)$ give cites$(p_1, b)$ and cites$(b, p_6)$, and a path query wrongly finds a path from $p_1$ to $p_6$.
- **Keeping function terms in answers.** Without the filter of line L8, the output holds tuples such as path$(1, s)$ that name no real value.
- **Closed world.** The algorithm gives certain answers under the open world assumption. Under the closed world assumption, where each view holds exactly its stored tuples, certain answers to conjunctive queries are coNP-hard in data complexity, as Abiteboul and Duschka showed.
- **Comparisons.** With comparison predicates in the views, a Skolem term has no known order, and the rules of line L5 are no longer enough.

## Implementations

## History

Duschka and Genesereth introduced the inverse rules at PODS 1997, in a paper on recursive queries over views. The journal version, with Levy, appeared in the Journal of Logic Programming in 2000 and added the removal of function symbols, functional dependencies and binding patterns. Abiteboul and Duschka placed the method among the results on the complexity of certain answers in 1998. Pottinger and Levy compared it with the bucket algorithm and MiniCon in 2000.

## References
