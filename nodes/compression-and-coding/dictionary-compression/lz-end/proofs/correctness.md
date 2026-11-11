---
title: LZ-End gives the LZ-End parse, extraction is correct, and LZ77 never needs more phrases
proves: [correctness]
status: full
---

We use the notation of the page. The text is $t[0 \ldots n-1]$, $t^R$ is its reverse with a sentinel at the end, and $E_q$ is the end of phrase $Z_q$. For a position $E$ with $-1 \le E \le n-1$, let $P_E = t[E] t[E-1] \cdots t[0]$ followed by the sentinel; this is the suffix of $t^R$ that starts at $n-1-E$. A string $x$ is a suffix of $t[0 \ldots E]$ exactly when the reverse of $x$ is a prefix of $P_E$.

## 1. The parser computes the LZ-End parse

Fix a phrase start $i$, and let $\mathcal{E}$ be the set of the ends of the phrases already made. Each element of $\mathcal{E}$ is less than $i$. Call a length $\ell \le n-1-i$ *good* when $t[i \ldots i+\ell-1]$ is a suffix of $t[0 \ldots E]$ for some $E \in \mathcal{E}$. The length 0 is good.

**Invariant (I).** After line L5 with the value $j$, the interval $[sp, ep)$ holds exactly the ranks of the suffixes $P_E$ that start with $t[j] t[j-1] \cdots t[i]$.

*Proof.* Before the first step the interval is all ranks, which is right for the empty string. Backward search on an FM-index maps the interval of the suffixes that start with a string $y$ to the interval of the suffixes that start with $c\,y$ (the LF property of the [Burrows-Wheeler transform](/burrows-wheeler-transform/)). Line L5 uses $c = t[j]$, so (I) holds after each step. $\square$

So, by (I), the length $j - i + 1$ is good exactly when the interval holds the rank of some $P_E$ with $E \in \mathcal{E}$, that is, a marked rank. Line L7 finds the first marked rank $r \ge sp$, and the test $r < ep$ of line L8 is true exactly when a marked rank lies in the interval. So line L8 sets $\ell$ to $j - i + 1$ exactly for the good lengths that the loop reaches, and $q$ to a phrase whose end gives the copy.

**The stop rule.** Line L6 stops when no $E < i$ in the interval exists, that is, when no prefix $t[0 \ldots E]$ with $E < i$ ends with $t[i \ldots j]$. Then no length $\ell' > j - i + 1$ is good: if $t[i \ldots i+\ell'-1]$ is a suffix of $t[0 \ldots E]$ with $E \in \mathcal{E}$, then $t[i \ldots j]$ is a suffix of $t[0 \ldots E - (i + \ell' - 1 - j)]$, and this end is less than $E < i$. The loop of line L4 also stops at $j = n-1$, which is the bound $\ell \le n-1-i$.

So, when the loop ends, $\ell$ is the largest good length, and line L9 outputs the phrase $(q, \ell, t[i+\ell])$ of the definition. Line L10 adds $E = i + \ell$ to $\mathcal{E}$ by marking the rank of $P_E$, and moves $i$ to the next phrase. By induction on the number of phrases, the output is the LZ-End parse. Each phrase has length at least 1, so the outer loop ends. $\square$

## 2. Decoding and extraction are correct

**Decoding.** Phrase $Z_p$ with $(q, \ell, c)$ is $t[E_q - \ell + 1 \ldots E_q]$ followed by $c$, by the definition, and $E_q < E_p - \ell$, so the decoder has already written the symbols that it copies. $\square$

**Extraction.** A task is a triple $(e, m, o)$: write $t[e - m + 1 \ldots e]$ to the output positions $o - m + 1 \ldots o$. We claim that each task on the stack has $e$ equal to a phrase end. This holds for the first task, whose end is the end of the phrase that holds the last symbol asked for.

Take a task $(e, m, o)$ with $e = E_p$ and $m \ge 1$, and let $Z_p = (q, \ell, c)$. Then $t[e] = c$, so the step writes the right symbol. The $k = \min(m - 1, \ell)$ symbols to the left of $e$ are the last $k$ symbols of the copy, so they equal $t[E_q - k + 1 \ldots E_q]$, and the new task $(E_q, k, o - 1)$ again ends at a phrase end. If $m - 1 > \ell$, the rest ends at $e - 1 - \ell = E_p - |Z_p| = E_{p-1}$, which is a phrase end, and the loop goes on with it. So each task ends at a phrase end, each symbol written is right, and the output positions of the tasks are disjoint and cover the whole range.

Each step writes exactly one output symbol, and it never writes a position twice. So the number of steps is the length of the range, $e - a + 1$ for $t[a \ldots e]$. For a range $t[a \ldots b]$ that does not end at a phrase end, extraction works on $t[a \ldots E_p]$ where $Z_p$ holds $t[b]$, so it takes at most $b - a + 1 + |Z_p|$ steps. $\square$

## 3. Greedy LZ77 has at most as many phrases

Consider parses of $t$ into phrases of the form "a copy, then one symbol", where the copy of a phrase that starts at $s$ has the form $t[s \ldots s+m-1]$, with $m \le n-1-s$ and an occurrence that starts at a position less than $s$ (it may overlap the phrase). Call these *LZ77-type parses*. Greedy LZ77 takes the longest such copy at each phrase start.

The LZ-End parse is of this type: the copy of $Z_p$ is a suffix of $t[0 \ldots E_q]$ with $E_q < s$, so it occurs at a start less than $s$.

**Claim.** Let $g_1 < g_2 < \cdots$ be the ends of the greedy phrases and $e_1 < e_2 < \cdots$ the ends of the phrases of any LZ77-type parse. Then $g_k \ge e_k$ for each $k$ for which both exist.

*Proof by induction on $k$*, with $g_0 = e_0 = -1$. Assume $g_{k-1} \ge e_{k-1}$. If $g_{k-1} \ge e_k$, then $g_k > g_{k-1} \ge e_k$. Otherwise $e_{k-1} \le g_{k-1} < e_k$. Phrase $k$ of the other parse starts at $s = e_{k-1} + 1$, and its copy $t[s \ldots e_k - 1]$ occurs at some $u < s$. Let $d = g_{k-1} + 1 - s \ge 0$. Then $t[g_{k-1} + 1 \ldots e_k - 1]$ occurs at $u + d < g_{k-1} + 1$, and its length is at most $n - 1 - (g_{k-1}+1)$. So the greedy copy at $g_{k-1} + 1$ has at least this length, and $g_k \ge e_k$. $\square$

So the greedy parse reaches the end of the text after at most as many phrases as any LZ77-type parse. With the LZ-End parse as the other parse, $z_{77} \le z_{\text{end}}$. $\square$
