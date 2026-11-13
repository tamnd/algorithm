---
tag: 8KSNX9
kind: problem
slug: pell-equation
name: Pell's equation
aliases:
- "Pell equation x^2 - D y^2 = 1"
area: quantum/quantum-number-theory
level: advanced
summary: Given a positive non-square integer D, find the least positive x, y with x^2 - D y^2 = 1. This solution can have about sqrt(D) digits, so the regulator is the usual output.
prereqs: [continued-fraction, continued-fraction-convergents]
see_also: [hallgren-pell-algorithm, unit-group, principal-ideal-problem, ideal-class-group, shanks-squfof, continued-fraction-factorization, baby-step-giant-step, quantum-principal-ideal-algorithm]
sources:
  - paper: "Hendrik W. Lenstra Jr., Solving the Pell equation, Notices of the American Mathematical Society 49(2):182-192, 2002"
    title: Hendrik W. Lenstra Jr., Solving the Pell equation
    locator: the history, the continued fraction method, the size of the fundamental solution, power products, and the cattle problem of Archimedes
  - book: isbn:9780387849225
    title: Michael J. Jacobson Jr. and Hugh C. Williams, Solving the Pell Equation, Springer, 2009
    locator: the continued fraction method, the infrastructure of reduced ideals, compact representations, and the subexponential methods
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138, Springer, 1993
    locator: Chapter 5, algorithms for quadratic fields, including the regulator of a real quadratic field
  - paper: "Johannes Buchmann, A subexponential algorithm for the determination of class groups and regulators of algebraic number fields, Seminaire de Theorie des Nombres, Paris 1988-1989, Progress in Mathematics 91, Birkhauser, 1990, pp. 27-41"
    title: Johannes Buchmann, A subexponential algorithm for the determination of class groups and regulators of algebraic number fields
    locator: the subexponential method for the regulator, under the generalized Riemann hypothesis
  - paper: doi:10.1145/1206035.1206039
    title: "Sean Hallgren, Polynomial-time quantum algorithms for Pell's equation and the principal ideal problem, Journal of the ACM 54(1), Article 4, 2007"
    locator: the polynomial-time quantum algorithm for the regulator, and the remark that factoring reduces to Pell's equation
  - paper: doi:10.1103/RevModPhys.82.1
    title: "Andrew M. Childs and Wim van Dam, Quantum algorithms for algebraic problems, Reviews of Modern Physics 82:1-52, 2010"
    locator: the survey section on Pell's equation, with the classical background and the quantum algorithm
---

Pell's equation asks for integers $x$ and $y$ with $x^2 - Dy^2 = 1$, where $D$ is a positive integer that is not a square. It always has a smallest positive solution, the fundamental solution, and every other solution is a power of it in $\mathbb{Z}[\sqrt D]$. The fundamental solution can have about $\sqrt D$ digits, so the computational problem is to find its logarithm, the regulator, to good precision. The best known classical methods are subexponential in $\log D$, and Hallgren's quantum algorithm is polynomial.

## In plain words

The equation asks for two whole numbers whose squares, one of them scaled by a fixed number, differ by exactly one. A solution always exists, and all solutions grow from the smallest one by a fixed rule.

The catch is size. For some inputs with only a few digits, the smallest solution already has thousands of digits. So just writing it down can take too long, and computer methods compute a short description of it instead, such as its number of digits to high precision.

A classical method that dates back centuries finds the solution step by step, but the number of steps can grow like the square root of the input. Better classical methods exist but still slow down quickly as the input grows. A quantum computer can find the short description fast.

## Definition

Let $D > 1$ be an integer that is not a square. The equation $x^2 - Dy^2 = 1$ has the trivial solutions $(\pm 1, 0)$ and infinitely many others. The **fundamental solution** $(x_1, y_1)$ is the one with $x_1, y_1 \ge 1$ and the smallest $x_1$. Every solution with $x > 0$ satisfies

$$x + y\sqrt D = (x_1 + y_1\sqrt D)^u \quad \text{for some integer } u.$$

