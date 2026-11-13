---
tag: M8TEVB
kind: algorithm
slug: quantum-principal-ideal-algorithm
name: Quantum principal ideal algorithm (Biasse-Song)
aliases:
- Biasse-Song algorithm
area: quantum/quantum-number-theory
level: research
summary: A quantum algorithm that decides whether an ideal of a number field is principal and finds a generator, in polynomial time in any degree, through a hidden lattice of S-units.
solves: [principal-ideal-problem]
model: quantum-circuit-model
complexity:
  vars: {n: "the input size, the degree of the field plus the bit lengths of its discriminant and of the norm of the input ideal"}
  time: {quantum_per_sample: poly(n), expected_rounds: poly(n), classical_per_round: poly(n)}
  space: {qubits: poly(n)}
properties: {deterministic: false, exact: true, las_vegas: false, quantum: true}
history:
  year: 2016
  people: [Jean-François Biasse, Fang Song]
  note: Hallgren solved the real quadratic case in 2002. Eisenträger, Hallgren, Kitaev and Song computed the unit group in any degree in 2014, and Biasse and Song extended the method to S-units, class groups and the principal ideal problem.
prereqs: [principal-ideal-problem, unit-group, hallgren-pell-algorithm, quantum-fourier-transform]
see_also: [quantum-class-group-algorithm, ideal-class-group, pell-equation, fourier-sampling, shor-algorithm, ring-lwe-hardness, closest-vector-problem, lll-algorithm]
sources:
  - paper: doi:10.1137/1.9781611974331.ch64
    title: "Jean-François Biasse and Fang Song, Efficient quantum algorithms for computing class groups and solving the principal ideal problem in arbitrary degree number fields, SODA 2016"
    locator: the reduction of the principal ideal problem to the computation of S-unit groups, and the quantum algorithm for S-units in any degree
  - paper: doi:10.1145/2591796.2591860
    title: "Kirsten Eisenträger, Sean Hallgren, Alexei Kitaev and Fang Song, A quantum algorithm for computing the unit group of an arbitrary degree number field, STOC 2014"
    locator: the continuous hidden subgroup problem on R^m and its application to the unit group in any degree
  - paper: doi:10.1145/1206035.1206039
    title: "Sean Hallgren, Polynomial-time quantum algorithms for Pell's equation and the principal ideal problem, Journal of the ACM 54(1), Article 4, 2007"
    locator: the quantum algorithm for the principal ideal problem in real quadratic fields, with a function on two variables that combines the ideal and the distance
  - paper: doi:10.1145/1060590.1060660
    title: "Sean Hallgren, Fast quantum algorithms for computing the unit group and class group of a number field, STOC 2005"
    locator: the extension to number fields of constant degree
  - paper: doi:10.1007/978-3-662-49896-5_20
    title: "Ronald Cramer, Léo Ducas, Chris Peikert and Oded Regev, Recovering short generators of principal ideals in cyclotomic rings, EUROCRYPT 2016"
    locator: the step from any generator to a short generator in cyclotomic fields of prime-power conductor, and its use with a quantum principal ideal algorithm
  - paper: doi:10.1103/RevModPhys.82.1
    title: "Andrew M. Childs and Wim van Dam, Quantum algorithms for algebraic problems, Reviews of Modern Physics 82:1-52, 2010"
    locator: the survey section on Pell's equation and the principal ideal problem
  - book: isbn:9780387849225
    title: Michael J. Jacobson Jr. and Hugh C. Williams, Solving the Pell Equation, Springer, 2009
    locator: reduced ideals of real quadratic fields, their cycles, distances and the infrastructure
---

The quantum principal ideal algorithm decides whether an ideal of a number field is principal and, if it is, finds a generator in compact form. Biasse and Song (2016) solved this in quantum polynomial time for fields of any degree, by computing a group of $S$-units with the continuous hidden subgroup algorithm of Eisenträger, Hallgren, Kitaev and Song. The real quadratic case, due to Hallgren (2002), is the smallest instance and is the one shown and implemented here. Together with the short generator step of Cramer, Ducas, Peikert and Regev, the algorithm breaks cryptosystems that hide a short generator of a principal ideal in a cyclotomic field.

## In plain words

An ideal is principal if all its numbers are multiples of one number, the generator. Checking this classically is slow for large fields, because the generator can be huge.

The quantum algorithm looks at the powers of the ideal and at the numbers that move them along a circle of small, standard ideals. All the ways to return to the same standard ideal form a hidden grid. The ideal is principal exactly when this grid has a point that uses the ideal once, and the position of that point gives the generator.

A quantum computer builds a superposition over the powers and the positions, writes down the standard ideal for each one, and applies a Fourier transform. Each measurement gives a rough estimate of where the generator sits on the circle. A classical check then looks near the estimate. If it finds the input ideal there, the answer is sure.

