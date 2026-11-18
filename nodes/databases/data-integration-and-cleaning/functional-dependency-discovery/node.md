---
tag: 1TD1WN
kind: problem
slug: functional-dependency-discovery
name: Functional dependency discovery
aliases:
- FD discovery
- dependency mining
area: databases/data-integration-and-cleaning
level: advanced
summary: "Given one relation instance, list every minimal functional dependency X -> A that holds in it. The output can be exponential in the number of attributes."
model: word-ram
complexity:
  vars: {n: the number of tuples, m: the number of attributes}
  time: {worst: "O(m n 2^m)"}
prereqs: [functional-dependency, attribute-closure-algorithm]
see_also: [tane-algorithm, candidate-key, armstrongs-axioms, hitting-set, conditional-functional-dependency, denial-constraint, normalization, holoclean]
sources:
  - paper: "Yka Huhtala, Juha Kärkkäinen, Pasi Porkka and Hannu Toivonen, TANE: an efficient algorithm for discovering functional and approximate dependencies, The Computer Journal 42(2), 1999, pages 100 to 111"
    locator: "Section 1 (the problem, minimal dependencies, the g3 error of approximate dependencies, and the remark that the number of minimal dependencies can be exponential in the number of attributes), Section 2 (partitions)"
  - paper: "Heikki Mannila and Kari-Jouko Räihä, On the complexity of inferring functional dependencies, Discrete Applied Mathematics 40, 1992, pages 237 to 243"
    locator: the paper that Huhtala et al. (1999, Section 1) cite for the exponential number of minimal dependencies
  - paper: "Thorsten Papenbrock, Jens Ehrlich, Jannik Marten, Tommy Neubert, Jan-Peer Rudolph, Martin Schönberg, Jakob Zwiener and Felix Naumann, Functional dependency discovery: an experimental evaluation of seven algorithms, PVLDB 8(10), 2015, pages 1082 to 1093"
    locator: the classification of the algorithms into lattice traversal, difference and agree set, and dependency induction methods, and the measured run times and memory use of TANE, FUN, FD_Mine, DFD, Dep-Miner, FastFDs and FDEP
---

