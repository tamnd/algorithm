---
tag: C3KFYD
kind: technique
slug: representative-families
name: Representative families
aliases:
- representative sets
area: complexity/parameterized-complexity
level: research
summary: "Keep only a small subfamily of partial solutions that can still be completed whenever any of them can. Families of p-sets shrink to binom(p+q, p) sets, so subset dynamic programs become FPT."
prereqs: [fixed-parameter-tractable, linear-matroid]
see_also: [color-coding, k-path-color-coding, divide-and-color, parameterized-longest-path, graph-motif, parameterized-hitting-set, matroid, uniform-matroid]
sources:
  - paper: doi:10.1145/2886094
    title: "Fedor V. Fomin, Daniel Lokshtanov, Fahad Panolan and Saket Saurabh, Efficient computation of representative families with applications in parameterized and exact algorithms, Journal of the ACM 63(4), article 29 (2016)"
    locator: the fast computation of representative families for linear and uniform matroids, and the deterministic k-path algorithm in time 2.619^k n^O(1)
  - paper: doi:10.1137/1.9781611973402.10
    title: "Fedor V. Fomin, Daniel Lokshtanov and Saket Saurabh, Efficient computation of representative sets with applications in parameterized and exact algorithms, Proceedings of the 25th ACM-SIAM Symposium on Discrete Algorithms (SODA 2014)"
    locator: the conference version, with a deterministic k-path algorithm in time 2.851^k n^O(1)
  - paper: doi:10.1016/j.tcs.2009.07.027
    title: "Daniel Marx, A parameterized view on matroid optimization problems, Theoretical Computer Science 410(44), 4471-4479 (2009)"
    locator: an algorithm that computes representative sets in linear matroids, and its use for parameterized problems
  - paper: doi:10.1007/bf01904851
    title: "Béla Bollobás, On generalized graphs, Acta Mathematica Academiae Scientiarum Hungaricae 16(3-4), 447-452 (1965)"
    locator: the set-pair inequality that gives the size bound binom(p+q, p)
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 12, Matroids (Section 12.3, Representative sets, and the applications to paths that follow)
---

Representative families make dynamic programming over subsets smaller without losing any answer. A dynamic program that builds a solution of $k$ elements step by step must often keep every *partial* solution, because it cannot tell which of them will fit with the rest. After $p$ steps there can be about $n^p$ of them. A *$q$-representative* subfamily keeps only a few: for every set $Y$ of at most $q$ elements that could complete a partial solution, it keeps at least one partial solution that is disjoint from $Y$. A theorem of Bollobás (1965) says that a family of $p$-element sets always has a $q$-representative subfamily of at most $\binom{p+q}{p}$ sets, a number that does not depend on $n$. Marx (2009) and then Fomin, Lokshtanov, Panolan and Saurabh (2014, 2016) showed how to compute such subfamilies quickly, with linear algebra over a matroid. The parameter is the solution size $k$, and the result is a *deterministic* [fixed-parameter tractable](/fixed-parameter-tractable/) algorithm, such as $k$-path in time $2.619^k n^{O(1)}$.

## In plain words

You build a team of $k$ people one person at a time. After a few steps you have many partial teams. You cannot keep them all, but you also cannot throw one away at random: later you may need exactly the people it does not use.

So you keep a small set of partial teams with one promise. Whatever group of people the rest of the team will need, at least one kept partial team avoids all of them. Then you never lose a full team.

The surprise is that this small set exists and its size depends only on the team size, not on the number of people. You can also compute it quickly. So the search keeps few partial teams at each step.

## When it applies

- A solution is a set of $k$ elements from a ground set $U$, and a dynamic program builds it by adding one element (or a few) at a time.
- A partial solution $X$ with $p$ elements has a *state* $s$, such as the last vertex of a path. Whether $X$ can be completed by a set $Y$ of the remaining elements depends only on the state $s$, on $Y$, and on the condition $X \cap Y = \emptyset$.
- The parameter is $k$. The method gives a deterministic algorithm with time $c^k n^{O(1)}$, where [color coding](/color-coding/) gives a randomized one or a deterministic one with extra factors.
- More generally, the condition "disjoint" can be "independent in a [matroid](/matroid/)": $X \cup Y$ is independent and $X \cap Y = \emptyset$. Then the matroid must be [linear](/linear-matroid/), with a known representation.

## The template

For a family $\mathcal{S}$ of $p$-element subsets of $U$, a subfamily $\widehat{\mathcal{S}} \subseteq \mathcal{S}$ *$q$-represents* $\mathcal{S}$ if for every $Y \subseteq U$ with $|Y| \le q$: if some $X \in \mathcal{S}$ has $X \cap Y = \emptyset$, then some $\widehat{X} \in \widehat{\mathcal{S}}$ has $\widehat{X} \cap Y = \emptyset$.

