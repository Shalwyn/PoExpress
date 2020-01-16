parameters = {
    "query": {
        "status": {
            "option": "online"
        },
        "name": itemparse.splitlines()[2],
        "stats": [{
            "type": "and",
            "filters": {
                "map_filters": {
                    "filters": {
                        "map_tier": splitmap[2]
                    }
                }
            }

        }]
    },
    "sort": {
        "price": "asc"
    }
}
