---
tag: 98XS2A
kind: algorithm
slug: parallel-prefix
name: Parallel prefix computation
aliases:
- prefix circuit
- Ladner-Fischer prefix circuit
area: parallel/parallel-primitives
level: core
summary: Computes all prefix sums of an array under an associative operator in parallel with logarithmic span and linear work.
solves: [all-prefix-sums]
model: work-span-model
complexity:
  vars: {n: the number of inputs}
  time: {worst: Θ(n)}
  depth: {worst: Θ(log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: true}
prereqs: [all-prefix-sums, blelloch-scan, boolean-circuit]
see_also: [hillis-steele-scan, kogge-stone-adder, brent-kung-adder, sklansky-adder, carry-lookahead-adder, sorting-network, circuit-complexity, segmented-scan]
sources:
  - paper: doi:10.1145/322217.322232
    title: Richard E. Ladner and Michael J. Fischer, Parallel Prefix Computation, Journal of the ACM 27(4), 831 to 838, 1980
    locator: the recursive construction of the circuits P_k(n), with depth at most k + ⌈lg n⌉ and size at most 2(1 + 2^−k)n, and the example C(P_0(9)) = 13
  - paper: doi:10.1109/TC.1973.5009159
    title: Peter M. Kogge and Harold S. Stone, A Parallel Algorithm for the Efficient Solution of a General Class of Recurrence Equations, IEEE Transactions on Computers C-22(8), 786 to 793, 1973
    locator: the recursive doubling algorithm
  - paper: doi:10.1109/TC.1982.1675982
    title: Richard P. Brent and H. T. Kung, A Regular Layout for Parallel Adders, IEEE Transactions on Computers C-31(3), 260 to 264, 1982
    locator: the carry computation as a prefix problem and its tree layout
  - paper: doi:10.1109/TEC.1960.5219822
    title: J. Sklansky, Conditional-Sum Addition Logic, IRE Transactions on Electronic Computers EC-9(2), 226 to 231, 1960
    locator: the conditional-sum adder
  - paper: doi:10.1016/0196-6774(86)90003-9
    title: Marc Snir, Depth-size trade-offs for parallel prefix computation, Journal of Algorithms 7(2), 185 to 201, 1986
    locator: the lower bound depth + size ≥ 2n − 2 and the circuits that meet it
  - paper: doi:10.1145/800061.808738
    title: Faith E. Fich, New bounds for parallel prefix circuits, Proceedings of the 15th ACM Symposium on Theory of Computing (STOC), 100 to 109, 1983
    locator: the bounds on the size of prefix circuits of a given depth
  - url: https://www.cs.cmu.edu/~guyb/papers/Ble93.pdf
    title: Guy E. Blelloch, Prefix Sums and Their Applications, Technical Report CMU-CS-90-190, Carnegie Mellon University, 1990
    locator: Notes at the end of the chapter (Ofman 1963, Kogge and Stone, Ladner and Fischer, Brent and Kung, Fich)
---

Parallel prefix computation is the [all-prefix-sums](/all-prefix-sums/) problem viewed as a circuit. Each gate applies an [associative operator](/associative-operator/) $\oplus$ to two wires. The size of the circuit (the number of gates) is its work, and its depth (the longest path of gates) is its span. Ladner and Fischer (1980) built, for each $k \ge 0$, a circuit $P_k(n)$ with depth at most $k + \lceil \lg n \rceil$ and size at most $2(1 + 2^{-k})n$. So the optimal depth $\lceil \lg n \rceil$ is possible with at most $4n$ gates. The classic circuits of Sklansky, Kogge and Stone, and Brent and Kung are other points on the same trade-off between size and depth.

## In plain words

A prefix circuit is a fixed wiring diagram. Numbers go in at the top, each box adds the two numbers that reach it, and the running totals come out at the bottom. The diagram does not depend on the data, so it can be built into hardware, such as the part of a processor that adds two binary numbers.

Two things count: the number of boxes, which is the cost of the hardware or the work, and the number of boxes on the longest path, which is the delay. A chain of boxes is cheap but slow. A diagram where every output looks back in steps of 1, 2, 4 and so on is fast but has many boxes. Ladner and Fischer showed how to be as fast as possible with only a few times as many boxes as the chain.

## The problem

The input is $n$ values $v_1, \ldots, v_n$ on $n$ wires and an associative operator $\oplus$. A prefix circuit is a sequence of gates; each gate takes two wires $s < t$ and puts $w[s] \oplus w[t]$ on wire $t$, with the earlier wire on the left. At the end, wire $j$ must hold $v_1 \oplus \cdots \oplus v_j$, the inclusive scan. The circuit must work for every associative operator, so it may use only associativity, not commutativity or inverses. Its size is the number of gates and its depth is the largest number of gates on a path from an input to an output.

## The algorithm

The procedure below adds the gates of $P_k$ to the circuit for the wires $w[1..n]$. The calls on lines L4 and L5 use disjoint wires, so their gates can run at the same time.

```pseudo id=main
PREFIX(w[1..n], k)                   ▷ adds the gates of P_k(n)
L1   if n ≤ 1 then return
L2   if k = 0 then
L3     c ← ⌈n/2⌉
L4     PREFIX(w[1..c], 1)
L5     PREFIX(w[c+1..n], 0)
L6     for j ← c + 1 to n do add gate w[j] ← w[c] ⊕ w[j]
L7   else
L8     for i ← 1 to ⌊n/2⌋ do add gate w[2i] ← w[2i − 1] ⊕ w[2i]
L9     PREFIX(w[2], w[4], …, w[2⌊n/2⌋], and w[n] if n is odd; k − 1)
L10    for each odd j with 3 ≤ j < n do add gate w[j] ← w[j − 1] ⊕ w[j]
```

For $k = 0$, the circuit splits the wires into halves, as Sklansky does, but solves the left half with $P_1$, which is cheaper and still fast enough. Its last output is ready after only $\lceil \lg n \rceil - 1$ levels, in time for line L6. For $k \ge 1$, the circuit adds adjacent pairs, solves the problem for the $\lceil n/2 \rceil$ pair sums with $P_{k-1}$, and then fills in the odd positions, as the [Blelloch scan](/blelloch-scan/) does. A larger $k$ gives fewer gates and more depth.

## Example

Run $P_1(8)$ on $[3, 1, 7, 0, 4, 1, 6, 3]$ with $+$. The gates come in four levels; each row shows the wires after one level, with wire indices from 0.

| level | gates (source, target) | wires |
|---|---|---|
| input | | 3, 1, 7, 0, 4, 1, 6, 3 |
| 1 | (0,1) (2,3) (4,5) (6,7) | 3, 4, 7, 7, 4, 5, 6, 9 |
| 2 | (1,3) (5,7) | 3, 4, 7, 11, 4, 5, 6, 14 |
| 3 | (3,5) (3,7) | 3, 4, 7, 11, 4, 16, 6, 25 |
| 4 | (1,2) (3,4) (5,6) | 3, 4, 11, 11, 15, 16, 22, 25 |

This circuit has 11 gates and depth 4. For $n = 8$ it is the same as the Brent-Kung circuit. The circuit $P_0(8)$ has 12 gates and depth $3 = \lg 8$, the same gates as the Sklansky circuit. The Kogge-Stone circuit, which is the [Hillis-Steele scan](/hillis-steele-scan/), has depth 3 but 17 gates.

## Correctness

The proof is by strong induction on $n$. For $k = 0$, the two calls leave the prefixes of each half, and line L6 puts the total of the left half in front of each right prefix. For $k \ge 1$, after line L8 the even wires hold pair sums, so the prefixes of the pair sums are the prefixes at even positions; line L10 then adds one more input to get each odd position. The depth bound follows by the same induction, together with the fact that the last output of $P_k(n)$ has depth at most $\lceil \lg n \rceil$ for every $k$. The full proof is in [the proof of correctness](proofs/correctness.md).

## Complexity

The field `time` of this page is the size of the circuit, and the field `depth` is its depth.

**The trade-off.** For $n = 2^K$, the classic prefix circuits have the size and depth below. The tests check each formula.

| circuit | size | depth | largest fan-out |
|---|---|---|---|
| serial (a chain) | $n - 1$ | $n - 1$ | 1 |
| [Sklansky](/sklansky-adder/) (1960) | $\frac{n}{2} \lg n$ | $\lg n$ | $n/2$ |
| [Kogge-Stone](/kogge-stone-adder/) (1973) | $n \lg n - n + 1$ | $\lg n$ | 2 |
| [Brent-Kung](/brent-kung-adder/) (1982), $n \ge 4$ | $2n - 2 - \lg n$ | $2 \lg n - 2$ | small |
| Ladner-Fischer $P_k$ (1980) | $\le 2(1 + 2^{-k})n$ | $\le k + \lceil \lg n \rceil$ | grows with $n$ |

**Lower bounds.** Every prefix circuit has size at least $n - 1$, since each output except the first needs a gate, and depth at least $\lceil \lg n \rceil$, since the last output depends on all $n$ inputs. Snir (1986) proved the stronger bound
$$
\text{depth} + \text{size} \ge 2n - 2
$$
for every prefix circuit, and built circuits that meet it with equality for every depth between about $2 \lg n$ and $n - 1$. Circuits that meet the bound are called zero-deficiency circuits. So for small depth, each level of depth saved costs at least one more gate. At the smallest depth, Fich (1983) gave sharper bounds on the size.

**As a parallel algorithm.** A circuit of size $s$ and depth $d$ is a parallel algorithm with work $s$ and span $d$ in the [work-span model](/work-span-model/). On a PRAM, one level of gates is one step, and the gates of one level read and write distinct wires except for fan-out, so circuits with fan-out greater than one need a CREW PRAM or a copy step. By [Brent's theorem](/brent-theorem/), $P_0(n)$ runs in time $O(n/p + \log n)$ on $p$ processors.

## Properties

- **Oblivious.** The gates do not depend on the data, so the same circuit works for every input and every associative operator.
- **Order-keeping.** Each gate has the earlier wire on the left, so commutativity is not needed. This matters for carry operators and for matrix products.
- **Deterministic.** A fixed circuit fixes the bracketing, so floating-point results are reproducible, but different circuits give different results.
- **Inclusive.** Wire $j$ ends with the prefix that includes input $j$.

## Variants and improvements

- **Adders.** A binary adder computes its carries with a prefix circuit over pairs (generate, propagate) and the associative carry operator $(g, p) \circ (g', p') = (g' \lor (p' \land g),\ p \land p')$, where $(g, p)$ is the lower block. The [carry-lookahead adder](/carry-lookahead-adder/) page gives the details, and the Sklansky, Kogge-Stone and Brent-Kung adders are named after their prefix circuits.
- **Fan-out and wiring.** In hardware, size and depth are not the only costs. Kogge-Stone keeps fan-out at 2 but has long wires and many gates; Sklansky has few levels but a fan-out of $n/2$; Brent-Kung has few gates and short wires but twice the depth. Knowles and Han-Carlson circuits sit between these.
- **Software scans.** The [Hillis-Steele scan](/hillis-steele-scan/) is the Kogge-Stone circuit run on a PRAM, and the [Blelloch scan](/blelloch-scan/) is a work-efficient tree circuit with an exclusive output. GPU warp scans use the Kogge-Stone shape because the lanes are free.
- **Segmented prefix.** With the segmented operator on (flag, value) pairs, every prefix circuit computes a [segmented scan](/segmented-scan/).

## When to use it

Think in terms of prefix circuits when the structure is fixed in advance: adders and other arithmetic hardware, sorting and permutation networks that are built from scans, and SIMD code where all lanes run the same instructions. Choose a point on the trade-off by the cost that matters most: depth for delay, size for area or energy, and fan-out and wire length for layout. In software on a few cores, the blocked form of a work-efficient scan is usually better than any fixed circuit.

## Pitfalls

- **The depth of the last output.** The bound for $P_0$ depends on the last output of the left $P_1$ being ready after $\lceil \lg n \rceil - 1$ levels, before the other outputs of $P_1$. A depth count that takes the maximum depth of the whole sub-circuit gets $\lceil \lg n \rceil + 1$ instead.
- **Gate order in a simulation.** When a level of gates is simulated sequentially in place, a gate can read a wire that another gate of the same level has already changed. Process a level so that every read comes before every write to the same wire, as in descending order for Kogge-Stone.
- **Swapped operands.** A gate $w[t] \oplus w[s]$ works for $+$ and $\max$ but not for the carry operator, matrices or strings.
- **Mixing up conventions.** Published size and depth values for the same circuit differ by one or two, because some authors count the first level of an adder, or the exclusive output, as part of the prefix circuit.

## Implementations

## History

Sklansky (1960) used the divide-and-conquer circuit in the conditional-sum adder. Blelloch's notes credit Ofman (1963) with the first parallel circuit for prefix computation, in the context of binary addition. Kogge and Stone (1973) solved first-order recurrences by recursive doubling, which is the circuit now named after them. Ladner and Fischer (1980) stated the problem for any associative operator, called it parallel prefix computation, and gave the family $P_k(n)$, with optimal depth and linear size together. Brent and Kung (1982) gave a regular layout with $O(n)$ gates and depth about $2 \lg n$ for VLSI adders. Fich (1983) and Snir (1986) proved lower bounds on the trade-off, and later work built circuits that meet them.

## References
