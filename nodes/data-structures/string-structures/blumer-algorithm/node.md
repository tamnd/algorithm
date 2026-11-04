---
tag: EMPS9K
kind: algorithm
slug: blumer-algorithm
name: Blumer et al. suffix automaton algorithm
aliases:
- DAWG construction
area: data-structures/string-structures
level: advanced
summary: Online linear-time construction of the suffix automaton by extending the automaton one character at a time.
solves: [suffix-automaton-construction]
model: word-ram
complexity:
  vars: {n: the length of the text, σ: the number of distinct symbols in the text}
  time: {worst: O(n log σ)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: false, adaptive: false, online: true, deterministic: true, comparison: false, recursive: false}
history:
  year: 1985
  people: [Anselm Blumer, Janet Blumer, David Haussler, Andrzej Ehrenfeucht, Mu-Tian Chen, Joel Seiferas]
  note: Blumer and coauthors defined the directed acyclic word graph, bounded its size by 2n − 1 states and 3n − 4 edges, and built it online in linear time.
prereqs: [suffix-automaton, deterministic-finite-automaton, suffix-link]
see_also: [suffix-automaton, suffix-automaton-construction, distinct-substrings-counting, ukkonen-algorithm, weiner-algorithm, longest-common-substring, myhill-nerode-theorem, potential-method]
sources:
  - paper: Anselm Blumer, Janet Blumer, David Haussler, Andrzej Ehrenfeucht, Mu-Tian Chen and Joel Seiferas, The smallest automaton recognizing the subwords of a text, Theoretical Computer Science 40, 1985, doi:10.1016/0304-3975(85)90157-4
    locator: pages 31 to 55, the end-set equivalence, the size bounds, and the online construction with suffix pointers and the split of a state
  - paper: Maxime Crochemore, Transducers and repetitions, Theoretical Computer Science 45(1), 1986, doi:10.1016/0304-3975(86)90041-1
    locator: pages 63 to 86, the minimal suffix automaton, its construction and its use for repetitions
  - book: isbn:9780521848992
    title: Maxime Crochemore, Christophe Hancart and Thierry Lecroq, Algorithms on Strings
    locator: Chapter 5, the suffix automaton, its size and its online construction
---

The algorithm of Blumer, Blumer, Haussler, Ehrenfeucht, Chen and Seiferas builds the [suffix automaton](/suffix-automaton/) of a text, the minimal deterministic automaton that accepts the suffixes of the text; with all its states made accepting, it accepts the substrings, and it is then called the directed acyclic word graph (DAWG). It reads the text from left to right and after each symbol updates the automaton of the prefix read so far, so it is an [online algorithm](/online-algorithm/). Each step adds one state, walks back along [suffix links](/suffix-link/) to add transitions, and sometimes splits a state in two by *cloning*. The total time is linear for a fixed alphabet. This page covers the construction and its analysis; the structure itself and its uses are on the page of the suffix automaton.

## In plain words

The automaton has one state for each group of substrings that end at exactly the same places in the text. When a new letter arrives, the text has new substrings: the old suffixes followed by the letter. They all end at the new last place.

So the algorithm makes a state for the whole text, then walks through the old suffixes from longest to shortest, using the suffix links, and gives each the new letter as a way to reach the new state. It stops at the first suffix that already had that letter. Then one state may hold strings that now end at different places: some at the new end, some not. The algorithm splits it, copying its arrows into a twin. The walk is long only rarely, so the total work stays linear.

## The problem

Given a text $t = t_1 \cdots t_n$, build the minimal deterministic automaton whose language is the set of suffixes of $t$, with its suffix links ([suffix automaton construction](/suffix-automaton-construction/)). For a string $w$, let $endpos(w)$ be the set of end positions of its occurrences. Two substrings are equivalent when they have the same end set, and the states of the automaton are these classes, plus the initial state for the empty string. For a state $v$, $len(v)$ is the length of its longest string, and the suffix link $link(v)$ is the state of the longest suffix of that string that lies in another class. The strings of $v$ are the suffixes of its longest string with lengths in $(len(link(v)), len(v)]$.

## The algorithm

The automaton of the empty text has the initial state 0 with $len = 0$ and no link; $last = 0$. To append a symbol $c$:

