---
tag: 7T9702
kind: problem
slug: pctl-model-checking
name: PCTL model checking
aliases:
- Probabilistic model checking
- Model checking Markov chains
area: logic-and-constraints/model-checking
level: advanced
summary: Decide which states of a finite Markov chain satisfy a PCTL formula. Graph search plus one linear system per until gives time polynomial in the chain and linear in the formula.
prereqs: [probabilistic-ctl, markov-chain, ctl-model-checking]
see_also: [statistical-model-checking, gaussian-elimination, value-iteration, markov-decision-process, graph-reachability, linear-programming-problem, symbolic-model-checking, state-explosion-problem]
sources:
  - paper: doi:10.1007/BF01211866
    title: Hans Hansson and Bengt Jonsson, A logic for reasoning about time and reliability, Formal Aspects of Computing 6(5), 1994, pages 512 to 535
    locator: the model checking algorithm for PCTL on discrete-time Markov chains, with linear equations for until and iteration for bounded until
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 10 (reachability probabilities, the qualitative precomputation, Section 10.2 on PCTL model checking and its complexity, and the Knuth-Yao die)
  - paper: "Costas Courcoubetis and Mihalis Yannakakis, The complexity of probabilistic verification, Journal of the ACM 42(4), 1995, pages 857 to 907"
    title: The complexity of probabilistic verification
    locator: the complexity of checking linear-time properties and automata on Markov chains and on Markov decision processes
  - paper: "Andrea Bianco and Luca de Alfaro, Model checking of probabilistic and nondeterministic systems, Foundations of Software Technology and Theoretical Computer Science (FSTTCS 1995), Lecture Notes in Computer Science 1026, Springer, pages 499 to 513"
    title: Model checking of probabilistic and nondeterministic systems
    locator: PCTL model checking on Markov decision processes in polynomial time by linear programming
---

*PCTL model checking* asks which states of a finite [Markov chain](/markov-chain/) satisfy a formula of [probabilistic CTL](/probabilistic-ctl/). The answer is a set of states. Along the way the algorithm computes, for each probability operator $\mathcal{P}_{\bowtie p}(\varphi)$, the exact probability of $\varphi$ from every state. Hansson and Jonsson gave the algorithm in 1994. It follows [CTL model checking](/ctl-model-checking/): process the parse tree bottom up and label each state with the subformulas it satisfies. The probabilistic cases need three tools. Next is one matrix-vector product. Bounded until $\mathcal{U}^{\le k}$ is $k$ matrix-vector products. Unbounded until is a graph search for the states with probability 0 or 1, then one linear system for the rest. The total cost is polynomial in the size of the chain and linear in the size of the formula, apart from the factor $k$ for bounded until. [Statistical model checking](/statistical-model-checking/) answers the same questions approximately by simulation, when the chain is too large to solve.

## In plain words

A Markov chain is a set of states with a random move from each one, and each move has a known probability. We ask questions like "from this state, is the chance of reaching a failure without first passing a check at most 1 in 1000?". To answer, first find the states that cannot reach a failure at all, and the states from which a failure is certain. Plain graph search finds both. For each of the other states, its chance is the weighted average of the chances of its successors. That gives one equation per state, and solving the equations gives every chance exactly. Formulas that contain other formulas are answered from the inside out.

## Definition

**Input.** A finite Markov chain $M = (S, \mathbf{P}, L)$ with rational transition probabilities, and a PCTL state formula $\Phi$.

**Output.** The set $\mathrm{Sat}(\Phi) = \{s \in S : s \models \Phi\}$. The decision version asks whether a given state is in it.

The size of the input is $|M|$, the number of states and nonzero transitions plus the bits of the probabilities, together with $|\Phi|$, the number of operators. The step bounds $k$ in $\mathcal{U}^{\le k}$ are written in binary, and $k_{\max}$ is the largest of them.

The core computation is the *until probability*. For sets $A = \mathrm{Sat}(\Phi_1)$ and $B = \mathrm{Sat}(\Phi_2)$ it is the vector

$$x_s = \Pr_s(A \,\mathcal{U}\, B) = \Pr_s\{s_0 s_1 \ldots : \exists j.\ s_j \in B \text{ and } s_i \in A \text{ for all } i < j\}.$$

## Variants

- **Quantitative output.** Return the probability vector itself, not only the states above a threshold. Tools such as PRISM and Storm write this as $\mathcal{P}_{=?}(\varphi)$.
- **Qualitative PCTL.** Only $\mathcal{P}_{=1}$ and $\mathcal{P}_{>0}$ occur. The answer depends only on the graph of the chain, not on the numbers, and graph search solves it in linear time.
- **Markov decision processes.** With nondeterministic choices as well, $\mathcal{P}_{\bowtie p}$ ranges over all schedulers. The maximal and minimal until probabilities come from a [linear program](/linear-programming-problem/) or from [value iteration](/value-iteration/) on the [Markov decision process](/markov-decision-process/) (Bianco and de Alfaro 1995).
- **PCTL\* and LTL.** For a path formula of [LTL](/linear-temporal-logic/) under $\mathcal{P}$, build an automaton for the formula, take the product with the chain, and compute a reachability probability in the product.
- **Rewards.** Expected reward until a set is reached is also a linear system, after a graph search that finds the states where the expectation is infinite.
- **Continuous time.** CSL on continuous-time chains needs transient analysis, usually by uniformization, for time-bounded until.

