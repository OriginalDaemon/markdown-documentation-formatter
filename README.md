# markdown-documentation-formatter

![Coverage Status](https://coveralls.io/repos/github/OriginalDaemon/markdown-documentation-processing/badge.svg?branch=main&service=github) ![CI](https://github.com/OriginalDaemon/markdown-documentation-processing/actions/workflows/ci.yml/badge.svg)

A system to take product documentation, stored in branch in markdown, and process it in various ways to ready it for deployment. This allows you to automate various parts of documentation maintenance such as;

 - Make all markdown file names unique for the purpose of deploying to confluence.
 - Use macros, written in the form ${variable_name} for consts and ${macro(arg1, ...)} for functions, throughout the documentation and have them filled automatically using values from a configured macros file written in python.
 - Automatically link the first instance of a keyword on each page to a predefined glossary of terms.
 - Use a structure of folders with README.md files for github convenience, but automate renaming them based on their parent folder.
 - Clean internal markdown links so they are in the form \[text\](\<path/to/file#subsection\>) which works for both github and obsidian.

This system is also extensible; you can add rules of your own by writing a python module with all your rules and passing them in. 

The overall aim is to be able to store your documentation with your code, in a form that is convenient to use when working on it, but massage it into a nicer form for users to read.

This system features a python library, which can be used on its own, a cli for convenient local running, and a github action so it can be included in your CI.

## TODO

 - Add a validate mode.
   - Do the normal full process and report if any files would be modified. In cases where modifications are required, then the docs are "invalid".
