---
tag: 6ZS7YE
kind: algorithm
slug: hallgren-pell-algorithm
name: Hallgren's algorithm for Pell's equation
aliases:
- Hallgren's Pell algorithm
area: quantum/quantum-number-theory
level: research
summary: A quantum algorithm that finds the regulator of Z[sqrt(D)], and with it the fundamental solution of Pell's equation, in time polynomial in the number of digits of D.
solves: [pell-equation]
model: quantum-circuit-model
complexity:
  vars: {n: "the bit length of D"}
  time: {quantum_per_sample: poly(n), expected_rounds: poly(n), classical_per_round: poly(n)}
  space: {qubits: poly(n)}
properties: {deterministic: false, exact: true, las_vegas: true, quantum: true}
history:
  year: 2002
  people: [Sean Hallgren]
  note: Hallgren presented the algorithm at STOC 2002 and published the full version in the Journal of the ACM in 2007. It was the first quantum algorithm to find a period that is irrational.
prereqs: [pell-equation, continued-fraction, continued-fraction-convergents, quantum-fourier-transform]
see_also: [unit-group, principal-ideal-problem, quantum-principal-ideal-algorithm, quantum-class-group-algorithm, shor-algorithm, order-finding, fourier-sampling, continued-fraction-post-processing]
sources:
  - paper: doi:10.1145/1206035.1206039
    title: "Sean Hallgren, Polynomial-time quantum algorithms for Pell's equation and the principal ideal problem, Journal of the ACM 54(1), Article 4, 2007"
    locator: the function with an irrational period on the cycle of reduced principal ideals, the analysis of its Fourier sampling, and the recovery of the regulator
  - paper: arxiv:quant-ph/0302134
    title: Richard Jozsa, Notes on Hallgren's efficient quantum algorithm for solving Pell's equation, 2003
    locator: the self-contained account of the infrastructure, the distance function and the quantum step
  - paper: doi:10.1103/RevModPhys.82.1
    title: "Andrew M. Childs and Wim van Dam, Quantum algorithms for algebraic problems, Reviews of Modern Physics 82:1-52, 2010"
    locator: the survey section on Pell's equation and the principal ideal problem
  - paper: "Hendrik W. Lenstra Jr., Solving the Pell equation, Notices of the American Mathematical Society 49(2):182-192, 2002"
    title: Hendrik W. Lenstra Jr., Solving the Pell equation
    locator: the classical methods, the size of the fundamental solution, and its compact representation
  - book: isbn:9780387849225
    title: Michael J. Jacobson Jr. and Hugh C. Williams, Solving the Pell Equation, Springer, 2009
    locator: the continued fraction of sqrt(D), the cycle of reduced principal ideals, and their distances
  - paper: doi:10.1145/1060590.1060660
    title: "Sean Hallgren, Fast quantum algorithms for computing the unit group and class group of a number field, STOC 2005"
    locator: the extension of the method from real quadratic fields to number fields of constant degree
---

Hallgren's algorithm is a quantum algorithm that solves Pell's equation $x^2 - Dy^2 = 1$ for a positive non-square integer $D$. It computes the regulator $R = \ln \varepsilon$ of the fundamental unit $\varepsilon$ of $\mathbb{Z}[\sqrt D]$ in time polynomial in $\log D$, while the best known classical methods take subexponential time. The method samples the Fourier transform of a function on the integers that repeats with the irrational period $NR$, and it recovers $R$ from two samples with continued fractions. The same method solves the [principal ideal problem](/principal-ideal-problem/) in real quadratic fields, and it was the first quantum algorithm to find an irrational period.

## In plain words

Pell's equation asks for whole numbers that make one simple formula equal to 1. The smallest answer can have so many digits that even writing it down takes very long. No fast classical way to find its size is known.

There is a hidden repeating pattern behind the equation. A chain of number objects starts at a known point, and after a fixed distance it comes back to the start. That distance tells us the size of the smallest answer.

The repeat distance is not a whole number, so the usual quantum period finder does not fit directly. Hallgren's idea is to mark each point by the object reached there plus a rounded offset. Then the pattern repeats almost exactly, and a quantum Fourier transform shows the repeat distance. Two samples and a fraction method give a good estimate, and a short classical check turns it into the exact answer.

## The problem

