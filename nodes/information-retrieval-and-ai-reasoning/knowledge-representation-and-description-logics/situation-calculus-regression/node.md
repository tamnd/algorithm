---
tag: A4NKPR
kind: algorithm
slug: situation-calculus-regression
name: Regression in the situation calculus
aliases:
- Reiter's regression operator
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: advanced
summary: Rewrites a query about the situation after a sequence of actions into an equivalent query about the initial situation, using successor state axioms.
model: word-ram
complexity:
  vars: {n: the number of actions in the sequence, q: the number of nodes of the query, p: the number of nodes of the largest precondition, m: "the largest total size of the successor state formulas of one action", k: the number of fluents}
  time: {regress_expected: O(n q + n^2 m), executable_expected: O(n p + n^2 m), entail_brute_force: O(2^k (q + n m))}
  space: {regressed_formula: O(q + n m)}
properties: {deterministic: true, exact: true, needs_complete_initial_database: false}
history:
  year: 1991
  people: [Raymond Reiter]
  note: Reiter gave successor state axioms and showed that regression with them is complete for the projection problem. Pirri and Reiter (1999) proved the general regression theorem for basic action theories.
prereqs: [situation-calculus, successor-state-axioms]
see_also: [goal-regression, frame-problem, weakest-precondition, yale-shooting-problem, backward-state-space-search, hash-consing, tseitin-transformation, event-calculus]
sources:
  - book: isbn:9780262182188
    title: Raymond Reiter, Knowledge in Action, Logical Foundations for Specifying and Implementing Dynamical Systems, MIT Press, 2001
    locator: Chapter 4, Section 4.4 (basic action theories), Section 4.5 (regression, the regression operator and the regression theorem), Section 4.6 (using regression for executability and projection); Section 11.6 (regression with knowledge-producing actions)
  - paper: doi:10.1145/316542.316545
    title: Fiora Pirri and Raymond Reiter, Some contributions to the metatheory of the situation calculus, Journal of the ACM 46(3), 1999
    locator: pages 325 to 361 (basic action theories, relative satisfiability, regressable formulas and the soundness and completeness of regression)
  - paper: doi:10.1016/B978-0-12-450010-5.50026-8
    title: "Raymond Reiter, The frame problem in the situation calculus: A simple solution (sometimes) and a completeness result for goal regression, in V. Lifschitz (editor), Artificial Intelligence and Mathematical Theory of Computation, Academic Press, 1991"
    locator: pages 359 to 380 (successor state axioms and the completeness of goal regression)
  - paper: doi:10.1016/S0004-3702(96)00044-6
    title: Fangzhen Lin and Raymond Reiter, How to progress a database, Artificial Intelligence 92(1-2), 1997
    locator: pages 131 to 167 (progression as the alternative to regression, and the result that progression is not always first-order definable; general locator)
---

Regression is Reiter's method for the projection problem of the [situation calculus](/situation-calculus/): to decide whether a formula holds in the situation $\mathit{do}([\alpha_1, \ldots, \alpha_n], S_0)$, it replaces each fluent by the right side of its [successor state axiom](/successor-state-axioms/), one action at a time from the last to the first, until the formula speaks only about $S_0$. Then a theorem prover checks the result against the initial database alone, with no axioms about actions or situations. [Goal regression](/goal-regression/) does the same for a set of [STRIPS](/strips/) facts and one action; this page treats arbitrary formulas and whole action sequences, and gives the regression theorem that makes the method complete. The code on this page handles a ground, finite, propositional fragment with no sensing actions, while the regression theorem of Pirri and Reiter (1999) is first order.

## In plain words

You know some things about the world now, and you plan to do a list of actions. You want to know whether some fact will be true at the end. One way is to run the actions forward in your head from every world you think possible. Regression goes the other way. Take the question about the end and ask: what must be true one step before, so that the last action makes the fact true? Each action has a rule that says exactly when it makes a fact true and when it leaves it alone, so that question has an exact answer. Repeat this for each action, back to the start. Now the question is about the present only, and you can check it against what you know now. The rules are used, but never the full history of possible worlds.

