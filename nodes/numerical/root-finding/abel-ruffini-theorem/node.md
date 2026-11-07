---
tag: NKYH0V
kind: theorem
slug: abel-ruffini-theorem
name: Abel-Ruffini theorem
aliases:
- Abel's impossibility theorem
- unsolvability of the general quintic
- insolvability of the quintic
area: numerical/root-finding
level: intro
summary: For each degree n of at least 5, no formula in radicals gives the roots of every polynomial of degree n, and x^5 - 4x + 2 has roots that no radical expression gives.
prereqs: [fundamental-theorem-of-algebra, polynomial, symmetric-group]
see_also: [quadratic-formula, cardano-formula, ferrari-method, polynomial-root-finding, eisenstein-criterion, irreducible-polynomial, durand-kerner-method, jenkins-traub-algorithm]
sources:
  - paper: "Niels Henrik Abel, Beweis der Unmöglichkeit, algebraische Gleichungen von höheren Graden als dem vierten allgemein aufzulösen, Journal für die reine und angewandte Mathematik 1, 65-84, 1826"
    locator: the proof that the general equation of degree five has no solution by radicals
  - book: isbn:9780471433347
    title: David S. Dummit and Richard M. Foote, Abstract Algebra, third edition, Wiley, 2004
    locator: Section 14.7, Solvable and Radical Extensions, Insolvability of the Quintic (a polynomial is solvable by radicals if and only if its Galois group is solvable) and Section 14.6, Galois Groups of Polynomials
  - book: isbn:9781482245820
    title: Ian Stewart, Galois Theory, fourth edition, CRC Press, 2015
    locator: the chapters on solvability by radicals and on the general polynomial (the Galois group of the general polynomial of degree n is the symmetric group)
  - paper: "Paolo Ruffini, Teoria generale delle equazioni, in cui si dimostra impossibile la soluzione algebraica delle equazioni generali di grado superiore al quarto, Bologna, 1799"
    locator: the first, incomplete, proof of the impossibility
---

The Abel-Ruffini theorem says that for each degree $n \ge 5$ there is no formula that gives the roots of every polynomial of degree $n$ from its coefficients by the four arithmetic operations and the extraction of $k$-th roots. Formulas of this kind exist for degree 2 ([quadratic formula](/quadratic-formula/)), 3 ([Cardano's formula](/cardano-formula/)) and 4 ([Ferrari's method](/ferrari-method/)). The stronger form says that particular polynomials with integer coefficients, such as $x^5 - 4x + 2$, have roots that no radical expression gives at all. This is why [polynomial root finding](/polynomial-root-finding/) of degree 5 and more is done by iterative methods.

## Statement

A number $\alpha \in \mathbb{C}$ is *expressible by radicals* over a field $F \subseteq \mathbb{C}$ if there is a chain of fields $F = F_0 \subseteq F_1 \subseteq \cdots \subseteq F_r$ with $\alpha \in F_r$ and $F_{i+1} = F_i(\beta_i)$, where $\beta_i^{k_i} \in F_i$ for some integer $k_i \ge 1$. A polynomial $p \in F[x]$ is *solvable by radicals* over $F$ if each of its roots is expressible by radicals over $F$.

**Theorem (Abel-Ruffini, general form).** Let $n \ge 5$, and let $a_0, \ldots, a_{n-1}$ be indeterminates. The general polynomial $x^n + a_{n-1}x^{n-1} + \cdots + a_0$ is not solvable by radicals over the field $\mathbb{Q}(a_0, \ldots, a_{n-1})$. So no formula built from the coefficients by $+, -, \times, \div$ and radicals gives the roots of all polynomials of degree $n$.

**Theorem (a specific quintic).** The polynomial $p(x) = x^5 - 4x + 2$ is not solvable by radicals over $\mathbb{Q}$. Its roots are $-1.5185121528$, $0.5084994847$, $1.2435963906$ and $-0.1167918612 \pm 1.4384476953\,i$, and none of them is expressible by radicals over $\mathbb{Q}$.

