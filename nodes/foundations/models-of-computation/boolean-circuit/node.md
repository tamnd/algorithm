---
tag: F2PHTH
kind: model
slug: boolean-circuit
name: Boolean circuit
aliases:
- logic circuit
- combinational circuit
area: foundations/models-of-computation
level: core
summary: Directed acyclic graph of AND, OR and NOT gates; the non-uniform model for size and depth.
prereqs: [asymptotic-notation, logarithms]
see_also: [non-uniform-computation, p-poly, circuit-complexity, circuit-value-problem, circuit-sat, nc, ac0, branching-program]
sources:
  - book: isbn:9780521424264
    title: "Sanjeev Arora and Boaz Barak, Computational Complexity: A Modern Approach"
    locator: Chapter 6 (Boolean circuits, P/poly, uniformity, Karp-Lipton, the counting bound, NC and AC), Chapter 7 (BPP is in P/poly) and Chapter 14 (circuit lower bounds, parity and AC0, monotone circuits for clique)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 9.3, Circuit complexity (circuits of size O(t(n)^2) for one-tape time t(n), and the NP-completeness of circuit satisfiability)
  - paper: doi:10.1002/j.1538-7305.1949.tb03624.x
    title: Claude E. Shannon, The synthesis of two-terminal switching circuits, Bell System Technical Journal 28(1) (1949)
    locator: pp. 59 to 98 (the counting argument for almost all functions)
  - paper: "O. B. Lupanov, On a method of circuit synthesis, Izvestiya VUZ, Radiofizika 1 (1958)"
    locator: the upper bound (1 + o(1)) 2^n / n
  - paper: doi:10.1145/322123.322138
    title: Nicholas Pippenger and Michael J. Fischer, Relations among complexity measures, Journal of the ACM 26(2) (1979)
    locator: pp. 361 to 381 (oblivious simulation and circuits of size O(T log T))
  - paper: "Philip M. Spira, On time-hardware complexity tradeoffs for Boolean functions, Proceedings of the 4th Hawaii International Symposium on System Sciences (1971)"
    locator: pp. 525 to 527 (depth reduction of formulas)
  - paper: doi:10.1016/0022-0000(89)90037-8
    title: David A. Barrington, Bounded-width polynomial-size branching programs recognize exactly those languages in NC1, Journal of Computer and System Sciences 38(1) (1989)
    locator: pp. 150 to 164
  - paper: doi:10.1016/0168-0072(83)90038-6
    title: Miklos Ajtai, Sigma-1-1 formulae on finite structures, Annals of Pure and Applied Logic 24(1) (1983)
    locator: pp. 1 to 48
  - paper: doi:10.1007/BF01744431
    title: Merrick Furst, James B. Saxe and Michael Sipser, Parity, circuits, and the polynomial-time hierarchy, Mathematical Systems Theory 17 (1984)
    locator: pp. 13 to 27 (a superpolynomial bound for parity in constant depth)
  - paper: doi:10.1145/12130.12132
    title: Johan Hastad, Almost optimal lower bounds for small depth circuits, Proceedings of the 18th ACM Symposium on Theory of Computing (STOC 1986)
    locator: pp. 6 to 20 (the bound exp(Omega(n^(1/(d-1)))) for parity)
  - paper: doi:10.1145/3519935.3519976
    title: Jiatu Li and Tianqi Yang, 3.1n - o(n) circuit lower bounds for explicit functions, Proceedings of the 54th ACM Symposium on Theory of Computing (STOC 2022)
    locator: pp. 1180 to 1193
---

A Boolean circuit is a directed acyclic graph whose sources are the input bits and whose other nodes are gates that compute AND, OR or NOT. It computes a function from $\{0,1\}^n$ to $\{0,1\}^m$ for one fixed $n$, so a program for inputs of all sizes is a family of circuits, one for each $n$. The cost of a circuit is its size (the number of gates) and its depth (the length of the longest path). The model is [non-uniform](/non-uniform-computation/). It is the model of parallel time and of hardware, and the setting of [circuit complexity](/circuit-complexity/): a counting argument that goes back to Shannon (1949) shows that almost every function of $n$ bits needs about $2^n/n$ gates, but no explicit function is known to need more than a small constant times $n$.

