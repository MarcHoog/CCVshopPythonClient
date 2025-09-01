import json
import httpx

from typing import List, Tuple, Dict, Any
from selectolax.parser import HTMLParser
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

URL = "https://demo.ccvshop.nl"
BASE_URL = "https://demo.ccvshop.nl"

def fetch_html(url: str) -> str:
    headers = {"User-Agent": "my-scraper/0.1"}
    timeout = httpx.Timeout(20.0, connect=10.0)
    with httpx.Client(follow_redirects=True, headers=headers, timeout=timeout) as client:
        r = client.get(url)
        r.raise_for_status()  # raises on 4xx/5xx
        return r.text

def fetch_schema(url: str):
    headers = {"User-Agent": "my-scraper/0.1"}
    timeout = httpx.Timeout(20.0, connect=10.0)
    with httpx.Client(follow_redirects=True, headers=headers, timeout=timeout) as client:
        r = client.get(url)
        r.raise_for_status()

        try:
            jr = r.json()
        except json.JSONDecodeError:
            print(f"Couldn't Decoce json {url}")
            return None

        return jr


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
            })


        if description:
            resources.append({
                "name": resource_name,
                "description": description,
                "operations": operations
            })

    return resources



def get_schemas_and_endpoints(base_url: str) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    if base_url[-1] == "/":
        base_url = base_url[:-1]

    html = fetch_html(f"{base_url}/API/Docs/")
    endpoints = extract_resource_description(html)
    schemas = {}
    for i in endpoints:
        for o in i.get('operations', []):
            schema_link = o.get('schema_link')
            if schema_link:
                if schema_link not in schemas:
                    schema = fetch_schema(f"{BASE_URL}{schema_link}")
                    schemas[schema_link] = schema
                o['schema'] = schemas[schema_link]

    return endpoints, schemas

def create_folder(path: str | Path) -> Path:
    """Create a folder if it does not exist and return the Path."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p

def create_file(folder: str | Path, file_name: str, content: str = "", overwrite: bool = False) -> Path:
    """
    Create a file inside the given folder.
    """
    folder_path = Path(folder)
    folder_path.mkdir(parents=True, exist_ok=True)

    file_path = folder_path / file_name

    if file_path.exists() and not overwrite:
        return file_path  # leave existing file untouched

    file_path.write_text(content, encoding="utf-8")
    return file_path


if __name__ == "__main__":
    env = Environment(loader=FileSystemLoader("generator/templates"))
    endpoints, schemas = get_schemas_and_endpoints(BASE_URL)
    ccv_folder = create_folder("ccv")
    endpoint_folder = create_folder("ccv/endpoints")
    ccv_folder = create_folder("ccv")


    template = env.get_template("client.py.j2")
    render = template.render(categories = endpoints)
    create_file(ccv_folder, "client.py", render, True)


    template = env.get_template("api/__init__.py.j2")
    render = template.render(categories = endpoints)
    create_file(endpoint_folder, "__init__.py", render, True)





    template = env.get_template("api/endpoint.py.j2")
    for cat in endpoints:
        render = template.render(**cat)
        create_file(endpoint_folder, f'{cat['name'].lower()}.py', render, True)


    ...
