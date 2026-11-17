---
title: The caller lists the supported haplotypes, the pair HMM sums over all alignments, and the genotypes are the MAP calls of the stated model
proves: [correctness]
status: full
---

The caller has three parts, and this file proves what each part computes. The model is a simplification, and the genotype likelihoods of line L8 are an approximation of the full marginal likelihood; the last section says which steps are exact and which are not.

**Setting.** The reference of the region is $\mathit{ref}$, with no repeated $k$-mer (the code raises ValueError otherwise). The reads are strings on the forward strand, each base with a Phred quality $Q$ and error rate $e = 10^{-Q/10}$. A *$(k+1)$-mer* of a string $x$ is a substring $x[t{:}t + k + 1]$. Its count is its number of occurrences, over all the reads.

## The candidate haplotypes

Line L1 builds the graph whose nodes are $k$-mers and whose edges are the $(k+1)$-mers of the reads and of $\mathit{ref}$, from the first $k$ bases to the last $k$ bases. Line L2 keeps every edge of $\mathit{ref}$ and every other edge with count at least $c_{\min}$. Line L3 lists, by depth-first search from the source $\mathit{ref}[0{:}k]$, the paths to the sink $\mathit{ref}[|\mathit{ref}| - k{:}]$ that do not visit a node twice, and spells each path as a string.

**Lemma 1 (supported haplotypes are found).** Let $h$ be a string that starts with the source and ends with the sink, has no repeated $k$-mer, and whose every $(k+1)$-mer is a $(k+1)$-mer of $\mathit{ref}$ or has count at least $c_{\min}$. Then $h$ is in the list $H$ of line L3, unless the list has reached its cap of max_haplotypes strings. The reference is always in $H$.

*Proof.* The $k$-mers of $h$ in order are a walk in the graph, and each step is an edge that line L2 keeps. The $k$-mers are distinct, so the walk is a simple path. The sink is the last $k$-mer of $h$ and is not repeated, so the path meets the sink only at its end. The search of line L3 tries, from each node, every kept edge to a node that is not on the current path, and records the path when it reaches the sink. By induction on the length of the path, it reaches every simple path from the source that meets the sink only at its end, so it reaches the path of $h$, unless it stopped at the cap. Two adjacent $k$-mers overlap in $k - 1$ bases, so the spelled string is $h$. The reference satisfies the conditions, and the code puts it first. $\square$

The converse also holds: every string in $H$ is spelled by a simple path of kept edges, so each of its $(k+1)$-mers is in $\mathit{ref}$ or has count at least $c_{\min}$. A true haplotype is missed when one of its $(k+1)$-mers has fewer supporting occurrences (low coverage or errors at one place), when it has a repeated $k$-mer, or when it differs from the reference in the first or last $k$ bases of the region.

## The pair HMM

For a read $r$ of length $L$ and a haplotype $h$ of length $n$, an *alignment path* starts in state M at a position $j$ of $h$ chosen with probability $1/n$, emits $r$ from left to right, and ends after the last read base in state M or I. State M emits the next read base against the next base of $h$, with probability $1 - e$ for the same base and $e/3$ for another. State I emits the next read base alone with probability $1/4$. State D uses the next base of $h$ and emits nothing. The transitions are $M \to M$ with $1 - 2\delta$, $M \to I$ and $M \to D$ with $\delta$ each, $I \to I$ and $D \to D$ with $\gamma$, and $I \to M$ and $D \to M$ with $1 - \gamma$. The bases of $h$ before the start and after the last used base are free. The probability of a path is the product of its start, transition and emission probabilities, and PAIR-HMM returns $\ln \sum$ over all alignment paths.

**Lemma 2 (forward recurrence).** For $i \ge 1$ and $1 \le j \le n$, the values of lines P3 to P5 are $X[i][j] = \sum$ of the probabilities of the path prefixes that have emitted $r[0{:}i]$, whose last state is $X$, and whose last used base of $h$ is $h[j - 1]$ (for I, the last used base before the insertion).

