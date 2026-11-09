---
tag: SSC0Z5
kind: concept
slug: constraint-language-polymorphisms
name: Polymorphisms of constraint languages
aliases:
- polymorphism clone
- algebraic approach to CSP
- Galois connection Inv-Pol
area: logic-and-constraints/constraint-satisfaction
level: research
summary: Operations preserving a constraint language; their existence characterises the tractable CSP fragments.
prereqs: [constraint-satisfaction-problem, polynomial-time-reduction]
see_also: [csp-dichotomy-theorem, schaefer-dichotomy-theorem, boolean-constraint-satisfaction, k-consistency, counting-csp, horn-sat, 2-sat, xor-sat]
sources:
  - paper: doi:10.1145/263867.263489
    title: Peter Jeavons, David Cohen and Marc Gyssens, Closure properties of constraints, Journal of the ACM 44(4), 1997
    locator: pages 527 to 548 (closure of constraint languages under operations, and tractable languages closed under constant, near-unanimity, semilattice or affine operations)
  - paper: doi:10.1137/S0097539700376676
    title: Andrei Bulatov, Peter Jeavons and Andrei Krokhin, Classifying the complexity of constraints using finite algebras, SIAM Journal on Computing 34(3), 2005
    locator: pages 720 to 742 (reduction to cores and idempotent algebras, NP-hardness when the algebra has no Taylor term, and the algebraic dichotomy conjecture)
  - paper: "Peter Jeavons, On the algebraic structure of combinatorial problems, Theoretical Computer Science 200(1-2), 1998, pages 185 to 204"
    locator: the theorem that pp-definable relations can be added to a constraint language without changing the complexity, and the Galois connection with polymorphisms
  - paper: "David Geiger, Closed systems of functions and predicates, Pacific Journal of Mathematics 27(1), 1968, pages 95 to 100"
    locator: the Galois connection between clones of operations and relational clones on a finite set
  - paper: "Libor Barto, Andrei Krokhin and Ross Willard, Polymorphisms, and how to use them, in The Constraint Satisfaction Problem, Complexity and Approximability, Dagstuhl Follow-Ups 7, 2017, pages 1 to 44"
    locator: a survey of pp-definitions, pp-interpretations, cores, Taylor, weak near-unanimity and Siggers polymorphisms, and their use in the dichotomy
  - paper: "Mark H. Siggers, A strong Mal'cev condition for locally finite varieties omitting the unary type, Algebra Universalis 64, 2010, pages 15 to 20"
    locator: the 6-ary Siggers term, which exists exactly when a Taylor term exists
  - paper: "Miklós Maróti and Ralph McKenzie, Existence theorems for weakly symmetric operations, Algebra Universalis 59, 2008, pages 463 to 489"
    locator: a finite idempotent algebra has a Taylor term exactly when it has a weak near-unanimity term
---