## The machine

A **Boolean circuit** $C$ with $n$ inputs and $m$ outputs is a directed acyclic graph with these parts.

- There are $n$ **input nodes** with no incoming edge. They are labeled $x_1, \dots, x_n$.
- Each other node is a **gate**. It is labeled AND, OR or NOT. A NOT gate has one incoming edge. An AND or OR gate has two incoming edges (bounded fan-in) or any number (unbounded fan-in).
- There are $m$ **output nodes**, each one an input node or a gate.

The edges leaving a node can go to any number of gates (the fan-out is not limited). On an input $x \in \{0,1\}^n$, each input node takes its bit, and each gate takes the AND, OR or NOT of the values on its incoming edges. The value of the circuit is the vector of the values of the output nodes. This defines a function $C : \{0,1\}^n \to \{0,1\}^m$. Because the graph has no cycle, the values are defined by induction along a topological order.

A **formula** is a circuit in which each gate has fan-out at most 1. The leaves are labeled by variables, and one variable may label many leaves, so the graph is a tree (a forest when there are several outputs).

**Circuit families.** A circuit works for one input length. To decide a language $L \subseteq \{0,1\}^*$, one uses a family $\mathcal{C} = (C_n)_{n \ge 0}$, where $C_n$ has $n$ inputs and one output, and $C_{|x|}(x) = 1$ exactly when $x \in L$.

**Uniformity.** A family is **uniform** when a fixed algorithm builds $C_n$ from $n$. For example, a family is *log-space uniform* if a Turing machine with a work tape of $O(\log n)$ cells, given $1^n$, writes down a description of $C_n$. A family is **non-uniform** when there is no such requirement: each $C_n$ can be chosen without a rule that connects it to $C_{n+1}$.

## What it counts

- **Size** $|C|$: the number of gates. Some texts count the edges instead. With fan-in at most 2, each edge enters a gate and each gate has one or two incoming edges, so the number of edges is between the number of gates and twice that number.
- **Depth**: the number of edges on a longest path from an input node to an output node. This is the time of the circuit in the model of parallel computation, in which all gates of one layer work at the same time.
- **Fan-in**: bounded (2) or unbounded. Replace a gate of fan-in $k \ge 2$ by a balanced tree of $k - 1$ gates of fan-in 2 and depth $\lceil \lg k \rceil$. The new circuit has at most as many gates as the old one has edges, and its depth is at most $\lceil \lg K \rceil$ times the old depth, where $K$ is the largest fan-in. A circuit of polynomial size has $K$ at most polynomial, so the size stays polynomial and the depth grows by a factor of $O(\log n)$. This is why $\mathsf{AC}^k \subseteq \mathsf{NC}^{k+1}$.
- **The basis** is the set of gate types. AND, OR and NOT is the standard one. With another finite complete basis of bounded fan-in, such as NAND alone, the size and the depth change by a constant factor, because each gate of one basis is a function of a bounded number of inputs and a circuit of constant size computes it in the other basis.

For a function $f$ on $n$ bits, $S(f)$ is the least size of a circuit that computes $f$. For a family, the size is a function $s(n)$ of $n$.

## Relation to other models

