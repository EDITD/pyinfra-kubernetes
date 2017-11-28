from setuptools import find_packages, setup


if __name__ == '__main__':
    setup(
        version='0.1.1',
        name='pyinfra-kubernetes',
        author='EDITED',
        author_email='engineering@edited.com',
        url='https://github.com/EDITD/pyinfra-kubernetes',
        license='MIT',
        description='Install & bootstrap Kubernetes clusters with pyinfra.',
        packages=find_packages(),
        install_requires=('pyinfra>=0.5'),
        include_package_data=True,
    )
