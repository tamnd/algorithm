---
tag: JEGV8S
kind: algorithm
slug: stickel-ac-unification
name: Stickel's AC-unification algorithm
aliases:
- AC unification algorithm
- Stickel's algorithm
area: logic-and-constraints/unification-and-resolution
level: research
summary: Complete algorithm that computes a finite complete set of associative-commutative unifiers from the minimal solutions of a linear Diophantine equation.
solves: [ac-unification-problem]
model: word-ram
complexity:
  vars: {m: the number of distinct arguments after cancellation, b: the number of minimal Diophantine solutions, c: the largest multiplicity of an argument}
  time: {worst: O((c+1)^m m + 2^b b m)}
  space: {extra: O(2^b b m)}
properties: {deterministic: true, exact: true, online: false, recursive: false, in_place: false}
history:
  year: 1975
  people: [Mark E. Stickel]
  note: Stickel presented the algorithm in 1975 and published the full version in 1981; Fages proved in 1984 and 1987 that the general version terminates.
prereqs: [ac-unification-problem, equational-unification, linear-diophantine-equation, substitution]
see_also: [linear-diophantine-system, ac-matching, rewriting-modulo-equations, knuth-bendix-completion, most-general-unifier, martelli-montanari-unification]
sources:
  - paper: "M. E. Stickel, A unification algorithm for associative-commutative functions, Journal of the ACM 28(3), 1981, pages 423 to 434"
    locator: the reduction of an AC equation to a homogeneous linear Diophantine equation, the combination of basis solutions, and the general algorithm with free symbols
  - paper: "F. Fages, Associative-commutative unification, Journal of Symbolic Computation 3(3), 1987, pages 257 to 275"
    locator: the termination proof of the general algorithm with several AC symbols
  - paper: "G. Huet, An algorithm to generate the basis of solutions to homogeneous linear Diophantine equations, Information Processing Letters 7(3), 1978, pages 144 to 147"
    locator: the bound on the coordinates of a minimal solution and the generation of the basis
  - paper: "D. Kapur and P. Narendran, Double-exponential complexity of computing a complete set of AC-unifiers, Proceedings of the Seventh IEEE Symposium on Logic in Computer Science, 1992, pages 11 to 21"
    locator: the doubly exponential bounds on the size of minimal complete sets of AC unifiers
  - book: isbn:9780444508133
    title: Franz Baader and Wayne Snyder, Unification Theory, in J. A. Robinson and A. Voronkov (editors), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Volume I, Chapter 8, Section 3 (unification in commutative theories, the AC case and its complexity)
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Chapter 10, Equational unification (unification in commutative theories and the role of linear Diophantine equations)
---

**Stickel's algorithm** computes a finite complete set of unifiers modulo associativity and commutativity (AC), and so solves the [AC unification problem](/ac-unification-problem/). Its central idea is to count. Modulo AC, a sum is a multiset of arguments, so an equation such as $x + x \doteq y + z$ is about how many copies of each piece go into each variable. These counts must solve the linear Diophantine equation $2x' = y' + z'$ over the natural numbers. The algorithm computes the minimal solutions of that equation, gives each one a new variable, and builds one unifier for each admissible subset of them. Mark Stickel gave it in 1975 (journal version 1981), and François Fages proved that the general version terminates. This page treats the core case of one AC symbol with variables and free constants, and describes the general case under Variants.

## In plain words

Think of $+$ as putting things into one bag, where order and grouping do not matter. The equation $x + x = y + z$ says: two copies of bag $x$ hold the same things as bag $y$ and bag $z$ together.

Each kind of thing that ends up in these bags must be counted the same on both sides. So each kind follows a counting pattern: one thing in $x$ means two in $z$, or one in each of $x$, $y$ and $z$, or one in $x$ and two in $y$. There are only a few basic patterns, and every possible answer mixes them. The algorithm lists the basic patterns, gives each a fresh name, and then tries every mix in which every bag gets something. Each such mix is one answer, and together they cover all answers.

## The problem

Notation: $+$ is an AC symbol, $=_{AC}$ is equality modulo associativity and commutativity, and $\sigma, \theta, \lambda$ are substitutions. A term that is not a sum is an **atom**. Modulo AC, a sum is the multiset of its atoms. There is no unit element, so a variable cannot become the empty sum. $X = \mathrm{Var}(s, t)$, and $\sigma \le_{AC}^X \theta$ means that $x\theta =_{AC} x\sigma\lambda$ for some $\lambda$ and each $x \in X$.

**Input:** two sums $s$ and $t$ of variables and free constants.

**Output:** a finite set $U$ of AC-unifiers such that every AC-unifier $\theta$ of $s$ and $t$ has some $\sigma \in U$ with $\sigma \le_{AC}^X \theta$. If $U$ is empty, $s$ and $t$ have no AC-unifier.

## The algorithm

