---
tag: SATJ60
kind: theorem
slug: quantum-threshold-theorem
name: Quantum threshold theorem
aliases:
- fault-tolerance threshold theorem
area: quantum/quantum-primitives
level: research
summary: "If every gate, preparation and measurement fails with a rate below a constant threshold, under local weakly correlated noise, any quantum circuit runs reliably with polylog overhead."
prereqs: [quantum-error-correction, steane-code, universal-gate-set]
see_also: [shor-code, concatenated-codes, clifford-group, gottesman-knill-theorem, solovay-kitaev-theorem, repetition-code, binary-symmetric-channel, quantum-circuit-model]
sources:
  - paper: doi:10.1137/S0097539799359385
    title: Dorit Aharonov and Michael Ben-Or, Fault-tolerant quantum computation with constant error rate, SIAM Journal on Computing 38(4), 2008, pages 1207 to 1282; conference version in STOC 1997, pages 176 to 188, doi:10.1145/258533.258579; arXiv:quant-ph/9611025
    locator: the theorem with polylog overhead in time and space, the proper codes, the nearest-neighbour version and the threshold of about 10^-6
  - paper: doi:10.1007/978-1-4615-5923-8_19
    title: A. Yu. Kitaev, Quantum error correction with imperfect gates, in Quantum Communication, Computing, and Measurement, Plenum Press, 1997, pages 181 to 188
    locator: the whole chapter
  - paper: doi:10.1098/rspa.1998.0166
    title: Emanuel Knill, Raymond Laflamme and Wojciech H. Zurek, Resilient quantum computation, error models and thresholds, Proceedings of the Royal Society of London A 454, 1998, pages 365 to 384
    locator: the error models and the threshold for concatenated codes
  - url: https://arxiv.org/abs/quant-ph/0504218
    title: Panos Aliferis, Daniel Gottesman and John Preskill, Quantum accuracy threshold for concatenated distance-3 codes, Quantum Information and Computation 6(2), 2006, pages 97 to 165, arXiv:quant-ph/0504218
    locator: the extended rectangles, the inductive proof for distance-3 codes, the bound epsilon_0 > 2.73 x 10^-5 for adversarial independent stochastic noise, and the local non-Markovian noise model
  - paper: doi:10.1103/PhysRevA.86.032324
    title: Austin G. Fowler, Matteo Mariantoni, John M. Martinis and Andrew N. Cleland, Surface codes, towards practical large-scale quantum computation, Physical Review A 86, 2012, article 032324
    locator: the surface code threshold of about 1% under circuit noise
  - url: https://arxiv.org/abs/quant-ph/9611028
    title: Dorit Aharonov, Michael Ben-Or, Russell Impagliazzo and Noam Nisan, Limitations of noisy reversible computation, arXiv:quant-ph/9611028, 1996
    locator: the abstract, noisy quantum circuits without fresh qubits need size exponential in the depth
  - url: https://arxiv.org/abs/quant-ph/0310136
    title: Alexander A. Razborov, An upper bound on the threshold quantum decoherence rate, arXiv:quant-ph/0310136, 2003
    locator: the abstract, the threshold is at most 1/2 for gates of fan-in 2, under QP not in QNC^1
  - paper: doi:10.1038/s41586-024-08449-y
    title: Google Quantum AI and collaborators, Quantum error correction below the surface code threshold, Nature 638, 2025, starting on page 920, arXiv:2408.13687
    locator: the distance-7 surface code memory with error suppression factor 2.14 per distance step
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 10.6 (fault-tolerant quantum computation), with Section 10.6.1 for the concatenation argument
---

The *quantum threshold theorem* says that noise does not rule out large quantum computations. There is a constant $\varepsilon_{\mathrm{th}} > 0$ such that, if every gate, preparation, measurement and wait fails with probability below $\varepsilon_{\mathrm{th}}$, and the failures are local and only weakly correlated, then any ideal circuit of $m$ gates can be simulated to accuracy $\delta$ by a noisy circuit of $O(m \cdot \mathrm{polylog}(m/\delta))$ gates. The proof encodes the computation in a [quantum error-correcting code](/quantum-error-correction/), does every step on encoded data so that one fault stays one error, and concatenates the code so that the logical error rate falls doubly exponentially with the level. It was proved in 1996 and 1997 by Aharonov and Ben-Or, by Kitaev, and by Knill, Laflamme and Zurek, and it is the reason that physicists build machines with error rates below about $10^{-2}$ to $10^{-3}$.

