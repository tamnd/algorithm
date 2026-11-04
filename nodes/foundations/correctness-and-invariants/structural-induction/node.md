---
tag: VNSQ4X
kind: technique
slug: structural-induction
name: Structural induction
aliases:
- Induction on structure
area: foundations/correctness-and-invariants
level: intro
summary: Induction over recursively defined objects such as trees and lists, proving a property for base cases and for each constructor.
prereqs: [induction]
see_also: [well-founded-relation, well-ordering-principle, termination-proof, binary-tree, loop-invariant, abstract-syntax-tree]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.3.1, Traversing binary trees (binary trees, internal and external nodes)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B, Section B.5, Trees (full binary trees)
  - paper: "R. M. Burstall, Proving properties of programs by structural induction, The Computer Journal 12(1) (1969), doi:10.1093/comjnl/12.1.41"
    locator: pages 41 to 48
  - url: https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/mit6_042js15_textbook2.pdf
    title: Eric Lehman, F. Thomson Leighton and Albert R. Meyer, Mathematics for Computer Science (2015 version)
    locator: Chapter 7, Recursive Data Types, Section 7.1 (recursive definitions and structural induction)
---

Structural induction is a proof technique for a property of objects that are built by rules, such as lists, trees and expressions. You prove the property for the simplest objects, and you prove that each rule that builds a new object keeps the property when the parts have it. It is [induction](/induction/) where the objects, not the numbers, carry the argument. A proof that a recursive algorithm is correct on a list or a tree is a structural induction on its input.

## In plain words

Many data types are built from small pieces by a few rules. A list is empty, or it is one item put in front of a shorter list. A tree is a single leaf, or it is a new root with two smaller trees below it. Each object is made by using the rules a finite number of times.

To show that all objects have a property, you follow the rules. First show that the simplest objects have it. Then take a rule that makes a new object from smaller ones. Assume that the smaller ones have the property, and show that the new object has it. Because every object comes from the rules, every object has the property.

A recursive function over such a type has the same shape as the rules, so its proof has one case for each rule.

## When it applies

- The objects are defined by an inductive definition: base objects, rules that build new objects from old ones, and the clause that nothing else is an object.
- The claim is about every object of the type, such as every list, every tree or every expression.
- The algorithm is recursive on the type, and each call is on a part of its argument.

For an object whose rules are not so clean, or for a claim about a graph, count the size of the object (nodes, edges, length) and use strong [induction](/induction/) on this number. The principle below shows that this is always possible.

## The template

**Lists.** The set of lists over a set $X$ is the smallest set that contains $\mathrm{nil}$ and contains $\mathrm{cons}(x, L)$ whenever $x \in X$ and $L$ is a list. The principle is

$$\big( P(\mathrm{nil}) \ \wedge\ \forall x \in X\ \forall L\ (P(L) \Rightarrow P(\mathrm{cons}(x, L))) \big) \ \Rightarrow\ \forall L\ P(L).$$

**Full binary trees.** The set of full binary trees is the smallest set that contains the one-node tree $\mathrm{leaf}$ and contains $\mathrm{node}(T_1, T_2)$ whenever $T_1$ and $T_2$ are full binary trees. The principle is

$$\big( P(\mathrm{leaf}) \ \wedge\ \forall T_1, T_2\ (P(T_1) \wedge P(T_2) \Rightarrow P(\mathrm{node}(T_1, T_2))) \big) \ \Rightarrow\ \forall T\ P(T).$$

**General form.** For an inductive definition with several rules, prove one case for each rule. A rule with no premise gives a base case. A rule with premises gives a step whose induction hypothesis is $P$ for each premise.

Write the proof in these parts.

1. **Define the type** and list its rules.
2. **State the predicate** $P(x)$ for an object $x$ of the type.
3. **Prove one case for each rule.** In each case, assume $P$ for the parts and prove $P$ for the new object. Name the places where you use the hypothesis.
4. **Conclude** that $P$ holds for every object.

**Why the principle holds.** Define the size $|x|$ of an object as the number of times that rules are used to build it. A part of an object has a smaller size than the object. Suppose the cases above are proved. We prove $P(x)$ by strong induction on $|x|$. Let $x$ be an object, and assume $P(y)$ for each object $y$ with $|y| < |x|$. By the clause "nothing else", $x$ was built by a rule from parts of smaller size. If the rule has no premise, $P(x)$ is the base case. Otherwise the parts satisfy $P$ by the assumption, and the step case gives $P(x)$. So $P(x)$ holds for each $x$. This also shows that the principle is a special case of induction on a [well-founded relation](/well-founded-relation/): the relation "is a part of".

