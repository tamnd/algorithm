---
tag: FFWYTM
kind: algorithm
slug: quantum-class-group-algorithm
name: Quantum class group algorithm
aliases:
- Hallgren's class group algorithm
- Schmidt-Vollmer algorithm
area: quantum/quantum-number-theory
level: research
summary: A quantum algorithm that finds the class group of a number field by Fourier sampling of the relations among small prime ideals. It is polynomial-time under GRH for quadratic and fixed-degree fields.
solves: [ideal-class-group]
model: quantum-circuit-model
complexity:
  vars: {n: "the bit length of the absolute value of the discriminant", k: "the number of generating prime ideals or prime forms"}
  time: {quantum_per_sample: poly(n), expected_samples: O(n), classical: poly(n)}
  space: {qubits_imaginary_quadratic: O(k n), qubits_general: poly(n)}
properties: {deterministic: false, exact: true, las_vegas: true, quantum: true}
history:
  year: 2002
  people: [Sean Hallgren]
  note: Cheung and Mosca noted in 2001 that their quantum decomposition of abelian groups computes class numbers under GRH. Hallgren treated real quadratic fields in 2002 and fields of constant degree in 2005.
prereqs: [ideal-class-group, smith-normal-form, quantum-fourier-transform, order-finding]
see_also: [quantum-principal-ideal-algorithm, hallgren-pell-algorithm, principal-ideal-problem, unit-group, fourier-sampling, shor-algorithm, csidh, hermite-normal-form]
sources:
  - paper: arxiv:cs/0101004
    title: Kevin K. H. Cheung and Michele Mosca, Decomposing finite abelian groups, 2001
    locator: the quantum algorithm for the structure of a finite abelian group with unique encodings, and its use for class numbers under the generalized Riemann hypothesis
  - paper: doi:10.1145/1206035.1206039
    title: "Sean Hallgren, Polynomial-time quantum algorithms for Pell's equation and the principal ideal problem, Journal of the ACM 54(1), Article 4, 2007"
    locator: the computation of the class group of a real quadratic field under the generalized Riemann hypothesis
  - paper: doi:10.1145/1060590.1060660
    title: "Sean Hallgren, Fast quantum algorithms for computing the unit group and class group of a number field, STOC 2005"
    locator: the unit group and class group of number fields of constant degree
  - paper: doi:10.1145/1060590.1060661
    title: "Arthur Schmidt and Ulrich Vollmer, Polynomial time quantum algorithm for the computation of the unit group of a number field, STOC 2005"
    locator: the independent quantum algorithm for the unit group of a number field of constant degree
  - paper: doi:10.1137/1.9781611974331.ch64
    title: "Jean-François Biasse and Fang Song, Efficient quantum algorithms for computing class groups and solving the principal ideal problem in arbitrary degree number fields, SODA 2016"
    locator: the class group in arbitrary degree through S-unit groups, under the generalized Riemann hypothesis
  - paper: doi:10.1103/RevModPhys.82.1
    title: "Andrew M. Childs and Wim van Dam, Quantum algorithms for algebraic problems, Reviews of Modern Physics 82:1-52, 2010"
    locator: the survey sections on the abelian hidden subgroup problem, decomposing abelian groups, and number fields
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138, Springer, 1993
    locator: Chapter 5, reduction and composition of binary quadratic forms
---

The quantum class group algorithm computes the ideal class group of a number field from a set of small prime ideals that generate it. A quantum computer samples the dual of the lattice of relations among the generators, and classical integer linear algebra turns the samples into the relation lattice and the Smith normal form gives the group structure. For imaginary quadratic fields, where each class has a unique reduced form, this is a hidden subgroup problem on a finite abelian group, and Hallgren extended it to real quadratic fields and to fields of constant degree. All these results run in time polynomial in the size of the discriminant, under the generalized Riemann hypothesis (GRH).

## In plain words

The class group sorts the ideals of a number field into classes. A few small ideals are enough to reach every class by multiplying them together. The question is which products of these small ideals land back in the trivial class. These products are the relations, and they fix the shape of the group.

