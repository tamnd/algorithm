---
tag: ZQ6MP9
kind: concept
slug: subsumption
name: Clause subsumption
aliases:
- subsumption
- theta-subsumption
- θ-subsumption
- subsumption deletion
area: logic-and-constraints/unification-and-resolution
level: advanced
summary: A clause C subsumes D if some substitution maps C into a subset of D. Then C implies D, and provers delete D. Testing it is NP-complete; deletion keeps resolution complete.
prereqs: [substitution, clause, term-matching]
see_also: [robinson-resolution, set-of-support, ordered-resolution, factoring, term-indexing, term-matching, plotkin-lgg, three-coloring]
sources:
  - paper: doi:10.1145/321250.321253
    title: John Alan Robinson, A machine-oriented logic based on the resolution principle, Journal of the ACM 12(1), 1965
    locator: the subsumption principle, which allows a clause subsumed by another clause to be deleted without loss of completeness
  - book: isbn:9780121703509
    title: Chin-Liang Chang and Richard Char-Tung Lee, Symbolic Logic and Mechanical Theorem Proving, Academic Press, 1973
    locator: Chapter 5, The resolution principle (deletion strategy, with tautology deletion and subsumption, and its completeness)
  - book: isbn:9780444508133
    title: Alan Robinson and Andrei Voronkov (eds.), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Volume I, Chapter 2, Leo Bachmair and Harald Ganzinger, Resolution theorem proving (redundancy, and subsumption as a case of redundancy)
---

A [clause](/clause/) $C$ **subsumes** a clause $D$ if there is a [substitution](/substitution/) $\theta$ with $C\theta \subseteq D$; this relation is often called **θ-subsumption**. Then $C$ implies $D$, so a prover that keeps $C$ can delete $D$ without changing the models of its clause set, and deletion of subsumed clauses keeps unrestricted resolution and [set of support](/set-of-support/) complete. Deciding whether $C$ subsumes $D$ is NP-complete, although [term indexing](/term-indexing/) and backtracking [matching](/term-matching/) make it fast in practice. Subsumption is a syntactic test for one special case of implication, and it is weaker than implication.

## In plain words

Suppose a prover already knows "every bird can fly". Then a later fact "Tweety can fly or Tweety is red" adds nothing: it follows from the first fact by naming Tweety, and adding an extra option only makes a statement weaker. The prover may throw the later fact away.

This check is the main way that provers keep their memory small. Most new facts they produce are weaker copies of facts they already have. Checking that one fact is a stronger copy of another can be slow in bad cases, because the names must be chosen to fit many parts at once. In practice it is quick, and throwing weak facts away never stops the prover from finding a contradiction.

## The idea

**Definition.** Clauses are finite sets of literals. $C$ **subsumes** $D$, written $C \le_s D$, if $C\theta \subseteq D$ for some substitution $\theta$. Provers that keep factors use the stronger test with a length condition, $C\theta \subseteq D$ and $|C| \le |D|$, or **multiset subsumption**, where $\theta$ must map different literals of $C$ to different literals of $D$. The variables of $D$ are treated as constants: $\theta$ acts on $C$ only, so the test is one-sided [matching](/term-matching/), not unification.

**Soundness.** If $C\theta \subseteq D$, then $C \models D$. *Proof.* In a model of $C$, the instance $C\theta$ is true under every assignment, so some literal of $C\theta$ is true, and it is a literal of $D$. $\square$

**Not the same as implication.** $C = \lnot P(x) \vee P(f(x))$ implies $D = \lnot P(x) \vee P(f(f(x)))$, since $D$ is the resolvent of $C$ with a renamed copy of itself. But $C$ does not subsume $D$: $\theta$ must send $\lnot P(x)$ to $\lnot P(x)$, which forces $x\theta = x$, and then $P(f(x))$ is not in $D$.

**Theorem 1.** Deciding whether $C$ subsumes $D$ is NP-complete, with or without the length condition, and for multiset subsumption.

*Proof.* *In NP.* If $C\theta \subseteq D$, then for each variable $x$ of $C$, $x\theta$ is a subterm of $D$, so a certificate is a map from the variables of $C$ to subterms of $D$, of polynomial size. Checking $C\theta \subseteq D$, the length, and injectivity takes polynomial time.

*Hard.* Reduce [3-colouring](/three-coloring/), which is NP-complete. Let $G = (V, E)$ be a graph with $m$ edges, each written once as $uv$. Use a binary predicate $E$, a variable $x_u$ for each vertex, and constants $c_0, c_1, c_2$. Let

$$C_G = \{ E(x_u, x_v) : uv \in E \}, \qquad D = \{ E(c_i, c_j) : i, j \in \{0, 1, 2\}, i \ne j \}.$$

If $\chi$ is a proper 3-colouring, then $\theta = \{x_u \mapsto c_{\chi(u)}\}$ maps each $E(x_u, x_v)$ to $E(c_{\chi(u)}, c_{\chi(v)})$ with $\chi(u) \ne \chi(v)$, which is in $D$. Conversely, if $C_G\theta \subseteq D$, each $x_u$ of a vertex with an edge is sent to some $c_i$, and the colouring $u \mapsto i$, with any colour for isolated vertices, is proper, since $E(c_i, c_i) \notin D$. For the length condition, add to $D$ the $m$ literals $F(d_1), \ldots, F(d_m)$ with a new predicate $F$ and new constants; they match no literal of $C_G$, and now $|C_G| = m \le |D|$. For multiset subsumption, use a third argument: $C'_G = \{E(x_u, x_v, w_e) : e = uv \in E\}$ with a new variable $w_e$ per edge, and $D' = \{E(c_i, c_j, k_e) : i \ne j, e \in E\}$ with a new constant $k_e$ per edge. A proper colouring gives $\theta$ with $w_e \mapsto k_e$, which is injective because the $k_e$ differ, and any $\theta$ with $C'_G\theta \subseteq D'$ gives a colouring as before. All three constructions take polynomial time. $\square$

