---
tag: M2RDRT
kind: theorem
slug: factoring-in-bqp
name: Factoring is in BQP
aliases:
- Shor's theorem
area: quantum/quantum-number-theory
level: advanced
summary: Integer factorization is solvable in polynomial time with bounded error on a quantum computer. The decision version is in BQP, and the full factorization is found in expected polynomial time.
prereqs: [bqp, shor-algorithm, factoring-to-order-finding, aks-primality-test, markov-inequality, solovay-kitaev-theorem]
see_also: [integer-factorization, discrete-logarithm-in-bqp, bpp, order-finding, quantum-circuit-model, quantum-threshold-theorem, rsa-cryptosystem, regev-factoring-algorithm]
sources:
  - paper: doi:10.1137/S0097539795293172
    title: "Peter W. Shor, Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer, SIAM Journal on Computing 26(5):1484-1509, 1997"
    locator: the main theorem on factoring and the section on factoring
  - paper: doi:10.1137/S0097539796300921
    title: "Ethan Bernstein and Umesh Vazirani, Quantum complexity theory, SIAM Journal on Computing 26(5):1411-1473, 1997"
    locator: the definition of BQP and its robustness to the choice of gates
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 4.5 (universal gate sets and the error of approximate gates), Section 4.4 (the principle of deferred measurement), Section 5.3 (order finding and factoring)
  - paper: doi:10.4007/annals.2004.160.781
    title: "Manindra Agrawal, Neeraj Kayal and Nitin Saxena, PRIMES is in P, Annals of Mathematics 160(2):781-793, 2004"
    locator: the deterministic polynomial-time primality test
  - paper: arxiv:quant-ph/0505030
    title: Christopher M. Dawson and Michael A. Nielsen, The Solovay-Kitaev algorithm, Quantum Information and Computation 6(1), 2006
    locator: approximating each gate to error e with O(log^c(1/e)) gates from a finite universal set
  - paper: doi:10.1109/SFCS.2000.892140
    title: "Richard Cleve and John Watrous, Fast parallel circuits for the quantum Fourier transform, Proceedings of the 41st Annual Symposium on Foundations of Computer Science (FOCS), IEEE, 2000, pp. 526-536"
    locator: approximate QFT circuits of logarithmic depth
---

