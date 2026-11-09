---
tag: 5XGNFS
kind: technique
slug: equivalent-literal-substitution
name: Equivalent literal substitution
aliases:
- equivalence reasoning
- ELS
- equivalent literal detection
- SCC-based substitution
area: logic-and-constraints/sat-solving
level: advanced
summary: Find literals that must be equal by computing the strongly connected components of the binary implication graph, and replace each component by one representative literal.
prereqs: [conjunctive-normal-form, strongly-connected-components, implication-graph]
see_also: [2-sat, two-sat-algorithm, tarjan-scc, failed-literal-probing, bounded-variable-elimination, clause-subsumption]
sources:
  - paper: doi:10.1016/0020-0190(79)90002-4
    title: Bengt Aspvall, Michael F. Plass and Robert E. Tarjan, A linear-time algorithm for testing the truth of certain quantified Boolean formulas, Information Processing Letters 8(3), 1979, 121-123
    locator: the implication graph of 2-CNF, its strongly connected components, and the test that x and not x lie in one component
  - book: isbn:9781643681603
    title: Biere, Heule, van Maaren and Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 9 (Biere, Järvisalo and Kiesl, Preprocessing in SAT Solving), the section on equivalent literal substitution
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms Part 2, 2022
    locator: Section 7.2.2.2, Satisfiability, the discussion of binary clauses, the implication digraph and strong components
---

Equivalent literal substitution (ELS) finds literals that have the same value in every model of a [CNF](/conjunctive-normal-form/) formula and replaces them by one literal. It uses only the binary clauses. Each binary clause $(a \vee b)$ gives two implications, $\neg a \to b$ and $\neg b \to a$, and these form the binary [implication graph](/implication-graph/). If two literals are in the same [strongly connected component](/strongly-connected-components/), each implies the other, so they are equivalent. ELS picks one representative per component, rewrites every clause with it, and drops the clauses that become tautologies. If a component holds both $x$ and $\neg x$, the formula is unsatisfiable. The components come from [Tarjan's algorithm](/tarjan-scc/) in linear time. Unlike most other preprocessing steps, ELS keeps the number of models: each removed variable is a fixed function of its representative.

## In plain words

Two-option clauses say "if this is false, that must be true". Draw an arrow for each such rule. If you can follow arrows from A to B and also back from B to A, then A and B must always have the same value. A whole loop of such literals is one quantity with several names.

So pick one name for each loop and write it everywhere instead of the others. The formula gets fewer variables, and many clauses fall away because they turn into "A or not A". If a loop contains a variable and its own opposite, the formula has no solution. At the end, each removed variable simply copies the value of the name that replaced it.

## When it applies

Use it as a cheap preprocessing or inprocessing step, before [bounded variable elimination](/bounded-variable-elimination/) and other steps that work better on fewer variables. Signals:

- the formula comes from circuits with buffers, inverters or equal signals, which give equivalences $x \leftrightarrow y$ as two binary clauses;
- [failed-literal probing](/failed-literal-probing/) or learning added many binary clauses, which may close new cycles;
- the formula has a large [2-SAT](/2-sat/) part.

## The template

Notation: $F$ has $n$ variables, $m$ clauses and $|F|$ literal occurrences. The binary implication graph $G_F$ has the $2n$ literals as nodes and two edges $\neg a \to b$ and $\neg b \to a$ for each binary clause $(a \vee b)$ of $F$. $\mathrm{rep}(l)$ is the representative of the component of $l$.

```pseudo id=main
ELS(F)
L1  build the binary implication graph G_F
L2  compute the strongly connected components of G_F
L3  if some component holds both x and ¬x then return UNSAT
L4  in each component S pick r(S), the literal with the smallest variable; set rep(l) ← r(S) for l ∈ S
L5  replace each literal l in each clause by rep(l)
L6  drop the clauses that became tautologies; merge repeated literals
L7  drop repeated clauses; repeat from L1 while new equivalences appear; return (F, rep)
RECONSTRUCT(α, rep)
L8  for each variable x with rep(x) ≠ x: α(x) ← α(rep(x))
```

The graph has a symmetry: there is an edge $a \to b$ exactly when there is an edge $\neg b \to \neg a$. So if $S$ is a component, so is $\neg S = \{\neg l : l \in S\}$, and line L4 picks $r(\neg S) = \neg r(S)$, because the variable with the smallest index is the same in both. So $\mathrm{rep}(\neg l) = \neg\,\mathrm{rep}(l)$, and the substitution is consistent.

### Example

Let $F$ have the six clauses
$$(\neg x_1 \vee x_2),\ (\neg x_2 \vee x_3),\ (\neg x_3 \vee x_1),\ (x_1 \vee x_4 \vee x_5),\ (\neg x_2 \vee \neg x_4),\ (x_3 \vee \neg x_5 \vee x_6).$$

The first three clauses give the cycle $x_1 \to x_2 \to x_3 \to x_1$ and the cycle $\neg x_1 \to \neg x_3 \to \neg x_2 \to \neg x_1$. The clause $(\neg x_2 \vee \neg x_4)$ adds $x_2 \to \neg x_4$ and $x_4 \to \neg x_2$, which close no cycle. So the components are $\{x_1, x_2, x_3\}$, $\{\neg x_1, \neg x_2, \neg x_3\}$ and singletons, and $\mathrm{rep}(x_2) = \mathrm{rep}(x_3) = x_1$. The first three clauses become $(\neg x_1 \vee x_1)$ and are dropped, and the result is
$$(x_1 \vee x_4 \vee x_5),\ (\neg x_1 \vee \neg x_4),\ (x_1 \vee \neg x_5 \vee x_6)$$
over 4 variables. It has as many models over $x_1, x_4, x_5, x_6$ as $F$ has over $x_1, \ldots, x_6$, and RECONSTRUCT sets $x_2 = x_3 = x_1$.

### Why it is correct

**Lemma 1.** If $G_F$ has a path from $a$ to $b$, then every model of $F$ that makes $a$ true makes $b$ true.

*Proof.* By induction on the length of the path. An edge $\neg u \to v$ comes from a clause $(u \vee v)$ of $F$: if $\neg u$ is true then $u$ is false, so $v$ is true. $\square$

**Theorem.** Let ELS return $F'$ and $\mathrm{rep}$ without UNSAT. Then the map $\alpha \mapsto \alpha|_{V'}$, where $V'$ is the set of variables not replaced, is a bijection from the models of $F$ to the models of $F'$, and RECONSTRUCT is its inverse. If ELS returns UNSAT, $F$ has no model.

