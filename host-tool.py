# coding: utf-8

import datetime
import logging
import re
import sys

# Constants
APP_NAME = 'HostTool'
AUTHOR = 'Ned'
DATETIME_FORMAT = "%Y%m%d.%H%M%S"
LOG_FILE = APP_NAME + '.log'
LOG_FORMAT = "%(asctime)s %(levelname)-7s %(message)s"
HOSTS_FILE = '/etc/hosts'
HOST_URL_REGEX = r"^\d+(?:\.\d+){3}\s+(\w.*$)"
OUT_FILE_PREFIX='host-urls-'
OUT_FILE_EXT='.txt'


class HostToolError(Except)



class HostsTool:
    # Interface -------------------------

    def addNewUrls(self):
        # Read hosts file
        pass

    def getUrls(self):
        logging.info('Returning host URLs')

        return self._getHostsUrls()

    def mergeUrls(self, mergedFilename):
        pass


    def writeUrlsToFile(self):
        urls = self._getHostsUrls()
        outFilename = self._getOutputFilename()

        logging.info('Writing %s URLs to file %s' % (len(urls), outFilename))

        with open(outFilename, 'w') as outFile:
            for url in urls:
                outFile.write(url + '\n')

            outFile.close()            


    def turnFacebook(self, onOff):
        if onOff is True:
            logging.info('Turning Facebook ON')
        else:
            logging.info('Turning Facebook OFF')

    def turnSpecial(self, onOff):
        if onOff is True:
            logging.info('Turning Special ON')
        else:
            logging.info('Turning Special OFF')


    # Private --------------------------

    def _getHostsUrls(self):
        hostLines = []

        try:
            with open(HOSTS_FILE, 'r') as hostsFile:
                hostLines = hostsFile.read().splitlines()
                hostsFile.close()
        except IOError:
            logging.error("Hosts file '%s' not found" % HOSTS_FILE)
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

        logging.info("Found %s URLs in hosts file" % len(urls))

        return sorted(urls)

    def _getOutputFilename(self):
        now = datetime.datetime.now().strftime(DATETIME_FORMAT)
        return OUT_FILE_PREFIX + now + OUT_FILE_EXT


    def _hashUrl(self, url):
        return 'blah'

    def _unhashUrl(self, hash):
        return 'blah'
            

def initLog():
    format = logging.Formatter(LOG_FORMAT)

    fileHandler = logging.FileHandler(LOG_FILE)
    screenHandler = logging.StreamHandler()

    fileHandler.setFormatter(format)
    screenHandler.setFormatter(format)

    fileHandler.setLevel(logging.DEBUG)
    screenHandler.setLevel(logging.DEBUG)

    logging.getLogger('').addHandler(fileHandler)
    logging.getLogger('').addHandler(screenHandler)
    logging.getLogger('').setLevel(logging.DEBUG)

    logging.debug('Log initialized')


def printUsage():
    print('\n------------------------------------------------------\n')
    print('Usage: host-tool [-merge urlFile mergedFile] [-union file1 file2 outFile] [-f on/off]\n')
    print('-union    file1 file2 outFile, where if outFile is "STDOUT", print to screen')
    print('-merge    combine urlFile urls with hosts --> mergedFile')
    print('-f        turn facebook access ON or OFF\n')


def handleMerge(hostsTool, urlHostsFile, mergedFile):
    logging.info('Merging URLs from local hosts and %s to: %s' % (urlHostsFile, mergedFile))


def handleUnion():
    pass




# main
if '__main__' == __name__:
    initLog()

    args = sys.argv
    numArgs = len(args)

    # possibleArgs = [
    #     '-merge', 'urlFile', 'mergedFile',
    #     '-compare', 'file1', 'file2', 'outFile',
    #     '-f', ''
    # ]

    # operations = {
    #     '-merge': 
    # }

    if numArgs <= 1 or numArgs > 9:
        printUsage()
        sys.exit(1)

    hostsTool = HostsTool()

    # Check -merge
    try:
        mergeIndex = args.index('-merge')
        logging.debug('-merge is at index %s' % mergeIndex)

        urlFileIndex = mergeIndex + 1
        mergeFileIndex = urlFileIndex + 1
        mergedFile = ''
        urlFile = ''

        try:
            urlFile = args[urlFileIndex]
        except IndexError:
            logging.error('-merge urlFile missing')
            printUsage()
            sys.exit(1)

        try:
            mergedFile = args[mergeFileIndex]
        except IndexError:
            logging.error('-merge mergedFile missing')
            printUsage()
            sys.exit(1)

        handleMerge(hostsTool, urlFile, mergedFile)


    except ValueError:
        logging.debug('-merge argument not present')
    except HostToolError as error:
        logging.debug('Error performing action: %s' % error)


    #ht = HostTool()
    #ht.writeUrlsToFile()
