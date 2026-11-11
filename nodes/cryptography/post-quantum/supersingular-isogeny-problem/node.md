---
tag: QQP1FK
kind: problem
slug: supersingular-isogeny-problem
name: Supersingular isogeny problem
aliases:
- SSI problem
- supersingular isogeny path finding
- isogeny path problem
area: cryptography/post-quantum
level: research
summary: Given two supersingular elliptic curves over F_{p^2}, find an isogeny between them. Best known costs are O~(p^(1/2)) classical and O~(p^(1/4)) quantum.
prereqs: [isogeny-based-cryptography, breadth-first-search, meet-in-the-middle-attack]
see_also: [castryck-decru-attack, sidh, csidh, elliptic-curve-discrete-logarithm-problem, bidirectional-search, grover-search, pollard-rho-collision-search, expander-walk-sampler]
sources:
  - paper: "Christina Delfs and Steven D. Galbraith, Computing isogenies between supersingular elliptic curves over F_p, Designs, Codes and Cryptography 78(2), 2016"
    locator: the O~(p^(1/2)) algorithm for the general problem by a walk to a curve defined over F_p, and the O~(p^(1/4)) algorithm for two curves over F_p
  - paper: "Jean-Francois Biasse, David Jao and Anirudh Sankar, A quantum algorithm for computing isogenies between supersingular elliptic curves, INDOCRYPT 2014, LNCS 8885"
    locator: the quantum algorithm in O~(p^(1/4)), a Grover search for a curve over F_p followed by a subexponential quantum step on the F_p subgraph
  - paper: "Benjamin Wesolowski, The supersingular isogeny path and endomorphism ring problems are equivalent, FOCS 2021"
    locator: the main theorem, probabilistic polynomial time reductions in both directions under the generalized Riemann hypothesis
  - paper: "Kirsten Eisentraeger, Sean Hallgren, Kristin Lauter, Travis Morrison and Christophe Petit, Supersingular isogeny graphs and endomorphism rings: reductions and solutions, EUROCRYPT 2018, LNCS 10822"
    locator: the heuristic reductions between path finding and computing endomorphism rings, and the link to collisions in the CGL hash
  - paper: "David Kohel, Kristin Lauter, Christophe Petit and Jean-Pierre Tignol, On the quaternion l-isogeny path problem, LMS Journal of Computation and Mathematics 17(A), 2014"
    locator: the KLPT algorithm, which solves the path problem for maximal orders of the quaternion algebra in polynomial time
  - paper: "Denis X. Charles, Eyal Z. Goren and Kristin E. Lauter, Cryptographic hash functions from expander graphs, Journal of Cryptology 22(1), 2009"
    locator: the supersingular l-isogeny graph as a hash function, with collision resistance based on path and cycle finding
  - paper: "Arnold K. Pizer, Ramanujan graphs and Hecke operators, Bulletin of the AMS 23(1), 1990"
    locator: the proof that the supersingular l-isogeny graphs are Ramanujan graphs
  - book: "Joseph H. Silverman, The Arithmetic of Elliptic Curves, 2nd edition, Springer, 2009"
    locator: Theorem V.4.1, the count of supersingular j-invariants in characteristic p
  - paper: "Wouter Castryck and Thomas Decru, An efficient key recovery attack on SIDH, EUROCRYPT 2023, LNCS 14008"
    locator: the polynomial time attack on the SIDH variant, which uses the images of torsion points and does not apply to the general problem
---

The supersingular isogeny problem asks for an isogeny between two given supersingular elliptic curves over $\mathbb{F}_{p^2}$. It is the hard problem under most of [isogeny-based cryptography](/isogeny-based-cryptography/): the CGL hash, SQIsign and, in a special form over $\mathbb{F}_p$, [CSIDH](/csidh/). The best known algorithms take $\tilde O(p^{1/2})$ time on a classical computer (Delfs and Galbraith, 2016) and $\tilde O(p^{1/4})$ on a quantum computer (Biasse, Jao and Sankar, 2014). Wesolowski (FOCS 2021) proved, under the generalized Riemann hypothesis, that it is equivalent to computing endomorphism rings. The SIDH variant, which also gives the images of torsion points, is a different and much easier problem: it is broken in polynomial time by the [Castryck-Decru attack](/castryck-decru-attack/) and its successors.

**Notation.** $p$ is a large prime and $\ell$ a small prime, $\ell \neq p$. An isogeny $\varphi : E_1 \to E_2$ is a nonconstant rational map that sends the point at infinity to the point at infinity; it is a group homomorphism. $\deg \varphi$ is its degree; for a separable isogeny this is the size of its kernel. $j(E)$ is the j-invariant, which fixes the curve up to isomorphism over $\overline{\mathbb{F}}_p$. $G_\ell(p)$ is the supersingular $\ell$-isogeny graph: one vertex for each supersingular j-invariant, one edge for each isogeny of degree $\ell$ up to isomorphism. $\mathrm{End}(E)$ is the ring of endomorphisms of $E$. $\tilde O(f)$ means $O(f \cdot (\log f)^c)$ for some constant $c$.