The input is an integer $D > 1$ that is not a square. The output is the fundamental solution $(x_1, y_1)$ of Pell's equation, the solution with $x_1, y_1 \ge 1$ and the smallest $x_1$. Every other positive solution comes from a power of $x_1 + y_1\sqrt D$. The units of the order $\mathcal{O} = \mathbb{Z}[\sqrt D]$ are $\pm\varepsilon^u$ for one fundamental unit $\varepsilon > 1$, and the regulator is $R = \ln \varepsilon$. Then $x_1 + y_1\sqrt D$ is $\varepsilon$ when $\varepsilon$ has norm 1, and $\varepsilon^2$ when it has norm $-1$. See [Pell's equation](/pell-equation/) for the classical background.

The solution can be huge: $x_1$ has about $R/\ln 2$ bits, and $R$ can be about $\sqrt D$. So the real task is to find $R$ to a precision polynomial in $n = \log_2 D$, from which a compact representation of $\varepsilon$ follows. When $R$ is small, as in the examples here, $x_1$ and $y_1$ can also be written out in full.

Notation on this page. The reduced principal ideals of $\mathcal{O}$ form a cycle given by the [continued fraction](/continued-fraction/) of $\sqrt D$. The $k$-th one is $I_k = [Q_k, P_k + \sqrt D]$ with the generator $\theta_k = p_{k-1} + q_{k-1}\sqrt D$, where $p_k/q_k$ are the [convergents](/continued-fraction-convergents/), $\theta_0 = 1$, and the distance is $\delta(I_k) = \ln \theta_k$. The distances increase, and after one period the ideal $(1) = \mathcal{O}$ returns with the distance $R$. So $(1)$ occurs exactly at the distances $uR$. The scale is $N > 0$, the period of the sampled function is $S = NR$, the input register has size $q$, and $B \ge R$ is a known bound. Classical bounds give $R$ below $\sqrt D$ times a polynomial in $\log D$, so such a $B$ with $O(n)$ bits is available.

## The algorithm

