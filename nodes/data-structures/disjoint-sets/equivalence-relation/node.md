---
tag: R1127H
kind: concept
slug: equivalence-relation
name: Equivalence relation
aliases:
- equivalence
area: data-structures/disjoint-sets
level: intro
summary: Binary relation that is reflexive, symmetric and transitive, partitioning a set into classes.
see_also: [disjoint-set, dynamic-equivalence-problem, bell-numbers, congruence, partition-refinement, connected-components, transitive-closure]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B, Section B.2 (Relations, equivalence classes, and the theorem that an equivalence relation is the same as a partition)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.3.3 (the equivalence problem and Algorithm E)
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 6.1 (Stirling numbers of the second kind, which count partitions into a given number of classes)
---

An equivalence relation on a set $X$ is a binary relation $\sim$ that is reflexive, symmetric and transitive. Each equivalence relation splits $X$ into disjoint nonempty *equivalence classes*, and each such split into classes comes from exactly one equivalence relation. This one-to-one match between relations and partitions is why a [disjoint-set](/disjoint-set/) structure, which stores a partition, can answer "is $x \sim y$?" for a relation that is given only by a list of pairs. It is the base of the [dynamic equivalence problem](/dynamic-equivalence-problem/).

## In plain words

A relation says, for each pair of things, whether they are related. Some relations behave like "is the same as" in some respect: same color, same remainder after division by 7, same city. Such a relation has three rules. Each thing is related to itself. If one thing is related to a second, the second is related to the first. If a first is related to a second, and the second to a third, then the first is related to the third.

These rules let you sort all the things into groups, where two things are related exactly when they are in the same group. Each thing is in one group, and the groups do not overlap. If you only know some related pairs, the three rules decide all the other pairs, and a union-find structure finds them for you.

## The idea

**Definition.** A binary relation on a set $X$ is a subset $R \subseteq X \times X$, and we write $x \sim y$ for $(x, y) \in R$. It is an *equivalence relation* when, for all $x, y, z \in X$:

- **reflexive:** $x \sim x$;
- **symmetric:** $x \sim y$ implies $y \sim x$;
- **transitive:** $x \sim y$ and $y \sim z$ imply $x \sim z$.

The *class* of $x$ is $[x] = \{y \in X : x \sim y\}$, and the set of all classes is the *quotient* $X/{\sim}$.

**Theorem.** (1) If $\sim$ is an equivalence relation on $X$, its classes are nonempty, pairwise disjoint, and their union is $X$, so they form a partition of $X$. (2) If $P$ is a partition of $X$, the relation "$x$ and $y$ lie in the same block of $P$" is an equivalence relation whose classes are the blocks of $P$. (3) The two maps are inverse to each other.

*Proof.* (1) By reflexivity $x \in [x]$, so each class is nonempty and the classes cover $X$. Suppose $z \in [x] \cap [y]$. Then $x \sim z$ and $y \sim z$, so $z \sim y$ by symmetry and $x \sim y$ by transitivity. For each $w \in [y]$, $y \sim w$ gives $x \sim w$, so $[y] \subseteq [x]$; and $y \sim x$ by symmetry, so $[x] \subseteq [y]$ in the same way. So two classes that meet are equal. (2) Each $x$ lies in exactly one block $B(x)$. The relation $B(x) = B(y)$ is reflexive, symmetric and transitive because equality is. The class of $x$ is $\{y : B(y) = B(x)\} = B(x)$. (3) Starting from $\sim$, the relation of (2) for the partition of (1) relates $x$ and $y$ when $[x] = [y]$, which holds exactly when $x \sim y$, by the proof of (1). Starting from $P$, (2) gives a relation whose classes are the blocks of $P$, so (1) gives back $P$. $\square$

**The closure of a relation.** For any relation $R$ on $X$, the intersection of all equivalence relations that contain $R$ is an equivalence relation, because each of the three rules survives an intersection. It is the smallest one that contains $R$, the *equivalence closure* of $R$. Two elements are equivalent under it exactly when they are joined by a path of pairs of $R$, each pair used in either direction. So the classes are the [connected components](/connected-components/) of the undirected graph with the edge set $R$. A [disjoint-set](/disjoint-set/) structure computes these classes with one union per pair of $R$.

