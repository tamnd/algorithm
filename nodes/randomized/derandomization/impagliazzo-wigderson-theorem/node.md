---
tag: ZFYVT8
kind: theorem
slug: impagliazzo-wigderson-theorem
name: Impagliazzo-Wigderson theorem
aliases:
- BPP = P under exponential hardness
area: randomized/derandomization
level: research
summary: If some problem in E needs circuits of size 2^(Ω(n)), then BPP = P. Worst-case hardness is amplified to average-case hardness and fed to the Nisan-Wigderson generator.
prereqs: [nisan-wigderson-generator, hardness-versus-randomness, bpp, circuit-complexity]
see_also: [hardness-versus-randomness, nisan-wigderson-generator, reed-muller-code, locally-decodable-codes, list-decoding, expander-walk-sampler, exptime, p-poly]
sources:
  - paper: doi:10.1145/258533.258590
    title: Russell Impagliazzo and Avi Wigderson, P = BPP if E requires exponential circuits, derandomizing the XOR lemma, 29th ACM Symposium on Theory of Computing (STOC), 1997
    locator: the main theorem and the derandomized XOR lemma
  - paper: doi:10.1016/S0022-0000(05)80043-1
    title: Noam Nisan and Avi Wigderson, Hardness vs randomness, Journal of Computer and System Sciences 49(2), 1994
    locator: the generator from an average-case hard function and the design lemma
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 19 (hardness amplification, the XOR lemma, Impagliazzo's hard-core lemma and local list decoding) and Chapter 20 (derandomization from worst-case hardness)
  - paper: doi:10.1561/0400000010
    title: Salil P. Vadhan, Pseudorandomness, Foundations and Trends in Theoretical Computer Science 7(1 to 3), 2012
    locator: Chapter 7 (from worst-case hardness to pseudorandom generators through locally list-decodable codes)
---

The Impagliazzo-Wigderson theorem says that [BPP](/bpp/) $=$ P if some problem solvable in time $2^{O(n)}$ needs Boolean circuits of size $2^{\Omega(n)}$. The hypothesis is about worst-case hardness: the circuits only have to fail on one input of each length. The proof amplifies this to average-case hardness, where every small circuit fails on almost half of the inputs, and then uses the [Nisan-Wigderson generator](/nisan-wigderson-generator/). The theorem is an implication with no unproved step. Its hypothesis is open: the best known lower bounds for explicit functions are linear.

## Statement

$\mathrm{E} = \bigcup_{c} \mathrm{DTIME}(2^{cn})$. For a function $f : \{0,1\}^* \to \{0,1\}$, $f_n$ is its restriction to inputs of length $n$. Circuits have gates AND and OR of fan-in 2 and NOT gates.

**Theorem (Impagliazzo and Wigderson 1997).** Suppose there are a function $f \in \mathrm{E}$ and a constant $\delta > 0$ such that for all large $n$, every circuit that computes $f_n$ on all inputs has size at least $2^{\delta n}$. Then BPP $=$ P.

More precisely, under the same hypothesis there are a constant $c$ and, for every $m$, a generator $G_m : \{0,1\}^{c \log m} \to \{0,1\}^m$ computable in time $\mathrm{poly}(m)$ such that every circuit $D$ of size at most $m$ has $|\Pr[D(G_m(U)) = 1] - \Pr[D(U_m) = 1]| \le \frac1{10}$. The same generator gives promise-BPP $=$ P.

## In plain words

Suppose some problem can be solved in exponential time but needs very large circuits, even to get every input right. The theorem says that then every fast randomized algorithm can be turned into a fast deterministic one.

The proof first makes the hard problem harder in a useful way. It builds a related problem that every small circuit gets wrong on almost half of the inputs, so its answers look like coin flips. Then it computes those answers on many overlapping slices of a short seed. The result looks random to every small circuit. A deterministic algorithm tries every seed, which costs only polynomial time, and takes the majority vote.

## Proof

The proof has two parts: a chain of hardness amplification, which is cited, and the use of the generator, which is proved here.

**Part 1: from worst-case hardness to a generator (outline, cited).** Say that $g$ on $n$ bits is $(s, \rho)$-hard on average if every circuit of size $s$ agrees with $g$ on less than a fraction $1 - \rho$ of the inputs. The chain keeps the functions in E and the input length $O(n)$, so the exponent of the circuit size changes only by a constant factor.

1. *Worst case to mild average case.* Encode the truth table of $f_n$ as a polynomial of low degree in a few variables over a field of size $\mathrm{poly}(n)$: the low-degree extension, a [Reed-Muller](/reed-muller-code/) encoding. A polynomial of low degree is self-correctable: from a circuit that is right on a fraction $1 - 1/\mathrm{poly}(n)$ of points, a slightly larger randomized circuit computes it everywhere, and fixing its random bits gives a circuit. So the binary form $f'$ of the extension is $(2^{\delta' n}, 1/\mathrm{poly}(n))$-hard on average. This step is due to Babai, Fortnow, Nisan and Wigderson (1993).
2. *Mild to constant hardness.* Impagliazzo's hard-core lemma (1995) shows that a function that is $\rho$-hard on average has a set of density about $\rho$ on which it is nearly unpredictable. Taking $f'$ on many inputs chosen by a short random walk on an [expander graph](/expander-walk-sampler/) hits that set with high probability, while the input length stays $O(n)$.
3. *Constant hardness to advantage $2^{-\Omega(n)}$.* Yao's XOR lemma says that the XOR of $f$ on $k$ independent inputs is hard with advantage about $(1 - 2\rho)^k$, but $k$ independent inputs make the input length $kn$. Impagliazzo and Wigderson *derandomize the XOR lemma*: they choose the $k$ inputs by combining an expander walk with a [Nisan-Wigderson design](/nisan-wigderson-generator/), so the input length stays $O(n)$ and the advantage still drops to $2^{-\Omega(n)}$.
4. *The generator.* The result is $g \in \mathrm{E}$ on $\ell = O(n)$ bits that is $(2^{\gamma\ell}, 2^{-\gamma\ell})$-hard on average in the sense of the NW theorem, for a constant $\gamma > 0$. With designs of $m = 2^{\Theta(\gamma\ell)}$ sets in a ground set of size $d = O(\ell)$, the Nisan-Wigderson theorem gives a generator from $d = O(\log m)$ bits to $m$ bits that fools circuits of size $m$ with error $\frac1{10}$ and runs in time $m \cdot 2^{O(\ell)} = \mathrm{poly}(m)$.

