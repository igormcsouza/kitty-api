# ChatBot API for Cats questions

[![Continuous Integration](https://github.com/igormcsouza/kitty-api/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/igormcsouza/kitty-api/actions/workflows/ci.yml)

Do you have any questions about cats? Don't worry, this api will help answer
your questions using a very smart AI that knows everything about cats.

## Release Notes

See [CHANGELOG.md](CHANGELOG.md) for release notes.

## How to test the api

Github actions already does that every push and pull request. Nevertheless you
might want to run locally the test. I'm using tox to manage testing pipeline.

    kitty-api$ tox

As simple as that.

## How does the IA works?

:sweat_smile: I built a
[gist](https://gist.github.com/igormcsouza/c8ec7f56de42c782ee2e82b7e96eb99b)
where I created the AI model from scratch!

## Troubleshooting

* [Wrong Heroku Stack](https://gist.github.com/igormcsouza/17282ec2189cb822a66a2d05e8d6800d#wrong-heroku-stack)

* [Tox could not find setup](https://gist.github.com/igormcsouza/17282ec2189cb822a66a2d05e8d6800d#tox-could-not-find-setup)