*Proof.* By induction in the order of the loops of lines P1 and P2. The last step of a prefix fixes the cell of the step before it: an M step at $(i, j)$ comes from $(i - 1, j - 1)$, an I step from $(i - 1, j)$ and a D step from $(i, j - 1)$. At $i = 1$, a prefix in M has just started, so its probability is $\frac1n$ times the emission, which is line P3 for $i = 1$; an I at $i = 1$ would need an M before it with no read base, so it has probability 0, as line P4 gives with the row before it all zero. For $i > 1$, an M step can follow M, I or D, with the transition probabilities of the model, which is line P3. An I step follows M or I and emits $1/4$, which is line P4. A D step follows M or D in the same row and emits nothing, which is line P5. The sum over the prefixes with a given last step is the sum over the previous state of the earlier value times the transition and the emission, so each line is the claim by the induction hypothesis. $\square$

**Theorem 1 (pair HMM).** Line P6 returns $\ln P(r \mid h)$, the log of the sum of the probabilities of all alignment paths.

*Proof.* A full alignment path ends after its last read base in M or I, at some last used base $j$. By Lemma 2 with $i = L$, the sum over all of them is $\sum_j (M[L][j] + I[L][j])$. $\square$

The tests compare this value with a sum over the paths listed one by one. The sum is over the alignments, so the value is a likelihood, not the score of the best alignment.

## Genotypes

Line L4 computes $\ell[r][h] = \ln P(r \mid h)$ for every read and candidate. In the diploid model, each read comes from one of the two haplotypes $h_a, h_b$ of the sample, with probability $1/2$ each, and the reads are independent given the pair. So

$$\ln P(\text{reads} \mid h_a, h_b) = \sum_r \ln\bigl(\tfrac12 e^{\ell[r][h_a]} + \tfrac12 e^{\ell[r][h_b]}\bigr).$$

**Lemma 3 (best pair).** Line L5 returns a pair $\{h_a, h_b\}$, possibly with $h_a = h_b$, that maximizes this likelihood over all pairs of candidates.

*Proof.* The loop visits every unordered pair with repetition and keeps the first one whose value is larger than the best so far by more than $10^{-9}$. $\square$

Line L6 aligns each non-reference candidate to $\mathit{ref}$ with affine gaps, writes each difference as a VCF-style variant shifted to the left, and lists the candidates that carry each variant. For a variant $v$ with carriers $C_v$, line L8 sets

$$\mathrm{GL}_v(g) = \sum_r \ln\Bigl(\tfrac g2 \max_{h \in C_v} e^{\ell[r][h]} + \bigl(1 - \tfrac g2\bigr) \max_{h \notin C_v} e^{\ell[r][h]}\Bigr), \quad g = 0, 1, 2.$$

**Theorem 2 (calls).** For each variant $v$, line L9 returns the posterior $P(g \mid \text{reads}) \propto \pi(g)\, e^{\mathrm{GL}_v(g)}$ with the prior $\pi = (1 - \frac32\theta, \theta, \frac\theta2)$, and the genotype $\hat g$ of largest posterior, the smallest on ties. Line L10 returns the variants with $\hat g > 0$.

*Proof.* The formula of line L8 is the [genotype likelihood](/genotype-likelihood/) of a site whose two alleles are represented by one haplotype each: a read comes from a chromosome with the variant with probability $g/2$. The code forms each mixture with log-sum-exp, which is an identity. Line L9 adds $\ln \pi(g)$, normalizes by log-sum-exp, and takes the largest value with ties to the smaller $g$, which is Bayes' theorem and the MAP rule as in [Bayesian genotype calling](/bayesian-genotype-calling/). $\square$

## What is exact and what is not

- Lemma 1, Theorem 1 and Lemma 3 are exact statements about the code, up to rounding.
- The likelihood of a read given an allele, at line L8, takes the best haplotype of each class. The full marginal under the model would average over the haplotypes of each class with weights, and the max rule is an approximation of it. The genotype likelihoods of two variants on the same haplotypes are also treated one at a time, so the calls of nearby variants are not a joint genotype.
- The pair HMM is a model of the errors. Its gap rates do not depend on the context here, and the reads are taken as independent, which PCR duplicates break.
- The prior is the per-site heterozygosity prior, not a prior on haplotype pairs.

**Cost.** For $R$ reads of length $L$ and $|H|$ candidates of length about $n$, line L4 costs $\Theta(R |H| L n)$, and line L5 costs $\Theta(R |H|^2)$. The graph has $O(N)$ edges for $N$ read bases, and the search of line L3 is exponential in the number of bubbles in the worst case, which the cap on $|H|$ limits.