The template has three holes. START gives the partial solutions with no elements, by state. EXTEND$(F)$ adds one new element to each partial solution in every allowed way and records the new state. REPRESENT$(F, q)$ returns a $q$-representative subfamily of $F$.

```pseudo id=main
REP-DP(I, k)                          ▷ true if a solution with k elements exists
L1  F_0 ← START(I)
L2  for p ← 1 to k do
L3      F_p ← EXTEND(F_{p-1})
L4      for each state s do
L5          F_p[s] ← REPRESENT(F_p[s], k - p)
L6  return true if F_k[s] ≠ ∅ for some final state s, else false
```

The only change from the plain dynamic program is L4 and L5. The number $q = k - p$ is the number of elements still to add.

**Theorem (size).** Every family $\mathcal{S}$ of $p$-element sets has a $q$-representative subfamily with at most $\binom{p+q}{p}$ sets.

*Proof.* Take a subfamily $\widehat{\mathcal{S}}$ that $q$-represents $\mathcal{S}$ and is minimal: no set can be removed. For each $X \in \widehat{\mathcal{S}}$, removing $X$ breaks the property, so there is a $Y_X$ with $|Y_X| \le q$ that is disjoint from some set of $\mathcal{S}$ but meets every set of $\widehat{\mathcal{S}}$ other than $X$. Since $\widehat{\mathcal{S}}$ represents $\mathcal{S}$, $X$ itself is disjoint from $Y_X$. So the pairs $(X, Y_X)$ satisfy $X \cap Y_X = \emptyset$ and $X' \cap Y_X \ne \emptyset$ for $X' \ne X$. Bollobás's inequality for such set pairs gives $\sum_X 1/\binom{p + |Y_X|}{p} \le 1$, and each term is at least $1/\binom{p+q}{p}$. $\square$

The bound is tight. Let $|U| = p + q$ and let $\mathcal{S}$ be all $p$-subsets. For each $X$, the set $Y = U \setminus X$ is disjoint only from $X$, so no set can be removed.

**Lemma (transitivity).** If $\mathcal{A}$ $q$-represents $\mathcal{B}$ and $\mathcal{B}$ $q$-represents $\mathcal{C}$, then $\mathcal{A}$ $q$-represents $\mathcal{C}$.

*Proof.* If some set of $\mathcal{C}$ avoids $Y$, then some set of $\mathcal{B}$ avoids $Y$, and then some set of $\mathcal{A}$ avoids $Y$. $\square$

**Computation.** For a [linear matroid](/linear-matroid/) of rank $p + q$ given by a matrix, Fomin, Lokshtanov, Panolan and Saurabh compute a $q$-representative subfamily of a family of $t$ sets of size $p$ with at most $\binom{p+q}{p}$ sets in $O\left(\binom{p+q}{p} t p^{\omega} + t \binom{p+q}{q}^{\omega - 1}\right)$ field operations, where $\omega$ is the [matrix multiplication exponent](/matrix-multiplication-exponent/). Plain disjointness is the case of the [uniform matroid](/uniform-matroid/) of rank $p + q$, which has a representation by a [Vandermonde matrix](/vandermonde-matrix/) over a field with at least $|U|$ elements. For this case they also give a faster method with a trade-off: it returns a family somewhat larger than $\binom{p+q}{p}$ in less time.

## Classic examples

### k-path

The ground set is $V$, the state of a partial path is its last vertex $v$, and $P^p_v$ is the family of vertex sets of paths with $p$ vertices that end at $v$. EXTEND adds a neighbor $w \notin X$ of $v$, with the new state $w$. Without L5, $P^p_v$ can have $\binom{n}{p-1}$ sets.

*Claim.* After L5, $F_p[v] \subseteq P^p_v$ and $F_p[v]$ $(k - p)$-represents $P^p_v$.

*Proof by induction on $p$.* Let $X \in P^p_v$ and $|Y| \le k - p$ with $X \cap Y = \emptyset$. Remove $v$ from the path of $X$: the rest $X'$ is in $P^{p-1}_u$ for a neighbor $u$ of $v$. The set $Y' = Y \cup \{v\}$ has at most $k - p + 1$ elements and is disjoint from $X'$. By induction some $\widehat{X}' \in F_{p-1}[u]$ avoids $Y'$. Then $v \notin \widehat{X}'$, so EXTEND puts $\widehat{X}' \cup \{v\}$ into the family for $v$, and this set avoids $Y$. So the family after L3 represents $P^p_v$, and by transitivity so does its subfamily after L5. $\square$

At $p = k$ the claim with $q = 0$ says that $F_k[v]$ is not empty exactly when some path with $k$ vertices ends at $v$. Each $F_p[v]$ has at most $\binom{k}{p}$ sets, so the work is $2^{O(k)} n^{O(1)}$. With the fast trade-off for uniform matroids and a careful choice of the family sizes per step, the time is $2.619^k n^{O(1)}$ (the journal version; the SODA 2014 version had $2.851^k$). See [parameterized longest path](/parameterized-longest-path/) for the other algorithms.

