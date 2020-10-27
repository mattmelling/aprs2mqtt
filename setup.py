from setuptools import setup


def main():
    setup(name='aprs2mqtt',
          packages=['aprs2mqtt'],
          entry_points={
              'console_scripts': [
                  'aprs2mqtt = aprs2mqtt.main:main'
              ]})


if __name__ == '__main__':
    main()
