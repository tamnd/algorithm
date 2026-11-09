---
tag: JF7B8D
kind: algorithm
slug: stalmarck-algorithm
name: Stalmarck's algorithm
aliases:
- Stalmarck's method
- dilemma rule
- Stålmarck's proof procedure
area: logic-and-constraints/sat-solving
level: advanced
summary: Decides SAT by growing a set of equivalences between subformulas with simple rules on triplets and the dilemma rule, which keeps what both values of a variable imply.
solves: [sat]
model: word-ram
complexity:
  vars: {n: the number of variables, m: the number of clauses, s: "the size |F|, the total number of literal occurrences", t: "the number of nodes, n + s - m + 1"}
  time: {worst: O(n (2 n t)^n s t^2), best: O(n s t^2)}
  space: {extra: O(n t + m)}
properties: {deterministic: true, exact: true, online: false, recursive: true, in_place: false}
history:
  year: 1989
  people: [Gunnar Stålmarck]
  note: Stålmarck filed a Swedish patent application in June 1989. The US patent 5,276,897 was filed on 14 June 1990 and granted on 4 January 1994.
prereqs: [sat, conjunctive-normal-form, tseitin-transformation, unit-propagation, disjoint-set]
see_also: [dpll, cdcl, lookahead-sat, failed-literal-probing, equivalent-literal-substitution, binary-decision-diagram, equivalence-checking, boolean-circuit]
sources:
  - paper: doi:10.1023/A:1008725524946
    title: Mary Sheeran and Gunnar Stålmarck, A tutorial on Stålmarck's proof procedure for propositional logic, Formal Methods in System Design 16(1), 2000, 23-58
    locator: the triplet form of a formula, the simple rules, the dilemma rule, k-saturation and the hardness of a formula
  - url: "https://patents.google.com/patent/US5276897A/en"
    title: Gunnar Stålmarck, Method and system for computer-aided proving of tautologies, US patent 5,276,897
    locator: filed 14 June 1990, granted 4 January 1994, with Swedish priority of 16 June 1989; the claims define the triplets, the propagation rules and the dilemma rule
---

Stålmarck's algorithm decides the [SAT problem](/sat/) by reasoning about equivalences, not about single assignments. It cuts the formula into small parts called *triplets*, each of the form $x \leftrightarrow (y \wedge z)$, and keeps one relation $E$ that says which literals and subformulas must be equal. *Simple rules* close $E$ over each triplet. The *dilemma rule* branches on a variable, closes $E$ in both branches, and keeps the equivalences that both branches derive. Repeating the dilemma rule with nesting depth $k$ is called $k$-saturation. It runs in polynomial time for fixed $k$, and some $k \le n$ decides every formula. Gunnar Stålmarck patented the method in Sweden in 1989 and in the US in 1994. It is used mainly to prove that formulas from hardware and software verification are tautologies.

## In plain words

Write the formula as many small facts, each one saying that one wire is the AND of two other wires. Keep a list of the wires that must have the same value, or opposite values.

Some steps are forced. If an AND wire is on, both inputs are on. If one input is on, the output equals the other input. Do all such steps.

When nothing is forced, pick one input and try it both ways. Do all forced steps in each case. Any fact that comes out in both cases is true in general, so you keep it, and you forget the rest. If one case ends in a clash, the other case must hold. If both clash, the formula has no solution.

If a level of trying is not enough, you try inside the tries, two levels deep, and so on.

## The problem

The input is a CNF formula $F$ over the variables $x_1, \ldots, x_n$ with $m$ clauses. A clause is a list of literals, and $|F|$ is the total number of literal occurrences. The output is a model of $F$ or UNSAT. The original method decides whether a formula $A$ is a tautology, by an attempt to refute $\neg A$; this is the same problem, since $A$ is a tautology exactly when $\neg A$ is unsatisfiable.

## The algorithm

**Triplets.** The tutorial of Sheeran and Stålmarck writes formulas with implication, so that its triplets have the form $x \leftrightarrow (y \to z)$. This page and its implementation use AND triplets $x \leftrightarrow (y \wedge z)$ over literals, which is the same thing up to negation, since $y \to z \equiv \neg(y \wedge \neg z)$. A clause $(\ell_1 \vee \cdots \vee \ell_w)$ is false exactly when $\neg\ell_1 \wedge \cdots \wedge \neg\ell_w$ is true. So the clause gets a chain of $w - 1$ new nodes $g_2 = \neg\ell_1 \wedge \neg\ell_2$, $g_j = g_{j-1} \wedge \neg\ell_j$, and the fact $\neg g_w \equiv \top$. A unit clause $(\ell)$ gives the fact $\ell \equiv \top$ and no triplet. This is a [Tseitin transformation](/tseitin-transformation/) in which the gate definitions are kept as triplets, not as clauses. There are $|F| - m$ triplets and $t = n + |F| - m + 1$ nodes: the constant $\top$, the $n$ variables and the new nodes.

