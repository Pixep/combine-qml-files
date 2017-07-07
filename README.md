# qml-files-combiner
Python script that integrates QML components file into a base file.

## Features
- Combine QML components into a base file
- Aware of properties override. It will preserve the value assigned where your component is used
- Supports custom properties

#### Limitations
- Requires a special `@` token at the time in front of component name
- Not compatible with `alias` properties, as QML files are merged together

#### Known issues
- Final indentation can vary if both base and component files use different indentation styles (tabs, different number of spaces, ...)

## Usage

```
usage: combine-qml.py [-h] -c FILE COMPONENT [-v] basefile destfile

Integrate components in a base QML file, where the @COMPONENT syntax is used
(i.e. @MyButton)

positional arguments:
  basefile              Base file used to combine QML files together
  destfile              Destination file after operation

optional arguments:
  -h, --help            show this help message and exit
  -c FILE COMPONENT, --component FILE COMPONENT
                        Add a component file to combine, from FILE file, and
                        replacing @COMPONENT from base QML file
  -v, --verbose         Output more information
```
 
## Example

Below is an example where we integrate a custom QML button into another file

This is the base file, note the presence of the `@` token followed by the name of the component
```
Item {
    @Button {
        text: "final text"
    }
}
```

Button component file:
```
import QtQuick 2.2
Text {
    color: "gray"
    width: 100
    height: 30
    text: "original text"

    MouseArea {}
}
```

Then you can use the following command line to replace `@Button` from base-main.qml, by the content of Button.qml. The result outputs in final-main.qml
```
> python combine-qml.py base-main.qml final-main.qml -c Button.qml Button
```

Here is the final output file
```
Item {
    //---------------
    // @Button
    Text {
        color: "gray"
        width: 100
        height: 30

        MouseArea {}

        //---- Redefinitions ----
        text: "final text"
    }
 }
 ```
