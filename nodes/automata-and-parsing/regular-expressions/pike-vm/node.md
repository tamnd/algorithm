---
tag: VF24KJ
kind: algorithm
slug: pike-vm
name: Pike VM
aliases:
- Pike's VM
- thread-list NFA simulation with submatches
area: automata-and-parsing/regular-expressions
level: advanced
summary: Runs Thompson's simulation with thread priorities so that it returns leftmost-first submatches.
solves: [submatch-extraction, regex-search]
model: word-ram
complexity:
  vars: {m: the number of instructions of the compiled program, n: the length of the text, c: the number of capture groups, counting the whole match as group 0}
  time: {worst: O(m n c)}
  space: {extra: O(m c)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 1985
  people: [Rob Pike]
  note: Pike's regular expression code for the editor sam, written around 1985 according to Cox, kept submatch positions in the threads of an NFA simulation; Cox (2009) described it as a virtual machine and gave it this name.
prereqs: [thompson-nfa-simulation, thompson-construction]
see_also: [backtracking-regex-matching, one-pass-regex-matching, lazy-dfa-construction, greedy-and-lazy-quantifiers, posix-regex-semantics, submatch-extraction, backreference-matching, redos]
sources:
  - url: "https://swtch.com/~rsc/regexp/regexp2.html"
    title: Russ Cox, Regular Expression Matching, the Virtual Machine Approach (2009)
    locator: sections A Regular Expression Virtual Machine (the instructions char, match, jmp, split and save), Pike's Implementation (one thread per program counter, each with its own saved pointers), Ambiguous Submatching (split prefers its first target; the code for greedy and non-greedy repetition; addthread must follow jmp, split and save in priority order), Digression, POSIX Submatching, and Digression, A Forgotten Technique (sam, written around 1985, and the exercises in Aho, Hopcroft and Ullman 1974)
  - url: "https://swtch.com/~rsc/regexp/regexp1.html"
    title: Russ Cox, Regular Expression Matching Can Be Simple And Fast (2007)
    locator: section History and References (Pike's implementation for sam, extracted by Dave Presotto into a library in the Eighth Edition, and Henry Spencer's backtracking reimplementation of its interface)
  - paper: doi:10.1002/spe.4380171105
    title: Rob Pike, The text editor sam, Software Practice and Experience 17(11) (1987)
    locator: pp. 813 to 845
  - paper: doi:10.1145/363347.363387
    title: Ken Thompson, Programming techniques, regular expression search algorithm, Communications of the ACM 11(6) (1968)
    locator: pp. 419 to 422 (the simulation that keeps a list of current states and advances all of them one symbol at a time)
  - book: isbn:9780201000290
    title: Alfred V. Aho, John E. Hopcroft and Jeffrey D. Ullman, The Design and Analysis of Computer Algorithms, Addison-Wesley (1974)
    locator: Chapter 9, Exercises 9.6 and 9.7 (attach a start position to each state of the NFA simulation), as quoted by Cox
---

The Pike VM finds the leftmost-first match of a [regular expression](/regular-expression/) in a text, together with the positions of its capture groups, in time $O(m n c)$ for a program of $m$ instructions, a text of length $n$ and $c$ groups. It is [Thompson's NFA simulation](/thompson-nfa-simulation/) with two changes: each thread carries its own copy of the group positions, and the thread list is kept in priority order, so that when two threads reach the same instruction the one a [backtracking matcher](/backtracking-regex-matching/) would try first wins. When no star has a nullable body, it gives the same groups as a backtracking engine, without the exponential worst case.

## In plain words

Turn the pattern into a small program with instructions such as "read an a", "try this first, else that", and "write down the current position in slot 3". Run many copies of the program in step, one per way of reading the text so far, all at the same text position. Each copy has its own notebook of written positions.

When two copies reach the same instruction at the same position, they will behave the same from then on, so keep only one: the one with higher priority, that is, the one that made the more preferred choices so far. Keep the copies in priority order. When a copy reaches the end of the program, it is a match, and every copy behind it can be dropped. The notebook of the last such copy gives the groups.

## The problem

**Notation.** This site writes regular expressions with $r \mid s$ for union, $rs$ for concatenation, $r^*$ for the star, $\varepsilon$ for the empty string and $\emptyset$ for the empty language. Star binds tightest, then concatenation, then union. This page adds capture groups $(r)$, numbered by their opening parentheses, and the non-greedy star $r^{*?}$. Neither changes the language of an expression; they only choose between the ways a text can match. Backreferences, which do change the language and take it beyond the regular languages, are not supported: see [backreference matching](/backreference-matching/).

Given an expression $r$ and a text $w = a_1 \cdots a_n$, find the match that a priority-ordered backtracking engine reports: the least start position $s$ such that some substring $w[s:e]$ is in $L(r)$, and among the matches from $s$ the one whose choices are preferred. For each group $k$, report the span $(s_k, e_k)$ of its last iteration in that match, or nothing if it took no part. A union prefers its left side, a greedy star prefers one more iteration and a non-greedy star prefers one fewer. The [Correctness](#correctness) section makes this priority precise.

## The algorithm

The expression is compiled into a program, as in [Thompson's construction](/thompson-construction/), with these instructions:

| instruction | meaning |
|---|---|
| char $a$ | read the symbol $a$ and go to the next instruction |
| split $x, y$ | go to $x$ and to $y$, preferring $x$ |
| jmp $x$ | go to $x$ |
| save $k$ | write the current position into slot $k$ and go on |
| fail | stop this thread (the code for $\emptyset$) |
| match | report a match |

The code for $r \mid s$ is "split L1, L2; L1: code for $r$; jmp L3; L2: code for $s$; L3:". The code for $r^*$ is "L1: split L2, L3; L2: code for $r$; jmp L1; L3:", and for $r^{*?}$ the split is "split L3, L2". Group $k$ is "save $2k$; code; save $2k+1$", and the whole program is "save 0; code for $r$; save 1; match".

A thread is a pair of an instruction number pc and an array caps of $2c$ slots. A thread list holds at most one thread for each pc, in priority order.

```pseudo id=main
PIKE-VM(prog, w)
L1  clist ← an empty thread list; matched ← none
L2  for i ← 0 to n do
L3      if matched = none then ADD(clist, 0, all slots unset, i)
L4      if clist is empty then break
L5      nlist ← an empty thread list
L6      for each thread (pc, caps) of clist, in order do
L7          if prog[pc] = char a then (if i < n and a_{i+1} = a then ADD(nlist, pc + 1, caps, i + 1))
L8          else ▷ prog[pc] = match
L9              matched ← caps
L10             break ▷ drop the threads of lower priority
L11     clist ← nlist
L12 if matched = none then return none
L13 return the spans (caps[2k], caps[2k+1]) of matched, for each group k

ADD(list, pc, caps, i) ▷ depth first, in priority order, with an explicit stack
L14 if pc is already in list then return
L15 if prog[pc] = jmp x then ADD(list, x, caps, i)
L16 else if prog[pc] = split x, y then ADD(list, x, caps, i); ADD(list, y, caps, i)
L17 else if prog[pc] = save k then ADD(list, pc + 1, caps with slot k set to i, i)
L18 else if prog[pc] ≠ fail then append (pc, caps) to list
```

ADD marks pc as present when it first reaches it, even for jmp, split and save, so a later thread that reaches the same instruction at the same position is dropped. Line L3 starts a new thread at each position, with the lowest priority, until a match is found; this makes the search unanchored. At line L10 the threads after a match are dropped, but the threads before it go on, and if one of them reaches match later, it replaces the match found so far.

## Example

Take $r = (a \mid ab)(c \mid bcd)(d^*)$ and $w = abcd$. The program has 23 instructions:

| pc | instruction | pc | instruction | pc | instruction |
|---|---|---|---|---|---|
| 0 | save 0 | 8 | save 4 | 16 | save 6 |
| 1 | save 2 | 9 | split 10, 12 | 17 | split 18, 20 |
| 2 | split 3, 5 | 10 | char c | 18 | char d |
| 3 | char a | 11 | jmp 15 | 19 | jmp 17 |
| 4 | jmp 7 | 12 | char b | 20 | save 7 |
| 5 | char a | 13 | char c | 21 | save 1 |
| 6 | char b | 14 | char d | 22 | match |
| 7 | save 3 | 15 | save 5 | | |

The thread lists, with the start of each thread and the groups that are already closed:

| i | threads in priority order (pc, start, groups) |
|---|---|
| 0 | (3, 0), (5, 0) |
| 1 | (10, 0, $g_1 = a$), (12, 0, $g_1 = a$), (6, 0), (3, 1), (5, 1) |
| 2 | (13, 0, $g_1 = a$), (10, 0, $g_1 = ab$), (12, 0, $g_1 = ab$), (3, 2), (5, 2) |
| 3 | (14, 0, $g_1 = a$), (18, 0, $g_1 = ab$, $g_2 = c$), (22, 0, $g_1 = ab$, $g_2 = c$, $g_3 = \varepsilon$), (3, 3), (5, 3) |
| 4 | (18, 0, $g_1 = a$, $g_2 = bcd$), (22, 0, $g_1 = a$, $g_2 = bcd$, $g_3 = \varepsilon$) |

At $i = 3$ the thread at pc 22 is a match for $abc$, with groups $ab$, $c$ and $\varepsilon$, and the two threads behind it are dropped. The two threads ahead of it go on. At $i = 4$ the thread from pc 14 has read d and, through save 5 and save 6, has reached pc 18 and pc 22 first. The thread from pc 18 at $i = 3$ also reads d, but its next instructions 19 and 17 lead to pcs that are already in the list, so it is dropped. The match at pc 22 replaces the old one. The result is the span $(0, 4)$ with $g_1 = (0, 1) = a$, $g_2 = (1, 4) = bcd$ and $g_3 = (4, 4) = \varepsilon$, the same as Python's `re`. A [POSIX](/posix-regex-semantics/) matcher gives $ab$, $c$ and $d$ instead, because it prefers the longest $g_1$.

## Correctness

Call a pair (pc, position) a configuration. Define the reference result as that of the backtracking matcher that tries start positions from left to right, explores the configurations depth first with the preferred branch of every split first, never visits a configuration twice, and stops at the first match it meets. As in Thompson's simulation, the lists hold every reachable char and match instruction at each position until a match is found, and the threads are sorted by start, so the VM finds a match exactly when some substring is in $L(r)$, and its match has the leftmost start. Two further facts give the priority. First, the configurations at one position are first visited by the backtracker in exactly the order of the VM's list, because both follow the same entries in the same order with the same depth-first rule. Second, the descendants of a thread that comes before a match in the list are all visited by the backtracker before that match, and those of a thread after it are visited after. So the last match the VM records is the first match the backtracker meets. When no star has a nullable body, no configuration can be met twice on one path, and this is the lexicographically least accepting path, the result of plain backtracking. The full proof is below.

## Complexity

Compiling takes $O(m)$ time. In each of the $n + 1$ rounds, ADD visits each instruction at most once per list, because of the check at line L14, and a save copies the $2c$ slots. So a round costs $O(m c)$ time, and the whole run $O(m n c)$. Two lists of at most $m$ threads, each with $2c$ slots, take $O(m c)$ space. With no groups, $c = 1$ and the bound is Thompson's $O(m n)$.

## Properties

- The run time is linear in the text for a fixed expression, with no exponential case, unlike [backtracking](/backtracking-regex-matching/), which is the cause of [ReDoS](/redos/).
- The VM is online: it reads each symbol once and keeps two lists, so it never needs to back up in the text.
- When no star has a nullable body, it returns the result of plain priority backtracking, which is what Perl and Python's `re` compute. With such a star, engines differ on empty iterations. The VM drops a thread that comes back to the split of a star at the same position, so on $(a^*)^*$ and the empty text it reports no span for group 1, and on $aa$ it reports $(0, 2)$; Python's `re` reports $(0, 0)$ and $(2, 2)$.
- The VM can stop as soon as the list is empty, and after the first match it adds no new start threads.

## Variants and improvements

- **Thompson VM.** Without save instructions and without priorities, the VM is [Thompson's simulation](/thompson-nfa-simulation/) and only answers yes or no; a [lazy DFA](/lazy-dfa-construction/) answers that question faster.
- **One-pass matching.** When the expression never needs more than one thread to decide, [one-pass matching](/one-pass-regex-matching/) records the groups with a single set of slots and no copying.
- **Anchored and full matches.** Adding the start thread only at $i = 0$ anchors the match at the start; accepting match only at $i = n$ requires the match to end at the end. The implementation below offers both.
- **POSIX submatches.** Cox explains that for POSIX submatching a forward simulation that merges threads may need unbounded state per thread, and describes two ways around it: running the machine backward, and comparing all threads regularly and keeping a per-thread priority, as Kuklewicz's regex-tdfa package does.
- **Fewer copies.** Copying the slots on every save is the main cost of the VM. Slot arrays can be shared between threads and copied only when a thread writes, which keeps the bound and lowers the constant.

## When to use it

Use the Pike VM when groups are needed and the expression or the text is not under your control, so that the exponential worst case of backtracking is not acceptable. If only a yes or no answer, or only the span of the whole match, is needed, a DFA-based search is faster. If the expression is one-pass, the one-pass matcher is faster still. Expressions with backreferences need a backtracking engine and its worst case.

## Pitfalls

- The thread list must be built depth first in priority order. Cox notes that his first version of `pikevm`, which added the targets of jmp, split and save to the end of the current list instead of following them at once, did not completely respect thread priority.
- The check at line L14 must apply to jmp, split and save too, not only to char and match. Otherwise an empty loop, as in $(\varepsilon)^*$, makes ADD run forever.
- At line L10 only the threads after the match are dropped. Stopping the whole run at the first match gives the match that ends first, which need not be the leftmost-first one and need not even start leftmost: on the example above it would give $abc$ instead of $abcd$, and for $xab \mid a$ on $xab$ it would give the span $(1, 2)$ of the a, since that thread reaches match one step before the thread that started at 0.
- Leftmost-first is not leftmost-longest. A tool that promises POSIX results, such as [grep](/grep/) with [extended regular expressions](/extended-regular-expressions/), needs a different merging rule.

## Implementations

## History

Thompson (1968) simulated the automaton of a regular expression by advancing a list of states one symbol at a time. Aho, Hopcroft and Ullman (1974) set as exercises the problem of attaching start positions to the states of this simulation, to find the match that ends first and the leftmost-longest match. According to Cox, Rob Pike wrote a new regular expression implementation for his editor sam, which kept submatch positions in each thread of the simulation. Cox places it in the early 1980s in one article and around 1985 in another, and credits Bruce Janson with the submatch changes a couple of years after the original. Dave Presotto extracted it into a library in the Eighth Edition of Unix, and Henry Spencer reimplemented the same interface with backtracking, which became the basis of the backtracking engines of Perl, PCRE and Python. Cox (2009) described the technique as a virtual machine with prioritized threads and called it Pike's VM.

## References