**Kernel of a map.** Each function $f : X \to Y$ defines the equivalence relation $x \sim_f y \iff f(x) = f(y)$. Each equivalence relation is of this form: take $f(x) = [x]$, the map from $X$ to $X/{\sim}$. In code, a representative of each class, as returned by `find`, is such a map.

**Counting.** The number of equivalence relations on a set of $n$ elements equals the number of its partitions, the [Bell number](/bell-numbers/) $B_n$. The first values are $B_0, \ldots, B_8 = 1, 1, 2, 5, 15, 52, 203, 877, 4140$. The number with exactly $k$ classes is the Stirling number of the second kind $\left\{ {n \atop k} \right\}$, see [counting set partitions](/counting-set-partitions/).

## Examples

- **Equality.** $x \sim y \iff x = y$ is the finest equivalence relation; each class has one element. The relation $X \times X$ is the coarsest; it has one class.
- **Congruence modulo $k$.** On the integers, $a \equiv b \pmod k$ for a fixed $k \ge 1$ means $k \mid a - b$. It is reflexive since $k \mid 0$, symmetric since $k \mid -(a - b)$, and transitive since $k \mid (a - b) + (b - c)$. There are $k$ classes, the residues $0$ to $k - 1$. See [congruence](/congruence/).
- **The three-element set.** On $X = \{a, b, c\}$ there are $B_3 = 5$ equivalence relations: all three apart; $\{a, b\}$ and $\{c\}$; $\{a, c\}$ and $\{b\}$; $\{b, c\}$ and $\{a\}$; all three together. Of the $2^9 = 512$ relations on $X$, exactly these 5 are equivalence relations.
- **Closure of a list of pairs.** On $X = \{0, \ldots, 7\}$, let $R = \{(1, 2), (3, 4), (2, 4), (5, 6)\}$. The equivalence closure has the classes $\{0\}$, $\{1, 2, 3, 4\}$, $\{5, 6\}$ and $\{7\}$. For example $1 \sim 3$ by the path $1, 2, 4, 3$, which uses $(3, 4)$ backwards.
- **Same component, same strongly connected component.** In an undirected graph, "joined by a path" is an equivalence relation, with the [connected components](/connected-components/) as classes. In a directed graph, "each reaches the other" is one too, with the [strongly connected components](/strongly-connected-components/) as classes.

**Non-examples.**

- $\le$ on the integers is reflexive and transitive, but not symmetric: $1 \le 2$ and not $2 \le 1$. It is a [total order](/total-order/).
- "Differ by at most 1" on the integers is reflexive and symmetric, but not transitive: $0$ and $1$ differ by 1, $1$ and $2$ differ by 1, but $0$ and $2$ differ by 2. Code that groups numbers with "close enough" as an equivalence, for example floats within a tolerance, gets groups that depend on the order of the input.
- "Reachable by a path" in a directed graph is reflexive and transitive, but not symmetric. Its closure under symmetry is "same weak component", which is coarser than "same strong component".
- The empty relation on a nonempty set is symmetric and transitive, but not reflexive.

## Where it is used

- **Union-find.** The [disjoint-set](/disjoint-set/) type stores the classes of a growing equivalence relation, and the [dynamic equivalence problem](/dynamic-equivalence-problem/) asks for it to be kept under new pairs. The [disjoint-set forest](/disjoint-set-forest/) solves it in almost linear time.
- **Graphs.** [Kruskal's algorithm](/kruskal/) keeps the classes "joined by chosen edges", and [connected component labeling](/connected-component-labeling/) of images keeps "same component" over the pixels.
- **Automata.** [DFA minimization](/dfa-minimization/) merges the states that are equivalent under the [Myhill-Nerode](/myhill-nerode-theorem/) relation, by [partition refinement](/partition-refinement/). The [Hopcroft-Karp](/hopcroft-karp-equivalence/) test of the equivalence of two automata merges pairs of states with union-find.
- **Logic and compilers.** [Congruence closure](/congruence-closure/) computes the smallest equivalence closed under function application, and unification finds a [most general unifier](/most-general-unifier/) by merging classes of terms.
- **Hashing and grouping.** A key function defines the kernel equivalence, and grouping by key, as in a hash table or a database GROUP BY, lists its classes.

## References