**The relation.** $E$ is an equivalence relation on literals over the nodes, closed under negation: $a \equiv b$ in $E$ if and only if $\neg a \equiv \neg b$ in $E$. A [disjoint-set](/disjoint-set/) structure with a parity bit on each edge stores it; the parity says whether a node equals its root or the negation of the root. $E$ is *contradictory* when it contains $\top \equiv \bot$. A variable $v$ is *fixed* when $v \equiv \top$ or $v \equiv \bot$ is in $E$.

**The simple rules.** For each triplet $x \leftrightarrow (y \wedge z)$:

| rule | if $E$ contains | then add |
|---|---|---|
| R1 | $x \equiv \top$ | $y \equiv \top$ and $z \equiv \top$ |
| R2 | $y \equiv \bot$ or $z \equiv \bot$ | $x \equiv \bot$ |
| R3 | $y \equiv \top$ (or $z \equiv \top$) | $x \equiv z$ (or $x \equiv y$) |
| R4 | $y \equiv z$ | $x \equiv y$ |
| R5 | $y \equiv \neg z$ | $x \equiv \bot$ |
| R6 | $x \equiv \neg y$ (or $x \equiv \neg z$) | $y \equiv \top$ and $z \equiv \bot$ (or $z \equiv \top$ and $y \equiv \bot$) |

Closing $E$ under these rules is *0-saturation*.

**The dilemma rule.** Let $v$ be a variable that $E$ does not fix. Compute $E_1$, the closure of $E \cup \{v \equiv \top\}$, and $E_0$, the closure of $E \cup \{v \equiv \bot\}$, and replace $E$ by $E_1 \cap E_0$. A contradictory relation contains every pair, so if $E_1$ is contradictory the result is $E_0$, and the other way round. *$k$-saturation* uses $(k-1)$-saturation as the closure inside the dilemma rule, and it applies the dilemma rule to every variable until a whole pass adds nothing.

```pseudo id=main
STALMARCK(F)
L1  build the triplets T of F, and let E hold ¬g ≡ ⊤ for the last node g of each clause
L2  for k = 0, 1, 2, … do
L3      E ← SATURATE(T, E, k)
L4      if E is contradictory then return UNSAT
L5      if EXTEND(T, E, k) returns a model β then return SAT and β
L6      ▷ k-saturation cannot decide F; go on with k + 1
SATURATE(T, E, k)
L7  repeat
L8      close E under the simple rules R1 to R6 on T
L9      if E is contradictory or k = 0 then return E
L10     for each class of variables that E does not fix, with one variable v of it, do
L11         E1 ← SATURATE(T, E ∪ {v ≡ ⊤}, k − 1);  E0 ← SATURATE(T, E ∪ {v ≡ ⊥}, k − 1)
L12         E ← E1 ∩ E0                       ▷ a contradictory branch adds nothing to the intersection
L13 until the pass of lines L10 to L12 adds nothing to E
```

Line L5 turns a $k$-saturated relation into a model, if it can, by fixing one variable at a time:

```pseudo id=extend
EXTEND(T, E, k)
1  for each variable v that E does not fix do
2      E' ← SATURATE(T, E ∪ {v ≡ ⊤}, k)
3      if E' is contradictory then E' ← SATURATE(T, E ∪ {v ≡ ⊥}, k)
4      if E' is contradictory then return FAIL     ▷ F has no model, but level k cannot see it
5      E ← E'
6  return the assignment that E fixes
```

The tutorial presents the procedure as a proof system: $k$-saturation is applied to the relation of $\neg A$, and if it derives a contradiction, $A$ is proved. A formula has *hardness* $k$ when $k$-saturation refutes it and $(k-1)$-saturation does not. Lines L2 to L6 search for the hardness by increasing $k$, and EXTEND adds the satisfiable side, which a proof procedure does not need.

## Example

Take $n = 4$ variables and $m = 6$ clauses:

$$(\neg x_1 \vee x_2),\ (\neg x_2 \vee x_1),\ (x_1 \vee x_3),\ (\neg x_1 \vee \neg x_3),\ (x_4 \vee \neg x_2),\ (x_4 \vee x_2).$$

