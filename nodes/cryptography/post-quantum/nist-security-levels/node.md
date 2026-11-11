---
tag: RP9RYK
kind: definition
slug: nist-security-levels
name: NIST post-quantum security levels
aliases:
- NIST PQC security categories 1 to 5
- NIST security categories
area: cryptography/post-quantum
level: intro
summary: "Five categories that rate a post-quantum parameter set by the cost of breaking it against key search on AES-128, 192, 256 or collision search on SHA-256 or SHA-384."
prereqs: [post-quantum-cryptography, grover-search, advanced-encryption-standard, birthday-attack]
see_also: [nist-pqc-standardization, core-svp-hardness, crystals-kyber, crystals-dilithium, sphincs-plus, grover-optimality, sha-3, quantum-circuit-model]
sources:
  - url: "https://csrc.nist.gov/CSRC/media/Projects/Post-Quantum-Cryptography/documents/call-for-proposals-final-dec-2016.pdf"
    title: "NIST, Submission Requirements and Evaluation Criteria for the Post-Quantum Cryptography Standardization Process, December 2016"
    locator: Section 4.A.5 (the five categories, MAXDEPTH from 2^40 to 2^96, the table of gate counts, and footnotes 2, 4 and 5)
  - url: "https://csrc.nist.gov/csrc/media/Projects/pqc-dig-sig/documents/call-for-proposals-dig-sig-sept-2022.pdf"
    title: "NIST, Call for Additional Digital Signature Schemes for the Post-Quantum Cryptography Standardization Process, September 2022"
    locator: Section 4.B.3 (the same categories with the updated quantum gate counts 2^157, 2^221 and 2^285 divided by MAXDEPTH, and footnote 4)
  - paper: doi:10.6028/NIST.IR.8547
    title: "NIST IR 8547, Transition to Post-Quantum Cryptography Standards, final version, October 2026"
    locator: Section 4.1, Table 1 (the categories), Table 3 (signature parameter sets and note 2 on ML-DSA-44), Table 5 (ML-KEM) and Section 4.1.3 with Table 6 (block ciphers)
  - paper: doi:10.1007/978-3-319-29360-8_3
    title: "Markus Grassl, Brandon Langenberg, Martin Roetteler and Rainer Steinwandt, Applying Grover's algorithm to AES: quantum resource estimates, PQCrypto 2016, LNCS 9606"
    locator: the resource tables for AES-128, AES-192 and AES-256 (the source of the 2016 quantum figures)
  - paper: doi:10.1007/978-3-030-45724-2_10
    title: "Samuel Jaques, Michael Naehrig, Martin Roetteler and Fernando Virdia, Implementing Grover oracles for quantum key search on AES and LowMC, Eurocrypt 2020, LNCS 12106"
    locator: the cost of parallel Grover search under a depth limit (the source of the 2022 quantum figures)
  - paper: doi:10.1103/PhysRevA.60.2746
    title: "Christof Zalka, Grover's quantum searching algorithm is optimal, Physical Review A 60, 2746, 1999"
    locator: the lower bound that makes parallel Grover search lose the quadratic speedup in total work
---

The NIST post-quantum security levels, which NIST calls security strength categories, are five classes that rate a parameter set by comparison with a reference attack on a symmetric primitive: key search on AES-128, AES-192 or AES-256 for categories 1, 3 and 5, and collision search on a 256-bit or 384-bit hash for categories 2 and 4. A parameter set is in a category when every attack on it costs at least as much as the reference attack, in every cost metric that NIST considers relevant, classical and quantum. The categories come from Section 4.A.5 of the 2016 call for proposals and are used in all the post-quantum standards, for example ML-KEM-512, ML-KEM-768 and ML-KEM-1024 in categories 1, 3 and 5.

## Definition

Let $\mathcal{S}$ be a cryptosystem with a fixed parameter set, and fix a security definition for it (IND-CCA2 for a KEM, EUF-CMA for a signature). Let $\mathcal{M}$ be the set of cost metrics that NIST considers relevant, for example the number of classical gates, and the number of quantum gates in a circuit of depth at most MAXDEPTH. Then $\mathcal{S}$ is in **category $c$** if, for every metric in $\mathcal{M}$, every attack that breaks the security definition costs at least as much as the reference attack of category $c$:

| category | reference attack | example | classical gates | quantum gates, 2016 call | quantum gates, 2022 call |
|---|---|---|---|---|---|
| 1 | key search on a 128-bit block cipher | AES-128 | $2^{143}$ | $2^{170}/\text{MAXDEPTH}$ | $2^{157}/\text{MAXDEPTH}$ |
| 2 | collision search on a 256-bit hash | SHA-256, SHA3-256 | $2^{146}$ | | |
| 3 | key search on a 192-bit block cipher | AES-192 | $2^{207}$ | $2^{233}/\text{MAXDEPTH}$ | $2^{221}/\text{MAXDEPTH}$ |
| 4 | collision search on a 384-bit hash | SHA-384, SHA3-384 | $2^{210}$ | | |
| 5 | key search on a 256-bit block cipher | AES-256 | $2^{272}$ | $2^{298}/\text{MAXDEPTH}$ | $2^{285}/\text{MAXDEPTH}$ |

The gate counts are the estimates in the calls, for the best known attacks with circuit depth limited to MAXDEPTH. The 2016 quantum figures come from Grassl, Langenberg, Roetteler and Steinwandt (2016), the 2022 figures from Jaques, Naehrig, Roetteler and Virdia (2020), which found cheaper AES circuits. The calls give only classical figures for the hash collision categories: the known quantum collision algorithms need a large quantum memory, and they are not believed to cost less than parallel classical collision search.

**MAXDEPTH.** This is a bound on the depth of the quantum circuit, that is, on its serial running time. The call gives three plausible values:

- $2^{40}$ logical gates, about what presently envisioned quantum architectures can do in series in a year;
- $2^{64}$ logical gates, about what current classical architectures can do in series in a decade;
- at most $2^{96}$ logical gates, about what atomic scale qubits with speed of light propagation could do in a millennium.

**Where $2^{k}/\text{MAXDEPTH}$ comes from.** A single Grover search on a $k$-bit key makes $\frac{\pi}{4}2^{k/2}$ iterations in series. If one iteration has depth $d$ and $g$ gates, the depth $\frac{\pi}{4}2^{k/2}d$ is far above MAXDEPTH. The attacker must split the key space over $S$ machines that each run $\frac{\pi}{4}\sqrt{2^k/S}$ iterations. The depth bound gives

$$S = \frac{2^k\left(\frac{\pi}{4}d\right)^2}{\text{MAXDEPTH}^2},\qquad \text{total gates} = S\cdot\frac{\pi}{4}\sqrt{\frac{2^k}{S}}\cdot g = \left(\frac{\pi}{4}\right)^2 d\,g\cdot\frac{2^k}{\text{MAXDEPTH}}.$$

So the product of the gate count and MAXDEPTH is constant, and Grover with parallel machines gains only a factor MAXDEPTH over classical exhaustive search, not the square root. Zalka (1999) showed that no quantum algorithm does better for unstructured search. The 2022 table puts $(\frac{\pi}{4})^2 d g = 2^{29}$ for all three AES key sizes.

**Rules that come with the categories.**

1. A parameter set that meets a higher category meets all lower ones.
2. NIST assumes that the categories are correctly ordered in practice: for example, collision search on SHA-256 becomes feasible before key search on AES-192 (2016 call, footnote 2).
3. The estimates may understate the security of SHA for very small MAXDEPTH and the quantum security of AES for very large MAXDEPTH (footnote 5).
4. A quantum gate may cost billions or trillions of times as much as a classical gate on present designs, but for the high categories NIST says it is prudent to assume that this gap can become small or disappear.

The code with this page computes $S$, the depth and the total gate count from $k$, MAXDEPTH, $d$ and $g$, recovers the constants $2^{42}, 2^{41}, 2^{42}$ (2016) and $2^{29}, 2^{29}, 2^{29}$ (2022) from the tables, and checks a given attack cost against the five thresholds. It is for study only.

## Examples and non-examples

**The standard parameter sets.** NIST IR 8547 (Tables 3 and 5) gives:

