# MornBot

Norwegian multi-purpose Discord bot written for personal use.

This project is no longer being actively maintained. This means that it contains a lot of poorly written code. It is not recommended that you run this bot yourself, however if you want to for some god awful reason, you can keep reading :)

It also has a lot of poorly written issues and weird commit messages but I can't be bothered to clean up the mess I've made.

### Table of Contents

* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Setup](#setup)
* [Built With](#built-with)
* [Contributing](#contributing)
* [License](#license)
* [Acknowledgments](#acknowledgments)

## Getting Started

### Prerequisites

* [Python](https://github.com/python/cpython) 3.6 or newer
* A [MongoDB](https://github.com/mongodb/mongo) database

### Setup

*Assming that you have set your Python 3 path to `python` and you have set up a database.*

* Install the required Python modules:
  ```
  python -m pip install -r requirements.txt
  ```

* Rename the [config.yaml.example](config.yaml.example) file to `config.yaml` and replace the values within it with your own.

* Run the bot
  ```
  python run.py
  ```

## Built With

* [Discord.py](https://github.com/Rapptz/discord.py)

...and all the other modules listed in the [requirements.txt](requirements.txt) file.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* [PurpleBooth](https://github.com/PurpleBooth) for creating the [README template](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2) used to write what you're looking at right now :)

and these people for their indirect contributions to the project. Their code is not necessary in order for the bot to operate however their code is used in the production version of the bot and they deserve credit nonetheless:

* [nitros12](https://github.com/nitros12) for writing the [Eval.py](cogs/Eval.py) cog - ([original code](https://gist.github.com/nitros12/2c3c265813121492655bc95aa54da6b9))
* [EvieePy](https://github.com/EvieePy) for writing a template for the [Errors.py](cogs/Errors.py) cog - ([original code](https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612))