## The problem

The input is a number field $K$ of degree $d$ with ring of integers $\mathcal{O}_K$ and an ideal $\mathfrak{a}$, given by a $\mathbb{Z}$-basis. The output is "not principal", or a generator $\alpha$ with $\mathfrak{a} = \alpha\mathcal{O}_K$ in compact form, as on the page on the [principal ideal problem](/principal-ideal-problem/). The size $n$ counts the degree, the bit length of the discriminant and the bit length of the norm of $\mathfrak{a}$.

For a finite set $S$ of prime ideals, the **$S$-units** are the $\beta \in K^\ast$ such that $\beta\mathcal{O}_K$ is a product of powers of primes in $S$. They form a group of rank $|S| + r$, where $r$ is the rank of the [unit group](/unit-group/). If $S$ holds the primes that divide $\mathfrak{a} = \prod_{\mathfrak{p}\in S}\mathfrak{p}^{e_\mathfrak{p}}$, then $\mathfrak{a}$ is principal exactly when some $S$-unit $\beta$ has the valuations $v_\mathfrak{p}(\beta) = e_\mathfrak{p}$, and then $\beta$ is a generator. So the problem reduces to computing the $S$-unit group and solving a linear system over $\mathbb{Z}$.

The page shows the real quadratic case $K = \mathbb{Q}(\sqrt D)$ with $D$ squarefree, $D \equiv 2, 3 \pmod 4$ and $\mathcal{O}_K = \mathbb{Z}[\sqrt D]$. Here $r = 1$, the input is a reduced ideal $I = [Q, P + \sqrt D]$, and the set $S$ is replaced by the single ideal $I$, as in Hallgren's algorithm. The reduced ideals of each class lie on one cycle, as on the page on [Pell's equation](/pell-equation/). For a reduced ideal $\mathfrak{b} = \nu I^a$, the distance $\ln|\nu|$ is defined up to multiples of the regulator $R$.

## The algorithm

Let $g(a, k) = (\mathfrak{b}, \lfloor k - Nd \rfloor)$, where $\mathfrak{b} = \nu I^a$ is the reduced ideal of the class of $I^a$ with the largest distance $d = \ln|\nu| \le k/N$, and $N > 0$ is a scale. If $I = \alpha\mathcal{O}$, then $g(a, k)$ is the function of [Hallgren's algorithm for Pell's equation](/hallgren-pell-algorithm/) at $k + aN\ln|\alpha|$. In general $g$ hides the lattice $\Lambda$ of the pairs $(m, -N\ln|\beta|)$ with $I^m = \beta\mathcal{O}$, which is the image of the $I$-units. The lattice holds a point with $m = 1$ exactly when $I$ is principal. Fourier sampling over $a$ and $k$ gives points near the dual lattice, with $c \approx jq/(NR)$ for an integer $j$ and $b/A \approx cN\ln|\alpha|/q \pmod 1$.

```pseudo id=main
QUANTUM-PRINCIPAL-IDEAL(D, I, N, A, q, T)     ▷ I = [Q, P + √D] reduced; T rounds
L1  R ← the regulator of Z[√D], by Hallgren's algorithm for Pell's equation
L2  repeat T times
L3      (b, c) ← the outcome of lines L4 to L7
L4      prepare (Aq)^(-1/2) Σ_{a < A, k < q} |a⟩|k⟩|0⟩
L5      apply |a⟩|k⟩|0⟩ → |a⟩|k⟩|g(a, k)⟩        ▷ I^a by repeated squaring, then the ideal at distance k/N
L6      apply the QFT of Z_A to a and the QFT of Z_q to k
L7      measure b and c, and take c in (-q/2, q/2]
L8      if round(cNR/q) ≠ 0: for each t = (b/A + m) q/(cN) in [-w, R + w), m ∈ Z, with w = q/(|c|NA)
L9          for each reduced principal ideal J = θO with |ln θ - t| ≤ w (mod R)
L10             if J = I
L11                 return θ                      ▷ I = θO
L12 return "not principal"
```

Line L5 uses ideal multiplication and reduction, which keep track of the distance, and the infrastructure of the cycle to reach distance $k/N$ in polynomial time. Line L9 is classical: it computes the reduced principal ideals near distance $t$ and their generators in compact form. The samples with $j = \mathrm{round}(cNR/q) = 0$ give no information about the distance and are skipped.

## Example

