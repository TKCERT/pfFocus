# pfFocus

[![Build Status](https://travis-ci.org/TKCERT/pfFocus.svg?branch=master)](https://travis-ci.org/TKCERT/pfFocus)

This simple tool allows you to convert a full configuration backup of a *pf*Sense firewall into some meaningful output format, like Markdown or YAML. It enables you to **focus** on the important parts of your firewall configuration and allows you to get a quick overview of the most important settings.

## Requirements

* Python 3.5+
    * defusedxml==0.5.0
    * PyYAML==3.12

## Screenshots

**Before:** Configuration backup as XML

![Configuration backup as XML](screenshots/pfFocus_xml.png)

**After:** Markdown documentation

![System and Interfaces](screenshots/pfFocus_System_Interfaces.png)
![Filter rules](screenshots/pfFocus_Filter_rules.png)

## Usage

Main formatting tool: ```format.py```
```
format.py
```

Examples:
```
./format.py -i config-backup.xml -f md -o test.md
./format.py -i config-backup.xml -f yaml -o test.yaml
```

Test parsing tool: ```parse.py```
```
parse.py [-h] input_path
```

Examples:
```
./parse.py config-backup.xml
```

## Credits

* Thomas Patzke ([@thomaspatzke](https://github.com/thomaspatzke)) for
    * valuable suggestions and feedback
* Florian Roth ([@Cyb3rOps](https://twitter.com/Cyb3rOps)) for
    * giving it the name *pfFocus*