## Statement

**The model.** A circuit is a set of *locations* in time steps: preparations of $|0\rangle$, gates from a fixed [universal gate set](/universal-gate-set/) on one or two qubits (for example $H$, $S$, CNOT and $T$), measurements in the computational basis, and wait steps of a qubit that does nothing. Operations in one step act in parallel on disjoint qubits.

**The noise.** A noisy run of the circuit has a random set $F$ of faulty locations. A faulty location may apply any quantum operation to its qubits in place of the ideal one, chosen by an adversary. The noise is *local stochastic with rate $\varepsilon$*: for every set $R$ of $r$ locations, $\Pr[R \subseteq F] \le \varepsilon^r$. This includes independent failures with probability at most $\varepsilon$ each. The other hypotheses are:

1. fresh qubits in the state $|0\rangle$ can be prepared at any step, anywhere (the entropy that errors add must leave the computer);
2. classical computation on the measurement outcomes is free of errors and instantaneous, so a correction can depend on a syndrome at once (Aharonov and Ben-Or avoid this by correcting coherently, with no measurement during the computation);
3. many operations run in parallel in every step, so that errors on idle qubits are corrected as fast as they come.

**Theorem (threshold theorem).** For the gate set and noise model above there is a constant $\varepsilon_{\mathrm{th}} > 0$ with this property. For every ideal circuit $C$ with $m$ locations and every $\delta > 0$ there is a circuit $C'$ with $m \cdot O(\log^{a}(m/\delta))$ locations and depth $\mathrm{depth}(C) \cdot O(\log^{a}(m/\delta))$, for a constant $a$, such that for every noise of rate $\varepsilon < \varepsilon_{\mathrm{th}}$ the output distribution of the noisy run of $C'$, after classical decoding, is within total variation distance $\delta$ of the output distribution of $C$.

The value of $\varepsilon_{\mathrm{th}}$ depends on the gate set, the code, the decoding circuits and the noise model; the theorem only says it is a positive constant. Rigorous lower bounds: about $10^{-6}$ (Aharonov and Ben-Or, with their codes), and $\varepsilon_{\mathrm{th}} > 2.73 \times 10^{-5}$ for concatenated distance-3 codes under adversarial independent stochastic noise (Aliferis, Gottesman and Preskill, computer-assisted). Estimates from simulations are much higher, about $1\%$ for the surface code under circuit noise (Fowler, Mariantoni, Martinis and Cleland).

## In plain words

Every part of a quantum computer makes mistakes, and the mistakes can spread. The theorem says this is not fatal if the parts are good enough. Store each qubit in a code that can fix one mistake, and build every step so that one faulty part causes at most one mistake in each code block. Then a block fails only if two parts fail close together, which is much rarer than one failure. Now treat each protected block as a new, better part and do the same again, and again. Each round squares the failure rate, measured against the threshold, so a few rounds give an extremely reliable computer. The cost grows only slowly. The catch: the parts must start below the threshold, failures must not be strongly linked across the machine, and you need a steady supply of fresh qubits.

## Proof

**Proof sketch.** The full proofs are long; this sketch follows the concatenated distance-3 version of Aliferis, Gottesman and Preskill (their extended rectangles and inductive argument) and Section 10.6 of Nielsen and Chuang. It is not a complete proof.

**Step 1: a code and fault-tolerant gadgets.** Use a code that corrects one error, such as the [Steane code](/steane-code/). For each location type build a *gadget* that acts on encoded blocks: logical $H$, $S$ and CNOT transversally (one physical gate per qubit, so one fault affects one qubit per block), logical $T$ from a prepared magic state, logical preparation and measurement, and an error-correction gadget that measures the syndrome with ancillas prepared and checked so that one fault inside it causes at most one error in the data block. The gadgets are *fault tolerant*: each one, if it has at most one fault, either outputs at most one error per block, or is followed by correction that removes it.

**Step 2: extended rectangles.** A *1-rectangle* is a gadget followed by error correction. An *extended rectangle* (1-exRec) adds the error correction before it. Call an exRec *good* if it has at most one fault. The main lemma is: a good exRec acts like the ideal gate on the encoded data, in the sense that decoding after it gives the same result as the ideal gate applied to the decoded input. The proof checks each gadget, and uses only the fault-tolerance property of Step 1. Overlapping exRecs share their leading correction; the lemma is set up so that goodness can be decided one exRec at a time.

