---
tag: KS4RN5
kind: theorem
slug: pseudoknot-np-hardness
name: NP-hardness of pseudoknot prediction
aliases:
- Pseudoknot prediction is NP-hard
- Lyngsø-Pedersen theorem
area: biology/structure-prediction
level: research
summary: Finding a minimum energy RNA structure with arbitrary pseudoknots is NP-complete in the nearest neighbor pseudoknot model (Lyngsø and Pedersen, 2000).
prereqs: [pseudoknot, np-complete, polynomial-time-reduction, 3-sat]
see_also: [rna-pseudoknot-prediction, nearest-neighbor-model, maximum-matching, zuker-algorithm, rna-inverse-folding, hp-folding-np-completeness]
sources:
  - paper: doi:10.1089/106652700750050862
    title: Rune B. Lyngsø and Christian N. S. Pedersen, RNA pseudoknot prediction in energy-based models, Journal of Computational Biology 7(3-4), 2000, pages 409 to 427
    locator: the nearest neighbor pseudoknot model and the NP-completeness of structure prediction in it
  - paper: "Rune B. Lyngsø and Christian N. S. Pedersen, Pseudoknots in RNA secondary structures, BRICS Report Series RS-00-1, University of Aarhus, 2000 (also RECOMB 2000)"
    title: Pseudoknots in RNA secondary structures
    locator: Section 4, Definition 1 (the model), Proposition 1, Lemmas 1 and 2, and the reduction from 3SAT
  - paper: doi:10.1016/S0166-218X(00)00186-4
    title: Tatsuya Akutsu, Dynamic programming algorithms for RNA secondary structure prediction with pseudoknots, Discrete Applied Mathematics 104(1-3), 2000, pages 45 to 62
    locator: the NP-hardness of optimal planar structures and the polynomial algorithms for simple pseudoknots
  - paper: doi:10.1089/106652703322756186
    title: Samuel Ieong, Ming-Yang Kao, Tak-Wah Lam, Wing-Kin Sung and Siu-Ming Yiu, Predicting RNA secondary structures with arbitrary pseudoknots by maximizing the number of stacking pairs, Journal of Computational Biology 10(6), 2003, pages 981 to 995
    locator: NP-hardness of the most stacking pairs in a planar structure, and the 1/2 and 1/3 approximations
  - paper: "Rune B. Lyngsø, Complexity of pseudoknot prediction in simple models, ICALP 2004, Lecture Notes in Computer Science 3142, Springer, pages 919 to 931"
    title: Complexity of pseudoknot prediction in simple models
    locator: hardness with fixed energies in the stacking pair models, and the polynomial and approximation results
  - paper: doi:10.1007/978-3-642-31265-6_26
    title: Saad Sheikh, Rolf Backofen and Yann Ponty, Impact of the energy model on the complexity of RNA folding with pseudoknots, CPM 2012, Lecture Notes in Computer Science 7354, pages 321 to 333
    locator: hardness for many parametrizations of the stacking pair model and the inapproximability of the nearest neighbor version
  - paper: doi:10.1089/cmb.2019.0420
    title: Édouard Bonnet, Paweł Rzążewski and Florian Sikora, Designing RNA secondary structures is hard, Journal of Computational Biology 27(3), 2020, pages 302 to 316
    locator: the remark that the energy values in the reduction of Lyngsø and Pedersen are part of the input
  - paper: "Piotr Berman, Marek Karpinski and Alexander D. Scott, Approximation hardness and satisfiability of bounded occurrence instances of SAT, Electronic Colloquium on Computational Complexity, Report TR03-022, 2003"
    title: Approximation hardness and satisfiability of bounded occurrence instances of SAT
    locator: NP-completeness of 3SAT with three literals per clause and each literal exactly twice
---

Lyngsø and Pedersen (2000) proved that finding a minimum energy structure of an RNA is NP-complete when the structure may have arbitrary [pseudoknots](/pseudoknot/), even in a very simple energy model where each base pair gets an energy from its neighbors only. Without pseudoknots, the same kind of problem is solved in $O(n^3)$ time by the [Zuker algorithm](/zuker-algorithm/). So the hardness comes from the crossing pairs, and it explains why practical pseudoknot programs restrict the class of structures. The theorem needs care in its statement: the energy values in the proof depend on the input, and with crossings and an energy only per pair (no stacking), the problem is a [maximum matching](/maximum-matching/) and is polynomial.

## Statement

