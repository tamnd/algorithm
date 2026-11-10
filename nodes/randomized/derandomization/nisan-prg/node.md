---
tag: AGXJ9C
kind: algorithm
slug: nisan-prg
name: Nisan's generator
aliases:
- Nisan's PRG for space-bounded computation
area: randomized/derandomization
level: advanced
summary: A generator with seed length O(log² n) that fools read-once branching programs of width n reading n bits. It joins outputs through pairwise independent hash functions, recursively.
solves: [pseudorandom-generation]
model: word-ram
complexity:
  vars: {k: "the bits per block, at most the word size", N: "the number of output blocks, a power of two"}
  time: {worst: Θ(k·N), average: Θ(k·N), best: Θ(k·N)}
  space: {extra: Θ(N)}
properties: {in_place: false, online: true, deterministic: true, recursive: false}
history:
  year: 1992
  people: [Noam Nisan]
  note: Nisan published the generator in Combinatorica in 1992, after a conference version in 1990.
prereqs: [read-once-branching-program, pairwise-independence, universal-hash-family, pseudorandom-generator]
see_also: [randomized-logspace, rl-versus-l, sc-class, savitch-theorem, expander-walk-sampler, pseudorandom-generation, branching-program, space-complexity]
sources:
  - paper: doi:10.1007/BF01305237
    title: Noam Nisan, Pseudorandom generators for space-bounded computation, Combinatorica 12(4), 1992
    locator: the generator built from pairwise independent hash functions and the main theorem on space-bounded machines
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 21 (pseudorandom generators for space-bounded computation)
  - paper: doi:10.1006/jcss.1996.0004
    title: Noam Nisan and David Zuckerman, Randomness is linear in space, Journal of Computer and System Sciences 52(1), 1996
    locator: a different generator for space-bounded machines, built from extractors, for comparison with Nisan's generator
---

Nisan's generator stretches a seed of $O(\log^2 n)$ bits into $n$ bits that fool every [read-once branching program](/read-once-branching-program/) of width $n$ that reads them in order. Such programs model [randomized logspace](/randomized-logspace/) machines that read their random bits once, so the generator gives a deterministic simulation of these machines in space $O(\log^2 n)$. Unlike the generators for circuits, it needs no unproved assumption. It is built by doubling: the output for a seed $x$ is the output for $x$ followed by the output for $h(x)$, where $h$ is a [pairwise independent](/pairwise-independence/) hash function, and this is repeated $\log n$ times.

## In plain words

A program that uses little memory cannot remember much of what it has read. Nisan's generator uses this. It takes a short random block and a few random hash functions. It writes the block, then the hashed block. That pair is a list; the next level writes the list, then the list built from the hashed starting block with a new hash function. Each level doubles the length.

A program with little memory reads the first half and then forgets almost all of it. It keeps only its current state. The hash function mixes the two halves so well that, from the point of view of such a state, the second half looks independent of the first. So the doubled list fools the program almost as well as two independent lists would.

## The problem

Fix a block length $k$ and a field $\mathbb{F} = \mathrm{GF}(2^k)$. A *read-once branching program* of width $w$ and length $N$ has $N + 1$ layers of $w$ states. At step $t$ it reads block $t$, an element of $\mathbb{F}$, and moves from its state in layer $t - 1$ to a state in layer $t$. At the end it accepts or rejects. A bit-level program of width $w$ that reads $n$ bits once is a program of this kind with $N = \lceil n/k \rceil$, by grouping $k$ bits into a block.

The goal is a map $G : \{0,1\}^d \to \mathbb{F}^N$ with a short seed $d$, such that for every such program $P$, $|\Pr[P(G(U_d)) = 1] - \Pr[P(U) = 1]| \le \varepsilon$, where $U$ is $N$ uniform blocks. This is the space-bounded case of [pseudorandom generation](/pseudorandom-generation/).

## The algorithm

The seed is a block $x \in \mathbb{F}$ and $\ell$ hash functions $h_i(y) = a_i y + b_i$ with $a_i, b_i \in \mathbb{F}$, so it has $k(2\ell + 1)$ bits. The recursive definition is $G_0(x) = x$ and $G_i(x) = G_{i-1}(x) \circ G_{i-1}(h_i(x))$, where $\circ$ joins two lists and $G_{i-1}$ uses $h_1, \ldots, h_{i-1}$. Unrolled, block $j$ is $h_1^{j_1} \circ \cdots \circ h_\ell^{j_\ell}(x)$, where $j_i$ is bit $i$ of $j$ from the low end and $h^0$ is the identity. The loop below computes all blocks with one field operation each.

