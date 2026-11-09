---
tag: JGY442
kind: algorithm
slug: robinson-unification
name: Robinson's unification algorithm
aliases:
- Robinson unification
- unification algorithm of 1965
area: logic-and-constraints/unification-and-resolution
level: core
summary: Original unification algorithm; exponential time in the worst case without term sharing.
solves: [unification-problem]
model: word-ram
complexity:
  vars: {n: the number of variables, N: the total size of the two input terms}
  time: {worst: 2^Θ(N), bindings: O(n)}
  space: {extra: 2^Θ(N)}
properties: {deterministic: true, exact: true, online: false, recursive: false, in_place: false}
history:
  year: 1965
  people: [John Alan Robinson]
  note: Robinson gave the algorithm and the unification theorem in his 1965 paper on the resolution principle.
prereqs: [unifier, most-general-unifier, substitution, occurs-check]
see_also: [mgu-existence-theorem, martelli-montanari-unification, paterson-wegman-unification, idempotent-substitution, term-dag, robinson-resolution, unification-problem]
sources:
  - paper: doi:10.1145/321250.321253
    title: J. A. Robinson, A machine-oriented logic based on the resolution principle, Journal of the ACM 12(1), 1965, pages 23 to 41
    locator: the definition of the disagreement set, the unification algorithm and the unification theorem
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Section 4.5, Syntactic unification, Section 4.7, Unification and term rewriting in ML, and Section 4.8, Unification of term graphs (the exponential example and its cure by sharing)
  - paper: "Kevin Knight, Unification: a multidisciplinary survey, ACM Computing Surveys 21(1), 1989, doi:10.1145/62029.62030"
    locator: the sections on Robinson's algorithm, its exponential worst case and the faster algorithms that followed
  - book: isbn:9780444508133
    title: Franz Baader and Wayne Snyder, Unification Theory, in J. A. Robinson and A. Voronkov (editors), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Volume I, Chapter 8, Section 2 (syntactic unification algorithms and their complexity)
---

Robinson's unification algorithm decides whether two first-order [terms](/term/) $s$ and $t$ have a [unifier](/unifier/), and returns an [idempotent](/idempotent-substitution/) [most general unifier](/most-general-unifier/) if they do. It finds the first place where the two terms differ, binds a variable there, applies the binding, and repeats. J. A. Robinson gave it in 1965 with the resolution principle, and its correctness proves the [unification theorem](/mgu-existence-theorem/). It makes at most one binding per variable, but on terms stored as trees the terms can grow to exponential size. The [Martelli-Montanari](/martelli-montanari-unification/) and [Paterson-Wegman](/paterson-wegman-unification/) algorithms remove this cost with shared terms.

## In plain words

Write the two patterns one above the other and read them from left to right. At the first place where they differ, look at the two parts. If both start with different fixed symbols, the patterns can never match, so stop. If one part is a blank, fill that blank with the other part everywhere, in both patterns. But if the other part contains that same blank, stop: the filling would grow forever. Then read again from the left.

Each filling removes one blank for good, so the process ends. When the two patterns read the same, the list of fillings is the answer. It is the most general answer: it fills only what the patterns force.

## The problem

The input is two first-order terms $s$ and $t$ over a signature $\Sigma$ and a set of variables $V$. Notation: $n = |\mathrm{Var}(s) \cup \mathrm{Var}(t)|$, $N = |s| + |t|$, $\sigma, \theta$ are substitutions, $t\sigma$ is the application of $\sigma$ to $t$, and $\sigma\theta$ means "first $\sigma$, then $\theta$". The output is a most general unifier of $s$ and $t$, or FAIL when no unifier exists. This is the [unification problem](/unification-problem/) for one equation. A set of equations reduces to one equation by pairing the sides under a new symbol.

## The algorithm

The **first disagreement pair** of two different terms is found by reading them together in preorder. It is the pair of subterms $(u, v)$ at the first position where the two terms differ in a variable, in a root symbol or in an arity.

```pseudo id=main
ROBINSON(s, t)                          ▷ an idempotent mgu of s and t, or FAIL
L1  σ ← ε                               ▷ the identity substitution
L2  while sσ ≠ tσ do
L3      (u, v) ← the first disagreement pair of sσ and tσ
L4      if neither u nor v is a variable then return FAIL       ▷ clash
L5      x ← the variable of the pair (u if u is one), r ← the other term
L6      if x occurs in r then return FAIL                       ▷ occurs check
L7      σ ← σ{x ↦ r}                    ▷ compose, and apply {x ↦ r} to sσ and tσ
L8  return σ
```

