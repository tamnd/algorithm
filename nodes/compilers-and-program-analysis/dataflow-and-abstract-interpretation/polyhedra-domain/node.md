---
tag: FC44XR
kind: definition
slug: polyhedra-domain
name: Convex polyhedra abstract domain
aliases:
- Cousot-Halbwachs polyhedra
- linear relation analysis
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: advanced
summary: A relational domain of conjunctions of linear inequalities between variables, precise but exponential in the worst case.
prereqs: [abstract-domain, widening-operator, minkowski-weyl-theorem]
see_also: [octagon-domain, interval-domain, fourier-motzkin-elimination, convex-hull, galois-connection, narrowing-operator, reduced-product, weak-topological-ordering]
sources:
  - paper: doi:10.1145/512760.512770
    title: "Patrick Cousot and Nicolas Halbwachs, Automatic discovery of linear restraints among variables of a program, POPL 1978, pages 84 to 96"
    locator: the polyhedra domain, the convex hull as join, the transfer functions for linear assignments and tests, and the widening that keeps the stable constraints
  - paper: "Nicolas Halbwachs, Détermination automatique de relations linéaires vérifiées par les variables d'un programme, thèse de troisième cycle, Université scientifique et médicale de Grenoble, 1979"
    locator: the standard widening, with the constraints of the new polyhedron that can replace a constraint of the old one, and the use of the double description
  - paper: "T. S. Motzkin, H. Raiffa, G. L. Thompson and R. M. Thrall, The double description method, in H. W. Kuhn and A. W. Tucker (eds.), Contributions to the Theory of Games II, Annals of Mathematics Studies 28, Princeton University Press, 1953, pages 51 to 73"
    locator: the method that keeps a cone both as a system of inequalities and as a set of generating rays, and adds one inequality at a time
  - paper: doi:10.1016/j.scico.2005.02.003
    title: "Roberto Bagnara, Patricia M. Hill, Elisa Ricci and Enea Zaffanella, Precise widening operators for convex polyhedra, Science of Computer Programming 58(1-2), 2005, pages 28 to 56"
    locator: the statement of the standard widening, its termination, and a family of widenings that are never less precise
  - book: isbn:9780262043410
    title: Xavier Rival and Kwangkeun Yi, Introduction to Static Analysis, An Abstract Interpretation Perspective, MIT Press, 2020
    locator: Chapter 3 (relational abstract domains for numeric states, among them octagons and convex polyhedra)
---

The polyhedra domain describes the numeric names of a program by a conjunction of linear inequalities $a_1 x_1 + \cdots + a_v x_v \le b$ with rational coefficients, such as $y = 2x$ and $0 \le x \le 10$. The set of points that satisfy them is a convex polyhedron. It is the most precise of the classic numeric domains: it keeps every linear relation that holds on all paths through a join. Patrick Cousot and Nicolas Halbwachs introduced it in 1978, and it is also called linear relation analysis. Its cost is the price. A polyhedron is kept in two forms at once, as inequalities and as generators, and the size of either form can be exponential in the number of names $v$.

## Definition

The order is the Cousot order: lower is more precise, and $\bot$ means that no state reaches the point. The dataflow pages that use Kildall's convention turn it round. The framework is on the [abstract domain](/abstract-domain/) page.

**Polyhedra.** A *convex polyhedron* in $\mathbb{Q}^v$ is a set $P = \{\, x : Ax \le b \,\}$ for a rational matrix $A$ and vector $b$. An equality is a pair of inequalities. The elements of the domain are the polyhedra, with the empty one as $\bot$ and $\mathbb{Q}^v$ as $\top$. For a program over integers, $\gamma(P) = P \cap \mathbb{Z}^v$. This is sound, but integer facts that need rounding, such as $2x = 1$ being impossible, are lost unless the analyzer adds them.

**The double description.** By the [Minkowski-Weyl theorem](/minkowski-weyl-theorem/), every polyhedron also has a *generator* form

$$ P = \Bigl\{\, \sum_i \lambda_i p_i + \sum_j \mu_j r_j + \sum_k \nu_k \ell_k \ :\ \lambda_i, \mu_j \ge 0,\ \textstyle\sum_i \lambda_i = 1,\ \nu_k \in \mathbb{Q} \,\Bigr\}, $$