Functional dependency discovery asks for all [functional dependencies](/functional-dependency/) that hold in a given relation *instance*, not the ones that a designer declares for a schema. The answer is the set of minimal dependencies $X \to A$, from which [Armstrong's axioms](/armstrongs-axioms/) give all the others. This page states the problem, its size bounds and its reduction to hitting sets. The page [TANE](/tane-algorithm/) gives one algorithm for it in full: the levelwise lattice search with partitions. The other main family works from the pairs of rows that agree on some attributes and disagree on others.

## In plain words

You get a table and nobody tells you its rules. You want to find every rule of the form "if two rows have the same values in these columns, they also have the same value in that column". You want only the shortest such rules, because a longer rule follows from a shorter one. The rules describe this one table: a new row can break any of them. The hard part is that a table with a few dozen columns can have a huge number of short rules, so any method must sometimes do a huge amount of work just to write the answer down. Methods differ in what they count: groups of columns, or pairs of rows.

## Definition

**Input.** A relation instance $r$ with $n$ tuples over a set $R$ of $m$ attributes, under set semantics and with no nulls.

**Dependencies.** $X \to A$, with $X \subseteq R$ and $A \in R \setminus X$, *holds* in $r$ if any two tuples that agree on every attribute of $X$ also agree on $A$. It is *minimal* if it holds and no $Y \to A$ with $Y \subsetneq X$ holds. The empty left side is allowed: $\emptyset \to A$ holds when $A$ is constant in $r$.

**Output.** The set of all minimal dependencies that hold in $r$. Every dependency that holds in $r$ follows from this set by augmentation, so it is a cover of all of them.

**Agree sets.** For two tuples $t \ne u$, the *agree set* is $\mathrm{ag}(t, u) = \{ B \in R : t[B] = u[B] \}$. Then $X \to A$ holds if and only if $X \not\subseteq \mathrm{ag}(t, u)$ for every pair with $t[A] \ne u[A]$.

## Variants

- **Approximate dependencies.** Allow a small error. The usual measure is $g_3$: the least fraction of tuples that must be deleted for $X \to A$ to hold. The task is to list the minimal $X \to A$ with $g_3 \le \varepsilon$. These dependencies are not closed under Armstrong's axioms.
- **Keys.** A [candidate key](/candidate-key/) is a minimal set $X$ with $X \to A$ for every $A$. Finding all minimal keys of an instance is the special case of unique column combinations.
- **Conditional dependencies.** A [conditional functional dependency](/conditional-functional-dependency/) holds only on the tuples that match a pattern. [Denial constraints](/denial-constraint/) generalize both and are mined by similar methods.
- **Fixed right side.** List the minimal left sides of one attribute $A$ only. This is the core step of most algorithms.

## Examples

**A small instance.** Over $A, B, C, D$ take the tuples $(1, a, x, 1)$, $(1, a, y, 2)$, $(2, b, x, 1)$, $(2, b, y, 3)$ and $(3, b, x, 1)$. The minimal dependencies are $A \to B$, $D \to C$, $AC \to D$ and $BC \to D$. For the right side $D$: the pairs of tuples that differ on $D$ are (1, 2), (1, 4), (2, 3), (2, 4), (2, 5), (3, 4) and (4, 5), with agree sets $AB$, $\emptyset$, $\emptyset$, $C$, $\emptyset$, $AB$ and $B$. A left side for $D$ must leave each of these agree sets, so it must contain $C$ (from the pairs that agree on $AB$) and one of $A$ or $B$ (from the pair that agrees on $C$). The smallest such sets are $AC$ and $BC$. The page [TANE](/tane-algorithm/) finds the same four dependencies on the same instance level by level.

**An instance with many dependencies.** Take attributes $A_1, B_1, \ldots, A_k, B_k$ and $C$, so $m = 2k + 1$, and $k + 1$ tuples. Tuple 0 is all zeros with $C = 0$. Tuple $i$, for $i = 1, \ldots, k$, has $A_i = B_i = 1$, every other $A_j$ and $B_j$ equal to 0, and $C = i$. For $k = 2$ the minimal dependencies with the right side $C$ are $A_1 A_2 \to C$, $A_1 B_2 \to C$, $B_1 A_2 \to C$ and $B_1 B_2 \to C$.

## Known algorithms

- **Brute force.** For each $A$ and each $X \subseteq R \setminus \{A\}$, test $X \to A$ by grouping the tuples on $X$ with a hash table, and keep the minimal ones. This takes $O(m n 2^m)$ expected time.
- **Lattice traversal.** [TANE](/tane-algorithm/) visits the attribute sets level by level and tests each candidate with stripped partitions. FUN and FD_Mine also go level by level with other pruning rules, and DFD goes depth first. These methods are linear in $n$ and exponential in $m$.
- **Difference and agree sets.** Dep-Miner and FastFDs compute the agree sets of all pairs of tuples, then find the minimal left sides as minimal hitting sets (see Reductions). They are quadratic in $n$ and do better than lattice methods when $m$ is large and $n$ is small.
- **Dependency induction.** FDEP starts from the most general dependencies and specializes them with each pair of tuples that violates one.

Papenbrock et al. (2015) implemented all seven of these algorithms in one framework and measured them on the same data sets. Their results are measurements on those data sets, not bounds.

## Bounds

**The output can be exponential.** In the second example, $X \subseteq R \setminus \{C\}$ determines $C$ if and only if $X$ holds at least one attribute of each pair $\{A_i, B_i\}$. *Proof.* All values of $C$ differ, so $X \to C$ holds if and only if no two tuples agree on $X$. Tuples 0 and $i$ agree exactly on the attributes outside $\{A_i, B_i\}$, and tuples $i$ and $j$ agree on a subset of those. So two tuples agree on $X$ if and only if $X$ misses some pair. The minimal such $X$ pick one attribute from each pair, so there are $2^k = 2^{(m-1)/2}$ minimal dependencies with $k + 1$ tuples. Any algorithm must write them all, so the worst case time is $\Omega(2^{(m-1)/2})$ even for $n = O(m)$. The source of Huhtala et al. for the same remark is Mannila and Räihä (1992).

**The output is at most about $2^m$.** For a fixed $A$, no minimal left side is a subset of another, so the left sides form an antichain of subsets of $R \setminus \{A\}$. By Sperner's theorem there are at most $\binom{m-1}{\lfloor (m-1)/2 \rfloor}$ of them, and at most $m \binom{m-1}{\lfloor (m-1)/2 \rfloor} = O(2^m \sqrt{m})$ minimal dependencies in total.

**Per test.** One test of $X \to A$ needs $\Theta(n)$ time to read the two columns, and partition methods reach $O(n)$ for each lattice node.

## Reductions

**To minimal hitting sets.** Fix $A$. For each pair of tuples with $t[A] \ne u[A]$, let the *difference set* be $R \setminus \mathrm{ag}(t, u) \setminus \{A\}$. By the agree set condition, $X \to A$ holds if and only if $X$ meets every difference set. So the minimal left sides of $A$ are exactly the minimal [hitting sets](/hitting-set/) (minimal transversals) of the family of difference sets, and only the minimal difference sets matter. The first example shows this for $A = D$. This is the reduction that the agree set methods use.

**Keys.** $X$ is a superkey if and only if no two tuples agree on $X$, that is, $X$ meets $R \setminus \mathrm{ag}(t, u)$ for every pair. The minimal keys are the minimal hitting sets of these complements; the second example is the case where they are the $2^k$ choices of one attribute per pair.

**From the output to closures.** Once the minimal dependencies are known, the [attribute closure algorithm](/attribute-closure-algorithm/) decides any implied dependency without the data.

## Applications

- **Data profiling.** Find keys and dependencies of a table that has no declared schema, such as an exported file or a data lake table.
- **Schema design.** The dependencies suggest a decomposition in [normalization](/normalization/), after a person confirms which ones are real rules and which hold only by chance.
- **Data cleaning.** Approximate dependencies point at the few tuples that break a rule, and the rules become input to repair systems such as [HoloClean](/holoclean/).
- **Query optimization.** Known dependencies let an optimizer drop redundant grouping columns and estimate the sizes of joins and groups better.

## References
