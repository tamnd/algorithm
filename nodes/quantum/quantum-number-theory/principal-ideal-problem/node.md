---
tag: 6WEB0R
kind: problem
slug: principal-ideal-problem
name: Principal ideal problem
aliases: []
area: quantum/quantum-number-theory
level: research
summary: Given an ideal of a number field, decide whether it is principal and, if so, find a generator. It is subexponential classically and polynomial on a quantum computer.
prereqs: [ideal-class-group, unit-group]
see_also: [quantum-principal-ideal-algorithm, hallgren-pell-algorithm, quantum-class-group-algorithm, pell-equation, ring-lwe-hardness, closest-vector-problem, lll-algorithm, hermite-normal-form]
sources:
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138, Springer, 1993
    locator: Chapter 5, reduction of quadratic forms and ideals, and the later chapter on testing whether an ideal of a number field is principal
  - paper: "Johannes Buchmann, A subexponential algorithm for the determination of class groups and regulators of algebraic number fields, Seminaire de Theorie des Nombres, Paris 1988-1989, Progress in Mathematics 91, Birkhauser, 1990, pp. 27-41"
    title: Johannes Buchmann, A subexponential algorithm for the determination of class groups and regulators of algebraic number fields
    locator: the relation method, which also tests whether an ideal is principal
  - paper: doi:10.1145/1206035.1206039
    title: "Sean Hallgren, Polynomial-time quantum algorithms for Pell's equation and the principal ideal problem, Journal of the ACM 54(1), Article 4, 2007"
    locator: the quantum algorithm for the principal ideal problem in real quadratic fields, and its relation to Pell's equation and the Buchmann-Williams key exchange
  - paper: doi:10.1145/1060590.1060660
    title: "Sean Hallgren, Fast quantum algorithms for computing the unit group and class group of a number field, STOC 2005"
    locator: the quantum algorithms for number fields of constant degree
  - paper: doi:10.1137/1.9781611974331.ch64
    title: "Jean-François Biasse and Fang Song, Efficient quantum algorithms for computing class groups and solving the principal ideal problem in arbitrary degree number fields, SODA 2016"
    locator: the quantum polynomial-time algorithm for the principal ideal problem in number fields of any degree, through S-unit groups
  - paper: doi:10.1007/978-3-662-49896-5_20
    title: "Ronald Cramer, Léo Ducas, Chris Peikert and Oded Regev, Recovering short generators of principal ideals in cyclotomic rings, EUROCRYPT 2016"
    locator: the reduction from any generator to a short one with the log-unit lattice of a cyclotomic field
  - paper: doi:10.1103/RevModPhys.82.1
    title: "Andrew M. Childs and Wim van Dam, Quantum algorithms for algebraic problems, Reviews of Modern Physics 82:1-52, 2010"
    locator: the survey section on Pell's equation and the principal ideal problem
---

The principal ideal problem asks, for an ideal $\mathfrak{a}$ of the ring of integers of a number field, whether $\mathfrak{a} = \alpha\mathcal{O}_K$ for a single element $\alpha$, and if so, for such a generator. The generator is unique only up to a unit and can be huge, so it is given in compact form or, in real quadratic fields, by its distance. Classical methods take subexponential time except in easy cases such as imaginary quadratic fields. Quantum algorithms solve it in polynomial time, by Hallgren for real quadratic fields and by Biasse and Song for any degree, and this breaks several cryptosystems built on ideal lattices.

## In plain words

In a number field, an ideal is a set of numbers closed under addition and under multiplication by any whole number of the field. Some ideals are simply all the multiples of one number. These are the principal ideals, and that one number is a generator.

The problem gives an ideal, usually by a few numbers that span it, and asks two things. Is it principal? If yes, what is a generator?

This is hard because a generator can be far larger than the numbers that describe the ideal. Classical computers check only slowly for large fields. Quantum computers find the answer fast, and this matters for cryptography: some encryption schemes hide their secret key as the generator of an ideal.