The theorem does not say that no quintic is solvable: $x^5 - 2$ has the root $2^{1/5}$, and $x^5 - 5x + 12$ is solvable by radicals. It says that no single formula works for all of them, and that some of them cannot be solved by radicals at all.

## In plain words

For a quadratic equation, school teaches a formula: add, subtract, multiply, divide the numbers of the equation, and take a square root. Similar formulas, longer ones, exist for equations whose highest power is three or four. They use cube roots and fourth roots too. For a fifth power or higher there is no such formula. This is not because nobody has found it yet: it is proved that it cannot exist. Some fifth-degree equations with small whole numbers in them have answers that cannot be written with roots at all. Those answers still exist, and a computer finds them to any number of digits by repeating an improving step.

## Proof

The proof has four steps. Step 1 is the main theorem of Galois theory on radicals, which we cite. Steps 2 to 4 are proved here.

*Step 1 (Galois, cited).* Let $F \subseteq \mathbb{C}$ and $p \in F[x]$, and let $G$ be the Galois group of the splitting field of $p$ over $F$. If $p$ is solvable by radicals over $F$, then $G$ is a solvable group: it has a chain of subgroups $G = G_0 \trianglerighteq G_1 \trianglerighteq \cdots \trianglerighteq G_s = \{1\}$, each normal in the one before, with each quotient $G_{i}/G_{i+1}$ abelian. The proof adjoins roots of unity, so that each step of the chain of fields is a cyclic extension, and then uses the Galois correspondence (Dummit and Foote, Section 14.7; Stewart, the chapter on solvability by radicals).

*Step 2: $S_n$ is not solvable for $n \ge 5$.* Let $H$ be a subgroup of $S_n$ that holds every 3-cycle, and let $K$ be a normal subgroup of $H$ with $H/K$ abelian. In an abelian quotient every commutator $xyx^{-1}y^{-1}$ maps to the identity, so $K$ holds every commutator of elements of $H$. Take a 3-cycle $(i\,j\,k)$. Since $n \ge 5$ there are two more points $l, m$. With $x = (i\,j\,l)$ and $y = (i\,k\,m)$, both in $H$, a direct computation, composing from right to left, gives $xyx^{-1}y^{-1} = (i\,j\,k)$. So $K$ holds every 3-cycle. Now suppose $S_n = G_0 \trianglerighteq G_1 \trianglerighteq \cdots \trianglerighteq G_s = \{1\}$ with abelian quotients. By induction on $i$, each $G_i$ holds every 3-cycle, so $G_s \ne \{1\}$, a contradiction.

*Step 3: the Galois group of $p(x) = x^5 - 4x + 2$ over $\mathbb{Q}$ is $S_5$.*

1. $p$ is irreducible over $\mathbb{Q}$ by the [Eisenstein criterion](/eisenstein-criterion/) at the prime 2: 2 divides $-4$ and $2$, 2 does not divide the leading coefficient 1, and 4 does not divide 2.
2. $p$ has exactly three real roots. $p'(x) = 5x^4 - 4$ is zero only at $\pm c$ with $c = (4/5)^{1/4} = 0.94574$. $p$ increases on $(-\infty, -c]$, decreases on $[-c, c]$ and increases on $[c, \infty)$. Since $p(-c) = 5.0264 > 0$, $p(c) = -1.0264 < 0$, and $p(x) \to \mp\infty$ as $x \to \mp\infty$, there is exactly one real root in each of the three intervals. By the [fundamental theorem of algebra](/fundamental-theorem-of-algebra/) the other two roots are non-real and conjugate.
3. Let $G$ act on the five roots, so $G \le S_5$. If $\alpha$ is a root, $[\mathbb{Q}(\alpha) : \mathbb{Q}] = 5$ since $p$ is irreducible, and this degree divides $|G|$. By Cauchy's theorem $G$ has an element of order 5, which in $S_5$ is a 5-cycle.
4. Complex conjugation maps the splitting field to itself, fixes the three real roots and swaps the two non-real ones. So $G$ holds a transposition.
5. A 5-cycle $\sigma$ and a transposition $\tau = (a\,b)$ generate $S_5$. Some power $\sigma^j$ maps $a$ to $b$, and it is again a 5-cycle because 5 is prime. Number the points so that $\sigma^j = (1\,2\,3\,4\,5)$ and $\tau = (1\,2)$. Conjugating $\tau$ by powers of $\sigma^j$ gives $(2\,3), (3\,4), (4\,5)$, and the adjacent transpositions generate $S_5$.

