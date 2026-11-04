---
tag: 5NZZYB
kind: theorem
slug: horners-rule-optimality
name: Horner's rule optimality
aliases:
- Horner optimality
- Optimality of Horner's rule
- Ostrowski-Pan theorem
- Pan's theorem on polynomial evaluation
area: foundations/lower-bounds
level: advanced
summary: Every straight-line program that evaluates a general polynomial of degree n uses at least n additions and at least n multiplications that involve the coefficients, so Horner's rule is optimal.
prereqs: [polynomial-evaluation, straight-line-program, polynomial]
see_also: [multipoint-evaluation, binary-exponentiation, addition-chain, fft-lower-bound, lower-bound, optimality]
sources:
  - paper: doi:10.1070/RM1966v021n01ABEH004147
    title: "V. Ya. Pan, Methods of computing values of polynomials, Russian Mathematical Surveys 21(1) (1966), 105-136"
    locator: the lower bound of n multiplications and divisions (the substitution method)
  - paper: doi:10.1016/b978-1-4832-3272-0.50010-7
    title: "A. M. Ostrowski, On two problems in abstract algebra connected with Horner's rule, in Studies in Mathematics and Mechanics presented to Richard von Mises, Academic Press (1954), 40-48"
    locator: the whole paper (the question, and the cases of small degree)
  - paper: doi:10.1016/b978-0-12-417750-5.50008-7
    title: "A. Borodin, Horner's rule is uniquely optimal, in Z. Kohavi and A. Paz (eds.), Theory of Machines and Computations, Academic Press (1971), 45-58"
    locator: the main theorem
  - book: isbn:9783540605829
    title: Peter Buergisser, Michael Clausen and M. Amin Shokrollahi, Algebraic Complexity Theory, Springer (1997)
    locator: Chapter 6, The Substitution Method, and its notes (Ostrowski, Pan, Belaga); Chapter 5, Preconditioning and Transcendence Degree
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6.4, Evaluation of Polynomials (Horner's rule, lower bounds, adaptation of coefficients)
  - url: https://jeffe.cs.illinois.edu/teaching/497/08-polynomials.pdf
    title: Jeff Erickson, CS 497 Concrete Models of Computation, lecture notes on evaluating polynomials (2003)
    locator: Sections 10.2 and 10.3 (the addition bound and the substitution argument)
---

Horner's rule optimality is the theorem that a [straight-line program](/straight-line-program/) that evaluates a general polynomial $a_n x^n + \cdots + a_1 x + a_0$, with the coefficients and $x$ as inputs, needs at least $n$ additions or subtractions and at least $n$ multiplications. Horner's rule $(\cdots((a_n x + a_{n-1})x + a_{n-2})x \cdots)x + a_0$ uses exactly $n$ of each, so it is optimal for both counts at once. Ostrowski asked the question in 1954, and Pan proved the multiplication bound in 1966 with his *substitution method*, one of the first lower-bound techniques of algebraic complexity theory.

## Statement

**Model.** Let $K$ be a field and let $x, a_0, \ldots, a_n$ be indeterminates. A *straight-line program* over $K$ is a finite sequence of steps $v_k = u \circ w$ with $\circ \in \{+, -, \times\}$, where each operand $u, w$ is an input, a constant of $K$, or an earlier $v_j$. Each $v_k$ is then a polynomial in $K[x, a_0, \ldots, a_n]$. The program *computes* $f$ if some $v_k$ is equal to $f$ as a polynomial. A multiplication step $u \times w$ is

- *scalar* if $u \in K$ or $w \in K$;
- *$x$-only* if $u, w \in K[x]$;
- *significant* otherwise, that is, if neither factor is a constant and at least one factor involves some $a_i$.

Whether a step is scalar, $x$-only or significant depends on the polynomials that it multiplies, not on how they were written.

**Theorem.** Let $n \ge 1$ and $f = a_n x^n + a_{n-1} x^{n-1} + \cdots + a_1 x + a_0$. Every straight-line program over $K$ that computes $f$ has

1. at least $n$ steps that are additions or subtractions, and
2. (Pan) at least $n$ significant multiplications.

Horner's rule has exactly $n$ additions and $n$ multiplications, and all its multiplications are significant. So it is optimal for the number of additions, for the number of significant multiplications, and for the total number of multiplications.

Part 2 follows from a more general statement. For a polynomial of the form

$$
g = \sum_{i=0}^{d} x^i \, \ell_i + r(x), \qquad \ell_i \in \mathrm{span}_K\{a_0, \ldots, a_n\},\ r \in K[x],
$$

let $\rho(g) = \dim_K \mathrm{span}\{\ell_1, \ldots, \ell_d\}$. The forms $\ell_i$ are unique, because $\ell_i$ collects the monomials $x^i a_j$ of $g$. Then:

**Theorem P (Pan's bound, general form).** Every straight-line program over $K$ that computes such a $g$ has at least $\rho(g)$ significant multiplications.

For $f$ above, $\ell_i = a_i$, so $\rho(f) = \dim \mathrm{span}\{a_1, \ldots, a_n\} = n$. The term $\ell_0$ is left out of $\rho$ because $a_0$ is added and never multiplied.

## In plain words

To evaluate a polynomial you can start with the leading coefficient, and then, once for each lower coefficient, multiply by the point and add that coefficient. This is Horner's rule, and it uses one multiplication and one addition for each degree.

The theorem says that no trick does better when the coefficients are not known in advance. The proof of the multiplication bound has a simple core. Look at the first multiplication that mixes in a coefficient. Pretend that one coefficient has a special value that makes one factor of this multiplication equal to zero. Now that multiplication is free, and the polynomial loses one free coefficient. Repeat this, and each multiplication pays for at most one coefficient. A polynomial with as many free coefficients as its degree, after the constant term, needs that many multiplications.

## Proof

### Part 1: additions

Apply the substitution $x \mapsto 1$ to every step. This map is a ring homomorphism from $K[x, a_0, \ldots, a_n]$ to $K[a_0, \ldots, a_n]$ that fixes $K$, so it turns the program into a program with the same number of additions and subtractions that computes $a_0 + a_1 + \cdots + a_n$. It is enough to prove:

**Claim.** For $n \ge 0$, every straight-line program over $K$ that computes a sum $b_0 + b_1 + \cdots + b_n$ of $n + 1$ distinct indeterminates has at least $n$ additions or subtractions.

*Proof.* Induction on $n$. For $n = 0$ there is nothing to prove. Let $n \ge 1$. A *monomial value* is a polynomial $c \, b^{e}$ with $c \in K$ and $b^{e}$ a product of powers of the indeterminates; constants are monomial values with $e = 0$. Inputs and constants are monomial values, and a product of monomial values is one. The sum or difference of two constants is a constant.

Suppose every addition or subtraction of the program has two constant operands. Then by induction over the steps, every value is a monomial value. But $b_0 + \cdots + b_n$ with $n \ge 1$ is not a monomial value. So some addition or subtraction has an operand that is not a constant; let $v_k = u \pm w$ be the first such step. All values before step $k$ are monomial values, so the non-constant operand, say $w$, is $c\, b^{e}$ with $c \ne 0$ and $e \ne 0$. Choose an indeterminate $b_t$ that divides $b^{e}$ and apply the substitution $b_t \mapsto 0$ to the whole program. Then $w$ becomes $0$, and step $k$ computes $u$ or $-u$. Remove the step and use $u$ in its place, or replace it by the scalar multiplication $(-1) \times u$. The new program has one addition or subtraction fewer and computes the sum of the $n$ indeterminates other than $b_t$. By the induction hypothesis it has at least $n - 1$ additions or subtractions, so the old program has at least $n$. $\square$

### Part 2: multiplications (Pan's substitution method)

Let $V = \mathrm{span}_K\{a_0, \ldots, a_n\}$ and $W = V + K[x]$, the set of polynomials $\ell + r(x)$ with $\ell \in V$ and $r \in K[x]$.

**Lemma 1.** In a straight-line program over $K$, every value computed before the first significant multiplication lies in $W$.

*Proof.* Inputs and constants lie in $W$, and $W$ is closed under addition and subtraction. A scalar multiplication of an element of $W$ by $c \in K$ gives an element of $W$. An $x$-only multiplication gives an element of $K[x] \subseteq W$. Induction over the steps gives the claim. $\square$

**Lemma 2.** Let $\varphi : V \to V'$ be a linear map onto a space $V'$ with $\dim V' = \dim V - 1$. For every subspace $S \subseteq V$, $\dim \varphi(S) \ge \dim S - 1$.

*Proof.* The kernel of $\varphi$ has dimension $\dim V - \dim V' = 1$. The restriction of $\varphi$ to $S$ has a kernel of dimension at most $1$, so its image has dimension at least $\dim S - 1$. $\square$

*Proof of Theorem P.* We prove the statement for every finite set of indeterminates $a_j$ (the variable $x$ stays), by induction on the number $s$ of significant multiplications of the program.

*Case $s = 0$.* By Lemma 1 every value lies in $W$, so $g = \ell + r(x)$ with $\ell \in V$. By the uniqueness of the forms $\ell_i$, we get $\ell_i = 0$ for $i \ge 1$, and $\rho(g) = 0 \le s$.

*Case $s \ge 1$.* Let step $k$, $v_k = u \times w$, be the first significant multiplication. By Lemma 1, $u, w \in W$. The step is not $x$-only, so one factor, say $u$, is not in $K[x]$. Write $u = \sum_j \gamma_j a_j + h(x)$ with $\gamma_j \in K$ and $h \in K[x]$; some coefficient $\gamma_t$ is not zero. Let $\sigma$ be the substitution

$$
a_t \ \mapsto\ -\frac{1}{\gamma_t}\Big( \sum_{j \ne t} \gamma_j a_j + h(x) \Big),
$$

which fixes $x$, every $a_j$ with $j \ne t$, and $K$. It is a ring homomorphism, and $\sigma(u) = 0$.

Build a new program: first compute $\sigma(a_t)$ from $x$ and the $a_j$ with $j \ne t$. This needs only additions, scalar multiplications and $x$-only multiplications (to compute $h(x)$), so no significant multiplication. Then run the old program with every use of the input $a_t$ replaced by this value. Each new step computes $\sigma$ of the old value. A scalar step stays scalar, because $\sigma$ fixes $K$. An $x$-only step stays $x$-only, because $\sigma$ fixes $K[x]$. Step $k$ becomes $0 \times \sigma(w)$, a scalar multiplication. So the new program has at most $s - 1$ significant multiplications, and it computes $\sigma(g)$.

Now compute $\sigma(g)$. Write $\ell_i = \lambda_i a_t + \ell_i^{\circ}$ where $\ell_i^{\circ}$ does not involve $a_t$. Then

$$
\sigma(g) = \sum_{i=0}^{d} x^i \, \varphi(\ell_i) + r'(x), \qquad r'(x) = r(x) - \sum_{i=0}^{d} \frac{\lambda_i}{\gamma_t}\, x^i h(x),
$$

where $\varphi : V \to V' = \mathrm{span}\{a_j : j \ne t\}$ is the linear map with $\varphi(a_t) = -\sum_{j \ne t} (\gamma_j / \gamma_t) a_j$ and $\varphi(a_j) = a_j$ for $j \ne t$. So $\sigma(g)$ has the required form, with the forms $\varphi(\ell_i)$, and $\rho(\sigma(g)) = \dim \varphi(\mathrm{span}\{\ell_1, \ldots, \ell_d\})$. The map $\varphi$ is onto $V'$ and $\dim V' = \dim V - 1$, so Lemma 2 gives $\rho(\sigma(g)) \ge \rho(g) - 1$. By the induction hypothesis, applied to the new program and the indeterminates $a_j$ with $j \ne t$,

$$
s - 1 \ \ge\ \rho(\sigma(g)) \ \ge\ \rho(g) - 1 ,
$$

so $s \ge \rho(g)$. $\blacksquare$

## Consequences

- **Horner's rule is optimal.** For a general polynomial, $n$ multiplications and $n$ additions are necessary and sufficient. No reordering, factoring or clever use of constants of $K$ helps.
- **Free powers do not help.** The $x$-only multiplications are not counted. So even a program that receives $x^2, x^3, \ldots, x^n$ for free needs $n$ multiplications that involve the coefficients. The naive method that first computes the powers of $x$ shows this: it uses $n - 1$ $x$-only multiplications and $n$ significant ones, $2n - 1$ in total. Horner's rule saves the $n - 1$ $x$-only multiplications.
- **Linear forms in the coefficients.** Theorem P gives bounds for other families. For example, evaluating $\sum_{i} a_i x^{2i}$ for $i = 0, \ldots, k$ needs at least $k$ significant multiplications, and the bound counts only the dimension of the coefficient forms, not the degree.

### Worked example

Evaluate $p(x) = 2x^3 - 6x^2 + 2x - 1$ at $x = 3$ by Horner's rule, so $n = 3$ and $(a_3, a_2, a_1, a_0) = (2, -6, 2, -1)$.

| step | computation | value |
|---|---|---|
| start | $a_3$ | 2 |
| 1 | $2 \cdot 3 + (-6)$ | 0 |
| 2 | $0 \cdot 3 + 2$ | 2 |
| 3 | $2 \cdot 3 + (-1)$ | 5 |

This takes 3 multiplications and 3 additions, and $p(3) = 54 - 54 + 6 - 1 = 5$. The naive method computes $x^2 = 9$ and $x^3 = 27$ (2 multiplications), then $2 \cdot 3$, $-6 \cdot 9$ and $2 \cdot 27$ (3 multiplications), then 3 additions: $5 = 2n - 1$ multiplications. For degree $10$ the counts are $10$ against $19$, and for degree $100$ they are $100$ against $199$.

### Pitfalls

- **General, not specific, polynomials.** The theorem is about programs that work for indeterminate coefficients. A specific polynomial can be much cheaper: $x^{16}$ needs $4$ multiplications by repeated squaring ([binary exponentiation](/binary-exponentiation/)), not $16$. The theorem says nothing about the cost of one fixed polynomial with numeric coefficients.
- **Preconditioning.** If the coefficients are known in advance and a one-time computation on them is free, fewer multiplications suffice. Then about $n/2$ multiplications and about $n$ additions suffice, and about $n/2$ multiplications are also necessary. The exact constants depend on the field and on the counting rules; see Knuth, Section 4.6.4 (adaptation of coefficients) and Buergisser, Clausen and Shokrollahi, Chapter 5. This does not contradict the theorem, which has no preconditioning.
- **The counting convention.** Multiplications by constants of $K$ are free in Part 2, and so are $x$-only multiplications. Additions are counted separately in Part 1. With other conventions, such as a cost for each multiplication by a constant, the numbers change.
- **Polynomials, not functions.** The program must compute $f$ as a polynomial. Over a finite field, two different polynomials can define the same function (over the field with two elements, $x^2$ and $x$ agree at every point), so a program that is correct only on the points of $K$ is not covered.
- **One point at a time.** The bound is for one evaluation. To evaluate a polynomial of degree $n$ at $n$ points, [multipoint evaluation](/multipoint-evaluation/) uses $O(n \log^2 n)$ operations in total, far less than the $n^2$ operations of $n$ separate runs of Horner's rule.
- **Divisions.** The proof on this page allows only $+$, $-$ and $\times$. Pan's theorem also holds when divisions are allowed, in the model that counts every multiplication and division that is not by a constant of $K$ (Buergisser, Clausen and Shokrollahi, Chapter 6). That proof must avoid substitutions that make a divisor zero.

## Tightness

Both bounds are reached by Horner's rule, which uses exactly $n$ additions and $n$ multiplications for every $n \ge 1$, and every multiplication of Horner's rule is significant. So the theorem is tight for each count separately and for both together. Borodin (1971) showed more: Horner's rule is the only program that reaches both bounds at the same time, in the precise sense defined in his paper. Theorem P is also tight in general: a polynomial $g = \sum_i x^i \ell_i + r(x)$ with $\rho(g) = \rho$ can be computed with $\rho$ significant multiplications, by writing it as $\sum_{k=1}^{\rho} m_k \, q_k(x) + \ell_0 + r(x)$ for a basis $m_1, \ldots, m_\rho$ of $\mathrm{span}\{\ell_1, \ldots, \ell_d\}$ and polynomials $q_k \in K[x]$ that are computed with $x$-only steps.

## History

Ostrowski (1954) asked whether Horner's rule is optimal. He proved that $n$ multiplications are necessary for small degrees. The sources differ on who first proved the bound on additions: some texts credit Ostrowski, and Buergisser, Clausen and Shokrollahi credit Belaga. Pan (1966) proved the multiplication bound for all $n$, also with divisions, by the substitution method. Borodin (1971) proved that Horner's rule is uniquely optimal. Winograd and Strassen developed the substitution method further, and it is now a standard tool for lower bounds on multiplicative complexity.

## References