## The problem

A **basic action theory** (Reiter 2001, Section 4.4) is $\mathcal{D} = \Sigma \cup \mathcal{D}_{ss} \cup \mathcal{D}_{ap} \cup \mathcal{D}_{una} \cup \mathcal{D}_{S_0}$: the foundational axioms $\Sigma$ for situations, one successor state axiom for each fluent,

$$F(\vec x, \mathit{do}(a, s)) \leftrightarrow \Phi_F(\vec x, a, s),$$

one precondition axiom $\mathit{Poss}(A(\vec x), s) \leftrightarrow \Pi_A(\vec x, s)$ for each action function $A$, unique names axioms for actions, and the initial database $\mathcal{D}_{S_0}$, a set of first-order sentences about $S_0$ only. A formula $W$ is **regressable** when every situation term in it has the form $\mathit{do}([\alpha_1, \ldots, \alpha_n], S_0)$, every $\mathit{Poss}$ atom has an action term of the form $A(\vec t)$, and it does not quantify over situations, compare situations with $\sqsubset$ or equate two situations.

- **Projection.** Given $\mathcal{D}$ and a regressable sentence $W$, decide $\mathcal{D} \models W$.
- **Executability.** Given ground actions $\alpha_1, \ldots, \alpha_n$, decide whether $\mathcal{D} \models \bigwedge_{i=1}^{n} \mathit{Poss}(\alpha_i, \mathit{do}([\alpha_1, \ldots, \alpha_{i-1}], S_0))$.

The **regression operator** $\mathcal{R}$ is defined on regressable formulas by: $\mathcal{R}[W] = W$ if $W$ mentions no situation term other than $S_0$; $\mathcal{R}[\mathit{Poss}(A(\vec t), \sigma)] = \mathcal{R}[\Pi_A(\vec t, \sigma)]$; $\mathcal{R}[F(\vec t, \mathit{do}(\alpha, \sigma))] = \mathcal{R}[\Phi_F(\vec t, \alpha, \sigma)]$ after a renaming of the bound variables of $\Phi_F$; and $\mathcal{R}$ commutes with $\neg$, $\wedge$ and $\exists$. Each rewrite of a fluent removes one $\mathit{do}$ from its situation term, so the recursion stops.

**Regression theorem** (Pirri and Reiter 1999; Reiter 2001, Section 4.5). If $W$ is regressable, then $\mathcal{R}[W]$ is a formula about $S_0$ only, and

$$\mathcal{D} \models W \iff \mathcal{D}_{S_0} \cup \mathcal{D}_{una} \models \mathcal{R}[W].$$

The foundational axioms, the successor state axioms and the precondition axioms are used up by the rewriting; the final test is an ordinary first-order entailment.

**The fragment of the code.** Fluents are ground atoms with no object arguments, the actions are a finite set of ground names, and no action senses. A state is then a truth assignment to the $k$ fluents. For each action $a$ and fluent $F$ the successor state axiom is $F(\mathit{do}(a, s)) \leftrightarrow \gamma^+_{F,a}(s) \vee (F(s) \wedge \neg \gamma^-_{F,a}(s))$, where $\gamma^\pm_{F,a}$ are propositional formulas over the fluents, and $\Phi_{F,a}$ is its right side. The unique names axioms are built into the action names, and $\mathcal{D}_{S_0}$ is a set of propositional formulas, which may leave fluents unknown.

## The algorithm

Formulas are nodes of a [hash-consed](/hash-consing/) DAG: MAKE returns the existing node for a formula that is already built, and folds the constants true and false.

