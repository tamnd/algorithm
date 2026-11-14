---
tag: VCCME7
kind: technique
slug: unate-recursive-paradigm
name: Unate recursive paradigm
aliases:
- URP
area: cad/logic-synthesis
level: core
summary: Solves an operation on a cover, such as tautology or complement, by Shannon splitting on binate variables until each part is unate and easy, then merging.
prereqs: [shannon-expansion, cofactor, unate-function, sum-of-products]
see_also: [espresso, divide-and-conquer-paradigm, binary-decision-diagram, co-np-complete, boolean-equivalence-checking, two-level-logic-minimization, implicant, sat]
sources:
  - book: isbn:9780898381641
    title: Robert K. Brayton, Gary D. Hachtel, Curtis T. McMullen and Alberto L. Sangiovanni-Vincentelli, Logic Minimization Algorithms for VLSI Synthesis, Kluwer, 1984
    locator: Chapter 3, Decomposition and Unate Functions (Sections 3.1 Cofactors and Shannon Expansion, 3.3 Unate Functions, 3.4 Choice of Splitting Variable, 3.5 Unate Complementation), and Chapter 4, Sections 4.1 Complementation and 4.2 Tautology
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 7, Two-Level Combinational Logic Optimization (the recursive operators on covers, tautology and complementation)
  - book: isbn:9780792397465
    title: Gary D. Hachtel and Fabio Somenzi, Logic Synthesis and Verification Algorithms, Kluwer, 1996
    locator: Chapter 5, Heuristic Minimization of Two-Level Circuits (the unate recursive paradigm and its operators)
---

The unate recursive paradigm is a way to compute an operation on a cover, a list of cubes that stands for a [sum of products](/sum-of-products/), without building the truth table. Split the cover by the [Shannon expansion](/shannon-expansion/) $f = \bar{x} f_{\bar{x}} + x f_x$ on one variable, solve the operation on the two [cofactors](/cofactor/), and merge the two answers. Choose the variable so that the parts become [unate](/unate-function/) fast, because on a unate cover the hard operations are easy: a unate cover is a tautology exactly when it holds the cube with no literal. Brayton, Hachtel, McMullen and Sangiovanni-Vincentelli (1984) built the operators of [Espresso](/espresso/) on this scheme: tautology, containment of a cube in a cover, complement, and others. The recursion is exponential in the worst case, since tautology of a cover is [co-NP-complete](/co-np-complete/), but on the covers met in logic design it stops early.

## In plain words

You have a list of AND terms and want to know something about their OR, such as "is it always 1?". Pick one input and look at two cases: the input is 0, and the input is 1. In each case the list gets simpler, since some terms drop out and others lose a letter. Answer the question for each case, then put the two answers together.

Some lists are easy. If no input appears both plain and negated in the list, the OR is always 1 only when one term has no letters at all. So pick the input that most often appears both ways, and the easy case comes soon.

## When it applies

- The function is given as a cover, and the truth table is too large to build.
- The operation can be computed from the two cofactors by a simple merge. Tautology is the AND of the two answers, and the complement is $\bar{x} \cdot \overline{f_{\bar{x}}} + x \cdot \overline{f_x}$.
- The operation has a cheap answer on a unate cover, or on a cover with one cube, so the recursion can stop before the leaves are single points.
- The cover is not too far from unate. On a cover where every variable is binate in every part, the recursion is a full binary tree of depth $n$.

## The template

A cube is a string over $\{0, 1, -\}$, and a cover is a list of cubes. The cofactor of a cover by $x_i = b$ drops each cube with the literal of the other value at position $i$, and sets position $i$ to $-$ in the cubes that are left. A cover is unate when no variable appears in it with both literals. The splitting rule takes the binate variable that is in the most cubes, then the one whose two literal counts are closest. On a unate cover it takes the variable in the most cubes.

The holes of the template are the leaf test, the splitting rule and the merge. Two instances fill them as follows.

```pseudo id=main
TAUTOLOGY(F)                        ▷ is the OR of the cubes of F equal to 1?
L1  if F = ∅ then return false
L2  if F holds the cube - - ... - then return true
L3  if F is unate then return false
L4  if the minterm counts of the cubes of F add up to less than 2^n then return false
L5  x ← the splitting variable of F
L6  return TAUTOLOGY(F with x = 0) and TAUTOLOGY(F with x = 1)

COMPLEMENT(F)                       ▷ a cover of the points where F is 0
L7  if F = ∅ then return { - - ... - }
L8  if F holds the cube - - ... - then return ∅
L9  if F has one cube c then return one cube for each literal of c, with that literal negated
L10 x ← the splitting variable of F
L11 G0 ← COMPLEMENT(F with x = 0), G1 ← COMPLEMENT(F with x = 1)
L12 return the cubes in both G0 and G1 as they are, the other cubes of G0 with x̄, and the other cubes of G1 with x
L13     after removing each cube that lies inside another cube of the result
```

**Why line L3 is right.** Let $F$ be unate and without the cube of no literal. Build a point $a$: if $x_i$ appears in $F$ only as $x_i$, set $a_i = 0$; if only as $\bar{x}_i$, set $a_i = 1$; if not at all, set $a_i$ to any value. Every cube of $F$ has a literal, and $a$ makes that literal 0, so $F(a) = 0$. So a unate cover is a tautology exactly when line L2 applies.

**Why line L4 is right.** A cube with $k$ dashes holds $2^k$ points. If the counts add up to less than $2^n$, the cubes cannot hold all $2^n$ points, even with no overlap.

