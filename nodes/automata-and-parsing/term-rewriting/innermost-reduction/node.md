---
tag: KTF62M
kind: algorithm
slug: innermost-reduction
name: Innermost reduction
aliases:
- innermost rewriting
- eager reduction
area: automata-and-parsing/term-rewriting
level: core
summary: Always contracts an innermost redex, one with no redex in its arguments.
solves: [normal-form-computation]
model: word-ram
complexity:
  vars: {n: the size of the input term, k: the number of rewrite steps, m: the largest size of a rule side, r: the number of rules}
  time: {worst: O((n + k m) r m), best: Θ(n)}
  space: {extra: O(n + k m)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1977
  people: [Michael J. O'Donnell]
  note: Innermost order is the call-by-value order of LISP (McCarthy 1960); O'Donnell compared innermost and outermost strategies for term rewriting in 1977.
prereqs: [rewrite-step, reduction-strategy, normal-form, term-matching]
see_also: [outermost-reduction, normal-form-computation, termination, beta-reduction, graph-reduction, hash-consing, orthogonal-rewrite-system, dependency-pairs]
sources:
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 9, Strategies (innermost and outermost strategies, and their normalization properties); Chapter 4, Orthogonality
  - paper: doi:10.1007/3-540-08531-9
    title: Michael J. O'Donnell, Computing in Systems Described by Equations, Lecture Notes in Computer Science 58, Springer, 1977
    locator: Chapter V, Termination (pp. 40 to 53); Chapter VI, Costs of reduction sequences (pp. 54 to 65)
  - paper: doi:10.3233/fi-1995-24121
    title: Bernhard Gramlich, Abstract relations between restricted termination and confluence properties of rewrite systems, Fundamenta Informaticae 24 (1995)
    locator: pp. 3 to 23 (innermost termination and its relation to termination for non-overlapping systems)
  - paper: doi:10.1016/0304-3975(75)90017-1
    title: Gordon D. Plotkin, Call-by-name, call-by-value and the lambda-calculus, Theoretical Computer Science 1(2) (1975)
    locator: pp. 125 to 159 (call-by-value evaluation)
  - paper: doi:10.1145/367177.367199
    title: John McCarthy, Recursive functions of symbolic expressions and their computation by machine, Part I, Communications of the ACM 3(4) (1960)
    locator: pp. 184 to 195 (the evaluation of arguments before the function is applied)
---

**Innermost reduction** computes a [normal form](/normal-form/) of a term by always contracting an innermost redex, a redex whose arguments contain no redex. The leftmost-innermost variant takes the leftmost such redex, and in effect evaluates the arguments of each function from left to right, completely, before it tries a rule at the function itself. This is call-by-value, the evaluation order of most programming languages. It is simple and fast, and it never rewrites the same argument twice, but it is not normalizing: it can loop on an argument that a rule would throw away.

## In plain words

To evaluate an expression, first evaluate its parts, then combine them. For `mul(2, 1)`, first make sure `2` and `1` are as simple as they can be, then apply the rule for `mul`. The rule produces a new expression; evaluate it in the same way. Stop when no rule applies anywhere.

This is how a calculator or a typical programming language works: it computes the inputs of a function before calling it. Each input is computed once, even when the function uses it many times. The cost is that an input is computed even when the function does not need it, and if that input never finishes, the whole computation never finishes, although a different order would have ended.

## The problem

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, positions as sequences of positive integers with root $\varepsilon$, subterm $t|_p$ and replacement $t[s]_p$, substitutions $\sigma$ applied as $t\sigma$, rules $l \to r$ with $l \notin V$ and $\mathrm{Var}(r) \subseteq \mathrm{Var}(l)$, and $\to_R^*$ the reflexive transitive closure of the rewrite relation of a [term rewriting system](/term-rewriting-system/) $R$.

The input is a finite list of rules $R$ and a term $t$, and optionally a step bound $B$. The output is a normal form $v$ with $t \to_R^* v$, as in the [normal form computation](/normal-form-computation/) problem, or a report that $B$ steps did not reach one.

A position $p$ of $t$ is a **redex** if $t|_p = l\tau$ for some rule $l \to r$ and some $\tau$; it is **innermost** if no position strictly below $p$ is a redex. The **leftmost-innermost** [strategy](/reduction-strategy/) contracts the leftmost innermost redex. When several rules match there, we use the first in the list.

## The algorithm

The algorithm walks the term with two explicit stacks: a stack of tasks and a stack of computed normal forms. $\mathrm{EVAL}(u, \sigma, p)$ means "push the normal form of $u\sigma$", where the values of $\sigma$ are already normal forms; $\mathrm{BUILD}(f, n, p)$ means "combine the top $n$ values under $f$ and try the rules at the root". The position $p$ is used only to report the steps.

```pseudo id=main
INNERMOST(t, R, B)                         ▷ B is a step bound, or ∞
L1  steps ← 0; tasks ← [EVAL(t, ∅, ε)]; vals ← []
L2  while tasks is not empty do
L3      pop a task
L4      if task = EVAL(x, σ, p) with x a variable then push xσ on vals
L5      else if task = EVAL(f(u1, …, un), σ, p) then push BUILD(f, n, p), EVAL(un, σ, p n), …, EVAL(u1, σ, p 1)
L6      else (task = BUILD(f, n, p)): pop v1, …, vn from vals; s ← f(v1, …, vn)
L7          find the first rule l → r in R and τ with lτ = s
L8          if there is none then push s on vals            ▷ s is a normal form
L9          else if steps = B then return ⊥                ▷ bound reached
L10         else steps ← steps + 1; push EVAL(r, τ, p)     ▷ the step s → rτ at p
L11 return (pop vals, steps)
```

Line L5 pushes the arguments so that $u_1$ is on top, which makes the evaluation go from left to right. When line L6 runs, all arguments of $s$ are normal forms, so the root is the only possible redex of $s$, and it is innermost. After a step, line L10 evaluates the right side $r$ under $\tau$ without copying the values of $\tau$: those are subterms of the arguments of $s$, hence already normal forms, and line L4 pushes them as they are.

Line L7 is [term matching](/term-matching/): walk $l$ and $s$ together, bind each variable at its first occurrence, and at a later occurrence of the same variable (a non-linear rule) compare the two subterms. The implementation does this with an explicit stack and compares terms without recursion, so a term of depth $10^5$ is fine.

## Example

Peano arithmetic with the rules, numbered 0 to 3,

$$\mathit{add}(0, y) \to y, \quad \mathit{add}(s(x), y) \to s(\mathit{add}(x, y)), \quad \mathit{mul}(0, y) \to 0, \quad \mathit{mul}(s(x), y) \to \mathit{add}(\mathit{mul}(x, y), y),$$

and $t = \mathit{mul}(2, 1)$, where $k$ stands for $s^k(0)$. The arguments $2$ and $1$ are normal forms, so the first redex is the root.

| step | position | rule | term after the step |
|---|---|---|---|
| 1 | $\varepsilon$ | 3 | $\mathit{add}(\mathit{mul}(1, 1), 1)$ |
| 2 | $1$ | 3 | $\mathit{add}(\mathit{add}(\mathit{mul}(0, 1), 1), 1)$ |
| 3 | $1\,1$ | 2 | $\mathit{add}(\mathit{add}(0, 1), 1)$ |
| 4 | $1$ | 0 | $\mathit{add}(1, 1)$ |
| 5 | $\varepsilon$ | 1 | $s(\mathit{add}(0, 1))$ |
| 6 | $1$ | 0 | $s(s(0)) = 2$ |

In step 2 the machine is evaluating the right side $\mathit{add}(\mathit{mul}(x, y), y)$ of step 1 with $\tau = \{x \mapsto 1, y \mapsto 1\}$: line L5 reaches $\mathit{mul}(x, y)$ first, line L6 builds $\mathit{mul}(1, 1)$, and rule 3 fires at position $1$. The outer $\mathit{add}$ waits on the task stack until its first argument is a normal form, which happens after step 4. The test file checks this trace step by step.

## Correctness

The machine makes exactly the leftmost-innermost steps, in order, and returns the normal form at the end of that sequence when it is finite. Two facts give this.

1. **Decomposition.** In $f(w_1, \ldots, w_n)$, if $w_i$ is the first argument that is not a normal form, the leftmost innermost redex lies in $w_i$, and it is the leftmost innermost redex of $w_i$. Only when all arguments are normal forms can the root be contracted. So the leftmost-innermost reduction of $f(w_1, \ldots, w_n)$ is that of $w_1$, then of $w_2$, and so on, then a root step and the reduction of its result. The machine follows the same order with lines L5 and L6.
2. **Substituted values are normal.** If all arguments of $s$ are normal forms and $l\tau = s$, then each $x\tau$ is a subterm of an argument, since $l$ is not a variable, so it is a normal form. That is why line L4 may push $x\tau$ without evaluating it again.

An induction on the number of steps, and inside it on the size of the term, turns these into the theorem; see [the correctness proof](proofs/correctness.md). The result is a normal form of $t$, and $t \to_R^* v$, because each step is an $R$-step. If the system is [confluent](/confluence/), it is the unique normal form of $t$.

## Complexity

**Counting work.** Each $\mathrm{EVAL}$ task of a non-variable term creates one $\mathrm{BUILD}$ task. The input term contributes $n$ tasks, and each step contributes at most $m$ more, one for each symbol of the right side; the values of $\tau$ are reused, not walked. So there are $O(n + k m)$ tasks. Each $\mathrm{BUILD}$ tries at most $r$ rules, and matching a left-linear left side costs $O(m)$, since the walk stops at the variables of $l$. In total, for left-linear rules, the time is $O((n + k m)\, r\, m)$ on the [word RAM](/word-ram/), and $\Theta(n)$ for fixed $R$ when $t$ is already a normal form whose root symbols match no rule.

**Non-linear rules.** A repeated variable needs a comparison of two subterms, which costs up to their size. With [hash-consing](/hash-consing/) every term has a unique node, and the comparison is $O(1)$.

**Space.** The two stacks and the new nodes take $O(n + k m)$ space. The result is stored with sharing: in $d(x) \to p(x, x)$, both arguments of $p$ point to the same node. Written out as a tree, the normal form can be exponentially larger than this: $k$ steps of $d$ applied to nested arguments give a tree of size $2^k$.

**Number of steps.** $k$ is not bounded by any function of $n$ in general, since rewriting is [Turing-complete](/turing-completeness/). For a terminating system, innermost runtime complexity, the largest $k$ as a function of $n$ over terms whose arguments are normal forms, is the cost measure that automatic tools for program complexity analyze.

## Properties

- **Not normalizing.** With $f(x) \to a$ and $b \to b$, the term $f(b)$ has the normal form $a$, by a root step. Innermost reduction contracts $b$ forever, because the root is not innermost while $b$ is a redex. So innermost reduction can fail on terms that have a normal form, unlike [outermost reduction](/outermost-reduction/) on suitable systems.
- **All innermost reductions have the same length on non-overlapping systems.** If no two left sides overlap (no [critical pairs](/critical-pair/) at all), two distinct innermost redexes of a term are at disjoint positions, and contracting one leaves the other an innermost redex. So any two innermost steps from $t$ can be completed by one step each to a common term, and by the usual tiling argument, if one innermost reduction from $t$ ends in a normal form after $k$ steps, then every maximal innermost reduction from $t$ ends there after exactly $k$ steps. The choice "leftmost" then does not matter.
- **Innermost termination.** A system is innermost terminating if every innermost reduction is finite. This is weaker than [termination](/termination/): $\{f(a) \to f(a),\ a \to b\}$ is not terminating, but it is innermost terminating, because the root of $f(a)$ is never innermost while the redex $a$ sits below it, and $f(b)$ is a normal form. The two left sides overlap here. For non-overlapping systems, Gramlich showed that innermost termination implies termination, so termination tools such as [dependency pairs](/dependency-pairs/) may prove the easier innermost property.
- **Sharing of arguments.** Every argument is evaluated at most once before a rule uses it, however many times the right side copies it. Outermost reduction without sharing may evaluate a copied argument many times.

## Variants and improvements

- **Rightmost-innermost and parallel-innermost.** Contract the rightmost innermost redex, or all innermost redexes at once. For non-overlapping systems these give the same normal form with the same number of steps (counting a parallel step as the number of redexes it contracts).
- **Call-by-value in the lambda calculus.** [Beta-reduction](/beta-reduction/) that contracts a redex only when its argument is a value is Plotkin's call-by-value calculus. It does not reduce under $\lambda$, so it computes weak normal forms rather than normal forms.
- **Memoization and sharing.** With [hash-consing](/hash-consing/) and a table from each term already normalized to its normal form, a confluent terminating system can skip repeated work: each distinct subterm is normalized once.
- **Compiling the rules.** Instead of trying the rules one by one at line L7, compile all left sides into one automaton that finds the matching rule in one pass over $s$, as in [Hoffmann and O'Donnell's bottom-up matching](/hoffmann-odonnell-matching/) or a [discrimination tree](/discrimination-tree/).
- **Outermost and lazy strategies.** To be normalizing, use [outermost reduction](/outermost-reduction/), or lazy evaluation with sharing as in [graph reduction](/graph-reduction/).

## When to use it

Use innermost reduction for a terminating system, where every strategy reaches a normal form and the only question is cost: it is the cheapest to run, needs no extra bookkeeping, and never copies an unevaluated argument. Term rewriting tools and functional languages with strict semantics evaluate in this order. For a system that is not terminating, use it only when the rules are known to be innermost normalizing on the inputs of interest, or with a step bound; otherwise use a normalizing strategy such as outermost reduction.

## Pitfalls

- **Assuming that it finds a normal form whenever one exists.** It does not; see the example $f(b)$ above. Use a step bound when the system is not known to terminate.
- **Evaluating a right side's variables again.** The values bound to variables are already normal forms. Pushing them as new $\mathrm{EVAL}$ tasks of their own terms is correct but costs time proportional to their size at each use.
- **Recursion on deep terms.** A natural recursive evaluator recurses once per level, and the term $s^{n}(0)$ has depth $n$. In Python this overflows at about a thousand levels. Use explicit stacks, and compare terms without recursion, as Python's own tuple equality also recurses.
- **Positions as copied tuples.** Building the position $p\,i$ as a new tuple at each level costs time proportional to the depth, which makes a deep term quadratic. The implementation keeps positions as linked pairs and expands them only when a trace is requested.
- **Different results on non-confluent systems.** With $a \to b$, $a \to c$, the choice of the first matching rule decides the normal form. The result is then one normal form of $t$, not the normal form.

## Implementations

## History

Evaluating the arguments of a function before applying it is the call-by-value order of LISP, which McCarthy described in 1960, and of most later programming languages. Plotkin in 1975 gave call-by-value its own lambda calculus and compared it with call-by-name. For term rewriting systems, O'Donnell's 1977 monograph studied when innermost and outermost strategies terminate and what they cost. Gramlich in 1995 related innermost termination to termination, which made innermost termination a target of automated termination proofs.

## References