```pseudo id=main
REGRESS(φ, [a_1, ..., a_n])            ▷ φ is about do([a_1, ..., a_n], S0)
L1  for i ← n down to 1 do
L2      M ← an empty memo table
L3      φ ← STEP(φ, a_i, M)                 ▷ now φ is about do([a_1, ..., a_{i-1}], S0)
L4  return φ                                ▷ a formula about S0

STEP(u, a, M)                           ▷ the formula u with each fluent F replaced by Φ_{F,a}
L5  if u is in M then return M[u]
L6  if u is true or false then r ← u
L7  else if u is a fluent F then r ← Φ_{F,a}
L8  else if u = ¬v then r ← MAKE(¬, STEP(v, a, M))
L9  else u = v ∘ w with ∘ in {∧, ∨}: r ← MAKE(∘, STEP(v, a, M), STEP(w, a, M))
L10 M[u] ← r; return r

EXECUTABLE-FORMULA([a_1, ..., a_n])
L11 χ ← true
L12 for i ← n down to 1 do
L13     χ ← MAKE(∧, Π_{a_i}, STEP(χ, a_i, an empty memo table))
L14 return χ

PROJECT(D, φ, [a_1, ..., a_n])
L15 return ENTAILS(D_S0, REGRESS(φ, [a_1, ..., a_n]))
```

ENTAILS$(\mathcal{D}_{S_0}, \psi)$ decides $\mathcal{D}_{S_0} \models \psi$. The code tries all $2^k$ states; a real system gives $\mathcal{D}_{S_0} \wedge \neg \psi$ to a SAT solver after the [Tseitin transformation](/tseitin-transformation/) of the DAG. Line L13 keeps the invariant that $\chi$, after the step for $a_i$, is about $\mathit{do}([a_1, \ldots, a_{i-1}], S_0)$ and says that $a_i, \ldots, a_n$ can run in order from there. So one backward pass regresses every precondition through all the actions before it.

## Example

Take the [Yale shooting](/yale-shooting-problem/) domain with the fluents $\mathit{loaded}$ and $\mathit{alive}$. The action $\mathit{load}$ has $\Pi_{\mathit{load}} = \neg \mathit{loaded}$ and $\gamma^+_{\mathit{loaded}} = \mathit{true}$; $\mathit{wait}$ has no effects; $\mathit{shoot}$ has $\gamma^-_{\mathit{alive}} = \mathit{loaded}$ and $\gamma^-_{\mathit{loaded}} = \mathit{true}$. Both $\mathit{wait}$ and $\mathit{shoot}$ are always possible. The right sides of the successor state axioms are:

| action | $\Phi_{\mathit{loaded}, a}$ | $\Phi_{\mathit{alive}, a}$ |
|---|---|---|
| $\mathit{load}$ | $\mathit{true}$ | $\mathit{alive}$ |
| $\mathit{wait}$ | $\mathit{loaded}$ | $\mathit{alive}$ |
| $\mathit{shoot}$ | $\mathit{false}$ | $\mathit{alive} \wedge \neg \mathit{loaded}$ |

Regress $\neg \mathit{alive}$ through $[\mathit{load}, \mathit{wait}, \mathit{shoot}]$:

| step | action | $\varphi$ after line L3 |
|---|---|---|
| start | | $\neg \mathit{alive}$ |
| $i = 3$ | $\mathit{shoot}$ | $\neg(\mathit{alive} \wedge \neg \mathit{loaded})$ |
| $i = 2$ | $\mathit{wait}$ | $\neg(\mathit{alive} \wedge \neg \mathit{loaded})$ |
| $i = 1$ | $\mathit{load}$ | $\neg(\mathit{alive} \wedge \neg \mathit{true})$, which MAKE folds to $\mathit{true}$ |

