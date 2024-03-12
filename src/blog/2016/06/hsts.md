---
title: How to enable HSTS in almost every PHP hosting
tags: web
date: 2016-06-13
---

[HTTP Strict Transport Security](https://de.wikipedia.org/wiki/HTTP_Strict_Transport_Security) (or HSTS for short) basically forces users to access your website with HTTPS.

It is much more than a `.htaccess` rewrite rule! If a client connects to your site, a HTTP header
tells your browser to always access your website with HTTPS for a specified amount of time. The browser vendors do also keep a list of all HSTS sites (Wikipedia for example) to prevent man-in-the-middle attacks.

But this tip is not about the technical details for HSTS - there are better articles around and more qualified people who write about this topic. I want to show you how to enable HSTS on one of the 90% of the "standard" PHP-Hosters.

## Before you start

Make sure you have a valid SSL certificate. Cool hosters like [Cyon](https://cyon.ch) offer you free [Let's Encrypt](https://letsencrypt.org/) certificates.

## The configuration

We have to do two things:

1. Redirect all HTTP traffic to HTTPS
2. Set the `Strict-Transport-Security` header

Both can be done within the `.htaccess` file. If you are not familiar with this, checkout [this htaccess tutorial](http://code.tutsplus.com/tutorials/the-ultimate-guide-to-htaccess-files--net-4757).

You can add the following two lines on top of your `.htaccess`:

```text
# Redirect to HTTPS
RewriteCond %{HTTPS} off
RewriteRule .* https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# HSTS Header - only when using https
Header set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" env=HTTPS
```

Note that you might want to modify the Strict-Transport-Security header value a bit - this configuration however is great if you want to add your site into the browsers (I'm getting to this in the next section).

That should be it - after uploading your changes you can test them with curl:

```bash
$ curl -I http://www.raphael.li
HTTP/1.1 301 Moved Permanently
Date: Mon, 13 Jun 2016 17:27:19 GMT
Accept-Ranges: bytes
Location: https://raphael.li/             <--- HTTPS!
Connection: Keep-Alive

$ curl -I https://www.raphael.li
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 3152
Date: Mon, 13 Jun 2016 17:28:04 GMT
Accept-Ranges: bytes
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Connection: close
```

## Add your site into the browsers

**WARNING**: Do not put your domain into a preload list unless you are sure that you can support HTTPS for your site _and all its subdomains_ the long term!

Please read [the removal section of chromes HSTS preload list](https://hstspreload.appspot.com/#removal) before you do this!

If you still want to do this after reading all these warnings, then you can apply for chromes HSTS preload list. That's very easy with [their registration form](https://hstspreload.appspot.com/).

You can enter your domain and check the status. If you haven't configured HSTS yet the way they
want it you will get a warning. If everything is green - you are ready go!

## Wrapping up

It's pretty easy to add support for HSTS to you site. You might think that adding strict transport
security to a personal website is a bit of a overkill - but in my opinion, it's my small contribution towards a more secure internet!
