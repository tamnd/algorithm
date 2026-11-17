---
tag: K9KY6N
kind: algorithm
slug: optknock
name: OptKnock
aliases:
- bilevel knockout optimization
area: biology/systems-biology
level: advanced
summary: Choose reaction deletions that couple product secretion to growth, as a bilevel mixed-integer program with FBA as the inner problem.
model: real-ram
complexity:
  vars: {m: the number of reactions, n: the number of metabolites, c: the number of candidate reactions, K: the largest number of knockouts, T: the time of one LP with 2m + n variables}
  time: {worst: O((c + 1)^K T)}
  space: {extra: O((m + n)^2)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2003
  people: [Anthony P. Burgard, Priti Pharkya, Costas D. Maranas]
  note: Burgard, Pharkya and Maranas posed strain design as a bilevel program, with the cell maximizing growth inside and the engineer maximizing a product outside, and turned it into one MILP by LP duality.
prereqs: [flux-balance-analysis, mixed-integer-programming, lp-duality]
see_also: [flux-variability-analysis, minimization-of-metabolic-adjustment, constraint-based-metabolic-modeling, strong-duality, big-m-formulation, lp-relaxation, branch-and-cut, np-hard]
sources:
  - paper: doi:10.1002/bit.10803
    title: Anthony P. Burgard, Priti Pharkya and Costas D. Maranas, OptKnock, a bilevel programming framework for identifying gene knockout strategies for microbial strain optimization, Biotechnology and Bioengineering 84(6), 2003, 647-657
    locator: the bilevel formulation, its reduction to a MILP through the dual of the inner LP, and the E. coli case studies
  - paper: doi:10.1093/bioinformatics/btp704
    title: Naama Tepper and Tomer Shlomi, Predicting metabolic engineering knockout strategies for chemical production, accounting for competing pathways, Bioinformatics 26(4), 2010, 536-543
    locator: RobustKnock, the max-min version that guarantees the product over all inner optima
  - paper: doi:10.1038/nbt.1614
    title: Jeffrey D. Orth, Ines Thiele and Bernhard O. Palsson, What is flux balance analysis?, Nature Biotechnology 28(3), 2010, 245-248
    locator: the inner FBA problem
---

OptKnock searches for a set of reaction deletions that makes a microbe secrete a chosen product as a side effect of growing. A wild-type cell that maximizes growth usually secretes little of a useful product, because making the product costs carbon and energy. OptKnock removes up to $K$ reactions so that, in the mutant, every way of growing at the best rate must also secrete the product. Then selection for growth also selects for production. Burgard, Pharkya and Maranas (2003) wrote this as a bilevel program: the outer level chooses the deletions to maximize the product flux, and the inner level is the [FBA](/flux-balance-analysis/) problem of the mutant, which maximizes growth. The inner LP is replaced by its [dual](/lp-duality/) and a [strong duality](/strong-duality/) equation, which gives one [mixed-integer program](/mixed-integer-programming/).

## In plain words

You want a factory that makes a product, but the factory manager only cares about one thing: producing as much new factory as possible. You cannot give orders to the manager. You can only remove some machines before the manager starts.

OptKnock looks for the machines to remove so that the manager's best plan, chosen only for growth, also makes a lot of your product. If you remove the right machines, the only good way left to grow is a way that gives off the product as waste. The method checks this by solving the manager's problem inside your own problem. A trick from linear programming turns the two nested problems into one problem that a standard solver can handle.

## The problem

**Input.** An $n \times m$ stoichiometric matrix $S$; flux bounds $lb \le v \le ub$; the index $b$ of the biomass reaction and $p$ of the product secretion; a set $C$ of candidate reactions that may be deleted; a limit $K$; and optionally a growth floor $\mu_{\min}$.

**Output.** A set $D \subseteq C$ with $|D| \le K$ that solves the bilevel program

$$\max_{D} \; v_p \quad \text{where} \quad v \in \arg\max_{u} \{ u_b : S u = 0, \; lb^D \le u \le ub^D \}, \quad v_b \ge \mu_{\min},$$

with $lb^D_j = ub^D_j = 0$ for $j \in D$, together with the flux vector $v$. When the inner problem has several optima, the original formulation takes the one with the largest product. This is the optimistic version: it is the best case among the states that the cell might choose.

## The algorithm

For a fixed $D$, the inner LP $\max \{u_b : S u = 0, \; lb \le u \le ub\}$ has the dual

$$\min \; ub^{\mathsf T} \alpha - lb^{\mathsf T} \beta \quad \text{subject to} \quad S^{\mathsf T} \lambda + \alpha - \beta = e_b, \quad \alpha, \beta \ge 0,$$

with free $\lambda$, one $\alpha_j$ for each finite upper bound and one $\beta_j$ for each finite lower bound. By weak duality every dual feasible point bounds $u_b$ from above. So $v$ is an optimum of the inner LP exactly when $v$ is primal feasible and some dual feasible point has $v_b = ub^{\mathsf T} \alpha - lb^{\mathsf T} \beta$. Putting these rows together gives one LP in $(v, \lambda, \alpha, \beta)$ for each $D$. Burgard and co-authors add binary variables $y_j$ for the deletions, which makes the products $ub_j y_j \alpha_j$ appear; they linearize them with bounds on the dual variables, as in a [big-M formulation](/big-m-formulation/), and solve one MILP. The implementation here enumerates the sets $D$ instead of using binaries.

```pseudo id=main
OPTKNOCK(S, lb, ub, b, p, K, C, μ_min)
L1  best ← none
L2  for each D ⊆ C with |D| ≤ K, by size:
L3      (lb_D, ub_D) ← lb, ub with lb_j = ub_j = 0 for j in D
L4      solve max v_p subject to S v = 0, lb_D ≤ v ≤ ub_D, v_b ≥ μ_min, S^T λ + α - β = e_b, α, β ≥ 0, v_b = ub_D^T α - lb_D^T β
L5      if the LP is infeasible then continue
L6      if best is none or v_p > the product of best then best ← (D, v)
L7  return best
```

The LP of line L4 is infeasible exactly when the mutant has no steady state, when its growth is unbounded, or when its optimal growth is below $\mu_{\min}$.

## Example

Take network N of the [FBA page](/flux-balance-analysis/): uptake EX_A of a substrate $A$ (at most 10), two respiration reactions RESP1 and RESP2 ($A \to 2E$), fermentation FERM ($A \to E + P$), secretion EX_P of the product $P$, and growth BIO ($A + E \to$). The candidates are RESP1, RESP2 and FERM, and the product is the flux of EX_P.

- **$K = 0$.** The wild type grows at $\frac{20}{3}$ by respiration only, and every optimum has zero fermentation, so the product is 0.
- **$K = 1$.** Deleting one respiration reaction leaves the other one, and growth stays at $\frac{20}{3}$ with no product. Deleting FERM removes the product route. So the best product is still 0.
- **$K = 2$.** Deleting RESP1 and RESP2 leaves fermentation as the only source of $E$. The mutant grows at 5, and its only optimal state is $v = (10, 0, 0, 5, 5, 5)$: it must secrete 5 units of $P$. Growth and production are now coupled. OptKnock returns $D = \{\text{RESP1}, \text{RESP2}\}$.
- **Growth floor.** With $\mu_{\min} = 6$, the coupled design grows too slowly, and the best design keeps respiration, with product 0 and growth $\frac{20}{3}$. With $\mu_{\min} = 7$, above the wild-type optimum, no design is feasible.

**Optimistic and guaranteed values.** Change the network so that it has one respiration reaction $A \to E$ and the fermentation $A \to E + P$, with the same yield of $E$. Then growth is the same for any split between the two, and the optimal face of the inner LP contains states with any product from 0 to 5. The OptKnock value without deletions is 5, but the cell may choose the state with product 0. The tests check this case, which is the reason for the max-min variant RobustKnock.

On random small networks, the tests check that the inner LP and its dual have the same optimum, which also equals the best growth over the vertices of the flux polytope. They check that the LP of line L4 has the same value as a two-step solve that uses no duality: first FBA for the optimal growth, then the maximum product with growth fixed at that value. Finally they compare optknock with a direct enumeration that uses those two-step solves.

## Correctness

For a fixed $D$, weak duality says that $u_b \le ub^{\mathsf T} \alpha - lb^{\mathsf T} \beta$ for every primal feasible $u$ and dual feasible $(\lambda, \alpha, \beta)$. So a feasible point of the LP of line L4 has a $v$ that is optimal for the inner problem. Conversely, if $v$ is optimal for the inner problem, strong duality gives a dual solution with the same value, so $v$ extends to a feasible point of the LP. The LP therefore maximizes $v_p$ over exactly the inner optima with $v_b \ge \mu_{\min}$, which is the optimistic bilevel value for $D$. Line L2 visits every allowed set, so the best set found is a solution of the bilevel program. The full proof is below.

## Complexity

- **This code.** The number of sets is $\sum_{k \le K} \binom{c}{k} \le (c + 1)^K$ for $c$ candidates, and each needs one LP with $2m + n$ or fewer variables and $n + m + 1$ equality rows. So the time is $O((c + 1)^K T)$ for an LP time $T$. This is exact, and it is practical only for small $K$ or few candidates.
- **The MILP.** The MILP of Burgard and co-authors has $c$ binary variables. Mixed-integer programming is [NP-hard](/np-hard/) in general, so no polynomial bound is known for the solver. Branch and bound and [branch and cut](/branch-and-cut/) codes solve it for genome-scale models with small $K$ in practice; this is an observation, not a bound.
- **Reductions of the candidate set.** Removing essential reactions, blocked reactions and reactions without gene association before the search makes $c$ much smaller. This is the usual preprocessing step.
- **Space.** $O((m + n)^2)$ for one LP tableau.

## Properties

- **Exact for its model.** For each $D$ the LP value is the exact optimistic bilevel value, and the enumeration finds the best set.
- **Optimistic.** The design is evaluated at the inner optimum that is best for the product. The cell may choose another optimum with less product. FVA on the product flux of the mutant at its optimal growth gives the guaranteed value.
- **Growth coupling.** A good design makes the product flux positive at every optimal state of the mutant, not only at one. The production envelope of the mutant shows this.
- **Assumes an optimal mutant.** OptKnock uses FBA as the inner model, so it assumes that the mutant grows at its optimum, for example after adaptive evolution. Right after a deletion, [MOMA](/minimization-of-metabolic-adjustment/) is the usual model instead.
- **Monotone in K.** A larger $K$ never gives a smaller optimum, since every set allowed for $K$ is allowed for $K + 1$.

## Variants and improvements

- **RobustKnock.** Tepper and Shlomi (2010) maximize the guaranteed product, the minimum of $v_p$ over the inner optima. This is a max-min program, and they reduce it to a MILP with a second dual.
- **OptStrain and OptReg.** Extensions that add reactions from a database or up- and down-regulate fluxes instead of deleting them.
- **OptGene.** A genetic algorithm searches the knockout sets and evaluates each one by FBA or MOMA. It allows nonlinear objectives, but it is a heuristic with no guarantee of finding the best set.
- **Gene-level deletions.** Deleting a gene removes all the reactions that depend on it, through the gene-protein-reaction rules. The candidate set is then a set of genes, and one binary variable switches off several reactions.
- **Minimal cut sets.** Sets of reactions whose removal blocks a given flux, often computed from elementary flux modes, are a related approach to coupling.

## When to use it

Use OptKnock to propose knockout strategies for growth-coupled production in a genome-scale model, before laboratory work. Check every proposed design with FVA for its guaranteed production, and prefer designs that couple the product at all optimal states. For small models or small $K$, the enumeration of this page gives the exact answer and a list of all good designs. For designs that must not depend on optimal growth, use MOMA or a robust formulation.

## Pitfalls

- **Optimistic designs.** A design with high OptKnock value but zero guaranteed product often fails in the laboratory, as in the tie example.
- **Big constants.** In the MILP, the bounds on the dual variables must be large enough. Too small values cut off the true dual solution and give a wrong design.
- **Unbounded product.** If the product can grow without bound on the optimal face (for example through a cycle), the outer problem is unbounded. Bound every flux in the model.
- **Wrong candidates.** Exchange reactions, spontaneous reactions and reactions without a gene are not real deletion targets. Remove them from the candidate set.
- **Model gaps.** Missing reactions in the model can make a design look coupled when the real cell has a bypass. [Gap filling](/metabolic-network-gap-filling/) and FVA on the mutant reduce this risk.

## Implementations

## History

Burgard, Pharkya and Maranas published OptKnock in 2003. They wrote the inner FBA problem through its dual and a strong duality constraint, which turns the bilevel program into one MILP, and they applied it to the production of chemicals such as succinate and lactate in Escherichia coli. Later work from the same group extended the approach with reaction additions and regulation (OptStrain, OptReg), and Tepper and Shlomi (2010) gave the robust max-min version.

## References
