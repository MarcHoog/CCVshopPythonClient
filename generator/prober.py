import re
import sys
import urllib.parse
from typing import List, Dict, Any, Tuple
import httpx
from selectolax.parser import HTMLParser

URL = "https://demo.ccvshop.nl/API/Docs/"

def fetch_html(url: str) -> str:
    headers = {"User-Agent": "my-scraper/0.1"}
    timeout = httpx.Timeout(20.0, connect=10.0)
    with httpx.Client(follow_redirects=True, headers=headers, timeout=timeout) as client:
        r = client.get(url)
        r.raise_for_status()  # raises on 4xx/5xx
        return r.text


def extract_resource_description(html: str):
    tree = HTMLParser(html)
    resources = []

    # iterate all resource <li>
    for res in tree.css("li.resource"):
        name = res.css_first("div.heading h3 a")
        resource_name = name.text(strip=True) if name else None

        desc_node = res.css_first("ul.endpoints li.resource_description")
        description = desc_node.text(strip=True) if desc_node else None

        operations = []
        for op in res.css("ul.endpoints li.endpoint ul.operations li.operation"):
            method_node = op.css_first("span.http_method")
            path_node = op.css_first("span.path")
            method = method_node.text(strip=True).upper() if method_node else None
            path = path_node.text(strip=True) if path_node else None

            operation_desc = None
            for li in op.css("div.content ul li"):
                text = li.text(strip=True)
                if text.lower().startswith("description:"):
                    operation_desc = text.split(":", 1)[-1].strip()
                    break

            schema_a = op.css_first("div.content ul a[href$='.json']")
            schema_link = schema_a.attributes.get("href") if schema_a else None



            operations.append({
                "description": operation_desc,
                "method": method,
                "path": path,
                "schema_link": schema_link,
                "schema": None
            })

        resources.append({
            "name": resource_name,
            "description": description,
            "operations": operations
        })

    return resources


if __name__ == "__main__":
     html = fetch_html(URL)
     items = extract_resource_description(html)
     ...
