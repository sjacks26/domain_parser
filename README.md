# domain_parser

This code uses Python's urllib to identify domains in URLs.  
The user can specify one of three options for output: either just the domain for each URL, just each full URL, or both the domain and the full URL.

For most URLs, it simply identifies the domain in the URL as it appears.
Many URLs - especially those that appear in social media messages - are shortened, though. This code looks at URLs to see whether they appear to have been shortened (based on a list of URL shorteners - currently including 23 services). If a URL appears to have been shortened, this code uses urllib to follow that URL to its final page. It then retrieves the URL for that final page and identifies the corresponding domain.

Some websites disallow user-agents that are not associated with browsers. If this code attempts to follow a shortened link to a website that disallows such user-agents (which leads to a 403 HTTP code), it spoofs a user-agent to look like Mozilla and tries again.

This code checks website certificates. If it attempts to follow a shortened link to a website with an invalid certificate, it returns an error rather than ignoring the bad certificate.

Finally, this code imposes a 10 second limit on any attempt to parse an individual URL. If the script takes longer than 10 seconds on a URL, it returns a RuntimeError and moves on to the next URL.

sample_script.py demonstrates how you can use this code.
