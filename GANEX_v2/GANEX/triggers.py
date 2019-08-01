

def init_triggers(db):

    with db["trainstats"].watch() as stream:
        for change in stream:
            print("train stat table updated...!")