---
tag: 1G4RR0
kind: algorithm
slug: sld-resolution
name: SLD resolution
aliases:
- SLD-resolution
- linear definite clause resolution
- selective linear definite clause resolution
area: logic-and-constraints/unification-and-resolution
level: core
summary: Goal-directed resolution for definite programs. Each step picks an atom of the goal, unifies it with a clause head and puts the body in its place. It is sound and complete for any choice rule.
solves: [first-order-theorem-proving]
model: word-ram
properties: {deterministic: true}
history:
  year: 1974
  people: [Robert Kowalski, Robert Hill]
  note: Kowalski proposed the procedural reading of Horn clauses in 1974, and Hill proved the completeness of the linear resolution that Prolog uses in the same year. Apt and van Emden gave the name SLD resolution in 1982.
prereqs: [horn-clause, most-general-unifier, linear-resolution, standardization-apart]
see_also: [logic-programming, answer-substitution, sldnf-resolution, warren-abstract-machine, input-resolution, datalog-evaluation, horn-sat-forward-chaining, refutation]
sources:
  - book: isbn:9783540181996
    title: John W. Lloyd, Foundations of Logic Programming, second edition, Springer (1987)
    locator: Chapter 1, Section 6 (least Herbrand model and the fixpoint characterisation), and Chapter 2, Sections 7 to 10 (SLD resolution, soundness, completeness, independence of the computation rule, SLD trees and search rules)
  - paper: doi:10.1145/322326.322339
    title: Krzysztof R. Apt and Maarten H. van Emden, Contributions to the theory of logic programming, Journal of the ACM 29(3), 841 to 862 (1982)
    locator: the definitions of SLD derivations, the success set and its equality with the least Herbrand model and the least fixed point of T_P
  - paper: doi:10.1145/321978.321991
    title: Maarten H. van Emden and Robert A. Kowalski, The semantics of predicate logic as a programming language, Journal of the ACM 23(4), 733 to 742 (1976)
    locator: the operational, model-theoretic and fixpoint semantics and the proof that they agree
  - paper: "Robert A. Kowalski, Predicate logic as programming language, Information Processing 74 (Proceedings of the IFIP Congress), North-Holland, 569 to 574 (1974)"
    locator: the procedural interpretation of Horn clauses
  - paper: "Robert Hill, LUSH-resolution and its completeness, DCL Memo 78, Department of Artificial Intelligence, University of Edinburgh (1974)"
    locator: the completeness of linear resolution with a selection function for Horn clauses
  - paper: "Keith L. Clark, Predicate logic as a computational formalism, Research Report DOC 79/59, Department of Computing, Imperial College London (1979)"
    locator: the soundness and the strong completeness of SLD resolution with respect to computed answers
---

SLD resolution answers queries over a definite program, a set of [Horn clauses](/horn-clause/) with exactly one positive literal each. A query is a list of atoms. Each step selects one atom of the current goal, [renames](/standardization-apart/) a program clause apart, unifies the atom with the clause head by a [most general unifier](/most-general-unifier/), and replaces the atom by the clause body. A derivation that ends with the empty goal is a refutation, and the composition of its unifiers, restricted to the query variables, is a [computed answer](/answer-substitution/). SLD resolution is sound, and it is complete for every computation rule: each correct answer is an instance of some computed answer, whichever atom the rule selects at each step. It is the execution model of [logic programming](/logic-programming/) and of Prolog. The name means *selective linear resolution for definite clauses*.

## In plain words

A program is a list of rules such as "X is an ancestor of Y if X is a parent of Z and Z is an ancestor of Y", and of facts such as "Ann is a parent of Bob". You ask a question, for example "who has Ann as an ancestor?". The question is a list of things to show. Pick one of them, find a rule whose conclusion can be made to match it, and replace the thing by what that rule needs. Matching may fix the unknowns of the question. When nothing is left to show, the values that the unknowns got are an answer. Different choices of rule give a tree of tries, and each successful branch gives an answer.

## The problem

The input is a definite program $P$, a finite set of clauses $H \leftarrow B_1, \ldots, B_m$ with $m \ge 0$, and a query $\leftarrow A_1, \ldots, A_k$. A substitution $\theta$ is a *correct answer* if $P \models \forall (A_1 \wedge \cdots \wedge A_k)\theta$. The task is to list answers: substitutions that are correct, such that each correct answer is an instance of one of them. A *computation rule* $R$ chooses the atom to select in each goal. The search below tries the clauses in program order, depth first, with a depth bound $d$. Without the bound it is the search of Prolog.