## Examples

**The Knuth-Yao die.** A fair coin drives a walk from the start state $s_0$. The moves are $s_0 \to s_1, s_2$; $s_1 \to s_3, s_4$; $s_2 \to s_5, s_6$; $s_3 \to s_1, d_1$; $s_4 \to d_2, d_3$; $s_5 \to d_4, d_5$; $s_6 \to d_6, s_2$. Each move has probability $1/2$, and the faces $d_i$ are absorbing. To check $\mathcal{P}_{\ge 1/6}(\mathcal{F}\, d_6)$, compute $x = \Pr(\mathrm{true} \,\mathcal{U}\, d_6)$:

1. Backward search from $d_6$ reaches $s_6, s_2, s_0$. All other states form $S_{=0}$, including $s_1, s_3, s_4, s_5$.
2. No state other than $d_6$ has probability 1, because each of $s_0, s_2, s_6$ can reach $S_{=0}$. So $S_{=1} = \{d_6\}$.
3. The rest is $\{s_0, s_2, s_6\}$, with the equations $x_{s_0} = \tfrac12 x_{s_2}$, $x_{s_2} = \tfrac12 x_{s_6}$ and $x_{s_6} = \tfrac12 + \tfrac12 x_{s_2}$.

Solving them gives $x_{s_6} = 2/3$, $x_{s_2} = 1/3$ and $x_{s_0} = 1/6$, so the formula holds at $s_0$, and $\mathcal{P}_{>1/6}$ does not. For $\mathcal{P}_{\ge 3/4}(\mathcal{F}^{\le 3}\, \mathit{done})$, three matrix-vector products give $3/4$ at $s_0$: the walk ends within three flips unless it takes the loop $s_3 \to s_1$ or $s_6 \to s_2$.

**A qualitative case.** In the same chain, $\mathcal{P}_{=1}(\mathcal{F}\, \mathit{done})$ holds at $s_0$. Graph search alone shows it: no state can reach a state from which $\mathit{done}$ is unreachable. The infinite path that loops forever has probability 0.

## Known algorithms

The algorithm computes $\mathrm{Sat}$ for each subformula, from the leaves up. Atomic propositions, $\neg$ and $\wedge$ are set operations. For $\mathcal{P}_{\bowtie p}(\varphi)$ it computes the vector $x_s = \Pr_s(\varphi)$ and keeps the states with $x_s \bowtie p$:

- **Next:** $x = \mathbf{P} \cdot \mathbf{1}_{\mathrm{Sat}(\Phi)}$, one matrix-vector product.
- **Bounded until:** set $x^{(0)} = \mathbf{1}_B$. Then for $i = 1, \ldots, k$, set $x^{(i)}_s = \sum_t \mathbf{P}(s, t)\, x^{(i-1)}_t$ for $s \in A \setminus B$, and keep $x^{(i)}_s = x^{(0)}_s$ for the other states. This is $k$ matrix-vector products.
- **Until:** the following procedure.

```pseudo id=main
PROB-UNTIL(M, A, B)        ▷ A = Sat(Φ1), B = Sat(Φ2); returns x(s) = Pr_s(A U B)
L1  S0 ← S minus the states that reach B through states of A       ▷ backward search from B
L2  S1 ← S minus the states that reach S0 through states of A \ B   ▷ backward search from S0
L3  S? ← S \ (S0 ∪ S1)
L4  Q ← P restricted to S? × S?
L5  b(s) ← Σ_{t ∈ S1} P(s, t) for each s ∈ S?
L6  solve (I − Q) y = b        ▷ Gaussian elimination, or an iterative method
L7  x(s) ← 1 for s ∈ S1, x(s) ← 0 for s ∈ S0
L8  x(s) ← y(s) for s ∈ S?
L9  return x
```

