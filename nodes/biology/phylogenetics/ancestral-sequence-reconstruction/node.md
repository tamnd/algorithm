---
tag: GHTCE8
kind: problem
slug: ancestral-sequence-reconstruction
name: Ancestral sequence reconstruction
aliases:
- ancestral state reconstruction
- joint and marginal reconstruction
area: biology/phylogenetics
level: advanced
summary: Infer the sequences at the internal nodes of a known tree, by parsimony or under a substitution model, either one node at a time (marginal) or all nodes at once (joint).
prereqs: [felsenstein-pruning, phylogenetic-likelihood]
see_also: [small-parsimony, fitch-algorithm, sankoff-algorithm, maximum-likelihood-phylogeny, max-product, viterbi-algorithm, forward-backward-algorithm, ml-tree-np-hard]
sources:
  - paper: doi:10.1093/oxfordjournals.molbev.a026369
    title: Tal Pupko, Itsik Pe'er, Ron Shamir and Dan Graur, A fast algorithm for joint reconstruction of ancestral amino acid sequences, Molecular Biology and Evolution 17(6), 2000
    locator: pp. 890 to 896 (the dynamic program for the joint reconstruction, linear in the number of taxa)
  - paper: "Ziheng Yang, Sudhir Kumar and Masatoshi Nei, A new method of inference of ancestral nucleotide and amino acid sequences, Genetics 141(4), 1995, pages 1641 to 1650"
    locator: the empirical Bayes approach to ancestral states, with the marginal and the joint reconstruction
  - book: isbn:9780199602612
    title: Ziheng Yang, Molecular Evolution, A Statistical Approach, Oxford University Press, 2014
    locator: Chapter 4, Maximum likelihood methods (the section on the reconstruction of ancestral states)
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 16, Likelihood methods (the section on inferring ancestral states)
---

