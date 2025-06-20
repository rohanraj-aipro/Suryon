// GUI Builder in C++ using Win32 API
// It collects Discord Token and Channel ID,
// replaces placeholders in main_template.py, and compiles it to an .exe using PyInstaller with icon1.ico

#include <windows.h>
#include <fstream>
#include <string>
#include <shellapi.h>

#define IDC_TOKEN     101
#define IDC_CHANNELID 102
#define IDC_GENERATE  103

HINSTANCE hInst;
HWND hTokenInput, hChannelInput;

std::string ReadFile(const std::string& path) {
    std::ifstream in(path);
    std::string content((std::istreambuf_iterator<char>(in)), std::istreambuf_iterator<char>());
    return content;
}

void WriteFile(const std::string& path, const std::string& content) {
    std::ofstream out(path);
    out << content;
    out.close();
}

std::string ReplacePlaceholders(std::string text, const std::string& token, const std::string& channelId) {
    size_t pos;
    pos = text.find("{DISCORD_TOKEN}");
    if (pos != std::string::npos) text.replace(pos, 15, token);
    pos = text.find("{CHANNEL_ID}");
    if (pos != std::string::npos) text.replace(pos, 12, channelId);
    return text;
}

void GenerateScriptAndCompile(HWND hwnd) {
    char token[256], channelId[256];
    GetWindowTextA(hTokenInput, token, 256);
    GetWindowTextA(hChannelInput, channelId, 256);

    std::string templateCode = ReadFile("main_template.py");
    std::string finalCode = ReplacePlaceholders(templateCode, token, channelId);
    WriteFile("main_final.py", finalCode);

    MessageBox(hwnd, "main_final.py created. Compiling to .exe...", "Please wait", MB_OK);

    // Compile with icon using PyInstaller
    system("pyinstaller --onefile --noconsole --icon=icon1.ico main_final.py");

    MessageBox(hwnd, "main_final.exe compiled successfully.", "Done", MB_OK);
}

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    switch (msg) {
        case WM_CREATE:
            CreateWindow("STATIC", "Discord Token:", WS_VISIBLE | WS_CHILD,
                         10, 10, 100, 20, hwnd, NULL, hInst, NULL);
            hTokenInput = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER,
                                       120, 10, 250, 20, hwnd, (HMENU)IDC_TOKEN, hInst, NULL);

            CreateWindow("STATIC", "Channel ID:", WS_VISIBLE | WS_CHILD,
                         10, 40, 100, 20, hwnd, NULL, hInst, NULL);
            hChannelInput = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER,
                                         120, 40, 250, 20, hwnd, (HMENU)IDC_CHANNELID, hInst, NULL);

            CreateWindow("BUTTON", "Generate .exe", WS_VISIBLE | WS_CHILD,
                         120, 80, 150, 30, hwnd, (HMENU)IDC_GENERATE, hInst, NULL);
            break;

        case WM_COMMAND:
            if (LOWORD(wParam) == IDC_GENERATE) {
                GenerateScriptAndCompile(hwnd);
            }
            break;

        case WM_DESTROY:
            PostQuitMessage(0);
            break;
    }
    return DefWindowProc(hwnd, msg, wParam, lParam);
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE, LPSTR, int nCmdShow) {
    hInst = hInstance;
    WNDCLASS wc = {0};
    wc.lpfnWndProc = WndProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = "GUIBuilder";

    RegisterClass(&wc);
    HWND hwnd = CreateWindow("GUIBuilder", "Discord Bot Builder", WS_OVERLAPPEDWINDOW,
                             CW_USEDEFAULT, CW_USEDEFAULT, 400, 160, NULL, NULL, hInstance, NULL);

    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);

    MSG msg = {0};
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    return 0;
}
