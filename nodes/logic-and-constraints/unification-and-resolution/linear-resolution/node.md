---
tag: 4MCTF6
kind: algorithm
slug: linear-resolution
name: Linear resolution
aliases:
- linear refutation
- linear format
- linear deduction
area: logic-and-constraints/unification-and-resolution
level: advanced
summary: Resolution in one chain, where each new clause comes from the last one and an input clause or an earlier clause of the chain. Refutation complete (Loveland 1970, Luckham 1970).
solves: [first-order-theorem-proving]
model: word-ram
complexity:
  vars: {b: the largest number of moves from one center, d: the depth bound}
  time: {worst: O(b^(d+1))}
  space: {extra: O(b d)}
properties: {deterministic: true, exact: false, online: false, recursive: true, in_place: false}
history:
  year: 1970
  people: [Donald W. Loveland, David Luckham]
  note: Loveland and Luckham proved, independently and in the same volume, that linear refutations exist for every unsatisfiable set of clauses.
prereqs: [binary-resolution, factoring, robinson-resolution]
see_also: [input-resolution, set-of-support, sld-resolution, unit-resolution, robinson-completeness-theorem, lifting-lemma]
sources:
  - paper: "Donald W. Loveland, A linear format for resolution, in Symposium on Automatic Demonstration, Lecture Notes in Mathematics 125, Springer, 1970, 147-162"
    locator: the linear format and its completeness
  - paper: "David Luckham, Refinement theorems in resolution theory, in Symposium on Automatic Demonstration, Lecture Notes in Mathematics 125, Springer, 1970, 163-190"
    locator: completeness of linear (ancestry-filter) resolution
  - book: isbn:9780121703509
    title: Chin-Liang Chang and Richard Char-Tung Lee, Symbolic Logic and Mechanical Theorem Proving, Academic Press, 1973
    locator: Chapter 7, linear resolution
  - paper: "Robert Anderson and W. W. Bledsoe, A linear format for resolution with merging and a new technique for establishing completeness, Journal of the ACM 17(3), 525-534, 1970"
    locator: the proof of completeness by induction on the number of excess literals
  - paper: "Robert Kowalski and Donald Kuehner, Linear resolution with selection function, Artificial Intelligence 2(3-4), 227-260, 1971"
    locator: SL resolution, linear resolution with a selection function
---

