---
title: Sequitur keeps the expansion and both invariants after each symbol
proves: [correctness]
status: full
---

We write $G$ for the grammar, $S$ for its start rule, and $|G|$ for the total length of the right-hand sides. A *digram* is a pair of adjacent symbols in one right-hand side. Two occurrences of a digram *overlap* when they share a node, which happens only inside a run $xxx$. A digram occurrence is *full* when it is the whole right-hand side of a rule other than $S$. The two invariants are:

- **(U) digram uniqueness:** no digram has two occurrences that do not overlap;
- **(R) rule utility:** each rule other than $S$ is used at least twice in the right-hand sides.

The implementation keeps two work lists: *todo* holds nodes whose digram must be checked, and *underused* holds rules whose use count fell to 1. Each time a link $x \to y$ between two symbols is made, the node $x$ is pushed to todo and the digram is added to the hash table; each time a use of a rule $r$ is removed and $r$ has 1 use left, $r$ is pushed to underused. Line L3 runs while one list is not empty, and it takes from underused first.

**Assumption (A).** When line L8 runs, at most one of the two occurrences $x$ and $m$ is full. Nevill-Manning and Witten do not treat the case of two full occurrences, and we do not prove that it never happens. The implementation raises an error if it does. The tests check both invariants after every symbol on all binary strings up to length 14, all strings over 3 letters up to length 8, and random inputs, and they never meet this case.

**Theorem.** Assume (A). After each call of APPEND with the symbol $w_t$, the expansion of $S$ is $w_1 \cdots w_t$, and $G$ satisfies (U) and (R). Over $n$ calls, the repair loop does at most $2n$ changes to the grammar in total.

## The expansion

Each change of the grammar keeps the expansion of each rule that remains.

- Line L1 puts $w_t$ at the end of $S$, so the expansion of $S$ grows by $w_t$.
- A *substitution* replaces an occurrence of a digram $ab$ by a nonterminal $R$ whose right-hand side is $ab$. In line L8 this right-hand side is the full occurrence; in lines L9 and L10 it is a new rule made of a copy of $ab$. The expansion of $R$ is that of $ab$, so the rule that held the occurrence keeps its expansion.
- An *expansion* in line L5 replaces the last use of a rule $r$ by the right-hand side of $r$, and deletes $r$. This also keeps the expansion of the rule that held the use.

No rule is used in its own derivation, because each new rule $R$ in line L9 is made from symbols that already exist, and substitutions and expansions only move symbols that already derive from the rule. So the expansion is defined, and by induction on $t$ the expansion of $S$ is $w_1 \cdots w_t$.

## Lengths and uses

Each rule other than $S$ has a right-hand side of length at least 2. A new rule has length 2. An expansion makes a right-hand side longer. A substitution shortens a rule by 1, but it is never applied to a full occurrence: in line L8 the full one is kept and the other one is replaced, and line L9 runs only when neither is full. A rule of length 2 has only one digram, which is full, so it is never shortened.

Each rule is used at least once until line L5 deletes it. A new rule gets 2 uses in line L10. A use is removed only by a substitution, which removes the two nodes of one digram, or by line L5. When one use is removed and 1 use is left, the rule goes on underused, and line L3 takes underused first, so line L5 expands the rule before any other change. A substitution can remove two uses of $r$ at once only for the digram $rr$. In line L8 the full rule then also holds two uses of $r$, and in line L9 the new rule receives two new uses of $r$ before the substitutions; in both cases $r$ keeps at least 2 uses. So no rule reaches 0 uses.

## The loop ends, with at most 2n changes

Count the changes of the grammar over all $n$ calls. Let $e$ be the number of substitutions in line L8, $c$ the number of new rules in line L9, and $x$ the number of expansions in line L5.

- Line L1 raises $|G|$ by 1.
- A substitution in line L8 lowers $|G|$ by 1.
- Lines L9 and L10 add a rule of length 2 and make two substitutions, so $|G|$ does not change.
- An expansion removes one use node and keeps the other symbols, so $|G|$ falls by 1, and the number of rules falls by 1.

So after $n$ calls, $|G| = n - e - x \ge 0$, which gives $e + x \le n$. The number of rules other than $S$ is $c - x$, and each has length at least 2, so $2(c - x) \le |G| = n - e - x$. Since $x \le c$, this gives $2c \le n + x \le n + c$, so $c \le n$. Each change of the grammar makes at most 6 new links, and each pass of line L3 that does not change the grammar removes one item from a work list. Line L8 pushes $x$ back once more in the case where $x$ is full. So the number of passes is at most a constant times $n$, and each call of APPEND ends.

## Rule utility at the end of a call

Suppose that, when the loop ends, a rule $r$ other than $S$ has exactly 1 use. It has not 0 uses, by the section on uses. Its count reached 1 at the last removal of one of its uses, and at that moment $r$ was pushed to underused. After that the count did not change. When line L4 took $r$ from underused, $r$ was alive with 1 use, so line L5 deleted it. This contradicts that $r$ exists at the end. So (R) holds.

## Digram uniqueness at the end of a call

Say that a node $x$ is *checked* when line L6 takes it from todo while $x$ is alive and $x$ and the node after it both hold symbols. Each time the link out of $x$ is made, $x$ is pushed. So for each digram occurrence that exists at the end of the loop, starting at node $x$, there is a check of $x$ after the link was made, and in all such checks the digram of $x$ is the final one.

Look at the last check of $x$. Line L6 searches for an occurrence $m$ of the same digram that does not overlap $x$. If it finds one, line L7 calls MATCH, and there are three cases.

- $m$ is full: $x$ is replaced, so its node is no longer alive at the end. This contradicts that the occurrence at $x$ exists at the end.
- $x$ is full: $m$ is replaced and $x$ is pushed again, so this was not the last check of $x$.
- Neither is full: both are replaced, which again removes $x$.

By (A), these are all cases. So at the last check of $x$, no occurrence of the digram that does not overlap $x$ existed.

Now suppose that two occurrences, at nodes $x$ and $y$, of the same digram exist at the end and do not overlap. Let $y$ be the one whose last check came later. The last check of $x$ came after the final link out of $x$ was made, so at the last check of $y$ the occurrence at $x$ already existed with its final digram. Whether two occurrences overlap depends only on the links out of $x$ and out of $y$, which are final. So at that check, $x$ was an occurrence that did not overlap $y$, and line L6 would have found one. This contradicts the paragraph above. So (U) holds.

## Conclusion

Before the first call, $S$ is empty and both invariants hold. By the sections above, each call of APPEND ends, keeps the expansion of $S$ equal to the prefix read so far, and leaves (U) and (R) true. The total number of changes over $n$ calls is $e + c + x \le 2n$, because $e + x \le n$ and $c \le n$, and each change and each pass of the loop takes a constant number of hash table operations and list operations, apart from the search of line L6 over the stored occurrences of one digram. $\blacksquare$
