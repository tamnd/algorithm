---
tag: KJGF11
kind: definition
slug: abstract-domain
name: Abstract domain
aliases:
- abstract lattice
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: core
summary: A lattice of abstract properties with a concretization map and sound abstract versions of the program operations, join and widening.
prereqs: [collecting-semantics, join-semilattice]
see_also: [abstract-interpretation, galois-connection, interval-domain, octagon-domain, polyhedra-domain, reduced-product, widening-operator, constant-propagation-problem]
sources:
  - paper: doi:10.1145/512950.512973
    title: "Patrick Cousot and Radhia Cousot, Abstract interpretation: a unified lattice model for static analysis of programs by construction or approximation of fixpoints, POPL 1977, pages 238 to 252"
    locator: the definition of an abstract interpretation as a lattice of abstract contexts with abstract operations, its consistency with the static semantics, and the widening for lattices with infinite ascending chains
  - paper: doi:10.1093/logcom/2.4.511
    title: "Patrick Cousot and Radhia Cousot, Abstract interpretation frameworks, Journal of Logic and Computation 2(4), 1992, pages 511 to 547"
    locator: the frameworks that use a concretization function only, with no best abstraction, and their comparison with the Galois connection framework
  - paper: doi:10.1145/567752.567778
    title: "Patrick Cousot and Radhia Cousot, Systematic design of program analysis frameworks, POPL 1979, pages 269 to 282"
    locator: the design of abstract domains and of their combinations from the concrete semantics
  - book: isbn:9780262043410
    title: Xavier Rival and Kwangkeun Yi, Introduction to Static Analysis, An Abstract Interpretation Perspective, MIT Press, 2020
    locator: Chapter 3 (abstract domains for sets of states, the non-relational and relational domains, and the soundness of the abstract operations)
  - book: isbn:9783540654100
    title: Flemming Nielson, Hanne Riis Nielson and Chris Hankin, Principles of Program Analysis, Springer, 1999
    locator: Chapter 4 (Abstract Interpretation), the property spaces and the correctness relations
---

An abstract domain is a set of machine-readable descriptions of sets of program states, together with the operations that an analyzer needs on them: an order, a join, sound versions of the program instructions, and a widening. Each description $a$ has a meaning $\gamma(a)$, the set of states it allows. The domain fixes what an analysis can say. The interval domain can say $0 \le i \le 10$ and cannot say $i \le n$; the polyhedra domain can say both, at a higher cost.

## Definition

The concrete side is the [collecting semantics](/collecting-semantics/): for each program point, a set of environments, ordered by inclusion. This page uses the Cousot order: lower is more precise, and $\bot$ describes the empty set of states. The dataflow pages, such as [monotone dataflow framework](/monotone-dataflow-framework/), use the dual order of Kildall, where the meet combines paths and the top element means "unreachable".

An **abstract domain** for the set $\mathit{Env}$ of environments is a tuple $(A, \sqsubseteq, \bot, \top, \sqcup, \gamma, \mathit{assign}^\sharp, \mathit{guard}^\sharp, \nabla)$ with these parts and conditions.

1. **Elements and order.** $A$ is a set with a preorder $\sqsubseteq$, and a program can decide $a \sqsubseteq b$. Often $(A, \sqsubseteq)$ is a lattice, but it need not be complete, and two representations of the same set may be equivalent without being equal.
2. **Concretization.** $\gamma : A \to \mathcal{P}(\mathit{Env})$ is monotone: $a \sqsubseteq b$ implies $\gamma(a) \subseteq \gamma(b)$.
3. **Extremes.** $\gamma(\bot) = \emptyset$ and $\gamma(\top) = \mathit{Env}$.
4. **Join.** $a \sqcup b$ is an upper bound of $a$ and $b$ that a program can compute. It is sound: $\gamma(a) \cup \gamma(b) \subseteq \gamma(a \sqcup b)$. It need not be the least upper bound, and $\gamma(a \sqcup b)$ is often larger than the union.
5. **Transfer functions.** For each instruction $x = e$ there is $\mathit{assign}^\sharp(x, e) : A \to A$, and for each branch condition $c$ there is $\mathit{guard}^\sharp(c) : A \to A$. Each one is sound: for every $a$,
$$ \mathit{post}_{x = e}\bigl(\gamma(a)\bigr) \subseteq \gamma\bigl(\mathit{assign}^\sharp(x, e)(a)\bigr), \qquad \{ \rho \in \gamma(a) : c \text{ holds in } \rho \} \subseteq \gamma\bigl(\mathit{guard}^\sharp(c)(a)\bigr). $$
6. **Widening.** If $A$ has an infinite strictly ascending chain, a [widening operator](/widening-operator/) $\nabla$ is part of the domain. Without it the iteration may not stop.