```pseudo id=main
EXTEND(c)
L1  cur ← a new state with len(cur) = len(last) + 1
L2  p ← last; while p ≠ NIL and p has no c-transition: δ(p, c) ← cur; p ← link(p)
L3  if p = NIL then link(cur) ← 0
    else q ← δ(p, c)
L4      if len(q) = len(p) + 1 then link(cur) ← q
        else
L5          clone ← a new state with len(clone) = len(p) + 1, the transitions of q, and link(clone) = link(q)
L6          while p ≠ NIL and δ(p, c) = q: δ(p, c) ← clone; p ← link(p)
L7          link(q) ← clone; link(cur) ← clone
L8  last ← cur
```

The states on the suffix link path from $last$ are the states of the suffixes of the text, so they are the accepting states of the suffix automaton when one wants to recognize suffixes only.

**Line L2.** The new substrings are the strings $wc$ for the suffixes $w$ of the old text. The states on the link path from $last$ hold these suffixes, longest first. A state $p$ with no $c$-transition holds suffixes $w$ for which $wc$ never occurred, so $wc$ ends only at the new position, and it belongs to $cur$.

**Lines L3 to L7.** The first state $p$ with a $c$-transition holds the longest suffix $w$ with $wc$ already a substring, and $wc$ is the longest suffix of the new text that occurred before, so it determines $link(cur)$. If $len(q) = len(p) + 1$, the longest string of $q$ is $wc$, and all strings of $q$ gain the new end position together: $q$ is the link. Blumer et al. call the transition from $p$ to $q$ *solid* in this case. Otherwise $q$ also holds strings longer than $wc$, which do not end at the new position, so $q$ splits: the strings up to length $len(p) + 1$ move to the clone, which has the same transitions, and the transitions on $c$ from $p$ and its link ancestors that led to $q$ are redirected to the clone.

## Example

Building the automaton of abbb. States are numbered in order of creation; the table gives the state of each step's new strings.

| step | text | new states | transitions added or changed | links set |
|---|---|---|---|---|
| 1 | a | 1 (len 1) | 0 →a 1 | 1 → 0 |
| 2 | ab | 2 (len 2) | 1 →b 2, 0 →b 2 | 2 → 0 |
| 3 | abb | 3 (len 3), clone 4 (len 1) | 2 →b 3; 4 →b 3 copied from 2; 0 →b 4 instead of 2 | 2 → 4, 3 → 4 |
| 4 | abbb | 5 (len 4), clone 6 (len 2) | 3 →b 5; 6 →b 5 copied from 3; 4 →b 6 instead of 3 | 3 → 6, 5 → 6 |

At step 3, the walk from $last = 2$ adds $2 \to_b 3$ and reaches the initial state, which has the transition $0 \to_b 2$. State 2 had $len = 2$ and held ab and b, but now b ends at positions 2 and 3 while ab ends only at 2, so state 2 splits: b moves to the clone 4. At step 4 the same happens to state 3, which held abb and bb: bb ends at positions 3 and 4 and moves to the clone 6. The walk of line L6 stops at state 0, whose $b$-transition already goes to 4.

The final automaton has 7 states:

| state | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| strings | ε | a | ab | abb | b | abbb, bbb | bb |
| len | 0 | 1 | 2 | 3 | 1 | 4 | 2 |
| link | NIL | 0 | 4 | 6 | 0 | 6 | 4 |

The text abbb has the 7 distinct nonempty substrings a, ab, abb, abbb, b, bb, bbb, and $\sum_{v \ne 0} (len(v) - len(link(v))) = 1 + 1 + 1 + 1 + 2 + 1 = 7$. The suffixes are the strings of the states on the link path 5, 6, 4, 0. A text $ab^{n-1}$ is the worst case for the number of states: it has $2n - 1$ states, here 7 for $n = 4$.

## Correctness

The proof shows by induction on the length of the text that after each call the states, transitions and links are those of the end set classes of the current text. The walk of line L2 handles the substrings that occur only at the new end, line L4 is the case where the class of $wc$ gains the new end as a whole, and lines L5 to L7 split the class of $wc$ when only its shorter strings gain it. Since the states are exactly the classes, the automaton is minimal for the suffixes of the text by the [Myhill-Nerode theorem](/myhill-nerode-theorem/). The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Blumer et al. prove that for $n \ge 2$ the automaton has at most $2n - 1$ states, and for $n \ge 3$ at most $3n - 4$ transitions; $ab^{n-1}$ and $ab^{n-2}c$ reach the bounds. Each step creates at most two states.

