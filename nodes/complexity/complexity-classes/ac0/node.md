---
tag: Y8YPMC
kind: definition
slug: ac0
name: AC0
aliases:
- AC^0
area: complexity/complexity-classes
level: advanced
summary: The problems decided by Boolean circuits of constant depth and polynomial size with AND and OR gates of unbounded fan-in. Addition is in AC0, but parity, majority and multiplication are not.
prereqs: [boolean-circuit, circuit-complexity]
see_also: [tc0, nc, circuit-complexity, carry-lookahead-adder, fourier-analysis-of-boolean-functions, natural-proofs-barrier, boolean-circuit, non-uniform-computation]
sources:
  - paper: doi:10.1007/BF01744431
    title: Merrick Furst, James B. Saxe and Michael Sipser, Parity, circuits, and the polynomial-time hierarchy, Mathematical Systems Theory 17(1), 13 to 27 (1984)
    locator: the theorem that parity has no constant-depth circuits of polynomial size
  - paper: doi:10.1016/0168-0072(83)90038-6
    title: Miklós Ajtai, Sigma-1-1 formulae on finite structures, Annals of Pure and Applied Logic 24(1), 1 to 48 (1983)
    locator: the independent proof of the parity lower bound
  - paper: doi:10.1145/12130.12132
    title: Johan Håstad, Almost optimal lower bounds for small depth circuits, 18th ACM Symposium on Theory of Computing, 6 to 20 (1986)
    locator: the switching lemma and the exp(Omega(n^(1/(d-1)))) bound for parity
  - paper: doi:10.1007/BF01137685
    title: Alexander A. Razborov, Lower bounds on the size of bounded depth circuits over a complete basis with logical addition, Mathematical Notes 41(4), 333 to 338 (1987)
    locator: the theorem that majority is not in AC0 with parity gates
  - paper: doi:10.1145/28395.28404
    title: Roman Smolensky, Algebraic methods in the theory of lower bounds for Boolean circuit complexity, 19th ACM Symposium on Theory of Computing, 77 to 82 (1987)
    locator: the theorem that MOD q is not in AC0 with MOD p gates for distinct primes p and q
  - paper: doi:10.1137/0213028
    title: Ashok K. Chandra, Larry Stockmeyer and Uzi Vishkin, Constant depth reducibility, SIAM Journal on Computing 13(2), 423 to 439 (1984)
    locator: constant-depth reductions among parity, majority, multiplication and related problems
  - paper: doi:10.1016/0022-0000(90)90022-D
    title: David A. Mix Barrington, Neil Immerman and Howard Straubing, On uniformity within NC1, Journal of Computer and System Sciences 41(3), 274 to 306 (1990)
    locator: DLOGTIME uniformity and the equality of uniform AC0 with first-order logic
  - paper: doi:10.1145/174130.174138
    title: Nathan Linial, Yishay Mansour and Noam Nisan, Constant depth circuits, Fourier transform, and learnability, Journal of the ACM 40(3), 607 to 620 (1993)
    locator: the Fourier concentration theorem for AC0 and the learning algorithm
  - book: isbn:9783540643104
    title: Heribert Vollmer, Introduction to Circuit Complexity, A Uniform Approach, Springer (1999)
    locator: the chapters on constant-depth circuits, uniformity and lower bounds
---

AC0 is the class of decision problems that have [Boolean circuits](/boolean-circuit/) of constant depth and polynomial size, built from AND and OR gates of unbounded fan-in and NOT gates. It models computation in constant parallel time with polynomially many processors, and it is the largest natural class for which strong unconditional lower bounds are known. Addition and comparison of $n$-bit numbers are in AC0. Parity is not, and from parity it follows that majority, multiplication and the [transitive closure](/transitive-closure/) of a graph are not in AC0 either. AC0 is the bottom level of the AC hierarchy in [NC](/nc/), and it is contained in [TC0](/tc0/).

## Definition

**Circuits.** A circuit family $\{C_n\}_{n \ge 0}$ has one circuit for each input length $n$. The circuit $C_n$ has $n$ inputs and one output. Its gates are:

