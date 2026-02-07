import re
from typing import Any, Dict, Optional

import requests


def extract_report_id(url: str) -> Optional[str]:
    match = re.search(r"reportid=([^&]+)", url)
    if match:
        return str(match.group(1))
    return None


def get_hansard_content(api_response: Dict[str, Any]) -> Optional[str]:
    # v1 format: post-2012
    if "resultHTML" in api_response:
        content = api_response["resultHTML"]["content"]
        return str(content) if content is not None else None

    # v0 format: pre-2012
    if "htmlContent" in api_response:
        content = api_response["htmlContent"]
        return str(content) if content is not None else None

    return None


def fetch_hansard(report_id: str) -> Dict[str, Any]:
    url = f"https://sprs.parl.gov.sg/search/getHansardTopic/?id={report_id}"
    headers = {"Content-Type": "application/json", "Accept": "application/json, text/plain, */*"}
    response = requests.post(url, headers=headers, json={})
    result: Dict[str, Any] = response.json()
    return result
