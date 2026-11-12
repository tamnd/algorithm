---
tag: W86NJM
kind: algorithm
slug: peeling-decoding
name: Peeling decoder
aliases:
- peeling algorithm
area: compression-and-coding/error-correcting-codes
level: advanced
summary: "Erasure decoder for sparse codes: solve a check with one unknown, put the value into the other checks, repeat. Linear time. It stops on a stopping set."
solves: [erasure-decoding]
model: word-ram
complexity:
  vars: {m: the number of edges of the Tanner graph, r: the number of checks}
  time: {worst: Θ(m + r), average: Θ(m + r), best: Θ(m + r)}
  space: {extra: Θ(m + r)}
properties: {deterministic: true, recursive: false, maximum_likelihood: false}
history:
  year: 1997
  people: [Michael Luby, Michael Mitzenmacher, Amin Shokrollahi, Daniel Spielman, Volker Stemann]
  note: Zyablov and Pinsker decoded low-density codes on the erasure channel this way in 1974. Luby, Mitzenmacher, Shokrollahi, Spielman and Stemann analyzed it in 1997 and designed codes for it.
prereqs: [erasure-decoding, tanner-graph]
see_also: [belief-propagation-decoding, ldpc-code, lt-codes, k-core, xor-filter, set-reconciliation, compressed-sensing, hypergraph]
sources:
  - paper: doi:10.1109/18.910575
    title: Michael G. Luby, Michael Mitzenmacher, M. Amin Shokrollahi and Daniel A. Spielman, Efficient erasure correcting codes, IEEE Transactions on Information Theory 47(2), 2001
    locator: The linear-time decoder that recovers a message symbol from a check node of degree one, and its analysis on random graphs
  - paper: doi:10.1109/TIT.2002.1003839
    title: Changyan Di, David Proietti, I. Emre Telatar, Thomas J. Richardson and Rüdiger L. Urbanke, Finite-length analysis of low-density parity-check codes on the binary erasure channel, IEEE Transactions on Information Theory 48(6), 2002
    locator: The definition of stopping sets and the fact that the iterative decoder fails exactly on the largest stopping set in the erased set
  - book: isbn:9780521852296
    title: Tom Richardson and Rüdiger Urbanke, Modern Coding Theory, Cambridge University Press, 2008
    locator: Chapter 3 (the peeling decoder, its equivalence with belief propagation on the BEC, stopping sets, density evolution and the threshold of the (3, 6)-regular ensemble)
---

The peeling decoder fills in erased symbols of a sparse linear code over $\mathrm{GF}(2)$. It looks for a check equation with only one unknown, solves it, puts the value into every other check that contains it, and repeats. It runs in time linear in the size of the [Tanner graph](/tanner-graph/). It is the decoder of [LT codes](/lt-codes/) and of [LDPC codes](/ldpc-code/) on the erasure channel, and it is the same as [belief propagation](/belief-propagation-decoding/) there. It stops early when the unknowns that are left form a *stopping set*, even when [Gaussian elimination](/gaussian-elimination/) would still succeed.

## In plain words

You have a set of puzzles. Each puzzle says: these few hidden numbers XOR to this value. Most puzzles have two or more hidden numbers, so you cannot solve them yet. But if one puzzle has only one hidden number left, its value is the answer. Write it down. Then go to every other puzzle that uses that number, take it out, and fix the value. Some of those puzzles now have one hidden number left, so you can solve them next.

You keep going until every number is found or no puzzle has exactly one hidden number. In the second case the decoder is stuck. Each hidden number that is left sits in puzzles with at least two hidden numbers. Each puzzle is touched only a few times, so the work is small.

## The problem

**Notation.** A binary [linear code](/linear-code/) $[n, k, d]_2$ has an $(n - k) \times n$ [parity-check matrix](/parity-check-matrix/) $H$ with $H c^T = 0$ for each codeword $c$. The Tanner graph has a variable node for each position and a check node for each row, with an edge where $H$ has a 1. $m$ is the number of edges and $r$ the number of checks.

**Channel.** On the [binary erasure channel](/binary-erasure-channel/) each symbol arrives intact or is erased, and the decoder knows which. A symbol can be one bit or a whole packet: the same XORs act on each bit of the packet.

**Input.** After the known symbols are moved to the right side, each check $c$ is a set $C[c]$ of erased positions and a value $\mathit{val}[c]$, the XOR of the erased symbols in $C[c]$. The same form describes an LT code: each received encoded symbol is a check whose set is its neighbors among the source symbols.

**Output.** The values of as many erased symbols as the checks determine by single substitutions, and the set of symbols that are left unknown.

## The algorithm

