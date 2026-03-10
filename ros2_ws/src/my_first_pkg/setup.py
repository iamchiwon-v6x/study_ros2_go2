from setuptools import find_packages, setup

package_name = 'my_first_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='chiwon.song@voyagerx.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'hello = my_first_pkg.hello_node:main',
            'simple_pub = my_first_pkg.simple_publisher:main',
            'turtle_circle = my_first_pkg.turtle_circle:main',
            'add_server = my_first_pkg.add_server:main',
            'add_client = my_first_pkg.add_client:main',
            'spawn_turtle = my_first_pkg.spawn_turtle:main',
            'rotate_client = my_first_pkg.rotate_client:main',
            'rotate_server = my_first_pkg.rotate_server:main',
        ],
    },
)
