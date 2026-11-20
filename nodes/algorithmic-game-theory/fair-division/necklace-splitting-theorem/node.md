---
tag: J7FE64
kind: theorem
slug: necklace-splitting-theorem
name: Necklace splitting theorem
aliases:
- Alon's necklace splitting theorem
area: algorithmic-game-theory/fair-division
level: advanced
summary: "If each of t colours has a number of beads that is a multiple of k, then k thieves can split an open necklace with at most (k - 1) t cuts so that each gets the same number of beads of each colour."
prereqs: [consensus-halving, tfnp]
see_also: [cake-cutting-problem, proportional-division, ppad, end-of-the-line-problem, sperner-lemma, su-rental-harmony-algorithm, chore-division]
sources:
  - paper: doi:10.1016/0001-8708(87)90055-7
    title: Noga Alon, Splitting necklaces, Advances in Mathematics 63(3) (1987)
    locator: pp. 247-253 (the theorem for k thieves, its continuous version for measures, and the proof that the number of cuts is best possible)
  - paper: doi:10.1137/0606010
    title: Charles H. Goldberg and Douglas B. West, Bisection of circle colorings, SIAM Journal on Algebraic and Discrete Methods 6(1) (1985)
    locator: pp. 93-106 (two thieves, and a polynomial algorithm for a fixed number of colours)
  - paper: "Noga Alon and Douglas B. West, The Borsuk-Ulam theorem and bisection of necklaces, Proceedings of the American Mathematical Society 98(4) (1986), 623-628"
    locator: the short proof for two thieves with the Borsuk-Ulam theorem
  - paper: doi:10.1145/3313276.3316334
    title: Aris Filos-Ratsikas and Paul W. Goldberg, The complexity of splitting necklaces and bisecting ham sandwiches, STOC 2019
    locator: pp. 638-649 (necklace splitting for two thieves is PPA-complete)
  - paper: doi:10.1145/3519935.3520079
    title: Argyrios Deligkas, John Fearnley, Alexandros Hollender and Themistoklis Melissourgos, Constant inapproximability for PPA, STOC 2022
    locator: the abstract (hardness of the approximate versions for constant epsilon)
  - paper: "Noga Alon and Andrei Graur, Efficient splitting of measures and necklaces, arXiv:2006.16613 (2020)"
    locator: Section 1 (the history of the existence proofs, and approximation algorithms with more cuts)
---

The necklace splitting theorem says that $k$ thieves can share an open necklace fairly with few cuts. If the necklace has $k a_i$ beads of colour $i$ for $i = 1, \dots, t$, then at most $(k - 1) t$ cuts between beads are enough to split it into intervals, and to give each thief some of the intervals, so that each thief gets exactly $a_i$ beads of each colour $i$. The number of beads of each colour must be a multiple of $k$, or no exact split can exist. The bound $(k - 1) t$ cannot be improved. The theorem is the discrete form of a statement about $t$ measures on an interval; its case $k = 2$ is the existence of a [consensus halving](/consensus-halving/) with $t$ cuts. The difference between the two pages is the object: consensus halving is the computational problem for $n$ agents with continuous measures, where approximation matters, while this page is the existence theorem for beads and any number of thieves. The proofs use topology and give no efficient algorithm: for two thieves, finding the split is complete for the class PPA.

## Statement

A necklace is a sequence of beads on a line, each with one of $t$ colours. A cut is a point between two adjacent beads. A set of $c$ cuts splits the necklace into $c + 1$ intervals, and a $k$-splitting gives each interval to one of $k$ thieves.

**Theorem (Alon 1987).** Let $k \ge 2$ and $t \ge 1$, and let a necklace have $k a_i$ beads of colour $i$ for $i = 1, \dots, t$, with integers $a_i \ge 0$. Then there are at most $(k - 1) t$ cuts and a $k$-splitting in which each thief gets exactly $a_i$ beads of colour $i$, for every $i$.

