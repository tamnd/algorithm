---
tag: QXTEBZ
kind: theorem
slug: schaefer-dichotomy-theorem
name: Schaefer's dichotomy theorem
aliases:
- Schaefer's theorem
- Boolean CSP dichotomy
area: logic-and-constraints/constraint-satisfaction
level: advanced
summary: Every Boolean CSP is in P if its relations fit one of six classes and is NP-complete otherwise.
prereqs: [boolean-constraint-satisfaction, constraint-language-polymorphisms]
see_also: [csp-dichotomy-theorem, horn-sat, 2-sat, xor-sat, one-in-three-sat, not-all-equal-sat, counting-csp, unit-propagation]
sources:
  - paper: doi:10.1145/800133.804350
    title: Thomas J. Schaefer, The complexity of satisfiability problems, Proceedings of the 10th ACM Symposium on Theory of Computing (STOC 1978)
    locator: pages 216 to 226 (the dichotomy theorem for SAT(S) and SAT_C(S), its proof, and the version for quantified formulas)
  - paper: doi:10.1145/263867.263489
    title: Peter Jeavons, David Cohen and Marc Gyssens, Closure properties of constraints, Journal of the ACM 44(4), 1997
    locator: pages 527 to 548 (the six tractable Boolean cases as closure under constant, AND, OR, majority and affine operations)
  - paper: doi:10.1137/0205048
    title: Shimon Even, Alon Itai and Adi Shamir, On the complexity of timetable and multicommodity flow problems, SIAM Journal on Computing 5(4), 1976
    locator: pages 691 to 703 (the polynomial algorithm for 2-SAT by trial assignment and propagation)
  - paper: "William F. Dowling and Jean H. Gallier, Linear-time algorithms for testing the satisfiability of propositional Horn formulae, Journal of Logic Programming 1(3), 1984, pages 267 to 284"
    locator: Horn satisfiability in linear time by forward chaining with counters
  - paper: "Emil L. Post, The two-valued iterative systems of mathematical logic, Annals of Mathematics Studies 5, Princeton University Press, 1941"
    locator: the complete description of the lattice of clones of Boolean operations
  - paper: "Elmar Böhler, Nadia Creignou, Steffen Reith and Heribert Vollmer, Playing with Boolean blocks, part II, constraint satisfaction problems, ACM SIGACT News 35(1), 2004"
    locator: a proof of Schaefer's theorem from Post's lattice and the Galois connection between clones and co-clones
  - book: isbn:9780898714791
    title: Nadia Creignou, Sanjeev Khanna and Madhu Sudan, Complexity Classifications of Boolean Constraint Satisfaction Problems, SIAM, 2001
    locator: the chapter on the complexity of satisfiability, with a full proof of Schaefer's theorem
---

## Statement

Let $\Gamma$ be a finite set of non-empty Boolean relations, and let SAT($\Gamma$) be the [Boolean constraint satisfaction problem](/boolean-constraint-satisfaction/) over $\Gamma$. Call $\Gamma$ 0-valid, 1-valid, Horn, dual Horn, bijunctive or affine if every relation of $\Gamma$ has this property; the six classes are defined on the Boolean CSP page.

> **Theorem (Schaefer 1978).** If $\Gamma$ is 0-valid, 1-valid, Horn, dual Horn, bijunctive or affine, then SAT($\Gamma$) is in P. Otherwise SAT($\Gamma$) is NP-complete.

> **Theorem (with constants).** Let SAT$_C$($\Gamma$) be SAT($\Gamma \cup \{\{0\}, \{1\}\}$), where variables can be fixed to 0 or 1. If $\Gamma$ is Horn, dual Horn, bijunctive or affine, SAT$_C$($\Gamma$) is in P. Otherwise it is NP-complete.

> **Theorem (polymorphism form; Jeavons, Cohen and Gyssens 1997).** SAT($\Gamma$) is in P if $\Gamma$ has one of the six [polymorphisms](/constraint-language-polymorphisms/) constant 0, constant 1, $x \wedge y$, $x \vee y$, $\mathrm{maj}(x, y, z)$ and $x \oplus y \oplus z$, and NP-complete otherwise.

