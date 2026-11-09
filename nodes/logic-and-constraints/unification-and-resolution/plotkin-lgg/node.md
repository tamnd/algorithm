---
tag: F51B82
kind: algorithm
slug: plotkin-lgg
name: Plotkin's least general generalization algorithm
aliases:
- lgg algorithm
- Reynolds anti-unification
area: logic-and-constraints/unification-and-resolution
level: advanced
summary: Computes the least general generalization of two terms by anti-unification.
solves: [anti-unification-problem]
model: word-ram
complexity:
  vars: {N: the total size of the two input terms}
  time: {expected: O(N), worst: O(N log N)}
  space: {extra: O(N)}
properties: {deterministic: true, exact: true, online: false, recursive: true, in_place: false}
history:
  year: 1970
  people: [Gordon Plotkin, John C. Reynolds]
  note: Plotkin and Reynolds found the least general generalization of terms independently, in two papers of Machine Intelligence 5.
prereqs: [term, substitution, anti-unification-problem]
see_also: [most-general-unifier, robinson-unification, hash-consing, term-dag, clause-subsumption, term-indexing, substitution-tree]
sources:
  - paper: "G. D. Plotkin, A note on inductive generalization, in B. Meltzer and D. Michie (editors), Machine Intelligence 5, Edinburgh University Press, 1970, pages 153 to 163"
    locator: the definition of the least general generalization, the algorithm for two terms, and the lgg of clauses
  - paper: "J. C. Reynolds, Transformational systems and the algebraic structure of atomic formulas, in B. Meltzer and D. Michie (editors), Machine Intelligence 5, Edinburgh University Press, 1970, pages 135 to 151"
    locator: the lattice of atomic formulas under instance order, in which the generalization is the meet and the unifier is the join
---

**Plotkin's algorithm** computes the least general generalization (lgg) of two first-order [terms](/term/) $s$ and $t$: the most specific term $g$ that has both $s$ and $t$ as instances. It walks the two terms together. Where they agree, it copies the common symbol. Where they disagree, it puts a new variable, and it puts the same variable every time the same pair of subterms disagrees. It is the dual of [unification](/robinson-unification/): unification finds the most general common instance, and this algorithm finds the most specific common pattern. It solves the [anti-unification problem](/anti-unification-problem/), and Plotkin and Reynolds found it independently in 1970.

## In plain words

You have two examples, and you want the pattern that fits both and says as much as possible. Lay the two examples side by side and read them together. Where they show the same symbol, copy that symbol into the pattern. Where they show different things, write a blank in the pattern.

There is one rule that makes the pattern as exact as possible. If the same two different things appear at several places, use the same blank at all of them. Then the pattern also records that these places are linked. A table of the pairs seen so far gives the blank for each pair.

## The problem

Notation: $N = |s| + |t|$ is the total number of symbol occurrences, and $\sigma, \theta, \eta, \lambda$ are substitutions. For terms, $h \le g$ means $g = h\lambda$ for some $\lambda$, so $h$ is at least as general as $g$.

**Input:** two terms $s$ and $t$.

**Output:** a term $g$ and substitutions $\theta_1, \theta_2$ with $g\theta_1 = s$ and $g\theta_2 = t$, such that every term $h$ with $h\eta_1 = s$ and $h\eta_2 = t$ satisfies $h \le g$.

The variables of $s$ and $t$ are treated like constants: the algorithm never binds them. A common variable $x$ at the same position stays $x$ in $g$.

## The algorithm

The algorithm keeps a table $M$ from pairs of subterms to new variables, and two substitutions $\theta_1, \theta_2$ that record what each new variable stands for.

```pseudo id=main
LGG(s, t)
L1  M ← empty table; θ₁ ← ∅; θ₂ ← ∅
L2  return (A(s, t), θ₁, θ₂)

A(a, b)                                        ▷ generalize the pair (a, b)
L3  if a and b have the same head f of arity k then
L4      return f(A(a₁, b₁), …, A(aₖ, bₖ))      ▷ a = f(a₁, …, aₖ), b = f(b₁, …, bₖ); k = 0 for a common constant or variable
L5  if (a, b) ∈ M then return M[(a, b)]
L6  z ← a new variable; M[(a, b)] ← z; θ₁[z] ← a; θ₂[z] ← b
L7  return z
```

The Python implementation numbers the subterms of $s$ and $t$ by [hash consing](/hash-consing/) first, so the key $(a, b)$ in L5 is a pair of integers, and it runs A with an explicit stack.

## Example

Let $s = f(g(a), a, h(a))$ and $t = f(g(b), b, h(c))$.

| pair | rule | result |
|---|---|---|
| $(s, t)$ | L3, head $f$ | $f(\cdot, \cdot, \cdot)$ |
| $(g(a), g(b))$ | L3, head $g$ | $g(\cdot)$ |
| $(a, b)$ | L6, new | $Z_0$ |
| $(a, b)$ | L5, found | $Z_0$ |
| $(h(a), h(c))$ | L3, head $h$ | $h(\cdot)$ |
| $(a, c)$ | L6, new | $Z_1$ |

