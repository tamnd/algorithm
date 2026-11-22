---
tag: ASHYJM
kind: definition
slug: same-origin-policy
name: Same-origin policy
aliases:
- SOP
- origin policy
area: security-and-privacy/network-and-web-security
level: intro
summary: "The browser rule that a script may read data only from pages with the same scheme, host and port as the page that loaded it."
history:
  year: 2011
  people: [Adam Barth]
  note: "Netscape browsers applied an origin check to JavaScript from the mid 1990s, and each browser grew its own version. Barth wrote the common core down as the web origin concept in RFC 6454 in 2011."
prereqs: []
see_also: [cross-site-scripting, cross-site-request-forgery, content-security-policy, context-sensitive-auto-escaping, reference-monitor, access-control-matrix, noninterference]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc6454"
    title: "Adam Barth, The Web Origin Concept, RFC 6454, December 2011"
    locator: "Section 3 (the principles of the policy), Section 4 (the origin of a URI), Section 5 (comparing origins), Section 7 (the Origin header field)"
  - url: "https://html.spec.whatwg.org/multipage/browsers.html#origin"
    title: "WHATWG, HTML Living Standard, Origin"
    locator: "the definitions of a tuple origin, an opaque origin, same origin and same site"
  - url: "https://fetch.spec.whatwg.org/#http-cors-protocol"
    title: "WHATWG, Fetch Living Standard, The CORS protocol"
    locator: the response headers by which a server lets another origin read a response
  - url: "https://www.rfc-editor.org/rfc/rfc6265"
    title: "Adam Barth, HTTP State Management Mechanism, RFC 6265, April 2011"
    locator: "Section 8 (security considerations, including the weak isolation of cookies by port and by scheme)"
---

The same-origin policy is the main isolation rule of the web browser. Each document and each resource has an origin, which for an ordinary URL is the triple of its scheme, host and port. A script that runs in a document may read the content of another document or the response to a request only when the two origins are equal. Other origins can still be linked to, embedded and sent requests, but their content cannot be read without their consent. The policy keeps a page on one site from reading the mail, the account data or the documents that the same browser shows from another site. It is the boundary that [cross-site scripting](/cross-site-scripting/) breaks from the inside, by getting code to run in the victim origin, and that [cross-site request forgery](/cross-site-request-forgery/) works around, because the policy limits reads and not requests. RFC 6454 (Barth, 2011) defines the origin and the comparison; the HTML and Fetch standards define what each browser feature allows across origins.

## Definition

**Origin.** Let $u$ be an absolute URL. If its scheme uses a host and a port, such as `http` and `https`, then the origin of $u$ is the triple

$$ \mathrm{origin}(u) = (\text{scheme}, \text{host}, \text{port}), $$

where the scheme and the host are in lower case after the standard normalization of the host, and the port is the default port of the scheme (80 for `http`, 443 for `https`) when $u$ gives none. Otherwise, for example for a `data:` URL or a document in a sandboxed frame, the origin is an opaque origin: a new identifier that is equal only to itself. An opaque origin is serialized as `null`.

**Same origin.** Two origins $o_1$ and $o_2$ are the same origin when both are triples and the three parts are equal, or when both are opaque and are the same identifier. The path, the query and the fragment of a URL play no part.

**The policy.** Let $d$ be a document and $s$ a script that runs in $d$, so that $s$ acts with $\mathrm{origin}(d)$. Then:

1. **Reads.** $s$ may read the content of a document $e$ or of the response to a request for $r$ only if $\mathrm{origin}(e) = \mathrm{origin}(d)$ or $\mathrm{origin}(r) = \mathrm{origin}(d)$, unless the other server allows it, for example with the CORS headers of the Fetch standard.
2. **Requests.** $s$ may cause the browser to send requests to any origin, for example by a link, a form or an embedded image. The response of such a request is still subject to rule 1.
3. **Embedding.** A document may embed a script, an image, a style sheet or a frame from another origin. An embedded script runs with the origin of the document that embeds it, not with the origin it came from. A framed document keeps its own origin.

The same-origin relation is an equivalence relation on origins: it is equality of triples, and each opaque origin is in a class of its own. The policy is a family of checks in the browser, one at each feature that crosses documents, and not one rule in one place.

## Examples and non-examples

The table compares each URL with `https://www.example.com/dir/page.html`, whose origin is (`https`, `www.example.com`, 443).

| URL | origin | same origin? | reason |
| --- | --- | --- | --- |
| `https://www.example.com/other/file.html` | (`https`, `www.example.com`, 443) | yes | only the path differs |
| `https://www.example.com:443/dir/page.html?q=1` | (`https`, `www.example.com`, 443) | yes | 443 is the default port; the query plays no part |
| `https://WWW.Example.COM/dir/page.html` | (`https`, `www.example.com`, 443) | yes | the host is compared in lower case |
| `http://www.example.com/dir/page.html` | (`http`, `www.example.com`, 80) | no | the scheme and the port differ |
| `https://www.example.com:8443/dir/page.html` | (`https`, `www.example.com`, 8443) | no | the port differs |
| `https://example.com/dir/page.html` | (`https`, `example.com`, 443) | no | the host differs, even though one name is inside the other |
| `https://shop.example.com/` | (`https`, `shop.example.com`, 443) | no | another host of the same site |
| `https://192.0.2.10/dir/page.html` | (`https`, `192.0.2.10`, 443) | no | an address is a different host from a name, even if the name resolves to it |
| `data:text/plain,hello` | opaque | no | a `data:` URL gets a new opaque origin |

**Non-example: cookies.** Cookies do not follow the same-origin policy. RFC 6265 scopes a cookie by a domain and a path, and a cookie set for `example.com` can be sent to `shop.example.com` and to every port of the host. A cookie without the `Secure` attribute is sent over `http` as well as `https`. This is why the cookie of one origin can reach another origin of the same site, and why the browser attaches cookies to requests that another site starts.

**Non-example: same site.** `https://www.example.com` and `https://shop.example.com` are not the same origin, but they are the same site, because they share the registrable domain `example.com`. The HTML standard defines "same site" for features such as the `SameSite` cookie attribute. Same site is a weaker relation than same origin.

**Non-example: an embedded script.** A page from `https://www.example.com` that loads a script from `https://cdn.example.net` runs that script with the origin `https://www.example.com`. The script can read the page, because it is not treated as code of its source. This is why a page must trust every script that it embeds.

## Related definitions

- **Cross-origin resource sharing.** The CORS protocol of the Fetch standard lets a server name the origins that may read its responses, with the `Access-Control-Allow-Origin` response header. It relaxes rule 1 with the consent of the server that owns the data; it does not change rules 2 and 3.
- **The Origin header.** RFC 6454 also defines the `Origin` request header, which tells a server the origin that caused a request. Servers use it as one of the defenses against [cross-site request forgery](/cross-site-request-forgery/).
- **Content security policy.** A [content security policy](/content-security-policy/) lets a page limit which sources it loads scripts from, which narrows rule 3 for that page.
- **Access control.** The policy is an [access control](/access-control-matrix/) rule whose subjects and objects are origins, and the browser acts as the [reference monitor](/reference-monitor/) that checks each access. It controls access, not information flow: it does not give [noninterference](/noninterference/), since a page can still learn, for example, whether an image of another origin loaded.

## References