- **Turing machine.** A one-tape [Turing machine](/turing-machine/) that decides $L$ in time $T(n) \ge n$ gives a circuit family for $L$ of size $O(T(n)^2)$: the circuit computes the table of the configurations, row by row, and each cell of a row is a fixed function of three cells of the row before (Sipser, Section 9.3). Pippenger and Fischer (1979) reduced the size to $O(T(n) \log T(n))$ for multitape machines, by first making the machine oblivious. This is the basis of the proofs that $\mathsf{P} \subseteq \mathsf{P/poly}$ and that the [circuit value problem](/circuit-value-problem/) is complete for $\mathsf{P}$ (Arora and Barak, Chapter 6). The other direction fails without uniformity.
- **Non-uniformity gives more power.** A family of circuits of size $O(n)$ can decide an undecidable language. Let $H \subseteq \mathbb{N}$ be the set of the numbers $n$ such that the $n$-th Turing machine halts on the empty input, and let $L = \{1^n : n \in H\}$. This language is undecidable (see the [halting problem](/halting-problem/)). Leave out the empty string and take $n \ge 1$. Let $C_n$ be an AND of its $n$ inputs if $n \in H$ (with $n - 1$ gates), and the constant 0 otherwise (the two gates $\neg x_1$ and $x_1 \wedge \neg x_1$). The family $(C_n)_{n \ge 1}$ decides $L$ with at most $\max(n-1, 2)$ gates in $C_n$. No algorithm needs to find the $C_n$. This is why the uniformity condition is part of the definition of a circuit family that stands for an algorithm.
- **[P/poly](/p-poly/).** The class $\mathsf{P/poly}$ is the set of languages that have a family of circuits of polynomial size, with no uniformity. It contains $\mathsf{P}$, and the languages of $\mathsf{P}$ are exactly those that have a polynomial-size family that is log-space uniform, or polynomial-time uniform (Arora and Barak, Chapter 6). See [non-uniform computation](/non-uniform-computation/) and [circuit complexity](/circuit-complexity/).
- **Parallel time.** Circuits of polynomial size and depth $O(\log^k n)$ with bounded fan-in define the class $\mathsf{NC}^k$. The same with unbounded fan-in defines $\mathsf{AC}^k$. These classes are usually defined with log-space uniform families. Without uniformity one gets the non-uniform versions, which contain undecidable languages by the example above. See [NC](/nc/) and [AC0](/ac0/).
- **Formulas.** A circuit of depth $d$ and fan-in 2 becomes a formula by copying, for each gate, the subcircuit below it, once for each of its outgoing edges. The formula has at most $2^{d+1} - 1$ nodes for each output, so depth $O(\log n)$ gives a formula of polynomial size. Conversely, every formula of size $s$ can be rebalanced to depth $O(\log s)$ (Spira, 1971), so the languages with polynomial-size formulas are those with circuits of depth $O(\log n)$.
- **[Branching programs](/branching-program/)** are another non-uniform model. A branching program of size $s$ can be simulated by a circuit of depth $O(\log^2 s)$, and branching programs of width 5 and polynomial size decide exactly the languages in $\mathsf{NC}^1$ (Barrington, 1989).
- **Problems.** [Circuit-SAT](/circuit-sat/) asks if a given circuit has an input with output 1. It is NP-complete.

## Known results in the model

### Examples

**The XOR of two bits** is $(a \vee b) \wedge \neg (a \wedge b)$. It has 4 gates (an OR, an AND, a NOT and an AND) and depth 3. The table of the four inputs $(a, b)$ gives $(0,0) \mapsto 0$, $(0,1) \mapsto 1$, $(1,0) \mapsto 1$ and $(1,1) \mapsto 0$.

**The parity of $n$ bits** is the XOR of all inputs. Combine the bits in pairs, then the results in pairs, and so on. This takes $n - 1$ XOR blocks and $\lceil \lg n \rceil$ levels. With the block above, the size is $4(n-1)$ and the depth is $3 \lceil \lg n \rceil$. For $n = 8$ the size is 28 and the depth is 9.

**The AND of $n$ bits** has $n - 1$ gates and depth $\lceil \lg n \rceil$ with fan-in 2, and 1 gate and depth 1 with unbounded fan-in.

**Any function** has a circuit of size $O(n 2^n)$. Write the function as an OR of the terms for the inputs $x$ with $f(x) = 1$. Each term is an AND of $n$ literals. There are at most $2^n$ terms, each with at most $n - 1$ AND gates. The OR of the terms uses at most $2^n - 1$ gates. The NOT gates for the $n$ inputs add $n$ gates. If $f$ is identically 0, the gate $x_1 \wedge \neg x_1$ computes it with 2 gates.

