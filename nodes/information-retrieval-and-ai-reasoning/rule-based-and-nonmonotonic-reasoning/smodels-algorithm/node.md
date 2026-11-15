---
tag: NCW1XZ
kind: algorithm
slug: smodels-algorithm
name: Smodels algorithm
aliases:
- Simons-Niemela-Soininen search
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: advanced
summary: Searches for stable models by branching on atoms and propagating with well-founded and lookahead reasoning, in the style of DPLL.
model: word-ram
complexity:
  vars: {n: the number of atoms, s: "the size of the program, the number of rules plus the number of literals"}
  time: {worst: "O(2^n · n^3 · s)"}
  space: {extra: "O(n + s)"}
properties: {deterministic: true}
history:
  year: 2002
  people: [Patrik Simons, Ilkka Niemelä, Timo Soininen]
  note: Simons, Niemelä and Soininen gave the journal account of the smodels search, with weight constraint rules, in 2002. The smodels system had been in use since the middle of the 1990s.
prereqs: [stable-model-semantics, well-founded-semantics, dpll, choice-rule]
see_also: [conflict-driven-answer-set-solving, answer-set-programming, answer-set-grounding, alternating-fixpoint, unit-propagation, loop-formulas, stable-model-np-completeness]
sources:
  - paper: doi:10.1016/s0004-3702(02)00187-x
    title: Patrik Simons, Ilkka Niemelä and Timo Soininen, Extending and implementing the stable model semantics, Artificial Intelligence 138(1-2), 181 to 234 (2002)
    locator: the procedures smodels, expand, atleast, atmost and lookahead, and the semantics of choice, cardinality and weight rules
  - paper: doi:10.1023/a:1018930122475
    title: Ilkka Niemelä, Logic programs with stable model semantics as a constraint programming paradigm, Annals of Mathematics and Artificial Intelligence 25(3-4), 241 to 273 (1999)
    locator: stable model search as constraint programming and the use of the smodels system
  - paper: "Michael Gelfond and Vladimir Lifschitz, The stable model semantics for logic programming, in Robert A. Kowalski and Kenneth A. Bowen (eds.), Logic Programming: Proceedings of the Fifth International Conference and Symposium, MIT Press, 1070 to 1080 (1988)"
    locator: the definition of stable models by the reduct
  - paper: doi:10.1145/116825.116838
    title: Allen Van Gelder, Kenneth A. Ross and John S. Schlipf, The well-founded semantics for general logic programs, Journal of the ACM 38(3), 620 to 650 (1991)
    locator: unfounded sets, which the upper closure of atmost removes
  - paper: doi:10.1016/0743-1066(84)90014-1
    title: William F. Dowling and Jean H. Gallier, Linear-time algorithms for testing the satisfiability of propositional Horn formulae, Journal of Logic Programming 1(3), 267 to 284 (1984)
    locator: the counter method behind the linear-time fixpoints
  - paper: doi:10.1016/j.artint.2004.04.004
    title: "Fangzhen Lin and Yuting Zhao, ASSAT: computing answer sets of a logic program by SAT solvers, Artificial Intelligence 157(1-2), 115 to 137 (2004)"
    locator: the completion given to a SAT solver, with loop formulas added for models that are not stable
---

The smodels algorithm finds the [stable models](/stable-model-semantics/) of a ground logic program by search. It works like [DPLL](/dpll/): it keeps a partial assignment of truth values to atoms, extends it by propagation, and branches on an open atom when propagation stops. The propagation has two parts. The first follows the rules forward and backward, much like [unit propagation](/unit-propagation/). The second computes an upper bound on the atoms that can still be derived, as in the [well-founded semantics](/well-founded-semantics/), and makes every other atom false. This second part is what separates stable models from the models of the [Clark completion](/clark-completion/).

## In plain words

You want to pick a set of facts that the rules justify, with no fact that only supports itself in a circle. Smodels guesses one fact at a time, true or false. After each guess it works out what must follow. A rule whose conditions all hold forces its conclusion. A fact with no rule left that could prove it must be false. A true fact with only one rule left that could prove it forces the conditions of that rule. Then it asks which facts could still be proved at all from the rules that are not blocked yet, and every other fact becomes false. If the guess leads to a contradiction, it tries the other value. Before it guesses, it also tests each open fact both ways, and a value that fails at once is never guessed.

## The problem

