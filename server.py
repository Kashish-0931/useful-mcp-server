
from mcp.server.fastmcp import FastMCP
from datetime import datetime
import json
import re

mcp = FastMCP("Useful Tools MCP Server")


# TOOL 1: Calculator
@mcp.tool()
def calculate(a: float, b: float, operation: str) -> dict:
    """Perform addition, subtraction, multiplication or division."""

    operations = {
        "add": lambda: a + b,
        "subtract": lambda: a - b,
        "multiply": lambda: a * b,
        "divide": lambda: a / b
    }

    if operation not in operations:
        return {"error": "Use add, subtract, multiply or divide"}

    if operation == "divide" and b == 0:
        return {"error": "Cannot divide by zero"}

    return {"result": operations[operation]()}


# TOOL 2: Text Analyzer
@mcp.tool()
def analyze_text(text: str) -> dict:
    """Count words, characters, sentences and lines in text."""

    sentences = len(re.findall(r'[.!?]+', text))

    return {
        "characters": len(text),
        "words": len(text.split()),
        "sentences": sentences,
        "lines": len(text.splitlines())
    }


# TOOL 3: Date Calculator
@mcp.tool()
def calculate_date_difference(date1: str, date2: str) -> dict:
    """Calculate days between two dates in YYYY-MM-DD format."""

    try:
        first = datetime.strptime(date1, "%Y-%m-%d")
        second = datetime.strptime(date2, "%Y-%m-%d")

        return {
            "date1": date1,
            "date2": date2,
            "difference_in_days": abs((second - first).days)
        }
    except ValueError:
        return {"error": "Use YYYY-MM-DD date format"}


# TOOL 4: JSON Validator
@mcp.tool()
def validate_json(json_text: str) -> dict:
    """Validate JSON input and return parsed data or an error."""

    try:
        data = json.loads(json_text)
        return {
            "valid": True,
            "parsed_data": data
        }
    except json.JSONDecodeError as e:
        return {
            "valid": False,
            "error": str(e)
        }


# TOOL 5: Text Slug Generator
@mcp.tool()
def generate_slug(text: str) -> dict:
    """Convert text into a URL-friendly slug."""

    slug = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

    return {"original_text": text, "slug": slug}


if __name__ == "__main__":
    import os
    mcp.settings.host = "0.0.0.0"
    mcp.settings.port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="streamable-http")