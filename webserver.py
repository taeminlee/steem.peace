#-*- coding: utf-8 -*-
from kyoukai import Kyoukai, HTTPRequestContext
from kyoukai.util import as_html

import json

def run_server():
    kyk = Kyoukai("example_app")

    @kyk.route("/")
    async def index(ctx: HTTPRequestContext):
        with open("index.html") as f:
            return as_html(f.read())

    @kyk.route("/data")
    async def data(ctx: HTTPRequestContext):
        with open('db.json', 'r') as db:
            R = json.load(db)
            output = {"data" : list(map(lambda r:[r['timestamp'], "<a href='https://steemit.com/@%s' target='_blank'>%s</a>" % (r['voter'],r['voter']), "<a href='https://steemit.com/@%s' target='_blank'>%s</a>" % (r['author'],r['author']), int(r['weight'])/100, "<a href='%s' target='_blank'>%s</a>" % ("https://steemit.com/@%s/%s" % (r['author'], r['permlink']), r['title'])],R['_default'].values()))}
            return json.dumps(output), 200, {"Content-Type": "application/json"}
        
    kyk.run()

if __name__ == "__main__":
    run_server()