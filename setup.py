import setuptools

setuptools.setup(name='kangrouter-py',
                 version='1.0.0',
                 description='Python client for the KangRouter transportation service optimizer.',
                 long_description=open('README.md').read().strip(),
                 author='TheSolvingMachine',
                 author_email='support@thesolvingmachine.com',
                 url='https://thesolvingmachine.com/kangrouter',
                 py_modules=['kangrouter','tsm.common.app'],
                 install_requires=['requests'],
                 license='Apache',
                 keywords='optimization, pickup and delivery, shortest path',
                 classifiers=['Development Status :: 3 - Alpha',
                              'Intended Audience :: Developers',
                              'License :: OSI Approved :: Apache Software License',
                              'Topic :: Scientific/Engineering :: Artificial Intelligence',
                              'Programming Language :: Python :: 2',
                              'Programming Language :: Python :: 3'])