The result is $\mathit{true}$, so every initial database entails that the victim is dead after the sequence. EXECUTABLE-FORMULA gives $\chi = \mathit{true}$ after $\mathit{shoot}$ and $\mathit{wait}$, and $\neg \mathit{loaded}$ after $\mathit{load}$. With $\mathcal{D}_{S_0} = \{\mathit{alive}\}$ the sequence is not known to be executable, since the state with $\mathit{loaded}$ true is a model, and with $\mathcal{D}_{S_0} = \{\mathit{alive}, \neg \mathit{loaded}\}$ it is. The query $\mathit{alive}$ after $[\mathit{wait}, \mathit{shoot}]$ regresses to $\mathit{alive} \wedge \neg \mathit{loaded}$: the first database does not entail it and the second does.

**Sharing matters.** Let one action set $p$ to $p \leftrightarrow q$, with $\gamma^+_p = \neg p \wedge \neg q$ and $\gamma^-_p = \neg q$, so that $\Phi_{p,a} = (\neg p \wedge \neg q) \vee (p \wedge q)$. Regressing $p$ through $n$ copies of $a$ gives a formula whose tree has $2^{n+3} - 7$ nodes for $n \ge 1$ (9, 25, 57, ..., 2041 for $n = 8$), because $p$ occurs twice in $\Phi_{p,a}$. The DAG has $4n + 3$ nodes (7, 11, 15, ..., 35).

## Correctness

The proofs are in the [correctness proof](proofs/correctness.md). For a state $s$ and an action $a$, let $\mathrm{succ}(s, a)$ be the state with $\mathrm{succ}(s, a)(F) = s(\Phi_{F,a})$ for each fluent $F$; this is what the successor state axioms force.

1. **One step.** For every formula $u$ and state $s$, $s \models \mathrm{STEP}(u, a, M) \iff \mathrm{succ}(s, a) \models u$. The proof is an induction on $u$; the case of a fluent is the successor state axiom, and the memo table only returns values that were computed by the same rule.
2. **Whole sequence.** By induction on $n$, $s \models \mathrm{REGRESS}(\varphi, [a_1, \ldots, a_n])$ if and only if $\varphi$ holds in the state reached from $s$ by $a_1, \ldots, a_n$.
3. **Projection.** In the fragment, a model of $\mathcal{D}$ is fixed by its initial state, which is any model of $\mathcal{D}_{S_0}$, since the successor state axioms determine every later state. So $\mathcal{D} \models \varphi(\mathit{do}([a_1, \ldots, a_n], S_0))$ if and only if $\mathcal{D}_{S_0} \models \mathrm{REGRESS}(\varphi, [a_1, \ldots, a_n])$, which is the regression theorem for this fragment.
4. **Executability.** By induction from $i = n$ down to 1, $\chi$ after line L13 holds at $s$ if and only if $a_i, \ldots, a_n$ are possible in order from $s$.

## Complexity

- **Size.** Line L7 adds the nodes of $\Phi_{F,a}$ and lines L8 and L9 add at most one node for each node of $\varphi$. So the DAG after the step for $a_i$ has at most $|\varphi_i| + \sum_F |\Phi_{F,a_i}|$ nodes, and the result has at most $q + n m$ nodes. The tree form has no such bound, as the example shows.
- **Time.** Step $i$ visits each node of the current DAG once, with one expected $O(1)$ hash lookup per node, so the total is $\sum_i O(q + (n - i) m) = O(n q + n^2 m)$ expected. EXECUTABLE-FORMULA has the same bound with $q$ replaced by the size $p$ of the largest precondition, because $\chi$ grows by at most one precondition and one round of $\Phi$ formulas per step.
- **Entailment.** In the fragment, projection with an arbitrary propositional $\mathcal{D}_{S_0}$ is [coNP](/co-np/)-complete. It is in coNP because the regressed DAG has polynomial size, and a model of $\mathcal{D}_{S_0}$ that falsifies it is a short certificate. It is coNP-hard already for $n = 0$, where it is propositional entailment. If $\mathcal{D}_{S_0}$ fixes every fluent, ENTAILS is one evaluation and projection takes polynomial time. In the first-order case regression still terminates, but the final test $\mathcal{D}_{S_0} \cup \mathcal{D}_{una} \models \mathcal{R}[W]$ is first-order entailment, which is undecidable in general.

