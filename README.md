# MornBot

Norwegian Discord bot written for personal use. **It is not recommended that you use this code. Use at own risk**

### Prerequisites

In order to run the bot yourself you need to install the programs listed below

* Python 3.6 or newer

### Installing

Before you can run the bot you need to set up some stuff

Install the required modules

```
python -m pip install -r requirements.txt
```

Rename the [config.json.example](config.json.example) to **config.json** and fill in the following:

* token

[Click here if you don't know how to retrieve a discord bot token](https://discordpy.readthedocs.io/en/latest/discord.html).

The other fields are only required for certain commands to work. These commands will automatically be disabled if a required field is not filled in

**Do not remove the other fields from the file. Leave them as is.**

## Contributing

If you for some reason want to clean up my shitty code/contribute then these are the requirements:

* Code meets the PEP8 standard (max 120 char length)
* Use single quotes unless it's necessary to use double quotation marks
* Use double quotation marks for multi-line comments 
* Use snake_case var names
* Var names that are not exposed to the user through e.g. help messages should be in english
* Use embeds unless you have a good reason for not doing so. Default embed color should be set to `ctx.me.color`

This is not required, but preferred:
* Messages and all text exposed to the user should be in norwegian

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
