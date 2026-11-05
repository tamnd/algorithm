---
title: PPJoin reports exactly the pairs above the Jaccard threshold
proves: [correctness]
status: full
---

We use the names of the pseudocode on the page. Fix $R$, a threshold $0 < t \le 1$, and the global order $\prec$. Every set is a sorted list $x[1] \prec x[2] \prec \cdots \prec x[|x|]$, and the sets are processed in a fixed order in which $|y| \le |x|$ whenever $y$ comes before $x$. Write

$$p(x) = |x| - \lceil t|x| \rceil + 1, \qquad q(x) = |x| - \left\lceil \tfrac{2t}{1+t}|x| \right\rceil + 1, \qquad \alpha(x, y) = \left\lceil \tfrac{t}{1+t}(|x| + |y|) \right\rceil$$

for the probing prefix length, the indexing prefix length and the required overlap.

**Lemma 1 (overlap form).** For nonempty $x$ and $y$, $J(x, y) \ge t$ if and only if $|x \cap y| \ge \alpha(x, y)$.

*Proof.* Let $o = |x \cap y|$, so $|x \cup y| = |x| + |y| - o > 0$. Then $o / (|x| + |y| - o) \ge t$ if and only if $o \ge t(|x| + |y|) - to$, that is $o \ge \frac{t}{1+t}(|x| + |y|)$. Since $o$ is an integer, this holds if and only if $o \ge \alpha(x, y)$. $\square$

**Lemma 2 (the index).** When the probe of $x$ starts in line L3, the list $I[w]$ holds exactly the pairs $(y, j)$ such that $y$ was processed before $x$, $y[j] = w$ and $j \le q(y)$, in the order in which those sets were processed.

*Proof.* Line L2 starts with an empty index. During the probe of $y$, line L11 appends $(y, i)$ to $I[y[i]]$ exactly for the $i \le \min(p(y), q(y))$. Since $\frac{2t}{1+t} \ge t$ for $t \le 1$, $q(y) \le p(y)$, so these are the $i \le q(y)$. Nothing else changes $I$. The appends during the probe of $x$ itself come after all reads of the same list in that iteration of line L5, and $x$ has no repeated element, so $x$ never meets itself. $\square$

**Lemma 3 (the counter).** During the probe of $x$, at the moment line L9 examines the pair $(y, j)$ found under $w = x[i]$, if $y$ is not pruned for $x$, then $A[y]$ equals the number of elements $u \in x \cap y$ with $u \prec w$.

*Proof.* Let $u \in x \cap y$ with $u \prec w$, at position $i'$ of $x$ and $j'$ of $y$. Then $i' < i$, and since $w$ is in $y$ at position $j$ and $u \prec w$, $j' < j \le q(y)$. So $u$ is in the probing prefix of $x$, and by Lemma 2, $(y, j')$ is in $I[u]$. When the loop of line L5 reached $i'$, line L7 met $(y, j')$. The size test gave the same answer as now, since it depends only on $|x|$ and $|y|$, and it passes now. The pair $y$ was not pruned then, since pruning is permanent for the probe of $x$ and $y$ is not pruned now. So line L9 ran on it, and its test passed, or $y$ would be pruned. So $A[y]$ grew by one for $u$. Conversely $A[y]$ grows only in line L9, once per element of $x$ met in a list entry of $y$, and such an element is common to $x$ and $y$ and earlier than $w$. Each common element gives one entry, since $y$ has no repeated element. $\square$

**Lemma 4 (the positional bound).** In the situation of Lemma 3, $|x \cap y| \le A[y] + 1 + \min(|x| - i, |y| - j)$.

*Proof.* Split $x \cap y$ by the element $w$, which is common. The elements before $w$ number $A[y]$ by Lemma 3. The element $w$ counts one. An element after $w$ is among $x[i+1], \ldots, x[|x|]$ and among $y[j+1], \ldots, y[|y|]$, so there are at most $\min(|x| - i, |y| - j)$ of them. $\square$

**Lemma 5 (the prefixes).** Let $x$ and $y$ be nonempty with $|y| \le |x|$ and $J(x, y) \ge t$, and let $u$ be the $\prec$-least element of $x \cap y$, with $x[i] = u = y[j]$. Then $|y| \ge t|x|$, $i \le p(x)$ and $j \le q(y)$.

*Proof.* We have $|y| \ge |x \cap y| \ge t|x \cup y| \ge t|x|$. Let $\alpha = \alpha(x, y)$; by Lemma 1, $|x \cap y| \ge \alpha$. All common elements are at or after $u$ in $x$, so $|x| - i + 1 \ge \alpha$, that is $i \le |x| - \alpha + 1$; in the same way $j \le |y| - \alpha + 1$. Now $|y| \ge t|x|$ gives $\frac{t}{1+t}(|x| + |y|) \ge \frac{t}{1+t}(1+t)|x| = t|x|$, so $\alpha \ge \lceil t|x| \rceil$ and $i \le p(x)$. And $|x| \ge |y|$ gives $\frac{t}{1+t}(|x| + |y|) \ge \frac{2t}{1+t}|y|$, so $\alpha \ge \lceil \frac{2t}{1+t}|y| \rceil$ and $j \le q(y)$. $\square$

**Theorem.** PPJOIN outputs a pair $(x, y)$ if and only if $x$ and $y$ are distinct nonempty sets of $R$ with $J(x, y) \ge t$, and it outputs each such pair once.

*Proof.* (Soundness.) Line L13 outputs $(x, y)$ only if $|x \cap y| \ge \alpha(x, y)$, that is, by Lemma 1, only if $J(x, y) \ge t$. An empty set has no prefix, so it never enters $I$ and never probes.

(Uniqueness.) A pair is considered only during the probe of the later of its two sets, by Lemma 2, and line L12 visits each $y$ once in that probe.

(Completeness.) Let $J(x, y) \ge t$, with $y$ processed before $x$, so $|y| \le |x|$. Take $u$, $i$ and $j$ as in Lemma 5. By Lemma 5 and Lemma 2, $i \le p(x)$, so the loop of line L5 reaches $w = u$, and $(y, j)$ is in $I[u]$, and the size filter of line L7 passes. We claim that $y$ is never pruned during the probe of $x$. Suppose line L10 prunes $y$ for the first time, at an element $w = x[i']$ with $y[j'] = w$. Before that $y$ was not pruned, so Lemma 4 applies and gives $A[y] + 1 + \min(|x| - i', |y| - j') \ge |x \cap y| \ge \alpha(x, y)$, by Lemma 1. So the test of line L9 passes, a contradiction. At $w = u$ the test passes as well, so $A[y] \ge 1$ after it, and line L12 visits $y$. Line L13 checks $|x \cap y| \ge \alpha(x, y)$, which holds, and outputs the pair. $\blacksquare$