## Properties

- **Exact.** The answer is the same as the answer from the whole theory, not an approximation.
- **Works with incomplete knowledge.** $\mathcal{D}_{S_0}$ may leave fluents open; the answer is "entailed" only when every possible initial state gives the same answer.
- **Query-driven.** Only the fluents that the query reaches are rewritten. Regression never builds a state.
- **Leaves the database unchanged.** Many queries over different histories use the same $\mathcal{D}_{S_0}$.

## Variants and improvements

- **Composition forward.** In the propositional fragment, compute for each fluent $F$ a formula $\theta_i(F)$ about $S_0$ that gives $F$ after $a_1, \ldots, a_i$: $\theta_0(F) = F$ and $\theta_i(F) = \Phi_{F,a_i}[G := \theta_{i-1}(G)]$. Then $\mathcal{R}[\varphi] = \varphi[G := \theta_n(G)]$. With sharing this takes $O(q + n m)$ expected time, at the cost of computing all fluents, also those that the query does not need.
- **Progression** (Lin and Reiter 1997). Update $\mathcal{D}_{S_0}$ to a database about the current situation, and answer later queries against it. Lin and Reiter show that the progressed database is not always first-order definable, and they give classes where it is.
- **Knowledge and sensing.** With a knowledge fluent and sensing actions, regression extends to formulas about what the agent knows (Reiter 2001, Section 11.6).
- **Goal regression for STRIPS.** When each $\gamma^+_{F,a}$ and $\gamma^-_{F,a}$ is $\mathit{true}$ or $\mathit{false}$ and the query is a conjunction of fluents, $\mathcal{R}$ is the set formula of [goal regression](/goal-regression/), and regressing through a plan is [backward state-space search](/backward-state-space-search/) read as logic. The [weakest precondition](/weakest-precondition/) of an assignment is the same substitution idea for programs.

## When to use it

Use regression for a few queries about hypothetical action sequences over an initial database that changes rarely, for example in an interpreter that must check that each step of a candidate plan is possible. Use progression when an agent acts for a long time and asks many questions about the current state: the regressed formulas then grow with the length of the history, while a progressed database does not.

## Pitfalls

- **Projection is not executability.** A query can hold after a sequence in every model even when the sequence cannot run. In the example, $\neg \mathit{alive}$ after $[\mathit{load}, \mathit{wait}, \mathit{shoot}]$ is entailed by $\{\mathit{alive}\}$, but the sequence is not known to be executable there. Check $\mathit{Poss}$ separately, or conjoin it to the query.
- **Exponential growth without sharing.** A successor state formula that mentions a fluent twice doubles the tree at each step, as in the example. Keep the formula as a DAG and pass it to the prover in a form that keeps the sharing.
- **Non-regressable queries.** "The light is on in every situation reachable from $S_0$" quantifies over situations, and $\mathcal{R}$ is not defined on it. Such properties need induction on situations, which $\Sigma$ provides but regression does not use.
- **Variable capture and unique names.** In the first-order case, rename the bound variables of $\Phi_F$ before the substitution. A formula such as $a = \mathit{shoot}$ inside $\Phi_F$ simplifies to $\mathit{false}$ for $a = \mathit{load}$ only with the unique names axioms, so leaving $\mathcal{D}_{una}$ out of the final test gives wrong answers.

## Implementations

## History

Reiter (1991) gave successor state axioms, built from effect axioms and the causal completeness assumption, and proved that goal regression with them is complete. Pirri and Reiter (1999) gave the metatheory of basic action theories, including the regression theorem and the result that such a theory is satisfiable if and only if its initial database together with the unique names axioms is satisfiable. Lin and Reiter (1997) studied progression as the alternative. Reiter (2001) collected the theory, an implementation in Prolog and the extension to knowledge.

## References
