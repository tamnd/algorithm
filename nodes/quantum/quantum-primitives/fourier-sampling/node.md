---
tag: C3A113
kind: technique
slug: fourier-sampling
name: Fourier sampling
area: quantum/quantum-primitives
level: core
summary: "Query f once on a uniform superposition, apply the Fourier transform of the group and measure. If f hides a subgroup K, the outcome is uniform on the characters that are trivial on K."
prereqs: [quantum-fourier-transform, walsh-hadamard-transform, quantum-oracle, quantum-measurement]
see_also: [deutsch-jozsa-algorithm, bernstein-vazirani-algorithm, simon-algorithm, order-finding, shor-algorithm, quantum-discrete-logarithm, quantum-phase-estimation, fourier-analysis-of-boolean-functions]
sources:
  - paper: doi:10.1137/S0097539796300921
    title: "Ethan Bernstein and Umesh Vazirani, Quantum complexity theory, SIAM Journal on Computing 26(5):1411-1473, 1997"
    locator: sampling from the Fourier spectrum of a Boolean function, and the recursive Fourier sampling problem (section number not checked)
  - paper: doi:10.1137/S0097539796298637
    title: "Daniel R. Simon, On the power of quantum computation, SIAM Journal on Computing 26(5):1474-1483, 1997"
    locator: samples orthogonal to a hidden XOR period, with classical linear algebra
  - paper: doi:10.1137/S0097539795293172
    title: "Peter W. Shor, Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer, SIAM Journal on Computing 26(5):1484-1509, 1997"
    locator: Fourier sampling over the integers modulo a power of 2 for periods, and over a product of two cyclic groups for discrete logarithms
  - paper: doi:10.1137/S009753970139450X
    title: "Sean Hallgren, Alexander Russell and Amnon Ta-Shma, The hidden subgroup problem and quantum computation using group representations, SIAM Journal on Computing 32(4):916-934, 2003"
    locator: Fourier sampling over nonabelian groups when only the name of the representation is measured, which finds normal hidden subgroups
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 5.4 (period finding, discrete logarithms and the hidden subgroup problem)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Chapter 6 (the hidden subgroup problem and its solution for abelian groups)
---

