---
title: Three-way radix quicksort sorts strings in lexicographic order
proves: [correctness, termination]
status: full
---

Let $c(s, d) = s[d]$ for $d < |s|$ and $c(s, d) = -1$ otherwise, with $-1$ less than every character. Call a range $A[lo \ldots hi-1]$ *valid at $d$* if its strings have length at least $d$ and agree on their first $d$ characters.

**Fact 1.** Let $s$ and $t$ agree on their first $d$ characters, with $|s|, |t| \ge d$. If $c(s, d) < c(t, d)$ then $s < t$. If $c(s, d) = c(t, d) = -1$ then $s = t$. If $c(s, d) = c(t, d) \ne -1$ then $s$ and $t$ agree on $d + 1$ characters.

*Proof.* If $c(s, d) = -1 < c(t, d)$, then $s$ is a proper prefix of $t$. If $-1 < c(s, d) < c(t, d)$, then $d$ is the first index where they differ. The last two cases follow from the definition. $\square$

**Fact 2 (partition).** At line L4 the following holds: $c(A[k], d) < v$ for $lo \le k < lt$; $c(A[k], d) = v$ for $lt \le k < i$; $c(A[k], d) > v$ for $gt < k < hi$; and the range is a permutation of its values at line L2.

*Proof.* Before the first test, $lt = lo$ and $i = lo + 1$, and $A[lo]$ has the value $v$, so the equal part is $A[lo]$ and the other parts are empty. The equal part $[lt, i)$ is never empty: it starts with one item, line L6 shifts it one place to the right, line L7 does not change it, and line L8 makes it longer. So in line L6, $lt < i$ and $A[lt]$ is an equal item; the swap moves it to $i$ and the less item to $lt$, both pointers advance, and the three properties hold. In line L7, the item at $i$ goes to the greater part and $gt$ decreases; the item that comes to $i$ is not yet tested. Line L8 extends the equal part. Each step is a swap or nothing, so the range stays a permutation. $\square$

The loop ends when $i > gt$, so every index of the range is in one of the three parts: less $[lo, lt)$, equal $[lt, gt]$, greater $(gt, hi)$.

**Claim.** If $A[lo \ldots hi-1]$ is valid at $d$, then THREE-WAY-RADIX-QUICKSORT$(A, lo, hi, d)$ ends, permutes only this range, and leaves it sorted.

*Proof.* By induction on $hi - lo$. Let $L$ be the largest length of a string; a valid range with at least one string has $d \le L$. Consider one turn of the loop at L1 with a valid range of size $m > M$.

By Fact 2, the less and greater parts each miss at least the pivot item, so they have fewer than $m$ items, and they are valid at $d$, since they are parts of a valid range. By induction, the calls of lines L9 and L10 end and sort them. After them, the range is less part, then equal part, then greater part, each part internally as above. By Fact 1, every string of the less part is less than every string of the equal part, which is less than every string of the greater part. So the range is sorted if the equal part is sorted.

If $v = -1$, the strings of the equal part all end at $d$ and are equal by Fact 1, so the equal part is sorted and line L11 returns a sorted range. Otherwise, by Fact 1 the equal part is valid at $d + 1$, and line L12 makes it the new range. Its size is at most $m$ and its depth is $d + 1 \le L$, because its strings have length at least $d + 1$. So each turn of the loop either makes the range smaller or keeps its size and increases $d$, and $d \le L$, so the loop ends after finitely many turns. Each turn leaves its outer parts sorted and in order with the equal part, which becomes the new range, so the whole range is sorted if the final range is sorted.

The loop ends either at line L11, with a sorted range, or with $hi - lo \le M$. Then line L13 runs insertion sort on a range that is valid at $d$. Insertion sort with the order of the suffixes from index $d$ sorts the range, and this order agrees with lexicographic order on strings that share their first $d$ characters. So the final range is sorted, and the whole original range is sorted. $\square$

**Result.** The first call has the range $A[0 \ldots n-1]$ at $d = 0$, which is valid, so the claim gives a sorted permutation of the input. $\blacksquare$
