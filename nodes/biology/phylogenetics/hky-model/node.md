---
tag: 70W1M5
kind: model
slug: hky-model
name: HKY85 model
aliases:
- Hasegawa-Kishino-Yano model
- HKY
area: biology/phylogenetics
level: advanced
summary: A DNA model with unequal base frequencies (from F81) and a faster rate kappa for transitions (from K80). The rate to base j is kappa beta pi_j for a transition and beta pi_j otherwise.
history:
  year: 1985
  people: [Masami Hasegawa, Hirohisa Kishino, Taka-aki Yano]
  note: Hasegawa, Kishino and Yano gave the model in a study that dated the split of humans and apes with a molecular clock on mitochondrial DNA.
prereqs: [kimura-two-parameter-model, felsenstein-81-model]
see_also: [substitution-model, jukes-cantor-model, gtr-model, rate-heterogeneity, phylogenetic-likelihood, felsenstein-pruning, molecular-clock, maximum-likelihood-phylogeny]
sources:
  - paper: doi:10.1007/BF02101694
    title: Masami Hasegawa, Hirohisa Kishino and Taka-aki Yano, Dating of the human-ape splitting by a molecular clock of mitochondrial DNA, Journal of Molecular Evolution 22 (1985)
    locator: pp. 160 to 174 (the model with transition and transversion rates times the base frequencies, and its transition probabilities)
  - book: isbn:9780199602612
    title: Ziheng Yang, Molecular Evolution, A Statistical Approach, Oxford University Press, 2014
    locator: Chapter 1, Section 1.2 (HKY85, F84 and TN93 among the models with unequal base frequencies)
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 13, Models of DNA evolution
---

The HKY85 model of Hasegawa, Kishino and Yano is a [substitution model](/substitution-model/) for DNA that joins the two ideas of the simpler models. Like [F81](/felsenstein-81-model/), it lets the four bases have different stationary frequencies $\pi_A, \pi_C, \pi_G, \pi_T$. Like [K80](/kimura-two-parameter-model/), it makes transitions (A with G, C with T) faster than transversions by a factor $\kappa$. The rate from base $i$ to base $j$ is $\kappa \beta \pi_j$ for a transition and $\beta \pi_j$ for a transversion, so it has four free parameters: $\kappa$ and three frequencies. The transition probabilities still have a closed form. HKY85 with a gamma model of [rate heterogeneity](/rate-heterogeneity/) is one of the most used DNA models in practice.

## The machine

**States and rates.** The states are A, C, G, T. Write $\pi_R = \pi_A + \pi_G$ for the purine frequency and $\pi_Y = \pi_C + \pi_T$ for the pyrimidine frequency. For $i \ne j$,

$$Q_{ij} = \begin{cases} \kappa \beta \pi_j & \text{if } i \to j \text{ is a transition}, \\ \beta \pi_j & \text{if } i \to j \text{ is a transversion}, \end{cases}$$

and $Q_{ii} = -\sum_{j \ne i} Q_{ij}$. Hasegawa, Kishino and Yano wrote the two rates as $\alpha \pi_j$ and $\beta \pi_j$; then $\kappa = \alpha / \beta$.

**Stationary and reversible.** Detailed balance holds because $\pi_i Q_{ij}$ is $\kappa \beta \pi_i \pi_j$ or $\beta \pi_i \pi_j$, which is symmetric in $i$ and $j$. So $\pi$ is the stationary distribution and the model is reversible.

**Scaling.** The expected rate at stationarity is $2\beta \left[\kappa (\pi_A \pi_G + \pi_C \pi_T) + \pi_R \pi_Y\right]$. Programs set

$$\beta = \frac{1}{2\kappa (\pi_A \pi_G + \pi_C \pi_T) + 2 \pi_R \pi_Y},$$

so that branch lengths are in expected substitutions per site.

**Transition probabilities.** The eigenvalues of $Q$ are

$$0, \quad -\beta, \quad -\beta (\pi_R \kappa + \pi_Y), \quad -\beta (\pi_Y \kappa + \pi_R).$$

Let $j$ be a base in class $C$ (the purines R or the pyrimidines Y), let $\Pi_C$ be the frequency of that class and $\Pi_{\bar C} = 1 - \Pi_C$ the frequency of the other class. Then:

- If $i$ is in the other class (a transversion), $P_{ij}(t) = \pi_j \left(1 - e^{-\beta t}\right)$.
- If $i$ is in the same class as $j$,

$$P_{ij}(t) = \pi_j + \pi_j \frac{\Pi_{\bar C}}{\Pi_C} e^{-\beta t} + \frac{\delta_{ij} \Pi_C - \pi_j}{\Pi_C} e^{-\beta (\Pi_C \kappa + \Pi_{\bar C}) t}.$$