**Addition** of two $n$-bit numbers has a circuit of size $O(n)$ (the [ripple-carry adder](/ripple-carry-adder/)) and depth $O(n)$. A circuit of depth $O(\log n)$ and size $O(n)$ exists too (see the [carry-lookahead adder](/carry-lookahead-adder/) and the [Brent-Kung adder](/brent-kung-adder/)).

**Non-example.** A directed graph with a cycle, such as a gate that takes its own output as an input, is not a Boolean circuit. A cycle makes the value of a gate depend on itself, and the evaluation by induction fails.

### Shannon's counting bound

**Theorem 1 (Shannon, counting part).** Let $n \ge 10$ and $s = \lfloor 2^n/(8n) \rfloor$. The number of functions $f : \{0,1\}^n \to \{0,1\}$ that have a circuit over $\{\wedge, \vee, \neg\}$ with at most $s$ gates, with fan-in at most 2, is less than $2^{2^n/2}$. So fewer than a fraction $2^{-2^n/2}$ of all $2^{2^n}$ functions have such a circuit. In particular, for each $n \ge 10$ some function needs more than $\lfloor 2^n/(8n) \rfloor$ gates, and almost all of them do.

*Proof.* We count circuits of size at most $s$ with one output, and show that this number is less than $2^{2^n/2}$. There are $2^{2^n}$ functions, and each function that has such a circuit is computed by at least one of the counted circuits.

*Step 1: the circuit as a code.* Take a circuit with at most $s$ gates. Add unused gates until it has exactly $s$ gates. This does not change the function. Order the gates $g_1, \dots, g_s$ so that each gate has its inputs among the input nodes and the earlier gates (a topological order). This is possible because the graph has no cycle. The circuit is described by these choices.

- The type of each gate $g_j$, one of three: AND, OR, NOT.
- The two nodes that $g_j$ reads, each one among the $n + s$ nodes (the $n$ inputs and the $s$ gates). A NOT gate ignores the second.
- The output node, one among the $n + s$ nodes.

*Step 2: the count.* There are at most $3 (n+s)^2$ choices for one gate. So the number of descriptions is at most $\big(3(n+s)^2\big)^s (n+s)$. Each circuit with at most $s$ gates has at least one description. So the number of functions with such a circuit is at most this number.

*Step 3: the estimate.* For $n \ge 10$ we have $2^n \ge 8 n^2$ ($1024 \ge 800$ at $n = 10$, and the left side doubles when $n$ grows by 1, while the right side grows by a factor less than 2). So $2^n/(8n) \ge n$, and since $n$ is an integer, $s \ge n$. This gives $n + s \le 2s$. Then the number of descriptions is at most $(12 s^2)^s \cdot 2s$. Take $\lg$. Then $\lg\big((12 s^2)^s \cdot 2s\big) = s(\lg 12 + 2 \lg s) + \lg(2s)$. Now $s < 2^n$ gives $\lg s < n$, and $\lg(2s) \le s$ for $s \ge 1$, and $\lg 12 < 3.59$. So the sum is less than $s(2n + 4.59)$. Since $s \le 2^n/(8n)$,

$$s(2n + 4.59) \le \frac{2^n (2n + 4.59)}{8n} \le 2^n \Big(\frac14 + \frac{0.574}{n}\Big) \le 2^n \cdot 0.3075 < 2^n/2,$$

where the second inequality uses $n \ge 10$. So the number of descriptions is less than $2^{2^n/2}$. Divide by $2^{2^n}$ to get the fraction. ∎

The proof counts only. It does not show one hard function. It shows that one exists, and that a function chosen at random is hard with probability above $1 - 2^{-2^n/2}$. This is an example of the [counting argument](/counting-argument/).

