---
tag: DE61J9
kind: theorem
slug: chvatal-gomory-finite-convergence
name: Chvátal-Gomory finite convergence theorem
aliases:
- Chvátal's theorem
- Gomory's finiteness theorem
- finite Chvátal rank theorem
area: optimization/integer-programming
level: advanced
summary: Repeated Chvátal-Gomory closures reach the integer hull after finitely many rounds.
prereqs: [chvatal-closure, chvatal-gomory-cut, integer-hull, lp-duality]
see_also: [chvatal-closure, chvatal-gomory-cut, gomory-cutting-plane-algorithm, integer-hull, cutting-plane-method-integer-programming, totally-dual-integrality, lift-and-project, integer-feasibility]
sources:
  - paper: "Vašek Chvátal, Edmonds polytopes and a hierarchy of combinatorial problems, Discrete Mathematics 4 (1973), 305 to 337"
    locator: the theorem that finitely many rounds give the integer hull of a rational polytope
  - paper: "Alexander Schrijver, On cutting planes, Annals of Discrete Mathematics 9 (1980), 291 to 296"
    locator: the extension to rational polyhedra
  - paper: doi:10.1090/S0002-9904-1958-10224-4
    title: Ralph E. Gomory, Outline of an algorithm for integer solutions to linear programs, Bulletin of the American Mathematical Society 64(5), 1958
    locator: the finite cutting plane algorithm, the algorithmic form of the theorem
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Chapter 23 (cutting planes, the face lemma and finite convergence)
  - book: isbn:9783319110073
    title: Michele Conforti, Gérard Cornuéjols and Giacomo Zambelli, Integer Programming, Springer, 2014
    locator: Chapter 5 (the Chvátal rank is finite)
  - paper: "Friedrich Eisenbrand and Andreas S. Schulz, Bounds on the Chvátal rank of polytopes in the 0/1-cube, Combinatorica 23 (2003), 245 to 261"
    locator: the bound on the rank for 0/1 polytopes
  - paper: "William Cook, Collette R. Coullard and György Turán, On the complexity of cutting-plane proofs, Discrete Applied Mathematics 18 (1987), 25 to 38"
    locator: cutting plane proofs as a proof system
  - paper: doi:10.1007/BF01580858
    title: William Cook, Ravi Kannan and Alexander Schrijver, Chvátal closures for mixed integer programming problems, Mathematical Programming 47, 1990
    locator: the mixed-integer example with infinite split rank
---

## Statement

For a polyhedron $P$, let $P'$ be its [Chvátal closure](/chvatal-closure/), the set of points that satisfy all [Chvátal-Gomory cuts](/chvatal-gomory-cut/) of $P$. Let $P^{(0)} = P$, $P^{(k+1)} = (P^{(k)})'$, and let $P_I = \operatorname{conv}(P \cap \mathbb{Z}^n)$ be the [integer hull](/integer-hull/).

**Theorem (Chvátal 1973, Schrijver 1980).** For every rational polyhedron $P$, there is a finite $k$ with

$$P^{(k)} = P_I.$$

Chvátal proved this for rational polytopes, and Schrijver for all rational polyhedra. An equivalent form: every linear inequality valid for the integer points of $P$ can be derived from the inequalities of $P$ by finitely many steps of the form "take a nonnegative combination whose left side is integral, and round the right side down". In particular, if $P$ contains no integer point, there is such a derivation of $0 \le -1$.

## In plain words

Cutting planes add rules that keep every whole-number answer and remove some fractional points. One round of all possible rounding cuts gives a smaller region. The theorem says that if you repeat the rounds, you do not shrink forever: after a finite number of rounds, the region is exactly the hull of the whole-number points.

So the simple rounding trick is complete. Every true statement of the form "all whole-number answers satisfy this linear rule" can be proved by rounding steps alone. The number of rounds can be large, even for problems with two unknowns, so this is a guarantee of finiteness, not of speed.

## Proof

The full proof for rational polytopes is in the proof file below. Here is its plan.

