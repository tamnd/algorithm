---
tag: Y3KK7E
kind: algorithm
slug: minicon-algorithm
name: MiniCon algorithm
aliases:
- MiniCon
area: databases/data-integration-and-cleaning
level: advanced
summary: "Rewrite a conjunctive query using views: form minimal descriptions of the subgoals each view can cover, then combine sets of them that cover the query exactly once."
solves: [answering-queries-using-views]
model: word-ram
complexity:
  vars: {n: the number of subgoals of the query, m: the largest number of subgoals of a view, k: the number of views, a: the largest arity of a predicate}
  time: {worst: O(a n k (m+1)^n (n k m+1)^n)}
  space: {extra: O(a n k (m+1)^n)}
properties: {deterministic: true, exact: true, online: false, in_place: false, recursive: true}
history:
  year: 2000
  people: [Rachel Pottinger, Alon Y. Halevy]
  note: "Pottinger and Levy gave MiniCon at VLDB 2000 as a faster successor of the bucket and inverse rules algorithms. The journal version by Pottinger and Halevy appeared in the VLDB Journal in 2001."
prereqs: [conjunctive-query, query-containment-problem, answering-queries-using-views]
see_also: [bucket-algorithm, inverse-rules-algorithm, view-rewriting-np-completeness, chandra-merlin-theorem, gav-and-lav, certain-answers, materialized-view, view-selection]
sources:
  - paper: doi:10.1007/s007780100048
    title: "Rachel Pottinger and Alon Halevy, MiniCon: a scalable algorithm for answering queries using views, The VLDB Journal 10(2), 2001"
    locator: "pages 182-198, MiniCon descriptions, Property 1, the combination step and the experiments"
  - paper: doi:10.1007/s007780100054
    title: "Alon Y. Halevy, Answering queries using views: a survey, The VLDB Journal 10(4), 2001"
    locator: "pages 270-294, the section on algorithms for data integration"
  - book: isbn:9780124160446
    title: "AnHai Doan, Alon Halevy and Zachary Ives, Principles of Data Integration, Morgan Kaufmann, 2012"
    locator: "Chapter 2, answering queries using views, the MiniCon algorithm"
---

MiniCon rewrites a [conjunctive query](/conjunctive-query/) into a union of conjunctive queries over a set of views, for [answering queries using views](/answering-queries-using-views/) in local-as-view integration. It returns the maximally contained rewriting, as the [bucket algorithm](/bucket-algorithm/) does, but it does the containment work before it combines views. The bucket algorithm puts each view in a bucket for one subgoal and then tests every combination for containment. MiniCon first finds, for each view, the smallest set of subgoals that the view must cover together, and then it only combines these sets when they do not overlap. No containment test is left at the end.

## In plain words

A view stores the answers of a small query, and some of its variables are not stored. If a query subgoal uses a variable that the view hides, the view can only help if it also covers every other subgoal that uses that variable, because the hidden value cannot be joined with anything outside the view.

MiniCon starts with one subgoal and one view. Each time the view would hide a variable that some other subgoal needs, it pulls that subgoal into the same group. The result is a small group of subgoals that the view covers alone. Then it picks groups from different views so that each subgoal is in exactly one group, and each such choice gives one rewriting.

## The problem

The input is a query $Q(\bar x) \text{ :- } R_1(\bar u_1), \ldots, R_n(\bar u_n)$ in AHV notation and a set of views, each of the form $V(\bar Y) \text{ :- } S_1(\bar w_1), \ldots, S_r(\bar w_r)$. All terms are variables, there are no comparisons, and set semantics holds. A variable of a view is *distinguished* if it is in the head and *existential* otherwise. A rewriting is a conjunctive query over the view names. It is contained in $Q$ when its expansion, the query you get by replacing each view atom by the body of the view with new existential variables, is [contained](/query-containment-problem/) in $Q$. The output is a union of contained rewritings that contains every other contained union of conjunctive queries.

A **MiniCon description** (MCD) for a view $V$ is a tuple $(h, \varphi, G)$. $G$ is a set of subgoals of $Q$, $h$ is a head homomorphism that may equate head variables of $V$, and $\varphi$ maps the variables of $G$ to variables of $V$ so that each subgoal of $G$ maps onto $h$ of some subgoal of $V$. It must satisfy Property 1:

- **C1.** Each head variable of $Q$ in $G$ maps to a distinguished variable of $V$.
- **C2.** If $\varphi(x)$ is existential, then every subgoal of $Q$ that holds $x$ is in $G$.

## The algorithm