with points $p_i$, rays $r_j$ and lines $\ell_k$. A *double description* of $P$ is a pair (a constraint system $C$, a generator system $G$) that describe the same polyhedron. The name and the method come from Motzkin, Raiffa, Thompson and Thrall (1953). Each operation uses the form in which it is easy, and the conversion from one form to the other is done by Chernikova's algorithm, which adds one constraint (or one generator) at a time and keeps both forms in step. A system is *minimal* when no constraint (or generator) can be dropped; for a polyhedron of full dimension the minimal constraint system is unique up to scaling, one inequality per facet.

**Order, meet and join.**

- $P \sqsubseteq Q$ when every generator of $P$ satisfies every constraint of $Q$: points satisfy them, rays $r$ satisfy $a \cdot r \le 0$, and lines $\ell$ satisfy $a \cdot \ell = 0$. This is exact inclusion.
- $P \sqcap Q$ is the union of the two constraint systems. It is exact.
- $P \sqcup Q$ is the union of the two generator systems. It gives the closed [convex hull](/convex-hull/) of $P \cup Q$, the least polyhedron that contains both. A union of two polyhedra is not convex in general, so the join loses precision, but it is the best that the domain can do.

**Abstraction.** There is no best abstraction in general. The disk $x^2 + y^2 \le 1$ is contained in polyhedra that come closer and closer to it, and no least one exists; the [Galois connection](/galois-connection/) page shows this. So the domain is used with a concretization only, and soundness is proved operation by operation.

**Transfer functions.**

