---
tag: D8KK9G
kind: definition
slug: elementary-flux-mode
name: Elementary flux mode
aliases:
- elementary mode
- EFM
area: biology/systems-biology
level: advanced
summary: A minimal steady-state flux vector that obeys irreversibility, so no smaller set of its reactions can carry a steady flux.
prereqs: [stoichiometric-matrix, nullspace]
see_also: [elementary-flux-mode-enumeration, flux-balance-analysis, constraint-based-metabolic-modeling, extreme-point, polyhedron, matroid, rank-nullity-theorem, farkas-lemma]
sources:
  - paper: doi:10.1142/S0218339094000131
    title: Stefan Schuster and Claus Hilgetag, On elementary flux modes in biochemical reaction systems at steady state, Journal of Biological Systems 2(2), 1994, 165-182
    locator: the definition by steady state, sign feasibility and support minimality, and the relation to extreme rays for irreversible networks
  - paper: doi:10.1038/73786
    title: Stefan Schuster, David A. Fell and Thomas Dandekar, A general definition of metabolic pathways useful for systematic organization and analysis of complex metabolic networks, Nature Biotechnology 18(3), 2000, 326-332
    locator: elementary modes as the general definition of a metabolic pathway, with examples
  - paper: doi:10.1186/1471-2105-5-175
    title: Julien Gagneur and Steffen Klamt, Computation of elementary modes, a unifying framework and the new binary approach, BMC Bioinformatics 5, 2004, 175
    locator: the splitting of reversible reactions, the correspondence with extreme rays, and the rank test for elementary modes
  - paper: doi:10.1016/j.biosystems.2008.06.015
    title: Vicente Acuña, Flavio Chierichetti, Vincent Lacroix, Alberto Marchetti-Spaccamela, Marie-France Sagot and Leen Stougie, Modes and cuts in metabolic networks, complexity and algorithms, BioSystems 95(1), 2009, 51-60
    locator: Section 3.2 (counting elementary modes is #P-complete), and the results that one mode is found in polynomial time while a shortest mode is NP-hard to find
---

An elementary flux mode is a smallest way for a metabolic network to run at steady state. It is a flux vector $e$ with $S e = 0$ that respects the direction of every irreversible reaction and that uses a set of reactions so small that no proper subset of it can carry a non-zero steady flux. Schuster and Hilgetag (1994) introduced elementary flux modes as a formal definition of a metabolic pathway. Every steady-state flux vector of the network is a non-negative sum of elementary flux modes, so they describe all the routes through the network. The modes of a network are finite in number, but the number can grow exponentially with the size of the network. They are listed by [elementary flux mode enumeration](/elementary-flux-mode-enumeration/).

## Definition

Let $S$ be the $n \times m$ [stoichiometric matrix](/stoichiometric-matrix/) of a network with $n$ internal metabolites and $m$ reactions, and let $\text{Irr} \subseteq \{1, \ldots, m\}$ be the set of irreversible reactions. The *flux cone* is

$$C = \{ v \in \mathbb{R}^m : S v = 0, \; v_j \ge 0 \text{ for } j \in \text{Irr} \} .$$

The *support* of a vector is $\operatorname{supp}(v) = \{ j : v_j \ne 0 \}$. A vector $e$ is an *elementary flux mode* (EFM) if

1. $e \in C$ (steady state and sign feasibility),
2. $e \ne 0$, and
3. there is no $v \in C$ with $v \ne 0$ and $\operatorname{supp}(v) \subsetneq \operatorname{supp}(e)$ (support minimality).

Modes are counted up to a positive factor: $e$ and $\lambda e$ with $\lambda > 0$ are the same mode. In the code of the enumeration page, each mode is written as the unique vector of coprime integers in its ray.

**The rank test.** For a non-zero $e \in C$ with support $Q$, let $S_Q$ be the columns of $S$ in $Q$. Then $e$ is an EFM if and only if $\ker S_Q$ has dimension 1, that is, $\operatorname{rank} S_Q = |Q| - 1$. This is a theorem. One direction: if $\ker S_Q$ had a second vector $w$ independent of $e$, move from $e$ along $-w$ (or $w$) until the first coordinate becomes zero; all other coordinates keep their signs, so the result is in $C$, non-zero, and has a smaller support. The other direction: if $v \in C$ had a smaller support, both $v$ and $e$ would be in the one-dimensional space $\ker S_Q$, so $v$ would be a multiple of $e$ with the same support, a contradiction. So a mode is determined by its support up to a factor, and the number of modes is at most twice the number of subsets of reactions, so it is finite.

**Decomposition.** Every $v \in C$ is a non-negative combination of EFMs whose signs agree with $v$ on every reaction. This is a theorem (a conformal decomposition): if $v$ is not a mode, take a mode $e$ with $\operatorname{supp}(e) \subseteq \operatorname{supp}(v)$ and the same signs as $v$, subtract the largest multiple $t e$ that keeps the signs, and repeat on $v - t e$, whose support is smaller. A mode with support inside $\operatorname{supp}(v)$ and the signs of $v$ exists by the same argument as in the rank test, applied to the cone of vectors with the signs of $v$. So the modes generate the cone $C$. The converse fails: a non-negative sum of modes is in $C$, but it is usually not a mode.

**Extreme rays.** If every reaction is irreversible, $C$ is a pointed cone in the non-negative orthant, and its EFMs are exactly its extreme rays: an extreme ray of $\{v \ge 0 : S v = 0\}$ is a non-zero vector whose tight constraints $v_j = 0$ have rank $m - 1$ together with the rows of $S$, which is the rank test above. With reversible reactions, $C$ may contain a line, and then the EFMs are not extreme rays: a mode made of reversible reactions only, and its negative, are both modes. After each reversible reaction is split into a forward and a backward irreversible copy, the EFMs of the original network correspond one to one to the extreme rays of the split cone, except the trivial two-cycles that run one reaction forward and backward (Gagneur and Klamt 2004).

## Examples and non-examples

**Network E.** Take three metabolites $A$, $B$, $C$ and six reactions:

| reaction | equation | reversible |
|---|---|---|
| R1 | $\emptyset \to A$ | no |
| R2 | $A \to B$ | no |
| R3 | $A \leftrightarrow C$ | yes |
| R4 | $B \to C$ | no |
| R5 | $C \to \emptyset$ | no |
| R6 | $B \to \emptyset$ | no |

It has four EFMs, written as $(v_1, \ldots, v_6)$:

- $e_1 = (1, 1, 0, 0, 0, 1)$: R1, R2, R6, from the uptake to the secretion of $B$;
- $e_2 = (1, 0, 1, 0, 1, 0)$: R1, R3 forward, R5;
- $e_3 = (1, 1, 0, 1, 1, 0)$: R1, R2, R4, R5;
- $e_4 = (0, 1, -1, 1, 0, 0)$: the internal cycle $A \to B \to C \to A$, with R3 backward.

Each one passes the rank test: for $e_1$, the columns of R1, R2 and R6 have rank 2 in a space of three columns.

**Non-example: a sum of modes.** $e_1 + e_2 = (2, 1, 1, 0, 1, 1)$ is a steady state that obeys the signs, but it is not elementary: its support contains the support of $e_1$. Its columns R1, R2, R3, R5, R6 have rank 3, so the kernel on this support has dimension 2.

**A mode that is a sum of two modes.** $e_3 = e_2 + e_4$, yet $e_3$ is a mode. The R3 terms cancel, so the support of the sum is smaller than the union of the supports. This shows that a mode is defined by its support, not by being "not a sum".

**Non-example: a wrong sign.** $-e_4 = (0, -1, 1, -1, 0, 0)$ is in $\ker S$, and its support passes the rank test, but it runs the irreversible reactions R2 and R4 backward. It is not in $C$, so it is not a mode. In an all-reversible network both $e_4$ and $-e_4$ would be modes.

**Network N of the FBA page.** With uptake EX_A, two respiration reactions RESP1 and RESP2 ($A \to 2E$), fermentation FERM ($A \to E + P$), secretion EX_P and growth BIO ($A + E \to$), all irreversible, the modes are $(3, 1, 0, 0, 0, 2)$, $(3, 0, 1, 0, 0, 2)$ and $(2, 0, 0, 1, 1, 1)$: growth by RESP1, by RESP2, or by fermentation. Their yields of growth per substrate are $\frac{2}{3}$, $\frac{2}{3}$ and $\frac{1}{2}$, and the FBA optimum $\frac{20}{3}$ at uptake 10 is reached by the two respiration modes.

**Exponential count.** A chain of $k$ "diamonds", in which each step $M_{i-1} \to M_i$ can use one of two parallel reactions, has $2k + 2$ reactions and $2^k$ modes: one for each choice of reaction at each step.

## Related definitions

- **Extreme pathways.** Schilling, Letscher and Palsson (2000) defined extreme pathways, the extreme rays of the cone after a fixed splitting of internal reversible reactions. Every extreme pathway is an EFM, but a network can have EFMs that are not extreme pathways.
- **Minimal generating sets.** For a cone with a line (reversible reactions), a smallest set of generators is a basis of the line part plus the extreme rays of the rest. It is in general smaller than the set of EFMs and is not unique.
- **Minimal cut sets.** A minimal set of reactions whose removal blocks a target reaction in every steady state. The minimal cut sets are the minimal hitting sets of the EFMs that contain the target, which links them to [hitting set](/hitting-set/) problems. Acuña and co-authors (2009) also study their complexity.
- **Circuits.** If every reaction is reversible, $C = \ker S$, and the supports of the EFMs are the circuits of the linear [matroid](/matroid/) of the columns of $S$: the minimal dependent sets of columns.
- **Steady-state flux vector.** Any $v \in C$, as used in [flux balance analysis](/flux-balance-analysis/). If all reactions are irreversible and only one uptake $u$ is bounded, by $v_u \le U$, the vertices of the flux polyhedron other than 0 are the modes with $v_u > 0$, scaled to $v_u = U$. So an FBA optimum can then be taken to be a scaled mode.

## References
