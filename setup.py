from setuptools import setup, find_packages

setup(
    name='efb-message-merge',
    packages=find_packages(),
    version='0.1.0',
    description='message merge',
    author='QQ-War',
    author_email="undefined@example.com",
    url='https://github.com/QQ_War/efb_message_merge.git',
    include_package_data=True,
    install_requires=[
        "ehforwarderbot"
    ],
    entry_points={
        "ehforwarderbot.middleware":"QQ_War.message_merge=efb_message_merge:MessageMergeMiddleware",
    }
    )
