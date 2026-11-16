---
tag: 23FVBZ
kind: concept
slug: circuit-complexity
name: Circuit complexity
aliases:
- boolean circuit complexity
area: complexity/complexity-classes
level: advanced
summary: The study of how many gates, or how many layers of gates, a Boolean circuit needs to compute a given function, and why lower bounds on this are so hard to prove.
prereqs: [boolean-circuit, non-uniform-computation, counting-argument]
see_also: [ac0, tc0, nc, p-poly, natural-proofs-barrier, karchmer-wigderson-theorem, algorithmic-method, hardness-versus-randomness]
sources:
  - paper: doi:10.1002/j.1538-7305.1949.tb03624.x
    title: Claude E. Shannon, The synthesis of two-terminal switching circuits, Bell System Technical Journal 28(1), 59 to 98 (1949)
    locator: the counting argument that almost all functions need large circuits
  - paper: doi:10.1109/FOCS.2016.19
    title: Magnus G. Find, Alexander Golovnev, Edward A. Hirsch and Alexander S. Kulikov, A better-than-3n lower bound for the circuit complexity of an explicit function, 57th IEEE Symposium on Foundations of Computer Science, 89 to 98 (2016)
    locator: the main theorem
  - paper: doi:10.1145/3519935.3519976
    title: Jiatu Li and Tianqi Yang, 3.1n - o(n) circuit lower bounds for explicit functions, 54th ACM Symposium on Theory of Computing, 1180 to 1193 (2022)
    locator: the main theorem
  - paper: doi:10.1007/BF01405045
    title: V. M. Khrapchenko, Complexity of the realization of a linear function in the class of II-circuits, Mathematical Notes of the Academy of Sciences of the USSR 9(1), 21 to 23 (1971)
    locator: the n^2 lower bound on the formula size of parity
  - paper: doi:10.1137/S0097539794261556
    title: Johan Håstad, The shrinkage exponent of de Morgan formulas is 2, SIAM Journal on Computing 27(1), 48 to 64 (1998)
    locator: the shrinkage theorem and the formula lower bound for the Andreev function
  - paper: doi:10.1145/2559903
    title: Ryan Williams, Nonuniform ACC circuit lower bounds, Journal of the ACM 61(1) (2014)
    locator: the theorem that NEXP is not in ACC0
  - paper: doi:10.1006/jcss.1997.1494
    title: Alexander A. Razborov and Steven Rudich, Natural proofs, Journal of Computer and System Sciences 55(1), 24 to 35 (1997)
    locator: the definition of natural proofs and the main theorem
  - book: isbn:9783642245077
    title: Stasys Jukna, Boolean Function Complexity, Advances and Frontiers, Springer (2012)
    locator: the chapters on general circuits, formulas (Khrapchenko's bound) and bounded-depth circuits
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 6, Boolean circuits, and Chapter 14, Circuit lower bounds
---

Circuit complexity measures a Boolean function by the smallest [Boolean circuit](/boolean-circuit/) that computes it: the number of gates (size), the length of the longest input-to-output path (depth), or the number of leaves of a formula. It gives a non-uniform view of computation, because each input length gets its own circuit, and it is the main known route to proving that a problem is hard without a statement about all algorithms. A counting argument shows that almost every function needs exponential size, but for no explicit function, and in particular for no problem in [NP](/np/), is any superlinear lower bound for general circuits known. The field is the study of this gap, of the restricted models where strong lower bounds are known, and of the barriers that explain why the general case resists.

## In plain words

A circuit is a fixed wiring of simple logic gates, built for one input size. Circuit complexity asks how small such a wiring can be for a given task, such as adding numbers or checking whether a graph has a large clique. Small circuits mean the task is easy, at least in principle. Most tasks have no small circuit at all, and this is easy to prove by counting. The hard part is to name one specific, useful task and prove that it has no small circuit. Nobody can do this yet for general circuits. Researchers prove it for weaker kinds of circuits instead, for example circuits with only a few layers, and they also study why the known methods stop working.

## The idea

**Measures.** For a function $f : \{0,1\}^n \to \{0,1\}$ and a set of allowed gates (a basis), the main measures are:

- *Size* $C(f)$: the minimum number of gates of a circuit for $f$. With fan-in 2 gates, this corresponds to sequential time, because a machine that runs in time $T(n)$ has circuits of size $O(T(n)^2)$, and $O(T(n) \log T(n))$ with a more careful simulation.
- *Depth* $D(f)$: the minimum length of a longest path. This corresponds to parallel time, see [NC](/nc/).
- *Formula size* $L(f)$: the minimum number of leaves of a formula, that is a circuit in which every gate has fan-out 1. For fan-in 2, $D(f) = \Theta(\log L(f))$ (Spira), so formula size and depth are two views of one measure.

A language $L$ has circuits of size $s(n)$ if for each $n$ some circuit of size $s(n)$ decides $L \cap \{0,1\}^n$. With $s$ a polynomial, this defines [P/poly](/p-poly/). The [Karchmer-Wigderson theorem](/karchmer-wigderson-theorem/) turns depth into a communication game: $D(f)$ equals the communication complexity of finding a position where an input with $f = 1$ and an input with $f = 0$ differ.

**Why lower bounds matter.** Polynomial-time machines have polynomial-size circuits, so $\mathsf{P} \subseteq \mathsf{P/poly}$. A superpolynomial circuit lower bound for any problem in NP would therefore prove $\mathsf{P} \ne \mathsf{NP}$. Lower bounds also give pseudorandomness: by the [hardness versus randomness](/hardness-versus-randomness/) results, a function in exponential time that needs circuits of size $2^{\Omega(n)}$ gives $\mathsf{P} = \mathsf{BPP}$ ([Impagliazzo-Wigderson theorem](/impagliazzo-wigderson-theorem/)).

**The counting gap.** There are $2^{2^n}$ functions of $n$ bits, and at most $2^{O(s \log s)}$ circuits of size $s$. So most functions need size $\Omega(2^n / n)$ (Shannon 1949, proved on the [Boolean circuit](/boolean-circuit/) page), and every function has size $O(2^n / n)$ (Lupanov). The counting proof does not name a hard function. For explicit functions over the full basis of fan-in 2 gates, the best known lower bound was $3n - o(n)$ for decades, then slightly above $3n$ (Find, Golovnev, Hirsch and Kulikov 2016), and now $3.1n - o(n)$ (Li and Yang 2022). The gap between linear and exponential is the central open problem of the field.

**Restricted models.** Because general circuits resist, most progress is in models with a restriction on the circuit:

| Model | Restriction | Strongest known type of bound |
|---|---|---|
| De Morgan formulas | fan-out 1, gates AND, OR, NOT | $n^{3 - o(1)}$ for the Andreev function (Håstad 1998) |
| [AC0](/ac0/) | constant depth, unbounded fan-in AND, OR | $\exp(\Omega(n^{1/(d-1)}))$ for parity at depth $d$ |
| AC0 with MOD p gates, p prime | as AC0, plus MOD p gates | exponential for MOD q, q a different prime (Razborov, Smolensky) |
| ACC0 | as AC0, plus MOD m gates for a fixed m | NEXP is not in ACC0 (Williams 2011) |
| Monotone circuits | AND, OR only | exponential for clique (Razborov 1985, then Alon and Boppana) |
| [TC0](/tc0/) | constant depth, majority gates | no superpolynomial bound for any problem in NEXP is known |

Each row stops at a natural next step. Parity is easy once MOD 2 gates are allowed, majority is easy once threshold gates are allowed, and for TC0 it is open whether NEXP has polynomial-size majority circuits even of depth 3.

**Barriers.** Three results explain part of the difficulty. Proofs that [relativize](/relativization/), such as diagonalization, cannot separate P from NP. [Natural proofs](/natural-proofs-barrier/) (Razborov and Rudich 1997), which give a property that is easy to test and true of most functions, cannot prove lower bounds for a class that has [pseudorandom functions](/pseudorandom-function/). Most known circuit lower bounds are natural. Algebrization (Aaronson and Wigderson 2008) extends the relativization barrier to the arithmetic methods used for [IP = PSPACE](/ip-equals-pspace/). Williams' ACC0 bound avoids the natural proofs barrier by the [algorithmic method](/algorithmic-method/): a satisfiability algorithm for a circuit class that beats brute force by a small factor gives a lower bound for that class.

## Examples

**Formula size of three-variable functions.** Exhaustive search over de Morgan formulas, with literals $x_i$ and $\lnot x_i$ as leaves and gates AND and OR, gives the formula size of every one of the $256$ functions of $3$ bits. Majority of $3$ bits needs $5$ leaves, as in $(x_1 \land (x_2 \lor x_3)) \lor (x_2 \land x_3)$. Parity of $3$ bits, and its negation, need $10$ leaves, and they are the only two functions of $3$ bits that need more than $8$. Khrapchenko's bound (1971) gives $L(\oplus_n) \ge n^2$, here $9$, by counting the pairs of inputs at Hamming distance $1$ across the boundary between $f = 1$ and $f = 0$. So the bound is close for $n = 3$ but not exact. Khrapchenko's method can never give more than $n^2$, and the best formula lower bounds known for any explicit function are about $n^3$.

**Depth 2 against depth 3 for parity.** A DNF for parity of $n$ bits needs $2^{n-1}$ terms: every term must fix all $n$ variables, since a term with a free variable accepts inputs of both parities. For $n = 4$ that is $8$ terms of $4$ literals. With depth $d$, size $\exp(O(n^{1/(d-1)}))$ is enough and also necessary, which is the content of the [AC0](/ac0/) lower bounds. One extra layer of depth lowers the cost from $2^{n-1}$ to about $2^{\sqrt{n}}$.

**A problem in P with no known nonlinear bound.** [Integer multiplication](/integer-multiplication/) of two $n$-bit numbers has circuits of size $n^{1 + o(1)}$ by FFT-based methods, and the best lower bound for general circuits is linear. Many functions in NP are believed to need exponential size, but the known bound for each of them is also linear.

**The minimum circuit size problem.** Given the truth table of $f$, of length $N = 2^n$, and a number $s$, does $f$ have a circuit of size at most $s$? This problem is in NP: guess the circuit and evaluate it on all $N$ inputs. Whether it is NP-complete is open, and results on it connect circuit lower bounds, cryptography and learning.

## Where it is used

- *Parallel algorithms.* The classes [NC](/nc/), [AC0](/ac0/) and [TC0](/tc0/) describe what can be computed in polylogarithmic or constant parallel time, and [P-completeness](/circuit-value-problem/) is the evidence that a problem is inherently sequential.
- *Derandomization.* Circuit lower bounds for exponential time give [pseudorandom generators](/pseudorandom-generator/), for example the [Nisan-Wigderson generator](/nisan-wigderson-generator/), and so deterministic simulations of [BPP](/bpp/).
- *Cryptography.* Security is defined against adversaries that are circuits of polynomial size, so [one-way functions](/one-way-function/) are defined with respect to P/poly, not P.
- *Learning.* Fourier analysis of AC0 (Linial, Mansour and Nisan) gives quasi-polynomial time learning algorithms for constant-depth circuits, see [Fourier analysis of Boolean functions](/fourier-analysis-of-boolean-functions/).
- *Structural complexity.* The [Karp-Lipton theorem](/karp-lipton-theorem/) says that if NP has polynomial-size circuits, the [polynomial hierarchy](/polynomial-hierarchy/) collapses. This is evidence that NP has no small circuits.
- *Logic synthesis.* Hardware design minimizes circuits in practice. [Exact synthesis](/exact-synthesis/) finds a provably smallest circuit for small functions with a SAT solver.

## References
