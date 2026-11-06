---
tag: 4TKTY0
kind: algorithm
slug: narrowing
name: Narrowing
aliases:
- basic narrowing
- narrowing-based E-unification
- narrowing-based solving
area: automata-and-parsing/term-rewriting
level: advanced
summary: Rewriting with unification in place of matching, to solve equations and goals.
solves: [equational-unification]
model: word-ram
complexity:
  vars: {n: the size of the goal s = t, D: the depth bound, r: the number of rules, M: the largest size of a goal in the search}
  time: {worst: O((r M)^(D+1) M^2), best: Θ(n)}
  space: {extra: O((r M)^D M)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1980
  people: [Jean-Marie Hullot]
  note: Slagle used narrowing steps in theorem proving in 1974 and Fay used them for unification in 1979; Hullot proved in 1980 that narrowing finds a complete set of unifiers for every convergent system.
prereqs: [most-general-unifier, rewrite-step, confluence, termination]
see_also: [equational-unification, knuth-bendix-completion, innermost-reduction, logic-programming, sld-resolution, rewriting-logic, term-matching, word-problem]
sources:
  - paper: doi:10.1007/3-540-10009-1_25
    title: Jean-Marie Hullot, Canonical forms and unification, 5th Conference on Automated Deduction, Lecture Notes in Computer Science 87, Springer, 1980
    locator: pp. 318 to 334 (narrowing and basic narrowing, the lifting lemma, and completeness for canonical systems)
  - paper: doi:10.1145/321850.321859
    title: James R. Slagle, Automated theorem-proving for theories with simplifiers, commutativity, and associativity, Journal of the ACM 21(4) (1974)
    locator: pp. 622 to 642 (the narrowing inference in resolution theorem proving with simplifiers)
  - paper: doi:10.1145/347476.347484
    title: Sergio Antoy, Rachid Echahed and Michael Hanus, A needed narrowing strategy, Journal of the ACM 47(4) (2000)
    locator: pp. 776 to 822 (needed narrowing for inductively sequential systems, its soundness, completeness and optimality)
---

**Narrowing** solves equations modulo a [term rewriting system](/term-rewriting-system/): given $s \approx t$ with variables, it finds substitutions $\theta$ such that $s\theta$ and $t\theta$ rewrite to the same term. A narrowing step is a rewrite step in which [matching](/term-matching/) is replaced by [unification](/most-general-unifier/): at a non-variable subterm of the goal, unify with a rule's left side, apply the unifier to the whole goal, and replace the subterm by the right side. Searching all narrowing derivations is sound for every system, and for a convergent system it finds every solution, up to instances. It is the standard method for [equational unification](/equational-unification/) with a convergent system, and the operational semantics of functional logic programming languages such as Curry.

## In plain words

Ordinary rewriting evaluates: it takes a fully known expression and simplifies it with the rules. Narrowing works with unknowns. When an expression contains an unknown $x$, and a rule could apply if $x$ had a certain shape, narrowing guesses that shape, records the guess, and applies the rule. For the question "which $x$ gives $x + 1 = 2$?", it tries $x = 0$, which gives $1 = 2$, a dead end, and $x = x' + 1$, which leads on to $x' = 0$. The recorded guesses form the answer $x = 1$. Trying all guesses, level by level, finds all answers, but the search can be very large.

## The problem

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, positions as sequences of positive integers with root $\varepsilon$, subterm $t|_p$ and replacement $t[s]_p$, substitutions $\sigma$ applied as $t\sigma$, rules $l \to r$ with $l \notin V$ and $\mathrm{Var}(r) \subseteq \mathrm{Var}(l)$, and $\to_R^*$ for the reflexive transitive closure.

The input is a finite set $R$ of rules, a goal $s \approx t$, and a depth bound $D$. A **solution**, or $R$-unifier, is a substitution $\theta$ with $s\theta \leftrightarrow_R^* t\theta$. The output is a list of answers: substitutions on the variables of the goal that are solutions, such that, for a convergent $R$, every solution whose values are normal forms is an instance of an answer once $D$ is large enough. This is [equational unification](/equational-unification/) for the theory of $R$.

A **narrowing step** $e \leadsto_{p, l \to r, \tau} e'$ takes a position $p$ of $e$ with $e|_p \notin V$, a rule $l \to r$ with variables renamed apart from $e$, and a most general unifier $\tau$ of $e|_p$ and $l$, and sets $e' = (e[r]_p)\tau$. Then $e\tau \to_R e'$: a narrowing step is a rewrite step of an instance.

## The algorithm

The goal is kept as the term $\mathrm{eq}(s, t)$, so that positions in both sides can be narrowed. Each node of the search holds a goal, the composed substitution on the variables of $s$ and $t$, and a depth.

```pseudo id=main
NARROW(s, t, R, D)
L1  queue ← [(eq(s, t), id, 0)]; answers ← []
L2  while queue is not empty do
L3      (eq(u, v), σ, d) ← remove the first node of queue
L4      if u and v unify with mgu μ then add σμ, restricted to Var(s, t), to answers
L5      if d = D then continue
L6      for each position p of eq(u, v) other than the root, with eq(u, v)|p not a variable do
L7          for each rule l → r of R, renamed with fresh variables do
L8              if eq(u, v)|p and l unify with mgu τ then
L9                  append ((eq(u, v)[r]p)τ, στ, d + 1) to queue
L10 return answers
```

Line L4 is the success test: once the two sides unify syntactically, the composed substitution is an answer. A goal is not removed when it succeeds, because further narrowing can give other answers. Lines L6 to L9 create all narrowing steps from the goal, and the queue makes the search [breadth-first](/breadth-first-search/), so every derivation of length at most $D$ is explored.

Unification is Robinson's algorithm with an occurs check, written with an explicit stack and a triangular substitution, and the result is applied fully, so each $\mu$ and $\tau$ is idempotent. Rule variables are renamed with a counter, so they never clash with variables already in the goal. The implementation removes repeated answers and renames the fresh variables in each answer to $\_1, \_2, \ldots$.

## Example

Peano addition $R = \{ \mathit{add}(0, y) \to y,\ \mathit{add}(s(x), y) \to s(\mathit{add}(x, y)) \}$, numbered 1 and 2, with $k$ for $s^k(0)$. The goal is $\mathit{add}(x, 1) \approx 2$ with $D = 3$.

| node | depth | goal | $\sigma$ on $x$ | L4 | created by |
|---|---|---|---|---|---|
| A | 0 | $\mathit{add}(x, 1) \approx 2$ | $x$ | fails | L1 |
| B | 1 | $1 \approx 2$ | $0$ | fails | A, rule 1 at position 1, $\tau = \{ x \mapsto 0, y_1 \mapsto 1 \}$ |
| C | 1 | $s(\mathit{add}(x_2, 1)) \approx 2$ | $s(x_2)$ | fails | A, rule 2 at position 1, $\tau = \{ x \mapsto s(x_2), y_2 \mapsto 1 \}$ |
| D | 2 | $2 \approx 2$ | $s(0)$ | **answer** $x \mapsto 1$ | C, rule 1 at position 1 1 |
| E | 2 | $s(s(\mathit{add}(x_3, 1))) \approx 2$ | $s(s(x_3))$ | fails | C, rule 2 at position 1 1 |
| F | 3 | $3 \approx 2$ | $s(s(0))$ | fails | E, rule 1 |
| G | 3 | $s^3(\mathit{add}(x_4, 1)) \approx 2$ | $s^3(x_4)$ | fails | E, rule 2 |

Node B has no narrowing steps, since no left side unifies with a subterm of $1$ or $2$. The answer is $\{ x \mapsto 1 \}$, found at depth 2. With $D = 1$ there is no answer, and with a larger $D$ the branch through G keeps growing without new answers: the search space is infinite, which is why a depth bound is needed.

The goal $\mathit{add}(x, y) \approx 2$ with $D = 4$ gives the three answers $\{x \mapsto 0, y \mapsto 2\}$, $\{x \mapsto 1, y \mapsto 1\}$ and $\{x \mapsto 2, y \mapsto 0\}$, in this order. With the list rules $\mathit{app}(\mathit{nil}, y) \to y$ and $\mathit{app}(\mathit{cons}(x, y), z) \to \mathit{cons}(x, \mathit{app}(y, z))$, the goal $\mathit{app}(x, y) \approx [a, b]$ gives the three ways to split the list.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). It has two parts.

