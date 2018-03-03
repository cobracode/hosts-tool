# coding: utf-8

import datetime
import logging
import re
import sys

# Constants
APP_NAME = 'HostsTool'
AUTHOR = 'Ned'
DATETIME_FORMAT = "%Y%m%d.%H%M%S"
LOG_FILE = APP_NAME + '.log'
LOG_FORMAT = "%(asctime)s %(levelname)-7s %(message)s"
LOG_LEVELS = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']
HOSTS_FILE = '/etc/hosts'
HOST_URL_REGEX = r"^\d+(?:\.\d+){3}\s+(\w.*$)"
MAX_ARGS = 9
OUT_FILE_PREFIX='host-urls-'
OUT_FILE_EXT='.txt'


# Exception types
class HostToolError(Exception):
    pass




class HostsTool:
    # Interface -------------------------

    def merge(self, urlFile, outFilename):
        info("Merging URLs in %s with HOSTS into %s" % (urlFile, outFilename))

        # Read urls from urlfile
        fileUrls = self._getFileUrls(outFilename)
        debug("Read %s URLs from %s" % (len(fileUrls), outFilename))

        # Read urls from Hosts
        hostsUrls = self._getHostsUrls()
        debug("Read %s URLs from %s" % (len(hostsUrls)))

        # Add both to a set
        result = set()

        for url in fileUrls:
            result.add(url)

        for url in hostsUrls:
            result.add(url)

        self._writeUrlsToFile(result, outFilename)


    def writeUrlsToFile(self):
        urls = self._getHostsUrls()
        outFilename = self._getOutputFilename()

        self._writeUrlsToFile(urls, outFilename)     


    def turnFacebook(self, onOff):
        if onOff is True:
            info('Turning Facebook ON')
        else:
            info('Turning Facebook OFF')


    def turnSpecial(self, onOff):
        if onOff is True:
            info('Turning Special ON')
        else:
            info('Turning Special OFF')



    # Private --------------------------

    def _getFileUrls(self, filename):
        pass


    def _getHostsUrls(self):
        hostLines = []

        try:
            with open(HOSTS_FILE, 'r') as hostsFile:
                hostLines = hostsFile.read().splitlines()
                hostsFile.close()
        except IOError:
            error("Hosts file '%s' not found" % HOSTS_FILE)
            return []

        # Use regex to get host(s) from each line and add to list
        urls = set()

        for line in hostLines:
            matches = re.search(HOST_URL_REGEX, line)

            if matches is None:
                continue

            # Will be string like: ned.com jim.com
            urlsString = matches.groups()[0].split()

            for url in urlsString:
                urls.add(url)

        info("Found %s URLs in hosts file" % len(urls))

        return sorted(urls)

    def _getOutputFilename(self):
        now = datetime.datetime.now().strftime(DATETIME_FORMAT)
        return OUT_FILE_PREFIX + now + OUT_FILE_EXT


    def _hashUrl(self, url):
        return 'blah'


    def _unhashUrl(self, hash):
        return 'blah'


    def _writeUrlsToFile(self, urls, filename):
        info('Writing %s URLs to file %s' % (len(urls), filename))

        with open(filename, 'w') as outFile:
            for url in urls:
                outFile.write(url + '\n')

            outFile.close()  


def initLog(level):
    logger = logging.getLogger('')

    screenHandler = None

    # this verison of python seems to come with
    # streamhandler already, so configure it
    # rather than add a new one if it exists
    if logger.hasHandlers():
        screenHandler = logger.handlers[0]
    else:
        screenHandler = logging.StreamHandler()
        logger.addHandler(screenHandler)

    fileHandler = logging.FileHandler(LOG_FILE)

    format = logging.Formatter(LOG_FORMAT)
    fileHandler.setFormatter(format)
    screenHandler.setFormatter(format)

    fileHandler.setLevel(level)
    screenHandler.setLevel(level)

    logger.addHandler(fileHandler)
    logger.setLevel(level)

    logger.debug('Logger intialized')


def error(msg):
    logging.error(msg)

def warn(msg):
    logging.warn(msg)

def info(msg):
    logging.info(msg)

def debug(msg):
    logging.debug(msg)


def printUsage():
    print('\n------------------------------------------------------\n')
    print('Usage: host-tool [-merge urlFile mergedFile] [-union file1 file2 outFile] [-f on/off] [-w] [-l LEVEL]\n')
    print('-union    file1 file2 outFile, where if outFile is "STDOUT", print to screen')
    print('-merge    combine urlFile urls with hosts --> mergedFile')
    print('-l        log level: %s' % LOG_LEVELS)
    print('-f        turn facebook access ON or OFF')
    print('-w        write current hosts urls to file\n')


def handleMerge(hostsTool, urlHostsFile, mergedFile):
    info('Merging URLs from local hosts and %s to: %s' % (urlHostsFile, mergedFile))


def handleUnion():
    pass





def checkDoMerge(args):
    key = '-merge'

    try:
        index = args.index(key)
        debug(key + ' is at index %s' % index)

        urlFileIndex = index + 1
        urlFile = ''
        outFileIndex = urlFileIndex + 1
        outFile = ''

        try:
            urlFile = args[urlFileIndex]
        except IndexError:
            error(key + ' urlFile missing')
            printUsage()
            sys.exit(1)

        try:
            outFile = args[outFileIndex]
        except IndexError:
            error(key + ' outFile missing')
            printUsage()
            sys.exit(1)

        debug("User specified merging %s with hosts into %s" % (urlFile, outFile))

        return True, urlFile, outFile
    except ValueError:
        debug(key + ' argument not present')

    return (False, None, None)



def checkDoWrite(args):
    key = '-w'

    try:
        index = args.index(key)
        debug(key + ' is at index %s' % index)

        return True
    except ValueError:
        debug(key + ' argument not present')

    return False


def checkLogLevel(args):
    key = '-l'
    defaultLevel = 'DEBUG'

    try:
        index = args.index(key)
        # print("%s is at index %s" % (key, index))

        levelIndex = index + 1

        try:
            level = args[levelIndex]

            if level not in LOG_LEVELS:
                print("%s log level '%s' not valid. Need one of: %s.\nUsing default %s" % (key, level, LOG_LEVELS, defaultLevel))
                return defaultLevel

            return level
        except IndexError:
            print("%s log level missing. Using default of %s" % (key, defaultLevel))
            return defaultLevel

    except ValueError:
        print("%s (log level) argument not present; using %s" % (key, defaultLevel))

    return defaultLevel



# main
if '__main__' == __name__:
    args = sys.argv
    initLog(checkLogLevel(args))

    numArgs = len(args)

    if numArgs <= 1 or numArgs > MAX_ARGS:
        printUsage()
        sys.exit(1)

    doMerge, urlFile, outFile = checkDoMerge(args)
    doWrite = checkDoWrite(args)

    hostsTool = HostsTool()

    if doMerge:
        hostsTool.merge(urlFile, outFile)

    if doWrite:
        hostsTool.writeUrlsToFile()