The third form is the same theorem, because each class is exactly closure under its operation; the [Boolean CSP](/boolean-constraint-satisfaction/) page proves this. Since P $\ne$ NP is not known, the theorem says "in P or NP-complete", not "in P exactly when".

## In plain words

Take any fixed list of rule types on yes and no unknowns. Either all the rule types share one of six good shapes, and then a fast method solves every instance, or they do not, and then the problem is as hard as 3-SAT. There is nothing in between. The six shapes are: everything no works, everything yes works, Horn rules, dual Horn rules, rules on two unknowns, and parity equations.

This contrasts with NP as a whole: Ladner showed that if P $\ne$ NP, some problems in NP are neither in P nor NP-complete. Schaefer's theorem says that no Boolean CSP is such a problem.

## Proof

The proof has two parts: an algorithm for each of the six classes, given in full below, and the hardness of all other languages, outlined with references.

**Step 0, rewriting the constraints.** For a fixed $\Gamma$, write each relation of $\Gamma$ once as a formula of its class: the Horn, dual Horn or 2-clauses that it satisfies, or the GF(2) equations that it satisfies. By the definition of the classes such a formula exists, and the conjunction of all clauses of that shape satisfied by $R$ is one. Each relation has constant arity, so this is a constant amount of work, and an instance with $m$ constraints becomes a formula of $O(m)$ clauses or equations with the same solutions.

> **Lemma 1 (0-valid and 1-valid).** If $\Gamma$ is 0-valid, the all-0 assignment satisfies every instance. If it is 1-valid, the all-1 assignment does.
>
> *Proof.* Each constraint applies some $R \in \Gamma$ to its scope, and the all-0 assignment gives it the tuple $(0, \ldots, 0) \in R$. The same holds for 1. $\square$

> **Lemma 2 (Horn).** Let $\phi$ be a conjunction of Horn clauses on $x_1, \ldots, x_n$. Start with $T = \emptyset$. While some clause $\neg x_{a_1} \vee \cdots \vee \neg x_{a_k} \vee x_b$ has $\{a_1, \ldots, a_k\} \subseteq T$ and $b \notin T$, add $b$ to $T$. Then $\phi$ is satisfiable exactly when no clause $\neg x_{a_1} \vee \cdots \vee \neg x_{a_k}$ without a positive literal has $\{a_1, \ldots, a_k\} \subseteq T$ at the end, and in that case the assignment $s$ with $s_i = 1 \iff i \in T$ satisfies $\phi$.
>
> *Proof.* Every model $u$ of $\phi$ has $u_i = 1$ for all $i \in T$: this holds for $T = \emptyset$, and if $u$ is 1 on $a_1, \ldots, a_k$, the clause forces $u_b = 1$. So if a clause without a positive literal has all its variables in $T$, every model falsifies it, and there is no model. Otherwise consider $s$. A clause with head $x_b$ and body in $T$ has $b \in T$ when the loop stops, so $s_b = 1$ satisfies it. Any other clause has a body variable $a_j \notin T$, so $s_{a_j} = 0$ satisfies $\neg x_{a_j}$. So $s$ is a model, in fact the least one. With a counter per clause of the body variables not yet in $T$, and for each variable the list of clauses whose body contains it, each variable enters $T$ once and each counter decreases at most once per body literal, so the time is linear in the size of $\phi$ (Dowling and Gallier 1984). $\square$

> **Lemma 3 (dual Horn).** If $\Gamma$ is dual Horn, SAT($\Gamma$) is solvable in linear time.
>
> *Proof.* Replace every variable $x_i$ by $\neg y_i$. A clause with at most one negative literal becomes a clause with at most one positive literal, so the new formula is Horn, and $s$ is a model of the old formula exactly when its complement is a model of the new one. Apply Lemma 2. $\square$

