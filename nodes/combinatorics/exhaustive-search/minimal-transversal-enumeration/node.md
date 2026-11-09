---
tag: XDSJ0X
kind: problem
slug: minimal-transversal-enumeration
name: Enumeration of minimal transversals
aliases:
- minimal hitting set enumeration
- hypergraph transversal enumeration
- hypergraph dualization
- monotone dualization
area: combinatorics/exhaustive-search
level: research
summary: List all minimal sets that intersect every hyperedge of a hypergraph.
prereqs: [hypergraph, hitting-set, enumeration-problem]
see_also: [fredman-khachiyan-algorithm, maximal-independent-set-enumeration, output-sensitive-enumeration, hitting-set, hypergraph, tsukiyama-algorithm, vertex-cover, enumeration-problem]
sources:
  - paper: "Thomas Eiter and Georg Gottlob, Identifying the minimal transversals of a hypergraph and related problems, SIAM Journal on Computing 24(6), 1995, 1278 to 1304"
    locator: the problem Trans-Enum and its decision form Trans-Hyp, their equivalence, the many problems in logic, databases and artificial intelligence that reduce to them, and the special classes that are solved in output-polynomial time
  - paper: doi:10.1006/jagm.1996.0062
    title: Michael L. Fredman and Leonid Khachiyan, On the complexity of dualization of monotone disjunctive normal forms, Journal of Algorithms 21(3), 1996, 618 to 628
    locator: the quasi-polynomial duality test, which lists the minimal transversals in incremental quasi-polynomial time
  - book: "Claude Berge, Hypergraphs: Combinatorics of Finite Sets, North-Holland, 1989"
    locator: the chapter on transversals, the identity Tr(Tr(H)) = H for simple hypergraphs, and the method that adds the edges one at a time
  - paper: "Thomas Eiter, Kazuhisa Makino and Georg Gottlob, Computational aspects of monotone dualization: a brief survey, Discrete Applied Mathematics 156(11), 2008, 2035 to 2049"
    locator: the survey of the known algorithms, the special classes, and the open question of output-polynomial time
  - paper: "Keisuke Murakami and Takeaki Uno, Efficient algorithms for dualizing large-scale hypergraphs, Discrete Applied Mathematics 170, 2014, 83 to 94"
    locator: the practical search methods for minimal transversals and their experiments on large hypergraphs
---

A *transversal*, or *hitting set*, of a hypergraph is a set of vertices that meets every edge, and it is *minimal* when no proper subset is a transversal. The enumeration problem asks for the list $\mathrm{Tr}(H)$ of all minimal transversals of a hypergraph $H$. It is the same problem as the *dualization* of a monotone Boolean function, and dozens of problems in logic, databases, data mining and diagnosis reduce to it. Its exact complexity is a famous open question: no algorithm is known that runs in time polynomial in the size of the input and the output, but the [Fredman-Khachiyan algorithm](/fredman-khachiyan-algorithm/) solves it in quasi-polynomial time, so it is unlikely to be hard.

## In plain words

You have several groups of people, and the groups may overlap. You want to pick a team with at least one member from every group. A team is minimal if every member is needed: drop anyone, and some group has nobody on the team.

The task is to list every minimal team. There can be very many. With five pairs of people, for example, there are 32, one for each way to pick one person from each pair.

A good method should take time that depends on the size of the groups and on the number of teams it lists. Nobody knows such a method that is truly fast in every case, but there is one that comes close.

## Definition

A *hypergraph* $H$ on a finite vertex set $V$ is a family of subsets of $V$, its *edges*. A set $T \subseteq V$ is a *transversal* of $H$ if $T \cap E \ne \emptyset$ for every edge $E$. It is a *minimal transversal* if no proper subset of $T$ is a transversal. The family of minimal transversals is the *transversal hypergraph* or *blocker* $\mathrm{Tr}(H)$.

- **Enumeration (Trans-Enum).** Given $H$, output every set of $\mathrm{Tr}(H)$ exactly once.
- **Decision (Trans-Hyp).** Given $H$ and a family $G$, decide whether $G = \mathrm{Tr}(H)$.

Since $\mathrm{Tr}(H)$ can be exponentially larger than $H$, an algorithm is measured as an [output-sensitive](/output-sensitive-enumeration/) one, by its time in terms of the input size $N$ and the output size $M$. The two forms are equivalent: an output-polynomial algorithm for one gives one for the other.

In Boolean terms, let $f$ be the monotone DNF whose terms are the edges of $H$. Its dual $f^d(x) = \lnot f(\bar{x})$ has the minimal transversals of $H$ as its minimal terms. So listing $\mathrm{Tr}(H)$ is the same as computing the irredundant DNF of $f^d$, the problem of *monotone dualization*.

## Variants

- **Graphs.** When every edge has two vertices, the minimal transversals are the minimal vertex covers, the complements of the maximal independent sets. This case is solved with polynomial delay; see [maximal independent set enumeration](/maximal-independent-set-enumeration/).
- **Bounded edge size.** When every edge has at most $k$ vertices, for fixed $k$, output-polynomial algorithms are known.
- **Other special classes.** Acyclic hypergraphs, hypergraphs of bounded degree, and several other classes have output-polynomial or polynomial-delay algorithms.
- **Minimal transversals of bounded size.** List only the minimal transversals with at most $k$ vertices. This is the parameterized setting of [hitting set](/hitting-set/).
- **Weighted and minimum forms.** Finding one minimum transversal is the NP-hard hitting set problem, a different question from listing all minimal ones.
- **Counting.** Count $|\mathrm{Tr}(H)|$ without listing. This is #P-hard already for graphs.