Take $D = 7$ and $I = [2, 1 + \sqrt 7]$. The principal cycle holds $(1)$ at distance 0, $[3, 2 + \sqrt 7]$ at 1.5360, $[2, 1 + \sqrt 7]$ at 1.7309 and $[3, 1 + \sqrt 7]$ at 2.3313, and line L1 gives $R = \ln(8 + 3\sqrt 7) \approx 2.7687$. Take $N = 1.5$, $A = 16$ and $q = 32$, so $NR \approx 4.153$, and $g$ takes 6 values, which fit in a 3-qubit target. The circuit has $4 + 5 + 3 = 12$ qubits.

Row $a = 0$ of $g$ is the principal cycle: $(1)$ for $k = 0, 1, 2$ with the offsets 0, 1, 2, then $I$ at $k = 3$, then $[3, 1 + \sqrt 7]$ at $k = 4$, and $(1)$ again at $k = 5$. The ideal $[3, 2 + \sqrt 7]$ is skipped, because the interval $[2.30, 2.60)$ of $Nd$ values that it owns holds no integer. Row $a = 1$ starts at $I$ and is row 0 shifted by $N \cdot 1.7309 \approx 2.596$. For $a = 2$, $I^2 = 2(8 + 3\sqrt 7)\mathcal{O}$ reduces to $(1)$ with the factor $1/2$, at distance $-\ln 2$.

The outcome $(0, 0)$ has probability 0.1958 and carries no information. The outcomes $(10, 8)$ and $(6, 24)$ each have probability 0.1261. For $(10, 8)$, $j = 1$ and the only candidate is $t = (10/16) \cdot 32/12 \approx 1.6667$ with $w \approx 0.1667$, which holds 1.7309. One run with seed 1 samples $(0, 0)$ and then $(12, 16)$. Then $c = -16$, $j = -2$, $w = 1/12$, and the candidates are 0.3333 and 1.6667. No principal ideal lies within $1/12$ of 0.3333, and $I$ lies at 1.7309, within $1/12$ of 1.6667. So round 2 returns $\theta = 3 + \sqrt 7$, which has norm $9 - 7 = 2$ and lies in $I$ because $3 \equiv 1 \pmod 2$.

For a non-principal ideal, take $D = 10$ and $I = [2, \sqrt{10}]$. Its cycle holds the ideals with $Q = 2, 3, 3$, and the principal cycle holds only $(1)$. The rows of $g$ alternate between the two cycles, so the outcomes with $c = 0$ have $b \in \{0, 8\}$, which shows that the class of $I$ has order 2. No window ever holds $I$, and after $T$ rounds the algorithm returns "not principal".

## Correctness

Ideal multiplication gives $I_1I_2 = w[Q, P + \sqrt D]$ exactly, and each reduction step multiplies by a known $\mu$, so the oracle knows the distance of each reduced ideal $\nu I^a$. If $I^m = \beta\mathcal{O}$, the reduced ideals of the class of $I^{a+m}$ are those of $I^a$ with the distances shifted by $\ln|\beta|$, so $g$ is invariant under $\Lambda$ up to the rounding of the offset, the same weak periodicity as in Hallgren's algorithm. For a principal $I$ with $\delta = \ln|\alpha| \in [0, R)$, a good sample has $b/A - cN\delta/q$ within $1/A$ of an integer. Then one candidate of line L8 is within $w = q/(|c|NA)$ of $\delta$, line L9 lists $I$, and the round returns its generator. A returned $\theta$ is always correct, because line L10 compares ideals exactly and $\theta$ generates $J$. A non-principal ideal is never on the principal cycle, so the answer is then always "not principal". The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

