---
tag: SAF228
kind: theorem
slug: discrete-logarithm-in-bqp
name: Discrete logarithm is in BQP
area: quantum/quantum-number-theory
level: advanced
summary: Discrete logarithms in Z_p^* are computable in quantum polynomial time with bounded error, so the decision version is in BQP. The proof also covers elliptic curves and other groups.
prereqs: [bqp, quantum-discrete-logarithm, discrete-logarithm-problem, factoring-in-bqp, multiplicative-order, markov-inequality, solovay-kitaev-theorem]
see_also: [factoring-in-bqp, quantum-elliptic-curve-discrete-log, shoup-generic-lower-bound, generic-group-model, finite-field-discrete-logarithm-problem, diffie-hellman, order-finding, quantum-threshold-theorem]
sources:
  - paper: doi:10.1137/S0097539795293172
    title: "Peter W. Shor, Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer, SIAM Journal on Computing 26(5):1484-1509, 1997"
    locator: Section 6, the discrete logarithm algorithm and its probability bound
  - paper: doi:10.1137/S0097539796300921
    title: "Ethan Bernstein and Umesh Vazirani, Quantum complexity theory, SIAM Journal on Computing 26(5):1411-1473, 1997"
    locator: the definition of BQP and its robustness to the choice of gates
  - paper: doi:10.1007/3-540-44750-4_34
    title: "Dan Boneh and Richard J. Lipton, Quantum cryptanalysis of hidden linear functions, Advances in Cryptology (CRYPTO 1995), LNCS 963, Springer, pp. 424-437"
    locator: the extension to hidden linear functions over groups whose order is not known
  - paper: doi:10.1007/3-540-69053-0_18
    title: "Victor Shoup, Lower bounds for discrete logarithms and related problems, Advances in Cryptology (EUROCRYPT 1997), LNCS 1233, Springer, pp. 256-266"
    locator: the lower bound of order sqrt(s) group operations for generic classical algorithms, where s is the largest prime factor of the group order
  - url: https://www.cs.umd.edu/~amchilds/qa/qa.pdf
    title: Andrew M. Childs, Lecture Notes on Quantum Algorithms, University of Maryland, version of 17 April 2025
    locator: Section 4.4 (the Fourier transform of Z_N by phase estimation) and Chapter 5 (discrete log)
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 4.4 (deferred measurement), Section 4.5 (approximation of gates) and Section 5.4.2 (discrete logarithms)
  - paper: arxiv:quant-ph/0505030
    title: Christopher M. Dawson and Michael A. Nielsen, The Solovay-Kitaev algorithm, Quantum Information and Computation 6(1), 2006
    locator: approximating each gate to error e with O(log^c(1/e)) gates from a finite universal set
---

