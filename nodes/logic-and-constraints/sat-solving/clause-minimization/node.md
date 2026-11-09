---
tag: Y6TCQW
kind: technique
slug: clause-minimization
name: Learned clause minimization
aliases:
- recursive clause minimization
- conflict clause minimization
area: logic-and-constraints/sat-solving
level: advanced
summary: "Remove from a first-UIP learned clause every literal whose value follows, through reason clauses, from the other literals of the clause. The result is shorter, still implied and still asserting."
prereqs: [clause-learning, first-uip, implication-graph]
see_also: [cdcl, literal-block-distance, unit-propagation, binary-resolution, depth-first-search, drat-proof, clause-subsumption]
sources:
  - paper: doi:10.1007/978-3-642-02777-2_23
    title: Niklas Sörensson and Armin Biere, Minimizing learned clauses, Theory and Applications of Satisfiability Testing (SAT 2009), Lecture Notes in Computer Science 5584, 2009
    locator: pages 237 to 243 (local and recursive minimization of learned clauses, and their use in MiniSat since version 1.13)
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 4, Conflict-Driven Clause Learning SAT Solvers, by Marques-Silva, Lynce and Malik (conflict clause minimization)
  - paper: doi:10.1007/978-3-540-24605-3_37
    title: Niklas Eén and Niklas Sörensson, An extensible SAT-solver, SAT 2003, Lecture Notes in Computer Science 2919, 2004
    locator: pages 502 to 518 (conflict analysis, the reason clauses and the trail on which minimization works)
---

Learned clause minimization is the step of [conflict analysis](/clause-learning/) that removes from the [first-UIP clause](/first-uip/) $C$ every literal whose value is implied, through the reason clauses of the [implication graph](/implication-graph/), by the other literals of $C$ and by level 0. The recursive form, by Sörensson and Biere, follows reasons to any depth with a [depth-first search](/depth-first-search/). It never removes the asserting literal, the result is still implied by the formula, and, as proved below, it keeps at least one literal of every decision level of $C$, so the backjump level and the [LBD](/literal-block-distance/) do not change. It shortens the clause only, which makes propagation with the clause cheaper and the clause stronger.

## In plain words

When the solver explains a dead end, the explanation is a list of facts that cannot all be true. Some facts in this list may be there only because other facts in the same list already force them. Such a fact adds nothing: if the others hold, it holds too.

Minimization goes through the list and asks, for each fact: can I get this fact back from the other facts in the list, by following the chain of reasons that forced it? If every chain ends in facts that are already in the list, or in facts that are always true, the fact can go. If some chain ends in a free guess that is not in the list, the fact must stay. The one fact from the last guess, which makes the explanation useful, always stays.

## When it applies

- A CDCL solver has just learned the first-UIP clause $C$, with asserting literal $u$ at the conflict level $d$, and the trail with all its reasons is still in place.
- The solver propagates to a fixpoint before each decision and backjumps to the asserting level, as standard CDCL does. The level facts proved below need this; the soundness facts do not.
- Each literal on the trail has its reason clause at hand. A decision has none, and a decision literal is never removed.

## The template

The literals of $C$ are false on the trail; for a literal $\ell$, write $\bar\ell$ for its true complement and $\mathrm{reason}(\ell)$ for the reason clause of $\bar\ell$.

```pseudo id=main
MINIMIZE(C)                                       ▷ C: first-UIP clause, u = C[0] asserting
L1  mark the variables of the literals of C other than u
L2  Λ ← the set of levels of the literals of C other than u
L3  M ← [u]
L4  for each literal ℓ of C other than u do
L5      if ℓ is a decision or not REDUNDANT(ℓ) then append ℓ to M
L6  unmark all variables
L7  return M

REDUNDANT(ℓ)                                      ▷ hole DEPTH: follow reasons to any depth
L8  S ← [var(ℓ)]; N ← []                           ▷ N: variables marked by this call
L9  while S is not empty do
L10     v ← pop S
L11     for each literal r of the reason of v, other than the one on v do
L12         if var(r) is marked or level(var(r)) = 0 then continue
L13         if var(r) is a decision or level(var(r)) ∉ Λ then   ▷ hole FILTER
L14             unmark every variable of N; return false        ▷ hole CACHE
L15         mark var(r); append var(r) to N and to S
L16 return true                                   ▷ the marks of N stay: these variables are implied
```

The holes:

- **DEPTH.** Recursive minimization follows reasons to any depth, as written. Local minimization looks at one reason only: $\ell$ goes if every other literal of $\mathrm{reason}(\ell)$ is marked or at level 0.
- **FILTER.** The test $\mathrm{level} \notin \Lambda$ stops a search that cannot succeed (Fact 3 below). MiniSat keeps $\Lambda$ as a 32-bit mask of the levels modulo 32, which can only let more searches go on, never stop a good one.
- **CACHE.** A successful search keeps its marks, so later searches stop at these variables. Many solvers also keep a "failed" mark for the variables of a failed search, so that no search expands a variable twice.

