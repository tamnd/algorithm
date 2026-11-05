---
tag: 6Y37PE
kind: concept
slug: backreference
name: Backreference
aliases:
- back-reference
- regex backreference
area: automata-and-parsing/regular-expressions
level: intro
summary: A construct that matches the same text as an earlier capture group, which takes the language beyond regular.
prereqs: [regular-expression, regular-language, myhill-nerode-theorem]
see_also: [backreference-matching, backtracking-regex-matching, extended-regular-expressions, posix-regex-semantics, submatch-extraction, regex-lookaround, redos, pumping-lemma-for-regular-languages]
sources:
  - book: isbn:9780444880710
    title: Alfred V. Aho, Algorithms for finding patterns in strings, in Jan van Leeuwen (ed.), Handbook of Theoretical Computer Science, Volume A, Elsevier and MIT Press (1990)
    locator: Chapter 5, pp. 255 to 300 (the part on regular expressions with back referencing, and the NP-completeness of their matching)
  - paper: doi:10.1142/S012905410300214X
    title: Cezar Câmpeanu, Kai Salomaa and Sheng Yu, A formal study of practical regular expressions, International Journal of Foundations of Computer Science 14(6) (2003)
    locator: pp. 1007 to 1018 (the definition of regex with backreferences and the pumping lemma for their languages)
  - url: "https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap09.html"
    title: The Open Group, POSIX.1-2024 (IEEE Std 1003.1-2024), Base Definitions, Chapter 9, Regular Expressions
    locator: Section 9.3.6, item 3 (the BRE back-reference \n), and Section 9.5.1 (BACKREF is applicable only to basic regular expressions)
  - book: isbn:9780596528126
    title: Jeffrey E. F. Friedl, Mastering Regular Expressions, third edition, O'Reilly (2006)
    locator: Chapters 1 and 2 (backreferences in practice, such as finding doubled words) and Chapter 4, The Mechanics of Expression Processing
---

A backreference is a regex construct, written `\k`, that matches exactly the string that the $k$-th capture group matched earlier in the same match. It is not part of the [regular expressions](/regular-expression/) of automata theory: with backreferences a pattern can describe languages that are not [regular](/regular-language/), such as $\{a^n b a^n : n \ge 0\}$ or the squares $\{ww\}$. Matching with backreferences is NP-complete ([matching with backreferences](/backreference-matching/)), so engines that support them use [backtracking](/backtracking-regex-matching/) and lose the linear-time guarantee of automaton-based matching.

## In plain words

A pair of parentheses in a pattern is a capture group: it remembers the piece of text that it matched. A backreference later in the pattern says "here, the same piece of text again". The pattern `(a*)b\1` means: some letters a, then b, then the same number of letters a as before.

A finite automaton cannot do this, because it has a fixed amount of memory and the remembered text can be as long as you like. So a pattern with a backreference can describe sets of strings that no ordinary regular expression describes.

The price is speed. An engine that supports backreferences must try different choices for what each group captures, and in bad cases the number of choices grows very fast with the length of the text.

## The idea

**Notation.** This site writes regular expressions with $r \mid s$ for union, $rs$ for concatenation, $r^*$ for the star, $\varepsilon$ for the empty string and $\emptyset$ for the empty language. Star binds tightest, then concatenation, then union. Program text in `code font` uses the syntax of practical engines, where `|` is union too.

**Syntax.** A regex with backreferences (often called a *regex*, as opposed to a regular expression) is built like a regular expression, with two more forms: a capture group $(r)_k$, which is a pair of parentheses with a number, and a backreference $\backslash k$. The groups are numbered $1, 2, \ldots$ in the order of their opening parentheses.

**Semantics.** A match is a run of the pattern from left to right that keeps an environment $\rho$, a partial map from group numbers to strings. Matching $(r)_k$ against a substring $u$ matches $r$ against $u$ and then sets $\rho(k) = u$. Matching $\backslash k$ consumes exactly the string $\rho(k)$. Inside a star, a group is set again in each iteration, so a later backreference sees the string of the *last* iteration that set it. A string $w$ is in the language $L(p)$ of the pattern $p$ if some run consumes all of $w$. This is the semantics of Câmpeanu, Salomaa and Yu (2003), and it agrees with the behavior of Perl-style engines on patterns where each backreference follows a group that has been set.

**What is left open by the definition.** Two details differ between engines and must be fixed before a pattern has a meaning:

- **An unset group.** In Python, Perl and PCRE, `\k` fails when group $k$ has not matched. In JavaScript (ECMA-262), it matches the empty string.
- **A reference to a later or an enclosing group.** POSIX makes `\n` invalid when fewer than $n$ groups precede it. Other engines allow some of these forms, with their own rules.

