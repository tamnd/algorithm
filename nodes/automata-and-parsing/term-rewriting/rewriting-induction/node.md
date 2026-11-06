---
tag: 35E48J
kind: algorithm
slug: rewriting-induction
name: Rewriting induction
aliases:
- Reddy's rewriting induction
area: automata-and-parsing/term-rewriting
level: research
summary: A proof method for inductive theorems over terminating rewrite systems.
solves: [inductive-theorem-proving]
model: word-ram
complexity:
  vars: {k: the number of steps, h: the largest number of rules and hypotheses, m: the largest size of a term that occurs, N: the largest number of rewrite steps in one normalization}
  time: {worst: O(k h m^2 (N + m))}
  space: {extra: O(k h m)}
properties: {deterministic: true, recursive: true, online: false}
prereqs: [inductive-theorem-proving, narrowing, lexicographic-path-ordering]
see_also: [structural-induction, term-algebra, knuth-bendix-completion, unfailing-completion, most-general-unifier, termination, orthogonal-rewrite-system]
sources:
  - paper: doi:10.1007/3-540-52885-7_86
    title: Uday S. Reddy, Term rewriting induction, 10th International Conference on Automated Deduction (CADE-10), Lecture Notes in Computer Science 449, Springer (1990)
    locator: pp. 162 to 177 (the expand, simplify and delete rules, and soundness by induction on the rewrite relation)
  - paper: doi:10.1007/11805618_18
    title: Takahito Aoto, Dealing with non-orientable equations in rewriting induction, Term Rewriting and Applications (RTA 2006), Lecture Notes in Computer Science 4098, Springer
    locator: pp. 242 to 256 (the inference system, its soundness, and ordered rewriting for unorientable equations)
  - paper: doi:10.4230/LIPIcs.FSCD.2016.33
    title: Takahito Aoto and Yoshihito Toyama, Ground confluence prover based on rewriting induction, 1st International Conference on Formal Structures for Computation and Deduction (FSCD 2016), LIPIcs 52
    locator: article 33
---

**Rewriting induction** proves that an equation holds for all ground values of its variables, given a terminating rewrite system that defines the functions involved. It orients the conjecture into a rule, splits it into cases by the rules that can apply to it, and then uses the conjecture itself, as a rule, to simplify the cases. That last move is the induction hypothesis, and the rewrite order is the induction order, so no induction variable or induction scheme is chosen by hand. Reddy introduced the method in 1990.

## In plain words

Suppose we have defined addition by two rules: zero plus anything is that thing, and one more than a number plus another is one more than their sum. We want to show that a number plus zero is the number, for every number.

The method looks at the left side and asks how it can be computed. A rule needs to know whether the first argument is zero or one more than something, so the proof splits into these two cases, just as a proof by induction would. In each case it applies the rule once. Then it may use the claim itself to simplify, but only on smaller instances, which the rewrite order guarantees. If every case ends with two equal sides, the claim holds for every number. If a case ends with two different numbers, the claim is false.

## The problem

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, positions as sequences of integers, $t|_p$ and $t[u]_p$, substitutions $\sigma$ applied on the right, rules $l \to r$, and $\to^*$ for the reflexive transitive closure. An equation is written $s \doteq t$, and $s \leftrightarrow^*_R t$ is equality modulo $R$.

**Constructor systems.** $\Sigma$ is split into constructors, such as $0$ and $s$ for the naturals, and defined symbols. A rewrite system $R$ is a constructor system if the left side of each rule is $f(c_1, \ldots, c_n)$ with $f$ defined and $c_i$ terms of constructors and variables. A **basic** term has this shape. $R$ is **sufficiently complete** if every ground basic term $f(c_1, \ldots, c_n)$ with ground constructor terms $c_i$ is reducible; then every ground term reduces to a ground constructor term.

**Input.** A constructor system $R$, sufficiently complete, a precedence for the [lexicographic path ordering](/lexicographic-path-ordering/) $>$ such that $l > r$ for every rule, a finite set $E_0$ of conjectures, and a step bound $B$.

**Question.** Is every $s \doteq t$ in $E_0$ an **inductive theorem** of $R$, that is, does $s\sigma \leftrightarrow^*_R t\sigma$ hold for every ground substitution $\sigma$? This is the problem of [inductive theorem proving](/inductive-theorem-proving/), which is undecidable, so the answer is "proved", "disproved" or "unknown".

