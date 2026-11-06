---
tag: WM035M
kind: algorithm
slug: knuth-bendix-completion
name: Knuth-Bendix completion
aliases:
- Knuth-Bendix procedure
- completion procedure
area: automata-and-parsing/term-rewriting
level: advanced
summary: Turns a set of equations into a confluent, terminating rewrite system by adding critical-pair rules.
solves: [rewrite-system-completion]
model: word-ram
complexity:
  vars: {n: the total size of the input equations, k: the number of iterations of the main loop, r: the largest number of rules, m: the largest size of a term that occurs, N: the largest number of rewrite steps in one normalization}
  time: {worst: O(k N r^3 m^3), best: Θ(n)}
  space: {extra: O((k + r) r m^2)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1970
  people: [Donald E. Knuth, Peter B. Bendix]
  note: Knuth and Bendix gave the procedure and used it to find complete systems for groups and other theories; Huet proved in 1981 that a fair version is correct when it runs forever.
prereqs: [critical-pair-lemma, newman-lemma, well-founded-reduction-ordering, most-general-unifier]
see_also: [word-problem, lexicographic-path-ordering, knuth-bendix-ordering, unfailing-completion, critical-pair, birkhoff-completeness-theorem, rewriting-modulo-equations, buchberger-algorithm]
sources:
  - paper: doi:10.1016/B978-0-08-012975-4.50028-X
    title: Donald E. Knuth and Peter B. Bendix, Simple word problems in universal algebras, in J. Leech (editor), Computational Problems in Abstract Algebra, Pergamon Press, 1970
    locator: pp. 263 to 297 (the completion procedure, the critical pair test, and the complete system for groups)
  - paper: doi:10.1016/0022-0000(81)90002-7
    title: Gérard Huet, A complete proof of correctness of the Knuth-Bendix completion algorithm, Journal of Computer and System Sciences 23(1) (1981)
    locator: pp. 11 to 21 (fairness, persistent rules, and correctness of runs that do not stop)
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Chapter 7, Completion (the basic procedure, completion as an inference system, and its correctness)
  - paper: doi:10.1145/174652.174655
    title: Leo Bachmair and Nachum Dershowitz, Equational inference, canonical proofs, and proof orderings, Journal of the ACM 41(2) (1994)
    locator: pp. 236 to 276 (completion as inference rules, proof orderings, and critical pair criteria)
---

**Knuth-Bendix completion** takes a set $E$ of equations and a [reduction order](/well-founded-reduction-ordering/) $>$, and tries to build a [term rewriting system](/term-rewriting-system/) $R$ that is terminating, [confluent](/confluence/), and proves the same equations as $E$. It orients each equation into a rule that goes down in $>$, computes the [critical pairs](/critical-pair/) of the rules, and adds as new equations those that the rules cannot join. On success, two terms are equal under $E$ exactly when they have the same normal form under $R$, so $R$ decides the [word problem](/word-problem/) of $E$. The procedure can also fail, on an equation that $>$ cannot orient, or run forever, so the implementation takes a step bound.

## In plain words

Start with some facts of the form "this expression equals that one". Turn each fact into a one-way simplification rule, from the bigger side to the smaller side. Then look for expressions that two rules can simplify in two different ways. If the two results do not simplify to the same thing, that is a new fact, and it becomes a new rule. Repeat. Clean up the rules on the way: simplify their right sides, and drop a rule whose left side a newer rule can simplify.

When nothing new comes up, the rules always lead each expression to the same simplest form, whatever order they are used in. Two expressions are then equal by the facts exactly when their simplest forms are the same.

## The problem

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, positions as sequences of positive integers with root $\varepsilon$, subterm $t|_p$ and replacement $t[s]_p$, substitutions $\sigma$ applied as $t\sigma$, rules $l \to r$, and $\to_R^*$ for the reflexive transitive closure of the rewrite relation of $R$. $\leftrightarrow_E^*$ is the conversion of a set of equations $E$, which by the [Birkhoff completeness theorem](/birkhoff-completeness-theorem/) is the set of equations that hold in all models of $E$. $u{\downarrow}_R$ is a normal form of $u$ under $R$.

The input is a finite set $E_0$ of equations, a reduction order $>$ (well-founded, closed under contexts and substitutions) such as the [lexicographic path ordering](/lexicographic-path-ordering/) or the [Knuth-Bendix ordering](/knuth-bendix-ordering/), and a step bound $B$. The goal is the [rewrite system completion](/rewrite-system-completion/) problem: a finite $R$ with $l > r$ for each rule, confluent, and with $\leftrightarrow_R^* = \leftrightarrow_{E_0}^*$. Such an $R$ is **convergent** and **equivalent** to $E_0$.

A critical pair of rules $l_1 \to r_1$ and $l_2 \to r_2$, with variables renamed apart, is $\langle l_1\sigma[r_2\sigma]_p,\ r_1\sigma \rangle$, where $p$ is a position of $l_1$ with $l_1|_p \notin V$ and $\sigma$ is a [most general unifier](/most-general-unifier/) of $l_1|_p$ and $l_2$. The position $p = \varepsilon$ is excluded when the two rules are the same rule.

## The algorithm

The procedure keeps a set $E$ of pending equations and a set $R$ of rules. Each iteration takes one equation, simplifies it with $R$, and either deletes it, turns it into a rule, or fails.

```pseudo id=main
COMPLETE(E, >, B)
L1  R ← ∅; steps ← 0; queue the equations of E
L2  loop
L3      if E is empty then E ← critical pairs ⟨u,v⟩ of R with u↓R ≠ v↓R; if E is empty then return SUCCESS(R)
L4      steps ← steps + 1; if steps > B then return GIVE-UP(R)
L5      remove a smallest equation s ≈ t from E; s ← s↓R; t ← t↓R        ▷ simplify
L6      if s = t then continue                                           ▷ delete
L7      if s > t then ρ ← s → t else if t > s then ρ ← t → s else return FAIL(s ≈ t)   ▷ orient
L8      for each g → d in R with g reducible by ρ: remove it, add g ≈ d to E   ▷ collapse
L9      for each g → d in R: d ← d↓ for (R \ {g→d}) ∪ {ρ}                       ▷ compose
L10     add ρ to R; add to E the critical pairs of ρ with every rule of R, ρ included  ▷ deduce
```

Line L5 picks the equation with the fewest symbols, with ties broken by arrival order; the implementation keeps $E$ in a [binary heap](/binary-heap/). Normal forms exist at line L5 because every rule satisfies $l > r$ and $>$ is well-founded, so $R$ terminates at all times.

Line L8 moves a rule back to $E$ when the new rule rewrites its left side. The rule is not lost: it returns as an equation and line L5 simplifies it with the new rules. Line L9 keeps the right sides in normal form, which keeps $R$ small and makes later normalizations shorter. Both lines are optional for correctness, but without them the rule set grows quickly: on the group axioms the run keeps many redundant rules.

Line L10 computes the critical pairs of $\rho$ with each rule, in both directions, and of $\rho$ with itself. Line L3 recomputes all critical pairs of the final $R$ before it reports success. Most of them are joinable by then, and the check makes the success case independent of what lines L8 and L9 removed or changed.

All functions work on terms of any depth with explicit stacks: normalization uses the innermost machine of [innermost reduction](/innermost-reduction/), unification uses a triangular substitution with an occurs check, and the [lexicographic path ordering](/lexicographic-path-ordering/) is compared with memoized frames on an explicit stack.

## Example

Let $E_0 = \{ f(f(x)) \approx g(x) \}$ with the lexicographic path ordering for the precedence $f > g$.

| iteration | equation after line L5 | action | rules after the iteration | new critical pairs |
|---|---|---|---|---|
| 1 | $f(f(x)) \approx g(x)$ | orient | $f(f(x)) \to g(x)$ | $f(g(x)) \approx g(f(x))$ |
| 2 | $f(g(x)) \approx g(f(x))$ | orient | $f(f(x)) \to g(x)$, $f(g(x)) \to g(f(x))$ | $f(g(f(x))) \approx g(g(x))$ |
| 3 | $g(g(x)) \approx g(g(x))$ | delete | unchanged | none |

In iteration 1, the rule overlaps itself: $f(x)$ at position $1$ of $f(f(x))$ unifies with a renamed copy $f(f(y))$ by $x \mapsto f(y)$. The term $f(f(f(y)))$ rewrites at position $1$ to $f(g(y))$ and at the root to $g(f(y))$, and both are normal forms, so the pair is new. In iteration 2, $f(g(x)) > g(f(x))$ because $f > g$ and $f(g(x)) > f(x)$, so line L7 orients the pair from left to right. Its overlap with the first rule, $f(f(g(y)))$, gives $f(g(f(y)))$ and $g(g(y))$. In iteration 3, line L5 rewrites $f(g(f(x))) \to g(f(f(x))) \to g(g(x))$, so both sides become $g(g(x))$ and line L6 deletes the equation.

Now $E$ is empty, and line L3 checks the two critical pairs of $R$, which are the two pairs above. Both are joinable, so the result is $\mathrm{SUCCESS}$ with $R = \{ f(f(x)) \to g(x),\ f(g(x)) \to g(f(x)) \}$. The rules move every $f$ to the right of every $g$ and replace $f f$ by $g$, so the normal forms are the terms $g^i(f^j(t))$ with $j \le 1$.

The order matters. With the precedence $g > f$ instead, line L7 orients the input as $g(x) \to f(f(x))$, which has no critical pairs, and completion succeeds at once with one rule.

**Groups.** With $E_0 = \{ e \cdot x \approx x,\ i(x) \cdot x \approx e,\ (x \cdot y) \cdot z \approx x \cdot (y \cdot z) \}$ and the lexicographic path ordering with $i > \cdot > e$, completion succeeds with the ten rules found by Knuth and Bendix:

$$\begin{aligned} e \cdot x &\to x & x \cdot e &\to x & i(x) \cdot x &\to e & x \cdot i(x) &\to e & (x \cdot y) \cdot z &\to x \cdot (y \cdot z) \\ i(e) &\to e & i(i(x)) &\to x & i(x) \cdot (x \cdot y) &\to y & x \cdot (i(x) \cdot y) &\to y & i(x \cdot y) &\to i(y) \cdot i(x) \end{aligned}$$

So an equation holds in all groups iff both sides have the same normal form under these rules. With the precedence $\cdot > i > e$ the run fails instead, on $i(x) \cdot i(y) \approx i(y \cdot x)$, which this order cannot orient in either direction.

## Correctness

Two invariants hold at the start of each iteration (see [the correctness proof](proofs/correctness.md)).

1. **Every rule goes down.** Each rule $g \to d$ of $R$ satisfies $g > d$. Line L7 creates only such rules, and line L9 replaces $d$ by a reduct $d'$ with $d >d'$ or $d = d'$, because each rewrite step goes down in a reduction order. So $R$ terminates at all times, and its rules never have a variable as left side or a new variable on the right.
2. **The theory does not change.** $\leftrightarrow_{E \cup R}^* = \leftrightarrow_{E_0}^*$. Simplifying an equation with $R$, deleting $s \approx s$, moving an equation between $E$ and $R$, and adding critical pairs, which are consequences of $R$, all keep the conversion.

On success $E$ is empty, so $\leftrightarrow_R^* = \leftrightarrow_{E_0}^*$, and line L3 has just checked that all critical pairs of $R$ are joinable. The [critical pair lemma](/critical-pair-lemma/) gives local confluence, and [Newman's lemma](/newman-lemma/) with termination gives confluence. On failure the returned equation is a consequence of $E_0$ with two distinct sides that $>$ does not compare. On give-up the rules are sound and terminating but may be incomplete.

**Runs that do not stop.** If the procedure is fair, which means every critical pair of rules that stay in $R$ from some point on is eventually processed, and if it never fails, then the set $R_\infty$ of such persistent rules is convergent and equivalent to $E_0$, even if it is infinite (Huet 1981). Then the procedure is a semi-decision procedure for $E_0$: two terms are equal iff they eventually have the same normal form under the current $R$.

## Complexity

**Per iteration.** Write $m$ for the largest size of a term that occurs, $r$ for the largest number of rules, and $N$ for the largest number of rewrite steps in one normalization. One normalization with the innermost machine costs $O(N r m^2)$: $O(m)$ tasks per step, $r$ rules tried per task, $O(m)$ per match. Line L5 does two normalizations, line L8 checks $r$ left sides against one rule, line L9 does $r$ normalizations, and line L10 tries $O(r m)$ unifications of cost $O(m^2)$ each. Line L3 is the most expensive: $R$ has $O(r^2 m)$ critical pairs, each normalized on both sides, which costs $O(N r^3 m^3)$.

**In total.** Each run of line L3 that does not return adds an equation, which a later iteration removes, so line L3 runs at most $k + 1$ times. The total time is $O(k N r^3 m^3)$ on the [word RAM](/word-ram/), plus the heap operations. The best case is $\Theta(n)$, for an input such as one equation $s \approx s$, which line L6 deletes after one normalization with the empty system.

**Space.** Line L10 adds $O(r m)$ equations per iteration and line L3 adds at most $O(r^2 m)$, each of size $O(m)$, so the queue takes $O((k + r) r m^2)$ space.

**No bound in the input size.** None of $k$, $N$, $r$ and $m$ is bounded by a function of $n$. The procedure may run forever (see below), and even on success the number of iterations and the size of $R$ can be very large, since the word problem of some finitely presented theories is undecidable and completion succeeds only on theories with a decidable one.

## Properties

- **Three outcomes.** Success gives a convergent equivalent system. Failure happens when an equation cannot be oriented; commutativity $x + y \approx y + x$ fails at once with every reduction order, since $x + y > y + x$ would give $y + x > x + y$ by the substitution that swaps $x$ and $y$. The procedure can also run forever: from $f(g(f(x))) \approx g(f(x))$ with $f > g$ it generates the rules $f(g^n(f(x))) \to g^n(f(x))$ for $n = 1, 2, 3, \ldots$, one new rule for each $n$, and the run never stops.
- **Depends on the order and on the choices.** Different reduction orders give different results, as the two group runs above show, and the choice of equation at line L5 can decide whether a run stops. There is no best choice in general.
- **Unique result.** For a fixed reduction order, a convergent system is reduced if every right side is in normal form and no left side is reducible by another rule. Two reduced convergent systems that are equivalent and both contained in the same reduction order are equal up to renaming of variables (Métivier 1983). Lines L8 and L9 make the success result reduced, so on success the run's choices do not matter for the final set of rules.
- **Not an algorithm for the word problem in general.** When it succeeds it decides the word problem of $E_0$, but it cannot succeed for theories whose word problem is undecidable, see the [undecidability of the word problem](/undecidability-of-word-problem/).

## Variants and improvements

- **Inference rules.** Bachmair, Dershowitz and Hsiang presented completion as six inference rules (deduce, orient, delete, simplify, compose, collapse) on pairs $(E, R)$. Any fair use of them is correct; the procedure above is one strategy. Correctness proofs use proof orderings: each rule replaces a proof by a smaller one.
- **Critical pair criteria.** Many critical pairs need not be computed: a pair whose overlapped term is reducible below the overlap position is redundant, and so are pairs that a connectedness argument covers. Such criteria save much of the work of line L3 and line L10, as in [Buchberger's algorithm](/buchberger-algorithm/) for [Gröbner bases](/groebner-basis/), which is completion for polynomial equations.
- **Unfailing completion.** [Unfailing completion](/unfailing-completion/) keeps an unorientable equation as an equation, and uses its instances that the order can orient. It never fails, and it is a complete semi-decision procedure for the equational theory. Equational theorem provers such as Waldmeister are built on it.
- **Completion modulo a theory.** Commutativity and associativity cannot be oriented, so completion [modulo equations](/rewriting-modulo-equations/) builds them into matching and unification, as in Peterson and Stickel's AC-completion. It needs [AC matching](/ac-matching/) and AC unification.
- **String rewriting.** For a [string rewriting system](/string-rewriting-system/), which presents a monoid, the same procedure works with overlaps of strings instead of unification. It is a standard tool for finitely presented monoids and groups.
- **Inductive theorems.** Completion can also prove equations that hold only for ground terms, in proof by consistency, a form of [inductive theorem proving](/inductive-theorem-proving/).
- **Narrowing.** For a convergent result, solving equations with variables uses [narrowing](/narrowing/), which applies the rules with unification instead of matching.

## When to use it

Use completion to turn an algebraic specification into a decision procedure: to decide equality in a theory, to check that a set of rules is confluent and repair it if it is not, or as the core of an equational theorem prover. Choose the order carefully, often by trying several precedences, and always use a step bound, since completion may run forever. For ground equations only, [congruence closure](/congruence-closure/) is simpler and always stops. When completion keeps failing on an equation such as commutativity, use unfailing completion or completion modulo that theory.

## Pitfalls

- **Forgetting the occurs check or the renaming.** Critical pairs need the two rules with disjoint variables, including the overlap of a rule with itself, and a unifier without the occurs check accepts $x = f(x)$ and produces false pairs.
- **Skipping overlaps at the root of two different rules, or including the trivial root overlap of a rule with itself.** The first misses pairs; the second gives the trivial pair $\langle r, r \rangle$ and only costs time.
- **Using an order that is not a reduction order.** If $>$ is not closed under contexts and substitutions, the rules need not terminate, and Newman's lemma does not apply. Comparing the number of symbols alone is not closed under substitutions: $f(x, a, a)$ has more symbols than $g(x, x)$, but under $x \mapsto h(h(a))$ the left instance has 6 symbols and the right one 7. Use a proper order such as LPO or KBO.
- **Unfair selection.** Picking the smallest equation is a good heuristic, but if new small equations keep arriving, an old equation may wait forever, and a non-stopping run then loses the completeness of Huet's theorem. Fair implementations mix in the oldest equation from time to time.
- **Reporting success without the final check.** If a rule removed by line L8 had its critical pairs computed earlier, a pair that the new $R$ cannot join may be lost; line L3 catches this case.
- **Deep terms.** Terms such as $g^{2000}(a)$ appear in practice. Recursive matching, unification or order comparison overflows the Python stack; the implementation uses explicit stacks throughout.

## Implementations

## History

Knuth and Bendix described the procedure in a paper published in 1970, in a volume on computational problems in abstract algebra. They introduced the critical pair test for confluence of terminating systems and the ordering now named after them, and their computer runs found complete systems for groups, central groupoids and other theories. Huet in 1981 gave the first complete proof of correctness, including the case of runs that do not stop, with the notion of fairness. Peterson and Stickel in 1981 extended completion to associative and commutative operators. Hsiang and Rusinowitch, and Bachmair, Dershowitz and Plaisted, developed unfailing completion in the late 1980s. Bachmair and Dershowitz then recast completion as an inference system with proof orderings, which is the standard presentation today.

## References