1. **Soundness, for every system.** If $(e, \sigma, d)$ is a node, then $\mathrm{eq}(s, t)\sigma \to_R^d e$, because each narrowing step is a rewrite step of an instance and rewriting is closed under substitutions. So an answer $\alpha = \sigma\mu$ gives $s\alpha \to_R^* w \leftarrow_R^* t\alpha$ with at most $D$ steps in total. This needs neither termination nor confluence.
2. **Completeness, for a convergent system (Hullot).** Let $\theta$ be a solution whose values are normal forms. Then $\mathrm{eq}(s\theta, t\theta)$ has an innermost reduction to $\mathrm{eq}(w, w)$ of some length $n$. The **lifting lemma** turns each innermost step of an instance $e\eta$, with $\eta$ normalized, into a narrowing step from $e$: the redex cannot lie inside $\eta$, since its values are normal forms, so it sits at a non-variable position of $e$, and $\eta$ together with the rule's matcher unifies that subterm with the left side. By induction the search reaches, at depth $n$, a goal whose sides are unified by an instance of the answer it gives, and $\theta$ is an instance of that answer. So $D \ge n$ suffices.

The restriction to normalized solutions loses nothing for a convergent system: normalizing the values of a solution gives a solution equal to it modulo $R$.

## Complexity

**Branching.** A goal of size $M$ has at most $M$ non-variable positions and each of them is tried with $r$ rules, so a node has at most $r M$ children. There are $O((r M)^D)$ nodes up to depth $D$. Each node costs one unification of its two sides and $r M$ unifications for its children, each $O(M^2)$ with the simple occurs check, plus $O(M)$ to build each child. The total time is $O((r M)^{D+1} M^2)$ on the [word RAM](/word-ram/), where $M$ is the largest goal size in the search; $M$ can grow with the depth, since right sides and unifiers can make terms larger. The best case is $\Theta(n)$, for $D = 0$ and two sides with different root symbols.

