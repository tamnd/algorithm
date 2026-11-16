---
tag: Z8JRKC
kind: definition
slug: bpp
name: BPP
aliases:
- bounded-error probabilistic polynomial time
area: complexity/complexity-classes
level: core
summary: The decision problems that a probabilistic machine decides in polynomial time with error at most 1/3 on every input. Repetition with a majority vote makes the error exponentially small.
prereqs: [probabilistic-turing-machine, p, two-sided-error, chernoff-bound]
see_also: [rp, zpp, pp, bqp, adleman-theorem, sipser-gacs-theorem, impagliazzo-wigderson-theorem, error-amplification]
sources:
  - paper: doi:10.1137/0206049
    title: John Gill, Computational complexity of probabilistic Turing machines, SIAM Journal on Computing 6(4), 675 to 695 (1977)
    locator: the definitions of PP and BPP, and the bound BPP in PSPACE
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 7, Randomized computation (BPP, error reduction, BPP and the other classes)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition, Cengage (2013)
    locator: Section 10.2, Probabilistic algorithms (the class BPP and the amplification lemma)
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity, Addison-Wesley (1994)
    locator: Chapter 11, Randomized computation
  - paper: doi:10.1137/0210008
    title: Charles H. Bennett and John Gill, Relative to a random oracle A, P^A != NP^A != co-NP^A with probability 1, SIAM Journal on Computing 10(1), 96 to 113 (1981)
    locator: the result that P^A = BPP^A for a random oracle A with probability 1
  - paper: doi:10.4007/annals.2004.160.781
    title: Manindra Agrawal, Neeraj Kayal and Nitin Saxena, PRIMES is in P, Annals of Mathematics 160(2), 781 to 793 (2004)
    locator: the main theorem
---

BPP (bounded-error probabilistic polynomial time) is the class of decision problems that a [probabilistic Turing machine](/probabilistic-turing-machine/) decides in polynomial time, with a wrong answer of probability at most $1/3$ on every input. The error is [two-sided](/two-sided-error/): the machine may err on yes-instances and on no-instances. The constant $1/3$ is arbitrary, because a majority vote over independent runs makes the error exponentially small. BPP contains [P](/p/), and whether the two classes are equal is open; most researchers conjecture that they are, and strong circuit lower bounds would prove it.

## Definition

**Model.** The machine is a probabilistic [multitape Turing machine](/multitape-turing-machine/): at each step it flips a fair coin and chooses one of two transition functions. Equivalently, it is a deterministic machine $M$ that reads the input $x$ and a string $r$ of coin flips. The time bound holds for every input and every coin sequence, so it is a worst-case bound, not an expected one. P and BPP do not change under polynomial-time simulations between machine models ([multitape simulation](/multitape-simulation-theorem/), [RAM and Turing machine](/ram-turing-equivalence/)), so the multitape choice does not matter for the class.

**Definition (Gill 1977).** A language $L \subseteq \{0,1\}^*$ is in $\mathsf{BPP}$ if there are a polynomial $p$ and a deterministic machine $M$ that runs in time polynomial in $|x|$ such that for every $x$:

$$x \in L \Rightarrow \Pr_r[M(x, r) = 1] \ge 2/3, \qquad x \notin L \Rightarrow \Pr_r[M(x, r) = 1] \le 1/3,$$

where $r$ is uniform on $\{0,1\}^{p(|x|)}$. The probability is over the coins only. The input is fixed and arbitrary: a machine that is right on most inputs but wrong on some input with probability $1$ does not show that $L \in \mathsf{BPP}$.

**The constants do not matter.** Let $q$ and $s$ be polynomials. The class does not change if the two conditions are replaced by "$\Pr[M(x,r) = L(x)] \ge 1/2 + 1/q(|x|)$" (a weaker condition) or by "$\Pr[M(x,r) = L(x)] \ge 1 - 2^{-s(|x|)}$" (a stronger one). To go from the weak form to the strong form, run $M$ for an odd number $k$ of times with independent coins and output the majority answer. Let the error of one run be at most $1/2 - \gamma$. The majority is wrong only if at least $k/2$ runs are wrong, and by the [Chernoff](/chernoff-bound/)-Hoeffding bound this has probability at most $e^{-2\gamma^2 k}$. With $\gamma = 1/q(n)$, the choice $k = q(n)^2 s(n)$ gives error below $2^{-s(n)}$, and the time grows by a factor $k$, which is polynomial. The full proof is on the page of the [probabilistic Turing machine](/probabilistic-turing-machine/), and the method is [error amplification](/error-amplification/).

