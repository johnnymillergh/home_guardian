![Home Guardian Social Image](https://raw.githubusercontent.com/johnnymillergh/MaterialLibrary/master/home_guardian/home_guardian_social_image_dark_theme.png)
[![GitHub release](https://img.shields.io/github/release/johnnymillergh/home_guardian.svg)](https://github.com/johnnymillergh/home_guardian/releases)
[![Github Actions workflow status](https://github.com/johnnymillergh/home_guardian/actions/workflows/build-and-test.yml/badge.svg?branch=main)](https://github.com/johnnymillergh/home_guardian/actions)
[![GitHub issues](https://img.shields.io/github/issues/johnnymillergh/home_guardian)](https://github.com/johnnymillergh/home_guardian/issues)
[![GitHub forks](https://img.shields.io/github/forks/johnnymillergh/home_guardian)](https://github.com/johnnymillergh/home_guardian/network)
[![GitHub stars](https://img.shields.io/github/stars/johnnymillergh/home_guardian)](https://github.com/johnnymillergh/home_guardian)
[![GitHub license](https://img.shields.io/github/license/johnnymillergh/home_guardian)](https://github.com/johnnymillergh/home_guardian/blob/master/LICENSE)
[![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/johnnymillergh/home_guardian.svg?style=popout)](https://github.com/johnnymillergh/home_guardian)
[![GitHub repo size](https://img.shields.io/github/repo-size/johnnymillergh/home_guardian.svg)](https://github.com/johnnymillergh/home_guardian)
[![Twitter](https://img.shields.io/twitter/url/https/github.com/johnnymillergh/home_guardian?style=social)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2Fjohnnymillergh%2Fhome_guardian)

# home_guardian

**Home Guardian**, a smart intruder inspection system, ran on Python 3, Raspberry Pi.

## Features

Here are the highlights of **home_guardian**:

1. Inherited from modern and the latest newest Python technologies:

   `Python` - [![Python](https://img.shields.io/badge/Python-v3.10.0-blue)](https://www.python.org/downloads/release/python-3100/)
   `OpenCV` - [![OpenCV](https://img.shields.io/badge/OpenCV-v4.5.4.58-red)](https://pypi.org/project/opencv-python/4.5.4.58/)
   
2. Sending Email via [Tom](https://mail.tom.com/) Email Service, email template engine powered by [Jinjia2](https://jinja2docs.readthedocs.io/en/stable/)

2. Data persistence with [peewee](http://docs.peewee-orm.com/en/latest/), [SQLite3](https://sqlite.org/index.html) as local database

2. Environment variable and configuration with [pyhocon](https://pythonhosted.org/pyhocon/_modules/pyhocon.html). Read `${ENVIRONMENT_VARIABLE}` when startup

3. Testing with [pytest](https://docs.pytest.org/en/latest/)

4. Formatting with [black](https://github.com/psf/black)

5. Import sorting with [isort](https://github.com/timothycrosley/isort)

6. Static typing with [mypy](http://mypy-lang.org/)

7. Linting with [flake8](http://flake8.pycqa.org/en/latest/)

8. Git hooks that run all the above with [pre-commit](https://pre-commit.com/)

9. Deployment ready with [Docker](https://docker.com/)

10. Continuous Integration with [GitHub Actions](https://github.com/features/actions)

11. Universal logging configuration based on [Loguru](https://github.com/Delgan/loguru/releases/tag/0.5.3). Log sample is like,

    ```
    2021-11-09 10:57:55.362 | WARNING  | MainThread      | home_guardian.configuration.loguru_configuration:configure:61 - Loguru logging configured
    2021-11-09 10:57:55.367 | WARNING  | MainThread      | home_guardian.configuration.thread_pool_configuration:configure:18 - Thread pool executor with 8 workers, executor: <concurrent.futures.thread.ThreadPoolExecutor object at 0x10ad487c0>
    2021-11-09 10:57:55.603 | INFO     | MainThread      | home_guardian.repository.model.base.model:<module>:7 - SQLite database path: /Users/johnny/Projects/PyCharmProjects/home_guardian/home_guardian/_data/home_guardian.db
    2021-11-09 10:57:55.603 | WARNING  | MainThread      | home_guardian.repository.model.base.model:<module>:9 - Initialized db file: <peewee.SqliteDatabase object at 0x10ad48fa0>
    ```

## Usage

1. Clone or download this project.

   ```shell
   $ git clone https://github.com/johnnymillergh/python_boilerplater.git
   ```

2. Build with newest PyCharm.

3. Click the green triangle to Run.

## Setup

1. Install dependencies

   ```shell
   $ pipenv install --dev
   ```

2. Setup pre-commit and pre-push hooks

   ```shell
   $ pipenv run pre-commit install -t pre-commit
   $ pipenv run pre-commit install -t pre-push
   ```

## Useful Commands

### Run unit test

```shell
$ pipenv run pytest --cov --cov-fail-under=50
```

### Conventional Changelog CLI

1. Install global dependencies (optional if installed):

   ```sh
   $ npm install -g conventional-changelog-cli
   ```

2. This will *not* overwrite any previous changelogs. The above generates a changelog based on commits since the last semver tag that matches the pattern of "Feature", "Fix", "Performance Improvement" or "Breaking Changes".

   ```sh
   $ conventional-changelog -p angular -i CHANGELOG.md -s
   ```

3. If this is your first time using this tool and you want to generate all previous changelogs, you could do:

   ```sh
   $ conventional-changelog -p angular -i CHANGELOG.md -s -r 0
   ```

## CI (Continuous Integration)

- GitHub Actions is for building project and running tests.
- ~~[Travis CI](https://travis-ci.com/github/johnnymillergh/media-streaming) is for publishing Docker Hub images of SNAPSHOT and RELEASE.~~

## Maintainers

[@johnnymillergh](https://github.com/johnnymillergh)

## Contributing

Feel free to dive in! [Open an issue](https://github.com/johnnymillergh/home_guardian/issues/new).

### Contributors

This project exists thanks to all the people who contribute. 

- Johnny Miller [[@johnnymillergh](https://github.com/johnnymillergh)]
- …

### Sponsors

Support this project by becoming a sponsor. Your logo will show up here with a link to your website. [[Become a sponsor](https://become-a-sponsor.org)]

## Credits

This package was created with Cookiecutter and the [sourcery-ai/python-best-practices-cookiecutter](https://github.com/sourcery-ai/python-best-practices-cookiecutter) project template.

Inspired by [How to set up a perfect Python project](https://sourcery.ai/blog/python-best-practices/).

Icon from [flaticon - Shield](https://www.flaticon.com/free-icon/shield_929429), [home](https://www.flaticon.com/premium-icon/home_2549900).

## License

[Apache License](https://github.com/johnnymillergh/home_guardian/blob/master/LICENSE) © Johnny Miller

2021 - Present