## The algorithm

```pseudo id=main
SLD-SOLVE(P, Q, R, d)           ▷ program P, query Q, computation rule R, depth bound d
L1  S ← a stack with the triple (Q, ε, 0)                 ▷ goal, substitution so far, depth
L2  while S is not empty do
L3      (G, θ, n) ← pop(S)
L4      if G is empty then output θ restricted to the variables of Q; continue
L5      if n = d then continue
L6      A ← R(G)                                          ▷ the selected atom
L7      for each clause of P, in program order do
L8          H ← B_1, …, B_m ← the clause with fresh variables
L9          μ ← MGU(A, H)
L10         if μ exists then
L11             G' ← (G with A replaced by B_1, …, B_m) μ
L12             push (G', θμ, n + 1) on S, so that the child of the first clause is popped first
```

One pass of lines L6 to L11 is an *SLD step*. A sequence of steps from $Q$ is an *SLD derivation*. The tree of all derivations from $Q$ via $R$, with one child for each clause whose head unifies with the selected atom, is the *SLD tree*. The loop searches this tree depth first. The choice of $R$ changes the shape of the tree but, as the correctness section shows, not the set of answers it contains.

## Example

Take the program

```text
e(a, b).    e(b, c).
path(X, Y) ← e(X, Y).
path(X, Y) ← e(X, Z), path(Z, Y).
```

and the query $\leftarrow \mathit{path}(a, W)$, with the leftmost computation rule.

| goal | selected atom | clause used | unifier | result |
|---|---|---|---|---|
| $\mathit{path}(a, W)$ | $\mathit{path}(a, W)$ | path rule 1 | $X_1 = a, Y_1 = W$ | $e(a, W)$ |
| $e(a, W)$ | $e(a, W)$ | $e(a, b)$ | $W = b$ | empty: answer $W = b$ |
| $\mathit{path}(a, W)$ | $\mathit{path}(a, W)$ | path rule 2 | $X_2 = a, Y_2 = W$ | $e(a, Z_2), \mathit{path}(Z_2, W)$ |
| $e(a, Z_2), \mathit{path}(Z_2, W)$ | $e(a, Z_2)$ | $e(a, b)$ | $Z_2 = b$ | $\mathit{path}(b, W)$ |
| $\mathit{path}(b, W)$ | $\mathit{path}(b, W)$ | path rule 1, then $e(b, c)$ | $W = c$ | empty: answer $W = c$ |
| $\mathit{path}(b, W)$ | $\mathit{path}(b, W)$ | path rule 2, then $e(b, c)$ | $Z_4 = c$ | $\mathit{path}(c, W)$, which fails |

The SLD tree is finite and has two success leaves, with the computed answers $W = b$ and $W = c$. These are the atoms $\mathit{path}(a, \cdot)$ of the least Herbrand model. Bottom-up, $T_P \uparrow 1 = \{e(a,b), e(b,c)\}$, $T_P \uparrow 2$ adds $\mathit{path}(a,b)$ and $\mathit{path}(b,c)$, and $T_P \uparrow 3$ adds $\mathit{path}(a,c)$, which is the fixed point with 5 atoms. With the rule $\mathit{path}(X, Y) \leftarrow \mathit{path}(X, Z), e(Z, Y)$ in place of the second rule, the SLD tree holds the same two answers, and the depth-first search finds both. But the tree is now infinite, so the search never stops after the second answer.

## Correctness

The full proofs are in the [correctness proof](proofs/correctness.md). Let $M_P$ be the least Herbrand model of $P$, and $T_P$ the immediate consequence operator: $T_P(I)$ is the set of heads of ground instances of clauses whose bodies are in $I$.

1. **Fixpoint semantics (van Emden and Kowalski 1976).** $M_P = \mathrm{lfp}(T_P) = T_P \uparrow \omega$, and a ground atom $A$ satisfies $P \models A$ if and only if $A \in M_P$. The proof uses the [Knaster-Tarski theorem](/knaster-tarski-theorem/) and the continuity of $T_P$.
2. **Soundness (Clark 1979).** If $\sigma$ is a computed answer, then $P \models \forall (A_1 \wedge \cdots \wedge A_k)\sigma$. The proof is an induction on the length of the refutation.
3. **Completeness for every computation rule (Hill 1974, Apt and van Emden 1982, Clark 1979).** If $\theta$ is a correct answer and $R$ is any computation rule, there is a refutation via $R$ with computed answer $\sigma$ and a substitution $\gamma$ with $A_i\theta = A_i\sigma\gamma$ for all $i$. The proof builds the refutation from finite proof trees of ground instances, one step for each node of the proof trees, and lifts it by the property of most general unifiers. Since the length of the refutation is the size of the proof trees, it is the same for every $R$.