> **Lemma 4 (bijunctive; Even, Itai and Shamir 1976).** Let $\phi$ be a conjunction of clauses with at most two literals. The following procedure decides $\phi$ in $O(n m)$ time. Pick an unassigned variable $x$. Set $x = 1$ and *propagate*: while some clause has all literals but one false and that one unassigned, make it true; stop with a *conflict* if a clause has all its literals false. If there is no conflict, keep the assignment. If there is a conflict, undo it, set $x = 0$, and propagate again; if this also gives a conflict, report "unsatisfiable". Repeat until all variables are assigned.
>
> *Proof.* First, unit clauses of $\phi$ are propagated at the start, with the same rules. Two facts give correctness.
>
> (a) *Propagation is sound.* If the current partial assignment $p$ extends to a model of $\phi$, then so does $p$ with each forced literal added, because a model that extends $p$ must make the last unassigned literal of such a clause true. So if $x = 1$ leads to a conflict, every model that extends the current assignment has $x = 0$.
>
> (b) *A kept assignment loses nothing.* After a propagation without conflict, consider a clause with an assigned variable. If one of its literals is true, it is satisfied. If one of its literals is false, the clause had at most one other literal, and propagation made it true; a false clause would be a conflict. So every clause that mentions an assigned variable is satisfied, and the other clauses use only unassigned variables. These remaining clauses are a subset of $\phi$, so any model of $\phi$ satisfies them; and any model of them, joined with the current assignment, satisfies $\phi$. So $\phi$ is satisfiable exactly when the remaining clauses are.
>
> By (b), keeping an assignment never turns a satisfiable formula into an unsatisfiable one. By (a), if both $x = 1$ and $x = 0$ lead to a conflict from the current assignment, no model extends it; by (b), every kept assignment so far has kept satisfiability, so $\phi$ itself is unsatisfiable. When all variables are assigned without conflict, every clause is satisfied. Each variable costs at most two propagations of $O(m)$ steps, so the time is $O(n m)$. $\square$

Aspvall, Plass and Tarjan (1979) reduced the time to $O(n + m)$ with the implication graph, which has an edge $\neg a \to b$ and $\neg b \to a$ for each clause $a \vee b$: the formula is unsatisfiable exactly when some $x$ and $\neg x$ lie in the same strongly connected component. See [2-SAT](/2-sat/).

> **Lemma 5 (affine).** A system of $m$ linear equations over GF(2) in $n$ variables can be decided, and solved, by Gaussian elimination in $O(m n \min(m, n))$ bit operations. If it has solutions, it has exactly $2^{n - \rho}$ of them, where $\rho$ is the rank.
>
> *Proof.* Adding one equation to another, and swapping equations, do not change the solution set, because each step can be undone by a step of the same kind. Elimination brings the system to echelon form: $\rho$ equations, each with a pivot variable that appears in no other equation, plus equations $0 = c$. If some $c = 1$, there is no solution. Otherwise each of the $n - \rho$ non-pivot variables can take any value, and each pivot variable is then fixed by its equation, which gives $2^{n - \rho}$ solutions. Each of at most $\min(m, n)$ pivots is cleared from at most $m$ rows of $n + 1$ bits. $\square$

Lemmas 1 to 5, with Step 0, show the polynomial cases of both theorems. In the version with constants, the constants $\{0\}$ and $\{1\}$ are Horn, dual Horn, bijunctive and affine, so they can be added to the formula of any of these four classes, but they are not both 0-valid and 1-valid.

**Hardness (outline).** SAT($\Gamma$) is in NP, since an assignment can be checked. For NP-hardness, Schaefer (1978) showed that a language outside the six classes can express every Boolean relation by primitive positive formulas, which are conjunctions of constraints with some variables existentially quantified, or, if all its relations are closed under complement, every relation closed under complement. Primitive positive definitions give polynomial reductions ([Galois connection](/constraint-language-polymorphisms/)), so 3-SAT, or not-all-equal 4-SAT in the second case, reduces to SAT($\Gamma$), and both are NP-complete. In the polymorphism language: when $\mathrm{Pol}(\Gamma)$ contains none of the six operations, Post's description of all Boolean clones (Post 1941) shows that $\mathrm{Pol}(\Gamma)$ consists of projections, or of projections and their negations, and the Galois connection then gives the two cases above (Böhler, Creignou, Reith and Vollmer 2004). For SAT$_C$($\Gamma$) the constants rule out the second case. The full proof is in Schaefer (1978) and in Creignou, Khanna and Sudan (2001).

## Consequences