The solutions are the units of norm 1 in the order $\mathbb{Z}[\sqrt D]$, where the norm of $x + y\sqrt D$ is $x^2 - Dy^2$. The unit group of this order is $\{\pm\varepsilon^u\}$ for a **fundamental unit** $\varepsilon > 1$, and its **regulator** is $R = \ln \varepsilon$. If $\varepsilon$ has norm 1, then $x_1 + y_1\sqrt D = \varepsilon$. If it has norm $-1$, then $x_1 + y_1\sqrt D = \varepsilon^2$, and $\varepsilon$ solves the negative equation $x^2 - Dy^2 = -1$.

The computational problem has three forms. One asks for $x_1$ and $y_1$ in full. One asks for $R$ to a given number of bits of precision. One asks for a compact representation of $\varepsilon$, a product of a few powers of small elements of $\mathbb{Q}(\sqrt D)$ with a total size polynomial in $\log D$. The second and third forms are equivalent up to polynomial time, and they are the forms that can be solved quickly.

## Variants

- **The negative Pell equation** $x^2 - Dy^2 = -1$. It is solvable exactly when $\varepsilon$ has norm $-1$, which holds when the period of the continued fraction of $\sqrt D$ is odd. It is not solvable when $D$ has a prime factor $p \equiv 3 \pmod 4$.
- **The generalized equation** $x^2 - Dy^2 = N$. Its solutions fall into finitely many classes, and each class is a family $\alpha\varepsilon^u$. Finding the classes is a [principal ideal problem](/principal-ideal-problem/) for the ideals of norm $|N|$.
- **The ring of integers.** For $D \equiv 1 \pmod 4$, the ring of integers of $\mathbb{Q}(\sqrt D)$ is $\mathbb{Z}[(1 + \sqrt D)/2]$, and its units come from $x^2 - Dy^2 = \pm 4$. Its fundamental unit can be smaller, as $(1 + \sqrt 5)/2$ is for $D = 5$, and the unit of $\mathbb{Z}[\sqrt D]$ is its first power that lies in $\mathbb{Z}[\sqrt D]$.
- **The unit group of a general number field.** Pell's equation is the case of a real quadratic field in [unit group computation](/unit-group/).

## Examples

**$D = 7$.** The continued fraction of $\sqrt 7$ is $[2; \overline{1, 1, 1, 4}]$ with period 4, and the convergents are $2/1, 3/1, 5/2, 8/3, \dots$. The period is even, so the convergent before the end of the first period gives $(x_1, y_1) = (8, 3)$, with $64 - 7 \cdot 9 = 1$. Then $R = \ln(8 + 3\sqrt 7) \approx 2.7687$, and the next solution is $(8 + 3\sqrt 7)^2 = 127 + 48\sqrt 7$.

**$D = 13$.** The fundamental unit is $18 + 5\sqrt{13}$ with $324 - 325 = -1$, so the negative equation is solvable. Its square gives the fundamental solution $(649, 180)$.

**$D = 61$.** Fermat posed this case as a challenge in 1657. The fundamental unit is $29718 + 3805\sqrt{61}$ of norm $-1$, and the fundamental solution is $(1766319049, 226153980)$. A small $D$ can have a large solution.

**$D = 94$.** The fundamental solution is $(2143295, 221064)$, much larger than for the nearby $D = 95$, whose solution is $(39, 4)$.

**The cattle problem of Archimedes.** It leads to Pell's equation with $D = 410286423278424$. Amthor showed in 1880 that the smallest total number of cattle has 206545 digits. Lenstra's article shows how a power product describes this solution in a few lines.

## Known algorithms

**Classical.**

