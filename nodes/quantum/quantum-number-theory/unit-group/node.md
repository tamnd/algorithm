---
tag: YXQ3WG
kind: problem
slug: unit-group
name: Unit group computation
aliases:
- computing the unit group of a number field
area: quantum/quantum-number-theory
level: research
summary: Given a number field, find a system of fundamental units of its ring of integers, or its regulator. Classical methods are subexponential, and quantum ones run in polynomial time.
prereqs: [pell-equation, lattice]
see_also: [hallgren-pell-algorithm, quantum-principal-ideal-algorithm, quantum-class-group-algorithm, principal-ideal-problem, ideal-class-group, lll-algorithm, hermite-normal-form, ring-lwe-hardness]
sources:
  - book: isbn:9783540653998
    title: Jürgen Neukirch, Algebraic Number Theory, Springer, 1999
    locator: Chapter I, Section 7, the logarithmic embedding and Dirichlet's unit theorem
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138, Springer, 1993
    locator: Chapter 5 on quadratic fields, and the later chapter on computing the class group, the regulator and fundamental units of a general number field
  - paper: "Johannes Buchmann, A subexponential algorithm for the determination of class groups and regulators of algebraic number fields, Seminaire de Theorie des Nombres, Paris 1988-1989, Progress in Mathematics 91, Birkhauser, 1990, pp. 27-41"
    title: Johannes Buchmann, A subexponential algorithm for the determination of class groups and regulators of algebraic number fields
    locator: the relation method for the unit group and the class group, under the generalized Riemann hypothesis
  - paper: doi:10.1145/1060590.1060660
    title: "Sean Hallgren, Fast quantum algorithms for computing the unit group and class group of a number field, STOC 2005"
    locator: the quantum algorithm for the unit group of a number field of constant degree
  - paper: doi:10.1145/1060590.1060661
    title: "Arthur Schmidt and Ulrich Vollmer, Polynomial time quantum algorithm for the computation of the unit group of a number field, STOC 2005"
    locator: the independent quantum algorithm for the unit group of a number field of constant degree
  - paper: doi:10.1145/2591796.2591860
    title: "Kirsten Eisenträger, Sean Hallgren, Alexei Kitaev and Fang Song, A quantum algorithm for computing the unit group of an arbitrary degree number field, STOC 2014"
    locator: the continuous hidden subgroup problem on R^m and its application to the unit group in any degree
  - paper: doi:10.1007/978-3-662-49896-5_20
    title: "Ronald Cramer, Léo Ducas, Chris Peikert and Oded Regev, Recovering short generators of principal ideals in cyclotomic rings, EUROCRYPT 2016"
    locator: the use of the cyclotomic units to reduce a generator of a principal ideal to a short one
---

Unit group computation asks for the units of the ring of integers $\mathcal{O}_K$ of a number field $K$, the elements whose inverse is also in $\mathcal{O}_K$. By Dirichlet's unit theorem, they are the roots of unity times the products of powers of $r$ fundamental units, so the task is to find these units or their regulator. The real quadratic case is [Pell's equation](/pell-equation/). Classical methods are subexponential at best, and quantum algorithms solve the problem in polynomial time, first for fixed degree and since 2014 for any degree.

## In plain words

A number field extends the ordinary numbers with the roots of one polynomial. In it, some special numbers have an inverse that is again a "whole" number of the field. These are the units, like 1 and -1 among the ordinary integers.

In most number fields there are infinitely many units, but a few basic ones produce all others by multiplication and division. The task is to find such a basic set.

These basic units are often enormous, with far too many digits to write out. So a computer finds a short description of them, or one number that measures their total size. Classical methods slow down quickly as the field grows. Quantum computers can do it fast, because the units form a hidden repeating pattern that a quantum Fourier transform can detect.

## Definition

Let $K$ be a number field of degree $n = r_1 + 2r_2$, with $r_1$ real embeddings $\sigma_1, \dots, \sigma_{r_1}$ and $r_2$ pairs of complex embeddings, of which $\sigma_{r_1 + 1}, \dots, \sigma_{r_1 + r_2}$ are one from each pair. Let $\mathcal{O}_K$ be its ring of integers. The **logarithmic embedding** maps a nonzero $\alpha$ to

$$\mathrm{Log}(\alpha) = (e_1 \ln|\sigma_1(\alpha)|, \dots, e_{r_1 + r_2} \ln|\sigma_{r_1 + r_2}(\alpha)|),$$

