---
title: Extendible hashing keeps its invariant and implements a dictionary
proves: [correctness, termination]
status: full
---

We write $\text{low}_j(x) = x \bmod 2^j$, and $P(T)$ for the set of pairs in the buckets that the directory points to. The invariant is the one of the page: (E1) each bucket $B$ has a pattern $p(B) < 2^{\ell(B)}$ with $\ell(B) \le d$, and $\text{dir}[i] = B$ exactly when $\text{low}_{\ell(B)}(i) = p(B)$; (E2) each pair $(k, v)$ in $B$ has $\text{low}_{\ell(B)}(h(k)) = p(B)$; (E3) the keys are distinct; (E4) $n = |P(T)|$; (E5) $|B| \le b$ unless $\ell(B) = W$. The hash values are in $\{0, \ldots, 2^W - 1\}$.

**Theorem.** Start with $d = 0$ and one empty bucket of depth 0, and apply any sequence of EH-INSERT, EH-SEARCH and EH-DELETE. Each operation ends, keeps (E1) to (E5), and keeps $P(T)$ equal to the map that the same sequence gives on an abstract dictionary. Each search returns the value of its key in that map, or NIL.

*Proof.* At the start, the one bucket has pattern 0 of depth 0, and $\text{dir}[0]$ points to it, so (E1) holds; the bucket is empty, so (E2) to (E5) hold.

**Step 1 (the right bucket).** Assume (E1) and (E2), and let $i = \text{low}_d(h(k))$. If a pair with key $k$ is in a bucket $B$, then by (E2) $p(B) = \text{low}_{\ell(B)}(h(k))$. Since $\ell(B) \le d$, $\text{low}_{\ell(B)}(i) = \text{low}_{\ell(B)}(h(k)) = p(B)$, so by (E1) $\text{dir}[i] = B$. Hence lines L1, L4 and L13 find the only bucket that can hold key $k$, and if it holds no pair with key $k$, then $k$ is not a key.

**Step 2 (search and delete).** By Step 1 and (E3), lines L2 and L3 return the value of $k$ or NIL. Lines L13 and L14 remove the only pair with key $k$, if there is one, and lower $n$ by 1. Removing a pair keeps (E1) to (E5), and the map loses exactly $k$.

**Step 3 (doubling, line L7).** Let the directory have $2^d$ entries with (E1), and set $\text{dir}[i + 2^d] = \text{dir}[i]$ for $0 \le i < 2^d$, then $d \leftarrow d + 1$. For $0 \le i < 2^{d+1}$, the new $\text{dir}[i]$ is the old $\text{dir}[\text{low}_d(i)]$. For a bucket $B$ with $\ell(B) \le d$, the new $\text{dir}[i] = B$ exactly when $\text{low}_{\ell(B)}(\text{low}_d(i)) = p(B)$, which is $\text{low}_{\ell(B)}(i) = p(B)$. So (E1) holds for the new depth. No pair moves, so (E2) to (E5) hold.

**Step 4 (split, lines L8 to L10).** Let $B$ have depth $\ell < d$ and pattern $p$; line L7 ensures $\ell < d$ before line L8, since it doubles when $\ell = d$. Lines L8 to L10 set both depths to $\ell + 1$, move to $B'$ the pairs whose hash has bit $\ell$ equal to 1, and move to $B'$ the directory entries $i$ with $\text{dir}[i] = B$ and bit $\ell$ of $i$ equal to 1. Give $B$ the pattern $p$ and $B'$ the pattern $p + 2^\ell$, both with $\ell + 1$ bits. An index $i$ with $\text{low}_\ell(i) = p$ has $\text{low}_{\ell+1}(i) = p$ when bit $\ell$ of $i$ is 0, and $p + 2^\ell$ when it is 1. So after line L10, $\text{dir}[i] = B$ exactly when $\text{low}_{\ell+1}(i) = p$, and $\text{dir}[i] = B'$ exactly when $\text{low}_{\ell+1}(i) = p + 2^\ell$, and $\ell + 1 \le d$. The other buckets and their entries do not change, so (E1) holds. A pair of $B$ had $\text{low}_\ell(h(k)) = p$, and the same case split on bit $\ell$ of $h(k)$ shows that it now satisfies (E2) in $B$ or in $B'$. The set $P(T)$ does not change, so (E3) and (E4) hold. The two new buckets have at most the old size of $B$, and (E5) is used only at line L12.

**Step 5 (insert).** If line L5 finds $k$, by Step 1 this is its only pair, and the value is replaced; nothing else changes. Else $k$ is not a key. While the bucket $B$ of $k$ is full and $\ell(B) < W$, a round of the loop does Steps 3 and 4 and then, by Step 1 applied to the new state, line L11 finds the bucket where a pair with key $k$ must go. Each round raises the local depth of the bucket of $k$ by 1: after the split, $k$'s bucket is $B$ or $B'$, both of depth $\ell(B) + 1$. Since this depth is at most $W$, the loop runs at most $W$ rounds and ends. At its end, the bucket $B$ of $k$ has fewer than $b$ pairs, or $\ell(B) = W$. Line L12 adds $(k, v)$ to $B = \text{dir}[\text{low}_d(h(k))]$. By (E1), $p(B) = \text{low}_{\ell(B)}(\text{low}_d(h(k))) = \text{low}_{\ell(B)}(h(k))$, so (E2) holds. $k$ was not a key, so (E3) holds, $n$ grows by 1, so (E4) holds, and $B$ now has at most $b$ pairs or depth $W$, so (E5) holds. The map is the old map plus $(k, v)$.

By induction on the number of operations, the theorem holds. $\blacksquare$