- **One sample.** Line L5 computes $I^a$ for $a < A$ with $O(\log A)$ multiplications and reductions, and moves to distance $k/N$ with $O(\log(q/N))$ more steps of the infrastructure. Each step works with numbers of $O(\log D)$ bits and distances to $O(\log(qN))$ bits. So one sample takes time polynomial in $\log D$, $\log A$ and $\log q$.
- **Rounds.** With $A$, $q$ and $N$ of polynomial size, Hallgren's analysis bounds the probability of a good sample below by an inverse polynomial. For $D \le 23$ with the sizes of the example and $NR \approx 4.3$, the rate is 0.31 to 0.77 per round.
- **Classical part.** Line L8 gives $O(|j|)$ candidates, and line L9 looks at the few reduced principal ideals within $w$ of each candidate, again with the infrastructure.
- **Any degree.** Biasse and Song run in time polynomial in the degree, in $\log|\Delta_K|$ and in the size of $\mathfrak{a}$. The $S$-unit computation uses the continuous hidden subgroup algorithm on $\mathbb{Z}^{|S|} \times \mathbb{R}^r$, and the prime factors of $\mathfrak{a}$ come from factoring its norm with [Shor's algorithm](/shor-algorithm/).

## Properties

- **One-sided error.** A returned generator is always correct, and a non-principal ideal always gets "not principal". Only a principal ideal can get the wrong answer, with probability at most $(1 - p)^T$ for the rate $p$ of good samples.
- **No GRH for the principal ideal problem.** Biasse and Song state their principal ideal result without the generalized Riemann hypothesis. Their class group computation in any degree needs GRH, to bound the set of primes that generate the class group.
- **Compact output.** A generator can have exponentially many digits, so it comes as its distance and a product of powers of small elements. In the implementation the generators are small enough to give as $x + y\sqrt D$.
- **The $S$-unit group as a hidden lattice.** The hidden subgroup is the image of the $S$-units under the valuations and the logarithmic embedding. For the ideal $I$ alone and a real quadratic field, it is the rank-2 lattice $\Lambda$ above.

## Variants and improvements

- **Real quadratic fields.** Hallgren (2002) solved the problem with the function $g$ on two variables of this page, and the same work computes the regulator and, under GRH, the class group.
- **Constant degree.** Hallgren (2005) extended the method to fields of constant degree, with a hidden lattice in $\mathbb{Z}^k \times \mathbb{R}^r$.
- **Any degree.** Eisenträger, Hallgren, Kitaev and Song (2014) gave a continuous hidden subgroup algorithm on $\mathbb{R}^m$ that runs in time polynomial in $m$, and used it for the unit group. Biasse and Song (2016) applied it to $S$-unit groups, which gives the principal ideal problem and, under GRH, the class group in any degree.
- **Relation to the class group algorithm.** The [quantum class group algorithm](/quantum-class-group-algorithm/) covers the direct hidden subgroup approach on the class group, with the relations among generating primes. This page covers the $S$-unit approach. With $S$ as the generating primes, the valuations of the $S$-units are exactly the relations among them, so the $S$-unit group also gives the class group.
- **Short generators.** Cramer, Ducas, Peikert and Regev showed that in cyclotomic fields of prime-power conductor, any generator turns into the shortest one by a [closest vector](/closest-vector-problem/) step in the log-unit lattice with a known basis of cyclotomic units. With a quantum principal ideal algorithm, this recovers the secret key of schemes that hide a short generator.

## When to use it

Use it on a quantum computer to test whether an ideal is principal, to find a generator, or to solve norm equations in number fields of any degree. Its main use is cryptanalysis: with the short generator step, it breaks schemes such as Soliloquy, the Smart-Vercauteren encryption scheme and some candidate multilinear maps, which rest on finding a short generator of a principal ideal in a cyclotomic field. It does not break schemes based on [Ring-LWE](/ring-lwe-hardness/). In imaginary quadratic fields the problem is classically easy, and classically in general use the relation methods on the page on [class group computation](/ideal-class-group/).

## Pitfalls

- **The value must be canonical.** The oracle must write the reduced ideal and the rounded offset. An unreduced ideal or an offset that is not rounded the same way makes the same point give different values, and the samples lose their structure.
- **Skipped ideals.** When two ideals on the cycle are closer than $1/N$, the grid $k/N$ can skip one of them, as in the example. This does not hurt the classical check, which works on the cycle itself.
- **The window.** The window $w = q/(|c|NA)$ shrinks with $A$. With a small $A$, a window covers a large part of the cycle, and the check succeeds by luck rather than by the estimate. Compare the success rate with the share of the cycle that the windows cover, which is the success rate of random windows.
- **"Not principal" is a Monte Carlo answer.** It means that no round succeeded. Choose $T$ from the rate of good samples, or compute the full lattice $\Lambda$ and test it for a point with $m = 1$.
- **A generator is not a short generator.** For the cryptographic attacks, the generator from this algorithm still needs the short generator step, which works well only in fields with a good basis of the log-unit lattice.
- **The simulation is small.** The implementation computes $g$ by walking the cycle and takes $R$ from a walk of the principal cycle, which stands for Hallgren's algorithm. The state vector has at most 12 qubits, and the larger cases use the closed form of the output distribution.

## Implementations

## History

Buchmann and Williams proposed a key exchange in real quadratic fields in 1989 whose security rests on the principal ideal problem. Hallgren gave a quantum polynomial-time algorithm for the real quadratic case in 2002, which breaks it, and extended it to fields of constant degree in 2005. In 2014 Campbell, Groves and Shepherd described the Soliloquy scheme and a possible quantum attack on it through the principal ideal problem, and Eisenträger, Hallgren, Kitaev and Song gave the continuous hidden subgroup algorithm for the unit group in any degree. In 2016 Biasse and Song solved the principal ideal problem in any degree with $S$-units, and in the same year Cramer, Ducas, Peikert and Regev showed how to turn a generator into a short one in cyclotomic fields.

## References