**Beyond regular.** Let $p = (a^*)_1\, b\, \backslash 1$. Then $L(p) = \{a^n b a^n : n \ge 0\}$, because group 1 takes some $a^n$, and the backreference must then match the same $a^n$. This language is not regular. *Proof.* Take $i \ne j$. The string $a^i b a^i$ is in $L(p)$ and $a^j b a^i$ is not, so $a^i$ and $a^j$ are in different classes of the Myhill-Nerode relation of $L(p)$. There are infinitely many classes, so by the [Myhill-Nerode theorem](/myhill-nerode-theorem/) $L(p)$ is not regular. $\square$ The same argument with $a^i b$ and $a^j b$ shows that the squares $\{ww : w \in \{a, b\}^*\}$, the language of $((a \mid b)^*)_1 \backslash 1$, are not regular.

**What stays true.** Each language of a regex with backreferences is decidable, and its membership problem is in NP. Câmpeanu, Salomaa and Yu (2003) prove a pumping lemma for these languages, and use it to show that some simple languages, for example $\{a^n b^n : n \ge 0\}$, have no regex with backreferences.

**Cost.** Aho (1990) shows that matching a regex with backreferences against a string is NP-complete when both are part of the input. The [matching with backreferences](/backreference-matching/) page has the reduction. No engine is known that matches all such patterns in polynomial time, and none exists unless P = NP.

## Examples

**Counting by copy.** With $p = (a^*)_1 b \backslash 1$, written `(a*)b\1`:

| string | in $L(p)$? | reason |
|---|---|---|
| `b` | yes | group 1 is empty |
| `aba` | yes | group 1 is `a` |
| `aabaaa` | no | 2 letters a before b, 3 after |
| `aaabaaa` | yes | group 1 is `aaa` |
| `abaa` | no | 1 letter a before b, 2 after |

**Squares.** The pattern `((a|b)*)\1` matches exactly the strings $ww$ with $w \in \{a, b\}^*$: it matches `abab`, `aa`, `abaaba` and the empty string, and it rejects `aba` and `abba`. Over $\{a, b\}$, the strings of length at most 8 that it matches are the 31 strings $ww$ with $|w| \le 4$, one for each $w$, since $1 + 2 + 4 + 8 + 16 = 31$.

**Last iteration wins.** In `(a|b)*\1`, group 1 is set in each iteration of the star, and the backreference repeats the letter of the last iteration. So the pattern matches `abb` (the star reads `ab`, the group holds `b`, and the backreference reads the last `b`) and `aa`. It rejects `aba`: if the star reads `ab`, the group holds `b` but the last letter is `a`; if the star reads `a`, the backreference reads `a` and the text `ba` is left over. In Python it also rejects the empty string, because the star then runs zero times and group 1 is unset. In JavaScript the same pattern accepts the empty string.

**Doubled words.** The search pattern `\b(\w+) \1\b` finds a word that is written twice, as in "it is is fine", where it matches `is is`. The pattern `<(\w+)>.*?</\1>` matches an element whose end tag has the same name as its start tag, as in `<b>bold</b>`. These are common uses in text editors and in scripts. The second one does not handle nested elements of the same name, which no regex handles in general.

**Non-example.** The pattern `(a|b)\1` looks like it needs a backreference, but its language is $\{aa, bb\}$, which is finite and so regular. A backreference to a group with a finite language can always be removed by trying each string of that language: here `aa|bb`. A backreference makes a language non-regular only when the group can capture unboundedly many different strings.

## Where it is used

- **Engines with backreferences.** Perl, PCRE, Python `re`, Java, JavaScript and .NET support `\k`, and so do POSIX basic regular expressions, the syntax of `grep` and `sed` without options. POSIX [extended regular expressions](/extended-regular-expressions/) have no backreferences in the standard, although GNU and other implementations accept them as an extension. All these engines match by [backtracking](/backtracking-regex-matching/).
- **Engines without them.** RE2, Go's `regexp` and Rust's `regex` crate reject backreferences, because they guarantee time linear in the text by an automaton ([Thompson NFA simulation](/thompson-nfa-simulation/), [Pike VM](/pike-vm/), [lazy DFA construction](/lazy-dfa-construction/)), and a backreference cannot be compiled into an automaton.
- **Complexity.** [Matching with backreferences](/backreference-matching/) is NP-complete, and a backtracking engine can take exponential time on short inputs, which is one cause of [ReDoS](/redos/).
- **Formal language theory.** Regexes with backreferences, and the closely related pattern languages of Angluin, are studied as a class between the [regular languages](/regular-language/) and the context-sensitive languages.
- **Related constructs.** [Lookaround](/regex-lookaround/) is another feature of practical engines; [submatch extraction](/submatch-extraction/) defines what a group captures, which a backreference then reuses.

## References