```pseudo id=main
MINICON(Q, Views)
L1  C <- empty
L2  for each subgoal g of Q, view V and subgoal v of V with the predicate of g do
L3      (h, phi) <- the least restrictive pair with phi(g) = h(v); skip if none exists
L4      for each (h', phi', G) in CLOSE(Q, V, h, phi, {g}) do
L5          add the MCD (V, h', phi', G) to C
L6  R <- empty
L7  for each set {M_1, ..., M_c} of MCDs in C whose sets G_i partition the subgoals of Q do
L8      EC <- the classes of the query variables, with x ~ y if phi_i(x) = phi_i(y) for some i
L9      Psi_i(y) <- a variable x with phi_i(x) = y, or a fresh variable if there is none
L10     add Q'(EC(X)) :- V_1(EC(Psi_1(h_1(Y_1)))), ..., V_c(EC(Psi_c(h_c(Y_c)))) to R
L11 return R

CLOSE(Q, V, h, phi, G)
L12 if phi maps a head variable of Q to an existential variable of V then return nothing
L13 if no subgoal g' outside G holds a variable x with phi(x) existential then return {(h, phi, G)}
L14 for each subgoal v' of V with the predicate of g' do
L15     extend (h, phi) least restrictively so that phi(g') = h(v'); skip v' if impossible
L16     return also everything that CLOSE(Q, V, h, phi, G + {g'}) returns
```

Lines L3 and L15 unify a query subgoal with a view subgoal position by position. When two query variables meet one view variable, or one query variable meets two view variables, the two view variables must become one. That is allowed only for two distinguished variables, and then the head homomorphism $h$ equates them. An existential variable cannot be equated with anything else, because the view stores no value for it.

Line L12 is C1. Line L13 checks C2: it looks for a subgoal outside $G$ that shares a variable mapped to an existential. If there is one, lines L14 to L16 try each way to map it into the same view. A branch that fails is dropped, and if all branches fail, the seed of line L2 gives no MCD.

The combination step needs no containment test. Line L7 takes MCDs whose subgoal sets are disjoint and cover the query. Line L8 joins the query variables that one view puts in the same place. Line L9 picks the argument of each head position: the query variable mapped there, or a new variable for a position that no query variable uses.

## Example

The query and views come from Pottinger and Halevy. $Q(x) \text{ :- } \text{cites}(x, y), \text{cites}(y, x), \text{sameTopic}(x, y)$ asks for papers that cite a paper on the same topic that cites them back. The views are

- $V_4(a) \text{ :- } \text{cites}(a, b), \text{cites}(b, a)$,
- $V_5(c, d) \text{ :- } \text{sameTopic}(c, d)$,
- $V_6(f, h) \text{ :- } \text{cites}(f, g), \text{cites}(g, h), \text{sameTopic}(f, g)$.

Call the subgoals $g_1, g_2, g_3$. The table shows the seeds of line L2 and what CLOSE does with them.

| seed | after line L3 | CLOSE | MCD |
|---|---|---|---|
| $g_1$ with cites$(a, b)$ of $V_4$ | $x \mapsto a$, $y \mapsto b$ | $y$ is existential, so add $g_2$ with cites$(b, a)$; then $g_3$ needs sameTopic, which $V_4$ lacks | none |
| $g_1$ with cites$(b, a)$ of $V_4$ | $x \mapsto b$ | line L12: head variable $x$ on an existential | none |
| $g_3$ with sameTopic$(c, d)$ of $V_5$ | $x \mapsto c$, $y \mapsto d$ | nothing to add | $(V_5, \{g_3\})$ |
| $g_1$ with cites$(f, g)$ of $V_6$ | $x \mapsto f$, $y \mapsto g$ | add $g_2$ with cites$(g, h)$, which forces $h \mapsto f$; add $g_3$ with sameTopic$(f, g)$ | $(V_6, \{g_1, g_2, g_3\})$, $h = \{f, h \mapsto f\}$ |
| $g_2$ with cites$(g, h)$ of $V_6$ | $y \mapsto g$, $x \mapsto h$ | the same closure | the same MCD |

The other seeds fail at line L12 or repeat an MCD. $V_5$ covers $g_3$ alone, but no MCD covers $g_1$ and $g_2$ without $g_3$. So line L7 finds one partition, $\{g_1, g_2, g_3\}$, and the answer is $Q'(x) \text{ :- } V_6(x, x)$. The bucket algorithm would build 2 times 2 times 2 candidates here and test each one for containment.

**A chain.** For $Q(x, w) \text{ :- } e(x, y), e(y, z), e(z, w)$ with $V_1(a, c) \text{ :- } e(a, b), e(b, c)$ and $V_2(a, b) \text{ :- } e(a, b)$, there are five MCDs: $V_2$ on each subgoal alone, $V_1$ on $\{g_1, g_2\}$ and $V_1$ on $\{g_2, g_3\}$. A single subgoal cannot use $V_1$, since its middle variable $b$ is existential and is shared with the next or previous subgoal. Three partitions exist, and MiniCon returns $Q'(x, w) \text{ :- } V_1(x, z), V_2(z, w)$, $Q'(x, w) \text{ :- } V_2(x, y), V_1(y, w)$ and $Q'(x, w) \text{ :- } V_2(x, y), V_2(y, z), V_2(z, w)$.

