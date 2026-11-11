---
tag: DSEB3X
kind: algorithm
slug: bgw-protocol
name: BGW protocol
aliases:
- Ben-Or-Goldwasser-Wigderson protocol
area: cryptography/protocols
level: research
summary: Secure multiparty computation of an arithmetic circuit on Shamir shares of degree t. Addition is local; each product has degree 2t and needs a degree reduction. Perfect security for t < n/2.
solves: [secure-multiparty-computation]
model: word-ram
complexity:
  vars: {n: the number of parties, t: the threshold, m: the number of multiplication gates, k: the number of linear gates}
  time: {worst: Θ(m n² t + k n), average: Θ(m n² t + k n), best: Θ(m n² t + k n)}
  space: {extra: Θ(n (m + k))}
properties: {deterministic: false, randomized: true}
history:
  year: 1988
  people: [Michael Ben-Or, Shafi Goldwasser, Avi Wigderson]
  note: Ben-Or, Goldwasser and Wigderson gave the protocol at STOC 1988, with perfect security for t < n/2 semi-honest and t < n/3 malicious parties. Asharov and Lindell gave a full proof in 2017.
prereqs: [shamir-secret-sharing, semi-honest-model, lagrange-interpolation]
see_also: [gmw-protocol, yao-garbled-circuits, secure-multiparty-computation, malicious-adversary-model, reed-solomon-code, berlekamp-welch, verifiable-secret-sharing, byzantine-resilience-bound]
sources:
  - paper: doi:10.1145/62212.62213
    title: "Michael Ben-Or, Shafi Goldwasser and Avi Wigderson, Completeness theorems for non-cryptographic fault-tolerant distributed computation, STOC 1988, pages 1 to 10"
    locator: the protocol on Shamir shares, the degree reduction, and the bounds t < n/2 (semi-honest) and t < n/3 (malicious)
  - paper: doi:10.1007/s00145-015-9214-4
    title: "Gilad Asharov and Yehuda Lindell, A full proof of the BGW protocol for perfectly secure multiparty computation, Journal of Cryptology 30(1), 2017, pages 58 to 151"
    locator: the full protocol and proofs for the semi-honest and malicious cases
  - paper: doi:10.1145/277697.277716
    title: "Rosario Gennaro, Michael O. Rabin and Tal Rabin, Simplified VSS and fast-track multiparty computations with applications to threshold cryptography, PODC 1998, pages 101 to 111"
    locator: the degree reduction by resharing the products and combining with Lagrange coefficients
  - paper: doi:10.1145/62212.62214
    title: "David Chaum, Claude Crépeau and Ivan Damgård, Multiparty unconditionally secure protocols, STOC 1988, pages 11 to 19"
    locator: the parallel result for information-theoretic MPC with an honest majority
  - paper: doi:10.1007/3-540-46766-8_34
    title: "Donald Beaver, Efficient multiparty protocols using circuit randomization, CRYPTO 1991, LNCS 576, pages 420 to 432"
    locator: multiplication triples, which replace the online degree reduction by two openings
  - paper: doi:10.1561/3300000019
    title: "David Evans, Vladimir Kolesnikov and Mike Rosulek, A pragmatic introduction to secure multi-party computation, Foundations and Trends in Privacy and Security 2(2-3), 2018"
    locator: Section 3.3 (the BGW protocol)
---

The BGW protocol, by Ben-Or, Goldwasser and Wigderson (1988), lets $n$ parties compute an arithmetic circuit over a prime field on their private inputs, with no computational assumption at all. Every wire value is held as a [Shamir sharing](/shamir-secret-sharing/) of degree $t$: each party holds one point of a random polynomial whose constant term is the value. Addition and multiplication by a constant are local. Multiplying the shares point by point gives a polynomial of degree $2t$, so each multiplication gate ends with a *degree reduction*, one round of interaction that brings the degree back to $t$. The protocol is perfectly secure against $t < n/2$ [semi-honest](/semi-honest-model/) parties, and with error correction against $t < n/3$ [malicious](/malicious-adversary-model/) parties, and both bounds are optimal. This page gives the semi-honest protocol with both the original degree reduction and the simpler one of Gennaro, Rabin and Rabin (1998), and proves it correct.

