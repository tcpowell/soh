import subprocess, os, re, shutil

# *********************************************************************************************************************
# * Defined methods
# *********************************************************************************************************************

def pathExists(dir):
    if (os.path.exists(dir)):
        return True
    else:
        return False 

def info(text):
    print("INFO: " + text)

def error(text):
    print("\033[91m{}\033[00m".format("ERROR: ") + text)
    errors+=1
    
def warning(text):
    print("\033[93m{}\033[00m".format("WARNING: ") + text)
    warnings+=1

def success(text):
    print("\033[92m{}\033[00m".format("SUCCESS: ") + text)

def copyFile(sourceFilePath, targetDirectory, targetFilename):
    if (pathExists(sourceFilePath)):
        shutil.copy2(sourceFilePath, targetDirectory + "\\" + targetFilename)
        info("Copied " + targetFilename + " to " + targetDirectory)
    else:
        warning("File not located: " + sourceFilePath)

def runSubprocess(commands):
    try:
        process = subprocess.run(
           commands, timeout=100, check=True, capture_output=True, encoding="utf-8"
        )
        for line in process.stdout.split("\n"):
            info(line)
        return process.returncode
    except FileNotFoundError as exc:
        error(f"Process failed because the executable could not be found.\n{exc}")
        return 1
    except subprocess.CalledProcessError as exc:
        error(
            f"Process failed because did not return a successful return code. "
            f"Returned {exc.returncode}\n{exc}"
        )
        return 1
    except subprocess.TimeoutExpired as exc:
        error(f"Process timed out.\n{exc}")
        return 1

def updateGit():
    runSubprocess(["git", "fetch", "--all"])
    runSubprocess(["git", "reset", "--hard", "origin/master"])

def downloadFile(url, saveLocation, fileName):
    try:
        process = subprocess.run(
           ["wget", url, "-O", saveLocation + "\\" + fileName], timeout=100, check=True, capture_output=True, encoding="utf-8"
        )
        for line in process.stderr.split("\n"):
            if line != "":
                lastline = line
        info(lastline)
        return process.returncode
    except FileNotFoundError as exc:
        error(f"Process failed because the executable could not be found.\n{exc}")
        return 1
    except subprocess.CalledProcessError as exc:
        error(
            f"Process failed because did not return a successful return code. "
            f"Returned {exc.returncode}\n{exc}"
        )
        return 1
    except subprocess.TimeoutExpired as exc:
        error(f"Process timed out.\n{exc}")
        return 1

def extract(file, target):
    try:
        process = subprocess.run(
           ["tar", "-xf", file, "-C", target], timeout=100, check=True, capture_output=True, encoding="utf-8"
        )
        for line in process.stdout.split("\n"):
            info(line)
        return process.returncode
    except FileNotFoundError as exc:
        error(f"Process failed because the executable could not be found.\n{exc}")
        return 1
    except subprocess.CalledProcessError as exc:
        error(
            f"Process failed because did not return a successful return code. "
            f"Returned {exc.returncode}\n{exc}"
        )
        return 1
    except subprocess.TimeoutExpired as exc:
        error(f"Process timed out.\n{exc}")
        return 1

def teardown():
    print()
    if errors==0 and warnings==0:
        success("SOH Updater completed")
    if warnings > 0:
        warning(str(warnings) + " warnings were encountered")
        info("SOH Updater completed")
    if errors > 0:
        error(str(errors) + " errors were encountered")
        info("SOH Updater completed")
    print()
    input('Press Enter to exit')
    exit()

def createDir(path):
    if not os.path.exists(path):
        info("Creating directory " + path)
        os.mkdir(path)



# *********************************************************************************************************************
# * Main Block
# *********************************************************************************************************************

# Variables
romDir = os.environ.get('USERPROFILE') + "\\Games\\SoH-ROM"
romFilename = "ZELOOTD.z64"
gamesDir = os.environ.get('USERPROFILE') + '\\Games'
shortcutsDir = os.environ.get('USERPROFILE') + '\\Shortcuts'
shortcutName = "soh.bat"
tempDir = os.environ.get("TEMP")
saveDir = "\\Save"
sohURLs = "soh_urls.txt"
modURLs = "mod_urls.txt"
modList = "mod_list.txt"
gitFiles = ["shipofharkinian.json", "imgui.ini"]
modsFolder = "\\mods"
warnings = 0
errors = 0

# Clear screen
os.system('cls')