Sudan, Trevisan and Vadhan (2001) replaced steps 1 to 3 by one step: the truth table of $f_n$ is encoded with a code that has a local list-decoding algorithm, a Reed-Muller code concatenated with a [Hadamard code](/hadamard-code/). A circuit that agrees with the encoding on a fraction $\frac12 + \varepsilon$ of positions gives, with a small amount of advice, a circuit for $f_n$ on every input.

**Part 2: from the generator to BPP $=$ P.** Let $L \in$ BPP be decided by a probabilistic algorithm $A$ that runs in time $T(n) = n^{c'}$, uses at most $T(n)$ random bits, and errs with probability at most $\frac13$ on every input.

Fix an input $x$ of length $n$. The function $r \mapsto A(x, r)$ on $T(n)$ bits is computed by a circuit $D_x$ of size at most $m = O(T(n)^2)$; the circuit has $x$ built in. Pad the random string so that $D_x$ reads $m$ bits and uses the first $T(n)$. The generator $G_m$ fools $D_x$:

$$\big|\Pr_s[D_x(G_m(s)) = 1] - \Pr_r[D_x(r) = 1]\big| \le \frac1{10}.$$

If $x \in L$, then $\Pr_r[D_x(r) = 1] \ge \frac23$, so $\Pr_s[D_x(G_m(s)) = 1] \ge \frac23 - \frac1{10} > \frac12$. If $x \notin L$, the same bound gives $\Pr_s[D_x(G_m(s)) = 1] \le \frac13 + \frac1{10} < \frac12$.

The deterministic algorithm computes $G_m(s)$ for each of the $2^{c \log m} = m^c$ seeds, runs $A(x, G_m(s))$, and accepts if more than half of the runs accept. By the two bounds, it decides $L$ correctly. Its time is $m^c \cdot (\mathrm{poly}(m) + T(n))$, a polynomial in $n$. So $L \in$ P. Since $L$ was any language in BPP, BPP $=$ P. $\blacksquare$

The argument of Part 2 does not use that the error of $A$ is the same on all inputs, only that it is bounded away from $\frac12$ on each input that satisfies the promise. So it also gives promise-BPP $=$ P.

## Consequences

- **BPP $=$ P under a natural hypothesis.** Most researchers believe the hypothesis, so they believe BPP $=$ P.
- **Polynomial identity testing.** [Polynomial identity testing](/polynomial-identity-testing/) would be in P, and so would every other problem now solved by a randomized polynomial-time algorithm.
- **Equivalence for generators.** By the claim on [hardness versus randomness](/hardness-versus-randomness/), a generator with seed $O(\log m)$ that fools circuits of size $m$ and runs in time $\mathrm{poly}(m)$ gives a function in E with circuit complexity $2^{\Omega(n)}$. So the hypothesis of the theorem and the existence of such a generator are equivalent.
- **Arthur-Merlin games.** The same chain with circuits that have an NP oracle gives [AM](/arthur-merlin/) $=$ NP under a hardness hypothesis for nondeterministic circuits (Klivans and van Melkebeek; Miltersen and Vinodchandran).

## Tightness

- **The hypothesis is equivalent to the generator.** See the consequences above: the theorem cannot be improved to a generator with seed $O(\log m)$ from a weaker hypothesis.
- **Weaker hardness gives weaker results.** With hardness $s(n)$ instead of $2^{\Omega(n)}$, the same method gives generators with seed about $n$ for circuits of size about $s(n)^{\Omega(1)}$. For example, if E needs circuits of superpolynomial size, BPP is in subexponential time for infinitely many input lengths (Babai, Fortnow, Nisan and Wigderson 1993). Umans (2003) gave generators that turn hardness $s(n)$ into $s(n)^{\Omega(1)}$ output bits with a seed of $O(n)$ bits, which is optimal up to the constant in the exponent.
- **BPP $=$ P alone is weaker.** It is not known whether BPP $=$ P implies the hypothesis. By Kabanets and Impagliazzo (2004), it implies a weaker circuit lower bound: NEXP is not in P/poly, or the permanent has no arithmetic circuits of polynomial size.
- **What is known.** The best lower bounds for explicit functions in E against general circuits are only a little above $3n$ gates. The hypothesis asks for $2^{\Omega(n)}$.

## History

Nisan and Wigderson (1988, journal 1994) obtained BPP $=$ P from average-case hardness. Babai, Fortnow, Nisan and Wigderson (1993) used random self-reducibility to start from worst-case hardness, at the cost of weaker conclusions. Impagliazzo (1995) proved the hard-core lemma. Impagliazzo and Wigderson (1997) derandomized Yao's XOR lemma and reached BPP $=$ P from worst-case exponential hardness. Sudan, Trevisan and Vadhan (2001) gave a direct proof by local list decoding, and Impagliazzo and Wigderson (1998) gave a uniform version under the assumption BPP $\ne$ EXP.

## References
