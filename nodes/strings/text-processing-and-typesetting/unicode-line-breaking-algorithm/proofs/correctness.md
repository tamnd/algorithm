---
title: LINE-BREAKS returns exactly the break opportunities of the rules LB1 to LB31
proves: [correctness, termination]
status: full
---

**Setup.** Let $s = s[0] \cdots s[n-1]$ with $n \ge 1$. By UAX 14, the result at a position $i$ with $1 \le i \le n-1$ is the action of the first rule, in the order LB4 to LB31, whose left side matches a suffix of $s[0 \ldots i-1]$ and whose right side matches a prefix of $s[i \ldots n-1]$. The action is ! (mandatory break), ÷ (break allowed) or × (no break). LB2 forbids a break at position 0 and LB3 makes a break at position $n$. The rules work on the classes after LB1, and the rules from LB11 on work on the text as LB9 and LB10 change it. In the patterns, $sot$ matches only the start of the text and $eot$ only the end.

Line L1 applies LB1 to each code point, so $c[i]$ is the resolved class of $s[i]$. Line L10 adds the mandatory break at $n$ of LB3 and adds nothing at 0, as LB2 says.

**Claim 1.** For $1 \le i \le n-1$, if one of the rules LB4 to LB9 matches at $i$, lines L5 to L8 give the action of the first of them. If none matches, the iteration reaches line L9.

*Proof.* The rules are LB4 `BK !`, LB5 `CR × LF`, `CR !`, `LF !`, `NL !`, LB6 `× (BK | CR | LF | NL)`, LB7 `× SP` and `× ZW`, LB8 `ZW SP* ÷`, LB8a `ZWJ ×`, and LB9, which gives × between `X (CM | ZWJ)*` and a following CM or ZWJ when X is not BK, CR, LF, NL, SP or ZW.

- Line L5 holds when $c[i-1]$ is BK, LF or NL, or is CR with $c[i] \ne$ LF. These are the cases where LB4 or one of the ! rules of LB5 matches, and no earlier rule matches, because `CR × LF` needs $c[i] = $ LF. So L5 gives !.
- If L5 does not hold and $c[i-1] = $ CR, then $c[i] = $ LF and LB5 gives ×. Else, LB6 and LB7 match exactly when $c[i]$ is in {BK, CR, LF, NL, SP, ZW}. This is line L6.
- At line L7 no earlier rule matches. The left side `ZW SP*` matches a suffix of $s[0 \ldots i-1]$ if and only if the last code point before the run of SP that ends at $i-1$ is ZW. The loop before L7 finds this code point.
- At line L8, LB8a matches if $c[i-1] = $ ZWJ. The function that builds the units puts a CM or ZWJ $s[i]$ into the unit of $s[i-1]$ exactly when $s[i-1]$ is not BK, CR, LF, NL, SP or ZW. In that case $s[i-1]$ is the end of a sequence `X (CM | ZWJ)*`, where X is the first code point of the unit, and X is not of an excluded class: either X has its own class, which is not excluded, or X is a CM or ZWJ that starts a unit and counts as AL. Conversely, if LB9 matches, the code point before the run of CM and ZWJ is a valid X, and every CM or ZWJ of the run, and $s[i]$ too, joins its unit. So unit$[i]$ = unit$[i-1]$ if and only if LB9 matches.

So each of L5 to L8 holds exactly when its rules match and no earlier rule does. $\square$

**The units.** By Claim 1, line L9 runs only where $s[i]$ starts a unit. Let $U = U[0] \cdots U[m-1]$ be the units and $k = $ unit$[i]$. LB9 says that each unit counts as its first code point X for the later rules, and LB10 says that a unit that starts with CM or ZWJ counts as AL. The unit records exactly this class, together with the first code point, whose general category and East Asian Width the rules LB15a, LB15b, LB19, LB19a, LB21a, LB28a, LB30 and LB30b read. So the rules LB11 to LB31 at position $i$ are the same rules on the string $U$ at the border between $U[k-1]$ and $U[k]$.

**Claim 2 (runs).** Let $Q$ be a set of classes and $P$ a class not in $Q$. The left side `P Q*` matches a suffix of $U[0 \ldots k-1]$ if and only if the unit just before the longest run of units of $Q$ that ends at $k-1$ has class $P$.

*Proof.* Let the longest run be $U[j+1 \ldots k-1]$. A match `P Q*` places P at some unit $U[t]$ with $U[t+1 \ldots k-1]$ in $Q$. Then $t \ge j$ because the run is the longest, and $t \le j$ because $U[t]$ has class $P \notin Q$ and all of $U[j+1 \ldots k-1]$ are in $Q$. So $t = j$. Conversely, if $U[j]$ has class P, the units $U[j \ldots k-1]$ match. $\square$

The function `back` finds $j$ for $Q$ = {SP} in LB14, LB15a, LB16 and LB17, and for $Q$ = {SY, IS} in LB25, where LB25 first steps over one CL or CP for the rules `NU (SY | IS)* (CL | CP) × (PO | PR)`. The pattern of LB15a puts a context before the quotation mark, and the test reads it at $U[j-1]$, or $sot$ when $j = 0$.

**Claim 3 (regional indicators).** The left side of LB30a, `sot (RI RI)* RI` or `[^RI] (RI RI)* RI`, matches a suffix of $U[0 \ldots k-1]$ if and only if the longest run of RI units that ends at $k-1$ has odd length.

*Proof.* Both patterns end with an odd run of RI that has a non-RI unit or the start of the text before it, so the run is the longest run. Conversely, a longest run of odd length matches one of the two patterns. $\square$

The list `ri` of the implementation holds the length of the longest run of RI units that ends at each unit, by the recurrence $r[k] = r[k-1] + 1$ if $U[k-1]$ and $U[k]$ are both RI, and $r[k] = 1$ or $0$ otherwise.

**Claim 4.** At a unit border that line L9 reaches, `rule_break` returns the action of the first rule among LB11 to LB31 that matches.

*Proof.* Each test in `rule_break` belongs to a rule, the tests come in the order of the rules, and each test returns the action of its rule. Each test holds if and only if both sides of its rule match:

- The tests of one class on each side compare the classes of $U[k-1]$ and $U[k]$, and where the rule says so, the category Pi or Pf, membership in `$EastAsian`, U+2010 or U+25CC.
- The tests with a fixed context also look at $U[k-2]$, $U[k+1]$ or $U[k+2]$, or report no match when the unit does not exist. Where the pattern allows $sot$ or $eot$ (LB15a, LB15b, LB19a, LB20a), the test treats a missing unit as a match.
- The tests with runs are correct by Claims 2 and 3.

Some tests cover several rules with the same action, such as the rules of LB25 with ×. Merging rules with the same action that follow each other does not change which action comes first. So the first test that holds gives the action of the first rule that matches. LB31 matches every position, so the function always returns. $\square$

By Claims 1 and 4, every position from 1 to $n-1$ gets the action of the first matching rule, and line L10 handles position $n$. The output lists the positions with action ÷ or !, in increasing order, with ! marked as mandatory. This is the result that UAX 14 defines.

**Termination.** Lines L1 and L2 make one pass over $s$. The loop of L4 runs $n-1$ times. Each step back over a run stops at the start of the text, and each test of `rule_break` takes a bounded number of steps apart from these runs. So the algorithm stops on every input.
