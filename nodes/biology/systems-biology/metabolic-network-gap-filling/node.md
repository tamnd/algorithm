---
tag: WC084Q
kind: problem
slug: metabolic-network-gap-filling
name: Metabolic network gap filling
aliases:
- GapFill
area: biology/systems-biology
level: advanced
summary: Add the fewest reactions from a database to a draft metabolic network so that it can make biomass, a mixed-integer program.
prereqs: [flux-balance-analysis, mixed-integer-programming]
see_also: [flux-variability-analysis, constraint-based-metabolic-modeling, set-cover, np-hard, lp-relaxation, big-m-formulation, branch-and-cut, elementary-flux-mode]
sources:
  - paper: doi:10.1186/1471-2105-8-212
    title: Vinay Satish Kumar, Madhukar S. Dasika and Costas D. Maranas, Optimization based automated curation of metabolic reconstructions, BMC Bioinformatics 8, 2007, 212
    locator: the Methods section, with the GapFind formulation that finds metabolites that cannot be produced or consumed, and the GapFill formulation that restores them with the fewest changes from a reaction database
  - paper: doi:10.1073/pnas.0603364103
    title: Jennifer L. Reed, Trina R. Patel, Keri H. Chen, Andrew R. Joyce, Margaret K. Applebee, Christopher D. Herring, Olivia T. Bui, Eric M. Knight, Stephen S. Fong and Bernhard O. Palsson, Systems approach to refining genome annotation, PNAS 103(46), 2006, 17480-17484
    locator: the SMILEY method, which adds the fewest reactions from a universal database so that the model grows on media where growth was observed
  - paper: doi:10.1093/bioinformatics/btu321
    title: Ines Thiele, Nikos Vlassis and Ronan M. T. Fleming, fastGapFill, efficient gap filling in metabolic networks, Bioinformatics 30(17), 2014, 2529-2531
    locator: the linear programming method that finds a compact set of added reactions for all blocked reactions of a genome-scale model
  - paper: doi:10.1016/j.biosystems.2008.06.015
    title: Vicente Acuña, Flavio Chierichetti, Vincent Lacroix, Alberto Marchetti-Spaccamela, Marie-France Sagot and Leen Stougie, Modes and cuts in metabolic networks, complexity and algorithms, BioSystems 95(1), 2009, 51-60
    locator: Section 2.1, the NP-hardness of finding the fewest reactions to add so that a network becomes consistent
---

Gap filling completes a draft metabolic network. A draft built from a genome annotation usually misses some reactions, because some genes have no known function or were annotated wrongly. Then the model cannot make some metabolites, or cannot grow on a medium where the real organism grows. Gap filling takes a database of known reactions from other organisms and asks for the smallest set of them that, added to the draft, lets the model carry a steady flux through a target, usually the biomass reaction. Each added reaction is a hypothesis about a missing gene function. The problem is NP-hard, and the standard methods solve it as a [mixed-integer program](/mixed-integer-programming/), with one binary variable for each database reaction.

## In plain words

A model of a cell's metabolism is built from its genes. Some genes are missing from the list or have the wrong label, so the model has holes: it cannot make some of the parts it needs to grow. But the real cell does grow.

Gap filling looks for the fewest new reactions that close the holes. It takes them from a large catalogue of reactions found in other living things. A solver tries many choices of reactions and keeps the smallest choice that lets the model grow.

The result is a list of suggestions. Each one says that the cell probably has an enzyme for this reaction, and a biologist can then look for the gene or test it in the lab.

## Definition

**Input.** A draft network with reaction set $N$, a database of candidate reactions $D$ with $D \cap N = \emptyset$, one stoichiometric matrix $S$ over all metabolites and the reactions $N \cup D$, flux bounds $lb \le v \le ub$ for all these reactions, a target reaction $b \in N$, a threshold $\varepsilon > 0$, and costs $w_j > 0$ for $j \in D$.

**Feasibility of a set.** For $A \subseteq D$, the network $N \cup A$ can make the target if there is a flux vector $v$ with

$$S v = 0, \qquad lb \le v \le ub, \qquad v_j = 0 \text{ for } j \in D \setminus A, \qquad v_b \ge \varepsilon .$$

