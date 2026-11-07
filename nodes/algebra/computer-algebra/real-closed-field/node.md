---
tag: V7FPHG
kind: concept
slug: real-closed-field
name: Real closed field
aliases: [real closed field, RCF, real closure, Artin-Schreier theory]
area: algebra/computer-algebra
level: advanced
summary: An ordered field with no proper algebraic ordered extension, the setting for real algebraic geometry.
prereqs: [polynomial-ring, sturm-theorem]
see_also: [semialgebraic-set, tarski-seidenberg-theorem, quantifier-elimination, sturm-sequence, descartes-rule-of-signs, real-root-isolation, cylindrical-algebraic-decomposition, hilbert-nullstellensatz]
sources:
  - book: isbn:9783540330981
    title: Saugata Basu, Richard Pollack and Marie-Françoise Roy, Algorithms in Real Algebraic Geometry, second edition, Springer, 2006
    locator: Chapter 2, Real Closed Fields (ordered fields, real closure, real root counting, the Tarski-Seidenberg principle, Puiseux series and Thom encodings)
  - book: isbn:9783540646631
    title: Jacek Bochnak, Michel Coste and Marie-Françoise Roy, Real Algebraic Geometry, Springer, 1998
    locator: Chapter 1, Ordered Fields, Real Closed Fields
  - paper: doi:10.1007/BF02952512
    title: Emil Artin and Otto Schreier, Algebraische Konstruktion reeller Körper, Abhandlungen aus dem Mathematischen Seminar der Universität Hamburg 5, 1927
    locator: pp. 85 to 99 (real closed fields, their characterizations and the existence and uniqueness of the real closure)
  - paper: doi:10.1007/BF02952513
    title: Emil Artin, Über die Zerlegung definiter Funktionen in Quadrate, Abhandlungen aus dem Mathematischen Seminar der Universität Hamburg 5, 1927
    locator: pp. 100 to 115 (the solution of Hilbert's 17th problem with real closed fields)
  - paper: "Alfred Tarski, A Decision Method for Elementary Algebra and Geometry, RAND Corporation, 1948; second edition, University of California Press, 1951"
    locator: completeness and quantifier elimination for real closed fields
---

## In plain words

The real numbers have an order, and every polynomial behaves there as a graph that can only change sign by passing through zero. Many fields share this behavior, for example the real numbers that are roots of polynomials with rational coefficients. A real closed field is any ordered field in which polynomials behave like this, with no more roots to add without breaking the order.

This matters for computer algebra because a computer cannot store all real numbers, but it can work exactly in smaller real closed fields. Also, a statement about polynomials and order that is true in one real closed field is true in all of them. So an algorithm proved correct for the real numbers is correct in every such field, including fields that contain numbers that are smaller than every positive real.

## The idea

**Ordered and real fields.** An *ordered field* is a field $F$ with a total order such that $a \le b$ implies $a + c \le b + c$, and $0 \le a, b$ implies $0 \le ab$. Then squares are nonnegative, so $-1$ is not a sum of squares. A field is *real* (or formally real) if $-1$ is not a sum of squares, and Artin and Schreier proved that a field is real exactly when it has at least one ordering. Real fields have characteristic $0$.

**Definition.** A field $R$ is *real closed* if it is real and no proper algebraic extension of $R$ is real.

**Equivalent conditions** (Artin and Schreier 1927). For a field $R$, the following are equivalent.

1. $R$ is real closed.
2. $R$ has an ordering whose nonnegative elements are exactly the squares, and every polynomial of odd degree in $R[x]$ has a root in $R$.
3. $R \ne R[i]$ with $i^2 = -1$, and $R[i]$ is algebraically closed.
4. $R$ is ordered, and every polynomial $P \in R[x]$ with $P(a) P(b) < 0$ for some $a < b$ has a root between $a$ and $b$ (the intermediate value property for polynomials).

In a real closed field the ordering is unique, because the positive elements are the nonzero squares. So it is not extra data.

**Real closure.** Every ordered field $(F, \le)$ has a *real closure*: a real closed field $R$, algebraic over $F$, whose ordering extends that of $F$. It is unique up to a unique isomorphism over $F$ that keeps the order. The real closure of $\mathbb{Q}$ is the field $\mathbb{R}_{\text{alg}}$ of real algebraic numbers.

**Analysis without limits.** Many facts of calculus for polynomials hold in every real closed field, with proofs that use only algebra: Rolle's theorem and the mean value theorem for polynomials, [Descartes' rule of signs](/descartes-rule-of-signs/), [Sturm's theorem](/sturm-theorem/) for counting roots in an interval, and Thom's lemma, which says that the set where a polynomial and all its derivatives have prescribed signs is empty, a point or an open interval. So real roots can be counted and separated by exact algorithms in any real closed field.

**Thom encodings.** By Thom's lemma, a real root $\alpha$ of $P$ is determined by the signs of $P', P'', \ldots, P^{(\deg P)}$ at $\alpha$. This list of signs is the *Thom encoding* of $\alpha$. It describes a real algebraic number exactly, without an approximating interval. This matters in fields such as $\mathbb{R}\langle\varepsilon\rangle$ below, where two roots can be infinitely close and no interval with rational ends separates them.

**Transfer.** Tarski proved that the theory of real closed fields in the language $(+, \cdot, <, 0, 1)$ admits [quantifier elimination](/quantifier-elimination/). As a consequence it is complete: a first-order sentence with coefficients in $R$ that holds in one real closed field containing $R$ holds in all of them. This is the *transfer principle*. It turns the [Tarski-Seidenberg theorem](/tarski-seidenberg-theorem/) into a statement about every real closed field, and it lets proofs over $\mathbb{R}$, with topology and limits, carry over to real closed fields where these tools do not exist.

**Infinitesimals.** The field $\mathbb{R}\langle\varepsilon\rangle$ of algebraic Puiseux series in $\varepsilon$ over $\mathbb{R}$, ordered so that $0 < \varepsilon < r$ for every real $r > 0$, is real closed. Algorithms add $\varepsilon$ to perturb a system into general position, compute in $\mathbb{R}\langle\varepsilon\rangle$, and then take the limit $\varepsilon \to 0$ algebraically. This is how the singly exponential algorithms of Basu, Pollack and Roy avoid degenerate cases.

## Examples

- **$\mathbb{R}$** is real closed: it is complete, so the intermediate value theorem holds for all continuous functions, and condition 4 holds.
- **$\mathbb{R}_{\text{alg}}$**, the real algebraic numbers, is real closed and countable. It is the real closure of $\mathbb{Q}$, and the transfer principle says that a first-order statement with rational coefficients holds in $\mathbb{R}_{\text{alg}}$ exactly when it holds in $\mathbb{R}$.
- **$\mathbb{Q}$ is not real closed.** $x^3 - 2$ has odd degree and no rational root, and $2 > 0$ is not a square. The same holds for $\mathbb{Q}(\sqrt{2})$, where $x^3 - 2$ still has no root.
- **$\mathbb{R}(t)$ with $t$ positive and smaller than every positive real** is an ordered field but not real closed: $t > 0$ has no square root. Its real closure is the field of real algebraic Puiseux series in $t$, which contains $t^{1/2}$.
- **$\mathbb{C}$ is not real**: $-1 = i^2$. It is $\mathbb{R}[i]$, as in condition 3.
- **A Thom encoding.** $P = x^2 - 2$ has $P' = 2x$ and $P'' = 2$. Its roots are $\sqrt 2$ with signs $(+, +)$ and $-\sqrt 2$ with signs $(-, +)$, so the sign of $P'$ alone tells them apart.

## Where it is used

- **Real algebraic geometry.** [Semialgebraic sets](/semialgebraic-set/) are defined over any real closed field, and their basic theory, such as decomposition into cells, finiteness of the number of connected components, and stability under projection, holds over all of them.
- **Quantifier elimination and decision.** [Quantifier elimination](/quantifier-elimination/) and [cylindrical algebraic decomposition](/cylindrical-algebraic-decomposition/) are correct over every real closed field, and their output is the same over $\mathbb{R}_{\text{alg}}$ and over $\mathbb{R}$.
- **Exact real roots.** [Real root isolation](/real-root-isolation/), [Sturm sequences](/sturm-sequence/) and Thom encodings compute with real algebraic numbers exactly.
- **Perturbation.** Infinitesimals in real closed extensions handle degenerate inputs in algorithms for the existential theory of the reals, roadmaps and connected components.
- **Positivity.** Artin (1927) solved Hilbert's 17th problem with real closed fields: a real polynomial that is nonnegative on $\mathbb{R}^n$ is a sum of squares of rational functions. The later Positivstellensatz of Krivine and Stengle, the real analogue of the [Nullstellensatz](/hilbert-nullstellensatz/), gives algebraic certificates of positivity and emptiness that are used with semidefinite programming.

## References