**The model.** A *structure* of $s = s_1 \cdots s_n \in \{A, C, G, U\}^*$ is a set $S$ of pairs $i \cdot j$ with $1 \le i < j \le n$ in which no base is in two pairs. Pairs may cross, with no restriction. In the *nearest neighbor pseudoknot model* (Lyngsø and Pedersen, Definition 1), the energy is a sum over pairs,

$$E(S) = \sum_{i \cdot j \in S} E(i \cdot j,\ i + 1,\ j - 1),$$

where the term of $i \cdot j$ may depend on the bases $s_i$ and $s_j$, on the neighbor bases $s_{i+1}$ and $s_{j-1}$, and, if $i + 1$ or $j - 1$ is paired in $S$, on the position of its partner.

**Theorem (Lyngsø and Pedersen 2000).** The following problem is NP-complete. Given a sequence $s$, an energy function of the nearest neighbor pseudoknot model, and an integer $K$, decide whether $s$ has a structure $S$ with $E(S) \le K$. It stays NP-complete when only the Watson-Crick pairs AU and CG are allowed and the energy function has the following form, with $d$ an integer that depends on the input:

$$E(i \cdot j, i + 1, j - 1) = \begin{cases} -1 & \text{if } (i + 1) \cdot (j - 1) \in S \text{ and both pairs are AU or UA, or both are CG or GC}, \\ 4d + 7 & \text{else, if neither } i + 1 \text{ nor } j - 1 \text{ pairs with a base outside } [i + 1, j - 1], \\ 4d + 8 & \text{otherwise.} \end{cases}$$

The energy values grow with the input, so the energy function is part of the input. The theorem does not show hardness for one fixed table of energies; see Tightness.

## In plain words

Without crossing pairs, the best fold of an RNA can be found fast by splitting the string into independent parts. When pairs may cross, the parts are no longer independent. The theorem shows that the problem then becomes as hard as the hardest search problems in NP, even when the energy of each pair depends only on the letters next to it.

The proof turns a logic formula into an RNA string. Some stretches of the string can form a long helix with their complement. Helices of one kind say which literal is true in each clause. Helices of another kind cover other stretches and block them, so that a clause cannot profit twice and a variable cannot be both true and false. The string has a fold with a given low energy exactly when the formula can be satisfied.

## Proof

*Membership in NP.* A structure has at most $n/2$ pairs, and $E(S)$ is a sum of $|S|$ terms that each need $O(1)$ lookups. So a structure with $E(S) \le K$ is a certificate that can be checked in polynomial time.

*Hardness.* The reduction is from 3SAT in which each clause has three literals and each literal (a variable or its negation) occurs at most twice. This restriction of [3-SAT](/3-sat/) is NP-complete; Berman, Karpinski and Scott show this even when each literal occurs exactly twice. Let $\varphi$ have $c$ clauses and $v$ variables, and let $d = \lceil \log_2(3c + v) \rceil$. We build a sequence $s_\varphi$ and use the energy function of the statement. We show that the minimum energy of $s_\varphi$ is $-(3c + v)$ if $\varphi$ is satisfiable, and greater otherwise. This is a [polynomial-time reduction](/polynomial-time-reduction/) with $K = -(3c + v)$.

**Patterns.** For $0 \le k < 2^d$, let $b(k)$ be the $d$-digit binary form of $k$ over $\{A, U\}$, with A for 0 and U for 1. The $k$-th *$\{A, U\}$ pattern* is

$$A^{d+2}\, U\, b(k)\, AUA\, b(k)\, U\, A^{d+2},$$

of length $4d + 9$. The $\{C, G\}$ patterns are the same with C for A and G for U. The *complement* $\bar x$ of a string $x$ is $x$ reversed, with A and U swapped and C and G swapped, so that $x$ and $\bar x$ can form a helix of $|x| = 4d + 9$ Watson-Crick pairs, all AU or all CG. Each pattern below uses its own value of $k$; there are $2c + v$ values for the $\{A, U\}$ patterns and $3c$ for the $\{C, G\}$ patterns, and $2^d \ge 3c + v$ is enough.

**Clause block.** For a clause $l_1 \vee l_2 \vee l_3$, take two new $\{A, U\}$ patterns $S_1$, $S_2$ and three new $\{C, G\}$ patterns $L_1$, $L_2$, $L_3$, one for each literal, and write

$$S_1\ L_1\ \bar S_1\ S_2\ L_2\ S_1\ \bar S_2\ L_3\ S_2.$$

