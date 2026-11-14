---
tag: CC4R1Y
kind: algorithm
slug: signal-probability-propagation
name: Signal probability propagation
aliases:
- Parker-McCluskey signal probability
- probability polynomial with exponent suppression
area: eda/power-reliability-and-manufacturability
level: core
summary: Compute P(signal = 1) for each node from input probabilities by gate formulas. Numbers are exact only without reconvergence; Parker-McCluskey polynomials are exact but can be exponential.
model: word-ram
complexity:
  vars: {G: the number of gates, P: the number of gate input pins, n: the number of primary inputs}
  time: {worst: "O(G + P)"}
  space: {extra: "O(G + n)"}
properties: {deterministic: true, exact: false, recursive: false, online: false}
history:
  year: 1975
  people: [Kenneth P. Parker, Edward J. McCluskey]
  note: Parker and McCluskey defined the signal probability, wrote it as a polynomial in the input probabilities, and suppressed exponents to stay exact under reconvergent fanout.
prereqs: [boolean-circuit, boolean-network]
see_also: [switching-activity, transition-density, bdd-switching-activity-estimation, monte-carlo-power-estimation, model-counting, bdd-satisfy-count, cop-testability-measure, bayesian-network]
sources:
  - paper: "Kenneth P. Parker and Edward J. McCluskey, Probabilistic treatment of general combinational networks, IEEE Transactions on Computers C-24(6), 668 to 670, 1975"
    title: K. P. Parker and E. J. McCluskey, Probabilistic treatment of general combinational networks, IEEE Transactions on Computers C-24(6), 668 to 670, June 1975
    locator: the definition of signal probability and signal independence, the gate formulas, and the polynomial algorithm with exponent suppression for reconvergent fanout
  - paper: doi:10.1109/92.335013
    title: Farid N. Najm, A survey of power estimation techniques in VLSI circuits, IEEE Transactions on VLSI Systems 2(4), 446 to 455, December 1994
    locator: the section on probabilistic techniques (signal probabilities, the independence assumption and the effect of reconvergent fanout)
  - paper: doi:10.1137/0208032
    title: Leslie G. Valiant, The complexity of enumeration and reliability problems, SIAM Journal on Computing 8(3), 410 to 421, 1979
    locator: the #P-completeness of counting the satisfying assignments of a CNF formula, used in the hardness proof
  - paper: doi:10.1109/TC.1984.5009315
    title: Jacob Savir, Gary S. Ditlow and Paul H. Bardell, Random pattern testability, IEEE Transactions on Computers C-33(1), 79 to 90, 1984
    locator: the cutting algorithm, which cuts fanout branches and propagates intervals to bound the signal probabilities
---

Signal probability propagation computes, for each node $y$ of a combinational circuit, the *signal probability* $P(y = 1)$, given the probability that each primary input is 1 and assuming that the primary inputs are independent. It walks the gates in topological order and applies one formula per gate, for example $P(y) = P(a) P(b)$ for $y = \mathrm{AND}(a, b)$. With plain numbers the formulas assume that the inputs of each gate are independent, so the result is exact on circuits without reconvergent fanout and can be wrong otherwise. Parker and McCluskey (1975) carry each probability as a polynomial in the input probabilities and replace $x^k$ by $x$ after each product. That version is exact on every circuit, but the polynomials can have $2^n$ terms, and no method can avoid such a cost in general: exact signal probability is #P-hard. Signal probabilities are the base of [switching activity](/switching-activity/) estimates for power, of [transition density](/transition-density/), and of [COP](/cop-testability-measure/) testability for random test.

## In plain words

Each input wire of a circuit is on with some chance, and the inputs do not influence each other. The question is how often each wire inside the circuit is on.

For one gate this is easy if its inputs are unrelated. An AND gate is on only when both inputs are on, so you multiply the two chances. An inverter turns the chance into one minus the chance. So you go through the gates from the inputs to the outputs and fill in a number for each wire.

The trouble starts when one input feeds two paths that meet again. Then the two inputs of the meeting gate share a cause, and multiplying their chances is wrong. The exact method keeps a formula in the input chances instead of a number. When one input chance appears twice in a product, it keeps it once.

## The problem

The input is a combinational circuit $C$ with primary inputs $x_1, \ldots, x_n$ and gates $g_1, \ldots, g_G$ in topological order, each gate being BUF, NOT, AND, OR, NAND, NOR, XOR or XNOR, and a probability $p_i = P(x_i = 1)$ for each input. The inputs are random variables $X_1, \ldots, X_n$, mutually independent, with $P(X_i = 1) = p_i$. Each node $y$ computes a [Boolean function](/boolean-function/) $f_y$ of the inputs. The output is

$$ P(y) \;=\; P\big(f_y(X) = 1\big) \;=\; \sum_{x \in \{0,1\}^n} f_y(x) \prod_{i=1}^{n} p_i^{x_i} (1 - p_i)^{1 - x_i} $$

for every node $y$. The *support* $S(y)$ is the set of primary inputs in the transitive fanin of $y$. A gate has *reconvergent fanout* when two of its input pins have supports that meet; a circuit in which every node drives at most one gate pin (a *fanout-free* circuit) has none.