**Step 3: the failure rate of one level.** An exRec is *bad* only if it has two faults that together break it. If an exRec has at most $A$ pairs of locations, then

$$\Pr[\text{a given exRec is bad}] \le A \varepsilon^2 = \varepsilon_{\mathrm{th}} (\varepsilon/\varepsilon_{\mathrm{th}})^2 \quad\text{with } \varepsilon_{\mathrm{th}} = 1/A.$$

So the noisy level-1 circuit behaves like the ideal circuit run with level-1 locations that fail with rate $\varepsilon^{(1)} \le A \varepsilon^2$, and the failures still satisfy the local stochastic condition, since disjoint exRecs depend on disjoint faults (up to the shared corrections, which the lemma handles).

**Step 4: concatenation.** Replace each physical location of a level-1 gadget by a level-1 gadget again. The level-$k$ circuit is a level-1 simulation of the level-$(k-1)$ circuit, so by induction

$$\varepsilon^{(k)} \le \varepsilon_{\mathrm{th}} \left(\frac{\varepsilon}{\varepsilon_{\mathrm{th}}}\right)^{2^k}.$$

For $\varepsilon < \varepsilon_{\mathrm{th}}$ this falls doubly exponentially in $k$.

**Step 5: the overhead.** Each of the $m$ locations of $C$ fails at level $k$ with probability at most $\varepsilon^{(k)}$, so by the union bound the whole run is correct except with probability $m \varepsilon^{(k)} \le \delta$ as soon as $2^k \ge \log(m \varepsilon_{\mathrm{th}}/\delta) / \log(\varepsilon_{\mathrm{th}}/\varepsilon)$, that is, $2^k = O(\log(m/\delta))$. If a level-1 gadget has at most $L$ locations and depth at most $D$, the level-$k$ simulation has at most $L^k = (2^k)^{\log_2 L} = O(\log^{\log_2 L}(m/\delta))$ locations and depth $D^k$ per ideal location, which is polylogarithmic. When an outcome of the ideal circuit is a measurement, its logical value is decoded classically by the same recursion. $\blacksquare$

The detailed proofs must also handle: errors that enter during decoding of the final measurements; the correlation of faults in shared error-correction steps; noise that is not a Pauli channel, by expanding it in [Kraus operators](/kraus-operators/) and using the discretization of errors; and, for the non-Markovian version of Aliferis, Gottesman and Preskill, a bath that couples to the qubits with a bounded local Hamiltonian. Aharonov and Ben-Or give a different proof with *proper* codes, polynomial codes over qupits, and correct without measurement.

## Consequences

- **Quantum computing is possible in principle.** Under the hypotheses, a noisy quantum computer with error rate below the threshold computes [BQP](/bqp/) with only a polylogarithmic slowdown. Noise is an engineering problem, not a fundamental barrier, as long as it is local and weakly correlated.
- **Resource estimates are possible.** With $\varepsilon$ ten times below a threshold of $10^{-2}$, the bound $\varepsilon_{\mathrm{th}}(\varepsilon/\varepsilon_{\mathrm{th}})^{2^k}$ reaches $10^{-15}$ at $k = 4$ levels, which is $7^4 = 2401$ physical qubits per logical qubit for the concatenated Steane code before ancillas. Modern estimates use the surface code instead, whose distance grows by steps and whose threshold is higher.
- **The gate set must be fault tolerant, not only universal.** The [Clifford group](/clifford-group/) gates are transversal in many codes; the $T$ gate needs magic states. The [Solovay-Kitaev theorem](/solovay-kitaev-theorem/) then compiles any circuit into this set with a polylogarithmic overhead, so the two overheads multiply.
- **Error correction can be checked classically.** The gadgets are Clifford circuits, so with Pauli noise the [Gottesman-Knill theorem](/gottesman-knill-theorem/) simulates them efficiently, which is how thresholds are estimated numerically.
- **Experiments test it.** In 2025 a Google group ran a distance-7 surface code memory in which each step of the distance by 2 lowered the logical error rate by a factor of about $2.14$, the behaviour expected below threshold.

## Tightness

Each hypothesis matters, and the threshold is a true constant.