*Proof.* By Lemma 1, in every model of $F$ each literal has the value of its representative. If $x$ and $\neg x$ are in one component, then $x = \neg x$ in every model, so there is none. Otherwise, let $\alpha$ be a model of $F$. Each clause $C'$ of $F'$ comes from a clause $C$ of $F$ by line L5, and the literals of $C'$ have the same values under $\alpha$ as those of $C$, so $\alpha$ satisfies $F'$, and so does $\alpha|_{V'}$ since $F'$ uses only $V'$. Conversely, let $\beta$ be a model of $F'$ and let $\alpha$ be its extension by RECONSTRUCT. A clause $C$ of $F$ whose image is a tautology contains literals $l, l'$ with $\mathrm{rep}(l) = \neg\,\mathrm{rep}(l')$; under $\alpha$ one of them is true. Every other clause has an image in $F'$, which $\beta$ satisfies, and each literal $l$ has the value of $\mathrm{rep}(l)$ under $\alpha$. So $\alpha$ is a model of $F$. Both maps are inverse to each other, because in every model of $F$ the replaced variables are fixed by $V'$. The repeat of line L7 applies the same argument to each round. $\blacksquare$

**Cost.** Lines L1 to L3 take $O(n + m)$ time with Tarjan's algorithm, and lines L5 to L7 take $O(|F|)$, so one round is $O(n + |F|)$.

## Classic examples

- **[2-SAT](/2-sat/).** For a formula with only binary clauses, ELS with the check of line L3 is the [linear-time 2-SAT algorithm](/two-sat-algorithm/) of Aspvall, Plass and Tarjan, up to the step that reads off a model from the component order.
- **Circuits.** A buffer $y = x$ or an inverter $y = \neg x$ in a [Tseitin encoding](/tseitin-transformation/) gives two binary clauses that form a cycle, so ELS removes the extra variable.
- **Structural hashing.** After two AND gates with the same inputs are found equal by other means (for example by [failed-literal probing](/failed-literal-probing/)), the learned binary clauses close a cycle, and ELS merges the gates.
- **Preprocessors and inprocessors.** Lingeling, CaDiCaL and Kissat run ELS on the binary clauses, including learned ones, between other steps.

## Variations

- **Failed literals from the same graph.** If there is a path from $l$ to $\neg l$, then $\neg l$ holds in every model and can be added as a unit. This is a case of [failed-literal probing](/failed-literal-probing/) found without propagation.
- **Transitive reduction.** Binary clauses implied by paths of other binary clauses can be removed, which shrinks the graph.
- **Equivalences from longer clauses.** Gate detection or [Stålmarck's method](/stalmarck-algorithm/) finds equivalences that are not cycles of binary clauses, for example from XOR constraints, and feeds them into the same substitution.
- **Hyper-binary resolution.** Adding binary clauses found by unit propagation from one literal can create more cycles for ELS.

## Pitfalls

- **Consistent representatives.** If $\mathrm{rep}(\neg l) \ne \neg\,\mathrm{rep}(l)$, the substitution is wrong. Choose the representative by a rule that respects the symmetry, such as the smallest variable index.
- **Frozen variables.** A variable that appears in assumptions or later clauses of [incremental SAT](/incremental-sat/) can be the representative but must not be replaced, or the later clauses must be rewritten too.
- **Proof output.** In a [DRAT](/drat-proof/) proof, each rewritten clause is implied by unit propagation from the original clause and the binary clauses of the cycle, so add it before deleting the old one.
- **Deep recursion.** On large formulas a recursive SCC algorithm overflows the stack; use an explicit stack.

## Exercises

1. Prove the symmetry of $G_F$ and show that if $S$ is a strongly connected component then $\neg S$ is one too.
2. Show that ELS keeps the number of models, and give a formula where [blocked clause elimination](/blocked-clause-elimination/) does not.
3. Give a formula in which ELS finds no equivalence in the first round but finds one in the second round, after line L5 turns a ternary clause into a binary one.

## References