## The algorithm

The state is a set $E$ of equations still to prove and a set $H$ of hypotheses, rules oriented by $>$. Expanding $s$ at a basic subterm $u = s|_p$ is a [narrowing](/narrowing/) step with each rule: for each rule $l \to r$ of $R$, renamed apart, with a [most general unifier](/most-general-unifier/) $\tau$ of $u$ and $l$, it produces $s[r]_p\tau \doteq t\tau$.

```pseudo id=main
REWRITING-INDUCTION(R, E₀, >, B)
L1  E ← E₀; H ← ∅; steps ← 0
L2  while E is not empty do
L3      if steps = B then return UNKNOWN
L4      remove the first equation s ≐ t from E; steps ← steps + 1
L5      s ← s↓R∪H; t ← t↓R∪H                                   ▷ simplify
L6      if s = t then continue                                    ▷ delete
L7      if s and t contain no defined symbol then return DISPROVED if a ground instance has sₚ ≠ tₚ, else UNKNOWN
L8      if t > s then swap s and t
L9      if s ≯ t or s has no basic subterm then return UNKNOWN
L10     u ← the first basic subterm of s, at position p; add s → t to H
L11     for each l → r in R with mgu τ of u and l: append s[r]ₚτ ≐ tτ to E      ▷ expand
L12 return PROVED
```

Line L5 rewrites with $R$ and the hypotheses until no rule applies; it stops because every rule of $R \cup H$ decreases in $>$. Line L7 handles equations between constructor terms, which no rule can simplify further: if some ground instance of the two sides differs, the equation is false, and line L7 searches ground constructor terms of at most four symbols for the variables. Line L9 fails when the conjecture cannot be oriented, as for commutativity, or when its larger side is a constructor term. Lines L10 and L11 are Reddy's expansion: the cases of line L11 cover every ground instance of $u$, because $R$ is sufficiently complete.

## Example

**$x + 0 \doteq x$.** Take $0 + y \to y$ and $s(x) + y \to s(x + y)$, with $+ > s > 0$.

| step | equation | action |
| --- | --- | --- |
| 1 | $x + 0 \doteq x$ | $x + 0 > x$; add $x + 0 \to x$ to $H$; expand at $x + 0$ |
| 2 | $0 \doteq 0$ | from $0 + y \to y$ with $\tau = \{x \mapsto 0, y \mapsto 0\}$; delete |
| 3 | $s(x' + 0) \doteq s(x')$ | from $s(x') + y \to s(x' + y)$ with $\tau = \{x \mapsto s(x'), y \mapsto 0\}$; the hypothesis gives $s(x') \doteq s(x')$; delete |

$E$ is empty, so $x + 0 = x$ for every natural number $x$. Step 3 used the conjecture on $x' + 0$, which is smaller than $s(x') + 0$ in the order: this is the induction step. Associativity $(x + y) + z \doteq x + (y + z)$ is proved the same way in three steps, by expanding at $x + y$.

**A conjecture that needs a lemma.** Add $d(0) \to 0$ and $d(s(x)) \to s(s(d(x)))$ with $d > +$. For $d(x) \doteq x + x$ alone, the run adds the hypotheses $s^n(x' + s^n(x')) \to s^{2n}(x' + x')$ for $n = 1, 2, 3, \ldots$, one after another, and stops at the step bound, here 50. With the lemma $x + s(y) \doteq s(x + y)$ as a second conjecture, both are proved in 6 steps.

**Unknown and disproved.** For $x + y \doteq y + x$ the two sides are incomparable in the path order, so line L9 returns "unknown" at step 1. For $x + y \doteq x$, the expansion case $x \mapsto 0$ gives $y \doteq 0$. Both sides are constructor terms, and the instance $y \mapsto s(0)$ gives $s(0) \doteq 0$, so the conjecture is disproved after 2 steps.

## Correctness

The full proof is below. It assumes that $R$ is sufficiently complete and $R \subseteq {>}$; disproof also assumes that $R$ is ground confluent, which holds for orthogonal constructor systems.