A polymorphism of a constraint language $\Gamma$ is an operation $f$ on the domain such that applying $f$ coordinate by coordinate to tuples of any relation of $\Gamma$ gives a tuple of the same relation. The polymorphisms of $\Gamma$ form a *clone*, $\mathrm{Pol}(\Gamma)$, and for a finite language this clone alone determines the complexity of the [constraint satisfaction problem](/constraint-satisfaction-problem/) CSP($\Gamma$) up to polynomial-time reductions. Jeavons, Cohen and Gyssens (1997) started this algebraic approach, and Bulatov, Jeavons and Krokhin (2005) turned it into a precise conjecture: CSP($\Gamma$) is in P when $\Gamma$ has a polymorphism of a certain kind, and NP-complete otherwise. The [CSP dichotomy theorem](/csp-dichotomy-theorem/) of Bulatov and Zhuk proved it. On two values, the six polymorphisms behind [Schaefer's theorem](/schaefer-dichotomy-theorem/) are the classic example.

## In plain words

Fix a set of allowed rules, all over the same small set of values. Think of an operation that takes a few solutions and combines them, one position at a time, into a new assignment. If the new assignment is always a solution again, the operation is a polymorphism. For example, if a rule's solutions are closed under "position-wise AND", the rule can be written with Horn clauses.

A polymorphism is a symmetry of the solution sets that lets an algorithm combine partial answers. If the rules have a good polymorphism, the problem is easy. If the only polymorphisms are trivial, such as "return the first input", the rules can express 3-SAT and the problem is NP-complete. The deep result of the field is that nothing lies between these two cases.

## The idea

**Notation.** $A$ is a finite domain with $d = |A| \ge 2$ values. A *constraint language* $\Gamma$ is a set of relations on $A$, each of some arity $r$, so $R \subseteq A^r$. An instance of CSP($\Gamma$) is a set of variables and a list of constraints $R(x_{i_1}, \ldots, x_{i_r})$ with $R \in \Gamma$. An operation of arity $k$ is a map $f: A^k \to A$.

**Polymorphisms.** $f$ *preserves* $R$ if for all $t_1, \ldots, t_k \in R$, the tuple $f(t_1, \ldots, t_k) = (f(t_1[1], \ldots, t_k[1]), \ldots, f(t_1[r], \ldots, t_k[r]))$ lies in $R$. $f$ is a *polymorphism* of $\Gamma$ if it preserves every relation of $\Gamma$. $\mathrm{Pol}(\Gamma)$ contains all projections $\pi^k_i(x_1, \ldots, x_k) = x_i$ and is closed under composition, so it is a clone. For a set $F$ of operations, $\mathrm{Inv}(F)$ is the set of relations that every operation of $F$ preserves.

**Primitive positive definitions.** A relation $R$ is *pp-definable* from $\Gamma$ if $R(y_1, \ldots, y_r) \iff \exists z_1 \ldots z_s \; \phi$, where $\phi$ is a conjunction of constraints from $\Gamma$ and equalities on the $y_i$ and $z_j$. Write $\langle \Gamma \rangle$ for the set of these relations.

> **Theorem (Geiger 1968; Bodnarchuk, Kaluzhnin, Kotov and Romov 1969).** For a set $\Gamma$ of relations on a finite set $A$, $\mathrm{Inv}(\mathrm{Pol}(\Gamma)) = \langle \Gamma \rangle$, where non-empty relations are considered.
>
> *Proof.* ($\supseteq$) A polymorphism $f$ preserves each conjunct of $\phi$, so applied to $k$ satisfying assignments of $\phi$ it gives a satisfying assignment, and projection onto $y_1, \ldots, y_r$ keeps this. ($\subseteq$) Let $R \in \mathrm{Inv}(\mathrm{Pol}(\Gamma))$ have the tuples $t_1, \ldots, t_k$. Take one variable $v_c$ for each $c \in A^k$, and for each $S \in \Gamma$ of arity $s$ and each choice of $u_1, \ldots, u_k \in S$, add the constraint $S(v_{c_1}, \ldots, v_{c_s})$, where $c_j = (u_1[j], \ldots, u_k[j])$. An assignment $c \mapsto g(c)$ satisfies these constraints exactly when $g: A^k \to A$ is a polymorphism. Now let $b_j = (t_1[j], \ldots, t_k[j])$ for $j = 1, \ldots, r$, and quantify away every variable except $v_{b_1}, \ldots, v_{b_r}$. The resulting relation is $\{(g(b_1), \ldots, g(b_r)) : g \in \mathrm{Pol}_k(\Gamma)\} = \{g(t_1, \ldots, t_k)\}$. It is inside $R$ because $R$ is preserved by every polymorphism, and it contains each $t_i$, taking $g = \pi^k_i$. So it equals $R$, and this is a pp-definition. $\square$

> **Theorem (Jeavons, Cohen and Gyssens 1997; Jeavons 1998).** Let $\Gamma$ and $\Delta$ be languages on $A$ with $\Delta$ finite. If $\mathrm{Pol}(\Gamma) \subseteq \mathrm{Pol}(\Delta)$, then CSP($\Delta$) reduces to CSP($\Gamma$) in polynomial time.
>
> *Proof.* By the theorem above, each relation of $\Delta$ is in $\langle \Gamma \rangle$; fix one pp-definition for each, which is possible as $\Delta$ is finite. Given an instance of CSP($\Delta$), replace each constraint by the conjunction of its pp-definition, with new variables for the quantified ones, and merge the variables that an equality joins. Each constraint grows by a constant amount. An assignment of the original variables satisfies the old instance exactly when it extends to the new variables so as to satisfy the new one, so the answers agree. $\square$

So the complexity of CSP($\Gamma$) depends only on $\mathrm{Pol}(\Gamma)$: more polymorphisms means fewer expressible relations, and an easier problem.

**Cores and idempotence.** $\Gamma$ is a *core* if every unary polymorphism is a bijection. Every finite $\Gamma$ has a core $\Gamma'$, on a subset of $A$, with the same yes-instances, so CSP($\Gamma$) and CSP($\Gamma'$) are the same problem. For a core, adding the singleton relations $\{a\}$ for $a \in A$ does not change the complexity (Bulatov, Jeavons and Krokhin 2005), and the polymorphisms of the result are the *idempotent* ones, with $f(a, \ldots, a) = a$. So one may study idempotent polymorphisms of cores.

