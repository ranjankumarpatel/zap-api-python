#!/usr/bin/env python2

'''
This script aims to be the most generic and the most explicit possible.
It works with OWASP ZAP API Python client.
To use it, you have to load the Python API client module and start ZAP

Before starting this script for the first time: Open ZAP, go to
Tools -> Options -> API -> Generate random Key, copy and paste the key in the
variable "apiKey" of the configuration area

This script is divided into two parts : a configuration area, where you have to
change variables according to your needs, and the part with API calls.

Author : aine-rb on Github, from Sopra Steria
'''

import time
from pprint import pprint
from zapv2 import ZAPv2


#######################################
### BEGINNING OF CONFIGURATION AREA ###
#######################################
## The user only needs to change variable values bellow to make the script
## work according to his/her needs. MANDATORY parameters must not be empty

# MANDATORY. Define the API key generated by ZAP and used to verify actions.
apiKey='qiiutul4utrfub1b8veqs50bk0'

# MANDATORY. Define the listening address of ZAP instance
localProxy = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

# MANDATORY. True to create another ZAP session (overwritte the former if the
# same name already exists), False to use an existing one
isNewSession = True
# MANDATORY. ZAP Session name
sessionName = 'WebgoatSession'

# Define the list of global exclude URL regular expressions. List can be empty.
# The expressions must follow the java.util.regex.Pattern class syntax
# The following example excludes every single URL except http://localhost:8081
globalExcludeUrl = ['^(?:(?!http:\/\/localhost:8081).*).$']

# MANDATORY. Define if an outgoing proxy server is used
useProxyChain = False
# MANDATORY only if useProxyChain is True, ignored otherwise.
# Outgoing proxy address and port
proxyAddress = 'my.corp.proxy'
proxyPort = '8080'
# Define the addresses to skip in case useProxyChain is True. Ignored
# otherwise. List can be empty.
skipProxyAddresses = ('127.0.0.1;'
                      'localhost')
# MANDATORY only if useProxyChain is True. Ignored otherwise.
# Define if proxy server needs authentication
useProxyChainAuth = False
# MANDATORY only if useProxyChainAuth is True. Ignored otherwise
proxyUsername = ''
proxyPassword = ''
proxyRealm = ''

# MANDATORY. Determine if a proxy script must be loaded. Proxy scripts are
# executed for every request traversing ZAP
useProxyScript = False
# MANDATORY only if useProxyScript is True. Ignored otherwise
proxyScriptName = 'proxyScript.js'
# Script engine values: "Oracle Nashorn" for Javascript,
# "jython" for python, "JSR 223 JRuby Engine" for ruby
proxyScriptEngine = 'Oracle Nashorn'
# Asolute local path
proxyScriptFileName = '/zap/scripts/proxy/proxyScript.js'
proxyScriptDescription = 'This is a description'

# MANDATORY. Determine if context must be configured then used during scans.
# You have to set this parameter to True if you want that ZAP performs scans
# from the point of view of a specific user
useContextForScan = True

# MANDATORY only if useContextForScan is True. Ignored otherwise. Set value to
# True to define a new context. Set value to False to use an existing one.
defineNewContext = True
# MANDATORY only if defineNewContext is True. Ignored otherwise
contextName = 'WebGoat_script-based'
# MANDATORY only if defineNewContext is False. Disregarded otherwise.
# Corresponds to the ID of the context to use
contextId = 0
# Define Context Include URL regular expressions. Ignored if useContextForScan
# is False. You have to put the URL you want to test in this list.
contextIncludeURL = ['http://localhost:8081.*']
# Define Context Exclude URL regular expressions. Ignored if useContextForScan
# is False. List can be empty.
contextExcludeURL = ['http://localhost:8081/WebGoat/j_spring_security_logout',
                     'http://localhost:8081/WebGoat/logout.mvc']

# MANDATORY only if useContextForScan is True. Ignored otherwise. Define the
# session management method for the context. Possible values are:
# "cookieBasedSessionManagement"; "httpAuthSessionManagement"
sessionManagement = 'cookieBasedSessionManagement'

# MANDATORY only if useContextForScan is True. Ignored otherwise. Define
# authentication method for the context. Possible values are:
# "manualAuthentication"; "scriptBasedAuthentication"; "httpAuthentication";
# "formBasedAuthentication"
authMethod = 'scriptBasedAuthentication'