1. **Every hypothesis is an inductive theorem.** Let $l \to r$ be in the final $H$ and $\sigma$ ground; we use induction on $l\sigma$ in the well-founded order $>$. If $\sigma$ maps a variable to a term with a defined symbol, replace it by its constructor normal form, which gives a smaller left side. Otherwise the basic subterm $u\sigma$ is reducible at its root, so $l\sigma \to_R w$ where $w \doteq r\sigma$ is an instance of an equation added at line L11. Every later step on that equation, followed on the instance, uses $R$, deletes, or uses a hypothesis on a term smaller than $l\sigma$, which is valid by induction; a hypothesis made from it has a smaller left side as well. So $w \leftrightarrow^*_R r\sigma$ and $l\sigma \leftrightarrow^*_R r\sigma$.
2. **Proved.** If line L12 returns, each conjecture was deleted after steps with $R$ and $H$, or became a hypothesis; by part 1 every ground instance holds.
3. **Disproved.** If all conjectures were inductive theorems, then all hypotheses and all equations derived from them would be too. A ground equation between two different constructor terms is not, since they are different normal forms of a ground confluent system. So some conjecture is false.

## Complexity

The run need not stop, and inductive theorem proving is undecidable, so there is no bound in terms of the input. Let $k$ be the number of steps, $h$ the largest size of $R \cup H$, $m$ the largest term size and $N$ the largest number of rewrite steps in one normalization.

- **Simplify.** Each rewrite step tries $O(m)$ positions and $h$ rules with an $O(m)$ match, so a normalization costs $O(N h m^2)$.
- **Orient.** One path order comparison costs $O(m^3)$ with memoization.
- **Expand.** Each of the at most $h$ rules is unified with $u$ in $O(m^3)$.
- **Total.** $O(k h m^2 (N + m))$ time. The queue grows by at most $|R|$ equations per step, each of size $O(m)$, so the space is $O(k h m)$. The search at line L7 tries $g^v$ substitutions, where $v$ is the number of variables and $g$ the number of ground constructor terms with at most four symbols; it runs at most once.

## Properties

- **Sound.** "Proved" and "disproved" are correct under the assumptions above; "unknown" carries no information.
- **No induction scheme.** The cases come from the rules of $R$ by narrowing, and the induction order is the rewrite order, so mutual recursion and nested recursion need no special treatment.
- **Hypotheses are reused.** A hypothesis from one conjecture can simplify the cases of another, which is why a lemma given next to the goal helps, in either order.
- **Refutation.** Under ground confluence, the method also finds false conjectures, by reaching a case with different constructor terms.

## Variants and improvements

- **Non-orientable equations.** Aoto (2006) extends the method with ordered rewriting, as in [unfailing completion](/unfailing-completion/), so that conjectures such as commutativity can be kept as equations and used when an instance is oriented.
- **Decomposition.** An equation $c(s_1, \ldots, s_n) \doteq c(t_1, \ldots, t_n)$ with a constructor $c$ can be replaced by $s_i \doteq t_i$ for each $i$, since constructors are free; line L7 then applies earlier.
- **Lemma generation.** Practical systems generalize a diverging sequence of equations, such as the $s^n(\ldots)$ family above, into a lemma and add it as a conjecture.
- **Ground confluence.** Aoto and Toyama (2016) use rewriting induction to prove ground confluence of rewrite systems.

## When to use it

Use rewriting induction to prove properties of functions defined by terminating, pattern-matching rules, as in functional programs and algebraic specifications, when the conjecture can be oriented by a path order. It needs no induction variable and finds the case split from the rules. For properties that need a lemma, supply the lemma as an extra conjecture or use a prover that generalizes. For commutative operators, use the variant with ordered rewriting.

## Pitfalls

- **Sufficient completeness is needed.** If some ground basic term is irreducible, the expansion at line L11 misses cases, and "proved" can be wrong. A partial function, such as a predecessor with no rule for $0$, breaks the method unless the missing cases are added.
- **Orientation fixes the hypothesis.** $s \to t$ is used only from left to right, and only because $s > t$. A rule that the order does not contain could make $R \cup H$ loop, and then the induction is unsound.
- **Disproof needs confluence.** If two different constructor terms are equal modulo $R$, a case with different constructor terms is not a counterexample.
- **The choice of basic subterm matters.** This implementation expands at the first basic subterm in preorder. Another choice gives other cases, and can change whether the run succeeds.

## Implementations

## History

Reddy introduced term rewriting induction in 1990, as a reformulation of proof by consistency in which the rewrite relation itself is the induction order. Aoto (2006) extended it to non-orientable equations, and Aoto and Toyama (2016) used it to build a prover for ground confluence.

## References