*Fourier sampling* is the pattern behind the first quantum speedups. Put the input register in a uniform superposition over a finite abelian group $G$, query the function $f$ once, apply the Fourier transform of $G$, and measure. The outcome is a random character of $G$. If $f$ is constant on the cosets of an unknown subgroup $K$ and distinct on different cosets, the outcome is uniform on the characters that are trivial on $K$. A few samples then give $K$ by classical post-processing: linear algebra mod $2$ for $G = \mathbb{Z}_2^n$, or a greatest common divisor or [continued fractions](/continued-fraction/) for $G = \mathbb{Z}_N$. With a phase oracle, the outcome is a sample from the squared Fourier spectrum of $(-1)^f$. The [Deutsch-Jozsa](/deutsch-jozsa-algorithm/), [Bernstein-Vazirani](/bernstein-vazirani-algorithm/) and [Simon](/simon-algorithm/) algorithms and the period finding step of [Shor's algorithm](/shor-algorithm/) are all instances.

## In plain words

Some functions repeat. They give the same output on inputs that differ by a hidden step, and different outputs otherwise. Finding the step by trying inputs one by one can take a very long time.

Fourier sampling asks about all inputs at once and then looks at the result through a Fourier transform, which picks out the ways in which the result repeats. One measurement gives one random clue about the hidden step. Each clue is a sample from a small set that the step decides. After enough clues, a classical program solves for the step. The quantum part is short and is the same for many problems, and only the group and the classical part change.

## When it applies

- The input set is a finite abelian group $G$, such as $\mathbb{Z}_2^n$ (bit strings with XOR), $\mathbb{Z}_N$ (integers mod $N$) or a product of such groups.
- The function $f$ on $G$ has a hidden subgroup $K$: $f(x) = f(x')$ exactly when $x - x' \in K$. Or $f$ is Boolean and the question is about its Fourier spectrum, for example "which character has all the weight".
- $f$ is given as an oracle that can be queried on a superposition, with no garbage left in work qubits.
- The Fourier transform of $G$ has an efficient circuit: $H^{\otimes n}$ for $\mathbb{Z}_2^n$, the [QFT](/quantum-fourier-transform/) for $\mathbb{Z}_{2^n}$, and approximate transforms for other $\mathbb{Z}_N$.
- The subgroup can be recovered from a few uniform elements of its annihilator by classical work.

## The template

The characters of $G$ are the maps $\chi_y : G \to \mathbb{C}$, $\chi_y(x) = (-1)^{x \cdot y}$ for $G = \mathbb{Z}_2^n$ and $\chi_y(x) = e^{2\pi i xy/N}$ for $G = \mathbb{Z}_N$. The Fourier transform of $G$ is $|x\rangle \mapsto |G|^{-1/2} \sum_y \chi_y(x) |y\rangle$. The annihilator of $K$ is $K^\perp = \{y : \chi_y(k) = 1 \text{ for all } k \in K\}$, a subgroup with $|K^\perp| = |G|/|K|$. Qubit $0$ is the least significant bit of $x$ and $y$, as on [quantum state](/quantum-state/).

```pseudo id=main
FOURIER-SAMPLE(G, U_f)                     ▷ hole: the group and an oracle for f on G
L1  prepare |0⟩ on the input register and |0⟩ on the output register
L2  apply the Fourier transform of G to the input register   ▷ gives |G|^(-1/2) Σ_x |x⟩
L3  apply U_f: |x⟩|0⟩ → |x⟩|f(x)⟩          ▷ the only query
L4  measure or discard the output register ▷ optional: it does not change the law of y
L5  apply the Fourier transform of G to the input register
L6  measure the input register and return y ▷ hole: repeat, then post-process the samples
```

**Why it works.** After line L3 the state is $|G|^{-1/2} \sum_x |x\rangle |f(x)\rangle$. Group the inputs by cosets of $K$: with $|c + K\rangle = |K|^{-1/2} \sum_{k \in K} |c + k\rangle$, the state is $\sqrt{|K|/|G|} \sum_{c} |c + K\rangle |f(c)\rangle$, where $c$ runs over one element of each coset and the values $f(c)$ are distinct. The Fourier transform maps a coset state to

$$|c + K\rangle \mapsto \sqrt{\frac{|K|}{|G|}} \sum_{y \in K^\perp} \chi_y(c) |y\rangle,$$

because $\sum_{k \in K} \chi_y(k)$ is $|K|$ for $y \in K^\perp$ and $0$ otherwise. The output states $|f(c)\rangle$ are orthogonal, so $\Pr[y] = \sum_c (|K|/|G|)^2 = |K|/|G| = 1/|K^\perp|$ for each $y \in K^\perp$. The offset $c$ appears only in the phase $\chi_y(c)$, so it does not matter which coset the state is in. This is also why line L4 changes nothing.

**The phase form.** With the phase oracle $|x\rangle \mapsto (-1)^{f(x)} |x\rangle$ for $G = \mathbb{Z}_2^n$, lines L1 to L6 give $y$ with probability $\hat F(y)^2$, where $\hat F(y) = 2^{-n} \sum_x (-1)^{f(x) + x \cdot y}$ is the Fourier coefficient of $F = (-1)^f$ (see [Fourier analysis of Boolean functions](/fourier-analysis-of-boolean-functions/)). By Parseval the squares sum to $1$.

**Example over $\mathbb{Z}_2^3$.** Take $s = 110$ and an $f$ with $f(x) = f(x \oplus s)$, two-to-one. Then $K = \{000, 110\}$, and $K^\perp = s^\perp = \{000, 001, 110, 111\}$. The simulator in the implementation of [Simon's algorithm](/simon-algorithm/) gives each of the four outcomes with probability $1/4$ and the others with probability $0$. The samples $001$, $000$, $110$ (seed $7$) span a space of rank $2$, and the only nonzero solution of $y \cdot s = 0$ for all of them is $s = 110$.

**Example over $\mathbb{Z}_8$.** Take $f(x) = x \bmod 4$, so $K = \{0, 4\}$ and $K^\perp = \{0, 2, 4, 6\}$, the multiples of $N/r = 8/4 = 2$. Each outcome has probability $1/4$. If line L4 gives $f = 1$, the input register is $(|1\rangle + |5\rangle)/\sqrt{2}$, the example on the [QFT](/quantum-fourier-transform/) page. The samples $2$ and $6$ give $r = 8/\gcd(8, 2, 6) = 4$.

## Classic examples

- **Deutsch-Jozsa.** $G = \mathbb{Z}_2^n$ with the phase oracle. For a constant $f$ the spectrum is all at $y = 0$, and for a balanced $f$ it has no weight at $0$, so one sample decides. See the [Deutsch-Jozsa algorithm](/deutsch-jozsa-algorithm/).
- **Bernstein-Vazirani.** $G = \mathbb{Z}_2^n$ with the phase oracle of $f(x) = s \cdot x$. The spectrum is all at $y = s$, so one sample gives $s$. See the [Bernstein-Vazirani algorithm](/bernstein-vazirani-algorithm/).
- **Simon.** $G = \mathbb{Z}_2^n$ and $K = \{0, s\}$. Each sample is uniform on $s^\perp$, and about $n$ samples and [Gaussian elimination mod 2](/linear-system-modulo-2/) give $s$. See [Simon's algorithm](/simon-algorithm/).
- **Period finding.** $G = \mathbb{Z}_N$ and $K = r\mathbb{Z}_N$ for a period $r$ that divides $N$. The samples are $y = jN/r$ with $j$ uniform mod $r$, and $r = N/\gcd(N, y_1, \ldots, y_k)$ once $\gcd(j_1, \ldots, j_k, r) = 1$. For $k = 2$ this happens with probability at least $\prod_p (1 - p^{-2}) = 6/\pi^2$.
- **Order finding and factoring.** $f(x) = a^x \bmod M$ on $\mathbb{Z}_N$ with $N = 2^n$ a power of $2$. The period $r$ does not divide $N$ in general, so the samples are only near $jN/r$, and [continued-fraction post-processing](/continued-fraction-post-processing/) recovers $r$. This is the quantum part of [Shor's algorithm](/shor-algorithm/) and of [order finding](/order-finding/).
- **Discrete logarithms.** $G = \mathbb{Z}_r \times \mathbb{Z}_r$ and $f(x_1, x_2) = g^{x_1} h^{-x_2}$ with $h = g^\ell$. The hidden subgroup is generated by $(\ell, 1)$, and each sample $(y_1, y_2)$ satisfies $y_1 \ell + y_2 \equiv 0 \pmod r$, which gives $\ell$. See [quantum discrete logarithm](/quantum-discrete-logarithm/).

## Variations

- **Measured or discarded output.** Line L4 can measure the output register, discard it, or leave it alone. The law of $y$ is the same, because the output states for different cosets are orthogonal.
- **Hadamard gates for the first transform.** Over $\mathbb{Z}_{2^n}$, line L2 only has to make the uniform superposition, so $H^{\otimes n}$ is enough there, and only line L5 needs the QFT. Shor's algorithm and phase estimation do this.
- **Periods that do not divide $N$.** Take $N$ much larger than $r^2$. The outcomes are then near the multiples of $N/r$, with a peak of width about $1$, and continued fractions recover $j/r$.
- **Other abelian groups.** For $\mathbb{Z}_N$ with $N$ not a power of $2$, use an approximate Fourier transform. For products of cyclic groups, use the transform of each factor. The same template then solves the hidden subgroup problem for every finite abelian group whose structure is known.
- **Recursive Fourier sampling.** Bernstein and Vazirani nested Fourier sampling problems inside each other, where each oracle answer is itself the answer to a smaller Fourier sampling problem. This gave the first superpolynomial gap between quantum and classical query complexity with bounded error.
- **Nonabelian groups.** The Fourier transform of a nonabelian group gives an irreducible representation and a row and column inside it. *Weak Fourier sampling* measures only the representation, and it finds normal hidden subgroups (Hallgren, Russell and Ta-Shma), but it cannot tell conjugate subgroups apart. *Strong Fourier sampling* also measures the row and column, and its power depends on the basis. For the dihedral and symmetric groups no efficient method is known.
- **Learning from the spectrum.** For a Boolean $f$ with most of its Fourier weight on a few characters, repeated phase-form samples find those characters. This is a quantum form of finding the large Fourier coefficients of $f$.

## Pitfalls

- **Garbage in the oracle.** If the circuit for $f$ leaves work qubits that depend on $x$, they act as extra output, which is fine only if they are a function of $f(x)$ alone. Work qubits that depend on $x$ in another way change the cosets. Clear them by [uncomputation](/uncomputation/).
- **Collisions across cosets.** If $f$ is constant on the cosets of $K$ but takes equal values on two different cosets, the samples still lie in $K^\perp$, but they need not be uniform and may miss part of it. A constant $f$ gives only $y = 0$, which says nothing about $K$.
- **One sample is not an answer.** Each sample is one random element of $K^\perp$. Plan the number of runs from the post-processing, and check the answer with classical queries, for example $f(0) = f(s)$ in Simon's problem or $a^r \equiv 1 \pmod M$ in order finding.
- **The sign of the transform.** For sampling the sign does not matter, because it maps $y$ to $-y$ and $K^\perp$ to itself. In post-processing that uses the value of $y$, as for discrete logarithms, the sign must match the equations.
- **Bit order.** Read qubit $j$ as bit $j$ of $y$. Over $\mathbb{Z}_N$ a reversed order gives wrong values. Over $\mathbb{Z}_2^n$ it gives the hidden string with its bits reversed.
- **Exponential speedup is relative to an oracle.** The gaps of Simon and Bernstein-Vazirani are in the query model. For factoring the oracle is a circuit, and the speedup is over the best known classical algorithm only.

## Exercises

1. Show that the distribution of $y$ in the template does not change if line L4 is removed.
2. For $G = \mathbb{Z}_{16}$ and $f(x) = x \bmod 4$, give the distribution of $y$. What does $\gcd(16, y_1, y_2)$ tell you?
3. Prove that with the phase oracle over $\mathbb{Z}_2^n$, the outcome $y$ has probability $\hat F(y)^2$, and that these probabilities sum to $1$.
4. For $G = \mathbb{Z}_2^n$ and a hidden subgroup $K$ of dimension $d$, show that the expected number of samples until they span $K^\perp$ is less than $n - d + 2$.
5. Let $j_1, j_2$ be independent and uniform mod $r$. Show that $\Pr[\gcd(j_1, j_2, r) = 1] = \prod_{p \mid r} (1 - p^{-2}) \ge 6/\pi^2$.
6. Over $\mathbb{Z}_N$, show that the template gives $y = 0$ with probability $1/|K^\perp|$, and use it to estimate the number of cosets of $K$.

## References
