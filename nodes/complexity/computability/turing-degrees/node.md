---
tag: P24ZFN
kind: concept
slug: turing-degrees
name: Turing degrees
aliases:
- degrees of unsolvability
area: complexity/computability
level: research
summary: "The classes of sets that are computable from each other with an oracle, ordered by Turing reducibility. The decidable sets form the least degree 0, and the halting problem has the degree 0'."
prereqs: [oracle-turing-machine, equivalence-relation]
see_also: [oracle-turing-machine, turing-jump, post-problem, arithmetical-hierarchy, halting-problem, many-one-reducibility, ladners-theorem, chaitins-constant]
sources:
  - paper: doi:10.1090/S0002-9904-1944-08111-1
    title: "Emil L. Post, Recursively enumerable sets of positive integers and their decision problems, Bulletin of the American Mathematical Society 50 (1944)"
    locator: "pp. 284 to 316 (Turing reducibility, and degrees of unsolvability of c.e. sets)"
  - paper: doi:10.2307/1969708
    title: "Stephen C. Kleene and Emil L. Post, The upper semi-lattice of degrees of recursive unsolvability, Annals of Mathematics 59(3) (1954)"
    locator: pp. 379 to 407
  - paper: doi:10.1073/pnas.43.2.236
    title: "Richard M. Friedberg, Two recursively enumerable sets of incomparable degrees of unsolvability, Proceedings of the National Academy of Sciences 43(2) (1957)"
    locator: pp. 236 to 238
  - book: isbn:9783642319327
    title: "Robert I. Soare, Turing Computability, Theory and Applications, Springer, 2016"
    locator: "Chapter 3, Turing Reducibility, and Chapter 6, Oracle Constructions and Forcing"
---

A Turing degree is a class of sets that are all computable from each other. Two sets $A$ and $B$ have the same degree if an [oracle Turing machine](/oracle-turing-machine/) with oracle $B$ decides $A$ and one with oracle $A$ decides $B$. The degree measures how hard a set is to compute: it ignores everything about a set except the information that can be extracted from it by an algorithm. The degrees are ordered by Turing reducibility. The decidable sets form the least degree $\mathbf{0}$, and the [halting problem](/halting-problem/) has the degree $\mathbf{0}'$, which is the largest degree of a computably enumerable (c.e.) set. Post introduced the notion in 1944 under the name "degrees of unsolvability", and Kleene and Post (1954) began the study of the order. The order is far from a line: there are incomparable degrees, degrees between $\mathbf{0}$ and $\mathbf{0}'$, and pairs with no greatest lower bound.

## In plain words

Some problems cannot be solved by any program. They are still not all equally hard. Suppose you had a magic box that answers one such problem instantly. With it, you might be able to solve a second problem. If each problem can be solved with a box for the other, they are equally hard, and they have the same degree.

The halting problem sits at a famous level. Every problem whose yes answers can be confirmed by a search is at that level or below. There are levels above it, levels between it and the solvable problems, and pairs of levels where neither is below the other.

## The idea

**Definition.** For sets $A, B \subseteq \mathbb{N}$, $A \le_T B$ if $A$ is decided by an oracle machine with oracle $B$. Write $A \equiv_T B$ if $A \le_T B$ and $B \le_T A$. This is an [equivalence relation](/equivalence-relation/), because $\le_T$ is reflexive and transitive. The *Turing degree* of $A$ is its class
$$\deg(A) = \{ B : B \equiv_T A \},$$
written with bold letters $\mathbf{a}, \mathbf{b}$. The order $\deg(A) \le \deg(B)$ if and only if $A \le_T B$ is well defined, and $(\mathcal{D}, \le)$ is the partial order of all degrees.

**Basic structure.**

- **Least element.** $\mathbf{0} = \deg(\emptyset)$ is the set of decidable sets.
- **Joins.** The *join* $A \oplus B = \{2x : x \in A\} \cup \{2x + 1 : x \in B\}$ computes both $A$ and $B$, and any set that computes both computes $A \oplus B$. So $\deg(A \oplus B)$ is the least upper bound of $\deg(A)$ and $\deg(B)$, and $\mathcal{D}$ is an upper semi-lattice.
- **Size.** Each degree contains countably many sets, since there are countably many oracle programs, and each degree has countably many degrees below it. There are $2^{\aleph_0}$ degrees, so the order is uncountable.
- **The jump.** For each set $A$, the halting problem relative to $A$, written $A'$, has a degree strictly above $\deg(A)$. So there is no greatest degree. This is the [Turing jump](/turing-jump/); $\mathbf{0}' = \deg(\emptyset')$ is the degree of $K$.
- **Turing and many-one.** Turing equivalence is coarser than [many-one](/many-one-reducibility/) equivalence. A set and its complement always have the same Turing degree, while $K$ and its complement are not many-one equivalent, because the complement of $K$ is not c.e.

**The c.e. degrees.** A degree is *c.e.* if it contains a c.e. set. Every c.e. set is many-one reducible to $K$, so the c.e. degrees lie between $\mathbf{0}$ and $\mathbf{0}'$. Post asked in 1944 whether there are any c.e. degrees other than these two; this is [Post's problem](/post-problem/). Friedberg (1957) and Muchnik (1956) answered yes, with two c.e. sets of incomparable degree, built by the priority method.

