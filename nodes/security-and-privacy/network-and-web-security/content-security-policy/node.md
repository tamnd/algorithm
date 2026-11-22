---
tag: KC43J3
kind: technique
slug: content-security-policy
name: Content security policy
aliases:
- CSP header
area: security-and-privacy/network-and-web-security
level: core
summary: "A header that tells the browser which sources of script, style and other content a page may load, to limit cross-site scripting."
history:
  year: 2010
  people: [Sid Stamm, Brandon Sterne, Gervase Markham, Lukas Weichselbaum, Michele Spagnuolo, Sebastian Lekies, Artur Janc]
  note: "Stamm, Sterne and Markham proposed content security policy at Mozilla in 2010. Weichselbaum, Spagnuolo, Lekies and Janc showed in 2016 that most host allowlists can be bypassed and proposed nonce policies with strict-dynamic."
prereqs: [same-origin-policy, cross-site-scripting]
see_also: [context-sensitive-auto-escaping, cryptographic-hash-function, pseudorandom-number-generator, cross-site-request-forgery, reference-monitor, inline-reference-monitor]
sources:
  - paper: "Sid Stamm, Brandon Sterne and Gervase Markham, Reining in the web with content security policy, WWW 2010, pages 921 to 930"
    locator: "the design of the policy header, the directives for each type of content, and the violation reports"
  - paper: "Lukas Weichselbaum, Michele Spagnuolo, Sebastian Lekies and Artur Janc, CSP is dead, long live CSP! On the insecurity of whitelists and the future of content security policy, ACM CCS 2016, pages 1376 to 1387, doi:10.1145/2976749.2978363"
    locator: "the measurement of 26,011 distinct policies, the bypasses of host allowlists, and the nonce policy with strict-dynamic"
  - url: "https://www.w3.org/TR/CSP3/"
    title: "W3C, Content Security Policy Level 3"
    locator: "the script-src directive, nonce and hash source expressions, strict-dynamic, the report-only header, violation reports and frame-ancestors"
---

A content security policy (CSP) is a response header by which a site tells the browser which content a page may load and run. Its main use is to limit the damage of [cross-site scripting](/cross-site-scripting/): even if an attacker gets markup into the page, the browser runs only the scripts that the policy allows. A policy is a list of directives, such as `script-src` for scripts, `object-src` for plugins, `base-uri` for the base URL and `frame-ancestors` for the pages that may frame this one. Each directive gives sources: hosts, a nonce that the server puts on each script it trusts, or the hash of a script's text. Stamm, Sterne and Markham (2010) proposed CSP with host allowlists. Weichselbaum et al. (2016) measured 26,011 distinct policies on the web and found that 94.72 percent of them could be bypassed, mostly because the allowed hosts served scripts that an attacker could reuse. They proposed the strict policy: a fresh nonce on each response with the keyword `strict-dynamic`, so that trust follows the scripts the server marked and not their hosts. CSP is a second layer of defense, after correct output encoding, not a replacement for it. It narrows the [same-origin policy](/same-origin-policy/) rule that a page may embed scripts from anywhere.

## In plain words

A web page can load scripts from many places, and the browser runs each one with the full rights of the site. If an attacker manages to add a script to the page, the browser runs it too.

With a content security policy, the site sends a short list of rules with the page: "run only scripts that carry this secret mark", or "load images only from my own site". The server puts a new random mark on each script it wrote, every time it sends the page. A script that an attacker added does not have the mark, because the attacker cannot see it in advance, so the browser refuses to run it. The browser can also send a report when it blocks something, so the site learns about the problem.

## When it applies

- The site serves HTML pages and wants a second layer of defense against cross-site scripting, after [context-sensitive auto-escaping](/context-sensitive-auto-escaping/) or correct encoding.
- The server can generate each response, so it can put a fresh nonce in the header and on each script element. For static pages, hashes of the inline scripts do the same job.
- The scripts of the page do not depend on inline event handlers or on `eval` of strings, or the site can refactor them. A strict policy blocks both.
- The site wants to control which pages can frame it, with `frame-ancestors`, as a defense against clickjacking.

It does not apply as a fix for an injection flaw itself, as a defense against [cross-site request forgery](/cross-site-request-forgery/), or as a way to stop data that a running script already has from leaving the page in every way.

## The template

The server marks each script it trusts with a fresh nonce, and the browser checks each script before it runs it. The browser part is a simplified form of the checks of CSP Level 3 for `script-src`.

```pseudo id=main
SERVE(page)
L1  n ← a fresh random value of at least 128 bits, new for this response
L2  for each script element s that the server wrote do set s.nonce ← n
L3  send the header  script-src 'nonce-n' 'strict-dynamic'; object-src 'none'; base-uri 'none'

SCRIPT-ALLOWED(s, policy)            ▷ in the browser, before s runs
L4  if s.nonce is in the nonces of policy then return allow
L5  if s is inline and hash(text of s) is in the hashes of policy then return allow
L6  if policy has 'strict-dynamic' and s was created by an allowed script, not by the parser, then return allow
L7  if policy has 'strict-dynamic' then return deny     ▷ host lists and 'unsafe-inline' are ignored
L8  if s.src matches a host source of policy then return allow
L9  return deny, and send a violation report if policy names a report endpoint
```