```pseudo id=main
STICKEL(s, t)
L1  flatten s and t to multisets of arguments; remove the common arguments
L2  if both sides are empty then return {identity}; if one side is empty then return ∅
L3  list the distinct arguments as columns: c₁..cₚ on the left with multiplicities a₁..aₚ, d₁..d_q on the right with b₁..b_q
L4  B ← the minimal nonzero solutions v₁..v_r of Σ aᵢ v(cᵢ) = Σ bⱼ v(dⱼ) over ℕ; give vₖ a new variable zₖ
L5  U ← ∅
L6  for each nonempty subset K ⊆ B do
L7      if some column has sum 0 over K then skip K
L8      if some constant column has sum ≠ 1 over K then skip K
L9      for each constant column c: the one k ∈ K with vₖ(c) = 1 gets wₖ ← c; every other k ∈ K gets wₖ ← zₖ
L10     if some zₖ gets two different constants then skip K
L11     for each variable column x: σ(x) ← Σ_{k ∈ K} vₖ(x) · wₖ
L12     U ← U ∪ {σ}
L13 return U
```

L4 uses Huet's bound (1978): in a minimal solution, $v(c_i) \le \max_j b_j$ and $v(d_j) \le \max_i a_i$. The implementation searches this box and keeps the minimal vectors.

The conditions of L7 to L10 have a direct meaning. L7: no variable may be empty, and every constant must be produced. L8: a constant is an atom, so exactly one basis piece may produce it, and only once. L10: one new variable cannot be two different constants.

## Example

**$x + x \doteq y + z$.** The columns are $x$ on the left with multiplicity 2, and $y$, $z$ on the right. The equation $2v(x) = v(y) + v(z)$ has three minimal solutions $(v(x), v(y), v(z))$:

| basis vector | new variable | meaning |
|---|---|---|
| $(1, 0, 2)$ | $z_1$ | one $z_1$ in $x$, two in $z$ |
| $(1, 1, 1)$ | $z_2$ | one $z_2$ in each of $x$, $y$, $z$ |
| $(1, 2, 0)$ | $z_3$ | one $z_3$ in $x$, two in $y$ |

A subset passes L7 when it covers the columns $y$ and $z$. The five such subsets give five unifiers:

| $K$ | $x$ | $y$ | $z$ |
|---|---|---|---|
| $\{2\}$ | $z_2$ | $z_2$ | $z_2$ |
| $\{1, 2\}$ | $z_1 + z_2$ | $z_2$ | $z_1 + z_1 + z_2$ |
| $\{1, 3\}$ | $z_1 + z_3$ | $z_3 + z_3$ | $z_1 + z_1$ |
| $\{2, 3\}$ | $z_2 + z_3$ | $z_2 + z_3 + z_3$ | $z_2$ |
| $\{1, 2, 3\}$ | $z_1 + z_2 + z_3$ | $z_2 + z_3 + z_3$ | $z_1 + z_1 + z_2$ |

The subsets $\{1\}$ and $\{3\}$ fail L7, since they leave $y$ or $z$ empty. For instance, in the row $\{1, 3\}$, $x\sigma + x\sigma = z_1 + z_1 + z_3 + z_3 = y\sigma + z\sigma$.

**With constants: $x + a \doteq y + b$.** The columns are $x, a$ on the left and $y, b$ on the right, all with multiplicity 1. The basis has the four vectors that pair one left column with one right column: $xy$, $xb$, $ay$, $ab$. The column $a$ must have the sum 1 (L8), so exactly one of $ay$, $ab$ is chosen, and in the same way exactly one of $xb$, $ab$. The vector $ab$ would make its variable equal to both $a$ and $b$, so L10 removes it. Two subsets remain: $\{xb, ay\}$ gives $\{x \mapsto b, y \mapsto a\}$, and $\{xy, xb, ay\}$ gives $\{x \mapsto b + z, y \mapsto a + z\}$.

More examples:

| equation | basis size | unifiers |
|---|---|---|
| $x + y \doteq u + v$ | 4 | 7 |
| $x + x + y \doteq z + a$ | 5 | 4 |
| $x + x + x \doteq y + y$ | 1 | 1: $\{x \mapsto z_1 + z_1, y \mapsto z_1 + z_1 + z_1\}$ |
| $x + x \doteq y + y + y + z$ | 3 | 5 |
| $x_1 + \cdots + x_n \doteq y_1 + \cdots + y_n$ | $n^2$ | 1, 7, 265, 41503 for $n = 1, 2, 3, 4$ |

In the last row, the basis vectors are the pairs $(x_i, y_j)$, and the admissible subsets are the edge covers of the complete bipartite graph $K_{n,n}$. Their number grows like $2^{n^2}$.

## Correctness

