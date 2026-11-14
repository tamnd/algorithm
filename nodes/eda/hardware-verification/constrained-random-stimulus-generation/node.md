---
tag: H74QKF
kind: problem
slug: constrained-random-stimulus-generation
name: Constrained random stimulus generation
aliases:
- constrained random verification
- constrained random test generation
area: eda/hardware-verification
level: core
summary: Generate random input vectors that satisfy declared constraints, with a controlled and ideally uniform distribution, to drive simulation of a design.
prereqs: [sat, boolean-function, rejection-sampling]
see_also: [bdd-constrained-random-generation, coverage-directed-test-generation, functional-coverage, model-counting, jerrum-valiant-vazirani-theorem, tseitin-transformation, bit-blasting, np-hard]
sources:
  - paper: "IEEE Std 1800-2017, IEEE Standard for SystemVerilog, Unified Hardware Design, Specification, and Verification Language, IEEE, 2018"
    title: IEEE Standard for SystemVerilog, Unified Hardware Design, Specification, and Verification Language, IEEE Std 1800-2017
    locator: Clause 18 (Constrained random value generation, with random variables, constraint blocks, distributions, implication, variable ordering and the randomize method)
  - book: isbn:9780387259475
    title: Jun Yuan, Carl Pixley and Adnan Aziz, Constraint-Based Verification, Springer, 2006
    locator: the chapters on constrained random simulation, the constraint languages, and the BDD-based and other constraint solvers (general locator)
  - paper: doi:10.1006/inco.2000.2885
    title: Mihir Bellare, Oded Goldreich and Erez Petrank, Uniform generation of NP-witnesses using an NP-oracle, Information and Computation 163(2), 510 to 526, 2000
    locator: the probabilistic polynomial-time generator, with an NP oracle, that outputs each witness with exactly the same probability
  - paper: doi:10.1016/0304-3975(86)90174-X
    title: Mark R. Jerrum, Leslie G. Valiant and Vijay V. Vazirani, Random generation of combinatorial structures from a uniform distribution, Theoretical Computer Science 43, 169 to 188, 1986
    locator: the reduction of exactly uniform generation to approximate counting, and the equivalence of almost uniform generation and randomized approximate counting for self-reducible relations
  - paper: doi:10.1007/978-3-642-39799-8_40
    title: Supratik Chakraborty, Kuldeep S. Meel and Moshe Y. Vardi, A scalable and nearly uniform generator of SAT witnesses, Computer Aided Verification (CAV 2013), LNCS 8044, 608 to 623
    locator: UniWit, near-uniform generation of the models of a CNF formula by random XOR constraints
  - paper: doi:10.1145/2593069.2593097
    title: Supratik Chakraborty, Kuldeep S. Meel and Moshe Y. Vardi, Balancing scalability and uniformity in SAT witness generator, Proceedings of the 51st Design Automation Conference (DAC 2014), 1 to 6
    locator: UniGen, its tolerance parameter and its guarantee that each model is returned with probability within a bounded factor of the uniform probability
---

Constrained random stimulus generation is the problem of producing random input values for the simulation of a design such that every value satisfies a set of declared constraints, and the values follow a chosen distribution over the legal ones, most often the uniform distribution. The constraints say what a legal input is: a valid opcode with its operand fields, a packet whose length matches its header, a request that only comes when the queue is not full. The verification languages make this the main way to write stimulus; SystemVerilog defines random variables, constraint blocks and the `randomize` method in Clause 18 of IEEE Std 1800-2017. Finding one legal value is [SAT](/sat/), so the problem is [NP-hard](/np-hard/); drawing each legal value with the same probability is tied to [model counting](/model-counting/). Methods are on [BDD-based constrained random generation](/bdd-constrained-random-generation/) and the pages listed under Known algorithms.

## In plain words

A simulation needs inputs, and most random inputs are nonsense for the design: a bus transfer with a length that does not match its address, an instruction with an illegal field. So the engineer writes rules that every input must obey, and a solver picks random values that obey all of them.

Obeying the rules is not enough. If the solver always picks the same easy answer, or favors some answers by accident, many legal situations are never tried. The usual goal is that every legal input is equally likely, or that the likelihoods follow weights the engineer chose on purpose. Finding even one legal input can be as hard as any puzzle of this kind, and picking among all of them fairly is harder still.

## Definition

**Input.** Variables $x = (x_1, \ldots, x_n)$ over finite domains, which after [bit-blasting](/bit-blasting/) are $n$ bits; a *constraint* $C : \{0, 1\}^n \to \{0, 1\}$, given as a Boolean formula, a circuit or a set of word-level relations; and a target distribution. The set of *solutions* (models) is $S = C^{-1}(1)$, and $\#C = |S|$.

**Output.** A random $x \in S$, or the answer "no solution" when $S = \emptyset$. Each call is independent of the others, and a stream of calls gives a stream of stimuli.