**Notation.** $\mathbb{F}_p$ is a prime field with $p > n$. Party $P_i$ has the evaluation point $i$. $[v]_i$ is $P_i$'s share of $v$: $[v]_i = f(i)$ for a polynomial $f$ of degree at most $t$ with $f(0) = v$. $\lambda_1, \ldots, \lambda_n$ are the [Lagrange](/lagrange-interpolation/) coefficients at 0 for the points $1, \ldots, n$, so $g(0) = \sum_i \lambda_i g(i)$ for every $g$ of degree less than $n$. $m$ is the number of multiplication gates and $k$ the number of linear gates.

## In plain words

Each secret number is hidden in a random curve of low degree $t$: the secret is where the curve meets zero, and each party holds one other point on it. Any $t$ parties together see only random numbers, but $t + 1$ points fix the curve and the secret.

Adding two secrets is easy: each party adds its two points, and the result lies on the sum of the two curves. Multiplying is harder. The products of the points lie on the product curve, which meets zero at the right value, but its degree is now $2t$. Repeat that and $n$ points no longer fix the curve.

So after each multiplication the parties talk once to bring the degree back to $t$. Each party hides its product point in a fresh curve of degree $t$ and sends out the points. Then each party combines what it received with fixed weights.

## The problem

There are $n$ parties and an arithmetic circuit $C$ over $\mathbb{F}_p$ with addition, multiplication, and multiplication by a constant. Each input wire belongs to one party. All parties must learn the outputs, and any coalition of at most $t$ semi-honest parties must learn nothing beyond their inputs and the outputs: their joint view must be simulatable from those. This is [secure multiparty computation](/secure-multiparty-computation/) with information-theoretic security and private channels between all pairs of parties.

## The algorithm

Gates are $(op, a, b, c)$ in topological order. For a gate $\mathrm{CMUL}$, $\kappa$ is the public constant.

```pseudo id=main
BGW(C, inputs, n, t, p)
L1  for each input wire w of party P_i with value x_w: P_i picks a random f_w of degree t with f_w(0) = x_w and sends f_w(j) to P_j
L2  for each gate (op, a, b, c) in topological order:
L3      ADD: each P_j sets [c]_j ← [a]_j + [b]_j
L4      CMUL: each P_j sets [c]_j ← κ [a]_j
L5      MUL:
L6          each P_j computes h_j ← [a]_j [b]_j, a point on h = f_a f_b of degree 2t
L7          each P_i deals a sharing of 0 of degree 2t; each P_j adds the n shares it gets to h_j, giving h̃_j
L8          each P_i deals a sharing of h̃_i of degree t
L9          for each r, each P_j computes its share Σ_i A[r][i] [h̃_i]_j of (A h̃)_r and sends it to P_r
L10         each P_r reconstructs [c]_r ← (A h̃)_r from the n shares it got
L11 each party sends its shares of the output wires to all; each output is reconstructed by Lagrange interpolation at 0
```

Here $A = V P V^{-1}$, where $V$ is the $n \times n$ Vandermonde matrix with $V_{jm} = j^m$ and $P$ keeps coordinates $0, \ldots, t$ and zeroes the rest. Applied to the values of a polynomial of degree less than $n$ at $1, \ldots, n$, $A$ returns the values of the same polynomial with all coefficients above $t$ cut off. The randomization of line L7 is needed because the high coefficients of $f_a f_b$ are not random, and cutting them would leave a polynomial whose shares leak information.

**The GRR degree reduction.** Gennaro, Rabin and Rabin (1998) replace lines L7 to L10 by one step. Each $P_i$ deals a sharing of $h_i$ of degree $t$ by a polynomial $s_i$, and each $P_j$ sets

$$[c]_j \leftarrow \sum_{i=1}^n \lambda_i\, s_i(j).$$

This is a point on $\sum_i \lambda_i s_i$, a random polynomial of degree $t$ whose constant term is $\sum_i \lambda_i h_i = h(0) = v_a v_b$. It needs $n(n-1)$ field elements per multiplication instead of about $3n(n-1)$, and one round instead of three. It is the version that the code uses by default.

## Example

$n = 5$, $t = 2$, $p = 101$. The inputs are $a = 3$ and $b = 4$, shared by $f_a(x) = 3 + 2x + 5x^2$ and $f_b(x) = 4 + 7x + x^2$. The Lagrange coefficients at 0 for the points $1, \ldots, 5$ are $\lambda = (5, -10, 10, -5, 1)$. For the reduction, suppose every party reshares with $s_i(x) = h_i + x^2$ (in a real run the coefficients are random).

