# My Personal Workspace Setup

## Python
I've written a series of Python scripts that help out with some tasks I constantly find myself doing

The scripts are located in the `python_scripts` directory. They are bundled into a single executable using the following command in Pyinstaller:

```bash
pyinstaller  ./python_scripts/pyinstall.py  --name pyscripts --onefile --distpath ./bin
```

The executable can be run via:

```bash
./bin/pyscripts
```

## Eclipse

When writing Java code, I make use of auto-formatting functionality in the [Language Support for Java](https://github.com/redhat-developer/vscode-java) extension in VSCode. The extension will format files according to an Eclipse formatter file that the user specifies.

To set the formatter file, add the following property to your settings.json file in VSCode:

```json
"java.format.settings.url": "https://raw.githubusercontent.com/mscully4/workspace/staging/eclipse/formatting/java-style-amazon.xml"
```

A single formatter file can contain multiple profiles. To set the profile to use, add the following entry your settings.json file in VSCode

```json
"java.format.settings.profile": "PineappleDev",
```

The full setup for the extension can be found in the project's wiki [here](https://github.com/redhat-developer/vscode-java/wiki/Formatter-settings).