**The key polymorphisms.** Each of the following is a property of $\mathrm{Pol}(\Gamma)$:

- **Only projections.** If a core with constants has only projections as idempotent polymorphisms, then $\langle \Gamma \rangle$ contains every relation on $A$, including those of 3-SAT, and CSP($\Gamma$) is NP-complete.
- **Semilattice.** A binary operation that is associative, commutative and idempotent, such as $\min$ or $\wedge$. Then generalized arc consistency decides CSP($\Gamma$) (Jeavons, Cohen and Gyssens 1997). Horn clauses are closed under $\wedge$.
- **Near-unanimity.** $f(y, x, \ldots, x) = f(x, y, x, \ldots, x) = \cdots = f(x, \ldots, x, y) = x$, of arity $k + 1 \ge 3$. Then strong $(k+1)$-consistency decides CSP($\Gamma$) (Jeavons, Cohen and Cooper 1998). The majority operation on $\{0, 1\}$ preserves all binary relations, which is why path consistency decides 2-SAT.
- **Mal'tsev.** $m(x, y, y) = m(y, y, x) = x$, such as $x - y + z$ in a group. Then a generalization of Gaussian elimination solves CSP($\Gamma$) (Bulatov and Dalmau 2006). Linear equations modulo $p$ are preserved by $x - y + z \bmod p$.
- **Weak near-unanimity (WNU).** Idempotent and $w(y, x, \ldots, x) = w(x, y, x, \ldots, x) = \cdots = w(x, \ldots, x, y)$, without asking that this value be $x$. Semilattice, near-unanimity and Mal'tsev operations all yield WNU polymorphisms.
- **Siggers.** A 6-ary idempotent $s$ with $s(x, x, y, y, z, z) = s(y, z, z, x, x, y)$ (Siggers 2010), or a 4-ary one with $s(a, r, e, a) = s(r, a, r, e)$ (Kearnes, Marković and McKenzie 2014).

For a finite idempotent algebra, having a WNU polymorphism, having a Siggers polymorphism and having a Taylor polymorphism are equivalent (Maróti and McKenzie 2008; Siggers 2010). Bulatov, Jeavons and Krokhin (2005) proved that a core with no Taylor polymorphism gives an NP-complete CSP, and conjectured the converse.