## The algorithm

The algorithm is one pass in topological order. It has two modes that differ only in the type of the values: numbers, or polynomials over the input probabilities with exponent suppression.

```pseudo id=main
SIGNAL-PROBABILITIES(C, p, mode)
L1  for each primary input x_i do
L2      if mode = numeric then P[x_i] ← p_i else P[x_i] ← the polynomial x_i
L3  for each gate y = kind(z_1, …, z_k) in topological order do
L4      q_j ← P[z_j] for j = 1, …, k
L5      if kind ∈ {AND, NAND} then r ← q_1 · q_2 · … · q_k
L6      if kind ∈ {OR, NOR} then r ← 1 − (1 − q_1)(1 − q_2) … (1 − q_k)
L7      if kind ∈ {XOR, XNOR} then r ← q_1, then r ← r + q_j − 2 r q_j for j = 2, …, k
L8      if kind ∈ {BUF, NOT} then r ← q_1
L9      if kind ∈ {NAND, NOR, XNOR, NOT} then r ← 1 − r
L10     P[y] ← r
L11 if mode = polynomial then
L12     for each node y do P[y] ← the value of P[y] at x_i = p_i for all i
L13 return P
```

In the polynomial mode every product of lines L5 to L7 is followed by *exponent suppression*: each monomial $c \prod_i x_i^{e_i}$ becomes $c \prod_{i : e_i \ge 1} x_i$. A polynomial is then a map from sets of inputs to integer coefficients, and the product of two monomials is the union of their sets. Line L12 evaluates the final polynomials. In the numeric mode the same formulas run on numbers, with no suppression.

## Example

**A fanout-free circuit.** Take $u = \mathrm{AND}(a, b)$, $w = \mathrm{NOT}(c)$, $y = \mathrm{OR}(u, w)$ and $z = \mathrm{XOR}(y, d)$, with $p_a = 1/2$, $p_b = 1/4$, $p_c = 3/4$ and $p_d = 1/3$. Each node drives one pin, so the numeric mode is exact.

| node | formula | value |
|---|---|---|
| $u$ | $p_a p_b$ | $1/8$ |
| $w$ | $1 - p_c$ | $1/4$ |
| $y$ | $1 - (1 - 1/8)(1 - 1/4)$ | $11/32$ |
| $z$ | $11/32 + 1/3 - 2 \cdot 11/32 \cdot 1/3$ | $43/96$ |

Summing the input probabilities over the $2^4$ vectors on which $z = 1$ gives the same $43/96$.

**A reconvergent circuit.** Take $u = \mathrm{AND}(a, b)$, $v = \mathrm{AND}(a, c)$ and $y = \mathrm{OR}(u, v)$, so $y = ab \lor ac$, and let every input have probability $1/2$. The input $a$ reaches $y$ through both $u$ and $v$.

| node | numeric mode | polynomial mode |
|---|---|---|
| $u$ | $1/4$ | $ab$ |
| $v$ | $1/4$ | $ac$ |
| $y$ | $1 - (3/4)^2 = 7/16$ | $1 - (1 - ab)(1 - ac) = ab + ac - a^2 bc \to ab + ac - abc$ |

The polynomial evaluates to $1/4 + 1/4 - 1/8 = 3/8$, which is right: $y = 1$ exactly when $a = 1$ and $b \lor c = 1$, with probability $1/2 \cdot 3/4$. The numeric mode gives $7/16$, too high by $1/16$, because it treats $u$ and $v$ as independent when both need $a = 1$. The extreme case is $y = \mathrm{AND}(a, \mathrm{NOT}(a))$: the true value is 0, and the numeric mode gives $p_a (1 - p_a)$.

## Correctness

The polynomial mode is exact on every circuit. Each gate formula of lines L5 to L9 is a polynomial identity on 0 and 1 values, so the polynomial of a node agrees with its Boolean function at every corner of the cube $\{0,1\}^n$, and suppression keeps the values at the corners. A polynomial with no exponent above 1 is fixed by its corner values, and the function $p \mapsto P(f_y(X) = 1)$ is such a polynomial with the same corner values. So they are the same polynomial.

The numeric mode is exact when no gate has reconvergent fanout. By induction in topological order, each node is a function of the inputs in its support. The fanins of a gate then depend on disjoint sets of independent inputs, so they are independent, and each gate formula is the probability law of its gate for independent inputs. With reconvergent fanout the fanins can be dependent, and the example above shows that the result can then be wrong.

Exact signal probability is #P-hard, so the exponential worst case of the polynomial mode is expected. A CNF formula $F$ over $n$ variables becomes a circuit with one OR gate per clause and one AND gate over the clauses. With every $p_i = 1/2$, $P(\text{output}) = \#F / 2^n$, so an exact signal probability gives the number of models of $F$, which is the #P-complete [model counting](/model-counting/) problem (Valiant 1979). The [full proof](proofs/correctness.md) gives the details of the three results.

## Complexity

Let $G$ be the number of gates, $P$ the number of gate input pins and $n$ the number of primary inputs.

