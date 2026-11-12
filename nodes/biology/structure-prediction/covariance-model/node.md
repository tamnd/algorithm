---
tag: 9XQKJ4
kind: model
slug: covariance-model
name: Covariance model
aliases:
- CM
- Infernal model
area: biology/structure-prediction
level: advanced
summary: "A stochastic context-free grammar built from the consensus structure of an RNA family. It scores both sequence and base pairs, and CYK aligns a sequence to it in O(M L^2 + B L^3) time."
prereqs: [probabilistic-context-free-grammar, profile-hmm, rna-secondary-structure]
see_also: [cyk-algorithm, inside-outside-algorithm, rna-homology-search, hmmer, sankoff-rna-algorithm, pseudoknot, nussinov-algorithm, multiple-sequence-alignment]
sources:
  - paper: doi:10.1093/nar/22.11.2079
    title: Sean R. Eddy and Richard Durbin, RNA sequence analysis using covariance models, Nucleic Acids Research 22(11), 1994, pages 2079 to 2088
    locator: the guide tree of node types, the states of each node, the CYK alignment algorithm and its cost, and training from unaligned sequences
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 10, Section 10.3, Covariance models, SCFG-based RNA profiles (from page 277); Chapter 9 for stochastic context-free grammars
  - paper: doi:10.1093/bioinformatics/btt509
    title: Eric P. Nawrocki and Sean R. Eddy, Infernal 1.1, 100-fold faster RNA homology searches, Bioinformatics 29(22), 2013, pages 2933 to 2935
    locator: the Infernal 1.1 software, its filter pipeline of profile HMM stages and HMM-banded CM alignment, and the speed against Infernal 1.0
  - paper: doi:10.1093/nar/gkg006
    title: Sam Griffiths-Jones, Alex Bateman, Mhairi Marshall, Ajay Khanna and Sean R. Eddy, Rfam, an RNA family database, Nucleic Acids Research 31(1), 2003, pages 439 to 441
    locator: the Rfam database of RNA families, each with a seed alignment, a consensus structure and a covariance model
  - paper: doi:10.1371/journal.pcbi.0030056
    title: Eric P. Nawrocki and Sean R. Eddy, Query-dependent banding (QDB) for faster RNA similarity searches, PLoS Computational Biology 3(3), 2007, e56
    locator: the time and memory of CYK alignment and of a database scan with window W
  - paper: doi:10.1186/1471-2105-3-18
    title: Sean R. Eddy, A memory-efficient dynamic programming algorithm for optimal alignment of a sequence to an RNA secondary structure, BMC Bioinformatics 3, 2002, article 18
    locator: the divide and conquer CYK alignment that cuts the memory of CM alignment
---

A covariance model (CM) is a [stochastic context-free grammar](/probabilistic-context-free-grammar/) built from the consensus secondary structure of an RNA family, with one group of states for each consensus position or base pair. A pair state emits two bases at once, the two sides of a consensus base pair, with a score for each of the 16 base combinations, so the model rewards a pair that changes from G-C to A-U in a family member (a compensatory change, or covariation) as well as an unchanged one. Eddy and Durbin introduced it in 1994 as the RNA analogue of a [profile hidden Markov model](/profile-hmm/): a CM built from a structure with no base pairs is a profile HMM. CMs are the models of the Rfam database and of the Infernal software for [RNA structural homology search](/rna-homology-search/).

## The machine

### The structure model

The input to model building is a consensus [RNA secondary structure](/rna-secondary-structure/) over $N$ consensus columns, written in dot-bracket form: a set of nested base pairs with no [pseudoknots](/pseudoknot/). Each pair state can emit any of the 16 base pairs, including non-canonical ones, each with its own score, so the model does not fix Watson-Crick and G-U pairs; it learns how often each pair appears at each consensus pair. There is no minimum hairpin size and no energy model: the scores are log-odds ratios of emission and transition probabilities against a background, estimated from a family alignment with pseudocounts or priors.

### The guide tree

The consensus structure is turned into a binary tree of nodes, the guide tree. Read the structure from the outside in, on an interval $[a, b)$ of columns:

- if column $a$ pairs with column $b - 1$, make a MATP node (match pair) and go on with $[a + 1, b - 1)$;
- else if column $a$ is unpaired, make a MATL node (match left) and go on with $[a + 1, b)$;
- else if column $b - 1$ is unpaired, make a MATR node (match right) and go on with $[a, b - 1)$;
- else columns $a$ and $b - 1$ are paired with other columns, so the interval holds two separate stems; make a BIF node (bifurcation) whose children start the two parts, $[a, k)$ with a BEGL node and $[k, b)$ with a BEGR node, where $k$ is one past the partner of $a$;
- when the interval is empty, make an END node.

The tree starts with a ROOT node. The order of the tests above is a convention, and other orders give equivalent models.

### The states

Each node expands into a fixed set of states:

| node | states | meaning |
|---|---|---|
| ROOT | S, IL, IR | start, insert left, insert right |
| MATP | MP, ML, MR, D, IL, IR | both bases, left base only, right base only, neither, inserts |
| MATL | ML, D, IL | the base, or a delete, and an insert |
| MATR | MR, D, IR | the base, or a delete, and an insert |
| BIF | B | split into two subsequences |
| BEGL | S | start of the left part |
| BEGR | S, IL | start of the right part, insert |
| END | E | end, emits nothing |

In a MATP node, ML and MR keep only one side of the consensus pair, which models a base deleted on one side. A state of type P emits a pair $(x_i, x_{j-1})$, L emits $x_i$ on the left, R emits $x_{j-1}$ on the right, S and D emit nothing, B splits, and E ends. Each non-insert state moves to the inserts of its own node or to the first states of the next node; an insert state can loop to itself. So the number of states is

$$M = 3 + 6\,\#\mathrm{MATP} + 3\,(\#\mathrm{MATL} + \#\mathrm{MATR}) + \#\mathrm{BIF} + \#\mathrm{BEGL} + 2\,\#\mathrm{BEGR} + \#\mathrm{END},$$

which is about $3N$ for $N$ consensus columns. As a grammar, each state is a nonterminal and each state type is a production of one form: $W_v \to x_i W_y x_{j-1}$ for P, $W_v \to x_i W_y$ for L, $W_v \to W_y x_{j-1}$ for R, $W_v \to W_y$ for S and D, $W_v \to W_y W_z$ for B, and $W_v \to \varepsilon$ for E.

### What a parse is

A parse of a sequence $x$ of length $L$ is a derivation from the root state that generates $x$. In it, the P states give the base pairs of $x$, the L and R states give its unpaired bases, and the states of each node say which consensus column each base aligns to. So one parse is at the same time a structure for $x$ and an alignment of $x$ to the family. Its score is the sum of its transition and emission scores.

## What it counts

- **States and cells.** The size of a model is its number of states $M$ and of bifurcation states $B$. A dynamic program over a sequence of length $L$ has one cell for each state $v$ and each subsequence $x[i:j)$, $0 \le i \le j \le L$, so $M (L + 1)(L + 2)/2$ cells.
- **Operations.** A non-bifurcation cell takes the best of at most 6 children, a constant. A bifurcation cell at $x[i:j)$ tries the $j - i + 1$ split points $k$. Over all subsequences, one bifurcation state does $\sum_{d=0}^{L} (L - d + 1)(d + 1) = \binom{L + 3}{3}$ split terms. So CYK on a whole sequence costs $\Theta(M L^2 + B L^3)$ time and $\Theta(M L^2)$ memory, in every case.
- **Scores.** Scores are log-odds ratios; the integer toy scores on this page are in arbitrary units. Local search reports a score for each hit, and the significance of a score is an E-value from a fitted distribution, not a property of the model.

## Relation to other models

- **Profile HMM.** A CM of a structure with no base pairs is a chain of MATL nodes with match, delete and insert states, which is a [profile HMM](/profile-hmm/). Adding MATP nodes adds the pair emissions that make the grammar context free. [HMMER](/hmmer/) searches with profile HMMs, and Infernal uses a profile HMM of the CM as a fast filter.
- **SCFG.** A CM is a [probabilistic context-free grammar](/probabilistic-context-free-grammar/) in a fixed normal form designed so that each production emits at most one pair. The [CYK algorithm](/cyk-algorithm/) and the [inside-outside algorithm](/inside-outside-algorithm/) apply to it after small changes: emissions happen on the left, the right or both sides of the current subsequence, not at leaves of a Chomsky normal form tree.
- **Folding models.** The [Nussinov algorithm](/nussinov-algorithm/) is the CYK of a small grammar that knows nothing about a family. A CM is a grammar specialised to one family, with one set of states per consensus position. Energy based folding, as in the [Zuker algorithm](/zuker-algorithm/), uses physical parameters instead of family statistics.
- **Simultaneous alignment and folding.** The [Sankoff algorithm](/sankoff-rna-algorithm/) aligns and folds two sequences with no model. Aligning a sequence to a CM is the same task with one side fixed to a known consensus structure, which is why it costs about $L^3$ instead of the $n^6$ of two free sequences.
- **Pseudoknots.** A CM cannot express [pseudoknots](/pseudoknot/), because crossing pairs are not context free. Families with pseudoknots are modelled by their nested part.

## Known results in the model

### CYK alignment

Write $\alpha_v(i, j)$ for the best score of a parse of $x[i:j)$ that starts in state $v$, and $t_v(w)$ and $e_v$ for the transition and emission scores. States are numbered so that every child of a state has a larger number or is the same insert state on a shorter subsequence.

