import sys
import importlib

def create_gan_object(db, pid, expid, gan_dir, gan_file, gan_class):
    """
    The method to create gan object from given dir, file and class
    """
    sys.path.append(gan_dir)
    my_module = importlib.import_module(gan_file)
    gan = eval("my_module.{}(db, pid, expid)".format(gan_class))

    return gan