> **The algebraic dichotomy (Bulatov 2017; Zhuk 2017, 2020).** Let $\Gamma$ be a finite core language. If $\Gamma$ has a WNU polymorphism, equivalently a Siggers polymorphism, then CSP($\Gamma$) is in P. Otherwise it is NP-complete.

Assuming P $\ne$ NP, this says that CSP($\Gamma$) is in P exactly when such a polymorphism exists. The [CSP dichotomy theorem](/csp-dichotomy-theorem/) page gives the history and an outline of the proofs.

**Finer classes.** Polymorphisms also describe which algorithms work. CSP($\Gamma$) has *bounded width*, so that a fixed level of [k-consistency](/k-consistency/) decides it, exactly when $\Gamma$ has WNU polymorphisms of all arities $\ge 3$ (Barto and Kozik 2014; Kozik, Krokhin, Valeriote and Willard 2015). For counting, a Mal'tsev polymorphism is necessary for [#CSP](/counting-csp/) to be in FP, unless FP equals #P.

## Examples

**Two-colouring and three-colouring.** $K_2$, the relation $\ne$ on $\{0, 1\}$, has the polymorphisms majority and minority, $x \oplus y \oplus z$: if $a_i \ne b_i$ for $i = 1, 2, 3$, then each $b_i = 1 - a_i$, and $b_1 \oplus b_2 \oplus b_3 = 1 - (a_1 \oplus a_2 \oplus a_3)$. So 2-colouring is in P. $K_3$, the relation $\ne$ on $\{0, 1, 2\}$, is a core whose idempotent polymorphisms are projections, so 3-colouring is NP-complete. Hell and Nešetřil (1990) showed that for any undirected graph $H$, deciding whether a graph maps to $H$ is in P if $H$ is bipartite or has a loop, and NP-complete otherwise; this is the dichotomy for one-relation languages that are graphs.

**Boolean languages.** On $\{0, 1\}$ the six tractable cases of [Schaefer's theorem](/schaefer-dichotomy-theorem/) are the languages with one of the polymorphisms: constant 0, constant 1, $\wedge$ ([Horn](/horn-sat/)), $\vee$ (dual Horn), majority ([2-SAT](/2-sat/)) and minority $x \oplus y \oplus z$ ([XOR-SAT](/xor-sat/)). Of the 256 ternary Boolean relations, 15 have none of them, among them one-in-three and not-all-equal; the [Boolean CSP](/boolean-constraint-satisfaction/) page lists the counts.

**Linear equations.** Equations $a_1 x_1 + \cdots + a_r x_r = c$ over the field $\mathbb{Z}_p$ are preserved by $x - y + z$, a Mal'tsev operation, and they do not have bounded width; Gaussian elimination solves them.

**Ordered domains.** On $\{0, \ldots, d-1\}$, the relations preserved by $\min$ include $x \le y$ and $x \le c$, and arc consistency decides any instance built from them.

## Where it is used

- **Complexity classification.** Polymorphisms reduce the question "is CSP($\Gamma$) easy?" to a question about a finite algebra, which can be decided for a given finite $\Gamma$. This led to the [CSP dichotomy theorem](/csp-dichotomy-theorem/), to [Schaefer's theorem](/schaefer-dichotomy-theorem/) as a special case, and to the classification of [counting CSPs](/counting-csp/).
- **Algorithm design.** Each algorithmic idea has a polymorphism behind it: local consistency for bounded width, Gaussian elimination and its generalization for Mal'tsev and few subpowers, and the combination of both in the general algorithms of Bulatov and Zhuk.
- **Other problems.** The same tools classify the complexity of quantified CSPs, valued CSPs (with weighted polymorphisms), approximation of MAX-CSP, and promise CSPs, and they apply to CSPs with infinite domains such as temporal and spatial reasoning.
- **Database theory and logic.** pp-definitions are conjunctive queries, so polymorphisms describe which relations a database can define with such queries, and link CSPs with Datalog and with finite model theory.

## References
