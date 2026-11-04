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
see_also: [non-uniform-computation, p-poly, circuit-complexity, circuit-value-problem, circuit-sat, nc, ac0, counting-argument]
sources:
  - book: isbn:9780521424264
    title: "Sanjeev Arora and Boaz Barak, Computational Complexity: A Modern Approach"
    locator: Chapter 6, Boolean circuits
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 9.3, Circuit complexity
  - paper: "Claude E. Shannon, The synthesis of two-terminal switching circuits, Bell System Technical Journal 28(1) (1949), pages 59 to 98"
  - paper: "Philip M. Spira, On time-hardware complexity tradeoffs for Boolean functions, Proceedings of the 4th Hawaii Symposium on System Sciences, 1971"
  - paper: "David A. Barrington, Bounded-width polynomial-size branching programs recognize exactly those languages in NC1, Journal of Computer and System Sciences 38(1) (1989)"
  - paper: "Johan Hastad, Almost optimal lower bounds for small depth circuits, STOC 1986"
  - paper: "Merrick Furst, James B. Saxe and Michael Sipser, Parity, circuits, and the polynomial-time hierarchy, Mathematical Systems Theory 17 (1984)"
  - paper: "O. B. Lupanov, On a method of circuit synthesis, Izvestiya VUZ, Radiofizika 1 (1958)"
---

A Boolean circuit is a directed acyclic graph whose sources are the input bits and whose other nodes are gates that compute AND, OR or NOT. It computes a function from $\{0,1\}^n$ to $\{0,1\}^m$ for one fixed $n$, so a program for inputs of all sizes is a family of circuits, one for each $n$. The cost of a circuit is its size (the number of gates) and its depth (the length of the longest path). The model is non-uniform, and it is the model in which one proves that most functions are hard: Shannon showed by counting that most functions of $n$ bits need circuits of size about $2^n/n$.

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
- **Fan-in**: bounded (2) or unbounded. A gate of fan-in $k$ is replaced by a tree of gates of fan-in 2, which has $k - 1$ gates and depth $\lceil \lg k \rceil$. So the size grows to at most the number of edges of the original circuit, which is a factor of at most the largest fan-in in gates, and the depth is multiplied by at most $\lceil \lg k \rceil$, where $k$ is the largest fan-in. Measured in edges, the size changes by a constant factor. For a polynomial-size circuit, the size stays polynomial.
- **The basis** is the set of gate types. AND, OR and NOT is the standard one. With another finite complete basis of bounded fan-in, such as NAND alone, the size and the depth change by a constant factor, because each gate of one basis is a function of a bounded number of inputs and a circuit of constant size computes it in the other basis.

For a function $f$ on $n$ bits, $S(f)$ is the least size of a circuit that computes $f$. For a family, the size is a function $s(n)$ of $n$.

## Relation to other models

- **Turing machine.** A Turing machine that decides $L$ in time $T(n)$ gives a circuit family for $L$ of size polynomial in $T(n)$. This is the basis of the proof that $\mathsf{P} \subseteq \mathsf{P/poly}$ and of the [circuit value problem](/circuit-value-problem/) being complete for $\mathsf{P}$ (Arora and Barak, Chapter 6). The other direction fails without uniformity.
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

**What is known about the size.** Shannon (1949) proved the counting lower bound for switching circuits: almost all functions of $n$ variables need about $2^n/n$ contacts. The bound is tight for the basis $\{\wedge, \vee, \neg\}$: every function of $n$ variables has a circuit of size $(1 + o(1)) \, 2^n / n$ (Lupanov, 1958). So the size of the hardest function is $\Theta(2^n/n)$. Compare this with the simple bound $O(n 2^n)$ above. The constants in Theorem 1 are not the best possible.

**Explicit functions.** The counting argument does not give a function with a short description that is hard. For an explicit function in NP, the best lower bounds on the size of circuits that are known are linear in $n$. For restricted circuits, strong lower bounds are known: for each constant depth, a circuit with unbounded fan-in that computes parity needs exponential size (Furst, Saxe and Sipser 1984; Ajtai 1983; Hastad 1986). So parity is not in $\mathsf{AC}^0$. See [AC0](/ac0/). A proof that some language of NP is not in $\mathsf{P/poly}$ would show $\mathsf{P} \ne \mathsf{NP}$, and it is an open problem. See [circuit complexity](/circuit-complexity/) and the [Karp-Lipton theorem](/karp-lipton-theorem/).

## References
