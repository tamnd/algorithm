---
tag: W1D2WX
kind: problem
slug: word-problem-for-groups
name: Word problem for groups
aliases:
- Dehn's word problem
area: complexity/computability
level: advanced
summary: Given a finitely presented group and a word in its generators, decide whether the word equals the identity. Novikov and Boone proved that some groups have an undecidable word problem.
prereqs: [halting-problem, many-one-reducibility, recursively-enumerable-language]
see_also: [undecidability-of-word-problem, word-problem, string-rewriting-system, knuth-bendix-completion, finite-group, halting-problem, post-correspondence-problem, turing-degrees]
sources:
  - paper: doi:10.1007/BF01456932
    title: Max Dehn, Über unendliche diskontinuierliche Gruppen, Mathematische Annalen 71 (1911)
    locator: pp. 116 to 144 (the word, conjugacy and isomorphism problems)
  - paper: doi:10.1007/BF01455888
    title: Wilhelm Magnus, Das Identitätsproblem für Gruppen mit einer definierenden Relation, Mathematische Annalen 106 (1932)
    locator: pp. 295 to 307
  - title: Pyotr S. Novikov, On the algorithmic unsolvability of the word problem in group theory, Trudy Matematicheskogo Instituta imeni V. A. Steklova 44 (1955)
  - paper: doi:10.2307/1970103
    title: William W. Boone, The word problem, Annals of Mathematics 70(2) (1959)
    locator: pp. 207 to 265
  - paper: doi:10.1090/S0273-0979-1982-14963-1
    title: John Stillwell, The word problem and the isomorphism problem for groups, Bulletin of the American Mathematical Society (New Series) 6(1) (1982)
    locator: pp. 33 to 56
  - title: Joseph J. Rotman, An Introduction to the Theory of Groups, fourth edition, Graduate Texts in Mathematics 148, Springer, 1995
    locator: Chapter 12, The Word Problem
---

The word problem for a group asks whether a given product of generators and their inverses equals the identity element. Max Dehn posed it in 1911 for finitely presented groups, together with the conjugacy and isomorphism problems, and solved it for the fundamental groups of closed surfaces. For many classes of groups the problem is decidable: free groups, abelian groups, finite groups, groups with one defining relation. In 1955 Pyotr Novikov, and independently William Boone in 1959, built a finitely presented group whose word problem is [undecidable](/undecidability/). The result for groups is harder than the earlier one for semigroups, on the page [undecidability of the word problem](/undecidability-of-word-problem/), because inverses make it harder to keep a machine's computation from collapsing.

## In plain words

A group can be described by a few basic moves and a few rules that say when a sequence of moves cancels out. A word is a sequence of moves. The question is: does this word cancel out to nothing?

For some groups this is easy. If the only rule is that a move followed by its reverse cancels, you cross out such pairs until none is left. If moves can be done in any order, you just count each move.

Novikov and Boone found a group, given by a finite list of moves and rules, for which no method can answer the question for every word. Its rules are built so that a word cancels out exactly when a certain computer program stops.

## Definition

A *finite presentation* $\langle S \mid R \rangle$ has a finite set $S$ of generators and a finite set $R$ of relators, which are words over $S \cup S^{-1}$. It defines the group $G = F(S) / N$, where $F(S)$ is the free group on $S$ and $N$ is the smallest normal subgroup that contains $R$.

**Instance.** A finite presentation $\langle S \mid R \rangle$ and a word $w$ over $S \cup S^{-1}$.

**Question.** Does $w$ represent the identity element of $G$?

For a fixed group $G$, the *word problem of $G$* takes only $w$ as input. Whether it is decidable depends only on the group, not on the finite presentation or the finite generating set chosen, since words over one generating set can be rewritten over another by a fixed substitution.

**The problem is c.e.** A word $w$ equals the identity in $G$ if and only if it is freely equal to a product of conjugates $u_1 r_1^{\pm 1} u_1^{-1} \cdots u_k r_k^{\pm 1} u_k^{-1}$ of relators. A program can list all such products, reduce each one freely, and halt when it finds $w$. So the set of words equal to the identity is computably enumerable (c.e.) for every finitely presented group. Its complement need not be c.e.

**Theorem (Novikov 1955, Boone 1959).** There is a finite presentation $\langle S \mid R \rangle$ whose word problem is undecidable.

The proofs start from a Turing machine $M$, or from a semigroup with undecidable word problem, and build a group with generators for the states and tape symbols. Conjugation by special generators acts like a step of $M$, and a carefully chosen word equals the identity if and only if $M$ halts on the input coded in the word. The hard part is to show that the relators allow no unwanted shortcuts. Britton's lemma on HNN extensions is the usual tool for this; see Rotman, Chapter 12.

## Variants

