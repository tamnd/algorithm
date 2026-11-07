---
tag: B7EE9Z
kind: model
slug: parallel-fft-circuit
name: Parallel FFT circuit
aliases:
- FFT circuit
- butterfly network
- FFT graph
- FFT network
area: algebra/fast-transforms
level: advanced
summary: Circuit of butterfly operations arranged in stages that computes the FFT in logarithmic depth.
prereqs: [fast-fourier-transform, butterfly-operation, iterative-fft]
see_also: [straight-line-program, boolean-circuit, circuit-complexity, pram-model, red-blue-pebble-game, external-memory-model, sorting-network, bit-reversal-permutation]
sources:
  - paper: doi:10.1145/321450.321457
    title: Marshall C. Pease, An adaptation of the fast Fourier transform for parallel processing, Journal of the ACM 15(2), 1968
    locator: pp. 252 to 264 (the FFT as stages of sums and differences, a perfect shuffle, and multiplications by constants)
  - paper: doi:10.1109/T-C.1971.223205
    title: Harold S. Stone, Parallel processing with the perfect shuffle, IEEE Transactions on Computers C-20(2), 1971
    locator: pp. 153 to 161 (the FFT on a shuffle-exchange network)
  - paper: doi:10.1145/321752.321761
    title: Jacques Morgenstern, Note on a lower bound on the linear complexity of the fast Fourier transform, Journal of the ACM 20(2), 1973
    locator: pp. 305 to 306 (at least (n/2) lg n additions for linear algorithms with constants of modulus at most 1)
  - paper: doi:10.1145/800135.804401
    title: C. D. Thompson, Area-time complexity for VLSI, Proceedings of the 11th Annual ACM Symposium on Theory of Computing, 1979
    locator: pp. 81 to 88 (the bound AT^2 at least N^2/16 for the DFT on a chip)
  - paper: doi:10.1109/TC.1983.1676155
    title: Clark D. Thompson, Fourier transforms in VLSI, IEEE Transactions on Computers C-32(11), 1983
    locator: pp. 1047 to 1057 (a survey of nine chip designs for the transform)
  - paper: doi:10.1145/358645.358660
    title: Franco P. Preparata and Jean Vuillemin, The cube-connected cycles, a versatile network for parallel computation, Communications of the ACM 24(5), 1981
    locator: pp. 300 to 309
  - paper: doi:10.1145/800076.802486
    title: Hong Jia-Wei and H. T. Kung, I/O complexity, the red-blue pebble game, Proceedings of the 13th Annual ACM Symposium on Theory of Computing, 1981
    locator: pp. 326 to 333 (the FFT graph needs Ω(n log n / log S) input and output steps with memory S)
  - paper: doi:10.1145/48529.48535
    title: Alok Aggarwal and Jeffrey Scott Vitter, The input/output complexity of sorting and related problems, Communications of the ACM 31(9), 1988
    locator: pp. 1116 to 1127 (tight bounds for the FFT with blocks of B records)
  - paper: doi:10.1109/SFFCS.1999.814600
    title: Matteo Frigo, Charles E. Leiserson, Harald Prokop and Sridhar Ramachandran, Cache-oblivious algorithms, Proceedings of the 40th Annual Symposium on Foundations of Computer Science, 1999
    locator: pp. 285 to 297 (a cache-oblivious FFT)
---

The parallel FFT circuit is the radix-2 [fast Fourier transform](/fast-fourier-transform/) of length $n = 2^m$ written as a fixed network: $m = \lg n$ stages, each made of $n/2$ independent [butterfly operations](/butterfly-operation/), with wires between the stages that depend only on $n$. Because no operation depends on the data, the FFT is an arithmetic circuit, and the circuit is the right model for questions that the operation count alone does not answer: how fast the transform runs with many processors (the depth), how it maps onto a network of processors or a chip (the wiring), and how much data must move between levels of memory (the input and output of the graph). Its size is $\frac n2 \lg n$ multiplications and $n \lg n$ additions, its depth is $\lg n$ butterfly stages, and there is exactly one path from each input to each output.

## The machine

**Notation.** As on all pages of fast transforms, $n$ is the transform length, here a power of two, $m = \lg n$, and $\omega_n = e^{-2\pi i/n}$, the sign of signal processing, FFTW and NumPy (CLRS uses the other sign). The circuit computes $X_k = \sum_{j=0}^{n-1} x_j \omega^{jk}$ for a root $\omega$ with $\omega^{n/2} = -1$: over $\mathbb{C}$, $\omega = \omega_n$; over $\mathbb{Z}/p\mathbb{Z}$, a principal $n$-th root of unity. The inverse is the same circuit with $\omega^{-1}$ followed by $n$ multiplications by $1/n$.