Classical computers find relations slowly. A quantum computer prepares all products at once, writes down the class of each product, and then applies a Fourier transform. Each measurement gives a random hint about the relations. After a few dozen hints, ordinary linear algebra rebuilds all relations, and a standard matrix form reads off the group.

The method needs a unique way to write each class. For imaginary quadratic fields this is easy, and for other fields it takes extra work.

## The problem

The input is a number field $K$ with discriminant $\Delta_K$. The output is the structure $\mathrm{Cl}_K \cong \mathbb{Z}/d_1 \times \cdots \times \mathbb{Z}/d_m$ with $d_1 \mid \cdots \mid d_m$ and generators, as on the page on [class group computation](/ideal-class-group/). The size of the input is $n = \log_2|\Delta_K|$.

This page gives the algorithm for an imaginary quadratic discriminant $\Delta < 0$. Here $\mathrm{Cl}(\Delta)$ is the group of primitive positive definite forms $(a, b, c)$ with $b^2 - 4ac = \Delta$ under composition, and each class has exactly one reduced form, with $|b| \le a \le c$. So the reduced form is a unique encoding of the class. The prime forms $(p, b, c)$ of primes $p \le B$ generate the group for $B = \sqrt{|\Delta|/3}$, and under GRH for Bach's bound $B = 12(\ln|\Delta|)^2$. For $y$ in $G = \mathbb{Z}_{r_1} \times \cdots \times \mathbb{Z}_{r_k}$, the Fourier transform of $G$ maps $|x\rangle$ to $|G|^{-1/2}\sum_y e^{2\pi i\sum_i x_i y_i/r_i}|y\rangle$. Qubit 0 of each register is its least significant bit.

## The algorithm

Let $f(x) = g_1^{x_1}\cdots g_k^{x_k}$, reduced. It is constant on the cosets of the subgroup $H \subseteq G$ of relations and takes different values on different cosets. The algorithm solves this hidden subgroup problem with [Fourier sampling](/fourier-sampling/): each sample is uniform in the dual group $H^\perp$, the set of $y$ with $\sum_i x_i y_i/r_i \in \mathbb{Z}$ for every relation $x$.

```pseudo id=main
QUANTUM-CLASS-GROUP(Δ, B)          ▷ Δ < 0; the prime forms of norm ≤ B generate Cl(Δ)
L1  g_1, ..., g_k ← the reduced prime forms (p, b, c) with p ≤ B prime and b^2 ≡ Δ (mod 4p)
L2  r_i ← the order of g_i by quantum order finding; drop the g_i with r_i = 1
L3  Y ← ∅
L4  repeat
L5      prepare (r_1 ⋯ r_k)^(-1/2) Σ_{x ∈ Z_{r_1} × ⋯ × Z_{r_k}} |x⟩|0⟩
L6      apply |x⟩|0⟩ → |x⟩|reduce(g_1^{x_1} ⋯ g_k^{x_k})⟩
L7      apply the QFT of Z_{r_i} to register i, for each i
L8      measure y = (y_1, ..., y_k); Y ← Y ∪ {y}
L9      L ← {x ∈ Z^k : Σ_i x_i y_i / r_i ∈ Z for all y ∈ Y}      ▷ integer linear algebra
L10 until g_1^{x_1} ⋯ g_k^{x_k} = 1 for every x in a basis of L
L11 D ← U A W, the Smith normal form of a basis matrix A of L, with D = diag(d_1, ..., d_k)
L12 h_i ← g_1^{w_i1} ⋯ g_k^{w_ik}, where (w_i1, ..., w_ik) is row i of W^(-1), for each d_i > 1
L13 return the invariants d_i > 1, the generators h_i, and h = Π d_i
```

Line L2 uses [order finding](/order-finding/) for each generator. Line L9 solves $Ax \equiv 0 \pmod M$ with $M = \mathrm{lcm}(r_i)$ and the rows $(y_1 M/r_1, \dots, y_k M/r_k)$ of $A$, through the integer kernel of $[A \mid MI]$. The set $L$ always contains the true relation lattice, so the check of line L10 holds exactly when $L$ equals it.

## Example

