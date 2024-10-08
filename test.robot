*** Settings ***
Library    AppiumLibrary
Library    BuiltIn
Library    OperatingSystem

Suite Setup       connect_appium
Suite Teardown    close_app

*** Variables ***
${REMOTE_URL}         http://127.0.0.1:4723/wd/hub
${PLATFORM_NAME}      Android
${PLATFORM_VERSION}   None
${DEVICE_NAME}        None
${APP_PACKAGE}        com.pax.us.pay.std.cyberlab
${APP_ACTIVITY}       com.pax.pay.ui.SplashActivity

*** Test Cases ***
test_capture_home
    [Documentation]    在应用主页面截屏并保存至报告中
    Log    Application is running. Preparing to take a screenshot.
    Sleep     5s
    Capture Page Screenshot    ${OUTPUT_DIR}${/}${TEST NAME}.png

test_case2
    [Documentation]    case2截屏并保存至报告中
    Log    Application is running. Preparing to take a screenshot.
    Sleep     5s
    Capture Page Screenshot    ${OUTPUT_DIR}${/}${TEST NAME}.png

*** Keywords ***
connect_appium
    [Documentation]    连接到Appium Server并打开已安装的应用
    init_params
    Open Application    ${REMOTE_URL}    platformName=${PLATFORM_NAME}    platformVersion=${PLATFORM_VERSION}    deviceName=${DEVICE_NAME}    appPackage=${APP_PACKAGE}    appActivity=${APP_ACTIVITY}    automationName=uiautomator2    noReset=false
    Log    Application has been launched successfully.

close_app
    [Documentation]    关闭已连接的应用程序
    Close Application
    Log    Application has been closed successfully.

init_params
    [Documentation]    初始化测试参数
    # 从环境变量获取参数
    ${platformVersion}   Get Environment Variable    platformVersion
    ${deviceName}        Get Environment Variable    deviceName

    #设置为全局变量
    Set Global Variable    ${PLATFORM_VERSION}   ${platformVersion}
    Set Global Variable    ${DEVICE_NAME}        ${deviceName}
    Log    Platform Version: ${PLATFORM_VERSION}
    Log    Device Name: ${DEVICE_NAME}
    Log    Test parameters initialized.
