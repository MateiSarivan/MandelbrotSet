from setuptools import setup, find_packages

setup(
    name="manset",
    version="0.1",
    description="Mandelbrot set implementation",
    long_description="Mandelbrot set implementation",
    author="Ioan-Matei Sarivan",
    author_email="ioanms@mp.aau.dk",
    packages=find_packages(),
    package_dir={
        "manset": "manset"
        },
    entry_points={
        "console_scripts": [
            "manset=manset.__init__:manset_gui"
        ]
    },
    install_requires=[
        "numpy"
    ],
    zip_safe=False,
    keywords="manset",
    classifiers=[
        "Development Status :: Experimental",
        "Intended Audience :: Researchers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8"
    ]
)
