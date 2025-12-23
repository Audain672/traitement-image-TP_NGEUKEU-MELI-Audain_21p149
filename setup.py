from setuptools import setup, find_packages

setup(
    name="image_processor",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'opencv-python>=4.5.0',
        'numpy>=1.19.0',
        'Pillow>=8.0.0',
    ],
    entry_points={
        'console_scripts': [
            'image-processor=image_processor.main:main',
        ],
    },
    python_requires='>=3.6',
)