- **The known Boolean cases.** [2-SAT](/2-sat/) (bijunctive), [Horn-SAT](/horn-sat/) and dual Horn SAT, and [XOR-SAT](/xor-sat/) (affine) are in P. [One-in-three SAT](/one-in-three-sat/), [not-all-equal SAT](/not-all-equal-sat/) and [3-SAT](/3-sat/) are NP-complete, since their relations lie in no class, and the positive one-in-three and not-all-equal versions are NP-complete without negated literals.
- **No intermediate Boolean CSPs.** Unlike NP in general, the Boolean CSPs avoid the intermediate degrees that Ladner's theorem gives under P $\ne$ NP.
- **The classification is decidable.** Given $\Gamma$ as tables, checking the six closures takes time polynomial in the table sizes, so one can tell which case applies.
- **A template for other problems.** The same six classes, or sub-lattices of Post's lattice, classify counting ([#CSP](/counting-csp/): only affine stays easy), quantified Boolean formulas (Horn, dual Horn, bijunctive and affine are in P, everything else PSPACE-complete), and optimization problems.
- **A special case of the CSP dichotomy.** For domains of any finite size, the [CSP dichotomy theorem](/csp-dichotomy-theorem/) of Bulatov and Zhuk gives the same "P or NP-complete" split, and on $\{0, 1\}$ it reduces to Schaefer's theorem: each of the six polymorphisms gives a weak near-unanimity polymorphism on the core, and the languages without them have none.

## Tightness

**A whole language must fit one class.** The relation $x \vee y$ is 1-valid, dual Horn and bijunctive. The relation $\neg x \vee \neg y \vee \neg z$ is 0-valid and Horn. So each relation is in a class, but the language $\{x \vee y, \; \neg x \vee \neg y \vee \neg z\}$ is in none, and SAT of this language is NP-complete. The hypothesis of the theorem is about the language as a whole, not about its relations one at a time.

**No class can be dropped.** Each class contains a language that is in no other class, so the list of six is not redundant:

| Class | A language in this class only |
|---|---|
| 0-valid | $\{000, 011, 101\}$ |
| 1-valid | $\{001, 010, 111\}$ |
| Horn | $\{0\}$, $\{1\}$ and $\neg x \vee \neg y \vee z$ |
| dual Horn | $\{0\}$, $\{1\}$ and $\neg x \vee y \vee z$ |
| bijunctive | $\{0\}$, $\{1\}$, $x \vee y$ and $\neg x \vee \neg y$ |
| affine | $\{0\}$, $\{1\}$ and $x \oplus y \oplus z = 0$ |

**Constants matter.** The relation $\{000, 011, 101\}$ is only 0-valid. SAT of it is trivial, but SAT$_C$ of it is NP-complete by the second theorem.

**Domain size 2 matters.** On larger domains there are tractable languages with none of these six forms, for example linear equations modulo 3 or the relation $x \le y$ on $\{0, 1, 2\}$ combined with constants. Bulatov (2006) classified the domain of size 3, and the general case needed the [CSP dichotomy theorem](/csp-dichotomy-theorem/).

**Counting is different.** #2-SAT and #Horn-SAT are #P-complete although their decision versions are in P. For counting only the affine class remains easy ([counting CSP](/counting-csp/)).

## History

Post (1941) described all clones of Boolean operations, the structure behind the six classes, long before complexity theory. Polynomial algorithms for the special cases came from several sources: 2-SAT by Even, Itai and Shamir (1976) and in linear time by Aspvall, Plass and Tarjan (1979), Horn-SAT in linear time by Dowling and Gallier (1984), and linear equations by Gaussian elimination. Schaefer (1978) defined generalized satisfiability and proved the dichotomy, with and without constants, and also classified the quantified versions. Jeavons, Cohen and Gyssens (1997) restated the six classes as closure under operations, which led to the algebraic approach to CSPs. Creignou and Hermann (1996) classified counting, and Allender, Bauland, Immerman, Schnoor and Vollmer (2009) refined the polynomial side into complexity classes inside P. Feder and Vardi (1998) conjectured that the dichotomy extends to every finite domain, which Bulatov and Zhuk proved in 2017.

## References
