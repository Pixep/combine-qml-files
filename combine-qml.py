import re
import os
import sys
from shutil import copyfile

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("basefile", help="Base file used to combine QML files together")
parser.add_argument("destfile", help="Destination file after operation")
parser.add_argument("-c", "--component", dest="components", required=True, action='append', nargs=2, metavar=('FILE', 'LABEL'),
                    help="Add a component file to combine, from FILE file, and replacing LABEL from base QML file")
parser.add_argument("-v", "--verbose", help="Output more information", action="store_true")
args = parser.parse_args()

def trimComponent(componentLines):
    linesToDelete = []
    for i in range(len(componentLines)):
        if componentLines[i].startswith('import'):
            linesToDelete.append(i)

    for lineIndex in reversed(linesToDelete):
        del componentLines[lineIndex]

# Removes components original properties when redefined in final file
def filterRedefinedProperties(componentLines, contentLines):
    linesToAdd = componentLines[:]
    propertyRegexp = re.compile(r'^(\s*)(property\s+\w+\s+)?(\w+)\s*:(.*$)')

    for contentIndex, contentLine in enumerate(contentLines):
        matchInRedefinition = propertyRegexp.search(contentLine)

        if matchInRedefinition:
            deleteLineIndex = -1
            propertyIndentation = matchInRedefinition.group(1)
            propertyName = matchInRedefinition.group(3)
            propertyValue = matchInRedefinition.group(4)
            openedBraces = 0
            for lineIndex in range(len(linesToAdd)):

                if linesToAdd[lineIndex].find('{') >= 0:
                    openedBraces += 1
                if linesToAdd[lineIndex].find('}') >= 0:
                    openedBraces -= 1

                if openedBraces == 1:
                    matchInOriginal = re.match(r'^\s+((property\s+\w+\s+)?' + propertyName + '\s*:)', linesToAdd[lineIndex])
                    if matchInOriginal:
                        propertyDeclaration = matchInOriginal.group(1)

                        # Combine original declaration, and value redefinition
                        newLine = propertyDeclaration + propertyValue + '\n'
                        newLine = propertyIndentation + newLine

                        contentLines[contentIndex] = newLine
                        deleteLineIndex = lineIndex

                        if args.verbose:
                            print 'merging line ' + linesToAdd[lineIndex].replace('\n', '')
                        break

            if deleteLineIndex >= 0:
                del linesToAdd[deleteLineIndex]

    return linesToAdd

# Returns the component merged with its local content
def mergedComponent(componentLines, contentLines, indentation):
    comp = ''
    filteredComponentLines = filterRedefinedProperties(componentLines=componentLines, contentLines=contentLines)

    # Insert component code
    for line in filteredComponentLines:
        if line.find('}') == 0:
            break
        else:
            comp += indentation + line

    if len(contentLines) > 0:
        comp += indentation + '    //---- Redefinitions ----\n'

    # Insert code form its content
    for contentLine in contentLines:
        comp += contentLine

    return comp

# Replaces component tokens by content of a file
def mergeComponentInDocument(originalFilePath, componentFilePath, componentName):
    print 'Merging @' + componentName + ' (' + componentFilePath + ') into ' + originalFilePath

    # Open destination file
    try:
        originalFile = open(originalFilePath, 'r+')
    except:
        print 'Failed to open base file ""' + originalFilePath + '"'
        return False

    # Read component
    try:
        componentFile = open(componentFilePath)
        componentLines = componentFile.readlines()
    except:
        print 'Failed to open component file "' + componentFilePath + '"'
        return False

    trimComponent(componentLines)

    # Insert component in file
    finalFileContent = ''
    componentRegexp = re.compile(r'^(\s*)@'+componentName+' ?{')
    insertingComponent = False
    indentation = ''

    for line in originalFile:
        if insertingComponent == False:
            res = componentRegexp.search(line)
            if res:
                indentation = res.group(1)
                contentLines = []
                insertingComponent = True
                openedBraces = 1
            else:
                finalFileContent += line
        else:
            if line.find('{') >= 0:
                openedBraces += 1
            if line.find('}') >= 0:
                openedBraces -= 1

            if openedBraces > 0:
                contentLines.append(line)
            else:
                insertingComponent = False
                comp = mergedComponent(componentLines=componentLines, contentLines=contentLines, indentation=indentation)
                finalFileContent += indentation + '//---------------\n'
                finalFileContent += indentation + '// @' + componentName + '\n'
                finalFileContent += comp
                finalFileContent += line

    originalFile.seek(0)
    originalFile.write(finalFileContent)
    originalFile.truncate()

    return True

workfile = args.basefile + '.tmp'
copyfile(args.basefile, workfile)

for comp in args.components:
    if mergeComponentInDocument(workfile, comp[0], comp[1]) == False:
        print "Aborting..."
        sys.exit(1)

copyfile(workfile, args.destfile)

if args.verbose:
    print open(workfile).read()

os.remove(workfile)
print "Combination successful"