The exact error of a majority of $k$ runs, each wrong with probability exactly $1/3$, is the binomial tail $\sum_{j > k/2} \binom{k}{j} (1/3)^j (2/3)^{k-j}$:

| runs $k$ | 1 | 3 | 5 | 9 | 15 | 31 | 51 |
|---|---|---|---|---|---|---|---|
| exact error | 0.333 | 0.259 | 0.210 | 0.145 | 0.0882 | 0.0270 | 0.00689 |
| bound $e^{-k/18}$ | 0.946 | 0.846 | 0.757 | 0.607 | 0.435 | 0.179 | 0.0588 |

The least odd $k$ with exact error at most $2^{-10}$ is $81$, and for $2^{-40}$ it is $423$. The bound $e^{-k/18} \le 2^{-s}$ asks for $k \ge 18\, s \ln 2$, which is $125$ for $s = 10$ and $500$ for $s = 40$. In both cases the number of runs grows linearly in $s$.

**The gap must be at least an inverse polynomial.** If a single run is right with probability only $1/2 + \gamma$, about $1/\gamma^2$ runs are needed. With $\gamma = 1/10$, 5 runs bring the error from $0.4$ down to at most $1/3$. With $\gamma = 1/100$, 465 runs are needed. With $\gamma = 2^{-10}$, even 1001 runs leave an error of $0.475$. A gap of $2^{-n}$ would need about $4^n$ runs, so it cannot be amplified in polynomial time. Machines with such gaps define the larger class [PP](/pp/).

**Basic properties.**

- *Complement.* $\mathsf{BPP}$ is closed under complement: swap the answers of $M$. So $\mathsf{BPP} = \mathsf{coBPP}$.
- *Union and intersection.* If $L_1, L_2 \in \mathsf{BPP}$, amplify both machines to error at most $1/6$ and run both. By the [union bound](/union-bound/), both answers are right with probability at least $2/3$, so $L_1 \cup L_2$ and $L_1 \cap L_2$ are in $\mathsf{BPP}$.
- *Reductions.* If $A \le_p B$ by a polynomial-time many-one (Karp) reduction $f$ and $B \in \mathsf{BPP}$, then $A \in \mathsf{BPP}$: run the machine for $B$ on $f(x)$.
- *A deterministic simulation.* $\mathsf{BPP} \subseteq \mathsf{PSPACE}$: run $M(x, r)$ for each of the $2^{p(n)}$ strings $r$ in turn, reuse the space, and count the accepting ones (Gill 1977). So $\mathsf{BPP} \subseteq \mathsf{EXP}$ as well.

## Examples and non-examples

**Examples.**

- *Every problem in P.* A deterministic machine ignores its coins and has error $0$.
- *Polynomial identity testing.* Given an arithmetic circuit over the integers, is the polynomial that it computes identically zero? Evaluate it at a random point from a large enough set; by the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/), a nonzero polynomial of degree $d$ vanishes at a random point of $S^n$ with probability at most $d/|S|$. This test never rejects the zero polynomial, so the problem is in [coRP](/co-rp/) and hence in BPP. No deterministic polynomial-time algorithm is known. See [polynomial identity testing](/polynomial-identity-testing/).
- *Primality.* The [Miller-Rabin test](/miller-rabin-primality-test/) never rejects a prime and accepts an odd composite with probability at most $1/4$ for a random base, so PRIMES is in coRP, and so in BPP. For 25 years this was the main example of a randomized algorithm with no known deterministic counterpart. In 2002 Agrawal, Kayal and Saxena showed that PRIMES is in P ([AKS test](/aks-primality-test/)). It is an example of a problem that moved from BPP to P.
- *Problems with one-sided error.* [RP](/rp/), coRP and [ZPP](/zpp/) are subsets of BPP. An RP machine run twice, accepting if either run accepts, has two-sided error at most $1/4$.