# MANDATORY only if authMethod is set to scriptBasedAuthentication.
# Ignored otherwise
authScriptName = 'TwoStepAuthentication.js'
# Script engine values: Oracle Nashorn for Javascript
# jython for python, JSR 223 JRuby Engine for ruby
authScriptEngine = 'Oracle Nashorn'
# Absolute local path
authScriptFileName = '/zap/scripts/authentication/TwoStepAuthentication.js'
authScriptDescription = 'This is a description'

# MANDATORY only if useContextForScan is True. Ignored otherwise. Each
# name/value pair of authParams are expected to be "x-www-form-urlencoded"
# Here is an example for scriptBasedAuthentication method:
authParams = ('scriptName=' + authScriptName + '&'
              'Submission Form URL=http://localhost:8081/WebGoat/j_spring_security_check&'
              'Username field=username&'
              'Password field=password&'
              'Target URL=http://localhost:8081/WebGoat/welcome.mvc')
## Here is an example for formBasedAuthentication method:
#authParams = ('loginUrl=http://localhost:8081/WebGoat/j_spring_security_check&'
#              'loginRequestData=username%3D%7B%25username%25%7D%26'
#              'password%3D%7B%25password%25%7D')
##Here is an example for httpAuthentication method:
#authParams = ('hostname=http://www.example.com&'
#              'realm=CORP\\administrator&'
#              'port=80')

# MANDATORY only if useContextForScan is True. Ignored otherwise.
# Set the value to True if a loggedin indicator must be used. False if it's a
# logged out indicator that must be used
isLoggedInIndicator = False
# MANDATORY only if useContextForScan is True. Ignored otherwise.
# Define either a loggedin or a loggedout indicator regular expression.
# It allows ZAP to see if the user is always authenticated during scans.
indicatorRegex = '\QLocation: http://localhost:8081/WebGoat/login.mvc\E'


# MANDATORY only if useContextForScan is True. Ignored otherwise.
# Set value to True to create new users, False otherwise
createUser = True
# MANDATORY only if createUser is True. Ignored otherwise. Define the list of
# users, with name and credentials (in x-www-form-urlencoded format)
## Here is an example with the script NashornTwoStepAuthentication.js:
userList = [
    {'name': 'guest', 'credentials': 'Username=guest&Password=guest'},
    {'name': 'webgoat', 'credentials': 'Username=webgoat&Password=webgoat'}
]
## Here is an example with formBasedAuthentication:
#userList = [
#    {'name': 'guest', 'credentials': 'username=guest&password=guest'},
#    {'name': 'webgoat', 'credentials': 'username=webgoat&password=webgoat'}
#]

# MANDATORY only if useContextForScan is True. Ignored otherwise. List can be
# empty. Define the userid list. Created users will be added to this list later
userIdList = []

# MANDATORY. Define the target site to test
target = 'http://localhost:8081/WebGoat'

# You can specify other URL in order to help ZAP discover more site locations
# List can be empty
applicationURL = ['http://localhost:8081/WebGoat/start.mvc',
                  'http://localhost:8081/WebGoat/welcome.mvc',
                  'http://localhost:8081/WebGoat/attack']

# MANDATORY. Set value to True if you want to customize and use a scan policy
useScanPolicy = True
# MANDATORY only if useScanPolicy is True. Ignored otherwise. Set a policy name
scanPolicyName = 'SQL Injection and XSS'
# MANDATORY only if useScanPolicy is True. Ignored otherwise.
# Set value to True to disable all scan types except the ones set in ascanIds,
# False to enable all scan types except the ones set in ascanIds..
isWhiteListPolicy = True
# MANDATORY only if useScanPolicy is True. Ignored otherwise. Set the scan IDs
# to use with the policy. Other scan types will be disabled if
# isWhiteListPolicy is True, enabled if isWhiteListPolicy is False.
# Use zap.ascan.scanners() to list all ascan IDs.
## In the example bellow, the first line corresponds to SQL Injection scan IDs,
## the second line corresponds to some XSS scan IDs
ascanIds = [40018, 40019, 40020, 40021, 40022, 40024, 90018,
            40012, 40014, 40016, 40017]
# MANDATORY only if useScanPolicy is True. Ignored otherwise. Set the alert
# Threshold and the attack strength of enabled active scans.
# Currently, possible values are:
# Low, Medium and High for alert Threshold
# Low, Medium, High and Insane for attack strength
alertThreshold = 'Medium'
attackStrength = 'Low'