| Party $j$ | $[a]_j = f_a(j)$ | $[b]_j = f_b(j)$ | $h_j = [a]_j [b]_j$ | $\lambda_j$ | $[c]_j = \sum_i \lambda_i s_i(j)$ |
|---|---|---|---|---|---|
| 1 | 10 | 12 | 19 | 5 | 13 |
| 2 | 27 | 22 | 89 | $-10$ | 16 |
| 3 | 54 | 34 | 18 | 10 | 21 |
| 4 | 91 | 48 | 25 | $-5$ | 28 |
| 5 | 37 | 64 | 45 | 1 | 37 |

All values are mod 101. The points $h_j$ lie on $h = f_a f_b = 12 + 29x + 37x^2 + 37x^3 + 5x^4$, of degree $4 = 2t$, and $\sum_j \lambda_j h_j = 95 - 890 + 180 - 125 + 45 = -695 \equiv 12 = 3 \cdot 4$. Because $\sum_j \lambda_j = 1$, the new shares are $[c]_j = 12 + j^2$: the points of a polynomial of degree 2 with constant term 12. Two parties together see two points of it, which say nothing about the constant term when the reshare coefficients are random.

**The code.** The implementation evaluates 30 random circuits with $n = 5$ and $t = 2$ over $\mathbb{F}_p$ with $p = 2^{61} - 1$, in both reduction modes, compares each output with plain evaluation, and checks that every product sharing has degree at most $t$ after the reduction. It also checks the example's Lagrange coefficients, the truncation matrix $A$, the message counts, and that $t \ge n/2$ is refused.

**A malicious share.** The tests also run two attacks on local simulated parties. One wrong output share makes plain interpolation return a wrong value; with $n = 5$ and $t = 2$ the five shares then fit no polynomial of degree 2, so the error is detected. But two colluding parties at $n = 5$ can send points of $g = f + c(x-1)(x-2)$: then "$f$ with two errors" and "$g$ with one error" both explain the shares, and decoding for one error returns $g(0) = f(0) + 2c$. With $n = 7 = 3t + 1$ the test corrects any two wrong shares. The decoder in the code is brute force over subsets; [Berlekamp-Welch](/berlekamp-welch/) does the same in polynomial time.

There are no official test vectors for BGW. The code is for study only and is not constant time; it runs all parties in one process with Python's `random` module. Use a maintained framework such as MP-SPDZ for real data.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). The invariant is that every processed wire carries a sharing of its true value by a polynomial of degree at most $t$. Input sharing (line L1) sets it, and addition and multiplication by a constant keep it because a linear combination of polynomials of degree at most $t$ has degree at most $t$. For a multiplication, $h = f_a f_b$ has degree at most $2t \le n - 1$, so its $n$ points determine it and $\sum_i \lambda_i h(i) = h(0) = v_a v_b$. In the original reduction, adding sharings of zero keeps $h(0)$, and the matrix $A$ maps the points of $\tilde h$ to the points of its truncation to degree $t$, which has the same constant term. In the GRR reduction, the new shares are points on $\sum_i \lambda_i s_i$, which has degree $t$ and constant term $h(0)$. The output step interpolates a polynomial of degree $t$ from $n > t$ points.

**Security against $t$ semi-honest parties.** A coalition of $t$ parties sees at most $t$ points of each sharing of degree $t$, and these are uniform and independent of the secret. In the GRR reduction, the new sharing of $c$ is uniform among the sharings of degree $t$ of $v_c$, because each $s_i$ has fresh random coefficients and at least one dealer is honest. So the simulator samples the coalition's incoming shares at random, and at the output it picks the honest parties' output shares so that they interpolate to the true output together with the coalition's shares. Asharov and Lindell (2017) give the full proof; it is perfect security, with no error and no computational assumption.

## Complexity

| Resource | Per multiplication gate (GRR) | Per multiplication gate (original) | Per linear gate |
|---|---|---|---|
| field elements sent | $n(n-1)$ | about $3n(n-1)$ | 0 |
| rounds | 1 | 3 | 0 |
| local work, all parties | $\Theta(n^2 t)$ | $\Theta(n^2 t + n^3)$ | $\Theta(n)$ |

With $n - 1$ messages per input and $n(n-1)$ per output, the GRR protocol sends $\Theta(m n^2)$ field elements in total, and the rounds equal the multiplicative depth of the circuit plus two. The local work is dominated by evaluating $n$ polynomials of degree $t$ at $n$ points per multiplication.

## Properties

