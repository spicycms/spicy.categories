from django import template
from django.template.defaultfilters import stringfilter
from presscenter import parsers

register = template.Library()


@register.filter
@stringfilter
def stripped_paragraphs(text):
    """
    {{ var|stripped_tag }}
    Returns a list of paragraphs with HTML stripped.
    """
    parser = parsers.StrippingParagraphHTMLParser()
    parser.feed(text)
    parser.close()
    return parser.paragraphs_gen()


class DocsNode(template.Node):
    def __init__(self, data, issue):
        self.data = template.Variable(data)
        self.issue = template.Variable(issue)

    def render(self, context):
        data = self.data.resolve(context)
        issue = self.issue.resolve(context)
        data = list(data)
        for related_issue in issue.related_issues.all():
            data.extend(
                related_issue.document_set.all().order_by('order_lv'))
        context[self.data.var] = data
        return ''


@register.tag
def extend_with_related_issues(parser, token):
    """
    {% extend_with_related_issues data issue %}
    Updates documents list with documents from related issues.
    """
    try:
        tag_name, data, issue = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, (
            "%r tag requires exactly two arguments" %
            token.contents.split()[0])

    return DocsNode(data, issue)
