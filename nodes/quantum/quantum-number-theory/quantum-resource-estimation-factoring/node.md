---
tag: PB6TT3
kind: concept
slug: quantum-resource-estimation-factoring
name: Quantum resource estimation for factoring
aliases:
- cost of factoring RSA-2048 on a quantum computer
area: quantum/quantum-number-theory
level: advanced
summary: Estimates of the logical qubits, Toffoli gates, physical qubits and run time needed to factor RSA-sized numbers with Shor's algorithm, and the assumptions behind them.
prereqs: [shor-algorithm, quantum-modular-exponentiation, quantum-error-correction, quantum-threshold-theorem, toffoli-gate]
see_also: [ekera-hastad-algorithm, regev-factoring-algorithm, quantum-elliptic-curve-discrete-log, rsa-cryptosystem, post-quantum-cryptography, phase-and-t-gates, general-number-field-sieve, factoring-in-bqp]
sources:
  - paper: doi:10.22331/q-2021-04-15-433
    title: "Craig Gidney and Martin Ekerå, How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits, Quantum 5:433, 2021"
    locator: Table 1 (abstract qubit and Toffoli+T/2 counts of earlier constructions) and Table 2 (earlier physical estimates for n = 2048)
  - paper: arxiv:2505.15917
    title: Craig Gidney, How to factor 2048 bit RSA integers with less than a million noisy qubits, 2025
    locator: the abstract, Sections 3.1 and 3.2, and Tables 4 and 5 (assumptions and costs)
  - paper: doi:10.1103/PhysRevA.86.032324
    title: "Austin G. Fowler, Matteo Mariantoni, John M. Martinis and Andrew N. Cleland, Surface codes: Towards practical large-scale quantum computation, Physical Review A 86:032324, 2012"
    locator: the sections on logical error rates and on the cost of Shor's algorithm
  - paper: arxiv:1702.00249
    title: "Martin Ekerå and Johan Håstad, Quantum algorithms for computing short discrete logarithms and factoring RSA integers, PQCrypto 2017, LNCS 10346, pages 347-363"
    locator: the abstract (exponent of slightly more than n/2 bits against 2n bits for Shor)
  - url: https://eprint.iacr.org/2024/222
    title: Clémence Chevignard, Pierre-Alain Fouque and André Schrottenloher, Reducing the number of qubits in quantum factoring, IACR ePrint 2024/222, revised version at CRYPTO 2025
    locator: the abstract (n/2 + o(n) qubits)
  - paper: arxiv:1706.06752
    title: Martin Roetteler, Michael Naehrig, Krysta M. Svore and Kristin Lauter, Quantum resource estimates for computing elliptic curve discrete logarithms, ASIACRYPT 2017
    locator: the abstract (qubit and Toffoli bounds for an n-bit prime field)
  - paper: doi:10.1103/PhysRevA.54.1034
    title: "David Beckman, Amalavoyal N. Chari, Srikrishna Devabhaktuni and John Preskill, Efficient networks for quantum factoring, Physical Review A 54:1034, 1996"
    locator: the operation and qubit counts for modular exponentiation
---

