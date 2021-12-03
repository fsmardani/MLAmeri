def input_path(instance, filename):
    file_type = filename.split(".")[-1]
    return f"{instance.__class__.__name__}/{instance.id}.{file_type}"
