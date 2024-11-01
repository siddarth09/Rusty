from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'rusty'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'config'), glob('config/*.lua'))
        
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='siddarth',
    maintainer_email='siddarth.dayasagar@gmail.com',
    description='Rusty:warehouse robot',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'gps_node = rusty.gps:main',
            'bayes_node=rusty.bayes_filter:main',
            'kalman_f = rusty.kalman_filter:main',
            'ekf = rusty.ekf_for_gps:main',
        ],
    },
)