Take $\Delta = -260$, with class number 8. The bound is $\sqrt{260/3} \approx 9.3$, and line L1 gives the prime forms $g_1 = (2, 2, 33)$, $g_2 = (3, 2, 22)$ and $g_3 = (5, 0, 13)$. The prime 7 is inert. The powers of $g_2$ are $(1, 0, 65)$, $(3, 2, 22)$, $(9, 8, 9)$, $(3, -2, 22)$ and $(1, 0, 65)$, so order finding gives the orders $2$, $4$ and $2$. Each order finding run uses a 7-qubit input register and a 3-qubit target.

The group $G = \mathbb{Z}_2 \times \mathbb{Z}_4 \times \mathbb{Z}_2$ needs $1 + 2 + 1$ qubits, and the target needs 3 more. The relation subgroup is $H = \{0, (1, 2, 1)\}$, because $g_1 g_3 = g_2^2 = (9, 8, 9)$. So the samples are uniform on the 8 elements of $H^\perp$: $(0,0,0)$, $(0,1,1)$, $(0,2,0)$, $(0,3,1)$, $(1,0,1)$, $(1,1,0)$, $(1,2,1)$ and $(1,3,0)$, each with probability $1/8$.

One run with seed 1 samples $(1, 2, 1)$, $(0, 0, 0)$, $(0, 0, 0)$, $(1, 2, 1)$ and $(0, 3, 1)$. After the first four samples, $L$ still contains a vector such as $(-1, 1, 0)$ that is not a relation, so line L10 fails. The fifth sample completes a generating set of $H^\perp$. Then line L9 gives $L$ generated by $(-1, -2, 3)$, $(-2, 0, 0)$ and $(2, 0, -2)$, all relations. The Smith normal form has the diagonal $(1, 2, 4)$, and rows 2 and 3 of $W^{-1}$ give the generators $(2, 2, 33)$ and $(3, 2, 22)$. So $\mathrm{Cl}(-260) \cong \mathbb{Z}/2 \times \mathbb{Z}/4$ and $h = 8$.

## Correctness