Line L7 composes: each binding $y \mapsto w$ of $\sigma$ becomes $y \mapsto w\{x \mapsto r\}$, and the binding $x \mapsto r$ is added. This keeps $\sigma$ idempotent. The implementation keeps the current terms $s\sigma$ and $t\sigma$ and applies the new binding to them.

## Example

Unify $s = f(x_1, h(x_1), x_2)$ and $t = f(g(x_3), x_4, x_3)$.

| step | $s\sigma$ | $t\sigma$ | pair | binding |
|---|---|---|---|---|
| 1 | $f(x_1, h(x_1), x_2)$ | $f(g(x_3), x_4, x_3)$ | $(x_1, g(x_3))$ | $x_1 \mapsto g(x_3)$ |
| 2 | $f(g(x_3), h(g(x_3)), x_2)$ | $f(g(x_3), x_4, x_3)$ | $(h(g(x_3)), x_4)$ | $x_4 \mapsto h(g(x_3))$ |
| 3 | $f(g(x_3), h(g(x_3)), x_2)$ | $f(g(x_3), h(g(x_3)), x_3)$ | $(x_2, x_3)$ | $x_2 \mapsto x_3$ |
| 4 | $f(g(x_3), h(g(x_3)), x_3)$ | $f(g(x_3), h(g(x_3)), x_3)$ | none | return |

The result is $\sigma = \{x_1 \mapsto g(x_3),\ x_4 \mapsto h(g(x_3)),\ x_2 \mapsto x_3\}$. In step 2 the variable is on the right side, so line L5 takes $x = x_4$.

**A failure.** For $f(x, y) \doteq f(g(y), g(x))$, step 1 binds $x \mapsto g(y)$, which gives $f(g(y), y)$ and $f(g(y), g(g(y)))$. Step 2 finds the pair $(y, g(g(y)))$, and line L6 returns FAIL.

**The exponential example.** Let

$$s = f(x_1, x_2, \ldots, x_n), \qquad t = f(g(x_0, x_0), g(x_1, x_1), \ldots, g(x_{n-1}, x_{n-1})).$$

Step $i$ binds $x_i$ to $g(x_{i-1}, x_{i-1})$ with $x_{i-1}$ already replaced, so $x_i\sigma$ is the complete binary tree of $g$ nodes of height $i$, with $2^{i+1} - 1$ symbols. The input has $N = 4n + 2$ symbols, but $|s\sigma| = 2^{n+2} - n - 3$ and the bindings of $\sigma$ have $2^{n+2} - n - 4$ symbols in total. The implementation below gave these sizes and times (Python, one run, seconds):

| $n$ | input size | $\lvert s\sigma \rvert$ | size of $\sigma$ | time |
|---|---|---|---|---|
| 5 | 22 | 120 | 119 | under 0.001 |
| 10 | 42 | 4083 | 4082 | 0.006 |
| 15 | 62 | 131054 | 131053 | 0.47 |
| 18 | 74 | 1048555 | 1048554 | 5.8 |
| 20 | 82 | 4194281 | 4194280 | 18.9 |

The time grows by a factor of about 4 when $n$ grows by 1, because each step rewrites terms that double in size. With shared subterms the same mgu is a DAG of $n + 1$ nodes.

## Correctness

The proof keeps three invariants. After $k$ bindings, (I1) $\sigma$ is idempotent and uses only input variables, (I2) each unifier $\theta$ of $s$ and $t$ satisfies $\theta = \sigma\theta$, and (I3) the current terms $s\sigma, t\sigma$ contain no variable of $\mathrm{dom}(\sigma)$, which has $k$ elements. A unifier of $s, t$ also unifies $s\sigma, t\sigma$, and so it unifies the disagreement pair. So FAIL at L4 (two different roots) and at L6 ($|r\theta| > |x\theta|$ for each $\theta$) is correct. At L7, each unifier $\theta$ has $x\theta = r\theta$, so $\{x \mapsto r\}\theta = \theta$, which keeps (I2). Each binding removes the variable $x$ from the current terms for good, so there are at most $n$ bindings. At L8, $\sigma$ unifies, and (I2) gives $\sigma \le \theta$ for every unifier $\theta$. The full proof is below.

## Complexity