- **Cancellation (L1, L2).** A common argument can be removed from both sides, because the multisets of atoms of the two instances then lose the same part. If one side becomes empty and the other does not, no unifier exists, since there is no unit.
- **Soundness (L6 to L12).** For a chosen $K$, both $s\sigma$ and $t\sigma$ contain each $w_k$ exactly $L(v_k) = R(v_k)$ times, where $L$ and $R$ are the two sides of the equation. So $s\sigma =_{AC} t\sigma$. L8 and L9 make sure that each constant of the input is produced by exactly one piece.
- **Completeness.** Let $\theta$ be any AC-unifier. For each atom $u$ of the instances, count how often $u$ occurs in each $x\theta$. This count vector solves the Diophantine equation, so it is a sum of basis vectors. The basis vectors used by some atom form a subset $K$ that passes L7, L8 and L10. Mapping each $z_k$ to the sum of the atoms that use $v_k$ gives $\lambda$ with $x\sigma\lambda =_{AC} x\theta$.
- **Termination.** The basis is finite by Dickson's lemma, so there are finitely many subsets.

The full proof is below.

## Complexity

Let $m = p + q$ be the number of columns, $c$ the largest multiplicity, and $b$ the size of the basis.

- **Basis.** The search of the box from Huet's bound tries at most $(c + 1)^m$ vectors, each in $O(m)$ time. Better algorithms exist, but the basis itself can be exponentially large in $m$.
- **Subsets.** L6 tries $2^b - 1$ subsets, each in $O(b m)$ time, and the output can have about $2^b$ unifiers.

So the time is $O((c + 1)^m m + 2^b b m)$. For $x_1 + \cdots + x_n \doteq y_1 + \cdots + y_n$, $b = n^2$ and the number of unifiers grows like $2^{n^2}$. In general, minimal complete sets of AC unifiers can be doubly exponential in the size of the problem (Kapur and Narendran 1992), so no algorithm that lists such a set can be fast in the worst case. Deciding only whether a unifier exists is NP-complete.

## Properties

- The output is complete, but it is not always minimal. With constants, some outputs can be instances of others.
- For elementary AC equations without constants, every subset that passes L7 gives a unifier, so the output size is the number of subsets of the basis that cover all columns.
- The method is a reduction: AC equations become a linear Diophantine equation over $\mathbb{N}$, and the unifiers are built from its Hilbert basis.
- It is deterministic, and the result does not depend on the order of the arguments, up to renaming of the new variables.

## Variants and improvements

- **Free symbols and nested terms.** In general the arguments of a sum can be terms with other symbols. The general algorithm first replaces each argument that is not a variable by a new variable and records an equation for it. It then solves the AC equation as above, without the constant rules, and finally unifies the recorded equations recursively, with syntactic unification for free symbols and AC unification for other AC symbols. Stickel's termination argument for this general case was incomplete. Fages (1984, journal version 1987) gave a full proof.
- **Several equations.** Systems of AC equations give systems of linear Diophantine equations. Their Hilbert bases can be computed by the algorithm of Contejean and Devie, and AC unification algorithms that solve all equations at once avoid much repeated work.
- **Pruning subsets.** Many subsets lead to the same unifier or to failure in the recursive step. Later implementations order and prune the subsets. For example, a subset in which the column of a non-variable argument has a sum larger than 1 can be rejected at once, because a term with a free top symbol is a single atom.
- **ACU, ACI and other theories.** With a unit element, variables may be empty, and every solution of the Diophantine equation is allowed. For abelian monoids, elementary unification is then unitary. Adding idempotence or inverses changes the arithmetic to sets or to integers.
- **AC matching.** If one side has no variables, the problem is [AC matching](/ac-matching/), which is NP-complete but much simpler in practice.

## When to use it

Use it when a theorem prover, a [completion procedure](/knuth-bendix-completion/) or a rewriting engine must reason modulo AC, for example with $+$ and $\cdot$ in algebra, or with set and multiset union. The cost is real: equations with many variables under one AC symbol produce huge sets of unifiers. Systems that only need matching should use AC matching. Systems that can avoid AC unification, for example by orienting equations or by using ordered rewriting, often do so.

## Pitfalls

- **No unit element.** In pure AC, a variable cannot be empty, which is why L7 removes subsets that leave a column empty. Allowing empty values gives unifiers that are wrong for AC.
- **Constants are atoms.** A constant must come from exactly one basis piece with coefficient 1. Without L8 and L10, the algorithm would split a constant or make one variable equal to two constants.
- **Fresh names.** The new variables $z_k$ must not occur in the input.
- **Size.** The number of unifiers can be huge. Code that stores all of them at once can run out of memory, so a lazy enumeration is often better.
- **Termination of the general case.** In the general algorithm, the recursion must be organized so that it ends. Stickel's original argument had a gap, and Fages's proof covers it.

## Implementations

## History

Stickel presented the algorithm in 1975 and published the complete version in the Journal of the ACM in 1981. Huet (1978) gave a bound and an algorithm for the minimal solutions of homogeneous linear Diophantine equations. Fages proved in 1984 that the general algorithm terminates, with a journal version in 1987. Later work by Kapur and Narendran located the complexity: AC unifiability is NP-complete, and minimal complete sets can be doubly exponential.

## References