The function $f_N(k) = (I, \lfloor k - N\delta(I) \rfloor)$ takes the reduced principal ideal $I$ with the largest distance $\delta(I) \le k/N$ and adds the rounded offset of $k$ beyond it. Both parts are needed. The ideal alone repeats with period $S$ but is constant on long stretches, and the offset makes $f_N$ one-to-one inside a period. Two values $f_N(k) = f_N(k')$ are equal only if $|k' - k - uS| < 1$ for an integer $u$. This weak periodicity is enough for the Fourier transform to put its weight near the multiples of $q/S$.

```pseudo id=main
HALLGREN-PELL(D, N, q, B)          ▷ B ≥ R is a known bound, q ≥ 3(NB)^2
L1  repeat
L2      for i ← 1 to 2 do
L3          prepare q^(-1/2) Σ_{k<q} |k⟩|0⟩
L4          apply |k⟩|0⟩ → |k⟩|f_N(k)⟩, f_N(k) = (I, ⌊k - N δ(I)⌋), I the reduced principal ideal with the largest δ(I) ≤ k/N
L5          apply the QFT of size q to the first register
L6          measure it; call the result c_i
L7      for each convergent a/b of c_1/c_2 with a > 0 and t = a q/(N c_1) ≤ B + 1/N do
L8          if the ideal (1) has a distance δ > 0 with |δ - t| ≤ 1/N then record δ
L9  until some δ is recorded
L10 δ* ← the smallest recorded δ; K ← ⌈(B + 2/N)/ln(1 + √D)⌉
L11 R ← the smallest distance δ > 0 of (1) with |δ - δ*/k| ≤ 1/N for some k in 1..K
L12 x + y√D ← the generator of (1) at distance R       ▷ the fundamental unit ε
L13 if x^2 - D y^2 = -1 then (x, y) ← (x^2 + D y^2, 2xy)
L14 return (x, y) and R
```

Line L4 is the expensive step. A real circuit computes the ideal at distance about $k/N$ in polynomial time by repeated multiplication and reduction of ideals, the infrastructure of Shanks, and it keeps track of the distance to polynomial precision. Lines L8 and L11 use the same arithmetic to test whether $(1)$ lies within $1/N$ of a given distance. The bound on $t$ in line L7 removes the large estimates that come from long convergents, and lines L10 and L11 turn a recorded multiple $uR$ into $R$ itself. They use $R \ge \ln(1 + \sqrt D)$, so $u \le K$.

## Example

Take $D = 7$, $N = 3$ and $q = 256$, so the input register has 8 qubits, and a 4-qubit target register holds a code of $f_N(k)$. The continued fraction of $\sqrt 7$ gives this cycle:

| $k$ | $(Q_k, P_k \bmod Q_k)$ | $\theta_k$ | $\delta_k$ |
| --- | --- | --- | --- |
| 0 | (1, 0) | $1$ | 0 |
| 1 | (3, 2) | $2 + \sqrt 7$ | 1.5360 |
| 2 | (2, 1) | $3 + \sqrt 7$ | 1.7309 |
| 3 | (3, 1) | $5 + 2\sqrt 7$ | 2.3313 |
| 4 | (1, 0) | $8 + 3\sqrt 7$ | 2.7687 |

So $R = 2.7687$ and $S = 3R = 8.306$. Writing an ideal by its pair, the values $f_N(0), \dots, f_N(9)$ are $((1,0),0), ((1,0),1), \dots, ((1,0),4)$, then $((3,2),0)$, $((2,1),0)$, $((3,1),0)$, $((3,1),1)$, and $f_N(9) = ((1,0),0) = f_N(0)$, because $9$ is within 1 of $S$. These are 10 distinct values in one period.

The exact output distribution has $P(0) = 0.1076$, $P(31) = P(225) = 0.0918$, $P(62) = P(194) = 0.056$ and $P(123) = P(133) = 0.0419$, with peaks near $jq/S = 30.8, 61.6, 92.5$ and $123.3$. The bound is $B = \sqrt{256/3}/3 = 3.079$, so $q = 3(NB)^2$. One round samples $c_1 = 31$ and $c_2 = 195$. The convergents of $31/195$ are $0, 1/6, 3/19, 7/44$ and $31/195$. Only $a = 1$ gives $t = 256/93 = 2.7527 \le B + 1/N$. The window $[2.419, 3.086]$ contains the distance $2.7687$ of $(1)$, so line L8 records it. Line L10 gives $K = 3$, and line L11 finds nothing smaller at $\delta^\star/2$ or $\delta^\star/3$. So $R = 2.7687$ and $\varepsilon = 8 + 3\sqrt 7$, with $64 - 63 = 1$, and the algorithm returns $(8, 3)$ after one round.

## Correctness

Equal values of $f_N$ have the same ideal, so they lie a whole number $u$ of periods apart in the cycle and their distances differ by $uR$. Equal offsets then force $|k' - k - uS| < 1$. So each level set of $f_N$ is a set of points within 1 of an arithmetic progression with step $S$. Hallgren showed that the Fourier transform of such a state gives, with probability at least inverse polynomial in $\log D$, samples $c_i$ within 1 of $j_i q/S$ for coprime $j_1, j_2$ of moderate size.

For such a pair, $|c_1/c_2 - j_1/j_2| < 1/(2j_2^2)$, so $j_1/j_2$ is a convergent of $c_1/c_2$ by Legendre's theorem. Then $t = j_1 q/(Nc_1)$ is within $NR^2/(q - S) \le 1/N$ of $R$ when $q \ge 3(NB)^2$. Line L8 records only true distances of $(1)$, which are multiples $uR$ with $u \le K$, and line L11 at $k = u$ finds $R$ itself. Line L13 squares a unit of norm $-1$, which gives the fundamental solution. So every returned answer is right. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

- **Quantum part.** One sample uses $O(n + \log N)$ input qubits for $q \ge 3(NB)^2$ and a Fourier transform of that size. The function $f_N$ needs polynomial-time ideal arithmetic and distances to polynomial precision, so one sample costs time polynomial in $n$.
- **Rounds.** A round succeeds with probability at least inverse polynomial in $n$, so the expected number of rounds is polynomial in $n$.
- **Classical part.** The convergents take $O(n)$ steps. The window tests in lines L8 and L11 are a polynomial number of ideal reductions.
- **Output size.** The value of $R$ to polynomial precision, or a compact representation of $\varepsilon$, has size polynomial in $n$. Writing $x_1$ and $y_1$ in decimal can need about $\sqrt D$ digits, which no algorithm can do in polynomial time.
- **Classical baselines.** Walking the continued fraction cycle takes about $R$ steps, and $R$ can be about $\sqrt D$. Shanks' baby-step giant-step method in the infrastructure takes about $D^{1/4}$ steps. Buchmann's method is subexponential in $n$ under the generalized Riemann hypothesis.

## Properties

- **Irrational period.** The period $S = NR$ is irrational, so no sample is an exact multiple of $q/S$. The algorithm only needs samples within 1 of such multiples.
- **Las Vegas.** The answer comes from the cycle itself and is checked by the identity $x^2 - Dy^2 = 1$ in integers. Only the number of rounds is random.
- **Exponential speedup.** The quantum cost is polynomial in $\log D$, while the best known classical methods are subexponential at best.
- **Uses a bound on $R$.** The register size depends on a bound $B \ge R$, which classical estimates give for free.

## Variants and improvements

- **The principal ideal problem.** Hallgren's paper also decides whether an ideal of a real quadratic field is principal and finds the distance of a generator. This breaks the Buchmann-Williams key exchange, which is based on that problem. See [principal ideal problem](/principal-ideal-problem/).
- **The class group.** Under the generalized Riemann hypothesis, the same paper computes the class group of a real quadratic field. See [quantum class group algorithm](/quantum-class-group-algorithm/).
- **Number fields of constant degree.** Hallgren (2005) and Schmidt and Vollmer (2005) extended the unit group computation to number fields of constant degree. See [unit group computation](/unit-group/).
- **Arbitrary degree.** Eisenträger, Hallgren, Kitaev and Song (2014) computed the unit group of number fields of any degree, and Biasse and Song (2016) solved the principal ideal problem in that setting. See [quantum principal ideal algorithm](/quantum-principal-ideal-algorithm/).
- **Other expositions.** Jozsa gave a self-contained account of the algorithm, and Childs and van Dam put it in the setting of hidden subgroups of the real line.

## When to use it

Use it as the method for Pell's equation, the regulator and the principal ideal problem of a real quadratic field on a quantum computer. It is the base case for the quantum algorithms on unit groups and class groups of general number fields. For small $D$, or when $R$ is small, the classical continued fraction walk is simpler and fast. For factoring itself, [Shor's algorithm](/shor-algorithm/) is simpler, although Hallgren notes that factoring reduces to Pell's equation.

