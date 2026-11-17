---
tag: 7EMCZC
kind: definition
slug: stoichiometric-matrix
name: Stoichiometric matrix
aliases:
- stoichiometry matrix
area: biology/systems-biology
level: intro
summary: The matrix S with a row per species and a column per reaction whose entries are the net molecules made, so dx/dt = S v(x).
prereqs: [rank, rank-nullity-theorem]
see_also: [chemical-reaction-network, mass-action-kinetics, flux-balance-analysis, elementary-flux-mode, deficiency-zero-theorem, petri-net, chemical-master-equation, reduced-row-echelon-form]
sources:
  - book: isbn:9783030038571
    title: Martin Feinberg, Foundations of Chemical Reaction Network Theory, Applied Mathematical Sciences 202, Springer, 2019
    locator: Chapter 3 (reaction networks, kinetics and the induced differential equations, the stoichiometric subspace and the compatibility classes) and Chapter 6 (complexes, linkage classes and the deficiency)
  - book: isbn:9781107038851
    title: Bernhard O. Palsson, Systems Biology, Constraint-based Reconstruction and Analysis, Cambridge University Press, 2015
    locator: Chapter 9, The stoichiometric matrix (the four fundamental subspaces, conservation pools and steady-state fluxes)
  - paper: doi:10.1007/BF00251225
    title: F. Horn and R. Jackson, General mass action kinetics, Archive for Rational Mechanics and Analysis 47(2), 1972, 81-116
    locator: the description of a network by its complexes, and the factorization of the species formation rate through the complex space
---

The stoichiometric matrix $S$ of a [chemical reaction network](/chemical-reaction-network/) has one row for each species and one column for each reaction. The entry $S_{ij}$ is the net number of molecules of species $i$ that one event of reaction $j$ makes, so it is negative for a species that the reaction uses up. With a vector $v(x)$ of reaction rates, the concentrations obey $dx/dt = S\, v(x)$. The matrix holds only the bookkeeping of the network: the [rank](/rank/) of $S$ and its null spaces give the conservation laws and the steady-state fluxes, for every rate law.

## Definition

Let $X_1, \ldots, X_n$ be the species and $R_1, \ldots, R_m$ the reactions. Reaction $R_j$ is
$$\sum_{i=1}^{n} \alpha_{ij} X_i \;\longrightarrow\; \sum_{i=1}^{n} \beta_{ij} X_i,$$
with integers $\alpha_{ij}, \beta_{ij} \ge 0$: the reactant and the product coefficients. The *stoichiometric matrix* is the $n \times m$ integer matrix
$$S = (S_{ij}), \qquad S_{ij} = \beta_{ij} - \alpha_{ij}.$$
Column $j$ is the *reaction vector* $\nu_j = \beta_{\cdot j} - \alpha_{\cdot j}$, the change of the state when $R_j$ fires once. A reversible reaction is either two columns $\nu$ and $-\nu$, or one column with a signed net rate; say which. This page uses two columns.

**The rate equation.** Let $x \in \mathbb{R}^n_{\ge 0}$ be the concentrations and $v_j(x) \ge 0$ the rate of $R_j$, for example the [mass action](/mass-action-kinetics/) rate. Then
$$\frac{dx}{dt} = S\, v(x), \qquad x(t) = x(0) + S\, \xi(t), \quad \xi(t) = \int_0^t v(x(\tau))\, d\tau.$$
The vector $\xi(t)$ is the extent of each reaction. In the stochastic model the same identity holds for counts: $X(t) = X(0) + S\, N(t)$, where $N_j(t)$ is the number of times $R_j$ fired up to time $t$ (see [chemical master equation](/chemical-master-equation/)). So in both models the change of the state stays in the column space of $S$.

**The four subspaces.** Let $s = \operatorname{rank} S$.
- The *stoichiometric subspace* is $\operatorname{im} S \subseteq \mathbb{R}^n$, of dimension $s$. For each start $x_0$, the *stoichiometric compatibility class* is $(x_0 + \operatorname{im} S) \cap \mathbb{R}^n_{\ge 0}$, and its *positive* part is $(x_0 + \operatorname{im} S) \cap \mathbb{R}^n_{> 0}$. A solution never leaves the class of its start.
- A *conservation law* is a row vector $w$ with $w^{\mathsf T} S = 0$. Then $w^{\mathsf T} x(t) = w^{\mathsf T} x(0)$ for all $t$, because $w^{\mathsf T} S \xi(t) = 0$. The left null space has dimension $n - s$ by the [rank-nullity theorem](/rank-nullity-theorem/) applied to $S^{\mathsf T}$. A conservation law with $w \ge 0$ is a *conserved pool*, such as the total enzyme.
- A *steady-state flux* is a vector $v$ with $S v = 0$: the rates add up so that no concentration changes. The null space $\ker S$ has dimension $m - s$. Constraint-based models such as [flux balance analysis](/flux-balance-analysis/) search the cone $\{v : S v = 0, \ v_{\text{irr}} \ge 0\}$, and, after each reversible reaction is split into a forward and a backward reaction, its extreme rays are the [elementary flux modes](/elementary-flux-mode/).
- The row space $\operatorname{im} S^{\mathsf T}$ is the orthogonal complement of $\ker S$.

