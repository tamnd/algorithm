---
tag: S43GW2
kind: technique
slug: datalog-program-analysis
name: Datalog-based program analysis
aliases:
- declarative program analysis
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: advanced
summary: Writes an analysis as Datalog rules over facts taken from the program, and runs it on a Datalog engine, often with BDDs or semi-naive evaluation.
prereqs: [datalog, datalog-evaluation, andersen-analysis]
see_also: [semi-naive-evaluation, magic-sets, bdd-points-to-analysis, reduced-ordered-bdd, context-sensitivity, object-sensitivity, demand-driven-points-to, taint-analysis]
sources:
  - paper: doi:10.1007/3-540-57877-3_26
    title: Thomas W. Reps, Solving demand versions of interprocedural analysis problems, Compiler Construction (CC '94), LNCS 786, 1994, pages 389-403
    locator: interprocedural dataflow problems written as logic programs, and their demand versions
  - paper: doi:10.1145/996841.996859
    title: John Whaley and Monica S. Lam, Cloning-based context-sensitive pointer alias analysis using binary decision diagrams, Proceedings of the ACM SIGPLAN 2004 Conference on Programming Language Design and Implementation (PLDI '04), 2004, pages 131-144
    locator: the bddbddb system, which evaluates Datalog over relations stored as BDDs, and a context-sensitive points-to analysis for Java by cloning
  - paper: doi:10.1145/1640089.1640108
    title: Martin Bravenboer and Yannis Smaragdakis, Strictly declarative specification of sophisticated points-to analyses, Proceedings of the 24th ACM SIGPLAN Conference on Object Oriented Programming Systems Languages and Applications (OOPSLA '09), 2009, pages 243-261
    locator: the Doop framework, points-to analyses for Java written fully in Datalog, and the optimization of rules for semi-naive evaluation with explicit tables
  - paper: doi:10.1007/978-3-319-41540-6_23
    title: Herbert Jordan, Bernhard Scholz and Pavle Subotić, Soufflé, on synthesis of program analyzers, Computer Aided Verification (CAV 2016), LNCS 9780, 2016, pages 422-430
    locator: the translation of Datalog rules into C++ programs that run semi-naive evaluation on specialized data structures
  - paper: doi:10.1145/800070.802186
    title: Moshe Y. Vardi, The complexity of relational query languages (extended abstract), Proceedings of the 14th Annual ACM Symposium on Theory of Computing (STOC '82), 1982, pages 137-146
    locator: data complexity and combined complexity, and the polynomial data complexity of fixed-point queries
---

Datalog-based program analysis writes a program analysis as a set of [Datalog](/datalog/) rules. A front end reads the program and stores what it says as input relations, such as "variable `v` is assigned a new object at site `h`". The rules define the output relations, such as "variable `v` may point to an object of site `h`", and a Datalog engine computes their least fixed point. Points-to analysis, call-graph construction, taint analysis and many dataflow problems fit in a few rules each. For a fixed set of rules the analysis always terminates, in time polynomial in the size of the program, because the facts that can be derived form a finite set. Engines reach large programs with [semi-naive evaluation](/semi-naive-evaluation/), with relations stored as [BDDs](/reduced-ordered-bdd/) (bddbddb), with hand-tuned rules on explicit tables (Doop), or by compiling the rules to C++ (Soufflé).

## In plain words

Many program analyses are rules of the form "if this and that hold, then this other thing holds". For example: if a variable gets a new object, it points to that object; if one variable is copied into another, the second points to whatever the first points to. Datalog is a small language for exactly such rules. The analysis first reads the program and writes down simple facts about it, one per statement, in tables. Then the rules are given to a Datalog engine. The engine applies the rules again and again and adds the new facts that they give, until nothing new appears. The facts at the end are the result of the analysis. The person who writes the analysis says what to compute, and the engine decides how to compute it fast.

## When it applies

- The facts of the analysis are finite relations over entities of the program: variables, allocation sites, fields, methods, call sites, statements, contexts.
- The analysis is monotone: new facts never remove old ones. Points-to sets, call graphs, reachability and taint are of this kind. An analysis that needs to remove facts, such as a kill set, needs stratified negation or an explicit complement relation.
- The rules change often, as when one tries many variants of context sensitivity. A change is a few lines of rules, and the engine does the rest.
- The program is large. The engine handles indexing, join order and storage for all rules alike, and a good engine is often faster than a hand-written solver.

## The template

**Step 1: extract the facts.** Normalize the program, for example to [three-address code](/three-address-code/), and write one tuple per relevant statement. For a flow-insensitive points-to analysis of a Java-like language:

| relation | statement |
|---|---|
| `New(v, h)` | `v = new C()` at allocation site `h` |
| `Assign(v, w)` | `v = w` |
| `Store(b, f, w)` | `b.f = w` |
| `Load(v, b, f)` | `v = b.f` |

**Step 2: write the rules.** [Andersen's analysis](/andersen-analysis/) with fields is four rules.

```
VarPointsTo(v, h)    :- New(v, h).
VarPointsTo(v, h)    :- Assign(v, w), VarPointsTo(w, h).
FieldPointsTo(g, f, h) :- Store(b, f, w), VarPointsTo(b, g), VarPointsTo(w, h).
VarPointsTo(v, h)    :- Load(v, b, f), VarPointsTo(b, g), FieldPointsTo(g, f, h).
```

The input relations are the extensional database (EDB) and the derived ones are the intensional database (IDB). Calls add relations for call sites, formal and actual parameters and return values, and rules that build the call graph from the points-to sets of receivers at the same time, so that the call graph and the points-to sets reach a common fixed point.

**Step 3: evaluate.** The engine computes the least model of the rules over the facts, bottom-up, usually by semi-naive evaluation, which joins each rule only with facts that are new in the last round. Relations can be stored as hash tables, B-trees, tries or BDDs. For a query about one variable, the [magic sets](/magic-sets/) transformation restricts the work to facts that the query needs.

**Step 4: read the result.** The output relations are the analysis result, and further rules can query them: a may-alias relation, the virtual calls with one target, the casts that may fail.

**Why it terminates in polynomial time.** Let the rules be fixed, with $p$ predicates of arity at most $a$, $r$ rules, at most $b$ atoms in a body and at most $w$ variables in a rule. The facts from a program of size $n$ mention a set $D$ of constants with $|D| = d = O(n)$.

*Claim.* The least model has at most $p d^a$ facts, and naive evaluation computes it in $O(p\, r\, b\, d^{a+w})$ steps, with constant-time lookups. For fixed rules this is polynomial in $n$.

*Proof.* Datalog rules have no function symbols, and every variable of a head occurs in the body, so by induction on the length of a derivation every derived fact is a predicate applied to constants of $D$ and of the rules. That set, the part of the Herbrand base over these constants, has at most $p d^a$ elements, counting the constants of the rules into $D$. Let $T$ map a set $I$ of facts to the EDB together with all heads of rule instances whose bodies are in $I$. $T$ is monotone on the finite lattice of subsets of the Herbrand base, so the sequence $I_0 = \emptyset$, $I_{k+1} = T(I_k)$ increases and reaches the least fixed point of $T$, which is the least model, by the [Kleene fixed-point theorem](/kleene-fixed-point-theorem/). Every step before the last adds a fact, so there are at most $p d^a + 1$ steps. One step tries, for each rule, each of at most $d^w$ assignments of its variables and looks up at most $b$ body atoms, which is $O(r\, b\, d^w)$. Multiplying gives the bound. $\square$

The bound is coarse. The rules above have $a = 3$ and $w = 5$, so the claim gives $O(n^{8})$, while Andersen's analysis runs in cubic time; semi-naive evaluation with good join orders and indexes comes much closer to the hand-written bound. Stratified negation keeps the claim: the strata are evaluated in order, each with the lower ones fixed. Vardi (STOC 1982) showed that for fixed rules the evaluation is in P, and the problem is P-complete, so a general speed-up to fast parallel time is unlikely. When the rules are part of the input, $a$ and $w$ grow, and [Datalog evaluation](/datalog-evaluation/) is EXPTIME-complete.

## Classic examples

**Andersen's analysis on five statements.** The program

```
a = new A()      // site h1
b = new B()      // site h2
c = a
a.f = b
d = c.f
```

gives the facts `New(a, h1)`, `New(b, h2)`, `Assign(c, a)`, `Store(a, f, b)` and `Load(d, c, f)`. Semi-naive evaluation of the four rules runs in rounds.

| round | new facts | rule |
|---|---|---|
| 1 | `VarPointsTo(a, h1)`, `VarPointsTo(b, h2)` | 1 |
| 2 | `VarPointsTo(c, h1)`, `FieldPointsTo(h1, f, h2)` | 2 and 3 |
| 3 | `VarPointsTo(d, h2)` | 4 |
| 4 | none | |

Rule 4 fires in round 3, the first round in which both `VarPointsTo(c, h1)` and `FieldPointsTo(h1, f, h2)` are present. The result is that `d` may point to the object of site `h2`.

**Context sensitivity by cloning.** Add a context to the relations: `VarPointsTo(c, v, h)` and `CallGraph(c, i, c2, m)`, where a context is the last $k$ call sites. The rules compute the new context at each call. Pure Datalog has no function symbols, so the contexts must come from a finite set, given as a relation that pairs each context and call site with the next context. For a fixed $k$ there are at most $n^k$ contexts and the analysis stays polynomial. Whaley and Lam (PLDI 2004) wrote such an analysis for Java in bddbddb, which stores each relation as a BDD and runs each rule as BDD operations; the BDDs share the many similar contexts, and the analysis handled huge numbers of contexts.

**Doop.** Bravenboer and Smaragdakis (OOPSLA 2009) wrote points-to analyses for Java, with several forms of context sensitivity and with the call graph, reflection and exceptions computed together, all as Datalog rules on explicit tables. They reported that, with rules tuned for semi-naive evaluation, their analyses were faster than the same analyses in the BDD-based Paddle framework.

**Demand analysis.** Reps (CC 1994) wrote interprocedural dataflow problems as logic programs and asked for their demand versions, which compute the answer at one program point only. The companion chapter in *Applications of Logic Databases* (Kluwer, 1994) obtains the demand versions with the magic sets transformation, which turns the exhaustive bottom-up analysis into a goal-directed one.

## Variations

- **Soufflé.** Jordan, Scholz and Subotić (CAV 2016) translate the rules into parallel C++ programs with data structures chosen for each relation. Soufflé runs the Doop rules and many other analyses.
- **Lattices.** Plain Datalog computes sets of tuples. Extensions such as Flix let a relation hold an element of a lattice, which gives constant propagation and interval analysis in the same style.
- **Incremental evaluation.** After a change to the program, update the fixed point instead of computing it again. This needs care with negation and with facts that lose their last derivation.
- **Query languages.** CodeQL writes analyses in a Datalog dialect with classes and lets users query a database built from the code.
- **Taint and security.** Sources, sinks and propagation rules sit beside the points-to rules, so that [taint analysis](/taint-analysis/) and the heap analysis are solved together.
- **Demand-driven analysis.** Magic sets and [demand-driven points-to analysis](/demand-driven-points-to/) compute only the facts that a query needs.

## Pitfalls

- **No function symbols.** Unbounded call strings, abstract syntax built during the analysis, or integers with arithmetic do not fit. Bound them, as with $k$-limited contexts, or use an extension and lose the termination argument.
- **Non-monotone parts.** Rules with negation must be stratified. An analysis whose result feeds back into its own negated premise, such as a kill set that depends on the points-to sets, has no stratification and must be restated.
- **The front end.** Most errors are in the fact extraction: a missing kind of statement, a wrong normalization, a library without a model. The rules cannot fix missing facts.
- **Join order.** The same rules can run fast or slowly depending on the order of the body atoms and the indexes. Doop's speed came in part from rules rewritten for evaluation.
- **BDD variable order.** With bddbddb the size of the BDDs, and so the speed, depends heavily on the order of the BDD variables.
- **Computing everything.** Bottom-up evaluation computes the whole least model even when one query matters. Use magic sets or a demand-driven analysis when only a few answers are needed.

## Exercises

1. Add rules for static calls with one parameter and one return value to the four rules of Andersen's analysis, using relations `Call(i, m)`, `Actual(i, v)`, `Formal(m, p)`, `Return(m, r)` and `Result(i, v)`.
2. Write reaching definitions as Datalog rules over `Def(s, x)`, `Succ(s, t)` and `Kills(s, t)`. Which relation needs negation, and is the program stratified?
3. Run naive and semi-naive evaluation on the five-statement example and count the rule instances that each one tries.
4. Show that with contexts of the last $k$ call sites, the number of facts in `VarPointsTo(c, v, h)` is $O(n^{k+2})$.
5. Apply the magic sets transformation to the rules of Andersen's analysis for the query `VarPointsTo(d, h)` with `d` fixed, and say which facts of the example are no longer derived.

## References
