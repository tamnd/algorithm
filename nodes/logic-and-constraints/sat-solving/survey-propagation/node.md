---
tag: VFSYED
kind: algorithm
slug: survey-propagation
name: Survey propagation
aliases:
- SP
area: logic-and-constraints/sat-solving
level: research
summary: Message-passing heuristic for random k-SAT from statistical physics. It estimates which variables are frozen, fixes the most biased ones, simplifies, repeats, then runs WalkSAT.
solves: [sat]
model: word-ram
complexity:
  vars: {n: the number of variables, m: the number of clauses, k: the largest clause size, d: the largest number of clauses that contain one variable, R: the number of decimation rounds, S: the sweep limit per round, w: the WalkSAT flip limit}
  time: {worst: O(R (S m k (d + k) + n m k) + w (m + k^2 d))}
  space: {extra: O(n + m k)}
properties: {deterministic: false, exact: false}
history:
  year: 2002
  people: [Marc Mézard, Giorgio Parisi, Riccardo Zecchina]
  note: Derived from the one-step replica symmetry breaking cavity method, and reported to find models of very large random 3-CNF formulas close to the predicted threshold.
prereqs: [sat, k-sat, unit-propagation, walksat]
see_also: [satisfiability-threshold, walksat, probsat, k-sat, 3-sat, unit-propagation, belief-propagation, cdcl]
sources:
  - paper: doi:10.1126/science.1073287
    title: "Marc Mézard, Giorgio Parisi and Riccardo Zecchina, Analytic and algorithmic solution of random satisfiability problems, Science 297 (2002), 812 to 815"
    locator: the SP equations and the first decimation results
  - paper: doi:10.1103/PhysRevE.66.056126
    title: "Marc Mézard and Riccardo Zecchina, Random K-satisfiability problem, from an analytic solution to an efficient algorithm, Physical Review E 66 (2002), 056126"
    locator: the cavity derivation, the predicted thresholds 3.921 and 4.267 for 3-SAT, and SP-guided decimation
  - paper: doi:10.1002/rsa.20057
    title: "Alfredo Braunstein, Marc Mézard and Riccardo Zecchina, Survey propagation, an algorithm for satisfiability, Random Structures and Algorithms 27 (2005), 201 to 226"
    locator: the algorithm in the form used on this page, with decimation and the final WalkSAT phase, and the experiments
  - paper: doi:10.1145/1255443.1255445
    title: "Elitza Maneva, Elchanan Mossel and Martin J. Wainwright, A new look at survey propagation and its generalizations, Journal of the ACM 54 (2007), article 17"
    locator: SP as belief propagation on an extended model with a joker value
  - book: isbn:9780198570837
    title: Marc Mézard and Andrea Montanari, Information, Physics, and Computation (2009)
    locator: Chapter 20, random k-satisfiability, and the chapters on survey propagation
---

Survey propagation (SP) is a heuristic for the [satisfiability problem](/sat/) on large random [$k$-CNF](/k-sat/) formulas, by Mézard, Parisi and Zecchina (2002). It comes from the cavity method of statistical physics. Each clause sends each of its variables a number between 0 and 1, the *survey*, which estimates the probability that the clause forces that variable. The surveys are updated until they stop changing. From them SP computes, for each variable, how strongly it is pushed toward true or false, fixes the most biased variables, simplifies the formula, and starts again. When the surveys become all zero, a local search such as [WalkSAT](/walksat/) finishes the job. SP has no correctness proof for finding models: its results on random formulas near the [satisfiability threshold](/satisfiability-threshold/) are measured, and the physics that motivates it is a prediction, not a theorem.

## In plain words

Think of the clauses as a crowd of people, each holding a rule, and the variables as switches. Each rule-holder looks at its own switches and asks: "Are the other switches of my rule all pushed the wrong way by other people? If so, I must insist on this one." It sends a message with how likely it is to insist. Everyone listens, updates, and sends again, until the messages settle.

Then each switch adds up the messages it got. A switch that many people insist should be on is set on. A few of the most certain switches are fixed, the rules that they satisfy are removed, and the talk starts again on the smaller problem. When nobody insists on anything any more, the rest is easy, and a simple local search finds the last settings.

## The problem