These parts are optional: a meet $\sqcap$ with $\gamma(a) \cap \gamma(b) \subseteq \gamma(a \sqcap b)$, a [narrowing operator](/narrowing-operator/), and an abstraction $\alpha : \mathcal{P}(\mathit{Env}) \to A$ that gives the best description of each set. When $\alpha$ exists and $\alpha(S) \sqsubseteq a \iff S \subseteq \gamma(a)$, the pair is a [Galois connection](/galois-connection/). The definition does not require it: the [polyhedra domain](/polyhedra-domain/) has no best description of a disk.

**From local conditions to a sound result.** For an edge $\ell \to \ell'$, let $\mathit{post}^\sharp_{\ell \to \ell'}$ be the composition of the transfer functions of the instructions of $\ell$, followed by $\mathit{guard}^\sharp$ of the branch condition that selects $\ell'$ (or of its negation). Let $\mathit{init}^\sharp$ satisfy $\mathit{Init} \subseteq \gamma(\mathit{init}^\sharp)$. Define $F^\sharp$ on maps $A^{\mathit{Labels}}$ in the same shape as the concrete $F$:

$$ F^\sharp(X)(\ell) = [\ell = \mathit{entry}]\,\mathit{init}^\sharp \ \sqcup \bigsqcup_{\ell' \to \ell} \mathit{post}^\sharp_{\ell' \to \ell}\bigl(X(\ell')\bigr). $$

*Claim.* For every $X$, $F(\gamma \circ X) \subseteq \gamma \circ F^\sharp(X)$ pointwise.

*Proof.* First, a composition of sound steps is sound. If $\mathit{post}_{s_1}(\gamma(a)) \subseteq \gamma(s_1^\sharp(a))$ and the same holds for $s_2$, then, since the concrete $\mathit{post}_{s_2}$ is monotone,

$$ \mathit{post}_{s_2}\bigl(\mathit{post}_{s_1}(\gamma(a))\bigr) \subseteq \mathit{post}_{s_2}\bigl(\gamma(s_1^\sharp(a))\bigr) \subseteq \gamma\bigl(s_2^\sharp(s_1^\sharp(a))\bigr). $$

By induction on the length of the block, $\mathit{post}_{\ell' \to \ell}(\gamma(X(\ell'))) \subseteq \gamma(\mathit{post}^\sharp_{\ell' \to \ell}(X(\ell')))$. Second, a join of sound terms is sound. If $S_i \subseteq \gamma(b_i)$ for each $i$, then $\bigcup_i S_i \subseteq \bigcup_i \gamma(b_i) \subseteq \gamma(\bigsqcup_i b_i)$, by condition 4 and induction on the number of terms. The entry term is covered by $\mathit{Init} \subseteq \gamma(\mathit{init}^\sharp)$. Put the two parts together at each $\ell$. $\square$

*Consequence.* If $F^\sharp(X) \sqsubseteq X$ pointwise, then $F(\gamma \circ X) \subseteq \gamma \circ F^\sharp(X) \subseteq \gamma \circ X$, by the claim and condition 2. So $\gamma \circ X$ is an element $S$ with $F(S) \subseteq S$, and the least fixed point is below it: $\mathit{Coll} \subseteq \gamma \circ X$. The [abstract interpretation](/abstract-interpretation/) page gives this last step as its soundness theorem; Knaster-Tarski calls such an $S$ a pre-fixed point, and Cousot calls the abstract $X$ with $F^\sharp(X) \sqsubseteq X$ a post-fixed point. Two points matter in practice. The proof does not use the monotonicity of $F^\sharp$, so a non-monotone transfer function or a widening does not break soundness. And a map $X$ with $F^\sharp(X) \sqsubseteq X$ is a certificate: to check it, a program evaluates $F^\sharp$ once and tests $\sqsubseteq$ at each point.

**Non-relational and relational domains.** A *non-relational* domain keeps one value description per name. It is built from a value domain $(B, \sqsubseteq_B, \gamma_B)$ that describes sets of integers: $A = (V \to B) \cup \{\bot\}$, with the pointwise order and

$$ \gamma(m) = \{ \rho : \rho(x) \in \gamma_B(m(x)) \text{ for each } x \in V \}. $$

A map in which one name has the empty description describes no state, so it is identified with $\bot$. A *relational* domain describes sets of tuples directly, and it can keep a relation between names, such as $x \le y$ or $x + y = 10$.

## Examples and non-examples

