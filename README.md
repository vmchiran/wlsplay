# Introduction
__wlsplay__ is a Vagrant project for setting up a local environment for Oracle WebLogic Server with a base WebLogic domain.  
PROJ_HOME=wlsplay

The project is used to create a virtual machine for VirtualBox, containing:
* Centos 7 64-bit
* JDK 7
* WebLogic 11g
* WebLogic domain base_domain

# Prerequisites
The project was tested on a laptop with Windows 10 64-bit and virtualization enabled.
* VirtualBox - latest; project was tested on version 5.2.22
* Vagrant - latest; project was tested on version 2.2.2
* Vagrant plugins:
	* mandatory, to enable VirtualBox guest additions optimization: `vagrant plugin install vagrant-vbguest`
* Software packages present in `PROJ_HOME\software\`. The software packages versions should follow the [Oracle FMW 11g Certification Matrix](https://www.oracle.com/technetwork/middleware/downloads/fmw-11gr1certmatrix.xls)

# Customizations
`PROJ_HOME\Vagrantfile` and `PROJ_HOME\provisioning\group_vars\all.yml`

# Provisioning
## Step 1
On Windows, open cmd in the project folder PROJ_HOME and run:
`vagrant up`

This step creates a virtual machine with:
- base is the vagrant box `centos/7`  
  project was tested on box_version 1811.01, which installs basic CentOS 7.5
- Network: NAT for SSH, Host-Only Adapter for TCP (e.g. to access the WebLogic console from a browser on the Windows host)

- Mounted folders
	- `/vagrant_provisioning` from `PROJ_HOME\provisioning`
	- `/vagrant_software` from `PROJ_HOME\software`
	- `/vagrant_share` from `PROJ_HOME\share`

- Ansible - latest; project was tested on version 2.7.4
- Ansible provisioning with playbook wls-11g-provisioning.yml
	- Update packages, install tree and unzip
	- OS user and group for WebLogic
	- Folder structure for WebLogic installation and next steps
	- JDK 7 Update 171
	- WebLogic 11g (10.3.6.0) generic

## Step 2
Connect to the virtual machine via SSH:
### Option a - SSH from Windows shell
Run `vagrant ssh` from cmd prompt anywhere in the path. If there are multiple virtual machines running, use `vagrant ssh <name of vm>` to connect to the correct one.
### Option b - PuTTY with PuTTYgen
This is another way to use if you want to connect to the VM with putty or mRemoteNG. 
Use puttygen to convert the open ssh private key generated by Vagrant. The key is located in the project folder: `PROJ_HOME\.vagrant\machines\wls\virtualbox\private_key`. Convert the key and save it as `private_key.ppk`. 
For details, follow this guide: https://www.cnx-software.com/2012/07/20/how-use-putty-with-an-ssh-private-key-generated-by-openssh/  
Now you can setup a connection in putty to host: localhost, port: 2222 (default is 2222, see the output from `vagrant up` command for confirmation), SSH Auth with ppk key above.

## Step 3
SSH connect to the VM as user `vagrant` and execute the playbook wls-11g-domain-setup.yml

	cd /vagrant_provisioning
	ansible-playbook wls-11g-domain-setup.yml -i inventory

This step will:
- create a basic WebLogic domain and the default user `weblogic`
- configure AdminServer as a service and start the AdminServer

__Now you have a local env fully provisioned and running.__

# How To
## How to access WebLogic
Access the WebLogic console from a browser on the host machine: `http://172.16.0.10:7001/console`  
Use the IP address configured in Vagrantfile and use the default WebLogic port 7001.  
Use the credentials defined in `PROJ_HOME\provisioning\group_vars\all.yml` as weblogic_admin and weblogic_admin_pass, typically weblogic/welcome1.

## How to start/stop the AdminServer
AdminServer is setup as a linux service and will start automatically when booting the VM.  
To manually start/stop the service, use: `sudo systemctl start wls_adminserver` and `sudo systemctl stop wls_adminserver`

## How to control the VM
The VM must be provisioned successfully.  
Either use VirtualBox to control the VM, or use Vagrant commands.  
On Windows, open cmd in the project folder PROJ_HOME and run:
- `vagrant status`
- `vagrant suspend` - fast, saves the machine state; can be followed by `vagrant resume` or `vagrant up`
- `vagrant halt` - gracefully shutdown the machine
- `vagrant reload` - gracefully shuts down and restarts the machine
- `vagrant destroy` - cleans the host of all the VM files. Shared folders and `.vagrant` folder remain. You should delete manually the folder `PROJ_HOME\.vagrant`

# References and Inspiration
* https://www.taniarascia.com/what-are-vagrant-and-virtualbox-and-how-do-i-use-them/
* https://www.cnx-software.com/2012/07/20/how-use-putty-with-an-ssh-private-key-generated-by-openssh/
* http://jeremykendall.net/2013/08/09/vagrant-synced-folders-permissions/
* https://www.vagrantup.com/docs/provisioning/ansible_intro.html
* Vagrant Essentials (video), By Eduonix, June 2017, Complete Guide for Managing Infrastructure Using Vagrant, Packt Mapt
* https://tuhrig.de/resizing-vagrant-box-disk-space/
* https://github.com/sprotheroe/vagrant-disksize
* https://technology.amis.nl/2018/07/27/virtualbox-networking-explained/
* https://www.qualogy.com/techblog/oracle/introducing-weblogic-to-systemd#
* https://stackoverflow.com/questions/17895256/creating-symbolic-link-protocol-error
* https://github.community/t5/Project-Development-Help-and/Ansible-playbook-setup-py-permission-denied/td-p/5924
* https://blog.davesnigier.com/changing-ansible-temporary-directory/
* http://www.mydailytutorials.com/ansible-blockinfile-module-adding-multiple-lines/
* 11g WLST Command Reference: https://docs.oracle.com/cd/E23943_01/web.1111/e13813/reference.htm#WLSTC119
* Vagrant Documentation: https://www.vagrantup.com/docs/index.html
* Ansible Documentation: https://docs.ansible.com/
