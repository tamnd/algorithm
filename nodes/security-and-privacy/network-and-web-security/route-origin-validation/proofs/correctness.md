---
title: Correctness of route origin validation with a trie
proves: [correctness]
status: full
---

**Setting.** Addresses of one family have $W$ bits. For a prefix $q$, write $|q|$ for its length and $q[0..|q|)$ for its first $|q|$ bits; the remaining bits are 0. The trie $T$ has a root for the empty string, and the node for a bit string $s$ has a child for bit $b$ if some VRP prefix starts with $s b$. A VRP $(q, \ell_{\max}, a)$ is stored at the node for $q[0..|q|)$. The route has prefix $P$ and origin $o$, which is an ASN or NONE.

**Lemma 1 (the loop visits the path of $P$).** At the start of iteration $i$ of line L3, node is the node for $P[0..i)$. The loop stops after iteration $i$ exactly when $i = |P|$ or no node exists for $P[0..i+1)$.

*Proof.* At $i = 0$, node is the root, the node for the empty string (line L2). If the loop continues after iteration $i$, line L7 moves node to the child for bit $P[i]$, which is the node for $P[0..i+1)$. Line L7 stops the loop when $i = |P|$ or that child does not exist. $\square$

**Lemma 2 (the visited VRPs are the covering VRPs).** The VRPs read at line L4, over the whole run, are exactly the VRPs that cover $P$, unless the loop returns Valid earlier.

*Proof.* A VRP with prefix $q$ covers $P$ if and only if $|q| \le |P|$ and $q[0..|q|) = P[0..|q|)$ (RFC 6811, Section 2). If it covers $P$, then the node for $q[0..|q|) = P[0..|q|)$ exists, since the VRP is stored there, and so do all nodes for the shorter strings $P[0..i)$ with $i \le |q|$, since the trie contains every prefix of a stored string. By Lemma 1 the loop does not stop before iteration $|q| \le |P|$, and at that iteration node is the node for $q[0..|q|)$, so line L4 reads the VRP. Conversely, a VRP read at iteration $i$ is stored at the node for $P[0..i)$ with $i \le |P|$, so its prefix $q$ has $|q| = i \le |P|$ and $q[0..|q|) = P[0..|q|)$, and it covers $P$. Each node is visited at most once, so each VRP is read at most once. $\square$

**Theorem.** VALIDATE$(T, P, o)$ returns Valid if at least one VRP matches the route, Invalid if at least one VRP covers $P$ and none matches, and NotFound if no VRP covers $P$.

*Proof.* By RFC 6811, Section 2, a VRP $(q, \ell_{\max}, a)$ matches the route if it covers $P$, $|P| \le \ell_{\max}$ and $o = a$, with the extra rules that NONE matches no VRP and no route matches a VRP with $a = 0$. Line L6 tests exactly these conditions for a covering VRP.

If some VRP matches, it covers $P$, so by Lemma 2 line L4 reads it unless the loop has already returned Valid. When line L6 tests it, the test succeeds and the result is Valid. If the loop returns Valid, line L6 succeeded for a covering VRP, so that VRP matches.

If no VRP matches, line L6 never succeeds, and the loop ends at line L8 with state. The variable state is NotFound at line L1 and becomes Invalid at line L5 the first time a VRP is read. By Lemma 2, a VRP is read if and only if some VRP covers $P$. So the result is Invalid if some VRP covers $P$ and NotFound otherwise. $\square$

**Cost.** By Lemma 1 the loop runs at most $|P| + 1$ iterations, each with $O(1)$ work outside line L4, and by Lemma 2 line L4 reads each of the $c$ covering VRPs at most once. The time is $O(|P| + c)$. $\blacksquare$
