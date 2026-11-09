---
tag: 5EARHB
kind: algorithm
slug: e-matching
name: E-matching
aliases:
- matching modulo equalities
- matching modulo ground equations
- e-graph matching
area: logic-and-constraints/smt
level: research
summary: Finds all ways to make a pattern with variables equal to a term in an e-graph, modulo its ground equalities. SMT solvers use the matches to instantiate quantified formulas.
solves: [smt-problem]
model: word-ram
complexity:
  vars: {m: the number of symbols in the pattern, n: the number of nodes in the e-graph}
  time: {worst: O(m n^m)}
  space: {extra: O(m n^m)}
properties: {deterministic: true, recursive: true}
history:
  year: 2005
  people: [David Detlefs, Greg Nelson, James B. Saxe]
  note: The Simplify prover matched triggers in its e-graph to instantiate quantifiers, an idea that goes back to Nelson's work on cooperating decision procedures. De Moura and Bjørner made it efficient for Z3 in 2007.
prereqs: [e-graph, congruence-closure, quantifier-instantiation]
see_also: [euf-satisfiability, smt-lib, hash-consing, term-dag, cdcl-t, model-based-theory-combination, incremental-solving, np-complete]
sources:
  - paper: doi:10.1145/1066100.1066102
    title: David Detlefs, Greg Nelson and James B. Saxe, Simplify, a theorem prover for program checking, Journal of the ACM 52(3), 2005, pages 365 to 473
    locator: the E-graph, triggers and multi-triggers, the matching of triggers modulo the E-graph, and matching loops
  - paper: doi:10.1007/978-3-540-73595-3_13
    title: Leonardo de Moura and Nikolaj Bjørner, Efficient E-matching for SMT solvers, CADE-21, LNCS 4603, 2007, pages 183 to 198
    locator: the recursive matching function, its compilation into an abstract machine with code trees, and incremental matching of new terms
  - book: isbn:9781643681603
    title: Clark Barrett, Roberto Sebastiani, Sanjit A. Seshia and Cesare Tinelli, Satisfiability Modulo Theories, Chapter 33 of the Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Section 33.7.2 (the instantiation rules, triggers, T-matching and E-matching, and the remark that the most effective techniques are incomplete and heuristic)
  - url: https://smt-lib.org/papers/smt-lib-reference-v2.7-r2025-07-07.pdf
    title: Clark Barrett, Pascal Fontaine and Cesare Tinelli, The SMT-LIB Standard, Version 2.7, release of July 7, 2025
    locator: Section 3.6.5 (the :pattern attribute, multi-patterns, the transitivity example, and footnote 7 on the use of the matching substitution)
  - paper: doi:10.1007/978-3-642-02658-4_25
    title: Yeting Ge and Leonardo de Moura, Complete instantiation for quantified formulas in satisfiability modulo theories, CAV 2009, LNCS 5643, pages 306 to 320
    locator: the essentially uninterpreted fragment and model-based quantifier instantiation, a complete alternative to E-matching on that fragment
  - paper: doi:10.1109/fmcad.2014.6987613
    title: Andrew Reynolds, Cesare Tinelli and Leonardo de Moura, Finding conflicting instances of quantified formulas in SMT, FMCAD 2014, pages 195 to 202
    locator: conflict-based instantiation, which searches for instances that are false in the current e-graph
  - paper: doi:10.1145/3498696
    title: Yihong Zhang, Yisu Remy Wang, Max Willsey and Zachary Tatlock, Relational e-matching, Proceedings of the ACM on Programming Languages 6 (POPL), 2022, pages 1 to 22
    locator: E-matching as a conjunctive query over the relations of an e-graph, for equality saturation
---

