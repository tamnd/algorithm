---
tag: TFPG45
kind: algorithm
slug: nisan-wigderson-generator
name: Nisan-Wigderson generator
aliases:
- NW generator
area: randomized/derandomization
level: advanced
summary: A generator that evaluates a hard function f on m seed subsets with small pairwise overlaps. If f is hard on average for circuits, no small circuit tells the output from uniform.
solves: [pseudorandom-generation]
model: word-ram
complexity:
  vars: {m: "the number of output bits", ℓ: "the size of each set, with one evaluation of f counted as ℓ steps"}
  time: {worst: Θ(m·ℓ), average: Θ(m·ℓ), best: Θ(m·ℓ)}
  space: {extra: Θ(m)}
properties: {in_place: false, online: true, deterministic: true, recursive: false}
history:
  year: 1994
  people: [Noam Nisan, Avi Wigderson]
  note: Nisan and Wigderson presented the generator at FOCS 1988, and the journal version appeared in 1994.
prereqs: [pseudorandom-generator, yao-next-bit-unpredictability, boolean-circuit, circuit-complexity]
see_also: [hardness-versus-randomness, impagliazzo-wigderson-theorem, trevisan-extractor, bpp, nisan-prg, pseudorandom-generation, hybrid-argument, reed-solomon-code]
sources:
  - paper: doi:10.1016/S0022-0000(05)80043-1
    title: Noam Nisan and Avi Wigderson, Hardness vs randomness, Journal of Computer and System Sciences 49(2), 1994
    locator: the definition of designs, the generator, the reconstruction argument and the consequences for BPP
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 20 (the Nisan-Wigderson construction, combinatorial designs and the proof)
  - paper: doi:10.1561/0400000010
    title: Salil P. Vadhan, Pseudorandomness, Foundations and Trends in Theoretical Computer Science 7(1 to 3), 2012
    locator: Chapter 7 (the Nisan-Wigderson generator and designs)
  - paper: doi:10.1145/258533.258590
    title: Russell Impagliazzo and Avi Wigderson, P = BPP if E requires exponential circuits, derandomizing the XOR lemma, 29th ACM Symposium on Theory of Computing (STOC), 1997
    locator: the use of the generator with a function made hard on average from a worst-case hard function
---

The Nisan-Wigderson (NW) generator turns a function $f$ that is hard on average for circuits into a [pseudorandom generator](/pseudorandom-generator/) for circuits. It picks $m$ subsets $S_1, \ldots, S_m$ of the seed positions, each of size $\ell$, any two of which share at most $a$ positions. Output bit $i$ is $f$ applied to the seed bits in $S_i$. If no small circuit computes $f$ with probability much above $1/2$, no small circuit tells the output from uniform. With an exponentially hard $f$, the seed has $O(\log m)$ bits, and this is the route from circuit lower bounds to [BPP](/bpp/) $=$ P. The generator may run longer than the circuits it fools, so it fits [derandomization](/hardness-versus-randomness/) but not cryptography.

## In plain words

Take a function that is hard to predict. Feed it many slices of one random seed and write down the answers. If the slices did not overlap at all, the answers would be independent coin flips that no one can predict. But the seed would have to be long.

The trick is to let the slices overlap a little. Then the seed can be short. Each slice still has most of its bits to itself. If some program could tell the answers from random coins, it could guess one answer from the earlier ones. The earlier answers depend on only a few bits of the current slice, so they are cheap to compute inside a small program. That program would then predict the hard function, which is impossible.

## The problem

Given a stretch $m$ and a class of tests, find a map $G : \{0,1\}^d \to \{0,1\}^m$ with a short seed $d$ that no circuit of size $m$ tells from uniform with advantage more than a small $\varepsilon$, and that runs in time $2^{O(d)}$. This is the complexity-theoretic form of [pseudorandom generation](/pseudorandom-generation/). The NW generator solves it under an assumption on the hardness of a function.

**Average-case hardness.** $f : \{0,1\}^\ell \to \{0,1\}$ is *$(s, \delta)$-hard* if every circuit $C$ of size at most $s$ has $\Pr_z[C(z) = f(z)] < \frac12 + \delta$ for uniform $z$.

**Designs.** $S_1, \ldots, S_m \subseteq [d]$ form an *$(\ell, a)$ design* if $|S_i| = \ell$ and $|S_i \cap S_j| \le a$ for all $i \ne j$.

## The algorithm

For a seed $y \in \{0,1\}^d$, write $y|_S$ for the bits of $y$ at the positions in $S$, in increasing order. The design below is the polynomial design over a prime field: the ground set is $\mathrm{GF}(q)^2$, so $d = q^2$, and each polynomial of degree less than $r$ gives the set of points on its graph.