## Pitfalls

- **The offset is needed.** If $f_N$ returns only the ideal, it is constant on stretches of length about $N$ times a distance step, and the Fourier peaks blur. The rounded offset makes $f_N$ one-to-one inside a period.
- **Long convergents give multiples.** The last convergent $c_1/c_2$ itself gives $t = q/N$, which is far larger than $R$, and other long convergents give multiples of $R$ that pass the window test. The bound in line L7 and the search over $\delta^\star/k$ in line L11 remove them.
- **Norm $-1$.** If $\varepsilon$ has norm $-1$, as for $D = 2$ with $1 + \sqrt 2$, then $\varepsilon$ solves $x^2 - Dy^2 = -1$. Line L13 squares it.
- **The order and the field.** This page uses the order $\mathbb{Z}[\sqrt D]$. For $D \equiv 1 \pmod 4$ the ring of integers is larger and can have a smaller fundamental unit, such as $(1 + \sqrt 5)/2$ for $D = 5$. Pell's equation needs the unit of $\mathbb{Z}[\sqrt D]$, which is a power of that one.
- **The size of the output.** Asking for $x_1$ and $y_1$ in full defeats the speedup when $R$ is large. Keep $\varepsilon$ in compact form.
- **The simulation walks the cycle.** The implementation evaluates $f_N$ by walking the continued fraction cycle, which is fine for small $D$. It also picks $N$ so that $NR = 8.5$ to fit the 4-qubit target register. A real circuit uses ideal multiplication and reduction instead and does not know $R$.

## Implementations

## History

Pell's equation has a long history. Indian mathematicians, among them Brahmagupta and Bhāskara II, solved many cases, and Lagrange proved in 1768 that the continued fraction of $\sqrt D$ always gives the fundamental solution. Shanks introduced the infrastructure of reduced ideals in 1972, and Buchmann gave a subexponential method under the generalized Riemann hypothesis. In 2002 Hallgren gave a polynomial-time quantum algorithm for the regulator and the principal ideal problem, and the full version appeared in the Journal of the ACM in 2007. Jozsa wrote an exposition in 2003. Later work by Hallgren, by Schmidt and Vollmer, by Eisenträger, Hallgren, Kitaev and Song, and by Biasse and Song extended the method to general number fields.

## References
