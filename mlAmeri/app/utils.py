def input_path(instance, filename):
    file_type = filename.split(".")[-1]
    return f"{instance.__class__.__name__}/{instance.id}.{file_type}"


def coutput_path(instance, filename):
    file_type = filename.split(".")[-1]
    return f"{instance.__class__.__name__}/M{instance.id}.{file_type}"


def moutput_path(instance, filename):
    file_type = filename.split(".")[-1]
    return f"{instance.__class__.__name__}/C{instance.id}.{file_type}"


def cmoutput_path(instance, filename):
    file_type = filename.split(".")[-1]
    return f"{instance.__class__.__name__}/CM{instance.id}.{file_type}"