Completeness says that the SLD tree has a success leaf for each answer. The depth-first search finds it only if no infinite branch lies to its left. A fair search, such as [breadth-first search](/breadth-first-search/) or [iterative deepening](/iterative-deepening-search/) on the depth bound $d$, finds every success leaf.

## Complexity

Each step costs one unification, which takes time linear in the size of the terms with a good [unification algorithm](/paterson-wegman-unification/), plus the renaming of one clause. The number of steps has no bound in general. Definite programs can compute every partial recursive function (Tärnlund 1977), so whether a query has an answer is [undecidable](/undecidability/), and the SLD tree can be infinite. For [Datalog](/datalog/) programs, which have no function symbols, the least model is finite, but the SLD tree can still be infinite, as the left-recursive path rule shows. Bottom-up [Datalog evaluation](/datalog-evaluation/) is then the better choice. The depth-first search with bound $d$ uses memory linear in $d$ times the size of a goal, since the stack holds the siblings of the nodes on one branch.

## Properties

- **Sound and complete.** For definite programs, computed answers are exactly the most general correct answers, up to instances.
- **Independent of the computation rule.** The set of answers in the SLD tree does not depend on $R$. The size of the tree does.
- **Linear and input.** Each resolvent comes from the last goal and one input clause, so SLD resolution is a form of [linear](/linear-resolution/) and [input resolution](/input-resolution/). For Horn clauses input resolution is complete, though it is not complete for general clauses.
- **Answers, not only yes or no.** The unifiers build the values of the query variables, which can contain variables.

## Variants and improvements

- **Prolog.** Prolog uses the leftmost computation rule and depth-first search in program order, with backtracking. The [Warren Abstract Machine](/warren-abstract-machine/) compiles this search.
- **Negation as failure.** [SLDNF resolution](/sldnf-resolution/) adds negative literals to bodies and queries, decided by finite failure.
- **Tabling.** SLG resolution and other tabled methods record goals and their answers, so that left recursion terminates on Datalog programs.
- **Bottom-up evaluation.** Computing $T_P \uparrow \omega$ directly, with semi-naive evaluation and magic sets for the query, is the standard method for [Datalog](/datalog-evaluation/). For propositional programs it is [forward chaining](/horn-sat-forward-chaining/), which runs in linear time.

## When to use it

Use SLD resolution to run logic programs top-down, when only the answers to one query are needed and the program has function symbols, as in list processing or parsing. It gives answers with variables, and its depth-first form needs little memory. Use bottom-up evaluation or tabling for recursive queries over finite relations, where depth-first SLD can loop.

## Pitfalls

- **Depth-first search is not complete.** For the program `p ← p.` and `p.`, the query $\leftarrow p$ has a refutation of length 1. Prolog first takes the clause `p ← p` and loops forever. Swapping the clauses gives the answer at once, but then asking for all answers loops too.
- **Left recursion.** With a rule such as $\mathit{path}(X, Y) \leftarrow \mathit{path}(X, Z), e(Z, Y)$, depth-first search with the leftmost rule never stops, even over a finite graph. It can print answers first, but it loops when it looks for more, and a query with no answer loops with no output.
- **No occurs check in Prolog.** Prolog systems skip the [occurs check](/occurs-check/) by default for speed. Then $X = f(X)$ succeeds and the soundness theorem no longer holds.
- **Forgetting to rename apart.** Each use of a clause needs fresh variables. Otherwise two uses of the same rule share variables, and correct answers are lost.
- **Search rule versus computation rule.** Completeness holds for any computation rule, which chooses the atom. It does not hold for any search rule, which chooses the order of the branches.

## Implementations

## History

Kowalski (1974) proposed to read Horn clauses as procedures, and the language Prolog of Colmerauer and Roussel (1972 and 1973) ran them. Hill (1974) proved the completeness of LUSH resolution, a linear resolution with a selection function for Horn clauses. Van Emden and Kowalski (1976) gave the operational, model-theoretic and fixpoint semantics and proved that they agree. Clark (1979) proved soundness and the strong completeness for computed answers. Apt and van Emden (1982) named the method SLD resolution and proved that the success set equals the least Herbrand model. Lloyd's book (1984, second edition 1987) became the standard reference for the theory.

## References