- **Search over $y$.** Test $y = 1, 2, \dots$ until $Dy^2 + 1$ is a square. This takes $y_1$ steps, which can be exponential in $\sqrt D$.
- **The cyclic method.** Brahmagupta's composition rule and the chakravala method of Bhāskara II solve the equation by a cycle of small steps. In effect they follow the continued fraction of $\sqrt D$.
- **The [continued fraction](/continued-fraction/) of $\sqrt D$.** The expansion is periodic with some period $\ell$. The fundamental solution is the [convergent](/continued-fraction-convergents/) $p_{\ell-1}/q_{\ell-1}$ when $\ell$ is even and $p_{2\ell-1}/q_{2\ell-1}$ when $\ell$ is odd. Each step uses small integers $P_k$ and $Q_k$ below $2\sqrt D$, and $\ell = O(\sqrt D \log D)$. So the method takes about $\sqrt D$ steps in the worst case. The distance $R$ can be summed from the steps without forming $x_1$ and $y_1$.
- **Shanks' infrastructure.** The reduced principal ideals of the cycle have distances, and two of them can be multiplied and reduced to move far along the cycle at once. A [baby-step giant-step](/baby-step-giant-step/) search over these distances finds $R$ in about $D^{1/4}$ steps, up to factors polynomial in $\log D$.
- **Subexponential methods.** Buchmann's index calculus method finds the regulator and the class group together in time $\exp(O(\sqrt{\log D \log\log D}))$. Its analysis assumes the generalized Riemann hypothesis.
- **Compact output.** Once $R$ is known, a power product for $\varepsilon$ follows in polynomial time from the infrastructure, which avoids the full digits of $x_1$.

**Quantum.**

- **[Hallgren's algorithm](/hallgren-pell-algorithm/).** It finds $R$ to polynomial precision in time polynomial in $\log D$. It samples the Fourier transform of a function on the cycle of ideals that repeats with an irrational period, and it recovers $R$ with continued fractions.
- **General number fields.** The later quantum algorithms for the unit group of number fields of any degree, such as the [quantum principal ideal algorithm](/quantum-principal-ideal-algorithm/) of Biasse and Song, include Pell's equation as the real quadratic case.

## Bounds

The regulator satisfies $R \ge \ln(1 + \sqrt D)$, because $x_1, y_1 \ge 1$. From above, classical estimates give $R$ below $\sqrt D$ times a polynomial in $\log D$, and for many $D$ the value of $R$ is close to this bound. Then $x_1 \approx e^R/2$ has about $R/\ln 10$ decimal digits, so no algorithm can write out $x_1$ in time polynomial in $\log D$ for all $D$. No classical algorithm that runs in polynomial time in $\log D$ is known for $R$ or for a compact representation of $\varepsilon$, while the quantum algorithm runs in polynomial time.

## Reductions

- **Pell's equation and the regulator.** The two forms are equivalent: $R$ gives $\varepsilon$ in compact form, and a compact form of $\varepsilon$ gives $R$.
- **From factoring.** Hallgren notes that factoring integers reduces to Pell's equation, while no reduction in the other direction is known. So a fast classical method for Pell's equation would also break [RSA](/rsa-cryptosystem/).
- **To the principal ideal problem.** Deciding whether an ideal is principal and finding the distance of a generator is at least as hard as finding $R$, because $R$ is the distance between two generators of the ideal $(1)$.
- **To the class group.** Buchmann's method finds $R$ and the [class group](/ideal-class-group/) of the field together. The class number formula links $hR$ to a value of an L-function, which gives an approximation of $hR$.

## Applications

- **Diophantine equations.** Many integer equations, such as the search for numbers that are both square and triangular, lead to Pell's equation.
- **Factoring.** [Continued fraction factorization](/continued-fraction-factorization/) and [Shanks' square forms factorization](/shanks-squfof/) both walk the continued fraction of $\sqrt{kN}$, the same cycle that solves Pell's equation.
- **Cryptography.** The Buchmann-Williams key exchange uses the principal ideal problem of real quadratic fields. Hallgren's algorithm breaks it on a quantum computer.
- **Quantum algorithms.** Pell's equation was the first problem where a quantum algorithm found a period that is not an integer, which opened the way to the quantum algorithms for unit groups and class groups.

## References
