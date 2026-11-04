---
title: The HAT-trie stores each key once and finds it, and bursts and splits keep its invariant
proves: [correctness]
status: full
---

We use the pseudocode, the notation and the invariant (H1) to (H4) of the page. For a node $x$, write $u(x)$ for its string, the symbols of the pointers from the root to $x$. An entry *stands for* the key given by (H2).

**Lemma 1 (descent).** For a string $s$, DESCEND stops at the node $x$ with $u(x) = s[0 \ldots d - 1]$, where either $d = \lvert s \rvert$ or the pointer $x.child[s[d]]$ leads to a container $y$. A key $s$ can only be stored at $x.value$ in the first case, and only in $y$ in the second, under the string $s[d + 1 \ldots]$ if $y$ is pure and $s[d \ldots]$ if $y$ is hybrid.

*Proof.* The loop follows one pointer per symbol while it leads to a trie node, so $u(x) = s[0 \ldots d - 1]$. A key $k$ is stored at a node value when $k = u(x)$, or in a container under a node $x'$ whose string $u(x')$ is a prefix of $k$, with the pointer by $k[\lvert u(x') \rvert]$ leading to that container, by (H2). Suppose $s$ is stored. If $s = u(x')$ for a node $x'$, the descent reaches $x'$ and stops with $d = \lvert s \rvert$, since it consumes the symbols of $u(x')$ along existing nodes; so $x' = x$. Otherwise the container holding $s$ hangs under a node $x'$ by the pointer $s[\lvert u(x') \rvert]$; the descent passes through $x'$ and stops there, because that pointer leads to a container; so $x' = x$ and the container is $y$, and the stored string is the one given by (H2). $\square$

**GET.** By Lemma 1, GET looks at the only place where $s$ can be. By (H3) the entry for the string is in the slot of its hash, which FIND scans, and by (H4) it is there at most once. So GET returns the value of $s$ if it is a key, and NIL otherwise.

**PUT.** By Lemma 1 and the same argument, PUT updates the existing entry of $s$ if there is one, and else adds one entry, at the place where GET will look. So (H2) and (H4) hold, and (H3) holds except that $y$ may have $L + 1$ entries.

**BURST keeps the keys.** Each case of lines L9 to L11 replaces one container $y$ under a node $x$ and moves its entries; we show that each entry keeps the key it stands for.

- *Line L9.* $y$ is pure under symbol $c$ of $x$, so its entry $t$ stands for $u(x) c t$. The new node $z$ has $u(z) = u(x) c$. The empty entry becomes $z.value$, standing for $u(z)$. Each other entry $t$ goes into the hybrid container of $z$, which covers all symbols, as the string $t$, and stands for $u(z) t = u(x) c t$, with $t[0]$ in its range.
- *Line L10.* $y$ is hybrid under $x$ with range $[lo, hi)$, and its entries $t$ stand for $u(x) t$. The new containers are hybrid under $x$ with ranges that partition $[lo, hi)$, each pointer of the range now leads to the part that contains it, and each entry goes to the part that contains $t[0]$. So $t$ still stands for $u(x) t$ and lies in the container its first symbol points to.
- *Line L11.* $y$ is hybrid with range $[c, c + 1)$, so all its entries start with $c$ and stand for $u(x) t$ with $t = c t'$. As a pure container under $c$, the entry $t'$ stands for $u(x) c t'$, the same key.

In each case the moved entries are distinct strings in the new container, because they stood for distinct keys, and each is put in the slot of its hash. So (H2) to (H4) hold except for the size bound of the new containers, which line L12 puts on the work list.

**BURST ends.** Assume $L \ge 1$. A container processed at line L9 is pure with more than $L \ge 1$ entries, so it has a nonempty entry $t$, and the new node $z$ has $u(z) = u(x) c$, a proper prefix of the key $u(x) c t$. Node strings are distinct, so line L9 runs at most once for each proper prefix of a stored key, finitely often. Between two runs of line L9, the work list only processes containers under existing nodes. Line L10 replaces a container by parts with strictly smaller ranges, and line L11 turns a container with a range of one symbol into a pure one, which is not split again. For one node, the ranges of its hybrid containers partition its $R$ pointers, so at most $R - 1$ splits and $R$ conversions can happen before the next node is created. Hence the work list empties, and at that point every container has at most $L$ entries, so (H3) holds. $\blacksquare$