with $e_i = 1$ for real and $e_i = 2$ for complex embeddings. **Dirichlet's unit theorem** states that

$$\mathcal{O}_K^\ast \cong \mu_K \times \mathbb{Z}^r, \qquad r = r_1 + r_2 - 1,$$

where $\mu_K$ is the finite group of roots of unity in $K$. The image $\mathrm{Log}(\mathcal{O}_K^\ast)$ is a lattice of rank $r$ in the hyperplane of vectors whose coordinates sum to 0, and its kernel is $\mu_K$. A **system of fundamental units** is a set $\varepsilon_1, \dots, \varepsilon_r$ whose images form a basis of this lattice. The **regulator** $R_K$ is the absolute value of the determinant of any $r \times r$ minor of the matrix with the rows $\mathrm{Log}(\varepsilon_j)$. It does not depend on the choice of the units or of the minor.

The input is $K$, given by a defining polynomial and an integral basis of $\mathcal{O}_K$. The output is a system of fundamental units in compact representation, as products of powers of elements of polynomial size, or the regulator and the unit lattice to a given precision. The size of the input is measured by $n$ and $\log|\Delta_K|$, where $\Delta_K$ is the discriminant.

## Variants

- **The regulator only.** Find $R_K$ to a given precision. With the analytic class number formula, it also gives the class number.
- **Orders.** Compute the unit group of an order $\mathcal{O} \subseteq \mathcal{O}_K$, such as $\mathbb{Z}[\sqrt D]$ for Pell's equation. It is a subgroup of finite index in $\mathcal{O}_K^\ast$.
- **S-units.** For a finite set $S$ of prime ideals, the $S$-units are the elements whose factorization uses only primes in $S$. Their group has rank $r + |S|$. Computing it is the key step for the [principal ideal problem](/principal-ideal-problem/) and the [class group](/ideal-class-group/).
- **Fixed degree or any degree.** Many results treat $n$ as a constant and measure the cost in $\log|\Delta_K|$ only. Results for arbitrary degree must also be polynomial in $n$.
- **Cyclotomic fields.** For $K = \mathbb{Q}(\zeta_m)$, the cyclotomic units $(1 - \zeta^a)/(1 - \zeta)$ are known explicitly. They generate a subgroup of finite index in the units of the real subfield, so the units of these fields are much easier to handle.

## Examples

**Imaginary quadratic fields.** Here $r_1 = 0$ and $r_2 = 1$, so $r = 0$ and the units are the roots of unity: $\{\pm 1, \pm i\}$ for $\mathbb{Q}(i)$, six roots of unity for $\mathbb{Q}(\sqrt{-3})$, and $\{\pm 1\}$ for every other one.

**Real quadratic fields.** Here $r = 1$. For $\mathbb{Q}(\sqrt 2)$, $\varepsilon = 1 + \sqrt 2$ and $R = \ln(1 + \sqrt 2) \approx 0.8814$. For $\mathbb{Q}(\sqrt 5)$, the ring of integers is $\mathbb{Z}[(1 + \sqrt 5)/2]$, $\varepsilon = (1 + \sqrt 5)/2$ and $R \approx 0.4812$. For $\mathbb{Q}(\sqrt{61})$, the fundamental unit is $(39 + 5\sqrt{61})/2$, whose cube is the unit $29718 + 3805\sqrt{61}$ of $\mathbb{Z}[\sqrt{61}]$.

**A pure cubic field.** For $K = \mathbb{Q}(\alpha)$ with $\alpha^3 = 2$, there is one real embedding and one complex pair, so $r = 1$. The norm of $\alpha - 1$ is $1$, because $(\alpha - 1)(\alpha^2 + \alpha + 1) = \alpha^3 - 1 = 1$. In fact $\varepsilon = 1 + \alpha + \alpha^2$ is a fundamental unit, and $R = \ln(1 + \sqrt[3]{2} + \sqrt[3]{4}) \approx 1.3473$.

**A cyclotomic field.** For $\mathbb{Q}(\zeta_{12})$, of degree 4 with $r_2 = 2$, the rank is $r = 1$. The real subfield is $\mathbb{Q}(\sqrt 3)$, and its fundamental unit $2 + \sqrt 3$ is a unit of $\mathbb{Q}(\zeta_{12})$ of infinite order.

## Known algorithms

**Classical.**