**Uniform generation.** The output law is $\Pr[x = s] = 1/\#C$ for every $s \in S$.

**Near-uniform generation.** For a tolerance $\varepsilon > 0$, $\frac{1}{(1 + \varepsilon)\#C} \le \Pr[x = s] \le \frac{1 + \varepsilon}{\#C}$ for every $s \in S$, possibly with a stated probability that the call fails and returns nothing.

**Weighted generation.** A weight $w : \{0, 1\}^n \to \mathbb{Q}_{> 0}$ is given, and $\Pr[x = s] = w(s) / \sum_{t \in S} w(t)$ for $s \in S$. A common form is a product of independent biases, $w(s) = \prod_i p_i^{s_i} (1 - p_i)^{1 - s_i}$, which is the bias law conditioned on $C$.

**With state.** In a simulation the constraint often depends on the state $q$ of the design or of the test bench, $C(q, x)$, and a new instance with the current $q$ is solved in each cycle or transaction.

## Variants

- **Uniform, near-uniform, weighted.** As defined above. Most practical generators guarantee none of the three and only aim at a spread of values; the definitions say what a claim of "uniform" must mean.
- **SystemVerilog constraints.** Variables declared `rand` are solved together; `randc` variables cycle through all values of their domain in a random order before any value repeats. The standard asks that, without distributions and ordering, all legal combinations be equally likely. A `dist` constraint gives relative weights to the values of one expression; when other constraints also restrict that expression, the result depends on the tool. `solve a before b` keeps the set of solutions and changes the law: $a$ is drawn as if alone, then $b$ given $a$. Soft constraints are dropped when they conflict with hard ones.
- **Sequences.** Constraints over several transactions, such as "no two writes to the same address within four cycles", are written with state in the test bench, which turns them into the stateful form above.
- **Word-level or bit-level.** Constraints over integers with arithmetic are solved either on words by interval and modular reasoning, or after bit-blasting on bits, where a constraint like $a + b < c$ becomes an adder circuit.
- **Projection.** The constraint may use auxiliary variables $y$ that are not stimulus, $C(x, y)$. Then the target is uniform over $\{x : \exists y\, C(x, y)\}$, which is not the same as uniform over pairs $(x, y)$ when the number of $y$ varies with $x$.

## Examples

**An ordered pair.** Two 2-bit variables $a, b \in \{0, 1, 2, 3\}$ with the constraint $a < b$. The solutions are $(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)$, so $\#C = 6$ of the 16 assignments, and the uniform law gives each one $1/6$.

| solution | uniform | $a$ before $b$ | $b$ before $a$ |
|---|---|---|---|
| (0,1) | 1/6 | 1/9 | 1/3 |
| (0,2) | 1/6 | 1/9 | 1/6 |
| (0,3) | 1/6 | 1/9 | 1/9 |
| (1,2) | 1/6 | 1/6 | 1/6 |
| (1,3) | 1/6 | 1/6 | 1/9 |
| (2,3) | 1/6 | 1/3 | 1/9 |

The second column draws $a$ uniformly from its legal values $\{0, 1, 2\}$, then $b$ uniformly from the values above $a$: $(2,3)$ gets $1/3 \cdot 1 = 1/3$ and $(0,1)$ gets $1/3 \cdot 1/3 = 1/9$. The third column draws $b$ from $\{1, 2, 3\}$ first. Both orders keep the six solutions, and both put three times as much weight on one solution as on another. Drawing all 16 assignments uniformly and keeping the first that satisfies $a < b$ gives the uniform column, after $16/6 = 8/3$ draws on average.

**Projection.** Let $x \in \{0, 1\}$ and an auxiliary $y \in \{0, 1, 2, 3\}$ with $C(x, y) = (x = 1) \lor (y = 0)$. The pairs with $x = 1$ are 4 and the pairs with $x = 0$ are 1, so uniform pairs give $x = 1$ with probability $4/5$, while uniform stimulus over $\{x : \exists y\, C\} = \{0, 1\}$ gives $1/2$.

**A header and a length.** A packet has a 2-bit `kind` and a 6-bit `len`, with `kind == 0 -> len == 0` and `kind != 0 -> len inside [1:63]`. There are $1 + 3 \cdot 63 = 190$ solutions. The uniform law gives `kind == 0` the probability $1/190$; a generator that first picks `kind` uniformly gives it $1/4$. Which one the engineer wants depends on the [coverage](/functional-coverage/) goal, which is why the law must be stated.

## Known algorithms

- **[Rejection sampling](/rejection-sampling/)** from the uniform law on all assignments. Exact; expected tries $2^n / \#C$.
- **[BDD-based constrained random generation](/bdd-constrained-random-generation/)** (Yuan, Shultz, Pixley, Miller and Aziz 1999). Exact uniform or exact weighted generation from path counts on a [binary decision diagram](/binary-decision-diagram/) of $C$, in time linear in the number of variables per sample once the BDD is built.
- **Counting by [self-reducibility](/self-reducibility/).** Fix the variables one at a time, with probabilities given by the [model counts](/model-counting/) of the two restricted constraints. Exact with an exact counter.
- **Hashing.** UniWit (CAV 2013) and UniGen (DAC 2014) of Chakraborty, Meel and Vardi add random XOR constraints from a [$k$-wise independent](/k-wise-independence/) family to cut $S$ into small cells, enumerate one cell with a SAT solver, and return a random member: near-uniform with a stated tolerance.
- **SAT or constraint solvers with random choices.** Random decisions and random restarts of a [CDCL](/cdcl/) solver give a spread of solutions with no bound on the bias.
- **Steering the law.** [Coverage-directed test generation](/coverage-directed-test-generation/) changes the weights between runs to reach coverage holes.

## Bounds

- **NP-hardness.** A generator that runs in polynomial time and returns a solution whenever one exists decides [SAT](/sat/): run it on $C$ and check the output. If it is randomized and returns a solution with probability at least $1/2$ whenever one exists, the same check puts SAT in RP. So no such generator exists unless $\mathrm{NP} = \mathrm{P}$, respectively $\mathrm{NP} = \mathrm{RP}$. This holds for any target law, uniform or not.
- **Rejection.** Drawing $x$ uniformly from $\{0, 1\}^n$ until $C(x) = 1$ returns each solution with probability exactly $1/\#C$, and the number of draws has a [geometric distribution](/geometric-distribution/) with success probability $\#C / 2^n$, so its mean is $2^n / \#C$. The proof is on [BDD-based constrained random generation](/bdd-constrained-random-generation/). The method is exact and fast when solutions are dense, and useless when they are rare, as they are for most real constraints.
- **Exact uniform generation and counting.** With exact [model counts](/model-counting/) of restricted constraints, self-reducibility gives exact uniform generation with $n$ counting calls. Counting is #P-complete, so this route is not polynomial in general. Jerrum, Valiant and Vazirani (1986) showed that exactly uniform generation of witnesses of an NP relation reduces to approximate counting, which places it in the third level of the polynomial hierarchy.
- **An NP oracle suffices.** Bellare, Goldreich and Petrank (2000) generate each witness with exactly the same probability in probabilistic polynomial time with an NP oracle, failing with a small probability.
- **Almost uniform equals approximate counting.** For [self-reducible](/self-reducibility/) relations, almost uniform generation and randomized [approximate counting](/approximate-counting/) are inter-reducible in polynomial time ([Jerrum-Valiant-Vazirani theorem](/jerrum-valiant-vazirani-theorem/)).
- **Compiled forms.** If $C$ is given as a reduced ordered BDD, uniform and weighted generation take $O(n)$ time per sample after $O(|B|)$ preprocessing, where $|B|$ is the number of nodes. The BDD itself can be exponential in $n$ under every [variable order](/variable-ordering/), for example for a constraint on the middle output bit of a multiplier.

## Reductions

- **SAT to generation.** Shown in Bounds: a generator decides SAT by one call and one check.
- **Generation to counting.** By self-reducibility, as in Known algorithms.
- **Circuits to CNF.** The [Tseitin transformation](/tseitin-transformation/) of a circuit constraint adds one variable per gate whose value is fixed by the inputs, so the models of the CNF are in bijection with the solutions of the circuit. Uniform generation on the CNF, projected onto the input variables, is uniform generation for the circuit.
- **Word-level to bit-level.** [Bit-blasting](/bit-blasting/) maps word constraints to Boolean ones with the same solutions on the stimulus bits, plus auxiliary bits fixed by them.
- **Weighted to uniform.** Product weights with rational biases $p_i = k_i / 2^{m_i}$ reduce to uniform generation by giving variable $i$ $m_i$ fresh bits and constraining it to be 1 exactly when the number those bits encode is below $k_i$, for $0 < k_i < 2^{m_i}$. A solution $s$ then has $\prod_i k_i^{s_i} (2^{m_i} - k_i)^{1 - s_i}$ extensions, a number proportional to $w(s)$, so uniform generation on the new constraint, projected onto $x$, is the weighted law.

## Applications

- **Simulation-based verification.** Test benches in SystemVerilog and similar languages declare transactions with constraints and call the solver for each one; the [functional coverage](/functional-coverage/) model then measures which legal situations the runs reached.
- **Processor verification.** Instruction stream generators draw instructions, operands and addresses under constraints that keep the program legal and steer it toward interesting cases, such as cache conflicts.
- **Closure loops.** [Coverage-directed generation](/coverage-directed-test-generation/) tunes the weights of the generator from coverage data.
- **Beyond hardware.** The same problem appears in software test input generation and in sampling configurations of product lines, where hashing-based samplers are used.

## References
