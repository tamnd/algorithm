---
tag: X9HKD8
kind: algorithm
slug: thompson-nfa-simulation
name: Thompson's NFA simulation
aliases:
- Thompson's regex search algorithm
- NFA state-set simulation
- Thompson 1968 matcher
area: automata-and-parsing/regular-expressions
level: core
summary: Simulates an NFA on the input by tracking the set of active states, in O(mn) time.
solves: [regex-matching, regex-search]
model: word-ram
complexity:
  vars: {m: the size of the regular expression, n: the length of the text}
  time: {worst: O(m n)}
  space: {extra: Θ(m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1968
  people: [Ken Thompson]
  note: Thompson's search for the QED editor ran all states of the automaton of the pattern at once, one input character at a time.
prereqs: [thompson-construction, epsilon-closure, nfa-simulation]
see_also: [regex-matching, regex-search, pike-vm, lazy-dfa-construction, backtracking-regex-matching, redos, bit-parallel-regex-matching, backurs-indyk-regex-hardness]
sources:
  - paper: doi:10.1145/363347.363387
    title: Ken Thompson, Programming techniques, regular expression search algorithm, Communications of the ACM 11(6) (1968)
    locator: pp. 419 to 422
  - url: "https://swtch.com/~rsc/regexp/regexp1.html"
    title: Russ Cox, Regular Expression Matching Can Be Simple And Fast, 2007
    locator: sections Simulating the NFA, Implementation and Performance (the lists of states, the generation marks, and the pattern a?^n a^n)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 3.7.2, Simulation of an NFA, and Section 3.7.3, Efficiency of NFA Simulation
  - book: isbn:9780521813075
    title: Gonzalo Navarro and Mathieu Raffinot, Flexible Pattern Matching in Strings, Cambridge University Press, 2002
    locator: Chapter 5, Regular expression matching (Thompson's automaton and its simulation)
  - paper: doi:10.1145/128749.128755
    title: Eugene W. Myers, A four Russians algorithm for regular expression pattern matching, Journal of the ACM 39(2) (1992)
    locator: pp. 430 to 448 (the O(mn / log n) bound)
---

Thompson's NFA simulation decides whether a text matches a [regular expression](/regular-expression/) by compiling the expression with [Thompson's construction](/thompson-construction/) and then running the resulting NFA on the text with a list of all active states. For an expression of size $m$ and a text of length $n$ it takes $O(mn)$ time and $O(m)$ extra space in the worst case, whatever the pattern. It is the special case of [NFA simulation](/nfa-simulation/) for the automata that Thompson's construction builds, in which each state has at most two moves, and it is the reason why engines such as RE2 cannot suffer [ReDoS](/redos/).

## In plain words

Turn the pattern into a small map of points and arrows, where some arrows read a letter and some are free. Put a marker on the start point and on every point that free arrows reach from it. Then read the text one letter at a time. For each marked point that has an arrow with the current letter, put a marker at the end of that arrow, and again follow every free arrow from there. Remove the old markers.

A point is marked at most once at each step, so the work for one letter is at most the size of the map. At the end, the text matches if the end point of the map is marked. If at some step no point is marked, no way of reading the text can succeed, and you can stop.

## The problem

The input is a regular expression $r$ of size $m$, in the syntax of the [regular expression](/regular-expression/) page, and a text $w = a_1 \cdots a_n$. The output of the *match* version is whether $w \in L(r)$; this is [regex matching](/regex-matching/). The output of the *search* version is whether some substring $a_{i+1} \cdots a_j$ of $w$ is in $L(r)$; this is the decision form of [regex search](/regex-search/).

## The algorithm

Line L1 builds the Thompson NFA $N$ with start $q_0$ and the one accepting state $q_f$. Each state has either one symbol move, or up to two $\varepsilon$-moves, or no move. The array $\mathit{mark}$ holds, for each state, the last step at which the state was added to a list; it starts at $-1$ for all states. This makes "is $p$ already in the list?" an $O(1)$ test without clearing anything between steps.

```pseudo id=main
THOMPSON-MATCH(r, w)                         ▷ w = a1 ... an
L1  N ← THOMPSON(r); mark[q] ← −1 for each state q
L2  C ← an empty list; ADD(C, q0, 0)
L3  for i ← 1 to n do
L4      D ← an empty list
L5      for each state q in C, in order do
L6          if q has the move q --ai--> p then ADD(D, p, i)
L7      C ← D
L8      if C is empty then return false
L9  return mark[qf] = n                       ▷ qf ∈ C

ADD(L, q, i)                                  ▷ append q and its ε-closure, each state once
L10 K ← a stack that holds q
L11 while K is not empty do
L12     p ← pop K
L13     if mark[p] = i then continue
L14     mark[p] ← i; append p to L
L15     push the ε-targets of p on K
```

After line L7, $C$ is the list of states in which some run of $N$ on $a_1 \cdots a_i$ can be. Line L9 accepts if the last list contains $q_f$, which holds exactly when $\mathit{mark}[q_f] = n$.

**The search version.** At the end of each pass of the loop, also call ADD$(D, q_0, i)$, which starts a new run at position $i$, and return true as soon as $\mathit{mark}[q_f] = i$, or at the start if $\mathit{mark}[q_f] = 0$. Then $C$ holds the states of the runs that started at any earlier position, and the first $i$ with $q_f$ marked is the end of the earliest-ending match. Thompson's original program searched in this way.

## Example

Take $r = (a \mid b)^* abb$ and the Thompson NFA of the [construction](/thompson-construction/) page: 14 states, start 6, accepting state 13, symbol moves $0 \xrightarrow{a} 1$, $2 \xrightarrow{b} 3$, $8 \xrightarrow{a} 9$, $10 \xrightarrow{b} 11$ and $12 \xrightarrow{b} 13$. On $w = abab$ the lists, as sets, are:

| step | symbol | active states | $q_f = 13$ active? |
|---|---|---|---|
| 0 | | $\{0, 2, 4, 6, 7, 8\}$ | no |
| 1 | $a$ | $\{0, 1, 2, 4, 5, 7, 8, 9, 10\}$ | no |
| 2 | $b$ | $\{0, 2, 3, 4, 5, 7, 8, 11, 12\}$ | no |
| 3 | $a$ | $\{0, 1, 2, 4, 5, 7, 8, 9, 10\}$ | no |
| 4 | $b$ | $\{0, 2, 3, 4, 5, 7, 8, 11, 12\}$ | no |

In step 1, states 0 and 8 have moves on $a$, to 1 and 9. ADD from 1 follows $1 \to 5 \to 4 \to 0, 2$ and $5 \to 7 \to 8$; ADD from 9 adds 9 and 10. In step 2, states 2 and 10 read $b$, and 11 leads to 12. State 13 would come from 12 on one more $b$, so $abab$ is rejected and $ababb$ is accepted.

**A pattern that defeats backtracking.** Let $r_k = (a \mid \varepsilon)^k a^k$, the pattern $a?^k a^k$ of Cox's article, and $w = a^k$. The match must choose $\varepsilon$ in all $k$ optional parts. A greedy [backtracking matcher](/backtracking-regex-matching/) tries $a$ first in each of them and needs about $2^k$ attempts; CPython's `re` module takes over a second for $k = 24$, about five times longer for each increase of $k$ by 2. The simulation does $k$ steps on a list of at most $6k - 1$ states:

| $k$ | NFA states | largest list | state visits in total |
|---|---|---|---|
| 3 | 24 | 17 | 54 |
| 10 | 80 | 59 | 460 |
| 20 | 160 | 119 | 1720 |
| 29 | 232 | 173 | 3538 |

## Correctness

Write $E(S)$ for the set of states reachable from $S$ by $\varepsilon$-moves, and $R(v)$ for the set of states in which a run of $N$ on $v$ can end. ADD$(L, q, i)$ appends to $L$ exactly the states of $E(\{q\})$ that do not have mark $i$ yet, and marks them: line L13 skips a state at its second visit, so each state is appended at most once per step, and every $\varepsilon$-target of an appended state is pushed. So after lines L4 to L6, the list $D$ holds each state of $E(\{p : q \in C,\ q \xrightarrow{a_i} p\})$ exactly once. With the invariant $C = R(a_1 \cdots a_{i-1})$ before pass $i$, the one-step lemma of [NFA simulation](/nfa-simulation/) gives $D = R(a_1 \cdots a_i)$. Line L8 is correct because an empty set of runs stays empty, and line L9 tests $q_f \in R(w)$, which is the definition of acceptance. Together with $L(N) = L(r)$ from the [Thompson construction](/thompson-construction/), this shows that the algorithm returns true if and only if $w \in L(r)$. The full proof, with the search version, is below.

## Complexity

- **Construction.** Line L1 costs $\Theta(m)$ and gives at most $2m$ states and $4m$ moves.
- **One step.** In pass $i$, each state is appended to $D$ at most once, by the mark test, and each appended state pushes at most two targets. A state can be pushed more often than it is appended, but each push comes from one appended state, so a step pushes at most $2 \cdot 2m$ states. The loop of line L5 reads each state of $C$ once. So a pass costs $O(m)$.
- **Total.** $O(m)$ for the construction plus $O(m)$ per symbol gives $O(mn)$ time in the worst case on the [word RAM](/word-ram/), and the search version has the same bound. The space is $O(m)$ for the NFA, the two lists, the stack and the marks; the text is read once, from left to right.
- **Lower bound for this method.** On $r_k$ above the lists have $\Theta(k)$ states for $\Theta(k)$ steps, so the bound $O(mn)$ is reached up to a constant factor. No algorithm is known that beats $mn$ by more than a polylogarithmic factor, and the [Backurs and Indyk](/backurs-indyk-regex-hardness/) results explain why, under the strong exponential time hypothesis.

## Properties

- **Pattern-independent bound.** The time is $O(mn)$ for every pattern and text. A backtracking matcher can take $2^{\Theta(n)}$ time on the same inputs.
- **Online.** The text is read once, without going back, so the method works on a stream.
- **No recursion.** Both the construction and ADD use explicit stacks, so long texts and deeply nested patterns are safe.
- **Ordered lists.** The lists keep the order in which states are added. Pushing the $\varepsilon$-targets in reverse order at line L15 makes the first target be visited first. The order does not change the answer, but the [Pike VM](/pike-vm/) uses it to give the threads priorities and to report the same submatches as a backtracking engine.
- **Regular features only.** The method relies on the finite state set. [Backreferences](/backreference/) cannot be simulated this way, because the state would have to remember a substring of unbounded length.

## Variants and improvements

- **Lazy DFA.** Cache each list, as a set, together with its successor on each symbol. A repeated set costs one lookup instead of $O(m)$ work. This is the [lazy DFA construction](/lazy-dfa-construction/) of RE2 and grep, with the simulation as the fallback when the cache fills up.
- **Submatches.** The [Pike VM](/pike-vm/) attaches to each active state the positions of the capture groups, and keeps only the highest-priority thread for each state. It reports [submatches](/submatch-extraction/) in the same $O(mn)$ time.
- **Bit-parallel simulation.** When the number of states fits in a machine word, store the set as one word and update it with a few word operations per symbol ([bit-parallel regex matching](/bit-parallel-regex-matching/)).
- **Myers's speedup.** Myers (1992) cut the expression into blocks of $O(\log n)$ states and precomputed their behavior, which gives $O(mn / \log n)$ time.
- **Leftmost-longest search.** Store with each active state the smallest start position of the runs that reach it, stop adding $q_0$ once a match is found, and run until the list is empty, keeping the match with the smallest start and then the largest end. This finds the leftmost-longest match that [POSIX semantics](/posix-regex-semantics/) asks for, in the same $O(mn)$ time.

## When to use it

Use it when the pattern or the text comes from an untrusted source, or when a worst-case bound is a requirement: it is the safe default for a regex library. Use a DFA, built eagerly or lazily, when the same pattern is matched against much text and the DFA stays small. Use backtracking only when the pattern needs features beyond regular languages, such as backreferences, and the input is trusted or the time is bounded.

## Pitfalls

- **No mark test.** Without line L13, a state can enter a list once for each run that reaches it, and on $r_k$ the lists grow like the number of runs, which is exponential. Worse, a cycle of $\varepsilon$-moves, as in $(a^*)^*$, makes ADD loop forever. The mark test is what makes the method terminate and run in polynomial time.
- **Clearing a set each step.** Resetting a boolean array of $2m$ entries costs $O(m)$, which is within the bound but slow; a hash set rebuilt each step is slower. The step number in $\mathit{mark}$ avoids any reset.
- **Forgetting the closure.** ADD must follow $\varepsilon$-moves from the start state at line L2 and after every symbol, the last one included. Without the closure at line L2, the pattern $a^*$ rejects the empty text.
- **Recursive closure.** A recursive ADD overflows the call stack on long chains of $\varepsilon$-moves, which a pattern like $((a^*)^*)^*$ with deep nesting creates. Use a stack as in lines L10 to L15.
- **Search by restarting.** Running the match version once from each start position costs $O(mn^2)$. Add $q_0$ to the list at each step instead.

## Implementations

## History

Thompson (1968) published the method as a regular expression search for the QED text editor. The program parsed the pattern into postfix form, compiled it into IBM 7094 machine code, and at run time kept a list of the active parts of the code for the current and the next character; a new start was added at each character, so the search found matches anywhere in a line. Thompson later used the method in the Unix editor ed, from which grep came. Cox (2007) revived the method in a widely read article that compared it with the backtracking engines of Perl, Python and PCRE on the pattern $a?^n a^n$.

## References