This is one [linear program](/linear-programming-problem/), so it is decided in polynomial time.

**Output.** A set $A \subseteq D$ of least cost $\sum_{j \in A} w_j$ such that $N \cup A$ can make the target, or the answer that no such set exists. With all costs 1 the cost is the number of added reactions. An instance has a solution if and only if $A = D$ is feasible, which one LP checks.

**The MILP.** With a binary $y_j$ for each $j \in D$, and bounds $lb_j \le 0 \le ub_j$, the problem is

$$\min \sum_{j \in D} w_j y_j \quad \text{subject to} \quad S v = 0, \quad lb \le v \le ub, \quad lb_j y_j \le v_j \le ub_j y_j \;\; (j \in D), \quad v_b \ge \varepsilon, \quad y \in \{0, 1\}^D .$$

If a bound is infinite, it is replaced by a large constant, as in any [big-M formulation](/big-m-formulation/).

## Variants

- **Make each blocked metabolite producible.** GapFind (Satish Kumar, Dasika and Maranas 2007) first finds the metabolites that the draft cannot produce or cannot consume at steady state. GapFill then restores each of them with the fewest changes: added database reactions, added transport or exchange reactions, and reversed directions of draft reactions. Each change type can have its own cost.
- **Growth on observed media.** SMILEY (Reed and co-authors 2006) uses growth data: for a medium on which the organism grows but the model does not, it adds the fewest reactions from a universal database so that the model grows. One instance is solved per medium.
- **Unblock all blocked reactions.** fastGapFill (Thiele, Vlassis and Fleming 2014) takes all blocked reactions of the model as targets at once and finds a compact set of added reactions with a sequence of linear programs. It does not promise a minimum set.
- **Weighted costs.** Reactions with sequence evidence for a gene in the genome get a low cost, and transport and exchange reactions a high cost, so that the solver prefers biologically plausible solutions.
- **Removing growth.** The reverse problem removes the fewest reactions so that the model does not grow on media where the organism does not grow.
- **All minimal solutions.** Adding a constraint that cuts off each solution found, and solving again, lists other minimal sets. Different sets are different hypotheses.

## Examples

**A small draft.** The draft has an uptake EX_A ($\to A$, at most 10), R1 ($A \to B$) and the target BIO ($B + C + D \to$). It cannot grow, because nothing makes $C$ or $D$. The database has four reactions:

| reaction | equation |
|---|---|
| D1 | $A \to C$ |
| D2 | $A \to D$ |
| D3 | $B \to C + D$ |
| D4 | $C \to D$ |

No single reaction other than D3 helps, since D1 and D4 alone make no $D$ and D2 alone makes no $C$. The set $\{D3\}$ is feasible: with growth $g$, D3 carries $g$, R1 carries $2g$, and the uptake is $2g$. So the minimum is one reaction. The sets $\{D1, D2\}$ and $\{D1, D4\}$ are also feasible but cost two. The choice also changes the predicted growth. With D3 the uptake bound gives $2g \le 10$, so $g \le 5$. With D1 and D2 it gives $3g \le 10$, so $g \le \frac{10}{3}$.

**Blocked reactions.** In the draft, R1 is blocked: its flux range from [flux variability analysis](/flux-variability-analysis/) with no objective is $[0, 0]$, because $B$ has no consumer except BIO, which is blocked too. Blocked reactions mark where the gaps are, and the gap-filling targets are often chosen from them.

**A set cover instance.** For the universe $\{1, 2, 3\}$ and the sets $T_1 = \{1, 2\}$, $T_2 = \{2, 3\}$ and $T_3 = \{3\}$, the reduction below builds metabolites $M_1, M_2, M_3$, the target BIO ($M_1 + M_2 + M_3 \to$), a drain for each $M_i$, and the database reactions X1 ($\to M_1 + M_2$), X2 ($\to M_2 + M_3$) and X3 ($\to M_3$). The smallest feasible sets are $\{X1, X2\}$ and $\{X1, X3\}$, the minimum set covers.

## Known algorithms

