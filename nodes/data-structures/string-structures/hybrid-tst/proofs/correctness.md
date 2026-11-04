---
title: The hybrid TST operations keep the invariant and answer the string symbol table queries
proves: [correctness]
status: full
---

We use the pseudocode and the invariant (H1) to (H4) of the page. For a key $s$, its *place* is: $T.short$ if $\lvert s \rvert \le 1$; the value field of the cell of $s[0] s[1]$ if $\lvert s \rvert = 2$; and the TST of the cell of $s[0] s[1]$, with the key $s[2 ..]$, if $\lvert s \rvert > 2$. Each string has exactly one place, fixed by its length and its first two symbols, and two different strings with the same place in a TST differ in the suffix $s[2 ..]$, because they share the first two symbols.

**Lemma 1 (reduction).** Under (H1) to (H3), $s$ is a key with value $v$ if and only if its place holds $v$.

*Proof.* For $\lvert s \rvert \le 1$ this is (H1). For $\lvert s \rvert = 2$, (H2) says that the cell of $s$ is NIL exactly when no key starts with $s$, in which case $s$ is not a key, and else the cell value is the value of $s$. For $\lvert s \rvert > 2$, (H2) says that the TST of the cell holds $(s[2 ..], v)$ exactly when $s$ is a key with value $v$, and if the cell is NIL then no key starts with $s[0] s[1]$. $\square$

**GET.** Lines L1 to L4 read the place of $s$ when $\lvert s \rvert \le 2$, and return NIL when the cell is missing. Line L5 runs TST-GET on the TST of the cell, which by (H3) and the correctness of the TST search returns the value of $s[2 ..]$ in that TST or NIL. By Lemma 1, GET returns the value of $s$ or NIL.

**PUT.** Line L6 changes only $T.short$, so (H1) holds for the new set of keys and (H2), (H3) do not change. For $\lvert s \rvert \ge 2$, line L7 makes sure the cell of $s[0] s[1]$ exists; now some key starts with $s[0] s[1]$ (namely $s$, after this call), so (H2) holds for the existence of the cell. Line L8 sets the value of the key $s[0] s[1]$, and line L9 runs TST-PUT, which keeps (H3) and makes the TST hold $(s[2 ..], v)$ while the other pairs stay. Each line adds 1 to $T.n$ exactly when $s$ was not a key before, by Lemma 1, so (H4) holds.

**DELETE.** Line L10 is the case of a short key, as for PUT. If the cell is NIL at line L11, no key starts with $s[0] s[1]$, so $s$ is not a key and nothing changes. Lines L12 and L13 clear the place of $s$, by setting the cell value to NIL or by TST-DELETE, which keeps (H3) and removes exactly the pair of $s[2 ..]$. $T.n$ decreases exactly when $s$ was a key. Now (H2) can fail only in its first part: the cell exists, but it may hold no key. A cell holds a key exactly when its value is not NIL or its TST is not empty, because by (H3) a nonempty TST has no dead node and so holds at least one key (a leaf of the TST has no middle child, so it has a value). Line L14 frees the cell in exactly the case where it holds no key, so (H2) holds.

**KEYS-WITH-PREFIX.** We show that the call on $p$ returns the keys with prefix $p$ in lexicographic order. Every key $k$ with $p \preceq k$ lies, by Lemma 1, at its place.

- If $\lvert p \rvert \ge 2$, all keys with prefix $p$ start with $p[0] p[1]$ and have length at least 2, so they are in the cell of $p[0] p[1]$. If the cell is NIL there are none (line L17). If $\lvert p \rvert = 2$, the keys are $p$ itself, when the cell value is not NIL, and $p \cdot t$ for the keys $t$ of the TST, which the TST walk lists in order; $p$ comes first because it is a prefix of the others. If $\lvert p \rvert > 2$, the keys are $p[0] p[1] \cdot t$ for the keys $t$ of the TST with prefix $p[2 ..]$, which TST-KEYS-WITH-PREFIX lists in order (line L18). Adding a common prefix keeps the order.
- If $\lvert p \rvert = 1$, the keys with prefix $p$ are $p$ itself and, for each symbol $b$, the keys with prefix $p b$. Line L16 lists $p$ first, then the blocks for $b = \sigma_0, \ldots, \sigma_{R-1}$ in increasing order, each block given by the case $\lvert p b \rvert = 2$ above. A key in the block of $b$ is smaller than a key in the block of $b' > b$, because they first differ at position 1. So the list is sorted.
- If $p = \varepsilon$, the keys are $\varepsilon$, when it is a key, and the keys with prefix $\sigma$ for each symbol $\sigma$ in increasing order. Line L15 lists them in this order, and the same argument on position 0 shows that the list is sorted.

**LONGEST-PREFIX-OF.** The keys that are prefixes of $s$ are: $\varepsilon$ and $s[0]$, read from $T.short$; $s[0] s[1]$, read from the cell value; and $s[0] s[1] \cdot t$ for the keys $t$ of the cell TST that are prefixes of $s[2 ..]$. The TST walk along $s[2 ..]$ meets exactly the nodes of the prefixes of $s[2 ..]$ that have a node, by the correctness of the TST search, and records the longest one with a value. Taking the longest of all these candidates gives the answer. $\blacksquare$