```pseudo id=main
CM-CYK(x, model)                           ▷ x of length L; states 0 .. M − 1, 0 is the root
L1  for v ← M − 1 down to 0 do
L2      for d ← 0 to L do                  ▷ d: length of the subsequence
L3          for i ← 0 to L − d do
L4              j ← i + d
L5              if v is E then α_v(i, j) ← 0 if d = 0, else −∞
L6              else if v is B with children y, z then α_v(i, j) ← max over i ≤ k ≤ j of α_y(i, k) + α_z(k, j)
L7              else if v is S or D then α_v(i, j) ← max over children w of t_v(w) + α_w(i, j)
L8              else if v is P and d ≥ 2 then α_v(i, j) ← e_v(x_i, x_{j−1}) + max over w of t_v(w) + α_w(i + 1, j − 1)
L9              else if v is L and d ≥ 1 then α_v(i, j) ← e_v(x_i) + max over w of t_v(w) + α_w(i + 1, j)
L10             else if v is R and d ≥ 1 then α_v(i, j) ← e_v(x_{j−1}) + max over w of t_v(w) + α_w(i, j − 1)
L11             else α_v(i, j) ← −∞
L12 return α_0(0, L)
```

Each case reads only cells of a larger state, or of the same insert state on a shorter subsequence, so the order of lines L1 to L3 fills each cell after the cells it needs. The result is the score of the best parse, and a traceback from $\alpha_0(0, L)$ gives the parse, its base pairs and its alignment. The correctness of this recursion is the correctness of CYK for a grammar: by induction on the state number and the length, $\alpha_v(i, j)$ is the best score over all derivations of $x[i:j)$ from $v$, because every derivation begins with exactly one production of the form of its state.

### Costs

- **Alignment of a whole sequence.** $\Theta(M L^2 + B L^3)$ time and $\Theta(M L^2)$ memory, with $M \approx 3N$. For a sequence about as long as the model, $L \approx N$, this is $O(N^3)$ memory, which limits plain CYK to short RNAs.
- **Memory.** Eddy (2002) gave a divide and conquer version of the alignment, modelled on the Myers and Miller methods for linear sequence alignment. It needs $O(N^2 \log N)$ memory, for a small constant factor more time.
- **Inside and outside.** Replacing max by a sum of probabilities gives the inside algorithm, the total probability of $x$ under the model, with the same cost. Inside and outside together give the posterior probability that a base aligns to a state, and the expectations for training by expectation maximization.
- **Search.** Nawrocki and Eddy (2007) give the cost of a scan for local hits of length at most $W$ as $O(M W + B W^2)$ memory and $O(L (M W + B W^2))$ time, where $L$ is now the length of the database. The filters and bands that make search practical are on the [homology search](/rna-homology-search/) page.

### Training

A CM is built from a family alignment with an annotated consensus structure: count the emissions and transitions of each state over the aligned sequences and add priors. Eddy and Durbin also gave an iterative method that starts from unaligned sequences: align them to the current model, re-estimate the structure from the mutual information of pairs of columns, rebuild the model, and repeat.

### Example

Take the consensus structure `((...))` with the consensus sequence `GGAAACC`. The guide tree is ROOT, MATP, MATP, MATL, MATL, MATL, END, so the model has $M = 3 + 2 \cdot 6 + 3 \cdot 3 + 1 = 25$ states and no bifurcation. With a toy scoring scheme (an MP state scores 3 for a Watson-Crick pair, 1 for G-U and $-4$ otherwise; an ML or MR state scores 1 for the consensus base and $-1$ otherwise; inserts emit with score 0; a move into an insert or a delete costs 3, an insert self-loop costs 1, other moves are free), CYK gives:

| sequence | best score | best parse |
|---|---|---|
| `GGAAACC` | 9 | pairs (0, 6) and (1, 5); three loop matches |
| `CUAAAAG` | 9 | pairs C-G and U-A at the same places; the compensatory changes cost nothing |
| `GGAAAACC` | 6 | as the consensus, with one insert ($-3$) |
| `GGACC` | 1 | two pairs and one loop match, two deletes ($-6$) |
| `GGAAACA` | 4 | the last A is a right insert of the root ($-3$), then one pair, one MATP with only its left base, and the loop |
| `AAAAAAA` | $-3$ | no good pair exists |

The second row is what a profile HMM cannot do: the bases at both ends differ from the consensus, but each pair is still a valid pair, so the CM scores the sequence as high as the consensus itself. For this model and $L = 7$ the table has $25 \cdot 8 \cdot 9 / 2 = 900$ cells. A local scan of `UUCUAAAAGUU` with window 9 finds the hit `CUAAAAG` at positions 2 to 8 with score 9.

The structure `(.)(.)` needs a bifurcation. Its guide tree is ROOT, BIF, then BEGL, MATP, MATL, END for the first stem and BEGR, MATP, MATL, END for the second, with $M = 27$ states and $B = 1$. On a sequence of length 6 the table has $27 \cdot 7 \cdot 8 / 2 = 756$ cells and the bifurcation does $\binom{9}{3} = 84$ split terms.

### Software and databases

Infernal implements CMs. Its version 1.1 (2013) puts a pipeline of profile HMM filters and HMM-banded CM alignment in front of the full CM search, and Nawrocki and Eddy report it as about 100 times faster than version 1.0 on their benchmark. Rfam (2003 and later) stores RNA families, each as a seed alignment with a consensus structure and a CM, and annotates genomes by searching them with Infernal.

## References
