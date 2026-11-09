---
tag: FSZY2A
kind: concept
slug: autarky
name: Autarky
aliases:
- autark assignment
- lean kernel
- autarky reduction
area: logic-and-constraints/sat-solving
level: advanced
summary: Partial assignment that satisfies every clause it touches; removing those clauses keeps satisfiability, and the clauses no autarky touches form the lean kernel.
prereqs: [clause, conjunctive-normal-form, sat]
see_also: [minimal-unsatisfiable-subset, pure-literal-elimination, blocked-clause-elimination, 2-sat, backbone, minimal-correction-subset]
sources:
  - paper: doi:10.1016/0166-218X(85)90050-2
    title: Burkhard Monien and Ewald Speckenmeyer, Solving satisfiability in less than 2^n steps, Discrete Applied Mathematics 10(3), 1985, 287-295
    locator: autark assignments and their use in a branching algorithm for k-SAT
  - book: isbn:9781643681603
    title: Biere, Heule, van Maaren and Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 14 (Kleine Büning and Kullmann, Minimal Unsatisfiability and Autarkies), the sections on autarkies, the lean kernel, and polynomial-time autarky classes
  - paper: "Oliver Kullmann, Lean clause-sets: generalizations of minimally unsatisfiable clause-sets, Discrete Applied Mathematics 130(2), 2003, pages 209 to 249"
    title: Lean clause-sets
    locator: lean clause-sets, the lean kernel as the result of autarky reduction, and the coNP-completeness of leanness
  - paper: "Mark H. Liffiton and Karem A. Sakallah, Searching for autarkies to trim unsatisfiable clause sets, SAT 2008, LNCS 4996, pages 182 to 195"
    title: Searching for autarkies to trim unsatisfiable clause sets
    locator: the reduction of autarky search to SAT with two variables per original variable, and its use before MUS extraction
---

An autarky for a [CNF](/conjunctive-normal-form/) formula $F$ is a partial assignment $\alpha$ such that every clause of $F$ that contains a variable set by $\alpha$ is satisfied by $\alpha$. The clauses that $\alpha$ touches can then be removed without changing whether $F$ is satisfiable, because $\alpha$ looks after them and does not affect the rest. A satisfying assignment is an autarky, and so is a pure literal. Monien and Speckenmeyer introduced autarkies in 1985 for a branching algorithm for $k$-SAT. Autarkies are closed under composition, so every formula has a largest set of clauses that some autarky satisfies; what is left is the **lean kernel**. Every [minimal unsatisfiable subset](/minimal-unsatisfiable-subset/) lies inside the lean kernel, which makes autarky reduction a useful first step for core extraction.

## In plain words

Think of a group of variables that can settle their own affairs. You choose values for them, and every clause that mentions any of them is then satisfied. The clauses that do not mention them are untouched. So the chosen variables cause no problems and solve all the clauses they meet.

You can set such a group aside together with all the clauses it satisfies. If the rest of the formula has a solution, add the group's values to get a solution of the whole. If the rest has no solution, neither has the whole. Doing this again and again leaves a core part on which no such group exists, and every source of contradiction lives in that core.

## The idea

Notation: $F$ has $n$ variables, $m$ clauses and $|F|$ literal occurrences. A partial assignment $\alpha$ **touches** a clause $C$ if it sets some variable of $C$. $F_\alpha$ is the set of clauses of $F$ that $\alpha$ does not touch.

**Definition.** $\alpha$ is an autarky for $F$ if $\alpha$ satisfies every clause of $F$ that it touches. It is non-trivial if it touches some clause.

**Theorem 1 (Monien and Speckenmeyer).** If $\alpha$ is an autarky for $F$, then $F$ is satisfiable if and only if $F_\alpha$ is.

*Proof.* $F_\alpha \subseteq F$, so a model of $F$ satisfies $F_\alpha$. Let $\beta$ be a model of $F_\alpha$ and let $\gamma$ agree with $\alpha$ on the variables of $\alpha$ and with $\beta$ elsewhere. A clause touched by $\alpha$ is satisfied by $\alpha$, hence by $\gamma$. A clause of $F_\alpha$ has no variable of $\alpha$, so $\gamma$ agrees with $\beta$ on it and satisfies it. $\blacksquare$

**Lemma 2 (subsets and composition).** (a) An autarky for $F$ is an autarky for every $G \subseteq F$. (b) If $\alpha$ is an autarky for $F$ and $\beta$ is an autarky for $F_\alpha$ that sets only variables of $F_\alpha$, then $\alpha \cup \beta$ is an autarky for $F$.

*Proof.* (a) The condition is a "for every touched clause" over fewer clauses. (b) $\alpha$ and $\beta$ set disjoint variables, because $F_\alpha$ has none of $\alpha$'s. A clause touched by $\alpha$ is satisfied by $\alpha$; any other touched clause is in $F_\alpha$ and touched by $\beta$, so $\beta$ satisfies it. $\square$

By (b) and (a), applying autarkies until none is left gives the same set of remaining clauses in every order: the clauses that no autarky of $F$ touches. This set is the lean kernel $N(F)$, and $F$ is **lean** if $N(F) = F$, that is, if $F$ has no non-trivial autarky. If $F$ is satisfiable, a total model is an autarky, so $N(F)$ is empty. If $F$ is unsatisfiable, $N(F)$ is unsatisfiable by Theorem 1.