```pseudo id=main
PEEL(V, C, val)                     ▷ C[c]: unknowns of check c, val[c]: their XOR
L1  x[v] ← ? for each v ∈ V
L2  Q ← {c : |C[c]| = 1}
L3  while Q ≠ ∅ do
L4      remove some c from Q
L5      if |C[c]| ≠ 1 then continue          ▷ the entry is out of date
L6      v ← the only element of C[c]
L7      x[v] ← val[c]
L8      for each check c' with v ∈ C[c'] do    ▷ c itself included
L9          C[c'] ← C[c'] \ {v};  val[c'] ← val[c'] ⊕ x[v]
L10         if |C[c']| = 1 then add c' to Q
L11 return x                         ▷ the unknowns left form a stopping set
```

Line L8 needs, for each variable, the list of its checks. Line L9 keeps each $C[c']$ as a set or as a counter plus the XOR of the indices that are left. With the counter form, the only element in line L6 is that XOR, which is how invertible Bloom lookup tables find the last key in a cell.

A **stopping set** is a nonempty set $S$ of variables such that each check with a neighbor in $S$ has at least two neighbors in $S$. The union of two stopping sets is a stopping set, so each set of erased positions contains a largest stopping set (possibly empty).

## Example

Take the [Hamming code](/hamming-code/) $[7, 4, 3]$ whose check $r$ contains the positions $j$ where bit $r$ of $j + 1$ is 1:

$$c_0: \{0, 2, 4, 6\}, \qquad c_1: \{1, 2, 5, 6\}, \qquad c_2: \{3, 4, 5, 6\}.$$

The codeword $(1, 1, 1, 0, 0, 0, 0)$ arrives as $y = (?, 1, 1, ?, 0, ?, 0)$. Moving the known symbols to the right side gives $C[c_0] = \{0\}$ with $\mathit{val} = y_2 \oplus y_4 \oplus y_6 = 1$, $C[c_1] = \{5\}$ with $\mathit{val} = y_1 \oplus y_2 \oplus y_6 = 0$, and $C[c_2] = \{3, 5\}$ with $\mathit{val} = y_4 \oplus y_6 = 0$.

| step | check taken | resolved | $C[c_0]$, val | $C[c_1]$, val | $C[c_2]$, val | $Q$ |
|---|---|---|---|---|---|---|
| start | | | $\{0\}$, 1 | $\{5\}$, 0 | $\{3, 5\}$, 0 | $c_0, c_1$ |
| 1 | $c_0$ | $x_0 = 1$ | $\{\}$, 0 | $\{5\}$, 0 | $\{3, 5\}$, 0 | $c_1$ |
| 2 | $c_1$ | $x_5 = 0$ | $\{\}$, 0 | $\{\}$, 0 | $\{3\}$, 0 | $c_2$ |
| 3 | $c_2$ | $x_3 = 0$ | $\{\}$, 0 | $\{\}$, 0 | $\{\}$, 0 | |

The output is $(1, 1, 1, 0, 0, 0, 0)$. Now erase positions 4, 5 and 6 instead. Then $C[c_0] = \{4, 6\}$, $C[c_1] = \{5, 6\}$ and $C[c_2] = \{4, 5, 6\}$: no check has one unknown, and $\{4, 5, 6\}$ is a stopping set. Peeling stops at once. Gaussian elimination still succeeds, because the columns of $H$ at 4, 5 and 6 (the binary forms of 5, 6 and 7) are independent. Over all 128 erasure patterns of this code, 57 are decodable by Gaussian elimination and peeling decodes 54 of them; the other three are $\{2, 4, 6\}$, $\{2, 5, 6\}$ and $\{4, 5, 6\}$.

## Correctness

Three facts hold for every order of the queue. Each value written in line L7 is right, because line L9 keeps the invariant that $\mathit{val}[c]$ is the XOR of the true values of the unknowns in $C[c]$. When the loop ends, no check has exactly one unknown, so the unknowns left are empty or a stopping set. And no variable of a stopping set $S$ inside the erased set is ever resolved, because each check that touches $S$ keeps at least two unknowns of $S$. So the decoder stops exactly at the largest stopping set inside the erased set, and it decodes everything if and only if the erased set contains no stopping set. The full proof is in [the correctness proof](proofs/correctness.md).

Every output of peeling is also the output of maximum likelihood decoding, since each step uses a true equation. The converse fails, as the example shows.

## Complexity

Building the variable-to-check lists takes $\Theta(m + r)$ time. Each check enters $Q$ at the start or when its set drops to size 1, and a set drops to size 1 at most once, so $Q$ receives at most $2r$ entries. Each variable is resolved at most once, and then line L8 visits its checks once. So lines L8 to L10 run at most $m$ times in total.

- The time is $\Theta(m + r)$ operations on symbols. With packets of $s$ bits, each XOR costs $\Theta(s / w)$ on a machine with words of $w$ bits.
- The extra space is $\Theta(m + r)$ for the adjacency lists and the queue.
- For LDPC codes with bounded degrees, $m = \Theta(n)$, so the decoder is linear in the length. For LT codes with the robust soliton distribution, $m = \Theta(k \log(k/\delta))$.

## Properties

- **Same as belief propagation on the BEC.** On the erasure channel each message of belief propagation is a known bit or an erasure. A check sends a known bit to a variable exactly when all its other neighbors are known. So belief propagation resolves exactly the same variables as peeling (the tests check this on all patterns of small codes).
- **Order independent.** The final set of unknowns is the largest stopping set in the erased set, whatever the order of $Q$.
- **No guessing.** Peeling never outputs a wrong value on an erasure channel. It fails by stopping, and the caller sees which symbols are missing.
- **Thresholds.** On a long random code from an LDPC ensemble with edge degree distributions $\lambda$ and $\rho$, the fraction of erased messages after $\ell$ rounds follows density evolution, $x_\ell = \varepsilon\, \lambda(1 - \rho(1 - x_{\ell - 1}))$. Peeling succeeds when $\varepsilon$ is below the threshold. For the $(3, 6)$-regular ensemble of rate 1/2 the threshold is about 0.4294, while the capacity limit is 0.5 (Richardson and Urbanke, Chapter 3).

## Variants and improvements

- **Inactivation decoding.** When peeling stops, mark one unknown as *inactive* (treat it as a symbol variable), and continue. At the end, solve the small dense system for the inactive unknowns by Gaussian elimination and substitute back. This gives maximum likelihood decoding at a cost close to peeling. RaptorQ (RFC 6330) decodes this way.
- **Peeling in hashing and sketches.** The same loop finds the 2-core of a [hypergraph](/hypergraph/), which is the [k-core](/k-core/) with $k = 2$. It builds [XOR filters](/xor-filter/) and cuckoo hash tables, and lists the contents of invertible Bloom lookup tables for [set reconciliation](/set-reconciliation/). Some sparse recovery schemes in [compressed sensing](/compressed-sensing/) hash the nonzero entries into cells and peel the cells that hold only one.
- **LT and Raptor decoding.** For [LT codes](/lt-codes/) the checks are the received symbols; the set $Q$ is called the *ripple*. [Raptor codes](/raptor-codes/) run peeling on the LT part and a second decoder on the precode.
- **Guess and peel.** Guess the value of one unknown in a stopping set, peel, and check for a contradiction. Each guess doubles the work, so it is useful for a few guesses only.

## When to use it

Use peeling for sparse codes on erasure channels when speed matters more than the last few percent of rate: LDPC codes for packet loss, LT codes, and the first stage of Raptor decoding. Use it in hashing structures that are built to be peelable. If peeling stops and the data is still needed, fall back to inactivation decoding or [Gaussian elimination](/gaussian-elimination/) on what is left. Do not use it for dense codes such as Reed-Solomon codes: every check has many unknowns, so it stops at once.

## Pitfalls

- **Stale queue entries.** A check can be in $Q$ and lose its last unknown through another check before it is taken. Line L5 must skip it. Without the test, line L6 reads from an empty set.
- **Forgetting the value update.** Line L9 must XOR $x[v]$ into $\mathit{val}[c']$ as well as remove $v$ from $C[c']$. Removing $v$ alone writes wrong values in later steps and gives no sign of the error.
- **Scanning for degree one.** Searching all checks for one with a single unknown, in place of keeping $Q$ in line L10, makes the decoder quadratic.
- **Errors in the input.** Peeling assumes erasures only. A wrong received symbol spreads through line L9 into many values. A check that ends with no unknowns and a nonzero value shows that the input had an error.
- **Reading a stop as failure of the code.** Line L11 can return unknowns that maximum likelihood decoding would find. Report the stopping set, or hand it to Gaussian elimination.

## Implementations

## History

Zyablov and Pinsker studied this decoder for low-density codes on the erasure channel in 1974. Luby, Mitzenmacher, Shokrollahi, Spielman and Stemann analyzed it on random irregular graphs in 1997 and designed degree distributions (Tornado codes) for which it comes as close to capacity as desired. Luby used it as the decoder of LT codes in 2002. Di, Proietti, Telatar, Richardson and Urbanke named stopping sets in 2002 and used them for the exact finite-length analysis on the erasure channel.

## References