## Correctness

**Theorem (Pottinger and Halevy).** For conjunctive queries and views without comparisons, the union of the rewritings that MINICON returns is a maximally contained rewriting of $Q$ among unions of conjunctive queries over the views.

The [proof file](proofs/correctness.md) proves it in full. Soundness uses C2: a variable that two MCDs share is distinguished in both, so the containment mapping of each MCD agrees with the others on it. Completeness starts from a containment mapping of $Q$ into the expansion of any contained rewriting. The subgoals that map into one view atom split into pieces that share existential variables, each piece is an MCD that the search finds, and these MCDs give a rewriting that contains the given one.

By the results of Abiteboul and Duschka, the maximally contained rewriting gives the [certain answers](/certain-answers/) under the open world assumption when the views and the query are conjunctive.

## Complexity

All bounds are in combined complexity, since the query and the views are the input.

- **Time.** An MCD is fixed by its view and by the view subgoal of each query subgoal, so there are at most $k (m + 1)^n$ MCDs. A set of MCDs that partitions the subgoals is fixed by the partition and by these choices, so line L7 yields at most $(n k m)^n$ sets, as Pottinger and Halevy state. With the scans of the enumeration, the total is $O(a\, n\, k\, (m + 1)^n (n k m + 1)^n)$ time (a theorem, proved in the proof file).
- **Space.** $O(a\, n\, k\, (m + 1)^n)$ for the MCDs, plus the output.

The exponent in $n$ cannot go away in general, since deciding whether an equivalent rewriting exists is [NP-complete](/view-rewriting-np-completeness/). In practice the number of MCDs is small, because C2 kills most seeds early.

## Properties

- **Exact.** The output is the maximally contained rewriting, not an approximation of it.
- **Deterministic.** The order of the views and the subgoals fixes the order of the output.
- **No final containment test.** Every combination of line L7 is a contained rewriting, by the soundness lemma.
- **Duplicates.** Two partitions can give the same rewriting up to variable names, and a rewriting can be contained in another one. The code removes only exact copies.

## Variants and improvements

- **Comparison predicates.** Pottinger and Halevy extend MiniCon to queries and views with arithmetic comparisons. The extension needs extra checks on the comparisons that an MCD covers. This page and its code treat only the case without comparisons.
- **Equivalent rewritings.** To find an [equivalent](/view-rewriting-np-completeness/) rewriting, run the same combination step, then test each candidate for containment of $Q$ in its expansion.
- **Inverse rules.** The [inverse rules algorithm](/inverse-rules-algorithm/) gets the same answers from the view instance by a Datalog program with Skolem terms, without writing out the rewriting.

## When to use it

Use MiniCon when you need the rewriting itself, for example to send it to the sources or to optimize it, and the views are many. Pottinger and Levy measured (a measurement, in Java on a dual Pentium II) that MiniCon scales to more than a thousand views for chain queries, while the bucket and inverse rules algorithms are much slower. If you only need the answers on one view instance, the inverse rules program is simpler.

## Pitfalls

- **Skipping C2.** If line L13 always returns, an MCD can cover one subgoal with a view that hides the join variable. In the chain, $V_1$ would cover $e(x, y)$ alone with $y \mapsto b$, and the combination $Q'(x, w) \text{ :- } V_1(x, u), V_2(y, z), V_2(z, w)$ loses the join on $y$. Its expansion is not contained in $Q$.
- **Equating an existential.** Lines L3 and L15 may only merge two distinguished view variables. If the unifier also merges an existential with another variable, it produces MCDs whose rewritings claim joins that the view does not expose.
- **Head variables on existentials.** Without line L12, $g_1$ with cites$(b, a)$ of $V_4$ in the example sends the answer variable $x$ to $b$, which the view does not return.
- **Overlapping MCDs.** Line L7 needs disjoint sets. If it allows overlaps, the rewritings are still contained, but there are many more of them, and each one is contained in a rewriting from a disjoint set, so the extra work buys nothing.

## Implementations

## History

Levy, Rajaraman and Ordille introduced the bucket algorithm for the Information Manifold in 1996, and Duschka and Genesereth gave the inverse rules algorithm in 1997. Pottinger and Levy (Alon Levy, now Halevy) presented MiniCon at VLDB 2000. The journal version, with comparison predicates and experiments, appeared in the VLDB Journal in 2001. Halevy's survey of the same year places MiniCon among the algorithms for data integration.

## References
