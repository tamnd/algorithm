---
tag: SCYM7S
kind: technique
slug: magic-sets
name: Magic sets transformation
aliases:
- magic set rewriting
- magic sets method for Datalog
- generalized magic sets
area: systems/database-algorithms
level: research
summary: "Rewrites a Datalog program for a query with constants, with magic predicates that pass the bindings sideways, so that bottom-up evaluation derives only facts relevant to the query."
prereqs: [datalog, semi-naive-evaluation]
see_also: [datalog-evaluation, sld-resolution, transitive-closure, query-optimization, dred-algorithm, horn-sat-forward-chaining]
sources:
  - paper: doi:10.1145/6012.15399
    title: François Bancilhon, David Maier, Yehoshua Sagiv and Jeffrey D. Ullman, Magic sets and other strange ways to implement logic programs, Proceedings of the 5th ACM SIGACT-SIGMOD Symposium on Principles of Database Systems (PODS 1986), 1 to 15
    locator: the magic sets method for linear rules with a bound query argument, the counting method, and the comparison with other strategies
  - paper: doi:10.1016/0743-1066(91)90038-Q
    title: Catriel Beeri and Raghu Ramakrishnan, On the power of magic, Journal of Logic Programming 10(3 and 4), 255 to 299 (1991)
    locator: adorned programs, sideways information passing strategies, generalized and supplementary magic sets for all Datalog programs, the proof that the rewritten program gives the same answers, and the comparison with top-down evaluation
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 13 (evaluation of Datalog), the section on the magic set transformation, with adornments and the same-generation example
---

The magic sets transformation makes bottom-up evaluation of a [Datalog](/datalog/) program goal directed. A query such as $\mathit{path}(10, y)$ needs only the facts about nodes that can be reached from node 10, but [semi-naive evaluation](/semi-naive-evaluation/) of the program computes the whole least model. The transformation rewrites the program for the query. It marks each argument of each IDB atom as bound or free (the *adornment*), it fixes an order in which bindings pass from atom to atom in a rule body (the *sideways information passing strategy*, or SIPS), and it adds a *magic predicate* for each adorned predicate. A magic fact $\mathit{magic\_path\_bf}(c)$ says that the subquery $\mathit{path}(c, y)$ is needed, and each rule of the new program fires only for needed subqueries. Bottom-up evaluation of the new program gives the same answers to the query. Bancilhon, Maier, Sagiv and Ullman introduced the method in 1986, and Beeri and Ramakrishnan gave the general form for all Datalog programs and its proof in 1991.

## In plain words

Suppose you ask "where can I go from city 10?" A plain bottom-up method first works out every route between every pair of cities and then picks the routes that start at 10. Most of that work is wasted.

The magic sets method first changes the rules. It adds a second kind of fact, a note that says "we need the routes that start at city c". The note for city 10 is there from the start. A rule that finds a route now runs only when there is a note for its start city. When the rule wants a route from a next city, it first writes a note for that city.

The changed rules still run bottom up, in rounds, with no search and no stack. But they only build the routes that the question needs, and the answer is the same as before.

## When it applies

- The query has constants, such as $\mathit{path}(10, y)$ or $\mathit{sg}(40, y)$, and the answer depends on a small part of the least model.
- The program is Datalog, possibly with stratified negation, where the method applies with care to keep the strata (see the pitfalls).
- The evaluation engine is bottom up: semi-naive evaluation, a relational engine with recursive SQL, or a parallel dataflow engine. Magic sets give such an engine the goal direction of top-down evaluation without changing the engine.
- It also applies to nonrecursive SQL views and correlated subqueries, where the magic relation is the set of values that the outer query passes in.

It does not help when the query has no constants and is not joined with a selective relation: then the magic predicates hold everything, and the rewritten program does more work than the original one.

## The template

**Conventions.** A term is a variable or a constant. An *adornment* of a predicate of arity $k$ is a string of $k$ letters, $b$ for bound and $f$ for free. For an atom $p(\bar t)$ and a set of bound variables, the adornment marks a position $b$ when its term is a constant or a bound variable. For an adorned predicate $p^a$, the magic predicate $\mathit{magic\_}p^a$ has one argument for each $b$ position, and $\bar t^{\,b}$ is the list of the terms of $\bar t$ at those positions. The SIPS here is the left-to-right one: a variable is bound in a body atom if it is bound in the head or occurs in an atom to its left.

