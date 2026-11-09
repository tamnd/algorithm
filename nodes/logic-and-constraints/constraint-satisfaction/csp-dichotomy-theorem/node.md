---
tag: EFM807
kind: theorem
slug: csp-dichotomy-theorem
name: CSP dichotomy theorem
aliases:
- Bulatov-Zhuk theorem
- Feder-Vardi dichotomy conjecture
- algebraic dichotomy theorem
area: logic-and-constraints/constraint-satisfaction
level: research
summary: Every fixed-template CSP is either in P or NP-complete, settling the Feder-Vardi conjecture.
prereqs: [constraint-language-polymorphisms, schaefer-dichotomy-theorem, np-complete]
see_also: [constraint-satisfaction-problem, boolean-constraint-satisfaction, counting-csp, k-consistency, graph-coloring, datalog, polynomial-time-reduction, xor-sat]
sources:
  - paper: doi:10.1137/S0097539794266766
    title: Tomás Feder and Moshe Y. Vardi, The computational structure of monotone monadic SNP and constraint satisfaction, a study through Datalog and group theory, SIAM Journal on Computing 28(1), 1998
    locator: pages 57 to 104 (the dichotomy conjecture for CSPs with a fixed finite template, and the relation between MMSNP and CSP)
  - paper: doi:10.1137/S0097539700376676
    title: Andrei Bulatov, Peter Jeavons and Andrei Krokhin, Classifying the complexity of constraints using finite algebras, SIAM Journal on Computing 34(3), 2005
    locator: pages 720 to 742 (reduction to cores with constants, NP-completeness without a Taylor polymorphism, and the algebraic form of the conjecture)
  - paper: doi:10.1109/FOCS.2017.37
    title: Andrei A. Bulatov, A dichotomy theorem for nonuniform CSPs, Proceedings of the 58th IEEE Symposium on Foundations of Computer Science (FOCS 2017)
    locator: pages 319 to 330 (a polynomial algorithm for every template with a weak near-unanimity polymorphism)
  - paper: doi:10.1109/FOCS.2017.38
    title: Dmitriy Zhuk, A proof of CSP dichotomy conjecture, Proceedings of the 58th IEEE Symposium on Foundations of Computer Science (FOCS 2017)
    locator: pages 331 to 342 (an independent polynomial algorithm for every template with a weak near-unanimity polymorphism)
  - paper: doi:10.1145/3402029
    title: Dmitriy Zhuk, A proof of the CSP dichotomy conjecture, Journal of the ACM 67(5), 2020
    locator: the full version of the algorithm, with the reductions to binary absorbing subuniverses, centers and linear factors
  - paper: doi:10.1016/0095-8956(90)90132-J
    title: Pavol Hell and Jaroslav Nešetřil, On the complexity of H-coloring, Journal of Combinatorial Theory, Series B 48(1), 1990
    locator: pages 92 to 110 (H-colouring of undirected graphs is in P when H is bipartite or has a loop, and NP-complete otherwise)
  - paper: doi:10.1145/1120582.1120584
    title: Andrei A. Bulatov, A dichotomy theorem for constraint satisfaction problems on a 3-element set, Journal of the ACM 53(1), 2006
    locator: pages 66 to 120 (the dichotomy for domains of size 3)
  - paper: "Manuel Bodirsky and Martin Grohe, Non-dichotomies in constraint satisfaction complexity, Proceedings of ICALP 2008, Lecture Notes in Computer Science 5126, Springer, 2008, pages 184 to 196"
    locator: every computational problem is equivalent to the CSP of some infinite template, so the dichotomy fails for infinite templates
---

## Statement

A *template* is a finite relational structure $\mathbf{B} = (B; R_1, \ldots, R_k)$: a finite domain $B$ and finitely many relations on it. CSP($\mathbf{B}$) asks, for a given finite structure $\mathbf{A}$ with relations of the same arities, whether there is a homomorphism $\mathbf{A} \to \mathbf{B}$, a map $h: A \to B$ that sends each tuple of each relation of $\mathbf{A}$ into the matching relation of $\mathbf{B}$. This is the [constraint satisfaction problem](/constraint-satisfaction-problem/) whose constraints all come from the language $\Gamma = \{R_1, \ldots, R_k\}$: the elements of $A$ are the variables and the tuples of $\mathbf{A}$ are the constraints.