## In plain words

Think of a large maze where each room is a special kind of curve and each door is a simple map from one curve to another. Every room has the same small number of doors, and the maze is so well connected that any two rooms are joined by a short route. You are put in one room and told the name of another. The task is to find a route between them.

A short route always exists, but nobody knows a quick way to find it. The best known plan is to search from both ends and wait for the two searches to meet, which takes about the square root of the number of rooms. A quantum computer does better, but still needs a time that grows fast with the size of the maze.

## Definition

**Input.** A prime $p$ and two supersingular elliptic curves $E_1$ and $E_2$ over $\mathbb{F}_{p^2}$.

**Output.** An isogeny $\varphi : E_1 \to E_2$, given in a form that can be evaluated efficiently. The usual form is a chain of isogenies of small prime degree $\ell$, each given by its kernel or its rational maps. This is a path from $j(E_1)$ to $j(E_2)$ in $G_\ell(p)$, so the problem is also called the $\ell$-isogeny path problem.

Some facts make the problem well posed. Every supersingular j-invariant lies in $\mathbb{F}_{p^2}$, and there are $\lfloor p/12 \rfloor + \{0, 1, 2\}$ of them (Silverman, Theorem V.4.1), so $G_\ell(p)$ has about $p/12$ vertices. Each vertex has $\ell + 1$ outgoing edges, counted with multiplicity. Pizer (1990) proved that $G_\ell(p)$ is a Ramanujan graph, so it is connected and has diameter $O(\log p)$. Thus a path of length $O(\log p)$ always exists, and its description has polynomial size. The problem is to find one.

## Variants

**Path problem in a fixed graph.** Find a path in $G_\ell(p)$ for a given $\ell$, usually $\ell = 2$ or $3$. Any isogeny of smooth degree can be split into such steps, so this is the standard form.

**Endomorphism ring problem.** Given one supersingular curve $E$, compute a basis of $\mathrm{End}(E)$, which is a maximal order in the quaternion algebra over $\mathbb{Q}$ ramified at $p$ and at infinity. The Deuring correspondence links curves to such orders, and the KLPT algorithm of Kohel, Lauter, Petit and Tignol (2014) finds paths between orders in polynomial time. That is why this problem and the path problem are equivalent (see Reductions).

**Curves over $\mathbb{F}_p$.** When $E_1$ and $E_2$ are both defined over $\mathbb{F}_p$, one can restrict to isogenies defined over $\mathbb{F}_p$. These form the action of a commutative class group, and the problem becomes the inversion of a group action, a hidden shift problem. Delfs and Galbraith solve it in $\tilde O(p^{1/4})$ classically, and Kuperberg-type algorithms solve it in subexponential time on a quantum computer. This is the problem under [CSIDH](/csidh/).

**SIDH variant (computational supersingular isogeny problem).** The secret isogeny $\varphi_A : E_0 \to E_A$ has the fixed degree $2^{e_A}$, and the instance also contains $\varphi_A(P_B)$ and $\varphi_A(Q_B)$ for a public basis $(P_B, Q_B)$ of $E_0[3^{e_B}]$. This extra information is what [SIDH](/sidh/) published. It is much weaker than the general problem: Castryck and Decru (2022), Maino, Martindale, Panny, Pope and Wesolowski, and Robert solve it in polynomial time with isogenies between products of curves. See [Castryck-Decru attack](/castryck-decru-attack/). These attacks need the torsion images and give nothing for the general problem, so a break of SIDH is not a break of the problem on this page.

## Examples

**The toy graph at $p = 431$.** Here $p \equiv 11 \pmod{12}$, so $G_2(431)$ has $\lfloor 431/12 \rfloor + 2 = 37$ vertices, 21 of them in $\mathbb{F}_{431}$. The code with this page builds the graph from $E_0 : y^2 = x^3 + x$, which has $j = 1728 \equiv 4$, with Velu's formulas. A shortest path from $j = 4$ to $j = 102$, one of the vertices farthest from $4$, is

$$4 \to 19 \to 234 \to 242 \to 67 \to 304 + 67i \to 319 \to 102,$$

of length 7, which is the largest distance from $4$. The code then turns the path back into seven 2-isogenies with Velu's formulas, so the composite map $E_0 \to E$ of degree $2^7$ has $j(E) = 102$. Search from $4$ alone touches all 37 vertices before it reaches $102$; search from both ends touches 33 in total. The graph is too small for a real gap.

**A larger toy graph.** At $p = 10007$ the graph has $835$ vertices. For 40 random pairs (seed 7), the mean distance is $7.95$ and the largest is $11$. One-sided search touches $569$ vertices on average and search from both ends touches $106$, both balls together. The ratio grows with $p$: a ball of radius $d$ has about $2^d$ vertices, and two balls of radius $d/2$ have about $2 \cdot 2^{d/2}$.