# Update Git repository
info("Updating Git repository")
updateGit()

# Check the Games directory exists, or create it
createDir(gamesDir)

# Check the Shortcuts directory exists, or create it
createDir(shortcutsDir)

# Verify SOH URL file exists
if not pathExists(sohURLs):
    error("Could not locate " + sohURLs)
    teardown()

# Loop through to see what versions we have installed
info("Checking for new versions")
with open(sohURLs) as f:
    linenum = 0
    for line in f:
        url = line.rstrip()
        version = re.split(r"\.|/", url)[-2]
        versionDir = gamesDir + '\\' + version
        if linenum == 0:
            newestDir = versionDir
            if pathExists(versionDir):
                info("Already on the latest version: " + version)
                teardown()
            else:
                # Download and unzip newest
                info("Downloading newest version")
                downloadFile(url, tempDir, version + ".zip")
                zipFile = tempDir + "\\" + version + ".zip"
                createDir(newestDir)
                info("Extracting archive")
                extract(zipFile, newestDir)
                os.remove(zipFile)
                
                # Copy ROM file
                info("Copying ROM to new directory")
                copyFile(romDir + "\\" + romFilename, newestDir, romFilename)
                
                # Copy Git files
                info("Copying configuration files to new directory")
                for gitFile in gitFiles:
                    copyFile(gitFile, newestDir, gitFile)

                # Verify mod URLs exist
                if not pathExists(modURLs):
                    warning("Could not locate " + modURLs)
                    teardown()
                    
                # Verify mod List exists
                if not pathExists(modList):
                    warning("Could not locate " + modList)
                    teardown()

                # Download and unzip mods
                info("Downloading and extracting mods")
                createDir(newestDir + modsFolder)
                with open(modURLs) as m:
                    modnum = 1
                    for modLine in m:
                        modURL = modLine.rstrip()
                        modFilename = "soh_mod_"+str(modnum)+".zip"
                        modZipFile = tempDir + "\\" + modFilename
                        downloadFile(modURL, tempDir, modFilename)
                        extract(modZipFile, newestDir + modsFolder)
                        os.remove(modZipFile)
                        modnum+=1
                
                # Deal with nested folders (only deals with one level at the moment)
                for files in os.listdir(newestDir + modsFolder):
                    fullFile = newestDir + modsFolder+"\\"+files
                    if os.path.isdir(fullFile):
                        for nested in os.listdir(fullFile):
                            if os.path.isfile(fullFile+"\\"+nested):
                                shutil.move(fullFile+"\\"+nested, newestDir + modsFolder+"\\"+nested)
                            else:
                                warning("Nested folder found: " + nested)
                        os.rmdir(fullFile)
                
                # Verify mods
                info("Verifying mods")
                with open(modList) as l:
                    modArray = [] 
                    for modItem in l:
                        modArray.append(modItem.rstrip())
                        if not pathExists(newestDir + modsFolder + "\\" + modItem.rstrip()):
                            warning("Listed mod could not be found: " + modItem.rstrip())
                
                # Inactivate/Delete unused mods
                info("Toggling mods (inactivated mods appended with .old)")
                for dir, subdirs, files in os.walk(newestDir + modsFolder):
                    for modOTR in files:
                        if modOTR.lower().endswith(".otr"):
                            if modOTR in modArray:
                                info(modOTR + " is active")
                            else:
                                os.rename(newestDir + modsFolder + "\\" + modOTR, newestDir + modsFolder + "\\" + modOTR + ".old")
                                info(modOTR + " set INACTIVE")
                        else:
                            os.remove(newestDir + modsFolder + "\\" + modOTR)
                
                # Create and move shortcut
                print("Configuring shortcut")
                shortcut = open(shortcutName, "w")
                shortcut.write("cd %USERPROFILE%\\Games\\"+version+"\n")
                shortcut.write("start soh.exe")
                shortcut.close()
                shutil.move(shortcutName, shortcutsDir+"\\"+shortcutName)
                
        if linenum>0 and pathExists(versionDir):
            
            # Copy Save information
            info("Copying save data from older version: " + version)
            versionSave = versionDir + saveDir
            newSave = newestDir + saveDir
            createDir(newSave)
            
            saveFiles = os.listdir(versionSave)
            for saveFile in saveFiles:
                copyFile(versionSave+"\\"+saveFile, newSave, saveFile)

            teardown()
            
        linenum+=1