**Continuous version.** Let $\mu_1, \dots, \mu_t$ be continuous probability measures on $[0, 1]$. Then $[0, 1]$ can be cut at $(k - 1) t$ points into $(k - 1) t + 1$ intervals, and these intervals can be split into $k$ families $F_1, \dots, F_k$, so that $\mu_i(\bigcup F_j) = 1/k$ for every measure $i$ and every family $j$.

For $k = 2$ the theorem is due to Goldberg and West (1985), with a short proof by Alon and West (1986); Alon proved the general case. The continuous version for $k = 2$ follows from the Hobby-Rice theorem of 1965.

## In plain words

Some thieves steal a necklace with beads of several colours. They want to share it so that each thief gets the same number of beads of each colour, but each cut costs them, so they want few cuts. The theorem says that with two thieves they never need more cuts than there are colours. With more thieves, each extra thief adds as many cuts as there are colours. For each colour, the beads must split evenly among the thieves to begin with.

No shortcut does better: if all beads of one colour sit together, every thief needs some of them, so that block alone needs a cut for each extra thief.

## Proof

We prove the case $k = 2$ in full and sketch the general case.

**Continuous version for two thieves (Alon and West).** Let $S^t$ be the set of $z = (z_0, \dots, z_t) \in \mathbb{R}^{t+1}$ with $|z_0| + \dots + |z_t| = 1$; it is a sphere of dimension $t$. For $z \in S^t$, cut $[0, 1]$ into $t + 1$ consecutive intervals $I_0, \dots, I_t$ of lengths $|z_0|, \dots, |z_t|$, and give $I_j$ to thief 1 if $z_j > 0$ and to thief 2 if $z_j < 0$ (an interval of length 0 does not matter). Let $U_1(z)$ be the part of thief 1 and define $f(z)_i = \mu_i(U_1(z)) - 1/2$ for $i = 1, \dots, t$. The map $f: S^t \to \mathbb{R}^t$ is continuous, because the measures are continuous and the cut points depend continuously on $z$. It is odd: $-z$ gives the same intervals with the thieves swapped, so $f(-z) = -f(z)$. By the Borsuk-Ulam theorem, every continuous odd map from $S^t$ to $\mathbb{R}^t$ has a zero. At a zero, thief 1 gets exactly half of every measure, with $t$ cuts.

**From measures to beads, for two thieves.** Let the necklace have $m$ beads. Put bead $b$ on the interval $[(b - 1)/m, b/m]$, and let $\mu_i$ be the uniform measure on the beads of colour $i$, scaled to total 1. The continuous version gives at most $t$ cut points at which thief 1 gets exactly $a_i$ beads' worth of colour $i$. Some cuts may lie inside beads. First delete every cut whose two sides go to the same thief; this changes no share, and afterwards the intervals alternate between the thieves. If a bead holds two cuts in a row, the parts of the bead on their far sides belong to the same thief. Slide both cuts by the same amount toward one end of the bead: one of these parts grows and the other shrinks by the same amount, and the part between the cuts keeps its length, so no share changes. Stop when a cut reaches the end of the bead. Repeat until each bead holds at most one cut. Thief 1 gets an integer number of whole beads of colour $i$, and a fraction strictly between 0 and 1 of each cut bead of colour $i$. Its total is the integer $a_i$, so the cut beads of colour $i$ cannot number exactly one. If two beads of colour $i$ hold cuts, slide both cuts at the same speed, in the directions in which the share of thief 1 of the first bead grows and its share of the second bead shrinks. Every share of every other colour stays the same, and so does the share of colour $i$. Stop when one of the cuts reaches the end of its bead. The number of cuts inside beads drops by at least one. Repeat until no cut lies inside a bead. The result has at most $t$ cuts, all between beads, and each thief gets $a_i$ beads of colour $i$. $\square$