The input is a CNF formula $F$ with $n$ variables and $m$ clauses, usually a uniform random $k$-CNF formula with $m/n$ close to the satisfiability threshold. The output is a model of $F$ or "failure". SP does not decide satisfiability: "failure" also happens on satisfiable formulas, and it proves nothing.

## The algorithm

For a clause $a$ and a variable $i$ of $a$, the survey $\eta_{a \to i} \in [0, 1]$ estimates the probability that $a$ sends a *warning* to $i$, which means that all other variables of $a$ are forced to values that make their literals in $a$ false, so that $i$ must satisfy $a$. For $j$ in $a$, let $p_s$ be the product of $1 - \eta_{b \to j}$ over the other clauses $b$ in which $j$ has the same sign as in $a$, and $p_u$ the same product over the other clauses with the opposite sign. Then

$$\Pi^u_{j \to a} = (1 - p_u)\, p_s, \quad \Pi^s_{j \to a} = (1 - p_s)\, p_u, \quad \Pi^0_{j \to a} = p_s p_u, \qquad \eta_{a \to i} = \prod_{j \in a \setminus i} \frac{\Pi^u_{j \to a}}{\Pi^u_{j \to a} + \Pi^s_{j \to a} + \Pi^0_{j \to a}}.$$

$\Pi^u$ is the weight of "$j$ is forced to violate $a$", $\Pi^s$ of "forced to satisfy $a$", and $\Pi^0$ of "free". With $P_+$ and $P_-$ the products of $1 - \eta_{a \to i}$ over the clauses where $i$ is positive and negative, the biases are

$$W^+_i \propto (1 - P_+) P_-, \qquad W^-_i \propto (1 - P_-) P_+, \qquad W^0_i \propto P_+ P_-,$$

normalized to sum to 1.

```pseudo id=main
SP-DECIMATION(F, f, δ)
L1 while F has clauses do
L2     iterate the SP update over the clauses, in random order, until no survey moves by more than ε, or until the sweep limit
L3     if SP did not converge or a variable is warned both ways then return "failure"
L4     if every survey is below δ then leave the loop            ▷ trivial fixed point: no information
L5     compute W+(i), W−(i), W0(i) for each variable i of F
L6     fix the fraction f of the variables with the largest |W+(i) − W−(i)|, each to the sign of W+(i) − W−(i)
L7     simplify F with the fixed values and unit propagation
L8     if F has an empty clause then return "failure"
L9 x ← the fixed values, with the free variables set by WalkSAT on the rest of F
L10 if x satisfies the original F then return x else return "failure"
```

The implementation starts each round from random surveys, uses $\varepsilon = 10^{-3}$, at most 1000 sweeps, $\delta = 10^{-2}$ and $f = 5\%$ (at least one variable per round). It applies unit propagation once before the first round.

## Example

Take $F = (x_1) \wedge (\neg x_1 \vee x_2) \wedge (x_2 \vee x_3 \vee x_4)$ and run the SP update alone, without simplification.

- The unit clause $(x_1)$ has no other variable, so its survey to $x_1$ is the empty product, 1: it always warns $x_1$.
- For the clause $(\neg x_1 \vee x_2)$ and the variable $x_2$: the other variable is $x_1$, which appears in that clause negated. The only other clause of $x_1$ is $(x_1)$, with the opposite sign and survey 1, so $p_u = 0$ and $p_s = 1$, the ratio is 1, and the survey to $x_2$ is 1. The survey from this clause to $x_1$ is 0, since nothing warns $x_2$ to be false.
- For the clause $(x_2 \vee x_3 \vee x_4)$: $x_2$ gets a warning from a clause in which it has the same sign, so $p_s = 0$ and $\Pi^u = 0$, and all three surveys of this clause are 0.

The biases are $W^+ = 1$ for $x_1$ and $x_2$, and $W^0 = 1$ for $x_3$ and $x_4$, which are free. The surveys that are 0 or 1 reproduce [unit propagation](/unit-propagation/) exactly; the proof file shows this in general. On a large random formula near the threshold, most surveys are strictly between 0 and 1, and that is where SP adds information that unit propagation does not have.

## Correctness

Line L10 checks the final assignment against every clause, so each answer is a model. Simplification is sound: every model of the simplified formula, together with the fixed values, satisfies the original formula. Each round fixes at least one variable that still occurs, so there are at most $n$ rounds, and the sweeps and flips are bounded, so the procedure stops. The proof file gives these facts, and that a unit clause always sends a full warning, so that surveys of 0 and 1 follow unit propagation.

