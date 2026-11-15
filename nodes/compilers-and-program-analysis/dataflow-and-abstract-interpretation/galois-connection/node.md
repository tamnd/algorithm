---
tag: 733ZE7
kind: definition
slug: galois-connection
name: Galois connection
aliases:
- adjunction between posets
- Galois insertion
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: core
summary: A pair of monotone maps alpha and gamma between concrete and abstract posets with alpha(x) <= y exactly when x <= gamma(y).
prereqs: [abstract-domain, knaster-tarski-theorem]
see_also: [abstract-interpretation, collecting-semantics, interval-domain, polyhedra-domain, reduced-product, join-semilattice, fixed-point]
sources:
  - paper: doi:10.1145/567752.567778
    title: "Patrick Cousot and Radhia Cousot, Systematic design of program analysis frameworks, POPL 1979, pages 269 to 282"
    locator: the Galois connection between the concrete and the abstract lattice, the best approximation of the concrete operations, and the design of analyses from it
  - paper: doi:10.1145/512950.512973
    title: "Patrick Cousot and Radhia Cousot, Abstract interpretation: a unified lattice model for static analysis of programs by construction or approximation of fixpoints, POPL 1977, pages 238 to 252"
    locator: the abstraction and concretization functions that relate an abstract interpretation to the static semantics
  - paper: doi:10.1093/logcom/2.4.511
    title: "Patrick Cousot and Radhia Cousot, Abstract interpretation frameworks, Journal of Logic and Computation 2(4), 1992, pages 511 to 547"
    locator: the comparison of the framework with a Galois connection and the frameworks with a concretization function only
  - book: isbn:9780521784511
    title: B. A. Davey and H. A. Priestley, Introduction to Lattices and Order, second edition, Cambridge University Press, 2002
    locator: Chapter 7 (Complete lattices and Galois connections), the section on Galois connections
  - book: isbn:9783540654100
    title: Flemming Nielson, Hanne Riis Nielson and Chris Hankin, Principles of Program Analysis, Springer, 1999
    locator: Chapter 4 (Abstract Interpretation), the sections on Galois connections, Galois insertions and induced operations
---

A Galois connection is a pair of monotone maps between a concrete ordered set and an abstract one: the abstraction $\alpha$ maps a set of states to its best description, and the concretization $\gamma$ maps a description to the set of states it allows. The two are tied by one equivalence, $\alpha(c) \sqsubseteq a \iff c \le \gamma(a)$. From it come the best abstract version of each concrete operation and the transfer of fixed points from the concrete side to the abstract one.

## Definition

Let $(C, \le)$ and $(A, \sqsubseteq)$ be partially ordered sets. In program analysis $C$ is $\mathcal{P}(\mathit{Env})$ ordered by inclusion, as in the [collecting semantics](/collecting-semantics/), and $A$ is an [abstract domain](/abstract-domain/). The orders are the Cousot orders: lower is more precise. A pair of maps $\alpha : C \to A$ and $\gamma : A \to C$ is a **Galois connection** when, for all $c \in C$ and $a \in A$,

$$ \alpha(c) \sqsubseteq a \iff c \le \gamma(a). $$

In words, $a$ describes $c$ soundly in the abstract order exactly when $c$ is inside the meaning of $a$ in the concrete order. The notation is $(C, \le) \underset{\alpha}{\overset{\gamma}{\leftrightarrows}} (A, \sqsubseteq)$.

**Theorem 1 (four conditions).** $(\alpha, \gamma)$ is a Galois connection if and only if

1. $\alpha$ is monotone,
2. $\gamma$ is monotone,
3. $\alpha(\gamma(a)) \sqsubseteq a$ for every $a$, and
4. $c \le \gamma(\alpha(c))$ for every $c$.