| method | type | result |
|---|---|---|
| MILP with [branch and cut](/branch-and-cut/) | exact | a minimum set, in exponential time in the worst case |
| GapFill (Satish Kumar, Dasika and Maranas 2007) | MILP per problem metabolite | minimum changes for each metabolite |
| SMILEY (Reed and co-authors 2006) | MILP per growth medium | minimum added reactions for each medium |
| fastGapFill (Thiele, Vlassis and Fleming 2014) | a sequence of LPs | a compact set, not always minimum |
| [LP relaxation](/lp-relaxation/) and rounding | heuristic | a feasible set, with no guarantee on the size |
| brute force over subsets | exact | a minimum set in $O(2^{|D|})$ LPs |

The LP methods replace the count of added reactions by the sum of their absolute fluxes, a weighted L1 norm, which tends to give sparse solutions. This is a heuristic. Its main use is speed on databases with thousands of reactions.

## Bounds

- **NP-hard.** The problem with unit costs is NP-hard, by the reduction from set cover below. Acuña and co-authors (2009, Section 2.1) prove the NP-hardness of the closely related problem of adding the fewest reactions so that a network becomes consistent. This is a theorem.
- **In NP.** The decision version, "is there a feasible set of at most $k$ reactions?", is in NP, because a feasible set is checked with one LP. With the reduction, it is NP-complete. This is a theorem.
- **No good approximation in general.** The reduction keeps the cost: a feasible set of $k$ reactions is a cover by $k$ sets and the reverse. So a polynomial-time approximation within a factor $(1 - \delta) \ln n$, for $n$ the number of metabolites and any fixed $\delta > 0$, would give the same factor for [set cover](/set-cover/), which is impossible unless P = NP. This is a theorem.
- **Feasibility is easy.** Whether any solution exists is one LP, with $A = D$.
- **Exact methods.** The MILP has $|D|$ binary variables, so brute force needs at most $2^{|D|}$ LPs. The published MILP methods were applied to genome-scale models with large databases, so branch and cut often works in practice. This is a measurement on those models, not a bound.

## Reductions

**From set cover.** Take a universe $\{1, \ldots, n\}$ and sets $T_1, \ldots, T_r$. Build one metabolite $M_i$ for each element. The draft has the target BIO, which uses one unit of each $M_i$, and a drain reaction $M_i \to$ for each $i$, with all fluxes in $[0, \infty)$ or a large finite bound. The database has one reaction $X_s$ for each set, which makes one unit of $M_i$ for each $i \in T_s$ from nothing. Take $\varepsilon = 1$ and unit costs.

If $\{T_s : s \in A\}$ covers the universe, set $v_{X_s} = 1$ for $s \in A$ and $v_{\text{BIO}} = 1$. Each $M_i$ is made by at least one chosen reaction, so its production $c_i \ge 1$, and the drain carries $c_i - 1 \ge 0$. So $S v = 0$ and $\{X_s : s \in A\}$ is feasible. Conversely, if $A$ is feasible, then for each $i$ the production of $M_i$, which comes only from the chosen $X_s$ with $i \in T_s$, is at least $v_{\text{BIO}} \ge 1$. So some chosen set contains $i$, and $\{T_s : s \in A\}$ is a cover. The two problems have the same feasible sets and the same costs, and the construction takes polynomial time.

**To MILP.** The formulation in the definition is a reduction to mixed-integer programming, with one binary variable per database reaction.

## Applications

- **Draft reconstructions.** Automated reconstruction pipelines run gap filling to make a draft model grow on its standard medium before any manual work.
- **Finding gene functions.** An added reaction says that some gene of the organism has an enzyme activity that the annotation missed. Reed and co-authors (2006) used growth data on many media to suggest such reactions for Escherichia coli and then looked for the genes.
- **Model curation.** GapFind and GapFill show the metabolites and reactions that are disconnected in a published model, which points to errors in the reconstruction.
- **Before analysis.** FBA, FVA and the knockout methods of [constraint-based modeling](/constraint-based-metabolic-modeling/) give wrong answers on a model that cannot grow, so gap filling is usually done first.

## References
