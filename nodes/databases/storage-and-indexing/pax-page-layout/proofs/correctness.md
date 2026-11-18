---
title: A PAX page returns every attribute of every live record, keeps its minipages apart, and a scan of one attribute reads one contiguous range per page
proves: [correctness]
status: full
---

We use the notation of the page. The schema has $k$ attributes. A page of $p$ bytes has capacity $c$, a header of $H = 4 + 2k + \lceil c/8 \rceil$ bytes, and minipages $j = 0, \ldots, k - 1$ that occupy $[start_j, end_j)$, where $end_j = start_{j+1}$ and $end_{k-1} = p$. An F-minipage holds $c$ values of 8 bytes. A V-minipage holds $c$ ends of 2 bytes at $[start_j, start_j + 2c)$ and the texts from $base_j = start_j + 2c$ to $end_j$. Let $n$ be the number of records and $b_j(s)$ the end stored for record $s$ in V-minipage $j$, with $b_j(-1) = 0$.

**Lemma 1 (layout).** $H \le start_0$, the minipages are disjoint and lie in $[H, p)$, and each F-minipage $j$ has room for $c$ values: $start_j + 8c \le end_j$.

*Proof.* Lines L1 and L2 place the minipages one after another, each at the next multiple of 8 after the end of the previous one (after the header for $j = 0$), and give minipage $j$ the size $8c$ for an int and $c(2 + avg_j)$ for a text. Line L1 picks $c$ so that the last one ends at most at $p$. So the starts increase, the size of minipage $j$ is at most $end_j - start_j$, and no minipage meets the header. $\square$

**Invariant.** (a) $0 \le n \le c$. (b) For every record $s < n$ and int attribute $j$, the 8 bytes at $start_j + 8s$ are $t_s[j]$, the value of attribute $j$ of the record inserted as $s$. (c) For every text attribute $j$, $0 = b_j(-1) \le b_j(0) \le \ldots \le b_j(n - 1) \le end_j - base_j$, and the bytes $[base_j + b_j(s - 1), base_j + b_j(s))$ are $t_s[j]$. (d) Presence bit $s$ is 1 if and only if record $s$ is live.

**Lemma 2.** INSERT keeps the invariant, and it fails only if $n = c$ or some text does not fit in the free part of its V-minipage.

*Proof.* Line L3 refuses when $n = c$, and line L4 refuses when, for some text attribute $j$, $|t[j]| > (end_j - base_j) - b_j(n - 1)$. Otherwise, for an int attribute, line L6 writes at $start_j + 8n$, which is inside the minipage since $n < c$ (Lemma 1), and touches no byte of another record. For a text attribute, line L7 writes the text at $base_j + b_j(n - 1)$, just after the text of record $n - 1$, and stores the end $b_j(n) = b_j(n - 1) + |t[j]|$, which is at most $end_j - base_j$ by line L4. The end is at $start_j + 2n < base_j$, so it does not overlap the texts. Line L8 sets bit $n$ and increases $n$. Parts (a) to (d) hold for the new record and did not change for the old ones. DELETE only clears one presence bit. $\square$

**Theorem 1 (round trip).** For every live record $s$ of a page and every attribute $j$, $\text{ATTR}(s, j) = t_s[j]$. SCAN outputs the attributes $J$ of every live record of the page once, in slot order.

*Proof.* For an int, line L9 reads the 8 bytes at $start_j + 8s$, which are $t_s[j]$ by part (b). For a text, line L10 reads $a = b_j(s - 1)$ (or 0 for $s = 0$) and $b = b_j(s)$, and line L11 returns $[base_j + a, base_j + b)$, which is $t_s[j]$ by part (c). SCAN visits $s = 0, \ldots, n - 1$ and, by part (d), outputs exactly the live ones. $\square$

**Theorem 2 (cache lines).** A scan of one int attribute $j$ of a page with $n$ records reads only the header and the bytes $[start_j, start_j + 8n)$. With lines of $L$ bytes, it touches at most $\lceil H/L \rceil + \lceil 8n/L \rceil + 1$ lines, and exactly $\lceil H/L \rceil + 8n/L$ when $L$ divides $H$, $start_j$ and $8n$.

*Proof.* SCAN reads the header once, for $n$ and the presence bits. For each live record it reads, by line L9, the 8 bytes at $start_j + 8s$, and these ranges for $s = 0, \ldots, n - 1$ fill $[start_j, start_j + 8n)$ (a deleted record only leaves a gap). A range of $x$ bytes meets at most $\lceil x/L \rceil + 1$ lines, and exactly $x/L$ when it starts at a multiple of $L$ and $L$ divides $x$. $\square$

For $k$ int attributes the capacity follows from Lemma 1: $c$ is the largest number such that the header, rounded up to a multiple of 8, plus $8kc$ is at most $p$. A table of $N$ such records has $\lceil N/c \rceil$ pages, since each page takes records until $n = c$, by Lemma 2. Theorem 2 is the point of the layout: in NSM the same scan touches one line per record, here it touches about $8/L$ of a line per record.
