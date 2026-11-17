---
title: A unique prefix and suffix match give the event D = e - p - L, and the split range holds every split that explains the read
proves: [correctness]
status: full
---

**Setting.** The reference is $\mathit{ref}$, the read is $r$ of length $L$, and the window is $[lo, hi)$ with $hi \le |\mathit{ref}|$. For strings, $x[i{:}j]$ is the part from position $i$ up to, but not including, $j$. A string $w$ *occurs at* $x$ in the window when $lo \le x$, $x + |w| \le hi$ and $\mathit{ref}[x{:}x + |w|] = w$.

**Lemma 1 (prefix growth).** `grow_prefix` returns the largest $a \le L$ such that $r[0{:}a]$ occurs in the window, and the list $P$ of all positions where it occurs. If $r[0]$ does not occur, it returns $a = 0$.

*Proof.* Line L1 sets $P$ to the positions $x$ in the window with $\mathit{ref}[x] = r[0]$, which are the occurrences of $r[0{:}1]$. The loop at line L2 keeps the invariant that $P$ is the list of the occurrences of $r[0{:}a]$. A position $x$ is an occurrence of $r[0{:}a+1]$ exactly when it is an occurrence of $r[0{:}a]$, $x + a < hi$ and $\mathit{ref}[x + a] = r[a]$, which is the filter of the loop. So if the filter keeps some positions, the invariant holds for $a + 1$. If it keeps none, $r[0{:}a+1]$ does not occur, and then no longer prefix occurs either, because each occurrence of a longer prefix is an occurrence of $r[0{:}a+1]$. So the returned $a$ is the largest. $\square$

`grow_suffix` is the same with the read and the window read from the right end, and returns the largest $b$ such that $r[L - b{:}L]$ occurs in the window $[p, hi)$, with the list $Q$ of the end positions $e$ of its occurrences. Line L4 searches only at or after $p$, so the second part cannot start to the left of the first.

**Lemma 2 (the event).** Let $r[0{:}a]$ occur at $p$ and $r[L - b{:}L]$ end at $e$, and let $D = e - p - L$ (line L6) and $\iota = \max(-D, 0)$. Let $i$ be an integer with $\max(L - \iota - b, 1) \le i \le \min(a, L - \iota - 1)$, the range of line L7. Then:

- if $D > 0$, $r = \mathit{ref}[p{:}p + i] + \mathit{ref}[p + i + D{:}e]$, so $r$ is the sequence of $\mathit{ref}[p{:}e]$ with the $D$ bases $\mathit{ref}[p + i{:}p + i + D]$ deleted;
- if $D < 0$, $r = \mathit{ref}[p{:}p + i] + r[i{:}i + \iota] + \mathit{ref}[p + i{:}e]$, so $r$ is $\mathit{ref}[p{:}e]$ with the $\iota$ bases $r[i{:}i + \iota]$ inserted before $\mathit{ref}[p + i]$.

*Proof.* Since $i \le a$, the prefix $r[0{:}i]$ is a prefix of $r[0{:}a]$, so $r[0{:}i] = \mathit{ref}[p{:}p + i]$. Since $L - (i + \iota) \le b$, the suffix $r[i + \iota{:}L]$ is a suffix of $r[L - b{:}L]$, so $r[i + \iota{:}L] = \mathit{ref}[e - (L - i - \iota){:}e]$. If $D > 0$, then $\iota = 0$ and $e - (L - i) = p + D + i$, which is the first claim. If $D < 0$, then $\iota = -D$ and $e - (L - i - \iota) = p + D + i + \iota = p + i$, so the suffix is $\mathit{ref}[p + i{:}e]$, and the middle $r[i{:}i + \iota]$ is left over, which is the second claim. The bounds $1 \le i \le L - \iota - 1$ make both parts non-empty. $\square$

**Lemma 3 (the range is complete).** Every split point $i$ for which the first part $r[0{:}i]$ is $\mathit{ref}[p{:}p + i]$ and the second part $r[i + \iota{:}L]$ ends at $e$, with both parts non-empty, is in the range of line L7.

*Proof.* The second part starts at or after $p + i$ and ends at $e \le hi$, so $p + i \le hi$, and $r[0{:}i]$ occurs at $p$ in the window. By the maximality of $a$ in Lemma 1, $i \le a$. If $r[i + \iota{:}L]$ ends at $e$, then it is a suffix of $r$ that occurs in $[p, hi)$, and by the lemma for `grow_suffix`, $L - i - \iota \le b$. Non-empty parts give $i \ge 1$ and $i \le L - \iota - 1$. $\square$

When the range has more than one split point, the bases next to the breakpoint repeat (microhomology), and every point gives the same sequence of the sample, by Lemma 2. The event is then not fixed at one place by the read, and the code reports the leftmost point that leaves both parts at least $m_{\min}$ long, as VCF normalization does for indels.

**Theorem.** If `split_read` returns ("DEL", $q$, $D$, "") then the read equals $\mathit{ref}[p{:}e]$ with $\mathit{ref}[q{:}q + D]$ deleted. If it returns ("INS", $q$, $\iota$, $w$) then the read equals $\mathit{ref}[p{:}e]$ with $w$ inserted before $\mathit{ref}[q]$. In both cases both parts have at least $m_{\min}$ bases, and the prefix $r[0{:}a]$ occurs once in the window and the suffix $r[L - b{:}L]$ occurs once in $[p, hi)$.

*Proof.* Line L3 returns nothing unless the prefix occurs exactly once, at $p$, and line L5 returns nothing unless the suffix occurs exactly once, ending at $e$. Line L6 returns nothing for $D = 0$ (the whole read would then match $\mathit{ref}[p{:}e]$ as one piece, or not at all) and for an insertion longer than the limit. Line L7 takes the smallest $i$ of the range of Lemma 2 that is at least $m_{\min}$ and leaves a second part of at least $m_{\min}$, and returns nothing if there is none. Lines L8 and L9 return $q = p + i$ with the event of Lemma 2. $\square$

**What the theorem does not say.** Uniqueness is uniqueness of the longest exact matches in the window. If the read has a sequencing error in the first $a$ bases, $a$ stops early and the call can be wrong or missing; the method has no mismatch model. A unique match can still be a wrong one, if the true place of the read is outside the window. These are limits of the method, which the page lists.

**Cost.** Each step of the growth filters the current list of occurrences, so the prefix growth costs $O(w + \sum_t |P_t|)$, where $w = hi - lo$ and $P_t$ is the list after step $t$. This is $O(w a)$ in the worst case, and close to $O(w)$ when the list shrinks to one position after a few bases, as it does in a random sequence. The suffix growth is the same, so one read costs $O(w L)$ in the worst case.