```pseudo id=main
NISAN(x, h_1, …, h_ℓ)                     ▷ x ∈ GF(2^k), h_i(y) = a_i·y + b_i
L1  B[0] ← x
L2  for j ← 1 to 2^ℓ − 1 do
L3      i ← 1 + (the number of trailing zero bits of j)
L4      B[j] ← h_i(B[j − 2^(i−1)])         ▷ one multiplication in GF(2^k)
L5  return B[0] ∘ B[1] ∘ … ∘ B[2^ℓ − 1]
```

Line L3 picks the lowest set bit of $j$. Clearing it gives an earlier index $j - 2^{i-1}$, and applying $h_i$ to that block gives block $j$.

## Example

Take $k = 2$ and $\mathbb{F} = \mathrm{GF}(4)$ built with $t^2 + t + 1$, so the elements are $0, 1, 2 = t, 3 = t + 1$, and $2 \cdot 3 = t^2 + t = 1$. Take $\ell = 3$, $x = 1$, $h_1(y) = 2y + 1$, $h_2(y) = 3y$ and $h_3(y) = 2y + 2$.

| $j$ | bits $j_3 j_2 j_1$ | $i$ | computation | $B[j]$ |
|---|---|---|---|---|
| 0 | 000 | | $x$ | 1 |
| 1 | 001 | 1 | $h_1(B[0]) = 2 + 1$ | 3 |
| 2 | 010 | 2 | $h_2(B[0]) = 3$ | 3 |
| 3 | 011 | 1 | $h_1(B[2]) = 2 \cdot 3 + 1 = 1 + 1$ | 0 |
| 4 | 100 | 3 | $h_3(B[0]) = 2 + 2$ | 0 |
| 5 | 101 | 1 | $h_1(B[4]) = 0 + 1$ | 1 |
| 6 | 110 | 2 | $h_2(B[4]) = 0$ | 0 |
| 7 | 111 | 1 | $h_1(B[6]) = 0 + 1$ | 1 |

The seed has $2 \cdot 7 = 14$ bits and the output has $2 \cdot 8 = 16$ bits. The stretch is small at this size; the seed grows like $\ell$ and the output like $2^\ell$.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It has two parts.

1. *The loop computes $G_\ell$.* By induction on $j$, $B[j] = h_1^{j_1} \circ \cdots \circ h_\ell^{j_\ell}(x)$, and by induction on $\ell$ this is block $j$ of the recursive definition.
2. *The generator fools the programs.* For a program of width $w$ and length $N = 2^\ell$, and every $\varepsilon' > 0$,
$$\big|\Pr[P(G_\ell(U)) = 1] - \Pr[P(U) = 1]\big| \le (N-1)\Big(w^2\varepsilon' + \frac{w}{\varepsilon'^2 2^k}\Big).$$
The proof treats each half of a segment as a $w \times w$ matrix of transition probabilities. For sets $A, B \subseteq \mathbb{F}$ of densities $\alpha, \beta$, the fraction of $x$ with $x \in A$ and $h(x) \in B$ has mean $\alpha\beta$ and variance $\alpha\beta(1-\beta)/2^k$ over a random $h$, by pairwise independence. Chebyshev's inequality and a union bound over the states make every $h_i$ good except with small probability. If all are good, the error at level $i$ is at most twice the error at level $i - 1$ plus $w^2\varepsilon'$.

With $\varepsilon' = (w 2^k)^{-1/3}$ the error is at most $2N w^{5/3} 2^{-k/3}$, so $k = 3\log_2(2N/\varepsilon) + 5\log_2 w$ suffices. The seed then has $O(\log N \cdot \log(Nw/\varepsilon))$ bits. For width $w \le n$, $n$ bits and $\varepsilon = 1/n$, this is $O(\log^2 n)$. The constants here are those of this proof, not Nisan's.

Nisan's paper states the result for a machine with space $S$ that uses $R$ random bits: the seed has $O(S \log R)$ bits and the error is $2^{-S}$.

## Complexity

