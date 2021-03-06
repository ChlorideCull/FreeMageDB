import time
class FreeMageDB(object):
    """
    The FreeMageDB supports all types of file formats, as well as
    tagging. It's philosophy is simplicity over performance, as
    well as leaving error handling to the API user. This means
    that it's YOUR responsibility to handle SQL errors.
    """
    def __init__(self, DBAPI2Connector, UserID=0):
        """
        Load a session with the specified UserID for R/W, as well as UID 0 for R.
        """
        self.connector = DBAPI2Connector
        if type(UserID) != int:
            raise Exception("User type invalid!")
        self.user = UserID
    
    
    def get_tags(self, all_users=False):
        """
        Returns a list of all tag names.
        """
        cur = self.connector.cursor()
        if all_users:
            cur.execute("SELECT TagName FROM freemage_data")
        else:
            cur.execute("SELECT TagName FROM freemage_data WHERE "
                        "UsID=0 OR UsID=?", (self.user,))
        output = []
        for x in cur.fetchall():
            output.append(x[0])
        cur.close()
        return output
    
    
    
    def get_files(self):
        """
        Returns a list of all file IDs.
        """
        cur = self.connector.cursor()
        cur.execute("SELECT UniqueID FROM freemage_files WHERE UsID=0 OR UsID=?"
                    , (self.user,))
        output = []
        for x in cur:
            output.append(x[0])
        cur.close()
        return output
    
    
    
    def get_file_info(self, FileUID):
        """
        Gets info about the FileUID. Returns a dictionary containing "filenames"
        which is a list of filenames; "timestamp", a UNIX timestamp; "userid", 
        an integer specifying the owner and "tags", a list of tags which may or
        may not be available as the current user.
        """
        cur = self.connector.cursor()
        output = {"filenames": [], "timestamp": 0, "tags": []}
        cur.execute(("SELECT FileNamesCSV,Timestamp,TagsCSV,UsID"
                    " FROM freemage_files WHERE UniqueID=?"), (FileUID,))
        curout = cur.fetchone()
        for x in curout[0].split(","):
            output["filenames"].append(x)
        if curout[2] != None:
            for x in curout[2].split(","):
                output["tags"].append(x)
        output["timestamp"] = curout[1]
        output["userid"] = curout[3]
        cur.close()
        return output
    
    
    def get_files_from_tags(self, TagNameList):
        """
        Returns a list of file IDs that's a member of all tags in TagNameList.

        Works by keeping a counter on how many times each image is present,
        which might not be that optimized on large databases.
        Patches welcome.
        """
        cur = self.connector.cursor()
        output = {}
        outputlist = []
        for tag in TagNameList:
            cur.execute(("SELECT FileUIDsCSV FROM freemage_data WHERE TagName=?"
                        " AND (UsID=0 OR UsID=?)"), (tag, self.user))
            for y in cur.fetchone()[0].split(","):
                output[y] = output.get(y, 0) + 1
        for x in output:
            if (output[x] == len(TagNameList)) and (x != ''):
                outputlist.append(int(x))
        cur.close()
        return outputlist
    
    
    
    def make_tag(self, TagName):
        """
        Creates an empty tag with the specified name.
        """
        if ((TagName in self.get_tags()) or ((self.user == 0) and 
                    (TagName in self.get_tags(all_users=True)))):
            raise Exception("Tag already exists")
        cur = self.connector.cursor()
        cur.execute("INSERT INTO freemage_data VALUES (?, ?, '')",
                    (self.user, TagName))
        self.connector.commit()
        cur.close()
    
    
    
    def make_file(self, FileNameList):
        """
        Creates a file entry pointing to the paths located at FileNameList, 
        returning the UID.
        """
        cur = self.connector.cursor()
        FileNamesCSV = ""
        for x in FileNameList:
            FileNamesCSV += x + ","
        FileNamesCSV = FileNamesCSV.rstrip(",")
        Timestamp = int(time.time())
        cur.execute(("INSERT INTO freemage_files (UsID,FileNamesCSV,Timestamp)"
                    " VALUES (?, ?, ?)"), (self.user, FileNamesCSV, Timestamp))
        self.connector.commit()
        cur.execute(("SELECT UniqueID FROM freemage_files WHERE "
                    "FileNamesCSV=? AND Timestamp=? AND UsID=?"), 
                    (FileNamesCSV, Timestamp, self.user))
        toreturn = cur.fetchone()[0]
        cur.close()
        return toreturn
    
    
    
    def add_file_tag(self, FileUID, Tag):
        """
        Adds the Tag to the FileUID.
        """
        tags = self.get_file_info(FileUID)["tags"]
        if Tag in tags:
            raise ValueError("Tag is already on this file")
        else:
            tags.append(Tag)
        self.set_file_tags(FileUID, tags)
    
    
    
    def remove_file_tag(self, FileUID, Tag):
        """
        Removes the Tag from the FileUID.
        """
        tags = self.get_file_info(FileUID)["tags"]
        if Tag not in tags:
            raise ValueError("Tag is not on this file")
        else:
            del tags[tags.index(Tag)]
        self.set_file_tags(FileUID, tags)
    
    
    
    def set_file_tags(self, FileUID, NewTags):
        """
        Set the tags of FileUID to the NewTags-list.
        """
        cur = self.connector.cursor()
        FileInfo = self.get_file_info(FileUID)
        if (FileInfo["userid"] != self.user) and (self.user != 0):
            raise Exception("Not allowed to change other users image")
            return
        OldTags = FileInfo["tags"]
        DeletedTags = [x for x in OldTags if not x in NewTags]
        AddedTags = [x for x in NewTags if not x in OldTags]
    
        def _process_query(FileUID, x, delete):
            FileList = self.get_files_from_tags([x])
            if delete:
                del FileList[FileList.index(FileUID)]
            else:
                FileList.append(FileUID)
            outputcsv = ""
            for y in FileList:
                outputcsv += str(y) + ","
            outputcsv = outputcsv.rstrip(",")
            cur.execute(("UPDATE freemage_data SET FileUIDsCSV=? WHERE"
                        " TagName=? AND (UsID=? OR UsID=0)"), (outputcsv, x, self.user))

        for x in DeletedTags:
            _process_query(FileUID, x, True)
        for x in AddedTags:
            _process_query(FileUID, x, False)
        
        outputcsv = ""
        for x in NewTags:
            outputcsv += x + ","
        outputcsv = outputcsv.rstrip(",")
        cur.execute(("UPDATE freemage_files SET TagsCSV=? WHERE"
                    " UniqueID=? AND UsID=?"), (outputcsv, FileUID, self.user))
        self.connector.commit()
        cur.close()