Each class has one reduced form, so $f(x) = f(x')$ exactly when $x - x' \in H$. After the Fourier transform, the amplitude of $|y\rangle$ next to a coset is a sum of the character $\chi_y$ over $H$, which is $|H|$ for $y \in H^\perp$ and 0 otherwise. So each sample is uniform on $H^\perp$, a group of order $h$. The lattice $L$ of line L9 always contains the relation lattice $\Lambda$, and by duality of finite abelian groups it equals $\Lambda$ exactly when the samples generate $H^\perp$. Line L10 checks $L \subseteq \Lambda$ directly, so the loop ends with $L = \Lambda$. While the samples generate a proper subgroup, a new sample leaves it with probability at least $1/2$ and at least doubles it, so about $2\log_2 h$ samples suffice on average. Finally $\mathbb{Z}^k/\Lambda \cong \mathrm{Cl}(\Delta)$, and the Smith normal form splits it into cyclic factors. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

- **One sample.** Line L6 takes $k$ exponentiations of forms with exponents below the class number, each with $O(n)$ compositions of $O(n)$-bit forms. The register for $x$ has $O(kn)$ qubits. So one sample costs time polynomial in $n$ and $k$.
- **Samples.** The expected number of samples is at most $2\log_2 h + 1 = O(n)$, since $h = |\Delta|^{1/2 + o(1)}$.
- **Generators.** With Bach's bound under GRH, $k = O(n^2)$, so the whole algorithm is polynomial in $n$. With the unconditional bound $\sqrt{|\Delta|/3}$, $k$ is exponential in $n$.
- **Classical part.** The kernel and the Smith normal form of integer matrices with $O(n)$ rows and $k$ columns take polynomial time, and the check of line L10 takes $k$ exponentiations per basis vector.
- **Other fields.** For real quadratic fields and fields of constant degree, the quantum part also has to handle distances or the unit lattice, and the cost stays polynomial in $n$ under GRH.

## Properties

- **Las Vegas.** Line L10 checks every basis vector of $L$ as a relation, so a returned structure is always right if the generators generate the group. Only the number of samples is random.
- **Uses GRH only for the generators.** The quantum steps and the check are unconditional. GRH enters through Bach's bound, which makes the generating set of polynomial size.
- **A hidden subgroup algorithm.** For imaginary quadratic fields, the method is the general abelian hidden subgroup algorithm applied to a group with unique encodings and efficient operations.
- **Gives discrete logarithms too.** Adding a target class $\mathfrak{a}$ as an extra generator gives a relation that writes $\mathfrak{a}$ in terms of the $h_i$.

## Variants and improvements

- **Decomposing abelian groups.** Cheung and Mosca gave a quantum algorithm that decomposes any finite abelian group with unique encodings, and they noted that it computes class numbers under GRH. The algorithm on this page follows their outline.
- **Real quadratic fields.** Here a class has many reduced ideals, which lie on a cycle with distances, so $f$ has no unique value. Hallgren (2002) combined the class of $g_1^{x_1}\cdots g_k^{x_k}$ with a position on its cycle, as in [Hallgren's algorithm for Pell's equation](/hallgren-pell-algorithm/), and solved the resulting hidden subgroup problem on $\mathbb{Z}^k \times \mathbb{R}$. The regulator comes out at the same time.
- **Constant degree.** Hallgren (2005) extended the method to number fields of constant degree, where the hidden subgroup lives on $\mathbb{Z}^k \times \mathbb{R}^r$ with the unit rank $r$. Schmidt and Vollmer (2005) independently gave the [unit group](/unit-group/) algorithm for these fields, which is the part that needs the continuous periods.
- **Any degree.** Biasse and Song (2016) computed the class group in time polynomial in the degree as well, under GRH, by computing $S$-unit groups with the continuous hidden subgroup algorithm of Eisenträger, Hallgren, Kitaev and Song. That method also solves the principal ideal problem and is the subject of the [quantum principal ideal algorithm](/quantum-principal-ideal-algorithm/). This page covers the direct hidden subgroup approach on the class group, and that page covers the $S$-unit approach.

## When to use it

Use it to compute class groups, class numbers and discrete logarithms in class groups on a quantum computer, for example to attack cryptosystems based on groups of unknown order from imaginary quadratic fields. For quadratic fields it is the simplest quantum method. For fields of large degree, use the $S$-unit method of Biasse and Song. A class group algorithm alone does not break [CSIDH](/csidh/), whose security rests on a hidden shift problem in the class group action. Classically, use the subexponential relation methods on the page on [class group computation](/ideal-class-group/).

## Pitfalls

- **Use the reduced form.** The oracle must write the unique reduced form of each class. With an unreduced form, equal classes get different values, and the samples are no longer uniform on $H^\perp$.
- **The generators must generate.** If the prime forms of line L1 generate only a subgroup, the algorithm returns that subgroup and the check of line L10 still passes. Use Bach's bound under GRH or the unconditional bound, or compare $h$ with an estimate from the class number formula.
- **Zero samples.** The sample $y = 0$ carries no information and comes with probability $1/h$. For a small group, as in the example, several samples are needed even for 3 generators.
- **Register sizes in order finding.** The order finding register must satisfy $2^t \ge 2B_h^2$ for a bound $B_h$ on the class number, or the convergents can miss the order. A wrong denominator gives a multiple of the order, which the implementation reduces by trying $r/p$.
- **The simulation is small.** The implementation computes $f$ by repeated composition and uses the class number as the order bound, so that every circuit fits in 12 qubits. A real circuit composes forms in superposition and uses a bound such as $\sqrt{|\Delta|}\ln|\Delta|$.

## Implementations

## History

Gauss introduced composition of binary quadratic forms in 1801, and the computation of class groups has been a central task of algorithmic number theory since Shanks' baby-step giant-step method of the 1970s and the subexponential relation methods of Hafner and McCurley (1989) and Buchmann (1990). In 2001 Cheung and Mosca gave a quantum algorithm for the structure of finite abelian groups and noted that it computes class numbers under GRH. In 2002 Hallgren computed the class group of real quadratic fields, where classes have no unique encoding, in quantum polynomial time under GRH. In 2005 Hallgren extended this to fields of constant degree, and Schmidt and Vollmer gave an independent unit group algorithm for such fields. In 2016 Biasse and Song removed the restriction on the degree.

## References
