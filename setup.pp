# script to quickly get server up and running
# installs python3 and pip3
package { 'python3-pip':
ensure => 'present',
name   => 'python3-pip'
}
# installs pipenv
package { 'pipenv':
ensure   => 'present',
provider => 'pip3',
name     => 'pipenv'
}
# installs gunicorn
package { 'gunicorn':
ensure   => 'present',
provider => 'pip3',
name     => 'gunicorn'
}
# installs nginx
package { 'nginx':
ensure => 'present',
name   => 'nginx'
}
# installs requests via pip
package { 'requests':
provider        => 'pip3',
name            => 'requests',
install_options => '-m'
}
# installs git
package { 'git':
ensure => 'present',
name   => 'git'
}
# clones Wingmates repo
#exec { 'git clone https://github.com/nokeefe/Wingmate.git':
#cwd     => '/home',
#creates => '/home/Wingmates',
#path    => ['/usr/bin/git']
#}
# install django
package { 'django':
ensure   => 'present',
provider => 'pip3',
name     => 'django'
}
# start gunicorn instance
#exec {'tmux new-session -d 'gunicorn 0.0.0.0:8000 wingmate.wsgi:application'':
#cwd => '',
#path  =>'',
#}