Each clause has two literals, so each gives one triplet whose node is $\bot$: $a = x_1 \wedge \neg x_2$, $b = x_2 \wedge \neg x_1$, $c = \neg x_1 \wedge \neg x_3$, $d = x_1 \wedge x_3$, $e = \neg x_4 \wedge x_2$, $f = \neg x_4 \wedge \neg x_2$. The table shows $E$ after each step, without the facts $a, \ldots, f \equiv \bot$ of line L1.

| step | line | what happens | $E$ after the step |
|---|---|---|---|
| 1 | L8, $k = 0$ | no rule applies: a node equal to $\bot$ with free inputs forces nothing | nothing |
| 2 | L5, $k = 0$ | EXTEND tries $x_1 \equiv \top$: R3 on $a$ and $d$, then on $e$, gives $x_2 \equiv \top$, $x_3 \equiv \bot$, $x_4 \equiv \top$ | model found |
| 3 | L11, $k = 1$, $v = x_1$, branch $\top$ | the same three facts as in step 2 | $x_1, x_2, x_4 \equiv \top$, $x_3 \equiv \bot$ |
| 4 | L11, $k = 1$, $v = x_1$, branch $\bot$ | R3 on $b$ and $c$ gives $x_2 \equiv \bot$, $x_3 \equiv \top$; then R3 on $f$ gives $x_4 \equiv \top$ | $x_1, x_2 \equiv \bot$, $x_3, x_4 \equiv \top$ |
| 5 | L12 | keep what both branches derive | $x_1 \equiv x_2 \equiv \neg x_3$, $x_4 \equiv \top$ |

At level 0 the formula is already decided: EXTEND finds the model $x_1 = x_2 = x_4 = 1$, $x_3 = 0$ in step 2. Steps 3 to 5 show what 1-saturation would add. None of these facts follows from 0-saturation, and none is a single assignment, so a method that intersects only the assignments of the two branches, as a [lookahead](/lookahead-sat/) solver does, finds only $x_4 \equiv \top$, and [failed literal probing](/failed-literal-probing/) finds nothing, because no branch fails. Stålmarck's method finds the two equivalences as well, and they halve the search twice: after step 5 one free class $\{x_1, x_2, \neg x_3\}$ is left.

For an unsatisfiable case, take $(x_1 \vee x_2), (x_1 \vee \neg x_2), (\neg x_1 \vee x_3), (\neg x_1 \vee \neg x_3)$. 0-saturation derives nothing, and EXTEND at $k = 0$ returns FAIL, since both values of $x_1$ lead to a contradiction. At $k = 1$ the first dilemma, on $x_1$, makes both branches contradictory, so line L4 returns UNSAT with one dilemma. The hardness of this formula is 1.

## Correctness

The key invariant is that every model of $F$, extended to the nodes by their AND definitions, respects $E$. Each simple rule is a valid consequence of its triplet. The dilemma rule keeps only facts that hold in both branches, and every model lies in one branch. So a contradiction proves that $F$ is unsatisfiable. For the other direction, a consistent $k$-saturated relation with at most $k$ free classes of variables always has a model, by induction on $k$: one of the two branches of a free variable is consistent, it is $(k-1)$-saturated, and it has one free class fewer. So the loop of line L2 stops with $k$ at most the number of variables, and EXTEND only returns assignments that satisfy every clause. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the word RAM, with $s = |F|$, $t$ nodes and $|T| = s - m$ triplets. The implementation uses a disjoint-set forest without union by rank or path compression, so a find costs $O(t)$.

- **0-saturation.** A pass over $T$ costs $O(|T| \cdot t)$. Each pass except the last merges two classes, and there are at most $t$ classes, so $S_0 = O(|T| \, t^2)$.
- **$k$-saturation.** Each pass of the loop L7 to L13 except the last merges classes, so there are at most $t + 1$ passes. A pass makes at most $n$ dilemmas, and each costs $2 S_{k-1}$ plus $O(t^2)$ for the intersection. So $S_k \le (t + 1) \, n \, (2 S_{k-1} + O(t^2))$, which gives $S_k = O((2n(t+1))^k \, |T| \, t^2)$. For fixed $k$ this is a polynomial.
- **The whole run.** EXTEND at level $k$ makes at most $2n$ calls of SATURATE at level $k$. The bounds grow by a factor of at least $2n(t+1)$ per level, so the run is dominated by the last level $K$, and it costs $O(n \cdot S_K)$. The proof shows $K \le n$, so the worst case is $O(n (2nt)^n s t^2)$, and when $F$ is decided at level 0, the time is $O(n s t^2)$.
- **Space.** The recursion of line L11 is at most $K + 1 \le n + 1$ levels deep, and each level holds a constant number of relations of size $O(t)$. With the triplets and the clause roots, the extra space is $O(n t + m)$.

