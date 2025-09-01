import requests
import logging
import json
import time

from typing import Dict, Optional, Any, Union
from ccv.auth import CCVAuth
from ccv.result import CCVShopResult
import ccv.endpoints as endpoint

logger = logging.getLogger(__name__)

class CCVClient():

    def __init__(self,
                 base_url: str,
                 public_key: str,
                 private_key: str,
                 verify_ssl: bool = True):


        base_url = base_url.strip('/')
        self.auth = CCVAuth(base_url, public_key, private_key)
        self.base_url = base_url
        self.default_headers = {
            "Content-Type": "application/json"
        }

        self.verifiy_ssl = verify_ssl
        self.Root = endpoint.Root(self)
        self.Affiliatenetworks = endpoint.Affiliatenetworks(self)
        self.Apicredentialdevicesettings = endpoint.Apicredentialdevicesettings(self)
        self.Apicredentialdevices = endpoint.Apicredentialdevices(self)
        self.Appcodeblocks = endpoint.Appcodeblocks(self)
        self.Appconfig = endpoint.Appconfig(self)
        self.Appmessages = endpoint.Appmessages(self)
        self.Apppsp = endpoint.Apppsp(self)
        self.Apppsppaymethods = endpoint.Apppsppaymethods(self)
        self.Appstorecategories = endpoint.Appstorecategories(self)
        self.Apps = endpoint.Apps(self)
        self.Attributecombinationphotos = endpoint.Attributecombinationphotos(self)
        self.Attributecombinations = endpoint.Attributecombinations(self)
        self.Attributevalues = endpoint.Attributevalues(self)
        self.Attributes = endpoint.Attributes(self)
        self.Basesubscriptions = endpoint.Basesubscriptions(self)
        self.Brands = endpoint.Brands(self)
        self.Cashups = endpoint.Cashups(self)
        self.Categories = endpoint.Categories(self)
        self.Categoryproductlayouts = endpoint.Categoryproductlayouts(self)
        self.Categorytree = endpoint.Categorytree(self)
        self.Colors = endpoint.Colors(self)
        self.Conditions = endpoint.Conditions(self)
        self.Credentials = endpoint.Credentials(self)
        self.Creditpointmutations = endpoint.Creditpointmutations(self)
        self.Creditpoints = endpoint.Creditpoints(self)
        self.Currentsubscriptions = endpoint.Currentsubscriptions(self)
        self.Currentuser = endpoint.Currentuser(self)
        self.Dashboardblocks = endpoint.Dashboardblocks(self)
        self.Dashboards = endpoint.Dashboards(self)
        self.Disabledpaymethods = endpoint.Disabledpaymethods(self)
        self.Discountcoupons = endpoint.Discountcoupons(self)
        self.Domains = endpoint.Domains(self)
        self.Fiscaltransactionsignatures = endpoint.Fiscaltransactionsignatures(self)
        self.Geozonecountries = endpoint.Geozonecountries(self)
        self.Invoicelabels = endpoint.Invoicelabels(self)
        self.Invoicenotifications = endpoint.Invoicenotifications(self)
        self.Invoicerows = endpoint.Invoicerows(self)
        self.Invoices = endpoint.Invoices(self)
        self.Labels = endpoint.Labels(self)
        self.Languages = endpoint.Languages(self)
        self.Mailingaddresses = endpoint.Mailingaddresses(self)
        self.Mailinglists = endpoint.Mailinglists(self)
        self.Marktplaatscategories = endpoint.Marktplaatscategories(self)
        self.Merchant = endpoint.Merchant(self)
        self.Orderaffiliatenetworks = endpoint.Orderaffiliatenetworks(self)
        self.Orderlabels = endpoint.Orderlabels(self)
        self.Ordermessages = endpoint.Ordermessages(self)
        self.Ordernotes = endpoint.Ordernotes(self)
        self.Ordernotifications = endpoint.Ordernotifications(self)
        self.Orderrowattributevalues = endpoint.Orderrowattributevalues(self)
        self.Orderrowcalculator = endpoint.Orderrowcalculator(self)
        self.Orderrows = endpoint.Orderrows(self)
        self.Orders = endpoint.Orders(self)
        self.Packages = endpoint.Packages(self)
        self.Paymethods = endpoint.Paymethods(self)
        self.Productattachments = endpoint.Productattachments(self)
        self.Productattributesets = endpoint.Productattributesets(self)
        self.Productattributevalues = endpoint.Productattributevalues(self)
        self.Productkeywords = endpoint.Productkeywords(self)
        self.Productlabels = endpoint.Productlabels(self)
        self.Productphotos = endpoint.Productphotos(self)
        self.Productproperties = endpoint.Productproperties(self)
        self.Productpropertygroups = endpoint.Productpropertygroups(self)
        self.Productpropertyoptions = endpoint.Productpropertyoptions(self)
        self.Productpropertyvalues = endpoint.Productpropertyvalues(self)
        self.Productqueries = endpoint.Productqueries(self)
        self.Productrelevant = endpoint.Productrelevant(self)
        self.Productreviews = endpoint.Productreviews(self)
        self.Productshippingcosts = endpoint.Productshippingcosts(self)
        self.Productstaggeredprices = endpoint.Productstaggeredprices(self)
        self.Producttaxtariffexceptions = endpoint.Producttaxtariffexceptions(self)
        self.Producttocategories = endpoint.Producttocategories(self)
        self.Producttopropertygroups = endpoint.Producttopropertygroups(self)
        self.Productvariations = endpoint.Productvariations(self)
        self.Productvideos = endpoint.Productvideos(self)
        self.Products = endpoint.Products(self)
        self.Quotationrows = endpoint.Quotationrows(self)
        self.Quotations = endpoint.Quotations(self)
        self.Redirects = endpoint.Redirects(self)
        self.Returnrows = endpoint.Returnrows(self)
        self.Returns = endpoint.Returns(self)
        self.Servicecategories = endpoint.Servicecategories(self)
        self.Services = endpoint.Services(self)
        self.Settings = endpoint.Settings(self)
        self.Status = endpoint.Status(self)
        self.Subscriptiondiscountcoupons = endpoint.Subscriptiondiscountcoupons(self)
        self.Subscriptionupgrades = endpoint.Subscriptionupgrades(self)
        self.Suppliers = endpoint.Suppliers(self)
        self.Takeoutslots = endpoint.Takeoutslots(self)
        self.Terminalreceipts = endpoint.Terminalreceipts(self)
        self.Translations = endpoint.Translations(self)
        self.Usercategoryadjustments = endpoint.Usercategoryadjustments(self)
        self.Usergroupcategoryadjustments = endpoint.Usergroupcategoryadjustments(self)
        self.Usergroupproductadjustments = endpoint.Usergroupproductadjustments(self)
        self.Usergroupstaggeredpriceadjustments = endpoint.Usergroupstaggeredpriceadjustments(self)
        self.Usergroups = endpoint.Usergroups(self)
        self.Userproductadjustments = endpoint.Userproductadjustments(self)
        self.Userstaggeredpriceadjustments = endpoint.Userstaggeredpriceadjustments(self)
        self.Users = endpoint.Users(self)
        self.Webhooks = endpoint.Webhooks(self)
        self.Webshops = endpoint.Webshops(self)


    def _do(
        self,
        method: str,
        uri: str,
        params: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
        raw: Any = None,
        attempt = 0,
        max_attempt = 3,
        wait_before_retry = 60
    ) -> CCVShopResult:  # type: ignore | It litteraly errors

        uri = f"/{uri.strip('/')}/"
        url = f"{self.base_url}{uri}"

        data = None
        if body != None:
            try:
                data = json.dumps(body)
            except json.decoder.JSONDecodeError:
                raise ValueError(f"Body: {body} couldn't be decoded into json, if you want to send a non decodable body, or raw  ")

        resp = requests.request(
            url=url,
            method=method.upper(),
            params=params,
            auth=self.auth,
            headers=self.default_headers,
            verify=self.verifiy_ssl,
            data=data or raw
        )

        resp_data = None
        if resp.ok:
            try:
                if method in ["POST", "GET"]:
                    resp_data = resp.json()
            except json.decoder.JSONDecodeError as e:
                raise e
            return CCVShopResult(status_code=resp.status_code,
                                       data=resp_data)

        if not resp.ok:
            logger.warning(f"Non-2xx response: {resp.status_code} - {resp.text}")
            if resp.status_code == 429:  # Rate-limiting response
                attempt += 1
                if attempt <= max_attempt:  # Retry up to 3 times
                    logger.info(f"Rate limit hit. Retrying attempt {attempt} after a delay {wait_before_retry} seconds...")
                    time.sleep(wait_before_retry)
                    return self._do(
                        method,
                        uri,
                        params,
                        body,
                        raw,
                        attempt
                    )

            try:
                resp.raise_for_status()
            except requests.HTTPError as e:
                raise Exception(f"HTTP request failed: {e}") from e

    def _get(
        self,
        uri_path: str,
        **params
    ) -> CCVShopResult:
        """
        Internal helper to perform GET requests.

        Args:
            uri_path: Relative URI path to append to base URL.
            **params: Optional query parameters as keyword arguments.

        Returns:
            requests.Response: The HTTP response object.
        """
        return self._do(
            method="GET",
            uri=uri_path,
            params=params if params else None,
        )

    def _put(self, uri_path: str, body: Dict[str, Any]) -> CCVShopResult:
        """
        Internal helper to perform PATCH requests.

        Args:
            uri_path: Relative URI path to append to base URL.
            body: body Data to send

        Returns:
            requests.Response: The HTTP response object.
        """
        return self._do(
            method="PUT",
            uri=uri_path,
            body=body,
        )


    def _post(self,uri_path: str, body: Dict[str, Any]) -> CCVShopResult:
        """
        Internal helper to perform POST requests.

        Args:
            uri_path: Relative URI path to append to base URL.
            body: body Data to send

        Returns:
            requests.Response: The HTTP response object.
        """
        return self._do(
            method="POST",
            uri=uri_path,
            body=body,
        )

    def _patch(self, uri_path: str, body: Dict[str, Any]) -> CCVShopResult:
        """
        Internal helper to perform PATCH requests.

        Args:
            uri_path: Relative URI path to append to base URL.
            body: body Data to send

        Returns:
            requests.Response: The HTTP response object.
        """
        return self._do(
            method="PATCH",
            uri=uri_path,
            body=body,
        )


    def _delete(self, uri_path: str) -> CCVShopResult:
        """
        Internal helper to perform DELETE requests.

        Args:
            uri_path: Relative URI path to append to base URL.

        Returns:
            requests.Response: The HTTP response object.
        """
        return self._do(
            method="DELETE",
            uri=uri_path,
        )

    def _get_paged(self, uri_path: str, per_page: int, total_pages: Union[str, int], **params: Any):
        """
        Fetch paginated results from a CCV Shop API endpoint.

        This helper performs multiple GET requests to retrieve paginated data. It supports
        both a fixed number of pages or automatic pagination by setting total_pages="all".

        Args:
            uri_path: The relative URI path to request (e.g., "products").
            per_page: Number of items per request (min 1, max 250).
            total_pages: Number of pages to retrieve, or "all" to fetch until 'next' is empty.
            **params: Additional query parameters to pass to the request.

        Returns:
            CCVShopResult: Combined result with all paginated items in result.data["items"].
        """

        if isinstance(total_pages, str):
            if total_pages == "all":
                total_pages = -1
            else:
                raise ValueError(f"Total Pages `{total_pages}` can only be defined as 'all' when string")
        elif isinstance(total_pages, int) and (total_pages < -1 or total_pages == 0):
            raise ValueError("Total Pages cannot be below -1 or 0 when int")

        per_page = max(1, min(per_page, 250))
        start = 0
        results = []
        pages = 0

        status_code = -1

        while pages < total_pages or total_pages == -1:
            paging_params = {
                "start": start,
                "size": per_page,
            }
            result = self._get(uri_path, **{**params, **paging_params})
            status_code = result.status_code

            if not result.data:
                raise ValueError("Something unexpected happend")

            items = result.data.get("items")
            if items is None:
                raise ValueError("Expected 'items' field missing in response")
            results.extend(items)

            pages += 1
            next_link = result.data.get("next")

            if not next_link:
                break

            start += per_page

        return CCVShopResult(status_code=status_code, data={
            "items": results,
            "total_pages": pages,
            "total_items": len(results),
        })
