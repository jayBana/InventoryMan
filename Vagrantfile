ENV['VAGRANT_DEFAULT_PROVIDER'] = 'docker'

Vagrant.configure("2") do |config|

  # this for the docker container
  config.vm.synced_folder "./G53IDS", "/home/www/G53IDS"

  config.vm.define "g53ids" do |a|
    a.vm.provider "docker" do |d|
      d.build_dir = "."
      d.build_args = ["-t=jaybana/g53ids"]
      d.ports = ["8080:80"]
      d.name = "g53ids"
      d.remains_running = true
      d.vagrant_machine = "dockerhost"
      d.vagrant_vagrantfile = "./DockerHostVagrantfile"
    end
  end
end
