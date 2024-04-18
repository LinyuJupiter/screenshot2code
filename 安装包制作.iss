; �ű��� Inno Setup �ű��� ���ɣ�
; �йش��� Inno Setup �ű��ļ�����ϸ��������İ����ĵ���

#define MyAppName "Screenshot2code"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "����"
#define MyAppExeName "Screenshot2code.exe"

[Setup]
; ע: AppId��ֵΪ������ʶ��Ӧ�ó���
; ��ҪΪ������װ����ʹ����ͬ��AppIdֵ��
; (�����µ�GUID����� ����|��IDE������GUID��)
AppId={{B2F9A9D7-D460-4F67-B56C-D4F8812A62E2}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=C:\Users\86188\PycharmProjects\screenshot2code\�û�Э��.txt
InfoBeforeFile=C:\Users\86188\PycharmProjects\screenshot2code\��װ��Ϣ.txt
InfoAfterFile=C:\Users\86188\PycharmProjects\screenshot2code\������־.txt
OutputDir=C:\Users\86188\PycharmProjects\screenshot2code\packages
OutputBaseFilename=Screenshot2code-setup-1.0.0
SetupIconFile=C:\Users\86188\PycharmProjects\screenshot2code\favicon.ico
Compression=lzma
SolidCompression=yes

[UninstallDelete]
Name: {app}; Type: filesandordirs; Languages:

[Languages]
Name: "chinesesimp"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkablealone; OnlyBelowVersion: 0,6.3

[Files]
Source: "C:\Users\86188\PycharmProjects\screenshot2code\Screenshot2code\Screenshot2code.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\86188\PycharmProjects\screenshot2code\Screenshot2code\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; ע��: ��Ҫ���κι���ϵͳ�ļ���ʹ�á�Flags: ignoreversion��

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