# MANDATORY. Set True to use Ajax Spider, False otherwise.
useAjaxSpider = True

# MANDATORY. Set True to shutdown ZAP once finished, False otherwise
shutdownOnceFinished = False

#################################
### END OF CONFIGURATION AREA ###
#################################


# Connect ZAP API client to the listening address of ZAP instance
zap = ZAPv2(proxies=localProxy, apikey=apiKey)

# Start the ZAP session
core = zap.core
if isNewSession:
    pprint('Create ZAP session: ' + sessionName + ' -> ' +
            core.new_session(name=sessionName, overwrite=True))
else:
    pprint('Load ZAP session: ' + sessionName + ' -> ' +
            core.load_session(name=sessionName))

# Configure ZAP global Exclude URL option
print('Add Global Exclude URL regular expressions:')
for regex in globalExcludeUrl:
    pprint(regex + ' ->' + core.exclude_from_proxy(regex=regex))

# Configure ZAP outgoing proxy server connection option
pprint('Enable outgoing proxy chain: ' + str(useProxyChain) + ' -> ' +
        core.set_option_use_proxy_chain(boolean=useProxyChain))
if useProxyChain:
    pprint('Set outgoing proxy name: ' + proxyAddress + ' -> ' +
            core.set_option_proxy_chain_name(string=proxyAddress))
    pprint('Set outgoing proxy port: ' + proxyPort + ' -> ' +
            core.set_option_proxy_chain_port(integer=proxyPort))
    pprint('Skip names for outgoing proxy: ' + skipProxyAddresses + ' -> ' +
            core.set_option_proxy_chain_skip_name(string=skipProxyAddresses))

    # Configure ZAP outgoing proxy server authentication
    pprint('Set outgoing proxy chain authentication: ' +
            str(useProxyChainAuth) + ' -> ' +
            core.set_option_use_proxy_chain_auth(boolean=useProxyChainAuth))
    if useProxyChainAuth:
        pprint('Set outgoing proxy username -> ' +
                core.set_option_proxy_chain_user_name(string=proxyUsername))
        pprint('Set outgoing proxy password -> ' +
                core.set_option_proxy_chain_password(string=proxyPassword))
        pprint('Set outgoing proxy realm: ' + proxyRealm + ' -> ' +
                core.set_option_proxy_chain_realm(string=proxyRealm))

if useProxyScript:
    script = zap.script
    script.remove(scriptname=proxyScriptName)
    pprint('Load proxy script: ' + proxyScriptName + ' -> ' +
            script.load(scriptname=proxyScriptName, scripttype='proxy',
                scriptengine=proxyScriptEngine,
                filename=proxyScriptFileName,
                scriptdescription=proxyScriptDescription))
    pprint('Enable proxy script: ' + proxyScriptName + ' -> ' +
            script.enable(scriptname=proxyScriptName))


