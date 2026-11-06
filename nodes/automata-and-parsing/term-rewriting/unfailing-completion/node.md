---
tag: FECHPF
kind: algorithm
slug: unfailing-completion
name: Unfailing completion
aliases:
- unfailing Knuth-Bendix
- Bachmair-Dershowitz-Hsiang completion
area: automata-and-parsing/term-rewriting
level: research
summary: Completion that works on equations without orienting them first.
solves: [word-problem]
model: word-ram
complexity:
  vars: {k: the number of steps of the main loop, a: the largest number of active equations, m: the largest size of a term that occurs, N: the largest number of ordered rewrite steps in one normalization}
  time: {worst: O(k N a^3 m^5)}
  space: {extra: O(k a^2 m^2)}
properties: {deterministic: true, recursive: true, online: false}
prereqs: [knuth-bendix-completion, lexicographic-path-ordering, critical-pair-lemma]
see_also: [rewrite-system-completion, word-problem, newman-lemma, superposition, paramodulation, demodulation, rewriting-modulo-equations, inductive-theorem-proving]
sources:
  - paper: doi:10.1016/B978-0-12-046371-8.50007-9
    title: Leo Bachmair, Nachum Dershowitz and David A. Plaisted, Completion without failure, in H. Aït-Kaci and M. Nivat (editors), Resolution of Equations in Algebraic Structures, volume 2, Rewriting Techniques, Academic Press, 1989
    locator: chapter 1, pp. 1 to 30 (ordered rewriting, ordered critical pairs, and completeness of unfailing completion)
  - paper: doi:10.1007/3-540-18088-5_6
    title: Jieh Hsiang and Michaël Rusinowitch, On word problems in equational theories, ICALP 1987, Lecture Notes in Computer Science 267, Springer
    locator: pp. 54 to 71
  - paper: doi:10.1145/174652.174655
    title: Leo Bachmair and Nachum Dershowitz, Equational inference, canonical proofs, and proof orderings, Journal of the ACM 41(2) (1994)
    locator: pp. 236 to 276 (completion as an inference system, proof orderings, fairness)
---

**Unfailing completion** is a version of [Knuth-Bendix completion](/knuth-bendix-completion/) that does not stop when an equation cannot be oriented. It keeps such an equation, like commutativity $x + y \approx y + x$, as an equation, and uses an instance of it only in the direction that makes the term smaller in a fixed order that is total on ground terms. Critical pairs are computed the same way, between equations rather than rules. When the run stops, the result decides the [word problem](/word-problem/) for ground terms, and when it runs forever it still gives a semi-decision procedure.

## In plain words

Completion turns a list of laws into rewrite rules that always simplify. It needs each law to have a "bigger side" that it can replace by the smaller side. Some laws have none: swapping the two arguments of an addition gives a term of the same shape and size, so neither side is bigger. Ordinary completion gives up there.

Unfailing completion keeps such a law and uses it case by case. Given a concrete term, it swaps the arguments only if the result comes earlier in a fixed order, like alphabetical order. Every concrete term then has one simplest form. The procedure adds laws, just as completion adds rules, until every way of simplifying a term leads to the same result. Two concrete terms are equal under the laws exactly when they simplify to the same term.

## The problem

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, positions as sequences of integers, $t|_p$ for the subterm at $p$ and $t[u]_p$ for the replacement, substitutions $\sigma$ applied on the right, rules $l \to r$, and $\to^*$ for the reflexive transitive closure. An equation is written $s \approx t$ and can be used in both directions.

**Input.** A finite set $E$ of equations and a precedence, a strict total order on $\Sigma$. Each equation is **regular**: both sides have the same variables. $\Sigma$ has at least one constant, so ground terms exist.

**The order.** $>$ is the [lexicographic path ordering](/lexicographic-path-ordering/) for the precedence. It is well-founded, closed under contexts and substitutions, and total on ground terms: for ground $s \neq t$, either $s > t$ or $t > s$. On terms with variables it is partial; $f(x, y)$ and $f(y, x)$ are incomparable.