## Definition

Let $K$ be a number field of degree $n$ with ring of integers $\mathcal{O}_K$ and discriminant $\Delta_K$. An integral ideal $\mathfrak{a} \subseteq \mathcal{O}_K$ is given by a $\mathbb{Z}$-basis, usually in [Hermite normal form](/hermite-normal-form/) with respect to an integral basis of $\mathcal{O}_K$, or by two generators. The ideal is **principal** if $\mathfrak{a} = \alpha\mathcal{O}_K$ for some $\alpha \in \mathcal{O}_K$. Then the set of all generators is $\alpha\mathcal{O}_K^\ast$, the multiples of $\alpha$ by [units](/unit-group/).

- **Decision version.** Decide whether $\mathfrak{a}$ is principal, that is, whether its class in the [class group](/ideal-class-group/) is trivial.
- **Search version.** Given that $\mathfrak{a}$ is principal, find a generator $\alpha$. Because $\alpha$ can have coefficients with a number of digits exponential in $\log|\Delta_K|$, the output is a compact representation, a product of powers of elements of polynomial size, or the logarithmic embedding of $\alpha$ to a given precision.

In a real quadratic field the reduced principal ideals form a cycle with distances, as on the page on [Pell's equation](/pell-equation/). There the search version asks for the distance $\delta$ of a reduced ideal $\mathfrak{a}$ on the principal cycle, which is $\ln$ of a generator up to multiples of the regulator $R$.

## Variants

- **Short generators.** Given a principal ideal that has an unusually short generator, find it. This version arises in cryptography and needs a generator and a reduction by the unit lattice.
- **Class group discrete logarithm.** Given generators of the class group, write the class of $\mathfrak{a}$ in terms of them. The ideal is principal when all coordinates are 0, and a relation then gives a generator.
- **Norm equations.** Find elements of a given norm $N$. Their principal ideals have norm $|N|$, so this reduces to the principal ideal problem for the ideals of norm $|N|$, together with the units. The equation $x^2 - Dy^2 = N$ is the real quadratic case.
- **Orders.** The same question for invertible ideals of a non-maximal order.

## Examples

**The Gaussian integers.** In $\mathbb{Z}[i]$, every ideal is principal. The ideal $(5, 2 + i)$ has norm 5, and $2 + i$ has norm $4 + 1 = 5$ and lies in it, so $(5, 2 + i) = (2 + i)$. In small fields with class number 1, an element of the right norm in the ideal is a generator.

**A non-principal ideal.** In $\mathbb{Z}[\sqrt{-5}]$, the ideal $\mathfrak{p} = (2, 1 + \sqrt{-5})$ has norm 2. A generator $a + b\sqrt{-5}$ would have $a^2 + 5b^2 = 2$, which has no integer solution, so $\mathfrak{p}$ is not principal. Its square $\mathfrak{p}^2 = (2)$ is principal.

**A real quadratic field.** In $\mathbb{Z}[\sqrt 7]$, the reduced ideal $[3, 2 + \sqrt 7]$ is principal with the generator $2 + \sqrt 7$, whose norm is $4 - 7 = -3$. Its distance on the principal cycle is $\ln(2 + \sqrt 7) \approx 1.5360$, and every generator has the form $\pm(2 + \sqrt 7)(8 + 3\sqrt 7)^u$.

**Large generators.** In $\mathbb{Z}[\sqrt{94}]$, the ideal $(1)$ already has the generator $2143295 + 221064\sqrt{94}$ besides $1$. For larger $D$ the reduced principal ideals far along the cycle have generators with a number of digits that grows like $\sqrt D$, while their $\mathbb{Z}$-bases stay below $2\sqrt D$.

## Known algorithms

**Classical.**

- **Imaginary quadratic fields.** Each class contains exactly one reduced form, and reduction takes polynomial time. So $\mathfrak{a}$ is principal exactly when its form reduces to the principal form, and the reduction steps give a generator of polynomial size. This case is easy.
- **Real quadratic fields.** Reduce $\mathfrak{a}$ to a reduced ideal and search for it on the principal cycle. Walking the cycle takes about $R$ steps, and Shanks' baby-step giant-step method in the infrastructure takes about $\sqrt R$ steps up to logarithmic factors, so about $D^{1/4}$. Buchmann's relation method takes subexponential time under the generalized Riemann hypothesis (GRH).
- **General number fields.** Relation methods compute the class group and the $S$-unit group for a factor base of small prime ideals, then factor $\mathfrak{a}$ times a random element over the base and solve a linear system for its class and a generator. For fields of fixed degree this takes subexponential time in $\log|\Delta_K|$ under GRH, and later heuristic methods improve it for special families such as cyclotomic fields.
- **From a generator to a short one.** Cramer, Ducas, Peikert and Regev showed that in cyclotomic fields of prime-power conductor, the log-unit lattice has a known, well-behaved basis of cyclotomic units. So a [closest vector](/closest-vector-problem/) step with this basis turns any generator into the short one, if it exists, in classical polynomial time.

**Quantum.**

- **Real quadratic fields.** Hallgren (2002) gave a polynomial-time algorithm that finds the distance of a generator, with the same irrational period finding as in [Hallgren's algorithm for Pell's equation](/hallgren-pell-algorithm/). The period now appears in a function of two variables that combines the principal cycle with the cycle that contains $\mathfrak{a}$.
- **Constant degree.** Hallgren (2005) extended the method to fields of constant degree.
- **Any degree.** Biasse and Song (2016) solved the problem in time polynomial in $n$ and $\log|\Delta_K|$. They compute an $S$-unit group with the continuous hidden subgroup algorithm of Eisenträger, Hallgren, Kitaev and Song, where $S$ contains the primes that divide $\mathfrak{a}$, and read the generator off a relation. See [quantum principal ideal algorithm](/quantum-principal-ideal-algorithm/).

## Bounds

A generator can have coefficients with a number of digits about $R_K$, which can be close to $\sqrt{|\Delta_K|}$, so the output must be in compact form. No classical polynomial-time algorithm is known except in special cases such as imaginary quadratic fields, while the quantum algorithms above run in polynomial time. The search version is at least as hard as computing the regulator in real quadratic fields, as Hallgren notes, so it is at least as hard as [Pell's equation](/pell-equation/).

## Reductions

- **From Pell's equation.** In a real quadratic field, the distances of the generators of $(1)$ are the multiples of $R$, and a principal ideal problem solver with distances finds them. So Pell's equation reduces to the principal ideal problem, and through it factoring does too.
- **To the class group and $S$-units.** Given the structure of the class group and an $S$-unit group for a factor base, the problem becomes linear algebra over the integers. This is the route of both the classical relation methods and the quantum algorithm of Biasse and Song.
- **To the short generator problem.** The short generator problem reduces to the search version plus a closest vector problem in the log-unit lattice, which is easy in cyclotomic fields of prime-power conductor.

## Applications

- **The Buchmann-Williams key exchange.** This key exchange in real quadratic fields rests on the difficulty of the principal ideal problem. Hallgren's quantum algorithm breaks it.
- **Lattice schemes on principal ideals.** Soliloquy, the Smart-Vercauteren encryption scheme, and some candidate multilinear maps hide a short secret as the generator of a principal ideal of a cyclotomic field. A quantum algorithm for the principal ideal problem together with the reduction of Cramer, Ducas, Peikert and Regev breaks them in quantum polynomial time. Schemes based on [Ring-LWE](/ring-lwe-hardness/) do not rest on this problem and are not broken by it.
- **Norm equations and Diophantine equations.** Generalized Pell equations, norm form equations and the search for integral points need generators of principal ideals.

## References