- **Uniform problem.** The presentation is part of the input. It is undecidable because the fixed version is.
- **Conjugacy problem.** Are two words conjugate in $G$? It is at least as hard as the word problem, since $w$ is conjugate to the empty word exactly when $w = 1$.
- **Isomorphism and triviality.** Do two presentations define the same group? Does a presentation define the trivial group? Both are undecidable, by the Adian-Rabin theorem (1955 to 1958). It covers every *Markov property*: a property that some finitely presented group has, while some other finitely presented group is not a subgroup of any finitely presented group that has it. Being trivial, finite, abelian or free are examples; see Stillwell's survey.
- **Semigroups and monoids.** The same question for semigroup presentations was shown undecidable by Post and by Markov in 1947. See [undecidability of the word problem](/undecidability-of-word-problem/) and the general [word problem](/word-problem/).
- **Recursively presented groups.** If $R$ is an infinite c.e. set, the group is recursively presented. Higman's embedding theorem (1961) says that a finitely generated group is recursively presented if and only if it embeds in a finitely presented group.

## Examples

Write capital letters for inverses, so $A = a^{-1}$ and $B = b^{-1}$.

**Free group on $a, b$.** Here $R$ is empty. A word equals the identity if and only if *free reduction*, which deletes adjacent pairs $aA$, $Aa$, $bB$ or $Bb$ until none is left, reduces it to the empty word. The word $abBA$ reduces to $aA$ and then to nothing, so it is the identity. The word $aBbbAaBA$ also reduces to nothing. The commutator $abAB$ has no adjacent inverse pair, so it is not the identity, and neither is $abaBAbAB$. A stack does free reduction in one left-to-right pass, so the word problem of a free group takes linear time.

**The group $\mathbb{Z}^2 = \langle a, b \mid abAB \rangle$.** The relator says that $a$ and $b$ commute. A word equals the identity if and only if the number of $a$ minus the number of $A$ is $0$, and the same for $b$. The words $abAB$ and $aabAAB$ both have exponent sums $(0, 0)$, so both equal the identity here, though neither is the identity in the free group. The same counting method solves the word problem of every finitely generated abelian group.

**Finite groups.** For a finite group given by a multiplication table, multiply out the word. For a finite presentation of a group known to be finite, coset enumeration (the Todd-Coxeter method) builds the table first; see [finite groups](/finite-group/).

## Known algorithms

- **Free reduction** for free groups, in linear time.
- **Magnus's method** for groups with one relator (Magnus 1932). It works by induction on the length of the relator, and its running time has no good general bound.
- **Dehn's algorithm.** Some presentations have the property that every nonempty word equal to the identity contains more than half of some relator as a subword. Then replace that part by the shorter rest of the relator, and repeat. The word is the identity if and only if this ends at the empty word. Dehn used this for surface groups; it works for small cancellation groups and for Gromov's hyperbolic groups, in linear time.
- **Rewriting.** If [Knuth-Bendix completion](/knuth-bendix-completion/) turns the presentation into a finite confluent and terminating [string rewriting system](/string-rewriting-system/), then two words are equal if and only if they have the same normal form.
- **Residually finite groups.** If $G$ is finitely presented and every nonidentity element survives in some finite quotient of $G$, the word problem is decidable. Run two searches side by side: list the words that equal $1$, as above, and list the maps from $S$ to finite permutation groups that send every relator to $1$, looking for one that sends $w$ to a nonidentity permutation. Exactly one search halts. This covers, for example, all finitely presented linear groups.

## Bounds

- **Undecidable** for some fixed finite presentation (Novikov, Boone), and so for the uniform problem.
- **Always c.e.** for finitely presented groups. The undecidable cases have a complement that is not c.e.
- **Degrees.** Boone showed that every c.e. [Turing degree](/turing-degrees/) is the degree of the word problem of some finitely presented group, so the word problem can be exactly as hard as the [halting problem](/halting-problem/), or strictly easier and still undecidable.
- **Decidable classes** include free, abelian, finite, one-relator, hyperbolic, automatic and residually finite finitely presented groups.

## Reductions

All reductions here are many-one reductions by total computable maps.

- **From halting.** The Novikov-Boone construction maps an input $x$ of a fixed machine $M$, with a c.e. but undecidable set of accepted inputs, to a word $w_x$ that equals the identity in a fixed group if and only if $M$ accepts $x$.
- **From semigroups.** Boone's and Britton's proofs reduce the word problem of a semigroup with an undecidable word problem to the word problem of a group built from it.
- **To halting.** Map $w$ to the program that lists the products of conjugates of relators and halts when one freely reduces to $w$.
- **To other group problems.** The word problem reduces to the conjugacy problem in the same group, and to the triviality and isomorphism problems for presentations built from $w$.

## Applications

- **Topology.** Every finitely presented group is the fundamental group of a closed four-dimensional manifold. With the Adian-Rabin theorem this shows that it is undecidable whether two such manifolds are homeomorphic.
- **Computational group theory.** Systems for computing with groups use free reduction, coset enumeration, rewriting systems and Dehn's algorithm, each on the classes of groups where it works.
- **Logic.** The theorem was one of the first undecidability results about a question from ordinary mathematics, not from logic or machines.

## References