```pseudo id=main
MAGIC-SETS(P, query q(t̄))
L1  a ← adornment of t̄ with no bound variables      ▷ the constants of the query are bound
L2  todo ← {q^a}; P' ← ∅
L3  while todo has a predicate p^a that is not done do
L4      mark p^a as done
L5      for each rule p(s̄) ← B₁, …, Bₘ of P do
L6          bound ← the variables of s̄ at the b positions of a
L7          for i ← 1 to m do                                   ▷ the SIPS: left to right
L8              if Bᵢ = r(ū) is an IDB atom then
L9                  c ← adornment of ū given bound; add r^c to todo
L10                 add to P' the magic rule  magic_r^c(ū^b) ← magic_p^a(s̄^b), B₁', …, B_{i-1}'
L11             bound ← bound ∪ the variables of Bᵢ;  Bᵢ' ← Bᵢ with IDB predicates adorned
L12         add to P' the modified rule  p^a(s̄) ← magic_p^a(s̄^b), B₁', …, Bₘ'
L13 add to P' the seed fact  magic_q^a(t̄^b)
L14 evaluate P' bottom up (semi-naively) on D; return the facts of q^a that match t̄
```

Lines L1 to L4 build the *adorned program*: only the adorned predicates that can be reached from the query are made. Line L10 makes a magic rule for each IDB atom of each rule. Its head is the subquery that the atom asks, and its body is what is known at that point: the magic fact of the head, which carries the bindings of the caller, and the atoms to the left. Line L12 guards each rule with the magic predicate of its head, so that the rule fires only for subqueries that are needed. Line L13 seeds the evaluation with the query.

**Why the answers stay the same.** Let $M$ be the least model of $P$ on $D$ and $M'$ that of $P'$. Each fact $p^a(\bar c)$ in $M'$ is a fact $p(\bar c)$ of $M$, because each modified rule is a rule of $P$ with one more body atom. Conversely, show by induction on the height of a derivation in $P$ that if $p(\bar c) \in M$ and $\mathit{magic\_}p^a(\bar c^{\,b}) \in M'$, then $p^a(\bar c) \in M'$. Take the last rule instance of the derivation. Its head magic fact is in $M'$. Go through the body from left to right: the atoms to the left are in $M'$, by the induction for IDB atoms and because $D \subseteq M'$ for EDB atoms, so the magic rule of line L10 puts the magic fact of the next IDB atom in $M'$, and then the induction gives that atom. So the whole body is in $M'$, and the modified rule of line L12 fires. The seed of line L13 is the magic fact of the query, so every answer in $M$ is an answer in $M'$. Beeri and Ramakrishnan prove this for every SIPS.

**Cost.** The rewriting takes time linear in the size of the adorned program, which has at most $2^k$ adorned copies of a predicate of arity $k$. The evaluation of $P'$ derives the magic facts, which are the subqueries that top-down evaluation with the same SIPS would make, and the IDB facts that answer them. Beeri and Ramakrishnan show that, with the same SIPS, this is the same set of subqueries and answers as top-down evaluation with tables.

## Classic examples

**Transitive closure from one node.** For the right-linear program $\mathit{path}(x, y) \leftarrow \mathit{edge}(x, y)$, $\mathit{path}(x, y) \leftarrow \mathit{edge}(x, z), \mathit{path}(z, y)$ and the query $\mathit{path}(10, y)$, the adornment is $bf$, and the rewritten program is

$$\begin{aligned}
\mathit{magic\_path\_bf}(10)&, \\
\mathit{magic\_path\_bf}(z) &\leftarrow \mathit{magic\_path\_bf}(x), \mathit{edge}(x, z), \\
\mathit{path\_bf}(x, y) &\leftarrow \mathit{magic\_path\_bf}(x), \mathit{edge}(x, y), \\
\mathit{path\_bf}(x, y) &\leftarrow \mathit{magic\_path\_bf}(x), \mathit{edge}(x, z), \mathit{path\_bf}(z, y).
\end{aligned}$$

The magic facts are the nodes reachable from 10, which is a graph search. The answers are the paths that start at these nodes.

**Derived facts on a chain.** On the chain $1 \to 2 \to \cdots \to 20$, the full least model has 190 $\mathit{path}$ facts. These are the numbers of IDB facts that each program derives for the query $\mathit{path}(10, y)$, which has 10 answers:

| program | full evaluation | magic sets |
|---|---|---|
| right-linear, $\mathit{edge}(x, z), \mathit{path}(z, y)$ | 190 | 66 (11 magic, 55 path) |
| left-linear, $\mathit{path}(x, z), \mathit{edge}(z, y)$ | 190 | 11 (1 magic, 10 path) |
| nonlinear, $\mathit{path}(x, z), \mathit{path}(z, y)$ | 190 | 66 |

In the left-linear program, the recursive atom $\mathit{path}(x, z)$ has $x$ bound, so its magic rule is $\mathit{magic\_path\_bf}(x) \leftarrow \mathit{magic\_path\_bf}(x)$, and only node 10 is ever asked. The method finds the 10 answers and nothing else.

**Same generation.** With $\mathit{sg}(x, y) \leftarrow \mathit{flat}(x, y)$ and $\mathit{sg}(x, y) \leftarrow \mathit{up}(x, u), \mathit{sg}(u, v), \mathit{down}(v, y)$, the query $\mathit{sg}(40, y)$ on a complete binary tree with 63 nodes, where $\mathit{up}$ goes to the parent, $\mathit{down}$ to a child, and $\mathit{flat}$ joins each node to itself, has the 32 leaves as its answers. Full evaluation derives 1365 $\mathit{sg}$ facts, all pairs of nodes at the same depth. The rewritten program derives 69: 6 magic facts, for node 40 and its 5 ancestors, and 63 $\mathit{sg}$ facts for them. The magic rule here is $\mathit{magic\_sg\_bf}(u) \leftarrow \mathit{magic\_sg\_bf}(x), \mathit{up}(x, u)$.

All the counts above come from the implementation of this page, whose tests also compare the answers with full evaluation on random graphs and random programs.

## Variations

- **Other SIPS.** Any order of the body atoms, or any choice of which bound atoms pass bindings to which, gives a correct rewriting. A good SIPS binds the recursive atom through a selective EDB atom.
- **Supplementary magic sets.** The magic rule of line L10 and the modified rule of line L12 recompute the same prefix joins $B_1', \ldots, B_{i-1}'$. Supplementary predicates store each prefix once, with the variables that later atoms need (Beeri and Ramakrishnan).
- **Counting.** For linear programs such as same generation, the counting method of Bancilhon and others keeps, with each magic fact, its distance from the query, and then goes down the same number of steps. It is faster but fails to stop on cyclic data.
- **Magic for SQL.** Query optimizers apply the same idea to correlated subqueries and views: compute the set of bindings that the outer query passes in, and join the view with it first.
- **Magic with negation.** With stratified negation, the rewritten program may no longer be stratified. Variants restrict the rewriting or use well-founded evaluation.
- **Top-down with tables.** SLG resolution and query-subquery evaluation compute the same subqueries and answers at run time instead of by rewriting.

## Pitfalls

- **Queries with no constants.** With adornment $ff\cdots f$ the magic predicate has no argument, the guard is always true, and the rewriting only adds work.
- **The SIPS matters.** The left-to-right SIPS on a body that starts with the IDB atom passes no binding to it, as in $\mathit{path}(x, y) \leftarrow \mathit{path}(z, y), \mathit{edge}(x, z)$ with $x$ bound: the recursive atom gets adornment $ff$, and the magic set can grow to the full relation. Reorder the body or choose another SIPS.
- **Many adornments.** A predicate can get several adornments, each with its own copy of the rules. The rewritten program can be much larger than the original one.
- **Answers of other adornments.** The answers to the query are the facts of $q^a$ that match the query; the facts of other adorned copies are not answers.
- **Negation.** Rewriting a stratified program can make a predicate depend negatively on itself through the magic predicates. Do not apply the plain rewriting to programs with negation.

## Exercises

1. Write the rewritten program for the left-linear transitive closure and the query $\mathit{path}(10, y)$, and explain why it derives only the answers and one magic fact.
2. Rewrite the right-linear program for the query $\mathit{path}(x, 10)$. Which adornments appear with the left-to-right SIPS? Which body order gives the adornment $fb$ for the recursive atom?
3. Give a program and a query with constants for which the rewritten program derives more facts than the original one.
4. Show that the magic facts of the same-generation example are exactly the ancestors of the query node, including the node itself.
5. Prove that the rewritten program derives no fact $p^a(\bar c)$ for which $p(\bar c)$ is not in the original least model.

## References