**More thieves (sketch, Alon 1987).** For a prime $k = p$, Alon proves the continuous version with a generalization of the Borsuk-Ulam theorem to maps that respect a free action of the cyclic group of order $p$, due to Barany, Shlosman and Szucs. If the continuous version holds for $k_1$ and $k_2$ thieves, it holds for $k_1 k_2$: first split among $k_1$ groups with $(k_1 - 1) t$ cuts, then split the share of each group among $k_2$ thieves, with $(k_2 - 1) t$ cuts per group, applied to the measures restricted to that share and joined into one interval. This gives $(k_1 - 1) t + k_1 (k_2 - 1) t = (k_1 k_2 - 1) t$ cuts. Alon then deduces the discrete theorem from the continuous one.

## Consequences

- **Consensus halving exists.** The continuous version with $k = 2$ says that $n$ agents with continuous measures on $[0, 1]$ can cut it with $n$ cuts into two parts that every agent values equally. This is the existence theorem behind consensus halving.
- **Equal division of a cake with few cuts.** The continuous version for $k$ thieves is a consensus $1/k$ division: one cut set at which all $t$ agents agree that each of $k$ shares is worth $1/k$. With $k = t = n$ it gives an exact division of a [cake](/cake-cutting-problem/) among $n$ agents with $(n - 1) n$ cuts. Every agent values every share at $1/n$, so this division is [proportional](/proportional-division/) and [envy-free](/envy-freeness/), but the pieces are unions of intervals and the proof does not give a finite protocol.
- **Hard to compute.** Finding a necklace splitting for two thieves is PPA-complete (Filos-Ratsikas and Goldberg 2019). PPA is the class of total search problems that reduce in polynomial time to LEAF: given a graph of degree at most 2, described by a circuit, and a vertex of degree 1, find another vertex of degree 1, which exists because the number of such vertices is even. PPA contains [PPAD](/ppad/), and both lie in [TFNP](/tfnp/). Deligkas, Fearnley, Hollender and Melissourgos (2022) extend the hardness to constant approximation.
- **Algorithms with more cuts.** If more cuts are allowed, a fair split is easy: Alon and Graur (2020) give efficient algorithms that use more than $(k - 1) t$ cuts.
- **Few colours.** For two thieves and a fixed number $t$ of colours, a brute force over all sets of at most $t$ cuts and all ways to give out the intervals takes polynomial time in the number of beads; Goldberg and West give a faster polynomial algorithm for this case.

## Tightness

The bound $(k - 1) t$ is best possible for every $k$ and $t$. Put all beads of colour 1 first, then all beads of colour 2, and so on, with $a_i \ge 1$. Each thief needs a bead of colour $i$, so the block of colour $i$ meets at least $k$ of the intervals, and at least $k - 1$ cuts lie strictly inside this block. Different blocks have different cuts inside them, so at least $(k - 1) t$ cuts are needed.

For example, take two thieves and the necklace red, red, blue, blue. With one cut, the first part is red, red-red or red-red-blue, and none of these has one bead of each colour. With two cuts after the first and the third bead, the parts are red, red-blue and blue; thief 1 takes the first and the last part and thief 2 takes the middle part, so each gets one red and one blue bead.

The divisibility condition is needed: with $k a_i + 1$ beads of colour $i$, the thieves cannot all get the same number of them. The later form of the problem asks each thief for $\lfloor m_i / k \rfloor$ or $\lceil m_i / k \rceil$ beads of colour $i$, where $m_i$ is the number of beads of colour $i$; Alon and Graur note that it is equivalent to the form with multiples of $k$.

## History

Hobby and Rice proved in 1965 a theorem on moments in $L^1$ approximation that gives the continuous case for two thieves. Goldberg and West proved the bead case for two thieves in 1985, in a paper on bisections of circle colourings, and asked about more thieves. Alon and West gave a short proof with the Borsuk-Ulam theorem in 1986, and Alon solved the case of $k$ thieves in 1987. The computational side came much later: Filos-Ratsikas and Goldberg showed at STOC 2018 that approximate consensus halving is PPA-complete, and at STOC 2019 that necklace splitting for two thieves is PPA-complete too.

## References
