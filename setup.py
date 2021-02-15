from setuptools import setup
import unittest


def main():
    setup(name='aprs2mqtt',
          packages=['aprs2mqtt'],
          test_suite='aprs2mqtt',
          entry_points={
              'console_scripts': [
                  'aprs2mqtt = aprs2mqtt.__main__:main'
              ]})


if __name__ == '__main__':
    main()