```pseudo id=main
NW(y)                                   ▷ y ∈ {0,1}^d, design S_1 … S_m, function f on ℓ bits
L1  for i ← 1 to m do
L2      z ← y|S_i                       ▷ the ℓ seed bits at the positions of S_i
L3      out_i ← f(z)
L4  return out_1 … out_m

POLY-DESIGN(q, r)                       ▷ q prime, 1 ≤ r ≤ q
L5  for each polynomial p over GF(q) of degree < r do
L6      S_p ← {(α, p(α)) : α ∈ GF(q)}, with the point (α, β) numbered α·q + β
L7  return the list of all S_p
```

POLY-DESIGN gives $m = q^r$ sets of size $\ell = q$ in a ground set of size $d = q^2$, with pairwise intersections at most $a = r - 1$: two different polynomials of degree less than $r$ agree on at most $r - 1$ points.

## Example

Take $q = 3$ and $r = 2$. The nine lines $p(\alpha) = c_0 + c_1\alpha$ over $\mathrm{GF}(3)$ give nine sets of size 3 in $\{0, \ldots, 8\}$, and two lines meet in at most one point:

| $(c_0, c_1)$ | (0,0) | (0,1) | (0,2) | (1,0) | (1,1) | (1,2) | (2,0) | (2,1) | (2,2) |
|---|---|---|---|---|---|---|---|---|---|
| $S_p$ | 0,3,6 | 0,4,8 | 0,5,7 | 1,4,7 | 1,5,6 | 1,3,8 | 2,5,8 | 2,3,7 | 2,4,6 |
| $y\vert_{S_p}$ | 111 | 100 | 101 | 001 | 001 | 010 | 100 | 111 | 101 |
| $\mathrm{MAJ}$ | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 1 |

The seed is $y = y_0 \ldots y_8 = 101100110$ and $f$ is the majority of three bits. Majority is easy, so this toy is not pseudorandom; it shows only the shape. With $r = 3$ the same ground set carries 27 sets, and the generator maps 9 bits to 27 bits, with intersections at most 2.

**A non-example.** Let $f$ be the parity of its input. Then every output bit is the parity of the seed bits in one set, a linear function of $y$ over $\mathrm{GF}(2)$. With $m = 27 > d = 9$, some nonempty set of outputs has XOR 0 for every seed. The test that checks this XOR accepts the output always and a uniform string with probability $\frac12$. Parity has small circuits, so the theorem does not apply.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md).

**Theorem (Nisan and Wigderson 1994).** Let $S_1, \ldots, S_m$ be an $(\ell, a)$ design in $[d]$, and let $f : \{0,1\}^\ell \to \{0,1\}$ be $(t + (m-1)(a+1)2^a + 2, \varepsilon/m)$-hard. Then every circuit of size at most $t$ tells $\mathrm{NW}(U_d)$ from $U_m$ with advantage less than $\varepsilon$.

