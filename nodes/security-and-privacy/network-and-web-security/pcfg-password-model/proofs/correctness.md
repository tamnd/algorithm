---
title: The PCFG password model is unambiguous, sums to 1, and its guess numbers are exact
proves: [correctness, complexity]
status: full
---

We use the pseudocode PCFG-SCORE of the page. Each character has one tag: L for a letter, D for a digit and S for any other character. A run of a string is a maximal block of consecutive characters with the same tag. The segmentation of $w$ is the list of its runs $x_1, \ldots, x_r$, and its base structure is $\mathrm{st}(w) = ((t_1, \ell_1), \ldots, (t_r, \ell_r))$, where $t_i$ is the tag of $x_i$ and $\ell_i = |x_i|$. We call a pair $(t, \ell)$ a slot.

Training on a list of $T$ non-empty passwords counts $N(s)$, the number of passwords with base structure $s$, and $N_{t,\ell}(x)$, the number of times $x$ is a run in slot $(t, \ell)$ over the whole list. Let $N_{t,\ell} = \sum_x N_{t,\ell}(x)$. The model is

$$ P(s) = \frac{N(s)}{T}, \qquad P(x \mid t, \ell) = \frac{N_{t,\ell}(x)}{N_{t,\ell}}, $$

and these are the rule probabilities of the grammar with the rules $\mathrm{START} \to (t_1, \ell_1) \cdots (t_r, \ell_r)$ for each $s$ with $N(s) > 0$ and $(t, \ell) \to x$ for each $x$ with $N_{t,\ell}(x) > 0$. We write $S$ for the set of structures and $X_{t,\ell}$ for the set of runs with a positive count in slot $(t, \ell)$.

**Fact 1.** Each $s \in S$ has no two neighbouring slots with the same tag, and each $x \in X_{t,\ell}$ is a string of $\ell$ characters, all with tag $t$.

*Proof.* Both come from the segmentation of a training password. Two neighbouring runs have different tags, since otherwise they would form one longer block, and a run has one tag and its own length. $\square$

**Claim 1 (one derivation).** Each string $w$ has at most one derivation in the grammar. If it has one, it uses the rule of $\mathrm{st}(w)$ and the rules $(t_i, \ell_i) \to x_i$ for the runs of $w$.

*Proof.* Take a derivation with structure $s = ((t_1, \ell_1), \ldots, (t_r, \ell_r))$ and terminals $y_1, \ldots, y_r$, so $w = y_1 \cdots y_r$. By Fact 1, each $y_i$ is a block of characters with tag $t_i$, and $t_i \ne t_{i+1}$. So each block is maximal: it cannot extend into a neighbour with another tag. The maximal blocks of $w$ are its runs, so $y_i = x_i$ for each $i$ and $s = \mathrm{st}(w)$. $\square$

**Claim 2 (the score).** PCFG-SCORE returns $P(w) = P(\mathrm{st}(w)) \prod_{i=1}^{r} P(x_i \mid t_i, \ell_i)$, which is the probability of $w$ under the grammar.

*Proof.* Line L1 computes the runs and line L2 the base structure. Line L3 sets $p$ to $P(\mathrm{st}(w))$, which is 0 when the structure was not seen. The loop of lines L4 and L5 keeps the invariant that after $j$ steps $p = P(\mathrm{st}(w)) \prod_{i \le j} P(x_i \mid t_i, \ell_i)$, where an unseen run gives the factor 0. Line L6 returns the full product. The probability of a string under a grammar is the sum of the probabilities of its derivations. By Claim 1 there is at most one, and its probability is this product; if there is none, some factor is 0. $\square$

**Claim 3 (a distribution).** $\sum_w P(w) = 1$, where the sum is over all strings.

*Proof.* By Claim 1 the map from a structure $s \in S$ and a choice of runs $x_i \in X_{t_i, \ell_i}$ to the string $x_1 \cdots x_r$ is one to one, and its image is the set of strings with $P(w) > 0$. So

$$ \sum_w P(w) = \sum_{s \in S} P(s) \prod_{i=1}^{r} \sum_{x \in X_{t_i, \ell_i}} P(x \mid t_i, \ell_i) = \sum_{s \in S} P(s) = 1, $$

since each inner sum is $N_{t_i,\ell_i} / N_{t_i,\ell_i} = 1$ and the counts $N(s)$ add up to $T$. $\square$

**Claim 4 (maximum likelihood).** Among all choices of rule probabilities for the same grammar, the relative frequencies maximize the probability of the training list.

*Proof.* By Claim 2 the log likelihood of the list is

$$ \sum_{s} N(s) \log P(s) + \sum_{(t, \ell)} \sum_x N_{t,\ell}(x) \log P(x \mid t, \ell). $$

The first sum and each slot of the second depend on separate distributions. For one of them, with counts $c_1, \ldots, c_m$ and total $c$, the term is $c \sum_j (c_j / c) \log q_j$, and by Gibbs' inequality it is largest exactly when $q_j = c_j / c$. $\square$

**Claim 5 (guess numbers).** For $\tau > 0$, COUNT-ABOVE$(\tau)$ of the code returns $|\{v : P(v) > \tau\}|$. So GUESS-NUMBER$(w)$ returns $1 + |\{v : P(v) > P(w)\}|$ when $P(w) > 0$.

*Proof.* By the one to one map in the proof of Claim 3, it is enough to count, for each $s \in S$, the choices of runs with $P(s) \prod_i P(x_i \mid t_i, \ell_i) > \tau$. The code sorts each list $X_{t_i,\ell_i}$ by decreasing probability and sets $B_j = \prod_{i \ge j} \max_x P(x \mid t_i, \ell_i)$. A node of the search is a prefix of choices $x_1, \ldots, x_{j-1}$ with the partial product $p$. Each completion of this prefix with $x_j = x$ has a probability of at most $p \cdot P(x \mid t_j, \ell_j) \cdot B_{j+1}$. When this bound is at most $\tau$ for some $x$, it is also at most $\tau$ for each later $x$ in the sorted list, so the code stops the loop and loses no counted completion. Each other choice is pushed once, so each complete choice with a product above $\tau$ is reached once and counted once, and a complete choice is reached only if its bound, which is then its own product, is above $\tau$. $\square$

The code counts the strings and does not list them.

**Cost.** Line L1 reads $w$ once, $O(n)$ for $n = |w|$. Line L2 builds a tuple of $r \le n$ slots, and line L3 hashes it in $O(r)$. Each lookup of line L5 hashes the run $x_i$ in $O(|x_i|)$, and $\sum_i |x_i| = n$. So PCFG-SCORE takes $\Theta(n)$ time and $O(n)$ extra space for the runs on the word-RAM. Training does the same for each password, so it takes $O(N)$ time for $N$ characters in the list. COUNT-ABOVE takes $O(r)$ work for each node it pushes, and each pushed node is a prefix of a counted string, so its time is $O(r^2 G)$ plus the sorting, where $G$ is the count it returns. $\blacksquare$