**Non-example.** Curves that are not supersingular, the ordinary curves, are not instances. Their isogeny graphs are volcanoes, and the analogous problem has a different structure and a quantum subexponential algorithm (Childs, Jao and Soukharev, 2014).

**The toy code.** The Python code builds the full graph, which is only possible for toy $p$, and compares the two searches. It is for study only and is not constant time. There is no production library for this problem; for post-quantum security in practice, use ML-KEM or ML-DSA from a FIPS 140 validated module.

## Known algorithms

**Meet in the middle.** Grow breadth-first balls around $j(E_1)$ and $j(E_2)$ until they share a vertex. Each ball must reach about $\sqrt{p/12}$ vertices before a collision is likely, so time and memory are $\tilde O(p^{1/2})$. With the collision search of van Oorschot and Wiener the memory becomes small and the time stays $\tilde O(p^{1/2})$.

**Delfs and Galbraith (2016).** About $\tilde O(p^{1/2})$ of the $p/12$ vertices are defined over $\mathbb{F}_p$. A random walk from each of $E_1$ and $E_2$ reaches such a vertex after $\tilde O(p^{1/2})$ steps. Between two curves over $\mathbb{F}_p$, a meet in the middle on the $\mathbb{F}_p$ subgraph, which has about $p^{1/2}$ vertices, takes $\tilde O(p^{1/4})$. The total is $\tilde O(p^{1/2})$ time with polynomial memory. This is the best classical algorithm known for the general problem.

**Biasse, Jao and Sankar (2014).** Replace the walk to an $\mathbb{F}_p$ curve by a Grover search, which cuts $\tilde O(p^{1/2})$ to $\tilde O(p^{1/4})$, and solve the $\mathbb{F}_p$ step with a quantum subexponential algorithm. The total is $\tilde O(p^{1/4})$ quantum time.

**Through the endomorphism ring.** If $\mathrm{End}(E_1)$ and $\mathrm{End}(E_2)$ are known, KLPT finds a path in polynomial time. So any fast way to compute endomorphism rings would solve the problem.

**SIDH variant.** Before 2022, the best attack on SIDH ignored the torsion images: a meet in the middle on isogenies of degree $2^{e_A} \approx p^{1/2}$, in $\tilde O(p^{1/4})$ time. Quantum claw finding (Tani) gives $\tilde O(p^{1/6})$, but Jaques and Schanck (CRYPTO 2019) showed that it is not cheaper than the classical attack once memory cost is counted. Since 2022 the variant is solved in polynomial time; see [Castryck-Decru attack](/castryck-decru-attack/).

## Bounds

No lower bound is known beyond the trivial one. The size of the output is polynomial in $\log p$, since a path of length $O(\log p)$ exists. The upper bounds above, $\tilde O(p^{1/2})$ classical and $\tilde O(p^{1/4})$ quantum, have not been improved for the general problem since 2016 and 2014, which is the main evidence that it is hard. A generic walk on an expander graph needs $\Omega(\sqrt{N})$ queries to find a collision among $N$ vertices, but this does not bound algorithms that use the algebra of the curves.

For parameters, this means a prime of $2\lambda$ bits gives about $\lambda$ bits of classical security against the general problem. SQIsign at NIST category 1 uses $p$ of about 250 bits.

## Reductions

**Path and endomorphism ring are equivalent.** Eisentraeger, Hallgren, Lauter, Morrison and Petit (EUROCRYPT 2018) gave reductions in both directions under heuristics. Wesolowski (FOCS 2021) proved them under the generalized Riemann hypothesis only: given an algorithm for one problem, the other is solved in probabilistic polynomial time.

**CGL hash collisions.** A collision in the hash of Charles, Goren and Lauter gives a cycle in $G_\ell(p)$, which is a nontrivial endomorphism of a curve. So path finding, through the endomorphism ring, gives collisions, and collision resistance rests on this problem.

**The SIDH variant reduces to the general problem.** An algorithm for the general problem, with a degree constraint, solves the SIDH variant. The converse is false as far as anyone knows: the polynomial time attacks on SIDH use the torsion images in an essential way.

**The $\mathbb{F}_p$ variant.** Path finding between curves over $\mathbb{F}_p$ is the inversion of the class group action of CSIDH, which reduces to a hidden shift problem in an abelian group.

## Applications

- The CGL hash function, whose collision resistance rests on path and cycle finding.
- SQIsign, a NIST additional signature candidate, whose security rests on this problem and the endomorphism ring problem.
- [CSIDH](/csidh/) and related group actions, which use the $\mathbb{F}_p$ variant.
- [SIDH](/sidh/) and SIKE used the SIDH variant, which is broken. This shows that extra public information can change the problem completely.

## References
