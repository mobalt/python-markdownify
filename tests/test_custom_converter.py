from markdownify import MarkdownConverter
from bs4 import BeautifulSoup


class ImageBlockConverter(MarkdownConverter):
    """
    Create a custom MarkdownConverter that adds two newlines after an image
    """
    def convert_img(self, el, text, convert_as_inline):
        return super().convert_img(el, text, convert_as_inline) + '\n\n'


def test_img():
    # Create shorthand method for conversion
    def md(html, **options):
        return ImageBlockConverter(**options).convert(html)

    assert md('<img src="/path/to/img.jpg" alt="Alt text" title="Optional title" />') == '![Alt text](/path/to/img.jpg "Optional title")\n\n'
    assert md('<img src="/path/to/img.jpg" alt="Alt text" />') == '![Alt text](/path/to/img.jpg)\n\n'


class ColonTagConverter(MarkdownConverter):
    """
    Create a custom MarkdownConverter capable of convert a custom tag that contains a colon
    """

    def convert_ac_structured_macro(self, el, codetext, convert_as_inline):
        lang = el.find(attrs={"ac:name": "language"})
        lang = lang.get_text().strip() if lang else self.options.get("code_language")
        title = el.find(attrs={"ac:name": "title"})
        title = ("**" + title.get_text().strip() + "**\n") if title else ""
        body = el.find("ac:plain-text-body").get_text().strip()
        result = f"\n{title}```{lang}\n{body}\n```\n"
        return result


def test_tags_with_colon():
    def md(html, **options):
        return ColonTagConverter(**options).convert(html)

    assert md( """<ac:structured-macro ac:macro-id="8398ad03-beb3-4f6d-8017-396f8ffc2fea" ac:name="code" ac:schema-version="1">
 <ac:plain-text-body>
  <![CDATA[if (log.isDebugEnabled()) {
    log.debug("Hello World.");
}]]>
 </ac:plain-text-body>
</ac:structured-macro>""") == """
```
if (log.isDebugEnabled()) {
    log.debug("Hello World.");
}
```
"""

    # full example
    assert md("""<ac:structured-macro ac:macro-id="8398ad03-beb3-4f6d-8017-396f8ffc2fea" ac:name="code" ac:schema-version="1">
 <ac:structured-macro ac:macro-id="8398ad03-beb3-4f6d-8017-396f8ffc2fea" ac:name="code" ac:schema-version="1">
 <ac:parameter ac:name="language">
  java
 </ac:parameter>
 <ac:parameter ac:name="title">
  Example Code
 </ac:parameter>
 <ac:plain-text-body>
  <![CDATA[if (log.isDebugEnabled()) {
    log.debug("Hello World.");
}]]>
 </ac:plain-text-body>
</ac:structured-macro>""") == """
**Example Code**
```java
if (log.isDebugEnabled()) {
    log.debug("Hello World.");
}
```
"""


def test_soup():
    html = '<b>test</b>'
    soup = BeautifulSoup(html, 'html.parser')
    assert MarkdownConverter().convert_soup(soup) == '**test**'
