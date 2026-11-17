---
title: The window scan finds the connected components of the linkage graph, and the pairs of one deletion form one cluster
proves: [correctness]
status: full
---

**Setting.** A pair is $q = (u_q, s_q, v_q, s'_q)$: the leftmost reference positions $u_q \le v_q$ of its two mates and their strands. Both mates have length $L$, and the span of $q$ is $v_q + L - u_q$. Lines L1 to L3 give each pair a type by the rules of the page and put each discordant pair in the group of its type and strand layout. Within one group $G$, two pairs $q, q'$ are *linked* when $|u_q - u_{q'}| \le d$ and $|v_q - v_{q'}| \le d$. The *linkage graph* of $G$ has the pairs as vertices and the linked pairs as edges. A cluster is a connected component of this graph.

**Lemma 1 (the scan sees every edge).** Lines L4 to L7 call UNION on every edge of the linkage graph of $G$, and on no other pair.

*Proof.* Line L4 sorts $G$ by $u$, so in the sorted order $u$ does not decrease. Line L5 takes each pair $q$ and the pairs $q'$ after it in that order, and stops at the first $q'$ with $u_{q'} - u_q > d$. Every later pair has an even larger $u$, so it also has $u - u_q > d$ and is not linked to $q$. So the scan visits, for each $q$, exactly the later pairs $q'$ with $0 \le u_{q'} - u_q \le d$, which are the later pairs with $|u_q - u_{q'}| \le d$. Line L6 tests the second condition and line L7 joins the pair only if it holds. Each edge $\{q, q'\}$ has one end earlier in the order, and the scan from that end visits the other. $\square$

**Lemma 2 (union-find gives the components).** After the scan, two pairs have the same union-find root exactly when they are in the same connected component of the linkage graph.

*Proof.* The union-find invariant is that the sets of the structure are the components of the graph made of the edges joined so far. It holds at the start, with every vertex alone and no edges. UNION on an edge $\{q, q'\}$ merges the sets of $q$ and $q'$, which is the component of the graph with the new edge. Path halving in FIND changes parents only to other members of the same set, so it keeps the sets. By Lemma 1, after the scan the joined edges are all the edges of the linkage graph. $\square$

**Theorem.** `call_svs` returns one call for each cluster with at least $s_{\min}$ pairs, in each group, and for no other set of pairs. The fields of a call are the type and strand layout of its group, the number of pairs, the bounds of line L9 and, for DEL and INS, the size from the median span.

*Proof.* By Lemma 2, the lists that `cluster` returns are the connected components of the linkage graph of each group. Line L8 keeps the components with at least $s_{\min}$ pairs, and line L9 computes the stated fields from the pairs of the component. Line L10 sorts the calls. $\square$

**Lemma 3 (the pairs of one deletion are linked).** Let the sample have a deletion of the reference bases $[a, b)$, and let $d \ge \mu + z\sigma - 2L$. Take two pairs that cross the deletion, with the left mate before it ($u + L \le a$) and the right mate after it ($v \ge b$), and with fragment lengths in the sample of at most $\mu + z\sigma$. Then the two pairs are linked.

*Proof.* In the sample, the fragment of a crossing pair covers $a - u$ bases before the junction and $v + L - b$ bases after it, so its length is $f = (a - u) + (v + L - b)$. Each part holds a whole mate, so each is at least $L$. From $f \le \mu + z\sigma$ and $v + L - b \ge L$ we get $a - u \le \mu + z\sigma - L$, and from $u + L \le a$ we get $a - u \ge L$. So $u$ lies in an interval of length $\mu + z\sigma - 2L$. In the same way, $v - b$ lies between 0 and $\mu + z\sigma - 2L$. So two such pairs differ by at most $\mu + z\sigma - 2L \le d$ at each end. $\square$

The same argument holds at each breakpoint of the other types: the two mates of a pair that crosses a breakpoint have distances to it that add up to its fragment length, so the mates of all such pairs lie in two windows of length at most $\mu + z\sigma$. With the default $d = \mu + z\sigma$, the pairs of one breakpoint pair (one deletion, one insertion, one end of an inversion, or one tandem duplication) are linked to each other, so they are in one cluster. The converse is not true: two events closer than $d$ at both ends can join into one cluster, and a single noise pair between two clusters can join them.

**What is a heuristic.** The classification of a pair is a test on its span and layout, and a concordant-looking pair can come from a variant, as an insertion smaller than $z\sigma$ shows. The bounds of line L9 hold for pairs that come from the event, and the size of a DEL or an INS is an estimate with a bias: the pairs that cross a deletion have fragment lengths cut to the range above, so their median span is not $\mu$ plus the deletion size. These are properties of the model, not of the code.

**Cost.** For $n$ discordant pairs, the types take $O(n)$, the sort $O(n \log n)$, and the scan $O(n w)$ comparisons, where $w$ is the largest number of pairs whose $u$ lies in one window of length $d$. With path halving and union by the smaller index, each FIND takes $O(\log n)$ amortized time, so the total is $O(n \log n + n w \log n)$.
