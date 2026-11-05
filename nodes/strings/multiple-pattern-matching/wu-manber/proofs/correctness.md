---
title: Wu-Manber outputs exactly the occurrences of the patterns
proves: [correctness, termination]
status: full
---

**Claim.** For every text $T[0 \ldots n-1]$, patterns $P_0, \ldots, P_{k-1}$ and block size $B \ge 1$, WU-MANBER stops and outputs each pair $(s, j)$ with $0 \le s \le n - |P_j|$ and $T[s \ldots s + |P_j| - 1] = P_j$ exactly once, and no other pair.

**Notation.** After line L3, $\ell \ge 1$ is the shortest nonempty length and $1 \le B \le \ell$. For a nonempty $P_j$, the cut pattern is $\hat P_j = P_j[0 \ldots \ell - 1]$. A window is identified by $\mathrm{pos}$; its start is $s(\mathrm{pos}) = \mathrm{pos} - \ell + 1$ and its block is $X(\mathrm{pos}) = T[\mathrm{pos} - B + 1 \ldots \mathrm{pos}]$, which is inside the text when $\ell - 1 \le \mathrm{pos} \le n - 1$ since $B \le \ell$.

**Lemma 1 (the tables).** After line L6, for every block $X$:

1. $\mathrm{SHIFT}[X] = \min\big(\{\ell - B + 1\} \cup \{\ell - q : B \le q \le \ell,\ \exists j: \hat P_j[q - B \ldots q - 1] = X\}\big)$, so $0 \le \mathrm{SHIFT}[X] \le \ell - B + 1$;
2. $\mathrm{HASH}[X] = \{ j : P_j \ne \varepsilon,\ \hat P_j[\ell - B \ldots \ell - 1] = X \}$;
3. $\mathrm{PREFIX}[j] = P_j[0 \ldots B - 1]$ for every nonempty $P_j$.

*Proof.* Line L4 sets every entry of SHIFT to $\ell - B + 1$, and line L5 lowers the entry of each block of each cut pattern, ending at $q$, to $\ell - q$ when smaller; the blocks visited are exactly those of the set in item 1. Line L6 appends each nonempty index once to the list of its last cut block, and stores the prefix. $\square$

**Lemma 2 (a zero-shift window).** Let $\mathrm{SHIFT}[X(\mathrm{pos})] = 0$ and $s = s(\mathrm{pos})$. Lines L13 and L14 output exactly the pairs $(s, j)$ with $P_j$ nonempty and occurring at $s$, each once.

*Proof.* If a nonempty $P_j$ occurs at $s$, then $s + |P_j| \le n$, $T[s \ldots s + \ell - 1] = \hat P_j$, and so $X(\mathrm{pos}) = T[\mathrm{pos} - B + 1 \ldots \mathrm{pos}] = \hat P_j[\ell - B \ldots \ell - 1]$. By Lemma 1, $j \in \mathrm{HASH}[X(\mathrm{pos})]$. The three tests of line L14 succeed: the first $B$ characters agree because $B \le \ell \le |P_j|$, the length fits, and the whole pattern agrees. So $(s, j)$ is output. Conversely, line L14 outputs $(s, j)$ only after it has checked $s + |P_j| \le n$ and $T[s \ldots s + |P_j| - 1] = P_j$, so the pair is an occurrence. Each $j$ appears once in $\mathrm{HASH}[X(\mathrm{pos})]$, so the pair is output once by this window. $\square$

**Lemma 3 (safe shift).** Let $d = \mathrm{SHIFT}[X(\mathrm{pos})] > 0$ and $s = s(\mathrm{pos})$. No nonempty pattern occurs at any start $s + \delta$ with $0 \le \delta < d$.

*Proof.* Suppose $P_j$ occurs at $s + \delta$ with $0 \le \delta < d$. Then $T[s + \delta \ldots s + \delta + \ell - 1] = \hat P_j$, and this range ends at $\mathrm{pos} + \delta$.

- If $\delta \le \ell - B$, let $q = \ell - \delta$, so $B \le q \le \ell$. The block $X(\mathrm{pos})$ occupies $\mathrm{pos} - B + 1 \ldots \mathrm{pos}$, which is the range of indices $q - B \ldots q - 1$ of $\hat P_j$ in this occurrence, since $s + \delta + q - 1 = \mathrm{pos}$ and $q - B \ge 0$. So $\hat P_j[q - B \ldots q - 1] = X(\mathrm{pos})$, and Lemma 1 gives $d \le \ell - q = \delta$, a contradiction.
- If $\delta \ge \ell - B + 1$, then $d > \delta \ge \ell - B + 1$, which contradicts $d \le \ell - B + 1$ from Lemma 1. $\square$

**Theorem.** The claim holds.

*Proof.* *Empty patterns.* Line L1 outputs $(s, j)$ for all $s \in \{0, \ldots, n\}$ and every empty $P_j$, exactly their occurrences, once each. Later lines output only nonempty patterns, since only they are in HASH. If all patterns are empty, line L2 stops.

*Termination.* Each pass of the loop of line L8 increases $\mathrm{pos}$ by $\mathrm{SHIFT}[X] \ge 1$ at line L10 or by 1 at line L15, and the inner loop of line L13 is over a finite list. So the loop ends.

*Nonempty patterns.* Let $\mathrm{pos}_1 < \mathrm{pos}_2 < \cdots < \mathrm{pos}_r$ be the windows visited, with $\mathrm{pos}_1 = \ell - 1$, so the starts $s_t = s(\mathrm{pos}_t)$ begin at $s_1 = 0$. Each window outputs only pairs with the start $s_t$, so different windows output different pairs, and by Lemma 2 no pair is output twice. Let $P_j$ be nonempty and occur at $s$; then $0 \le s \le n - |P_j| \le n - \ell$. Let $t$ be the largest index with $s_t \le s$; it exists since $s_1 = 0$. The step taken after window $t$ carries the start from $s_t$ to a value above $s$: if window $t + 1$ exists, its start is above $s$ by the choice of $t$; if $t = r$, the loop ended because the next value of $\mathrm{pos}$ exceeds $n - 1$, so the next start exceeds $n - \ell \ge s$.

- If window $t$ had a zero shift, the next start is $s_t + 1 > s$, so $s = s_t$ and Lemma 2 outputs $(s, j)$.
- If window $t$ had a shift $d > 0$, the next start, or the end of the loop, lies beyond $s$, so $s_t \le s < s_t + d$, and Lemma 3 says that no nonempty pattern occurs at $s$, a contradiction.

So every occurrence of a nonempty pattern is output exactly once, and only occurrences are output. $\blacksquare$