**Space.** The queue of breadth-first search holds a whole level, $O((r M)^D)$ goals of size $O(M)$ each.

**The search is exponential and may be infinite.** Unrestricted narrowing explores many redundant derivations: the same solution can be reached by narrowing at different positions in different orders. Equational unification modulo a convergent system is undecidable in general, so no bound on $D$ can be computed from the goal.

## Properties

- **Sound for every system, complete for convergent ones.** Without confluence completeness fails: with $\{ a \to b,\ a \to c \}$, $b \approx c$ holds modulo $R$ but narrowing finds nothing. Without termination, Hullot's proof does not apply, and the lifting needs other arguments.
- **Normalized solutions only.** With $R = \{ f(a) \to b \}$, the solution $x \mapsto f(a)$ of $x \approx b$ is not an instance of the only answer $x \mapsto b$, but it is equal to it modulo $R$.
- **Answers are general.** An answer may keep variables, and it then stands for all its instances: $\mathit{add}(x, y) \approx s(z)$ has the answer $\{ x \mapsto s(x'), z \mapsto \mathit{add}(x', y) \}$ at depth 1. Its value for $z$ is not a normal form; normalizing the answers with $R$ is a common improvement.
- **Generalizes rewriting and unification.** For a ground goal, narrowing steps are rewrite steps. For the empty system, the only answer is the syntactic most general unifier of $s$ and $t$.

## Variants and improvements

- **Basic narrowing.** Hullot's restriction: never narrow at a position that was introduced by a unifier, only at positions of the original goal and of right sides inserted later. It is still complete for convergent systems, and it terminates for some systems, for example when the right sides of all rules are variables or ground, which gives a decision procedure for unification in those theories.
- **Normalizing narrowing.** Normalize each goal with $R$ before narrowing it again (Fay). Since $R$ is convergent, this loses no solutions and cuts many branches, including all goals whose normal forms clash at the root.
- **Innermost and outermost strategies.** Narrow only at innermost positions, as in call-by-value, or use lazy narrowing, which narrows at an outer position as soon as the root needs it.
- **Needed narrowing.** For inductively sequential systems, such as functional programs defined by pattern matching on constructors, Antoy, Echahed and Hanus defined needed narrowing. It narrows only at positions that are needed, computes only disjoint answers, and is optimal in the number of steps. It is the operational semantics of Curry.
- **Narrowing modulo axioms.** With associativity and commutativity built in, narrowing uses AC unification at each step, as in Maude's narrowing for symbolic analysis of cryptographic protocols. See [rewriting logic](/rewriting-logic/).
- **Relation to logic programming.** [SLD resolution](/sld-resolution/) of [logic programming](/logic-programming/) is a form of narrowing in which predicates are functions to the Booleans, and narrowing adds functions with evaluation to logic programs.

## When to use it

Use narrowing to solve equations, or to find inputs that make a term reduce to a given value, modulo a convergent system: equational unification after [Knuth-Bendix completion](/knuth-bendix-completion/), queries in functional logic programs, test case generation and symbolic execution of rewrite specifications, and reachability analysis of protocols. Use a restricted strategy, basic, normalizing or needed narrowing, rather than the plain search on this page, and a depth or time bound. For syntactic unification, use a unification algorithm directly; for checking a ground equation, normalize both sides.

## Pitfalls

- **Not renaming the rule apart.** If a rule shares a variable with the goal, the unifier mixes them and gives wrong answers. Rename at each use, not once per rule, since the same rule can be used many times in one derivation.
- **Narrowing at variable positions.** Unifying a variable of the goal with a left side gives no information and makes the search infinite at once; such steps are excluded, and completeness does not need them because the solutions are normalized.
- **Depth-first search.** Following the first branch can loop forever on the infinite branch in the example while answers wait elsewhere. Use breadth-first search, iterative deepening or a fair strategy.
- **Stopping at the first success.** A goal that unifies can still narrow further to other answers; line L4 records the answer and the search continues.
- **Expecting completeness without convergence.** For a system that is not confluent or not terminating, the answers are correct, but some solutions can be missed.
- **Deep terms.** Goals such as $\mathit{add}(x, s^{800}(0)) \approx s^{801}(0)$ are deep. The implementation unifies, substitutes and replaces with explicit stacks, and turns terms into strings without recursion when it compares answers.

## Implementations

## History

Slagle in 1974 used narrowing steps as an inference in resolution theorem proving with simplifying equations. Fay in 1979 used narrowing to compute unifiers modulo an equational theory given by a convergent system, and Hullot in 1980 gave the lifting lemma, the completeness proof for convergent systems, and basic narrowing. In the 1980s narrowing became the operational semantics of languages that combine functional and logic programming, and many strategies were proposed to cut its search space. Antoy, Echahed and Hanus introduced needed narrowing in 1994, published in full in 2000, which is the basis of the language Curry. Narrowing modulo axioms is used in Maude for symbolic reachability and protocol analysis.

## References