**Arithmetic circuits.** An arithmetic circuit over a ring $R$ is a directed acyclic graph whose sources are the inputs $x_0, \ldots, x_{n-1}$ and constants of $R$, and whose other nodes (gates) compute the sum, difference or product of the values on two incoming wires. Some gates are marked as outputs. The *size* is the number of gates and the *depth* the length of the longest path from a source to an output. A circuit is the graph of a [straight-line program](/straight-line-program/), and it is *linear* if every product has a constant as one factor. A butterfly gate computes $(u, v) \mapsto (u + c v, u - c v)$ for a constant $c$; it is one multiplication by a constant and two additions, and has depth $2$ in gates or $1$ in butterflies.

**The FFT circuit.** Number the wires of each stage $0$ to $n - 1$. The input stage holds $x$ in [bit-reversed order](/bit-reversal-permutation/): wire $i$ carries $x_{\mathrm{rev}(i)}$, where $\mathrm{rev}$ reverses the $m$ binary digits. At stage $s = 1, \ldots, m$, with block size $b = 2^s$, each block $[q, q + b)$ with $q$ a multiple of $b$ has $b/2$ butterflies; the butterfly at offset $r$, $0 \le r < b/2$, reads the wires $q + r$ and $q + r + b/2$ and writes

$$(u, v) \mapsto (u + \omega^{(n/b) r} v,\ u - \omega^{(n/b) r} v).$$

After stage $m$, wire $k$ carries $X_k$. This is the circuit of the [iterative FFT](/iterative-fft/), where each stage is one pass of the loop; its correctness proof there is a proof for the circuit. The connections between consecutive stages, wire $w$ to the wire that differs from it in one binary digit, form the *butterfly network*.

**An example.** Over $\mathbb{Z}/17\mathbb{Z}$ with $n = 8$, $\omega = 2$ (so $\omega^4 = 16 = -1$) and $x = (1, 2, \ldots, 8)$, the input stage holds $(1, 5, 3, 7, 2, 6, 4, 8)$. Stage 1 uses the constant $1$ and gives $(6, 13, 10, 13, 8, 13, 12, 13)$. Stage 2 uses $1$ and $\omega^2 = 4$ and gives $(16, 14, 13, 12, 3, 14, 13, 12)$. Stage 3 uses $1, 2, 4, 8$ and gives $X = (2, 8, 14, 6, 13, 3, 12, 1)$, the DFT of $x$ with root $2$ modulo $17$. A script checked the three stages and that every input reaches every output by exactly one path.

## What it counts

- **Size.** The circuit has $\frac n2 \lg n$ butterflies: $\frac n2 \lg n$ multiplications by constants and $n \lg n$ additions and subtractions. Skipping the constants $\omega^0 = 1$ removes $n - 1$ multiplications, and over $\mathbb{C}$ skipping $\pm i$ as well removes $\frac n2 - 1$ more.
- **Depth.** $\lg n$ butterfly stages, or $2\lg n$ gates (one product and one sum on each path through a butterfly). All $n/2$ butterflies of a stage are independent, so with $n/2$ processors, one per butterfly, the transform takes $\lg n$ parallel steps.
- **Width.** Every stage has exactly $n$ wires; no value needs to live longer than one stage.
- **Wiring.** Stage $s$ connects wires whose numbers differ in binary digit $s - 1$. The total number of wires is $n(\lg n + 1)$ values, and the graph has $n(\lg n + 1)$ nodes in $\lg n + 1$ columns.
- **Data movement.** The graph is the dependence structure of every radix-2 FFT, so it is the object to which pebble games and memory-hierarchy bounds apply.

| n | butterflies | multiplications | additions | depth (stages) |
|---|---|---|---|---|
| 2 | 1 | 1 | 2 | 1 |
| 4 | 4 | 4 | 8 | 2 |
| 8 | 12 | 12 | 24 | 3 |
| 16 | 32 | 32 | 64 | 4 |
| 32 | 80 | 80 | 160 | 5 |

## Relation to other models

