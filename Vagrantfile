VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/precise64"

  config.vm.network :forwarded_port, guest: 5432, host: 5431
  
end
