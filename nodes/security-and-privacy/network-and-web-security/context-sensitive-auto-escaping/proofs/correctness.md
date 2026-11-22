---
title: Auto-escaping keeps every value inside one data region of the toy HTML machine
proves: [correctness, complexity]
status: full
---

We use the pseudocode AUTO-ESCAPE of the page and the toy HTML machine of the page. A context $c$ is a state of the machine with its fields (tag name, attribute name, quote character). $\delta(c, x)$ is the context after the machine reads the character $x$ in context $c$, and it is undefined when the machine rejects $x$. $\delta^*(c, s)$ is the run over a string $s$. TRANSITION$(c, s)$ computes $\delta^*(c, s)$ and fails when it is undefined.

**The URL merge.** Let $\sigma(c)$ be $c$ with the two states URL-START and URL-REST replaced by one state URL, with the same fields. The machine reads a quote that closes the value in both states, and goes to URL-REST on each other character, so $\sigma(\delta(c, x))$ depends only on $\sigma(c)$ and $x$. By induction on the length of $s$, the same holds for $\delta^*$: if $\sigma(c) = \sigma(d)$, then $\delta^*(c, s)$ is defined if and only if $\delta^*(d, s)$ is defined, and then $\sigma(\delta^*(c, s)) = \sigma(\delta^*(d, s))$. We need $\sigma$ because an empty value at the start of a URL leaves the machine in URL-START, while line L7 moves the inferred context to URL-REST.

**Lemma 1 (escapers).** Let $c$ be a context with ESCAPER$(c) = E$, not none, and let $d$ be a context with $\sigma(d) = \sigma(c)$. Then for each value $v$, $\delta^*(d, E(v))$ is defined and $\sigma(\delta^*(d, E(v))) = \sigma(\textsc{After-Print}(c)) = \sigma(c)$.

*Proof.* We take the six cases of ESCAPER.

- TEXT, escaper html. The output has no `<`, since each `<` of $v$ became `&lt;`. In TEXT the machine changes state only on `<`, so it stays in TEXT.
- VALUE with quote $q$ in an attribute that is not an event handler or a style, escaper html. The output has no `"` and no `'`. In VALUE the machine changes state only on $q$, so it stays in the same VALUE context.
- URL-START or URL-REST with quote $q$, escaper url-filter or url-encode. The url-filter output is html-escaped, so it has no quote. The url-encode output has only unreserved characters and `%XX` triples, so it has no quote. In both URL states each character that is not $q$ leads to URL-REST, so $\sigma$ stays URL with the same fields.
- SCRIPT, escaper js-value. The output is `"`, then a sequence of ASCII letters, digits, spaces and escapes `\uXXXX`, then `"`. The machine goes from SCRIPT to JS-STRING on the first `"`. In JS-STRING, a letter, a digit or a space keeps the state, and a backslash goes to JS-ESCAPE, from which `u` returns to JS-STRING; the hex digits then keep JS-STRING. The last `"` returns to SCRIPT. No `<` occurs, so the machine does not fail.
- JS-STRING with quote $q$, escaper js-string. The output is the middle part of the last case, so the machine ends in the same JS-STRING context. No quote, no `<` and no line break occurs. $\square$

**Lemma 2 (the induction).** Suppose AUTO-ESCAPE$(T, c)$ returns the context $c'$ without failure. Let $d$ be a context with $\sigma(d) = \sigma(c)$, and let $\rho$ be an environment that gives a string to each hole, a truth value to each IF and a count $k \ge 0$ to each LOOP. Let $R$ be the rendering of the annotated $T$ under $\rho$. Then $\delta^*(d, R)$ is defined and $\sigma(\delta^*(d, R)) = \sigma(c')$.

