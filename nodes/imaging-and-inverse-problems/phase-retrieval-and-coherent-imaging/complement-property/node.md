---
tag: EFW7RB
kind: theorem
slug: complement-property
name: Complement property
aliases:
- Balan-Casazza-Edidin theorem
area: imaging-and-inverse-problems/phase-retrieval-and-coherent-imaging
level: research
summary: "Real vectors x are fixed up to sign by the values |<x, a_k>| exactly when, for every split of the a_k into two sets, one of the sets spans the space. So at least 2n - 1 vectors are needed."
prereqs: [phase-retrieval, linear-independence]
see_also: [phaselift, wirtinger-flow, phase-retrieval-ambiguities, spectral-initialization, rank-nullity-theorem, determinant, schwartz-zippel-lemma, bruck-sodin-uniqueness]
sources:
  - paper: doi:10.1016/j.acha.2005.07.001
    title: Radu Balan, Pete Casazza and Dan Edidin, On signal reconstruction without phase, Applied and Computational Harmonic Analysis 20(3), 2006, 345 to 356
    locator: the property of splits and the characterization of injectivity for real vectors, the 2n - 1 generic real vectors, and the 4n - 2 generic complex vectors (theorem numbers not confirmed)
  - paper: doi:10.1016/j.acha.2013.10.002
    title: Afonso S. Bandeira, Jameson Cahill, Dustin G. Mixon and Aaron A. Nelson, Saving phase, injectivity and stability for phase retrieval, Applied and Computational Harmonic Analysis 37(1), 2014, 106 to 125
    locator: Definition 2 (the complement property), Theorem 3 (the real case, with proof), Theorem 7 (necessity in the complex case), the example after Theorem 7, and the conjecture of 4n - 4 measurements (preprint arXiv 1302.4618)
  - paper: doi:10.1016/j.acha.2014.06.005
    title: Aldo Conca, Dan Edidin, Milena Hering and Cynthia Vinzant, An algebraic characterization of injectivity in phase retrieval, Applied and Computational Harmonic Analysis 38(2), 2015, 346 to 356
    locator: the result that 4n - 4 generic complex vectors give injectivity (preprint arXiv 1312.0158)
---

The complement property is a test for when [phase retrieval](/phase-retrieval/) with known real vectors has a unique answer. The data are the values $|\langle x, a_k \rangle|$ for vectors $a_1, \dots, a_m \in \mathbb{R}^n$, and the signal $x$ can only be found up to its sign. Balan, Casazza and Edidin (2006) showed that the data fix $x$ up to sign for every $x$ exactly when no split of the vectors into two sets leaves both sets unable to span $\mathbb{R}^n$. This page is about the uniqueness of the answer for general vectors. The page on [trivial ambiguities](/phase-retrieval-ambiguities/) is about Fourier data, where other ambiguities appear.

## Statement

Let $a_1, \dots, a_m \in \mathbb{R}^n$, and define $\mathcal{A} : \mathbb{R}^n / \{\pm 1\} \to \mathbb{R}^m$ by $\mathcal{A}(x)_k = |\langle x, a_k \rangle|^2$. The vectors have the **complement property** if for every subset $S \subseteq \{1, \dots, m\}$, the vectors $\{a_k\}_{k \in S}$ span $\mathbb{R}^n$ or the vectors $\{a_k\}_{k \notin S}$ span $\mathbb{R}^n$.

**Theorem (Balan, Casazza and Edidin 2006).** $\mathcal{A}$ is injective, that is, $\mathcal{A}(x) = \mathcal{A}(y)$ implies $y = \pm x$, if and only if $a_1, \dots, a_m$ have the complement property.

The same definition applies to vectors in $\mathbb{C}^n$, with $x$ fixed up to a factor $e^{i\varphi}$. There the complement property is necessary for injectivity but not sufficient (see Consequences).

## In plain words

Each measurement tells you the size of the shadow of an unknown arrow on a known direction, but not on which side the shadow falls. The question is whether these sizes always fix the arrow, up to turning it around.

Split the known directions into two groups in every possible way. The theorem says that the sizes fix the arrow exactly when, for every split, at least one group is rich enough to point in every direction of the space. If both groups of some split are too poor, you can build two different arrows that give the same sizes for every direction, by adding and subtracting two arrows that each hide from one of the groups.

## Proof

The proof follows Bandeira, Cahill, Mixon and Nelson (2014, Theorem 3). Both directions are proved in the contrapositive form.

*If the complement property fails, $\mathcal{A}$ is not injective.* Take $S$ such that neither $\{a_k\}_{k \in S}$ nor $\{a_k\}_{k \notin S}$ spans $\mathbb{R}^n$. Then there is a nonzero $u$ orthogonal to every $a_k$ with $k \in S$, and a nonzero $v$ orthogonal to every $a_k$ with $k \notin S$. For every $k$, one of $\langle u, a_k \rangle$ and $\langle v, a_k \rangle$ is $0$, so

$$|\langle u \pm v, a_k \rangle|^2 = \langle u, a_k \rangle^2 \pm 2 \langle u, a_k \rangle \langle v, a_k \rangle + \langle v, a_k \rangle^2 = \langle u, a_k \rangle^2 + \langle v, a_k \rangle^2 .$$

So $\mathcal{A}(u + v) = \mathcal{A}(u - v)$. But $u + v = u - v$ would give $v = 0$, and $u + v = -(u - v)$ would give $u = 0$. So $u + v \neq \pm(u - v)$.