1. **The closure is a rational polytope.** Each cut comes from multipliers $u \ge 0$. Writing $u = \lfloor u \rfloor + f$, the cut is the sum of a combination of the original rows and a cut with multipliers $f \in [0, 1)^m$. These give finitely many left sides, so finitely many cuts suffice, and the closure can be taken again.
2. **The face lemma.** For a face $F = \{x \in P : a^T x = \beta\}$, $F' = P' \cap F$. Given a cut of $F$, LP duality writes its left side as $A^T y + \lambda a$ with $y \ge 0$. Subtracting the integer multiple $\lfloor \lambda \rfloor a$ gives a cut of $P$ that implies the cut of $F$ on the hyperplane $a^T x = \beta$. Iterating, $P^{(k)} \cap F = F^{(k)}$.
3. **Descent by induction on dimension.** Take a facet $c^T x \le \delta$ of $P_I$ with integral data. The first closure gives $c^T x \le \gamma$ with $\gamma = \lfloor \max_P c^T x \rfloor$. If $\gamma > \delta$, the face $F$ of the current closure where $c^T x = \gamma$ has no integer points and lower dimension. By induction, some closure of $F$ is empty, so by the face lemma some later closure of $P$ satisfies $c^T x < \gamma$, and the next one $c^T x \le \gamma - 1$. After $\gamma - \delta$ such steps, the facet is valid. Doing this for each of the finitely many facets of $P_I$ gives $P^{(k)} \subseteq P_I$.
4. **Empty hulls.** If $P_I = \emptyset$, the same descent with a coordinate $x_j$ that is not constant on $P$ pushes $\max x_j$ below $\min_P x_j$, so some closure is empty.

Schrijver's proof for unbounded rational polyhedra follows the same plan, with extra care for the recession cone, which $P$ and $P_I$ share when $P_I \ne \emptyset$ by Meyer's theorem, and for the case where the affine hull of $P$ contains no integer point.

## Consequences

- **Finite cutting plane algorithms.** [Gomory's algorithm](/gomory-cutting-plane-algorithm/) with the lexicographic rule ends after finitely many cuts. Its proof is a version of the descent above, done one cut at a time.
- **Completeness of cutting plane proofs.** Every valid inequality for the integer points of a rational polytope, and every proof that a system has no integer solution, can be written as a cutting plane proof. This makes cutting planes a complete proof system for [integer feasibility](/integer-feasibility/) and for propositional logic, studied in proof complexity since Cook, Coullard and Turán (1987).
- **The Chvátal rank.** Each rational polyhedron has a finite rank, the least $k$ with $P^{(k)} = P_I$, and each valid inequality has a finite rank. Rank gives Chvátal's hierarchy of combinatorial problems.
- **A route to the hull.** Combined with the [face lemma](/chvatal-closure/), the theorem shows that cutting planes alone, without branching, can solve any pure integer program with rational data.

## Tightness

- **The rank is not bounded in terms of the dimension.** The triangle $\operatorname{conv}\{(0,0), (0,1), (t, 1/2)\}$ in the plane has rank at least $2t$ for each integer $t \ge 1$, as shown on the [Chvátal closure](/chvatal-closure/) page. So no bound depending only on $n$ exists for general polytopes.
- **For 0/1 polytopes the rank is bounded.** For a rational polytope in $[0,1]^n$, the rank is $O(n^2 \log n)$ (Eisenbrand and Schulz, 2003), and Rothvoss and Sanità (2013) gave 0/1 polytopes of rank $\Omega(n^2)$.
- **Rationality is needed.** For an irrational polyhedron, $P_I$ need not be a polyhedron, as the example on the [integer hull](/integer-hull/) page shows, so no finite number of rounds can produce it.
- **Mixed-integer sets do not converge.** For mixed-integer programs, the analogous split closure, which contains the [Gomory mixed-integer cuts](/gomory-mixed-integer-cut/), can need infinitely many rounds: Cook, Kannan and Schrijver (1990) gave a mixed-integer example in which no finite number of rounds of split cuts reaches the hull.

## History

Gomory (1958) gave the first finite cutting plane algorithm for pure integer programs, using cuts from the simplex tableau. Chvátal (1973) stated the rounding operation independently of any algorithm, proved that finitely many rounds give the integer hull of a rational polytope, and used the number of rounds to define a hierarchy of combinatorial problems. Schrijver (1980) extended the theorem to rational polyhedra and proved that the closure is a polyhedron. The name Chvátal-Gomory cut joins the two lines of work. Eisenbrand and Schulz (2003), and Rothvoss and Sanità (2013), gave tight bounds for the rank of 0/1 polytopes.

## References
