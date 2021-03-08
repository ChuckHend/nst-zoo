from setuptools import setup

setup(
    name="nst-processor",
    entry_points="""
    [console_scripts]
    nst-processor=nst_zoo.batch_processing.io:cli
    """
)