**Non-examples and open cases.**

- *Gaps that are too small.* The language MAJSAT of Boolean formulas that are satisfied by more than half of their assignments has a polynomial-time machine with acceptance probability above $1/2$ exactly on the yes-instances (pick a random assignment and test it). The gap can be $2^{-n}$, so this does not put MAJSAT in BPP. MAJSAT is PP-complete, and it is not known to be in BPP.
- *NP-complete problems.* No NP-complete problem is known to be in BPP. If $\mathsf{NP} \subseteq \mathsf{BPP}$, then $\mathsf{NP} \subseteq \mathsf{P/poly}$ by [Adleman's theorem](/adleman-theorem/), and the polynomial hierarchy collapses to its second level by the [Karp-Lipton theorem](/karp-lipton-theorem/).
- *Undecidable problems.* The halting problem is not in BPP, because $\mathsf{BPP} \subseteq \mathsf{EXP}$ and every language in EXP is decidable. Randomness with bounded error does not decide more languages than a deterministic machine; it may only decide them faster.
- *Average-case algorithms.* An algorithm that is fast and correct on a random input from some distribution, but always wrong on some fixed input, is not a BPP algorithm. The probability in the definition is over the coins of the machine, for each input.

**What is known and what is open.**

- $\mathsf{P} \subseteq \mathsf{ZPP} \subseteq \mathsf{RP} \subseteq \mathsf{BPP} \subseteq \mathsf{PP} \subseteq \mathsf{PSPACE}$. No inclusion in this chain is known to be strict.
- $\mathsf{BPP} \subseteq \Sigma_2^p \cap \Pi_2^p$ ([Sipser-Gács theorem](/sipser-gacs-theorem/)) and $\mathsf{BPP} \subseteq \mathsf{P/poly}$ ([Adleman's theorem](/adleman-theorem/)). So if $\mathsf{P} = \mathsf{NP}$, then $\mathsf{P} = \mathsf{BPP}$.
- $\mathsf{BPP} \subseteq \mathsf{BQP}$: a quantum computer can flip fair coins ([BQP](/bqp/)).
- Whether $\mathsf{BPP} \subseteq \mathsf{NP}$ is open. It is not even known whether $\mathsf{BPP} \ne \mathsf{NEXP}$.
- *Derandomization.* If some language in $\mathsf{E} = \mathsf{DTIME}(2^{O(n)})$ needs circuits of size $2^{\Omega(n)}$, then $\mathsf{P} = \mathsf{BPP}$ ([Impagliazzo-Wigderson theorem](/impagliazzo-wigderson-theorem/); see [hardness versus randomness](/hardness-versus-randomness/)). Relative to a random oracle $A$, $\mathsf{P}^A = \mathsf{BPP}^A$ with probability $1$ (Bennett and Gill 1981). The statement $\mathsf{P} = \mathsf{BPP}$ itself is a conjecture.

## Related definitions

- [RP](/rp/) and [coRP](/co-rp/) allow error on one side only. [ZPP](/zpp/) allows no error and bounds the expected time. These are the classes of [one-sided error](/one-sided-error/) and [Las Vegas](/las-vegas-algorithm/) algorithms, and BPP is the class of [Monte Carlo algorithms](/monte-carlo-algorithm/) with two-sided error.
- [PP](/pp/) has the same form with no gap: acceptance probability above $1/2$ on yes-instances and at most $1/2$ on no-instances.
- [BQP](/bqp/) is the quantum analogue, with quantum circuits in place of coins.
- [BPL](/randomized-logspace/) is the logarithmic-space analogue, and [MA](/merlin-arthur/) adds a proof from a prover to a BPP verifier.
- $\mathsf{BPP} \subseteq$ [P/poly](/p-poly/): a fixed good coin sequence for each input length is non-uniform advice.

## References