A system with $n - s$ independent conservation laws can be reduced to $s$ independent variables. Find a basis of each null space with exact [Gaussian elimination](/gaussian-elimination/) to the [reduced row echelon form](/reduced-row-echelon-form/); the entries are integers, so rational arithmetic gives an exact answer in $O(n\, m \min(n, m))$ arithmetic operations.

**Conventions.** Some books, in particular on [Petri nets](/petri-net/), write the transpose, with one row per reaction. Some metabolic models leave out the external species, so that $S v = 0$ has nonzero solutions through "exchange" reactions $\emptyset \to X$ and $X \to \emptyset$.

## Examples and non-examples

**The enzyme scheme.** Take $E + S \rightleftharpoons C \to E + P$, written as three reactions: $R_1: E + S \to C$, $R_2: C \to E + S$ and $R_3: C \to E + P$. Order the species as $(S, E, C, P)$. Then
$$S = \begin{pmatrix} -1 & 1 & 0 \\ -1 & 1 & 1 \\ 1 & -1 & -1 \\ 0 & 0 & 1 \end{pmatrix}.$$
The first two columns are $\nu$ and $-\nu$, and the third is independent of them, so $s = 2$. There are $n - s = 4 - 2 = 2$ independent conservation laws:
$$w_1 = (0, 1, 1, 0): \ [E] + [C] = E_T, \qquad w_2 = (1, 0, 1, 1): \ [S] + [C] + [P] = S_T.$$
Check: $w_1^{\mathsf T}$ times column 3 is $1 - 1 = 0$, and $w_2^{\mathsf T}$ times column 3 is $-1 + 1 = 0$. The null space has dimension $m - s = 1$ and is spanned by $(1, 1, 0)$: the only steady flux runs $R_1$ and $R_2$ at the same rate and $R_3$ not at all. So this network has no steady state in which product forms, as long as substrate remains. This is the scheme of [Michaelis-Menten kinetics](/michaelis-menten-kinetics/).

**A linear pathway with exchange.** Take $R_1: \emptyset \to A$, $R_2: A \to B$ and $R_3: B \to \emptyset$, with species $(A, B)$:
$$S = \begin{pmatrix} 1 & -1 & 0 \\ 0 & 1 & -1 \end{pmatrix}.$$
Here $s = 2 = n$, so there is no conservation law, and $\ker S$ is spanned by $(1, 1, 1)$: at steady state the three fluxes are equal. This is the smallest case of the flux balance constraint $S v = 0$.

**Non-example: $S$ does not show a catalyst.** The reactions $A + E \to B + E$ and $A \to B$ have the same column $(-1, 0, 1)$ for the species $(A, E, B)$. The entry for $E$ is $0$ in both, because $E$ is used and made again. So $S$ alone does not give the rate law: with mass action the first rate is $k[A][E]$ and the second is $k[A]$. A rate law needs the reactant coefficients $\alpha_{ij}$ as well.

**Non-example: $S$ does not determine the complexes.** The reactions $2A \to A + B$ and $A \to B$ both have the column $(-1, 1)$ for $(A, B)$. The first network has the complexes $2A$ and $A + B$, the second $A$ and $B$. The column of $S$ is the difference of the two complexes, and different pairs give the same difference. Results that depend on the complexes, such as the [deficiency zero theorem](/deficiency-zero-theorem/), cannot be read from $S$ alone.

**Non-example: the coefficient is not the reactant count.** For $2A \to A + B$ the entry for $A$ is $1 - 2 = -1$, not $-2$. The mass action rate is still $k[A]^2$, with the exponent $\alpha = 2$.

## Related definitions

- **Complexes and the factorization of $S$.** A *complex* is the left or the right side of a reaction, a vector in $\mathbb{Z}^n_{\ge 0}$. Let $c$ be the number of distinct complexes, $Y$ the $n \times c$ matrix whose columns are the complexes, and $I_a$ the $c \times m$ incidence matrix of the reaction graph, with $-1$ at the source complex and $+1$ at the target complex of each reaction. Then $S = Y I_a$, because column $j$ of $Y I_a$ is (target complex) minus (source complex). Horn and Jackson (1972) built their theory on this factorization.
- **Linkage classes and deficiency.** The *linkage classes* are the connected components of the reaction graph on the complexes; let $l$ be their number. The *deficiency* is $\delta = c - l - s$. It is never negative: the incidence matrix of a directed graph with $c$ vertices and $l$ components has rank $c - l$, and $s = \operatorname{rank}(Y I_a) \le \operatorname{rank} I_a$. For the enzyme scheme, the complexes are $E + S$, $C$ and $E + P$, so $c = 3$, $l = 1$, $s = 2$ and $\delta = 0$.
- **The reactant matrix.** The matrix $(\alpha_{ij})$ gives the exponents of the mass action rates. Together with $S$ it describes the network fully.
- **The Petri net view.** A reaction network is a [Petri net](/petri-net/) with places for species and transitions for reactions; the incidence matrix of the net is $S$ (or its transpose), and the state equation $M = M_0 + S\, N$ is the counting identity above. A place invariant of the net is a conservation law.
- **Elementary flux modes.** The support-minimal vectors of the flux cone $\{v : S v = 0, v_{\text{irr}} \ge 0\}$; see [elementary flux mode](/elementary-flux-mode/).

## References
