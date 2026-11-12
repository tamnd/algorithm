---
tag: WABGYW
kind: concept
slug: long-branch-attraction
name: Long-branch attraction
aliases:
- Felsenstein zone
area: biology/phylogenetics
level: core
summary: Parsimony tends to join two long branches as sisters, because parallel changes on them look like shared history. On some trees it picks the wrong tree with probability tending to 1.
prereqs: [maximum-parsimony, substitution-model]
see_also: [parsimony-informative-site, maximum-likelihood-phylogeny, quartet, jukes-cantor-model, law-of-large-numbers, rate-heterogeneity, phylogenetic-tree-reconstruction, neighbor-joining]
sources:
  - paper: doi:10.2307/2412923
    title: Joseph Felsenstein, Cases in which parsimony or compatibility methods will be positively misleading, Systematic Zoology 27(4), 1978, 401-410
    locator: the four-taxon tree with two long branches, and the region of branch lengths where parsimony and compatibility converge to the wrong tree
  - paper: doi:10.1093/sysbio/42.3.247
    title: John P. Huelsenbeck and David M. Hillis, Success of phylogenetic methods in the four-taxon case, Systematic Biology 42(3), 1993, 247-264
    locator: the consistency and the simulated accuracy of many methods over the space of four-taxon trees with two long branches
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 9, Statistical properties of parsimony, the section Consistency and parsimony
---

Long-branch attraction is the tendency of [maximum parsimony](/maximum-parsimony/), and of some other methods, to put two long branches of a tree next to each other, whatever their true relation. Two lineages that change a lot often reach the same state by chance. Parsimony counts such parallel changes as one shared change, so it takes them as evidence that the two lineages are related. Felsenstein (1978) showed that on a tree of four taxa with two long branches that are not sisters, this effect is not only noise: as the number of sites grows, parsimony returns the wrong tree with probability tending to 1. So parsimony is not statistically consistent. The region of branch lengths where this happens is called the Felsenstein zone.

## In plain words

Suppose two species on the tree are far from their relatives and have changed a lot, and they are not close relatives of each other. At many positions of their genes, both have changed. With four letters, or two in the simplest model, they often land on the same letter by chance.

Parsimony looks for the tree that needs the fewest changes. A letter that two species share costs less if the two species sit together on the tree. So the chance matches pull the two long branches together. The true signal, which needs a change on a short inner branch, is weaker than this noise.

More data does not help. With more sites, the chance matches keep their lead, and parsimony becomes more and more sure of the wrong tree.

## The idea

**Parsimony on four taxa.** On the taxa $A, B, C, D$ there are three unrooted trees, one for each split $AB \mid CD$, $AC \mid BD$ and $AD \mid BC$. A site of the form $xxyy$ costs 1 on its own tree and 2 on the other two, and every other kind of site costs the same on all three trees ([parsimony-informative site](/parsimony-informative-site/)). So parsimony picks the tree whose informative pattern occurs most often among the sites.

**The model.** Take the two-state symmetric model: each site has state 0 or 1, the state at the root is 0 or 1 with probability $\tfrac12$ each, and on each edge $e$ the state flips with probability $p_e < \tfrac12$, independently over the edges and the sites. With a rate of change and a length $t$ for the edge, $p_e = (1 - e^{-2t})/2$. Let the true tree be $AB \mid CD$, with an inner edge from $u$, the parent of $A$ and $B$, to $v$, the parent of $C$ and $D$. Let the two edges to $A$ and $C$ be long, with flip probability $p$, and let the edges to $B$ and $D$ and the inner edge be short, with flip probability $q$.

**The pattern probabilities.** Write $\varepsilon_e \in \{0, 1\}$ for the flip on edge $e$. Then $A = u \oplus \varepsilon_A$, $C = u \oplus \varepsilon_I \oplus \varepsilon_C$, and so on. The pattern of $AB \mid CD$, with $A = B \ne C = D$, needs $\varepsilon_A = \varepsilon_B$, $\varepsilon_C = \varepsilon_D$ and $\varepsilon_A \oplus \varepsilon_I \oplus \varepsilon_C = 1$. Adding the four choices of $(\varepsilon_A, \varepsilon_C)$ gives

$$P_{AB} = q\bigl[(1 - p)^2 (1 - q)^2 + p^2 q^2\bigr] + 2p(1 - p) q (1 - q)^2.$$

In the same way, the pattern of $AC \mid BD$ needs $\varepsilon_A \ne \varepsilon_B$ and both $\varepsilon_A \oplus \varepsilon_I \oplus \varepsilon_C$ and $\varepsilon_B \oplus \varepsilon_I \oplus \varepsilon_D$ equal to 0, and

$$P_{AC} = (1 - q)\bigl[(1 - p)^2 q^2 + p^2 (1 - q)^2\bigr] + 2p(1 - p) q^2 (1 - q).$$

The pattern of $AD \mid BC$ has the probability $P_{AD}$ of the same form. Expanding gives two identities:

$$P_{AC} - P_{AB} = (1 - 2q)\bigl(p^2 - q(1 - q)\bigr), \qquad P_{AC} - P_{AD} = (1 - 2q)(p - q)^2.$$