**Why it is correct.** A state in $S_0$ has no path to $B$ through $A$, so its probability is 0. A state $s$ outside $S_0$ that cannot reach $S_0$ through $A \setminus B$ has probability 1, for the following reason. Until a path reaches $B$ or leaves $A$, it stays in states outside $S_0$. From each such state, $B$ can be reached within $|S|$ steps with probability at least some $\delta > 0$. So the probability of avoiding $B$ for $j|S|$ steps is at most $(1 - \delta)^j \to 0$. The path also cannot leave $A$ without entering $B$, since that would be a move into $S_0$. For $s \in S_?$, a first-step analysis gives $x_s = \sum_t \mathbf{P}(s, t)\, x_t$. With the known values on $S_0$ and $S_1$, this is $(I - Q) y = b$. Every state of $S_?$ can leave $S_?$ within $|S|$ steps with positive probability, so $Q^{|S|}$ has all row sums below 1. The spectral radius of $Q$ is then below 1, and $I - Q$ is invertible. So the solution is unique, and it equals $\sum_j Q^j b$, the until probability. Without step L2 the system is still uniquely solvable, but the probability-1 states are better found by graph search: it is exact, and it makes iterative solvers converge faster.

**Other methods.**

| Method | Cost | Notes |
|---|---|---|
| Graph search plus [Gaussian elimination](/gaussian-elimination/) | $O(n^3)$ arithmetic operations per until | Exact over the rationals; polynomial bit size with fraction-free elimination such as [Bareiss](/bareiss-algorithm/) |
| [Jacobi](/jacobi-method/), [Gauss-Seidel](/gauss-seidel-method/), [value iteration](/value-iteration/) | $O(m)$ per sweep | Used for large sparse chains; the usual stopping test does not bound the error, and interval iteration fixes this with bounds from above and below |
| [Matrix powers](/matrix-exponentiation/) for bounded until | $O(n^3 \log k)$ arithmetic operations | Make $\neg A \vee B$ absorbing, then $x = \mathbf{P}'^{k} \mathbf{1}_B$ |
| Symbolic, with multi-terminal [BDDs](/binary-decision-diagram/) | Depends on the structure | Used in PRISM for very large structured chains |
| Simulation ([statistical model checking](/statistical-model-checking/)) | Independent of $n$, about $\varepsilon^{-2} \log(1/\delta)$ runs | Approximate answers with a confidence level; no linear system |

## Bounds

- **Upper bound.** Each subformula is handled once. Next costs $O(m)$, bounded until $O(k m)$, and until $O(m)$ for the two searches plus the cost of the linear system, $O(n^3)$ arithmetic operations. The total is $O(|\Phi| \cdot (n^3 + k_{\max} m))$ operations, where $n = |S|$ and $m$ is the number of transitions. This is polynomial in $|M|$ and linear in $|\Phi|$. Because of the factor $k_{\max}$, the bounded until is only pseudo-polynomial when $k$ is written in binary. Repeated squaring reduces the number of operations to $O(n^3 \log k)$, but exact values can then have about $k$ times as many bits as the input probabilities.
- **Lower bound.** The problem is P-hard, by the same reduction from the [circuit value problem](/circuit-value-problem/) as for CTL. That reduction uses only next and the qualitative operators.
- **Linear-time properties.** Checking whether an LTL formula holds with probability 1 on a Markov chain is PSPACE-complete, and the exact probability can be computed in time polynomial in the chain and exponential in the formula (Courcoubetis and Yannakakis 1995). This is why PCTL keeps path formulas flat.
- **Markov decision processes.** PCTL model checking stays polynomial, through linear programming for until (Bianco and de Alfaro 1995).

## Reductions

- **To reachability in an absorbing chain.** Make every state outside $A \setminus B$ absorbing. Then $\Pr(A \,\mathcal{U}\, B)$ is the probability of absorption in $B$. This is the classical fundamental matrix computation, $x = (I - Q)^{-1} b$.
- **To graph problems.** Qualitative PCTL reduces to [graph reachability](/graph-reachability/): $\mathcal{P}_{>0}(A \,\mathcal{U}\, B)$ is $\mathsf{E}(A \,\mathcal{U}\, B)$ of CTL, and $\mathcal{P}_{=1}(A \,\mathcal{U}\, B)$ is "not reach $S_0$ through $A \setminus B$".
- **From probabilistic bisimulation.** Before model checking, the chain can be reduced by lumping probabilistically bisimilar states. This keeps all PCTL properties, as on [bisimulation](/bisimulation/).
- **From LTL.** A deterministic automaton for the path formula, multiplied with the chain, turns the LTL probability into a reachability probability on bottom [strongly connected components](/strongly-connected-components/) of the product.

## Applications

- **Randomized protocols.** Leader election, consensus with coin flips, and randomized mutual exclusion, where "eventually" holds only with probability 1.
- **Reliability and performance.** The probability of failure within $k$ steps, and the expected time to recovery.
- **Security and biology.** Anonymity protocols, and models of biochemical networks given as chains.
- **Tools.** PRISM and Storm implement these algorithms, with exact, iterative and symbolic engines. The [state explosion problem](/state-explosion-problem/) and the size of the linear systems are the main limits, which is where [statistical model checking](/statistical-model-checking/) and [symbolic methods](/symbolic-model-checking/) come in.

## References
