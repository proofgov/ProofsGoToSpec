# PROOF's Go to Spec (forked from Rails Go To Spec)

A Sublime Text 3 plug-in. From a .rb file this plug-in will open the relevant spec. If the spec doesn't exist it asks if it should be created.

Supports `_spec.rb` files and `-test.js` files and `_test.py` files

## Installation

> Note that the repo must be pulic to work.

1. Package Control: Add Repository -> https://github.com/proofgov/ProofsGoToSpec.git
2. Package Control: Install Package -> PROOF's Go To Spec: https://github.com/proofgov/ProofsGoToSpec.git
3. Inside SublimeText open Preferences -> Browse Packages.
   > optionally - Restart SublimeText
4. Package Control: List Packages -> PROOFsGoToSpec should exist.

## Preferences

Preferences -> Package Settings > ProofsGoToSpec > Settings
By default, specs are assumed to live in "/spec", but if you have a nonstandard
location, you can override current setting in your preferences.

If you have Javascript files they will live in "/test", which you can override in your preferences. The path is also slightly mangled "/javascript/" becomes "/js/". Vue files are supported with the same style as JS files.

If you have Python files they will live in "/tests".

## Usage

- Run from menu > Goto > PROOF's Go to Spec
- Default key binding is `command + shift + y`
- Or run from command palette `PROOF's Go to Spec`

## Dev

git clone https://github.com/proofgov/ProofsGoToSpec.git PROOFsGoToSpec

## Testing

From the project directory:
`python -m unittest discover`

## Acknowledgements

Thanks to [PROOF](https://proofgov.com/) for providing the time to work on this.
And to [elthran](https://github.com/elthran) for always getting me to write code that needs this kind of thing.