Ancestral sequence reconstruction asks for the sequences at the internal nodes of a known tree, given the sequences at its leaves. The answer is a guess about extinct ancestors, and there are two kinds of guess. The *marginal* reconstruction picks, at each node, the state with the largest posterior probability given the leaves. The *joint* reconstruction picks the one assignment of states to all internal nodes that has the largest probability. Both come from the same tree likelihood that [Felsenstein's pruning algorithm](/felsenstein-pruning/) computes, and both take $O(n k^2)$ time per site on a tree with $n$ nodes and $k$ states. They can give different answers, and the example below shows a case. With parsimony instead of a substitution model, the problem is the [small parsimony problem](/small-parsimony/).

## In plain words

We know the family tree of some living species and their genes. We want the genes of their shared ancestors, which we cannot see. For each position in the gene, we ask which letter each ancestor most likely had.

There are two ways to ask this. We can take one ancestor at a time and ask for its most likely letter. Or we can ask for the most likely full story, with one letter for every ancestor at once. These two answers are often the same, but not always. The letter that is best for one ancestor alone can be part of no best full story.

A third, older way uses no probabilities. It picks the letters that need the fewest changes along the tree. It ignores the branch lengths, so on a tree with very unequal branches it can disagree with the other two.

## Definition

**Input.** A rooted tree $T$ with leaf set $X$ and internal nodes $V$, a substitution model with $k$ states that gives each edge $(u, w)$ a transition matrix $P_w$ with $P_w(a, b)$ the probability of state $b$ at $w$ given state $a$ at $u$, a root distribution $\pi$, and an alignment with a state $x_v$ at each leaf $v$ for each site. Sites are independent, so it is enough to state the problem for one site. For a time-reversible model, the tree can be rooted at any node, and $\pi$ is the stationary distribution.

**The joint probability.** For an assignment $s : V \to \{1, \ldots, k\}$ of states to the internal nodes, together with the leaf states $x$,

$$\Pr(s, x) = \pi_{s(\rho)} \prod_{(u, w) \in E(T)} P_w\bigl(s(u), s(w)\bigr),$$

where $\rho$ is the root and $s(w) = x_w$ at a leaf. The site likelihood is $\Pr(x) = \sum_s \Pr(s, x)$.

**Joint reconstruction.** Find $s^* = \arg\max_s \Pr(s, x)$, which is also the assignment of largest posterior $\Pr(s \mid x) = \Pr(s, x) / \Pr(x)$.

**Marginal reconstruction.** For each internal node $v$, find $\hat s(v) = \arg\max_a \Pr(s(v) = a \mid x)$, where

$$\Pr(s(v) = a \mid x) = \frac{1}{\Pr(x)} \sum_{s \,:\, s(v) = a} \Pr(s, x).$$

**Parsimony reconstruction.** For a cost $\delta(a, b)$ of a change, find $s$ that minimizes $\sum_{(u, w)} \delta(s(u), s(w))$. This is the [small parsimony problem](/small-parsimony/).

The tree, its branch lengths and the model parameters are input. In practice they are first estimated, for example by [maximum likelihood](/maximum-likelihood-phylogeny/), and then held fixed. Yang, Kumar and Nei call this approach *empirical Bayes*, because the posterior uses estimated parameters as if they were known.

## Variants

- **Joint versus marginal.** The joint reconstruction answers "what is the most probable history", and is the right choice when the states at several nodes are used together, for example to count the changes on each branch. The marginal reconstruction answers "what was the state at this node", and is the right choice when one ancestor is the object of study. The marginal posterior also measures the uncertainty at each node.
- **Whole sequences.** Under independent sites, the reconstruction of a sequence is the reconstruction of each site. Identical site patterns give identical answers, so each pattern is done once.
- **Rate heterogeneity.** Under a [discrete gamma model](/rate-heterogeneity/), the marginal posterior is a mixture over the rate classes, weighted by their posterior. A joint reconstruction can either sum over the rate class or maximize over it as one more unknown.
- **Parsimony.** [Fitch's algorithm](/fitch-algorithm/) for unit costs and the [Sankoff algorithm](/sankoff-algorithm/) for any cost table solve the parsimony version. They need no model, but they ignore branch lengths and give no probabilities.
- **Bayesian reconstruction.** The empirical Bayes posterior ignores the error in the tree and the parameters. A full Bayesian analysis averages the posterior of the ancestral states over trees and parameters, for example by sampling them with [Bayesian phylogenetic inference](/bayesian-phylogenetic-inference/). A node must then be defined by a set of leaves, since it does not exist in every sampled tree.
- **Sampling ancestors.** Instead of the single best state, one can draw assignments from the posterior $\Pr(s \mid x)$. A downward pass that draws each node state given its parent and the upward vectors does this exactly. Samples show the uncertainty that the best guess hides.
- **Insertions and deletions.** Substitution models have no gap state, so a gap is usually treated as missing data. Whether a position existed in an ancestor is a separate question that needs an indel model.
- **Morphological and discrete characters.** The same definitions apply to any discrete character with a Markov model on the tree, such as the presence of a trait. The name "ancestral state reconstruction" is usual for this case.

## Examples

Take the rooted tree with root $r$, whose children are the internal node $u$ and the leaf $z$, where $u$ has the leaves $x$ and $y$. The model is [JC69](/jukes-cantor-model/) with uniform $\pi$. The branches above $u$, $z$ and $x$ are short, with $t = -\tfrac34 \ln 0.9 \approx 0.079$ substitutions per site, so they keep a state with probability $0.925$ and change to each other state with probability $0.025$. The branch above $y$ is long, with $t = -\tfrac34 \ln 0.2 \approx 1.207$, so it keeps a state with probability $0.4$ and changes to each other state with probability $0.2$. The site is $x = \text{A}$, $y = \text{C}$ and $z = \text{C}$.

The 16 assignments $(s(r), s(u))$ have these posteriors, with the site likelihood $\Pr(x) = 0.004459375$:

| $(s(r), s(u))$ | posterior | story |
|---|---|---|
| (C, C) | 0.4797 | one change, on the short branch to $x$ |
| (A, A) | 0.2398 | two changes, on the long branch to $y$ and the short branch to $z$ |
| (C, A) | 0.2398 | two changes, on the short branch to $u$ and the long branch to $y$ |
| each of the 13 others | at most 0.0065 | |

Summing the rows gives the marginal posteriors:

| node | A | C | G | T |
|---|---|---|---|---|
| $r$ | 0.2405 | 0.7325 | 0.0135 | 0.0135 |
| $u$ | 0.4926 | 0.4807 | 0.0133 | 0.0133 |

So the **joint** reconstruction is $(s(r), s(u)) = (\text{C}, \text{C})$, with posterior 0.4797. The **marginal** reconstruction is $s(r) = \text{C}$ and $s(u) = \text{A}$, an assignment with posterior 0.2398, only half that of the joint answer. A change on the long branch to $y$ is cheap, so two stories with $s(u) = \text{A}$ use it, and together they outweigh the single best story at $u$. State C at $u$ has almost all its mass in one assignment.

**Parsimony on the same site.** [Fitch's algorithm](/fitch-algorithm/) gives the set $\{\text{A}, \text{C}\}$ at $u$ and $\{\text{C}\}$ at $r$, and its traceback gives (C, C), the only assignment with one change. So here parsimony agrees with the joint reconstruction, and both disagree with the marginal one at $u$.

## Known algorithms

| method | output | time per site | source |
|---|---|---|---|
| [Fitch's algorithm](/fitch-algorithm/) | a most parsimonious assignment, unit costs, binary tree | $O(n k)$ | Fitch 1971 |
| [Sankoff algorithm](/sankoff-algorithm/) | a least-cost assignment, any costs | $O(n k^2)$ | Sankoff 1975 |
| pruning plus a downward pass | all marginal posteriors | $O(n k^2)$ | Yang, Kumar and Nei 1995 |
| Pupko's dynamic program | the joint reconstruction | $O(n k^2)$ | Pupko et al. 2000 |
| exhaustive enumeration | either, as a check | $O(k^{|V|} n)$ | |

**Marginal reconstruction.** The upward pass is [Felsenstein's pruning](/felsenstein-pruning/), which gives for each node $v$ the vector $L_v(a) = \Pr(\text{leaves below } v \mid s(v) = a)$. A downward pass from the root gives $O_v(a) = \Pr(\text{leaves outside the subtree of } v, s(v) = a)$, with $O_\rho = \pi$ and, for a child $w$ of $v$,

$$O_w(b) = \sum_a O_v(a) \Bigl(\prod_{w' \ne w} M_{w'}(a)\Bigr) P_w(a, b),$$

where the product is over the other children $w'$ of $v$ and $M_{w'}(a) = \sum_c P_{w'}(a, c) L_{w'}(c)$ is the message of the upward pass. Then $\Pr(s(v) = a \mid x) = O_v(a) L_v(a) / \Pr(x)$. For a reversible model, one can instead reroot the tree at each node in turn and run the pruning pass, at a cost of $O(n^2 k^2)$; the two passes give all nodes in $O(n k^2)$.

**Joint reconstruction (Pupko et al.).** Replace the sum in the pruning pass by a maximum, and remember the argument. For a leaf $w$ with parent state $i$, set $L_w(i) = P_w(i, x_w)$. For an internal non-root node $w$ with children $w_1, \ldots, w_d$,

$$L_w(i) = \max_j P_w(i, j) \prod_{c=1}^{d} L_{w_c}(j), \qquad C_w(i) = \text{the } j \text{ that attains the maximum}.$$

At the root, pick $s(\rho) = \arg\max_a \pi_a \prod_c L_{w_c}(a)$, and then set $s(w) = C_w(s(\text{parent}(w)))$ in preorder. The value at the root is $\max_s \Pr(s, x)$. This is the [max-product](/max-product/) form of the pruning pass, and it is the tree version of the [Viterbi algorithm](/viterbi-algorithm/), while the marginal reconstruction is the tree version of the [forward-backward algorithm](/forward-backward-algorithm/). The Python implementation of this page implements both and checks them against enumeration of all $k^{|V|}$ assignments.

## Bounds

- **Time.** Each edge does $k$ maximizations or sums of length $k$, so both reconstructions take $\Theta(n k^2)$ per site pattern, and $\Theta(m n k^2)$ for $m$ distinct patterns. This is linear in the size of the input, which holds $n - 1$ matrices of $k^2$ entries. For DNA $k = 4$, for amino acids $k = 20$, and for codons $k = 61$.
- **Space.** The joint reconstruction keeps $k$ values and $k$ pointers per node, so $\Theta(n k)$. The marginal reconstruction keeps the upward and downward vectors, also $\Theta(n k)$.
- **Exhaustive search.** There are $k^{|V|}$ assignments, which is $4^{n - 1}$ on a rooted binary tree with $n$ leaves of DNA. Pupko et al. replaced such searches by their linear dynamic program.
- **Unknown tree.** If the tree is not given and one maximizes over trees and internal states together, the problem is *ancestral maximum likelihood*, which is NP-hard (Addario-Berry et al. 2004). Maximizing over trees alone is also NP-hard; see [maximum likelihood tree inference is NP-hard](/ml-tree-np-hard/).

## Reductions

- **Joint reconstruction is weighted parsimony.** Taking $-\ln$ turns the joint probability into the sum $-\ln \pi_{s(\rho)} + \sum_{(u, w)} -\ln P_w(s(u), s(w))$. So the joint reconstruction is the [Sankoff algorithm](/sankoff-algorithm/) with a cost table $-\ln P_w$ that depends on the edge, plus a cost $-\ln \pi$ at the root. Pupko's dynamic program is this Sankoff run.
- **Short branches give parsimony.** Under JC69 with all branches of the same small length $t$, a change costs about $\ln(1 / t)$ and a non-change about 0, so the joint reconstruction tends to a most parsimonious assignment as $t \to 0$. With unequal branches the costs differ by edge, and the two methods can disagree.
- **Marginal reconstruction is inference on a tree graphical model.** The tree with its matrices is a directed graphical model, and the marginals are what [belief propagation](/belief-propagation/) computes exactly on a tree.

## Applications

- **Resurrecting ancestral proteins.** Researchers synthesize an inferred ancestral protein in the lab and measure its properties, to test hypotheses about how a function evolved. The marginal reconstruction at the node of interest is the usual choice, with alternative states at sites where the posterior is low.
- **Mapping changes on branches.** The joint reconstruction places each substitution on a branch, which gives counts of changes per branch and per site, for example to find sites that changed several times.
- **Evolution of traits.** For morphological or ecological characters, the posterior at internal nodes says when a trait appeared and how certain that is.
- **Epidemiology.** For viral and bacterial trees, the states at internal nodes can be locations or hosts, which gives estimates of where and in which host a lineage started.

**Known issue.** The most probable state at every site gives one sequence without its uncertainty. Such a sequence tends to have the common states at the uncertain sites, so its properties can be biased. Sampling from the posterior, or testing several reconstructions, reduces this risk.

## References