The input is a finite ground program $P$ over a set $A$ of $n$ atoms. Its rules are normal rules $h \leftarrow b_1, \ldots, b_m, \mathit{not}\ c_1, \ldots, \mathit{not}\ c_k$, [choice rules](/choice-rule/) $\{h_1, \ldots, h_j\} \leftarrow b_1, \ldots, \mathit{not}\ c_k$, and constraints $\leftarrow b_1, \ldots, \mathit{not}\ c_k$. The output is the set of stable models of $P$, or one of them, or the answer that there is none. The existence question is NP-complete for normal programs, by the [NP-completeness theorem](/stable-model-np-completeness/), so the search is exponential in the worst case. This is the propositional case: programs with variables are first [ground](/answer-set-grounding/).

## The algorithm

A partial assignment $a$ maps some atoms to true or false. A body is true under $a$ if every literal in it is true, false if some literal in it is false, and open otherwise. A rule is *live* if its body is not false.

```pseudo id=main
SMODELS(P, a)                       ▷ a is a partial assignment; returns the stable models that extend it
L1  try a ← LOOKAHEAD(P, EXPAND(P, a)) on conflict return ∅
L2  if a assigns every atom then return {the set of true atoms of a}
L3  x, v ← the open atom and value chosen by the heuristic
L4  return SMODELS(P, a ∪ {x ↦ v}) ∪ SMODELS(P, a ∪ {x ↦ ¬v})

EXPAND(P, a)
L5  repeat
L6      a ← ATLEAST(P, a)
L7      U ← the least set closed under: for each normal or choice rule r with no negative atom true in a
L8              and pos(r) ⊆ U, add each head h of r that is not false in a      ▷ the upper closure
L9      make every atom outside U false
L10 until a does not change
L11 return a

ATLEAST(P, a)                       ▷ repeat until no rule applies; a clash is a conflict
L12 R1: a normal rule with a true body makes its head true
L13 R2: an atom that is the head of no live rule becomes false
L14 R3: a true atom with exactly one live rule makes every literal of that body true
L15 R4: a constraint, or a normal rule with a false head, must not get a true body:
L16     if all its literals but one are true, make the last one false

LOOKAHEAD(P, a)
L17 for each open atom x and each value v do
L18     if EXPAND(P, a ∪ {x ↦ v}) gives a conflict then
L19         a ← EXPAND(P, a ∪ {x ↦ ¬v}) and restart the loop at L17
L20 return a
```

Lines L7 to L9 are the ATMOST step. In the real system, ATLEAST and ATMOST keep a counter per rule and a queue, so each runs in time linear in the size of the program. The heuristic at line L3 uses the sizes that LOOKAHEAD computes: the Python code branches on the atom whose two expansions assign the most atoms in the worse case, and tries first the value with the larger expansion.

## Example

Take the program

$$p \leftarrow \mathit{not}\ q. \quad q \leftarrow \mathit{not}\ p. \quad r \leftarrow p. \quad r \leftarrow s. \quad s \leftarrow r. \quad \leftarrow \mathit{not}\ r.$$

Its completion has two models, $\{p, r, s\}$ and $\{q, r, s\}$. In the second one, $r$ and $s$ support only each other. The only stable model is $\{p, r, s\}$.

| step | rule | assignment |
|---|---|---|
| EXPAND at the root | R4 on the constraint: its one literal $\mathit{not}\ r$ must be false | $r$ true |
| | R1 on $s \leftarrow r$ | $s$ true |
| | ATMOST: the upper closure is $\{p, q, r, s\}$, no change | $\{r, s\}$ true, $p, q$ open |
| LOOKAHEAD, try $p$ false | R4 on $p \leftarrow \mathit{not}\ q$: the head is false, so $\mathit{not}\ q$ must be false | $q$ true |
| | ATMOST: $r \leftarrow p$ is blocked, and $r$, $s$ need each other, so the upper closure is $\{q\}$ | $r$ false, but $r$ is true: conflict |
| LOOKAHEAD fixes $p$ true | R2: $q \leftarrow \mathit{not}\ p$ is no longer live | $q$ false |
| L2 | every atom is assigned | return $\{p, r, s\}$ |

The search visits one node and makes no guess. Without LOOKAHEAD, the code branches on $p$, finds the model on the true branch and a conflict on the false branch: three nodes and one conflict. The rules R1 to R4 alone cannot see the conflict, because $q, r, s$ true and $p$ false is a model of the completion. Only the upper closure finds it.