Linear resolution is the restriction of [Robinson's resolution principle](/robinson-resolution/) in which a refutation is one chain of clauses. It starts with a **top clause** $C_0$ from the input. Each next clause $C_{i+1}$, a **center**, is a factor of $C_i$, or a [binary resolvent](/binary-resolution/) of $C_i$ with a **side clause**, which is an input clause, a factor of one, or an earlier center $C_j$ with $j < i$. Loveland (1970) and Luckham (1970) proved that this restriction is still refutation complete. If $S$ is unsatisfiable and $S$ minus a clause $C$ is satisfiable, a linear refutation with top clause $C$ exists. The chain shape makes the search a depth-first search over one sequence, so it needs little memory, and it is the base of model elimination, SL resolution and [SLD resolution](/sld-resolution/).

## In plain words

You want to show that a list of rules cannot all hold. Pick one rule to start with. At each step, combine the newest rule with one other rule: a rule from the list, or a rule that you made earlier in this same line. The combination gives the next newest rule. If you reach the empty rule, you are done.

So the proof is one line of rules, each from the one before. You never combine two old results that sit far apart. That keeps the search narrow. It also means you can search like a maze: walk forward, and step back when the line goes nowhere.

The surprise is that you lose nothing. If the rules clash at all, some single line reaches the empty rule. You can even choose the starting rule, as long as the other rules can hold together.

## The problem

The input is a finite set $S$ of first-order clauses, and the question is whether $S$ is unsatisfiable. This page uses a bounded search: it looks for a linear refutation of at most $D$ steps, and answers UNSAT with the chain, or UNKNOWN. A larger $D$ finds more refutations, and every unsatisfiable set has a linear refutation for some $D$.

A **linear derivation** from $S$ with top clause $C_0 \in S$ is a sequence $C_0, C_1, \ldots, C_r$ in which each $C_{i+1}$ is a [factor](/factoring/) of $C_i$, or a binary resolvent of $C_i$ and a side clause $B_i$. The side clause is a clause of $S$, a factor of one (or a factor of a factor, and so on), or an earlier center $C_j$ with $j < i$. It is a **linear refutation** when $C_r = \square$.

## The algorithm

The search is iterative deepening: it tries all chains of length 0, then 1, then 2, and so on, up to $D$.

```pseudo id=main
LINEAR-RESOLUTION(S, D)
L1  sides ← the clauses of S, their factors, the factors of those, and so on
L2  for d ← 0 to D
L3      for each clause T of S
L4          if SEARCH([T], d) then return UNSAT
L5  return UNKNOWN

SEARCH(chain, d)
L6  C ← the last center of chain; if C = □ then return true
L7  if d = 0, or S is ground and C has more than d literals, then return false
L8  moves ← the factors of C, and the binary resolvents of C with each clause of sides and with each earlier center of chain
L9  for each R in moves: if SEARCH(chain + [R], d − 1) then return true
L10 return false
```

Line L1 is finite, because a factor has fewer literals than its parent. Line L7 is a sound cut for ground input: a ground factor is the clause itself, and a ground resolvent loses at most one literal of the center, so a center with more than $d$ literals cannot reach $\square$ in $d$ steps. Each resolvent at line L8 is formed after the side clause is renamed apart.

## Example

Take the four clauses

$$0: p \vee q, \quad 1: \neg p \vee q, \quad 2: p \vee \neg q, \quad 3: \neg p \vee \neg q.$$

They are unsatisfiable: each of the four assignments of $p$ and $q$ makes one clause false. Every proper subset is satisfiable, so by the completeness theorem every clause can be the top clause. The search with top clause 0 finds this chain at depth 4:

| step | center | made from | side clause | why it is allowed |
|---|---|---|---|---|
| 0 | $C_0 = p \vee q$ | top clause | | clause 0 of $S$ |
| 1 | $C_1 = q$ | $C_0$, on $p$ | clause 1: $\neg p \vee q$ | input side |
| 2 | $C_2 = p$ | $C_1$, on $q$ | clause 2: $p \vee \neg q$ | input side |
| 3 | $C_3 = \neg q$ | $C_2$, on $p$ | clause 3: $\neg p \vee \neg q$ | input side |
| 4 | $C_4 = \square$ | $C_3$, on $q$ | $C_1 = q$ | earlier center |

The last step uses the earlier center $C_1$. Without it, the chain is an [input refutation](/input-resolution/), and this set has none, because no input clause has one literal. The tests check that no linear refutation of three steps exists, from any of the four top clauses.

## Correctness

Each center is a factor or a resolvent of clauses that follow from $S$, so UNSAT is always right. The search at lines L6 to L10 tries every move at every center, so it finds a linear refutation of at most $D$ steps whenever one exists with a top clause from $S$.

The completeness theorem says that one exists for some $D$. Let $S$ be unsatisfiable and let $C \in S$ be such that $S \setminus \{C\}$ is satisfiable. The ground case is an induction on the number of excess literals, the total number of literals minus the number of clauses. If $C$ is a unit $\{L\}$, delete the other clauses that contain $L$ and delete $\neg L$ from the rest, refute the result by induction, and put $\neg L$ back: the chain ends in $\square$ or in $\{\neg L\}$, which resolves with the top clause $\{L\}$, an earlier center. If $C$ has more literals, split off one literal $L$, refute $(S \setminus \{C\}) \cup \{C \setminus \{L\}\}$ to reach $\square$ or $\{L\}$, and then continue with a refutation of $(S \setminus \{C\}) \cup \{\{L\}\}$ from top clause $\{L\}$. The first-order case follows from [Herbrand's theorem](/herbrand-theorem/) and the [lifting lemma](/lifting-lemma/), applied to the chain one step at a time; the factors of centers and of input clauses take care of merged literals. The full proof is in the proof file.

## Complexity

Let $b$ be the largest number of moves at line L8 from one center, and count the making of one move as one operation. The chains of length at most $k$ form a tree with at most $\sum_{i \le k} b^i = O(b^k)$ nodes for $b \ge 2$. Iterative deepening runs the search for $k = 0, 1, \ldots, d$, and each node makes at most $b$ moves, so the time is $\sum_{k \le d} O(b^{k+1}) = O(b^{d+1})$. The recursion is at most $d$ levels deep, and each level holds its list of at most $b$ moves, so the extra space is $O(b d)$, apart from the clauses themselves.

For ground input with $n$ atoms and $m$ clauses, a center has at most $n$ literals, and it resolves with at most $m + d$ sides on at most $n$ literals each, so $b \le n(m + d)$. On first-order input $b$ also counts the factors, and the search does not stop on its own: that is why line L2 has the bound $D$.

## Properties

- **Sound.** Every UNSAT answer comes with a chain that a checker can verify.
- **Refutation complete.** Every unsatisfiable set has a linear refutation, with any top clause $C$ such that $S \setminus \{C\}$ is satisfiable.
- **Bounded.** The search of this page is complete only up to the depth bound $D$. UNKNOWN means that there is no refutation of at most $D$ steps from the tried top clauses.
- **Memory light.** Depth-first search keeps one chain and one list of moves per level.
- **Ancestors are needed.** Linear input refutations, which use only input side clauses, are not complete; the example needs the earlier center $C_1$.

## Variants and improvements

- **Linear input resolution.** Allow only input side clauses. It is complete for [Horn clauses](/horn-clause/) and not in general; see [input resolution](/input-resolution/).
- **SLD resolution.** For Horn clauses with a negative top clause, linear input resolution with a rule that selects the literal to resolve is [SLD resolution](/sld-resolution/), the basis of Prolog.
- **Model elimination and SL resolution.** Loveland's model elimination (1968) and the SL resolution of Kowalski and Kuehner (1971) keep the resolved literals of the chain and allow a center to be resolved only with an ancestor whose literal is the complement of a kept literal. This cuts the search much more, and it is the basis of connection-tableau provers such as SETHEO and leanCoP.
- **Set of support.** A linear refutation whose top clause is in a support set is also a [set-of-support](/set-of-support/) refutation, because every center descends from the top clause.
- **Saturation instead of search.** A given-clause prover explores all chains at once and shares common sub-chains, at the cost of memory.

## When to use it

Use linear resolution when memory is short or when goal-directed search pays, as for logic programs and for problems with one clear goal clause. Pick the negated goal as the top clause, because the axioms alone are usually satisfiable, so the theorem applies. For problems where many clauses interact, or with equality, saturation provers based on [superposition](/superposition/) do better.

## Pitfalls

- **Only input side clauses.** If line L8 drops the earlier centers, the search fails on the four clauses of the example. Keep the centers of the chain as side clauses.
- **A bad top clause.** If the top clause is not needed for the contradiction, there may be no refutation from it. In $\{p,\ \neg p,\ q\}$ the chain from $q$ never reaches $\square$, because $q$ cannot be resolved. Choose a top clause $C$ such that $S \setminus \{C\}$ is satisfiable, such as the negated goal, or try every top clause as line L3 does.
- **No factors of side clauses.** If line L1 keeps only the clauses of $S$, a ground instance of a side clause can merge two literals that the chain cannot merge, and the lifting argument fails. Line L1 adds all factors of input clauses.
- **The literal count cut on first-order input.** On first-order input one factor can merge many literals, so line L7 may use the cut "more literals than steps left" only when the input is ground.
- **Depth-first search without a bound.** Without line L2, depth-first search can follow an infinite chain, such as $P(a), P(f(a)), P(f(f(a))), \ldots$, and never come back. Use iterative deepening or another bound.

## Implementations

## History

Donald Loveland introduced model elimination in 1968, a linear proof procedure with a special treatment of ancestors. In 1970 Loveland ("A linear format for resolution") and David Luckham ("Refinement theorems in resolution theory") proved, in the same volume of the Symposium on Automatic Demonstration, that linear resolution is refutation complete. Robert Anderson and Woody Bledsoe (1970) gave the short proof by induction on excess literals that this page follows. Robert Kowalski and Donald Kuehner (1971) added a selection function, which led to SL resolution, and the Horn case became SLD resolution and the logic programming of Kowalski and Colmerauer.

## References