**Theorem 2 (deletion is safe, ground case).** Let $C \subseteq D$ be ground clauses. If $D$ is replaced by $C$ in a ground resolution derivation, every clause $E$ of the derivation can be replaced by a clause $E^* \subseteq E$ derived from the new inputs, with no more steps. In particular, if $D$ is in an unsatisfiable set $S$, then $(S \setminus \{D\}) \cup \{C\}$ has a refutation no longer than the shortest refutation of $S$; and if $C \in S$ already, $S \setminus \{D\}$ has one.

*Proof.* Induction along the derivation. Set $D^* = C$ and $E^* = E$ for the other inputs. Let $E$ be the resolvent of $E_1$ and $E_2$ on $L \in E_1$ and $\bar L \in E_2$, with $E_1^* \subseteq E_1$ and $E_2^* \subseteq E_2$ already built. If $L \in E_1^*$ and $\bar L \in E_2^*$, let $E^*$ be their resolvent; it is a subset of $E$. If $L \notin E_1^*$, then $E_1^* \subseteq E_1 \setminus \{L\} \subseteq E$, so let $E^* = E_1^*$, with no new step. The case $\bar L \notin E_2^*$ is the same. At the end, $\square^* \subseteq \square$ is $\square$. $\square$

**Strategies.** The replacement in Theorem 2 keeps the shape of a derivation, so it keeps every restriction that is preserved by passing to a subset of a parent. Two cases on this site:

- *Unrestricted resolution.* Theorem 2 covers ground clauses. For first-order clauses, forward and backward deletion in a running prover needs care with infinite chains of deletions and with factors; the proof on the [Robinson's resolution](/robinson-resolution/) page does this with the length condition (its Lemmas 5 to 7), and the [ordered resolution](/ordered-resolution/) page does it for multiset subsumption.
- *Set of support.* The completeness proof on the [set of support](/set-of-support/) page gives a ground refutation in which every step has a parent that is false in a fixed model $I$ of the clauses outside the support. A subset of a ground clause that is false in $I$ is also false in $I$, so after the replacement of Theorem 2 every step still has a parent false in $I$, and such a parent is a support clause or derived from one.

For strategies that restrict which clauses may be parents by their origin, such as [input resolution](/input-resolution/) and [linear resolution](/linear-resolution/), backward deletion of an input clause by a derived clause changes the set of allowed parents, and Theorem 2 alone does not show completeness.

## Examples

**Simple cases.** $P(x)$ subsumes $P(a) \vee Q(b)$ with $x \mapsto a$. $P(x, y)$ subsumes $P(a, b)$, but $P(x, x)$ does not, since $x$ cannot be both $a$ and $b$. $P(x) \vee Q(x)$ does not subsume $P(a) \vee Q(b)$, but $P(x) \vee Q(y)$ does.

**Colouring.** For the triangle, $C_G = \{E(x_1, x_2), E(x_2, x_3), E(x_1, x_3)\}$ subsumes the six-literal clause $D$, with $x_i \mapsto c_{i-1}$. For the complete graph on 4 vertices, $C_G$ has six literals and does not subsume $D$, because 4 vertices that are pairwise adjacent need 4 colours.

**Factors and the length condition.** Without the length condition, $P(x) \vee P(y)$ subsumes its own factor $P(x)$, with $y \mapsto x$. A prover that deletes by this test deletes every factor of this clause, and on the unsatisfiable set $\{P(x) \vee P(y), \lnot P(u) \vee \lnot P(v)\}$ it saturates without deriving $\square$. With the condition $|C| \le |D|$ the factor is kept, and the prover finds the refutation. See [factoring](/factoring/).

**Forward and backward.** When a prover derives $P(a) \vee Q(b)$ while $P(x)$ is stored, it discards the new clause (forward subsumption). When it derives $P(x)$ while $P(a) \vee Q(b)$ is stored, it deletes the stored clause (backward subsumption).

## Where it is used

- **Resolution and superposition provers.** Forward and backward subsumption are standard in [Robinson's resolution](/robinson-resolution/), [ordered resolution](/ordered-resolution/) and [superposition](/superposition/), where subsumption is a case of redundancy. Most derived clauses are subsumed, so deletion keeps the clause set from exploding.
- **Indexing.** Provers find candidate subsuming or subsumed clauses with [term indexing](/term-indexing/), such as discrimination trees and feature vectors, and then run a backtracking matcher.
- **Inductive logic programming.** θ-subsumption orders clauses by generality, and Plotkin's least general generalization of two clauses is a least general clause that subsumes both; see [Plotkin's lgg](/plotkin-lgg/).
- **SAT solvers.** For ground clauses the test is $C \subseteq D$, and [CDCL](/cdcl/) solvers remove subsumed learned clauses and use self-subsuming resolution to shorten clauses.

## References
