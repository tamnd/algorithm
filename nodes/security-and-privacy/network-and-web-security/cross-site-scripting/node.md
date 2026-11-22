---
tag: 7KW88Y
kind: concept
slug: cross-site-scripting
name: Cross-site scripting
aliases:
- XSS
area: security-and-privacy/network-and-web-security
level: intro
summary: "An attack that gets a site to serve attacker script to other users, where it runs with the site's origin and rights."
history:
  year: 2000
  people: [Amit Klein]
  note: "CERT advisory CA-2000-02 of February 2000 described the class, and the name cross-site scripting came into use the same year. Klein described the DOM-based kind in 2005."
prereqs: [same-origin-policy]
see_also: [context-sensitive-auto-escaping, content-security-policy, cross-site-request-forgery, sql-injection, parse-tree-query-validation, taint-analysis]
sources:
  - url: "https://www-uxsup.csx.cam.ac.uk/pub/webmirrors/www.cert.org/advisories/CA-2000-02.html"
    title: "CERT Coordination Center, Advisory CA-2000-02, Malicious HTML tags embedded in client web requests, 2 February 2000"
    locator: "the description of the problem, its impact, and the solutions for web site operators (encoding of output and filtering of input)"
  - paper: "Amit Klein, DOM based cross site scripting or XSS of the third kind, Web Application Security Consortium, 2005"
    locator: "the third kind, in which the page's own script writes data from the URL into the document"
  - paper: "Mike Samuel, Prateek Saxena and Dawn Song, Context-sensitive auto-sanitization in web templating languages using type qualifiers, ACM CCS 2011, pages 587 to 600"
    locator: the contexts of a web page and the choice of a sanitizer for each one
  - paper: "Zhendong Su and Gary Wassermann, The essence of command injection attacks in web applications, ACM POPL 2006, pages 372 to 382"
    locator: the definition of an injection as input that is not syntactically confined
  - url: "https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html"
    title: "OWASP, Cross Site Scripting Prevention Cheat Sheet"
    locator: "output encoding for each context, HTML sanitization, and the safe sinks of the DOM"
---

Cross-site scripting (XSS) is a class of attack in which a web site puts data from an untrusted source into a page in a way that lets the browser read the data as markup or script. The script then runs in the victim's browser with the [origin](/same-origin-policy/) of the site, so it can read the page, act as the user and send the data away. The same-origin policy cannot help, because from the browser's point of view the code came from the site itself. The cause is the same as for [SQL injection](/sql-injection/): a document of one language is built by pasting strings, and the data is not kept apart from the code. The main defense is to encode each value for the exact context of the page where it goes, which [context-sensitive auto-escaping](/context-sensitive-auto-escaping/) does in the template system. A [content security policy](/content-security-policy/) adds a second layer that limits the scripts a page can run. This page describes the class and its defenses; it gives no attack strings.

## In plain words

A web page is a text that the browser reads as instructions: this is a heading, this is a link, this is a program to run. When a site builds a page, it often puts in text that came from someone else, such as a name, a comment or a search word.

If the site copies that text into the page as it is, the browser can read part of it as instructions instead of as text. Then a stranger can make the site's page do things the site never meant, inside the browsers of other users, with the rights of the site. The fix is to convert each piece of outside text so that the browser can only read it as text, in the way that fits the place where it goes in the page.

## The idea

**The trust boundary.** The browser decides what a script may do from the origin of the document it runs in. A script that a site serves is trusted with all the data of that origin. So the question for a site is not only "is this script safe?" but "can any part of this page be read as script that the site did not write?"

**Why it happens.** An HTML page mixes several languages: the markup itself, attribute values, URLs, style sheets and JavaScript. Each has its own special characters and its own rules for where a value ends. A value that is safe in one place is not safe in another. Text that a server pastes into a page without the right encoding can end the current context, for example close an attribute or a string, and start a new one. In the terms of Su and Wassermann (2006), the input is not syntactically confined: it does not stay inside one leaf of the parse of the page.

**The three kinds.**

| kind | where the data comes from | where it goes into the page |
| --- | --- | --- |
| stored (persistent) | data saved on the server, such as a comment or a profile field | into pages that the server later sends to other users |
| reflected | a part of the current request, such as a query parameter | into the response to that request |
| DOM-based | a part of the URL or another value that the browser holds | into the document, by the page's own script, without the server seeing it |

