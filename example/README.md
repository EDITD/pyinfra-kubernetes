# pyinfra-kubernetes Example Deploy

```sh
# Install the requirements (pyinfra-kubernetes, pyinfra-etcd, pyinfra-docker)
pip install -r requirements.pip

# Boot the vagrant hosts
vagrant up

# Run the deploy against the Vagrant hosts
pyinfra @vagrant deploy.py
```