if useContextForScan:
    # Define the ZAP context
    context = zap.context
    if defineNewContext:
        contextId = context.new_context(contextname=contextName)
    pprint('Use context ID: ' + contextId)

    # Include URL in the context
    print('Include URL in context:')
    for url in contextIncludeURL:
        pprint(url + ' -> ' +
                context.include_in_context(contextname=contextName,
                                           regex=url))

    # Exclude URL in the context
    print('Exclude URL from context:')
    for url in contextExcludeURL:
        pprint(url + ' -> ' +
                context.exclude_from_context(contextname=contextName,
                                             regex=url))

    # Setup session management for the context.
    # There is no methodconfigparams to provide for both current methods
    pprint('Set session management method: ' + sessionManagement + ' -> ' +
            zap.sessionManagement.set_session_management_method(
                contextid=contextId, methodname=sessionManagement,
                methodconfigparams=None))

    ## In case we use the scriptBasedAuthentication method, load the script
    if authMethod == 'scriptBasedAuthentication':
        script = zap.script
        script.remove(scriptname=authScriptName)
        pprint('Load script: ' + authScriptName + ' -> ' +
                script.load(scriptname=authScriptName,
                            scripttype='authentication',
                            scriptengine=authScriptEngine,
                            filename=authScriptFileName,
                            scriptdescription=authScriptDescription))

    # Define an authentication method with parameters for the context
    auth = zap.authentication
    pprint('Set authentication method: ' + authMethod + ' -> ' +
            auth.set_authentication_method(contextid=contextId,
                                           authmethodname=authMethod,
                                           authmethodconfigparams=authParams))
    # Define either a loggedin indicator or a loggedout indicator regexp
    # It allows ZAP to see if the user is always authenticated during scans
    if isLoggedInIndicator:
        pprint('Define Loggedin indicator: ' + indicatorRegex + ' -> ' +
                auth.set_logged_in_indicator(contextid=contextId,
                                        loggedinindicatorregex=indicatorRegex))
    else:
        pprint('Define Loggedout indicator: ' + indicatorRegex + ' -> ' +
                auth.set_logged_out_indicator(contextid=contextId,
                                        loggedoutindicatorregex=indicatorRegex))

    # Define the users
    users = zap.users
    if createUser:
        for user in userList:
            userName = user.get('name')
            print('Create user ' + userName + ':')
            userId = users.new_user(contextid=contextId, name=userName)
            userIdList.append(userId)
            pprint('User ID: ' + userId + '; username -> ' +
                    users.set_user_name(contextid=contextId, userid=userId,
                                        name=userName) +
                    '; credentials -> ' +
                    users.set_authentication_credentials(contextid=contextId,
                        userid=userId,
                        authcredentialsconfigparams=user.get('credentials')) +
                    '; enabled -> ' +
                    users.set_user_enabled(contextid=contextId, userid=userId,
                                           enabled=True))

# Enable all passive scanners (it's possible to do a more specific policy by
# setting needed scan ID: Use zap.pscan.scanners() to list all passive scanner
# IDs, then use zap.scan.enable_scanners(ids) to enable what you want
pprint('Enable all passive scanners -> ' +
        zap.pscan.enable_all_scanners())

ascan = zap.ascan
# Define if a new scan policy is used
if useScanPolicy:
    ascan.remove_scan_policy(scanpolicyname=scanPolicyName)
    pprint('Add scan policy ' + scanPolicyName + ' -> ' +
            ascan.add_scan_policy(scanpolicyname=scanPolicyName))
    for policyId in range(0, 5):
        # Set alert Threshold for all scans
        ascan.set_policy_alert_threshold(id=policyId,
                                         alertthreshold=alertThreshold,
                                         scanpolicyname=scanPolicyName)
        # Set attack strength for all scans
        ascan.set_policy_attack_strength(id=policyId,
                                         attackstrength=attackStrength,
                                         scanpolicyname=scanPolicyName)
    if isWhiteListPolicy:
        # Disable all active scanners in order to enable only what you need
        pprint('Disable all scanners -> ' +
                ascan.disable_all_scanners(scanpolicyname=scanPolicyName))
        # Enable some active scanners
        pprint('Enable given scan IDs -> ' +
                ascan.enable_scanners(ids=ascanIds,
                                      scanpolicyname=scanPolicyName))
    else:
        # Enable all active scanners
        pprint('Enable all scanners -> ' +
                ascan.enable_all_scanners(scanpolicyname=scanPolicyName))
        # Disable some active scanners
        pprint('Disable given scan IDs -> ' +
                ascan.disable_scanners(ids=ascanIds,
                                       scanpolicyname=scanPolicyName))
else:
    print('No custom policy used for scan')
    scanPolicyName = None

# Open URL inside ZAP
pprint('Access target URL ' + target)
core.access_url(url=target, followredirects=True)
for url in applicationURL:
    pprint('Access URL ' + url)
    core.access_url(url=url, followredirects=True)
# Give the sites tree a chance to get updated
time.sleep(2)