*Proof.* By induction on the size of $T$, and inside one list by induction on the number of nodes done by the loop of line L1. The invariant of that loop is: after the nodes $t_1, \ldots, t_j$, the variable $c$ of the procedure and the real context $d_j = \delta^*(d, R_1 \cdots R_j)$ have $\sigma(d_j) = \sigma(c)$, where $R_i$ is the rendering of $t_i$. It holds for $j = 0$. For the node $t_{j+1}$:

- TEXT$(s)$, lines L2 and L3. TRANSITION$(c, s)$ succeeded, so by the URL merge $\delta^*(d_j, s)$ is defined and has the same $\sigma$ as the new $c$.
- PRINT$(e)$, lines L4 to L7. Line L5 did not fail, so ESCAPER$(c)$ is an escaper $E$, and line L6 makes the rendering $E(\rho(e))$. By Lemma 1 the real context after it has $\sigma$ equal to $\sigma(c)$, and line L7 keeps $\sigma(c)$.
- IF$(b, T_1, T_2)$, lines L8 to L11. The rendering is the rendering of $T_1$ or of $T_2$, as $\rho(b)$ says. Both are smaller than $T$, and both calls of line L9 returned, with $c_1 = c_2$ by line L10. By the induction hypothesis the real context after the chosen branch has $\sigma$ equal to $\sigma(c_1)$, and line L11 sets $c$ to $c_1$.
- LOOP$(n, B)$, lines L12 and L13. The rendering is $k$ copies of the rendering of $B$, where $k = \rho(n)$. Line L13 says that AUTO-ESCAPE$(B, c)$ returns $c$. By the induction hypothesis on $B$, applied $k$ times, each copy starts and ends in a real context with $\sigma$ equal to $\sigma(c)$, and $c$ does not change.

At line L14 the procedure returns $c$, and the invariant for the whole list is the claim. $\square$

**Theorem.** If AUTO-ESCAPE of the page accepts the template $T$ (it returns TEXT from the start context TEXT), then for each environment $\rho$:

1. the machine reads the rendering of $T$ from TEXT without failure and ends in TEXT;
2. the escaped output of each hole is read inside one data region: a text run, one quoted attribute value or one string literal of a script, and never in a tag, an attribute name or script code (except the two quotes that js-value adds);
3. each static character of $T$ is read in a context whose $\sigma$ does not depend on $\rho$.

*Proof.* Part 1 is Lemma 2 with $c = d = $ TEXT, since $\sigma$ is the identity on TEXT. For part 3, the proof of Lemma 2 shows that each static string $s$ is read from a real context with the same $\sigma$ as the inferred context, and the inferred context is computed from $T$ alone. For part 2, the proof of Lemma 1 shows the states that each escaped output passes through: TEXT, one VALUE context, the URL states of one value, or the JS-STRING and JS-ESCAPE states of one literal. $\square$

Part 3 is the property "data stays data": the static characters that open and close tags, attributes and scripts are the same for every value, so a value cannot add or remove a token. Inside its region each value decodes back to itself: html-unescaping inverts html escaping because `&` is replaced first, percent-decoding inverts percent-encoding byte by byte, and the `\uXXXX` escapes give back the UTF-16 code units of the value. At the start of a URL the value decodes to its filtered form. The test checks parts 2 and 3 and the decoding with an independent parser on random templates.

**Limits.** The theorem is about the toy machine. A browser parser has many more states (character references, comments, raw text elements, unquoted values, CSS, event handler attributes), and the claim holds for a real browser only as far as the machine of the code agrees with it. The URL filter checks the value, not the URL that the static text after the hole completes.

**Cost.** Each node of $T$ is visited once: line L9 visits each branch once and line L13 visits each loop body once. TRANSITION reads each character of static text once, with $O(1)$ work when tag and attribute names have bounded length, and the comparisons of lines L10 and L13 compare contexts with a bounded number of fields. So AUTO-ESCAPE runs in $\Theta(n)$ time for a template of size $n$ (characters of static text plus nodes), with $O(d)$ extra space for a nesting depth $d$ besides the annotated copy. $\blacksquare$
