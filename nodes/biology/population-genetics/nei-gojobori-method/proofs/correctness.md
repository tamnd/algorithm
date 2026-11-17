---
title: NEI-GOJOBORI computes the counts of the definition, and the counts measure the two kinds of change on the same scale
proves: [correctness]
status: full
---

**Setting.** $X$ and $Y$ are aligned coding sequences of $c$ codons with no stop codon, and the genetic code maps the 64 codons to 20 amino acids and stop. For a sense codon $x$, $f_i(x)$, $s(x)$ and $n(x) = 3 - s(x)$ are as on the page. For sense codons $x$ and $y$ that differ at the positions in a set $P$ with $|P| = k$, a pathway is an order $(i_1, \ldots, i_k)$ of $P$, and its codons are $x = z_0, z_1, \ldots, z_k = y$, where $z_j$ is $z_{j-1}$ with the base at $i_j$ changed to that of $y$. Step $j$ is synonymous when $z_{j-1}$ and $z_j$ code the same amino acid. The kept pathways are those whose codons are all sense codons, or all pathways if none is.

**Lemma 1.** After the loop of lines L2 to L5, $S = \sum_{t=1}^{c} (s(x_t) + s(y_t))/2$, $S_d = \sum_t s_d(x_t, y_t)$ and $N_d = \sum_t n_d(x_t, y_t)$, where $(x_t, y_t)$ is the $t$-th codon pair.

*Proof.* Line L1 sets the three sums to 0, and each pass of the loop adds the term of one codon pair to each of them, by lines L3 to L5. $\square$

So lines L6 and L7 compute $N$, $p_S$, $p_N$, $d_S$ and $d_N$ by their definitions, and line L8 returns them.

**Lemma 2.** For every codon pair, $s_d + n_d = k$, the number of positions where the codons differ. Hence $S_d + N_d$ is the number of bases at which $X$ and $Y$ differ, and $S + N = 3c$.

*Proof.* Each step of a pathway changes the base at one position of $P$ to its final value, and no position appears twice, so every pathway has exactly $k$ steps, each synonymous or not. The mean over the kept pathways of (synonymous steps + nonsynonymous steps) is therefore $k$. Summing over codon pairs gives the number of differing bases. Since $s(x) + n(x) = 3$ for every codon, $N = 3c - S$ is the sum of $(n(x_t) + n(y_t))/2$. $\square$

**Lemma 3.** The result does not change when $X$ and $Y$ are swapped.

*Proof.* The term of line L3 is symmetric. Reversing the codons of a pathway from $x$ to $y$ gives a pathway from $y$ to $x$ with the same steps in reverse order, the same synonymous steps, and the same codons, so it is kept exactly when the first one is. This is a bijection between the pathways of the two directions, so $s_d$ and $n_d$ are the same. $\square$

**Lemma 4.** Suppose each base mutates to each of the three other bases at rate $u$, independently of the others. Then at a sense codon $x$, the rate of synonymous single-base changes is $3u\, s(x)$, and the rate of changes to a codon of another amino acid or to a stop codon is $3u\, n(x)$.

*Proof.* There are nine single-base changes of $x$, each at rate $u$. By the definition of $f_i$, the number of synonymous ones at position $i$ is $3 f_i(x)$, so in total there are $3 s(x)$ synonymous changes and $9 - 3 s(x) = 3 n(x)$ others. $\square$

So in a short time $\tau$, the expected number of synonymous changes in the sequence is $3u\tau$ times its synonymous site count, and the expected number of other changes is $3u\tau$ times its nonsynonymous site count. Dividing by the site counts puts both kinds of change on the same scale, the expected number of changes per site. This is what $p_S$ and $p_N$ estimate when divergence is small.

**Lemma 5.** Under the Jukes-Cantor model with $d$ expected substitutions per site between two sequences, the probability that a site differs is $p = \frac{3}{4}(1 - e^{-4d/3})$. For $0 \le p < 3/4$, the inverse is $d = -\frac{3}{4}\ln(1 - \frac{4}{3}p)$.

*Proof.* Along the path between the two sequences, a site is replaced at rate $4/3$ per unit of $d$ by a base drawn uniformly from all four, since a substitution at rate 1 to one of the three other bases is the same as a uniform draw at rate $4/3$ that keeps the base with probability $1/4$. The site differs exactly when at least one draw happened, probability $1 - e^{-4d/3}$, and the last draw gives another base, probability $3/4$. Solving for $d$ gives the inverse, which is defined and increasing on $[0, 3/4)$. $\square$

**Theorem.** NEI-GOJOBORI returns the Nei-Gojobori values $S$, $N$, $S_d$, $N_d$, $p_S$, $p_N$, $d_S$ and $d_N$ of $X$ and $Y$, and these do not depend on the order of the two sequences. $d_S$ and $d_N$ are the Jukes-Cantor distances of the two classes of sites, each treated as a separate sequence.

*Proof.* Lemma 1 gives the counts, and lines L6 and L7 apply the definitions and, by Lemma 5, the Jukes-Cantor inverse. Lemma 3 gives the symmetry. $\square$

The method of moments in Lemma 5 is exact only for the model it assumes. For a class of sites in a real gene, rates differ between transitions and transversions and between sites, and the class is not a fixed set of sites, since $f_i$ changes when a codon changes; so $d_S$ and $d_N$ are approximations.