# Launch Spider, Ajax Spider (if useAjaxSpider is set to true) and
# Active scans, with a context and users or not
forcedUser = zap.forcedUser
spider = zap.spider
ajax = zap.ajaxSpider
scanId = 0
print('Starting Scans on target: ' + target)
if useContextForScan:
    for userId in userIdList:
        print('Starting scans with User ID: ' + userId)

        # Spider the target and recursively scan every site node found
        scanId = spider.scan_as_user(contextid=contextId, userid=userId,
                url=target, maxchildren=None, recurse=True, subtreeonly=None)
        print('Start Spider scan with user ID: ' + userId +
                '. Scan ID equals: ' + scanId)
        # Give the spider a chance to start
        time.sleep(2)
        while (int(spider.status(scanId)) < 100):
            print('Spider progress: ' + spider.status(scanId) + '%')
            time.sleep(2)
        print('Spider scan for user ID ' + userId + ' completed')

        if useAjaxSpider:
            # Prepare Ajax Spider scan
            pprint('Set forced user mode enabled -> ' +
                    forcedUser.set_forced_user_mode_enabled(boolean=True))
            pprint('Set user ID: ' + userId + ' for forced user mode -> ' +
                        forcedUser.set_forced_user(contextid=contextId,
                            userid=userId))
            # Ajax Spider the target URL
            pprint('Ajax Spider the target with user ID: ' + userId + ' -> ' +
                        ajax.scan(url=target, inscope=None))
            # Give the Ajax spider a chance to start
            time.sleep(10)
            while (ajax.status != 'stopped'):
                print('Ajax Spider is ' + ajax.status)
                time.sleep(5)
            for url in applicationURL:
                # Ajax Spider every url configured
                pprint('Ajax Spider the URL: ' + url + ' with user ID: ' +
                        userId + ' -> ' +
                        ajax.scan(url=url, inscope=None))
                # Give the Ajax spider a chance to start
                time.sleep(10)
                while (ajax.status != 'stopped'):
                    print('Ajax Spider is ' + ajax.status)
                    time.sleep(5)
            pprint('Set forced user mode disabled -> ' +
                    forcedUser.set_forced_user_mode_enabled(boolean=False))
            print('Ajax Spider scan for user ID ' + userId + ' completed')

        # Launch Active Scan with the configured policy on the target url
        # and recursively scan every site node
        scanId = ascan.scan_as_user(url=target, contextid=contextId,
                userid=userId, recurse=True, scanpolicyname=scanPolicyName,
                method=None, postdata=True)
        print('Start Active Scan with user ID: ' + userId +
                '. Scan ID equals: ' + scanId)
        # Give the scanner a chance to start
        time.sleep(2)
        while (int(ascan.status(scanId)) < 100):
            print('Active Scan progress: ' + ascan.status(scanId) + '%')
            time.sleep(2)
        print('Active Scan for user ID ' + userId + ' completed')

else:
    # Spider the target and recursively scan every site node found
    scanId = spider.scan(url=target, maxchildren=None, recurse=True,
            contextname=None, subtreeonly=None)
    print('Scan ID equals ' + scanId)
    # Give the Spider a chance to start
    time.sleep(2)
    while (int(spider.status(scanId)) < 100):
        print('Spider progress ' + spider.status(scanId) + '%')
        time.sleep(2)
    print('Spider scan completed')

    if useAjaxSpider:
        # Ajax Spider the target URL
        pprint('Start Ajax Spider -> ' + ajax.scan(url=target, inscope=None))
        # Give the Ajax spider a chance to start
        time.sleep(10)
        while (ajax.status != 'stopped'):
            print('Ajax Spider is ' + ajax.status)
            time.sleep(5)
        for url in applicationURL:
            # Ajax Spider every url configured
            pprint('Ajax Spider the URL: ' + url + ' -> ' +
                    ajax.scan(url=url, inscope=None))
            # Give the Ajax spider a chance to start
            time.sleep(10)
            while (ajax.status != 'stopped'):
                print('Ajax Spider is ' + ajax.status)
                time.sleep(5)
        print('Ajax Spider scan completed')

    # Launch Active scan with the configured policy on the target url and
    # recursively scan every site node
    scanId = zap.ascan.scan(url=target, recurse=True, inscopeonly=None,
        scanpolicyname=scanPolicyName, method=None, postdata=True)
    print('Start Active scan. Scan ID equals ' + scanId)
    while (int(ascan.status(scanId)) < 100):
        print('Active Scan progress: ' + ascan.status(scanId) + '%')
        time.sleep(5)
    print('Active Scan completed')

# Give the passive scanner a chance to finish
time.sleep(5)

# If you want to retrieve alerts:
## pprint(zap.core.alerts(baseurl=target, start=None, count=None))

# To retrieve ZAP report in XML or HTML format
## print('XML report')
## core.xmlreport()
print('HTML report:')
pprint(core.htmlreport())

if shutdownOnceFinished:
    # Shutdown ZAP once finished
    pprint('Shutdown ZAP -> ' + core.shutdown())