The complement $\bar S_1$ can form a helix with the first copy of $S_1$, which encloses $L_1$, or with the second copy, which encloses $S_2 L_2$. In the same way $\bar S_2$ can pair with the first $S_2$, enclosing $L_2 S_1$, or with the second, enclosing $L_3$.

**Variable block.** For a variable $x$, take a new $\{A, U\}$ pattern $S$ and write

$$S\ \bar P_1\ \bar P_2\ \bar S\ \bar N_1\ \bar N_2\ S,$$

where $\bar P_1, \bar P_2$ are the complements of the $L$ patterns of the positive occurrences of $x$ and $\bar N_1, \bar N_2$ those of the negative occurrences (one is left out if the literal occurs once, both if it does not occur). The helix of $\bar S$ with the left copy of $S$ encloses the $\bar P$ part, and with the right copy the $\bar N$ part.

**The sequence.** $s_\varphi = C_1 C_2 \cdots C_c\, V_1 V_2 \cdots V_v$, the clause blocks and then the variable blocks. For a literal with two occurrences, the two complements are written in the reverse order of the two $L$ patterns, so that the two helices of the literal nest and do not cross. The length is $O((c + v) \log(c + v))$, and the construction takes polynomial time.

**Runs.** Call a *run* a maximal chain of pairs $i \cdot j, (i + 1) \cdot (j - 1), \ldots$ in $S$ that are all AU or all CG. The pairs of $S$ split into runs. In a run of $h$ pairs, the $h - 1$ outer pairs have energy $-1$, and the innermost pair has energy $4d + 7$ or $4d + 8$. So a run has energy $4d + 8 - h$ or $4d + 9 - h$, and

$$E(S) = \sum_{\text{runs } R} \big(4d + 8 - |R| + \pi(R)\big), \qquad \pi(R) \in \{0, 1\},$$

where $\pi(R) = 1$ if a neighbor of the innermost pair of $R$ pairs with a base outside the run. A run has negative energy only if $|R| \ge 4d + 9$.

**Lemma A (long runs).** In any structure of $s_\varphi$, a run has at most $4d + 9$ pairs, and a run of exactly $4d + 9$ pairs pairs a pattern with its own complement, base by base.

