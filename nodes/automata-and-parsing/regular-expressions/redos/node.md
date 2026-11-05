---
tag: R02CTM
kind: concept
slug: redos
name: ReDoS (regular expression denial of service)
aliases:
- catastrophic backtracking
- exponential regex backtracking
area: automata-and-parsing/regular-expressions
level: intro
summary: A slowdown in which a backtracking matcher takes exponential time on crafted input.
prereqs: [regular-expression, backtracking-regex-matching]
see_also: [thompson-nfa-simulation, regex-ambiguity-detection, algorithmic-complexity-attack, pike-vm, lazy-dfa-construction, greedy-and-lazy-quantifiers, unambiguous-nfa, backurs-indyk-regex-hardness]
sources:
  - url: "https://swtch.com/~rsc/regexp/regexp1.html"
    title: Russ Cox, Regular Expression Matching Can Be Simple And Fast, 2007
    locator: the introduction and the section Performance (the pattern a?^n a^n on a^n, backtracking against Thompson's simulation)
  - paper: doi:10.1145/3236024.3236027
    title: James C. Davis, Christy A. Coghlan, Francisco Servant and Dongyoon Lee, The impact of regular expression denial of service (ReDoS) in practice, an empirical study at the ecosystem scale, ESEC/FSE 2018
    locator: pp. 246 to 256 (super-linear regexes in npm and pypi modules, and how developers repair them)
  - paper: doi:10.1007/978-3-319-40946-7_27
    title: Nicolaas Weideman, Brink van der Merwe, Martin Berglund and Bruce Watson, Analyzing matching time behavior of backtracking regular expression matchers by using ambiguity of NFA, CIAA 2016, Lecture Notes in Computer Science 9705
    locator: pp. 322 to 334 (exponential and polynomial backtracking related to the degree of ambiguity of the NFA)
  - paper: doi:10.1016/0304-3975(91)90381-B
    title: Andreas Weber and Helmut Seidl, On the degree of ambiguity of finite automata, Theoretical Computer Science 88(2) (1991)
    locator: pp. 325 to 349 (the criteria EDA and IDA for exponential and polynomial ambiguity)
  - book: isbn:9780596528126
    title: Jeffrey E. F. Friedl, Mastering Regular Expressions, third edition, O'Reilly (2006)
    locator: Chapter 4, The Mechanics of Expression Processing, and Chapter 6, Crafting an Efficient Expression
  - url: "https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/"
    title: John Graham-Cumming, Details of the Cloudflare outage on July 2, 2019
    locator: the sections on the regular expression at the heart of the outage and the appendix on backtracking
  - url: "https://stackstatus.net/post/147710624694/outage-postmortem-july-20-2016"
    title: Stack Exchange, Outage Postmortem, July 20, 2016
    locator: the whole post (the pattern that trims trailing white space, and the quadratic count of steps)
---

ReDoS is a denial of service in which an attacker sends a short input that makes a [backtracking regex matcher](/backtracking-regex-matching/) run for a time exponential, or a high polynomial, in the input length. It needs two things: a pattern in which some substring can be matched in many ways, and an engine that tries these ways one by one before it gives up. Engines that simulate the automaton, such as [Thompson's NFA simulation](/thompson-nfa-simulation/), run in time linear in the input for a fixed pattern and are not open to it. ReDoS is a special case of an [algorithmic complexity attack](/algorithmic-complexity-attack/).

## In plain words

Most regex libraries in scripting languages check a pattern by trial and error. At each choice in the pattern, they take one option and go on. If the rest fails, they come back and take the next option.

Some patterns give the engine a huge number of ways to read the same text. A pattern that says "one or more groups of one or more letters a, then b" can split a run of letters a into groups in very many ways. If the text has no b at the end, every split fails, and the engine tries all of them before it says no. One more letter doubles the work. Thirty letters can keep a server busy for a long time. An attacker who can choose the text, for example in a web form, can use this to stop the service.

## The idea

**Where the time goes.** A backtracking matcher walks the [syntax tree](/regular-expression/) of the pattern, or the NFA of the pattern, in depth-first order. At a union it tries the left branch first; at a star it tries one more round first (greedy) or stopping first (lazy). When the text does not match, the matcher returns only after it has tried every way to match every prefix of the text. So on a failing input, its running time is at least the number of distinct ways in which parts of the pattern match prefixes of the text. On a matching input it can stop early, but an attacker chooses a failing input.

**Exponential blowup.** Suppose the pattern has the form $x\,s^*\,z$, the string $u$ matches $s^*$ in at least two different ways, and the string $v$ makes the final part fail. Then on the text $u^n v$ the subpattern $s^*$ matches $u^n$ in at least $2^n$ ways: one independent choice for each copy of $u$. For each of these ways the matcher tries $z$ and fails, so it does at least $2^n$ steps. The pattern $(a \mid a)^* b$ with $u = a$ and $v = \varepsilon$ is the smallest case. Nested stars such as $(a^+)^+$ and $(a^*)^*$ give the same effect, because $a^k$ splits into nonempty pieces in $2^{k-1}$ ways.

**Polynomial blowup.** If two stars in a row can both read the same string, as in $a^* a^* b$, the matcher tries each way to share $a^n$ between them: $n + 1$ choices for the first star, and $O(n^2)$ attempts in total. With $k$ such stars in a row the count is $\Theta(n^k)$. A search for the leftmost match restarts at each position of the text, which adds one more factor of $n$; this is how a pattern with a single star becomes quadratic.

**The criterion.** In automaton terms, the exponential case is an NFA with a state $q$ and two different paths from $q$ to $q$ that read the same string; the polynomial case of degree $k$ is a chain of $k$ loops that can read the same string. These are the conditions that Weber and Seidl gave for the degree of ambiguity of an NFA to be exponential or polynomial, and Weideman, van der Merwe, Berglund and Watson (2016) showed how they bound the number of steps of a backtracking matcher. So the static check for ReDoS is a form of [regex ambiguity detection](/regex-ambiguity-detection/). Ambiguity is also what the blowup needs. If each state of the NFA can still reach acceptance and no string has two accepting runs (the NFA is [unambiguous](/unambiguous-nfa/)), then two partial runs on the same prefix never end in the same state, since extending both would give two accepting runs. So a backtracking matcher meets at most one run for each state and prefix, and its work is polynomial. The condition on the states matters: $(a \mid a)^* \emptyset$ denotes $\emptyset$, which is trivially unambiguous, but a backtracking matcher still tries all $2^n$ ways on $a^n$.

**The defenses.**

- **Use an automaton engine.** [Thompson's NFA simulation](/thompson-nfa-simulation/), the [Pike VM](/pike-vm/) and the [lazy DFA](/lazy-dfa-construction/) keep the set of all active states instead of trying runs one by one. They take $O(mn)$ time for a pattern of size $m$ and a text of length $n$. RE2, the Go `regexp` package and the Rust `regex` crate work this way. The price is that they do not support [backreferences](/backreference/) and support little or no [lookaround](/regex-lookaround/), the features that go beyond regular languages or that need extra machinery.
- **Rewrite the pattern.** Replace $(a \mid a)^*$ by $a^*$ and $(a^+)^+$ by $a^+$, so that each string has one way to match. Anchor the pattern, or make the parts that follow each other read disjoint sets of symbols.
- **Cut the backtracking.** Atomic groups `(?>...)` and possessive quantifiers `a*+` forbid the engine to come back into a part once it has matched. They change which strings match, so they are a change of meaning, not only of speed.
- **Bound the damage.** Limit the length of the input, or give each match a time limit. .NET, for example, accepts a match timeout.

## Examples

**Counting the attempts.** The table counts, for an exhaustive backtracking matcher that tries greedy stars and left branches first, how many times it tries to match the final $b$ before it reports that the text $a^n$ does not match the whole pattern.

| pattern | $n = 1$ | $n = 2$ | $n = 3$ | $n = 5$ | $n = 10$ | $n = 20$ | formula |
|---|---|---|---|---|---|---|---|
| $(a \mid a)^* b$ | 3 | 7 | 15 | 63 | 2047 | 2097151 | $2^{n+1} - 1$ |
| $(a^*)^* b$ | 2 | 4 | 8 | 32 | 1024 | 1048576 | $2^n$ |
| $(a \mid aa)^* b$ | 2 | 4 | 7 | 20 | 232 | 28656 | $F_{n+3} - 1$ |
| $a^* a^* b$ | 3 | 6 | 10 | 21 | 66 | 231 | $(n+1)(n+2)/2$ |
| $(a \mid b)^* a (a \mid b)^* b$ | 4 | 9 | 16 | 36 | 121 | 441 | $(n+1)^2$ |

Here $F_k$ is the $k$-th Fibonacci number. For $(a \mid a)^* b$, the star matches $a^k$ in $2^k$ ways for each $k$ from 0 to $n$, and each way is followed by one failed try of $b$, so the count is $\sum_{k=0}^{n} 2^k = 2^{n+1} - 1$. For $(a^*)^* b$, the empty match of the outer star gives one try, and each $a^k$ with $k \ge 1$ splits into nonempty rounds in $2^{k-1}$ ways, so the count is $1 + \sum_{k=1}^{n} 2^{k-1} = 2^n$. For $(a \mid aa)^* b$, the number of ways to write $k$ as an ordered sum of 1s and 2s is $F_{k+1}$, and $\sum_{k=0}^{n} F_{k+1} = F_{n+3} - 1$.

The same inputs cost a set-based simulation one step for each symbol of the text, with at most a few active states: 20 steps for $n = 20$. In CPython's `re` module, which backtracks, a full match of `(a|a)*b` against $a^n$ takes about twice as long for each extra $a$, and more than a second near $n = 24$ on a laptop.

**Stack Overflow, July 2016.** The site trimmed white space with the pattern `^[\s\u200c]+|[\s\u200c]+$`. A post contained about 20,000 spaces followed by another character. For the second branch, the search starts at each of the spaces, matches all the spaces to its right, and then fails at the final character, so the class test runs about $20000 + 19999 + \cdots + 1$, or about $2 \times 10^8$, times. This is quadratic, not exponential, and it made the home page slow enough that the load balancer took the site out of service for 34 minutes.

**Cloudflare, July 2019.** A new rule of a web application firewall contained a subexpression of the form `.*(?:.*=.*)`. The postmortem explains with the simpler `.*.*=.*`: three stars in a row that can all read the same characters, so a text with no `=` costs a number of steps cubic in its length. The rule took the CPUs of the network to full load, and the service was down for 27 minutes. Cloudflare planned to move to an engine with a run-time guarantee, such as RE2 or the Rust regex engine.

**A safe rewrite.** The patterns $(a \mid a)^* b$ and $a^* b$ denote the same language. The second has one way to match each $a^k$, so a backtracking matcher tries $b$ only $n + 1$ times on $a^n$.

## Where it is used

- **Security of web services.** Patterns that validate user input, such as e-mail addresses, URLs and headers, are the usual target. Davis, Coghlan, Servant and Lee (2018) found thousands of super-linear patterns in the JavaScript and Python package ecosystems, affecting more than 10,000 modules, and found that developers prefer to revise the pattern over truncating the input or writing a custom parser.
- **Choice of engine.** The risk of ReDoS is the main argument for engines with linear-time guarantees, such as RE2, and for [automaton-based search](/regex-search/) in tools such as [grep](/grep/).
- **Static analysis.** Linters and security scanners search patterns for nested or overlapping stars, which is the ambiguity criterion above.
- **Fine-grained complexity.** For patterns with backreferences no fast engine is known, and [matching with backreferences](/backreference-matching/) is NP-complete; even for true regular expressions, the [Backurs and Indyk](/backurs-indyk-regex-hardness/) results show that $O(mn)$ is close to optimal for many pattern types under a standard hypothesis.

## References
