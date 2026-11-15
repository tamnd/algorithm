---
tag: 8FMM4D
kind: problem
slug: belief-merging
name: Belief merging
aliases:
- knowledge base merging
area: information-retrieval-and-ai-reasoning/argumentation-and-belief-revision
level: research
summary: Combine several belief bases, possibly in conflict, into one consistent base that respects integrity constraints and fairness postulates.
prereqs: [belief-revision, katsuno-mendelzon-revision]
see_also: [dalal-revision, hamming-distance, belief-update, borda-count, polynomial-hierarchy, max-sat]
sources:
  - paper: "Sébastien Konieczny and Ramón Pino Pérez, Merging information under constraints: a logical framework, Journal of Logic and Computation 12(5), 773 to 808 (2002)"
    locator: the whole paper (the postulates IC0 to IC8, Maj and Arb, the representation by syncretic assignments, and the distance-based operators with the sum, max and Gmax aggregations)
  - paper: doi:10.1016/0004-3702(91)90069-V
    title: Hirofumi Katsuno and Alberto O. Mendelzon, Propositional knowledge base revision and minimal change, Artificial Intelligence 52(3), 263 to 294 (1991)
    locator: Section 3 (the postulates R1 to R6, which IC0 to IC8 extend to profiles)
  - paper: doi:10.1016/0004-3702(92)90018-S
    title: Thomas Eiter and Georg Gottlob, On the complexity of propositional knowledge base revision, updates, and counterfactuals, Artificial Intelligence 57(2-3), 227 to 270 (1992)
    locator: Theorem 6.9 (Dalal's revision is P^NP[O(log n)]-complete, which gives the lower bound for merging with one base)
---

Belief merging combines several belief bases of equal standing into one. The bases may come from different sensors, experts or databases, each consistent on its own but in conflict with the others. The result must be consistent, must satisfy a set of integrity constraints, and should treat the sources fairly. Sébastien Konieczny and Ramón Pino Pérez (2002) gave the standard postulates, IC0 to IC8, which extend the [Katsuno and Mendelzon postulates for revision](/katsuno-mendelzon-revision/) from one base to a multiset of bases. The most used operators measure how far each world is from each base and aggregate the distances by a sum or by a maximum.

## In plain words

Several people each give you what they believe. They do not agree, so you cannot just believe all of it. You also have hard rules that the answer must obey. You want one consistent answer that follows the rules and stays as close as possible to what everyone said.

"As close as possible" for a group needs a choice. You can make the total disagreement small, so that the majority wins. Or you can make the worst disagreement small, so that nobody is left far behind. The two choices can give different answers from the same inputs, and the postulates say which properties each choice keeps.

## Definition

Fix a finite propositional language. A belief base $K$ is a consistent formula. A profile $\Psi = \{K_1, \ldots, K_m\}$ is a finite multiset of bases, so the same base may occur twice and then counts twice. $\bigwedge \Psi$ is the conjunction of its bases, and $\Psi_1 \sqcup \Psi_2$ is the multiset union. An integrity constraint is a formula $\mu$. A merging operator maps $\Psi$ and $\mu$ to a formula $\Delta_\mu(\Psi)$.

The postulates of Konieczny and Pino Pérez (2002) are:

| | postulate |
|---|---|
| IC0 | $\Delta_\mu(\Psi) \models \mu$. |
| IC1 | If $\mu$ is consistent, then $\Delta_\mu(\Psi)$ is consistent. |
| IC2 | If $\bigwedge \Psi \wedge \mu$ is consistent, then $\Delta_\mu(\Psi) \equiv \bigwedge \Psi \wedge \mu$. |
| IC3 | If $\Psi_1 \equiv \Psi_2$ and $\mu_1 \equiv \mu_2$, then $\Delta_{\mu_1}(\Psi_1) \equiv \Delta_{\mu_2}(\Psi_2)$. |
| IC4 | If $K_1 \models \mu$ and $K_2 \models \mu$, then $\Delta_\mu(\{K_1, K_2\}) \wedge K_1$ is consistent if and only if $\Delta_\mu(\{K_1, K_2\}) \wedge K_2$ is consistent. |
| IC5 | $\Delta_\mu(\Psi_1) \wedge \Delta_\mu(\Psi_2) \models \Delta_\mu(\Psi_1 \sqcup \Psi_2)$. |
| IC6 | If $\Delta_\mu(\Psi_1) \wedge \Delta_\mu(\Psi_2)$ is consistent, then $\Delta_\mu(\Psi_1 \sqcup \Psi_2) \models \Delta_\mu(\Psi_1) \wedge \Delta_\mu(\Psi_2)$. |
| IC7 | $\Delta_{\mu_1}(\Psi) \wedge \mu_2 \models \Delta_{\mu_1 \wedge \mu_2}(\Psi)$. |
| IC8 | If $\Delta_{\mu_1}(\Psi) \wedge \mu_2$ is consistent, then $\Delta_{\mu_1 \wedge \mu_2}(\Psi) \models \Delta_{\mu_1}(\Psi) \wedge \mu_2$. |

Two profiles are equivalent when there is a one to one map between their bases that pairs equivalent bases. IC4 is fairness: when two bases are merged, the result cannot agree with one and not the other. IC5 and IC6 say that when two groups agree on some worlds, the merged group picks exactly those. IC7 and IC8 are the revision postulates R5 and R6 for the constraint.

**Representation.** An operator satisfies IC0 to IC8 if and only if there is a syncretic assignment, a map from each profile $\Psi$ to a total preorder $\le_\Psi$ on worlds, with $\mathrm{Mod}(\Delta_\mu(\Psi)) = \min(\mathrm{Mod}(\mu), \le_\Psi)$. The conditions on the assignment are: the models of $\bigwedge \Psi$, when there are any, are exactly the least worlds of $\le_\Psi$; equivalent profiles get the same preorder; for two bases $K$ and $K'$, each model of $K$ is matched by a model of $K'$ that is at least as good in $\le_{\{K, K'\}}$; and if $w \le_{\Psi_1} w'$ and $w \le_{\Psi_2} w'$ then $w \le_{\Psi_1 \sqcup \Psi_2} w'$, strictly if one of the two is strict (Konieczny and Pino Pérez 2002).

**Majority and arbitration.** Two more postulates split the operators. Maj: for some $n$, $\Delta_\mu(\Psi_1 \sqcup \Psi_2^n) \models \Delta_\mu(\Psi_2)$, where $\Psi_2^n$ is $n$ copies of $\Psi_2$; enough repeated voices win. Arb asks the opposite: the result does not depend on how many times a base is repeated, in a precise sense stated in the paper. An IC operator with Maj is a majority operator, and one with Arb is an arbitration operator.

The computational problem for a fixed operator is: given $\Psi$, $\mu$ and $q$, does $\Delta_\mu(\Psi)$ entail $q$?

## Variants

- **No constraint.** Take $\mu$ to be a tautology. The result then only has to be consistent.
- **One base.** For $\Psi = \{K\}$, IC0, IC1, IC2, IC3, IC7 and IC8 become R1, R3, R2, R4, R5 and R6, so $\Delta_\mu(\{K\})$ is a revision of $K$ by $\mu$. Merging generalizes revision.
- **Weighted merging.** Give each source a weight and multiply its distance by it. This breaks the symmetry of IC3 on purpose.
- **Formula-based merging.** Take the union of the bases as a set of formulas and keep its maximal consistent subsets with $\mu$. It depends on how the bases are written.
- **Judgment and preference aggregation.** In social choice, voters give judgments on linked issues or rankings, and the same tension between majority and consistency appears. Distance-based merging with the sum is close to choosing the outcome with the least total disagreement, as the [Borda count](/borda-count/) does for rankings with its own measure.

## Examples

Take the atoms $a$ and $b$ and the profile $\Psi = \{K_1, K_2, K_3\}$ with $K_1 = K_2 = a \wedge b$ and $K_3 = \neg a \wedge \neg b$. The distance from a world $w$ to a base $K$ is $d(w, K) = \min_{v \in \mathrm{Mod}(K)} h(w, v)$, with $h$ the [Hamming distance](/hamming-distance/).

| world $ab$ | $d$ to $K_1$, $K_2$, $K_3$ | sum $\Sigma$ | max | sorted vector (Gmax) |
|---|---|---|---|---|
| 11 | 0, 0, 2 | 2 | 2 | (2, 0, 0) |
| 10 | 1, 1, 1 | 3 | 1 | (1, 1, 1) |
| 01 | 1, 1, 1 | 3 | 1 | (1, 1, 1) |
| 00 | 2, 2, 0 | 4 | 2 | (2, 2, 0) |

With $\mu$ a tautology:

- $\Delta^{\Sigma}$ keeps the worlds with the least sum, so the result is $a \wedge b$. The two agreeing sources outvote the third.
- $\Delta^{\max}$ and $\Delta^{\mathrm{Gmax}}$ keep the worlds with the least worst distance, and Gmax breaks ties by the next largest, and so on. The result is $a \oplus b$, a compromise in which every source is one atom away.

With the constraint $\mu = \neg(a \wedge b)$, the world 11 is excluded, and all three operators give $a \oplus b$. These results were checked by a script, which also checked IC0 to IC8 on random profiles over 3 atoms: $\Delta^{\Sigma}$ and $\Delta^{\mathrm{Gmax}}$ passed all of them, and $\Delta^{\max}$ failed only IC6.

A small failure of IC6 for the maximum: let $\Psi_1 = \{\neg a \wedge \neg b\}$ and $\Psi_2 = \{\neg a \wedge \neg b,\ a \wedge \neg b\}$, with no constraint. $\Delta^{\max}(\Psi_1)$ is $\neg a \wedge \neg b$. For $\Psi_2$, the worlds 00 and 10 both have worst distance 1, so $\Delta^{\max}(\Psi_2)$ is $\neg b$. The two results are consistent together, with the common model 00, so IC6 asks that merging all three bases gives 00 alone. But in $\Psi_1 \sqcup \Psi_2$ the worlds 00 and 10 still both have worst distance 1, and the result is $\neg b$. The maximum cannot see that $\Psi_1$ prefers 00, because the worst source of the joined profile hides it. The sum gives 00, since 00 has total distance 1 and 10 has total distance 2.

## Known algorithms

- **Distance-based merging.** For a distance $d$ between worlds and an aggregation function $f$, set $d(w, \Psi) = f(d(w, K_1), \ldots, d(w, K_m))$ and return the models of $\mu$ with the least value. Konieczny and Pino Pérez show that with the Hamming distance, the sum gives a majority operator that satisfies IC0 to IC8 and Maj, Gmax gives an arbitration operator that satisfies IC0 to IC8 and Arb, and the maximum satisfies IC0 to IC5, IC7 and IC8 but not IC6.
- **On model sets.** Compute $d(w, K_i)$ for every world by a [multi-source BFS](/multi-source-bfs/) on the cube from the models of $K_i$, as in [Dalal's operator](/dalal-revision/), in $O(n \cdot 2^n)$ time for each base. Aggregate and take the minimum over the models of $\mu$. The total time is $O(m \cdot n \cdot 2^n)$ for $m$ bases over $n$ atoms.
- **On formulas.** For the sum, ask a SAT solver whether some model of $\mu$ has total distance at most $k$, with one copy of the atoms for each base and a cardinality constraint on the disagreements. A binary search on $k$ finds the least value, and a [MaxSAT](/max-sat/) solver can find it directly.

## Bounds

For the sum with the Hamming distance, "does $\Delta^{\Sigma}_\mu(\Psi)$ entail $q$" is in $\mathrm{P}^{\mathrm{NP}[O(\log n)]}$: the least total distance is at most $n \cdot m$, so a binary search with SAT calls finds it in $O(\log(nm))$ calls, and one more call looks for a model of $\mu \wedge \neg q$ at that distance. It is also hard for this class, because a profile with one base is Dalal's revision, whose entailment problem is $\mathrm{P}^{\mathrm{NP}[O(\log n)]}$-complete (Eiter and Gottlob 1992, Theorem 6.9). This argument is ours, from the two facts cited. Other distances and aggregations place the problem elsewhere in the [polynomial hierarchy](/polynomial-hierarchy/). Every operator that satisfies IC2 is coNP-hard: with one base and $\mu$ both tautologies, the result is a tautology, and the question becomes whether $q$ is valid.

## Reductions

- **Revision as merging.** As shown above, merging with one base is a KM revision. So every lower bound for a revision operator applies to the matching merging operator.
- **Merging as revision of the conjunction.** When the bases are jointly consistent with $\mu$, IC2 forces the plain conjunction, as R2 does for revision. Merging only differs from revision when there is conflict.
- **Merging and update.** [Update](/belief-update/) treats each model of one base separately. Merging treats each base separately and then compares worlds across bases, so it is the opposite split.

## Applications

- Fusion of data from several sensors or several databases that disagree, with physical laws or schema rules as constraints.
- Group decision making, where the bases are the wishes of the members and $\mu$ lists the feasible plans.
- Combining expert opinions or knowledge bases in a shared ontology.
- Merging the results of several classifiers or annotators when their outputs are logical descriptions.

## References