- **Straight-line programs and the real RAM.** The circuit is a straight-line program with $\frac32 n \lg n$ operations; the sequential FFT in the [real RAM](/real-ram/) executes it gate by gate. The loop structure of the iterative FFT only generates the circuit.
- **PRAM.** Each stage is one step of $n/2$ processors on a [PRAM](/pram-model/), reading and writing disjoint cells, so the FFT runs on an [EREW PRAM](/erew-pram/) in $O(\log n)$ time with $n/2$ processors and $O(n \log n)$ work.
- **Networks of processors.** On a network with one processor per wire, stage $s$ needs only the links between nodes that differ in one binary digit. A hypercube has all of them. Stone (1971) showed how to run the FFT on the shuffle-exchange network, where every stage uses the same perfect shuffle followed by an exchange of neighbours; Pease (1968) had already rewritten the FFT so that every stage has the same pattern of sums and differences, a fixed shuffle and multiplications by constants. Preparata and Vuillemin (1981) designed the cube-connected cycles, a network of bounded degree that runs the FFT with little loss.
- **Boolean circuits.** Over $\mathbb{Z}/p\mathbb{Z}$, replacing each gate by a [Boolean circuit](/boolean-circuit/) for modular addition or multiplication gives a Boolean circuit for the number-theoretic transform; its size and depth multiply those of the arithmetic circuit by the cost of the gates.
- **Sorting networks.** The butterfly network is also the wiring of the merging network of [bitonic sort](/bitonic-sort/): both are built from stages that combine wires differing in one binary digit.
- **Memory hierarchies.** In the [red-blue pebble game](/red-blue-pebble-game/) and the [external memory model](/external-memory-model/), the cost of an FFT is the cost of pebbling this graph with a fast memory of bounded size.

## Known results in the model

**Size and depth of the circuit.** The circuit above has $\frac n2 \lg n$ butterflies and depth $\lg n$, and it computes the DFT; this is the correctness of the [iterative FFT](/iterative-fft/), whose loop performs exactly these butterflies. Cooley and Tukey's algorithm therefore gives a linear circuit of size $\frac32 n \lg n$ and depth $2 \lg n$.

**Depth lower bound.** Every output $X_k$ depends on every input, because each coefficient $\omega^{jk}$ is a unit. In a circuit with fan-in $2$, a value at depth $d$ depends on at most $2^d$ sources, so every circuit for the DFT has depth at least $\lg n$, counting gates. The FFT circuit has depth $\lg n$ in butterflies and $2 \lg n$ in gates, so it is within a factor $2$ of optimal depth.

**Unique paths.** For every input wire $i$ and output wire $k$, there is exactly one path from $i$ to $k$ in the FFT graph. *Proof.* Going through stage $s$, a path keeps all binary digits of its wire number except digit $s - 1$, which it may set to either value. After stages $1, \ldots, m$ every digit has been chosen once, so the path is determined by its endpoints, and every endpoint is reachable. Hence the coefficient of the input on wire $i$ in output $k$ is the product of the constants along one path, a power of $\omega$.

**Size lower bound with bounded constants.** Morgenstern (1973) proved that a linear algorithm over $\mathbb{C}$ whose constants have modulus at most $1$ needs at least $\frac n2 \lg n$ additions to compute the DFT. The argument: each new linear form $\alpha u + \beta v$ at most doubles the largest absolute determinant of $n$ of the forms computed so far, which starts at $1$, and $|\det F_n| = n^{n/2}$ because $F_n F_n^* = nI$. The FFT circuit, whose constants are powers of $\omega$ and have modulus $1$, uses $n \lg n$ additions, so it is optimal within a factor $2$ in this model. Without a bound on the constants no superlinear lower bound for the DFT is known.

**Chips.** In Thompson's model of VLSI, where a chip of area $A$ computes a function in time $T$, every chip for the $N$-point DFT satisfies $AT^2 \ge N^2/16$ (Thompson 1979). Thompson (1983) surveyed nine designs, from a fully parallel one with area $O(N^2 \log N)$ that starts a new transform every $O(\log N)$ time units to small designs with about $1/N$ of its area and throughput.

**Memory traffic.** With a fast memory of $S$ words, pebbling the FFT graph needs $\Omega(n \log n / \log S)$ transfers between fast and slow memory, and this is achievable (Hong and Kung 1981). With blocks of $B$ records, Aggarwal and Vitter (1988) proved matching upper and lower bounds for the FFT in the external memory model, of the same order as for sorting, and Frigo, Leiserson, Prokop and Ramachandran (1999) gave an FFT that achieves the optimal number of cache misses, under a tall-cache assumption, without knowing the cache size.

## References
