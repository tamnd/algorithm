---
tag: CZ0A4K
kind: theorem
slug: smith-mcmillan-form
name: Smith-McMillan form
aliases:
- Smith-McMillan canonical form
area: control/modeling-and-identification
level: advanced
summary: Every rational transfer matrix equals U M V with U and V unimodular and M a unique diagonal matrix of coprime ratios with divisibility conditions. M gives the poles and zeros with multiplicities.
prereqs: [transfer-function-matrix, smith-normal-form]
see_also: [smith-normal-form, transmission-zero, transfer-function-matrix, poles-and-zeros, minimal-realization, unimodular-matrix, polynomial-gcd, coprime-factorization]
sources:
  - paper: doi:10.1002/j.1538-7305.1952.tb01383.x
    title: Brockway McMillan, Introduction to formal realizability theory, I, Bell System Technical Journal 31(2), 1952
    locator: pp. 217 to 279 (the diagonal form of a rational matrix and the degree of a network), with Part II in 31(3), pp. 541 to 600, doi:10.1002/j.1538-7305.1952.tb01396.x
  - book: isbn:0177810025
    title: H. H. Rosenbrock, State-Space and Multivariable Theory, Nelson, London, 1970
    locator: the whole book (the form as a tool for poles, zeros and the system matrix of multivariable systems)
  - book: isbn:0135369614
    title: Thomas Kailath, Linear Systems, Prentice Hall, 1980
    locator: Chapter 6, State-Space and Matrix-Fraction Descriptions of Multivariable Systems (the Smith and Smith-McMillan forms, and the McMillan degree)
  - book: isbn:0134565673
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Section 3.11, Multivariable System Poles and Zeros (the form, the pole and zero polynomials, and the minors)
---

The Smith-McMillan form is a canonical diagonal form of a rational matrix, such as the [transfer function matrix](/transfer-function-matrix/) of a system with several inputs and outputs. Row and column operations with polynomial matrices that have polynomial inverses bring the matrix to a diagonal of fractions, each in lowest terms, with the numerators each dividing the next and the denominators each dividing the one before. The diagonal is unique. Its denominators define the poles of the matrix and its numerators define the [transmission zeros](/transmission-zero/), both with multiplicities, and the total degree of the denominators is the least number of states of a realization. The form extends the [Smith normal form](/smith-normal-form/) of a polynomial matrix to rational matrices.

## Statement

**Notation.** $\mathbb{R}[s]$ is the ring of real polynomials and $\mathbb{R}(s)$ the field of real rational functions. A square polynomial matrix $U$ is *unimodular* if its inverse is also a polynomial matrix, or equivalently if $\det U$ is a nonzero constant. The *normal rank* of $G \in \mathbb{R}(s)^{p \times m}$ is its rank over $\mathbb{R}(s)$.

**Theorem (Smith-McMillan form).** Let $G \in \mathbb{R}(s)^{p \times m}$ have normal rank $r$. There are unimodular $U \in \mathbb{R}[s]^{p \times p}$ and $V \in \mathbb{R}[s]^{m \times m}$ such that

$$U(s)\, G(s)\, V(s) = M(s) = \begin{pmatrix} \operatorname{diag}\left(\dfrac{\varepsilon_1}{\psi_1}, \dots, \dfrac{\varepsilon_r}{\psi_r}\right) & 0 \\ 0 & 0 \end{pmatrix},$$

where the $\varepsilon_i$ and $\psi_i$ are monic polynomials and

1. $\varepsilon_i$ and $\psi_i$ are coprime for each $i$,
2. $\varepsilon_i$ divides $\varepsilon_{i+1}$ for $i < r$,
3. $\psi_{i+1}$ divides $\psi_i$ for $i < r$.

The matrix $M$ is unique: it depends on $G$ only, not on the choice of $U$ and $V$.

**Definitions that use it.** The *pole polynomial* is $\psi_1 \psi_2 \cdots \psi_r$, the *zero polynomial* is $\varepsilon_1 \varepsilon_2 \cdots \varepsilon_r$, and the *McMillan degree* is the degree of the pole polynomial. The poles and the transmission zeros of $G$ are the roots of these polynomials, with multiplicity.

## In plain words

Take a table of fractions of polynomials, such as the transfer functions between all the inputs and outputs of a machine. One may add a polynomial multiple of one row to another row, or of one column to another column, and swap rows or columns, since all these steps can be undone. With such steps, the table can always be cleared until only a diagonal remains, and each diagonal fraction is in lowest terms. One can also arrange that each top divides the next top, and each bottom divides the bottom before it. Then the diagonal is the same however one did the steps. The bottoms tell where the system has its natural modes, the tops tell which input patterns it can block, and the size of the bottoms tells how many states a model of it needs.

