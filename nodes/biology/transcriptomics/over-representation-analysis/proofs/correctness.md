---
title: The over-representation p-value is the exact hypergeometric tail, and it equals the one-sided Fisher test
proves: [correctness]
status: full
---

We prove that the code returns the exact probability that a uniformly random selection of $n$ genes from the universe puts at least $k$ genes in the set (Theorem 2). We also prove that this number is the p-value of the one-sided [Fisher exact test](/fisher-exact-test/) on the 2 by 2 table of the set against the selection (Theorem 3), so that it is valid under any null model in which the selection and the set are independent given the margins. The claim that real gene selections behave like uniform draws is a modelling assumption. It fails when genes are correlated or when the chance of selection depends on gene length, and it is not proved here.

**Setting.** The universe $U$ has $N$ genes. Line L1 cuts the list of selected genes to $U$, which gives $D \subseteq U$ with $n = |D|$. Line L3 cuts each set to $U$, which gives $S \subseteq U$ with $K = |S|$ and $k = |S \cap D|$. Line L4 computes
$$p = \sum_{i=k}^{\min(K, n)} \frac{\binom{K}{i}\binom{N-K}{n-i}}{\binom{N}{n}},$$
with the terms outside the range $\max(0, n - (N - K)) \le i$ left out, since they are 0.

**Lemma 1 (the hypergeometric law).** Let $X = |S \cap R|$, where $R$ is a subset of $U$ of size $n$ chosen uniformly at random and $S$ is fixed. Then $P(X = i) = \binom{K}{i}\binom{N-K}{n-i}\big/\binom{N}{n}$.

*Proof.* There are $\binom{N}{n}$ subsets of size $n$, all equally likely. A subset with $|S \cap R| = i$ is fixed by choosing $i$ members of $S$ and $n - i$ genes of $U \setminus S$, which can be done in $\binom{K}{i}\binom{N-K}{n-i}$ ways. $\square$

**Theorem 2 (exact p-value).** The value returned for $S$ is $P(X \ge k)$ for $X$ as in Lemma 1, computed without rounding before the final conversion to a float.

*Proof.* By Lemma 1, $P(X \ge k)$ is the sum at line L4. The code forms the numerator as an integer sum of products of binomial coefficients and divides by the integer $\binom{N}{n}$ as an exact fraction. Only the final call to float rounds. $\square$

The exact arithmetic matters in the far tail. A sum of floating point terms near $10^{-300}$ can underflow, and the complement $1 - P(X < k)$ loses all its digits when $P(X \ge k)$ is small.

**Theorem 3 (equality with the one-sided Fisher test).** Write the 2 by 2 table with rows "in $S$" and "not in $S$" and columns "selected" and "not selected", with margins $K$, $N - K$, $n$ and $N - n$. Suppose the genes of $S$ are selected independently with probability $\pi_1$ each, and the genes outside $S$ with probability $\pi_0$ each. If $\pi_1 = \pi_0$, then given $n$, the count $k$ has the law of Lemma 1. So $p$ is the p-value of the one-sided Fisher exact test of $\pi_1 = \pi_0$ against $\pi_1 > \pi_0$.

*Proof.* Let $Y_1 = k \sim \operatorname{Bin}(K, \pi)$ and $Y_0 = n - k \sim \operatorname{Bin}(N - K, \pi)$, independent, with the common value $\pi \in (0, 1)$. Then $Y_1 + Y_0 \sim \operatorname{Bin}(N, \pi)$, and
$$P(Y_1 = i \mid Y_1 + Y_0 = n) = \frac{\binom{K}{i}\pi^i(1-\pi)^{K-i}\binom{N-K}{n-i}\pi^{n-i}(1-\pi)^{N-K-n+i}}{\binom{N}{n}\pi^n(1-\pi)^{N-n}} = \frac{\binom{K}{i}\binom{N-K}{n-i}}{\binom{N}{n}}.$$
The factor $\pi$ cancels, so the conditional law does not depend on the unknown $\pi$. The one-sided Fisher test conditions on both margins and sums this law over the tables at least as extreme as the observed one in the direction of $\pi_1 > \pi_0$, which are the tables with $Y_1 \ge k$. $\square$

**Validity.** Under the null hypothesis, $X$ is a discrete variable and $p = P(X \ge k)$ is its upper tail at the observed value. For a discrete variable, $P(P(X \ge X_{\text{obs}}) \le u) \le u$ for every $u \in [0, 1]$: let $x^*$ be the smallest value with $P(X \ge x^*) \le u$; then the event is $\{X_{\text{obs}} \ge x^*\}$, which has probability $P(X \ge x^*) \le u$. So the test is valid, and it is conservative because the inequality is usually strict.

**Adjustment.** Line L5 applies the [Benjamini-Hochberg procedure](/benjamini-hochberg-procedure/) to the p-values of the tested sets. The tests of overlapping sets are positively dependent in many cases but not in all, so the control of the [false discovery rate](/false-discovery-rate/) at the nominal level is a heuristic here, not a theorem. The adjusted value is not a [q-value](/storey-q-value/).

**What the universe changes.** Every quantity depends on $U$. A gene outside $U$ is removed from the list and from every set, so it changes $n$ and $K$. Taking all genes of the genome as $U$, when only the expressed genes could have been selected, makes $N$ too large and $p$ too small for every set of expressed genes. This is a fact about the model, and the tests check that the cut to $U$ changes $p$ as the formula says.

**What the tests check.** The test file enumerates every subset $R$ of size $n$ of a small universe and counts the subsets with $|S \cap R| \ge k$ (Theorem 2). It checks Theorem 3 by computing the conditional law of two binomials from their joint law. It compares the probabilities with the hypergeometric mass function of the shared helper, checks the BH adjustment against its definition, and checks the page example, $p = 31/969$ for set A.

**Complexity.** The cut to $U$ takes $O(N + \sum_S |S|)$ expected time with hash sets. For one set, line L4 sums at most $\min(K, n) + 1$ terms with integers of $O(N)$ bits, so the cost is polynomial in $N$; a floating point version on the log scale costs $O(\min(K, n))$ operations. The BH step sorts the $m$ p-values in $O(m\log m)$ time.
