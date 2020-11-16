from setuptools import setup, find_packages
import versioneer

setup(
    name="winglets",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Winglet solver",
    author_email="enrique.millanvalbuena@gmail.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["numpy", "scipy", "fluids", "AeroSandbox", "pandas"],
)