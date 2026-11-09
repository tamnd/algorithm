---
tag: 4MQXH0
kind: technique
slug: reliability-branching
name: Reliability branching
aliases:
- reliability pseudocost branching
area: optimization/integer-programming
level: research
summary: Use strong branching on a variable until its pseudocosts rest on enough observations, then trust the pseudocosts.
prereqs: [strong-branching, pseudocost-branching, branching-rule]
see_also: [strong-branching, pseudocost-branching, branching-rule, node-selection-rule, branch-and-cut, mixed-integer-programming, land-doig-algorithm, presolve]
sources:
  - paper: doi:10.1016/j.orl.2004.04.002
    title: Tobias Achterberg, Thorsten Koch and Alexander Martin, Branching rules revisited, Operations Research Letters 33(1), 2005
    locator: pp. 42 to 54; Section 2.6 (Algorithm 3, reliability branching) and Section 3 (computational results)
  - paper: "Tobias Achterberg, Thorsten Koch and Alexander Martin, Branching rules revisited, ZIB-Report 04-13, Zuse Institute Berlin, 2004"
    locator: Table 1 (geometric means of nodes and time for all strategies, lookahead 4 and 8) and Figure 2
  - paper: doi:10.1287/ijoc.11.2.173
    title: Jeff T. Linderoth and Martin W. P. Savelsbergh, A computational study of search strategies for mixed integer programming, INFORMS Journal on Computing 11(2), 1999
    locator: pp. 173 to 187 (pseudocost branching with strong branching initialization, the rule that reliability branching generalizes)
  - paper: "Tobias Achterberg, Constraint Integer Programming, PhD thesis, Technische Universität Berlin, 2007"
    locator: the chapter on branching (reliability branching as the default rule of SCIP; chapter number unsure)
---

Reliability branching is a [branching rule](/branching-rule/) that combines [strong branching](/strong-branching/) and [pseudocost branching](/pseudocost-branching/). It calls a pseudocost unreliable while it rests on fewer than $\eta_{\text{rel}}$ observations in one of the two directions, runs strong branching only on candidates with unreliable pseudocosts, and uses the strong branching results as new observations. Achterberg, Koch and Martin introduced it in 2004, and in their measurements it was faster than both rules it combines. It is the default rule of SCIP and the basis of the rules of other solvers.

## In plain words

Strong branching makes good choices but costs a lot, because it tests every candidate. Pseudocost branching is cheap, because it guesses from past experience, but at the start it has no experience to guess from.

Reliability branching tests a variable only as long as the experience about it is thin. Each test also adds to the experience. After a variable has been observed a few times in both directions, the solver trusts the guess for it and stops testing it. Near the top of the tree, where choices matter most, most variables are still tested; deeper in the tree, most choices are cheap guesses.

## When it applies

- LP-based branch and bound or [branch-and-cut](/branch-and-cut/) for a [mixed integer program](/mixed-integer-programming/), with variable branching on fractional variables.
- Strong branching is affordable for some nodes but too expensive for all of them.
- The same variables are candidates at many nodes, so pseudocosts collect observations. In very small trees, the rule behaves like strong branching.

## The template

The holes are the reliability threshold $\eta_{\text{rel}}$, the iteration limit $\gamma$, the lookahead $\lambda$ and SCORE. The pseudocosts $\Psi_j^\pm$, the counts $\eta_j^\pm$ and the update rule are those of [pseudocost branching](/pseudocost-branching/); an uninitialized pseudocost takes the average of the initialized ones.

```pseudo id=main
RELIABILITY-BRANCH(N, x̄, v)
L1  C ← fractional integer variables of x̄
L2  for each j in C do s_j ← SCORE(f⁻_j Ψ⁻_j, f⁺_j Ψ⁺_j)       ▷ pseudocost scores
L3  sort C by s_j, largest first
L4  best ← the first j in C;  unchanged ← 0
L5  for each j in C with min(η⁻_j, η⁺_j) < η_rel do           ▷ unreliable candidates
L6      solve the two children of j with at most γ dual simplex iterations each
L7      update Ψ⁻_j and Ψ⁺_j with the gains found              ▷ counts η_j grow
L8      s_j ← SCORE(gain down, gain up)
L9      if s_j > s_best then best ← j;  unchanged ← 0
L10     else unchanged ← unchanged + 1
L11     if unchanged = λ then exit the loop
L12 return best
```

With $\eta_{\text{rel}} = 0$ the loop never runs and the rule is pure pseudocost branching. With $\eta_{\text{rel}} = 1$ it is pseudocost branching with strong branching initialization, as in Linderoth and Savelsbergh. With $\eta_{\text{rel}} = \infty$ every candidate is tested at every node, so the rule is strong branching with lookahead $\lambda$.

**Why the search stays correct.** As with every branching rule, the choice of a fractional variable cannot change the answer of branch and bound. Pseudocost scores are estimates and are used only for the choice. The strong branching trials of line L6 give valid upper bounds on the child LPs, as explained on the [strong branching](/strong-branching/) page, so a solver may also use them to prune a child or to tighten a bound.