## Classic examples

### Lists: the length of an append

Define $\mathrm{append}$ and $\mathrm{length}$ by recursion on the first argument:

$$\mathrm{append}(\mathrm{nil}, B) = B, \qquad \mathrm{append}(\mathrm{cons}(x, A), B) = \mathrm{cons}(x, \mathrm{append}(A, B)),$$

$$\mathrm{length}(\mathrm{nil}) = 0, \qquad \mathrm{length}(\mathrm{cons}(x, L)) = 1 + \mathrm{length}(L).$$

**Claim.** For all lists $A$ and $B$: $\mathrm{length}(\mathrm{append}(A, B)) = \mathrm{length}(A) + \mathrm{length}(B)$.

**Proof.** Fix $B$. Let $P(A)$ be the claim for $A$ and this $B$. Induction on $A$.

- *Case nil.* $\mathrm{length}(\mathrm{append}(\mathrm{nil}, B)) = \mathrm{length}(B) = 0 + \mathrm{length}(B) = \mathrm{length}(\mathrm{nil}) + \mathrm{length}(B)$.
- *Case cons.* Let $A = \mathrm{cons}(x, A')$ and assume $P(A')$. Then $\mathrm{length}(\mathrm{append}(A, B)) = \mathrm{length}(\mathrm{cons}(x, \mathrm{append}(A', B))) = 1 + \mathrm{length}(\mathrm{append}(A', B))$. By $P(A')$ this is $1 + \mathrm{length}(A') + \mathrm{length}(B) = \mathrm{length}(A) + \mathrm{length}(B)$.

By structural induction, $P(A)$ holds for each list $A$. $\blacksquare$

### Lists: append is associative

**Claim.** For all lists $A$, $B$ and $C$: $\mathrm{append}(\mathrm{append}(A, B), C) = \mathrm{append}(A, \mathrm{append}(B, C))$.

**Proof.** Fix $B$ and $C$, and use induction on $A$.

- *Case nil.* Both sides equal $\mathrm{append}(B, C)$, by the first equation of $\mathrm{append}$, used once on each side.
- *Case cons.* Let $A = \mathrm{cons}(x, A')$ and assume the claim for $A'$. The left side is $\mathrm{append}(\mathrm{cons}(x, \mathrm{append}(A', B)), C) = \mathrm{cons}(x, \mathrm{append}(\mathrm{append}(A', B), C))$. By the hypothesis this is $\mathrm{cons}(x, \mathrm{append}(A', \mathrm{append}(B, C)))$, which is the right side by the second equation of $\mathrm{append}$. $\blacksquare$

### Lists: a claim that must be generalised

A fast list reversal keeps an accumulator:

$$\mathrm{rev}(\mathrm{nil}, R) = R, \qquad \mathrm{rev}(\mathrm{cons}(x, L), R) = \mathrm{rev}(L, \mathrm{cons}(x, R)).$$

It takes time linear in the length of $L$. The slow reversal is $\mathrm{reverse}(\mathrm{nil}) = \mathrm{nil}$ and $\mathrm{reverse}(\mathrm{cons}(x, L)) = \mathrm{append}(\mathrm{reverse}(L), \mathrm{cons}(x, \mathrm{nil}))$. The goal is $\mathrm{rev}(L, \mathrm{nil}) = \mathrm{reverse}(L)$. A direct induction on $L$ fails: in the step, $\mathrm{rev}(\mathrm{cons}(x, L), \mathrm{nil}) = \mathrm{rev}(L, \mathrm{cons}(x, \mathrm{nil}))$, and the hypothesis is about $\mathrm{rev}(L, \mathrm{nil})$ only. The fix is to prove a more general claim, with the accumulator quantified inside the predicate.

**Claim.** For each list $L$, the predicate $P(L)$ holds: for all lists $R$, $\mathrm{rev}(L, R) = \mathrm{append}(\mathrm{reverse}(L), R)$.

**Proof.** Induction on $L$.

- *Case nil.* $\mathrm{rev}(\mathrm{nil}, R) = R = \mathrm{append}(\mathrm{nil}, R) = \mathrm{append}(\mathrm{reverse}(\mathrm{nil}), R)$.
- *Case cons.* Let $L = \mathrm{cons}(x, L')$, assume $P(L')$, and let $R$ be any list. Then $\mathrm{rev}(L, R) = \mathrm{rev}(L', \mathrm{cons}(x, R))$. By $P(L')$, used with the list $\mathrm{cons}(x, R)$ in place of $R$, this is $\mathrm{append}(\mathrm{reverse}(L'), \mathrm{cons}(x, R))$. On the other side, $\mathrm{append}(\mathrm{reverse}(L), R) = \mathrm{append}(\mathrm{append}(\mathrm{reverse}(L'), \mathrm{cons}(x, \mathrm{nil})), R)$. By associativity this is $\mathrm{append}(\mathrm{reverse}(L'), \mathrm{append}(\mathrm{cons}(x, \mathrm{nil}), R))$, and $\mathrm{append}(\mathrm{cons}(x, \mathrm{nil}), R) = \mathrm{cons}(x, R)$ by the two equations of $\mathrm{append}$. The two sides are equal. $\blacksquare$

With $R = \mathrm{nil}$ and the fact $\mathrm{append}(A, \mathrm{nil}) = A$ (a short induction on $A$), this gives $\mathrm{rev}(L, \mathrm{nil}) = \mathrm{reverse}(L)$. For $L = [1, 2, 3]$, the calls of $\mathrm{rev}$ go through the pairs $([1, 2, 3], [\,])$, $([2, 3], [1])$, $([3], [2, 1])$ and $([\,], [3, 2, 1])$. The step used the hypothesis with a different accumulator. If $R$ is fixed before the induction, as $B$ was in the length claim, the proof fails.

### Full binary trees: leaves and internal nodes

A full binary tree is a tree in which each node has 0 or 2 children. In the inductive definition above, the nodes built by $\mathrm{node}$ are the *internal* nodes, and the one-node trees $\mathrm{leaf}$ are the *leaves*. Define two functions by recursion:

$$i(\mathrm{leaf}) = 0, \quad i(\mathrm{node}(T_1, T_2)) = i(T_1) + i(T_2) + 1,$$

$$\ell(\mathrm{leaf}) = 1, \quad \ell(\mathrm{node}(T_1, T_2)) = \ell(T_1) + \ell(T_2).$$

**Claim.** For each full binary tree $T$: $\ell(T) = i(T) + 1$. In words, a full binary tree with $n$ internal nodes has $n + 1$ leaves.

**Proof.** Let $P(T)$ be $\ell(T) = i(T) + 1$. Induction on $T$.

- *Case leaf.* $\ell(\mathrm{leaf}) = 1 = 0 + 1 = i(\mathrm{leaf}) + 1$.
- *Case node.* Let $T = \mathrm{node}(T_1, T_2)$, and assume $P(T_1)$ and $P(T_2)$, that is, $\ell(T_1) = i(T_1) + 1$ and $\ell(T_2) = i(T_2) + 1$. Then
  $$\ell(T) = \ell(T_1) + \ell(T_2) = (i(T_1) + 1) + (i(T_2) + 1) = (i(T_1) + i(T_2) + 1) + 1 = i(T) + 1.$$

By structural induction, $P(T)$ holds for each full binary tree $T$. $\blacksquare$

Two consequences follow at once. A full binary tree with $n$ internal nodes has $n + (n+1) = 2n + 1$ nodes in all. The number of leaves is at most $2^h$ for a tree of height $h$; this is the next claim.

**Claim.** If $T$ has height $h(T)$, where $h(\mathrm{leaf}) = 0$ and $h(\mathrm{node}(T_1, T_2)) = 1 + \max(h(T_1), h(T_2))$, then $\ell(T) \le 2^{h(T)}$.

**Proof.** For $\mathrm{leaf}$, $\ell = 1 = 2^0$. For $T = \mathrm{node}(T_1, T_2)$, assume $\ell(T_k) \le 2^{h(T_k)} \le 2^{h(T) - 1}$ for $k = 1, 2$. Then $\ell(T) = \ell(T_1) + \ell(T_2) \le 2 \cdot 2^{h(T)-1} = 2^{h(T)}$. $\blacksquare$

For the small tree $\mathrm{node}(\mathrm{node}(\mathrm{leaf}, \mathrm{leaf}), \mathrm{leaf})$ we get $i = 2$, $\ell = 3$ and $h = 2$. For $n = 0, 1, 2, 3, 4$ internal nodes there are $1, 1, 2, 5, 14$ full binary trees, and all of them have $n + 1$ leaves.

### A recursive algorithm

```pseudo id=count-leaves
COUNT-LEAVES(T)                   ▷ T a full binary tree
L1  if T is a leaf then return 1
L2  return COUNT-LEAVES(T.left) + COUNT-LEAVES(T.right)
```

**Claim.** COUNT-LEAVES$(T) = \ell(T)$ and the call stops. *Proof.* Structural induction on $T$. If $T$ is a leaf, line L1 returns $1 = \ell(T)$. If $T = \mathrm{node}(T_1, T_2)$, the calls in line L2 are on $T_1$ and $T_2$, which are parts of $T$. By the hypothesis they stop and return $\ell(T_1)$ and $\ell(T_2)$. So line L2 returns $\ell(T)$. $\blacksquare$ The same induction proves termination: each call is on a part of its argument, so the number of nodes drops at each call.

## Variations

- **Several constructors.** A type with more rules, such as expressions with sums, products and numbers, has one case for each rule.
- **Binary trees that need not be full.** Add the empty tree as a base object, and give $\mathrm{node}(L, x, R)$ two premises. A binary tree with $n$ nodes then has $n + 1$ empty subtrees, and the proof is the same as above.
- **Induction on the size or the height.** If the rules are unclear, use strong induction on the number of nodes or on the height.
- **Mutual induction.** For types defined in terms of each other, such as a tree of forests and a forest of trees, prove the claims for both types together.
- **Well-founded induction.** For any [well-founded relation](/well-founded-relation/), the same shape holds: assume $P$ for all smaller objects, and prove $P$ for the object. Structural induction is the case where "smaller" means "is a part of".
- **Rule induction.** For a set defined by inference rules, such as the derivable judgements of a logic, prove that $P$ is kept by each rule.

## Pitfalls

- **A missing case.** Each rule needs a case. The base case is often forgotten when a type has several base objects.
- **A hypothesis on the wrong object.** The hypothesis is only for the parts used to build the object. It does not hold for the object itself, and it does not hold for an unrelated object of the same size.
- **Using a fact about the whole in a step.** In the step for $\mathrm{node}(T_1, T_2)$, do not assume that $T$ has the property. Assume it only for $T_1$ and $T_2$.
- **Infinite objects.** The principle covers objects that are built in a finite number of steps. An infinite list, such as a stream, is not covered, and the claim may be false for it. Streams need coinduction or a claim about each finite prefix.
- **Trees with other shapes.** The claim $\ell = i + 1$ is false if a node may have one child. A chain of nodes, each with a single child, has one leaf and many internal nodes. Check that the definition of the type matches the claim.
- **A fixed variable that the step must change.** In the claim about $\mathrm{rev}$, the accumulator must stay quantified inside $P$. Fix only the variables that the recursion passes unchanged.
- **An ambiguous definition.** A definition by recursion on the rules gives a function only when each object is built in exactly one way. If expressions are built by $E ::= n \mid E - E$ with no parentheses, the string $8 - 4 - 2$ has two parse trees, and the "value" defined by recursion is both $2$ and $6$. Structural induction on such a set is still valid, but recursion on it is not. Use [abstract syntax trees](/abstract-syntax-tree/), or a grammar in which each string has one [parse tree](/parse-tree/).
- **A function that is not defined by the rules.** If $\mathrm{length}$ is defined by recursion on a type, the proof is easy. If it is defined in another way, first prove that it satisfies the recursive equations.

## Exercises

1. Prove by structural induction that $\mathrm{length}(\mathrm{reverse}(L)) = \mathrm{length}(L)$, where $\mathrm{reverse}(\mathrm{nil}) = \mathrm{nil}$ and $\mathrm{reverse}(\mathrm{cons}(x, L)) = \mathrm{append}(\mathrm{reverse}(L), \mathrm{cons}(x, \mathrm{nil}))$. You can use the append claim above.
2. Prove that $\mathrm{append}(A, \mathrm{nil}) = A$ for each list $A$.
3. Prove that a full binary tree with $n$ internal nodes has exactly $2n$ edges.
4. Define the size of a binary tree (not necessarily full) as the number of its nodes, and the number of empty subtrees as $e$. Prove that a binary tree with $n$ nodes has $e = n + 1$.
5. Prove that a full binary tree of height $h$ has at least $2h + 1$ nodes.
6. Write a recursive function that returns the height of a full binary tree, and prove by structural induction that its result is equal to $h(T)$ as defined above.
7. List all the full binary trees with 3 internal nodes. There are 5.
8. Show by an example that the claim $\ell = i + 1$ fails for trees whose nodes may have one child.

## References