The result is $g = f(g(Z_0), Z_0, h(Z_1))$ with $\theta_1 = \{Z_0 \mapsto a, Z_1 \mapsto a\}$ and $\theta_2 = \{Z_0 \mapsto b, Z_1 \mapsto c\}$. The term $f(g(Z_0), Z_1, h(Z_2))$ is also a generalization, but it is strictly more general: it does not say that the second argument is the argument of $g$. The pair $(a, c)$ is not the pair $(a, b)$, so $Z_1$ is a separate variable.

More results:

| $s$ | $t$ | lgg |
|---|---|---|
| $f(g(a), a, g(a))$ | $f(g(b), b, g(b))$ | $f(g(Z_0), Z_0, g(Z_0))$ |
| $f(a, b, a)$ | $f(b, a, b)$ | $f(Z_0, Z_1, Z_0)$ |
| $f(x, x)$ | $f(x, y)$ | $f(x, Z_0)$ |
| $f(a)$ | $g(a)$ | $Z_0$ |
| $s$ | $s$ | $s$ |

In the second row, the pairs $(a, b)$ and $(b, a)$ are different, so they get different variables.

## Correctness

Call $A(a, b)$ the value of the call on the pair $(a, b)$. Because of the table, $A$ is a function of the pair: the same disagreeing pair always gives the same variable.

- **Generalization.** By induction on the terms, $A(a, b)\theta_1 = a$ and $A(a, b)\theta_2 = b$. So $g\theta_1 = s$ and $g\theta_2 = t$.
- **Least general.** Let $h\eta_1 = s$ and $h\eta_2 = t$. Put $\lambda(y) = A(y\eta_1, y\eta_2)$ for each variable $y$ of $h$. By induction on $h$, $h\lambda = A(h\eta_1, h\eta_2) = g$: at a function symbol of $h$, both instances have that symbol, so L4 applies. So $h \le g$.
- **Uniqueness.** If $g$ and $g'$ are both least general, each is an instance of the other, so they have the same size and differ only by a renaming of variables.

The full proof is below. It also shows why the table is needed: without it, the result for $f(a, a)$ and $f(b, b)$ would be $f(Z_0, Z_1)$, which is more general than $f(Z_0, Z_0)$.

## Complexity

Hash consing numbers all subterms of $s$ and $t$ in $O(N)$ expected time. The run visits at most $\min(|s|, |t|)$ pairs, one for each common position where all the symbols above agree. Each pair costs $O(1)$ expected time for the table and $O(k)$ for its $k$ children. So the total time is $O(N)$ expected, and the space is $O(N)$. With balanced search trees in place of hash tables, the time is $O(N \log N)$ in the worst case.

If the table is keyed by the subterms themselves, each lookup compares terms, and the time can grow to $O(N^2)$.

## Properties

- The output $g$ is unique up to a renaming of its new variables.
- $|g| \le \min(|s|, |t|)$, so the output is never larger than the smaller input. Unification can produce exponentially large output on trees, and generalization cannot.
- The operation is commutative and associative up to renaming, so the lgg of $n$ terms can be computed pairwise, or in one pass with a table keyed by $n$-tuples.
- Terms modulo renaming, ordered by $\le$, with a top element added, form a lattice: the lgg is the meet, and the instance given by the [most general unifier](/most-general-unifier/) is the join. This is the structure that Reynolds described.

## Variants and improvements

- **Clauses.** Plotkin also defined the lgg of two clauses under subsumption: it pairs every literal of one clause with every compatible literal of the other and generalizes all pairs with one shared table. The result can have as many literals as the product of the sizes, and is usually reduced afterwards.
- **Relative lgg.** Plotkin's relative lgg generalizes with respect to background knowledge, and was used in inductive logic programming systems such as Golem.
- **Equational and higher-order anti-unification.** Modulo theories such as associativity and commutativity, or for lambda terms, the lgg may not be unique, and algorithms return a complete set of generalizations. See the [anti-unification problem](/anti-unification-problem/).
- **Term indexing.** [Substitution trees](/substitution-tree/) store a set of terms under common generalizations, computed in the same way. See [term indexing](/term-indexing/).

## When to use it

Use it to find the common pattern of examples: in inductive logic programming, in learning programs from examples, in finding repeated code (clone detection), in building index trees for theorem provers, and in computing invariants in program analysis. For first-order syntactic terms, this algorithm is the standard solution and is linear. Modulo equational theories or for higher-order terms, specialized algorithms are needed.

## Pitfalls

- **Forgetting the table.** Without the table, the result is a generalization but not the least general one.
- **Ordered pairs.** The pairs $(a, b)$ and $(b, a)$ are different keys. Merging them gives a wrong result.
- **Clashing names.** The new variables must not occur in $s$ or $t$. Otherwise $\theta_1$ binds a variable of the input.
- **Input variables.** The variables of the inputs are constants for this algorithm. Two different variables $x$ and $y$ at the same position are a disagreement and get a new variable.

## Implementations

## History

Gordon Plotkin and John C. Reynolds both introduced the least general generalization of terms in 1970, in two papers in the same volume of Machine Intelligence. Plotkin's motivation was inductive generalization, the step from examples to a general rule, and he also defined the lgg of clauses. Reynolds studied the lattice of atomic formulas under the instance order. The lgg of clauses later became the basis of inductive logic programming, and anti-unification became a tool in program analysis and code search.

## References
