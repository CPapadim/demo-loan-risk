import os
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import cPickle as pickle

class s3_connect(object):

    def __init__(self, access, secret, bucketname):
        self.conn = S3Connection(access, secret)
        self.bucketname = bucketname

    def get_bucket(self):
        return self.conn.get_bucket(self.bucketname, validate=False)

    def push_file_to_s3(self, path, key=None, string=False):
        """Take in a path or string (specify string True for serialized objects) and key, push to default S3"""

        if key:
            name = key
        elif key is None and not(string):
            parts = path.split('/')
            name = str(parts[len(parts)-1])
        else:
            print "Can't push a string to S3 without a key. Please specify a key."
            return

        k = name.replace(' ', '-')

        s3_key = Key(self.get_bucket())
        s3_key.key = k

        if not string:
            s3_key.set_contents_from_file(open(path, 'r'))
            print "Sent file %s to S3 with key '%s'" % (path, k)
        else:
            s3_key.set_contents_from_string(path)
            print "Sent string to S3 with key '%s'" % (k)

    def pull_file_from_s3(self, key, tmp_localdir=''):
        s3_bucket = self.get_bucket()
        payload = s3_bucket.get_key(key)
        if not os.path.exists(os.path.dirname(tmp_localdir+key)):
            os.makedirs(os.path.dirname(tmp_localdir+key))

        local_file = payload.get_contents_to_filename(tmp_localdir+key)
        print "Grabbed %s from S3. Local file %s is now available." % (key, tmp_localdir+key)

    def pull_pickle_from_s3(self, key, tmp_localdir=''):
        local_path = tmp_localdir+key
        local_dir = os.path.dirname(local_path)
        if not os.path.exists(os.path.dirname(tmp_localdir+key)):
            os.makedirs(os.path.dirname(tmp_localdir+key))

        s3_bucket = self.get_bucket()
        payload = s3_bucket.get_key(key)
        local_file = payload.get_contents_to_filename(local_path)
        print "Grabbed %s from S3. Local file %s is now available." % (key, key)
        return pickle.load(open(local_path, 'rb'))

    def s3_ls(self, key):
        s3_bucket = self.get_bucket()
        path_name = '/'.join(key.split('/')[1:])
        files = list(s3_bucket.list(path_name))
        return [file.name for file in files]
