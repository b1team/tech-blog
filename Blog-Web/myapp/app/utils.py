def row2dict(row):
    d = dict(row.__dict__)
    d.pop("_sa_instance_state")
    return d
