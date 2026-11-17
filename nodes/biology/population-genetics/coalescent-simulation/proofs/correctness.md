---
title: HUDSON samples exactly from the Kingman coalescent with infinite-sites mutations
proves: [correctness]
status: full
---

**The model.** The Kingman $n$-coalescent is the continuous-time Markov chain $(\Pi_t)_{t \ge 0}$ on partitions of $\{1, \ldots, n\}$ that starts from the partition into singletons and in which, from a partition with $k \ge 2$ blocks, each of the $\binom{k}{2}$ pairs of blocks merges at rate 1; the partition with one block is absorbing. Its genealogy is the tree whose leaves are the copies, whose internal nodes are the blocks formed by the merges, and whose node ages are the merge times. Given the genealogy, the mutations are a Poisson process of rate $\theta/2$ on the union of the branches (measured in time), and the sites have independent uniform positions in $[0, 1)$. Under the infinite sites model each mutation creates its own site, at which the copies below the mutated branch carry allele 1 and the others allele 0.

We use two standard facts.

*Fact A (jump chain).* For a continuous-time Markov chain with finitely many states and rates $q(x, y)$, let $\lambda(x) = \sum_{y \ne x} q(x, y)$. From state $x$ with $\lambda(x) > 0$, the time to the next jump is exponential with rate $\lambda(x)$, the next state is $y$ with probability $q(x, y)/\lambda(x)$, the two are independent, and given the next state the future is a new copy of the chain started there.

*Fact B (Poisson restriction).* If points form a Poisson process of rate $c$ on a set that is the disjoint union of intervals of lengths $l_1, \ldots, l_r$, then the counts on the intervals are independent Poisson variables with means $c l_1, \ldots, c l_r$, and given the counts the points are independent and uniform on their intervals.

**Lemma 1.** After the loop of lines L2 to L5, the tree and its node ages have the law of the genealogy of the Kingman $n$-coalescent.

*Proof.* The set $A$ in the algorithm is a partition of the copies: each element of $A$ is a node, and it stands for the set of copies below it. At the start (line L1) it is the partition into singletons at time 0. Suppose that before a pass, $A$ has $k \ge 2$ blocks and $t$ is the time of the last merge. In the chain, the total rate out of a partition with $k$ blocks is $\lambda = \binom{k}{2}$, and each of the $\binom{k}{2}$ merges has probability $1/\binom{k}{2}$. By Fact A, the next merge happens after an exponential time with rate $\binom{k}{2}$, independent of which pair merges, and the pair is uniform. Line L3 draws that time and line L4 that pair, independently. Line L5 records the merge at the right time and makes the merged block a node with the two blocks as its children. By Fact A again, the rest of the chain is a new copy started from the new partition, which is what the next pass of the loop simulates with fresh random numbers. By induction on the number of passes, the sequence of partitions and merge times after $n - 1$ passes has the law of the chain up to absorption, and so the tree has the law of the genealogy. $\square$

**Lemma 2.** Given the tree, lines L6 to L9 output sites with the law of the infinite sites model on it.

*Proof.* The branches of the tree are disjoint intervals of time, one above each non-root node $v$, of length $l_v$ equal to the age of the parent minus the age of $v$. By Fact B, the numbers of mutations on them are independent Poisson variables with means $\theta l_v / 2$, which line L7 draws independently for each branch. The model gives each mutation its own site with a uniform position, independent of everything else, and allele 1 exactly in the copies below the branch, which line L8 does. Sorting in line L9 only puts the sites in the order of their positions. $\square$

**Theorem.** HUDSON returns a tree and a sample matrix with the joint law of the Kingman coalescent with infinite-sites mutations of rate $\theta$.

*Proof.* The random numbers of lines L6 to L8 are drawn after the tree and independently of the draws of lines L3 and L4. By Lemma 1 the tree has the law of the model, and by Lemma 2 the conditional law of the sites given the tree is the law of the model. A joint law is the law of the first part times the conditional law of the second given the first. $\blacksquare$

**The option with a fixed number of sites.** Given the tree and given that the Poisson process has exactly $s$ points, by Fact B (applied to the union of all branches) the points are independent and uniform on the union of the branches. So each point is on branch $v$ with probability $l_v / L$, with $L = \sum_v l_v$, independently. The implementation draws the branches that way, so for a fixed tree it gives the law of the sites given $S = s$. It does not give the law of the sample given $S = s$ under the model, because that would also weight the tree by the probability $P(S = s \mid L)$; like ms, the implementation draws the tree without this weight.

**Remarks.** The tests check the consequences $E[T_{\text{MRCA}}] = 2(1 - 1/n)$ and $\operatorname{Var}[T_{\text{MRCA}}] = \sum_{k=2}^{n} 1/\binom{k}{2}^2$, $E[L] = 2 a_n$ and $\operatorname{Var}[L] = 4 b_n$, $E[S] = \theta a_n$ and $\operatorname{Var}[S] = \theta a_n + \theta^2 b_n$, $E[\xi_i] = \theta / i$, the law $2i/(n(n-1))$ of the size of the side of the root that holds copy 1, and the geometric law of $S$ for $n = 2$, the last two by a chi-squared test.