With the header `Content-Security-Policy-Report-Only`, the browser sends the report of line L9 but runs the script anyway, which lets a site test a policy before it enforces it. The nonce of line L1 must come from a cryptographically strong [random generator](/pseudorandom-number-generator/), and the hash of line L5 is a [cryptographic hash](/cryptographic-hash-function/) such as SHA-256 of the exact script text. When a policy has a nonce or a hash, a browser that supports them ignores `'unsafe-inline'`; old browsers that do not support them still honor it, so a policy can list it as a fallback.

**Why it works.** Markup that an attacker adds to a page arrives with the response, so the attacker would have to know the nonce of that response in advance. If the nonce is fresh, unpredictable and only in the header and the server's own script elements, the added script fails lines L4 and L5. Line L6 lets the trusted scripts load others, which keeps the policy usable on large applications. This argument assumes the nonce does not leak, that the server marks only scripts it wrote, and that no trusted script copies attacker data into a new script.

## Classic examples

- **A nonce policy for a server-side application.** This is the template above. Weichselbaum et al. (2016) report that such policies avoid the host allowlist bypasses they found. The application still needs [context-sensitive auto-escaping](/context-sensitive-auto-escaping/), because CSP does not stop injected markup that is not a script.
- **A hash policy for a static page.** The build step computes the [cryptographic hash](/cryptographic-hash-function/) of each inline script and lists the values in `script-src`. The page needs no server code, but any change to a script needs a new hash.
- **Framing control.** `frame-ancestors 'self'` lets only pages of the same [origin](/same-origin-policy/) frame the page. It replaces the older `X-Frame-Options` header and blocks pages that hide the site under a decoy to collect clicks.
- **Plugin and base controls.** `object-src 'none'` blocks plugin content, and `base-uri 'none'` stops added markup from changing the base URL that relative script paths use. Both close gaps that a script policy alone leaves open.
- **Reporting during rollout.** A site first sends the policy as report-only, collects the violation reports, fixes the inline handlers and scripts they show, and then enforces it.

## Variations

- **Host allowlists.** The original design of Stamm et al. lists hosts, such as `script-src 'self' https://cdn.example.com`. It is simple, but an allowed host that serves user content, open redirects or JSONP endpoints lets an attacker load a script from it, which is the main finding of Weichselbaum et al.
- **Hashes instead of nonces.** Hashes suit pages that do not change per response. With `strict-dynamic`, a hashed loader script can then load the rest.
- **Trusted Types.** The directive `require-trusted-types-for 'script'` makes the DOM sinks that parse HTML or script accept only values made by a named policy, which targets DOM-based cross-site scripting.
- **Other directives.** `style-src`, `img-src`, `connect-src` and `form-action` restrict other types of content. They reduce some leaks, but a policy that limits scripts gives most of the benefit.

## Pitfalls

- **A fixed nonce.** If line L1 reuses one value for all responses, or a cache serves the same page to many users, an attacker can read the nonce once and use it. Line L1 must make a new unpredictable value for each response that is sent.
- **Marking every script.** If line L2 marks all script elements in the final page, including those that came from user data, the nonce gives no protection. Only the scripts in the server's own template may get the nonce.
- **`'unsafe-inline'` with no nonce or hash.** A policy whose `script-src` allows `'unsafe-inline'` without a nonce or a hash lets every inline script run without the checks of lines L4 and L5. Weichselbaum et al. found many such policies.
- **Host lists that are too wide.** If line L8 allows a whole content network or a host with user uploads, an attacker can serve a script from it. Use nonces and `strict-dynamic` instead of host lists.
- **Report-only forever.** A policy sent only as report-only does not block anything. Enforce it after the reports are clean.
- **Missing `object-src` and `base-uri`.** A script policy without them can be bypassed by a plugin element or by a new base URL. Add both with `'none'`.

## Exercises

1. A site sends `script-src 'nonce-abc' 'unsafe-inline'`. Which scripts run in a browser that supports nonces, and which in an old browser that does not? *Answer:* in the new browser only the scripts with the nonce, because a nonce makes it ignore `'unsafe-inline'`; in the old browser every inline script.
2. Why does `strict-dynamic` drop host allowlists at line L7? *Answer:* the trust comes from the nonce or hash of a loader script, and a host list would bring back the bypasses through allowed hosts. Without the drop, the strict policy would be no stronger than its host list.
3. A page is cached by a shared proxy for ten minutes, with its nonce. What does an attacker who can add markup to the page learn, and how should the site fix it? *Answer:* the attacker can load the cached page, read the nonce and use it in added markup while the cache lasts. The site must not cache pages with nonces in a shared cache, or must use hashes.
4. Give a case where a nonce policy does not stop the effect of an injection. *Answer:* added markup that is not a script, for example a form whose action points to another site, or a trusted script that reads a value from the page and passes it to a script sink.

## References