**Why lines L6 and L12 are right.** By the Shannon expansion, $F = 1$ exactly when $F_{\bar{x}} = 1$ and $F_x = 1$, and $\bar{F} = \bar{x} \cdot \overline{F_{\bar{x}}} + x \cdot \overline{F_x}$. A cube $c$ that is in both $G_0$ and $G_1$ gives $\bar{x} c + x c = c$, so it needs no literal of $x$. Line L13 only removes cubes inside other cubes, which does not change the function. Line L9 is De Morgan's law for one cube.

**Why it stops.** A cofactor by $x$ sets position $x$ to $-$ in every cube that is left. At line L5 the cover is binate, so $x$ appears in it. At line L10 the cover has at least two cubes and none is the cube of no literal, so the chosen $x$ appears in some cube. So each call reduces the number of positions that hold a literal in some cube, and the depth is at most $n$.

**Cost.** Each call spends $O(n |F|)$ time on the cofactors, the counts and the tests. The recursion tree has at most $2^n$ leaves, and in the worst case it is that large: tautology of a cover is co-NP-complete. The leaf tests of lines L2 to L4 and L9 cut the tree, and the splitting rule is chosen to reach them early. The complement can also be exponential in its output alone: the cover $x_1 x_2 + x_3 x_4 + \cdots + x_{2k-1} x_{2k}$ has $k$ cubes, and its complement, the product $(\bar{x}_1 + \bar{x}_2) \cdots (\bar{x}_{2k-1} + \bar{x}_{2k})$, needs $2^k$ cubes in any sum of products.

**Example.** Take $F = \{1\text{-}0,\ 0\text{-}1,\ \text{-}\text{-}1\}$ over $x_1 x_2 x_3$. The variable $x_1$ is binate in two cubes, and $x_3$ is binate in all three, so line L5 picks $x_3$. The cofactor by $x_3 = 0$ is $\{1\text{-}\text{-}\}$, which is unate and has no universal cube, so line L3 returns false. So $F$ is not a tautology. Indeed, the point $x_1 = 0, x_3 = 0$ is 0 for all three cubes.

## Classic examples

- **Tautology and containment.** A cube $c$ lies inside a cover $F$ exactly when the cofactor $F_c$ is a tautology. [Espresso](/espresso/) uses this test to find redundant cubes in its IRREDUNDANT step.
- **Complement.** Espresso computes the off-set of the function as the complement of the on-set plus the don't-care set, by the recursion of lines L7 to L13, and its EXPAND step checks each raise of a cube against it.
- **Equivalence of two covers.** Two covers $F$ and $G$ are equal when each cube of $F$ lies in $G$ and each cube of $G$ lies in $F$. This is a small form of [Boolean equivalence checking](/boolean-equivalence-checking/) with tautology as the oracle.
- **Building a BDD.** A [binary decision diagram](/binary-decision-diagram/) is built by the same Shannon recursion, but it stores and shares the cofactors in place of throwing them away.
- **Satisfiability of a product of sums.** The dual question, whether a CNF has a satisfying point, is [SAT](/sat/). The complement of a cover is 0 everywhere exactly when the cover is a tautology, so DPLL search and the tautology recursion split on variables in the same way.

## Variations

- **Unate leaves for the complement.** Brayton and coauthors give a separate method for the complement of a unate cover, in their section on unate complementation. The code of this page uses the general recursion down to one cube in place of it.
- **Other operators.** The same template computes the intersection of two covers, the cofactor by a cube, and the set of primes of a cover, each with its own leaf rule and merge.
- **Component split.** If the cubes of a cover fall into groups with no shared variable, the cover is a tautology exactly when one group is. Testing this before the split cuts the tree.
- **Splitting rules.** The rule can weigh the counts in other ways, or prefer variables in the largest cubes. All correct rules give the same answer, and they differ only in time.
- **Multiple-valued variables.** Espresso-MV applies the same recursion to variables with more than two values, where a split has one branch per value.

## Pitfalls

- **A unate function is not a unate cover.** Line L3 tests the cover, not the function. The cover $\{1\text{-}, 0\text{-}\}$ is a tautology, and its function, the constant 1, is unate, but no cube of the cover is the universal cube. A test of line L3 on the function would return false here, which is wrong. The rule holds for unate covers only.
- **Splitting on an absent variable.** If line L5 or line L10 picks a variable that appears in no cube, both cofactors equal $F$ and the recursion never stops.
- **Losing the merge at line L12.** Adding $\bar{x}$ to every cube of $G_0$ and $x$ to every cube of $G_1$ is correct, but a cube $c$ in both halves then becomes the two cubes $\bar{x} c$ and $x c$. Neither lies inside the other, so line L13 does not remove them, and the result has more cubes and literals than needed.
- **Counting minterms with overlap.** Line L4 can only reject. A sum of $2^n$ or more does not mean a tautology, because cubes overlap.
- **The don't-cares.** A tautology test for a function with don't-cares must use the on-set plus the don't-care set as the cover, since the points of the don't-care set may be covered or not.

## Exercises

1. Prove that the complement of a unate cover is a unate function, with each variable in the opposite polarity.
2. Show that the cover $\{0\text{-}, 10, 11\}$ is a tautology by the recursion, and draw its recursion tree.
3. Give a family of covers on which TAUTOLOGY, with the splitting rule of this page, builds a tree with $2^{n-1}$ leaves or more.
4. Prove that the cube $c$ lies inside the cover $F$ exactly when the cofactor $F_c$ is a tautology.
5. Write the merge for the intersection of two covers, and prove it correct by the Shannon expansion.

## References
