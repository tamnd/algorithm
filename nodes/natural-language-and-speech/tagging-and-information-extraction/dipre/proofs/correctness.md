---
title: "DIPRE: the pattern step ends and gives patterns that match their own occurrences, and the loop ends"
proves: [correctness]
status: full
---

DIPRE is a heuristic: nothing guarantees that a pair it finds is a true fact, and the example of the page shows a false pair. What can be proved is what each step computes. The line numbers refer to the pseudocode on the page; a page is a pair (url, text), and a field is a string of 1 to max_len characters with no '<', '>' or newline.

## Claim 1: the longest common prefix and suffix

The code computes the longest common prefix of a list as the longest common prefix of its smallest and largest strings in lexicographic order. Let $P$ be the longest common prefix of the smallest string $a$ and the largest string $b$. Every common prefix of the list is a common prefix of $a$ and $b$, so it is no longer than $P$. Conversely, take any string $s$ of the list, so $a \le s \le b$. If $s$ did not start with $P$, let $k$ be the first position where $s$ and $P$ differ (or $s$ ends before $|P|$). If $s$ ends first, or $s_k < P_k$, then $s < a$; if $s_k > P_k$, then $s > b$. Both contradict $a \le s \le b$. So $P$ is a common prefix of the whole list and it is the longest. The longest common suffix is the longest common prefix of the reversed strings. The test file checks both against a search over all candidates.

## Claim 2: pattern generation ends, and each kept pattern satisfies the test

Line L4 puts each occurrence into exactly one group, by (order, middle). Line L5 builds one candidate pattern for a group. If the group has fewer than 2 occurrences it is dropped. If specificity times $n$ is above $t$ (line L6), the pattern is kept. Otherwise, if all the urls are equal, the group is dropped. Otherwise line L7 splits the group by the character of each url just after the common url prefix $U$ (or by the end of the url). Since $U$ is the longest common prefix and the urls are not all equal, at least two urls differ at that position, so the group splits into at least 2 nonempty parts, each smaller than the group. Each part has a longer common url prefix than $U$, or it consists of urls that end at $|U|$ and are therefore all equal. So each recursive call has fewer occurrences than its caller, the recursion depth is at most the group size, and the procedure ends. A pattern is returned only from line L6, so every kept pattern was built from at least 2 occurrences and has specificity times $n > t$. In particular its specificity is positive, so its url prefix, prefix, middle and suffix are all nonempty.

## Claim 3: a kept pattern matches every occurrence that is consistent with it

Let $p = (\text{order}, U, A, M, B)$ be a kept pattern and $o$ an occurrence with the same order and middle $M$ whose url starts with $U$, whose prefix ends with $A$ and whose suffix starts with $B$. Every occurrence that line L5 used to build $p$ has these properties, because $U$, $A$ and $B$ are its longest common prefix of the urls, longest common suffix of the prefixes and longest common prefix of the suffixes. Let $o$ have its first string $x$ at position $i$ of its page and its second string $y$ right after the middle. The prefix of $o$ is the text just before $i$, so $A$ ends at $i$; $M$ starts at $i + |x|$; and $B$ starts right after $y$. The function match_pattern tries every position of $A$, then every position of $M$ that starts 1 to max_len characters later, then every position of $B$ that starts 1 to max_len characters after the end of $M$, so it tries this one when $x$ and $y$ have at most max_len characters and reads off $x$ and $y$ as the two fields. If $x$ and $y$ are fields (true for the pairs of the example and of the tests), the pair of $o$ is in the output. The test file checks this on random pages, and checks match_pattern itself against a search over all choices of the four cut points.

## Claim 4: the loop ends, and the set of pairs only grows

Line L8 adds the matches to the known set and never removes a pair, so the set grows weakly from round to round. Every pair that a pattern finds is two substrings of the pages of length at most max_len, and there are finitely many such pairs. So the set can grow only finitely many times, and the stop test of line L9 (no new pair in a round) is met after a finite number of rounds, even without a round limit. The test file checks that the sizes never go down.

## What is not proved

Whether a found pair is a true fact depends on the pages and on $t$. In the example of the page, the round that adds "William Gibson, Neuromancer" also makes the pattern of the first site more general, and the next round accepts the false pair "chapter, Contents". Raising $t$ removes the false pair and also most of the true ones. This trade is a measurement on data, not a theorem.
