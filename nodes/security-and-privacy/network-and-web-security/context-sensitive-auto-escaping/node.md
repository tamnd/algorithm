---
tag: ZZYC2R
kind: algorithm
slug: context-sensitive-auto-escaping
name: Context-sensitive auto-escaping
aliases:
- contextual auto-sanitization
area: security-and-privacy/network-and-web-security
level: advanced
summary: "Runs an HTML parser model over the static text of a template to find the context of each hole, and inserts the escaper of that context. It rejects templates whose contexts do not agree."
model: word-ram
complexity:
  vars: {n: the size of the template (characters of static text plus nodes), d: the nesting depth of the template}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: O(d)}
properties: {deterministic: true, recursive: true, online: false}
history:
  year: 2011
  people: [Mike Samuel, Prateek Saxena, Dawn Song]
  note: "Samuel, Saxena and Song described the context inference as a type system with type qualifiers at CCS 2011, with an implementation in the Closure Templates system."
prereqs: [cross-site-scripting, deterministic-finite-automaton]
see_also: [content-security-policy, same-origin-policy, taint-analysis, type-system, parse-tree-query-validation, abstract-syntax-tree, regular-expression]
sources:
  - paper: "Mike Samuel, Prateek Saxena and Dawn Song, Context-sensitive auto-sanitization in web templating languages using type qualifiers, ACM CCS 2011, pages 587 to 600"
    locator: "the context type qualifiers, the inference of contexts over branches and loops, and the choice of a sanitizer for each context"
  - paper: "Zhendong Su and Gary Wassermann, The essence of command injection attacks in web applications, POPL 2006, pages 372 to 382"
    locator: the definition of an injection as input that changes the syntactic structure of the output (syntactic confinement)
  - url: "https://pkg.go.dev/html/template"
    title: "The Go standard library, package html/template"
    locator: "the package overview (contexts, the escapers it adds to each action, and the errors for branches and loops that end in different contexts)"
---

Context-sensitive auto-escaping makes a web template safe against [cross-site scripting](/cross-site-scripting/) without asking the author to choose an escaper for each value. The algorithm reads the static text of the template with a model of the HTML parser, as a [finite automaton](/deterministic-finite-automaton/). At each hole it knows the parser state, called the context: HTML text, a quoted attribute value, the start or the rest of a URL, script code or a script string. It puts the escaper of that context at the hole. It rejects the template when a hole is in a context with no safe escaper, or when the two branches of an IF, or a loop body, end in different contexts. Samuel, Saxena and Song (2011) wrote it as type inference with type qualifiers. The run is one pass, linear in the size of the template, and done once when the template is compiled.

## In plain words

A web page template is fixed text with holes, and each hole is filled with a value at run time. A value must be changed before it goes in, so that the browser reads it as plain data. The right change depends on where the hole is. Between tags, an angle bracket must change. Inside a link, a space and a quote must change. Inside a script string, other characters must change.

Authors often forget, or choose the wrong change. This method reads the template once, the way a browser would, and keeps track of where it is. At each hole it writes down the change for that place. If a hole is in a place where no change is safe, or if two paths through the template leave the browser in different places, it stops and reports an error before the page is ever served.

## The problem

A template $T$ is a list of nodes: TEXT$(s)$ with static text $s$ from the author, PRINT$(e)$ with a hole filled by a value $e$ at run time, IF$(b, T_1, T_2)$ and LOOP$(n, B)$. The static text is trusted and the values are not. The task is to give each PRINT node an escaper so that, for each choice of values, the parser reads each value as data inside one region (a text run, one attribute value, one string literal) and never as markup or code. In the words of Su and Wassermann (2006), the values must not change the syntactic structure of the output. A template for which no such choice exists must be rejected at compile time.

The parser model is a deterministic machine with a state for each context. The code of this page uses a toy subset of HTML: elements with quoted attributes, the URL attributes `href` and `src`, and script elements with string literals. It has no comments, character references in static text, unquoted values, CSS or event handler attributes; static text outside the subset is an error.