- **Real quadratic fields.** The continued fraction of the quadratic irrational and Shanks' infrastructure find $R$ in about $|\Delta_K|^{1/2}$ and $|\Delta_K|^{1/4}$ steps, as on the page on [Pell's equation](/pell-equation/).
- **Voronoi's method and its successors.** For cubic fields and for fields of small degree, these methods walk through minima of lattices in $K$, a higher-dimensional analogue of the continued fraction. Their cost grows like a power of $|\Delta_K|$.
- **The relation method.** Choose a factor base of small prime ideals and collect many elements that factor over it. Each one gives a relation, a vector of valuations together with its logarithmic embedding. The integer kernel of the valuation matrix, computed with the [Hermite normal form](/hermite-normal-form/), gives units, and [LLL](/lll-algorithm/) reduces them. An approximation of $hR_K$ from the analytic class number formula checks that the units generate the whole group. Buchmann's version runs in subexponential time in $\log|\Delta_K|$ for fixed degree, with an analysis that assumes the generalized Riemann hypothesis.
- **Compact representation.** The fundamental units can have coefficients with a number of digits exponential in $\log|\Delta_K|$. The algorithms keep them as products of powers of small elements.

**Quantum.**

- **Real quadratic fields.** [Hallgren's algorithm](/hallgren-pell-algorithm/) (2002) finds $R$ in time polynomial in $\log \Delta_K$.
- **Constant degree.** Hallgren (2005) and, independently, Schmidt and Vollmer (2005) find the unit group in time polynomial in $\log|\Delta_K|$ when $n$ is fixed. Their algorithms find the hidden periods of a function on $\mathbb{R}^r$ that maps a point to a reduced ideal and an offset.
- **Any degree.** Eisenträger, Hallgren, Kitaev and Song (2014) solved the continuous hidden subgroup problem on $\mathbb{R}^m$ and used it to find the unit group in time polynomial in $n$ and $\log|\Delta_K|$. The function maps a point $x$ to a quantum encoding of the lattice $e^{x}\mathcal{O}_K$, and its periods are the logarithms of the units.
- **S-units.** Biasse and Song (2016) extended this to $S$-units, which gives the [quantum principal ideal algorithm](/quantum-principal-ideal-algorithm/) and the class group.

## Bounds

The rank $r = r_1 + r_2 - 1$ is at most $n - 1$. For families of fields of fixed degree, the Brauer-Siegel theorem says that $\ln(h_K R_K)$ grows like $\ln \sqrt{|\Delta_K|}$. So $R_K$ is often close to $\sqrt{|\Delta_K|}$ up to logarithmic factors, and the coefficients of the fundamental units can have a number of digits exponential in $\log|\Delta_K|$. This is why the output must be in compact form. No classical algorithm with a running time polynomial in $\log|\Delta_K|$ is known, even for real quadratic fields, while the quantum algorithms above run in polynomial time.

## Reductions

- **Pell's equation.** The unit group of $\mathbb{Z}[\sqrt D]$ is exactly the set of solutions of $x^2 - Dy^2 = \pm 1$, so Pell's equation is the case $n = 2$, $r = 1$.
- **From factoring.** Factoring reduces to Pell's equation, as Hallgren notes, so it also reduces to unit group computation.
- **To a hidden subgroup problem.** The unit lattice is the period lattice of a function on $\mathbb{R}^{r_1 + r_2}$ that maps a point to an ideal lattice scaled by the point. This is the continuous hidden subgroup problem that the quantum algorithms solve.
- **With the class group and the principal ideal problem.** Classical relation methods compute the unit group and the class group together. The $S$-unit group gives both, and a generator of a principal ideal is unique only up to a unit, so the [principal ideal problem](/principal-ideal-problem/) needs the units to give a canonical answer.

## Applications

- **Diophantine equations.** Thue equations, norm form equations and the search for integral points on curves need a system of fundamental units, for example in methods based on Baker's bounds.
- **Lattice cryptography.** Attacks on schemes built on principal ideals of cyclotomic fields find a generator of the ideal and then reduce it by units to a short one. Cramer, Ducas, Peikert and Regev showed that the cyclotomic units make this reduction work, which together with a quantum principal ideal algorithm breaks these schemes. See [Ring-LWE hardness](/ring-lwe-hardness/).
- **Class numbers and L-functions.** The regulator enters the analytic class number formula, so it is needed to compute class numbers and to check conjectures about them.

## References