Quantum resource estimation for factoring is the work of counting what a quantum computer needs to run [Shor's algorithm](/shor-algorithm/) on a modulus of a given size, usually a 2048-bit [RSA](/rsa-cryptosystem/) modulus. An estimate gives logical counts, such as logical qubits and [Toffoli gates](/toffoli-gate/), and physical counts, such as noisy qubits and wall-clock time, under stated hardware assumptions. The best published estimate for RSA-2048 fell from billions of physical qubits in 2009 to under one million in 2025, mostly through better arithmetic and better error correction.

## In plain words

Knowing that a quantum computer can factor fast is not the same as knowing how big the computer must be. To answer that, people write out the full circuit, count its parts, and then ask how much extra hardware is needed to protect each part from noise.

There are two kinds of count. The first kind is for a perfect machine: how many qubits and how many expensive gates. The second kind is for a real machine whose parts make small errors. Each protected qubit is built from hundreds of noisy ones, and each expensive gate needs a special state made in a small factory on the chip.

The second count depends on how good and how fast the hardware is. So a number such as "one million qubits" means little without its assumptions. Smarter circuits and protection have cut the estimates a thousandfold.

## The idea

**Layers of an estimate.** An estimate passes through four layers, and each layer has its own model.

1. *The algorithm.* Which variant of factoring runs: plain Shor with a $2n$-bit exponent, the [Ekerå-Håstad algorithm](/ekera-hastad-algorithm/) with an exponent of slightly more than $n/2$ bits, or another variant. The variant fixes how many modular multiplications the circuit does.
2. *The logical circuit.* In the [quantum circuit model](/quantum-circuit-model/) with perfect gates, count the logical qubits, the Toffoli gates (or the [T gates](/phase-and-t-gates/)) and the depth. Data qubits and [ancillas](/ancilla-qubits/) are often counted apart. The count depends on the multiplication method and the adder, as on the [quantum modular exponentiation](/quantum-modular-exponentiation/) page.
3. *Error correction.* Pick a [quantum error-correcting code](/quantum-error-correction/), almost always the surface code, and a code distance $d$ that keeps the total failure probability small. Add the factories that make the magic states for the non-Clifford gates, and the space for routing.
4. *The hardware.* Assume a physical error rate $p$, a surface-code cycle time, a reaction time (the delay from a measurement to a gate that depends on it), and a connectivity, such as a planar grid of nearest neighbors. Only this layer turns gate counts into seconds.

The physical figures include all the overhead of layers 3 and 4. The logical figures include none of it. A comparison is fair only within one layer and under the same assumptions.

**Why the Toffoli count leads.** In the surface code, Clifford gates such as CNOT are cheap: they are done by code deformation or lattice surgery. A non-Clifford gate, such as T or Toffoli, needs a magic state that must be distilled or otherwise prepared at high fidelity, which takes much more space and time. So the run time is roughly the Toffoli count divided by the rate at which the factories produce Toffoli states, unless the reaction time limits the chain of dependent measurements first. This is why the modular-exponentiation literature reports "Toffoli count" or "Toffoli + T/2 count" and not the total gate count.

**Choosing the code distance.** Below the threshold of the [threshold theorem](/quantum-threshold-theorem/), the logical error rate of one surface-code patch per cycle falls roughly as $(p/p_{\mathrm{th}})^{(d+1)/2}$, where $p_{\mathrm{th}}$ is the threshold. The estimate needs (number of patches) times (number of cycles) times (logical error rate) to stay well below 1. Since the factor drops exponentially in $d$, $d$ grows only like the logarithm of the circuit size, which is the source of the polylogarithmic overhead in the theorem. A patch of distance $d$ uses about $2d^2$ physical qubits.

**The levers.** Each big drop in the estimates came from one of a few places.

- *Fewer multiplications.* A shorter exponent (Ekerå and Håstad) and windowed arithmetic, which handles several exponent bits with one table lookup.
- *Cheaper multiplications.* Schoolbook multiplication with fast adders, the coset representation of modular integers, which removes most modular reductions, and carry runways, which cut the depth of long additions.
- *Fewer qubits.* Approximate residue arithmetic computes the output of the modular exponentiation in pieces. Chevignard, Fouque and Schrottenloher show that $n/2 + o(n)$ logical qubits suffice for an $n$-bit RSA modulus.
- *Cheaper error correction.* Better factories, yoked surface codes, which store idle qubits more densely, and magic state cultivation, which grows a T state inside one patch.

The levers trade against each other. Fewer qubits usually means fewer factories, and so a longer run.

## Examples

**Earlier physical estimates for RSA-2048.** Gidney and Ekerå (Table 2) list these estimates. Each one uses its own hardware assumptions, so the rows show the trend and are not strictly comparable.

| Estimate | Physical qubits | Expected run time |
|---|---|---|
| Van Meter et al. 2009 | 6500 million | 410 days |
| Jones et al. 2010 | 620 million | 10 days |
| Fowler et al. 2012 | 1000 million | 1.1 days |
| O'Gorman and Campbell 2017 | 230 million | 3.7 days |
| Gheorghiu and Mosca 2019 | 170 million | 1 day |

The two estimates below continue the table.

**Abstract counts of modular exponentiation.** Gidney and Ekerå (Table 1) also compare logical constructions by abstract qubits and by the Toffoli + T/2 count, for an $n$-bit modulus.

| Construction | Abstract qubits | Toffoli + T/2 count |
|---|---|---|
| Vedral, Barenco and Ekert 1996 | $7n + 1$ | $80 n^3$ |
| Zalka 2006, basic | $3n$ | $12 n^3$ |
| Beauregard 2003 | $2n + 3$ | |
| Fowler et al. 2012 | $3n$ | $40 n^3$ |
| Häner, Roetteler and Svore 2016 | $2n + 2$ | $64 n^3 \lg n$ |
| Gidney and Ekerå 2021 | $3n + 0.002 n \lg n$ | $0.3 n^3 + 0.0005 n^3 \lg n$ |

At $n = 2048$, $40 n^3 \approx 3.4 \times 10^{11}$, while $0.3 n^3 + 0.0005 n^3 \lg n \approx 2.6 \times 10^9$: the arithmetic alone became more than 100 times cheaper. The circuit on the quantum modular exponentiation page uses at least $t(20n^2 + 21n)$ Toffolis, which at $t = 2n = 4096$ is about $3.44 \times 10^{11}$, the same leading term as the Fowler row.

**From logical to physical: Gidney and Ekerå 2021.** The assumptions are a planar grid of nearest-neighbor qubits, a physical gate error rate of 0.1%, a surface-code cycle of 1 microsecond and a reaction time of 10 microseconds. The formula $3n + 0.002 n \lg n$ gives about 6,190 logical qubits at $n = 2048$. One of the code distances in the layout is $d = 27$, and a patch then needs about $2 \cdot 27^2 = 1458$ physical qubits. So the logical qubits alone take about $6190 \cdot 1458 \approx 9.0$ million physical qubits. The layout also needs routing space and 28 CCZ factories, which bring the total to about 20 million, and the run makes about 3 billion CCZ states in about 8 hours.

**Gidney 2025.** Under the same error rate, cycle time and reaction time, on a square grid, the estimate is fewer than one million noisy qubits and an expected run of under a week. The circuit uses fewer than 1,600 logical qubits and about $6.5 \times 10^9$ Toffoli gates, with code distance 25. It combines approximate residue arithmetic, yoked surface codes and magic state cultivation. Compared with 2021 it has about 20 times fewer physical qubits but more Toffolis and a longer run: about $6.5 \times 10^9$ Toffolis in about 5 days is roughly 15,000 Toffolis per second. This is the trade between qubits and time from the list of levers.

**Elliptic curves for comparison.** Roetteler, Naehrig, Svore and Lauter bound the cost of the [elliptic curve discrete logarithm](/quantum-elliptic-curve-discrete-log/) over an $n$-bit prime field by $9n + 2\lceil \log_2 n \rceil + 10$ logical qubits and $448 n^3 \log_2 n + 4090 n^3$ Toffoli gates. At $n = 256$ this is 2330 logical qubits, far fewer than RSA at a similar classical security level needs, which makes elliptic-curve keys an easier target in qubits.

## Where it is used

- **Cryptographic planning.** Estimates are the evidence for timelines to move from RSA and elliptic-curve keys to [post-quantum cryptography](/post-quantum-cryptography/). Data encrypted today can be stored and decrypted later ([harvest now, decrypt later](/harvest-now-decrypt-later/)), so the time to migrate counts against the time to a large quantum computer.
- **Choosing key sizes.** The quantum cost of solving the [RSA problem](/rsa-problem/) by factoring grows only polynomially with $n$, so larger RSA keys do not give long-term safety against quantum attack, unlike the case of the classical [general number field sieve](/general-number-field-sieve/). Post-quantum schemes are instead rated by [NIST security levels](/nist-security-levels/).
- **Hardware targets.** The assumptions of an estimate (error rate, cycle time, connectivity) give hardware groups a concrete target, and the sensitivity of the estimate to each assumption shows which improvement matters most.
- **Comparing algorithms.** New variants, such as the [Regev factoring algorithm](/regev-factoring-algorithm/), are judged by their resource counts and not only by their asymptotic gate count. A variant that uses fewer gates per run but more qubits or more runs can cost more in practice.
- **Judging demonstrations.** Small experiments, such as the compiled factoring of 15, use only a few qubits and say little about these costs; see [Shor's algorithm](/shor-algorithm/).

## References