What is not proved is that SP finds models. Decimation can fix a variable to a value that no model has, which makes the rest unsatisfiable; the surveys may fail to converge; and the meaning of the surveys as probabilities over clusters of models comes from the one-step replica symmetry breaking cavity method, which is a non-rigorous method of physics. Maneva, Mossel and Wainwright showed that the SP equations are exactly belief propagation on a related model in which a variable may also take a "joker" value, which explains the equations but does not give a guarantee.

## Complexity

One SP sweep updates every clause. For each of its at most $k$ variables it scans at most $d$ other clauses, then it forms $k$ products of $k - 1$ ratios, so a sweep costs $O(mk(d + k))$. A round makes at most $S$ sweeps and one simplification, which in this implementation costs $O(nmk)$ in the worst case. With fraction $f$, about $(\ln n)/f$ rounds fix all variables, plus at most $1/f$ rounds that fix one variable each. The WalkSAT phase of the implementation costs $O(m + k^2 d)$ per flip. Better implementations reach $O(mk)$ per sweep by keeping products of the incoming surveys per variable and per sign.

The number of sweeps until convergence is not bounded in theory, and is measured.

## Properties

- **Heuristic.** It returns only models, but it may fail on satisfiable formulas, and it cannot prove unsatisfiability.
- **Built for random formulas.** It works where the factor graph of the formula is locally like a tree, as in uniform random $k$-CNF. On structured formulas with many short cycles, it often fails to converge or gives no information.
- **Generalizes unit propagation.** With surveys in $\{0, 1\}$ it is warning propagation, which is unit propagation.
- **Trivial fixed point.** At low clause density, all surveys go to 0 and SP gives no information; then WalkSAT alone is enough.

## Variants and improvements

- **Belief propagation guided decimation.** Use the marginals of belief propagation over all models instead of the surveys. It is simpler but was reported to stop working at lower densities than SP on random 3-SAT.
- **SP with backtracking.** Undo some fixed values when a contradiction appears.
- **SP-y.** A version with a parameter $y$ that also handles MAX-SAT on formulas above the threshold.
- **Reinforcement.** Add a slowly growing external field instead of fixing variables in rounds.
- **Larger $k$ and other problems.** The same method was applied to random $k$-SAT for $k > 3$, to graph coloring, and to other constraint problems.

## When to use it

Use SP on very large uniform random $k$-CNF formulas with clause density between the clustering transition and the threshold, where local search alone is slow and the formula is expected to be satisfiable. For anything structured, use a [CDCL](/cdcl/) solver. For random formulas well below the threshold, [WalkSAT](/walksat/) or [probSAT](/probsat/) alone is simpler and fast.

## Pitfalls

- **Reading "failure" as UNSAT.** SP proves nothing about unsatisfiable formulas.
- **Expecting help on easy formulas.** Below the clustering density the surveys are all zero, and SP only adds cost.
- **Fixing too many variables at once.** A large fraction $f$ saves sweeps but makes wrong fixes more likely.
- **Division by zero.** A variable warned by both signs makes the three weights 0. This is a contradiction and must be handled, not divided.
- **Treating the physics predictions as theorems.** The threshold 4.267 for 3-SAT that comes with SP is a prediction of the cavity method; see [satisfiability threshold](/satisfiability-threshold/) for what is proved.

## Implementations

## History

Physicists had studied random $k$-SAT as a disordered system since the 1990s. In 2002 Mézard, Parisi and Zecchina, and Mézard and Zecchina, used the one-step replica symmetry breaking cavity method to predict that for 3-SAT the models split into many clusters at a density of about 3.921 and disappear at about 4.267, and turned the cavity equations into the SP algorithm. They reported that SP-guided decimation found models of random 3-CNF formulas with very many variables, in the range of millions, at densities above 4.2, where the local search methods of the time were reported to fail. Braunstein, Mézard and Zecchina described the algorithm in detail in 2005. Maneva, Mossel and Wainwright gave a combinatorial reading of SP in 2007. Later work proved parts of the physics picture for large $k$, such as the location of the threshold (Ding, Sly and Sun 2015), but no proof covers the success of SP itself.

## References