**Ordered rewriting.** For a set $A$ of equations, $s \to_A t$ if $s|_p = u\sigma$ and $t = s[v\sigma]_p$ for some $u \approx v$ or $v \approx u$ in $A$, and $u\sigma > v\sigma$. Every step makes the term smaller, so ordered rewriting terminates, and $s{\downarrow}_A$ denotes the normal form that the implementation reaches.

**Ordered critical pairs.** Let $u_1 \approx v_1$ and $u_2 \approx v_2$ be directions of two equations with disjoint variables, $p$ a non-variable position of $u_1$, and $\sigma$ a [most general unifier](/most-general-unifier/) of $u_1|_p$ and $u_2$. If neither $v_1\sigma > u_1\sigma$ nor $v_2\sigma > u_2\sigma$, the pair $u_1\sigma[v_2\sigma]_p \approx v_1\sigma$ is an ordered critical pair. A direction of an equation that $>$ orients the other way is not used at all.

**Output.** A finite set $A$ of equations such that, for all ground terms $s$ and $t$, $s \approx t$ follows from $E$ if and only if $s{\downarrow}_A = t{\downarrow}_A$; or a report that the step bound was reached.

## The algorithm

The procedure keeps a set of active equations and a priority queue of pending ones, and moves pending equations into the active set one at a time.

```pseudo id=main
UNFAILING-COMPLETE(E, >, B)
L1  A ← ∅; queue the equations of E; steps ← 0
L2  while steps < B do
L3      if the queue is empty then P ← ordered critical pairs ⟨u,v⟩ of A with u↓A ≠ v↓A
L4          if P is empty then return SATURATED(A) else queue P; continue
L5      remove a smallest equation s ≈ t from the queue; steps ← steps + 1
L6      s ← s↓A; t ← t↓A                                            ▷ simplify
L7      if s = t or s ≈ t is a variant of an equation in A then continue    ▷ delete
L8      if t > s then swap s and t                                    ▷ orient if possible
L9      for each equation in A that s ≈ t rewrites: remove it from A and queue it
L10     add s ≈ t to A
L11     queue the ordered critical pairs of s ≈ t with every equation of A, in both orders
L12 return GIVE-UP(A)
```

Line L5 takes the equation with the fewest symbols, the oldest first among equal sizes. Line L7 compares equations up to renaming of variables and up to the swap of sides. Line L8 does not fail: if neither side is larger, the equation is stored as it is, and ordered rewriting decides on each instance. Line L9 moves an equation back to the queue when the new equation rewrites one of its sides, as collapse does in Knuth-Bendix completion. Line L3 recomputes all ordered critical pairs of the final set, including those of each equation with a renamed copy of itself, so the answer does not depend on what line L9 removed.

Rewriting, matching, unification and renaming in the implementation use explicit stacks. The order is compared by a memoized recursion, which visits each pair of subterms once.

## Example

**Commutativity.** $E = \{f(x, y) \approx f(y, x)\}$ with $f > b > a$. Knuth-Bendix completion fails at once, since neither side is larger. Unfailing completion keeps the equation; all its ordered critical pairs with itself are trivial, so the run is saturated with $A = E$. A ground term rewrites by swapping arguments when the swap makes it smaller: $f(b, a) \to f(a, b)$ because $b > a$, and $f(a, b)$ is a normal form.

**Commutativity with a unit.** Add $f(x, a) \approx x$. With the same precedence:

| step | equation taken | result |
| --- | --- | --- |
| 1 | $f(x, a) \approx x$ | added, oriented $f(x, a) \to x$ |
| 2, 3 | $x' \approx x'$, critical pairs of $f(x, a) \approx x$ with itself | trivial, deleted |
| 4 | $f(x, y) \approx f(y, x)$ | added, not orientable |
| 5 | $x' \approx f(a, x')$ | added, oriented $f(a, x') \to x'$ |
| 6 to 24 | the remaining critical pairs | trivial or variants, deleted |

The critical pair at step 5 comes from unifying $f(x', a)$ with $f(x, y)$: commutativity gives $f(a, x')$ and the unit gives $x'$. The run is saturated after 24 steps with $A = \{f(x, a) \approx x,\ f(x, y) \approx f(y, x),\ f(a, x) \approx x\}$. Now $f(f(a, b), f(b, a)) \to f(b, f(b, a)) \to f(b, b)$: the swap at the top is not allowed, since $f(f(b, a), f(a, b))$ is larger, so the first step uses $f(a, x) \to x$ inside and the second $f(x, a) \to x$. Likewise $f(f(b, a), a) \to f(b, a) \to b$. So these terms are equal to $f(b, b)$ and $b$ under $E$, and $f(b, b) \neq b$ in $E$ because both are normal forms.

**Groups.** For $e \cdot x \approx x$, $i(x) \cdot x \approx e$, $(x \cdot y) \cdot z \approx x \cdot (y \cdot z)$ with $i > \cdot > e$, the run is saturated after 143 steps with the ten equations of the classical complete system for groups, among them $i(x \cdot y) \approx i(y) \cdot i(x)$ and $i(i(x)) \approx x$. All ten are oriented, so the result is an ordinary convergent rewrite system, as Knuth-Bendix completion would give.

**A run that does not stop.** For $h(g(h(x))) \approx h(g(x))$ with $h > g$, the critical pair of the equation with itself at position $1.1$ gives $h(g(g(h(x)))) \approx h(g(g(x)))$, and each new equation gives the next one. After 25 steps the active set is $h(g^n(h(x))) \approx h(g^n(x))$ for $n = 1, \ldots, 6$, and the run returns at the bound without a result.

## Correctness

The full proof is below. The argument assumes regular equations; every equation the run creates is then regular as well, since a critical pair replaces a subterm by a term with the same variables.

1. **Soundness.** Every equation added to the queue follows from $E$: critical pairs and simplified equations are derived by replacing equals by equals. So the final $A$ only relates terms equal under $E$.
2. **No loss.** The equations of $A$ together with those in the queue always have the same equational consequences as $E$. Line L6 replaces an equation by one that, together with $A$, implies it; lines L7 and L9 only delete equations that $A$ implies or move them back to the queue. When line L4 returns, the queue is empty, so $A$ and $E$ have the same consequences.
3. **Ground confluence.** On ground terms ordered rewriting with $A$ terminates, so by [Newman's lemma](/newman-lemma/) it is enough to join every one-step peak. A peak at an overlap of two equations is an instance of an ordered critical pair, because the order is closed under substitution; line L3 found its two sides with the same normal form, and that joining sequence is closed under ground substitution. A peak where one step is inside the substitution part of the other is joined by rewriting the other copies of the variable, and then using the equation in whichever direction the total order allows. Disjoint peaks commute.
4. **The answer.** For ground $s, t$, $s \approx t$ follows from $E$ iff it follows from $A$, iff $s$ and $t$ are connected by steps of $A$ on ground terms; each such step goes down in one direction or the other, since the order is total on ground terms. By ground confluence the two terms have the same normal form.

## Complexity

There is no bound in terms of the input: the run may not stop, as in the example above, and when it stops the result can be much larger than $E$. Let $k$ be the number of steps, $a$ the largest number of active equations, $m$ the largest term size that occurs, and $N$ the largest number of ordered steps in one normalization.

- **One comparison.** The memoized path ordering makes at most $|s| \cdot |t|$ calls, each with an $O(m)$ equality or occurrence test, so $O(m^3)$.
- **One normalization.** Each ordered step tries $m$ positions and $2a$ directions, with a match and a comparison each, so $O(a m^4)$ per step and $O(N a m^4)$ per term.
- **One step.** The critical pairs of the new equation with $a$ equations cost $O(a m^4)$, with unification in $O(m^3)$. Simplifying the active set costs the same.
- **The final check.** Line L3 normalizes the $O(a^2 m)$ ordered critical pairs of $A$, which costs $O(N a^3 m^5)$. Each check that does not return is followed by at least one step, so there are at most $k + 1$ checks, and the total time is $O(k N a^3 m^5)$.
- **Space.** Each step queues $O(a m)$ pairs and each check $O(a^2 m)$, each of size $O(m)$, so the queue takes $O(k a^2 m^2)$.

## Properties

- **Never fails.** Unlike Knuth-Bendix completion, no equation stops the run for lack of orientation. The run stops with a saturated set or reaches the bound.
- **Ground decision procedure.** A saturated result decides the word problem of $E$ for ground terms. For equations with variables, replace the variables by new constants, placed anywhere in the precedence; then $s \approx t$ holds in $E$ iff the resulting ground terms have the same normal form.
- **Semi-decision procedure.** Bachmair, Dershowitz and Plaisted (1989) show that a fair run without a bound produces in the limit a set that proves every true ground equation by ordered rewriting. So any true equation is eventually confirmed, even when the run never stops.
- **Generalizes completion.** If every equation of the result is oriented, the result is an ordinary convergent rewrite system, as in the group example.

## Variants and improvements

- **Refutational goal proving.** Hsiang and Rusinowitch (1987) use the procedure to prove a goal $s \approx t$: the variables of the goal become new constants, and the goal is simplified by the active equations during the run until its two sides meet.
- **Ground joinability tests.** The test at line L3 asks for identical normal forms with variables. Stronger tests check that every ground instance of a critical pair is joinable, for example by splitting into cases on the order of the variables. They are needed for theories like associativity and commutativity, where the simple test never succeeds.
- **Inference systems.** Bachmair and Dershowitz (1994) present completion as inference rules (deduce, orient, simplify, delete, collapse, compose) with a proof ordering. Any fair strategy of rule application is complete, which separates correctness from the choice of the next equation.
- **Superposition.** [Superposition](/superposition/) extends ordered critical pairs and ordered rewriting from equations to clauses, which gives a complete calculus for first-order logic with equality. [Demodulation](/demodulation/) is its name for the simplification at lines L6 and L9.

## When to use it

Use unfailing completion when the equations include permutative laws, such as commutativity, or other equations that no reduction order can orient, and Knuth-Bendix completion fails. It is also the right tool for proving a single equation from axioms, where a finite complete system is not needed and the run can stop as soon as the goal is proved. When a finite convergent system exists and the order orients everything, plain completion gives the same result with simpler data structures.

## Pitfalls

- **Regular equations only.** If one side of $u \approx v$ has a variable that the other lacks, the direction $u \to v$ creates new variables and cannot be used on ground terms. This implementation drops such directions, and its correctness argument does not cover such input.
- **Totality matters.** The precedence must be total on $\Sigma$. With a partial precedence two different ground terms can be incomparable, and a variable overlap may then not be joinable.
- **The order condition is checked on instances.** A direction $u \to v$ of an unoriented equation may rewrite $u\sigma$ only if $u\sigma > v\sigma$. Using it whenever $u$ matches makes rewriting loop, as for commutativity.
- **Associativity and commutativity.** With the identical-normal-form test, the run on associativity and commutativity never reports saturation, although the ground instances are joinable. Use a ground joinability test or rewriting modulo the theory.
- **Recursion depth.** The memoized order comparison recurses to depth at most the sum of the term depths, so very deep terms need a raised recursion limit or a stack-based comparison.

## Implementations

## History

Knuth-Bendix completion, from 1970, fails on an equation that the order cannot orient. Hsiang and Rusinowitch (1987) gave a completion procedure for equational theories that uses unorientable equations by ordered rewriting, and proved it complete for proving equations. Bachmair, Dershowitz and Plaisted (1989) presented unfailing completion with ordered critical pairs and proved it complete. Bachmair and Dershowitz (1994) gave the proof ordering framework in journal form, in which completion is a set of inference rules and correctness follows from fairness.

## References