The proof is a *reconstruction*. A test $D$ with advantage $\varepsilon$ gives, by [Yao's theorem](/yao-next-bit-unpredictability/), a position $i$ and a predictor for output bit $i$ from bits $1, \ldots, i-1$ with success $\frac12 + p_i - p_{i-1} \ge \frac12 + \varepsilon/m$. Split the seed into $z = y|_{S_i}$, which is the input of $f$, and the other bits $w$. Fix $w$ and the random bits of the predictor to values at least as good as the average. Now each earlier output $f(y|_{S_j})$ depends only on the bits of $z$ in $S_i \cap S_j$, at most $a$ bits, so it has a circuit of size $(a+1)2^a$. Put these circuits in front of $D$: the result computes $f(z)$ with probability at least $\frac12 + \varepsilon/m$ and has size at most $t + (m-1)(a+1)2^a + 2$, which the hardness of $f$ forbids.

The design property is used only in this step, through $|S_i \cap S_j| \le a$.

**Parameters for derandomization (cited).** Nisan and Wigderson show that for $a \le \ell$ there are $(\ell, a)$ designs with $m = 2^{\Omega(a)}$ sets in a ground set of size $d = O(\ell^2/a)$, found greedily in time $2^{O(d)}$. Suppose $f \in \mathrm{E} = \mathrm{DTIME}(2^{O(\ell)})$ is $(2^{\delta\ell}, 2^{-\delta\ell})$-hard for some constant $\delta > 0$. Take $a = \Theta(\delta\ell)$ and $m = 2^{\Theta(\delta\ell)}$ with the constants chosen so that $m(a+1)2^a + m + 2 \le 2^{\delta\ell}$ and $m 2^{-\delta\ell} \le \frac1{10}$. Then the generator fools circuits of size $m$ with error $\frac1{10}$, the seed has $d = O(\ell) = O(\log m)$ bits, and it runs in time $m \cdot 2^{O(\ell)} = \mathrm{poly}(m)$. Enumerating all $2^d = \mathrm{poly}(m)$ seeds then puts BPP in P. This is the conditional result of [hardness versus randomness](/hardness-versus-randomness/).

## Complexity

- **Time.** $m$ evaluations of $f$ on $\ell$ bits, plus $m\ell$ steps to collect the bits. For $f \in \mathrm{E}$, one evaluation costs $2^{O(\ell)}$, so the whole output costs $m \cdot 2^{O(\ell)}$, which is $2^{O(d)}$ when $d = \Theta(\ell)$.
- **Design.** POLY-DESIGN costs $O(q^{r+1} r)$ field operations. The greedy design of Nisan and Wigderson costs $2^{O(d)}$ time, which is within the budget for derandomization.
- **Space.** $O(m)$ for the output, plus the space for $f$ and the design.

## Properties

- **Conditional.** The pseudorandomness needs an average-case hard $f$. Whether such an $f$ exists in E is not known; the known lower bounds for explicit functions are far smaller.
- **Black-box and with an explicit reduction.** The proof turns any distinguisher into a circuit for $f$ with a small amount of advice: the fixed bits $w$, the bits $r$ and the tables of the functions $g_j$. This is the property that [Trevisan's extractor](/trevisan-extractor/) uses.
- **Slow generator.** The generator runs in time $2^{O(d)}$, longer than the circuits it fools. That is fine for derandomization, where all seeds are enumerated anyway, but it is not a cryptographic generator.
- **Non-adaptive and parallel.** Each output bit depends on its own set only, so the bits can be computed in any order or at once.

## Variants and improvements

- **Worst-case hardness.** [Impagliazzo and Wigderson](/impagliazzo-wigderson-theorem/) (1997) start from a function in E that needs circuits of size $2^{\Omega(n)}$ in the worst case. They make it hard on average by amplification and then apply NW. Sudan, Trevisan and Vadhan (2001) do the amplification with local list decoding of Reed-Muller codes.
- **Optimal trade-offs.** Impagliazzo, Shaltiel and Wigderson, Shaltiel and Umans, and Umans gave constructions whose seed length is close to optimal for every level of hardness, not only for exponential hardness.
- **Extractors.** Trevisan (2001) saw that the proof needs nothing of $f$ but its truth table. Replacing the hard function by the encoding of a weak random source in a list-decodable code gives [Trevisan's extractor](/trevisan-extractor/). Raz, Reingold and Vadhan (2002) relaxed designs to *weak designs*, which save seed bits there.
- **Other models.** With oracle circuits, the same argument derandomizes Arthur-Merlin games under hardness for nondeterministic circuits; this is the line of Klivans and van Melkebeek.

## When to use it

- To prove conditional derandomization results: from a hard function in E to BPP $=$ P or to a subexponential simulation, depending on the hardness.
- To build extractors whose analysis is a reconstruction argument.
- As a template: any proof of the form "a distinguisher gives a small circuit for $f$" can follow the same steps.

## Pitfalls

- The function must be hard *on average*, with a success bound close to $1/2$. Worst-case hardness alone is not enough; it must first be amplified.
- The hardness must hold for circuits of size larger than the tests, by the term $(m-1)(a+1)2^a$. If $a$ is large this term is large, so the design must keep $a$ small, about $\log m$.
- The loss of a factor $m$ in the advantage comes from the hybrid argument. The function must be hard with advantage $\varepsilon/m$, not $\varepsilon$.
- A polynomial design needs $r \le q$. For $r > q$, different coefficient lists can give the same function on $\mathrm{GF}(q)$, and two sets can be equal.
- The proof is non-uniform: it fixes good values of $w$ and $r$. It shows that circuits cannot break the generator, not that a uniform algorithm cannot.

## Implementations

The Python implementation in `impl/python/nisan_wigderson_generator.py` uses the standard library only. It builds polynomial designs over a prime field, evaluates the generator, and builds the circuit $C$ of the reconstruction step as a Python function for a given position, fixed seed bits and fixed random bits. The tests check the design property, compute the hybrid probabilities $p_i$ exactly, and check that the average success of $C$ over all fixings is exactly $\frac12 + p_i - p_{i-1}$.

## History

Nisan and Wigderson presented the generator at FOCS 1988 under the title "Hardness vs. randomness", and the journal version appeared in 1994. It followed the cryptographic generators of Blum, Micali and Yao, but used a weaker assumption and a generator that may run longer than the tests. Babai, Fortnow, Nisan and Wigderson (1993) used it with worst-case to average-case reductions. Impagliazzo and Wigderson (1997) reached BPP $=$ P from worst-case exponential hardness, and Trevisan (2001) used the construction for extractors.

## References
