def denormalize_json(obj, parent_key=None):
    """
    Denormalizes json to a flat view, e.g.
    {
        "key1": "value1",
        "key2": {
            "sub_key1": "sub_value1",
            "sub_key2": "sub_value2"
        },
        "key3": [
            {
                "sub_key1": "sub_value1",
                "sub_key2": "sub_value2"
            },
            {
                "sub_key1": "sub_value1",
                "sub_key2": "sub_value2"
            }
        ]
    }

    transforms into:
    {
        "key1": "value1",
        "key2.sub_key1": "sub_value1",
        "key2.sub_key2": "sub_value2",
        "key3[0].sub_key1: "sub_value1",
        "key3[0].sub_key2: "sub_value2",
        "key3[1].sub_key1: "sub_value1",
        "key3[1].sub_key2: "sub_value2",
    }

    """
    denormalized = {}

    if isinstance(obj, list):
        for index, item in enumerate(obj):
            key = "{}[{}]".format(parent_key, index)
            denormalized.update(denormalize_json(item, key))
    else:
        for key, value in obj.items():
            if parent_key:
                key = "{}.{}".format(parent_key, key)

            if isinstance(value, str):
                denormalized[key] = value
            else:
                denormalized.update(denormalize_json(value, key))

    return denormalized
