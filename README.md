# Warning

This is not activly maintained, or tested ("if somebody actually wants that message me")
It was mostly a learning experience

# CCVShop Python API Client & Generator

This project provides:
- A **code generator CLI** for creating Python clients for the [CCVShop API](https://demo.ccvshop.nl/API/Docs/).
- A **semi-generated Python library** for interacting with CCVShop endpoints.

---

## Project Structure

```
CCVShopApiClient/
├── generator/         # Code generator CLI
│   ├── __init__.py
│   ├── __main__.py
│   ├── pyproject.toml
│   └── templates/     # Jinja2 templates for code generation
├── ccv/               # Generated CCVShop API client library
│   ├── client.py
│   ├── endpoints/
│   ├── pyproject.toml
│   └── ...            # Other generated modules
├── LICENSE            # MIT License
└── README.md          # This file
```

---

## Installation

### 1. Install the Generator CLI

From the project root:

```bash
pip install -e ./generator
```

### 2. Generate the CCVShop Client Library

Run the generator CLI:

```bash
ccvshop-client-gen --base-url https://demo.ccvshop.nl --output ccv
```

Or, without installing:

```bash
python -m generator --base-url https://demo.ccvshop.nl --output ccv
```

### 3. Install the Generated Client Library

```bash
pip install -e ./ccv
```

---

## Usage

After generating and installing the client, you can use it in your Python projects:

```python
from ccv import client
from ccv.endpoints import orders, products  # Example endpoints

# Example usage
api = client.CCVShopClient(api_key="YOUR_API_KEY")
orders_list = api.orders.list()
print(orders_list)
```

_Note: The actual API surface depends on the generated endpoints and schemas._

---

## Development

- Templates for code generation are in `generator/templates/`.
- Regenerate the client library whenever the CCVShop API changes.
- Extend or customize templates for your needs.

---

## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.

---

## Contributing

Pull requests and issues are welcome! Please open an issue for bugs or feature requests.

---

## Credits

- [CCVShop API Documentation](https://demo.ccvshop.nl/API/Docs/)
- Uses [httpx](https://www.python-httpx.org/), [selectolax](https://github.com/rushter/selectolax), and [jinja2](https://jinja.palletsprojects.com/).

---