**Correctness.** Let $F$ be the formula, $\Delta$ the learned clauses, and $M$ the result. Call a variable *removable* if it is a removed literal of $C$ or it was marked by a successful call of REDUNDANT. For each removable variable, every other literal of its reason is at level 0, marked by L1, or removable, and is assigned before it on the trail.

*Lemma 1 (propagation is complete below the current level).* In CDCL that propagates to a fixpoint before each decision and backjumps to the asserting level, for every level $k$ below the current one, no clause of the database is unit or false under the part of the trail at levels $\le k$. *Proof.* A level is complete when the next decision is made, and propagation was at a fixpoint then. Later steps only add literals at higher levels, or backjump, which removes whole levels. A clause learned with backjump level $b$ has its asserting literal and a literal at level $b$, both unassigned under every prefix of level $k < b$, so it is neither unit nor false there; under the prefix of level $b$, it is propagated before level $b$ is complete. Deleted clauses play no role. $\blacksquare$

*Fact 1 (the first literal of each level stays).* Fix a level $\lambda \ge 1$. Let $S_\lambda$ be the set of variables at level $\lambda$ that are either the variable of a literal of $C$ other than $u$, or removable. If $S_\lambda$ is not empty, its earliest variable $x$ on the trail is a kept literal of $C$. *Proof.* Suppose $x$ is removable. Every other literal of its reason is at level 0 or is a variable of $C$ or is removable, and is assigned before $x$. Such a literal at level $\lambda$ would be in $S_\lambda$ and earlier than $x$, so none is at level $\lambda$, and all are at levels below $\lambda$. Then the reason of $x$ is unit under the trail prefix of level $\lambda - 1$, where $x$ is unassigned, which Lemma 1 forbids, since $\lambda - 1$ is below the current level. $\blacksquare$

*Fact 2 (the asserting literal stays, and the levels do not change).* Line L4 never tests $u$, but more holds: no variable at the conflict level $d$ is ever removable. $C$ has no literal at level $d$ other than $u$, whose variable L1 does not mark, so a removable variable at level $d$ would make $S_d$ nonempty with no kept literal of $C$ in it, against Fact 1. Also by Fact 1, for every level of a literal of $C$ other than $u$, a literal of that level is kept. So $M$ has exactly the levels of $C$: it contains $u$ as its only literal at level $d$, so it is asserting, and its backjump level and its LBD equal those of $C$.

*Fact 3 (the filter loses nothing).* By Fact 1, every removable variable is at a level in $\Lambda$. A search that reaches an unmarked variable with level outside $\Lambda$ can succeed only if that variable becomes removable, which is impossible; so line L13 only ends searches that would fail.

*Fact 4 (implied).* $F \wedge \Delta \models M$, and so $F \models M$. *Proof.* Take an assignment $\alpha$ that satisfies $F \wedge \Delta$ and makes $M$ false. By induction along the trail, $\alpha$ gives every removable variable its trail value: each other literal of its reason is in $M$, so false under $\alpha$ as on the trail; or at level 0, and the level-0 literals follow from $F \wedge \Delta$ by unit propagation, so $\alpha$ agrees; or removable and earlier, so by induction $\alpha$ agrees. So all these literals are false under $\alpha$. The reason clause is in $F \wedge \Delta$, so $\alpha$ satisfies it, and $\alpha$ must give the removable variable its trail value. In particular every removed literal of $C$ is false under $\alpha$, so $C$ is false under $\alpha$. But $C$ is implied by $F \wedge \Delta$, a contradiction. $\blacksquare$

The same induction, read as unit propagation, shows more: setting all literals of $M$ false and propagating with the reason clauses makes all of $C$ false, and the first-UIP clause then leads to a conflict by propagation. So $M$ has the reverse unit propagation property, and a [DRAT](/drat-proof/) checker accepts it as a lemma directly.

**Cost.** A successful search keeps its marks, so each variable is expanded by at most one successful search per conflict. A failed search unmarks its variables, so without a failed mark the same work can be repeated from each literal of $C$, which gives a bound of $|C|$ times the size of the part of the implication graph below $C$. With both marks, each variable is expanded at most once, and the time is linear in the sizes of the reason clauses visited. The explicit stack avoids deep recursion.

**Example.** Take the clauses $(\neg x_1 \vee x_5)$, $(\neg x_5 \vee x_2)$, $(\neg x_4 \vee \neg x_1 \vee x_6)$, $(\neg x_4 \vee \neg x_2 \vee \neg x_3 \vee x_7)$ and $(\neg x_6 \vee \neg x_7)$, and the decisions $x_1$, $x_3$, $x_4$ at levels 1, 2 and 3.