## The algorithm

```pseudo id=main
AUTO-ESCAPE(T, c)                       ▷ c is the context where T starts
L1  for each node t of T, in order do
L2      if t is TEXT(s) then
L3          c ← TRANSITION(c, s)          ▷ run the parser model over s
L4      else if t is PRINT(e) then
L5          if ESCAPER(c) = none then fail
L6          annotate t with ESCAPER(c)
L7          c ← AFTER-PRINT(c)            ▷ the start of a URL becomes the rest of a URL
L8      else if t is IF(b, T1, T2) then
L9          c1 ← AUTO-ESCAPE(T1, c); c2 ← AUTO-ESCAPE(T2, c)
L10         if c1 ≠ c2 then fail
L11         c ← c1
L12     else if t is LOOP(n, B) then
L13         if AUTO-ESCAPE(B, c) ≠ c then fail
L14 return c
```

The whole template starts in the context TEXT and must end in TEXT. TRANSITION is the parser model. It fails on text outside the subset. ESCAPER maps a context to an escaper:

| context | escaper | what it does |
| --- | --- | --- |
| HTML text | html | `&`, `<`, `>`, `"` and `'` become character references |
| quoted attribute value | html | the same, so the value cannot close its quote |
| start of a URL value | url-filter | keeps a relative URL or the schemes http, https and mailto; any other scheme becomes `about:invalid`; then html |
| rest of a URL value | url-encode | percent-encodes each UTF-8 byte that is not an unreserved character |
| script code | js-value | writes the value as a quoted string literal, with each character that is not a letter, a digit or a space as `\uXXXX` |
| script string | js-string | the same escapes, without the quotes |
| tag name, attribute name, event handler or style value | none | the template is rejected |

Line L7 changes the context only at the start of a URL: after a value, the parser is no longer at the start, so a second value in the same URL is encoded and not filtered. Lines L10 and L13 are the join rules. A value that is printed after an IF must have one context whatever branch ran, and a loop body must leave the context as it found it, so that each repetition sees the same context. The code returns the annotated template; rendering it calls the chosen escaper on each value.

## Example

The template below prints the value `name` five times and the value `link` once, in six contexts. The table gives the context that line L3 computes before each hole, the escaper that line L6 chooses, and the output for the benign value `O'Neil & <Co>`, which holds a quote, an ampersand and angle brackets. The value `link` is `/u`.

| static text before the hole | context | escaper | output for the hole |
| --- | --- | --- | --- |
| `<p title="` | attribute value, quote `"` | html | `O&#39;Neil &amp; &lt;Co&gt;` |
| `">Hello, ` | HTML text | html | `O&#39;Neil &amp; &lt;Co&gt;` |
| `</p><a href="` | start of a URL | url-filter | `/u` |
| `?ref=` | rest of a URL | url-encode | `O%27Neil%20%26%20%3CCo%3E` |
| `">home</a><script>var n = ` | script code | js-value | `"O\u0027Neil \u0026 \u003cCo\u003e"` |
| `; var s = 'Hi ` | script string, quote `'` | js-string | `O\u0027Neil \u0026 \u003cCo\u003e` |

The last static text `';</script>` returns the machine to HTML text, so the template is accepted. With `link` equal to `ab:c`, a scheme that is not on the list, the third hole renders `about:invalid`. One escaper for all six holes cannot work: html escaping inside the script string gives `&#39;`, which a script reads as five characters and not as a quote, and html escaping in the URL leaves the space and the `&` to end the query value.

## Correctness

The claim, for the toy machine: if AUTO-ESCAPE accepts $T$, then for each choice of values the machine reads the rendered page without failure and ends in HTML text, the output of each escaper stays inside one text run, attribute value or string literal, and each static character is read in the same context whatever the values are. The key step is a lemma for each escaper: from its context, the escaped output never takes the machine to another context, because it has no character that the machine reacts to there (no `<` in text, no quote in a value). The loop of line L1 then keeps the invariant that the context computed by the algorithm equals the real context of the machine on the rendered prefix, up to merging the start and the rest of a URL, since an empty value leaves the machine at the start. Lines L10 and L13 make this hold whatever branch runs and however often a loop repeats. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