**Results on the order.**

- **Kleene and Post (1954)** built two sets $A, B \le_T K$ with $A \not\le_T B$ and $B \not\le_T A$, by extending finite parts of the characteristic functions step by step, with $K$ answering the questions that each step needs. So $\mathcal{D}$ is not linear, even below $\mathbf{0}'$.
- **Minimal degrees.** Spector showed that there are *minimal* degrees: degrees $\mathbf{m} > \mathbf{0}$ with nothing strictly between $\mathbf{0}$ and $\mathbf{m}$. No c.e. degree is minimal.
- **Not a lattice.** Some pairs of degrees have no greatest lower bound in $\mathcal{D}$. Among the c.e. degrees, Lachlan and Yates (1966) showed that some pairs have no infimum in the c.e. degrees.
- **Density of the c.e. degrees.** Sacks proved that between any two c.e. degrees $\mathbf{a} < \mathbf{b}$ there is a c.e. degree $\mathbf{c}$ with $\mathbf{a} < \mathbf{c} < \mathbf{b}$. The whole order $\mathcal{D}$ is not dense, because minimal degrees exist.

## Examples

**Degree $\mathbf{0}$.** The primes $A = \{2, 3, 5, 7, 11, 13, 17, 19, \ldots\}$ and the squares $B = \{0, 1, 4, 9, 16, \ldots\}$ are decidable, so $\deg(A) = \deg(B) = \mathbf{0}$. Their join has, below 40, the elements $1, 3, 4, 6, 9, 10, 14, 19, 22, 26, 33, 34, 38$: the even ones are twice a prime and the odd ones are twice a square plus one. It is decidable too, which matches $\mathbf{0} \vee \mathbf{0} = \mathbf{0}$.

**Degree $\mathbf{0}'$.** These sets are all Turing equivalent to $K$:

- $K$, HALT and the acceptance problem $A_{\mathrm{TM}}$;
- the set of Diophantine equations that have an integer solution, by the MRDP theorem ([Hilbert's tenth problem](/hilberts-tenth-problem/));
- the solvable instances of the [Post correspondence problem](/post-correspondence-problem/);
- the set of words equal to the identity in a suitable finitely presented group with an undecidable [word problem](/word-problem-for-groups/);
- [Chaitin's constant](/chaitins-constant/) $\Omega$, as an infinite binary sequence, and the [busy beaver function](/busy-beaver-function/).

The sets in the first four items are c.e. sets to which $K$ reduces, so they are complete c.e. sets. $\Omega$ and the busy beaver function are not sets of instances of a decision problem, but each computes $K$ and is computed from $K$.

**Above $\mathbf{0}'$.** $\mathrm{FIN} = \{ e : W_e \text{ is finite} \}$ and $\mathrm{TOT} = \{ e : \varphi_e \text{ is total} \}$ have the degree $\mathbf{0}''$, and $\mathrm{COF} = \{ e : W_e \text{ is cofinite} \}$ has the degree $\mathbf{0}'''$. The [arithmetical hierarchy](/arithmetical-hierarchy/) page gives the quantifier forms that put them there.

**Same degree, different difficulty for many-one.** $K$ and its complement have the same Turing degree $\mathbf{0}'$. One query to $K$ answers a question about the complement. With a many-one reduction this is not possible: the answer cannot be negated.

## Where it is used

- **Classifying undecidable problems.** The degree says whether a problem is as hard as halting ($\mathbf{0}'$), harder (for example $\mathbf{0}''$ for totality of programs), or strictly between. Most natural undecidable problems turn out to be complete for a level of the [arithmetical hierarchy](/arithmetical-hierarchy/), so they sit on degrees of the form $\mathbf{0}^{(n)}$. No natural problem is known to have an intermediate c.e. degree.
- **Complexity theory.** Polynomial-time Turing and many-one reductions give degrees of the same kind inside the decidable sets. [Ladner's theorem](/ladners-theorem/) is the analog of the Friedberg-Muchnik theorem: if $\mathrm{P} \ne \mathrm{NP}$, there are problems in $\mathrm{NP}$ between $\mathrm{P}$ and the NP-complete problems. Its proof is a delayed diagonalization, a method that comes from recursion theory.
- **Algorithmic randomness and computable analysis.** The degree of a random sequence, or of a real number, measures the information it contains. For example, Chaitin's constant is random and has the degree $\mathbf{0}'$.
- **Computable mathematics.** The degrees of the solutions of a mathematical problem measure how far it is from having an algorithmic solution, as in the study of which theorems have computable instances with no computable solution.

## References