The graph from [k-path by color coding](/k-path-color-coding/) has the vertices $a, \ldots, f$, the edges $ab, bc, cd, de, be, ef$, and $k = 4$. The table counts the pairs (end vertex, set) in all families, and in minimum representative subfamilies found by brute force:

| $p$ | $q = k - p$ | all partial paths | minimum representative | bound $\binom{k}{p}$ per end vertex |
|---|---|---|---|---|
| 1 | 3 | 6 | 6 | 4 |
| 2 | 2 | 12 | 12 | 6 |
| 3 | 1 | 16 | 12 | 4 |
| 4 | 0 | 14 | 6 | 1 |

The graph is too small for a large gain, but the last two steps already drop a quarter and then more than half of the sets. On large graphs the bound per end vertex stays at $\binom{k}{p}$ while the number of all partial paths grows with $n$.

### Kernel for d-hitting set

In [hitting set](/parameterized-hitting-set/) with sets of size $d$, the question is whether $k$ elements meet every set of a family $\mathcal{S}$. A set $Y$ of size $k$ is a hitting set exactly when no set of $\mathcal{S}$ avoids $Y$. If $\widehat{\mathcal{S}}$ $k$-represents $\mathcal{S}$, then some set of $\mathcal{S}$ avoids $Y$ exactly when some set of $\widehat{\mathcal{S}}$ does. So $(U, \widehat{\mathcal{S}}, k)$ is an equivalent instance with at most $\binom{k+d}{d}$ sets, a kernel with $O(k^d)$ sets for fixed $d$. The [sunflower lemma](/sunflower-lemma/) gives a kernel of the same order by a different route.

### Graph motif

Pinter, Shachnai and Zehavi (MFCS 2014) used representative families to solve [graph motif](/graph-motif/) deterministically in time $O^*(5.22^k)$, where $O^*$ hides factors polynomial in $n$. The partial solutions are connected vertex sets with their color counts, and the families are kept small per state as in the template.

## Variations

- *Matroids.* With a matroid $M$, $\widehat{\mathcal{S}}$ $q$-represents $\mathcal{S}$ if for every $Y$ of size at most $q$: if some $X \in \mathcal{S}$ has $X \cap Y = \emptyset$ and $X \cup Y$ independent, then some $\widehat{X}$ has the same property. Lovász proved the same $\binom{p+q}{p}$ bound for linear matroids, and Marx made it an algorithm.
- *Weights.* Each set has a weight, and for every $Y$ the subfamily keeps a set of the largest weight among those that avoid $Y$. This gives algorithms for weighted path and packing problems with the same size bound.
- *Size against time.* For the uniform matroid, a larger subfamily can be computed faster. Balancing the two over the steps of the dynamic program gives the best known deterministic bases for $k$-path.
- *Compare color coding and divide and color.* [Color coding](/color-coding/) and [divide and color](/divide-and-color/) are randomized and remove the randomness with hash families. Representative families are deterministic from the start.

## Pitfalls

- Using $q = k$ at every step. The correct $q$ is the number of elements still to add, $k - p$. A larger $q$ is correct but makes the families much larger.
- A state that forgets something the future needs. If the completion depends on more than the state and disjointness, for example on the first vertex of a path for a cycle, that information must go into the state.
- Representing the union over all states at once. The family for each state is represented separately; a set that ends at $u$ cannot stand in for one that ends at $v$.
- Forgetting the field. The uniform matroid needs a field with at least $|U|$ elements for its Vandermonde representation, and the arithmetic cost of that field goes into the time bound.
- Mixing up the unit. The bound $\binom{p+q}{p}$ counts sets, not bits; each set also has $p$ elements of $O(\log n)$ bits.

## Exercises

1. Let $U = \{1, 2, 3, 4, 5\}$ and $\mathcal{S} = \{12, 13, 14, 15, 23, 45\}$. Find a smallest 1-representative and a smallest 2-representative subfamily. (Answer: $\{12, 45\}$ of size 2, and $\{12, 13, 23, 45\}$ of size 4.)
2. In exercise 1, show that no set can be removed for $q = 3$. Is that a contradiction to the bound $\binom{5}{2} = 10$?
3. Show that if $\mathcal{A}$ $q$-represents $\mathcal{B}$, then $\mathcal{A}$ also $q'$-represents $\mathcal{B}$ for every $q' \le q$.
4. Give a family of $p$-sets for which every $q$-representative subfamily has $\binom{p+q}{p}$ sets, and explain why the minimal subfamily in the proof of the size theorem need not be unique.
5. Adapt the template to decide whether a graph has a cycle with exactly $k$ vertices. What is the state, and what does L6 check?

## References
