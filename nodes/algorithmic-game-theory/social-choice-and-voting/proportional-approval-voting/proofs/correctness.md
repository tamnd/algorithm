---
title: Exact PAV and local-search PAV satisfy extended justified representation, and local search stops after at most k^2 H(k) swaps
proves: [correctness]
status: full
---

An approval profile has ballots $A_1, \ldots, A_n \subseteq \{0, \ldots, m - 1\}$, and $k$ is the committee size with $0 \le k \le m$. Let $H(j) = 1 + 1/2 + \cdots + 1/j$, with $H(0) = 0$. The PAV score of a committee $W$ is

$$\mathrm{pav}(W) = \sum_{i=1}^{n} H(|A_i \cap W|).$$

Since $H(j + 1) - H(j) = 1/(j + 1)$, a voter with $j$ approved members gains $1/(j + 1)$ when one more approved candidate joins, and loses $1/j$ when one of its $j$ approved members leaves.

## The exact search

`pav` computes $\mathrm{pav}(W)$ for every $W$ of size $k$, in the lexicographic order of sorted tuples, and keeps a new committee only when its score is strictly larger. So it returns the lexicographically first committee with the largest score. Every score is an exact fraction, so no rounding can change a comparison.

## Sequential PAV

By the remark above, the gain of adding $c \notin W$ is

$$\Delta(W, c) = \mathrm{pav}(W \cup \{c\}) - \mathrm{pav}(W) = \sum_{i : c \in A_i} \frac{1}{|A_i \cap W| + 1}.$$

`seq_pav` keeps $x_i = |A_i \cap W|$ for each voter, computes $\Delta(W, c)$ by this formula, and adds a candidate with the largest gain, ties to the smallest index. It does this $k$ times, so it is the greedy algorithm for the PAV score.

## The gain of a swap

Let $w \in W$, $c \notin W$ and $W' = (W \setminus \{w\}) \cup \{c\}$. For a voter $i$ with $x_i = |A_i \cap W|$:

- if $c \in A_i$ and $w \notin A_i$, then $|A_i \cap W'| = x_i + 1$ and the voter gains $1/(x_i + 1)$;
- if $w \in A_i$ and $c \notin A_i$, then $x_i \ge 1$, $|A_i \cap W'| = x_i - 1$, and the voter loses $1/x_i$;
- otherwise $|A_i \cap W'| = x_i$ and nothing changes.

`swap_gain` adds exactly these terms, so it returns $\mathrm{pav}(W') - \mathrm{pav}(W)$. Line L9 updates $x_i$ by the same three cases.

## The swap lemma

A committee $W$ of size $k$ violates extended justified representation (EJR) if there are an integer $\ell$ with $1 \le \ell \le k$ and a nonempty group $S$ of voters such that $|S| \ge \ell n / k$, $|\bigcap_{i \in S} A_i| \ge \ell$, and $|A_i \cap W| < \ell$ for every $i \in S$.

**Lemma.** Let $n \ge 1$ and $1 \le k < m$. If $W$ violates EJR, then some swap of a member $w \in W$ for a candidate $c \notin W$ raises the PAV score by at least $n / k^2$.

*Proof.* Take $\ell$ and $S$ as in the definition, and let $T = \bigcap_{i \in S} A_i$. Pick any $i \in S$. Then $|T \cap W| \le |A_i \cap W| \le \ell - 1 < \ell \le |T|$, so some $c \in T$ is not in $W$.

Write $x_i = |A_i \cap W|$. Every voter of $S$ approves $c$ and has $x_i \le \ell - 1$, so

$$G = \Delta(W, c) \ge \sum_{i \in S} \frac{1}{x_i + 1} \ge \frac{|S|}{\ell} \ge \frac{n}{k}.$$

Let $W^+ = W \cup \{c\}$ and $y_i = |A_i \cap W^+|$. For $w \in W$, let $L(w) = \mathrm{pav}(W^+) - \mathrm{pav}(W^+ \setminus \{w\})$ be the loss when $w$ leaves $W^+$. A voter that approves $w$ loses $1/y_i$, so

$$\sum_{w \in W} L(w) = \sum_{i=1}^{n} \frac{|A_i \cap W|}{y_i},$$

where a term with $y_i = 0$ is $0$. If $c \in A_i$, then $y_i = x_i + 1$ and the term is $1 - 1/(x_i + 1)$. If $c \notin A_i$, the term is at most $1$. Hence

$$\sum_{w \in W} L(w) \le \sum_{i : c \in A_i} \Bigl(1 - \frac{1}{x_i + 1}\Bigr) + \sum_{i : c \notin A_i} 1 = n - G.$$

So some $w \in W$ has $L(w) \le (n - G)/k$. The swap of $w$ for $c$ gives the committee $W^+ \setminus \{w\}$, and

$$\mathrm{pav}(W^+ \setminus \{w\}) - \mathrm{pav}(W) = G - L(w) \ge G - \frac{n - G}{k} = G \Bigl(1 + \frac{1}{k}\Bigr) - \frac{n}{k} \ge \frac{n}{k}\Bigl(1 + \frac{1}{k}\Bigr) - \frac{n}{k} = \frac{n}{k^2}. \qquad \square$$

## Exact PAV satisfies EJR

If $n = 0$ or $k = 0$ there is no group to check. If $k = m$, then $W$ contains every candidate, and a voter of an $\ell$-cohesive group approves at least $\ell$ members. Otherwise, let $W$ have the largest PAV score. No swap raises the score, and $n / k^2 > 0$, so by the lemma $W$ satisfies EJR. This holds for every optimal committee, so it holds for the one that `pav` returns.

## Local-search PAV

**Result.** `ls_pav` stops, and its output satisfies EJR.

*Termination.* The early return after line L1 covers $n = 0$, $k = 0$ and $k = m$, where EJR holds as shown above. Otherwise each pass of the loop L4 to L9 either returns (line L7) or makes a swap with gain at least $\varepsilon = n / k^2$ (lines L6 and L8). The score is at least $0$ and at most $n H(k)$, because each voter has at most $k$ approved members. So there are at most

$$\frac{n H(k)}{n / k^2} = k^2 H(k)$$

swaps, and the loop stops.

*EJR.* Line L7 returns only when lines L5 and L6 found no swap with gain at least $n / k^2$. By the lemma, the committee does not violate EJR.

*Running time.* Each pass tries at most $k (m - k)$ swaps, and each call of `swap_gain` takes $O(n)$ arithmetic operations, with a membership test in $O(1)$ time on a 0/1 table of the ballots. With $k^2 H(k) + 1$ passes and $H(k) = O(\log k)$, the local search uses $O(k^3 m n \log k)$ arithmetic operations, and the start by sequential PAV adds $O(k m n)$.

## Party-list profiles

Suppose the voters split into parties, the voters of party $p$ all approve the same list of $k$ candidates, the lists are disjoint, and party $p$ has $v_p$ voters. A committee with $s_p$ members from list $p$ has score $\sum_p v_p H(s_p)$, and $v_p H(s) = \sum_{t=1}^{s} v_p / t$. The terms $v_p / t$ decrease in $t$, so the largest score with $\sum_p s_p = k$ is the sum of the $k$ largest numbers among all $v_p / t$, which is what the D'Hondt method of highest averages selects. So the seat counts of PAV are a D'Hondt allocation, up to ties.
