def params_adapter(args):
    params = {}
    params["query_str"] = args.name if args.name else None
    params["size"] = args.size if args.size else None
    return params

def create_query(params):
    query = {
        "size": 0,
        "query": {"wildcard": {"pangolin_lineage": {"value": params["query_str"]}}},
        "aggs": {"lineage": {"terms": {"field": "pangolin_lineage.keyword", "size": 10000}}},
    }
    return query

def parse_response(resp = {}, size = None):
    path_to_results = ["aggregations", "lineage", "buckets"]
    buckets = resp
    for i in path_to_results:
        buckets = buckets[i]
    flattened_response = [{"name": i["key"], "total_count": i["doc_count"]} for i in buckets]
    if size:
        try:
            size = int(size)
        except Exception:
            return {"success": False, "results": [], "errors": "Invalide size value"}
        flattened_response = sorted(flattened_response, key=lambda x: -x["total_count"])
        flattened_response = flattened_response[:size]
    return flattened_response
