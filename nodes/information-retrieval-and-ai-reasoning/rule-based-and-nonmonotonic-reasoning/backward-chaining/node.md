---
tag: 3214H5
kind: algorithm
slug: backward-chaining
name: Backward chaining
aliases:
- goal-driven inference
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: intro
summary: Start from the goal, pick a rule that concludes it, and prove the conditions of that rule as subgoals in the same way, depth first, until every subgoal is a known fact.
solves: [horn-sat]
model: word-ram
complexity:
  vars: {n: the number of atoms, s: the total number of atom occurrences in the rules}
  time: {worst: O(s^(n+1)), best: O(1)}
  space: {extra: O(n)}
properties: {deterministic: true}
history:
  year: 1976
  people: [Edward H. Shortliffe]
  note: MYCIN, the medical consultation program of Shortliffe's thesis, chained backward from the goal of naming the organism of an infection and asked the user for the facts that no rule concluded. Goal-directed rule search in logic is older and has no single inventor.
prereqs: [horn-clause, depth-first-search]
see_also: [forward-chaining, sld-resolution, slg-resolution, horn-sat-forward-chaining, production-system, certainty-factors, negation-as-failure, magic-sets]
sources:
  - book: isbn:9780136042594
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, third edition, Prentice Hall (2010)
    locator: Chapter 7 (backward chaining for propositional definite clauses) and Chapter 9 (backward chaining with variables and logic programming)
  - book: isbn:9780201101720
    title: Bruce G. Buchanan and Edward H. Shortliffe (eds.), Rule-Based Expert Systems, The MYCIN Experiments of the Stanford Heuristic Programming Project, Addison-Wesley (1984)
    locator: the chapters on the MYCIN consultation program and its goal-directed control
  - book: isbn:9783540181996
    title: John W. Lloyd, Foundations of Logic Programming, second edition, Springer (1987)
    locator: the chapters on SLD resolution, the least Herbrand model and the soundness and completeness of SLD resolution
---

Backward chaining is the inference method of goal-driven rule systems. To prove a goal, it picks a rule whose conclusion is the goal and proves the conditions of the rule as new goals, depth first and from left to right, until each open goal is a known fact. This page treats it as the control method of rule-based expert systems such as MYCIN, on propositional rules: it adds a loop check on the goal stack and memo tables for proved and failed goals, and it shows the cost of the search. With variables and unification the same search is [SLD resolution](/sld-resolution/), the proof procedure of Prolog, and the page on it gives the first-order theory. The propositional decision problem itself is [Horn-SAT](/horn-sat/), which [forward chaining](/forward-chaining/) solves in linear time.

## In plain words

You want to know one thing, and you have rules of the form "if these things are true, then that thing is true". Look for a rule whose "then" part is the thing you want. Its "if" parts become new questions, and you answer each of them the same way. A question that is a known fact is answered at once. If a rule fails, try the next rule for the same question. Keep a list of the questions that you are working on now. If a question comes back while you are still working on it, do not start it again, or you go around in a circle forever. Write down the answers you found, so that you do not do the same work twice.

## The problem

The input is a finite set $P$ of propositional definite rules $a \leftarrow b_1, \ldots, b_m$, where a fact is a rule with $m = 0$, and a goal atom $g$. The semantics is the least model $M$ of $P$: the least set of atoms that contains the head of each rule whose body atoms it contains, or $M = \bigcup_k T_P^k(\emptyset)$ for the immediate consequence operator $T_P$. The task is to decide whether $g \in M$, which is the same as deciding that the [Horn clause](/horn-clause/) set $P \cup \{\leftarrow g\}$ is unsatisfiable. This is a P-complete problem that has a linear-time algorithm; backward chaining is chosen for its focus on the goal, not for its worst case.

## The algorithm

The procedure is [depth-first search](/depth-first-search/) over the rules. $S$ is the stack of goals that are open now, and $\mathrm{depth}(x)$ is the position of $x$ on $S$, from $0$ at the bottom. A call returns a truth value and $\mathit{low}$, the smallest depth of a stack atom that a loop check met during the call, or $\infty$.

```pseudo id=main
BACKWARD-CHAIN(P, g)
L1  proved ← ∅, failed ← ∅, S ← an empty stack
L2  return the truth value of PROVE(g)

PROVE(a)
L3  if a ∈ proved then return (true, ∞)
L4  if a ∈ failed then return (false, ∞)
L5  if a is on S at depth d then return (false, d)            ▷ loop check
L6  k ← the size of S; push a on S; low ← ∞
L7  for each rule a ← b_1, …, b_m of P, in order do
L8      for j ← 1 to m do
L9          (ok, c) ← PROVE(b_j); low ← min(low, c)
L10         if not ok then continue with the next rule at L7
L11     pop a from S; add a to proved; return (true, ∞)
L12 pop a from S
L13 if low ≥ k then add a to failed; return (false, ∞)       ▷ the failure did not use the stack below a
L14 return (false, low)                                      ▷ the failure used a goal below a: do not store it
```

Line L13 stores a failure only when no loop check below $a$ hit a goal that was open before $a$. A failure that line L14 reports depends on the current stack: the same atom can be provable when it is asked from another place. MYCIN added one more case to line L7: when no rule concludes a goal that is marked *askable*, ask the user.

## Example

The rules, in this order, are $g \leftarrow d$, $d \leftarrow d$, $g \leftarrow a, b$, $a \leftarrow g$, $a \leftarrow c$, $b \leftarrow a$, and the fact $c$.

