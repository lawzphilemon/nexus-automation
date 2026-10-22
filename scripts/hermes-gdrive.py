"""Drive steps the Hermes google-workspace skill lacks: upload HTML as a Google Doc, list a Doc's comments.

Run with the same Python as Hermes' google_api.py, so its OAuth token and googleapiclient are used:
  python scripts/hermes-gdrive.py upload-doc <file.html> --name "<Doc name>" [--parent <folder id>]
  python scripts/hermes-gdrive.py comments <file id>
"""
import argparse
import json
import os
import pathlib
import sys

DOC = "application/vnd.google-apps.document"


def doc_metadata(name, parent=""):
    meta = {"name": name, "mimeType": DOC}  # this mimeType makes Drive convert the HTML into a Doc
    if parent:
        meta["parents"] = [parent]
    return meta


def format_comments(comments):
    out = []
    for c in comments:
        if c.get("deleted"):
            continue
        quote = (c.get("quotedFileContent") or {}).get("value", "")
        out.append({"comment": c.get("content", ""), "on": quote, "resolved": bool(c.get("resolved")),
                    "replies": [r.get("content", "") for r in c.get("replies", []) if not r.get("deleted")]})
    return out


def drive():
    home = os.environ.get("HERMES_HOME") or next(
        (p for p in (os.path.join(os.environ.get("LOCALAPPDATA", ""), "hermes"), os.path.expanduser("~/.hermes"))
         if os.path.isdir(p)), "")
    sys.path.insert(0, str(pathlib.Path(home) / "skills" / "productivity" / "google-workspace" / "scripts"))
    from google_api import build_service
    return build_service("drive", "v3")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    up = sub.add_parser("upload-doc")
    up.add_argument("path")
    up.add_argument("--name", required=True)
    up.add_argument("--parent", default="")
    cm = sub.add_parser("comments")
    cm.add_argument("file_id")
    a = ap.parse_args()

    if a.cmd == "upload-doc":
        from googleapiclient.http import MediaFileUpload
        r = drive().files().create(body=doc_metadata(a.name, a.parent),
                                   media_body=MediaFileUpload(a.path, mimetype="text/html"),
                                   fields="id, name, mimeType, webViewLink").execute()
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        svc, items, token = drive(), [], None
        while True:
            r = svc.comments().list(fileId=a.file_id, pageToken=token, pageSize=100, includeDeleted=False,
                                    fields="nextPageToken, comments(content, quotedFileContent, resolved, deleted, replies(content, deleted))").execute()
            items += r.get("comments", [])
            token = r.get("nextPageToken")
            if not token:
                break
        print(json.dumps(format_comments(items), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
