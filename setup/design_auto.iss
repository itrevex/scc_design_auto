; -- Design Auto.iss --
; For creating design auto files

; SEE THE DOCUMENTATION FOR DETAILS ON CREATING .ISS SCRIPT FILES!

#define MyAppName "SSC Design"
#define MyAppSetUpName "ssc_design_setup-"
#define MyAppExeName "trsc.exe"
#define MyAppIcoName "icon_red.ico"
#define MyAppVersion "1.0.4"
#define SourcePath "E:\Projects/ESAI/PROGRAMMING/PYTHON/SSC/design_auto/dist"
;
[Setup]
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2
SolidCompression=yes
OutputDir=setups
ChangesAssociations = yes
OutputBaseFilename={#MyAppSetUpName}{#MyAppVersion}

[Registry]
Root: HKCR; Subkey: ".trsc";                            ValueData: "{#MyAppName}";          Flags: uninsdeletevalue; ValueType: string;  ValueName: ""
Root: HKCR; Subkey: "{#MyAppName}";                     ValueData: "{#MyAppName}";          Flags: uninsdeletekey;   ValueType: string;  ValueName: ""
Root: HKCR; Subkey: "{#MyAppName}\DefaultIcon";         ValueData: """{app}\{#MyAppIcoName}""";                      ValueType: string;  ValueName: ""
Root: HKCR; Subkey: "{#MyAppName}\shell\open\command";  ValueData: """{app}\{#MyAppExeName}"" ""%1""";               ValueType: string;  ValueName: ""

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; \
    GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
;
;Program icon
Source: "{#MyAppIcoName}"; DestDir: "{app}"
;
;Files in assests folder
; Source: "{#SourcePath}\assests\document_table_template.json"; DestDir: "{app}\assests"
; Source: "{#SourcePath}\assests\document_value_template.json"; DestDir: "{app}\assests"
; Source: "{#SourcePath}\assests\wind_coeffiecients.json"; DestDir: "{app}\assests"
; Source: "{#SourcePath}\assests\wind_design_defaults.json"; DestDir: "{app}\assests"
; Source: "{#SourcePath}\assests\windmap_defaults.json"; DestDir: "{app}\assests"
; Source: "{#SourcePath}\assests\Gen-Desc_710_asd.docx"; DestDir: "{app}\assests"
; Source: "{#SourcePath}\assests\Gen-Desc.docx"; DestDir: "{app}\assests"
; Source: "{#SourcePath}\assests\asce\table_27_3_1.json"; DestDir: "{app}\assests\asce"
;
Source: "{#SourcePath}\main\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs
;Files in lxml folder
; Source: "{#SourcePath}\lxml\_elementpath.cp37-win_amd64.pyd"; DestDir: "{app}\lxml"
; Source: "{#SourcePath}\lxml\etree.cp37-win_amd64.pyd"; DestDir: "{app}\lxml"
; ;
; ;Files in input folder
; Source: "{#SourcePath}\input\sample1.trsc"; DestDir: "{userdesktop}\{#MyAppName}"
; Source: "{#SourcePath}\input\sample1.trsc"; DestDir: "{localappdata}\{#MyAppName}\data"

; ;
; ;Files in main Folder
; Source: "{#SourcePath}\_bz2.pyd"; DestDir: "{app}"
; Source: "{#SourcePath}\_hashlib.pyd"; DestDir: "{app}"
; Source: "{#SourcePath}\_lzma.pyd"; DestDir: "{app}"
; Source: "{#SourcePath}\_socket.pyd"; DestDir: "{app}"
; Source: "{#SourcePath}\_ssl.pyd"; DestDir: "{app}"
; Source: "{#SourcePath}\base_library.zip"; DestDir: "{app}"
Source: "{#SourcePath}\main\libcrypto-1_1-x64.dll"; DestDir: "{app}"; CopyMode: alwaysskipifsameorolder; Flags: onlyifdoesntexist restartreplace sharedfile 64bit; Check: IsWin64
Source: "{#SourcePath}\main\libssl-1_1-x64.dll"; DestDir: "{app}"; CopyMode: alwaysskipifsameorolder; Flags: onlyifdoesntexist restartreplace sharedfile 64bit; Check: IsWin64
Source: "{#SourcePath}\main\python37.dll"; DestDir: "{app}"; CopyMode: alwaysskipifsameorolder; Flags: onlyifdoesntexist restartreplace sharedfile 64bit; Check: IsWin64
Source: "{#SourcePath}\main\VCRUNTIME140.dll"; DestDir: "{app}"; CopyMode: alwaysskipifsameorolder; Flags: onlyifdoesntexist restartreplace sharedfile 64bit; Check: IsWin64
; Source: "{#SourcePath}\{#MyAppExeName}"; DestDir: "{app}"
; Source: "{#SourcePath}\{#MyAppExeName}.manifest"; DestDir: "{app}"
; Source: "{#SourcePath}\pyexpat.pyd"; DestDir: "{app}"
; Source: "{#SourcePath}\{#MyAppExeName}"; DestDir: "{app}"
; Source: "{#SourcePath}\select.pyd"; DestDir: "{app}"
; Source: "{#SourcePath}\unicodedata.pyd"; DestDir: "{app}"

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppIcoName}"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"; IconFilename: "{app}\{#MyAppIcoName}"
Name: "{userdesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; IconFilename: "{app}\{#MyAppIcoName}"