| step | call | stack before the call | what happens |
|---|---|---|---|
| 1 | PROVE$(g)$ | empty | push $g$ at depth 0, try $g \leftarrow d$ |
| 2 | PROVE$(d)$ | $g$ | push $d$ at depth 1, try $d \leftarrow d$ |
| 3 | PROVE$(d)$ | $g, d$ | loop check: $d$ is at depth 1, return (false, 1) |
| 4 | back in $d$ | $g$ | no rule left, $\mathit{low} = 1 \ge 1$: store $d$ as failed |
| 5 | PROVE$(a)$ | $g$ | rule $g \leftarrow a, b$; push $a$ at depth 1, try $a \leftarrow g$ |
| 6 | PROVE$(g)$ | $g, a$ | loop check: $g$ is at depth 0, return (false, 0) |
| 7 | PROVE$(c)$ | $g, a$ | rule $a \leftarrow c$; $c$ is a fact: store $c$ as proved |
| 8 | back in $a$ | $g$ | store $a$ as proved |
| 9 | PROVE$(b)$ | $g$ | push $b$, rule $b \leftarrow a$, PROVE$(a)$ is a memo hit, store $b$ as proved |
| 10 | back in $g$ | empty | store $g$ as proved; the answer is true |

In step 6 the call for $a$ meets $g$, a goal that was open before it. If $a$ had then failed, line L14 would not have stored the failure, since $a$ could still follow from $g$ by another rule of $g$.

## Correctness

The [correctness proof](proofs/correctness.md) shows an invariant: every atom in *proved* is in $M$, no atom in *failed* is in $M$, and a call that returns $(\mathit{false}, l)$ has no proof tree that avoids the stack atoms at depth $l$ or more. A proof tree of least size has no atom twice on one path, so the loop check of line L5 loses no proof. When $\mathit{low} \ge k$, the set of avoided atoms is empty, so the atom is not in $M$ and line L13 may store it. The top call starts with the empty stack, so it returns true exactly when $g \in M$. The stack holds distinct atoms, so the search stops.

## Complexity

The stack holds at most $n$ distinct atoms, so the recursion depth is at most $n + 1$, and each call makes at most one inner call for each atom occurrence in the rules of its goal. So the number of calls is at most $O(s^{n+1})$, and the extra space is $O(n)$ for the stack and the memo tables. The worst case is exponential. In the rules $a_i \leftarrow a_j$ for all $i \ne j$ among $n$ atoms, with no facts, every failure meets a goal deeper in the stack, so line L14 stores nothing, and the search walks every simple path from $a_1$. The number of calls is at least $(n-1)!$; the implementation makes 11743 calls for $n = 7$. A goal that is a fact is decided in $O(1)$ time.

The problem has better algorithms. [Forward chaining](/forward-chaining/) with counters decides $g \in M$ in time linear in the size of $P$. [SLG resolution](/slg-resolution/) (tabling) keeps the goal-directed search but stores answers in tables, which makes it polynomial. With variables, the question whether an atom follows from a Datalog program is EXPTIME-complete in combined complexity; see [Datalog evaluation](/datalog-evaluation/).

## Properties

- **Goal directed.** Only rules that can help with the goal, or with its subgoals, are ever looked at.
- **Sound and complete** for propositional definite rules, with the loop check. Without it, the search does not stop on a rule such as $a \leftarrow a$.
- **Order dependent cost.** The answer does not depend on the order of the rules or of the body atoms, but the number of calls does.
- **Explainable.** The stack at each moment is a chain of reasons, which is why MYCIN could answer the user's question "why do you ask this?".

## Variants and improvements

- **Variables.** Rules with variables need unification, and the search becomes [SLD resolution](/sld-resolution/). Prolog uses it with leftmost selection and without a loop check, so it can run forever on left-recursive rules.
- **Tabling.** [SLG resolution](/slg-resolution/) stores the answers of each subgoal and suspends a goal that loops, in place of failing it. This removes the exponential repetition and also handles negation with the [well-founded semantics](/well-founded-semantics/).
- **Negation as failure.** A condition $\mathit{not}\ c$ succeeds when the proof of $c$ fails finitely; see [negation as failure](/negation-as-failure/).
- **Askable facts.** MYCIN and EMYCIN asked the user for the value of a goal that no rule concludes, and combined the answers with [certainty factors](/certainty-factors/).
- **Bottom-up with goal focus.** The [magic sets](/magic-sets/) rewriting lets forward chaining compute only the facts that a backward search would need.

## When to use it

Use backward chaining when there is one question, or a few, and most of the rules are irrelevant to it, as in diagnosis and consultation systems that ask the user for data only when a rule needs it. Use [forward chaining](/forward-chaining/) when new data must trigger all of its consequences, or when the worst case matters.

## Pitfalls

- **No loop check.** A left-recursive rule such as $a \leftarrow a, b$ makes a plain depth-first search run forever.
- **Storing every failure.** A failure that met an open goal is only a failure for the current stack. Storing it as a plain failure makes the search incomplete, as the program $g \leftarrow q$, $g \leftarrow s$, $q \leftarrow g$, $s$ shows: $q$ fails inside $g$, but $q \in M$.
- **Repeated work.** Without memo tables the same subgoal is proved again in every place where it occurs, and even with them the loop case can be exponential.
- **Asking too much.** In a consultation system the order of the rules decides which questions the user sees and in which order.

## Implementations

## History

Goal-directed search over rules goes back to the early theorem provers and to Kowalski's procedural reading of Horn clauses (1974), the base of Prolog. Shortliffe's MYCIN (1976) made backward chaining the control method of medical expert systems, and EMYCIN made it a shell for other domains; Buchanan and Shortliffe (1984) collect the work. Tabled resolution, which removes the repeated work, came in the 1990s with SLG resolution of Chen and Warren.

## References