**Inconsistency.** Since $q < \tfrac12$, the first identity shows that $P_{AC} > P_{AB}$ exactly when $p^2 > q(1 - q)$, and the second shows $P_{AC} \ge P_{AD}$, with equality only if $p = q$. Let $N_{AB}$, $N_{AC}$ and $N_{AD}$ be the numbers of sites of the three patterns among $m$ sites. By the [law of large numbers](/law-of-large-numbers/), $N_{AC}/m \to P_{AC}$ and so on. So if $p^2 > q(1 - q)$ and $p \ne q$, then $N_{AC}$ is the largest count with probability tending to 1, and parsimony returns $AC \mid BD$, the tree that joins the two long branches. If $p^2 < q(1 - q)$, parsimony returns the true tree with probability tending to 1. In words: parallel flips on the two long branches, with probability about $p^2$, beat the single flip on the short inner edge, with probability about $q$.

**What goes wrong.** Parsimony does not model the chance of two parallel changes. [Maximum likelihood](/maximum-likelihood-phylogeny/) with the true [substitution model](/substitution-model/) accounts for it and is consistent on this tree. Distance methods such as [neighbor joining](/neighbor-joining/) are consistent if the distances are corrected by the right model, as with the [Jukes-Cantor](/jukes-cantor-model/) correction for that model. Compatibility methods, which on four taxa also pick the split of the most frequent $xxyy$ pattern, fail in the same way, as the title of Felsenstein's paper says.

## Examples

**Inside the zone.** Let $p = \tfrac25$ and $q = \tfrac1{10}$, which are edge lengths of about 0.805 and 0.112 in the model above. Then $p^2 = \tfrac{4}{25} > q(1 - q) = \tfrac{9}{100}$. Exact computation with fractions gives

| pattern | supports | probability |
|---|---|---|
| $A = B \ne C = D$ | $AB \mid CD$ (true) | $341/5000 = 0.0682$ |
| $A = C \ne B = D$ | $AC \mid BD$ | $621/5000 = 0.1242$ |
| $A = D \ne B = C$ | $AD \mid BC$ | $261/5000 = 0.0522$ |

The two identities check: $P_{AC} - P_{AB} = \tfrac{280}{5000} = \tfrac45 \cdot \tfrac{7}{100}$, and $P_{AC} - P_{AD} = \tfrac{360}{5000} = \tfrac45 \cdot \tfrac{9}{100}$. The wrong pattern is almost twice as frequent as the true one. Summing the multinomial distribution of the three counts gives the chance that parsimony returns each tree as its only best tree:

| sites $m$ | 10 | 100 | 500 |
|---|---|---|---|
| $P$(parsimony returns $AB \mid CD$) | 0.1575 | 0.0728 | 0.0016 |
| $P$(parsimony returns $AC \mid BD$) | 0.4086 | 0.8552 | 0.9977 |

With more sites, parsimony becomes more sure of the wrong tree.

**Outside the zone.** Let $p = \tfrac15$ and $q = \tfrac1{10}$. Now $p^2 = \tfrac{4}{100} < \tfrac{9}{100}$, and $P_{AB} = 389/5000$, $P_{AC} = 189/5000$, $P_{AD} = 149/5000$. The chance that parsimony returns the true tree alone is 0.3596, 0.8087 and 0.9951 for 10, 100 and 500 sites.

**On the boundary.** For $p = \tfrac3{10}$ and $q = \tfrac1{10}$, or $p = \tfrac25$ and $q = \tfrac15$, $p^2 = q(1 - q)$ and $P_{AB} = P_{AC}$. Parsimony then returns $AB \mid CD$ and $AC \mid BD$ with the same probability: 0.4756 each for the first pair and 0.4622 each for the second pair, at 500 sites. It does not converge to one tree.

**The exact computation.** This program computes the three probabilities with exact fractions, by a sum over the states of $u$ and $v$.

```python
from fractions import Fraction as F
from itertools import product

def pattern_probs(p, q):
    """P(AB|CD pattern), P(AC|BD pattern), P(AD|BC pattern) on the tree AB|CD."""
    flip = {"A": p, "B": q, "C": p, "D": q}
    prob = {}
    for a, b, c, d in product((0, 1), repeat=4):
        total = F(0)
        for u, v in product((0, 1), repeat=2):
            pr = F(1, 2) * (q if u != v else 1 - q)
            for leaf, node, name in ((a, u, "A"), (b, u, "B"), (c, v, "C"), (d, v, "D")):
                pr *= flip[name] if leaf != node else 1 - flip[name]
            total += pr
        prob[a, b, c, d] = total
    ab = prob[0, 0, 1, 1] + prob[1, 1, 0, 0]
    ac = prob[0, 1, 0, 1] + prob[1, 0, 1, 0]
    ad = prob[0, 1, 1, 0] + prob[1, 0, 0, 1]
    return ab, ac, ad

print(pattern_probs(F(2, 5), F(1, 10)))  # 341/5000, 621/5000, 261/5000
```

## Where it is used

- **Choosing a method.** Long-branch attraction is the main argument for model-based methods, [maximum likelihood](/maximum-likelihood-phylogeny/) and Bayesian inference, over parsimony for molecular data with unequal rates of change.
- **Sampling taxa.** Adding taxa that branch off a long branch breaks it into shorter pieces, which is a standard way to reduce the effect.
- **Removing fast sites.** Leaving out the fastest sites, such as the third codon positions, or modeling [rate heterogeneity](/rate-heterogeneity/), lowers the number of chance matches.
- **Outgroups.** A distant outgroup is a long branch. It can attract a fast ingroup lineage to the base of the tree, so the choice of outgroup matters.
- **Tests of methods.** Four-taxon trees in the Felsenstein zone are a standard test case in simulations of phylogenetic methods, as in Huelsenbeck and Hillis (1993). The name Felsenstein zone for this region of branch lengths is usually traced to their paper.

## References
