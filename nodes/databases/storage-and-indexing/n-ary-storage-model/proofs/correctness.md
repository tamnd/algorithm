---
title: An NSM page returns every attribute of every stored record, and a scan reads the number of pages and cache lines given on the page
proves: [correctness]
status: full
---

We use the notation of the page. The schema has $k$ attributes. Attribute $j$ has a field at offset $f_j$ of the fixed part, of $w_j = 8$ bytes for an int and 2 bytes for a str, and $F = \sum_j w_j$ is the size of the fixed part. A page of $p$ bytes has a header $(n, e)$ and slots $0, \ldots, n - 1$ of 4 bytes each; a live slot holds $(o_s, \ell_s)$ with $o_s \ne 0$.

**Lemma 1 (the encoding).** Let $r = \text{ENCODE}(t)$. For every attribute $j$, ATTR applied to $r$ at offset 0 returns $t[j]$.

*Proof.* Lines L2 to L4 append the fields in schema order, so field $j$ starts at $f_j$ in $r$, and $|r| = F + \sum_{j \text{ str}} |t[j]|$. For an int, field $j$ is $t[j]$ itself, which line L12 reads. For a str, let $j_1 < j_2 < \ldots$ be the str attributes. When line L4 runs for $j_i$, the text part holds $t[j_1] \ldots t[j_i]$, so the stored end $b_i = F + \sum_{m \le i} |t[j_m]|$, and the bytes $[b_{i-1}, b_i)$ of $r$ (with $b_0 = F$) are $t[j_i]$. Lines L13 and L14 read exactly $a = b_{i-1}$ and $b = b_i$, and line L15 returns those bytes. $\square$

**Lemma 2 (the page).** After any sequence of INSERT and DELETE, (a) $4 + 4n \le e \le p$; (b) the byte ranges $[o_s, o_s + \ell_s)$ of the live slots are disjoint and lie in $[e, p)$; (c) the bytes of a live slot $s$ are the encoding of the record inserted with slot $s$.

*Proof.* An empty page has $n = 0$ and $e = p$. INSERT runs line L8 only after the test of line L7, so $|r| + 4 \le e - 4 - 4n$. The new range $[e - |r|, e)$ lies above the new slot, which ends at $4 + 4(n + 1) \le e - |r|$, and below all older ranges, which lie in $[e, p)$. So (a) and (b) hold for the new values of $n$ and $e$, no older byte changes, and (c) holds. DELETE writes only the 4 bytes of one slot and makes it not live, which keeps (a) to (c). $\square$

**Theorem 1 (round trip).** For every live record id $(P, s)$ and attribute $j$, $\text{ATTR}(P, s, j)$ returns $t[j]$, where $t$ is the record inserted as $(P, s)$. SCAN outputs the attributes $J$ of every live record exactly once, in record id order.

*Proof.* Line L11 gives $o_s$, and by Lemma 2(c) the bytes at $o_s$ are ENCODE$(t)$. All offsets of lines L12 to L15 are relative to $o_s$, so Lemma 1 applies. SCAN visits the pages in order and, in each, the slots $0, \ldots, n - 1$ in order, and line L18 skips exactly the slots that are not live. INSERT never gives a new record a slot that was used before, so each live record has one slot. $\square$

**Theorem 2 (pages).** If every record has the same length $s$ and records are only inserted, the file has $\lceil N / m \rceil$ pages for $N$ records, where $m = \lfloor (p - 4) / (s + 4) \rfloor$.

*Proof.* A page with $c$ records has $e = p - cs$, so by line L7 it takes one more record if and only if $s + 4 \le p - cs - 4 - 4c$, that is, if and only if $(c + 1)(s + 4) \le p - 4$, which is $c + 1 \le m$. So each page takes exactly $m$ records. The file opens a new page only when the last one refuses a record, so all pages but the last hold $m$ records, and the last holds from 1 to $m$. $\square$

**Theorem 3 (cache lines).** Assume all attributes are ints, so $s = 8k$, and that the line size $L$ is a power of 2, at least 8, that divides both $s$ and $p$. A scan of one attribute of a page with $c$ records reads $c + \lceil (4 + 4c) / L \rceil$ distinct cache lines, and a scan of all attributes reads $cs / L + \lceil (4 + 4c) / L \rceil$.

*Proof.* The header and the slots are the bytes $[0, 4 + 4c)$, which meet $\lceil (4 + 4c) / L \rceil$ lines. Record $i$ lies at $p - (i + 1)s$, which is a multiple of $L$, so its $s$ bytes fill exactly $s / L$ whole lines, and the lines of different records differ. An 8-byte field at an offset that is a multiple of 8 lies in one line, because 8 divides $L$; so the one attribute costs one line per record, and all attributes cost $s / L$ lines per record. The record lines start at $e = p - cs$, a multiple of $L$ with $e \ge 4 + 4c$, so they are disjoint from the lines of the slots. $\square$

So the scan of one attribute reads one line per record, while a dense array of the same values would need only $8 / L$ lines per record. That gap is the cost that the [PAX layout](/pax-page-layout/) removes.