E-matching finds the instances of a pattern in an [e-graph](/e-graph/). The pattern is a term with variables, such as $g(f(x))$. The e-graph holds ground terms in equivalence classes, closed under the ground equalities that a solver knows. A *match* is an assignment of classes to the variables that makes the pattern equal to some term of the e-graph *modulo these equalities*. If the e-graph knows $f(a) = b$ and contains $g(b)$, then $g(f(x))$ matches $g(b)$ with $x = a$, although $g(b)$ has no $f$ in it. SMT solvers use E-matching to instantiate universally quantified formulas: the patterns are the *triggers* of a formula $\forall x.\, \varphi$, and each match $x \mapsto t$ gives the instance $\varphi[x/t]$. The matching itself is exact: the algorithm finds every match. But instantiation by E-matching is a heuristic. It only uses terms that are already in the e-graph and that fit a trigger, so it can miss the instances that a proof needs, and it can loop. E-matching came from the Simplify prover, and de Moura and Bjørner made it efficient in Z3.

## In plain words

You have a rule that holds for every x, for example "g of f of x equals x". You want to use it only where it can help, on terms that already appear in the problem.

So you write a shape, "g of f of something", and look through the known terms for that shape. The search does not only compare letters. It knows which terms are equal. If you know "f of a is b" and you see "g of b", that is "g of f of a" in disguise, so the shape fits with "something" equal to a.

Every fit gives one copy of the rule with x filled in, and the solver adds this copy to the problem. Shapes that fit nothing give nothing. That is why a badly chosen shape can make the solver miss a proof.

## The problem

**Input.** An e-graph $G$ for a set $E$ of ground equations: the terms of $G$ are closed under subterms, and its classes are the classes of the congruence closure of $E$. A *pattern* $p$: a term built from function symbols, constants and variables.

**Output.** All substitutions $\sigma$ from the variables of $p$ to classes of $G$, together with a class $c$, such that $E \models p\sigma = t$ for the terms $t$ of $c$. Here $p\sigma$ replaces each variable by any term of its class; the choice does not matter.

A *multi-pattern* is a list of patterns $p_1, \ldots, p_k$ with shared variables. A match is one substitution that matches all of them, each in some class. SMT-LIB writes patterns with the `:pattern` attribute on the body of a quantified formula. A formula can have several `:pattern` attributes, each with one or more terms. The standard says that patterns "provide heuristic information to SMT solvers that reason about quantified formulas by quantifier instantiation" (Section 3.6.5). This example from the standard gives transitivity a multi-pattern:

```
(forall ((x0 A) (x1 A) (x2 A))
  (! (=> (and (r x0 x1) (r x1 x2)) (r x0 x2))
     :pattern ((r x0 x1) (r x1 x2))
     :pattern ((p x0 a))))
```

## The algorithm

The matcher walks down the pattern and the e-graph together. At a function symbol of the pattern, it tries every node with the same symbol in the current class, and matches the arguments in their classes. At a variable, it binds the variable to the class, or checks that an earlier binding is the same class. All equality reasoning is in the e-graph: two terms are equal exactly when they are in the same class.

```pseudo id=main
EMATCH(p, c, σ)                    ▷ all extensions of σ that put p in class c
L1  if p is a variable x:
L2      if σ does not bind x: return {σ ∪ {x ↦ c}}
L3      if find(σ(x)) = find(c): return {σ}; else return ∅
L4  R ← ∅                          ▷ here p = f(p1, ..., pn), with n ≥ 0
L5  for each node f(c1, ..., cn) of class c with the same symbol and arity as p:
L6      Σ ← {σ}
L7      for i ← 1 to n: Σ ← the union of EMATCH(pi, ci, τ) over all τ ∈ Σ
L8      R ← R ∪ Σ
L9  return R

MATCH-ALL(p, G)
L10 return the union of EMATCH(p, c, ∅) over all classes c of G
```

A constant is a function symbol with no arguments, so it matches a class exactly when the class contains it. For a multi-pattern, match $p_1$, then match $p_2$ starting from each substitution found, and so on.

**Instantiation.** A solver runs E-matching in rounds. For each quantified formula $\forall \bar x.\, \varphi$ that is asserted, and each of its triggers, it finds the matches, makes the instances $\varphi[\bar x / \bar t]$ that it has not made before, and adds them to the ground problem. The new terms go into the e-graph, and the next round can match them.

## Example

**A match modulo an equality.** Let $E = \{f(a) = b\}$ and let the e-graph contain $g(b)$. The classes are $\{a\}$, $\{b, f(a)\}$ and $\{g(b)\}$. Match the pattern $g(f(x))$.