- **Time.** Line L4 runs $2^\ell - 1 = N - 1$ times, each with one multiplication and one addition in $\mathrm{GF}(2^k)$. A multiplication by shift and reduce costs $O(k)$ word operations, or $O(1)$ when $k$ is at most the word size and a carry-less multiply is available.
- **Space.** The array $B$ has $kN$ bits. A program that consumes the blocks in order needs only the blocks on the path from the root of the recursion: block $j$ depends on the block at $j$ with its lowest set bit cleared. A stack of $\ell + 1$ blocks suffices, so a streaming version uses $O(k\ell)$ bits plus the seed. This is what the space-bounded simulation needs.
- **Random access.** Block $j$ alone costs at most $\ell$ applications of hash functions, by the closed form.

## Properties

- **Unconditional.** The theorem needs no assumption about circuits or one-way functions.
- **Deterministic.** The output is a fixed function of the seed.
- **Each block is exactly uniform.** Block $0$ is $x$. Every other block is $a_i y + b_i$ for a $b_i$ that is uniform and independent of $y$.
- **Order matters.** The proof uses the order in which the program reads the blocks: the two halves of each segment must be read one after the other.
- **Wide programs break it.** For every seed, $B[1] + B[3] = a_1(B[0] + B[2])$ and $B[5] + B[7] = a_1(B[4] + B[6])$, so $(B[1] + B[3])(B[4] + B[6]) = (B[5] + B[7])(B[0] + B[2])$. For uniform blocks this equation holds with probability about $1/2^k$. A program that checks it must remember about $4k$ bits, so it has width about $2^{4k}$, more than the theorem allows.

## Variants and improvements

- **Impagliazzo, Nisan and Wigderson (1994)** replaced the hash functions by walks on [expander graphs](/expander-walk-sampler/). The seed has the same order, $O(\log^2 n)$, and the construction extends to some other models of communication.
- **RL in SC (Nisan 1994).** The generator, with a careful search for good hash functions, puts randomized logspace in the class [SC](/sc-class/): polynomial time and polylogarithmic space at once.
- **Saks and Zhou (1999)** combined the generator with rounding of matrix powers to show that BPL is in $\mathrm{DSPACE}(\log^{3/2} n)$. This is the best known deterministic space bound for randomized logspace up to lower order factors, and it improves on the bound $\log^2 n$ that the generator gives directly, which equals [Savitch's](/savitch-theorem/) bound for nondeterminism.
- **Nisan and Zuckerman (1996)** built a generator from [extractors](/randomness-extractor/) that uses a seed of $O(S)$ bits to produce $\mathrm{poly}(S)$ bits for a machine with space $S$.
- **Smaller width or special programs.** For permutation programs, regular programs and programs of small width there are generators with shorter seeds. Seed $O(\log n)$ for general polynomial-width programs would give BPL = L; see [RL versus L](/rl-versus-l/).

## When to use it

- To derandomize a space-bounded algorithm that reads its random bits once and in order.
- To reduce the random bits of a streaming algorithm: a sketch that uses many random bits but reads them in a fixed order with small memory can draw them from the generator instead. Indyk used this for sketches based on stable distributions.
- As a lemma in proofs about space-bounded classes, such as the inclusion of BPL in SC.

## Pitfalls

- The generator is not a cryptographic generator. Programs with large memory, such as the wide program above, break it.
- The hash family must be pairwise independent. A family of the form $h(y) = ay$ alone, without the constant $b$, maps 0 to 0, and the proof fails.
- The multiplier $a_i$ may be 0. Then $h_i$ is constant and the second half repeats one value pattern. This is allowed; the proof averages over $a_i$, and the event is part of the error.
- The polynomial that defines $\mathrm{GF}(2^k)$ must be irreducible. With a reducible one, multiplication has zero divisors, and pairwise independence fails.
- Bits from the generator must be read in the order of the blocks. Feeding them to a program that reads them in another order is not covered by the theorem.

## Implementations

The Python implementation in `impl/python/nisan_prg.py` uses the standard library only. It stores a field element as an integer below $2^k$, multiplies by shift and reduce modulo a fixed irreducible polynomial for each $k \le 8$, and computes the blocks with the loop of lines L1 to L5. The tests compare it with the recursive definition, check that every block is exactly uniform, check that the hash family is pairwise independent, and compute the mean and variance of the mixing lemma exactly.

## History

Nisan presented his generator at STOC 1990, and the journal version appeared in Combinatorica in 1992. Nisan used it in 1994 to show that RL is in SC. Impagliazzo, Nisan and Wigderson (1994) gave the variant with expanders, and Saks and Zhou (1999) showed that BPL is in $\mathrm{DSPACE}(\log^{3/2} n)$. A generator with seed $O(\log n)$ for general programs is still not known.

## References