- **Fresh qubits.** Without fresh qubits during the computation, Aharonov, Ben-Or, Impagliazzo and Nisan show that a noisy quantum circuit that is not useless must have size exponential in its depth. Noise adds entropy, and only fresh qubits or measurement with reset remove it.
- **Noise above a constant.** The threshold cannot be close to 1. Razborov shows that with independent noise on all wires at a rate above $1/2$ and gates of fan-in 2, a qubit cannot even be stored for more than logarithmic time, so the threshold is at most $1/2$ under the assumption $\mathrm{QP} \not\subseteq \mathrm{QNC}^1$.
- **Correlated noise.** The condition $\Pr[R \subseteq F] \le \varepsilon^r$ excludes noise that hits many qubits at once, such as a stray field that rotates every qubit by the same angle. Such errors break every block in the same way, and a code of fixed distance does not help.
- **The rate of the decoder.** Classical decoding must keep up with the syndrome rate, or a backlog of syndromes grows without limit.
- **A classical analogue.** For the 3-bit [repetition code](/repetition-code/) on the [binary symmetric channel](/binary-symmetric-channel/) with perfect majority votes, one level maps the flip rate $p$ to $f(p) = 3p^2 - 2p^3$. The fixed point $p = 1/2$ is the threshold: below it the concatenated code drives the error to $0$, above it to $1$. The quantum theorem is harder only because the gates that do the correction are noisy too, which lowers the threshold by orders of magnitude.

**A small example to check by hand.** Take the bound with $A = 100$, so $\varepsilon_{\mathrm{th}} = 10^{-2}$, and $\varepsilon = 10^{-3}$. Level 1 gives $100 \cdot 10^{-6} = 10^{-4}$, level 2 gives $10^{-6}$, level 3 gives $10^{-10}$ and level 4 gives $10^{-18}$. The number of correct digits doubles at each level, while the size grows by the constant factor $L$.

### Implementation

The file `impl/python/quantum_threshold_theorem.py` computes the concatenation recursion exactly in two *code-capacity* models, where noise hits only the data and decoding is perfect. It is not a fault-tolerant simulation, so its thresholds are far above the threshold of the theorem. The first model is the concatenated 3-bit majority code. The second is the concatenated Steane code: each qubit gets an independent Pauli error, each block is decoded by its Hamming syndrome, and one level maps the physical Pauli channel to the exact logical Pauli channel by a sum over all $4^7 = 16384$ error patterns, with `fractions.Fraction` or floats.

The tests check: the majority recursion against brute force over all $2^9$ patterns of level 2, and level 3 against 20000 samples (seed 6061) with a Hoeffding tolerance; the bound $p_k \le \tfrac13 (3p)^{2^k}$ for $k \le 5$; the fixed point $1/2$; the Steane failure counts by weight, $0, 0, 147, 693, 2226, 3822, 3675, 1725$, where of the 189 errors of weight 2 exactly the 42 errors $X_i Z_j$ with $i \ne j$ are corrected; the exact logical channel at $p = 1/100$; the leading term $(147/9) p^2$ for depolarizing noise of rate $p$; a one-level pseudo-threshold of about $0.0811$; double exponential decay at $p = 0.01$ (failure rates $0.01$, $1.6 \times 10^{-3}$, $3.3 \times 10^{-5}$, $1.0 \times 10^{-8}$ for levels 0 to 3); growth at $p = 0.12$; and the level count of the example above. With more levels the logical channel stops being depolarizing ($Y$ errors become rarer than $X$ and $Z$), so the multi-level threshold of this model is higher than the one-level value; in our runs the failure rate still falls to $0$ for depolarizing rates up to about $0.093$.

## History

Shor (1996) gave the first fault-tolerant constructions, which worked when the error rate is logarithmically small in the size of the circuit, as Aharonov and Ben-Or describe it. Aharonov and Ben-Or (STOC 1997, journal version 2008), Kitaev (1997) and Knill, Laflamme and Zurek (1998) independently proved that a constant error rate is enough, using concatenated codes. Aharonov and Ben-Or also proved it for circuits with only nearest-neighbour gates. Aharonov, Ben-Or, Impagliazzo and Nisan (1996) showed why fresh qubits are needed. Aliferis, Gottesman and Preskill (2006) gave the extended-rectangle proof for distance-3 codes with the bound $2.73 \times 10^{-5}$ and extended it to local non-Markovian noise. Topological codes, analysed by Dennis, Kitaev, Landahl and Preskill (2002) and later by Fowler and coauthors, raised the estimated threshold to about $1\%$, and in 2025 a superconducting device showed surface code memory below threshold.

## References