| standard | parameter set | category |
|---|---|---|
| FIPS 203 | ML-KEM-512, ML-KEM-768, ML-KEM-1024 | 1, 3, 5 |
| FIPS 204 | ML-DSA-44, ML-DSA-65, ML-DSA-87 | 2, 3, 5 |
| FIPS 205 | SLH-DSA-SHA2-128s and 128f, and the SHAKE versions | 1 |
| FIPS 205 | SLH-DSA 192s and 192f | 3 |
| FIPS 205 | SLH-DSA 256s and 256f | 5 |
| SP 800-208 | LMS, HSS, XMSS and XMSS^MT with SHA-256/192 or SHAKE256/192 | 3 |
| SP 800-208 | the same with SHA-256 or SHAKE256 | 5 |

ML-DSA-44 is in category 2, but drops to category 1 if the random bit generator gives less than 192 bits of security (IR 8547, Table 3, note 2). ML-KEM-768 is the recommended default. No standard parameter set targets category 4. The Falcon submission placed Falcon-512 in category 1 and Falcon-1024 in category 5, and HQC-128, HQC-192 and HQC-256 target categories 1, 3 and 5; FIPS 206 and the HQC standard will fix the final names.

**AES-128 under each MAXDEPTH (2022 figures).** With MAXDEPTH $=2^{40}$, Grover costs $2^{157-40}=2^{117}$ quantum gates, far less than the $2^{143}$ classical gates of exhaustive search. With MAXDEPTH $=2^{64}$ it costs $2^{93}$. Grover beats classical search in gate count only when MAXDEPTH $>2^{157-143}=2^{14}$. If we assume that one Grover iteration has depth $d=2^{12}$ (an illustrative value), the attack at MAXDEPTH $2^{40}$ needs $S\approx 2^{71.3}$ machines, and at $2^{64}$ about $2^{23.3}$ machines.

**The footnote 5 effect.** With the same $d=2^{12}$, a single machine finishes the whole serial Grover search in depth about $2^{75.7}$. For MAXDEPTH $=2^{96}$ no split is necessary, and the cost stays at the serial cost of about $2^{81.3}$ gates. The formula $2^{157}/2^{96}=2^{61}$ is lower than that, so for very large MAXDEPTH the table understates the cost of attacking AES.

**Categories are not "bits of quantum security".** AES-128 is in category 1, but its quantum security is not 64 bits. With $2^{40}$ depth the attack costs about $2^{117}$ gates, and each quantum gate is much more expensive than a classical gate. This is why NIST IR 8547 (Section 4.1.3) says that every approved symmetric primitive with at least 128 bits of classical security meets category 1, and why AES-128 stays acceptable.

**Non-example: a scheme with a $2^{140}$ classical attack.** It fails category 1, even if no quantum attack is known, because the classical threshold is $2^{143}$.

**Non-example: a scheme with a cheap quantum attack.** A parameter set whose best classical attack costs $2^{150}$ gates meets category 2 on classical cost. If a quantum attack costs $2^{120}$ gates at any depth, it fails category 2, which needs $2^{146}$ in every metric, but it still meets category 1, because at MAXDEPTH $2^{40}$ the reference attack on AES-128 costs only $2^{117}$.

**Non-example: SIKE.** SIKEp434 was submitted as category 1. The [Castryck-Decru attack](/castryck-decru-attack/) breaks it in about ten minutes on one core, so it meets no category. The categories rate known attacks; they say nothing about future ones.

## Related definitions

- **Security strength (bits of security).** NIST SP 800-57 rates classical schemes by $s$ bits, meaning that an attack needs about $2^s$ operations, with $s\in\{112, 128, 192, 256\}$. NIST IR 8547 keeps this number for classical attacks and uses the categories for quantum attacks, so ML-DSA-65 has 192 bits of classical security strength and category 3.
- **[Core-SVP hardness](/core-svp-hardness/).** The usual way to estimate the cost of lattice attacks, which lattice teams then map to a category.
- **[Grover search](/grover-search/)** and its [optimality](/grover-optimality/). The quantum attack behind categories 1, 3 and 5.
- **[Birthday attack](/birthday-attack/).** The classical collision attack behind categories 2 and 4.
- **[Quantum circuit model](/quantum-circuit-model/).** The model in which the quantum gate counts and depth are measured.
- **[NIST post-quantum standardization](/nist-pqc-standardization/).** The process that asked each submission to claim a category for each parameter set.

## References