- AND and OR gates of any fan-in (unbounded fan-in),
- NOT gates of fan-in 1. Without loss of generality, NOT gates are applied only to inputs, by De Morgan's laws, at no cost in depth and at most a doubling of size.

**Definition.** A language $L \subseteq \{0,1\}^*$ is in $\mathsf{AC}^0$ if there are a constant $d$, a polynomial $s$ and a family $\{C_n\}$ such that, for every $n$:

- *size*: $C_n$ has at most $s(n)$ gates (and so at most $s(n)^2 + s(n) n$ wires),
- *depth*: every path from an input to the output has at most $d$ gates,
- *gate set and fan-in*: AND and OR of unbounded fan-in, NOT of fan-in 1,
- *correctness*: $C_n(x) = 1$ if and only if $x \in L$, for every $x \in \{0,1\}^n$.

**Uniformity.** The definition above is non-uniform: the family may be arbitrary, as in [non-uniform computation](/non-uniform-computation/). Then AC0 contains undecidable unary languages, since a circuit of constant size can output a fixed bit for each $n$. The uniform version asks that the circuits be easy to describe:

- *DLOGTIME-uniform* AC0: a deterministic Turing machine with random access to its input decides in time $O(\log n)$ whether gate $g$ of $C_n$ has type $t$ and whether gate $g$ is an input of gate $h$, given $n$ in binary and the gate numbers. This is the standard uniformity for AC0. Barrington, Immerman and Straubing (1990) proved that DLOGTIME-uniform AC0 equals the languages definable in first-order logic with order and the BIT predicate.
- *P-uniform* AC0: a polynomial-time machine prints $C_n$ from $1^n$. This is a weaker condition, and too weak for classes inside [logspace](/logspace/), because the machine that builds the circuit is more powerful than the circuit.

All lower bounds below hold for non-uniform AC0, which makes them stronger. All upper bounds below are DLOGTIME-uniform.

**Depth hierarchy.** For each fixed depth, the class of problems with polynomial-size circuits of depth $d$ is strictly smaller than that of depth $d + 1$ (Sipser 1983, with exponential bounds by Håstad 1986). So the constant $d$ matters, but every fixed $d$ gives a subclass of AC0.

## Examples and non-examples

**AND, OR and pattern matching.** The AND of $n$ bits is a single gate. Whether a text of length $n$ contains a fixed pattern of length $m$ is an OR over the $n - m + 1$ positions of an AND of $m$ literals, depth $2$.

**Addition is in AC0.** Let $a$ and $b$ have bits $a_0, \ldots, a_{n-1}$ and $b_0, \ldots, b_{n-1}$. Let $g_j = a_j \land b_j$ (position $j$ generates a carry) and $p_j = a_j \lor b_j$ (position $j$ propagates a carry). The carry into position $i$ is

$$c_i = \bigvee_{j < i} \Big( g_j \land \bigwedge_{j < k < i} p_k \Big),$$

since a carry reaches position $i$ exactly when some lower position generates it and every position in between passes it on. Then the sum bit is $s_i = a_i \oplus b_i \oplus c_i$, and an XOR of three bits is a constant-size DNF. The whole circuit has constant depth, and the carries use $n(n+1)/2$ AND gates: $36$ for $n = 8$ and $528$ for $n = 32$. The [carry-lookahead adder](/carry-lookahead-adder/) in hardware computes the same carries with fan-in 2 gates in depth $O(\log n)$. Comparison of two numbers, and subtraction, are in AC0 in the same way.

**Parity is not in AC0.** The function $\oplus_n(x) = x_1 \oplus \cdots \oplus x_n$ is the basic non-example.