A production version uses union by rank and path compression and fires a rule only on the triplets of a class that just changed, which removes most of the factors of $t$. The exponent in $k$ stays: $k$-saturation is polynomial only for fixed $k$, so formulas of high hardness take time exponential in their hardness.

## Properties

- **Sound and complete.** UNSAT is returned only for unsatisfiable formulas, and a model is returned exactly for satisfiable ones.
- **Equivalences, not only units.** The relation $E$ records $a \equiv b$ and $a \equiv \neg b$ between any two nodes. Intersecting two branches can derive such equivalences when the branches derive no unit at all.
- **Breadth first in the proof.** The method never commits to a branch: after a dilemma both branches are dropped and only their common part stays. The depth of nesting, not the number of branches, measures how hard a formula is.
- **Deterministic and recursive.** The run is fixed by the variable order of line L10, and the recursion depth is $k$.

## Variants and improvements

- **Other triplet forms.** The tutorial uses implication triplets $x \leftrightarrow (y \to z)$ with the constant $\bot$, and other versions allow $\wedge$, $\leftrightarrow$ and $\oplus$ as connectives.
- **Dilemma on any node.** The dilemma rule may branch on any node, or on an equivalence $a \equiv b$ between two nodes, not only on a variable. This allows more branches, so it cannot raise the hardness of a formula.
- **Lookahead.** At depth 1 and restricted to units, the dilemma rule is the [lookahead](/lookahead-sat/) step on one variable: [failed literal probing](/failed-literal-probing/) handles the case of one contradictory branch, and the intersection of the two branches gives the literals that both values imply.
- **Equivalence reasoning in CDCL.** CDCL solvers find some equivalences of literals with [equivalent literal substitution](/equivalent-literal-substitution/) on the binary implication graph, a cheaper and weaker form of the same idea.
- **Model extension.** EXTEND is one way to get a model. A proof procedure needs none, and a combined solver can hand the saturated relation to a [DPLL](/dpll/) or [CDCL](/cdcl/) search.

## When to use it

Use Stålmarck's method for tautology checking on formulas with much structure and low hardness, such as many formulas of [equivalence checking](/equivalence-checking/) of circuits, where two copies of a circuit agree node by node. The equivalences it derives are exactly the facts that such proofs need. For random formulas or for formulas with high hardness, the bound grows as a polynomial of degree about $2k$ in the size, and [CDCL](/cdcl/) is the better choice. To compare whole functions of a few variables, a [BDD](/binary-decision-diagram/) is another option.

## Pitfalls

- **Union instead of intersection.** At line L12, `E ← E1 ∪ E0` derives $v \equiv \top$ and $v \equiv \bot$ from every dilemma, so it refutes every formula. The right line is `E ← E1 ∩ E0`: only facts true in both branches are true in general.
- **Giving up on one bad branch.** At line L11, `if E1 is contradictory then return UNSAT` is unsound; one branch says only that $v \equiv \bot$. The right rule treats a contradictory branch as the full relation, so that line L12 adopts the other branch.
- **Consistency taken as SAT.** After line L4, `if E is consistent then return SAT` is wrong: the unsatisfiable example above is consistent after 0-saturation. The right step is line L5, a model check by EXTEND, and if it fails, a higher $k$ at line L6.
- **One pass only.** If line L13 is dropped, so that each variable gets one dilemma, a fact found by a later dilemma cannot help an earlier one, and the result is not $k$-saturated. Then the completeness argument fails. The right loop repeats the pass until it adds nothing.
- **Reading equivalences without parity.** In the disjoint-set structure, $a \equiv b$ and $a \equiv \neg b$ put $a$ and $b$ in the same class. The intersection at line L12 must compare the parities as well as the roots, or it keeps false equivalences.

## Implementations

## History

Gunnar Stålmarck developed the method in Sweden in the late 1980s. He filed a Swedish patent application on 16 June 1989, and the US patent 5,276,897, *Method and system for computer-aided proving of tautologies*, was filed on 14 June 1990 and granted on 4 January 1994. The patent claims the triplet form, the simple rules and the dilemma rule. Sheeran and Stålmarck (2000) gave a tutorial account with the notions of saturation and hardness, and the method was applied to industrial verification problems, for example of railway interlocking systems.

## References
