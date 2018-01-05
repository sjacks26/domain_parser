from urllib.parse import urlparse
from urllib import error, request
import signal
import ssl

link_shortener_domains = ["tiny.cc", "youtu.be", "ht.ly", "clk.gop", "eepurl.com", "dld.bz", "t.co", "bit.ly", "goo.gl",
                          "ow.ly", "tinyurl.com", "bitly.com", "ln.is", "linkis.com", "tr.im", "smarturl.it", "spr.ly",
                          "shar.es", "com.me", "trib.al", "natl.re", "fw.to", "j.mp"]


def handler(signum, frame):
    raise RuntimeError("Time's up")


def parser(link):
    """
    Function takes in a url as a string. If it succeeds in parsing a domain from the url, it returns the domain as a
    string; if not, it returns an error code or message as a string
    """
    signal.signal(signal.SIGALRM, handler)
    # Shortened urls trigger this loop, which attempts to follow shortened urls to their final destination, then parse
    # the domain based on that final destination.
    if any(l in link for l in link_shortener_domains) and not 't.com' in link:
        if not link.startswith("http"):
            link = "http://" + link
        signal.alarm(10)
        # The first try statement adds a timer, so that the script doesn't get stuck on a problematic url.
        try:
            # The try statement sends a request for each url, which allows the url to redirect as it would if
            # clicked by a user. It then finds the domain for the final url after redirection. The first except
            # statement handles 403 (permission denied) errors: it spoofs the user-agent to get past user-agent
            # restrictions. The next except statement handles any failed requests, grabbing the domain from the url as
            # it appears in the text of the message. Because of the previous if statement, only urls that seem to use a
            # link shortener service are put through this process.
            try:
                response = request.urlopen(link)
                expanded_link = response.geturl()
                domain = urlparse(expanded_link).netloc
            except error.HTTPError as e:
                # If 403 error, spoof user-agent to look like a browser
                if e.code == 403:
                    try:
                        req = request.Request(link)
                        req.add_header('User-agent', 'Mozilla/5.0')
                        response = request.urlopen(req)
                        expanded_link = response.geturl()
                        domain = urlparse(expanded_link).netloc
                    # If spoof fails, parse domain from original url
                    except:
                        domain = urlparse(link).netloc
                # If HTTPError code is anything other than 403, parse domain from original url
                else:
                    error_code = str(e.code)
                    domain = urlparse(link).netloc
            except error.URLError as e:
                error_code = str(e)
            except ssl.CertificateError as e:
                error_code = str(e)
        # If it takes longer than 10 seconds to follow a url, return RuntimeError
        except RuntimeError as e:
            error_code = e.args

    # If the link doesn't appear to be shortened, parse the domain from the link as it appears
    else:
        if not link.startswith('http'):
            link = 'http://' + link
        else:
            link = link
        domain = urlparse(link).netloc

    if 'error_code' in locals():
        return error_code
    else:
        return domain