| level | trail | reason |
|---|---|---|
| 1 | $x_1$ | decision |
| 1 | $x_5$ | $(\neg x_1 \vee x_5)$ |
| 1 | $x_2$ | $(\neg x_5 \vee x_2)$ |
| 2 | $x_3$ | decision |
| 3 | $x_4$ | decision |
| 3 | $x_6$ | $(\neg x_4 \vee \neg x_1 \vee x_6)$ |
| 3 | $x_7$ | $(\neg x_4 \vee \neg x_2 \vee \neg x_3 \vee x_7)$ |

The clause $(\neg x_6 \vee \neg x_7)$ is false. Resolving with the reasons of $x_7$ and $x_6$ gives the first-UIP clause $C = (\neg x_4 \vee \neg x_1 \vee \neg x_2 \vee \neg x_3)$, with asserting literal $\neg x_4$. Minimization marks $x_1$, $x_2$, $x_3$ and $\Lambda = \{1, 2\}$. The literal $\neg x_1$ is a decision and stays, and so does $\neg x_3$. For $\neg x_2$, the reason $(\neg x_5 \vee x_2)$ leads to $x_5$, which is unmarked, at level $1 \in \Lambda$, and not a decision; it is marked, and its reason $(\neg x_1 \vee x_5)$ leads to $x_1$, which is marked. The search succeeds, and $M = (\neg x_4 \vee \neg x_1 \vee \neg x_3)$. Local minimization keeps $\neg x_2$, because $x_5$ is not in $C$. Both clauses have levels $\{3, 1, 2\}$, LBD 3 and backjump level 2.

On larger formulas, with the Python code of the [CDCL](/cdcl/) page and Luby restarts, the first-UIP clauses had the following total numbers of literals before and after minimization.

| formula | conflicts | literals in first-UIP clauses | after local | after recursive |
|---|---|---|---|---|
| random 3-CNF, 150 variables, 639 clauses, unsatisfiable | 3986 | 45080 | 36968 | 34456 |
| pigeonhole, 8 pigeons, 7 holes | 2964 | 52893 | 47755 | 44695 |

## Classic examples

- **MiniSat.** Sörensson and Biere report that MiniSat has used minimization since version 1.13. MiniSat implements the recursive form with a mask of levels and keeps the marks of successful searches, as in the template.
- **Proof logging.** Because the minimized clause has the reverse unit propagation property, solvers that write DRAT proofs log $M$ directly, with no extra steps.
- **Every modern CDCL solver.** Recursive minimization is a standard part of conflict analysis in the solvers that followed MiniSat.

## Variations

- **Local minimization.** One level of reasons only, as in the DEPTH hole. It is cheaper per literal and removes fewer literals; in the table above, it removed between about 60 and 80 percent as many as the recursive form.
- **Binary implication minimization.** If the database has a binary clause $(u \vee \neg\ell)$ for a literal $\ell$ of $M$, then $\ell$ can go, since [resolving](/binary-resolution/) $M$ with this clause on $\ell$ gives $M$ without $\ell$. This step is not a special case of the template, because it uses clauses that are not reasons, and it can remove a whole level.
- **Shrinking.** Replace all literals of one level by a single literal of that level that dominates them, a UIP of that level, in the sense of the [dominator tree](/dominator-tree/). Unlike the template, this can add a literal that is not in $C$.
- **Vivification of learned clauses.** Assign the complements of some literals of the clause, propagate, and drop literals that become false or implied; this uses the whole database and costs more.

## Pitfalls

- **Order of literals.** After minimization, keep $u$ first and put a literal of the backjump level second, so that the two watches are right after the backjump.
- **Not unmarking after a failed search.** A variable left marked by a failed search counts as implied in later searches and can remove a literal that must stay; the clause is then no longer implied.
- **Reasons that changed.** Minimization must run before the backjump, while the trail and the reasons are intact.
- **Chronological backtracking.** With solvers that backtrack chronologically, or that leave literals at lower levels than their implications, Lemma 1 fails. Minimization stays sound by Fact 4, but it may then remove a whole level, so compute the backjump level and the LBD after it.
- **Deep recursion.** A recursive implementation can overflow the call stack on long chains of reasons; use an explicit stack.

## Exercises

1. Give a formula and a trail on which recursive minimization removes a literal that local minimization keeps, with a chain of reasons of length 3.
2. Show that $M$ can be derived from $C$ by a sequence of resolution steps with reason clauses, each of which removes one literal, and bound the number of steps.
3. Show that the order of the literals tested in line L4 does not change $M$.
4. Construct a family of conflicts on which, without failure marks, REDUNDANT takes time quadratic in the length of the trail.

## References