- **Number of steps.** At most $n$ executions of line L7, and at most $n + 1$ passes of the loop.
- **Cost of a step on trees.** Finding the pair, the occurs check and applying the binding take time linear in the current sizes of $s\sigma$, $t\sigma$ and $\sigma$.
- **Worst case.** The sizes can grow to $2^{\Theta(N)}$, so the time and the space are $2^{\Theta(N)}$ in the worst case. The example above is a lower bound family with $N = 4n + 2$ and output size $2^{n+2} - n - 4$. The upper bound holds because the mgu, written as a DAG, has at most $N$ nodes and at most $N$ edges, and such a DAG unfolds to trees of size $2^{O(N)}$.
- **The cost is in the representation.** The number of bindings is small. All the cost comes from copying subterms. Any algorithm that outputs the mgu as explicit trees must pay the output size on the example, so linear algorithms output the mgu in a shared form.
- **With sharing.** If bindings are kept in triangular form and terms are shared, Robinson's method avoids the copying. Corbin and Bidoit (1983) showed a quadratic bound for such a version. The almost linear and linear algorithms go further: the union-find method, the [Martelli-Montanari algorithm](/martelli-montanari-unification/) and the [Paterson-Wegman algorithm](/paterson-wegman-unification/).

## Properties

- **Deterministic and exact.** It always returns an mgu or a correct FAIL.
- **Idempotent output.** The result satisfies $\mathrm{dom}(\sigma) \cap \mathrm{vran}(\sigma) = \emptyset$, and its variables are input variables. No fresh variable is created.
- **Order-dependent output.** Which variable of a pair $(x, y)$ is bound changes the output by a renaming only. Line L5 prefers the left side.
- **Sound only with the occurs check.** Without line L6 the algorithm can loop on cyclic terms or return a "unifier" of $x \doteq f(x)$. See [occurs check](/occurs-check/).

## Variants and improvements

- **Sets of terms.** Robinson stated the algorithm for a finite set of expressions, with the disagreement set of the whole set. Unifying $\{t_1, \ldots, t_k\}$ is the same as unifying $f(t_1, \ldots, t_{k-1}) \doteq f(t_2, \ldots, t_k)$.
- **Recursive form.** Most programs unify recursively: unify the arguments from left to right, and look variables up in the current bindings instead of applying them to the terms. This is Robinson's algorithm with lazy application of $\sigma$.
- **Triangular bindings.** Store $\sigma$ as the list of single bindings $\{x_1 \mapsto r_1\} \cdots \{x_k \mapsto r_k\}$ and never compose. The size of the output is then at most $N$, and the explicit form can be computed later if needed.
- **Without the occurs check.** Dropping line L6 gives unification over rational trees, which needs a guard against infinite loops on cyclic bindings.
- **Faster algorithms.** Huet's union-find algorithm (1976), the [Paterson-Wegman algorithm](/paterson-wegman-unification/) (1978) and the [Martelli-Montanari algorithm](/martelli-montanari-unification/) (1982) work on a [term DAG](/term-dag/) and run in almost linear or linear time.

## When to use it

Use it to learn unification, and to prove the [unification theorem](/mgu-existence-theorem/). In practice, the recursive version with lazy bindings is the common choice in Prolog systems and in theorem provers, because typical terms are small and the exponential case needs special input. If the input can be adversarial, or the terms are large and shared, use an algorithm on a term DAG, such as [Martelli-Montanari](/martelli-montanari-unification/) with union-find.

## Pitfalls

- **Forgetting to compose.** Adding $x \mapsto r$ to $\sigma$ without applying $\{x \mapsto r\}$ to the earlier bindings gives a substitution that is not idempotent and may not unify: after $x \mapsto f(y)$ and then $y \mapsto a$, the binding of $x$ must become $f(a)$.
- **Applying the binding to only one side.** Line L7 must update both $s\sigma$ and $t\sigma$.
- **Dropping the occurs check.** The result is unsound for theorem proving. See the refutation example on the [occurs check](/occurs-check/) page.
- **Deep recursion.** A recursive implementation can exceed the call stack on deep terms, such as long lists. The implementation below uses explicit stacks.
- **Rescanning from the root.** Recomputing the first disagreement pair from the root in each pass adds a factor; a real implementation resumes from the last position.

## Implementations

## History

J. A. Robinson introduced unification in "A machine-oriented logic based on the resolution principle", published in the Journal of the ACM in 1965. The paper defines the disagreement set, gives this algorithm, and proves that it returns a most general unifier of each unifiable finite set of expressions. The exponential behavior on trees led to the work on faster algorithms in the 1970s: Huet's thesis (1976) with almost linear union-find unification, Paterson and Wegman (1978) with linear time, and Martelli and Montanari (1982).

## References