**Parity.** The value domain has four elements, $\bot \sqsubseteq \mathit{even}, \mathit{odd} \sqsubseteq \top$, with $\gamma_B(\mathit{even})$ the even integers and $\gamma_B(\mathit{odd})$ the odd ones. Its sum gives $\mathit{even}$ when both arguments are equal and not $\top$, and $\mathit{odd}$ when they differ; its product gives $\mathit{even}$ when one argument is $\mathit{even}$ and $\mathit{odd}$ when both are $\mathit{odd}$. Both are the best transformers: a check over all argument pairs gives exactly these results. Analyze this program with the parameter `n`:

```
entry:
  x = 1
  jump head
head:
  t = x < n
  br t body exit
body:
  x = x + 2
  jump head
exit:
  y = x * x
  ret y
```

At head the first pass gives $x \mapsto \mathit{odd}$ from the entry edge, and the body edge gives $\mathit{odd} + \mathit{even} = \mathit{odd}$, so the second pass changes nothing. The domain has finite height, so no widening is needed. At exit $y = \mathit{odd} \cdot \mathit{odd} = \mathit{odd}$: the program always returns an odd number. The guard `x < n` gives no parity information, so its transfer function is the identity.

**A table of common domains.** All of these are domains in the sense above. The height is that of the value lattice of one name, and $v$ is the number of names.

| domain | kind | height | example fact | cost of one operation |
|---|---|---|---|---|
| sign | non-relational | 2 | $x > 0$ | $O(v)$ |
| parity | non-relational | 2 | $x$ odd | $O(v)$ |
| constants ([constant propagation](/constant-propagation-problem/)) | non-relational | 2 | $x = 7$ | $O(v)$ |
| [intervals](/interval-domain/) | non-relational | infinite | $0 \le x \le 10$ | $O(v)$ |
| [octagons](/octagon-domain/) | relational, weakly | infinite | $x - y \le 3$, $x + y \le 10$ | $O(v^3)$ for closure |
| [convex polyhedra](/polyhedra-domain/) | relational | infinite | $y = 2x$, $x + y + z \le 9$ | exponential in $v$ in the worst case |

The constant lattice has height 2 but infinite width, so its iteration still stops. The interval, octagon and polyhedra domains need a widening.

**Non-relational loses relations.** Two runs reach a point with $(x, y) = (1, 2)$ and $(2, 1)$. Intervals give $x \in [1, 2]$ and $y \in [1, 2]$, which also allows $(1, 1)$, so they cannot prove $x + y = 3$. Octagons keep $x + y = 3$ exactly.

**Non-example: an unsound transfer function.** Take the sign domain and define $\mathit{pos} - \mathit{pos} = \mathit{pos}$. Then $\gamma(\mathit{pos})$ contains 1 and 2, and $1 - 2 = -1$ is not in $\gamma(\mathit{pos})$. Condition 5 fails, and an analysis with this rule can prove that `y = x - z` is positive when it is not. The sound rule gives $\top$.

**Non-example: an order that does not follow the meaning.** Order intervals by their width: $[0, 0] \sqsubseteq [5, 6]$ because $0 \le 1$. Then $\gamma([0, 0]) = \{0\}$ is not inside $\gamma([5, 6]) = \{5, 6\}$, so $\gamma$ is not monotone and condition 2 fails. A test $F^\sharp(X) \sqsubseteq X$ in this order proves nothing about the program.

**Non-example: a join that is too small.** Use the intersection of intervals as the join. Then $[0, 1] \sqcup [5, 6] = \bot$, and the point after an `if` with these two branches would look unreachable. Condition 4 fails. Any computable upper bound is acceptable, but a lower bound is not.

## Related definitions

- [Collecting semantics](/collecting-semantics/): the concrete meaning that the domain approximates, and the target of the soundness claim.
- [Galois connection](/galois-connection/): the extra structure when each set of states has a best description; it gives the best transfer function $\alpha \circ f \circ \gamma$.
- [Widening operator](/widening-operator/) and [narrowing operator](/narrowing-operator/): the operators that make the iteration stop on domains of infinite height, and then recover precision.
- [Interval domain](/interval-domain/), [octagon domain](/octagon-domain/) and [polyhedra domain](/polyhedra-domain/): three numeric domains, in order of growing precision and cost.
- [Reduced product](/reduced-product/): a way to combine two domains, with a reduction that passes facts from one to the other.
- [Join-semilattice](/join-semilattice/): the order structure that most domains have.
- [Abstract interpretation](/abstract-interpretation/): the general technique that runs a program over an abstract domain.
- [Predicate abstraction](/predicate-abstraction/) and [three-valued logic shape analysis](/three-valued-logic-shape-analysis/): domains whose elements are formulas over chosen predicates, and logical structures for the heap.

## References
