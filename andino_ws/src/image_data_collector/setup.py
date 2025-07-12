import os
from glob import glob
from setuptools import setup, find_packages

package_name = 'image_data_collector'

setup(
    name=package_name,
    version='0.0.0',
    # Automatically find all packages (directories with __init__.py)
    packages=find_packages(exclude=['test']),
    
    # Files to include in the installation
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Include your launch files if you have any
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        # Include scripts directory
        (os.path.join('lib', package_name), glob('scripts/*.py')),
    ],
    
    # Dependencies needed to run the code
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='pi',
    maintainer_email='pi@todo.todo',
    description='A package to collect image data from a ROS topic.',
    license='TODO: License declaration',
    tests_require=['pytest'],
    
    # This is where we define the executable script
    entry_points={
        'console_scripts': [
            # 'executable_name = package_name.folder.file_name:main'
            'image_saver = image_data_collector.scripts.image_saver:main',
        ],
    },
)