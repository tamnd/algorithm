---
title: Syndrome decoding with least weight coset leaders returns a nearest codeword
proves: [correctness]
status: full
---

Let $C$ be an $[n, k, d]$ linear code over $\mathrm{GF}(q)$ and let $H$ be an $(n - k) \times n$ parity-check matrix of rank $n - k$, so $C = \{\, c : H c^T = 0 \,\}$. Vectors are rows, $\mathrm{wt}$ is the Hamming weight, and $d(x, y) = \mathrm{wt}(x - y)$. Write $\sigma(x) = H x^T$.

**Lemma 1 (syndromes and cosets).** $\sigma$ is linear and onto $\mathrm{GF}(q)^{n-k}$, and $\sigma(x) = \sigma(y)$ if and only if $x - y \in C$. So for each $s$, the set $\sigma^{-1}(s) = \{\, x : \sigma(x) = s \,\}$ is a coset of $C$.

*Proof.* $\sigma$ is a matrix product, so it is linear. Its image is the column space of $H$, which has dimension $\mathrm{rank}(H) = n - k$, so it is all of $\mathrm{GF}(q)^{n-k}$. By linearity $\sigma(x) = \sigma(y)$ if and only if $\sigma(x - y) = 0$, that is, $x - y \in C$. So if $\sigma(a) = s$, then $\sigma^{-1}(s) = a + C$. $\square$

**Lemma 2 (the table).** BUILD-TABLE$(H)$ returns a map $T$ with an entry for every $s \in \mathrm{GF}(q)^{n-k}$, and $\sigma(T[s]) = s$ and $\mathrm{wt}(T[s]) = \min \{\, \mathrm{wt}(x) : \sigma(x) = s \,\}$.

*Proof.* We use this invariant at the start of each pass of the loop of line L2, with the current value $w$:

> **(T)** For every pattern $x$ with $\mathrm{wt}(x) < w$, $T$ has an entry for $\sigma(x)$. Every entry $T[s]$ has $\sigma(T[s]) = s$, and $\mathrm{wt}(T[s]) \le \mathrm{wt}(x)$ for every $x$ with $\sigma(x) = s$.

Before the first pass, $w = 0$ and $T$ is empty (line L1); there is no pattern of negative weight, so (T) holds.

During the pass for $w$, lines L3 to L5 visit every pattern $e$ of weight $w$. For each, line L4 computes $s = \sigma(e)$, and line L5 adds $T[s] = e$ if $s$ has no entry. So after the pass, every pattern of weight at most $w$ has its syndrome in $T$, and every entry satisfies $\sigma(T[s]) = s$. An entry added in this pass has weight $w$. If some $x$ with $\sigma(x) = s$ had $\mathrm{wt}(x) < w$, then by (T) the entry for $s$ existed before the pass, and line L5 would not have added it. Entries made before the pass are not changed, since line L5 never overwrites. So (T) holds with $w + 1$.

If line L6 returns, $T$ has $q^{n-k}$ entries, which by Lemma 1 is every syndrome. Otherwise the loop ends after $w = n$, and by (T) every pattern of weight at most $n$, that is every word, has its syndrome in $T$; by Lemma 1 every syndrome is the syndrome of some word, so again all syndromes have entries. Line L7 or line L6 returns $T$, and by (T) each entry has the least weight among the words with its syndrome. $\square$

**Theorem.** For every received word $r \in \mathrm{GF}(q)^n$, SYNDROME-DECODE$(T, H, r)$ returns a codeword $\hat c$ with $d(r, \hat c) = \min_{c \in C} d(r, c)$.

*Proof.* Line L8 computes $s = \sigma(r)$, and line L9 sets $\hat e = T[s]$, which exists by Lemma 2. Line L10 returns $\hat c = r - \hat e$. Then $\sigma(\hat c) = \sigma(r) - \sigma(\hat e) = s - s = 0$, so $\hat c \in C$, and $d(r, \hat c) = \mathrm{wt}(\hat e)$. For any $c \in C$, $\sigma(r - c) = \sigma(r) - \sigma(c) = s$, so by Lemma 2, $d(r, c) = \mathrm{wt}(r - c) \ge \mathrm{wt}(\hat e) = d(r, \hat c)$. $\square$

**Corollary 1.** If $c \in C$ is sent and $r = c + e$ is received, the output is $c$ if and only if $e = T[\sigma(e)]$, that is, $e$ is the stored leader of its coset.

*Proof.* $\sigma(r) = \sigma(e)$, so $\hat e = T[\sigma(e)]$ and the output is $c + e - \hat e$, which equals $c$ if and only if $e = \hat e$. $\square$

**Corollary 2.** Let $t = \lfloor (d - 1)/2 \rfloor$. Every error $e$ with $\mathrm{wt}(e) \le t$ is corrected.

*Proof.* Let $\hat e = T[\sigma(e)]$. By Lemma 2, $\mathrm{wt}(\hat e) \le \mathrm{wt}(e) \le t$. By Lemma 1, $e - \hat e \in C$, and its weight is at most $2t < d$. The only codeword of weight less than $d$ is $0$, so $\hat e = e$, and Corollary 1 gives the result. $\square$

**Corollary 3 (maximum likelihood on BSC).** On the $q$-ary symmetric channel with symbol error probability $p < (q - 1)/q$, which for $q = 2$ is BSC($p$) with $p < 1/2$, an error $x$ has probability $(p/(q-1))^{\mathrm{wt}(x)} (1 - p)^{n - \mathrm{wt}(x)}$. The ratio of consecutive terms is $p / ((q - 1)(1 - p)) < 1$, so this probability falls strictly as the weight grows. If all codewords are equally likely, $\Pr[r \mid c]$ is largest for the codeword $c$ with the least $d(r, c)$, so by the Theorem the output maximizes the likelihood. $\blacksquare$