| call | pattern | class | what happens |
|---|---|---|---|
| 1 | $g(f(x))$ | $\{g(b)\}$ | the node $g(\{b, f(a)\})$ has symbol $g$; match its argument (L5 to L7) |
| 2 | $f(x)$ | $\{b, f(a)\}$ | the node $b$ has the wrong symbol; the node $f(\{a\})$ fits; match its argument |
| 3 | $x$ | $\{a\}$ | $x$ is not bound: return $\{x \mapsto \{a\}\}$ (L2) |

The only match is $x \mapsto a$ in the class of $g(b)$. Matching on syntax alone finds nothing. With the axiom $\forall x.\, g(f(x)) = x$ and this trigger, the instance is $g(f(a)) = a$, and the solver learns $g(b) = a$.

**A bad trigger makes instantiation incomplete.** The ground facts $g(a) = g(b)$ and $a \ne b$, with the axiom $\forall x.\, f(g(x)) = x$, are unsatisfiable: the instances for $a$ and $b$ give $a = f(g(a)) = f(g(b)) = b$. With the trigger $f(g(x))$, the e-graph has no $f$ at all, E-matching finds nothing, and the solver can only say "unknown". With the trigger $g(x)$, the matches $x \mapsto a$ and $x \mapsto b$ give the two instances, and congruence closure finds the conflict. The implementation checks both runs.

**A matching loop.** The axiom $\forall x.\, f(x) = f(g(x))$ with the trigger $f(x)$ matches $f(a)$, and the instance adds the new term $f(g(a))$. This term matches the trigger again, and the next instance adds $f(g(g(a)))$. Each round makes one new instance, and instantiation never stops by itself. With the trigger $f(g(x))$ there is no match on $f(a)$, and no loop.

## Correctness

The [proof page](proofs/correctness.md) proves that EMATCH returns exactly the matches, each once, when the e-graph is closed under congruence.

- **Where a new term lands.** A ground term $s$ that is not in the e-graph is equal to a term of class $c$ exactly when, bottom-up, each subterm of $s$ finds a node with its symbol and the classes of its arguments, and the top node is in $c$. This is the key lemma: adding $s$ to the e-graph cannot merge old classes, and $s$ joins an old class only by congruence with an old node.
- **The induction.** By induction on the pattern, line L2 and line L3 handle variables exactly, and lines L5 to L8 collect the matches that go through each node of the class. A match fixes the classes of the arguments, so it goes through exactly one node, and it is found once.

**Tests.** The tests compare MATCH-ALL with a brute force on 376 random e-graphs and patterns, of which 262 had ground equations. The brute force tries every assignment of classes to the variables, builds the ground term $p\sigma$, and decides $E \models p\sigma = t$ with a naive congruence closure computed from scratch over all subterms. It shares no code with the matcher. The two agreed on all cases; 130 had at least one match, and 52 had several. The tests also check the examples above, a pattern with a repeated variable, and the reduction from 3-coloring below.

## Complexity

Let $m$ be the size of the pattern and $n$ the number of nodes of the e-graph. Each function symbol of the pattern chooses one node at line L5, so a run follows at most $n + n^2 + \cdots + n^m$ sequences of choices, each for $O(m)$ steps. The time is $O(m\, n^m)$, counting a union-find operation as one step. The output can be that large. If one class holds the $n$ nodes $f(c_1), \ldots, f(c_n)$ and the e-graph contains $h(f(c_1), \ldots, f(c_1))$, the pattern $h(f(x_1), \ldots, f(x_k))$ has $n^k$ matches.

Deciding whether a pattern has a match at all is NP-complete. It is in NP: guess a node for each function symbol of the pattern and check the choices. It is NP-hard even without equations, by a reduction from graph 3-coloring. Let the e-graph contain the six terms $e(c, d)$ for distinct colors $c, d \in \{r, g, b\}$. For a graph, take the multi-pattern with one pattern $e(x_u, x_v)$ for each edge $uv$. A match assigns a color to each vertex with different colors on each edge, so it exists exactly when the graph is 3-colorable. To get a single pattern, merge the six terms into one class with ground equations, and match $h(e(x_{u_1}, x_{v_1}), \ldots, e(x_{u_k}, x_{v_k}))$ against a term $h(e(r, g), \ldots, e(r, g))$. The implementation checks the triangle (6 matches) and the complete graph on four vertices (none).