## Proof

The proof has three steps: the Smith form of a polynomial matrix, the passage to rational matrices, and uniqueness.

**Step 1: the Smith form over $\mathbb{R}[s]$.** Let $N$ be a $p \times m$ polynomial matrix of rank $r$. We show that unimodular row and column operations bring $N$ to $\operatorname{diag}(n_1, \dots, n_r, 0, \dots)$ with monic $n_i$ and $n_i \mid n_{i+1}$. The allowed operations are: swap two rows (or columns), multiply a row by a nonzero constant, and add a polynomial multiple of one row to another (and the same for columns). Each is a product with a unimodular matrix.

If $N = 0$ there is nothing to do. Otherwise, move a nonzero entry of least degree to position $(1, 1)$. For each $i > 1$, divide $a_{i1}$ by $a_{11}$ with remainder, $a_{i1} = q\, a_{11} + \rho$, and subtract $q$ times row 1 from row $i$; the new entry is $\rho$, with $\deg \rho < \deg a_{11}$. If some $\rho \ne 0$, move it to $(1, 1)$ and start again. Do the same with the first row and column operations. Each restart lowers $\deg a_{11}$, so after finitely many steps the first row and column are zero except $a_{11}$. If $a_{11}$ does not divide some entry $a_{ij}$ with $i, j > 1$, add row $i$ to row 1 and repeat; the division then leaves a nonzero remainder of lower degree, so this too ends. Now $a_{11}$ divides every other entry, and every later operation on the lower right block keeps that property, because sums and polynomial multiples of multiples of $a_{11}$ are multiples of $a_{11}$. Apply the same method to the lower right block, and scale to make the diagonal monic.

For uniqueness, let $d_k(N)$ be the monic gcd of all $k \times k$ minors of $N$ (with $d_0 = 1$). By the Cauchy-Binet formula, each $k \times k$ minor of $U N V$ is a sum of polynomial multiples of $k \times k$ minors of $N$, so $d_k(N)$ divides $d_k(UNV)$. The same holds with $U^{-1}$ and $V^{-1}$, so $d_k(UNV) = d_k(N)$. For the diagonal form, the divisibility $n_1 \mid n_2 \mid \cdots$ gives $d_k = n_1 n_2 \cdots n_k$. So $n_k = d_k(N)/d_{k-1}(N)$ is fixed by $N$.

**Step 2: from polynomial to rational.** Let $d$ be the monic least common denominator of the entries of $G$, and $N = d\, G$, a polynomial matrix of rank $r$. Step 1 gives $U N V = \operatorname{diag}(n_1, \dots, n_r, 0, \dots)$, so $U G V = \operatorname{diag}(n_1/d, \dots, n_r/d, 0, \dots)$. Put each fraction in lowest terms: with $g_i = \gcd(n_i, d)$, let $\varepsilon_i = n_i/g_i$ and $\psi_i = d/g_i$. Condition 1 holds by construction.

Condition 3: $g_i$ divides $n_i$, hence $n_{i+1}$, and it divides $d$, so $g_i \mid g_{i+1}$. Then $\psi_{i+1} = d/g_{i+1}$ divides $d/g_i = \psi_i$.

Condition 2: write $n_{i+1} = n_i\, q$ with $q$ a polynomial. Then $\varepsilon_{i+1}/\psi_{i+1} = q\, \varepsilon_i/\psi_i$, so $\varepsilon_{i+1}\, \psi_i = q\, \varepsilon_i\, \psi_{i+1}$. Thus $\varepsilon_i$ divides $\varepsilon_{i+1} \psi_i$, and since $\varepsilon_i$ and $\psi_i$ are coprime, $\varepsilon_i \mid \varepsilon_{i+1}$.

**Step 3: uniqueness of $M$.** Let $U' G V' = M'$ be any form with the three conditions. By condition 3, every $\psi'_i$ divides $\psi'_1$, so $\psi'_1$ is the least common denominator of the entries of $M'$. The entries of $M' = U' G V'$ are polynomial combinations of the entries of $G$, so $d\, M'$ is a polynomial matrix and $\psi'_1 \mid d$. In the same way $G = U'^{-1} M' V'^{-1}$ gives $d \mid \psi'_1$. Both are monic, so $\psi'_1 = d$. Now $d\, M'$ is diagonal with the entries $n'_i = (d/\psi'_i)\, \varepsilon'_i$, which are monic polynomials, and $n'_i \mid n'_{i+1}$ because $d/\psi'_i$ divides $d/\psi'_{i+1}$ and $\varepsilon'_i \mid \varepsilon'_{i+1}$. So $d M' = (U') N (V')$ is a Smith form of $N$, and by Step 1, $n'_i = n_i$. Then $\varepsilon'_i/\psi'_i = n_i/d$ in lowest terms, which is $\varepsilon_i/\psi_i$. $\square$

