# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # Proxy setting
  if Vagrant.has_plugin?("vagrant-proxyconf")
    config.proxy.http     = "http://127.0.0.1:1080/"
    config.proxy.https    = "http://127.0.0.1:1080/"
    config.proxy.no_proxy = "localhost,127.0.0.1,.example.com"
  end
  
  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "ubuntu/xenial64"

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  config.vm.network "forwarded_port", guest: 8000, host: 8080

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  
  config.vm.provider "virtualbox" do |vb|
    # Customize the amount of memory on the VM:
    vb.memory = "1024"
    vb.cpus = 2
  end
  
  # View the documentation for the provider you are using for more
  # information on available options.

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell", inline: <<-SHELL
     apt-get update
     sudo apt-get install -y python3-pip sqlite redis-server redis-tools htop
     sudo pip3 install flask flask-migrate flask-script flask-sqlalchemy redis gunicorn gevent
     cd /vagrant
     python3 app.py db upgrade
     echo "cd /vagrant" >> ~/.bashrc
  SHELL
end
