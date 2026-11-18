---
title: GRAPHEME-BOUNDARIES returns exactly the grapheme cluster boundaries of the UAX 29 rules
proves: [correctness, termination]
status: full
---

**Setup.** Let $s = s[0] \cdots s[n-1]$ with $n \ge 1$. For a position $i$ with $1 \le i \le n-1$, the rules GB3 to GB999 are tried in order, and the first rule whose left side matches a suffix of $s[0 \ldots i-1]$ and whose right side matches a prefix of $s[i \ldots n-1]$ decides. Rules GB1 and GB2 make 0 and $n$ boundaries. Write $a = \mathrm{GCB}(s[i-1])$ and $b = \mathrm{GCB}(s[i])$. The right side of every rule from GB3 to GB13 is a single code point, so only the left sides need a context.

Define three predicates of a prefix $u = s[0 \ldots j-1]$:

- $E(u)$: $u$ ends with a match of \p{ExtPict} Extend*, where Extend means GCB=Extend.
- $R(u)$: the number of GCB=RI code points at the end of $u$, that is, the largest $r$ such that the last $r$ code points of $u$ all have GCB=RI.
- $C(u)$: the state of $u$ for GB9c. $C(u)$ = linked if $u$ ends with a match of \p{InCB=Consonant} [\p{InCB=Extend}\p{InCB=Linker}]* \p{InCB=Linker} [\p{InCB=Extend}\p{InCB=Linker}]*. $C(u)$ = consonant if $u$ ends with a match of \p{InCB=Consonant} \p{InCB=Extend}*. $C(u)$ = none otherwise.

The two patterns of $C$ cannot both match: in the first one a Linker follows the last Consonant, and in the second one it does not. So $C$ is well defined.

**Claim 1 (invariant).** After line L4 of the iteration for $i$, $ep = E(s[0 \ldots i-1])$, $pict = E(s[0 \ldots i-2])$, $ri = R(s[0 \ldots i-1])$ and $conj = C(s[0 \ldots i-1])$. Here $s[0 \ldots -1]$ is the empty string, and all three predicates of the empty string are false, 0 and none.

*Proof.* By induction on $i$. Before the first iteration, line L1 sets the values of the empty prefix. Assume that before the update of iteration $i$ the variables hold the values for $u = s[0 \ldots i-2]$, and let $c = s[i-1]$.

- $pict \leftarrow ep$ gives $pict = E(u) = E(s[0 \ldots i-2])$.
- $uc$ ends with ExtPict Extend* if and only if $c$ is ExtPict (the run of Extend is empty), or $c$ has GCB=Extend and $u$ ends with ExtPict Extend*. So $ep \leftarrow \mathrm{ExtPict}(c) \lor (ep \land \mathrm{GCB}(c) = \mathrm{Extend})$ gives $E(uc)$.
- The run of RI at the end of $uc$ is the run of $u$ plus one if $c$ is RI, and empty otherwise. This is the update of $ri$.
- For $conj$: if InCB($c$) = Consonant, the second pattern matches $uc$ with an empty Extend run, and the first cannot, because it must end in Extend or Linker. So $C(uc)$ = consonant. If InCB($c$) = Linker, then $uc$ matches the first pattern exactly when $u$ ends with Consonant [Extend Linker]*, that is, when $C(u) \ne$ none; so $C(uc)$ = linked or none as the update says. If InCB($c$) = Extend, a match for $u$ extends by $c$ in either pattern, and a match for $uc$ shortens to a match for $u$, so $C(uc) = C(u)$. If $c$ has no InCB value, no pattern can end at $c$, so $C(uc)$ = none. $\square$

**Claim 2.** In the iteration for $i$, the value of $x$ set by lines L5 to L12 is true exactly when the first matching rule at $i$ is a ÷ rule.

*Proof.* Each line tests the left and right sides of its rules.

- L5 is GB3, CR × LF. L6 is GB4 and GB5: (Control | CR | LF) ÷ and ÷ (Control | CR | LF). L7 is GB6, GB7 and GB8, which are pairs of GCB values.
- L8 is GB9 (× (Extend | ZWJ)), GB9a (× SpacingMark) and GB9b (Prepend ×).
- L9 is GB9c: the left side matches a suffix of $s[0 \ldots i-1]$ if and only if $C(s[0 \ldots i-1])$ = linked, which is $conj$ = linked by Claim 1.
- L10 is GB11: the left side \p{ExtPict} Extend* ZWJ matches a suffix of $s[0 \ldots i-1]$ if and only if $s[i-1]$ is ZWJ and $E(s[0 \ldots i-2])$ holds, which is $a$ = ZWJ and $pict$ by Claim 1.
- L11 is GB12 and GB13. Their left sides are sot (RI RI)* RI and [^RI] (RI RI)* RI. Together they match exactly when the run of RI at the end of $s[0 \ldots i-1]$ has odd length, which is $ri$ odd by Claim 1. The test $a$ = RI is implied by $ri$ odd and kept for clarity.
- L12 is GB999, Any ÷ Any, which always matches.

The lines form an if and else-if chain in the order of the rule numbers, so the first line whose test holds belongs to the first rule that matches. Its value of $x$ is false for a × rule and true for a ÷ rule. $\square$

**Claim 3.** GRAPHEME-BOUNDARIES($s$) returns the sorted list of all grapheme cluster boundaries of $s$.

*Proof.* Line L1 puts 0 in $B$ (GB1). By Claim 2, line L13 appends $i$ exactly when $i$ is a boundary, for each $i$ from 1 to $n - 1$ in increasing order. Line L14 appends $n$ (GB2). So $B$ holds each boundary once, in increasing order. $\square$

**Legacy clusters.** With extended = false, lines L8 and L9 lose the tests for GB9a, GB9b and GB9c. The legacy rule list is the extended list without these three rules, so the same proof applies with the shorter chain.

**Word and sentence boundaries.** The implementation follows the same scheme: the rules before WB4 and SB5 are tested on the raw neighbours, and the later rules on the neighbours after the ignored code points are skipped. The rule "X (Extend | Format | ZWJ)* → X" of WB4 means that a later rule sees the last code point $X$ before the run, unless $X$ is sot, CR, LF or Newline, where the first ignored code point stands for itself. The helper that walks back stops at those code points, so each later rule is tested on the sequence that WB4 defines. The same holds for SB5 with Extend and Format, and the stops sot and ParaSep. Each rule is then a test of its left and right sides on that sequence, in the order of the rule numbers, so the argument of Claim 2 applies.

**Termination.** The loop of line L2 runs $n - 1$ times, and each iteration does a fixed number of table lookups and comparisons. For words and sentences, each walk back or forward stops at the ends of the string, so each position takes at most $O(n)$ steps and the procedure stops.
