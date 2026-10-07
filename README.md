# WikiTree for Gramps

WikiTree for Gramps adds WikiTree integration to Gramps.

**Current version: 0.1.0**

The current version adds a **WikiTree ID** field directly to the Gramps Person Editor, allowing a person in Gramps to be linked to their corresponding WikiTree profile.

## Features

- Link a Gramps person to their WikiTree profile directly from the Person Editor.

## Requirements

- Gramps 6.0.x

## Installation

WikiTree for Gramps can be installed through the Gramps Addon Manager.

### 1. Open the Addon Manager

In Gramps, go to:

**Addons**

### 2. Add the WikiTree for Gramps repository

Select the **Projects** tab.

Click **Add Project** and enter the WikiTree for Gramps addon repository URL:

    [REPOSITORY URL]

Save the project.

### 3. Install WikiTree for Gramps

Select the **Addons** tab.

Find **WikiTree for Gramps** in the list of available addons and install it.

### 4. Restart Gramps

Close Gramps completely and reopen it.

WikiTree for Gramps will then be available in the Person Editor.

## Usage

Open a person in Gramps and select **Edit**.

The Person Editor will include a **WikiTree ID** field.

Enter the person's WikiTree ID:

    Smith-12345

You can also paste a full WikiTree profile URL:

    https://www.wikitree.com/wiki/Smith-12345

The WikiTree ID will be extracted automatically.

Click **Open WikiTree** to open the corresponding WikiTree profile in your default browser.

## Updating

Updates to WikiTree for Gramps are distributed through the Gramps Addon Manager.

Open:

**Edit > Addon Manager**

Gramps can check the configured WikiTree for Gramps repository for newer versions of the addon.

## Manual Installation

Manual installation is primarily intended for development and troubleshooting.

Download the `WikiTreeForGramps.addon.tgz` package and extract its contents into a `WikiTreeForGramps` folder in your Gramps plugins directory.

On Windows with Gramps 6.0, this is normally:

    %APPDATA%\gramps\gramps60\plugins\WikiTreeForGramps\

The folder should contain:

    WikiTreeForGramps/
    ├── WikiTreeForGramps.gpr.py
    └── WikiTreeForGramps.py

Restart Gramps after installing the files.

## Development

The source code for WikiTree for Gramps is maintained on GitHub.

The addon currently consists of:

    WikiTreeForGramps/
    ├── WikiTreeForGramps.gpr.py
    └── WikiTreeForGramps.py

The distributable Gramps addon package is:

    WikiTreeForGramps.addon.tgz

## Contributing

Bug reports, feature requests, and pull requests are welcome.

Use GitHub Issues to report problems or suggest new WikiTree integration features.

## License

WikiTree for Gramps is licensed under the GNU General Public License v2.0 or later.

## Links

- WikiTree: https://www.wikitree.com/
- Gramps: https://gramps-project.org/