- **Time.** Each node is visited once. Line L9 visits each branch once and line L13 each loop body once; the loop is not unrolled. TRANSITION reads each static character once with $O(1)$ work, for tag and attribute names of bounded length. So the time is $\Theta(n)$ on every template, where $n$ counts the characters of static text and the nodes. This is a compile-time cost on the word-RAM.
- **Space.** The recursion of lines L9 and L13 is $O(d)$ deep for a template of nesting depth $d$, besides the annotated copy of the template.
- **Run time.** Rendering costs what the escapers cost, linear in the length of the output. No parsing happens at run time, which is the main advantage over a run-time sanitizer.

## Properties

- **Sound for the model.** An accepted template keeps data in data regions for each value, in the sense of the theorem. The guarantee is only as good as the agreement of the parser model with the real browser parser.
- **Conservative.** Some safe templates are rejected, for example an IF whose branches end in different contexts that are never followed by a hole.
- **Deterministic and compile time.** The output depends only on the template, and the check runs once per template.
- **Static text is trusted.** The algorithm protects against values, not against the author. A template that puts a hole inside script code that the author wrote is treated as the author intends.

## Variants and improvements

- **Type qualifiers.** Samuel, Saxena and Song present the contexts as type qualifiers on the output of each template expression, and the join rules as type checking of branches and loops.
- **Run-time checks for dynamic contexts.** Where the context of a hole cannot be known at compile time, a system can track it at run time and choose the escaper then, at a run-time cost.
- **Typed values.** Go's html/template and the Closure systems let trusted code mark a value as already safe for one context, for example as HTML from a sanitizer, so the escaper keeps it as is.
- **More contexts.** Real systems model comments, CSS, unquoted attribute values, event handler attributes and the many string and regular expression states of JavaScript. The toy machine of this page rejects them.

## When to use it

Use it in a template system that produces HTML, so that escaping is the default and not a task for each author. It removes the most common causes of [cross-site scripting](/cross-site-scripting/) in server templates: a missing escaper and the wrong escaper. It does not cover values that reach the page by script at run time in the browser (DOM-based cases), nor values that the author marks as trusted. Use it together with a [content security policy](/content-security-policy/), which limits what an escaping mistake can do. For SQL, the matching check of the output structure is [parse-tree query validation](/parse-tree-query-validation/), but prepared statements are the better defense there.

## Pitfalls

- **One escaper everywhere.** Line L6 with html escaping for all contexts is wrong: a script string decodes `&#39;` as five characters, and a URL keeps the space and `&` that end a query value. The right line L6 uses ESCAPER$(c)$.
- **No join check.** Without line L10, a value after an IF gets the escaper of one branch only; when the other branch runs, the parser may be in an attribute value and the html escaper of text no longer matches. The right line L10 fails when $c_1 \ne c_2$.
- **A loop checked once.** Without line L13, the first repetition of a loop body is right and the second starts in the context the body left. Line L13 requires the body to end where it began.
- **A missing AFTER-PRINT.** Without line L7, a second value in a URL is filtered as if it were the start of a URL, and its characters are not encoded. The context must change after the first value.
- **A parser model that differs from the browser.** If TRANSITION handles a state in a different way than the browser does, the proof holds for the model and the page can still break. This is why real systems reject the cases they do not model.

## Implementations

## History

Escaping by hand, with a function call for each value, was the rule for many years, and auto-escaping first meant one HTML escaper for all values, which is wrong in scripts and URLs. Samuel, Saxena and Song (CCS 2011) gave the context-sensitive version as type inference with type qualifiers and implemented it for the Closure Templates system. Go's html/template package uses the same approach, with errors for branches and loops that end in different contexts.

## References