- **Perfect security.** No assumption is used: the adversary may have unbounded computing power. This needs private channels between every pair of parties.
- **Optimal thresholds.** $t < n/2$ for semi-honest parties and $t < n/3$ for malicious parties without broadcast are the best possible for perfect security. For $t \ge n/2$ some functions (for example AND of two bits with $n = 2$) have no information-theoretically secure protocol, and $t < n/3$ matches the bound for [Byzantine agreement](/byzantine-resilience-bound/).
- **Arithmetic, not Boolean.** Each gate is one field operation, so sums and products of large numbers are cheap; comparisons need bit decomposition and are expensive.
- **Rounds grow with depth.** Each layer of multiplications costs one round, as in [GMW](/gmw-protocol/).
- **Any number of parties.** The cost per multiplication grows as $n^2$ in this form; later protocols bring it to $O(n)$.

## Variants and improvements

- **Malicious parties, $t < n/3$.** Shares are dealt with [verifiable secret sharing](/verifiable-secret-sharing/), and the output is decoded as a [Reed-Solomon code](/reed-solomon-code/): with $n \ge 3t + 1$, $n$ points of a polynomial of degree $t$ with at most $t$ wrong ones still determine it. The multiplication step uses the same error correction to check each party's reshares. Asharov and Lindell (2017) give the complete version.
- **Malicious parties, $t < n/2$.** Rabin and Ben-Or (1989) reach an honest majority with a broadcast channel, at the price of a small error probability.
- **The CCD protocol.** Chaum, Crépeau and Damgård (1988) gave a similar result at the same STOC, for $t < n/3$ malicious parties with an exponentially small error probability.
- **Beaver triples.** Precomputed sharings of $(x, y, xy)$ turn each online multiplication into two openings (Beaver 1991). This is the base of the offline and online split in SPDZ and other modern systems.
- **Linear communication.** Damgård and Nielsen (CRYPTO 2007) use double sharings, of the same random value with degree $t$ and $2t$, so that a multiplication costs $O(n)$ field elements in total, in amortized form.
- **Packed secret sharing.** Franklin and Yung (STOC 1992) hide several secrets in one polynomial, to compute many gates at once.
- **Replicated sharing for three parties.** With $n = 3$ and $t = 1$, replicated sharing over a ring such as $\mathbb{Z}_{2^{64}}$ gives fast honest-majority MPC, as in Araki, Furukawa, Lindell, Nof and Ohara (CCS 2016).

## When to use it

Use BGW style protocols when there are three or more parties with an honest majority, when the computation is mostly additions and multiplications over a field (statistics, linear algebra, auctions), and when you do not want to rely on any computational assumption. With two parties or a dishonest majority there is no honest majority to use: choose [Yao's garbled circuits](/yao-garbled-circuits/), [GMW](/gmw-protocol/) or SPDZ, which need [oblivious transfer](/oblivious-transfer/) or another assumption. For deep circuits on a high-latency network, the rounds per multiplication layer can dominate, and a constant-round protocol may be better.

## Pitfalls

- **$t \ge n/2$.** The product of two sharings has degree $2t$, and $n$ points no longer determine it. The multiplication silently returns a wrong value. The code refuses such a $t$.
- **Truncation without randomization.** In the original method, cutting the high coefficients of $f_a f_b$ directly gives a polynomial that is not uniformly random, and the shares leak information about the inputs. Line L7 must come first.
- **Reusing randomness.** Each sharing needs fresh coefficients. Two sharings with the same coefficients above the constant term let $t$ parties take differences and learn the difference of the secrets.
- **Plain interpolation against malicious parties.** With $n = 5$ and $t = 2$, one wrong share is detected, but two colluding parties can make the output ambiguous, as the test shows. Error correction needs $n \ge 3t + 1$.
- **Field size.** The field must have more than $n$ elements, and must be large enough to hold the values without wrapping around; integer arithmetic must be encoded with care.
- **Not constant time.** The code on this page is for study only.

## Implementations

## History

Ben-Or, Goldwasser and Wigderson presented the protocol at STOC 1988, in "Completeness theorems for non-cryptographic fault-tolerant distributed computation". At the same conference, Chaum, Crépeau and Damgård gave a protocol for the same setting. Both showed that with private channels and an honest majority (two thirds for malicious parties), every function has a secure protocol with no computational assumption, a year after the computational result of [GMW](/gmw-protocol/). The paper sketched the proofs. Rabin and Ben-Or (1989) extended the malicious case to $t < n/2$ with broadcast. Gennaro, Rabin and Rabin (1998) simplified the multiplication to one resharing step with Lagrange coefficients. Asharov and Lindell published a full proof of the protocol in the Journal of Cryptology in 2017, with a complete treatment of the malicious case.

## References