This theorem says that a quantum computer computes discrete logarithms in polynomial time with bounded error. Formally, the decision version of the [discrete logarithm problem](/discrete-logarithm-problem/) in $\mathbb{Z}_p^*$ is in [BQP](/bqp/), and $\log_g h$ itself can be computed with $\mathrm{poly}(\log p)$ quantum gates. It follows from [Shor's discrete logarithm algorithm](/quantum-discrete-logarithm/), and the same proof covers elliptic curves and any cyclic group with efficient, uniquely encoded group operations.

## Statement

Let $n = \lceil \log_2 p \rceil$. The decision problem is

$$\mathrm{DLOG} = \{(p, g, h, k) : p \text{ is prime},\ g, h \in \mathbb{Z}_p^*, \text{ and } g^x \equiv h \pmod p \text{ for some } 0 \le x \le k\}.$$

**Theorem (Shor).**

1. $\mathrm{DLOG} \in \mathrm{BQP}$.
2. There is a uniform family of quantum circuits of size polynomial in $n$, with gates from a fixed finite [universal gate set](/universal-gate-set/), that on input $(p, g, h)$ outputs the least $x \ge 0$ with $g^x \equiv h$ if $h \in \langle g \rangle$, and "none" otherwise. It is right with probability at least $2/3$, and when it is wrong it outputs "fail".
3. The same holds for any family of cyclic groups whose elements have unique encodings of $n$ bits and whose group operation and inverse have classical circuits of size $\mathrm{poly}(n)$, provided the group order $r$ is given or can be computed in quantum polynomial time. This includes the groups $E(\mathbb{F}_q)$ of [elliptic curves](/elliptic-curve-discrete-logarithm-problem/).

## In plain words

A problem is in BQP when a quantum computer solves it in polynomial time and is wrong at most a third of the time. Repeating the run and taking the majority makes errors as rare as you like.

Shor's method finds a discrete logarithm after a few runs on average, and it checks each answer, so it never returns a wrong one. Before it starts, it needs the size of the group that the base number generates. Factoring finds that size, and factoring is also fast on a quantum computer. If the whole process takes much longer than its average, we stop and report a failure, which happens only rarely. Then the steps turn into one quantum circuit of polynomial size.

## Proof

Write $r$ for the order of $g$ in $\mathbb{Z}_p^*$. All classical steps below take $\mathrm{poly}(n)$ time.

**Step 1: the order of $g$.** Factor $p - 1$ with the Las Vegas procedure in the proof of [factoring in BQP](/factoring-in-bqp/), which returns the correct prime factorization after an expected $\mathrm{poly}(n)$ gates and steps. Then set $r \leftarrow p - 1$, and for each prime $s \mid p - 1$, while $s \mid r$ and $g^{r/s} = 1$, set $r \leftarrow r/s$. At the end $g^r = 1$ and $g^{r/s} \ne 1$ for each prime $s \mid r$. The [order](/multiplicative-order/) divides every $e$ with $g^e = 1$, so it divides $r$ but no $r/s$, and so it equals $r$.

**Step 2: membership.** $\mathbb{Z}_p^*$ is cyclic, so for each $r \mid p - 1$ it has exactly one subgroup of order $r$, namely $\{y : y^r = 1\}$. So $h \in \langle g \rangle$ if and only if $h^r = 1$. If $h^r \ne 1$, output "none". The answer is then right with certainty.

**Step 3: the logarithm.** If $h^r = 1$, run QDLOG$(g, h, r)$ of [the algorithm page](/quantum-discrete-logarithm/). Each run costs $O(n^3)$ gates and $O(n^2)$ classical steps. Each answer is checked by $g^{x_\star} = h$ with $0 \le x_\star < r$, so it is the least non-negative logarithm. The expected number of runs is less than 2.775, by the theorem on the number of runs in [its correctness proof](/quantum-discrete-logarithm/). So steps 1 to 3 form a Las Vegas procedure with expected cost $\mathbb{E}[T] = \mathrm{poly}(n)$.

**Step 4: cut it off.** Run the procedure with a budget of $12\,\mathbb{E}[T]$ steps, and output "fail" if the budget runs out. By [Markov's inequality](/markov-inequality/), this happens with probability at most $1/12$. Otherwise the output is correct.

**Step 5: one circuit per input length.** The random bits become Hadamard gates and measurements. The classical steps become reversible circuits of [Toffoli gates](/toffoli-gate/) with only a polynomial overhead; see [reversible computation](/reversible-computation/). All measurements move to the end by the principle of deferred measurement. This gives one circuit $C_n$ of size $G = \mathrm{poly}(n)$, and a classical machine builds $C_n$ from $n$ in polynomial time. $C_n$ still has two kinds of gates outside a finite set: the Fourier transform $F_r$ of $\mathbb{Z}_r$ for a general $r$, and controlled rotations by arbitrary angles.

**Step 6: a finite gate set.** $F_r$ is approximated by phase estimation of the map $|y\rangle \mapsto |y + 1 \bmod r\rangle$, whose eigenvectors are the Fourier basis states. With $O(n + \log(1/\epsilon))$ bits of precision it has error at most $\epsilon$ in operator norm and $\mathrm{poly}(n, \log(1/\epsilon))$ gates. Then the [Solovay-Kitaev theorem](/solovay-kitaev-theorem/) replaces each remaining gate with $O(\log^c(1/\epsilon))$ gates from a fixed finite universal set with error at most $\epsilon$. With $\epsilon = 1/(24 G')$, where $G' = \mathrm{poly}(n)$ counts all the approximated gates, the errors of the unitaries add to at most $1/24$ in norm. Each output probability then moves by at most $2 \cdot 1/24 = 1/12$. The checks of steps 2 and 3 are classical, so every output other than "fail" is still correct, and the approximation only changes the probability of "fail". The total error is at most $1/12 + 1/12 < 1/3$, and the circuit size is still polynomial. This proves part 2.

**Part 1.** On input $(p, g, h, k)$, first test that $p$ is prime with the [AKS test](/aks-primality-test/), and reject if not. Then run the circuit of part 2 and accept if and only if it outputs some $x \le k$. A wrong answer needs the output "fail", so the error is at most $1/3$.

**Part 3.** Steps 3 to 6 use only the group law, its inverse and unique encodings, so they hold for any such family once $r$ is known. For $E(\mathbb{F}_q)$, the order $r$ of a point is found by [order finding](/order-finding/) in the group, with the same kind of circuit and a check of $rP = O$ and $(r/s)P \ne O$ after factoring the candidate. $\blacksquare$

## Consequences

- **Cryptography.** [Diffie-Hellman](/diffie-hellman/) key exchange, [DSA](/dsa/), [ECDSA](/ecdsa/) and the other schemes whose security rests on discrete logarithms in $\mathbb{Z}_p^*$ or in elliptic curve groups are broken by a large enough quantum computer. Together with [factoring in BQP](/factoring-in-bqp/), this covers almost all public-key cryptography in use before [post-quantum cryptography](/post-quantum-cryptography/).
- **An exponential separation for generic algorithms.** In the [generic group model](/generic-group-model/), [Shoup's bound](/shoup-generic-lower-bound/) says that a classical algorithm needs on the order of $\sqrt{s}$ group operations, where $s$ is the largest prime factor of $r$. The quantum algorithm uses $O(\log r)$ group operations per run, in superposition, and a constant expected number of runs. This is a proven exponential gap, but only for generic algorithms.
- **No consequence for NP.** DLOG is in [NP](/np/) and [co-NP](/co-np/). For a yes-instance the certificate is $x$. For a no-instance it is the factorization of $p - 1$ with prime certificates, which fixes $r$ as in step 1, together with either $h^r \ne 1$ or the logarithm $x$ with $k < x < r$. So DLOG is not NP-complete unless NP equals co-NP.
- **Hidden linear functions.** Boneh and Lipton extended the method to hidden linear functions, which include groups whose order is not known.

## Tightness

- **Classical side.** No classical polynomial-time algorithm is known for $\mathbb{Z}_p^*$. The [number field sieve](/number-field-sieve-discrete-logarithm/) runs in heuristic time $\exp(O(n^{1/3} (\log n)^{2/3}))$. For elliptic curves of cryptographic size, the best known classical attacks are generic and need about $\sqrt{r}$ operations. It is open whether DLOG is in [BPP](/bpp/), so the theorem gives no unconditional separation.
- **Gate count.** The bound of the proof is loose. One run costs $O(n^3)$ gates with schoolbook arithmetic, and the dominant cost of step 1 is the factoring of $p - 1$. When the factorization of $p - 1$ or the order $r$ is known, as in cryptographic groups, step 1 is free.
- **Noise.** The proof assumes perfect gates. With noise below a constant threshold, the [threshold theorem](/quantum-threshold-theorem/) keeps the result with a polylogarithmic overhead.

## History

Bernstein and Vazirani defined BQP in 1993, with the journal version in 1997. Shor gave the discrete logarithm algorithm in 1994 together with factoring, and the journal version in 1997. Boneh and Lipton (1995) generalized it to hidden linear functions, and Shoup (1997) proved the generic classical lower bound that the quantum algorithm beats.

## References