**Theorem 3.** Every minimal unsatisfiable subset $M$ of $F$ is contained in $N(F)$.

*Proof.* Let $\alpha$ be an autarky of $F$ that touches a clause of $M$. By Lemma 2(a) it is an autarky for $M$, so by Theorem 1 the set $M_\alpha$ is unsatisfiable. But $M_\alpha$ is a proper subset of $M$, against minimality. $\blacksquare$

The inclusion can be strict. The formula $(x_2), (\neg x_2), (x_1 \vee x_2), (\neg x_1 \vee \neg x_2)$ is lean: an autarky that sets $x_1$ must satisfy both of the last two clauses, so it sets $x_2$ and then falsifies $(x_2)$ or $(\neg x_2)$. But its only minimal unsatisfiable subset is $\{(x_2), (\neg x_2)\}$.

**Finding autarkies by SAT.** For each variable $x$ use two new variables, $t_x$ ("$x$ is set true") and $f_x$ ("$x$ is set false"). For a literal $l$ of $x$ write $\mathrm{true}(l)$ for $t_x$ if $l = x$ and $f_x$ if $l = \neg x$, and $\mathrm{false}(l)$ for the other one.

```pseudo id=main
FIND-AUTARKY(F)
L1  for each variable x of F: add (¬t_x ∨ ¬f_x)               ▷ not both values
L2  for each clause C of F and each literal l ∈ C do
L3      add (¬false(l) ∨ ⋁_{l' ∈ C} true(l'))                 ▷ touched by a false literal ⇒ satisfied
L4  add ⋁ true(l) over all literals l of F                     ▷ some clause is satisfied
L5  solve the new formula E; if E is unsatisfiable then return NONE
L6  return α with α(x) = 1 if t_x, α(x) = 0 if f_x, x unset otherwise

LEAN-KERNEL(F)
L7  while α ← FIND-AUTARKY(F) is not NONE do
L8      F ← F_α
L9  return F
```

A model of $E$ gives exactly an autarky that satisfies some clause: a touched clause is touched by a true literal (then it is satisfied) or by a false one (then line L3 makes it satisfied). $E$ has $2n$ variables and $n + |F| + 1$ clauses. LEAN-KERNEL makes at most $m + 1$ SAT calls, because each round removes a clause. Deciding whether $F$ is lean is coNP-complete (Kullmann 2003), so no polynomial algorithm is expected in general.

## Examples

**An autarky next to a contradiction.** Let
$$F = (x_1 \vee x_2),\ (\neg x_1 \vee x_2),\ (x_1 \vee \neg x_2),\ (\neg x_1 \vee \neg x_2),\ (x_2 \vee x_3 \vee x_4),\ (\neg x_3 \vee x_4),\ (\neg x_4 \vee x_5).$$
The assignment $\{x_4 = 1, x_5 = 1\}$ touches the last three clauses and satisfies all of them, so it is an autarky. The first four clauses are unsatisfiable and lean, so $N(F)$ is these four clauses, which are also the only minimal unsatisfiable subset.

**Non-example.** $\{x_4 = 1\}$ alone is not an autarky: it touches $(\neg x_4 \vee x_5)$ and does not satisfy it.

**Pure literals.** If $\neg l$ occurs in no clause, then $\{l\}$ is an autarky. [Pure literal elimination](/pure-literal-elimination/) is autarky reduction with these small autarkies.

**2-CNF.** If $F$ has only binary clauses and unit propagation from a literal $l$ ends without a conflict, the propagated assignment is an autarky: a touched clause has a literal set false, and then unit propagation set its other literal true. This is the step behind the [2-SAT](/2-sat/) algorithm of Even, Itai and Shamir.

**Satisfiable formulas.** For a satisfiable $F$ the lean kernel is empty, and a model is the largest autarky.

## Where it is used

- **Exponential-time SAT algorithms.** Monien and Speckenmeyer branch on the literals of a shortest clause. When the assignment of a branch is an autarky, they take that branch alone, which bounds the branching and gives a running time below $2^n$ for 3-SAT.
- **MUS extraction.** By Theorem 3, removing the clauses outside the lean kernel never removes a clause of a [minimal unsatisfiable subset](/minimal-unsatisfiable-subset/). Liffiton and Sakallah use autarky search to shrink formulas before computing cores and [minimal correction subsets](/minimal-correction-subset/).
- **Theory of minimal unsatisfiability.** Kleine Büning and Kullmann study classes of lean and minimally unsatisfiable formulas, such as those of small deficiency $m - n$, through autarkies.
- **Polynomial autarky classes.** Matching autarkies (found by bipartite matching) and linear autarkies (found by linear programming) are restricted kinds that can be found in polynomial time, and they give preprocessing steps with guaranteed cost.
- **Preprocessing.** Pure literals, blocked clauses with a pure blocking literal, and satisfied components of the formula are all autarky reductions; see [blocked clause elimination](/blocked-clause-elimination/).

## References