- *Guard* $a \cdot x \le b$: add the constraint (a meet). Exact. A strict guard $a \cdot x < b$ over integer coefficients and integer names is the same as $a \cdot x \le b - 1$. A nonlinear guard is ignored or replaced by a linear consequence.
- *Forget* $x_i$: add the line $e_i$ to the generators. On the constraint side this is [Fourier-Motzkin elimination](/fourier-motzkin-elimination/) of $x_i$, which can square the number of constraints in one step.
- *Assignment* $x_i \leftarrow a \cdot x + c$ with $a_i \ne 0$: the map is invertible, so substitute $x_i = (x_i' - \sum_{j \ne i} a_j x_j - c)/a_i$ in the constraints, or apply the map to the generators. Exact.
- *Assignment* $x_i \leftarrow a \cdot x + c$ with $a_i = 0$: forget $x_i$, then add the equality $x_i = a \cdot x + c$. Exact.
- *Any other assignment*: forget $x_i$, then add what is known, for example interval bounds. Sound.

**Widening.** The domain has infinite ascending chains, so it needs a [widening](/widening-operator/). Let $C_P$ be a minimal constraint system of $P$. The *standard widening* of Cousot and Halbwachs, as completed by Halbwachs (1979), is

$$ P \mathbin{\nabla} Q = \{\, c \in C_P : Q \text{ satisfies } c \,\} \ \cup\ \{\, c \in C_Q : \text{some } c' \in C_P \text{ can be replaced by } c \text{ without changing } P \,\}. $$

The first part keeps the constraints of $P$ that are stable. The second part was added because a polyhedron of lower dimension has many minimal systems: its equalities can be written in many ways, and the first part alone would give results that depend on the choice. A strict step either raises the dimension of the polyhedron or drops at least one constraint, which can happen only finitely often, so the widened chain stops. Bagnara, Hill, Ricci and Zaffanella (2005) define widenings that are never less precise than this one. Delayed widening (join for the first few steps) and widening with thresholds are often used with polyhedra.

**Cost.** Meet, guard and the constraint side of inclusion are linear in the size of the constraint system; join and forget are linear in the size of the generator system. Inclusion costs $O(|G_P| \cdot |C_Q| \cdot v)$. The conversion between the forms is the expensive part, and so is keeping the systems minimal. Each form can be exponential in $v$ while the other is small, as the examples show. The total cost of an analysis is therefore exponential in the worst case, and in practice analyzers split the names into small groups that are known to be related, and keep one polyhedron per group.

## Examples and non-examples

**A loop with a linear relation.**

```
entry:
  x = 0
  y = 0
  jump head
head:
  t = x < 10
  br t body exit
body:
  x = x + 1
  y = y + 2
  jump head
exit:
  ret y
```

Write $P_k$ for the value at `head` after $k$ steps and $F$ for the value computed from `entry` and the end of `body`.

| step | value at `head` | how |
|---|---|---|
| 0 | the point $(0, 0)$ | from `entry` |
| 1, before widening | the segment $y = 2x$, $0 \le x \le 1$ | join of $(0, 0)$ and $(1, 2)$ |
| 1, after widening | $y = 2x$, $x \ge 0$ | standard widening, see below |
| 2 | stable: $F$ gives $y = 2x$, $0 \le x \le 10$ | the guard $x \le 9$, then $+1$ and $+2$ |
| exit | $y = 2x$, $x \ge 10$ | the guard $x \ge 10$ |
| exit, after one decreasing step | $x = 10$, $y = 20$ | `head` becomes $F$, so $0 \le x \le 10$ |

At step 1, $P_0$ is a point. If its minimal system is written as $x \le 0$, $x \ge 0$, $y \le 0$, $y \ge 0$, the first part of the widening keeps only $x \ge 0$ and $y \ge 0$. The second part adds $y \le 2x$ and $y \ge 2x$ from the segment, because each can replace $y \le 0$ or $y \ge 0$ in the system of the point without changing it. So the standard widening keeps $y = 2x$. With the first part alone, the head would become the quarter plane $x \ge 0$, $y \ge 0$, and the exit would get only $x = 10$ and $y \ge 2$ after one decreasing step (a [narrowing](/narrowing-operator/) of the simplest kind). A delayed widening, which joins once before it widens, also keeps $y = 2x$, since the segment of step 1 has the stable equality $y = 2x$ in every minimal system. Neither intervals nor octagons can express $y = 2x$; [octagons](/octagon-domain/) would keep only bounds such as $y - x \ge 0$.

**The cross-polytope: exponentially many constraints.** Join the $2v$ points $\pm e_1, \ldots, \pm e_v$. The result is the cross-polytope

$$ X_v = \{\, x : |x_1| + \cdots + |x_v| \le 1 \,\} = \{\, x : s \cdot x \le 1 \text{ for every } s \in \{-1, 1\}^v \,\}. $$

Each of the $2^v$ inequalities $s \cdot x \le 1$ defines a facet: it holds with equality at the $v$ points $s_1 e_1, \ldots, s_v e_v$, which are affinely independent, and $X_v$ has full dimension. Different sign vectors give different facets. So the minimal constraint system has exactly $2^v$ rows, while the generator system has $2v$ points. An analysis that joins $2v$ simple states and then applies one guard must convert to constraints and write $2^v$ rows.

**The hypercube: exponentially many generators.** The box $[0, 1]^v$ has $2v$ constraints and $2^v$ vertices, each a point of every generator system. An analysis that adds $2v$ interval guards and then joins the result with one point must write $2^v$ points. Together the two families show that neither form is small in the worst case, and that converting between them takes exponential time just to write the output.

**Not a polyhedron.** The set $\{\, (x, y) : y = x^2 \,\}$ and the set $\{\, x : x \text{ even} \,\}$ have no exact polyhedral description. The first one is not convex; its best linear facts on a bounded range come from the join of sample points. The second needs a congruence domain, which is often combined with polyhedra by a [reduced product](/reduced-product/).

**Not a join.** Taking the union of the two constraint systems as the join gives the intersection, which is unsound. Taking only the constraints common to both systems (as written) is sound but depends on how the constraints are written: $x \le 1$ in one state and $2x \le 2$ in the other would be dropped.

## Related definitions

- [Interval domain](/interval-domain/) and [octagon domain](/octagon-domain/): the polyhedra whose constraints have one name, or two names with coefficients $\pm 1$. They cost polynomial time per operation.
- [Minkowski-Weyl theorem](/minkowski-weyl-theorem/): every polyhedron is both an intersection of half-spaces and the sum of a polytope and a cone, the fact behind the double description.
- [Fourier-Motzkin elimination](/fourier-motzkin-elimination/): projection on the constraint side, used to forget a name.
- [Convex hull](/convex-hull/): the join of the domain.
- [Widening operator](/widening-operator/) and [narrowing operator](/narrowing-operator/): the general definitions behind the standard widening.

## References