## Correctness

The [correctness proof](proofs/correctness.md) has the details. Every step keeps every stable model $M$ that agrees with the current assignment. R1 and R4 hold because $M$ is a model of $P$. R2 and R3 hold because each atom of $M$ is the head of a rule whose body $M$ satisfies. ATMOST holds because $M$ is the least model of its reduct, and each stage of that least model lies inside the upper closure. LOOKAHEAD only fixes a value whose opposite leads to a conflict. Conversely, at a total assignment with no conflict, R1 makes the set $M$ of true atoms a model of the reduct $P^M$, and ATMOST makes $M$ a subset of the least model of $P^M$, so $M$ is stable. Branching on both values of an atom covers every stable model exactly once.

## Complexity

Let $s$ be the number of rules plus the number of literals. With counters, ATLEAST and ATMOST take $O(s)$ time, so EXPAND takes $O(n \cdot s)$: each round but the last assigns an atom. LOOKAHEAD runs at most $2n$ expansions for each of at most $n$ atoms that it fixes, which gives $O(n^3 \cdot s)$ per node. The search tree has at most $2^n$ leaves, so the worst-case time is $O(2^n \cdot n^3 \cdot s)$. With a trail of assignments that is undone on backtracking, the extra space is $O(n + s)$. The Python code copies the assignment at each node and recomputes each fixpoint by repeated scans, which costs an extra factor $n$ in time and $O(n^2)$ space for the copies. No algorithm is expected to avoid the exponential factor, since the problem is NP-complete.

## Properties

- **Complete and sound.** It returns every stable model and nothing else, and it can stop after the first one.
- **Stronger than completion.** The upper closure removes every atom outside the least model of the reduct. On a [tight](/fages-theorem/) program this adds nothing; on a program with positive loops it is necessary.
- **Contains the well-founded model.** At the root, before any guess, EXPAND makes every atom that is true in the well-founded model true and every atom that is false in it false, since ATMOST removes unfounded atoms and R1 derives the rest.
- **No learning.** The search backtracks chronologically and forgets why a branch failed.

## Variants and improvements

- **Weight constraint rules.** Simons, Niemelä and Soininen (2002) extend the same four rules and the upper closure to cardinality and weight constraints, so that a rule such as $1 \{a, b, c\}\ 2$ is handled directly and not through a translation.
- **Conflict-driven learning.** [Conflict-driven answer set solving](/conflict-driven-answer-set-solving/) keeps the same two propagators, written as nogoods of the completion and loop nogoods, and adds clause learning and backjumping.
- **SAT-based solvers.** Lin and Zhao (2004) give the completion to a SAT solver and add [loop formulas](/loop-formulas/) for each model that is not stable.
- **Disjunctive programs.** For [disjunctive programs](/disjunctive-logic-program/) the same kind of search needs an extra minimality check at each candidate, which is a coNP problem.

## When to use it

Use smodels-style search to understand or to teach stable model solvers, or when a small, simple solver for ground programs is enough. The algorithm shows clearly which propagation does what. For hard instances, conflict-driven solvers are usually much faster, because they learn from failed branches.

## Pitfalls

- **Forgetting ATMOST.** Without the upper closure, the search accepts supported models of positive loops. For $p \leftarrow q$, $q \leftarrow p$ it would return $\{p, q\}$, which is not stable.
- **Choice heads in R1.** A choice rule with a true body does not force its heads; R1 applies only to normal rules. A choice rule is live for R2 and R3, and it adds its heads to the upper closure.
- **Atoms that occur only in bodies.** They have no rule, so R2 must make them false at the start. If the set of atoms is taken from the heads only, they stay open forever.
- **Cost of lookahead.** LOOKAHEAD runs up to $2n$ expansions per fixed atom, and on easy programs it can cost more than the search it saves.
- **Constraints do not derive atoms.** The constraint $\leftarrow \mathit{not}\ r$ makes $r$ true in the assignment, but $r$ must still be derived by a rule in the end, or ATMOST reports a conflict.

## Implementations

## History

Niemelä and Simons wrote the smodels system in the middle of the 1990s. Niemelä (1999) argued that logic programs with stable models are a constraint programming language and used smodels as the main example. Simons, Niemelä and Soininen (2002) published the full algorithm with weight constraint rules and its proofs. The approach set the pattern for the first generation of answer set solvers, and its propagators survive in the conflict-driven solvers that replaced it.

## References
