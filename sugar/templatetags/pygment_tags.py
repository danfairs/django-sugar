from django import template
import re
from pygments import lexers, formatters, highlight

register = template.Library()

@register.filter(name='pygmentize')
def pygmentize(value, arg='code'):
    '''
    Finds all <code></code> blocks in a text block and replaces it with 
    pygments-highlighted html semantics. It tries to guess the format of the 
    input, and it falls back to Python highlighting if it can't decide. This 
    is useful for highlighting code snippets on a blog, for instance.

    Source:  http://www.djangosnippets.org/snippets/25/

    Example
    -------
    
    {% post.body|pygmentize %}

    '''
    bits = arg.split(':')
    if len(bits) == 1:
        regex = '<%(element)s>(.*?)</%(element)s>' % {'element': bits[0].strip()}
    else:
        element, css_class = bits
        regex = '<%(element)s\W*class=[\'|"]%(css_class)s[\'|"]\W*>(.*?)</%(element)s>' % {
            'element': element.strip(),
            'css_class': css_class.strip()
        }

    last_end = 0
    to_return = ''
    for match_obj in re.finditer(regex, value, re.DOTALL):
        code_string = match_obj.group(1)
        try:
            lexer = lexers.guess_lexer(code_string)
        except ValueError:
            lexer = lexers.PythonLexer()
        pygmented_string = highlight(code_string, lexer, formatters.HtmlFormatter())
        to_return = to_return + value[last_end:match_obj.start(1)] + pygmented_string
        last_end = match_obj.end(1)
    return to_return + value[last_end:]