**A worked example.** Take
$$G(s) = \begin{pmatrix} 1/(s + 1) & 2/(s + 3) \\ 1/(s + 1) & 1/(s + 1) \end{pmatrix}, \qquad d = (s + 1)(s + 3), \qquad N = \begin{pmatrix} s + 3 & 2(s + 1) \\ s + 3 & s + 3 \end{pmatrix}.$$
The entries of $N$ have gcd 1, and $\det N = (s + 3)(1 - s)$. So $d_1 = 1$, $d_2 = (s + 3)(s - 1)$, and the Smith form of $N$ is $\operatorname{diag}(1, (s + 3)(s - 1))$. One sequence of operations that reaches it: subtract row 1 from row 2, subtract twice column 1 from column 2, swap the columns, then clear the off-diagonal entries with the multiples $(s + 3)/4$ and $(1 - s)/4$ of the corner $-4$, and scale. Dividing by $d$ and reducing:

$$M(s) = \begin{pmatrix} \dfrac{1}{(s + 1)(s + 3)} & 0 \\ 0 & \dfrac{s - 1}{s + 1} \end{pmatrix}.$$

The pole polynomial is $(s + 1)^2 (s + 3)$: the poles are $-1$ twice and $-3$, and the McMillan degree is 3, although each entry has degree 1. The zero polynomial is $s - 1$: there is one transmission zero at $s = 1$, in the right half plane, while no entry of $G$ has a zero there.

## Consequences

- **Poles and zeros with multiplicity.** The form defines the poles and the transmission zeros of a rational matrix, and it shows that a zero and a pole can sit at the same point in different diagonal entries, which the determinant hides. See [transmission zero](/transmission-zero/).
- **The minors give the same polynomials.** The pole polynomial is the monic least common denominator of all minors of $G$ of all orders. The zero polynomial is the gcd of the numerators of the minors of order $r$, once each is written with the pole polynomial as its denominator. In the example, the minors are the four entries and $\det G = (1 - s)/((s + 1)^2 (s + 3))$, which give $(s + 1)^2(s + 3)$ and $s - 1$. This is a theorem stated in Zhou, Doyle and Glover, Section 3.11, and it follows from the invariance of the determinantal divisors in Step 1.
- **The McMillan degree is the minimal order.** For a proper $G$, the McMillan degree equals the number of states of a [minimal realization](/minimal-realization/), and the poles of $G$ with multiplicity are the eigenvalues of its $A$ matrix. This page does not prove it; see Kailath, Chapter 6.
- **Coprime factorizations.** Writing $M = E\, \Psi^{-1}$ with $E = \operatorname{diag}(\varepsilon_i)$ and $\Psi = \operatorname{diag}(\psi_i)$, padded with zeros in $E$ and ones in $\Psi$ when $r < m$, gives $G = (U^{-1} E)(V \Psi)^{-1}$, a right coprime polynomial matrix fraction of $G$; see [coprime factorization](/coprime-factorization/).

## Tightness

- **The divisibility conditions are needed for uniqueness.** $G = \operatorname{diag}(1/(s + 1), 1/(s + 2))$ is diagonal with coprime fractions, but condition 3 fails. Its Smith-McMillan form is $\operatorname{diag}(1/((s + 1)(s + 2)), 1)$: here $d = (s + 1)(s + 2)$, $N = \operatorname{diag}(s + 2, s + 1)$, $d_1 = 1$ and $d_2 = (s + 1)(s + 2)$. Without conditions 2 and 3, both diagonal matrices would count as forms of the same $G$.
- **The operations must be unimodular.** If one allows any matrices that are invertible over $\mathbb{R}(s)$, every $G$ of normal rank $r$ becomes $\operatorname{diag}(1, \dots, 1, 0, \dots)$, and all poles and zeros are lost. A unimodular $U$ has no finite poles or zeros of its own, which is why it keeps those of $G$.
- **Zeros at infinity are not shown.** The form deals with finite poles and zeros only. A strictly proper $G$ has zeros at infinity, which need a different form (over the ring of proper rational functions).

## History

Henry J. S. Smith proved the diagonal form of integer matrices in 1861, and the same argument works over any Euclidean ring, such as $\mathbb{R}[s]$. Brockway McMillan, at Bell Laboratories, extended it to rational matrices in his 1952 papers on the realizability of electrical networks, where the degree of the form counts the reactive elements a network needs. H. H. Rosenbrock made the form a standard tool of multivariable control in his 1970 book, where it defines the poles and zeros of a system and links them with the system matrix.

## References
