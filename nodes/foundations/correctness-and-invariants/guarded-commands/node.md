---
tag: DZDG4A
kind: model
slug: guarded-commands
name: Guarded command language
aliases:
- Dijkstra's guarded commands
area: foundations/correctness-and-invariants
level: advanced
summary: A small imperative language with nondeterministic guarded choice and loops, designed for calculating correct programs.
prereqs: [hoare-triple, precondition, postcondition]
see_also: [weakest-precondition, hoare-logic, loop-invariant, variant-function, total-correctness, partial-correctness, refinement-calculus]
sources:
  - url: "https://en.wikipedia.org/wiki/Guarded_Command_Language"
    locator: article Guarded Command Language, sections Guarded command, Statements and Semantics
  - book: isbn:9780387964805
    title: David Gries, The Science of Programming, Springer (1981)
    locator: Chapters 7 to 11 (weakest preconditions, skip and abort, assignment, the alternative command, the iterative command)
  - book: isbn:9780132158718
    title: Edsger W. Dijkstra, A Discipline of Programming, Prentice Hall (1976)
    locator: Chapter 3 (properties 1 to 4 of wp), Chapter 4 (the semantics of the commands), Chapter 5 (the theorems for if and do), Chapter 7 (Euclid's algorithm), Chapter 9 (On nondeterminacy being bounded, property 5)
  - book: isbn:9780387969572
    title: Edsger W. Dijkstra and Carel S. Scholten, Predicate Calculus and Program Semantics, Springer (1990)
    locator: the chapters on the semantics of the repetition and on the healthiness properties (conjunctivity, continuity) of predicate transformers
  - paper: doi:10.1145/360933.360975
    title: Edsger W. Dijkstra, Guarded commands, nondeterminacy and formal derivation of programs, Communications of the ACM 18(8), 1975
    locator: pp. 453 to 457
---

The guarded command language is a small imperative language that Edsger Dijkstra published in 1975. It has the commands skip, abort, assignment, sequence, a choice command (if, fi) and a loop command (do, od), and the choice and the loop use guards. When more than one guard is true, the language does not say which branch runs. Its meaning is given by the [weakest precondition](/weakest-precondition/) of each command, so that a program and its proof of [total correctness](/total-correctness/) can be built together.

## The machine

A state gives a value to each variable. A predicate is a boolean expression over the variables, and we identify it with the set of states where it is true. A program is a command, and a command is one of the following forms. Here $B$ and $B_i$ are boolean expressions called guards, $E$ and $E_i$ are expressions that are defined in every state, and $S$ and $S_i$ are commands.

- $\mathbf{skip}$ stops at once and changes nothing.
- $\mathbf{abort}$ never ends in a normal way: it may fail, or it may run forever.
- $x \leftarrow E$ assigns the value of $E$ to the variable $x$.
- $x_1, \dots, x_k \leftarrow E_1, \dots, E_k$, with distinct variables $x_i$, is the concurrent assignment. It evaluates all the expressions first, in the old state, and then assigns them at the same time. So $x, y \leftarrow y, x$ swaps $x$ and $y$.
- $S_1 ; S_2$ runs $S_1$ and then $S_2$.
- $\mathrm{IF} = \mathbf{if}\ B_1 \to S_1 \mathbin{[\,]} \cdots \mathbin{[\,]} B_n \to S_n\ \mathbf{fi}$ is the alternative command. It evaluates all guards. If some guard $B_i$ is true, it runs one $S_i$ with a true guard. If no guard is true, it behaves like $\mathbf{abort}$.
- $\mathrm{DO} = \mathbf{do}\ B_1 \to S_1 \mathbin{[\,]} \cdots \mathbin{[\,]} B_n \to S_n\ \mathbf{od}$ is the repetitive command. While some guard is true, it runs one $S_i$ with a true guard. When no guard is true, it stops. Here an empty set of true guards is the normal exit, not a failure.

When two or more guards are true, the choice among them is not specified. The language does not mean a random choice or a fixed order. It means that a proof must work for every possible choice. This is the nondeterminism of the language. When the guards exclude each other, the command is deterministic.

### The semantics

The meaning of a command $S$ is the predicate transformer $Q \mapsto \mathrm{wp}(S, Q)$. For a postcondition $Q$, $\mathrm{wp}(S, Q)$ is the set of start states from which every run of $S$ stops, and stops in a state that satisfies $Q$, whatever choices are made. Let $BB = B_1 \vee \cdots \vee B_n$ be the disjunction of the guards. The rules are as follows, where $Q[x := E]$ is $Q$ with each free $x$ replaced by $E$.

$$ \mathrm{wp}(\mathbf{skip}, Q) = Q, \qquad \mathrm{wp}(\mathbf{abort}, Q) = \mathit{false}, $$

$$ \mathrm{wp}(x \leftarrow E, Q) = Q[x := E], \qquad \mathrm{wp}(x_1, \dots, x_k \leftarrow E_1, \dots, E_k,\ Q) = Q[x_1, \dots, x_k := E_1, \dots, E_k], $$

$$ \mathrm{wp}(S_1 ; S_2, Q) = \mathrm{wp}(S_1, \mathrm{wp}(S_2, Q)), $$

$$ \mathrm{wp}(\mathrm{IF}, Q) = BB \wedge \bigwedge_{i=1}^{n} \big(B_i \implies \mathrm{wp}(S_i, Q)\big). $$

The substitution in the concurrent assignment is simultaneous. For the loop, let $H_k(Q)$ be the set of states from which DO stops after at most $k$ iterations, in a state that satisfies $Q$:

$$ H_0(Q) = Q \wedge \neg BB, \qquad H_{k+1}(Q) = H_0(Q) \vee \mathrm{wp}(\mathrm{IF}, H_k(Q)), $$

$$ \mathrm{wp}(\mathrm{DO}, Q) = \exists k \ge 0 : H_k(Q). $$

Here IF is the alternative command with the same guarded commands as DO. The conjunct $BB$ in the rule for IF has a consequence for proofs: a proof that an $\mathbf{if}$ command is correct must also show that at least one guard is true.

The weakest liberal precondition $\mathrm{wlp}(S, Q)$ is the set of start states from which every run that stops ends in $Q$. It has the same rules, except that $\mathrm{wlp}(\mathbf{abort}, Q) = \mathit{true}$, the conjunct $BB$ is absent from the rule for IF, and $\mathrm{wlp}(\mathrm{DO}, Q)$ is the greatest predicate $X$ with $X = (Q \wedge \neg BB) \vee (BB \wedge \mathrm{wlp}(\mathrm{IF}, X))$. It is the semantics of [partial correctness](/partial-correctness/).

## What it counts

The model has no cost measure. It does not count steps or memory. For each command $S$ and each postcondition $Q$ it fixes one set of start states, $\mathrm{wp}(S, Q)$. A program $S$ is correct for the precondition $P$ and the postcondition $Q$ when $P \implies \mathrm{wp}(S, Q)$. What a run can do is a set of outcomes, and a program is correct when all outcomes are good.

Take the loop $L = \mathbf{do}\ x > 0 \to x \leftarrow x - 1 \mathbin{[\,]} x > 1 \to x \leftarrow x - 2\ \mathbf{od}$ over the integers. From $x = 3$ the loop can run 2 times (3, 1, 0) or 3 times (3, 2, 1, 0). From $x = 5$ the number of iterations can be 3, 4 or 5. In general, for each integer $x \ge 0$ the number of iterations can be any integer from $\lceil x/2 \rceil$ to $x$, and every run ends with $x = 0$. For $x < 0$ no guard is true, so $L$ does nothing.

The rules give the same answer. Here $BB$ is $x > 0$, and $H_0(x = 0) = (x = 0 \wedge x \le 0)$, which is $x = 0$. By induction on $k$, $H_k(x = 0)$ is $0 \le x \le k$. The step: if $1 \le x \le k + 1$, then the first branch gives $x - 1 \in [0, k]$, and the second branch, when $x > 1$, gives $x - 2 \in [0, k]$, so both branches end in $H_k$ and $x \in \mathrm{wp}(\mathrm{IF}, H_k)$. If $x > k + 1$, the first branch gives $x - 1 > k$, so $x \notin \mathrm{wp}(\mathrm{IF}, H_k)$. If $x < 0$, then $x$ is in neither part. Hence $\mathrm{wp}(L, x = 0) = \exists k : 0 \le x \le k$, which is $x \ge 0$. The bound $k$ in $H_k$ must hold for the worst choice, which is $x$ iterations here.

## Relation to other models

- **Hoare logic.** [Hoare logic](/hoare-logic/) gives rules to derive a triple for a given program. The partial-correctness triple $\{P\}\ S\ \{Q\}$ holds exactly when $P \implies \mathrm{wlp}(S, Q)$. The total-correctness triple $[P]\ S\ [Q]$ holds exactly when $P \implies \mathrm{wp}(S, Q)$. Dijkstra used the language with wp to go in the other direction: the specification comes first and the program is calculated from it. The language can just as well be used to verify a program after it is written.
- **The usual while language.** The command $\mathbf{if}\ B \to S_1 \mathbin{[\,]} \neg B \to S_2\ \mathbf{fi}$ is the same as $\mathbf{if}\ B\ \mathbf{then}\ S_1\ \mathbf{else}\ S_2$, and $\mathbf{do}\ B \to S\ \mathbf{od}$ is the same as $\mathbf{while}\ B\ \mathbf{do}\ S$. A conditional without an else branch is $\mathbf{if}\ B \to S \mathbin{[\,]} \neg B \to \mathbf{skip}\ \mathbf{fi}$. The bare form $\mathbf{if}\ B \to S\ \mathbf{fi}$ is different: it aborts when $B$ is false.
- **Refinement calculus.** The [refinement calculus](/refinement-calculus/) extends the language with specification statements, and it treats a program as a refinement of a specification. Its specification statements can be miraculous or unboundedly nondeterministic, so some laws below do not hold for them.
- **Floyd's method.** The [inductive assertion method](/floyd-inductive-assertions/) works on flowcharts. The loop theorem for $\mathbf{do}$ has the same two parts: an invariant that each path keeps, and a measure that goes down.

## Known results in the model

**Healthiness conditions.** Every command $S$ of the language satisfies the following laws, for all predicates $Q$ and $R$ (Dijkstra 1976, Chapter 3, properties 1 to 4). Each is proved by induction on the structure of $S$, with an inner induction on $k$ for the sets $H_k$ of a loop.

- *Law of the excluded miracle:* $\mathrm{wp}(S, \mathit{false}) = \mathit{false}$. No run ends in a state that satisfies $\mathit{false}$.
- *Monotonicity:* if $Q \implies R$, then $\mathrm{wp}(S, Q) \implies \mathrm{wp}(S, R)$.
- *Conjunctivity:* $\mathrm{wp}(S, Q) \wedge \mathrm{wp}(S, R) = \mathrm{wp}(S, Q \wedge R)$.
- *Disjunctivity, one direction:* $\mathrm{wp}(S, Q) \vee \mathrm{wp}(S, R) \implies \mathrm{wp}(S, Q \vee R)$. Equality holds for a deterministic $S$. For $S = \mathbf{if}\ \mathit{true} \to x \leftarrow 0 \mathbin{[\,]} \mathit{true} \to x \leftarrow 1\ \mathbf{fi}$, $\mathrm{wp}(S, x = 0 \vee x = 1) = \mathit{true}$, while $\mathrm{wp}(S, x = 0) = \mathrm{wp}(S, x = 1) = \mathit{false}$.

**Continuity and bounded nondeterminism.** From each state, each command of the language has finitely many possible next steps: the guards are finite in number, and each assignment gives one result. Dijkstra (1976, Chapter 9) shows that this makes wp *continuous*: for each increasing chain $Q_0 \implies Q_1 \implies \cdots$ of predicates,

$$ \mathrm{wp}\Big(S, \exists i : Q_i\Big) = \exists i : \mathrm{wp}(S, Q_i). $$

Continuity is what makes the rule $\mathrm{wp}(\mathrm{DO}, Q) = \exists k : H_k(Q)$ correct: with finitely many choices at each step, a tree of runs in which every branch is finite is finite (König's lemma), so a bound $k$ on the number of iterations exists. With an unbounded choice the rule fails. Add the command $x \leftarrow ?$, which sets $x$ to any natural number, and take $\mathbf{do}\ b \to x \leftarrow ? ;\ b \leftarrow \mathit{false} \mathbin{[\,]} \neg b \wedge x > 0 \to x \leftarrow x - 1\ \mathbf{od}$. From a state with $b$ true, every run stops, after $1 + x'$ iterations where $x'$ is the chosen value. But no $k$ bounds all runs, so $\exists k : H_k(\mathit{true})$ is false in that state.

**The loop theorem.** Let $P$ be a predicate (the invariant), $t$ an integer expression (the [variant function](/variant-function/)), and IF the alternative command with the guarded commands of DO. Assume:

1. $P \wedge BB \implies \mathrm{wp}(\mathrm{IF}, P)$;
2. $P \wedge BB \implies t > 0$;
3. $P \wedge BB \wedge t = t_0 \implies \mathrm{wp}(\mathrm{IF}, t < t_0)$ for every integer $t_0$.

Then $P \implies \mathrm{wp}(\mathrm{DO}, P \wedge \neg BB)$.

*Proof.* We show by induction on $k \ge 0$ that $P \wedge t \le k \implies H_k(P \wedge \neg BB)$. Take a state with $P$ and $t \le k$. If $BB$ is false in it, the state is in $H_0(P \wedge \neg BB)$, which is part of $H_k$. If $BB$ is true, then $t > 0$ by 2, so $k \ge 1$. Let $t_0$ be the value of $t$. By conjunctivity, 1 and 3 give $\mathrm{wp}(\mathrm{IF}, P \wedge t < t_0)$. Since $t < t_0 \le k$ means $t \le k - 1$ for integers, monotonicity gives $\mathrm{wp}(\mathrm{IF}, P \wedge t \le k - 1)$, and the induction hypothesis with monotonicity gives $\mathrm{wp}(\mathrm{IF}, H_{k-1}(P \wedge \neg BB))$. So the state is in $H_k(P \wedge \neg BB)$. For $k = 0$ the case $BB$ cannot occur, since then $t > 0 \ge t$. Each state has some value of $t$, and if $t \le 0$ we use $k = 0$, so $P \implies \exists k : H_k(P \wedge \neg BB)$. $\square$

**Euclid's algorithm.** Let $X$ and $Y$ be positive integers. Consider
$$ x, y \leftarrow X, Y ;\ \mathbf{do}\ x > y \to x \leftarrow x - y \mathbin{[\,]} y > x \to y \leftarrow y - x\ \mathbf{od} $$
and the invariant $P$: $x > 0 \wedge y > 0 \wedge \gcd(x, y) = \gcd(X, Y)$, with the variant $t = x + y$. This is the subtraction form of the [Euclidean algorithm](/euclidean-algorithm/), as in Dijkstra (1976, Chapter 7). The initial assignment establishes $P$, because $\mathrm{wp}(x, y \leftarrow X, Y,\ P) = X > 0 \wedge Y > 0$. If $x > y$, then $x - y > 0$ and $\gcd(x - y, y) = \gcd(x, y)$, so the first branch keeps $P$. The second branch is the same with $x$ and $y$ exchanged. Each branch subtracts a positive integer from $t$, so condition 3 holds, and $t > 0$ under $P$. At exit, neither guard is true, so $x \le y$ and $y \le x$, hence $x = y$. Then $\gcd(x, x) = x$ equals $\gcd(X, Y)$. So the program is totally correct for the postcondition $x = \gcd(X, Y)$. For $(X, Y) = (12, 18)$ the states are $(12, 18), (12, 6), (6, 6)$: it ends with $x = y = 6$ after 2 iterations. For $(9, 6)$ the states are $(9, 6), (3, 6), (3, 3)$. For $(1, 100)$ it needs 99 iterations, so the subtraction form takes time linear in the inputs, not in their length.

**A choice command without a default.** For $\mathbf{if}\ x \ge y \to m \leftarrow x \mathbin{[\,]} y \ge x \to m \leftarrow y\ \mathbf{fi}$ and the postcondition $m = \max(x, y)$, the rule for IF gives
$$ (x \ge y \vee y \ge x) \wedge (x \ge y \implies x = \max(x, y)) \wedge (y \ge x \implies y = \max(x, y)), $$
and each conjunct is true. So the weakest precondition is $\mathit{true}$. The guards overlap when $x = y$, and there both branches give the same value, so the nondeterminism does no harm. If a branch gave a different value at $x = y$, the same program would be wrong.

## References
