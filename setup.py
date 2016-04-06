from setuptools import *                                                                                                                                                                             

kwargs = {
        "author" : "Frankie Primerano",
        "author_email" : "max00355@gmail.com",
        "description" : "A micro web framework with a production ready web server.",
        "name" : "feather",
        "packages" : ["feather", "feather/utils"],
        "version" : "0.2.0",
}

setup(**kwargs)
