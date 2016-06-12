#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This is a modified version of Hashsync (http://thb.lt/blog/2013/fast-ftp-sync-for-jekyll.html)
# based on Thibault Polge - modifications by Raphael Zimmermann <hi@raphael.li>
#
# Copyright (c) 2012-2013 Thibault Polge <http://thb.lt>. All rights reserved.
#
# This program is free software: GPL version 3 or later <http://www.gnu.org/licenses/>.
#

import ftplib
import hashlib
import os
import ssl
import tempfile

SOURCE = '_site/'
HASH_FILE_NAME = '.sync_hashes'

HOST = os.getenv('FTP_HOST')
USER = os.getenv('FTP_USER')
PASSWORD = os.getenv('FTP_PASSWORD')
DIRECTORY = os.getenv('FTP_DIRECTORY')


def main():
    # verify weather the FTP credentials are set
    assert os.path.isdir(SOURCE), 'No such directory "{0}".'.format(SOURCE)
    assert HOST, 'missing environment variable "FTP_HOST"!'
    assert USER, 'missing environment variable "FTP_USER"!'
    assert PASSWORD, 'missing environment variable "FTP_PASSWORD"!'
    assert DIRECTORY, 'missing environment variable "FTP_DIRECTORY"!'

    print('Connecting....')
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = False
    context.load_default_certs()

    dest = ftplib.FTP_TLS(context=context)
    dest.encoding = 'utf-8'
    dest.connect(HOST)

    print('Logging in...')
    dest.login(USER, PASSWORD)
    dest.cwd(DIRECTORY)

    print('Loading remote hash cache.')
    try:
        destHashes = []
        dest.retrlines('RETR {0}'.format(HASH_FILE_NAME), lambda l: destHashes.append(l))
        destHashes = {x.split('\t')[0]: x.split('\t')[1] for x in destHashes}
    except Exception as e:
        print('Can not load remote hash file: {0}'.format(str(e)))
        print('Everything will be pushed.')
        destHashes = {}

    print('Computing local hashes.')
    sourceHashes = hashdir('')

    # Compute difference
    added = [x for x in sourceHashes if x not in destHashes.keys()]
    modified = [x for x in sourceHashes if x in destHashes.keys() and not sourceHashes[x] == destHashes[x]]
    deleted = [x for x in destHashes if x not in sourceHashes.keys()]

    print('{0} added, {1} modified and {2} removed.'.format(
          plural_of_files(added), plural_of_files(modified), plural_of_files(deleted)))

    for f in sorted(added + modified):
        if sourceHashes[f] == 'directory':
            dest.mkd(f)
        else:
            print('Uploading {0} ....'.format(f))
            command = 'STOR ' + f
            dest.storbinary(command, open(fullpath(f), 'rb'))

    for f in deleted:
        print('Delete:\t'+f)
        if destHashes[f] == 'directory':
            dest.rmd(f)
        else:
            try:
                dest.delete(f)
            except:
                pass

    print('Sending hashes...')
    hashes = tempfile.NamedTemporaryFile('w')
    for h in sourceHashes.items():
        hashes.write('{0}\t{1}\n'.format(h[0], h[1]))
    hashes.flush()

    dest.storbinary('STOR ' + HASH_FILE_NAME, open(hashes.name, 'rb'))

    dest.quit()
    dest.close()


def fullpath(path, path2=None):
    if path2:
        path = os.path.join(path, path2)
    return os.path.join(SOURCE, path)


def hashdir(path):
    ret = {}
    for file_path in os.listdir(fullpath(path)):
        if os.path.isdir(fullpath(path, file_path)):
            sub_directory = os.path.join(path, file_path)
            ret[sub_directory] = 'directory'
            ret.update(hashdir(sub_directory))
        else:
            try:
                hash_sha1 = hashlib.sha1()
                with open(fullpath(path, file_path), 'rb') as f:
                    for chunk in iter(lambda: f.read(4096), b''):
                        hash_sha1.update(chunk)
                ret[os.path.join(path, file_path)] = hash_sha1.hexdigest()
            except Exception as e:
                print('Can not compute hash for {0}:\t{1}'.format(fullpath(path, file_path), e))
    return ret


def plural_of_files(files):
    count = len(files)
    noun = 'file'
    if count != 1:
        noun = 'files'
    return '{0} {1}'.format(count, noun)

if __name__ == '__main__':
    main()