- At depth $2$, a DNF for parity needs $2^{n-1}$ terms. Each term must fix all $n$ variables, since a term that leaves $x_i$ free also accepts the input with $x_i$ flipped, whose parity is different. For $n = 4$ this gives $8$ terms.
- Furst, Saxe and Sipser (1984) and Ajtai (1983) proved that parity has no polynomial-size circuits of any constant depth. Håstad (1986) proved, with the switching lemma, that depth $d$ needs size $\exp(\Omega(n^{1/(d-1)}))$. This is tight up to the constant in the exponent: a tree of parity gates of fan-in $n^{1/(d-1)}$, each written as a DNF or CNF, gives depth $d$ and size $\exp(O(n^{1/(d-1)}))$.
- The proof idea: a random restriction fixes most variables at random. A DNF with short terms then becomes, with high probability, a function of few variables, which can be written as a CNF with short clauses. This lets two layers merge into one, so the depth goes down. After $d - 2$ rounds, a constant function remains, but parity restricted to its free variables is still parity, which is not constant.

**Problems that parity reduces to.** A reduction by a projection, in which each input bit of the new instance is a constant, a bit of the old one or the negation of a bit, keeps a problem out of AC0.

- *Majority.* AC0 circuits can compute "at least $k$ ones" from majority by padding the input with constants, and parity is an OR over odd $k$ of "at least $k$ ones and not at least $k + 1$ ones". So with majority gates parity has constant-depth circuits of polynomial size (see [TC0](/tc0/)), and majority is not in AC0.
- *Multiplication.* Let $k = \lceil \log_2(n+1) \rceil$, $A = \sum_i x_i 2^{ik}$ and $B = \sum_{i<n} 2^{ik}$. Block $n - 1$ of $A \cdot B$, the bits from position $(n-1)k$ to $nk - 1$, holds $\sum_i x_i$, since no lower block carries into it. Its lowest bit is the parity. For $x = 10110110$, with $k = 4$, $A = \texttt{0x1101101}$, $B = \texttt{0x11111111}$ and $A \cdot B = \texttt{0x12234455433211}$. The block at bit $28$ is $5$, the number of ones, so the parity is $1$. The construction is a projection, so multiplication of two $nk$-bit numbers is not in AC0.
- *Transitive closure.* Parity reduces to reachability in a layered graph by a projection. Layer $i$ has the vertices $(i, 0)$ and $(i, 1)$, and $(i, b)$ has an edge to $(i + 1, b \oplus x_{i+1})$. Then $(0, 0)$ reaches $(n, 1)$ exactly when the parity is $1$. So [graph reachability](/graph-reachability/) and [Boolean matrix powers](/boolean-matrix-multiplication/) are not in AC0.

**Modular gates.** AC0[$m$] adds MOD $m$ gates, which output $1$ when the number of ones among their inputs is not divisible by $m$. Parity is in AC0[2] by one gate. Razborov (1987) proved that majority is not in AC0[2], with exponential size bounds. Smolensky (1987) proved that for distinct primes $p$ and $q$, MOD $q$ is not in AC0[$p$]. Both proofs approximate each gate by a polynomial of low degree over a finite field. For a composite modulus such as $6$, no such bound is known, and the class ACC0, the union of AC0[$m$] over all $m$, is only known not to contain NEXP (Williams 2011).

**Learning and Fourier analysis.** Linial, Mansour and Nisan (1993) proved that a function computed by an AC0 circuit of size $s$ and depth $d$ has almost all of its Fourier weight on sets of size $(O(\log s))^{d}$. So AC0 functions can be learned from uniform random examples in time $n^{\mathrm{poly}(\log n)}$, a [quasi-polynomial time](/quasi-polynomial-time/) bound. See [Fourier analysis of Boolean functions](/fourier-analysis-of-boolean-functions/).

## Related definitions

- [NC](/nc/): $\mathsf{AC}^i$ allows depth $O(\log^i n)$, and $\mathsf{NC}^0 \subsetneq \mathsf{AC}^0 \subsetneq \mathsf{NC}^1$. The first inclusion is strict because the AND of $n$ bits depends on all inputs, and the second because parity is in $\mathsf{NC}^1$.
- [TC0](/tc0/): AC0 plus majority gates. It contains parity, majority, multiplication and division.
- AC0 reductions: constant-depth reductions in the sense of Chandra, Stockmeyer and Vishkin (1984), used to define completeness inside NC1 and below.
- [Circuit complexity](/circuit-complexity/): the general study, with AC0 as its main success.

## References