- **Numeric mode.** Each gate with $k$ inputs costs $O(k)$ arithmetic operations, so the pass costs $O(G + P)$ operations and $O(G + n)$ space. With exact rationals the numbers grow, so a tool uses floating point.
- **Polynomial mode.** A node's polynomial has at most $2^{|S(y)|} \le 2^n$ monomials, one per subset of its support. A product of two such polynomials costs at most $4^n$ monomial products, each a set union of cost $O(n)$, so the pass costs $O(P \, n \, 4^n)$ time in the worst case and $O(G \, 2^n)$ space. A gate with small supports costs much less: the cost depends on the supports, not on $n$ alone.
- **Lower bound.** No polynomial-time algorithm computes exact signal probabilities unless every #P function is computable in polynomial time, which would give $\mathrm{P} = \mathrm{NP}$. Even deciding whether $P(y) > 0$ is [NP-complete](/np-complete/), because it is circuit satisfiability.

## Properties

- **Exact cases.** The numeric mode is exact without reconvergent fanout, which includes every fanout-free circuit and every circuit in which fanout stems feed only different outputs. The polynomial mode is always exact.
- **Not a bound.** Under reconvergence the numeric value can be too high or too low. For $y = \mathrm{AND}(a, \mathrm{NOT}(a))$ it is too high; for $y = \mathrm{OR}(a, \mathrm{NOT}(a))$, which is always 1, it gives $1 - p_a(1 - p_a)$, too low.
- **Multilinear.** In the polynomial mode each result is the multilinear polynomial of its function, so it gives $P(y)$ for every choice of input probabilities, not only one. This is useful when the input probabilities change, as in [weighted random pattern testing](/weighted-random-pattern-testing/).
- **Only spatial correlation.** Both modes compute probabilities at one instant. They say nothing about the correlation of a signal with itself at the next clock cycle, which [switching activity](/switching-activity/) needs.

## Variants and improvements

- **Reduced ordered BDDs.** Build the [BDD](/reduced-ordered-bdd/) of each node and compute $P(y)$ by the weighted form of [BDD satisfy-count](/bdd-satisfy-count/), in time linear in the BDD size. This is exact and is fast whenever the BDDs are small; the [BDD-based switching activity](/bdd-switching-activity-estimation/) page uses the same traversal on pairs of vectors.
- **Cutting algorithm.** Savir, Ditlow and Bardell (1984) cut all but one branch of each fanout stem, give each cut line the interval $[0, 1]$, and propagate intervals. The result is a lower and an upper bound on each $P(y)$, which holds on every circuit, but the interval can be wide.
- **Local correction.** Keep the numeric mode, and add correlation terms only for pairs of signals that share a stem within a few levels. This is a heuristic with no general bound.
- **Bayesian networks.** A circuit with independent inputs is a [Bayesian network](/bayesian-network/) in which each gate is a deterministic node. Exact inference by junction trees is exponential only in the treewidth, and [belief propagation](/belief-propagation/) on the circuit is the numeric mode written as messages.
- **Simulation.** Simulate random vectors and count. The error falls as one over the square root of the number of vectors, as on [Monte Carlo power estimation](/monte-carlo-power-estimation/), and the cost does not depend on the reconvergence.

## When to use it

Use the numeric mode as a fast first estimate, for example for power budgeting during synthesis or for the [COP](/cop-testability-measure/) measure in test, and accept its error on reconvergent logic. Use the polynomial mode, or BDDs, when the circuit or the cone of interest is small and an exact value is needed, for example to check an estimator or to compute the state probabilities that set the average [leakage power](/leakage-power/) of a gate. For large circuits that need accuracy, use simulation with a stated confidence.

## Pitfalls

- **Forgetting suppression.** In the polynomial mode, a product without $x^2 \to x$ is just the numeric mode in disguise, and it is wrong under reconvergence.
- **Suppressing too early.** Suppression is valid only because the polynomial is in the primary input probabilities. Applying $q^2 \to q$ to the probability of an internal node $q$ is wrong unless that node is a primary input.
- **The XOR formula.** $P(a \oplus b) = P(a) + P(b) - 2 P(a) P(b)$ needs independent $a$ and $b$. For three inputs, fold the two-input rule, or use $(1 - \prod_j (1 - 2 q_j)) / 2$.
- **Dependent primary inputs.** Both modes assume that the primary inputs are independent. Inputs that come from the same register bank, or from a counter, are often correlated, and then even the polynomial mode is wrong.
- **Probability is not activity.** A node with $P(y) = 1/2$ can switch every cycle or never. Power needs the [switching activity](/switching-activity/), which also depends on how inputs change over time.

## Implementations

## History

Parker and McCluskey (1975) defined the probability of a signal and the independence of two signals for combinational networks, gave the gate formulas, and handled reconvergent fanout by computing a polynomial in the input probabilities in which exponents are suppressed. Their motivation was the analysis of random testing and of circuits with faults. The cutting algorithm of Savir, Ditlow and Bardell (1984) gave bounds in place of exact values for large circuits. In power estimation, signal probabilities became the input of the probabilistic methods surveyed by Najm (1994), next to transition densities and BDD-based methods.

## References