*Proof sketch, following Lyngsø and Pedersen (Lemmas 1 and 2).* Each strand of a run of at least $4d + 5$ pairs contains $2d + 3$ bases at one end of some pattern or complement, such as $A^{d+2} U b(k)$. The only places where $d + 2$ letters U follow an A are the ends of the complements of $\{A, U\}$ patterns, and only Watson-Crick pairs are allowed, so these bases pair with $\bar b(k') A U^{d+2}$ and the binary codes force $k' = k$. So a long run contains part of a designed helix. A designed helix cannot be extended by one more pair of the same class: each $\{C, G\}$ pattern sits between A or U bases in its clause block, each complement of a variable block $\{A, U\}$ pattern sits next to G or C bases, and the complements in a clause block are bordered by a base that would form a forbidden pair. $\square$

**Lemma B (counting).** For every structure $S$ of $s_\varphi$, $E(S) \ge -(3c + v)$.

*Proof.* By Lemma A and the formula for runs, only designed helices of $4d + 9$ pairs with $\pi = 0$ have negative energy, each exactly $-1$; all other runs have energy at least 0. Call such a helix *active*. Since no base is in two pairs, each complement $\bar S_1$, $\bar S_2$ or $\bar S$ is in at most one active helix, and each $L$ pattern is in at most one. A helix that encloses a pattern $L$ (or $\bar P$, $\bar N$) right next to its innermost pair is not active if that pattern forms its own designed helix with a partner outside: the first or last base of the pattern is a neighbor of the innermost pair and pairs outside, so $\pi = 1$. We say the helix *screens* the pattern.

In a clause block, the two choices for $\bar S_1$ and the two for $\bar S_2$ give four cases. If $\bar S_1$ takes the second $S_1$ and $\bar S_2$ takes the first $S_2$, the two helices cross with neighbor pairs, so both have $\pi = 1$ and neither is active. In the other three cases, the two helices screen two of $L_1, L_2, L_3$ and leave the third free. If only one helix of the block is active, it screens at least one $L$. So each clause block has at most 3 active helices among its own two $\{A, U\}$ helices and the helices of its three $L$ patterns. Each variable block has at most one active $\{A, U\}$ helix. The total is at most $3c + v$. $\square$

**Satisfiable implies energy $-(3c + v)$.** Fix a satisfying assignment. In the block of each variable $x$, form the helix of $\bar S$ that encloses the complements of the false literals: the $\bar N$ part if $x$ is true, the $\bar P$ part if not. In each clause, choose a true literal $l_t$, and form the two $\{A, U\}$ helices of the case that leaves $L_t$ free. Then form the helix of $L_t$ with its complement in the variable block. That complement is not enclosed, because its literal is true. The neighbors of the innermost pair of each helix are free or pair inside the helix: this is where the reverse order of the two complements of a literal is used. So all $2c + v + c$ helices are active, and $E(S) = -(3c + v)$.

**Energy $-(3c + v)$ implies satisfiable.** If $E(S) = -(3c + v)$, every bound in Lemma B is tight. Each variable block has an active helix, which screens the complements of one of the two literals of $x$; set $x$ true if it screens the negative side and false if it screens the positive side. Each clause block has 3 active helices, so at least one $L_t$ of the clause forms an active helix with its complement. That complement is not screened, so its literal is true under the assignment. So every clause is satisfied. $\blacksquare$

## Consequences

- **Richer models are hard too.** The nearest neighbor pseudoknot model is a special case of the energy model of Rivas and Eddy (1999), obtained by fixing parameters. So minimum energy prediction with arbitrary pseudoknots is NP-hard in that model, and in any model that contains it in this way, unless the model restricts the class of structures.
- **Restricted classes.** Algorithms with pseudoknots must restrict the class: Rivas and Eddy handle their gap matrix class in $O(n^6)$ time, Dirks and Pierce their class in $O(n^5)$, Akutsu and Reeder and Giegerich simple or canonical classes in $O(n^4)$. See [RNA pseudoknot prediction](/rna-pseudoknot-prediction/).
- **No exact polynomial algorithm, unless P = NP.** For arbitrary pseudoknots, only heuristics, restricted classes, exponential algorithms or approximations remain.

## Tightness

The border between hard and easy depends on three things: the class of structures, the energy model, and whether the energies are fixed or part of the input.

- **Polynomial: no crossings.** For nested structures, the minimum energy in the loop model is found in $O(n^3)$ time with a bound on interior loops ([Zuker algorithm](/zuker-algorithm/)), and the largest number of pairs in $O(n^3)$ ([Nussinov algorithm](/nussinov-algorithm/)).
- **Polynomial: crossings, energy per pair only.** If each pair has an energy that depends only on its two bases, any set of pairs without shared bases is allowed, and the best structure is a [maximum weight matching](/maximum-weight-matching/) in the graph of allowed pairs, solvable in polynomial time. Tabaska and others (1998) used this for pseudoknots. The stacking term is what makes the problem hard.
- **Hard: planar structures.** Akutsu (2000) showed that finding an optimal planar structure is NP-hard, where a structure is planar if the graph of its pairs and the backbone is planar. Ieong, Kao, Lam, Sung and Yiu (2003) showed that maximizing the number of stacking pairs in a planar structure is NP-hard, by a reduction from tripartite matching, and gave approximations with ratios $1/2$ for planar structures in $O(n^3)$ time and $1/3$ for general structures in $O(n)$ time.
- **Hard with fixed energies.** In the proof above the values $4d + 7$ and $4d + 8$ grow with the input, as Bonnet, Rzążewski and Sikora point out. Lyngsø (2004) proved hardness for fixed simple energy functions: in a model that counts stacking pairs the problem is NP-hard already over a binary alphabet and has a polynomial-time approximation scheme, and in a model that rewards stacks of each type of pair it is NP-hard over an unbounded alphabet but polynomial for a fixed alphabet. Sheikh, Backofen and Ponty (2012) showed hardness for many settings of the stacking pair model, a 5-approximation, and that the nearest neighbor version cannot be approximated within any positive ratio unless P = NP.

## History

The first algorithms with pseudoknots, by Rivas and Eddy (1999) and Akutsu (2000), were polynomial only for restricted classes. Lyngsø and Pedersen presented the hardness result at RECOMB 2000, with a longer version in the Journal of Computational Biology the same year. Akutsu proved hardness for planar structures in the same year. Later work moved toward simpler and fixed energy models: Ieong and others (2003) for stacking pairs in planar structures, Lyngsø (2004) for fixed energies, and Sheikh, Backofen and Ponty (2012) for the effect of the energy model.

## References