*Proof.* Assume the equivalence. For condition 4, put $a = \alpha(c)$: since $\alpha(c) \sqsubseteq \alpha(c)$, we get $c \le \gamma(\alpha(c))$. For condition 3, put $c = \gamma(a)$: since $\gamma(a) \le \gamma(a)$, we get $\alpha(\gamma(a)) \sqsubseteq a$. For condition 1, let $c \le c'$. By condition 4, $c \le c' \le \gamma(\alpha(c'))$, and the equivalence turns this into $\alpha(c) \sqsubseteq \alpha(c')$. For condition 2, let $a \sqsubseteq a'$. By condition 3, $\alpha(\gamma(a)) \sqsubseteq a \sqsubseteq a'$, and the equivalence turns this into $\gamma(a) \le \gamma(a')$.

Now assume the four conditions. If $\alpha(c) \sqsubseteq a$, then $c \le \gamma(\alpha(c)) \le \gamma(a)$ by condition 4 and condition 2. If $c \le \gamma(a)$, then $\alpha(c) \sqsubseteq \alpha(\gamma(a)) \sqsubseteq a$ by condition 1 and condition 3. $\square$

**Theorem 2 (each map determines the other).** In a Galois connection,

$$ \gamma(a) = \max\{ c \in C : \alpha(c) \sqsubseteq a \}, \qquad \alpha(c) = \min\{ a \in A : c \le \gamma(a) \}. $$

So if $(\alpha, \gamma_1)$ and $(\alpha, \gamma_2)$ are both Galois connections, then $\gamma_1 = \gamma_2$, and the same holds for $\alpha$.

*Proof.* By condition 3, $\gamma(a)$ is in the set $\{ c : \alpha(c) \sqsubseteq a \}$. By the equivalence, each $c$ in the set has $c \le \gamma(a)$. So $\gamma(a)$ is the greatest element of the set. The formula for $\alpha$ is the dual argument with condition 4. A greatest element is unique, so $\gamma$ depends only on $\alpha$. $\square$

**Theorem 3 (joins and meets).** $\alpha$ preserves every join that exists in $C$, and $\gamma$ preserves every meet that exists in $A$. In particular $\alpha(\bot_C) = \bot_A$ when $\bot_C$ exists.

*Proof.* Let $S \subseteq C$ have a join $\bigvee S$. For every $a$,

$$ \alpha\Bigl(\bigvee S\Bigr) \sqsubseteq a \iff \bigvee S \le \gamma(a) \iff \forall s \in S : s \le \gamma(a) \iff \forall s \in S : \alpha(s) \sqsubseteq a. $$

So the upper bounds of $\alpha(S)$ are exactly the elements above $\alpha(\bigvee S)$, and $\alpha(\bigvee S)$ is the join of $\alpha(S)$. The case of $\gamma$ is dual. For $S = \emptyset$ the join is $\bot_C$, and the claim gives $\alpha(\bot_C) = \bot_A$. $\square$

The converse holds for complete lattices: if $\alpha$ preserves all joins, then $\gamma(a) = \bigvee \{ c : \alpha(c) \sqsubseteq a \}$ makes a Galois connection. Indeed $\alpha(c) \sqsubseteq a$ puts $c$ in the set, so $c \le \gamma(a)$; and if $c \le \gamma(a)$, then $\alpha(c) \sqsubseteq \alpha(\gamma(a)) = \bigsqcup \{ \alpha(c') : \alpha(c') \sqsubseteq a \} \sqsubseteq a$. So to give a Galois connection between complete lattices, it is enough to give an $\alpha$ that preserves joins.

**Closure.** From conditions 1, 3 and 4, $\alpha \circ \gamma \circ \alpha = \alpha$: the inequality $\alpha \sqsubseteq \alpha \gamma \alpha$ is condition 4 under the monotone $\alpha$, and $\alpha \gamma (\alpha(c)) \sqsubseteq \alpha(c)$ is condition 3. Dually $\gamma \circ \alpha \circ \gamma = \gamma$. So $\gamma \circ \alpha$ is an upper closure on $C$: monotone, extensive ($c \le \gamma\alpha(c)$) and idempotent. It maps each set of states to the smallest set that the domain can express.

**Galois insertion.** A Galois connection is a *Galois insertion* when $\alpha \circ \gamma = \mathrm{id}_A$, the special case where condition 3 holds with equality. These are equivalent:

1. $\alpha \circ \gamma = \mathrm{id}_A$;
2. $\alpha$ is onto;
3. $\gamma$ is one to one.

*Proof.* From 1, each $a$ equals $\alpha(\gamma(a))$, so $\alpha$ is onto; and $\gamma(a) = \gamma(b)$ gives $a = \alpha\gamma(a) = \alpha\gamma(b) = b$. From 2, write $a = \alpha(c)$; then $\alpha\gamma(a) = \alpha\gamma\alpha(c) = \alpha(c) = a$. From 3, $\gamma(\alpha\gamma(a)) = \gamma(a)$ by the closure identity, so $\alpha\gamma(a) = a$. $\square$

In an insertion no two abstract elements have the same meaning, so the domain has no redundant elements. Every Galois connection gives an insertion when $A$ is cut down to the image of $\alpha$; this keeps one element for each meaning.

**The best transformer.** Let $f : C \to C$ be monotone, for example the concrete $\mathit{post}$ of an instruction. Call $g : A \to A$ sound for $f$ when $f \circ \gamma \le \gamma \circ g$ pointwise. Then:

- $\alpha \circ f \circ \gamma$ is sound: $f(\gamma(a)) \le \gamma(\alpha(f(\gamma(a))))$ by condition 4.
- It is the most precise sound map: for each $a$, $\alpha(f(\gamma(a))) \sqsubseteq g(a)$ if and only if $f(\gamma(a)) \le \gamma(g(a))$, by the equivalence. So $g$ is sound exactly when $\alpha \circ f \circ \gamma \sqsubseteq g$.
- If $g$ is monotone, soundness is the same as $\alpha \circ f \sqsubseteq g \circ \alpha$. From $\alpha f \sqsubseteq g \alpha$: $\alpha f \gamma \sqsubseteq g \alpha \gamma \sqsubseteq g$ by condition 3 and the monotone $g$. From $\alpha f \gamma \sqsubseteq g$: $\alpha f \sqsubseteq \alpha f \gamma \alpha \sqsubseteq g \alpha$ by condition 4 and the monotone $\alpha f$.

The best transformer is a specification. It may not be computable in a closed form, and a real domain often uses a sound map that is less precise but faster.

**Theorem 4 (fixed point transfer).** Let $C$ and $A$ be complete lattices, and let $f : C \to C$ and $g : A \to A$ be monotone with $\alpha \circ f \sqsubseteq g \circ \alpha$. Then

$$ \alpha(\mathrm{lfp}\, f) \sqsubseteq \mathrm{lfp}\, g, \qquad \text{equivalently} \qquad \mathrm{lfp}\, f \le \gamma(\mathrm{lfp}\, g). $$

If moreover $\alpha \circ f = g \circ \alpha$, then $\alpha(\mathrm{lfp}\, f) = \mathrm{lfp}\, g$.

*Proof.* Let $a = \mathrm{lfp}\, g$. By the last point above, $f(\gamma(a)) \le \gamma(g(a)) = \gamma(a)$. So $\gamma(a)$ is an element $x$ with $f(x) \le x$, and by the [Knaster-Tarski theorem](/knaster-tarski-theorem/) the least fixed point of $f$ is below it: $\mathrm{lfp}\, f \le \gamma(a)$. The equivalence gives $\alpha(\mathrm{lfp}\, f) \sqsubseteq a$. For the second claim, $g(\alpha(\mathrm{lfp}\, f)) = \alpha(f(\mathrm{lfp}\, f)) = \alpha(\mathrm{lfp}\, f)$, so $\alpha(\mathrm{lfp}\, f)$ is a fixed point of $g$, and $\mathrm{lfp}\, g$ is below it. $\square$

When $\alpha \circ f = g \circ \alpha$, the abstraction is called *complete* for $f$: the abstract least fixed point loses nothing beyond what $\alpha$ loses on the exact answer. This is rare. Most transfer functions give only the inequality, and a widening then gives an element above $\mathrm{lfp}\, g$, which is still sound.

**Order-reversing form.** Ore and the older algebra texts use a pair of order-reversing maps with $a \sqsubseteq \alpha(c) \iff c \le \gamma(a)$, as between sets of polynomials and sets of their roots. Reverse the order of $A$ to get the monotone form used here. The monotone form is also called an adjunction between posets, with $\alpha$ the lower adjoint and $\gamma$ the upper adjoint.

## Examples and non-examples

**Intervals.** Let $C = \mathcal{P}(\mathbb{Z})$ and let $A$ be the [interval domain](/interval-domain/) with bounds in $\mathbb{Z} \cup \{-\infty, +\infty\}$. Put $\gamma([l, u]) = \{ x : l \le x \le u \}$, $\gamma(\bot) = \emptyset$, $\alpha(\emptyset) = \bot$ and $\alpha(S) = [\inf S, \sup S]$ otherwise. Then $\alpha(S) \sqsubseteq [l, u]$ says $l \le \inf S$ and $\sup S \le u$, which says $S \subseteq \gamma([l, u])$. So this is a Galois connection. It is an insertion, because $\alpha$ is onto: $[l, u] = \alpha(\gamma([l, u]))$. For $S = \{1, 4, 9\}$, $\alpha(S) = [1, 9]$ and $\gamma(\alpha(S)) = \{1, \dots, 9\}$, which shows that condition 4 can be strict. The best transformer for $x \mapsto x \cdot x$ applied to $[-2, 3]$ is $\alpha(\{0, 1, 4, 9\}) = [0, 9]$, while the interval product of $[-2, 3]$ with itself gives $[-6, 9]$, because it does not know that both factors are the same number.

**A connection that is not an insertion.** Take two names and the plain product of two interval domains, without identifying the pairs that contain $\bot$. Then $\gamma(\bot, [0, 1]) = \emptyset = \gamma(\bot, \bot)$, so $\gamma$ is not one to one, and $\alpha(\gamma(\bot, [0, 1])) = (\bot, \bot) \ne (\bot, [0, 1])$. The pair is still a Galois connection: the four conditions hold. Identify every pair that has a $\bot$ component with one bottom element, and the result is an insertion. The [reduced product](/reduced-product/) does the same in general, with a reduction operator.

**Non-example: no best abstraction.** Let $C$ be the subsets of the real plane and $A$ the closed convex polyhedra, with $\gamma$ the inclusion, as in the [polyhedra domain](/polyhedra-domain/). The disk $D = \{ (x, y) : x^2 + y^2 \le 1 \}$ has no least polyhedron above it. Take any polyhedron $P \supseteq D$. The boundary of a polyhedron is made of finitely many line segments, and the boundary of $D$ is a circle, so $P \ne D$, and some point $p$ is in $P$ and not in $D$. The disk is closed and convex, so a line separates $p$ from $D$: there is a closed half-plane $H$ with $D \subseteq H$ and $p \notin H$. Then $P \cap H$ is a polyhedron above $D$ and strictly below $P$. So $\min\{ a : D \subseteq \gamma(a) \}$ does not exist, and by Theorem 2 no $\alpha$ makes a Galois connection with this $\gamma$. The domain is still usable: it only needs $\gamma$ and sound operations.

**Non-example: monotone maps that do not match.** On $C = \mathcal{P}(\mathbb{Z})$ and the interval domain, keep $\gamma$ and take $\alpha'(S) = \top$ for every nonempty $S$. Both maps are monotone and condition 4 holds, but $\alpha'(\gamma([0, 1])) = \top \not\sqsubseteq [0, 1]$, so condition 3 fails. Then $[0, 1]$ describes $\{0, 1\}$ soundly, but $\alpha'(\{0, 1\}) \sqsubseteq [0, 1]$ is false, and the equivalence breaks. By Theorem 2 the only $\alpha$ that works with this $\gamma$ is the one in the interval example.

## Related definitions

- [Abstract domain](/abstract-domain/): the abstract side; a domain needs $\gamma$ and sound operations, and a Galois connection is the extra structure that gives best descriptions.
- [Collecting semantics](/collecting-semantics/): the concrete side, $C = \mathcal{P}(\mathit{Env})$ at each point.
- [Abstract interpretation](/abstract-interpretation/): the general technique, which uses Theorem 4 to relate the abstract fixed point to the concrete one.
- [Knaster-Tarski theorem](/knaster-tarski-theorem/) and [fixed point](/fixed-point/): the facts about least fixed points that the transfer theorem uses.
- [Join-semilattice](/join-semilattice/): Theorem 3 says that $\alpha$ is a join homomorphism.
- [Reduced product](/reduced-product/): a product of two Galois connections, cut down to an insertion by a reduction.
- [Widening operator](/widening-operator/): the way to reach an element above $\mathrm{lfp}\, g$ when the abstract lattice has infinite chains.

## References