For example, $P_{AA}(t) = \pi_A + \pi_A \tfrac{\pi_Y}{\pi_R} e^{-\beta t} + \tfrac{\pi_G}{\pi_R} e^{-\beta (\pi_R \kappa + \pi_Y) t}$, and $P_{AG}(t) = \pi_G + \pi_G \tfrac{\pi_Y}{\pi_R} e^{-\beta t} - \tfrac{\pi_G}{\pi_R} e^{-\beta (\pi_R \kappa + \pi_Y) t}$. The structure is the same as for K80: the class of a base (purine or pyrimidine) follows a two-state chain, and the term $e^{-\beta t}$ comes from it.

## What it counts

**Kappa against the observed ratio.** The parameter $\kappa$ is the ratio of the rates per pair of bases. The ratio of the expected numbers of transitions and transversions at stationarity is a different number:

$$R = \frac{\kappa (\pi_A \pi_G + \pi_C \pi_T)}{\pi_R \pi_Y}.$$

With uniform frequencies, $R = \kappa / 2$, because each base has one transition partner and two transversion partners. Papers that report a "transition and transversion ratio" can mean either $\kappa$ or $R$, and the two can differ by a factor of 2 or more.

**Distances.** HKY85 has no distance formula as simple as those of K80 and F81. Programs estimate the distance between two sequences by maximizing their two-sequence likelihood over $d$ (and $\kappa$). The closely related TN93 model of Tamura and Nei, with separate rates for the two kinds of transition, and the F84 model of Felsenstein do have explicit distance formulas.

## Relation to other models

- **It contains K80 and F81.** With equal frequencies, HKY85 is [K80](/kimura-two-parameter-model/). With $\kappa = 1$, it is [F81](/felsenstein-81-model/). With both, it is [JC69](/jukes-cantor-model/). So the two chains JC69 $\subset$ K80 $\subset$ HKY85 and JC69 $\subset$ F81 $\subset$ HKY85 meet here.
- **It is inside TN93 and GTR.** TN93 gives the transitions A with G and C with T two different rates. [GTR](/gtr-model/) lets all six pairs have their own rate. HKY85 is GTR with $r_{AG} = r_{CT} = \kappa$ and the other four exchangeabilities equal to 1. A likelihood ratio test of HKY85 against GTR has four degrees of freedom.
- **F84 is a sibling.** Felsenstein's F84 model, used in the PHYLIP programs, also has unequal frequencies and one extra parameter for transitions, but in a different form. Neither of F84 and HKY85 contains the other, and both contain F81 and K80.

## Known results in the model

**A worked matrix.** Take $\pi = (0.1, 0.2, 0.3, 0.4)$ in the order A, C, G, T and $\kappa = 4$. Then $\pi_A \pi_G + \pi_C \pi_T = 0.03 + 0.08 = 0.11$, $\pi_R \pi_Y = 0.4 \times 0.6 = 0.24$, and $\beta = 1/(0.88 + 0.48) = 0.735294$. The rate matrix is

| | A | C | G | T |
|---|---|---|---|---|
| A | $-1.323529$ | $0.147059$ | $0.882353$ | $0.294118$ |
| C | $0.073529$ | $-1.470588$ | $0.220588$ | $1.176471$ |
| G | $0.294118$ | $0.147059$ | $-0.735294$ | $0.294118$ |
| T | $0.073529$ | $0.588235$ | $0.220588$ | $-0.882353$ |

Its eigenvalues are $0$, $-0.735294$, $-1.617647$ and $-2.058824$, as the formula gives with $\pi_R \kappa + \pi_Y = 2.2$ and $\pi_Y \kappa + \pi_R = 2.8$. At $t = 0.2$,

| | A | C | G | T |
|---|---|---|---|---|
| A | $0.772179$ | $0.027351$ | $0.145766$ | $0.054703$ |
| C | $0.013676$ | $0.756753$ | $0.041027$ | $0.188545$ |
| G | $0.048589$ | $0.027351$ | $0.869357$ | $0.054703$ |
| T | $0.013676$ | $0.094272$ | $0.041027$ | $0.851025$ |

The closed form and the matrix exponential agree on every entry. From A, the transition to G has probability $0.146$, more than the two transversions together. Here $R = 4 \times 0.11 / 0.24 = 1.833$, while $\kappa = 4$.

**Likelihood and model choice.** The [phylogenetic likelihood](/phylogenetic-likelihood/) under HKY85 is computed by [pruning](/felsenstein-pruning/) with these closed-form matrices. In model selection over the nested family, HKY85 and HKY85+$\Gamma$ are often chosen for real data, and GTR+$\Gamma$ is the other common choice.

## References