So $G = S_5$. By Steps 1 and 2, $p$ is not solvable by radicals over $\mathbb{Q}$. Since $p$ is irreducible, each root has the same minimal polynomial, so if one root were expressible by radicals, every root would be, in a normal closure; hence no root is. This proves the second theorem.

*Step 4: the general form.* For the general polynomial of degree $n$, the Galois group over $\mathbb{Q}(a_0, \ldots, a_{n-1})$ is $S_n$: the roots $t_1, \ldots, t_n$ are algebraically independent, the coefficients are the elementary symmetric functions of the roots up to sign, and the field of symmetric rational functions is fixed exactly by $S_n$ (Dummit and Foote, Section 14.6; Stewart, the chapter on the general polynomial). By Steps 1 and 2 it is not solvable by radicals for $n \ge 5$. A formula valid for all polynomials of degree $n$ would give the roots of the general polynomial, so no such formula exists. $\blacksquare$

## Consequences

- **Iteration is needed.** From degree 5 on, root finders iterate: [Newton's method](/newton-raphson-method/), the [Durand-Kerner method](/durand-kerner-method/), the [Aberth-Ehrlich method](/aberth-ehrlich-method/), the [Jenkins-Traub algorithm](/jenkins-traub-algorithm/) and the [companion matrix method](/companion-matrix-method/). No finite sequence of arithmetic operations and radicals can replace them.
- **Exact formulas end at degree 4.** [Cardano's formula](/cardano-formula/) and [Ferrari's method](/ferrari-method/) are the last general radical formulas. In floating point they have their own troubles, so even for degree 3 and 4 an iterative method is often more accurate.
- **Eigenvalues.** A matrix of size $n \ge 5$ can have the characteristic polynomial $x^5 - 4x + 2$ (the companion matrix does), so no finite radical formula computes eigenvalues in general. This is why eigenvalue algorithms such as the [QR algorithm](/qr-algorithm/) must iterate.
- **Special classes.** The theorem leaves room for polynomials whose Galois group is solvable, such as $x^n - a$, cyclotomic polynomials and the quintics with a solvable group, which have radical solutions.

## Tightness

- **Degree 4 is solvable.** For $n \le 4$, $S_n$ is solvable ($S_4 \trianglerighteq A_4 \trianglerighteq V_4 \trianglerighteq \{1\}$), and the quadratic formula, Cardano's formula and Ferrari's method give the roots. So 5 is the least degree for which the theorem holds.
- **Radicals, not other functions.** The roots of the general quintic can be written with functions other than radicals, for example with elliptic modular functions, or with the Bring radical (the real root of $x^5 + x + a$) after a Tschirnhaus transformation. The theorem is about radicals only.
- **Specific polynomials.** The degree alone does not decide: $x^5 - 2$ is solvable and $x^5 - 4x + 2$ is not. The test is whether the Galois group is solvable.

## History

Ruffini published a proof in 1799 that had gaps. Abel gave a complete proof in 1824, published in 1826 in the first volume of Crelle's journal. Galois then found the criterion of Step 1, a group-theoretic test for each polynomial, which also explains Step 3. Dummit and Foote (Section 14.7) and Stewart give the modern proof.

## References
