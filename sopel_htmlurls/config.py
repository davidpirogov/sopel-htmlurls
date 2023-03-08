from sopel.config.types import (
    BooleanAttribute,
    ListAttribute,
    StaticSection,
    ValidatedAttribute,
)


class HtmlUrlsConfigSection(StaticSection):
    """
    Configuration class for Sopel config file
    """

    template_file = ValidatedAttribute(
        "template_file", parse=str, default="repositories/sopel-htmlurls/sopel_htmlurls/template.html"
    )
    """
    The path to the template file used to generate the html
    """

    output_dir = ValidatedAttribute(
        "output_dir", parse=str, default="public/"
    )
    """
    The path to the output HTML file that is generated
    """

    channels = ListAttribute("channels")
    """
    The list of channels to generate a templated output for
    """

    allow_only_public_urls = BooleanAttribute("allow_only_public_urls", default=True)
    """
    Whether or not only urls that are publicly accessible are allowed
    """

    page_refresh_seconds = ValidatedAttribute(
        "page_refresh_seconds", parse=int, default=30
    )
    """
    How often should the html page refresh
    """

    max_output_urls = ValidatedAttribute(
        "max_output_urls", parse=int, default=30
    )
    """
    The maximum number of urls to render into the template
    """