For $n = 10$ the theorem gives $s = 12$. The number of descriptions is at most $(3 \cdot 22^2)^{12} \cdot 22 < 2^{131}$, far below the bound $2^{512}$ and the $2^{1024}$ functions of 10 bits.

**What is known about the size.** Shannon (1949) gave the counting argument for switching circuits built from contacts: almost all functions of $n$ variables need about $2^n/n$ contacts. The same counting, done with more care than in Theorem 1, shows that almost all functions need circuits of size $(1 - o(1))\, 2^n/n$. The bound is tight: every function of $n$ variables has a circuit of size $(1 + o(1))\, 2^n / n$ (Lupanov, 1958). So the size of the hardest function is $\Theta(2^n/n)$, against the simple bound $O(n 2^n)$ above.

**Explicit functions.** The counting argument does not give a function with a short description that is hard. For circuits of fan-in 2 over the basis of all 16 functions of two bits, the best lower bound known for an explicit function is $3.1n - o(n)$ (Li and Yang, 2022, for an affine disperser). No function in $\mathsf{NP}$ is known to need circuits of superlinear size. A proof that some language of NP is not in $\mathsf{P/poly}$ would show $\mathsf{P} \ne \mathsf{NP}$, and it is an open problem.

**Restricted circuits.** Strong lower bounds are known when the circuit is restricted.

- *Constant depth.* Parity is not in $\mathsf{AC}^0$. Ajtai (1983) and Furst, Saxe and Sipser (1984) proved that circuits of constant depth and unbounded fan-in for parity need superpolynomial size. Hastad (1986) proved, with the switching lemma, that depth $d$ needs size $\exp\big(\Omega(n^{1/(d-1)})\big)$, which is tight up to the constant in the exponent. See [AC0](/ac0/).
- *Monotone circuits.* A circuit with AND and OR gates only computes a monotone function. Razborov (1985) proved that monotone circuits for the clique function need superpolynomial size, and later work raised the bound to exponential (Arora and Barak, Chapter 14). Some monotone functions in $\mathsf{P}$ need superpolynomial monotone circuits, so this bound does not separate $\mathsf{P}$ from $\mathsf{NP}$.

**Randomness and the polynomial hierarchy.** Every language in [BPP](/bpp/) has circuits of polynomial size, so $\mathsf{BPP} \subseteq \mathsf{P/poly}$ (Adleman 1978; see [Adleman's theorem](/adleman-theorem/) and Arora and Barak, Chapter 7). If $\mathsf{NP} \subseteq \mathsf{P/poly}$, then the polynomial hierarchy collapses to its second level (the [Karp-Lipton theorem](/karp-lipton-theorem/), Arora and Barak, Chapter 6).

### Pitfalls

- **Non-uniform families are not algorithms.** A family of linear size decides the unary halting language (above). A bound on the size of a family says that small circuits exist, not that a program can build them. State whether a class is uniform.
- **Size in gates or in edges.** With unbounded fan-in, one gate can have $n$ inputs, so gates and edges can differ by a factor of $n$. With fan-in 2 they differ by a factor of at most 2. A bound must say which one it counts.
- **Fan-in changes depth classes.** The AND of $n$ bits has depth 1 with unbounded fan-in and depth $\lceil \lg n \rceil$ with fan-in 2. A function in $\mathsf{NC}^0$ has each output bit depend on a constant number of inputs, so the AND of $n$ bits is in $\mathsf{AC}^0$ but not in $\mathsf{NC}^0$.
- **Formulas are not circuits.** A formula cannot reuse a result, so it can be much larger than a circuit for the same function. Do not apply a circuit lower bound to formulas, or a formula upper bound to circuits, without the conversion above.
- **The basis matters by a constant factor only if it is finite and complete.** A basis without NOT computes only monotone functions, and unbounded fan-in or majority gates change the depth classes, as in [TC0](/tc0/).
- **Counting gives existence, not an example.** Theorem 1 shows that hard functions exist. It does not name one, and it is not a lower bound for any explicit problem such as SAT.
## References