The time is linear apart from the cost of a transition lookup:

- Each iteration of line L2 adds a transition, and transitions are never removed, so these iterations total $O(n)$.
- Line L5 copies at most $\sigma$ transitions, and the copies are counted in the $3n - 4$ transitions too.
- For line L6, let $d(v)$ be the number of links from $v$ to the initial state, and take $d(last)$ as the potential. A transition goes from a state $x$ to a state of depth at most $d(x) + 1$, and each iteration of lines L2 and L6 moves $p$ one link up, so one step leaves $d(last)$ at most 3 larger than before, minus the number of iterations. So these iterations also total $O(n)$, by the [potential method](/potential-method/); the proof gives the details.

With transitions in a balanced search tree, each lookup costs $O(\log \sigma)$, so the total is $O(n \log \sigma)$; with arrays of size $\sigma$ it is $O(n)$ time and $O(n \sigma)$ space; with hash tables, as in the implementation, it is $O(n)$ expected. A single step can take $\Theta(n)$ time, so the bound is amortized.

## Properties

- **Online.** After reading $t_1 \cdots t_i$, the structure is the suffix automaton of that prefix, and it can answer queries before the rest arrives.
- **Minimal for suffixes, not for substrings.** Each state is one end set class, so no smaller deterministic automaton accepts the suffixes, with no separate minimization step. The minimal automaton of the substrings alone, the factor automaton, can be smaller: two substrings are equivalent there when their first occurrences end at the same place. For abb it has 4 states where the suffix automaton has 5.
- **Amortized.** One symbol can cause a long walk of line L2 or L6; the linear bound holds for the whole text.

## Variants and improvements

- **The suffix tree of the reversed text.** The suffix link tree of the automaton is the suffix tree of the reversed text. Appending a symbol to the text puts it at the front of the reversed text, which is the step of [Weiner's algorithm](/weiner-algorithm/), so the two constructions are closely related.
- **Compact DAWG.** The compact directed acyclic word graph merges chains of states with one transition, as a suffix tree merges unary nodes, and takes less space than both the automaton and the suffix tree.
- **Several texts.** Resetting $last$ to the initial state between texts, with extra care for states that already exist, builds the automaton of all substrings of a set of texts, which answers multi-string queries.
- **Counting and positions.** Storing for each state the number of positions in its end set, by summing over the suffix link tree after the build, gives the number of occurrences of each substring.

## When to use it

Use this construction when you need the substrings of a text as an automaton: to test substrings or count distinct substrings ([distinct substrings counting](/distinct-substrings-counting/)), to find the [longest common substring](/longest-common-substring/) by running a second string through the automaton, or when the text arrives online. For positional queries and string matching on fixed texts, a suffix array or a suffix tree from [Ukkonen's algorithm](/ukkonen-algorithm/) is a common alternative with similar costs.

## Pitfalls

- **Forgetting the clone's link and transitions.** The clone takes the link of $q$ and a copy of all its transitions; then $q$ and $cur$ link to the clone. Setting only some of these breaks later steps.
- **Redirecting too many transitions.** The loop of line L6 must stop at the first state whose $c$-transition does not go to $q$. Redirecting further changes transitions that are already correct.
- **Testing solidity by the target alone.** The test of line L4 compares lengths, $len(q) = len(p) + 1$. Testing whether $q$ is a clone, or whether $q$ was just created, gives wrong links.
- **Terminal states.** The states of the suffixes are only known after the last symbol: they are those on the link path from the final $last$. Marking states as accepting during the build is wrong, since the path changes.
- **Memory.** A dictionary or array per state costs much more than the $3n$ transitions suggest. For large texts use one flat table of transitions.

## Implementations

The Python class keeps $len$, $link$ and one dictionary of transitions per state, and appends one symbol at a time with lines L1 to L8. It also tests substrings and suffixes and counts distinct substrings. Its check builds a longest string for each state and verifies the size bounds. The tests replay the example, check the worst cases of the bounds, and compare 600 random texts against the substring set and against the number of end set classes, computed directly.

## History

Blumer, Blumer, Haussler, Ehrenfeucht, Chen and Seiferas introduced the directed acyclic word graph and its linear online construction in Theoretical Computer Science in 1985. Crochemore (1986) studied the same automaton as the minimal suffix automaton and used it for string matching and repetitions. The construction is now the standard way to build suffix automata.

## References