## Examples

**Two disjoint edges.** For $H = \{ab, cd\}$, a transversal needs one of $a, b$ and one of $c, d$, so $\mathrm{Tr}(H) = \{ac, ad, bc, bd\}$. Applying $\mathrm{Tr}$ again gives back $\{ab, cd\}$.

**A matching.** If $H$ has $k$ disjoint edges with two vertices each, then $\mathrm{Tr}(H)$ has $2^k$ sets, one choice from each edge. So the output can be exponential in the input.

**A triangle.** For the edges $ab, bc, ca$, the minimal transversals are $ab$, $ac$ and $bc$: any two vertices meet all three edges, and one vertex misses the edge opposite to it.

**A path.** For the edges $ab, bc, cd$, $\mathrm{Tr}(H) = \{ac, bc, bd\}$. The set $\{a, c, d\}$ is a transversal but not minimal, since $\{a, c\}$ is one too.

**The Fano plane.** The 7 lines of the Fano plane, each with 3 points, form a hypergraph whose minimal transversals are exactly the 7 lines again. So $\mathrm{Tr}(H) = H$.

**A non-example.** For $H = \{ab, cd\}$, the set $\{a, b\}$ is not a transversal, since it misses the edge $cd$.

## Known algorithms

- **Berge's method.** Add the edges one at a time. After edge $E$, the new minimal transversals are the minimal sets among $T \cup \{v\}$ for $T$ in the old list and $v \in E$. It is simple and often fast, but the list after some prefix of edges can be much larger than the final output, so it is not output-polynomial.
- **Fredman and Khachiyan (1996).** A duality test that decides $G = \mathrm{Tr}(H)$, or finds a new minimal transversal, in time $m^{O(\log^2 m)}$, where $m = |H| + |G|$, times a polynomial in $|V|$. Calling it once per output gives incremental quasi-polynomial time. A refined version runs in $m^{o(\log m)}$. See the [Fredman-Khachiyan algorithm](/fredman-khachiyan-algorithm/).
- **Graphs.** The [Tsukiyama algorithm](/tsukiyama-algorithm/) and its successors list the maximal independent sets, and so the minimal vertex covers, with polynomial delay.
- **Practical search.** Depth-first methods such as those of Kavvadias and Stavropoulos, and the MMCS and RS methods of Murakami and Uno, build transversals vertex by vertex with strong pruning. They handle large hypergraphs from data mining well, though no output-polynomial bound is proven for them.

## Bounds

**Size of the output.** On $n$ vertices, $\mathrm{Tr}$ is a bijection on the *simple* hypergraphs, those in which no edge contains another, with $\mathrm{Tr}(\mathrm{Tr}(H)) = H$. So the largest possible $|\mathrm{Tr}(H)|$ is the size of the largest such family, which is $\binom{n}{\lfloor n/2 \rfloor}$ by Sperner's theorem. It is reached by the hypergraph of all sets of size $n - \lfloor n/2 \rfloor + 1$. For graphs the number is at most $3^{n/3}$, by the bound of Moon and Moser.

**Complexity of the decision form.** Trans-Hyp is in co-NP: a "no" answer has a short proof, a set that is a transversal and contains no member of $G$, or a member of $G$ that is not a minimal transversal. The Fredman-Khachiyan test puts it in quasi-polynomial time, so it is not co-NP-complete unless every problem in NP has quasi-polynomial algorithms. Later work showed that it needs only $O(\log^2 N)$ nondeterministic guesses. Whether it is in polynomial time is open.

**Why flashlight search fails.** The usual way to get polynomial delay is to ask, at each step, whether a partial solution extends to a full one. For minimal transversals, deciding whether a given set is a subset of some minimal transversal is NP-complete, so this simple approach does not work here.

**Counting.** Counting minimal transversals is #P-hard, since it is hard already for the minimal vertex covers of graphs.

## Reductions

- **Dualization.** As above, the problem is the dualization of a monotone DNF, and also the conversion of a monotone CNF into its irredundant DNF.
- **Maximal independent sets of a hypergraph.** $T$ is a minimal transversal if and only if $V \setminus T$ is a maximal set that contains no edge. So the two lists are complements of each other.
- **Frequent sets.** In data mining, the minimal infrequent sets are the minimal transversals of the complements of the maximal frequent sets. So the border between frequent and infrequent sets is found by dualization.
- **Keys and dependencies.** Finding all minimal keys of a relation, or all functional dependencies from data, reduces to listing minimal transversals of a hypergraph built from pairs of rows.
- **Diagnosis.** In model-based diagnosis, the minimal diagnoses are the minimal transversals of the family of conflict sets.

## Applications

- **Model-based diagnosis.** Reiter's theory finds the minimal sets of faulty components that explain an observed fault as minimal hitting sets of the conflicts.
- **Data mining.** Algorithms for frequent itemsets, association rules and the borders of version spaces use dualization to switch between a family and its blocker.
- **Databases.** Discovery of keys and functional dependencies, and the design of Armstrong relations.
- **Systems biology.** Minimal cut sets, which block every pathway that produces a target, are minimal transversals of the set of pathways.
- **Logic and learning.** Learning monotone Boolean functions with membership queries, computing prime implicants, and finding Horn approximations all reduce to or use dualization.

## References
