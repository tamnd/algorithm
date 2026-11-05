---
tag: AA2R4Q
kind: algorithm
slug: backtracking-regex-matching
name: Backtracking regex matching
aliases:
- recursive backtracking matcher
- depth-first regex matching
area: automata-and-parsing/regular-expressions
level: core
summary: Explores pattern alternatives depth-first with backtracking; supports backreferences but can take exponential time.
solves: [regex-matching]
model: word-ram
complexity:
  vars: {m: the number of nodes of the regular expression, n: the length of the text}
  time: {worst: 2^(O(m^2 n)), best: O(1)}
  space: {extra: O(m^2 n)}
properties: {deterministic: true, recursive: false}
history:
  year: 1971
  people: [Ken Thompson, Henry Spencer]
  note: The regular expressions of the Unix editor ed, in First Edition Unix, were matched by recursive backtracking; Henry Spencer's later backtracking library became the model for the engines of Perl, PCRE and Python.
prereqs: [regular-expression, depth-first-search, stack]
see_also: [regex-matching, thompson-nfa-simulation, pike-vm, backreference, redos, greedy-and-lazy-quantifiers, memoization, lazy-dfa-construction]
sources:
  - url: "https://swtch.com/~rsc/regexp/regexp1.html"
    title: Russ Cox, Regular Expression Matching Can Be Simple And Fast (2007)
    locator: sections Regular Expression Search Algorithms (the backtracking approach), Performance (exponential time of backtracking engines) and History (ed, Henry Spencer's library, Perl, PCRE and Python)
  - url: "https://swtch.com/~rsc/regexp/regexp3.html"
    title: Russ Cox, Regular Expression Matching in the Wild (2010)
    locator: section Step 4, Match, part Where are the submatches (the bit-state backtracker of RE2, with a bitmap of visited state and position pairs)
  - book: isbn:9780201615869
    title: Brian W. Kernighan and Rob Pike, The Practice of Programming, Addison-Wesley (1999)
    locator: Section 9.2, Regular Expressions (a short recursive backtracking matcher)
  - book: isbn:9780596528126
    title: Jeffrey E. F. Friedl, Mastering Regular Expressions, third edition, O'Reilly (2006)
    locator: Chapter 4, The Mechanics of Expression Processing (backtracking, the order of choices, and the cost of failure)
---

Backtracking regex matching decides whether a string matches a [regular expression](/regular-expression/) by a [depth-first search](/depth-first-search/) over the choices of the expression: which side of a union to take, and whether to repeat a star once more. When a choice leads to a dead end, the search goes back to the last open choice and tries the other side. It is short to write and it extends at once to captures and [backreferences](/backreference/), which is why Perl, PCRE, Python, Java and JavaScript use it. Its cost is exponential time in the worst case, even on patterns without backreferences, while an automaton method such as [Thompson's NFA simulation](/thompson-nfa-simulation/) takes $O(mn)$ time.

## In plain words

Read the pattern and the text from left to right together. When the pattern offers a choice, such as "a or ab", take the first option and keep a note that the second one is still open. Go on until both end, which is a match, or until a letter does not fit.

When a letter does not fit, go back to the most recent note, return to the text position saved with it, and take the other option. If no note is left, there is no match.

A repeat such as "any number of a" is a choice at each step: one more round, or stop. Try one more round first. A round that reads nothing is cut off, so the search cannot loop forever.

The method is fast when the first choices are right. When choices fail late, the work can double with each letter of the text.

## The problem

**Notation.** This site writes regular expressions with $r \mid s$ for union, $rs$ for concatenation, $r^*$ for the star, $\varepsilon$ for the empty string and $\emptyset$ for the empty language. Star binds tightest, then concatenation, then union.

The input is a regular expression $r$ with $m$ nodes in its syntax tree and a text $w = w_1 \cdots w_n$. The output is true if $w \in L(r)$ and false otherwise. This is [regex matching](/regex-matching/) in the full-match form; the search form, which looks for a substring, is in the variants below.

A *configuration* is a pair $(i, k)$: the first $i$ symbols of $w$ are read, and $k$ is the list of what must still match the rest, the *continuation*. An item of $k$ is a regular expression or a marker $\mathrm{CHECK}(s^*, j)$, which records that an iteration of $s^*$ began at position $j$. The empty list is $[\,]$, and $x :: k$ is the list with head $x$ and tail $k$.

## The algorithm

```pseudo id=main
BACKTRACK(r, w)                          ▷ w = w1 ... wn; true iff w ∈ L(r)
L1  K ← a stack that holds the configuration (0, [r])
L2  while K is not empty do
L3      (i, k) ← pop K
L4      if k = [ ] then
L5          if i = n then return true
L6          continue                     ▷ dead end: text left over
L7      x ← head of k;  k′ ← tail of k
L8      if x = ∅ then continue           ▷ dead end
L9      if x = ε then push (i, k′)
L10     if x is a symbol a and i < n and w_{i+1} = a then push (i + 1, k′)
L11     if x = s | t then push (i, t :: k′); push (i, s :: k′)
L12     if x = s t then push (i, s :: t :: k′)
L13     if x = s* then push (i, k′); push (i, s :: CHECK(s*, i) :: k′)
L14     if x = CHECK(s*, j) and i > j then push (i, s* :: k′)
L15 return false
```

The stack $K$ holds the open choices. Line L11 pushes the right side of a union first, so the left side is popped and tried first. Line L13 pushes the exit of the star first, so one more iteration is tried first: this is the greedy order. Line L14 lets the star loop again only if the iteration that just ended read at least one symbol; an iteration that read nothing is a dead end, and the exit pushed at line L13 covers that case. Lines L5, L6, L8, L10 and L14 are the places where a path ends or fails, and the next pop at line L3 is the backtrack.

Continuations are linked lists that share their tails, so each push makes $O(1)$ new cells.

## Example

**One backtrack.** Let $r = (a \mid ab)c$ and $w = abc$. The configurations are popped in this order:

| step | $i$ | continuation $k$ | action |
|---|---|---|---|
| 1 | 0 | $[(a \mid ab)c]$ | L12: split the concatenation |
| 2 | 0 | $[a \mid ab,\ c]$ | L11: push the option $ab$, then the option $a$ |
| 3 | 0 | $[a,\ c]$ | L10: $w_1 = a$ fits |
| 4 | 1 | $[c]$ | L10: $w_2 = b$ is not $c$; dead end |
| 5 | 0 | $[ab,\ c]$ | backtrack to the open option; L12 |
| 6 | 0 | $[a,\ b,\ c]$ | L10 |
| 7 | 1 | $[b,\ c]$ | L10 |
| 8 | 2 | $[c]$ | L10 |
| 9 | 3 | $[\,]$ | L5: $i = n$, return true |

**The empty-iteration cut.** Let $r = (a \mid \varepsilon)^* b$ and $w = ab$. After the first iteration reads $a$, the configuration $(1, [\mathrm{CHECK}((a \mid \varepsilon)^*, 0),\ b])$ passes line L14 because $1 > 0$, and the star starts again at position 1. In the second iteration the option $a$ fails on $w_2 = b$, and the option $\varepsilon$ reaches $(1, [\mathrm{CHECK}((a \mid \varepsilon)^*, 1),\ b])$. Now $i = j = 1$, so line L14 cuts this path. The exit of the star, pushed at line L13, gives $(1, [b])$, then $(2, [\,])$, and the algorithm returns true after 12 pops. Without the cut, the option $\varepsilon$ would restart the star at the same position again and again.

**Exponential time.** With $r = (a \mid a)^* b$ and $w = a^n$, each $a$ can be read by either side of the union, so there are $2^n$ ways to read the text, and each fails at the end because $b$ is missing. The implementation below pops exactly $12 \cdot 2^n - 6$ configurations, which is $12{,}582{,}906$ for $n = 20$. On $a^{20} b$, where a match exists, the first path succeeds after 87 pops. For $r = (a^*)^* b$ on $a^n$ the count is $9 \cdot 2^n - 3$: the text $a^n$ can be cut into iterations of the outer star in $2^{n-1}$ ways.

## Correctness

Call a configuration *successful* if a sequence of the steps of lines L9 to L14 leads from it to $(n, [\,])$. The steps from a configuration, in the order of lines L8 to L14, define a tree of configurations rooted at $(0, [r])$, and the stack holds the unexplored nodes of this tree.

**Soundness.** Give each item a language: $L(\mathrm{CHECK}(s^*, j)) = L(s^*)$, and $L(x :: k) = L(x) L(k)$ with $L([\,]) = \{\varepsilon\}$. Each step from $(i, k)$ to $(i', k')$ keeps the property "$w_{i'+1} \cdots w_n \in L(k')$ implies $w_{i+1} \cdots w_n \in L(k)$"; for a star this uses $L(s) L(s^*) \subseteq L(s^*)$ and $\varepsilon \in L(s^*)$. The configuration $(n, [\,])$ has this property with the empty suffix, so a path from $(0, [r])$ to it gives $w \in L(r)$.

**Completeness.** By induction on the length of $u = w_{i+1} \cdots w_{i'}$ and then on the size of $x$: if $u \in L(x)$ and $(i', k)$ is successful, then $(i, x :: k)$ is successful. The case of a star is the only one that needs care: $u \in L(s)^*$ can be written as $u_1 \cdots u_p$ with each $u_q$ nonempty and in $L(s)$, so each iteration reads at least one symbol and passes line L14. With $i = 0$, $i' = n$ and $k = [\,]$, $w \in L(r)$ makes the root successful.

**Termination.** Each node has at most two children, so by König's lemma the tree is finite if it has no infinite path. On a path the position never decreases. Once it stops growing, the markers made later have $j$ equal to the position and fail at line L14, and every other step lowers the total size of the expressions in $k$. So every path is finite.

A depth-first search of a finite tree visits every node, so BACKTRACK returns true if and only if the root is successful, that is, if and only if $w \in L(r)$. The full proof is below.

## Complexity

- **Length of a path.** The expressions in a continuation are disjoint subtrees of $r$, so their total size is at most $m$, and there is at most one marker for each star of $r$. At a fixed position, each step lowers the total size by at least 1, except the steps of line L14 with $j < i$, and there are at most $m$ of those, each of which adds a size of at most $m$. So a path has $O(m^2)$ steps at each position and $O(m^2 (n + 1))$ steps in all.
- **Time.** The tree is binary with paths of length $O(m^2 (n + 1))$, so it has $2^{O(m^2 n)}$ nodes, and each pop costs $O(1)$ on the [word RAM](/word-ram/). For a fixed pattern this is $2^{O(n)}$, and the example $(a \mid a)^* b$ shows that $2^{\Omega(n)}$ is reached. In the best case, the first path succeeds or fails at once.
- **Space.** The stack holds at most one open sibling for each node of the current path, so it has $O(m^2 n)$ entries, and the shared lists add $O(1)$ cells per push on that path.
- **Compared with automata.** Thompson's simulation and the [Pike VM](/pike-vm/) take $O(mn)$ time in the worst case; a DFA takes $O(n)$ time after its construction.

## Properties

- **Leftmost-first priority.** The search finds the paths in a fixed order: the left side of a union before the right side, and one more iteration before the exit. The first path that succeeds is the match that Perl-style engines report; see [greedy and lazy quantifiers](/greedy-and-lazy-quantifiers/).
- **One path at a time.** The algorithm holds the state of one path, so it can carry any extra data along the path, such as the positions of capture groups or the strings that a [backreference](/backreference/) must repeat. Automaton methods follow all paths at once and cannot carry the captured strings.
- **Fast when the first guess is right.** On many practical patterns the first path matches, and the time is close to $n$.
- **Not online.** A failure can send the search back to an earlier position, so the text is read many times.
- **No recursion.** The explicit stack replaces the recursion of the usual short implementations, so deep patterns and long texts do not overflow the call stack.

## Variants and improvements

- **Recursive matcher.** Kernighan and Pike give a matcher of about 30 lines for the characters, `.`, `^`, `$` and `*`, where each function call is one choice and the call stack is the backtracking stack.
- **Compiled programs.** Real engines compile the pattern to a program with instructions such as CHAR, SPLIT, JMP and MATCH, and run the same search over (instruction, position) pairs. A SPLIT has a preferred and a second target; a lazy quantifier swaps them.
- **Search.** To find a substring, run the search from each start position $0, 1, \ldots, n$ in turn and accept at the first configuration $(i, [\,])$, with any $i$. This gives the leftmost match, and among the matches at that start, the first one in priority order.
- **Captures and backreferences.** Add an array of group positions to each configuration, or set and restore it on the way down and back. A backreference item $\backslash g$ compares the text at position $i$ with the captured substring. With backreferences the problem is NP-complete ([backreference matching](/backreference-matching/)), so no general fix for the exponential time is expected.
- **Memoization.** On a compiled program, a configuration is a pair (instruction, position). If a pair has been visited and failed, it fails again, so a bitmap of visited pairs makes the search take $O(mn)$ time and $O(mn)$ bits of space, and it keeps the priority order. RE2 uses this bit-state backtracker for small inputs, when the bitmap fits in 32 kilobytes (Cox, 2010). This is [memoization](/memoization/), and it is correct only without backreferences, where the future of a path depends on the pair alone.
- **Cutting choices.** Atomic groups and possessive quantifiers throw away the open choices of a subpattern. They can stop exponential searches, but they change the language that the pattern matches.

## When to use it

Use backtracking when the pattern needs backreferences or other features that no automaton supports, or for small patterns on trusted input where the simple code is worth more than a worst-case bound. For patterns or texts from untrusted users, use an automaton method such as the [Pike VM](/pike-vm/) or a [lazy DFA](/lazy-dfa-construction/), or at least memoize, since a crafted pattern or text can make backtracking run for years; this is [ReDoS](/redos/).

## Pitfalls

- **Empty iterations.** Without the test $i > j$ at line L14, a star whose body matches the empty string, such as $(a \mid \varepsilon)^*$ or $(a^*)^*$, loops forever at one position. Engines differ in how they cut such loops, and the choice changes which groups are set in some matches.
- **Exponential time without backreferences.** Nested stars such as `(a*)*`, `(a+)+` or unions of overlapping options under a star, such as `(a|a)*`, make the number of paths exponential when the match fails. Lazy quantifiers do not help, since a failing search must try every path in any order.
- **Recursion depth.** A recursive matcher uses one call per step of a path, which is about $m^2 n$ calls for long texts and overflows the call stack. Keep the stack explicit.
- **Memoization with backreferences.** The visited bitmap is wrong when backreferences are present, because two paths that reach the same (instruction, position) pair can hold different captured strings.
- **Search by retrying.** Running a full search from each start position costs up to $n$ times the cost of one search, even when each search alone is fast.

## Implementations

## History

Cox (2007) reports that the Unix editor `ed`, which appeared in First Edition Unix in 1971, and the first `grep` matched regular expressions by recursive backtracking, although Thompson had published a simulation of all paths at once in 1968. Henry Spencer later wrote a regular expression library from scratch that used backtracking, and it became the model for the engines of Perl, PCRE and Python. Cox also describes how Perl added partial memoization, and how RE2 restricts its bit-state backtracker to inputs that keep the bitmap small.

## References
