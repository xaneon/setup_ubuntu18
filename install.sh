# presets
HOSTNAME="ubuntu"
MOUNTDIR="/media/sf_caumont/"
DBDIR="$MOUNTDIR/Dropbox"
DOTDIR="$DBDIR/Dotfiles/WHOTRSURFACE20"

sudo apt-get update
sudo apt-get install vmfs-tools -y
sudo apt-get install vmware-manager -y
sudo apt-get install vim  -y
sudo apt-get install virtualbox  -y
sudo apt-get install virtualbox-ext-pack  -y
sudo apt-get install gnome-system-tools
sudo apt install linux-headers-$(uname -r) build-essential dkms -y
# sudo ./VBoxLinuxAdditions.run
sudo apt-get install qterminal -y
sudo apt-get install firefox -y
sudo apt-get install htop -y
sudo apt-get install autojump -y
sudo apt-get install mc -y
sudo apt-get install zsh -y
sudo apt-get install tmux -y
sudo apt-get install git -y
sudo apt-get install powerline -y
sudo apt-get install python3 -y
sudo apt-get install python3-pip -y
sudo apt-get install python3-setuptools -y
sudo apt-get install python3-dev -y
sudo apt-get install python3.6 -y
sudo apt-get install python3.6-pip -y
sudo apt-get install python3.6-setuptools -y
sudo apt-get install python3.6-dev -y
sudo apt-get install virtualenv -y
sudo apt-get install virtualenvwrapper -y
sudo apt install libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev -y

# install python3.7
wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz

# settings
sudo addgroup $USER vboxsf 
sudo hostname $HOSTNAME

# links
if [ ! -f $DOTDIR/vimrc ]; then
	ln -s $MOUNTDIR/Dropbox/Dotfiles/WHOTRSURFACE20/vimrc /home/bh/.vimrc
fi
ln -s $MOUNTDIR/Dropbox/EigeneDateien /home/bh/EigeneDateien
ln -s $MOUNTDIR/Dropbox/ /home/bh/Dropbox
ln -s $MOUNTDIR/Dropbox/Dotfiles/WHOTRSURFACE20/bashrc /home/bh/.bashrc
ln -s $MOUNTDIR/Dropbox/Dotfiles/WHOTRSURFACE20/tmux.conf /home/bh/.tmux.conf
ln -s $MOUNTDIR/Dropbox/Dotfiles/WHOTRSURFACE20/jupyter /home/bh/.jupyter
ln -s $MOUNTDIR/Dropbox/Dotfiles/WHOTRSURFACE20/vim /home/bh/.vim
ln -s $MOUNTDIR/Dropbox/Dotfiles/WHOTRSURFACE20/powerline /home/bh/.powerline
