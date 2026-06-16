def knowledge_agent(query):
    # Clean the query (remove question words)
    cleaned = (
        query.lower()
        .replace("what is", "")
        .replace("who is", "")
        .replace("explain", "")
        .replace("tell me about", "")
        .replace("define", "")
        .strip()
    )

    # 1. Try direct Wikipedia summary
    try:
        direct_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{cleaned.replace(' ', '_')}"
        response = requests.get(direct_url).json()

        if "extract" in response and response["extract"]:
            return response["extract"]

        if "description" in response and response["description"]:
            return response["description"]

    except Exception:
        pass

    # 2. Fallback: Wikipedia search
    try:
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={cleaned}&format=json"
        search_results = requests.get(search_url).json()

        if "query" in search_results and search_results["query"]["search"]:
            top_title = search_results["query"]["search"][0]["title"]

            summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{top_title.replace(' ', '_')}"
            summary_response = requests.get(summary_url).json()

            if "extract" in summary_response and summary_response["extract"]:
                return summary_response["extract"]

            if "description" in summary_response and summary_response["description"]:
                return summary_response["description"]

    except Exception:
        pass

    return "No Wikipedia information found."