This theorem says that a quantum computer can factor integers in polynomial time with bounded error. Formally, the decision version of [integer factorization](/integer-factorization/) is in [BQP](/bqp/), and the full prime factorization of $N$ can be computed with $\mathrm{poly}(\log N)$ quantum gates. It follows from [Shor's algorithm](/shor-algorithm/), and it is the main evidence that quantum computers can solve some problems far faster than classical ones.

## Statement

Let $n = \lceil \log_2 N \rceil$. The decision problem is

$$\mathrm{FACTOR} = \{(N, k) : N \text{ has a factor } f \text{ with } 1 < f \le k\}.$$

**Theorem (Shor).**

1. $\mathrm{FACTOR} \in \mathrm{BQP}$.
2. There is a uniform family of quantum circuits of size polynomial in $n$, with gates from a fixed finite [universal gate set](/universal-gate-set/), that outputs the prime factorization of $N$ with probability at least $2/3$ and otherwise outputs "fail".

A binary search over $k$ with the decision version also finds the factors, but part 2 gives them directly. With the gates of the [quantum circuit model](/quantum-circuit-model/) and schoolbook arithmetic, the expected gate count of part 2 is $O(n^4 \log n)$; this follows from the proof and is not optimized.

## In plain words

A problem is in BQP if a quantum computer can solve it in a time that grows like a polynomial in the length of the input, while being wrong at most a third of the time. The wrong answers can be made as rare as you like by running it a few times and taking the majority.

Shor's algorithm splits a number into two parts with good probability, and it checks its own answer. Splitting again and again, and checking each part for being prime, gives all the prime factors. If the process takes too long, we stop and give up, which happens only rarely. That turns the method into a fixed quantum circuit of polynomial size, so factoring is in BQP.

## Proof

**Step 1: a Las Vegas factoring procedure.** Let FULL$(N)$ do this: if $N = 1$, return nothing; if $N$ is prime, by the deterministic [AKS test](/aks-primality-test/), return $N$; otherwise let $f$ = SHOR$(N)$ and return FULL$(f)$ together with FULL$(N/f)$. Each output is a prime and the product of the outputs is $N$, so whenever FULL stops its answer is right. The recursion tree has fewer than $\log_2 N + 1$ leaves, so SHOR is called fewer than $n$ times, each time on a number at most $N$.

**Step 2: its expected cost.** By the analysis of [Shor's algorithm](/shor-algorithm/) and the bound on good bases in [factoring to order finding](/factoring-to-order-finding/), one call of SHOR on a number below $N$ makes an expected $O(1)$ choices of the base $a$ and an expected $O(\log n)$ runs of the order-finding circuit per base. Each run has $O(n^3)$ gates and is followed by $\mathrm{poly}(n)$ classical work. So the expected total cost $T$ of FULL$(N)$ in gates and classical steps is at most $\mathrm{poly}(n)$; with schoolbook arithmetic it is $O(n^4 \log n)$.

**Step 3: cut it off.** Run FULL with a budget of $6\,\mathbb{E}[T]$ steps and output "fail" if the budget runs out. By [Markov's inequality](/markov-inequality/), the budget runs out with probability at most $1/6$. If it does not, the output is the correct factorization. To decide $(N, k)$, accept if the least prime factor is at most $k$ and reject on "fail". The error is at most $1/6$, and only on yes-instances.

**Step 4: one circuit per input length.** The cut-off procedure is a classical polynomial-time machine that takes random bits and calls quantum circuits with measurements. Each random bit is a Hadamard gate followed by a measurement. The classical steps become reversible circuits of [Toffoli gates](/toffoli-gate/) on fresh [ancillas](/ancilla-qubits/), with only a polynomial overhead; see [reversible computation](/reversible-computation/). All measurements but the final one can be moved to the end, with classically controlled gates replaced by quantum controlled gates (the principle of deferred measurement). The result is a single quantum circuit $C_n$ of size $G = \mathrm{poly}(n)$, and a classical machine builds $C_n$ from $n$ in polynomial time.

**Step 5: a finite gate set.** $C_n$ uses controlled rotations by angles $2\pi/2^j$. By the [Solovay-Kitaev theorem](/solovay-kitaev-theorem/), each gate can be replaced by $O(\log^c(G/\delta))$ gates from a fixed finite universal set with operator-norm error at most $\delta/(2G)$. The errors of a product of unitaries add, so the final state moves by at most $\delta/2$ in norm, and each output probability by at most $\delta$. With $\delta = 1/6$ the total error stays at most $1/6 + 1/6 = 1/3$, and the circuit size is still polynomial. This proves both parts. $\blacksquare$

## Consequences

- **Cryptography.** [RSA](/rsa-cryptosystem/) and the other schemes whose security rests on factoring are broken by a large enough quantum computer. The discrete-logarithm analog, [discrete logarithms in BQP](/discrete-logarithm-in-bqp/), breaks Diffie-Hellman and elliptic-curve systems.
- **Evidence that BQP is larger than BPP.** Factoring is not known to be in [BPP](/bpp/), and decades of work have found no classical polynomial-time method. So the theorem is strong evidence, though not a proof, that quantum computers are more powerful than classical randomized ones. It is the main challenge to the strong form of the Church-Turing thesis, which says that every reasonable model can be simulated by a probabilistic Turing machine with polynomial overhead.
- **No consequence for NP.** FACTOR is in [NP](/np/) and in [co-NP](/co-np/): the prime factorization is a certificate for both answers, and AKS checks the primes. If FACTOR were NP-complete, NP would equal co-NP. So the theorem gives no reason to think that NP is in BQP.
- **Related problems.** [Order finding](/order-finding/), computing $\varphi(N)$ and $\lambda(N)$, and finding square roots modulo $N$ are all in the function class of BQP by the same argument.

## Tightness

- **Classical side.** No classical polynomial-time algorithm is known. The best classical method, the [general number field sieve](/general-number-field-sieve/), runs in heuristic time $\exp(O(n^{1/3} (\log n)^{2/3}))$. It is open whether FACTOR is in BPP, so the theorem is not known to give a separation.
- **Gate count.** The bound of the proof is loose. Fast multiplication gives about $O(n^2 \log n \log\log n)$ gates per run, and [Regev's algorithm](/regev-factoring-algorithm/) uses about $n^{3/2}$ gates per run with about $\sqrt{n}$ runs, but its analysis relies on a number-theoretic conjecture, so it does not replace the unconditional theorem.
- **Depth.** Cleve and Watrous gave approximate QFT circuits of depth $O(\log n)$, so the depth of order finding is set by the modular exponentiation.
- **Noise.** The proof assumes perfect gates. With noise below a constant threshold, the [threshold theorem](/quantum-threshold-theorem/) keeps the result with a polylogarithmic overhead; the practical cost is in [quantum resource estimation for factoring](/quantum-resource-estimation-factoring/).

## History

Bernstein and Vazirani defined BQP in 1993, in the journal version of 1997. Shor proved the theorem in 1994, with the journal version in 1997, and it changed the view of quantum computing from a curiosity to a threat to public-key cryptography. When Shor wrote, primality was known to be in ZPP; the AKS test of 2002 later made the primality steps of the proof deterministic.

## References
