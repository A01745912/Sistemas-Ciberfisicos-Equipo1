from setuptools import setup
import os 
from glob import glob

package_name = 'com_mqtt'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*.launch.py'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ricardo',
    maintainer_email='ricardo@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'nodo_talker = com_mqtt.nodo_talker:main',
            'lisros_pubmqtt = com_mqtt.lisros_pubmqtt:main',
            'lismqtt = com_mqtt.lismqtt:main',
            'pub_json = com_mqtt.pub_json:main',
            'cammqtt = com_mqtt.cammqtt:main',
        ],
    },
)