> **Theorem (Bulatov 2017; Zhuk 2017, 2020).** For every finite template $\mathbf{B}$, CSP($\mathbf{B}$) is in P or NP-complete.

> **Theorem (algebraic form).** Let $\mathbf{B}$ be a finite template that is a core. If $\mathbf{B}$ has a weak near-unanimity polymorphism, equivalently a Siggers polymorphism, then CSP($\mathbf{B}$) is in P. Otherwise CSP($\mathbf{B}$) is NP-complete.

The terms are defined on the [polymorphisms](/constraint-language-polymorphisms/) page. An operation $w$ of arity $n \ge 2$ is a *weak near-unanimity* (WNU) operation if $w(x, \ldots, x) = x$ and $w(y, x, \ldots, x) = w(x, y, x, \ldots, x) = \cdots = w(x, \ldots, x, y)$ for all $x, y$. A *Siggers* operation is a 4-ary idempotent $s$ with $s(a, r, e, a) = s(r, a, r, e)$ for all $a, r, e$. Every template has a core with the same CSP, so the algebraic form covers all templates. Under P $\ne$ NP, it says that CSP($\mathbf{B}$) is in P exactly when the core of $\mathbf{B}$ has a WNU polymorphism.

**How it relates to the Boolean case.** The [Boolean CSP](/boolean-constraint-satisfaction/) is the case $|B| = 2$, and [Schaefer's theorem](/schaefer-dichotomy-theorem/) is this theorem for it, with six explicit classes. For $|B| \ge 3$ no such short list exists, and the polymorphism condition replaces it. This page covers arbitrary finite domains and the algebraic proof.

## In plain words

Fix a finite set of values and a finite list of rule types. The problem is: given unknowns and rules of these types, can all rules hold at once? Feder and Vardi asked in 1993 whether every such problem is either easy, solvable in polynomial time, or as hard as any problem in NP. Most of NP does not behave this way: if P $\ne$ NP, Ladner's theorem gives problems that are neither.

The answer is yes. The deciding factor is whether the rule types have a certain kind of "averaging" operation: a way to combine several solutions into a new one that treats its inputs almost symmetrically. With such an operation, a clever polynomial algorithm solves every instance. Without it, the rule types can simulate 3-SAT.

## Proof

The proof has three parts. Parts 1 and 2 are short and given in full. Part 3 is the hardness direction, due to Bulatov, Jeavons and Krokhin (2005), and is outlined. Part 4, the algorithms, is the work of Bulatov (2017) and Zhuk (2017, 2020), and is outlined with references.

**Part 1, cores.** An endomorphism of $\mathbf{B}$ is a homomorphism $\mathbf{B} \to \mathbf{B}$, a unary polymorphism. Let $e$ be an endomorphism with the smallest image, and let $\mathbf{C}$ be $\mathbf{B}$ restricted to $e(B)$. Then $\mathbf{C}$ is a *core*: if some endomorphism $g$ of $\mathbf{C}$ were not a bijection, $g \circ e$ would be an endomorphism of $\mathbf{B}$ with a smaller image.

> **Lemma 1.** CSP($\mathbf{B}$) and CSP($\mathbf{C}$) have the same yes-instances.
>
> *Proof.* If $h: \mathbf{A} \to \mathbf{B}$, then $e \circ h: \mathbf{A} \to \mathbf{C}$, since $e$ maps each tuple of a relation of $\mathbf{B}$ into the same relation, inside $e(B)$. If $h: \mathbf{A} \to \mathbf{C}$, then $h$ is also a homomorphism to $\mathbf{B}$, as $\mathbf{C}$ is a substructure. $\square$

**Part 2, adding constants.** Let $\mathbf{C}$ be a core on $\{c_1, \ldots, c_q\}$, and let $\mathbf{C}^+$ add the unary relations $\{c\}$ for each $c$. The polymorphisms of $\mathbf{C}^+$ are the idempotent polymorphisms of $\mathbf{C}$.

> **Lemma 2.** CSP($\mathbf{C}^+$) reduces to CSP($\mathbf{C}$) in polynomial time.
>
> *Proof.* Build the structure $\mathbf{D}$ with elements $v_1, \ldots, v_q$ and, for each relation $R$ of $\mathbf{C}$ and each tuple $(c_{i_1}, \ldots, c_{i_r}) \in R$, the tuple $(v_{i_1}, \ldots, v_{i_r})$ in $R^{\mathbf{D}}$. A map $g: \mathbf{D} \to \mathbf{C}$ is a homomorphism exactly when $c_i \mapsto g(v_i)$ is an endomorphism of $\mathbf{C}$, and since $\mathbf{C}$ is a core, an automorphism. Given an instance $\mathbf{A}$ of CSP($\mathbf{C}^+$), take the disjoint union of $\mathbf{A}$ without its unary constant relations and $\mathbf{D}$, and merge each element of $\mathbf{A}$ that must equal $c_i$ with $v_i$. If $\mathbf{A}$ has a solution, extend it by $v_i \mapsto c_i$, which is a homomorphism since the identity is an automorphism. If the new instance has a solution $h$, then $\alpha: c_i \mapsto h(v_i)$ is an automorphism, and $\alpha^{-1} \circ h$ is a solution that maps each $v_i$ to $c_i$; on $\mathbf{A}$ it respects the constants. The new instance has size $O(|\mathbf{A}| + |\mathbf{C}|)$, and $\mathbf{C}$ is fixed. $\square$

The reverse reduction is trivial, so CSP($\mathbf{C}$) and CSP($\mathbf{C}^+$) are polynomially equivalent, and it suffices to study idempotent polymorphisms of cores.

**Part 3, hardness without a WNU polymorphism (outline).** Let $\mathbf{C}^+$ be as above, and suppose it has no Taylor polymorphism, an idempotent $t$ satisfying, for each coordinate $i$, some identity $t(\ldots) = t(\ldots)$ in the variables $x, y$ with $x$ in position $i$ on the left and $y$ on the right. By results of universal algebra going back to Taylor, the algebra of polymorphisms then has a subalgebra with a two-element quotient on which every polymorphism acts as a projection. Relations preserved by projections on two elements are all Boolean relations, so $\mathbf{C}^+$ can define, by primitive positive formulas over a subset and a quotient, the relations of 3-SAT. Each such definition is a polynomial reduction ([Galois connection](/constraint-language-polymorphisms/)), so 3-SAT reduces to CSP($\mathbf{C}^+$), and by Lemmas 1 and 2 to CSP($\mathbf{B}$) (Bulatov, Jeavons and Krokhin 2005). Maróti and McKenzie (2008) showed that for finite idempotent algebras a Taylor polymorphism exists exactly when a WNU polymorphism exists, and Siggers (2010) gave the single Siggers identity, so all three conditions are the same.

**Part 4, algorithms with a WNU polymorphism (outline).** This direction was open from 1993 to 2017. Two independent proofs appeared at FOCS 2017.

- *Zhuk's algorithm.* It first enforces local conditions that Zhuk calls cycle-consistency and irreducibility. If some domain has a proper subset of one of three special kinds, a binary absorbing subuniverse, a center, or a subuniverse coming from a polynomially complete quotient, Zhuk proves that the instance has a solution inside this smaller domain if it has any solution at all, so the algorithm shrinks the domain and recurses. Otherwise the domains have quotients with an affine structure, and the algorithm solves linear equations over these quotients to cut down the possible solutions, then recurses. The proof that each reduction keeps a solution uses the WNU polymorphism throughout.
- *Bulatov's algorithm.* It colours the pairs of elements of each domain by the kind of local structure the polymorphisms create on them, as semilattice, majority or affine edges, and combines propagation along semilattice and majority edges with a form of Gaussian elimination for the affine parts, so that solutions found on separate parts can be glued.

Both proofs are long. They join two older lines of algorithms: *bounded width*, where a fixed level of [k-consistency](/k-consistency/) decides the instance, which holds for a core with constants exactly when it has WNU polymorphisms of all arities from 3 on (Barto and Kozik 2014; in this form Kozik, Krokhin, Valeriote and Willard 2015), and *few subpowers*, a generalization of Gaussian elimination that covers linear equations over finite groups and fields. Neither alone suffices: linear equations modulo 2 do not have bounded width, and Horn clauses do not have few subpowers.

## Consequences

- **Graph colouring problems.** For an undirected graph $H$, the $H$-colouring problem asks whether a graph maps to $H$ by a homomorphism. Hell and Nešetřil (1990) showed that it is in P when $H$ is bipartite or has a loop and NP-complete otherwise; [graph colouring](/graph-coloring/) with $k \ge 3$ colours is the case $H = K_k$. This is the case of one symmetric binary relation, and it follows from the algebraic form.
- **Small domains.** Schaefer's theorem for $|B| = 2$ and Bulatov's theorem for $|B| = 3$ (2006) are special cases.
- **No intermediate CSPs.** Under P $\ne$ NP, no finite-template CSP has an intermediate degree, in contrast with Ladner's theorem for NP in general. Feder and Vardi (1998) showed that every problem in the logic class MMSNP is equivalent to a finite-template CSP under randomized polynomial reductions, so a dichotomy holds there as well.
- **A decidable criterion.** Whether a given finite template has a 4-ary Siggers polymorphism can be checked by a finite search, so one can decide from the template which case applies.
- **Algorithm choice.** In practice, the theorem tells which languages admit a polynomial algorithm, and the bounded width result tells when [constraint propagation](/constraint-propagation/) alone, at a fixed level, suffices.
- **Further classifications.** The same algebraic method classifies the [counting CSP](/counting-csp/), valued CSPs and quantified CSPs on small domains, and it is the starting point for the study of promise CSPs.

## Tightness

**Finite templates are needed.** For infinite templates the dichotomy fails: Bodirsky and Grohe (2008) showed that every computational problem is polynomially equivalent to the CSP of some infinite template, so under P $\ne$ NP some of these CSPs are neither in P nor NP-complete. Dichotomies are known for some infinite classes, such as templates first-order definable over $(\mathbb{Q}; <)$, the temporal CSPs.

**A fixed template is needed.** If the template is part of the input, the problem contains [SAT](/sat/) and graph [colouring](/graph-coloring/) with a given number of colours and is NP-complete, and the question of a dichotomy does not arise in the same form.

**The core matters.** Let $\mathbf{B}$ be the graph made of a triangle $K_3$ and a separate vertex $\ell$ with a loop. Its CSP is trivial, since every graph maps to $\ell$, and its core is $\ell$ alone. But $\mathbf{B}$ has no idempotent WNU polymorphism $w$. If $w$ sent a tuple $a$ of triangle vertices to $\ell$, then for any tuple $b$ with $b_i$ a neighbour of $a_i$ in the triangle, $w(b)$ would be a neighbour of $\ell$, so $w(b) = \ell$; if $a$ uses at most two values, $b$ can be constant, $b_i = c$, and $w(c, \ldots, c) = c \ne \ell$ is a contradiction, and if $a$ uses all three values, some such $b$ uses only two values, which is the first case. So $w$ maps the triangle into itself and gives a WNU polymorphism of $K_3$, which does not exist, since every idempotent polymorphism of $K_3$ is a projection. So the condition must be checked on the core, or with all constants added to the core.

**Single relations already suffice for hardness.** The NP-complete side is reached already by a single binary relation, such as $K_3$, and on two elements by a single ternary relation, such as one-in-three. So no bound on the arity or the number of relations changes the picture.

## History

Feder and Vardi stated the dichotomy conjecture in 1993, in the conference version of their 1998 paper, after showing that CSPs with a finite template form the largest part of the logic class MMSNP that might have a dichotomy. Earlier cases were Schaefer's for two elements (1978) and Hell and Nešetřil's for undirected graphs (1990). Jeavons, Cohen and Gyssens (1997) introduced polymorphisms, and Bulatov, Jeavons and Krokhin (2005) reduced the conjecture to cores with constants and stated it in algebraic form. Bulatov proved it for three elements (2006) and for conservative languages, which contain all unary relations. Barto and Kozik characterized bounded width, and Idziak, Marković, McKenzie, Valeriote and Willard (2010) gave the few subpowers algorithm. In 2017 Bulatov and Zhuk announced independent proofs of the full conjecture, both presented at FOCS 2017; Zhuk's journal version appeared in the Journal of the ACM in 2020.

## References
