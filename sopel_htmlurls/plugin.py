from pathlib import Path
from typing import Union
from urllib.parse import quote_plus

from jinja2 import Environment, FileSystemLoader
from sopel import plugin, tools
from sopel.bot import SopelWrapper
from sopel.config import Config
from sopel.trigger import Trigger

from .config import HtmlUrlsConfigSection
from .urls import is_url_valid

log = tools.get_logger("htmlurls")


# --- Sopel Setup Section ---


def configure(config: Config):
    config.define_section("htmlurls", HtmlUrlsConfigSection)
    if config is None or config.htmlurls is None:
        raise ValueError(
            "Bot config or HtmlUrls config has not been configured. Ensure the bot is "
            "configured properly with the [htmlurls] config section."
        )

    config.htmlurls.configure_setting(
        "template_file",
        "What is the path to the template file?",
        default="template.html",
    )  # type: ignore

    config.htmlurls.configure_setting(
        "output_file", "What is the path to the output file?", default="public.html"
    )  # type: ignore

    config.htmlurls.configure_setting(
        "allow_only_public_urls",
        "Allow only publicly accessible urls?",
        default=True,
    )  # type: ignore

    config.htmlurls.configure_setting(
        "page_refresh_seconds",
        "How often, in seconds, should the html page refresh?",
        default=30,
    )  # type: ignore

    config.htmlurls.configure_setting(
        "max_output_urls",
        "How many historical urls should each channel's page store?",
        default=45,
    )  # type: ignore

    config.htmlurls.configure_setting(
        "channels",
        "Please list the channels that the bot will watch for?",
    )  # type: ignore

def setup(bot: SopelWrapper) -> None:
    """
    Ensures that our set up configuration items are present
    """

    # Ensure configuration exists
    bot.config.define_section("htmlurls", HtmlUrlsConfigSection)

    # Load our OWM API into bot memory
    if "htmlurls" not in bot.memory:
        bot.memory["htmlurls"] = tools.SopelMemory()
        bot.memory["htmlurls"]["template_file"] = bot.config.htmlurls.template_file
        bot.memory["htmlurls"]["output_dir"] = bot.config.htmlurls.output_dir
        bot.memory["htmlurls"]["channels"] = bot.config.htmlurls.channels
        bot.memory["htmlurls"][
            "page_refresh_seconds"
        ] = bot.config.htmlurls.page_refresh_seconds
        bot.memory["htmlurls"]["max_output_urls"] = bot.config.htmlurls.max_output_urls
        bot.memory["htmlurls"][
            "allow_only_public_urls"
        ] = bot.config.htmlurls.allow_only_public_urls

        # Generate the holding context for each channel
        bot.memory["htmlurls"]["context"] = {}
        for channel in bot.memory["htmlurls"]["channels"]:
            bot.memory["htmlurls"]["context"][channel] = {
                "output_file": Path(
                    bot.memory["htmlurls"]["output_dir"], f"{channel}.html"
                ),
                "history": [],
            }

            if not bot.memory["htmlurls"]["context"][channel][
                "output_file"
            ].parent.exists():
                log.info(
                    "Output file does not exist, attempting to create %s",
                    bot.memory["htmlurls"]["context"][channel][
                        "output_file"
                    ].parent.absolute(),
                )
                bot.memory["htmlurls"]["context"][channel]["output_file"].parent.mkdir(
                    exist_ok=True
                )

        # Load the template into our memory
        template_path = Path(bot.memory["htmlurls"]["template_file"])
        bot.memory["htmlurls"]["template_environment"] = Environment(
            loader=FileSystemLoader(template_path.parent.absolute())
        )

        # Add filters that the template can use
        bot.memory["htmlurls"]["template_environment"].filters[
            "quote_plus"
        ] = lambda u: quote_plus(u)
        bot.memory["htmlurls"]["template_environment"].filters[
            "datetime"
        ] = lambda dt, fmt: dt.strftime(fmt)

        # Attempt to load the template file
        log.info(
            "Attempting to load template file from '%s' (template name: '%s')",
            template_path.absolute(),
            template_path.name,
        )
        bot.memory["htmlurls"]["template"] = bot.memory["htmlurls"][
            "template_environment"
        ].get_template(template_path.name)

    log.debug("Configured HtmlUrls bot with settings:")
    for s_key in bot.memory["htmlurls"]:
        log.debug("\t %s: %s", s_key, bot.memory["htmlurls"][s_key])


def shutdown(bot: SopelWrapper) -> None:
    del bot.memory["htmlurls"]


# --- End Sopel Setup Section ---


# --- Sopel Runtime Section ---


@plugin.rule(r".*")
def handle_message(bot: SopelWrapper, trigger: Trigger) -> Union[None, int]:
    """
    Handles a message based on configured channels and rules
    """

    message_type = trigger.event
    if message_type not in ["PRIVMSG"]:
        return None

    channel = trigger.sender
    if channel not in bot.memory["htmlurls"]["channels"]:
        return None

    context = bot.memory["htmlurls"]["context"][channel]

    # Validate the urls and append to our context
    urls = list(trigger.urls)
    for u in urls:
        if is_url_valid(
            u, allow_public_only=bot.memory["htmlurls"]["allow_only_public_urls"]
        ):
            context["history"].append(
                {"time": trigger.time, "nick": trigger.nick, "url": u}
            )

    # Only keep the last max_output_urls entries in the list
    if len(context["history"]) > bot.memory["htmlurls"]["max_output_urls"]:
        context["history"] = context["history"][
            -bot.memory["htmlurls"]["max_output_urls"] :
        ]

    # Generate the output template file with the updated context
    with open(context["output_file"], mode="w", encoding="utf8") as fh:
        fh.write(
            bot.memory["htmlurls"]["template"].render(
                page_refresh_seconds=bot.memory["htmlurls"]["page_refresh_seconds"],
                history=context["history"],
            )
        )


# --- End Sopel Runtime Section ---