The space is the size of the output plus the recursion stack, $O(m\, n^m)$ in the worst case.

## Properties

- **Exact for the matching problem.** Every match is found, once, if the e-graph is closed under congruence.
- **Uses only known terms.** Each variable is bound to a class that already exists. E-matching never invents a term.
- **Heuristic for instantiation.** The set of instances depends on the triggers. Instantiation by E-matching is incomplete, and it can loop.
- **Incremental.** After new terms or merges, only the matches that use them are new. Efficient matchers look only for these.

## Variants and improvements

- **Code trees and an abstract machine.** De Moura and Bjørner compile each pattern into code for an abstract machine, and share the code of similar patterns in a code tree. They also find the matches that are new after a merge without matching everything again.
- **Multi-patterns.** A trigger can be a list of patterns with shared variables, as in the transitivity example. Simplify called these multi-triggers.
- **Automatic triggers.** When the user gives no pattern, solvers choose triggers themselves, usually the smallest subterms of the body that contain all the bound variables. Simplify did this, and it also avoided triggers that it saw would loop.
- **Relational E-matching.** Zhang, Wang, Willsey and Tatlock (2022) see an e-graph as a database of relations, one per function symbol, and a pattern as a conjunctive query. Join algorithms then give worst-case optimal bounds for E-matching in equality saturation tools such as egg.
- **Other instantiation methods.** Conflict-based instantiation (Reynolds, Tinelli and de Moura, 2014) looks only for instances that are false in the current e-graph. Model-based instantiation (Ge and de Moura, 2009) checks the quantified formulas against a candidate model. Enumerative instantiation tries terms in a fixed order. See [quantifier instantiation](/quantifier-instantiation/).

## When to use it

Use E-matching when a problem has many universally quantified axioms but only a few instances matter, as in program verification with Boogie, Dafny or F*, where the axioms describe heaps, sequences or user functions. Write triggers that contain all the bound variables and that appear in the ground terms that the proofs need. Use model-based or enumerative instantiation when the formula is in a fragment where those methods are complete, or when the goal is to show satisfiability, which E-matching cannot do on its own. Use E-matching also to apply rewrite rules in an e-graph, as in equality saturation.

## Pitfalls

- **Expecting completeness.** A solver that only uses E-matching can answer "unknown" on an unsatisfiable formula, as the bad-trigger example shows. The Handbook notes that the most effective instantiation techniques "are incomplete and heuristic" (Section 33.7.2).
- **Matching loops.** A trigger that matches a term created by its own instances, such as $f(x)$ for $\forall x.\, f(x) = f(g(x))$, makes an unbounded chain of instances. Solvers limit the depth of instances, but the time is lost.
- **Triggers that miss variables.** A trigger must contain every bound variable, or the match leaves some variables without a value.
- **Triggers under interpreted symbols.** A trigger such as $f(x + 1)$ needs matching modulo arithmetic. Most matchers treat $+$ as an uninterpreted symbol, so the trigger does not match $f(a)$ even when the solver knows $a = b + 1$ for some $b$.
- **Too many matches.** A trigger with several variables and a common symbol can have a number of matches that grows like $n^k$. Each match is an instance, and the instances flood the solver.

## Implementations

## History

Greg Nelson's work on the Stanford Pascal Verifier and on cooperating decision procedures around 1980 used matching against an equality graph to instantiate quantifiers. The prover Simplify, by Detlefs, Nelson and Saxe, made this its central method, with triggers, multi-triggers and automatic trigger selection; its full description appeared in the Journal of the ACM in 2005. Simplify was the prover of ESC/Java, and its approach to quantifiers was taken over by the SMT solvers that replaced it. In 2007 de Moura and Bjørner gave the efficient matching of Z3, with code trees and incremental matching. SMT-LIB 2 standardized the `:pattern` attribute. Later work added conflict-based and model-based instantiation for SMT, and relational E-matching for equality saturation.

## References
