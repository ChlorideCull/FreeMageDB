#!/usr/bin/env python3
import FreeMage
import sqlite3

def main(filename, userid=0, debug=False):
    print("FreeMageDB Console")
    print("Connected to " + filename + " as User " + str(userid))
    fmgdb = FreeMage.FreeMageDB(sqlite3.connect(filename), userid)
    print()
    while True:
        try:
            query = input("FMDB> ")
            qargv = query.split(" ")
            if qargv[0] == "quit":
                exit(0)
            elif qargv[0] == "help":
                print("quit - leave program")
                print("add")
                print("   tag - creates a tag")
                print("   file - creates a file")
                print("tag - sets tags of a file")
                print("list")
                print("   tags - lists all tags")
                print("   files - lists all files")
                print("info - get image info")
            elif qargv[0] == "add":
                if len(qargv) != 2:
                    print("incorrect usage, see help")
                else:
                    if qargv[1] == "tag":
                        tagname = input("Name: ")
                        print("making tag " + tagname)
                        fmgdb.make_tag(tagname)
                        print("done")
                    elif qargv[1] == "file":
                        fn_output = []
                        while True:
                            fn = input("File name (blank to finish): ")
                            if fn != "":
                                fn_output.append(fn + ",")
                            else:
                                break
                        print("making file")
                        idimg = fmgdb.make_file(fn_output)
                        print("made file ID " + str(idimg))
                        print("done")
                    else:
                        print("incorrect usage, see help")
            elif qargv[0] == "tag":
                idimg = int(input("ID: "))
                tag_output = []
                while True:
                    tag = input("Tag (blank to finish): ")
                    if tag != "":
                        tag_output.append(tag)
                    else:
                        break
                print("setting tags of " + str(idimg))
                fmgdb.set_file_tags(idimg, tag_output)
                print("done")
            elif qargv[0] == "list":
                if len(qargv) != 2:
                    print("incorrect usage, see help")
                elif qargv[1] == "tags":
                    for x in fmgdb.get_tags():
                        amount = len(fmgdb.get_files_from_tags([x]))
                        print(x + ", " + str(amount) + " images")
                elif qargv[1] == "files":
                    outputstr = ""
                    for x in fmgdb.get_files():
                        outputstr += str(x)
                    print(outputstr)
            elif qargv[0] == "info":
                fileid = int(input("File ID: "))
                filedata = fmgdb.get_file_info(fileid)
                print("Filenames: " + str(filedata["filenames"]))
                print("Tags: " + str(filedata["tags"]))
                print("Timestamp: " + str(filedata["timestamp"]))
                print("Owner: " + str(filedata["userid"]))
                print()
            else:
                print("unknown command")
        except sqlite3.Error:
            if not debug:
                print("sqlite error occured")
            else:
                raise
        except Exception:
            if not debug:
                print("misc error occured")
            else:
                raise

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        main(sys.argv[1])
    elif len(sys.argv) == 3:
        main(sys.argv[1], userid=int(sys.argv[2]))
    elif (len(sys.argv) == 4) and (sys.argv[3] == "debug"):
        main(sys.argv[1], userid=int(sys.argv[2]), debug=True)
    else:
        print("Usage:" + sys.argv[0] + " <database> [UserID]")