**What is not proved.** The rule is a heuristic. There is no theorem about its tree size or running time compared with other rules. The claim that it works well rests on computational studies.

**Example.** Take the instance of the [strong branching](/strong-branching/) page:
$$\max\ 10x_1 + 10x_2 + 7x_3 \quad \text{s.t.} \quad 6x_1 + 4x_2 + 6x_3 \le 15,\quad 3x_1 + 8x_2 + 2x_3 \le 18,\quad x \in \{0, 1, 2, 3\}^3,$$
with $\eta_{\text{rel}} = 1$ and $\mu = 1/6$ in SCORE.

1. At the root, $\bar{x} = (\tfrac43, \tfrac74, 0)$ and no variable has a pseudocost, so both candidates are unreliable. The trials give the scores $\tfrac76$ for $x_1$ and $\tfrac{49}{18}$ for $x_2$, and they set $\Psi_1 = (\tfrac{11}{5}, 5)$ and $\Psi_2 = (\tfrac{10}{3}, \tfrac{46}{3})$. The rule branches on $x_2$.
2. The up child is integral with value 27. The down child has $\bar{x} = (\tfrac{11}{6}, 1, 0)$, and $x_1$ is the only candidate. It now has one observation in each direction, so it is reliable, and the rule uses its pseudocost score without any LP solve.

With $\eta_{\text{rel}} = 2$, step 2 would run one more trial on $x_1$ and add the true gains $\tfrac52$ and $\tfrac56$ to its pseudocosts.

## Classic examples

- **The original study.** Achterberg, Koch and Martin ran all rules in the solver SIP on instances from MIPLIB 2003 and from Mittelmann's benchmarks that CPLEX 9.0 solves with at least 5000 nodes within one hour, with cuts only at the root and a time limit of one hour. The table below gives some of the geometric means of their Table 1, with lookahead $\lambda = 4$.
- **SCIP.** The default branching rule of SCIP is reliability branching on pseudocosts, with further terms in the score, as described in Achterberg's thesis.

| rule | nodes | time (s) | instances not solved |
|---|---|---|---|
| most infeasible | 262369 | 938.0 | 11 |
| pseudocost | 88707 | 283.4 | 2 |
| full strong | 7242 | 504.4 | 2 |
| reliability, $\eta_{\text{rel}} = 1$ | 70014 | 216.4 | 1 |
| reliability, $\eta_{\text{rel}} = 4$ | 53523 | 178.2 | 0 |
| reliability, $\eta_{\text{rel}} = 8$ | 48773 | 170.5 | 0 |
| reliability, $\eta_{\text{rel}} = 32$ | 39655 | 184.2 | 0 |

In these measurements, a larger $\eta_{\text{rel}}$ gave fewer nodes, and the time was best near $\eta_{\text{rel}} = 8$. Reliability branching was faster than hybrid strong and pseudocost branching for every parameter setting they tried. These are results for one solver, one machine and one test set, not general facts.

## Variations

- **Dynamic reliability.** Make $\eta_{\text{rel}}$ depend on the state of the search, for example on the ratio of strong branching iterations to node LP iterations, so that the rule tests less when trials have been expensive.
- **Hybrid scores.** Add to the pseudocost score terms for the number of bound changes caused by branching on the variable (inference), for its part in conflicts, and for how often it is fractional. SCIP combines several such terms.
- **Lookahead and iteration limits.** The lookahead $\lambda$ stops the trials after $\lambda$ tests without a new best candidate. Achterberg, Koch and Martin found $\lambda = 4$ sufficient in their tests, because the candidates are already ordered by pseudocost score.
- **Reliability by statistics.** Instead of a count, call a pseudocost reliable when the confidence interval of its mean is small enough.

## Pitfalls

- **Too small a threshold.** With $\eta_{\text{rel}} = 1$, one early observation decides all later choices for that variable, even if it was untypical.
- **Too large a threshold.** With a large $\eta_{\text{rel}}$, the rule spends most of its time in trials, as strong branching does.
- **Trials that are stopped early.** A trial limited to $\gamma$ iterations gives a gain that is smaller than the true one. Adding it to the pseudocosts biases them downward.
- **Nodes and time.** Like other rules, reliability branching should be judged by time and by solved instances, not only by node counts. The table above shows that full strong branching needs the fewest nodes but is not the fastest.

## Exercises

1. Show that the template with $\eta_{\text{rel}} = 0$ is pseudocost branching, and with $\eta_{\text{rel}} = \infty$ and $\lambda = \infty$ is full strong branching.
2. In the example with $\eta_{\text{rel}} = 2$, compute the pseudocosts of $x_1$ after step 2.
3. Suppose each trial costs as much as $t$ node LPs. If a variable is a candidate at $k$ nodes, how many trials does reliability branching spend on it in the worst case?
4. Design a rule that marks a pseudocost as unreliable again when the model changes, for example after a restart, and discuss its cost.
5. Use the table to compute, for each rule, the time per node. What does it show about the cost of trials?

## References