*If $\mathcal{A}$ is not injective, the complement property fails.* Take $x \neq \pm y$ with $\mathcal{A}(x) = \mathcal{A}(y)$. For each $k$, $\langle x, a_k \rangle^2 = \langle y, a_k \rangle^2$, so $\langle x, a_k \rangle = \langle y, a_k \rangle$ or $\langle x, a_k \rangle = -\langle y, a_k \rangle$. Let $S = \{k : \langle x, a_k \rangle = -\langle y, a_k \rangle\}$. Then $\langle x + y, a_k \rangle = 0$ for $k \in S$, and $\langle x - y, a_k \rangle = 0$ for $k \notin S$. Both $x + y$ and $x - y$ are nonzero because $x \neq \pm y$. A nonzero vector orthogonal to a set of vectors shows that the set does not span $\mathbb{R}^n$. So neither part of the split spans. $\square$

## Consequences

- **At least $2n - 1$ vectors.** If $m \le 2n - 2$, split the vectors into two sets of at most $n - 1$ each. Neither set spans $\mathbb{R}^n$, so $\mathcal{A}$ is not injective.
- **$2n - 1$ vectors: full spark.** For $m = 2n - 1$, $\mathcal{A}$ is injective exactly when every $n$ of the vectors span $\mathbb{R}^n$. If every $n$ of them span, each split has a part with at least $n$ vectors, and that part spans. If some $n$ of them do not span, take $S$ to be these $n$; the other $n - 1$ cannot span either.
- **Generic vectors.** Every $n$ of the vectors span exactly when each $n \times n$ [determinant](/determinant/) of them is not $0$. Each determinant is a nonzero polynomial in the entries, so $2n - 1$ vectors drawn from a continuous distribution give injectivity with probability one.
- **The complex case.** For vectors in $\mathbb{C}^n$ and $x$ fixed up to $e^{i\varphi}$, the complement property is necessary (Bandeira, Cahill, Mixon and Nelson 2014, Theorem 7), but not sufficient. Their example is $(1, 0)$, $(0, 1)$, $(1, 1)$ in $\mathbb{C}^2$: these have the complement property, but $x = (1, i)$ and $y = (1, -i)$ both give the data $(1, 1, 2)$, and $y$ is not $e^{i\varphi} x$. Real vectors cannot tell a complex $x$ from its conjugate.
- **How many complex vectors.** Balan, Casazza and Edidin (2006) showed that $4n - 2$ generic vectors in $\mathbb{C}^n$ give injectivity, and Conca, Edidin, Hering and Vinzant (2015) brought this down to $4n - 4$. Heinosaari, Mazzarella and Wolf showed a lower bound of $4n - 2\alpha(n - 1) - 3$, where $\alpha(n - 1)$ is the number of ones in the binary form of $n - 1$, as stated by Bandeira, Cahill, Mixon and Nelson. So the answer is $(4 + o(1)) n$.
- **Stability.** Injectivity does not bound the error for noisy data. Bandeira, Cahill, Mixon and Nelson ask for a numerical version, where for every split one part has a smallest singular value bounded below, and show that Gaussian vectors have it with high probability. The guarantees of [PhaseLift](/phaselift/) and [Wirtinger flow](/wirtinger-flow/) use $m$ a larger multiple of $n$, or $n \log n$.

## Tightness

Both parts of the theorem are sharp, as these small examples in $\mathbb{R}^2$ show.

- **Three vectors that work.** $e_1$, $e_2$, $e_1 + e_2$ have the complement property: every split puts two of the three vectors on one side, and any two of them span $\mathbb{R}^2$. Indeed the data $x_1^2$, $x_2^2$ and $(x_1 + x_2)^2$ give $|x_1|$, $|x_2|$ and the product $x_1 x_2 = \frac12\bigl((x_1 + x_2)^2 - x_1^2 - x_2^2\bigr)$, so $x$ is fixed up to sign.
- **Four vectors that fail.** $e_1$, $2 e_1$, $e_2$, $3 e_2$ are more than $2n - 1 = 3$ vectors, but the split $S = \{e_1, 2e_1\}$ leaves two sets that each span only a line. The proof gives $u = e_2$ and $v = e_1$, and indeed $x = (1, 1)$ and $y = (1, -1)$ both give the data $(1, 4, 1, 9)$. So a large number of vectors is not enough; the condition is on every split.
- **Two vectors.** $m = 2 = 2n - 2$ is never enough, as in the first consequence: $e_1$ and $e_2$ give the same data for $(1, 1)$ and $(1, -1)$.

## History

Balan, Casazza and Edidin (2006) asked which frames make the magnitudes of the coefficients determine a signal up to a global phase. They introduced the condition on splits, proved that it is equivalent to injectivity for real frames, and used algebraic geometry to show that $2n - 1$ generic real vectors and $4n - 2$ generic complex vectors are enough. Bandeira, Cahill, Mixon and Nelson (2014) use the name complement property, give the proof above, point out a gap in the earlier argument that the property is necessary in the complex case, and prove that necessity in a different way. They also conjectured that $4n - 4$ generic complex vectors are enough and that fewer are not, and proved the conjecture for $n = 2$ and $n = 3$. Conca, Edidin, Hering and Vinzant (2015) proved the sufficiency of $4n - 4$ generic vectors for all $n$.

## References