The first two are server-side flaws. The DOM-based kind, named by Klein (2005), is a flaw in the client code: the page's own script writes a value into a sink such as an HTML insertion function.

**The defenses**, from the most to the least important:

1. **Contextual output encoding.** Encode each value for its context: HTML entities in text and quoted attributes, percent-encoding in URL parts, string escapes in JavaScript strings, and nothing at all in a place where no safe encoding exists, such as a raw script body or an event handler name. Template systems with [context-sensitive auto-escaping](/context-sensitive-auto-escaping/) choose the encoder from a parse of the template, so the developer cannot pick the wrong one.
2. **Sanitization of rich text.** When users may post formatted text, parse it with an HTML parser and keep only an allowlist of elements and attributes. Removing bad patterns from a string with regular expressions does not work, because the browser parses more forms than the filter knows.
3. **Safe DOM sinks.** In client code, set text with text properties instead of HTML insertion. The Trusted Types feature of browsers makes the dangerous sinks accept only values that passed a policy.
4. **Defense in depth.** A [content security policy](/content-security-policy/) with nonces blocks scripts that the server did not mark. The `HttpOnly` cookie attribute keeps scripts from reading the session cookie, which limits one result of an attack but not the attack itself.

Input validation, such as checking that a name has no angle brackets, helps but is not a defense on its own. The same value can be safe as input and unsafe in a context that the validator did not think of.

**Detection.** Static [taint analysis](/taint-analysis/) tracks values from sources such as request parameters to sinks such as page output, and reports a path that has no encoder on it. Most tools track explicit flows only.

## Examples

**One value in four contexts.** The value is the benign string `Tom & Jerry <TJ>`. A correct encoder must turn its special characters into a form that the context reads as plain text.

| context in the page | correct output for the value | what goes wrong without encoding |
| --- | --- | --- |
| text of an element | `Tom &amp; Jerry &lt;TJ&gt;` | the browser reads `<TJ>` as the start tag of an unknown element, so the page shows "Tom & Jerry " and the structure of the page changes |
| quoted attribute value | `Tom &amp; Jerry &lt;TJ&gt;` (and `"` as `&quot;`) | a quote character in a value would end the attribute early |
| query part of a URL | `Tom%20%26%20Jerry%20%3CTJ%3E` | the `&` starts a new query parameter, so the server receives `Tom ` and a parameter named ` Jerry <TJ>` |
| JavaScript string | each of `&`, `<` and `>` as a numeric string escape | the `<` can end the script element early in some positions |

The value is harmless here, but the table shows the mechanism: without the right encoder, data changes the syntax of the page. In each case the fix is to encode the value, not to change the value.

**A quote in an attribute.** The benign name `O'Neil` goes into an attribute written with single quotes. Without encoding, the attribute ends after `O`, and the rest of the name is parsed as more of the tag. With HTML encoding, the quote becomes `&#39;` and the attribute holds the full name.

**The wrong encoder.** HTML-encoding a value that goes into a URL attribute is not enough. The value `Tom & Jerry` becomes `Tom &amp; Jerry`, which the browser decodes back to `Tom & Jerry` before it reads the URL, so the `&` still splits the query. A URL value needs percent-encoding first, and a URL from outside also needs a check of its scheme. The test of [context-sensitive auto-escaping](/context-sensitive-auto-escaping/) checks this with benign strings.

## Where it is used

- **Web template systems.** Go's `html/template`, Google Closure Templates and other systems escape by context by default, which removes most of the server-side class.
- **Browser features.** Content security policy, Trusted Types and the `HttpOnly` and `SameSite` cookie attributes exist largely because of this class.
- **Threat models and reviews.** XSS is one of the classes that a review of a web application checks for. The OWASP Top 10 counts it under injection in its 2021 list.
- **Research on injection.** The definition of Su and Wassermann covers XSS, [SQL injection](/sql-injection/) and other command injections in one model, and the same idea drives [parse tree validation](/parse-tree-query-validation/) of queries.
- **Related attacks.** [Cross-site request forgery](/cross-site-request-forgery/) needs no script in the target site; it only makes the browser send a request. An XSS flaw defeats most CSRF defenses, since a script in the origin can read the token.

## References
